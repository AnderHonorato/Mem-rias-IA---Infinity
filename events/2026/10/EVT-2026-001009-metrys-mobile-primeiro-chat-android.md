---
id: EVT-2026-001009
schema_version: 1
type: event
status: recorded
scope: project:ander-whatsapp/metrys-mobile
occurred_at: 2026-10-08
actor: codex
confidence: observed
sensitivity: normal
source:
  type: local-tools-and-physical-android-test
  ref: metrys-mobile-checkpoint-2026-10-08
generated_by:
  agent: codex
---

# Primeiro APK vinculado e conversa real no Android

Implementação separada dentro de metrys-mobile no Ander-WhatsApp, preservando dados e processos legados. Kotlin nativo, Node 22/SQLite, Ollama local, intermediário autenticado com conexão de saída WSS. Modelo instalado qwen2.5:1.5b; nenhuma API paga necessária para o teste.

APK 0.1.1, código 2, instalado em Galaxy A35 Android 16 com atualização ADB confirmada. Assinatura de desenvolvimento verificada. Arquivo de 921192 bytes, SHA256 eb538a0ff0598f5fe24a5873f2d22a1fb4de3b2af02a506e69d0f93d58120275. O código de pareamento temporário foi preenchido no aplicativo; o servidor autorizou o dispositivo e a tela informou computador conectado. Mensagem de teste enviada pelo próprio Android recebeu uma resposta real do modelo e a tarefa foi concluída e persistida. Nenhum conteúdo privado de conversas é registrado aqui.

Erros reais corrigidos: menus sem vínculo repetiam boas-vindas; páginas autenticadas escondiam erro de consulta e não ofereciam recuperação; callbacks tardios podiam inserir resultado em outra página; conversa removida gerava estado incorreto de PC indisponível; sessão revogada não orientava novo pareamento; processo antigo da ponte negava rotas GitHub já implementadas; registros antigos de processos podiam iniciar conexões duplicadas. A janela Samsung Pass de autopreenchimento interferiu no diagnóstico físico; foi dispensada sem salvar o código temporário.

Evidência automatizada: 23 testes Node passaram serialmente, abrangendo autenticação, idempotência, versões, reply, fila, recuperação, paginação, permissões, Git isolado, extração documental, FFmpeg e transporte. Validador usado no Android passou 18 verificações de formato e segurança. Testes HTTP reais pelo HTTPS confirmaram pareamento, resposta local e menus GitHub, projetos, arquivos, memória, WhatsApp e tarefas. Essas evidências não substituem toda a matriz física Android.

O arquivo APK disponibilizado pela ponte HTTPS foi baixado novamente e seu hash correspondeu ao artefato assinado. A ponte oferece somente esse arquivo explicitamente configurado, sem permitir escolha de caminhos do computador.

Limitações: túnel gratuito provisório com domínio variável, sem SLA e com intermediário rodando no mesmo PC; uso físico entre redes distintas ainda pendente. Modelo de visão e transcritor não instalados. Extração de documentos/quadros não equivale a análise semântica completa. WhatsApp lê somente o acervo disponível, com deduplicação, contagens e referências privadas; não envia mensagens a contatos. Fluxo Android completo de Git sensível, rich renderer completo, testes de reinício do celular e toda a matriz de aceitação permanecem pendentes.

Os registros antigos do mesmo projeto tinham frontmatter incompatível com os schemas V2. Metadados normalizados com legacy_id e texto original preservado, sem promover observações a hipóteses confirmadas. Índices devem ser reconstruídos e verificações de governança executadas após este evento.

Continuidade: README, docs/PLANO.md, docs/CHECKPOINT.md e docs/ACEITACAO.md no código local documentam inicialização, interrupção, recuperação, divisão de responsabilidades e resultados. Commit baseline local 731c2d4; código Metrys ainda em consolidação neste evento. ADR relacionado: knowledge/decisions/ADR-2026-000002-metrys-mobile.md.
