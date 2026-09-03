# Registro de sucessos e caminhos preferenciais

Este arquivo registra soluções, formatos e abordagens que foram confirmados como corretos pelo usuário ou por evidência verificável. Uma entrada ativa deve ser priorizada quando uma nova tarefa tiver o mesmo escopo e condições.

## Modelo obrigatório

```md
### SUC-AAAA-MM-DD-NNN — título curto
- Estado: ATIVO
- Data:
- IA que registrou:
- Origem da confirmação: usuário | teste | validação | outra
- Escopo: GLOBAL | PROJETO:<nome> | ASSUNTO:<tema> | TECNOLOGIA:<stack> | ENTREGA:<tipo> | TEMPORARIO:<condição>
- Contexto:
- Objetivo:
- Solução correta/preferida:
- Por que funcionou:
- Como reutilizar:
- Pré-requisitos:
- Limites/exceções:
- Erro substituído: ERR-... | nenhum
- Evidência de sucesso:
- Última verificação:
```

## Regras de preenchimento

- Registre apenas sucessos com alguma confirmação real; não trate uma tentativa nova como sucesso antes de validar.
- Em código, inclua a estratégia técnica e as condições de ambiente necessárias para reproduzir a solução.
- Em respostas, design ou outros assuntos subjetivos, descreva os elementos aprovados sem inferir preferências além do que o usuário confirmou.
- Se a solução deixar de funcionar, não apague a entrada. Marque como `SUPERADO` ou reduza seu escopo e crie a nova entrada de erro/sucesso correspondente.
- Não inclua segredos, tokens, credenciais ou informações sensíveis desnecessárias.

## Entradas

### SUC-2026-09-03-001 — protocolo compartilhado de erro e sucesso
- Estado: ATIVO
- Data: 2026-09-03
- IA que registrou: GPT
- Origem da confirmação: usuário — especificação direta do comportamento desejado
- Escopo: GLOBAL
- Contexto: sistema de memórias compartilhadas Memórias IA — Infinity.
- Objetivo: fazer todas as IAs aprenderem com feedback negativo, evitar repetição de caminhos errados e priorizar soluções que deram certo.
- Solução correta/preferida: manter registros compartilhados de `ERROS.md` e `SUCESSOS.md`, com escopo, evidência, relação entre tentativa rejeitada e solução correta, consulta obrigatória antes de repetir tarefas semelhantes e preservação do histórico quando uma regra for substituída.
- Por que funcionou: transforma feedback do usuário em conhecimento operacional persistente e reutilizável entre IAs.
- Como reutilizar: antes de tarefas semelhantes, consultar o índice e as entradas relevantes; após novo feedback negativo, registrar erro, corrigir por caminho diferente, validar e registrar o sucesso correspondente.
- Pré-requisitos: acesso ao repositório e permissão de leitura/escrita quando a IA for persistir a entrada.
- Limites/exceções: instruções atuais do usuário e regras de segurança/plataforma sempre prevalecem; casos específicos não devem virar regras globais sem evidência.
- Erro substituído: ERR-2026-09-03-001
- Evidência de sucesso: protocolo criado a partir da instrução explícita do usuário e integrado à documentação central do projeto.
- Última verificação: 2026-09-03
