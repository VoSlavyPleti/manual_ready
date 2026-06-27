# Output Contract

Use this reference when writing `outputs/discrepancy_analysis.json`.

The final artifact is one JSON object:

```json
{
  "analysis_profile": {
    "product": [],
    "legal_regime": "44_fz|223_fz|commercial|common"
  },
  "links": [
    {
      "contract_ids": ["<contract locator>"],
      "matrix_ids": ["<matrix number>"],
      "relationship": "aligned|deviation",
      "status_reason": "<short legal reason>",
      "risk_level": "none|low|medium|high",
      "discrepancies": [
        {
          "type": "deadline|amount|party|scope|trigger|procedure|liability|other",
          "description": "<material difference>",
          "risk": "<why it matters for the Bank>"
        }
      ]
    }
  ],
  "unmatched_matrix": [
    {
      "matrix_id": "<matrix number>",
      "status": "missing_in_contract",
      "requirement": "<missing Bank-standard requirement>",
      "required_type": "mandatory|optional",
      "risk_level": "low|medium|high",
      "risk": "<risk of omission>"
    }
  ],
  "unmatched_contract": [
    {
      "contract_id": "<contract locator>",
      "status": "extra_in_contract",
      "contract_position": "<extra contract term>",
      "risk_level": "low|medium|high",
      "risk": "<impact for the Bank>",
      "materiality_reason": "<why it has legal effect>"
    }
  ],
  "coverage_ledger": {
    "matrix": [
      {
        "matrix_id": "<matrix number>",
        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
        "reason": "<short source-grounded reason>"
      }
    ],
    "contract": [
      {
        "contract_id": "<contract locator>",
        "closure": "linked|extra_in_contract|not_material",
        "reason": "<short source-grounded reason>"
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

## Structural Rules

- `links[].relationship` is only `aligned` or `deviation`.
- Missing matrix rows go only to `unmatched_matrix`, not to `links`.
- Extra contract rows go only to `unmatched_contract`, not to `links`.
- A clause may appear in both `links` and `unmatched_contract` only when the
  same source text contains a true matrix analogue plus a separate independent
  extra proposition.
- `aligned` links have empty `discrepancies`.
- Every `deviation` has at least one named discrepancy.
- `summary` counts equal the final array counts.

## Coverage Rules

- Every source matrix id appears once in `coverage_ledger.matrix`.
- Every `coverage_ledger.matrix` row with `closure: "linked"` appears in at
  least one `links[].matrix_ids`.
- Every `coverage_ledger.matrix` row with `closure: "missing_in_contract"`
  appears in `unmatched_matrix[].matrix_id`.
- `out_of_scope` and `not_applicable` rows state the source-based applicability
  reason.
- Every material contract locator appears in `coverage_ledger.contract`.
- Every `coverage_ledger.contract` row with `closure: "linked"` appears in at
  least one `links[].contract_ids`.
- Every `coverage_ledger.contract` row with `closure: "extra_in_contract"`
  appears in `unmatched_contract[].contract_id`.

Verify by exact source id sets, not by row counts alone.
