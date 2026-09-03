---
id: PAT-2026-000001
schema_version: 1
type: pattern
status: active
scope: global
created_at: 2026-09-03
confidence: confirmed
sensitivity: normal
source:
  type: derived
  ref: ERR-2026-000001+SUC-2026-000001
generated_by:
  agent: gpt-5.6-sol
derived_from:
  - ERR-2026-000001
  - SUC-2026-000001
---

# Padrão: feedback → correção → validação → reutilização

Quando houver feedback negativo reutilizável: classificar → definir escopo → registrar erro → corrigir por abordagem diferente → validar → registrar sucesso → reutilizar em tarefa equivalente.

Não aplicar como bloqueio eterno: mudanças atuais do usuário e novas evidências podem superseder registros anteriores.
