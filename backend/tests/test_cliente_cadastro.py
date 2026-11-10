from backend import create_app
from backend.extensions import db
from backend.models import Cliente
from backend.tests.database_guard import validar_nome_banco_testes


def criar_app_para_teste():
    validar_nome_banco_testes("festkids_test")

    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                "mysql+pymysql://root@127.0.0.1:3308/festkids_test"
            ),
        }
    )


def preparar_banco(app):
    with app.app_context():
        db.drop_all()
        db.create_all()


def limpar_banco(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_cadastra_cliente_valido():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        resposta = app.test_client().post(
            "/api/clientes",
            json={
                "nome": "Ana Demonstração",
                "email": "ANA.DEMO@FESTKIDS.LOCAL",
                "telefone": "(31) 90000-0001",
            },
        )

        assert resposta.status_code == 201
        assert resposta.get_json()["id"] is not None
        assert resposta.get_json()["email"] == "ana.demo@festkids.local"

        with app.app_context():
            cliente = Cliente.query.filter_by(
                email="ana.demo@festkids.local"
            ).first()
            assert cliente is not None
    finally:
        limpar_banco(app)


def test_recusa_cadastro_sem_nome():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        resposta = app.test_client().post(
            "/api/clientes",
            json={
                "email": "ana.demo@festkids.local",
                "telefone": "(31) 90000-0001",
            },
        )

        assert resposta.status_code == 400
        assert resposta.get_json()["erro"]["codigo"] == "validacao"

        with app.app_context():
            assert Cliente.query.count() == 0
    finally:
        limpar_banco(app)


def test_recusa_email_invalido():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        resposta = app.test_client().post(
            "/api/clientes",
            json={
                "nome": "Ana Demonstração",
                "email": "email-invalido",
                "telefone": "(31) 90000-0001",
            },
        )

        assert resposta.status_code == 400
        assert resposta.get_json()["erro"]["mensagem"] == (
            "Informe um e-mail valido."
        )
    finally:
        limpar_banco(app)


def test_recusa_email_duplicado():
    app = criar_app_para_teste()
    preparar_banco(app)
    dados = {
        "nome": "Ana Demonstração",
        "email": "ana.demo@festkids.local",
        "telefone": "(31) 90000-0001",
    }

    try:
        primeira_resposta = app.test_client().post("/api/clientes", json=dados)
        segunda_resposta = app.test_client().post("/api/clientes", json=dados)

        assert primeira_resposta.status_code == 201
        assert segunda_resposta.status_code == 409
        assert segunda_resposta.get_json()["erro"]["codigo"] == "conflito"
    finally:
        limpar_banco(app)
