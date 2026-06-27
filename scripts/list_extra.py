import json
with open('outputs/discrepancy_analysis.json') as f:
    d = json.load(f)
print('EXTRA items:')
for i, uc in enumerate(d['unmatched_contract']):
    print(f"  [{i}] {uc['contract_id']}: {uc['contract_position'][:100]}")
