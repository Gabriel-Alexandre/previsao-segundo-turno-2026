"""Recontagem independente: refaz os numeros centrais por outro caminho, sem importar previsao.modelo.

1. Urna: os percentuais nacionais do 1o turno de 2026 contra o projeto presidente-primeiro-turno-2026 (derivacao feita em outra
   sessao, de outro arquivo do TSE) e os 2os turnos de 2014 e 2018 contra a coluna da urna da base do Pindograma.
2. Abstencao: abstencoes = aptos - comparecimento, municipio por municipio.
3. P refeito em Python puro, a partir das tabelas publicadas (pesquisa, nota, vies), com o teto de 25% feito a mao.
4. H refeito so com os votos nacionais.
5. R refeito somando as UFs a mao.
6. A combinacao e o arredondamento.
Saida: resultados/validacao_independente.csv (cada linha: numero, valor principal, valor recontado, diferenca, passou).
"""
from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
DER = RAIZ / "dados" / "derivados"
linhas = []


def conferir(nome, principal, recontado, tol):
    linhas.append({"numero": nome, "principal": principal, "recontado": recontado, "diferenca": abs(principal - recontado), "tolerancia": tol,
                   "passou": abs(principal - recontado) <= tol})


resumo = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))

# 1. urna
votos = {}
with open(DER / "uf_votos.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        k = (int(r["ano"]), int(r["turno"]), int(r["partido"]))
        votos[k] = votos.get(k, 0) + int(r["votos"])


def pct(ano, turno, partido):
    tot = sum(v for (a, t, p), v in votos.items() if a == ano and t == turno)
    return 100 * votos[(ano, turno, partido)] / tot


outro = pd.read_parquet(RAIZ.parent / "presidente-primeiro-turno-2026/dados/derivados/mun_presidente.parquet")
o26 = outro[(outro.ano == 2026) & (outro.turno == 1)]
conferir("Flávio 1º turno 2026 (%) contra o projeto do vídeo 7", pct(2026, 1, 22), 100 * o26.flavio.sum() / o26.nominais.sum(), 0.01)
conferir("Lula 1º turno 2026 (%) contra o projeto do vídeo 7", pct(2026, 1, 13), 100 * o26.lula.sum() / o26.nominais.sum(), 0.01)
pin = pd.read_csv(DER / "copias/pindograma-late-polls-2012-2018.csv", low_memory=False)
for ano, anti in ((2014, 45), (2018, 17)):
    u = pin[(pin.year == ano) & (pin.turno == 2) & (pin.CD_CARGO == 1) & (pin.polled_UE == "BR") & (pin.NUMERO_CANDIDATO == anti)].pct.dropna().iloc[0]
    conferir(f"anti-PT 2º turno {ano} (%) contra a coluna da urna do Pindograma", pct(ano, 2, anti), float(u), 0.02)

# 2. abstencao
det = pd.read_parquet(DER / "mun_detalhe.parquet")
d26 = det[(det.ano == 2026) & (det.turno == 1)]
conferir("abstenção 1º turno 2026 (%)", resumo["abstencao"]["abstencao_1t_2026"], 100 * (d26.aptos.sum() - d26.comparecimento.sum()) / d26.aptos.sum(), 0.01)

# 3. P em Python puro
p = pd.read_csv(RES / "p_pesquisas_usadas.csv").to_dict("records")
rank = pd.read_csv(RES / "institutos_ranking.csv")
p75 = statistics.quantiles(rank.nota.tolist(), n=4, method="inclusive")[2]
pesos = []
for r in p:
    nota = r["nota"] if r["nota"] == r["nota"] else p75
    pesos.append(1 / max(nota, 0.25) ** 2)
s = sum(pesos)
pesos = [w / s for w in pesos]
for _ in range(50):
    acima = [i for i, w in enumerate(pesos) if w > 0.25 + 1e-12]
    if not acima:
        break
    exc = sum(pesos[i] - 0.25 for i in acima)
    for i in acima:
        pesos[i] = 0.25
    livres = [i for i in range(len(pesos)) if i not in acima and pesos[i] < 0.25]
    sl = sum(pesos[i] for i in livres)
    for i in livres:
        pesos[i] += exc * pesos[i] / sl
P = 0.0
for r, w in zip(p, pesos):
    valido = 100 * r["flavio_total"] / (r["flavio_total"] + r["lula_total"])
    n2 = r["n_2t"] if r["n_2t"] == r["n_2t"] else 0
    corr = -r["vies_2t"] * n2 / (n2 + 2) if n2 > 0 else 0.0
    P += w * (valido + corr)
conferir("P (pesquisas)", resumo["estimativas"]["P"], P, 0.001)
conferir("soma dos pesos", 1.0, sum(pesos), 1e-9)
conferir("maior peso não passa de 25%", 0.25, max(0.25, max(pesos)), 1e-9)

# 4. H
razoes = []
for ano, anti in ((2002, 45), (2006, 45), (2010, 45), (2014, 45), (2018, 17), (2022, 22)):
    a1, t1 = pct(ano, 1, anti), pct(ano, 1, 13)
    a2 = pct(ano, 2, anti)
    lider_anti = a1 > t1
    v1 = abs(a1 - t1) / (a1 + t1) * 100
    v2 = (2 * a2 - 100) if lider_anti else (100 - 2 * a2)
    razoes.append(v2 / v1)
f1, l1 = pct(2026, 1, 22), pct(2026, 1, 13)
H = 50 + statistics.median(razoes) * ((f1 - l1) / (f1 + l1) * 100) / 2
conferir("H (histórico)", resumo["estimativas"]["H"], H, 0.001)

# 5. R
det_uf = pd.read_csv(DER / "uf_detalhe.csv")
fat = {}
for uf, g in det_uf[det_uf.ano < 2026].groupby("uf"):
    rs = []
    for ano, h in g.groupby("ano"):
        t = dict(zip(h.turno, h.validos))
        if 1 in t and 2 in t:
            rs.append(t[2] / t[1])
    fat[uf] = statistics.median(rs)
med = statistics.median(fat.values())
uv = pd.read_csv(DER / "uf_votos.csv")
uv = uv[(uv.ano == 2026) & (uv.turno == 1)]
fa = la = 0.0
for uf, g in uv.groupby("uf"):
    vv = dict(zip(g.partido, g.votos))
    out = sum(vv.values()) - vv.get(22, 0) - vv.get(13, 0)
    k = fat.get(uf, med)
    fa += (vv.get(22, 0) + 0.5 * out) * k
    la += (vv.get(13, 0) + 0.5 * out) * k
R = 100 * fa / (fa + la)
conferir("R (crescimento)", resumo["estimativas"]["R"], R, 0.001)

# 6. combinacao
F = 0.6 * P + 0.25 * H + 0.15 * R
conferir("número final de Flávio (sem arredondar)", resumo["final"]["flavio_sem_arredondar"], F, 0.001)
conferir("número final de Flávio (arredondado)", resumo["final"]["flavio"], round(F, 1), 0.0)
conferir("número final de Lula (arredondado)", resumo["final"]["lula"], round(100 - round(F, 1), 1), 0.0)
outros = sum(v for (a, t, pp), v in votos.items() if a == 2026 and t == 1 and pp not in (22, 13))
gap = votos[(2026, 1, 22)] - votos[(2026, 1, 13)]
conferir("parte dos outros que Lula precisaria", resumo["de_onde"]["parte_dos_outros_que_lula_precisa"], (outros + gap) / (2 * outros), 1e-9)

df = pd.DataFrame(linhas)
df.to_csv(RES / "validacao_independente.csv", index=False)
print(df.to_string())
print(f"\n{int(df.passou.sum())} de {len(df)} passaram")
