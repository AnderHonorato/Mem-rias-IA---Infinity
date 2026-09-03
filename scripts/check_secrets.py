#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import ROOT, V2_TEXT_ROOTS, iter_files, relative

PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "generic-secret-assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|client[_-]?secret)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{12,}"
    ),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}


def detect(text: str) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            found.append((name, text.count("\n", 0, match.start()) + 1))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="inclui legado; pode gerar avisos históricos")
    args = parser.parse_args()
    roots = [ROOT] if args.all else list(V2_TEXT_ROOTS) + [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / "GEMINI.md", ROOT / ".github"]
    hits: list[str] = []
    suffixes = (".md", ".py", ".json", ".yml", ".yaml", ".txt")
    for path in iter_files(roots, suffixes=suffixes):
        if any(part in {".git", "node_modules", "dist", "build"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, line in detect(text):
            hits.append(f"{relative(path)}:{line} [{name}]")
    if hits:
        print("POSSÍVEIS SEGREDOS (valor omitido)")
        for hit in hits:
            print(f"- {hit}")
        return 1
    print("SECRETS OK: nenhum padrão sensível detectado no escopo V2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
