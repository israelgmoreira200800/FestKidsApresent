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
        db.session.execute(db.text("drop table if exists planejamentos_teste"))
        db.drop_all()
        db.create_all()


def limpar_banco(app):
    with app.app_context():
        db.session.rollback()
        db.session.execute(db.text("drop table if exists planejamentos_teste"))
        db.drop_all()


def cadastrar_fornecedor(client):
    return client.post(
        "/api/fornecedores",
        json={
            "nome_comercial": "Sabor Kids Buffet",
            "email": "sabor@festkids.local",
            "telefone": "(31) 91000-0001",
            "disponivel": True,
        },
    ).get_json()


def dados_servico(fornecedor_id):
    return {
        "fornecedor_id": fornecedor_id,
        "nome": "Buffet Completo",
        "descricao": "Buffet para ate 60 convidados",
        "categoria": "buffet",
        "preco_base": "1200.50",
        "capacidade_convidados": 60,
        "disponivel": True,
    }


def test_executa_crud_completo_de_servico_com_preco_decimal():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        fornecedor = cadastrar_fornecedor(client)
        cadastro = client.post(
            "/api/servicos",
            json=dados_servico(fornecedor["id"]),
        )
        servico = cadastro.get_json()

        assert cadastro.status_code == 201
        assert servico["preco_base"] == "1200.50"
        assert servico["categoria"] == "BUFFET"

        listagem = client.get("/api/servicos")
        assert listagem.status_code == 200
        assert len(listagem.get_json()) == 1

        consulta = client.get(f"/api/servicos/{servico['id']}")
        assert consulta.status_code == 200

        dados_atualizados = dados_servico(fornecedor["id"])
        dados_atualizados["nome"] = "Buffet Atualizado"
        dados_atualizados["preco_base"] = "999.90"
        dados_atualizados["disponivel"] = False
        atualizacao = client.put(
            f"/api/servicos/{servico['id']}",
            json=dados_atualizados,
        )

        assert atualizacao.status_code == 200
        assert atualizacao.get_json()["preco_base"] == "999.90"
        assert atualizacao.get_json()["disponivel"] is False

        exclusao = client.delete(f"/api/servicos/{servico['id']}")
        assert exclusao.status_code == 200
        assert client.get(
            f"/api/servicos/{servico['id']}"
        ).status_code == 404
    finally:
        limpar_banco(app)


def test_recusa_fornecedor_inexistente_preco_e_capacidade_invalidos():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        sem_fornecedor = client.post(
            "/api/servicos",
            json=dados_servico(99999),
        )
        assert sem_fornecedor.status_code == 400

        fornecedor = cadastrar_fornecedor(client)
        preco_invalido = dados_servico(fornecedor["id"])
        preco_invalido["preco_base"] = "10.999"
        assert client.post(
            "/api/servicos",
            json=preco_invalido,
        ).status_code == 400

        capacidade_invalida = dados_servico(fornecedor["id"])
        capacidade_invalida["capacidade_convidados"] = 0
        assert client.post(
            "/api/servicos",
            json=capacidade_invalida,
        ).status_code == 400
    finally:
        limpar_banco(app)


def test_recusa_categoria_invalida():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        fornecedor = cadastrar_fornecedor(client)
        dados = dados_servico(fornecedor["id"])
        dados["categoria"] = "categoria_inexistente"

        resposta = client.post("/api/servicos", json=dados)
        assert resposta.status_code == 400
        assert resposta.get_json()["erro"]["codigo"] == "validacao"
    finally:
        limpar_banco(app)


def test_recusa_exclusao_de_servico_usado_em_planejamento():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        fornecedor = cadastrar_fornecedor(client)
        servico = client.post(
            "/api/servicos",
            json=dados_servico(fornecedor["id"]),
        ).get_json()

        with app.app_context():
            db.session.execute(
                db.text(
                    """
                    create table planejamentos_teste (
                        id int auto_increment primary key,
                        servico_id int not null,
                        foreign key (servico_id) references servicos(id)
                    ) engine = InnoDB
                    """
                )
            )
            db.session.execute(
                db.text(
                    "insert into planejamentos_teste (servico_id) "
                    "values (:servico_id)"
                ),
                {"servico_id": servico["id"]},
            )
            db.session.commit()

        resposta = client.delete(f"/api/servicos/{servico['id']}")
        assert resposta.status_code == 409
        assert resposta.get_json()["erro"]["codigo"] == "conflito"
    finally:
        limpar_banco(app)
