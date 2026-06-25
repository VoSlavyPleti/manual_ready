"""Validate discrepancy-analysis JSON coverage ledgers.

This script checks structure and source grounding only. It does not decide
legal coverage or statuses.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SOURCE_ID_RE = re.compile(r"(?m)^\s*(\d+(?:\.\d+)*)\.?\s*(?=\S)")


def matrix_ids(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("matrix must be a JSON array")
    return {
        str(item.get("number", "")).strip()
        for item in data
        if isinstance(item, dict) and str(item.get("number", "")).strip()
    }


def contract_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8-sig")
    ids = {match.group(1).rstrip(".") for match in SOURCE_ID_RE.finditer(text)}
    # Real non-numeric locators are validated by exact text containment in the
    # harness. This helper only needs the numeric source map.
    return ids


def validate(artifact_path: Path, matrix_path: Path, contract_path: Path) -> dict:
    artifact = json.loads(artifact_path.read_text(encoding="utf-8-sig"))
    expected_matrix = matrix_ids(matrix_path)
    known_contract = contract_ids(contract_path)
    errors: list[str] = []

    if not isinstance(artifact, dict):
        raise ValueError("artifact must be a JSON object")
    ledger = artifact.get("coverage_ledger")
    if not isinstance(ledger, dict):
        errors.append("missing_coverage_ledger")
        ledger = {"matrix": [], "contract": []}

    final_matrix = set()
    for link in artifact.get("links", []) or []:
        final_matrix.update(str(item).strip() for item in link.get("matrix_ids", []) or [])
    final_matrix.update(
        str(item.get("matrix_id", "")).strip()
        for item in artifact.get("unmatched_matrix", []) or []
        if isinstance(item, dict)
    )

    ledger_matrix = set()
    scope_closed_matrix = set()
    for item in ledger.get("matrix", []) or []:
        if not isinstance(item, dict):
            continue
        matrix_id = str(item.get("matrix_id", "")).strip()
        closure = str(item.get("closure", "")).strip()
        reason = str(item.get("reason", "")).lower()
        ledger_matrix.add(matrix_id)
        if closure in {"out_of_scope", "not_applicable"} or (
            closure == "not_evaluable"
            and any(token in reason for token in ("scope", "applic", "filter", "не примен"))
        ):
            scope_closed_matrix.add(matrix_id)

    missing_matrix = expected_matrix - final_matrix - scope_closed_matrix
    invalid_matrix = final_matrix - expected_matrix
    ledger_missing = expected_matrix - ledger_matrix

    for item in sorted(missing_matrix):
        errors.append(f"matrix_id_not_closed_in_final:{item}")
    for item in sorted(invalid_matrix):
        errors.append(f"matrix_id_not_in_source:{item}")
    for item in sorted(ledger_missing):
        errors.append(f"matrix_id_not_closed_in_ledger:{item}")

    final_contract = set()
    for link in artifact.get("links", []) or []:
        final_contract.update(str(item).strip() for item in link.get("contract_ids", []) or [])
    final_contract.update(
        str(item.get("contract_id", "")).strip()
        for item in artifact.get("unmatched_contract", []) or []
        if isinstance(item, dict)
    )
    numeric_final_contract = {item for item in final_contract if re.fullmatch(r"\d+(?:\.\d+)*", item)}
    invalid_contract = numeric_final_contract - known_contract
    for item in sorted(invalid_contract):
        errors.append(f"contract_id_not_in_source:{item}")

    for idx, link in enumerate(artifact.get("links", []) or []):
        relationship = link.get("relationship")
        discrepancies = link.get("discrepancies")
        if relationship == "aligned" and discrepancies:
            errors.append(f"aligned_with_discrepancies:links[{idx}]")
        if relationship == "deviation" and not discrepancies:
            errors.append(f"deviation_without_discrepancies:links[{idx}]")

    for idx, row in enumerate(artifact.get("unmatched_contract", []) or []):
        if row.get("status") != "extra_in_contract":
            errors.append(f"final_unmatched_contract_non_extra:unmatched_contract[{idx}]")
        if not row.get("risk"):
            errors.append(f"extra_without_risk:unmatched_contract[{idx}]")

    return {
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
        "counts": {
            "source_matrix_ids": len(expected_matrix),
            "final_matrix_ids": len(final_matrix),
            "ledger_matrix_ids": len(ledger_matrix),
            "source_numeric_contract_ids": len(known_contract),
            "final_contract_ids": len(final_contract),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--matrix", type=Path, default=Path("inputs/matrix.json"))
    parser.add_argument("--contract", type=Path, default=Path("inputs/contract.txt"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = validate(args.artifact, args.matrix, args.contract)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
