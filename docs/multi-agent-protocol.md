# Protocolo multiagente

## Leitura

Cada agente começa pelo adaptador compatível e `AGENTS.md`, depois `knowledge/INDEX.md` e somente o contexto necessário.

## Escrita

- Estado específico → `agents/<agent>/`.
- Handoff → `coordination/handoffs/`.
- Evento → `events/`.
- Conhecimento durável → `knowledge/` após validação.
- Reflexão útil → `reflections/`.

## Correção

Não apague silenciosamente. Marque o registro anterior como `superseded` e crie novo registro com `supersedes` quando a informação durável mudar.

## Coordenação

Handoffs devem incluir: `task`, `status`, `agent_from`, `agent_to`, `project`, `files_changed`, `decisions`, `errors`, `successes`, `pending`, `risks`.

Handoff não é conhecimento; itens duráveis devem ser promovidos separadamente.
