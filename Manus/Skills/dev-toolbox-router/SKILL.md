---
name: dev-toolbox-router
description: "Roteia tarefas de programação, design, full stack, bancos de dados, segurança e desenvolvimento de jogos para o workflow e a skill mínima adequados, mantendo contexto persistente no repositório GitHub Memórias IA - Infinity. Use no início de qualquer tarefa técnica, quando for necessário recuperar ou registrar contexto, selecionar uma habilidade especializada ou organizar habilidades de IA."
---

# Dev Toolbox Router

Use esta skill como ponto de entrada para tarefas técnicas. Classifique a solicitação, consulte a memória compartilhada, selecione somente as habilidades necessárias e registre o contexto útil ao final.

## Regra de memória — executar primeiro e por último

No início de toda conversa, inclusive bate-papo casual, pergunta simples ou assunto completamente alheio à memória, execute o gate universal: valide o remote autorizado, carregue o Git, leia `Manus/README.md`, `Manus/Memorias/INDEX.md` e o arquivo mensal mais recente em `Manus/Memorias/conversas/`. O carregamento e a consulta do Git são obrigatórios e não dependem do tema; leia categorias adicionais apenas quando forem necessárias ao assunto. Em conversa casual, não crie uma entrada artificial se não houver contexto novo, mas ainda assim carregue e consulte o Git. Leia também `Manus/Skills/catalog.md` quando precisar escolher uma skill externa. Nunca procure ou grave memórias fora do repositório `AnderHonorato/Mem-rias-IA---Infinity` e nunca grave arquivos da Manus fora de `Manus/`.

Antes da primeira resposta substantiva, sincronize o repositório e registre um início de sessão usando `scripts/sync_memory.py`. Se a sincronização falhar, informe a limitação, continue sem inventar memórias e tente registrar o resultado ao final. A memória deve ser persistente e expansível por arquivos Markdown temáticos; “infinita” significa não impor um limite artificial de histórico, não significa ignorar limites de armazenamento, permissões ou tamanho do Git.

Ao concluir a tarefa, registre em Markdown, dentro de `Manus/Memorias/`, o resumo do que foi decidido, artefatos criados, preferências duráveis, fontes utilizadas e pendências. Atualize `Manus/Memorias/INDEX.md` e `Manus/Logs/INDEX.md` quando aplicável. Salve habilidades e catálogos somente em `Manus/Skills/`. Nunca salve senhas, tokens, chaves privadas, cookies, códigos de recuperação ou credenciais; registre apenas que uma credencial foi necessária, sem seu valor. Não copie automaticamente dados pessoais sensíveis quando eles não forem necessários para a continuidade da tarefa.

Consulte [memory-protocol.md](references/memory-protocol.md) para o formato de sessão, comandos de sincronização e convenções de arquivos.

## Roteamento em quatro passos

1. **Classificar a tarefa.** Determine o domínio primário e, se necessário, um domínio secundário. Não escolha por palavra isolada: considere objetivo, artefato, stack, ambiente e risco.
2. **Escolher o menor conjunto suficiente.** Leia o item correspondente em [routing-matrix.md](references/routing-matrix.md). Prefira uma skill oficial ou de repositório mantido, combinada com uma skill de verificação quando houver código, dados, segurança ou publicação.
3. **Verificar dependências e riscos.** Confirme se a skill depende de API, conector, credencial, engine, banco, pacote ou comando externo. Não habilite conectores nem execute publicação, exclusão, migração, fuzzing ativo ou alteração de produção sem autorização explícita e as confirmações exigidas pelo ambiente.
4. **Executar e verificar.** Siga a skill selecionada, valide o resultado com testes, inspeção ou evidência equivalente e registre a decisão. Se mais de uma skill puder atender, explique a escolha e evite carregar instruções redundantes.

## Matriz rápida

| Domínio | Sinais de entrada | Primeira referência | Verificação recomendada |
|---|---|---|---|
| Programação | feature, bug, refatoração, testes, revisão, Git | `test-driven-development`, `systematic-debugging`, `react-best-practices` | `verification-before-completion` ou `webapp-testing` |
| Design | interface, layout, identidade, acessibilidade, tokens, Figma | `frontend-design`, `web-design-guidelines`, `anydesign` | `canvas-design` ou revisão visual |
| Full stack | frontend + backend, API, deploy, auth, MCP, CI/CD | `web-artifacts-builder`, `mcp-builder`, `software-architecture` | `webapp-testing`, `playwright-skill`, `deploy-to-vercel` |
| Banco e dados | SQL, schema, migração, exploração, CSV, análise | `postgres`, `database-lookup`, `exploratory-data-analysis` | skill de análise/validação e modo somente leitura por padrão |
| Segurança | vulnerabilidade, threat hunting, fuzzing, forense, auditoria | `security-audit`, `ffuf-skill`, `computer-forensics` | relatório com escopo, evidência, impacto e correção; sem exploração não autorizada |
| Jogos | engine, gameplay, protótipo, level design, assets, playtest | roteador de `awesome-gamedev-agent-skills` ou `Claude-Code-Game-Studios` | `prototype-fast`, `smoke-check`, `security-audit` quando houver rede/saves |

## Regras por domínio

### Programação e full stack

Entenda o repositório antes de editar. Para funcionalidade nova ou correção, escreva ou atualize testes antes da implementação quando a stack permitir. Para aplicações web, identifique framework, package manager, comandos de build, lint e testes. Para deploy, prefira preview e não produção, a menos que o usuário peça produção de forma inequívoca.

### Design

Preserve o sistema visual existente quando houver um. Verifique hierarquia, estados, responsividade, acessibilidade e consistência antes de sugerir mudanças. Para reconstruir uma interface a partir de imagem, URL ou arquivo Figma, leia o workflow `anydesign` e seus formatos de saída antes de gerar código.

### Banco e dados

Comece por operações de leitura e inspeção de schema. Não execute INSERT, UPDATE, DELETE, DROP, ALTER, migração ou alteração de permissões sem pedido explícito, plano de reversão e confirmação. Mantenha credenciais em arquivos locais protegidos ou variáveis de ambiente; nunca as copie para a memória compartilhada.

### Segurança

Defina escopo, autorização, alvo e janela de teste antes de qualquer ação ativa. Priorize análise passiva, evidência reproduzível e correções defensivas. Não transforme uma skill de auditoria em autorização para explorar terceiros, interromper serviços, coletar segredos ou alterar sistemas.

### Jogos

Detecte a engine e sua versão, escolha uma skill específica e mantenha o protótipo pequeno. Para ideias novas, use `prototype-fast` e produza um veredito claro; para produção, use o workflow de engine, testes e gates apropriados. Não misture as skills de game dev em cada tarefa: carregue apenas engine, disciplina e workflow relevantes.

## Formato de resposta e encerramento

Explique em uma frase qual domínio foi selecionado e por quê. Entregue o artefato ou resultado com os testes realizados e as limitações conhecidas. Ao encerrar, escreva a memória da sessão na categoria mais específica e acrescente uma linha no índice. Se o usuário pedir para esquecer ou corrigir uma memória, trate isso como uma operação explícita de edição e remova ou revise somente o conteúdo indicado.

## Quando não usar

Não use esta skill como substituta de autenticação, conector, banco de dados ou ferramenta de execução. Ela define o workflow; os acessos e ações devem ocorrer por ferramentas autorizadas e pelas skills especializadas correspondentes.
