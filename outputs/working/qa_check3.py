import json, os
from collections import Counter

with open('/outputs/discrepancy_analysis.json', 'r') as f:
    data = json.load(f)

links = data.get('links', [])
atomic_links = data.get('atomic_links', [])
unmatched_matrix = data.get('unmatched_matrix', [])
unmatched_contract = data.get('unmatched_contract', [])
coverage_ledger = data.get('coverage_ledger', {})
summary = data.get('summary', {})

errors = []
warnings = []

# ============================================================
# 1. Check for mixed link formats
# ============================================================
print("=" * 60)
print("1. LINK FORMAT ANALYSIS")
print("=" * 60)
group_format = []
batch_format = []
null_format = []
for i, link in enumerate(links):
    if 'relationship' in link and link['relationship'] is not None:
        group_format.append(i)
    elif 'link_index' in link:
        batch_format.append(i)
    else:
        null_format.append(i)

print("Group-format links (with relationship): %d" % len(group_format))
print("Batch-format links (with link_index): %d" % len(batch_format))
print("Null/empty links: %d" % len(null_format))

if batch_format:
    errors.append("BLOCKING: %d links use batch format (link_index/status) instead of group format (relationship). These must be merged into proper group-level links." % len(batch_format))
if null_format:
    errors.append("BLOCKING: %d links have null relationship and no link_index. These are empty placeholder entries." % len(null_format))

# ============================================================
# 2. Check for null/empty links (placeholder entries)
# ============================================================
print()
print("=" * 60)
print("2. NULL/EMPTY LINKS")
print("=" * 60)
for i in null_format:
    link = links[i]
    mids = link.get('matrix_ids', [])
    cids = link.get('contract_ids', [])
    print("  Link[%d]: matrix_ids=%s, contract_ids=%s" % (i, mids, cids))

# ============================================================
# 3. Check batch-format links for proper fields
# ============================================================
print()
print("=" * 60)
print("3. BATCH-FORMAT LINK VALIDATION")
print("=" * 60)
batch_issues = []
for i in batch_format:
    link = links[i]
    # These should have been merged into group format
    batch_issues.append("Link[%d]: batch format with link_index=%s, matrix_ids=%s, status=%s" % (
        i, link.get('link_index'), link.get('matrix_ids', []), link.get('status', 'N/A')))
for issue in batch_issues[:10]:
    print("  " + issue)
if len(batch_issues) > 10:
    print("  ... and %d more" % (len(batch_issues) - 10))

# ============================================================
# 4. Validate group-format links
# ============================================================
print()
print("=" * 60)
print("4. GROUP-FORMAT LINK VALIDATION")
print("=" * 60)
for i in group_format:
    link = links[i]
    rel = link.get('relationship')
    risk = link.get('risk_level')
    discs = link.get('discrepancies', [])
    cids = link.get('contract_ids', [])
    mids = link.get('matrix_ids', [])

    # deviation must have risk_level != none
    if rel == 'deviation' and risk == 'none':
        errors.append("Link[%d] (%s): deviation with risk_level=none" % (i, mids))

    # deviation must have non-empty discrepancies
    if rel == 'deviation' and len(discs) == 0:
        errors.append("Link[%d] (%s): deviation with empty discrepancies" % (i, mids))

    # aligned must have empty discrepancies
    if rel == 'aligned' and len(discs) > 0:
        errors.append("Link[%d] (%s): aligned with %d discrepancies" % (i, mids, len(discs)))

    # aligned must have risk_level=none
    if rel == 'aligned' and risk != 'none':
        errors.append("Link[%d] (%s): aligned with risk_level=%s (should be none)" % (i, mids, risk))

    # must have contract_ids
    if rel in ('aligned', 'deviation') and len(cids) == 0:
        errors.append("Link[%d] (%s): %s with empty contract_ids" % (i, mids, rel))

    # must have matrix_ids
    if len(mids) == 0:
        errors.append("Link[%d]: empty matrix_ids" % i)

    # must have legal_topic
    if not link.get('legal_topic'):
        warnings.append("Link[%d] (%s): missing legal_topic" % (i, mids))

    # must have matrix_standard
    if not link.get('matrix_standard'):
        warnings.append("Link[%d] (%s): missing matrix_standard" % (i, mids))

    # must have contract_position
    if not link.get('contract_position'):
        warnings.append("Link[%d] (%s): missing contract_position" % (i, mids))

    # must have status_reason
    if not link.get('status_reason'):
        warnings.append("Link[%d] (%s): missing status_reason" % (i, mids))

    # must have matrix_evidence
    if not link.get('matrix_evidence'):
        warnings.append("Link[%d] (%s): missing matrix_evidence" % (i, mids))

    # must have contract_evidence
    if not link.get('contract_evidence'):
        warnings.append("Link[%d] (%s): missing contract_evidence" % (i, mids))

