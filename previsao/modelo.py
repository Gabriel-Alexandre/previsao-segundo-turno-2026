"""As tres estimativas do pre-registro (P, H e R) e a combinacao, como funcoes que tambem rodam no teste do passado.

Convencao: toda parte e do candidato CONTRA o PT nos votos validos (em 2026, Flavio). Lula = 100 menos isso.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from previsao.comum import ANOS, DERIV, FINALISTAS

PESOS = {"P": 0.60, "H": 0.25, "R": 0.15}
DIVISAO_OUTROS = 0.50          # parte dos outros candidatos que vai para cada finalista (parametro do autor)
PESO_2T, PESO_1T = 2.0, 1.0    # nota de acerto: 2o turno pesa o dobro
TETO_PESO = 0.25               # nenhum instituto passa de 25% do peso
JANELA_DIAS = (4, 13)          # em 2026: fim de campo de 12/out a 21/out, eleicao em 25/out (de 13 a 4 dias antes)
DATAS = {(2014, 1): date(2014, 10, 5), (2014, 2): date(2014, 10, 26), (2018, 1): date(2018, 10, 7), (2018, 2): date(2018, 10, 28),
         (2022, 1): date(2022, 10, 2), (2022, 2): date(2022, 10, 30), (2026, 1): date(2026, 10, 4), (2026, 2): date(2026, 10, 25)}

# o mesmo instituto com nomes diferentes nas bases (Ibope virou Ipec; DataPoder360 e PoderData; a Nexus e o braco de pesquisa da FSB,
# como mostra o endereco nexus.fsb.com.br; a Futura registra no TSE como 100% Cidades)
NOMES = {"Ibope": "Ipec", "Ipec (antigo Ibope)": "Ipec", "DataPoder360": "PoderData", "Real Time Big Data": "Real Time",
         "Ideia Big Data": "Ideia", "Veritá": "Verita", "FSB Pesquisa": "Nexus", "Paraná Pesquisas": "Parana Pesquisas"}


def nome(n: str) -> str:
    return NOMES.get(n, n)


# ---------------------------------------------------------------- dados da urna

def uf_votos() -> pd.DataFrame:
    return pd.read_csv(DERIV / "uf_votos.csv")


def uf_detalhe() -> pd.DataFrame:
    return pd.read_csv(DERIV / "uf_detalhe.csv")


def urna_nacional(ano: int, turno: int) -> dict:
    """Parte de cada partido nos validos (0 a 100) e os votos."""
    v = uf_votos()
    v = v[(v.ano == ano) & (v.turno == turno)].groupby("partido").votos.sum()
    return {"votos": v.to_dict(), "pct": (100 * v / v.sum()).to_dict(), "validos": int(v.sum())}


def anti_pt_urna(ano: int, turno: int) -> float:
    f = FINALISTAS[ano]
    u = urna_nacional(ano, turno)["pct"]
    if turno == 2:
        return u[f["anti"]]
    return u[f["anti"]], u[f["pt"]]


# ---------------------------------------------------------------- pesquisas do passado

def _pindograma(ano: int, turno: int) -> pd.DataFrame:
    if ano in (2014, 2018):
        a = pd.read_csv(DERIV / "copias/pindograma-late-polls-2012-2018.csv", low_memory=False)
        a = a[(a.year == ano) & (a.turno == turno)].copy()
        a["valido"] = a.valid_result  # na base, valid_result e a pesquisa nos validos; pct e a urna
    else:
        a = pd.read_csv(DERIV / "copias/pindograma-late-polls-2022.csv", low_memory=False)
        a = a[a.turno == turno].copy()
        a["valido"] = 100 * a.result / a.groupby(["NR_IDENTIFICACAO_PESQUISA", "scenario_id"]).result.transform("sum")
    a = a[(a.CD_CARGO == 1) & (a.polled_UE == "BR") & (a.estimulada == 1) & (a.NUMERO_CANDIDATO > 0)]
    a["fim"] = pd.to_datetime(a.DT_FIM_PESQUISA).dt.date
    a["n_cand"] = a.groupby(["NR_IDENTIFICACAO_PESQUISA", "scenario_id"]).NUMERO_CANDIDATO.transform("nunique")
    a["instituto"] = a.pretty_name.map(nome)
    f = FINALISTAS[ano]
    p = a.pivot_table(index=["NR_IDENTIFICACAO_PESQUISA", "scenario_id", "instituto", "fim", "n_cand"], columns="NUMERO_CANDIDATO",
                      values="valido", aggfunc="first").reset_index()
    p = p.rename(columns={f["anti"]: "anti", f["pt"]: "pt"}).dropna(subset=["anti", "pt"])
    p["ano"], p["turno"] = ano, turno
    return p[["ano", "turno", "instituto", "fim", "n_cand", "NR_IDENTIFICACAO_PESQUISA", "anti", "pt"]]


def pesquisas_passado() -> pd.DataFrame:
    return pd.concat([_pindograma(a, t) for a in (2014, 2018, 2022) for t in (1, 2)], ignore_index=True)


def ultima_antes(df: pd.DataFrame, eleicao: date, dias: tuple[int, int]) -> pd.DataFrame:
    """Ultima pesquisa de cada instituto com fim de campo entre dias[1] e dias[0] dias antes da eleicao."""
    w = df[(df.fim >= eleicao - timedelta(days=dias[1])) & (df.fim <= eleicao - timedelta(days=dias[0]))]
    return w.sort_values(["instituto", "fim", "n_cand"]).groupby("instituto").tail(1)


def erros_institutos() -> pd.DataFrame:
    """Erro da ultima pesquisa (1 a 8 dias antes) de cada instituto, em cada turno de 2014 a 2022 e no 1o turno de 2026."""
    pp = pesquisas_passado()
    out = []
    for (ano, turno), g in pp.groupby(["ano", "turno"]):
        u = ultima_antes(g, DATAS[(ano, turno)], (1, 8))
        for r in u.itertuples():
            if turno == 2:
                anti_p = 100 * r.anti / (r.anti + r.pt)
                erro = anti_p - anti_pt_urna(ano, 2)
            else:
                ua, up = anti_pt_urna(ano, 1)
                erro = ((r.anti - r.pt) - (ua - up)) / 2
            out.append({"ano": ano, "turno": turno, "instituto": r.instituto, "fim": r.fim, "anti_pesquisa": r.anti, "pt_pesquisa": r.pt, "erro": erro})
    b6 = pd.read_csv(DERIV / "copias/b6_erro_por_instituto_e_rodada.csv")
    b6 = b6[b6.rodada == "2026-1"]
    ua, up = anti_pt_urna(2026, 1)
    for r in b6.itertuples():
        out.append({"ano": 2026, "turno": 1, "instituto": nome(r.instituto), "fim": pd.Timestamp(r.fim).date(), "anti_pesquisa": r.pl,
                    "pt_pesquisa": r.pt, "erro": ((r.pl - r.pt) - (ua - up)) / 2})
    return pd.DataFrame(out)


def notas(erros: pd.DataFrame, antes_de: int) -> pd.DataFrame:
    """Nota de acerto (media ponderada do erro absoluto) e vies no 2o turno, so com eleicoes anteriores a 'antes_de'.

    Para 2026 (antes_de = 2027) entram o 1o turno de 2026 e tudo antes; no teste do passado, so as eleicoes anteriores."""
    e = erros[erros.ano < antes_de].copy()
    if e.empty:
        return pd.DataFrame(columns=["instituto", "nota", "vies_2t", "n_2t", "n_rodadas"])
    e["peso"] = np.where(e.turno == 2, PESO_2T, PESO_1T)
    e["abs"] = e.erro.abs()
    g = e.groupby("instituto")
    out = pd.DataFrame({"nota": g.apply(lambda x: (x["abs"] * x.peso).sum() / x.peso.sum()), "n_rodadas": g.size()})
    t2 = e[e.turno == 2].groupby("instituto").erro
    out["vies_2t"] = t2.mean()
    out["n_2t"] = t2.size()
    out = out.fillna({"n_2t": 0}).reset_index()
    out["n_2t"] = out.n_2t.astype(int)
    return out


# ---------------------------------------------------------------- P

def estimativa_P(pesq: pd.DataFrame, nt: pd.DataFrame, corrigir_vies: bool = True, pesar: bool = True) -> tuple[float, pd.DataFrame]:
    """pesq: instituto, anti_valido (ja uma por instituto). nt: saida de notas()."""
    d = pesq.merge(nt, on="instituto", how="left")
    for c in ("nota", "vies_2t", "n_2t", "n_rodadas"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    p75 = nt.nota.quantile(0.75) if len(nt) else np.nan
    d["tem_historico"] = d.nota.notna()
    d["nota_usada"] = d.nota.fillna(p75)
    if not pesar or d.nota_usada.isna().all():
        d["peso"] = 1.0
    else:
        d["peso"] = 1 / d.nota_usada.clip(lower=0.25) ** 2  # piso de 0,25 ponto para nenhum acerto perfeito virar peso infinito
    d["peso"] = d.peso / d.peso.sum()
    for _ in range(20):  # teto de 25%, redistribuindo o excesso
        acima = d.peso > TETO_PESO + 1e-12
        if not acima.any() or len(d) * TETO_PESO < 1:
            break
        excesso = (d.loc[acima, "peso"] - TETO_PESO).sum()
        d.loc[acima, "peso"] = TETO_PESO
        livres = ~acima
        d.loc[livres, "peso"] += excesso * d.loc[livres, "peso"] / d.loc[livres, "peso"].sum()
    n2 = d.n_2t.fillna(0)
    d["correcao"] = np.where(corrigir_vies & (n2 > 0), -d.vies_2t.fillna(0) * n2 / (n2 + 2), 0.0)
    d["anti_corrigido"] = d.anti_valido + d.correcao
    return float((d.peso * d.anti_corrigido).sum()), d


# ---------------------------------------------------------------- H

def tabela_lideranca(anos=ANOS) -> pd.DataFrame:
    out = []
    for ano in anos:
        f = FINALISTAS[ano]
        p1 = urna_nacional(ano, 1)["pct"]
        p2 = urna_nacional(ano, 2)["pct"]
        lider = f["anti"] if p1[f["anti"]] > p1[f["pt"]] else f["pt"]
        outro = f["pt"] if lider == f["anti"] else f["anti"]
        v1 = 100 * (p1[lider] / (p1[lider] + p1[outro])) * 2 - 100
        v2 = 2 * p2[lider] - 100
        out.append({"ano": ano, "lider_1t": f["anti_nome"] if lider == f["anti"] else f["pt_nome"], "lider_partido": lider,
                    "vantagem_1t": v1, "vantagem_2t": v2, "razao": v2 / v1, "lider_venceu": v2 > 0})
    return pd.DataFrame(out)


def estimativa_H(ano: int, razao=None) -> tuple[float, dict]:
    anos = [a for a in ANOS if a < ano]
    t = tabela_lideranca(anos)
    r = float(t.razao.median()) if razao is None else razao
    f = FINALISTAS[ano]
    p1 = urna_nacional(ano, 1)["pct"]
    v1_anti = 100 * (p1[f["anti"]] / (p1[f["anti"]] + p1[f["pt"]])) * 2 - 100  # vantagem do anti-PT (negativa se o PT liderou)
    return 50 + r * v1_anti / 2, {"razao_mediana": r, "vantagem_1t_anti": v1_anti, "anos": anos}


# ---------------------------------------------------------------- R

def fatores_comparecimento(antes_de: int) -> pd.Series:
    """Mediana, por UF, de validos do 2o turno / validos do 1o turno nas eleicoes anteriores."""
    d = uf_detalhe()
    d = d[d.ano < antes_de].pivot_table(index=["ano", "uf"], columns="turno", values="validos").dropna()
    return (d[2] / d[1]).groupby("uf").median()


def estimativa_R(ano: int, divisao: float = DIVISAO_OUTROS, com_fator: bool = True) -> tuple[float, pd.DataFrame]:
    f = FINALISTAS[ano]
    v = uf_votos()
    v = v[(v.ano == ano) & (v.turno == 1)]
    t = v.pivot_table(index="uf", columns="partido", values="votos", aggfunc="sum").fillna(0)
    outros = t.drop(columns=[f["anti"], f["pt"]]).sum(axis=1)
    d = pd.DataFrame({"anti_1t": t[f["anti"]], "pt_1t": t[f["pt"]], "outros_1t": outros})
    fat = fatores_comparecimento(ano) if com_fator else pd.Series(dtype=float)
    d["fator"] = fat.reindex(d.index).fillna(fat.median() if len(fat) else 1.0) if com_fator else 1.0
    d["anti_2t"] = (d.anti_1t + divisao * d.outros_1t) * d.fator
    d["pt_2t"] = (d.pt_1t + (1 - divisao) * d.outros_1t) * d.fator
    return float(100 * d.anti_2t.sum() / (d.anti_2t.sum() + d.pt_2t.sum())), d


# ---------------------------------------------------------------- combinacao

def combinar(P: float, H: float, R: float, pesos=PESOS) -> float:
    return pesos["P"] * P + pesos["H"] * H + pesos["R"] * R
