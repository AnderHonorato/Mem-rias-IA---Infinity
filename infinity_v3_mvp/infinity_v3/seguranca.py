"""Barreiras conservadoras para evitar a indexação acidental de credenciais.

Heurísticas não substituem classificação humana, autenticação ou criptografia.
O conteúdo detectado jamais deve aparecer em mensagens de erro ou logs.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RiscoDetectado:
    categoria: str
    gravidade: str = "bloqueante"


_PADROES = (
    ("chave_privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.I)),
    ("chave_api", re.compile(r"\b(?:sk-(?:proj-|live-|test-)?[A-Za-z0-9_-]{18,}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{15,}|AKIA[0-9A-Z]{16})\b")),
    ("senha_explicita", re.compile(r"(?i)\b(?:senha|password|passwd|api[_ -]?key|access[_ -]?token|secret[_ -]?key)\s*[:=]\s*[^\s,;]{6,}")),
    ("documento_cpf", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
)


def analisar_riscos(*textos: str) -> tuple[RiscoDetectado, ...]:
    """Retorna somente tipos dos indícios; nunca devolve o segredo encontrado."""
    encontrado: set[str] = set()
    for texto in textos:
        if not isinstance(texto, str):
            continue
        for categoria, padrao in _PADROES:
            if categoria not in encontrado and padrao.search(texto):
                encontrado.add(categoria)
    return tuple(RiscoDetectado(categoria) for categoria in sorted(encontrado))


def exigir_sem_segredos(*textos: str) -> None:
    if analisar_riscos(*textos):
        raise ValueError("Conteúdo potencialmente sensível: armazenamento bloqueado")
