#!/usr/bin/env python3
"""Build matrix_inventory.json and contract_inventory.json from inputs."""
import json, re

# --- Load matrix ---
with open("inputs/matrix.json", "r", encoding="utf-8") as f:
    matrix = json.load(f)

matrix_inv = []
for item in matrix:
    num = item["number"]
    enriched = item.get("enriched_text", "")
    main_idea = item.get("main_idea", "")
    topics = item.get("topics", [])
    product = item.get("only_for_product", "common")
    lot = item.get("only_for_lot", "common")
    terminal = item.get("only_for_terminal", "common")
    req_type = item.get("required_type", "optional")
    
    # Build proposition
    if main_idea:
        proposition = main_idea
    elif topics:
        proposition = "; ".join(topics[:3])
    else:
        proposition = enriched[:200]
    
    # Determine materiality
    if not enriched.strip() and not topics:
        materiality = "heading"
    elif req_type == "mandatory":
        materiality = "material"
    else:
        # optional items can still be material if they have operative content
        if any(kw in enriched.lower() for kw in ["обязуется", "имеет право", "вправе", "удерживать", "штраф", "ответственность", "расторг", "срок", "оплат", "перечисл", "возместить"]):
            materiality = "material"
        else:
            materiality = "technical"
    
    # Determine applicability
    applicability = "in_scope"
    applicability_reason = "common acquiring contract"
    if product != "common":
        applicability = "conditional"
        applicability_reason = f"product={product}"
    if lot == "fz_44":
        applicability = "conditional"
        applicability_reason = f"lot=fz_44"
    if lot == "fz_223":
        applicability = "conditional"
        applicability_reason = f"lot=fz_223"
    
    # Determine party
    if "Банк имеет право" in enriched or "Банк вправе" in enriched:
        party = "Bank"
    elif "Предприятие обязуется" in enriched or "Предприятие обязано" in enriched:
        party = "Merchant"
    elif "Банк обязуется" in enriched:
        party = "Bank"
    elif "Предприятие имеет право" in enriched:
        party = "Merchant"
    else:
        party = "Both"
    
    # Determine right_or_obligation
    if "обязуется" in enriched or "обязано" in enriched or "обязан" in enriched:
        right_or_obligation = "obligation"
    elif "имеет право" in enriched or "вправе" in enriched:
        right_or_obligation = "right"
    elif "не несет ответственности" in enriched:
        right_or_obligation = "allocation_of_risk"
    else:
        right_or_obligation = "obligation"
    
    # Determine object
    if "ТСТ" in enriched or "торгово-сервисн" in enriched.lower():
        object_ = "merchant outlet registration"
    elif "QR" in enriched or "QR-код" in enriched:
        object_ = "QR code operations"
    elif "SberPay" in enriched:
        object_ = "SberPay payment method"
    elif "терминал" in enriched.lower():
        object_ = "terminal equipment"
    elif "ПДн" in enriched or "персональных данных" in enriched:
        object_ = "personal data"
    elif "оплат" in enriched.lower() and "услуг" in enriched.lower():
        object_ = "payment for Bank services"
    elif "перечисл" in enriched.lower():
        object_ = "settlement of operations"
    elif "ответственность" in enriched.lower():
        object_ = "liability"
    elif "расторж" in enriched.lower():
        object_ = "contract termination"
    elif "форс-мажор" in enriched.lower():
        object_ = "force majeure"
    elif "спор" in enriched.lower():
        object_ = "dispute resolution"
    elif "конфиденциальн" in enriched.lower():
        object_ = "confidentiality"
    elif "документ" in enriched.lower() and "обмен" in enriched.lower():
        object_ = "document exchange"
    elif "PCI DSS" in enriched:
        object_ = "PCI DSS compliance"
    elif "Повторяющихся платежей" in enriched:
        object_ = "recurring payments"
    else:
        object_ = "general contract terms"
    
    # Determine trigger
    trigger = ""
    if "при изменении" in enriched.lower():
        trigger = "change in TST information"
    elif "при подключении" in enriched.lower():
        trigger = "connection of additional equipment"
    elif "в случае" in enriched.lower():
        m = re.search(r'в случае\s+(.{10,80}?)[,;.]', enriched.lower())
        if m:
            trigger = m.group(1).strip()
    elif "при выявлении" in enriched.lower():
        trigger = "detection of violation"
    elif "по запросу" in enriched.lower():
        trigger = "Bank request"
    elif "с даты расторжения" in enriched.lower():
        trigger = "contract termination"
    
    # Material terms
    material_terms = ""
    # Look for deadlines
    deadlines = re.findall(r'(\d+\s*(?:\((?:[а-я]+)\))?\s*(?:рабочих|календарных)\s*дней)', enriched)
    if deadlines:
        material_terms = "deadline: " + ", ".join(deadlines)
    # Look for amounts
    amounts = re.findall(r'(\d+\s*\d*\s*(?:рублей|руб\.))', enriched)
    if amounts:
        if material_terms:
            material_terms += "; "
        material_terms += "amount: " + ", ".join(amounts)
    
    matrix_inv.append({
        "id": num,
        "proposition": proposition[:300],
        "party": party,
        "right_or_obligation": right_or_obligation,
        "object": object_,
        "trigger": trigger[:200] if trigger else "",
        "material_terms": material_terms[:200],
        "applicability": applicability,
        "applicability_reason": applicability_reason,
        "materiality": materiality
    })

