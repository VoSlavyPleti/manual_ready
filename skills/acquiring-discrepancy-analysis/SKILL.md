---
name: acquiring-discrepancy-analysis
description: "Use this skill when comparing a bank acquiring standard matrix with a counterparty acquiring contract to find many-to-many legal correspondences, deviations, missing bank-standard requirements, and material extra contract terms."
---

# Acquiring Discrepancy Analysis

Use this skill for legal discrepancy analysis between a standard bank acquiring
matrix and a counterparty acquiring contract.

## Purpose

Build a many-to-many legal comparison map:

- which bank-standard requirements are preserved by the contract;
- which contract terms deviate from the bank standard;
- which matrix requirements are absent from the contract;
- which material contract terms have no matrix analogue.

The matrix is the Bank's standard. The contract is assessed against that
standard. The documents are not equal sources of policy.

## Inputs

- `inputs/matrix.json`: bank standard matrix. Use `number` as the matrix id.
  Analyze `main_idea`, `topics`, and `enriched_text` as the legal requirement.
- `inputs/contract.txt`: counterparty contract text. Use exact printed clause
  ids when available. If a provision has no printed number, use the exact
  heading, definition label, appendix/table row label, or nearest real locator
  from the document; do not invent numbering.
- `/outputs/discrepancy_analysis.json`: the only final output. Treat this as an
  absolute virtual path rooted at the project workspace.
- `/outputs/working/`: required working area for temporary batch fragments,
  helper scripts, notes, checks, and intermediate files.

Before writing the final artifact, read `references/output-contract.md`.
Use `references/comparison-patterns.md` when calibrating uncertain relationship
or materiality calls.

## Required Working Artifacts

Before comparing the documents, create these working files:

- `/outputs/working/matrix_inventory.json`
- `/outputs/working/contract_inventory.json`
- optional compact batch fragments under `/outputs/working/`

Each inventory entry must contain:

- `id`: exact matrix `number` or exact contract locator as written;
- `proposition`: short legal proposition;
- `party`: party protected or bound by the proposition, if identifiable;
- `right_or_obligation`: operative right, obligation, prohibition, permission,
  or allocation of risk;
- `object`: legal object affected by the proposition;
- `trigger`: event or condition that activates the proposition, if present;
- `material_terms`: deadline, amount, formula, procedure, liability, penalty,
  cap, exception, or consequence, if present;
- `applicability`: `in_scope`, `out_of_scope`, `conditional`, or `unknown`;
- `applicability_reason`: product, channel, terminal, party role, legal regime,
  or document scope reason for the applicability call;
- `materiality`: `material`, `technical`, or `heading`.

Do not start the many-to-many comparison until both inventories exist. The
inventories are legal working tables, not final deliverables.

Keep inventories compact. Do not copy full clause text into inventory entries
unless the text is needed to identify an unnumbered locator. The inventory is an
index for coverage and ids, not the legal memo.

Contract locator discipline:

- final `contract_ids` must be exact printed locators from `inputs/contract.txt`;
- do not use internal aliases such as `Appendix_1`, `app_1`, or translated
  labels in the final artifact;
- if a script needs aliases, store them in an `aliases` field, but keep `id` as
  the printed locator;
- never cite a parenthetical locator unless the parenthetical text is printed in
  the contract.

## Legal Comparison Principles

- Compare legal propositions, not numbering, order, or isolated words.
- A proposition is material when it changes rights, duties, triggers, deadlines,
  amounts, formulas, liability, procedures, scope, parties, exceptions, or
  consequences.
- The first question is applicability. A matrix requirement outside the
  contract's product, channel, terminal type, party role, or legal regime is not
  a weak `deviation`; it is normally `missing_in_contract` unless the contract
  contains an operative analogue for that exact legal object.
- One matrix requirement may be covered by several contract provisions.
- One contract provision may cover several matrix requirements.
- A package can be `aligned` even if no single clause covers the whole standard,
  provided the linked clauses together preserve the legal result.
- Grouped package result and atomic pair role are different. A grouped package
  may be `aligned` because several clauses work together. An atomic row records
  what one exact contract locator contributes to one matrix item; it must not
  pretend that every locator in the package independently covers the whole
  matrix item.
- A package is `deviation` when there is an analogue but any material element is
  changed, narrowed, weakened, omitted, or shifted against the Bank.
