# Registro contínuo de interações

**Definido por Ander em:** 2026-08-29
**Estado:** REGRA PERMANENTE

## Regra

O GPT deve usar o repositório `AnderHonorato/Mem-rias-IA---Infinity` como memória persistente da conversa.

- A leitura dos READMEs, índices e contexto necessário ocorre no início da interação/conversa. Não é necessário reler os mesmos arquivos a cada mensagem do mesmo fluxo, salvo quando houver motivo técnico, mudança de assunto que exija outro arquivo temático ou pedido explícito de Ander.
- A gravação é contínua: **cada nova mensagem de Ander e cada nova resposta do GPT devem ser registradas resumidamente**, sem exceção, no histórico de `GPT/Interacoes/`.
- Quando surgir conteúdo classificável, registrar também na pasta temática apropriada (`Memorias/`, `Projetos/`, `Decisoes/`, `Artefatos/` etc.), sem concentrar tudo em um único arquivo.
- Preferências, fatos pessoais duráveis, decisões, andamento de projetos, correções e instruções permanentes devem ser preservados para continuidade futura.
- Mídias e artefatos importantes devem ser preservados quando tecnicamente possível; quando o arquivo binário não puder ser gravado diretamente pelo conector, registrar uma referência identificável ao arquivo, anexo, URL, caminho ou contexto correspondente em `GPT/Artefatos/`.
- Nunca registrar senhas, tokens, cookies, chaves privadas, códigos de recuperação ou outros segredos.
- O GPT deve seguir também todas as demais regras vigentes em `GPT/README.md` e no README raiz.

## Correção da interpretação anterior

A regra de "ler uma vez no início" se aplica somente à **releitura dos arquivos de memória**. Ela **não** limita o registro. O registro deve continuar acontecendo após cada nova mensagem do usuário e após cada resposta do GPT durante toda a interação.
