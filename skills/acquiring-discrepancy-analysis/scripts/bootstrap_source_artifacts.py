"""Build source-map seed artifacts for discrepancy analysis.

This script is mechanical. It does not decide legal analogues or statuses.
It creates a complete clause index and a seed legal-proposition ledger that
must be enriched by the agent before final matching.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CLAUSE_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)\.?\s*(.+?)\s*$")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def compact(value: Any, limit: int = 800) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        text = "; ".join(str(item) for item in value if str(item).strip())
    elif isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False)
    else:
        text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def excerpt(text: str, limit: int = 240) -> str:
    return compact(text, limit=limit)


def proposition_seed(row: dict[str, Any], *, source: str) -> dict[str, Any]:
    source_text = compact(row.get("source_text"), limit=2400)
    row_type = row.get("type") or "operative"
    materiality = "heading" if row_type == "heading" else "needs_source_review"
    seed: dict[str, Any] = {
        "id": row.get("id") or row.get("number") or row.get("contract_id"),
        "source_text": source_text,
        "source_excerpt": excerpt(source_text),
        "type": row_type,
        "materiality": materiality,
        "protected_party": "",
        "bound_party": "",
        "right_or_obligation": "",
        "legal_object": "",
        "trigger": "",
        "deadline": "",
        "amount_formula_cap": "",
        "procedure_channel": "",
        "liability_remedy": "",
        "scope_options": [],
        "consequence": "",
    }
    if source == "matrix":
        seed["applicability_filters"] = row.get("applicability", {})
        seed["main_idea"] = row.get("main_idea", "")
        seed["topics"] = row.get("topics", "")
        seed["enriched_text"] = row.get("enriched_text", "")
    else:
        seed["source_locator"] = row.get("source_locator", row.get("contract_id", ""))
        seed["line_start"] = row.get("line_start")
        seed["line_end"] = row.get("line_end")
        seed["section_context"] = row.get("section_context", "")
    return seed


def matrix_items(matrix_path: Path) -> list[dict[str, Any]]:
    data = read_json(matrix_path)
    if not isinstance(data, list):
        raise ValueError("matrix.json must be an array")

    rows: list[dict[str, Any]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            continue
        matrix_id = compact(item.get("number"))
        if not matrix_id:
            continue
        source_parts = [
            compact(item.get("main_idea")),
            compact(item.get("topics")),
            compact(item.get("enriched_text"), limit=2000),
        ]
        rows.append(
            {
                "id": matrix_id,
                "number": matrix_id,
                "source_index": index,
                "type": "operative",
                "source_text": "\n".join(part for part in source_parts if part),
                "main_idea": item.get("main_idea", ""),
                "topics": item.get("topics", ""),
                "enriched_text": item.get("enriched_text", ""),
                "applicability": {
                    key: item.get(key)
                    for key in (
                        "required_type",
                        "requirement_type",
                        "only_for_product",
                        "only_for_lot",
                        "only_for_terminal",
                        "payment_method",
                    )
                    if key in item
                },
            }
        )
    return rows


def contract_items(contract_path: Path) -> list[dict[str, Any]]:
    text = contract_path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    starts: list[tuple[int, str, str, str]] = []
    current_heading = ""

    for line_no, line in enumerate(lines, start=1):
        match = CLAUSE_RE.match(line)
        if match:
            starts.append(
                (line_no, match.group(1).rstrip("."), match.group(2).strip(), current_heading)
            )
        elif line.strip() and not re.match(r"^\s*\d+(?:\.\d+)*", line):
            clean = re.sub(r"\s+", " ", line).strip()
            if len(clean) <= 160:
                current_heading = clean

    rows: list[dict[str, Any]] = []
    for idx, (line_no, clause_id, first_text, heading) in enumerate(starts):
        end_line = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else len(lines)
        clause_lines = [first_text]
        for raw in lines[line_no:end_line]:
            if raw.strip():
                clause_lines.append(raw.strip())
        clause_text = re.sub(r"\s+", " ", " ".join(clause_lines)).strip()
        row_type = "operative"
        if len(clause_text) < 80 and re.search(
            r"(раздел|приложение|термины|реквизиты|подписи)",
            clause_text,
            re.I,
        ):
            row_type = "heading"
        rows.append(
            {
                "id": clause_id,
                "contract_id": clause_id,
                "source_locator": clause_id,
                "line_start": line_no,
                "line_end": end_line,
                "section_context": heading,
                "type": row_type,
                "source_text": clause_text,
            }
        )
    return rows


def product_profile(contract_text: str) -> dict[str, Any]:
    lower = contract_text.lower()
    legal_regime = "unknown"
    if "44-фз" in lower or "44 фз" in lower or "44-fz" in lower:
        legal_regime = "44_fz"
    elif "223-фз" in lower or "223 фз" in lower or "223-fz" in lower:
        legal_regime = "223_fz"

    products = []
    for needle, label in (
        ("эквайр", "acquiring"),
        ("qr", "qr"),
        ("sberpay", "sberpay"),
        ("сберpay", "sberpay"),
        ("сберпэй", "sberpay"),
        ("терминал", "terminal"),
    ):
        if needle in lower:
            products.append(label)

    return {
        "product": sorted(set(products)) or ["unknown"],
        "lot": legal_regime if legal_regime != "unknown" else "unknown",
        "terminal": [],
        "payment_method": [],
        "legal_regime": legal_regime,
    }


def build(matrix_path: Path, contract_path: Path, working_dir: Path) -> dict[str, Any]:
    working_dir.mkdir(parents=True, exist_ok=True)
    matrix = matrix_items(matrix_path)
    contract = contract_items(contract_path)
    contract_text = contract_path.read_text(encoding="utf-8-sig")

    clause_index = {
        "matrix_items": matrix,
        "contract_items": contract,
        "source_files": {
            "matrix": str(matrix_path),
            "contract": str(contract_path),
        },
    }
    propositions = {
        "matrix": [proposition_seed(row, source="matrix") for row in matrix],
        "contract": [proposition_seed(row, source="contract") for row in contract],
    }
    profile = product_profile(contract_text)

    (working_dir / "clause_index.json").write_text(
        json.dumps(clause_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (working_dir / "legal_propositions.json").write_text(
        json.dumps(propositions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (working_dir / "contract_product_profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "matrix_items": len(matrix),
        "contract_items": len(contract),
        "contract_product_profile": profile,
        "legal_propositions_seeded_for_review": len(matrix) + len(contract),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=Path("inputs/matrix.json"))
    parser.add_argument("--contract", type=Path, default=Path("inputs/contract.txt"))
    parser.add_argument("--working", type=Path, default=Path("outputs/working"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = build(args.matrix, args.contract, args.working)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