- Any material difference from the Bank standard in deadline, amount, formula,
  protected party, trigger, scope, procedure, liability, Bank right, merchant
  obligation, exception, or consequence is a `deviation`.
- A matrix requirement is `missing_in_contract` when no strong legal analogue
  covers the same protected party, legal object, operative right or duty,
  trigger or condition, and legal consequence.
- Generic clauses about payment, notices, electronic documents, inspections,
  confidentiality, compliance, or liability do not satisfy a specific Bank
  standard unless they preserve the same protected party, legal object, trigger,
  procedure, and consequence.
- Weak thematic similarity is not enough for a link. If a clause is only from
  the same broad area but does not pass the legal analogue threshold, keep the
  matrix item in `unmatched_matrix` and record the rejected weak candidate
  there.
- Do not create a `deviation` link with empty `contract_ids`. If no useful
  contract locator exists, the matrix item belongs in `unmatched_matrix`.
- Do not force every matrix item into `links`. A real absence from the contract
  is a required finding, not a failure to be hidden.
- A contract provision is `extra_in_contract` when it has independent legal
  effect and no matrix analogue.
- Use `not_material` for administrative headings, recitals, party details,
  definitions without operative effect, technical formatting, and service text
  that creates no standalone legal risk.

Full preservation is allowed when the difference is only formal:

- blank placeholders or fields intended to be filled later;
- one selected option from alternatives allowed by the standard;
- different document label or appendix title with the same legal effect;
- mandatory law provides the same or stronger result and the contract does not
  waive or narrow it.

Do not spend analysis budget optimizing structural rows, headings, or framework
labels. They may help navigation, but the quality target is the operative legal
proposition: the right, duty, trigger, amount, deadline, procedure, liability,
or consequence that can change risk for the Bank.

## Legal Analogue Threshold

Create a link only after testing these elements:

- `protected_party`: who receives the right, protection, payment, remedy, or
  procedural advantage;
- `bound_party`: who bears the duty, restriction, liability, or burden;
- `legal_object`: what transactions, terminal, channel, data, service, payment,
  document, breach, or relationship the provision regulates;
- `operative_act`: the actual right, duty, prohibition, permission, remedy, or
  allocation of risk;
- `trigger`: the event or condition that activates the provision;
- `consequence`: payment, refusal, deduction, suspension, termination, evidence
  effect, penalty, liability, approval, rejection, or other legal result.

Classify the analogue strength before linking:

- `strong`: same legal object and same operative legal result, with only
  details left to compare;
- `partial`: same legal object and operative area, but one material element is
  narrower, weaker, changed, or incomplete;
- `weak_context`: same broad topic only, adjacent procedure, background,
  framework, appendix, or generic right without the same operative result.

Only `strong` and `partial` analogues may appear in `links` and
`atomic_links`. `weak_context` candidates must be rejected into
`unmatched_matrix[].rejected_candidates` or used only as explanatory context.
This is the main guard against false `deviation` findings.

Use `missing_in_contract` instead of `deviation` when the contract contains:

- generic payment text but not the Bank-standard settlement, deduction, fee,
  holdback, or reconciliation mechanism;
- generic notice or document exchange but not the named channel, evidentiary
  effect, deadline, or delivery procedure required by the matrix;
- generic inspection, acceptance, or request rights but not the same fraud,
  issuer verification, profile, terminal, or payment-system control;
- generic liability but not the specific trigger, protected party, amount,
  formula, cap, exception, or remedy;
- an appendix, form, table, heading, or framework clause that does not itself
  set the operative right, duty, amount, deadline, scope, or consequence.

## Material Element Checklist

For every linked group and every atomic pair, check the material elements below.
Use these fixed results: `same`, `equivalent`, `different`, `missing`,
`not_applicable`.

- `party`
- `legal_object`
- `operative_right_or_duty`
- `trigger`
- `deadline`
- `amount_formula_cap`
- `procedure_channel`
- `liability_remedy`
- `scope_exceptions`
- `consequence`

When an element contains a value, deadline, amount, cap, formula, party, named
channel, document route, or trigger, record the comparison explicitly in
`value_comparison`:

- `element`: checklist element being compared;
- `matrix_value`: value or legal position in the Bank standard;
- `contract_value`: value or legal position in the contract;
- `result`: `same`, `equivalent`, `different`, `missing`, or
  `not_applicable`;
- `equivalence_reason`: why a non-identical value is still equivalent, or empty
  when it is not equivalent.

Rules:

