import json, os

with open('/outputs/discrepancy_analysis.json', 'r') as f:
    data = json.load(f)

print("=== NULL LINKS (relationship is None) ===")
for i, link in enumerate(data.get('links', [])):
    if link.get('relationship') is None:
        mids = link.get('matrix_ids', [])
        cids = link.get('contract_ids', [])
        print("  Link[%d]: matrix_ids=%s, contract_ids=%s" % (i, mids, cids))

print()
print("=== LINKS with link_index field ===")
for i, link in enumerate(data.get('links', [])):
    if 'link_index' in link:
        print("  Link[%d]: link_index=%s, matrix_ids=%s, status=%s" % (i, link['link_index'], link.get('matrix_ids', []), link.get('status', 'N/A')))

print()
print("=== ATOMIC LINKS sample (first 5) ===")
for i, al in enumerate(data.get('atomic_links', [])[:5]):
    print("  AL[%d]: matrix_id=%s, contract_id=%s, relationship=%s, link_index=%s, coverage_role=%s" % (i, al.get('matrix_id'), al.get('contract_id'), al.get('relationship'), al.get('link_index'), al.get('coverage_role')))

print()
print("=== ATOMIC LINKS validation ===")
al_errors = []
for i, al in enumerate(data.get('atomic_links', [])):
    if 'matrix_id' not in al:
        al_errors.append("AL[%d]: missing matrix_id" % i)
    if 'contract_id' not in al:
        al_errors.append("AL[%d]: missing contract_id" % i)
    if 'relationship' not in al:
        al_errors.append("AL[%d]: missing relationship" % i)
    if 'link_index' not in al:
        al_errors.append("AL[%d]: missing link_index" % i)
    if 'coverage_role' not in al:
        al_errors.append("AL[%d]: missing coverage_role" % i)
    if 'coverage' not in al:
        al_errors.append("AL[%d]: missing coverage" % i)
for e in al_errors[:20]:
    print("  " + e)
print("  Total atomic link errors: %d" % len(al_errors))

print()
print("=== COVERAGE LEDGER MATRIX: closures ===")
from collections import Counter
closures = Counter()
empty_link = []
for m in data.get('coverage_ledger', {}).get('matrix', []):
    closures[m['closure']] += 1
    if m['closure'] == 'linked' and not m.get('link_indices'):
        empty_link.append(m['matrix_id'])
print("  Closures: %s" % dict(closures))
print("  Linked with empty link_indices: %d" % len(empty_link))
if empty_link:
    print("  Sample: %s" % empty_link[:10])

print()
print("=== COVERAGE LEDGER CONTRACT: closures ===")
c_closures = Counter()
for c in data.get('coverage_ledger', {}).get('contract', []):
    c_closures[c['closure']] += 1
print("  Closures: %s" % dict(c_closures))

print()
print("=== UNMATCHED MATRIX check ===")
um_ids = [u['matrix_id'] for u in data.get('unmatched_matrix', [])]
print("  IDs: %s" % um_ids)

print()
print("=== UNMATCHED CONTRACT check ===")
uc_ids = [u['contract_id'] for u in data.get('unmatched_contract', [])]
print("  IDs: %s" % uc_ids)

print()
print("=== SUMMARY vs ACTUAL COUNTS ===")
summary = data.get('summary', {})
actual_aligned = sum(1 for l in data.get('links', []) if l.get('relationship') == 'aligned')
actual_deviation = sum(1 for l in data.get('links', []) if l.get('relationship') == 'deviation')
actual_missing = len(data.get('unmatched_matrix', []))
actual_extra = len(data.get('unmatched_contract', []))
print("  Summary: aligned=%s, deviation=%s, missing=%s, extra=%s" % (summary.get("aligned_count"), summary.get("deviation_count"), summary.get("missing_in_contract_count"), summary.get("extra_in_contract_count")))
print("  Actual:  aligned=%s, deviation=%s, missing=%s, extra=%s" % (actual_aligned, actual_deviation, actual_missing, actual_extra))

print()
print("=== OUT_OF_SCOPE/NOT_APPLICABLE in unmatched_matrix? ===")
for u in data.get('unmatched_matrix', []):
    if u.get('status') in ('out_of_scope', 'not_applicable'):
        print("  FOUND: %s has status=%s" % (u['matrix_id'], u['status']))

print()
print("=== OUT_OF_SCOPE in coverage_ledger also in unmatched_matrix? ===")
um_set = set(um_ids)
for m in data.get('coverage_ledger', {}).get('matrix', []):
    if m['closure'] in ('out_of_scope', 'not_applicable') and m['matrix_id'] in um_set:
        print("  LEAK: %s is %s but appears in unmatched_matrix" % (m['matrix_id'], m['closure']))

print()
print("=== MATRIX IDS NOT IN COVERAGE LEDGER ===")
cl_matrix_ids = set(m['matrix_id'] for m in data.get('coverage_ledger', {}).get('matrix', []))
link_matrix_ids = set()
for l in data.get('links', []):
    for mid in l.get('matrix_ids', []):
        link_matrix_ids.add(mid)
um_matrix_ids = set(um_ids)
all_matrix_ids = link_matrix_ids | um_matrix_ids
missing_from_cl = all_matrix_ids - cl_matrix_ids
print("  Matrix ids in links+unmatched but not in coverage_ledger: %s" % sorted(missing_from_cl))

cl_only = cl_matrix_ids - all_matrix_ids
print("  Matrix ids in coverage_ledger only (not in links or unmatched): %d" % len(cl_only))
if cl_only:
    print("  Sample: %s" % sorted(list(cl_only))[:20])

print()
print("=== DEVIATION WITHOUT RISK ===")
for l in data.get('links', []):
    if l.get('relationship') == 'deviation' and l.get('risk_level') == 'none':
        print("  %s: deviation with risk_level=none" % l.get('matrix_ids'))

print()
print("=== ALIGNED WITH DISCREPANCIES ===")
for l in data.get('links', []):
    if l.get('relationship') == 'aligned' and len(l.get('discrepancies', [])) > 0:
        print("  %s: aligned but has %d discrepancies" % (l.get('matrix_ids'), len(l.get('discrepancies', []))))

print()
print("=== DEVIATION WITH EMPTY DISCREPANCIES ===")
for l in data.get('links', []):
    if l.get('relationship') == 'deviation' and len(l.get('discrepancies', [])) == 0:
        print("  %s: deviation with empty discrepancies" % l.get('matrix_ids'))

print()
print("=== LINKS WITH EMPTY contract_ids BUT relationship set ===")
for l in data.get('links', []):
    if l.get('contract_ids') == [] and l.get('relationship') is not None:
        print("  %s: relationship=%s, contract_ids=[]" % (l.get('matrix_ids'), l.get('relationship')))

print()
print("=== PARENTHETICAL CONTRACT IDS ===")
all_contract_ids = set()
for l in data.get('links', []):
    for cid in l.get('contract_ids', []):
        all_contract_ids.add(cid)
for al in data.get('atomic_links', []):
    all_contract_ids.add(al.get('contract_id', ''))
for uc in data.get('unmatched_contract', []):
    all_contract_ids.add(uc.get('contract_id', ''))
all_contract_ids.discard('')
parenthetical = [cid for cid in all_contract_ids if '(' in cid or ')' in cid]
print("  Parenthetical ids: %s" % parenthetical)
print("  Total unique contract ids: %d" % len(all_contract_ids))
