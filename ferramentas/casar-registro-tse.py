"""Casa cada pesquisa do 2o turno de 2026 com o registro no TSE (arquivo pesquisa_eleitoral_2026).

Casamento: registro nacional de presidente (SG_UE = BR) com fim de campo igual (ou 1 dia de diferenca), inicio de campo com ate
1 dia de diferenca, amostra com ate 2% de diferenca e o nome da empresa contendo a chave do instituto.
Saida: dados/derivados/pesquisas_2t_2026_registro.csv
"""
from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import DERIV, TSE, ler_csv_zip, registrar_arquivo  # noqa: E402

CHAVES = {"Ideia": ["IDEIA"], "Alfa": ["ALFA"], "Real Time": ["REAL TIME"], "PoderData": ["PODER", "AYA"], "Nexus": ["NEXUS", "FSB"],
          "AtlasIntel": ["ATLAS"], "DataTrends": ["DATATRENDS", "DATA TRENDS"], "Vox Brasil": ["VOX"], "Gerp": ["GERP"],
          "Verita": ["VERITA"], "Futura": ["FUTURA", "100% CIDADES"], "Ipespe": ["IPESPE"], "MDA": ["MDA"], "Datafolha": ["DATAFOLHA", "FOLHA"],
          "Indexa": ["INDEXA"], "Palver": ["PALVER"], "Quaest": ["QUAEST"]}


def sem_acento(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()


def main() -> None:
    reg = ler_csv_zip(TSE / "pesquisa_eleitoral_2026.zip")
    reg = reg[(reg.SG_UE == "BR") & reg.DS_CARGO.str.contains("Presidente", na=False)].copy()
    reg["ini"] = pd.to_datetime(reg.DT_INICIO_PESQUISA).dt.normalize()
    reg["fim"] = pd.to_datetime(reg.DT_FIM_PESQUISA).dt.normalize()
    reg["n"] = pd.to_numeric(reg.QT_ENTREVISTADO, errors="coerce")
    reg["empresa"] = (reg.NM_EMPRESA.fillna("") + " | " + reg.NM_EMPRESA_FANTASIA.fillna("")).map(sem_acento)
    w = pd.read_csv(DERIV / "pesquisas_2t_2026_wikipedia.csv")
    out = []
    for r in w.itertuples():
        ini, fim = pd.Timestamp(r.campo_ini), pd.Timestamp(r.campo_fim)
        c = reg[((reg.fim - fim).abs() <= pd.Timedelta(days=1)) & ((reg.ini - ini).abs() <= pd.Timedelta(days=1)) & ((reg.n - r.amostra).abs() <= 0.02 * r.amostra)]
        c = c[c.empresa.apply(lambda e: any(k in e for k in CHAVES.get(r.instituto, [sem_acento(r.instituto)])))]
        out.append({"instituto": r.instituto, "campo_fim": r.campo_fim, "registro_tse": ";".join(c.NR_PROTOCOLO_REGISTRO), "empresa_tse": ";".join(c.NM_EMPRESA),
                    "contratante_propria": ";".join(c.ST_PESQUISA_PROPRIA), "casou": len(c) > 0})
        print(r.instituto, r.campo_fim, len(c), ";".join(c.NR_PROTOCOLO_REGISTRO), ";".join(c.NM_EMPRESA.str[:40]))
    p = DERIV / "pesquisas_2t_2026_registro.csv"
    pd.DataFrame(out).to_csv(p, index=False)
    registrar_arquivo(p, "ferramentas/casar-registro-tse.py", "casamento com dados/brutos/tse/pesquisa_eleitoral_2026.zip")


if __name__ == "__main__":
    main()
