"""Testes das regras do pré-registro. Rodar: python -m pytest -q"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from previsao import modelo as M  # noqa: E402

RES = RAIZ / "resultados"


@pytest.fixture(scope="module")
def resumo():
    return json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))


def test_pesos_do_pre_registro():
    assert M.PESOS == {"P": 0.60, "H": 0.25, "R": 0.15}
    assert M.DIVISAO_OUTROS == 0.50


def test_final_soma_100_e_e_a_combinacao(resumo):
    f, e = resumo["final"], resumo["estimativas"]
    assert f["flavio"] + f["lula"] == pytest.approx(100)
    assert f["flavio_sem_arredondar"] == pytest.approx(0.6 * e["P"] + 0.25 * e["H"] + 0.15 * e["R"])
    assert f["flavio"] == round(f["flavio_sem_arredondar"], 1)


def test_pesquisas_usadas_registradas_e_conferidas():
    p = pd.read_csv(RES / "p_pesquisas_usadas.csv")
    assert p.instituto.is_unique
    assert p.registro_tse.str.match(r"^BR\d{9}$").all()
    assert (pd.to_datetime(p.campo_fim) >= "2026-10-12").all()
    assert p.peso.sum() == pytest.approx(1, abs=1e-3)  # a tabela publicada tem 4 casas
    assert p.peso.max() <= 0.25 + 1e-9


def test_teto_redistribui():
    pesq = pd.DataFrame({"instituto": ["a", "b", "c", "d", "e"], "anti_valido": [50, 51, 52, 53, 54]})
    nt = pd.DataFrame({"instituto": ["a", "b", "c", "d", "e"], "nota": [0.3, 3, 3, 3, 3], "vies_2t": [None] * 5, "n_2t": [0] * 5, "n_rodadas": [1] * 5})
    _, d = M.estimativa_P(pesq, nt)
    assert d.peso.max() == pytest.approx(0.25)
    assert d.peso.sum() == pytest.approx(1)


def test_correcao_de_vies_encolhe():
    pesq = pd.DataFrame({"instituto": ["a"], "anti_valido": [52.0]})
    nt = pd.DataFrame({"instituto": ["a"], "nota": [2.0], "vies_2t": [3.0], "n_2t": [3], "n_rodadas": [3]})
    _, d = M.estimativa_P(pesq, nt)
    assert d.anti_corrigido.iloc[0] == pytest.approx(52 - 3 * 3 / 5)


def test_lider_do_primeiro_turno_e_tabela_historica():
    t = M.tabela_lideranca()
    assert list(t.ano) == [2002, 2006, 2010, 2014, 2018, 2022]
    assert t.lider_venceu.all()


def test_r_simetrico_com_divisao():
    r40, _ = M.estimativa_R(2026, divisao=0.4)
    r60, _ = M.estimativa_R(2026, divisao=0.6)
    r50, _ = M.estimativa_R(2026, divisao=0.5)
    assert r40 < r50 < r60


def test_validacao_independente_passou():
    v = pd.read_csv(RES / "validacao_independente.csv")
    assert v.passou.all()
