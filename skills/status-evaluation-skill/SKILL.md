---
name: status-evaluation-skill
description: "Strict legal status evaluation for matrix-contract candidate pairs."
---

# status-evaluation-skill

## Task

For each assigned matrix item and candidate contract package, decide the final
legal status: `full_match`, `partial_match`, or `missing`.

Use these JSON status literals. If task text uses shorthand labels, map
`full match` to `full_match`, `partial` to `partial_match`, and `miss` to
`missing`.

Status terms:

- `full_match` means the contract clauses fully cover every material legal
  requirement of the matrix item.
- `partial_match` means at least one material legal requirement is uncovered,
  incomplete, weakened, materially changed, or inverted, while at least one
  useful legal candidate remains.
- `missing` means no useful contract candidate exists for the matrix item after
  checking the supplied candidate artifact and the targeted recovery search.

This task is status evaluation for supplied matrix-candidate pairs. The supplied
candidate artifact is the primary evidence, but it is not authority. Re-read the
current matrix item and contract text before finalizing status. Do not rely on
benchmark labels, workbook answers, prior document-specific runs, or numbering
patterns.

## Inputs

The task input must provide:

- matrix path or assigned matrix items;
- contract path or full contract text;
- candidate artifact or candidate package for each assigned matrix item;
- assigned matrix ids, range, or batch file;
- exact output path.

Use all available matrix fields:

- `number`;
- `enriched_text` or source text;
- `main_idea`;
- `topics`;
- applicability fields;
- product, terminal, channel, payment-method, lot, and procurement restrictions.

The candidate artifact normally contains `contract_analog` and
`candidate_analysis`. Start from that artifact and use only the supplied inputs.
Do not infer hidden intent behind the artifact.

## Output

Save a JSON array to the exact assigned output path. Each item must use exactly
this schema:

```json
{
  "matrix_id": "<matrix number>",
  "contract_analog": ["<contract clause id>"],
  "overall_status": "full_match|partial_match|missing",
  "legal_analysis": [
    {
      "contract_id": "<contract clause id>",
      "pair_status": "full_match|partial_match",
      "matrix_evidence": "<short legal core of the matrix requirement>",
      "contract_evidence": "<short legal core of the contract clause>",
      "coverage": "<why this clause matters to the status>",
      "discrepancies": ["<pair-level material gap, only for partial_match>"],
      "pair_status_checklist": [
        {
          "element": "<material legal element>",
          "result": "covered|equivalent|different|missing|not_applicable",
          "discrepancy": "<empty unless result is different or missing>"
        }
      ],
      "full_match_blockers": [
        {
          "element": "<material legal element>",
          "blocker_type": "missing|different|narrower|weaker|party_inverted|deadline_changed|amount_changed|framework_missing|procedure_missing",
          "reason": "<why this blocks full_match for this pair>"
        }
      ]
    }
  ],
  "status_checklist": [
    {
      "element": "<material legal element from the matrix>",
      "result": "covered|equivalent|different|missing|not_applicable",
      "contract_ids": ["<contract clause id>"],
      "discrepancy": "<empty unless result is different or missing>"
    }
  ]
}
```

Rules:

- include exactly the assigned matrix ids once each;
- preserve `matrix_id` from the matrix `number` field;
- preserve contract ids exactly as they appear in the contract;
- include recovered contract clauses in `contract_analog` when they are needed
  for the final status;
- do not add fields outside the schema;
- for final `missing`, use `contract_analog: []` and `legal_analysis: []`;
- evaluate `pair_status` separately for every `legal_analysis[].contract_id`;
- `pair_status` must be `full_match` or `partial_match`; `missing` is expressed
  by an empty candidate set, not by a pair entry;
- for pair-level `full_match`, `discrepancies` and `full_match_blockers` must be
  empty;
- for pair-level `partial_match`, name a concrete material gap in
  `discrepancies`, `pair_status_checklist`, and `full_match_blockers`;
- `status_checklist` is mandatory for every row and must cover the material
  matrix elements used to decide status;
- `status_checklist[].result` must be one of `covered`, `equivalent`,
  `different`, `missing`, or `not_applicable`;
- `contract_analog` must equal the set of `legal_analysis[].contract_id`;
- compute `overall_status` conservatively: use `missing` when `contract_analog`
  is empty; use `partial_match` when any pair has `pair_status:
  "partial_match"`; otherwise use `full_match`.

