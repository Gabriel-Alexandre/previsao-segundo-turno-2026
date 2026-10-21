"""Caminhos, manifesto e leitura dos arquivos do TSE."""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BRUTOS = RAIZ / "dados" / "brutos"
TSE = BRUTOS / "tse"
CAPTURAS = BRUTOS / "capturas"
DERIV = RAIZ / "dados" / "derivados"
RES = RAIZ / "resultados"
MANIFESTO = RAIZ / "dados" / "MANIFESTO.json"
REPOS = RAIZ.parent

ANOS = [2002, 2006, 2010, 2014, 2018, 2022]
TODOS_ANOS = ANOS + [2026]
CDN = "https://cdn.tse.jus.br/estatistica/sead/odsele"

# partido do candidato do PT e do principal candidato contra o PT em cada eleicao (numero da urna)
FINALISTAS = {
    2002: {"pt": 13, "anti": 45, "pt_nome": "Lula", "anti_nome": "Serra"},
    2006: {"pt": 13, "anti": 45, "pt_nome": "Lula", "anti_nome": "Alckmin"},
    2010: {"pt": 13, "anti": 45, "pt_nome": "Dilma", "anti_nome": "Serra"},
    2014: {"pt": 13, "anti": 45, "pt_nome": "Dilma", "anti_nome": "Aécio"},
    2018: {"pt": 13, "anti": 17, "pt_nome": "Haddad", "anti_nome": "Bolsonaro"},
    2022: {"pt": 13, "anti": 22, "pt_nome": "Lula", "anti_nome": "Bolsonaro"},
    2026: {"pt": 13, "anti": 22, "pt_nome": "Lula", "anti_nome": "Flávio"},
}
DATA_ELEICAO = {
    (2014, 1): "2014-10-05", (2014, 2): "2014-10-26",
    (2018, 1): "2018-10-07", (2018, 2): "2018-10-28",
    (2022, 1): "2022-10-02", (2022, 2): "2022-10-30",
    (2026, 1): "2026-10-04", (2026, 2): "2026-10-25",
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def manifesto() -> dict:
    if MANIFESTO.exists():
        return json.loads(MANIFESTO.read_text(encoding="utf-8"))
    return {}


def registrar_arquivo(p: Path, origem: str, nota: str = "") -> None:
    m = manifesto()
    m[str(p.relative_to(RAIZ)).replace("\\", "/")] = {
        "origem": origem, "bytes": p.stat().st_size, "sha256": sha256(p),
        "registrado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"), "nota": nota,
    }
    MANIFESTO.write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def ler_csv_zip(zpath: Path, filtro=None, usecols=None) -> pd.DataFrame:
    """Le o CSV nacional (ou todos os CSVs) de um zip do TSE, em latin-1, separado por ';'."""
    partes = []
    with zipfile.ZipFile(zpath) as z:
        nomes = [n for n in z.namelist() if n.lower().endswith((".csv", ".txt"))]
        brasil = [n for n in nomes if n.upper().endswith("_BRASIL.CSV")]
        alvo = brasil or nomes
        for n in alvo:
            with z.open(n) as f:
                df = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep=";", dtype=str, usecols=usecols, low_memory=False)
            if filtro is not None:
                df = filtro(df)
            partes.append(df)
    return pd.concat(partes, ignore_index=True)


def salvar_json(nome: str, obj) -> Path:
    RES.mkdir(parents=True, exist_ok=True)
    p = RES / nome
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    return p
