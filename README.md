# FestKids

Plataforma acadêmica para planejamento de festas infantis, reconstruída do zero para demonstrar arquitetura em camadas, regras de negócio, persistência e integração entre frontend e API.

## Estado atual

O projeto já possui a base executável da API Flask, tratamento de erros, proteções das requisições, os quatro cadastros com ORM e suas telas de gestão.

As decisões e tarefas da reconstrução estão registradas em:

- `openspec/changes/reconstruir-festkids-do-zero/proposal.md`
- `openspec/changes/reconstruir-festkids-do-zero/design.md`
- `openspec/changes/reconstruir-festkids-do-zero/tasks.md`

Os requisitos do produto estão explicados em `docs/requisitos.md`.
As entidades e seus relacionamentos estão explicados em `docs/modelo-dominio.md`.
A matriz das vinte operações e a separação das camadas estão explicadas em `docs/matriz-crud.md`.
O DDL inicial do MySQL está em `backend/database/create_database.sql`.

O script cria o banco `festkids` e as tabelas `clientes`, `fornecedores`, `servicos`, `festas` e `planejamento_itens`. Ele foi executado e verificado em MySQL Community Server 8.4.9. A configuração segura do usuário da aplicação será adicionada em uma etapa própria.

Os dados fictícios usados na demonstração estão em `backend/database/seed_demo.sql`. O arquivo pode ser executado novamente sem duplicar os registros identificados.

Os testes automatizados usam o banco separado `festkids_test`, criado por `backend/database/create_test_database.sql`. A proteção em `backend/tests/database_guard.py` recusa a execução quando outro nome de banco é informado.

## Arquitetura planejada

```text
Frontend HTML, CSS e JavaScript
            ↓ HTTP/JSON
Routes → Controllers → Services → Models/Repositories → MySQL
```

## Mapa inicial das pastas

```text
backend/
  controllers/   recebe e devolve dados HTTP
  database/      scripts de criação e dados de demonstração
  models/        entidades e operações simples com ORM
  repositories/  consultas e transações especializadas
  routes/        URLs e métodos da API
  services/      casos de uso e regras da aplicação
  tests/         testes do backend e da persistência
frontend/
  css/           estilos da interface
  js/            comportamento e comunicação com a API
  tests/         testes das funções do frontend
docs/            arquitetura, diagramas, fluxos e apresentação
openspec/        proposta, especificações e tarefas rastreáveis
```

## Escopo acadêmico

O sistema terá CRUD de clientes, fornecedores, serviços e festas, além de quatro funcionalidades de negócio:

1. Sugerir pacote de serviços.
2. Analisar orçamento.
3. Verificar agenda dos fornecedores.
4. Confirmar planejamento.

Autenticação, pagamentos, propostas comerciais, avaliações, chat e inteligência artificial de recomendação não fazem parte desta versão.

## Segurança

Nunca coloque senhas, chaves ou conexões reais no Git. Copie `backend/.env.example` para um arquivo local ignorado somente quando a configuração do backend for implementada.

## Dependências do backend

O projeto requer Python 3.11 ou superior. Para criar um ambiente isolado e instalar as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

O ambiente `.venv` é local e está ignorado pelo Git.

## Executar o backend

Copie `backend/.env.example` para `backend/.env.local` e preencha `DATABASE_URL` com a conexão local do MySQL. Depois, execute:

```powershell
.\.venv\Scripts\python.exe -m backend.run
```

A rota `GET http://127.0.0.1:5000/api/saude` confirma que a API está funcionando.

## Formato dos erros da API

Erros de validação, recurso não encontrado, conflito e falha interna usam o mesmo formato JSON:

```json
{
  "erro": {
    "codigo": "validacao",
    "mensagem": "Mensagem compreensível"
  }
}
```

Falhas internas retornam uma mensagem genérica e não expõem traceback ou detalhes técnicos.

## Proteções das requisições

`FRONTEND_ORIGINS` contém os endereços locais autorizados a consumir `/api/*` pelo navegador. `MAX_CONTENT_LENGTH` limita o corpo de cada requisição; o valor padrão é `1000000` bytes, adequado para os dados JSON desta versão sem uploads.

## Primeiro Model ORM

`backend/models/cliente.py` mapeia a classe `Cliente` para a tabela `clientes` usando a sintaxe clássica `db.Column`. O método `para_dict()` prepara seus atributos para respostas JSON, mantendo a persistência simples sob responsabilidade do SQLAlchemy.

