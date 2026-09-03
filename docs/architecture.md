# Arquitetura V2

## Pipeline

`entrada → evento → classificação → validação → reflexão → promoção → conhecimento canônico → indexação → recuperação`

## Camadas

- **Event store:** histórico append-only do que aconteceu.
- **Knowledge:** materialização canônica do que deve ser lembrado.
- **Reflection:** Decision Traces auditáveis sobre por que decisões foram tomadas.
- **Lessons:** erros, sucessos e padrões reutilizáveis.
- **Provenance:** origem, derivação, atribuição, evidência e confirmação.
- **Indexes:** visões geradas para busca e navegação; não substituem a fonte Markdown.
- **Adapters:** instruções mínimas para cada plataforma.

## Princípio de concorrência

Prefira um registro por arquivo com ID estável. Evite arquivos monolíticos compartilhados entre várias IAs para reduzir conflitos Git.

## Integridade

IDs nunca são reutilizados. Hash SHA-256 pode ser usado por índices/snapshots quando útil, sem criar infraestrutura blockchain.
