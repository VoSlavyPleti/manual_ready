import json
with open('outputs/discrepancy_analysis.json', 'r') as f:
    a = json.load(f)

print('=== UNMATCHED MATRIX ===')
for m in a['unmatched_matrix']:
    req = m['requirement'][:120]
    print(f"  {m['matrix_id']}: {req} [{m['risk_level']}]")

print('\n=== UNMATCHED CONTRACT ===')
for c in a['unmatched_contract']:
    pos = c['contract_position'][:120]
    print(f"  {c['contract_id']}: {pos} [{c['risk_level']}]")

print('\n=== SUMMARY ===')
print(json.dumps(a['summary'], indent=2))
