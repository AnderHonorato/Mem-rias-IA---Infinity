---
id: evt-2026-10-08-ander-whatsapp-archive
date: 2026-10-08
scope: project/ander-whatsapp
source: trusted-user + observed-tool-results
sensitivity: personal
confidence: high-for-observed-tests
---
# Evento: integração de arquivamento multimídia e comando GPT local

Solicitação: download de imagens, áudios, arquivos e vídeos, manter registro do conteúdo lido e obedecer memória Flow no repositório Infinity. Adicionalmente, o usuário quer enviar "GPT" para si no WhatsApp e receber a resposta nesta conversa ChatGPT sem API adicional.

Foram lidos `AGENTS.md`, `knowledge/INDEX.md`, `knowledge/projects/INDEX.md` e `docs/security.md` antes da escrita. A implementação local passou a usar `archive.mjs` para mensagens com texto, tipo de mídia e download privado quando disponível e `gpt-inbox.mjs` para fila dos comandos próprios.

Teste sintético via Node: quatro casos passaram (acesso em loopback; persistência deduplicada; metadados sem salvar visualização única; filtro do comando GPT para a conversa do dono). O funcionamento com mídia real será confirmado separadamente.

Decisão: **não enviar conteúdo pessoal de conversas e anexos ao GitHub**; registrar apenas implementação e resultados. Nenhuma API OpenAI/Claude/DeepSeek foi configurada. Esta conversa do ChatGPT não aceita injeção automática de mensagens por um plugin; o usuário deve invocar a ferramenta para consultar a fila/responder manualmente.

Nota: não inferir que mídia histórica esteja recuperada só porque arquivos originais estão marcados no histórico; depende da plataforma.
