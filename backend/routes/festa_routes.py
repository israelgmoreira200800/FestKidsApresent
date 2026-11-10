from flask import Blueprint

from backend.controllers.festa_controller import (
    consultar_festa,
    criar_festa,
    editar_festa,
    listar_todas_festas,
    remover_festa,
)


festa_blueprint = Blueprint(
    "festas",
    __name__,
    url_prefix="/api/festas",
)


@festa_blueprint.post("")
def cadastrar_festa():
    return criar_festa()


@festa_blueprint.get("")
def listar_festas():
    return listar_todas_festas()


@festa_blueprint.get("/<int:festa_id>")
def buscar_festa(festa_id):
    return consultar_festa(festa_id)


@festa_blueprint.put("/<int:festa_id>")
def atualizar_festa(festa_id):
    return editar_festa(festa_id)


@festa_blueprint.delete("/<int:festa_id>")
def excluir_festa(festa_id):
    return remover_festa(festa_id)
