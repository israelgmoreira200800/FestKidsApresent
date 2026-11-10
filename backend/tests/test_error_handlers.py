from backend import create_app
from backend.errors import ErroConflito, ErroValidacao
from backend.tests.database_guard import validar_nome_banco_testes


def criar_app_para_teste():
    validar_nome_banco_testes("festkids_test")

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                "mysql+pymysql://root@127.0.0.1:3308/festkids_test"
            ),
        }
    )

    @app.get("/teste/validacao")
    def provocar_erro_validacao():
        raise ErroValidacao("O nome e obrigatorio.")

    @app.get("/teste/conflito")
    def provocar_erro_conflito():
        raise ErroConflito("O registro possui um vinculo.")

    @app.get("/teste/erro-interno")
    def provocar_erro_interno():
        raise RuntimeError("detalhe interno que nao pode aparecer")

    return app


def test_erro_de_validacao_retorna_400():
    resposta = criar_app_para_teste().test_client().get("/teste/validacao")

    assert resposta.status_code == 400
    assert resposta.get_json() == {
        "erro": {
            "codigo": "validacao",
            "mensagem": "O nome e obrigatorio.",
        }
    }


def test_rota_inexistente_retorna_404():
    resposta = criar_app_para_teste().test_client().get("/rota-inexistente")

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"]["codigo"] == "nao_encontrado"


def test_erro_de_conflito_retorna_409():
    resposta = criar_app_para_teste().test_client().get("/teste/conflito")

    assert resposta.status_code == 409
    assert resposta.get_json() == {
        "erro": {
            "codigo": "conflito",
            "mensagem": "O registro possui um vinculo.",
        }
    }


def test_erro_inesperado_retorna_500_sem_detalhe_interno():
    resposta = criar_app_para_teste().test_client().get("/teste/erro-interno")
    corpo = resposta.get_json()

    assert resposta.status_code == 500
    assert corpo["erro"]["codigo"] == "erro_interno"
    assert "detalhe interno" not in corpo["erro"]["mensagem"]
    assert "traceback" not in resposta.get_data(as_text=True).lower()
