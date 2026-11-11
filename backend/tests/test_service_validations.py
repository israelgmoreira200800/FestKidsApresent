from decimal import Decimal

import pytest

from backend.errors import ErroValidacao
from backend.services import (
    cliente_service,
    festa_service,
    fornecedor_service,
    planejamento_service,
    servico_service,
)


class ConsultaFake:
    def __init__(self, resultado):
        self.resultado = resultado

    def filter_by(self, **_filtros):
        return self

    def first(self):
        return self.resultado


def substituir_model_query(monkeypatch, modulo, nome_model, resultado):
    model_fake = type("ModelFake", (), {"query": ConsultaFake(resultado)})
    monkeypatch.setattr(modulo, nome_model, model_fake)


def dados_servico_validos():
    return {
        "fornecedor_id": 1,
        "nome": "Buffet completo",
        "descricao": "Atendimento infantil",
        "categoria": "buffet",
        "preco_base": "1250.90",
        "capacidade_convidados": 80,
        "disponivel": True,
    }


def dados_festa_validos():
    return {
        "cliente_id": 1,
        "nome": "Festa da Lia",
        "data": "2027-05-15",
        "local": "Belo Horizonte",
        "quantidade_convidados": 50,
        "orcamento": "5000.90",
        "status": "RASCUNHO",
    }


@pytest.mark.parametrize("dados", [None, [], "cliente"])
def test_cliente_exige_objeto_json(dados):
    with pytest.raises(ErroValidacao, match="formato JSON"):
        cliente_service.validar_dados_cliente(dados)


def test_cliente_normaliza_textos_e_recusa_limites_invalidos():
    assert cliente_service.validar_dados_cliente(
        {
            "nome": "  Ana Demonstração  ",
            "email": "  ANA@EXEMPLO.COM  ",
            "telefone": "  (31) 90000-0000  ",
        }
    ) == ("Ana Demonstração", "ana@exemplo.com", "(31) 90000-0000")

    with pytest.raises(ErroValidacao, match="no maximo 120"):
        cliente_service.validar_dados_cliente(
            {"nome": "A" * 121, "email": "a@b.com", "telefone": "1"}
        )
    with pytest.raises(ErroValidacao, match="telefone e obrigatorio"):
        cliente_service.validar_dados_cliente(
            {"nome": "Ana", "email": "a@b.com", "telefone": " "}
        )
    with pytest.raises(ErroValidacao, match="e-mail valido"):
        cliente_service.validar_dados_cliente(
            {"nome": "Ana", "email": "ana@localhost", "telefone": "1"}
        )


def test_fornecedor_aplica_disponibilidade_padrao_e_valida_email():
    assert fornecedor_service.validar_dados_fornecedor(
        {
            "nome_comercial": "  Sabor Kids  ",
            "email": "  CONTATO@SABOR.COM  ",
            "telefone": "  31900000000  ",
        },
        disponibilidade_padrao=False,
    ) == ("Sabor Kids", "contato@sabor.com", "31900000000", False)

    with pytest.raises(ErroValidacao, match="e-mail valido"):
        fornecedor_service.validar_dados_fornecedor(
            {
                "nome_comercial": "Sabor Kids",
                "email": "invalido@localhost",
                "telefone": "31900000000",
            }
        )


@pytest.mark.parametrize("dados", [None, [], "fornecedor"])
def test_fornecedor_exige_objeto_json(dados):
    with pytest.raises(ErroValidacao, match="formato JSON"):
        fornecedor_service.validar_dados_fornecedor(dados)


def test_fornecedor_recusa_nome_longo_e_disponibilidade_invalida():
    base = {
        "nome_comercial": "Sabor Kids",
        "email": "contato@sabor.com",
        "telefone": "31900000000",
    }
    with pytest.raises(ErroValidacao, match="no maximo 120"):
        fornecedor_service.validar_dados_fornecedor(
            {**base, "nome_comercial": "F" * 121}
        )
    with pytest.raises(ErroValidacao, match="verdadeiro ou falso"):
        fornecedor_service.validar_dados_fornecedor(
            {**base, "disponivel": 1}
        )


@pytest.mark.parametrize("valor", [None, "texto", "NaN", "Infinity", -1])
def test_preco_recusa_valores_invalidos_ou_nao_finitos(valor):
    with pytest.raises(ErroValidacao):
        servico_service.validar_preco(valor)


def test_preco_aceita_zero_e_recusa_mais_de_duas_casas():
    assert servico_service.validar_preco("0") == Decimal("0.00")
    with pytest.raises(ErroValidacao, match="duas casas"):
        servico_service.validar_preco("10.999")


@pytest.mark.parametrize("dados", [None, [], "servico"])
def test_servico_exige_objeto_json(dados):
    with pytest.raises(ErroValidacao, match="formato JSON"):
        servico_service.validar_dados_servico(dados)


