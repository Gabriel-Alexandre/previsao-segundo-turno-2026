"""Roda o pre-registro inteiro: notas dos institutos, P, H, R, o numero final, regras por UF, abstencao, de onde viriam os votos,
para onde foram os votos dos outros no passado (informativo), teste do passado e sensibilidade.

Saidas: resultados/RESUMO.json e as tabelas resultados/*.csv. Uso: python ferramentas/analise.py
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao import modelo as M  # noqa: E402
from previsao.comum import ANOS, DERIV, FINALISTAS, RES, salvar_json  # noqa: E402

CORTE_2026 = date(2026, 10, 21)
NOMES_PARTIDO_2026 = {22: "Flávio Bolsonaro", 13: "Lula", 70: "Augusto Cury", 14: "Renan Santos", 55: "Ronaldo Caiado", 30: "Romeu Zema"}


def tab(nome: str, df: pd.DataFrame) -> None:
    RES.mkdir(parents=True, exist_ok=True)
    df.to_csv(RES / nome, index=False)


# ------------------------------------------------------------ pesquisas de 2026

def pesquisas_2026() -> pd.DataFrame:
    w = pd.read_csv(DERIV / "pesquisas_2t_2026_wikipedia.csv")
    c = pd.read_csv(DERIV / "pesquisas_2t_2026_conferencia.csv")
    r = pd.read_csv(DERIV / "pesquisas_2t_2026_registro.csv")
    d = w.merge(c, on=["instituto", "campo_fim"]).merge(r, on=["instituto", "campo_fim"])
    d["instituto"] = d.instituto.map(M.nome)
    d["anti_valido"] = 100 * d.flavio_total / (d.flavio_total + d.lula_total)  # emenda 1: valido sempre pela conta dos totais
    d["fim"] = pd.to_datetime(d.campo_fim).dt.date
    return d


def janela(d: pd.DataFrame, so_validas: bool = True) -> pd.DataFrame:
    w = d[(d.fim >= date(2026, 10, 12)) & (d.fim <= CORTE_2026)]
    if so_validas:
        w = w[w.casou & w.conferida]
    return w.sort_values(["instituto", "fim", "amostra"]).groupby("instituto").tail(1)


# ------------------------------------------------------------ regras por UF

def regras_uf() -> tuple[pd.DataFrame, dict]:
    v = M.uf_votos()
    linhas = []
    for ano in ANOS:
        f = FINALISTAS[ano]
        nac2 = M.urna_nacional(ano, 2)["pct"]
        venc = f["anti"] if nac2[f["anti"]] > nac2[f["pt"]] else f["pt"]
        for turno in (1, 2):
            g = v[(v.ano == ano) & (v.turno == turno)]
            top = g.sort_values("votos").groupby("uf").tail(1)
            for t in top.itertuples():
                linhas.append({"ano": ano, "turno": turno, "uf": t.uf, "vencedor_uf": t.partido, "vencedor_nacional_2t": venc, "acertou": t.partido == venc})
    d = pd.DataFrame(linhas)
    resumo = d.groupby(["uf", "turno"]).acertou.agg(["sum", "count"]).unstack("turno")
    resumo.columns = [f"{a}_{t}t" for a, t in resumo.columns]
    resumo = resumo.reset_index().rename(columns={"sum_1t": "acertos_1t", "count_1t": "eleicoes_1t", "sum_2t": "acertos_2t", "count_2t": "eleicoes_2t"})
    g26 = v[(v.ano == 2026) & (v.turno == 1)]
    top26 = g26.sort_values("votos").groupby("uf").tail(1).set_index("uf").partido
    resumo["vencedor_1t_2026"] = resumo.uf.map(top26).map(NOMES_PARTIDO_2026)
    perfeitas = resumo[(resumo.acertos_1t == resumo.eleicoes_1t)]
    contagem = perfeitas.vencedor_1t_2026.value_counts().to_dict()
    return resumo.sort_values(["acertos_1t", "acertos_2t"], ascending=False), {"ufs_6_de_6_no_1t": perfeitas.uf.tolist(), "para_quem_apontam_em_2026": contagem,
                                                                                  "mg": resumo[resumo.uf == "MG"].to_dict("records")[0]}


# ------------------------------------------------------------ abstencao

def abstencao() -> tuple[pd.DataFrame, dict]:
    d = M.uf_detalhe().groupby(["ano", "turno"])[["aptos", "comparecimento", "abstencoes", "validos", "brancos", "nulos"]].sum().reset_index()
    d["abstencao_pct"] = 100 * d.abstencoes / d.aptos
    d["brancos_nulos_pct"] = 100 * (d.brancos + d.nulos) / d.comparecimento
    d["validos_pct_aptos"] = 100 * d.validos / d.aptos
    w = d.pivot_table(index="ano", columns="turno", values=["abstencao_pct", "brancos_nulos_pct", "validos"])
    hist = pd.DataFrame({"abst_1t": w["abstencao_pct"][1], "abst_2t": w["abstencao_pct"][2], "bn_1t": w["brancos_nulos_pct"][1], "bn_2t": w["brancos_nulos_pct"][2]})
    hist["delta_abst"] = hist.abst_2t - hist.abst_1t
    hist["delta_bn"] = hist.bn_2t - hist.bn_1t
    hist["razao_validos"] = w["validos"][2] / w["validos"][1]
    h = hist.loc[ANOS]
    a26 = d[(d.ano == 2026) & (d.turno == 1)].iloc[0]
    abst1 = h.abst_1t
    tendencia = np.polyfit(np.array(ANOS), abst1.values, 1)
    esperado26 = float(np.polyval(tendencia, 2026))
    info = {"abstencao_1t_2026": float(a26.abstencao_pct), "brancos_nulos_1t_2026": float(a26.brancos_nulos_pct), "aptos_2026": int(a26.aptos),
            "comparecimento_1t_2026": int(a26.comparecimento), "abstencoes_1t_2026": int(a26.abstencoes),
            "brancos_nulos_votos_1t_2026": int(a26.brancos + a26.nulos), "validos_1t_2026": int(a26.validos),
            "abstencao_1t_tendencia_2026": esperado26, "abstencao_1t_2026_menos_tendencia": float(a26.abstencao_pct) - esperado26,
            "delta_abst_mediana": float(h.delta_abst.median()), "delta_abst_min": float(h.delta_abst.min()), "delta_abst_max": float(h.delta_abst.max()),
            "delta_bn_mediana": float(h.delta_bn.median()), "razao_validos_mediana": float(h.razao_validos.median()),
            "anos_abstencao_caiu_no_2t": h.index[h.delta_abst < 0].tolist()}
    info["abstencao_2t_2026_se_mediana"] = info["abstencao_1t_2026"] + info["delta_abst_mediana"]
    return hist.reset_index(), info


# ------------------------------------------------------------ de onde viriam os votos

def de_onde(abst: dict) -> dict:
    u = M.urna_nacional(2026, 1)
    vf, vl = u["votos"][22], u["votos"][13]
    outros = u["validos"] - vf - vl
    gap = vf - vl
    precisa_outros = (outros + gap) / (2 * outros)
    aptos = abst["aptos_2026"]
    # se a abstencao do 2o turno cair x pontos, entram x% dos aptos como votos novos; Lula precisaria de s = 0,5 + gap/(2N) deles
    cenarios = []
    for queda in (0.37, 1.0, 2.0, 3.0):
        n = queda / 100 * aptos
        cenarios.append({"abstencao_cai_pontos": queda, "votos_novos": int(n), "parte_de_lula_necessaria": 0.5 + gap / (2 * n)})
    return {"votos_flavio_1t": int(vf), "votos_lula_1t": int(vl), "votos_outros_1t": int(outros), "diferenca_1t": int(gap),
            "parte_dos_outros_que_lula_precisa": precisa_outros,
            "outros_por_candidato": {NOMES_PARTIDO_2026.get(p, f"partido {p}"): int(v) for p, v in u["votos"].items() if p not in (22, 13)},
            "virar_eleitor_de_flavio_necessario": int(np.ceil(gap / 2)), "virar_eleitor_de_flavio_pct": 100 * (gap / 2) / vf,
            "novos_eleitores": cenarios}


# ------------------------------------------------------------ para onde foram os outros no passado (informativo)

def transferencia_historica() -> pd.DataFrame:
    """Regressao ecologica por municipio (Goodman): votos do PT no 2o turno, como fracao dos aptos, contra PT, anti-PT, outros e nao
    validos do 1o turno. O coeficiente dos outros e a fracao deles que foi para o PT. Informativo: nao entra no numero."""
    v = pd.read_parquet(DERIV / "mun_votos.parquet")
    d = pd.read_parquet(DERIV / "mun_detalhe.parquet")
    out = []
    for ano in ANOS:
        f = FINALISTAS[ano]
        a = v[v.ano == ano].pivot_table(index=["uf", "mun"], columns=["turno", "partido"], values="votos", aggfunc="sum").fillna(0)
        det = d[(d.ano == ano) & (d.turno == 1)].set_index(["uf", "mun"]).aptos
        t1 = a[1]
        x = pd.DataFrame({"pt1": t1[f["pt"]], "anti1": t1[f["anti"]]})
        x["outros1"] = t1.sum(axis=1) - x.pt1 - x.anti1
        x["aptos"] = det.reindex(x.index)
        x = x.dropna()
        x = x[x.aptos > 0]
        x["nv1"] = x.aptos - x.pt1 - x.anti1 - x.outros1
        y_pt = a[2][f["pt"]].reindex(x.index) / x.aptos
        y_an = a[2][f["anti"]].reindex(x.index) / x.aptos
        X = (x[["pt1", "anti1", "outros1", "nv1"]].div(x.aptos, axis=0)).values
        wts = np.sqrt(x.aptos.values)
        bp = np.linalg.lstsq(X * wts[:, None], y_pt.values * wts, rcond=None)[0]
        ba = np.linalg.lstsq(X * wts[:, None], y_an.values * wts, rcond=None)[0]
        ofp, ofa = bp[2], ba[2]
        out.append({"ano": ano, "outros_1t_pct": float(100 * x.outros1.sum() / (x.pt1.sum() + x.anti1.sum() + x.outros1.sum())),
                    "outros_para_pt": float(ofp), "outros_para_anti": float(ofa), "parte_pt_entre_os_que_votaram": float(ofp / (ofp + ofa)),
                    "municipios": int(len(x))})
    return pd.DataFrame(out)


# ------------------------------------------------------------ teste do passado

def teste_do_passado(erros: pd.DataFrame) -> pd.DataFrame:
    pp = M.pesquisas_passado()
    out = []
    for ano in (2014, 2018, 2022):
        g = pp[(pp.ano == ano) & (pp.turno == 2)]
        u = M.ultima_antes(g, M.DATAS[(ano, 2)], M.JANELA_DIAS).copy()
        u["anti_valido"] = 100 * u.anti / (u.anti + u.pt)
        nt = M.notas(erros, ano)
        P, _ = M.estimativa_P(u[["instituto", "anti_valido"]], nt)
        P_simples = float(u.anti_valido.mean())
        H, _ = M.estimativa_H(ano)
        R, _ = M.estimativa_R(ano)
        F = M.combinar(P, H, R)
        real = M.anti_pt_urna(ano, 2)
        out.append({"ano": ano, "institutos": len(u), "P": P, "media_simples_pesquisas": P_simples, "H": H, "R": R, "final": F, "urna": real,
                    "erro_P": P - real, "erro_media_simples": P_simples - real, "erro_H": H - real, "erro_R": R - real, "erro_final": F - real,
                    "faixa_1_ponto_conteve": abs(round(F, 1) - real) <= 1.0})
    return pd.DataFrame(out)


# ------------------------------------------------------------ principal

def main() -> None:
    erros = M.erros_institutos()
    nt = M.notas(erros, 2027)
    tab("institutos_erros.csv", erros.round(3))
    rank = nt.sort_values("nota").reset_index(drop=True)
    rank.insert(0, "posicao", range(1, len(rank) + 1))
    tab("institutos_ranking.csv", rank.round(3))

    todas = pesquisas_2026()
    tab("pesquisas_2026_todas.csv", todas.drop(columns=["fim"]).round(3))
    jan = janela(todas)
    P, detP = M.estimativa_P(jan[["instituto", "anti_valido"]], nt)
    detP = detP.merge(jan[["instituto", "campo_ini", "campo_fim", "flavio_total", "lula_total", "amostra", "registro_tse", "url_conferida"]], on="instituto")
    tab("p_pesquisas_usadas.csv", detP.round(4))

    H, infoH = M.estimativa_H(2026)
    lid = M.tabela_lideranca()
    tab("h_lideranca.csv", lid.round(4))
    reg, infoReg = regras_uf()
    tab("h_regras_por_uf.csv", reg)

    R, detR = M.estimativa_R(2026)
    tab("r_por_uf.csv", detR.reset_index().round(4))

    F = M.combinar(P, H, R)
    flavio = round(F, 1)
    lula = round(100 - flavio, 1)

    hist_abst, infoA = abstencao()
    tab("abstencao_historica.csv", hist_abst.round(4))
    onde = de_onde(infoA)
    transf = transferencia_historica()
    tab("transferencia_historica.csv", transf.round(4))
    R_hist2022, _ = M.estimativa_R(2026, divisao=1 - float(transf[transf.ano == 2022].parte_pt_entre_os_que_votaram.iloc[0]))

    bt = teste_do_passado(erros)
    tab("teste_do_passado.csv", bt.round(4))

    # sensibilidade
    sens = []

    def add(rotulo, valor):
        sens.append({"variante": rotulo, "flavio": valor, "lula": 100 - valor, "diferenca_para_o_principal": valor - F})

    add("principal (60/25/15)", F)
    add("só pesquisas (P)", P)
    add("pesos 50/30/20", M.combinar(P, H, R, {"P": 0.5, "H": 0.3, "R": 0.2}))
    add("pesos iguais", M.combinar(P, H, R, {"P": 1 / 3, "H": 1 / 3, "R": 1 / 3}))
    for dv in (0.40, 0.45, 0.55, 0.60):
        Rv, _ = M.estimativa_R(2026, divisao=dv)
        add(f"outros {int(dv*100)}% para Flávio e {int(100-dv*100)}% para Lula", M.combinar(P, H, Rv))
    add("outros divididos como em 2022 (estimativa por município)", M.combinar(P, H, R_hist2022))
    H22, _ = M.estimativa_H(2026, razao=float(lid[lid.ano == 2022].razao.iloc[0]))
    add("H só com 2022", M.combinar(P, H22, R))
    Pv, _ = M.estimativa_P(jan[["instituto", "anti_valido"]], nt, corrigir_vies=False)
    add("P sem correção de viés", M.combinar(Pv, H, R))
    Pp, _ = M.estimativa_P(jan[["instituto", "anti_valido"]], nt, pesar=False)
    add("P sem peso por acerto", M.combinar(Pp, H, R))
    add("P média simples (sem peso e sem correção)", M.combinar(float(jan.anti_valido.mean()), H, R))
    tj = todas[(todas.fim >= date(2026, 10, 12)) & todas.casou & todas.conferida].copy()
    tj["peso_n"] = 1 / tj.groupby("instituto").instituto.transform("size")  # cada instituto pesa 1 no total
    add("P com todas as pesquisas da janela (média simples)", M.combinar(float(tj.anti_valido.mean()), H, R))
    Rsf, _ = M.estimativa_R(2026, com_fator=False)
    add("R sem fator de comparecimento por UF", M.combinar(P, H, Rsf))
    # nota encolhida pelo numero de rodadas (instituto com 1 rodada so puxa metade para a propria nota)
    nt2 = nt.copy()
    med = nt.nota.median()
    nt2["nota"] = (nt2.nota * nt2.n_rodadas + med * 2) / (nt2.n_rodadas + 2)
    Ps, _ = M.estimativa_P(jan[["instituto", "anti_valido"]], nt2)
    add("nota de acerto encolhida pelo número de eleições", M.combinar(Ps, H, R))
    sensdf = pd.DataFrame(sens)
    tab("sensibilidade.csv", sensdf.round(3))

    resumo = {
        "gerado_em": str(date.today()), "corte_das_pesquisas": str(CORTE_2026),
        "final": {"flavio": flavio, "lula": lula, "faixa_pontos": 1.0, "flavio_sem_arredondar": F,
                  "flavio_faixa": [round(flavio - 1, 1), round(flavio + 1, 1)], "lula_faixa": [round(lula - 1, 1), round(lula + 1, 1)]},
        "estimativas": {"P": P, "H": H, "R": R, "pesos": M.PESOS, "contribuicao": {"P": M.PESOS["P"] * P, "H": M.PESOS["H"] * H, "R": M.PESOS["R"] * R}},
        "P": {"institutos": len(detP), "media_simples": float(jan.anti_valido.mean()), "mediana": float(jan.anti_valido.median()),
              "min": float(jan.anti_valido.min()), "max": float(jan.anti_valido.max()),
              "institutos_com_flavio_na_frente": int((jan.anti_valido > 50).sum()), "institutos_com_lula_na_frente": int((jan.anti_valido < 50).sum()),
              "pesquisas_capturadas": len(todas), "pesquisas_registradas": int(todas.casou.sum()), "pesquisas_conferidas": int(todas.conferida.sum()),
              "maior_peso": detP.sort_values("peso").iloc[-1][["instituto", "peso"]].to_dict(), "correcao_media_ponderada": float((detP.peso * detP.correcao).sum())},
        "H": {**infoH, "lider_1t_venceu": f"{int(lid.lider_venceu.sum())} de {len(lid)}", "razoes": lid.set_index("ano").razao.round(3).to_dict(),
              "vantagem_encolheu": f"{int((lid.razao < 1).sum())} de {len(lid)}", "regras_uf": infoReg},
        "R": {"divisao_outros_para_flavio": M.DIVISAO_OUTROS, "R_sem_fator": float(Rsf), "R_com_divisao_de_2022": float(R_hist2022)},
        "abstencao": infoA, "de_onde": onde,
        "transferencia_historica": transf.set_index("ano").round(3).to_dict("index"),
        "teste_do_passado": bt.set_index("ano").round(3).to_dict("index"),
        "teste_do_passado_resumo": {"erro_absoluto_medio_final": float(bt.erro_final.abs().mean()), "erro_absoluto_medio_P": float(bt.erro_P.abs().mean()),
                                    "erro_absoluto_medio_media_simples": float(bt.erro_media_simples.abs().mean()),
                                    "erro_absoluto_medio_H": float(bt.erro_H.abs().mean()), "erro_absoluto_medio_R": float(bt.erro_R.abs().mean()),
                                    "faixa_1_ponto_conteve": int(bt.faixa_1_ponto_conteve.sum())},
        "sensibilidade": {"min_flavio": float(sensdf.flavio.min()), "max_flavio": float(sensdf.flavio.max()),
                          "variantes_com_flavio_acima_de_50": int((sensdf.flavio > 50).sum()), "variantes": len(sensdf)},
        "urna_1t_2026": {NOMES_PARTIDO_2026.get(p, str(p)): round(v, 4) for p, v in M.urna_nacional(2026, 1)["pct"].items()},
    }
    salvar_json("RESUMO.json", resumo)
    print(f"P={P:.3f} H={H:.3f} R={R:.3f} -> Flavio {F:.3f} -> {flavio} x {lula}")
    print(bt.round(2).to_string())
    print(sensdf.round(2).to_string())


if __name__ == "__main__":
    main()
