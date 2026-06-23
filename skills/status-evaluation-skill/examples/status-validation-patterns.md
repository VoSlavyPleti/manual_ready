# Status Validation Patterns

Generic examples for package-level status evaluation.

## status/package-full-from-partial-rows

Matrix requires duty, document route, deadline, and consequence.

Contract package:

- row A creates the duty;
- row B gives the route;
- row C gives the deadline and consequence.

Result: `overall_status = full_match`.

Row status: A, B, and C may each be `contract_row_status = partial_match` when
they are incomplete alone.

Reason: package status and row contribution status answer different questions.

## status/direct-row-full-package-full

Matrix requires one operative duty with a trigger and consequence.

Contract row contains the same duty, trigger, and consequence.

Result: `overall_status = full_match`; that row may have
`contract_row_status = full_match`.

## status/package-incomplete

Matrix requires duty, deadline, and penalty.

Contract has duty and deadline, but no penalty or equivalent consequence.

Result: `partial_match`.

Named gap: consequence missing.

## status/adjacent-only-is-missing

Matrix requires a specific right, trigger, and consequence.

Contract mentions the same topic but lacks the trigger or consequence.

Result: `missing` if no other useful candidate exists.

Reason: topic adjacency is not a legal analog.

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

## status/lifecycle-trigger-required

Matrix requires automatic connection, activation, installation, suspension,
support, access, or proof procedure.

Contract only mentions product capability or appendix availability.

Result: `missing` if the lifecycle trigger is absent, or `partial_match` only
when another useful clause contains the same operative mechanism.

## status/statutory-equivalent

Matrix requires acceptance document with signature and reject function.

Contract uses mandatory statutory electronic acceptance with the same accept or
reasoned-refusal result.

Result: `full_match`.

Reason: different legal route, same enforceable result.

## status/statutory-not-blanket-full

Matrix fixes an economic amount, formula, penalty trigger, liability cap,
protected party, or special bank-control mechanism.

Contract relies on a mandatory-law regime but changes that material term.

Result: `partial_match`.

Reason: mandatory law can substitute procedures, but it does not erase material
economic or protected-party differences.

## status/deadline-statutory-route

Matrix has a standard commercial deadline. Contract is governed by a mandatory
statutory process with a different deadline but the same accept/pay/remedy
result.

Result: `full_match`.

Reason: mandatory framework preserves the legal result.

## status/bank-controlled-payment

Matrix requires accepted payment demand, set-off, withholding, direct debit, or
another bank-controlled collection mechanism.

Contract uses ordinary payment order or ordinary post-acceptance payment.

Result: `partial_match`.

Reason: payment exists, but the control mechanism is weaker or different.

## status/deadline-changed

Matrix contains a fixed deadline and no mandatory framework substitutes it.

Contract has a different deadline.

Result: `partial_match`.

Named gap: deadline changed.

## status/payment-settlement-object

Matrix requires a settlement act, settlement invoice, VAT treatment, operation
sum, set-off, withholding, or bank-controlled collection.

Contract has only service acceptance or ordinary payment language.

Result: `missing` when the settlement object is absent; `partial_match` when the
same mechanism exists but a material parameter differs.

## status/liability-source-changed

Matrix fixes a fine, penalty, cap, amount source, or appendix schedule.

Contract calculates the same liability through a different statute, regulation,
or external source.

Result: `partial_match` when the source changes the economic risk allocation.

## status/confidentiality-vs-personal-data

Matrix protects card security, transaction technology, business, financial, or
other confidential information.

Contract protects only personal data.

Result: `missing` if no broader confidentiality clause exists.

Reason: the protected legal object differs.

## status/non-liability-vs-indemnity

Matrix says one party is not liable for a defined claim category.

Contract only gives that party indemnity for losses.

Result: `partial_match` only if the same claim category and protected party are
preserved; otherwise `missing`.

## status/placeholder-not-gap

Matrix and contract use blank fields for a rate, site, identifier, or form value
to be completed later. No conflicting value is stated.

Result: `full_match`.

Reason: completion placeholder is not a changed term.

## status/named-mechanism-blank

Matrix requires a named EDI provider, platform, mailbox, tariff source, website,
proof provider, or payment-system channel.

Contract leaves that named mechanism blank.

Result: `partial_match` unless `main_idea` says the blank is acceptable.

Reason: the missing name affects the enforceable route or source.

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

## status/equivalent-not-status

Checklist may mark an element `equivalent`.

Result: final `overall_status` remains `full_match` if all elements are covered
or equivalent. Never output `equivalent` as final status.
