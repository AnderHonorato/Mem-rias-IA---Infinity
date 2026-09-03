# Aprendizado por feedback

Este diretório implementa o protocolo obrigatório de **aprendizado por erro, correção e sucesso confirmado pelo usuário** para todas as IAs que utilizam o repositório Memórias IA — Infinity.

A finalidade é simples: quando uma IA tenta um caminho, código, resposta, formato, procedimento ou decisão que o usuário informa estar errado, inadequado ou indesejado, esse erro não deve ser repetido no mesmo contexto. Quando outro caminho resolve o problema ou recebe confirmação positiva, ele deve ser registrado como solução preferencial e reutilizável.

## Arquivos centrais

- `ERROS.md` — registro dos caminhos rejeitados, falhas e padrões que não devem ser repetidos.
- `SUCESSOS.md` — registro dos caminhos corretos, soluções confirmadas e padrões que devem ser priorizados.
- `CASOS-DE-USO.md` — exemplos detalhados para código, escrita, design, recomendações, pesquisa, suporte e outros tipos de tarefa.
- `INDEX.md` — índice e estado do sistema.

## Regra obrigatória para todas as IAs

Antes de repetir uma tarefa, correção, abordagem técnica ou tipo de entrega já executada anteriormente, a IA deve consultar `ERROS.md` e `SUCESSOS.md` quando houver entrada relevante para o mesmo projeto, assunto, tecnologia, preferência ou fluxo.

### Quando registrar um ERRO

Registrar quando ocorrer pelo menos uma destas situações:

1. O usuário disser que a resposta, solução, código, resultado ou caminho está errado.
2. O usuário informar que algo não funcionou e a causa estiver ligada à abordagem aplicada.
3. O usuário rejeitar explicitamente um formato, estilo, comportamento, ferramenta, recomendação ou decisão.
4. Uma tentativa produzir erro verificável e posteriormente outra abordagem corrigir o problema.
5. O usuário corrigir uma afirmação, preferência ou interpretação da IA.
6. Uma IA descobrir que um procedimento anterior gerou regressão, perda de funcionalidade, quebra de compatibilidade ou resultado contrário ao pedido.

### Quando registrar um SUCESSO

Registrar quando houver evidência de que outro caminho foi correto, por exemplo:

1. O usuário confirmar que funcionou, ficou correto, resolveu ou aprovou.
2. Um teste verificável passar após substituir a abordagem errada.
3. A correção eliminar o erro anterior sem regressão conhecida.
4. O usuário indicar explicitamente o formato, estilo, método ou solução que prefere no lugar do rejeitado.

## Escopo: o que significa “não tentar novamente”

Uma entrada de erro possui um **escopo**. A IA deve bloquear a repetição do erro dentro desse escopo.

Escopos possíveis:

- `GLOBAL` — vale para qualquer tarefa futura do usuário.
- `PROJETO:<nome>` — vale para um projeto específico.
- `ASSUNTO:<tema>` — vale para um assunto ou categoria.
- `TECNOLOGIA:<stack>` — vale para determinada stack, versão ou ambiente.
- `ENTREGA:<tipo>` — vale para um tipo de saída, como legenda, interface, relatório, imagem ou prompt.
- `TEMPORARIO:<condição>` — vale enquanto uma condição específica existir.

Não transformar um caso local em regra global sem evidência. Se o usuário disser “nunca faça isso comigo”, use `GLOBAL`. Se disser “nesse projeto não use X”, use o projeto correspondente.

## Estados de uma entrada

- `ATIVO` — deve ser obedecido.
- `SUPERADO` — uma nova instrução, ambiente ou solução substituiu a regra antiga; manter para histórico.
- `EM_REVISAO` — há conflito ou evidência insuficiente.
- `ARQUIVADO` — não é mais aplicável, mas permanece para rastreabilidade.