Do not write a batch result to `outputs/matrix_contract_mapping.json` unless
that exact path was assigned for this task.

## Status Method

For each assigned matrix item:

1. Read the supplied candidate artifact for the matrix item:
   - listed `contract_analog` ids;
   - candidate evidence, if present;
   - any empty candidate set.
2. Rebuild the active profile:
   - product, channel, terminal, payment method, lot, and procurement mode;
   - active vs inactive alternatives;
   - whether the item is a concrete commercial mechanism, legal framework,
     channel, liability, payment, document, product, or formality item.
3. Extract the legal core:
   - protected party;
   - legal object;
   - operative action;
   - trigger;
   - measure: deadline, amount, formula, cap, channel, document, list, or
     procedure;
   - legal consequence.
4. Re-read every supplied candidate clause in context.
5. Remove false positives.
6. Build `status_checklist` from the material matrix elements.
7. Evaluate every candidate pair with the Pair-Level Status Rules.
8. If any pair has an uncovered material element, or the candidate set is empty,
   run targeted recovery search for the exact uncovered legal elements.
9. Add recovered clauses only when they materially change or explain coverage.
10. Run the Full Match Gate for every pair that could be `full_match`.
11. Recompute `overall_status` conservatively from pair statuses.
12. Rewrite evidence so each pair status follows from material legal elements.

Do not use uncertainty as `partial_match`. A partial row must identify the
specific legal element that is lost or weakened.

## Pair-Level Status Rules

Evaluate the pair `(matrix_id, contract_id)`, not only the matrix item as a
whole. A matrix item may have several useful contract candidates, and those
candidates may have different pair statuses.

Do not transfer coverage from one contract clause to another when deciding
`legal_analysis[].pair_status`. A strong direct clause does not make a separate
framework, context, parent, survival, or notice clause a pair-level
`full_match`.

When full coverage is achieved only by a package of several clauses, assign pair
status by each clause's own legal role:

- a direct operative clause can be `full_match` when it independently preserves
  the protected party, object, trigger, measure, and consequence;
- a framework, parent, survival, context, notice, procedure, or incorporation
  clause is usually `partial_match` unless it itself contains the operative
  duty or right being tested;
- a payment, liability, or termination companion can be `full_match` only for a
  matrix item whose protected legal element is exactly that companion rule.

The top-level `overall_status` is only a compatibility summary. The row-level
status evidence is `legal_analysis[].pair_status`.

## Full Match Gate

Before assigning pair-level `full_match`, challenge that exact pair against
every material legal element in the matrix item. Use `full_match` only when
`full_match_blockers` is empty for that pair. Use pair-level `partial_match`
when any required element is materially absent, weaker, narrower, inverted, or
deferred.

Check at least:

- deadline, date, term, expiry condition, or contract-price exhaustion;
- amount, formula, tariff, cap, base, fine, penalty, or accrual period;
- protected party, payer, payee, responsible party, or inverted obligation;
- trigger, procedure, acceptance route, notice route, document, appendix, or
  channel;
- protected product, operation, person category, risk, or scope;
- companion clause required for legal force, payment mechanics, liability
  consequence, termination procedure, return, survival, or post-termination
  settlement.

If all material checklist elements are `covered`, `equivalent`, or
`not_applicable`, keep `full_match`. If the only difference is a formal label,
document title, appendix number, placeholder, procurement label, or inactive
alternative and the enforceable result is preserved, keep `full_match`.

## Anti-Full Gates

Use these gates before any pair-level `full_match`:

- **Framework Carrier Gate**: framework, rules, law, residual regulation, or
  incorporation clauses are not pair-level `full_match` unless the clause itself
  contains the operative duty or right.
- **Economic Term Gate**: changed deadline, amount, formula, cap, fine, penalty,
  payment basis, withholding, set-off, demand, or acceptance route blocks
  pair-level `full_match`.
- **Procedure / Channel Gate**: generic notice, approval, document exchange, or
  electronic form is not pair-level `full_match` for a named site, mailbox, EDI,
  support channel, proof model, or procedure.
- **Liability Package Gate**: general liability is not pair-level `full_match`
  for a special trigger, protected party, cap, exception, penalty amount, base,
  accrual period, or claim procedure.
- **Party Symmetry Gate**: a one-sided right, duty, prohibition, or exception is
  not pair-level `full_match` for a bilateral requirement.
- **Scope Narrowing Gate**: coverage of only part of the products, channels,
  terminals, operations, documents, persons, risks, or parties blocks pair-level
  `full_match`.

