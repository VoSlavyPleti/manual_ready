import json

# Build the complete discrepancy analysis
# Contract profile: trade_acquiring, 44-FZ, POS terminals (Bank-provided), card payments + basic QR display

analysis = {
  "analysis_profile": {
    "product": ["trade_acquiring"],
    "legal_regime": "44_fz"
  },
  "links": [],
  "unmatched_matrix": [],
  "unmatched_contract": [],
  "coverage_ledger": {"matrix": [], "contract": []},
  "summary": {"aligned_count": 0, "deviation_count": 0, "missing_in_contract_count": 0, "extra_in_contract_count": 0}
}

# Helper
def add_link(contract_ids, matrix_ids, relationship, status_reason, risk_level, discrepancies=None):
    if discrepancies is None:
        discrepancies = []
    analysis["links"].append({
        "contract_ids": contract_ids,
        "matrix_ids": matrix_ids,
        "relationship": relationship,
        "status_reason": status_reason,
        "risk_level": risk_level,
        "discrepancies": discrepancies
    })

def add_unmatched_matrix(matrix_id, status, requirement, required_type, risk_level, risk):
    analysis["unmatched_matrix"].append({
        "matrix_id": matrix_id,
        "status": status,
        "requirement": requirement,
        "required_type": required_type,
        "risk_level": risk_level,
        "risk": risk
    })

def add_unmatched_contract(contract_id, status, contract_position, risk_level, risk, materiality_reason):
    analysis["unmatched_contract"].append({
        "contract_id": contract_id,
        "status": status,
        "contract_position": contract_position,
        "risk_level": risk_level,
        "risk": risk,
        "materiality_reason": materiality_reason
    })

def close_matrix(matrix_id, closure, reason):
    analysis["coverage_ledger"]["matrix"].append({
        "matrix_id": matrix_id,
        "closure": closure,
        "reason": reason
    })

def close_contract(contract_id, closure, reason):
    analysis["coverage_ledger"]["contract"].append({
        "contract_id": contract_id,
        "closure": closure,
        "reason": reason
    })

# ==========================================
# NOW BUILD LINKS
# ==========================================

# --- 2.1 TST Registration ---
add_link(["4.3"], ["2.1"], "deviation",
    "Contract 4.3 requires Заказчик to provide TST registration documents after contract signing; Bank right to refuse registration without explanation missing",
    "medium",
    [{"type": "procedure", "description": "Matrix grants Bank unilateral right to refuse TST registration without reason; contract 4.3 omits this Bank right", "risk": "Bank loses control over which TSTs are registered"}])
close_matrix("2.1", "linked", "Deviation: TST registration analogue in 4.3 but Bank refusal right missing")
close_contract("4.3", "linked", "Linked to matrix 2.1 (TST registration)")

# --- 2.2 Ruble settlements ---
add_link(["5.1.8", "Приложение №1"], ["2.2"], "aligned",
    "Contract 5.1.8 and Technical Assignment confirm settlements in rubles RF",
    "none")
close_matrix("2.2", "linked", "Aligned: ruble currency preserved")
close_contract("5.1.8", "linked", "Linked to matrix 2.2 (ruble settlements)")
close_contract("Приложение №1", "linked", "Linked to matrix 2.2 (ruble settlements); also linked to other items")

# --- 2.3.1 Email exchange ---
add_link(["2.3.1"], ["2.3.1"], "aligned",
    "Contract 2.3.1 preserves email channel with exclusions for personal data/bank secrecy and full legal force",
    "none")
close_matrix("2.3.1", "linked", "Aligned: email exchange terms preserved")
close_contract("2.3.1", "linked", "Linked to matrix 2.3.1 (email exchange)")

# --- 2.3.2 DBO ---
add_link(["2.3.2"], ["2.3.2"], "aligned",
    "Contract 2.3.2 preserves DBO or analogous Bank system channel",
    "none")
close_matrix("2.3.2", "linked", "Aligned: DBO channel preserved")
close_contract("2.3.2", "linked", "Linked to matrix 2.3.2 (DBO exchange)")

# --- 2.3.3 Courier ---
add_link(["2.3.3"], ["2.3.3"], "aligned",
    "Contract 2.3.3 preserves courier/hand-delivery channel",
    "none")
close_matrix("2.3.3", "linked", "Aligned: courier channel preserved")
close_contract("2.3.3", "linked", "Linked to matrix 2.3.3 (courier exchange)")

# --- 2.3.4 Registered mail ---
add_link(["2.3.4"], ["2.3.4"], "aligned",
    "Contract 2.3.4 preserves registered mail channel",
    "none")
close_matrix("2.3.4", "linked", "Aligned: registered mail channel preserved")
close_contract("2.3.4", "linked", "Linked to matrix 2.3.4 (registered mail)")

# --- 2.3.5 E-invoicing ---
add_link(["2.3.5"], ["2.3.5"], "deviation",
    "Contract 2.3.5 has blank placeholder for EDI system name; UKEP and equal legal force preserved",
    "low",
    [{"type": "other", "description": "Matrix specifies E-invoicing/СФЕРА-Курьер; contract 2.3.5 leaves system name blank (______)", "risk": "Operational uncertainty about which EDI system is used"}])
close_matrix("2.3.5", "linked", "Deviation: EDI system name is blank placeholder")
close_contract("2.3.5", "linked", "Linked to matrix 2.3.5 (EDI exchange)")

# --- 2.3.6 EIS ---
add_link(["2.3.6"], ["2.3.6"], "aligned",
    "Contract 2.3.6 preserves EIS and electronic trading platform channel with UKEP and equal legal force; 44-FZ contract matches this mandatory channel",
    "none")
close_matrix("2.3.6", "linked", "Aligned: EIS channel preserved per 44-FZ")
close_contract("2.3.6", "linked", "Linked to matrix 2.3.6 (EIS exchange)")

# --- 2.3.7 Support service + receipt dates ---
add_link(["2.3.7", "2.3"], ["2.3.7"], "aligned",
    "Contract 2.3.7 preserves Bank support service channel; receipt-date rules for all sub-channels preserved in 2.3 concluding paragraph",
    "none")
close_matrix("2.3.7", "linked", "Aligned: support service channel and receipt dates preserved")
close_contract("2.3.7", "linked", "Linked to matrix 2.3.7 (support service + receipt dates)")
close_contract("2.3", "linked", "Linked to matrix 2.3.7 (receipt date rules); also parent of communication channels")

# --- 2.4 Integral documents ---
add_link(["12.5", "8.3.2"], ["2.4"], "aligned",
    "Contract 12.5 lists appendices; 8.3.2 states attached documents are integral part of contract",
    "none")
close_matrix("2.4", "linked", "Aligned: appendices are integral part")
close_contract("12.5", "linked", "Linked to matrix 2.4 (integral documents)")
close_contract("8.3.2", "linked", "Linked to matrix 2.4 (attached documents integral)")

# --- 2.5.1.1 OUT OF SCOPE (internet_acquiring) ---
close_matrix("2.5.1.1", "out_of_scope", "internet_acquiring not in contract scope")

# --- 2.5.2.1 OUT OF SCOPE (SberPay FaceScan) ---
close_matrix("2.5.2.1", "out_of_scope", "SberPay FaceScan/biometric payment not in contract scope")

# --- 2.6.1.1 QR on Smart terminals ---
# Contract Приложение №1 mentions QR capability; Приложение №1.1 has Smart-terminal + QR
add_link(["Приложение №1", "Приложение №1.1"], ["2.6.1.1"], "aligned",
    "Contract Technical Assignment provides QR-code display on terminals; Smart-terminal with QR configured in TST Information",
    "none")
close_matrix("2.6.1.1", "linked", "Aligned: QR on smart terminals provided in contract appendices")
close_contract("Приложение №1.1", "linked", "Linked to matrix 2.6.1.1 (smart terminal QR)")

# --- 2.6.2.1 QR-API ---
# Contract doesn't mention QR-API; QR is basic display feature, not API integration
close_matrix("2.6.2.1", "not_applicable", "QR-API mechanism not activated; contract has basic QR display only, no own KKT software integration")

# --- 2.6.2.2 QR-Vendor ---
close_matrix("2.6.2.2", "not_applicable", "QR-Vendor mechanism not activated; contract has basic QR display only")

# --- 2.6.3.1 QR on Electronic terminals (Bank as Vendor) ---
add_link(["Приложение №1"], ["2.6.3.1"], "aligned",
    "Contract Technical Assignment provides QR-code display capability on terminals; aligned for Bank-provided electronic terminals",
    "none")
close_matrix("2.6.3.1", "linked", "Aligned: QR on electronic terminals provided")

# --- 2.6.3.2 QR deactivation by merchant ---
add_unmatched_matrix("2.6.3.2", "missing_in_contract",
    "Procedure for merchant to request QR deactivation via Bank channels per 2.3.1-2.3.4, 2.3.7",
    "mandatory", "low",
    "QR deactivation procedure absent; operational gap but low risk as QR is supplementary feature")
close_matrix("2.6.3.2", "missing_in_contract", "No procedure for QR deactivation by merchant")

# --- 2.7 Electronic contract conclusion ---
add_link(["12.4"], ["2.7"], "aligned",
    "Contract 12.4 states contract is in electronic form signed with UKEP; equal legal force preserved",
    "none")
close_matrix("2.7", "linked", "Aligned: electronic form with UKEP")
close_contract("12.4", "linked", "Linked to matrix 2.7 (electronic contract)")

# --- 3.1 Merchant organizes card acceptance ---
add_link(["1.1", "1.3", "Приложение №1"], ["3.1"], "aligned",
    "Contract 1.1, 1.3 and Technical Assignment define card acceptance organization and processing on electronic terminals; card list in Technical Assignment includes Mir, VISA, MasterCard",
    "none")
close_matrix("3.1", "linked", "Aligned: card acceptance obligations preserved")
close_contract("1.1", "linked", "Linked to matrix 3.1 (subject of contract)")
close_contract("1.3", "linked", "Linked to matrix 3.1 (card acceptance organization)")

