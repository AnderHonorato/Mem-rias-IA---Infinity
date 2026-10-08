---
id: ADR-2026-000002
schema_version: 1
type: decision
status: active
scope: project/ander-whatsapp/metrys-mobile
created_at: 2026-10-08
confidence: observed
sensitivity: normal
source:
  type: user-request-and-local-audit
  ref: metrys-mobile-prompt-mestre-2026-10-08
generated_by:
  agent: codex
---

# ADR-2026-000002 — Metrys Mobile nativo e independente do WhatsApp

Decisão: criar aplicativo Android nativo Kotlin, serviço Node 22/SQLite separado e integrações opcionais dentro de metrys-mobile/ no projeto Ander-WhatsApp. Conversas e credenciais ficam no armazenamento privado; o legado Baileys não é reiniciado nem migrado. Dados privados nunca entram nesta central.

A stack Kotlin ajusta a referência React Native/Expo do pedido: o computador auditado possui 8 GB RAM e SDK Android/Java já instalados. Não adicionar runtime React Native evita custo extra de instalação/build neste primeiro APK. Android nativo não usa WebView.

Autenticação prevista/implementada no serviço: código de pareamento temporário de uso único, token individual por dispositivo com hash no servidor e Android Keystore. Tarefas são registradas antes de execução e têm eventos persistidos, idempotência e cancelamento. Texto de chat não autoriza comandos arbitrários nem ações Git sensíveis.

Rede preferida: intermediário HTTPS/WSS com conexão de saída do PC, sem publicar a API do computador ou Ollama diretamente. O transporte já passou testes locais de desafio HMAC, rejeição de replay, autenticação individual encaminhada ao backend, caminhos permitidos e estado de desconexão. Isso ainda não comprova operação em redes diferentes.

O proprietário escolheu infraestrutura gratuita nesta primeira etapa. Um Cloudflare Quick Tunnel é opção provisória de teste, com endereço variável e sem garantia de disponibilidade. Não equivale a hospedagem estável de produção; migrar para túnel nomeado/servidor autorizado quando disponível. Referência primária: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/ .

Falha histórica identificada: o worker local não oferece ferramenta de análise geral do arquivo WhatsApp; a API /messages limita cada consulta a 500 registros. Um pedido de resumo global ao modelo sozinho não lhe fornece o histórico. Criar leitor completo JSONL com deduplicação de revisões, filtros, contadores, cobertura, arquivos efetivamente presentes, erros e referências privadas. Nunca afirmar histórico remoto completo ou análise semântica de placeholders.

Preservação verificada por SHA256 de 391 arquivos locais antes da implementação; snapshot com serviço ativo não é backup transacional. Sessões autenticadas continuam no PC. Referência visual encontrada: estrela Metrys existente no projeto metrys-hub, consultada sem modificar aquele projeto.

Checkpoint desta decisão: implementação em andamento; nenhum APK nem aceitação física Android ou rede externa declarado neste registro. Resultados posteriores devem ir a events/ com evidências e limitações.
