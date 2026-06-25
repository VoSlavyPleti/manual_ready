import json

# Build batch 3 fragment: links, atomic_links, unmatched_matrix, unmatched_contract

links = []
atomic_links = []
unmatched_matrix = []
unmatched_contract = []

# Helper to add a simple aligned 1:1 link
def add_aligned_1to1(matrix_id, contract_id, legal_topic, matrix_standard, contract_position,
                      coverage_role="direct", analogue_strength="strong",
                      element_checklist_notes=None):
    link_idx = len(links)
    links.append({
        "matrix_ids": [matrix_id],
        "contract_ids": [contract_id],
        "relationship": "aligned",
        "legal_topic": legal_topic,
        "matrix_standard": matrix_standard,
        "contract_position": contract_position,
        "discrepancies": []
    })
    
    default_checklist = [
        ("party", "same", "Bank right; Enterprise bound"),
        ("legal_object", "same", "same legal object"),
        ("operative_right_or_duty", "same", "same operative right/duty"),
        ("trigger", "same", "same trigger"),
        ("deadline", "same", "same deadline if any"),
        ("amount_formula_cap", "not_applicable", ""),
        ("procedure_channel", "same", "same procedure"),
        ("liability_remedy", "same", "same remedy"),
        ("scope_exceptions", "same", "same scope"),
        ("consequence", "same", "same consequence")
    ]
    
    if element_checklist_notes:
        checklist = []
        for elem, result, note in default_checklist:
            if elem in element_checklist_notes:
                checklist.append({"element": elem, "result": element_checklist_notes[elem][0], "note": element_checklist_notes[elem][1]})
            else:
                checklist.append({"element": elem, "result": result, "note": note})
    else:
        checklist = [{"element": e, "result": r, "note": n} for e, r, n in default_checklist]
    
    atomic_links.append({
        "matrix_id": matrix_id,
        "contract_id": contract_id,
        "relationship": "aligned",
        "link_index": link_idx,
        "legal_topic": legal_topic,
        "analogue_strength": analogue_strength,
        "coverage_role": coverage_role,
        "coverage": f"Contract clause {contract_id} directly mirrors matrix requirement {matrix_id}",
        "element_checklist": checklist,
        "status_reason": "All material elements are same; contract preserves the Bank standard.",
        "discrepancies": []
    })

def add_deviation_1to1(matrix_id, contract_id, legal_topic, matrix_standard, contract_position,
                       discrepancies, element_checklist, status_reason,
                       coverage_role="direct", analogue_strength="partial"):
    link_idx = len(links)
    links.append({
        "matrix_ids": [matrix_id],
        "contract_ids": [contract_id],
        "relationship": "deviation",
        "legal_topic": legal_topic,
        "matrix_standard": matrix_standard,
        "contract_position": contract_position,
        "discrepancies": discrepancies
    })
    
    atomic_links.append({
        "matrix_id": matrix_id,
        "contract_id": contract_id,
        "relationship": "deviation",
        "link_index": link_idx,
        "legal_topic": legal_topic,
        "analogue_strength": analogue_strength,
        "coverage_role": coverage_role,
        "coverage": f"Contract clause {contract_id} partially covers matrix requirement {matrix_id}",
        "element_checklist": element_checklist,
        "status_reason": status_reason,
        "discrepancies": discrepancies
    })

def add_missing(matrix_id, requirement, risk, rejected_candidates=None):
    entry = {
        "matrix_id": matrix_id,
        "requirement": requirement,
        "status": "missing_in_contract",
        "risk": risk
    }
    if rejected_candidates:
        entry["rejected_candidates"] = rejected_candidates
    unmatched_matrix.append(entry)

def add_extra_contract(contract_id, contract_position, risk, materiality_reason):
    unmatched_contract.append({
        "contract_id": contract_id,
        "contract_position": contract_position,
        "status": "extra_in_contract",
        "risk": risk,
        "materiality_reason": materiality_reason
    })

# ============================================================
# GROUP 1: 5.1.8.5 - 5.1.8.13 (Bank rights to terminate authorization)
# All are identical in contract
# ============================================================

