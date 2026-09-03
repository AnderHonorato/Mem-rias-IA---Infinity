# Registro de erros e caminhos bloqueados

Este arquivo é append-only para novas entradas. Correções de uma entrada existente devem preservar o histórico, alterando o estado para `SUPERADO`, `EM_REVISAO` ou `ARQUIVADO` e apontando para a entrada substituta.

> Regra: uma entrada `ATIVO` não deve ser repetida dentro do mesmo escopo.

## Modelo obrigatório

```md
### ERR-AAAA-MM-DD-NNN — título curto
- Estado: ATIVO
- Data:
- IA que registrou:
- Origem do feedback: usuário | teste | regressão | outra
- Escopo: GLOBAL | PROJETO:<nome> | ASSUNTO:<tema> | TECNOLOGIA:<stack> | ENTREGA:<tipo> | TEMPORARIO:<condição>
- Contexto:
- Objetivo original:
- Tentativa rejeitada/errada:
- Sintoma ou feedback:
- Causa raiz: confirmada | provável | DESCONHECIDA
- NÃO REPETIR:
- Condições/exceções:
- Solução substituta: SUC-... | ainda não confirmada
- Evidência:
- Última verificação:
```

## Regras de preenchimento

- Descreva o padrão errado de forma reproduzível, não apenas “não funcionou”.
- Em código, registre o trecho mínimo/padrão técnico necessário para reconhecer o erro futuramente.
- Não copie segredos, credenciais ou dados sensíveis.
- Se o erro depender de versão, ambiente ou projeto, registre isso no escopo.
- Se o usuário rejeitar algo por preferência, registre exatamente o elemento rejeitado e não extrapole para outras categorias sem confirmação.
- Quando existir uma solução correta confirmada, relacione o `SUC-ID` correspondente.

## Entradas

### ERR-2026-09-03-001 — ausência de aprendizado persistente após feedback negativo
- Estado: ATIVO
- Data: 2026-09-03
- IA que registrou: GPT
- Origem do feedback: usuário
- Escopo: GLOBAL
- Contexto: sistema de memórias compartilhadas Memórias IA — Infinity.
- Objetivo original: garantir que as IAs aprendam com tentativas erradas e não repitam caminhos rejeitados.
- Tentativa rejeitada/errada: manter somente memórias, decisões e históricos sem um registro operacional específico que bloqueie abordagens já informadas como erradas.
- Sintoma ou feedback: o usuário solicitou explicitamente que erros, caminhos rejeitados e respectivas correções passem a ser registrados e reutilizados por todas as IAs.
- Causa raiz: confirmada — faltava um protocolo compartilhado de erro/sucesso baseado em feedback.
- NÃO REPETIR: tratar feedback negativo como algo descartável ou restrito à conversa atual quando ele contiver aprendizado reutilizável.
- Condições/exceções: aplicar somente a aprendizados úteis e seguros; não persistir segredos ou dados sensíveis desnecessários.
- Solução substituta: SUC-2026-09-03-001
- Evidência: instrução explícita do usuário nesta atualização do projeto.
- Última verificação: 2026-09-03
