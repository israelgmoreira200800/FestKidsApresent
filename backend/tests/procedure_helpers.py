from backend.extensions import db


def instalar_procedures_planejamento():
    db.session.execute(db.text("drop procedure if exists sp_servicos_elegiveis"))
    db.session.execute(
        db.text(
            """
            create procedure sp_servicos_elegiveis(
                in p_categoria varchar(40),
                in p_quantidade_convidados int
            )
            begin
                select
                    s.id as servico_id,
                    s.fornecedor_id,
                    s.nome as servico_nome,
                    s.categoria,
                    s.preco_base,
                    f.nome_comercial as fornecedor_nome
                from servicos s
                inner join fornecedores f on f.id = s.fornecedor_id
                where s.categoria = p_categoria
                  and s.capacidade_convidados >= p_quantidade_convidados
                  and s.disponivel = true
                  and f.disponivel = true
                order by s.preco_base, s.id;
            end
            """
        )
    )
    db.session.execute(
        db.text(
            "drop procedure if exists sp_itens_planejamento_por_festa"
        )
    )
    db.session.execute(
        db.text(
            """
            create procedure sp_itens_planejamento_por_festa(
                in p_festa_id int
            )
            begin
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
                where pi.festa_id = p_festa_id
                order by s.categoria, pi.id;
            end
            """
        )
    )
    db.session.commit()
