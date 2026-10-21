# Pré-registro: projeção do 2º turno de 2026 (Lula × Flávio Bolsonaro)

**Escrito em:** 21/out/2026, antes de qualquer conta. Vale o commit em que este arquivo entrou pela primeira vez. Mudança depois disso só pela §12, com data e dizendo se veio antes ou depois de ver o número.

**Pedido do autor (21/out/2026), nas palavras dele:** uma previsão do 2º turno *"baseada nas pesquisas, baseada no histórico e baseada no resultado do primeiro turno"*, *"bem metódica"*, com pelo menos 10 a 12 anos de histórico, ranking de quem mais acertou dando *"mais peso para as que acertaram mais no segundo turno"*, a capacidade de crescimento de cada um, a abstenção do 1º e do 2º turno desta e das outras eleições, os votos dos outros candidatos divididos *"50% em cada um [...] para ser mais conservador"*, pesos na ordem *"primeiramente, o resultado das pesquisas. Depois [...] questões históricas, depois a capacidade de recuperação"*, e no fim **uma porcentagem para cada um, variando 1 ponto para mais ou para menos**, conclusiva: *"eu não quero saber se você vai acertar ou não. Eu quero que você chegue no número"*.

## 1. O que já foi visto antes de escrever isto (declaração honesta)

- O resultado do 1º turno de 2026 (Flávio 47,03% e Lula 45,16% dos válidos; outros, cerca de 7,8%), lido no projeto `presidente-primeiro-turno-2026`.
- As manchetes de quatro pesquisas do 2º turno, numa busca para saber se havia dado: AtlasIntel de 19/out (51,1 × 48,9 para Flávio), Datafolha de 15/out (51 × 49), Quaest de 14/out (51 × 49) e Vox Brasil de 18/out (51 × 49 para Lula); e o cabeçalho da tabela de pesquisas de outubro da Wikipédia em inglês.
- Os resultados nacionais dos 2º turnos de 2002 a 2022, que são conhecimento geral, e os erros por instituto em 2018, 2022 e 2026 (1º turno) já medidos no projeto anterior.
- **Não** foram vistos: o erro de cada instituto em 2014, a abstenção por UF, as pesquisas de outubro uma a uma, nem nenhuma das três estimativas abaixo.

## 2. A pergunta e a saída

**Pergunta:** qual a porcentagem dos votos válidos de Flávio Bolsonaro e de Lula no 2º turno de 25/out/2026?

**Saída:** um número para cada um (somando 100), arredondado a uma casa, com a faixa de **1 ponto para cada lado**, escolhida pelo autor para a apresentação. A faixa **não** é margem de erro estatística; o erro que o método teria tido no passado é medido e publicado à parte (§8).

## 3. As três estimativas e os pesos

| Estimativa | O que é | Peso |
|---|---|---|
| **P, pesquisas** | média das pesquisas do 2º turno de 2026, com mais peso para os institutos que mais acertaram no passado e corrigida pelo erro histórico de cada um no 2º turno | **60%** |
| **H, histórico** | o que costuma acontecer com a vantagem de quem lidera o 1º turno, nas 6 eleições de 2002 a 2022 | **25%** |
| **R, capacidade de crescimento** | o 1º turno de 2026 com os votos dos outros candidatos divididos 50% e 50% e o comparecimento de cada UF se comportando como costuma se comportar no 2º turno | **15%** |

**Número final de Flávio = 0,60 × P + 0,25 × H + 0,15 × R.** Lula = 100 − Flávio.

**Por que esses pesos:** a ordem é a do autor (pesquisas, histórico, recuperação). As pesquisas levam mais da metade porque medem o eleitor desta eleição, já depois do 1º turno, e boa parte do que H e R medem já aparece nelas; H e R entram como freio, com o que a história e a aritmética do 1º turno dizem. O teste do passado (§8) mostra se essa ordem se sustenta; ele **não** muda os pesos.

## 4. P, pesquisas

1. **Universo:** pesquisa nacional, estimulada, do 2º turno de 2026 entre Lula e Flávio, com fim de campo de 05/out a 21/out.
2. **Janela:** a **última pesquisa de cada instituto** com fim de campo de **12/out em diante** (os dez últimos dias antes da coleta). Instituto sem pesquisa na janela fica fora.
3. **Votos válidos:** o válido publicado; sem ele, Flávio ÷ (Flávio + Lula).
4. **Registro no TSE:** a pesquisa precisa casar com um registro do arquivo `pesquisa_eleitoral_2026` do TSE (empresa, datas de campo e amostra). Sem casamento, fica fora da conta principal e entra só na sensibilidade.
5. **Duas fontes:** o número de cada pesquisa conferido em duas fontes (a tabela da Wikipédia e a matéria ou o relatório do instituto). Divergência: vale o instituto ou, sem ele, o veículo que contratou.
6. **Nota de acerto de cada instituto** (o pedido do autor, com o 2º turno pesando mais):
   - erro de uma pesquisa = parte do candidato contra o PT nos válidos da pesquisa menos a da urna (no 1º turno, a diferença entre os dois primeiros dividida por 2, para ficar na mesma escala);
   - a pesquisa que conta em cada eleição é a última do instituto com fim de campo de 1 a 8 dias antes da votação;
   - eleições: 2º turno de 2014, 2018 e 2022 (**peso 2**) e 1º turno de 2014, 2018, 2022 e 2026 (**peso 1**);
   - nota = média ponderada do erro absoluto.
