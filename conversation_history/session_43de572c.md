## Summarized at 2026-06-26T11:47:07.239201+00:00

Human: Contract-only extra review
AI: I'll start by reading the skill file and understanding the task, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_R9nwkwGpwMlZ84gm0JTg6273', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/'}, 'id': 'call_01_nvXpAifAQ6c5GX86IJTD0473', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-discrepancy-analysis
     3	description: "Use this skill to compare an acquiring Bank standard matrix against a counterparty acquiring contract: build many-to-many legal coverage, identify aligned terms, deviations from the Bank standard, missing applicable matrix requirements, out-of-scope matrix requirements, and material contract-only terms. Trigger on phrases like check this contract against our matrix, what is missing in the counterparty contract, acquiring contract review, compare bank standard with contract, discrepancy analysis, or matrix-to-contract legal gap analysis."
     4	---
     5	
     6	# Acquiring Discrepancy Analysis
     7	
     8	Use this skill to compare a Bank standard acquiring matrix with a counterparty
     9	acquiring contract. The matrix is the Bank standard. The contract is checked
    10	against that standard. The output is a many-to-many legal coverage graph plus a
    11	two-sheet review table generated from the JSON.
    12	
    13	Reference loading:
    14	
    15	- Read `references/matching-rules.md` before substantive matching.
    16	- Read `references/status-rules.md` before group-level status and risk
    17	  classification.
    18	- Read `references/comparison-patterns.md` when a matching or status decision
    19	  is ambiguous. It contains calibration examples for analogue threshold,
    20	  grouped coverage, weak-candidate rejection, hard terms, procurement terms,
    21	  appendix terms, and risk status.
    22	- Read `references/output-contract.md` before writing or validating final
    23	  artifacts. It is the field contract for JSON and XLSX outputs.
    24	
    25	## Quick Start
    26	
    27	1. Preflight `inputs/contract.txt`; stop with a source error artifact if the
    28	   text is not legally usable.
    29	2. Build `clause_index.json` as the complete source map.
    30	3. Build and validate `legal_propositions.json`; do not start matching until
    31	   `working_artifact_validation.json` is valid.
    32	4. Build the contract product profile and close out-of-scope matrix rows only
    33	   in the internal ledger.
    34	5. Read `references/matching-rules.md`; compare both directions: matrix
    35	   requirements to contract package, and material contract terms back to matrix
    36	   analogues.
    37	6. Read `references/status-rules.md`; assign group-level `aligned`,
    38	   `deviation`, `missing_in_contract`, or `extra_in_contract` based on source
    39	   text.
    40	7. Run Final QA, then write one final JSON and the mechanical XLSX export.
    41	
    42	## Purpose
    43	
    44	Find and explain:
    45	
    46	- Bank-standard matrix requirements preserved by the contract;
    47	- true analogues that deviate from the Bank standard;
    48	- applicable matrix requirements absent from the contract;
    49	- legally meaningful contract terms with no matrix analogue.
    50	- matrix requirements that are out of scope for the current contract profile,
    51	  closed in the internal ledger without final risk reporting.
    52	
    53	The review is risk-oriented. Missing a real risk is worse than marking a
    54	borderline issue as `deviation`, but weak thematic matches must not be promoted
    55	into legal links.
    56	
    57	## Inputs And Outputs
    58	
    59	Inputs:
    60	
    61	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    62	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    63	  applicability filters.
    64	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    65	  ids or real document locators visible in this file.
    66	
    67	Final outputs:
    68	
    69	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    70	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    71	
    72	Working artifacts belong under `/outputs/working/`.
    73	
    74	## Source Hierarchy
    75	
    76	Use the source text as the legal authority:
    77	
    78	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    79	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    80	3. Working ledgers as indexes and evidence aids.
    81	
    82	Do not decide status from extracted fields alone. When a status depends on a
    83	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    84	consequence, re-read the source text. Extracted fields are useful for recall,
    85	but source text controls the legal conclusion.
    86	
    87	## Required Artifacts And Contracts
    88	
    89	Create the artifacts in this order. Each later step depends on the earlier
    90	artifact contract. The purpose is to prevent legal facts from being lost
    91	between stages: `clause_index` proves source coverage, `legal_propositions`
    92	preserves legal meaning, and `coverage_ledger` proves final closure.
    93	
    94	### 1. Source Preflight
    95	
    96	Check `inputs/contract.txt` before analysis:
    97	
    98	- real clause numbering is present;
    99	- deep clause numbers are not visibly collapsed or shifted;
   100	- repeated locators have enough context to distinguish source rows;
   101	- text is readable and not corrupted by encoding.
   102	
   103	If the contract text is not usable, stop and write
   104	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
   105	invalid text.
   106	
   107	### 2. Clause Index
   108	
   109	Create `/outputs/working/clause_index.json`.
   110	
   111	It is a source map only. It must include:
   112	
   113	- every matrix `number`;
   114	- every contract clause, operative parent, definition, appendix/table row, and
   115	  unnumbered operative provision;
   116	- source text or source locator for each row;
   117	- context for duplicate printed contract ids.
   118	
   119	Do not use `clause_index` to decide legal status. It only proves source
   120	coverage and valid ids. Never overwrite it with a batch subset.
   121	
   122	### 3. Legal Proposition Ledger
   123	
   124	Create `/outputs/working/legal_propositions.json`.
   125	
   126	This is the mandatory legal evidence ledger. It must contain `matrix` and
   127	`contract` arrays. Every evaluable proposition should include:
   128	
   129	- `id`: matrix number or printed contract locator;
   130	- `source_text`: text used for legal comparison;
   131	- `source_excerpt`: short quote supporting the normalized proposition;
   132	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   133	  `appendix`, `table`, or `technical`;
   134	- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
   135	- `protected_party`, `bound_party`;
   136	- `right_or_obligation`;
   137	- `legal_object`;
   138	- `trigger`;
   139	- `deadline`;
   140	- `amount_formula_cap`;
   141	- `procedure_channel`;
   142	- `liability_remedy`;
   143	- `scope_options`;
   144	- `consequence`;
   145	- `applicability_filters` where available.
   146	
   147	If a legally meaningful row cannot be normalized, mark it
   148	`needs_source_review` and explain the missing element. It is not fully
   149	processed until the source text has been reviewed. Do not proceed to matching
   150	with unresolved source-review rows that could affect status.
   151	
   152	The ledger is an evidence table, not a substitute for the source. Matching may
   153	use it to find candidates. Status must still be confirmed against source text
   154	because legal meaning may depend on context outside a normalized field.
   155	
   156	Run the mechanical check before matching:
   157	
   158	```bash
   159	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/working_artifact_validation.json
   160	```
   161	
   162	This is a stage gate, not a final QA item. Before starting matrix matching,
   163	contract-only review, merge, or status work:
   164	
   165	- `outputs/working/working_artifact_validation.json` must have `"valid": true`;
   166	- `legal_propositions.json` must not contain unresolved
   167	  `needs_source_review` rows;
   168	- every evaluable row must have source text and enough normalized legal fields
   169	  to preserve its legal meaning.
   170	
   171	If the check fails, repair the working artifact that failed and rerun this
   172	validator. Do not defer incomplete legal proposition rows to Final QA.
   173	
   174	The validator checks source-map completeness, matrix id coverage, contract row
   175	coverage, legal proposition row counts, unresolved `needs_source_review`, empty
   176	source text, and weak evaluable rows. `"valid": true` means the working
   177	artifacts are complete enough to begin legal matching; it does not mean the
   178	legal conclusions are correct.
   179	
   180	### 4. Contract Product Profile
   181	
   182	Create `/outputs/working/contract_product_profile.json`.
   183	
   184	Extract from the contract:
   185	
   186	- product and payment channels;
   187	- lot/procurement type;
   188	- terminal/payment-device scope;
   189	- payment methods;
   190	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   191	
   192	Apply matrix filters before status:
   193	
   194	- `common` applies to every contract.
   195	- A filtered matrix item applies only when the profile matches
   196	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   197	- Mandatory applicable missing = high risk.
   198	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   199	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   200	  profile-based reason. Do not put them in final `unmatched_matrix`.
   201	- Optional applicable missing = low or conditional risk.
   202	- Slash-separated alternatives are options unless the matrix says all options
   203	  are mandatory.
   204	- Placeholder or blank in an applicable material term = low-risk `deviation`.
   205	- In `44_fz` public-procurement contracts, expect mandatory-law acceptance,
   206	  payment, reporting, termination, and control clauses. They may be legal
   207	  analogues, low-risk `extra_in_contract`, or internal ledger closures
   208	  depending on legal effect. Their presence is not itself a coverage error.
   209	- Matrix heading rows and non-operative matrix parents close as
   210	  `not_evaluable` in `coverage_ledger.matrix`; they are not final
   211	  `unmatched_matrix` risks.
   212	
   213	## Matching Method
   214	
   215	Read and follow `references/matching-rules.md` before matching. The short rule:
   216	final links require true legal analogues, not broad topic overlap. Perform both
   217	directions:
   218	
   219	- matrix to contract: find the contract package that covers each applicable
   220	  Bank-standard requirement;
   221	- contract to matrix: find matrix analogues for each material contract term or
   222	  classify it as `extra_in_contract`;
   223	- keep weak candidates out of final `links`; use them only as rejected
   224	  candidates or reasoning;
   225	- group ids only when they form one legal package.
   226	
   227	Use `references/comparison-patterns.md` for calibration examples such as weak
   228	candidate rejection, parent/child package retention, mandatory-law extras,
   229	appendix terms, contract-only materiality, and grouped coverage.
   230	
   231	## Status And Risk Method
   232	
   233	Read and follow `references/status-rules.md` before status classification. The
   234	short rule: status is group-level and source-text based.
   235	
   236	- `aligned`: the contract package preserves the matrix legal result.
   237	- `deviation`: a true analogue exists, but a material element is changed,
   238	  narrowed, weakened, omitted, shifted, or blank.
   239	- `missing_in_contract`: no true contract analogue exists for an applicable
   240	  matrix requirement.
   241	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   242	  analogue.
   243	- `not_material`, `out_of_scope`, and `not_applicable` are internal ledger
   244	  closures unless the output contract says otherwise.
   245	
   246	Compare hard terms directly: deadlines, amounts, formulas, caps, penalties,
   247	protected parties, triggers, procedures, liability, remedies, and consequences.
   248	Formal labels and mandatory-law mechanics do not create `deviation` when the
   249	legal result is preserved. An applicable blank or placeholder remains
   250	`deviation`, normally low risk.
   251	
   252	## Final QA
   253	
   254	Before writing final artifacts, perform release checks over already-built
   255	artifacts. Do not use Final QA as the first pass over missing working data.
   256	
   257	Blocking checks; repair before final JSON:
   258	
   259	- verify `clause_index` covers all source ids;
   260	- verify `outputs/working/working_artifact_validation.json` exists and is
   261	  valid; if it is missing or invalid, return to the Legal Proposition Ledger
   262	  stage instead of patching only the final JSON;
   263	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   264	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   265	  `coverage_ledger`;
   266	- verify every applicable evaluable matrix id is linked or in
   267	  `unmatched_matrix`;
   268	- verify out-of-scope / non-applicable matrix ids are not in final
   269	  `unmatched_matrix`;
   270	- verify every material contract id is closed as linked or extra;
   271	- verify `coverage_ledger.contract` closes every contract id from
   272	  `legal_propositions.contract` as `linked`, `extra_in_contract`, or
   273	  `not_material`;
   274	- verify `coverage_ledger` is derived from final `links`,
   275	  `unmatched_matrix`, and `unmatched_contract`;
   276	- verify every final id is visible in source text;
   277	- verify `aligned` has no material discrepancy;
   278	- verify every `deviation` has a named legal gap and evidence;
   279	- verify weak candidates are not in final `links`;
   280	- verify non-material contract rows are absent from final `unmatched_contract`;
   281	- verify summary counts equal final arrays.
   282	
   283	Advisory cleanup; fix when practical, but do not rewrite legal conclusions
   284	without source support:
   285	
   286	- keep quotes concise;
   287	- keep risk explanations specific to the Bank;
   288	- keep XLSX as a mechanical export from JSON;
   289	- keep working files under `/outputs/working/`.
   290	
   291	## Output Discipline
   292	
   293	Read and follow `references/output-contract.md` before writing any final
   294	artifact. Do not duplicate or reinterpret the field contract locally.
   295	
   296	`links` carry group-level legal findings. `atomic_links` are traceability
   297	projections only and must inherit the group relationship. Do not assign
   298	separate final pair-level statuses.
   299	
   300	## Tools And Scripts
   301	
   302	Use helper scripts for mechanical work: source extraction, indexing,
   303	normalization checks, batch completeness, coverage validation, JSON schema
   304	checks, and Excel export. Do not put legal mapping or status decisions into
   305	hardcoded scripts.
   306	
   307	Required scripts live under `skills/acquiring-discrepancy-analysis/scripts/`
   308	and run with the project Python environment. If a script fails because of a
   309	path or environment issue, repair the command/path and rerun it. If a required
   310	validator is genuinely unavailable, do not skip the gate: perform the same
   311	mechanical checks manually, write the expected validation report under
   312	`/outputs/working/`, and state that the fallback was used.
Tool: ['/.agents/', '/.codex/', '/.env', '/.git/', '/.gitignore', '/.venv/', '/ALL_DATA/', '/README.md', '/__pycache__/', '/acquiring-contract-review.skill', '/conversation_history/', '/inputs/', '/large_tool_results/', '/llm.py', '/main.py', '/output/', '/outputs/', '/run_logs/', '/runs/', '/skills/', '/tmp/', '/tools/', '/workspace/']
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'in_progress'}, {'content': 'Read inputs: matrix.json and contract.txt', 'status': 'pending'}, {'content': 'Read existing working artifacts: clause_index.json, legal_propositions.json, coverage_ledger, contract_product_profile.json', 'status': 'pending'}, {'content': 'Identify material contract-only terms (extra_in_contract vs not_material)', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]}, 'id': 'call_00_VQF6aw24LFDCst4himml9420', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'in_progress'}, {'content': 'Read inputs: matrix.json and contract.txt', 'status': 'pending'}, {'content': 'Read existing working artifacts: clause_index.json, legal_propositions.json, coverage_ledger, contract_product_profile.json', 'status': 'pending'}, {'content': 'Identify material contract-only terms (extra_in_contract vs not_material)', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/matching-rules.md', 'limit': 500}, 'id': 'call_00_RqZ4uJXAGbYRfpnw0poy2102', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/status-rules.md', 'limit': 500}, 'id': 'call_01_1x2NUJeERRP2FGWQrO9j5837', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_02_oHr46MkYsY2xJB53gGU22172', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_03_jrQElrP8SIWe73ocBDTg8697', 'type': 'tool_call'}]
Tool:      1	# Matching Rules
     2	
     3	Use these rules when building final `links`, `unmatched_matrix`,
     4	`unmatched_contract`, and closure rows. They are universal calibration rules,
     5	not document-specific answers.
     6	
     7	## True Analogue Threshold
     8	
     9	Create a final link only when the contract proposition is a true legal
    10	analogue of the matrix proposition. Test:
    11	
    12	- same or equivalent protected party;
    13	- same or equivalent bound party;
    14	- same legal object;
    15	- same operative right, duty, prohibition, permission, remedy, or allocation
    16	  of risk;
    17	- same or legally equivalent material trigger, scope, procedure, and
    18	  consequence.
    19	
    20	A broad topic match is not enough. General law, payment, liability,
    21	notification, acceptance, or procurement language can be considered, but it
    22	becomes a final link only if it governs the same legal object and legal effect.
    23	
    24	See examples: `True Analogue`, `Weak Thematic Candidate`, `Generic Product Capability`.
    25	
    26	## Matrix To Contract
    27	
    28	For each applicable evaluable matrix proposition, retrieve the contract
    29	package that covers the Bank-standard requirement.
    30	
    31	Include parent, child, appendix, payment, procedure, liability, and framework
    32	clauses only when they provide material coverage or legally cure a gap. Each
    33	included locator should explain which element it covers: duty, right, trigger,
    34	deadline, amount, procedure, liability, remedy, scope, or consequence.
    35	
    36	If a child clause is selected, check whether its parent carries operative legal
    37	meaning for the same topic. If a parent is selected, check whether children
    38	contain hard terms or exceptions. Do not include non-operative parent headings.
    39	
    40	For payment, acceptance, liability, termination, and document-exchange
    41	requirements, keep the legal package together only when the clauses govern one
    42	legal result. Do not merge sibling requirements just because they share a
    43	section parent.
    44	
    45	For large matrices, preserve thematic continuity during review: complete the
    46	local payment, liability, termination, document-exchange, or product-scope
    47	cluster you are analyzing before switching context. This is a context-retention
    48	rule, not a requirement to create broad domain batches or crosswalk artifacts.
    49	
    50	See examples: `One Matrix Requirement Covered By Several Clauses`, `Parent And Child Package Retention`, `Non-Informative Parent`.
    51	
    52	## Fragment Shape Before Merge
    53	
    54	Every batch fragment should already follow the final output contract. Do not
    55	use `links` as a temporary bucket for missing or unresolved rows.
    56	
    57	- `links[].relationship` can only be `aligned` or `deviation`;
    58	- applicable matrix rows with no true analogue go to `unmatched_matrix`;
    59	- unresolved rows go to a `needs_review` list or are repaired before merge;
    60	- weak candidates stay in `rejected_candidates` or reasoning, not in
    61	  `contract_ids`;
    62	- a fragment with invalid relationships or ids should be repaired before it is
    63	  merged into the final artifact.
    64	
    65	See examples: `Missing Belongs In Unmatched Matrix`, `Weak Thematic Candidate`.
    66	
    67	## Contract To Matrix
    68	
    69	For each evaluable contract proposition, find the matrix analogue group. If no
    70	true analogue exists and the proposition has independent legal effect, classify
    71	it as `extra_in_contract`.
    72	
    73	Do not classify a contract term as `not_material` merely because no final
    74	finding was produced. `not_material` is reserved for headings, definitions
    75	without legal effect, requisites, signatures, blank forms, and purely
    76	technical rows.
    77	
    78	The contract-side review is complete only when every contract proposition from
    79	`legal_propositions.contract` is closed as `linked`, `extra_in_contract`, or
    80	`not_material` in `coverage_ledger.contract`. A material contract row cannot be
    81	left unclassified because the matrix-side pass already produced enough links.
    82	If it has a true matrix analogue, link it. If it has independent legal effect
    83	and no true analogue, report `extra_in_contract`. If it is only a heading,
    84	duplicate, blank form, or non-operative definition, close it as `not_material`.
    85	
    86	See examples: `Contract-Only Material Clause`, `Definition Without Legal Effect`, `Definition With Legal Effect`, `Contract-Only Pass Cannot Be Empty`.
    87	
    88	## Matrix Headings And Non-Operative Parents
    89	
    90	Matrix rows that only name a section, subsection, theme, or parent category
    91	close as `not_evaluable` in `coverage_ledger.matrix`. They never appear in
    92	final `unmatched_matrix`.
    93	
    94	If a matrix parent row contains its own right, duty, procedure, limitation,
    95	definition with legal effect, or consequence, treat it as evaluable. Otherwise
    96	use it only as context for children.
    97	
    98	See examples: `Matrix Heading Row`, `Non-Informative Parent`.
    99	
   100	## Appendix And Schedule Terms
   101	
   102	Appendix, schedule, specification, table, tariff, technical assignment, or
   103	payment-detail rows can be final contract locators when they contain an
   104	operative legal term: deadline, amount, currency, payment method, procedure,
   105	scope, product, acceptance condition, liability, remedy, or consequence.
   106	
   107	Index those rows in `clause_index` and `legal_propositions.contract` with real
   108	source locators visible in the contract text. Do not invent semantic ids. If an
   109	operative detail has no printed sub-id, use the nearest printed source locator
   110	as `contract_id` and describe the exact detail in `contract_evidence`,
   111	`coverage`, or `source_evidence`. Do not create synthetic locators with
   112	semantic suffixes, translated names, or helper-script ids.
   113	
   114	If an appendix title only marks the beginning of a document part, keep it
   115	`evidence_only` / `not_material`; do not use it as a final `contract_id`.
   116	
   117	See examples: `Appendix Operative Term`, `Canonical Locator For Unnumbered Appendix Detail`, `Formal Label Difference`.
   118	
   119	## 44-FZ And Mandatory-Law Clauses
   120	
   121	Public-procurement clauses are not automatically extra and not automatically
   122	deviation:
   123	
   124	- if they regulate the same legal object as the matrix, link them and evaluate
   125	  `aligned` or `deviation`;
   126	- if they are mandatory-law mechanics with no matrix analogue and no adverse
   127	  Bank-specific risk, classify as low-risk `extra_in_contract` when they have
   128	  independent legal effect;
   129	- if they are headings or procedural scaffolding without independent legal
   130	  effect, keep them out of final `unmatched_contract`.
   131	
   132	See examples: `Procurement Mechanism As Analogue`, `Mandatory-Law Extra`.
   133	
   134	## Structural Duplicates
   135	
   136	If two contract clauses regulate the same legal object, same parties, same
   137	right or duty, same trigger, and same consequence, treat the later clause as a
   138	structural duplicate. It can inherit closure from the primary clause or close
   139	as `not_material` in `coverage_ledger.contract` with a reference to the
   140	primary clause. Do not create a new group or search for a different matrix id
   141	only to make the duplicate unique.
   142	
   143	See example: `Structural Duplicate Contract Clause`.
   144	
   145	## Grouping Discipline
   146	
   147	Group ids only for an indivisible legal package. Sibling matrix ids with
   148	different legal objects, channels, grounds, duties, or consequences should
   149	remain separate links even if they share a parent section.
   150	
   151	One matrix id may need several contract clauses. One contract clause may cover
   152	several matrix ids. The group must still describe one legal result.
   153	
   154	Payment and procedure clauses often sit near each other but remain separate
   155	legal results: payment amount, payment trigger, acceptance document, acceptance
   156	deadline, payment deadline, service fee, and evidence channel should not be
   157	merged into one broad group unless the matrix item itself requires the whole
   158	package. A gap in one payment or procedure element does not downgrade sibling
   159	links that preserve their own legal result.
   160	
   161	See examples: `Group-Level Status`, `Duplicate Gap Propagation`, `One Child Deviation Does Not Spread To Siblings`, `Payment Procedure Siblings Keep Separate Status`.
Tool:      1	# Status And Risk Rules
     2	
     3	Use these rules after true legal links are built. They calibrate the group-level
     4	status and risk level. They do not relax the analogue threshold.
     5	
     6	## Group-Level Status
     7	
     8	Assign status to the group, not to each atomic pair.
     9	
    10	- `aligned`: the contract package preserves the matrix legal result.
    11	- `deviation`: a true analogue exists, but a material element is changed,
    12	  narrowed, weakened, omitted, shifted, or blank.
    13	- `missing_in_contract`: no true contract analogue exists for an applicable
    14	  matrix requirement.
    15	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
    16	  analogue.
    17	- `not_material`, `out_of_scope`, and `not_applicable` are internal ledger
    18	  closures unless the output contract says otherwise.
    19	
    20	`atomic_links` are traceability rows only and inherit the group relationship.
    21	
    22	## Hard Terms
    23	
    24	Compare hard terms directly:
    25	
    26	- same material deadline, amount, formula, cap, penalty, protected party,
    27	  trigger, procedure, liability, remedy, or consequence can be `aligned`;
    28	- changed or missing value is `deviation`;
    29	- a hard term from another clause counts only when that clause expressly
    30	  governs the same obligation or is explicitly incorporated;
    31	- a neighboring date, amount, or procedure for another legal object cannot
    32	  cure the gap.
    33	
    34	An applicable blank or placeholder remains `deviation`, normally low risk. Do
    35	not create an exception for administrative-looking placeholders when the field
    36	is part of an applicable matrix or contract requirement.
    37	
    38	For document, evidence, reporting, confirmation, chargeback, request-response,
    39	and transaction-information duties, the response or performance deadline is a
    40	hard term. Before marking such a group `aligned`, re-read the source text for
    41	the exact period and trigger. If the analogue has the same duty but omits,
    42	changes, or moves the deadline to another unincorporated procedure, use
    43	`deviation`.
    44	
    45	See examples: `Changed Or Missing Deadline`, `Borrowed Hard Term Does Not Cure Gap`, `Placeholder In Applicable Term`, `Document Or Evidence Deadline Is A Hard Term`.
    46	
    47	## Functional Equivalence
    48	
    49	Do not downgrade for formal differences alone: heading, title, appendix label,
    50	permitted option selection, equivalent mandatory-law mechanism, or wording
    51	style.
    52	
    53	Do not downgrade for low-risk notes when the legal result is preserved. If the
    54	difference is merely terminological, beneficial to the Bank, already
    55	incorporated through another clause, or caused only by a mandatory-law
    56	mechanism that preserves the Bank's practical right, keep `aligned`.
    57	
    58	Functional equivalence cannot override a missing or changed hard term.
    59	
    60	See examples: `Formal Label Difference`, `Low-Risk Note Does Not Force Deviation`, `Slash Options`.
    61	
    62	## 44-FZ And Mandatory-Law Calibration
    63	
    64	Mandatory 44-FZ/GK/EIS mechanics are not deviations by themselves. Evaluate
    65	their legal effect:
    66	
    67	- if the mandatory-law mechanism preserves the Bank-standard legal result,
    68	  keep `aligned`;
    69	- if it changes payment timing, acceptance control, withholding right,
    70	  penalty/cap, termination power, protected party, evidence channel, or
    71	  enforceability, use `deviation`;
    72	- if a mandatory-law clause exists only because public procurement requires it
    73	  and has no matrix analogue, use low-risk `extra_in_contract` when the clause
    74	  has independent legal effect;
    75	- if it is only a heading, formality, or procedural scaffold, close it as
    76	  `not_material` in the ledger.
    77	
    78	See examples: `Procurement Mechanism As Analogue`, `Procurement Mechanism With Material Deviation`, `Mandatory-Law Extra`.
    79	
    80	## Bank Right Displaced By Mandatory Law
    81	
    82	When the matrix gives the Bank a unilateral right but the contract omits or
    83	restricts it because mandatory procurement law limits that unilateral power,
    84	do not treat the issue as harmless. The matrix requirement remains absent or
    85	weakened.
    86	
    87	Use `missing_in_contract` when no true contract analogue exists. Use
    88	`deviation` when the contract contains a narrower substitute. Risk is normally
    89	`medium` when statutory mechanisms partially compensate the Bank, and `high`
    90	when the omitted right is central and no practical substitute exists.
    91	
    92	See example: `Bank Right Displaced By Mandatory Law`.
    93	
    94	## Liability Package
    95	
    96	Before marking a liability group `aligned`, check amount, formula, cap,
    97	trigger, protected party, excluded delay/non-delay buckets, claim procedure,
    98	damages, and remedy survival across the package.
    99	
   100	General fault-based liability does not close a special Bank exemption, special
   101	penalty, or special cap rule unless it preserves the same protected party and
   102	legal consequence.
   103	
   104	See examples: `Liability Group Review`, `Changed Amount, Formula, Cap, Or Penalty`.
   105	
   106	## Risk Level
   107	
   108	Use `risk_level` consistently:
   109	
   110	- `none`: only for `aligned`;
   111	- `low`: optional applicable missing, applicable placeholder, formal but
   112	  legally manageable gap, or mandatory-law extra with no adverse Bank-specific
   113	  effect;
   114	- `medium`: material deviation that can affect performance, evidence, payment,
   115	  control, liability, enforceability, or a Bank right displaced by mandatory
   116	  law with partial statutory compensation;
   117	- `high`: mandatory applicable missing, changed protected party, major
   118	  payment/remedy change, important Bank right omitted without substitute, or
   119	  broad contract-only risk.
   120	
   121	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   122	a short evidence-based reason. Use concise quotes rather than long excerpts.
