# Candidate Selection Pattern Examples

Use these examples for candidate-selection tasks. They calibrate how to find
and explain legally useful contract clauses for matrix items.

Use this file only for candidate recall, candidate pruning, and explaining why a
candidate belongs in `contract_analog`.

## How To Use

For each matrix item:

1. Extract the legal function: protected party, object, action, trigger,
   measure, channel or document, and consequence.
2. Use `enriched_text`, `main_idea`, and `topics` to understand the legal
   meaning of the matrix item.
3. Search for direct clauses first.
4. Add parent, sibling, appendix, framework, payment, liability, notice, or
   termination clauses only when they supply a mandatory element.
5. Reject topical clauses that do not change the legal conclusion.
6. Reject numbering, heading, or word-overlap matches when the legal function is
   different.
7. Assign each candidate a legal role and list the matrix elements it covers.
8. Populate `matrix_legal_elements` and `element_candidate_map`.
9. Explain why every selected candidate is legally useful.

## Candidate Examples

### Example: `candidate/direct-operative-clause`

Matrix signal:

- A concrete right, duty, prohibition, payment obligation, notice rule, or
  liability rule must exist.

Good candidate package:

- The direct clause stating the same operative rule.

Why it fits:

- It identifies who must or may act, what the legal object is, when the rule is
  triggered, and what consequence follows.

Do not add:

- Background clauses that only repeat the topic unless they supply a mandatory
  element absent from the direct clause.

### Example: `candidate/direct-and-framework-both-needed`

Matrix signal:

- A direct clause performs the main duty or right, but a framework, parent,
  incorporation, or residual-law clause may be a separate useful analogue.

Good candidate package:

- Direct operative clause.
- Framework or parent clause when it supplies legal force, source, scope,
  survival, or continuing consequence.

Why it fits:

- Row-level evaluation may assess the direct clause and the framework clause as
  separate contract candidates, so both must be available when both perform a
  material function.

### Example: `candidate/cross-reference-companion-clause`

Matrix signal:

- A clause refers to another clause, section, appendix, tariff, form, table, or
  specification for a material element.

Good candidate package:

- Referring clause that creates the right, duty, or framework.
- Referenced clause that supplies scope, deadline, amount, formula, procedure,
  channel, liability consequence, or continuing effect.

Why it fits:

- A cross-reference can carry the element that later determines whether the
  candidate is complete or only partial evidence.

### Example: `candidate/scattered-payment-package`

Matrix signal:

- A payment, fee, commission, invoice, act, acceptance, withholding, set-off, or
  post-termination settlement mechanism is required.

Good candidate package:

- Clause creating the payment duty.
- Clause defining amount basis, tariff, rate, or calculation base.
- Clause defining document, trigger, deadline, payer, payee, or collection
  route.

Why it fits:

- Payment mechanics are commonly split across price, acceptance, settlement,
  and document sections.

### Example: `candidate/payment-control`

Matrix signal:

- The protected element is bank control over payment: demand, pre-acceptance,
  debit, set-off, withholding, invoice approval, or acceptance trigger.

Good candidate package:

- Candidate clauses that actually grant or regulate that control point.

Why it fits:

- A general payment duty may prove money is payable, but not the protected bank
  control mechanism.

Do not add:

- A generic price or payment clause as the only candidate when the matrix tests
  a separate control right.

### Example: `candidate/protective-right-package`

Matrix signal:

- The matrix requires refusal, suspension, withholding, inspection, audit,
  termination, document request, reimbursement, or non-liability.

Good candidate package:

- Clause creating the right.
- Clause defining the trigger.
- Clause defining procedure or consequence.

Why it fits:

- A protective right is not fully evidenced until the protected party, trigger,
  scope, and consequence are clear.

### Example: `candidate/liability-cap-and-trigger-package`

Matrix signal:

- The requirement concerns penalty, fine, damages, cap, formula, accrual period,
  protected party, trigger, exception, or liability shield.

Good candidate package:

- General liability clause when it creates the regime.
- Party-specific or violation-specific clause.
- Formula, cap, base, trigger, exception, or statutory calculation clause.

Why it fits:

