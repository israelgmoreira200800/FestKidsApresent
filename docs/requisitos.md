# Requisitos do FestKids

## 1. Visão do produto

O FestKids é uma plataforma acadêmica de planejamento de festas infantis. O sistema ajuda o responsável pelo evento a cadastrar a festa, selecionar categorias de serviços, receber uma sugestão de pacote, avaliar o orçamento, verificar conflitos de agenda e confirmar o planejamento.

Nesta versão, confirmar o planejamento representa uma reserva acadêmica dentro do sistema. Não representa pagamento, assinatura de contrato nem contratação comercial real.

## 2. Problema

Organizar uma festa infantil exige pesquisar fornecedores separados, comparar serviços, somar preços e verificar se todos poderão atender na data desejada. Esse processo fragmentado pode causar:

- perda de tempo;
- dificuldade para comparar alternativas;
- estouro do orçamento;
- falta de alguma categoria necessária;
- conflito de agenda dos fornecedores;
- desorganização das escolhas realizadas.

O FestKids centraliza essas informações e aplica regras simples e explicáveis para auxiliar o planejamento.

## 3. Público-alvo

### Público principal

Pais, mães e responsáveis que desejam organizar uma festa infantil com mais controle sobre serviços, orçamento e disponibilidade.

### Público representado no sistema

Fornecedores de serviços para festas, como buffet, decoração, fotografia, recreação, bolos, doces e espaços para eventos.

Nesta versão acadêmica, fornecedores serão registros administrados pelo sistema. Eles não terão conta, login ou painel próprio.

## 4. Proposta de valor

> Planeje uma festa infantil em um único lugar, selecione serviços, acompanhe o orçamento e verifique a disponibilidade dos fornecedores antes de confirmar suas escolhas.

O FestKids não será apenas uma lista de fornecedores. Seu núcleo será o fluxo integrado:

```text
Festa cadastrada
→ pacote sugerido
→ orçamento analisado
→ agenda verificada
→ planejamento confirmado
```

## 5. Escopo da primeira versão

### Entidades

- Cliente
- Fornecedor
- Serviço
- Festa
- Item de Planejamento

### Operações cadastrais

Cliente, Fornecedor, Serviço e Festa terão cinco operações cada:

1. Cadastrar.
2. Listar.
3. Consultar por identificador.
4. Atualizar.
5. Excluir.

Isso totaliza vinte operações cadastrais implementadas com ORM.

### Funcionalidades de negócio

- sugerir um pacote de serviços;
- analisar o orçamento da festa;
- verificar conflitos de agenda;
- confirmar o planejamento.

## 6. Cinco casos de uso principais

### UC01 — Cadastrar festa

**Ator:** responsável pela festa.

**Objetivo:** registrar as informações necessárias para iniciar o planejamento.

**Entrada principal:** cliente, nome da festa, data, local, quantidade de convidados e orçamento.

**Resultado esperado:** festa criada com estado inicial de planejamento.

**Tela prevista:** formulário de festa.

### UC02 — Sugerir pacote de serviços

**Ator:** responsável pela festa.

**Objetivo:** obter uma combinação inicial de serviços para as categorias escolhidas.

**Entrada principal:** festa e categorias desejadas.

**Resultado esperado:** um serviço elegível por categoria, com o preço utilizado preservado no planejamento.

**Tela prevista:** etapa de seleção das categorias e resultado do pacote.

### UC03 — Analisar orçamento

**Ator:** responsável pela festa.

**Objetivo:** saber se o pacote cabe no orçamento disponível.

**Entrada principal:** festa e pacote atual.

**Resultado esperado:** total, saldo, percentual utilizado, custo por convidado e indicação de viabilidade.

**Tela prevista:** resumo financeiro do planejamento.

### UC04 — Verificar agenda

**Ator:** responsável pela festa.

**Objetivo:** descobrir se algum fornecedor do pacote já está reservado na data da festa.

**Entrada principal:** data da festa e fornecedores selecionados.

**Resultado esperado:** indicação de agenda livre ou relação dos fornecedores em conflito.

**Tela prevista:** verificação de disponibilidade.

