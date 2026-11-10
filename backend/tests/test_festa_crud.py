from backend import create_app
from backend.extensions import db
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
        db.session.execute(db.text("drop table if exists itens_teste"))
        db.drop_all()
        db.create_all()


def limpar_banco(app):
    with app.app_context():
        db.session.rollback()
        db.session.execute(db.text("drop table if exists itens_teste"))
        db.drop_all()


def cadastrar_cliente(client):
    return client.post(
        "/api/clientes",
        json={
            "nome": "Ana Demonstração",
            "email": "ana.demo@festkids.local",
            "telefone": "(31) 90000-0001",
        },
    ).get_json()


def dados_festa(cliente_id):
    return {
        "cliente_id": cliente_id,
        "nome": "Festa da Lia",
        "data": "2027-05-15",
        "local": "Belo Horizonte",
        "quantidade_convidados": 50,
        "orcamento": "5000.00",
    }


def test_executa_crud_completo_de_festa():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        cliente = cadastrar_cliente(client)
        cadastro = client.post(
            "/api/festas",
            json=dados_festa(cliente["id"]),
        )
        festa = cadastro.get_json()

        assert cadastro.status_code == 201
        assert festa["data"] == "2027-05-15"
        assert festa["orcamento"] == "5000.00"
        assert festa["status"] == "RASCUNHO"

        listagem = client.get("/api/festas")
        assert listagem.status_code == 200
        assert len(listagem.get_json()) == 1

        consulta = client.get(f"/api/festas/{festa['id']}")
        assert consulta.status_code == 200

        atualizados = dados_festa(cliente["id"])
        atualizados["nome"] = "Festa da Lia Atualizada"
        atualizados["quantidade_convidados"] = 60
        atualizados["orcamento"] = "5500.90"
        atualizacao = client.put(
            f"/api/festas/{festa['id']}",
            json=atualizados,
        )
        assert atualizacao.status_code == 200
        assert atualizacao.get_json()["orcamento"] == "5500.90"

        exclusao = client.delete(f"/api/festas/{festa['id']}")
        assert exclusao.status_code == 200
        assert client.get(f"/api/festas/{festa['id']}").status_code == 404
    finally:
        limpar_banco(app)


def test_recusa_cliente_data_orcamento_e_convidados_invalidos():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        assert client.post(
            "/api/festas",
            json=dados_festa(99999),
        ).status_code == 400

        cliente = cadastrar_cliente(client)
        data_invalida = dados_festa(cliente["id"])
        data_invalida["data"] = "15/05/2027"
        assert client.post(
            "/api/festas",
            json=data_invalida,
        ).status_code == 400

        orcamento_invalido = dados_festa(cliente["id"])
        orcamento_invalido["orcamento"] = "0.00"
        assert client.post(
            "/api/festas",
            json=orcamento_invalido,
        ).status_code == 400

        convidados_invalidos = dados_festa(cliente["id"])
        convidados_invalidos["quantidade_convidados"] = 0
        assert client.post(
            "/api/festas",
            json=convidados_invalidos,
        ).status_code == 400
    finally:
        limpar_banco(app)


def test_recusa_confirmacao_pelo_crud_comum():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        cliente = cadastrar_cliente(client)
        dados = dados_festa(cliente["id"])
        dados["status"] = "CONFIRMADA"

        resposta = client.post("/api/festas", json=dados)

        assert resposta.status_code == 400
        assert resposta.get_json()["erro"]["codigo"] == "validacao"
    finally:
        limpar_banco(app)


def test_recusa_exclusao_de_festa_com_planejamento_vinculado():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        cliente = cadastrar_cliente(client)
        festa = client.post(
            "/api/festas",
            json=dados_festa(cliente["id"]),
        ).get_json()

        with app.app_context():
            db.session.execute(
                db.text(
                    """
                    create table itens_teste (
                        id int auto_increment primary key,
                        festa_id int not null,
                        foreign key (festa_id) references festas(id)
                    ) engine = InnoDB
                    """
                )
            )
            db.session.execute(
                db.text(
                    "insert into itens_teste (festa_id) values (:festa_id)"
                ),
                {"festa_id": festa["id"]},
            )
            db.session.commit()

        resposta = client.delete(f"/api/festas/{festa['id']}")
        assert resposta.status_code == 409
        assert resposta.get_json()["erro"]["codigo"] == "conflito"
    finally:
        limpar_banco(app)
