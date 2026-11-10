from flask import current_app
from werkzeug.exceptions import HTTPException

from backend.errors import ErroAplicacao


def criar_resposta_erro(codigo, mensagem, status_http):
    resposta = {
        "erro": {
            "codigo": codigo,
            "mensagem": mensagem,
        }
    }
    return resposta, status_http


def registrar_tratamento_erros(app):
    @app.errorhandler(ErroAplicacao)
    def tratar_erro_aplicacao(erro):
        return criar_resposta_erro(
            erro.codigo,
            erro.mensagem,
            erro.status_http,
        )

    @app.errorhandler(HTTPException)
    def tratar_erro_http(erro):
        codigo = "nao_encontrado" if erro.code == 404 else "erro_http"
        return criar_resposta_erro(codigo, erro.description, erro.code)

    @app.errorhandler(Exception)
    def tratar_erro_inesperado(erro):
        current_app.logger.exception("Erro inesperado na API", exc_info=erro)
        return criar_resposta_erro(
            "erro_interno",
            "Ocorreu um erro interno. Tente novamente.",
            500,
        )
