from flask import Blueprint

from backend.controllers.cliente_controller import (
    consultar_cliente,
    criar_cliente,
    editar_cliente,
    listar_todos_clientes,
    remover_cliente,
)


cliente_blueprint = Blueprint(
    "clientes",
    __name__,
    url_prefix="/api/clientes",
)


@cliente_blueprint.post("")
def cadastrar_cliente():
    return criar_cliente()


@cliente_blueprint.get("")
def listar_clientes():
    return listar_todos_clientes()


@cliente_blueprint.get("/<int:cliente_id>")
def buscar_cliente(cliente_id):
    return consultar_cliente(cliente_id)


@cliente_blueprint.put("/<int:cliente_id>")
def atualizar_cliente(cliente_id):
    return editar_cliente(cliente_id)


@cliente_blueprint.delete("/<int:cliente_id>")
def excluir_cliente(cliente_id):
    return remover_cliente(cliente_id)
