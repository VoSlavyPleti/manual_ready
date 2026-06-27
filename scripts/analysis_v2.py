import json

# Build the comprehensive analysis

analysis = {
  "analysis_profile": {
    "product": ["trade_acquiring"],
    "legal_regime": "44_fz"
  },
  "links": [],
  "unmatched_matrix": [],
  "unmatched_contract": [],
  "coverage_ledger": {
    "matrix": [],
    "contract": []
  },
  "summary": {
    "aligned_count": 0,
    "deviation_count": 0,
    "missing_in_contract_count": 0,
    "extra_in_contract_count": 0
  }
}

L = analysis["links"]
UM = analysis["unmatched_matrix"]
UC = analysis["unmatched_contract"]
CLM = analysis["coverage_ledger"]["matrix"]
CLC = analysis["coverage_ledger"]["contract"]
S = analysis["summary"]

def add_aligned(contract_ids, matrix_ids, reason, risk="none"):
    L.append({
        "contract_ids": contract_ids,
        "matrix_ids": matrix_ids,
        "relationship": "aligned",
        "status_reason": reason,
        "risk_level": risk,
        "discrepancies": []
    })
    S["aligned_count"] = S["aligned_count"] + 1
    for m_id in matrix_ids:
        if not any(x.get("matrix_id") == m_id and x.get("closure") == "linked" for x in CLM):
            CLM.append({"matrix_id": m_id, "closure": "linked", "reason": "linked via aligned"})
    for c_id in contract_ids:
        if not any(x.get("contract_id") == c_id and x.get("closure") == "linked" for x in CLC):
            CLC.append({"contract_id": c_id, "closure": "linked", "reason": "linked via aligned"})

def add_deviation(contract_ids, matrix_ids, reason, risk, discrepancies):
    L.append({
        "contract_ids": contract_ids,
        "matrix_ids": matrix_ids,
        "relationship": "deviation",
        "status_reason": reason,
        "risk_level": risk,
        "discrepancies": discrepancies
    })
    S["deviation_count"] = S["deviation_count"] + 1
    for m_id in matrix_ids:
        if not any(x.get("matrix_id") == m_id and x.get("closure") == "linked" for x in CLM):
            CLM.append({"matrix_id": m_id, "closure": "linked", "reason": "linked via deviation"})
    for c_id in contract_ids:
        if not any(x.get("contract_id") == c_id and x.get("closure") == "linked" for x in CLC):
            CLC.append({"contract_id": c_id, "closure": "linked", "reason": "linked via deviation"})

def add_missing(matrix_id, requirement, req_type, risk_level, risk_text):
    UM.append({
        "matrix_id": matrix_id,
        "status": "missing_in_contract",
        "requirement": requirement,
        "required_type": req_type,
        "risk_level": risk_level,
        "risk": risk_text
    })
    S["missing_in_contract_count"] = S["missing_in_contract_count"] + 1
    CLM.append({"matrix_id": matrix_id, "closure": "missing_in_contract", "reason": "no true analogue found"})

def add_extra(contract_id, contract_position, risk_level, risk, materiality):
    UC.append({
        "contract_id": contract_id,
        "status": "extra_in_contract",
        "contract_position": contract_position,
        "risk_level": risk_level,
        "risk": risk,
        "materiality_reason": materiality
    })
    S["extra_in_contract_count"] = S["extra_in_contract_count"] + 1
    CLC.append({"contract_id": contract_id, "closure": "extra_in_contract", "reason": "no matrix analogue"})

def add_matrix_closure(matrix_id, closure, reason):
    CLM.append({"matrix_id": matrix_id, "closure": closure, "reason": reason})

def add_contract_closure(contract_id, closure, reason):
    CLC.append({"contract_id": contract_id, "closure": closure, "reason": reason})

# ============ SECTION 2: TERMS, DEFINITIONS, INTERACTION ============

add_deviation(
    ["4.3"],
    ["2.1"],
    "Contract requires TST registration via application and info form, but Bank's right to refuse registration without explanation is omitted",
    "high",
    [{"type": "procedure", "description": "Matrix gives Bank right to refuse TST registration 'без объяснения причин'. Contract 4.3 has no such right.", "risk": "Bank loses unconditional right to refuse TST registration; must register every TST presented."}]
)

add_aligned(
    ["Приложение №1 п.5 (Расчеты при совершении операций)", "5.1.8"],
    ["2.2"],
    "Contract Приложение №1 п.5: 'Расчеты при совершении операций производятся в валюте Российской Федерации'; 5.1.8 confirms RUB transfers"
)

add_aligned(
    ["2.3.1"],
    ["2.3.1"],
    "Contract 2.3.1 mirrors matrix: email exchange with legal force, exclusion of personal data/commercial/bank secrets from email"
)

add_aligned(
    ["2.3.2"],
    ["2.3.2"],
    "Contract 2.3.2 mirrors matrix: exchange via DBO or analogous Bank systems"
)

add_aligned(
    ["2.3.3"],
    ["2.3.3"],
    "Contract 2.3.3 mirrors matrix: courier/personal delivery"
)

add_aligned(
    ["2.3.4"],
    ["2.3.4"],
    "Contract 2.3.4 mirrors matrix: registered mail"
)

add_deviation(
    ["2.3.5"],
    ["2.3.5"],
    "Contract 2.3.5 has blank '_________________' for automated system name instead of 'E-invoicing/СФЕРА-Курьер'",
    "low",
    [{"type": "other", "description": "Matrix specifies 'E-invoicing/СФЕРА-Курьер'; Contract 2.3.5 leaves system name blank.", "risk": "Blank system name creates uncertainty about which EDI operator will be used; UCEP and legal equivalence provisions preserved."}]
)

