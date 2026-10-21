# Revisão adversarial

Três leitores, cada um procurando o defeito que mais o incomodaria. O que cada objeção mudou está dito; nenhuma mudou o número principal, porque as regras foram escritas antes. As variantes estão em [`resultados/sensibilidade.csv`](../resultados/sensibilidade.csv).

## 1. O leitor que desconfiaria de um número favorável a Flávio

| Objeção | O que os dados dizem | Efeito |
|---|---|---|
| Institutos que costumam inflar o candidato contra o PT empurram a média | a correção pelo viés no 2º turno reduziu a Veritá, a MDA e a Gerp; os três somam pouco peso | já no número |
| Na reta final, o PT costuma crescer | verdade em 2014 e 2018 (as pesquisas desta janela erraram 3,2 e 3,1 pontos a favor do anti-PT); falso em 2022 (-1,1) | descontando o erro médio, o final vai a **49,47%** (Lula na frente); é a variante mais forte contra o número |
| Os votos dos outros podem ir mais para Lula | com 60% para Lula, 50,40%; com a divisão estimada para 2022, 50,50% | pequeno |
| Abstenção maior no Nordeste no 2º turno é premissa contra Lula | o fator por UF é a mediana do que aconteceu; sem ele, 50,53% | desprezível |

## 2. O leitor que desconfiaria de um número favorável a Lula

| Objeção | O que os dados dizem | Efeito |
|---|---|---|
| A Vox Brasil, única com Lula na frente, ganhou 25% do peso com uma eleição só | verdade, pela regra do §4.7 | com a nota encolhida pelo número de eleições: **50,78%**; com a média simples: 50,89% |
| No 1º turno de 2026 os institutos mostraram Flávio menor que a urna | erro médio de -1,90 ponto na escala da parte | corrigindo cada instituto por isso: **51,11%**; é a variante mais forte a favor de Flávio |
| O 50% e 50% é generoso com Lula, já que os outros se apresentam à direita | é o parâmetro do autor, para ser conservador | com 60% para Flávio: 50,63% |

## 3. O auditor de método e linguagem

| Ponto | Resposta |
|---|---|
| A faixa de 1 ponto parece margem de erro | dito no topo do relatório, no gráfico e no resumo: é a escolha do autor; o erro do método no passado foi 1,74 ponto e a faixa teria contido 0 de 3 |
| A Wikipédia como fonte | só como primeira lista; cada pesquisa foi casada com o registro no TSE e conferida numa segunda fonte |
| Teste do passado com poucas eleições | são 3; o teste mostra a ordem de grandeza do erro, não uma probabilidade |
| Regressão ecológica dos outros | informativa; não entra no número e o limite está dito |
| Linguagem | sem "vai ganhar", "favorito" ou recomendação de voto (`ferramentas/conferir-linguagem.py`) |

**Conclusão da revisão:** as duas objeções mais fortes puxam para lados opostos e caem, as duas, dentro da faixa de 1 ponto em torno de 50,5%.
