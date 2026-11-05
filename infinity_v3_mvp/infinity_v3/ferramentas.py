"""Gateway local explícito de ferramentas com modo simulação por padrão.

Não executa plugins automaticamente: exige callback confiável injetado pelo host.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class AcaoNaoAutorizada(PermissionError):
    pass


@dataclass(frozen=True)
class Ferramenta:
    nome: str
    risco: str
    executor: Callable[[dict[str, Any]], dict[str, Any]]

    def __post_init__(self) -> None:
        if self.risco not in {"leitura", "escrita", "destrutiva"} or not self.nome:
            raise ValueError("Ferramenta inválida")


@dataclass(frozen=True)
class PoliticaFerramentas:
    nomes_permitidos: frozenset[str]
    permite_escrever: bool = False
    permite_destruir: bool = False
    confirmacoes: frozenset[str] = frozenset()
    simular: bool = True


class ExecutorControlado:
    def __init__(self, ferramentas: list[Ferramenta], *, limite_por_instancia: int = 25) -> None:
        if not 1 <= limite_por_instancia <= 10000:
            raise ValueError("Limite inválido")
        self.catalogo = {f.nome: f for f in ferramentas}
        if len(self.catalogo) != len(ferramentas):
            raise ValueError("Ferramenta duplicada")
        self.limite = limite_por_instancia
        self.chamadas = 0
        self.confirmacoes_consumidas: set[str] = set()

    def executar(self, *, nome: str, entrada: dict[str, Any], politica: PoliticaFerramentas,
                 id_confirmacao: str | None = None) -> dict[str, Any]:
        if self.chamadas >= self.limite:
            raise AcaoNaoAutorizada("Limite de chamadas atingido")
        ferramenta = self.catalogo.get(nome)
        if ferramenta is None or nome not in politica.nomes_permitidos:
            raise AcaoNaoAutorizada("Ferramenta não autorizada")
        if ferramenta.risco in {"escrita", "destrutiva"} and not politica.permite_escrever:
            raise AcaoNaoAutorizada("Escrita não autorizada")
        if ferramenta.risco == "destrutiva" and not politica.permite_destruir:
            raise AcaoNaoAutorizada("Operação destrutiva não autorizada")
        if ferramenta.risco != "leitura":
            if not id_confirmacao or id_confirmacao not in politica.confirmacoes or id_confirmacao in self.confirmacoes_consumidas:
                raise AcaoNaoAutorizada("Falta confirmação de uso único")
        self.chamadas += 1
        if politica.simular:
            # Não revelar argumentos que podem conter dados privados.
            return {"estado": "simulacao", "nome": nome, "risco": ferramenta.risco}
        if ferramenta.risco != "leitura":
            self.confirmacoes_consumidas.add(str(id_confirmacao))
        try:
            resultado = ferramenta.executor(dict(entrada))
            if not isinstance(resultado, dict):
                raise TypeError("Retorno inválido")
            return resultado
        except Exception as exc:
            raise RuntimeError(f"Falha da ferramenta: {type(exc).__name__}") from None
