from flask import request

from backend.services.festa_service import (
    atualizar_festa,
    buscar_festa,
    cadastrar_festa,
    excluir_festa,
    listar_festas,
)


def criar_festa():
    dados = request.get_json(silent=True)
    festa = cadastrar_festa(dados)
    return festa.para_dict(), 201


def listar_todas_festas():
    festas = listar_festas()
    return [festa.para_dict() for festa in festas], 200


def consultar_festa(festa_id):
    festa = buscar_festa(festa_id)
    return festa.para_dict(), 200


def editar_festa(festa_id):
    dados = request.get_json(silent=True)
    festa = atualizar_festa(festa_id, dados)
    return festa.para_dict(), 200


def remover_festa(festa_id):
    excluir_festa(festa_id)
    return {"mensagem": "Festa excluida com sucesso."}, 200
