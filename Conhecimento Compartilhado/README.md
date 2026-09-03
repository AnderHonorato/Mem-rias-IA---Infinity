# Conhecimento Compartilhado

Esta pasta contém o contexto que pode ser útil para todas as IAs: perfil de colaboração do usuário, mapa dos projetos, decisões globais e aprendizado confirmado por feedback. Ela é diferente de `Conversa entre IAs/`: a conversa é um mural de coordenação; esta pasta é uma base curada e resumida.

## Princípios

Registre apenas informações necessárias para melhorar o atendimento ao usuário e a execução dos projetos. Toda entrada deve indicar **origem**, **data de atualização**, **nível de confiança**, **escopo de compartilhamento** e, quando apropriado, **validade**. Preferências ou fatos sobre o usuário só devem ser promovidos para esta pasta quando forem declarados pelo usuário ou confirmados em mais de uma interação. Hipóteses de uma IA devem permanecer marcadas como hipóteses.

Não armazene senhas, tokens, cookies, chaves privadas, códigos de recuperação, dados financeiros completos, documentos de identidade ou informações pessoais sensíveis que não sejam indispensáveis. Para dados sensíveis, prefira registrar uma referência redigida ou o local seguro onde o dado é mantido, sem copiar o valor.

## Arquivos recomendados

| Arquivo | Conteúdo |
|---|---|
| `perfil-de-colaboracao.md` | Preferências de comunicação, objetivos, ferramentas, restrições e estilo de trabalho confirmados. |
| `mapa-de-projetos.md` | Índice de projetos, estado, stack, repositório, objetivo e próximos marcos. |
| `projetos/<slug>.md` | Ficha detalhada de cada projeto compartilhado. |
| `decisoes/<slug>.md` | Decisões globais, alternativas rejeitadas, motivo e data de revisão. |
| `glossario.md` | Termos, nomes e abreviações específicos do usuário ou dos projetos. |
| `fontes-e-afirmacoes.md` | Afirmações técnicas ou de negócio com fonte, data e grau de verificação. |
| `perguntas-em-aberto.md` | Questões que uma IA pode investigar ou encaminhar a outra. |
| `aprendizado-por-feedback/` | Erros bloqueados, sucessos confirmados, protocolo e casos de uso compartilhados entre todas as IAs. |
| `INDEX.md` | Índice de todos os arquivos curados. |

## Aprendizado por feedback

O diretório `aprendizado-por-feedback/` é obrigatório para todas as IAs que utilizam este repositório. Ele existe para impedir que um caminho já informado como errado seja repetido e para fazer uma solução confirmada virar referência preferencial.

Fluxo resumido:

1. feedback negativo reutilizável → registrar em `aprendizado-por-feedback/ERROS.md`;
2. definir o escopo da proibição de repetição;
3. tentar uma abordagem diferente;
4. solução aprovada ou tecnicamente validada → registrar em `aprendizado-por-feedback/SUCESSOS.md`;
5. ligar o erro ao sucesso pelo ID;
6. antes de repetir tarefa semelhante, consultar ambos os registros.

O protocolo completo, incluindo estados (`ATIVO`, `SUPERADO`, `EM_REVISAO`, `ARQUIVADO`), tratamento de código, mudanças de preferência, falhas temporárias e exemplos não técnicos, está em `aprendizado-por-feedback/README.md` e `CASOS-DE-USO.md`.

## Fluxo de atualização

1. Leia `README.md`, `INDEX.md` e o arquivo relevante antes de propor uma mudança.
2. Se a tarefa já teve tentativa rejeitada ou solução confirmada, consulte também `aprendizado-por-feedback/INDEX.md`, `ERROS.md` e `SUCESSOS.md` nas entradas do mesmo escopo.
3. Separe fato, decisão, preferência, hipótese, erro, sucesso e pendência.
4. Solicite confirmação ao usuário para transformar hipótese em fato ou para registrar uma preferência pessoal durável quando isso não estiver explícito.
5. Feedback negativo explícito do usuário pode ser registrado como erro sem nova confirmação, desde que o escopo não seja ampliado além do que ele informou.
6. Faça a atualização mínima, preserve histórico relevante e altere `atualizado-em`.
7. Publique uma nota na `Conversa entre IAs/` quando a mudança exigir coordenação.

A instrução atual do usuário prevalece sobre qualquer conteúdo desta pasta. Se houver conflito, marque a entrada como `CONFLITO` ou `EM_REVISAO`, preserve o histórico e não faça uma alteração irreversível por conta própria.
