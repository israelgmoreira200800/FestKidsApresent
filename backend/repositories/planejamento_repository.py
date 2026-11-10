from sqlalchemy import text

from backend.extensions import db


class PlanejamentoRepository:
    @staticmethod
    def buscar_servicos_elegiveis(categoria, quantidade_convidados):
        sql = text(
            "CALL sp_servicos_elegiveis("
            ":categoria, :quantidade_convidados)"
        )
        parametros = {
            "categoria": categoria,
            "quantidade_convidados": quantidade_convidados,
        }
        resultado = db.session.execute(sql, parametros)
        linhas = resultado.mappings().all()
        resultado.close()

        return [dict(linha) for linha in linhas]

    @staticmethod
    def listar_itens_da_festa(festa_id):
        sql = text("CALL sp_itens_planejamento_por_festa(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linhas = resultado.mappings().all()
        resultado.close()

        return [dict(linha) for linha in linhas]

    @staticmethod
    def buscar_resumo_orcamento(festa_id):
        sql = text("CALL sp_resumo_orcamento(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linha = resultado.mappings().one_or_none()
        resultado.close()

        return dict(linha) if linha else None

    @staticmethod
    def buscar_conflitos_agenda(festa_id):
        sql = text("CALL sp_conflitos_agenda(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linhas = resultado.mappings().all()
        resultado.close()

        return [dict(linha) for linha in linhas]

    @staticmethod
    def listar_fornecedores_do_planejamento(festa_id):
        sql = text("CALL sp_fornecedores_planejamento(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linhas = resultado.mappings().all()
        resultado.close()

        return [linha["fornecedor_id"] for linha in linhas]

    @staticmethod
    def bloquear_fornecedor(fornecedor_id):
        sql = text("CALL sp_bloquear_fornecedor(:fornecedor_id)")
        resultado = db.session.execute(
            sql,
            {"fornecedor_id": fornecedor_id},
        )
        linha = resultado.mappings().one_or_none()
        resultado.close()

        return dict(linha) if linha else None

    @staticmethod
    def bloquear_festa(festa_id):
        sql = text("CALL sp_bloquear_festa(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linha = resultado.mappings().one_or_none()
        resultado.close()

        return dict(linha) if linha else None

    @staticmethod
    def bloquear_itens_do_planejamento(festa_id):
        sql = text("CALL sp_bloquear_itens_planejamento(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linhas = resultado.mappings().all()
        resultado.close()

        return [dict(linha) for linha in linhas]

    @staticmethod
    def buscar_conflitos_para_confirmacao(festa_id):
        sql = text("CALL sp_conflitos_agenda_confirmacao(:festa_id)")
        resultado = db.session.execute(sql, {"festa_id": festa_id})
        linhas = resultado.mappings().all()
        resultado.close()

        return [dict(linha) for linha in linhas]