Tool:      1	# Comparison Patterns
     2	
     3	These are universal calibration patterns. They are not answers for a specific
     4	document.
     5	
     6	## 1. Good Legal Proposition Ledger Row
     7	
     8	Source clause gives the Bank a right to refuse service registration without
     9	explaining reasons.
    10	
    11	Good ledger row:
    12	
    13	- `source_text` preserves the clause text;
    14	- `source_excerpt` quotes the refusal right;
    15	- `protected_party = Bank`;
    16	- `bound_party = merchant/counterparty`;
    17	- `right_or_obligation = Bank refusal right`;
    18	- `legal_object = service/outlet registration`;
    19	- `consequence = registration may be refused`.
    20	
    21	Result: evaluable. It can participate in matching and status analysis.
    22	
    23	## 2. Bad Ledger Row
    24	
    25	Source clause contains a payment deadline, but the ledger says only
    26	`payment terms`.
    27	
    28	Result: incomplete. Mark `needs_source_review` or repair the ledger before
    29	status. A missing extracted deadline must not make the final analysis forget
    30	the deadline in source text.
    31	
    32	## 3. True Analogue
    33	
    34	Matrix gives the Bank a specific right to deduct a fee after a defined trigger.
    35	Contract gives the same party the same deduction right for the same trigger and
    36	object.
    37	
    38	Result: link the provisions and compare details for `aligned` or `deviation`.
    39	
    40	## 4. Weak Thematic Candidate
    41	
    42	Matrix gives the Bank a specific deduction right. Contract has only a general
    43	payment clause.
    44	
    45	Result: no final link. Record the payment clause as rejected weak context if it
    46	was considered.
    47	
    48	## 5. One Matrix Requirement Covered By Several Clauses
    49	
    50	Matrix requires a duty, a deadline, a procedure, and a consequence. Contract
    51	splits those elements across parent, operative, procedure, and liability
    52	clauses that all govern the same obligation.
    53	
    54	Result: one group link with several `contract_ids`. `aligned` is allowed if the
    55	package preserves all material elements.
    56	
    57	## 6. One Contract Clause Covers Several Matrix Requirements
    58	
    59	One contract clause contains duties for payment, documents, acceptance, and
    60	liability. Several matrix requirements describe those elements separately.
    61	
    62	Result: one group can contain one contract id and several matrix ids when the
    63	legal object and effect are genuinely shared.
    64	
    65	## 7. Mandatory Missing
    66	
    67	Matrix item is mandatory and applicable to the contract profile. No true
    68	contract analogue exists.
    69	
    70	Result: `missing_in_contract` with high risk.
    71	
    72	## 8. Out Of Scope Matrix Requirement
    73	
    74	Matrix item is filtered to a product, lot, terminal, payment method, or legal
    75	regime not used by the contract.
    76	
    77	Result: close it in `coverage_ledger.matrix` as `out_of_scope` or
    78	`not_applicable` with the profile reason. Do not put it in final
    79	`unmatched_matrix`, and do not force a weak link.
    80	
    81	## 9. Optional Applicable Missing
    82	
    83	Matrix item is optional but applicable to the selected product/profile. No true
    84	contract analogue exists.
    85	
    86	Result: `missing_in_contract` with low or conditional risk.
    87	
    88	## 10. Slash Options
    89	
    90	Matrix lists `cards / QR / mobile pay / smart terminal` as alternatives.
    91	Contract selects `cards / QR`, and the profile confirms only those services are
    92	in scope.
    93	
    94	Result: `aligned` for scope. Absence of unselected alternatives is not a
    95	deviation.
    96	
    97	## 11. Placeholder In Applicable Term
    98	
    99	Matrix or contract requires a filled penalty, fee, account, deadline, appendix,
   100	or system name. The applicable field is blank.
   101	
   102	Result: `deviation`, low risk in most cases. Raise to medium when the blank
   103	prevents identification of a named system, channel, counterparty, account,
   104	amount, deadline, or procedure needed for enforcement or performance.
   105	
   106	## 12. Same Deadline
   107	
   108	Matrix requires a document within 3 business days. Contract imposes the same
   109	3-business-day deadline on the same duty.
   110	
   111	Result: deadline element is covered.
   112	
   113	## 13. Changed Or Missing Deadline
   114	
   115	Matrix requires 3 business days. Contract says 5 business days, uses another
   116	period, or states the duty without a deadline.
   117	
   118	Result: `deviation`; discrepancy type `deadline`.
   119	
   120	## 14. Borrowed Hard Term Does Not Cure Gap
   121	
   122	Contract clause A covers the same duty but lacks the matrix deadline. Clause B
   123	has the same number of days but governs a different request or procedure and is
   124	not incorporated into clause A.
   125	
   126	Result: clause B cannot make clause A aligned. Record a deadline deviation.
   127	
   128	## 15. Changed Amount, Formula, Cap, Or Penalty
   129	
   130	Matrix requires a fixed penalty, no cap, full damages, or a specific formula.
   131	Contract lowers the amount, adds a cap, changes the base, or requires an extra
   132	demand.
   133	
   134	Result: `deviation`; discrepancy type `amount` or `liability`.
   135	
   136	## 16. Party Inversion
   137	
   138	Matrix protects the Bank or imposes a duty on the counterparty. Contract gives
   139	the analogous right to the customer or shifts the burden to the Bank.
   140	
   141	Result: `deviation` if it is an analogue; `extra_in_contract` if it creates a
   142	new independent right.
   143	
   144	## 17. Procurement Mechanism As Analogue
   145	
   146	Public-contract acceptance, EIS signing, budget payment, statutory penalties,
   147	or unilateral termination regulates the same legal object as the matrix.
   148	
   149	Result: link it. Use `aligned` if the Bank standard is preserved or stronger.
   150	Do not mark `deviation` merely because the mechanism is 44-FZ/EIS.
   151	
   152	## 18. Procurement Mechanism With Material Deviation
   153	
   154	Public-contract mechanics regulate the same legal object, but the contract
   155	changes a material element: longer payment deadline, weaker withholding right,
   156	different acceptance consequence, penalty cap, lost termination power, or
   157	changed protected party.
   158	
   159	Result: grouped `deviation` with the specific changed element.
   160	
   161	## 19. Procurement Mechanism As Extra
   162	
   163	Contract gives the customer an independent inspection, rejection, correction,
   164	withholding, reporting, or convenience termination right with no matrix
   165	analogue.
   166	
   167	Result: `extra_in_contract` with materiality reason and risk.
   168	
   169	## 20. Formal Label Difference
   170	
   171	The same legal content appears under another appendix title, report label, or
   172	document name.
   173	
   174	Result: `aligned` if rights, duties, timing, evidence, and consequences are
   175	preserved.
   176	
   177	## 21. Low-Risk Note Does Not Force Deviation
   178	
   179	The contract uses another label for the same channel, another party label for
   180	the same legal role, or adds language beneficial to the Bank. The legal result,
   181	timing, enforceability, and protected party are preserved.
   182	
   183	Result: `aligned`. The note can appear in `status_reason`, but it is not a
   184	discrepancy.
   185	
   186	## 22. Named Channel Or Legal Force Missing
   187	
   188	Matrix requires a named EDI/email/site/channel or legal-force effect. Contract
   189	has a generic document exchange clause and omits the named element.
   190	
   191	Result: `deviation` when it is the same exchange mechanism with a missing
   192	material element. If it is only broad-topic context, use `missing_in_contract`.
   193	
   194	## 23. Generic Product Capability
   195	
   196	Contract says a terminal can display QR or accept cards. Matrix requires a
   197	named Bank product or product-specific procedure.
   198	
   199	Result: apply the product profile first. Generic capability is not enough for a
   200	named product obligation.
   201	
   202	## 24. Parent And Child Package Retention
   203	
   204	Parent clause states the operative right or duty. Child clauses enumerate
   205	events, exceptions, deadlines, or remedies. Either parent or child alone would
   206	be incomplete.
   207	
   208	Result: final group includes the material parent and children. Do not drop the
   209	parent only because children contain more detail, and do not drop children when
   210	they carry the hard term.
   211	
   212	## 25. Framework Clause As Analogue
   213	
   214	Contract clause requires compliance with applicable law, payment-system rules,
   215	contract specifications, or incorporated operating procedures. A matrix row
   216	uses that same framework as the legal object or risk-allocation rule.
   217	
   218	Result: include the framework clause as a legal analogue. Do not use it to
   219	inflate unrelated rows where it is only background context.
   220	
   221	## 26. Liability Group Review
   222	
   223	Matrix separates delay penalties, non-delay fines, caps, exceptions, claim
   224	procedure, and damages. Contract distributes the same topics across several
   225	clauses.
   226	
   227	Result: compare the liability package as a group. Before `aligned`, verify
   228	amounts, formulas, caps, triggers, protected party, and excluded buckets.
   229	
   230	## 27. Definition Without Legal Effect
   231	
   232	Definition has no analogue in the matrix and creates no standalone right, duty,
   233	risk, amount, procedure, liability, or consequence.
   234	
   235	Result: `not_material` in the working ledger only.
   236	
   237	## 28. Definition With Legal Effect
   238	
   239	Definition expands a key term so that it changes scope, liability, covered
   240	transactions, parties, or remedies.
   241	
   242	Result: evaluable. Link it if it modifies a matrix analogue; otherwise classify
   243	as `extra_in_contract`.
   244	
   245	## 29. Contract-Only Material Clause
   246	
   247	Contract adds maximum price, budget source, customer control, acceptance,
   248	withholding, unilateral refusal, penalty cap, reporting, anti-corruption,
   249	confidentiality, audit, data, or evidence procedure with no matrix analogue.
   250	
   251	Result: `extra_in_contract`.
   252	
   253	## 30. Duplicate Gap Propagation
   254	
   255	One payment deadline gap affects a payment package with parent and child
   256	clauses.
   257	
   258	Result: record one grouped `deviation`. Do not duplicate the same gap across
   259	unrelated companion clauses.
   260	
   261	## 31. Non-Informative Parent
   262	
   263	A parent row merely names a section and all legal effect is in children.
   264	
   265	Result: close as non-evaluable or `not_material` in the ledger. Do not report
   266	it as a final risk.
   267	
   268	## 32. Group-Level Status
   269	
   270	A group contains several matrix ids and several contract ids. One status
   271	applies to the group as a whole.
   272	
   273	Result: do not assign separate final statuses per pair. `atomic_links` are only
   274	traceability rows and inherit the group relationship.
   275	
   276	## 33. Mandatory-Law Extra
   277	
   278	Contract clause exists because mandatory procurement law requires a public
   279	contract procedure: acceptance in an official system, statutory reporting,
   280	customer-side control, statutory payment mechanics, or mandatory termination
   281	procedure. The matrix has no true analogue because the Bank standard does not
   282	regulate that public-law mechanism.
   283	
   284	Result: if the clause has independent legal effect, classify it as
   285	`extra_in_contract` with low risk and explain that it is mandatory-law
   286	specific. If it is only a heading or formality, close it as `not_material` in
   287	the ledger.
   288	
   289	## 34. Structural Duplicate Contract Clause
   290	
   291	Two contract clauses regulate the same legal object, the same parties, the same
   292	right or duty, the same trigger, and the same consequence. The second clause
   293	does not add a new amount, deadline, scope, exception, remedy, or procedure.
   294	
   295	Result: use the primary clause for the legal link. Close the duplicate in the
   296	ledger as `not_material` or duplicate-of-primary with a short reason. Do not
   297	invent a different matrix analogue just to make the duplicate distinct.
   298	
   299	## 35. Matrix Heading Row
   300	
   301	Matrix row only names a section, subsection, product block, responsibility
   302	block, payment block, or document-exchange block. It contains no independent
   303	right, duty, procedure, limit, remedy, or consequence beyond child rows.
   304	
   305	Result: close as `not_evaluable` in `coverage_ledger.matrix`. Do not include it
   306	in final `unmatched_matrix`.
   307	
   308	## 36. Appendix Operative Term
   309	
   310	Appendix, specification, tariff table, technical assignment, or schedule row
   311	contains an operative legal term: currency, fee, term, deadline, product scope,
   312	payment method, acceptance condition, service scope, or liability consequence.
   313	
   314	Result: index it as an evaluable contract row with a real source locator and
   315	use it as a final `contract_id` if it covers a matrix element. Appendix
   316	headings without operative content remain evidence/context only.
   317	
   318	## 37. Bank Right Displaced By Mandatory Law
   319	
   320	Matrix gives the Bank a unilateral right such as refusal, suspension,
   321	withholding, termination, verification, or operational control. The public
   322	contract omits or narrows that right because mandatory law restricts
   323	unilateral powers of the contractor or reallocates the mechanism through
   324	statutory procedures.
   325	
   326	Result: use `missing_in_contract` if no true analogue exists, or `deviation` if
   327	a narrower statutory substitute exists. Risk is usually medium when statutory
   328	mechanisms partly compensate the Bank, and high when the omitted Bank right has
   329	no practical substitute.
   330	
   331	## 38. One Child Deviation Does Not Spread To Siblings
   332	
   333	Root clause states a general operative rule. Child clauses enumerate separate
   334	channels, grounds, products, duties, exceptions, or consequences. One child has
   335	a gap, but neighboring children preserve their own legal result.
   336	
   337	Result: include the root with the relevant child when it is needed for context,
   338	but keep separate child-level legal results separate. Do not downgrade all
   339	siblings because one sibling has a deviation.
   340	
   341	## 39. Missing Belongs In Unmatched Matrix
   342	
   343	Matrix requirement is applicable and evaluable. The contract has only weak
   344	topic candidates, not a true analogue.
   345	
   346	Result: do not create a `link` with `relationship = missing_in_contract`.
   347	Record the requirement in `unmatched_matrix` and include the weak candidates
   348	only as rejected candidates with reasons.
   349	
   350	## 40. Canonical Locator For Unnumbered Appendix Detail
   351	
   352	An appendix table contains an operative fee, currency, product, or payment
   353	method, but the specific row has no printed sub-number. The nearest printed
   354	source locator is the appendix or table item that contains the row.
   355	
   356	Result: use the nearest printed locator as `contract_id`. Put the exact row
   357	detail in `contract_evidence` or `coverage`. Do not invent ids such as
   358	`appendix_fee_row`, translated labels, or semantic suffixes.
   359	
   360	## 41. Payment Procedure Siblings Keep Separate Status
   361	
   362	One contract payment section contains an acceptance document, a payment
   363	trigger, a payment deadline, a currency rule, and a service-fee rule. Matrix
   364	requirements split these into separate rows.
   365	
   366	Result: link each legal result separately unless the matrix row itself
   367	requires the whole payment package. A deadline gap in one payment row should
   368	not make the acceptance-document row or currency row `deviation`.
   369	
   370	## 42. Contract-Only Pass Cannot Be Empty
   371	
   372	After matrix matching, several material contract clauses remain: customer
   373	inspection, rejection, withholding, unilateral refusal, statutory reporting, or
   374	mandatory-law control. They do not have true matrix analogues.
   375	
   376	Result: final `unmatched_contract` cannot be empty merely because matrix-side
   377	coverage was completed. Report material rows as `extra_in_contract`; close only
   378	headings, signatures, requisites, blank forms, duplicates, or non-operative
   379	definitions as `not_material`.
   380	
   381	## 43. Document Or Evidence Deadline Is A Hard Term
   382	
   383	Matrix requires a party to provide transaction documents, confirmations,
   384	responses, reports, or evidence within a specified period. Contract contains
   385	the same duty but omits the period, changes it, or gives a period for another
   386	unincorporated procedure.
   387	
   388	Result: true analogue exists, but status is `deviation` with a deadline gap.
Tool:      1	# Output Contract
     2	
     3	Write two final artifacts:
     4	
     5	- `/outputs/discrepancy_analysis.json`
     6	- `/outputs/discrepancy_analysis.xlsx`
     7	
     8	The JSON is the source of truth. The XLSX is a mechanical presentation export.
     9	
    10	## Working Artifact Contract
    11	
    12	Before final comparison, create:
    13	
    14	- `/outputs/working/clause_index.json`
    15	- `/outputs/working/legal_propositions.json`
    16	- `/outputs/working/contract_product_profile.json`
    17	- `/outputs/working/coverage_ledger.json`
    18	
    19	`clause_index.json` is a source map. It contains source ids and text, but no
    20	final legal status.
    21	
    22	`legal_propositions.json` is the legal evidence ledger. It must contain:
    23	
    24	```json
    25	{
    26	  "matrix": [
    27	    {
    28	      "id": "<matrix number>",
    29	      "source_text": "<matrix enriched/source text>",
    30	      "source_excerpt": "<short quote>",
    31	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    32	      "materiality": "evaluable|not_material|heading|needs_source_review",
    33	      "protected_party": "<party protected by the rule>",
    34	      "bound_party": "<party bound by the rule>",
    35	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    36	      "legal_object": "<regulated object>",
    37	      "trigger": "<event/condition>",
    38	      "deadline": "<deadline if any>",
    39	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    40	      "procedure_channel": "<procedure/channel if any>",
    41	      "liability_remedy": "<liability/remedy if any>",
    42	      "scope_options": ["<scope option>"],
    43	      "consequence": "<legal consequence>",
    44	      "applicability_filters": {}
    45	    }
    46	  ],
    47	  "contract": [
    48	    {
    49	      "id": "<printed contract locator>",
    50	      "source_text": "<contract clause text>",
    51	      "source_excerpt": "<short quote>",
    52	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    53	      "materiality": "evaluable|not_material|heading|needs_source_review",
    54	      "protected_party": "<party protected by the rule>",
    55	      "bound_party": "<party bound by the rule>",
    56	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    57	      "legal_object": "<regulated object>",
    58	      "trigger": "<event/condition>",
    59	      "deadline": "<deadline if any>",
    60	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    61	      "procedure_channel": "<procedure/channel if any>",
    62	      "liability_remedy": "<liability/remedy if any>",
    63	      "scope_options": ["<scope option>"],
    64	      "consequence": "<legal consequence>"
    65	    }
    66	  ]
    67	}
    68	```
    69	
    70	Rows marked `needs_source_review` are not complete. Resolve them before
    71	substantive matching if they can affect a link, missing item, or contract-only
    72	finding.
    73	
    74	After creating or repairing `legal_propositions.json`, run
    75	`validate_working_artifacts.py` and write
    76	`/outputs/working/working_artifact_validation.json`. The validation report must
    77	be valid before substantive matching begins. If it is invalid, repair the
    78	working artifact first; do not wait until final JSON QA to discover incomplete
    79	legal proposition rows.
    80	
    81	## Final JSON Shape
    82	
    83	```json
    84	{
    85	  "analysis_profile": {
    86	    "contract_product_profile": {
    87	      "product": ["<selected product/channel>"],
    88	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
    89	      "terminal": ["<selected terminal/payment device>"],
    90	      "payment_method": ["<selected payment method>"],
    91	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
    92	    },
    93	    "source_preflight": {
    94	      "contract_numbering_valid": true,
    95	      "notes": []
    96	    }
    97	  },
    98	  "links": [
    99	    {
   100	      "matrix_ids": ["<matrix id>"],
   101	      "contract_ids": ["<contract locator>"],
   102	      "relationship": "aligned|deviation",
   103	      "legal_topic": "<short legal topic>",
   104	      "matrix_standard": "<bank standard requirement group>",
   105	      "contract_position": "<counterparty contract position group>",
   106	      "matrix_evidence": "<short matrix quote>",
   107	      "contract_evidence": "<short contract quote>",
   108	      "status_reason": "<group-level reason>",
   109	      "risk_level": "none|low|medium|high",
   110	      "discrepancies": [
   111	        {
   112	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   113	          "description": "<material difference>",
   114	          "risk": "<why this matters for the Bank>"
   115	        }
   116	      ]
   117	    }
   118	  ],
   119	  "atomic_links": [
   120	    {
   121	      "matrix_id": "<one matrix id>",
   122	      "contract_id": "<one contract locator>",
   123	      "relationship": "aligned|deviation",
   124	      "link_index": 0,
   125	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   126	      "coverage": "<what this contract locator contributes to the group>"
   127	    }
   128	  ],
   129	  "unmatched_matrix": [
   130	    {
   131	      "matrix_id": "<matrix id>",
   132	      "requirement": "<missing bank standard requirement>",
   133	      "source_evidence": "<short matrix quote>",
   134	      "status": "missing_in_contract",
   135	      "required_type": "mandatory|optional|unknown",
   136	      "applicability": "applicable|conditional|unknown",
   137	      "risk_level": "low|medium|high",
   138	      "risk": "<risk of omission>",
   139	      "rejected_candidates": [
   140	        {
   141	          "contract_id": "<weak candidate considered>",
   142	          "reason": "<why it is not a true analogue>"
   143	        }
   144	      ]
   145	    }
   146	  ],
   147	  "unmatched_contract": [
   148	    {
   149	      "contract_id": "<contract locator>",
   150	      "contract_position": "<extra legally significant contract term>",
   151	      "source_evidence": "<short contract quote>",
   152	      "status": "extra_in_contract",
   153	      "risk_level": "low|medium|high",
   154	      "risk": "<risk or impact for the Bank>",
   155	      "materiality_reason": "<why this has independent legal effect>"
   156	    }
   157	  ],
   158	  "coverage_ledger": {
   159	    "matrix": [
   160	      {
   161	        "matrix_id": "<matrix id>",
   162	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
   163	        "link_indices": [0],
   164	        "reason": "<short closure reason>"
   165	      }
   166	    ],
   167	    "contract": [
   168	      {
   169	        "contract_id": "<contract locator>",
   170	        "closure": "linked|extra_in_contract|not_material",
   171	        "link_indices": [0],
   172	        "reason": "<short closure reason>"
   173	      }
   174	    ]
   175	  },
   176	  "summary": {
   177	    "aligned_count": 0,
   178	    "deviation_count": 0,
   179	    "missing_in_contract_count": 0,
   180	    "extra_in_contract_count": 0
   181	  }
   182	}
   183	```
   184	
   185	## JSON Rules
   186	
   187	- `links` are group-level legal findings. One status applies to the whole
   188	  many-to-many group.
   189	- Intermediate batch fragments should use the same relationship values as the
   190	  final artifact. Do not put `missing_in_contract`, `extra_in_contract`,
   191	  `not_material`, unresolved rows, or candidate-only rows inside `links`.
   192	- `atomic_links` are traceability rows only. They inherit the group
   193	  `relationship`; do not invent pair-level final statuses.
   194	- `contract_ids` contain clauses that provide material coverage for the group.
   195	  Background clauses can be cited in reasoning, but should not become final
   196	  candidates unless they affect coverage or status.
   197	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   198	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   199	  matrix closures. Do not use it to invent final conclusions.
   200	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   201	  not a risk for the current product, lot, terminal, payment method, or legal
   202	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   203	  final `unmatched_matrix`.
   204	- `not_evaluable` matrix closures mean the row is a heading, non-operative
   205	  parent, or source row without an independent legal proposition. They stay in
   206	  `coverage_ledger.matrix` only and do not appear in final `unmatched_matrix`.
   207	- `unmatched_contract` contains only legally significant `extra_in_contract`
   208	  rows. Non-material rows stay in `coverage_ledger.contract`.
   209	- `coverage_ledger.contract` must close every contract row from
   210	  `legal_propositions.contract`: `linked` when it appears in a final link,
   211	  `extra_in_contract` when it has independent legal effect and no matrix
   212	  analogue, or `not_material` when it is a heading, duplicate, blank form,
   213	  signature/requisites row, or non-operative definition. Do not leave material
   214	  contract rows out of the ledger.
   215	- `relationship = aligned` requires empty `discrepancies`, `risk_level = none`,
   216	  and text-grounded confirmation that the contract package preserves the matrix
   217	  legal result.
   218	- `relationship = deviation` requires at least one discrepancy with `type`,
   219	  `description`, and `risk`.
   220	- Missing mandatory applicable requirements should normally be `high` risk.
   221	  Missing optional applicable requirements should normally be `low` or
   222	  conditional risk.
   223	- Mandatory-law public-procurement extras with independent legal effect can be
   224	  `low` risk when they do not materially worsen the Bank position. They still
   225	  require a non-empty `risk` and `materiality_reason`.
   226	- All final ids must be visible in source files. Do not use corrected,
   227	  inferred, translated, parenthetical, or internal ids.
   228	- If an appendix, table, or technical assignment detail has no printed
   229	  sub-locator, use the nearest printed locator visible in the source as the
   230	  final `contract_id` and cite the detail in evidence fields. Do not create
   231	  synthetic ids such as semantic suffixes, translated labels, helper-script
   232	  names, or pseudo-paragraph locators.
   233	- Weak candidates do not appear in final `links`; use
   234	  `unmatched_matrix[].rejected_candidates`.
   235	
   236	## Excel Output
   237	
   238	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   239	
   240	Sheet 1: `Contract-Matrix`
   241	
   242	Columns:
   243	
   244	1. `contract_id`
   245	2. `contract_summary`
   246	3. `matrix_ids`
   247	4. `status`
   248	5. `risk_level`
   249	6. `comment`
   250	
   251	Rules:
   252	
   253	- one row per group-level contract-to-matrix finding;
   254	- `matrix_ids` contains the full matrix id set for the group;
   255	- status is `aligned`, `deviation`, or `extra_in_contract`;
   256	- contract-only extras have blank `matrix_ids`.
   257	
   258	Sheet 2: `Only in Matrix`
   259	
   260	Columns:
   261	
   262	1. `matrix_id`
   263	2. `requirement`
   264	3. `required_type`
   265	4. `risk_level`
   266	5. `comment`
   267	
   268	Rules:
   269	
   270	- one row per final `unmatched_matrix` item;
   271	- include optional applicable missing as low/conditional risk;
   272	- do not include out-of-scope / not-applicable requirements;
   273	- do not include non-evaluable headings or purely technical rows.
   274	
   275	## Bad Output Patterns
   276	
   277	Do not output:
   278	
   279	- multiple competing final JSON files;
   280	- pair-level final statuses as the primary answer;
   281	- `deviation` for unselected slash alternatives;
   282	- `deviation` for heading/title/label changes alone;
   283	- final `unmatched_contract` rows for definitions without legal effect;
   284	- final `unmatched_matrix` rows for matrix headings or non-operative parents;
   285	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   286	  requirements;
   287	- final ids that exist only in helper scripts or working ledgers;
   288	- `links` with `relationship = missing_in_contract`;
   289	- an empty `unmatched_contract` section while material contract propositions
   290	  remain unclosed in `coverage_ledger.contract`;
   291	- `extra_in_contract` with empty risk;
   292	- `aligned` with non-empty discrepancies;
   293	- `missing_in_contract` where a weak candidate is silently treated as a link;
   294	- final conclusions based only on extracted fields without source-text evidence.
