"""Microbenchmark reprodutível com dados sintéticos (sem informações pessoais).

Compare execuções no MESMO dispositivo; não estabelece SLA universal.
"""
from __future__ import annotations

import json
import statistics
import tempfile
import time
from pathlib import Path

from infinity_v3.motor import MotorMemoria
from infinity_v3.cache import CachePublico


def medir(quantidade: int = 300, consultas: int = 150) -> dict[str, object]:
    if not 10 <= quantidade <= 10000 or not 10 <= consultas <= 50000:
        raise ValueError("Volume fora do limite")
    with tempfile.TemporaryDirectory() as tmp, MotorMemoria(Path(tmp) / "desempenho.db") as motor:
        inicio = time.perf_counter()
        for i in range(quantidade):
            motor.registrar(usuario="fixture", escopo="global", titulo=f"Padrão fictício {i}",
                conteudo=f"Validar código Python e testes de regressão no exemplo {i}",
                origem="fixture-de-benchmark", aprovado=True)
        duracao_ingestao = time.perf_counter() - inicio
        medidas = []
        cache = CachePublico[list](capacidade=5, ttl_segundos=30)
        revisao = "fixture-v1"
        for _ in range(consultas):
            inicio = time.perf_counter()
            motor.buscar(usuario="fixture", escopos=["global"], consulta="regressão Python", limite=8)
            medidas.append((time.perf_counter() - inicio) * 1000)
        medidas.sort()
        # Cache público explicitamente rotulado em RAM.
        chave = cache.chave(consulta="regressão Python", escopo="global", revisao_fonte=revisao)
        cache.guardar(chave, ["resultado público fictício"], sensibilidade="publica")
        inicio = time.perf_counter()
        for _ in range(consultas):
            cache.obter(chave, sensibilidade="publica")
        duracao_cache = ((time.perf_counter() - inicio) / consultas) * 1000
    return {"quantidade": quantidade, "consultas": consultas,
        "ingestao_segundos": round(duracao_ingestao, 4),
        "fts_mediana_ms": round(statistics.median(medidas), 4),
        "fts_p95_ms": round(medidas[max(0, int(len(medidas) * 0.95) - 1)], 4),
        "cache_mediana_aproximada_ms": round(duracao_cache, 4),
        "observacao": "Ambiente e carga locais; resultado não é promessa de velocidade para o GPT."}


if __name__ == "__main__":
    print(json.dumps(medir(), ensure_ascii=False, indent=2))
