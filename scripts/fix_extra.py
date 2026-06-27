import json

with open('outputs/discrepancy_analysis.json') as f:
    d = json.load(f)

# Fix 1: Move 4.1 from extra to link with 10.1
# Find the 10.1 link and add 4.1 to it
for link in d['links']:
    if '10.1' in link['matrix_ids']:
        if '4.1' not in link['contract_ids']:
            link['contract_ids'].append('4.1')
        print(f"Added 4.1 to link with matrix {link['matrix_ids']}")
        break

# Fix 2: Move 4.4 from extra - create deviation link with 5.1.13
# Remove from unmatched_contract
d['unmatched_contract'] = [uc for uc in d['unmatched_contract'] if uc['contract_id'] != '4.4 (абз.2)']
# Find existing 5.1.13 link and add 4.4
for link in d['links']:
    if '5.1.13' in link['matrix_ids']:
        if '4.4 (абз.2)' not in link['contract_ids']:
            link['contract_ids'].append('4.4 (абз.2)')
        # If link is aligned, change to deviation since contract changes notification method
        link['relationship'] = 'deviation'
        link['risk_level'] = 'low'
        link['status_reason'] = 'Matrix 5.1.13: Bank notifies via Official Site. Contract 4.4: Bank must notify in writing within 2 days. Deviation in notification channel but Bank obligation preserved.'
        link['discrepancies'] = [
            {"type": "procedure", "description": "Matrix: notification via Official Site. Contract: written notification in 2 working days.", "risk": "Different channel; risk is low as written notification is also effective. Additional obligation on Bank (2-day deadline) is beneficial."}
        ]
        print(f"Added 4.4 to 5.1.13 link, changed to deviation")
        break

# Fix 3: Move 5.1.2 from extra to link with 6.2
d['unmatched_contract'] = [uc for uc in d['unmatched_contract'] if uc['contract_id'] != '5.1.2']
for link in d['links']:
    if '6.2' in link['matrix_ids']:
        if '5.1.2' not in link['contract_ids']:
            link['contract_ids'].append('5.1.2')
        print(f"Added 5.1.2 to link with matrix {link['matrix_ids']}")
        break

# Fix 4: Move 5.2.2 from extra to link with 5.1.8.1
d['unmatched_contract'] = [uc for uc in d['unmatched_contract'] if uc['contract_id'] != '5.2.2']
for link in d['links']:
    if '5.1.8.1' in link['matrix_ids']:
        if '5.2.2' not in link['contract_ids']:
            link['contract_ids'].append('5.2.2')
        print(f"Added 5.2.2 to link with matrix {link['matrix_ids']}")
        break

# Fix 5: Move 5.3.5 from extra to link with 7.4
d['unmatched_contract'] = [uc for uc in d['unmatched_contract'] if uc['contract_id'] != '5.3.5']
for link in d['links']:
    if '7.4' in link['matrix_ids']:
        if '5.3.5' not in link['contract_ids']:
            link['contract_ids'].append('5.3.5')
        print(f"Added 5.3.5 to link with matrix {link['matrix_ids']}")
        break

# Update coverage_ledger.contract
clc = d['coverage_ledger']['contract']
# Remove extra entries for fixed items
clc = [x for x in clc if not (x['contract_id'] in ['4.4 (абз.2)', '5.1.2', '5.2.2', '5.3.5'] and x['closure'] == 'extra_in_contract')]
# Add/update linked entries
fixed_ids = {'4.1', '4.4 (абз.2)', '5.1.2', '5.2.2', '5.3.5'}
# Remove any existing entries for these in extra context
for cid in fixed_ids:
    # Remove old entries
    clc = [x for x in clc if not (x['contract_id'] == cid and x['closure'] == 'extra_in_contract')]
    # Add linked entry if not already present as linked
    if not any(x['contract_id'] == cid and x['closure'] == 'linked' for x in clc):
        clc.append({"contract_id": cid, "closure": "linked", "reason": "linked via deviation" if cid == '4.4 (абз.2)' else "linked via alignment"})
d['coverage_ledger']['contract'] = clc

# Update summary
d['summary']['extra_in_contract_count'] = len(d['unmatched_contract'])
aligned = sum(1 for l in d['links'] if l['relationship'] == 'aligned')
deviation = sum(1 for l in d['links'] if l['relationship'] == 'deviation')
d['summary']['aligned_count'] = aligned
d['summary']['deviation_count'] = deviation

print(f"Updated summary: aligned={aligned}, deviation={deviation}, missing={d['summary']['missing_in_contract_count']}, extra={d['summary']['extra_in_contract_count']}")

with open('outputs/discrepancy_analysis.json', 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("File rewritten")
