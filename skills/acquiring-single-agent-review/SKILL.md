---
name: acquiring-single-agent-review
description: "Reference: legal review of an acquiring contract against a Bank standard matrix. Finds aligned coverage, deviations, missing matrix requirements, out-of-scope matrix rows, and material contract-only terms."
---

# Acquiring Single Agent Review

## Purpose

Review a counterparty acquiring contract against the Bank's standard matrix.
The matrix is the Bank's playbook: it states the rights, duties, procedures,
protections, products, and risk allocation the Bank expects to see.

The goal is a source-grounded legal coverage report:

- which matrix requirements are preserved by the contract;
- which true analogues exist but deviate from the Bank standard;
- which applicable matrix requirements are missing from the contract;
- which material contract terms have no matrix analogue and create extra risk.

This is a many-to-many comparison. One contract clause can cover several
matrix requirements, and several contract clauses can collectively satisfy one
matrix requirement.

## Source Of Truth

Use the source text as authority:

- matrix `enriched_text`, `main_idea`, `topics`, `required_type`, and
  applicability filters;
- `inputs/contract.txt` and the exact printed contract locators visible there.

Pre-normalized matrix propositions can help navigation. They do not replace
the matrix source text. Final links and statuses must be grounded in the
matrix source text and contract source text.

Re-read source text before deciding hard terms: deadlines, amounts, formulas,
caps, penalties, protected party, bound party, trigger, procedure, forum,
termination, liability, and consequence.

Every final `contract_id` must be a locator visible in the contract text. Do
not invent suffixes, translated ids, semantic ids, or range labels as final
contract ids. Use explanation fields for interpretation.

Keep matrix ids and contract ids in separate namespaces even when printed
numbers match. A contract clause `5.1.3` and a matrix row `5.1.3` are different
source objects until their texts pass the analogue threshold.

## Review Stance

Protect the Bank standard. The main risk is missing an applicable Bank
protection, missing a material deviation, or failing to report a material
contract-only term.

Do not create artificial risk from formal wording differences. Labels, party
aliases, document names, procurement mechanics, or broader Bank protections are
not deviations when the legal result required by the matrix is preserved.

When a public-procurement or mandatory-law mechanism replaces Bank template
wording, compare legal effect rather than labels. It can be an analogue, a
deviation, an extra term, or the reason a matrix row is not applicable.

## Output

Write the final artifact to `outputs/discrepancy_analysis.json`.

- `analysis_profile`;
- `links` with `relationship: aligned|deviation`;
- `unmatched_matrix` for `missing_in_contract`;
- `unmatched_contract` for `extra_in_contract`;
- `coverage_ledger.matrix`;
- `coverage_ledger.contract`;
- `summary`.

Do not put missing or extra items in `links`. `aligned` links must have empty
`discrepancies`. `deviation` links must name the material legal gap and explain
why it matters for the Bank. Make `summary` counts match the final arrays.
Use `references/output-contract.md` for the exact machine-readable schema.

`not_material` is only an internal contract closure. Do not include
not-material clauses in the final business report.

## Workflow

### Step 1: Orient

Load both `inputs/matrix.json` and `inputs/contract.txt` in full first — read
each file in as few passes as possible (a whole-file read, or a single script
that prints the whole file), before any analysis. The strength of a single-agent
review is holding the whole matrix and the whole contract in one reasoning
context; do not interleave many small chunked reads with analysis, which wastes
budget and fragments the picture. Once both documents are fully loaded,
determine:

- product and payment method;
- terminal/device scope;
- lot and legal regime;
- 44-FZ, 223-FZ, commercial, or common mechanics;
- active and inactive product/channel options;
- party roles despite local labels such as customer, contractor, executor,
  provider, supplier, merchant, enterprise, or Bank.

Use `out_of_scope` / `not_applicable` very sparingly, and prefer
`missing_in_contract` when in doubt. The Bank's report exists to surface gaps,
not to hide them behind a scope label.

A matrix row whose applicability filter names a product/channel the contract
does not actively use — internet acquiring, QR / SberPay, biometric payment,
smart-terminal-only, 223-FZ — is still a Bank requirement this contract did not
cover. Report it as **`missing_in_contract` at low risk** with a short note that
it targets a product the contract does not use. Do **not** close it
`out_of_scope`: a scope closure removes the requirement from the report
entirely, but the Bank still wants to see "this standard requirement is absent;
it concerns a product you did not buy." A scope closure and a low-risk missing
both mean "not a live risk here", but only the missing row keeps the gap
visible.

Reserve `out_of_scope` / `not_applicable` for the rare row that cannot logically
exist for this contract at all. If you can restate the row as "the Bank standard
wanted X, the contract has no X", it is `missing_in_contract` (risk calibrated by
applicability), not out of scope. Never use a scope closure as a softer synonym
for missing, and never scope out a common/optional/mandatory row merely because
no analogue was found.

