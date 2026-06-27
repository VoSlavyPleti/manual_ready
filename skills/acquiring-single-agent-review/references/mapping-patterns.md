# Mapping Patterns

Use this reference while building `links`. The goal of mapping is not to find
similar words; it is to find true legal analogues by legal object and legal
effect.

## Stage Logic

1. Read the matrix source text for the requirement: `enriched_text`,
   `main_idea`, `topics`, required type, and applicability filters.
2. Identify the material legal elements: party, protected party, right/duty,
   object, trigger, deadline, amount/formula/cap, procedure, consequence.
3. Search the contract for clauses that regulate the same legal object and
   consequence. Numbers, headings, and shared vocabulary are only navigation.
4. Build a focused package only from clauses that cover a named element of the
   matrix requirement.
5. Keep weak thematic candidates out of final `contract_ids`. Record the legal
   result as `missing_in_contract` when no true analogue exists.
6. For public-procurement contracts, first test 44-FZ/EIS clauses as possible
   analogues for payment, acceptance, liability, termination, documents, and
   control before calling them extras.

## Calibration Examples

### Same Number Is Not An Analogue

The contract clause and matrix row share a printed number. Link only if the
source texts regulate the same legal object and effect. In scripts or tables,
keep `contract_id` and `matrix_id` in separate namespaces; never let a shared
number close both sources automatically.

### General Law Or Framework Clause Is Not Universal Coverage

Contract: "services are provided according to law, contract terms, and
incorporated rules", or a general compliance/confidentiality/succession clause.

Right: use it only for a matrix row about the same framework object (compliance
with law, incorporated rules, payment-system rules). It does not cure missing
deadlines, payment mechanisms, Bank rights, liability formulas, product scope,
or procedural hard terms. When it is the analogue for a framework row but lacks
the matrix's named hierarchy, payment-system rules, confidentiality object,
warranty, or protected party, use `deviation`; do not reuse the same general
clause to cure unrelated hard terms.

### A Weak Candidate Becomes Missing, Not A Link

Matrix: a specific active Bank right or mechanism — suspend authorization,
issuer/payment-system verification, fraud-information transfer, QR provision,
auto-connection, accept all listed cards, or follow Bank instructions.
Contract: only general cooperation, technical capability, broad compliance,
general document requests, or reimbursement, and your own reason says "no
explicit" same right exists.

Right: do not keep the weak candidate in `contract_ids`. Use
`missing_in_contract` unless another clause creates the same active legal
mechanism. (Convert to `not_applicable` only if the matrix filter itself is
inactive — see `missing-and-extra-patterns.md`.)

### One Matrix Requirement Covered By A Package

Matrix: one requirement bundles a duty, trigger, payment formula, and deadline.
Contract: the duty is in one clause, the formula in an appendix, the deadline in
a payment clause.

Right: use all clauses as one package if together they cover the same legal
result; each added clause must cover a named element. If a material element is
changed or absent, status is `deviation`.

### Operative Root Travels With Its Child

A child clause carries a deadline or detail, while a nearby operative root or
chapeau creates the legal mechanism: the payment obligation, the
document-exchange method list, EIS acceptance, the withholding right, the
liability regime, or the termination route.

Right: include the operative root together with the child when the matrix
requirement needs both the mechanism and the detail. Do not include a
non-operative heading as a root.

### Same Parent Does Not Mean Same Link

Several child clauses sit under one parent — one about document exchange, one
about payment, one about liability. Do not merge them into one broad link just
because they share a parent. Link each child only to the matrix requirement
whose legal object it actually covers. A gap in one sibling does not downgrade
the others.

### Map By Legal Role, Not Label

The Bank is called contractor/executor/provider and the merchant is called
customer. Map by legal role and consequence: a customer duty can be the matrix
merchant duty, and an executor right can be the matrix Bank right when the legal
object and consequence match.

### Public-Procurement Acceptance As A Payment Analogue

Matrix: payment starts after a legally sufficient operation/acceptance document.
Contract: a public-procurement contract uses an EIS acceptance document as the
payment trigger.

Right: treat the EIS acceptance provision as a possible analogue and classify by
the actual trigger, deadline, party, and consequence. (Its independent customer
control/refusal children are handled in `missing-and-extra-patterns.md`.)

### QR / SberPay Needs An Active Mechanism, Not Capability

Matrix: the Bank standard requires a named QR/SberPay product, QR-API,
auto-connection with a smart terminal, or a Bank-issued QR code.
Contract: only a terminal model, technical QR-display capability, or a generic
appendix QR reference.

Right: reject the candidate. Terminal capability is not a final analogue for a
named QR/SberPay obligation. Use `missing_in_contract` unless the contract
creates the same active product, API, auto-connection, or payment mechanism.

### Term And Price-Cap Form One Duration Package

Matrix: the contract is effective until a date or until the contract price is
exhausted. Contract: one clause states maximum price/volume by customer need,
another states the service period or price-exhaustion stop.

Right: treat them as one focused duration/price-exhaustion package. Do not report
them as unrelated extras before checking the matrix term and price-cap rows.

### Commercial Carrier Rows Are Link Candidates

A payment/term/price matrix requirement depends on maximum price, unit price,
volume cap, payment basis, acceptance document, or price-exhaustion rule, and
those elements live in separate contract carrier rows (subject/volume, maximum
price, specification, acceptance document, payment deadline).

Right: include the carrier rows that supply the element being compared. Do not
replace a visible carrier row with a generic section title or appendix label.

### Liability / Penalty Package: Root, Direction, Formula, Cap

A liability section has a clause granting the penalty-demand right, child clauses
with the fine formula/percentage/fixed amount, and a clause with a total cap or
exception.

Right: for one breach direction, map the demand-right row to the matrix
demand-right row, and map formula and cap rows for the same direction together.
Do not mark the formula aligned while missing the cap, do not classify the cap
as extra before checking neighboring matrix liability rows, and never use a
customer-breach clause to close a Bank-breach requirement.

### Contract-Side Analogue Sweep Before Calling Extra

A contract clause states maximum price, service period, payment basis, dispute
forum, termination route, assignment rule, appendix list, or governing-law
fallback. Search the matrix for the same legal object and effect first; use
`extra_in_contract` only when no true matrix analogue exists.

### Final Locator Is The Exact Printed Source Id

A final `contract_id` must be a locator printed in the contract text.

- Wrong: `Appendix_fee`, `8.5.2-8.5.4`, `8.1-8.5.9`, a translated/semantic
  suffix, or a generic appendix title used to stand in for a specific row.
- Right: use the most specific visible locator — an appendix paragraph or table
  row — when that row itself carries the legal term (currency, device condition,
  product scope, commission basis, payment method, fee). Do not demote a material
  appendix/table row to evidence-only merely because it sits in an appendix, and
  do not collapse several material children into one section range. Put
  descriptions in evidence/reason fields, not inside `contract_id`.
