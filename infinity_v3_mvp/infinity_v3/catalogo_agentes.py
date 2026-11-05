"""Contratos de papéis. Cadastros não criam sessões de IA por si só.

Executores reais devem ser conectados por chamadas autorizadas do host.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PapelAgente:
    nome: str
    especialidade: str
    categoria: str
    ferramentas: tuple[str, ...] = ()


AGENTES: dict[str, PapelAgente] = {
    a.nome: a for a in (
        PapelAgente("planejador", "Divisão, dependências e metas", "planejamento"),
        PapelAgente("pesquisador", "Fontes, referências e versões", "pesquisa", ("buscar_publico",)),
        PapelAgente("arquiteto", "Contratos e trade-offs", "engenharia"),
        PapelAgente("backend", "Serviços, dados e APIs", "engenharia", ("editar_codigo",)),
        PapelAgente("frontend", "Interfaces e experiência", "engenharia", ("editar_codigo",)),
        PapelAgente("memoria", "Proveniência, conflitos e memória V2", "conhecimento", ("consultar_memoria",)),
        PapelAgente("seguranca", "Ameaças, privacidade e autorização", "governanca"),
        PapelAgente("performance", "Métricas e gargalos", "qualidade", ("testar_codigo",)),
        PapelAgente("qa", "Testes, regressões e cobertura", "qualidade", ("testar_codigo",)),
        PapelAgente("devops", "CI, provisionamento e deployment", "operacoes", ("publicar_codigo",)),
        PapelAgente("integracoes", "Plugins, modelos e conectores", "operacoes", ("buscar_publico",)),
        PapelAgente("documentacao", "Guias, changelogs e handoffs", "documentacao", ("editar_codigo",)),
    )
}

CRITICOS: dict[str, PapelAgente] = {
    c.nome: c for c in (
        PapelAgente("critico_corretude", "Verifica evidências e critérios de aceite", "critico"),
        PapelAgente("critico_seguranca", "Revisa injeção, segredos e permissões", "critico"),
        PapelAgente("critico_privacidade", "Examina vazamentos e retenção", "critico"),
        PapelAgente("critico_performance", "Revisa benchmarks e custo", "critico"),
        PapelAgente("critico_acessibilidade", "Verifica WCAG, teclado e semântica", "critico"),
        PapelAgente("critico_integracao", "Verifica interfaces e regressões entre módulos", "critico"),
    )
}


def criticos_exigidos(risco: str) -> int:
    if risco not in {"baixo", "medio", "alto"}:
        raise ValueError("Classificação de risco inválida")
    return 2 if risco == "alto" else 1
