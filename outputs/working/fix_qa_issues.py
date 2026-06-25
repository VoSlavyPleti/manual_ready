import json

with open('/outputs/discrepancy_analysis.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# E01: Remove invented locator '354340' from coverage_ledger.contract
cl = data['coverage_ledger']['contract']
before = len(cl)
data['coverage_ledger']['contract'] = [c for c in cl if c.get('contract_id') != '354340']
print(f"E01: Removed {before - len(data['coverage_ledger']['contract'])} rows with contract_id=354340")

# E02: Fix 6 unmatched_matrix items with placeholder risk text
placeholder = 'No confirmed contract analogue was present in completed fragments.'
fixed_count = 0
risks = {
    '2.6.1.1': 'Отсутствие автоматического подключения QR-кода на смарт-терминалах создает риск задержки активации сервиса и дополнительных процедур согласования.',
    '2.6.3.1': 'Отсутствие автоматического подключения QR-кода при установке терминала Банка создает риск задержки активации QR-функционала.',
    '4.2.22': 'Отсутствие обязанности Предприятия предоставлять QR-код покупателям снижает контроль Банка над использованием QR-сервиса.',
    '5.1.3': 'Отсутствие права Банка на одностороннее изменение документов с уведомлением за 1 день ограничивает оперативность Банка в обновлении условий.',
    '5.2.9': 'Отсутствие права Банка приостанавливать авторизацию при отсутствии операций в течение 30 дней ограничивает контроль Банка над неактивными ТСТ.',
    '6.20': 'Отсутствие положения о неуменьшении суммы возмещения Предприятием ограничивает защиту Банка от зачетов и удержаний.'
}
for item in data['unmatched_matrix']:
    if item.get('risk') == placeholder:
        mid = item['matrix_id']
        if mid in risks:
            item['risk'] = risks[mid]
            fixed_count += 1
print(f"E02: Fixed {fixed_count} placeholder risk texts")

# E03: Fix risk miscalibration - mandatory missing should be high risk
mandatory_low = ['2.6.2.1', '2.6.2.2', '2.6.3.2', '4.2.8', '5.1.4', '6.7', '6.8', '6.10', '6.11', '6.13', '6.14', '6.16', '6.17', '7.14', '7.17', '10.3']
recalibrated = 0
for item in data['unmatched_matrix']:
    if item['matrix_id'] in mandatory_low and item.get('risk_level') == 'low':
        item['risk_level'] = 'high'
        recalibrated += 1
print(f"E03: Recalibrated {recalibrated} mandatory missing items from low to high risk")

# E07: Check link for 5.1.10
for link in data['links']:
    if '5.1.10' in link.get('matrix_ids', []):
        if link.get('risk_level') == 'low':
            link['risk_level'] = 'medium'
            print('E07: Upgraded 5.1.10 link risk from low to medium')

# E08: Check link for 11.12
for link in data['links']:
    if '11.12' in link.get('matrix_ids', []):
        if link.get('risk_level') == 'low':
            link['risk_level'] = 'medium'
            print('E08: Upgraded 11.12 link risk from low to medium')

# Remove finalizer note
if 'finalizer' in data.get('analysis_profile', {}):
    del data['analysis_profile']['finalizer']
    print('Removed finalizer note')

# Recalculate summary
data['summary']['aligned_count'] = sum(1 for l in data['links'] if l['relationship'] == 'aligned')
data['summary']['deviation_count'] = sum(1 for l in data['links'] if l['relationship'] == 'deviation')
data['summary']['missing_in_contract_count'] = len(data['unmatched_matrix'])
data['summary']['extra_in_contract_count'] = len(data['unmatched_contract'])
print(f"Summary recalculated: {data['summary']}")

with open('/outputs/discrepancy_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Done - all fixes applied')
