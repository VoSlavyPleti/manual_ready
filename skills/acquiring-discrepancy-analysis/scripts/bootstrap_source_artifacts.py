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


MULTI_NUMERIC_RE = re.compile(r"^\s*(\d+(?:\.\d+)+)\.?\s*(.+?)\s*$")
TOP_NUMERIC_RE = re.compile(r"^\s*(\d{1,2})[.)]\s*(.+?)\s*$")
BARE_TOP_NUMERIC_RE = re.compile(r"^\s*(\d{1,2})\s+(.{8,}?)\s*$")
APPENDIX_RE = re.compile(r"^\s*Приложение\s*№\s*([\d.]+)", re.IGNORECASE)
INLINE_MULTI_NUMERIC_RE = re.compile(
    r"(?<![\d.])(\d+(?:\.\d+)+)\.(?=[A-Za-zА-Яа-яЁё])"
)
INLINE_TOP_NUMERIC_RE = re.compile(r"(?<![\d.])(\d{1,2})\.(?=[A-Za-zА-Яа-яЁё])")
TABLE_MARKER_RE = re.compile(
    r"(№\s*п/п|наименование\s+услуг|ед\.\s*изм|количество|цена\s+за\s+единицу|"
    r"максимальное\s+значение|размер\s+комиссии|адрес\s+объекта|платежн\w+\s+систем)",
    re.IGNORECASE,
)
REQUISITES_RE = re.compile(
    r"(банковские\s+реквизиты|места\s+нахождения|инн|кпп|"
    r"огрн|р/с|бик|банк\s+получатель|тел/факс|e-mail)",
    re.IGNORECASE,
)
AMOUNT_RE = re.compile(r"^[\d\s\u00a0]+(?:[,.]\d{2})?(?:\s*(?:руб\.?|%))?$", re.IGNORECASE)


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


def looks_like_amount_or_code(text: str) -> bool:
    clean = text.strip()
    if not clean:
        return True
    if AMOUNT_RE.fullmatch(clean):
        return True
    digits = re.sub(r"\D", "", clean)
    return bool(digits and len(digits) >= 5 and len(digits) >= len(clean.replace(" ", "")) - 2)


def nearby_text(lines: list[str], index: int, radius: int = 4) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return " ".join(line.strip() for line in lines[start:end] if line.strip())


def in_table_context(lines: list[str], index: int) -> bool:
    return bool(TABLE_MARKER_RE.search(nearby_text(lines, index, radius=5)))


def in_requisites_context(current_heading: str, lines: list[str], index: int) -> bool:
    if REQUISITES_RE.search(current_heading):
        return True
    current = lines[index].strip()
    return bool(
        re.match(
            r"^\s*(инн|кпп|огрн|р/с|бик|банк\s+получатель|тел/факс|e-mail|"
            r"заказчик:|исполнитель:)",
            current,
            flags=re.IGNORECASE,
        )
    )


def expand_inline_clause_markers(lines: list[str]) -> list[str]:
    """Split visible clause locators that were extracted onto one text line.

    This is source-map hygiene only. It does not decide legal meaning.
    """

    expanded: list[str] = []
    for line in lines:
        marked = INLINE_MULTI_NUMERIC_RE.sub(r"\n\1. ", line)
        marked = INLINE_TOP_NUMERIC_RE.sub(r"\n\1. ", marked)
        expanded.extend(part for part in marked.splitlines())
    return expanded


def parse_clause_candidate(
    lines: list[str],
    index: int,
    *,
    current_heading: str,
    current_appendix: str,
    current_parent: str,
) -> tuple[str, str] | None:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return None

    for pattern in (MULTI_NUMERIC_RE, TOP_NUMERIC_RE):
        match = pattern.match(line)
        if match:
            clause_id = match.group(1).rstrip(".")
            first_text = match.group(2).strip()
            if looks_like_amount_or_code(first_text):
                return None
            if in_requisites_context(current_heading, lines, index) and not current_appendix:
                return None
            if current_appendix and re.fullmatch(r"\d+(?:\.\d+)*", clause_id):
                clause_id = f"{current_appendix} п.{clause_id}"
            return clause_id, first_text

    bare = BARE_TOP_NUMERIC_RE.match(line)
    if bare:
        clause_id = bare.group(1)
        first_text = bare.group(2).strip()
        if not current_appendix:
            return None
        if (
            looks_like_amount_or_code(first_text)
            or in_table_context(lines, index)
            or in_requisites_context(current_heading, lines, index)
        ):
            return None
        if current_appendix:
            clause_id = f"{current_appendix} п.{clause_id}"
        return clause_id, first_text

    return None


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
        seed["final_allowed"] = row_type not in {"heading", "technical"}
        seed["evidence_only"] = row_type in {"heading", "technical"}
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


