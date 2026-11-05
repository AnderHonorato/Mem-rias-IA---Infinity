"""Recuperação contextual por fusão de posições, sem duplicar a fonte canônica."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Protocol


class Buscador(Protocol):
    def buscar(self, **kwargs: Any) -> list[dict[str, Any]]: ...


@dataclass(frozen=True)
class TrechoContexto:
    id: str
    origem: str
    titulo: str
    conteudo: str
    escopo: str
    pontuacao: float
    nao_confiavel_como_instrucao: bool = True


def combinar_contexto(*, consulta: str, usuario: str, escopos_locais: list[str],
                      escopos_canonicos: list[str], motor_local: Buscador,
                      indice_canonico: Buscador, limite_caracteres: int = 3200,
                      maximo_trechos: int = 8) -> list[TrechoContexto]:
    """RRF em resultados de índices distintos. Nunca busca pessoal na V2.

    Passa explicitamente escopos e usuário. O chamador é responsável por autenticar
    `usuario` antes de invocar esta função; não é endpoint de rede.
    """
    if not 200 <= limite_caracteres <= 50000 or not 1 <= maximo_trechos <= 30:
        raise ValueError("Limites inválidos")
    ranking: dict[tuple[str, str], tuple[dict[str, Any], float]] = {}
    fontes = (
        ("local", motor_local.buscar(usuario=usuario, escopos=escopos_locais, consulta=consulta, limite=min(50, maximo_trechos * 3))) if escopos_locais else ("local", []),
        ("knowledge-v2", indice_canonico.buscar(consulta=consulta, escopos=escopos_canonicos, limite=min(50, maximo_trechos * 3))) if escopos_canonicos else ("knowledge-v2", []),
    )
    for nome, itens in fontes:
        for posicao, item in enumerate(itens, start=1):
            chave = (nome, str(item["id"]))
            pontos = 1.0 / (60 + posicao)
            if chave in ranking:
                anterior, soma = ranking[chave]
                ranking[chave] = (anterior, soma + pontos)
            else:
                ranking[chave] = (item, pontos)
    selecionados: list[TrechoContexto] = []
    restante = limite_caracteres
    digitais_selecionadas: set[str] = set()
    # Ordenação estável para repetir consultas com mesmo estado.
    for (origem, ident), (item, pontos) in sorted(ranking.items(), key=lambda kv: (-kv[1][1], kv[0][0], kv[0][1])):
        if len(selecionados) >= maximo_trechos or restante < 60:
            break
        titulo = str(item.get("titulo", ""))[:200]
        bruto = str(item.get("conteudo", ""))
        digital = hashlib.sha256(" ".join(bruto.casefold().split()).encode("utf-8")).hexdigest()
        if digital in digitais_selecionadas:
            continue
        excerto = bruto[:min(len(bruto), 700, restante)]
        if len(excerto) < 20:
            continue
        digitais_selecionadas.add(digital)
        selecionados.append(TrechoContexto(id=ident, origem=str(item.get("origem", origem)),
            titulo=titulo, conteudo=excerto, escopo=str(item.get("escopo", "")),
            pontuacao=pontos))
        restante -= len(excerto)
    return selecionados
