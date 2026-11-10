from datetime import date
from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from backend.errors import ErroConflito, ErroValidacao, RecursoNaoEncontrado
from backend.extensions import db
from backend.models import Cliente, Festa


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


def validar_data(valor):
    if not isinstance(valor, str):
        raise ErroValidacao("Informe a data no formato AAAA-MM-DD.")

    try:
        return date.fromisoformat(valor)
    except ValueError:
        raise ErroValidacao("Informe uma data valida no formato AAAA-MM-DD.")


def validar_orcamento(valor):
    try:
        orcamento = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        raise ErroValidacao("Informe um orcamento valido.")

    if not orcamento.is_finite() or orcamento <= 0:
        raise ErroValidacao("O orcamento deve ser maior que zero.")

    if orcamento.as_tuple().exponent < -2:
        raise ErroValidacao("O orcamento deve possuir no maximo duas casas.")

    return orcamento.quantize(Decimal("0.01"))


def validar_dados_festa(dados, status_atual="RASCUNHO"):
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados da festa em formato JSON.")

    cliente_id = dados.get("cliente_id")
    nome = validar_texto_obrigatorio(dados, "nome", 120)
    data_festa = validar_data(dados.get("data"))
    local = validar_texto_obrigatorio(dados, "local", 180)
    quantidade = dados.get("quantidade_convidados")
    orcamento = validar_orcamento(dados.get("orcamento"))
    status_enviado = dados.get("status", status_atual)

    if isinstance(cliente_id, bool) or not isinstance(cliente_id, int):
        raise ErroValidacao("Informe um cliente_id valido.")

    if not Cliente.query.filter_by(id=cliente_id).first():
        raise ErroValidacao("O cliente informado nao existe.")

    if isinstance(quantidade, bool) or not isinstance(quantidade, int):
        raise ErroValidacao("Informe uma quantidade_convidados valida.")

    if quantidade <= 0:
        raise ErroValidacao("A quantidade_convidados deve ser maior que zero.")

    if status_enviado != status_atual:
        raise ErroValidacao(
            "O status da festa nao pode ser alterado pelo cadastro comum."
        )

    return cliente_id, nome, data_festa, local, quantidade, orcamento


def buscar_festa(festa_id):
    festa = Festa.query.filter_by(id=festa_id).first()

    if not festa:
        raise RecursoNaoEncontrado("Festa nao encontrada.")

    return festa


def listar_festas():
    return Festa.query.order_by(Festa.id).all()


def cadastrar_festa(dados):
    valores = validar_dados_festa(dados)
    festa = Festa(
        cliente_id=valores[0],
        nome=valores[1],
        data=valores[2],
        local=valores[3],
        quantidade_convidados=valores[4],
        orcamento=valores[5],
        status="RASCUNHO",
    )

    db.session.add(festa)
    db.session.commit()
    return festa


def atualizar_festa(festa_id, dados):
    festa = buscar_festa(festa_id)
    valores = validar_dados_festa(dados, festa.status)

    festa.cliente_id = valores[0]
    festa.nome = valores[1]
    festa.data = valores[2]
    festa.local = valores[3]
    festa.quantidade_convidados = valores[4]
    festa.orcamento = valores[5]

    db.session.commit()
    return festa


def excluir_festa(festa_id):
    festa = buscar_festa(festa_id)

    try:
        db.session.delete(festa)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroConflito(
            "A festa nao pode ser excluida porque possui planejamento vinculado."
        )