AI: Good, I've read all the reference files. Now let me read the inputs and existing working artifacts.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json and contract.txt', 'status': 'in_progress'}, {'content': 'Read existing working artifacts: clause_index.json, legal_propositions.json, coverage_ledger, contract_product_profile.json', 'status': 'pending'}, {'content': 'Identify material contract-only terms (extra_in_contract vs not_material)', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]}, 'id': 'call_00_bb1hqOyLAHoWAx59GdDy6811', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json and contract.txt', 'status': 'in_progress'}, {'content': 'Read existing working artifacts: clause_index.json, legal_propositions.json, coverage_ledger, contract_product_profile.json', 'status': 'pending'}, {'content': 'Identify material contract-only terms (extra_in_contract vs not_material)', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]
AI: [{'name': 'ls', 'args': {'path': '/inputs'}, 'id': 'call_00_DpNH0Ujdeu7MPRoK8i2j6940', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_01_lwy4MOKeUI5H4wnG81Fs8048', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/enrich_propositions.py', '/outputs/working/legal_propositions.json', '/outputs/working/working_artifact_validation.json']
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_eBfCoOz0K0Kl6pnsxtAb5301', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_9HZZScvNZVKWTSg3WU7l4111', 'type': 'tool_call'}]
Tool:      1	[
     2	 {
     3	  "number":"2.1",
     4	  "enriched_text":"В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров\/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия\/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора.\nПри изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов\/Смарт-терминалов Банка\/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов\/Смарт-терминалов Банка\/сканеров.",
     5	  "required_type":"mandatory",
     6	  "main_idea":"Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
     7	  "only_for_product":"common",
     8	  "only_for_lot":"common",
     9	  "only_for_terminal":"common",
    10	  "topics":[
    11	   "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    12	   "Банк может отказать в регистрации ТСТ без указания причины",
    13	   "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    14	   "Информация о новых устройствах предоставляется с указанием их количества"
    15	  ],
    16	  "payment_method":"common"
    17	 },
    18	 {
    19	  "number":"2.2",
    20	  "enriched_text":"Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. ",
    21	  "required_type":"mandatory",
    22	  "main_idea":"Важен факт, что валюта рубль РФ, другая валюта недопустима",
    23	  "only_for_product":"common",
    24	  "only_for_lot":"common",
    25	  "only_for_terminal":"common",
    26	  "topics":[
    27	   "Расчёты производятся в рублях Российской Федерации"
    28	  ],
    29	  "payment_method":"common"
    30	 },
    31	 {
    32	  "number":"2.3.1",
    33	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации\/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг и\/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация\/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    34	  "required_type":"mandatory",
    35	  "main_idea":"Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять\/обновлять адреса.",
    36	  "only_for_product":"common",
    37	  "only_for_lot":"common",
    38	  "only_for_terminal":"common",
    39	  "topics":[
    40	   "Обмен информацией по электронной почте",
    41	   "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
    42	   "Информация и документы, направленные по электронной почте, имеют юридическую силу"
    43	  ],
    44	  "payment_method":"common"
    45	 },
    46	 {
    47	  "number":"2.3.2",
    48	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
    49	  "required_type":"mandatory",
    50	  "main_idea":"Важен сам факт возможности отправки информации \/ документов таким способом",
    51	  "only_for_product":"common",
    52	  "only_for_lot":"common",
    53	  "only_for_terminal":"common",
    54	  "topics":[
    55	   "Обмен документами посредством системы ДБО или аналогичных систем Банка"
    56	  ],
    57	  "payment_method":"common"
    58	 },
    59	 {
    60	  "number":"2.3.3",
    61	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг \/Информации о ТСТ получающей стороны;",
    62	  "required_type":"optional",
    63	  "main_idea":"Важен сам факт возможности отправки информации \/ документов таким способом",
    64	  "only_for_product":"common",
    65	  "only_for_lot":"common",
    66	  "only_for_terminal":"common",
    67	  "topics":[
    68	   "Обмен документами с доставкой нарочным или курьером"
    69	  ],
    70	  "payment_method":"common"
    71	 },
    72	 {
    73	  "number":"2.3.4",
    74	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг \/Информации о ТСТ получающей стороны;",
    75	  "required_type":"optional",
    76	  "main_idea":"Важен сам факт возможности отправки информации \/ документов таким способом",
    77	  "only_for_product":"common",
    78	  "only_for_lot":"common",
    79	  "only_for_terminal":"common",
    80	  "topics":[
    81	   "Обмен документами через заказное письмо"
    82	  ],
    83	  "payment_method":"common"
    84	 },
    85	 {
    86	  "number":"2.3.5",
    87	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing\/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью   (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
    88	  "required_type":"mandatory",
    89	  "main_idea":"Важна равнозначность документов",
    90	  "only_for_product":"common",
    91	  "only_for_lot":"common",
    92	  "only_for_terminal":"common",
    93	  "topics":[
    94	   "Обмен информацией и документами осуществляется через систему E-invoicing\/«СФЕРА-Курьер» с использованием УКЭП",
    95	   "электронные документы имеют юридическую силу документов на бумаге"
    96	  ],
    97	  "payment_method":"common"
    98	 },
    99	 {
   100	  "number":"2.3.6",
   101	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   102	  "required_type":"mandatory",
   103	  "main_idea":"Важен сам факт наличия данного канала для обмена электронными документами",
   104	  "only_for_product":"common",
   105	  "only_for_lot":"fz_44",
   106	  "only_for_terminal":"common",
   107	  "topics":[
   108	   "Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок)",
   109	   "Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП)"
   110	  ],
   111	  "payment_method":"common"
   112	 },
   113	 {
   114	  "number":"2.3.7",
   115	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24\/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках\/на Ресурсе.Сторона считается получившей информацию\/документ в случае направления способом, указанным в:\n• п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО\/аналогичной системе Банка соответственно;\n• п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма\/почтового отправления (заказного письма);\n• п. 2.3.5. Договора – в дату поступления информации\/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации\/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;\n•  п. 2.3.6. Договора – в дату направления информации\/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке;\n• п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   116	  "required_type":"optional",
   117	  "main_idea":"Для представленных в контракте способах обмена информацией \/ документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию",
   118	  "only_for_product":"common",
   119	  "only_for_lot":"common",
   120	  "only_for_terminal":"common",
   121	  "topics":[
   122	   "Обмен информацией через обращение в службу поддержки Банка",
   123	   "Дата с которой сторона считается получившей информацию в случае её направления на электронную почту",
   124	   "Дата с которой сторона считается получившей информацию в случае запроса в ДБО",
   125	   "Дата с которой сторона считается получившей информацию \/ документы в случае отправки заказного письма",
   126	   "Дата с которой сторона считается получившей информацию \/ документы в случае отправки по E-invoicing\/«СФЕРА-Курьер»",
   127	   "Дата с которой сторона считается получившей информацию \/ документы в случае отправки по ЕИС"
   128	  ],
   129	  "payment_method":"common"
   130	 },
   131	 {
   132	  "number":"2.4",
   133	  "enriched_text":"Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   134	  "required_type":"optional",
   135	  "main_idea":"Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   136	  "only_for_product":"common",
   137	  "only_for_lot":"common",
   138	  "only_for_terminal":"common",
   139	  "topics":[
   140	
   141	  ],
   142	  "payment_method":"common"
   143	 },
   144	 {
   145	  "number":"2.5.1.1",
   146	  "enriched_text":"Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;",
   147	  "required_type":"mandatory",
   148	  "main_idea":"Важен факт, что бесконтактная оплата подключается автоматически",
   149	  "only_for_product":"internet_acquiring",
   150	  "only_for_lot":"common",
   151	  "only_for_terminal":"common",
   152	  "topics":[
   153	   "SberPayOnline подключается автоматически при подключении Интернет-эквайринга",
   154	   "используется единый тариф по Интернет-эквайрингу"
   155	  ],
   156	  "payment_method":"common"
   157	 },
   158	 {
   159	  "number":"2.5.2.1",
   160	  "enriched_text":"Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.",
   161	  "required_type":"mandatory",
   162	  "main_idea":"Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением",
   163	  "only_for_product":"trade_acquiring",
   164	  "only_for_lot":"common",
   165	  "only_for_terminal":"common",
   166	  "topics":[
   167	   "подключение SberPayFaceScan оформляется на бумажном носителе",
   168	   "подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия",
   169	   "наличие документа 'Информация о ТСТ'"
   170	  ],
   171	  "payment_method":"sber_pay_face_scan"
   172	 },
   173	 {
   174	  "number":"2.6.1.1",
   175	  "enriched_text":"Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка\/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.",
   176	  "required_type":"mandatory",
   177	  "main_idea":"Для приема QR на смарт-терминал не нужно отдельное ПО",
   178	  "only_for_product":"trade_acquiring",
   179	  "only_for_lot":"common",
   180	  "only_for_terminal":"smart",
   181	  "topics":[
   182	   "OR-код подключается при установке Смарт-терминала Банка",
   183	   "OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ"
   184	  ],
   185	  "payment_method":"qr"
   186	 },
   187	 {
   188	  "number":"2.6.2.1",
   189	  "enriched_text":"Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;",
   190	  "required_type":"mandatory",
   191	  "main_idea":"ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре.  Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка",
   192	  "only_for_product":"trade_acquiring",
   193	  "only_for_lot":"common",
   194	  "only_for_terminal":"common",
   195	  "topics":[
   196	   "возможность использования QR-кода на ККТ с собственным ПО Предприятия",
   197	   "подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API)",
   198	   "порядок и условия подключения QR-API описаны на Официальном сайте Банка"
   199	  ],
   200	  "payment_method":"qr"
Tool:      1	КОНТРАКТ № _________
     2	на оказание услуг по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)
     3	г. Сочи                                      «___»________20_ г.
     4	Федеральное государственное бюджетное учреждение «Кавказский государственный природный биосферный заповедник имени Х.Г. Шапошникова», именуемое в дальнейшем «Заказчик», в лице директора Шевелева Сергея Георгиевича, действующего на основании Устава, с одной стороны, и ___________  (Лицензия № ____ от __.___.___г.), именуемое в дальнейшем Банк/Исполнитель, в лице _______, действующего на основании _________, с другой стороны, вместе именуемые Стороны, с соблюдением требований Федерального закона от 5 апреля 2013 г. № 44-ФЗ «О контрактной системе в сфере закупок товаров, работ, услуг для обеспечения государственных и муниципальных нужд» (далее – Федеральный закон № 44-ФЗ), на основании проведения _______________________ (протокол № ____ от __.__.202__г.) заключили настоящий Контракт (далее - Контракт) о нижеследующем:
     5	1. ПРЕДМЕТ КОНТРАКТА
     6	1.1. По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга) (далее - услуги) в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта, а Заказчик обязуется принять и оплатить указанные услуги в порядке и размере установленном настоящим контрактом.
     7	Идентификационный код закупки 251231702678823170100100060016619244.
     8	1.2. Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.
     9	1.3. Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.
    10	2. ТЕРМИНЫ, ОПРЕДЕЛЕНИЯ И ВЗАИМОДЕЙСТВИЕ
    11	2.1. Авторизация – процедура получения разрешения от банка-эмитента или иного юридического лица, действующего от его имени, на проведение операции;
    12	2.1.1. банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы, являющаяся электронным средством платежа. Для совершения операций в ТСТ. Карта может быть представлена на  физическом носителе, путем указания её  реквизитов, а также через мобильное  устройство, которое позволяет его покупателю совершать операции по технологии беспроводной высокочастотной связи малого радиуса действия (NFC);
    13	2.1.2. банк-эквайрер - кредитная организация, являющаяся участником платежной системы, организующая точки приема карт и осуществляющая весь комплекс финансовых операций, связанных с выполнением расчетов и платежей по картам в этих точках;
    14	2.1.3. банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;
    15	2.1.4. возврат платежа – операция, инициируемая банком-эмитентом в соответствии с правилами платежной системы и оспаривающая предъявленную банком-эквайрером операцию (транзакцию). Результатом операции «Возврат платежа» является списание денежных средств со счета банка-эквайрера и зачисление на счет банка-эмитента;
    16	2.1.5. держатель карты (держатель) – покупатель-физическое лицо, на имя которого выпущена карта;
    17	2.1.6. документ по операции - документ на бумажном носителе или в электронном виде, являющийся основанием для осуществления расчетов по операциям, совершенным с использованием карты;
    18	2.1.7. код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации;
    19	2.1.8. контрольно-кассовая техника (ККТ) – программно-технические средства и их комплексы, обеспечивающие запись и хранение фискальных данных в фискальных накопителях, формирующие фискальные документы, обеспечивающие передачу фискальных документов в налоговые органы через оператора фискальных данных и печать фискальных документов на бумажных носителях в соответствии с правилами, установленными законодательством Российской Федерации о применении контрольно-кассовой техники;
    20	2.1.9.контрольная лента - отчет, распечатываемый на электронном терминале и содержащий информацию о транзакциях, совершенных в ТСТ на электронном терминале за определенный период;
    21	2.1.10.отложенный платеж - операция оплаты, осуществляемая на основании полученного от Заказчика/ТСТ сообщения, направленного с использованием электронного терминала, о наличии задолженности покупателя перед Заказчиком/ТСТ, после окончательного расчета;
    22	2.1.11.операция – действие, осуществляемое Заказчиком/ТСТ/покупателем на электронном терминале, в том числе операция оплаты, операция отмены, операция возврата, совершенная с использованием карты/реквизитов карты/NFС-карты/ без предъявления карты;
    23	2.1.12.операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;
    24	2.1.13. операция отмены – операция, выполняемая Заказчиком/ТСТ на электронном терминале/смарт-терминале, с целью отмены авторизации. Операция отмены авторизации выполняется до проведения операции «Сверка итогов»;
    25	2.1.14. операция возврата – операция, оформляемая  Заказчиком/ТСТ  при возврате товаров/отказе от услуг или от части товаров/услуг, оплаченных картой, после проведения операции «Сверка итогов», следствием которой является возврат суммы операции оплаты или ее части на карту, предъявленную покупателем;
    26	2.1.15. платежная система – совокупность организаций, взаимодействующих по правилам платежной системы в целях осуществления перевода денежных средств;
    27	2.1.16. покупатель - физическое лицо, осуществляющее оплату товара/услуги в ТСТ при помощи карты, а также лицо, осуществляющее возврат/отказ от товара/услуги в ТСТ;
    28	2.1.17. повторяющиеся платежи – платежи в оплату товаров/услуг, осуществляемые регулярно в течение определенного периода времени;
    29	2.1.18. предавторизация - операция по резервированию денежных средств на карте для последующей оплаты, требующая подтверждения со стороны Заказчика/ТСТ с указанием суммы списания;
    30	2.1.19. предприятие (Заказчик) – торгово-сервисное предприятие (ТСП): юридическое лицо/ индивидуальный предприниматель (ИП), принимающие карты в качестве средства оплаты товаров/услуг на основании условий настоящего контракта.  Заказчик может иметь одну торгово-сервисную точку или сеть из двух и более торгово-сервисных точек;
    31	расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;
    32	2.1.20. рабочий день – день, который не признается в соответствие с законодательством Российской Федерации выходным и (или) нерабочим праздничным днем;
    33	2.1.21. реверсивная транзакция – финансово-информационное сообщение, которое банк-эквайрер направляет в платежную систему для отмены ранее направленной транзакции (например, в случае ошибочного предъявления транзакции). В результате обработки этого сообщения происходит списание денежных средств со счета банка-эквайрера (со счета Заказчика) и зачисление их на счет банка-эмитента (на счет карты покупателя);
    34	2.1.22. сводный чек электронного терминала – бумажный отчет, распечатываемый электронным терминалом и содержащий итоговую информацию по операциям за определенный промежуток времени;
    35	2.1.23. тарифы банка– стоимость услуг банка за выполнение расчетов по операциям оплаты в виде процента от суммы каждой операции оплаты и размера платы за сервисное обслуживание;
    36	2.1.24. товар/услуга – товар, работа, услуга, результат интеллектуальной деятельности, реализуемые Заказчиком в ТСТ;
    37	2.1.25. торгово-сервисная точка (ТСТ) – подразделение Заказчика, зарегистрированное банком на основании информации о ТСТ, в котором осуществляется реализация товаров/ услуг покупателям;
    38	2.1.26. торговый эквайринг – осуществление банком-эквайрером расчетов с предприятиями, осуществляющими реализацию товаров/услуг с использованием карт в ТСТ;
    39	транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;
    40	2.1.27. чек электронного терминала (чек) – документ по операции, распечатываемый электронным терминалом и содержащий информацию о проведенной операции;
    41	2.1.28. электронная сверка итогов – процедура передачи от электронного терминала исполнителю расчетной информации об операциях за определенный период;
    42	2.2. электронный терминал – электронное программно-техническое устройство исполнителя (в том числе дополнительное оборудование и/или специальное программное обеспечение ККТ), позволяющее осуществлять прием карт в ТСТ для проведения операций. Электронный терминал может включать в себя в том числе мобильный терминал (mPOS), биометрический терминал. Электронный терминал предоставляется исполнителем и устанавливается на срок действия контракта. Электронный терминал предназначен и может использоваться только в целях исполнения контракта.
    43	2.3. Банк и Заказчик в рамках настоящего Контракта обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Контрактом:
    44	2.3.1. с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Заказчиком в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Заказчика за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Контракте, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;
    45	2.3.2. посредством системы ДБО или аналогичных систем Банка;
    46	2.3.3. путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;
    47	2.3.4. путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;
    48	2.3.5. путем обмена электронными документами посредством автоматизированной системы _________________. В этом случае документы подписываются усиленной квалифицированной электронной подписью  (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;
    49	2.3.6. путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;
    50	2.3.7. через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.
    51	Сторона считается получившей информацию/документ в случае направления способом, указанным в:
    52	• п. 2.3.1, п. 2.3.2 Контракта – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;
    53	• п. 2.3.3, п. 2.3.4 Контракта – в дату доставки получающей стороне письма/почтового отправления (заказного письма);
    54	• п. 2.3.5. Контракта – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;
    55	•  п. 2.3.6. Контракта – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке ;
    56	• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка
    57	3. ЦЕНА КОНТРАКТА
    58	3.1. Максимальное значение цены контракта (стоимость услуг) (далее – цена контракта) составляет 1 900 000,00 рублей (один миллион девятьсот тысяч рублей 00 копеек), в том числе НДС ______________ (в случае если Исполнитель не является плательщиком НДС, указать «НДС не облагается»).
    59	3.1.1. Цена за единицу услуги указана в спецификации (Приложение № 1), являющейся неотъемлемой частью настоящего контракта.
    60	3.2.Цена единицы услуги включает в себя расходы Исполнителя, связанные с оказанием услуг Банка за выполнение расчетов с Заказчиком по Операциям оплаты в виде процента от суммы каждой Операции оплаты.
    61	3.3. Положения настоящего Контракта, касающиеся применения цены контракта или начальной максимальной цены Контракта применяются к максимальному значению цены Контракта, указанному в настоящем разделе Контракта, если Федеральным законом №44-ФЗ не установлено иное.
    62	4. СРОКИ, УСЛОВИЯ ОКАЗАНИЯ УСЛУГ, ПОРЯДОК ОПЛАТЫ
    63	4.1. Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее.
    64	4.2. В случае если действующим законодательством Российской Федерации и извещением о проведении закупки предусмотрены требования, предъявляемые к лицам, оказывающим услуги, составляющие предмет настоящего контракта (объект закупки), Исполнитель должен соответствовать таким требованиям.
    65	Исполнитель должен иметь лицензию на осуществление банковских операций, соответствующих виду предмета контракта (основание: Федеральный закон от 02.12.1990 N 395-1 "О банках и банковской деятельности"), за исключением случая, указанного в части 9 статьи 13 Федерального закона от 02.12.1990 № 395-1 «О банках и банковской деятельности» и в Федеральном законе «О национальной платежной системе».
    66	4.3.Оказание услуг осуществляется Исполнителем по адресу местоположения точек приема к оплате пластиковых карт (эквайринга) торгово-сервисных точек (ТСТ). Перечень ТСТ указан в Приложении № 1.
    67	В целях регистрации нового ТСТ в рамках настоящего контракта Заказчик после заключения контракта предоставляет Исполнителю заявление Заказчика на проведение расчетов по операциям с использованием банковских карт и информацию о ТСТ Заказчика/изменение информации о ТСТ заказчика, подписанную уполномоченным представителем заказчика.
    68	4.4. Оплата по контракту осуществляется по безналичному расчёту платёжным поручением путём перечисления Заказчиком денежных средств на счёт Исполнителя, указанный в настоящем контракте. В случае изменения счета Исполнителя он обязан в двухдневный срок в письменной форме сообщить об этом Заказчику с указанием новых реквизитов расчётного счёта. В противном случае все риски, связанные с перечислением Заказчиком денежных средств на указанный в настоящем контракте счёт Исполнителя, несёт Исполнитель.
    69	Оплата оказанной услуги осуществляется по цене единицы услуги исходя из объема фактически оказанной услуги, но в размере, не превышающем максимального значения цены контракта.
    70	4.5.Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг и производится ежемесячно.
    71	4.5.1. Услуги, оказанные в ноябре оплачиваются в срок не позднее 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг, но не позднее 30 декабря 2025 года.
    72	5.ОБЯЗАТЕЛЬСТВА СТОРОН
    73	5.1.Исполнитель обязуется:
    74	5.1.1. Установить Заказчику и подготовить к эксплуатации Электронные терминалы для проведения операций в течение 5 (пяти) рабочих дней с даты подписания контракта. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком. Разместить на сайте: ___________________ обучающие материалы для прохождения инструктажа сотрудниками Заказчика.
    75	5.1.2. Ежемесячно формировать и направлять Заказчику документ о приемке в соответствии с пунктами 8.3.1 и 8.3.2. Контракта.
    76	5.1.3. Обеспечить соответствие оказанных услуг предъявляемым к ним требованиям законодательства Российской Федерации.
    77	5.1.4. Обеспечивать круглосуточную работоспособность Электронных терминалов. В случае выхода из строя Электронного терминала, обеспечить Заказчика исправным Электронным терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Исполнителем заявки от Заказчикам по номеру службы поддержки Банка.
    78	5.1.5. Предоставлять Заказчику полную и точную информацию об услугах, а также о ходе исполнения своих обязательств по настоящему контракту, в том числе о сложностях, возникающих при исполнении контракта.
    79	5.1.6. Осуществлять круглосуточную авторизацию;
    80	5.1.7. Обеспечивать электронные терминалы, установленные у заказчика/ТСТ, рекламно-информационными материалами, необходимыми для проведения операций с использованием карт;
    81	5.1.8. На основании полученной от Заказчика расчетной информации, переданной от Электронного терминала Исполнителю, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты в валюте проведения операции (рубли РФ).
    82	Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.
    83	В случае технического сбоя при передаче Электронной сверки итогов/ невозможности проведения Предприятием/ТСТ или отсутствия Электронной сверки итогов по иным причинам, перечислять Заказчику суммы Операций, по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов, проводить расчеты по всем Операциям с данной ТСТ;
    84	5.1.9. Осуществлять обработку персональных данных, полученных от заказчика, а также обеспечить конфиденциальность и защиту обрабатываемых персональных данных в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных» (далее – Закона 152-ФЗ). Принимать необходимые правовые, организационные и технические меры или обеспечивать их принятие для защиты получаемых от заказчика персональных данных от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения персональных данных, а также от иных неправомерных действий в отношении получаемых от заказчика персональных данных.
    85	5.1.10. Исполнитель в соответствии с контрактом перечисляет Заказчику суммы операций оплаты услуг, совершенных на предприятии Заказчика/торгово-сервисных точках (ТСТ) с использованием карт.
    86	5.2. Исполнитель вправе:
    87	5.2.1. Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате стоимости услуг по настоящему контракту.
    88	5.2.2. Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств.
    89	5.2.3. Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов, расположенных на территории заказчика/ТСТ. Производить замену электронных терминалов, а также обновлять программное обеспечение электронного терминала, уведомив заказчика не менее чем за два рабочих дня до даты замены или обновления;
    90	5.2.4. Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций;
    91	5.2.5. Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции. Для анализа спорных ситуаций исполнитель также может потребовать от заказчика предоставления копии контрольной ленты, письменного заявления заказчика с изложением обстоятельств проведения операции, счетов за предоставленные товары/услуги, товарные или кассовые чеки и другие документы, необходимые для проведения анализа обстоятельств проведения операции или претензионной работы;
    92	5.2.6. В случае изменения реквизитов исполнителя, указанных в контракте, уведомить об этом заказчика в письменном виде путем направления информации в адрес заказчика в течение трех рабочих дней;
    93	5.2.7. В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении заказчика на проведение расчетов по операциям с использованием банковских карт/информации о ТСТ;
    94	5.2.8. Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.
    95	5.2.9. В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению Контракта при наступлении следующих событий:
    96	5.2.9.1. нарушение Заказчиком условий Контракта;
    97	5.2.9.2. внесение данных Заказчика в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;
    98	5.2.9.3. при наличии у Исполнителя подозрений, что Операции в ТСТ совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;
    99	5.2.9.4. получение негативной информации о Заказчике/ТСТ от органов государственной власти РФ и/или Платежных систем;
   100	5.2.9.5. получение информации о мошенничестве в ТСТ
   101	стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных систем, полученные c использованием факсимильной связи, по электронной почте (e-mail);
   102	5.2.9.6. осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций;
   103	5.2.9.7. ликвидация Заказчика либо возбуждение в отношении Заказчика дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)»;
   104	5.2.9.8. выявление недостоверных сведений о Заказчике/ТСТ, руководителе(-ях) в информации, указанной при заключении Контракта;
   105	5.2.9.9. несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Заказчика, указанному в Информации о ТСТ;
   106	5.2.9.10. отсутствие операций в течение 30 (тридцати) календарных дней подряд
   107	5.2.9.11. исчерпание Цены Контракта и/или окончание срока действия Контракта.
   108	5.2.10. Удерживать из сумм, подлежащих перечислению Заказчику по Контракту, следующие суммы:
   109	5.2.10.1 Суммы Операций, являющихся недействительными, в следующих случаях:
   110	Операция совершена с нарушением Контракта, требований законодательства РФ и/или правил Платежной системы и инструктивных материалов Банка;
   111	Операция совершена по поддельной или недействительной Карте;
   112	Документ по операции заполнен не полностью, имеются исправления или отсутствует возможность определить сумму Операции, код Авторизации;
   113	экземпляр Документа по операции, переданный в Банк, не соответствует экземпляру Документа по операции, переданному Покупателю;
   114	подпись Покупателя на Чеке электронного терминала отсутствует, при этом на Чеке электронного терминала присутствует поле «Подпись Клиента»;
   115	по требованию Банка в течение 3 (трех) рабочих дней со дня получения запроса не предоставлены или предоставлены не в полном объеме (или не соответствующие правилам Платежной системы) или в ненадлежащем качестве подтверждающие Документы по операции/объяснения обстоятельств Операции;
   116	оплаченные с использованием Карты/ ее реквизитов/ NFС-карты/ SberPay/ Плати QR/ Платежного счета /Платежных решений  Товары/услуги были возвращены Предприятию, или не доставлены Покупателю/услуги отменены/не оказаны, но возврат денежных средств Покупателю произведен не был (за исключением случаев, когда Товары/услуги не были приняты/возврат Товара/отказ от услуг не предусмотрен законодательством РФ или правилами работы Предприятия и Покупатель был об этом проинформирован до совершения сделки);
   117	Товар/услуга уже был оплачен Покупателем ранее (о чем имеется документальное подтверждение);
   118	на совершенную Операцию Банком не был получен код Авторизации согласно Порядка проведения операций в Торгово-сервисных точках/на Ресурсе. Код Авторизации считается полученным Банком в том случае, если он содержится в электронных реестрах кодов Авторизации Банка и относится к указанной Операции. Код Авторизации указывается на Чеке Электронного терминала, который передается в ККТ Предприятия от Электронного терминала ;
   119	сумма Товара/услуги была разбита на несколько Операций;
   120	от Банка-эмитента получена информация о мошенническом характере Операции;
   121	Операция была проведена без считывания Карты в Электронном терминале (реквизиты Карты были введены в Электронный терминал вручную), за исключением случаев, когда данные действия согласованы  с Банком.
   122	5.2.10.2 Суммы, ошибочно перечисленные на счет Заказчика.
   123	5.2.10.3 Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.
   124	5.2.10.4 Исполнитель  удерживает из общих сумм, подлежащих перечислению на Счет Заказчика суммы операций, которые были оспорены и/или списаны со счета Исполнителя Банком – эмитентом в соответствии с правилами Платежных систем по операциям, проведенным в ТСТ, а также суммы оспоренных операций в отношении Товаров/услуг, реализуемых Заказчиком  как агентом.
   125	5.2.10.5 Банк удерживает из общих сумм, подлежащих перечислению на Счет Заказчика суммы штрафов и иных убытков, возникших у Исполнителя в результате применения к нему штрафных санкций в соответствии с правилами Платежных систем, а также привлечения Исполнителя к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Заказчиком обязательств по Контракту.
   126	5.3. Заказчик обязуется:
   127	5.3.1. Принять оказанные услуги по документу о приемке оказанных услуг.
   128	5.3.2. Оплатить стоимость услуг, оказанных Исполнителем, согласно условиям настоящего контракта.
   129	5.3.3. Осуществлять контроль за ходом оказания услуг Исполнителем.
   130	5.3.4. Принять решение об одностороннем отказе от исполнения настоящего контракта в случае, если в ходе исполнения контракта установлено, что Исполнитель не соответствует установленным извещением о проведении закупки требованиям к участникам закупки или предоставил недостоверную информацию о своем соответствии таким требованиям, что позволило ему стать победителем определения Исполнителя.
   131	5.3.5. Требовать уплаты неустоек (штрафов, пеней) в случае просрочки исполнения Исполнителем обязательств, предусмотренных контрактом, а также в иных случаях неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных контрактом.
   132	5.3.6. Уменьшить сумму, подлежащую уплате Заказчиком юридическому лицу или физическому лицу, в том числе зарегистрированному в качестве индивидуального предпринимателя, на размер налогов, сборов и иных обязательных платежей в бюджеты бюджетной системы Российской Федерации, связанных с оплатой контракта, если в соответствии с законодательством Российской Федерации о налогах и сборах такие налоги, сборы и иные обязательные платежи подлежат уплате в бюджеты бюджетной системы Российской Федерации.
   133	5.3.7. Размещать на видных местах ТСТ, предоставляемые исполнителем рекламно-информационные материалы, извещающие покупателей о возможности оплаты услуг с использованием карт, в случае если это не противоречит требованиям законодательства Российской Федерации;
   134	5.3.8. Не разбивать сумму одной операции оплаты на несколько сумм и не проводить отдельные операции на каждую из этих сумм;
   135	5.3.9. Не использовать реквизиты карты, которые стали доступны заказчику/ТСТ, для иных целей, кроме как проведение операций в присутствии или по распоряжению покупателя;
   136	5.3.10. Проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту и нести ответственность за правильность указанной в документах информации;
   137	5.3.11. Хранить в недоступном для третьих лиц месте документы по операциям (чеки, кассовые чеки, распоряжения покупателя, документы, подтверждающие факт передачи товара/оказания услуги, контрольные ленты и т.п.) не менее тринадцати месяцев с даты совершения операции и передавать их копии надлежащего качества (изображение четкое, размер не менее оригинального документа) исполнителю по его запросу  в течение трех рабочих дней с даты получения запроса;
   138	5.3.12. Передавать исполнителю по его запросу в течение трех рабочих дней с даты получения запроса от исполнителя письменное заявление с изложением обстоятельств проведения операции в ТСТ. В случае утраты составленных с использованием карты документов по операции немедленно сообщить об утрате исполнителю;
   139	5.3.13. В случае реорганизации, внесения изменений и дополнений в документы, представленные заказчиком при заключении  контракта, при открытии в отношении заказчика/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса местонахождения заказчика/ТСТ, внесенного в ЕГРЮЛ, реквизитов заказчика/ТСТ обязуется информировать исполнителя и передать (по месту заключения контракта) надлежащим образом заверенные и оформленные документы, подтверждающие внесение изменений и дополнений не позднее трех рабочих дней с даты дополнений/изменений;
   140	5.3.14. Предоставлять исполнителю достоверные документы и сведения, необходимые исполнителю для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе, но не исключительно: не реже одного раза в год, а также по отдельному запросу исполнителя в течение семи рабочих дней со дня получения запроса обновлять сведения и документы, представленные исполнителю при заключении настоящего контракта, включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации заказчика, а также сведения о своих представителях, выгодоприобретателях и бенефициарных владельцах (при наличии);
   141	5.3.15. По письменному запросу исполнителя заказчик обязуется предоставить подтверждение правомерности передачи ПДн. В случае если заказчик не предоставит подтверждение наличия таких оснований, он обязуется за свой счёт урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные исполнителю, а также возместить любые убытки и расходы, понесенные исполнителем в результате не предоставления таких доказательств. Заказчик обязан уведомить исполнителя об отзыве согласия руководителя заказчика на передачу указанных данных;
   142	5.3.16. С даты расторжения контракта прекратить прием к оплате карт, снять рекламно-информационные материалы, извещающие об обслуживании карт;
   143	5.3.17. Не принимать мер противодействия исполнителю в проведение проверки заказчика/ТСТ на предмет выявления мошеннических операций и/или предоставления покупателям товаров/услуг, не соответствующих роду деятельности заказчика/ТСТ, а также оказывать содействие исполнителю в проведении разбирательства по факту совершения подозрительных операций;
   144	5.3.18. При осуществлении операций у заказчика в ТСТ (торговый эквайринг):
   145	5.3.18.1. Использовать электронные терминалы (в том числе технологические sim-карты)/смарт-терминалы и программное обеспечение, предоставленное исполнителем, только для целей реализации настоящего контракта и на территории регистрации ТСТ/фактической установки электронного терминала. Не вносить изменения в программное обеспечение и электронные терминалы/смарт-терминалы, предоставленное исполнителем, и не осуществлять самостоятельно их ремонт. Использовать термоленту только для электронных терминалов, установленных в ТСТ. Не передавать третьим лицам электронные терминалы, документы по операциям, термоленту для электронных терминалов и рекламно-инструктивные материалы, предоставленные исполнителем, за исключением работников обслуживающей компании;
   146	5.3.18.2. Предоставлять исполнителю доступ к местам установки электронных терминалов для проведения работ по его подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке;
   147	5.3.18.3. Принять электронные терминалы по акту принятия оказанных услуг, составленному в двух экземплярах и подписанных исполнителем и заказчиком. один экземпляр акта находится на хранении у исполнителя, второй – у заказчика;
   148	5.3.20.4. В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя;
   149	5.3.18.5. Вернуть исполнителю или обслуживающей компании электронные терминалы/смарт-терминала в течение пяти рабочих дней с даты расторжения контракта или с даты получения письменного/устного требования исполнителя о возврате электронных терминалов;
   150	5.3.19. Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере:
   151	• средств, которые в соответствии с правилами Платежных систем были списаны со счета Исполнителя в пользу Банка-эмитента либо уплачены Исполнителем Банку-эмитенту и (или) Держателям карт, эмитированных Исполнителем, по Операциям :
   152	 ставшим предметом каких-либо споров и разногласий в соответствии с законодательством Российской Федерации и (или) в соответствии с правилами Платежных систем;
   153	 являющимся недействительными в соответствии с Контрактом;
   154	• средств, которые в соответствии с правилами Платежных систем были списаны со счета Исполнителя либо уплачены Исполнителем в связи с рассмотрением споров и разногласий между Покупателями и Заказчиком касательно Операций, указанных в настоящем пункте Контракта, в том числе любые сборы, комиссии, платы и (или) иные расходы Исполнителя, связанные с рассмотрением споров и разногласий по таким Операциям;
   155	• убытков, возникших у Исполнителя в результате применения к нему штрафных санкций в соответствии с законодательством Российской Федерации и (или) правилами Платежных систем, а также привлечения Исполнителя к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Заказчиком обязательств по Контракту.
   156	5.3.20. В рамках настоящего Контракта Заказчик передает Исполнителю персональные данные (далее – ПДн) руководителя Заказчика, состав которых включает: ФИО, адрес, паспортные данные. Заказчик гарантирует наличие правовых оснований на передачу Исполнителю персональных данных руководителя Заказчика, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные в целях, оказания услуг по контракту.
   157	5.4. Заказчик вправе:
   158	5.4.1. Требовать от Исполнителя исполнения обязательств, предусмотренных контрактом, надлежащим образом в соответствии с действующим законодательством Российской Федерации и настоящим контрактом.
   159	5.4.2. Отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества.
   160	5.4.3. Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств.
   161	5.4.4. Отказаться от оплаты услуг ненадлежащего качества, а если услуги оплачены, потребовать возврата уплаченных сумм, а также требовать возмещения убытков.
   162	5.4.5. Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем настоящего контракта;
   163	5.5.  Заказчик обязуется передавать Исполнителю по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Исполнителя письменное заявление с изложением обстоятельств проведения Операции. В случае утраты составленных Документов по операции немедленно сообщить об утрате Исполнителю  одним из способов, предусмотренных Контрактом.
   164	5.6. Заказчик обязуется в случае утери оборудования Заказчиком:
   165	Вернуть Исполнителю или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Контракта или с даты получения письменного/устного требования Исполнителя о возврате Электронных терминалов/Смарт-терминалов Исполнителя.
   166	5.7. В случае невозврата Электронных терминалов/Смарт-терминалов Исполнителя  Заказчик обязан уплатить Исполнителю  штраф в размере 10 000 (десяти тысяч) рублей, включая НДС, за каждый Электронный терминал, в размере 25 000 (двадцати пяти тысяч) рублей, включая НДС, за каждый Смарт-терминал Банка.
   167	5.9. Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций с использованием карт путем обращения в службу поддержки исполнителя.
   168	5.10. Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________.
   169	6. АНТИКОРРУПЦИОННАЯ ОГОВОРКА
   170	6.1. При заключении, исполнении, изменении и расторжении Контракта Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция» , а также иных действий (бездействия), нарушающих требования применимого законодательства, применимых норм международного права в области противодействия коррупции.
   171	7. ОТВЕТСТВЕННОСТЬ СТОРОН
   172	7.1. За неисполнение или ненадлежащее исполнение обязательств по Контракту Стороны несут ответственность в соответствии с действующим законодательством Российской Федерации.
   173	Сторона освобождается от уплаты неустойки (штрафа, пени), если докажет, что неисполнение или ненадлежащее исполнение обязательства, предусмотренного Контрактом, произошло вследствие непреодолимой силы или по вине другой стороны.
   174	Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, не может превышать цену контракта.
   175	Общая сумма начисленных штрафов за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, не может превышать цену контракта.
   176	7.2. В случае просрочки исполнения Заказчиком обязательств, предусмотренных Контрактом, а также в иных случаях неисполнения или ненадлежащего исполнения Заказчиком обязательств, предусмотренных Контрактом, Исполнитель вправе потребовать уплаты неустоек (штрафов, пеней).
   177	7.3. Пеня начисляется за каждый день просрочки исполнения Заказчиком обязательства, предусмотренного Контрактом, начиная со дня, следующего после дня истечения установленного Контрактом срока исполнения обязательства. При этом размер пени устанавливается в размере 1/300 действующей на день уплаты пеней ключевой ставки Центрального банка Российской Федерации от не уплаченной в срок суммы.
   178	7.4. Штрафы начисляются за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств, предусмотренных Контрактом.
   179	7.4.1. Размер штрафа по каждому факту неисполнения Заказчиком обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств, предусмотренных Контрактом, устанавливается в соответствии с постановлением Правительства РФ от 30.08.2017 № 1042 «Об утверждении Правил определения размера штрафа, начисляемого в случае ненадлежащего исполнения заказчиком, неисполнения или ненадлежащего исполнения поставщиком (Подрядчиком, исполнителем) обязательств, предусмотренных контрактом (за исключением просрочки исполнения обязательств заказчиком, поставщиком (Подрядчиком, исполнителем), о внесении изменений в постановление Правительства Российской Федерации от 15 мая 2017 г. № 570 и признании утратившим силу постановления Правительства Российской Федерации от 25 ноября 2013 г. N 1063» (далее – Постановление № 1042) в следующем порядке:
   180	а) 1000 рублей, если цена контракта не превышает 3 млн. рублей (включительно);
   181	б) 5000 рублей, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   182	в) 10000 рублей, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   183	г) 100000 рублей, если цена контракта превышает 100 млн. рублей.
   184	7.5. В случае просрочки исполнения Исполнителем обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом, а также в иных случаях неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных Контрактом, Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней).
   185	7.6. Пеня начисляется за каждый день просрочки исполнения Исполнителем обязательства, предусмотренного Контрактом, начиная со дня, следующего за днем истечения установленного Контрактом срока исполнения обязательства,  в размере 1/300 действующей на дату уплаты пеней ключевой ставки Центрального банка Российской Федерации от цены контракта, уменьшенной на сумму, пропорциональную объему обязательств, предусмотренных Контрактом (соответствующим отдельным этапом исполнения контракта) и фактически исполненных Исполнителем, за исключением случаев, если законодательством РФ установлен иной порядок начисления пени.
   186	7.7. Штрафы начисляются за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, за исключением просрочки исполнения Исполнителем обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом.
   187	7.7.1. Размер штрафа по каждому факту неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом, и за исключением случаев, если законодательством РФ установлен иной порядок начисления пени, устанавливается в соответствии с Постановлением № 1042 в следующем порядке:
   188	а) 10 процентов цены контракта (этапа) в случае, если цена контракта (этапа) не превышает 3 млн. рублей;
   189	б) 5 процентов цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   190	в) 1 процент цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   191	г) 0,5 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 100 млн. рублей до 500 млн. рублей (включительно);
   192	д) 0,4 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 500 млн. рублей до 1 млрд. рублей (включительно);
   193	е) 0,3 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 1 млрд. рублей до 2 млрд. рублей (включительно);
   194	ж) 0,25 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 2 млрд. рублей до 5 млрд. рублей (включительно);
   195	з) 0,2 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 5 млрд. рублей до 10 млрд. рублей (включительно);
   196	и) 0,1 процента цены контракта (этапа) в случае, если цена контракта (этапа) превышает 10 млрд. рублей.
   197	7.7.2. Размер штрафа Исполнителем как победителя закупки (или иного участника закупки в случаях, установленных Федеральным законом от 05.04.2013 № 44-ФЗ), предложившего наиболее высокую цену за право заключения контракта, по каждому факту неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом, устанавливается в соответствии с Постановлением № 1042 в следующем порядке:
   198	а) в случае, если цена контракта не превышает начальную (максимальную) цену контракта:
   199	10 процентов начальной (максимальной) цены контракта, если цена контракта не превышает 3 млн. рублей;
   200	5 процентов начальной (максимальной) цены контракта, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
