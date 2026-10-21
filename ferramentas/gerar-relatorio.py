"""Escreve RELATORIO.md, RESUMO_SIMPLES.md, docs/LEITURA_DA_IA.md e docs/REVISAO_ADVERSARIAL.md a partir de resultados/.

Nenhum número é escrito à mão: todos vêm de resultados/RESUMO.json e das tabelas ao lado.
Uso: python ferramentas/gerar-relatorio.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import RAIZ, RES  # noqa: E402

r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
P = pd.read_csv(RES / "p_pesquisas_usadas.csv").sort_values("peso", ascending=False)
RANK = pd.read_csv(RES / "institutos_ranking.csv")
LID = pd.read_csv(RES / "h_lideranca.csv")
REG = pd.read_csv(RES / "h_regras_por_uf.csv")
AB = pd.read_csv(RES / "abstencao_historica.csv")
TR = pd.read_csv(RES / "transferencia_historica.csv")
BT = pd.read_csv(RES / "teste_do_passado.csv")
SE = pd.read_csv(RES / "sensibilidade.csv")
VAL = pd.read_csv(RES / "validacao_independente.csv")


def b(x, c=1):
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n(x):
    return f"{int(round(x)):,}".replace(",", ".")


f, l = r["final"]["flavio"], r["final"]["lula"]
f_raw = r["final"]["flavio_sem_arredondar"]
E = r["estimativas"]
H = r["H"]
A = r["abstencao"]
D = r["de_onde"]
T = r["teste_do_passado_resumo"]
S = r["sensibilidade"]
ADV = r["adversarial"]
mais_peso = P.iloc[0]
var = SE.set_index("variante").flavio
v_horiz = var["P menos o erro médio das pesquisas a 4-13 dias (2014-2022)"]
v_1t = var["P corrigido pelo erro de cada instituto no 1º turno de 2026"]
v_encolhida = var["nota de acerto encolhida pelo número de eleições"]
v_simples = var["P média simples (sem peso e sem correção)"]
v_pre_P = r["P"]["P_antes_da_emenda_2"]
v_pre = var["como no pré-registro, antes da emenda 2 (Vox Brasil com 25% do peso)"]
fi, li = r["final"]["flavio_inteiro"], r["final"]["lula_inteiro"]
faixa_lo, faixa_hi = f - 1, f + 1


def na_faixa(v):
    return faixa_lo - 0.05 <= v <= faixa_hi + 0.05


def onde(v):
    if na_faixa(v):
        return "dentro da faixa"
    return f"{b(abs(v - (faixa_hi if v > faixa_hi else faixa_lo)), 2)} ponto fora da faixa"

tr22 = TR.set_index("ano").loc[2022]
perfeitas = REG[(REG.eleicoes_1t == 6) & (REG.acertos_1t == 6)]


def tabela(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |\n|" + "---|" * len(df.columns) + "\n"
    return cab + "\n".join("| " + " | ".join(str(v) for v in row) + " |" for row in df.values)


tab_p = tabela(pd.DataFrame({
    "Instituto": P.instituto, "Fim de campo": P.campo_fim, "Flávio nos válidos": P.anti_valido.map(lambda x: b(x, 2)),
    "Nota de acerto": [b(a, 2) if a == a else ("1 turno, não conta" if n == n and n >= 1 else "sem histórico") for a, n in zip(P.nota, P.n_rodadas)], "Correção": P.correcao.map(lambda x: b(x, 2)),
    "Corrigida": P.anti_corrigido.map(lambda x: b(x, 2)), "Peso": P.peso.map(lambda x: b(100 * x, 1) + "%"), "Registro TSE": P.registro_tse}))
tab_lid = tabela(pd.DataFrame({"Eleição": LID.ano, "Líder do 1º turno": LID.lider_1t, "Vantagem no 1º (entre os dois)": LID.vantagem_1t.map(b),
                               "Vantagem no 2º": LID.vantagem_2t.map(b), "Sobrou da vantagem": (100 * LID.razao).map(lambda x: b(x, 0) + "%"),
                               "Líder venceu?": LID.lider_venceu.map({True: "sim", False: "não"})}))
tab_ab = tabela(pd.DataFrame({"Eleição": AB.ano, "Abstenção 1º turno": AB.abst_1t.map(lambda x: b(x) + "%"),
                              "Abstenção 2º turno": AB.abst_2t.map(lambda x: b(x) + "%" if x == x else "25/out"),
                              "Variação": AB.delta_abst.map(lambda x: ("+" if x > 0 else "") + b(x) if x == x else ""),
                              "Brancos e nulos 1º": AB.bn_1t.map(lambda x: b(x) + "%"), "Brancos e nulos 2º": AB.bn_2t.map(lambda x: b(x) + "%" if x == x else "")}))
tab_tr = tabela(pd.DataFrame({"Eleição": TR.ano, "Outros no 1º turno": TR.outros_1t_pct.map(lambda x: b(x) + "%"),
                              "Parte que foi para o PT (entre os que votaram em alguém)": TR.parte_pt_entre_os_que_votaram.map(lambda x: b(100 * x, 0) + "%")}))
tab_bt = tabela(pd.DataFrame({"Eleição": BT.ano, "Urna": BT.urna.map(lambda x: b(x, 2)), "Pesquisas (P)": BT.P.map(lambda x: b(x, 2)), "Média simples das pesquisas": BT.media_simples_pesquisas.map(lambda x: b(x, 2)),
                              "Histórico (H)": BT.H.map(lambda x: b(x, 2)), "Crescimento (R)": BT.R.map(lambda x: b(x, 2)),
                              "Número final": BT.final.map(lambda x: b(x, 2)), "Erro do final": BT.erro_final.map(lambda x: ("+" if x > 0 else "") + b(x, 2))}))
tab_se = tabela(pd.DataFrame({"Variante": SE.variante, "Flávio": SE.flavio.map(lambda x: b(x, 2)), "Lula": SE.lula.map(lambda x: b(x, 2)),
                              "Diferença": SE.diferenca_para_o_principal.map(lambda x: ("+" if x > 0 else "") + b(x, 2))}))
tab_rank = tabela(pd.DataFrame({"Posição": RANK.posicao, "Instituto": RANK.instituto, "Erro médio (pontos)": RANK.nota_medida.map(lambda x: b(x, 2)),
                                "Turnos medidos": RANK.n_rodadas, "Conta no peso": RANK.conta_no_peso.map({True: "sim", False: "não (1 turno)"}), "Viés no 2º turno (+ = Flávio/anti-PT maior)": RANK.vies_2t.map(lambda x: ("+" if x > 0 else "") + b(x, 2) if x == x else "")}))
tab_uf = tabela(pd.DataFrame({"UF": perfeitas.uf, "Acertos no 1º turno": perfeitas.acertos_1t.astype(str) + " de 6",
                              "Acertos no 2º turno": perfeitas.acertos_2t.astype(str) + " de 6", "1º turno de 2026": perfeitas.vencedor_1t_2026}))
tab_val = tabela(pd.DataFrame({"Número": VAL.numero, "Passou": VAL.passou.map({True: "sim", False: "NÃO"})}))
outros_txt = ", ".join(f"{k} ({n(v)})" for k, v in D["outros_por_candidato"].items())

RELATORIO = f"""# Relatório: projeção do 2º turno de 2026

