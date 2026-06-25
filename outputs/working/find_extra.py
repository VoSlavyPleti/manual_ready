import json

with open('outputs/working/matrix_inventory.json', 'r') as f:
    matrix = json.load(f)
with open('outputs/working/contract_inventory.json', 'r') as f:
    contract = json.load(f)

# Build matrix coverage map by legal object + party + right/obligation
matrix_coverage = {}
for m in matrix:
    if m.get('materiality') == 'material':
        obj = m.get('object','')
        party = m.get('party','')
        roo = m.get('right_or_obligation','')
        key = (obj, party, roo)
        matrix_coverage.setdefault(key, []).append(m['id'])

# Contract material items
contract_material = [c for c in contract if c.get('materiality') == 'material']

print("=== Matrix coverage keys ===")
for k in sorted(matrix_coverage.keys()):
    print(f"  {k}: {matrix_coverage[k]}")

print("\n=== Contract material items ===")
for c in contract_material:
    cid = c['id']
    obj = c.get('object','')
    party = c.get('party','')
    roo = c.get('right_or_obligation','')
    key = (obj, party, roo)
    matrix_hits = matrix_coverage.get(key, [])
    # Also check with empty object (framework clauses)
    matrix_hits_any = []
    for mk, mv in matrix_coverage.items():
        if mk[1] == party and mk[2] == roo:
            matrix_hits_any.extend(mv)
    
    has_analogue = len(matrix_hits) > 0
    print(f"  {cid}: key={key}, matrix_hits={matrix_hits[:3]}, has_analogue={has_analogue}")
