# Índice de memória do GPT

**Atualizado em:** 2026-09-03

| Caminho | Finalidade | Estado |
|---|---|---|
| [README.md](README.md) | Regras da área do GPT. | Ativo |
| [Interacoes/](Interacoes/) | Histórico cronológico obrigatório e contínuo. | Ativo |
| [Memorias/Sentimentais/](Memorias/Sentimentais/) | Memórias emocionais e relacionais. | Ativo |
| [Memorias/](Memorias/) | Demais memórias temáticas e registros legados. | Ativo |
| [Projetos/only-nos.md](Projetos/only-nos.md) | Contexto, deploy e pendências do projeto Only Nós (antigo Enlace). | Ativo |
| [Projetos/peonia-identidade-visual.md](Projetos/peonia-identidade-visual.md) | Briefing e andamento da identidade visual da cliente Peônia. | Ativo |
| [Decisoes/habilidades-compartilhadas-do-repositorio.md](Decisoes/habilidades-compartilhadas-do-repositorio.md) | Regra permanente sobre consulta e manutenção de habilidades compartilhadas. | Ativo |
| [Decisoes/registro-continuo-de-interacoes.md](Decisoes/registro-continuo-de-interacoes.md) | Regra permanente: ler contexto no início e registrar resumidamente cada nova mensagem do usuário e resposta do GPT. | Ativo |
| [Decisoes/registro-de-raciocinio-resumido.md](Decisoes/registro-de-raciocinio-resumido.md) | Regra permanente: registrar sínteses seguras de decisões, hipóteses, aprendizados, incertezas e próximos passos, sem chain-of-thought privada. | Ativo |
| [../Habilidades/](../Habilidades/) | Catálogo compartilhado de habilidades disponível a todas as IAs. | Ativo |

## Fluxo

1. No início de cada interação/conversa, ler o README raiz, `GPT/README.md`, este índice e os arquivos temáticos necessários.
2. Não é necessário reler os mesmos arquivos a cada mensagem do mesmo fluxo, salvo necessidade técnica, novo contexto temático ou pedido explícito de Ander.
3. Após cada nova mensagem de Ander e cada nova resposta do GPT, registrar resumidamente a ocorrência em `Interacoes/`.
4. Quando houver conteúdo temático, registrar também na pasta temática correspondente.
5. Quando houver valor para continuidade, registrar uma síntese segura do raciocínio útil conforme `Decisoes/registro-de-raciocinio-resumido.md`.
6. Preservar mídias e artefatos importantes quando possível; quando o binário não puder ser salvo, registrar referência identificável em `Artefatos/`.
7. Manter categorias separadas em vez de concentrar tudo em um único arquivo.
