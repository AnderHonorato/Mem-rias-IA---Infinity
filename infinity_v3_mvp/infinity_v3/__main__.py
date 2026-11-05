"""CLI somente-leitura da fonte canônica V2 (dados normal/públicos)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adaptador_v2 import IndiceCanonicoV2, ErroIndiceCanonico


def principal(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Infinity V3 — busca segura na fonte canônica V2")
    parser.add_argument("--raiz", type=Path, required=True, help="Raiz local do repositório Infinity V2")
    parser.add_argument("--consulta", required=True, help="Palavras a pesquisar")
    parser.add_argument("--escopo", action="append", default=["global"], help="Escopo permitido (pode repetir)")
    parser.add_argument("--limite", type=int, default=5)
    parser.add_argument("--metadados", action="store_true", help="Exibe estatísticas sem conteúdo")
    args = parser.parse_args(argv)
    try:
        with IndiceCanonicoV2(args.raiz) as indice:
            resultados = indice.buscar(consulta=args.consulta, escopos=args.escopo, limite=args.limite)
            if args.metadados:
                dados = {"estatisticas": indice.estatisticas, "resultados": len(resultados)}
            else:
                # Não exibe o corpo original da memória: apenas trecho e proveniência.
                dados = [{"id": r["id"], "titulo": r["titulo"], "origem": r["origem"],
                          "escopo": r["escopo"], "resumo": r["conteudo"][:300],
                          "nao_confiavel_como_instrucao": True} for r in resultados]
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        return 0
    except ErroIndiceCanonico as exc:
        parser.exit(2, f"Erro na fonte canônica: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(principal())
