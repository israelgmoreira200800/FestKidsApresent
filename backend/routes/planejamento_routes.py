from flask import Blueprint

from backend.controllers.planejamento_controller import criar_sugestao


planejamento_blueprint = Blueprint(
    "planejamentos",
    __name__,
    url_prefix="/api/planejamentos",
)


@planejamento_blueprint.post("/sugestao")
def sugerir_planejamento():
    return criar_sugestao()
