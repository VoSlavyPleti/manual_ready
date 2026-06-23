# Status Evaluation Pattern Examples

Use these examples for legal status-evaluation tasks. They calibrate how to
decide pair-level status for each `(matrix_id, contract_id)` candidate and then
derive the compatibility `overall_status`.

Do not copy statuses from examples, spreadsheet labels, prior runs, or
document-specific memories. Each example below is a transferable reasoning
pattern.

## How To Use

For each matrix item and supplied candidate artifact:

1. Rebuild the legal core from the full matrix item.
2. Re-read every supplied candidate clause in context.
3. Evaluate `pair_status` separately for each `contract_id`.
4. Do not transfer coverage between different contract clauses.
5. Build `pair_status_checklist` and `full_match_blockers` for each pair.
6. Run targeted recovery only for a concrete uncovered material element.
7. Derive `overall_status` conservatively from pair statuses.
8. Rewrite evidence so each pair status follows from a concrete legal element.

## Status Examples

### Example: `status/full-pair-with-empty-blockers`

Matrix legal test:

- A concrete right, duty, payment rule, notice rule, or liability allocation
  must exist.

Candidate pair:

- The clause independently preserves the protected party, legal object, trigger,
  measure, and consequence.

Pair result:

- `pair_status`: `full_match`
- `full_match_blockers`: `[]`

Reason:

- Pair-level full is allowed only when no material blocker remains.

### Example: `status/same-matrix-direct-full-framework-partial`

Matrix legal test:

- A matrix item has both an operative mechanism and a framework source.

Candidate pairs:

- Direct operative clause: contains the required duty or right.
- Framework clause: gives the legal source but does not itself create the duty
  or right.

Pair results:

- Direct clause: `pair_status` is `full_match` if all elements are covered.
- Framework clause: `pair_status` is `partial_match`.

Reason:

- A framework carrier can be a useful analogue, but it does not inherit full
  coverage from the direct clause.

### Example: `status/no-cross-candidate-status-lifting`

Matrix legal test:

- Full coverage is achieved only by a package of several clauses.

Candidate pairs:

- Clause A covers the operative duty.
- Clause B covers deadline or procedure.
- Clause C covers survival or legal force.

Pair result:

- Evaluate A, B, and C separately.
- Do not mark B or C `full_match` merely because the package as a whole is
  sufficient.

Reason:

- Row-level comparison may score each contract row separately. Each pair must
  stand on its own legal role.

### Example: `status/framework-carrier-is-partial`

Matrix legal test:

- The row requires a special commercial right, duty, control, or remedy.

Candidate pair:

- A clause incorporates rules, law, standards, or residual regulation but does
  not contain the operative right or duty.

Pair result:

- `pair_status`: `partial_match`
- blocker type: `framework_missing`

Reason:

- Framework language is useful context, not a full substitute for the operative
  mechanism.

### Example: `status/payment-economic-term-blocks-full`

Matrix legal test:

- Payment must preserve object, payer, payee, amount basis, trigger, deadline,
  and collection route.

Candidate pair:

- Payment duty exists, but deadline, amount basis, acceptance route, withholding,
  set-off, demand, or payer/payee is changed.

Pair result:

- `pair_status`: `partial_match`
- blocker type: `deadline_changed`, `amount_changed`, `different`, or `weaker`.

Reason:

- Payment topic is useful, but changed economics block pair-level full.

### Example: `status/liability-trigger-or-cap-blocks-full`

Matrix legal test:

- Liability must protect a party for a specific trigger with a specific formula,
  cap, amount, exception, or accrual period.

Candidate pair:

- General liability exists, but trigger, protected party, cap, penalty amount,
  base, or exception differs.

Pair result:

- `pair_status`: `partial_match`

Reason:

- Liability clauses are not interchangeable when the protected risk or economic
  consequence changes.

### Example: `status/named-channel-generic-notice-blocks-full`

Matrix legal test:

- A named site, mailbox, platform, EDI route, support channel, proof model, or
  procedure is material.