add_aligned(
    ["2.3.6"],
    ["2.3.6"],
    "Contract 2.3.6 mirrors matrix: EIS and electronic trading platforms exchange with UCEP, legal equivalence"
)

add_deviation(
    ["2.3.7"],
    ["2.3.7"],
    "Contract 2.3.7 exists but receipt date rules differ: matrix references specific EDI operator subsidiary, contract uses generic reference; matrix СФЕРА-Курьер operator differs from contract's blank/generic operator",
    "low",
    [{"type": "procedure", "description": "Matrix 2.3.7 receipt rules reference ООО «КОРУС Консалтинг СНГ» (Bank subsidiary). Contract has generic 'Оператор электронного документооборота (дочерней компании Банка)'.", "risk": "Operator identification differs; matrix names specific subsidiary. Low operational risk as receipt mechanism preserved."}]
)

add_deviation(
    ["1.1", "12.5"],
    ["2.4"],
    "Contract 1.1 states appendices are integral parts but no standalone clause equivalent to matrix 2.4 making all referenced documents integral parts of the contract",
    "low",
    [{"type": "scope", "description": "Matrix 2.4: 'Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.' Contract 1.1 makes specific appendices integral but not all referenced documents.", "risk": "Documents referenced but not attached may lack binding force; key appendices covered by 1.1."}]
)

add_matrix_closure("2.5.1.1", "out_of_scope", "internet_acquiring only; contract is trade_acquiring")
add_matrix_closure("2.5.2.1", "not_applicable", "SberPayFaceScan/biometrics not selected in contract; application form biometrics checkbox unchecked")

add_deviation(
    ["Приложение №1 п.5 (Возможность вывода QR-кода)"],
    ["2.6.1.1"],
    "Contract indicates QR capability on terminals as technical requirement but does not explicitly state QR connects automatically upon smart terminal installation",
    "low",
    [{"type": "procedure", "description": "Matrix 2.6.1.1: QR connects automatically when Bank's Smart terminal or software is installed. Contract only has technical QR capability listing.", "risk": "Without automatic connection clause, QR activation may require separate steps."}]
)

add_matrix_closure("2.6.2.1", "not_applicable", "Requires Customer's own KKT software with QR-API integration; contract uses Bank-provided terminals")
add_matrix_closure("2.6.2.2", "not_applicable", "Requires Customer's own KKT software without QR needing Vendor development; contract uses Bank terminals")

add_deviation(
    ["Приложение №1 п.5 (Возможность вывода QR-кода)"],
    ["2.6.3.1"],
    "Contract mentions QR code display capability but does not state QR connects upon electronic terminal installation as matrix requires",
    "low",
    [{"type": "procedure", "description": "Matrix 2.6.3.1: QR connects when electronic terminal installed (Bank as Vendor). Contract has QR as technical requirement without automatic connection language.", "risk": "Technical requirement covers capability but not automatic connection procedure."}]
)

add_missing("2.6.3.2", "Procedure for Customer-initiated QR code disconnection via contacting Bank through specified channels (2.3.1-2.3.4, 2.3.7)", "mandatory", "low", "No contractual procedure for disconnecting QR code at Customer's initiative")

add_aligned(["12.4"], ["2.7"], "Contract 12.4: electronic form signed with UCEP, equivalent to matrix 2.7")

# ============ SECTION 3: SUBJECT MATTER ============

add_aligned(["1.1", "1.3"], ["3.1"], "Contract 1.1 and 1.3: Customer organizes card acceptance and processes information on electronic terminals")
add_aligned(["5.1.8", "5.1.10"], ["3.2"], "Contract 5.1.8 and 5.1.10: Bank transfers operation amounts to Customer")
add_aligned(["3.2", "4.4"], ["3.3"], "Contract 3.2 and 4.4: Customer pays Bank commission as percentage of each operation, monthly payment structure")

# ============ SECTION 4: CUSTOMER RIGHTS AND OBLIGATIONS ============

add_deviation(
    ["5.4.5"],
    ["4.1.1"],
    "Matrix covers Cards/QR-code ad references with approval via specific channels (2.3.1/2.3.2); Contract 5.4.5 mentions only cards, no specific approval channels",
    "low",
    [{"type": "scope", "description": "Matrix covers Cards/QR-code; Contract 5.4.5 mentions only cards without QR. Matrix requires approval via email/DBO channels; Contract says 'предварительно согласовав' without channel specification.", "risk": "QR-code not covered in ad approval right; channel specification omitted."}]
)

add_aligned(["5.9"], ["4.1.2"], "Contract 5.9: Customer entitled to Bank consultations on terminal operation and card transactions via support service")

add_deviation(
    ["Приложение №1 п.5 (Возможность вывода QR-кода)"],
    ["4.1.3"],
    "Matrix grants right to use Bank-provided QR codes; Contract has QR as technical specification, not as explicit right",
    "low",
    [{"type": "scope", "description": "Matrix grants right to use Bank-provided QR codes on terminals/devices. Contract states QR display as technical requirement without explicit right grant.", "risk": "No explicit contractual right to use Bank-provided QR codes."}]
)

add_aligned(["3.2", "4.4"], ["4.2.1"], "Contract 3.2, 4.4: Customer obligated to pay for Bank services")

add_deviation(
    ["5.3.10"],
    ["4.2.2"],
    "Matrix requires explicit obligation to comply with contract terms AND Bank instructional materials; Contract 5.3.10 covers operations/documentation per contract rules but no standalone clause binding Customer to all Bank instructional materials",
    "medium",
    [{"type": "liability", "description": "Matrix 4.2.2: explicit obligation to 'соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/инструктивных материалах'. Contract lacks standalone clause; 5.3.10 is narrower (operations/documentation only).", "risk": "Without explicit obligation to follow all Bank instructional materials, enforcement position for operational rule violations is weaker."}]
)