Slash-separated product/channel lists are alternatives unless the source says
all options are mandatory. If the contract selects one applicable option, the
absence of other inactive options is not a deviation.

### Step 2: Build The Source Map

Identify the real matrix ids and printed contract locators that can appear in
the final answer. If helper scripts are used, derive locators from
`inputs/contract.txt`; do not maintain a hand-picked subset.

For each non-technical source item, understand the legal proposition:

- who is bound and who is protected;
- right, duty, restriction, procedure, or remedy;
- legal object;
- trigger;
- deadline, amount, formula, cap, or penalty if present;
- procedure, channel, or evidence requirement;
- consequence;
- applicability and materiality.

Headings, signatures, requisites, blank forms, and definitions without
operative effect may be closed internally as `not_material` or
`not_evaluable`. Operative public-procurement, payment, acceptance, liability,
termination, assignment, communication, governing-law, price, and appendix or
table terms are material unless source text shows otherwise.

A contract clause is `not_material` only if deleting it would not change any
party's right, duty, deadline, evidence burden, acceptance or payment trigger,
remedy, control right, refusal right, correction duty, withholding right,
termination route, or consequence.

### Step 3: Find Legal Analogues

For each applicable matrix requirement, find true contract analogues by legal
object and legal effect, not by number, heading, or word overlap.

A final link is allowed only when the contract package answers the same legal
question for the relevant parties. Weak thematic similarity is not enough.
Reject candidates that only share generic payment, notice, liability, law,
acceptance, procurement, or compliance wording without the concrete right,
duty, procedure, consequence, or hard term required by the matrix.

Use focused packages. Add a parent, child, companion, appendix, or table row
only when it covers a named legal element of the same matrix requirement. Do
not merge sibling matrix requirements into a broad thematic group when each
sibling has its own legal object or could have a different status.

Run a weak-link audit before finalizing links. If your reason for a link says
the contract only mentions a capability, general compliance, general document
request, generic liability, or that no explicit same right/procedure exists,
that candidate usually does not close the matrix requirement. Convert the row
to `missing_in_contract` unless another contract clause creates the same active
right, duty, procedure, trigger, or consequence. Do not convert it to
`not_applicable` unless the matrix applicability filter itself is inactive for
the contract profile.

For product-specific matrix rows, require the same active product or mechanism.
Technical capability, appendix equipment descriptions, advertising material, or
generic operation wording do not become final links for named QR, SberPay,
QR-API, biometric, or automatic-connection obligations.

Use `references/mapping-patterns.md` for analogue threshold and mapping
calibration.

### Step 4: Sweep Contract-Only Terms

After matrix-to-contract mapping, review each material contract clause for a
matrix analogue before reporting it as extra.

Clauses about price, maximum price, service term, payment, acceptance, document
exchange, liability, penalties, termination/change, governing law, dispute
forum, assignment/succession, appendix lists, product scope, and payment
methods often have matrix analogues. Link them when the same legal object and
effect exist.

When a child clause is linked, check whether an operative root or chapeau clause
creates the legal mechanism for that child: document-exchange methods,
acceptance through EIS, payment basis, withholding right, liability formula,
termination route, or appendix/table incorporation. Add the root only when it is
operative; do not add headings.

A clause can appear in `links` for an analogue and in `unmatched_contract` for
a separate independent extra proposition if the same source text contains both.

Do not let a broad matrix analogue absorb an independent customer,
procurement, or counterparty right that burdens the Bank. If a clause used as
context also creates a customer monitoring right, refusal right,
correction/refund/damages remedy, quality warranty, EIS receipt/date rule,
evidence burden, or special liability rule with no matrix analogue, report that
independent proposition as `extra_in_contract`.

If a helper script assigns a contract locator to `not_material` only by default
or because it was not selected for `links` / `unmatched_contract`, re-read that
locator. A printed operative clause with a right, duty, deadline, review step,
refusal, correction, signing, evidence, withholding, termination, liability, or
consequence cannot be closed by a default `not_material` bucket.

Enumerate before you close. The most damaging contract-only miss is collapsing a
whole operative section into one linked analogue and silently dropping its
children. For each section that contains several printed child clauses —
especially acceptance / приёмка, EIS / ЕИС control, customer-rights, and
liability sections — list every numbered child and give each its own closure
(linked or `extra_in_contract`). A numbered clause carrying an obligation/right
verb (обязан, вправе, проверяет, подписывает, отказывает, удерживает, требует,
возвращает, контролирует) is material and cannot become `not_material` just
because a neighboring clause was linked to a matrix payment/acceptance row.

