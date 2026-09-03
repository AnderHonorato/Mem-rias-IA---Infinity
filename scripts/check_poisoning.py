#!/usr/bin/env python3
from __future__ import annotations

import re

try:
    from .common import load_records
except ImportError:
    from common import load_records

SUSPICIOUS = [
    re.compile(r"ignore (?:all |the )?(?:previous|prior) instructions", re.I),
    re.compile(r"ignore suas instruções", re.I),
    re.compile(r"(?:reveal|expose|show) (?:the )?(?:system prompt|secret|token|password)", re.I),
    re.compile(r"(?:change|override|alter).{0,30}(?:permission|policy|instruction)", re.I),
]
UNTRUSTED_TYPES = {"external-source", "untrusted-external", "unknown", "tool-output", "other-ai"}


def suspicious(text: str) -> bool:
    return any(pattern.search(text) for pattern in SUSPICIOUS)


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    for record in load_records():
        data, body, path = record["data"], record["body"], record["path"]
        source = data.get("source") if isinstance(data.get("source"), dict) else {}
        origin = str(source.get("trust") or source.get("type") or "")
        if not suspicious(body):
            continue
        if path.startswith("knowledge/inbox/") or data.get("status") in {"draft", "review", "disputed"}:
            warnings.append(path)
        elif origin in UNTRUSTED_TYPES:
            failures.append(path)
    for path in warnings:
        print(f"AVISO: conteúdo suspeito isolado para revisão: {path}")
    if failures:
        print("MEMORY POISONING: conteúdo suspeito não confiável foi promovido")
        for path in failures:
            print(f"- {path}")
        return 1
    print("POISONING CHECK OK (heurístico; não substitui revisão semântica).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
