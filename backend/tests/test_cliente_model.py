from backend import create_app
from backend.extensions import db
from backend.models import Cliente
from backend.tests.database_guard import validar_nome_banco_testes


def test_cliente_e_gravado_recuperado_e_serializado_no_mysql():
    validar_nome_banco_testes("festkids_test")

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                "mysql+pymysql://root@127.0.0.1:3308/festkids_test"
            ),
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        cliente = Cliente(
            nome="Cliente de Teste",
            email="cliente@festkids.local",
            telefone="(31) 90000-0099",
        )
        db.session.add(cliente)
        db.session.commit()

        cliente_recuperado = db.session.get(Cliente, cliente.id)

        assert cliente_recuperado is not None
        assert cliente_recuperado.nome == "Cliente de Teste"
        assert cliente_recuperado.para_dict() == {
            "id": cliente.id,
            "nome": "Cliente de Teste",
            "email": "cliente@festkids.local",
            "telefone": "(31) 90000-0099",
            "criado_em": cliente.criado_em.isoformat(),
        }

        db.session.remove()
        db.drop_all()
