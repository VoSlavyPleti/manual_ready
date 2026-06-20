# Gold Pattern Examples

Compact calibration file for legal matrix-to-contract matching.

Use this file only after applying `../SKILL.md`. It is not a lookup table and
does not contain ready answers by document number. Compare the current matrix
requirement with the current contract text every time.

The archived full corpus is kept at
`examples/archive/gold-patterns.full-corpus.md`. Do not load it during normal
work. Open it only for offline audit or when the orchestrator explicitly asks
for corpus review.

## How To Use

1. Build the `search profile` from `main_idea` and `topics`.
2. Build the `status profile` from the full matrix text.
3. Find direct candidates.
4. Harvest the linked legal package: parent, child, sibling, appendix,
   specification, table, form, tariff, payment, liability, notice,
   termination, procurement, or electronic-workflow provisions.
5. Reject topical near-misses.
6. Assign one status to the whole package.

## Status Calibration

### `full_match`

Use `full_match` when the contract package preserves the same enforceable
legal result as the matrix:

- same protected side or functional equivalent;
- same legal object;
- same operative action;
- same trigger;
- same deadline, amount, formula, channel, form, or procedure where required;
- same legal consequence or an equivalent enforceable consequence.

Formal wording differences do not matter if the practical legal result is the
same.

### `partial_match`

Use `partial_match` when a candidate performs a useful part of the required
legal function, but the package leaves a material gap or changes the protected
result.

Material gaps include:

- different deadline;
- different amount, formula, cap, base, payer, payee, or payment trigger;
- weaker right or softer obligation;
- different party protected by the mechanism;
- missing control point, document, channel, or approval mechanism;
- narrower product, terminal, operation, or service scope;
- future agreement instead of an enforceable current obligation.

### `missing`

Use `missing` when no clause performs a useful part of the required legal
function. Similar topic, same section, same terminology, or general context is
not enough.

Return no candidates for `missing`.

## Recall Patterns

### Pattern: `recall/parent-child-framework`

Good:

- Parent clause creates the duty, right, liability regime, settlement
  mechanism, or incorporated procedure.
- Child clause supplies the exact trigger, amount, deadline, exception, or
  document.
- Framework clause makes the mechanism enforceable through procurement,
  electronic workflow, acceptance, claim, payment, or statutory procedure.
- Together they answer who must/may do what, when, through which document or
  procedure, and with what consequence.

Why this is a strong analogue:

- The child clause alone often proves only one element.
- The parent/framework clause often proves legal force.
- Missing one part of the package lowers recall and can turn a full package
  into an apparent partial.

Anti-pattern:

- Returning only the clause with the amount or deadline when the matrix also
  requires the right to charge, withhold, refuse, inspect, terminate, or demand
  documents.
- Returning only a parent framework clause when the matrix requires the exact
  amount, deadline, trigger, form, or list.

### Pattern: `recall/incorporated-appendix`

Good:

- Main text states that an appendix, tariff, table, statement form,
  specification, or technical assignment is part of the contract.
- The incorporated document contains the required operational detail.
- Both the incorporation clause and the detailed appendix may be needed.

Why this is a strong analogue:

- The appendix supplies content.
- The main text supplies enforceability.

Anti-pattern:

- Returning a generic list of appendices without the appendix content.
- Returning appendix content when the contract never incorporates it.
- Treating a blank form as full coverage when a required field is left
  legally indeterminate.

### Pattern: `recall/scattered-payment-package`

Good:

- One clause defines payment duty.
- Another defines tariff, commission, price, rate, or calculation base.
- Another defines invoice, acceptance, payment term, withholding, set-off,
  bank demand, or post-termination settlement.
- The package together proves the economic mechanism required by the matrix.

Why this is a strong analogue:

- Payment requirements are often distributed across price, acceptance,
  settlement, and liability sections.

Anti-pattern:

- Matching only a general payment clause when the matrix requires a specific
  bank-control mechanism, acceptance trigger, withholding right, invoice form,
  or settlement after termination.

### Pattern: `recall/protective-right-package`

Good:

