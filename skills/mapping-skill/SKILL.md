---
name: mapping-skill
description: >
  Find legally meaningful contract candidate clauses for each item in a
  standard acquiring risk matrix. Use for candidate recall only.
---

# mapping-skill

## Purpose

For each assigned matrix item, return the contract clauses that may legally
cover, qualify, implement, limit, evidence, or explain the matrix requirement.

The matrix is the bank standard. The incoming contract is checked against that
standard. This skill only builds the candidate pool. It does not assign
compliance status.

## Inputs

Use only the assigned data:

- matrix items from `inputs/matrix.json`;
- contract text from `inputs/contract.txt`;
- assigned matrix ids or ranges;
- exact output path.

Matrix field priority:

1. `main_idea`: legal risk focus and what must be preserved.
2. `enriched_text`: operative wording of the standard requirement.
3. `topics`: search vocabulary and navigation hints.
4. applicability fields: product, terminal, channel, lot, payment method, scope.
5. `number`: output id only; never a matching signal.

If `enriched_text` lists a menu of alternative products, channels, payment
instruments, documents, or devices, search for the part that is inside the
contract scope. Do not treat every unused alternative as a separate candidate
target unless the matrix fields or `main_idea` make that alternative mandatory.

## Output Schema

Save a JSON array to the assigned output path:

```json
{
  "matrix_id": "<matrix number>",
  "contract_analog": ["<exact contract clause id>"],
  "candidate_analysis": [
    {
      "contract_id": "<exact contract clause id>",
      "legal_role": "direct|parent|child|framework|payment|liability|notice|termination|appendix|context",
      "matrix_evidence": "<short legal core from the matrix>",
      "contract_evidence": "<short legal content of this clause>",
      "coverage": "<why this clause is legally useful>",
      "covered_elements": ["<matrix legal element this clause may cover>"]
    }
  ],
  "matrix_legal_elements": [
    {
      "element": "<material legal element>",
      "element_type": "scope|party|trigger|deadline|amount|formula|channel|framework|liability|procedure|survival|other",
      "source_field": "main_idea|topics|enriched_text"
    }
  ],
  "element_candidate_map": [
    {
      "element": "<material legal element>",
      "candidate_ids": ["<exact contract clause id>"],
      "candidate_role": "direct|parent|child|framework|payment|liability|notice|termination|appendix|context",
      "search_result": "found|not_found"
    }
  ],
  "candidate_limit_reason": "<why no other clauses were added, or why none were found>"
}
```

`contract_analog` must equal the set of `candidate_analysis[].contract_id`.
Use exact clause ids as printed in the contract. Do not add parenthetical
explanations, translations, repaired numbering, or invented ids.

If the legal rule is in an appendix, table, form, or technical assignment row,
use the most specific row-level id available, for example `Приложение №1 п.5`.
Descriptions belong in evidence fields, not in ids.

## Workflow

### 1. Extract Legal Elements

For each matrix item, extract:

- functional roles: bank/acquirer/executor, merchant/customer/enterprise,
  cardholder, operator, payment system, third party;
- legal object: service, operation, money, terminal, data, document, risk,
  payment instrument, product, channel;
- required right, duty, prohibition, permission, remedy, or procedure;
- trigger or condition;
- deadline, amount, formula, cap, tariff, currency, payment route;
- notice route, document form, signature, proof, platform, appendix, table;
- product/scope restriction.

Search by legal function and matrix field priority, not by clause numbering or
isolated word overlap.

### 2. Search By Legal Function

Use headings and keywords only to navigate. Include a clause only when it may
supply a material element or materially explain another candidate.

Search across:

- definitions, subject, scope, services, and incorporated documents;
- rights and obligations of each functional role;
- payment, acceptance, invoice, act, set-off, withholding, reimbursement;
- equipment, terminal, software, security, return, support;
- liability, penalties, caps, exceptions, non-liability, indemnity, chargeback;
- notice, document exchange, EDI, e-mail, platform, signature, proof;
- term, termination, refusal, suspension, survival, post-termination settlement;
- procurement, mandatory law, payment-system rules, privacy rules, framework
  documents, appendices, specifications, forms, tables.

### 3. Preserve Contract Row Level

Include the contract row that carries the legal rule and any row that gives that
rule legal force.

Add the parent or umbrella clause when it:

- introduces a list of grounds, rights, duties, penalties, documents, or
  procedures later detailed in child clauses;
