import json
from collections import Counter

with open('/outputs/discrepancy_analysis.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print('=== FINAL VALIDATION ===')
print()

# 1. Schema
required_keys = ['analysis_profile', 'links', 'atomic_links', 'unmatched_matrix', 'unmatched_contract', 'coverage_ledger', 'summary']
missing = [k for k in required_keys if k not in data]
print('Schema check:', 'PASS' if not missing else f'MISSING: {missing}')

# 2. Summary counts
s = data['summary']
actual_aligned = sum(1 for l in data['links'] if l['relationship'] == 'aligned')
actual_deviation = sum(1 for l in data['links'] if l['relationship'] == 'deviation')
actual_missing = len(data['unmatched_matrix'])
actual_extra = len(data['unmatched_contract'])
counts_ok = (s['aligned_count'] == actual_aligned and s['deviation_count'] == actual_deviation 
             and s['missing_in_contract_count'] == actual_missing and s['extra_in_contract_count'] == actual_extra)
print('Counts match:', 'PASS' if counts_ok else 'FAIL')
print(f'  Summary: aligned={s["aligned_count"]}, deviation={s["deviation_count"]}, missing={s["missing_in_contract_count"]}, extra={s["extra_in_contract_count"]}')
print(f'  Actual:  aligned={actual_aligned}, deviation={actual_deviation}, missing={actual_missing}, extra={actual_extra}')

# 3. Aligned links have empty discrepancies and risk=none
aligned_issues = []
for i, link in enumerate(data['links']):
    if link['relationship'] == 'aligned':
        if link.get('discrepancies') and len(link['discrepancies']) > 0:
            aligned_issues.append(f'Link {i}: aligned has discrepancies')
        if link.get('risk_level') != 'none':
            aligned_issues.append(f'Link {i}: aligned has risk_level={link["risk_level"]}')
print('Aligned consistency:', 'PASS' if not aligned_issues else f'FAIL: {aligned_issues}')

# 4. Deviation links have discrepancies
dev_issues = []
for i, link in enumerate(data['links']):
    if link['relationship'] == 'deviation':
        if not link.get('discrepancies') or len(link['discrepancies']) == 0:
            dev_issues.append(f'Link {i}: deviation has no discrepancies')
        if link.get('risk_level') == 'none':
            dev_issues.append(f'Link {i}: deviation has risk_level=none')
print('Deviation consistency:', 'PASS' if not dev_issues else f'FAIL: {dev_issues}')

# 5. Unmatched matrix items have required fields
um_issues = []
for item in data['unmatched_matrix']:
    if not item.get('risk_level'):
        um_issues.append(f'{item["matrix_id"]}: missing risk_level')
    if not item.get('risk'):
        um_issues.append(f'{item["matrix_id"]}: missing risk')
    if item.get('status') != 'missing_in_contract':
        um_issues.append(f'{item["matrix_id"]}: wrong status={item.get("status")}')
print('Unmatched matrix:', 'PASS' if not um_issues else f'FAIL: {um_issues[:5]}...')

# 6. Unmatched contract items have required fields
uc_issues = []
for item in data['unmatched_contract']:
    if not item.get('risk_level'):
        uc_issues.append(f'{item["contract_id"]}: missing risk_level')
    if not item.get('risk'):
        uc_issues.append(f'{item["contract_id"]}: missing risk')
    if not item.get('materiality_reason'):
        uc_issues.append(f'{item["contract_id"]}: missing materiality_reason')
    if item.get('status') != 'extra_in_contract':
        uc_issues.append(f'{item["contract_id"]}: wrong status')
print('Unmatched contract:', 'PASS' if not uc_issues else f'FAIL: {uc_issues[:5]}...')

# 7. Atomic links have link_index references
al_issues = []
for i, al in enumerate(data['atomic_links']):
    if al.get('link_index', -1) >= len(data['links']) or al.get('link_index', -1) < 0:
        al_issues.append(f'Atomic {i}: invalid link_index {al.get("link_index")}')
print('Atomic links:', 'PASS' if not al_issues else f'FAIL: {al_issues[:5]}...')

# 8. Coverage ledger completeness
cl_matrix_ids = set(r['matrix_id'] for r in data['coverage_ledger']['matrix'])
with open('/inputs/matrix.json', 'r', encoding='utf-8-sig') as f:
    matrix = json.load(f)
all_matrix = set(item['number'] for item in matrix)
missing_from_ledger = all_matrix - cl_matrix_ids
print('Coverage ledger matrix coverage:', 'PASS' if not missing_from_ledger else f'FAIL: missing {missing_from_ledger}')

# 9. No out_of_scope in unmatched_matrix
oos_in_um = []
for item in data['unmatched_matrix']:
    mid = item['matrix_id']
    for c in data['coverage_ledger']['matrix']:
        if c['matrix_id'] == mid and c['closure'] in ('out_of_scope', 'not_applicable'):
            oos_in_um.append(mid)
print('Out-of-scope in unmatched:', 'PASS' if not oos_in_um else f'FAIL: {oos_in_um}')

# 10. Risk level distribution
link_risks = Counter(l['risk_level'] for l in data['links'])
um_risks = Counter(i['risk_level'] for i in data['unmatched_matrix'])
uc_risks = Counter(i['risk_level'] for i in data['unmatched_contract'])
print(f'Link risk levels: {dict(link_risks)}')
print(f'Unmatched matrix risk levels: {dict(um_risks)}')
print(f'Unmatched contract risk levels: {dict(uc_risks)}')

print()
print('=== VALIDATION COMPLETE ===')
