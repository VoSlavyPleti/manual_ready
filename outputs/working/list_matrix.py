import json
with open('outputs/working/matrix_inventory.json', 'r') as f:
    matrix = json.load(f)
for m in matrix:
    if m.get('materiality') == 'material':
        print(f"{m['id']}: obj={m.get('object','')}, party={m.get('party','')}, roo={m.get('right_or_obligation','')}")
