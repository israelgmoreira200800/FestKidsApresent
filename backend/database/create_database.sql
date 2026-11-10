-- Banco de dados do FestKids.
-- Este arquivo usa os mesmos tipos de comandos estudados nas aulas.

create database if not exists festkids;

use festkids;

-- Um cliente pode possuir varias festas.
create table clientes (
    id int auto_increment primary key,
    nome varchar(120) not null,
    email varchar(255) not null unique,
    telefone varchar(20) not null,
    criado_em datetime default current_timestamp
) engine = InnoDB;

-- Um fornecedor pode oferecer varios servicos.
create table fornecedores (
    id int auto_increment primary key,
    nome_comercial varchar(120) not null,
    email varchar(255) not null unique,
    telefone varchar(20) not null,
    disponivel boolean default true,
    criado_em datetime default current_timestamp
) engine = InnoDB;

-- fornecedor_id liga cada servico ao seu fornecedor.
create table servicos (
    id int auto_increment primary key,
    fornecedor_id int not null,
    nome varchar(120) not null,
    descricao text,
    categoria varchar(40) not null,
    preco_base decimal(12,2) not null,
    capacidade_convidados int not null,
    disponivel boolean default true,
    criado_em datetime default current_timestamp,

    foreign key (fornecedor_id) references fornecedores(id)
) engine = InnoDB;

-- cliente_id liga cada festa ao cliente responsavel.
create table festas (
    id int auto_increment primary key,
    cliente_id int not null,
    nome varchar(120) not null,
    data date not null,
    local varchar(180) not null,
    quantidade_convidados int not null,
    orcamento decimal(12,2) not null,
    status varchar(20) default 'RASCUNHO',
    criado_em datetime default current_timestamp,

    foreign key (cliente_id) references clientes(id)
) engine = InnoDB;

-- Esta tabela liga festas e servicos.
-- O preco de referencia guarda o valor usado no planejamento.
create table planejamento_itens (
    id int auto_increment primary key,
    festa_id int not null,
    servico_id int not null,
    preco_referencia decimal(12,2) not null,
    criado_em datetime default current_timestamp,

    unique (festa_id, servico_id),
    foreign key (festa_id) references festas(id),
    foreign key (servico_id) references servicos(id)
) engine = InnoDB;

-- O Repository chama esta procedure para buscar opcoes do planejamento.
drop procedure if exists sp_servicos_elegiveis;

delimiter //
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
end //
delimiter ;

-- O Repository chama esta procedure para recuperar o pacote de uma festa.
drop procedure if exists sp_itens_planejamento_por_festa;

delimiter //
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
end //
delimiter ;

-- A procedure soma os precos preservados no pacote da festa.
drop procedure if exists sp_resumo_orcamento;

delimiter //
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
end //
delimiter ;

-- Um fornecedor fica reservado pelo dia inteiro em uma festa confirmada.
drop procedure if exists sp_conflitos_agenda;

delimiter //
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
end //
delimiter ;
