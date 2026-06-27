import json

with open('outputs/discrepancy_analysis.json') as f:
    d = json.load(f)

# Contract 4.1 is still in unmatched_contract - remove it
d['unmatched_contract'] = [uc for uc in d['unmatched_contract'] if uc['contract_id'] != '4.1']

# Also remove from CLC any 'extra_in_contract' entry for 4.1
clc = d['coverage_ledger']['contract']
clc = [x for x in clc if not (x['contract_id'] == '4.1' and x['closure'] == 'extra_in_contract')]
d['coverage_ledger']['contract'] = clc

d['summary']['extra_in_contract_count'] = len(d['unmatched_contract'])

with open('outputs/discrepancy_analysis.json', 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Fixed. Extra count: {d['summary']['extra_in_contract_count']}")
print(f"Unmatched contract ids: {[uc['contract_id'] for uc in d['unmatched_contract']]}")
