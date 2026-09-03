#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date

from common import load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="falha quando review_after venceu")
    args = parser.parse_args()
    today = date.today()
    stale: list[str] = []
    for record in load_records():
        value = record["data"].get("review_after")
        if not value:
            continue
        try:
            review = value if isinstance(value, date) else date.fromisoformat(str(value))
        except ValueError:
            stale.append(f"{record['path']}: review_after inválido {value!r}")
            continue
        if review < today and record["data"].get("status") == "active":
            stale.append(f"{record['path']}: revisão vencida em {review.isoformat()}")
    for item in stale:
        print(f"AVISO: {item}")
    if stale and args.strict:
        return 1
    print(f"FRESHNESS OK: {len(stale)} aviso(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