@pytest.mark.parametrize(
    ("campo", "valor", "mensagem"),
    [
        ("fornecedor_id", True, "fornecedor_id valido"),
        ("fornecedor_id", "1", "fornecedor_id valido"),
        ("categoria", "MAGICA", "categoria valida"),
        ("capacidade_convidados", True, "capacidade_convidados valida"),
        ("capacidade_convidados", 0, "maior que zero"),
        ("disponivel", "sim", "verdadeiro ou falso"),
        ("descricao", 123, "descricao deve ser um texto"),
    ],
)
def test_servico_valida_tipos_e_regras(monkeypatch, campo, valor, mensagem):
    substituir_model_query(monkeypatch, servico_service, "Fornecedor", object())
    dados = dados_servico_validos()
    dados[campo] = valor
    with pytest.raises(ErroValidacao, match=mensagem):
        servico_service.validar_dados_servico(dados)


def test_servico_recusa_fornecedor_inexistente_e_limpa_descricao(monkeypatch):
    substituir_model_query(monkeypatch, servico_service, "Fornecedor", None)
    with pytest.raises(ErroValidacao, match="fornecedor informado nao existe"):
        servico_service.validar_dados_servico(dados_servico_validos())

    substituir_model_query(monkeypatch, servico_service, "Fornecedor", object())
    dados = dados_servico_validos()
    dados["descricao"] = "   "
    valores = servico_service.validar_dados_servico(dados)
    assert valores[2] is None
    assert valores[3] == "BUFFET"


@pytest.mark.parametrize("valor", [None, 20270515])
def test_data_exige_texto_iso(valor):
    with pytest.raises(ErroValidacao, match="formato AAAA-MM-DD"):
        festa_service.validar_data(valor)


def test_data_recusa_dia_inexistente():
    with pytest.raises(ErroValidacao, match="data valida"):
        festa_service.validar_data("2027-02-30")


@pytest.mark.parametrize("valor", [None, "texto", "NaN", "Infinity", 0, -1])
def test_orcamento_recusa_valores_invalidos(valor):
    with pytest.raises(ErroValidacao):
        festa_service.validar_orcamento(valor)


def test_orcamento_recusa_mais_de_duas_casas():
    with pytest.raises(ErroValidacao, match="duas casas"):
        festa_service.validar_orcamento("5000.999")


@pytest.mark.parametrize(
    ("campo", "valor", "mensagem"),
    [
        ("cliente_id", True, "cliente_id valido"),
        ("cliente_id", "1", "cliente_id valido"),
        ("quantidade_convidados", True, "quantidade_convidados valida"),
        ("quantidade_convidados", 0, "maior que zero"),
        ("status", "CONFIRMADA", "nao pode ser alterado"),
    ],
)
def test_festa_valida_tipos_e_status(monkeypatch, campo, valor, mensagem):
    substituir_model_query(monkeypatch, festa_service, "Cliente", object())
    dados = dados_festa_validos()
    dados[campo] = valor
    with pytest.raises(ErroValidacao, match=mensagem):
        festa_service.validar_dados_festa(dados)


def test_festa_recusa_cliente_inexistente_e_texto_longo(monkeypatch):
    substituir_model_query(monkeypatch, festa_service, "Cliente", None)
    with pytest.raises(ErroValidacao, match="cliente informado nao existe"):
        festa_service.validar_dados_festa(dados_festa_validos())

    substituir_model_query(monkeypatch, festa_service, "Cliente", object())
    dados = dados_festa_validos()
    dados["local"] = "L" * 181
    with pytest.raises(ErroValidacao, match="no maximo 180"):
        festa_service.validar_dados_festa(dados)


@pytest.mark.parametrize("dados", [None, [], "festa"])
def test_festa_exige_objeto_json(dados):
    with pytest.raises(ErroValidacao, match="formato JSON"):
        festa_service.validar_dados_festa(dados)


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        (None, "formato JSON"),
        ({"festa_id": True, "categorias": ["BUFFET"]}, "festa_id valido"),
        ({"festa_id": "1", "categorias": ["BUFFET"]}, "festa_id valido"),
        ({"festa_id": 1, "categorias": []}, "ao menos uma categoria"),
        ({"festa_id": 1, "categorias": "BUFFET"}, "ao menos uma categoria"),
        ({"festa_id": 1, "categorias": [1]}, "apenas categorias validas"),
        ({"festa_id": 1, "categorias": ["MAGICA"]}, "categoria MAGICA e invalida"),
        ({"festa_id": 1, "categorias": ["BUFFET", " buffet "]}, "Nao repita"),
    ],
)
def test_pedido_sugestao_valida_todos_os_formatos(dados, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        planejamento_service.validar_pedido_sugestao(dados)


def test_pedido_sugestao_normaliza_categorias():
    assert planejamento_service.validar_pedido_sugestao(
        {"festa_id": 7, "categorias": [" buffet ", "decoracao"]}
    ) == (7, ["BUFFET", "DECORACAO"])
