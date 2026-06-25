---
name: acquiring-discrepancy-analysis
description: "Compare a bank acquiring standard matrix with a counterparty acquiring contract using bidirectional legal proposition coverage, group-level statuses, missing bank-standard requirements, and material contract-only terms."
---

# Acquiring Discrepancy Analysis

Use this skill to compare a Bank standard acquiring matrix with a counterparty
acquiring contract. The matrix is the Bank standard. The contract is checked
against that standard. The output is a many-to-many legal coverage graph plus a
two-sheet review table generated from the JSON.

Before finalization, read:

- `references/output-contract.md` for artifact shape and field contracts.
- `references/comparison-patterns.md` for calibration examples.

## Purpose

Find and explain:

- Bank-standard matrix requirements preserved by the contract;
- true analogues that deviate from the Bank standard;
- applicable matrix requirements absent from the contract;
- legally meaningful contract terms with no matrix analogue.
- matrix requirements that are out of scope for the current contract profile,
  closed in the internal ledger without final risk reporting.

The review is risk-oriented. Missing a real risk is worse than marking a
borderline issue as `deviation`, but weak thematic matches must not be promoted
into legal links.

## Inputs And Outputs

Inputs:

- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
  applicability filters.
- `inputs/contract.txt`: full counterparty contract text. Use printed clause
  ids or real document locators visible in this file.

Final outputs:

- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.

Working artifacts belong under `/outputs/working/`.

## Source Hierarchy

Use the source text as the legal authority:

1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
2. Contract clause text and real printed locators from `inputs/contract.txt`.
3. Working ledgers as indexes and evidence aids.

Do not decide status from extracted fields alone. When a status depends on a
deadline, amount, penalty, party, trigger, procedure, channel, scope, or
consequence, re-read the source text.

## Required Artifacts And Contracts

Create the artifacts in this order. Each later step depends on the earlier
artifact contract.

### 1. Source Preflight

Check `inputs/contract.txt` before analysis:

- real clause numbering is present;
- deep clause numbers are not visibly collapsed or shifted;
- repeated locators have enough context to distinguish source rows;
- text is readable and not corrupted by encoding.

