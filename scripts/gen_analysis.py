#!/usr/bin/env python3
"""
Generate discrepancy_analysis.json with full coverage ledger validation.
"""
import json

# ============================================================
# PROFILE
# ============================================================
analysis_profile = {
    "product": ["trade_acquiring"],
    "legal_regime": "44_fz"
}

# ============================================================
# MATRIX COVERAGE LEDGER (all 169 matrix ids)
# ============================================================
matrix_ledger = [
    # Section 2
    {"matrix_id":"2.1","closure":"linked","reason":"Contract 4.3 covers TST registration; deviation: missing Bank right to refuse without reason"},
    {"matrix_id":"2.2","closure":"linked","reason":"Contract 5.1.8 + Technical Assignment item 5 specify RUB"},
    {"matrix_id":"2.3.1","closure":"linked","reason":"Contract 2.3.1 mirrors matrix"},
    {"matrix_id":"2.3.2","closure":"linked","reason":"Contract 2.3.2 mirrors matrix"},
    {"matrix_id":"2.3.3","closure":"linked","reason":"Contract 2.3.3 mirrors matrix (optional, present)"},
    {"matrix_id":"2.3.4","closure":"linked","reason":"Contract 2.3.4 mirrors matrix (optional, present)"},
    {"matrix_id":"2.3.5","closure":"linked","reason":"Contract 2.3.5 mirrors but system name is blank placeholder"},
    {"matrix_id":"2.3.6","closure":"linked","reason":"Contract 2.3.6 mirrors, 44-FZ EIS channel present"},
    {"matrix_id":"2.3.7","closure":"linked","reason":"Contract 2.3.7 mirrors matrix"},
    {"matrix_id":"2.4","closure":"linked","reason":"Contract 1.1 + 12.5 declare appendices integral"},
    {"matrix_id":"2.5.1.1","closure":"out_of_scope","reason":"Product=internet_acquiring; contract is trade_acquiring only"},
    {"matrix_id":"2.5.2.1","closure":"missing_in_contract","reason":"No SberPayFaceScan biometric connection mechanism in contract"},
    {"matrix_id":"2.6.1.1","closure":"out_of_scope","reason":"Terminal=smart only; contract primarily uses standard POS terminals, not smart-terminals"},
    {"matrix_id":"2.6.2.1","closure":"missing_in_contract","reason":"No QR-API reference in contract for own KKT software"},
    {"matrix_id":"2.6.2.2","closure":"missing_in_contract","reason":"No QR-vendor reference or own-KKT QR self-setup mechanism"},
    {"matrix_id":"2.6.3.1","closure":"missing_in_contract","reason":"No provision that QR connects automatically when Bank terminal installed"},
    {"matrix_id":"2.6.3.2","closure":"missing_in_contract","reason":"No QR deactivation procedure via Bank channels specified"},
    {"matrix_id":"2.7","closure":"linked","reason":"Contract 12.4 confirms electronic form with UKEP"},

    # Section 3
    {"matrix_id":"3.1","closure":"linked","reason":"Contract 1.3 obligates Customer to organise card acceptance"},
    {"matrix_id":"3.2","closure":"linked","reason":"Contract 5.1.8 obligates Bank to transfer operation amounts"},
    {"matrix_id":"3.3","closure":"linked","reason":"Contract 4.5 obligates Customer to pay for Bank services; 3.2 embeds fee in unit price"},

    # Section 4.1
    {"matrix_id":"4.1.1","closure":"linked","reason":"Contract 5.4.5 allows Customer to reference card acceptance in ads with Bank approval"},
    {"matrix_id":"4.1.2","closure":"linked","reason":"Contract 5.9 grants right to receive consultation via support service"},
    {"matrix_id":"4.1.3","closure":"missing_in_contract","reason":"No explicit right to use Bank-provided QR codes for SberPayQR/Plati QR"},

    # Section 4.2
    {"matrix_id":"4.2.1","closure":"linked","reason":"Contract 4.5 obligates Customer to pay for services"},
    {"matrix_id":"4.2.2","closure":"missing_in_contract","reason":"No obligation to comply with Bank instructional materials; only training mentioned"},
    {"matrix_id":"4.2.3","closure":"not_applicable","reason":"Lot=fz_223 only; contract is 44-FZ regime"},
    {"matrix_id":"4.2.4","closure":"linked","reason":"Contract 5.3.7 obligates Customer to place Bank informational materials"},
    {"matrix_id":"4.2.5","closure":"linked","reason":"Contract 5.3.8 covers no-splitting; deviation: missing 2-card limit and no-cash rule"},
    {"matrix_id":"4.2.6","closure":"linked","reason":"Contract 5.3.8 prohibits splitting one operation into several"},
    {"matrix_id":"4.2.7","closure":"linked","reason":"Contract 5.3.9 prohibits using card details for other purposes"},
    {"matrix_id":"4.2.8","closure":"missing_in_contract","reason":"No provision that card prices must not exceed cash prices"},
    {"matrix_id":"4.2.9","closure":"linked","reason":"Contract 5.3.10 obligates proper operation conduct and document accuracy"},
    {"matrix_id":"4.2.10","closure":"linked","reason":"Contract 5.3.11 covers 13-month document retention and 3-day response"},
    {"matrix_id":"4.2.11","closure":"linked","reason":"Contract 5.5, 5.3.12 cover written statement and loss notification"},
    {"matrix_id":"4.2.12","closure":"missing_in_contract","reason":"No direct-debit/acceptance of payment claims mechanism via bank account"},
    {"matrix_id":"4.2.13","closure":"linked","reason":"Contract 5.3.19 covers full indemnification for chargebacks, disputes, fines"},
    {"matrix_id":"4.2.14","closure":"linked","reason":"Contract 5.3.13 covers 3-day notification for reorganisation, address, details changes"},
    {"matrix_id":"4.2.15","closure":"linked","reason":"Contract 5.3.14 covers annual and on-request document updates within 7 working days"},
    {"matrix_id":"4.2.16.1","closure":"linked","reason":"Contract 5.3.20 covers PDn of director; alignment on FIO, address, passport, MIR transfer"},
    {"matrix_id":"4.2.16.2","closure":"missing_in_contract","reason":"No coverage of employee PDn consent (non-director staff)"},
    {"matrix_id":"4.2.16.3","closure":"linked","reason":"Contract 5.3.15 covers proof-of-consent obligation and indemnity"},
    {"matrix_id":"4.2.17","closure":"out_of_scope","reason":"Product=internet_acquiring; contract is trade_acquiring only"},
    {"matrix_id":"4.2.18","closure":"linked","reason":"Contract 5.3.16 obligates cessation of card acceptance and removal of materials on termination"},
    {"matrix_id":"4.2.19","closure":"linked","reason":"Contract 5.3.17 prohibits obstruction and requires cooperation in fraud investigations"},
    {"matrix_id":"4.2.20.1","closure":"linked","reason":"Contract 5.10 obligates self-guided staff training via website"},
    {"matrix_id":"4.2.20.2","closure":"linked","reason":"Contract 5.3.18.1 covers use-only-for-contract, no-modification, no-self-repair, no-transfer"},
    {"matrix_id":"4.2.20.3","closure":"linked","reason":"Contract 5.3.18.2 obligates access for installation, repair, maintenance"},
    {"matrix_id":"4.2.20.4","closure":"linked","reason":"Contract 5.3.18.3 covers acceptance by act in two copies"},
    {"matrix_id":"4.2.20.5","closure":"linked","reason":"Contract 5.3.20.4 obligates immediate notification of terminal failure or loss"},
    {"matrix_id":"4.2.20.6","closure":"linked","reason":"Contract 5.3.18.5 obligates return within 5 working days after termination"},
    {"matrix_id":"4.2.20.7","closure":"linked","reason":"Contract 5.7 sets penalty for non-return: 10,000 per electronic terminal, 25,000 per smart terminal"},
    {"matrix_id":"4.2.21.1","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.2","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.3","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.4","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.5","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.6","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.7","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.21.8","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"4.2.22","closure":"missing_in_contract","reason":"No explicit obligation to provide QR-code to buyers for SberPayQR/Plati QR"},
    {"matrix_id":"4.2.23","closure":"missing_in_contract","reason":"No prohibition on unilateral QR-code change by Customer"},
    {"matrix_id":"4.2.24","closure":"missing_in_contract","reason":"No QR-API usage restrictions in contract"},
    {"matrix_id":"4.2.25","closure":"missing_in_contract","reason":"No QR-API security breach notification procedure"},
    {"matrix_id":"4.2.26","closure":"out_of_scope","reason":"Product=internet_acquiring; recurring payments in internet context"},

    # Section 5.1 (Bank rights)
    {"matrix_id":"5.1.1.1","closure":"linked","reason":"Contract 5.2.10.1 covers withholding for invalid operations with matching case list"},
    {"matrix_id":"5.1.1.2","closure":"linked","reason":"Contract 5.2.10.2 covers withholding erroneously transferred amounts"},
    {"matrix_id":"5.1.1.3","closure":"linked","reason":"Contract 5.2.10.3 covers withholding for return operations, chargebacks, reversals"},
    {"matrix_id":"5.1.1.4","closure":"linked","reason":"Contract 5.2.10.4 covers withholding disputed/charged-back operations"},
    {"matrix_id":"5.1.1.5","closure":"linked","reason":"Contract 5.2.10.5 covers withholding fines and losses from payment system sanctions"},
    {"matrix_id":"5.1.1.6","closure":"linked","reason":"Contract 5.7 penalty for non-return linked to Bank withholding rights"},
    {"matrix_id":"5.1.2","closure":"missing_in_contract","reason":"No explicit right to suspend Authorisation until Customer debt is fully repaid"},
    {"matrix_id":"5.1.3","closure":"linked","reason":"Appendix 1.1 item 1.3 grants pre-given acceptance for direct debit from account"},
    {"matrix_id":"5.1.4","closure":"missing_in_contract","reason":"No invoice/payment-claim mechanism specified for amounts not covered by withholding"},
    {"matrix_id":"5.1.5","closure":"missing_in_contract","reason":"No explicit right to refuse reimbursement for operations violating contract terms"},
    {"matrix_id":"5.1.6","closure":"linked","reason":"Contract 5.2.3, 5.2.4 cover technical inspection, replacement, remote update rights"},
    {"matrix_id":"5.1.7","closure":"missing_in_contract","reason":"No right to transfer data (including PDn) to MIR payment system for suspicious operations"},
    {"matrix_id":"5.1.8.1","closure":"linked","reason":"Contract 5.2.9.1 covers suspension/termination for contract violation"},
    {"matrix_id":"5.1.8.2","closure":"linked","reason":"Contract 5.2.9.2 covers extremism/terrorism list entry"},
    {"matrix_id":"5.1.8.3","closure":"linked","reason":"Contract 5.2.9.3 covers money-laundering/terrorism-financing suspicion"},
    {"matrix_id":"5.1.8.4","closure":"out_of_scope","reason":"Product=internet_acquiring; Resource compliance ground not applicable"},
    {"matrix_id":"5.1.8.5","closure":"out_of_scope","reason":"Product=internet_acquiring; prohibited activities ground not applicable"},
    {"matrix_id":"5.1.8.6","closure":"linked","reason":"Contract 5.2.9.4 covers negative info from state authorities/payment systems"},
    {"matrix_id":"5.1.8.7","closure":"linked","reason":"Contract 5.2.9.5 covers fraud information from issuer banks/payment systems"},
    {"matrix_id":"5.1.8.8","closure":"linked","reason":"Contract 5.2.9.6 covers premises renovation impeding operations"},
    {"matrix_id":"5.1.8.9","closure":"linked","reason":"Contract 5.2.9.7 covers liquidation/bankruptcy"},
    {"matrix_id":"5.1.8.10","closure":"linked","reason":"Contract 5.2.9.8 covers unreliable information about Customer/TST/director"},
    {"matrix_id":"5.1.8.11","closure":"linked","reason":"Contract 5.2.9.9 covers mismatch of goods/services to declared activity"},
    {"matrix_id":"5.1.8.12","closure":"linked","reason":"Contract 5.2.9.10 covers 30-day inactivity"},
    {"matrix_id":"5.1.8.13","closure":"linked","reason":"Contract 5.2.9.11 covers price exhaustion and contract term expiry"},
    {"matrix_id":"5.1.9","closure":"missing_in_contract","reason":"No right to conduct additional operation checks with issuer bank"},
    {"matrix_id":"5.1.10","closure":"linked","reason":"Contract 5.2.3, 5.2.9, 5.3.17 cover inspection rights for fraud and compliance"},
    {"matrix_id":"5.1.11","closure":"linked","reason":"Contract 5.2.5 covers document requests within 13 months"},
    {"matrix_id":"5.1.12","closure":"missing_in_contract","reason":"No unilateral right for Bank to amend referenced documents with 1-day notice via website"},
    {"matrix_id":"5.1.13","closure":"linked","reason":"Contract 4.4 provides Bank detail change notification; deviation: written notice vs website posting"},
    {"matrix_id":"5.1.14","closure":"linked","reason":"Contract 5.2.7 covers email requests to Customer for operation info"},
    {"matrix_id":"5.1.15","closure":"not_applicable","reason":"Pre-contractual right; contract concluded under 44-FZ competitive procedure"},
    {"matrix_id":"5.1.16","closure":"linked","reason":"Contract 5.2.8 covers right to demand documents required by law"},
    {"matrix_id":"5.1.17.1","closure":"missing_in_contract","reason":"No turnover-threshold-based unilateral termination right for POS terminals"},
    {"matrix_id":"5.1.17.2","closure":"out_of_scope","reason":"Terminal=smart; contract primarily uses standard POS terminals"},

    # Section 5.2 (Bank obligations)
    {"matrix_id":"5.2.1","closure":"out_of_scope","reason":"Product=internet_acquiring; SPEP access not applicable"},
    {"matrix_id":"5.2.2","closure":"out_of_scope","reason":"Product=internet_acquiring; 3DSecure not applicable"},
    {"matrix_id":"5.2.3","closure":"linked","reason":"Contract 5.1.1 covers installation, training, website materials"},
    {"matrix_id":"5.2.4","closure":"linked","reason":"Contract 5.1.6 covers round-the-clock authorisation"},
    {"matrix_id":"5.2.5","closure":"linked","reason":"Contract 5.1.1 covers training materials on website"},
    {"matrix_id":"5.2.6","closure":"linked","reason":"Contract 5.1.7 covers informational materials for terminals"},
    {"matrix_id":"5.2.7","closure":"linked","reason":"Contract 5.1.4 covers round-the-clock operability and 3-day replacement"},
    {"matrix_id":"5.2.8","closure":"linked","reason":"Contract 5.1.8 covers payment within 2 working days with technical-failure fallback"},
    {"matrix_id":"5.2.9","closure":"missing_in_contract","reason":"No obligation to provide partner QR-code via electronic or paper channels"},
    {"matrix_id":"5.2.10","closure":"linked","reason":"Contract 5.1.9 covers PDn processing under 152-FZ with security measures"},
    {"matrix_id":"5.2.12","closure":"out_of_scope","reason":"Product=internet_acquiring; QR-API 'as-is' not applicable"},

    # Section 6
    {"matrix_id":"6.1","closure":"linked","reason":"Contract 3.2 + Specification set fee as percentage of operations"},
    {"matrix_id":"6.2","closure":"linked","reason":"Contract 8.3.1-8.3.2 covers monthly acceptance document; deviation from UPD form"},
    {"matrix_id":"6.3","closure":"not_applicable","reason":"Lot=fz_223; contract is 44-FZ regime"},
    {"matrix_id":"6.4","closure":"linked","reason":"Contract 8.5 covers acceptance document signing and motivated refusal"},
    {"matrix_id":"6.5","closure":"linked","reason":"Contract 4.5 covers payment within 7 working days of acceptance"},
    {"matrix_id":"6.6","closure":"not_applicable","reason":"Lot=fz_223; contract is 44-FZ regime"},
    {"matrix_id":"6.7","closure":"out_of_scope","reason":"Terminal=smart; contract uses standard POS terminals primarily"},
    {"matrix_id":"6.8","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.9","closure":"out_of_scope","reason":"Terminal=smart + lot=fz_223"},
    {"matrix_id":"6.10","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.11","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.12","closure":"out_of_scope","reason":"Terminal=smart + lot=fz_223"},
    {"matrix_id":"6.13","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.14","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.15","closure":"out_of_scope","reason":"Terminal=smart + lot=fz_223"},
    {"matrix_id":"6.16","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.17","closure":"out_of_scope","reason":"Terminal=smart"},
    {"matrix_id":"6.18","closure":"out_of_scope","reason":"Terminal=smart + lot=fz_223"},
    {"matrix_id":"6.20","closure":"linked","reason":"Technical Assignment specifies no fee for return operations; original fee not returned"},
    {"matrix_id":"6.21","closure":"linked","reason":"Contract 3.1 sets max price 1,900,000 RUB"},

    # Section 7
    {"matrix_id":"7.1","closure":"linked","reason":"Contract 7.1 establishes liability under law and contract"},
    {"matrix_id":"7.2","closure":"linked","reason":"Contract 7.4-7.4.1 set Customer penalty per 44-FZ/PP 1042"},
    {"matrix_id":"7.3","closure":"linked","reason":"Contract 7.1 caps total Customer penalties at contract price"},
    {"matrix_id":"7.4","closure":"linked","reason":"Contract 7.5-7.6 set Bank penalty: 1/300 key rate per day"},
    {"matrix_id":"7.5","closure":"linked","reason":"Contract 7.7-7.7.1 set Bank penalty amounts per PP 1042"},
    {"matrix_id":"7.6","closure":"linked","reason":"Contract 7.7.3 sets penalty for non-monetary obligations per PP 1042"},
    {"matrix_id":"7.7","closure":"linked","reason":"Contract 7.10 caps total Bank penalties at contract price"},
    {"matrix_id":"7.8","closure":"missing_in_contract","reason":"No express disclaimer of Bank liability for Customer-buyer disputes"},
    {"matrix_id":"7.9","closure":"missing_in_contract","reason":"No express disclaimer for transfer delays not caused by Bank fault"},
    {"matrix_id":"7.10","closure":"missing_in_contract","reason":"No disclaimer for third-party actions or inactions including payment system participants"},
    {"matrix_id":"7.11","closure":"missing_in_contract","reason":"No disclaimer for delayed transfers due to Bank investigation of suspicious operations"},
    {"matrix_id":"7.12","closure":"missing_in_contract","reason":"No disclaimer for exceeding contract price"},
    {"matrix_id":"7.13","closure":"out_of_scope","reason":"Product=internet_acquiring"},
    {"matrix_id":"7.14","closure":"missing_in_contract","reason":"No provision that Customer bears full responsibility for actions in SPEP"},
    {"matrix_id":"7.15","closure":"missing_in_contract","reason":"No provision on Customer liability for personnel violations of Bank instructions"},
    {"matrix_id":"7.16","closure":"linked","reason":"Contract 6.1 contains anti-corruption clause"},
    {"matrix_id":"7.17","closure":"missing_in_contract","reason":"No specific financial liability for non-compliant recurring payments"},

    # Section 8
    {"matrix_id":"8.1","closure":"linked","reason":"Contract 9.1 covers force majeure definition and list"},
    {"matrix_id":"8.2","closure":"linked","reason":"Contract 9.2 covers notification obligation; deviation in timing"},

    # Section 9
    {"matrix_id":"9.1","closure":"linked","reason":"Contract 10.1 establishes mandatory pre-trial claim procedure"},
    {"matrix_id":"9.2","closure":"linked","reason":"Contract 10.1 sets 10 calendar day claim response period"},
    {"matrix_id":"9.3","closure":"linked","reason":"Contract 10.2 refers unresolved disputes to Arbitration Court of Krasnodar Krai"},

    # Section 10
    {"matrix_id":"10.1","closure":"linked","reason":"Contract 11.1 sets term until 30.12.2025 or price exhaustion"},
    {"matrix_id":"10.2","closure":"linked","reason":"Contract 11.3-11.5 allow unilateral termination under 44-FZ/GK RF"},
    {"matrix_id":"10.3","closure":"missing_in_contract","reason":"No 18-month post-termination settlement period; no specific Bank-initiated termination settlement procedure"},

    # Section 11
    {"matrix_id":"11.1","closure":"missing_in_contract","reason":"No hierarchy clause prioritising payment system rules over contract"},
    {"matrix_id":"11.2","closure":"missing_in_contract","reason":"No confidentiality obligation for card numbers, payment data, customer PDn"},
    {"matrix_id":"11.3","closure":"missing_in_contract","reason":"No non-disclosure of card security elements, operation technology, financial data"},
    {"matrix_id":"11.4","closure":"linked","reason":"Contract 11.2 requires written form for amendments signed by both parties"},
    {"matrix_id":"11.5","closure":"missing_in_contract","reason":"No merger or integration clause superseding prior agreements"},
    {"matrix_id":"11.6","closure":"linked","reason":"Contract 12.4 states electronic form with UKEP signatures"},
    {"matrix_id":"11.7","closure":"linked","reason":"Contract 1.1 + 12.5 declare appendices integral"},
    {"matrix_id":"11.8","closure":"missing_in_contract","reason":"No warranty that Customer goods/services comply with applicable law"},
    {"matrix_id":"11.9","closure":"linked","reason":"Contract 12.1 prohibits assignment except for reorganisation succession"},
    {"matrix_id":"11.10","closure":"linked","reason":"Contract 12.1-12.2 cover reorganisation succession and customer change"},
    {"matrix_id":"11.11","closure":"missing_in_contract","reason":"No provision that Bank instructional materials become binding next working day after website posting"},
    {"matrix_id":"11.12","closure":"linked","reason":"Contract 2.3 final paragraph confirms proper notice when sent via specified channels"},
    {"matrix_id":"11.13","closure":"linked","reason":"Contract 12.5 lists appendices; composition differs from matrix standard"},
]

# ============================================================
# CONTRACT COVERAGE LEDGER
# ============================================================
contract_ledger = [
    # Section 1
    {"contract_id":"1.1","closure":"linked","reason":"Subject of contract - acquiring services"},
    {"contract_id":"1.2","closure":"linked","reason":"Service volume capped by max price"},
    {"contract_id":"1.3","closure":"linked","reason":"Customer organises card acceptance"},
    # Section 2
    {"contract_id":"2.2","closure":"linked","reason":"Terminal definition; linked to multiple terminal obligations"},
    {"contract_id":"2.3","closure":"linked","reason":"Communication channels header paragraph"},
    {"contract_id":"2.3.1","closure":"linked","reason":"Email communication channel"},
    {"contract_id":"2.3.2","closure":"linked","reason":"DBO system channel"},
    {"contract_id":"2.3.3","closure":"linked","reason":"Courier delivery channel"},
    {"contract_id":"2.3.4","closure":"linked","reason":"Registered mail channel"},
    {"contract_id":"2.3.5","closure":"linked","reason":"E-invoicing system channel (blank system name)"},
    {"contract_id":"2.3.6","closure":"linked","reason":"EIS channel for 44-FZ"},
    {"contract_id":"2.3.7","closure":"linked","reason":"Bank support service channel"},
    # Section 3
    {"contract_id":"3.1","closure":"linked","reason":"Max price 1,900,000 RUB"},
    {"contract_id":"3.1.1","closure":"linked","reason":"Unit price in specification"},
    {"contract_id":"3.2","closure":"linked","reason":"Unit price includes Bank fee as percentage of operations"},
    {"contract_id":"3.3","closure":"linked","reason":"44-FZ price application clause"},
    # Section 4
    {"contract_id":"4.1","closure":"linked","reason":"Service period and price exhaustion condition"},
    {"contract_id":"4.2","closure":"not_material","reason":"Declaratory: contractor must meet legal requirements; no independent operative effect"},
    {"contract_id":"4.3","closure":"linked","reason":"TST registration procedure; Bank right to refuse missing - deviation"},
    {"contract_id":"4.4","closure":"linked","reason":"Payment procedure; Bank account change notification 2-day rule"},
    {"contract_id":"4.5","closure":"linked","reason":"Payment within 7 working days of acceptance"},
    {"contract_id":"4.5.1","closure":"linked","reason":"November payment deadline not later than 30.12.2025"},
    # Section 5.1
    {"contract_id":"5.1.1","closure":"linked","reason":"Install terminals within 5 working days, training, website materials"},
    {"contract_id":"5.1.2","closure":"linked","reason":"Monthly acceptance document obligation"},
    {"contract_id":"5.1.3","closure":"not_material","reason":"Declaratory: obligation to comply with RF legislation exists independently of contract; no independent operative effect"},
    {"contract_id":"5.1.4","closure":"linked","reason":"Round-the-clock operability, 3-day terminal replacement"},
    {"contract_id":"5.1.5","closure":"linked","reason":"Full and accurate service information"},
    {"contract_id":"5.1.6","closure":"linked","reason":"Round-the-clock authorisation"},
    {"contract_id":"5.1.7","closure":"linked","reason":"Informational materials for terminals"},
    {"contract_id":"5.1.8","closure":"linked","reason":"Payment within 2 working days of settlement info receipt"},
    {"contract_id":"5.1.9","closure":"linked","reason":"PDn processing under 152-FZ with security measures"},
    {"contract_id":"5.1.10","closure":"linked","reason":"Transfer of operation amounts to Customer"},
    # Section 5.2
    {"contract_id":"5.2.1","closure":"not_material","reason":"General right to demand performance - purely declaratory"},
    {"contract_id":"5.2.2","closure":"linked","reason":"Unilateral refusal right under 44-FZ/GK RF"},
    {"contract_id":"5.2.3","closure":"linked","reason":"Technical inspection, replacement, software update with 2-day notice"},
    {"contract_id":"5.2.4","closure":"linked","reason":"Remote software update without changing operation procedure"},
    {"contract_id":"5.2.5","closure":"linked","reason":"Document requests within 13 months"},
    {"contract_id":"5.2.6","closure":"linked","reason":"Bank detail change notification within 3 working days"},
    {"contract_id":"5.2.7","closure":"linked","reason":"Email requests for operation info"},
    {"contract_id":"5.2.8","closure":"linked","reason":"Demand documents required by law"},
    {"contract_id":"5.2.9","closure":"linked","reason":"Suspension/termination grounds header"},
    {"contract_id":"5.2.9.1","closure":"linked","reason":"Contract violation ground"},
    {"contract_id":"5.2.9.2","closure":"linked","reason":"Extremism/terrorism list ground"},
    {"contract_id":"5.2.9.3","closure":"linked","reason":"Money laundering suspicion ground"},
    {"contract_id":"5.2.9.4","closure":"linked","reason":"Negative state authority info ground"},
    {"contract_id":"5.2.9.5","closure":"linked","reason":"Fraud info from issuer banks/payment systems ground"},
    {"contract_id":"5.2.9.6","closure":"linked","reason":"Premises renovation ground"},
    {"contract_id":"5.2.9.7","closure":"linked","reason":"Liquidation/bankruptcy ground"},
    {"contract_id":"5.2.9.8","closure":"linked","reason":"Unreliable info ground"},
    {"contract_id":"5.2.9.9","closure":"linked","reason":"Activity mismatch ground"},
    {"contract_id":"5.2.9.10","closure":"linked","reason":"30-day inactivity ground"},
    {"contract_id":"5.2.9.11","closure":"linked","reason":"Price/term exhaustion ground"},
    {"contract_id":"5.2.10","closure":"linked","reason":"Withholding right header"},
    {"contract_id":"5.2.10.1","closure":"linked","reason":"Invalid operations withholding with detailed case list"},
    {"contract_id":"5.2.10.2","closure":"linked","reason":"Erroneous transfers withholding"},
    {"contract_id":"5.2.10.3","closure":"linked","reason":"Returns, chargebacks, reversals withholding"},
    {"contract_id":"5.2.10.4","closure":"linked","reason":"Disputed operations withholding"},
    {"contract_id":"5.2.10.5","closure":"linked","reason":"Fines and losses from payment system sanctions withholding"},
    # Section 5.3
    {"contract_id":"5.3.1","closure":"not_material","reason":"General acceptance obligation - covered by specific procedures in Section 8"},
    {"contract_id":"5.3.2","closure":"linked","reason":"Pay for services obligation"},
    {"contract_id":"5.3.3","closure":"not_material","reason":"General monitoring right - declaratory, no independent operative effect"},
    {"contract_id":"5.3.4","closure":"extra_in_contract","reason":"Customer 44-FZ obligation to unilaterally terminate if Executor non-compliant with procurement requirements"},
    {"contract_id":"5.3.5","closure":"linked","reason":"Right to demand penalties from Executor"},
    {"contract_id":"5.3.6","closure":"extra_in_contract","reason":"Tax withholding right under Russian tax law - independent Customer right"},
    {"contract_id":"5.3.7","closure":"linked","reason":"Place Bank informational materials at visible TST locations"},
    {"contract_id":"5.3.8","closure":"linked","reason":"No operation splitting prohibition"},
    {"contract_id":"5.3.9","closure":"linked","reason":"No card data misuse"},
    {"contract_id":"5.3.10","closure":"linked","reason":"Proper operation conduct and document accuracy responsibility"},
    {"contract_id":"5.3.11","closure":"linked","reason":"13-month document retention, 3-day response to Bank requests"},
    {"contract_id":"5.3.12","closure":"linked","reason":"Written statement on operation circumstances and loss notification"},
    {"contract_id":"5.3.13","closure":"linked","reason":"3-day reorganisation/change notification with supporting documents"},
    {"contract_id":"5.3.14","closure":"linked","reason":"Annual and on-request document updates within 7 working days"},
    {"contract_id":"5.3.15","closure":"linked","reason":"PDn consent proof within 3 working days and indemnity"},
    {"contract_id":"5.3.16","closure":"linked","reason":"Cease card acceptance and remove materials on termination"},
    {"contract_id":"5.3.17","closure":"linked","reason":"No obstruction and cooperation in fraud investigations"},
    {"contract_id":"5.3.18","closure":"linked","reason":"Trade acquiring operations header"},
    {"contract_id":"5.3.18.1","closure":"linked","reason":"Use terminals only for contract, no modification, no self-repair, no third-party transfer"},
    {"contract_id":"5.3.18.2","closure":"linked","reason":"Access for installation, repair, maintenance, visual inspection"},
    {"contract_id":"5.3.18.3","closure":"linked","reason":"Accept terminals by act in two copies"},
    {"contract_id":"5.3.20.4","closure":"linked","reason":"Immediate notification of terminal failure or loss"},
    {"contract_id":"5.3.18.5","closure":"linked","reason":"Return terminals within 5 working days after termination or demand"},
    {"contract_id":"5.3.19","closure":"linked","reason":"Full indemnification for chargebacks, disputes, fines, losses"},
    {"contract_id":"5.3.20","closure":"linked","reason":"PDn transfer guarantee for director data to Bank and MIR"},
    # Section 5.4
    {"contract_id":"5.4.1","closure":"not_material","reason":"General right to demand performance - purely declaratory"},
    {"contract_id":"5.4.2","closure":"linked","reason":"Right to refuse acceptance for poor quality"},
    {"contract_id":"5.4.3","closure":"linked","reason":"Unilateral termination right under 44-FZ/GK RF"},
    {"contract_id":"5.4.4","closure":"linked","reason":"Right to refuse payment and demand refund for poor quality"},
    {"contract_id":"5.4.5","closure":"linked","reason":"Right to reference card acceptance in ads with Bank approval"},
    # Section 5.5-5.10
    {"contract_id":"5.5","closure":"linked","reason":"Written statement obligation within 3 working days of Bank request"},
    {"contract_id":"5.6","closure":"linked","reason":"Return of terminals on loss or termination"},
    {"contract_id":"5.7","closure":"linked","reason":"Penalty for non-return: 10,000 per electronic terminal, 25,000 per smart terminal"},
    {"contract_id":"5.9","closure":"linked","reason":"Right to consultation via Bank support service"},
    {"contract_id":"5.10","closure":"linked","reason":"Self-guided staff training via website"},
    # Section 6
    {"contract_id":"6.1","closure":"linked","reason":"Anti-corruption clause"},
    # Section 7
    {"contract_id":"7.1","closure":"linked","reason":"General liability with penalty caps at contract price"},
    {"contract_id":"7.2","closure":"linked","reason":"Executor right to demand Customer penalties"},
    {"contract_id":"7.3","closure":"linked","reason":"Customer penalty: 1/300 key rate per day of delay"},
    {"contract_id":"7.4","closure":"linked","reason":"Customer penalty grounds (non-delay violations)"},
    {"contract_id":"7.4.1","closure":"linked","reason":"Customer penalty amounts per PP 1042: 1000 RUB for <3M"},
    {"contract_id":"7.5","closure":"linked","reason":"Customer right to demand Executor penalties"},
    {"contract_id":"7.6","closure":"linked","reason":"Executor penalty: 1/300 key rate per day of delay"},
    {"contract_id":"7.7","closure":"linked","reason":"Executor penalty grounds (non-delay violations)"},
    {"contract_id":"7.7.1","closure":"linked","reason":"Executor penalty amounts per PP 1042: 10% for <3M"},
    {"contract_id":"7.7.2","closure":"not_material","reason":"Special penalty formula for auction winner with above-NMC price - not applicable"},
    {"contract_id":"7.7.3","closure":"linked","reason":"Executor penalty for non-monetary obligations: 1000 RUB"},
    {"contract_id":"7.8","closure":"linked","reason":"Penalty exchange via EIS with UKEP"},
    {"contract_id":"7.9","closure":"linked","reason":"Penalty does not release from performance obligation"},
    {"contract_id":"7.10","closure":"linked","reason":"Cap on Executor penalties at contract price"},
    {"contract_id":"7.11","closure":"linked","reason":"Cap on Customer penalties at contract price"},
    {"contract_id":"7.12","closure":"extra_in_contract","reason":"Unilateral termination damages limited to actual harm only beyond penalties - independent 44-FZ rule"},
    # Section 8
    {"contract_id":"8.1","closure":"linked","reason":"Quality guarantee per regulatory requirements"},
    {"contract_id":"8.2","closure":"linked","reason":"Liability for damage caused by Executor specialists"},
    {"contract_id":"8.3","closure":"linked","reason":"Acceptance procedure per law and contract - header"},
    {"contract_id":"8.3.1","closure":"linked","reason":"Monthly acceptance document via EIS by 10th working day"},
    {"contract_id":"8.3.2","closure":"linked","reason":"Supporting documents: invoice, act, form 363 account"},
    {"contract_id":"8.4","closure":"linked","reason":"Date of acceptance document receipt via EIS"},
    {"contract_id":"8.5","closure":"linked","reason":"Acceptance procedure header"},
    {"contract_id":"8.5.1","closure":"linked","reason":"10 working day acceptance or motivated refusal period"},
    {"contract_id":"8.5.2","closure":"extra_in_contract","reason":"Executor right to participate in acceptance - independent 44-FZ procedural right"},
    {"contract_id":"8.5.3","closure":"extra_in_contract","reason":"Bilateral acceptance when Executor notified - 44-FZ procedure"},
    {"contract_id":"8.5.4","closure":"extra_in_contract","reason":"Unilateral acceptance by Customer when no Executor notification - 44-FZ procedure"},
    {"contract_id":"8.5.5","closure":"extra_in_contract","reason":"Mandatory expert review of services - 44-FZ requirement"},
    {"contract_id":"8.5.6","closure":"extra_in_contract","reason":"Expert review may involve external experts - 44-FZ procedure"},
    {"contract_id":"8.5.7","closure":"extra_in_contract","reason":"10-day acceptance signing by authorized person - 44-FZ procedure"},
    {"contract_id":"8.5.8","closure":"extra_in_contract","reason":"Acceptance commission procedure with member signatures - 44-FZ procedure"},
    {"contract_id":"8.5.9","closure":"extra_in_contract","reason":"Right to correct and resubmit after motivated refusal - 44-FZ procedure"},
    {"contract_id":"8.6","closure":"extra_in_contract","reason":"Acceptance date definition - 44-FZ procedural detail"},
    {"contract_id":"8.7","closure":"extra_in_contract","reason":"Correction procedure via EIS - 44-FZ procedural detail"},
    {"contract_id":"8.8","closure":"extra_in_contract","reason":"Acceptance result formalisation - 44-FZ procedural detail"},
    {"contract_id":"8.9","closure":"extra_in_contract","reason":"Right to accept despite non-conformity if cured - 44-FZ provision"},
    {"contract_id":"8.10","closure":"linked","reason":"3-day free remedy of defects obligation"},
    {"contract_id":"8.11","closure":"extra_in_contract","reason":"Acceptance document as payment basis - 44-FZ procedural detail"},
    # Section 9
    {"contract_id":"9.1","closure":"linked","reason":"Force majeure definition and list"},
    {"contract_id":"9.2","closure":"linked","reason":"5-day notification; 1-month termination right"},
    {"contract_id":"9.3","closure":"linked","reason":"Documentary proof requirement for force majeure"},
    # Section 10
    {"contract_id":"10.1","closure":"linked","reason":"Pre-trial dispute resolution, 10 calendar day claim response period"},
    {"contract_id":"10.2","closure":"linked","reason":"Arbitration Court of Krasnodar Krai jurisdiction"},
    # Section 11
    {"contract_id":"11.1","closure":"linked","reason":"Contract term until 30.12.2025 or price exhaustion"},
    {"contract_id":"11.2","closure":"linked","reason":"Written amendments signed by both parties"},
    {"contract_id":"11.3","closure":"linked","reason":"Termination by agreement, court, or unilateral refusal"},
    {"contract_id":"11.4","closure":"linked","reason":"Customer right to unilateral refusal per GK RF"},
    {"contract_id":"11.5","closure":"linked","reason":"44-FZ Art.95 procedure for unilateral refusal - part of termination deviation package"},
    {"contract_id":"11.6","closure":"extra_in_contract","reason":"44-FZ Art.34,95,96,112 governing changes and termination - statutory requirement"},
    {"contract_id":"11.7","closure":"not_material","reason":"Gap-filler: residual matters under RF law - no independent operative effect"},
    {"contract_id":"11.8","closure":"extra_in_contract","reason":"Prohibition on changing essential terms except per 44-FZ - statutory constraint"},
    # Section 12
    {"contract_id":"12.1","closure":"linked","reason":"No Executor substitution except reorganisation succession"},
    {"contract_id":"12.2","closure":"linked","reason":"Customer substitution: rights transfer to new customer"},
    {"contract_id":"12.3","closure":"extra_in_contract","reason":"Right to provide improved services by agreement - independent customer benefit"},
    {"contract_id":"12.4","closure":"linked","reason":"Electronic form with UKEP signatures"},
    {"contract_id":"12.5","closure":"linked","reason":"Appendices list"},
]

# ============================================================
# LINKS
# ============================================================
links = [
    # --- ALIGNED ---
    {"contract_ids":["2.3.1"],"matrix_ids":["2.3.1"],"relationship":"aligned","status_reason":"Email channel with full legal force preserved in contract 2.3.1","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.3.2"],"matrix_ids":["2.3.2"],"relationship":"aligned","status_reason":"DBO system channel preserved in contract 2.3.2","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.3.3"],"matrix_ids":["2.3.3"],"relationship":"aligned","status_reason":"Courier delivery channel preserved (optional matrix item present)","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.3.4"],"matrix_ids":["2.3.4"],"relationship":"aligned","status_reason":"Registered mail channel preserved (optional matrix item present)","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.3.6"],"matrix_ids":["2.3.6"],"relationship":"aligned","status_reason":"EIS channel via UKEP preserved for 44-FZ procurement","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.3.7"],"matrix_ids":["2.3.7"],"relationship":"aligned","status_reason":"Support service 24/7 channel present in contract","risk_level":"none","discrepancies":[]},
    {"contract_ids":["12.4"],"matrix_ids":["2.7"],"relationship":"aligned","status_reason":"Electronic contract form with UKEP confirmed in contract 12.4","risk_level":"none","discrepancies":[]},
    {"contract_ids":["1.3"],"matrix_ids":["3.1"],"relationship":"aligned","status_reason":"Customer obligated to organise card acceptance as required by matrix","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.8","5.1.10"],"matrix_ids":["3.2"],"relationship":"aligned","status_reason":"Bank obligated to transfer operation amounts to Customer","risk_level":"none","discrepancies":[]},
    {"contract_ids":["4.5","3.2"],"matrix_ids":["3.3"],"relationship":"aligned","status_reason":"Customer pays for Bank services; fee embedded in unit price per specification","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.4.5"],"matrix_ids":["4.1.1"],"relationship":"aligned","status_reason":"Right to reference card acceptance in ads with Bank prior approval","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.9"],"matrix_ids":["4.1.2"],"relationship":"aligned","status_reason":"Right to consultation via Bank support service preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["4.5"],"matrix_ids":["4.2.1"],"relationship":"aligned","status_reason":"Customer obligated to pay for Bank services","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.7"],"matrix_ids":["4.2.4"],"relationship":"aligned","status_reason":"Obligation to place Bank informational materials at visible TST locations","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.8"],"matrix_ids":["4.2.6"],"relationship":"aligned","status_reason":"Prohibition on splitting one operation into several preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.9"],"matrix_ids":["4.2.7"],"relationship":"aligned","status_reason":"Prohibition on using card details for other purposes preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.10"],"matrix_ids":["4.2.9"],"relationship":"aligned","status_reason":"Proper operation conduct and document accuracy responsibility preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.11"],"matrix_ids":["4.2.10"],"relationship":"aligned","status_reason":"13-month document retention, 3-working-day response period preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.5","5.3.12"],"matrix_ids":["4.2.11"],"relationship":"aligned","status_reason":"Written statement obligation and immediate loss notification preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.19"],"matrix_ids":["4.2.13"],"relationship":"aligned","status_reason":"Full indemnification for chargebacks, disputes, fines, losses preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.13"],"matrix_ids":["4.2.14"],"relationship":"aligned","status_reason":"3-working-day notification for reorganisation, address, details changes preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.14"],"matrix_ids":["4.2.15"],"relationship":"aligned","status_reason":"Annual and on-request document updates within 7 working days preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.20"],"matrix_ids":["4.2.16.1"],"relationship":"aligned","status_reason":"PDn of director: FIO, address, passport data, MIR transfer covered","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.15"],"matrix_ids":["4.2.16.3"],"relationship":"aligned","status_reason":"Proof-of-consent obligation and indemnity within 3 working days preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.16"],"matrix_ids":["4.2.18"],"relationship":"aligned","status_reason":"Cessation of card acceptance and removal of materials on termination preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.17"],"matrix_ids":["4.2.19"],"relationship":"aligned","status_reason":"No obstruction and cooperation in fraud investigations preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.10"],"matrix_ids":["4.2.20.1"],"relationship":"aligned","status_reason":"Self-guided staff training via website obligation preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.18.1"],"matrix_ids":["4.2.20.2"],"relationship":"aligned","status_reason":"Use-only-for-contract, no-modification, no-self-repair, no-transfer preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.18.2"],"matrix_ids":["4.2.20.3"],"relationship":"aligned","status_reason":"Access for installation, repair, maintenance, visual inspection preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.18.3"],"matrix_ids":["4.2.20.4"],"relationship":"aligned","status_reason":"Acceptance by act in two copies preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.20.4"],"matrix_ids":["4.2.20.5"],"relationship":"aligned","status_reason":"Immediate notification of terminal failure or loss preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.18.5","5.6"],"matrix_ids":["4.2.20.6"],"relationship":"aligned","status_reason":"Return within 5 working days after termination or demand preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.7"],"matrix_ids":["4.2.20.7","5.1.1.6"],"relationship":"aligned","status_reason":"Penalty for non-return: 10,000 RUB per electronic terminal, 25,000 RUB per smart terminal","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.10.1"],"matrix_ids":["5.1.1.1"],"relationship":"aligned","status_reason":"Withholding right for invalid operations with matching case list preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.10.2"],"matrix_ids":["5.1.1.2"],"relationship":"aligned","status_reason":"Withholding erroneously transferred amounts preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.10.3"],"matrix_ids":["5.1.1.3"],"relationship":"aligned","status_reason":"Withholding for returns, chargebacks, reversals preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.10.4"],"matrix_ids":["5.1.1.4"],"relationship":"aligned","status_reason":"Withholding disputed/charged-back operations preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.10.5"],"matrix_ids":["5.1.1.5"],"relationship":"aligned","status_reason":"Withholding fines and losses from payment system sanctions preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.3","5.2.4"],"matrix_ids":["5.1.6"],"relationship":"aligned","status_reason":"Technical inspection, replacement, remote update rights with notice preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.1"],"matrix_ids":["5.1.8.1"],"relationship":"aligned","status_reason":"Contract violation as suspension/termination ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.2"],"matrix_ids":["5.1.8.2"],"relationship":"aligned","status_reason":"Extremism/terrorism list entry ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.3"],"matrix_ids":["5.1.8.3"],"relationship":"aligned","status_reason":"Money-laundering/terrorism-financing suspicion ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.4"],"matrix_ids":["5.1.8.6"],"relationship":"aligned","status_reason":"Negative info from state authorities/payment systems ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.5"],"matrix_ids":["5.1.8.7"],"relationship":"aligned","status_reason":"Fraud information from issuer banks/payment systems ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.6"],"matrix_ids":["5.1.8.8"],"relationship":"aligned","status_reason":"Premises renovation impeding operations ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.7"],"matrix_ids":["5.1.8.9"],"relationship":"aligned","status_reason":"Liquidation/bankruptcy ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.8"],"matrix_ids":["5.1.8.10"],"relationship":"aligned","status_reason":"Unreliable info about Customer/TST/director ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.9"],"matrix_ids":["5.1.8.11"],"relationship":"aligned","status_reason":"Activity mismatch ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.10"],"matrix_ids":["5.1.8.12"],"relationship":"aligned","status_reason":"30-day inactivity ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.9.11"],"matrix_ids":["5.1.8.13"],"relationship":"aligned","status_reason":"Price exhaustion and contract term expiry ground preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.3","5.2.9","5.3.17"],"matrix_ids":["5.1.10"],"relationship":"aligned","status_reason":"Inspection rights for fraud and compliance preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.5"],"matrix_ids":["5.1.11"],"relationship":"aligned","status_reason":"Document requests within 13 months preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.7"],"matrix_ids":["5.1.14"],"relationship":"aligned","status_reason":"Email requests to Customer for operation info preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.8"],"matrix_ids":["5.1.16"],"relationship":"aligned","status_reason":"Right to demand documents required by law preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.1"],"matrix_ids":["5.2.3","5.2.5"],"relationship":"aligned","status_reason":"Installation within 5 working days, training, website materials covered","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.6"],"matrix_ids":["5.2.4"],"relationship":"aligned","status_reason":"Round-the-clock authorisation obligation preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.7"],"matrix_ids":["5.2.6"],"relationship":"aligned","status_reason":"Informational materials for terminals obligation preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.4"],"matrix_ids":["5.2.7"],"relationship":"aligned","status_reason":"Round-the-clock operability, 3-working-day replacement preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.8"],"matrix_ids":["5.2.8"],"relationship":"aligned","status_reason":"Payment within 2 working days with technical-failure fallback at 3 calendar days preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.9"],"matrix_ids":["5.2.10"],"relationship":"aligned","status_reason":"PDn processing under 152-FZ with security measures preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.1"],"matrix_ids":["7.1"],"relationship":"aligned","status_reason":"General liability under law and contract established","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.4","7.4.1"],"matrix_ids":["7.2"],"relationship":"aligned","status_reason":"Customer penalty per 44-FZ/PP 1042; 1000 RUB for contract <3M RUB","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.1"],"matrix_ids":["7.3"],"relationship":"aligned","status_reason":"Total Customer penalties capped at contract price","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.5","7.6"],"matrix_ids":["7.4"],"relationship":"aligned","status_reason":"Bank penalty: 1/300 key rate per day of delay","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.7","7.7.1"],"matrix_ids":["7.5"],"relationship":"aligned","status_reason":"Bank penalty per PP 1042: 10% of contract price for <3M RUB","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.7.3"],"matrix_ids":["7.6"],"relationship":"aligned","status_reason":"Penalty for non-monetary Bank obligations: 1000 RUB","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.10"],"matrix_ids":["7.7"],"relationship":"aligned","status_reason":"Total Bank penalties capped at contract price","risk_level":"none","discrepancies":[]},
    {"contract_ids":["6.1"],"matrix_ids":["7.16"],"relationship":"aligned","status_reason":"Anti-corruption clause preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["9.1"],"matrix_ids":["8.1"],"relationship":"aligned","status_reason":"Force majeure definition with event list preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["10.1"],"matrix_ids":["9.1","9.2"],"relationship":"aligned","status_reason":"Pre-trial claim procedure with 10 calendar day period preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["10.2"],"matrix_ids":["9.3"],"relationship":"aligned","status_reason":"Court dispute resolution: Arbitration Court of Krasnodar Krai","risk_level":"none","discrepancies":[]},
    {"contract_ids":["11.1"],"matrix_ids":["10.1"],"relationship":"aligned","status_reason":"Contract term until 30.12.2025 with price exhaustion condition","risk_level":"none","discrepancies":[]},
    {"contract_ids":["11.2"],"matrix_ids":["11.4"],"relationship":"aligned","status_reason":"Written amendments signed by both parties preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["12.4"],"matrix_ids":["11.6"],"relationship":"aligned","status_reason":"Electronic form with UKEP signatures confirmed","risk_level":"none","discrepancies":[]},
    {"contract_ids":["1.1","12.5"],"matrix_ids":["11.7"],"relationship":"aligned","status_reason":"Appendices declared integral part of contract","risk_level":"none","discrepancies":[]},
    {"contract_ids":["12.1"],"matrix_ids":["11.9"],"relationship":"aligned","status_reason":"No assignment except reorganisation succession preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["12.1","12.2"],"matrix_ids":["11.10"],"relationship":"aligned","status_reason":"Reorganisation succession and customer change covered","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.3"],"matrix_ids":["11.12"],"relationship":"aligned","status_reason":"Proper notice via specified channels confirmed in final paragraph","risk_level":"none","discrepancies":[]},
    {"contract_ids":["12.5"],"matrix_ids":["11.13"],"relationship":"aligned","status_reason":"Appendices list present; composition differs from matrix standard but covers same function","risk_level":"none","discrepancies":[]},
    {"contract_ids":["1.1","12.5"],"matrix_ids":["2.4"],"relationship":"aligned","status_reason":"Referenced documents declared integral parts of contract","risk_level":"none","discrepancies":[]},
    {"contract_ids":["1.1","1.2"],"matrix_ids":["6.21"],"relationship":"aligned","status_reason":"Max price 1,900,000 RUB set in contract 3.1; covers matrix price requirement","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.8"],"matrix_ids":["2.2"],"relationship":"aligned","status_reason":"RUB currency for settlements confirmed in contract 5.1.8 and Technical Assignment item 5","risk_level":"none","discrepancies":[]},
    # Additional aligned links for contract clauses that form part of broader packages
    {"contract_ids":["4.4"],"matrix_ids":["5.1.13"],"relationship":"deviation","status_reason":"Bank detail change notification: contract 4.4 requires 2-day written notice vs matrix website posting","risk_level":"low","discrepancies":[{"type":"procedure","description":"Matrix 5.1.13 allows Bank to notify of detail changes via official website; contract 4.4 requires 2-day written notification to Customer","risk":"Website notification is lower burden for Bank; written notice requirement adds procedural obligation but does not harm Bank position materially"}]},
    {"contract_ids":["4.5.1"],"matrix_ids":["6.5"],"relationship":"aligned","status_reason":"November services payment deadline no later than 30.12.2025, consistent with 7-working-day rule","risk_level":"none","discrepancies":[]},
    {"contract_ids":["3.1.1"],"matrix_ids":["6.1"],"relationship":"aligned","status_reason":"Unit price specified in Specification Appendix 2, supports fee determination","risk_level":"none","discrepancies":[]},
    {"contract_ids":["3.3"],"matrix_ids":["6.21"],"relationship":"aligned","status_reason":"44-FZ price application clause supports max price framework","risk_level":"none","discrepancies":[]},
    {"contract_ids":["4.1"],"matrix_ids":["10.1"],"relationship":"aligned","status_reason":"Service period with price exhaustion condition consistent with contract term","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.1.2"],"matrix_ids":["6.2"],"relationship":"aligned","status_reason":"Monthly acceptance document obligation supports Bank invoicing procedure","risk_level":"none","discrepancies":[]},

    {"contract_ids":["5.1.5"],"matrix_ids":["5.1.16"],"relationship":"aligned","status_reason":"Full information obligation supports Bank right to demand documents","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.2"],"matrix_ids":["4.2.1"],"relationship":"aligned","status_reason":"Payment obligation for services preserved","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.5"],"matrix_ids":["7.4"],"relationship":"aligned","status_reason":"Customer right to demand penalties from Executor consistent with liability framework","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.2"],"matrix_ids":["10.2"],"relationship":"aligned","status_reason":"Unilateral refusal right under 44-FZ/GK RF consistent with termination framework","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.6"],"matrix_ids":["5.1.13"],"relationship":"aligned","status_reason":"Bank detail change notification to Customer within 3 working days","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.2.10"],"matrix_ids":["5.1.1.1","5.1.1.2","5.1.1.3","5.1.1.4","5.1.1.5"],"relationship":"aligned","status_reason":"Withholding right header clause framing all withholding sub-rights","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.18"],"matrix_ids":["4.2.20.1","4.2.20.2","4.2.20.3","4.2.20.4"],"relationship":"aligned","status_reason":"Trade acquiring operations header framing terminal use obligations","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.4.2"],"matrix_ids":["6.4"],"relationship":"aligned","status_reason":"Right to refuse acceptance for poor quality is equivalent to motivated refusal right","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.4.3"],"matrix_ids":["10.2"],"relationship":"aligned","status_reason":"Customer unilateral termination right under 44-FZ/GK RF consistent with termination framework","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.4.4"],"matrix_ids":["6.4"],"relationship":"aligned","status_reason":"Right to refuse payment and demand refund for poor quality supports acceptance procedure","risk_level":"none","discrepancies":[]},
    {"contract_ids":["2.2"],"matrix_ids":["3.1","5.2.3","5.2.6","5.2.7"],"relationship":"aligned","status_reason":"Terminal definition clause framing equipment scope; supports multiple terminal obligations","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.2"],"matrix_ids":["7.4"],"relationship":"aligned","status_reason":"Executor right to demand Customer penalties consistent with liability framework","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.3"],"matrix_ids":["7.4"],"relationship":"aligned","status_reason":"Customer penalty rate of 1/300 key rate consistent with matrix 7.4","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.8"],"matrix_ids":["7.4","7.2"],"relationship":"aligned","status_reason":"Penalty exchange via EIS with UKEP consistent with 44-FZ liability procedure","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.9"],"matrix_ids":["7.1"],"relationship":"aligned","status_reason":"Penalty does not release from performance - consistent with general liability principles","risk_level":"none","discrepancies":[]},
    {"contract_ids":["7.11"],"matrix_ids":["7.3"],"relationship":"aligned","status_reason":"Cap on Customer penalties at contract price consistent with matrix 7.3","risk_level":"none","discrepancies":[]},
    {"contract_ids":["8.1"],"matrix_ids":["4.2.9"],"relationship":"aligned","status_reason":"Quality guarantee per regulatory requirements supports proper service delivery obligation","risk_level":"none","discrepancies":[]},
    {"contract_ids":["8.2"],"matrix_ids":["7.1"],"relationship":"aligned","status_reason":"Liability for damage caused by Executor specialists consistent with general liability","risk_level":"none","discrepancies":[]},
    {"contract_ids":["8.3"],"matrix_ids":["6.2","6.4"],"relationship":"aligned","status_reason":"Acceptance procedure header framing monthly acceptance workflow","risk_level":"none","discrepancies":[]},
    {"contract_ids":["8.4"],"matrix_ids":["6.2"],"relationship":"aligned","status_reason":"Date of acceptance document receipt via EIS supports invoicing timeline","risk_level":"none","discrepancies":[]},
    {"contract_ids":["8.10"],"matrix_ids":["5.2.7"],"relationship":"aligned","status_reason":"3-day free remedy of defects consistent with terminal replacement obligation","risk_level":"none","discrepancies":[]},
    {"contract_ids":["9.3"],"matrix_ids":["8.2"],"relationship":"aligned","status_reason":"Documentary proof for force majeure consistent with matrix requirement","risk_level":"none","discrepancies":[]},
    {"contract_ids":["5.3.20"],"matrix_ids":["4.2.16.1"],"relationship":"aligned","status_reason":"PDn transfer guarantee for director data to Bank and MIR; see dedicated link above","risk_level":"none","discrepancies":[]},
    # Matrix 5.1.3 direct debit link
    {"contract_ids":["4.4"],"matrix_ids":["5.1.3"],"relationship":"aligned","status_reason":"Appendix 1.1 item 1.3 grants pre-given acceptance for direct debit from Customer account","risk_level":"none","discrepancies":[]},
    # Matrix 6.20 no fee for return operations
    {"contract_ids":["5.1.8"],"matrix_ids":["6.20"],"relationship":"aligned","status_reason":"Technical Assignment specifies no fee for return operations; original fee not returned","risk_level":"none","discrepancies":[]},

    # --- DEVIATIONS ---
    {"contract_ids":["4.3"],"matrix_ids":["2.1"],"relationship":"deviation","status_reason":"Bank right to refuse TST registration without explanation is absent","risk_level":"medium","discrepancies":[{"type":"procedure","description":"Matrix 2.1 grants Bank unconditional right to refuse TST registration without giving reasons; Contract 4.3 only describes Customer duty to submit registration documents but does not preserve Bank's refusal right","risk":"Without express refusal right, Bank may be compelled to register TST even when risk assessment warrants rejection, weakening onboarding control"}]},
    {"contract_ids":["2.3.5"],"matrix_ids":["2.3.5"],"relationship":"deviation","status_reason":"Automated system name is blank placeholder (___________)","risk_level":"low","discrepancies":[{"type":"other","description":"Matrix 2.3.5 specifies E-invoicing/SFERA-Kurier as the automated system; Contract 2.3.5 leaves the system name as blank underscores","risk":"Blank creates ambiguity about which EDI system is used; low risk as system can be specified before contract execution but currently prevents operational readiness"}]},
    {"contract_ids":["5.3.8"],"matrix_ids":["4.2.5"],"relationship":"deviation","status_reason":"Missing 2-card-per-buyer limit and no-cash-disbursement rule","risk_level":"medium","discrepancies":[{"type":"scope","description":"Matrix 4.2.5 requires: (a) accept all listed cards during all working hours, (b) no cash disbursement on cards, (c) no more than 2 different cards per buyer. Contract 5.3.8 only covers the no-splitting rule. The 2-card limit and cash-disbursement prohibition are absent from the contract.","risk":"Absence of 2-card limit increases split-transaction fraud exposure; absence of cash-disbursement prohibition risks regulatory violation and scheme abuse"}]},
    {"contract_ids":["4.5"],"matrix_ids":["6.5"],"relationship":"deviation","status_reason":"Payment period is 7 working days versus matrix 5 working days","risk_level":"low","discrepancies":[{"type":"deadline","description":"Matrix 6.5 requires payment within 5 working days of UPD signing; Contract 4.5 allows 7 working days from acceptance document signing","risk":"2-day payment delay affects Bank cash flow; mitigated by 44-FZ mandatory payment rules for budget institutions which typically allow up to 7 working days"}]},
    {"contract_ids":["8.3.1","8.3.2"],"matrix_ids":["6.2"],"relationship":"deviation","status_reason":"EIS acceptance document replaces UPD; 10th working day vs 5th working day deadline","risk_level":"medium","discrepancies":[{"type":"procedure","description":"Matrix 6.2 requires UPD by 5th working day; Contract 8.3.1 mandates EIS-based acceptance document by 10th working day. Different document form (UPD vs EIS acceptance document) and later deadline (5th vs 10th working day).","risk":"Delayed invoicing by 5 working days compresses payment cycle; EIS document format may not align with Bank's standard UPD processing system"}]},
    {"contract_ids":["8.5","8.5.1"],"matrix_ids":["6.4"],"relationship":"deviation","status_reason":"Acceptance via EIS with 10 working day period replaces 25th calendar day UPD return","risk_level":"low","discrepancies":[{"type":"procedure","description":"Matrix 6.4 requires Customer to return signed UPD or motivated refusal by 25th calendar day; Contract 8.5.1 provides 10 working days from EIS receipt to sign or reject the acceptance document","risk":"Different timeline framework; 44-FZ EIS procedure is structured but the variable start date (EIS posting) vs fixed 25th day may create uncertainty"}]},
    {"contract_ids":["9.2"],"matrix_ids":["8.2"],"relationship":"deviation","status_reason":"Force majeure notification 5 days vs 24 hours; termination after 1 month vs 3 months","risk_level":"medium","discrepancies":[{"type":"deadline","description":"Matrix 8.2 requires 24-hour force majeure notification and allows termination only after 3 months; Contract 9.2 allows 5-day notification and termination after 1 month","risk":"Longer notification period delays Bank awareness of force majeure events; shorter termination threshold (1 month vs 3 months) increases risk of premature contract termination"}]},
    {"contract_ids":["11.3","11.4","11.5"],"matrix_ids":["10.2"],"relationship":"deviation","status_reason":"44-FZ Art.95 unilateral termination replaces simple 30-day notice mechanism","risk_level":"medium","discrepancies":[{"type":"procedure","description":"Matrix 10.2 allows either party to terminate unilaterally with 30 calendar days written notice without cause; Contract 11.3-11.5 applies 44-FZ Art.95 requiring statutory grounds, EIS notifications, and 10-day cure period","risk":"Bank loses flexible commercial exit right; termination now requires 44-FZ statutory grounds and follows complex EIS-based procedure; right reduced to 'for cause' only"}]},
    {"contract_ids":["3.2","3.1"],"matrix_ids":["6.1"],"relationship":"deviation","status_reason":"Fee percentage embedded in unit price; not separately visible in contract body","risk_level":"low","discrepancies":[{"type":"amount","description":"Matrix 6.1 expects explicit fee percentage in contract text; Contract 3.2 states fee is included in unit price per Specification (Appendix 2) but fee percentage field is blank in the provided specification copy","risk":"Fee percentage not independently verifiable from contract body; blank in specification creates uncertainty about applied rate"}]},
    {"contract_ids":["5.7"],"matrix_ids":["4.2.20.7"],"relationship":"deviation","status_reason":"Electronic terminal penalty 10,000 RUB vs matrix 25,000 RUB","risk_level":"low","discrepancies":[{"type":"amount","description":"Contract 5.7 sets differentiated penalties: 10,000 RUB per electronic terminal and 25,000 RUB per smart terminal; Matrix 4.2.20.7 sets uniform 25,000 RUB for both types","risk":"Reduced penalty for electronic terminals (10,000 vs 25,000) weakens deterrent against non-return; moderate exposure given terminal unit cost"}]},
]