add_matrix_closure("4.2.3", "out_of_scope", "fz_223 only; contract is 44_fz")

add_aligned(["5.3.7"], ["4.2.4"], "Contract 5.3.7: display Bank-provided informational materials at TST about card acceptance")

add_deviation(
    ["5.3.8", "5.3.9"],
    ["4.2.5"],
    "Matrix prohibits (1) issuing cash via cards, (2) accepting more than 2 different cards from one buyer. Contract covers bill splitting (5.3.8) and card data misuse (5.3.9) but omits cash disbursement prohibition and max-2-cards rule.",
    "medium",
    [
        {"type": "scope", "description": "Matrix rule missing: prohibition on issuing cash via cards. Contract silent.", "risk": "Cash disbursement via cards creates fraud and regulatory risk."},
        {"type": "scope", "description": "Matrix rule missing: no more than 2 different cards from one buyer. Contract silent.", "risk": "Accepting 3+ cards from one buyer enables transaction structuring."}
    ]
)

add_aligned(["5.3.8"], ["4.2.6"], "Contract 5.3.8 explicitly prohibits splitting one operation amount into multiple operations")
add_aligned(["5.3.9"], ["4.2.7"], "Contract 5.3.9 prohibits using card details for purposes other than operations at buyer's direction")

add_missing("4.2.8", "Customer must provide full range of goods/services at prices not exceeding cash prices", "mandatory", "medium", "No clause requiring equal pricing for card vs cash payments. Payment system rule violation risk.")

add_aligned(["5.3.10"], ["4.2.9"], "Contract 5.3.10: conduct operations per contract, bear responsibility for information accuracy")

add_deviation(
    ["5.3.11"],
    ["4.2.10"],
    "Contract 5.3.11 covers storage (13 months) and copy provision (3 working days) but matrix requires copy transmission via specific electronic channels (2.3.1, 2.3.2). Contract does not specify transmission channel.",
    "low",
    [{"type": "procedure", "description": "Matrix 4.2.10 requires copy transmission via email/DBO channels. Contract 5.3.11 omits transmission channel specification.", "risk": "Ambiguity about acceptable transmission method for copy provision."}]
)

add_aligned(["5.3.12", "5.5"], ["4.2.11"], "Contract 5.3.12 and 5.5: written statement on operations within 3 working days, immediate loss notification")

add_deviation(
    ["8.5.1"],
    ["4.2.12"],
    "Matrix 4.2.12 requires acceptance of payment claims within 5 working days. Contract 8.5.1 provides 10 working days for acceptance document via EIS.",
    "medium",
    [{"type": "deadline", "description": "Matrix: 5 working days. Contract: 10 working days.", "risk": "Longer acceptance period delays payment finalization."}]
)

add_aligned(["5.3.19"], ["4.2.13"], "Contract 5.3.19: full indemnification for amounts debited from Bank, dispute costs, and Bank's losses from Customer non-performance")
add_aligned(["5.3.13"], ["4.2.14"], "Contract 5.3.13: notify Bank of reorganization, changes, bankruptcy, management change, address/rekvizity changes within 3 working days")
add_aligned(["5.3.14"], ["4.2.15"], "Contract 5.3.14: provide reliable documents at least annually and within 7 working days of Bank request, including beneficial owner info")
add_aligned(["5.3.20"], ["4.2.16.1"], "Contract 5.3.20: Customer guarantees legal basis for transfer of manager's PD (FIO, address, passport) to Bank and MIR payment system")

add_missing("4.2.16.2", "Customer must guarantee consent for processing employee PD (FIO, phone, email, position, workplace) and transfer to Service Companies acting on Bank's behalf", "mandatory", "medium", "Contract 5.3.20 covers only manager PD, not employees. Employee PD consent for Service Companies is missing.")

add_missing("4.2.16.3", "Customer must provide confirmation of PD consent within 3 working days of Bank's written request; indemnify Bank for all claims and losses from non-provision", "mandatory", "medium", "Contract 5.3.15 covers confirmation obligation and indemnification but does not set the specific 3-working-day deadline.")

add_matrix_closure("4.2.17", "out_of_scope", "internet_acquiring only; contract is trade_acquiring")

add_aligned(["5.3.16"], ["4.2.18"], "Contract 5.3.16: upon termination, stop card acceptance, remove informational materials")
add_aligned(["5.3.17"], ["4.2.19"], "Contract 5.3.17: not obstruct Bank inspections, assist suspicious operation investigations")

add_deviation(
    ["5.10"],
    ["4.2.20.1"],
    "Matrix specifies training materials at sberbank.ru; Contract 5.10 has blank URL placeholder ('______________________________')",
    "low",
    [{"type": "other", "description": "Matrix specifies URL: https://www.sberbank.ru/help/business/acquiring. Contract 5.10: blank URL.", "risk": "Blank URL creates uncertainty about training material location."}]
)

add_aligned(["5.3.18.1"], ["4.2.20.2"], "Contract 5.3.18.1: use terminals only for contract purposes, no modifications, no self-repair, no transfer to third parties")
add_aligned(["5.3.18.2"], ["4.2.20.3"], "Contract 5.3.18.2: provide access for terminal connection, setup, repair, replacement, maintenance, inspection")
add_aligned(["5.3.18.3"], ["4.2.20.4"], "Contract 5.3.18.3: accept terminals by act in 2 copies signed by both parties")
add_aligned(["5.3.20.4"], ["4.2.20.5"], "Contract 5.3.20.4: immediately inform Bank of terminal failure or loss")

add_aligned(["5.3.18.5", "5.6"], ["4.2.20.6"], "Contract 5.3.18.5 and 5.6: return terminals within 5 working days of termination or Bank's demand")