- One clause may identify who is liable while another supplies the economic
  consequence.

### Example: `candidate/personal-data-package`

Matrix signal:

- Consent, confirmation of consent, processing basis, transfer purpose, or data
  category is required for employees, representatives, contact persons, or other
  individuals.

Good candidate package:

- Clause covering the relevant persons.
- Clause covering processing or transfer purpose.
- Clause requiring consent, confirmation, protection, or legal basis.

Why it fits:

- Personal-data rows often require both covered persons and purpose; a privacy
  heading alone is not enough.

### Example: `candidate/electronic-document-package`

Matrix signal:

- Electronic exchange, legal force, qualified signature, EDI, platform,
  mailbox, proof of receipt, or named channel matters.

Good candidate package:

- Clause naming the channel or system.
- Clause giving legal force or proof of delivery.
- Clause defining receipt timing or signing rules.

Why it fits:

- The legal function is usually channel plus proof model, not merely electronic
  wording.

### Example: `candidate/procurement-framework`

Matrix signal:

- The row concerns legal admissibility, statutory limits, procurement payment,
  acceptance, residual law, assignment, anti-corruption, or legal compliance.

Good candidate package:

- Procurement or statutory framework clause.
- Payment/acceptance/EIS or platform clause if the row depends on it.
- Residual law, dispute, assignment, or compliance clause where relevant.

Why it fits:

- Framework clauses can be legally useful when the matrix tests the framework
  itself or when the framework changes the operative mechanism.

### Example: `candidate/framework-anchor-candidate`

Matrix signal:

- The matrix item concerns legal framework, payment-system rules, general party
  duties, confidentiality, liability, term, termination, legal succession,
  applicable law, incorporated documents, or continuing effects.

Good candidate package:

- Direct clause, if any.
- Framework anchor that supplies source of regulation, incorporated-document
  force, rule or standard, survival effect, legal succession, or limiting legal
  consequence.

Why it fits:

- Framework anchors can be separate contract-row candidates when they materially
  explain the matrix item's legal function.

### Example: `candidate/termination-package`

Matrix signal:

- Termination, suspension, unilateral refusal, return, survival, settlement, or
  continuing duty is required.

Good candidate package:

- Ground or right to terminate/suspend.
- Notice and effective-date procedure when required.
- Post-termination settlement, return, or survival clause when required.

Why it fits:

- Termination rows often split ground, procedure, and consequences.

### Example: `candidate/active-profile`

Matrix signal:

- The requirement applies only to a specific product, channel, terminal,
  payment method, or lot.

Good candidate package:

- Clauses that create active legal terms for that profile.

Why it fits:

- Candidate selection should follow the active profile, not all products
  mentioned in the matrix.

Do not add:

- Clauses for inactive alternatives unless the current row makes them operative.

### Example: `candidate/technical-capability-is-not-activation`

Matrix signal:

- A product, channel, terminal, software route, or payment method must be active
  under the contract.

Good candidate package:

- Clauses creating activation, duties, pricing, operating procedure, support,
  liability, or termination consequences for that product.

Why it fits:

- Legal activation requires enforceable terms, not just a form field, hardware
  name, checkbox, or technical possibility.

### Example: `candidate/procedure-channel-package`

Matrix signal:

- A named site, mailbox, API, EDI route, support channel, notice path, or proof
  model is protected, or a specific procedure must be followed.

Good candidate package:

- Clauses identifying the channel.
- Clauses defining legal force, timing, or consequence of using it.
- Cross-referenced procedure clauses when they define proof, effective date, or
  required route.

Why it fits:

- Procedure and channel rows require the route plus the legal effect of using or
  failing to use that route.

### Example: `candidate/wrong-control-object`

Matrix signal:

- The matrix protects a specific control object: fraud, business profile,
  transaction verification, terminal security, resource use, documents, or
  actual activity.

Bad candidate:

- A generic inspection, cooperation, support, or document-request clause aimed
  at a different object.

Why to reject:

- Same control vocabulary is not enough when the object and legal consequence
  differ.

### Example: `candidate/generic-boilerplate`

Matrix signal:

- A concrete duty, right, remedy, payment, channel, liability rule, or active
  product term must exist.

