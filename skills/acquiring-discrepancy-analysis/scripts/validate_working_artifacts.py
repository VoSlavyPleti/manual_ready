"""Validate mandatory source-map artifacts before final legal comparison.

This helper is mechanical. It checks source-map coverage only; it does not
extract legal entities, decide analogues, or decide statuses.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


CLAUSE_RE = re.compile(r"(?m)^\s*(\d+(?:\.\d+)*)\.?\s*(?=\S)")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def matrix_ids(path: Path) -> set[str]:
    data = read_json(path)
    if not isinstance(data, list):
        raise ValueError("matrix must be a JSON array")
    return {
        str(item.get("number", "")).strip()
        for item in data
        if isinstance(item, dict) and str(item.get("number", "")).strip()
    }


def contract_ids(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    return [match.group(1).rstrip(".") for match in CLAUSE_RE.finditer(text)]


def rows_from(data: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if not isinstance(data, dict):
        return []
    for key in keys:
        value = data.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
    return []


def proposition_rows(data: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if isinstance(data, dict):
        matrix = rows_from(data, "matrix", "matrix_items", "matrix_propositions")
        contract = rows_from(data, "contract", "contract_items", "contract_propositions")
        if matrix or contract:
            return matrix, contract
        rows = rows_from(data, "propositions", "items")
        return rows, []
    if isinstance(data, list):
        rows = rows_from(data)
        return rows, []
    return [], []


def row_id(row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(row.get(key, "")).strip()
        if value:
            return value
    return ""


def validate(matrix_path: Path, contract_path: Path, working_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    expected_matrix_ids = matrix_ids(matrix_path)
    source_contract_ids = contract_ids(contract_path)

    clause_path = working_dir / "clause_index.json"
    propositions_path = working_dir / "legal_propositions.json"
    if not clause_path.exists():
        errors.append("missing_clause_index")
        clause_index = {}
    else:
        clause_index = read_json(clause_path)

    matrix_rows = rows_from(clause_index, "matrix_items", "matrix_index", "matrix")
    contract_rows = rows_from(clause_index, "contract_items", "contract_index", "contract")
    indexed_matrix_ids = {row_id(row, "id", "number", "matrix_id") for row in matrix_rows}
    indexed_matrix_ids.discard("")

    missing_matrix = sorted(expected_matrix_ids - indexed_matrix_ids)
    extra_matrix = sorted(indexed_matrix_ids - expected_matrix_ids)
    if missing_matrix:
        errors.append(f"clause_index_missing_matrix_ids:{len(missing_matrix)}")
    if extra_matrix:
        errors.append(f"clause_index_unknown_matrix_ids:{len(extra_matrix)}")
    if len(indexed_matrix_ids) < len(expected_matrix_ids):
        errors.append(
            f"clause_index_matrix_subset:{len(indexed_matrix_ids)}/{len(expected_matrix_ids)}"
        )

    if len(contract_rows) < max(20, int(len(set(source_contract_ids)) * 0.6)):
        errors.append(
            f"clause_index_contract_too_small:{len(contract_rows)}/{len(set(source_contract_ids))}"
        )

    duplicate_contract_ids = [
        item for item, count in Counter(source_contract_ids).items() if count > 1
    ]
    if duplicate_contract_ids:
        contextual = 0
        for row in contract_rows:
            if row_id(row, "id", "contract_id") in duplicate_contract_ids and any(
                row.get(key)
                for key in (
                    "source_locator",
                    "locator",
                    "context",
                    "section_context",
                    "appendix",
                    "line",
                    "line_start",
                )
            ):
                contextual += 1
        if contextual == 0:
            warnings.append(
                f"duplicate_contract_ids_without_context:{len(duplicate_contract_ids)}"
            )

    matrix_propositions: list[dict[str, Any]] = []
    contract_propositions: list[dict[str, Any]] = []
    if not propositions_path.exists():
        errors.append("missing_legal_propositions")
    else:
        matrix_propositions, contract_propositions = proposition_rows(
            read_json(propositions_path)
        )

        proposition_matrix_ids = {
            row_id(row, "id", "number", "matrix_id")
            for row in matrix_propositions
        }
        proposition_matrix_ids.discard("")
        missing_proposition_matrix = sorted(expected_matrix_ids - proposition_matrix_ids)
        if missing_proposition_matrix:
            errors.append(
                f"legal_propositions_missing_matrix_ids:{len(missing_proposition_matrix)}"
            )

        if len(contract_propositions) < max(20, int(len(set(source_contract_ids)) * 0.6)):
            errors.append(
                "legal_propositions_contract_too_small:"
                f"{len(contract_propositions)}/{len(set(source_contract_ids))}"
            )

        missing_materiality = 0
        invalid_materiality = 0
        unresolved_review = 0
        missing_source_text = 0
        weak_rows = 0
        for row in matrix_propositions + contract_propositions:
            materiality = str(row.get("materiality", "")).strip()
            if not materiality:
                missing_materiality += 1
            elif materiality not in {
                "evaluable",
                "not_material",
                "heading",
                "needs_source_review",
            }:
                invalid_materiality += 1
            if materiality == "needs_source_review":
                unresolved_review += 1
            if not str(row.get("source_text", "")).strip():
                missing_source_text += 1

            if materiality in {"evaluable", "needs_source_review"}:
                has_core = all(
                    str(row.get(key, "")).strip()
                    for key in ("right_or_obligation", "legal_object")
                )
                has_party = bool(
                    str(row.get("protected_party", "")).strip()
                    or str(row.get("bound_party", "")).strip()
                )
                has_evidence = bool(str(row.get("source_excerpt", "")).strip())
                if not (has_core and has_party and has_evidence):
                    weak_rows += 1

        if missing_materiality:
            errors.append(f"legal_propositions_missing_materiality:{missing_materiality}")
        if invalid_materiality:
            errors.append(f"legal_propositions_invalid_materiality:{invalid_materiality}")
        if unresolved_review:
            errors.append(f"legal_propositions_needs_source_review:{unresolved_review}")
        if missing_source_text:
            errors.append(f"legal_propositions_missing_source_text:{missing_source_text}")
        if weak_rows:
            warnings.append(f"legal_propositions_weak_evaluable_rows:{weak_rows}")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "expected_matrix_ids": len(expected_matrix_ids),
            "clause_index_matrix_ids": len(indexed_matrix_ids),
            "clause_index_contract_rows": len(contract_rows),
            "source_contract_unique_ids": len(set(source_contract_ids)),
            "duplicate_contract_ids": len(duplicate_contract_ids),
            "legal_proposition_matrix_rows": len(matrix_propositions),
            "legal_proposition_contract_rows": len(contract_propositions),
            "legal_proposition_rows": len(matrix_propositions) + len(contract_propositions),
        },
        "samples": {
            "missing_matrix_ids": missing_matrix[:20],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=Path("inputs/matrix.json"))
    parser.add_argument("--contract", type=Path, default=Path("inputs/contract.txt"))
    parser.add_argument("--working", type=Path, default=Path("outputs/working"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = validate(args.matrix, args.contract, args.working)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
