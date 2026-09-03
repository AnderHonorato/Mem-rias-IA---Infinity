#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from common import ROOT, V2_TEXT_ROOTS, iter_files, relative

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "data:")


def main() -> int:
    broken: list[str] = []
    roots = list(V2_TEXT_ROOTS) + [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / "GEMINI.md"]
    for path in iter_files(roots):
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split("#", 1)[0].strip().strip("<>")
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            target = unquote(target)
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                broken.append(f"{relative(path)} -> {raw} (fora do repositório)")
                continue
            if not resolved.exists():
                broken.append(f"{relative(path)} -> {raw}")
    if broken:
        print("LINKS QUEBRADOS")
        for item in broken:
            print(f"- {item}")
        return 1
    print("LINKS OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
