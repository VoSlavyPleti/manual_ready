import json

with open('inputs/matrix.json', 'r') as f:
    matrix = json.load(f)

# Print all matrix numbers and their product/lot/regime filters for scoping
for m in matrix:
    n = m['number']
    prod = m.get('only_for_product', 'common')
    lot = m.get('only_for_lot', 'common')
    term = m.get('only_for_terminal', 'common')
    pm = m.get('payment_method', 'common')
    rt = m.get('required_type', '')
    print(f"{n} | prod={prod} | lot={lot} | term={term} | pm={pm} | req={rt}")
