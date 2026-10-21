# Projeção do 2º turno de 2026: Lula × Flávio Bolsonaro

Projeto aberto que crava uma porcentagem para cada candidato no 2º turno de 25/out/2026 a partir de três coisas, com pesos escritos **antes** de qualquer conta (commit `b30ae7f`): as **pesquisas** registradas no TSE, com mais peso para quem mais acertou no passado (60%), o **histórico** das 6 eleições de 2002 a 2022 (25%) e a **capacidade de crescimento** de cada um a partir do 1º turno, com os votos dos outros candidatos divididos 50% e 50% (15%).

## O resultado

| | Flávio Bolsonaro | Lula |
|---|---|---|
| **Projeção (votos válidos)** | **50,5%** | **49,5%** |
| Faixa de 1 ponto (escolha do autor, não margem de erro) | 49,5% a 51,5% | 48,5% a 50,5% |

> ⛔ **Não é pesquisa e não diz quem deveria ganhar.** É a consequência aritmética de dados públicos e de pesos definidos antes ([`docs/LIMITE_ELEITORAL.md`](docs/LIMITE_ELEITORAL.md)). No teste do passado, o mesmo método errou em média 1,7 ponto a 4 dias da eleição.

## Por onde começar

| Quero | Leia |
|---|---|
| o resultado em uma página | [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md) |
| tudo, com tabelas e limites | [`RELATORIO.md`](RELATORIO.md) |
| a leitura da IA | [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md) |
| o método e os pesos, escritos antes | [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md) |
| as objeções de cada lado | [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md) |
| de onde veio cada dado | [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md), [`dados/MANIFESTO.json`](dados/MANIFESTO.json) |
| refazer tudo | [`docs/REPLICAR.md`](docs/REPLICAR.md) |
| os gráficos (1920x1080) | [`resultados/figuras/`](resultados/figuras/) |

## O método em cinco linhas

1. **Pesquisas (60%):** a última pesquisa de cada instituto de 12 a 21/out, todas casadas com o registro no TSE e conferidas numa segunda fonte; peso pelo acerto de cada instituto de 2014 a 2026 (2º turno pesando o dobro) e desconto do erro que cada um costuma ter no 2º turno.
2. **Histórico (25%):** quanto da vantagem de quem lidera o 1º turno sobra no 2º, nas 6 eleições de 2002 a 2022.
3. **Crescimento (15%):** o 1º turno de 2026 com os outros candidatos divididos meio a meio e o comparecimento de cada UF como costuma ser no 2º turno.
4. **Teste do passado:** o mesmo método rodado 4 dias antes de 2014, 2018 e 2022.
5. **Validação:** totais do TSE conferidos turno a turno, recontagem independente, revisão adversarial e 18 variantes de sensibilidade.

## Estrutura

```
docs/            pré-registro, limite eleitoral, leitura da IA, revisão, fontes, replicar
dados/           MANIFESTO.json (hash de tudo), derivados/ (tabelas leves), brutos/capturas/ (páginas das pesquisas)
previsao/        o modelo (P, H, R e a combinação)
ferramentas/     coletar, derivar, capturar, conferir, casar registro, análise, validação, gráficos, relatório
resultados/      RESUMO.json, tabelas e figuras/
tests/           python -m pytest -q
```

Análise feita pelo Claude, modelo de IA da Anthropic, com o método, os pesos e o parâmetro de 50% e 50% definidos pelo autor, Gabriel Alexandre.
