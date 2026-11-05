# Etapa 4 — Gateways de modelos e agentes LLM reais (desligados por padrão)

## Funcionalidade implementada

- `gateway_modelos.py`: adaptadores HTTP para OpenAI Responses, Claude Messages e Ollama Chat; endereço **fixo por provedor**, sem redirecionamentos nem proxy herdado.
- `agentes_modelos.py`: callbacks reais dos papéis de agentes/críticos que usam o gateway; executam dentro do orquestrador Python já existente.
- `roteamento_modelos.py`: liga roteador por custo, velocidade e classe à execução real; valida consistência entre catálogo e destino.
- `test_gateway_modelos.py` e `test_roteamento_real.py`: testes com transportes falsos, sem chamadas e sem cobrança de API.
- `exemplos/consultar_ollama.py`: chamada sintética ao Ollama **somente** com flag de autorização.

Documentações de referência, consultadas em 05/11/2026:
- OpenAI Responses: https://developers.openai.com/api/reference/resources/responses/methods/create
- Claude Messages: https://platform.claude.com/docs/en/api/messages/create
- Claude Authentication: https://platform.claude.com/docs/en/manage-claude/authentication
- Ollama Chat: https://docs.ollama.com/api/chat

## Regra operacional

Por padrão nenhuma API é chamada. A biblioteca exige **todas** as permissões necessárias, configuração de preços **fornecida pelo operador**, modelo realmente existente, limite de chamadas, autorização de dados e credenciais externas ao repositório.

As tarifas declaradas são estimativas e **não asseguram** que a cobrança efetiva ficará abaixo do teto; cache de prompt, tokens e outras tarifas variam por API. Para limites reais, configure alertas, créditos/orçamentos no próprio provedor. É proibido publicar chaves no GitHub ou gravar dados privados nos logs.

Informações internas exigem permissão adicional de envio à nuvem. Material rotulado como `sensivel` é **sempre bloqueado para nuvem**, mesmo com permissão de custo, mas pode ser enviado localmente mediante autorização; heurísticas de detecção não classificam tudo sozinhas.

## Exemplo de Ollama local com consentimento

O script utiliza apenas um exemplo público e texto sintético. Certifique-se de que o Ollama está executando e que o modelo foi instalado por você.

```bash
cd infinity_v3_mvp
python -m unittest discover -s testes -v
python -m exemplos.consultar_ollama --modelo nome-do-modelo
# A chamada acima fica bloqueada até haver confirmação:
python -m exemplos.consultar_ollama --modelo nome-do-modelo --autorizo-rede-local
```

Não há conexão automática com as assinaturas ChatGPT/Claude; uso via API costuma exigir faturamento separado e credenciais próprias.

## Integração de agente e crítico (sem API por padrão)

```python
from infinity_v3.gateway_modelos import GatewayModelos, ConfiguracaoModelo, PermissaoChamada
from infinity_v3.agentes_modelos import PreparadorAgentes, Atribuicao
from infinity_v3.orquestrador import Tarefa

modelos = ConfiguracaoModelo('ollama', 'nome-do-modelo')
permissao = PermissaoChamada()  # nega chamadas por padrão
conexao = Atribuicao(modelos, permissao)
gestao = PreparadorAgentes(GatewayModelos(),
    agentes={'backend': conexao},
    criticos={'critico_corretude': conexao})
resultado = gestao.orquestrador().executar([
    Tarefa(id='demonstração', agente='backend',
           entrada={'objetivo': 'Crie um plano de testes para código sintético', 'classificacao': 'publica'},
           criticos=('critico_corretude',))
])
print(resultado[0].estado)  # erro, sem requisições (simulação segura de negação)
```

Para conectar modelos reais, o **host do usuário** precisa criar `PermissaoChamada(rede_habilitada=True, ...)` e fornecer modelo instalado ou chave na variável de ambiente apropriada. Críticos e autores são papéis separados, mas NÃO são automaticamente instâncias de IA independentes se atribuídos ao mesmo provedor/modelo. Para ações de alto risco, escolha revisores independentes, utilize o gate de supervisão e valide evidências fora da própria resposta do modelo.

## Ameaças ainda não mitigadas (bloqueios para produção)

- Sem autenticação/autorização de identidades reais, armazenamento criptografado ou isolamento entre contas no servidor.
- Sem medidor de consumo de tokens confirmado por fatura, nenhuma garantia de limite financeiro absoluto.
- Nenhum modelo real foi consultado na CI: adaptadores são verificados com payloads sintéticos/transportes substitutos.
- Sem limite de frequência global distribuído, autorização revogável ou serviço robusto de filas.
- Não aplicar ferramentas mutáveis diretamente a respostas de LLMs sem validação humana e confirmação de uso único.
- Não misturar memória pública do repositório Git com dados privados; `knowledge/` segue fonte canônica V2.
- Críticos com mesmo modelo podem reproduzir os mesmos erros; análise de independência externa é necessária.

**Status:** código de integração concluído e testado localmente; implantação privada ainda não ativada. PR continua em rascunho até segurança e testes end-to-end.
