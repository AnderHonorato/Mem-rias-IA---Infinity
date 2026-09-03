# Modelo de memória

- **Semântica:** fatos, requisitos, preferências, relações e arquitetura.
- **Episódica:** experiência de uma execução: tentativa, falha, solução, contexto.
- **Procedural:** como os agentes devem agir em fluxos recorrentes.
- **Temporal:** estado que pode mudar, com `valid_from`, `valid_until` e `review_after`.
- **Reflection:** síntese auditável do raciocínio útil e evidências; não chain-of-thought bruto.
- **Eventos:** o que aconteceu; não possuem autoridade automática de verdade durável.

## Ciclo de vida

`captured → classified → validated → promoted → active → reviewed → superseded/disputed/archived`

Correções preservam a versão anterior e apontam `supersedes`/`superseded_by`.
