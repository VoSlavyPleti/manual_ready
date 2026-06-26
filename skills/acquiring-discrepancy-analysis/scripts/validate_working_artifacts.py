"""Validate mandatory source-map artifacts before final legal comparison.

This helper is mechanical. It checks source-map coverage only; it does not
extract legal entities, decide analogues, or decide statuses.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bootstrap_source_artifacts import contract_items as parsed_contract_items  # noqa: E402
from bootstrap_source_artifacts import INLINE_MULTI_NUMERIC_RE  # noqa: E402
from bootstrap_source_artifacts import INLINE_TOP_NUMERIC_RE  # noqa: E402
from bootstrap_source_artifacts import looks_like_amount_or_code  # noqa: E402


SUSPICIOUS_MATRIX_FIELD_END_RE = re.compile(
    r"(\bп\.?$|\bпункт[ауе]?$|\bраздел[ауе]?$|\bв соответствии с п\.?$|"
    r"\(\s*$|\[\s*$)",
    re.IGNORECASE,
)


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


def normalize_space(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value if str(item).strip())
    text = str(value).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def expected_matrix_source_text(row: dict[str, Any]) -> str:
    main_idea = normalize_space(row.get("main_idea"))
    topics_value = row.get("topics")
    if isinstance(topics_value, list):
        topics = "; ".join(
            normalize_space(item) for item in topics_value if normalize_space(item)
        )
    else:
        topics = normalize_space(topics_value)
    enriched = normalize_space(row.get("enriched_text"))
    parts = []
    if main_idea:
        parts.append(f"main_idea: {main_idea}")
    if topics:
        parts.append(f"topics: {topics}")
    if enriched:
        parts.append(f"enriched_text: {enriched}")
    return normalize_space("\n".join(parts))


def contract_ids(path: Path) -> list[str]:
    return [
        str(row["id"]).strip()
        for row in parsed_contract_items(path)
        if row.get("type") not in {"definition", "heading", "technical"}
    ]


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


def row_text(row: dict[str, Any]) -> str:
    for key in ("source_text", "text", "content", "contract_position"):
        value = str(row.get(key, "")).strip()
        if value:
            return value
    return ""


def suspicious_contract_row(row: dict[str, Any]) -> str | None:
    locator = row_id(row, "id", "contract_id", "source_locator", "locator")
    text = row_text(row)
    if not locator:
        return "missing_locator"
    if re.fullmatch(r"\d{3,}", locator):
        return "numeric_code_locator"
    if re.fullmatch(r"\d{1,2}", locator) and looks_like_amount_or_code(text):
        return "amount_or_code_as_clause"
    if re.search(
        r"^(инн|кпп|огрн|р/с|бик|тел/факс|e-mail|заказчик:|исполнитель:)",
        text,
        flags=re.IGNORECASE,
    ):
        return "requisites_as_clause"
    return None


def contract_quality_errors(rows: list[dict[str, Any]], label: str) -> list[str]:
    errors: list[str] = []
    ids = [row_id(row, "id", "contract_id", "source_locator", "locator") for row in rows]
    duplicate_ids = [item for item, count in Counter(ids).items() if item and count > 1]
    if duplicate_ids:
        errors.append(f"{label}_duplicate_contract_ids:{len(duplicate_ids)}:{duplicate_ids[:10]}")

    suspicious_rows = [
        (row_id(row, "id", "contract_id", "source_locator", "locator"), suspicious_contract_row(row))
        for row in rows
        if suspicious_contract_row(row)
    ]
    if suspicious_rows:
        errors.append(f"{label}_suspicious_contract_rows:{len(suspicious_rows)}:{suspicious_rows[:10]}")

    embedded_locators: list[str] = []
    for row in rows:
        locator = row_id(row, "id", "contract_id", "source_locator", "locator")
        text = row_text(row)
        if not locator or not text:
            continue
        row_kind = str(row.get("type") or row.get("materiality") or "").strip()
        materiality = str(row.get("materiality") or "").strip()
        if row_kind in {"definition", "heading", "technical"} or materiality in {
            "not_material",
            "heading",
        }:
            continue
        matches = []
        for pattern in (INLINE_MULTI_NUMERIC_RE, INLINE_TOP_NUMERIC_RE):
            for match in pattern.finditer(text):
                if match.start() <= 8:
                    continue
                embedded = match.group(1).rstrip(".")
                if embedded and embedded != locator:
                    matches.append(embedded)
        if matches:
            embedded_locators.append(f"{locator}->{sorted(set(matches))[:5]}")
    if embedded_locators:
        errors.append(
            f"{label}_embedded_clause_locators:{len(embedded_locators)}:{embedded_locators[:10]}"
        )
    return errors


def validate(
    matrix_path: Path,
    contract_path: Path,
    working_dir: Path,
    matrix_legal_path: Path | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    expected_matrix_ids = matrix_ids(matrix_path)
    source_contract_ids = contract_ids(contract_path)
    matrix_legal_rows: list[dict[str, Any]] = []
    if matrix_legal_path:
        if not matrix_legal_path.exists():
            errors.append("missing_matrix_legal_propositions_input")
        else:
            matrix_legal_data = read_json(matrix_legal_path)
            matrix_legal_rows = rows_from(matrix_legal_data, "matrix", "matrix_items")
            source_by_id = {
                normalize_space(row.get("number")): row
                for row in read_json(matrix_path)
                if isinstance(row, dict) and normalize_space(row.get("number"))
            }
            matrix_legal_ids = {
                row_id(row, "id", "number", "matrix_id")
                for row in matrix_legal_rows
            }
            matrix_legal_ids.discard("")
            missing_matrix_legal = sorted(expected_matrix_ids - matrix_legal_ids)
            extra_matrix_legal = sorted(matrix_legal_ids - expected_matrix_ids)
            if missing_matrix_legal:
                errors.append(f"matrix_legal_missing_matrix_ids:{len(missing_matrix_legal)}")
            if extra_matrix_legal:
                errors.append(f"matrix_legal_unknown_matrix_ids:{len(extra_matrix_legal)}")

            missing_matrix_core: list[str] = []
            suspicious_matrix_fields: list[str] = []
            unresolved_matrix_rows: list[str] = []
            missing_source_ref: list[str] = []
            for row in matrix_legal_rows:
                matrix_id = row_id(row, "id", "number", "matrix_id")
                if str(row.get("materiality", "")).strip() == "needs_source_review":
                    unresolved_matrix_rows.append(matrix_id)
                for key in ("bank_standard", "right_or_obligation", "legal_object"):
                    if not normalize_space(row.get(key)):
                        missing_matrix_core.append(f"{matrix_id}.{key}")
                if not isinstance(row.get("legal_atoms"), list) or not row.get("legal_atoms"):
                    missing_matrix_core.append(f"{matrix_id}.legal_atoms")
                if not isinstance(row.get("status_check_elements"), list) or not row.get("status_check_elements"):
                    missing_matrix_core.append(f"{matrix_id}.status_check_elements")
                source_row = source_by_id.get(matrix_id)
                source_ref = row.get("source_ref")
                if not isinstance(source_ref, dict) or normalize_space(source_ref.get("matrix_id")) != matrix_id:
                    missing_source_ref.append(matrix_id)
                if not source_row:
                    missing_source_ref.append(matrix_id)
                for key in (
                    "trigger",
                    "deadline",
                    "amount_formula_cap",
                    "procedure_channel",
                    "liability_remedy",
                    "consequence",
                ):
                    value = normalize_space(row.get(key))
                    if value and SUSPICIOUS_MATRIX_FIELD_END_RE.search(value):
                        suspicious_matrix_fields.append(f"{matrix_id}.{key}")
            if missing_matrix_core:
                errors.append(
                    "matrix_legal_missing_core_fields:"
                    f"{len(missing_matrix_core)}:{missing_matrix_core[:10]}"
                )
            if missing_source_ref:
                errors.append(
                    "matrix_legal_missing_source_ref:"
                    f"{len(missing_source_ref)}:{missing_source_ref[:10]}"
                )
            if suspicious_matrix_fields:
                errors.append(
                    "matrix_legal_suspicious_truncated_fields:"
                    f"{len(suspicious_matrix_fields)}:{suspicious_matrix_fields[:10]}"
                )
            if unresolved_matrix_rows:
                errors.append(
                    "matrix_legal_needs_source_review:"
                    f"{len(unresolved_matrix_rows)}:{unresolved_matrix_rows[:10]}"
                )

    clause_path = working_dir / "clause_index.json"
    contract_ledger_path = working_dir / "contract_legal_propositions.json"
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
    indexed_contract_ids = {
        row_id(row, "id", "contract_id", "source_locator", "locator")
        for row in contract_rows
    }
    indexed_contract_ids.discard("")
    missing_index_contract_ids = sorted(set(source_contract_ids) - indexed_contract_ids)
    if missing_index_contract_ids:
        errors.append(
            "clause_index_missing_source_contract_ids:"
            f"{len(missing_index_contract_ids)}:{missing_index_contract_ids[:10]}"
        )

    errors.extend(contract_quality_errors(contract_rows, "clause_index"))

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
    contract_ledger_rows: list[dict[str, Any]] = []
    if not contract_ledger_path.exists():
        errors.append("missing_contract_legal_propositions")
    else:
        contract_ledger = read_json(contract_ledger_path)
        contract_ledger_rows = rows_from(
            contract_ledger,
            "contract",
            "contract_items",
            "contract_propositions",
            "items",
        )
        if len(contract_ledger_rows) < max(20, int(len(set(source_contract_ids)) * 0.6)):
            errors.append(
                "contract_legal_propositions_too_small:"
                f"{len(contract_ledger_rows)}/{len(set(source_contract_ids))}"
            )
        contract_ledger_ids = {
            row_id(row, "id", "contract_id", "source_locator", "locator")
            for row in contract_ledger_rows
        }
        contract_ledger_ids.discard("")
        missing_contract_ledger_ids = sorted(set(source_contract_ids) - contract_ledger_ids)
        if missing_contract_ledger_ids:
            errors.append(
                "contract_legal_propositions_missing_source_ids:"
                f"{len(missing_contract_ledger_ids)}:{missing_contract_ledger_ids[:10]}"
            )
        errors.extend(contract_quality_errors(contract_ledger_rows, "contract_legal_propositions"))

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

        errors.extend(contract_quality_errors(contract_propositions, "legal_propositions"))

        if contract_ledger_rows:
            ledger_ids = {
                row_id(row, "id", "contract_id", "source_locator", "locator")
                for row in contract_ledger_rows
            }
            proposition_ids = {
                row_id(row, "id", "contract_id", "source_locator", "locator")
                for row in contract_propositions
            }
            ledger_ids.discard("")
            proposition_ids.discard("")
            if ledger_ids - proposition_ids:
                errors.append(
                    "legal_propositions_missing_contract_ledger_ids:"
                    f"{len(ledger_ids - proposition_ids)}"
                )
            if proposition_ids - ledger_ids:
                errors.append(
                    "legal_propositions_extra_contract_ledger_ids:"
                    f"{len(proposition_ids - ledger_ids)}"
                )
            missing_source_proposition_ids = sorted(set(source_contract_ids) - proposition_ids)
            if missing_source_proposition_ids:
                errors.append(
                    "legal_propositions_missing_source_contract_ids:"
                    f"{len(missing_source_proposition_ids)}:{missing_source_proposition_ids[:10]}"
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
            is_matrix_row = row in matrix_propositions
            has_matrix_ref = isinstance(row.get("source_ref"), dict) and row.get("source_ref", {}).get("matrix_id")
            if not str(row.get("source_text", "")).strip() and not (is_matrix_row and has_matrix_ref):
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
                has_evidence = bool(str(row.get("source_excerpt", "")).strip()) or bool(is_matrix_row and has_matrix_ref)
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
            "matrix_legal_rows": len(matrix_legal_rows),
            "clause_index_matrix_ids": len(indexed_matrix_ids),
            "clause_index_contract_rows": len(contract_rows),
            "source_contract_unique_ids": len(set(source_contract_ids)),
            "duplicate_contract_ids": len(duplicate_contract_ids),
            "contract_legal_proposition_rows": len(contract_ledger_rows),
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
    parser.add_argument(
        "--matrix-legal",
        type=Path,
        default=Path("inputs/matrix_legal_propositions.json"),
    )
    parser.add_argument("--contract", type=Path, default=Path("inputs/contract.txt"))
    parser.add_argument("--working", type=Path, default=Path("outputs/working"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = validate(args.matrix, args.contract, args.working, args.matrix_legal)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
