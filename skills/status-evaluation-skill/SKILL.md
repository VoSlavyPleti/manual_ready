---
name: status-evaluation-skill
description: >
  Evaluate legal coverage status for standard acquiring matrix items against
  supplied contract candidate packages.
---

# status-evaluation-skill

## Purpose

For each assigned matrix item, decide whether the cited contract candidate
package fully covers the bank standard requirement.

The matrix is the standard. Any material deviation from the matrix is a risk
unless the contract package, a mandatory legal framework, or an incorporated
document preserves the same enforceable result.

## Inputs

Use only the assigned data:

- matrix item or matrix path;
- contract text;
- candidate package for the matrix item;
- assigned matrix ids;
- exact output path.

The candidate package is evidence, not authority. Re-read the matrix item and
the cited contract clauses before finalizing status.

Matrix field priority:

1. `main_idea`: legal risk focus and materiality signal.
2. `enriched_text`: operative standard wording.
3. `topics`: search and evidence hints, not an automatic checklist.
4. applicability fields: product, terminal, channel, lot, payment method, scope.
5. `number`: output id only; never a status signal.

When `enriched_text` contains a menu of alternative products, channels, payment
instruments, documents, or devices, evaluate the part that is inside the
contract scope unless the matrix fields or `main_idea` make every alternative a
mandatory requirement.

## Output Schema

Save a JSON array:

```json
{
  "matrix_id": "<matrix number>",
  "contract_analog": ["<contract clause id>"],
  "overall_status": "full_match|partial_match|missing",
  "legal_analysis": [
    {
      "contract_id": "<contract clause id>",
      "contract_row_status": "full_match|partial_match",
      "package_role": "direct|parent|child|framework|payment|liability|notice|termination|appendix|companion|context",
      "matrix_evidence": "<material matrix requirement>",
      "contract_evidence": "<contract legal content>",
      "coverage": "<what this clause contributes>",
      "discrepancies": ["<material row-level gaps, if any>"]
    }
  ],
  "status_checklist": [
    {
      "element": "<material legal element>",
      "result": "covered|equivalent|different|missing|not_applicable",
      "contract_ids": ["<contract clause id>"],
      "discrepancy": "<empty unless different or missing>"
    }
  ],
  "reasoning": "<short final explanation>"
}
```

Allowed `overall_status` values:

- `full_match`
- `partial_match`
- `missing`

`equivalent` is only a checklist result, never an `overall_status`.

Every id in `contract_analog` must have one matching `legal_analysis` object.
Do not put explanations, translations, or repaired numbering inside ids.
Each `legal_analysis` object must include `contract_row_status`. This is the
standalone contribution of that contract row, not a replacement for
`overall_status`.

## Status Rule

Use package-level status for each matrix item:

- `missing`: no useful contract candidate exists, including when the relevant
  product, channel, device, or legal mechanism is absent from the contract.
- `full_match`: the non-empty candidate package covers or legally substitutes
  every material matrix element.
- `partial_match`: at least one useful candidate exists, but at least one
  material element is absent, narrower, weaker, inverted, delayed, changed, or
  moved to a materially different mechanism.

Several contract clauses may be incomplete alone but full together. Evaluate the
candidate package as a whole.

Never use `full_match` or `partial_match` with an empty `contract_analog`.

Also evaluate each cited contract row inside `legal_analysis`:

- `contract_row_status = full_match` when that row, read with its inseparable
  parent, child, sibling, appendix, and cross-referenced rows, contains or
  legally substitutes the matrix core for the row's role;
- `contract_row_status = partial_match` when the row is a useful analog or
  package member but its local row package is narrower, procedural,
  framework-only, or missing a material element.

Do not let an unrelated strong direct row upgrade another framework, parent,
penalty, payment, or context row to row-level `full_match`. But do allow local
family coverage: a parent row may be row-level `full_match` when its child rows
provide the details, and a child row may be row-level `full_match` when its
parent supplies the protected party, scope, or common consequence.

Do not downgrade the package `overall_status` merely because individual package
members are partial alone.

## Workflow

### 1. Build A Material Checklist

Extract material elements using matrix field priority:

- functional roles and protected party;
- legal object: money, service, operation, terminal, data, document, risk,
  payment instrument, product, channel;
- right, duty, prohibition, permission, remedy, or procedure;
- trigger or condition;
- deadline, amount, formula, cap, currency, tariff, payment route;
- notice route, platform, provider, signature, proof, document form;
- scope: product, terminal, operation, person category, territory, lot;
- consequence: liability, refusal, suspension, termination, reimbursement,
  non-liability, survival.