- The matrix requires a protective right: refusal, suspension, withholding,
  audit, inspection, unilateral termination, document request, risk allocation,
  penalty, or compensation.
- The contract may split the right across a general powers clause, a trigger
  clause, a procedure clause, and a consequence clause.

Why this is a strong analogue:

- A protective right is not fully proved until the protected party, trigger,
  scope, and consequence are all clear.

Anti-pattern:

- Returning only a broad "right to control performance" clause for a matrix
  item that requires inspection of fraud, documents, operations, terminal
  security, or payment compliance.

### Pattern: `recall/liability-package`

Good:

- The matrix requires a penalty, fine, liquidated damages, liability cap, or
  non-performance consequence.
- The contract package may split the mechanism across a general liability
  clause, a party-specific clause, a violation-specific clause, and a formula
  or statutory procurement calculation.
- Collect the package before deciding status.

Why this is a strong analogue:

- One clause may identify the protected party while another supplies the
  formula or confirms that penalties are demandable.
- A procurement formula can still be a useful or full analogue even when it is
  not the same bank-template scale.

Anti-pattern:

- Returning only a delay penalty for a matrix item about non-performance.
- Returning only the customer-liability clause for a matrix item about bank
  liability, or vice versa.
- Marking `missing` before checking the general liability framework and the
  party-specific penalty clause together.

## Status Examples

### Example: `full/formal-difference-only`

Matrix requirement:

- A party must send legally significant documents through an agreed channel.

Contract package:

- Uses a different channel label or document title.
- Still identifies the sender, recipient, delivery method, legal force, and
  moment of receipt.

Status:

- `full_match`

Why:

- The protected legal result is the same. Label differences do not weaken the
  obligation.

Bad status:

- `partial_match` only because the contract uses another appendix number,
  form title, channel label, or procurement document name.

### Example: `full/formal-channel-or-placeholder`

Matrix requirement:

- A party must notify, provide documents, place materials, complete training,
  or exchange legally significant information through a specified channel,
  form, site, or system label.

Contract package:

- Fixes the sender, recipient, duty, deadline, legal effect, and required
  action.
- Uses another channel label, omits the exact template channel number, or has a
  blank technical URL/form placeholder that does not change the enforceable
  duty.
- The matrix does not make the exact system name, API, website, or email
  address an operative element of the requirement.

Status:

- `full_match`

Why:

- The legal result is preserved. A missing label or placeholder is not a
  material gap when the duty is already enforceable.

Bad status:

- `partial_match` only because the exact channel number, site, form label, or
  document title is absent.

### Example: `partial/specific-channel-or-address`

Matrix requirement:

- A party must exchange documents through a named EDI system, named API, named
  website, or send a required document to a specific email address.

Contract package:

- Keeps the general duty and legal force.
- Replaces the named channel with an unnamed automated system, generic website,
  or omits the specific email address.

Status:

- `partial_match`

Why:

- The channel is not just a label. The named system/address is part of the
  operative legal mechanism and audit trail.

Bad status:

- `full_match` because electronic exchange or submission to the bank exists in
  general.

### Example: `full/framework-equivalence`

Matrix requirement:

- A party must accept, pay, notify, or sign documents through a specific
  enforceable procedure.

Contract package:

- Replaces the template mechanism with a procurement, electronic-platform,
  EIS, statutory, claim, or acceptance framework.
- The framework still fixes the duty, trigger, deadline, document, protected
  party, and consequence.

Status:

- `full_match`

Why:

- The legal result is enforceable even though the procedural vocabulary is
  different.

Bad status:

- `partial_match` merely because the bank-template mechanism is not copied
  verbatim.

### Example: `full/placeholder-price-or-vat-exempt`

Matrix requirement:

- Requires that the contract contain a price, tariff, commission percentage,
  payment document, reporting period, or VAT treatment.
- The matrix text itself uses a placeholder, or `main_idea` says the exact price
  is not contradiction-relevant.

Contract package:

- Preserves the enforceable price/tariff/payment mechanism, document, period,
  and deadline.
- Uses a blank amount/percentage placeholder, or states that the service is not
  subject to VAT under mandatory tax law.

Status:

