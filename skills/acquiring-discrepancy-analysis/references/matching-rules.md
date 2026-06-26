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

Do not begin or finalize matching on a merged source row. If a contract
proposition's `source_text` contains another visible operative locator, repair
the proposition ledger first. The later status cannot reliably recover a
deadline, amount, right, or termination term that was hidden inside a neighbor
row.

Include parent, child, appendix, payment, procedure, liability, and framework
clauses only when they provide material coverage or legally cure a gap. Each
included locator should explain which element it covers: duty, right, trigger,
deadline, amount, procedure, liability, remedy, scope, or consequence.

If a child clause is selected, check whether its parent carries operative legal
meaning for the same topic. If a parent is selected, check whether children
contain hard terms or exceptions. Do not include non-operative parent headings.
If a linked detail clause is part of an enumerated legal package, also check
the operative root or anchor row that grants the right, imposes the duty, or
introduces the list. The anchor belongs in `contract_ids` when it carries the
same legal object; it stays out when it is only a heading.

For payment, acceptance, liability, termination, and document-exchange
requirements, keep the legal package together only when the clauses govern one
legal result. Do not merge sibling requirements just because they share a
section parent.
Public-procurement payment and acceptance clauses can be true analogues for
Bank-standard payment, acceptance-document, and service-fee requirements when
they preserve the same economic obligation and legal trigger. Do not reject
them only because the route is EIS/acceptance/budget payment.

Keep directionality in public acceptance clauses. A clause requiring the
provider to create an EIS acceptance document is not the same legal object as a
clause requiring the customer to accept, sign, refuse, or pay. Link only the
direction that matches the matrix requirement. If the EIS substep has
independent legal effect but no matrix analogue, review it as contract-only
instead of using it as a broad payment analogue.

Document-exchange roots and term/effective-period roots are operative when
they choose the allowed channels, set the contract term, tie duration to price
exhaustion, or preserve post-expiry responsibility. If a child channel,
payment, or termination clause is selected, check whether the root is part of
the same legal result.

For large matrices, preserve thematic continuity during review: complete the
local payment, liability, termination, document-exchange, or product-scope
cluster you are analyzing before switching context. This is a context-retention
rule, not a requirement to create broad domain batches or crosswalk artifacts.

See examples: `One Matrix Requirement Covered By Several Clauses`, `Parent And Child Package Retention`, `Non-Informative Parent`, `Document Exchange Root Travels With Channel`, `Term And Price-Exhaustion Package`, `Public Acceptance Direction Matters`.

## Fragment Shape Before Merge

Every batch fragment should already follow the final output contract. Do not
use `links` as a temporary bucket for missing or unresolved rows.

- `links[].relationship` can only be `aligned` or `deviation`;
- applicable matrix rows with no true analogue go to `unmatched_matrix`;
- unresolved rows go to a `needs_review` list or are repaired before merge;
- weak candidates stay in `rejected_candidates` or reasoning, not in
  `contract_ids`;
- a fragment with invalid relationships or ids should be repaired before it is
  merged into the final artifact.

See examples: `Missing Belongs In Unmatched Matrix`, `Weak Thematic Candidate`.

## Contract To Matrix

For each evaluable contract proposition, find the matrix analogue group. If no
true analogue exists and the proposition has independent legal effect, classify
it as `extra_in_contract`.

Do not classify a contract term as `not_material` merely because no final
finding was produced. `not_material` is reserved for headings, definitions
without legal effect, requisites, signatures, blank forms, and purely
technical rows.

The contract-side review is complete only when every contract proposition from
`legal_propositions.contract` is closed as `linked`, `extra_in_contract`, or
`not_material` in `coverage_ledger.contract`. A material contract row cannot be
left unclassified because the matrix-side pass already produced enough links.
If it has a true matrix analogue, link it. If it has independent legal effect
and no true analogue, report `extra_in_contract`. If it is only a heading,
duplicate, blank form, or non-operative definition, close it as `not_material`.

Public-procurement acceptance, control, expert review, motivated refusal,
correction, and EIS document-flow substeps are material when they give the
customer an independent procedure or right. They are not `not_material` merely
because another acceptance clause was linked to a matrix payment or document
row.

See examples: `Contract-Only Material Clause`, `Definition Without Legal Effect`, `Definition With Legal Effect`, `Contract-Only Pass Cannot Be Empty`.

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
source locators visible in the contract text. Do not invent semantic ids. If an
operative detail has no printed sub-id, use the nearest printed source locator
as `contract_id` and describe the exact detail in `contract_evidence`,
`coverage`, or `source_evidence`. Do not create synthetic locators with
semantic suffixes, translated names, or helper-script ids.
If the appendix or table has a printed item number, row label, or visible
sub-locator, preserve that visible locator instead of collapsing the whole
appendix into one generic id. Missing such a row is a source coverage problem,
not a legal matching choice.

If an appendix title only marks the beginning of a document part, keep it
`evidence_only` / `not_material`; do not use it as a final `contract_id`.

See examples: `Appendix Operative Term`, `Canonical Locator For Unnumbered Appendix Detail`, `Formal Label Difference`.

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

Payment and procedure clauses often sit near each other but remain separate
legal results: payment amount, payment trigger, acceptance document, acceptance
deadline, payment deadline, service fee, and evidence channel should not be
merged into one broad group unless the matrix item itself requires the whole
package. A gap in one payment or procedure element does not downgrade sibling
links that preserve their own legal result.

For liability, keep the operative root with the relevant directional child:
who breaches, who is protected, which formula applies, whether a cap exists,
and which exception applies. Do not use a customer-delay child to cover a
Bank-delay requirement, or a general penalty root to cover a special cap or
exemption without the matching child.

See examples: `Group-Level Status`, `Duplicate Gap Propagation`, `One Child Deviation Does Not Spread To Siblings`, `Payment Procedure Siblings Keep Separate Status`, `Liability Root And Directional Children`.
