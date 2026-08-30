# Registro de raciocínio resumido do GPT

**Definido por Ander em:** 2026-08-30
**Estado:** REGRA PERMANENTE

## Regra

Além de registrar resumidamente as interações, o GPT deve preservar no repositório, quando houver utilidade para continuidade, um **resumo seguro do raciocínio útil produzido durante a tarefa**.

O registro pode incluir:

- decisões tomadas e por quê;
- hipóteses consideradas;
- alternativas relevantes avaliadas;
- dúvidas ou incertezas que permaneceram;
- conclusões e aprendizados;
- critérios usados para escolher uma solução;
- erros encontrados e correções aplicadas;
- pendências e próximos passos.

## Limite obrigatório

Não registrar chain-of-thought privada, raciocínio interno bruto, scratchpad oculto, conteúdo confidencial do sistema ou qualquer sequência detalhada de pensamentos internos. Em vez disso, registrar apenas uma síntese de alto nível, segura e útil para continuidade.

Também continuam proibidos segredos como senhas, tokens, cookies, chaves privadas e códigos de recuperação.

## Onde registrar

- O resumo da interação continua em `GPT/Interacoes/`.
- Decisões e justificativas duráveis podem ser registradas em `GPT/Decisoes/`.
- Aprendizados e contexto temático devem ir para a pasta apropriada em `GPT/Memorias/` ou `GPT/Projetos/`.
- Não duplicar conteúdo desnecessariamente; registrar somente o que tiver valor futuro.
