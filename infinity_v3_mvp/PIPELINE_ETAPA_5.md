# Etapa 5 — Perguntas com contexto recuperado e guardas de privacidade

## Caminho completo implementado

`pergunta → IndiceCanonicoV2 + MotorMemoria → RRF → política de dados → Roteador → GatewayModelos → resposta com referências`

O `PipelineContextual` reutiliza os módulos existentes e não duplica a fonte canônica.
Os trechos são serializados em campo `memorias_nao_confiaveis` e o prompt instrui o modelo a não obedecer comandos neles. Isto **não é** uma proteção infalível contra prompt injection.

- **Sem escopos de memória:** preserva classificação de entrada (padrão `interna`).
- **Somente escopos canônicos:** força `interna` ou `sensivel`, nunca `publica`.
- **Qualquer escopo local:** força `sensivel`, e o gateway proíbe envio à nuvem.
- **Sem modelo local elegível:** falha fechada, não tenta API paga automaticamente.
- **Rede desabilitada:** não envia prompts, mesmo que o roteador encontre modelo elegível.
- **Proveniência:** a resposta carrega referências dos documentos selecionados, sem afirmar que o modelo efetivamente as citou.

## Contrato de confiança

`usuario_autenticado` e `escopos_*` são fornecidos por um host confiável. A classe **não autentica** usuários, e um chamador Python malicioso no mesmo processo pode burlar controles de escopo. Não exponha este módulo diretamente como endpoint web público.

O estado SQLite local continua não criptografado, o que impede armazenamento de dados pessoais reais. Para um ambiente de produção ainda faltam autenticação, criptografia, gestão de segredos, quotas persistentes e testes reais com modelos instalados.

## Testes

`python -m unittest discover -s testes -v` cobre a recuperação seletiva, impossibilidade de enviar memória local à nuvem, falha sem permissão e preservação de escopos.

**Não significa que o ChatGPT tenha acesso automático à memória V2:** o pipeline só funciona em um serviço ou computador que execute este código, com acesso local aos arquivos e configuração autorizada dos modelos.
