# Skills da Manus

A pasta contém três camadas: a skill própria `dev-toolbox-router/`, o catálogo de links em `catalog.md` e os snapshots auditados em `snapshots/`.

## Regra de uso

A skill própria é a única que deve ser importada como criação desta tarefa. O catálogo aponta para fontes oficiais e links de importação do Manus. Snapshots são cópias de referência para consulta e rastreabilidade; não devem ser executados automaticamente e permanecem sujeitos às licenças dos projetos originais.

## Organização da skill própria

```text
Manus/Skills/dev-toolbox-router/
├── SKILL.md
├── references/
│   ├── memory-protocol.md
│   └── routing-matrix.md
└── scripts/
    ├── sync_memory.py
    └── append_shared_conversation.py
```

Ao atualizar a skill, valide o pacote com `quick_validate.py`, registre a mudança no log e mantenha o conteúdo dentro de `Manus/`.
