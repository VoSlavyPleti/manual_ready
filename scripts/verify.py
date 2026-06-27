import json

with open('inputs/matrix.json') as f:
    matrix = json.load(f)
with open('outputs/discrepancy_analysis.json') as f:
    analysis = json.load(f)

matrix_ids = [m['number'] for m in matrix]
print(f"Total matrix IDs in source: {len(matrix_ids)}")

clm = analysis['coverage_ledger']['matrix']
clm_ids = [x['matrix_id'] for x in clm]
print(f"Total CLM entries: {len(clm)}")

# Check for duplicates
from collections import Counter
counter = Counter(clm_ids)
dupes = {k: v for k, v in counter.items() if v > 1}
if dupes:
    print(f"DUPLICATE matrix IDs in CLM: {dupes}")
else:
    print("No duplicate matrix IDs in CLM")

# Check for missing
missing_in_clm = set(matrix_ids) - set(clm_ids)
if missing_in_clm:
    print(f"MISSING from CLM: {sorted(missing_in_clm)}")
else:
    print("All matrix IDs present in CLM")

# Check for extra
extra_in_clm = set(clm_ids) - set(matrix_ids)
if extra_in_clm:
    print(f"EXTRA in CLM (not in source): {sorted(extra_in_clm)}")
else:
    print("No extra matrix IDs in CLM")

# Verify closure types
closures = {}
for x in clm:
    closures.setdefault(x['closure'], []).append(x['matrix_id'])
for c, ids in closures.items():
    print(f"  {c}: {len(ids)}")

# Verify consistency: linked -> in links
linked_clm = set(x['matrix_id'] for x in clm if x['closure'] == 'linked')
all_linked_matrix = set()
for link in analysis['links']:
    for mid in link['matrix_ids']:
        all_linked_matrix.add(mid)
not_in_links = linked_clm - all_linked_matrix
if not_in_links:
    print(f"CLM 'linked' but NOT in links: {sorted(not_in_links)}")

# missing_in_contract -> in unmatched_matrix
missing_clm = set(x['matrix_id'] for x in clm if x['closure'] == 'missing_in_contract')
um_ids = set(x['matrix_id'] for x in analysis['unmatched_matrix'])
not_in_um = missing_clm - um_ids
if not_in_um:
    print(f"CLM 'missing_in_contract' but NOT in unmatched_matrix: {sorted(not_in_um)}")
um_not_in_clm = um_ids - missing_clm
if um_not_in_clm:
    print(f"In unmatched_matrix but CLM not 'missing_in_contract': {sorted(um_not_in_clm)}")

# Verify summary counts
s = analysis['summary']
print(f"\nSummary counts: aligned={s['aligned_count']}, deviation={s['deviation_count']}, missing={s['missing_in_contract_count']}, extra={s['extra_in_contract_count']}")
print(f"Actual: aligned={len(analysis['links'])} links ({sum(1 for l in analysis['links'] if l['relationship']=='aligned')} aligned + {sum(1 for l in analysis['links'] if l['relationship']=='deviation')} deviation), missing={len(analysis['unmatched_matrix'])}, extra={len(analysis['unmatched_contract'])}")
