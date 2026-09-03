# Decisão permanente — aprendizado por feedback

**Data:** 2026-09-03  
**Origem:** instrução explícita de Ander  
**Estado:** ATIVO

## Decisão

O GPT deve tratar feedback negativo reutilizável como memória operacional, não apenas como correção momentânea da conversa.

Quando Ander informar que um caminho, código, resposta, interpretação, visual, ferramenta, recomendação ou processo está errado, não funciona ou não deve ser usado, o GPT deve registrar o padrão rejeitado no sistema compartilhado `../../Conhecimento Compartilhado/aprendizado-por-feedback/` quando ele puder afetar tarefas futuras.

Se uma abordagem alternativa funcionar ou for aprovada, registrar também o sucesso correspondente e relacionar os IDs.

## Regra de não repetição

Uma entrada `ATIVO` em `ERROS.md` bloqueia a repetição do mesmo padrão dentro do escopo registrado. O GPT deve consultar erros e sucessos relevantes antes de repetir tarefas semelhantes.

O escopo pode ser global, projeto, assunto, tecnologia, entrega ou condição temporária. Não ampliar uma rejeição específica para proibição global sem confirmação de Ander.

## Mudanças futuras

Se Ander mudar de preferência, pedir explicitamente uma nova tentativa ou o ambiente técnico mudar de forma relevante, preservar a entrada anterior, marcar como `SUPERADO` quando apropriado e registrar a nova regra/solução.

## Segurança

Nunca copiar segredos, credenciais, tokens, cookies, chaves privadas ou dados sensíveis para os registros de erro/sucesso. Trechos técnicos devem ser sanitizados.

## Referências

- `../../Conhecimento Compartilhado/aprendizado-por-feedback/README.md`
- `../../Conhecimento Compartilhado/aprendizado-por-feedback/ERROS.md`
- `../../Conhecimento Compartilhado/aprendizado-por-feedback/SUCESSOS.md`
- `../../Conhecimento Compartilhado/aprendizado-por-feedback/CASOS-DE-USO.md`
