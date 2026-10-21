"""Gráficos 1920x1080 para o vídeo, todos lidos de resultados/ (nenhum número à mão).

Cores iguais às dos projetos anteriores do canal: Lula #C8553D, Flávio #2D6A8A, base #6B6B6B.
Uso: python ferramentas/graficos.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import RES  # noqa: E402

COR = {"lula": "#C8553D", "flavio": "#2D6A8A", "base": "#6B6B6B", "claro": "#BDBDBD"}
FIG = RES / "figuras"
RODAPE = "Projeção aberta: github.com/Gabriel-Alexandre/previsao-segundo-turno-2026. Análise feita pelo Claude (IA da Anthropic), com o método do autor escrito antes"
plt.rcParams.update({"font.size": 18, "axes.titlesize": 26, "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "axes.facecolor": "white", "axes.titlepad": 24})


def br(x: float, casas: int = 1) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def nova(titulo: str, fonte: str):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.86, bottom=0.17)
    ax.set_title(titulo, loc="left")
    fig.text(0.01, 0.012, f"Fonte: {fonte}. {RODAPE}.", fontsize=11, color="#555555")
    return fig, ax


def salvar(fig, nome: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / nome)
    plt.close(fig)


def g01_resultado(r: dict) -> None:
    f, l = r["final"]["flavio"], r["final"]["lula"]
    fig, ax = nova("A projeção do método para o 2º turno (votos válidos)", "TSE, 17 pesquisas registradas no TSE, 2002 a 2026")
    fi, li = r["final"]["flavio_inteiro"], r["final"]["lula_inteiro"]
    for i, (nome, v, vi, cor) in enumerate((("Flávio Bolsonaro", f, fi, COR["flavio"]), ("Lula", l, li, COR["lula"]))):
        y = 1 - i
        ax.barh(y, v, height=0.5, color=cor)
        ax.errorbar(v, y, xerr=1, color="black", capsize=14, lw=2.5)
        ax.text(1.5, y, nome, va="center", color="white", fontsize=34, fontweight="bold")
        ax.text(v + 1.8, y, f"{br(v)}%", va="center", fontsize=54, fontweight="bold", color=cor)
        ax.text(v + 1.8, y - 0.3, f"faixa: {br(v - 1)}% a {br(v + 1)}%", va="center", fontsize=17, color="#333333")
    ax.axvline(50, color="black", lw=1.5, ls="--")
    ax.text(50, 1.45, "50%", ha="center", fontsize=16)
    ax.set_xlim(0, 70)
    ax.set_ylim(-0.6, 1.6)
    ax.set_yticks([])
    ax.set_xlabel("% dos votos válidos")
    ax.xaxis.set_label_coords(0.5, -0.06)
    fig.text(0.08, 0.05, "Pesos: pesquisas 60%, histórico 25%, crescimento 15%. Instituto com 1 turno de histórico conta como sem histórico (emenda 2). A faixa não é margem de erro.",
             fontsize=13, color="#333333")
    salvar(fig, "g01_resultado.png")


def g02_tres_estimativas(r: dict) -> None:
    e = r["estimativas"]
    fig, ax = nova("As três estimativas e o peso de cada uma", "resultados/RESUMO.json")
    nomes = [f"Pesquisas\n(peso 60%)", f"Histórico\n(peso 25%)", f"Crescimento\n(peso 15%)", "Número final"]
    vals = [e["P"], e["H"], e["R"], r["final"]["flavio_sem_arredondar"]]
    cores = [COR["flavio"], COR["flavio"], COR["flavio"], "black"]
    ax.bar(range(4), [v - 50 for v in vals], bottom=50, color=cores, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.05, f"{br(v, 2)}%", ha="center", fontsize=24, fontweight="bold")
    ax.axhline(50, color="black", lw=1.2)
    ax.set_xticks(range(4), nomes)
    ax.set_ylim(49.5, 51.4)
    ax.set_ylabel("Flávio, % dos válidos (acima de 50 = à frente)")
    salvar(fig, "g02_tres_estimativas.png")


def g03_pesquisas(p: pd.DataFrame) -> None:
    p = p.sort_values("anti_valido")
    fig, ax = nova("As 17 pesquisas usadas: a última de cada instituto, de 12 a 21/out", "Wikipédia (en), matéria ou relatório de cada instituto e registro no TSE")
    y = range(len(p))
    ax.scatter(p.anti_valido, y, s=200 + 4000 * p.peso, color=[COR["flavio"] if v > 50 else COR["lula"] for v in p.anti_valido], zorder=3)
    ax.scatter(p.anti_corrigido, y, s=60, marker="|", color="black", zorder=4, linewidths=3)
    for i, r in enumerate(p.itertuples()):
        ax.text(48.05, i, f"{r.instituto}  ({br(100 * r.peso, 0)}% do peso)", va="center", fontsize=14)
    ax.axvline(50, color="black", lw=1.2, ls="--")
    ax.set_yticks([])
    ax.set_xlim(48, 53)
    ax.set_xlabel("Flávio, % dos válidos na pesquisa (círculo, do tamanho do peso)  |  traço preto: depois da correção pelo erro do instituto no 2º turno")
    salvar(fig, "g03_pesquisas.png")


def g04_ranking(rank: pd.DataFrame, usados: set) -> None:
    rank = rank[rank.instituto.isin(usados)].sort_values("nota", ascending=False)
    fig, ax = nova("Quem mais acertou (erro médio, 2º turno pesando o dobro)", "Pindograma (2014 a 2022), projeto do vídeo 7 (1º turno de 2026) e TSE")
    ax.barh(rank.instituto, rank.nota, color=COR["base"])
    for i, r in enumerate(rank.itertuples()):
        n = int(r.n_rodadas)
        ax.text(r.nota + 0.05, i, f"{br(r.nota, 2)} ponto  ({n} turno{'s' if n > 1 else ''} medido{'s' if n > 1 else ''})", va="center", fontsize=14)
    ax.set_xlim(0, 5.2)
    ax.set_xlabel("erro médio na parte do candidato contra o PT, em pontos (menor = mais perto da urna)")
    salvar(fig, "g04_ranking_institutos.png")


def g05_lideranca(lid: pd.DataFrame, r: dict) -> None:
    fig, ax = nova("Quem liderou o 1º turno venceu o 2º nas 6 eleições", "TSE, 2002 a 2026")
    x = range(len(lid))
    ax.bar([i - 0.2 for i in x], lid.vantagem_1t, width=0.38, color=COR["claro"], label="vantagem no 1º turno (só os dois finalistas)")
    ax.bar([i + 0.2 for i in x], lid.vantagem_2t, width=0.38, color=COR["base"], label="vantagem no 2º turno")
    for i, rr in enumerate(lid.itertuples()):
        ax.text(i, max(rr.vantagem_1t, rr.vantagem_2t) + 0.8, f"{rr.lider_1t}\nsobrou {br(100 * rr.razao, 0)}%", ha="center", fontsize=14)
    ax.set_xticks(list(x), lid.ano.astype(str))
    ax.set_ylim(0, 40)
    ax.set_ylabel("vantagem do líder do 1º turno, em pontos")
    ax.legend(frameon=False, loc="upper right")
    h = r["H"]
    fig.text(0.08, 0.05, f"Mediana: sobra {br(100 * h['razao_mediana'], 0)}% da vantagem. Flávio liderou o 1º turno de 2026 por {br(h['vantagem_1t_anti'], 1)} pontos entre os dois "
             f"→ {br(h['razao_mediana'] * h['vantagem_1t_anti'], 1)} ponto no 2º.", fontsize=15)
    salvar(fig, "g05_lideranca_historica.png")


def g06_abstencao(ab: pd.DataFrame, r: dict) -> None:
    fig, ax = nova("Abstenção no 1º e no 2º turno", "TSE, detalhe da votação por município, 2002 a 2026")
    ab = ab.sort_values("ano")
    ax.plot(ab.ano, ab.abst_1t, marker="o", lw=3, ms=12, color=COR["claro"], label="1º turno")
    h = ab.dropna(subset=["abst_2t"])
    ax.plot(h.ano, h.abst_2t, marker="o", lw=3, ms=12, color=COR["base"], label="2º turno")
    for rr in ab.itertuples():
        tem2 = rr.abst_2t == rr.abst_2t
        primeiro_acima = tem2 and rr.abst_1t > rr.abst_2t  # o rotulo de cima vai para o maior dos dois (2022)
        ax.text(rr.ano, rr.abst_1t + (0.3 if primeiro_acima else -0.5), br(rr.abst_1t), ha="center", fontsize=14, color="#555555")
        if tem2:
            ax.text(rr.ano, rr.abst_2t + (-0.5 if primeiro_acima else 0.3), br(rr.abst_2t), ha="center", fontsize=14, fontweight="bold")
    a = r["abstencao"]
    ax.scatter([2026], [a["abstencao_2t_2026_se_mediana"]], s=250, facecolors="none", edgecolors="black", lw=2.5, zorder=5,
               label=f"2026 no 2º turno se repetir a mediana (+{br(a['delta_abst_mediana'])} ponto)")
    ax.set_xticks(list(ab.ano))
    ax.set_ylim(15.8, 23.8)
    ax.set_ylabel("% dos eleitores aptos")
    ax.legend(frameon=False, loc="upper left")
    salvar(fig, "g06_abstencao.png")


def g07_de_onde(r: dict, tr: pd.DataFrame) -> None:
    d = r["de_onde"]
    fig, ax = nova("Para passar Flávio, Lula precisaria de 62% dos outros", "TSE (1º turno de 2026) e estimativa por município, 2002 a 2022")
    ax.barh(["Lula precisaria", "parâmetro do método\n(50% e 50%)"], [100 * d["parte_dos_outros_que_lula_precisa"], 50], color=[COR["lula"], COR["base"]], height=0.55)
    for i, v in enumerate([100 * d["parte_dos_outros_que_lula_precisa"], 50]):
        ax.text(v + 1, i, f"{br(v, 0)}%", va="center", fontsize=30, fontweight="bold")
    ax.set_xlim(0, 100)
    fig.subplots_adjust(left=0.2)
    ax.set_xlabel("parte dos votos dos outros candidatos (Cury, Renan, Caiado, Zema e demais) que iria para Lula")
    txt = "No passado, o candidato do PT ficou com " + ", ".join(f"{br(100 * x, 0)}% ({a})" for a, x in zip(tr.ano, tr.parte_pt_entre_os_que_votaram)) + \
          "\ndos outros; mas os outros eram de centro e de esquerda (Ciro, Marina, Tebet, Garotinho). Em 2026, na leitura do autor, eles ficam mais à direita."
    fig.text(0.08, 0.045, txt, fontsize=14, color="#333333")
    salvar(fig, "g07_de_onde_viriam_os_votos.png")


def g08_teste(bt: pd.DataFrame) -> None:
    fig, ax = nova("Teste do passado: o método 4 dias antes de 2014, 2018 e 2022", "TSE e Pindograma")
    cols = [("erro_P", "Pesquisas", COR["flavio"]), ("erro_H", "Histórico", COR["base"]), ("erro_R", "Crescimento", COR["claro"]), ("erro_final", "Número final", "black")]
    for k, (c, nome, cor) in enumerate(cols):
        ax.bar([i + (k - 1.5) * 0.2 for i in range(len(bt))], bt[c], width=0.19, color=cor, label=nome)
    for i, rr in enumerate(bt.itertuples()):
        ax.text(i + 0.3, rr.erro_final + (0.15 if rr.erro_final > 0 else -0.35), br(rr.erro_final, 1), ha="center", fontsize=15, fontweight="bold")
    ax.axhline(0, color="black", lw=1)
    ax.axhspan(-1, 1, color="#EEEEEE", zorder=0)
    ax.set_xticks(range(len(bt)), bt.ano.astype(str))
    ax.set_ylabel("erro na parte do candidato contra o PT (pontos)")
    ax.set_ylim(-3, 4.5)
    ax.legend(frameon=False, ncol=4, loc="upper center")
    fig.text(0.08, 0.05, "Faixa cinza: 1 ponto para cada lado. Nas três eleições o número final ficou fora dela; o erro médio foi de "
             f"{br(bt.erro_final.abs().mean(), 1)} ponto.", fontsize=15)
    salvar(fig, "g08_teste_do_passado.png")


def g09_sensibilidade(s: pd.DataFrame, r: dict) -> None:
    s = s.sort_values("flavio")
    fig, ax = nova("O número muda pouco quando se troca a regra (18 variantes)", "resultados/sensibilidade.csv")
    ax.axvspan(r["final"]["flavio"] - 1, r["final"]["flavio"] + 1, color="#EEEEEE")
    ax.scatter(s.flavio, range(len(s)), s=160, color=[COR["flavio"] if v > 50 else COR["lula"] for v in s.flavio], zorder=3)
    for i, rr in enumerate(s.itertuples()):
        ax.text(51.7, i, rr.variante, va="center", fontsize=12)
    ax.axvline(50, color="black", ls="--", lw=1.2)
    ax.set_xlim(49, 54.6)
    ax.set_yticks([])
    ax.set_xlabel("Flávio, % dos válidos (faixa cinza: o número final, 1 ponto para cada lado)")
    salvar(fig, "g09_sensibilidade.png")


def g10_ufs(reg: pd.DataFrame) -> None:
    t = reg[reg.eleicoes_1t == 6].copy()
    t = t[t.acertos_1t == 6]
    fig, ax = nova("Os 4 estados que acertaram as 6 eleições, de 2002 a 2022", "TSE, votos por UF")
    ax.axis("off")
    for i, rr in enumerate(t.itertuples()):
        cor = COR["flavio"] if rr.vencedor_1t_2026.startswith("Flávio") else COR["lula"]
        ax.text(0.05 + i * 0.24, 0.6, rr.uf, fontsize=90, fontweight="bold", color=cor, transform=ax.transAxes)
        ax.text(0.05 + i * 0.24, 0.42, f"1º turno de 2026:\n{rr.vencedor_1t_2026}", fontsize=22, transform=ax.transAxes)
        ax.text(0.05 + i * 0.24, 0.25, f"6 de 6 no 1º turno\n{rr.acertos_2t} de 6 no 2º turno", fontsize=16, color="#333333", transform=ax.transAxes)
    fig.text(0.08, 0.08, "Empate: dois apontam para cada lado. Minas Gerais acertou as 6 nos dois turnos e deu Flávio no 1º turno de 2026; o Amazonas também e deu Lula.",
             fontsize=16)
    salvar(fig, "g10_estados_que_acertam.png")


def g11_emenda(r: dict, se: pd.DataFrame) -> None:
    pre = se.set_index("variante").flavio["como no pré-registro, antes da emenda 2 (Vox Brasil com 25% do peso)"]
    fig, ax = nova("Um acerto só não é histórico: o peso da Vox Brasil", "resultados/sensibilidade.csv e p_pesquisas_usadas.csv")
    ax.axis("off")
    p = pd.read_csv(RES / "p_pesquisas_usadas.csv").set_index("instituto")
    blocos = [("Peso da Vox Brasil", "25%", f"{br(100 * p.loc['Vox Brasil', 'peso'], 1)}%"), ("Flávio no número final", f"{br(pre, 1)}%", f"{br(r['final']['flavio'], 1)}%")]
    for i, (rot, antes, depois) in enumerate(blocos):
        x = 0.06 + i * 0.48
        ax.text(x, 0.80, rot, fontsize=26, fontweight="bold", transform=ax.transAxes)
        ax.text(x, 0.52, antes, fontsize=64, color=COR["claro"], transform=ax.transAxes)
        ax.text(x + 0.20, 0.55, "→", fontsize=50, transform=ax.transAxes)
        ax.text(x + 0.26, 0.52, depois, fontsize=64, fontweight="bold", color=COR["flavio"] if i else "black", transform=ax.transAxes)
        ax.text(x, 0.42, "antes", fontsize=16, color="#555555", transform=ax.transAxes)
        ax.text(x + 0.26, 0.42, "depois da regra", fontsize=16, color="#555555", transform=ax.transAxes)
    fig.text(0.08, 0.2, "A regra vale pra todo instituto com um turno só de histórico: Vox Brasil, Palver, Gerp e Indexa.\n"
             "Decisão do autor depois de ver o 1º número (emenda 2, publicada no repositório).", fontsize=18)
    salvar(fig, "g11_um_acerto_nao_e_historico.png")


def g12_placar(r: dict) -> None:
    e, hh = r["estimativas"], r["H"]
    fig, ax = nova("O resultado de cada parte, na ordem do peso", "resultados/RESUMO.json")
    ax.axis("off")
    linhas = [("Pesquisas", "60%", f"Flávio {br(e['P'], 1)}%", f"{r['P']['institutos_com_flavio_na_frente']} de {r['P']['institutos']} institutos com Flávio na frente"),
              ("Histórico", "25%", f"Flávio {br(e['H'], 1)}%", f"líder do 1º turno venceu {hh['lider_1t_venceu']}; os estados que acertam empatam, 2 a 2"),
              ("Crescimento", "15%", f"Flávio {br(e['R'], 1)}%", f"Lula precisaria de {br(100 * r['de_onde']['parte_dos_outros_que_lula_precisa'], 0)}% dos outros"),
              ("Abstenção", "fora da conta", "sem reserva", f"no 2º turno ela subiu em 5 de 6 eleições")]
    for i, (a, b, c, d) in enumerate(linhas):
        y = 0.82 - i * 0.17
        ax.text(0.02, y, a, fontsize=28, fontweight="bold", transform=ax.transAxes)
        ax.text(0.22, y, b, fontsize=20, color="#555555", transform=ax.transAxes)
        ax.text(0.38, y, c, fontsize=28, fontweight="bold", color=COR["flavio"] if c.startswith("Flávio") else "black", transform=ax.transAxes)
        ax.text(0.38, y - 0.06, d, fontsize=15, color="#333333", transform=ax.transAxes)
    ax.text(0.02, 0.08, f"Número final:  Flávio {br(r['final']['flavio'])}%  ·  Lula {br(r['final']['lula'])}%", fontsize=36, fontweight="bold", transform=ax.transAxes)
    salvar(fig, "g12_placar_por_parte.png")


def main() -> None:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    p = pd.read_csv(RES / "p_pesquisas_usadas.csv")
    g01_resultado(r)
    g02_tres_estimativas(r)
    g03_pesquisas(p)
    g04_ranking(pd.read_csv(RES / "institutos_ranking.csv"), set(p.instituto))
    g05_lideranca(pd.read_csv(RES / "h_lideranca.csv"), r)
    g06_abstencao(pd.read_csv(RES / "abstencao_historica.csv"), r)
    g07_de_onde(r, pd.read_csv(RES / "transferencia_historica.csv"))
    g08_teste(pd.read_csv(RES / "teste_do_passado.csv"))
    g09_sensibilidade(pd.read_csv(RES / "sensibilidade.csv"), r)
    g10_ufs(pd.read_csv(RES / "h_regras_por_uf.csv"))
    g11_emenda(r, pd.read_csv(RES / "sensibilidade.csv"))
    g12_placar(r)
    print(sorted(x.name for x in FIG.glob("*.png")))


if __name__ == "__main__":
    main()
