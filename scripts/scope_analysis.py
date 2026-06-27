import json

with open('inputs/matrix.json', 'r') as f:
    matrix = json.load(f)

# Categorize matrix items
out_of_scope = []
applicable = []

for m in matrix:
    n = m['number']
    prod = m.get('only_for_product', 'common')
    lot = m.get('only_for_lot', 'common')
    term = m.get('only_for_terminal', 'common')
    pm = m.get('payment_method', 'common')
    
    # Determine applicability for this contract:
    # Contract profile: trade_acquiring, 44-FZ, common/pos/smart terminals, card payments + optional QR
    
    is_applicable = True
    reason = ""
    
    # Product scope: internet_acquiring items not applicable
    if prod == 'internet_acquiring':
        is_applicable = False
        reason = "internet_acquiring not in contract scope"
    # Payment method: SberPay FaceScan not in contract
    elif pm == 'sber_pay_face_scan':
        is_applicable = False
        reason = "SberPay FaceScan/biometric payment not in contract scope"
    # 223-FZ specific
    elif lot == 'fz_223':
        is_applicable = False
        reason = "223-FZ regime not applicable; contract under 44-FZ"
    
    if is_applicable:
        applicable.append(n)
    else:
        out_of_scope.append((n, reason))

print("=== OUT OF SCOPE / NOT APPLICABLE ===")
for n, r in out_of_scope:
    print(f"  {n}: {r}")

print(f"\nTotal out of scope: {len(out_of_scope)}")
print(f"Total applicable: {len(applicable)}")
print(f"Total matrix items: {len(matrix)}")