add_deviation(
    ["5.7"],
    ["4.2.20.7"],
    "Matrix: 25,000 RUB penalty for each electronic terminal and smart terminal. Contract 5.7: 10,000 RUB per electronic terminal, 25,000 RUB per smart terminal.",
    "medium",
    [{"type": "amount", "description": "Matrix: 25,000 RUB each. Contract: 10,000 RUB (electronic), 25,000 RUB (smart).", "risk": "Electronic terminal penalty reduced by 60%, weakening Bank's equipment return leverage."}]
)

for mid in ["4.2.21.1","4.2.21.2","4.2.21.3","4.2.21.4","4.2.21.5","4.2.21.6","4.2.21.7","4.2.21.8"]:
    add_matrix_closure(mid, "out_of_scope", "internet_acquiring only")

add_missing("4.2.22", "Customer must provide QR code to buyer for SberPayQR/Плати QR payment", "optional", "low", "No explicit obligation to provide QR code to buyer; QR listed only as technical requirement")
add_missing("4.2.23", "Customer must not unilaterally change partner QR code", "optional", "low", "No prohibition on unilateral QR code modification")
add_matrix_closure("4.2.24", "not_applicable", "QR-API not activated in contract")
add_matrix_closure("4.2.25", "not_applicable", "QR-API not activated in contract")
add_matrix_closure("4.2.26", "out_of_scope", "internet_acquiring only")

# ============ SECTION 5: BANK RIGHTS AND OBLIGATIONS ============

add_aligned(["5.2.10", "5.2.10.1"], ["5.1.1.1"], "Contract 5.2.10/5.2.10.1: Bank right to withhold invalid operation amounts with matching grounds list")
add_aligned(["5.2.10.2"], ["5.1.1.2"], "Contract 5.2.10.2: withhold erroneously transferred amounts")
add_aligned(["5.2.10.3"], ["5.1.1.3"], "Contract 5.2.10.3: withhold return operations, chargebacks, reversals")
add_aligned(["5.2.10.4"], ["5.1.1.4"], "Contract 5.2.10.4: withhold disputed/charged-back operations and agent sales amounts")
add_aligned(["5.2.10.5"], ["5.1.1.5"], "Contract 5.2.10.5: withhold fines/losses from payment system sanctions and liability due to Customer")
add_aligned(["5.2.10", "5.7"], ["5.1.1.6"], "Contract 5.2.10 read with 5.7: Bank right to withhold terminal non-return penalty")

add_missing("5.1.2", "Bank may suspend authorization until full repayment of Customer's debt", "mandatory", "high", "Contract 5.2.9 allows suspension for various violations but not solely for indebtedness until full repayment. Critical collection leverage missing.")

add_deviation(
    ["Приложение №1.1 п.1.3"],
    ["5.1.3"],
    "Contract appendix provides direct debit consent (заранее данный акцепт) but limited to specified sums. Matrix covers broader direct debit from Customer's Bank account when withholding from future transfers is impossible.",
    "low",
    [{"type": "scope", "description": "Matrix 5.1.3: direct debit from Customer's account at Bank when withholding from transfers impossible. Contract appendix 1.1.3: consent limited to sums in 5.1.1.", "risk": "Scope may be narrower than matrix but core mechanism preserved."}]
)

add_missing("5.1.4", "When withholding from future transfers is impossible, Bank issues payment claim/invoice to Customer's account at specified bank", "mandatory", "medium", "No explicit procedure for issuing payment claims to external bank account when internal withholding fails.")

add_missing("5.1.5", "Bank may not reimburse amounts for operations conducted in violation of contract terms", "mandatory", "high", "No explicit Bank right to refuse reimbursement for violating operations. Key Bank protection missing.")

add_aligned(["5.2.3", "5.2.4"], ["5.1.6"], "Contract 5.2.3/5.2.4: Bank may check/replace/update terminals; 2-day notice for replacement; remote updates without notice if not affecting operations")

add_missing("5.1.7", "Bank may transfer info including PD of manager/representative to MIR payment system for suspicious/fraudulent operations and upon termination for fraud", "mandatory", "high", "No provision allowing Bank to transfer Customer/manager data to MIR for fraud investigation. 5.3.20 PD consent limited to contract execution purposes.")

add_aligned(["5.2.9", "5.2.9.1"], ["5.1.8.1"], "Contract 5.2.9.1: termination for Customer contract violation")
add_aligned(["5.2.9.2"], ["5.1.8.2"], "Contract 5.2.9.2: termination for extremist/terrorist list inclusion")
add_aligned(["5.2.9.3"], ["5.1.8.3"], "Contract 5.2.9.3: termination for money laundering/terrorism financing suspicion")

add_matrix_closure("5.1.8.4", "out_of_scope", "internet_acquiring only")
add_matrix_closure("5.1.8.5", "out_of_scope", "internet_acquiring only")

add_aligned(["5.2.9.4"], ["5.1.8.6"], "Contract 5.2.9.4: termination for negative info from state authorities or payment systems")
add_aligned(["5.2.9.5"], ["5.1.8.7"], "Contract 5.2.9.5: termination for fraud info in TST; sufficient confirmation from issuer banks/payment systems")
add_aligned(["5.2.9.6"], ["5.1.8.8"], "Contract 5.2.9.6: termination for TST renovation preventing operations")
add_aligned(["5.2.9.7"], ["5.1.8.9"], "Contract 5.2.9.7: termination for Customer liquidation or bankruptcy")
add_aligned(["5.2.9.8"], ["5.1.8.10"], "Contract 5.2.9.8: termination for false info about Customer/TST/management")
add_aligned(["5.2.9.9"], ["5.1.8.11"], "Contract 5.2.9.9: termination for goods/services vs declared business activity mismatch")
add_aligned(["5.2.9.10"], ["5.1.8.12"], "Contract 5.2.9.10: termination for no operations for 30 calendar days")
add_aligned(["5.2.9.11"], ["5.1.8.13"], "Contract 5.2.9.11: termination for price exhaustion or contract expiration")

