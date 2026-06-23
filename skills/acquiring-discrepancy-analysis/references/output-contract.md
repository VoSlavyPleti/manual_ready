# Output Contract

Write `/outputs/discrepancy_analysis.json` as one JSON object with this shape.
Do not write this file anywhere else.

Before writing the final file, create and use:

- `/outputs/working/matrix_inventory.json`
- `/outputs/working/contract_inventory.json`

These working files prove that the comparison covered both documents. They are
not part of the final JSON object.

```json
{
  "links": [
    {
      "matrix_ids": ["<matrix id>"],
      "contract_ids": ["<contract locator>"],
      "relationship": "aligned|deviation",
      "legal_topic": "<short legal topic>",
      "matrix_standard": "<bank standard requirement>",
      "contract_position": "<counterparty contract position>",
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
      "legal_topic": "<short legal topic>",
      "analogue_strength": "strong|partial",
      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
      "coverage": "<what this exact contract clause contributes to this exact matrix item>",
      "element_checklist": [
        {
          "element": "party|legal_object|operative_right_or_duty|trigger|deadline|amount_formula_cap|procedure_channel|liability_remedy|scope_exceptions|consequence",
          "result": "same|equivalent|different|missing|not_applicable",
          "note": "<short evidence-based note>"
        }
      ],
      "status_reason": "<why this exact pair is aligned or deviation>",
      "discrepancies": [
        {
          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
          "description": "<pair-level material difference>",
          "risk": "<why this pair-level difference matters for the Bank>"
        }
      ]
    }
  ],
  "unmatched_matrix": [
    {
      "matrix_id": "<matrix id>",
      "requirement": "<missing bank standard requirement>",
      "status": "missing_in_contract",
      "risk": "<legal or business risk for the Bank>",
      "rejected_candidates": [
        {
          "contract_id": "<contract locator considered but rejected>",
          "reason": "<why this is only weak context and not a legal analogue>"
        }
      ]
    }
  ],
  "unmatched_contract": [
    {
      "contract_id": "<contract locator>",
      "contract_position": "<extra contract term>",
      "status": "extra_in_contract|not_material",
      "risk": "<risk if material; empty or low-risk explanation if not material>",
      "materiality_reason": "<why this creates independent legal effect or why it is non-operative>"
    }
  ],
  "summary": {
    "aligned_count": 0,
    "deviation_count": 0,
    "missing_in_contract_count": 0,
    "extra_in_contract_count": 0
  }
}
```

## Field Rules

- `matrix_ids`: exact `number` values from `inputs/matrix.json`.
- `contract_ids`: exact printed clause ids or real document locators from
  `inputs/contract.txt` and `/outputs/working/contract_inventory.json`; never
  use invented subparagraph labels.
- `contract_ids`: do not use internal aliases or translated labels such as
  `Appendix_1`. If an alias is useful in a working file, keep it out of the
  final artifact.
- `contract_ids`: must be non-empty for every `links` item. If no contract
  locator exists, use `unmatched_matrix` instead of a link.
- `relationship`: only `aligned` or `deviation`.
- `discrepancies`: empty array for `aligned`; non-empty array for `deviation`.
- `unmatched_matrix[].status`: must be exactly `missing_in_contract`. Do not
  use `reason`, `classification`, or `relationship` as a substitute for
  `status`.
- `atomic_links`: one object per legally related `matrix_id` + `contract_id`
  pair. Do not omit atomic pairs just because a grouped `links` item already
  contains them.
- `atomic_links[].analogue_strength`: use only `strong` or `partial`. Do not put
  weak-context candidates in `atomic_links`.
- `atomic_links[].coverage_role`: describe the exact role of the contract
  locator in the legal package.
- `atomic_links[].relationship`: evaluate the exact pair and its role. Do not
  borrow coverage from unrelated clauses. Do not automatically mark a necessary
  parent, child, appendix, or procedure clause as `deviation` unless the pair
  has a named material gap in `element_checklist`.
- `atomic_links[].link_index`: zero-based index of the grouped `links` item that
  contains the pair. Use `null` only if the pair cannot be placed into a grouped
  link.