Uma entrada `ATIVO` em `ERROS.md` não deve ser repetida no mesmo escopo. Caso uma nova instrução do usuário contradiga a entrada, a instrução atual prevalece e a IA deve marcar a entrada anterior como `SUPERADO`, apontando para a nova decisão.

## Protocolo obrigatório após feedback negativo

1. **Reconhecer o feedback:** identificar exatamente o que o usuário rejeitou ou informou que falhou.
2. **Classificar:** objetivo/técnico, preferência, interpretação, conteúdo, visual, processo ou outro.
3. **Definir o escopo:** global, projeto, assunto, tecnologia, entrega ou temporário.
4. **Registrar o erro:** adicionar entrada em `ERROS.md` com contexto suficiente para não repetir.
5. **Corrigir:** tentar uma abordagem diferente, sem reutilizar o padrão bloqueado.
6. **Validar:** obter confirmação do usuário ou evidência técnica quando possível.
7. **Registrar o sucesso:** quando houver solução confirmada, adicionar em `SUCESSOS.md` e relacionar ao erro.
8. **Reutilizar no futuro:** em tarefas equivalentes, priorizar o sucesso relacionado antes de inventar nova abordagem.

## Regra especial para código

Quando código, comando, configuração, arquitetura ou procedimento técnico estiver errado por causa da solução fornecida pela IA, o registro de erro deve conter, quando disponível:

- projeto/repositório e ambiente;
- linguagem, framework, versão ou plataforma relevante;
- objetivo original;
- tentativa que falhou;
- trecho mínimo ou padrão técnico que causou o erro, sem segredos;
- mensagem/sintoma do erro;
- causa raiz confirmada ou `DESCONHECIDA`;
- regra explícita `NÃO REPETIR`;
- condições em que o bloqueio vale;
- link/ID do sucesso que substituiu a tentativa;
- evidência de validação.

O arquivo não deve guardar senhas, tokens, cookies, chaves privadas, strings de conexão com segredo, códigos de recuperação ou qualquer credencial. Exemplos técnicos devem ser sanitizados.

## Feedback negativo em assuntos não técnicos

A mesma lógica vale fora de programação. Exemplos:

- usuário rejeita texto muito longo → registrar o formato rejeitado e, quando confirmado, o formato curto aprovado;
- usuário rejeita um estilo visual → registrar elementos rejeitados e a alternativa aprovada;
- usuário corrige uma interpretação → registrar a interpretação incorreta e a forma correta;
- usuário recusa uma recomendação por um critério específico → registrar o critério para não recomendar opções equivalentes no mesmo escopo;
- usuário diz que determinado fluxo de trabalho é inconveniente → registrar o fluxo rejeitado e o processo preferido.

## O que NÃO registrar

Não registrar como erro permanente:

- uma hipótese ainda não testada;
- simples diferença de opinião sem rejeição do usuário;
- falha causada exclusivamente por indisponibilidade temporária externa, salvo se houver lição reutilizável;
- conteúdo sensível, segredo ou credencial;
- afirmação sobre o usuário que não seja necessária para executar melhor suas tarefas.

## Conflitos e prioridade

Ordem de prioridade:

1. instrução atual e explícita do usuário;
2. regras de segurança, plataforma e permissões;
3. `ERROS.md` e `SUCESSOS.md` ativos no escopo correspondente;
4. demais memórias e decisões anteriores.

Quando dois sucessos conflitarem, use o mais recente e mais específico ao contexto. Quando um sucesso deixar de funcionar, registre o novo erro sem apagar o sucesso antigo; marque-o como `SUPERADO` ou limite seu escopo.

## Responsabilidade de cada IA

Cada IA continua registrando sua própria memória na sua pasta nominal. Porém, erros e sucessos **úteis para mais de uma IA** devem ser promovidos para este diretório compartilhado. A IA que detectou o feedback é responsável por registrar o aprendizado, desde que tenha permissão de escrita.

Se não puder gravar, deve informar a limitação e não fingir que o aprendizado foi persistido.