AI: Let me continue reading the contract and matrix files to get the full picture.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_O9PjUYjkXgUWvChXWpoy9218', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 200}, 'id': 'call_01_CG4778FXY6UbcefBwi5y0282', 'type': 'tool_call'}]
Tool:    201	1 процент начальной (максимальной) цены контракта, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   202	б) в случае, если цена контракта превышает начальную (максимальную) цену контракта:
   203	10 процентов цены контракта, если цена контракта не превышает 3 млн. рублей;
   204	5 процентов цены контракта, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   205	1 процент цены контракта, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно).
   206	7.7.3. Размер штрафа по каждому факту неисполнения или ненадлежащего исполнения Исполнителем обязательства, предусмотренного Контрактом, которое не имеет стоимостного выражения (при наличии в Контракте таких обязательств), устанавливается в соответствии с Постановлением № 1042 в следующем порядке:
   207	а) 1000 рублей, если цена контракта не превышает 3 млн. рублей (включительно);
   208	б) 5000 рублей, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   209	в) 10000 рублей, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   210	г) 100000 рублей, если цена контракта превышает 100 млн. рублей.
   211	7.8. В случае обмена документами при применении мер ответственности и совершении иных действий в связи с нарушением Исполнителем или Заказчиком условий Контракта, такой обмен осуществляется с использованием ЕИС путем направления электронных уведомлений. Такие уведомления формируются с использованием ЕИС, подписываются усиленной электронной подписью лица, имеющего право действовать от имени Заказчика или Исполнителя соответственно, и размещаются в ЕИС без размещения на официальном сайте.
   212	7.9.   Применение неустойки (штрафа, пени) не освобождает Стороны от исполнения обязательств по Контракту.
   213	7.10. Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, не может превышать цену Контракта.
   214	7.11. Общая сумма начисленных штрафов за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, не может превышать цену Контракта.
   215	7.12. В случае расторжения Контракта в связи с односторонним отказом Стороны от исполнения Контракта другая Сторона вправе потребовать возмещения только фактически понесенного ущерба, непосредственно обусловленного обстоятельствами, являющимися основанием для принятия решения об одностороннем отказе от исполнения Контракта сверх начисленных неустоек.
   216	8. КАЧЕСТВО ОКАЗАННЫХ УСЛУГ, ПОРЯДОК ИХ ПРИЕМКИ.
   217	ГАРАНТИЯ КАЧЕСТВА УСЛУГ
   218	8.1. Исполнитель гарантирует Заказчику качество оказанных услуг, предусмотренных требованиями Приложения №1 в течение всего срока, установленного нормативно-правовыми актами Российской Федерации.
   219	8.2. Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг его специалистами.
   220	8.3. Приемка результата исполнения Контракта осуществляется в порядке, установленном законодательством Российской Федерации и настоящим Контрактом.
   221	8.3.1. Исполнитель ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за отчетным, формирует с использованием единой информационной системы, подписывает усиленной квалифицированной электронной подписью (далее – усиленной электронной подписью) лица, имеющего право действовать от имени Исполнителя, и размещает в единой информационной системе документ о приемке, который должен содержать:
   222	а) включенные в контракт в соответствии с пунктом 1 части 2 статьи 51 Федерального закона № 44-ФЗ идентификационный код закупки, наименование, место нахождения заказчика, наименование объекта закупки, место оказания услуги, информацию о Исполнителе, предусмотренную подпунктами "а", "г" и "е" части 1 статьи 43 Федерального закона № 44-ФЗ, единицу измерения поставленного товара (при осуществлении закупки товара);
   223	б) наименование оказанной услуги;
   224	д) информацию об объеме оказанной услуги;
   225	е) стоимость исполненных Исполнителем обязательств, предусмотренных контрактом, с указанием цены за единицу оказанной услуги;
   226	ж) иную информацию (с учетом требований, установленных в соответствии с частью 3 статьи 5 Федерального закона № 44-ФЗ).
   227	8.3.2. К документу о приемке, предусмотренному пунктом 8.3.1. Контракта, Исполнитель прилагает документы, предусмотренные Контрактом, которые считаются его неотъемлемой частью: счет-фактуру (при наличии), акт о перечислении Заказчику сумм операций по картам и счет ф.363 на оплату услуг за проведение расчетов по Операциям оплаты за Отчетный месяц.
   228	При этом в случае, если информация, содержащаяся в прилагаемых документах, не соответствует информации, содержащейся в документе о приемке, приоритет имеет предусмотренная пунктом 8.3.1 Контракта информация, содержащаяся в документе о приемке.
   229	8.4. Датой поступления Заказчику документа о приемке, подписанного Исполнителем, считается дата размещения в соответствии с пунктом 8.3.1. Контракта такого документа в единой информационной системе в соответствии с часовой зоной, в которой расположен Заказчик.
   230	8.5. Приемка услуг от имени Заказчика производится уполномоченным лицом, (либо приемочной комиссией – п. 8.5.8) в следующем порядке:
   231	8.5.1. Заказчик в срок не более 10 (десяти) рабочих дней со дня поступления документа о приемке в соответствии с пунктом 3 части 13 статьи 94  Федерального закона № 44-ФЗ, пунктом 8.3.1. Контракта Заказчик подписывает усиленной электронной подписью лица, имеющего право действовать от имени Заказчика, и размещает в ЕИС документ о приемке либо формирует с использованием ЕИС, подписывает усиленной электронной подписью лица, имеющего право действовать от имени заказчика, и размещает в ЕИС мотивированный отказ от подписания документа о приемке с указанием причин такого отказа.
   232	8.5.2. По письменному уведомлению Исполнителем Заказчика, приемка оказанных услуг может производиться только в присутствии представителя Исполнителя, имеющего надлежащим образом оформленные документы на участие в приемке с точно оговоренными полномочиями. О намерении принять участие в приемке Исполнитель обязан сообщить до момента окончания оказания услуг Заказчику, указав в письменном уведомлении дату в пределах установленного п. 8.5.1 срока, но не позднее чем за 15 рабочих дней до истечения срока приемки, предусмотренного Контрактом.
   233	8.5.3. В случае, если поступило уведомление об участии в приемке в установленный Контрактом срок, приемка оказанных услуг производится только в двустороннем порядке.
   234	8.5.4. В случае, если уведомление об участии в приемке не поступило, либо поступило в более поздний срок, чем предусмотрено Контрактом, приемка оказанных услуг производится только Заказчиком в одностороннем порядке.
   235	8.5.5. Для проверки оказанных услуг, предусмотренных Контрактом, в части их соответствия условиям Контракта, Заказчик проводит экспертизу.
   236	8.5.6. Экспертиза результатов, предусмотренных Контрактом, может проводиться Заказчиком своими силами или к ее проведению могут привлекаться эксперты, экспертные организации на основании контрактов, заключенных в соответствии с Федеральным законом № 44-ФЗ.
   237	8.5.7. В случае отсутствия замечаний Заказчик (уполномоченное лицо) в течение десяти рабочих дней с даты, следующей за днем поступления документа о приемке в соответствии с пунктом 8.4 Контракта подписывает усиленной электронной подписью лица, имеющего право действовать от имени Заказчика, и размещает в единой информационной системе документ о приемке.
   238	8.5.8. В случае, если уполномоченным лицом будут установлены несоответствия требованиям, указанным в Контракте, дальнейшая приемка может осуществляться приемочной комиссией.
   239	Не позднее десяти рабочих дней, следующих за днем поступления Заказчику документа о приемке в соответствии с пунктом 8.4 Контракта:
   240	а) члены приемочной комиссии подписывают усиленными электронными подписями решение приемочной комиссии в составе поступившего документа о приемке или формируют с использованием единой информационной системы, подписывают усиленными электронными подписями мотивированный отказ от подписания документа о приемке с указанием причин такого отказа.
   241	б) После подписания членами приемочной комиссии в соответствии с подпунктом «а» настоящего пункта документа о приемке или мотивированного отказа от подписания документа о приемке Заказчик подписывает документ о приемке или мотивированный отказ от подписания документа о приемке усиленной электронной подписью лица, имеющего право действовать от имени Заказчика, и размещает их в единой информационной системе.
   242	в) Датой поступления Исполнителю документа о приемке, мотивированного отказа от подписания документа о приемке считается дата размещения в соответствии с настоящим пунктом таких документа о приемке, мотивированного отказа в единой информационной системе в соответствии с часовой зоной, в которой расположен Исполнитель.
   243	8.5.9. В случае получения в соответствии с пунктом 8.5.8. Контракта мотивированного отказа от подписания документа о приемке Исполнитель вправе устранить причины, указанные в таком мотивированном отказе, и направить заказчику исправленный документ о приемке в порядке, предусмотренном настоящим разделом Контракта.
   244	8.6. Датой приемки оказанных услуг считается дата размещения в единой информационной системе документа о приемке, подписанного уполномоченным лицом или приемочной комиссией Заказчика.
   245	8.7. Внесение исправлений в документ о приемке, оформленный в соответствии с настоящим разделом Контракта, осуществляется путем формирования, подписания усиленными электронными подписями уполномоченных лиц, имеющих право действовать от имени Исполнителя, Заказчика, и размещения в единой информационной системе исправленного документа о приемке.
   246	8.8. Оформление результата проведения процедуры приемки оказанных услуг осуществляется в порядке и в сроки, указанные в настоящем разделе Контракта.
   247	8.9. В случае выявления несоответствия оказанной услуги условиям Контракта Заказчик вправе не отказывать в приемке оказанной услуги, если выявленное несоответствие не препятствует приемке и устранено Исполнителем.
   248	8.10. В случае оказания услуг ненадлежащего качества Исполнитель обязан безвозмездно устранить недостатки в течение 3 дней с даты заявления о них Заказчиком.
   249	8.11. Подписанный усиленными электронными подписями Заказчика и Исполнителя документ о приемке является основанием для оплаты Исполнителю оказанных услуг.
   250	9. ДЕЙСТВИЕ ОБСТОЯТЕЛЬСТВ НЕПРЕОДОЛИМОЙ СИЛЫ
   251	9.1. Стороны освобождаются от ответственности за частичное или полное неисполнение своих обязательств по настоящему контракту, если их исполнению препятствует чрезвычайное и непреодолимое при данных условиях обстоятельство (непреодолимая сила), а именно: стихийные бедствия, наводнения, землетрясения, пожары, военные действия, забастовки, массовые заболевания(эпидемия), повлекшие введение режима повышенной готовности или чрезвычайной ситуации.
   252	9.2. При возникновении обстоятельств непреодолимой силы, препятствующих исполнению обязательств по настоящему контракту одной из Сторон, она обязана оповестить другую Сторону не позднее пяти дней с момента возникновения таких обстоятельств, при этом срок выполнения обязательств по контракту переносится соразмерно времени, в течение которого действовали такие обстоятельства. В случае если такие обстоятельства длятся более одного календарного месяца Стороны праве расторгнуть настоящий контракт по соглашению Сторон.
   253	9.3. При рассмотрении споров в связи с обстоятельствами непреодолимой силы сторона, ссылающаяся на эти обстоятельства, обязана представить документальное подтверждение их наступления (выданный лицом, уполномоченным выдавать такие документы).
   254	10. ПОРЯДОК РАЗРЕШЕНИЯ СПОРОВ
   255	10.1. Все споры или разногласия, возникающие между Сторонами по настоящему контракту или в связи с ним, разрешаются путем переговоров (в досудебном порядке).
   256	Срок ответа на претензии, письма и обращения – 10 (десять) календарных дней с даты их получения. Любое уведомление, которое одна Сторона направляет другой Стороне в соответствии с Контрактом, высылается в письменном виде, заказным письмом или доставляется лично по юридическим (почтовым) адресам другой Стороны с подтверждением о получении.
   257	В случае обмена документами при применении мер ответственности и совершении иных действий в связи с нарушением Исполнителем или заказчиком условий контракта в отношении контракта, заключенного по результатам электронных процедур, такой обмен осуществляется с использованием единой информационной системы путем направления электронных уведомлений. Такие уведомления формируются с использованием единой информационной системы, подписываются усиленной электронной подписью лица, имеющего право действовать от имени заказчика, исполнителя и размещаются в единой информационной системе без размещения на официальном сайте.
   258	10.2. В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в Арбитражном суде Краснодарского края.
   259	11. СРОК ДЕЙСТВИЯ, ПОРЯДОК ИЗМЕНЕНИЯИРАСТОРЖЕНИЯ КОНТРАКТА
   260	11.1. Настоящий контракт действует с даты заключения по 30 декабря 2025 года, или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее, а по обязательствам, возникшим в период действия настоящего Контракта, но не исполненным до окончания срока действия Контракта – до полного исполнения принятых сторонами обязательств. Окончание срока действия контракта не освобождает Стороны от ответственности за его нарушение.
   261	11.2. Любые изменения и дополнения к настоящему контракту имеют силу только в том случае, если они оформлены в письменном виде и подписаны обеими Сторонами. В случае изменения у какой - либо из Сторон места нахождения, названия она обязана в течение двух дней письменно известить об этом другую Сторону.
   262	11.3. Расторжение контракта допускается по соглашению Сторон, по решению суда, в случае одностороннего отказа Стороны контракта от исполнения контракта в соответствии с гражданским законодательством Российской Федерации.
   263	11.4. Заказчик вправе принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Гражданским кодексом Российской Федерации для одностороннего отказа от исполнения отдельных видов обязательств.
   264	11.5. Решение Сторон об одностороннем отказе от исполнения контракта по основаниям, предусмотренным ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств, принимается и реализуется в порядке и сроки, предусмотренные статьей 95 Федерального закона № 44-ФЗ.
   265	11.6. Изменение и(или) расторжение контракта осуществляется в порядке, сроки, случаях и на условиях, установленных статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ.
   266	11.7. Во всем, что не предусмотрено настоящим контрактом, Стороны руководствуются действующим законодательством Российской Федерации.
   267	11.8. Стороны предусмотрели, что изменение существенных условий контракта при его исполнении не допускается, за исключением их изменения по соглашению Сторон в случаях, предусмотренных Федеральным законом № 44-ФЗ.
   268	12. ПРОЧИЕ УСЛОВИЯ
   269	12.1. При исполнении настоящего контракта не допускается перемена Исполнителя, за исключением случая, когда новый исполнитель является правопреемником Исполнителя по контракту вследствие реорганизации юридического лица в форме преобразования, слияния или присоединения.
   270	12.2. В случае перемены Заказчика по контракту права и обязанности Заказчика по настоящему контракту переходят к новому Заказчику в том же объеме и на тех же условиях.
   271	12.3. При исполнении контракта по согласованию Заказчика с Исполнителем допускается оказание услуги, качество, технические и функциональные характеристики (потребительские свойства) которых являются улучшенными по сравнению с качеством и соответствующими техническими и функциональными характеристиками, указанными в контракте.
   272	12.4. Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон.
   273	12.5. Приложения:
   274	№ 1 «Техническое задание»
   275	№ 2 «Спецификация»
   276	13. МЕСТА НАХОЖДЕНИЯ, БАНКОВСКИЕ РЕКВИЗИТЫСТОРОН
   277	ЗАКАЗЧИК
   278	Федеральное государственное бюджетное учреждение «Кавказский государственный природный биосферный заповедник имени Х.Г. Шапошникова» (ФГБУ «Кавказский государственный  заповедник»)
   279	354340, г. Сочи, Адлерский район ул. Карла Маркса, д.8
   280	ИНН 2317026788 КПП231701001
   281	ОГРН: 1022302723409
   282	р\с 03214643000000011800
   283	банк получатель: Южное ГУ банка России//УФК по Краснодарскому краю г.Краснодар (л/с 20186X56810)
   284	БИК ТОФК 010349101
   285	ЕКС 40102810945370000010
   286	тел/факс (862) 240-51-36, 240-52-65
   287	e-mail: kgpbz@mail.ru
   288	Директор
   289	___________________________ С.Г. Шевелев
   290	ИСПОЛНИТЕЛЬ
   291	Приложение № 1
   292	к контракту на оказание услуг
   293	от _____________ № _______
   294	Техническое задание
   295	Оказание услуг по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)
   296	1. Объектом закупки является: Оказание услуг по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)  (далее по тексту- услуга, эквайринг) для нужд Федерального государственного бюджетного учреждения «Кавказский государственный природный биосферный заповедник имени Х. Г. Шапошникова» (далее - Заказчик).
   297	Платежно-пропускная система, установленная у Заказчика - «Барс» НПО «Дата Крат».
   298	2. Местоположение точек приема Заказчика установки электронных терминалов и оказания услуг, а также количество необходимых электронных терминалов (POS-терминалов):
   299	№ п/п
   300	Адрес объекта Заказчика, на которых необходимо установить электронные терминалы и обеспечить оказание услуг
   301	Количество необходимых POS-терминалов
   302	1
   303	Краснодарский край, г. Сочи, Адлерский район ул. Карла Маркса, д. 8 (Управление)
   304	1
   305	2
   306	Краснодарский край, пгт. Сириус, ул. Нагорный тупик, 13, (Дендрологический парк федерального значения «Южные культуры»)
   307	4
   308	3
   309	Краснодарский край, город Сочи, кордон Лаура Южное участковое лесничество: Краснодарский край, Сочи г, Адлерский р-н, Эстосадок с, Ачипсинская ул (43N4150 — 040E1600 в системе координат ГСК-2011) (Вольерный комплекс Лаура)
   310	2
   311	4
   312	Краснодарский край, город Сочи,  Хостинское участковое лесничество – г. Сочи, ул. Самшитовая, (Тисо-самшитовая роща)
   313	2
   314	5
   315	Республика Адыгея,  Майкопский район, ул. Заречная дом 5.(кордон Гузерипль на территории заповедника Северное участковое лесничество) (Вольерный комплекс Гузерипль)
   316	2
   317	6
   318	Краснодарский край, город Сочи, пгт. Дагомыс, ул. Гайдара, 16
   319	1
   320	7
   321	Краснодарский край, пгт. Псебай, ул. Первомайская, 186
   322	1
   323	8
   324	Краснодарский край, город Сочи,  Хостинское участковое лесничество,  Приют "Фишт", восточное подножие горы Фишт, Западное участковое лесничество (43N5731— 039E5549 в системе координат ГСК-2011)
   325	1
   326	Данный перечень объектов Заказчика не является исчерпывающим и может изменяться.
   327	3. Перечень карт, которые сервисная точка принимает в оплату услуг:
   328	№п/п
   329	Наименование платежной системы
   330	1
   331	Национальная система платежных карт «МИР»
   332	2
   333	VISA International Service Association
   334	3
   335	MasterCard (MasterCard, MasterCard Electronic, Maestro)
   336	4. Сроки оказания Услуг: Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее.
   337	5. Условия оказания услуг:
   338	Комиссия за предоставление терминалов- отсутствует.
   339	Абонентская плата за пользование терминалами - отсутствует.
   340	Терминалы Исполнителя должны иметь возможность принятия бесконтактной оплаты
   341	Возможность вывода QR-кода для безналичной оплаты на дисплей терминала
   342	Расчеты при совершении операций производятся в валюте Российской Федерации.
   343	Возмещение Заказчику денежных средств по операциям:
   344	- производится путем перечисления денежных средств на номер банковского счета, входящего в состав единого казначейского счета
   345	-на основании полученной от Заказчика расчетной информации, переданной от электронного терминала Исполнителю, не позднее 2 (двух) рабочих дней с даты ее получения перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты.
   346	Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.
   347	Требования к характеристикам услуг.
   348	Исполнитель должен будет:
   349	установить и подключить к рабочим местам Заказчика бесплатно во временное пользование на весь срок действия контракта необходимое оборудование;
   350	POS-терминалы, подбор которых осуществляет Исполнитель в соответствии с описанием объекта закупки;
   351	проводить дополнительный инструктаж сотрудников Заказчика в случае изменений порядка проведения операций с использованием банковских карт, изменения программного обеспечения, замены электронного терминала на другой вид, а также в иных случаях по письменному или устному запросу Заказчика;
   352	по Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается. В этом случае плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается;
   353	Для передачи в Банк информации о совершенных в течение дня Операциях на Электронном терминале ежедневно, не позднее 23.59.59 Московского времени, работник ТСТ должен выполнить следующие действия:
   354	a) распечатать Контрольную ленту Электронного терминала;
   355	b) инициировать закрытие смены в ККТ (в случае если Электронный терминал работает под управлением ККТ) или выбрать в меню Электронного терминала «Служебные операции» - «Сверка итогов»;
   356	c) подтвердить выбор операции «Сверка итогов» нажатием клавиши «ВВОД»;
   357	d) распечатать Сводный чек Электронного терминала, передать Контрольную ленту и чеки ответственному работнику ТСТ для хранения.
   358	e) После проведения операции «Сверка итогов» список Операций сохраняется в памяти Электронного терминала до момента проведения следующей операции (включая «Сверку итогов»). При этом список операций обнуляется, и печать отчетов по проведенным ранее операциям станет невозможным.
   359	9.2.1 в случае несовпадения итогов или технического сбоя работник ТСТ:
   360	a) распечатывает Контрольную ленту;
   361	b) проверяет соответствие информации в Контрольной ленте с реально проведенными Операциями;
   362	c) ставит свою подпись на Контрольной ленте и передает ее ответственному работнику ТСТ.;
   363	Подключить ежедневную/еженедельную/ежемесячную (выбрать необходимую периодичность)  автоотчетность по успешно проведенным операциям на электронных терминалах  и направлять на электронную почту(ы) Заказчика _________;
   364	Объем услуг по сопровождению системы эквайринга:
   365	№п/п
   366	Наименование услуг
   367	Количество
   368	1
   369	Консультации персонала Заказчика по работе POS-терминала и сопровождение проведения операции на POS-терминале в телефонном режиме, на первом уровне поддержки (на «горячей линии»)
   370	Неограниченное
   371	2
   372	Замена, устранение ошибок, мелкосрочный ремонт, возобновление работоспособности POS-терминала (время реакции – в течение двух рабочих дней со дня подачи заявки).
   373	Неограниченное
   374	3
   375	Инструктаж персонала Заказчика в момент установки POS-терминала, далее по просьбе Заказчика
   376	Неограниченное
   377	4
   378	Инструктаж Заказчика информационными материалами, необходимыми для проведения операций с использованием банковских карт
   379	Неограниченное
   380	Приложение № 1.1
   381	к Контракту на проведение расчетов по операциям оплаты товаров/услуг
   382	с условием постоплаты оказанных Банком услуг
   383	ЗАЯВЛЕНИЕ ПРЕДПРИЯТИЯ НА ПРОВЕДЕНИЕ РАСЧЕТОВ ПО ОПЕРАЦИЯМ ОПЛАТЫ ТОВАРОВ/УСЛУГ
   384	1. СВЕДЕНИЯ О ПРЕДПРИЯТИИ
   385	Наименование:  ______________________________
   386	(указывается полное наименование в соответствии с учредительными документами)
   387	ИНН: КПП:
   388	КБК:  ОКАТО:
   389	Род деятельности Предприятия:
   390	р/с  к/с
   391	БИК  010349101
   392	АДРЕС РЕГИСТРАЦИИ
   393	(указывается адрес по месту государственной регистрации Предприятия)
   394	(указывается фактический (почтовый) адрес Предприятия (в случае отличия от адреса регистрации))
   395	Контактный телефон:
   396	e-mail:                                            e-mail:
   397	(e-mail для получения корреспонденции)                             (e—mail для запросов по финансовым операциям)
   398	2. ИНФОРМАЦИЯ ОБ УСЛУГАХ
   399	¨ Торговый эквайринг + Электронный терминал + QR-код
   400	¨ Интернет-эквайринг + SberPay Online + Платежные решения:
Tool:    201	 },
   202	 {
   203	  "number":"2.6.2.2",
   204	  "enriched_text":"Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и\/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору.",
   205	  "required_type":"mandatory",
   206	  "main_idea":"ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия",
   207	  "only_for_product":"trade_acquiring",
   208	  "only_for_lot":"common",
   209	  "only_for_terminal":"common",
   210	  "topics":[
   211	   "возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ",
   212	   "подключение динамического QR-кода зависит от ПО ККТ",
   213	   "при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора",
   214	   "первая операция оплаты QR-кодом активирует услугу",
   215	   "Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора",
   216	   "подключение QR-кода производится согласно Приложениям №1 и №1.1"
   217	  ],
   218	  "payment_method":"qr"
   219	 },
   220	 {
   221	  "number":"2.6.3.1",
   222	  "enriched_text":"Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: →  QR-код подключается при установке Электронного терминала в ТСТ;",
   223	  "required_type":"mandatory",
   224	  "main_idea":"Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке",
   225	  "only_for_product":"trade_acquiring",
   226	  "only_for_lot":"common",
   227	  "only_for_terminal":"common",
   228	  "topics":[
   229	   "QR-код подключается при установке Электронного терминала в ТСТ"
   230	  ],
   231	  "payment_method":"qr"
   232	 },
   233	 {
   234	  "number":"2.6.3.2",
   235	  "enriched_text":"Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора.",
   236	  "required_type":"mandatory",
   237	  "main_idea":"Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк",
   238	  "only_for_product":"trade_acquiring",
   239	  "only_for_lot":"common",
   240	  "only_for_terminal":"common",
   241	  "topics":[
   242	   "отключение QR-кода возможно по инициативе Предприятия",
   243	   "инициатива отключения реализуется через обращение в Банк"
   244	  ],
   245	  "payment_method":"qr"
   246	 },
   247	 {
   248	  "number":"2.7",
   249	  "enriched_text":"Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юридическую силу с Договором, оформленным на бумажном носителе, подписанным собственноручными подписями уполномоченных представителей Банка и Предприятия.",
   250	  "required_type":"optional",
   251	  "main_idea":"Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП ",
   252	  "only_for_product":"common",
   253	  "only_for_lot":"common",
   254	  "only_for_terminal":"common",
   255	  "topics":[
   256	
   257	  ],
   258	  "payment_method":"common"
   259	 },
   260	 {
   261	  "number":"3.1",
   262	  "enriched_text":"«ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары\/услуги с использованием Карты\/ее реквизитов\/NFC-карты\/SberPay\/Плати QR в ТСТ\/на Ресурсе и обработку информации на Электронных терминалах\/Смарт-терминалах [1]\/через СПЭП. Перечень Карт перечислен в Порядке проведения операций в Торгово-сервисных точках\/на Ресурсе к Договору, размещенном на Официальном сайте Банка",
   263	  "required_type":"optional",
   264	  "main_idea":"Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР",
   265	  "only_for_product":"common",
   266	  "only_for_lot":"common",
   267	  "only_for_terminal":"common",
   268	  "topics":[
   269	   "Предприятие обязано организовать приём оплаты за Товары\/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Плати QR)",
   270	   "Приём оплаты осуществляется в ТСТ (торгово-сервисных точках) и\/или на Ресурсе (сайт\/приложение Предприятия)",
   271	   "Обработка информации производится через Электронные терминалы, Смарт-терминалы или СПЭП",
   272	   "Перечень допустимых к приёму Карт"
   273	  ],
   274	  "payment_method":"common"
   275	 },
   276	 {
   277	  "number":"3.2",
   278	  "enriched_text":"«ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров\/услуг в ТСТ\/на Ресурсе.",
   279	  "required_type":"optional",
   280	  "main_idea":"Важен сам факт обязанности Банка в перечислении сумм Предприятию",
   281	  "only_for_product":"common",
   282	  "only_for_lot":"common",
   283	  "only_for_terminal":"common",
   284	  "topics":[
   285	   "Банк обязан перечислять суммы операций оплаты товаров\/услуг Предприятию"
   286	  ],
   287	  "payment_method":"common"
   288	 },
   289	 {
   290	  "number":"3.3",
   291	  "enriched_text":"«ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров\/услуг в ТСТ[7]\/на Ресурсе – к ИЭ[8]",
   292	  "required_type":"mandatory",
   293	  "main_idea":"Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору",
   294	  "only_for_product":"common",
   295	  "only_for_lot":"common",
   296	  "only_for_terminal":"common",
   297	  "topics":[
   298	   "Предприятие перечисляет Банку плату за проведение расчётов ежемесячно"
   299	  ],
   300	  "payment_method":"common"
   301	 },
   302	 {
   303	  "number":"4.1.1",
   304	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров\/услуг с использованием Карт\/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3.1 и п. 2.3.2 настоящего Договора.",
   305	  "required_type":"optional",
   306	  "main_idea":"Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком",
   307	  "only_for_product":"common",
   308	  "only_for_lot":"common",
   309	  "only_for_terminal":"common",
   310	  "topics":[
   311	   "Предприятие имеет право ссылаться на возможность оплаты с использованием Карт\/QR-кода после согласования материалов с Банком",
   312	   "Согласование информационных материалов осуществляется в соответствии с пунктами 2.3.1 и 2.3.2"
   313	  ],
   314	  "payment_method":"qr"
   315	 },
   316	 {
   317	  "number":"4.1.2",
   318	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов\/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, указанному в п.2 Порядка проведения операций в Торгово-сервисных точках\/на Ресурсе.",
   319	  "required_type":"optional",
   320	  "main_idea":"Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования",
   321	  "only_for_product":"common",
   322	  "only_for_lot":"common",
   323	  "only_for_terminal":"common",
   324	  "topics":[
   325	   "закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов\/Смарт-терминалов",
   326	   "закреплено право Заказчика на получение консультаций по проведению Операций"
   327	  ],
   328	  "payment_method":"common"
   329	 },
   330	 {
   331	  "number":"4.1.3",
   332	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров\/услуг по SberPayQR\/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Мобильных устройствах Предприятия, а также на ККТ, принадлежащей Предприятию, или на видном месте, в том числе на бумажном носителе.",
   333	  "required_type":"optional",
   334	  "main_idea":"Важен сам факт, что QR выдаёт Банк",
   335	  "only_for_product":"trade_acquiring",
   336	  "only_for_lot":"common",
   337	  "only_for_terminal":"common",
   338	  "topics":[
   339	   "Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR\/Плати QR"
   340	  ],
   341	  "payment_method":"qr_sber_pay"
   342	 },
   343	 {
   344	  "number":"4.2.1",
   345	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настоящего Договора. ",
   346	  "required_type":"mandatory",
   347	  "main_idea":"Важен факт, что предприятие обязуется оплачивать услуги",
   348	  "only_for_product":"common",
   349	  "only_for_lot":"common",
   350	  "only_for_terminal":"common",
   351	  "topics":[
   352	   "Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям",
   353	   "Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена)"
   354	  ],
   355	  "payment_method":"common"
   356	 },
   357	 {
   358	  "number":"4.2.2",
   359	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных\/ инструктивных материалах, предоставляемых Банком.",
   360	  "required_type":"optional",
   361	  "main_idea":"Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее нет, то пункты не относятся к теме матрицы",
   362	  "only_for_product":"common",
   363	  "only_for_lot":"common",
   364	  "only_for_terminal":"common",
   365	  "topics":[
   366	   "Обязанность Предприятия соблюдать положения Договора (наличие формулировки об обязанности соблюдать)",
   367	   "Обязанность Предприятия выполнять требования, содержащиеся в информационных \/ инструктивных материалах, предоставляемых Банком (наличие формулировки об обязанности выполнять)"
   368	  ],
   369	  "payment_method":"common"
   370	 },
   371	 {
   372	  "number":"4.2.3",
   373	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление Предприятия с изменениями, внесенными в вышеуказанные документы, не является основанием для их неприменения Банком.",
   374	  "required_type":"optional",
   375	  "main_idea":"",
   376	  "only_for_product":"common",
   377	  "only_for_lot":"fz_223",
   378	  "only_for_terminal":"common",
   379	  "topics":[
   380	   "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов",
   381	   "Несвоевременное ознакомление не является основанием для неприменения изменений"
   382	  ],
   383	  "payment_method":"common"
   384	 },
   385	 {
   386	  "number":"4.2.4",
   387	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]\/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров\/услуг с использованием Карт\/NFC-карт\/SberPay\/Плати QR, в случае если это не противоречит требованиям законодательства Российской Федерации.",
   388	  "required_type":"optional",
   389	  "main_idea":"Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте",
   390	  "only_for_product":"common",
   391	  "only_for_lot":"common",
   392	  "only_for_terminal":"common",
   393	  "topics":[
   394	   "Предприятие обязано размещать информационные материалы Банка о способах оплаты",
   395	   "Размещение материалов осуществляется в случае отсутствия противоречий с законодательством РФ"
   396	  ],
   397	  "payment_method":"common"
   398	 },
   399	 {
   400	  "number":"4.2.5",
AI: Let me continue reading the remaining parts of both files and the working artifacts.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 400, 'limit': 200}, 'id': 'call_00_1InpIxvwKcAKLn99uFop6349', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 400, 'limit': 200}, 'id': 'call_01_7zoB2nGW2YQbE5IdO7Qk9783', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 200}, 'id': 'call_02_YoulPZhHqDT1wYv379ys3148', 'type': 'tool_call'}]
Tool:    401	¨ Интернет сайт                    http://__________
   402	¨ Мобильное приложение   http://__________
   403	¨ SberPay Online
   404	¨ Интернет сайт                    http://__________
   405	¨ Мобильное приложение   http://__________
   406	¨ QR-код
   407	¨ Торговый автомат
   408	¨ Торговый эквайринг + Cмарт-терминал + QR-код
   409	Смарт-терминал: ¨ Смарт - POS; Х  Эвотор+
   410	3. ПОДТВЕРЖДЕНИЕ ЗАКЛЮЧЕНИЯ КОНТРАКТА
   411	1.1. Подтверждает, что вся информация, указанная в настоящем Заявлении, предоставленных Предприятием документах, а также в Информационных сведениях Предприятия, является полной и достоверной.
   412	1.2. Согласно, что Банк имеет право проверить сведения, указанные в настоящем Заявлении и предоставленных документах.
   413	1.3. Предоставляет Банку согласие (заранее данный акцепт) на списание со счета, указанного в настоящем Заявлении, без дополнительных распоряжений сумм, перечисленных в п.5.1.1 Контракта, при невозможности удержать указанные суммы из сумм, подлежащих последующему перечислению Предприятию.
   414	МП Предприятия
   415	ПОДПИСЬ\ФИО ___________________ДАТА ____________________
   416	(указывается ФИО руководителя/уполномоченного представителя Предприятия/доверенного лица Предприятия)
   417	4. ОТМЕТКИ БАНКА
   418	_______________________
   419	______________________________________ ______________________________________
   420	(указывается номер/наименование, место нахождения ГОСБ по месту оформления Контракта)
   421	Банк получателя ____________ БИК Банка получателя ____________Счет № Банка получателя ____________________
   422	ИНН 7707083893         КПП_____________________________________
   423	Банк  подтверждает факт заключения Контракта № ___________________________ от «______» ________20______г.
   424	¨ Копия документа, удостоверяющего личность руководителя Предприятия / уполномоченного представителя Предприятия / доверенного лица Предприятия
   425	¨ СНИЛС
   426	¨ В заключении Контракта отказал
   427	«_____» __________ 20____г. _____________________________________________________________________                ___________________________
   428	(указывается должность уполномоченного работника Банка на заключение/внесение изменений в Контракта)                       (подпись/Фамилия, И.О.)
   429	Приложение № 1..2
   430	к Контракту на проведение расчетов по операциям оплаты товаров/услуг
   431	с условием постоплаты оказанных Банком услуг
   432	ИНФОРМАЦИЯ О ТОРГОВО-СЕРВИСНОЙ ТОЧКЕ/РЕСУРСЕ ПРЕДПРИТИЯ
   433	_________________________
   434	Наименование Предприятия
   435	ИНН
   436	Название ТСТ (указывается название как на уличной/витринной вывеске ТСТ, не более 20 знаков)
   437	Номер и дата свидетельства о регистрации
   438	Фактический адрес
   439	Индекс
   440	Субъект РФ Краснодарский край
   441	Город Сочи
   442	Улица
   443	Дом  Корпус / Строение ___
   444	Квартира/Офис/Помещение __________________
   445	Время работы
   446	Понедельник – пятница
   447	Суббота                             не работает
   448	Воскресенье                      не работает
   449	Род деятельности (четко указывается вид предоставляемой услуги)
   450	История приема карт
   451	☐ Новая ☐ Перерегистрация ☐ Ранее использовали оборудование другого банка
   452	Средний чек
   453	10 000
   454	Телефон для отражения в чеке
   455	нет
   456	Контактные данные администратора (в том числе для направления паролей и кодов подтверждения для настройки Смарт-терминала)
   457	Телефон
   458	E-mail
   459	Контактные данные для личного кабинета  Оператора фискальных данных (ОФД)
   460	Телефон
   461	E-mail
   462	Телефон IT- специалиста
   463	Дополнительные сервисы проведения операции
   464	☐ проведение операций без предъявления карты на основании распоряжения держателя карты
   465	☐ проведение повторяющихся платежей без предъявления карты на основании распоряжения держателя карты
   466	☐ проведение операций с биометрическим методом идентификации
   467	☐ отмена операции оплаты в режиме онлайн
   468	ТОРГОВЫЙ ЭКВАЙРИНГ
   469	Электронные терминалы (без учета mPOS)
   470	.
   471	Тип подключения Электронных терминалов
   472	☐ выделенная линия (Ethernet)______шт. ☐ WI-FI_____шт. ☐ GPRS ______шт.
   473	☐ Банк -Вендор
   474	☐ ИКР – касса с кассиром
   475	☐ ИКР – касса самообслуживания
   476	☐ Мобильные терминалы (mPOS)
   477	☐ Биометрические терминалы
   478	IP-адрес терминала для Ethernet-терминала
   479	IP                           маска.                        шлюз
   480	☐ Мобильное устройство Предприятия
   481	_________шт.
   482	Номер мобильного телефона для авторизации Мобильного устройства Предприятия
   483	+7 987 847 44 87
   484	Смарт-терминал Банка
   485	Тип терминала
   486	(Количество Смарт-терминалов должно равняться количеству ФН при тарифе «Максимальный»)
   487	Количество
   488	ФН-36 для пакета «Максимальный», шт.
   489	Количество
   490	ФН-15 для пакета «Максимальный»,  шт.
   491	Пакет
   492	☐ Смарт- POS;
   493	☐ aQsi ____ шт.
   494	☐ нет сканера;
   495	☐ 2D сканер беспроводной
   496	☐ Начальный
   497	☐ Максимальный
   498	Салют 12Ф ____ шт.
   499	☐ нет сканера;
   500	☐ 2D сканер беспроводной
   501	☐ Эвотор 5I _ шт.
   502	☐ нет сканера;
   503	☐ 2D сканер беспроводной
   504	☐ 2D сканер проводной
   505	☐ Эвотор+
   506	☐ СТ-7.2, ______шт.
   507	☐ нет сканера;
   508	☐ 2D сканер беспроводной;
   509	☐ 2D сканер проводной
   510	☐ СТ-7.3,     3      шт.
   511	☐ нет сканера;
   512	☐ 2D сканер беспроводной;
   513	☐ 2D сканер проводной
   514	☐ СТ-5, ______шт.
   515	☐ нет сканера;
   516	☐ 2D сканер беспроводной;
   517	☐ 2D сканер проводной
   518	☐ СТ-10, ______шт.
   519	☐ нет сканера;
   520	☐ 2D сканер беспроводной;
   521	☐ 2D сканер проводной
   522	Смарт-терминал Предприятия
   523	☐ Эвотор 5i_ шт.
   524	Продажа акцизных товаров для тарифа «Максимальный»
   525	☐ Да        ☐ Нет
   526	☐ Слабоалкогольная продукция    ☐ Крепкий алкоголь   ☐ Табак
   527	☐ Другое (укажите тип товара): _______
   528	Режим (система) налогообложения, в случае использования нескольких систем – указать, в том числе, основной режим для тарифа «Максимальный»
   529	☐ УСН: Доходы                           ☐ ОСНО торговля; ☐ ОСНО услуги;
   530	☐ УСН: Доходы-Расходы
   531	☐ ЕСХН                                       ☐ Патент (только для ИП)
   532	Режим работы Смарт -терминала
   533	☐ online                                ☐ offline (не отправляет данные в ФНС)
   534	Контрольно-кассовая техника используется для развозной и (или) разносной торговли (оказания услуг, выполнения работ)
   535	☐ Да                   ☐ Нет
   536	Контрольно-кассовая техника применяется только при оказании услуг
   537	☐ Да                   ☐ Нет
   538	Сезонная деятельность
   539	☐ Да                   ☐ Нет
   540	Контрольно-кассовая техника используется при осуществлении деятельности платежного агента (субагента)
   541	☐ Да                   ☐ Нет
   542	Контрольно-кассовая техника применяется для продаж маркированных товаров
   543	☐ Да                   ☐ Нет
   544	☐ ИНТЕРНЕТ ЭКВАЙРИНГ
   545	Альтернативные способы приема оплаты
   546	☐ Социальные сети ☐ Мессенджеры
   547	☐ QR-код
   548	_____________шт.
   549	Номер наклейки для QR-кода
   550	_______; _________;________.
   551	Типы подключения QR- кода
   552	☐ QR-API
   553	☐ QR-Вендор. Типы вендоров:
   554	☐ Эвотор        Серийный №_________________
   555	☐ Смарт-POS
   556	☐ Кристалл
   557	☐ Другие ________________
   558	ТОРГОВЫЙ АВТОМАТ
   559	☐ Торговый автомат с максимальной суммой операции выше 1000 рублей ___, шт.
   560	☐ Торговый автомат с максимальной суммой операции ниже 1000 рублей ___, шт.
   561	Информацию, указанную в настоящем документе, подтверждаю
   562	_______________________________________________________ _______________ «__» ___________ 20____г.
   563	(указывается ФИО руководителя/уполномоченного представителя Предприятия)           (подпись)
   564	Отметки Банка:
   565	Заявление принял:
   566	_______________________________________________________ _______________ «__» ___________ 20____г.
   567	(указывается ФИО работника Банка)              (подпись)
   568	Заказчик:
   569	ФГБУ «Кавказский государственный  заповедник»
   570	От «Банка/Исполнителя»:
   571	Приложение № 2
   572	к контракту на оказание услуг
   573	от _____________ № _______
   574	СПЕЦФИКАЦИЯ
   575	№ п/п
   576	Наименование услуг
   577	Ед. изм.
   578	Цена за единицу, руб.
   579	размер комиссии, % (цена в процентном соотношении)
   580	Максимальное значение цены контракта, руб.
   581	1
   582	Услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)
   583	тыс.руб.
   584	1 900 000,00
   585	Максимальное значение цены контракта, руб.
   586	1 900 000,00
   587	Заказчик:
   588	ФГБУ «Кавказский государственный  заповедник»
   589	От «Банка/Исполнителя»:
Tool:    401	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров\/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках\/на Ресурсе, в течение всего рабочего времени Предприятия. Не выдавать по Картам наличные денежные средства[3]. Не принимать от Покупателя более 2 (двух) различных Карт.",
   402	  "required_type":"mandatory",
   403	  "main_idea":"Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства",
   404	  "only_for_product":"common",
   405	  "only_for_lot":"common",
   406	  "only_for_terminal":"common",
   407	  "topics":[
   408	   "Принимать к оплате все карты из списка в течение всего рабочего времени",
   409	   "Не выдавать наличные деньги по картам",
   410	   "Не принимать более двух разных карт от одного покупателя"
   411	  ],
   412	  "payment_method":"common"
   413	 },
   414	 {
   415	  "number":"4.2.6",
   416	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм.",
   417	  "required_type":"mandatory",
   418	  "main_idea":"Важен сам факт, что нельзя разбивать Операцию на нескольку сумм",
   419	  "only_for_product":"common",
   420	  "only_for_lot":"common",
   421	  "only_for_terminal":"common",
   422	  "topics":[
   423	   "Предприятие обязано проводить Операцию оплаты единой суммой без разделения на части"
   424	  ],
   425	  "payment_method":"common"
   426	 },
   427	 {
   428	  "number":"4.2.7",
   429	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не использовать реквизиты Карты\/Платежного счета, которые стали доступны Предприятию\/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупателя.",
   430	  "required_type":"mandatory",
   431	  "main_idea":"",
   432	  "only_for_product":"common",
   433	  "only_for_lot":"common",
   434	  "only_for_terminal":"common",
   435	  "topics":[
   436	   "Не использовать реквизиты Карты без присутствия или распоряжения Покупателя",
   437	   "Использовать реквизиты Карты только для проведения операций"
   438	  ],
   439	  "payment_method":"common"
   440	 },
   441	 {
   442	  "number":"4.2.8",
   443	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять Покупателям полный набор Товаров\/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства.",
   444	  "required_type":"mandatory",
   445	  "main_idea":"Важно, что цена не зависит от способа оплаты",
   446	  "only_for_product":"common",
   447	  "only_for_lot":"common",
   448	  "only_for_terminal":"common",
   449	  "topics":[
   450	   "Предприятие предоставляет полный набор товаров\/услуг покупателям",
   451	   "цены для расчетов с использованием банковской карты не превышают цены за наличный расчет"
   452	  ],
   453	  "payment_method":"common"
   454	 },
   455	 {
   456	  "number":"4.2.9",
   457	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций в Торгово-сервисных точках\/на Ресурсе к Договору и нести ответственность за правильность указанной в документах информации.",
   458	  "required_type":"mandatory",
   459	  "main_idea":"Заказчик несет ответственность за информацию которую он указывает в документах при проведении платежей",
   460	  "only_for_product":"common",
   461	  "only_for_lot":"common",
   462	  "only_for_terminal":"common",
   463	  "topics":[
   464	   "Предприятие обязано проводить операции в соответствии с Порядком проведения операций",
   465	   "Предприятие обязано оформлять документы по операциям в соответствии с Порядком проведения операций",
   466	   "Предприятие несет ответственность за корректность информации в документах по операциям"
   467	  ],
   468	  "payment_method":"common"
   469	 },
   470	 {
   471	  "number":"4.2.10",
   472	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Хранить в недоступном для третьих лиц месте Документы по операциям (Чеки, кассовые чеки, распоряжения Покупателя, документы, подтверждающие факт заключения договора и проведения каждой Операции при проведении Повторяющихся платежей, документы, подтверждающие факт передачи Товара\/оказания услуги и т.п.) не менее 13 (тринадцати) месяцев с даты совершения Операции и передавать их копии в Банк по его запросу путем направления ответа на первоначальный запрос по электронным каналам связи, указанным в п.2.3.1., п.2.3.2. Договора в течение 3 (трех) рабочих дней с даты получения запроса. Предоставленные документы должны быть надлежащего качества (изображение четкое, размер не менее оригинального документа). ",
   473	  "required_type":"mandatory",
   474	  "main_idea":"Важен факт необходимости хранения документы по операциям, срок в течении которого их нужно хранить, факт передачи копий по опревцияс, а так же срок в течение которого обязаны их передать",
   475	  "only_for_product":"common",
   476	  "only_for_lot":"common",
   477	  "only_for_terminal":"common",
   478	  "topics":[
   479	   "хранение документов по операциям (сам факт хранения и срок храннеия)",
   480	   "передача копий документов Банку в течение 3 рабочих дней",
   481	   "надлежащее качество предоставленных документов"
   482	  ],
   483	  "payment_method":"common"
   484	 },
   485	 {
   486	  "number":"4.2.11",
   487	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Передавать в Банк по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Банка письменное заявление с изложением обстоятельств проведения Операции в ТСТ \/на Ресурсе . В случае утраты составленных Документов по операции немедленно сообщить об утрате в Банк одним из способов, указанных в п. 2.3.1, п. 2.3.2 Договора. ",
   488	  "required_type":"mandatory",
   489	  "main_idea":"Важен факт обязанности передавать заявление Банку, а так же сроки в течение которых оно должно быть передано",
   490	  "only_for_product":"common",
   491	  "only_for_lot":"common",
   492	  "only_for_terminal":"common",
   493	  "topics":[
   494	   "Передача заявления в банк с изложением обстоятельств проведения Операции в течение 3 рабочих дней после получения запроса",
   495	   "немедленное уведомление банка об утрате документов"
   496	  ],
   497	  "payment_method":"common"
   498	 },
   499	 {
   500	  "number":"4.2.12",
   501	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг, в течение 5 (пяти) рабочих дней с даты их выставления.",
   502	  "required_type":"optional",
   503	  "main_idea":"Важен факт обязанности Предприятия подписать закрывающие документы по оплате, а так же сроки в течение которых оно должно это сделать",
   504	  "only_for_product":"common",
   505	  "only_for_lot":"common",
   506	  "only_for_terminal":"common",
   507	  "topics":[
   508	   "Предприятие обязано акцептовать платежные требования и счета на оплату. Пункт относится только к оплате счетов",
   509	   "Срок оплаты платежных требований и счетов"
   510	  ],
   511	  "payment_method":"common"
   512	 },
   513	 {
   514	  "number":"4.2.13",
   515	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере:\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка в пользу Банка-эмитента либо уплачены Банком Банку-эмитенту и (или) Держателям карт, эмитированных Банком, по Операциям :\n- ставшим предметом каких-либо споров и разногласий в соответствии с законодательством Российской Федерации и (или) в соответствии с правилами Платежной системы;\n- являющимся недействительными в соответствии с Договором;\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка либо уплачены Банком в связи с рассмотрением споров и разногласий между Покупателями и Предприятием касательно Операций, указанных в настоящем пункте Договора, в том числе любые сборы, комиссии, платы и (или) иные расходы Банка, связанные с рассмотрением споров и разногласий по таким Операциям;\n• убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с законодательством Российской Федерации и (или) правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору.",
   516	  "required_type":"mandatory",
   517	  "main_idea":"Важен сам факт обязанности Предприятия возмещать все суммы и убытки, которые Банк понёс из-за Предприятия, все возмещения - в полном объеме. Сранвнить случаи в которых возникает обязанность в возмещении",
   518	  "only_for_product":"common",
   519	  "only_for_lot":"common",
   520	  "only_for_terminal":"common",
   521	  "topics":[
   522	   "возмещение средств, списанных со счета Банка в пользу Банка-эмитента или Держателей карт",
   523	   "возмещение средств, уплаченных Банком Банку-эмитенту или Держателям карт",
   524	   "возмещение средств при спорах и разногласиях по операциям",
   525	   "возмещение сборов, комиссий и расходов Банка при рассмотрении споров",
   526	   "возмещение убытков Банка от штрафных санкций и ответственности"
   527	  ],
   528	  "payment_method":"common"
   529	 },
   530	 {
   531	  "number":"4.2.14",
   532	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В случае реорганизации, внесения изменений и дополнений в документы, представленные Предприятием при заключении Договора, при открытии в отношении Предприятия\/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса местонахождения Предприятия\/ТСТ, внесенного в ЕГРЮЛ, реквизитов Предприятие\/ТСТ обязуется информировать Банк и передать (по месту заключения Договора) надлежащим образом заверенные и оформленные документы, подтверждающие внесение изменений и дополнений одним из способов, указанных в п. 2.3 Договора, не позднее 3 (трех) рабочих дней с даты дополнений\/изменений. ",
   533	  "required_type":"mandatory",
   534	  "main_idea":"Важен факт предоставления подтверждающих документов, важны сроки предоставления, а так же нужно сравнить события, при которых это допустимо",
   535	  "only_for_product":"common",
   536	  "only_for_lot":"common",
   537	  "only_for_terminal":"common",
   538	  "topics":[
   539	   "информирование Банка о реорганизации предприятия в течение 3 рабочих дней",
   540	   "уведомление об изменениях документов в течение 3 рабочих дней",
   541	   "сообщение об открытии или смене стадии банкротства в течение 3 рабочих дней",
   542	   "предоставление сведений о смене руководства в течение 3 рабочих дней",
   543	   "оповещение об изменении адреса нахождения в течение 3 рабочих дней",
   544	   "передача информации об изменении реквизитов в течение 3 рабочих дней"
   545	  ],
   546	  "payment_method":"common"
   547	 },
   548	 {
   549	  "number":"4.2.15",
   550	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять в Банк достоверные документы и сведения, необходимые Банку для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе, но не исключительно: не реже одного раза в год, а также по отдельному запросу Банка в течение 7 (семи) рабочих дней со дня получения запроса обновлять сведения и документы, представленные Банку при заключении настоящего Договора, включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации Предприятия, а также сведения о своих представителях, выгодоприобретателях и бенефициарных владельцах (при наличии).",
   551	  "required_type":"mandatory",
   552	  "main_idea":"Важен факт необходимости предоставлять достоверные сведения, своевременное обновление сведений. Важен факт и срок периодичного предоставления. Важен факт и срок предоставления по запросу",
   553	  "only_for_product":"common",
   554	  "only_for_lot":"common",
   555	  "only_for_terminal":"common",
   556	  "topics":[
   557	   "Предприятие обязано предоставлять документы не реже одного раза в год",
   558	   "Предприятие обязано предоставлять сведения по запросу Банка в течение 7 рабочих дней",
   559	   "Сведения о целях финансово-хозяйственной деятельности",
   560	   "Информация о финансовом положении предприятия",
   561	   "Данные о деловой репутации предприятия",
   562	   "Сведения о представителях предприятия",
   563	   "Информация о выгодоприобретателях",
   564	   "Сведения о бенефициарных владельцах (если имеются)"
   565	  ],
   566	  "payment_method":"common"
   567	 },
   568	 {
   569	  "number":"4.2.16.1",
   570	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) руководителя Предприятия, указанные в Заявлении\/Информации о ТСТ: → Предприятие гарантирует наличие правовых оснований на передачу в Банк персональных данных руководителя Предприятия, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные в целях, указанных в п.5.1.7 Договора. Предприятие обязано уведомить Банк о прекращении правовых оснований на обработку ПДн руководителя Предприятия, указанных в настоящем пункте Договора.\n",
   571	  "required_type":"mandatory",
   572	  "main_idea":"Важно, чтобы было действующее согласие на передачу ПДн руководителя Предприятия.  Состав ПДн: ФИО, адрес, паспортные данные. Важно, чтобы не была предусмотрена передача данных другим лицам \/ системам",
   573	  "only_for_product":"common",
   574	  "only_for_lot":"common",
   575	  "only_for_terminal":"common",
   576	  "topics":[
   577	   "Предприятие гарантирует наличие правовых оснований на передачу ПДн",
   578	   "Предприятие передает ФИО руководителя",
   579	   "Предприятие передает адрес руководителя",
   580	   "Предприятие передает паспортные данные руководителя",
   581	   "Обязанность уведомления Банка о прекращении правовых оснований обработки ПДн"
   582	  ],
   583	  "payment_method":"common"
   584	 },
   585	 {
   586	  "number":"4.2.16.2",
   587	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) сотрудников Предприятия: → Предприятие гарантирует наличие согласий на обработку Банком персональных данных своих работников, состав которых включает: ФИО, мобильный телефон, электронная почта, должность и место работы, а также на их дальнейшую передачу в Обслуживающие компании, действующие от лица Банка, необходимых для целей заключения и исполнения настоящего Договора. Договора. Предприятие обязуется предоставить подтверждение наличия согласий по письменному запросу Банка в соответствии с пунктом 4.2.16.3 Договора.",
   588	  "required_type":"mandatory",
   589	  "main_idea":"Важно, что данный пункт относится ко всем сотрудникам кроме руководителя, важно наличие согласий, обязанность подтвердить наличие согласий, важен состав ПДн",
   590	  "only_for_product":"common",
   591	  "only_for_lot":"common",
   592	  "only_for_terminal":"common",
   593	  "topics":[
   594	   "Предприятие гарантирует наличие согласий сотрудников(кроме руководтитела) на обработку его персональных данных",
   595	   "Состав персональных данных сотрудников (кроме руководителя)"
   596	  ],
   597	  "payment_method":"common"
   598	 },
   599	 {
   600	  "number":"4.2.16.3",
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предостав",
     7	      "type": "operative",
     8	      "materiality": "evaluable",
     9	      "protected_party": "Bank",
    10	      "bound_party": "Enterprise",
    11	      "right_or_obligation": "right",
    12	      "legal_object": "TST registration; terminal equipment; payment; refusal right",
    13	      "trigger": "TST registration request; change in TST information; connection of additional equipment",
    14	      "deadline": "",
    15	      "amount_formula_cap": "",
    16	      "procedure_channel": "",
    17	      "liability_remedy": "refusal right",
    18	      "scope_options": [],
    19	      "consequence": "registration may be refused",
    20	      "applicability_filters": {
    21	        "required_type": "mandatory",
    22	        "only_for_product": "common",
    23	        "only_for_lot": "common",
    24	        "only_for_terminal": "common",
    25	        "payment_method": "common"
    26	      },
    27	      "main_idea": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
    28	      "topics": [
    29	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    30	        "Банк может отказать в регистрации ТСТ без указания причины",
    31	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    32	        "Информация о новых устройствах предоставляется с указанием их количества"
    33	      ],
    34	      "enriched_text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора.\nПри изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров."
    35	    },
    36	    {
    37	      "id": "2.2",
    38	      "source_text": "Важен факт, что валюта рубль РФ, другая валюта недопустима Расчёты производятся в рублях Российской Федерации Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    39	      "source_excerpt": "Важен факт, что валюта рубль РФ, другая валюта недопустима Расчёты производятся в рублях Российской Федерации Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    40	      "type": "operative",
    41	      "materiality": "evaluable",
    42	      "protected_party": "Both",
    43	      "bound_party": "Both",
    44	      "right_or_obligation": "obligation",
    45	      "legal_object": "settlement currency",
    46	      "trigger": "ongoing/upon event",
    47	      "deadline": "",
    48	      "amount_formula_cap": "",
    49	      "procedure_channel": "",
    50	      "liability_remedy": "",
    51	      "scope_options": [],
    52	      "consequence": "legal effect as specified",
    53	      "applicability_filters": {
    54	        "required_type": "mandatory",
    55	        "only_for_product": "common",
    56	        "only_for_lot": "common",
    57	        "only_for_terminal": "common",
    58	        "payment_method": "common"
    59	      },
    60	      "main_idea": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    61	      "topics": [
    62	        "Расчёты производятся в рублях Российской Федерации"
    63	      ],
    64	      "enriched_text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. "
    65	    },
    66	    {
    67	      "id": "2.3.1",
    68	      "source_text": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса. Обмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту; Информация и документы, направленные по электронной почте, имеют юридическую силу Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    69	      "source_excerpt": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса. Обмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и бан",
    70	      "type": "operative",
    71	      "materiality": "evaluable",
    72	      "protected_party": "Both",
    73	      "bound_party": "Both",
    74	      "right_or_obligation": "mutual_obligation",
    75	      "legal_object": "email communication channel; payment; personal data; transaction documents",
    76	      "trigger": "upon specified condition",
    77	      "deadline": "",
    78	      "amount_formula_cap": "",
    79	      "procedure_channel": "email",
    80	      "liability_remedy": "",
    81	      "scope_options": [],
    82	      "consequence": "documents have legal force",
    83	      "applicability_filters": {
    84	        "required_type": "mandatory",
    85	        "only_for_product": "common",
    86	        "only_for_lot": "common",
    87	        "only_for_terminal": "common",
    88	        "payment_method": "common"
    89	      },
    90	      "main_idea": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    91	      "topics": [
    92	        "Обмен информацией по электронной почте",
    93	        "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
    94	        "Информация и документы, направленные по электронной почте, имеют юридическую силу"
    95	      ],
    96	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;"
    97	    },
    98	    {
    99	      "id": "2.3.2",
   100	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами посредством системы ДБО или аналогичных систем Банка Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
   101	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами посредством системы ДБО или аналогичных систем Банка Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним и",
   102	      "type": "operative",
   103	      "materiality": "evaluable",
   104	      "protected_party": "Both",
   105	      "bound_party": "Both",
   106	      "right_or_obligation": "mutual_obligation",
   107	      "legal_object": "DBO communication channel; transaction documents",
   108	      "trigger": "ongoing/upon event",
   109	      "deadline": "",
   110	      "amount_formula_cap": "",
   111	      "procedure_channel": "DBO system",
   112	      "liability_remedy": "",
   113	      "scope_options": [],
   114	      "consequence": "legal effect as specified",
   115	      "applicability_filters": {
   116	        "required_type": "mandatory",
   117	        "only_for_product": "common",
   118	        "only_for_lot": "common",
   119	        "only_for_terminal": "common",
   120	        "payment_method": "common"
   121	      },
   122	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   123	      "topics": [
   124	        "Обмен документами посредством системы ДБО или аналогичных систем Банка"
   125	      ],
   126	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;"
   127	    },
   128	    {
   129	      "id": "2.3.3",
   130	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   131	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способо",
   132	      "type": "operative",
   133	      "materiality": "evaluable",
   134	      "protected_party": "Both",
   135	      "bound_party": "Both",
   136	      "right_or_obligation": "mutual_obligation",
   137	      "legal_object": "payment; transaction documents",
   138	      "trigger": "ongoing/upon event",
   139	      "deadline": "",
   140	      "amount_formula_cap": "",
   141	      "procedure_channel": "courier",
   142	      "liability_remedy": "",
   143	      "scope_options": [],
   144	      "consequence": "legal effect as specified",
   145	      "applicability_filters": {
   146	        "required_type": "optional",
   147	        "only_for_product": "common",
   148	        "only_for_lot": "common",
   149	        "only_for_terminal": "common",
   150	        "payment_method": "common"
   151	      },
   152	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   153	      "topics": [
   154	        "Обмен документами с доставкой нарочным или курьером"
   155	      ],
   156	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
   157	    },
   158	    {
   159	      "id": "2.3.4",
   160	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами через заказное письмо Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   161	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами через заказное письмо Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемы",
   162	      "type": "operative",
   163	      "materiality": "evaluable",
   164	      "protected_party": "Both",
   165	      "bound_party": "Both",
   166	      "right_or_obligation": "mutual_obligation",
   167	      "legal_object": "payment; transaction documents",
   168	      "trigger": "ongoing/upon event",
   169	      "deadline": "",
   170	      "amount_formula_cap": "",
   171	      "procedure_channel": "registered mail",
   172	      "liability_remedy": "",
   173	      "scope_options": [],
   174	      "consequence": "legal effect as specified",
   175	      "applicability_filters": {
   176	        "required_type": "optional",
   177	        "only_for_product": "common",
   178	        "only_for_lot": "common",
   179	        "only_for_terminal": "common",
   180	        "payment_method": "common"
   181	      },
   182	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   183	      "topics": [
   184	        "Обмен документами через заказное письмо"
   185	      ],
   186	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
   187	    },
   188	    {
   189	      "id": "2.3.5",
   190	      "source_text": "Важна равнозначность документов Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП; электронные документы имеют юридическую силу документов на бумаге Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   191	      "source_excerpt": "Важна равнозначность документов Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП; электронные документы имеют юридическую силу документов на бумаге Банк и Предприятие в рамках нас",
   192	      "type": "operative",
   193	      "materiality": "evaluable",
   194	      "protected_party": "Both",
   195	      "bound_party": "Both",
   196	      "right_or_obligation": "mutual_obligation",
   197	      "legal_object": "EDI communication channel; transaction documents",
   198	      "trigger": "ongoing/upon event",
   199	      "deadline": "",
   200	      "amount_formula_cap": "",
AI: Now let me read the existing working artifacts - the clause_index, contract_product_profile, and the contract-side of legal_propositions.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json', 'limit': 100}, 'id': 'call_00_EhEBrFHZHNsPJ8wAL40j7179', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 200, 'limit': 300}, 'id': 'call_01_TrJKqZhv7zyy3s04aVzM7534', 'type': 'tool_call'}]
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos"],
     5	  "payment_method": ["cards", "qr", "nfc"],
     6	  "legal_regime": "44_fz",
     7	  "notes": "Contract is for trade acquiring (POS terminals at physical TST locations). QR code display on terminal is mentioned in Technical Assignment. NFC/contactless payment capability required. No internet acquiring. 44-FZ public procurement with EIS acceptance procedures."
     8	}
