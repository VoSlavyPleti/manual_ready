import json, re

with open('inputs/contract.txt') as f:
    contract = f.read()
with open('outputs/discrepancy_analysis.json') as f:
    analysis = json.load(f)

clc = analysis['coverage_ledger']['contract']
clc_ids = set(x['contract_id'] for x in clc)

# All linked contract ids
all_linked_contract = set()
for link in analysis['links']:
    for cid in link['contract_ids']:
        all_linked_contract.add(cid)

# All extra contract ids
all_extra_contract = set(x['contract_id'] for x in analysis['unmatched_contract'])

# All not_material contract ids
all_nm_contract = set(x['contract_id'] for x in clc if x['closure'] == 'not_material')

print(f"Linked contract IDs: {len(all_linked_contract)}")
print(f"Extra contract IDs: {len(all_extra_contract)}")
print(f"Not material contract IDs: {len(all_nm_contract)}")
print(f"Total unique contract IDs in CLC: {len(clc_ids)}")

# Verify: every linked contract id is in CLC as 'linked'
for cid in all_linked_contract:
    entries = [x for x in clc if x['contract_id'] == cid]
    if not entries:
        print(f"  MISSING from CLC: {cid}")
    elif entries[0]['closure'] != 'linked':
        print(f"  WRONG closure for {cid}: {entries[0]['closure']}")

# Verify: every extra contract id is in CLC as 'extra_in_contract'
for cid in all_extra_contract:
    entries = [x for x in clc if x['contract_id'] == cid]
    if not entries:
        print(f"  EXTRA missing from CLC: {cid}")
    elif entries[0]['closure'] != 'extra_in_contract':
        print(f"  EXTRA wrong closure for {cid}: {entries[0]['closure']}")

# Check for duplicates in CLC
from collections import Counter
clc_counter = Counter(x['contract_id'] for x in clc)
clc_dupes = {k: v for k, v in clc_counter.items() if v > 1}
if clc_dupes:
    print(f"DUPLICATE contract IDs in CLC: {clc_dupes}")
    for cid in clc_dupes:
        entries = [x for x in clc if x['contract_id'] == cid]
        for e in entries:
            print(f"  {e}")

# Check if any contract ids appear in both linked and extra
both = all_linked_contract & all_extra_contract
if both:
    print(f"Contract IDs in BOTH linked and extra: {both}")

# Verify contract ids exist in contract text (spot check)
for cid in list(all_linked_contract)[:5]:
    # Extract the clause number for search
    search = cid.split('(')[0].strip()
    if search in contract:
        print(f"  OK: '{search}' found in contract")
    else:
        print(f"  WARNING: '{search}' NOT found in contract")
