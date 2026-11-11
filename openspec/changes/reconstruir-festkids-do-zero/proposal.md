# Proposal

## Why

O FestKids precisa ser reconstruído em uma base pequena, coerente e didática para que a equipe compreenda todo o caminho entre interface, API, regras de negócio e banco de dados. A reconstrução também precisa atender ao roteiro da banca: cinco casos de uso com telas, quatro funcionalidades não CRUD, CRUD com ORM, consultas no Repository e frontend separado da API.

## What Changes

- Criar um projeto novo, sem copiar a implementação anterior, preservando apenas o domínio e os requisitos validados do FestKids.
- Organizar o backend como monólito modular em camadas: Routes, Controllers, Services, Models e Repositories.
- Criar os cadastros de clientes, fornecedores, serviços e festas, totalizando vinte operações com SQLAlchemy ORM.
- Criar o agregado de planejamento e os casos de uso para sugerir pacote, analisar orçamento, verificar agenda e confirmar planejamento.
- Criar frontend responsivo em HTML, CSS e JavaScript, separado da API Flask e integrado por requisições HTTP com JSON.
- Reorganizar o frontend em experiências identificáveis de planejamento do cliente, gestão acadêmica de fornecedores e cadastros, sem simular autenticação ou recursos comerciais ausentes.
- Adicionar protótipos visuais separados para cliente e fornecedor, claramente identificados como demonstrações estáticas e sem integração com a API.
- Usar MySQL com integridade referencial, valores monetários decimais e consultas especializadas parametrizadas no Repository.
- Adicionar testes, documentação arquitetural, diagramas, fluxogramas e roteiro de apresentação.
- Excluir da primeira versão autenticação, pagamentos, propostas comerciais, avaliações, chat, uploads, IA de recomendação e publicação em produção.

## Capabilities

### New Capabilities

- `cadastros-basicos`: Cadastro, listagem, consulta, atualização e exclusão de clientes, fornecedores, serviços e festas, com validações e integridade dos vínculos.
- `planejamento-festa`: Sugestão determinística de pacote, análise de orçamento, verificação de conflitos de agenda e confirmação transacional do planejamento.
- `interface-api`: Cinco fluxos visuais no frontend consumindo a API por HTTP/JSON, com estados de carregamento, vazio, sucesso e erro.

### Modified Capabilities

Nenhuma. O projeto ainda não possui especificações existentes.

## Impact

- Novo repositório local e nova estrutura de código.
- Backend em Python, Flask, Flask-SQLAlchemy, SQLAlchemy e PyMySQL.
- Frontend em HTML semântico, CSS responsivo e JavaScript em módulos.
- Banco MySQL com tabelas para Cliente, Fornecedor, Serviço, Festa e Item de Planejamento.
- API HTTP local com contratos JSON e códigos de status documentados.
- Suíte de testes de backend, integração com banco e comportamento do frontend.
- Nenhuma integração externa ou segredo será necessário na fundação; arquivos de ambiente reais não serão versionados.
