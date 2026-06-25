#!/usr/bin/env python3
"""Merge batch fragments and contract-only findings into one unified artifact."""
import json, os

import pathlib
WORKING = str(pathlib.Path(__file__).parent)

# Load all batch fragments
batches = []
for fname in ['batch_1_fragment.json', 'batch_2_fragment.json', 'batch3_fragment.json', 'batch_4_fragment.json']:
    with open(os.path.join(WORKING, fname)) as f:
        batches.append(json.load(f))

# Load contract-only findings
with open(os.path.join(WORKING, 'contract_only_findings_v2.json')) as f:
    contract_only = json.load(f)

# Merge
merged = {
    'links': [],
    'atomic_links': [],
    'unmatched_matrix': [],
    'unmatched_contract': []
}

# Track all matrix ids for coverage check
all_matrix_ids = set()
linked_matrix_ids = set()
unmatched_matrix_ids = set()

for b in batches:
    for link in b.get('links', []):
        merged['links'].append(link)
        for mid in link.get('matrix_ids', []):
            linked_matrix_ids.add(mid)
    for al in b.get('atomic_links', []):
        merged['atomic_links'].append(al)
    for um in b.get('unmatched_matrix', []):
        merged['unmatched_matrix'].append(um)
        unmatched_matrix_ids.add(um.get('matrix_id', ''))
    for uc in b.get('unmatched_contract', []):
        merged['unmatched_contract'].append(uc)

# Add contract-only findings
for item in contract_only:
    merged['unmatched_contract'].append(item)

# Load matrix inventory to get all ids
with open(os.path.join(WORKING, 'matrix_inventory.json')) as f:
    matrix_inv = json.load(f)
all_matrix_ids = set(i['id'] for i in matrix_inv if i['materiality'] == 'material')

# Coverage check
covered = linked_matrix_ids | unmatched_matrix_ids
missing = all_matrix_ids - covered
extra_in_links = linked_matrix_ids - all_matrix_ids
extra_in_unmatched = unmatched_matrix_ids - all_matrix_ids

print(f"Total material matrix ids: {len(all_matrix_ids)}")
print(f"Linked: {len(linked_matrix_ids)}")
print(f"Unmatched: {len(unmatched_matrix_ids)}")
print(f"Covered: {len(covered)}")
print(f"Missing from coverage: {len(missing)}")
if missing:
    print(f"  Missing ids: {sorted(missing)}")
if extra_in_links:
    print(f"  Extra in links: {extra_in_links}")
if extra_in_unmatched:
    print(f"  Extra in unmatched: {extra_in_unmatched}")

# Re-index atomic_links link_index
link_index_map = {}
for i, link in enumerate(merged['links']):
    for mid in link.get('matrix_ids', []):
        for cid in link.get('contract_ids', []):
            key = (mid, cid)
            link_index_map[key] = i

for al in merged['atomic_links']:
    key = (al['matrix_id'], al['contract_id'])
    if key in link_index_map:
        al['link_index'] = link_index_map[key]
    else:
        print(f"WARNING: atomic pair {key} not found in any grouped link")

# Compute summary
aligned_count = sum(1 for l in merged['links'] if l['relationship'] == 'aligned')
deviation_count = sum(1 for l in merged['links'] if l['relationship'] == 'deviation')
missing_count = len(merged['unmatched_matrix'])
extra_count = sum(1 for u in merged['unmatched_contract'] if u.get('status') == 'extra_in_contract')

merged['summary'] = {
    'aligned_count': aligned_count,
    'deviation_count': deviation_count,
    'missing_in_contract_count': missing_count,
    'extra_in_contract_count': extra_count
}

print(f"\nSummary:")
print(f"  Aligned links: {aligned_count}")
print(f"  Deviation links: {deviation_count}")
print(f"  Missing in contract: {missing_count}")
print(f"  Extra in contract: {extra_count}")
print(f"  Atomic links: {len(merged['atomic_links'])}")
print(f"  Unmatched contract total: {len(merged['unmatched_contract'])}")

# Write merged artifact
with open(os.path.join(WORKING, 'merged_artifact.json'), 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("\nMerged artifact written to /outputs/working/merged_artifact.json")
