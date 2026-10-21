"""Deriva dos zips do TSE as tabelas leves de presidente (2002 a 2026), por municipio e por UF.

Saidas em dados/derivados/:
- mun_votos.parquet: ano, turno, uf, mun, partido, votos (votos nominais do candidato a presidente, somando voto em transito)
- mun_detalhe.parquet: ano, turno, uf, mun, aptos, comparecimento, abstencoes, validos, brancos, nulos
- uf_resumo.csv: o mesmo agregado por UF ('ZZ' e o exterior)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import DERIV, TODOS_ANOS, TSE, ler_csv_zip, registrar_arquivo  # noqa: E402


def so_presidente(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.CD_CARGO.astype(int) == 1]


def votos(ano: int) -> pd.DataFrame:
    # ate 2014 a coluna e QT_VOTOS_NOMINAIS; de 2018 em diante, QT_VOTOS_NOMINAIS_VALIDOS
    cols = {"ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "CD_CARGO", "NR_PARTIDO", "QT_VOTOS_NOMINAIS", "QT_VOTOS_NOMINAIS_VALIDOS"}
    df = ler_csv_zip(TSE / f"votacao_partido_munzona_{ano}.zip", so_presidente, usecols=lambda c: c in cols)
    col = "QT_VOTOS_NOMINAIS_VALIDOS" if "QT_VOTOS_NOMINAIS_VALIDOS" in df else "QT_VOTOS_NOMINAIS"
    df = df.rename(columns={"NR_TURNO": "turno", "SG_UF": "uf", "CD_MUNICIPIO": "mun", "NR_PARTIDO": "partido", col: "votos"})
    df["ano"] = ano
    for c in ("turno", "partido", "votos"):
        df[c] = df[c].astype(int)
    df["mun"] = df["mun"].astype(int)
    return df.groupby(["ano", "turno", "uf", "mun", "partido"], as_index=False).votos.sum()


def detalhe(ano: int) -> pd.DataFrame:
    cols = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "CD_CARGO", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES",
            "QT_TOTAL_VOTOS_VALIDOS", "QT_VOTOS_BRANCOS", "QT_TOTAL_VOTOS_NULOS"]
    df = ler_csv_zip(TSE / f"detalhe_votacao_munzona_{ano}.zip", so_presidente, usecols=cols)
    df = df.rename(columns={"NR_TURNO": "turno", "SG_UF": "uf", "CD_MUNICIPIO": "mun", "QT_APTOS": "aptos", "QT_COMPARECIMENTO": "comparecimento",
                            "QT_ABSTENCOES": "abstencoes", "QT_TOTAL_VOTOS_VALIDOS": "validos", "QT_VOTOS_BRANCOS": "brancos", "QT_TOTAL_VOTOS_NULOS": "nulos"})
    df["ano"] = ano
    num = ["turno", "aptos", "comparecimento", "abstencoes", "validos", "brancos", "nulos"]
    for c in num:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    df["mun"] = df["mun"].astype(int)
    return df.groupby(["ano", "turno", "uf", "mun"], as_index=False)[num[1:]].sum()


def main() -> None:
    v = pd.concat([votos(a) for a in TODOS_ANOS], ignore_index=True)
    d = pd.concat([detalhe(a) for a in TODOS_ANOS], ignore_index=True)
    DERIV.mkdir(parents=True, exist_ok=True)
    v.to_parquet(DERIV / "mun_votos.parquet", index=False)
    d.to_parquet(DERIV / "mun_detalhe.parquet", index=False)
    uf_v = v.groupby(["ano", "turno", "uf", "partido"], as_index=False).votos.sum()
    uf_v.to_csv(DERIV / "uf_votos.csv", index=False)
    uf_d = d.groupby(["ano", "turno", "uf"], as_index=False)[["aptos", "comparecimento", "abstencoes", "validos", "brancos", "nulos"]].sum()
    uf_d.to_csv(DERIV / "uf_detalhe.csv", index=False)
    for nome in ("mun_votos.parquet", "mun_detalhe.parquet", "uf_votos.csv", "uf_detalhe.csv"):
        registrar_arquivo(DERIV / nome, "ferramentas/derivar-votos.py", "derivado dos zips do TSE")
    # conferencia imediata: votos dos candidatos somam os validos do detalhe
    a = v.groupby(["ano", "turno"]).votos.sum()
    b = d.groupby(["ano", "turno"]).validos.sum()
    print(pd.DataFrame({"soma_candidatos": a, "validos_detalhe": b, "diferenca": a - b}))


if __name__ == "__main__":
    main()