# --- 3.2 Bank transfers operation sums ---
add_link(["5.1.10", "5.1.8"], ["3.2"], "aligned",
    "Contract 5.1.10 and 5.1.8 establish Bank duty to transfer operation sums to merchant",
    "none")
close_matrix("3.2", "linked", "Aligned: Bank duty to transfer sums preserved")
close_contract("5.1.10", "linked", "Linked to matrix 3.2 (Bank transfers sums)")

# --- 3.3 Merchant pays Bank fee ---
add_link(["4.4", "3.1.1", "3.2", "Приложение №2"], ["3.3"], "aligned",
    "Contract 4.4, 3.1.1, 3.2 and Specification establish merchant's duty to pay for services; monthly payment preserved",
    "none")
close_matrix("3.3", "linked", "Aligned: merchant payment duty preserved")
close_contract("4.4", "linked", "Linked to matrix 3.3 (payment obligation)")
close_contract("3.1.1", "linked", "Linked to matrix 3.3 (unit price)")
close_contract("3.2", "linked", "Linked to matrix 3.3 (price includes fee %)")
close_contract("Приложение №2", "linked", "Linked to matrix 3.3 (specification/price)")

# --- 4.1.1 Right to reference card/QR payment ---
# Matrix has pm=qr filter
close_matrix("4.1.1", "not_applicable", "QR-specific right; contract 5.4.5 covers card payment references only, not QR")

# --- 4.1.2 Right to consultation ---
add_link(["5.9"], ["4.1.2"], "aligned",
    "Contract 5.9 grants merchant right to receive consultation on terminal operation and transactions via Bank support service",
    "none")
close_matrix("4.1.2", "linked", "Aligned: consultation right preserved")
close_contract("5.9", "linked", "Linked to matrix 4.1.2 (consultation right)")

# --- 4.1.3 SberPayQR ---
close_matrix("4.1.3", "not_applicable", "SberPayQR payment method not in contract scope")

# --- 4.2.1 Pay Bank services ---
add_link(["4.4", "5.3.2"], ["4.2.1"], "aligned",
    "Contract 4.4, 5.3.2 establish merchant duty to pay for Bank services; fee structure in Specification",
    "none")
close_matrix("4.2.1", "linked", "Aligned: duty to pay Bank services preserved")
close_contract("5.3.2", "linked", "Linked to matrix 4.2.1 (payment duty)")

# --- 4.2.2 Comply with contract and instructional materials ---
add_link(["5.1.1"], ["4.2.2"], "deviation",
    "Contract 5.1.1 requires Bank to conduct initial instruction; no explicit merchant covenant to comply with instructional materials",
    "medium",
    [{"type": "obligation", "description": "Matrix requires explicit merchant obligation to comply with Bank instructional materials; contract only has Bank duty to instruct, not merchant duty to comply", "risk": "Bank cannot enforce compliance with instructional materials as a contractual covenant"}])
close_matrix("4.2.2", "linked", "Deviation: instruction compliance covenant missing")
close_contract("5.1.1", "linked", "Linked to matrix 4.2.2 (instruction); also to 5.2.3")

# --- 4.2.3 Self-familiarization with changes ---
close_matrix("4.2.3", "out_of_scope", "223-FZ regime not applicable; contract under 44-FZ")

# --- 4.2.4 Display Bank info materials ---
add_link(["5.3.7"], ["4.2.4"], "aligned",
    "Contract 5.3.7 requires merchant to display Bank-provided informational materials about card payment capability",
    "none")
close_matrix("4.2.4", "linked", "Aligned: display info materials duty preserved")
close_contract("5.3.7", "linked", "Linked to matrix 4.2.4 (display info materials)")

# --- 4.2.5 Accept all listed cards, no cash, max 2 cards ---
add_link(["5.3.8"], ["4.2.5"], "deviation",
    "Contract 5.3.8 prohibits splitting one operation into multiple; but contract lacks explicit obligation to accept all cards from list, prohibition on cash disbursement, and max 2 different cards per customer",
    "medium",
    [{"type": "scope", "description": "Matrix requires accepting all cards from list, no cash on cards, max 2 cards per customer; contract 5.3.8 only prohibits splitting amounts", "risk": "Merchant could refuse certain card types, issue cash, or accept many cards per customer"}])
close_matrix("4.2.5", "linked", "Deviation: card acceptance scope narrower; cash prohibition and card limit missing")
close_contract("5.3.8", "linked", "Linked to matrix 4.2.5 and 4.2.6 (no splitting)")

# --- 4.2.6 Do not split operations ---
add_link(["5.3.8"], ["4.2.6"], "aligned",
    "Contract 5.3.8 prohibits splitting one operation amount into multiple operations",
    "none")
close_matrix("4.2.6", "linked", "Aligned: no splitting preserved")

# --- 4.2.7 Do not use card details for other purposes ---
add_link(["5.3.9"], ["4.2.7"], "aligned",
    "Contract 5.3.9 prohibits using card details for purposes other than conducting operations in presence or by order of customer",
    "none")
close_matrix("4.2.7", "linked", "Aligned: card details use restriction preserved")
close_contract("5.3.9", "linked", "Linked to matrix 4.2.7 (card details use)")

# --- 4.2.8 Same prices as cash ---
add_unmatched_matrix("4.2.8", "missing_in_contract",
    "Merchant obligation to provide full range of goods/services at prices not exceeding cash prices",
    "mandatory", "medium",
    "No price parity clause; merchant could charge higher prices for card payments")
close_matrix("4.2.8", "missing_in_contract", "No price parity obligation in contract")

# --- 4.2.9 Conduct operations per procedure, responsible for document accuracy ---
add_link(["5.3.10"], ["4.2.9"], "aligned",
    "Contract 5.3.10 requires conducting operations and processing documents per contract, with responsibility for document accuracy",
    "none")
close_matrix("4.2.9", "linked", "Aligned: operational procedure and document accuracy duty preserved")
close_contract("5.3.10", "linked", "Linked to matrix 4.2.9 (document accuracy)")

# --- 4.2.10 Store documents 13 months, provide copies in 3 working days ---
add_link(["5.3.11"], ["4.2.10"], "aligned",
    "Contract 5.3.11 requires storing operation documents 13+ months and providing copies within 3 working days of Bank request",
    "none")
close_matrix("4.2.10", "linked", "Aligned: document storage and copy provision preserved")
close_contract("5.3.11", "linked", "Linked to matrix 4.2.10 (document storage)")

# --- 4.2.11 Provide written statement on operation circumstances in 3 working days ---
add_link(["5.5", "5.3.12"], ["4.2.11"], "aligned",
    "Contract 5.5 and 5.3.12 require written statement on operation circumstances within 3 working days of Bank request; immediate notification of document loss preserved",
    "none")
close_matrix("4.2.11", "linked", "Aligned: statement provision and loss notification preserved")
close_contract("5.5", "linked", "Linked to matrix 4.2.11 (statement on operations)")
close_contract("5.3.12", "linked", "Linked to matrix 4.2.11 (statement on operations)")

# --- 4.2.12 Accept payment claims within 5 working days ---
add_link(["8.5.1"], ["4.2.12"], "deviation",
    "Contract uses EIS-based acceptance procedure under 44-FZ (8.5.1: 10 working days for acceptance); matrix requires 5 working days for payment claim acceptance. Different mechanism but analogous.",
    "low",
    [{"type": "deadline", "description": "Matrix requires 5 working days for payment claim acceptance; contract 8.5.1 provides 10 working days via EIS acceptance under 44-FZ", "risk": "Longer acceptance period delays payment finality"}])
close_matrix("4.2.12", "linked", "Deviation: acceptance deadline 10 vs 5 working days")
close_contract("8.5.1", "linked", "Linked to matrix 4.2.12 (acceptance deadline); also to matrix 6.4")

# --- 4.2.13 Full indemnity to Bank ---
add_link(["5.3.19"], ["4.2.13"], "aligned",
    "Contract 5.3.19 requires merchant to fully and unconditionally reimburse Bank for: disputed/invalid operations, chargeback-related costs, fines from payment systems, and regulatory penalties due to merchant breach. Scope and formula aligned.",
    "none")
close_matrix("4.2.13", "linked", "Aligned: full indemnity duty preserved")
close_contract("5.3.19", "linked", "Linked to matrix 4.2.13 (indemnity); also to 5.1.1.5")

# --- 4.2.14 Notify of changes (reorganization, address, etc.) in 3 working days ---
add_link(["5.3.13"], ["4.2.14"], "aligned",
    "Contract 5.3.13 requires notification and document provision within 3 working days for reorganization, changes, bankruptcy, management change, address/rekvizity change",
    "none")
close_matrix("4.2.14", "linked", "Aligned: change notification duty preserved")
close_contract("5.3.13", "linked", "Linked to matrix 4.2.14 (change notification)")

# --- 4.2.15 Provide reliable documents annually and on request within 7 working days ---
add_link(["5.3.14"], ["4.2.15"], "aligned",
    "Contract 5.3.14 requires providing reliable documents/s info at least annually and within 7 working days of Bank request, including beneficial owners, financial position, business reputation",
    "none")
close_matrix("4.2.15", "linked", "Aligned: document update duty preserved")
close_contract("5.3.14", "linked", "Linked to matrix 4.2.15 (document updates)")

# --- 4.2.16.1 Transfer director personal data, guarantee legal basis ---
add_link(["5.3.20"], ["4.2.16.1"], "aligned",
    "Contract 5.3.20 requires merchant to transfer director PD (FIO, address, passport) and guarantees legal basis; transfer to Mir payment system covered",
    "none")
close_matrix("4.2.16.1", "linked", "Aligned: director PD transfer preserved")
close_contract("5.3.20", "linked", "Linked to matrix 4.2.16.1 (director PD); also to 4.2.16.2")

