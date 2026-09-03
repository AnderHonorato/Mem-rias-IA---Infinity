#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .common import ROOT, load_records, relation_values, sha256_text, title_from_body
except ImportError:
    from common import ROOT, load_records, relation_values, sha256_text, title_from_body

INDEX_DIR = ROOT / "indexes"


def build() -> tuple[list[dict], list[dict], list[dict]]:
    records = load_records()
    catalog: list[dict] = []
    relations: list[dict] = []
    search: list[dict] = []
    for record in records:
        data, body, path = record["data"], record["body"], record["path"]
        record_id = str(data["id"])
        title = title_from_body(body, record_id)
        catalog.append({
            "id": record_id,
            "path": path,
            "type": data.get("type"),
            "status": data.get("status"),
            "scope": data.get("scope"),
            "updated_at": str(data.get("updated_at") or data.get("created_at") or data.get("occurred_at") or ""),
            "sha256": sha256_text(record["file"].read_text(encoding="utf-8")),
        })
        search.append({"id": record_id, "path": path, "title": title, "type": data.get("type"), "scope": data.get("scope")})
        for field, target in relation_values(data):
            relations.append({"from": record_id, "relation": field, "to": target})
    catalog.sort(key=lambda x: x["id"])
    search.sort(key=lambda x: x["id"])
    relations.sort(key=lambda x: (x["from"], x["relation"], x["to"]))
    return catalog, relations, search


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def core_catalog(items):
    if not isinstance(items, list):
        return None
    return sorted((x.get("id"), x.get("path"), x.get("type"), x.get("status"), x.get("scope")) for x in items if isinstance(x, dict))


def core_search(items):
    if not isinstance(items, list):
        return None
    return sorted((x.get("id"), x.get("path"), x.get("type"), x.get("scope")) for x in items if isinstance(x, dict))


def core_relations(items):
    if not isinstance(items, list):
        return None
    return sorted((x.get("from"), x.get("relation"), x.get("to")) for x in items if isinstance(x, dict))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog, relations, search = build()
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    if args.check:
        checks = {
            "catalog.json": core_catalog(load_json(INDEX_DIR / "catalog.json")) == core_catalog(catalog),
            "relations.json": core_relations(load_json(INDEX_DIR / "relations.json")) == core_relations(relations),
            "search-index.json": core_search(load_json(INDEX_DIR / "search-index.json")) == core_search(search),
        }
        stale = [name for name, ok in checks.items() if not ok]
        if stale:
            print("ÍNDICES DESATUALIZADOS: " + ", ".join(stale))
            print("Execute: python scripts/rebuild_indexes.py")
            return 1
        print("ÍNDICES OK: cobertura, caminhos, tipos, escopos e relações estão atualizados.")
        return 0
    paths = {
        "catalog.json": catalog,
        "relations.json": relations,
        "search-index.json": search,
    }
    for name, content in paths.items():
        (INDEX_DIR / name).write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ÍNDICES RECONSTRUÍDOS: {len(catalog)} registros, {len(relations)} relações.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
