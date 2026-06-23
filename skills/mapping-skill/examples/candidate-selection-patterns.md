# Candidate Selection Patterns

Generic examples for candidate recall. They do not assign compliance status.

## candidate/umbrella-plus-child

Matrix signal: several detailed grounds, duties, penalties, or procedures.

Good candidates:

- umbrella clause that introduces the list and common legal consequence;
- child clause that states the exact ground, duty, formula, or exception.

Reject: child-only output when the parent gives the row legal force.

## candidate/appendix-row

Matrix signal: scope, tariff, device, service level, or form value is in an
appendix/table/specification.

Good candidates:

- incorporation clause if needed;
- exact appendix/table row carrying the operative term.

Reject: appendix heading alone when a specific row exists.

## candidate/statutory-substitute

Matrix signal: acceptance, payment, penalty, termination, signature, or document
exchange procedure.

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

## candidate/payment-package

Matrix signal: payment deadline, invoice, act, acceptance, set-off, withholding,
direct debit, payment demand, reimbursement.

Good candidates:

- payment obligation;
- document or acceptance trigger;
- route or collection mechanism;
- deadline and consequence.

Reject: generic price clause if the required mechanism is elsewhere or absent.

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

## candidate/channel-specific-notice

Matrix signal: named e-mail, EDI, platform, mailbox, courier, receipt proof, or
qualified signature process.

Good candidates:

- clause naming the channel;
- clause giving documents legal force;
- clause defining receipt date or proof.

Reject: generic electronic-document clause for a named-channel requirement.

## candidate/non-empty-before-missing

Before empty output, recover by legal element across payment, liability,
termination, appendix, notice, signature, mandatory-law, and incorporated-rule
zones.

Reject: empty candidate set without recovery evidence.

## candidate/exact-id

Good id: exact printed clause, subclause, appendix row, or table row.

Reject: normalized, translated, repaired, descriptive, or approximate ids.