7. **Peso de cada instituto** = 1 ÷ nota²; instituto sem histórico recebe a nota do percentil 75 dos que têm (desconhecido pesa um pouco menos que a média). Nenhum instituto passa de **25%** do peso; o excesso se redistribui na proporção dos outros.
8. **Correção pelo viés:** viés = erro médio com sinal do instituto nos 2º turnos. Pesquisa corrigida = pesquisa − viés × n ÷ (n + 2), em que n é o número de 2º turnos com histórico (com 3 eleições, corrige 60% do viés; com 1, 33%). Sem histórico no 2º turno, sem correção.
9. **P** = média ponderada das pesquisas corrigidas.

## 5. H, histórico

1. Para cada eleição de 2002 a 2022 (todas tiveram 2º turno, e em todas o PT esteve num dos lados): vantagem do líder no 1º turno entre os dois finalistas (parte do líder na soma dos dois, menos 50, vezes 2) e a vantagem dele no 2º turno.
2. **Razão** = vantagem no 2º turno ÷ vantagem no 1º turno.
3. **H** = 50 + (mediana das 6 razões × vantagem de Flávio no 1º turno de 2026) ÷ 2.
4. As regras do tipo *"quem ganhou o 1º turno ganhou o 2º"* e *"quem ganhou em Minas ganhou a eleição"* são medidas para as 27 UFs e o exterior, em 2002 a 2022, e aplicadas a 2026, **sem entrar no número**: elas dão direção, não tamanho.

## 6. R, capacidade de crescimento

1. Em cada UF (e no exterior), votos do 2º turno de cada um = votos do 1º turno + **50% dos votos dos outros candidatos** daquela UF (parâmetro do autor, para não puxar para Flávio: os três outros mais votados, Augusto Cury, Renan Santos e Ronaldo Caiado, se apresentam mais à direita).
2. O total de válidos de cada UF é multiplicado pela **mediana, de 2002 a 2022, da razão válidos do 2º turno ÷ válidos do 1º turno daquela UF** (onde o comparecimento costuma cair mais, aquele eleitorado pesa menos).
3. **R** = soma dos votos de Flávio ÷ soma dos dois.
4. Medido junto, sem entrar no número: quanto dos outros Lula precisaria para empatar; a abstenção e os brancos e nulos do 1º e do 2º turno de 2002 a 2022 e o 1º turno de 2026 (se a de 2026 está no padrão); de onde Lula precisaria tirar a diferença, fonte por fonte (outros candidatos, quem não votou, brancos e nulos, eleitor de Flávio); e, só como informação, para onde foram de fato os votos dos outros candidatos no passado (estimativa por município), para mostrar quanto o 50% e 50% é conservador.

## 7. Dados (fonte e validação)

| Dado | Fonte | Validação |
|---|---|---|
| votos por partido e município, 2002 a 2026, presidente | TSE, `votacao_partido_munzona_AAAA.zip` | total nacional contra o arquivo de detalhe e, em 2026, contra o projeto `presidente-primeiro-turno-2026` |
| aptos, comparecimento, brancos e nulos, 2002 a 2026 | TSE, `detalhe_votacao_munzona_AAAA.zip` | soma de válidos igual à do arquivo de votos |
| pesquisas finais de 2014, 2018 e 2022 | base do Pindograma (cópia com hash no projeto `congresso-e-governos-eleicoes-2026`) | o resultado da urna recalculado pelos arquivos do TSE |
| erro por instituto no 1º turno de 2026 | `presidente-primeiro-turno-2026`, `resultados/b6_erro_por_instituto_e_rodada.csv` (hash registrado) | recalculado aqui com a urna do TSE |
| pesquisas do 2º turno de 2026 | Wikipédia (en), seção de outubro, mais a matéria ou o relatório de cada uma | registro no TSE (`pesquisa_eleitoral_2026.zip`) e segunda fonte |

Todo arquivo baixado entra em `dados/MANIFESTO.json` com endereço, hora, tamanho e sha256.

## 8. Teste do passado (validação, não muda pesos)

As três estimativas e a combinação são refeitas para 2014, 2018 e 2022 com **só o que se sabia antes daquela eleição** (as notas e os vieses dos institutos sem a própria eleição). Publica-se o erro de cada uma e da combinação, e em quantas das três a faixa de 1 ponto teria contido o resultado.

## 9. Sensibilidade (publicada, não muda o número)

Pesos (só pesquisas; 50/30/20; iguais), divisão dos outros (40/60 a 60/40, e a divisão estimada pelo histórico), H só com 2022, sem correção de viés, sem peso por acerto, todas as pesquisas da janela em vez da última de cada instituto, e pesquisas sem registro casado.

## 10. Linguagem

A saída é **projeção estatística**, não preferência. ⛔ *"vai ganhar"*, *"favorito"*, *"vencedor"*, *"a IA aposta em"*, recomendação de voto, julgamento de candidato. ✅ *"a projeção do método dá"*, *"pelos pesos escritos antes"*. Toda frase passa pelo teste do espelho: com os nomes trocados, seria escrita igual.

## 11. O que este projeto não faz

Não ouve eleitor (não é pesquisa), não mede intenção de ninguém, não modela evento depois de 21/out, não calcula probabilidade de vitória e não diz quem deveria ganhar.

## 12. Emendas

(nenhuma até aqui)
