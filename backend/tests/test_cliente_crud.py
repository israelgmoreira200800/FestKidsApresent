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
        db.session.execute(db.text("drop table if exists festas_teste"))
        db.drop_all()
        db.create_all()


def limpar_banco(app):
    with app.app_context():
        db.session.rollback()
        db.session.execute(db.text("drop table if exists festas_teste"))
        db.drop_all()


def cadastrar_pela_api(client, nome, email):
    return client.post(
        "/api/clientes",
        json={
            "nome": nome,
            "email": email,
            "telefone": "(31) 90000-0001",
        },
    )


def test_lista_consulta_atualiza_e_exclui_cliente():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        primeiro = cadastrar_pela_api(
            client,
            "Ana Demonstração",
            "ana.demo@festkids.local",
        ).get_json()
        segundo = cadastrar_pela_api(
            client,
            "Bruno Demonstração",
            "bruno.demo@festkids.local",
        ).get_json()

        resposta_lista = client.get("/api/clientes")
        assert resposta_lista.status_code == 200
        assert [item["id"] for item in resposta_lista.get_json()] == [
            primeiro["id"],
            segundo["id"],
        ]

        resposta_consulta = client.get(f"/api/clientes/{primeiro['id']}")
        assert resposta_consulta.status_code == 200
        assert resposta_consulta.get_json()["nome"] == "Ana Demonstração"

        resposta_atualizacao = client.put(
            f"/api/clientes/{primeiro['id']}",
            json={
                "nome": "Ana Atualizada",
                "email": "ana.atualizada@festkids.local",
                "telefone": "(31) 90000-0099",
            },
        )
        assert resposta_atualizacao.status_code == 200
        assert resposta_atualizacao.get_json()["nome"] == "Ana Atualizada"

        resposta_exclusao = client.delete(
            f"/api/clientes/{primeiro['id']}"
        )
        assert resposta_exclusao.status_code == 200

        resposta_apos_exclusao = client.get(
            f"/api/clientes/{primeiro['id']}"
        )
        assert resposta_apos_exclusao.status_code == 404
    finally:
        limpar_banco(app)


def test_recusa_atualizacao_com_email_de_outro_cliente():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        primeiro = cadastrar_pela_api(
            client,
            "Ana Demonstração",
            "ana.demo@festkids.local",
        ).get_json()
        cadastrar_pela_api(
            client,
            "Bruno Demonstração",
            "bruno.demo@festkids.local",
        )

        resposta = client.put(
            f"/api/clientes/{primeiro['id']}",
            json={
                "nome": "Ana Demonstração",
                "email": "bruno.demo@festkids.local",
                "telefone": "(31) 90000-0001",
            },
        )

        assert resposta.status_code == 409
        assert resposta.get_json()["erro"]["codigo"] == "conflito"
    finally:
        limpar_banco(app)


def test_recusa_exclusao_de_cliente_com_vinculo():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        cliente = cadastrar_pela_api(
            client,
            "Ana Demonstração",
            "ana.demo@festkids.local",
        ).get_json()

        with app.app_context():
            db.session.execute(
                db.text(
                    """
                    create table festas_teste (
                        id int auto_increment primary key,
                        cliente_id int not null,
                        foreign key (cliente_id) references clientes(id)
                    ) engine = InnoDB
                    """
                )
            )
            db.session.execute(
                db.text(
                    "insert into festas_teste (cliente_id) values (:cliente_id)"
                ),
                {"cliente_id": cliente["id"]},
            )
            db.session.commit()

        resposta = client.delete(f"/api/clientes/{cliente['id']}")

        assert resposta.status_code == 409
        assert resposta.get_json()["erro"]["codigo"] == "conflito"

        with app.app_context():
            assert Cliente.query.filter_by(id=cliente["id"]).first() is not None
    finally:
        limpar_banco(app)
