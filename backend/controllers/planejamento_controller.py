from flask import request

from backend.services.planejamento_service import sugerir_pacote


def criar_sugestao():
    dados = request.get_json(silent=True)
    resultado = sugerir_pacote(dados)
    return resultado, 200
