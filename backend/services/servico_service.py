from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from backend.errors import ErroConflito, ErroValidacao, RecursoNaoEncontrado
from backend.extensions import db
from backend.models import Fornecedor, Servico


CATEGORIAS_VALIDAS = {
    "BUFFET",
    "DECORACAO",
    "FOTOGRAFIA",
    "RECREACAO",
    "BOLO_E_DOCES",
    "ESPACO",
}


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


def validar_preco(valor):
    try:
        preco = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        raise ErroValidacao("Informe um preco_base valido.")

    if not preco.is_finite() or preco < 0:
        raise ErroValidacao("O preco_base deve ser maior ou igual a zero.")

    if preco.as_tuple().exponent < -2:
        raise ErroValidacao("O preco_base deve possuir no maximo duas casas.")

    return preco.quantize(Decimal("0.01"))


def validar_dados_servico(dados, disponibilidade_padrao=True):
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados do servico em formato JSON.")

    fornecedor_id = dados.get("fornecedor_id")
    nome = validar_texto_obrigatorio(dados, "nome", 120)
    categoria = validar_texto_obrigatorio(dados, "categoria", 40).upper()
    preco = validar_preco(dados.get("preco_base"))
    capacidade = dados.get("capacidade_convidados")
    disponivel = dados.get("disponivel", disponibilidade_padrao)
    descricao = dados.get("descricao")

    if isinstance(fornecedor_id, bool) or not isinstance(fornecedor_id, int):
        raise ErroValidacao("Informe um fornecedor_id valido.")

    if not Fornecedor.query.filter_by(id=fornecedor_id).first():
        raise ErroValidacao("O fornecedor informado nao existe.")

    if categoria not in CATEGORIAS_VALIDAS:
        raise ErroValidacao("Informe uma categoria valida.")

    if isinstance(capacidade, bool) or not isinstance(capacidade, int):
        raise ErroValidacao("Informe uma capacidade_convidados valida.")

    if capacidade <= 0:
        raise ErroValidacao("A capacidade_convidados deve ser maior que zero.")

    if not isinstance(disponivel, bool):
        raise ErroValidacao("O campo disponivel deve ser verdadeiro ou falso.")

    if descricao is not None:
        if not isinstance(descricao, str):
            raise ErroValidacao("O campo descricao deve ser um texto.")
        descricao = descricao.strip() or None

    return (
        fornecedor_id,
        nome,
        descricao,
        categoria,
        preco,
        capacidade,
        disponivel,
    )


def buscar_servico(servico_id):
    servico = Servico.query.filter_by(id=servico_id).first()

    if not servico:
        raise RecursoNaoEncontrado("Servico nao encontrado.")

    return servico


def listar_servicos():
    return Servico.query.order_by(Servico.id).all()


def cadastrar_servico(dados):
    valores = validar_dados_servico(dados)
    servico = Servico(
        fornecedor_id=valores[0],
        nome=valores[1],
        descricao=valores[2],
        categoria=valores[3],
        preco_base=valores[4],
        capacidade_convidados=valores[5],
        disponivel=valores[6],
    )

    db.session.add(servico)
    db.session.commit()
    return servico


def atualizar_servico(servico_id, dados):
    servico = buscar_servico(servico_id)
    valores = validar_dados_servico(dados, servico.disponivel)

    servico.fornecedor_id = valores[0]
    servico.nome = valores[1]
    servico.descricao = valores[2]
    servico.categoria = valores[3]
    servico.preco_base = valores[4]
    servico.capacidade_convidados = valores[5]
    servico.disponivel = valores[6]

    db.session.commit()
    return servico


def excluir_servico(servico_id):
    servico = buscar_servico(servico_id)

    try:
        db.session.delete(servico)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito(
            "O servico nao pode ser excluido porque esta em um planejamento."
        )