print("Group-format link issues found: %d errors, %d warnings" % (
    len([e for e in errors if 'Link[' in e and 'group' not in e.lower()]),
    len(warnings)))

# ============================================================
# 5. Validate atomic_links
# ============================================================
print()
print("=" * 60)
print("5. ATOMIC LINKS VALIDATION")
print("=" * 60)
al_errors = []
for i, al in enumerate(atomic_links):
    if 'matrix_id' not in al or not al['matrix_id']:
        al_errors.append("AL[%d]: missing matrix_id" % i)
    if 'contract_id' not in al or not al['contract_id']:
        al_errors.append("AL[%d]: missing contract_id" % i)
    if 'relationship' not in al:
        al_errors.append("AL[%d]: missing relationship" % i)
    if 'link_index' not in al:
        al_errors.append("AL[%d]: missing link_index" % i)
    if 'coverage_role' not in al:
        al_errors.append("AL[%d]: missing coverage_role" % i)
    if 'coverage' not in al:
        al_errors.append("AL[%d]: missing coverage" % i)

    # Check that relationship matches the parent group link
    li = al.get('link_index')
    if li is not None and isinstance(li, int) and li < len(links):
        parent = links[li]
        parent_rel = parent.get('relationship')
        if parent_rel and al.get('relationship') != parent_rel:
            al_errors.append("AL[%d]: relationship '%s' != parent link[%d] relationship '%s'" % (
                i, al.get('relationship'), li, parent_rel))

for e in al_errors[:30]:
    print("  " + e)
print("  Total atomic link errors: %d" % len(al_errors))
errors.extend(al_errors)

# ============================================================
# 6. Validate coverage_ledger
# ============================================================
print()
print("=" * 60)
print("6. COVERAGE LEDGER VALIDATION")
print("=" * 60)

cl_matrix = coverage_ledger.get('matrix', [])
cl_contract = coverage_ledger.get('contract', [])

# Check matrix closures
matrix_closures = Counter(m['closure'] for m in cl_matrix)
print("  Matrix closures: %s" % dict(matrix_closures))

# Check contract closures
contract_closures = Counter(c['closure'] for c in cl_contract)
print("  Contract closures: %s" % dict(contract_closures))

# Every matrix id must be in coverage_ledger
cl_matrix_ids = set(m['matrix_id'] for m in cl_matrix)
link_matrix_ids = set()
for l in links:
    for mid in l.get('matrix_ids', []):
        link_matrix_ids.add(mid)
um_matrix_ids = set(u['matrix_id'] for u in unmatched_matrix)
all_matrix_ids = link_matrix_ids | um_matrix_ids

missing_from_cl = all_matrix_ids - cl_matrix_ids
if missing_from_cl:
    errors.append("BLOCKING: %d matrix ids in links/unmatched but not in coverage_ledger: %s" % (
        len(missing_from_cl), sorted(missing_from_cl)))

