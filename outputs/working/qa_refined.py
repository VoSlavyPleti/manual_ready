#!/usr/bin/env python3
"""Refined QA validation for merged discrepancy analysis artifact."""
import json, os, sys

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, 'merged_artifact.json'), 'r') as f:
    data = json.load(f)
with open(os.path.join(base, 'contract_inventory.json'), 'r') as f:
    cinv = json.load(f)
with open(os.path.join(base, 'matrix_inventory.json'), 'r') as f:
    minv = json.load(f)

cinv_ids = set(item['id'] for item in cinv)
minv_ids = set(item['id'] for item in minv)
errors = []
warnings = []

# ============================================================
# 1. Contract IDs in links/atomic_links vs contract_inventory
# ============================================================
bad_contract_ids = set()
for link in data['links']:
    for cid in link['contract_ids']:
        if cid not in cinv_ids:
            bad_contract_ids.add(cid)
for al in data['atomic_links']:
    cid = al['contract_id']
    if cid not in cinv_ids:
        bad_contract_ids.add(cid)

# Check if bad IDs are composite locators (section heading + sub-clause)
# The contract uses bare "0.X" in inventory but merged artifact uses "Section, p. 0.X"
# Let's check if stripping the section prefix helps
for cid in sorted(bad_contract_ids):
    # Try to extract the bare sub-clause number
    parts = cid.split(', ')
    if len(parts) == 2:
        bare = parts[1].replace('п. ', '')
        if bare in cinv_ids:
            warnings.append(f"Contract ID '{cid}' uses composite format; bare '{bare}' exists in inventory. Consider using bare locator or adding composite to inventory.")
        else:
            errors.append(f"Contract ID '{cid}' not in contract_inventory (composite format, bare '{bare}' also not found)")
    else:
        errors.append(f"Contract ID '{cid}' not in contract_inventory")

# ============================================================
# 2. Invented / parenthetical IDs check
# ============================================================
# "0.0.1", "0.0.2", "0.0.3" ARE real printed locators in contract.txt (lines 95-97)
# "0.1" through "0.17" ARE real printed locators in contract.txt
# The composite forms like "7. ОТВЕТСТВЕННОСТЬ сторон, п. 0.1" combine section heading + sub-clause
# These are descriptive but the bare sub-clause numbers are the actual printed locators

# Check for truly invented patterns
invented_patterns = []
for link in data['links']:
    for cid in link['contract_ids']:
        # Check for parenthetical-only ids (not in contract.txt)
        if cid.startswith('(') and cid.endswith(')'):
            invented_patterns.append(cid)

if invented_patterns:
    errors.append(f"Parenthetical contract IDs found: {invented_patterns}")

# ============================================================
# 3. Summary counts
# ============================================================
aligned = sum(1 for l in data['links'] if l['relationship'] == 'aligned')
deviation = sum(1 for l in data['links'] if l['relationship'] == 'deviation')
missing = len(data.get('unmatched_matrix', []))
extra = sum(1 for c in data.get('unmatched_contract', []) if c.get('status') == 'extra_in_contract')
not_material = sum(1 for c in data.get('unmatched_contract', []) if c.get('status') == 'not_material')

s = data['summary']
if aligned != s.get('aligned_count', -1):
    errors.append(f"Summary aligned_count={s.get('aligned_count')}, actual={aligned}")
if deviation != s.get('deviation_count', -1):
    errors.append(f"Summary deviation_count={s.get('deviation_count')}, actual={deviation}")
if missing != s.get('missing_in_contract_count', -1):
    errors.append(f"Summary missing_in_contract_count={s.get('missing_in_contract_count')}, actual={missing}")
if extra != s.get('extra_in_contract_count', -1):
    errors.append(f"Summary extra_in_contract_count={s.get('extra_in_contract_count')}, actual={extra}")

# ============================================================
# 4. Matrix coverage
# ============================================================
linked_matrix_ids = set()
for link in data['links']:
    for mid in link['matrix_ids']:
        linked_matrix_ids.add(mid)
unmatched_matrix_ids = set(item['matrix_id'] for item in data.get('unmatched_matrix', []))
all_matrix_ids = linked_matrix_ids | unmatched_matrix_ids
material_minv_ids = set(item['id'] for item in minv if item.get('materiality') == 'material')

missing_from_both = material_minv_ids - all_matrix_ids
if missing_from_both:
    errors.append(f"Material matrix items not in links or unmatched_matrix: {sorted(missing_from_both)}")

# Check for duplicates
seen = set()
dups = set()
for link in data['links']:
    for mid in link['matrix_ids']:
        if mid in seen:
            dups.add(mid)
        seen.add(mid)
for item in data.get('unmatched_matrix', []):
    mid = item['matrix_id']
    if mid in seen:
        dups.add(mid)
    seen.add(mid)
if dups:
    errors.append(f"Duplicate matrix ids: {sorted(dups)}")

