# Spec Delta

## Purpose

Definir uma experiência web separada da API que torne os cinco casos de uso demonstráveis, compreensíveis e verificáveis pela banca.

## ADDED Requirements

### Requirement: Cinco casos de uso acessíveis
O frontend SHALL oferecer telas ou etapas identificáveis para cadastrar festa, sugerir pacote, analisar orçamento, verificar agenda e confirmar planejamento.

#### Scenario: Navegação pelo planejamento
- **WHEN** o usuário inicia o planejamento de uma festa
- **THEN** a interface permite percorrer os cinco casos de uso e compreender a etapa atual

### Requirement: Integração HTTP com JSON
O frontend MUST obter e alterar dados por requisições HTTP à API, sem acessar diretamente o banco de dados.

#### Scenario: Requisição bem-sucedida
- **WHEN** o usuário executa uma ação válida na interface
- **THEN** o frontend envia a requisição adequada e atualiza a tela com a resposta JSON da API

#### Scenario: Falha da API
- **WHEN** a API devolve um erro de validação, conflito ou indisponibilidade
- **THEN** o frontend apresenta uma mensagem útil e preserva os dados que o usuário ainda pode corrigir

### Requirement: Estados visuais essenciais
O frontend SHALL apresentar estados de carregamento, conteúdo vazio, sucesso e erro nas operações assíncronas relevantes.

#### Scenario: Operação em andamento
- **WHEN** uma requisição ainda não terminou
- **THEN** a interface sinaliza o processamento e evita envio duplicado acidental

### Requirement: Interface responsiva e acessível
O frontend SHALL permanecer utilizável em telas móveis e por navegação de teclado, com estrutura semântica, rótulos e foco visível.

#### Scenario: Uso em tela estreita
- **WHEN** a interface é aberta em uma largura típica de celular
- **THEN** o conteúdo permanece legível e as ações essenciais continuam acessíveis sem rolagem horizontal da página

### Requirement: Contrato de erros consistente
A API SHALL responder erros em formato JSON previsível e com códigos HTTP compatíveis com a situação.

#### Scenario: Recurso inexistente
- **WHEN** o frontend solicita um recurso que não existe
- **THEN** a API devolve código de não encontrado e uma mensagem JSON sem traceback

