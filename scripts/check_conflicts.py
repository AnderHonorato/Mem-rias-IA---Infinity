#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict

from common import load_records, relation_values

ACTIVE = {"active", "confirmed", "recorded"}


def main() -> int:
    records = load_records()
    ids = {str(r["data"].get("id")): r for r in records if r["data"].get("id")}
    errors: list[str] = []
    subjects: dict[tuple[str, str, str], list[str]] = defaultdict(list)

    for record in records:
        data = record["data"]
        path = record["path"]
        for field, target in relation_values(data):
            if target not in ids:
                errors.append(f"{path}: {field} referencia ID inexistente {target}")
        if data.get("status") in ACTIVE and data.get("subject"):
            key = (str(data.get("type")), str(data.get("scope")), str(data.get("subject")))
            subjects[key].append(str(data.get("id")))

    for key, values in subjects.items():
        if len(values) > 1:
            errors.append(f"múltiplos registros ativos para {key}: {values}; revisar semanticamente")

    if errors:
        print("CONFLITOS/REFERÊNCIAS A REVISAR")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONFLITOS OK: nenhuma relação quebrada ou conflito explícito detectado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
