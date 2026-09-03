# Interação — melhoria do sistema de memórias por feedback

**Data:** 2026-09-03  
**IA:** GPT-5.6 Sol  
**Usuário:** Ander

## Resumo

Ander solicitou uma evolução global do repositório Memórias IA — Infinity para que erros e acertos deixem de ser apenas correções locais da conversa e passem a formar um aprendizado persistente reutilizável por todas as IAs.

A regra solicitada é: quando uma IA fornecer código ou outro caminho que esteja errado e o usuário indicar o erro, o caminho rejeitado deve ser registrado em um arquivo de erros com instrução para não ser repetido no mesmo escopo. Quando outra abordagem funcionar ou for aprovada, ela deve ser registrada em um arquivo de sucessos como referência correta. A mesma lógica deve valer para feedback negativo em assuntos não técnicos, com detalhes, casos de uso e exemplos.

## Implementação nesta interação

Foi criada a branch `feat/aprendizado-por-feedback` e iniciada a integração do protocolo em `Conhecimento Compartilhado/aprendizado-por-feedback/`, incluindo:

- `README.md` com protocolo, gatilhos, escopo, estados, segurança e fluxo de validação;
- `ERROS.md` com modelo de entrada e regra `NÃO REPETIR`;
- `SUCESSOS.md` com modelo de solução confirmada e reutilização;
- `CASOS-DE-USO.md` com exemplos técnicos e não técnicos;
- `INDEX.md` para descoberta rápida;
- integração no README raiz e em `Conhecimento Compartilhado/`;
- reforço específico em `GPT/README.md`, `GPT/INDEX.md` e `GPT/Decisoes/aprendizado-por-feedback.md`.

## Síntese segura do raciocínio útil

A principal decisão foi separar o conceito de “não repetir” por **escopo**, evitando transformar um erro de um projeto ou versão em proibição universal. Entradas permanecem históricas e podem ser marcadas como `SUPERADO` se Ander mudar de preferência ou o ambiente mudar. Instruções atuais do usuário e regras de segurança sempre prevalecem.

## Pendência ao criar este registro

Concluir a propagação e revisão da documentação, validar o diff, abrir PR e integrar a mudança na branch principal se os checks permitirem.
