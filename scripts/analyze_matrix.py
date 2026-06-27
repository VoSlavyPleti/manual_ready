import json

with open('inputs/matrix.json') as f:
    matrix = json.load(f)

matrix_ids = sorted(set(item['number'] for item in matrix))
print(f'Total matrix IDs: {len(matrix_ids)}')

sections = {}
for item in matrix:
    sec = item['number'].split('.')[0]
    sections.setdefault(sec, []).append(item['number'])
for s in sorted(sections):
    print(f'  Section {s}: {len(sections[s])} items')

print('\n--- Filtered items ---')
for item in matrix:
    filters = []
    op = item.get('only_for_product', 'common')
    ol = item.get('only_for_lot', 'common')
    ot = item.get('only_for_terminal', 'common')
    if op != 'common':
        filters.append(f'product={op}')
    if ol != 'common':
        filters.append(f'lot={ol}')
    if ot != 'common':
        filters.append(f'terminal={ot}')
    if filters:
        print(f'  {item["number"]}: req={item["required_type"]} {" ".join(filters)}')
