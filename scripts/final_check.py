import json

with open('outputs/discrepancy_analysis.json') as f:
    data = json.load(f)

# Print all not_material clauses for review
nm = [(c['contract_id'], c['reason']) for c in data['coverage_ledger']['contract'] if c['closure']=='not_material']
print('Not material clauses:')
for cid, reason in nm:
    print(f'  {cid}: {reason}')

print()
# Print all extra_in_contract with high/medium risk
extra_mh = [u for u in data['unmatched_contract'] if u['risk_level'] in ('high','medium')]
print(f'Extra contract (medium+ risk): {len(extra_mh)} items')
for u in extra_mh:
    pos = u['contract_position'][:120]
    print(f'  {u["contract_id"]}: {u["risk_level"]} - {pos}')

print()
# Print all missing_in_contract with high/medium risk
missing_mh = [u for u in data['unmatched_matrix'] if u['risk_level'] in ('high','medium')]
print(f'Missing matrix (medium+ risk): {len(missing_mh)} items')
for u in missing_mh:
    req = u['requirement'][:120]
    print(f'  {u["matrix_id"]}: {u["risk_level"]} - {req}')

print()
# Print all deviations
print('All deviations:')
for l in data['links']:
    if l['relationship'] == 'deviation':
        for d in l['discrepancies']:
            print(f'  {l["matrix_ids"]} -> {l["contract_ids"]}: [{d["type"]}] {d["description"][:100]}')
        print(f'    Risk: {l["risk_level"]} - {l["status_reason"][:120]}')
        print()
