# Roteiro de demonstração em dois minutos

## 1. Objetivo

Demonstrar, em um único percurso, as quatro funcionalidades não CRUD:

1. sugestão determinística de pacote;
2. análise de orçamento;
3. verificação de agenda;
4. confirmação transacional.

O percurso usa somente dados fictícios e termina como `RESERVA_ACADEMICA`, sem pagamento ou contrato comercial.

## 2. Dados esperados

### Festa escolhida

| Campo | Valor |
|---|---|
| Festa | Festa da Lia |
| Data | 05/12/2026 |
| Convidados | 50 |
| Orçamento | R$ 5.000,00 |
| Estado inicial | RASCUNHO |

### Categorias selecionadas

- Buffet;
- Decoração;
- Fotografia.

### Pacote determinístico esperado

| Categoria | Serviço escolhido | Fornecedor | Preço |
|---|---|---|---:|
| Buffet | Buffet Econômico | Festa Fácil Buffet | R$ 900,00 |
| Decoração | Decoração Colorida | Mundo Mágico Decorações | R$ 650,00 |
| Fotografia | Cobertura Fotográfica | Click Alegria Fotografia | R$ 500,00 |
|  | **Total** |  | **R$ 2.050,00** |

Resultados do orçamento:

- saldo: R$ 2.950,00;
- percentual utilizado: 41%;
- custo por convidado: R$ 41,00;
- situação: dentro do orçamento.

A Festa do Theo está confirmada na mesma data, mas utiliza o fornecedor de Recreação. Como Recreação não entra no pacote principal, a agenda deve ficar livre.

## 3. Preparação antes da banca

### 3.1 Restaurar os dados fictícios

Execute primeiro `seed_demo.sql` para garantir que os registros existam e depois `reset_demo.sql` para devolver o cenário ao estado inicial:

```powershell
$mysql = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
Get-Content backend\database\seed_demo.sql -Raw | & $mysql -u root -p festkids
Get-Content backend\database\reset_demo.sql -Raw | & $mysql -u root -p festkids
```

O reset altera somente os registros fictícios identificados pelos nomes e e-mails do projeto. A Festa da Lia volta para `RASCUNHO`, seu pacote é limpo e a Festa do Theo volta a reservar apenas Recreação.

### 3.2 Abrir os dois servidores

Terminal 1 — backend:

```powershell
.\.venv\Scripts\python.exe -m backend.run
```

Terminal 2 — frontend:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

Abra `http://127.0.0.1:5500/planejamento.html`. Deixe a página na etapa Festa e feche abas desnecessárias.

### 3.3 Checklist de trinta segundos

- A Festa da Lia aparece na seleção.
- O backend não mostra erro de conexão.
- A página está com zoom de 100%.
- Nenhum outro backend está usando a porta 5000.
- O terminal não exibe senha nem outro segredo.

## 4. Fala e ações cronometradas

### 0:00–0:15 — apresentar o fluxo

**Fala:** “Vou demonstrar as quatro regras que não são CRUD. O frontend se comunica por JSON com a API, que percorre Route, Controller, Service e Repository até o MySQL.”

**Ação:** mostrar rapidamente as cinco etapas e selecionar **Festa da Lia**.

### 0:15–0:45 — sugerir o pacote

**Fala:** “Escolho Buffet, Decoração e Fotografia. Para cada categoria, a procedure filtra disponibilidade e capacidade; depois ordena por menor preço e menor ID. O Service só substitui o pacote se todas as categorias tiverem candidato.”

**Ação:** marcar as três categorias e clicar em **Gerar sugestão**.

**Evidência visual:** Buffet Econômico, Decoração Colorida e Cobertura Fotográfica, totalizando R$ 2.050,00.

### 0:45–1:10 — analisar o orçamento

**Fala:** “O preço fica copiado no Item de Planejamento para não mudar no futuro. A análise usa esses preços preservados: o pacote custa R$ 2.050,00, usa 41% do orçamento e custa R$ 41,00 por convidado.”

**Ação:** continuar para Orçamento e clicar em **Analisar orçamento**.

**Evidência visual:** mensagem verde “Pacote dentro do orçamento” e saldo de R$ 2.950,00.

### 1:10–1:30 — verificar a agenda

**Fala:** “A agenda procura outra festa confirmada na mesma data usando os mesmos fornecedores. A Festa do Theo existe nesse dia, mas reservou Recreação, então estes três fornecedores continuam livres.”

**Ação:** continuar para Agenda e clicar em **Verificar agenda**.

**Evidência visual:** “Fornecedores disponíveis”.

### 1:30–2:00 — confirmar com transação

**Fala:** “Na confirmação, o Service bloqueia os fornecedores em ordem, bloqueia a Festa e os itens e revalida pacote, capacidade, orçamento e agenda na mesma transação. Só então faz commit; qualquer falha gera rollback. O resultado é uma reserva acadêmica, não pagamento ou contrato.”

**Ação:** continuar para Confirmação e clicar uma vez em **Confirmar reserva acadêmica**.

**Evidência visual:** status `CONFIRMADA`, mensagem de reserva acadêmica e botão desativado contra clique duplicado.

## 5. Resumo de uma frase

“A sugestão monta o pacote, o orçamento verifica viabilidade, a agenda verifica conflitos e a transação revalida tudo antes da confirmação.”

## 6. Plano alternativo se algo falhar

- Se a lista de festas não carregar, mostrar o terminal do backend e conferir `DATABASE_URL`.
- Se aparecer conflito de agenda, confirmar que Recreação não foi marcada no pacote principal e executar novamente `reset_demo.sql`.
- Se a Festa da Lia não aparecer, ela provavelmente já foi confirmada; executar `reset_demo.sql` e atualizar a página.
- Se a porta 5000 estiver ocupada, encerrar as instâncias antigas antes de iniciar o backend correto.
- Se faltar tempo, não abrir as telas CRUD; começar diretamente em `planejamento.html`.

## 7. Perguntas que podem surgir durante a demonstração

**Por que o Buffet Econômico foi escolhido?**  
Porque atende 50 convidados, está disponível e possui o menor preço entre os buffets elegíveis.

**Por que copiar o preço para PlanejamentoItem?**  
Para preservar o valor usado no pacote mesmo que o preço-base do Serviço seja alterado depois.

**Por que verificar a agenda novamente na confirmação?**  
Porque ela pode mudar entre a consulta e o clique de confirmar. A segunda verificação acontece dentro da transação.

**O que acontece se duas festas confirmarem o mesmo fornecedor ao mesmo tempo?**  
Os bloqueios em ordem estável serializam a disputa; uma confirma e a outra recebe conflito com rollback.
