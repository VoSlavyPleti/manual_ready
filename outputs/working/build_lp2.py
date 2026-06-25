import json
import re

with open('inputs/matrix.json', 'r', encoding='utf-8') as f:
    matrix = json.load(f)

with open('inputs/contract.txt', 'r', encoding='utf-8') as f:
    contract_text = f.read()

# ===== MATRIX PROPOSITIONS =====
matrix_props = []
for m in matrix:
    enriched = m.get('enriched_text', '')
    main_idea = m.get('main_idea', '')
    topics = m.get('topics', [])
    
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
    if 'Банк имеет право' in enriched or 'Банк вправе' in enriched:
        protected_party = 'Bank'
        bound_party = 'Merchant'
    elif 'Банк обязуется' in enriched:
        protected_party = 'Merchant'
        bound_party = 'Bank'
    elif 'Предприятие имеет право' in enriched or 'Предприятие вправе' in enriched:
        protected_party = 'Merchant'
        bound_party = 'Bank'
    elif 'Предприятие обязуется' in enriched:
        protected_party = 'Bank'
        bound_party = 'Merchant'
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
    
    legal_object = topics[0] if topics else ''
    
    # Extract deadline
    deadline = ''
    dm = re.search(r'в течение\s+([^.]*?(?:дней|дня|часов|месяц)[^.]*?)(?:\.|,)', enriched)
    if dm:
        deadline = dm.group(1).strip()
    
    # Extract amount
    amount_formula_cap = ''
    if 'рубл' in enriched.lower():
        amount_formula_cap = 'monetary_amount_present'
    if 'штраф' in enriched.lower() or 'неустойк' in enriched.lower() or 'пеня' in enriched.lower():
        amount_formula_cap = 'penalty_present'
    
    # Extract liability
    liability_remedy = ''
    if 'штраф' in enriched.lower():
        liability_remedy = 'fine'
    if 'неустойк' in enriched.lower() or 'пеня' in enriched.lower():
        liability_remedy = 'penalty'
    if 'возместить' in enriched.lower() or 'возмещени' in enriched.lower():
        liability_remedy = 'indemnification'
    if 'не несет ответственности' in enriched:
        liability_remedy = 'exemption'
    
    # Extract procedure/channel
    procedure_channel = ''
    if 'электронн' in enriched.lower() or 'email' in enriched.lower() or 'почт' in enriched.lower():
        procedure_channel = 'electronic/email'
    if 'ЕИС' in enriched:
        procedure_channel = 'EIS'
    if 'ДБО' in enriched:
        procedure_channel = 'DBO'
    
    # Extract consequence
    consequence = ''
    if 'расторжени' in enriched.lower():
        consequence = 'termination'
    if 'приостанов' in enriched.lower():
        consequence = 'suspension'
    
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
        'trigger': '',
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

# ===== CONTRACT PROPOSITIONS =====
# Parse contract into clauses with proper IDs
lines = contract_text.split('\n')
contract_clauses_raw = []
current_id = None
current_text = []
clause_pattern = re.compile(r'^(\d+(?:\.\d+)*)\.?\s')

for line in lines:
    stripped = line.strip()
    if not stripped:
        continue
    m = clause_pattern.match(stripped)
    if m:
        if current_id is not None and current_text:
            contract_clauses_raw.append((current_id, ' '.join(current_text)))
        current_id = m.group(1)
        current_text = [stripped]
    elif current_id is not None:
        current_text.append(stripped)

if current_id is not None and current_text:
    contract_clauses_raw.append((current_id, ' '.join(current_text)))

# Merge same IDs
merged = {}
for cid, txt in contract_clauses_raw:
    if cid in merged:
        merged[cid] += ' ' + txt
    else:
        merged[cid] = txt

# Also add appendix entries
appendix_entries = [
    ('Приложение №1', 'Техническое задание - описание объекта закупки, адреса ТСТ, перечень карт, условия оказания услуг'),
    ('Приложение №1.1', 'Заявление Предприятия на проведение расчетов - сведения о предприятии, информация об услугах'),
    ('Приложение №1..2', 'Информация о ТСТ/Ресурсе Предприятия - адреса, контактные данные, типы терминалов'),
    ('Приложение №2', 'Спецификация - наименование услуг, цена за единицу, максимальное значение цены контракта'),
]