- `aligned` requires every material element to be `same`, `equivalent`, or
  `not_applicable`.
- `deviation` requires at least one material element to be `different` or
  `missing`, and the provision must first pass the legal analogue threshold.
- If any checklist item is `different` or `missing`, the relationship must be
  `deviation` and `discrepancies` must be non-empty. Do not write `aligned` with
  a checklist gap and then explain the gap only in `status_reason`.
- If `discrepancies`, `status_reason`, or `coverage` says an element is absent,
  incomplete, weaker, narrower, or changed, the same element must be marked
  `missing` or `different` in `element_checklist`.
- Never return a `deviation` pair whose checklist contains only `same`,
  `equivalent`, and `not_applicable`.
- If no material element can be named as `different` or `missing`, do not use
  `deviation`.
- Do not mark `deviation` because of document title, appendix label, placeholder
  text, selected allowed option, or mandatory-law structure when the Bank's
  legal result is preserved.

## Status Calibration

Use these gates before finalizing `aligned` or `deviation`.

### False Deviation Guard

Do not create a `deviation` only because:

- the contract selects one product, terminal, payment instrument, or channel
  from a matrix menu and the omitted alternatives are outside the contract
  scope;
- the contract uses a public-procurement, EIS, qualified electronic signature,
  statutory acceptance, or statutory payment route that preserves the same
  enforceable result for the Bank;
- the contract names a different form, appendix, act, UTD/UPD, invoice, website,
  email, or document label while the same right, duty, deadline, evidentiary
  force, and consequence remain;
- the contract sends personal data to payment systems, service companies,
  processors, or mandatory operational participants for the same acquiring
  purpose and keeps the same legal basis, responsibility, and scope;
- the contract includes additional examples, procurement terminology, customer
  labels, or implementation wording that does not narrow a Bank right or add a
  Bank burden.

If a suspected gap is only one of these formal differences, set the checklist
result to `equivalent` and explain the equivalence in `value_comparison`.

### Hard Deviation Confirmations

Use `deviation` when the analogue exists but the contract materially changes or
omits:

- a fixed fee, penalty, cap, rate, formula, currency, payment base, VAT/tax
  treatment, withholding route, or settlement source;
- a deadline for payment, document return, terminal return, installation,
  correction, notice, acceptance, claim response, or post-termination
  settlement;
- a named legal channel or evidentiary route when the matrix makes that channel
  material and the contract replaces it with a weaker or unproven route;
- the protected party, obligated party, or party entitled to a remedy;
- a Bank unilateral right: deduction, direct debit, suspension, refusal,
  termination, non-reimbursement, investigation, document request, or set-off;
- a merchant/customer duty that protects the Bank from card-system, fraud,
  terminal, data, document, or payment risk;
- a liability trigger, exception, penalty amount, cap, or statutory formula
  compared with the Bank standard.

Before final `aligned`, challenge every non-identical value in
`value_comparison`. If no equivalence reason can be stated, the row is
`deviation`.

### Module Absence Sweep

When the contract excludes or does not contain a product module, channel, or
service that appears in the matrix, do not stop at one broad missing finding.
For each operative matrix proposition in that module, decide whether it has an
independent Bank-standard requirement. If yes, add it to `unmatched_matrix`.

Do not add structural headings solely to satisfy this sweep. Add operative
requirements: duties, rights, triggers, deadlines, amounts, procedures,
liability, scope, or consequences.

## Workflow

1. Read the full matrix and full contract.
2. Build `/outputs/working/matrix_inventory.json`. Include every matrix item and
   classify each as `material`, `technical`, or `heading`.
3. Build `/outputs/working/contract_inventory.json`. Include every printed
   clause, operative heading, definition with legal effect, appendix/table row,
   and unnumbered provision that may affect rights or duties.
4. Split material matrix ids into 3-5 batches and use `task` for substantive
   batch analysis when the harness provides it. The orchestrator may prepare
   inventories and merge results, but should not perform the full legal review
   alone.
5. For each material matrix proposition, perform candidate recall before
   deciding absence:
   - direct clause with the same legal object;
   - supporting clause that materially sets scope, procedure, amount,
     deadline, liability, or consequence;
   - detail clause;
   - appendix, table, tariff, form, or definition;
   - payment, procedure, liability, notice, termination, or survival companion;
   - clause referenced by `clause`, `section`, `appendix`, `rules`, or similar
     cross-reference language.
