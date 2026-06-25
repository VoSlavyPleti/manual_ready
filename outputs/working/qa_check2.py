#!/usr/bin/env python3
"""Deep QA checks on discrepancy_analysis.json."""
import json, os

_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "discrepancy_analysis.json")
_json_path = os.path.normpath(_json_path)
with open(_json_path, "r", encoding="utf-8") as f:
    d = json.load(f)

errors = []

# Check links
for i, link in enumerate(d['links']):
    if not link.get('contract_ids'):
        errors.append(f"link {i} has empty contract_ids")
    if not link.get('matrix_ids'):
        errors.append(f"link {i} has empty matrix_ids")
    if link.get('relationship') == 'deviation' and not link.get('discrepancies'):
        errors.append(f"link {i} is deviation but has empty discrepancies")
    if link.get('relationship') == 'aligned' and link.get('discrepancies'):
        errors.append(f"link {i} is aligned but has non-empty discrepancies")
    if link.get('relationship') == 'deviation' and link.get('risk_level') == 'none':
        errors.append(f"link {i} is deviation but risk_level=none")
    if link.get('relationship') == 'aligned' and link.get('risk_level') != 'none':
        errors.append(f"link {i} is aligned but risk_level={link.get('risk_level')}")

# Check atomic_links
for i, al in enumerate(d['atomic_links']):
    if not al.get('matrix_id'):
        errors.append(f"atomic_link {i} missing matrix_id")
    if not al.get('contract_id'):
        errors.append(f"atomic_link {i} missing contract_id")
    if not al.get('relationship'):
        errors.append(f"atomic_link {i} missing relationship")
    if not al.get('coverage_role'):
        errors.append(f"atomic_link {i} missing coverage_role")
    if not al.get('coverage'):
        errors.append(f"atomic_link {i} missing coverage")
    if al.get('link_index') is None:
        errors.append(f"atomic_link {i} missing link_index")

# Check unmatched_matrix
for i, um in enumerate(d['unmatched_matrix']):
    if not um.get('matrix_id'):
        errors.append(f"unmatched_matrix {i} missing matrix_id")
    if um.get('status') != 'missing_in_contract':
        errors.append(f"unmatched_matrix {i} status={um.get('status')}, expected missing_in_contract")
    if not um.get('risk_level'):
        errors.append(f"unmatched_matrix {i} missing risk_level")
    if not um.get('risk'):
        errors.append(f"unmatched_matrix {i} missing risk")

# Check unmatched_contract
for i, uc in enumerate(d['unmatched_contract']):
    if not uc.get('contract_id'):
        errors.append(f"unmatched_contract {i} missing contract_id")
    if uc.get('status') != 'extra_in_contract':
        errors.append(f"unmatched_contract {i} status={uc.get('status')}, expected extra_in_contract")
    if not uc.get('risk_level'):
        errors.append(f"unmatched_contract {i} missing risk_level")
    if not uc.get('risk'):
        errors.append(f"unmatched_contract {i} missing risk")

# Check coverage_ledger consistency
ledger_matrix_ids = {r['matrix_id'] for r in d['coverage_ledger']['matrix']}
ledger_contract_ids = {r['contract_id'] for r in d['coverage_ledger']['contract']}

# All linked matrix_ids should be in coverage_ledger
linked_matrix_ids = set()
for link in d['links']:
    for mid in link['matrix_ids']:
        linked_matrix_ids.add(mid)

# All unmatched_matrix ids should be in coverage_ledger
unmatched_matrix_ids = {r['matrix_id'] for r in d['unmatched_matrix']}

# All linked contract_ids should be in coverage_ledger
linked_contract_ids = set()
for link in d['links']:
    for cid in link['contract_ids']:
        linked_contract_ids.add(cid)

# All unmatched_contract ids should be in coverage_ledger
unmatched_contract_ids = {r['contract_id'] for r in d['unmatched_contract']}

# Check coverage_ledger matrix completeness
for mid in linked_matrix_ids:
    if mid not in ledger_matrix_ids:
        errors.append(f"linked matrix_id {mid} not in coverage_ledger.matrix")

for mid in unmatched_matrix_ids:
    if mid not in ledger_matrix_ids:
        errors.append(f"unmatched matrix_id {mid} not in coverage_ledger.matrix")

# Check coverage_ledger contract completeness
for cid in linked_contract_ids:
    if cid not in ledger_contract_ids:
        errors.append(f"linked contract_id {cid} not in coverage_ledger.contract")

for cid in unmatched_contract_ids:
    if cid not in ledger_contract_ids:
        errors.append(f"unmatched contract_id {cid} not in coverage_ledger.contract")

# Check that out_of_scope/not_applicable matrix ids are NOT in unmatched_matrix
for r in d['coverage_ledger']['matrix']:
    if r['closure'] in ('out_of_scope', 'not_applicable'):
        if r['matrix_id'] in unmatched_matrix_ids:
            errors.append(f"matrix_id {r['matrix_id']} is {r['closure']} but appears in unmatched_matrix")

# Check that not_material contract ids are NOT in unmatched_contract
for r in d['coverage_ledger']['contract']:
    if r['closure'] == 'not_material':
        if r['contract_id'] in unmatched_contract_ids:
            errors.append(f"contract_id {r['contract_id']} is not_material but appears in unmatched_contract")

# Check summary counts
summary = d['summary']
aligned_actual = sum(1 for l in d['links'] if l['relationship'] == 'aligned')
deviation_actual = sum(1 for l in d['links'] if l['relationship'] == 'deviation')
missing_actual = len(d['unmatched_matrix'])
extra_actual = len(d['unmatched_contract'])

if summary['aligned_count'] != aligned_actual:
    errors.append(f"summary.aligned_count={summary['aligned_count']} but actual={aligned_actual}")
if summary['deviation_count'] != deviation_actual:
    errors.append(f"summary.deviation_count={summary['deviation_count']} but actual={deviation_actual}")
if summary['missing_in_contract_count'] != missing_actual:
    errors.append(f"summary.missing_in_contract_count={summary['missing_in_contract_count']} but actual={missing_actual}")
if summary['extra_in_contract_count'] != extra_actual:
    errors.append(f"summary.extra_in_contract_count={summary['extra_in_contract_count']} but actual={extra_actual}")

# Check suspicious contract_ids
suspicious = ['354340', '10', '9.2.1']
for cid in suspicious:
    if cid in ledger_contract_ids:
        errors.append(f"suspicious contract_id in coverage_ledger: {cid}")

# Check atomic_links inherit group relationship
link_groups = {}
for i, link in enumerate(d['links']):
    for mid in link['matrix_ids']:
        for cid in link['contract_ids']:
            key = (mid, cid)
            link_groups[key] = link['relationship']

for al in d['atomic_links']:
    key = (al['matrix_id'], al['contract_id'])
    if key in link_groups:
        expected_rel = link_groups[key]
        if al['relationship'] != expected_rel:
            errors.append(f"atomic_link ({al['matrix_id']},{al['contract_id']}) relationship={al['relationship']} but group has {expected_rel}")

print(json.dumps({"errors": errors, "count": len(errors)}, ensure_ascii=False, indent=2))
