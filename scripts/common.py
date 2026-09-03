from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
STRUCTURED_ROOTS = (ROOT / "knowledge", ROOT / "events", ROOT / "reflections")
V2_TEXT_ROOTS = (
    ROOT / "knowledge",
    ROOT / "events",
    ROOT / "reflections",
    ROOT / "agents",
    ROOT / "coordination",
    ROOT / "skills",
    ROOT / "schemas",
    ROOT / "scripts",
    ROOT / "docs",
    ROOT / "tests",
    ROOT / "indexes",
)

RELATION_FIELDS = (
    "derived_from",
    "supersedes",
    "superseded_by",
    "related_error",
    "related_success",
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_files(roots: Iterable[Path], suffixes: tuple[str, ...] = (".md",)):
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        if root.is_file():
            candidates = [root]
        else:
            candidates = root.rglob("*")
        for path in candidates:
            if path.is_file() and path.suffix.lower() in suffixes and path not in seen:
                seen.add(path)
                yield path


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"frontmatter sem fechamento em {relative(path)}")
    raw = text[4:end]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter deve ser objeto em {relative(path)}")
    return data, text[end + 5 :]


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in iter_files(STRUCTURED_ROOTS):
        data, body = parse_frontmatter(path)
        if data is None:
            continue
        records.append({"path": relative(path), "file": path, "data": data, "body": body})
    return records


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def title_from_body(body: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def relation_values(data: dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in RELATION_FIELDS:
        value = data.get(field)
        if isinstance(value, str) and value:
            values.append((field, value))
        elif isinstance(value, list):
            values.extend((field, item) for item in value if isinstance(item, str) and item)
    return values
