# Comparison Patterns

These are universal calibration patterns. They are not answers for a specific
document.

## 1. Good Legal Proposition Ledger Row

Source clause gives the Bank a right to refuse service registration without
explaining reasons.

Good ledger row:

- `source_text` preserves the clause text;
- `source_excerpt` quotes the refusal right;
- `protected_party = Bank`;
- `bound_party = merchant/counterparty`;
- `right_or_obligation = Bank refusal right`;
- `legal_object = service/outlet registration`;
- `consequence = registration may be refused`.

Result: evaluable. It can participate in matching and status analysis.

## 2. Bad Ledger Row

Source clause contains a payment deadline, but the ledger says only
`payment terms`.

Result: incomplete. Mark `needs_source_review` or repair the ledger before
status. A missing extracted deadline must not make the final analysis forget
the deadline in source text.

## 3. True Analogue

Matrix gives the Bank a specific right to deduct a fee after a defined trigger.
Contract gives the same party the same deduction right for the same trigger and
object.

Result: link the provisions and compare details for `aligned` or `deviation`.

## 4. Weak Thematic Candidate

Matrix gives the Bank a specific deduction right. Contract has only a general
payment clause.

Result: no final link. Record the payment clause as rejected weak context if it
was considered.

## 5. One Matrix Requirement Covered By Several Clauses

Matrix requires a duty, a deadline, a procedure, and a consequence. Contract
splits those elements across parent, operative, procedure, and liability
clauses that all govern the same obligation.

Result: one group link with several `contract_ids`. `aligned` is allowed if the
package preserves all material elements.

## 6. One Contract Clause Covers Several Matrix Requirements

One contract clause contains duties for payment, documents, acceptance, and
liability. Several matrix requirements describe those elements separately.

Result: one group can contain one contract id and several matrix ids when the
legal object and effect are genuinely shared.

## 7. Mandatory Missing

Matrix item is mandatory and applicable to the contract profile. No true
contract analogue exists.

Result: `missing_in_contract` with high risk.

## 8. Out Of Scope Matrix Requirement

Matrix item is filtered to a product, lot, terminal, payment method, or legal
regime not used by the contract.

Result: close it in `coverage_ledger.matrix` as `out_of_scope` or
`not_applicable` with the profile reason. Do not put it in final
`unmatched_matrix`, and do not force a weak link.

## 9. Optional Applicable Missing

Matrix item is optional but applicable to the selected product/profile. No true
contract analogue exists.

Result: `missing_in_contract` with low or conditional risk.

## 10. Slash Options

Matrix lists `cards / QR / mobile pay / smart terminal` as alternatives.
Contract selects `cards / QR`, and the profile confirms only those services are
in scope.

Result: `aligned` for scope. Absence of unselected alternatives is not a
deviation.

## 11. Placeholder In Applicable Term

Matrix or contract requires a filled penalty, fee, account, deadline, appendix,
or system name. The applicable field is blank.

Result: `deviation`, low risk in most cases. Raise to medium when the blank
prevents identification of a named system, channel, counterparty, account,
amount, deadline, or procedure needed for enforcement or performance.

## 12. Same Deadline

Matrix requires a document within 3 business days. Contract imposes the same
3-business-day deadline on the same duty.

Result: deadline element is covered.

## 13. Changed Or Missing Deadline

Matrix requires 3 business days. Contract says 5 business days, uses another
period, or states the duty without a deadline.

Result: `deviation`; discrepancy type `deadline`.

## 14. Borrowed Hard Term Does Not Cure Gap

Contract clause A covers the same duty but lacks the matrix deadline. Clause B
has the same number of days but governs a different request or procedure and is
not incorporated into clause A.

Result: clause B cannot make clause A aligned. Record a deadline deviation.

## 15. Changed Amount, Formula, Cap, Or Penalty

Matrix requires a fixed penalty, no cap, full damages, or a specific formula.
Contract lowers the amount, adds a cap, changes the base, or requires an extra
demand.

Result: `deviation`; discrepancy type `amount` or `liability`.

## 16. Party Inversion

Matrix protects the Bank or imposes a duty on the counterparty. Contract gives
the analogous right to the customer or shifts the burden to the Bank.

Result: `deviation` if it is an analogue; `extra_in_contract` if it creates a
new independent right.

## 17. Procurement Mechanism As Analogue

Public-contract acceptance, EIS signing, budget payment, statutory penalties,
or unilateral termination regulates the same legal object as the matrix.

