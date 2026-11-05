# Infinity V3 — núcleo experimental (primeiro vertical slice)

Módulo Python 3.12+, com `sqlite3` e `FTS5` da biblioteca padrão. Não é uma versão final, não contém integração com modelos/ChatGPT e **não realiza aprendizado automático sem aprovação**.

## Rodar testes

```bash
python -m unittest discover -s testes -v
```

## Exemplo rápido

```python
from pathlib import Path
from infinity_v3 import MotorMemoria

# Banco local PRIVADO, não dentro do GitHub público.
with MotorMemoria(Path.home() / ".local/share/infinity-v3/memorias.db") as memoria:
    candidato = memoria.registrar(usuario="perfil-01", escopo="projeto:exemplo",
        titulo="Linguagem", conteudo="Documentar exemplos em português",
        origem="feedback-confirmado")
    memoria.aprovar(usuario="perfil-01", memoria_id=candidato)
    print(memoria.buscar(usuario="perfil-01", escopos=["projeto:exemplo"], consulta="português"))
```

## Orquestração local experimental

`infinity_v3/orquestrador.py` executa funções Python registradas em ordem de dependências e requer pelo menos um crítico independente por tarefa. Reprovação bloqueia dependentes. **Ainda não instancia agentes LLM**, mas fornece uma base real e testada para integrá-los futuramente.

## O que este MVP comprova
- SQLite transacional e índice FTS5 com atualizações por trigger.
- Candidatos exigem aprovação, salvo consentimento explícito no registro.
- Controle de acesso por usuário/escopo em cada leitura.
- Deduplicação por fingerprint por usuário/escopo.
- Correções mantêm histórico e o índice desconsidera dados substituídos.
- Expiração de memórias, rejeição de conteúdo marcado como segredo e eventos de auditoria mínimos.

## Ainda NÃO implementado
Armazenamento canônico em `knowledge/` sincronizado, banco criptografado, classificação semântica de sensibilidade, autenticação de rede, embeddings, ranking híbrido, agentes executores, plugins, API e UI; todos exigem novas fases e testes de segurança. Este motor é apenas local e sua autorização por identificador depende de uma camada externa que autentique o usuário.

**Alerta:** não use este protótipo como armazenamento de informações sensíveis em produção. O banco ainda não está criptografado em repouso.
