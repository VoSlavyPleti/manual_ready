"""Derive compatibility artifacts from proposition ledgers.

This script is mechanical. It takes the reusable matrix legal ledger and the
agent-reviewed contract legal ledger, then writes:

- clause_index.json
- legal_propositions.json

It does not decide legal analogues or statuses.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def rows_from(data: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []


def compact_row(row: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in keys:
        if key in row:
            result[key] = row[key]
    return result


def matrix_index_rows(matrix_path: Path, matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    raw = read_json(matrix_path)
    raw_by_id = {
        str(row.get("number", "")).strip(): row
        for row in raw
        if isinstance(row, dict) and str(row.get("number", "")).strip()
    }
    result: list[dict[str, Any]] = []
    for index, row in enumerate(matrix_rows):
        matrix_id = str(row.get("id") or row.get("number") or "").strip()
        raw_row = raw_by_id.get(matrix_id, {})
        result.append(
            {
                "id": matrix_id,
                "number": matrix_id,
                "source_index": raw_row.get("source_index", index),
                "type": row.get("type", "operative"),
                "source_text": row.get("source_text") or raw_row.get("enriched_text", ""),
                "main_idea": row.get("main_idea", raw_row.get("main_idea", "")),
                "topics": row.get("topics", raw_row.get("topics", [])),
                "enriched_text": row.get("enriched_text", raw_row.get("enriched_text", "")),
                "applicability": row.get("applicability_filters", {}),
            }
        )
    return result


def contract_index_rows(contract_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = (
        "id",
        "contract_id",
        "source_locator",
        "line_start",
        "line_end",
        "section_context",
        "type",
        "source_text",
        "final_allowed",
        "evidence_only",
    )
    result: list[dict[str, Any]] = []
    for row in contract_rows:
        out = compact_row(row, keys)
        locator = str(out.get("id") or out.get("contract_id") or out.get("source_locator") or "").strip()
        if locator:
            out["id"] = locator
            out.setdefault("contract_id", locator)
            out.setdefault("source_locator", locator)
        result.append(out)
    return result


def derive(
    matrix_path: Path,
    matrix_legal_path: Path,
    contract_ledger_path: Path,
    working_dir: Path,
) -> dict[str, Any]:
    matrix_legal = read_json(matrix_legal_path)
    contract_ledger = read_json(contract_ledger_path)
    matrix_rows = rows_from(matrix_legal, "matrix", "matrix_items")
    contract_rows = rows_from(contract_ledger, "contract", "contract_items", "items")
    if not matrix_rows:
        raise ValueError(f"No matrix rows in {matrix_legal_path}")
    if not contract_rows:
        raise ValueError(f"No contract rows in {contract_ledger_path}")

    clause_index = {
        "matrix_items": matrix_index_rows(matrix_path, matrix_rows),
        "contract_items": contract_index_rows(contract_rows),
        "source_files": {
            "matrix": str(matrix_path),
            "matrix_legal": str(matrix_legal_path),
            "contract_legal_propositions": str(contract_ledger_path),
        },
    }
    legal_propositions = {
        "matrix": matrix_rows,
        "contract": contract_rows,
    }

    working_dir.mkdir(parents=True, exist_ok=True)
    (working_dir / "clause_index.json").write_text(
        json.dumps(clause_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (working_dir / "legal_propositions.json").write_text(
        json.dumps(legal_propositions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {
        "matrix_rows": len(matrix_rows),
        "contract_rows": len(contract_rows),
        "wrote": ["clause_index.json", "legal_propositions.json"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=Path("inputs/matrix.json"))
    parser.add_argument(
        "--matrix-legal",
        type=Path,
        default=Path("inputs/matrix_legal_propositions.json"),
    )
    parser.add_argument(
        "--contract-ledger",
        type=Path,
        default=Path("outputs/working/contract_legal_propositions.json"),
    )
    parser.add_argument("--working", type=Path, default=Path("outputs/working"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = derive(args.matrix, args.matrix_legal, args.contract_ledger, args.working)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