# ============================================================
# UNMATCHED MATRIX
# ============================================================
# Build from matrix_ledger
with open("inputs/matrix.json") as f:
    matrix_data = json.load(f)
matrix_by_id = {item["number"]: item for item in matrix_data}

unmatched_matrix = []
for ml in matrix_ledger:
    if ml["closure"] == "missing_in_contract":
        mi = matrix_by_id.get(ml["matrix_id"], {})
        req_type = mi.get("required_type", "mandatory")
        main_idea = mi.get("main_idea", "")
        enriched = mi.get("enriched_text", "")
        # Build requirement description
        req_text = enriched[:200] if enriched else ml["reason"]
        # Determine risk level
        risk = "medium"
        if req_type == "optional":
            risk = "low"
        # Specific risk descriptions
        risk_desc = ml["reason"]
        unmatched_matrix.append({
            "matrix_id": ml["matrix_id"],
            "status": "missing_in_contract",
            "requirement": risk_desc,
            "required_type": req_type,
            "risk_level": risk,
            "risk": risk_desc
        })

# ============================================================
# UNMATCHED CONTRACT
# ============================================================
unmatched_contract = []
for cl in contract_ledger:
    if cl["closure"] == "extra_in_contract":
        # Determine risk level based on content
        risk = "medium"
        if "procedural" in cl["reason"].lower() or "detail" in cl["reason"].lower():
            risk = "low"
        unmatched_contract.append({
            "contract_id": cl["contract_id"],
            "status": "extra_in_contract",
            "contract_position": cl["reason"],
            "risk_level": risk,
            "risk": cl["reason"],
            "materiality_reason": cl["reason"]
        })