- `full_match`

Why:

- The matrix is testing the existence and structure of the mechanism, not the
  filled commercial value.
- VAT exemption by law is not a weaker legal result when the payment document,
  period, and duty are preserved.

Bad status:

- `partial_match` only because the price field is blank in both template-like
  texts.
- `partial_match` only because the matrix says VAT is included while the
  contract says the service is VAT-exempt by law.

### Example: `full/scoped-linked-gap`

Matrix requirement:

- Requires one specific legal function, such as the bank's right to withhold a
  penalty.

Contract package:

- The current clause fully preserves that function.
- A linked clause contains a separate defect, such as a blank penalty amount,
  but the current matrix item does not require the amount itself.

Status:

- `full_match`

Why:

- Linked clauses are used to understand scope, but their defects should not be
  transferred unless the defect is part of the current status profile.

Bad status:

- `partial_match` because a cross-referenced clause has a gap that belongs to a
  different matrix item.

### Example: `full/active-profile-alternatives`

Matrix requirement:

- A bank template lists several alternative products or channels, such as
  cards, QR, SberPay, NFC, internet resource, SPEP, electronic terminals, or
  smart terminals.

Contract package:

- The contract profile activates only POS/card/electronic-terminal acquiring.
- The contract fully covers the duty, right, payment, notice, or service rule
  for that active profile.

Status:

- `full_match`

Why:

- Missing inactive alternatives do not weaken the active contract result.

Bad status:

- `partial_match` only because QR, SberPay, NFC, internet resource, SPEP, or
  smart terminals are absent when the contract does not activate them.

### Example: `missing/inactive-standalone-channel`

Matrix requirement:

- The whole matrix item is about a standalone inactive channel or service, such
  as QR-API, SberPay, internet resource, SPEP, NFC, or smart-terminal service.

Contract package:

- Mentions the channel only as a technical capability, disclaimer, or background
  term.
- Does not activate the channel and does not create a price, procedure,
  settlement, liability, or duty package for it.

Status:

- `missing`

Why:

- A capability or disclaimer is not a useful legal analogue for a channel that
  is not active in the contract profile.

Bad status:

- `partial_match` because the inactive product name appears somewhere in the
  contract.

### Example: `full/44-fz-eis-substitution`

Matrix requirement:

- A party must sign, return, pay against, refuse, terminate, or change a party
  under a bank-template document or notice procedure.

Contract package:

- Uses a mandatory 44-FZ/EIS/procurement mechanism instead: EIS acceptance
  document, motivated refusal in EIS, procurement payment trigger, termination
  under Russian civil law/44-FZ, or statutory contractor-change rule.
- The duty, protected party, deadline or statutory procedure, document, and
  legal consequence are enforceable.

Status:

- `full_match`

Why:

- The procurement framework is the enforceable substitute for the bank
  template and preserves the same practical legal result.

Bad status:

- `partial_match` only because the document is not called UPD, the action
  occurs in EIS, the payment trigger is an acceptance document, or termination
  follows 44-FZ/GK mechanics.

### Example: `partial/payment-control-weakened`

Matrix requirement:

- The protected party may recover commission, debt, or penalties through a
  defined demand, withholding, set-off, or bank-controlled payment mechanism.

Contract package:

- Contains a general duty to pay, ordinary counterparty payment order, or
  invoice procedure.
- Does not preserve the required trigger, unilateral control, withholding,
  bank demand, acceptance, or deadline.

Status:

- `partial_match`

Why:

- There is a useful payment analogue, but the protected economic/control
  result is weaker.

Bad status:

- `full_match` because "payment exists".
- `missing` when the payment duty exists but lacks the stronger matrix
  mechanism.

### Example: `partial/liability-economics-differ`

Matrix requirement:

- Liability must apply on a specific trigger with a specific amount, formula,
  base, cap, rate, or accrual period.

Contract package:

- Contains liability or penalty language.
- Changes the amount, formula, base, cap, trigger, protected party, or accrual
  period.

Status:

- `partial_match`

Why:

- Liability is legally useful, but different economics change the protected
  result.

Bad status:

