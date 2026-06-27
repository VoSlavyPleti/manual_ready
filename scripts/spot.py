import json
with open('outputs/discrepancy_analysis.json') as f:
    d = json.load(f)
    
check_ids = ['2.1', '2.2', '2.3.6', '6.1', '10.2', '5.1.8.1', '2.5.2.1']
for mid in check_ids:
    found = False
    for link in d['links']:
        if mid in link['matrix_ids']:
            print(f"{mid}: {link['relationship']} -> {link['contract_ids']}")
            found = True
            break
    if not found:
        for um in d['unmatched_matrix']:
            if um['matrix_id'] == mid:
                print(f"{mid}: missing_in_contract")
                found = True
                break
    if not found:
        for clm in d['coverage_ledger']['matrix']:
            if clm['matrix_id'] == mid:
                print(f"{mid}: CLM closure={clm['closure']}")
                found = True
                break
