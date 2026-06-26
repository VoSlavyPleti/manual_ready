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

See examples: `Changed Or Missing Deadline`, `Borrowed Hard Term Does Not Cure Gap`, `Placeholder In Applicable Term`.

## Functional Equivalence

Do not downgrade for formal differences alone: heading, title, appendix label,
permitted option selection, equivalent mandatory-law mechanism, or wording
style.

Do not downgrade for low-risk notes when the legal result is preserved. If the
difference is merely terminological, beneficial to the Bank, already
incorporated through another clause, or caused only by a mandatory-law
mechanism that preserves the Bank's practical right, keep `aligned`.

Functional equivalence cannot override a missing or changed hard term.

See examples: `Formal Label Difference`, `Low-Risk Note Does Not Force Deviation`, `Slash Options`.

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
