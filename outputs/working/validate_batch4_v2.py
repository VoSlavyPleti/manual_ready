import json, os

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, 'batch_4_fragment.json'), 'r') as f:
    data = json.load(f)

# 1. Check all required top-level keys
required_keys = ['links', 'atomic_links', 'unmatched_matrix', 'unmatched_contract', 'summary']
for k in required_keys:
    if k == 'summary':
        print(f'{k}: {data.get(k)}')
    else:
        print(f'{k}: present={k in data}, count={len(data.get(k, []))}')

# 2. Check all atomic_links have required fields
required_atomic = ['matrix_id', 'contract_id', 'relationship', 'link_index', 'legal_topic', 'analogue_strength', 'coverage_role', 'coverage', 'element_checklist', 'status_reason']
atomic_issues = []
for i, al in enumerate(data['atomic_links']):
    for f in required_atomic:
        if f not in al:
            atomic_issues.append(f'atomic[{i}] missing {f}')
    strength = al.get('analogue_strength', '')
    if strength not in ('strong', 'partial'):
        atomic_issues.append(f'atomic[{i}] bad analogue_strength: {strength}')
    role = al.get('coverage_role', '')
    valid_roles = ('direct', 'parent', 'child', 'framework', 'procedure', 'liability', 'payment', 'appendix', 'context')
    if role not in valid_roles:
        atomic_issues.append(f'atomic[{i}] bad coverage_role: {role}')
    for j, item in enumerate(al.get('element_checklist', [])):
        if 'element' not in item or 'result' not in item:
            atomic_issues.append(f'atomic[{i}] checklist[{j}] missing element/result')
        result = item.get('result', '')
        if result not in ('same', 'equivalent', 'different', 'missing', 'not_applicable'):
            atomic_issues.append(f'atomic[{i}] checklist[{j}] bad result: {result}')
    if al.get('relationship') == 'deviation':
        has_gap = any(item.get('result') in ('different', 'missing') for item in al.get('element_checklist', []))
        if not has_gap:
            atomic_issues.append(f'atomic[{i}] deviation but no different/missing checklist items')

if atomic_issues:
    print('ATOMIC ISSUES:')
    for issue in atomic_issues:
        print(f'  {issue}')
else:
    print('All atomic_links pass validation')

# 3. Check no weak_context in atomic_links
weak = [al for al in data['atomic_links'] if al.get('analogue_strength') == 'weak_context']
if weak:
    print(f'WARNING: {len(weak)} atomic_links with weak_context strength')
else:
    print('No weak_context in atomic_links')

# 4. Check link_index references are valid
max_link = len(data['links']) - 1
bad_indices = [al for al in data['atomic_links'] if al.get('link_index', -1) > max_link or al.get('link_index', -1) < 0]
if bad_indices:
    print(f'WARNING: {len(bad_indices)} atomic_links with bad link_index')
else:
    print('All link_index values valid')

# 5. Verify all matrix_ids in links match batch scope
with open(os.path.join(base, 'batch_4_ids.json'), 'r') as f:
    batch_ids = set(json.load(f))
all_matrix = set()
for link in data['links']:
    all_matrix.update(link['matrix_ids'])
extra = all_matrix - batch_ids
missing_from_batch = batch_ids - all_matrix
if extra:
    print(f'WARNING: extra matrix_ids: {extra}')
if missing_from_batch:
    print(f'WARNING: missing from batch: {missing_from_batch}')
if not extra and not missing_from_batch:
    print('All batch IDs covered, no extras')

print('Done.')
