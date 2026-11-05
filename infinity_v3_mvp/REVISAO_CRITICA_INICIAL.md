# Parecer crítico — Infinity V3, Etapa 2

**Status de testes:** 47 testes unitários locais aprovados na fase 2 (dados sintéticos); o GitHub Actions precisa executar o mesmo conjunto antes de aceitar merge.

## Avanços comprovados

- Busca na V2 somente-leitura: índice FTS5 criado em RAM sem tocar nos arquivos originais, exclusão automática de `personal`/`restricted`, expirados, arquivados e disputados.
- Fusor de contexto RRF limitado por tamanho, com `fonte`, `id` e indicação explícita de dado não confiável.
- Sessões locais bloqueiam acesso a outros escopos, exigem revisão e permissões para exclusão.
- Motor registra hash da justificativa, rejeita alguns padrões de credenciais e normaliza validade para UTC.
- Cache só é usado com marcação explícita de conteúdo público. Roteador não usa modelo sem conexão, consentimento, custo e escopo permitido.
- CLI read-only e benchmark sintético. Nenhum segredo ou memória real foi carregado nos testes.

## Bloqueadores do merge / produção

- **Autenticação ausente:** `SessaoMemoria` é uma fachada para código já confiável, não prova a identidade de quem chama. O motor bruto pode ser acessado pelo mesmo processo.
- **Criptografia ausente:** SQLite local está em texto claro. chmod 0600 restringe permissões POSIX, mas não protege o disco/backups nem todos os arquivos temporários.
- **PII incompleta:** regex são um primeiro filtro, não reconhecimento completo de dados pessoais ou prompt injection. Conteúdo de memória segue não confiável.
- **Exclusão parcial:** remoção local não alcança cópias remotas, backups e histórico do Git.
- **Sem agentes de IA reais:** `OrquestradorLocal` usa funções Python e críticos callback. O roteador somente escolhe dentre modelos declarados; nenhum modelo foi executado nesta fase.
- **Sem embeddings reais:** a combinação atual é FTS5 + RRF; "híbrido" semântico exige embeddings e avaliação separada.
- **Sem mensuração real do ChatGPT:** benchmark mede biblioteca local, não tempo de resposta, tokens ou custos do ChatGPT.
- **Fonte V2 preservada:** ainda não existe promoção V3 -> V2 automática ou alteração de arquivos privados.

**Recomendação dos críticos:** aprovar para desenvolvimento experimental isolado. Manter PR como rascunho até implementar autenticação, segurança, auditoria de privacidade e teste de integração completo.
