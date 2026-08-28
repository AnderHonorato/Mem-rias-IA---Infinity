# Conhecimento Compartilhado

Esta pasta contém o contexto que pode ser útil para todas as IAs: perfil de colaboração do usuário, mapa dos projetos e decisões globais. Ela é diferente de `Conversa entre IAs/`: a conversa é um mural de coordenação; esta pasta é uma base curada e resumida.

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
| `INDEX.md` | Índice de todos os arquivos curados. |

## Fluxo de atualização

1. Leia `README.md`, `INDEX.md` e o arquivo relevante antes de propor uma mudança.
2. Separe fato, decisão, preferência, hipótese e pendência.
3. Solicite confirmação ao usuário para transformar hipótese em fato ou para registrar uma preferência pessoal durável.
4. Faça a atualização mínima, preserve histórico relevante e altere `atualizado-em`.
5. Publique uma nota na `Conversa entre IAs/` quando a mudança exigir coordenação.

A instrução atual do usuário prevalece sobre qualquer conteúdo desta pasta. Se houver conflito, marque a entrada como `CONFLITO`, peça confirmação e não faça uma alteração irreversível por conta própria.
