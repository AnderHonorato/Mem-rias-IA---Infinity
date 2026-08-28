# Manus

Esta é a área exclusiva da Manus no repositório `AnderHonorato/Mem-rias-IA---Infinity`.

## Regra de escopo

Toda memória, habilidade, catálogo, log e instrução criada pela Manus deve ficar abaixo de `Manus/`. Não grave em `GPT/`, `Claude/`, `Gemini/`, `Codex/`, `Perplexity/`, `Grok/`, `Copilot/`, `Cursor/` ou `Outras-IAs/` sem pedido explícito do usuário.

## Protocolo obrigatório

No início de cada tarefa, leia `Manus/Memorias/INDEX.md`, o arquivo de conversa mais recente e as categorias relacionadas. Sincronize o clone local antes de ler dados novos quando houver conectividade. Registre o início e o encerramento da tarefa em Markdown. O histórico pode crescer por tempo indefinido, organizado por tema e mês, sem apagar entradas automaticamente.

No encerramento, atualize o índice, registre decisões e artefatos e, se autorizado e autenticado, faça commit e push apenas de `Manus/`. A skill `dev-toolbox-router` e o script `sync_memory.py` implementam esse fluxo.

## Subpastas

| Pasta | Uso |
|---|---|
| `Memorias/` | Contexto persistente dividido por tema. |
| `Skills/` | Skills próprias da Manus, catálogo e snapshots autorizados. |
| `Logs/` | Registro resumido de sincronizações e decisões operacionais. |
| `Config/` | Convenções não secretas e metadados do espaço. |

## Segurança

Não armazenar segredos. Nunca registrar senhas, tokens, chaves privadas, cookies, códigos de recuperação ou valores de credenciais. Quando uma tarefa exigir autenticação, registrar somente o serviço, o tipo de acesso e o resultado, com o valor redigido.
