import json, sys
from collections import Counter

with open('/outputs/discrepancy_analysis.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

errors = []

# Schema
for k in ['analysis_profile', 'links', 'atomic_links', 'unmatched_matrix', 'unmatched_contract', 'coverage_ledger', 'summary']:
    if k not in data:
        errors.append(f'Missing key: {k}')

# Summary counts
s = data.get('summary', {})
aa = sum(1 for l in data.get('links', []) if l.get('relationship') == 'aligned')
ad = sum(1 for l in data.get('links', []) if l.get('relationship') == 'deviation')
am = len(data.get('unmatched_matrix', []))
ae = len(data.get('unmatched_contract', []))
if s.get('aligned_count') != aa: errors.append(f'aligned_count: summary={s.get("aligned_count")} actual={aa}')
if s.get('deviation_count') != ad: errors.append(f'deviation_count: summary={s.get("deviation_count")} actual={ad}')
if s.get('missing_in_contract_count') != am: errors.append(f'missing_in_contract_count: summary={s.get("missing_in_contract_count")} actual={am}')
if s.get('extra_in_contract_count') != ae: errors.append(f'extra_in_contract_count: summary={s.get("extra_in_contract_count")} actual={ae}')

# Aligned consistency
for i, link in enumerate(data.get('links', [])):
    if link.get('relationship') == 'aligned':
        if link.get('discrepancies') and len(link['discrepancies']) > 0:
            errors.append(f'Link {i}: aligned has discrepancies')
        if link.get('risk_level') != 'none':
            errors.append(f'Link {i}: aligned risk_level={link.get("risk_level")}')

# Deviation consistency
for i, link in enumerate(data.get('links', [])):
    if link.get('relationship') == 'deviation':
        if not link.get('discrepancies') or len(link['discrepancies']) == 0:
            errors.append(f'Link {i}: deviation has no discrepancies')
        if link.get('risk_level') == 'none':
            errors.append(f'Link {i}: deviation risk_level=none')

# Unmatched matrix
for item in data.get('unmatched_matrix', []):
    if not item.get('risk_level'): errors.append(f'UM {item.get("matrix_id")}: no risk_level')
    if not item.get('risk'): errors.append(f'UM {item.get("matrix_id")}: no risk')
    if item.get('status') != 'missing_in_contract': errors.append(f'UM {item.get("matrix_id")}: status={item.get("status")}')

# Unmatched contract
for item in data.get('unmatched_contract', []):
    if not item.get('risk_level'): errors.append(f'UC {item.get("contract_id")}: no risk_level')
    if not item.get('risk'): errors.append(f'UC {item.get("contract_id")}: no risk')
    if not item.get('materiality_reason'): errors.append(f'UC {item.get("contract_id")}: no materiality_reason')
    if item.get('status') != 'extra_in_contract': errors.append(f'UC {item.get("contract_id")}: status={item.get("status")}')

# Atomic links
for i, al in enumerate(data.get('atomic_links', [])):
    li = al.get('link_index', -1)
    if li < 0 or li >= len(data.get('links', [])):
        errors.append(f'Atomic {i}: invalid link_index {li}')

# Coverage ledger
clm = set(r['matrix_id'] for r in data.get('coverage_ledger', {}).get('matrix', []))
with open('inputs/matrix.json', 'r', encoding='utf-8-sig') as f:
    allm = set(item['number'] for item in json.load(f))
missing_from_ledger = allm - clm
if missing_from_ledger:
    errors.append(f'Missing from coverage_ledger: {missing_from_ledger}')

# OOS in unmatched
for item in data.get('unmatched_matrix', []):
    for c in data.get('coverage_ledger', {}).get('matrix', []):
        if c['matrix_id'] == item['matrix_id'] and c['closure'] in ('out_of_scope', 'not_applicable'):
            errors.append(f'OOS in unmatched: {item["matrix_id"]}')

# Risk distribution
lr = Counter(l.get('risk_level') for l in data.get('links', []))
ur = Counter(i.get('risk_level') for i in data.get('unmatched_matrix', []))
cr = Counter(i.get('risk_level') for i in data.get('unmatched_contract', []))

print(f'Total errors: {len(errors)}')
for e in errors:
    print(f'  ERROR: {e}')
print(f'Link risks: {dict(lr)}')
print(f'Missing risks: {dict(ur)}')
print(f'Extra risks: {dict(cr)}')
print(f'Coverage ledger: {len(clm)}/{len(allm)} matrix ids')
print(f'Links: {len(data.get("links",[]))} (aligned={aa}, deviation={ad})')
print(f'Unmatched: matrix={am}, contract={ae}')
print(f'Atomic links: {len(data.get("atomic_links",[]))}')

if errors:
    print('VALIDATION FAILED')
    sys.exit(1)
else:
    print('VALIDATION PASSED')