- allocates the party, object, trigger, scope, or common consequence for child
  clauses;
- incorporates an appendix, specification, table, form, statute, or external
  rule;
- states that a set of child clauses is exhaustive or applies as a package;
- is the contract row a reviewer would cite for the whole package.

Add the child clause when it supplies the concrete trigger, deadline, amount,
formula, exception, document, or consequence.

For appendix/table content, include:

- the main clause that incorporates the appendix when needed for legal force;
- the exact appendix/table/specification row carrying operative content;
- cross-referenced rows that define scope, timing, payment, liability, notice,
  or consequence.

### 4. Package Scattered Candidates

If one candidate is found, search for companion clauses that supply uncovered
parts of the same legal package:

- framework or statutory source;
- product or scope limitation;
- payment route, price base, invoice, act, acceptance, document deadline;
- liability trigger, protected party, cap, formula, exception, penalty amount;
- notice method, receipt proof, signature, platform, EDI route;
- termination ground, return duty, survival, post-termination settlement.

Do not stop at the first direct clause when the contract distributes the legal
requirement across several rows.

### 5. Regulatory And Framework Recall

For contracts governed by mandatory public-procurement, banking, payment-system,
privacy, or other regulatory frameworks, include clauses that implement the
matrix function through that framework even when wording differs.

Useful candidates include:

- statutory acceptance or refusal procedure for a matrix act/acceptance rule;
- procurement payment or penalty mechanism for a matrix payment/liability rule;
- mandatory electronic platform/signature rule for a matrix document-exchange
  rule;
- incorporated payment-system or banking rules for operational consequences.

Include these candidates when they govern the same legal object and consequence.

### 6. False Positive Filter

Reject clauses that are only topically similar.

Common false positives:

- generic e-signature for a matrix item requiring a specific platform, mailbox,
  proof model, provider, or EDI process;
- ordinary card acquiring, POS terminal, generic tariff, or payment clause for a
  named product/channel such as QR, biometric payment, tokenized wallet, mobile
  payment, internet acquiring, API, or another separately named instrument;
- generic payment/invoice/act wording for a distinct collection mechanism such
  as direct debit, set-off, payment demand, acceptance, withholding;
- general inspection/cooperation/request rights for fraud, issuer verification,
  business-profile control, terminal security, or restricted-resource use;
- a duty to cooperate, not obstruct, undergo instruction, or follow a procedure
  for a matrix item requiring a direct audit, investigation, compliance,
  verification, or instruction-compliance right;
- a clause covering only a minor adjacent element when `main_idea` identifies a
  different legal core as the risk focus;
- a generic QR, card, terminal, tariff, currency, form, or appendix mention for
  a matrix item requiring a lifecycle trigger such as automatic connection,
  installation, activation, support, suspension, or proof procedure;
- a generic electronic contract, copy-count, annex-list, notice, or address
  boilerplate clause for a matrix item requiring a different formal legal object;
- technical capability, form field, product label, or appendix title without an
  enforceable right, duty, trigger, or consequence.

If the matrix item is product-specific, a generic acquiring clause is not enough
unless it actually regulates that product or a clear legal substitute.

If the matrix item is common-scope and merely lists product/channel alternatives,
do not reject a common acquiring clause only because unused alternatives are not
present in the contract.

If `main_idea` states that a certain similar clause is not on-topic, follow that
instruction and reject that clause type.

### 7. Empty Candidate Recovery

Before returning an empty list, search the uncovered legal element in:

- payment/settlement/acceptance/invoice/act/withholding/set-off;
- liability/penalty/fine/damages/cap/non-liability/reimbursement;
- termination/refusal/suspension/return/survival/post-termination;
- confidentiality/personal data/banking secrecy/information use;
- appendix/specification/tariff/form/technical assignment/framework;
- notice/document exchange/EDI/signature/mailbox/platform/proof;
- mandatory law, procurement rules, payment-system rules, incorporated rules.

`candidate_limit_reason` must name the checked zones and the legal element that
remained uncovered.

## Final Checks

Before saving:

- every assigned matrix id appears exactly once;
- every candidate id appears in the contract text;
- every `contract_analog` id has a matching `candidate_analysis` object;
- parent/umbrella, child, appendix, table, and cross-reference rows were checked;
- appendix/table candidates use specific row ids when available;
- empty candidate rows include recovery evidence;
- false positives were removed;
- no compliance status is assigned.