# --- 4.2.16.2 Guarantee employee PD consent ---
add_unmatched_matrix("4.2.16.2", "missing_in_contract",
    "Merchant guarantee of employee consent for PD processing (FIO, mobile, email, position, workplace) including transfer to servicing companies",
    "mandatory", "medium",
    "Contract 5.3.20 only covers director PD; employee PD consent guarantee absent. Risk of PD processing without proper consent.")
close_matrix("4.2.16.2", "missing_in_contract", "Employee PD consent guarantee missing")

# --- 4.2.16.3 Provide PD confirmation within 3 working days ---
add_link(["5.3.15"], ["4.2.16.3"], "aligned",
    "Contract 5.3.15 requires merchant to provide confirmation of PD transfer legality upon Bank written request; indemnity for failure to provide preserved",
    "none")
close_matrix("4.2.16.3", "linked", "Aligned: PD confirmation provision preserved")
close_contract("5.3.15", "linked", "Linked to matrix 4.2.16.3 (PD confirmation)")

# --- 4.2.17 PCI DSS compliance ---
close_matrix("4.2.17", "out_of_scope", "PCI DSS requirement applies to internet_acquiring only")

# --- 4.2.18 Stop card acceptance upon termination ---
add_link(["5.3.16"], ["4.2.18"], "aligned",
    "Contract 5.3.16 requires merchant to stop card acceptance and remove informational materials from contract termination date",
    "none")
close_matrix("4.2.18", "linked", "Aligned: termination cessation duty preserved")
close_contract("5.3.16", "linked", "Linked to matrix 4.2.18 (stop acceptance)")

# --- 4.2.19 Do not obstruct Bank inspection, assist in investigation ---
add_link(["5.3.17"], ["4.2.19"], "aligned",
    "Contract 5.3.17 requires merchant not to obstruct Bank inspection and to assist in investigation of suspicious operations",
    "none")
close_matrix("4.2.19", "linked", "Aligned: non-obstruction and assistance duty preserved")
close_contract("5.3.17", "linked", "Linked to matrix 4.2.19 (non-obstruction)")

# --- 4.2.20.1 Self-organize employee instruction ---
add_link(["5.10"], ["4.2.20.1"], "aligned",
    "Contract 5.10 requires merchant to ensure timely self-instruction of all employees on operation procedures posted on Bank site",
    "none")
close_matrix("4.2.20.1", "linked", "Aligned: self-instruction duty preserved")
close_contract("5.10", "linked", "Linked to matrix 4.2.20.1 (employee instruction)")

# --- 4.2.20.2 Use terminals only for contract purposes, no modifications, no self-repair, no third-party transfer ---
add_link(["5.3.18.1"], ["4.2.20.2"], "aligned",
    "Contract 5.3.18.1 requires using terminals/SW only for contract purposes at TST location; prohibits modifications, self-repair, and transfer to third parties except servicing company employees",
    "none")
close_matrix("4.2.20.2", "linked", "Aligned: terminal use restrictions preserved")
close_contract("5.3.18.1", "linked", "Linked to matrix 4.2.20.2 (terminal use limits)")

# --- 4.2.20.3 Provide access for servicing ---
add_link(["5.3.18.2"], ["4.2.20.3"], "aligned",
    "Contract 5.3.18.2 requires providing access to terminal installation sites for connection, setup, repair, replacement, maintenance, and visual inspection",
    "none")
close_matrix("4.2.20.3", "linked", "Aligned: access for servicing preserved")
close_contract("5.3.18.2", "linked", "Linked to matrix 4.2.20.3 (servicing access)")

# --- 4.2.20.4 Accept terminals by act ---
add_link(["5.3.18.3"], ["4.2.20.4"], "aligned",
    "Contract 5.3.18.3 requires accepting electronic terminals by acceptance act in two copies, signed by both parties",
    "none")
close_matrix("4.2.20.4", "linked", "Aligned: terminal acceptance by act preserved")
close_contract("5.3.18.3", "linked", "Linked to matrix 4.2.20.4 (terminal acceptance act)")

# --- 4.2.20.5 Report terminal malfunction/loss immediately ---
add_link(["5.3.20.4"], ["4.2.20.5"], "aligned",
    "Contract 5.3.20.4 requires immediate notification of terminal malfunction or loss",
    "none")
close_matrix("4.2.20.5", "linked", "Aligned: malfunction reporting preserved")
close_contract("5.3.20.4", "linked", "Linked to matrix 4.2.20.5 (malfunction report)")

# --- 4.2.20.6 Return terminals within 5 working days of termination ---
add_link(["5.6", "5.3.18.5"], ["4.2.20.6"], "aligned",
    "Contract 5.6 and 5.3.18.5 require returning terminals within 5 working days of termination or written/oral Bank demand",
    "none")
close_matrix("4.2.20.6", "linked", "Aligned: terminal return duty preserved")
close_contract("5.6", "linked", "Linked to matrix 4.2.20.6 (return terminals)")
close_contract("5.3.18.5", "linked", "Linked to matrix 4.2.20.6 (return terminals)")

# --- 4.2.20.7 Penalty for non-return of terminals ---
add_link(["5.7"], ["4.2.20.7"], "deviation",
    "Contract 5.7 sets penalty: 10,000 RUB per Electronic terminal, 25,000 RUB per Smart terminal. Matrix requires 25,000 RUB for each Electronic terminal and 25,000 RUB for each Smart terminal.",
    "medium",
    [{"type": "amount", "description": "Matrix penalty: 25,000 RUB per Electronic terminal; Contract 5.7: 10,000 RUB per Electronic terminal, 25,000 RUB per Smart terminal", "risk": "Lower penalty for electronic terminal non-return reduces deterrence"}])
close_matrix("4.2.20.7", "linked", "Deviation: electronic terminal penalty 10k vs 25k RUB")
close_contract("5.7", "linked", "Linked to matrix 4.2.20.7 (non-return penalty); also to 5.1.1.6")

# --- 4.2.21.1 - 4.2.21.8 OUT OF SCOPE ---
for mid in ["4.2.21.1","4.2.21.2","4.2.21.3","4.2.21.4","4.2.21.5","4.2.21.6","4.2.21.7","4.2.21.8"]:
    close_matrix(mid, "out_of_scope", "internet_acquiring not in contract scope")

# --- 4.2.22 Provide QR to customer ---
# QR display capability is present, but no explicit merchant duty to provide QR to customer for SberPayQR/Plati QR
close_matrix("4.2.22", "not_applicable", "SberPayQR/Plati QR product not active; QR is terminal display feature only")

# --- 4.2.23 Do not unilaterally change partner QR ---
close_matrix("4.2.23", "not_applicable", "Partner QR mechanism not in contract; QR is basic display")

# --- 4.2.24 Use API within functional boundaries ---
close_matrix("4.2.24", "not_applicable", "QR-API not activated in contract")

# --- 4.2.25 Suspend API on security breach ---
close_matrix("4.2.25", "not_applicable", "QR-API not activated in contract")

# --- 4.2.26 Recurring payments ---
close_matrix("4.2.26", "out_of_scope", "internet_acquiring not in contract scope")

# --- 5.1.1.1 Withhold invalid operation sums ---
add_link(["5.2.10", "5.2.10.1"], ["5.1.1.1"], "aligned",
    "Contract 5.2.10 and 5.2.10.1 grant Bank right to withhold sums for invalid operations; list of invalidity grounds largely aligned",
    "none")
close_matrix("5.1.1.1", "linked", "Aligned: withholding right for invalid operations preserved")
close_contract("5.2.10", "linked", "Linked to matrix 5.1.1.1-5.1.1.5 (withholding)")
close_contract("5.2.10.1", "linked", "Linked to matrix 5.1.1.1 (invalid operations)")

# --- 5.1.1.2 Withhold erroneously transferred sums ---
add_link(["5.2.10.2"], ["5.1.1.2"], "aligned",
    "Contract 5.2.10.2 grants Bank right to withhold erroneously transferred sums",
    "none")
close_matrix("5.1.1.2", "linked", "Aligned: withholding erroneous transfers preserved")
close_contract("5.2.10.2", "linked", "Linked to matrix 5.1.1.2 (erroneous sums)")

# --- 5.1.1.3 Withhold return/chargeback/reversal sums ---
add_link(["5.2.10.3"], ["5.1.1.3"], "aligned",
    "Contract 5.2.10.3 grants Bank right to withhold return operations, chargebacks, and reversal transactions",
    "none")
close_matrix("5.1.1.3", "linked", "Aligned: withholding returns/chargebacks preserved")
close_contract("5.2.10.3", "linked", "Linked to matrix 5.1.1.3 (returns/chargebacks)")

# --- 5.1.1.4 Withhold disputed/charged-back sums ---
add_link(["5.2.10.4"], ["5.1.1.4"], "aligned",
    "Contract 5.2.10.4 grants Bank right to withhold disputed operations and sums charged back by issuer; agent operations covered",
    "none")
close_matrix("5.1.1.4", "linked", "Aligned: withholding disputed sums preserved")
close_contract("5.2.10.4", "linked", "Linked to matrix 5.1.1.4 (disputed sums)")

# --- 5.1.1.5 Withhold fines and losses from merchant breach ---
add_link(["5.2.10.5", "5.3.19"], ["5.1.1.5"], "aligned",
    "Contract 5.2.10.5 and 5.3.19 cover Bank right to withhold/claim fines, losses from payment system penalties and regulatory liability due to merchant breach",
    "none")
close_matrix("5.1.1.5", "linked", "Aligned: withholding fines/losses preserved")
close_contract("5.2.10.5", "linked", "Linked to matrix 5.1.1.5 (fines/losses)")

# --- 5.1.1.6 Withhold penalties for non-return of terminals ---
add_link(["5.7"], ["5.1.1.6"], "deviation",
    "Contract 5.7 sets penalty amounts; Bank may withhold these from sums due. Matrix penalty for electronic terminal is 25,000 RUB; contract is 10,000 RUB.",
    "medium",
    [{"type": "amount", "description": "Matrix: 25,000 RUB per Electronic terminal; Contract: 10,000 RUB. Smart terminal: both 25,000 RUB aligned.", "risk": "Lower penalty for electronic terminal non-return"}])