# 5.1.8.5
add_aligned_1to1("5.1.8.5", "5.1.8.5",
    "Bank right to stop authorization for prohibited activities per Resource Requirements",
    "Bank may unilaterally stop Authorization and/or terminate the Contract if Enterprise conducts activities prohibited by the Resource Requirements",
    "Contract 5.1.8.5: identical provision — Bank may unilaterally stop Authorization and/or terminate the Contract if Enterprise conducts activities listed in the Resource Requirements")

# 5.1.8.6
add_aligned_1to1("5.1.8.6", "5.1.8.6",
    "Bank right to stop authorization upon negative information from state authorities or Payment Systems",
    "Bank may unilaterally stop Authorization and/or terminate the Contract upon receiving negative information about the Enterprise/TST/Resource from Russian state authorities and/or Payment Systems",
    "Contract 5.1.8.6: identical provision")

# 5.1.8.7
add_aligned_1to1("5.1.8.7", "5.1.8.7",
    "Bank right to stop authorization upon fraud information",
    "Bank may unilaterally stop Authorization upon receiving fraud information about TST/Resource; sufficient confirmation includes information from issuer banks or Payment System notifications via fax/email",
    "Contract 5.1.8.7: identical provision including the evidentiary standard for fraud confirmation")

# 5.1.8.8
add_aligned_1to1("5.1.8.8", "5.1.8.8",
    "Bank right to stop authorization when TST premises repair prevents operations",
    "Bank may unilaterally stop Authorization and/or terminate the Contract if TST premises repair prevents conduct of Operations (trade_acquiring)",
    "Contract 5.1.8.8: identical provision")

# 5.1.8.9
add_aligned_1to1("5.1.8.9", "5.1.8.9",
    "Bank right to stop authorization upon Enterprise liquidation or bankruptcy",
    "Bank may unilaterally stop Authorization and/or terminate the Contract upon Enterprise liquidation or initiation of bankruptcy proceedings under Federal Law No. 127-FZ",
    "Contract 5.1.8.9: identical provision")

# 5.1.8.10
add_aligned_1to1("5.1.8.10", "5.1.8.10",
    "Bank right to stop authorization upon discovery of false information",
    "Bank may unilaterally stop Authorization and/or terminate the Contract upon discovery of false information about the Enterprise/TST/manager(s) provided at contract conclusion",
    "Contract 5.1.8.10: identical provision")

# 5.1.8.11
add_aligned_1to1("5.1.8.11", "5.1.8.11",
    "Bank right to stop authorization when goods/services do not match declared activity",
    "Bank may unilaterally stop Authorization and/or terminate the Contract if goods/services offered to Buyers do not correspond to the Enterprise's declared type of activity in TST Information",
    "Contract 5.1.8.11: identical provision")

# 5.1.8.12
add_aligned_1to1("5.1.8.12", "5.1.8.12",
    "Bank right to stop authorization after 30 calendar days without operations",
    "Bank may unilaterally stop Authorization and/or terminate the Contract if no operations occur for 30 consecutive calendar days",
    "Contract 5.1.8.12: identical provision")

# 5.1.8.13
add_aligned_1to1("5.1.8.13", "5.1.8.13",
    "Bank right to stop authorization upon exhaustion of Contract Price or expiry",
    "Bank may unilaterally stop Authorization and/or terminate the Contract upon exhaustion of the Contract Price and/or expiry of the Contract term per clause 10.1",
    "Contract 5.1.8.13: identical provision")

# ============================================================
# GROUP 2: 5.1.9 - 5.1.16 (Bank rights)
# ============================================================

# 5.1.9
add_aligned_1to1("5.1.9", "5.1.9",
    "Bank right to conduct additional operation checks including contacting issuer bank",
    "Bank may conduct additional checks of Operations at TST, including contacting the issuer bank to verify the lawfulness of the Operation",
    "Contract 5.1.9: identical provision")

