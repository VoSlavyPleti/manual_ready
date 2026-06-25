import json

data = json.load(open('inputs/matrix.json'))
batch_ids = ['5.1.8.5','5.1.8.6','5.1.8.7','5.1.8.8','5.1.8.9','5.1.8.10','5.1.8.11','5.1.8.12','5.1.8.13','5.1.9','5.1.10','5.1.11','5.1.12','5.1.13','5.1.14','5.1.15','5.1.16','5.1.17.1','5.1.17.2','5.2.1','5.2.2','5.2.3','5.2.4','5.2.5','5.2.6','5.2.7','5.2.8','5.2.9','5.2.10','5.2.12','6.1','6.2','6.3','6.4','6.5','6.6','6.7','6.8','6.9']
by_num = {d['number']: d for d in data}
for bid in batch_ids:
    d = by_num.get(bid)
    if d:
        print(f'=== {d["number"]} ===')
        print(f'main_idea: {d["main_idea"]}')
        print(f'enriched_text: {d["enriched_text"][:500]}')
        print(f'topics: {d["topics"]}')
        print(f'required_type: {d["required_type"]}')
        print(f'only_for_product: {d["only_for_product"]}')
        print(f'only_for_lot: {d["only_for_lot"]}')
        print(f'only_for_terminal: {d["only_for_terminal"]}')
        print(f'payment_method: {d["payment_method"]}')
        print()
    else:
        print(f'=== {bid} === NOT FOUND')
        print()
