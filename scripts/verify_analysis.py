import json

with open('outputs/discrepancy_analysis.json', 'r') as f:
    analysis = json.load(f)

# Verify consistency
errors = []

# 1. Every matrix coverage "linked" must have that matrix_id in at least one links[].matrix_ids
all_linked_matrix_ids = set()
for link in analysis["links"]:
    for mid in link["matrix_ids"]:
        all_linked_matrix_ids.add(mid)

for cov in analysis["coverage_ledger"]["matrix"]:
    if cov["closure"] == "linked":
        if cov["matrix_id"] not in all_linked_matrix_ids:
            errors.append(f"Matrix {cov['matrix_id']}: coverage=linked but not in any links[].matrix_ids")

# 2. Every contract coverage "linked" must have that contract_id in at least one links[].contract_ids
all_linked_contract_ids = set()
for link in analysis["links"]:
    for cid in link["contract_ids"]:
        all_linked_contract_ids.add(cid)

for cov in analysis["coverage_ledger"]["contract"]:
    if cov["closure"] == "linked":
        if cov["contract_id"] not in all_linked_contract_ids:
            errors.append(f"Contract {cov['contract_id']}: coverage=linked but not in any links[].contract_ids")

# 3. Every contract coverage "extra_in_contract" must have that contract_id in unmatched_contract
extra_ids = set(uc["contract_id"] for uc in analysis["unmatched_contract"])
for cov in analysis["coverage_ledger"]["contract"]:
    if cov["closure"] == "extra_in_contract":
        if cov["contract_id"] not in extra_ids:
            errors.append(f"Contract {cov['contract_id']}: coverage=extra_in_contract but not in unmatched_contract")

# 4. Every unmatched_contract id must be in coverage_ledger with "extra_in_contract"
for uc in analysis["unmatched_contract"]:
    found = False
    for cov in analysis["coverage_ledger"]["contract"]:
        if cov["contract_id"] == uc["contract_id"] and cov["closure"] == "extra_in_contract":
            found = True
            break
    if not found:
        errors.append(f"Contract {uc['contract_id']}: in unmatched_contract but coverage not extra_in_contract")

# 5. Summary counts
aligned = sum(1 for l in analysis["links"] if l["relationship"] == "aligned")
deviations = sum(1 for l in analysis["links"] if l["relationship"] == "deviation")
missing = len(analysis["unmatched_matrix"])
extra = len(analysis["unmatched_contract"])

if analysis["summary"]["aligned_count"] != aligned:
    errors.append(f"Summary aligned_count {analysis['summary']['aligned_count']} != actual {aligned}")
if analysis["summary"]["deviation_count"] != deviations:
    errors.append(f"Summary deviation_count {analysis['summary']['deviation_count']} != actual {deviations}")
if analysis["summary"]["missing_in_contract_count"] != missing:
    errors.append(f"Summary missing_in_contract_count {analysis['summary']['missing_in_contract_count']} != actual {missing}")
if analysis["summary"]["extra_in_contract_count"] != extra:
    errors.append(f"Summary extra_in_contract_count {analysis['summary']['extra_in_contract_count']} != actual {extra}")

# 6. All matrix ids covered
matrix_ids_from_file = {m["matrix_id"] for m in analysis["coverage_ledger"]["matrix"]}
with open('inputs/matrix.json', 'r') as f:
    matrix = json.load(f)
all_matrix_ids = {m["number"] for m in matrix}
missing_from_coverage = all_matrix_ids - matrix_ids_from_file
extra_in_coverage = matrix_ids_from_file - all_matrix_ids

if missing_from_coverage:
    errors.append(f"Matrix IDs not covered: {missing_from_coverage}")
if extra_in_coverage:
    errors.append(f"Matrix IDs in coverage not in source: {extra_in_coverage}")

# 7. No aligned link should have discrepancies
for link in analysis["links"]:
    if link["relationship"] == "aligned" and len(link["discrepancies"]) > 0:
        errors.append(f"Aligned link with matrix_ids {link['matrix_ids']} has non-empty discrepancies")

if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL CHECKS PASSED!")

print(f"\nMatrix coverage summary:")
closures = {}
for cov in analysis["coverage_ledger"]["matrix"]:
    c = cov["closure"]
    closures[c] = closures.get(c, 0) + 1
for k, v in sorted(closures.items()):
    print(f"  {k}: {v}")

print(f"\nContract coverage summary:")
closures = {}
for cov in analysis["coverage_ledger"]["contract"]:
    c = cov["closure"]
    closures[c] = closures.get(c, 0) + 1
for k, v in sorted(closures.items()):
    print(f"  {k}: {v}")
