from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from backend import create_app
from backend.extensions import db
from backend.models import Cliente, Festa, Fornecedor, PlanejamentoItem, Servico
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


def criar_dados_relacionados():
    cliente = Cliente(
        nome="Ana Demonstração",
        email="ana.item@festkids.local",
        telefone="(31) 90000-0001",
    )
    fornecedor = Fornecedor(
        nome_comercial="Sabor Kids Buffet",
        email="sabor.item@festkids.local",
        telefone="(31) 91000-0001",
        disponivel=True,
    )
    db.session.add(cliente)
    db.session.add(fornecedor)
    db.session.flush()

    festa = Festa(
        cliente_id=cliente.id,
        nome="Festa da Lia",
        data="2027-05-15",
        local="Belo Horizonte",
        quantidade_convidados=50,
        orcamento=Decimal("5000.00"),
        status="RASCUNHO",
    )
    servico = Servico(
        fornecedor_id=fornecedor.id,
        nome="Buffet Completo",
        descricao="Buffet para 50 convidados",
        categoria="BUFFET",
        preco_base=Decimal("1200.50"),
        capacidade_convidados=50,
        disponivel=True,
    )
    db.session.add(festa)
    db.session.add(servico)
    db.session.flush()
    return festa, servico


def test_preserva_preco_e_serializa_item_de_planejamento():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        with app.app_context():
            festa, servico = criar_dados_relacionados()
            item = PlanejamentoItem(
                festa_id=festa.id,
                servico_id=servico.id,
                preco_referencia=servico.preco_base,
            )
            db.session.add(item)
            db.session.commit()

            servico.preco_base = Decimal("1500.00")
            db.session.commit()
            db.session.refresh(item)

            assert item.preco_referencia == Decimal("1200.50")
            assert item.para_dict() == {
                "id": item.id,
                "festa_id": festa.id,
                "servico_id": servico.id,
                "preco_referencia": "1200.50",
                "criado_em": item.criado_em.isoformat(),
            }
    finally:
        limpar_banco(app)


def test_recusa_item_duplicado_e_vinculos_inexistentes():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        with app.app_context():
            festa, servico = criar_dados_relacionados()
            db.session.add(
                PlanejamentoItem(
                    festa_id=festa.id,
                    servico_id=servico.id,
                    preco_referencia=Decimal("1200.50"),
                )
            )
            db.session.commit()

            db.session.add(
                PlanejamentoItem(
                    festa_id=festa.id,
                    servico_id=servico.id,
                    preco_referencia=Decimal("1200.50"),
                )
            )
            with pytest.raises(IntegrityError):
                db.session.commit()
            db.session.rollback()

            db.session.add(
                PlanejamentoItem(
                    festa_id=99999,
                    servico_id=servico.id,
                    preco_referencia=Decimal("1200.50"),
                )
            )
            with pytest.raises(IntegrityError):
                db.session.commit()
            db.session.rollback()
    finally:
        limpar_banco(app)
