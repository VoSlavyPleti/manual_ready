import json, sys

data = json.load(open('inputs/matrix.json', encoding='utf-8'))
batch_ids = ['5.1.8.5','5.1.8.6','5.1.8.7','5.1.8.8','5.1.8.9','5.1.8.10','5.1.8.11','5.1.8.12','5.1.8.13','5.1.9','5.1.10','5.1.11','5.1.12','5.1.13','5.1.14','5.1.15','5.1.16','5.1.17.1','5.1.17.2','5.2.1','5.2.2','5.2.3','5.2.4','5.2.5','5.2.6','5.2.7','5.2.8','5.2.9','5.2.10','5.2.12','6.1','6.2','6.3','6.4','6.5','6.6','6.7','6.8','6.9']
by_num = {d['number']: d for d in data}

out = []
for bid in batch_ids:
    d = by_num.get(bid)
    if d:
        out.append({
            'number': d['number'],
            'main_idea': d['main_idea'],
            'enriched_text': d['enriched_text'],
            'topics': d['topics'],
            'required_type': d['required_type'],
            'only_for_product': d['only_for_product'],
            'only_for_lot': d['only_for_lot'],
            'only_for_terminal': d['only_for_terminal'],
            'payment_method': d['payment_method']
        })
    else:
        out.append({'number': bid, 'NOT_FOUND': True})

json.dump(out, open('outputs/working/batch3_matrix_items.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"Extracted {len(out)} items")
