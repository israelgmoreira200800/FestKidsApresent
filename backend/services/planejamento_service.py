from decimal import Decimal

from backend.errors import ErroConflito, ErroValidacao, RecursoNaoEncontrado
from backend.extensions import db
from backend.models import Festa, PlanejamentoItem
from backend.repositories import PlanejamentoRepository
from backend.services.servico_service import CATEGORIAS_VALIDAS


def validar_pedido_sugestao(dados):
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados da sugestao em formato JSON.")

    festa_id = dados.get("festa_id")
    categorias = dados.get("categorias")

    if isinstance(festa_id, bool) or not isinstance(festa_id, int):
        raise ErroValidacao("Informe um festa_id valido.")

    if not isinstance(categorias, list) or not categorias:
        raise ErroValidacao("Informe ao menos uma categoria.")

    categorias_normalizadas = []
    for categoria in categorias:
        if not isinstance(categoria, str):
            raise ErroValidacao("Informe apenas categorias validas.")

        categoria_normalizada = categoria.strip().upper()
        if categoria_normalizada not in CATEGORIAS_VALIDAS:
            raise ErroValidacao(
                f"A categoria {categoria_normalizada or categoria} e invalida."
            )

        if categoria_normalizada in categorias_normalizadas:
            raise ErroValidacao("Nao repita categorias na sugestao.")

        categorias_normalizadas.append(categoria_normalizada)

    return festa_id, categorias_normalizadas


def serializar_item_consultado(item):
    return {
        "item_id": item["item_id"],
        "festa_id": item["festa_id"],
        "servico_id": item["servico_id"],
        "preco_referencia": format(item["preco_referencia"], ".2f"),
        "servico_nome": item["servico_nome"],
        "categoria": item["categoria"],
        "fornecedor_id": item["fornecedor_id"],
        "fornecedor_nome": item["fornecedor_nome"],
    }


def sugerir_pacote(dados):
    festa_id, categorias = validar_pedido_sugestao(dados)
    festa = Festa.query.filter_by(id=festa_id).first()

    if not festa:
        raise RecursoNaoEncontrado("Festa nao encontrada.")

    if festa.status != "RASCUNHO":
        raise ErroConflito(
            "Somente uma festa em RASCUNHO pode receber nova sugestao."
        )

    servicos_escolhidos = []
    categorias_sem_candidato = []

    for categoria in categorias:
        candidatos = PlanejamentoRepository.buscar_servicos_elegiveis(
            categoria,
            festa.quantidade_convidados,
        )

        if not candidatos:
            categorias_sem_candidato.append(categoria)
            continue

        servicos_escolhidos.append(candidatos[0])

    if categorias_sem_candidato:
        return {
            "completo": False,
            "pacote_substituido": False,
            "categorias_sem_candidato": categorias_sem_candidato,
            "itens": [],
        }

    try:
        itens_anteriores = PlanejamentoItem.query.filter_by(
            festa_id=festa.id
        ).all()
        for item in itens_anteriores:
            db.session.delete(item)

        for servico in servicos_escolhidos:
            db.session.add(
                PlanejamentoItem(
                    festa_id=festa.id,
                    servico_id=servico["servico_id"],
                    preco_referencia=servico["preco_base"],
                )
            )

        db.session.flush()
        itens = PlanejamentoRepository.listar_itens_da_festa(festa.id)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "completo": True,
        "pacote_substituido": True,
        "categorias_sem_candidato": [],
        "itens": [serializar_item_consultado(item) for item in itens],
    }


def analisar_orcamento(festa_id):
    resumo = PlanejamentoRepository.buscar_resumo_orcamento(festa_id)

    if not resumo:
        raise RecursoNaoEncontrado("Festa nao encontrada.")

    orcamento = resumo["orcamento"]
    total = resumo["total_itens"]
    convidados = resumo["quantidade_convidados"]
    saldo = orcamento - total
    percentual = (total / orcamento * Decimal("100")).quantize(
        Decimal("0.01")
    )
    custo_por_convidado = (total / convidados).quantize(Decimal("0.01"))
    viavel = total <= orcamento
    excedente = Decimal("0.00") if viavel else total - orcamento

    return {
        "festa_id": resumo["festa_id"],
        "orcamento": format(orcamento, ".2f"),
        "total": format(total, ".2f"),
        "saldo": format(saldo, ".2f"),
        "percentual_utilizado": format(percentual, ".2f"),
        "custo_por_convidado": format(custo_por_convidado, ".2f"),
        "excedente": format(excedente, ".2f"),
        "viavel": viavel,
        "situacao": (
            "DENTRO_DO_ORCAMENTO" if viavel else "ACIMA_DO_ORCAMENTO"
        ),
    }


def verificar_agenda(festa_id):
    festa = Festa.query.filter_by(id=festa_id).first()

    if not festa:
        raise RecursoNaoEncontrado("Festa nao encontrada.")

    possui_itens = PlanejamentoItem.query.filter_by(festa_id=festa_id).first()
    if not possui_itens:
        raise ErroValidacao(
            "A festa precisa possuir um pacote para verificar a agenda."
        )

    conflitos_consultados = PlanejamentoRepository.buscar_conflitos_agenda(
        festa_id
    )
    conflitos = [
        {
            "fornecedor_id": conflito["fornecedor_id"],
            "fornecedor_nome": conflito["fornecedor_nome"],
            "festa_conflitante_id": conflito["festa_conflitante_id"],
            "festa_conflitante_nome": conflito["festa_conflitante_nome"],
            "data": conflito["data"].isoformat(),
        }
        for conflito in conflitos_consultados
    ]

    return {
        "festa_id": festa.id,
        "data": festa.data.isoformat(),
        "disponivel": len(conflitos) == 0,
        "conflitos": conflitos,
    }
