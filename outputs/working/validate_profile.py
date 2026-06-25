import json

# Load matrix and profile
with open('C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2/inputs/matrix.json', 'r', encoding='utf-8') as f:
    matrix = json.load(f)

with open('C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2/outputs/working/contract_product_profile.json', 'r', encoding='utf-8') as f:
    profile = json.load(f)

# Profile values
products = profile['product']  # ['trade_acquiring']
lots = profile['lot']  # 'fz_44'
terminals = profile['terminal']  # ['pos', 'smart']
payment_methods = profile['payment_method']  # ['cards', 'nfc', 'qr']
legal_regime = profile['legal_regime']  # '44_fz'

# Counters
applicable = []
not_applicable = []

for item in matrix:
    num = item['number']
    only_product = item.get('only_for_product', 'common')
    only_lot = item.get('only_for_lot', 'common')
    only_terminal = item.get('only_for_terminal', 'common')
    pay_method = item.get('payment_method', 'common')
    
    issues = []
    
    # Check product filter
    if only_product != 'common':
        if only_product not in products:
            issues.append(f'product: need {only_product}, have {products}')
    
    # Check lot filter
    if only_lot != 'common':
        if only_lot == 'fz_44' and legal_regime != '44_fz':
            issues.append(f'lot: need fz_44, have {legal_regime}')
        elif only_lot == 'fz_223' and legal_regime != '223_fz':
            issues.append(f'lot: need fz_223, have {legal_regime}')
        elif only_lot == 'commercial' and legal_regime not in ['commercial', 'common']:
            issues.append(f'lot: need commercial, have {legal_regime}')
    
    # Check terminal filter
    if only_terminal != 'common':
        if only_terminal == 'pos' and 'pos' not in terminals:
            issues.append(f'terminal: need pos, have {terminals}')
        elif only_terminal == 'smart' and 'smart' not in terminals:
            issues.append(f'terminal: need smart, have {terminals}')
    
    # Check payment method filter
    if pay_method != 'common':
        pm_map = {
            'qr': 'qr',
            'sber_pay': 'sber_pay',
            'sber_pay_face_scan': 'sber_pay_face_scan',
            'qr_sber_pay': 'qr_sber_pay'
        }
        needed = pm_map.get(pay_method, pay_method)
        if needed == 'qr' and 'qr' in payment_methods:
            pass  # applicable
        elif needed == 'sber_pay' and 'sber_pay' not in payment_methods:
            issues.append(f'payment_method: need sber_pay, have {payment_methods}')
        elif needed == 'sber_pay_face_scan' and 'sber_pay_face_scan' not in payment_methods:
            issues.append(f'payment_method: need sber_pay_face_scan, have {payment_methods}')
        elif needed == 'qr_sber_pay' and 'qr' in payment_methods:
            pass  # qr is present, sber_pay may not be
        elif needed not in payment_methods and needed != 'qr' and needed != 'qr_sber_pay':
            issues.append(f'payment_method: need {needed}, have {payment_methods}')
    
    if issues:
        not_applicable.append((num, issues))
    else:
        applicable.append(num)

print(f'Total matrix items: {len(matrix)}')
print(f'Applicable: {len(applicable)}')
print(f'Not applicable / Out of scope: {len(not_applicable)}')
print()
print('=== NOT APPLICABLE ITEMS ===')
for num, issues in not_applicable:
    print(f'{num}: {"; ".join(issues)}')
print()
print('=== APPLICABLE ITEMS ===')
for num in applicable:
    print(num)