Every gate failure must produce a `full_match_blockers[]` entry and a matching
`pair_status_checklist` item.

## Targeted Recovery Search

The supplied candidate artifact is the first source of truth for what was found,
but it may omit a clause that resolves a gap. Before finalizing `partial_match`
or `missing`, check the current contract and matrix text for the exact missing
legal element.

Use recovery search only for concrete uncovered elements, for example:

- deadline, date, term, contract-price exhaustion, or expiry condition;
- amount, tariff, formula, cap, base, or accrual period;
- party role, payer, payee, protected party, or inverted obligation;
- trigger, notice route, acceptance route, document, appendix, or channel;
- liability consequence, remedy, withholding, set-off, direct debit, refusal,
  suspension, termination, return, survival, or post-termination settlement.

If recovery finds a contract clause that covers the missing element, add it to
the final `contract_analog`, add a `legal_analysis` entry, evaluate its
`pair_status`, and recompute `overall_status`.

If recovery does not find a clause, keep the gap and explain it in
`discrepancies`.

Do not perform a broad second mapping pass. Search narrowly for the legal element
that prevents `full_match` or creates `missing`.

## Priority Rules

When rules conflict, apply them in this order:

1. False-positive rules.
2. Active profile and applicability rules.
3. Mandatory legal package rules.
4. Status rules.
5. Formal-difference rules.

## False Positives

Use `missing` when a supplied or recovered candidate is only topically related
and does not perform the current legal function.

Reject these common near-misses:

- generic electronic form, qualified signature, or EDI for a different signing
  or document function;
- training or initial instruction for a continuing duty to comply with all
  future instructions;
- application form, checkbox, or pre-printed acceptance for an active
  direct-debit/pre-acceptance right;
- technical inspection or non-obstruction for fraud, business-profile,
  restricted-resource, or actual-activity inspection;
- generic document request for issuer-bank contact or transaction verification;
- generic notice, claim, appendix list, website, or document request for a
  named channel, self-referenced notice clause, or exact appendix package;
- generic liability for a specific liability formula, cap, protected party, or
  non-liability shield;
- technical product capability for product activation.

## Mandatory Legal Packages

Before deciding status, verify whether the current row requires a package rather
than a single clause.

One clause is not enough for `full_match` when the matrix item requires a
package. Evaluate parent legal force, operative duty/right, formula or deadline,
procedure, appendix content, and consequence as separate checklist elements.

### Procurement / Statutory Framework

For procurement or statutory contracts, check whether framework clauses change
the current item's protected legal result:

- legal source;
- trigger or procedure;
- payment or acceptance mechanism;
- bank control or remedy;
- liability formula, cap, base, or protected party;
- legal force of notices, documents, or electronic exchange.

Framework clauses can support `partial_match` for broad legal rows, but they do
not create a missing special commercial right.

### Payment Package

For payment, account, invoice, act, acceptance, reimbursement, commission,
withholding, set-off, direct debit, demand, and post-termination settlement
items, verify:

- payment object;
- payer and payee;
- amount basis, tariff, commission, fee, or calculation base;
- trigger and deadline;
- document or acceptance route;
- bank-controlled demand, withholding, set-off, or collection route.

Do not substitute one payment object for another.

### Liability Package

For liability, fine, penalty, cap, personnel responsibility, non-performance,
and non-liability items, verify:

- protected party;
- protected risk;
- general liability regime;
- party-specific or violation-specific clause;
- amount, formula, base, cap, accrual period, or statutory calculation.

Protected party is mandatory. Opposite-party liability is not a match for the
current party's protection.

### Personal Data Package

For personal-data items, verify:

- covered person category;
- processing or transfer purpose;
- consent, confirmation, legal basis, or protection duty;
- deadline or form if the current item protects it.

Use `full_match` only when the same persons and protected purpose are preserved.

### Termination And Continuing Duties

For termination, suspension, unilateral refusal, return, survival, settlement,
and continuing-duty items, verify:

- right and grounds;
- notice and effective date;
- procedure or statutory framework;
- post-termination settlement;
- return, survival, or continuing duties.

Do not import gaps from unrelated survival, merger, or confidentiality clauses
unless the current item requires them.

## Status Rules

### `full_match`

Use pair-level `full_match` only when the evaluated contract clause preserves
the same enforceable result for every material legal element of the current
item. Every material `pair_status_checklist` item must be `covered`,
`equivalent`, or `not_applicable`, and `full_match_blockers` must be empty.