Do not turn every word in `topics` or every alternative in `enriched_text` into
a mandatory element. Use `main_idea` and applicability fields to decide what is
material.

### 2. Evaluate Coverage

For each material element, assign:

- `covered`: same legal element exists in the contract;
- `equivalent`: different drafting route preserves the same enforceable result;
- `different`: element exists but materially changes the matrix result;
- `missing`: element is absent;
- `not_applicable`: subordinate element is outside the contract scope while the
  row still has useful candidates.

A clause supports an element only if it governs the same functional role, legal
object, trigger, and consequence. Translate labels by function: for example,
merchant/customer/enterprise and bank/acquirer/executor may be equivalent roles
depending on the contract structure.

### 3. Full-Preserving Differences

Keep `full_match` when the legal result is preserved despite a drafting
difference.

Common full-preserving differences:

- the contract selects one product/channel from a matrix menu and does not
  include unused alternatives;
- product names, payment instruments, QR/wallet/mobile variants, terminal
  variants, card-system lists, website references, or support channels from a
  matrix menu are not gaps when the contract scope is narrower and the
  `main_idea` does not make those variants the risk focus;
- a blank rate, site, identifier, or form field is a completion placeholder and
  no conflicting value is stated;
- the matrix standard itself uses blanks, underscores, or an application/form
  placeholder for the same value;
- a mandatory public-procurement, banking, payment-system, privacy, or other
  legal framework supplies an equivalent procedure, deadline, document,
  acceptance, refusal, termination, signature, assignment, or payment mechanism
  for the same enforceable result;
- a broader notice or document-exchange route includes the matrix route;
- the operative duty exists but a clause does not repeat a cross-reference to a
  procedure, notice, document-exchange, appendix, or website section;
- a contract refers to compliance with the contract, technical assignment,
  appendix, incorporated procedure, or mandatory platform instead of repeating
  the matrix label for an operational procedure;
- document titles, appendix numbers, party labels, procurement terminology, or
  drafting style differ without changing legal effect;
- examples or illustrative force-majeure events differ, while the same
  force-majeure release and open-ended coverage are preserved.
- a service company, operator, contractor representative, or bank agent is used
  as the operational actor while the same party remains legally responsible;
- statutory electronic acceptance, payment, termination, assignment,
  reorganization, and signature routes replace the matrix commercial procedure
  in a mandatory public-procurement contract and preserve the same enforceable
  result;
- a mandatory public-procurement acceptance or payment route uses a statutory
  deadline instead of the matrix commercial deadline, while the same accept,
  reasoned-refusal, payment-basis, and payment-obligation result is preserved;
- a mandatory public-procurement rule restricts assignment, contractor
  replacement, unilateral refusal, or reorganization differently from the bank
  template, while the same protective result is supplied by mandatory law;
- consent/legal-basis wording for personal data is drafted through consent
  withdrawal, loss of legal basis, or warranty language, while the same data
  categories, transfer purpose, and party responsibility are preserved;
- a contract names some incorporated appendices or acceptance documents in the
  operative clauses instead of using a single general "all appendices are
  integral parts" formula.

Do not use `partial_match` unless the discrepancy changes enforceable rights,
duties, remedies, timing, amounts, scope, triggers, procedures, or protected
party.

Mandatory-law equivalence is not a blanket rule. It preserves `full_match` for
statutory acceptance, payment, termination, signature, assignment,
reorganization, and document routes when the same legal result is mandatory. It does not preserve
`full_match` when the matrix fixes an economic amount, formula, liability cap,
penalty trigger, protected party, or special control mechanism and the contract
uses a materially different one.

Do not treat a blank as harmless when the matrix requires a named external legal
mechanism: EDI provider, platform, payment system, mailbox, website, registry,
tariff source, proof provider, or support channel. A blank named mechanism is a
material gap unless `main_idea` says that an unfilled placeholder is acceptable.

### 4. Hard Partial Gates

Use `partial_match` when any gate is triggered:

- named platform/provider/channel gate: the matrix requires a named EDI system,
  platform, provider, mailbox, proof model, or channel and the contract leaves
  that name blank or replaces it with a materially different one;
- named lifecycle/procedure gate: the matrix requires automatic connection,
  installation, activation, suspension, support, access, or proof procedure and
  the contract only mentions the product/channel without that lifecycle trigger;
