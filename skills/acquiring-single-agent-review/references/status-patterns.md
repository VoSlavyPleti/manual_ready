# Status Patterns

Use this reference after a true legal analogue or package has been found. The
status answers whether the contract preserves the Bank standard, not whether a
candidate exists.

## Stage Logic

1. Status is group-level: evaluate the focused package of contract ids against
   the focused matrix requirement(s).
2. Use `aligned` when the legal result is preserved.
3. Use `deviation` only when a true analogue exists and a material element is
   changed, weakened, omitted, narrowed, shifted, inverted, or left blank.
4. Re-read source text before deciding hard terms: deadlines, amounts, caps,
   formulas, protected party, trigger, procedure, forum, termination, and
   liability consequences.
5. Do not downgrade for labels, document names, mandatory-law route, inactive
   product options, or beneficial expansions if the legal result is preserved.
6. Do not spread one gap across sibling requirements.

## Calibration Examples

### A Changed Or Missing Hard Term Is Deviation

A true analogue exists, but a material element differs. Read the source text,
not the proposition summary, before deciding.

- Matrix requires confirmation within 3 working days; the contract has the same
  duty but states no period → `deviation` (missing deadline).
- Matrix requires payment within 5 working days; the contract says 7 working
  days with no mandatory-law equivalence → `deviation` (changed deadline).
- Matrix requires proof of lawful personal-data transfer within a period after a
  written request; the contract has the proof/indemnity duty but no period →
  `deviation`. The response period is part of the Bank protection; do not mark
  `aligned` just because the duty exists.

The deadline applies only to that requirement; do not spread it to siblings.

### Forum Or Venue Is A Hard Term

Matrix names a court, arbitration body, venue, or contractual forum; the
contract regulates disputes but sends them elsewhere, to a general statutory
forum, or omits the named forum.

Result: `deviation`. The forum is a material allocation of legal risk; do not
mark `aligned` merely because both clauses are about dispute resolution.

### Liability: Check Protected Party, Direction, Formula, And Cap

Liability is a package. Before `aligned`, verify in the source text who may
demand the penalty, who is protected, the breach direction, the formula or
percentage, fixed amounts, the cap, and any exception.

- A general or statutory liability clause is not automatically enough for a
  specific Bank-protection requirement.
- A true analogue with a changed cap, formula, protected party, or breach
  direction is `deviation`.
- If the matrix sets the amount in one row and the cap/exception in a
  neighboring row for the same breach direction, and the contract has the amount
  but not the cap, the package is `deviation`.
- Never use a customer-breach clause to close a Bank-breach requirement.

### Mandatory-Law / EIS Route That Preserves The Result Is Aligned

The contract implements the Bank-standard legal result through a mandatory
public-procurement, EIS, or statutory route instead of the template wording: an
EIS acceptance document, statutory review period, motivated-refusal mechanism,
and a payment trigger.

Result: `aligned` for the linked payment/acceptance proposition when the route
gives the Bank an enforceable acceptance/payment trigger and refusal mechanism.
Do not downgrade only because the document is not called UPD, the system is EIS,
or the deadline is expressed through statutory timing. Use `deviation` only when
the source changes a material deadline, removes the refusal route, weakens the
payment trigger, or leaves the acceptance event unclear.

Boundary — do not over-read this into "the whole section is covered". Aligning
the shared payment/acceptance trigger does **not** absorb the section's
independent customer rights (separate review, expert involvement, correction,
withholding, unilateral-acceptance, or proof-burden clauses). Those are separate
propositions: keep this link `aligned`, and report each independent right
separately per `missing-and-extra-patterns.md`. A linked aligned trigger and a
neighboring `extra_in_contract` right coexist; neither downgrades the other.

### Formal Difference, Different Channel, Or Beneficial Expansion Is Not Deviation

The same enforceable right or duty exists, but the channel label, document name,
appendix label, or wording differs — or the contract adds a broader instrument,
extra method, or wider protective option for the Bank.

Result: `aligned`, unless the difference weakens a right, changes a hard term,
removes required proof, or makes performance unenforceable. Example: the Bank
keeps an enforceable advertising-approval right but does not repeat the exact
template channel cross-reference → `aligned` if the approval right itself is
intact; `deviation` only if the right is absent or unenforceable.

### Named Appendices Can Satisfy Incorporation

Matrix requires referenced documents/appendices to be integral parts of the
contract; the contract names the operative appendices, technical assignment,
specification, or acceptance documents as contract components.

Result: `aligned` for the incorporation requirement, unless a specific
referenced document needed for enforcement is left outside the contract.

### Inactive Product Option Within One Requirement Does Not Create A Gap

This is about slash-alternatives inside a single matrix requirement (e.g.
Cards/QR/SberPay, electronic/smart terminal, several notice channels), not about
a separate matrix row filtered to an unused product.

Result: `aligned` for the active alternative when the contract covers it, unless
all alternatives are mandatory. (A separate matrix row that is wholly filtered to
an unused product is handled as low-risk `missing_in_contract`, not here — see
`missing-and-extra-patterns.md`.)

### Statutory Succession Exception Is Not An Assignment Gap

Matrix forbids transfer without consent except legal succession/reorganization;
the public-procurement contract allows replacement/succession only as permitted
by law.

Result: `aligned` when the practical restriction is the same and the only
difference is mandatory-law succession wording.

### A Separate Extra Does Not Contaminate Linked Status

A standard clause is matched by a true contract analogue, and the same section
also contains an additional independent customer/procurement right.

Result: keep the linked analogue `aligned` if it preserves the matrix result;
report the independent right separately as `extra_in_contract`. Do not downgrade
the linked status merely because a neighboring extra exists.

### Placeholder Is Deviation

An applicable material field is blank or shown as `___`.

Result: `deviation`, usually low risk. Raise the risk when the blank prevents
identifying a named system, channel, counterparty, amount, term, or enforcement
route.
