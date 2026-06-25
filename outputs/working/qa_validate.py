#!/usr/bin/env python3
"""QA validation of discrepancy_analysis.json against skill rules."""
import json, sys, re
from collections import Counter, defaultdict

import os as _os
_json_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "discrepancy_analysis.json")
_json_path = _os.path.normpath(_json_path)
with open(_json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

import os
matrix_path = os.path.join(os.environ.get("SKILLSHOT_ROOT", ""), "inputs", "matrix.json")
if not os.path.exists(matrix_path):
    # Try relative paths
    for p in ["/inputs/matrix.json", "inputs/matrix.json", "../inputs/matrix.json"]:
        if os.path.exists(p):
            matrix_path = p
            break
with open(matrix_path, "r", encoding="utf-8") as f:
    matrix = json.load(f)

errors = []
warnings = []

# --- 1. Check all matrix ids from source are in coverage_ledger ---
source_matrix_ids = set()
if isinstance(matrix, list):
    for item in matrix:
        mid = item.get("number", "")
        if mid:
            source_matrix_ids.add(mid)
elif isinstance(matrix, dict):
    for item in matrix.values():
        mid = item.get("number", "")
        if mid:
            source_matrix_ids.add(mid)

ledger_matrix_ids = set()
for row in data.get("coverage_ledger", {}).get("matrix", []):
    ledger_matrix_ids.add(row["matrix_id"])

missing_from_ledger = source_matrix_ids - ledger_matrix_ids
if missing_from_ledger:
    errors.append(f"Matrix ids missing from coverage_ledger: {sorted(missing_from_ledger)}")

extra_in_ledger = ledger_matrix_ids - source_matrix_ids
if extra_in_ledger:
    errors.append(f"Matrix ids in coverage_ledger not in source: {sorted(extra_in_ledger)}")

# --- 2. Check out_of_scope / not_applicable are NOT in unmatched_matrix ---
unmatched_matrix_ids = set(row["matrix_id"] for row in data.get("unmatched_matrix", []))
for row in data.get("coverage_ledger", {}).get("matrix", []):
    if row["closure"] in ("out_of_scope", "not_applicable"):
        if row["matrix_id"] in unmatched_matrix_ids:
            errors.append(f"Matrix {row['matrix_id']} is {row['closure']} in coverage_ledger but appears in unmatched_matrix")

# --- 3. Check every unmatched_matrix item has closure=missing_in_contract in ledger ---
for row in data.get("unmatched_matrix", []):
    mid = row["matrix_id"]
    ledger_row = next((r for r in data.get("coverage_ledger", {}).get("matrix", []) if r["matrix_id"] == mid), None)
    if not ledger_row:
        errors.append(f"unmatched_matrix {mid} not found in coverage_ledger.matrix")
    elif ledger_row["closure"] != "missing_in_contract":
        errors.append(f"unmatched_matrix {mid} has ledger closure={ledger_row['closure']}, expected missing_in_contract")

# --- 4. Check every linked matrix id has a link ---
linked_matrix_ids = set()
for i, link in enumerate(data.get("links", [])):
    for mid in link["matrix_ids"]:
        linked_matrix_ids.add(mid)

for row in data.get("coverage_ledger", {}).get("matrix", []):
    if row["closure"] == "linked":
        if row["matrix_id"] not in linked_matrix_ids:
            errors.append(f"Matrix {row['matrix_id']} closure=linked but not in any link group")
        if not row["link_indices"]:
            errors.append(f"Matrix {row['matrix_id']} closure=linked but link_indices empty")

# --- 5. Check missing_in_contract in ledger matches unmatched_matrix ---
for row in data.get("coverage_ledger", {}).get("matrix", []):
    if row["closure"] == "missing_in_contract":
        if row["matrix_id"] not in unmatched_matrix_ids:
            errors.append(f"Matrix {row['matrix_id']} closure=missing_in_contract but not in unmatched_matrix")

# --- 6. Check links have non-empty contract_ids ---
for i, link in enumerate(data.get("links", [])):
    if not link["contract_ids"]:
        errors.append(f"Link group {i} (matrix_ids={link['matrix_ids']}) has empty contract_ids")
    if not link["matrix_ids"]:
        errors.append(f"Link group {i} has empty matrix_ids")

# --- 7. Check aligned has no discrepancies and risk_level=none ---
for i, link in enumerate(data.get("links", [])):
    if link["relationship"] == "aligned":
        if link.get("discrepancies") and len(link["discrepancies"]) > 0:
            errors.append(f"Link group {i} (matrix_ids={link['matrix_ids']}) is aligned but has {len(link['discrepancies'])} discrepancies")
        if link.get("risk_level") != "none":
            errors.append(f"Link group {i} (matrix_ids={link['matrix_ids']}) is aligned but risk_level={link['risk_level']}")

# --- 8. Check deviation has at least one discrepancy and risk_level ---
for i, link in enumerate(data.get("links", [])):
    if link["relationship"] == "deviation":
        if not link.get("discrepancies") or len(link["discrepancies"]) == 0:
            errors.append(f"Link group {i} (matrix_ids={link['matrix_ids']}) is deviation but has no discrepancies")
        if link.get("risk_level") == "none":
            errors.append(f"Link group {i} (matrix_ids={link['matrix_ids']}) is deviation but risk_level=none")
        for d in link.get("discrepancies", []):
            if not d.get("risk"):
                errors.append(f"Link group {i} discrepancy '{d.get('description','')}' has empty risk")

# --- 9. Check unmatched_contract items have risk ---
for row in data.get("unmatched_contract", []):
    if not row.get("risk"):
        errors.append(f"unmatched_contract {row['contract_id']} has empty risk")

# --- 10. Check atomic_links structure ---
atomic_link_indices = set()
for al in data.get("atomic_links", []):
    if "matrix_id" not in al:
        errors.append(f"atomic_link missing matrix_id")
    if "contract_id" not in al:
        errors.append(f"atomic_link missing contract_id")
    if "relationship" not in al:
        errors.append(f"atomic_link missing relationship")
    if "link_index" not in al:
        errors.append(f"atomic_link missing link_index")
    if "coverage_role" not in al:
        errors.append(f"atomic_link missing coverage_role")
    if "coverage" not in al:
        errors.append(f"atomic_link missing coverage")
    atomic_link_indices.add(al.get("link_index"))

# --- 11. Check atomic_links inherit group relationship ---
group_relationships = {}
for i, link in enumerate(data.get("links", [])):
    group_relationships[i] = link["relationship"]

for al in data.get("atomic_links", []):
    li = al.get("link_index")
    if li is not None and li in group_relationships:
        if al["relationship"] != group_relationships[li]:
            errors.append(f"atomic_link matrix={al['matrix_id']} contract={al['contract_id']} link_index={li} has relationship={al['relationship']} but group has {group_relationships[li]}")

# --- 12. Check summary counts ---
summary = data.get("summary", {})
aligned_count = sum(1 for l in data.get("links", []) if l["relationship"] == "aligned")
deviation_count = sum(1 for l in data.get("links", []) if l["relationship"] == "deviation")
missing_count = len(data.get("unmatched_matrix", []))
extra_count = len(data.get("unmatched_contract", []))

if summary.get("aligned_count") != aligned_count:
    errors.append(f"summary.aligned_count={summary.get('aligned_count')} but actual={aligned_count}")
if summary.get("deviation_count") != deviation_count:
    errors.append(f"summary.deviation_count={summary.get('deviation_count')} but actual={deviation_count}")
if summary.get("missing_in_contract_count") != missing_count:
    errors.append(f"summary.missing_in_contract_count={summary.get('missing_in_contract_count')} but actual={missing_count}")
if summary.get("extra_in_contract_count") != extra_count:
    errors.append(f"summary.extra_in_contract_count={summary.get('extra_in_contract_count')} but actual={extra_count}")

# --- 13. Check contract_ids in links are valid (exist in coverage_ledger.contract) ---
contract_ledger_ids = set(row["contract_id"] for row in data.get("coverage_ledger", {}).get("contract", []))
for i, link in enumerate(data.get("links", [])):
    for cid in link["contract_ids"]:
        if cid not in contract_ledger_ids:
            errors.append(f"Link group {i} contract_id={cid} not in coverage_ledger.contract")

# --- 14. Check for invented/parenthetical ids ---
# Contract ids should look like clause numbers (digits and dots) or be from source
for row in data.get("unmatched_contract", []):
    cid = row["contract_id"]
    if cid not in contract_ledger_ids:
        errors.append(f"unmatched_contract {cid} not in coverage_ledger.contract")

# --- 15. Check unmatched_matrix items have required fields ---
for row in data.get("unmatched_matrix", []):
    if not row.get("risk"):
        errors.append(f"unmatched_matrix {row['matrix_id']} has empty risk")
    if not row.get("risk_level"):
        errors.append(f"unmatched_matrix {row['matrix_id']} has empty risk_level")
    if row.get("status") != "missing_in_contract":
        errors.append(f"unmatched_matrix {row['matrix_id']} status={row.get('status')}, expected missing_in_contract")

# --- 16. Check unmatched_contract items have required fields ---
for row in data.get("unmatched_contract", []):
    if row.get("status") != "extra_in_contract":
        errors.append(f"unmatched_contract {row['contract_id']} status={row.get('status')}, expected extra_in_contract")
    if not row.get("materiality_reason"):
        errors.append(f"unmatched_contract {row['contract_id']} has empty materiality_reason")

# --- 17. Check coverage_ledger contract closures ---
for row in data.get("coverage_ledger", {}).get("contract", []):
    if row["closure"] not in ("linked", "extra_in_contract", "not_material"):
        errors.append(f"coverage_ledger.contract {row['contract_id']} has invalid closure={row['closure']}")

# --- 18. Check coverage_ledger matrix closures ---
for row in data.get("coverage_ledger", {}).get("matrix", []):
    if row["closure"] not in ("linked", "missing_in_contract", "out_of_scope", "not_applicable", "not_evaluable"):
        errors.append(f"coverage_ledger.matrix {row['matrix_id']} has invalid closure={row['closure']}")

# --- 19. Check for duplicate link_indices ---
link_indices_seen = set()
for i, link in enumerate(data.get("links", [])):
    link_indices_seen.add(i)

for al in data.get("atomic_links", []):
    li = al.get("link_index")
    if li is not None and li not in link_indices_seen:
        errors.append(f"atomic_link references link_index={li} which does not exist in links")

# --- 20. Check that every link has at least one atomic_link ---
for i in range(len(data.get("links", []))):
    has_atomic = any(al.get("link_index") == i for al in data.get("atomic_links", []))
    if not has_atomic:
        errors.append(f"Link group {i} has no atomic_links")

# --- 21. Check unmatched_matrix for out_of_scope items ---
out_of_scope_ids = set()
for row in data.get("coverage_ledger", {}).get("matrix", []):
    if row["closure"] in ("out_of_scope", "not_applicable"):
        out_of_scope_ids.add(row["matrix_id"])

for row in data.get("unmatched_matrix", []):
    if row["matrix_id"] in out_of_scope_ids:
        errors.append(f"unmatched_matrix contains out_of_scope/not_applicable item {row['matrix_id']}")

# --- 22. Check contract_ids in links are not empty strings ---
for i, link in enumerate(data.get("links", [])):
    for cid in link["contract_ids"]:
        if not cid or not cid.strip():
            errors.append(f"Link group {i} has empty contract_id")

# --- 23. Check for suspicious contract ids (parenthetical, invented) ---
# Look for ids that don't match typical clause numbering
suspicious_patterns = []
for row in data.get("coverage_ledger", {}).get("contract", []):
    cid = row["contract_id"]
    # Check for ids like "354340" which look like random numbers
    if re.match(r'^\d{5,}$', cid):
        warnings.append(f"Suspicious contract_id (looks like random number): {cid}")
    # Check for ids with parentheses
    if '(' in cid or ')' in cid:
        warnings.append(f"Contract_id with parentheses: {cid}")

# --- 24. Check that all matrix_ids in links exist in source ---
for i, link in enumerate(data.get("links", [])):
    for mid in link["matrix_ids"]:
        if mid not in source_matrix_ids:
            errors.append(f"Link group {i} matrix_id={mid} not in source matrix")

# --- 25. Check that unmatched_matrix ids exist in source ---
for row in data.get("unmatched_matrix", []):
    if row["matrix_id"] not in source_matrix_ids:
        errors.append(f"unmatched_matrix {row['matrix_id']} not in source matrix")

# --- 26. Check for required_type consistency ---
for row in data.get("unmatched_matrix", []):
    rt = row.get("required_type")
    if rt not in ("mandatory", "optional", "unknown"):
        errors.append(f"unmatched_matrix {row['matrix_id']} has invalid required_type={rt}")

# --- 27. Check risk_level values ---
valid_risk_levels = {"none", "low", "medium", "high"}
for i, link in enumerate(data.get("links", [])):
    if link.get("risk_level") not in valid_risk_levels:
        errors.append(f"Link group {i} has invalid risk_level={link.get('risk_level')}")
for row in data.get("unmatched_matrix", []):
    if row.get("risk_level") not in valid_risk_levels:
        errors.append(f"unmatched_matrix {row['matrix_id']} has invalid risk_level={row.get('risk_level')}")
for row in data.get("unmatched_contract", []):
    if row.get("risk_level") not in valid_risk_levels:
        errors.append(f"unmatched_contract {row['contract_id']} has invalid risk_level={row.get('risk_level')}")

# --- 28. Check relationship values ---
valid_relationships = {"aligned", "deviation"}
for i, link in enumerate(data.get("links", [])):
    if link.get("relationship") not in valid_relationships:
        errors.append(f"Link group {i} has invalid relationship={link.get('relationship')}")

# --- 29. Check coverage_role values ---
valid_roles = {"direct", "parent", "child", "framework", "procedure", "liability", "payment", "appendix", "context"}
for al in data.get("atomic_links", []):
    if al.get("coverage_role") not in valid_roles:
        errors.append(f"atomic_link matrix={al['matrix_id']} contract={al['contract_id']} has invalid coverage_role={al.get('coverage_role')}")

# --- 30. Check that mandatory missing items are not low risk ---
for row in data.get("unmatched_matrix", []):
    if row.get("required_type") == "mandatory" and row.get("risk_level") == "low":
        warnings.append(f"unmatched_matrix {row['matrix_id']} is mandatory missing but risk_level=low (should normally be medium or high)")

# --- Output ---
result = {
    "valid": len(errors) == 0,
    "error_count": len(errors),
    "warning_count": len(warnings),
    "errors": errors,
    "warnings": warnings,
    "counts": {
        "source_matrix_ids": len(source_matrix_ids),
        "ledger_matrix_ids": len(ledger_matrix_ids),
        "links_count": len(data.get("links", [])),
        "atomic_links_count": len(data.get("atomic_links", [])),
        "unmatched_matrix_count": len(data.get("unmatched_matrix", [])),
        "unmatched_contract_count": len(data.get("unmatched_contract", [])),
        "aligned_actual": aligned_count,
        "deviation_actual": deviation_count,
        "missing_actual": missing_count,
        "extra_actual": extra_count,
        "summary_aligned": summary.get("aligned_count"),
        "summary_deviation": summary.get("deviation_count"),
        "summary_missing": summary.get("missing_in_contract_count"),
        "summary_extra": summary.get("extra_in_contract_count"),
    }
}

print(json.dumps(result, ensure_ascii=False, indent=2))
