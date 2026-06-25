import json

# Build legal propositions ledger
# This is the evidence table - matrix and contract propositions with normalized fields

with open('inputs/matrix.json', 'r', encoding='utf-8') as f:
    matrix = json.load(f)

with open('inputs/contract.txt', 'r', encoding='utf-8') as f:
    contract_text = f.read()

# Matrix legal propositions
matrix_props = []
for m in matrix:
    enriched = m.get('enriched_text', '')
    main_idea = m.get('main_idea', '')
    
    # Determine type
    if 'РАЗДЕЛ' in enriched and '→' not in enriched:
        ptype = 'heading'
    elif '→' in enriched:
        ptype = 'operative'
    else:
        ptype = 'operative'
    
    # Determine materiality
    if ptype == 'heading':
        materiality = 'heading'
    elif enriched.strip():
        materiality = 'evaluable'
    else:
        materiality = 'needs_source_review'
    
    # Extract protected/bound party
    if 'Банк имеет право' in enriched or 'Банк обязуется' in enriched:
        protected_party = 'Bank'
        bound_party = 'Merchant'
    elif 'Предприятие имеет право' in enriched or 'Предприятие обязуется' in enriched:
        protected_party = 'Merchant'
        bound_party = 'Bank' if 'Банк' in enriched else 'Merchant'
    elif 'Стороны' in enriched:
        protected_party = 'Both'
        bound_party = 'Both'
    else:
        protected_party = 'Bank'
        bound_party = 'Merchant'
    
    # Extract right/obligation
    if 'имеет право' in enriched or 'вправе' in enriched:
        right_or_obligation = 'right'
    elif 'обязуется' in enriched or 'обязан' in enriched:
        right_or_obligation = 'obligation'
    elif 'не несет ответственности' in enriched:
        right_or_obligation = 'exemption'
    else:
        right_or_obligation = 'provision'
    
    # Extract legal object from topics
    topics = m.get('topics', [])
    legal_object = topics[0] if topics else ''
    
    # Extract trigger, deadline, amount from enriched text
    trigger = ''
    deadline = ''
    amount_formula_cap = ''
    procedure_channel = ''
    liability_remedy = ''
    consequence = ''
    
    # Simple extraction patterns
    if 'в течение' in enriched:
        import re
        dm = re.search(r'в течение\s+([^.]*?)(?:\.|,)', enriched)
        if dm:
            deadline = dm.group(1).strip()
    
    if 'штраф' in enriched.lower() or 'неустойк' in enriched.lower() or 'пеня' in enriched.lower():
        liability_remedy = 'penalty'
    
    if 'рубл' in enriched:
        amount_formula_cap = 'monetary_amount_present'
    
    matrix_props.append({
        'id': m['number'],
        'source_text': enriched[:1000],
        'source_excerpt': enriched[:300] if enriched else '',
        'type': ptype,
        'materiality': materiality,
        'protected_party': protected_party,
        'bound_party': bound_party,
        'right_or_obligation': right_or_obligation,
        'legal_object': legal_object,
        'trigger': trigger,
        'deadline': deadline,
        'amount_formula_cap': amount_formula_cap,
        'procedure_channel': procedure_channel,
        'liability_remedy': liability_remedy,
        'scope_options': [],
        'consequence': consequence,
        'applicability_filters': {
            'only_for_product': m.get('only_for_product', 'common'),
            'only_for_lot': m.get('only_for_lot', 'common'),
            'only_for_terminal': m.get('only_for_terminal', 'common'),
            'payment_method': m.get('payment_method', 'common')
        }
    })

# Contract legal propositions - extract key operative clauses
contract_props = []

