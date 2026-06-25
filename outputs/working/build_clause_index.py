import json
import re

# Load matrix
with open('/inputs/matrix.json', 'r') as f:
    matrix = json.load(f)

# Load contract
with open('/inputs/contract.txt', 'r') as f:
    contract_text = f.read()

# Matrix clause index
matrix_clauses = []
for m in matrix:
    matrix_clauses.append({
        'id': m['number'],
        'source_type': 'matrix',
        'source_text': m.get('enriched_text', ''),
        'main_idea': m.get('main_idea', ''),
        'required_type': m.get('required_type', ''),
        'only_for_product': m.get('only_for_product', ''),
        'only_for_lot': m.get('only_for_lot', ''),
        'only_for_terminal': m.get('only_for_terminal', ''),
        'payment_method': m.get('payment_method', ''),
        'topics': m.get('topics', [])
    })

# Contract clause index - extract all numbered clauses and appendices
contract_clauses = []

# Parse contract sections by clause numbers
lines = contract_text.split('\n')
current_clause = None
current_text = []
clause_pattern = re.compile(r'^(\d+(?:\.\d+)*)\.?\s')

# Also capture appendix headers
appendix_pattern = re.compile(r'^(Приложение\s+№\s*\S+)', re.IGNORECASE)

for line in lines:
    m_clause = clause_pattern.match(line.strip())
    m_appendix = appendix_pattern.match(line.strip())
    
    if m_clause:
        # Save previous clause
        if current_clause is not None and current_text:
            contract_clauses.append({
                'id': current_clause,
                'source_type': 'contract',
                'source_text': ' '.join(current_text).strip()
            })
        current_clause = m_clause.group(1)
        current_text = [line.strip()]
    elif m_appendix:
        if current_clause is not None and current_text:
            contract_clauses.append({
                'id': current_clause,
                'source_type': 'contract',
                'source_text': ' '.join(current_text).strip()
            })
        current_clause = m_appendix.group(1)
        current_text = [line.strip()]
    elif current_clause is not None:
        current_text.append(line.strip())

# Save last clause
if current_clause is not None and current_text:
    contract_clauses.append({
        'id': current_clause,
        'source_type': 'contract',
        'source_text': ' '.join(current_text).strip()
    })

# Merge multi-line clauses with same ID
merged_contract = {}
for c in contract_clauses:
    cid = c['id']
    if cid in merged_contract:
        merged_contract[cid]['source_text'] += ' ' + c['source_text']
    else:
        merged_contract[cid] = c

contract_clauses = list(merged_contract.values())

# Build final index
clause_index = {
    'matrix': matrix_clauses,
    'contract': contract_clauses
}

with open('/outputs/working/clause_index.json', 'w') as f:
    json.dump(clause_index, f, ensure_ascii=False, indent=2)

print(f"Matrix clauses: {len(matrix_clauses)}")
print(f"Contract clauses: {len(contract_clauses)}")
print("Contract clause IDs:")
for c in contract_clauses:
    print(f"  {c['id']}: {c['source_text'][:100]}...")
