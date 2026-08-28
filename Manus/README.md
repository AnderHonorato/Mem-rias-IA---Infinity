# Manus

Esta é a área exclusiva da Manus no repositório `AnderHonorato/Mem-rias-IA---Infinity`.

## Regra de escopo

Toda memória, habilidade, catálogo, log e instrução criada pela Manus deve ficar abaixo de `Manus/`. Não grave em `GPT/`, `Claude/`, `Gemini/`, `Codex/`, `Perplexity/`, `Grok/`, `Copilot/`, `Cursor/` ou `Outras-IAs/` sem pedido explícito do usuário.

## Protocolo obrigatório — inclusive em novos chats

Toda tarefa deve começar por este gate, antes de qualquer resposta substantiva, cálculo, consulta externa ou criação de artefato: validar o remote autorizado, executar `git pull --ff-only origin HEAD` quando possível, ler `Manus/README.md`, `Manus/Memorias/INDEX.md`, a conversa mensal mais recente e as categorias relacionadas, e registrar o início da sessão. Essa regra vale também quando a conversa for iniciada em um chat novo; não deve ser tratada como uma preferência opcional. Se a sincronização falhar, a Manus deve declarar a limitação, não inventar memórias e tentar registrar o resultado ao final.

No encerramento, a Manus deve registrar decisões, artefatos, fontes, pendências e preferências duráveis em `Manus/Memorias/`, atualizar `Manus/Memorias/INDEX.md` e `Manus/Logs/INDEX.md` quando aplicável e, se autorizado e autenticado, fazer commit e push apenas de `Manus/`. A skill `dev-toolbox-router` e o script `sync_memory.py` implementam esse fluxo. O Git armazena a regra e o histórico; a execução efetiva do gate em cada sessão ainda depende de o agente carregar e seguir estas instruções.

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
