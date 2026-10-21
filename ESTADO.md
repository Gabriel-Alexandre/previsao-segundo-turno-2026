# ESTADO: onde o trabalho parou

**Atualizado em:** 21/out/2026.

## Em uma frase

Executado de ponta a ponta em 21/out/2026: pré-registro em commit antes de qualquer conta (`b30ae7f`), uma emenda antes do cálculo, coleta do TSE de 2002 a 2026 com hash, 27 pesquisas do 2º turno casadas com o registro no TSE (26 conferidas numa segunda fonte), as três estimativas, teste do passado, 18 variantes, recontagem independente (14 de 14), revisão adversarial, relatório e 10 gráficos. **Projeção: Flávio 50,5% e Lula 49,5% dos válidos, com 1 ponto para cada lado.**

## O que está pronto

| Peça | Estado |
|---|---|
| Pré-registro e emenda 1 | ✅ `docs/PRE_REGISTRO.md` |
| Coleta com sha256 | ✅ `dados/MANIFESTO.json` |
| Pesquisas de 2026: registro no TSE e segunda fonte | ✅ `dados/derivados/pesquisas_2t_2026_*.csv` |
| Análise (P, H, R, regras por UF, abstenção, de onde viriam os votos, teste do passado, sensibilidade) | ✅ `resultados/RESUMO.json` |
| Recontagem independente | ✅ `resultados/validacao_independente.csv` |
| Revisão adversarial | ✅ `docs/REVISAO_ADVERSARIAL.md` |
| Relatório, resumo, leitura | ✅ |
| Gráficos 1920x1080 | ✅ `resultados/figuras/` |
| Testes | ✅ `python -m pytest -q` (8) |

## O que observar ao retomar

- **Depois de 25/out:** comparar a projeção com a urna (o arquivo do 2º turno sai no mesmo endereço do TSE) e registrar o erro numa seção nova do relatório, sem mudar o número publicado.
- Pesquisas publicadas depois de 21/out **não** entram nesta projeção; rodar de novo com elas exigiria uma emenda datada.
- Os zips do TSE (~150 MB) ficam fora do git em `dados/brutos/tse/`; `python ferramentas/coletar.py` baixa de novo e o manifesto confere o hash.
