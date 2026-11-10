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
    db.session.execute(db.text("drop procedure if exists sp_resumo_orcamento"))
    db.session.execute(
        db.text(
            """
            create procedure sp_resumo_orcamento(
                in p_festa_id int
            )
            begin
                select
                    f.id as festa_id,
                    f.orcamento,
                    f.quantidade_convidados,
                    coalesce(sum(pi.preco_referencia), 0.00) as total_itens
                from festas f
                left join planejamento_itens pi on pi.festa_id = f.id
                where f.id = p_festa_id
                group by f.id, f.orcamento, f.quantidade_convidados;
            end
            """
        )
    )
    db.session.execute(db.text("drop procedure if exists sp_conflitos_agenda"))
    db.session.execute(
        db.text(
            """
            create procedure sp_conflitos_agenda(
                in p_festa_id int
            )
            begin
                select distinct
                    fornecedor.id as fornecedor_id,
                    fornecedor.nome_comercial as fornecedor_nome,
                    festa_confirmada.id as festa_conflitante_id,
                    festa_confirmada.nome as festa_conflitante_nome,
                    festa_confirmada.data
                from festas festa_alvo
                inner join planejamento_itens item_alvo
                    on item_alvo.festa_id = festa_alvo.id
                inner join servicos servico_alvo
                    on servico_alvo.id = item_alvo.servico_id
                inner join fornecedores fornecedor
                    on fornecedor.id = servico_alvo.fornecedor_id
                inner join servicos servico_confirmado
                    on servico_confirmado.fornecedor_id = fornecedor.id
                inner join planejamento_itens item_confirmado
                    on item_confirmado.servico_id = servico_confirmado.id
                inner join festas festa_confirmada
                    on festa_confirmada.id = item_confirmado.festa_id
                where festa_alvo.id = p_festa_id
                  and festa_confirmada.id <> festa_alvo.id
                  and festa_confirmada.data = festa_alvo.data
                  and festa_confirmada.status = 'CONFIRMADA'
                order by fornecedor.id, festa_confirmada.id;
            end
            """
        )
    )
    db.session.commit()