If the contract text is not usable, stop and write
`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
invalid text.

### 2. Clause Index

Create `/outputs/working/clause_index.json`.

It is a source map only. It must include:

- every matrix `number`;
- every contract clause, operative parent, definition, appendix/table row, and
  unnumbered operative provision;
- source text or source locator for each row;
- context for duplicate printed contract ids.

Do not use `clause_index` to decide legal status. It only proves source
coverage and valid ids. Never overwrite it with a batch subset.

### 3. Legal Proposition Ledger

Create `/outputs/working/legal_propositions.json`.

This is the mandatory legal evidence ledger. It must contain `matrix` and
`contract` arrays. Every evaluable proposition should include:

- `id`: matrix number or printed contract locator;
- `source_text`: text used for legal comparison;
- `source_excerpt`: short quote supporting the normalized proposition;
- `type`: `operative`, `definition`, `heading`, `parent_framework`,
  `appendix`, `table`, or `technical`;
- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
- `protected_party`, `bound_party`;
- `right_or_obligation`;
- `legal_object`;
- `trigger`;
- `deadline`;
- `amount_formula_cap`;
- `procedure_channel`;
- `liability_remedy`;
- `scope_options`;
- `consequence`;
- `applicability_filters` where available.

If a legally meaningful row cannot be normalized, mark it
`needs_source_review` and explain the missing element. It is not fully
processed until the source text has been reviewed. Do not proceed to final
matching with unresolved source-review rows that could affect status.

The ledger is an evidence table, not a substitute for the source. Matching may
use it to find candidates. Status must still be confirmed against source text.

Run the mechanical check before matching:

```bash
python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working
```

Fix invalid working artifacts before delegating comparison work.

### 4. Contract Product Profile

Create `/outputs/working/contract_product_profile.json`.

Extract from the contract:

- product and payment channels;
- lot/procurement type;
- terminal/payment-device scope;
- payment methods;
- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).

Apply matrix filters before status:

- `common` applies to every contract.
- A filtered matrix item applies only when the profile matches
  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
- Mandatory applicable missing = high risk.
- Out-of-scope / non-applicable matrix items are not final risks. Close them in
  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
  profile-based reason. Do not put them in final `unmatched_matrix`.
- Optional applicable missing = low or conditional risk.
- Slash-separated alternatives are options unless the matrix says all options
  are mandatory.
- Placeholder or blank in an applicable material term = low-risk `deviation`.

## Analogue Threshold

Create a final link only when the contract proposition is a true legal analogue
of the matrix proposition. Test:

- same or equivalent protected party;
- same or equivalent bound party;
- same legal object;
- same operative right, duty, prohibition, permission, remedy, or allocation of
  risk;
- material trigger, scope, procedure, and consequence are the same or legally
  equivalent.

Reject weak thematic candidates. A clause about the same broad topic is not a
legal analogue when it governs a different object, party, trigger, procedure,
or consequence.

## Bidirectional Matching

Perform both directions.

Matrix to contract:

- for each applicable evaluable matrix proposition, retrieve all contract
  clauses that collectively cover the Bank-standard requirement;
- include parent, child, appendix, payment, procedure, liability, and framework
  clauses only when they provide material coverage or legally cure a gap.
- if a child clause is selected, check whether its parent carries operative
  legal meaning for the same topic; if a parent is selected, check whether its
  children contain the material elements;
- for payment, acceptance, liability, termination, and document-exchange
  requirements, keep the legal package together: operative clause, basis,
  deadline, procedure, remedy, consequence, and any incorporated appendix/table
  row that changes coverage;
- a framework or legal-compliance clause may be a standalone analogue only when
  it carries the same legal object or allocates the same risk, duty, or remedy.

Contract to matrix:

- for each evaluable contract proposition, find the matrix analogue group;
- if none exists and the term has independent legal effect, classify it as
  `extra_in_contract`;
- if it is non-operative, close it as `not_material` only in the ledger.

Group related ids into many-to-many `links`. One matrix id may need several
contract clauses. One contract clause may cover several matrix ids.

## Group-Level Status

Assign status to the group, not to each atomic pair.

- `aligned`: the contract package preserves the matrix legal result.
- `deviation`: a true analogue exists, but any material element is changed,
  narrowed, weakened, omitted, shifted, or blank.
- `missing_in_contract`: no true contract analogue exists for an applicable
  matrix requirement.
- `extra_in_contract`: a legally meaningful contract proposition has no matrix
  analogue.
- `not_material`: internal ledger closure only; exclude from final report.
- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
  final report because the requirement does not apply to the current product,
  lot, terminal, payment method, or legal regime.

Material elements include party, legal object, operative act, trigger,
deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
remedy, exception, Bank right, merchant duty, and consequence.

Hard terms must be compared directly:

- same material deadline/amount/procedure in the same legal obligation can be
  `aligned`;
- changed value or missing value is `deviation`;
- a hard term from another clause counts only when that clause expressly
  governs the same obligation or is explicitly incorporated;
- a neighboring date, amount, or procedure for another legal object cannot cure
  the gap.

Do not downgrade for formal differences alone: heading, title, appendix label,
permitted option selection, equivalent mandatory-law mechanism, or wording
style.

Do not downgrade for low-risk notes when the legal result is preserved. If the
reason says the difference is merely terminological, beneficial to the Bank,
already incorporated through another clause, or caused only by a mandatory
44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.

44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
when it materially worsens or changes a Bank-standard term: payment timing,
acceptance control, withholding right, penalty/cap, termination power, protected
party, evidence channel, or enforceability.

Liability, penalty, cap, and remedy provisions must be reviewed as a group.
Before marking a liability group `aligned`, check the amount, formula, cap,
trigger, protected party, excluded delay/non-delay buckets, and claim procedure
across the whole package.

## Risk Calibration

Use `risk_level` consistently:

- `none`: only for `aligned`;
- `low`: optional applicable missing, placeholder, formal but legally manageable
  gap;
- `medium`: material deviation that can affect performance, evidence, payment,
  control, liability, or enforceability;
- `high`: mandatory missing, changed protected party, major payment/remedy
  change, important Bank right omitted, or broad contract-only risk.

Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
a short evidence-based reason. Use concise quotes rather than long excerpts.

## Final QA

Before writing final artifacts:

- verify `clause_index` covers all source ids;
- verify `legal_proposition_ledger` has no unresolved
  `needs_source_review` rows that can affect final status;
- verify every matrix id is closed as `linked`, `missing_in_contract`,
  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
  `coverage_ledger`;
- verify every applicable evaluable matrix id is linked or in
  `unmatched_matrix`;
- verify out-of-scope / non-applicable matrix ids are not in final
  `unmatched_matrix`;
- verify every material contract id is closed as linked or extra;
- verify `coverage_ledger` is derived from final `links`,
  `unmatched_matrix`, and `unmatched_contract`;
- verify every final id is visible in source text;
- verify `aligned` has no material discrepancy;
- verify every `deviation` has a named legal gap and evidence;
- verify weak candidates are not in final `links`;
- verify non-material contract rows are absent from final `unmatched_contract`;
- verify summary counts equal final arrays.

## Output Discipline

Follow `references/output-contract.md`.

The final JSON must contain:

- `analysis_profile`
- `links`
- `atomic_links`
- `unmatched_matrix`
- `unmatched_contract`
- `coverage_ledger`
- `summary`

`links` carry group-level legal findings. `atomic_links` are traceability
projections only and must inherit the group relationship. Do not assign
separate final pair-level statuses.

## Tools And Scripts

Use helper scripts for mechanical work: source extraction, indexing,
normalization checks, batch completeness, coverage validation, JSON schema
checks, and Excel export. Do not put legal mapping or status decisions into
hardcoded scripts.
