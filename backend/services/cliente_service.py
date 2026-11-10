from sqlalchemy.exc import IntegrityError

from backend.errors import ErroConflito, ErroValidacao
from backend.extensions import db
from backend.models import Cliente


def validar_texto_obrigatorio(dados, campo, tamanho_maximo):
    valor = dados.get(campo)

    if not isinstance(valor, str) or not valor.strip():
        raise ErroValidacao(f"O campo {campo} e obrigatorio.")

    valor = valor.strip()

    if len(valor) > tamanho_maximo:
        raise ErroValidacao(
            f"O campo {campo} deve ter no maximo {tamanho_maximo} caracteres."
        )

    return valor


def cadastrar_cliente(dados):
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados do cliente em formato JSON.")

    nome = validar_texto_obrigatorio(dados, "nome", 120)
    email = validar_texto_obrigatorio(dados, "email", 255).lower()
    telefone = validar_texto_obrigatorio(dados, "telefone", 20)

    if email.count("@") != 1 or "." not in email.split("@")[1]:
        raise ErroValidacao("Informe um e-mail valido.")

    if Cliente.query.filter_by(email=email).first():
        raise ErroConflito("Ja existe um cliente com este e-mail.")

    cliente = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
    )

    try:
        db.session.add(cliente)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito("Ja existe um cliente com este e-mail.")

    return cliente
