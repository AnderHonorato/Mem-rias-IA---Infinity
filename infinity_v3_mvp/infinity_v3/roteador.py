"""Roteamento explícito e determinístico. Não invoca APIs de IA.

Preços e latências são configuração do operador, nunca afirmações de mercado.
Modelos indisponíveis ou sem permissão não podem ser selecionados.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Classe = Literal["rapido", "equilibrado", "profundo"]


@dataclass(frozen=True)
class Modelo:
    nome: str
    classe: Classe
    conectado: bool
    local: bool
    custo_estimado_por_mil_tokens: float  # valor configurado, não tarifa oficial
    latencia_prevista_ms: int


@dataclass(frozen=True)
class Politica:
    permite_pago: bool = False
    permite_nuvem: bool = False
    teto_estimado: float = 0.0
    tokens_estimados: int = 2000


@dataclass(frozen=True)
class Escolha:
    modelo: str
    classe: Classe
    custo_estimado: float
    motivo: str


class NenhumModeloElegivel(ValueError):
    pass


class Roteador:
    def __init__(self, modelos: list[Modelo]) -> None:
        nomes = [m.nome for m in modelos]
        if len(nomes) != len(set(nomes)) or any(m.latencia_prevista_ms < 0 or m.custo_estimado_por_mil_tokens < 0 for m in modelos):
            raise ValueError("Catálogo de modelos inválido")
        self.modelos = modelos[:]

    @staticmethod
    def complexidade(tarefa: str) -> Classe:
        texto = tarefa.casefold()
        if any(x in texto for x in ("auditoria", "arquitetura", "segurança", "vulnerabilidade", "migração", "refatoração complexa")):
            return "profundo"
        if any(x in texto for x in ("program", "código", "implementar", "pesquisa", "corrigir", "teste")) or len(tarefa) > 400:
            return "equilibrado"
        return "rapido"

    def escolher(self, tarefa: str, politica: Politica, *, preferido: str | None = None,
                 sigiloso: bool = False) -> Escolha:
        if not isinstance(tarefa, str) or not tarefa.strip() or len(tarefa) > 20000:
            raise ValueError("Tarefa inválida")
        if politica.teto_estimado < 0 or not 1 <= politica.tokens_estimados <= 1000000:
            raise ValueError("Política inválida")
        objetivo = self.complexidade(tarefa)
        ordem = {"rapido": 0, "equilibrado": 1, "profundo": 2}
        elegiveis = []
        for m in self.modelos:
            custo = m.custo_estimado_por_mil_tokens * (politica.tokens_estimados / 1000)
            if not m.conectado or (sigiloso and not m.local) or (not m.local and not politica.permite_nuvem):
                continue
            if custo > 0 and (not politica.permite_pago or custo > politica.teto_estimado):
                continue
            if preferido and m.nome != preferido:
                continue
            if not preferido and ordem[m.classe] < ordem[objetivo]:
                continue
            elegiveis.append((m, custo))
        if not elegiveis:
            raise NenhumModeloElegivel("Nenhum modelo conectado atende às permissões, custos e qualidade exigidos")
        elegiveis.sort(key=lambda x: (x[0].latencia_prevista_ms, x[0].custo_estimado_por_mil_tokens, x[0].nome))
        m, custo = elegiveis[0]
        return Escolha(m.nome, m.classe, round(custo, 6),
                       "Seleção por disponibilidade, privacidade, complexidade, custo autorizado e latência configurada")
