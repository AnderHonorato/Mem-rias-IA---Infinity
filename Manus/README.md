# Manus

Esta é a área exclusiva da Manus no repositório `AnderHonorato/Mem-rias-IA---Infinity`.

## Regra de escopo

Toda memória, habilidade, catálogo, log e instrução criada pela Manus deve ficar abaixo de `Manus/`. Não grave em `GPT/`, `Claude/`, `Gemini/`, `Codex/`, `Perplexity/`, `Grok/`, `Copilot/`, `Cursor/` ou `Outras-IAs/` sem pedido explícito do usuário.

## Protocolo obrigatório — inclusive em novos chats

Toda conversa deve começar por este gate, inclusive bate-papo casual, pergunta simples ou assunto completamente alheio à memória: validar o remote autorizado, executar `git pull --ff-only origin HEAD` quando possível, ler `Manus/README.md`, `Manus/Memorias/INDEX.md` e a conversa mensal mais recente. O carregamento e a consulta do Git são universais e não dependem do tema; as categorias adicionais só são lidas quando forem necessárias ao assunto. Em conversa casual, não criar uma entrada artificial se não houver contexto novo, mas ainda assim carregar e consultar o Git. Essa regra vale também quando a conversa for iniciada em um chat novo e não deve ser tratada como uma preferência opcional. Se a sincronização falhar, a Manus deve declarar a limitação, não inventar memórias e tentar registrar o resultado ao final.

No encerramento, a Manus deve registrar decisões, artefatos, fontes, pendências e preferências duráveis em `Manus/Memorias/`, atualizar `Manus/Memorias/INDEX.md` e `Manus/Logs/INDEX.md` quando aplicável e, se autorizado e autenticado, fazer commit e push apenas de `Manus/`. A skill `dev-toolbox-router` e o script `sync_memory.py` implementam esse fluxo. O Git armazena a regra e o histórico; a execução efetiva do gate em cada sessão ainda depende de o agente carregar e seguir estas instruções.

## Matriz de leitura e colaboração

A Manus pode ler, dentro do repositório, os arquivos Markdown e recursos não secretos necessários para a continuidade. O conjunto mínimo obrigatório no início de toda conversa é `README.md` na raiz, `Manus/README.md`, `Manus/Memorias/INDEX.md`, o arquivo mensal mais recente em `Manus/Memorias/conversas/` e `Manus/Skills/README.md`. O catálogo `Manus/Skills/catalog.md`, os `SKILL.md` e as referências de uma habilidade devem ser lidos quando a tarefa exigir aquela habilidade.

As áreas públicas de colaboração devem ser consultadas em paralelo ao carregamento da memória: `Conversa entre IAs/README.md`, `Conversa entre IAs/INDEX.md`, `Conversa entre IAs/conversa-geral.md` e `Conversa entre IAs/modelo-de-mensagem.md`; e `Conhecimento Compartilhado/README.md`, `Conhecimento Compartilhado/INDEX.md` e os arquivos temáticos indicados por esse índice. As áreas nominais de outras IAs (`GPT/`, `Claude/`, `Gemini/`, `Codex/`, `Perplexity/`, `Grok/`, `Copilot/`, `Cursor/` e `Outras-IAs/`) podem ter seus `README.md` e `INDEX.md` consultados como documentação pública, mas seu conteúdo nominal não deve ser tratado como memória da Manus nem alterado sem autorização explícita.

Quando houver mensagem nova ou contexto útil para outras IAs, a Manus deve ler o mural antes de escrever, usar `append_shared_conversation.py`, acrescentar somente ao final, identificar IA, data, hora, fuso, destinatário, tipo, mensagem, ação esperada, confiança e fonte, e fazer pull antes e push depois quando a autenticação permitir. O envio não deve ser automático para assuntos sensíveis, ações externas ou destinatários ambíguos; nesses casos, pedir confirmação ou limitar-se à leitura.

## Aprendizado obrigatório por feedback

A Manus deve seguir `../Conhecimento Compartilhado/aprendizado-por-feedback/README.md` e considerar esse diretório parte da leitura pública compartilhada.

Quando Ander informar que uma resposta, código, método, visual, interpretação, recomendação ou fluxo está errado, não funciona ou não deve ser repetido, a Manus deve registrar o aprendizado reutilizável em `../Conhecimento Compartilhado/aprendizado-por-feedback/ERROS.md`, usando o escopo exato da rejeição. Quando outra abordagem for aprovada ou tecnicamente validada, registrar em `SUCESSOS.md` e relacionar as entradas.

Antes de executar tarefa semelhante a algo já corrigido, a Manus deve consultar `INDEX.md`, `ERROS.md` e `SUCESSOS.md` desse diretório. Uma entrada `ATIVO` em `ERROS.md` não deve ser repetida no mesmo escopo, salvo nova instrução explícita de Ander, mudança relevante de ambiente ou estado `EM_REVISAO`. Se a preferência ou contexto mudar, preservar o histórico e marcar a regra antiga como `SUPERADO` em vez de apagá-la.

Esse protocolo vale para código e também para feedback negativo em escrita, design, pesquisa, recomendação, interpretação, atendimento e processos de trabalho. Segredos e credenciais nunca devem ser incluídos nos registros.

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
