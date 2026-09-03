#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict

from common import load_records


def main() -> int:
    by_id: dict[str, list[str]] = defaultdict(list)
    by_key: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for record in load_records():
        data = record["data"]
        path = record["path"]
        by_id[str(data.get("id", ""))].append(path)
        subject = data.get("subject")
        if subject:
            by_key[(str(data.get("type")), str(data.get("scope")), str(subject))].append(path)

    failures = [f"ID {key}: {paths}" for key, paths in by_id.items() if key and len(paths) > 1]
    warnings = [f"possível duplicação {key}: {paths}" for key, paths in by_key.items() if len(paths) > 1]
    for warning in warnings:
        print(f"AVISO: {warning}")
    if failures:
        for failure in failures:
            print(f"ERRO: {failure}")
        return 1
    print("DUPLICAÇÃO OK: nenhum ID duplicado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
