# Arquitetura do FestKids

## 1. Visão geral

O FestKids é um monólito modular: existe um único backend Flask, mas o código é separado por responsabilidade. O frontend é estático e conversa com a API exclusivamente por HTTP e JSON.

```mermaid
flowchart LR
    U[Usuário no navegador] --> F[Frontend HTML, CSS e JavaScript]
    F -->|HTTP e JSON| R[Routes]
    R --> C[Controllers]
    C --> S[Services]
    S --> M[Models ORM]
    S --> P[PlanejamentoRepository]
    M -->|SQL gerado pelo SQLAlchemy| B[(MySQL)]
    P -->|CALL parametrizado| SP[Stored procedures]
    SP --> B
```

A direção é sempre da entrada para a persistência. O banco não conhece o frontend, o Controller não acessa o banco e o Repository não decide regras de negócio.

## 2. Responsabilidade de cada parte

| Parte | Local | Responsabilidade | Não deve fazer |
|---|---|---|---|
| Frontend | `frontend/` | Exibir telas, coletar dados e chamar a API | Calcular regra de negócio ou acessar MySQL |
| Route | `backend/routes/` | Associar método e URL ao Controller | Validar domínio ou consultar banco |
| Controller | `backend/controllers/` | Ler entrada HTTP e montar resposta HTTP | Usar `db`, Model ou SQL diretamente |
| Service | `backend/services/` | Validar dados, aplicar regras e controlar transações | Formatar página ou definir URL |
| Model | `backend/models/` | Mapear classe Python para tabela e serializar entidade | Concentrar os casos de uso do planejamento |
| Repository | `backend/repositories/` | Executar consultas e bloqueios especializados | Executar `commit` ou decidir se pode confirmar |
| Stored procedure | `backend/database/create_database.sql` | Manter SQL especializado estudado no banco | Receber texto SQL concatenado pelo usuário |

## 3. Inicialização da aplicação

`backend/__init__.py` contém a factory `create_app`. Ela executa esta sequência:

```mermaid
flowchart TD
    A[create_app] --> B[Carregar Configuracao]
    B --> C{DATABASE_URL existe?}
    C -- não --> D[Interromper com RuntimeError]
    C -- sim --> E[Inicializar SQLAlchemy]
    E --> F[Configurar CORS para origens permitidas]
    F --> G[Registrar blueprints das Routes]
    G --> H[Registrar tratamento JSON de erros]
    H --> I[Aplicação Flask pronta]
```

`backend/run.py` cria a aplicação e usa `FLASK_HOST`, `FLASK_PORT` e `FLASK_DEBUG`. A configuração real fica em `backend/.env.local`, que não é versionado.

## 4. Diagrama de classes do domínio

O diagrama representa as cinco Models existentes. Os relacionamentos são implementados com chaves estrangeiras; o código não depende de atributos `relationship` nem de `Mapped`.

```mermaid
classDiagram
    class Cliente {
        +Integer id
        +String nome
        +String email
        +String telefone
        +DateTime criado_em
        +para_dict()
    }

    class Fornecedor {
        +Integer id
        +String nome_comercial
        +String email
        +String telefone
        +Boolean disponivel
        +DateTime criado_em
        +para_dict()
    }

    class Servico {
        +Integer id
        +Integer fornecedor_id
        +String nome
        +Text descricao
        +String categoria
        +Numeric preco_base
        +Integer capacidade_convidados
        +Boolean disponivel
        +DateTime criado_em
        +para_dict()
    }

    class Festa {
        +Integer id
        +Integer cliente_id
        +String nome
        +Date data
        +String local
        +Integer quantidade_convidados
        +Numeric orcamento
        +String status
        +DateTime criado_em
        +para_dict()
    }

    class PlanejamentoItem {
        +Integer id
        +Integer festa_id
        +Integer servico_id
        +Numeric preco_referencia
        +DateTime criado_em
        +para_dict()
    }

    Cliente "1" --> "0..*" Festa : cliente_id
    Fornecedor "1" --> "0..*" Servico : fornecedor_id
    Festa "1" --> "0..*" PlanejamentoItem : festa_id
    Servico "1" --> "0..*" PlanejamentoItem : servico_id
```

### Por que existe PlanejamentoItem

`PlanejamentoItem` transforma a relação entre Festa e Serviço em uma entidade própria. Além dos dois IDs, ela guarda `preco_referencia`. Assim, se o preço-base do Serviço mudar depois, o pacote já montado não muda silenciosamente.

A combinação `festa_id + servico_id` é única.

## 5. Fluxo de entrada: cadastrar um recurso

O cadastro de Cliente é o exemplo mais simples; Fornecedor, Serviço e Festa seguem o mesmo caminho.

```mermaid
sequenceDiagram
    actor U as Usuário
    participant F as frontend/clientes.js
    participant R as cliente_routes.py
    participant C as cliente_controller.py
    participant S as cliente_service.py
    participant M as Cliente Model
    participant B as MySQL

    U->>F: Preenche e envia o formulário
    F->>R: POST /api/clientes com JSON
    R->>C: criar_cliente()
    C->>S: cadastrar_cliente(dados)
    S->>S: Validar nome, e-mail e telefone
    S->>M: Criar objeto Cliente
    M->>B: INSERT pelo SQLAlchemy
    B-->>M: ID e data gerados
    S-->>C: Cliente persistido
    C-->>F: HTTP 201 com JSON
    F-->>U: Mensagem e cartão atualizado
```