with open("outputs/working/matrix_inventory.json", "w", encoding="utf-8") as f:
    json.dump(matrix_inv, f, ensure_ascii=False, indent=2)

print(f"Matrix inventory: {len(matrix_inv)} items")

# --- Load contract ---
with open("inputs/contract.txt", "r", encoding="utf-8") as f:
    contract_text = f.read()

# Parse contract into clauses
lines = contract_text.split('\n')
contract_inv = []

# Extract definitions (section 1)
in_defs = False
for line in lines:
    line_s = line.strip()
    # Detect definition lines like "1.1. Авторизация – ..."
    m = re.match(r'^(\d+\.\d+)\.\s+(.+?)\s*[–-]\s*(.+)$', line_s)
    if m:
        cid = m.group(1)
        term = m.group(2).strip()
        definition = m.group(3).strip()
        contract_inv.append({
            "id": cid,
            "proposition": f"{term}: {definition}"[:300],
            "party": "Both",
            "right_or_obligation": "definition",
            "object": "definitions",
            "trigger": "",
            "material_terms": "",
            "applicability": "in_scope",
            "applicability_reason": "definition section",
            "materiality": "technical"
        })
        continue
    
    # Detect operative clauses with numbering
    # Pattern: "2.1. ...", "4.2.1. ...", "5.1.1.1. ...", "0.0.1. ..."
    m = re.match(r'^(\d+(?:\.\d+)*)\.\s+(.+)$', line_s)
    if m:
        cid = m.group(1)
        content = m.group(2).strip()
        # Skip if it's just a heading like "2. общие положения"
        if re.match(r'^\d+$', cid) and len(content) < 100 and content.isupper():
            contract_inv.append({
                "id": cid,
                "proposition": content[:300],
                "party": "Both",
                "right_or_obligation": "heading",
                "object": "section heading",
                "trigger": "",
                "material_terms": "",
                "applicability": "in_scope",
                "applicability_reason": "section heading",
                "materiality": "heading"
            })
            continue
        
        # Determine party
        if "Банк имеет право" in content or "Банк вправе" in content:
            party = "Bank"
        elif "Предприятие обязуется" in content or "Предприятие обязано" in content:
            party = "Merchant"
        elif "Банк обязуется" in content:
            party = "Bank"
        elif "Предприятие имеет право" in content:
            party = "Merchant"
        elif "Стороны" in content:
            party = "Both"
        else:
            party = "Both"
        
        # Determine right_or_obligation
        if "обязуется" in content or "обязано" in content or "обязан" in content:
            right_or_obligation = "obligation"
        elif "имеет право" in content or "вправе" in content:
            right_or_obligation = "right"
        elif "не несет ответственности" in content:
            right_or_obligation = "allocation_of_risk"
        elif "несет ответственность" in content:
            right_or_obligation = "obligation"
        else:
            right_or_obligation = "provision"
        
        # Determine materiality
        if right_or_obligation in ("obligation", "right", "allocation_of_risk"):
            materiality = "material"
        elif any(kw in content.lower() for kw in ["штраф", "пеня", "неустойк", "расторж", "срок", "оплат", "перечисл", "возместить", "удерж"]):
            materiality = "material"
        else:
            materiality = "technical"
        
        contract_inv.append({
            "id": cid,
            "proposition": content[:300],
            "party": party,
            "right_or_obligation": right_or_obligation,
            "object": "",
            "trigger": "",
            "material_terms": "",
            "applicability": "in_scope",
            "applicability_reason": "operative clause",
            "materiality": materiality
        })

# Add appendix entries
for app_label in ["Приложение № 1", "Приложение № 1.1", "Приложение № 2"]:
    contract_inv.append({
        "id": app_label,
        "proposition": f"Appendix form referenced in contract",
        "party": "Both",
        "right_or_obligation": "form",
        "object": "appendix",
        "trigger": "",
        "material_terms": "",
        "applicability": "in_scope",
        "applicability_reason": "appendix to contract",
        "materiality": "technical"
    })

with open("outputs/working/contract_inventory.json", "w", encoding="utf-8") as f:
    json.dump(contract_inv, f, ensure_ascii=False, indent=2)

print(f"Contract inventory: {len(contract_inv)} items")
print("Done building inventories.")
