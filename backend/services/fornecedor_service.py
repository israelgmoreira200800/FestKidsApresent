from sqlalchemy.exc import IntegrityError

from backend.errors import ErroConflito, ErroValidacao, RecursoNaoEncontrado
from backend.extensions import db
from backend.models import Fornecedor


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


def validar_dados_fornecedor(dados, disponibilidade_padrao=True):
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados do fornecedor em formato JSON.")

    nome_comercial = validar_texto_obrigatorio(
        dados,
        "nome_comercial",
        120,
    )
    email = validar_texto_obrigatorio(dados, "email", 255).lower()
    telefone = validar_texto_obrigatorio(dados, "telefone", 20)
    disponivel = dados.get("disponivel", disponibilidade_padrao)

    if email.count("@") != 1 or "." not in email.split("@")[1]:
        raise ErroValidacao("Informe um e-mail valido.")

    if not isinstance(disponivel, bool):
        raise ErroValidacao("O campo disponivel deve ser verdadeiro ou falso.")

    return nome_comercial, email, telefone, disponivel


def verificar_email_em_uso(email, fornecedor_id=None):
    fornecedor_existente = Fornecedor.query.filter_by(email=email).first()

    if fornecedor_existente and fornecedor_existente.id != fornecedor_id:
        raise ErroConflito("Ja existe um fornecedor com este e-mail.")


def buscar_fornecedor(fornecedor_id):
    fornecedor = Fornecedor.query.filter_by(id=fornecedor_id).first()

    if not fornecedor:
        raise RecursoNaoEncontrado("Fornecedor nao encontrado.")

    return fornecedor


def listar_fornecedores():
    return Fornecedor.query.order_by(Fornecedor.id).all()


def cadastrar_fornecedor(dados):
    nome, email, telefone, disponivel = validar_dados_fornecedor(dados)
    verificar_email_em_uso(email)

    fornecedor = Fornecedor(
        nome_comercial=nome,
        email=email,
        telefone=telefone,
        disponivel=disponivel,
    )

    try:
        db.session.add(fornecedor)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito("Ja existe um fornecedor com este e-mail.")

    return fornecedor


def atualizar_fornecedor(fornecedor_id, dados):
    fornecedor = buscar_fornecedor(fornecedor_id)
    nome, email, telefone, disponivel = validar_dados_fornecedor(
        dados,
        fornecedor.disponivel,
    )
    verificar_email_em_uso(email, fornecedor.id)

    fornecedor.nome_comercial = nome
    fornecedor.email = email
    fornecedor.telefone = telefone
    fornecedor.disponivel = disponivel

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito("Ja existe um fornecedor com este e-mail.")

    return fornecedor


def excluir_fornecedor(fornecedor_id):
    fornecedor = buscar_fornecedor(fornecedor_id)

    try:
        db.session.delete(fornecedor)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito(
            "O fornecedor nao pode ser excluido porque possui servico vinculado."
        )
