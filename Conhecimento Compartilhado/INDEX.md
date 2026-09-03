# Índice de conhecimento compartilhado

Esta base contém somente contexto curado que pode ser útil para mais de uma IA. Leia o README antes de editar e confira a data, o escopo e a confiança de cada entrada.

| Arquivo | Finalidade | Estado |
|---|---|---|
| [README.md](README.md) | Regras de curadoria, privacidade, atualização e integração do aprendizado por feedback. | Ativo |
| [perfil-de-colaboracao.md](perfil-de-colaboracao.md) | Preferências de trabalho confirmadas. | Inicial |
| [mapa-de-projetos.md](mapa-de-projetos.md) | Visão geral dos projetos compartilhados. | Inicial |
| [glossario.md](glossario.md) | Termos e nomes específicos. | Inicial |
| [fontes-e-afirmacoes.md](fontes-e-afirmacoes.md) | Evidências e fatos verificáveis. | Inicial |
| [perguntas-em-aberto.md](perguntas-em-aberto.md) | Dúvidas que precisam de investigação ou decisão. | Inicial |
| [proposta-de-expansao.md](proposta-de-expansao.md) | Sugestões de camadas, campos e controles para aumentar conhecimento útil. | Ativo |
| [aprendizado-por-feedback/](aprendizado-por-feedback/) | Sistema obrigatório de erros bloqueados, sucessos confirmados e casos de uso para todas as IAs. | Ativo |
| `projetos/` | Fichas detalhadas de projetos. | Vazio |
| `decisoes/` | Decisões globais e alternativas rejeitadas. | Vazio |

## Regra de promoção

Uma informação começa na conversa entre IAs ou na memória individual. Ela só entra nesta base quando for útil para mais de uma IA e estiver confirmada pelo usuário ou apoiada por fonte verificável. Hipóteses permanecem marcadas como hipóteses.

Há uma exceção operacional importante: **feedback negativo explícito do usuário** sobre uma abordagem executada pode ser promovido diretamente para `aprendizado-por-feedback/ERROS.md`, desde que o escopo seja fiel ao que foi rejeitado. Quando uma alternativa for aprovada ou validada, registrar também em `SUCESSOS.md` e ligar as duas entradas.

Antes de tarefas semelhantes a algo já corrigido, todas as IAs devem consultar `aprendizado-por-feedback/INDEX.md` e as entradas relevantes em `ERROS.md` e `SUCESSOS.md`.