close_matrix("5.1.1.6", "linked", "Deviation: electronic terminal penalty amount differs")

# --- 5.1.2 Suspend authorization for merchant debt ---
add_unmatched_matrix("5.1.2", "missing_in_contract",
    "Bank right to suspend authorization until full repayment of merchant debt",
    "mandatory", "high",
    "Critical Bank protection missing; no right to suspend authorizations when merchant is indebted")
close_matrix("5.1.2", "missing_in_contract", "No Bank right to suspend authorization for debt")

# --- 5.1.3 Direct debit from merchant account ---
add_link(["Приложение №1.1"], ["5.1.3"], "aligned",
    "Contract Appendix 1.1 section 1.3 provides заранее данный акцепт (pre-given acceptance) for direct debit from merchant account when withholding is impossible",
    "none")
close_matrix("5.1.3", "linked", "Aligned: direct debit acceptance preserved in appendix")
close_contract("Приложение №1.1", "linked", "Linked to matrix 5.1.3 (direct debit acceptance)")

# --- 5.1.4 Invoice/payment claim when withholding impossible ---
add_unmatched_matrix("5.1.4", "missing_in_contract",
    "Bank right to issue invoice or payment claim to merchant's account at specified bank when withholding impossible",
    "mandatory", "low",
    "Contract has direct debit acceptance (5.1.3 analogue) but missing explicit invoice/payment claim mechanism with named bank account")
close_matrix("5.1.4", "missing_in_contract", "No explicit invoice/payment claim mechanism with named account")

# --- 5.1.5 Not reimburse operations violating contract ---
add_unmatched_matrix("5.1.5", "missing_in_contract",
    "Bank right not to reimburse sums for operations conducted in violation of contract terms",
    "mandatory", "medium",
    "Contract lacks explicit Bank right to refuse reimbursement for violating operations; only withholding right but no standalone refusal-to-pay right")
close_matrix("5.1.5", "missing_in_contract", "No explicit right to refuse reimbursement for violating operations")

# --- 5.1.6 Inspect terminals, replace, update software ---
add_link(["5.2.3", "5.2.4"], ["5.1.6"], "aligned",
    "Contract 5.2.3 grants Bank right to inspect technical condition and operation of terminals, replace terminals, and update software with 2 working days notice; 5.2.4 allows remote updates not affecting operation procedure",
    "none")
close_matrix("5.1.6", "linked", "Aligned: inspection/replacement/update rights preserved")
close_contract("5.2.3", "linked", "Linked to matrix 5.1.6 (inspection/replacement)")
close_contract("5.2.4", "linked", "Linked to matrix 5.1.6 (remote updates)")

# --- 5.1.7 Transfer data to Mir payment system ---
add_link(["5.3.20"], ["5.1.7"], "aligned",
    "Contract 5.3.20 covers PD transfer to Mir payment system for contract execution purposes",
    "none")
close_matrix("5.1.7", "linked", "Aligned: data transfer to Mir preserved")

# --- 5.1.8.1 Unilateral stop for contract breach ---
add_link(["5.2.9.1"], ["5.1.8.1"], "aligned",
    "Contract 5.2.9.1 grants Bank right to unilaterally suspend authorization and/or terminate for merchant breach",
    "none")
close_matrix("5.1.8.1", "linked", "Aligned: suspension/termination for breach preserved")
close_contract("5.2.9.1", "linked", "Linked to matrix 5.1.8.1 (breach ground)")

# --- 5.1.8.2 Extremism/terrorism list ---
add_link(["5.2.9.2"], ["5.1.8.2"], "aligned",
    "Contract 5.2.9.2 grants Bank right to suspend/terminate if merchant listed for extremism, terrorism, or WMD financing",
    "none")
close_matrix("5.1.8.2", "linked", "Aligned: extremism/terrorism ground preserved")
close_contract("5.2.9.2", "linked", "Linked to matrix 5.1.8.2 (extremism list)")

# --- 5.1.8.3 Money laundering suspicion ---
add_link(["5.2.9.3"], ["5.1.8.3"], "aligned",
    "Contract 5.2.9.3 grants Bank right to suspend/terminate on suspicion of money laundering or terrorism financing",
    "none")
close_matrix("5.1.8.3", "linked", "Aligned: AML/CTF ground preserved")
close_contract("5.2.9.3", "linked", "Linked to matrix 5.1.8.3 (AML suspicion)")

# --- 5.1.8.4 OUT OF SCOPE ---
close_matrix("5.1.8.4", "out_of_scope", "internet_acquiring not in contract scope")

# --- 5.1.8.5 OUT OF SCOPE ---
close_matrix("5.1.8.5", "out_of_scope", "internet_acquiring not in contract scope")

# --- 5.1.8.6 Negative info from state authorities ---
add_link(["5.2.9.4"], ["5.1.8.6"], "aligned",
    "Contract 5.2.9.4 grants Bank right to suspend/terminate on negative info from state authorities or payment systems",
    "none")
close_matrix("5.1.8.6", "linked", "Aligned: negative info ground preserved")
close_contract("5.2.9.4", "linked", "Linked to matrix 5.1.8.6 (negative info)")

# --- 5.1.8.7 Fraud information ---
add_link(["5.2.9.5", "5.2.9"], ["5.1.8.7"], "aligned",
    "Contract 5.2.9.5 and chapeau 5.2.9 grant Bank right to suspend/terminate on fraud info; sufficient evidence defined as issuer info or payment system notifications",
    "none")
close_matrix("5.1.8.7", "linked", "Aligned: fraud ground preserved")
close_contract("5.2.9.5", "linked", "Linked to matrix 5.1.8.7 (fraud)")
close_contract("5.2.9", "linked", "Linked to matrices 5.1.8.1-5.1.8.13 (suspension/termination chapeau)")

# --- 5.1.8.8 TST premises renovation ---
add_link(["5.2.9.6"], ["5.1.8.8"], "aligned",
    "Contract 5.2.9.6 grants Bank right to suspend/terminate if TST renovation prevents operations",
    "none")
close_matrix("5.1.8.8", "linked", "Aligned: renovation ground preserved")
close_contract("5.2.9.6", "linked", "Linked to matrix 5.1.8.8 (renovation)")

# --- 5.1.8.9 Liquidation/bankruptcy ---
add_link(["5.2.9.7"], ["5.1.8.9"], "aligned",
    "Contract 5.2.9.7 grants Bank right to suspend/terminate on merchant liquidation or bankruptcy proceedings",
    "none")
close_matrix("5.1.8.9", "linked", "Aligned: liquidation/bankruptcy ground preserved")
close_contract("5.2.9.7", "linked", "Linked to matrix 5.1.8.9 (liquidation)")

# --- 5.1.8.10 False information ---
add_link(["5.2.9.8"], ["5.1.8.10"], "aligned",
    "Contract 5.2.9.8 grants Bank right to suspend/terminate on discovery of false merchant/TST/management information",
    "none")
close_matrix("5.1.8.10", "linked", "Aligned: false info ground preserved")
close_contract("5.2.9.8", "linked", "Linked to matrix 5.1.8.10 (false info)")

# --- 5.1.8.11 Goods/services mismatch with declared activity ---
add_link(["5.2.9.9"], ["5.1.8.11"], "aligned",
    "Contract 5.2.9.9 grants Bank right to suspend/terminate if goods/services don't match declared merchant activity",
    "none")
close_matrix("5.1.8.11", "linked", "Aligned: activity mismatch ground preserved")
close_contract("5.2.9.9", "linked", "Linked to matrix 5.1.8.11 (activity mismatch)")

# --- 5.1.8.12 No operations for 30 calendar days ---
add_link(["5.2.9.10"], ["5.1.8.12"], "aligned",
    "Contract 5.2.9.10 grants Bank right to suspend/terminate if no operations for 30 consecutive calendar days",
    "none")
close_matrix("5.1.8.12", "linked", "Aligned: inactivity ground preserved")
close_contract("5.2.9.10", "linked", "Linked to matrix 5.1.8.12 (inactivity)")

# --- 5.1.8.13 Price exhaustion or contract expiry ---
add_link(["5.2.9.11"], ["5.1.8.13"], "aligned",
    "Contract 5.2.9.11 grants Bank right to suspend/terminate on price exhaustion or contract expiry",
    "none")
close_matrix("5.1.8.13", "linked", "Aligned: price expiry ground preserved")
close_contract("5.2.9.11", "linked", "Linked to matrix 5.1.8.13 (price expiry)")

# --- 5.1.9 Additional operation checks ---
add_unmatched_matrix("5.1.9", "missing_in_contract",
    "Bank right to conduct additional operation checks including contacting issuer bank for legitimacy verification",
    "mandatory", "low",
    "Contract lacks explicit right to contact issuer for additional verification; operational gap")
close_matrix("5.1.9", "missing_in_contract", "No explicit additional check/issuer contact right")

# --- 5.1.10 Merchant inspections ---
add_link(["5.2.3"], ["5.1.10"], "deviation",
    "Contract 5.2.3 grants Bank right to inspect technical condition and operation of terminals, but matrix scope includes broader inspection for fraud, goods/service mismatch, and contract compliance",
    "low",
    [{"type": "scope", "description": "Matrix allows inspection for fraud, goods mismatch with declared activity, Resource compliance; contract 5.2.3 limits to technical condition and operation of terminals", "risk": "Narrower inspection scope may limit Bank's ability to detect non-technical violations"}])
close_matrix("5.1.10", "linked", "Deviation: inspection scope narrower than matrix")

# --- 5.1.11 Request operation documents up to 13 months ---
add_link(["5.2.5"], ["5.1.11"], "aligned",
    "Contract 5.2.5 grants Bank right to request operation documents within 13 months; also can demand written statements, invoices, receipts for dispute analysis",
    "none")
