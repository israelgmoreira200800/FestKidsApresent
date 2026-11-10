from flask import request

from backend import create_app
from backend.tests.database_guard import validar_nome_banco_testes


def criar_app_para_teste():
    validar_nome_banco_testes("festkids_test")

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                "mysql+pymysql://root@127.0.0.1:3308/festkids_test"
            ),
            "FRONTEND_ORIGINS": ["http://localhost:5500"],
            "MAX_CONTENT_LENGTH": 10,
        }
    )

    @app.post("/api/teste-corpo")
    def receber_corpo():
        return {"tamanho": len(request.get_data())}

    return app


def test_origem_local_permitida_recebe_cabecalho_cors():
    app = criar_app_para_teste()
    resposta = app.test_client().get(
        "/api/saude",
        headers={"Origin": "http://localhost:5500"},
    )

    assert resposta.headers["Access-Control-Allow-Origin"] == (
        "http://localhost:5500"
    )


def test_origem_nao_prevista_nao_recebe_cabecalho_cors():
    app = criar_app_para_teste()
    resposta = app.test_client().get(
        "/api/saude",
        headers={"Origin": "https://site-nao-permitido.example"},
    )

    assert "Access-Control-Allow-Origin" not in resposta.headers


def test_corpo_maior_que_limite_retorna_413():
    app = criar_app_para_teste()
    resposta = app.test_client().post(
        "/api/teste-corpo",
        data="12345678901",
        content_type="text/plain",
    )

    assert resposta.status_code == 413
    assert resposta.get_json() == {
        "erro": {
            "codigo": "requisicao_muito_grande",
            "mensagem": "A requisicao ultrapassou o tamanho permitido.",
        }
    }
