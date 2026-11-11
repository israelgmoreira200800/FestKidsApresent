# FestKids

Plataforma acadêmica para planejamento de festas infantis, reconstruída do zero para demonstrar arquitetura em camadas, regras de negócio, persistência e integração entre frontend e API.

## Estado atual

O projeto possui API Flask, tratamento padronizado de erros, quatro cadastros completos com ORM, procedures MySQL para consultas especializadas e uma jornada visual de planejamento em cinco etapas.

As decisões e tarefas da reconstrução estão registradas em:

- `openspec/changes/reconstruir-festkids-do-zero/proposal.md`
- `openspec/changes/reconstruir-festkids-do-zero/design.md`
- `openspec/changes/reconstruir-festkids-do-zero/tasks.md`

Os requisitos do produto estão explicados em `docs/requisitos.md`.
As entidades e seus relacionamentos estão explicados em `docs/modelo-dominio.md`.
A arquitetura implementada e os fluxos estão explicados em `docs/arquitetura.md`.
A demonstração cronometrada está em `docs/roteiro-demonstracao.md`.
A matriz das vinte operações e a separação das camadas estão explicadas em `docs/matriz-crud.md`.
O DDL inicial do MySQL está em `backend/database/create_database.sql`.

O script cria o banco `festkids` e as tabelas `clientes`, `fornecedores`, `servicos`, `festas` e `planejamento_itens`. Ele foi executado e verificado em MySQL Community Server 8.4.9.

Os dados fictícios usados na demonstração estão em `backend/database/seed_demo.sql`. O arquivo pode ser executado novamente sem duplicar os registros identificados.

Os testes automatizados usam o banco separado `festkids_test`, criado por `backend/database/create_test_database.sql`. A proteção em `backend/tests/database_guard.py` recusa a execução quando outro nome de banco é informado.

## Arquitetura

```text
Frontend HTML, CSS e JavaScript
            ↓ HTTP/JSON
Routes → Controllers → Services → Models/Repositories → MySQL
```

## Mapa das pastas

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

O sistema possui CRUD de clientes, fornecedores, serviços e festas, além de quatro funcionalidades de negócio:

1. Sugerir pacote de serviços.
2. Analisar orçamento.
3. Verificar agenda dos fornecedores.
4. Confirmar planejamento.

Autenticação, pagamentos, propostas comerciais, avaliações, chat e inteligência artificial de recomendação não fazem parte desta versão.

## Pré-requisitos

- Python 3.11 ou superior;
- MySQL Community Server 8.4;
- Git;
- navegador moderno;
- PowerShell, nos comandos deste guia.

## Segurança

Nunca coloque senhas, chaves ou conexões reais no Git. O arquivo `backend/.env.local` é local e ignorado; apenas `backend/.env.example`, sem credenciais, pode ser versionado.

## Dependências do backend

O projeto requer Python 3.11 ou superior. Para criar um ambiente isolado e instalar as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

O ambiente `.venv` é local e está ignorado pelo Git.

## Criar e carregar o banco MySQL

No PowerShell, entre na pasta raiz do projeto. Se o comando `mysql` estiver disponível no `PATH`, execute:

```powershell
Get-Content backend\database\create_database.sql -Raw | mysql -u root -p
Get-Content backend\database\seed_demo.sql -Raw | mysql -u root -p festkids
```

O MySQL solicitará a senha do usuário `root`. Se o comando não for reconhecido, use o caminho completo da instalação:

```powershell
$mysql = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
Get-Content backend\database\create_database.sql -Raw | & $mysql -u root -p
Get-Content backend\database\seed_demo.sql -Raw | & $mysql -u root -p festkids
```

`source` é um comando do console interativo do MySQL e não funciona diretamente no PowerShell. Por isso, este guia usa `Get-Content` e o operador de pipeline.

## Executar o backend

Copie `backend/.env.example` para `backend/.env.local`:

