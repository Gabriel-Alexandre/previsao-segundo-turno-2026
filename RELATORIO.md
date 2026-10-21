# Relatório: projeção do 2º turno de 2026

**Fechado em:** 2026-10-21, com as pesquisas publicadas até 2026-10-21. Método, pesos e o parâmetro de 50% e 50% escritos e publicados antes de qualquer conta ([`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), commit `b30ae7f`).

## O que este relatório não consegue dizer (vem primeiro)

- **Não é pesquisa e não mede intenção de ninguém.** É uma conta sobre pesquisas registradas, o histórico e o 1º turno.
- **A faixa de 1 ponto foi escolhida pelo autor para a apresentação; não é margem de erro.** No teste do passado, o mesmo método, rodado 4 dias antes de 2014, 2018 e 2022, errou em média 1,8 ponto, e a faixa de 1 ponto teria contido o resultado em **0 das 3** eleições.
- **Nada depois de 2026-10-21** entra: pesquisas novas, debate, fato de reta final.
- **Não diz quem deveria ganhar** e não recomenda voto ([`docs/LIMITE_ELEITORAL.md`](docs/LIMITE_ELEITORAL.md)).

## 1. O número

| | Flávio Bolsonaro | Lula |
|---|---|---|
| **Projeção, em número inteiro** | **51%** | **49%** |
| Com uma casa | 50,8% | 49,2% |
| Faixa de 1 ponto | 49,8% a 51,8% | 48,2% a 50,2% |

Pela **emenda 2** (decisão do autor, depois de ver o número), instituto com um turno só de histórico conta como sem histórico; antes dela, o final era 50,52%. Nenhuma redução do peso da Vox Brasil, sozinha, chegaria a 51,0 com uma casa; em número inteiro, o resultado é 51 a 49.

| Estimativa | Parte de Flávio | Peso | Contribuição |
|---|---|---|---|
| P, pesquisas | 50,97% | 60% | 30,58 |
| H, histórico | 50,57% | 25% | 12,64 |
| R, capacidade de crescimento | 50,84% | 15% | 7,63 |
| **Final** | **50,85%**, arredondado para 50,8% | | |

As três estimativas, cada uma por um caminho diferente, deram Flávio entre 50,6% e 51,0%. Das 19 variantes da sensibilidade, 18 dão Flávio acima de 50%.

## 2. P, pesquisas (50,97%)

27 pesquisas do 2º turno capturadas, 27 casadas com o registro no TSE e 26 conferidas numa segunda fonte. Na janela (fim de campo de 12/out em diante), a última de cada instituto: **17 institutos, 16 com Flávio na frente e 1 com Lula** (Vox Brasil). Média simples: 51,04%; mediana: 51,09%.

Com a emenda 2, os institutos com um turno só de histórico (Vox Brasil, Palver, Gerp e Indexa) recebem o peso de quem não tem histórico; a Futura, com o menor erro em 3 turnos, bate no teto de 25%. A correção de viés reduziu a Veritá, a MDA e a Futura, que no passado mostraram o candidato contra o PT maior do que a urna, e aumentou AtlasIntel, PoderData e Datafolha, que mostraram menor. Antes da emenda, a Vox Brasil, única com Lula na frente, tinha 25% do peso e o P era 50,41%.

| Instituto | Fim de campo | Flávio nos válidos | Nota de acerto | Correção | Corrigida | Peso | Registro TSE |
|---|---|---|---|---|---|---|---|
| Futura | 2026-10-15 | 50,78 | 0,91 | -0,41 | 50,37 | 25,0% | BR037642026 |
| Real Time | 2026-10-19 | 51,61 | 1,61 | 0,16 | 51,77 | 11,0% | BR029522026 |
| Quaest | 2026-10-13 | 51,11 | 1,63 | 0,26 | 51,37 | 10,7% | BR087292026 |
| Datafolha | 2026-10-15 | 51,09 | 1,69 | 0,46 | 51,54 | 10,0% | BR004662026 |
| MDA | 2026-10-15 | 50,49 | 1,89 | -0,68 | 49,81 | 8,0% | BR006522026 |
| Ideia | 2026-10-19 | 51,06 | 2,05 | 0,00 | 51,06 | 6,8% | BR082512026 |
| AtlasIntel | 2026-10-18 | 51,13 | 2,37 | 0,84 | 51,97 | 5,1% | BR024182026 |
| Ipespe | 2026-10-15 | 51,06 | 2,48 | -0,13 | 50,93 | 4,6% | BR002232026 |
| PoderData | 2026-10-18 | 51,58 | 2,58 | 0,60 | 52,17 | 4,3% | BR025862026 |
| Nexus | 2026-10-18 | 50,32 | 3,16 | 0,00 | 50,32 | 2,8% | BR044992026 |
| Alfa | 2026-10-19 | 51,53 | sem histórico | 0,00 | 51,53 | 1,7% | BR008202026 |
| DataTrends | 2026-10-17 | 51,58 | sem histórico | 0,00 | 51,58 | 1,7% | BR044542026 |
| Gerp | 2026-10-16 | 52,63 | 1 turno, não conta | -1,04 | 51,59 | 1,7% | BR051872026 |
| Indexa | 2026-10-14 | 51,16 | 1 turno, não conta | 0,00 | 51,16 | 1,7% | BR046292026 |
| Palver | 2026-10-13 | 50,51 | 1 turno, não conta | 0,00 | 50,51 | 1,7% | BR080282026 |
| Verita | 2026-10-16 | 51,03 | 4,10 | -1,81 | 49,22 | 1,7% | BR011072026 |
| Vox Brasil | 2026-10-17 | 49,01 | 1 turno, não conta | 0,00 | 49,01 | 1,7% | BR043322026 |

### Ranking de acerto dos institutos (2014 a 2026, 2º turno pesando o dobro)

| Posição | Instituto | Erro médio (pontos) | Turnos medidos | Conta no peso | Viés no 2º turno (+ = Flávio/anti-PT maior) |
|---|---|---|---|---|---|
| 1 | Ranking Pesquisa | 0,07 | 1 | não (1 turno) | +0,07 |
| 2 | Vox Brasil | 0,49 | 1 | não (1 turno) |  |
| 3 | Futura | 0,91 | 3 | sim | +1,22 |
| 4 | Palver | 1,07 | 1 | não (1 turno) |  |
| 5 | Real Time | 1,61 | 3 | sim | -0,48 |
| 6 | Quaest | 1,63 | 3 | sim | -0,78 |
| 7 | Datafolha | 1,69 | 7 | sim | -0,76 |
| 8 | MDA | 1,89 | 7 | sim | +1,13 |
| 9 | Ideia | 2,05 | 2 | sim |  |
| 10 | Parana Pesquisas | 2,26 | 4 | sim | +2,99 |
| 11 | AtlasIntel | 2,37 | 3 | sim | -2,51 |
| 12 | Ipec | 2,46 | 6 | sim | -2,07 |
| 13 | Ipespe | 2,48 | 4 | sim | +0,27 |
| 14 | PoderData | 2,58 | 4 | sim | -1,79 |
| 15 | Gerp | 3,12 | 1 | não (1 turno) | +3,12 |
| 16 | Nexus | 3,16 | 2 | sim |  |
| 17 | Indexa | 3,74 | 1 | não (1 turno) |  |
| 18 | Verita | 4,10 | 4 | sim | +3,62 |
| 19 | IPRI | 4,56 | 2 | sim | +4,64 |
| 20 | Vox Populi | 4,57 | 4 | sim | -0,90 |
| 21 | Sensus | 4,57 | 2 | sim | +3,74 |
| 22 | Brasmarket | 6,25 | 2 | sim | +3,93 |

## 3. H, histórico (50,57%)

Nas 6 eleições de 2002 a 2022, **quem liderou o 1º turno venceu o 2º (6 de 6)**, e a vantagem **encolheu em 5 de 6**. Na mediana, sobrou 57% da vantagem. Flávio liderou o 1º turno de 2026 por 2,02 pontos entre os dois; 57% disso dá 1,15 ponto de vantagem, ou 50,57%.

| Eleição | Líder do 1º turno | Vantagem no 1º (entre os dois) | Vantagem no 2º | Sobrou da vantagem | Líder venceu? |
|---|---|---|---|---|---|
| 2002 | Lula | 33,4 | 22,5 | 68% | sim |
| 2006 | Lula | 7,7 | 21,7 | 280% | sim |
| 2010 | Dilma | 18,0 | 12,1 | 67% | sim |
| 2014 | Dilma | 10,7 | 3,3 | 31% | sim |
| 2018 | Bolsonaro | 22,2 | 10,3 | 46% | sim |
| 2022 | Lula | 5,7 | 1,8 | 32% | sim |

**As regras por estado (direção, sem entrar no número).** Quatro unidades acertaram, nas 6 eleições, quem venceria o 2º turno: quem ficou em primeiro ali no 1º turno venceu a eleição. Em 2026, duas apontam para cada lado:

| UF | Acertos no 1º turno | Acertos no 2º turno | 1º turno de 2026 |
|---|---|---|---|
| AM | 6 de 6 | 6 de 6 | Lula |
| MG | 6 de 6 | 6 de 6 | Flávio Bolsonaro |
| AP | 6 de 6 | 5 de 6 | Lula |
| TO | 6 de 6 | 5 de 6 | Flávio Bolsonaro |

Minas Gerais, a regra mais citada, acertou as 6 nos dois turnos e deu **Flávio** no 1º turno de 2026; o Amazonas também acertou as 6 nos dois turnos e deu **Lula**. A regra dos estados empata; a regra do líder do 1º turno aponta para Flávio. Tabela completa: [`resultados/h_regras_por_uf.csv`](resultados/h_regras_por_uf.csv).

## 4. R, capacidade de crescimento (50,84%)

No 1º turno, Flávio teve 56.104.503 votos, Lula 53.879.538 e os outros 9.316.747: Renan Santos (2.675.887), Romeu Zema (326.488), Ronaldo Caiado (2.605.148), Augusto Cury (3.448.569), demais candidatos (partidos 16, 21, 27, 29, 35 e 80) (260.655). A diferença foi de **2.224.965 votos**.

Com os outros divididos **50% e 50%** (parâmetro do autor, que lê a maior parte desses candidatos como mais à direita e não quis puxar a conta para Flávio), a diferença em votos continua a mesma (2,2 milhões), só que sobre uma base maior, e a parte de Flávio cai de 51,01% (só os dois) para 50,93%. O fator de comparecimento por UF quase não muda a conta (sem ele, 50,93%).

**De onde Lula precisaria tirar a diferença, cada fonte sozinha:**

| Fonte | O que seria preciso |
|---|---|
| Votos dos outros candidatos | **61,9%** deles para Lula (no lugar de 50%) |
| Eleitor de Flávio que muda de lado | 1.112.483 pessoas (2,0% dos eleitores dele no 1º turno) |
| Quem não votou no 1º turno | se a abstenção cair 2 pontos (nunca aconteceu; a maior queda foi 0,36 ponto, em 2022), Lula precisaria de 85% desses votos novos |

**Abstenção.** A do 1º turno de 2026 (21,08%) está 0,6 ponto abaixo da tendência de 2002 a 2022: está no padrão. No 2º turno, ela subiu em 5 das 6 eleições (mediana: +2,0 ponto); só caiu em 2022. Os brancos e nulos costumam cair no 2º turno, e os votos válidos ficaram praticamente iguais entre os turnos (mediana da razão: 1,001). Pelo padrão, não sobra uma reserva de votos novos para virar a eleição.

| Eleição | Abstenção 1º turno | Abstenção 2º turno | Variação | Brancos e nulos 1º | Brancos e nulos 2º |
|---|---|---|---|---|---|
| 2002 | 17,7% | 20,5% | +2,7 | 10,4% | 6,0% |
| 2006 | 16,8% | 19,0% | +2,2 | 8,4% | 6,0% |
| 2010 | 18,1% | 21,5% | +3,4 | 8,6% | 6,7% |
| 2014 | 19,4% | 21,1% | +1,7 | 9,6% | 6,3% |
| 2018 | 20,3% | 21,3% | +1,0 | 8,8% | 9,6% |
| 2022 | 20,9% | 20,6% | -0,4 | 4,4% | 4,6% |
| 2026 | 21,1% | 25/out |  | 4,8% |  |

**Para onde foram os votos dos outros no passado (informativo, não entra no número).** Estimativa por município (regressão ecológica, com os limites dela):

| Eleição | Outros no 1º turno | Parte que foi para o PT (entre os que votaram em alguém) |
|---|---|---|
| 2002 | 30,4% | 68% |
| 2006 | 9,8% | 65% |
| 2010 | 20,5% | 53% |
| 2014 | 24,9% | 49% |
| 2018 | 24,7% | 80% |
| 2022 | 8,4% | 51% |

O candidato do PT ficou com metade ou mais dos outros em quase todas as eleições, mas **os outros eram, na maior parte, de centro e de esquerda** (Garotinho, Ciro, Marina, Heloísa Helena, Tebet). Não existe eleição passada em que os maiores outros fossem lidos como de direita, como o autor lê os de 2026; por isso o 50% e 50% é uma escolha, não uma medida. Com a divisão estimada para 2022 (51% para o PT), o número final fica em 50,83%.

## 5. Teste do passado

O mesmo método, com só o que se sabia 4 dias antes de cada eleição:

| Eleição | Urna | Pesquisas (P) | Média simples das pesquisas | Histórico (H) | Crescimento (R) | Número final | Erro do final |
|---|---|---|---|---|---|---|---|
| 2014 | 48,36 | 51,60 | 51,60 | 46,38 | 45,94 | 49,45 | +1,09 |
| 2018 | 55,13 | 58,31 | 58,46 | 57,50 | 58,27 | 58,10 | +2,97 |
| 2022 | 49,10 | 47,97 | 49,15 | 48,08 | 47,27 | 47,89 | -1,21 |

Erro médio (absoluto): número final 1,76; pesquisas com peso 2,52; média simples das pesquisas 2,21; histórico 1,79; crescimento 2,46. **A combinação errou menos que as pesquisas sozinhas** nas três eleições juntas, o que sustenta a ideia de usar o histórico e o 1º turno como freio. Em 2022, porém, a média simples das pesquisas acertou quase em cheio e o peso por acerto piorou a conta; com três eleições, isso é registro, não regra. A faixa de 1 ponto conteve o resultado em 0 das 3.

## 6. Sensibilidade

| Variante | Flávio | Lula | Diferença |
|---|---|---|---|
| principal (60/25/15, com a emenda 2) | 50,85 | 49,15 | 0,00 |
| como no pré-registro, antes da emenda 2 (Vox Brasil com 25% do peso) | 50,52 | 49,48 | -0,33 |
| só pesquisas (P) | 50,97 | 49,03 | +0,12 |
| pesos 50/30/20 | 50,82 | 49,18 | -0,03 |
| pesos iguais | 50,79 | 49,21 | -0,06 |
| outros 40% para Flávio e 60% para Lula | 50,73 | 49,27 | -0,12 |
| outros 45% para Flávio e 55% para Lula | 50,79 | 49,21 | -0,06 |
| outros 55% para Flávio e 45% para Lula | 50,91 | 49,09 | +0,06 |
| outros 60% para Flávio e 40% para Lula | 50,97 | 49,03 | +0,12 |
| outros divididos como em 2022 (estimativa por município) | 50,83 | 49,17 | -0,02 |
| H só com 2022 | 50,78 | 49,22 | -0,06 |
| P sem correção de viés | 50,88 | 49,12 | +0,03 |
| P sem peso por acerto | 50,83 | 49,17 | -0,02 |
| P média simples (sem peso e sem correção) | 50,89 | 49,11 | +0,04 |
| P com todas as pesquisas da janela (média simples) | 50,88 | 49,12 | +0,03 |
| R sem fator de comparecimento por UF | 50,86 | 49,14 | +0,01 |
| nota de acerto encolhida pelo número de eleições | 50,78 | 49,22 | -0,07 |
| P menos o erro médio das pesquisas a 4-13 dias (2014-2022) | 49,79 | 50,21 | -1,06 |
| P corrigido pelo erro de cada instituto no 1º turno de 2026 | 51,88 | 48,12 | +1,03 |

As duas variantes que mais mexem vêm da revisão adversarial (§7): descontar o erro médio das pesquisas a esta distância da eleição dá 49,79% (Lula na frente); corrigir cada instituto pelo erro dele no 1º turno de 2026 dá 51,88%. A primeira fica dentro da faixa e a segunda 0,08 ponto fora da faixa.

## 7. Validação

- Totais do TSE: soma dos candidatos igual aos válidos do arquivo de detalhe em todos os 13 turnos de 2002 a 2026 (diferença zero).
- Recontagem independente ([`ferramentas/validacao-independente.py`](ferramentas/validacao-independente.py)): 14 de 14 números iguais por outro caminho.
- Pesquisas: 27 de 27 casadas com o registro no TSE; 26 de 27 conferidas numa segunda fonte (a que falta está fora da janela).
- Revisão adversarial: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md).

| Número | Passou |
|---|---|
| Flávio 1º turno 2026 (%) contra o projeto do vídeo 7 | sim |
| Lula 1º turno 2026 (%) contra o projeto do vídeo 7 | sim |
| anti-PT 2º turno 2014 (%) contra a coluna da urna do Pindograma | sim |
| anti-PT 2º turno 2018 (%) contra a coluna da urna do Pindograma | sim |
| abstenção 1º turno 2026 (%) | sim |
| P (pesquisas) | sim |
| soma dos pesos | sim |
| maior peso não passa de 25% | sim |
| H (histórico) | sim |
| R (crescimento) | sim |
| número final de Flávio (sem arredondar) | sim |
| número final de Flávio (arredondado) | sim |
| número final de Lula (arredondado) | sim |
| parte dos outros que Lula precisaria | sim |

## 8. Fontes

TSE (`votacao_partido_munzona`, `detalhe_votacao_munzona` e `pesquisa_eleitoral`, 2002 a 2026), base de pesquisas do Pindograma (2014 a 2022), projeto `presidente-primeiro-turno-2026` (erro dos institutos no 1º turno de 2026), Wikipédia em inglês e a matéria ou o relatório de cada pesquisa. Endereço, hora, tamanho e sha256 de cada arquivo em [`dados/MANIFESTO.json`](dados/MANIFESTO.json); detalhes em [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md).

Análise feita pelo Claude, modelo de IA da Anthropic, com o método, os pesos e o parâmetro de 50% e 50% definidos pelo autor, Gabriel Alexandre.
