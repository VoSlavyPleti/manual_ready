---
name: mapping-skill
description: >
  Selects legally useful contract candidate clauses for acquiring risk-matrix
  items using legal-function analysis.
---

# mapping-skill

## Task

For each assigned matrix item, find the contract clauses that are legally useful
candidates for that item. This is a one-to-many mapping task: one matrix item
may have zero, one, or many contract candidates. The goal is candidate recall
with disciplined pruning: include clauses that perform or materially explain the
required legal function, and exclude clauses that are only topically similar.

The task is not numbering alignment, keyword matching, or semantic similarity
search. Match the legal function.

## Inputs

The task input must provide:

- matrix path or assigned matrix items;
- contract path or full contract text;
- assigned matrix ids, range, or batch file;
- exact output path.

Use matrix fields as follows:

- `number` only as the immutable output identifier in `matrix_id`;
- `enriched_text` or source text as the main legal-content source;
- `main_idea` to identify the required legal function;
- `topics` to identify the legal zone and likely search vocabulary;
- applicability fields;
- product, terminal, channel, payment-method, lot, and procurement restrictions.

Candidate selection must be driven by the legal meaning of `enriched_text`,
`main_idea`, and `topics`. Do not select candidates because matrix numbers,
contract clause numbers, headings, or words happen to look similar.

## Output

Save a JSON array to the exact assigned output path. Each item must use exactly
this schema:

```json
{
  "matrix_id": "<matrix number>",
  "contract_analog": ["<contract clause id>"],
  "candidate_analysis": [
    {
      "contract_id": "<contract clause id>",
      "matrix_evidence": "<short legal core of the matrix requirement>",
      "contract_evidence": "<short legal core of the contract clause>",
      "coverage": "<why this clause is a useful candidate>",
      "legal_role": "direct|parent|child|framework|payment|liability|notice|termination|appendix|context",
      "covered_elements": ["<matrix legal element covered by this clause>"]
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
      "candidate_ids": ["<contract clause id>"],
      "candidate_role": "direct|parent|child|framework|payment|liability|notice|termination|appendix|context",
      "search_result": "found|not_found"
    }
  ],
  "candidate_limit_reason": "<why no other clauses were added, or why the candidate set is empty>"
}
```

Rules:

- preserve `matrix_id` exactly from the matrix `number` field;
- preserve contract clause ids exactly as they appear in the contract;
- use decimal contract clause ids when the contract provides them, for example
  `5.1.1`, `2.3`, or `4.2.6.3`;
- never infer a candidate from numbering similarity;
- do not add fields outside the schema;
- use `contract_analog: []` and `candidate_analysis: []` when no useful
  candidate exists;
- when the candidate set is empty, `candidate_limit_reason` must name the
  recovery zones checked and why none produced a useful legal candidate;
- `contract_analog` must equal the set of
  `candidate_analysis[].contract_id`;
- `contract_analog` may contain multiple clauses for one matrix item when the
  legal function is split across contract provisions;
- every candidate must have one `legal_role` value from the schema and at least
  one `covered_elements` item;
- `matrix_legal_elements` must list the material legal elements extracted from
  `main_idea`, `topics`, and `enriched_text`;
- `element_candidate_map` must show which candidates were found for each
  material element, or `not_found` when no useful candidate exists;
- include exactly the assigned matrix ids once each.

Do not write a batch result to `outputs/matrix_contract_mapping.json` unless
that exact path was assigned for this task.

## Analysis Method

For every matrix item:

1. Build the active profile:
   - active product, channel, payment method, terminal, and lot mode;
   - inactive alternatives;
   - procurement or statutory framework;
   - whether the item concerns payment, liability, document exchange, notice,
     product activation, confidentiality, termination, technical duties, or
     legal framework.
2. Extract the legal core:
   - protected party;
   - legal object;
   - operative action;
   - trigger;
   - measure: deadline, amount, formula, cap, document, channel, list, or
     procedure;
   - legal consequence.
3. Search broadly by legal function and legal synonyms. Synonyms are search
   handles only; they are not proof that a candidate belongs.
