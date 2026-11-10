from flask import Blueprint

from backend.controllers.fornecedor_controller import (
    consultar_fornecedor,
    criar_fornecedor,
    editar_fornecedor,
    listar_todos_fornecedores,
    remover_fornecedor,
)


fornecedor_blueprint = Blueprint(
    "fornecedores",
    __name__,
    url_prefix="/api/fornecedores",
)


@fornecedor_blueprint.post("")
def cadastrar_fornecedor():
    return criar_fornecedor()


@fornecedor_blueprint.get("")
def listar_fornecedores():
    return listar_todos_fornecedores()


@fornecedor_blueprint.get("/<int:fornecedor_id>")
def buscar_fornecedor(fornecedor_id):
    return consultar_fornecedor(fornecedor_id)


@fornecedor_blueprint.put("/<int:fornecedor_id>")
def atualizar_fornecedor(fornecedor_id):
    return editar_fornecedor(fornecedor_id)


@fornecedor_blueprint.delete("/<int:fornecedor_id>")
def excluir_fornecedor(fornecedor_id):
    return remover_fornecedor(fornecedor_id)
