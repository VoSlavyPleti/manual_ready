import json

with open('inputs/matrix.json') as f:
    matrix = json.load(f)

for m in matrix:
    print(f"{m['number']}: product={m['only_for_product']}, lot={m['only_for_lot']}, terminal={m['only_for_terminal']}, pm={m['payment_method']}, req={m['required_type']}")