### UC05 — Confirmar planejamento

**Ator:** responsável pela festa.

**Objetivo:** confirmar o pacote depois de revalidar todas as condições.

**Entrada principal:** festa e planejamento atual.

**Resultado esperado:** planejamento confirmado de forma atômica ou mensagem explicando a condição que impediu a confirmação.

**Tela prevista:** revisão e confirmação.

## 7. Quatro funcionalidades não CRUD

### 7.1 Sugestão determinística

Para cada categoria válida solicitada, o sistema escolherá o serviço disponível de menor preço. Em caso de empate, escolherá o menor identificador.

A regra é propositalmente simples porque precisa ser:

- previsível;
- testável;
- explicável ao usuário;
- defensável perante a banca.

Não será utilizada inteligência artificial para recomendar serviços.

### 7.2 Análise do orçamento

O sistema calculará automaticamente:

- valor total do pacote;
- saldo restante ou valor excedente;
- percentual do orçamento utilizado;
- custo por convidado;
- situação de viabilidade.

### 7.3 Verificação da agenda

O sistema comparará os fornecedores do pacote com outras festas confirmadas na mesma data.

Simplificação adotada: cada reserva ocupa o dia inteiro. Não haverá controle de horários nesta versão.

### 7.4 Confirmação transacional

Antes da confirmação, o sistema revalidará:

- existência da festa;
- existência e conteúdo do pacote;
- validade da data;
- orçamento suficiente;
- ausência de conflitos de agenda;
- estado atual da festa.

Se alguma condição falhar, nenhuma confirmação parcial poderá permanecer gravada.

## 8. Regras de negócio iniciais

1. Um cliente poderá possuir várias festas.
2. Uma festa pertencerá a um cliente.
3. Um fornecedor poderá oferecer vários serviços.
4. Um serviço pertencerá a um fornecedor.
5. Um planejamento deverá pertencer a uma festa.
6. O preço utilizado deverá ser preservado no Item de Planejamento.
7. Somente serviços e fornecedores disponíveis poderão ser sugeridos.
8. Categorias inválidas deverão ser rejeitadas.
9. Valores monetários deverão possuir duas casas decimais.
10. Registros vinculados não poderão ser excluídos de modo a quebrar a integridade dos dados.
11. Uma festa confirmada reservará seus fornecedores durante o dia inteiro.
12. A confirmação deverá ocorrer em uma transação única.

## 9. Requisitos de interface

- Funcionar em computadores e celulares.
- Possuir HTML semântico e navegação por teclado.
- Apresentar rótulos claros nos campos.
- Indicar carregamento durante operações assíncronas.
- Evitar envios duplicados.
- Apresentar estados vazios, sucessos e erros.
- Preservar dados corrigíveis quando a API rejeitar uma entrada.
- Informar claramente em qual etapa do planejamento o usuário está.

## 10. Fora do escopo

Não serão implementados nesta versão:

- autenticação e recuperação de senha;
- perfis e permissões;
- painel próprio do fornecedor;
- painel administrativo;
- aprovação ou verificação comercial de fornecedores;
- solicitações, propostas e contrapropostas;
- pagamentos e repasses;
- avaliações;
- chat e notificações reais;
- upload de imagens;
- geolocalização avançada;
- aplicativo móvel nativo;
- inteligência artificial de recomendação;
- hospedagem pública de produção.

Esses itens poderão ser citados como possíveis evoluções, mas não como funcionalidades existentes.

## 11. Critérios de conclusão acadêmica

O sistema será considerado pronto para apresentação quando possuir:

- cinco casos de uso funcionais e associados às respectivas telas;
- quatro funcionalidades não CRUD demonstráveis de ponta a ponta;
- vinte operações cadastrais com ORM;
- consultas especializadas na camada Repository;
- frontend separado da API e consumindo HTTP/JSON;
- banco MySQL com integridade referencial;
- testes proporcionais às regras;
- README, arquitetura, diagrama de classes e fluxogramas coerentes com o código;
- demonstração das quatro funcionalidades em até dois minutos;
- apresentação completa em até sete minutos.

