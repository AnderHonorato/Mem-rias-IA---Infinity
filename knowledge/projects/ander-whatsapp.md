---
id: project-ander-whatsapp
status: em-desenvolvimento
scope: project/ander-whatsapp
sensitivity: personal
origin: trusted-user + agent-generated + observed-tool-results
confidence: high-for-implemented-code / provisional-for-whatsapp-compatibility
last_verified: 2026-10-08
supersedes: null
---
# Ander WhatsApp (plugin privado e ponte local)

## Objetivo confirmado
Acessar WhatsApp pessoal sem controlar a tela nem depender de WhatsApp Web visível: ler e pesquisar mensagens, baixar anexos recebidos, manter memória **local privada** do que foi sincronizado e enviar mensagens apenas quando o usuário pedir. O usuário gostaria de escrever "GPT" na conversa consigo mesmo e receber resposta do ChatGPT nesta mesma conversa de ChatGPT e de volta no WhatsApp, sem chave externa/API paga.

## Arquitetura observada
- Plugin ChatGPT privado criado via Plugin Creator: `https://chatgpt.com/plugins/plugins_6ac726bceca88191b2a1f395eb5b8258`. A versão publicada deve ser revalidada em cada edição.
- Ponte local Node.js/Baileys, sob `C:\Projetos\Andamento\Ander-WhatsApp` no PC autorizado; endpoint HTTP apenas em `127.0.0.1:41777`.
- Ferramenta Remote Desktop Commander acessa o PC para consultas e envios autorizados.
- Interface local com status, chats, login por chave local, QR e código de pareamento; o painel não está publicado na internet.
- Armazenamento local: `data/messages.jsonl`, `data/contacts.json`, `data/media/`, `data/gpt-commands.jsonl`; nunca versionar essa pasta nem segredos.
- `archive.mjs` registra mensagens deduplicadas e tenta baixar mídias normais (imagem/áudio/vídeo/documento/figurinha) com limites por tamanho e relatório de falha. Não arquiva payload de visualização única.
- `gpt-inbox.mjs` identifica comandos de texto começando com GPT apenas da conversa do próprio dono, enviados em tempo real, e os deixa numa fila local para consulta futura. Não envia respostas automáticas.

## Limite de plataforma importante
**Um plugin não consegue por si só inserir uma nova mensagem nesta conversa ChatGPT, acordar o assistente em tempo real, nem produzir respostas WhatsApp imediatas sem alguma execução/autorização de ChatGPT.** A fila local pode ser lida quando o usuário invocar o plugin nesta conversa. Para resposta autônoma imediata seria preciso um serviço/modelo executando fora da conversa (por exemplo API ou IA local), que o usuário não quer usar neste momento. Nunca prometer tal capacidade.

## Privacidade e segurança
- Mensagens reais e arquivos de terceiros: manter localmente, sem copiar para o repositório de memórias. Salvar no GitHub apenas arquitetura, decisões, resultados técnicos, bugs e próximos passos.
- Não publicar `data/auth`, chaves, QR, tokens, telefone e conteúdo de conversas.
- Integrador Baileys é NÃO oficial e sujeito a instabilidade/restrições da conta.
- Não responder a outras conversas automaticamente e não enviar nada sem pedido explícito. A conexão do PC precisa estar ativa.
- O arquivo JSONL local contém conteúdo pessoal sem criptografia em repouso; segurança adicional e política de retenção são pendências.

## Observações de testes e limitações
- Em 08/10/2026, pareamento confirmado; em versões anteriores havia mais de 10 mil registros e muitas mensagens sem payload original, porque apenas texto/placeholders haviam sido salvos.
- Download retroativo só é possível quando o WhatsApp disponibiliza novamente a mídia original; placeholders não contêm bytes recuperáveis.
- Novos testes sintéticos demonstraram parse de texto, deduplicação, exclusão de view-once e isolamento de comandos GPT; download real de mídia e resposta ChatGPT automática ainda não comprovados.
- A versão histórica de contatos/chats não garante o histórico completo ou ordenação perfeita de mensagens.

## Próximos passos
1. Validar chegada real de uma foto, áudio, vídeo e documento com usuário.
2. Comprovar recuperação/retomada de mídia, índice de anexos, permissões e reprocessamento de falhas.
3. Oferecer busca eficiente e retenção/backup seguro, opcionalmente com criptografia de arquivos.
4. Se o usuário quiser acesso ao painel fora de casa, configurar túnel autenticado, sem expor porta local.
5. Registrar cada decisão e teste significativo neste repositório conforme `AGENTS.md`.

## Revisão verificada em 2026-10-08
- Plugin privado atualizado e verificado na versão `0.3.0`, contendo instruções de consulta a anexos locais, fila `GPT` e protocolo de memória Flow.
- Ponte local após reinício: `paired:true`, `connection:conectado`; estatísticas locais ainda registravam **0 mídias efetivamente baixadas**, portanto download real ainda precisa ser testado com uma mídia nova.
- Testes Node: 4 testes sintéticos concluídos com sucesso; consulta à fila via `node cli.mjs gpt-commands` retornou lista vazia até receber novo comando válido.
- Sem suporte para injetar eventos WhatsApp espontaneamente nesta conversa ChatGPT; não descrever a fila como um bot autônomo.