Bad candidate:

- Broad cooperation, good faith, ordinary notice, compliance with law,
  confidentiality, or dispute boilerplate.

Why to reject:

- Boilerplate may provide context but does not perform the specific legal
  function.

### Example: `candidate/number-or-word-overlap`

Matrix signal:

- The matrix item has a concrete legal function, but a contract clause only has
  a similar number, heading, or repeated words.

Bad candidate:

- A clause selected because its numbering, title, or vocabulary looks close to
  the matrix item, while its protected party, legal object, trigger, or
  consequence is different.

Why to reject:

- Numbers and words can route search, but they do not prove legal equivalence.
  A candidate belongs only when it performs or materially explains the required
  legal function.

### Example: `candidate/evidence-pruning`

Matrix signal:

- One direct clause already contains every mandatory legal element.

Good candidate package:

- The direct clause only.

Why it fits:

- Extra parent, sibling, tariff, payment, notice, appendix, or liability clauses
  should not inflate `contract_analog` if they do not change coverage.

### Example: `candidate/omitted-row-recall`

Matrix signal:

- The assigned batch includes an item that the initial search pass missed.

Good candidate process:

- Validate the assigned id list against output ids.
- Search the omitted item from scratch.
- Add the best candidate package or an empty candidate set if no legal function
  is performed.

Why it fits:

- Candidate selection is incomplete if an assigned item disappears.

### Example: `candidate/pre-missing-recovery-payment-framework`

Matrix signal:

- A payment document, deadline, acceptance route, payer, payee, withholding,
  set-off, direct-debit, fee, or post-termination settlement is required.

Good candidate process:

- If the first search finds no direct payment clause, check price, acceptance,
  invoice, act, settlement, reimbursement, set-off, withholding, and framework
  sections before returning an empty candidate set.

Why it fits:

- Payment requirements are often split between commercial, document, acceptance,
  and residual-law clauses.

### Example: `candidate/pre-missing-recovery-termination-package`

Matrix signal:

- A right or duty depends on termination, refusal, suspension, return, survival,
  reorganization, assignment, or post-termination consequences.

Good candidate process:

- If no direct match appears, search termination, continuing duties, return,
  settlement, survival, and legal-successor clauses by legal consequence.

Why it fits:

- The relevant legal effect may sit outside the clause that names the triggering
  right or duty.

### Example: `candidate/false-positive-generic-e-signature`

Matrix signal:

- A specific document channel, platform, proof model, mailbox, EDI route, or
  named electronic exchange mechanism is required.

Bad candidate:

- A generic electronic signature or electronic-form clause that only proves a
  document can be signed electronically.

Why to reject:

- Generic electronic form does not prove the protected channel, receipt model,
  or named route.

### Example: `candidate/false-positive-general-bank-right`

Matrix signal:

- The matrix protects a specific bank right: fraud review, business-profile
  control, issuer verification, restricted-resource control, direct debit,
  withholding, suspension, refusal, or non-liability.

Bad candidate:

- A broad cooperation, inspection, information request, or support clause aimed
  at a different object.

Why to reject:

- A general right is not a candidate unless it reaches the same protected object,
  trigger, and legal consequence.

### Example: `candidate/scattered-package-not-single-clause`

Matrix signal:

- A legal function requires a package: parent legal force plus operative clause
  plus formula, deadline, procedure, appendix, or consequence.

Good candidate package:

- Direct operative clause.
- Companion clause that supplies the missing legal element.

Why it fits:

- Candidate recall should preserve the package needed for later status analysis,
  without adding unrelated context clauses.

## Output Check

Before saving output, verify:

- every assigned matrix id appears once;
- every candidate is tied to a legal function;
- every selected clause has evidence explaining why it belongs;
- every selected clause has a role and covered elements;
- `matrix_legal_elements` lists material elements from matrix text;
- `element_candidate_map` shows found or not-found candidates for each material
  element;
- `candidate_limit_reason` explains why the package stops there;
- empty candidate sets were checked against the relevant recovery zones;
- background clauses are excluded unless they supply a mandatory element;
- topical near-misses are not kept as candidates.
