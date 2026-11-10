# Tasks

## 1. Fundação do repositório

- [x] 1.1 Criar README, AGENTS.md, `.gitignore`, `.env.example` e diretórios mínimos, verificando que a árvore corresponde ao design e nenhum segredo está versionado
- [x] 1.2 Confirmar versões atuais e compatíveis das dependências na documentação oficial, registrar `requirements.txt` e verificar a instalação em ambiente virtual limpo
- [x] 1.3 Documentar problema, público, escopo, cinco casos de uso e quatro funcionalidades não CRUD, verificando consistência com a proposta OpenSpec

## 2. Modelo de domínio e banco

- [x] 2.1 Documentar entidades, atributos, relacionamentos e simplificações do domínio, verificando o diagrama de classes contra as especificações
- [x] 2.2 Criar o DDL MySQL com comandos estudados, DECIMAL e relacionamentos por chaves estrangeiras, verificando sua execução em banco vazio
- [x] 2.3 Criar dados fictícios mínimos e idempotentes para demonstração, verificando que não há dados pessoais reais
- [x] 2.4 Configurar um schema separado de testes e proteções contra uso acidental do banco de demonstração, verificando a recusa de nomes não permitidos

## 3. Backend mínimo

- [x] 3.1 Criar a factory Flask, configuração por ambiente e inicialização do SQLAlchemy, verificando uma rota de saúde com cliente de teste
- [x] 3.2 Criar o tratamento JSON padronizado para validação, ausência, conflito e falha interna, verificando códigos 400, 404, 409 e 500 sem traceback
- [x] 3.3 Configurar CORS apenas para origens locais previstas e limite de corpo, verificando origem permitida e origem recusada

## 4. Primeira fatia vertical: Cliente

- [x] 4.1 Implementar Model Cliente e serialização, verificando persistência e recuperação no MySQL de teste
- [x] 4.2 Implementar cadastro de cliente em Route, Controller e Service, verificando sucesso e entradas inválidas por testes da API
- [x] 4.3 Criar a primeira tela de cliente e integração por fetch, verificando cadastro completo do navegador até o banco
- [x] 4.4 Completar listar, consultar, atualizar e excluir cliente, verificando as cinco operações e conflito de vínculo

## 5. Demais cadastros com ORM

- [x] 5.1 Implementar as cinco operações de Fornecedor, verificando validações e contratos HTTP
- [x] 5.2 Implementar as cinco operações de Serviço e o vínculo com Fornecedor, verificando preço decimal, capacidade e integridade
- [x] 5.3 Implementar as cinco operações de Festa e o vínculo com Cliente, verificando data, orçamento, convidados e transições permitidas de status
- [x] 5.4 Criar as telas de gestão dos quatro recursos, verificando carregamento, vazio, sucesso, erro e funcionamento em tela móvel
- [x] 5.5 Executar a matriz das vinte operações cadastrais, verificando que CRUD usa ORM e Controllers não acessam o banco diretamente

## 6. Agregado de planejamento

- [ ] 6.1 Implementar Model Item de Planejamento com preço preservado e vínculos, verificando restrições e serialização
- [ ] 6.2 Criar PlanejamentoRepository com helpers de consulta parametrizados na mesma transação da aplicação, verificando que não há concatenação de entrada em SQL
- [ ] 6.3 Implementar sugestão determinística por categoria, verificando disponibilidade, menor preço, desempate por ID e categoria sem candidato
- [ ] 6.4 Implementar análise de orçamento, verificando total, saldo, percentual, custo por convidado e casos dentro/acima do limite
- [ ] 6.5 Implementar verificação de agenda por fornecedor e dia inteiro, verificando cenários livre e conflitante
- [ ] 6.6 Implementar confirmação transacional com revalidação e bloqueio em ordem estável, verificando sucesso, rollback e concorrência entre confirmações

## 7. Jornada visual do planejamento

- [ ] 7.1 Criar navegação identificável pelas cinco etapas, verificando acesso por teclado e indicação da etapa atual
- [ ] 7.2 Integrar a tela de sugestão com a API, verificando categorias selecionadas, pacote resultante e ausência de candidato
- [ ] 7.3 Integrar a análise de orçamento, verificando formatação monetária e mensagens de viabilidade ou excedente
- [ ] 7.4 Integrar agenda e confirmação, verificando conflito, processamento, prevenção de clique duplicado e resultado sem alegação comercial
- [ ] 7.5 Validar responsividade e acessibilidade básica da jornada, verificando ausência de rolagem horizontal, rótulos, foco visível e contraste

## 8. Testes e qualidade

- [ ] 8.1 Cobrir Services e validações com testes unitários, verificando todos os ramos de regra de negócio especificados
- [ ] 8.2 Cobrir API e persistência com testes de integração MySQL, verificando CRUD, integridade, dinheiro, agenda e transações
- [ ] 8.3 Cobrir funções e contratos críticos do frontend com testes JavaScript, verificando renderização segura e transporte HTTP
- [ ] 8.4 Executar formatação, testes backend, testes frontend e inspeção de segredos, registrando resultados e qualquer verificação não executável

## 9. Documentação e preparação da banca

- [ ] 9.1 Finalizar README com instalação, configuração, execução separada, endpoints, casos de uso, limitações e testes, verificando os comandos em ambiente limpo
- [ ] 9.2 Criar documentação da arquitetura, diagrama de classes e fluxogramas de entrada e recuperação, verificando correspondência com o código real
- [ ] 9.3 Preparar dados e roteiro de demonstração das quatro funcionalidades não CRUD em até dois minutos, verificando o percurso completo em ensaio cronometrado
- [ ] 9.4 Preparar apresentação de até sete minutos e banco de perguntas técnicas, verificando tempos e respostas sobre cada camada e decisão

## 10. Publicação controlada

- [ ] 10.1 Revisar histórico, arquivos ignorados e configuração para segredos, verificando que somente exemplos vazios podem ser publicados
- [ ] 10.2 Solicitar autorização específica para criar o repositório remoto e, após autorização, publicar a branch main verificando a árvore no GitHub
