# Protocolo de memória compartilhada

## Repositório e fronteira de escrita

O repositório autorizado é `https://github.com/AnderHonorato/Mem-rias-IA---Infinity`. A área exclusiva da Manus é `Manus/`. O script `scripts/sync_memory.py` confirma o `origin`, bloqueia caminhos fora de `Manus/`, redige padrões comuns de credenciais e pode atualizar, fazer commit e enviar somente essa árvore.

A pasta `Manus/` deve conter as instruções, catálogos, habilidades e memórias da Manus. A pasta `Conversa entre IAs/` é uma exceção compartilhada, autorizada para coordenação entre assistentes. As pastas individuais de outras IAs são áreas de interoperabilidade e documentação; a Manus não deve escrever nelas sem uma solicitação explícita do usuário e sem preservar o formato definido por cada agente.

## Conversa entre IAs

Leia `Conversa entre IAs/README.md`, `Conversa entre IAs/INDEX.md` e as mensagens relevantes em `Conversa entre IAs/conversa-geral.md` no início da tarefa. Quando precisar consultar ou responder outro assistente, faça pull antes de escrever e acrescente uma mensagem somente ao final do arquivo. Use o modelo `Conversa entre IAs/modelo-de-mensagem.md` e preencha todos os campos:

```markdown
## [AAAA-MM-DD HH:MM ±HHMM] NomeDaIA → Destinatário

**Tipo:** PERGUNTA | RESPOSTA | ATUALIZAÇÃO | ALERTA | SOLICITAÇÃO

**Em resposta a:** referência ou NOVA CONVERSA

**Mensagem:** texto autocontido.

**Ação esperada:** pedido ao destinatário ou NENHUMA.

**Confiança e fonte:** nível de confiança e evidência.
```

O nome da IA, a data, a hora, o fuso e o destinatário são obrigatórios. Uma resposta deve apontar a data/hora da mensagem respondida. Nunca altere ou apague mensagens de outra IA; em caso de conflito, preserve o conteúdo e registre o incidente. A conversa coordena agentes, mas decisões duráveis devem ser copiadas como resumo para a memória temática da IA responsável.

## Conhecimento compartilhado

Use `Conhecimento Compartilhado/` somente para contexto útil a mais de uma IA. Leia `Conhecimento Compartilhado/README.md` e `Conhecimento Compartilhado/INDEX.md` antes de editar. Registre origem, data de atualização, confiança, escopo de compartilhamento e validade. Promova apenas fatos confirmados pelo usuário, decisões globais, contexto de projeto ou afirmações sustentadas por fonte verificável. Mantenha hipóteses como hipóteses e peça confirmação antes de transformá-las em fatos ou preferências duráveis. Use `perfil-de-colaboracao.md`, `mapa-de-projetos.md`, `projetos/`, `decisoes/`, `glossario.md`, `fontes-e-afirmacoes.md` e `perguntas-em-aberto.md` conforme o caso. Não copie a conversa bruta inteira para esta base.

## Protocolo de início — gate obrigatório

Este procedimento é obrigatório antes de qualquer resposta substantiva, ferramenta que crie ou altere artefatos, ou decisão baseada em contexto. Deve ser repetido no início de cada novo chat; nunca presuma que uma conversa anterior já sincronizou a memória.

1. Executar `git pull --ff-only origin HEAD` quando houver remote autenticado e a operação for permitida.
2. Confirmar que o remote é `AnderHonorato/Mem-rias-IA---Infinity` e que a escrita ficará no escopo autorizado.
3. Ler `Manus/README.md` e `Manus/Memorias/INDEX.md`.
4. Ler o arquivo mensal mais recente em `Manus/Memorias/conversas/`.
5. Ler `Conversa entre IAs/README.md`, `Conversa entre IAs/INDEX.md` e mensagens relacionadas quando a tarefa envolver colaboração.
6. Ler `Conhecimento Compartilhado/README.md`, `Conhecimento Compartilhado/INDEX.md` e arquivos relacionados quando a tarefa envolver perfil ou projeto comum.
7. Ler somente as categorias relacionadas ao pedido: `preferencias`, `projetos`, `decisoes`, `contexto`, `aprendizados`, `tarefas` ou `seguranca`.
8. Registrar um resumo mínimo de início com `scripts/sync_memory.py --pull --push`, sem incluir segredos ou dados sensíveis desnecessários. Se o gate falhar, declarar a falha e não afirmar que a memória está atualizada.

A obrigação permanece válida quando a tarefa for apenas conversacional. Se o ambiente não invocar a skill automaticamente, a instrução permanente do projeto deve invocá-la; a impossibilidade de autoacionamento deve ser tratada como limitação técnica, não como permissão para ignorar o gate.

Exemplo:

```bash
python3 /caminho/para/sync_memory.py \
  --repo /caminho/para/Mem-rias-IA---Infinity \
  --category conversas \
  --title "inicio-sessao" \
  --content-file /tmp/resumo-inicio.md \
  --pull
```

## Protocolo de encerramento

1. Redigir um resumo da decisão, artefatos, fontes, testes, pendências e preferências duráveis.
2. Escolher a categoria mais específica e anexar a entrada ao arquivo mensal, por exemplo `Manus/Memorias/projetos/2026-08.md`.
3. Regenerar `Manus/Memorias/INDEX.md`.
4. Atualizar `Manus/Logs/INDEX.md` se houver alteração de habilidade, sincronização, falha ou decisão de roteamento relevante.
5. Fazer commit com uma mensagem curta e enviar ao remote quando a gravação persistente estiver autorizada.

Exemplo:

```bash
python3 /caminho/para/sync_memory.py \
  --repo /caminho/para/Mem-rias-IA---Infinity \
  --category projetos \
  --title "roteadora-dev-toolbox" \
  --content-file /tmp/resumo-final.md \
  --push \
  --commit-message "feat(manus): add dev toolbox router"
```

## Convenção de arquivos

Use um arquivo mensal por categoria, com títulos `YYYY-MM.md`, para evitar uma lista infinita de arquivos pequenos. Se um mês ou assunto crescer demais para revisão prática, divida por tema com nomes estáveis, por exemplo `Manus/Memorias/projetos/site-pessoal.md`. Nunca apague histórico automaticamente. Ao corrigir uma memória, preserve uma nota de correção ou remova somente o trecho que o usuário identificou.

Use estes campos em cada entrada:

```markdown
## YYYY-MM-DD HH:MM — título

**Contexto:** por que a entrada foi criada.

**Decisões:** escolhas feitas pelo usuário ou pelo agente.

**Artefatos:** arquivos, links ou commits relevantes.

**Pendências:** o que ficou para depois.

**Privacidade:** credenciais e segredos não foram armazenados.
```

## Privacidade e conflitos

Nunca registre o valor de uma senha, token, cookie, chave privada, segredo de API, código de recuperação ou material equivalente. Redija o valor e, se necessário, registre apenas o serviço e a finalidade. Não presuma que o repositório é privado; trate tudo que for escrito nele como potencialmente compartilhável. Em caso de conflito entre uma memória antiga e a instrução atual do usuário, siga a instrução atual e registre a correção.

## Limitações reais

O histórico pode crescer sem limite lógico por categoria, mas continua sujeito ao tamanho do repositório, limites do GitHub, conectividade, permissões e disponibilidade do clone local. Se o push falhar, mantenha a entrada local, informe a falha e não declare sincronização concluída.