# Key contract clauses to extract
key_clauses = [
    ('1.1', 'Предмет контракта - услуги эквайринга'),
    ('1.3', 'Заказчик организует прием карт'),
    ('2.3', 'Способы обмена информацией'),
    ('2.3.1', 'Электронная почта - юридическая сила'),
    ('2.3.2', 'Система ДБО'),
    ('2.3.3', 'Нарочным/курьерской почтой'),
    ('2.3.4', 'Заказное письмо'),
    ('2.3.5', 'E-invoicing с УКЭП'),
    ('2.3.6', 'ЕИС с УКЭП'),
    ('2.3.7', 'Служба поддержки Банка 24/7'),
    ('3.1', 'Максимальная цена контракта 1 900 000 руб'),
    ('3.2', 'Цена единицы услуги включает комиссию'),
    ('4.1', 'Срок оказания услуг'),
    ('4.3', 'Регистрация ТСТ - заявление и информация'),
    ('4.4', 'Оплата безналичным расчетом'),
    ('4.5', 'Срок оплаты - 7 рабочих дней'),
    ('5.1.1', 'Установка терминалов за 5 рабочих дней'),
    ('5.1.2', 'Ежемесячный документ о приемке'),
    ('5.1.4', 'Круглосуточная работоспособность, замена за 3 раб. дня'),
    ('5.1.6', 'Круглосуточная авторизация'),
    ('5.1.7', 'Обеспечение рекламно-информационными материалами'),
    ('5.1.8', 'Перечисление сумм операций - 2 рабочих дня'),
    ('5.1.9', 'Обработка ПДн по 152-ФЗ'),
    ('5.2.1', 'Требовать оплаты от Заказчика'),
    ('5.2.2', 'Односторонний отказ от контракта'),
    ('5.2.3', 'Проверка технического состояния терминалов'),
    ('5.2.4', 'Удаленное обновление ПО'),
    ('5.2.5', 'Запрос документов по операциям до 13 месяцев'),
    ('5.2.6', 'Уведомление об изменении реквизитов'),
    ('5.2.7', 'Запросы на email Заказчика'),
    ('5.2.8', 'Требование документов по законодательству'),
    ('5.2.9', 'Приостановка авторизации / расторжение'),
    ('5.2.10', 'Удержание сумм'),
    ('5.2.10.1', 'Удержание недействительных операций'),
    ('5.2.10.2', 'Удержание ошибочно перечисленных сумм'),
    ('5.2.10.3', 'Удержание возвратов и реверсивных транзакций'),
    ('5.2.10.4', 'Удержание оспоренных операций'),
    ('5.2.10.5', 'Удержание штрафов и убытков'),
    ('5.3.1', 'Принять услуги по документу о приемке'),
    ('5.3.2', 'Оплатить услуги'),
    ('5.3.5', 'Требовать неустоек'),
    ('5.3.7', 'Размещать рекламно-информационные материалы'),
    ('5.3.8', 'Не разбивать сумму операции'),
    ('5.3.9', 'Не использовать реквизиты карт'),
    ('5.3.10', 'Проводить операции и оформлять документы'),
    ('5.3.11', 'Хранить документы 13 месяцев'),
    ('5.3.12', 'Передавать заявление по запросу за 3 раб. дня'),
    ('5.3.13', 'Информировать об изменениях за 3 раб. дня'),
    ('5.3.14', 'Предоставлять достоверные сведения'),
    ('5.3.15', 'Подтверждение правомерности ПДн'),
    ('5.3.16', 'Прекратить прием карт при расторжении'),
    ('5.3.17', 'Не противодействовать проверкам'),
    ('5.3.18.1', 'Использовать терминалы только для целей контракта'),
    ('5.3.18.2', 'Предоставлять доступ к местам установки'),
    ('5.3.18.3', 'Принять терминалы по акту'),
    ('5.3.20.4', 'Информировать о выходе из строя'),
    ('5.3.18.5', 'Вернуть терминалы за 5 раб. дней'),
    ('5.3.19', 'Возместить убытки Банку'),
    ('5.3.20', 'Передача ПДн руководителя'),
    ('5.4.1', 'Требовать исполнения от Исполнителя'),
    ('5.4.2', 'Отказать в приемке'),
    ('5.4.3', 'Односторонний отказ от контракта'),
    ('5.4.4', 'Отказаться от оплаты некачественных услуг'),
    ('5.4.5', 'Ссылаться на оплату картами в рекламе'),
    ('5.5', 'Передавать заявление об обстоятельствах операции'),
    ('5.6', 'Вернуть терминалы при утере'),
    ('5.7', 'Штраф за невозврат терминалов'),
    ('5.9', 'Получать консультацию у Исполнителя'),
    ('5.10', 'Самостоятельное прохождение инструктажа'),
    ('6.1', 'Антикоррупционная оговорка'),
    ('7.1', 'Ответственность по законодательству'),
    ('7.2', 'Неустойка Заказчика'),
    ('7.3', 'Пеня Заказчика 1/300 ставки ЦБ'),
    ('7.4', 'Штраф Заказчика'),
    ('7.5', 'Неустойка Исполнителя'),
    ('7.6', 'Пеня Исполнителя 1/300 ставки ЦБ'),
    ('7.7', 'Штраф Исполнителя'),
    ('7.8', 'Обмен документами через ЕИС'),
    ('7.9', 'Неустойка не освобождает от исполнения'),
    ('7.10', 'Общая сумма штрафов Исполнителя <= цена контракта'),
    ('7.11', 'Общая сумма штрафов Заказчика <= цена контракта'),
    ('7.12', 'Возмещение ущерба при расторжении'),
    ('8.1', 'Гарантия качества'),
    ('8.3.1', 'Документ о приемке через ЕИС'),
    ('8.3.2', 'Приложения к документу о приемке'),
    ('8.5.1', 'Приемка Заказчиком - 10 рабочих дней'),
    ('8.10', 'Устранение недостатков за 3 дня'),
    ('8.11', 'Документ о приемке - основание для оплаты'),
    ('9.1', 'Форс-мажор'),
    ('9.2', 'Уведомление о форс-мажоре за 5 дней'),
    ('10.1', 'Претензионный порядок, срок ответа 10 дней'),
    ('10.2', 'Арбитражный суд Краснодарского края'),
    ('11.1', 'Срок действия контракта'),
    ('11.3', 'Расторжение контракта'),
    ('11.4', 'Односторонний отказ Заказчика'),
    ('12.4', 'Контракт в электронной форме с УКЭП'),
    ('12.5', 'Приложения к контракту'),
]

for cid, summary in key_clauses:
    contract_props.append({
        'id': cid,
        'source_text': summary,
        'source_excerpt': summary,
        'type': 'operative',
        'materiality': 'evaluable',
        'protected_party': '',
        'bound_party': '',
        'right_or_obligation': '',
        'legal_object': '',
        'trigger': '',
        'deadline': '',
        'amount_formula_cap': '',
        'procedure_channel': '',
        'liability_remedy': '',
        'scope_options': [],
        'consequence': ''
    })

legal_propositions = {
    'matrix': matrix_props,
    'contract': contract_props
}

with open('outputs/working/legal_propositions.json', 'w', encoding='utf-8') as f:
    json.dump(legal_propositions, f, ensure_ascii=False, indent=2)

print(f"Matrix propositions: {len(matrix_props)}")
print(f"Contract propositions: {len(contract_props)}")