```powershell
Copy-Item backend\.env.example backend\.env.local
```

Preencha `DATABASE_URL` no arquivo local. Exemplo com senha:

```dotenv
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@127.0.0.1:3306/festkids
```

Se o usuário local realmente não possuir senha, a parte após `root:` fica vazia. Nunca copie uma senha real para o README ou para um arquivo versionado.

Depois, execute a partir da raiz:

```powershell
.\.venv\Scripts\python.exe -m backend.run
```

A rota `GET http://127.0.0.1:5000/api/saude` confirma que a API está funcionando.

Mantenha esse terminal aberto durante o uso do frontend.

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

Depois, acesse `http://127.0.0.1:5500`. Backend e frontend rodam simultaneamente em terminais diferentes. A navegação leva às cinco telas:

- `frontend/index.html`: entrada das áreas do sistema;
- `frontend/clientes.html`: clientes;
- `frontend/fornecedores.html`: fornecedores;
- `frontend/servicos.html`: serviços;
- `frontend/festas.html`: festas.
- `frontend/planejamento.html`: sugestão, orçamento, agenda e confirmação.

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

## Repository de planejamento

`backend/repositories/planejamento_repository.py` concentra chamadas às stored procedures que combinam itens, serviços e fornecedores. Seus primeiros helpers chamam `sp_servicos_elegiveis` e `sp_itens_planejamento_por_festa`.

As consultas ficam nas procedures criadas pelos scripts do banco. O Repository contém somente `CALL`, parâmetros nomeados e conversão do resultado, seguindo o exemplo usado em aula. Ele usa `db.session.execute` e não executa `commit`; por isso, participa da mesma transação controlada pelo Service e permite desfazer toda a operação com `rollback`.

## Sugestão de pacote

`POST /api/planejamentos/sugestao` recebe o identificador da Festa e as categorias desejadas:

```json
{
  "festa_id": 1,
  "categorias": ["BUFFET", "DECORACAO"]
}
```

Para cada categoria, a procedure considera apenas Serviço e Fornecedor disponíveis com capacidade suficiente. A ordenação usa menor preço e depois menor ID, tornando a escolha previsível. O Service preserva o preço escolhido no Item de Planejamento e substitui o pacote somente quando todas as categorias possuem candidato.

Se alguma categoria não possuir candidato, a resposta usa `completo: false`, informa `categorias_sem_candidato` e mantém o pacote anterior sem alterações.

## Análise de orçamento

`GET /api/planejamentos/{festa_id}/orcamento` analisa o pacote atualmente salvo. A procedure `sp_resumo_orcamento` soma os preços preservados nos itens e devolve os dados básicos da Festa; o Service calcula total, saldo, percentual utilizado, custo por convidado e excedente.

A resposta usa `viavel: true` e `DENTRO_DO_ORCAMENTO` quando o total não ultrapassa o limite. Quando ultrapassa, usa `viavel: false`, `ACIMA_DO_ORCAMENTO` e apresenta o excedente, sem sugerir que o pacote foi aprovado.

## Verificação de agenda

`GET /api/planejamentos/{festa_id}/agenda` verifica os fornecedores do pacote considerando reserva pelo dia inteiro. A procedure `sp_conflitos_agenda` procura o mesmo fornecedor em outra Festa `CONFIRMADA` na mesma data.

A resposta usa `disponivel: true` quando não há conflito. Quando existe conflito, usa `disponivel: false` e identifica fornecedor, Festa e data conflitante. Festas em `RASCUNHO` e festas em outras datas não reservam o fornecedor. Uma Festa sem pacote não pode apresentar uma falsa confirmação de agenda livre.

## Confirmação transacional

`POST /api/planejamentos/{festa_id}/confirmacao` revalida o planejamento antes de mudar a Festa para `CONFIRMADA`. A operação bloqueia fornecedores em ordem crescente de ID e depois bloqueia Festa e itens, reduzindo disputas e evitando dupla reserva do mesmo fornecedor no mesmo dia.

