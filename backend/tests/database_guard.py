NOME_BANCO_TESTES = "festkids_test"


def validar_nome_banco_testes(nome_banco):
    if nome_banco != NOME_BANCO_TESTES:
        raise ValueError(
            "Os testes so podem usar o banco festkids_test."
        )

    return nome_banco
