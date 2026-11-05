# Próxima fase — Infinity V3 / agentes reais e gateway seguro

## Gate de início

- [ ] Definir onde ficará o serviço (local privado vs servidor autenticado).
- [ ] Revisar política de privacidade; dados pessoais nunca no Git público ou no cache público.
- [ ] Selecionar apenas plugins/credenciais realmente disponíveis e consentidos.

## Etapa A: identidade e permissões

- API autenticada, sessões revogáveis, CSRF/CORS/rate-limit, segregação de dados, auditoria sem conteúdo privado.
- Criptografia em repouso e chaves via gestor de segredos do host; rotação de credenciais, testes de falha.
- Exclusão com comprovante e política de retenção/backups; não prometer apagamento físico absoluto.

## Etapa B: agentes, críticos e ferramentas

- 12 papéis: planejador, pesquisador, arquiteto, backend, frontend, memória, segurança, performance, QA, DevOps, integrações e documentação.
- 6 críticos independentes: segurança, privacidade, corretude, performance, acessibilidade e integração.
- Cada tarefa passa por revisão crítica; tarefas rejeitadas bloqueiam dependentes, com relatório de evidências.
- Executor de modelo é interface injetada; conexão real exige plugin/API habilitado, autorização de gastos e credenciais fora do repo.
- Ferramentas com allowlist por papel, modo dry-run e confirmação antes de ações destrutivas.

## Etapa C: contexto e velocidade

- Benchmark de recuperação V2 vs FTS+RRF, com dataset e casos de falha.
- Embeddings opcionais sob consentimento, com políticas específicas para dado pessoal.
- Usar métricas p50/p95, custo estimado e taxa de acertos, comparar com baseline; não inventar percentuais.

## Etapa D: UX e entrega

- Dashboard responsivo PT-BR; busca, proveniência, memória pendente, revisão, histórico, agentes e custos.
- Pipeline CI: testes, secrets, dependency review, lint, cobertura, integração e aprovação do crítico.
- Publicar somente com autenticação e testes end-to-end; PR da V3 continua draft até então.