6. Apply the applicability and legal analogue threshold:
   - reject weak-context candidates before creating a link;
   - if every candidate is weak-context only, add the matrix item to
     `unmatched_matrix` with the rejected candidates and reasons;
   - if the matrix item is outside the contract's product, channel, terminal, or
     legal regime and no operative analogue exists, use `missing_in_contract`.
7. Build relationship groups by legal meaning:
   - link all matrix ids and contract ids that form one legal package;
   - include appendix, table, definition, cross-reference, and other supporting
     locators only when they materially affect the legal result;
   - ignore numbering similarity unless the legal proposition also matches.
8. For each linked group, decide whether the contract preserves the bank
   standard:
   - `aligned`: no material legal gap remains after reading the package;
   - `deviation`: at least one material gap remains.
9. Build `atomic_links` from the relationship groups. For each exact
   `matrix_id` + `contract_id` pair that has a legal coverage relation:
   - add one atomic row;
   - state what that exact contract clause covers;
   - state `coverage_role` and `analogue_strength`;
   - include `element_checklist`;
   - include `value_comparison` for every non-identical value, deadline,
     amount, party, channel, procedure, formula, cap, or trigger that affects
     the status;
   - use the pair relationship that follows from that exact clause's legal
     contribution; do not borrow coverage from unrelated clauses, but do not
     automatically downgrade a supporting appendix, procedure, or referenced
     clause when it is a necessary part of an aligned package and has no changed
     material element;
   - do not create a Cartesian product from grouped ids. Add only real legal
     pairs.
10. Run the module absence sweep for product, channel, or service modules that
    are absent from the contract. Add every uncovered operative requirement to
    `unmatched_matrix`.
11. Add every uncovered matrix item to `unmatched_matrix`.
12. Run a contract-only review over the full `contract_inventory`. Each material
   contract item must be classified as:
   - `linked` when it appears in a relationship group;
   - `extra_in_contract` when it has independent legal effect and no matrix
     analogue;
   - `not_material` only when it creates no standalone legal risk.
13. During contract-only review, deliberately check for:
   - procurement and mandatory-law mechanics, including Federal Law No. 44-FZ;
   - electronic acceptance, acceptance in state systems, or customer acceptance
     procedures;
   - customer rights to inspect, reject, demand correction, suspend, or control
     performance;
   - price source, maximum price, budget/payment source, or settlement
     mechanics;
   - unilateral customer termination or convenience exit rights;
   - reporting, act-signing, evidence, or document-exchange procedures.
14. Run the final QA checklist and write one JSON object to
   `/outputs/discrepancy_analysis.json`.

## Tool Use Discipline

- Helper scripts are allowed for deterministic parsing, inventory creation,
  schema checks, coverage checks, merge, and summary counts.
- Do not encode substantive legal conclusions as a giant hardcoded script or a
  table of hundreds of ids inside Python code. Put legal conclusions in JSON
  fragments and merge those fragments.
- Do not create multiple competing full artifacts. Draft fragments belong under
  `/outputs/working/`; only the merged result goes to
  `/outputs/discrepancy_analysis.json`.
- Use at most one QA correction cycle. If QA finds defects, fix concrete
  defects once, re-run a targeted validation, then finish. Do not keep launching
  new broad revalidation agents.

## Status Gates

- `Aligned Package Rule`: several contract clauses may jointly satisfy one Bank
  standard when the package preserves every material element.
- `Atomic Pair Rule`: every final legal pair must be represented as one
  `atomic_links` row. Pair status is evaluated for the exact matrix item and
  exact contract locator, with `coverage_role`, `analogue_strength`, and a
  material element checklist.
- `No Cross-Clause Status Lifting`: do not mark a weak or unrelated clause
  `aligned` merely because another clause in the package is strong. Also do not
  mark a necessary supporting appendix, procedure, or referenced clause
  `deviation` merely because it covers only its own part of an otherwise aligned
  package. A pair needs a named material difference for `deviation`.
- `Deviation Rule`: changed deadline, amount, formula, party, trigger, scope,
  procedure, liability, Bank right, merchant obligation, exception, or
  consequence is a deviation.
- `Missing Beats Weak Deviation`: a weak-context or merely thematic candidate
  is not a legal analogue. Reject it and use `missing_in_contract` rather than
  creating a false `deviation`.
