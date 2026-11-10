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
