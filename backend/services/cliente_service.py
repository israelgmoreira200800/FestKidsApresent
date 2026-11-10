from sqlalchemy.exc import IntegrityError

from backend.errors import ErroConflito, ErroValidacao, RecursoNaoEncontrado
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


def validar_dados_cliente(dados):
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados do cliente em formato JSON.")

    nome = validar_texto_obrigatorio(dados, "nome", 120)
    email = validar_texto_obrigatorio(dados, "email", 255).lower()
    telefone = validar_texto_obrigatorio(dados, "telefone", 20)

    if email.count("@") != 1 or "." not in email.split("@")[1]:
        raise ErroValidacao("Informe um e-mail valido.")

    return nome, email, telefone


def verificar_email_em_uso(email, cliente_id=None):
    cliente_existente = Cliente.query.filter_by(email=email).first()

    if cliente_existente and cliente_existente.id != cliente_id:
        raise ErroConflito("Ja existe um cliente com este e-mail.")


def buscar_cliente(cliente_id):
    cliente = Cliente.query.filter_by(id=cliente_id).first()

    if not cliente:
        raise RecursoNaoEncontrado("Cliente nao encontrado.")

    return cliente


def listar_clientes():
    return Cliente.query.order_by(Cliente.id).all()


def cadastrar_cliente(dados):
    nome, email, telefone = validar_dados_cliente(dados)
    verificar_email_em_uso(email)

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


def atualizar_cliente(cliente_id, dados):
    cliente = buscar_cliente(cliente_id)
    nome, email, telefone = validar_dados_cliente(dados)
    verificar_email_em_uso(email, cliente.id)

    cliente.nome = nome
    cliente.email = email
    cliente.telefone = telefone

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito("Ja existe um cliente com este e-mail.")

    return cliente


def excluir_cliente(cliente_id):
    cliente = buscar_cliente(cliente_id)

    try:
        db.session.delete(cliente)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito(
            "O cliente nao pode ser excluido porque possui festa vinculada."
        )
