# Regras locais do FestKids

- Responda e documente em português do Brasil.
- Antes de implementar, leia a mudança ativa em `openspec/changes/reconstruir-festkids-do-zero/`.
- Avance uma tarefa OpenSpec por vez e marque-a somente depois da verificação indicada.
- Ao concluir e verificar uma tarefa, crie um commit local com mensagem que identifique a etapa; envie ao remoto quando ele existir e houver autorização.
- Explique ao usuário onde cada arquivo e elemento ficará antes de criá-lo.
- Preserve a arquitetura `Route → Controller → Service → Model/Repository → MySQL`.
- Use Models com ORM para CRUD simples e Repository apenas para consultas ou transações especializadas.
- Não coloque regras de negócio nos Controllers nem no frontend.
- Não copie código do repositório FestKids anterior; ele serve apenas como referência.
- Nunca versione `.env`, `.env.local`, credenciais, bancos ou dados pessoais reais.
- Use dados fictícios na demonstração e um schema MySQL separado para testes.

## Comandos disponíveis nesta fase

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m pytest backend\tests -q
openspec validate reconstruir-festkids-do-zero --type change --strict --no-interactive
openspec status --change reconstruir-festkids-do-zero
git status --short --branch
```

O comando de execução será adicionado quando a aplicação Flask realmente existir.