close_matrix("5.1.11", "linked", "Aligned: document request right preserved")
close_contract("5.2.5", "linked", "Linked to matrix 5.1.11 (document requests)")

# --- 5.1.12 Unilaterally amend referenced documents ---
add_unmatched_matrix("5.1.12", "missing_in_contract",
    "Bank right to unilaterally amend documents referenced in contract by publishing on Official Bank site at least 1 calendar day before effective date",
    "optional", "medium",
    "Bank cannot unilaterally change referenced documents; contract 11.2 requires written bilateral amendments. Significant operational limitation for Bank.")
close_matrix("5.1.12", "missing_in_contract", "No unilateral amendment right for Bank")

# --- 5.1.13 Notify of Bank rekvezity changes via website ---
add_unmatched_matrix("5.1.13", "missing_in_contract",
    "Bank right to notify merchant of rekvezity changes via Official Bank website",
    "optional", "low",
    "Contract 4.4 requires Bank to notify in writing within 2 days; website notification path not provided. Operational inconvenience but low risk.")
close_matrix("5.1.13", "missing_in_contract", "Website notification for rekvezity changes not provided")

# --- 5.1.14 Send requests to merchant email ---
add_link(["5.2.7"], ["5.1.14"], "aligned",
    "Contract 5.2.7 grants Bank right to send requests to merchant/TST email specified in application/TST information",
    "none")
close_matrix("5.1.14", "linked", "Aligned: email request right preserved")
close_contract("5.2.7", "linked", "Linked to matrix 5.1.14 (email requests)")

# --- 5.1.15 Refuse contract conclusion without reason ---
close_matrix("5.1.15", "not_applicable", "Contract already concluded under 44-FZ; pre-contractual refusal right not applicable to executed contract")

# --- 5.1.16 Require documents per law ---
add_link(["5.2.8"], ["5.1.16"], "aligned",
    "Contract 5.2.8 grants Bank right to require documents and information necessary for statutory functions",
    "none")
close_matrix("5.1.16", "linked", "Aligned: document requirement right preserved")
close_contract("5.2.8", "linked", "Linked to matrix 5.1.16 (document requests)")

# --- 5.1.17.1 Unilateral termination for low POS turnover ---
close_matrix("5.1.17.1", "not_applicable", "Term=pos; contract uses electronic terminals and smart terminals, not specifically pos-only category. This is a Bank commercial policy clause not essential for legal protection in 44-FZ context.")

# --- 5.1.17.2 Unilateral termination for low Smart terminal turnover ---
close_matrix("5.1.17.2", "not_applicable", "Term=smart; commercial turnover threshold clause; not essential for 44-FZ contract where termination governed by 44-FZ and contract section 11")

# --- 5.2.1 OUT OF SCOPE ---
close_matrix("5.2.1", "out_of_scope", "internet_acquiring not in contract scope")

# --- 5.2.2 OUT OF SCOPE ---
close_matrix("5.2.2", "out_of_scope", "internet_acquiring not in contract scope")

# --- 5.2.3 Install and prepare terminals, conduct initial instruction ---
add_link(["5.1.1"], ["5.2.3"], "aligned",
    "Contract 5.1.1 requires Bank to install and prepare electronic terminals within 5 working days of signing, conduct initial instruction of TST employees",
    "none")
close_matrix("5.2.3", "linked", "Aligned: installation and instruction duty preserved")

# --- 5.2.4 24/7 authorization ---
add_link(["5.1.6"], ["5.2.4"], "aligned",
    "Contract 5.1.6 requires Bank to provide round-the-clock authorization",
    "none")
close_matrix("5.2.4", "linked", "Aligned: 24/7 authorization preserved")
close_contract("5.1.6", "linked", "Linked to matrix 5.2.4 (24/7 authorization)")

# --- 5.2.5 Training materials on website ---
add_link(["5.1.1"], ["5.2.5"], "deviation",
    "Contract 5.1.1 mentions training materials on website but URL is blank (________); matrix specifies sberbank.ru/help/business/acquiring",
    "low",
    [{"type": "other", "description": "Training materials URL is blank placeholder; operational gap but materials exist", "risk": "Employees may not know where to access training"}])
close_matrix("5.2.5", "linked", "Deviation: training URL is blank")

# --- 5.2.6 Provide terminals with info materials ---
add_link(["5.1.7"], ["5.2.6"], "aligned",
    "Contract 5.1.7 requires Bank to provide terminals with advertising/info materials needed for card operations",
    "none")
close_matrix("5.2.6", "linked", "Aligned: info materials provision preserved")
close_contract("5.1.7", "linked", "Linked to matrix 5.2.6 (info materials)")

# --- 5.2.7 24/7 terminal operability, replacement within 3 working days ---
add_link(["5.1.4"], ["5.2.7"], "aligned",
    "Contract 5.1.4 requires Bank to ensure 24/7 terminal operability and replace faulty terminal within 3 working days of receiving merchant request via support service",
    "none")
close_matrix("5.2.7", "linked", "Aligned: terminal operability and replacement preserved")
close_contract("5.1.4", "linked", "Linked to matrix 5.2.7 (terminal operability)")

# --- 5.2.8 Transfer operation sums within 2 working days ---
add_link(["5.1.8", "Приложение №1"], ["5.2.8"], "aligned",
    "Contract 5.1.8 requires Bank to transfer operation sums within 2 working days of receiving settlement info; settlement date = working day after electronic reconciliation; 3 calendar day fallback for technical failure preserved",
    "none")
close_matrix("5.2.8", "linked", "Aligned: payment timing and fallback preserved")

# --- 5.2.9 Provide partner QR code ---
close_matrix("5.2.9", "not_applicable", "Partner QR code mechanism (SberPayQR/Plati QR) not in contract scope; QR is basic display feature")

# --- 5.2.10 Process PD per 152-FZ ---
add_link(["5.1.9"], ["5.2.10"], "aligned",
    "Contract 5.1.9 requires Bank to process PD per 152-FZ, ensure confidentiality and protection, take legal/organizational/technical measures",
    "none")
close_matrix("5.2.10", "linked", "Aligned: PD processing duty preserved")
close_contract("5.1.9", "linked", "Linked to matrix 5.2.10 (PD processing)")

# --- 5.2.12 OUT OF SCOPE ---
close_matrix("5.2.12", "out_of_scope", "internet_acquiring not in contract scope")

# --- 6.1 Fee as percentage ---
add_link(["3.2", "Приложение №2"], ["6.1"], "deviation",
    "Contract 3.2 states fee is percentage of each operation; Specification (Приложение №2) has fee column but value is blank/merged with total price. Percentage rate not specified.",
    "high",
    [{"type": "amount", "description": "Matrix requires specified fee percentage; contract Specification has blank fee percentage. Only maximum total contract price (1,900,000 RUB) is specified.", "risk": "Fee percentage is undefined; commercial uncertainty for Bank"}])
close_matrix("6.1", "linked", "Deviation: fee percentage blank in Specification")

# --- 6.2 Monthly UPD by 5th working day ---
add_link(["8.3.1", "8.3.2"], ["6.2"], "deviation",
    "Contract uses EIS-based acceptance document under 44-FZ (8.3.1, 8.3.2) rather than UPD. Monthly submission timeline differs: matrix 5th working day vs contract 10th working day (8.3.1). Different document form but same legal function.",
    "low",
    [{"type": "deadline", "description": "Matrix: UPD by 5th working day; Contract: EIS acceptance document by 10th working day. Form differs (EIS vs UPD) but 44-FZ requires EIS route.", "risk": "Longer document delivery period (10 vs 5 working days)"}])
close_matrix("6.2", "linked", "Deviation: EIS acceptance replaces UPD; deadline 10 vs 5 working days")

# --- 6.3 (fz_223) OUT OF SCOPE ---
close_matrix("6.3", "out_of_scope", "223-FZ regime not applicable")

# --- 6.4 Return signed UPD by 25th ---
add_link(["8.5.1"], ["6.4"], "deviation",
    "Contract 8.5.1 requires acceptance within 10 working days via EIS, not 25th calendar day. Under 44-FZ, acceptance procedure is EIS-based.",
    "low",
    [{"type": "deadline", "description": "Matrix: UPD return by 25th of month following reporting; Contract: EIS acceptance within 10 working days", "risk": "Different acceptance mechanism under 44-FZ but functional equivalent"}])
close_matrix("6.4", "linked", "Deviation: acceptance timeline follows 44-FZ EIS route")

# --- 6.5 Payment within 5 working days of UPD signing ---
add_link(["4.5"], ["6.5"], "deviation",
    "Contract 4.5 requires payment within 7 working days of acceptance document signing. Matrix requires 5 working days.",
    "low",
    [{"type": "deadline", "description": "Matrix: 5 working days after UPD signing; Contract 4.5: 7 working days after acceptance document signing", "risk": "2-day longer payment period; minor cash flow impact"}])
close_matrix("6.5", "linked", "Deviation: payment deadline 7 vs 5 working days")
close_contract("4.5", "linked", "Linked to matrix 6.5 (payment deadline)")

# --- 6.6 (fz_223) OUT OF SCOPE ---
close_matrix("6.6", "out_of_scope", "223-FZ regime not applicable")

# --- 6.7 - 6.18 Smart terminal service fees ---
# Contract Приложение №1 states: "Комиссия за предоставление терминалов - отсутствует. Абонентская плата за пользование терминалами - отсутствует."
# So there is NO service fee for terminals in this contract
for mid in ["6.7","6.8","6.9","6.10","6.11","6.12","6.13","6.14","6.15","6.16","6.17","6.18"]:
    close_matrix(mid, "not_applicable", "Contract states no terminal commission/subscription fee (Technical Assignment: комиссия/абонентская плата отсутствует)")

# --- 6.20 No fee on returns/chargebacks/reversals ---
add_link(["Приложение №1"], ["6.20"], "aligned",
    "Contract Technical Assignment states: плата за проведение расчетов по Операциям возврата, Возврат платежа и Реверсивным транзакциям не взимается; previously withheld fee not returned",
    "none")