Result: link it. Use `aligned` if the Bank standard is preserved or stronger.
Do not mark `deviation` merely because the mechanism is 44-FZ/EIS.

## 18. Procurement Mechanism With Material Deviation

Public-contract mechanics regulate the same legal object, but the contract
changes a material element: longer payment deadline, weaker withholding right,
different acceptance consequence, penalty cap, lost termination power, or
changed protected party.

Result: grouped `deviation` with the specific changed element.

## 19. Procurement Mechanism As Extra

Contract gives the customer an independent inspection, rejection, correction,
withholding, reporting, or convenience termination right with no matrix
analogue.

Result: `extra_in_contract` with materiality reason and risk.

## 20. Formal Label Difference

The same legal content appears under another appendix title, report label, or
document name.

Result: `aligned` if rights, duties, timing, evidence, and consequences are
preserved.

## 21. Low-Risk Note Does Not Force Deviation

The contract uses another label for the same channel, another party label for
the same legal role, or adds language beneficial to the Bank. The legal result,
timing, enforceability, and protected party are preserved.

Result: `aligned`. The note can appear in `status_reason`, but it is not a
discrepancy.

## 22. Named Channel Or Legal Force Missing

Matrix requires a named EDI/email/site/channel or legal-force effect. Contract
has a generic document exchange clause and omits the named element.

Result: `deviation` when it is the same exchange mechanism with a missing
material element. If it is only broad-topic context, use `missing_in_contract`.

## 23. Generic Product Capability

Contract says a terminal can display QR or accept cards. Matrix requires a
named Bank product or product-specific procedure.

Result: apply the product profile first. Generic capability is not enough for a
named product obligation.

## 24. Parent And Child Package Retention

Parent clause states the operative right or duty. Child clauses enumerate
events, exceptions, deadlines, or remedies. Either parent or child alone would
be incomplete.

Result: final group includes the material parent and children. Do not drop the
parent only because children contain more detail, and do not drop children when
they carry the hard term.

## 25. Framework Clause As Analogue

Contract clause requires compliance with applicable law, payment-system rules,
contract specifications, or incorporated operating procedures. A matrix row
uses that same framework as the legal object or risk-allocation rule.

Result: include the framework clause as a legal analogue. Do not use it to
inflate unrelated rows where it is only background context.

## 26. Liability Group Review

Matrix separates delay penalties, non-delay fines, caps, exceptions, claim
procedure, and damages. Contract distributes the same topics across several
clauses.

Result: compare the liability package as a group. Before `aligned`, verify
amounts, formulas, caps, triggers, protected party, and excluded buckets.

## 27. Definition Without Legal Effect

Definition has no analogue in the matrix and creates no standalone right, duty,
risk, amount, procedure, liability, or consequence.

Result: `not_material` in the working ledger only.

## 28. Definition With Legal Effect

Definition expands a key term so that it changes scope, liability, covered
transactions, parties, or remedies.

Result: evaluable. Link it if it modifies a matrix analogue; otherwise classify
as `extra_in_contract`.

## 29. Contract-Only Material Clause

Contract adds maximum price, budget source, customer control, acceptance,
withholding, unilateral refusal, penalty cap, reporting, anti-corruption,
confidentiality, audit, data, or evidence procedure with no matrix analogue.

Result: `extra_in_contract`.

## 30. Duplicate Gap Propagation

One payment deadline gap affects a payment package with parent and child
clauses.

Result: record one grouped `deviation`. Do not duplicate the same gap across
unrelated companion clauses.

## 31. Non-Informative Parent

A parent row merely names a section and all legal effect is in children.

Result: close as non-evaluable or `not_material` in the ledger. Do not report
it as a final risk.

## 32. Group-Level Status

A group contains several matrix ids and several contract ids. One status
applies to the group as a whole.

Result: do not assign separate final statuses per pair. `atomic_links` are only
traceability rows and inherit the group relationship.

## 33. Mandatory-Law Extra

Contract clause exists because mandatory procurement law requires a public
contract procedure: acceptance in an official system, statutory reporting,
customer-side control, statutory payment mechanics, or mandatory termination
procedure. The matrix has no true analogue because the Bank standard does not
regulate that public-law mechanism.

Result: if the clause has independent legal effect, classify it as
`extra_in_contract` with low risk and explain that it is mandatory-law
specific. If it is only a heading or formality, close it as `not_material` in
the ledger.

## 34. Structural Duplicate Contract Clause

Two contract clauses regulate the same legal object, the same parties, the same
right or duty, the same trigger, and the same consequence. The second clause
does not add a new amount, deadline, scope, exception, remedy, or procedure.