# ============================================================
# 5. Atomic links structure
# ============================================================
required_fields = ['matrix_id', 'contract_id', 'relationship', 'link_index', 'legal_topic',
                   'analogue_strength', 'coverage_role', 'coverage', 'element_checklist']
checklist_elements = ['party', 'legal_object', 'operative_right_or_duty', 'trigger', 'deadline',
                      'amount_formula_cap', 'procedure_channel', 'liability_remedy', 'scope_exceptions', 'consequence']
valid_results = {'same', 'equivalent', 'different', 'missing', 'not_applicable'}

for i, al in enumerate(data['atomic_links']):
    for f in required_fields:
        if f not in al:
            errors.append(f"atomic_links[{i}]: missing required field '{f}'")
    if al.get('analogue_strength') == 'weak_context':
        errors.append(f"atomic_links[{i}]: weak_context analogue_strength not allowed in atomic_links")
    checklist = al.get('element_checklist', [])
    found_elements = set()
    for item in checklist:
        e = item.get('element')
        r = item.get('result')
        found_elements.add(e)
        if r not in valid_results:
            errors.append(f"atomic_links[{i}]: invalid checklist result '{r}' for element '{e}'")
    for expected in checklist_elements:
        if expected not in found_elements:
            errors.append(f"atomic_links[{i}]: missing checklist element '{expected}'")
    rel = al.get('relationship')
    has_diff_or_missing = any(item.get('result') in ('different', 'missing') for item in checklist)
    if rel == 'deviation' and not has_diff_or_missing:
        errors.append(f"atomic_links[{i}]: relationship=deviation but no checklist item marked different/missing")
    if rel == 'aligned' and has_diff_or_missing:
        errors.append(f"atomic_links[{i}]: relationship=aligned but has checklist item(s) marked different/missing")

# ============================================================
# 6. Unmatched matrix status
# ============================================================
for item in data.get('unmatched_matrix', []):
    if item.get('status') != 'missing_in_contract':
        errors.append(f"unmatched_matrix {item['matrix_id']}: status is '{item.get('status')}', must be 'missing_in_contract'")

# ============================================================
# 7. Deviation links must have discrepancies
# ============================================================
for i, link in enumerate(data['links']):
    if link['relationship'] == 'deviation':
        if not link.get('discrepancies'):
            errors.append(f"links[{i}]: deviation but discrepancies array is empty")
        else:
            for j, d in enumerate(link['discrepancies']):
                if not d.get('type'):
                    errors.append(f"links[{i}].discrepancies[{j}]: missing 'type'")
                if not d.get('description'):
                    errors.append(f"links[{i}].discrepancies[{j}]: missing 'description'")
                if not d.get('risk'):
                    errors.append(f"links[{i}].discrepancies[{j}]: missing 'risk'")

# ============================================================
# 8. Aligned links must have NO discrepancies
# ============================================================
for i, link in enumerate(data['links']):
    if link['relationship'] == 'aligned' and link.get('discrepancies'):
        errors.append(f"links[{i}]: aligned but has non-empty discrepancies")

# ============================================================
# 9. No empty contract_ids
# ============================================================
for i, link in enumerate(data['links']):
    if not link.get('contract_ids'):
        errors.append(f"links[{i}]: empty contract_ids array")

# ============================================================
# 10. Contract-only material items coverage
# ============================================================
material_cinv = [item for item in cinv if item.get('materiality') == 'material']
linked_contract_ids = set()
for link in data['links']:
    for cid in link['contract_ids']:
        linked_contract_ids.add(cid)
unmatched_contract_ids = set(item['contract_id'] for item in data.get('unmatched_contract', []))

for item in material_cinv:
    cid = item['id']
    if cid not in linked_contract_ids and cid not in unmatched_contract_ids:
        warnings.append(f"Material contract item '{cid}' not in links or unmatched_contract")

# ============================================================
# 11. Check atomic_links link_index references
# ============================================================
for i, al in enumerate(data['atomic_links']):
    li = al.get('link_index')
    if li is None or li < 0 or li >= len(data['links']):
        errors.append(f"atomic_links[{i}]: invalid link_index={li}")

# ============================================================
# REPORT
# ============================================================
print("=" * 60)
print("REFINED QA VALIDATION RESULTS")
print("=" * 60)
print(f"\nERRORS: {len(errors)}")
for e in errors:
    print(f"  ERROR: {e}")
print(f"\nWARNINGS: {len(warnings)}")
for w in warnings:
    print(f"  WARNING: {w}")

print(f"\nSUMMARY:")
print(f"  links: {len(data['links'])}")
print(f"  atomic_links: {len(data['atomic_links'])}")
print(f"  unmatched_matrix: {len(data.get('unmatched_matrix', []))}")
print(f"  unmatched_contract: {len(data.get('unmatched_contract', []))}")
print(f"  aligned (actual): {aligned}")
print(f"  deviation (actual): {deviation}")
print(f"  missing_in_contract (actual): {missing}")
print(f"  extra_in_contract (actual): {extra}")
print(f"  not_material (actual): {not_material}")

sys.exit(len(errors))
