#!/usr/bin/env python3
"""Mechanical cross-reference: identify contract material items with no matrix analogue."""
import json

with open('/outputs/working/matrix_inventory.json', 'r') as f:
    matrix = json.load(f)
with open('/outputs/working/contract_inventory.json', 'r') as f:
    contract = json.load(f)

# Build matrix id set
matrix_ids = set(item['id'] for item in matrix)

# Build matrix propositions index for analogue testing
# Key: legal object + protected party + operative right/duty
matrix_index = {}
for item in matrix:
    if item.get('materiality') == 'material':
        key = (item.get('object',''), item.get('party',''), item.get('right_or_obligation',''))
        matrix_index.setdefault(key, []).append(item)

# Contract material items
contract_material = [item for item in contract if item.get('materiality') == 'material']

# For each contract material item, check if there's a matrix analogue
# We need to look at the legal proposition, not just id matching
# The matrix uses different numbering than the contract

# Print all contract material items with their propositions for manual review
print("=== CONTRACT MATERIAL ITEMS ===")
for item in contract_material:
    cid = item['id']
    prop = item.get('proposition','')[:200]
    obj = item.get('object','')
    party = item.get('party','')
    roo = item.get('right_or_obligation','')
    print(f"ID: {cid}")
    print(f"  Object: {obj}")
    print(f"  Party: {party}")
    print(f"  Right/Obligation: {roo}")
    print(f"  Proposition: {prop}")
    print()

# Also print all matrix material items for cross-reference
print("\n=== MATRIX MATERIAL ITEMS (summary) ===")
for item in matrix:
    if item.get('materiality') == 'material':
        print(f"  {item['id']}: obj={item.get('object','')}, party={item.get('party','')}, roo={item.get('right_or_obligation','')}")
