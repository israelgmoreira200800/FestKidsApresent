from flask import request

from backend.services.planejamento_service import analisar_orcamento, sugerir_pacote


def criar_sugestao():
    dados = request.get_json(silent=True)
    resultado = sugerir_pacote(dados)
    return resultado, 200


def consultar_orcamento(festa_id):
    resultado = analisar_orcamento(festa_id)
    return resultado, 200