add_missing("5.1.9", "Bank may conduct additional checks of operations in TST, including contacting issuer bank to verify operation legitimacy", "mandatory", "medium", "Contract 5.2.5 allows document requests but lacks explicit right to contact issuer banks for additional verification.")

add_deviation(
    ["5.2.3", "5.3.17"],
    ["5.1.10"],
    "Matrix 5.1.10 grants broad inspection right including fraud detection, activity mismatch, contract compliance. Contract 5.2.3 is limited to technical terminal inspection; 5.3.17 covers cooperation but not independent Bank inspection right.",
    "low",
    [{"type": "scope", "description": "Matrix: comprehensive inspection right. Contract: technical inspection (5.2.3) + cooperation duty (5.3.17) but no independent broad inspection right.", "risk": "Bank's inspection scope limited to terminal checks rather than full operational audit."}]
)

add_aligned(["5.2.5"], ["5.1.11"], "Contract 5.2.5: Bank may request operation documents within 13 months of operation date")

add_missing("5.1.12", "Bank may unilaterally modify documents referenced in contract by publishing on Official Bank website at least 1 calendar day before changes take effect", "optional", "medium", "Contract 11.4 requires written bilateral agreement for all changes; no Bank unilateral modification right for referenced documents.")

add_deviation(
    ["5.2.6"],
    ["5.1.13"],
    "Matrix requires Bank detail change notification via website. Contract 5.2.6 requires written notification within 3 working days.",
    "low",
    [{"type": "procedure", "description": "Matrix: website publication. Contract: written notification within 3 working days.", "risk": "Written notification more burdensome for Bank but more reliable for Customer."}]
)

add_aligned(["5.2.7"], ["5.1.14"], "Contract 5.2.7: Bank may send operation info requests to Customer/TST email from application")

add_missing("5.1.15", "Bank may refuse to conclude contract without explanation", "optional", "low", "Incompatible with 44-FZ procurement regime where Bank cannot refuse after winning procedure; regime-specific gap.")

add_aligned(["5.2.8"], ["5.1.16"], "Contract 5.2.8: Bank may demand documents/information necessary for functions under applicable law")

add_missing("5.1.17.1", "Bank may unilaterally terminate and demand terminal return if POS terminal turnover below 40,000 RUB/month (80,000 for Moscow/SPb)", "optional", "medium", "No turnover-based termination right for POS terminals.")

add_missing("5.1.17.2", "Bank may unilaterally terminate and demand terminal return if smart terminal turnover below 40,000 RUB/month (80,000 for Moscow/SPb) or service fee debt exists", "optional", "medium", "No turnover-based termination right for smart terminals.")

add_matrix_closure("5.2.1", "out_of_scope", "internet_acquiring only")
add_matrix_closure("5.2.2", "out_of_scope", "internet_acquiring only")

add_aligned(["5.1.1"], ["5.2.3"], "Contract 5.1.1: install and prepare terminals within 5 working days, conduct initial staff training")
add_aligned(["5.1.6"], ["5.2.4"], "Contract 5.1.6: Bank provides 24/7 authorization")

add_deviation(
    ["5.1.1 (обучающие материалы)"],
    ["5.2.5"],
    "Matrix specifies URL sberbank.ru/help/business/acquiring for training materials. Contract 5.1.1 has blank URL placeholder.",
    "low",
    [{"type": "other", "description": "Matrix: specified URL. Contract: blank URL placeholder.", "risk": "Blank URL creates uncertainty about training material location."}]
)

add_aligned(["5.1.7"], ["5.2.6"], "Contract 5.1.7: Bank provides informational materials for terminals")
add_aligned(["5.1.4"], ["5.2.7"], "Contract 5.1.4: 24/7 operability, replacement within 3 working days of request")
add_aligned(["5.1.8"], ["5.2.8"], "Contract 5.1.8: transfer within 2 working days of settlement info; settlement info date = working day after electronic reconciliation; 3 calendar days after last reconciliation for technical failure")

add_missing("5.2.9", "Bank provides partner QR code via electronic channels or on paper", "optional", "low", "No explicit Bank obligation to provide QR code; QR listed as terminal technical requirement only")

add_aligned(["5.1.9"], ["5.2.10"], "Contract 5.1.9: Bank processes PD per 152-FZ, ensures confidentiality and protection")
add_matrix_closure("5.2.12", "not_applicable", "QR-API not activated in contract")

# ============ SECTION 6: PAYMENT FOR BANK SERVICES ============

add_aligned(["3.2", "Спецификация"], ["6.1"], "Contract 3.2: price per unit includes Bank commission as % of each operation; Specification confirms structure")

add_deviation(
    ["8.3.1"],
    ["6.2"],
    "Matrix 6.2: Bank sends UPD by 5th working day. Contract 8.3.1: Bank forms acceptance document by 10th working day via EIS.",
    "low",
    [{"type": "deadline", "description": "Matrix: 5th working day. Contract: 10th working day.", "risk": "Later document submission delays acceptance/payment cycle by up to 5 working days."}]
)

add_matrix_closure("6.3", "out_of_scope", "fz_223 only")

add_deviation(
    ["8.5.1", "8.5.7"],
    ["6.4"],
    "Matrix 6.4: Customer returns signed UPD by 25th of month following reporting month. Contract 8.5.1: Customer signs within 10 working days of receiving document. Different timing mechanisms may not align.",
    "low",
    [{"type": "deadline", "description": "Matrix: calendar date (25th). Contract: working days from receipt (10 working days).", "risk": "Different deadline calculation creates timing uncertainty."}]
)