Candidate pair:

- The clause provides only generic notice, generic approval, ordinary document
  exchange, or electronic form.

Pair result:

- `pair_status`: `partial_match` when the generic route is useful but weaker.
- `missing` when it does not perform the protected channel function at all.

Reason:

- A generic channel cannot be full for a named-channel requirement.

### Example: `status/unilateral-rule-vs-bilateral-requirement`

Matrix legal test:

- Both parties must be bound by the same prohibition, right, duty, succession,
  assignment, confidentiality, or survival rule.

Candidate pair:

- The clause binds or protects only one party.

Pair result:

- `pair_status`: `partial_match`
- blocker type: `party_inverted` or `narrower`.

Reason:

- One-sided coverage is narrower than a bilateral requirement.

### Example: `status/scope-channel-narrowing-is-partial`

Matrix legal test:

- A rule must cover several products, channels, terminals, operations, documents,
  persons, risks, or lots.

Candidate pair:

- The clause covers only one active subset.

Pair result:

- `pair_status`: `partial_match`

Reason:

- A useful analogue exists, but scope narrowing blocks full.

### Example: `status/formal-difference-still-full`

Matrix legal test:

- A legal result must be preserved; labels may differ.

Candidate pair:

- Appendix number, document title, procurement label, placeholder, or channel
  label differs, but sender/recipient, trigger, legal force, timing, content,
  and consequence are preserved.

Pair result:

- `pair_status`: `full_match`

Reason:

- Formal labels are not blockers when the enforceable result is unchanged.

### Example: `status/partial-requires-named-blocker`

Matrix legal test:

- A candidate looks close, but the suspected gap must be concrete.

Candidate pair:

- No deadline, amount, formula, party, trigger, channel, scope, procedure, or
  consequence gap can be named after reading the contract.

Pair result:

- `pair_status`: `full_match`

Reason:

- Do not use `partial_match` for uncertainty alone. A pair-level partial needs a
  named blocker.

### Example: `status/recovery-closes-only-gap`

Matrix legal test:

- A candidate omits a concrete material element.

Recovery search:

- Search only for that missing element.
- A separate clause closes the gap.

Pair result:

- Add the recovered clause as its own pair and recompute `overall_status`.

Reason:

- Recovery changes evidence only when it finds the exact missing legal element.

### Example: `status/recovery-confirms-partial`

Matrix legal test:

- A duty, right, payment rule, or liability rule omits a protected limit,
  deadline, formula, channel, or consequence.

Recovery search:

- No clause supplies that exact element.

Pair result:

- `pair_status`: `partial_match`

Reason:

- A useful analogue remains, but the named blocker survives recovery.

### Example: `status/missing-no-useful-candidate`

Matrix legal test:

- A concrete legal function must exist.

Candidate package:

- Empty after false-positive pruning and targeted recovery.

Row result:

- `overall_status`: `missing`
- `contract_analog`: `[]`
- `legal_analysis`: `[]`

Reason:

- `missing` is used only when no useful candidate remains.

### Example: `status/generic-boilerplate-is-missing`

Matrix legal test:

- A concrete duty, right, remedy, channel, payment, liability rule, or product
  activation must exist.

Candidate pair:

- Broad cooperation, good faith, law compliance, ordinary notice,
  confidentiality, or dispute language only.

Pair result:

- Reject the pair; if no useful candidate remains, use `missing`.

Reason:

- Boilerplate does not perform the protected legal function.

### Example: `status/payment-control-vs-general-payment`

Matrix legal test:

- A payment rule requires demand, pre-acceptance, debit, set-off, withholding,
  document-control, or a specific acceptance trigger.

Candidate pair:

- General price or payment duty exists without the control mechanism.

Pair result:

- `pair_status`: `partial_match` if the payment object is useful.
- Reject the pair if it concerns a different payment object.

Reason:

- Payment existence does not prove the protected control route.

### Example: `status/separate-fee-not-general-price`