# 5.1.10
add_aligned_1to1("5.1.10", "5.1.10",
    "Bank right to inspect Enterprise for fraud, activity mismatch, and Resource compliance",
    "Bank may inspect the Enterprise for fraudulent operations, goods/services not matching declared activity, and non-compliance with Contract requirements for the Resource, including access to restricted sections",
    "Contract 5.1.10: identical provision including access to restricted Resource sections")

# 5.1.11
add_aligned_1to1("5.1.11", "5.1.11",
    "Bank right to request operation documents within 13 months",
    "Bank may request Operation documents within 13 months from the Operation date; may also demand written statements, invoices, receipts, and other documents for dispute analysis",
    "Contract 5.1.11: same right to request documents within 13 months and demand supporting materials; the matrix additionally specifies document exchange via electronic channels per clause 2.3, while the contract omits this channel specification in 5.1.11 — but the general document exchange framework in contract 2.3 already covers this",
    element_checklist_notes={
        "procedure_channel": ("equivalent", "matrix: specifies electronic channels per 2.3; contract: omits channel reference in 5.1.11 but 2.3 provides general framework; gap: none — same result")
    })

# 5.1.12
add_aligned_1to1("5.1.12", "5.1.12",
    "Bank right to unilaterally amend referenced documents via Official Site with 1 day notice",
    "Bank may unilaterally amend documents referenced in the Contract by publishing on the Official Site at least 1 calendar day before changes take effect",
    "Contract 5.1.12: identical provision")

# 5.1.13
add_aligned_1to1("5.1.13", "5.1.13",
    "Bank right to notify of requisites change via Official Site",
    "Bank may notify the Enterprise of changes to Bank requisites by posting information on the Official Site",
    "Contract 5.1.13: identical provision")

# 5.1.14
add_aligned_1to1("5.1.14", "5.1.14",
    "Bank right to send queries to Enterprise email for operation information",
    "Bank may send queries to the Enterprise/TST email address specified in the Application/TST Information to obtain information on Operations",
    "Contract 5.1.14: identical provision")

# 5.1.15
add_aligned_1to1("5.1.15", "5.1.15",
    "Bank right to refuse contract conclusion without explanation",
    "Bank may refuse to conclude the Contract with the Enterprise without stating reasons",
    "Contract 5.1.15: identical provision")

# 5.1.16
add_aligned_1to1("5.1.16", "5.1.16",
    "Bank right to demand documents and information required by law",
    "Bank may demand from the Enterprise documents and information necessary to perform functions required by applicable legislation",
    "Contract 5.1.16: identical provision")

# ============================================================
# GROUP 3: 5.1.17.1 and 5.1.17.2 — MISSING
# ============================================================

add_missing("5.1.17.1",
    "Bank right to unilaterally terminate the Contract and demand return of Bank-owned Electronic terminals (POS) if monthly turnover per terminal is below 40,000 RUB (80,000 RUB for Moscow/St. Petersburg) for the last calendar month, excluding return operations",
    "Without this right, the Bank cannot exit unprofitable POS-terminal placements based on objective low-turnover thresholds. The Bank remains bound to maintain and service POS terminals even when transaction volumes are commercially non-viable, creating ongoing operational costs without corresponding revenue.",
    rejected_candidates=[
        {
            "contract_id": "5.1.8",
            "reason": "Contract 5.1.8 provides general termination triggers (breach, fraud, etc.) but does not include the specific low-turnover threshold for POS terminals. This is a different legal object — general termination vs. turnover-based terminal recall."
        },
        {
            "contract_id": "9.2",
            "reason": "Contract 9.2 allows either party to terminate with 30 days' notice, but this is a general termination right, not the Bank's specific right to terminate and demand terminal return based on low turnover thresholds. The matrix right is automatic upon the threshold being met; the contract requires 30 days' notice."
        }
    ])

