from flask import Blueprint

from backend.controllers.planejamento_controller import (
    confirmar,
    consultar_agenda,
    consultar_orcamento,
    criar_sugestao,
)


planejamento_blueprint = Blueprint(
    "planejamentos",
    __name__,
    url_prefix="/api/planejamentos",
)


@planejamento_blueprint.post("/sugestao")
def sugerir_planejamento():
    return criar_sugestao()


@planejamento_blueprint.get("/<int:festa_id>/orcamento")
def analisar_orcamento_da_festa(festa_id):
    return consultar_orcamento(festa_id)


@planejamento_blueprint.get("/<int:festa_id>/agenda")
def verificar_agenda_da_festa(festa_id):
    return consultar_agenda(festa_id)


@planejamento_blueprint.post("/<int:festa_id>/confirmacao")
def confirmar_planejamento_da_festa(festa_id):
    return confirmar(festa_id)
