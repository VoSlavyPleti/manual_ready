"""Validate that extracted contract text has usable clause numbering.

This script is mechanical. It does not make legal conclusions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


BROKEN_RE = re.compile(r"(?m)^\s*0(?:\.0|\.\d+)+\.?\s*(?=\S)")
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bootstrap_source_artifacts import contract_items as parsed_contract_items  # noqa: E402


def validate_contract_text(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    ids = [str(row["id"]).strip() for row in parsed_contract_items(path)]
    broken = [match.group(0).strip().split()[0].rstrip(".") for match in BROKEN_RE.finditer(text)]
    duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
    top_level = sorted({item.split(".")[0] for item in ids if item.split(".")[0].isdigit()})
    deep_ids = [item for item in ids if "." in item]

    warnings = []
    if len(ids) < 20:
        warnings.append("too_few_numbered_clauses")
    if len(deep_ids) < 10:
        warnings.append("too_few_deep_clause_ids")
    if broken:
        warnings.append("broken_zero_numbering")

    valid = not broken and len(ids) >= 20 and len(deep_ids) >= 10
    return {
        "path": str(path),
        "valid": valid,
        "contract_numbering_valid": valid,
        "numbered_clause_count": len(ids),
        "deep_clause_count": len(deep_ids),
        "top_level_sections": top_level,
        "broken_zero_ids": sorted(set(broken)),
        "duplicate_ids": duplicate_ids,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract_txt", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = validate_contract_text(args.contract_txt)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
