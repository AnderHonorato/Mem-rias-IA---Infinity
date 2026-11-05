"""Cache de RAM com TTL somente para resultados públicos e não sensíveis."""
from __future__ import annotations

import hashlib
import copy
import time
from collections import OrderedDict
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class CachePublico(Generic[T]):
    def __init__(self, *, capacidade: int = 128, ttl_segundos: int = 120,
                 relogio: Callable[[], float] = time.monotonic) -> None:
        if not 1 <= capacidade <= 10000 or not 1 <= ttl_segundos <= 86400:
            raise ValueError("Parâmetros do cache inválidos")
        self.capacidade = capacidade
        self.ttl = ttl_segundos
        self.relogio = relogio
        self._dados: OrderedDict[str, tuple[float, T]] = OrderedDict()

    @staticmethod
    def chave(*, consulta: str, escopo: str, revisao_fonte: str) -> str:
        return hashlib.sha256("\x1f".join((consulta, escopo, revisao_fonte)).encode()).hexdigest()

    def obter(self, chave: str, *, sensibilidade: str = "nao_classificada") -> T | None:
        if sensibilidade != "publica":
            return None
        registro = self._dados.get(chave)
        if registro is None:
            return None
        expira, valor = registro
        if self.relogio() >= expira:
            del self._dados[chave]
            return None
        self._dados.move_to_end(chave)
        return copy.deepcopy(valor)

    def guardar(self, chave: str, valor: T, *, sensibilidade: str = "nao_classificada") -> bool:
        if sensibilidade != "publica":
            return False
        self._dados[chave] = (self.relogio() + self.ttl, copy.deepcopy(valor))
        self._dados.move_to_end(chave)
        while len(self._dados) > self.capacidade:
            self._dados.popitem(last=False)
        return True

    def invalidar(self) -> None:
        self._dados.clear()
