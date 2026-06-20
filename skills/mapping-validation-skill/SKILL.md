---
name: mapping-validation-skill
description: "Validates and directly corrects contract-matrix mapping batches for recall, false positives, status, and evidence defects."
---

# mapping-validation-skill

Use this skill for independent legal QA of a batch already produced with
`mapping-skill`.

The validator is the final legal reviewer for its batch. If the primary result
is correct, preserve it. If the primary result contains a material error, fix it
directly and save the corrected batch. Do not create a separate issue report or
ask for another correction pass.

## Inputs

The validator receives:

- `matrix_path` and `matrix_host_path`;
- `contract_path` and `contract_host_path`;
- `primary_batch_path` and `primary_batch_host_path`;
- `matrix_ids`;
- `validated_batch_output_path` and `validated_batch_output_host_path`.

Read the primary batch JSON, then independently check each assigned matrix id
against the matrix and contract.

## Output

Save a JSON array to the exact assigned `validated_batch_output_path`.

The output is not a validation report. It is the final validated mapping batch
and must follow the same schema as `mapping-skill`:

```json
{
  "matrix_id": "<matrix_id>",
  "contract_analog": ["<contract_clause_id>"],
  "overall_status": "full_match|partial_match|missing",
  "legal_analysis": [
    {
      "contract_id": "<contract_clause_id>",
      "matrix_evidence": "<short legal core of the matrix requirement>",
      "contract_evidence": "<short legal core of the contract clause>",
      "coverage": "<what this clause covers>",
      "discrepancies": ["<material gap, only for partial_match>"]
    }
  ]
}
```

For each assigned matrix id:

- keep the primary row unchanged if it is legally correct and schema-valid;
- replace the row if recall, false positives, status, or evidence are materially
  wrong;
- create a fresh row if the primary batch omitted the assigned id;
- preserve exact matrix ids from the matrix `number` field;
- preserve exact contract ids as they appear in the contract;
- include no fields outside the `mapping-skill` schema.

## Validation And Correction Focus

### 1. Recall gaps

Look for missing contract clauses that should be included because they
contribute to the legal conclusion.

Check:

- parent clauses that create the right, duty, liability, payment, notice,
  termination, inspection, or incorporated-document mechanism;
- child clauses that supply deadline, trigger, amount, formula, exception,
  document list, scope, or consequence;
- sibling clauses in the same legal mechanism;
- definitions and defined terms that change scope;
- cross-references;
- appendices, tables, forms, specifications, tariffs, technical assignments;
- payment, acceptance, invoice, withholding, set-off, settlement,
  post-termination settlement sections;
- liability, penalty, cap, claim, procurement, EIS, electronic workflow,
  notice, termination, data, audit, and control sections.

Correct the row when a missing clause changes coverage, status, or evidence.

Do not add context that does not change the legal conclusion.

### 2. False positives

Remove included candidates that do not perform a mandatory legal function from
the matrix item.

Common false positives:

- same section or same topic only;
- generic compliance with law or contract when the matrix item requires a
  concrete commercial, operational, payment, notice, control, liability, or
  document function;
- generic liability without required formula, amount, base, cap, trigger, or
  protected party;
- generic notice/e-signature/electronic-form wording instead of a required
  specific channel, document, delivery effect, or receipt rule;
- generic appendix list instead of required appendix content or legal effect;
- inactive product, payment method, channel, terminal, or service;
- technical capability instead of activation, payment, duty, service, notice,
  liability, or legal consequence;
- wrong legal object despite similar words.

If all candidates are false positives, return `missing` with empty arrays.

Do not treat a legal-framework clause as a false positive when the matrix item
itself requires compliance with mandatory law, 44-FZ/procurement procedure,
EIS/claim framework, statutory admissibility, or residual regulation by Russian
law. In that case, preserve or add the framework clause as `partial_match`
unless a more specific contract package fully preserves the required result.

### 3. Status errors

Check the whole candidate package, not each candidate separately.

Correct `overall_status` when:

- `full_match` was assigned despite a material gap;
- `partial_match` was assigned even though the package fully preserves the
  matrix result;
- `missing` was assigned despite a useful legal analogue;
- `partial_match` was assigned from a topical near-miss with no useful legal
  function.

Material differences usually require `partial_match`:

- different deadline, amount, formula, cap, base, trigger, payer, payee, or
  accrual period;
- different penalty/liability source or calculation regime, such as a
  procurement decree replacing the matrix appendix, tariff, amount, or formula;
- a specific court or forum replacing a broader Russian-law jurisdiction model,
  when the matrix protects that broader model;