Result: use the primary clause for the legal link. Close the duplicate in the
ledger as `not_material` or duplicate-of-primary with a short reason. Do not
invent a different matrix analogue just to make the duplicate distinct.

## 35. Matrix Heading Row

Matrix row only names a section, subsection, product block, responsibility
block, payment block, or document-exchange block. It contains no independent
right, duty, procedure, limit, remedy, or consequence beyond child rows.

Result: close as `not_evaluable` in `coverage_ledger.matrix`. Do not include it
in final `unmatched_matrix`.

## 36. Appendix Operative Term

Appendix, specification, tariff table, technical assignment, or schedule row
contains an operative legal term: currency, fee, term, deadline, product scope,
payment method, acceptance condition, service scope, or liability consequence.

Result: index it as an evaluable contract row with a real source locator and
use it as a final `contract_id` if it covers a matrix element. Appendix
headings without operative content remain evidence/context only.

## 37. Bank Right Displaced By Mandatory Law

Matrix gives the Bank a unilateral right such as refusal, suspension,
withholding, termination, verification, or operational control. The public
contract omits or narrows that right because mandatory law restricts
unilateral powers of the contractor or reallocates the mechanism through
statutory procedures.

Result: use `missing_in_contract` if no true analogue exists, or `deviation` if
a narrower statutory substitute exists. Risk is usually medium when statutory
mechanisms partly compensate the Bank, and high when the omitted Bank right has
no practical substitute.

## 38. One Child Deviation Does Not Spread To Siblings

Root clause states a general operative rule. Child clauses enumerate separate
channels, grounds, products, duties, exceptions, or consequences. One child has
a gap, but neighboring children preserve their own legal result.

Result: include the root with the relevant child when it is needed for context,
but keep separate child-level legal results separate. Do not downgrade all
siblings because one sibling has a deviation.

## 39. Missing Belongs In Unmatched Matrix

Matrix requirement is applicable and evaluable. The contract has only weak
topic candidates, not a true analogue.

Result: do not create a `link` with `relationship = missing_in_contract`.
Record the requirement in `unmatched_matrix` and include the weak candidates
only as rejected candidates with reasons.

## 40. Canonical Locator For Unnumbered Appendix Detail

An appendix table contains an operative fee, currency, product, or payment
method, but the specific row has no printed sub-number. The nearest printed
source locator is the appendix or table item that contains the row.

Result: use the nearest printed locator as `contract_id`. Put the exact row
detail in `contract_evidence` or `coverage`. Do not invent ids such as
`appendix_fee_row`, translated labels, or semantic suffixes.

## 41. Payment Procedure Siblings Keep Separate Status

One contract payment section contains an acceptance document, a payment
trigger, a payment deadline, a currency rule, and a service-fee rule. Matrix
requirements split these into separate rows.

Result: link each legal result separately unless the matrix row itself
requires the whole payment package. A deadline gap in one payment row should
not make the acceptance-document row or currency row `deviation`.

## 42. Contract-Only Pass Cannot Be Empty

After matrix matching, several material contract clauses remain: customer
inspection, rejection, withholding, unilateral refusal, statutory reporting, or
mandatory-law control. They do not have true matrix analogues.

Result: final `unmatched_contract` cannot be empty merely because matrix-side
coverage was completed. Report material rows as `extra_in_contract`; close only
headings, signatures, requisites, blank forms, duplicates, or non-operative
definitions as `not_material`.

## 43. Document Or Evidence Deadline Is A Hard Term

Matrix requires a party to provide transaction documents, confirmations,
responses, reports, or evidence within a specified period. Contract contains
the same duty but omits the period, changes it, or gives a period for another
unincorporated procedure.

Result: true analogue exists, but status is `deviation` with a deadline gap.

## 44. Operative Root Must Travel With Detail Clause

Contract child clauses list grounds, exceptions, events, or remedies. A root
clause directly before them grants the right or imposes the duty that makes the
list legally operative.

Result: when a child is linked, review the root. Include the root in the final
contract package if it carries the same legal object. Do not include a root
that is only a section heading.

## 45. Service Compliance Warranty As Analogue

Contract clause states that services must comply with applicable law or
contractual requirements. Matrix contains a warranty, legal-compliance,
payment-system-rules, or incorporated-documents requirement for the same
services or transactions.

Result: this can be a true analogue or companion framework clause. Compare
scope and protected party. Do not use it as a universal substitute for
unrelated duties.

