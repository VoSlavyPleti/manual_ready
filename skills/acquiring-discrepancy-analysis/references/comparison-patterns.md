# Comparison Patterns

These examples calibrate legal judgment. Do not copy ids, facts, or wording into
the final artifact unless they are present in the actual inputs.

## 1. One Matrix Item Covered By Several Contract Clauses

Matrix standard:
- settlement occurs after reconciliation;
- refunds and chargebacks may be deducted;
- settlement currency is fixed.

Contract position:
- reconciliation is in an operations clause;
- deductions are in a Bank-rights clause;
- currency is in a payment clause.

Result:
- one grouped `links` item may include all relevant contract locators;
- `aligned` if the package preserves every material element;
- each `atomic_links` row states the exact role of the locator and uses an
  element checklist.

## 2. One Contract Clause Covers Several Matrix Requirements

Matrix standard:
- the merchant must follow payment-system rules;
- the merchant must prevent fraud;
- the merchant must provide documents on request.

Contract position:
- one compliance clause imposes all three duties with the same protected party,
  object, triggers, and consequences.

Result:
- one contract locator may link to several matrix ids;
- the link is valid only because the operative duties are actually preserved,
  not because the clause is broadly worded.

## 3. Weak Topic Match Is Missing, Not Deviation

Matrix standard:
- the Bank has a specific right to deduct a named fee from settlement amounts
  after a defined trigger.

Contract position:
- the contract contains a general payment clause but does not give the same
  deduction right, trigger, or settlement mechanism.

Result:
- do not create `deviation`;
- put the matrix item in `unmatched_matrix`;
- record the payment clause in `rejected_candidates` as weak context.

## 4. Generic Notice Does Not Cover Named Bank Channel

Matrix standard:
- legally significant notices must be delivered through a named Bank channel
  and have evidentiary force.

Contract position:
- a generic written-notice clause allows email or paper notices but does not
  address the named channel or evidentiary force.

Result:
- `deviation` only if it governs the same legal notice process but changes the
  channel, deadline, or evidence effect;
- `missing_in_contract` if it is only a broad notice clause.

## 5. Generic Liability Does Not Cover Specific Remedy

Matrix standard:
- a fixed penalty applies for a specific breach, protected party, trigger,
  calculation method, and cap or no-cap position.

Contract position:
- the contract has only general damages or statutory liability.

Result:
- use `missing_in_contract` when the special remedy is absent;
- use `deviation` only when a true analogue exists but amount, trigger, cap,
  exception, or protected party differs.

## 6. Changed Deadline, Amount, Formula, Or Party Is Deviation

Matrix standard:
- notice is due within one business day;
- penalty is a fixed amount;
- the Bank is the protected party.

Contract position:
- notice is due within five business days;
- penalty is lower, capped, conditional, or absent;
- another party receives the protection.

Result:
- `relationship = deviation`;
- checklist marks `deadline`, `amount_formula_cap`, `party`, or
  `liability_remedy` as `different`;
- discrepancy explains the lost Bank protection.

## 7. Formal Label Difference Is Not Deviation

Matrix standard:
- an appendix, act, form, or channel has a specific label.

Contract position:
- the same legal content appears under a different title.

Result:
- `aligned` if rights, duties, evidentiary effect, deadlines, and consequences
  are preserved;
- naming alone is not a legal gap.

## 8. Mandatory Law Can Preserve The Result

Matrix standard:
- the Bank requires a protection that mandatory law already provides.

Contract position:
- the contract uses the statutory structure and does not waive, narrow, or shift
  the Bank's protection.

Result:
- `aligned` if the legal result is at least as strong for the Bank;
- `deviation` if the contract narrows the statutory protection or adds a
  material burden.

## 9. Mandatory-Law Procedure As Extra Contract Term

Contract position:
- the contract adds procurement, public-system acceptance, customer-control, or
  mandatory-law procedures that create independent rights or duties for the
  customer.

Matrix standard:
- the matrix does not contain an analogue for that customer-side procedure.

Result:
- `unmatched_contract`;
- status `extra_in_contract`;
- risk explains delay, customer leverage, payment control, termination risk, or
  procedural burden for the Bank.

## 10. Material Contract-Only Clause

Contract position:
- the customer may inspect performance, reject results, withhold payment, demand
  corrections, suspend performance, or terminate for convenience.

Matrix standard:
- no matrix requirement creates the same customer-side right.

Result:
- `unmatched_contract`;
- status `extra_in_contract`;
- `materiality_reason` explains the independent legal effect.

## 11. Technical Contract-Only Clause Is Not Material

Contract position:
- heading, signature block, blank requisites table, descriptive recital, or
  definition without operative effect.

Result:
- omit it if unnecessary, or include as `not_material`;
- `materiality_reason` states that it creates no standalone right, duty,
  procedure, economic term, liability, or consequence.

## 12. Selected Product Scope Is Not A Deviation

Matrix standard:
- a requirement lists several product variants, payment instruments, channels,
  or terminal types;
- only one of them is used in the counterparty contract.

Contract position:
- the contract regulates the selected product or channel and preserves the same
  Bank right, merchant duty, deadline, and consequence for that scope.

Result:
- do not mark `deviation` only because unused matrix alternatives are absent;
- mark the scoped element `equivalent` in `value_comparison`;
- use `missing_in_contract` only for an operative module that is required for
  the contract scope and has no analogue.

## 13. Mandatory Procedure Preserves The Result

Matrix standard:
- the Bank standard requires an electronic document, acceptance, payment, or
  signature route with legal force.

Contract position:
- a mandatory public-procurement, EIS, qualified electronic signature, statutory
  acceptance, or statutory payment route supplies the same enforceable result.

Result:
- `aligned` when the Bank keeps the same right, duty, deadline, evidence effect,
  and consequence;
- `value_comparison` records the different route as `equivalent` and explains
  the mandatory legal mechanism;
- `deviation` only if the mandatory route changes a material value, weakens a
  Bank right, or adds a material Bank burden.

## 14. Non-Identical Economic Value Needs A Decision

Matrix standard:
- fee, penalty, cap, VAT treatment, payment base, or settlement formula is fixed
  or legally material.

Contract position:
- the contract uses another amount, formula, source, cap, tax treatment, or
  payment base.

Result:
- `relationship = deviation` unless the legal and economic result is proven
  identical or stronger for the Bank;
- `value_comparison` records both values and marks `different`;
- discrepancy explains the lost economic or enforcement position.

## 15. Same Broad Topic But Different Legal Object

Matrix standard:
- the Bank can reject a merchant terminal registration for risk reasons.

Contract position:
- the customer can reject service acceptance after delivery.

Result:
- both clauses involve rejection, but the legal object and protected party
  differ;
- do not link them;
- the matrix item is `missing_in_contract` and the contract clause may be
  `extra_in_contract` if it has independent effect.