- `full_match` because both clauses mention penalties.
- `missing` when the same liability mechanism exists but is weaker or
  narrower.

### Example: `partial/liability-source-differs`

Matrix requirement:

- Liability must use a specified appendix, tariff, amount, formula, cap, base,
  rate, or accrual rule.

Contract package:

- Creates liability for the same party and trigger.
- Replaces the matrix economics with a statutory or procurement calculation,
  such as a government-decree formula.

Status:

- `partial_match`

Why:

- Liability exists, but the economic result is different.

Bad status:

- `full_match` only because the contract contains a valid penalty regime.

### Example: `partial/forum-narrowed`

Matrix requirement:

- Disputes are resolved under a broader Russian-law jurisdiction or general
  statutory model.

Contract package:

- Provides a specific court, venue, or forum selected by the contract.

Status:

- `partial_match`

Why:

- The court mechanism is useful, but it narrows or changes the protected
  jurisdiction model.

Bad status:

- `full_match` only because both provisions send disputes to court under
  Russian law.

### Example: `partial/scope-narrower`

Matrix requirement:

- A duty or right covers a defined set of products, payment methods, terminals,
  documents, operations, or services.

Contract package:

- Covers only one active part of the set, or covers a narrower object.
- The matrix requires the broader active scope, not merely an alternative
  selected option.

Status:

- `partial_match`

Why:

- The clause is useful, but coverage is incomplete.

Bad status:

- `full_match` because one product or method is present.
- `missing` when the covered subset is legally relevant.

### Example: `missing/inactive-product-or-channel`

Matrix requirement:

- Applies to a product, payment method, terminal type, channel, or service
  that is not active in the contract profile.

Contract package:

- Mentions technical capability, marketing name, application form, or general
  possibility.
- Does not activate the product/channel or create a duty, price, procedure,
  notice, settlement, or liability rule for it.

Status:

- `missing`

Why:

- There is no useful legal rule for the active contract profile.

Bad status:

- `partial_match` from a capability mention, blank application, or general
  product description.

### Example: `missing/generic-boilerplate`

Matrix requirement:

- Requires a concrete duty, right, trigger, document, deadline, amount,
  formula, channel, or consequence.

Contract package:

- Only says that parties comply with law, perform the contract, exchange
  documents generally, use electronic signatures, or are liable generally.

Status:

- `missing`

Why:

- Generic boilerplate does not perform the required legal function.

Bad status:

- Returning boilerplate to avoid an empty result.

### Example: `partial/statutory-framework-fallback`

Matrix requirement:

- Requires compliance with mandatory law, a procurement/44-FZ procedure,
  statutory admissibility, EIS/claim framework, or residual regulation by
  applicable Russian law.

Contract package:

- Contains a general clause that performance must comply with applicable law,
  44-FZ, procurement/EIS procedure, claim procedure, or Russian law for matters
  not expressly regulated by the contract.
- Does not contain a more specific clause that fully implements the matrix
  requirement.

Status:

- `partial_match`

Why:

- The clause is general, but it performs the same legal-framework function
  required by the matrix. It is useful coverage, not a topical near-miss.

Bad status:

- `missing` only because the clause is generic.
- `full_match` when the matrix also requires a concrete deadline, amount,
  document, control right, sanction, or operating procedure.

### Example: `missing/wrong-legal-object`

Matrix requirement:

- Concerns one legal object, for example payment documents, fraud control,
  post-termination settlement, terminal operation, card rules, confidential
  data, or unilateral refusal.

Contract package:

- Uses similar words but regulates another object or consequence.

Status:

- `missing`, unless the clause still covers a material part of the required
  function; then use `partial_match`.

Why:

- Same words do not prove the same legal mechanism.

Bad status:

- Matching by section title, shared vocabulary, or proximity.

## Final Check Before Output

For every non-missing row, the answer must be able to say:

- what mandatory matrix element each candidate covers;
- why the package is enough for `full_match`, or exactly what material gap
  remains for `partial_match`;
- why each included candidate changes the status conclusion;
- why rejected near-misses were not useful legal analogues.

If a candidate cannot pass that check, remove it.
