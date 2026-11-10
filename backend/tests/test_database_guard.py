import pytest

from backend.tests.database_guard import validar_nome_banco_testes


def test_aceita_banco_exclusivo_de_testes():
    nome_validado = validar_nome_banco_testes("festkids_test")

    assert nome_validado == "festkids_test"


def test_recusa_banco_de_demonstracao():
    with pytest.raises(ValueError):
        validar_nome_banco_testes("festkids")


def test_recusa_outro_nome_de_banco():
    with pytest.raises(ValueError):
        validar_nome_banco_testes("outro_banco")
