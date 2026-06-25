import json

with open('outputs/working/batch_1_fragment.json', 'r') as f:
    data = json.load(f)

with open('outputs/working/batch_1_ids.json', 'r') as f:
    batch_ids = json.load(f)

linked_ids = set()
for link in data['links']:
    for mid in link['matrix_ids']:
        linked_ids.add(mid)

unmatched_ids = set()
for um in data['unmatched_matrix']:
    unmatched_ids.add(um['matrix_id'])

all_covered = linked_ids | unmatched_ids
batch_set = set(batch_ids)

print(f'Batch IDs: {len(batch_set)}')
print(f'Linked IDs: {len(linked_ids)}')
print(f'Unmatched IDs: {len(unmatched_ids)}')
print(f'Total covered: {len(all_covered)}')
print(f'Missing from coverage: {batch_set - all_covered}')
print(f'Extra (not in batch): {all_covered - batch_set}')
print()

# Check atomic_links
atomic_pairs = set()
for al in data['atomic_links']:
    atomic_pairs.add((al['matrix_id'], al['contract_id']))

for i, link in enumerate(data['links']):
    for mid in link['matrix_ids']:
        for cid in link['contract_ids']:
            if (mid, cid) not in atomic_pairs:
                print(f'MISSING atomic pair: link[{i}] {mid} <-> {cid}')

for al in data['atomic_links']:
    if al['analogue_strength'] == 'weak_context':
        print(f'WEAK CONTEXT in atomic: {al["matrix_id"]} <-> {al["contract_id"]}')
    if al['relationship'] == 'deviation':
        has_gap = any(e['result'] in ('different', 'missing') for e in al['element_checklist'])
        if not has_gap:
            print(f'DEVIATION without gap: {al["matrix_id"]} <-> {al["contract_id"]}')
        if len(al.get('discrepancies', [])) == 0:
            print(f'DEVIATION without discrepancies: {al["matrix_id"]} <-> {al["contract_id"]}')
    if al['relationship'] == 'aligned':
        has_gap = any(e['result'] in ('different', 'missing') for e in al['element_checklist'])
        if has_gap:
            print(f'ALIGNED with gap: {al["matrix_id"]} <-> {al["contract_id"]}')

for um in data['unmatched_matrix']:
    if um['status'] != 'missing_in_contract':
        print(f'BAD STATUS: {um["matrix_id"]} status={um["status"]}')

for i, link in enumerate(data['links']):
    if len(link['contract_ids']) == 0:
        print(f'EMPTY contract_ids in link[{i}]')
    if link['relationship'] == 'aligned' and len(link['discrepancies']) > 0:
        print(f'ALIGNED with discrepancies in link[{i}]')
    if link['relationship'] == 'deviation' and len(link['discrepancies']) == 0:
        print(f'DEVIATION without discrepancies in link[{i}]')

# Check contract_ids are real
contract_ids_used = set()
for link in data['links']:
    for cid in link['contract_ids']:
        contract_ids_used.add(cid)
for al in data['atomic_links']:
    contract_ids_used.add(al['contract_id'])
print(f'\nContract IDs used: {sorted(contract_ids_used)}')

# Check link_index references
for al in data['atomic_links']:
    if al['link_index'] is not None:
        if al['link_index'] >= len(data['links']):
            print(f'BAD link_index: {al["matrix_id"]} link_index={al["link_index"]}')

print('\nValidation complete.')
