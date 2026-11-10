from datetime import date, timedelta
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


def criar_cenario(data_confirmada, status_confirmada="CONFIRMADA"):
    cliente = Cliente(
        nome="Ana Demonstração",
        email="ana.agenda@festkids.local",
        telefone="(31) 90000-0001",
    )
    fornecedor = Fornecedor(
        nome_comercial="Sabor Kids",
        email="sabor.agenda@festkids.local",
        telefone="(31) 91000-0001",
        disponivel=True,
    )
    db.session.add_all([cliente, fornecedor])
    db.session.flush()

    data_alvo = date(2027, 5, 15)
    festa_alvo = Festa(
        cliente_id=cliente.id,
        nome="Festa da Lia",
        data=data_alvo,
        local="Belo Horizonte",
        quantidade_convidados=50,
        orcamento=Decimal("5000.00"),
        status="RASCUNHO",
    )
    festa_existente = Festa(
        cliente_id=cliente.id,
        nome="Festa já confirmada",
        data=data_confirmada,
        local="Contagem",
        quantidade_convidados=40,
        orcamento=Decimal("4000.00"),
        status=status_confirmada,
    )
    servico_alvo = Servico(
        fornecedor_id=fornecedor.id,
        nome="Buffet alvo",
        categoria="BUFFET",
        preco_base=Decimal("1000.00"),
        capacidade_convidados=50,
        disponivel=True,
    )
    servico_confirmado = Servico(
        fornecedor_id=fornecedor.id,
        nome="Buffet confirmado",
        categoria="BUFFET",
        preco_base=Decimal("1100.00"),
        capacidade_convidados=50,
        disponivel=True,
    )
    db.session.add_all(
        [festa_alvo, festa_existente, servico_alvo, servico_confirmado]
    )
    db.session.flush()
    db.session.add_all(
        [
            PlanejamentoItem(
                festa_id=festa_alvo.id,
                servico_id=servico_alvo.id,
                preco_referencia=Decimal("1000.00"),
            ),
            PlanejamentoItem(
                festa_id=festa_existente.id,
                servico_id=servico_confirmado.id,
                preco_referencia=Decimal("1100.00"),
            ),
        ]
    )
    db.session.commit()
    return festa_alvo.id, festa_existente.id, fornecedor.id, data_alvo


def test_identifica_fornecedor_em_conflito_no_mesmo_dia():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, festa_conflitante_id, fornecedor_id, data_alvo = (
                criar_cenario(date(2027, 5, 15))
            )

        resposta = client.get(f"/api/planejamentos/{festa_id}/agenda")

        assert resposta.status_code == 200
        assert resposta.get_json() == {
            "festa_id": festa_id,
            "data": data_alvo.isoformat(),
            "disponivel": False,
            "conflitos": [
                {
                    "fornecedor_id": fornecedor_id,
                    "fornecedor_nome": "Sabor Kids",
                    "festa_conflitante_id": festa_conflitante_id,
                    "festa_conflitante_nome": "Festa já confirmada",
                    "data": data_alvo.isoformat(),
                }
            ],
        }
    finally:
        limpar_banco(app)


def test_informa_agenda_livre_em_outro_dia_ou_festa_nao_confirmada():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, _, _, data_alvo = criar_cenario(
                date(2027, 5, 15) + timedelta(days=1)
            )

        resposta = client.get(f"/api/planejamentos/{festa_id}/agenda")

        assert resposta.status_code == 200
        assert resposta.get_json() == {
            "festa_id": festa_id,
            "data": data_alvo.isoformat(),
            "disponivel": True,
            "conflitos": [],
        }
    finally:
        limpar_banco(app)


def test_festa_em_rascunho_no_mesmo_dia_nao_reserva_fornecedor():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, _, _, data_alvo = criar_cenario(
                date(2027, 5, 15),
                status_confirmada="RASCUNHO",
            )

        resposta = client.get(f"/api/planejamentos/{festa_id}/agenda")

        assert resposta.status_code == 200
        assert resposta.get_json() == {
            "festa_id": festa_id,
            "data": data_alvo.isoformat(),
            "disponivel": True,
            "conflitos": [],
        }
    finally:
        limpar_banco(app)
