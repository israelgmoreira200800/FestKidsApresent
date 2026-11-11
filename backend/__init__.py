from pathlib import Path

from flask import Flask

from backend.config import Configuracao
from backend.error_handlers import registrar_tratamento_erros
from backend.extensions import cors, db
from backend.routes import registrar_rotas


def create_app(configuracao_adicional=None):
    pasta_frontend = Path(__file__).resolve().parent.parent / "frontend"
    app = Flask(
        __name__,
        static_folder=str(pasta_frontend),
        static_url_path="",
    )
    app.config.from_object(Configuracao)

    if configuracao_adicional:
        app.config.update(configuracao_adicional)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("Defina DATABASE_URL antes de iniciar o FestKids.")

    db.init_app(app)
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["FRONTEND_ORIGINS"],
            }
        },
    )
    registrar_rotas(app)
    registrar_tratamento_erros(app)

    return app
