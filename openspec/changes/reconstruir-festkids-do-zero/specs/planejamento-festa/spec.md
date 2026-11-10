# Spec Delta

## Purpose

Definir o núcleo de planejamento que combina serviços, orçamento e agenda para permitir uma confirmação segura e explicável da festa.

## ADDED Requirements

### Requirement: Sugestão determinística de pacote
O sistema SHALL sugerir um serviço disponível de menor preço para cada categoria válida solicitada, usando o menor identificador como desempate.

#### Scenario: Pacote sugerido com sucesso
- **WHEN** a festa possui categorias válidas com serviços e fornecedores disponíveis
- **THEN** o sistema substitui o rascunho do pacote pela combinação determinística e preserva o preço utilizado em cada item

#### Scenario: Categoria sem candidato
- **WHEN** uma categoria solicitada não possui serviço elegível
- **THEN** o sistema informa a categoria sem candidato e não apresenta uma confirmação falsa de pacote completo

### Requirement: Análise de orçamento
O sistema SHALL calcular total, saldo, percentual utilizado, custo por convidado e situação de viabilidade do pacote atual.

#### Scenario: Pacote dentro do orçamento
- **WHEN** o total dos itens não ultrapassa o orçamento da festa
- **THEN** o sistema informa que o pacote é viável e apresenta os cálculos correspondentes

#### Scenario: Pacote acima do orçamento
- **WHEN** o total dos itens ultrapassa o orçamento da festa
- **THEN** o sistema informa o excedente e impede que a análise seja interpretada como aprovação

### Requirement: Verificação de agenda
O sistema MUST identificar fornecedores já reservados por outra festa confirmada na mesma data, considerando reserva por dia inteiro.

#### Scenario: Conflito encontrado
- **WHEN** um fornecedor do pacote já pertence a outro planejamento confirmado na data da festa
- **THEN** o sistema identifica o fornecedor em conflito e informa que a agenda não está livre

#### Scenario: Agenda disponível
- **WHEN** nenhum fornecedor do pacote está confirmado em outra festa na mesma data
- **THEN** o sistema informa que a agenda está disponível naquele instante

### Requirement: Confirmação transacional
O sistema MUST revalidar festa, pacote, data, orçamento e agenda na mesma operação transacional antes de confirmar o planejamento.

#### Scenario: Confirmação bem-sucedida
- **WHEN** todas as condições continuam válidas durante a operação
- **THEN** o sistema confirma o planejamento e atualiza o estado da festa de forma atômica

#### Scenario: Condição alterada antes da confirmação
- **WHEN** uma condição necessária deixa de ser válida antes do término da operação
- **THEN** o sistema desfaz a operação e mantém o planejamento sem confirmação

### Requirement: Limites da confirmação
O sistema SHALL apresentar a confirmação como reserva acadêmica do planejamento, sem alegar pagamento, contrato ou contratação comercial real.

#### Scenario: Resultado da confirmação
- **WHEN** o planejamento é confirmado
- **THEN** a interface identifica o resultado como planejamento confirmado e não como pagamento concluído