add_aligned(["4.5"], ["6.5"], "Contract 4.5: payment within 7 working days of acceptance document signing; functionally aligned with matrix 6.5 (5 working days from UPD signing)")
add_matrix_closure("6.6", "out_of_scope", "fz_223 only")

add_deviation(
    ["Приложение №1 п.5 (Комиссия/абонентская плата)"],
    ["6.7"],
    "Matrix 6.7 requires monthly service fee per electronic terminal. Contract Приложение №1 п.5: 'Комиссия за предоставление терминалов - отсутствует. Абонентская плата за пользование терминалами - отсутствует.' Zero fees.",
    "high",
    [{"type": "amount", "description": "Matrix: monthly service fee. Contract: zero commission, zero subscription fee.", "risk": "Bank receives no terminal service revenue. Core commercial term eliminated."}]
)

for mid in ["6.8", "6.10", "6.11", "6.13", "6.14", "6.16", "6.17"]:
    add_matrix_closure(mid, "not_applicable", "Contract waives all terminal service fees; fee-related procedures inapplicable")

for mid in ["6.9", "6.12", "6.15", "6.18"]:
    add_matrix_closure(mid, "out_of_scope", "fz_223 only")

add_aligned(
    ["Приложение №1 п.5 (по Операциям возврата)"],
    ["6.20"],
    "Contract mirrors matrix 6.20: no commission on returns/chargebacks/reversals; original commission not refunded"
)

add_aligned(["3.1"], ["6.21"], "Contract 3.1: maximum contract price 1,900,000 RUB")

# ============ SECTION 7: LIABILITY ============

add_aligned(["7.1"], ["7.1"], "Contract 7.1: parties bear liability per contract and Russian law")
add_aligned(["7.4", "7.4.1"], ["7.2"], "Contract 7.4/7.4.1: fines for Customer non-performance (excluding delay) per Resolution No. 1042")
add_aligned(["7.1 (абз.4)"], ["7.3"], "Contract 7.1 para 4: total Customer fines capped at contract price")
add_aligned(["7.5", "7.6"], ["7.4"], "Contract 7.5/7.6: penalty for Bank delay = 1/300 key rate of contract price reduced by performed volume per day")
add_aligned(["7.7", "7.7.1"], ["7.5"], "Contract 7.7/7.7.1: fines for Bank non-performance (excluding delay) per Resolution No. 1042")
add_aligned(["7.7.3"], ["7.6"], "Contract 7.7.3: fines for Bank non-monetary obligations per Resolution No. 1042")
add_aligned(["7.10"], ["7.7"], "Contract 7.10: total Bank fines capped at contract price")

add_missing("7.8", "Bank bears no responsibility for disputes between Customer and buyers not related to contract subject", "optional", "medium", "No explicit exclusion of Bank liability for Customer-buyer disputes.")
add_missing("7.9", "Bank not liable for delays in funds transfer if delays occurred through no fault of Bank", "optional", "medium", "No explicit exclusion for transfer delays beyond Bank's control.")
add_missing("7.10", "Bank not liable for non-performance caused by actions/inactions of third parties including payment system participants", "optional", "low", "No explicit third-party action liability exclusion for Bank.")
add_missing("7.11", "Bank not liable for untimely transfer of operation amounts due to Bank investigation of suspected contract violations", "optional", "medium", "No explicit protection when Bank delays transfers for investigation.")
add_missing("7.12", "Bank not liable in case of exceeding established Contract Price", "optional", "low", "No explicit clause; 44-FZ price cap mechanism provides inherent protection.")

add_matrix_closure("7.13", "out_of_scope", "internet_acquiring only")

add_missing("7.14", "Customer bears full responsibility for all actions conducted by Customer/TST in SPEP", "mandatory", "low", "SPEP not activated in trade acquiring contract; low practical risk")

add_deviation(
    ["7.1"],
    ["7.15"],
    "Matrix 7.15 explicitly states full Customer liability for personnel actions violating contract/instructions. Contract 7.1 has general liability clause without explicit personnel attribution.",
    "medium",
    [{"type": "liability", "description": "Matrix: explicit full liability for personnel. Contract: general liability without personnel-specific clause.", "risk": "Customer may argue not liable for unauthorized employee actions."}]
)

add_aligned(["6.1"], ["7.16"], "Contract 6.1: anti-corruption clause mirrors matrix 7.16")
add_missing("7.17", "Customer bears full financial liability for recurring payments non-compliance with Russian law, CBR regulations, payment system rules", "mandatory", "low", "No recurring payments in trade acquiring contract; low practical risk")

# ============ SECTION 8: FORCE MAJEURE ============

add_aligned(["9.1"], ["8.1"], "Contract 9.1: force majeure definition and exemption from liability")

add_deviation(
    ["9.2"],
    ["8.2"],
    "Matrix 8.2: 24-hour notification, termination right after 3 months. Contract 9.2: 5-day notification, termination right after 1 month.",
    "medium",
    [
        {"type": "deadline", "description": "Matrix: notification within 24 hours. Contract: 5 days.", "risk": "5-day vs 24-hour gap delays Bank's awareness of force majeure."},
        {"type": "deadline", "description": "Matrix: termination after 3 months. Contract: after 1 month.", "risk": "Earlier termination right (1 month vs 3 months) is more favorable to Bank."}
    ]
)

# ============ SECTION 9: DISPUTE RESOLUTION ============

add_aligned(["10.1"], ["9.1"], "Contract 10.1: disputes resolved through negotiations (pre-trial procedure)")
add_aligned(["10.1"], ["9.2"], "Contract 10.1: response to claims within 10 calendar days")
add_aligned(["10.2", "11.7"], ["9.3"], "Contract 10.2: unresolved disputes to Arbitration Court of Krasnodar Krai; 11.7: matters governed by Russian law")

