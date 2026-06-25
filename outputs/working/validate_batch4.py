import json

with open('outputs/working/batch_4_ids.json') as f:
    batch_ids = json.load(f)
with open('outputs/working/batch_4_fragment.json') as f:
    fragment = json.load(f)

linked_ids = set()
for link in fragment['links']:
    for mid in link['matrix_ids']:
        linked_ids.add(mid)

unmatched_ids = set()
for um in fragment['unmatched_matrix']:
    unmatched_ids.add(um['matrix_id'])

all_covered = linked_ids | unmatched_ids
missing = set(batch_ids) - all_covered
extra = all_covered - set(batch_ids)

print(f"Batch IDs: {len(batch_ids)}")
print(f"Linked: {len(linked_ids)}, Unmatched: {len(unmatched_ids)}, Covered: {len(all_covered)}")
print(f"Missing: {sorted(missing)}")
print(f"Extra: {sorted(extra)}")

for al in fragment['atomic_links']:
    mid = al['matrix_id']
    cid = al['contract_id']
    if al['relationship'] == 'deviation':
        has_gap = any(e['result'] in ('different', 'missing') for e in al['element_checklist'])
        if not has_gap:
            print(f"ISSUE dev no gap: {mid}+{cid}")
        if not al['discrepancies']:
            print(f"ISSUE dev no disc: {mid}+{cid}")
    if al['relationship'] == 'aligned':
        has_gap = any(e['result'] in ('different', 'missing') for e in al['element_checklist'])
        if has_gap:
            print(f"ISSUE aligned gap: {mid}+{cid}")
        if al['discrepancies']:
            print(f"ISSUE aligned disc: {mid}+{cid}")
    if al['analogue_strength'] == 'weak_context':
        print(f"ISSUE weak: {mid}+{cid}")

# Check link-level consistency
for i, link in enumerate(fragment['links']):
    if link['relationship'] == 'deviation' and not link['discrepancies']:
        print(f"ISSUE link dev no disc: link {i}")
    if link['relationship'] == 'aligned' and link['discrepancies']:
        print(f"ISSUE link aligned disc: link {i}")

print("Done")