add_missing("5.1.17.2",
    "Bank right to unilaterally terminate the Contract and demand return of Bank-owned Smart-terminals if monthly turnover per Smart-terminal is below 40,000 RUB (80,000 RUB for Moscow/St. Petersburg) for the last calendar month, or if there is debt for service fees/Bank remuneration/Smart-terminal return operations",
    "Without this right, the Bank cannot exit unprofitable Smart-terminal placements or recover terminals when the Enterprise has accumulated debt for service fees or return operations. The Bank remains exposed to both low-turnover and debtor scenarios without a specific contractual remedy to reclaim its equipment.",
    rejected_candidates=[
        {
            "contract_id": "5.1.8",
            "reason": "Contract 5.1.8 provides general termination triggers but does not include the specific low-turnover or debt-based terminal recall right for Smart-terminals."
        },
        {
            "contract_id": "5.1.2",
            "reason": "Contract 5.1.2 allows the Bank to suspend Authorization if the Enterprise has debt, but this is a suspension right, not a termination-and-return right tied to specific turnover thresholds or Smart-terminal debt categories."
        }
    ])

# ============================================================
# GROUP 4: 5.2.1 - 5.2.10, 5.2.12 (Bank obligations)
# ============================================================

# 5.2.1
add_aligned_1to1("5.2.1", "5.2.1",
    "Bank obligation to provide SPEP access for Operations",
    "Bank shall provide the Enterprise with access to SPEP (Electronic Payment System) for conducting Operations (internet_acquiring)",
    "Contract 5.2.1: identical provision")

# 5.2.2
add_aligned_1to1("5.2.2", "5.2.2",
    "Bank obligation to ensure security via modern protocols and 3DSecure",
    "Bank shall ensure security of Internet-acquiring Operations through modern protocols and 3DSecure technologies (internet_acquiring)",
    "Contract 5.2.2: identical provision")

# 5.2.3 — DEVIATION: Smart-terminals not mentioned
add_deviation_1to1("5.2.3", "5.2.3",
    "Bank obligation to install terminals and conduct staff training",
    "Bank shall install and prepare for operation Electronic terminals/Smart-terminals at the Enterprise and conduct initial training of TST employees per Bank instructional materials (trade_acquiring)",
    "Contract 5.2.3: Bank shall install and prepare Electronic terminals (without mentioning Smart-terminals) and conduct initial training of TST employees per Bank instructional materials",
    discrepancies=[{
        "type": "scope",
        "description": "Matrix covers both Electronic terminals and Smart-terminals for installation and training; contract 5.2.3 covers only Electronic terminals, omitting Smart-terminals from the Bank's installation and training obligation",
        "risk": "The Bank's obligation to install and train staff on Smart-terminals is not explicitly stated, potentially allowing the Enterprise to claim the Bank has not fulfilled installation/training duties for Smart-terminal devices. This narrows the Bank's documented scope of responsibility."
    }],
    element_checklist=[
        {"element": "party", "result": "same", "note": "Bank obligated; Enterprise benefited"},
        {"element": "legal_object", "result": "different", "note": "matrix: Electronic terminals and Smart-terminals; contract: Electronic terminals only; gap: Smart-terminals omitted from installation/training obligation"},
        {"element": "operative_right_or_duty", "result": "same", "note": "Bank duty to install and train"},
        {"element": "trigger", "result": "same", "note": "contract conclusion / terminal provision"},
        {"element": "deadline", "result": "same", "note": "no specific deadline in either"},
        {"element": "amount_formula_cap", "result": "not_applicable", "note": ""},
        {"element": "procedure_channel", "result": "same", "note": "installation and in-person training"},
        {"element": "liability_remedy", "result": "not_applicable", "note": ""},
        {"element": "scope_exceptions", "result": "different", "note": "matrix: covers both terminal types; contract: Smart-terminals not explicitly covered"},
        {"element": "consequence", "result": "same", "note": "terminals installed and staff trained"}
    ],
    status_reason="Contract 5.2.3 narrows the Bank's installation and training obligation by omitting Smart-terminals, which are a distinct terminal category in the matrix standard. The legal object is narrower.",
    analogue_strength="partial")

