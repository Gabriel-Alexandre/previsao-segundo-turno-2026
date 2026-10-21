"""Captura a tabela de pesquisas do 2o turno de outubro/2026 da Wikipedia (en) e transforma em CSV.

A Wikipedia e a primeira fonte; cada linha e conferida depois numa segunda fonte (ferramentas/conferir-pesquisas-2026.py)
e no registro do TSE (ferramentas/casar-registro-tse.py).
Saida: dados/brutos/capturas/wikipedia-2t-2026-outubro.wikitext e dados/derivados/pesquisas_2t_2026_wikipedia.csv
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import CAPTURAS, DERIV, registrar_arquivo  # noqa: E402

PAGINA = "Opinion_polling_for_the_2026_Brazilian_presidential_election"
API = "https://en.wikipedia.org/w/api.php"
MESES = {"Oct": 10, "Sep": 9}


def secao_outubro() -> tuple[str, int]:
    r = requests.get(API, params={"action": "parse", "page": PAGINA, "prop": "sections|revid", "format": "json"}, timeout=60,
                     headers={"User-Agent": "previsao-segundo-turno-2026 (pesquisa aberta)"})
    j = r.json()["parse"]
    idx = next(s["index"] for s in j["sections"] if s["line"].startswith("October (after"))
    r = requests.get(API, params={"action": "parse", "page": PAGINA, "prop": "wikitext", "section": idx, "format": "json"}, timeout=60,
                     headers={"User-Agent": "previsao-segundo-turno-2026 (pesquisa aberta)"})
    return r.json()["parse"]["wikitext"]["*"], j["revid"]


def limpar(c: str) -> str:
    c = re.sub(r"^\s*(style=\"[^\"]*\"\s*\|)", "", c.strip())
    return c.replace("'", "").strip()


def numero(c: str):
    c = limpar(c).replace(",", "")
    m = re.search(r"-?\d+(\.\d+)?", c)
    return float(m.group()) if m else None


def periodo(c: str):
    c = limpar(c)
    m = re.match(r"(\d+)\D+(\d+)?\s*(\w{3})", c)
    if not m:
        return None, None
    mes = MESES.get(m.group(3))
    ini, fim = int(m.group(1)), int(m.group(2) or m.group(1))
    return f"2026-{mes:02d}-{ini:02d}", f"2026-{mes:02d}-{fim:02d}"


def linhas(texto: str) -> list[dict]:
    out = []
    for bloco in texto.split("\n|-")[1:]:
        celulas = [c for c in bloco.split("\n|") if c.strip()]
        if len(celulas) < 9 or "colspan" in bloco:
            continue
        celulas = celulas[:9]
        url = re.search(r"https?://[^\s\]|}]+", celulas[8])
        ini, fim = periodo(celulas[1])
        out.append({"instituto": limpar(celulas[0]), "campo_ini": ini, "campo_fim": fim, "lula_total": numero(celulas[2]),
                    "flavio_total": numero(celulas[3]), "bni": numero(celulas[4]), "margem_erro": numero(celulas[5]),
                    "amostra": numero(celulas[6]), "url_wikipedia": url.group() if url else ""})
    return out


def main() -> None:
    texto, revid = secao_outubro()
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    cap = CAPTURAS / "wikipedia-2t-2026-outubro.wikitext"
    cap.write_text(texto, encoding="utf-8")
    registrar_arquivo(cap, f"https://en.wikipedia.org/wiki/{PAGINA} (secao October, revid {revid})", f"revid {revid}")
    df = pd.DataFrame(linhas(texto))
    df["url_wikipedia"] = df.url_wikipedia.str.replace(r"\?utm_source=chatgpt\.com", "", regex=True)
    df["flavio_valido_wiki"] = 100 * df.flavio_total / (df.flavio_total + df.lula_total)
    out = DERIV / "pesquisas_2t_2026_wikipedia.csv"
    df.to_csv(out, index=False)
    registrar_arquivo(out, "ferramentas/capturar-pesquisas-2026.py", f"revid {revid}")
    print(df.to_string())


if __name__ == "__main__":
    main()