Tool:    201	      "procedure_channel": "EDI/E-invoicing; courier; UKEP signature",
   202	      "liability_remedy": "",
   203	      "scope_options": [],
   204	      "consequence": "documents have legal force",
   205	      "applicability_filters": {
   206	        "required_type": "mandatory",
   207	        "only_for_product": "common",
   208	        "only_for_lot": "common",
   209	        "only_for_terminal": "common",
   210	        "payment_method": "common"
   211	      },
   212	      "main_idea": "Важна равнозначность документов",
   213	      "topics": [
   214	        "Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП",
   215	        "электронные документы имеют юридическую силу документов на бумаге"
   216	      ],
   217	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью   (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;"
   218	    },
   219	    {
   220	      "id": "2.3.6",
   221	      "source_text": "Важен сам факт наличия данного канала для обмена электронными документами Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок); Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП) Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   222	      "source_excerpt": "Важен сам факт наличия данного канала для обмена электронными документами Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок); Перечисление способов обмена документами: обмен документами через",
   223	      "type": "operative",
   224	      "materiality": "evaluable",
   225	      "protected_party": "Both",
   226	      "bound_party": "Both",
   227	      "right_or_obligation": "mutual_obligation",
   228	      "legal_object": "EIS communication channel; transaction documents",
   229	      "trigger": "ongoing/upon event",
   230	      "deadline": "",
   231	      "amount_formula_cap": "",
   232	      "procedure_channel": "EIS; UKEP signature",
   233	      "liability_remedy": "",
   234	      "scope_options": [
   235	        "lot:fz_44"
   236	      ],
   237	      "consequence": "documents have legal force",
   238	      "applicability_filters": {
   239	        "required_type": "mandatory",
   240	        "only_for_product": "common",
   241	        "only_for_lot": "fz_44",
   242	        "only_for_terminal": "common",
   243	        "payment_method": "common"
   244	      },
   245	      "main_idea": "Важен сам факт наличия данного канала для обмена электронными документами",
   246	      "topics": [
   247	        "Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок)",
   248	        "Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП)"
   249	      ],
   250	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;"
   251	    },
   252	    {
   253	      "id": "2.3.7",
   254	      "source_text": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию Обмен информацией через обращение в службу поддержки Банка; Дата с которой сторона считается получившей информацию в случае её направления на электронную почту; Дата с которой сторона считается получившей информацию в случае запроса в ДБО; Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма; Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»; Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в: • п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно; • п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма); • п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции; • п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке; • п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   255	      "source_excerpt": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию Обмен информацией через обращение в службу поддержки Банка;",
   256	      "type": "operative",
   257	      "materiality": "evaluable",
   258	      "protected_party": "Both",
   259	      "bound_party": "Both",
   260	      "right_or_obligation": "obligation",
   261	      "legal_object": "email communication channel; DBO communication channel; EDI communication channel; EIS communication channel; support service channel",
   262	      "trigger": "upon specified condition",
   263	      "deadline": "",
   264	      "amount_formula_cap": "",
   265	      "procedure_channel": "email; DBO system; EDI/E-invoicing; EIS",
   266	      "liability_remedy": "",
   267	      "scope_options": [],
   268	      "consequence": "legal effect as specified",
   269	      "applicability_filters": {
   270	        "required_type": "optional",
   271	        "only_for_product": "common",
   272	        "only_for_lot": "common",
   273	        "only_for_terminal": "common",
   274	        "payment_method": "common"
   275	      },
   276	      "main_idea": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию",
   277	      "topics": [
   278	        "Обмен информацией через обращение в службу поддержки Банка",
   279	        "Дата с которой сторона считается получившей информацию в случае её направления на электронную почту",
   280	        "Дата с которой сторона считается получившей информацию в случае запроса в ДБО",
   281	        "Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма",
   282	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»",
   283	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС"
   284	      ],
   285	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в:\n• п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;\n• п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма);\n• п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;\n•  п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке;\n• п. 2.3.7. Договора – в дату обращения в службу поддержки Банка."
   286	    },
   287	    {
   288	      "id": "2.4",
   289	      "source_text": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   290	      "source_excerpt": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   291	      "type": "operative",
   292	      "materiality": "evaluable",
   293	      "protected_party": "Both",
   294	      "bound_party": "Both",
   295	      "right_or_obligation": "obligation",
   296	      "legal_object": "transaction documents",
   297	      "trigger": "ongoing/upon event",
   298	      "deadline": "",
   299	      "amount_formula_cap": "",
   300	      "procedure_channel": "",
   301	      "liability_remedy": "",
   302	      "scope_options": [],
   303	      "consequence": "legal effect as specified",
   304	      "applicability_filters": {
   305	        "required_type": "optional",
   306	        "only_for_product": "common",
   307	        "only_for_lot": "common",
   308	        "only_for_terminal": "common",
   309	        "payment_method": "common"
   310	      },
   311	      "main_idea": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   312	      "topics": [],
   313	      "enriched_text": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора."
   314	    },
   315	    {
   316	      "id": "2.5.1.1",
   317	      "source_text": "Важен факт, что бесконтактная оплата подключается автоматически SberPayOnline подключается автоматически при подключении Интернет-эквайринга; используется единый тариф по Интернет-эквайрингу Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;",
   318	      "source_excerpt": "Важен факт, что бесконтактная оплата подключается автоматически SberPayOnline подключается автоматически при подключении Интернет-эквайринга; используется единый тариф по Интернет-эквайрингу Возможность совершения Операций оплаты с использо",
   319	      "type": "operative",
   320	      "materiality": "evaluable",
   321	      "protected_party": "Both",
   322	      "bound_party": "Both",
   323	      "right_or_obligation": "obligation",
   324	      "legal_object": "SberPay payment method; payment; internet acquiring; pricing/tariffs",
   325	      "trigger": "connection of additional equipment",
   326	      "deadline": "",
   327	      "amount_formula_cap": "",
   328	      "procedure_channel": "",
   329	      "liability_remedy": "",
   330	      "scope_options": [
   331	        "product:internet_acquiring"
   332	      ],
   333	      "consequence": "legal effect as specified",
   334	      "applicability_filters": {
   335	        "required_type": "mandatory",
   336	        "only_for_product": "internet_acquiring",
   337	        "only_for_lot": "common",
   338	        "only_for_terminal": "common",
   339	        "payment_method": "common"
   340	      },
   341	      "main_idea": "Важен факт, что бесконтактная оплата подключается автоматически",
   342	      "topics": [
   343	        "SberPayOnline подключается автоматически при подключении Интернет-эквайринга",
   344	        "используется единый тариф по Интернет-эквайрингу"
   345	      ],
   346	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;"
   347	    },
   348	    {
   349	      "id": "2.5.2.1",
   350	      "source_text": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; наличие документа 'Информация о ТСТ' Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.",
   351	      "source_excerpt": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; н",
   352	      "type": "operative",
   353	      "materiality": "evaluable",
   354	      "protected_party": "Both",
   355	      "bound_party": "Both",
   356	      "right_or_obligation": "obligation",
   357	      "legal_object": "SberPay payment method; payment; transaction documents",
   358	      "trigger": "ongoing/upon event",
   359	      "deadline": "",
   360	      "amount_formula_cap": "",
   361	      "procedure_channel": "",
   362	      "liability_remedy": "",
   363	      "scope_options": [
   364	        "product:trade_acquiring",
   365	        "payment:sber_pay_face_scan"
   366	      ],
   367	      "consequence": "legal effect as specified",
   368	      "applicability_filters": {
   369	        "required_type": "mandatory",
   370	        "only_for_product": "trade_acquiring",
   371	        "only_for_lot": "common",
   372	        "only_for_terminal": "common",
   373	        "payment_method": "sber_pay_face_scan"
   374	      },
   375	      "main_idea": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением",
   376	      "topics": [
   377	        "подключение SberPayFaceScan оформляется на бумажном носителе",
   378	        "подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия",
   379	        "наличие документа 'Информация о ТСТ'"
   380	      ],
   381	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ."
   382	    },
   383	    {
   384	      "id": "2.6.1.1",
   385	      "source_text": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.",
   386	      "source_excerpt": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-код",
   387	      "type": "operative",
   388	      "materiality": "evaluable",
   389	      "protected_party": "Both",
   390	      "bound_party": "Both",
   391	      "right_or_obligation": "obligation",
   392	      "legal_object": "QR payment method; terminal equipment; payment",
   393	      "trigger": "ongoing/upon event",
   394	      "deadline": "",
   395	      "amount_formula_cap": "",
   396	      "procedure_channel": "",
   397	      "liability_remedy": "",
   398	      "scope_options": [
   399	        "product:trade_acquiring",
   400	        "terminal:smart",
   401	        "payment:qr"
   402	      ],
   403	      "consequence": "legal effect as specified",
   404	      "applicability_filters": {
   405	        "required_type": "mandatory",
   406	        "only_for_product": "trade_acquiring",
   407	        "only_for_lot": "common",
   408	        "only_for_terminal": "smart",
   409	        "payment_method": "qr"
   410	      },
   411	      "main_idea": "Для приема QR на смарт-терминал не нужно отдельное ПО",
   412	      "topics": [
   413	        "OR-код подключается при установке Смарт-терминала Банка",
   414	        "OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ"
   415	      ],
   416	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ."
   417	    },
   418	    {
   419	      "id": "2.6.2.1",
   420	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка возможность использования QR-кода на ККТ с собственным ПО Предприятия; подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API); порядок и условия подключения QR-API описаны на Официальном сайте Банка Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;",
   421	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте бан",
   422	      "type": "operative",
   423	      "materiality": "evaluable",
   424	      "protected_party": "Both",
   425	      "bound_party": "Bank",
   426	      "right_or_obligation": "obligation",
   427	      "legal_object": "QR payment method; terminal equipment; payment; API integration",
   428	      "trigger": "connection of additional equipment",
   429	      "deadline": "",
   430	      "amount_formula_cap": "",
   431	      "procedure_channel": "API; Bank website",
   432	      "liability_remedy": "liability specified",
   433	      "scope_options": [
   434	        "product:trade_acquiring",
   435	        "payment:qr"
   436	      ],
   437	      "consequence": "legal effect as specified",
   438	      "applicability_filters": {
   439	        "required_type": "mandatory",
   440	        "only_for_product": "trade_acquiring",
   441	        "only_for_lot": "common",
   442	        "only_for_terminal": "common",
   443	        "payment_method": "qr"
   444	      },
   445	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре.  Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка",
   446	      "topics": [
   447	        "возможность использования QR-кода на ККТ с собственным ПО Предприятия",
   448	        "подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API)",
   449	        "порядок и условия подключения QR-API описаны на Официальном сайте Банка"
   450	      ],
   451	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;"
   452	    },
   453	    {
   454	      "id": "2.6.2.2",
   455	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ; подключение динамического QR-кода зависит от ПО ККТ; при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора; первая операция оплаты QR-кодом активирует услугу; Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора; подключение QR-кода производится согласно Приложениям №1 и №1.1 Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору.",
   456	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на",
   457	      "type": "operative",
   458	      "materiality": "evaluable",
   459	      "protected_party": "Bank",
   460	      "bound_party": "Both",
   461	      "right_or_obligation": "obligation",
   462	      "legal_object": "QR payment method; terminal equipment; payment; API integration",
   463	      "trigger": "ongoing/upon event",
   464	      "deadline": "",
   465	      "amount_formula_cap": "",
   466	      "procedure_channel": "API",
   467	      "liability_remedy": "",
   468	      "scope_options": [
   469	        "product:trade_acquiring",
   470	        "payment:qr"
   471	      ],
   472	      "consequence": "legal effect as specified",
   473	      "applicability_filters": {
   474	        "required_type": "mandatory",
   475	        "only_for_product": "trade_acquiring",
   476	        "only_for_lot": "common",
   477	        "only_for_terminal": "common",
   478	        "payment_method": "qr"
   479	      },
   480	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия",
   481	      "topics": [
   482	        "возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ",
   483	        "подключение динамического QR-кода зависит от ПО ККТ",
   484	        "при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора",
   485	        "первая операция оплаты QR-кодом активирует услугу",
   486	        "Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора",
   487	        "подключение QR-кода производится согласно Приложениям №1 и №1.1"
   488	      ],
   489	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору."
   490	    },
   491	    {
   492	      "id": "2.6.3.1",
   493	      "source_text": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → QR-код подключается при установке Электронного терминала в ТСТ;",
   494	      "source_excerpt": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-",
   495	      "type": "operative",
   496	      "materiality": "evaluable",
   497	      "protected_party": "Both",
   498	      "bound_party": "Both",
   499	      "right_or_obligation": "obligation",
   500	      "legal_object": "QR payment method; terminal equipment; payment",
AI: Now let me look at the contract side of legal_propositions to understand what contract clauses have been identified:[{'name': 'grep', 'args': {'pattern': '"contract":', 'path': '/outputs/working/legal_propositions.json', 'output_mode': 'content'}, 'id': 'call_00_b03IpJkcRcQMpSkKEPyY4844', 'type': 'tool_call'}]
Tool: No matches found
AI: [{'name': 'grep', 'args': {'pattern': '"contract"', 'path': '/outputs/working/legal_propositions.json', 'output_mode': 'content'}, 'id': 'call_00_LZIqrrmsCnZTZbummaft4584', 'type': 'tool_call'}]
Tool: No matches found
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/outputs/working/legal_propositions.json\', \'r\') as f:\n    data = json.load(f)\nprint(\'Top-level keys:\', list(data.keys()))\nif \'contract\' in data:\n    print(\'Contract entries:\', len(data[\'contract\']))\n    for i, c in enumerate(data[\'contract\'][:5]):\n        print(f\'  [{i}] id={c.get(\\"id\\")}, type={c.get(\\"type\\")}, materiality={c.get(\\"materiality\\")}\')\nelse:\n    print(\'No contract key found\')\n"'}, 'id': 'call_00_P78Amaec6vijido0tNg04796', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 9
[stderr]     print(f'  [{i}] id={c.get(" id\)},
[stderr]                               ^
[stderr] SyntaxError: unterminated string literal (detected at line 9)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/outputs/working/legal_propositions.json\', \'r\') as f:\n    data = json.load(f)\nprint(\'Top-level keys:\', list(data.keys()))\nif \'contract\' in data:\n    print(\'Contract entries:\', len(data[\'contract\']))\n    for i, c in enumerate(data[\'contract\'][:5]):\n        print(\'  [%d] id=%s, type=%s, materiality=%s\' % (i, c.get(\'id\'), c.get(\'type\'), c.get(\'materiality\')))\nelse:\n    print(\'No contract key found\')\n"'}, 'id': 'call_00_MaRVxONHn2OW6k1yCyMv3547', 'type': 'tool_call'}]
Tool: Top-level keys: ['matrix', 'contract']
Contract entries: 219
  [0] id=1, type=operative, materiality=evaluable
  [1] id=1.1, type=operative, materiality=evaluable
  [2] id=1.2, type=operative, materiality=evaluable
  [3] id=1.3, type=operative, materiality=evaluable
  [4] id=2, type=heading, materiality=heading

[Command succeeded with exit code 0]
AI: Good. Now let me get a full picture of the contract propositions - I need to see all of them to identify which ones are material and have no matrix analogue. Let me extract the contract side systematically.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/outputs/working/legal_propositions.json\', \'r\') as f:\n    data = json.load(f)\ncontract = data[\'contract\']\nfor c in contract:\n    mid = c.get(\'materiality\',\'\')\n    ctype = c.get(\'type\',\'\')\n    cid = c.get(\'id\',\'\')\n    pp = c.get(\'protected_party\',\'\')\n    bp = c.get(\'bound_party\',\'\')\n    ro = c.get(\'right_or_obligation\',\'\')\n    lo = c.get(\'legal_object\',\'\')\n    print(\'%s | %s | %s | pp=%s | bp=%s | ro=%s | lo=%s\' % (cid, ctype, mid, pp, bp, ro, lo))\n" 2>&1 | head -250'}, 'id': 'call_00_JbAVVEMG0ikK9ajfAd956078', 'type': 'tool_call'}]
Tool: [stderr] $ErrorActionPreference = 'Stop'
[stderr] $env:PYTHONIOENCODING = 'utf-8'
[stderr] $env:PYTHONUTF8 = '1'
[stderr] if (Test-Path -LiteralPath 'C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\.venv\Scripts') {
[stderr]   $env:Path = 'C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\.venv\Scripts;' + $env:Path
[stderr] }
[stderr] [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[stderr] $OutputEncoding = [Console]::OutputEncoding
[stderr] Remove-Item Alias:mkdir -Force -ErrorAction SilentlyContinue
[stderr] function mkdir {
[stderr]   param(
[stderr]     [Alias('p')][switch]$Parents,
[stderr]     [Parameter(Position=0, ValueFromRemainingArguments=$true)][string[]]$Paths
[stderr]   )
[stderr]   foreach ($path in $Paths) {
[stderr]     if ($path.StartsWith('-')) { continue }
[stderr]     New-Item -ItemType Directory -Force -Path $path | Out-Null
[stderr]   }
[stderr] }
[stderr] function touch {
[stderr]   param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Paths)
[stderr]   foreach ($path in $Paths) {
[stderr]     if (Test-Path -LiteralPath $path) {
[stderr]       (Get-Item -LiteralPath $path).LastWriteTime = Get-Date
[stderr]     } else {
[stderr]       New-Item -ItemType File -Force -Path $path | Out-Null
[stderr]     }
[stderr]   }
[stderr] }
[stderr] try {
[stderr] python3 -c "
[stderr] import json
[stderr] with open('outputs/working/legal_propositions.json', 'r') as f:
[stderr]     data = json.load(f)
[stderr] contract = data['contract']
[stderr] for c in contract:
[stderr]     mid = c.get('materiality','')
[stderr]     ctype = c.get('type','')
[stderr]     cid = c.get('id','')
[stderr]     pp = c.get('protected_party','')
[stderr]     bp = c.get('bound_party','')
[stderr]     ro = c.get('right_or_obligation','')
[stderr]     lo = c.get('legal_object','')
[stderr]     print('%s | %s | %s | pp=%s | bp=%s | ro=%s | lo=%s' % (cid, ctype, mid, pp, bp, ro, lo))
[stderr] " 2>&1 | head -250
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : The term 'head' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
[stderr] lling of the name, or if a path was included, verify that the path is correct and try again.
[stderr] At line:50 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/enrich_propositions.py 2>&1 || echo "Script not found or failed"'}, 'id': 'call_00_DwMiFPuNUMOj6Nm3ndWU9717', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:53
[stderr] + python3 outputs/working/enrich_propositions.py 2>&1 || echo "Script n ...
[stderr] +                                                     ~~
[stderr] The token '||' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import json; data=json.load(open(\'/outputs/working/legal_propositions.json\',\'r\')); contract=data[\'contract\']; [print(\'%s|%s|%s|pp=%s|bp=%s|ro=%s|lo=%s\' % (c.get(\'id\',\'\'), c.get(\'type\',\'\'), c.get(\'materiality\',\'\'), c.get(\'protected_party\',\'\'), c.get(\'bound_party\',\'\'), c.get(\'right_or_obligation\',\'\'), c.get(\'legal_object\',\'\'))) for c in contract]"'}, 'id': 'call_00_wzwifVvY63aOg1IgZZ1Q4231', 'type': 'tool_call'}]
Tool: 1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=contract subject matter
1.1|operative|evaluable|pp=Customer|bp=Customer|ro=obligation|lo=card acceptance; payment; TST/outlet; appendices; specification
1.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
1.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; payment
2|heading|heading|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
2.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=authorization; operations/transactions
2.1.1|operative|evaluable|pp=Both|bp=Both|ro=right|lo=card acceptance; operations/transactions; payment; TST/outlet; party details
2.1.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment
2.1.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment
2.1.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet; refund/chargeback
2.1.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance
2.1.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions
2.1.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=authorization
2.1.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
2.1.9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; TST/outlet
2.1.10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; operations/transactions; payment; TST/outlet
2.1.11|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; operations/transactions; payment; TST/outlet
2.1.12|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; authorization; operations/transactions; payment; TST/outlet
2.1.13|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; authorization; operations/transactions; TST/outlet; settlement reconciliation
2.1.14|definition|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment; TST/outlet; settlement reconciliation
2.1.15|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment
2.1.16|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment; TST/outlet; refund/chargeback
2.1.17|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment
2.1.18|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; authorization; operations/transactions; payment; TST/outlet
2.1.19|operative|evaluable|pp=Both|bp=Both|ro=right|lo=card acceptance; operations/transactions; payment; transaction receipts; settlement reconciliation
2.1.20|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
2.1.21|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment
2.1.22|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; operations/transactions; transaction receipts
2.1.23|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; price/cost
2.1.24|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
2.1.25|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
2.1.26|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; TST/outlet
2.1.27|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; operations/transactions; transaction receipts
2.1.28|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; operations/transactions; settlement reconciliation
2.2|operative|evaluable|pp=Both|bp=Both|ro=right|lo=terminal equipment; card acceptance; operations/transactions; TST/outlet; term/duration
2.3|operative|evaluable|pp=Both|bp=Both|ro=mutual_obligation|lo=general contractual terms
2.3.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet; email communication
2.3.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=DBO system
2.3.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet
2.3.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet
2.3.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=electronic signature
2.3.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=EIS; electronic signature
2.3.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet; email communication; DBO system; EIS
3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost
3.1|definition|not_material|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
3.1.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; appendices; specification
3.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; price/cost
3.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; term/duration
4.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
4.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet; contract subject matter; licensing
4.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment; TST/outlet; transaction receipts
4.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; term/duration; party details; cashless settlement
4.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; acceptance procedure; term/duration
4.5.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure; term/duration
5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.1|operative|evaluable|pp=Customer|bp=Bank|ro=obligation|lo=general contractual terms
5.1.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; operations/transactions; TST/outlet; training/instructions
5.1.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; acceptance procedure
5.1.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
5.1.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment
5.1.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.1.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=authorization
5.1.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; operations/transactions; TST/outlet
5.1.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; operations/transactions; payment; TST/outlet; settlement reconciliation
5.1.9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; personal data; confidentiality
5.1.10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment; TST/outlet
5.2|operative|evaluable|pp=Bank|bp=Customer|ro=right|lo=general contractual terms
5.2.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; acceptance procedure
5.2.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=unilateral termination
5.2.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; TST/outlet
5.2.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions
5.2.5|operative|evaluable|pp=Both|bp=Both|ro=right|lo=operations/transactions; transaction receipts; dispute resolution
5.2.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=party details
5.2.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; TST/outlet; email communication
5.2.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.2.9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=authorization; TST/outlet; contract termination; unilateral termination; suspension right
5.2.9.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.2.9.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.2.9.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet
5.2.9.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; TST/outlet
5.2.9.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet; email communication; fraud prevention
5.2.9.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet
5.2.9.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
5.2.9.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; contract subject matter
5.2.9.9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
5.2.9.10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet
5.2.9.11|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=term/duration
5.2.10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=withholding right
5.2.10.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; authorization; operations/transactions; payment
5.2.10.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.2.10.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; refund/chargeback
5.2.10.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment; TST/outlet; dispute resolution; withholding right
5.2.10.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; TST/outlet; EIS; penalties; liability
5.3|operative|evaluable|pp=Bank|bp=Customer|ro=obligation|lo=general contractual terms
5.3.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure
5.3.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; price/cost
5.3.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
5.3.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; unilateral termination
5.3.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=EIS; penalties
5.3.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; TST/outlet
5.3.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment; TST/outlet
5.3.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; payment
5.3.9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; TST/outlet; dispute resolution; party details
5.3.10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet; liability
5.3.11|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; transaction receipts; dispute resolution
5.3.12|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; TST/outlet
5.3.13|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; contract subject matter; party details
5.3.14|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=contract subject matter
5.3.15|operative|evaluable|pp=Bank|bp=Customer|ro=obligation|lo=personal data; indemnification
5.3.16|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment; contract termination
5.3.17|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet; fraud prevention
5.3.18|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet
5.3.18.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; operations/transactions; TST/outlet
5.3.18.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment
5.3.18.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment
5.3.20.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment
5.3.18.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; refund/chargeback; contract termination
5.3.19|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment; TST/outlet; EIS
5.3.20|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; personal data; dispute resolution
5.4|operative|evaluable|pp=Customer|bp=Bank|ro=right|lo=general contractual terms
5.4.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
5.4.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure
5.4.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=unilateral termination
5.4.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=payment; refund/chargeback; indemnification
5.4.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment
5.5|operative|evaluable|pp=Bank|bp=Customer|ro=obligation|lo=operations/transactions
5.6|operative|evaluable|pp=Bank|bp=Customer|ro=obligation|lo=terminal equipment; refund/chargeback; contract termination
5.7|operative|evaluable|pp=Bank|bp=Customer|ro=obligation|lo=terminal equipment; refund/chargeback; penalties; currency (RUB)
5.9|operative|evaluable|pp=Customer|bp=Bank|ro=right|lo=terminal equipment; card acceptance; operations/transactions
5.10|operative|evaluable|pp=Bank|bp=Customer|ro=obligation|lo=operations/transactions; training/instructions
6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=anti-corruption
6.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=contract termination; contract subject matter
7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; liability
7.1|operative|evaluable|pp=Both|bp=Both|ro=right|lo=TST/outlet; EIS; penalties; liability; force majeure
7.2|operative|evaluable|pp=Bank|bp=Customer|ro=right|lo=EIS; penalties
7.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=penalties; term/duration
7.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=penalties
7.4.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; penalties; price/cost; currency (RUB)
7.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=EIS; penalties
7.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; penalties; term/duration
7.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=EIS; penalties
7.7.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; penalties; price/cost; currency (RUB)
7.7.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; penalties; price/cost; contract subject matter
10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=price/cost; currency (RUB)
7.7.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; penalties; price/cost; currency (RUB)
7.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; liability
7.9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=penalties
7.10|operative|evaluable|pp=Both|bp=Both|ro=right|lo=EIS; penalties
7.11|operative|evaluable|pp=Both|bp=Both|ro=right|lo=penalties
7.12|operative|evaluable|pp=Both|bp=Both|ro=right|lo=contract termination; unilateral termination; indemnification
8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure
8.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=term/duration; appendices
8.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; liability
8.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure
8.3.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; acceptance procedure; price/cost
8.3.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment; TST/outlet; acceptance procedure
8.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; acceptance procedure
8.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure
8.5.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; acceptance procedure; term/duration
8.5.2|operative|evaluable|pp=Customer|bp=Bank|ro=right|lo=TST/outlet; acceptance procedure; term/duration
8.5.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure; term/duration
8.5.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure; term/duration; unilateral termination
8.5.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
8.5.6|operative|evaluable|pp=Both|bp=Both|ro=right|lo=TST/outlet; contract subject matter
8.5.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; acceptance procedure
8.5.8|operative|evaluable|pp=Both|bp=Both|ro=right|lo=TST/outlet; EIS; acceptance procedure
8.5.9|operative|evaluable|pp=Bank|bp=Customer|ro=right|lo=TST/outlet; acceptance procedure
8.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=EIS; acceptance procedure
8.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; acceptance procedure
8.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=acceptance procedure; term/duration
8.9|operative|evaluable|pp=Customer|bp=Bank|ro=right|lo=TST/outlet; acceptance procedure
8.10|operative|evaluable|pp=Customer|bp=Bank|ro=obligation|lo=general contractual terms
8.11|definition|not_material|pp=Both|bp=Both|ro=obligation|lo=payment; acceptance procedure
9|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=force majeure
9.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; EIS; liability; force majeure
9.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; term/duration; force majeure
9.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=force majeure; dispute resolution
10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=dispute resolution
10.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; email communication; EIS; liability; term/duration
10.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=dispute resolution
11|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=contract termination; term/duration
11.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; liability; term/duration; contract subject matter
11.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
11.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet; contract termination; unilateral termination
11.4|operative|evaluable|pp=Customer|bp=Bank|ro=right|lo=unilateral termination
11.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=term/duration; unilateral termination
11.6|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=contract termination; term/duration
11.7|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
11.8|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
12|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
12.1|definition|not_material|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
12.2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
12.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=TST/outlet
12.4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
12.5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=appendices; technical specification; specification
13|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=party details
354340|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment; appendices; technical specification
1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment
2|operative|evaluable|pp=Both|bp=Both|ro=right|lo=terminal equipment; transaction receipts
3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; payment
4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=term/duration
5|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; operations/transactions; payment; TST/outlet
9.2.1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; operations/transactions; payment; TST/outlet
1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=operations/transactions; TST/outlet
2|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; payment; appendices; QR payment; SberPay
3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=contract subject matter
1.1|definition|not_material|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
1.2|operative|evaluable|pp=Bank|bp=Both|ro=right|lo=general contractual terms
1.3|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=dispute resolution; withholding right
4|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=card acceptance; operations/transactions; payment; TST/outlet; transaction receipts
10|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=terminal equipment; card acceptance; authorization; operations/transactions; payment
1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms
1|operative|evaluable|pp=Both|bp=Both|ro=obligation|lo=general contractual terms