# 5.2.4
add_aligned_1to1("5.2.4", "5.2.4",
    "Bank obligation to provide 24/7 Authorization",
    "Bank shall provide round-the-clock Authorization",
    "Contract 5.2.4: identical provision")

# 5.2.5
add_aligned_1to1("5.2.5", "5.2.5",
    "Bank obligation to place training materials at specified URL",
    "Bank shall place training materials at https://www.sberbank.ru/help/business/acquiring for Enterprise employee training",
    "Contract 5.2.5: Bank shall place training materials at a site with blank/placeholder URL — formal difference only, to be filled",
    element_checklist_notes={
        "procedure_channel": ("equivalent", "matrix: specific URL; contract: blank placeholder; gap: none — placeholder to be filled, same legal effect")
    })

# 5.2.6 — DEVIATION: Smart-terminals not mentioned
add_deviation_1to1("5.2.6", "5.2.6",
    "Bank obligation to provide terminals with informational materials",
    "Bank shall provide Electronic terminals/Smart-terminals installed at the Enterprise/TST with informational materials necessary for conducting Operations (trade_acquiring)",
    "Contract 5.2.6: Bank shall provide Electronic terminals (without mentioning Smart-terminals) with informational materials necessary for conducting Operations",
    discrepancies=[{
        "type": "scope",
        "description": "Matrix covers both Electronic terminals and Smart-terminals for informational materials provision; contract 5.2.6 covers only Electronic terminals, omitting Smart-terminals",
        "risk": "The Bank's obligation to provide informational materials for Smart-terminals is not explicitly stated, potentially creating ambiguity about the Bank's duties for Smart-terminal informational support."
    }],
    element_checklist=[
        {"element": "party", "result": "same", "note": "Bank obligated; Enterprise benefited"},
        {"element": "legal_object", "result": "different", "note": "matrix: Electronic terminals and Smart-terminals; contract: Electronic terminals only; gap: Smart-terminals omitted"},
        {"element": "operative_right_or_duty", "result": "same", "note": "Bank duty to provide informational materials"},
        {"element": "trigger", "result": "same", "note": "terminal installation"},
        {"element": "deadline", "result": "not_applicable", "note": ""},
        {"element": "amount_formula_cap", "result": "not_applicable", "note": ""},
        {"element": "procedure_channel", "result": "same", "note": "physical informational materials"},
        {"element": "liability_remedy", "result": "not_applicable", "note": ""},
        {"element": "scope_exceptions", "result": "different", "note": "matrix: both terminal types; contract: Smart-terminals not covered"},
        {"element": "consequence", "result": "same", "note": "terminals equipped with informational materials"}
    ],
    status_reason="Contract 5.2.6 narrows the Bank's obligation by omitting Smart-terminals from the informational materials provision duty. The scope is narrower than the matrix standard.",
    analogue_strength="partial")

# 5.2.7 — DEVIATION: Smart-terminals not mentioned
add_deviation_1to1("5.2.7", "5.2.7",
    "Bank obligation to ensure 24/7 terminal operability and replacement within 3 working days",
    "Bank shall ensure round-the-clock operability of Electronic terminals/Smart-terminals; if a Bank terminal fails, provide a working replacement within 3 working days of receiving the Enterprise's request via Bank support phone numbers",
    "Contract 5.2.7: Bank shall ensure round-the-clock operability of Electronic terminals (without mentioning Smart-terminals); replacement within 3 working days",
    discrepancies=[{
        "type": "scope",
        "description": "Matrix covers both Electronic terminals and Smart-terminals for 24/7 operability and replacement obligations; contract 5.2.7 covers only Electronic terminals, omitting Smart-terminals",
        "risk": "The Bank's obligation to ensure Smart-terminal operability and timely replacement is not explicitly stated, potentially allowing the Enterprise to claim the Bank has not met its service-level obligations for Smart-terminal devices."
    }],
    element_checklist=[
        {"element": "party", "result": "same", "note": "Bank obligated; Enterprise benefited"},
        {"element": "legal_object", "result": "different", "note": "matrix: Electronic terminals and Smart-terminals; contract: Electronic terminals only; gap: Smart-terminals omitted from operability/replacement duty"},
        {"element": "operative_right_or_duty", "result": "same", "note": "Bank duty to maintain operability and replace"},
        {"element": "trigger", "result": "same", "note": "terminal failure and Enterprise request"},
        {"element": "deadline", "result": "same", "note": "3 working days for replacement"},
        {"element": "amount_formula_cap", "result": "not_applicable", "note": ""},
        {"element": "procedure_channel", "result": "same", "note": "support phone numbers"},
        {"element": "liability_remedy", "result": "not_applicable", "note": ""},
        {"element": "scope_exceptions", "result": "different", "note": "matrix: both terminal types; contract: Smart-terminals not covered"},
        {"element": "consequence", "result": "same", "note": "working replacement provided"}
    ],
    status_reason="Contract 5.2.7 narrows the Bank's operability and replacement obligation by omitting Smart-terminals. The scope of covered devices is narrower than the matrix standard.",
    analogue_strength="partial")