# ============ SECTION 10: TERM AND TERMINATION ============

add_aligned(["11.1"], ["10.1"], "Contract 11.1: effective from signing until 30.12.2025 or price exhaustion; liability survives termination")

add_deviation(
    ["11.3", "11.4", "11.5"],
    ["10.2"],
    "Matrix 10.2: any party may unilaterally terminate with 30 calendar days written notice (except 5.1.8 cases). Contract only allows termination on statutory grounds (agreement, court, 44-FZ/Civil Code grounds). No 30-day no-cause termination right.",
    "high",
    [{"type": "procedure", "description": "Matrix grants flexible 30-day notice termination. Contract: only for-cause termination under 44-FZ/Civil Code.", "risk": "Bank loses flexible exit right; can only terminate for cause. 44-FZ regime inherently limits unilateral termination without cause."}]
)

add_missing("10.3", "Upon unilateral termination by Bank under 5.1.8, contract terminates on date in Bank's notice; parties settle within 18 months; Customer pays per 5.1.3, 5.1.4, Section 6", "mandatory", "medium", "No 18-month post-termination settlement period or specific payment mechanics from matrix 10.3.")

# ============ SECTION 11: MISCELLANEOUS ============

add_deviation(
    ["7.1", "11.7"],
    ["11.1"],
    "Matrix 11.1: governing sources hierarchy includes payment system rules with primacy to align conflicting terms. Contract lacks payment system rule primacy.",
    "medium",
    [{"type": "liability", "description": "Matrix makes payment system rules a governing source and requires alignment. Contract lacks this hierarchy.", "risk": "Compliance gaps possible between contract terms and mandatory payment system requirements."}]
)

add_missing("11.2", "Information received by Customer (card numbers, PD of buyers, operation amounts, payment info) is confidential and not subject to transfer to third parties except as required by law or contract", "optional", "medium", "Contract 5.3.11 covers document storage but lacks explicit confidentiality regime for payment information.")

add_missing("11.3", "Parties undertake not to disclose information including card security features, operation technology, management/financial info, and other info whose disclosure may cause losses or reputational damage", "optional", "medium", "No comprehensive confidentiality clause covering all sensitive commercial information exchanged.")

add_aligned(["11.2"], ["11.4"], "Contract 11.2: changes valid only if in writing signed by both parties")

add_missing("11.5", "All prior agreements, negotiations, and correspondence on contract matters lose force from contract signing date", "optional", "low", "Standard integration clause absent; low risk in 44-FZ context where procurement documentation defines framework.")

add_aligned(["12.4"], ["11.6"], "Contract 12.4: contract in electronic form with UCEP; electronic format makes copy count less relevant")
add_aligned(["1.1", "12.5"], ["11.7"], "Contract 1.1 and 12.5: appendices are integral parts")

add_missing("11.8", "Customer warrants that sale of goods/services in TST complies with Russian law", "optional", "low", "Implied warranty exists; 44-FZ procurement and general legal compliance cover this.")

add_aligned(["12.1", "12.2"], ["11.9"], "Contract 12.1/12.2: no Executor substitution except reorganization; Customer substitution transfers rights/obligations")

add_deviation(
    ["12.1"],
    ["11.10"],
    "Matrix 11.10 covers reorganization (full succession) AND liquidation (claims from assets). Contract 12.1 covers only Executor reorganization, not liquidation claim procedure.",
    "low",
    [{"type": "scope", "description": "Matrix covers both reorganization and liquidation mechanisms. Contract covers reorganization only.", "risk": "Liquidation claim procedure not specified; Russian law provides default mechanisms."}]
)

add_missing("11.11", "Instructional materials posted on Bank's official website become binding from next working day after posting", "optional", "low", "In 44-FZ, all binding terms must be in contract; automatic incorporation via website posting is regime-limited.")

add_missing("11.12", "All notices and requests deemed properly sent if sent per 2.3 procedures", "optional", "low", "Contract 2.3 and 10.1 cover notice mechanics but lack explicit 'deemed sent' clause.")

add_aligned(["12.5"], ["11.13"], "Contract 12.5 lists appendices: Technical Assignment, Specification")

# ============ EXTRA (CONTRACT-ONLY) TERMS ============

