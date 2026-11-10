-- Dados ficticios para demonstracao do FestKids.
-- O where not exists evita duplicacoes ao executar este arquivo novamente.

use festkids;

-- CLIENTES

insert into clientes (nome, email, telefone)
select 'Ana Demonstração', 'ana.demo@festkids.local', '(31) 90000-0001'
where not exists (
    select id from clientes
    where email = 'ana.demo@festkids.local'
);

insert into clientes (nome, email, telefone)
select 'Bruno Demonstração', 'bruno.demo@festkids.local', '(31) 90000-0002'
where not exists (
    select id from clientes
    where email = 'bruno.demo@festkids.local'
);

-- FORNECEDORES

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'Sabor Kids Buffet', 'sabor.kids@festkids.local', '(31) 91000-0001', true
where not exists (
    select id from fornecedores
    where email = 'sabor.kids@festkids.local'
);

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'Festa Fácil Buffet', 'festa.facil@festkids.local', '(31) 91000-0002', true
where not exists (
    select id from fornecedores
    where email = 'festa.facil@festkids.local'
);

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'Mundo Mágico Decorações', 'mundo.magico@festkids.local', '(31) 91000-0003', true
where not exists (
    select id from fornecedores
    where email = 'mundo.magico@festkids.local'
);

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'Click Alegria Fotografia', 'click.alegria@festkids.local', '(31) 91000-0004', true
where not exists (
    select id from fornecedores
    where email = 'click.alegria@festkids.local'
);

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'BrincaMais Recreação', 'brincamais@festkids.local', '(31) 91000-0005', true
where not exists (
    select id from fornecedores
    where email = 'brincamais@festkids.local'
);

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'Doce Sonho Confeitaria', 'doce.sonho@festkids.local', '(31) 91000-0006', true
where not exists (
    select id from fornecedores
    where email = 'doce.sonho@festkids.local'
);

insert into fornecedores (nome_comercial, email, telefone, disponivel)
select 'Espaço Arco-Íris', 'arco.iris@festkids.local', '(31) 91000-0007', true
where not exists (
    select id from fornecedores
    where email = 'arco.iris@festkids.local'
);

-- SERVICOS

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Buffet Completo',
    'Buffet infantil para até 60 convidados',
    'BUFFET',
    1200.00,
    60,
    true
from fornecedores
where email = 'sabor.kids@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Buffet Completo'
);

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Buffet Econômico',
    'Buffet infantil para até 50 convidados',
    'BUFFET',
    900.00,
    50,
    true
from fornecedores
where email = 'festa.facil@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Buffet Econômico'
);

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Decoração Colorida',
    'Decoração infantil com tema escolhido',
    'DECORACAO',
    650.00,
    100,
    true
from fornecedores
where email = 'mundo.magico@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Decoração Colorida'
);

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Cobertura Fotográfica',
    'Fotografia durante a festa',
    'FOTOGRAFIA',
    500.00,
    100,
    true
from fornecedores
where email = 'click.alegria@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Cobertura Fotográfica'
);

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Recreação Infantil',
    'Equipe de recreadores para brincadeiras',
    'RECREACAO',
    450.00,
    60,
    true
from fornecedores
where email = 'brincamais@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Recreação Infantil'
);

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Bolo e Doces',
    'Bolo decorado e doces para até 50 convidados',
    'BOLO_E_DOCES',
    350.00,
    50,
    true
from fornecedores
where email = 'doce.sonho@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Bolo e Doces'
);

insert into servicos (
    fornecedor_id,
    nome,
    descricao,
    categoria,
    preco_base,
    capacidade_convidados,
    disponivel
)
select
    id,
    'Aluguel do Espaço',
    'Espaço infantil para até 80 convidados',
    'ESPACO',
    1400.00,
    80,
    true
from fornecedores
where email = 'arco.iris@festkids.local'
and not exists (
    select id from servicos
    where nome = 'Aluguel do Espaço'
);

-- FESTAS

insert into festas (
    cliente_id,
    nome,
    data,
    local,
    quantidade_convidados,
    orcamento,
    status
)
select
    id,
    'Festa da Lia',
    '2026-12-05',
    'Belo Horizonte',
    50,
    5000.00,
    'RASCUNHO'
from clientes
where email = 'ana.demo@festkids.local'
and not exists (
    select id from festas
    where nome = 'Festa da Lia'
    and data = '2026-12-05'
);

insert into festas (
    cliente_id,
    nome,
    data,
    local,
    quantidade_convidados,
    orcamento,
    status
)
select
    id,
    'Festa do Theo',
    '2026-12-05',
    'Contagem',
    40,
    3000.00,
    'CONFIRMADA'
from clientes
where email = 'bruno.demo@festkids.local'
and not exists (
    select id from festas
    where nome = 'Festa do Theo'
    and data = '2026-12-05'
);

-- A festa confirmada usa o fornecedor BrincaMais.
-- Isso cria um conflito de agenda proposital para a demonstracao.
insert into planejamento_itens (
    festa_id,
    servico_id,
    preco_referencia
)
select
    f.id,
    s.id,
    s.preco_base
from festas as f
join servicos as s on s.nome = 'Recreação Infantil'
where f.nome = 'Festa do Theo'
and f.data = '2026-12-05'
and not exists (
    select id from planejamento_itens
    where festa_id = f.id
    and servico_id = s.id
);