- economic term gate: a fixed amount, rate, cap, penalty, formula, currency, or
  payment route is changed, unless the matrix itself uses a placeholder for that
  value or a mandatory framework supplies an equivalent economic result;
- bank-control/payment-mechanism gate: bank-controlled collection, direct debit,
  set-off, payment demand, acceptance, withholding, or reimbursement is replaced
  by an ordinary payment order or weaker mechanism;
- party/protected-role gate: the duty, liability, protection, or remedy is put
  on the wrong functional role or protects the wrong party;
- scope gate: coverage is limited to materially fewer products, channels,
  operations, persons, terminals, territories, or documents than the matrix
  requires for the contract scope;
- consequence gate: the trigger exists but the remedy, refusal right,
  suspension, termination, non-liability, reimbursement, penalty, or survival
  consequence is absent or weaker.
- forum/jurisdiction gate: a general legal-dispute rule is replaced with a
  different mandatory forum, exclusive court, venue, or party-favorable
  jurisdiction rule.

The bank-control/payment-mechanism gate overrides generic payment equivalence:
ordinary statutory payment, ordinary invoice payment, or ordinary payment order
does not fully match a matrix rule whose legal core is bank-controlled
collection, accepted payment demand, set-off, withholding, or unilateral
reimbursement.

The liability economic gate overrides generic mandatory-law equivalence when a
contract row calculates a fine, penalty, cap, or liability amount through an
external statute or regulation while the matrix fixes a different source,
amount, formula, or appendix-based schedule.

If a package-level gap applies to the whole matrix proposition, apply that gap
to direct `contract_row_status` values too. Do not mark a direct row full when
the same direct row is part of a package that is partial because the bank right,
named mechanism, protected party, trigger, or economic source is absent.

If a cited clause is only adjacent, implicit, or weaker and does not share the
same functional role, legal object, trigger, and consequence, treat it as not a
useful candidate. If no other useful candidate exists, use `missing`, not
`partial_match`.

Use `missing`, not `partial_match`, for these adjacent-only patterns:

- product capability or appendix label without the required lifecycle trigger;
- general suspension without the matrix trigger;
- document request without the required third-party verification route;
- personal-data clause without the required confidentiality object;
- electronic-form clause for paper-copy/original-copy allocation;
- service-acceptance document for a settlement act, settlement invoice, VAT
  treatment, or operation-sum calculation;
- indemnity or damages clause for a non-liability rule, unless it preserves the
  same protected party and claim category.

### 5. Missing Discipline

Use `missing` only when no useful candidate exists after targeted recovery.

Use `missing`, not `full_match`, when the only reason for non-coverage is that
the contract does not include the matrix product, channel, device, or mechanism.

Before `missing`, search for the uncovered element in:

- definitions, subject, rights, obligations;
- payment, acceptance, invoices, acts, set-off, withholding;
- appendices, specifications, technical assignments, tariffs, forms;
- liability, penalties, caps, non-liability;
- notices, EDI, signature, platform, proof;
- termination, return, survival, post-termination;
- mandatory law and incorporated rules.

If a useful candidate exists but is incomplete, status is `partial_match`.

### 6. Full Match Challenge

Before final `full_match`, challenge it with these questions:

- Does the package cover the material role, object, trigger, scope, procedure,
  deadline, amount/formula, channel, and consequence?
- Is any named platform/channel/provider required and missing?
- Is any fixed economic or liability term changed?
- Is the protected party or obligated party inverted?
- Is the apparent gap only a label, placeholder, unused option, cross-reference,
  public-procurement route, or drafting difference?

If the challenge identifies a changed legal effect, use `partial_match`.
If it identifies only a full-preserving difference, keep `full_match`.

### 7. Evidence Rules

Evidence must be short and auditable:

- cite exact contract ids;
- summarize the legal core, not long quotations;
- explain the package-level result, not isolated clause similarity;
- do not rely on external answer labels, prior runs, or clause-number similarity;
- do not invent contract clauses.

## Final Checks

Before saving:

- every assigned matrix id appears exactly once;
- `contract_analog` equals `legal_analysis[].contract_id`;
- every `legal_analysis` row has `contract_row_status` and `package_role`;
- `missing` rows have empty `contract_analog` and `legal_analysis`;
- every `full_match` or `partial_match` row has at least one candidate;
- every `full_match` has no material checklist result `different` or `missing`;
- every `partial_match` has a named material gap;
- unused matrix-menu alternatives were not treated as gaps;
- hard partial gates were not hidden as `full_match`;
- `overall_status` is only `full_match`, `partial_match`, or `missing`.
