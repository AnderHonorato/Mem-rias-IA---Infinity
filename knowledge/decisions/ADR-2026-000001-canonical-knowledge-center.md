---
id: ADR-2026-000001
schema_version: 1
type: decision
status: active
scope: global
created_at: 2026-09-03
confidence: confirmed
sensitivity: normal
source:
  type: user-request
  ref: prompt-memorias-ia-infinity-v2
generated_by:
  agent: gpt-5.6-sol
---

# ADR-2026-000001 — fonte canônica compartilhada

## Contexto
A V1 distribui memória entre pastas nominais por IA e uma área compartilhada, criando risco de duplicação, divergência e alto custo de recuperação.

## Problema
Múltiplos agentes precisam colaborar sem manter cópias independentes da mesma verdade.

## Alternativas
A. continuar com uma base completa por IA; B. banco externo obrigatório; C. fonte canônica Markdown versionada com adaptadores por agente.

## Decisão
Adotar C: `knowledge/` é a fonte canônica; `events/` preserva fatos ocorridos; `reflections/` preserva Decision Traces; `agents/` mantém apenas estado específico; índices JSON são materializados e regeneráveis.

## Justificativa
Reduz duplicação e conflitos Git, preserva auditabilidade, funciona com múltiplas plataformas e permite progressive disclosure.

## Consequências
Adaptadores antigos devem apontar gradualmente para V2. Conteúdo legado permanece durante migração.

## Reversibilidade
Alta: Git preserva a V1 e a V2 é introduzida em paralelo.

## Evidências
Pesquisa registrada em `docs/research-2026-09-03.md` e auditoria da `main` em 2026-09-03.