Matrix legal test:

- A separate service, subscription, terminal, software, or maintenance fee must
  be payable.

Candidate pair:

- Only a general commission, contract price, or ordinary service payment exists.

Pair result:

- Reject as a false positive unless it creates that separate fee.

Reason:

- A separate fee is a different legal object.

### Example: `status/opposite-party-liability-is-missing`

Matrix legal test:

- Liability, cap, fine, shield, or non-liability protects one party.

Candidate pair:

- Similar liability rule protects the opposite party.

Pair result:

- Reject the pair unless it materially explains a broader bilateral regime.

Reason:

- Protected party is a mandatory legal element.

### Example: `status/personal-data-purpose-gap`

Matrix legal test:

- Personal-data transfer or processing must cover a person category, purpose,
  consent, confirmation duty, legal basis, or deadline.

Candidate pair:

- Privacy clause exists but omits one protected person category or purpose.

Pair result:

- `pair_status`: `partial_match`

Reason:

- Privacy coverage is useful but incomplete.

### Example: `status/technical-capability-not-product-activation`

Matrix legal test:

- A product, channel, terminal, software route, or payment method must be active
  under the contract.

Candidate pair:

- Technical capability, checkbox, form field, hardware name, or possible feature
  appears without active duties, price, procedure, support, liability, or
  termination terms.

Pair result:

- Reject as a false positive.

Reason:

- Technical possibility is not enforceable activation.

### Example: `status/direct-plus-context-overall-summary`

Matrix legal test:

- One direct clause is full, while a context clause is only partial.

Candidate pairs:

- Direct clause: `pair_status` is `full_match`.
- Context clause: `pair_status` is `partial_match`.

Row result:

- `overall_status`: `partial_match`

Reason:

- `overall_status` is conservative for compatibility; row-level metrics should
  use `legal_analysis[].pair_status`.

### Example: `status/full-active-profile-only`

Matrix legal test:

- The active profile concerns one product, channel, terminal, payment method, or
  lot; other alternatives are inactive.

Candidate pair:

- Fully covers the active profile and omits inactive alternatives.

Pair result:

- `pair_status`: `full_match`

Reason:

- Inactive alternatives are not blockers unless the current item makes them
  operative.

### Example: `status/termination-ground-vs-procedure`

Matrix legal test:

- The protected element is either the termination ground or the procedure.

Candidate pair:

- Same ground but changed notice, period, settlement, return, survival, or
  continuing consequence.

Pair result:

- `pair_status`: `full_match` if the row protects only the ground.
- `pair_status`: `partial_match` if the row protects procedure or consequence.

Reason:

- The protected element controls status, not the section heading.

### Example: `status/incorporated-document-detail-gap`

Matrix legal test:

- An incorporated document must contain a specific field, tariff, list, location,
  procedure, or limit.

Candidate pair:

- Incorporation exists, but the protected detail is blank, narrower, or deferred.

Pair result:

- `pair_status`: `partial_match`

Reason:

- Legal force exists, but the material content is incomplete.

### Example: `status/economic-placeholder-not-material`

Matrix legal test:

- The item tests existence of a payment or document duty, not the final value of
  a placeholder.

Candidate pair:

- The duty exists and only a site, form, price field, or placeholder value is
  blank.

Pair result:

- `pair_status`: `full_match`

Reason:

- A nonmaterial placeholder does not block full.

## Evidence Check

Before saving output, verify:

- `missing` rows have empty arrays;
- `contract_analog` equals the set of `legal_analysis[].contract_id`;
- every legal-analysis entry has `pair_status`, `pair_status_checklist`, and
  `full_match_blockers`;
- every pair-level `full_match` has empty `discrepancies` and empty blockers;
- every pair-level `partial_match` has a named blocker and checklist gap;
- `overall_status` is derived conservatively from pair statuses;
- every absent material element behind `partial_match` or `missing` was checked
  with targeted recovery search;
- evidence explains why each pair produces its own status.