# Out-of-scope/not_applicable must NOT be in unmatched_matrix
for m in cl_matrix:
    if m['closure'] in ('out_of_scope', 'not_applicable') and m['matrix_id'] in um_matrix_ids:
        errors.append("BLOCKING: matrix %s is %s in coverage_ledger but appears in unmatched_matrix" % (
            m['matrix_id'], m['closure']))

# Linked entries should have link_indices
empty_link_indices = [m['matrix_id'] for m in cl_matrix if m['closure'] == 'linked' and not m.get('link_indices')]
if empty_link_indices:
    warnings.append("%d linked matrix entries have empty link_indices: %s" % (
        len(empty_link_indices), empty_link_indices[:10]))

# Every contract id in links/unmatched_contract must be in coverage_ledger
cl_contract_ids = set(c['contract_id'] for c in cl_contract)
link_contract_ids = set()
for l in links:
    for cid in l.get('contract_ids', []):
        link_contract_ids.add(cid)
uc_contract_ids = set(u['contract_id'] for u in unmatched_contract)
all_contract_ids = link_contract_ids | uc_contract_ids

missing_contract_from_cl = all_contract_ids - cl_contract_ids
if missing_contract_from_cl:
    errors.append("BLOCKING: %d contract ids in links/unmatched_contract but not in coverage_ledger: %s" % (
        len(missing_contract_from_cl), sorted(missing_contract_from_cl)))

# ============================================================
# 7. Validate unmatched_matrix
# ============================================================
print()
print("=" * 60)
print("7. UNMATCHED MATRIX VALIDATION")
print("=" * 60)
for u in unmatched_matrix:
    if not u.get('matrix_id'):
        errors.append("unmatched_matrix entry missing matrix_id")
    if not u.get('requirement'):
        warnings.append("unmatched_matrix %s: missing requirement" % u.get('matrix_id', '?'))
    if not u.get('source_evidence'):
        warnings.append("unmatched_matrix %s: missing source_evidence" % u.get('matrix_id', '?'))
    if u.get('status') != 'missing_in_contract':
        errors.append("unmatched_matrix %s: status is '%s', should be 'missing_in_contract'" % (
            u.get('matrix_id'), u.get('status')))
    if u.get('risk_level') not in ('low', 'medium', 'high'):
        errors.append("unmatched_matrix %s: invalid risk_level '%s'" % (u.get('matrix_id'), u.get('risk_level')))
print("  Total unmatched_matrix entries: %d" % len(unmatched_matrix))

# ============================================================
# 8. Validate unmatched_contract
# ============================================================
print()
print("=" * 60)
print("8. UNMATCHED CONTRACT VALIDATION")
print("=" * 60)
for u in unmatched_contract:
    if not u.get('contract_id'):
        errors.append("unmatched_contract entry missing contract_id")
    if not u.get('contract_position'):
        warnings.append("unmatched_contract %s: missing contract_position" % u.get('contract_id', '?'))
    if not u.get('source_evidence'):
        warnings.append("unmatched_contract %s: missing source_evidence" % u.get('contract_id', '?'))
    if u.get('status') != 'extra_in_contract':
        errors.append("unmatched_contract %s: status is '%s', should be 'extra_in_contract'" % (
            u.get('contract_id'), u.get('status')))
    if u.get('risk_level') not in ('low', 'medium', 'high'):
        errors.append("unmatched_contract %s: invalid risk_level '%s'" % (u.get('contract_id'), u.get('risk_level')))
print("  Total unmatched_contract entries: %d" % len(unmatched_contract))

# ============================================================
# 9. Validate summary counts
# ============================================================
print()
print("=" * 60)
print("9. SUMMARY COUNT VALIDATION")
print("=" * 60)
actual_aligned = sum(1 for l in links if l.get('relationship') == 'aligned')
actual_deviation = sum(1 for l in links if l.get('relationship') == 'deviation')
actual_missing = len(unmatched_matrix)
actual_extra = len(unmatched_contract)

print("  Summary:  aligned=%s, deviation=%s, missing=%s, extra=%s" % (
    summary.get('aligned_count'), summary.get('deviation_count'),
    summary.get('missing_in_contract_count'), summary.get('extra_in_contract_count')))