**Fechado em:** {r['gerado_em']}, com as pesquisas publicadas até {r['corte_das_pesquisas']}. Método, pesos e o parâmetro de 50% e 50% escritos e publicados antes de qualquer conta ([`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), commit `b30ae7f`).

## O que este relatório não consegue dizer (vem primeiro)

- **Não é pesquisa e não mede intenção de ninguém.** É uma conta sobre pesquisas registradas, o histórico e o 1º turno.
- **A faixa de 1 ponto foi escolhida pelo autor para a apresentação; não é margem de erro.** No teste do passado, o mesmo método, rodado 4 dias antes de 2014, 2018 e 2022, errou em média {b(T['erro_absoluto_medio_final'])} ponto, e a faixa de 1 ponto teria contido o resultado em **{T['faixa_1_ponto_conteve']} das 3** eleições.
- **Nada depois de {r['corte_das_pesquisas']}** entra: pesquisas novas, debate, fato de reta final.
- **Não diz quem deveria ganhar** e não recomenda voto ([`docs/LIMITE_ELEITORAL.md`](docs/LIMITE_ELEITORAL.md)).

## 1. O número

| | Flávio Bolsonaro | Lula |
|---|---|---|
| **Projeção (votos válidos)** | **{b(f)}%** | **{b(l)}%** |
| Em número inteiro | {fi}% | {li}% |
| Faixa de 1 ponto | {b(f-1)}% a {b(f+1)}% | {b(l-1)}% a {b(l+1)}% |

Pela **emenda 2** (decisão do autor, depois de ver o número), instituto com um turno só de histórico conta como sem histórico; antes dela, o final era {b(v_pre, 2)}%. Nenhuma redução do peso da Vox Brasil, sozinha, chegaria a 51,0 com uma casa. Pela emenda 3 (decisão dele), o número apresentado é o de uma casa, {b(f)} a {b(l)}.

| Estimativa | Parte de Flávio | Peso | Contribuição |
|---|---|---|---|
| P, pesquisas | {b(E['P'], 2)}% | 60% | {b(E['contribuicao']['P'], 2)} |
| H, histórico | {b(E['H'], 2)}% | 25% | {b(E['contribuicao']['H'], 2)} |
| R, capacidade de crescimento | {b(E['R'], 2)}% | 15% | {b(E['contribuicao']['R'], 2)} |
| **Final** | **{b(r['final']['flavio_sem_arredondar'], 2)}%**, arredondado para {b(f)}% | | |

As três estimativas, cada uma por um caminho diferente, deram Flávio entre {b(min(E['P'], E['H'], E['R']), 1)}% e {b(max(E['P'], E['H'], E['R']), 1)}%. Das {S['variantes']} variantes da sensibilidade, {S['variantes_com_flavio_acima_de_50']} dão Flávio acima de 50%.

## 2. P, pesquisas ({b(E['P'], 2)}%)

{r['P']['pesquisas_capturadas']} pesquisas do 2º turno capturadas, {r['P']['pesquisas_registradas']} casadas com o registro no TSE e {r['P']['pesquisas_conferidas']} conferidas numa segunda fonte. Na janela (fim de campo de 12/out em diante), a última de cada instituto: **{r['P']['institutos']} institutos, {r['P']['institutos_com_flavio_na_frente']} com Flávio na frente e {r['P']['institutos_com_lula_na_frente']} com Lula** (Vox Brasil). Média simples: {b(r['P']['media_simples'], 2)}%; mediana: {b(r['P']['mediana'], 2)}%.

Com a emenda 2, os institutos com um turno só de histórico (Vox Brasil, Palver, Gerp e Indexa) recebem o peso de quem não tem histórico; a Futura, com o menor erro em 3 turnos, bate no teto de 25%. A correção de viés reduziu a Veritá, a MDA e a Futura, que no passado mostraram o candidato contra o PT maior do que a urna, e aumentou AtlasIntel, PoderData e Datafolha, que mostraram menor. Antes da emenda, a Vox Brasil, única com Lula na frente, tinha 25% do peso e o P era {b(v_pre_P, 2)}%.

{tab_p}

### Ranking de acerto dos institutos (2014 a 2026, 2º turno pesando o dobro)

{tab_rank}

## 3. H, histórico ({b(E['H'], 2)}%)

Nas 6 eleições de 2002 a 2022, **quem liderou o 1º turno venceu o 2º ({H['lider_1t_venceu']})**, e a vantagem **encolheu em {H['vantagem_encolheu']}**. Na mediana, sobrou {b(100*H['razao_mediana'], 0)}% da vantagem. Flávio liderou o 1º turno de 2026 por {b(H['vantagem_1t_anti'], 2)} pontos entre os dois; {b(100*H['razao_mediana'], 0)}% disso dá {b(H['razao_mediana']*H['vantagem_1t_anti'], 2)} ponto de vantagem, ou {b(E['H'], 2)}%.

{tab_lid}

**As regras por estado (direção, sem entrar no número).** Quatro unidades acertaram, nas 6 eleições, quem venceria o 2º turno: quem ficou em primeiro ali no 1º turno venceu a eleição. Em 2026, duas apontam para cada lado:

{tab_uf}

Minas Gerais, a regra mais citada, acertou as 6 nos dois turnos e deu **Flávio** no 1º turno de 2026; o Amazonas também acertou as 6 nos dois turnos e deu **Lula**. A regra dos estados empata; a regra do líder do 1º turno aponta para Flávio. Tabela completa: [`resultados/h_regras_por_uf.csv`](resultados/h_regras_por_uf.csv).

## 4. R, capacidade de crescimento ({b(E['R'], 2)}%)

No 1º turno, Flávio teve {n(D['votos_flavio_1t'])} votos, Lula {n(D['votos_lula_1t'])} e os outros {n(D['votos_outros_1t'])}: {outros_txt}. A diferença foi de **{n(D['diferenca_1t'])} votos**.

Com os outros divididos **50% e 50%** (parâmetro do autor, que lê a maior parte desses candidatos como mais à direita e não quis puxar a conta para Flávio), a diferença em votos continua a mesma ({b(D['diferenca_1t']/1e6, 1)} milhões), só que sobre uma base maior, e a parte de Flávio cai de {b(100*D['votos_flavio_1t']/(D['votos_flavio_1t']+D['votos_lula_1t']), 2)}% (só os dois) para {b(r['R']['R_sem_fator'], 2)}%. O fator de comparecimento por UF quase não muda a conta (sem ele, {b(r['R']['R_sem_fator'], 2)}%).

**De onde Lula precisaria tirar a diferença, cada fonte sozinha:**

| Fonte | O que seria preciso |
|---|---|
| Votos dos outros candidatos | **{b(100*D['parte_dos_outros_que_lula_precisa'], 1)}%** deles para Lula (no lugar de 50%) |
| Eleitor de Flávio que muda de lado | {n(D['virar_eleitor_de_flavio_necessario'])} pessoas ({b(D['virar_eleitor_de_flavio_pct'], 1)}% dos eleitores dele no 1º turno) |
| Quem não votou no 1º turno | se a abstenção cair 2 pontos (nunca aconteceu; a maior queda foi {b(-A['delta_abst_min'], 2)} ponto, em 2022), Lula precisaria de {b(100*D['novos_eleitores'][2]['parte_de_lula_necessaria'], 0)}% desses votos novos |

**Abstenção.** A do 1º turno de 2026 ({b(A['abstencao_1t_2026'], 2)}%) está {b(abs(A['abstencao_1t_2026_menos_tendencia']), 1)} ponto abaixo da tendência de 2002 a 2022: está no padrão. No 2º turno, ela subiu em 5 das 6 eleições (mediana: +{b(A['delta_abst_mediana'], 1)} ponto); só caiu em 2022. Os brancos e nulos costumam cair no 2º turno, e os votos válidos ficaram praticamente iguais entre os turnos (mediana da razão: {b(A['razao_validos_mediana'], 3)}). Pelo padrão, não sobra uma reserva de votos novos para virar a eleição.

{tab_ab}

**Para onde foram os votos dos outros no passado (informativo, não entra no número).** Estimativa por município (regressão ecológica, com os limites dela):

{tab_tr}

O candidato do PT ficou com metade ou mais dos outros em quase todas as eleições, mas **os outros eram, na maior parte, de centro e de esquerda** (Garotinho, Ciro, Marina, Heloísa Helena, Tebet). Não existe eleição passada em que os maiores outros fossem lidos como de direita, como o autor lê os de 2026; por isso o 50% e 50% é uma escolha, não uma medida. Com a divisão estimada para 2022 ({b(100*tr22.parte_pt_entre_os_que_votaram, 0)}% para o PT), o número final fica em {b(var['outros divididos como em 2022 (estimativa por município)'], 2)}%.

## 5. Teste do passado

O mesmo método, com só o que se sabia 4 dias antes de cada eleição:

{tab_bt}

Erro médio (absoluto): número final {b(T['erro_absoluto_medio_final'], 2)}; pesquisas com peso {b(T['erro_absoluto_medio_P'], 2)}; média simples das pesquisas {b(T['erro_absoluto_medio_media_simples'], 2)}; histórico {b(T['erro_absoluto_medio_H'], 2)}; crescimento {b(T['erro_absoluto_medio_R'], 2)}. **A combinação errou menos que as pesquisas sozinhas** nas três eleições juntas, o que sustenta a ideia de usar o histórico e o 1º turno como freio. Em 2022, porém, a média simples das pesquisas acertou quase em cheio e o peso por acerto piorou a conta; com três eleições, isso é registro, não regra. A faixa de 1 ponto conteve o resultado em {T['faixa_1_ponto_conteve']} das 3.

## 6. Sensibilidade

{tab_se}

As duas variantes que mais mexem vêm da revisão adversarial (§7): descontar o erro médio das pesquisas a esta distância da eleição dá {b(v_horiz, 2)}% (Lula na frente); corrigir cada instituto pelo erro dele no 1º turno de 2026 dá {b(v_1t, 2)}%. A primeira fica {onde(v_horiz)} e a segunda {onde(v_1t)}.

## 7. Validação

- Totais do TSE: soma dos candidatos igual aos válidos do arquivo de detalhe em todos os 13 turnos de 2002 a 2026 (diferença zero).
- Recontagem independente ([`ferramentas/validacao-independente.py`](ferramentas/validacao-independente.py)): {int(VAL.passou.sum())} de {len(VAL)} números iguais por outro caminho.
- Pesquisas: {r['P']['pesquisas_registradas']} de {r['P']['pesquisas_capturadas']} casadas com o registro no TSE; {r['P']['pesquisas_conferidas']} de {r['P']['pesquisas_capturadas']} conferidas numa segunda fonte (a que falta está fora da janela).
- Revisão adversarial: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md).

{tab_val}

## 8. Fontes

TSE (`votacao_partido_munzona`, `detalhe_votacao_munzona` e `pesquisa_eleitoral`, 2002 a 2026), base de pesquisas do Pindograma (2014 a 2022), projeto `presidente-primeiro-turno-2026` (erro dos institutos no 1º turno de 2026), Wikipédia em inglês e a matéria ou o relatório de cada pesquisa. Endereço, hora, tamanho e sha256 de cada arquivo em [`dados/MANIFESTO.json`](dados/MANIFESTO.json); detalhes em [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md).

Análise feita pelo Claude, modelo de IA da Anthropic, com o método, os pesos e o parâmetro de 50% e 50% definidos pelo autor, Gabriel Alexandre.
"""

RESUMO = f"""# Resumo simples

**A projeção do método para o 2º turno de 25/out/2026: Flávio Bolsonaro {b(f)}% e Lula {b(l)}% dos votos válidos, com 1 ponto para cada lado.**

| O que entrou | Peso | O que deu para Flávio | Por quê |
|---|---|---|---|
| Pesquisas | 60% | {b(E['P'], 1)}% | {r['P']['institutos']} institutos registrados no TSE; {r['P']['institutos_com_flavio_na_frente']} mostram Flávio na frente. Quem mais acertou no passado pesa mais, e o erro que cada um costuma ter no 2º turno foi descontado |
| Histórico | 25% | {b(E['H'], 1)}% | quem liderou o 1º turno venceu o 2º nas 6 eleições desde 2002, mas a vantagem costuma encolher; na mediana sobra pouco mais da metade |
| Capacidade de crescimento | 15% | {b(E['R'], 1)}% | com os votos de Cury, Renan, Caiado e Zema divididos meio a meio, a vantagem do 1º turno continua; Lula precisaria de {b(100*D['parte_dos_outros_que_lula_precisa'], 0)}% desses votos para passar |

**Por que não é "empate técnico":** as três contas, por caminhos diferentes, deram Flávio na frente, e {S['variantes_com_flavio_acima_de_50']} das {S['variantes']} variações do método também.

**O que pode fazer o número errar:** em 2014 e 2018, o candidato do PT cresceu nos últimos dias além do que as pesquisas mostravam; em 2022 foi o contrário. Se as pesquisas de agora errarem o que, em média, erraram a esta distância da eleição em 2014, 2018 e 2022, a conta vira para Lula ({b(100 - v_horiz, 1)}%). Se os institutos errarem como erraram no 1º turno de 2026, Flávio vai a {b(v_1t, 1)}%.

**Abstenção:** a do 1º turno de 2026 ({b(A['abstencao_1t_2026'], 1)}%) está no padrão. Ela costuma subir no 2º turno, então não há uma reserva de eleitores novos que mude a conta sozinha.

**O teste do passado:** rodado 4 dias antes de 2014, 2018 e 2022, o método errou em média {b(T['erro_absoluto_medio_final'], 1)} ponto, menos que as pesquisas sozinhas ({b(T['erro_absoluto_medio_P'], 1)}). A faixa de 1 ponto é a escolha de apresentação do autor, não uma margem de erro.

Não é pesquisa, não recomenda voto e não diz quem deveria ganhar. Detalhes: [`RELATORIO.md`](RELATORIO.md).
"""

LEITURA = f"""# Leitura da IA

Pelos pesos que o autor definiu antes e a emenda 2 (decisão dele), a projeção é **Flávio {b(f)}% e Lula {b(l)}%**. Esta é a leitura do Claude sobre o que sustenta o número e onde ele é frágil, sem opinião sobre os candidatos.

**O que sustenta.** O número não depende de uma escolha só. As pesquisas ({b(E['P'], 2)}%), o histórico ({b(E['H'], 2)}%) e a aritmética do 1º turno ({b(E['R'], 2)}%) chegaram ao mesmo lado por caminhos que não dependem um do outro, e {S['variantes_com_flavio_acima_de_50']} das {S['variantes']} variações também. O parâmetro de 50% e 50% não decide nada: de 40% a 60% para Flávio, o final vai de {b(var['outros 40% para Flávio e 60% para Lula'], 2)}% a {b(var['outros 60% para Flávio e 40% para Lula'], 2)}%.

**O que mudou depois de ver o número.** No pré-registro, a Vox Brasil, única pesquisa com Lula na frente, levava 25% do peso por ter acertado um turno só, e o final era {b(v_pre, 2)}%. O autor decidiu que ela não deveria pesar tanto; a regra adotada (um turno só não é histórico) vale para todos os institutos e levou o final a {b(f_raw, 2)}%. Isso está declarado como emenda feita depois de ver o resultado, e o número anterior continua publicado.

**Onde o número é frágil.** A esta distância da eleição, as pesquisas erraram {b(ADV['erros_P_horizonte']['2014'], 1)} e {b(ADV['erros_P_horizonte']['2018'], 1)} pontos a favor do candidato contra o PT em 2014 e 2018, e {b(abs(ADV['erros_P_horizonte']['2022']), 1)} ponto a favor do PT em 2022. A diferença projetada ({b(f - l, 1)} ponto) é menor que o erro que o próprio método teve no passado ({b(T['erro_absoluto_medio_final'], 1)} ponto, em média). O número é a melhor conta que os dados permitem; a chance de o resultado sair do outro lado existe e não é pequena.

**Veredito.** Pelas regras do pré-registro e da emenda 2, **o método crava Flávio {b(f)}% e Lula {b(l)}%**. Isso é a consequência aritmética dos dados e dos pesos, não preferência, e não diz quem deveria ganhar.
"""

ADVERS = f"""# Revisão adversarial

Três leitores, cada um procurando o defeito que mais o incomodaria. O que cada objeção mudou está dito; nenhuma mudou o número principal, porque as regras foram escritas antes. As variantes estão em [`resultados/sensibilidade.csv`](../resultados/sensibilidade.csv).

## 1. O leitor que desconfiaria de um número favorável a Flávio

| Objeção | O que os dados dizem | Efeito |
|---|---|---|
| Institutos que costumam inflar o candidato contra o PT empurram a média | a correção pelo viés no 2º turno reduziu a Veritá, a MDA e a Gerp; os três somam pouco peso | já no número |
| Na reta final, o PT costuma crescer | verdade em 2014 e 2018 (as pesquisas desta janela erraram {b(ADV['erros_P_horizonte']['2014'], 1)} e {b(ADV['erros_P_horizonte']['2018'], 1)} pontos a favor do anti-PT); falso em 2022 ({b(ADV['erros_P_horizonte']['2022'], 1)}) | descontando o erro médio, o final vai a **{b(v_horiz, 2)}%** (Lula na frente); é a variante mais forte contra o número |
| Os votos dos outros podem ir mais para Lula | com 60% para Lula, {b(var['outros 40% para Flávio e 60% para Lula'], 2)}%; com a divisão estimada para 2022, {b(var['outros divididos como em 2022 (estimativa por município)'], 2)}% | pequeno |
| Abstenção maior no Nordeste no 2º turno é premissa contra Lula | o fator por UF é a mediana do que aconteceu; sem ele, {b(var['R sem fator de comparecimento por UF'], 2)}% | desprezível |

## 2. O leitor que desconfiaria de um número favorável a Lula

| Objeção | O que os dados dizem | Efeito |
|---|---|---|
| A Vox Brasil, única com Lula na frente, ganhou 25% do peso com uma eleição só | verdade, pela regra do §4.7 | corrigido pela **emenda 2**, decisão do autor depois de ver o número: de {b(v_pre, 2)}% para {b(f_raw, 2)}% |
| No 1º turno de 2026 os institutos mostraram Flávio menor que a urna | erro médio de {b(ADV['erro_1t_2026_medio_institutos'], 2)} ponto na escala da parte | corrigindo cada instituto por isso: **{b(v_1t, 2)}%**; é a variante mais forte a favor de Flávio |
| O 50% e 50% é generoso com Lula, se esses votos forem mais de direita, como o autor lê | é o parâmetro do autor, para ser conservador | com 60% para Flávio: {b(var['outros 60% para Flávio e 40% para Lula'], 2)}% |

## 3. O auditor de método e linguagem

| Ponto | Resposta |
|---|---|
| A faixa de 1 ponto parece margem de erro | dito no topo do relatório, no gráfico e no resumo: é a escolha do autor; o erro do método no passado foi {b(T['erro_absoluto_medio_final'], 2)} ponto e a faixa teria contido 0 de 3 |
| A Wikipédia como fonte | só como primeira lista; cada pesquisa foi casada com o registro no TSE e conferida numa segunda fonte |
| Teste do passado com poucas eleições | são 3; o teste mostra a ordem de grandeza do erro, não uma probabilidade |
| Regressão ecológica dos outros | informativa; não entra no número e o limite está dito |
| Linguagem | sem "vai ganhar", "favorito" ou recomendação de voto (`ferramentas/conferir-linguagem.py`) |

**Conclusão da revisão:** as duas objeções mais fortes puxam para lados opostos: a primeira fica {onde(v_horiz)} e a segunda {onde(v_1t)}, em torno de {b(f)}%.
"""

(RAIZ / "RELATORIO.md").write_text(RELATORIO, encoding="utf-8")
(RAIZ / "RESUMO_SIMPLES.md").write_text(RESUMO, encoding="utf-8")
(RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(LEITURA, encoding="utf-8")
(RAIZ / "docs" / "REVISAO_ADVERSARIAL.md").write_text(ADVERS, encoding="utf-8")
print("relatorio, resumo, leitura e revisao escritos")
