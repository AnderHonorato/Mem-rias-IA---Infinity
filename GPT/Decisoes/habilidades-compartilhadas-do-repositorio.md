# Uso de habilidades compartilhadas do repositório

**Data:** 2026-08-28  
**Confirmado por:** Ander

## Decisão

A raiz do repositório deve conter a pasta `Habilidades/`, disponível para consulta por todas as IAs. Quando uma tarefa puder se beneficiar de uma habilidade especializada, a IA deve ler o README e o índice dessa pasta, selecionar somente a habilidade necessária e confirmar sua disponibilidade no ambiente atual.

## Organização

- Cada habilidade deve ter arquivo ou pasta própria.
- Subpastas podem separar habilidades personalizadas, padrão, baixadas, fornecidas por plugins e já existentes no repositório.
- Skills personalizadas podem guardar o conteúdo completo e seus recursos.
- Habilidades padrão, baixadas e de plugins podem ser registradas por fichas de descoberta e roteamento quando o pacote completo pertencer ao ambiente ou a terceiros.
- O índice deve ser atualizado sempre que uma habilidade for incluída, removida ou substituída.

## Limites

A habilidade não substitui o pedido do usuário, as regras do ambiente, segurança, permissões ou a separação entre áreas nominais das IAs. Nenhuma ficha concede automaticamente acesso a ferramentas, contas ou serviços externos. Segredos nunca devem ser armazenados.