- `atomic_links[].coverage`: short statement of the legal element this exact
  contract locator covers for this exact matrix item.
- `atomic_links[].element_checklist`: must include all material elements needed
  to justify the pair result. Use `different` or `missing` only for real legal
  gaps.
- If an atomic pair has `relationship = deviation`, at least one checklist item
  must be `different` or `missing`. If the discrepancy is an omitted sub-duty,
  omitted remedy, omitted trigger, omitted amount, or narrower scope, record
  that omission in the closest checklist element.
- If any checklist item is `different` or `missing`, the atomic pair cannot be
  `aligned`; change the pair to `deviation` and put the same gap in
  `discrepancies`.
- `atomic_links[].status_reason`: one sentence connecting the checklist to
  `aligned` or `deviation`.
- `type`: choose the closest fixed value. Use `other` only when none fit.
- `summary.aligned_count`: number of `links` with `relationship = aligned`.
- `summary.deviation_count`: number of `links` with `relationship = deviation`.
- `summary.missing_in_contract_count`: number of `unmatched_matrix` items.
- `summary.extra_in_contract_count`: number of `unmatched_contract` items with
  `status = extra_in_contract`.

## Coverage Rules

Each matrix id must appear once:

- in one `links[].matrix_ids` array when the contract has a legal analogue; or
- in one `unmatched_matrix[].matrix_id` when the contract has no useful analogue.

Each linked matrix-contract pair must also appear in `atomic_links`:

- for every legally meaningful pair from each grouped link, add exactly one
  `atomic_links` row;
- do not generate a Cartesian product automatically. Add a pair only when that
  contract locator actually contributes legal coverage to that matrix item;
- do not let one strong direct clause lift unrelated framework, context,
  appendix, or procedure clauses to `aligned`;
- do not downgrade a necessary package clause to `deviation` merely because it
  covers only its own role; `deviation` needs a named material difference;
- if the full legal result is achieved only by a package of several contract
  clauses, the grouped link may be `aligned`, while atomic pairs show each
  clause's role and checklist-supported relationship.

Do not create links for weak context:

- same broad topic without the same protected party, legal object, operative
  act, trigger, and consequence belongs in
  `unmatched_matrix[].rejected_candidates`;
- a weak candidate may explain why a matrix item is still missing, but it must
  not appear in `links` or `atomic_links`.

Each material contract inventory item must be accounted for:

- in `links[].contract_ids` when it is legally related to the matrix;
- in `unmatched_contract` with `status = extra_in_contract` when it has
  independent legal effect and no matrix analogue;
- in `unmatched_contract` with `status = not_material` only when it is useful to
  show that a reviewed provision creates no standalone risk.

Do not let contract-only review become a list of headings. Report material
contract-only provisions that affect procurement procedure, acceptance,
customer control rights, payment mechanics, termination, evidence, reporting,
liability, or enforceability.

`not_material` is reserved for headings, recitals, signatures, requisites,
blank forms, administrative details, and definitions with no operative effect.
Every `unmatched_contract` row must explain materiality in
`materiality_reason`.

## Bad Output Patterns

Do not output:

- several competing final files;
- arrays at the top level;
- `contract_id` values with explanations in parentheses;
- normalized internal locators such as `Appendix_1` when the contract uses a
  printed locator in another form;
- legal conclusions without source locators;
- `deviation` without a named changed element;
- `aligned` with an `element_checklist` item marked `different` or `missing`;
- grouped links without the corresponding `atomic_links` projection;
- atomic pairs created only because ids are located in the same grouped package
  but have no direct legal coverage relation;
- atomic pairs with `analogue_strength = weak_context`;
- `missing_in_contract` rows that hide considered weak candidates instead of
  recording why they were rejected;
- `extra_in_contract` for mere headings, recitals, signatures, or blank forms.

Temporary batch files, helper scripts, notes, and checks may be created under
`/outputs/working/`. They are working material only; the final deliverable is
still `/outputs/discrepancy_analysis.json`.

Helper scripts must stay mechanical: parsing, normalization, merge, coverage,
schema checks, and summary counts. Do not use generated scripts as the place
where legal mapping decisions are manually hardcoded.
