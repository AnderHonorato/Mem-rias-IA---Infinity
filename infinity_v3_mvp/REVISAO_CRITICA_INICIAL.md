# Parecer crítico — Infinity V3, Etapa 3

**Status de testes:** 68 testes unitários locais aprovados na fase 3 (dados sintéticos); o GitHub Actions precisa executar o mesmo conjunto antes de aceitar merge.

## Avanços comprovados

- Busca na V2 somente-leitura: índice FTS5 criado em RAM sem tocar nos arquivos originais, exclusão automática de `personal`/`restricted`, expirados, arquivados e disputados.
- Fusor de contexto RRF limitado por tamanho, com `fonte`, `id` e indicação explícita de dado não confiável.
- Sessões locais bloqueiam acesso a outros escopos, exigem revisão e permissões para exclusão.
- Motor registra hash da justificativa, rejeita alguns padrões de credenciais e normaliza validade para UTC.
- Cache só é usado com marcação explícita de conteúdo público. Roteador não usa modelo sem conexão, consentimento, custo e escopo permitido.
- CLI read-only e benchmark sintético. Nenhum segredo ou memória real foi carregado nos testes.
- 12 papéis e 6 revisores definidos em catálogo; tarefas de alto risco exigem dois críticos cadastrados.
- Ferramentas com allowlist, modo simulação, confirmação de uso único e autorização para operações destrutivas.
- Registro de metadados operacionais com HMAC para detectar alterações retroativas. Não persistimos entradas e saídas da tarefa.
- Orquestrador paralelo de callbacks locais, com dependências e retorno na ordem original. Críticos recebem cópias profundas das saídas.
- Confirmações de escrita consumidas atomicamente entre threads; validação dos IDs de auditoria antes da execução.

## Bloqueadores do merge / produção

- **Autenticação ausente:** `SessaoMemoria` é uma fachada para código já confiável, não prova a identidade de quem chama. O motor bruto pode ser acessado pelo mesmo processo.
- **Criptografia ausente:** SQLite local está em texto claro. chmod 0600 restringe permissões POSIX, mas não protege o disco/backups nem todos os arquivos temporários.
- **PII incompleta:** regex são um primeiro filtro, não reconhecimento completo de dados pessoais ou prompt injection. Conteúdo de memória segue não confiável.
- **Exclusão parcial:** remoção local não alcança cópias remotas, backups e histórico do Git.
- **Sem agentes de IA reais:** o catálogo de papéis, a supervisão e os orquestradores (sequencial/paralelo) usam funções Python e críticos callback. A existência de duas revisões não garante modelos distintos. Nenhum modelo foi executado nesta fase.
- **Sem conector externo real:** o gateway de ferramentas recebe callbacks do host, mas não tem conexões com ChatGPT, GitHub, Drive ou provedores de IA em produção. Tokens de confirmação não substituem autenticação de rede.
- **Auditoria não forense:** HMAC local detecta alterações dos registros presentes, mas exige proteção de chave, política de backups, controle entre processos e âncora externa para detectar truncamentos completos.
- **Paralelismo condicionado:** callbacks devem ser thread-safe, não devem compartilhar uma conexão SQLite entre threads, e chamadas de rede devem usar limites apropriados do host.
- **Sem embeddings reais:** a combinação atual é FTS5 + RRF; "híbrido" semântico exige embeddings e avaliação separada.
- **Sem mensuração real do ChatGPT:** benchmark mede biblioteca local, não tempo de resposta, tokens ou custos do ChatGPT.
- **Fonte V2 preservada:** ainda não existe promoção V3 -> V2 automática ou alteração de arquivos privados.

**Recomendação dos críticos:** aprovar para desenvolvimento experimental isolado. Manter PR como rascunho até implementar autenticação, segurança, auditoria de privacidade e teste de integração completo.