Na mesma transação, o Service verifica se a Festa continua em `RASCUNHO`, se o pacote não mudou, se serviços e fornecedores continuam disponíveis, se a capacidade atende aos convidados, se o orçamento é suficiente e se a agenda permanece livre. Somente depois executa `commit`; qualquer falha executa `rollback`.

A resposta identifica o resultado como `RESERVA_ACADEMICA` e informa que a confirmação não representa pagamento ou contrato comercial.

## Jornada visual do planejamento

`frontend/planejamento.html` apresenta as cinco etapas da jornada: Festa, Sugestão, Orçamento, Agenda e Confirmação. O link “Planejamento” também está disponível no menu das quatro telas de cadastro.

Cada etapa usa um link acessível por teclado, possui um painel identificado e atualiza `aria-current="step"` para indicar a posição atual. `frontend/js/planejamento.js` alterna os painéis e mantém a etapa no endereço por meio do fragmento `#`. Em tela estreita, a faixa das etapas possui rolagem própria para preservar a largura da página.

## Resumo dos endpoints

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/api/saude` | Verificar a API |
| `POST` | `/api/planejamentos/sugestao` | Sugerir pacote |
| `GET` | `/api/planejamentos/{festa_id}/orcamento` | Analisar orçamento |
| `GET` | `/api/planejamentos/{festa_id}/agenda` | Verificar conflitos |
| `POST` | `/api/planejamentos/{festa_id}/confirmacao` | Confirmar reserva acadêmica |

As tabelas anteriores deste README listam também as vinte operações cadastrais.

## Executar os testes

Crie primeiro o schema exclusivo de testes:

```powershell
$mysql = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
Get-Content backend\database\create_test_database.sql -Raw | & $mysql -u root -p
```

Os testes esperam o MySQL local na porta `3308`, conforme o ambiente portátil usado no desenvolvimento. Se sua instalação estiver na porta padrão `3306`, ajuste as URLs de teste antes da execução ou inicie uma instância de testes na porta prevista. Nunca aponte a suíte para o banco `festkids`: `backend/tests/database_guard.py` aceita somente `festkids_test`.

Execute a suíte a partir da raiz:

```powershell
.\.venv\Scripts\python.exe -m pytest backend\tests -q
```

Resultado verificado nesta versão: `101 passed`.

Valide também a mudança OpenSpec:

```powershell
openspec validate reconstruir-festkids-do-zero --type change --strict --no-interactive
```

## Solução de problemas

- `Can't connect to MySQL server`: confirme no aplicativo Serviços do Windows se o serviço MySQL está iniciado e confira host e porta.
- `Access denied for user`: a senha ou o usuário de `DATABASE_URL` não corresponde ao MySQL local.
- `source não é reconhecido`: use os comandos PowerShell com `Get-Content` mostrados acima.
- Frontend mostra erro interno: confira primeiro o terminal do backend e se o schema `festkids` foi criado.
- A porta `5000` já está ocupada: encerre a cópia antiga do backend antes de iniciar outra; várias instâncias podem responder versões diferentes da API.
- A página `http://127.0.0.1:5000/` devolve não encontrado: isso é esperado; a API começa em `/api`, enquanto o frontend usa a porta `5500`.

## Limitações acadêmicas

- Não há autenticação nem perfis de usuário.
- Não existe pagamento, contrato, contratação comercial ou envio de proposta.
- A confirmação representa somente uma reserva acadêmica no banco local.
- A agenda considera bloqueio pelo dia inteiro, sem horários parciais.
- A recomendação é determinística por categoria, menor preço e menor ID; não usa inteligência artificial.
- Não há upload de arquivos, notificações, chat ou integração com serviços externos.
- A aplicação foi preparada para execução local e não inclui publicação em produção.

