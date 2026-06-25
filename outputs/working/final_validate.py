#!/usr/bin/env python3
"""Final validation of discrepancy_analysis.json"""
import json
from collections import Counter

import pathlib
PROJECT = str(pathlib.Path(__file__).parent.parent)
with open(PROJECT + '/discrepancy_analysis.json', 'r') as f:
    art = json.load(f)

print("Top-level keys:", list(art.keys()))
print("Summary:", json.dumps(art['summary'], indent=2))

aligned = sum(1 for l in art['links'] if l['relationship'] == 'aligned')
deviation = sum(1 for l in art['links'] if l['relationship'] == 'deviation')
print(f"Actual aligned: {aligned}, deviation: {deviation}")
print(f"Actual unmatched_matrix: {len(art['unmatched_matrix'])}")
extra = sum(1 for u in art['unmatched_contract'] if u['status'] == 'extra_in_contract')
not_mat = sum(1 for u in art['unmatched_contract'] if u['status'] == 'not_material')
print(f"Actual extra_in_contract: {extra}, not_material: {not_mat}")
print(f"Actual atomic_links: {len(art['atomic_links'])}")

# Check for duplicate matrix ids
mid_counts = Counter()
for l in art['links']:
    for mid in l['matrix_ids']:
        mid_counts[mid] += 1
for um in art['unmatched_matrix']:
    mid_counts[um['matrix_id']] += 1

dupes = {k: v for k, v in mid_counts.items() if v > 1}
if dupes:
    print(f"DUPLICATE matrix ids: {dupes}")
else:
    print("No duplicate matrix ids - OK")

# Check atomic_links fields
missing_fields = []
for al in art['atomic_links']:
    for field in ['matrix_id', 'contract_id', 'relationship', 'coverage',
                  'analogue_strength', 'coverage_role', 'element_checklist']:
        if field not in al:
            missing_fields.append((al.get('matrix_id', '?'), field))
if missing_fields:
    print(f"Missing fields in atomic_links: {missing_fields[:5]}")
else:
    print("All atomic_links have required fields - OK")

# No weak_context
weak = [al for al in art['atomic_links'] if al.get('analogue_strength') == 'weak_context']
print(f"Weak context in atomic_links: {len(weak)}")

# Deviation links have discrepancies
dev_no_disc = [l for l in art['links'] if l['relationship'] == 'deviation' and len(l.get('discrepancies', [])) == 0]
print(f"Deviation links without discrepancies: {len(dev_no_disc)}")

# Aligned links have no discrepancies
al_with_disc = [l for l in art['links'] if l['relationship'] == 'aligned' and len(l.get('discrepancies', [])) > 0]
print(f"Aligned links with discrepancies: {len(al_with_disc)}")

# Unmatched matrix status
bad_status = [um for um in art['unmatched_matrix'] if um.get('status') != 'missing_in_contract']
print(f"Unmatched matrix with wrong status: {len(bad_status)}")

# Check deviation atomic pairs have checklist gaps
dev_atomic_ok = True
for al in art['atomic_links']:
    if al['relationship'] == 'deviation':
        has_gap = any(e['result'] in ('different', 'missing') for e in al.get('element_checklist', []))
        if not has_gap:
            print(f"Deviation atomic pair without checklist gap: {al['matrix_id']} + {al['contract_id']}")
            dev_atomic_ok = False
if dev_atomic_ok:
    print("All deviation atomic pairs have checklist gaps - OK")

# Check aligned atomic pairs have no gaps
aligned_atomic_ok = True
for al in art['atomic_links']:
    if al['relationship'] == 'aligned':
        has_gap = any(e['result'] in ('different', 'missing') for e in al.get('element_checklist', []))
        if has_gap:
            print(f"Aligned atomic pair with checklist gap: {al['matrix_id']} + {al['contract_id']}")
            aligned_atomic_ok = False
if aligned_atomic_ok:
    print("All aligned atomic pairs have no checklist gaps - OK")

# Verify summary counts match
s = art['summary']
assert s['aligned_count'] == aligned, f"aligned_count mismatch: {s['aligned_count']} vs {aligned}"
assert s['deviation_count'] == deviation, f"deviation_count mismatch: {s['deviation_count']} vs {deviation}"
assert s['missing_in_contract_count'] == len(art['unmatched_matrix']), "missing count mismatch"
assert s['extra_in_contract_count'] == extra, f"extra count mismatch: {s['extra_in_contract_count']} vs {extra}"
print("Summary counts match arrays - OK")

print("\n=== VALIDATION COMPLETE ===")
