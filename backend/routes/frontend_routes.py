from flask import Blueprint, current_app


frontend_blueprint = Blueprint("frontend", __name__)


@frontend_blueprint.get("/")
def abrir_pagina_inicial():
    return current_app.send_static_file("index.html")
