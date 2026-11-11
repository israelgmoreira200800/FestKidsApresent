from datetime import date
from decimal import Decimal

from backend import create_app
from backend.extensions import db
from backend.models import Cliente, Festa, Fornecedor, PlanejamentoItem, Servico
from backend.tests.database_guard import validar_nome_banco_testes
from backend.tests.procedure_helpers import instalar_procedures_planejamento


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
        instalar_procedures_planejamento()


def limpar_banco(app):
    with app.app_context():
        db.session.rollback()
        db.drop_all()


def criar_festa_e_fornecedores():
    cliente = Cliente(
        nome="Ana Demonstração",
        email="ana.sugestao@festkids.local",
        telefone="(31) 90000-0001",
    )
    fornecedor_um = Fornecedor(
        nome_comercial="Sabor Kids",
        email="sabor.sugestao@festkids.local",
        telefone="(31) 91000-0001",
        disponivel=True,
    )
    fornecedor_dois = Fornecedor(
        nome_comercial="Festa Fácil",
        email="facil.sugestao@festkids.local",
        telefone="(31) 91000-0002",
        disponivel=True,
    )
    fornecedor_indisponivel = Fornecedor(
        nome_comercial="Buffet Indisponível",
        email="indisponivel.sugestao@festkids.local",
        telefone="(31) 91000-0003",
        disponivel=False,
    )
    db.session.add_all(
        [
            cliente,
            fornecedor_um,
            fornecedor_dois,
            fornecedor_indisponivel,
        ]
    )
    db.session.flush()

    festa = Festa(
        cliente_id=cliente.id,
        nome="Festa da Lia",
        data=date(2027, 5, 15),
        local="Belo Horizonte",
        quantidade_convidados=50,
        orcamento=Decimal("5000.00"),
        status="RASCUNHO",
    )
    servico_indisponivel = Servico(
        fornecedor_id=fornecedor_indisponivel.id,
        nome="Buffet muito barato",
        categoria="BUFFET",
        preco_base=Decimal("100.00"),
        capacidade_convidados=50,
        disponivel=True,
    )
    buffet_menor_id = Servico(
        fornecedor_id=fornecedor_um.id,
        nome="Buffet econômico A",
        categoria="BUFFET",
        preco_base=Decimal("900.00"),
        capacidade_convidados=50,
        disponivel=True,
    )
    buffet_maior_id = Servico(
        fornecedor_id=fornecedor_dois.id,
        nome="Buffet econômico B",
        categoria="BUFFET",
        preco_base=Decimal("900.00"),
        capacidade_convidados=60,
        disponivel=True,
    )
    decoracao = Servico(
        fornecedor_id=fornecedor_dois.id,
        nome="Decoração colorida",
        categoria="DECORACAO",
        preco_base=Decimal("650.00"),
        capacidade_convidados=100,
        disponivel=True,
    )
    db.session.add_all(
        [
            festa,
            servico_indisponivel,
            buffet_menor_id,
            buffet_maior_id,
            decoracao,
        ]
    )
    db.session.commit()
    return festa.id, buffet_menor_id.id, decoracao.id


def test_sugere_menor_preco_desempata_por_id_e_preserva_preco():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, buffet_id, decoracao_id = criar_festa_e_fornecedores()

        resposta = client.post(
            "/api/planejamentos/sugestao",
            json={
                "festa_id": festa_id,
                "categorias": ["buffet", "decoracao"],
            },
        )

        assert resposta.status_code == 200
        dados = resposta.get_json()
        assert dados["completo"] is True
        assert [item["servico_id"] for item in dados["itens"]] == [
            buffet_id,
            decoracao_id,
        ]
        assert dados["itens"][0]["preco_referencia"] == "900.00"

        repeticao = client.post(
            "/api/planejamentos/sugestao",
            json={
                "festa_id": festa_id,
                "categorias": ["buffet", "decoracao"],
            },
        )
        assert repeticao.status_code == 200
        assert len(repeticao.get_json()["itens"]) == 2

        with app.app_context():
            servico = Servico.query.filter_by(id=buffet_id).first()
            servico.preco_base = Decimal("1200.00")
            db.session.commit()
            item = PlanejamentoItem.query.filter_by(
                festa_id=festa_id,
                servico_id=buffet_id,
            ).first()
            assert item.preco_referencia == Decimal("900.00")
    finally:
        limpar_banco(app)


def test_categoria_sem_candidato_nao_substitui_pacote_anterior():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, buffet_id, _ = criar_festa_e_fornecedores()
            db.session.add(
                PlanejamentoItem(
                    festa_id=festa_id,
                    servico_id=buffet_id,
                    preco_referencia=Decimal("900.00"),
                )
            )
            db.session.commit()

        resposta = client.post(
            "/api/planejamentos/sugestao",
            json={
                "festa_id": festa_id,
                "categorias": ["BUFFET", "FOTOGRAFIA"],
            },
        )

        assert resposta.status_code == 200
        assert resposta.get_json() == {
            "completo": False,
            "pacote_substituido": False,
            "categorias_sem_candidato": ["FOTOGRAFIA"],
            "itens": [],
        }
        with app.app_context():
            itens = PlanejamentoItem.query.filter_by(festa_id=festa_id).all()
            assert len(itens) == 1
            assert itens[0].servico_id == buffet_id
    finally:
        limpar_banco(app)


def test_recusa_categoria_invalida_ou_repetida():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, _, _ = criar_festa_e_fornecedores()

        invalida = client.post(
            "/api/planejamentos/sugestao",
            json={"festa_id": festa_id, "categorias": ["MAGICA"]},
        )
        repetida = client.post(
            "/api/planejamentos/sugestao",
            json={"festa_id": festa_id, "categorias": ["BUFFET", "buffet"]},
        )

        assert invalida.status_code == 400
        assert repetida.status_code == 400
    finally:
        limpar_banco(app)
