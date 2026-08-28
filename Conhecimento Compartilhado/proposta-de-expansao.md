# Proposta de expansão do conhecimento compartilhado

A melhor evolução é separar **coordenação**, **memória individual** e **conhecimento curado**. Isso evita que uma hipótese de uma IA vire fato global e permite que cada projeto tenha contexto suficiente sem transformar o repositório em uma cópia indiscriminada de todas as conversas.

## Camadas recomendadas

| Camada | Arquivo/pasta | Objetivo | Estado |
|---|---|---|---|
| Coordenação | `Conversa entre IAs/` | Perguntas, respostas, alertas e encaminhamentos entre IAs. | Implementada |
| Perfil | `Conhecimento Compartilhado/perfil-de-colaboracao.md` | Preferências de comunicação e trabalho confirmadas pelo usuário. | Implementada, inicial |
| Portfólio | `Conhecimento Compartilhado/mapa-de-projetos.md` | Lista de projetos, estado, stack, repositório e próximo marco. | Implementada, inicial |
| Fichas | `Conhecimento Compartilhado/projetos/<slug>.md` | Contexto detalhado por projeto. | Pronta para uso |
| Decisões | `Conhecimento Compartilhado/decisoes/<slug>.md` | Decisões, alternativas, motivo e data de revisão. | Pronta para uso |
| Evidências | `Conhecimento Compartilhado/fontes-e-afirmacoes.md` | Fonte e confiança para fatos reutilizáveis. | Implementada, inicial |
| Vocabulário | `Conhecimento Compartilhado/glossario.md` | Nomes e termos específicos. | Implementada, inicial |
| Pendências | `Conhecimento Compartilhado/perguntas-em-aberto.md` | Dúvidas encaminhadas entre IAs ou ao usuário. | Implementada, inicial |

## O que vale adicionar primeiro

### 1. Perfil de colaboração

Registrar somente preferências confirmadas: idioma, nível de detalhe, formato de resposta, tecnologias preferidas, tolerância a risco, modo de revisão, ferramentas autorizadas, fuso de referência e política de publicação. Cada item deve ter origem, data e confiança. Preferências antigas devem poder ser substituídas sem apagar o motivo da correção.

### 2. Ficha de projeto

Para cada projeto, manter objetivo, problema, público, escopo, não-escopo, estado, stack, ambiente, repositório, convenções, arquitetura, decisões, artefatos, riscos, dependências, testes, backlog e próximo marco. O campo `não-escopo` é importante para impedir que uma IA aumente o projeto sem autorização.

### 3. Registro de decisões

Guardar a decisão, data, participantes, alternativas consideradas, motivo, impacto, como reverter e quando revisar. Isso evita que outra IA repita uma opção já rejeitada ou contradiga uma escolha técnica sem perceber.

### 4. Fonte e confiança

Distinguir `fato confirmado pelo usuário`, `fato observado em arquivo`, `fato apoiado por fonte externa`, `hipótese`, `recomendação` e `decisão`. Assim, as IAs podem compartilhar conhecimento sem confundir opinião com verdade.

### 5. Perguntas e handoffs

Usar uma fila de perguntas em aberto com responsável, destinatário, prazo, estado e referência à conversa. Uma IA pode deixar uma investigação para outra sem perder o contexto nem duplicar trabalho.

### 6. Privacidade e consentimento

Adicionar uma lista explícita do que o usuário permite armazenar, do que deve ser redigido e do que deve ser esquecido. A regra padrão deve ser minimização: guardar somente o que melhora uma tarefa futura e nunca armazenar segredos ou dados sensíveis desnecessários.

## Melhorias posteriores

Quando o volume crescer, adicionar tags controladas, status de validade, data de revisão, links entre decisões e projetos, changelog da memória e uma rotina de detecção de contradições. Também é possível criar um resumo mensal, mas ele deve ser derivado dos arquivos temáticos e não substituir o histórico original.

Não recomendo salvar a conversa bruta inteira de todas as plataformas como conhecimento global. O formato mais útil é um resumo curado com origem e confiança, complementado pelo mural de conversa entre IAs. Isso aumenta a continuidade sem criar ruído, duplicação e exposição desnecessária.