close_matrix("6.20", "linked", "Aligned: no fee on returns/chargebacks preserved")

# --- 6.21 Contract price ---
add_link(["3.1", "Приложение №2"], ["6.21"], "aligned",
    "Contract 3.1 sets maximum contract price at 1,900,000 RUB; Specification confirms",
    "none")
close_matrix("6.21", "linked", "Aligned: contract price specified")
close_contract("3.1", "linked", "Linked to matrix 6.21 (contract price)")

# --- 7.1 General liability ---
add_link(["7.1"], ["7.1"], "aligned",
    "Contract 7.1 establishes liability for non-performance per contract and RF legislation",
    "none")
close_matrix("7.1", "linked", "Aligned: general liability clause preserved")
close_contract("7.1", "linked", "Linked to matrix 7.1 (general liability)")

# --- 7.2 Merchant non-performance fines ---
add_link(["7.4", "7.4.1"], ["7.2"], "aligned",
    "Contract 7.4 and 7.4.1 set fines for merchant non-performance (excluding delay) per RF Government Resolution 1042: 1000 RUB for contracts ≤3M RUB",
    "none")
close_matrix("7.2", "linked", "Aligned: merchant fine scale aligned")
close_contract("7.4", "linked", "Linked to matrix 7.2 (merchant fines)")
close_contract("7.4.1", "linked", "Linked to matrix 7.2 (merchant fine amounts)")

# --- 7.3 Merchant fine cap ---
add_link(["7.11", "7.1"], ["7.3"], "aligned",
    "Contract 7.11 and 7.1 cap total merchant fines at contract price",
    "none")
close_matrix("7.3", "linked", "Aligned: merchant fine cap preserved")
close_contract("7.11", "linked", "Linked to matrix 7.3 (merchant fine cap)")

# --- 7.4 Bank delay penalty ---
add_link(["7.6"], ["7.4"], "aligned",
    "Contract 7.6 sets penalty for Bank delay at 1/300 key rate of contract price reduced proportionally; merchant directs claim to Bank",
    "none")
close_matrix("7.4", "linked", "Aligned: Bank delay penalty preserved")
close_contract("7.6", "linked", "Linked to matrix 7.4 (Bank delay penalty)")

# --- 7.5 Bank non-performance fines ---
add_link(["7.7", "7.7.1", "7.7.3"], ["7.5"], "aligned",
    "Contract 7.7/7.7.1 set Bank non-performance fines: 10% for ≤3M; 7.7.3 sets non-monetary obligation fines per Resolution 1042",
    "none")
close_matrix("7.5", "linked", "Aligned: Bank fine scale aligned")
close_contract("7.7", "linked", "Linked to matrix 7.5 (Bank fines)")
close_contract("7.7.1", "linked", "Linked to matrix 7.5 (Bank fine scale)")
close_contract("7.7.3", "linked", "Linked to matrix 7.5 and 7.6 (non-monetary fines)")

# --- 7.6 Bank non-monetary obligation fines ---
add_link(["7.7.3"], ["7.6"], "aligned",
    "Contract 7.7.3 sets fines for non-monetary Bank obligations per Resolution 1042",
    "none")
close_matrix("7.6", "linked", "Aligned: non-monetary fine scale aligned")

# --- 7.7 Bank fine cap ---
add_link(["7.10", "7.1"], ["7.7"], "aligned",
    "Contract 7.10 and 7.1 cap total Bank fines at contract price",
    "none")
close_matrix("7.7", "linked", "Aligned: Bank fine cap preserved")
close_contract("7.10", "linked", "Linked to matrix 7.7 (Bank fine cap)")

# --- 7.8 Bank not liable for merchant-customer disputes ---
add_unmatched_matrix("7.8", "missing_in_contract",
    "Bank exemption from liability for disputes between merchant and customer not related to contract subject",
    "optional", "low",
    "Contract lacks explicit exclusion of Bank liability for merchant-customer disputes; general liability clause may expose Bank")
close_matrix("7.8", "missing_in_contract", "No Bank exemption for merchant-customer disputes")

# --- 7.9 Bank not liable for transfer delays not Bank's fault ---
add_unmatched_matrix("7.9", "missing_in_contract",
    "Bank exemption from liability for transfer delays not caused by Bank",
    "optional", "low",
    "Contract lacks explicit exemption; 7.1 general liability subject to fault may partially cover but not explicit")
close_matrix("7.9", "missing_in_contract", "No explicit exemption for non-Bank-fault delays")

# --- 7.10 Bank not liable for third-party actions ---
add_unmatched_matrix("7.10", "missing_in_contract",
    "Bank exemption from liability for non-performance caused by third parties including payment system participants",
    "optional", "low",
    "Contract lacks explicit third-party liability exclusion; force majeure (section 9) provides partial cover")
close_matrix("7.10", "missing_in_contract", "No explicit third-party liability exclusion")

# --- 7.11 Bank not liable for delayed transfers during investigation ---
add_unmatched_matrix("7.11", "missing_in_contract",
    "Bank exemption from liability for delayed transfer of operation sums due to Bank investigation of suspected contract violation",
    "optional", "low",
    "Contract lacks this protection; Bank exposed if it withholds funds during investigation")
close_matrix("7.11", "missing_in_contract", "No exemption for investigation-related delays")

# --- 7.12 Bank not liable for exceeding contract price ---
add_unmatched_matrix("7.12", "missing_in_contract",
    "Bank exemption from liability for exceeding contract price",
    "optional", "low",
    "Contract lacks explicit price-exceedance exemption")
close_matrix("7.12", "missing_in_contract", "No price-exceedance liability exemption")

# --- 7.13 OUT OF SCOPE ---
close_matrix("7.13", "out_of_scope", "internet_acquiring not in contract scope")

# --- 7.14 Merchant liable for all actions in SPEP ---
close_matrix("7.14", "not_applicable", "SPEP (Internet acquiring payment page) not in contract scope; trade acquiring only")

# --- 7.15 Merchant liable for personnel actions ---
add_unmatched_matrix("7.15", "missing_in_contract",
    "Merchant full liability for personnel actions violating contract and Bank instructional materials",
    "mandatory", "low",
    "Contract lacks explicit personnel liability clause; general liability (7.1) may cover but not explicit")
close_matrix("7.15", "missing_in_contract", "No explicit personnel liability clause")

# --- 7.16 Anti-corruption ---
add_link(["6.1"], ["7.16"], "aligned",
    "Contract 6.1 contains anti-corruption clause: parties undertake not to engage in corrupt actions per applicable law",
    "none")
close_matrix("7.16", "linked", "Aligned: anti-corruption clause preserved")
close_contract("6.1", "linked", "Linked to matrix 7.16 (anti-corruption)")

# --- 7.17 Merchant liability for recurring payments ---
close_matrix("7.17", "not_applicable", "Recurring payments (Повторяющиеся платежи) primarily internet acquiring; trade acquiring contract does not activate this")

# --- 8.1 Force majeure ---
add_link(["9.1"], ["8.1"], "aligned",
    "Contract 9.1 defines force majeure events and exempts parties from liability; includes natural disasters, floods, earthquakes, fires, military actions, strikes, epidemics; proportional extension of deadlines preserved",
    "none")
close_matrix("8.1", "linked", "Aligned: force majeure definition and relief preserved")
close_contract("9.1", "linked", "Linked to matrix 8.1 (force majeure)")

# --- 8.2 Force majeure notification ---
add_link(["9.2", "9.3"], ["8.2"], "deviation",
    "Contract 9.2 requires notification within 5 days (matrix: 24 hours); 9.3 requires documentary proof; termination right after 1 month (matrix: 3 months)",
    "medium",
    [{"type": "deadline", "description": "Matrix: 24 hours notification; Contract 9.2: 5 days. Matrix: termination after 3 months; Contract: 1 month.", "risk": "Longer notification period; shorter termination trigger period"}])
close_matrix("8.2", "linked", "Deviation: notification 5 days vs 24h; termination 1 month vs 3 months")
close_contract("9.2", "linked", "Linked to matrix 8.2 (FM notification)")
close_contract("9.3", "linked", "Linked to matrix 8.2 (FM proof)")

# --- 9.1 Pre-trial dispute resolution ---
add_link(["10.1"], ["9.1"], "aligned",
    "Contract 10.1 establishes pre-trial dispute resolution via negotiations and written claims",
    "none")
close_matrix("9.1", "linked", "Aligned: pre-trial procedure preserved")
close_contract("10.1", "linked", "Linked to matrix 9.1 and 9.2 (dispute resolution)")

# --- 9.2 10 calendar day claim review ---
add_link(["10.1"], ["9.2"], "aligned",
    "Contract 10.1 sets 10 calendar day response period for claims, letters, communications",
    "none")
close_matrix("9.2", "linked", "Aligned: 10 calendar day claim review preserved")

# --- 9.3 Unresolved disputes per RF law ---
add_link(["10.2"], ["9.3"], "aligned",
    "Contract 10.2: unresolved disputes referred to Arbitration Court of Krasnodar Krai",
    "none")
close_matrix("9.3", "linked", "Aligned: judicial resolution clause preserved")
close_contract("10.2", "linked", "Linked to matrix 9.3 (court)")

# --- 10.1 Contract term ---
add_link(["11.1"], ["10.1"], "aligned",
    "Contract 11.1: effective from signing through 30.12.2025 or until price exhaustion; post-termination liability preserved",
    "none")
close_matrix("10.1", "linked", "Aligned: term and post-termination liability preserved")
close_contract("11.1", "linked", "Linked to matrix 10.1 (contract term)")

# --- 10.2 Unilateral termination with 30-day notice ---
add_link(["11.3", "11.4", "11.5"], ["10.2"], "deviation",
    "Contract 11.3-11.5 allow unilateral termination per 44-FZ and Civil Code grounds, not a general 30-day notice right; 44-FZ constrains unilateral termination",
    "medium",
    [{"type": "procedure", "description": "Matrix: any party may terminate with 30 calendar day notice; Contract: termination governed by 44-FZ (art. 95) and Civil Code, no general 30-day notice right", "risk": "Bank cannot freely exit contract with 30-day notice; 44-FZ restrictions apply"}])
