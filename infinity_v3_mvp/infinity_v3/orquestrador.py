"""Orquestração local verificável de tarefas e críticos.

Executa funções Python registradas. NÃO cria subagentes LLM automaticamente.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

Executor = Callable[[dict[str, Any]], dict[str, Any]]
Critico = Callable[[dict[str, Any]], tuple[bool, str]]


@dataclass(frozen=True)
class Tarefa:
    id: str
    agente: str
    entrada: dict[str, Any] = field(default_factory=dict)
    depende_de: tuple[str, ...] = ()
    criticos: tuple[str, ...] = ()


@dataclass(frozen=True)
class Resultado:
    id: str
    estado: str
    saida: dict[str, Any] | None
    pareceres: tuple[str, ...]


class ErroDePlano(ValueError):
    pass


class OrquestradorLocal:
    def __init__(self, *, agentes: dict[str, Executor], criticos: dict[str, Critico],
                 maximo_tarefas: int = 100) -> None:
        self.agentes = agentes.copy()
        self.criticos = criticos.copy()
        self.maximo_tarefas = maximo_tarefas

    def executar(self, tarefas: list[Tarefa]) -> list[Resultado]:
        if not tarefas or len(tarefas) > self.maximo_tarefas:
            raise ErroDePlano("A quantidade de tarefas é inválida")
        mapa = {t.id: t for t in tarefas}
        if len(mapa) != len(tarefas) or not all(t.id and t.agente for t in tarefas):
            raise ErroDePlano("IDs devem ser únicos e agentes não vazios")
        for tarefa in tarefas:
            if tarefa.agente not in self.agentes:
                raise ErroDePlano(f"Agente não registrado: {tarefa.agente}")
            if not tarefa.criticos:
                raise ErroDePlano(f"Tarefa sem crítico independente: {tarefa.id}")
            if any(c not in self.criticos for c in tarefa.criticos):
                raise ErroDePlano(f"Crítico não registrado: {tarefa.id}")
            if any(d not in mapa or d == tarefa.id for d in tarefa.depende_de):
                raise ErroDePlano(f"Dependência inválida: {tarefa.id}")
        pendentes = dict(mapa)
        resultados: dict[str, Resultado] = {}
        while pendentes:
            prontos = [t for t in pendentes.values() if all(d in resultados for d in t.depende_de)]
            if not prontos:
                raise ErroDePlano("Dependência circular detectada; nenhuma tarefa foi ignorada")
            for tarefa in prontos:
                if any(resultados[d].estado != "aprovada" for d in tarefa.depende_de):
                    resultado = Resultado(tarefa.id, "bloqueada", None, ("Dependência não aprovada",))
                else:
                    try:
                        saida = self.agentes[tarefa.agente](dict(tarefa.entrada))
                        if not isinstance(saida, dict):
                            raise TypeError("A saída do agente deve ser dicionário")
                        pareceres: list[str] = []
                        aprovada = True
                        for nome in tarefa.criticos:
                            ok, mensagem = self.criticos[nome](dict(saida))
                            pareceres.append(f"{nome}: {mensagem}")
                            aprovada = aprovada and bool(ok)
                        resultado = Resultado(tarefa.id, "aprovada" if aprovada else "reprovada",
                                              saida, tuple(pareceres))
                    except Exception as e:
                        # Não incluir entradas ou dados potencialmente confidenciais no log.
                        resultado = Resultado(tarefa.id, "erro", None,
                                              (f"Falha do executor/crítico: {type(e).__name__}",))
                resultados[tarefa.id] = resultado
                del pendentes[tarefa.id]
        return [resultados[t.id] for t in tarefas]
