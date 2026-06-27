# Missing And Extra Patterns

Use this reference for `unmatched_matrix`, `unmatched_contract`, and coverage
ledger closure. The goal is to avoid both false missing and hidden contract-only
risk.

## Stage Logic

1. Every applicable/evaluable matrix id must be closed as `linked` or
   `missing_in_contract`.
2. Use `missing_in_contract` only after rejecting weak candidates that do not
   share the same legal object and effect.
3. Use `out_of_scope` / `not_applicable` very rarely — only for a row that
   cannot logically exist for this contract at all. A row filtered to an unused
   product/regime is still reported as low-risk `missing_in_contract` (see
   below), so the gap stays visible.
4. Every material contract clause must be closed as `linked` or
   `extra_in_contract`. Use `not_material` only for headings, requisites,
   signatures, blank forms, or definitions without independent legal effect.
5. Public-procurement and EIS clauses are not automatically extra. First test
   them as analogues. If they create independent customer control, refusal,
   correction, withholding, proof, or termination rights with no matrix
   analogue, report `extra_in_contract`.
6. Coverage must be exact-id based. Do not validate by row counts alone.

## Missing Calibration

### Bank Right Missing

Matrix: the Bank may refuse service, verify information, suspend an operation,
withhold funds, receive evidence, or transmit information to a payment system.
Contract: only general cooperation, document request, or lawful-processing.

Result: `missing_in_contract` if the specific Bank right is absent. A generic
formality or compliance clause is a weak candidate, not a cure for a named Bank
right, template framework, source hierarchy, or document regime.

### Mandatory-Law Displacement Without The Same Bank Right

Matrix: the Bank has a specific unilateral right, refusal right, direct-debit
right, or pre-contract discretion. Contract: the procurement regime explains a
different statutory process but does not give the Bank the same enforceable
right.

Result: `missing_in_contract` for the matrix protection. Do not create a weak
`deviation` link solely because mandatory law explains why the template right is
absent.

### Filtered-But-Unused Row Is Low-Risk Missing, Not Out Of Scope

Matrix: a requirement is filtered to internet acquiring, QR-API,
SberPay/biometric payment, smart-terminal, or 223-FZ — a product/regime this
card-present trade contract does not actively use.

Result: `missing_in_contract` at **low risk**, with a note that it targets a
product the contract does not use. Do not close it `out_of_scope`: the Bank
standard still wanted it, so keep the gap visible as a low-priority missing row.
A scope closure removes it from the report entirely; a low-risk missing keeps it
visible while signalling it is not a live risk. This applies to every filtered
row — there is no "but it was filtered, so scope it out" exception.

### Applicable Or Optional But Absent Is Missing

Matrix: the filter matches the profile, or the row is common/optional but
applicable. The required mechanism, QR procedure, Bank right, channel, amount,
fee, deadline, or smart-terminal term is not in the contract.

Result: `missing_in_contract`. Do not use `not_applicable` as a softer synonym
for missing. Optional means lower criticality (low-risk missing if absent), not
non-evaluable — an optional applicable row still needs a real closure.

### Technical Mention Or Partial Overlap Is Still Missing

Matrix: an applicable row requires a named active mechanism — accept all listed
card types, a specific QR/SberPay/QR-API code, auto-connection, suspend
authorization, issuer verification, fraud-information transfer, or following
Bank instructions.
Contract: only terminal capability, a product name in a device table, a single
card example, a general payment method, or broad cooperation appears.

Result: `missing_in_contract`. A technical capability or a secondary detail is
not a final analogue and must not become a weak `deviation` link. Use a link
only if another clause creates the same active mechanism.

### Blank Active Term

Matrix: the standard expects an active fee, amount, percentage, website, or
QR/smart-terminal term for this profile. Contract: the place is blank, omitted,
or deferred elsewhere.

Result: `deviation` if a true analogue exists with the blank hard term;
`missing_in_contract` if no true analogue exists. Not `not_applicable`.

### Matrix Closure Must Mirror The Final Report

An applicable row with no true analogue after source review is closed in
`coverage_ledger.matrix` as `missing_in_contract` **and** listed in
`unmatched_matrix`. The ledger and the report must agree id-for-id.

## Extra And Materiality Calibration

### Materiality Is A Deletion Test

A contract clause is material if deleting it would change any party's right,
duty, deadline, evidence burden, acceptance/payment trigger, remedy, control
right, refusal right, correction duty, withholding right, termination route, or
consequence.

- An operative root that lets a party withhold amounts, charge penalties,
  exchange documents by listed methods, accept through EIS, assign rights, or
  rely on applicable law is material — it creates the legal mechanism.
- Never assign `not_material` to a printed operative clause by default just
  because it was not selected for `links` or `unmatched_contract`, or because a
  neighboring clause was linked. Re-read it and close it as linked or extra.

### Enumerate EIS / Acceptance Children — Each Gets Its Own Closure

Public-procurement acceptance is usually split across several printed children:
document placement, receipt date, representative participation, review period,
expert involvement, motivated refusal, Bank correction, commission signing,
unilateral/deemed acceptance, and defect remedy.

Result: close **each** operative child separately. Use the children that supply
a matrix payment/acceptance trigger in `links`; report each independent customer
review, refusal, correction, expert-review, or withholding right as
`extra_in_contract` when no matrix row gives that right or imposes that burden on
the Bank. Do not hide siblings inside one payment analogue and do not treat them
as headings. If a multi-child acceptance section produced zero extras, you
collapsed it — re-read it clause by clause.

### A Linked Analogue Does Not Absorb Independent Customer Rights

A clause supplies a matrix payment/acceptance/quality/liability/termination
trigger (so it is rightly linked) **and** also gives the customer a separate
monitoring, refusal, refund, damages, correction, evidence, receipt-date, or
quality-control right with no matrix analogue.

Result: keep the link for the shared legal object, and also report the
independent right in `unmatched_contract`. The same source clause can appear in
both `links` and `unmatched_contract` when it carries both propositions. A broad
matrix analogue must not swallow an independent customer/procurement right that
burdens the Bank.

### Contract-Only Procurement Right

The customer has an independent right to inspect, reject, demand correction,
withhold payment, impose a penalty, or terminate, and no matrix row regulates
the same right.

Result: `extra_in_contract` with non-empty risk.

### Force-Majeure Evidence Burden Is Material

A force-majeure clause requires the party relying on it to provide documentary
confirmation from an authorized body.

Result: material evidence burden. Link it to a matrix force-majeure evidence
requirement if one exists; otherwise `extra_in_contract`.

### Contract Locator Inventory Must Come From Source

Derive printed contract locators from `inputs/contract.txt`, then close each
operative child. Do not build the contract coverage ledger from a hand-picked
list containing only clauses already used in links, and do not route the
remainder into a default `not_material` bucket.
