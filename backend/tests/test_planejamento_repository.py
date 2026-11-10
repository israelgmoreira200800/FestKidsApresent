from datetime import date
from decimal import Decimal

from backend import create_app
from backend.extensions import db
from backend.models import Cliente, Festa, Fornecedor, PlanejamentoItem, Servico
from backend.repositories import PlanejamentoRepository
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
        db.session.rollback()
        db.drop_all()


def criar_base():
    cliente = Cliente(
        nome="Ana Demonstração",
        email="ana.repository@festkids.local",
        telefone="(31) 90000-0001",
    )
    fornecedor = Fornecedor(
        nome_comercial="Sabor Kids Buffet",
        email="sabor.repository@festkids.local",
        telefone="(31) 91000-0001",
        disponivel=True,
    )
    db.session.add_all([cliente, fornecedor])
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
    servico = Servico(
        fornecedor_id=fornecedor.id,
        nome="Buffet Completo",
        descricao="Buffet para 60 convidados",
        categoria="BUFFET",
        preco_base=Decimal("1200.50"),
        capacidade_convidados=60,
        disponivel=True,
    )
    db.session.add_all([festa, servico])
    db.session.flush()
    return festa, servico


def test_busca_parametrizada_filtra_servicos_elegiveis():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        with app.app_context():
            criar_base()

            elegiveis = PlanejamentoRepository.buscar_servicos_elegiveis(
                "BUFFET",
                50,
            )
            categoria_maliciosa = (
                PlanejamentoRepository.buscar_servicos_elegiveis(
                    "BUFFET' or 1=1 --",
                    50,
                )
            )
            capacidade_excedida = (
                PlanejamentoRepository.buscar_servicos_elegiveis(
                    "BUFFET",
                    100,
                )
            )

            assert len(elegiveis) == 1
            assert elegiveis[0]["preco_base"] == Decimal("1200.50")
            assert categoria_maliciosa == []
            assert capacidade_excedida == []
    finally:
        limpar_banco(app)


def test_lista_itens_sem_confirmar_a_transacao_do_service():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        with app.app_context():
            festa, servico = criar_base()
            db.session.add(
                PlanejamentoItem(
                    festa_id=festa.id,
                    servico_id=servico.id,
                    preco_referencia=servico.preco_base,
                )
            )
            db.session.flush()

            itens = PlanejamentoRepository.listar_itens_da_festa(festa.id)
            assert len(itens) == 1
            assert itens[0]["fornecedor_nome"] == "Sabor Kids Buffet"

            db.session.rollback()
            assert PlanejamentoRepository.listar_itens_da_festa(festa.id) == []
    finally:
        limpar_banco(app)