## 46. Public Payment Route Can Preserve Payment Result

Matrix requires payment for Bank services or settlement services. Contract
uses public-procurement acceptance, official payment documents, and budget
payment instead of a commercial tariff-deduction route, but the counterparty
still owes payment for the same service after the same performance/acceptance
trigger.

Result: link the payment/acceptance package. Use `aligned` when economic
obligation, trigger, evidence, and enforceability are preserved. Use
`deviation` only for a changed deadline, amount, party, trigger, withholding
right, or other hard term.

## 47. Liability Root And Directional Children

Contract liability section has a general right to claim penalties, then
separate child clauses for customer delay, Bank delay, customer non-delay
breach, and Bank non-delay breach.

Result: link the root plus the relevant directional child. Do not treat one
direction as covering the opposite direction. Compare formula, cap, trigger,
protected party, and exception for each directional liability result.

## 48. Numbered Appendix Row Is A Final Locator

Appendix contains a visible numbered item or table row with a currency, fee,
payment method, service price, deadline, or other operative term.

Result: index and use that visible appendix item as a final contract locator
when it covers a matrix element. If the row has no visible sub-locator, use the
nearest printed appendix/table locator and put the exact row detail in
evidence. Do not invent semantic ids.

## 49. Term And Survival Package

Matrix requires contract term, early end by price exhaustion, and survival of
liability after expiry. Contract has one clause for service period/price
exhaustion and another clause for termination or post-termination settlements.

Result: review the term package before declaring a miss. Link the clauses that
cover term, price-exhaustion trigger, and survival/consequences. Status is
`aligned` only if each material element is preserved.

## 50. Final Missing Row Must Name Requirement

Matrix requirement is applicable and has no true contract analogue.

Result: final `unmatched_matrix` row must contain `matrix_id`, `requirement`,
`status = missing_in_contract`, `risk_level`, and `risk`. A `reason` field may
explain the conclusion, but it does not replace the missing requirement text.

## 51. Contract Proposition Extraction Is One Pass

Contract text has a clause with a printed locator, a duty, a deadline, and a
payment consequence.

Bad result: first create only a locator row, then lose the deadline during
later legal normalization.

Good result: create one `contract_legal_propositions` row with the same
printed locator, full `source_text`, deadline, duty, legal object, parties, and
consequence. Derive `clause_index` and `legal_propositions.contract` from that
row.

Result: matching and status use the same source-backed proposition; no hard
term is lost between extraction stages.

## 52. Amount Or Code Is Evidence, Not A Contract Id

Contract text contains a standalone line with a contract price, postal index,
bank account, table ordinal, or numerical value.

Bad result: create a contract id such as `900000`, `354340`, or `1` only
because the line starts with digits.

Good result: attach the amount or code to the nearest real clause, appendix
item, or table locator. Use the amount as `amount_formula_cap` or
`source_evidence`, not as `contract_id`.

Result: the value can affect `aligned` / `deviation`, but it cannot become a
final locator.

## 53. Pattern: Embedded Locator Must Be Split Before Matching

Situation:
A contract proposition row contains one printed locator at the beginning, then
another visible operative locator later in the same `source_text`.

Wrong outcome:
Use the merged row for matching and let the second locator disappear as an
independent candidate.

Correct outcome:
Repair `contract_legal_propositions` before matching. Each operative locator
gets its own source-backed row, unless the second marker is only a cross
reference and not the start of a clause.

Why:
Merged source rows hide payment deadlines, term clauses, termination rights,
or service-fee terms. Matching and status cannot be stable if the locator
itself is missing from the legal proposition ledger.

Decision rule:
If a row's text contains another visible locator followed by operative text,
stage validation should fail and the ledger must be split or repaired.

Source:
Current seed-eval / latest run.

## 54. Pattern: Document Exchange Root Travels With Channel

Situation:
A root clause gives the parties a choice among several document-exchange
channels. Child clauses name individual channels.

Wrong outcome:
Link only the child channel clauses and miss the root, or treat the root as a
heading.

Correct outcome:
If the matrix requirement concerns the availability, choice, or legal effect
of the exchange mechanism, include the root as an operative analogue. Link the
child only for the channel-specific requirement it actually covers.

Why:
The root clause can carry the legal permission to choose a channel. Children
usually define implementation details.

Decision rule:
Root travels with channel only when it grants the exchange right, channel
choice, legal-force rule, or default procedure. A pure section title does not
travel.

Source:
Current seed-eval / latest run.

