"""Confere que nenhum texto público do projeto usa linguagem de preferência ou de aposta (doutrina, regra 5).

Sai com código 1 se achar alguma expressão proibida fora das listas que as definem.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS = ["RELATORIO.md", "RESUMO_SIMPLES.md", "README.md", "docs/LEITURA_DA_IA.md", "docs/REVISAO_ADVERSARIAL.md"]
PROIBIDAS = [r"vai ganhar", r"\bfavorit[oa]s?\b", r"\bvencedor", r"aposta em", r"vote em", r"melhor candidato", r"ganhou a elei", r"mentiu", r"\bfraude", r"—"]
PERMITIDO = re.compile(r"sem \"vai ganhar\"|⛔|não recomenda", re.I)

achou = 0
for nome in ARQUIVOS:
    p = RAIZ / nome
    if not p.exists():
        continue
    for i, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if PERMITIDO.search(linha):
            continue
        for padrao in PROIBIDAS:
            if re.search(padrao, linha, re.I):
                print(f"{nome}:{i}: '{padrao}' -> {linha.strip()[:120]}")
                achou += 1
print(f"{achou} ocorrência(s)")
sys.exit(1 if achou else 0)
