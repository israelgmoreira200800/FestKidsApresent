from backend.extensions import db


class PlanejamentoRepository:
    @staticmethod
    def buscar_servicos_elegiveis(categoria, quantidade_convidados):
        consulta = db.text(
            """
            select
                s.id as servico_id,
                s.fornecedor_id,
                s.nome as servico_nome,
                s.categoria,
                s.preco_base,
                f.nome_comercial as fornecedor_nome
            from servicos s
            inner join fornecedores f on f.id = s.fornecedor_id
            where s.categoria = :categoria
              and s.capacidade_convidados >= :quantidade_convidados
              and s.disponivel = true
              and f.disponivel = true
            order by s.preco_base, s.id
            """
        )
        parametros = {
            "categoria": categoria,
            "quantidade_convidados": quantidade_convidados,
        }
        resultado = db.session.execute(consulta, parametros)
        return [dict(linha) for linha in resultado.mappings().all()]

    @staticmethod
    def listar_itens_da_festa(festa_id):
        consulta = db.text(
            """
            select
                pi.id as item_id,
                pi.festa_id,
                pi.servico_id,
                pi.preco_referencia,
                s.nome as servico_nome,
                s.categoria,
                s.fornecedor_id,
                f.nome_comercial as fornecedor_nome
            from planejamento_itens pi
            inner join servicos s on s.id = pi.servico_id
            inner join fornecedores f on f.id = s.fornecedor_id
            where pi.festa_id = :festa_id
            order by s.categoria, pi.id
            """
        )
        resultado = db.session.execute(consulta, {"festa_id": festa_id})
        return [dict(linha) for linha in resultado.mappings().all()]
