# Output Contract

Write two final artifacts:

- `/outputs/discrepancy_analysis.json`
- `/outputs/discrepancy_analysis.xlsx`

The JSON is the source of truth. The XLSX is a mechanical presentation export.

## Working Artifact Contract

Before final comparison, create:

- `/outputs/working/contract_legal_propositions.json`
- `/outputs/working/clause_index.json`
- `/outputs/working/legal_propositions.json`
- `/outputs/working/contract_product_profile.json`
- `/outputs/working/coverage_ledger.json`

The matrix-side legal ledger is curated before the run at
`inputs/matrix_legal_propositions.json`. It must contain every matrix `number`
from `inputs/matrix.json`, but it must stay compact: do not duplicate full
`enriched_text` there. Use `source_ref.matrix_id` to read the full raw matrix
row from `inputs/matrix.json` whenever source verification is needed. If this
input is missing or invalid, stop with a setup error; do not rebuild it during
contract review.

`contract_legal_propositions.json` is the primary contract working artifact.
It combines document-aware clause extraction and legal normalization in one
pass. The agent may use scripts as a seed, but this file must be repaired
against `inputs/contract.txt` before matching.

`clause_index.json` is a compatibility source map derived from the matrix
ledger and contract legal propositions. It contains source ids and text, but no
final legal status. It is document-aware: locators come from the actual
contract structure, not from a universal regex. Amounts, addresses, requisites,
account numbers, page artifacts, and table ordinals are not final locators by
themselves.

`legal_propositions.json` is the combined legal evidence ledger. Its `matrix`
array is copied from compact `inputs/matrix_legal_propositions.json`; its
`contract` array is copied from the repaired
`contract_legal_propositions.json`. Matrix rows use `source_ref` instead of
duplicating full source text. Matrix `status_check_elements` may be atom-id
references into `legal_atoms`; do not repeat the same text in both places.
Contract rows must contain source text. It must contain:

```json
{
  "matrix": [
    {
      "id": "<matrix number>",
      "source_ref": {"matrix_id": "<matrix number>"},
      "materiality": "evaluable|not_material|heading|needs_source_review",
      "required_type": "mandatory|optional|unknown",
      "applicability_filters": {},
      "bank_standard": "<concise bank-standard requirement>",
      "protected_party": "<party protected by the rule>",
      "bound_party": "<party bound by the rule>",
      "right_or_obligation": "<right/duty/remedy/prohibition>",
      "legal_object": "<regulated object>",
      "matching_cues": ["<short legal cue>"],
      "legal_atoms": [
        {"atom_id": "a1", "category": "<element type>", "text": "<atomic legal element>"}
      ],
      "status_check_elements": ["a1"],
      "hard_term_atom_ids": ["a1"],
      "trigger": "<event/condition>",
      "deadline": "<deadline if any>",
      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
      "procedure_channel": "<procedure/channel if any>",
      "liability_remedy": "<liability/remedy if any>",
      "consequence": "<legal consequence>"
    }
  ],
  "contract": [
    {
      "id": "<printed contract locator>",
      "source_text": "<contract clause text>",
      "source_excerpt": "<short quote>",
      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
      "materiality": "evaluable|not_material|heading|needs_source_review",
      "protected_party": "<party protected by the rule>",
      "bound_party": "<party bound by the rule>",
      "right_or_obligation": "<right/duty/remedy/prohibition>",
      "legal_object": "<regulated object>",
      "trigger": "<event/condition>",
      "deadline": "<deadline if any>",
      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
      "procedure_channel": "<procedure/channel if any>",
      "liability_remedy": "<liability/remedy if any>",
      "scope_options": ["<scope option>"],
      "consequence": "<legal consequence>",
      "final_allowed": true,
      "evidence_only": false
    }
  ]
}
```

Rows marked `needs_source_review` are not complete. Resolve them before
substantive matching if they can affect a link, missing item, or contract-only
finding.

`contract_legal_propositions.json` uses the same row shape as
`legal_propositions.contract`. A final `contract_id` may only use a row with
`final_allowed = true`. Rows with `evidence_only = true` may support quotes and
reasoning but must not appear as final ids.

