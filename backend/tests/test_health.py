from backend import create_app
from backend.tests.database_guard import validar_nome_banco_testes


def test_rota_de_saude_responde_com_sucesso():
    validar_nome_banco_testes("festkids_test")

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                "mysql+pymysql://root@127.0.0.1:3308/festkids_test"
            ),
        }
    )

    resposta = app.test_client().get("/api/saude")

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        "aplicacao": "FestKids",
        "status": "ok",
    }