add_extra("3.3", "Application of 44-FZ price cap/initial maximum price provisions", "low", "44-FZ regulatory mechanic; inherent in procurement regime", "44-FZ mandatory provision clarifying price cap application")
add_extra("4.1", "Service period tied to earlier of date or price exhaustion", "low", "Early price exhaustion protects Bank; 44-FZ standard", "Creates automatic contract end when maximum price reached")
add_extra("4.2", "Executor must have banking license per Federal Law 395-1", "low", "Standard 44-FZ participant requirement", "Confirms Bank must hold valid banking license")
add_extra("4.4 (абз.2)", "Bank must notify Customer of account changes within 2 days; otherwise bears all risks", "medium", "Short 2-day notification with risk transfer to Bank", "Creates independent obligation on Bank with liability consequence")
add_extra("5.1.2", "Monthly acceptance document obligation per 8.3.1/8.3.2", "low", "44-FZ EIS document exchange mechanic", "44-FZ required procedure for acceptance documentation via EIS")
add_extra("5.2.2", "Bank may unilaterally refuse contract per 44-FZ and Civil Code grounds", "low", "44-FZ statutory right", "44-FZ statutory termination right")
add_extra("5.3.4", "Customer must unilaterally terminate if Executor does not meet procurement requirements or provided false info", "medium", "Customer must terminate for Bank non-compliance; creates mandatory termination obligation", "44-FZ mandatory provision: termination for participant non-compliance")
add_extra("5.3.5", "Customer penalty demand right for Bank delay/non-performance", "low", "Standard 44-FZ penalty mechanism", "44-FZ penalty demand right")
add_extra("5.3.6", "Customer may reduce payment by amount of taxes/fees payable to budgets related to contract", "medium", "Tax withholding right may reduce amounts payable to Bank", "Creates payment reduction right for tax obligations")
add_extra("7.8", "Exchange of documents for liability measures via EIS with UCEP", "low", "44-FZ EIS procedure for penalty notifications", "44-FZ mandatory electronic notification for liability")
add_extra("7.9", "Penalty does not release from performance obligation", "low", "Standard contract principle beneficial to Bank", "Ensures penalty does not excuse non-performance")
add_extra("7.12", "Upon unilateral termination, only actual damages recoverable beyond penalties", "medium", "Limits Bank recovery to actual damages only (not lost profits)", "Liability limitation upon unilateral termination")
add_extra("8.1-8.5.9", "Detailed acceptance procedure via EIS with expert review, acceptance commission, correction mechanisms", "low", "44-FZ mandatory acceptance procedure", "44-FZ comprehensive acceptance regime")
add_extra("8.10", "Bank must correct service defects free of charge within 3 days of claim", "medium", "3-day correction period is strict; specific performance obligation", "Specific defect correction obligation with short deadline")
add_extra("9.3", "Documentary proof of force majeure from authorized body required", "low", "Standard force majeure proof requirement", "Evidentiary requirement for force majeure claims")
add_extra("11.6", "Contract changes/termination per 44-FZ Articles 34, 95, 96, 112", "low", "44-FZ regulatory reference", "44-FZ regulatory mechanic")
add_extra("11.8", "Essential contract conditions may not be changed except as permitted by 44-FZ", "low", "44-FZ restriction on changing essential terms", "44-FZ limitation on contract modifications")
add_extra("12.3", "Bank may provide services with improved characteristics by Customer agreement", "low", "Permits service improvements without formal change procedure", "Allows service quality improvements without contract amendment")

# ============ NOT MATERIAL CONTRACT CLAUSES ============

add_contract_closure("2.1-2.1.28", "not_material", "Definitions section; no independent operative effect")
add_contract_closure("2.2", "not_material", "Definition of electronic terminal; no independent operative effect")
add_contract_closure("5.3.1", "not_material", "General obligation to accept services; covered by 8.3 acceptance procedure")
add_contract_closure("5.3.2", "not_material", "General payment obligation; covered by 4.4/4.5")
add_contract_closure("5.3.3", "not_material", "General monitoring obligation; procedural without independent legal effect")
add_contract_closure("5.4.1", "not_material", "General right to demand performance; declaratory")
add_contract_closure("5.4.2", "not_material", "General right to refuse acceptance; covered by 8.5")
add_contract_closure("5.4.3", "not_material", "General right to unilateral refusal per 44-FZ/Civil Code; covered by 11.3-11.5")
add_contract_closure("5.4.4", "not_material", "General right to refuse payment for defective services; covered by 8.10")
add_contract_closure("7.2", "not_material", "Customer penalty demand right; covered by 7.4/7.4.1")
add_contract_closure("7.3", "not_material", "Customer penalty calculation; covered by 7.4/7.4.1")
add_contract_closure("7.7.2", "not_material", "Alternative penalty for auction winner; contingent on procurement type")
add_contract_closure("7.11", "not_material", "Total fines cap for Customer; duplicates 7.1 para 4")
add_contract_closure("8.1", "not_material", "Quality guarantee; general declaratory provision")
add_contract_closure("8.2", "not_material", "Responsibility for damage during service; general declaratory")
add_contract_closure("8.3", "not_material", "Acceptance per law and contract; general reference")
add_contract_closure("8.5.2-8.5.4", "not_material", "Executor participation in acceptance; procedural detail of 44-FZ")
add_contract_closure("8.5.5-8.5.6", "not_material", "Expert examination procedure; procedural detail")
add_contract_closure("8.5.8", "not_material", "Acceptance commission procedure; procedural detail")
add_contract_closure("8.5.9", "not_material", "Correction of acceptance document; procedural detail")
add_contract_closure("8.6", "not_material", "Acceptance date definition; covered by 8.4")
add_contract_closure("8.7", "not_material", "Correction procedure for acceptance documents; procedural")
add_contract_closure("8.8", "not_material", "Acceptance result formalization; procedural")
add_contract_closure("8.9", "not_material", "Right not to refuse acceptance if defect does not prevent acceptance; procedural")
add_contract_closure("8.11", "not_material", "Signed acceptance document as payment basis; declaratory")
add_contract_closure("13", "not_material", "Addresses and bank details; informational")
add_contract_closure("Приложение №1 (заголовок)", "not_material", "Technical Assignment header; informational")
add_contract_closure("Приложение №1.1 (формы)", "not_material", "Application/registration form templates; no independent operative effect until filled")
add_contract_closure("Приложение №1.2 (форма Информации о ТСТ)", "not_material", "TST information form template; no independent operative effect")
add_contract_closure("Приложение №2 (Спецификация заголовок)", "not_material", "Specification header; informational")
add_contract_closure("Подписи сторон", "not_material", "Signature blocks; no independent operative effect")
add_contract_closure("Преамбула", "not_material", "Contract preamble; informational identification of parties")

# Write the final JSON
with open('outputs/discrepancy_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print(f"Analysis complete.")
print(f"  Aligned: {S['aligned_count']}")
print(f"  Deviations: {S['deviation_count']}")
print(f"  Missing: {S['missing_in_contract_count']}")
print(f"  Extra: {S['extra_in_contract_count']}")
print(f"  Matrix coverage: {len(CLM)}")
print(f"  Contract coverage: {len(CLC)}")
