# Spec Delta

## Purpose

Definir os comportamentos cadastrais que mantêm clientes, fornecedores, serviços e festas de forma válida e coerente para sustentar o planejamento.

## ADDED Requirements

### Requirement: Operações cadastrais completas
O sistema SHALL permitir cadastrar, listar, consultar por identificador, atualizar e excluir clientes, fornecedores, serviços e festas.

#### Scenario: Cadastro válido
- **WHEN** o usuário envia todos os dados obrigatórios válidos de um recurso
- **THEN** o sistema persiste o registro e devolve sua representação com identificador

#### Scenario: Consulta de registro inexistente
- **WHEN** o usuário consulta um identificador que não existe
- **THEN** o sistema informa que o registro não foi encontrado sem expor detalhes internos

### Requirement: Validação dos dados
O sistema MUST rejeitar dados ausentes, malformados ou incompatíveis com as regras do recurso antes de concluir a operação.

#### Scenario: Entrada inválida
- **WHEN** o usuário envia um campo obrigatório vazio ou um valor com formato inválido
- **THEN** o sistema não persiste a alteração e devolve uma mensagem compreensível de validação

### Requirement: Integridade dos vínculos
O sistema MUST preservar os relacionamentos entre cliente e festa, fornecedor e serviço, e festa e itens de planejamento.

#### Scenario: Exclusão de registro vinculado
- **WHEN** o usuário tenta excluir um registro necessário para outro registro existente
- **THEN** o sistema impede a exclusão e explica o conflito de integridade

### Requirement: Dinheiro e datas consistentes
O sistema SHALL tratar valores monetários com duas casas decimais e datas em formato não ambíguo.

#### Scenario: Valor monetário válido
- **WHEN** um preço ou orçamento válido é persistido e recuperado
- **THEN** o valor retornado mantém duas casas decimais sem erro de ponto flutuante