- weaker right, softer duty, optional mechanism, extra approval, or future
  agreement;
- different protected party or risk allocation;
- missing named channel, system, API, site, delivery address, or mailbox when
  the matrix item requires that exact channel as part of the legal mechanism,
  such as `E-invoicing`, `SFERA-Kurier`, or a PCI DSS reporting email;
- missing document, channel, control point, payment mechanism, acceptance
  trigger, withholding/set-off right, inspection right, termination power,
  liability consequence, or post-termination settlement mechanism;
- narrower active product, terminal, operation, document package, or service
  scope.

Formal differences should not downgrade to `partial_match`:

- appendix number;
- form title;
- document label;
- channel/system label only when the same sender, recipient, delivery duty,
  channel certainty, and legal effect are preserved;
- missing exact channel number when sender, recipient, delivery duty, and legal
  effect are preserved;
- blank technical URL or form placeholder when the enforceable duty itself is
  already fixed and does not depend on that placeholder's content;
- provider/service-company label;
- inactive alternatives listed in the matrix but not activated by the contract,
  such as QR, SberPay, NFC, internet resource, SPEP, or smart terminal when the
  contract profile is POS/card/electronic terminal;
- procurement, EIS, electronic-platform, claim, or acceptance procedure when it
  preserves the same enforceable result.

The formal-difference rule does not apply when the matrix item specifically
requires a named EDI system, API, website, email address, or other channel as an
operative element. In that case, an unnamed automated system, generic website,
or missing email is a material gap and usually requires `partial_match`.

For 44-FZ/EIS contracts, do not downgrade only because the contract uses:

- EIS acceptance document instead of UPD;
- EIS placement of signed acceptance or motivated refusal instead of returning
  a bank-template document;
- procurement payment terms or acceptance triggers instead of bank-template
  payment wording;
- termination by agreement, court decision, or unilateral refusal under Russian
  civil law/44-FZ instead of a template notice period;
- the statutory ban/exception for changing the contractor instead of a general
  assignment clause.

Downgrade these only when the procurement framework removes the required duty,
deadline, document, protection, or economic result.

### 4. Evidence defects

Fix evidence when it:

- only repeats a topic;
- does not identify who must/may do what;
- omits trigger, object, deadline, amount/formula, channel, or consequence when
  those are status-relevant;
- cannot explain why the candidate supports `full_match` or `partial_match`;
- does not explain the material gap for `partial_match`.

Keep evidence short. It must justify the legal result, not summarize the whole
clause.

## Correction Rules

- Apply `mapping-skill` for every row you replace.
- Do not mark `full_match` if any active mandatory element remains materially
  different or uncovered.
- Do not mark `full_match` when penalty economics, formula, source, cap, base,
  accrual period, or protected jurisdiction model materially differ.
- Do not mark `missing` for a liability or penalty item until the whole
  liability package has been checked: framework clause, protected party,
  violation type, formula/base/cap, and any statutory procurement formula.
- Do not mark `partial_match` for a clause that has no useful legal function.
- Do not mark `missing` when a useful but weaker legal analogue exists.
- Do not mark `missing` for a general law, 44-FZ, procurement, EIS, claim, or
  Russian-law fallback clause when that framework is the legal function required
  by the matrix item.
- Do not keep `partial_match` only because the matrix lists inactive
  alternatives not activated by the contract profile.
- Do not keep `partial_match` only because inactive QR, SberPay, internet
  resource, SPEP, NFC, or smart-terminal wording is absent when the active
  POS/card/electronic-terminal rule is fully preserved.
- Do not keep `partial_match` only because a price, tariff, or contract amount
  field is blank when the matrix itself uses a placeholder or says the exact
  value is not contradiction-relevant.
- Do not transfer a gap from a linked clause to the current matrix item unless
  that gap is part of the current item's status profile.
- Do not keep `partial_match` only because a 44-FZ/EIS procedure uses different
  labels, documents, channels, or statutory mechanics while preserving the same
  enforceable result.
- Preserve strong packages even when wording differs.
- Remove topical packages even when wording is similar.
- For `full_match`, use empty `discrepancies`.
- For `partial_match`, include at least one concrete material discrepancy.
- For `missing`, use `contract_analog: []` and `legal_analysis: []`.

## Final Check

Before saving the validated batch:

- include exactly the assigned matrix ids, once each;
- preserve matrix ids exactly from the matrix `number` field;
- output valid JSON only;
- use no markdown;
- use no validation-report fields such as `decision`, `issues`, or
  `validator_notes`;
- save to the exact assigned output path.