# 5.2.8
add_aligned_1to1("5.2.8", "5.2.8",
    "Bank obligation to transfer funds within 2 working days after settlement information",
    "Bank shall transfer Operation amounts to the Enterprise's settlement account within 2 working days of receiving settlement information (after electronic reconciliation); in case of technical failure, within 3 calendar days after the last successful reconciliation",
    "Contract 5.2.8: identical provision including the date definition and technical failure fallback")

# 5.2.9
add_aligned_1to1("5.2.9", "5.2.9",
    "Bank obligation to provide QR-code via electronic channels or on paper",
    "Bank shall provide the Enterprise with a partner QR-code via electronic communication channels in electronic form or on paper (trade_acquiring, QR payment method)",
    "Contract 5.2.9: identical provision")

# 5.2.10
add_aligned_1to1("5.2.10", "5.2.10",
    "Bank obligation to process personal data per 152-FZ and ensure confidentiality",
    "Bank shall process personal data received from the Enterprise and ensure confidentiality and protection of processed personal data in accordance with Federal Law No. 152-FZ, including legal, organizational, and technical measures",
    "Contract 5.2.10: identical provision")

# 5.2.12 — MISSING
add_missing("5.2.12",
    "Bank obligation to provide QR-API (including all information-technology interaction via such API) 'as is' without any warranties (internet_acquiring, QR payment method)",
    "Without this clause, the Bank's provision of QR-API lacks the explicit 'as is' disclaimer and warranty exclusion. The Bank may face claims regarding API quality, fitness for purpose, or availability that the matrix standard expressly excludes. This exposes the Bank to liability for API performance issues.",
    rejected_candidates=[
        {
            "contract_id": "5.2.9",
            "reason": "Contract 5.2.9 covers QR-code provision but does not address QR-API provision or the 'as is' warranty disclaimer. Different legal object: QR-code delivery vs. API platform provision."
        },
        {
            "contract_id": "5.2.11",
            "reason": "Contract 5.2.11 covers Mobile application installation — a different technology channel unrelated to QR-API provision."
        }
    ])

# ============================================================
# GROUP 5: 6.1 - 6.9 (Payment for Bank services)
# ============================================================

# 6.1
add_aligned_1to1("6.1", "6.1",
    "Enterprise pays Bank a percentage fee from operation amounts",
    "Enterprise shall pay the Bank a fee in the amount of (____) percent of the sum of payment Operations",
    "Contract 6.1: Enterprise shall pay the Bank a fee as a percentage of each payment Operation, with blank percentage fields — formal difference only")

