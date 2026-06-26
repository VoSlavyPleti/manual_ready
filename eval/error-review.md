# Error Review: KAVKAZ Seed Eval, 2026-06-26

## Run And Sources

- Document: current KAVKAZ contract in `inputs/contract.txt`.
- Gold: `ALL_DATA/KAVKAZ.before_agent_better_pairs_20260618_172816.xlsx`.
- Agent run: `run_logs/agent_run_20260626_191410.*`.
- The run failed before writing `outputs/discrepancy_analysis.json` because of an `openai.APITimeoutError`.
- Diagnostic artifact used for metrics: `outputs/working/finalized_from_fragments.json`, built from completed batch fragments with the project finalize script.
- Coverage validation for the diagnostic artifact: `outputs/working/finalized_coverage_validation.json`, valid with 0 errors.

## Metrics Snapshot

Filtered legal metrics with artifact-declared out-of-scope rows removed:

| Metric | OK | Total | Percent |
|---|---:|---:|---:|
| status_accuracy | 140 | 204 | 68.63% |
| linked_mapping_exact_set | 62 | 112 | 55.36% |
| linked_mapping_soft_1plus | 91 | 112 | 81.25% |
| linked_group_status | 81 | 112 | 72.32% |
| missing_in_contract | 42 | 64 | 65.62% |
| extra_in_contract | 17 | 28 | 60.71% |

Out-of-scope handling looks useful, not erroneous: 14 matrix ids were closed as out-of-scope/not-applicable, 11 matrix-only gold rows were removed from the denominator, and no linked gold row was dropped.

## Error Class Summary

| Class | Count / Evidence | Dominance | Main Fix Area |
|---|---:|---|---|
| A: analogue threshold / recall | 21 linked mapping misses, 19 matrix-only false links, 11 extra misses | Dominant | `matching-rules.md`, `comparison-patterns.md` |
| B: status | 10 linked rows had a candidate but wrong status | Material | `status-rules.md`, `comparison-patterns.md` |
| C: profile | 0 confirmed; scope exclusions did not drop linked rows | Not dominant | no change now |
| D: coverage / proposition extraction | several gold locators were embedded in neighboring ledger rows, e.g. contract text for `3.1.1` contained `3.2`, and `4.4` contained payment timing later represented as `4.5.1` | Material root cause for some misses | stage gate and extraction scripts |

## Error Table

