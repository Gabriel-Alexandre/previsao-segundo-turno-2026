# Fontes de dados

| Dado | Endereço | Uso |
|---|---|---|
| Votos por partido, município e turno, presidente, 2002 a 2026 | `https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_partido_munzona/votacao_partido_munzona_AAAA.zip` | resultados nacionais, por UF e por município; até 2014 a coluna é `QT_VOTOS_NOMINAIS`, depois `QT_VOTOS_NOMINAIS_VALIDOS` |
| Aptos, comparecimento, abstenção, brancos e nulos | `.../detalhe_votacao_munzona/detalhe_votacao_munzona_AAAA.zip` | abstenção, fator de comparecimento por UF e conferência dos válidos |
| Registro das pesquisas de 2026 | `.../pesquisa_eleitoral/pesquisa_eleitoral_2026.zip` | casamento de cada pesquisa (empresa, datas, amostra) |
| Pesquisas finais de 2014, 2018 e 2022 | Pindograma, cópia com hash do projeto `congresso-e-governos-eleicoes-2026` | nota de acerto e viés de cada instituto |
| Erro por instituto no 1º turno de 2026 | `presidente-primeiro-turno-2026/resultados/b6_erro_por_instituto_e_rodada.csv` | nota de acerto (recalculada com a urna deste projeto) |
| Pesquisas do 2º turno de 2026 | Wikipédia (en), *Opinion polling for the 2026 Brazilian presidential election*, seção de outubro (revid no manifesto) | primeira lista; cada uma conferida na matéria ou no relatório citado, ou numa fonte alternativa (`dados/derivados/pesquisas_2t_2026_fonte_alternativa.csv`) |

Cada arquivo tem endereço, hora, tamanho e sha256 em `dados/MANIFESTO.json`. As páginas usadas como segunda fonte ficam em `dados/brutos/capturas/pesquisas-2026/`.

**Diferença registrada:** o arquivo de votos de 2026 que o TSE publicou em 21/out tem 1.311 votos válidos a menos que o usado pelo projeto do vídeo 7 (arquivo anterior); os percentuais batem até a segunda casa decimal (`resultados/validacao_independente.csv`).
