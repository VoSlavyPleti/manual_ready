import json

import os
base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'batch_2_fragment.json'), 'r') as f:
    data = json.load(f)

batch_ids = [
    "4.2.17", "4.2.18", "4.2.19", "4.2.20.1", "4.2.20.2", "4.2.20.3", "4.2.20.4",
    "4.2.20.5", "4.2.20.6", "4.2.20.7", "4.2.21.1", "4.2.21.2", "4.2.21.3",
    "4.2.21.4", "4.2.21.5", "4.2.21.6", "4.2.21.7", "4.2.21.8", "4.2.22", "4.2.23",
    "4.2.24", "4.2.25", "4.2.26", "5.1.1.1", "5.1.1.2", "5.1.1.3", "5.1.1.4",
    "5.1.1.5", "5.1.1.6", "5.1.2", "5.1.3", "5.1.4", "5.1.5", "5.1.6", "5.1.7",
    "5.1.8.1", "5.1.8.2", "5.1.8.3", "5.1.8.4"
]

errors = []

# 1. Every batch matrix id must appear exactly once
linked_ids = set()
for link in data['links']:
    for mid in link['matrix_ids']:
        linked_ids.add(mid)

unmatched_ids = set()
for um in data['unmatched_matrix']:
    unmatched_ids.add(um['matrix_id'])

all_covered = linked_ids | unmatched_ids

for bid in batch_ids:
    if bid not in all_covered:
        errors.append(f"MISSING: {bid} not in links or unmatched_matrix")
    if bid in linked_ids and bid in unmatched_ids:
        errors.append(f"DUPLICATE: {bid} in both links and unmatched_matrix")

for bid in all_covered:
    if bid not in batch_ids:
        errors.append(f"EXTRA: {bid} not in batch 2")

# 2. Every link must have non-empty contract_ids
for i, link in enumerate(data['links']):
    if not link['contract_ids']:
        errors.append(f"Link {i}: empty contract_ids")
    if link['relationship'] not in ('aligned', 'deviation'):
        errors.append(f"Link {i}: invalid relationship {link['relationship']}")
    if link['relationship'] == 'aligned' and link['discrepancies']:
        errors.append(f"Link {i}: aligned but has discrepancies")
    if link['relationship'] == 'deviation' and not link['discrepancies']:
        errors.append(f"Link {i}: deviation but no discrepancies")

# 3. Every atomic_link must have valid fields
for i, al in enumerate(data['atomic_links']):
    if al['analogue_strength'] not in ('strong', 'partial'):
        errors.append(f"Atomic {i}: invalid analogue_strength {al['analogue_strength']}")
    if al['analogue_strength'] == 'weak_context':
        errors.append(f"Atomic {i}: weak_context in atomic_links")
    if al['relationship'] not in ('aligned', 'deviation'):
        errors.append(f"Atomic {i}: invalid relationship")
    
    # Check element_checklist
    checklist = al.get('element_checklist', [])
    has_diff_or_missing = any(e['result'] in ('different', 'missing') for e in checklist)
    
    if al['relationship'] == 'deviation' and not has_diff_or_missing:
        errors.append(f"Atomic {i} ({al['matrix_id']}+{al['contract_id']}): deviation but no different/missing in checklist")
    if al['relationship'] == 'aligned' and has_diff_or_missing:
        errors.append(f"Atomic {i} ({al['matrix_id']}+{al['contract_id']}): aligned but has different/missing in checklist")
    if al['relationship'] == 'deviation' and not al.get('discrepancies'):
        errors.append(f"Atomic {i} ({al['matrix_id']}+{al['contract_id']}): deviation but no discrepancies")
    if al['relationship'] == 'aligned' and al.get('discrepancies'):
        errors.append(f"Atomic {i} ({al['matrix_id']}+{al['contract_id']}): aligned but has discrepancies")
    
    # Check required fields
    for field in ['matrix_id', 'contract_id', 'relationship', 'link_index', 'legal_topic',
                  'analogue_strength', 'coverage_role', 'coverage', 'element_checklist', 'status_reason']:
        if field not in al:
            errors.append(f"Atomic {i}: missing field {field}")

# 4. Every unmatched_matrix must have status = missing_in_contract
for i, um in enumerate(data['unmatched_matrix']):
    if um.get('status') != 'missing_in_contract':
        errors.append(f"Unmatched {i}: status is {um.get('status')}, not missing_in_contract")
    if 'matrix_id' not in um:
        errors.append(f"Unmatched {i}: missing matrix_id")
    if 'requirement' not in um:
        errors.append(f"Unmatched {i}: missing requirement")
    if 'risk' not in um:
        errors.append(f"Unmatched {i}: missing risk")

# 5. Cross-check atomic_links against links
link_indices = set(range(len(data['links'])))
for al in data['atomic_links']:
    if al['link_index'] is not None and al['link_index'] not in link_indices:
        errors.append(f"Atomic {al['matrix_id']}+{al['contract_id']}: link_index {al['link_index']} out of range")

# 6. Check that atomic pairs match their parent link
for al in data['atomic_links']:
    li = al['link_index']
    if li is not None:
        parent = data['links'][li]
        if al['matrix_id'] not in parent['matrix_ids']:
            errors.append(f"Atomic {al['matrix_id']}: not in parent link {li} matrix_ids")
        if al['contract_id'] not in parent['contract_ids']:
            errors.append(f"Atomic {al['contract_id']}: not in parent link {li} contract_ids")

# 7. Check for required elements in checklist
required_elements = {'party', 'legal_object', 'operative_right_or_duty', 'trigger', 'deadline',
                     'amount_formula_cap', 'procedure_channel', 'liability_remedy', 'scope_exceptions', 'consequence'}
for i, al in enumerate(data['atomic_links']):
    present = {e['element'] for e in al['element_checklist']}
    missing_elems = required_elements - present
    if missing_elems:
        errors.append(f"Atomic {i} ({al['matrix_id']}+{al['contract_id']}): missing checklist elements: {missing_elems}")

if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL CHECKS PASSED")

print(f"\nSummary:")
print(f"  Links: {len(data['links'])}")
print(f"  Atomic links: {len(data['atomic_links'])}")
print(f"  Unmatched matrix: {len(data['unmatched_matrix'])}")
print(f"  Unmatched contract: {len(data['unmatched_contract'])}")
print(f"  Batch ids: {len(batch_ids)}")
print(f"  Covered: {len(all_covered)}")