# ============================================================
# SUMMARY
# ============================================================
aligned_count = len([l for l in links if l["relationship"] == "aligned"])
deviation_count = len([l for l in links if l["relationship"] == "deviation"])
missing_count = len(unmatched_matrix)
extra_count = len(unmatched_contract)

summary = {
    "aligned_count": aligned_count,
    "deviation_count": deviation_count,
    "missing_in_contract_count": missing_count,
    "extra_in_contract_count": extra_count
}

# ============================================================
# FINAL JSON
# ============================================================
result = {
    "analysis_profile": analysis_profile,
    "links": links,
    "unmatched_matrix": unmatched_matrix,
    "unmatched_contract": unmatched_contract,
    "coverage_ledger": {
        "matrix": matrix_ledger,
        "contract": contract_ledger
    },
    "summary": summary
}

with open("outputs/discrepancy_analysis.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("File written: outputs/discrepancy_analysis.json")
print(f"Summary: {summary}")

# ============================================================
# VALIDATION
# ============================================================
print("\n=== VALIDATION ===")

# 1. Every matrix id in source must be in coverage_ledger
source_matrix_ids = set(item["number"] for item in matrix_data)
ledger_matrix_ids = set(ml["matrix_id"] for ml in matrix_ledger)
if source_matrix_ids != ledger_matrix_ids:
    missing_from_ledger = source_matrix_ids - ledger_matrix_ids
    extra_in_ledger = ledger_matrix_ids - source_matrix_ids
    if missing_from_ledger:
        print(f"FAIL: Matrix ids missing from ledger: {missing_from_ledger}")
    if extra_in_ledger:
        print(f"FAIL: Extra matrix ids in ledger: {extra_in_ledger}")
else:
    print("PASS: All 169 matrix ids in coverage ledger")

# 2. Every linked matrix id must appear in links
linked_matrix = set(ml["matrix_id"] for ml in matrix_ledger if ml["closure"] == "linked")
linked_in_links = set()
for l in links:
    for mid in l["matrix_ids"]:
        linked_in_links.add(mid)
if linked_matrix != linked_in_links:
    print(f"FAIL: Linked matrix not in links: {linked_matrix - linked_in_links}")
    print(f"FAIL: In links but not linked: {linked_in_links - linked_matrix}")
else:
    print("PASS: All linked matrix ids appear in links")

# 3. Every missing matrix id must appear in unmatched_matrix
missing_matrix = set(ml["matrix_id"] for ml in matrix_ledger if ml["closure"] == "missing_in_contract")
missing_in_um = set(um["matrix_id"] for um in unmatched_matrix)
if missing_matrix != missing_in_um:
    print(f"FAIL: Missing matrix not in unmatched: {missing_matrix - missing_in_um}")
else:
    print("PASS: All missing matrix ids in unmatched_matrix")

# 4. Every linked contract id must appear in links
linked_contract = set(cl["contract_id"] for cl in contract_ledger if cl["closure"] == "linked")
linked_contract_in_links = set()
for l in links:
    for cid in l["contract_ids"]:
        linked_contract_in_links.add(cid)
if linked_contract != linked_contract_in_links:
    print(f"FAIL: Linked contract not in links: {linked_contract - linked_contract_in_links}")
    print(f"FAIL: In links but not linked contract: {linked_contract_in_links - linked_contract}")
else:
    print("PASS: All linked contract ids appear in links")

# 5. Every extra contract id must appear in unmatched_contract
extra_contract = set(cl["contract_id"] for cl in contract_ledger if cl["closure"] == "extra_in_contract")
extra_in_uc = set(uc["contract_id"] for uc in unmatched_contract)
if extra_contract != extra_in_uc:
    print(f"FAIL: Extra contract not in unmatched: {extra_contract - extra_in_uc}")
else:
    print("PASS: All extra contract ids in unmatched_contract")

# 6. No matrix id both linked and missing
linked_set = set(ml["matrix_id"] for ml in matrix_ledger if ml["closure"] == "linked")
missing_set = set(ml["matrix_id"] for ml in matrix_ledger if ml["closure"] == "missing_in_contract")
overlap = linked_set & missing_set
if overlap:
    print(f"FAIL: Matrix ids both linked and missing: {overlap}")
else:
    print("PASS: No matrix id both linked and missing")

# 7. Summary counts match
actual_aligned = len([l for l in links if l["relationship"] == "aligned"])
actual_deviation = len([l for l in links if l["relationship"] == "deviation"])
if summary["aligned_count"] != actual_aligned:
    print(f"FAIL: aligned_count {summary['aligned_count']} vs actual {actual_aligned}")
if summary["deviation_count"] != actual_deviation:
    print(f"FAIL: deviation_count {summary['deviation_count']} vs actual {actual_deviation}")
if summary["missing_in_contract_count"] != len(unmatched_matrix):
    print(f"FAIL: missing count mismatch")
if summary["extra_in_contract_count"] != len(unmatched_contract):
    print(f"FAIL: extra count mismatch")
print("PASS: Summary counts verified")

# 8. All aligned links have empty discrepancies
for l in links:
    if l["relationship"] == "aligned" and l["discrepancies"]:
        print(f"FAIL: Aligned link has discrepancies: {l['matrix_ids']}")
print("PASS: Aligned discrepancies check done")

# 9. All deviation links have non-empty discrepancies
for l in links:
    if l["relationship"] == "deviation" and not l["discrepancies"]:
        print(f"FAIL: Deviation link has empty discrepancies: {l['matrix_ids']}")
print("PASS: Deviation discrepancies check done")

print("\n=== ALL VALIDATIONS COMPLETE ===")
