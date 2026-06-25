import json

f = json.load(open('outputs/working/batch3_fragment.json', encoding='utf-8'))

print('=== DEVIATIONS ===')
for l in f['links']:
    if l['relationship'] == 'deviation':
        print(f"  {l['matrix_ids']} -> {l['contract_ids']}: {l['legal_topic'][:80]}")
        for d in l['discrepancies']:
            print(f'    - {d["type"]}: {d["description"][:120]}')

print()
print('=== UNMATCHED MATRIX ===')
for m in f['unmatched_matrix']:
    print(f"  {m['matrix_id']}: {m['requirement'][:120]}")
    print(f'    risk: {m["risk"][:120]}')
    if 'rejected_candidates' in m:
        for rc in m['rejected_candidates']:
            print(f'    rejected: {rc["contract_id"]} - {rc["reason"][:80]}')

print()
print('=== UNMATCHED CONTRACT ===')
for c in f['unmatched_contract']:
    print(f"  {c['contract_id']}: {c['contract_position'][:120]}")
    print(f'    status: {c["status"]}')

print()
print('=== ATOMIC DEVIATIONS ===')
for al in f['atomic_links']:
    if al['relationship'] == 'deviation':
        print(f"  {al['matrix_id']}+{al['contract_id']}: {al['status_reason'][:120]}")
        for e in al['element_checklist']:
            if e['result'] in ('different', 'missing'):
                print(f'    {e["element"]}: {e["result"]} - {e["note"][:120]}')

# Summary
aligned = sum(1 for l in f['links'] if l['relationship'] == 'aligned')
deviations = sum(1 for l in f['links'] if l['relationship'] == 'deviation')
print(f'\n=== SUMMARY ===')
print(f'  aligned links: {aligned}')
print(f'  deviation links: {deviations}')
print(f'  unmatched_matrix: {len(f["unmatched_matrix"])}')
print(f'  unmatched_contract: {len(f["unmatched_contract"])}')
print(f'  total matrix ids: {len(f["batch_ids"])}')