Self-check: if a multi-child operative section (for example a full acceptance
section such as `8.x`) produced zero `extra_in_contract` rows, you almost
certainly folded independent customer/procurement rights into a linked analogue.
Re-read that section clause by clause before finishing — these customer control,
refusal, correction, expert-review, and withholding rights usually have no
matrix analogue and are exactly the contract-only risk the Bank needs flagged.

Use `references/missing-and-extra-patterns.md` for missing and extra
calibration.

### Step 5: Decide Status

Decide status at group level for each focused linked package:

- `aligned`: the contract preserves the Bank-standard legal result;
- `deviation`: a true analogue exists, but the contract changes, weakens,
  omits, narrows, shifts, inverts, or leaves blank a material element;
- `missing_in_contract`: an applicable matrix requirement has no true analogue;
- `extra_in_contract`: a material contract term has no matrix analogue;
- `out_of_scope` / `not_applicable`: a matrix requirement is inactive for the
  current profile.

Functional equivalence cannot be silent on a hard term. If the matrix contains
a hard term, `aligned` requires the same material element in the contract
package or a source-grounded explanation that mandatory law preserves that
exact legal result. If the analogue preserves only the broad topic or duty but
omits the hard term, use `deviation`.

Do not use low-risk `deviation` for a difference that your own analysis
describes as formal, equivalent, mandatory-law routing, or preserving the same
Bank-standard legal result. Low-risk `deviation` is appropriate for an
applicable blank/placeholder, an omitted hard term, a changed amount/deadline
not preserved by mandatory law, or a weakened Bank protection.

An applicable blank or placeholder is `deviation`, normally low risk. Raise the
risk when the blank prevents identifying a named system, channel, counterparty,
amount, date, or condition needed for performance or enforcement.

Use `references/status-patterns.md` for status calibration.

## Decision Rules

### Analogue Threshold

A true analogue must match the legal object and legal consequence for the
relevant parties. Same section, same topic, or same vocabulary is only a search
signal, not proof. If a candidate is only context or capability, reject it.
Use `deviation` only after a true analogue is found.

### Package Boundaries

Several contract clauses can collectively satisfy one matrix requirement.
However, each added clause must explain which element it covers. A broad parent
or framework clause is included only if it creates the right, duty, procedure,
trigger, consequence, amount, cap, or legal basis used in the comparison.

A gap in one sibling channel, product, right, or procedure does not downgrade
neighboring sibling requirements. Conversely, a missing or weaker hard term in
the true analogue package prevents `aligned`.

### Public Procurement Bridge

44-FZ, 223-FZ, EIS, acceptance, payment, termination, withholding, and
correction mechanics can be:

- an analogue, if they answer the same legal question as the matrix;
- a deviation, if they alter a material Bank-standard element;
- an extra term, if they create an independent customer/procurement right with
  no matrix analogue;
- out of scope, if the matrix row is inactive for the contract profile.

Do not treat mandatory-law wording as automatically extra or automatically
aligned. Compare the legal effect.

If mandatory-law mechanics merely explain why the Bank-standard right is absent
and do not give the Bank the same enforceable right or protection, do not force
a weak `deviation` link. Use `missing_in_contract` for the applicable matrix
requirement and explain the lower or regime-specific risk.

### Bank-Risk Priority

Prefer flagging real `deviation`, `missing_in_contract`, and
`extra_in_contract` risks over smoothing them into `aligned`.

Do not downgrade to `deviation` when the only difference is a formal channel or
document label, a party alias, an inactive product option, a broader or
beneficial Bank right, or a mandatory-law route that preserves the same right,
duty, trigger, amount, deadline, or consequence.

## What This Skill Does Not Do

- It does not compare clauses by numbering.
- It does not treat the counterparty contract as equal to the Bank matrix.
- It does not report headings, requisites, signatures, empty forms, or
  non-operative definitions as business findings.
- It does not create final ids that are not visible in the source text.
- It does not use calibration examples as document-specific answers.

## Quality Checks Before Finishing

- Every source matrix id is closed once in `coverage_ledger.matrix`.
- Every linked matrix id appears in `links`.
- Every `missing_in_contract` matrix id appears in `unmatched_matrix`.
- Out-of-scope/not-applicable rows state the source-based profile reason.
- Every material contract locator is closed as linked, extra, or not material.
- Every linked contract id appears in `links`.
- Every extra contract id appears in `unmatched_contract`.
- No matrix id is both linked and missing.
- No contract id is extra only if it is merely a heading, definition,
  signature, requisite, or empty form.
- Every `deviation` has a named material gap and risk.
- Every `aligned` link has no material discrepancy.

Verify by exact source ids, not by counts alone.