# 6.2 — DEVIATION: VAT treatment
add_deviation_1to1("6.2", "6.2",
    "Bank sends UPD by 5th working day; fee includes VAT",
    "Bank shall send UPD by the 5th working day of the month following the reporting month; Bank remuneration under 6.1 includes VAT at the rate established by Russian law",
    "Contract 6.2: Bank shall send UPD by the 5th working day; Bank remuneration under 6.1 is NOT subject to VAT under Art. 149(3) of the Russian Tax Code",
    discrepancies=[{
        "type": "amount",
        "description": "Matrix: Bank remuneration includes VAT at the statutory rate (VAT is added on top or included in the rate). Contract: Bank remuneration is exempt from VAT under Art. 149(3) of the Russian Tax Code. The tax treatment of the Bank's fee is fundamentally different.",
        "risk": "If the Bank's standard pricing model assumes VAT applicability (e.g., VAT-registered merchants can deduct input VAT), the VAT exemption changes the economic value of the fee. The Bank may receive a different net amount than anticipated, and the Enterprise's VAT recovery position is altered. This may affect pricing negotiations and the Bank's revenue model."
    }],
    element_checklist=[
        {"element": "party", "result": "same", "note": "Bank sends; Enterprise receives"},
        {"element": "legal_object", "result": "same", "note": "UPD for Bank service fees"},
        {"element": "operative_right_or_duty", "result": "same", "note": "Bank duty to send UPD"},
        {"element": "trigger", "result": "same", "note": "monthly, after reporting month"},
        {"element": "deadline", "result": "same", "note": "5th working day"},
        {"element": "amount_formula_cap", "result": "different", "note": "matrix: fee includes VAT; contract: fee exempt from VAT under Art. 149(3) Tax Code; gap: tax treatment materially different"},
        {"element": "procedure_channel", "result": "same", "note": "UPD delivery"},
        {"element": "liability_remedy", "result": "not_applicable", "note": ""},
        {"element": "scope_exceptions", "result": "same", "note": "same scope"},
        {"element": "consequence", "result": "different", "note": "matrix: VAT-inclusive fee; contract: VAT-exempt fee; gap: different economic result for both parties"}
    ],
    status_reason="Contract 6.2 changes the VAT treatment of the Bank's remuneration from VAT-inclusive to VAT-exempt under Art. 149(3) of the Tax Code. This is a material difference in the amount/formula element.",
    analogue_strength="partial")

# 6.3
add_aligned_1to1("6.3", "6.3",
    "Bank sends Act + form 363 invoice by 10th working day; fee per 6.1, no VAT (fz_223)",
    "Bank shall send Act (per Appendix 2) and form 363 invoice by the 10th working day; remuneration per 6.1, not subject to VAT under Art. 149(3) Tax Code (fz_223 lot)",
    "Contract 6.3: identical provision")

# 6.4
add_aligned_1to1("6.4", "6.4",
    "Enterprise must return signed UPD or motivated refusal by 25th",
    "Enterprise shall return signed UPD or provide a motivated refusal to sign by the 25th day of the month following the reporting month",
    "Contract 6.4: identical provision")

# 6.5
add_aligned_1to1("6.5", "6.5",
    "Enterprise pays within 5 working days of UPD signing, cashless",
    "Enterprise shall pay for Bank services within 5 working days of UPD signing, by cashless transfer to the Bank account specified in the UPD",
    "Contract 6.5: identical provision")

# 6.6
add_aligned_1to1("6.6", "6.6",
    "Enterprise pays within 5 working days of receiving Act + form 363 invoice (fz_223)",
    "Enterprise shall pay for Bank services within 5 working days of receiving the Act and form 363 invoice, by cashless transfer (fz_223 lot)",
    "Contract 6.6: identical provision")

# 6.7
add_aligned_1to1("6.7", "6.7",
    "Monthly service fee per Electronic terminal including VAT (trade_acquiring, smart)",
    "Enterprise shall pay a monthly service fee of _____ RUB (including VAT) for each Electronic terminal (trade_acquiring, smart terminal)",
    "Contract 6.7: Bank shall charge a monthly service fee of _____ RUB (including VAT) for each Electronic terminal — formal difference in phrasing (Enterprise pays vs. Bank charges), same legal result")

# 6.8
add_aligned_1to1("6.8", "6.8",
    "Bank sends UPD for service fee by 5th working day (trade_acquiring, smart)",
    "Bank shall send UPD for the service fee amount for Electronic terminals by the 5th working day of the month following the reporting month (trade_acquiring, smart terminal)",
    "Contract 6.8: identical provision")

