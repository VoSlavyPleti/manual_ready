# Status Validation Patterns

Generic examples for package-level status evaluation.

## status/package-full

Matrix requires duty, document route, deadline, and consequence.

Contract package:

- clause A creates the duty;
- clause B gives the route;
- clause C gives the deadline and consequence.

Result: `full_match`.

Reason: individual clauses may be incomplete alone, but the package covers all
material elements.

## status/package-incomplete

Matrix requires duty, deadline, and penalty.

Contract has duty and deadline, but no penalty or equivalent consequence.

Result: `partial_match`.

Named gap: consequence missing.

## status/product-absent

Matrix item applies only to a named product/channel outside the contract scope.

Contract has no functional substitute.

Result: `missing`.

Reason: absent product scope is not `full_match`.

## status/product-menu-unused-options

Matrix text lists several alternative acquiring channels. Contract is scoped to
one channel and fully regulates it.

Result: `full_match`.

Reason: unused menu alternatives are not gaps unless matrix fields make them
mandatory.

## status/named-product-required

Matrix specifically requires a named QR/API/wallet/EDI/platform product.

Contract has only ordinary card acquiring or generic e-document wording.

Result: `missing` or `partial_match` if the generic clause is legally useful.

Reason: named product/channel is the legal object.

## status/statutory-equivalent

Matrix requires acceptance document with signature and reject function.

Contract uses mandatory statutory electronic acceptance with the same accept or
reasoned-refusal result.

Result: `full_match`.

Reason: different legal route, same enforceable result.

## status/statutory-not-equivalent

Matrix gives one party bank-controlled collection or unilateral remedy.

Contract replaces it with ordinary payment order or weaker procedure, and no
mandatory rule preserves the control.

Result: `partial_match`.

Named gap: control mechanism weakened.

## status/placeholder-not-gap

Matrix and contract use blank fields for a rate, site, identifier, or form value
to be completed later. No conflicting value is stated.

Result: `full_match`.

Reason: completion placeholder is not a changed term.

## status/named-platform-blank

Matrix requires a named EDI system, platform, provider, mailbox, or proof model.

Contract leaves that name blank or replaces it with a materially different
channel.

Result: `partial_match`.

Named gap: required named channel not preserved.

## status/broader-channel

Matrix requires a specified notice route. Contract permits any contractual route
and the specified route is available elsewhere.

Result: `full_match`.

Reason: broader route includes the matrix function.

## status/missing-cross-reference

Matrix repeats a cross-reference to procedure or document-exchange rules.

Contract states the operative duty and the procedure exists elsewhere.

Result: `full_match`.

Reason: omitted cross-reference text is not a material gap.

## status/deadline-changed

Matrix contains a fixed deadline and no mandatory framework substitutes it.

Contract has a different deadline.

Result: `partial_match`.

Named gap: deadline changed.

## status/deadline-statutory-route

Matrix has a standard commercial deadline. Contract is governed by a mandatory
statutory process with a different deadline but the same accept/pay/remedy
result.

Result: `full_match`.

Reason: mandatory framework preserves the legal result.

## status/economic-term-changed

Matrix states a fixed amount, cap, rate, formula, currency, or penalty.

Contract states a different value and no mandatory equivalent applies.

Result: `partial_match`.

Named gap: economic term changed.

## status/party-inverted

Matrix imposes liability or duty on the merchant/customer role.

Contract imposes it on the bank/acquirer/executor role, or protects the wrong
party.

Result: `partial_match`.

Named gap: functional role changed.

## status/force-majeure-examples

Matrix and contract both provide force-majeure release and open-ended coverage,
but illustrative event lists differ.

Result: `full_match`.

Reason: examples differ; legal consequence is preserved.

## status/formal-label

Matrix uses one document title or appendix number. Contract uses another title
for the same operative rule.

Result: `full_match`.

Reason: label difference is not a legal gap.

## status/equivalent-not-status

Checklist may mark an element `equivalent`.

Result: final `overall_status` remains `full_match` if all elements are covered
or equivalent. Never output `equivalent` as final status.
