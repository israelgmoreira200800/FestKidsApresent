-- Restaura somente os registros ficticios da demonstracao oficial.
-- Pode ser executado antes de cada ensaio sem apagar outros cadastros.

use festkids;

update fornecedores
set disponivel = true
where email in (
    'sabor.kids@festkids.local',
    'festa.facil@festkids.local',
    'mundo.magico@festkids.local',
    'click.alegria@festkids.local',
    'brincamais@festkids.local',
    'doce.sonho@festkids.local',
    'arco.iris@festkids.local'
);

update servicos as servico
join fornecedores as fornecedor on fornecedor.id = servico.fornecedor_id
set servico.disponivel = true
where fornecedor.email in (
    'sabor.kids@festkids.local',
    'festa.facil@festkids.local',
    'mundo.magico@festkids.local',
    'click.alegria@festkids.local',
    'brincamais@festkids.local',
    'doce.sonho@festkids.local',
    'arco.iris@festkids.local'
);

update festas
set
    data = '2026-12-05',
    quantidade_convidados = 50,
    orcamento = 5000.00,
    status = 'RASCUNHO'
where nome = 'Festa da Lia';

update festas
set
    data = '2026-12-05',
    quantidade_convidados = 40,
    orcamento = 3000.00,
    status = 'CONFIRMADA'
where nome = 'Festa do Theo';

delete from planejamento_itens
where festa_id = (
    select min(id) from festas where nome = 'Festa da Lia'
);

delete from planejamento_itens
where festa_id = (
    select min(id) from festas where nome = 'Festa do Theo'
);

insert into planejamento_itens (
    festa_id,
    servico_id,
    preco_referencia
)
select
    festa.id,
    servico.id,
    servico.preco_base
from festas as festa
join servicos as servico
join fornecedores as fornecedor on fornecedor.id = servico.fornecedor_id
where festa.id = (
    select festa_id
    from (
        select min(id) as festa_id
        from festas
        where nome = 'Festa do Theo'
    ) as festa_demo
)
and fornecedor.email = 'brincamais@festkids.local';
