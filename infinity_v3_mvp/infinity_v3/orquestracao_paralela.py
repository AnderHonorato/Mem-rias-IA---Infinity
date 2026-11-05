"""Execução concorrente apenas de tarefas independentes e locais.

Não executa LLMs automaticamente. O host deve registrar callbacks thread-safe,
sem compartilhar conexões SQLite de uma única thread entre os executores.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from typing import Any

from .orquestrador import OrquestradorLocal, Tarefa, Resultado, ErroDePlano


class OrquestradorParaleloLocal(OrquestradorLocal):
    def __init__(self, *, agentes, criticos, maximo_tarefas: int = 100,
                 maximo_paralelo: int = 4) -> None:
        super().__init__(agentes=agentes, criticos=criticos, maximo_tarefas=maximo_tarefas)
        if not isinstance(maximo_paralelo, int) or not 1 <= maximo_paralelo <= 16:
            raise ErroDePlano("Paralelismo deve ficar entre 1 e 16")
        self.maximo_paralelo = maximo_paralelo

    def _executar_uma(self, tarefa: Tarefa) -> Resultado:
        try:
            saida = self.agentes[tarefa.agente](deepcopy(tarefa.entrada))
            if not isinstance(saida, dict):
                raise TypeError("O agente precisa retornar um dicionário")
            pareceres: list[str] = []
            aprovado = True
            for nome in tarefa.criticos:
                ok, mensagem = self.criticos[nome](deepcopy(saida))
                aprovado = aprovado and bool(ok)
                pareceres.append(f"{nome}: {str(mensagem)[:500]}")
            return Resultado(tarefa.id, "aprovada" if aprovado else "reprovada", saida, tuple(pareceres))
        except Exception as exc:
            return Resultado(tarefa.id, "erro", None, (f"Falha de execução: {type(exc).__name__}",))

    def executar(self, tarefas: list[Tarefa]) -> list[Resultado]:
        if not tarefas or len(tarefas) > self.maximo_tarefas:
            raise ErroDePlano("A quantidade de tarefas é inválida")
        mapa = {t.id: t for t in tarefas}
        if len(mapa) != len(tarefas) or not all(isinstance(t.id, str) and t.id and t.agente for t in tarefas):
            raise ErroDePlano("IDs devem ser únicos e agentes não vazios")
        for t in tarefas:
            if t.agente not in self.agentes or not t.criticos or any(c not in self.criticos for c in t.criticos):
                raise ErroDePlano(f"Agente ou crítico não registrado: {t.id}")
            if any(d not in mapa or d == t.id for d in t.depende_de):
                raise ErroDePlano(f"Dependência inválida: {t.id}")
        pendentes = dict(mapa)
        resultados: dict[str, Resultado] = {}
        with ThreadPoolExecutor(max_workers=self.maximo_paralelo) as pool:
            while pendentes:
                prontos = [t for t in pendentes.values() if all(d in resultados for d in t.depende_de)]
                if not prontos:
                    raise ErroDePlano("Dependência circular detectada")
                futuros = {}
                for t in prontos:
                    if any(resultados[d].estado != "aprovada" for d in t.depende_de):
                        resultados[t.id] = Resultado(t.id, "bloqueada", None, ("Dependência não aprovada",))
                    else:
                        futuros[t.id] = pool.submit(self._executar_uma, t)
                for tarefa_id, futuro in futuros.items():
                    resultados[tarefa_id] = futuro.result()
                for t in prontos:
                    del pendentes[t.id]
        # Ordem de entrada preservada independentemente da ordem de conclusão.
        return [resultados[t.id] for t in tarefas]
