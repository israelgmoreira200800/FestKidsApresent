from concurrent.futures import ThreadPoolExecutor
from datetime import date
from decimal import Decimal
from threading import Barrier

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


def criar_festas_concorrentes():
    cliente = Cliente(
        nome="Ana Demonstração",
        email="ana.confirmacao@festkids.local",
        telefone="(31) 90000-0001",
    )
    fornecedor = Fornecedor(
        nome_comercial="Sabor Kids",
        email="sabor.confirmacao@festkids.local",
        telefone="(31) 91000-0001",
        disponivel=True,
    )
    db.session.add_all([cliente, fornecedor])
    db.session.flush()

    festas = [
        Festa(
            cliente_id=cliente.id,
            nome="Festa da Lia",
            data=date(2027, 5, 15),
            local="Belo Horizonte",
            quantidade_convidados=50,
            orcamento=Decimal("2000.00"),
            status="RASCUNHO",
        ),
        Festa(
            cliente_id=cliente.id,
            nome="Festa do Theo",
            data=date(2027, 5, 15),
            local="Contagem",
            quantidade_convidados=40,
            orcamento=Decimal("2000.00"),
            status="RASCUNHO",
        ),
    ]
    servicos = [
        Servico(
            fornecedor_id=fornecedor.id,
            nome="Buffet Lia",
            categoria="BUFFET",
            preco_base=Decimal("1000.00"),
            capacidade_convidados=60,
            disponivel=True,
        ),
        Servico(
            fornecedor_id=fornecedor.id,
            nome="Buffet Theo",
            categoria="BUFFET",
            preco_base=Decimal("1100.00"),
            capacidade_convidados=60,
            disponivel=True,
        ),
    ]
    db.session.add_all(festas + servicos)
    db.session.flush()
    db.session.add_all(
        [
            PlanejamentoItem(
                festa_id=festas[0].id,
                servico_id=servicos[0].id,
                preco_referencia=Decimal("1000.00"),
            ),
            PlanejamentoItem(
                festa_id=festas[1].id,
                servico_id=servicos[1].id,
                preco_referencia=Decimal("1100.00"),
            ),
        ]
    )
    db.session.commit()
    return festas[0].id, festas[1].id, servicos[0].id


def test_confirma_planejamento_como_reserva_academica():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, _, _ = criar_festas_concorrentes()

        resposta = client.post(
            f"/api/planejamentos/{festa_id}/confirmacao"
        )

        assert resposta.status_code == 200
        assert resposta.get_json()["tipo"] == "RESERVA_ACADEMICA"
        assert "pagamento" in resposta.get_json()["mensagem"]
        with app.app_context():
            assert Festa.query.filter_by(id=festa_id).first().status == (
                "CONFIRMADA"
            )
    finally:
        limpar_banco(app)


def test_faz_rollback_quando_pacote_ultrapassa_orcamento():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, _, _ = criar_festas_concorrentes()
            festa = Festa.query.filter_by(id=festa_id).first()
            festa.orcamento = Decimal("500.00")
            db.session.commit()

        resposta = client.post(
            f"/api/planejamentos/{festa_id}/confirmacao"
        )

        assert resposta.status_code == 409
        with app.app_context():
            assert Festa.query.filter_by(id=festa_id).first().status == (
                "RASCUNHO"
            )
    finally:
        limpar_banco(app)


def test_faz_rollback_quando_pacote_deixa_de_ser_valido():
    app = criar_app_para_teste()
    preparar_banco(app)
    client = app.test_client()

    try:
        with app.app_context():
            festa_id, _, servico_id = criar_festas_concorrentes()
            servico = Servico.query.filter_by(id=servico_id).first()
            servico.disponivel = False
            db.session.commit()

        resposta = client.post(
            f"/api/planejamentos/{festa_id}/confirmacao"
        )

        assert resposta.status_code == 409
        with app.app_context():
            assert Festa.query.filter_by(id=festa_id).first().status == (
                "RASCUNHO"
            )
    finally:
        limpar_banco(app)


def test_duas_confirmacoes_concorrentes_reservam_fornecedor_uma_vez():
    app = criar_app_para_teste()
    preparar_banco(app)

    try:
        with app.app_context():
            festa_um_id, festa_dois_id, _ = criar_festas_concorrentes()

        barreira = Barrier(2)

        def confirmar(festa_id):
            with app.test_client() as client:
                barreira.wait(timeout=5)
                resposta = client.post(
                    f"/api/planejamentos/{festa_id}/confirmacao"
                )
                return resposta.status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            resultados = list(
                executor.map(confirmar, [festa_um_id, festa_dois_id])
            )

        assert sorted(resultados) == [200, 409]
        with app.app_context():
            status = [
                festa.status
                for festa in Festa.query.order_by(Festa.id).all()
            ]
            assert status.count("CONFIRMADA") == 1
            assert status.count("RASCUNHO") == 1
    finally:
        limpar_banco(app)
