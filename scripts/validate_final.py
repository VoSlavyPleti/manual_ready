import json, sys

with open('outputs/discrepancy_analysis.json', 'r') as f:
    a = json.load(f)

errors = []

# Verify structure
required_keys = ['analysis_profile', 'links', 'unmatched_matrix', 'unmatched_contract', 'coverage_ledger', 'summary']
for k in required_keys:
    if k not in a:
        errors.append(f'Missing key: {k}')

# Verify analysis_profile
if 'product' not in a['analysis_profile']:
    errors.append('Missing analysis_profile.product')
if 'legal_regime' not in a['analysis_profile']:
    errors.append('Missing analysis_profile.legal_regime')

# Verify links structure
for i, link in enumerate(a['links']):
    for k in ['contract_ids', 'matrix_ids', 'relationship', 'risk_level']:
        if k not in link:
            errors.append(f'Link {i}: missing {k}')
    if link.get('relationship') not in ('aligned', 'deviation'):
        errors.append(f'Link {i}: invalid relationship')
    if link.get('risk_level') not in ('none', 'low', 'medium', 'high'):
        errors.append(f'Link {i}: invalid risk_level')
    if link.get('relationship') == 'aligned' and link.get('discrepancies'):
        errors.append(f'Link {i}: aligned but has discrepancies {link["matrix_ids"]}')
    if link.get('relationship') == 'deviation' and not link.get('discrepancies'):
        errors.append(f'Link {i}: deviation but no discrepancies {link["matrix_ids"]}')

# Verify unmatched
for m in a['unmatched_matrix']:
    if m.get('status') != 'missing_in_contract':
        errors.append(f'Unmatched matrix {m["matrix_id"]}: bad status')
for c in a['unmatched_contract']:
    if c.get('status') != 'extra_in_contract':
        errors.append(f'Unmatched contract {c["contract_id"]}: bad status')

# Verify summary counts
s = a['summary']
if s['aligned_count'] + s['deviation_count'] != len(a['links']):
    errors.append('Link counts mismatch')
if s['missing_in_contract_count'] != len(a['unmatched_matrix']):
    errors.append('Missing matrix count mismatch')
if s['extra_in_contract_count'] != len(a['unmatched_contract']):
    errors.append('Extra contract count mismatch')

if errors:
    print('ERRORS:')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('All structure validations passed!')
    print(f'Links: {len(a["links"])} (aligned: {s["aligned_count"]}, deviation: {s["deviation_count"]})')
    print(f'Unmatched matrix: {len(a["unmatched_matrix"])}')
    print(f'Unmatched contract: {len(a["unmatched_contract"])}')
    print(f'Matrix coverage: {len(a["coverage_ledger"]["matrix"])}')
    print(f'Contract coverage: {len(a["coverage_ledger"]["contract"])}')
    print(f'File size: {len(json.dumps(a, ensure_ascii=False)):,} chars')
