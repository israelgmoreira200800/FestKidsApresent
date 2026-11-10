from flask import Blueprint

from backend.controllers.servico_controller import (
    consultar_servico,
    criar_servico,
    editar_servico,
    listar_todos_servicos,
    remover_servico,
)


servico_blueprint = Blueprint(
    "servicos",
    __name__,
    url_prefix="/api/servicos",
)


@servico_blueprint.post("")
def cadastrar_servico():
    return criar_servico()


@servico_blueprint.get("")
def listar_servicos():
    return listar_todos_servicos()


@servico_blueprint.get("/<int:servico_id>")
def buscar_servico(servico_id):
    return consultar_servico(servico_id)


@servico_blueprint.put("/<int:servico_id>")
def atualizar_servico(servico_id):
    return editar_servico(servico_id)


@servico_blueprint.delete("/<int:servico_id>")
def excluir_servico(servico_id):
    return remover_servico(servico_id)
