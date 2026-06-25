import json

f = json.load(open('outputs/working/batch3_fragment.json', encoding='utf-8'))

issues = []
for al in f['atomic_links']:
    if al['analogue_strength'] == 'weak_context':
        issues.append(f"WARNING: weak_context in {al['matrix_id']}+{al['contract_id']}")
    if al['relationship'] == 'deviation' and not al['discrepancies']:
        issues.append(f"WARNING: deviation without discrepancies: {al['matrix_id']}+{al['contract_id']}")
    if al['relationship'] == 'aligned' and al['discrepancies']:
        issues.append(f"WARNING: aligned with discrepancies: {al['matrix_id']}+{al['contract_id']}")
    if al['relationship'] == 'deviation':
        has_diff = any(e['result'] in ('different', 'missing') for e in al['element_checklist'])
        if not has_diff:
            issues.append(f"WARNING: deviation without different/missing checklist: {al['matrix_id']}+{al['contract_id']}")

for m in f['unmatched_matrix']:
    if m['status'] != 'missing_in_contract':
        issues.append(f"WARNING: unmatched_matrix {m['matrix_id']} has status {m['status']}")

if issues:
    for i in issues:
        print(i)
else:
    print("QA PASSED - no issues found")
