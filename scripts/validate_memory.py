#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from common import ROOT, load_records

SCHEMA_BY_TYPE = {
    "semantic-memory": "memory.schema.json",
    "preference": "memory.schema.json",
    "project": "project.schema.json",
    "event": "event.schema.json",
    "decision": "decision.schema.json",
    "decision-trace": "reflection.schema.json",
    "error": "lesson.schema.json",
    "success": "lesson.schema.json",
    "pattern": "lesson.schema.json",
}


def schema_for(record: dict) -> str | None:
    data = record["data"]
    path = record["path"]
    if path.startswith("events/"):
        return "event.schema.json"
    return SCHEMA_BY_TYPE.get(str(data.get("type", "")))


def main() -> int:
    errors: list[str] = []
    ids: dict[str, str] = {}
    schemas: dict[str, dict] = {}

    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        schemas[schema_path.name] = json.loads(schema_path.read_text(encoding="utf-8"))

    for record in load_records():
        data = record["data"]
        path = record["path"]
        record_id = data.get("id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{path}: id ausente")
        elif record_id in ids:
            errors.append(f"ID duplicado {record_id}: {ids[record_id]} e {path}")
        else:
            ids[record_id] = path

        schema_name = schema_for(record)
        if not schema_name:
            errors.append(f"{path}: tipo estruturado sem schema conhecido: {data.get('type')!r}")
            continue
        schema = schemas.get(schema_name)
        if not schema:
            errors.append(f"{path}: schema ausente: {schema_name}")
            continue
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            where = ".".join(str(p) for p in error.path) or "frontmatter"
            errors.append(f"{path}:{where}: {error.message}")

    if errors:
        print("VALIDAÇÃO FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDAÇÃO OK: {len(ids)} registros estruturados, IDs únicos e schemas válidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
