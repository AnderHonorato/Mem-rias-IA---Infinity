---
id: EVT-2026-001012
schema_version: 1
type: event
status: recorded
scope: project:ander-whatsapp
occurred_at: 2026-10-09
actor: codex
confidence: observed
sensitivity: normal
source:
  type: owner-revocation-local-api-and-automated-tests
  ref: whatsapp-pausa-automatica-2026-10-09
generated_by:
  agent: codex
---

# Pausa de atendimento após revogação do proprietário

O proprietário revogou envios automáticos para um destinatário. Para impedir envios enquanto a identidade era conferida, a configuração privada do atendimento foi preservada e recebeu enabled:false. API em execução confirmou atendimento desabilitado, zero tarefas elegíveis e WhatsApp conectado/pareado. Nenhuma sessão tem lastAutoAt posterior à pausa. Não houve envio de mensagem, apagamento de conversa ou remoção de autenticação nesta operação. O chat Metrys Mobile é independente desse atendimento.

A lista de contatos sincronizada não identificou o destinatário pelo nome indicado. O número foi solicitado para exclusão específica; não inferir que outro contato é a mesma pessoa. Nomes, números, identificadores WhatsApp e relacionamento permanecem somente nos dados locais privados. A pausa geral continua efetiva; não reativar antes de concluir a identificação e carregar a proteção.

Fonte recebeu política de exclusão automática por telefone, JID, LID, alias e nome normalizado com igualdade. Mensagem bloqueada não cria tarefa; uma exclusão posterior cancela a pendência na revalidação antes de envio e impede replay ao desbloquear. Eventos de contatos preservam aliases quando fornecidos. Onze testes legados passaram, usando fixtures sintéticas e sem rede WhatsApp. Um número privado presente em fixture antiga foi substituído por número técnico fictício, sem alterar configuração real do contato prioritário.

Foi identificada uma colisão no evento de auditoria: o tipo de tarefa sobrescrevia kind do evento. Fonte passou a usar taskKind separado, com teste que conserva sent como tipo do evento. Histórico não foi reescrito; contagem baseada apenas em kind:sent dos logs antigos não serve como prova completa de ausência de envio. A verificação da pausa consultou configuração/API e lastAutoAt das sessões.

O reinício controlado da ponte para carregar a nova política foi rejeitado pela revisão automática sem justificativa detalhada. O comando não foi executado e o processo antigo permaneceu conectado. Não contornar essa rejeição por outro shell ou ferramenta. A pausa por configuração já funciona no processo existente, mas exclusão específica em fonte e testes não equivale a proteção carregada. Ativação e identificação específica permanecem pendentes.

Registros locais de continuidade documentam a prioridade. Nenhum segredo, conteúdo de conversa, dado de contato ou link de artefato privado foi incluído neste evento técnico.
