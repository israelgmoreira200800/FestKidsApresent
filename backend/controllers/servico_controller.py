from flask import request

from backend.services.servico_service import (
    atualizar_servico,
    buscar_servico,
    cadastrar_servico,
    excluir_servico,
    listar_servicos,
)


def criar_servico():
    dados = request.get_json(silent=True)
    servico = cadastrar_servico(dados)
    return servico.para_dict(), 201


def listar_todos_servicos():
    servicos = listar_servicos()
    return [servico.para_dict() for servico in servicos], 200


def consultar_servico(servico_id):
    servico = buscar_servico(servico_id)
    return servico.para_dict(), 200


def editar_servico(servico_id):
    dados = request.get_json(silent=True)
    servico = atualizar_servico(servico_id, dados)
    return servico.para_dict(), 200


def remover_servico(servico_id):
    excluir_servico(servico_id)
    return {"mensagem": "Servico excluido com sucesso."}, 200
