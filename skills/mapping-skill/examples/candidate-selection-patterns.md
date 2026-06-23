# Candidate Selection Patterns

Generic examples for candidate recall. They do not assign compliance status.

## candidate/core-proposition-pass

Matrix signal: a party has a right to suspend a service when a named trigger
occurs.

Good candidate: contract clause giving the same party a suspension right for
that trigger, even if the deadline or procedure differs.

Reject: a general suspension list that does not include the trigger.

## candidate/core-proposition-fail

Matrix signal: automatic connection, activation, installation, or proof event.

Good candidate: clause stating that lifecycle event or a mandatory substitute.

Reject: product availability, terminal capability, appendix title, or tariff row
with no lifecycle trigger.

## candidate/numbered-family-expansion

Matrix signal: liability, acceptance, payment, termination, or document package.

Good candidates:

- parent row stating the right, duty, protected party, or common consequence;
- child row stating the amount, formula, deadline, trigger, or exception;
- adjacent sibling row covering delay, non-delay, cap, demand, or procedure.

Reject: a child-only output when the family rows carry separate operative rules.

## candidate/mirrored-right-duty-row

Matrix signal: payment, acceptance, liability, termination, service period, or
legal-compliance package.

Good candidates:

- special-section clause with the detailed mechanism;
- rights-and-obligations row that gives a party the mirrored right or duty;
- price-cap, service-period, or survival row when duration depends on them.

Reject: mirrored rows that only share vocabulary but would not be cited for the
same legal package.

## candidate/appendix-row

Matrix signal: scope, tariff, device, service level, or form value is in an
appendix/table/specification.

Good candidates:

- incorporation clause if needed for legal force;
- exact appendix/table row carrying the operative term.

Reject: appendix heading alone when a specific row exists.

## candidate/statutory-substitute

Matrix signal: acceptance, payment, termination, assignment, signature, or
document exchange procedure.

Good candidate: mandatory-law or incorporated-rule clause that governs the same
object and consequence.

Reject: generic legal-compliance wording with no operative mechanism.

## candidate/product-menu-scope

Matrix text lists card, QR, wallet, mobile, API, internet, terminal, or other
alternative channels.

Good candidate: clause governing the channel that is inside the contract scope.

Reject: treating every unused alternative as a separate candidate target unless
matrix fields make it mandatory.

## candidate/named-product-filter

Matrix requires a named payment instrument, platform, provider, API, wallet, QR,
biometric, or internet acquiring product.

Good candidate: clause regulating that named product or a true legal substitute.

Reject: generic card acquiring, terminal, tariff, or form row with no active
terms for the named product.

## candidate/payment-settlement-separation

Matrix signal: settlement act, operation-sum calculation, bank invoice, VAT
treatment, payment route, set-off, withholding, or reimbursement.

Good candidates: clauses that govern that same payment or settlement mechanism.

Reject: service acceptance or generic price clauses when the settlement legal
object is different.

## candidate/liability-package

Matrix signal: penalty, fine, damages, cap, non-liability, reimbursement,
chargeback.

Good candidates:

- liability basis;
- protected party;
- trigger;
- formula or amount;
- cap or exception;
- consequence.

Reject: broad responsibility wording with no matching trigger or consequence.

## candidate/confidentiality-object

Matrix signal: confidentiality of card security, transaction technology,
business information, financial information, or similar protected categories.

Good candidate: clause protecting the same information class or a broader
confidentiality clause that includes it.

Reject: personal-data processing alone when the protected object is not personal
data.

## candidate/exact-id

Good id: exact printed clause, subclause, appendix row, or table row.

Reject: normalized, translated, repaired, descriptive, or approximate ids.