| id | Source clause / matrix row | Expected | Actual | Class | Likely root cause | Target file | Proposed fix | Status |
|---|---|---|---|---|---|---|---|---|
| E01 | `1.2` -> `10.1` | link + deviation | no link | A | term/price-exhaustion package not recalled with contract term | `matching-rules.md`, `comparison-patterns.md` | add term/price-exhaustion recall calibration | fixed |
| E02 | `2.3` -> `2.3` | link + aligned | no link | A | operative document-exchange root dropped while child channel rows were linked | `matching-rules.md`, `comparison-patterns.md` | add document-exchange root anchor pattern | fixed |
| E03 | `3.1.1` -> `6.1`, `11.7` | link + aligned | no link | D/A | clause ledger merged `3.1.1` and `3.2`, reducing locator precision | validator, parser, patterns | detect embedded locators and require split/repair before matching | fixed |
| E04 | `3.2` -> `6.1` | aligned | deviation | B | service-fee clause was extracted inside another row and status was downgraded from formal/public-payment differences | `status-rules.md`, patterns | add public payment equivalence and embedded-locator stage gate | fixed |
| E05 | `4.1` -> `10.1` | link + aligned | no link | A | contract term/date package not connected to matrix term row | `matching-rules.md`, patterns | emphasize term/effective-period package recall | fixed |
| E06 | `4.4` -> `3.3`, `4.2.1`, `4.2.12` | link + deviation | partial weak link only to `3.3` | A/B/D | payment clause merged with payment deadline; economic payment package split incorrectly | parser, `matching-rules.md`, patterns | split embedded locators; separate payment trigger/deadline/currency rows | fixed |
| E07 | `4.5` -> `6.5` | aligned | deviation | B/D | payment timing locator became `4.5.1`; public-payment route over-penalized | validator, `status-rules.md` | embedded locator repair; functional equivalence for statutory payment route | fixed |
| E08 | `5.1.2` -> `2.3.6`, `6.2` | link + aligned | no link | A | advertising / information channel package not recalled | `matching-rules.md`, patterns | add root/child channel-package pattern | fixed |
| E09 | `5.1.3` -> large compliance package | link + deviation | no link | A | service-compliance warranty treated too narrowly and not projected to incorporated matrix duties | patterns | keep as needs more evidence; avoid broad warranty-as-universal-substitute rule | needs more evidence |
| E10 | `5.2.1` -> `4.2.1` | link + deviation | no link | A | merchant/card-operation duty not recalled from customer obligation block | `comparison-patterns.md` | add focused recall example only if repeats | needs more evidence |
| E11 | `5.2.2` -> `5.1.17` | link + deviation | no link | A | unilateral refusal/low-turnover termination substitute missed | `matching-rules.md` | covered by Bank-right-displaced and term/termination package examples | fixed |
| E12 | `5.2.3`, `5.2.4` -> `5.1.6` | aligned | deviation | B | model treated absence of an explicit negative notice phrase as a legal gap, despite same technical-update permission | `status-rules.md`, patterns | add formal technical permission equivalence pattern | fixed |
| E13 | `5.2.10` -> `5.1.1` | link + aligned | no link | A | non-reimbursement / reversal economic effect not recalled | patterns | mark as needs more evidence before adding a broad rule | needs more evidence |
| E14 | `5.3.1` -> `6.4` | link + deviation | no link | A | customer acceptance / return-document duty missed | `comparison-patterns.md` | add directional EIS/customer acceptance pattern | fixed |
| E15 | `5.3.5` -> `7.4`, `7.5`, `7.6` | link + aligned | no link | A | liability root/right-to-claim package not recalled | `matching-rules.md`, patterns | reinforce directional liability root + child pattern | fixed |
| E16 | `5.3.15` -> `4.2.16.3` | deviation | aligned | B | same PDn confirmation duty found, but 3-working-day hard deadline omitted in contract | `status-rules.md`, patterns | add source reread pattern for confirmation/evidence deadline | fixed |
| E17 | `7.2`, `7.3`, `7.4.1`, `7.5`, `7.7`, `7.7.2` -> liability rows | links expected | several no links / one false aligned | A/B | liability section not kept as root + directional children with formulas/caps | `matching-rules.md`, patterns | reinforce liability direction and formula package | fixed |
| E18 | `8.3.1`, `8.4`, `8.5.3`-`8.8` | extra_in_contract | omitted or used as weak links | A | EIS acceptance substeps were used as broad payment analogues instead of contract-only public-procurement mechanics | `matching-rules.md`, patterns | add directional public-acceptance detail rule | fixed |
| E19 | `8.5.1` -> `6.4` | aligned | deviation | B | statutory EIS acceptance route over-penalized despite preserving accept/refuse legal result | `status-rules.md`, patterns | add public acceptance functional-equivalence pattern | fixed |
| E20 | `9.1` -> `8.1` | aligned | deviation | B | force-majeure list/formulation differences treated as material | `status-rules.md`, patterns | add force-majeure equivalence pattern | fixed |
| E21 | `11.3` -> `10.2`, `10.3` | aligned | deviation | B/D | locator absent from ledger; termination package compared through neighboring clauses | validator, parser | embedded-locator stage gate should force source repair | fixed |
| E22 | `11.6` -> `10.2` | deviation | no link | A | mandatory-law termination procedure not recalled as narrower substitute for matrix termination rule | `matching-rules.md`, patterns | add termination/statutory-substitute recall | fixed |
| E23 | `Приложение №1 п.5` -> `2.2`, `6.20` | link + aligned | no link | D/A | operative appendix fee row not preserved as a final locator | parser, `matching-rules.md`, patterns | reinforce visible appendix row preservation and stage gate | fixed |
| E24 | matrix-only `2.3.1`, `2.3.4`, `2.3.7`, `2.7` | missing_in_contract | linked aligned | A | document-channel / electronic-form weak links promoted despite gold treating standard requirement as absent | `comparison-patterns.md` | keep as needs more evidence; possible gold/legal disagreement | needs more evidence |
| E25 | matrix-only `5.1.5`, `5.1.7`, `5.1.10`, `6.8`, `6.10`, `6.11`, `6.14`, `6.16`, `6.17`, `11.6`, `11.12`, `11.13` | missing_in_contract | linked | A | broad topic analogues used to hide missing bank-standard rights or hard terms | `matching-rules.md`, patterns | add strict weak-candidate rejection for payment/liability/termination/control specifics | fixed |

## What Was Correct

- Working artifact stage gate did create full matrix coverage and no unresolved proposition rows.
- Scope filtering correctly removed non-applicable product/legal-regime rows from final risk reporting.
- Soft linked mapping reached 91/112, so many true analogues were at least found.
- Contract-only review identified 17/28 gold extra rows and did not collapse to an empty result.

## Fix Strategy

The dominant class is A, with B and D as important secondary classes. Changes should therefore be narrow:

- add calibration patterns for the repeated A/B situations above;
- strengthen matching rules around term packages, public acceptance direction, document-exchange roots, and liability root/children;
- strengthen status rules for evidence deadlines and false deviations caused by formal public-procurement mechanics;
- extend stage validation so embedded locators and merged clauses are caught before matching.

No C-class product-profile change is made now because the current scope filter behaved consistently and did not drop linked gold rows.
