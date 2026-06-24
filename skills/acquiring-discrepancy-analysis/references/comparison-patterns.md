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

## 12. Parent And Child Locator Recall

Matrix standard:
- the Bank may demand penalties for late performance;
- amount and calculation trigger are material.

Contract position:
- a parent clause grants the penalty right;
- child clauses set amount, trigger, exceptions, and cap.

Result:
- include both parent and child locators when both have legal effect;
- do not cite only the child if the parent contains the operative right;
- do not cite only the parent if the child contains the amount, trigger, or cap.

## 13. Grouped Package And Atomic Rows

Matrix standard:
- one requirement needs a parent right, an operative duty, and a formula.

Contract position:
- several clauses jointly preserve the complete result.

Grouped result:
- one `links` item may be `aligned`.

Atomic result:
- create one row for each real matrix-contract pair;
- each row has `coverage_role`, `analogue_strength`, `element_checklist`, and
  `status_reason`;
- do not mark a necessary package clause as `deviation` merely because it covers
  only its role. `deviation` needs a named material gap.

## 14. Same Broad Topic But Different Legal Object

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

## 15. Procurement Payment Mechanism Is A Deviation

Matrix standard:
- the Bank is paid or may settle, deduct, or reconcile under the bank-standard
  mechanism.

Contract position:
- the same payment obligation is controlled by a public-contract mechanism,
  budget payment, acceptance document, payment order, EIS act, or statutory
  customer approval.

Result:
- create a legal link if the payment object is the same;
- use `deviation` when the contract changes the deadline, payer action,
  acceptance condition, deduction right, or enforceability of payment.

## 16. Procurement Termination Procedure Is A Deviation

Matrix standard:
- a party has a termination or unilateral refusal right with defined conditions.

Contract position:
- public-contract wording gives a similar termination path but changes notice,
  customer procedure, allowed grounds, effective date, or consequences.

Result:
- do not discard the clause as unrelated merely because it uses statutory
  language;
- link it as `deviation` when the same legal object is governed differently.

## 17. Generic QR Or Terminal Capability Is Not A Bank Product Analogue

Matrix standard:
- a named QR, API, mobile payment, registration, or operational rule is
  required.

Contract position:
- a terminal must display a QR code or support contactless/card payment.

Result:
- this is weak context unless it preserves the named product, channel, trigger,
  procedure, and consequence;
- put the matrix item in `unmatched_matrix` and record the generic clause as a
  rejected candidate.

## 18. Appendix Locator Must Be Real

Contract position:
- an appendix is mentioned in clause text, but the appendix subdivision is not
  printed as a standalone locator in the source contract text.

Result:
- do not use the invented appendix subdivision as `contract_id`;
- cite the nearest real clause or printed appendix locator and describe the
  appendix content in `coverage`.

## 19. Contract-Only Operative Child Clause

Contract position:
- a public-contract acceptance section has children for EIS signing, motivated
  refusal, correction, payment hold, or customer rejection.

Result:
- report child clauses with independent legal effect as `extra_in_contract`;
- omit headings and repeat-only children that add no right, duty, procedure,
  remedy, or consequence.