close_matrix("10.2", "linked", "Deviation: no general 30-day termination right; 44-FZ governs")
close_contract("11.3", "linked", "Linked to matrix 10.2 (termination)")
close_contract("11.4", "linked", "Linked to matrix 10.2 (customer termination right)")
close_contract("11.5", "linked", "Linked to matrix 10.2 (44-FZ termination procedure)")

# --- 10.3 Post-termination settlement within 18 months ---
add_unmatched_matrix("10.3", "missing_in_contract",
    "Post-unilateral-termination settlement period of 18 months; payment of operation sums per 5.1.3, 5.1.4 and section 6",
    "mandatory", "low",
    "Contract lacks explicit 18-month post-termination settlement period for unilateral Bank termination")
close_matrix("10.3", "missing_in_contract", "No 18-month post-termination settlement period")

# --- 11.1 Sources of regulation ---
add_unmatched_matrix("11.1", "missing_in_contract",
    "Clause stating contract, RF law, payment system rules as sources; contract terms conflicting with payment system rules to be aligned",
    "optional", "low",
    "Contract 11.7 references RF legislation for gaps but no explicit payment system rule precedence clause")
close_matrix("11.1", "missing_in_contract", "No payment system rule precedence clause")

# --- 11.2 Confidentiality of payment information ---
add_unmatched_matrix("11.2", "missing_in_contract",
    "Confidentiality of card numbers, PD, operation sums, payment info; prohibition on third-party transfer",
    "optional", "low",
    "Contract lacks explicit payment data confidentiality clause; general confidentiality not addressed")
close_matrix("11.2", "missing_in_contract", "No payment data confidentiality clause")

# --- 11.3 Non-disclosure of contract execution info ---
add_unmatched_matrix("11.3", "missing_in_contract",
    "Non-disclosure of card security elements, operation technology, financial/management info, other damaging info",
    "optional", "low",
    "Contract lacks non-disclosure clause for contract execution information")
close_matrix("11.3", "missing_in_contract", "No non-disclosure clause for execution info")

# --- 11.4 Written amendments ---
add_link(["11.2"], ["11.4"], "aligned",
    "Contract 11.2 requires written amendments signed by both parties",
    "none")
close_matrix("11.4", "linked", "Aligned: written amendment requirement preserved")
close_contract("11.2", "linked", "Linked to matrix 11.4 (written amendments)")

# --- 11.5 Prior agreements superseded ---
add_unmatched_matrix("11.5", "missing_in_contract",
    "Prior agreements, negotiations, correspondence on contract matters lose force upon signing",
    "optional", "low",
    "Contract lacks integration/merger clause; prior communications could theoretically be invoked")
close_matrix("11.5", "missing_in_contract", "No integration clause")

# --- 11.6 Number of contract copies ---
add_unmatched_matrix("11.6", "missing_in_contract",
    "Contract executed in X copies, Y for Bank, 1 for merchant",
    "optional", "low",
    "Contract is electronic (12.4); paper copy count not specified but this is formal")
close_matrix("11.6", "missing_in_contract", "Electronic contract; copy count not applicable")

# --- 11.7 Appendices are integral ---
add_link(["12.5"], ["11.7"], "aligned",
    "Contract 12.5 lists appendices as integral parts",
    "none")
close_matrix("11.7", "linked", "Aligned: appendices integral")

# --- 11.8 Merchant warrants legal compliance ---
add_unmatched_matrix("11.8", "missing_in_contract",
    "Merchant warranty that goods/services sales comply with RF legislation",
    "optional", "low",
    "Contract lacks explicit merchant warranty of legal compliance for goods/services")
close_matrix("11.8", "missing_in_contract", "No merchant legal compliance warranty")

# --- 11.9 No assignment without consent ---
add_link(["12.1", "12.2"], ["11.9"], "deviation",
    "Contract 12.1 prohibits performer substitution except reorganization succession; 12.2 allows customer rights transfer. Matrix requires mutual written consent for assignment.",
    "low",
    [{"type": "party", "description": "Matrix: no assignment without mutual written consent; Contract 12.1/12.2: 44-FZ governs assignment with different rules", "risk": "Assignment rules differ from matrix under 44-FZ"}])
close_matrix("11.9", "linked", "Deviation: assignment rules under 44-FZ vs mutual consent")
close_contract("12.1", "linked", "Linked to matrix 11.9 (assignment)")
close_contract("12.2", "linked", "Linked to matrix 11.9 (customer transfer)")

# --- 11.10 Reorganization succession ---
add_unmatched_matrix("11.10", "missing_in_contract",
    "Obligations transfer to successor upon reorganization; liquidation claims satisfied from liquidated party's assets",
    "optional", "low",
    "Contract 12.1 partially covers reorganization (performer substitution); full succession/liquidation clause absent")
close_matrix("11.10", "missing_in_contract", "Full succession/liquidation clause absent")

# --- 11.11 Instructional materials binding from next working day ---
add_unmatched_matrix("11.11", "missing_in_contract",
    "Instructional materials on Bank website become binding next working day after posting",
    "optional", "medium",
    "Contract lacks clause making Bank-website instructional materials contractually binding; significant gap for Bank operational control")
close_matrix("11.11", "missing_in_contract", "No website materials binding clause")

# --- 11.12 Notices valid if sent per 2.3 ---
add_link(["10.1", "2.3"], ["11.12"], "aligned",
    "Contract 2.3 defines communication channels; 10.1 specifies written notice via registered mail or personal delivery. Combined package preserves that notices via contract channels are valid.",
    "none")
close_matrix("11.12", "linked", "Aligned: notice validity via contract channels")
close_contract("10.1", "linked", "Linked to matrix 11.12 (notices)")

# --- 11.13 List of appendices ---
add_link(["12.5"], ["11.13"], "aligned",
    "Contract 12.5 lists appendices: №1 Technical Assignment, №2 Specification. Matrix also lists Application, TST Info, Act, Service Description. Different set but same legal function.",
    "none")
close_matrix("11.13", "linked", "Aligned: appendix list present")

# ==========================================
# EXTRA CONTRACT ITEMS
# ==========================================

# Customer rights unique to 44-FZ / contract
add_unmatched_contract("5.3.4", "extra_in_contract",
    "Customer right to unilaterally refuse contract if performer doesn't meet procurement requirements or provided false info",
    "medium",
    "Creates additional termination right for customer beyond matrix scope; 44-FZ art. 95 mechanism",
    "Independent customer termination right under 44-FZ not in matrix")
close_contract("5.3.4", "extra_in_contract", "44-FZ customer termination right")

add_unmatched_contract("5.3.5", "extra_in_contract",
    "Customer right to demand penalties (fines, late fees) for performer delay or non-performance",
    "low",
    "Standard 44-FZ penalty demand right; matrix 7.4 provides analogous Bank-side penalty mechanism",
    "Customer penalty demand right explicit under 44-FZ")
close_contract("5.3.5", "extra_in_contract", "Customer penalty demand right")

add_unmatched_contract("5.3.6", "extra_in_contract",
    "Customer right to reduce payment by amount of taxes/duties payable to budget system",
    "low",
    "Tax offset mechanism specific to 44-FZ contracts with budgetary institutions",
    "44-FZ tax deduction right not in matrix")
close_contract("5.3.6", "extra_in_contract", "Tax deduction from payment")

add_unmatched_contract("5.4.2", "extra_in_contract",
    "Customer right to refuse acceptance of services of improper quality",
    "medium",
    "Independent acceptance refusal right; matrix has no direct customer acceptance refusal analogue",
    "Customer quality-based refusal right")
close_contract("5.4.2", "extra_in_contract", "Customer acceptance refusal right")

add_unmatched_contract("5.4.3", "extra_in_contract",
    "Customer right to unilaterally refuse contract per 44-FZ and Civil Code",
    "medium",
    "Mirrors Bank's 5.2.2 but customer-side; creates symmetric but customer-initiated termination",
    "Customer unilateral termination right under 44-FZ")
close_contract("5.4.3", "extra_in_contract", "Customer unilateral termination right")

add_unmatched_contract("5.4.4", "extra_in_contract",
    "Customer right to refuse payment for improper quality and demand refund + damages",
    "medium",
    "Customer payment refusal and refund right beyond matrix scope",
    "Customer payment refusal/refund right")
close_contract("5.4.4", "extra_in_contract", "Customer payment refusal right")

add_unmatched_contract("8.5.2", "extra_in_contract",
    "Performer right to participate in acceptance procedure upon written notice 15 working days before acceptance deadline",
    "low",
    "44-FZ acceptance participation mechanism; matrix has no specific participation analogue",
    "44-FZ-specific acceptance participation right for performer")
close_contract("8.5.2", "extra_in_contract", "Performer acceptance participation right")

add_unmatched_contract("8.5.3", "extra_in_contract",
    "Bilateral acceptance required if performer notified of participation in time",
    "low",
    "44-FZ procedure detail",
    "Mandatory bilateral acceptance under 44-FZ")
close_contract("8.5.3", "extra_in_contract", "Mandatory bilateral acceptance")

add_unmatched_contract("8.5.4", "extra_in_contract",
    "Unilateral customer acceptance if performer didn't notify or notified late",
    "low",
    "44-FZ procedure detail",
    "Unilateral acceptance fallback under 44-FZ")
close_contract("8.5.4", "extra_in_contract", "Unilateral acceptance fallback")

add_unmatched_contract("8.5.5", "extra_in_contract",
    "Customer conducts expert examination of services for contract compliance",
    "low",
    "44-FZ mandatory expert examination right",
    "44-FZ expert examination requirement")
close_contract("8.5.5", "extra_in_contract", "Customer expert examination right")

