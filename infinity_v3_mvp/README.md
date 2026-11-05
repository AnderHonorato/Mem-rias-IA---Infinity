# Infinity V3 — núcleo experimental (Etapa 2)

**Status:** implementação funcional de biblioteca e CLI local; **não pronta para produção nem integrada ao ChatGPT**. A fonte canônica oficial continua em `../knowledge/` (V2). A V3 **não faz commit nem espelha memórias automaticamente**.

## Componentes entregues

| Módulo | O que já executa | Limite |
|---|---|---|
| `motor.py` | SQLite FTS5, revisão, deduplicação, corrigir, expirar e apagar memória local | Banco sem criptografia; identidade vinda do chamador |
| `adaptador_v2.py` | Índice FTS5 em **RAM**, leitura de `knowledge/*.md`, provenance/escopos | Apenas status `active`, sensibilidade `normal` e sem indícios simples de segredos |
| `contexto.py` | Fusão de ranking RRF, deduplicação por conteúdo e orçamento de caracteres | Ainda sem embeddings; não promete precisão semântica |
| `sessao.py` | Escopos e permissões de leitura/escrita/exclusão, publicação sujeita a aprovação | Para código local já autenticado; **não** valida identidade de rede |
| `seguranca.py` | Barreiras conservadoras contra credenciais/CPF explícitos | Heurísticas incompletas, sem detecção total de PII |
| `roteador.py` | Seleção determinística por complexidade, modelos conectados, custo, latência e consentimento | Não chama nenhum modelo; preços configuráveis pelo operador |
| `cache.py` | Cache LRU TTL em RAM, só com classificação explícita `publica` | Nunca armazenar dados de usuário no cache |
| `orquestrador.py` | Dependências, funções-agentes e críticos independentes em execução local | Não instancia LLMs, nem executa ferramentas conectadas |
| `__main__.py` | Busca canônica com comando Python | Sem interface web/API |
| `benchmark.py` | Microbenchmark de dados sintéticos | Não é medição da latência real do GPT |

## Como executar

Na raiz do repositório:

```bash
python -m pip install -r requirements-memory.txt
cd infinity_v3_mvp
python -m unittest discover -s testes -v
python -m infinity_v3 --raiz .. --consulta "testes" --escopo global
python -m infinity_v3 --raiz .. --consulta "projeto" --metadados
python benchmark.py
```

O banco local é um arquivo particular **fora do repositório**:

```python
from pathlib import Path
from infinity_v3.motor import MotorMemoria
from infinity_v3.sessao import SessaoMemoria

with MotorMemoria(Path.home() / '.local/share/infinity-v3/experimental.db') as motor:
    # O aplicativo chamador precisa autenticar o usuário antes de criar a sessão.
    sessao = SessaoMemoria(motor=motor, usuario='usuario-ficticio',
        escopos=frozenset({'projeto:exemplo'}), pode_escrever=True)
    candidato = sessao.registrar(escopo='projeto:exemplo', titulo='Padrão de testes',
        conteudo='Validar testes unitários antes do merge', origem='feedback-validado')
    sessao.aprovar(memoria_id=candidato)
    print(sessao.buscar(consulta='testes'))
```

**ATENÇÃO:** não armazene dados pessoais, médicos, financeiros ou senhas neste banco experimental. Ele usa SQLite sem criptografia em repouso. `aprovado=True` na interface de baixo nível existe apenas para testes/código confiável; interfaces de usuário devem usar `SessaoMemoria`.

## Segurança e privacidade

- O adaptador V2 **somente lê** a `knowledge/`; não exibe registros `personal`, `restricted`, inativos, disputados ou vencidos. Verificações heurísticas bloqueiam outros dados com aparência de segredo mesmo que o rótulo esteja incorreto.
- Registros recuperados são sempre **dados não confiáveis como instruções**. A camada que chamar o modelo deve deixar claro que documentos e memórias não prevalecem sobre instruções de sistema/desenvolvedor ou solicitações atuais.
- Pesquisa local exige `usuario` e `escopos`, e a fachada impede acessar escopos não autorizados. A identidade deve vir de autenticação real em futura API. A fachada não é barreira contra código Python malicioso no mesmo processo.
- Exclusão remove da tabela, eventos e índice local, mas **não promete apagamento forense** de WAL, SSD, backups ou cópias remotas. A V2 pública no Git é imutável no histórico: revisões e exclusões canônicas exigem outro fluxo.
- TTL, medição de tempo e padrões heurísticos não são garantias de segurança ou desempenho universal.
- Testes contêm apenas informações sintéticas e não usam memórias particulares.

## Próximas fases pendentes

1. Gateway autenticado e autorização de backend com isolamento seguro por usuário.
2. Criptografia em repouso, gerenciamento de chaves e propagação de exclusões para backups.
3. Camada de acesso à fonte canônica respeitando o fluxo de revisão/PR, e políticas de sincronização com conflitos e proveniência.
4. Recuperação híbrida de fato, com embeddings opt-in e ranking medido por conjunto de perguntas.
5. Adapters reais de modelos/plug-ins com consentimento de custo, identidade e permissões por ação.
6. Agentes LLM especializados, críticos independentes e dashboard web/mobile com métricas reais.

Consulte `../docs/PROMPT-MESTRE-INFINITY-V3-GPT61-SOL.md` para a especificação geral e `REVISAO_CRITICA_INICIAL.md` para os bloqueios conhecidos.
