from flask import Blueprint


health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/api/saude")
def consultar_saude():
    return {
        "aplicacao": "FestKids",
        "status": "ok",
    }, 200
