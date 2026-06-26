---
name: acquiring-discrepancy-analysis
description: "Use this skill to compare an acquiring Bank standard matrix against a counterparty acquiring contract: build many-to-many legal coverage, identify aligned terms, deviations from the Bank standard, missing applicable matrix requirements, out-of-scope matrix requirements, and material contract-only terms. Trigger on phrases like check this contract against our matrix, what is missing in the counterparty contract, acquiring contract review, compare bank standard with contract, discrepancy analysis, or matrix-to-contract legal gap analysis."
---

# Acquiring Discrepancy Analysis

Use this skill to compare a Bank standard acquiring matrix with a counterparty
acquiring contract. The matrix is the Bank standard. The contract is checked
against that standard. The output is a many-to-many legal coverage graph plus a
two-sheet review table generated from the JSON.

Reference loading:

- Read `references/matching-rules.md` before substantive matching.
- Read `references/status-rules.md` before group-level status and risk
  classification.
- Read `references/comparison-patterns.md` when a matching or status decision
  is ambiguous. It contains calibration examples for analogue threshold,
  grouped coverage, weak-candidate rejection, hard terms, procurement terms,
  appendix terms, and risk status.
- Read `references/output-contract.md` before writing or validating final
  artifacts. It is the field contract for JSON and XLSX outputs.

## Quick Start

1. Preflight `inputs/contract.txt`; stop with a source error artifact if the
   text is not legally usable.
2. Build `clause_index.json` as the complete source map.
3. Build and validate `legal_propositions.json`; do not start matching until
   `working_artifact_validation.json` is valid.
4. Build the contract product profile and close out-of-scope matrix rows only
   in the internal ledger.
5. Read `references/matching-rules.md`; compare both directions: matrix
   requirements to contract package, and material contract terms back to matrix
   analogues.
6. Read `references/status-rules.md`; assign group-level `aligned`,
   `deviation`, `missing_in_contract`, or `extra_in_contract` based on source
   text.
7. Run Final QA, then write one final JSON and the mechanical XLSX export.

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
consequence, re-read the source text. Extracted fields are useful for recall,
but source text controls the legal conclusion.

## Required Artifacts And Contracts

Create the artifacts in this order. Each later step depends on the earlier
artifact contract. The purpose is to prevent legal facts from being lost
between stages: `clause_index` proves source coverage, `legal_propositions`
preserves legal meaning, and `coverage_ledger` proves final closure.

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
processed until the source text has been reviewed. Do not proceed to matching
with unresolved source-review rows that could affect status.

The ledger is an evidence table, not a substitute for the source. Matching may
use it to find candidates. Status must still be confirmed against source text
because legal meaning may depend on context outside a normalized field.

Run the mechanical check before matching:

```bash
python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/working_artifact_validation.json
```

This is a stage gate, not a final QA item. Before starting matrix matching,
contract-only review, merge, or status work:

- `outputs/working/working_artifact_validation.json` must have `"valid": true`;
- `legal_propositions.json` must not contain unresolved
  `needs_source_review` rows;
- every evaluable row must have source text and enough normalized legal fields
  to preserve its legal meaning.

If the check fails, repair the working artifact that failed and rerun this
validator. Do not defer incomplete legal proposition rows to Final QA.

The validator checks source-map completeness, matrix id coverage, contract row
coverage, legal proposition row counts, unresolved `needs_source_review`, empty
source text, and weak evaluable rows. `"valid": true` means the working
artifacts are complete enough to begin legal matching; it does not mean the
legal conclusions are correct.

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
- In `44_fz` public-procurement contracts, expect mandatory-law acceptance,
  payment, reporting, termination, and control clauses. They may be legal
  analogues, low-risk `extra_in_contract`, or internal ledger closures
  depending on legal effect. Their presence is not itself a coverage error.
- Matrix heading rows and non-operative matrix parents close as
  `not_evaluable` in `coverage_ledger.matrix`; they are not final
  `unmatched_matrix` risks.

## Matching Method

Read and follow `references/matching-rules.md` before matching. The short rule:
final links require true legal analogues, not broad topic overlap. Perform both
directions:

- matrix to contract: find the contract package that covers each applicable
  Bank-standard requirement;
- contract to matrix: find matrix analogues for each material contract term or
  classify it as `extra_in_contract`;
- keep weak candidates out of final `links`; use them only as rejected
  candidates or reasoning;
- group ids only when they form one legal package.

Use `references/comparison-patterns.md` for calibration examples such as weak
candidate rejection, parent/child package retention, mandatory-law extras,
appendix terms, contract-only materiality, and grouped coverage.

## Status And Risk Method

Read and follow `references/status-rules.md` before status classification. The
short rule: status is group-level and source-text based.

- `aligned`: the contract package preserves the matrix legal result.
- `deviation`: a true analogue exists, but a material element is changed,
  narrowed, weakened, omitted, shifted, or blank.
- `missing_in_contract`: no true contract analogue exists for an applicable
  matrix requirement.
- `extra_in_contract`: a legally meaningful contract proposition has no matrix
  analogue.
- `not_material`, `out_of_scope`, and `not_applicable` are internal ledger
  closures unless the output contract says otherwise.

Compare hard terms directly: deadlines, amounts, formulas, caps, penalties,
protected parties, triggers, procedures, liability, remedies, and consequences.
Formal labels and mandatory-law mechanics do not create `deviation` when the
legal result is preserved. An applicable blank or placeholder remains
`deviation`, normally low risk.

## Final QA

Before writing final artifacts, perform release checks over already-built
artifacts. Do not use Final QA as the first pass over missing working data.

Blocking checks; repair before final JSON:

- verify `clause_index` covers all source ids;
- verify `outputs/working/working_artifact_validation.json` exists and is
  valid; if it is missing or invalid, return to the Legal Proposition Ledger
  stage instead of patching only the final JSON;
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

Advisory cleanup; fix when practical, but do not rewrite legal conclusions
without source support:

- keep quotes concise;
- keep risk explanations specific to the Bank;
- keep XLSX as a mechanical export from JSON;
- keep working files under `/outputs/working/`.

## Output Discipline

Read and follow `references/output-contract.md` before writing any final
artifact. Do not duplicate or reinterpret the field contract locally.

`links` carry group-level legal findings. `atomic_links` are traceability
projections only and must inherit the group relationship. Do not assign
separate final pair-level statuses.

## Tools And Scripts

Use helper scripts for mechanical work: source extraction, indexing,
normalization checks, batch completeness, coverage validation, JSON schema
checks, and Excel export. Do not put legal mapping or status decisions into
hardcoded scripts.

Required scripts live under `skills/acquiring-discrepancy-analysis/scripts/`
and run with the project Python environment. If a script fails because of a
path or environment issue, repair the command/path and rerun it. If a required
validator is genuinely unavailable, do not skip the gate: perform the same
mechanical checks manually, write the expected validation report under
`/outputs/working/`, and state that the fallback was used.
