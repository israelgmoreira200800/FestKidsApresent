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
    try:
        festa_bloqueada = PlanejamentoRepository.bloquear_festa(festa_id)

        if not festa_bloqueada:
            raise RecursoNaoEncontrado("Festa nao encontrada.")

        if festa_bloqueada["status"] != "RASCUNHO":
            raise ErroConflito(
                "Somente uma festa em RASCUNHO pode receber nova sugestao."
            )

        quantidade_convidados = festa_bloqueada["quantidade_convidados"]
        servicos_escolhidos = []
        categorias_sem_candidato = []

        for categoria in categorias:
            candidatos = PlanejamentoRepository.buscar_servicos_elegiveis(
                categoria,
                quantidade_convidados,
            )

            if not candidatos:
                categorias_sem_candidato.append(categoria)
                continue

            servicos_escolhidos.append(candidatos[0])

        if categorias_sem_candidato:
            db.session.rollback()
            return {
                "completo": False,
                "pacote_substituido": False,
                "categorias_sem_candidato": categorias_sem_candidato,
                "itens": [],
            }

        itens_anteriores = PlanejamentoItem.query.filter_by(
            festa_id=festa_id
        ).all()
        for item in itens_anteriores:
            db.session.delete(item)
        db.session.flush()

        for servico in servicos_escolhidos:
            db.session.add(
                PlanejamentoItem(
                    festa_id=festa_id,
                    servico_id=servico["servico_id"],
                    preco_referencia=servico["preco_base"],
                )
            )

        db.session.flush()
        itens = PlanejamentoRepository.listar_itens_da_festa(festa_id)
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


def confirmar_planejamento(festa_id):
    try:
        fornecedores_iniciais = sorted(
            set(
                PlanejamentoRepository.listar_fornecedores_do_planejamento(
                    festa_id
                )
            )
        )

        if not fornecedores_iniciais:
            raise ErroValidacao(
                "A festa precisa possuir um pacote para ser confirmada."
            )

        for fornecedor_id in fornecedores_iniciais:
            PlanejamentoRepository.bloquear_fornecedor(fornecedor_id)

        festa_bloqueada = PlanejamentoRepository.bloquear_festa(festa_id)
        if not festa_bloqueada:
            raise RecursoNaoEncontrado("Festa nao encontrada.")

        if festa_bloqueada["status"] != "RASCUNHO":
            raise ErroConflito("A festa nao esta mais em RASCUNHO.")

        itens = PlanejamentoRepository.bloquear_itens_do_planejamento(
            festa_id
        )
        fornecedores_atuais = sorted(
            {item["fornecedor_id"] for item in itens}
        )
        if fornecedores_atuais != fornecedores_iniciais:
            raise ErroConflito(
                "O pacote mudou durante a confirmacao. Tente novamente."
            )

        itens_invalidos = [
            item
            for item in itens
            if not item["servico_disponivel"]
            or not item["fornecedor_disponivel"]
            or item["capacidade_convidados"]
            < festa_bloqueada["quantidade_convidados"]
        ]
        if itens_invalidos:
            raise ErroConflito(
                "O pacote possui servico indisponivel ou sem capacidade."
            )

        total = sum(
            (item["preco_referencia"] for item in itens),
            Decimal("0.00"),
        )
        if total > festa_bloqueada["orcamento"]:
            raise ErroConflito(
                "O pacote ultrapassa o orcamento e nao pode ser confirmado."
            )

        conflitos = (
            PlanejamentoRepository.buscar_conflitos_para_confirmacao(
                festa_id
            )
        )
        if conflitos:
            raise ErroConflito(
                "A agenda de um ou mais fornecedores nao esta livre."
            )

        festa = Festa.query.filter_by(id=festa_id).first()
        festa.status = "CONFIRMADA"
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "festa_id": festa_id,
        "status": "CONFIRMADA",
        "tipo": "RESERVA_ACADEMICA",
        "mensagem": (
            "Planejamento confirmado. Esta confirmacao nao representa "
            "pagamento ou contrato comercial."
        ),
    }