print("  Actual:   aligned=%s, deviation=%s, missing=%s, extra=%s" % (
    actual_aligned, actual_deviation, actual_missing, actual_extra))

if summary.get('aligned_count') != actual_aligned:
    errors.append("Summary aligned_count=%s != actual=%s" % (summary.get('aligned_count'), actual_aligned))
if summary.get('deviation_count') != actual_deviation:
    errors.append("Summary deviation_count=%s != actual=%s" % (summary.get('deviation_count'), actual_deviation))
if summary.get('missing_in_contract_count') != actual_missing:
    errors.append("Summary missing_in_contract_count=%s != actual=%s" % (summary.get('missing_in_contract_count'), actual_missing))
if summary.get('extra_in_contract_count') != actual_extra:
    errors.append("Summary extra_in_contract_count=%s != actual=%s" % (summary.get('extra_in_contract_count'), actual_extra))

# ============================================================
# 10. Check for invented locators / parenthetical ids
# ============================================================
print()
print("=" * 60)
print("10. CONTRACT ID SANITY CHECKS")
print("=" * 60)
all_cids = set()
for l in links:
    for cid in l.get('contract_ids', []):
        all_cids.add(cid)
for al in atomic_links:
    all_cids.add(al.get('contract_id', ''))
for uc in unmatched_contract:
    all_cids.add(uc.get('contract_id', ''))
all_cids.discard('')

parenthetical = [cid for cid in all_cids if '(' in cid or ')' in cid]
if parenthetical:
    errors.append("Parenthetical contract ids found: %s" % parenthetical)

# Check for ids that look like they might be invented
# Valid patterns: numeric (e.g., "4.3"), "Appendix_X" style, "Section_X" style
import re
suspicious = []
for cid in sorted(all_cids):
    if re.match(r'^[\d.]+$', cid):
        continue  # numeric clause
    if re.match(r'^[A-Za-z]', cid):
        continue  # starts with letter
    if cid.startswith('Приложение') or cid.startswith('App'):
        continue
    suspicious.append(cid)
if suspicious:
    warnings.append("Potentially unusual contract ids: %s" % suspicious[:20])

print("  Total unique contract ids: %d" % len(all_cids))
print("  Parenthetical: %s" % parenthetical)
print("  Suspicious: %s" % suspicious[:10])

# ============================================================
# FINAL REPORT
# ============================================================
print()
print("=" * 60)
print("FINAL QA REPORT")
print("=" * 60)
print()
print("BLOCKING ERRORS (%d):" % len(errors))
for e in errors:
    print("  [ERROR] " + e)
print()
print("WARNINGS (%d):" % len(warnings))
for w in warnings:
    print("  [WARN]  " + w)

# Write validation report
report = {
    "valid": len(errors) == 0,
    "errors": errors,
    "warnings": warnings,
    "counts": {
        "links_total": len(links),
        "links_group_format": len(group_format),
        "links_batch_format": len(batch_format),
        "links_null": len(null_format),
        "atomic_links": len(atomic_links),
        "unmatched_matrix": len(unmatched_matrix),
        "unmatched_contract": len(unmatched_contract),
        "coverage_ledger_matrix": len(cl_matrix),
        "coverage_ledger_contract": len(cl_contract),
        "summary_aligned": summary.get('aligned_count'),
        "summary_deviation": summary.get('deviation_count'),
        "summary_missing": summary.get('missing_in_contract_count'),
        "summary_extra": summary.get('extra_in_contract_count'),
        "actual_aligned": actual_aligned,
        "actual_deviation": actual_deviation,
        "actual_missing": actual_missing,
        "actual_extra": actual_extra,
    }
}

with open('/outputs/working/final_qa_report.json', 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print()
print("Report written to /outputs/working/final_qa_report.json")
print("Overall: %s" % ("VALID" if report['valid'] else "INVALID - %d blocking errors" % len(errors)))
