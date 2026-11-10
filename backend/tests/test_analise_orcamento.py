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


def criar_planejamento():
    cliente = Cliente(
        nome="Ana Demonstração",
        email="ana.orcamento@festkids.local",
        telefone="(31) 90000-0001",
    )
    fornecedor = Fornecedor(
        nome_comercial="Sabor Kids",
        email="sabor.orcamento@festkids.local",
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
        orcamento=Decimal("2000.00"),
        status="RASCUNHO",
    )
    buffet = Servico(
        fornecedor_id=fornecedor.id,
        nome="Buffet",
        categoria="BUFFET",
        preco_base=Decimal("1300.00"),
        capacidade_convidados=50,
        disponivel=True,
    )
    decoracao = Servico(
        fornecedor_id=fornecedor.id,
        nome="Decoração",
        categoria="DECORACAO",
        preco_base=Decimal("800.00"),
        capacidade_convidados=50,
        disponivel=True,
    )
    db.session.add_all([festa, buffet, decoracao])
    db.session.flush()
    db.session.add_all(
        [
            PlanejamentoItem(
                festa_id=festa.id,
                servico_id=buffet.id,
                preco_referencia=Decimal("1000.00"),
            ),
            PlanejamentoItem(
                festa_id=festa.id,
                servico_id=decoracao.id,
                preco_referencia=Decimal("500.00"),
            ),
        ]
    )
    db.session.commit()
    return festa.id


def test_analisa_pacote_dentro_do_orcamento():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id = criar_planejamento()

        resposta = client.get(
            f"/api/planejamentos/{festa_id}/orcamento"
        )

        assert resposta.status_code == 200
        assert resposta.get_json() == {
            "festa_id": festa_id,
            "orcamento": "2000.00",
            "total": "1500.00",
            "saldo": "500.00",
            "percentual_utilizado": "75.00",
            "custo_por_convidado": "30.00",
            "excedente": "0.00",
            "viavel": True,
            "situacao": "DENTRO_DO_ORCAMENTO",
        }
    finally:
        limpar_banco(app)


def test_analisa_pacote_acima_do_orcamento():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id = criar_planejamento()
            festa = Festa.query.filter_by(id=festa_id).first()
            festa.orcamento = Decimal("1000.00")
            db.session.commit()

        resposta = client.get(
            f"/api/planejamentos/{festa_id}/orcamento"
        )

        assert resposta.status_code == 200
        assert resposta.get_json() == {
            "festa_id": festa_id,
            "orcamento": "1000.00",
            "total": "1500.00",
            "saldo": "-500.00",
            "percentual_utilizado": "150.00",
            "custo_por_convidado": "30.00",
            "excedente": "500.00",
            "viavel": False,
            "situacao": "ACIMA_DO_ORCAMENTO",
        }
    finally:
        limpar_banco(app)
