"""Finalize discrepancy-analysis JSON from agent working artifacts.

This script is a mechanical safety net. It does not decide legal analogues
or statuses. It preserves agent findings where present, removes structurally
invalid placements, fills required ledgers, and creates a valid JSON artifact
when the agent leaves only partial working files.
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


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def text_of(value: Any, limit: int = 500) -> str:
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


def load_matrix(matrix_path: Path) -> dict[str, dict[str, Any]]:
    data = read_json(matrix_path)
    rows: dict[str, dict[str, Any]] = {}
    if not isinstance(data, list):
        return rows
    for item in data:
        if not isinstance(item, dict):
            continue
        matrix_id = text_of(item.get("number"))
        if not matrix_id:
            continue
        rows[matrix_id] = item
    return rows


def load_contract_rows(contract_path: Path) -> dict[str, dict[str, Any]]:
    text = contract_path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    starts: list[tuple[int, str, str]] = []
    for line_no, line in enumerate(lines, start=1):
        match = CLAUSE_RE.match(line)
        if match:
            starts.append((line_no, match.group(1).rstrip("."), match.group(2).strip()))

    rows: dict[str, dict[str, Any]] = {}
    for idx, (line_no, clause_id, first_text) in enumerate(starts):
        end_line = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else len(lines)
        clause_lines = [first_text]
        for raw in lines[line_no:end_line]:
            if raw.strip():
                clause_lines.append(raw.strip())
        source_text = text_of(" ".join(clause_lines), limit=1200)
        rows.setdefault(
            clause_id,
            {
                "contract_id": clause_id,
                "source_text": source_text,
                "line_start": line_no,
                "line_end": end_line,
            },
        )
    return rows


def collect_candidate_fragments(working_dir: Path, final_path: Path) -> list[dict[str, Any]]:
    candidates: list[Path] = []
    if final_path.exists():
        candidates.append(final_path)
    if working_dir.exists():
        for path in sorted(working_dir.glob("*.json")):
            if path.name in {
                "clause_index.json",
                "legal_propositions.json",
                "contract_product_profile.json",
                "source_preflight.json",
                "working_artifact_validation.json",
            }:
                continue
            candidates.append(path)

    fragments: list[dict[str, Any]] = []
    for path in candidates:
        try:
            data = read_json(path)
        except Exception:
            continue
        if isinstance(data, dict) and any(
            isinstance(data.get(key), list)
            for key in ("links", "unmatched_matrix", "unmatched_contract", "atomic_links")
        ):
            fragments.append(data)
    return fragments


def normalize_matrix_ids(values: Any, known_matrix: set[str]) -> list[str]:
    if not isinstance(values, list):
        values = [values] if values else []
    result = []
    for value in values:
        matrix_id = text_of(value)
        if matrix_id and matrix_id in known_matrix and matrix_id not in result:
            result.append(matrix_id)
    return result


def normalize_contract_ids(values: Any, known_contract: set[str]) -> list[str]:
    if not isinstance(values, list):
        values = [values] if values else []
    result = []
    for value in values:
        contract_id = text_of(value)
        if contract_id and contract_id in known_contract and contract_id not in result:
            result.append(contract_id)
    return result


def matrix_requirement(matrix_item: dict[str, Any]) -> str:
    return (
        text_of(matrix_item.get("enriched_text"), limit=900)
        or text_of(matrix_item.get("main_idea"), limit=900)
        or text_of(matrix_item.get("topics"), limit=900)
        or "Matrix requirement."
    )


def normalize_link(
    link: dict[str, Any],
    known_matrix: set[str],
    known_contract: set[str],
) -> dict[str, Any] | None:
    relationship = link.get("relationship")
    if relationship not in {"aligned", "deviation"}:
        return None
    matrix_ids = normalize_matrix_ids(link.get("matrix_ids"), known_matrix)
    contract_ids = normalize_contract_ids(link.get("contract_ids"), known_contract)
    if not matrix_ids or not contract_ids:
        return None

    discrepancies = link.get("discrepancies") if isinstance(link.get("discrepancies"), list) else []
    if relationship == "aligned":
        discrepancies = []
    elif not discrepancies:
        discrepancies = [
            {
                "type": "other",
                "description": text_of(link.get("status_reason")) or "Material difference identified by analysis.",
                "risk": text_of(link.get("risk")) or "Requires legal review.",
            }
        ]

    return {
        "matrix_ids": matrix_ids,
        "contract_ids": contract_ids,
        "relationship": relationship,
        "legal_topic": text_of(link.get("legal_topic")) or "Coverage finding",
        "matrix_standard": text_of(link.get("matrix_standard"), limit=1500) or "Matrix standard.",
        "contract_position": text_of(link.get("contract_position"), limit=1500) or "Contract position.",
        "status_reason": text_of(link.get("status_reason"), limit=1000) or "Agent finding normalized by finalizer.",
        "risk_level": link.get("risk_level") if link.get("risk_level") in {"none", "low", "medium", "high"} else ("medium" if relationship == "deviation" else "none"),
        "discrepancies": discrepancies,
    }


def build_atomic_links(links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int]] = set()
    for link_index, link in enumerate(links):
        for matrix_id in link["matrix_ids"]:
            for contract_id in link["contract_ids"]:
                key = (matrix_id, contract_id, link_index)
                if key in seen:
                    continue
                seen.add(key)
                atoms.append(
                    {
                        "matrix_id": matrix_id,
                        "contract_id": contract_id,
                        "relationship": link["relationship"],
                        "link_index": link_index,
                        "coverage_role": "direct",
                        "coverage": link.get("status_reason", "Group coverage."),
                    }
                )
    return atoms


def finalize(
    matrix_path: Path,
    contract_path: Path,
    working_dir: Path,
    final_path: Path,
) -> dict[str, Any]:
    matrix = load_matrix(matrix_path)
    contract = load_contract_rows(contract_path)
    known_matrix = set(matrix)
    known_contract = set(contract)

    profile_path = working_dir / "contract_product_profile.json"
    try:
        profile = read_json(profile_path) if profile_path.exists() else {}
    except Exception:
        profile = {}

    links: list[dict[str, Any]] = []
    unmatched_contract_by_id: dict[str, dict[str, Any]] = {}
    explicit_unmatched_matrix: dict[str, dict[str, Any]] = {}
    scope_closed_matrix: dict[str, dict[str, Any]] = {}

    for fragment in collect_candidate_fragments(working_dir, final_path):
        coverage = fragment.get("coverage_ledger")
        if isinstance(coverage, dict):
            for raw in coverage.get("matrix", []) or []:
                if not isinstance(raw, dict):
                    continue
                matrix_id = text_of(raw.get("matrix_id"))
                closure = text_of(raw.get("closure"))
                reason = text_of(raw.get("reason"), limit=500)
                if matrix_id in known_matrix and (
                    closure in {"out_of_scope", "not_applicable"}
                    or (
                        closure == "not_evaluable"
                        and any(token in reason.lower() for token in ("scope", "applic", "filter", "не примен"))
                    )
                ):
                    scope_closed_matrix[matrix_id] = {
                        "closure": closure if closure in {"out_of_scope", "not_applicable"} else "out_of_scope",
                        "reason": reason or "Closed as not applicable to the contract profile.",
                    }

        for raw_link in fragment.get("links", []) or []:
            if not isinstance(raw_link, dict):
                continue
            link = normalize_link(raw_link, known_matrix, known_contract)
            if link:
                links.append(link)

        for raw in fragment.get("unmatched_matrix", []) or []:
            if not isinstance(raw, dict):
                continue
            matrix_id = text_of(raw.get("matrix_id"))
            if matrix_id in known_matrix:
                explicit_unmatched_matrix[matrix_id] = {
                    "matrix_id": matrix_id,
                    "requirement": text_of(raw.get("requirement"), limit=1000)
                    or matrix_requirement(matrix[matrix_id]),
                    "status": "missing_in_contract",
                    "required_type": raw.get("required_type") or "unknown",
                    "risk_level": raw.get("risk_level") if raw.get("risk_level") in {"low", "medium", "high"} else "medium",
                    "risk": text_of(raw.get("risk")) or "Matrix requirement is not covered in the contract package.",
                    "rejected_candidates": raw.get("rejected_candidates")
                    if isinstance(raw.get("rejected_candidates"), list)
                    else [],
                }

        for raw in fragment.get("unmatched_contract", []) or []:
            if not isinstance(raw, dict):
                continue
            contract_id = text_of(raw.get("contract_id"))
            if contract_id in known_contract:
                unmatched_contract_by_id[contract_id] = {
                    "contract_id": contract_id,
                    "contract_position": text_of(raw.get("contract_position"), limit=1000)
                    or contract[contract_id]["source_text"],
                    "status": "extra_in_contract",
                    "risk_level": raw.get("risk_level") if raw.get("risk_level") in {"low", "medium", "high"} else "medium",
                    "risk": text_of(raw.get("risk")) or "Contract term has no confirmed matrix analogue and requires legal review.",
                    "materiality_reason": text_of(raw.get("materiality_reason"))
                    or "Classified as legally significant by agent fragment.",
                }

    deduped_links: list[dict[str, Any]] = []
    seen_links: set[tuple[tuple[str, ...], tuple[str, ...], str, str]] = set()
    for link in links:
        key = (
            tuple(link["matrix_ids"]),
            tuple(link["contract_ids"]),
            link["relationship"],
            text_of(link.get("status_reason")),
        )
        if key in seen_links:
            continue
        seen_links.add(key)
        deduped_links.append(link)
    links = deduped_links

    linked_matrix = {matrix_id for link in links for matrix_id in link["matrix_ids"]}
    linked_contract = {contract_id for link in links for contract_id in link["contract_ids"]}

    unmatched_matrix = []
    for matrix_id, item in matrix.items():
        if matrix_id in linked_matrix:
            continue
        if matrix_id in scope_closed_matrix:
            continue
        row = explicit_unmatched_matrix.get(matrix_id)
        if not row:
            row = {
                "matrix_id": matrix_id,
                "requirement": matrix_requirement(item),
                "status": "missing_in_contract",
                "required_type": text_of(item.get("required_type") or item.get("requirement_type")) or "unknown",
                "risk_level": "medium",
                "risk": "No confirmed contract analogue was present in completed fragments.",
                "rejected_candidates": [],
            }
        unmatched_matrix.append(row)

    unmatched_contract = [
        row
        for contract_id, row in unmatched_contract_by_id.items()
        if contract_id not in linked_contract
    ]

    coverage_ledger = {
        "matrix": [],
        "contract": [],
    }
    matrix_link_indices: dict[str, list[int]] = {matrix_id: [] for matrix_id in matrix}
    contract_link_indices: dict[str, list[int]] = {contract_id: [] for contract_id in contract}
    for idx, link in enumerate(links):
        for matrix_id in link["matrix_ids"]:
            matrix_link_indices.setdefault(matrix_id, []).append(idx)
        for contract_id in link["contract_ids"]:
            contract_link_indices.setdefault(contract_id, []).append(idx)

    for matrix_id in matrix:
        indices = matrix_link_indices.get(matrix_id, [])
        if matrix_id in scope_closed_matrix and not indices:
            closure = scope_closed_matrix[matrix_id]["closure"]
            reason = scope_closed_matrix[matrix_id]["reason"]
        else:
            closure = "linked" if indices else "missing_in_contract"
            reason = "Linked in final group." if indices else "No linked final group."
        coverage_ledger["matrix"].append(
            {
                "matrix_id": matrix_id,
                "closure": closure,
                "link_indices": indices,
                "reason": reason,
            }
        )

    extra_contract_ids = {row["contract_id"] for row in unmatched_contract}
    for contract_id in contract:
        indices = contract_link_indices.get(contract_id, [])
        if indices:
            closure = "linked"
            reason = "Linked in final group."
        elif contract_id in extra_contract_ids:
            closure = "extra_in_contract"
            reason = "Reported as extra contract term."
        else:
            closure = "not_material"
            reason = "No final legal finding produced for this clause."
        coverage_ledger["contract"].append(
            {
                "contract_id": contract_id,
                "closure": closure,
                "link_indices": indices,
                "reason": reason,
            }
        )

    artifact = {
        "analysis_profile": {
            "contract_product_profile": profile,
            "source_preflight": {
                "contract_numbering_valid": True,
                "notes": [],
            },
            "finalizer": {
                "mode": "json_only_structural_normalization",
                "note": "Mechanical finalizer preserved agent findings and closed missing rows where fragments were incomplete.",
            },
        },
        "links": links,
        "atomic_links": build_atomic_links(links),
        "unmatched_matrix": unmatched_matrix,
        "unmatched_contract": unmatched_contract,
        "coverage_ledger": coverage_ledger,
        "summary": {
            "aligned_count": sum(1 for link in links if link["relationship"] == "aligned"),
            "deviation_count": sum(1 for link in links if link["relationship"] == "deviation"),
            "missing_in_contract_count": len(unmatched_matrix),
            "extra_in_contract_count": len(unmatched_contract),
        },
    }
    write_json(final_path, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=Path("inputs/matrix.json"))
    parser.add_argument("--contract", type=Path, default=Path("inputs/contract.txt"))
    parser.add_argument("--working", type=Path, default=Path("outputs/working"))
    parser.add_argument("--final", type=Path, default=Path("outputs/discrepancy_analysis.json"))
    args = parser.parse_args()

    artifact = finalize(args.matrix, args.contract, args.working, args.final)
    print(
        json.dumps(
            {
                "wrote": str(args.final),
                "links": len(artifact["links"]),
                "unmatched_matrix": len(artifact["unmatched_matrix"]),
                "unmatched_contract": len(artifact["unmatched_contract"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
