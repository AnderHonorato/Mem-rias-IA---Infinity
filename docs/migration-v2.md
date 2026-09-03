# Migração V1 → V2

## Estratégia

A migração é incremental e não destrutiva.

### Fase A — fundação paralela
Criar `knowledge/`, `events/`, `reflections/`, `agents/`, `coordination/`, `skills/`, `schemas/`, `indexes/`, `scripts/`, `docs/` e `tests/` sem apagar V1.

### Fase B — classificação
Copiar conhecimento confirmado para a V2 com IDs, escopo, confiança, temporalidade e proveniência. Não transformar todo histórico em conhecimento ativo.

### Fase C — validação
Rodar schemas, links, duplicação, conflitos, freshness, secrets e poisoning checks.

### Fase D — adaptadores
Atualizar arquivos de entrada das plataformas para apontar para a fonte canônica.

### Fase E — compatibilidade
Manter READMEs/caminhos V1 como legado até confirmação de que consumidores foram migrados.

### Fase F — arquivo
Somente depois de validação e confirmação, conteúdo legado poderá ser movido para `archive/legacy-v1/`; nada é apagado nesta etapa.

## Mapeamento inicial

- `Conhecimento Compartilhado/` → `knowledge/` após classificação.
- `Conversa entre IAs/` → `coordination/` para novos handoffs; histórico antigo permanece.
- `Habilidades/` → `skills/` para novo catálogo; legado permanece.
- `GPT/`, `Manus/` etc. → `agents/<agent>/` apenas para novo estado específico. Conteúdo compartilhável é promovido para `knowledge/`.

## Regra de preservação

Se houver dúvida, preserve o item legado e registre a incerteza. A migração não pode apagar conhecimento recente nem sobrescrever mudanças da `main`.