def matrix_legal_propositions(
    matrix_path: Path,
    matrix_legal_path: Path | None,
) -> list[dict[str, Any]]:
    if matrix_legal_path and matrix_legal_path.exists():
        data = read_json(matrix_legal_path)
        rows = data.get("matrix") if isinstance(data, dict) else data
        if isinstance(rows, list):
            result = [row for row in rows if isinstance(row, dict)]
            if result:
                return result
    return [proposition_seed(row, source="matrix") for row in matrix_items(matrix_path)]


def contract_items(contract_path: Path) -> list[dict[str, Any]]:
    text = contract_path.read_text(encoding="utf-8-sig")
    lines = expand_inline_clause_markers(text.splitlines())
    starts: list[tuple[int, str, str, str]] = []
    current_heading = ""
    current_appendix = ""
    current_parent = ""

    for line_index, line in enumerate(lines):
        line_no = line_index + 1
        appendix_match = APPENDIX_RE.match(line.strip())
        if appendix_match:
            current_appendix = f"Приложение №{appendix_match.group(1).rstrip('.')}"
            current_heading = current_appendix
            current_parent = ""
            continue

        candidate = parse_clause_candidate(
            lines,
            line_index,
            current_heading=current_heading,
            current_appendix=current_appendix,
            current_parent=current_parent,
        )
        if candidate:
            clause_id, first_text = candidate
            starts.append(
                (line_no, clause_id, first_text, current_heading)
            )
            current_parent = clause_id
        elif line.strip() and not re.match(r"^\s*\d+(?:\.\d+)*[.)]?\s+", line):
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
        if re.match(r"^[а-яёa-z][^.;]{1,100}\s+[–-]\s+", clause_text, re.I):
            row_type = "definition"
        elif re.match(r"^\s*(места\s+нахождения|банковские\s+реквизиты|подписи)", clause_text, re.I):
            row_type = "technical"
        elif len(clause_text) < 180 and re.search(
            r"(раздел|приложение|термины|реквизиты|подписи|"
            r"обязательства\s+сторон|права\s+и\s+обязанности|"
            r"срок\s+действия|ответственность|форс-мажор|"
            r"заключительные\s+положения|предмет\s+контракта)",
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


def build(
    matrix_path: Path,
    contract_path: Path,
    working_dir: Path,
    matrix_legal_path: Path | None = None,
) -> dict[str, Any]:
    working_dir.mkdir(parents=True, exist_ok=True)
    matrix = matrix_items(matrix_path)
    contract = contract_items(contract_path)
    contract_text = contract_path.read_text(encoding="utf-8-sig")
    matrix_props = matrix_legal_propositions(matrix_path, matrix_legal_path)
    contract_props = [proposition_seed(row, source="contract") for row in contract]

    clause_index = {
        "matrix_items": matrix,
        "contract_items": contract,
        "source_files": {
            "matrix": str(matrix_path),
            "contract": str(contract_path),
        },
    }
    contract_legal_propositions = {
        "schema_version": "1.0",
        "source_file": str(contract_path),
        "generation": "seed for agent-led extraction and enrichment",
        "contract": contract_props,
    }
    propositions = {
        "matrix": matrix_props,
        "contract": contract_props,
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
    (working_dir / "contract_legal_propositions.json").write_text(
        json.dumps(contract_legal_propositions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (working_dir / "contract_product_profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "matrix_items": len(matrix),
        "matrix_legal_propositions": len(matrix_props),
        "contract_items": len(contract),
        "contract_product_profile": profile,
        "contract_legal_propositions_seeded_for_review": len(contract_props),
        "legal_propositions_seeded_for_review": len(matrix_props) + len(contract_props),
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

    result = build(args.matrix, args.contract, args.working, args.matrix_legal)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