- `Generic Is Not Specific`: a generic clause is not enough for a named Bank
  channel, fraud mechanism, card-system duty, terminal fee, electronic document
  procedure, special liability trigger, or specific Bank remedy.
- `No Formal Deviation`: do not mark deviation for a label, heading, appendix
  title, placeholder, chosen allowed option, or mandatory-law structure when the
  legal result for the Bank is preserved.
- `Value Comparison Rule`: non-identical deadlines, amounts, formulas, caps,
  parties, named channels, procedures, and triggers must be listed in
  `value_comparison`. If the result is `equivalent`, give a concrete legal
  reason. If no reason exists, use `deviation`.
- `Module Absence Rule`: absent product/service modules must be decomposed into
  operative missing requirements, not collapsed into a single broad finding.
- `Named Gap Required`: every `deviation` must identify the changed legal
  element. If the gap cannot be named, re-check whether the package is actually
  `aligned`.
- `Contract-Only Materiality Gate`: `not_material` is limited to headings,
  recitals, signatures, blank forms, administrative details, and definitions
  without operative effect. Acceptance, public-system procedure, customer
  control, rejection, correction, withholding, payment, termination, reporting,
  evidence, liability, and mandatory-law mechanics are normally
  `extra_in_contract` when they have no matrix analogue.

## File Discipline

- Write the final result only to `/outputs/discrepancy_analysis.json`.
- Use `/outputs/working/` for intermediate artifacts, helper scripts,
  validation notes, batch files, and calculations.
- Treat files under `/outputs/working/` as working material, not final output.
- The final answer must be assembled into `/outputs/discrepancy_analysis.json`.
- Keep working files compact and purpose-specific. Prefer several small JSON
  fragments over one very large generated script.

## Output Shape

The output is graph-like, not a matrix-only list:

- `links`: many-to-many legal relationship groups.
- `atomic_links`: exact `matrix_id` + `contract_id` legal pairs projected from
  the grouped links for row-level verification.
- `unmatched_matrix`: bank-standard requirements absent from the contract.
- `unmatched_contract`: contract terms without a matrix analogue.
- `summary`: exact counts derived from the arrays.

Each `deviation` must name the legal gap and explain why it matters for the
Bank. Do not use vague risk text such as "may be risky" without identifying the
changed legal element.

## Final QA

Before finishing, verify:

- `/outputs/working/matrix_inventory.json` and
  `/outputs/working/contract_inventory.json` exist and were used;
- every matrix `number` appears in exactly one of `links[].matrix_ids` or
  `unmatched_matrix[].matrix_id`;
- every real legal matrix-contract pair from grouped `links` appears in
  `atomic_links`, and every `atomic_links` row points back to a grouped link;
- every `atomic_links` row has one real matrix id, one real contract locator,
  `relationship`, `coverage`, `coverage_role`, `analogue_strength`,
  `element_checklist`, and pair-level discrepancies when relationship is
  `deviation`;
- every non-identical deadline, amount, formula, cap, party, named channel,
  procedure, or trigger that affects status appears in `value_comparison` with
  `result` and, for `equivalent`, a concrete equivalence reason;
- no `deviation` is based only on formal labels, selected allowed options,
  procurement terminology, placeholders, or mandatory-law routing when the same
  Bank legal result is preserved;
- absent product, channel, and service modules have been swept for operative
  matrix requirements and those requirements appear in `unmatched_matrix`;
- no `atomic_links` row has `analogue_strength = weak_context`;
- every material contract inventory item appears in a link, in
  `unmatched_contract`, or is expressly classified as `not_material`;
- no link has an empty `contract_ids` array;
- every cited contract locator is present in `contract_inventory.json` and in
  `inputs/contract.txt` as printed numbering, heading, definition label,
  appendix/table label, or exact text;
- no invented ids, internal aliases, translated appendix labels, parenthetical
  ids, corrected numbering, or external answer labels;
- `aligned` links have no discrepancies;
- `deviation` links have at least one discrepancy with `type`, `description`,
  and `risk`;
- `missing_in_contract` items describe the absent bank-standard requirement and
  the risk of omission, and include rejected weak candidates when any were
  considered;
- every `unmatched_matrix` item uses the field `status:
  "missing_in_contract"`. Do not use `reason`, `classification`, or
  `relationship` instead of `status`;
- `extra_in_contract` items describe the extra contract term and its risk;
- `not_material` is used only for non-operative or no-risk contract-only text
  and includes a materiality reason;
- `summary` counts equal the arrays.
