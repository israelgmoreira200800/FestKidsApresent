from backend import create_app
from backend.tests.database_guard import validar_nome_banco_testes


def criar_aplicacao_de_teste():
    validar_nome_banco_testes("festkids_test")
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                "mysql+pymysql://root@127.0.0.1:3308/festkids_test"
            ),
        }
    )


def test_flask_entrega_frontend_e_api_na_mesma_origem():
    cliente = criar_aplicacao_de_teste().test_client()

    pagina_inicial = cliente.get("/")
    pagina_servicos = cliente.get("/servicos.html")
    javascript_api = cliente.get("/js/api.js")
    saude_api = cliente.get("/api/saude")

    assert pagina_inicial.status_code == 200
    assert b"FestKids | In" in pagina_inicial.data
    assert pagina_servicos.status_code == 200
    assert javascript_api.status_code == 200
    assert b'const URL_BASE_API = "";' in javascript_api.data
    assert saude_api.status_code == 200