## 55. Pattern: Term And Price-Exhaustion Package

Situation:
The matrix term row requires start/end date, early end by exhaustion of the
contract price, and survival of responsibility. The contract splits those
elements across service-period, price-cap, and termination clauses.

Wrong outcome:
Miss the analogue because no single contract clause contains the whole term
package.

Correct outcome:
Recall the package: service period, price-exhaustion or maximum-price clause,
termination/settlement clause, and survival clause if present. Then classify
`aligned` or `deviation` by the combined legal result.

Why:
Term, price exhaustion, and post-expiry consequences often live in different
places but regulate one duration result.

Decision rule:
Do not mark a term matrix row missing until these package elements have been
checked across the contract.

Source:
Current seed-eval / latest run.

## 56. Pattern: Public Acceptance Direction Matters

Situation:
A public-procurement contract has several EIS acceptance clauses: provider
creates the document, customer signs or refuses, expert review is possible,
and payment follows acceptance.

Wrong outcome:
Use every EIS substep as a broad analogue for any matrix payment or acceptance
row, or hide independent EIS rights as `not_material`.

Correct outcome:
Match by direction and legal object. A provider-created acceptance document
can support a payment-trigger analysis; a customer sign/refuse clause can map
to an acceptance/refusal requirement; expert review, correction, or control
substeps are contract-only extras when no matrix analogue exists.

Why:
EIS mechanics are related but not interchangeable. Provider evidence,
customer acceptance, payment timing, and control rights are separate legal
effects.

Decision rule:
Ask who must act, what act is required, and what consequence follows. Link
only the same direction; report independent customer-control effects as
`extra_in_contract`.

Source:
Current seed-eval / latest run.

## 57. Pattern: Confirmation Duty Without Deadline

Situation:
Matrix requires a party to provide confirmation, evidence, transaction
information, or personal-data transfer grounds within a defined period.
Contract contains the same confirmation duty but does not state that period.

Wrong outcome:
Mark `aligned` because the duty itself exists.

Correct outcome:
Link the analogue but use `deviation` for the missing hard-term deadline,
unless another expressly incorporated clause supplies the same period for that
exact duty.

Why:
The response period is part of the Bank's control and evidence right. A duty
without the required timing is weaker.

Decision rule:
For evidence/confirmation duties, always reread source text for the period and
trigger before `aligned`.

Source:
Current seed-eval / latest run.

## 58. Pattern: Technical Permission Without Extra Notice Gap

Situation:
Matrix permits a technical action such as remote software update without
changing operation order and explains that no separate notice is needed.
Contract permits the same technical action and does not impose a notice duty.

Wrong outcome:
Use `deviation` merely because the contract omits the explanatory phrase
about no prior notice.

Correct outcome:
Use `aligned` if the same technical permission, object, trigger, and practical
effect are preserved.

Why:
Absence of an explanatory negative phrase is not a legal gap when the contract
does not create the opposite obligation.

Decision rule:
Treat missing explanatory wording as formal unless the contract actually adds
a notice requirement, narrows the permission, changes the trigger, or weakens
the consequence.

Source:
Current seed-eval / latest run.

## 59. Pattern: Force Majeure Equivalent List

Situation:
Matrix and contract both release a party from liability for extraordinary
unavoidable events, but their illustrative event lists differ.

Wrong outcome:
Use `deviation` only because one list contains fewer examples or different
wording.

Correct outcome:
Use `aligned` when the same legal effect is preserved: force majeure prevents
performance, liability is released for the affected obligation, and the
contract does not materially narrow the protected party or consequence.

Why:
The legal test and consequence matter more than the exact illustrative list.

Decision rule:
Downgrade only for a narrower legal threshold, changed protected party,
missing notice/proof duty when the matrix makes it material, or changed
consequence.

Source:
Current seed-eval / latest run.

## 60. Pattern: Appendix Fee Row Must Be Preserved

Situation:
An appendix or specification row contains a fee, rate, price unit, currency,
or product-specific economic term.

Wrong outcome:
Use the appendix heading as evidence only and lose the operative row as a
candidate.

Correct outcome:
Index the visible appendix row as an evaluable source locator. If the row has
no separate printed id, use the nearest visible appendix/table locator and put
the exact fee row in evidence.

Why:
Commercial fee terms often live in appendices. Missing them lowers mapping
recall and can create false missing or false extra results.

Decision rule:
Appendix economic rows are final locators when they carry the operative price,
fee, currency, payment method, or service scope.

Source:
Current seed-eval / latest run.
