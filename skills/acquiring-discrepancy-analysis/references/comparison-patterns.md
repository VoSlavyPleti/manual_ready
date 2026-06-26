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
