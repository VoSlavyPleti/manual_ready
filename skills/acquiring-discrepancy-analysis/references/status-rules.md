# Status And Risk Rules

Use these rules after true legal links are built. They calibrate the group-level
status and risk level. They do not relax the analogue threshold.

## Group-Level Status

Assign status to the group, not to each atomic pair.

- `aligned`: the contract package preserves the matrix legal result.
- `deviation`: a true analogue exists, but a material element is changed,
  narrowed, weakened, omitted, shifted, or blank.
- `missing_in_contract`: no true contract analogue exists for an applicable
  matrix requirement.
- `extra_in_contract`: a legally meaningful contract proposition has no matrix
  analogue.
- `not_material`, `out_of_scope`, and `not_applicable` are internal ledger
  closures unless the output contract says otherwise.

`atomic_links` are traceability rows only and inherit the group relationship.

## Hard Terms

Compare hard terms directly:

- same material deadline, amount, formula, cap, penalty, protected party,
  trigger, procedure, liability, remedy, or consequence can be `aligned`;
- changed or missing value is `deviation`;
- a hard term from another clause counts only when that clause expressly
  governs the same obligation or is explicitly incorporated;
- a neighboring date, amount, or procedure for another legal object cannot
  cure the gap.

An applicable blank or placeholder remains `deviation`, normally low risk. Do
not create an exception for administrative-looking placeholders when the field
is part of an applicable matrix or contract requirement.

For document, evidence, reporting, confirmation, chargeback, request-response,
and transaction-information duties, the response or performance deadline is a
hard term. Before marking such a group `aligned`, re-read the source text for
the exact period and trigger. If the analogue has the same duty but omits,
changes, or moves the deadline to another unincorporated procedure, use
`deviation`.

When the source text says the same confirmation/evidence duty but lacks the
matrix response period, do not infer the matrix period from similarity of
topic. The duty is linked, but the status is `deviation` unless another
incorporated clause supplies the period for that exact duty.

See examples: `Changed Or Missing Deadline`, `Borrowed Hard Term Does Not Cure Gap`, `Placeholder In Applicable Term`, `Document Or Evidence Deadline Is A Hard Term`.

## Functional Equivalence

Do not downgrade for formal differences alone: heading, title, appendix label,
permitted option selection, equivalent mandatory-law mechanism, or wording
style.

Do not downgrade for low-risk notes when the legal result is preserved. If the
difference is merely terminological, beneficial to the Bank, already
incorporated through another clause, or caused only by a mandatory-law
mechanism that preserves the Bank's practical right, keep `aligned`.

For public-procurement contracts, an EIS acceptance route, budget-payment
route, statutory document form, or customer-side payment act is not a
deviation by itself. Treat it as `aligned` when it preserves the same economic
obligation, payment trigger, evidence of performance, protected party, and
enforceability. Use `deviation` only when the procurement mechanism changes a
material hard term or weakens the Bank-standard legal result.

For technical-operation permissions, do not require the contract to repeat
every negative or explanatory phrase from the matrix. If the contract grants
the same permission for the same technical action and does not add a notice
duty, restriction, changed trigger, or weaker consequence, keep `aligned`.

For force-majeure and comparable standard risk-allocation clauses, compare the
legal effect, not the exact list of examples. A different illustrative list is
not a deviation when the clause still covers extraordinary unavoidable events,
releases liability for the same period, and preserves the same consequence.

Functional equivalence cannot override a missing or changed hard term.

See examples: `Formal Label Difference`, `Low-Risk Note Does Not Force Deviation`, `Slash Options`, `Technical Permission Without Extra Notice Gap`, `Force Majeure Equivalent List`.

## 44-FZ And Mandatory-Law Calibration

Mandatory 44-FZ/GK/EIS mechanics are not deviations by themselves. Evaluate
their legal effect:

- if the mandatory-law mechanism preserves the Bank-standard legal result,
  keep `aligned`;
- if it changes payment timing, acceptance control, withholding right,
  penalty/cap, termination power, protected party, evidence channel, or
  enforceability, use `deviation`;
- if a mandatory-law clause exists only because public procurement requires it
  and has no matrix analogue, use low-risk `extra_in_contract` when the clause
  has independent legal effect;
- if it is only a heading, formality, or procedural scaffold, close it as
  `not_material` in the ledger.

Do not mark a payment, acceptance, document, or termination group as
`deviation` merely because the contract uses the statutory route required for
the contract type. First identify the matrix legal object, then compare the
actual legal result.

See examples: `Procurement Mechanism As Analogue`, `Procurement Mechanism With Material Deviation`, `Mandatory-Law Extra`.

## Bank Right Displaced By Mandatory Law

When the matrix gives the Bank a unilateral right but the contract omits or
restricts it because mandatory procurement law limits that unilateral power,
do not treat the issue as harmless. The matrix requirement remains absent or
weakened.

Use `missing_in_contract` when no true contract analogue exists. Use
`deviation` when the contract contains a narrower substitute. Risk is normally
`medium` when statutory mechanisms partially compensate the Bank, and `high`
when the omitted right is central and no practical substitute exists.

See example: `Bank Right Displaced By Mandatory Law`.

## Liability Package

Before marking a liability group `aligned`, check amount, formula, cap,
trigger, protected party, excluded delay/non-delay buckets, claim procedure,
damages, and remedy survival across the package.

General fault-based liability does not close a special Bank exemption, special
penalty, or special cap rule unless it preserves the same protected party and
legal consequence.

When liability is split into root rights and child formulas, keep the direction
of liability separate. A clause about customer delay, Bank delay, customer
non-delay breach, and Bank non-delay breach may sit in one section but can map
to different matrix requirements and different statuses.

See examples: `Liability Group Review`, `Changed Amount, Formula, Cap, Or Penalty`.

## Risk Level

Use `risk_level` consistently:

- `none`: only for `aligned`;
- `low`: optional applicable missing, applicable placeholder, formal but
  legally manageable gap, or mandatory-law extra with no adverse Bank-specific
  effect;
- `medium`: material deviation that can affect performance, evidence, payment,
  control, liability, enforceability, or a Bank right displaced by mandatory
  law with partial statutory compensation;
- `high`: mandatory applicable missing, changed protected party, major
  payment/remedy change, important Bank right omitted without substitute, or
  broad contract-only risk.

Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
a short evidence-based reason. Use concise quotes rather than long excerpts.
