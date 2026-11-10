from backend import create_app
from backend.extensions import db
from backend.models import Fornecedor
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
        db.session.execute(db.text("drop table if exists servicos_teste"))
        db.drop_all()
        db.create_all()


def limpar_banco(app):
    with app.app_context():
        db.session.rollback()
        db.session.execute(db.text("drop table if exists servicos_teste"))
        db.drop_all()


def dados_fornecedor(nome="Sabor Kids Buffet", email="sabor@festkids.local"):
    return {
        "nome_comercial": nome,
        "email": email,
        "telefone": "(31) 91000-0001",
        "disponivel": True,
    }


def test_executa_crud_completo_de_fornecedor():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        cadastro = client.post(
            "/api/fornecedores",
            json=dados_fornecedor(),
        )
        fornecedor = cadastro.get_json()
        assert cadastro.status_code == 201
        assert fornecedor["disponivel"] is True

        listagem = client.get("/api/fornecedores")
        assert listagem.status_code == 200
        assert len(listagem.get_json()) == 1

        consulta = client.get(f"/api/fornecedores/{fornecedor['id']}")
        assert consulta.status_code == 200

        atualizacao = client.put(
            f"/api/fornecedores/{fornecedor['id']}",
            json={
                "nome_comercial": "Sabor Kids Atualizado",
                "email": "sabor.atualizado@festkids.local",
                "telefone": "(31) 91000-0099",
                "disponivel": False,
            },
        )
        assert atualizacao.status_code == 200
        assert atualizacao.get_json()["disponivel"] is False

        exclusao = client.delete(f"/api/fornecedores/{fornecedor['id']}")
        assert exclusao.status_code == 200
        assert client.get(
            f"/api/fornecedores/{fornecedor['id']}"
        ).status_code == 404
    finally:
        limpar_banco(app)


def test_recusa_disponibilidade_que_nao_seja_booleana():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()
    dados = dados_fornecedor()
    dados["disponivel"] = "sim"

    try:
        resposta = client.post("/api/fornecedores", json=dados)
        assert resposta.status_code == 400
        assert resposta.get_json()["erro"]["codigo"] == "validacao"
    finally:
        limpar_banco(app)


def test_recusa_email_duplicado_de_fornecedor():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        primeira = client.post(
            "/api/fornecedores",
            json=dados_fornecedor(),
        )
        segunda = client.post(
            "/api/fornecedores",
            json=dados_fornecedor("Outro Buffet"),
        )

        assert primeira.status_code == 201
        assert segunda.status_code == 409
    finally:
        limpar_banco(app)


def test_recusa_exclusao_de_fornecedor_com_servico_vinculado():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        fornecedor = client.post(
            "/api/fornecedores",
            json=dados_fornecedor(),
        ).get_json()

        with app.app_context():
            db.session.execute(
                db.text(
                    """
                    create table servicos_teste (
                        id int auto_increment primary key,
                        fornecedor_id int not null,
                        foreign key (fornecedor_id) references fornecedores(id)
                    ) engine = InnoDB
                    """
                )
            )
            db.session.execute(
                db.text(
                    "insert into servicos_teste (fornecedor_id) "
                    "values (:fornecedor_id)"
                ),
                {"fornecedor_id": fornecedor["id"]},
            )
            db.session.commit()

        resposta = client.delete(
            f"/api/fornecedores/{fornecedor['id']}"
        )

        assert resposta.status_code == 409
        assert resposta.get_json()["erro"]["codigo"] == "conflito"

        with app.app_context():
            assert Fornecedor.query.filter_by(
                id=fornecedor["id"]
            ).first() is not None
    finally:
        limpar_banco(app)