4. Expand the candidate package with required parent, child, sibling, appendix,
   framework, payment, liability, notice, or termination clauses.
5. Build `matrix_legal_elements` and map each material element to direct,
   framework, payment, liability, notice, termination, appendix, or context
   candidates.
6. If no candidate remains, run Pre-Missing Recovery before returning an empty
   candidate set.
7. Remove false positives.
8. Write evidence that explains why each candidate belongs.

Do not stop at the first candidate. Many useful packages are scattered across
several sections.

## Pre-Missing Recovery

Before returning `contract_analog: []`, run a narrow recovery search by the
uncovered legal element. Check these contract zones even when the first search
found nothing:

- payment, settlement, invoice, act, acceptance, reimbursement, withholding,
  set-off, direct-debit, fee, and post-termination payment clauses;
- liability, penalty, fine, damages, cap, non-liability, reimbursement, and
  protected-risk clauses;
- termination, refusal, suspension, return, survival, reorganization, assignment,
  and post-termination clauses;
- confidentiality, personal-data, lawful-basis, consent, banking-secrecy, and
  information-use clauses;
- appendix incorporation, technical assignment, tariff, statement, form,
  specification, procurement, EIS, residual-law, and framework clauses;
- notice, document exchange, EDI, signature, mailbox, platform, proof-of-receipt,
  and channel clauses.

An empty candidate set is allowed only after recovery fails to find a clause with
the same protected party, legal object, trigger, or legal consequence. Record
that limit in `candidate_limit_reason`.

## Scattered Package Recall

When a direct clause is found, search for companion clauses that may supply a
mandatory legal element. Add them only when they materially explain the current
matrix item:

- parent clause creating legal force;
- appendix, tariff, table, form, or specification with the operative detail;
- payment deadline, amount basis, document route, payer, payee, or collection
  mechanism;
- liability consequence, formula, cap, protected party, or non-liability shield;
- termination ground, notice, effective date, survival, return, or settlement;
- framework clause changing source, trigger, procedure, remedy, or legal effect.

## Contract Row Candidate Recall

When a direct candidate is found, also search for parent, framework, context,
and cross-referenced clauses that may stand as separate legally useful contract
rows for the same matrix item. Add them only when they perform or materially
explain a legal element of the current item.

Always inspect clauses referenced by `clause`, `section`, `appendix`, table,
tariff, form, statement, or specification references when the referenced clause
defines one of these elements:

- scope, product, channel, terminal, operation, or party;
- deadline, term, amount, formula, cap, tariff, or payment basis;
- procedure, notice route, evidence route, acceptance route, or document route;
- liability trigger, protected party, penalty, cap, exception, or shield;
- applicable rules, standards, law, survival, return, assignment, or continuing
  consequence.

Do not add every referenced clause automatically. Add a referenced clause only
when it can be tied to a material element in `element_candidate_map`.

## Framework Anchor Recall

For matrix items about legal framework, payment-system rules, general party
duties, confidentiality, liability, term, termination, legal succession,
applicable law, incorporated documents, or continuing effects, include useful
framework anchors in addition to direct operative clauses.

A framework anchor belongs when it supplies:

- source of legal regulation;
- incorporated document force;
- rule or standard that controls performance;
- survival or post-termination effect;
- assignment, reorganization, or succession rule;
- legal consequence that limits or explains the operative clause.

Reject framework anchors that only repeat background law or section context
without changing a material element of the current item.

## Candidate Selection Rules

### Direct Operative Clauses

When the contract contains a direct operative clause that performs the exact
function named by the matrix, collect it first. Do not reject it merely because
the contract also contains generic framework language.

If the direct clause alone carries the legal function, do not add background
clauses merely because they are nearby.


### Procurement / Statutory Framework

For procurement or statutory contracts, check general legal framework clauses
when the matrix item concerns:

- legal admissibility or residual law;
- lawfulness of services;
- confidentiality and legal exceptions;
- electronic exchange legal force;
- tax, invoice, payment, or acceptance framework;
- liability formula or statutory penalty model;
- assignment, replacement, termination, or continuing legal consequences.

