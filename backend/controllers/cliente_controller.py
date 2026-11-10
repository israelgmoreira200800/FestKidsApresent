from flask import request

from backend.services.cliente_service import (
    atualizar_cliente,
    buscar_cliente,
    cadastrar_cliente,
    excluir_cliente,
    listar_clientes,
)


def criar_cliente():
    dados = request.get_json(silent=True)
    cliente = cadastrar_cliente(dados)

    return cliente.para_dict(), 201


def listar_todos_clientes():
    clientes = listar_clientes()
    return [cliente.para_dict() for cliente in clientes], 200


def consultar_cliente(cliente_id):
    cliente = buscar_cliente(cliente_id)
    return cliente.para_dict(), 200


def editar_cliente(cliente_id):
    dados = request.get_json(silent=True)
    cliente = atualizar_cliente(cliente_id, dados)
    return cliente.para_dict(), 200


def remover_cliente(cliente_id):
    excluir_cliente(cliente_id)
    return {"mensagem": "Cliente excluido com sucesso."}, 200
