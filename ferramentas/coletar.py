"""Baixa os arquivos do TSE (2002 a 2026) e copia, com hash, os derivados dos projetos anteriores.

Teto de requisicoes: um download por vez, sem paralelo (o TSE devolve 429 quando se abusa).
Uso: python ferramentas/coletar.py
"""
from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import CDN, DERIV, REPOS, TODOS_ANOS, TSE, registrar_arquivo, sha256  # noqa: E402

ARQUIVOS = [("votacao_partido_munzona", a) for a in TODOS_ANOS] + [("detalhe_votacao_munzona", a) for a in TODOS_ANOS] + [("pesquisa_eleitoral", 2026)]

COPIAS = [
    (REPOS / "congresso-e-governos-eleicoes-2026/dados/brutos/capturas/pindograma-late-polls-2012-2018.csv", "pindograma-late-polls-2012-2018.csv",
     "Pindograma, pesquisas finais 2012 a 2018; copia do projeto congresso-e-governos-eleicoes-2026"),
    (REPOS / "congresso-e-governos-eleicoes-2026/dados/brutos/capturas/pindograma-late-polls-2022.csv", "pindograma-late-polls-2022.csv",
     "Pindograma, pesquisas finais 2022; copia do projeto congresso-e-governos-eleicoes-2026"),
    (REPOS / "presidente-primeiro-turno-2026/resultados/b6_erro_por_instituto_e_rodada.csv", "b6_erro_por_instituto_e_rodada.csv",
     "erro por instituto, ultima pesquisa de 1 a 8 dias antes; projeto presidente-primeiro-turno-2026 (emenda 9 de la)"),
]


def baixar(nome: str, ano: int) -> Path:
    TSE.mkdir(parents=True, exist_ok=True)
    destino = TSE / f"{nome}_{ano}.zip"
    url = f"{CDN}/{nome}/{nome}_{ano}.zip"
    modificado = ""
    if not destino.exists():
        for tentativa in range(4):
            r = requests.get(url, stream=True, timeout=120)
            if r.status_code == 429:
                time.sleep(30 * (tentativa + 1))
                continue
            r.raise_for_status()
            modificado = "Last-Modified: " + r.headers.get("Last-Modified", "")
            with open(destino, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
            break
        time.sleep(1)
    registrar_arquivo(destino, url, modificado)
    return destino


def main() -> None:
    for nome, ano in ARQUIVOS:
        p = baixar(nome, ano)
        print(f"{p.name}: {p.stat().st_size:,} bytes, {sha256(p)[:12]}")
    DERIV.mkdir(parents=True, exist_ok=True)
    for orig, nome, nota in COPIAS:
        dest = DERIV / "copias" / nome
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(orig, dest)
        registrar_arquivo(dest, str(orig.relative_to(REPOS)).replace("\\", "/"), nota)
        print(f"copia {nome}: {sha256(dest)[:12]}")


if __name__ == "__main__":
    main()
