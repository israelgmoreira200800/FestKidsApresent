# FestKids

Plataforma acadêmica para planejamento de festas infantis, reconstruída do zero para demonstrar arquitetura em camadas, regras de negócio, persistência e integração entre frontend e API.

## Estado atual

O projeto já possui a base executável da API Flask, tratamento de erros, proteções das requisições e o primeiro Model ORM: `Cliente`.

As decisões e tarefas da reconstrução estão registradas em:

- `openspec/changes/reconstruir-festkids-do-zero/proposal.md`
- `openspec/changes/reconstruir-festkids-do-zero/design.md`
- `openspec/changes/reconstruir-festkids-do-zero/tasks.md`

Os requisitos do produto estão explicados em `docs/requisitos.md`.
As entidades e seus relacionamentos estão explicados em `docs/modelo-dominio.md`.
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

`backend/models/cliente.py` mapeia a classe `Cliente` para a tabela `clientes`. O método `para_dict()` prepara seus atributos para respostas JSON, mantendo a persistência simples sob responsabilidade do SQLAlchemy.