After the contract ledger is repaired, derive `clause_index.json` and
`legal_propositions.json` mechanically:

```bash
python skills/acquiring-discrepancy-analysis/scripts/derive_working_artifacts.py --matrix inputs/matrix.json --matrix-legal inputs/matrix_legal_propositions.json --contract-ledger outputs/working/contract_legal_propositions.json --working outputs/working --json-out outputs/working/derive_working_artifacts_report.json
```

After creating or repairing `legal_propositions.json`, run
`validate_working_artifacts.py` and write
`/outputs/working/working_artifact_validation.json`. The validation report must
be valid before substantive matching begins. If it is invalid, repair the
working artifact first; do not wait until final JSON QA to discover incomplete
legal proposition rows.

## Final JSON Shape

```json
{
  "analysis_profile": {
    "contract_product_profile": {
      "product": ["<selected product/channel>"],
      "lot": "<44_fz|223_fz|commercial|common|unknown>",
      "terminal": ["<selected terminal/payment device>"],
      "payment_method": ["<selected payment method>"],
      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
    },
    "source_preflight": {
      "contract_numbering_valid": true,
      "notes": []
    }
  },
  "links": [
    {
      "matrix_ids": ["<matrix id>"],
      "contract_ids": ["<contract locator>"],
      "relationship": "aligned|deviation",
      "legal_topic": "<short legal topic>",
      "matrix_standard": "<bank standard requirement group>",
      "contract_position": "<counterparty contract position group>",
      "matrix_evidence": "<short matrix quote>",
      "contract_evidence": "<short contract quote>",
      "status_reason": "<group-level reason>",
      "risk_level": "none|low|medium|high",
      "discrepancies": [
        {
          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
          "description": "<material difference>",
          "risk": "<why this matters for the Bank>"
        }
      ]
    }
  ],
  "atomic_links": [
    {
      "matrix_id": "<one matrix id>",
      "contract_id": "<one contract locator>",
      "relationship": "aligned|deviation",
      "link_index": 0,
      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
      "coverage": "<what this contract locator contributes to the group>"
    }
  ],
  "unmatched_matrix": [
    {
      "matrix_id": "<matrix id>",
      "requirement": "<missing bank standard requirement>",
      "source_evidence": "<short matrix quote>",
      "status": "missing_in_contract",
      "required_type": "mandatory|optional|unknown",
      "applicability": "applicable|conditional|unknown",
      "risk_level": "low|medium|high",
      "risk": "<risk of omission>",
      "rejected_candidates": [
        {
          "contract_id": "<weak candidate considered>",
          "reason": "<why it is not a true analogue>"
        }
      ]
    }
  ],
  "unmatched_contract": [
    {
      "contract_id": "<contract locator>",
      "contract_position": "<extra legally significant contract term>",
      "source_evidence": "<short contract quote>",
      "status": "extra_in_contract",
      "risk_level": "low|medium|high",
      "risk": "<risk or impact for the Bank>",
      "materiality_reason": "<why this has independent legal effect>"
    }
  ],
  "coverage_ledger": {
    "matrix": [
      {
        "matrix_id": "<matrix id>",
        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
        "link_indices": [0],
        "reason": "<short closure reason>"
      }
    ],
    "contract": [
      {
        "contract_id": "<contract locator>",
        "closure": "linked|extra_in_contract|not_material",
        "link_indices": [0],
        "reason": "<short closure reason>"
      }
    ]
  },
  "summary": {
    "aligned_count": 0,
    "deviation_count": 0,
    "missing_in_contract_count": 0,
    "extra_in_contract_count": 0
  }
}
```

## JSON Rules

- `links` are group-level legal findings. One status applies to the whole
  many-to-many group.
- Intermediate batch fragments should use the same relationship values as the
  final artifact. Do not put `missing_in_contract`, `extra_in_contract`,
  `not_material`, unresolved rows, or candidate-only rows inside `links`.
- `atomic_links` are traceability rows only. They inherit the group
  `relationship`; do not invent pair-level final statuses.
- `contract_ids` contain clauses that provide material coverage for the group.
  Background clauses can be cited in reasoning, but should not become final
  candidates unless they affect coverage or status.
- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
  matrix closures. Do not use it to invent final conclusions.
- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
  not a risk for the current product, lot, terminal, payment method, or legal
  regime. They stay in `coverage_ledger.matrix` only and do not appear in
  final `unmatched_matrix`.
- `not_evaluable` matrix closures mean the row is a heading, non-operative
  parent, or source row without an independent legal proposition. They stay in
  `coverage_ledger.matrix` only and do not appear in final `unmatched_matrix`.
- `unmatched_contract` contains only legally significant `extra_in_contract`
  rows. Non-material rows stay in `coverage_ledger.contract`.
- `coverage_ledger.contract` must close every contract row from
  `contract_legal_propositions.json` / `legal_propositions.contract`: `linked`
  when it appears in a final link,
  `extra_in_contract` when it has independent legal effect and no matrix
  analogue, or `not_material` when it is a heading, duplicate, blank form,
  signature/requisites row, or non-operative definition. Do not leave material
  contract rows out of the ledger.
- `relationship = aligned` requires empty `discrepancies`, `risk_level = none`,
  and text-grounded confirmation that the contract package preserves the matrix
  legal result.
- `relationship = deviation` requires at least one discrepancy with `type`,
  `description`, and `risk`.
- Missing mandatory applicable requirements should normally be `high` risk.
  Missing optional applicable requirements should normally be `low` or
  conditional risk.
- Mandatory-law public-procurement extras with independent legal effect can be
  `low` risk when they do not materially worsen the Bank position. They still
  require a non-empty `risk` and `materiality_reason`.
- All final ids must be visible in source files. Do not use corrected,
  inferred, translated, parenthetical, or internal ids.
- Final contract ids must exist in `outputs/working/clause_index.json`.
  Presence of the same digits somewhere in `contract.txt` is not enough.
- Final contract ids must also exist in
  `outputs/working/contract_legal_propositions.json` with
  `final_allowed = true`.
- If an appendix, table, or technical assignment detail has no printed
  sub-locator, use the nearest printed locator visible in the source as the
  final `contract_id` and cite the detail in evidence fields. Do not create
  synthetic ids such as semantic suffixes, translated labels, helper-script
  names, or pseudo-paragraph locators.
- Weak candidates do not appear in final `links`; use
  `unmatched_matrix[].rejected_candidates`.
- Every final `unmatched_matrix` item must use the exact field
  `requirement`. A narrative field such as `reason`, `matrix_requirement`, or
  `matrix_proposition` can be additional context, but it cannot replace
  `requirement`.

## Excel Output

Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.

Sheet 1: `Contract-Matrix`

Columns:

1. `contract_id`
2. `contract_summary`
3. `matrix_ids`
4. `status`
5. `risk_level`
6. `comment`

Rules:

- one row per group-level contract-to-matrix finding;
- `matrix_ids` contains the full matrix id set for the group;
- status is `aligned`, `deviation`, or `extra_in_contract`;
- contract-only extras have blank `matrix_ids`.

Sheet 2: `Only in Matrix`

Columns:

1. `matrix_id`
2. `requirement`
3. `required_type`
4. `risk_level`
5. `comment`

Rules:

- one row per final `unmatched_matrix` item;
- include optional applicable missing as low/conditional risk;
- do not include out-of-scope / not-applicable requirements;
- do not include non-evaluable headings or purely technical rows.

## Bad Output Patterns

Do not output:

- multiple competing final JSON files;
- pair-level final statuses as the primary answer;
- `deviation` for unselected slash alternatives;
- `deviation` for heading/title/label changes alone;
- final `unmatched_contract` rows for definitions without legal effect;
- final `unmatched_matrix` rows for matrix headings or non-operative parents;
- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
  requirements;
- final ids that exist only in helper scripts or working ledgers;
- `links` with `relationship = missing_in_contract`;
- `unmatched_matrix` rows that use `reason` instead of the required
  `requirement` field;
- an empty `unmatched_contract` section while material contract propositions
  remain unclosed in `coverage_ledger.contract`;
- `extra_in_contract` with empty risk;
- `aligned` with non-empty discrepancies;
- `missing_in_contract` where a weak candidate is silently treated as a link;
- final conclusions based only on extracted fields without source-text evidence.
