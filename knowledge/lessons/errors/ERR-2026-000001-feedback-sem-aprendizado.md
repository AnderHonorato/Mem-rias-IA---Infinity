---
id: ERR-2026-000001
schema_version: 1
type: error
status: active
scope: global
created_at: 2026-09-03
confidence: confirmed
sensitivity: normal
source:
  type: branch-reconciliation
  ref: feat/aprendizado-por-feedback:ERROS.md
generated_by:
  agent: gpt-5.6-sol
related_success: SUC-2026-000001
---

# Falha: feedback negativo sem aprendizado persistente

## Problema
Manter apenas históricos e decisões sem um registro operacional reutilizável de abordagens rejeitadas.

## Sintoma / feedback
O usuário solicitou explicitamente que erros e correções úteis sejam lembrados entre agentes.

## Causa
Ausência de protocolo canônico de erro/sucesso com escopo e evidência.

## Não repetir
Não tratar feedback negativo reutilizável como descartável ou restrito à conversa atual.

## Exceções
Não persistir ruído, hipóteses, segredos ou dados pessoais desnecessários.

## Solução relacionada
`SUC-2026-000001`.
