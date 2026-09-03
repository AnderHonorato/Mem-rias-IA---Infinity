---
id: TRACE-2026-000001
schema_version: 1
type: decision-trace
status: completed
scope: project:memorias-ia-infinity
project: memorias-ia-infinity
created_at: 2026-09-03
confidence: high
reasoning_visibility: summarized
sensitivity: normal
source:
  type: task
  ref: EVT-2026-000001
generated_by:
  agent: gpt-5.6-sol
---

# Objetivo
Transformar a V1 em Central de Conhecimento compartilhada sem apagar histórico recente.

# Contexto observado
A V1 possui pastas nominais por IA, área compartilhada, mural e skills. O README ainda centralizava regras da Manus. A branch de aprendizado por feedback estava 22 commits à frente e 5 atrás da `main`, portanto não era base segura.

# Alternativas relevantes
- Manter uma base completa por IA: rejeitado por duplicação/divergência.
- Banco externo obrigatório: rejeitado por aumentar dependência e não ser necessário para a fonte de verdade inicial.
- Markdown canônico + adaptadores + índices derivados: escolhido.

# Evidências
- Auditoria Git da main e comparação de branches.
- Documentação oficial de Codex, Claude Code, Gemini CLI, GitHub Copilot, JSON Schema, W3C PROV e OWASP Agentic Security.

# Decisão
Criar V2 paralela com `knowledge/`, `events/`, `reflections/`, `agents/`, `coordination/`, `skills/`, schemas/scripts/tests e adaptadores pequenos.

# Incertezas
Nem todo conteúdo V1 foi promovido nesta primeira consolidação. Conteúdo ainda não classificado permanece preservado no legado.

# Resultado
Fundação V2 e migração dos projetos/feedback identificados como canônicos foram iniciadas sem apagar arquivos V1.

# Aprendizado reutilizável
Branches divergidas com conhecimento novo devem ser reconciliadas semanticamente em vez de usadas diretamente como base.
