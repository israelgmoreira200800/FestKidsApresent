# Design

## Context

O projeto começa sem código de aplicação. A referência acadêmica exige frontend separado da API, organização em Controllers, Services, Repositories e Models, CRUD com ORM e consultas especializadas no Repository. O desenvolvimento precisa permanecer simples o bastante para ser explicado passo a passo; consulte `proposal.md` para a motivação e os arquivos em `specs/` para os comportamentos.

## Goals / Non-Goals

**Goals:**

- Construir um monólito modular com dependências fluindo da entrada HTTP para os casos de uso e a persistência.
- Permitir que cada funcionalidade seja ensinada e validada de ponta a ponta antes da próxima.
- Manter contratos HTTP, regras e persistência testáveis separadamente.
- Produzir evidências claras para arquitetura, ORM, Repository e separação frontend/API.

**Non-Goals:**

- Reutilizar arquivos do projeto anterior como implementação.
- Criar abstrações genéricas antes de existir repetição comprovada.
- Preparar microsserviços, filas, cache distribuído ou infraestrutura de produção.
- Modelar autenticação, pagamentos ou negociação comercial nesta mudança.

## Decisions

### Monólito modular em camadas

O backend será um único processo Flask organizado em `routes`, `controllers`, `services`, `models` e `repositories`. Essa escolha coincide com o material da disciplina e facilita acompanhar uma requisição completa.

Alternativas consideradas: microsserviços aumentariam implantação e comunicação sem benefício acadêmico; uma aplicação sem camadas esconderia as responsabilidades cobradas pela banca.

### Services por caso de uso

Cada ação da aplicação terá um Service identificável. Controllers cuidarão de HTTP e Models cuidarão de mapeamento/persistência simples.

Alternativa considerada: concentrar todas as regras em Models Active Record reduziria arquivos, mas dificultaria demonstrar a camada de aplicação e testar regras isoladamente.

### Repository somente para operações especializadas

CRUD simples usará ORM nas Models. Sugestões, agregações de orçamento, conflitos de agenda e confirmação coordenada usarão um Repository de planejamento. Seguindo o exemplo estudado em aula, as consultas especializadas ficarão em stored procedures do MySQL e o Repository conterá somente chamadas `CALL` parametrizadas e a conversão do resultado.

Alternativa considerada: um Repository para cada entidade duplicaria operações do ORM e criaria cerimônia sem regra adicional.

### MySQL como única persistência da aplicação

O ambiente de demonstração e os testes de integração usarão MySQL em schemas separados. Não haverá fallback silencioso para outro banco, evitando diferenças de dialeto, bloqueio e tipos monetários.

Alternativa considerada: SQLite simplificaria o início, mas não reproduziria o banco e a concorrência exigidos na apresentação.

### SQL limitado ao conteúdo estudado

O DDL usará comandos básicos de criação de banco, tabelas, chaves primárias, chaves estrangeiras, valores únicos, tipos já vistos e `ENGINE = InnoDB`. Validações de categoria, status, textos e números positivos ficarão nos Services. Views e procedures só serão adicionadas quando resolverem uma consulta real do Repository e puderem ser explicadas com base nos exercícios fornecidos.

Alternativa considerada: constraints nomeadas, checks, collations e índices avançados aumentariam a robustez do banco, mas introduziriam conceitos que a equipe não estudou e não conseguiria defender com segurança.

### Frontend sem framework na primeira versão

HTML semântico, CSS e JavaScript em módulos consumirão a API por `fetch`. Isso reduz ferramentas e deixa visível o contrato cliente-servidor.

Alternativa considerada: um framework de frontend adicionaria conceitos e build que não são necessários para os cinco fluxos.

### Experiências separadas por finalidade, sem autenticação simulada

O frontend apresentará uma entrada clara para planejamento do responsável, gestão acadêmica de fornecedores e serviços e cadastros gerais. A navegação e os textos diferenciarão essas finalidades, mas todas as páginas continuarão públicas no ambiente local porque a versão atual não possui usuário, senha, perfil ou autorização no backend.

Alternativa considerada: ocultar páginas conforme um perfil guardado apenas no navegador produziria uma falsa sensação de segurança e permitiria acesso direto às mesmas APIs. Solicitações, propostas, avaliações, imagens e painéis individuais serão apresentados somente como evoluções futuras, nunca como funcionalidades ativas.

### Desenvolvimento em fatias verticais

A primeira fatia será cadastrar cliente de ponta a ponta. Depois serão completados os cadastros e, em seguida, os casos de planejamento. Cada fatia deverá passar por explicação, autorização, implementação e verificação.

Alternativa considerada: criar todas as pastas e arquivos de todas as funcionalidades de uma vez reproduziria o problema de possuir código que a equipe não acompanhou.

### Segurança de configuração

Somente `.env.example` sem valores secretos será versionado. Configurações reais ficarão em arquivo ignorado ou no ambiente. Chaves existentes no histórico antigo não serão reutilizadas.

## Risks / Trade-offs

- [Muitas classes e arquivos para operações simples] → explicar o papel de cada camada e evitar abstrações adicionais.
- [MySQL aumenta o trabalho de configuração] → documentar um único procedimento reproduzível e separar demonstração de testes.
- [Reserva por dia inteiro limita o domínio] → registrar explicitamente a simplificação e deixar horários como evolução futura.
- [Sugestão pelo menor preço é simples] → valorizar determinismo e explicabilidade; regras adicionais só entram com requisito validado.
- [Prazo pode incentivar saltos entre etapas] → limitar cada aplicação a tarefas pequenas e impedir avanço sem verificação.
- [Concorrência na confirmação] → usar transação e bloqueios determinísticos, com teste de integração específico.

## Migration Plan

Não haverá migração automática do repositório ou banco anterior. O projeto criará um schema novo e dados fictícios próprios. Caso seja necessário comparar resultados, o repositório antigo permanecerá somente como referência de leitura. A reversão de cada etapa será feita por commits pequenos no novo histórico, sem alterar o projeto anterior.