# 6.9
add_aligned_1to1("6.9", "6.9",
    "Bank sends form 363 invoice for service fee by 10th working day (trade_acquiring, smart, fz_223)",
    "Bank shall send form 363 invoice for the service fee amount for Electronic terminals by the 10th working day; invoice per tax legislation (trade_acquiring, smart terminal, fz_223 lot)",
    "Contract 6.9: identical provision")

# ============================================================
# CONTRACT-ONLY: 5.2.11
# ============================================================

add_extra_contract("5.2.11",
    "Bank obligation to provide the Enterprise with the ability to install the Mobile Application for Enterprises on the Enterprise's Mobile Device",
    "This creates an independent Bank obligation not present in the matrix standard. The Bank must ensure the Enterprise can install its mobile application, which may involve technical support, compatibility obligations, and potential liability if the application cannot be installed or functions improperly on the Enterprise's device.",
    "Contract 5.2.11 creates a standalone Bank duty to enable mobile application installation on Enterprise devices. The matrix has no analogue for this specific obligation. This is an additional operational commitment that may create support burdens and liability exposure for the Bank.")

# ============================================================
# Write output
# ============================================================

fragment = {
    "batch": "batch_3",
    "batch_ids": ["5.1.8.5","5.1.8.6","5.1.8.7","5.1.8.8","5.1.8.9","5.1.8.10","5.1.8.11","5.1.8.12","5.1.8.13","5.1.9","5.1.10","5.1.11","5.1.12","5.1.13","5.1.14","5.1.15","5.1.16","5.1.17.1","5.1.17.2","5.2.1","5.2.2","5.2.3","5.2.4","5.2.5","5.2.6","5.2.7","5.2.8","5.2.9","5.2.10","5.2.12","6.1","6.2","6.3","6.4","6.5","6.6","6.7","6.8","6.9"],
    "links": links,
    "atomic_links": atomic_links,
    "unmatched_matrix": unmatched_matrix,
    "unmatched_contract": unmatched_contract
}

with open('outputs/working/batch3_fragment.json', 'w', encoding='utf-8') as f:
    json.dump(fragment, f, ensure_ascii=False, indent=2)

print(f"Batch 3 fragment written:")
print(f"  links: {len(links)}")
print(f"  atomic_links: {len(atomic_links)}")
print(f"  unmatched_matrix: {len(unmatched_matrix)}")
print(f"  unmatched_contract: {len(unmatched_contract)}")

# Verify coverage
all_batch = set(["5.1.8.5","5.1.8.6","5.1.8.7","5.1.8.8","5.1.8.9","5.1.8.10","5.1.8.11","5.1.8.12","5.1.8.13","5.1.9","5.1.10","5.1.11","5.1.12","5.1.13","5.1.14","5.1.15","5.1.16","5.1.17.1","5.1.17.2","5.2.1","5.2.2","5.2.3","5.2.4","5.2.5","5.2.6","5.2.7","5.2.8","5.2.9","5.2.10","5.2.12","6.1","6.2","6.3","6.4","6.5","6.6","6.7","6.8","6.9"])
in_links = set()
for l in links:
    in_links.update(l["matrix_ids"])
in_unmatched = set(m["matrix_id"] for m in unmatched_matrix)
covered = in_links | in_unmatched
missing = all_batch - covered
if missing:
    print(f"  WARNING: Uncovered matrix ids: {missing}")
else:
    print(f"  All {len(all_batch)} matrix ids covered")

# Verify deviations have discrepancies
for al in atomic_links:
    if al["relationship"] == "deviation":
        if not al["discrepancies"]:
            print(f"  WARNING: deviation pair {al['matrix_id']}+{al['contract_id']} has no discrepancies")
        has_diff = any(e["result"] in ("different", "missing") for e in al["element_checklist"])
        if not has_diff:
            print(f"  WARNING: deviation pair {al['matrix_id']}+{al['contract_id']} has no different/missing checklist items")
