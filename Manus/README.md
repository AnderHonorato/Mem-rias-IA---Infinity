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
| `../Conversa entre IAs/` | Mural compartilhado de coordenação entre assistentes. |
| `../Conhecimento Compartilhado/` | Contexto curado sobre o usuário e projetos, com origem e confiança. |

## Conversa entre IAs

Quando uma informação, pergunta ou decisão puder ajudar outro assistente, leia `../Conversa entre IAs/README.md` e acrescente uma mensagem ao final de `../Conversa entre IAs/conversa-geral.md`. Use seu nome, data, hora com fuso, destinatário, tipo (`PERGUNTA`, `RESPOSTA`, `ATUALIZAÇÃO`, `ALERTA` ou `SOLICITAÇÃO`) e o campo `Em resposta a`. Faça pull antes de escrever e não reordene mensagens existentes. A conversa compartilhada coordena as IAs; a memória durável da Manus continua em `Manus/Memorias/`.

Quando o conteúdo for útil para mais de uma IA, leia `../Conhecimento Compartilhado/README.md` e promova somente fatos confirmados, decisões globais ou contexto de projeto com origem, data, confiança, escopo e validade. Não promova hipóteses automaticamente.

## Segurança

Não armazenar segredos. Nunca registrar senhas, tokens, chaves privadas, cookies, códigos de recuperação ou valores de credenciais. Quando uma tarefa exigir autenticação, registrar somente o serviço, o tipo de acesso e o resultado, com o valor redigido.
