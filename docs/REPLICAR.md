# Refazer tudo

```
pip install -r requirements.txt
python ferramentas/coletar.py                 # zips do TSE e cópias com hash
python ferramentas/derivar-votos.py           # tabelas leves por município e UF
python ferramentas/capturar-pesquisas-2026.py # tabela da Wikipédia (a página muda: o revid usado está no manifesto)
python ferramentas/conferir-pesquisas-2026.py # segunda fonte de cada pesquisa
python ferramentas/casar-registro-tse.py      # registro no TSE
python ferramentas/analise.py                 # P, H, R, número final, teste do passado, sensibilidade
python ferramentas/validacao-independente.py  # recontagem por outro caminho
python ferramentas/graficos.py
python ferramentas/gerar-relatorio.py
python ferramentas/conferir-linguagem.py
python -m pytest -q
```

A captura da Wikipédia de 21/out/2026 está no git (`dados/brutos/capturas/wikipedia-2t-2026-outubro.wikitext`); para reproduzir exatamente este resultado, pule `capturar-pesquisas-2026.py` e use os CSVs de `dados/derivados/`.
