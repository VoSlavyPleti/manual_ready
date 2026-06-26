# Matching Rules

Use these rules when building final `links`, `unmatched_matrix`,
`unmatched_contract`, and closure rows. They are universal calibration rules,
not document-specific answers.

## True Analogue Threshold

Create a final link only when the contract proposition is a true legal
analogue of the matrix proposition. Test:

- same or equivalent protected party;
- same or equivalent bound party;
- same legal object;
- same operative right, duty, prohibition, permission, remedy, or allocation
  of risk;
- same or legally equivalent material trigger, scope, procedure, and
  consequence.

A broad topic match is not enough. General law, payment, liability,
notification, acceptance, or procurement language can be considered, but it
becomes a final link only if it governs the same legal object and legal effect.

See examples: `True Analogue`, `Weak Thematic Candidate`, `Generic Product Capability`.

## Matrix To Contract

For each applicable evaluable matrix proposition, retrieve the contract
package that covers the Bank-standard requirement.

Include parent, child, appendix, payment, procedure, liability, and framework
clauses only when they provide material coverage or legally cure a gap. Each
included locator should explain which element it covers: duty, right, trigger,
deadline, amount, procedure, liability, remedy, scope, or consequence.

If a child clause is selected, check whether its parent carries operative legal
meaning for the same topic. If a parent is selected, check whether children
contain hard terms or exceptions. Do not include non-operative parent headings.

For payment, acceptance, liability, termination, and document-exchange
requirements, keep the legal package together only when the clauses govern one
legal result. Do not merge sibling requirements just because they share a
section parent.

For large matrices, preserve thematic continuity during review: complete the
local payment, liability, termination, document-exchange, or product-scope
cluster you are analyzing before switching context. This is a context-retention
rule, not a requirement to create broad domain batches or crosswalk artifacts.

See examples: `One Matrix Requirement Covered By Several Clauses`, `Parent And Child Package Retention`, `Non-Informative Parent`.

## Contract To Matrix

For each evaluable contract proposition, find the matrix analogue group. If no
true analogue exists and the proposition has independent legal effect, classify
it as `extra_in_contract`.

Do not classify a contract term as `not_material` merely because no final
finding was produced. `not_material` is reserved for headings, definitions
without legal effect, requisites, signatures, blank forms, and purely
technical rows.

See examples: `Contract-Only Material Clause`, `Definition Without Legal Effect`, `Definition With Legal Effect`.

## Matrix Headings And Non-Operative Parents

Matrix rows that only name a section, subsection, theme, or parent category
close as `not_evaluable` in `coverage_ledger.matrix`. They never appear in
final `unmatched_matrix`.

If a matrix parent row contains its own right, duty, procedure, limitation,
definition with legal effect, or consequence, treat it as evaluable. Otherwise
use it only as context for children.

See examples: `Matrix Heading Row`, `Non-Informative Parent`.

## Appendix And Schedule Terms

Appendix, schedule, specification, table, tariff, technical assignment, or
payment-detail rows can be final contract locators when they contain an
operative legal term: deadline, amount, currency, payment method, procedure,
scope, product, acceptance condition, liability, remedy, or consequence.

Index those rows in `clause_index` and `legal_propositions.contract` with real
source locators visible in the contract text. Do not invent semantic ids. If
an appendix title only marks the beginning of a document part, keep it
`evidence_only` / `not_material`; do not use it as a final `contract_id`.

See examples: `Appendix Operative Term`, `Formal Label Difference`.

## 44-FZ And Mandatory-Law Clauses

Public-procurement clauses are not automatically extra and not automatically
deviation:

- if they regulate the same legal object as the matrix, link them and evaluate
  `aligned` or `deviation`;
- if they are mandatory-law mechanics with no matrix analogue and no adverse
  Bank-specific risk, classify as low-risk `extra_in_contract` when they have
  independent legal effect;
- if they are headings or procedural scaffolding without independent legal
  effect, keep them out of final `unmatched_contract`.

See examples: `Procurement Mechanism As Analogue`, `Mandatory-Law Extra`.

## Structural Duplicates

If two contract clauses regulate the same legal object, same parties, same
right or duty, same trigger, and same consequence, treat the later clause as a
structural duplicate. It can inherit closure from the primary clause or close
as `not_material` in `coverage_ledger.contract` with a reference to the
primary clause. Do not create a new group or search for a different matrix id
only to make the duplicate unique.

See example: `Structural Duplicate Contract Clause`.

## Grouping Discipline

Group ids only for an indivisible legal package. Sibling matrix ids with
different legal objects, channels, grounds, duties, or consequences should
remain separate links even if they share a parent section.

One matrix id may need several contract clauses. One contract clause may cover
several matrix ids. The group must still describe one legal result.

See examples: `Group-Level Status`, `Duplicate Gap Propagation`, `One Child Deviation Does Not Spread To Siblings`.