[Command succeeded with exit code 0]
AI: Now I have a comprehensive view. Let me now read the clause_index to understand the mapping, and also check if there's an existing coverage_ledger:[{'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_00_BCYqjhBUZnoXkMNHwuM24094', 'type': 'tool_call'}]
Tool: ['/outputs/working/batch_2_matrix.json', '/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/enrich_propositions.py', '/outputs/working/extract_batch4.py', '/outputs/working/legal_propositions.json', '/outputs/working/working_artifact_validation.json']
AI: No coverage_ledger yet. Let me now do the systematic contract-only analysis. I need to:

1. Read the full matrix to understand all matrix topics
2. For each evaluable contract proposition, determine if it has a matrix analogue
3. Classify as `extra_in_contract` (material, no analogue) or `not_material`

Let me get the full matrix topics list and then do the contract-to-matrix comparison.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\nfor m in matrix:\n    num = m.get(\'number\',\'\')\n    mi = m.get(\'main_idea\',\'\')[:120]\n    topics = \'; \'.join(m.get(\'topics\',[]))[:150]\n    req = m.get(\'required_type\',\'\')\n    prod = m.get(\'only_for_product\',\'\')\n    lot = m.get(\'only_for_lot\',\'\')\n    term = m.get(\'only_for_terminal\',\'\')\n    pm = m.get(\'payment_method\',\'\')\n    print(\'%s | %s | req=%s | prod=%s | lot=%s | term=%s | pm=%s | %s\' % (num, mi, req, prod, lot, term, pm, topics))\n"'}, 'id': 'call_00_2zvAIvppDOLGCxtvUZwM3699', 'type': 'tool_call'}]
Tool: 2.1 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РґР»СЏ СЂРµРіРёСЃС‚СЂР°С†РёРё РґРѕРіРѕРІРѕСЂР° Р±Р°РЅРєСѓ РЅСѓР¶РЅРѕ Р·Р°СЏРІР»РµРЅРёРµ. Р’ Р·Р°СЏРІР»РµРЅРёРё РґРѕР»Р¶РЅР° Р±С‹С‚СЊ СѓРєР°Р·Р°РЅР° РїРѕР»РЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ РЅРµРѕР±С…Рѕ | req=mandatory | prod=common | lot=common | term=common | pm=common | Р”Р»СЏ СЂРµРіРёСЃС‚СЂР°С†РёРё РЅРѕРІРѕР№ РўРЎРў РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ Р·Р°СЏРІР»РµРЅРёРµ РЅР° СЂР°СЃС‡РµС‚С‹ Рё РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ РўРЎРў, РїРѕРґРїРёСЃР°РЅРЅРѕРµ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј; Р‘Р°РЅРє РјРѕР¶РµС‚ РѕС‚РєР°Р·Р°С‚СЊ РІ СЂ
2.2 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РІР°Р»СЋС‚Р° СЂСѓР±Р»СЊ Р Р¤, РґСЂСѓРіР°СЏ РІР°Р»СЋС‚Р° РЅРµРґРѕРїСѓСЃС‚РёРјР° | req=mandatory | prod=common | lot=common | term=common | pm=common | Р Р°СЃС‡С‘С‚С‹ РїСЂРѕРёР·РІРѕРґСЏС‚СЃСЏ РІ СЂСѓР±Р»СЏС… Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё
2.3.1 | РќСѓР¶РЅРѕ РїСЂРѕРІРµСЂСЏС‚СЊ РїСЂРёР·РЅР°С‘С‚СЃСЏ Р»Рё РїРѕР»РЅР°СЏ СЋСЂРёРґРёС‡РµСЃРєР°СЏ СЃРёР»Р° eвЂ‘mail, РµСЃС‚СЊ Р»Рё РѕРіСЂР°РЅРёС‡РµРЅРёСЏ РїРѕ РІРёРґР°Рј СЃРІРµРґРµРЅРёР№ Рё РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РёР·РјРµРЅСЏ | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±РјРµРЅ РёРЅС„РѕСЂРјР°С†РёРµР№ РїРѕ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚Рµ; Р�СЃРєР»СЋС‡РµРЅРёРµ РїРµСЂРµРґР°С‡Рё РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…, РєРѕРјРјРµСЂС‡РµСЃРєРѕР№ Рё Р±Р°РЅРєРѕРІСЃРєРѕР№ С‚Р°Р№РЅС‹ С‡РµСЂРµР· СЌР»РµРєС‚СЂРѕРЅРЅСѓСЋ РїРѕС‡С‚Сѓ; Р�РЅС„РѕСЂРјР°С†РёСЏ Рё
2.3.2 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕС‚РїСЂР°РІРєРё РёРЅС„РѕСЂРјР°С†РёРё / РґРѕРєСѓРјРµРЅС‚РѕРІ С‚Р°РєРёРј СЃРїРѕСЃРѕР±РѕРј | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё РїРѕСЃСЂРµРґСЃС‚РІРѕРј СЃРёСЃС‚РµРјС‹ Р”Р‘Рћ РёР»Рё Р°РЅР°Р»РѕРіРёС‡РЅС‹С… СЃРёСЃС‚РµРј Р‘Р°РЅРєР°
2.3.3 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕС‚РїСЂР°РІРєРё РёРЅС„РѕСЂРјР°С†РёРё / РґРѕРєСѓРјРµРЅС‚РѕРІ С‚Р°РєРёРј СЃРїРѕСЃРѕР±РѕРј | req=optional | prod=common | lot=common | term=common | pm=common | РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё СЃ РґРѕСЃС‚Р°РІРєРѕР№ РЅР°СЂРѕС‡РЅС‹Рј РёР»Рё РєСѓСЂСЊРµСЂРѕРј
2.3.4 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕС‚РїСЂР°РІРєРё РёРЅС„РѕСЂРјР°С†РёРё / РґРѕРєСѓРјРµРЅС‚РѕРІ С‚Р°РєРёРј СЃРїРѕСЃРѕР±РѕРј | req=optional | prod=common | lot=common | term=common | pm=common | РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё С‡РµСЂРµР· Р·Р°РєР°Р·РЅРѕРµ РїРёСЃСЊРјРѕ
2.3.5 | Р’Р°Р¶РЅР° СЂР°РІРЅРѕР·РЅР°С‡РЅРѕСЃС‚СЊ РґРѕРєСѓРјРµРЅС‚РѕРІ | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±РјРµРЅ РёРЅС„РѕСЂРјР°С†РёРµР№ Рё РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· СЃРёСЃС‚РµРјСѓ E-invoicing/В«РЎР¤Р•Р Рђ-РљСѓСЂСЊРµСЂВ» СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РЈРљР­Рџ; СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РёРјРµСЋС‚ СЋСЂРёРґРёС‡РµСЃРєСѓСЋ
2.3.6 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅР°Р»РёС‡РёСЏ РґР°РЅРЅРѕРіРѕ РєР°РЅР°Р»Р° РґР»СЏ РѕР±РјРµРЅР° СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РґРѕРєСѓРјРµРЅС‚Р°РјРё | req=mandatory | prod=common | lot=fz_44 | term=common | pm=common | РџРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃРїРѕСЃРѕР±РѕРІ РѕР±РјРµРЅР° РґРѕРєСѓРјРµРЅС‚Р°РјРё: С‡РµСЂРµР· Р•Р�РЎ (Р•РґРёРЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅСѓСЋ СЃРёСЃС‚РµРјСѓ РІ СЃС„РµСЂРµ Р·Р°РєСѓРїРѕРє); РџРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃРїРѕСЃРѕР±РѕРІ РѕР±РјРµРЅР° РґРѕРєСѓРјРµРЅС‚Р°РјРё: РѕР±РјРµРЅ Рґ
2.3.7 | Р”Р»СЏ РїСЂРµРґСЃС‚Р°РІР»РµРЅРЅС‹С… РІ РєРѕРЅС‚СЂР°РєС‚Рµ СЃРїРѕСЃРѕР±Р°С… РѕР±РјРµРЅР° РёРЅС„РѕСЂРјР°С†РёРµР№ / РґРѕРєСѓРјРµРЅС‚Р°РјРё, РЅРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ СЂР°СЃС…РѕР¶РґРµРЅРёР№ РІ РґР°РЅРЅРѕРј РїСѓРЅРєС‚Рµ РЅР°  | req=optional | prod=common | lot=common | term=common | pm=common | РћР±РјРµРЅ РёРЅС„РѕСЂРјР°С†РёРµР№ С‡РµСЂРµР· РѕР±СЂР°С‰РµРЅРёРµ РІ СЃР»СѓР¶Р±Сѓ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР°; Р”Р°С‚Р° СЃ РєРѕС‚РѕСЂРѕР№ СЃС‚РѕСЂРѕРЅР° СЃС‡РёС‚Р°РµС‚СЃСЏ РїРѕР»СѓС‡РёРІС€РµР№ РёРЅС„РѕСЂРјР°С†РёСЋ РІ СЃР»СѓС‡Р°Рµ РµС‘ РЅР°РїСЂР°РІР»РµРЅРёСЏ РЅР° СЌР»РµРєС‚СЂРѕРЅ
2.4 | Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ РїСЂРёР·РЅР°РЅРёРµ СЃСЃС‹Р»РѕРє Рё РґРѕРєСѓРјРµРЅС‚РѕРІ РІ РґРѕРіРІРѕСЂРµ РµРіРѕ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ | req=optional | prod=common | lot=common | term=common | pm=common | 
2.5.1.1 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р±РµСЃРєРѕРЅС‚Р°РєС‚РЅР°СЏ РѕРїР»Р°С‚Р° РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | SberPayOnline РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°; РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РµРґРёРЅС‹Р№ С‚Р°СЂРёС„ РїРѕ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіСѓ
2.5.2.1 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїСЂРёРЅСЏС‚РёСЏ РѕРїР»Р°С‚С‹ РїРѕ Р±РёРѕРјРµС‚СЂРёРё РѕС„РѕСЂРјР»СЏРµС‚СЃСЏ РѕС‚РґРµР»СЊРЅС‹Рј Р·Р°СЏРІР»РµРЅРёРµРј | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=sber_pay_face_scan | РїРѕРґРєР»СЋС‡РµРЅРёРµ SberPayFaceScan РѕС„РѕСЂРјР»СЏРµС‚СЃСЏ РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ; РїРѕРґРєР»СЋС‡РµРЅРёРµ SberPayFaceScan С‚СЂРµР±СѓРµС‚ РїРѕРґРїРёСЃРё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅРѕРіРѕ РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РЅ
2.6.1.1 | Р”Р»СЏ РїСЂРёРµРјР° QR РЅР° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РЅРµ РЅСѓР¶РЅРѕ РѕС‚РґРµР»СЊРЅРѕРµ РџРћ | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=qr | OR-РєРѕРґ РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ РїСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° Р‘Р°РЅРєР°; OR-РєРѕРґ РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ РїСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ РџРћ Р‘Р°РЅРєР° РґР»СЏ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РўРЎРў
2.6.2.1 | Р’РђР–РќРћ РїСЂРѕРІРµСЂРёС‚СЊ, С‡С‚Рѕ РІ РґРѕРіРѕРІРѕСЂРµ РёРґС‘С‚ СЂРµС‡СЊ Рѕ РЎРћР‘РЎРўР’Р•РќРќР«РҐ С‚РµСЂРјРёРЅР°Р»Р°С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ. Р•СЃР»Рё СЌС‚Рѕ РЅРµ С‚Р°Рє,С‚Рѕ РґР°РЅРЅС‹Р№ СЂРёСЃРє РЅРµ СЃРѕРґРµСЂР¶ | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-РєРѕРґР° РЅР° РљРљРў СЃ СЃРѕР±СЃС‚РІРµРЅРЅС‹Рј РџРћ РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РїРѕРґРєР»СЋС‡РµРЅРёРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· РїРµСЂРµРґР°С‡Сѓ РёРЅС„РѕСЂРјР°С†РёРё РѕС‚ Р‘Р°РЅРєР° Рє РџСЂРµРґРїСЂРёСЏС‚РёСЋ С‡РµСЂ
2.6.2.2 | Р’РђР–РќРћ РїСЂРѕРІРµСЂРёС‚СЊ, С‡С‚Рѕ РІ РґРѕРіРѕРІРѕСЂРµ РёРґС‘С‚ СЂРµС‡СЊ Рѕ РЎРћР‘РЎРўР’Р•РќРќР«РҐ С‚РµСЂРјРёРЅР°Р»Р°С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ. Р•СЃР»Рё СЌС‚Рѕ РЅРµ С‚Р°Рє,С‚Рѕ РґР°РЅРЅС‹Р№ СЂРёСЃРє РЅРµ СЃРѕРґРµСЂР¶ | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ РїРѕ QR-РєРѕРґСѓ РЅР° СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»Р°С… Рё РљРљРў; РїРѕРґРєР»СЋС‡РµРЅРёРµ РґРёРЅР°РјРёС‡РµСЃРєРѕРіРѕ QR-РєРѕРґР° Р·Р°РІРёСЃРёС‚ РѕС‚ РџРћ РљРљРў; РїСЂРё РѕС‚СЃСѓС‚СЃС‚РІРёРё
2.6.3.1 | Р”Р°РЅРЅС‹Р№ СЂРёСЃРє РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє С‚РµСЂРјРёРЅР°Р»Р°Рј РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹Рј Р‘Р°РЅРєРѕРј. Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ QR РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ СЃСЂР°Р·Сѓ РїСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | QR-РєРѕРґ РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ РїСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° РІ РўРЎРў
2.6.3.2 | Р”Р°РЅРЅС‹Р№ СЂРёСЃРє РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє С‚РµСЂРјРёРЅР°Р»Р°Рј РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹Рј Р‘Р°РЅРєРѕРј. Р”Р»СЏ РѕС‚РєР»СЋС‡РµРЅРёСЏ QR-РєРѕРґР° РЅРµРѕР±С…РѕРґРёРјРѕ РѕР±СЂР°С‰РµРЅРёРµ РІ Р±Р°РЅРє | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | РѕС‚РєР»СЋС‡РµРЅРёРµ QR-РєРѕРґР° РІРѕР·РјРѕР¶РЅРѕ РїРѕ РёРЅРёС†РёР°С‚РёРІРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РёРЅРёС†РёР°С‚РёРІР° РѕС‚РєР»СЋС‡РµРЅРёСЏ СЂРµР°Р»РёР·СѓРµС‚СЃСЏ С‡РµСЂРµР· РѕР±СЂР°С‰РµРЅРёРµ РІ Р‘Р°РЅРє
2.7 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РґРѕРіРѕРІРѕСЂ РјРѕР¶РµС‚ Р±С‹С‚СЊ Р·Р°РєР»СЋС‡РµРЅ РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ СЃ РїРѕРґРїРёСЃР°РЅРёРµРј РЈРљР­Рџ  | req=optional | prod=common | lot=common | term=common | pm=common | 
3.1 | Р’Р°Р¶РЅРѕ РїРѕРґСЃРІРµС‚РёС‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё РїРµСЂРµС‡РёСЃР»РµРЅР° РїР»Р°С‚С‘Р¶РЅР°СЏ СЃРёСЃС‚РµРјР° РѕС‚Р»РёС‡РЅР°СЏ РѕС‚ РќРЎРџРљ РёР»Рё РњР�Р  | req=optional | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РѕСЂРіР°РЅРёР·РѕРІР°С‚СЊ РїСЂРёС‘Рј РѕРїР»Р°С‚С‹ Р·Р° РўРѕРІР°СЂС‹/СѓСЃР»СѓРіРё СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РїР»Р°С‚С‘Р¶РЅС‹С… РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ (РљР°СЂС‚Р°, СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹, NFC-РєР°СЂС‚Р°, SberPay, РџР»
3.2 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР° РІ РїРµСЂРµС‡РёСЃР»РµРЅРёРё СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЋ | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РѕР±СЏР·Р°РЅ РїРµСЂРµС‡РёСЃР»СЏС‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РџСЂРµРґРїСЂРёСЏС‚РёСЋ
3.3 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РґРѕР»Р¶РЅРѕ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµРјС‹Рµ РїРѕ РґРѕРіРѕРІРѕСЂСѓ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµС‡РёСЃР»СЏРµС‚ Р‘Р°РЅРєСѓ РїР»Р°С‚Сѓ Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡С‘С‚РѕРІ РµР¶РµРјРµСЃСЏС‡РЅРѕ
4.1.1 | Р’Р°Р¶РЅРѕ, РµСЃР»Рё РџСЂРµРґРїСЂРёСЏС‚РёРµ С…РѕС‡РµС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»Р°С… СѓРїРѕРјРёРЅР°РЅРёРµ Р±СЂРµРЅРґР° Р‘Р°РЅРєР° - РЅР°РґРѕ СЃРѕРіР»Р°СЃРѕРІС‹РІР°С‚СЊ СЃ Р‘Р° | req=optional | prod=common | lot=common | term=common | pm=qr | РџСЂРµРґРїСЂРёСЏС‚РёРµ РёРјРµРµС‚ РїСЂР°РІРѕ СЃСЃС‹Р»Р°С‚СЊСЃСЏ РЅР° РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚/QR-РєРѕРґР° РїРѕСЃР»Рµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РјР°С‚РµСЂРёР°Р»РѕРІ СЃ Р‘Р°РЅРєРѕРј; РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РёРЅС„РѕСЂРјР°С†РёРѕРЅ
4.1.2 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РѕРєР°Р·С‹РІР°РµС‚ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЋ Р·Р°РєР°Р·С‡РёРєР° РїРѕ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЋ РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ | req=optional | prod=common | lot=common | term=common | pm=common | Р·Р°РєСЂРµРїР»РµРЅРѕ РїСЂР°РІРѕ Р—Р°РєР°Р·С‡РёРєР° РЅР° РїРѕР»СѓС‡РµРЅРёРµ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёР№ РїРѕ СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ; Р·Р°РєСЂРµРїР»РµРЅРѕ РїСЂР°РІРѕ Р—Р°РєР°Р·С‡РёРєР° РЅР° РїРѕР»СѓС‡РµРЅРёРµ 
4.1.3 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ QR РІС‹РґР°С‘С‚ Р‘Р°РЅРє | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr_sber_pay | РџСЂРµРґРїСЂРёСЏС‚РёРµ РёРјРµРµС‚ РїСЂР°РІРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РїРѕР»СѓС‡РµРЅРЅС‹Рµ РѕС‚ Р‘Р°РЅРєР° QR-РєРѕРґС‹ РґР»СЏ РїСЂРёРµРјР° РїР»Р°С‚РµР¶РµР№ С‡РµСЂРµР· SberPayQR/РџР»Р°С‚Рё QR
4.2.1 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё Р±Р°РЅРєР° РїРѕ РІС‹РїРѕР»РЅРµРЅРёСЋ СЂР°СЃС‡С‘С‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј; РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РІРЅРѕСЃРёС‚СЊ РїР»Р°С‚Сѓ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ (РµСЃР»Рё
4.2.2 | Р’Р°Р¶РЅРѕ РІ РєРѕРЅС‚СЂР°РєС‚Рµ РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РІС‹РїРѕР»РЅСЏС‚СЊ Рё СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ РґРѕРіРѕРІРѕСЂР° Рё РёРЅСЃС‚ | req=optional | prod=common | lot=common | term=common | pm=common | РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃРѕР±Р»СЋРґР°С‚СЊ РїРѕР»РѕР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° (РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё РѕР± РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґР°С‚СЊ); РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІС‹РїРѕР»РЅСЏС‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ, СЃРѕ
4.2.3 |  | req=optional | prod=common | lot=fz_223 | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё РґРѕРєСѓРјРµРЅС‚РѕРІ; РќРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР·РЅР°РєРѕРјР»РµРЅРёРµ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РЅРµРїСЂРёРј
4.2.4 | Р’Р°Р¶РµРЅ С„Р°РєС‚, РµСЃР»Рё Р±Р°РЅРє РїРµСЂРµРґР°РµС‚ РїРѕ РґРѕРіРѕРІРѕСЂСѓ РїСЂРµРґРїСЂРёСЏС‚РёСЋ - Р·Р°РєР°Р·С‡РёРєСѓ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, С‚Рѕ Р·Р°РєР°Р·С‡РёРє РґРѕР»Р¶РµРЅ РёС… СЂР°Р·РјРµ | req=optional | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЂР°Р·РјРµС‰Р°С‚СЊ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ Р‘Р°РЅРєР° Рѕ СЃРїРѕСЃРѕР±Р°С… РѕРїР»Р°С‚С‹; Р Р°Р·РјРµС‰РµРЅРёРµ РјР°С‚РµСЂРёР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёР№ 
4.2.5 | Р’Р°Р¶РЅРѕ, РЅРµ РїСЂРёРЅРёРјР°С‚СЊ РѕС‚ РџРѕРєСѓРїР°С‚РµР»СЏ Р±РѕР»РµРµ 2 (РґРІСѓС…) СЂР°Р·Р»РёС‡РЅС‹С… РљР°СЂС‚. РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРёРЅРёРјР°С‚СЊ Рє РѕРїР»Р°С‚Рµ РІСЃРµ РєР°СЂС‚С‹ РёР· СЃРїРёСЃРєР° РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РІСЂРµРјРµРЅРё; РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅСЊРіРё РїРѕ РєР°СЂС‚Р°Рј; РќРµ РїСЂРёРЅРёРјР°С‚СЊ Р±РѕР»РµРµ РґРІСѓС… СЂР°Р·РЅС‹С… РєР°СЂС‚ РѕС‚
4.2.6 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РЅРµР»СЊР·СЏ СЂР°Р·Р±РёРІР°С‚СЊ РћРїРµСЂР°С†РёСЋ РЅР° РЅРµСЃРєРѕР»СЊРєСѓ СЃСѓРјРј | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РћРїРµСЂР°С†РёСЋ РѕРїР»Р°С‚С‹ РµРґРёРЅРѕР№ СЃСѓРјРјРѕР№ Р±РµР· СЂР°Р·РґРµР»РµРЅРёСЏ РЅР° С‡Р°СЃС‚Рё
4.2.7 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ Р±РµР· РїСЂРёСЃСѓС‚СЃС‚РІРёСЏ РёР»Рё СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏ; Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ С‚РѕР»СЊРєРѕ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№
4.2.8 | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С†РµРЅР° РЅРµ Р·Р°РІРёСЃРёС‚ РѕС‚ СЃРїРѕСЃРѕР±Р° РѕРїР»Р°С‚С‹ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РїРѕР»РЅС‹Р№ РЅР°Р±РѕСЂ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РїРѕРєСѓРїР°С‚РµР»СЏРј; С†РµРЅС‹ РґР»СЏ СЂР°СЃС‡РµС‚РѕРІ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј Р±Р°РЅРєРѕРІСЃРєРѕР№ РєР°СЂС‚С‹ РЅРµ РїСЂРµРІС‹С€Р°СЋС‚ С†РµРЅС‹ Р·Р° РЅР°Р»РёС‡РЅС‹Р№ СЂР°
4.2.9 | Р—Р°РєР°Р·С‡РёРє РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РёРЅС„РѕСЂРјР°С†РёСЋ РєРѕС‚РѕСЂСѓСЋ РѕРЅ СѓРєР°Р·С‹РІР°РµС‚ РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїСЂРё РїСЂРѕРІРµРґРµРЅРёРё РїР»Р°С‚РµР¶РµР№ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РѕРїРµСЂР°С†РёРё РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№; РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РѕС„РѕСЂРјР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚
4.2.10 | Р’Р°Р¶РµРЅ С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё С…СЂР°РЅРµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј, СЃСЂРѕРє РІ С‚РµС‡РµРЅРёРё РєРѕС‚РѕСЂРѕРіРѕ РёС… РЅСѓР¶РЅРѕ С…СЂР°РЅРёС‚СЊ, С„Р°РєС‚ РїРµСЂРµРґР°С‡Рё РєРѕРїРёР№  | req=mandatory | prod=common | lot=common | term=common | pm=common | С…СЂР°РЅРµРЅРёРµ РґРѕРєСѓРјРµРЅС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј (СЃР°Рј С„Р°РєС‚ С…СЂР°РЅРµРЅРёСЏ Рё СЃСЂРѕРє С…СЂР°РЅРЅРµРёСЏ); РїРµСЂРµРґР°С‡Р° РєРѕРїРёР№ РґРѕРєСѓРјРµРЅС‚РѕРІ Р‘Р°РЅРєСѓ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№; РЅР°РґР»РµР¶Р°С‰РµРµ РєР°С‡РµСЃС‚РІРѕ РїСЂ
4.2.11 | Р’Р°Р¶РµРЅ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїРµСЂРµРґР°РІР°С‚СЊ Р·Р°СЏРІР»РµРЅРёРµ Р‘Р°РЅРєСѓ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… РѕРЅРѕ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РїРµСЂРµРґР°РЅРѕ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџРµСЂРµРґР°С‡Р° Р·Р°СЏРІР»РµРЅРёСЏ РІ Р±Р°РЅРє СЃ РёР·Р»РѕР¶РµРЅРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р·Р°РїСЂРѕСЃР°; РЅРµРјРµРґР»РµРЅРЅРѕРµ СѓРІРµРґРѕРјР»РµРЅРёРµ Р±Р°РЅ
4.2.12 | Р’Р°Р¶РµРЅ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕРґРїРёСЃР°С‚СЊ Р·Р°РєСЂС‹РІР°СЋС‰РёРµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїР»Р°С‚Рµ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… РѕРЅРѕ РґРѕР»Р¶РЅ | req=optional | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ Р°РєС†РµРїС‚РѕРІР°С‚СЊ РїР»Р°С‚РµР¶РЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ Рё СЃС‡РµС‚Р° РЅР° РѕРїР»Р°С‚Сѓ. РџСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РѕРїР»Р°С‚Рµ СЃС‡РµС‚РѕРІ; РЎСЂРѕРє РѕРїР»Р°С‚С‹ РїР»Р°С‚РµР¶РЅС‹С… С‚СЂРµР±РѕРІР°РЅРёР№ Рё СЃС‡Рµ
4.2.13 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІРѕР·РјРµС‰Р°С‚СЊ РІСЃРµ СЃСѓРјРјС‹ Рё СѓР±С‹С‚РєРё, РєРѕС‚РѕСЂС‹Рµ Р‘Р°РЅРє РїРѕРЅС‘СЃ РёР·-Р·Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІСЃРµ РІРѕР·РјРµС‰РµРЅРё | req=mandatory | prod=common | lot=common | term=common | pm=common | РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ, СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡РµС‚Р° Р‘Р°РЅРєР° РІ РїРѕР»СЊР·Сѓ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё Р”РµСЂР¶Р°С‚РµР»РµР№ РєР°СЂС‚; РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ, СѓРїР»Р°С‡РµРЅРЅС‹С… Р‘Р°РЅРєРѕРј Р‘Р°РЅРєСѓ-СЌРјРёС‚РµРЅС‚Сѓ РёР»Рё Р”РµСЂ
4.2.14 | Р’Р°Р¶РµРЅ С„Р°РєС‚ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґР°СЋС‰РёС… РґРѕРєСѓРјРµРЅС‚РѕРІ, РІР°Р¶РЅС‹ СЃСЂРѕРєРё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ, Р° С‚Р°Рє Р¶Рµ РЅСѓР¶РЅРѕ СЃСЂР°РІРЅРёС‚СЊ СЃРѕР±С‹С‚РёСЏ, РїСЂРё РєРѕ | req=mandatory | prod=common | lot=common | term=common | pm=common | РёРЅС„РѕСЂРјРёСЂРѕРІР°РЅРёРµ Р‘Р°РЅРєР° Рѕ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№; СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёСЏС… РґРѕРєСѓРјРµРЅС‚РѕРІ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№; СЃРѕРѕР±С‰РµРЅРёРµ РѕР±
4.2.15 | Р’Р°Р¶РµРЅ С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕСЃС‚РѕРІРµСЂРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ, СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ СЃРІРµРґРµРЅРёР№. Р’Р°Р¶РµРЅ С„Р°РєС‚ Рё СЃСЂРѕРє РїРµСЂРёРѕРґ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РЅРµ СЂРµР¶Рµ РѕРґРЅРѕРіРѕ СЂР°Р·Р° РІ РіРѕРґ; РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ СЃРІРµРґРµРЅРёСЏ РїРѕ Р·Р°РїСЂРѕСЃСѓ Р‘Р°РЅРєР° РІ С‚РµС‡РµРЅРёРµ 7 СЂР°Р±РѕС‡РёС…
4.2.16.1 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ Р±С‹Р»Рѕ РґРµР№СЃС‚РІСѓСЋС‰РµРµ СЃРѕРіР»Р°СЃРёРµ РЅР° РїРµСЂРµРґР°С‡Сѓ РџР”РЅ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ.  РЎРѕСЃС‚Р°РІ РџР”РЅ: Р¤Р�Рћ, Р°РґСЂРµСЃ, РїР°СЃРїРѕСЂС‚РЅС‹Рµ РґР°РЅ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ РЅР°Р»РёС‡РёРµ РїСЂР°РІРѕРІС‹С… РѕСЃРЅРѕРІР°РЅРёР№ РЅР° РїРµСЂРµРґР°С‡Сѓ РџР”РЅ; РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµРґР°РµС‚ Р¤Р�Рћ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ; РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµРґР°РµС‚ Р°РґСЂРµСЃ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ; РџСЂ
4.2.16.2 | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ РєРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ, РІР°Р¶РЅРѕ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№, РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїРѕРґС‚РІРµСЂРґРёС‚ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ(РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґС‚РёС‚РµР»Р°) РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РµРіРѕ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…; РЎРѕСЃС‚Р°РІ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ
4.2.16.3 | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РґР°РЅРЅС‹Рј РїРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј. Р’Р°Р¶РµРЅ СЃСЂРѕРє РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃРѕРіР»Р°СЃРёР№ РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ (РІРєР»СЋС‡Р°СЏ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ) РїРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ Р·Р°РїСЂРѕСЃСѓ Р±Р°
4.2.17 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґРµРЅРёСЏ СЃС‚Р°РЅРґР°СЂС‚Р°, Р° С‚Р°Рє Р¶Рµ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ PCI DSS; РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ Р°С‚С‚РµСЃС‚Р°С‚Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РёР»Рё Р»РёСЃС‚Р° СЃР°РјРѕРѕС†РµРЅРєРё РїРѕ Р·Р°РїСЂРѕСЃСѓ Р±Р°РЅРєР°; РЈРєР°Р·Р°РЅРЅС‹Р№ email РґР»СЏ РѕС‚РїСЂР°РІРєРё 
4.2.18 | Р’Р°Р¶РЅС‹ С„Р°РєС‚С‹ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, Р° С‚Р°Рє Р¶Рµ РІР°Р¶РµРЅ СЃСЂРѕРє | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РїСЂРµРєСЂР°С‰РµРЅРёРµ РїСЂРёРµРјР° РєР°СЂС‚ Рє РѕРїР»Р°С‚Рµ (СЂРµРіСѓР»РёСЂСѓРµС‚СЃСЏ РґР°С‚Р° РїСЂРµРєСЂР°С‰РµРЅРёСЏ); РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° СЃРЅСЏС‚РёРµ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ Рѕ
4.2.19 | Р’Р°Р¶РµРЅ, С„Р°РєС‚ С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµ РґРѕР»Р¶РЅРѕ РјРµС€Р°С‚СЊ Р‘Р°РЅРєСѓ, Рё С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РґРѕР»Р¶РЅРѕ РїРѕРјРѕРіР°С‚СЊ Р‘Р°РЅРєСѓ РІ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёРё | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІРѕРІР°С‚СЊ РїСЂРѕРІРµСЂРєРµ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р°РЅРєР°; РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРґРµР№СЃС‚РІРѕРІР°С‚СЊ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЋ РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№
4.2.20.1 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ СЃР°РјРѕ СЃР»РµРґРёС‚ Р·Р° РїСЂРѕС…РѕР¶РґРµРЅРёРµРј РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё, СЂР°Р·РјРµС‰РµРЅРЅРѕРіРѕ РЅР° СЃР°Р№С‚Рµ Р‘Р°РЅРєР° | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРѕРІРѕРґРёС‚СЊ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ; СЃСЃС‹Р»РєР° РЅР° РёРЅСЃС‚СЂСѓРєС†РёСЋ Рѕ РїРѕСЂСЏРґРєРµ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№
4.2.20.2 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РїСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїРѕР»СЊР·РѕРІР°Р»Рѕ С‚РµСЂРјРёРЅР°Р»С‹ Рё РџРћ Р‘Р°РЅРєР° С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РїРѕ РјРµСЃС‚Сѓ СѓСЃС‚Р°РЅРѕРІРєРё, РЅРµ РјРµРЅСЏС‚СЊ Рё РЅ | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё СЂРµРіРёСЃС‚СЂР°С†РёРё РўРЎРў/СѓСЃС‚Р°РЅРѕРІРєРё СѓСЃС‚СЂРѕР№СЃС‚РІР°; Р·Р°РїСЂРµС‚
4.2.20.3 | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ СЃС‚РѕРёС‚ Р·Р°РїСЂРµС‚ РЅР° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»РѕРІ; Р”РѕСЃС‚СѓРї РґР»СЏ РїРѕРґРєР»СЋС‡РµРЅРёСЏ С‚РµСЂРјРёРЅР°Р»РѕРІ; Р”РѕСЃС‚СѓРї РґР»СЏ РЅР°СЃС‚СЂРѕР№РєРё С‚РµСЂРјРёРЅР°Р»РѕРІ; Р”РѕСЃС‚СѓРї РґР»СЏ СЂРµРј
4.2.20.4 | Р’Р°Р¶РЅРѕ, РµСЃР»Рё СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµ Р±РµР· РґРѕРєСѓРјРµРЅС‚РѕРІ РёР»Рё Р°РєС‚Р° РїРµСЂРµРґР°С‡Рё, С‚Рѕ РІСЃС‘ РѕРє, СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµС‚ | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ / РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РІ РїРѕ Р°РєС‚Сѓ; РїРѕРґРїРёСЃР°РЅРёРµ Р°РєС‚Р° СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹РјРё Р»РёС†Р°РјРё; РЅР°Р»РёС‡РёРµ РґРІСѓС… СЌРєР·РµРјРїР»СЏСЂРѕРІ Р°РєС‚Р°; С…СЂ
4.2.20.5 |  | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ Р‘Р°РЅРє Рѕ РІС‹С…РѕРґРµ РёР· СЃС‚СЂРѕСЏ РёР»Рё СѓС‚СЂР°С‚Рµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РёР»Рё РњРѕР±РёР»СЊРЅРѕРіРѕ СѓСЃС‚СЂРѕР№СЃС‚РІР°; Р�РЅС„РѕСЂ
4.2.20.6 |  | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°; РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ/СѓСЃС‚РЅРѕРіРѕ С‚СЂРµР±РѕРІР°РЅРёСЏ Р±Р°РЅРєР°
4.2.20.7 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРј РїСѓРЅРєС‚Рµ РґРѕРіРѕРІРѕСЂР° С€Р»Р° СЂРµС‡СЊ РїСЂРѕ С€С‚СЂР°С„ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»Р° Рё РµРіРѕ СЂР°Р·РјРµСЂ, РёРЅР°С‡Рµ РґР°РЅРЅС‹Р№ РїСѓРЅРє | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | РќРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РѕР± СѓРїР»Р°С‚Рµ С€С‚СЂР°С„Р° Р·Р° РЅРµРІРѕР·РІСЂР°С‚
4.2.21.1 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РѕРїРµСЂР°С†РёР№ РЅР° СЂРµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РѕРїРµСЂР°С†РёР№ РЅР° С‚РµСЃС‚РѕРІРѕР№ СЃСЂРµРґРµ
4.2.21.2 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
4.2.21.3 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃСѓРјРј Рє СЃРїРёСЃР°РЅРёСЋ РЅРµ РїРѕР·РґРЅРµРµ 5 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№; РЎРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРЅРѕР№ СЃСѓРјРјС‹ С„Р°РєС‚РёС‡РµСЃРєРё РѕРєР°Р·Р°РЅРЅС‹Рј С‚РѕРІР°СЂР°Рј/СѓСЃР»СѓРіР°Рј; РЎРѕР±Р»СЋРґРµРЅРёРµ РџРѕСЂСЏРґРє
4.2.21.4 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґРёР·Р°Р№РЅР° РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ СЃ Р‘Р°РЅРєРѕРј; РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ СЌР»РµРєС‚СЂРѕРЅРЅС‹С… РІР°СЂРёР°РЅС‚РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РЅР°РєР»РµРµРє СЃ Р‘Р°РЅРєРѕРј
4.2.21.5 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёСЋ Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°; РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹ РІ 
4.2.21.6 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚
4.2.21.7 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР°
4.2.21.8 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РЎРѕР±Р»СЋРґРµРЅРёРµ РїСЂР°РІРёР» РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°
4.2.22 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ QR-РєРѕРґ РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ SberPayQR/РџР»Р°С‚Рё QR (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)
4.2.23 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РЅРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)
4.2.24 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API | req=optional | prod=common | lot=common | term=common | pm=qr | РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API РІ СЂР°РјРєР°С… С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API); СЃРѕР±Р»СЋРґРµРЅРёРµ РїРѕСЂСЏРґРєР° РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏ
4.2.25 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API | req=optional | prod=common | lot=common | term=common | pm=qr | РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API - РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API); РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€
4.2.26 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
5.1.1.1 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, СЏРІР»СЏСЋС‰РёРµСЃСЏ РЅРµРґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё
5.1.1.2 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ РѕС€РёР±РѕС‡РЅРѕ РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ СЃСѓРјРјС‹ СЃ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ
5.1.1.3 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°, РІРѕР·РІСЂР°С‚Р° РїР»Р°С‚РµР¶Р°, СЂРµРІРµСЂСЃРёРІРЅС‹Рµ С‚СЂР°РЅР·Р°РєС†РёРё. Р’Р°Р¶РЅРѕ РЅРµ СЂР°СЃСЃРјР°С‚СЂРёРІР°С‚СЊ РїСѓРЅРєС‚С‹ РІ РєРѕС‚РѕСЂС‹С… РЅРµ СѓРєР°Р·Р°РЅР° С…РѕС‚СЏ
5.1.1.4 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕСЃРїРѕСЂРµРЅРЅС‹С… РѕРїРµСЂР°С†РёР№ РёР»Рё СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡С‘С‚Р° РёСЃРїРѕР»СЊРЅРёС‚РµР»СЏ Р±Р°РЅРєРѕРј-СЌРјРёС‚РµРЅС‚РѕРј; Р‘Р°РЅРє СѓРґРµСЂР¶РёРІР°РµС‚ СЃСѓРјРјС‹ РѕСЃРїРѕСЂРµРЅРЅС‹С… РѕРїРµСЂР°С†РёР№ 
5.1.1.5 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РІРїСЂР°РІРµ СѓРґРµСЂР¶РёРІР°С‚СЊ С€С‚СЂР°С„С‹ РёР· СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІРѕР·РЅРёРєС€РёРµ Сѓ Р‘Р°РЅРєР° РІ СЃРІСЏР·Рё РЅРµРґРѕР±СЂРѕСЃРѕРІРµСЃС‚РЅС‹Рј РёСЃРїРѕР»РЅРµРЅРёРµРј Р—Р°РєР°Р·С‡РёРєР° РєРѕРЅС‚СЂР°РєС‚Р°; Р‘Р°РЅРє РІРїСЂР°РІРµ СѓРґРµСЂР¶РёРІР°С‚СЊ 
5.1.1.6 | Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ.  | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ
5.1.2 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРёРѕСЃС‚Р°РЅР°РІР»РёРІР°С‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅР°Р»РёС‡РёРё Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РџСЂРёРѕСЃС‚Р°РЅРѕРІРєР° РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РґРѕ РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏ
5.1.3 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | СЃРїРёСЃР°РЅРёРµ СЃСЂРµРґСЃС‚РІ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ; СѓСЃР»РѕРІРёРµ Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р°; РѕСЃРЅРѕРІР°РЅРёРµ - Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ Рѕ РїСЂРѕРІРµРґРµРЅРёРё СЂР°СЃС‡РµС‚РѕРІ
5.1.4 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | СѓРєР°Р·Р°РЅ РЅРѕРјРµСЂ СЂР°СЃС‡РµС‚РЅРѕРіРѕ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ; СѓРєР°Р·Р°РЅРѕ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ Р‘Р°РЅРєР°, РІ РєРѕС‚РѕСЂРѕРј Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РѕС‚РєСЂС‹С‚ СЃС‡РµС‚
5.1.5 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅРµ РІРѕР·РјРµС‰Р°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР°
5.1.6 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРµСЂСЏС‚СЊ С‚РµС…РЅРёС‡РµСЃРєРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ; Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·
5.1.7 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РїСЂРё РІС‹СЏРІР»РµРЅРёРё РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№; Р‘Р°РЅРє РїРµСЂРµРґР°РµС‚ РґР°РЅРЅС‹Рµ РІ РџР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РњР�Р  РїСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅ
5.1.8.1 |  | req=optional | prod=common | lot=common | term=common | pm=common | РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°
5.1.8.2 |  | req=optional | prod=common | lot=common | term=common | pm=common | РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РїСЂРёС‡Р°СЃС‚РЅС‹С… Рє СЌРєСЃС‚СЂРµРјРёР·РјСѓ, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЋ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶
5.1.8.3 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РѕС‚РјС‹РІР°РЅРёРµ РґРµРЅРµРі РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёРµ С‚РµСЂСЂРѕСЂРёР·РјР°
5.1.8.4 |  | req=optional | prod=internet_acquiring | lot=common | term=common | pm=common | Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР°
5.1.8.5 |  | req=optional | prod=internet_acquiring | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё Р—Р°РєР°Р·С‡РёРєРѕРј Р·Р°РїСЂРµС‰РµРЅРЅС‹С… РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё СЃРѕРіР»Р°СЃРЅРѕ РўСЂРµР±РѕРІ
5.1.8.6 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё; Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°
5.1.8.7 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ; Р”РѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° СЏРІР»СЏСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР°-
5.1.8.8 |  | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common | РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РѕРїРµСЂР°С†РёСЏРј; Р±Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РґР»СЏ РўРЎРў; Р±Р°РЅРє РІРїСЂР°РІРµ РёРЅРёС†РёРёСЂРѕРІР°С‚СЊ СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РґРѕРіРѕРІРѕСЂР°
5.1.8.9 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РІРѕР·Р±СѓР¶РґРµРЅРёРµ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ Р·Р°РєРѕРЅСѓ в„–127-Р¤Р—
5.1.8.10 |  | req=optional | prod=common | lot=common | term=common | pm=common | РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё; РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РўРЎРў; РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ
5.1.8.11 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РїСЂРµРґРїСЂРёСЏС‚РёСЏ; Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕ
5.1.8.12 |  | req=optional | prod=common | lot=common | term=common | pm=common | РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°
5.1.8.13 |  | req=optional | prod=common | lot=common | term=common | pm=common | РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°; РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°
5.1.9 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў; Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё
5.1.10 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РџСЂРѕРІРµСЂРєРё РїСЂРѕРІРѕРґСЏС‚СЃСЏ РґР»СЏ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° Рё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СЂРѕРґР° РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РёРЅС„РѕСЂРј
5.1.11 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ Р·Р°РїСЂР°С€РёРІР°С‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј; Р‘Р°РЅРє РјРѕР¶РµС‚ С‚СЂРµР±РѕРІР°С‚СЊ РїРёСЃСЊРјРµРЅРЅРѕРµ Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё; РџСЂРµ
5.1.12 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РІРїСЂР°РІРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ СЃРІСЏР·Р°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ unilateral_in_one_day_right; РћРїСѓР±Р»РёРєРѕРІР°РЅРёРµ РёР·РјРµРЅРµРЅРёР№ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
5.1.13 | Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµРґРѕРјР»РµРЅРёСЏ, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РёР·РјРµРЅСЏС‚СЊ СЃРІРѕРё СЂРµРєРІРёР·РёС‚С‹; РЈРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёРё СЂРµРєРІРёР·РёС‚РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· РћС„РёС†РёР°Р»СЊРЅС‹Р№ СЃР°Р№С‚ Р‘Р°РЅРєР°
5.1.14 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ; РђРґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ СѓРєР°Р·Р°РЅ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡Рµ
5.1.15 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· СѓРєР°Р·Р°РЅРёСЏ РїСЂРёС‡РёРЅ
5.1.16 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ; РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј
5.1.17.1 |  | req=optional | prod=trade_acquiring | lot=common | term=pos | pm=common | РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ; РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±
5.1.17.2 |  | req=optional | prod=trade_acquiring | lot=common | term=smart | pm=common | С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ; С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±; РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ; 
5.2.1 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ; РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ
5.2.2 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё; РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure
5.2.3 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»Рє | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | СѓСЃС‚Р°РЅРѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё; РїРѕРґРіРѕС‚РѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё; РїСЂРѕРІРµ
5.2.4 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚ РђРІС‚РѕСЂРёР·Р°С†РёСЋ Р±РµР· РїРµСЂРµСЂС‹РІРѕРІ 24 С‡Р°СЃР° РІ СЃСѓС‚РєРё
5.2.5 | РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ | req=optional | prod=common | lot=common | term=common | pm=common | РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РјРµС‰РµРЅС‹ РїРѕ СѓРєР°Р·Р°РЅРЅРѕР№ СЃСЃС‹Р»РєРµ; РјР°С‚РµСЂРёР°Р»С‹ РґРѕСЃС‚СѓРїРЅС‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ
5.2.6 |  | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common | РћР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё; РћР±РµСЃРїРµС‡РµРЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё
5.2.7 |  | req=optional | prod=common | lot=common | term=common | pm=common | РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅР°СЏ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ; Р·Р°РјРµРЅР° РЅРµРёСЃРїСЂР°РІРЅРѕРіРѕ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РЅР° РёСЃРїСЂР°РІРЅС‹Р№ РЅРµ Рї
5.2.8 | Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ | req=mandatory | prod=common | lot=common | term=common | pm=common | РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅРµ РїРѕР·РґРЅРµРµ 2 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё; РґР°С‚Р° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё - СЂР°Р±РѕС‡РёР№
5.2.9 |  | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr | РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ QR-РєРѕРґР° РїР°СЂС‚РЅРµСЂР° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ
5.2.10 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | 
5.2.12 |  | req=optional | prod=internet_acquiring | lot=common | term=common | pm=qr | Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API Р±РµР· РіР°СЂР°РЅС‚РёР№
6.1 | Р’Р°Р¶РЅРѕ | req=mandatory | prod=common | lot=common | term=common | pm=common | СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№
6.2 | РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµ | req=mandatory | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°; РІ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РІРєР»СЋС‡РµРЅ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРј; РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»
6.3 |  | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common | Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РђРєС‚ РґРѕ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РђРєС‚ РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РІРјРµСЃС‚Рµ СЃРѕ СЃС‡РµС‚РѕРј-С„Р°РєС‚СѓСЂРѕР№ С„РѕСЂРјС‹ 363; Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ РѕРїСЂ
6.4 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Рё РІРѕР·РІСЂР°С‚РёС‚СЊ РЈРџР” (РїСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё); РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅ
6.5 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”; С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ; РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р±
6.6 |  | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common | РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р°РєС‚Р° Рё СЃС‡РµС‚Р° С„РѕСЂРјС‹ 363; С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ; РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂ
6.7 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | СѓРєР°Р·Р°РЅ СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°; СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂСѓР±Р»РµР№ РІРєР»СЋС‡Р°СЏ РќР”РЎ; СѓСЃС‚Р°РЅРѕРІР»РµРЅ РµР¶РµРјРµСЃСЏС‡РЅС‹Р№ РїРѕСЂСЏРґРѕРє РѕРїР»Р°С‚С‹
6.8 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚Рµ
6.9 |  | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РЎС‡РµС‚ РІС‹СЃС‚Р°РІР»СЏРµС‚СЃСЏ РїРѕ С„РѕСЂРјРµ в„–363; РЎС‡РµС‚ СЃРѕРґРµСЂР¶РёС‚ СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕ
6.10 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРё
6.11 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | РѕРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№; СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ С„РѕСЂРјР°; РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ
6.12 |  | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | РћРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№; РЎРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ; РћСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363; РџРѕР»СѓС‡Р°С‚РµР»СЊ РїР»Р°С‚РµР¶Р° - СЃС‡РµС‚ Р‘Р°
6.13 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | РїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РµР¶РµРјРµСЃСЏС‡РЅР°СЏ; СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РґРЅСЏРј РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»Р°; РїРµСЂРµСЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРё 
6.14 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»
6.15 |  | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚
6.16 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј; РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРё
6.17 |  | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | РѕРїР»Р°С‚Р° СЃРµСЂРІРёСЃР° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”; С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ; РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚
6.18 |  | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | РѕРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№; СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ; РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363; СЃСЂРѕРє РѕРїР»Р°С‚С‹ СЃС‡РёС‚Р°РµС‚СЃСЏ СЃ РґР°С‚С‹
6.20 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ | req=mandatory | prod=common | lot=common | term=common | pm=common | РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° РЅРµ РІР·РёРјР°РµС‚СЃСЏ; СѓРґРµСЂР¶Р°РЅРЅР°СЏ РїР»Р°С‚Р° Р·Р° СЂР°СЃС‡РµС‚С‹ РїСЂРё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РѕРїРµСЂР°С†РёРё РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
6.21 | РћС‚СЃСѓС‚СЃС‚РІРёРµ РєРѕРЅРєСЂРµС‚РЅРѕР№ С†РµРЅРЅС‹ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёРµРј | req=mandatory | prod=common | lot=common | term=common | pm=common | Р¦РµРЅР° РґРѕРіРѕРІРѕСЂР° РІ СЂСѓР±Р»СЏС…; РЈРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃСѓРјРјР° РІ СЂСѓР±Р»СЏС… Рё РєРѕРїРµР№РєР°С…; РЈРїРѕРјРёРЅР°РЅРёРµ Рѕ РІРєР»СЋС‡РµРЅРёРё РќР”РЎ
7.1 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”
7.2 | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° | req=mandatory | prod=common | lot=common | term=common | pm=common | РЁС‚СЂР°С„ РџСЂРµРґРїСЂРёСЏС‚РёСЋ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё.
7.3 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°
7.4 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№); РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РќР°С‡РёСЃР»РµРЅРё
7.5 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё, РёРјРµСЋС‰РёС… СЃС‚РѕРёРјРѕСЃС‚РЅРѕРµ РІС‹СЂР°Р¶РµРЅРёСЏ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ 
7.6 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, РЅРµ РёРјРµСЋС‰РµРіРѕ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ
7.7 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°
7.8 | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ(Р—Р°РєР°Р·С‡РёРєР°) Рё РџРѕРєСѓРїР°С‚РµР»СЏ | req=optional | prod=common | lot=common | term=common | pm=common | РћС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР° (Р�СЃРїРѕР»РЅРёС‚РµР»СЏ) Р·Р° СЃРїРѕСЂС‹ РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј (Р—Р°РєР°Р·С‡РёРєРѕРј) Рё РџРѕРєСѓРїР°С‚РµР»РµРј (РљР»РёРµРЅС‚ Р—Р°РєР°Р·С‡РёРєР°)
7.9 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё Р·Р°РґРµСЂР¶РєР°С… РїРµСЂРµРІРѕРґРѕРІ Р±РµР· СЃРІРѕРµР№ РІРёРЅС‹
7.10 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РЅРµ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РІ СЃРІСЏР·Рё СЃ РґРµР№СЃС‚РІРёРµРј Рё Р±РµР·РґРµР№СЃС‚РІРёРµРј С‚СЂРµС‚СЊРёС… Р»РёС†
7.11 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ РІ СЃР»СѓС‡Р°Рµ РёРЅРёС†РёРёСЂРѕРІР°РЅРёСЏ РёРј СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ РѕРїРµСЂР°С†РёР№
7.12 |  | req=optional | prod=common | lot=common | term=common | pm=common | РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р±Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё РїСЂРµРІС‹С€РµРЅРёРё Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°
7.13 |  | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅС‹Рµ РѕРїРµСЂР°С†РёРё РЅР° Р РµСЃСѓСЂСЃРµ
7.14 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±С‰РµРµ СѓС‚РІРµСЂР¶РґРµРЅРёРµ Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ РІ РЎРџР­Рџ
7.15 | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅРµСЃРµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ РіРѕРІРѕСЂРёС‚СЃСЏ РїСЂРѕ РЅРµСЃРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РґРµР№СЃС‚РІРёСЏ РїРµСЂСЃРѕРЅР°Р»Р°,  | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ РїРµСЂСЃРѕРЅР°Р»Р° СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР°; РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ РїРµСЂСЃРѕРЅР°Р»Р° РёРЅСЃС‚
7.16 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РЅРµ СЃРѕРІРµСЂС€Р°С‚СЊ РєРѕСЂСЂСѓРїС†РёРѕРЅРЅС‹С… Рё РёРЅС‹С… РїСЂРѕС‚РёРІРѕР·Р°РєРѕРЅРЅС‹С… РґРµР№СЃС‚РІРёР№ РїСЂРё Р»СЋР±С‹С… РѕРїРµСЂР°С†РёСЏС… РїРѕ РґРѕРіРѕРІРѕСЂСѓ
7.17 | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹  РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ Р±С‹Р»Рѕ СЃСѓР¶РµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё. | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ Р Р¤; РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ,
8.1 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РѕРїРёСЃР°РЅРёРµ С„РѕСЂСЃ-РјР°Р¶РѕСЂРЅС‹С… РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РєР°Рє РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕСЃРІРѕР±РѕР¶РґРµРЅРёСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё; РїРµСЂРµС‡РµРЅСЊ РєРѕРЅРєСЂРµС‚РЅС‹С… С„РѕСЂСЃ-РјР°Р¶РѕСЂРЅС‹С… СЃРѕР±С‹С‚РёР№ (СЃС‚РёС…РёР№РЅС‹Рµ Р±РµРґСЃС‚РІРёСЏ,
8.2 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹ РїСЂРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°С… РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹; РЎСЂРѕРє СѓРІРµРґРѕРјР»РµРЅРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹ РїСЂРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°С… РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹;
9.1 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | СЃРѕР±Р»СЋРґРµРЅ РїСЂРµС‚РµРЅР·РёРѕРЅРЅС‹Р№ РїРѕСЂСЏРґРѕРє СѓСЂРµРіСѓР»РёСЂРѕРІР°РЅРёСЏ СЃРїРѕСЂРѕРІ; СѓРєР°Р·Р°РЅ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РґРѕСЃСѓРґРµР±РЅС‹Р№ РїРѕСЂСЏРґРѕРє СЃ СѓРєР°Р·Р°РЅРёРµРј СЃСЂРѕРєР° СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№
9.2 | Р’Р°Р¶РµРЅ СЃСЂРѕРє СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№ | req=mandatory | prod=common | lot=common | term=common | pm=common | РЎСЂРѕРє СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№
9.3 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | 
10.1 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | СѓРєР°Р·Р°РЅР° РґР°С‚Р° РѕРєРѕРЅС‡Р°РЅРёСЏ РґРµР№СЃС‚РІРёСЏ РґРѕРіРѕРІРѕСЂР°; РѕРїСЂРµРґРµР»РµРЅ РїРѕСЂСЏРґРѕРє СѓС‡РµС‚Р° С†РµРЅС‹ РґРѕРіРѕРІРѕСЂР° РїСЂРё РѕРїСЂРµРґРµР»РµРЅРёРё СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ; СѓСЃС‚Р°РЅРѕРІР»РµРЅРѕ СЃРѕС…СЂР°РЅРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё
10.2 | Р’Р°Р¶РЅРѕ РѕРїРёСЃР°РЅРёРµ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ. Р’Р°Р¶РµРЅ СЃСЂРѕРє СѓРІРµРґРѕРјР»РµРЅРёСЏ Рѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёРё. | req=mandatory | prod=common | lot=common | term=common | pm=common | РџСЂР°РІРѕ Р»СЋР±РѕР№ СЃС‚РѕСЂРѕРЅС‹ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ; РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹ Рѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ; РџСЂР°РІРѕ Р‘
10.3 |  | req=mandatory | prod=common | lot=common | term=common | pm=common | РЎСЂРѕРєРё, РІ РєРѕС‚РѕСЂС‹Рµ РґРѕРіРѕРІРѕСЂ СЃС‡РёС‚Р°РµС‚СЃСЏ СЂР°СЃС‚РѕСЂРіРЅСѓС‚С‹Рј РІ СЃР»СѓС‡Р°Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РІРЅРµСЃСѓРґРµР±РЅРѕРј РїРѕСЂСЏРґРєРµ; РЎСЂРѕРєРё СЂР°СЃС‡РµС‚РѕРІ РїРѕСЃР»Рµ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРіРѕ РІРЅРµСЃСѓРґРµР±
11.1 |  | req=optional | prod=common | lot=common | term=common | pm=common | РџРµСЂРµС‡РёСЃР»РµРЅРёРµ РёСЃС‚РѕС‡РЅРёРєРѕРІ РїСЂР°РІРѕРІРѕРіРѕ СЂРµРіСѓР»РёСЂРѕРІР°РЅРёСЏ РѕС‚РЅРѕС€РµРЅРёР№ РЎС‚РѕСЂРѕРЅ; РўСЂРµР±РѕРІР°РЅРёРµ СЃРѕР±Р»СЋРґР°С‚СЊ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕ Р Р¤; РЈСЃР»РѕРІРёСЏ Рё РїРѕР»РѕР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°, РїСЂРѕС‚РёРІРѕСЂРµС‡Р°С‰
11.2 |  | req=optional | prod=common | lot=common | term=common | pm=common | РќРѕРјРµСЂР° РљР°СЂС‚/РџР»Р°С‚РµР¶РЅС‹С… СЃС‡РµС‚РѕРІ, РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ РџРѕРєСѓРїР°С‚РµР»РµР№, СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РёРЅС„РѕСЂРјР°С†РёСЏ Рѕ РїР»Р°С‚РµР¶Рµ СЏРІР»СЏСЋС‚СЃСЏ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРµР№; РћР±СЉСЏРІР»СЏРµС‚СЃСЏ
11.3 |  | req=optional | prod=common | lot=common | term=common | pm=common | РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РёРЅС‹Рј Р»РёС†Р°Рј РїРѕР»СѓС‡РµРЅРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ Рѕ Р·Р°С‰РёС‚РЅС‹С… СЌР»РµРјРµРЅС‚РѕРІ РєР°СЂС‚; РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РёРЅС‹Рј Р»РёС†Р°Рј РїРѕР»СѓС‡РµРЅРЅС‹Рµ СЃРІРµРґРµРЅ
11.4 |  | req=optional | prod=common | lot=common | term=common | pm=common | РёР·РјРµРЅРµРЅРёСЏ Рё РґРѕРїРѕР»РЅРµРЅРёСЏ РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РІ РїРёСЃСЊРјРµРЅРЅРѕР№ С„РѕСЂРјРµ; РїРѕРґРїРёСЃР°РЅС‹ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹РјРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏРјРё РѕР±РµРёС… СЃС‚РѕСЂРѕРЅ
11.5 |  | req=optional | prod=common | lot=common | term=common | pm=common | 
11.6 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р”РѕРіРѕРІРѕСЂ СЃРѕСЃС‚Р°РІР»РµРЅ РІ РѕРїСЂРµРґРµР»РµРЅРЅРѕРј РєРѕР»РёС‡РµСЃС‚РІРµ СЌРєР·РµРјРїР»СЏСЂРѕРІ; СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЌРєР·РµРјРїР»СЏСЂРѕРІ Р”РѕРіРѕРІРѕСЂР° РґР»СЏ Р‘Р°РЅРєР°; СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЌРєР·РµРјРїР»СЏСЂРѕРІ Р”РѕРіРѕРІРѕСЂР° РґР»
11.7 |  | req=optional | prod=common | lot=common | term=common | pm=common | РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РїСЂРёР»РѕР¶РµРЅРёСЏ СЏРІР»СЏСЋС‚СЃСЏ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ РґРѕРіРѕРІРѕСЂР°
11.8 |  | req=optional | prod=common | lot=common | term=common | pm=common | РџСЂРµРґРїСЂРёСЏС‚РёРµ (Р—Р°РєР°Р·С‡РёРє) Р·Р°РІРµСЂСЏРµС‚, С‡С‚Рѕ СЂРµР°Р»РёР·Р°С†РёСЏ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р Р¤
11.9 |  | req=optional | prod=common | lot=common | term=common | pm=common | Р·Р°РїСЂРµС‚ РїРµСЂРµРґР°С‡Рё РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Рё РїСЂР°РІ Р±РµР· РїРёСЃСЊРјРµРЅРЅРѕРіРѕ СЃРѕРіР»Р°СЃРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹; РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїРµСЂРµРґР°С‡Рё РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РґР»СЏ СЃР»СѓС‡Р°РµРІ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё СЃС‚РѕСЂРѕРЅС‹
11.10 |  | req=optional | prod=common | lot=common | term=common | pm=common | РџСЂРё СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР° РїРµСЂРµС…РѕРґСЏС‚ Рє РїСЂР°РІРѕРїСЂРµРµРјРЅРёРєСѓ; Р’ СЃР»СѓС‡Р°Рµ Р»РёРєРІРёРґР°С†РёРё РѕРґРЅРѕР№ РёР· СЃС‚РѕСЂРѕРЅ - СѓРґРѕРІР»РµС‚РІРѕСЂРµРЅРёРµ РёРјСѓС‰РµСЃС‚РІРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°
11.11 | Р•СЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ СѓРєР°Р·Р°РЅ СЃР°Р№С‚ - СЌС‚Рѕ РЅРµ СЏРІР»СЏРµС‚СЃСЏ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј | req=optional | prod=common | lot=common | term=common | pm=common | РЎСЂРѕРє, СЃ РєРѕС‚РѕСЂРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЃС‚Р°РЅРѕРІСЏС‚СЃСЏ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹РјРё Рє РІС‹РїРѕР»РµРЅРµРЅРёСЋ РїРѕСЃР»Рµ СЂР°Р·РјРµС‰РµРЅРёСЏ РЅР° РѕС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ
11.12 | Р’Р°Р¶РЅРѕ СЃР°РјРѕ РЅР°Р»РёС‡РёРµ С‚Р°РєРѕР№ РёР»Рё РїРѕС…РѕР¶РµР№ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё | req=optional | prod=common | lot=common | term=common | pm=common | РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚СЊ РѕС‚РїСЂР°РІРєРё СѓРІРµРґРѕРјР»РµРЅРёР№ Рё Р·Р°РїСЂРѕСЃРѕРІ, РµСЃР»Рё РѕС‚РїСЂР°РІР»РµРЅС‹ СЃРїРѕСЃРѕР±Р°РјРё РѕРїРёСЃР°РЅРЅС‹РјРё РІ РґРѕРіРѕРІРѕСЂРµ
11.13 |  | req=optional | prod=common | lot=common | term=common | pm=common | РџРµСЂРµС‡РµРЅСЊ РґРѕРєСѓРјРµРЅС‚РѕРІ, РїСЂРёР»РѕР¶РµРЅРЅС‹С… Рє РґРѕРіРѕРІРѕСЂСѓ

[Command succeeded with exit code 0]