Se a validação falhar, o Service lança `ErroValidacao`; o tratamento global devolve código `400` no formato JSON padronizado. Se o e-mail já existir, a resposta é `409`.

## 6. Fluxo de recuperação: listar registros

```mermaid
sequenceDiagram
    actor U as Usuário
    participant F as Frontend
    participant R as Route
    participant C as Controller
    participant S as Service
    participant M as Model ORM
    participant B as MySQL

    U->>F: Abre a tela ou clica em Atualizar
    F->>R: GET /api/clientes
    R->>C: listar_todos_clientes()
    C->>S: listar_clientes()
    S->>M: Cliente.query.order_by(id).all()
    M->>B: SELECT gerado pelo SQLAlchemy
    B-->>M: Linhas encontradas
    M-->>S: Objetos Cliente
    S-->>C: Lista de objetos
    C-->>F: HTTP 200 com lista JSON
    F-->>U: Lista, estado vazio ou erro
```

Consultar um único ID usa o mesmo fluxo com `filter_by(id=...).first()`. Quando não existe registro, o Service lança `RecursoNaoEncontrado` e a API devolve `404` sem traceback.

## 7. Fluxo especializado: sugerir pacote

```mermaid
flowchart TD
    A[Receber festa_id e categorias] --> B[Validar tipos, categorias e repetições]
    B --> C[Bloquear e consultar a Festa]
    C --> D{Festa está em RASCUNHO?}
    D -- não --> E[Rollback e erro]
    D -- sim --> F[Para cada categoria chamar sp_servicos_elegiveis]
    F --> G{Todas possuem candidato?}
    G -- não --> H[Rollback e preservar pacote anterior]
    G -- sim --> I[Excluir itens anteriores e flush]
    I --> J[Criar itens com preço de referência]
    J --> K[Consultar pacote completo]
    K --> L[Commit]
    L --> M[Responder pacote em JSON]
```

A procedure ordena os candidatos por `preco_base` e depois por `id`. Por isso, a sugestão é determinística e explicável.

## 8. Fluxo transacional: confirmar planejamento

```mermaid
flowchart TD
    A[POST confirmação] --> B[Listar fornecedores do pacote]
    B --> C{Existe pacote?}
    C -- não --> X[Rollback e erro]
    C -- sim --> D[Bloquear fornecedores em ordem de ID]
    D --> E[Bloquear Festa]
    E --> F{Continua RASCUNHO?}
    F -- não --> X
    F -- sim --> G[Bloquear itens]
    G --> H{Pacote permaneceu igual?}
    H -- não --> X
    H -- sim --> I{Serviços e fornecedores disponíveis e com capacidade?}
    I -- não --> X
    I -- sim --> J{Total cabe no orçamento?}
    J -- não --> X
    J -- sim --> K{Agenda continua livre?}
    K -- não --> X
    K -- sim --> L[Alterar status para CONFIRMADA]
    L --> M[Commit]
    M --> N[Responder RESERVA_ACADEMICA]
```

Todos os bloqueios, consultas e a alteração acontecem na mesma sessão do SQLAlchemy. O Repository não executa `commit`; o Service confirma tudo ao final ou executa `rollback` diante de qualquer exceção.

## 9. ORM e Repository não são concorrentes

- CRUD simples: `Model.query`, `db.session.add`, `delete` e `commit` nos Services.
- Consulta especializada: procedure MySQL chamada pelo `PlanejamentoRepository`.
- Regra de negócio: sempre no Service.
- Transação: controlada pelo Service, inclusive quando há chamadas ao Repository.

Resposta curta para a banca:

> O ORM resolve as operações simples sobre uma entidade. O Repository foi reservado para consultas e bloqueios especializados do planejamento; ele chama procedures com parâmetros e participa da transação aberta pelo Service.

## 10. Tratamento de erros

`backend/error_handlers.py` converte exceções em respostas previsíveis:

| Situação | Exceção | HTTP |
|---|---|---:|
| Entrada inválida | `ErroValidacao` | 400 |
| Registro inexistente | `RecursoNaoEncontrado` | 404 |
| Integridade ou estado incompatível | `ErroConflito` | 409 |
| Corpo acima do limite | `RequestEntityTooLarge` | 413 |
| Falha inesperada | `Exception` | 500 |

Falhas internas são registradas no terminal do backend, mas o JSON enviado ao navegador contém apenas uma mensagem genérica.

## 11. Evidências no código

- Factory e extensões: `backend/__init__.py` e `backend/extensions.py`.
- Routes: `backend/routes/`.
- Controllers sem acesso ao banco: `backend/controllers/`.
- Regras e transações: `backend/services/`.
- Mapeamento clássico com `db.Column`: `backend/models/`.
- Procedures e `ENGINE = InnoDB`: `backend/database/create_database.sql`.
- Chamadas `CALL` parametrizadas: `backend/repositories/planejamento_repository.py`.
- Integração HTTP: `frontend/js/api.js` e `frontend/js/planejamento.js`.
- Testes: `backend/tests/`.
