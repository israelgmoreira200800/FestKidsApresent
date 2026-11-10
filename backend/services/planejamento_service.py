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
