import json

with open('outputs/discrepancy_analysis.json') as f:
    analysis = json.load(f)

clc = analysis['coverage_ledger']['contract']

# All contract ids from links
linked_from_links = set()
for link in analysis['links']:
    for cid in link['contract_ids']:
        linked_from_links.add(cid)

# All contract ids from unmatched_contract
extra_from_uc = set(x['contract_id'] for x in analysis['unmatched_contract'])

# Check CLC 'linked' entries are in links
clc_linked = set(x['contract_id'] for x in clc if x['closure'] == 'linked')
not_found = clc_linked - linked_from_links
if not_found:
    print(f"CLC 'linked' NOT in links: {sorted(not_found)}")
else:
    print("All CLC 'linked' ids found in links")

# Check CLC 'extra_in_contract' entries are in unmatched_contract
clc_extra = set(x['contract_id'] for x in clc if x['closure'] == 'extra_in_contract')
not_found2 = clc_extra - extra_from_uc
if not_found2:
    print(f"CLC 'extra_in_contract' NOT in unmatched_contract: {sorted(not_found2)}")
else:
    print("All CLC 'extra_in_contract' ids found in unmatched_contract")

# Check unmatched_contract ids
extra_not_in_clc = extra_from_uc - clc_extra
if extra_not_in_clc:
    print(f"Unmatched_contract ids NOT in CLC 'extra_in_contract': {sorted(extra_not_in_clc)}")
else:
    print("All unmatched_contract ids in CLC as extra_in_contract")

# Check 'linked' from links not in CLC
links_not_in_clc_linked = linked_from_links - clc_linked
# Remove those that may be in CLC as extra also
if links_not_in_clc_linked:
    print(f"Link contract_ids NOT in CLC as 'linked': {sorted(links_not_in_clc_linked)}")
