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
