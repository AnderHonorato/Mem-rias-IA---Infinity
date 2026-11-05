"""Coordenação supervisionada: barreira dupla para operações de alto risco."""
from __future__ import annotations

from dataclasses import dataclass

from .auditoria import RegistroAuditoria
from .catalogo_agentes import AGENTES, CRITICOS, criticos_exigidos
from .orquestrador import OrquestradorLocal, Resultado, Tarefa, ErroDePlano


@dataclass(frozen=True)
class TarefaSupervisionada:
    tarefa: Tarefa
    risco: str = "baixo"


class Supervisao:
    def __init__(self, orquestrador: OrquestradorLocal,
                 auditoria: RegistroAuditoria | None = None) -> None:
        self.orquestrador = orquestrador
        self.auditoria = auditoria

    def executar(self, tarefas: list[TarefaSupervisionada]) -> list[Resultado]:
        if not tarefas:
            raise ErroDePlano("Plano vazio")
        for item in tarefas:
            t = item.tarefa
            # Antes de executar callbacks, rejeitar IDs que não cabem na auditoria.
            if self.auditoria is not None:
                for campo, valor in (("tarefa", t.id), ("agente", t.agente)):
                    if not isinstance(valor, str) or not 1 <= len(valor) <= 100 or not all(c.isalnum() or c in "-_" for c in valor):
                        raise ErroDePlano(f"{campo} inválido para auditoria")
            if t.agente not in AGENTES:
                raise ErroDePlano(f"Papel de agente desconhecido: {t.agente}")
            if len(set(t.criticos)) != len(t.criticos):
                raise ErroDePlano("Críticos duplicados")
            if any(c not in CRITICOS for c in t.criticos):
                raise ErroDePlano("Crítico fora do catálogo independente")
            if len(t.criticos) < criticos_exigidos(item.risco):
                raise ErroDePlano(f"Tarefa {t.id} exige mais revisores por ser de risco {item.risco}")
        resultados = self.orquestrador.executar([item.tarefa for item in tarefas])
        if self.auditoria is not None:
            for item, resultado in zip(tarefas, resultados):
                self.auditoria.registrar(tarefa=item.tarefa.id, agente=item.tarefa.agente,
                    estado=resultado.estado, revisores=(len(resultado.pareceres)
                        if resultado.estado in {"aprovada", "reprovada"} else 0))
        return resultados
