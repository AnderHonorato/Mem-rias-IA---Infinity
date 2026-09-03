# Índice de memória do GPT

**Atualizado em:** 2026-09-03

| Caminho | Finalidade | Estado |
|---|---|---|
| [README.md](README.md) | Regras da área do GPT. | Ativo |
| [Interacoes/](Interacoes/) | Histórico cronológico obrigatório e contínuo. | Ativo |
| [Memorias/Sentimentais/](Memorias/Sentimentais/) | Memórias emocionais e relacionais. | Ativo |
| [Memorias/](Memorias/) | Demais memórias temáticas e registros legados. | Ativo |
| [Projetos/peonia-identidade-visual.md](Projetos/peonia-identidade-visual.md) | Briefing e andamento da identidade visual da cliente Peônia. | Ativo |
| [Decisoes/habilidades-compartilhadas-do-repositorio.md](Decisoes/habilidades-compartilhadas-do-repositorio.md) | Regra permanente sobre consulta e manutenção de habilidades compartilhadas. | Ativo |
| [Decisoes/registro-continuo-de-interacoes.md](Decisoes/registro-continuo-de-interacoes.md) | Regra permanente: ler contexto no início e registrar resumidamente cada nova mensagem do usuário e resposta do GPT. | Ativo |
| [Decisoes/registro-de-raciocinio-resumido.md](Decisoes/registro-de-raciocinio-resumido.md) | Regra permanente: registrar sínteses seguras de decisões, hipóteses, aprendizados, incertezas e próximos passos, sem chain-of-thought privada. | Ativo |
| [Decisoes/aprendizado-por-feedback.md](Decisoes/aprendizado-por-feedback.md) | Regra permanente do GPT para registrar erros rejeitados, sucessos confirmados e consultar o aprendizado antes de repetir abordagens. | Ativo |
| [../Conhecimento Compartilhado/aprendizado-por-feedback/](../Conhecimento%20Compartilhado/aprendizado-por-feedback/) | Registro compartilhado de ERROS, SUCESSOS e casos de uso válido para todas as IAs. | Ativo |
| [../Habilidades/](../Habilidades/) | Catálogo compartilhado de habilidades disponível a todas as IAs. | Ativo |

## Fluxo

1. No início de cada interação/conversa, ler o README raiz, `GPT/README.md`, este índice e os arquivos temáticos necessários.
2. Não é necessário reler os mesmos arquivos a cada mensagem do mesmo fluxo, salvo necessidade técnica, novo contexto temático ou pedido explícito de Ander.
3. Se a tarefa for semelhante a algo que já recebeu correção, rejeição ou validação, consultar `../Conhecimento Compartilhado/aprendizado-por-feedback/INDEX.md`, `ERROS.md` e `SUCESSOS.md` nas entradas relevantes antes de escolher a abordagem.
4. Após cada nova mensagem de Ander e cada nova resposta do GPT, registrar resumidamente a ocorrência em `Interacoes/`.
5. Quando houver conteúdo temático, registrar também na pasta temática correspondente.
6. Quando houver feedback negativo reutilizável, registrar o erro compartilhado no escopo correto; quando a alternativa for aprovada ou validada, registrar o sucesso e relacionar os IDs.
7. Quando houver valor para continuidade, registrar uma síntese segura do raciocínio útil conforme `Decisoes/registro-de-raciocinio-resumido.md`.
8. Preservar mídias e artefatos importantes quando possível; quando o binário não puder ser salvo, registrar referência identificável em `Artefatos/`.
9. Manter categorias separadas em vez de concentrar tudo em um único arquivo.
