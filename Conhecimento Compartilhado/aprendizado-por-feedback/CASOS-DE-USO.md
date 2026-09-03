# Casos de uso do aprendizado por feedback

Os exemplos abaixo são didáticos. Eles mostram como transformar feedback negativo em memória operacional sem exagerar o escopo.

## 1. Código: abordagem técnica falhou e outra funcionou

### Situação
A IA fornece uma configuração para autenticação. O usuário testa e informa que o login quebra. Depois, uma configuração diferente funciona.

### Registrar em ERROS
- Escopo: `PROJETO:exemplo-app`
- Tentativa errada: usar middleware X nessa versão do framework.
- Sintoma: redirecionamento em loop após login.
- Causa raiz: incompatibilidade com a versão instalada.
- NÃO REPETIR: não usar middleware X nesse projeto enquanto permanecer nessa versão.
- Solução substituta: apontar para o `SUC-ID` correspondente.

### Registrar em SUCESSOS
- Solução correta: estratégia Y compatível com a versão atual.
- Evidência: teste de login aprovado pelo usuário.
- Como reutilizar: priorizar Y em futuras alterações de autenticação no mesmo projeto.

## 2. Código: comando destrutivo ou inadequado

### Situação
A IA sugere recriar banco de dados para corrigir migração. O usuário informa que isso apagaria dados e rejeita o caminho. Uma migração incremental resolve.

### Aprendizado
O erro deve bloquear a abordagem destrutiva dentro daquele projeto. O sucesso registra a migração incremental. Não generalizar para dizer que recriar banco é sempre proibido em qualquer ambiente; o escopo pode ser `PROJETO:<nome>` ou `AMBIENTE:produção`.

## 3. Front-end: estilo visual rejeitado

### Situação
A IA cria botões com emojis e visual 3D. O usuário rejeita ambos e aprova ícones SVG originais com visual plano.

### ERRO
- Escopo: `ENTREGA:interfaces`
- NÃO REPETIR: emojis de navegador como ícones de botão e componentes 3D quando o usuário pedir a mesma linguagem visual.

### SUCESSO
- Priorizar SVG original, interface plana e animações coerentes com o design aprovado.

Se o usuário disser que essa regra vale para todos os projetos futuros, promover o escopo para `GLOBAL`.

## 4. Escrita: resposta longa rejeitada

### Situação
O usuário pede uma resposta simples e recebe vários parágrafos. Ele diz que ficou grande demais. Uma segunda resposta curta é aprovada.

### ERRO
- Escopo: `ENTREGA:resposta curta` ou `GLOBAL`, somente se o usuário afirmar preferência geral.
- NÃO REPETIR: expandir desnecessariamente pedidos simples nesse escopo.

### SUCESSO
- Resposta direta, com somente o essencial e detalhes extras apenas quando necessários.

## 5. Escrita: tom errado

### Situação
A IA escreve uma mensagem de cliente em tom casual. O usuário informa que precisa ser mais sério. A versão profissional é aprovada.

### Aprendizado
Registrar o tom casual como rejeitado apenas para `ENTREGA:mensagem para cliente`, salvo se o usuário disser que prefere tom sério em tudo.

## 6. Pesquisa/recomendação: critério ignorado

### Situação
O usuário pede opções gratuitas. A IA recomenda uma ferramenta paga. O usuário rejeita. Outra ferramenta gratuita atende.

### ERRO
- Objetivo original: recomendar opções gratuitas.
- NÃO REPETIR: incluir alternativas exclusivamente pagas quando “gratuito” for requisito obrigatório.

### SUCESSO
- Priorizar opções realmente gratuitas e informar limitações do plano gratuito.

## 7. Interpretação: entendimento incorreto do pedido

### Situação
O usuário pede para editar um projeto existente e a IA começa a propor outro do zero. O usuário corrige.

### ERRO
- Escopo: `PROJETO:<nome>` ou `ASSUNTO:edição de projeto existente`.
- NÃO REPETIR: substituir o projeto atual quando o pedido for evoluir/preservar o existente.

### SUCESSO
- Auditar o projeto atual, preservar o que funciona e modificar incrementalmente.

## 8. Imagem/design: composição rejeitada

### Situação
O usuário pede edição mantendo a estrutura original. A IA muda enquadramento, pose ou elementos não solicitados. O usuário rejeita.

### ERRO
- NÃO REPETIR: alterações estruturais não solicitadas quando o escopo exigir preservação da composição.

### SUCESSO
- Alterar apenas os elementos pedidos e preservar enquadramento/estrutura restantes.

## 9. Processo de trabalho: ferramenta ou fluxo inconveniente

### Situação
A IA pede que o usuário faça manualmente várias etapas que poderiam ser executadas por uma ferramenta conectada. O usuário informa que quer execução direta.

### ERRO
- Escopo: tipo de tarefa com a ferramenta disponível.
- NÃO REPETIR: transferir ao usuário trabalho que a IA já pode executar com permissão.

### SUCESSO
- Usar a ferramenta adequada e reportar o que foi realmente executado.

## 10. Preferência muda com o tempo

### Situação
Em janeiro o usuário prefere abordagem A. Em setembro, ele diz explicitamente que agora prefere B.

### Procedimento
1. Marcar o sucesso A como `SUPERADO`.
2. Se A agora for indesejado, atualizar ou criar erro correspondente com o novo escopo.
3. Criar sucesso B com a data atual.
4. Nunca apagar o histórico apenas para esconder a mudança.
5. Em tarefas futuras, usar B.

## 11. Falha temporária externa

### Situação
Uma API externa fica fora do ar e o comando falha, mas o mesmo comando é tecnicamente correto.

### Não registrar como “nunca repetir” automaticamente
A falha foi externa e temporária. Só criar entrada se houver uma lição reutilizável, como necessidade de retry, fallback ou verificação de disponibilidade.

## 12. Usuário rejeita sem indicar alternativa

### Situação
O usuário diz apenas “não gostei”.

### Procedimento
Registrar o elemento claramente rejeitado somente se ele puder ser identificado sem adivinhação. Não inventar a causa. A entrada pode ter `Causa raiz: DESCONHECIDA` e ficar sem sucesso relacionado até existir uma alternativa confirmada.

## 13. Uma solução funcionou uma vez, mas falhou depois

Não apagar o sucesso antigo. Criar novo erro com data, ambiente e mudança relevante. Marcar o sucesso anterior como `SUPERADO` ou limitar sua validade. Isso permite entender regressões e mudanças de versão.

## 14. Feedback entre IAs

Se uma IA encontra uma entrada de erro criada por outra IA, ela deve tratá-la como regra operacional compartilhada quando:

- estado = `ATIVO`;
- escopo corresponde à tarefa atual;
- não existe instrução mais recente do usuário que a contradiga.

A IA não deve repetir o erro apenas para “testar de novo”, salvo quando o usuário pedir explicitamente nova tentativa, quando o ambiente tiver mudado de forma relevante ou quando a entrada estiver `EM_REVISAO`.
