# Protocolo de memória compartilhada

## Repositório e fronteira de escrita

O repositório autorizado é `https://github.com/AnderHonorato/Mem-rias-IA---Infinity`. A área exclusiva da Manus é `Manus/`. O script `scripts/sync_memory.py` confirma o `origin`, bloqueia caminhos fora de `Manus/`, redige padrões comuns de credenciais e pode atualizar, fazer commit e enviar somente essa árvore.

A pasta `Manus/` deve conter as instruções, catálogos, habilidades e memórias da Manus. As pastas de outras IAs são áreas de interoperabilidade e documentação; a Manus não deve escrever nelas sem uma solicitação explícita do usuário e sem preservar o formato definido por cada agente.

## Protocolo de início

1. Executar `git pull --ff-only origin HEAD` quando houver remote autenticado e a operação for permitida.
2. Ler `Manus/README.md` e `Manus/Memorias/INDEX.md`.
3. Ler o arquivo mensal mais recente em `Manus/Memorias/conversas/`.
4. Ler somente as categorias relacionadas ao pedido: `preferencias`, `projetos`, `decisoes`, `contexto`, `aprendizados`, `tarefas` ou `seguranca`.
5. Registrar um resumo mínimo do início, sem incluir segredos ou dados sensíveis desnecessários.

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