Use framework clauses as legal-function candidates, not as noise. Add them only
when they cover or materially explain the current item.

### Payment Package

For payment rows, identify the exact payment object first:

- acquiring commission for operations;
- separate terminal, software, subscription, or service fee;
- act, invoice, UPD, EIS acceptance document, or payment document;
- payment deadline;
- payer, payee, account, or payment route;
- reimbursement, withholding, direct debit, set-off, or demand;
- post-termination settlement.

Do not substitute one payment object for another. A general payment duty is not
the same candidate as a separate service fee or a bank-controlled collection
mechanism.

### Liability Package

For liability rows, check:

- general liability;
- party-specific liability;
- violation-specific clause;
- amount, formula, base, cap, accrual period, or statutory calculation;
- protected party and protected risk;
- non-liability shields.

Protected party controls candidate usefulness. A cap or penalty for one party is
not a candidate for an opposite-party requirement unless it materially explains
a broader liability framework.

### Personal Data Package

For personal-data rows, check:

- consent or confirmation of consent;
- covered persons;
- processing or transfer purpose;
- contract-performance purpose;
- protection, confidentiality, or lawful-basis duties.

The useful package must cover both the relevant person category and the legally
protected purpose or duty.

### Termination And Continuing Duties

For termination, suspension, return, settlement, survival, and continuing-duty
rows, check:

- termination or suspension right and grounds;
- notice and effective date;
- statutory termination framework;
- post-termination settlements;
- return, survival, and continuing duties.

Do not import unrelated confidentiality, merger, or survival clauses when the
current item only requires a direct continuing duty.

## False Positives

Reject a candidate when it is only topical and does not perform the same legal
function.

Reject these recurring near-misses:

- generic electronic form, qualified signature, or EDI clause for a matrix item
  that requires a specific document channel, platform, proof model, or named
  route;
- general payment, invoice, act, acceptance, or price clause for a separate
  bank-control mechanism such as demand, pre-acceptance, debit, set-off,
  withholding, approval, or payment trigger;
- general inspection, cooperation, support, or document request for a matrix item
  about fraud, business profile, issuer-bank verification, restricted-resource
  use, terminal security, or actual activity;
- technical capability, form field, checkbox, hardware name, or product mention
  for a matrix item that requires enforceable active product terms.


## Active Profile

Inactive products and channels do not create candidate gaps. Search for
enforceable terms that match the active profile.

A product, channel, terminal, software route, or payment method is legally
activated only when the contract creates an active package for it:

- activation or deactivation;
- price, tariff, or settlement;
- party duties;
- operating procedure;
- notice or support;
- liability or termination consequences.

Technical capability, a form field, a checkbox, or a hardware name is not legal
activation.

## Evidence

Evidence must be short and legal-function based:

- `matrix_evidence`: required legal function;
- `contract_evidence`: what the candidate clause provides;
- `coverage`: why this clause belongs in the candidate package.

Do not include a clause if you cannot explain how it helps prove the legal
function.

## Examples

Use `examples/candidate-selection-patterns.md` for candidate-selection examples.
Those examples show which clauses to select, which clauses to prune, and why a
candidate package is legally useful.

Do not infer answers from old benchmark ids, workbook labels, archived corpora,
or prior document-specific runs.

## Final QA

Before saving:

- every assigned matrix id is present once;
- JSON parses;
- no fields outside the output schema are present;
- every contract id in `contract_analog` appears once in `candidate_analysis`;
- every candidate has legal-function evidence;
- every candidate has `legal_role` and `covered_elements`;
- `matrix_legal_elements` lists material elements from the matrix content;
- `element_candidate_map` ties each material element to found candidates or
  records `not_found`;
- every empty candidate set has a `candidate_limit_reason` naming recovery
  zones checked;
- no topical near-miss is kept only because it shares vocabulary or section
  context;
- no candidate is kept because of matrix numbering, contract numbering, or
  clause proximity without the same legal function;
- the file is saved strictly to the assigned output path.
