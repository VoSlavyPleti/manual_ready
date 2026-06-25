#!/usr/bin/env python3
"""QA validation script for merged discrepancy analysis artifact."""

import json
import sys
from collections import Counter

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    errors = []
    warnings = []

    # Load data
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    artifact = load_json(os.path.join(base, 'merged_artifact.json'))
    matrix_inv = load_json(os.path.join(base, 'matrix_inventory.json'))
    contract_inv = load_json(os.path.join(base, 'contract_inventory.json'))

    links = artifact.get('links', [])
    atomic_links = artifact.get('atomic_links', [])
    unmatched_matrix = artifact.get('unmatched_matrix', [])
    unmatched_contract = artifact.get('unmatched_contract', [])
    summary = artifact.get('summary', {})

    # Build lookup sets
    matrix_ids_set = {item['id'] for item in matrix_inv}
    contract_ids_set = {item['id'] for item in contract_inv}

    # ============================================================
    # 1. Validate atomic_links structure
    # ============================================================
    required_atomic_fields = [
        'matrix_id', 'contract_id', 'relationship', 'coverage',
        'analogue_strength', 'coverage_role', 'element_checklist'
    ]
    checklist_elements = [
        'party', 'legal_object', 'operative_right_or_duty', 'trigger',
        'deadline', 'amount_formula_cap', 'procedure_channel',
        'liability_remedy', 'scope_exceptions', 'consequence'
    ]
    valid_results = {'same', 'equivalent', 'different', 'missing', 'not_applicable'}
    valid_relationships = {'aligned', 'deviation'}
    valid_strengths = {'strong', 'partial'}
    valid_roles = {'direct', 'parent', 'child', 'appendix', 'definition', 'procedure', 'companion'}

    for i, row in enumerate(atomic_links):
        prefix = f"atomic_links[{i}]"

        # Check required fields exist
        for field in required_atomic_fields:
            if field not in row:
                errors.append(f"{prefix}: missing required field '{field}'")

        # Check matrix_id exists in inventory
        mid = row.get('matrix_id', '')
        if mid and mid not in matrix_ids_set:
            errors.append(f"{prefix}: matrix_id '{mid}' not found in matrix_inventory.json")

        # Check contract_id exists in inventory
        cid = row.get('contract_id', '')
        if cid and cid not in contract_ids_set:
            errors.append(f"{prefix}: contract_id '{cid}' not found in contract_inventory.json")

        # Check relationship
        rel = row.get('relationship', '')
        if rel and rel not in valid_relationships:
            errors.append(f"{prefix}: invalid relationship '{rel}'")

        # Check analogue_strength - must NOT be weak_context
        strength = row.get('analogue_strength', '')
        if strength == 'weak_context':
            errors.append(f"{prefix}: analogue_strength is 'weak_context' — not allowed in atomic_links")
        elif strength and strength not in valid_strengths:
            errors.append(f"{prefix}: invalid analogue_strength '{strength}'")

        # Check coverage_role
        role = row.get('coverage_role', '')
        if role and role not in valid_roles:
            warnings.append(f"{prefix}: unrecognized coverage_role '{role}'")

        # Check element_checklist
        checklist = row.get('element_checklist', [])
        if not isinstance(checklist, list):
            errors.append(f"{prefix}: element_checklist is not a list")
            continue

        checklist_elements_found = set()
        checklist_results = {}
        for ci, item in enumerate(checklist):
            if not isinstance(item, dict):
                errors.append(f"{prefix}: element_checklist[{ci}] is not a dict")
                continue
            elem = item.get('element', '')
            result = item.get('result', '')
            if elem not in checklist_elements:
                errors.append(f"{prefix}: element_checklist[{ci}] has unknown element '{elem}'")
            if result not in valid_results:
                errors.append(f"{prefix}: element_checklist[{ci}] has invalid result '{result}'")
            checklist_elements_found.add(elem)
            checklist_results[elem] = result

        # Check all 10 elements present
        for elem in checklist_elements:
            if elem not in checklist_elements_found:
                errors.append(f"{prefix}: element_checklist missing element '{elem}'")

        # Check deviation rule: at least one different or missing
        if rel == 'deviation':
            has_gap = any(
                item.get('result') in ('different', 'missing')
                for item in checklist
            )
            if not has_gap:
                errors.append(f"{prefix}: relationship is 'deviation' but no checklist item is 'different' or 'missing'")

        # Check aligned rule: NO different or missing
        if rel == 'aligned':
            has_gap = any(
                item.get('result') in ('different', 'missing')
                for item in checklist
            )
            if has_gap:
                gap_items = [item.get('element') for item in checklist if item.get('result') in ('different', 'missing')]
                errors.append(f"{prefix}: relationship is 'aligned' but checklist has 'different'/'missing': {gap_items}")

    # ============================================================
    # 2. Validate links structure
    # ============================================================
    for i, link in enumerate(links):
        prefix = f"links[{i}]"

        # Check required fields
        for field in ['matrix_ids', 'contract_ids', 'relationship', 'legal_topic']:
            if field not in link:
                errors.append(f"{prefix}: missing required field '{field}'")

        # Check no empty contract_ids
        cids = link.get('contract_ids', [])
        if not cids:
            errors.append(f"{prefix}: contract_ids is empty")

        # Check no empty matrix_ids
        mids = link.get('matrix_ids', [])
        if not mids:
            errors.append(f"{prefix}: matrix_ids is empty")

        # Check all matrix_ids in inventory
        for mid in mids:
            if mid not in matrix_ids_set:
                errors.append(f"{prefix}: matrix_id '{mid}' not in matrix_inventory.json")

        # Check all contract_ids in inventory
        for cid in cids:
            if cid not in contract_ids_set:
                errors.append(f"{prefix}: contract_id '{cid}' not in contract_inventory.json")

        # Check relationship
        rel = link.get('relationship', '')
        if rel not in valid_relationships:
            errors.append(f"{prefix}: invalid relationship '{rel}'")

        # Check deviation has discrepancies
        discrepancies = link.get('discrepancies', [])
        if rel == 'deviation':
            if not discrepancies:
                errors.append(f"{prefix}: relationship is 'deviation' but discrepancies is empty")
            else:
                for di, disc in enumerate(discrepancies):
                    for df in ['type', 'description', 'risk']:
                        if df not in disc:
                            errors.append(f"{prefix}: discrepancy[{di}] missing '{df}'")

        # Check aligned has no discrepancies
        if rel == 'aligned':
            if discrepancies:
                errors.append(f"{prefix}: relationship is 'aligned' but discrepancies is non-empty")

    # ============================================================
    # 3. Check every matrix id appears exactly once
    # ============================================================
    all_linked_matrix_ids = []
    for link in links:
        all_linked_matrix_ids.extend(link.get('matrix_ids', []))
    all_unmatched_matrix_ids = [item.get('matrix_id', '') for item in unmatched_matrix]

    linked_counter = Counter(all_linked_matrix_ids)
    unmatched_counter = Counter(all_unmatched_matrix_ids)

    # Check for duplicates in links
    for mid, count in linked_counter.items():
        if count > 1:
            errors.append(f"matrix_id '{mid}' appears in {count} different links (should be exactly 1)")

    # Check for duplicates in unmatched
    for mid, count in unmatched_counter.items():
        if count > 1:
            errors.append(f"matrix_id '{mid}' appears {count} times in unmatched_matrix")

    # Check for cross-appearance
    linked_set = set(all_linked_matrix_ids)
    unmatched_set = set(all_unmatched_matrix_ids)
    cross = linked_set & unmatched_set
    if cross:
        errors.append(f"matrix_ids appear in BOTH links and unmatched_matrix: {cross}")

    # Check all material matrix items are covered
    material_matrix_ids = {item['id'] for item in matrix_inv if item.get('materiality') == 'material'}
    covered = linked_set | unmatched_set
    missing_from_artifact = material_matrix_ids - covered
    if missing_from_artifact:
        errors.append(f"Material matrix items not in links or unmatched_matrix: {missing_from_artifact}")

    # Check no extra matrix ids
    extra_matrix = covered - matrix_ids_set
    if extra_matrix:
        errors.append(f"Matrix ids in artifact not in matrix_inventory: {extra_matrix}")

    # ============================================================
    # 4. Check unmatched_matrix uses status: missing_in_contract
    # ============================================================
    for i, item in enumerate(unmatched_matrix):
        prefix = f"unmatched_matrix[{i}]"
        status = item.get('status', '')
        if status != 'missing_in_contract':
            errors.append(f"{prefix}: status is '{status}', must be 'missing_in_contract'")
        if 'matrix_id' not in item:
            errors.append(f"{prefix}: missing 'matrix_id'")
        # Check for forbidden fields
        for forbidden in ['reason', 'classification', 'relationship']:
            if forbidden in item:
                errors.append(f"{prefix}: contains forbidden field '{forbidden}' (use 'status' instead)")

    # ============================================================
    # 5. Check unmatched_contract
    # ============================================================
    for i, item in enumerate(unmatched_contract):
        prefix = f"unmatched_contract[{i}]"
        if 'contract_id' not in item:
            errors.append(f"{prefix}: missing 'contract_id'")
        cid = item.get('contract_id', '')
        if cid and cid not in contract_ids_set:
            errors.append(f"{prefix}: contract_id '{cid}' not in contract_inventory.json")

    # ============================================================
    # 6. Check summary counts
    # ============================================================
    aligned_count = sum(1 for link in links if link.get('relationship') == 'aligned')
    deviation_count = sum(1 for link in links if link.get('relationship') == 'deviation')
    missing_count = len(unmatched_matrix)
    extra_count = sum(1 for item in unmatched_contract if item.get('classification') == 'extra_in_contract')

    if summary.get('aligned_count') != aligned_count:
        errors.append(f"summary.aligned_count is {summary.get('aligned_count')}, actual: {aligned_count}")
    if summary.get('deviation_count') != deviation_count:
        errors.append(f"summary.deviation_count is {summary.get('deviation_count')}, actual: {deviation_count}")
    if summary.get('missing_in_contract_count') != missing_count:
        errors.append(f"summary.missing_in_contract_count is {summary.get('missing_in_contract_count')}, actual: {missing_count}")
    if summary.get('extra_in_contract_count') != extra_count:
        errors.append(f"summary.extra_in_contract_count is {summary.get('extra_in_contract_count')}, actual: {extra_count}")

    # ============================================================
    # 7. Check for invented/parenthetical ids
    # ============================================================
    # Check contract_ids in links and atomic_links
    all_contract_ids_used = set()
    for link in links:
        all_contract_ids_used.update(link.get('contract_ids', []))
    for row in atomic_links:
        all_contract_ids_used.add(row.get('contract_id', ''))

    # Suspicious patterns
    suspicious_patterns = []
    for cid in sorted(all_contract_ids_used):
        # Check for parenthetical ids like "Section 7 (Ответственность)"
        if '(' in cid and ')' in cid:
            # Allow if it's a real printed locator - we flag for manual review
            warnings.append(f"contract_id with parentheses: '{cid}' — verify this is a real printed locator")
        # Check for translated labels
        if any(word in cid.lower() for word in ['appendix_', 'app_', 'приложение_']):
            if not cid.startswith('Приложение'):
                warnings.append(f"contract_id may be an alias: '{cid}'")

    # Check for ids like "0.0.1", "0.0.2", "0.0.3" — these look invented
    for cid in sorted(all_contract_ids_used):
        if cid.startswith('0.0.'):
            errors.append(f"contract_id '{cid}' appears to be invented (starts with 0.0.) — must be a real printed locator from contract.txt")

    # Check for ids like "7. ОТВЕТСТВЕННОСТЬ сторон, п. 0.1" — parenthetical subdivision
    for cid in sorted(all_contract_ids_used):
        if 'п. 0.' in cid or 'п.0.' in cid:
            errors.append(f"contract_id '{cid}' uses 'п. 0.X' numbering which appears invented — contract.txt must contain this exact locator")

    # ============================================================
    # 8. Check atomic_links ↔ links consistency
    # ============================================================
    # Every atomic_link should have a corresponding link
    for i, arow in enumerate(atomic_links):
        mid = arow.get('matrix_id', '')
        cid = arow.get('contract_id', '')
        link_idx = arow.get('link_index')
        if link_idx is not None:
            if link_idx >= len(links):
                errors.append(f"atomic_links[{i}]: link_index {link_idx} out of range (max {len(links)-1})")
            else:
                link = links[link_idx]
                if mid not in link.get('matrix_ids', []):
                    errors.append(f"atomic_links[{i}]: matrix_id '{mid}' not in links[{link_idx}].matrix_ids")
                if cid not in link.get('contract_ids', []):
                    errors.append(f"atomic_links[{i}]: contract_id '{cid}' not in links[{link_idx}].contract_ids")

    # ============================================================
    # 9. Check contract-only material items are classified
    # ============================================================
    material_contract_ids = {item['id'] for item in contract_inv if item.get('materiality') == 'material'}
    linked_contract_ids = set()
    for link in links:
        linked_contract_ids.update(link.get('contract_ids', []))
    unmatched_contract_ids = {item.get('contract_id', '') for item in unmatched_contract}
    not_material_ids = {item.get('contract_id', '') for item in unmatched_contract if item.get('classification') == 'not_material'}

    covered_contract = linked_contract_ids | unmatched_contract_ids
    missing_contract = material_contract_ids - covered_contract
    if missing_contract:
        warnings.append(f"Material contract items not in links or unmatched_contract: {missing_contract}")

    # ============================================================
    # 10. Check for deviation without risk
    # ============================================================
    for i, link in enumerate(links):
        if link.get('relationship') == 'deviation':
            for di, disc in enumerate(link.get('discrepancies', [])):
                risk = disc.get('risk', '')
                if not risk or risk.strip() == '':
                    errors.append(f"links[{i}].discrepancies[{di}]: 'risk' is empty")

    # ============================================================
    # Output
    # ============================================================
    print("=" * 60)
    print("QA VALIDATION RESULTS")
    print("=" * 60)
    print(f"\nERRORS: {len(errors)}")
    for e in errors:
        print(f"  ❌ {e}")

    print(f"\nWARNINGS: {len(warnings)}")
    for w in warnings:
        print(f"  ⚠️ {w}")

    print(f"\nSUMMARY:")
    print(f"  links: {len(links)}")
    print(f"  atomic_links: {len(atomic_links)}")
    print(f"  unmatched_matrix: {len(unmatched_matrix)}")
    print(f"  unmatched_contract: {len(unmatched_contract)}")
    print(f"  aligned (actual): {aligned_count}")
    print(f"  deviation (actual): {deviation_count}")
    print(f"  missing_in_contract (actual): {missing_count}")
    print(f"  extra_in_contract (actual): {extra_count}")

    # Write errors to file
    with open(os.path.join(base, 'qa_errors.json'), 'w') as f:
        json.dump({'errors': errors, 'warnings': warnings}, f, indent=2, ensure_ascii=False)

    return len(errors)

if __name__ == '__main__':
    sys.exit(main())
