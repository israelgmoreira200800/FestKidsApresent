# Matriz das operações cadastrais

Esta matriz comprova as vinte operações de cadastro executadas pela API. Cada recurso possui as mesmas cinco operações: cadastrar, listar, consultar um registro, atualizar e excluir.

| Recurso | Cadastrar | Listar | Consultar | Atualizar | Excluir | Teste de evidência |
|---|---|---|---|---|---|---|
| Cliente | `POST /api/clientes` | `GET /api/clientes` | `GET /api/clientes/{id}` | `PUT /api/clientes/{id}` | `DELETE /api/clientes/{id}` | `test_lista_consulta_atualiza_e_exclui_cliente` |
| Fornecedor | `POST /api/fornecedores` | `GET /api/fornecedores` | `GET /api/fornecedores/{id}` | `PUT /api/fornecedores/{id}` | `DELETE /api/fornecedores/{id}` | `test_executa_crud_completo_de_fornecedor` |
| Serviço | `POST /api/servicos` | `GET /api/servicos` | `GET /api/servicos/{id}` | `PUT /api/servicos/{id}` | `DELETE /api/servicos/{id}` | `test_executa_crud_completo_de_servico_com_preco_decimal` |
| Festa | `POST /api/festas` | `GET /api/festas` | `GET /api/festas/{id}` | `PUT /api/festas/{id}` | `DELETE /api/festas/{id}` | `test_executa_crud_completo_de_festa` |

Os quatro testes foram executados juntos no schema isolado `festkids_test`: quatro testes aprovados, cobrindo as vinte operações.

## Caminho de uma requisição

```text
Frontend → Route → Controller → Service → Model ORM → MySQL
```

- A **Route** associa o endereço e o método HTTP à função correta.
- O **Controller** lê o JSON ou o identificador da requisição, chama o Service e monta a resposta HTTP.
- O **Service** valida os dados, aplica as regras e coordena a persistência.
- O **Model** descreve a tabela com `db.Model` e `db.Column`.
- O **SQLAlchemy** transforma chamadas do ORM em comandos para o MySQL.

## Evidência da separação das camadas

A inspeção automática dos arquivos em `backend/controllers/` não encontrou importação de `db` ou Models, uso de `.query`, `db.session` ou execução de SQL. Portanto, Controllers não acessam a persistência.

Nos arquivos em `backend/services/`, as consultas simples usam `Model.query`. Inclusões, alterações e exclusões usam `db.session.add`, `commit`, `delete` e `rollback`. Isso é ORM: o código manipula objetos Python em vez de montar comandos SQL manualmente.

O diretório `backend/repositories/` permanece reservado para as consultas e transações especializadas do planejamento. Criar um Repository para cada CRUD apenas repetiria as funções já fornecidas pelo ORM.

## Resposta curta para a banca

“O Controller não conhece o banco. Ele cuida apenas da entrada e da resposta HTTP. O Service contém as validações e usa o Model pelo ORM. Repository será usado somente quando o planejamento exigir consultas ou transações especializadas.”