## Cadastrar cliente

O endpoint `POST /api/clientes` recebe JSON com `nome`, `email` e `telefone`. A requisição percorre Route, Controller, Service e Model antes de chegar ao MySQL. Um cadastro válido retorna o cliente com código HTTP `201`; dados inválidos retornam `400` e e-mail repetido retorna `409`.

```json
{
  "nome": "Ana Demonstração",
  "email": "ana.demo@festkids.local",
  "telefone": "(31) 90000-0001"
}
```

## Executar o frontend

Com a API em execução, abra outro terminal e inicie o servidor estático:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

Depois, acesse `http://127.0.0.1:5500`. A navegação leva às quatro telas:

- `frontend/index.html`: clientes;
- `frontend/fornecedores.html`: fornecedores;
- `frontend/servicos.html`: serviços;
- `frontend/festas.html`: festas.

Cada página carrega `frontend/js/api.js`, que concentra a requisição HTTP e a criação segura dos cartões, e seu próprio arquivo JavaScript dentro de `frontend/js/`. O arquivo `frontend/css/styles.css` contém o visual compartilhado e as adaptações para telas menores.

Nas quatro telas, o usuário pode listar, cadastrar, editar e excluir registros. A interface informa quando está carregando, quando a lista está vazia, quando uma operação termina com sucesso e quando a API devolve um erro ou não está disponível.

## Endpoints de clientes

| Método | Endpoint | Operação |
|---|---|---|
| `POST` | `/api/clientes` | Cadastrar cliente |
| `GET` | `/api/clientes` | Listar clientes |
| `GET` | `/api/clientes/{id}` | Consultar cliente |
| `PUT` | `/api/clientes/{id}` | Atualizar cliente |
| `DELETE` | `/api/clientes/{id}` | Excluir cliente |

A exclusão retorna conflito `409` quando o cliente possui uma festa vinculada.

## Endpoints de fornecedores

| Método | Endpoint | Operação |
|---|---|---|
| `POST` | `/api/fornecedores` | Cadastrar fornecedor |
| `GET` | `/api/fornecedores` | Listar fornecedores |
| `GET` | `/api/fornecedores/{id}` | Consultar fornecedor |
| `PUT` | `/api/fornecedores/{id}` | Atualizar fornecedor |
| `DELETE` | `/api/fornecedores/{id}` | Excluir fornecedor |

O campo booleano `disponivel` controla se o fornecedor aceita novas seleções em geral. A exclusão retorna conflito `409` quando há serviço vinculado.

## Endpoints de serviços

| Método | Endpoint | Operação |
|---|---|---|
| `POST` | `/api/servicos` | Cadastrar serviço |
| `GET` | `/api/servicos` | Listar serviços |
| `GET` | `/api/servicos/{id}` | Consultar serviço |
| `PUT` | `/api/servicos/{id}` | Atualizar serviço |
| `DELETE` | `/api/servicos/{id}` | Excluir serviço |

Cada serviço exige um `fornecedor_id` existente, preço decimal com até duas casas e capacidade maior que zero. As categorias aceitas são `BUFFET`, `DECORACAO`, `FOTOGRAFIA`, `RECREACAO`, `BOLO_E_DOCES` e `ESPACO`.

## Endpoints de festas

| Método | Endpoint | Operação |
|---|---|---|
| `POST` | `/api/festas` | Cadastrar festa |
| `GET` | `/api/festas` | Listar festas |
| `GET` | `/api/festas/{id}` | Consultar festa |
| `PUT` | `/api/festas/{id}` | Atualizar festa |
| `DELETE` | `/api/festas/{id}` | Excluir festa |

Cada festa exige um `cliente_id` existente, data no formato `AAAA-MM-DD`, quantidade de convidados maior que zero e orçamento decimal maior que zero. Toda festa começa em `RASCUNHO`; o CRUD comum não pode mudar o status para `CONFIRMADA`.

## Item de planejamento

`backend/models/planejamento_item.py` mapeia a tabela `planejamento_itens`. Cada item liga uma Festa a um Serviço e copia o preço-base para `preco_referencia` no momento da seleção.

Essa cópia preserva o histórico: alterar depois o preço-base do Serviço não modifica o valor que já foi usado no planejamento. A combinação de `festa_id` e `servico_id` é única, impedindo que o mesmo Serviço apareça duas vezes na mesma Festa.

