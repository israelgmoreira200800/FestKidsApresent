from flask import request

from backend.services.fornecedor_service import (
    atualizar_fornecedor,
    buscar_fornecedor,
    cadastrar_fornecedor,
    excluir_fornecedor,
    listar_fornecedores,
)


def criar_fornecedor():
    dados = request.get_json(silent=True)
    fornecedor = cadastrar_fornecedor(dados)
    return fornecedor.para_dict(), 201


def listar_todos_fornecedores():
    fornecedores = listar_fornecedores()
    return [fornecedor.para_dict() for fornecedor in fornecedores], 200


def consultar_fornecedor(fornecedor_id):
    fornecedor = buscar_fornecedor(fornecedor_id)
    return fornecedor.para_dict(), 200


def editar_fornecedor(fornecedor_id):
    dados = request.get_json(silent=True)
    fornecedor = atualizar_fornecedor(fornecedor_id, dados)
    return fornecedor.para_dict(), 200


def remover_fornecedor(fornecedor_id):
    excluir_fornecedor(fornecedor_id)
    return {"mensagem": "Fornecedor excluido com sucesso."}, 200
