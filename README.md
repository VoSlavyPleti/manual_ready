# Single-Agent Acquiring Contract Review

This project runs one reasoning-mode DeepAgents analyst against:

- `inputs/matrix.json` — the Bank standard matrix.
- `inputs/contract.txt` — the counterparty acquiring contract.

The agent uses only the compact skill in:

- `skills/acquiring-single-agent-review/SKILL.md`
- `skills/acquiring-single-agent-review/references/calibration-examples.md`

The final machine-readable artifact is written to:

- `outputs/discrepancy_analysis.json`

## Run

```powershell
.venv\Scripts\python.exe single_agent.py
```

`single_agent.py` runs from the project root. The project now contains only the
single-agent harness and one compact skill; old multi-agent skills, subagent
prompts, validators, and staged working artifacts have been removed.

## Output Semantics

The matrix is the Bank standard. The contract is checked against that standard.

Statuses:

- `aligned`: the contract preserves the Bank-standard legal result.
- `deviation`: a true analogue exists, but a material legal element differs.
- `missing_in_contract`: an applicable matrix requirement is absent.
- `extra_in_contract`: a material contract term has no matrix analogue.
- `out_of_scope` / `not_applicable`: a matrix requirement does not apply to the
  current contract profile.

The comparison is many-to-many: one contract clause can correspond to several
matrix requirements, and several contract clauses can collectively cover one
matrix requirement.