## Monitoramento sem API (08/10/2026, 14h)
- Usuário solicitou que o próprio ChatGPT fosse acionado automaticamente por um comando `GPT` no WhatsApp, respondendo lá sem abrir o chat.
- Foi criada no ChatGPT a automação **Comandos GPT WhatsApp**, do tipo `condition_watch`, com verificação **a cada hora** da fila local por meio dos plugins quando disponíveis. Só notifica comandos pendentes; **não envia respostas pelo WhatsApp**.
- Essa solução não equivale a webhook nem gera resposta instantânea. A documentação do ChatGPT descreve eventos compatíveis via aplicativos suportados, não a injeção arbitrária de eventos do plugin nesta conversa.
- O código local do projeto recebeu estrutura adicional para estados de comandos; a tentativa de completar o envio automático via ferramenta de escrita foi bloqueada e **não pode ser considerada implementada**. O processo já em execução permaneceu conectado, mas não reiniciado para ativar novos endpoints.
- Testes estáticos/sintéticos verificados: 4/4 passaram; status operacional da ponte `conectado`; havia 1 comando `teste` na fila. Nenhuma resposta foi enviada.
- Não prometer que tarefas agendadas possuem acesso ao Remote Desktop Commander até comprovar o primeiro disparo. Alternativa de resposta imediata sem API externa seria um modelo local separado, mas **não é o mesmo ChatGPT desta conversa**.


## Atualização de requisitos e implementação — 08/10/2026 à noite

**Decisão posterior, substitui as regras históricas que limitavam o atendimento automático à conversa do próprio usuário.** O usuário autorizou Metrys a responder automaticamente a contatos individuais, preservando proteções de privacidade.

### Regras atuais
- A espera para contatos comuns foi reduzida de **15 para 10 minutos** desde a primeira mensagem não respondida pelo proprietário.
- O próprio usuário, ao enviar comandos começando em `GPT` para si mesmo, continua recebendo resposta sem atraso intencional (apenas o tempo de geração).
- Um contato prioritário explicitamente indicado recebe resposta sem espera; o número é **privado** e fica apenas em `data/attendant-config.json`, nunca neste repositório.
- Segunda a sexta, 07:30–16:30, e sábado, 08:00–12:00, horário de São Paulo: saudação informa que Ander está trabalhando. Fora dessas janelas informa que está ocupado.
- Metrys sempre se apresenta como assistente virtual criado por Ander e usa o prefixo `*Metrys:*\n` nas respostas. Não informa o fornecedor do modelo local a terceiros.
- Saudação oferece à pessoa aguardar Ander ou continuar com Metrys. Optando pela IA, respostas seguintes são imediatas e geradas localmente; preferindo Ander, Metrys não insiste. Resposta manual de Ander cancela pendências do contato.
- Grupos/canais/status excluídos. Nenhum acesso a conteúdos de outras conversas no prompt para um terceiro. Limite de 12 respostas automáticas por contato a cada hora para reduzir loops entre robôs.
- Cada envio revalida o destinatário e a tarefa elegível imediatamente antes de enviar. Respostas de resultado incerto não são repetidas automaticamente.

### Implementação técnica observada
- Novo módulo local `attendant.mjs` com estados privados persistentes, regras de horário, identificação de mensagens próprias e timeout configurável.
- A ponte `bridge.mjs` conecta eventos ao detector e expõe rotas locais autenticadas `/attendant/status`, `/attendant/tasks` e `/attendant/send`.
- O trabalhador `local-ai.mjs` consulta filas e gera o atendimento conversacional usando o Ollama instalado no PC, sob o nome de atendimento Metrys.
- Regras privadas `delaySeconds:600`, `immediateNumber`, `activatedAt` e `enabled` ficam fora do Git em `data/attendant-config.json`.
- Em execução no PC, a API retornou `/attendant/status: enabled=true, delaySeconds=600, pending=0`, conexão WhatsApp `paired=true` e IA local com estado `ativo`.
- **Testes sintéticos: 7/7 aprovados**, incluindo timeout, cancelamento por resposta manual, prioridade, exclusão de grupo e da conversa própria, fronteiras de horários e estado de comando.
- Proteção negativa validada: tentativa de enviar a uma conversa com tarefa não existente retornou HTTP 400 e não iniciou envio.
- **Pendente**: confirmar envio e cancelamento com contatos reais após a chegada de novas mensagens. Não alegar teste de entrega a destinatário real sem essa evidência.

### Privacidade
Todos os conteúdos de terceiros, números de telefone, arquivos pessoais, log de conversas, sessão e chaves permanecem apenas no PC privado. Memória Flow no GitHub registra somente regras técnicas, decisões e validações, conforme `AGENTS.md`. Modelos locais ainda podem produzir respostas incorretas; proteção de dados combina prompt, ausência de contexto privado e checagens de saída, sem garantia absoluta de segurança.