contract_props = []
for cid, txt in merged.items():
    # Determine type
    if re.match(r'^\d+$', cid) and not re.search(r'\d+\.\d+', cid):
        ptype = 'heading'
    elif re.match(r'^\d+\.\d+\.\d+', cid):
        ptype = 'operative'
    elif re.match(r'^\d+\.\d+$', cid):
        ptype = 'operative'
    else:
        ptype = 'operative'
    
    # Determine materiality
    if ptype == 'heading':
        materiality = 'heading'
    elif len(txt) < 20:
        materiality = 'not_material'
    else:
        materiality = 'evaluable'
    
    # Extract party info
    protected_party = ''
    bound_party = ''
    if 'Исполнитель обязуется' in txt or 'Исполнитель вправе' in txt:
        if 'обязуется' in txt:
            protected_party = 'Customer'
            bound_party = 'Bank'
        else:
            protected_party = 'Bank'
            bound_party = 'Customer'
    elif 'Заказчик обязуется' in txt or 'Заказчик вправе' in txt:
        if 'обязуется' in txt:
            protected_party = 'Bank'
            bound_party = 'Customer'
        else:
            protected_party = 'Customer'
            bound_party = 'Bank'
    elif 'Стороны' in txt:
        protected_party = 'Both'
        bound_party = 'Both'
    
    # Extract right/obligation
    if 'вправе' in txt or 'имеет право' in txt:
        right_or_obligation = 'right'
    elif 'обязуется' in txt or 'обязан' in txt:
        right_or_obligation = 'obligation'
    elif 'не несет' in txt:
        right_or_obligation = 'exemption'
    else:
        right_or_obligation = 'provision'
    
    # Extract deadline
    deadline = ''
    dm = re.search(r'в течение\s+([^.]*?(?:дней|дня|часов|месяц)[^.]*?)(?:\.|,)', txt)
    if dm:
        deadline = dm.group(1).strip()
    dm2 = re.search(r'не позднее\s+([^.]*?(?:дней|дня|часов|месяц)[^.]*?)(?:\.|,)', txt)
    if dm2:
        deadline = dm2.group(1).strip()
    
    # Extract amount
    amount_formula_cap = ''
    if 'рубл' in txt.lower():
        amount_formula_cap = 'monetary_amount_present'
    if 'штраф' in txt.lower() or 'неустойк' in txt.lower() or 'пеня' in txt.lower():
        amount_formula_cap = 'penalty_present'
    
    # Extract liability
    liability_remedy = ''
    if 'штраф' in txt.lower():
        liability_remedy = 'fine'
    if 'неустойк' in txt.lower() or 'пеня' in txt.lower():
        liability_remedy = 'penalty'
    if 'возместить' in txt.lower() or 'возмещени' in txt.lower():
        liability_remedy = 'indemnification'
    
    # Extract procedure
    procedure_channel = ''
    if 'ЕИС' in txt or 'единой информационной системе' in txt.lower():
        procedure_channel = 'EIS'
    if 'электронн' in txt.lower() or 'email' in txt.lower():
        procedure_channel = 'electronic'
    
    contract_props.append({
        'id': cid,
        'source_text': txt[:1000],
        'source_excerpt': txt[:300],
        'type': ptype,
        'materiality': materiality,
        'protected_party': protected_party,
        'bound_party': bound_party,
        'right_or_obligation': right_or_obligation,
        'legal_object': '',
        'trigger': '',
        'deadline': deadline,
        'amount_formula_cap': amount_formula_cap,
        'procedure_channel': procedure_channel,
        'liability_remedy': liability_remedy,
        'scope_options': [],
        'consequence': ''
    })

# Add appendix entries
for aid, atxt in appendix_entries:
    contract_props.append({
        'id': aid,
        'source_text': atxt,
        'source_excerpt': atxt,
        'type': 'appendix',
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
print(f"Contract IDs: {[c['id'] for c in contract_props]}")