Common full patterns:

- active profile is fully covered and inactive alternatives are not operative;
- a direct clause preserves the same party, object, trigger, duty/right, and
  consequence;
- document, appendix, channel, or form label differs but legal force and
  operative result are preserved;
- a placeholder, blank site, blank price, or VAT wording is not material for the
  current row and the operative duty exists;
- payment package preserves payer, payee, payment object, amount basis, trigger,
  and acceptable deadline;
- no-assignment or no-replacement result is preserved with a standard legal
  exception;
- the current item only requires a direct continuing duty and that duty exists.

### `partial_match`

Use pair-level `partial_match` when a useful analogue exists but a material
legal element is different, weaker, narrower, or still uncovered after targeted
recovery.

Common partial patterns:

- deadline, date, term, amount, formula, cap, party, trigger, channel, document,
  or legal consequence is changed materially;
- party roles are inverted or the protected party changes;
- framework changes legal source, trigger, remedy, control, formula, or
  protected party;
- payment exists but bank-controlled demand, acceptance, withholding, set-off,
  document-control, deadline, payer, or payee differs;
- liability exists but amount, formula, base, cap, accrual period, protected
  party, or protected risk differs;
- named channel, API, website, mailbox, EDI route, or proof model is material
  and the candidate has only a generic or different route;
- candidate covers only part of the required product, document, operation,
  person, or risk;
- a framework clause gives useful background but does not implement the special
  commercial or operational mechanism.

For pair-level `partial_match`, include the useful clause and name the material
gap in `pair_status_checklist`, `full_match_blockers`, and `discrepancies`. Do
not use `partial_match` for an unnamed concern, weak uncertainty, or stylistic
difference.

### `missing`

Use `missing` when no supplied or recovered candidate performs the current legal
function after false positives are removed.

Do not avoid `missing` by keeping:

- same-topic boilerplate;
- a narrower remedy for a broader right;
- a generic law-compliance clause for a concrete obligation;
- a generic e-signature clause for a different document function;
- a generic notice clause for a named-channel item;
- technical capability for product activation;
- opposite-party liability or cap.

## Formal Differences

Do not downgrade when the enforceable result is preserved and the difference is
only formal for the current row:

- appendix number or document title;
- placeholder URL, site, price, or form field;
- inactive alternative product or channel;
- reorganization exception in a no-assignment rule;
- statutory or procurement document label;
- VAT wording when VAT economics are not the protected issue;
- different training/materials location when the operative duty is otherwise
  fixed.

## Evidence

Evidence must be short and legal-function based:

- `matrix_evidence`: required right, duty, object, trigger, measure, or
  consequence;
- `contract_evidence`: what the candidate package actually provides;
- `coverage`: why the clause matters to the status;
- `discrepancies`: only material gaps justifying `partial_match`.
- `status_checklist`: the material elements that determine the final status.
- `pair_status_checklist`: the material elements checked for one
  `(matrix_id, contract_id)` pair.
- `full_match_blockers`: pair-level reasons that prevent `full_match`.

Do not include a clause if the evidence cannot explain how it affects the final
status. Do not add a separate field for recovery notes; the final JSON must keep
the schema above.

## Examples

Use `examples/status-validation-patterns.md` for status-evaluation examples.
Those examples show how to decide `full_match`, `partial_match`, or `missing`
from a matrix requirement and a candidate contract package.

Do not copy statuses from examples, benchmark ids, workbook labels, archived
corpora, or prior document-specific runs.

## Final QA

Before saving:

- every assigned matrix id is present once;
- JSON parses;
- status values are valid;
- `missing` rows have empty arrays;
- `full_match` discrepancies are empty;
- each `partial_match` has a concrete material discrepancy;
- every `full_match` has only `covered`, `equivalent`, or `not_applicable`
  checklist results;
- every `partial_match` has at least one `different` or `missing` checklist
  result with a named discrepancy;
- every `legal_analysis` entry has `pair_status`, `pair_status_checklist`, and
  `full_match_blockers`;
- every pair-level `full_match` has empty `discrepancies` and empty
  `full_match_blockers`;
- every pair-level `partial_match` has a named blocker and matching checklist
  gap;
- every `partial_match` or `missing` caused by an absent element has been checked
  against the contract with targeted recovery search;
- `contract_analog` equals the set of `legal_analysis[].contract_id`;
- no fields outside the output schema are present.
