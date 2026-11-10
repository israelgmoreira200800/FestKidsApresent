from flask import request

from backend.services.cliente_service import cadastrar_cliente


def criar_cliente():
    dados = request.get_json(silent=True)
    cliente = cadastrar_cliente(dados)

    return cliente.para_dict(), 201