add_unmatched_contract("8.5.6", "extra_in_contract",
    "Expert examination may be conducted by customer's own resources or external experts",
    "low",
    "44-FZ expert examination detail",
    "Customer expert examination options under 44-FZ")
close_contract("8.5.6", "extra_in_contract", "Customer expert examination options")

add_unmatched_contract("8.5.8", "extra_in_contract",
    "Acceptance commission procedure for non-conformities with detailed signing and EIS posting process",
    "low",
    "44-FZ acceptance commission mechanism; detailed procedure not in matrix",
    "44-FZ acceptance commission procedure")
close_contract("8.5.8", "extra_in_contract", "Acceptance commission procedure")

add_unmatched_contract("8.5.9", "extra_in_contract",
    "Performer right to remedy defects and resubmit corrected acceptance document",
    "low",
    "44-FZ correction mechanism",
    "44-FZ correction and resubmission right")
close_contract("8.5.9", "extra_in_contract", "Correction resubmission right")

add_unmatched_contract("8.7", "extra_in_contract",
    "Corrections to acceptance document via EIS with UKEP signatures",
    "low",
    "44-FZ document correction procedure",
    "EIS acceptance document correction procedure")
close_contract("8.7", "extra_in_contract", "Acceptance document correction procedure")

add_unmatched_contract("8.9", "extra_in_contract",
    "Customer right not to refuse acceptance if non-conformity doesn't prevent acceptance and is remedied",
    "low",
    "44-FZ acceptance flexibility provision",
    "Customer conditional acceptance right")
close_contract("8.9", "extra_in_contract", "Conditional acceptance right")

add_unmatched_contract("8.10", "extra_in_contract",
    "Performer duty to eliminate defects within 3 days of customer notice at own cost",
    "medium",
    "Creates specific defect correction timeline; matrix has no such explicit customer right",
    "Defect correction deadline")
close_contract("8.10", "extra_in_contract", "3-day defect correction duty")

add_unmatched_contract("8.11", "extra_in_contract",
    "Signed EIS acceptance document is basis for payment",
    "low",
    "44-FZ acceptance-payment link; functionally analogous to matrix but 44-FZ-specific mechanism",
    "EIS acceptance as payment basis")
close_contract("8.11", "extra_in_contract", "EIS acceptance = payment basis")

add_unmatched_contract("7.8", "extra_in_contract",
    "Exchange of documents for liability measures via EIS with UKEP",
    "low",
    "44-FZ-specific liability document exchange mechanism",
    "EIS liability document exchange")
close_contract("7.8", "extra_in_contract", "EIS liability document exchange")

add_unmatched_contract("7.12", "extra_in_contract",
    "Party may claim only actual damage (not lost profit) upon unilateral termination",
    "high",
    "Limits Bank's recovery to actual damage only, excluding lost profit; significant limitation",
    "Damage recovery limited to actual damage upon unilateral termination")
close_contract("7.12", "extra_in_contract", "Actual damage only upon termination")

# Additional extra items
add_unmatched_contract("4.2", "extra_in_contract",
    "Performer must hold banking license per 395-1 and comply with procurement requirements",
    "low",
    "Regulatory requirement restatement; low materiality",
    "Banking license requirement per law")
close_contract("4.2", "extra_in_contract", "Bank license requirement")

add_unmatched_contract("5.3.3", "extra_in_contract",
    "Customer right to monitor performer's service delivery",
    "low",
    "General monitoring right; limited independent legal effect",
    "Customer monitoring right")
close_contract("5.3.3", "extra_in_contract", "Customer monitoring right")

add_unmatched_contract("5.1.3", "extra_in_contract",
    "Performer duty to ensure services comply with RF legislation requirements",
    "low",
    "General compliance warranty; standard legal obligation",
    "Statutory compliance warranty")
close_contract("5.1.3", "extra_in_contract", "RF law compliance warranty")

add_unmatched_contract("5.1.5", "extra_in_contract",
    "Performer duty to provide full and accurate information about services and performance progress",
    "low",
    "Information duty; standard obligation",
    "Information provision duty")
close_contract("5.1.5", "extra_in_contract", "Information duty")

add_unmatched_contract("12.3", "extra_in_contract",
    "Parties may agree to improved service quality/characteristics vs contract specifications",
    "low",
    "44-FZ improvement clause; limited independent effect",
    "Service improvement possibility")
close_contract("12.3", "extra_in_contract", "Service improvement clause")

add_unmatched_contract("11.6", "extra_in_contract",
    "Contract changes/termination per 44-FZ articles 34, 95, 96, 112",
    "low",
    "44-FZ statutory reference; limited independent effect",
    "44-FZ statutory reference")
close_contract("11.6", "extra_in_contract", "44-FZ change/termination reference")

add_unmatched_contract("11.8", "extra_in_contract",
    "No change of essential contract terms except per 44-FZ",
    "low",
    "44-FZ restriction; protective for both parties",
    "44-FZ essential terms protection")
close_contract("11.8", "extra_in_contract", "Essential terms protection")

# Now handle contract clauses not yet closed
# Sections that are purely definitional or not material
not_material_clauses = [
    ("1.2", "Volume definition - not independently operative"),
    ("2.1", "Definitions preamble; covered through substantive clauses"),
    ("2.1.1", "Definition of bank card - not independently operative"),
    ("2.1.2", "Definition of acquiring bank - not independently operative"),
    ("2.1.3", "Definition of issuing bank - not independently operative"),
    ("2.1.4", "Definition of chargeback - not independently operative"),
    ("2.1.5", "Definition of cardholder - not independently operative"),
    ("2.1.6", "Definition of operation document - not independently operative"),
    ("2.1.7", "Definition of authorization code - not independently operative"),
    ("2.1.8", "Definition of KKT - not independently operative"),
    ("2.2", "Definition of electronic terminal - covered via substantive clauses"),
    ("3.3", "Price application per 44-FZ - not independently operative"),
    ("4.1", "Service period clause; covered through term clauses"),
    ("5.1", "Performer obligations chapeau - covered through child clauses"),
    ("5.1.2", "Monthly acceptance document; covered via 8.3.1/8.3.2"),
    ("5.2", "Performer rights chapeau - covered through child clauses"),
    ("5.2.1", "Demand timely acceptance/payment; covered via other clauses"),
    ("5.2.2", "Unilateral refusal per 44-FZ/GC; covered via 11.3-11.5"),
    ("5.2.6", "Notify of rekvezity changes; covered via 4.4"),
    ("5.3", "Customer obligations chapeau - covered through child clauses"),
    ("5.3.1", "Accept services; covered via section 8 acceptance"),
    ("5.4", "Customer rights chapeau - covered through child clauses"),
    ("5.4.1", "Demand proper performance; general clause"),
    ("5.4.5", "Reference card payment in ads; covered via consultation"),
    ("7.2", "Performer right to demand penalties; mirror of 7.5"),
    ("7.3", "Customer delay penalty formula; matrix 7.4 analogue"),
    ("7.5", "Customer right to demand performer penalties; mirror"),
    ("7.7.2", "Penalty for bidder offering highest price; not applicable"),
    ("7.9", "Penalty doesn't release from performance; general"),
    ("8.1", "Quality warranty; general"),
    ("8.2", "Performer liability for damage; general"),
    ("8.3", "Acceptance per law; chapeau"),
    ("8.4", "Acceptance document receipt date; detail"),
    ("8.5", "Acceptance procedure chapeau"),
    ("8.5.7", "Acceptance without remarks; detail"),
    ("8.6", "Acceptance date definition; detail"),
    ("8.8", "Acceptance result formalization; detail"),
    ("9", "Force majeure section chapeau"),
    ("10", "Dispute resolution section chapeau"),
    ("11", "Contract term section chapeau"),
    ("11.7", "Gaps governed by RF law; general"),
    ("12", "Miscellaneous section chapeau"),
    ("12.5", "Appendices list; covered"),
    ("13", "Addresses and bank details; formal"),
]

for cid, reason in not_material_clauses:
    close_contract(cid, "not_material", reason)

# Remaining contract clauses to close
remaining_linked = [
    ("5.2.9", "Chapeau for unilateral suspension; linked to matrices 5.1.8.x"),
    ("5.2.10", "Withholding chapeau; linked"),
    ("Приложение №1", "Technical Assignment; linked to multiple matrices"),
    ("Приложение №1.1", "TST Information; linked to multiple matrices"),
    ("Приложение №2", "Specification; linked to multiple matrices"),
]

for cid, reason in remaining_linked:
    if cid not in [c["contract_id"] for c in analysis["coverage_ledger"]["contract"]]:
        close_contract(cid, "linked", reason)

remaining_not_material = [
    ("4.5.1", "November payment deadline detail subsumed under 4.5"),
    ("5.3.18", "Trade acquiring chapeau; children carry operative content"),
    ("9.2.1", "Technical reconciliation discrepancy procedure; operational detail"),
]

for cid, reason in remaining_not_material:
    if cid not in [c["contract_id"] for c in analysis["coverage_ledger"]["contract"]]:
        close_contract(cid, "not_material", reason)

# ==========================================
# COMPUTE SUMMARY
# ==========================================
aligned = sum(1 for l in analysis["links"] if l["relationship"] == "aligned")
deviations = sum(1 for l in analysis["links"] if l["relationship"] == "deviation")
missing = len(analysis["unmatched_matrix"])
extra = len(analysis["unmatched_contract"])

analysis["summary"] = {
    "aligned_count": aligned,
    "deviation_count": deviations,
    "missing_in_contract_count": missing,
    "extra_in_contract_count": extra
}

with open('outputs/discrepancy_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print(f"Total links: {len(analysis['links'])} (aligned: {aligned}, deviation: {deviations})")
print(f"Unmatched matrix: {missing}")
print(f"Unmatched contract: {extra}")
print(f"Matrix coverage: {len(analysis['coverage_ledger']['matrix'])}")
print(f"Contract coverage: {len(analysis['coverage_ledger']['contract'])}")
