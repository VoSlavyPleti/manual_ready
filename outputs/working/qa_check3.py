#!/usr/bin/env python3
import json, os

_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "discrepancy_analysis.json")
_json_path = os.path.normpath(_json_path)
with open(_json_path, "r", encoding="utf-8") as f:
    d = json.load(f)

print("=== Mandatory missing with low risk ===")
for um in d['unmatched_matrix']:
    if um.get('required_type') == 'mandatory' and um.get('risk_level') == 'low':
        print(f"  {um['matrix_id']}: {um.get('risk','')[:120]}")

print("\n=== Optional missing with high risk ===")
for um in d['unmatched_matrix']:
    if um.get('required_type') == 'optional' and um.get('risk_level') == 'high':
        print(f"  {um['matrix_id']}: {um.get('risk','')[:120]}")

print("\n=== unmatched_matrix items with generic risk text ===")
for um in d['unmatched_matrix']:
    risk = um.get('risk','')
    if 'No confirmed contract analogue was present in completed fragments' in risk:
        print(f"  {um['matrix_id']}: GENERIC RISK TEXT")

print("\n=== Check for matrix ids in unmatched_matrix that are out_of_scope ===")
out_of_scope_ids = set()
for r in d['coverage_ledger']['matrix']:
    if r['closure'] in ('out_of_scope', 'not_applicable'):
        out_of_scope_ids.add(r['matrix_id'])
for um in d['unmatched_matrix']:
    if um['matrix_id'] in out_of_scope_ids:
        print(f"  ERROR: {um['matrix_id']} is out_of_scope but in unmatched_matrix")

print("\n=== Check for not_material contract ids in unmatched_contract ===")
not_material_ids = set()
for r in d['coverage_ledger']['contract']:
    if r['closure'] == 'not_material':
        not_material_ids.add(r['contract_id'])
for uc in d['unmatched_contract']:
    if uc['contract_id'] in not_material_ids:
        print(f"  ERROR: {uc['contract_id']} is not_material but in unmatched_contract")

print("\nDone.")
