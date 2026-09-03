---
id: SUC-2026-000001
schema_version: 1
type: success
status: active
scope: global
created_at: 2026-09-03
confidence: confirmed
sensitivity: normal
source:
  type: branch-reconciliation
  ref: feat/aprendizado-por-feedback:SUCESSOS.md
generated_by:
  agent: gpt-5.6-sol
related_error: ERR-2026-000001
---

# Sucesso: aprendizado por feedback com erro/sucesso

## Contexto
É necessário impedir repetição de caminhos rejeitados sem transformar toda conversa em regra global.

## Solução
Registrar erros e sucessos em arquivos independentes com escopo, evidência, relação entre tentativa e solução, estado e temporalidade.

## Por que funciona
O feedback passa a ser recuperável e auditável por múltiplos agentes sem apagar histórico.

## Quando reutilizar
Antes de tarefas equivalentes, consulte lições do mesmo projeto, assunto, tecnologia ou entrega.

## Limitações
Instruções atuais e segurança sempre prevalecem; sucesso antigo pode ser superseded se deixar de funcionar.
