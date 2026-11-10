from flask import Blueprint

from backend.controllers.cliente_controller import criar_cliente


cliente_blueprint = Blueprint(
    "clientes",
    __name__,
    url_prefix="/api/clientes",
)


@cliente_blueprint.post("")
def cadastrar_cliente():
    return criar_cliente()
