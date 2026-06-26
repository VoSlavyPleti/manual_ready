## Summarized at 2026-06-26T14:23:59.311656+00:00

Human: Matrix batch 4: sections 7-11
AI: I'll start by reading the skill file and understanding the task structure, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_wzCFqhpaXnwwHJhVBfSj9141', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/'}, 'id': 'call_01_886hWaB25d0YzHb7HzNz8175', 'type': 'tool_call'}]
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
    29	2. Use `inputs/matrix_legal_propositions.json` as the reusable normalized
    30	   Bank-standard matrix ledger.
    31	3. Build `contract_legal_propositions.json` from the contract in one
    32	   document-aware pass: extract each real clause/locator and fill the legal
    33	   proposition fields immediately.
    34	4. Derive compatibility artifacts `clause_index.json` and
    35	   `legal_propositions.json`; do not start matching until
    36	   `working_artifact_validation.json` is valid.
    37	5. Build the contract product profile and close out-of-scope matrix rows only
    38	   in the internal ledger.
    39	6. Read `references/matching-rules.md`; compare both directions: matrix
    40	   requirements to contract package, and material contract terms back to matrix
    41	   analogues.
    42	7. Read `references/status-rules.md`; assign group-level `aligned`,
    43	   `deviation`, `missing_in_contract`, or `extra_in_contract` based on source
    44	   text.
    45	8. Run Final QA, then write one final JSON and the mechanical XLSX export.
    46	
    47	## Purpose
    48	
    49	Find and explain:
    50	
    51	- Bank-standard matrix requirements preserved by the contract;
    52	- true analogues that deviate from the Bank standard;
    53	- applicable matrix requirements absent from the contract;
    54	- legally meaningful contract terms with no matrix analogue.
    55	- matrix requirements that are out of scope for the current contract profile,
    56	  closed in the internal ledger without final risk reporting.
    57	
    58	The review is risk-oriented. Missing a real risk is worse than marking a
    59	borderline issue as `deviation`, but weak thematic matches must not be promoted
    60	into legal links.
    61	
    62	## Inputs And Outputs
    63	
    64	Inputs:
    65	
    66	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    67	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    68	  applicability filters.
    69	- `inputs/matrix_legal_propositions.json`: reusable normalized matrix ledger
    70	  curated from `inputs/matrix.json`. Use it for matrix-side recall and status
    71	  evidence. It is a prepared input, not a per-run working artifact. If it is
    72	  absent or its ids/source text do not match `inputs/matrix.json`, stop with a
    73	  source setup error instead of rebuilding it during the contract run.
    74	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    75	  ids or real document locators visible in this file.
    76	
    77	Final outputs:
    78	
    79	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    80	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    81	
    82	Working artifacts belong under `/outputs/working/`.
    83	
    84	## Source Hierarchy
    85	
    86	Use the source text as the legal authority:
    87	
    88	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    89	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    90	3. Working ledgers as indexes and evidence aids.
    91	
    92	Do not decide status from extracted fields alone. When a status depends on a
    93	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    94	consequence, re-read the source text. Extracted fields are useful for recall,
    95	but source text controls the legal conclusion.
    96	
    97	## Required Artifacts And Contracts
    98	
    99	Create the artifacts in this order. Each later step depends on the earlier
   100	artifact contract. The purpose is to prevent legal facts from being lost
   101	between stages: `matrix_legal_propositions` preserves the stable Bank
   102	standard, `contract_legal_propositions` preserves contract legal meaning,
   103	compatibility artifacts expose valid locators, and `coverage_ledger` proves
   104	final closure.
   105	
   106	### 1. Source Preflight
   107	
   108	Check `inputs/contract.txt` before analysis:
   109	
   110	- real clause numbering is present;
   111	- deep clause numbers are not visibly collapsed or shifted;
   112	- repeated locators have enough context to distinguish source rows;
   113	- text is readable and not corrupted by encoding.
   114	
   115	If the contract text is not usable, stop and write
   116	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
   117	invalid text.
   118	
   119	### 2. Matrix Ledger Preflight
   120	
   121	Use `inputs/matrix_legal_propositions.json` as the matrix-side legal evidence
   122	ledger. It is curated before the run because the Bank matrix is stable across
   123	runs.
   124	
   125	Before contract analysis:
   126	
   127	- confirm it contains every `number` from `inputs/matrix.json`;
   128	- confirm each row has `source_ref.matrix_id`, concise `bank_standard`,
   129	  `matching_cues`, `legal_atoms`, `status_check_elements`, and hard-term
   130	  fields where relevant;
   131	- treat `legal_atoms` as the matrix-side atomic requirement list. When
   132	  `status_check_elements` contains atom ids, resolve them against
   133	  `legal_atoms`; do not expect the same text to be duplicated in both fields;
   134	- do not spend run time re-normalizing matrix rows;
   135	- if the curated file is missing, stale, or invalid, stop with a setup error
   136	  and do not begin contract analysis.
   137	
   138	The matrix ledger is an input optimization, not a new source of truth. It must
   139	stay compact and must not duplicate full `enriched_text`. If a status depends
   140	on a matrix hard term, use `source_ref.matrix_id` to verify it against
   141	`inputs/matrix.json`.
   142	
   143	### 3. Contract Legal Proposition Extraction
   144	
   145	Create `/outputs/working/contract_legal_propositions.json`.
   146	
   147	This is the primary contract working artifact. Extract the contract as a
   148	document, not as a universal numbering-regex result. For each real clause,
   149	subclause, appendix item, table row, or unnumbered operative provision, create
   150	one row and fill the legal fields immediately.
   151	
   152	Every row should include:
   153	
   154	- `id`: printed contract locator or nearest real source locator visible in the
   155	  contract;
   156	- `source_text` and concise `source_excerpt`;
   157	- `source_locator`, `line_start`, `line_end`, and section/context when useful;
   158	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   159	  `appendix`, `table`, or `technical`;
   160	- `materiality`: `evaluable`, `not_material`, `heading`, or
   161	  `needs_source_review`;
   162	- `final_allowed`: true only when the locator can appear as a final
   163	  `contract_id`;
   164	- `evidence_only`: true when the row can support evidence but is not a final
   165	  locator;
   166	- the legal proposition fields: `protected_party`, `bound_party`,
   167	  `right_or_obligation`, `legal_object`, `trigger`, `deadline`,
   168	  `amount_formula_cap`, `procedure_channel`, `liability_remedy`,
   169	  `scope_options`, `consequence`.
   170	
   171	The agent may use helper scripts to create a seed, but the seed is not
   172	authoritative. Review and repair the ledger against `inputs/contract.txt`
   173	before matching. Do not proceed while a legally meaningful row remains
   174	`needs_source_review`.
   175	
   176	Amounts, postal indexes, account numbers, table row ordinals, page artifacts,
   177	requisites, signatures, and form fields are not contract ids by themselves. If
   178	they are legally relevant, attach them to the nearest real source locator and
   179	cite them in evidence fields.
   180	
   181	See examples: `Contract Proposition Extraction Is One Pass`, `Amount Or Code
   182	Is Evidence, Not A Contract Id`.
   183	
   184	Duplicate printed ids are allowed only when their context makes the source row
   185	unambiguous. If two visible rows use the same printed locator in different
   186	appendices/tables, preserve context in `source_locator` / section fields rather
   187	than inventing semantic ids.
   188	
   189	### 4. Compatibility Artifacts
   190	
   191	Create:
   192	
   193	- `/outputs/working/clause_index.json`;
   194	- `/outputs/working/legal_propositions.json`.
   195	
   196	These are compatibility artifacts derived from the matrix and contract legal
   197	ledgers. They should not introduce new ids or legal propositions.
   198	
   199	`clause_index.json` is a source map only. Build its contract side from
   200	`contract_legal_propositions.json`; build its matrix side from
   201	`inputs/matrix.json` / `inputs/matrix_legal_propositions.json`.
   202	
   203	It must include:
   204	
   205	- every matrix `number`;
   206	- every contract row from `contract_legal_propositions.json`;
   207	- every numbered or named appendix/table item that contains an operative term
   208	  such as price, fee, currency, deadline, payment method, service scope,
   209	  acceptance condition, liability, or consequence;
   210	- source text or source locator for each row;
   211	- context for duplicate printed contract ids.
   212	
   213	Do not use `clause_index` to decide legal status. It only proves source
   214	coverage and valid ids. Never overwrite it with a batch subset.
   215	`legal_propositions.json` is the combined evidence ledger:
   216	
   217	- `matrix` is copied from compact `inputs/matrix_legal_propositions.json`;
   218	- `contract` is copied from the repaired
   219	  `/outputs/working/contract_legal_propositions.json`.
   220	
   221	After repairing `contract_legal_propositions.json`, derive these compatibility
   222	artifacts mechanically:
   223	
   224	```bash
   225	python skills/acquiring-discrepancy-analysis/scripts/derive_working_artifacts.py --matrix inputs/matrix.json --matrix-legal inputs/matrix_legal_propositions.json --contract-ledger outputs/working/contract_legal_propositions.json --working outputs/working --json-out outputs/working/derive_working_artifacts_report.json
   226	```
   227	
   228	The ledger is an evidence table, not a substitute for the source. Matching may
   229	use it to find candidates. Status must still be confirmed against source text
   230	because legal meaning may depend on context outside a normalized field.
   231	
   232	Run the mechanical check before matching:
   233	
   234	```bash
   235	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/working_artifact_validation.json
   236	```
   237	
   238	This is a stage gate, not a final QA item. Before starting matrix matching,
   239	contract-only review, merge, or status work:
   240	
   241	- `outputs/working/working_artifact_validation.json` must have `"valid": true`;
   242	- `legal_propositions.json` must not contain unresolved
   243	  `needs_source_review` rows;
   244	- every evaluable row must have source text and enough normalized legal fields
   245	  to preserve its legal meaning.
   246	
   247	If the check fails, repair the working artifact that failed and rerun this
   248	validator. Do not defer incomplete legal proposition rows to Final QA.
   249	
   250	The validator checks source-map completeness, matrix id coverage, contract row
   251	coverage, legal proposition row counts, unresolved `needs_source_review`, empty
   252	source text, suspicious locators, and weak evaluable rows. `"valid": true` means the working
   253	artifacts are complete enough to begin legal matching; it does not mean the
   254	legal conclusions are correct.
   255	
   256	### 5. Contract Product Profile
   257	
   258	Create `/outputs/working/contract_product_profile.json`.
   259	
   260	Extract from the contract:
   261	
   262	- product and payment channels;
   263	- lot/procurement type;
   264	- terminal/payment-device scope;
   265	- payment methods;
   266	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   267	
   268	Apply matrix filters before status:
   269	
   270	- `common` applies to every contract.
   271	- A filtered matrix item applies only when the profile matches
   272	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   273	- Mandatory applicable missing = high risk.
   274	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   275	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   276	  profile-based reason. Do not put them in final `unmatched_matrix`.
   277	- Optional applicable missing = low or conditional risk.
   278	- Slash-separated alternatives are options unless the matrix says all options
   279	  are mandatory.
   280	- Placeholder or blank in an applicable material term = low-risk `deviation`.
   281	- In `44_fz` public-procurement contracts, expect mandatory-law acceptance,
   282	  payment, reporting, termination, and control clauses. They may be legal
   283	  analogues, low-risk `extra_in_contract`, or internal ledger closures
   284	  depending on legal effect. Their presence is not itself a coverage error.
   285	- Matrix heading rows and non-operative matrix parents close as
   286	  `not_evaluable` in `coverage_ledger.matrix`; they are not final
   287	  `unmatched_matrix` risks.
   288	
   289	## Matching Method
   290	
   291	Read and follow `references/matching-rules.md` before matching. The short rule:
   292	final links require true legal analogues, not broad topic overlap. Perform both
   293	directions:
   294	
   295	- matrix to contract: find the contract package that covers each applicable
   296	  Bank-standard requirement;
   297	- contract to matrix: find matrix analogues for each material contract term or
   298	  classify it as `extra_in_contract`;
   299	- keep weak candidates out of final `links`; use them only as rejected
   300	  candidates or reasoning;
   301	- group ids only when they form one legal package.
   302	
   303	Use `references/comparison-patterns.md` for calibration examples such as weak
   304	candidate rejection, parent/child package retention, mandatory-law extras,
   305	appendix terms, contract-only materiality, and grouped coverage.
   306	
   307	## Status And Risk Method
   308	
   309	Read and follow `references/status-rules.md` before status classification. The
   310	short rule: status is group-level and source-text based.
   311	
   312	- `aligned`: the contract package preserves the matrix legal result.
   313	- `deviation`: a true analogue exists, but a material element is changed,
   314	  narrowed, weakened, omitted, shifted, or blank.
   315	- `missing_in_contract`: no true contract analogue exists for an applicable
   316	  matrix requirement.
   317	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   318	  analogue.
   319	- `not_material`, `out_of_scope`, and `not_applicable` are internal ledger
   320	  closures unless the output contract says otherwise.
   321	
   322	Compare hard terms directly: deadlines, amounts, formulas, caps, penalties,
   323	protected parties, triggers, procedures, liability, remedies, and consequences.
   324	Formal labels and mandatory-law mechanics do not create `deviation` when the
   325	legal result is preserved. An applicable blank or placeholder remains
   326	`deviation`, normally low risk.
   327	
   328	## Final QA
   329	
   330	Before writing final artifacts, perform release checks over already-built
   331	artifacts. Do not use Final QA as the first pass over missing working data.
   332	
   333	Blocking checks; repair before final JSON:
   334	
   335	- verify `clause_index` covers all source ids;
   336	- verify `outputs/working/working_artifact_validation.json` exists and is
   337	  valid; if it is missing or invalid, return to the Legal Proposition Ledger
   338	  stage instead of patching only the final JSON;
   339	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   340	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   341	  `coverage_ledger`;
   342	- verify every applicable evaluable matrix id is linked or in
   343	  `unmatched_matrix`;
   344	- verify out-of-scope / non-applicable matrix ids are not in final
   345	  `unmatched_matrix`;
   346	- verify every material contract id is closed as linked or extra;
   347	- verify `coverage_ledger.contract` closes every contract id from
   348	  `legal_propositions.contract` as `linked`, `extra_in_contract`, or
   349	  `not_material`;
   350	- verify `coverage_ledger` is derived from final `links`,
   351	  `unmatched_matrix`, and `unmatched_contract`;
   352	- verify every final id is visible in source text;
   353	- verify `aligned` has no material discrepancy;
   354	- verify every `deviation` has a named legal gap and evidence;
   355	- verify weak candidates are not in final `links`;
   356	- verify non-material contract rows are absent from final `unmatched_contract`;
   357	- verify every final `unmatched_matrix` item has `matrix_id`, `requirement`,
   358	  `status`, `risk_level`, and `risk`; `reason` is not a substitute for
   359	  `requirement`;
   360	- verify summary counts equal final arrays.
   361	
   362	Advisory cleanup; fix when practical, but do not rewrite legal conclusions
   363	without source support:
   364	
   365	- keep quotes concise;
   366	- keep risk explanations specific to the Bank;
   367	- keep XLSX as a mechanical export from JSON;
   368	- keep working files under `/outputs/working/`.
   369	
   370	## Output Discipline
   371	
   372	Read and follow `references/output-contract.md` before writing any final
   373	artifact. Do not duplicate or reinterpret the field contract locally.
   374	
   375	`links` carry group-level legal findings. `atomic_links` are traceability
   376	projections only and must inherit the group relationship. Do not assign
   377	separate final pair-level statuses.
   378	
   379	## Tools And Scripts
   380	
   381	Use helper scripts for mechanical work: source extraction, indexing,
   382	normalization checks, batch completeness, coverage validation, JSON schema
   383	checks, and Excel export. Do not put legal mapping or status decisions into
   384	hardcoded scripts.
   385	
   386	Required scripts live under `skills/acquiring-discrepancy-analysis/scripts/`
   387	and run with the project Python environment. If a script fails because of a
   388	path or environment issue, repair the command/path and rerun it. If a required
   389	validator is genuinely unavailable, do not skip the gate: perform the same
   390	mechanical checks manually, write the expected validation report under
   391	`/outputs/working/`, and state that the fallback was used.
   392	
   393	Useful mechanical scripts:
   394	
   395	- `bootstrap_source_artifacts.py`: creates seed working artifacts; seed
   396	  contract rows still require agent review.
   397	- `derive_working_artifacts.py`: derives `clause_index.json` and
   398	  `legal_propositions.json` from the repaired contract ledger.
   399	- `validate_working_artifacts.py`: stage gate before matching.
Tool: ['/.agents/', '/.codex/', '/.env', '/.git/', '/.gitignore', '/.venv/', '/ALL_DATA/', '/README.md', '/__pycache__/', '/conversation_history/', '/inputs/', '/llm.py', '/main.py', '/output/', '/outputs/', '/run_logs/', '/skills/', '/tools/']
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'in_progress'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'pending'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'pending'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract', 'status': 'pending'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]}, 'id': 'call_00_Xu6W2IbaHkPa1r6EzPGH2419', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'in_progress'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'pending'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'pending'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract', 'status': 'pending'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/matching-rules.md', 'limit': 500}, 'id': 'call_00_M0Mm4s6SL8XcVZxPuKYJ8423', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/status-rules.md', 'limit': 500}, 'id': 'call_01_hMOXaMK3UZk5mpZxjo8p9460', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_02_WltFwXwYMgYCPZGCB4sJ3614', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_03_YN7Z5RG96ZfeB7MPnfm61937', 'type': 'tool_call'}]
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
    39	If a linked detail clause is part of an enumerated legal package, also check
    40	the operative root or anchor row that grants the right, imposes the duty, or
    41	introduces the list. The anchor belongs in `contract_ids` when it carries the
    42	same legal object; it stays out when it is only a heading.
    43	
    44	For payment, acceptance, liability, termination, and document-exchange
    45	requirements, keep the legal package together only when the clauses govern one
    46	legal result. Do not merge sibling requirements just because they share a
    47	section parent.
    48	Public-procurement payment and acceptance clauses can be true analogues for
    49	Bank-standard payment, acceptance-document, and service-fee requirements when
    50	they preserve the same economic obligation and legal trigger. Do not reject
    51	them only because the route is EIS/acceptance/budget payment.
    52	
    53	For large matrices, preserve thematic continuity during review: complete the
    54	local payment, liability, termination, document-exchange, or product-scope
    55	cluster you are analyzing before switching context. This is a context-retention
    56	rule, not a requirement to create broad domain batches or crosswalk artifacts.
    57	
    58	See examples: `One Matrix Requirement Covered By Several Clauses`, `Parent And Child Package Retention`, `Non-Informative Parent`.
    59	
    60	## Fragment Shape Before Merge
    61	
    62	Every batch fragment should already follow the final output contract. Do not
    63	use `links` as a temporary bucket for missing or unresolved rows.
    64	
    65	- `links[].relationship` can only be `aligned` or `deviation`;
    66	- applicable matrix rows with no true analogue go to `unmatched_matrix`;
    67	- unresolved rows go to a `needs_review` list or are repaired before merge;
    68	- weak candidates stay in `rejected_candidates` or reasoning, not in
    69	  `contract_ids`;
    70	- a fragment with invalid relationships or ids should be repaired before it is
    71	  merged into the final artifact.
    72	
    73	See examples: `Missing Belongs In Unmatched Matrix`, `Weak Thematic Candidate`.
    74	
    75	## Contract To Matrix
    76	
    77	For each evaluable contract proposition, find the matrix analogue group. If no
    78	true analogue exists and the proposition has independent legal effect, classify
    79	it as `extra_in_contract`.
    80	
    81	Do not classify a contract term as `not_material` merely because no final
    82	finding was produced. `not_material` is reserved for headings, definitions
    83	without legal effect, requisites, signatures, blank forms, and purely
    84	technical rows.
    85	
    86	The contract-side review is complete only when every contract proposition from
    87	`legal_propositions.contract` is closed as `linked`, `extra_in_contract`, or
    88	`not_material` in `coverage_ledger.contract`. A material contract row cannot be
    89	left unclassified because the matrix-side pass already produced enough links.
    90	If it has a true matrix analogue, link it. If it has independent legal effect
    91	and no true analogue, report `extra_in_contract`. If it is only a heading,
    92	duplicate, blank form, or non-operative definition, close it as `not_material`.
    93	
    94	See examples: `Contract-Only Material Clause`, `Definition Without Legal Effect`, `Definition With Legal Effect`, `Contract-Only Pass Cannot Be Empty`.
    95	
    96	## Matrix Headings And Non-Operative Parents
    97	
    98	Matrix rows that only name a section, subsection, theme, or parent category
    99	close as `not_evaluable` in `coverage_ledger.matrix`. They never appear in
   100	final `unmatched_matrix`.
   101	
   102	If a matrix parent row contains its own right, duty, procedure, limitation,
   103	definition with legal effect, or consequence, treat it as evaluable. Otherwise
   104	use it only as context for children.
   105	
   106	See examples: `Matrix Heading Row`, `Non-Informative Parent`.
   107	
   108	## Appendix And Schedule Terms
   109	
   110	Appendix, schedule, specification, table, tariff, technical assignment, or
   111	payment-detail rows can be final contract locators when they contain an
   112	operative legal term: deadline, amount, currency, payment method, procedure,
   113	scope, product, acceptance condition, liability, remedy, or consequence.
   114	
   115	Index those rows in `clause_index` and `legal_propositions.contract` with real
   116	source locators visible in the contract text. Do not invent semantic ids. If an
   117	operative detail has no printed sub-id, use the nearest printed source locator
   118	as `contract_id` and describe the exact detail in `contract_evidence`,
   119	`coverage`, or `source_evidence`. Do not create synthetic locators with
   120	semantic suffixes, translated names, or helper-script ids.
   121	If the appendix or table has a printed item number, row label, or visible
   122	sub-locator, preserve that visible locator instead of collapsing the whole
   123	appendix into one generic id. Missing such a row is a source coverage problem,
   124	not a legal matching choice.
   125	
   126	If an appendix title only marks the beginning of a document part, keep it
   127	`evidence_only` / `not_material`; do not use it as a final `contract_id`.
   128	
   129	See examples: `Appendix Operative Term`, `Canonical Locator For Unnumbered Appendix Detail`, `Formal Label Difference`.
   130	
   131	## 44-FZ And Mandatory-Law Clauses
   132	
   133	Public-procurement clauses are not automatically extra and not automatically
   134	deviation:
   135	
   136	- if they regulate the same legal object as the matrix, link them and evaluate
   137	  `aligned` or `deviation`;
   138	- if they are mandatory-law mechanics with no matrix analogue and no adverse
   139	  Bank-specific risk, classify as low-risk `extra_in_contract` when they have
   140	  independent legal effect;
   141	- if they are headings or procedural scaffolding without independent legal
   142	  effect, keep them out of final `unmatched_contract`.
   143	
   144	See examples: `Procurement Mechanism As Analogue`, `Mandatory-Law Extra`.
   145	
   146	## Structural Duplicates
   147	
   148	If two contract clauses regulate the same legal object, same parties, same
   149	right or duty, same trigger, and same consequence, treat the later clause as a
   150	structural duplicate. It can inherit closure from the primary clause or close
   151	as `not_material` in `coverage_ledger.contract` with a reference to the
   152	primary clause. Do not create a new group or search for a different matrix id
   153	only to make the duplicate unique.
   154	
   155	See example: `Structural Duplicate Contract Clause`.
   156	
   157	## Grouping Discipline
   158	
   159	Group ids only for an indivisible legal package. Sibling matrix ids with
   160	different legal objects, channels, grounds, duties, or consequences should
   161	remain separate links even if they share a parent section.
   162	
   163	One matrix id may need several contract clauses. One contract clause may cover
   164	several matrix ids. The group must still describe one legal result.
   165	
   166	Payment and procedure clauses often sit near each other but remain separate
   167	legal results: payment amount, payment trigger, acceptance document, acceptance
   168	deadline, payment deadline, service fee, and evidence channel should not be
   169	merged into one broad group unless the matrix item itself requires the whole
   170	package. A gap in one payment or procedure element does not downgrade sibling
   171	links that preserve their own legal result.
   172	
   173	See examples: `Group-Level Status`, `Duplicate Gap Propagation`, `One Child Deviation Does Not Spread To Siblings`, `Payment Procedure Siblings Keep Separate Status`.
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
    58	For public-procurement contracts, an EIS acceptance route, budget-payment
    59	route, statutory document form, or customer-side payment act is not a
    60	deviation by itself. Treat it as `aligned` when it preserves the same economic
    61	obligation, payment trigger, evidence of performance, protected party, and
    62	enforceability. Use `deviation` only when the procurement mechanism changes a
    63	material hard term or weakens the Bank-standard legal result.
    64	
    65	Functional equivalence cannot override a missing or changed hard term.
    66	
    67	See examples: `Formal Label Difference`, `Low-Risk Note Does Not Force Deviation`, `Slash Options`.
    68	
    69	## 44-FZ And Mandatory-Law Calibration
    70	
    71	Mandatory 44-FZ/GK/EIS mechanics are not deviations by themselves. Evaluate
    72	their legal effect:
    73	
    74	- if the mandatory-law mechanism preserves the Bank-standard legal result,
    75	  keep `aligned`;
    76	- if it changes payment timing, acceptance control, withholding right,
    77	  penalty/cap, termination power, protected party, evidence channel, or
    78	  enforceability, use `deviation`;
    79	- if a mandatory-law clause exists only because public procurement requires it
    80	  and has no matrix analogue, use low-risk `extra_in_contract` when the clause
    81	  has independent legal effect;
    82	- if it is only a heading, formality, or procedural scaffold, close it as
    83	  `not_material` in the ledger.
    84	
    85	Do not mark a payment, acceptance, document, or termination group as
    86	`deviation` merely because the contract uses the statutory route required for
    87	the contract type. First identify the matrix legal object, then compare the
    88	actual legal result.
    89	
    90	See examples: `Procurement Mechanism As Analogue`, `Procurement Mechanism With Material Deviation`, `Mandatory-Law Extra`.
    91	
    92	## Bank Right Displaced By Mandatory Law
    93	
    94	When the matrix gives the Bank a unilateral right but the contract omits or
    95	restricts it because mandatory procurement law limits that unilateral power,
    96	do not treat the issue as harmless. The matrix requirement remains absent or
    97	weakened.
    98	
    99	Use `missing_in_contract` when no true contract analogue exists. Use
   100	`deviation` when the contract contains a narrower substitute. Risk is normally
   101	`medium` when statutory mechanisms partially compensate the Bank, and `high`
   102	when the omitted right is central and no practical substitute exists.
   103	
   104	See example: `Bank Right Displaced By Mandatory Law`.
   105	
   106	## Liability Package
   107	
   108	Before marking a liability group `aligned`, check amount, formula, cap,
   109	trigger, protected party, excluded delay/non-delay buckets, claim procedure,
   110	damages, and remedy survival across the package.
   111	
   112	General fault-based liability does not close a special Bank exemption, special
   113	penalty, or special cap rule unless it preserves the same protected party and
   114	legal consequence.
   115	
   116	When liability is split into root rights and child formulas, keep the direction
   117	of liability separate. A clause about customer delay, Bank delay, customer
   118	non-delay breach, and Bank non-delay breach may sit in one section but can map
   119	to different matrix requirements and different statuses.
   120	
   121	See examples: `Liability Group Review`, `Changed Amount, Formula, Cap, Or Penalty`.
   122	
   123	## Risk Level
   124	
   125	Use `risk_level` consistently:
   126	
   127	- `none`: only for `aligned`;
   128	- `low`: optional applicable missing, applicable placeholder, formal but
   129	  legally manageable gap, or mandatory-law extra with no adverse Bank-specific
   130	  effect;
   131	- `medium`: material deviation that can affect performance, evidence, payment,
   132	  control, liability, enforceability, or a Bank right displaced by mandatory
   133	  law with partial statutory compensation;
   134	- `high`: mandatory applicable missing, changed protected party, major
   135	  payment/remedy change, important Bank right omitted without substitute, or
   136	  broad contract-only risk.
   137	
   138	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   139	a short evidence-based reason. Use concise quotes rather than long excerpts.
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
   389	
   390	## 44. Operative Root Must Travel With Detail Clause
   391	
   392	Contract child clauses list grounds, exceptions, events, or remedies. A root
   393	clause directly before them grants the right or imposes the duty that makes the
   394	list legally operative.
   395	
   396	Result: when a child is linked, review the root. Include the root in the final
   397	contract package if it carries the same legal object. Do not include a root
   398	that is only a section heading.
   399	
   400	## 45. Service Compliance Warranty As Analogue
   401	
   402	Contract clause states that services must comply with applicable law or
   403	contractual requirements. Matrix contains a warranty, legal-compliance,
   404	payment-system-rules, or incorporated-documents requirement for the same
   405	services or transactions.
   406	
   407	Result: this can be a true analogue or companion framework clause. Compare
   408	scope and protected party. Do not use it as a universal substitute for
   409	unrelated duties.
   410	
   411	## 46. Public Payment Route Can Preserve Payment Result
   412	
   413	Matrix requires payment for Bank services or settlement services. Contract
   414	uses public-procurement acceptance, official payment documents, and budget
   415	payment instead of a commercial tariff-deduction route, but the counterparty
   416	still owes payment for the same service after the same performance/acceptance
   417	trigger.
   418	
   419	Result: link the payment/acceptance package. Use `aligned` when economic
   420	obligation, trigger, evidence, and enforceability are preserved. Use
   421	`deviation` only for a changed deadline, amount, party, trigger, withholding
   422	right, or other hard term.
   423	
   424	## 47. Liability Root And Directional Children
   425	
   426	Contract liability section has a general right to claim penalties, then
   427	separate child clauses for customer delay, Bank delay, customer non-delay
   428	breach, and Bank non-delay breach.
   429	
   430	Result: link the root plus the relevant directional child. Do not treat one
   431	direction as covering the opposite direction. Compare formula, cap, trigger,
   432	protected party, and exception for each directional liability result.
   433	
   434	## 48. Numbered Appendix Row Is A Final Locator
   435	
   436	Appendix contains a visible numbered item or table row with a currency, fee,
   437	payment method, service price, deadline, or other operative term.
   438	
   439	Result: index and use that visible appendix item as a final contract locator
   440	when it covers a matrix element. If the row has no visible sub-locator, use the
   441	nearest printed appendix/table locator and put the exact row detail in
   442	evidence. Do not invent semantic ids.
   443	
   444	## 49. Term And Survival Package
   445	
   446	Matrix requires contract term, early end by price exhaustion, and survival of
   447	liability after expiry. Contract has one clause for service period/price
   448	exhaustion and another clause for termination or post-termination settlements.
   449	
   450	Result: review the term package before declaring a miss. Link the clauses that
   451	cover term, price-exhaustion trigger, and survival/consequences. Status is
   452	`aligned` only if each material element is preserved.
   453	
   454	## 50. Final Missing Row Must Name Requirement
   455	
   456	Matrix requirement is applicable and has no true contract analogue.
   457	
   458	Result: final `unmatched_matrix` row must contain `matrix_id`, `requirement`,
   459	`status = missing_in_contract`, `risk_level`, and `risk`. A `reason` field may
   460	explain the conclusion, but it does not replace the missing requirement text.
   461	
   462	## 51. Contract Proposition Extraction Is One Pass
   463	
   464	Contract text has a clause with a printed locator, a duty, a deadline, and a
   465	payment consequence.
   466	
   467	Bad result: first create only a locator row, then lose the deadline during
   468	later legal normalization.
   469	
   470	Good result: create one `contract_legal_propositions` row with the same
   471	printed locator, full `source_text`, deadline, duty, legal object, parties, and
   472	consequence. Derive `clause_index` and `legal_propositions.contract` from that
   473	row.
   474	
   475	Result: matching and status use the same source-backed proposition; no hard
   476	term is lost between extraction stages.
   477	
   478	## 52. Amount Or Code Is Evidence, Not A Contract Id
   479	
   480	Contract text contains a standalone line with a contract price, postal index,
   481	bank account, table ordinal, or numerical value.
   482	
   483	Bad result: create a contract id such as `900000`, `354340`, or `1` only
   484	because the line starts with digits.
   485	
   486	Good result: attach the amount or code to the nearest real clause, appendix
   487	item, or table locator. Use the amount as `amount_formula_cap` or
   488	`source_evidence`, not as `contract_id`.
   489	
   490	Result: the value can affect `aligned` / `deviation`, but it cannot become a
   491	final locator.
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
    14	- `/outputs/working/contract_legal_propositions.json`
    15	- `/outputs/working/clause_index.json`
    16	- `/outputs/working/legal_propositions.json`
    17	- `/outputs/working/contract_product_profile.json`
    18	- `/outputs/working/coverage_ledger.json`
    19	
    20	The matrix-side legal ledger is curated before the run at
    21	`inputs/matrix_legal_propositions.json`. It must contain every matrix `number`
    22	from `inputs/matrix.json`, but it must stay compact: do not duplicate full
    23	`enriched_text` there. Use `source_ref.matrix_id` to read the full raw matrix
    24	row from `inputs/matrix.json` whenever source verification is needed. If this
    25	input is missing or invalid, stop with a setup error; do not rebuild it during
    26	contract review.
    27	
    28	`contract_legal_propositions.json` is the primary contract working artifact.
    29	It combines document-aware clause extraction and legal normalization in one
    30	pass. The agent may use scripts as a seed, but this file must be repaired
    31	against `inputs/contract.txt` before matching.
    32	
    33	`clause_index.json` is a compatibility source map derived from the matrix
    34	ledger and contract legal propositions. It contains source ids and text, but no
    35	final legal status. It is document-aware: locators come from the actual
    36	contract structure, not from a universal regex. Amounts, addresses, requisites,
    37	account numbers, page artifacts, and table ordinals are not final locators by
    38	themselves.
    39	
    40	`legal_propositions.json` is the combined legal evidence ledger. Its `matrix`
    41	array is copied from compact `inputs/matrix_legal_propositions.json`; its
    42	`contract` array is copied from the repaired
    43	`contract_legal_propositions.json`. Matrix rows use `source_ref` instead of
    44	duplicating full source text. Matrix `status_check_elements` may be atom-id
    45	references into `legal_atoms`; do not repeat the same text in both places.
    46	Contract rows must contain source text. It must contain:
    47	
    48	```json
    49	{
    50	  "matrix": [
    51	    {
    52	      "id": "<matrix number>",
    53	      "source_ref": {"matrix_id": "<matrix number>"},
    54	      "materiality": "evaluable|not_material|heading|needs_source_review",
    55	      "required_type": "mandatory|optional|unknown",
    56	      "applicability_filters": {},
    57	      "bank_standard": "<concise bank-standard requirement>",
    58	      "protected_party": "<party protected by the rule>",
    59	      "bound_party": "<party bound by the rule>",
    60	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    61	      "legal_object": "<regulated object>",
    62	      "matching_cues": ["<short legal cue>"],
    63	      "legal_atoms": [
    64	        {"atom_id": "a1", "category": "<element type>", "text": "<atomic legal element>"}
    65	      ],
    66	      "status_check_elements": ["a1"],
    67	      "hard_term_atom_ids": ["a1"],
    68	      "trigger": "<event/condition>",
    69	      "deadline": "<deadline if any>",
    70	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    71	      "procedure_channel": "<procedure/channel if any>",
    72	      "liability_remedy": "<liability/remedy if any>",
    73	      "consequence": "<legal consequence>"
    74	    }
    75	  ],
    76	  "contract": [
    77	    {
    78	      "id": "<printed contract locator>",
    79	      "source_text": "<contract clause text>",
    80	      "source_excerpt": "<short quote>",
    81	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    82	      "materiality": "evaluable|not_material|heading|needs_source_review",
    83	      "protected_party": "<party protected by the rule>",
    84	      "bound_party": "<party bound by the rule>",
    85	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    86	      "legal_object": "<regulated object>",
    87	      "trigger": "<event/condition>",
    88	      "deadline": "<deadline if any>",
    89	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    90	      "procedure_channel": "<procedure/channel if any>",
    91	      "liability_remedy": "<liability/remedy if any>",
    92	      "scope_options": ["<scope option>"],
    93	      "consequence": "<legal consequence>",
    94	      "final_allowed": true,
    95	      "evidence_only": false
    96	    }
    97	  ]
    98	}
    99	```
   100	
   101	Rows marked `needs_source_review` are not complete. Resolve them before
   102	substantive matching if they can affect a link, missing item, or contract-only
   103	finding.
   104	
   105	`contract_legal_propositions.json` uses the same row shape as
   106	`legal_propositions.contract`. A final `contract_id` may only use a row with
   107	`final_allowed = true`. Rows with `evidence_only = true` may support quotes and
   108	reasoning but must not appear as final ids.
   109	
   110	After the contract ledger is repaired, derive `clause_index.json` and
   111	`legal_propositions.json` mechanically:
   112	
   113	```bash
   114	python skills/acquiring-discrepancy-analysis/scripts/derive_working_artifacts.py --matrix inputs/matrix.json --matrix-legal inputs/matrix_legal_propositions.json --contract-ledger outputs/working/contract_legal_propositions.json --working outputs/working --json-out outputs/working/derive_working_artifacts_report.json
   115	```
   116	
   117	After creating or repairing `legal_propositions.json`, run
   118	`validate_working_artifacts.py` and write
   119	`/outputs/working/working_artifact_validation.json`. The validation report must
   120	be valid before substantive matching begins. If it is invalid, repair the
   121	working artifact first; do not wait until final JSON QA to discover incomplete
   122	legal proposition rows.
   123	
   124	## Final JSON Shape
   125	
   126	```json
   127	{
   128	  "analysis_profile": {
   129	    "contract_product_profile": {
   130	      "product": ["<selected product/channel>"],
   131	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
   132	      "terminal": ["<selected terminal/payment device>"],
   133	      "payment_method": ["<selected payment method>"],
   134	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
   135	    },
   136	    "source_preflight": {
   137	      "contract_numbering_valid": true,
   138	      "notes": []
   139	    }
   140	  },
   141	  "links": [
   142	    {
   143	      "matrix_ids": ["<matrix id>"],
   144	      "contract_ids": ["<contract locator>"],
   145	      "relationship": "aligned|deviation",
   146	      "legal_topic": "<short legal topic>",
   147	      "matrix_standard": "<bank standard requirement group>",
   148	      "contract_position": "<counterparty contract position group>",
   149	      "matrix_evidence": "<short matrix quote>",
   150	      "contract_evidence": "<short contract quote>",
   151	      "status_reason": "<group-level reason>",
   152	      "risk_level": "none|low|medium|high",
   153	      "discrepancies": [
   154	        {
   155	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   156	          "description": "<material difference>",
   157	          "risk": "<why this matters for the Bank>"
   158	        }
   159	      ]
   160	    }
   161	  ],
   162	  "atomic_links": [
   163	    {
   164	      "matrix_id": "<one matrix id>",
   165	      "contract_id": "<one contract locator>",
   166	      "relationship": "aligned|deviation",
   167	      "link_index": 0,
   168	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   169	      "coverage": "<what this contract locator contributes to the group>"
   170	    }
   171	  ],
   172	  "unmatched_matrix": [
   173	    {
   174	      "matrix_id": "<matrix id>",
   175	      "requirement": "<missing bank standard requirement>",
   176	      "source_evidence": "<short matrix quote>",
   177	      "status": "missing_in_contract",
   178	      "required_type": "mandatory|optional|unknown",
   179	      "applicability": "applicable|conditional|unknown",
   180	      "risk_level": "low|medium|high",
   181	      "risk": "<risk of omission>",
   182	      "rejected_candidates": [
   183	        {
   184	          "contract_id": "<weak candidate considered>",
   185	          "reason": "<why it is not a true analogue>"
   186	        }
   187	      ]
   188	    }
   189	  ],
   190	  "unmatched_contract": [
   191	    {
   192	      "contract_id": "<contract locator>",
   193	      "contract_position": "<extra legally significant contract term>",
   194	      "source_evidence": "<short contract quote>",
   195	      "status": "extra_in_contract",
   196	      "risk_level": "low|medium|high",
   197	      "risk": "<risk or impact for the Bank>",
   198	      "materiality_reason": "<why this has independent legal effect>"
   199	    }
   200	  ],
   201	  "coverage_ledger": {
   202	    "matrix": [
   203	      {
   204	        "matrix_id": "<matrix id>",
   205	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
   206	        "link_indices": [0],
   207	        "reason": "<short closure reason>"
   208	      }
   209	    ],
   210	    "contract": [
   211	      {
   212	        "contract_id": "<contract locator>",
   213	        "closure": "linked|extra_in_contract|not_material",
   214	        "link_indices": [0],
   215	        "reason": "<short closure reason>"
   216	      }
   217	    ]
   218	  },
   219	  "summary": {
   220	    "aligned_count": 0,
   221	    "deviation_count": 0,
   222	    "missing_in_contract_count": 0,
   223	    "extra_in_contract_count": 0
   224	  }
   225	}
   226	```
   227	
   228	## JSON Rules
   229	
   230	- `links` are group-level legal findings. One status applies to the whole
   231	  many-to-many group.
   232	- Intermediate batch fragments should use the same relationship values as the
   233	  final artifact. Do not put `missing_in_contract`, `extra_in_contract`,
   234	  `not_material`, unresolved rows, or candidate-only rows inside `links`.
   235	- `atomic_links` are traceability rows only. They inherit the group
   236	  `relationship`; do not invent pair-level final statuses.
   237	- `contract_ids` contain clauses that provide material coverage for the group.
   238	  Background clauses can be cited in reasoning, but should not become final
   239	  candidates unless they affect coverage or status.
   240	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   241	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   242	  matrix closures. Do not use it to invent final conclusions.
   243	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   244	  not a risk for the current product, lot, terminal, payment method, or legal
   245	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   246	  final `unmatched_matrix`.
   247	- `not_evaluable` matrix closures mean the row is a heading, non-operative
   248	  parent, or source row without an independent legal proposition. They stay in
   249	  `coverage_ledger.matrix` only and do not appear in final `unmatched_matrix`.
   250	- `unmatched_contract` contains only legally significant `extra_in_contract`
   251	  rows. Non-material rows stay in `coverage_ledger.contract`.
   252	- `coverage_ledger.contract` must close every contract row from
   253	  `contract_legal_propositions.json` / `legal_propositions.contract`: `linked`
   254	  when it appears in a final link,
   255	  `extra_in_contract` when it has independent legal effect and no matrix
   256	  analogue, or `not_material` when it is a heading, duplicate, blank form,
   257	  signature/requisites row, or non-operative definition. Do not leave material
   258	  contract rows out of the ledger.
   259	- `relationship = aligned` requires empty `discrepancies`, `risk_level = none`,
   260	  and text-grounded confirmation that the contract package preserves the matrix
   261	  legal result.
   262	- `relationship = deviation` requires at least one discrepancy with `type`,
   263	  `description`, and `risk`.
   264	- Missing mandatory applicable requirements should normally be `high` risk.
   265	  Missing optional applicable requirements should normally be `low` or
   266	  conditional risk.
   267	- Mandatory-law public-procurement extras with independent legal effect can be
   268	  `low` risk when they do not materially worsen the Bank position. They still
   269	  require a non-empty `risk` and `materiality_reason`.
   270	- All final ids must be visible in source files. Do not use corrected,
   271	  inferred, translated, parenthetical, or internal ids.
   272	- Final contract ids must exist in `outputs/working/clause_index.json`.
   273	  Presence of the same digits somewhere in `contract.txt` is not enough.
   274	- Final contract ids must also exist in
   275	  `outputs/working/contract_legal_propositions.json` with
   276	  `final_allowed = true`.
   277	- If an appendix, table, or technical assignment detail has no printed
   278	  sub-locator, use the nearest printed locator visible in the source as the
   279	  final `contract_id` and cite the detail in evidence fields. Do not create
   280	  synthetic ids such as semantic suffixes, translated labels, helper-script
   281	  names, or pseudo-paragraph locators.
   282	- Weak candidates do not appear in final `links`; use
   283	  `unmatched_matrix[].rejected_candidates`.
   284	- Every final `unmatched_matrix` item must use the exact field
   285	  `requirement`. A narrative field such as `reason`, `matrix_requirement`, or
   286	  `matrix_proposition` can be additional context, but it cannot replace
   287	  `requirement`.
   288	
   289	## Excel Output
   290	
   291	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   292	
   293	Sheet 1: `Contract-Matrix`
   294	
   295	Columns:
   296	
   297	1. `contract_id`
   298	2. `contract_summary`
   299	3. `matrix_ids`
   300	4. `status`
   301	5. `risk_level`
   302	6. `comment`
   303	
   304	Rules:
   305	
   306	- one row per group-level contract-to-matrix finding;
   307	- `matrix_ids` contains the full matrix id set for the group;
   308	- status is `aligned`, `deviation`, or `extra_in_contract`;
   309	- contract-only extras have blank `matrix_ids`.
   310	
   311	Sheet 2: `Only in Matrix`
   312	
   313	Columns:
   314	
   315	1. `matrix_id`
   316	2. `requirement`
   317	3. `required_type`
   318	4. `risk_level`
   319	5. `comment`
   320	
   321	Rules:
   322	
   323	- one row per final `unmatched_matrix` item;
   324	- include optional applicable missing as low/conditional risk;
   325	- do not include out-of-scope / not-applicable requirements;
   326	- do not include non-evaluable headings or purely technical rows.
   327	
   328	## Bad Output Patterns
   329	
   330	Do not output:
   331	
   332	- multiple competing final JSON files;
   333	- pair-level final statuses as the primary answer;
   334	- `deviation` for unselected slash alternatives;
   335	- `deviation` for heading/title/label changes alone;
   336	- final `unmatched_contract` rows for definitions without legal effect;
   337	- final `unmatched_matrix` rows for matrix headings or non-operative parents;
   338	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   339	  requirements;
   340	- final ids that exist only in helper scripts or working ledgers;
   341	- `links` with `relationship = missing_in_contract`;
   342	- `unmatched_matrix` rows that use `reason` instead of the required
   343	  `requirement` field;
   344	- an empty `unmatched_contract` section while material contract propositions
   345	  remain unclosed in `coverage_ledger.contract`;
   346	- `extra_in_contract` with empty risk;
   347	- `aligned` with non-empty discrepancies;
   348	- `missing_in_contract` where a weak candidate is silently treated as a link;
   349	- final conclusions based only on extracted fields without source-text evidence.
AI: Good, I've read all four reference files. Now let me read the inputs and existing working artifacts.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'in_progress'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'pending'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract', 'status': 'pending'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]}, 'id': 'call_00_RqvtyjiHNYAZ7XnnEX7M9020', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'in_progress'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'pending'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract', 'status': 'pending'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_L6t3XIoP2GOkYBOX5PqQ6287', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix_legal_propositions.json', 'limit': 200}, 'id': 'call_01_IWW9bBTs9BbVo808QLzF9425', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_02_AZbYzWa1V5C429TdPa2g6851', 'type': 'tool_call'}]
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
Tool:      1	{
     2	  "schema_version": "5.2-source-built-compact",
     3	  "source": {
     4	    "matrix_file": "inputs/matrix.json",
     5	    "row_count": 169,
     6	    "source_policy": "Built from original matrix.json only; previous matrix_legal_propositions.json was not used as a data source.",
     7	    "full_text_policy": "Full enriched_text stays in inputs/matrix.json and is resolved through source_ref.matrix_id for status checks."
     8	  },
     9	  "matrix": [
    10	    {
    11	      "id": "2.1",
    12	      "source_ref": {
    13	        "matrix_id": "2.1"
    14	      },
    15	      "materiality": "evaluable",
    16	      "required_type": "mandatory",
    17	      "applicability_filters": {
    18	        "only_for_product": "common",
    19	        "only_for_lot": "common",
    20	        "only_for_terminal": "common",
    21	        "payment_method": "common"
    22	      },
    23	      "bank_standard": "для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать...",
    24	      "protected_party": "Bank",
    25	      "bound_party": "counterparty",
    26	      "right_or_obligation": "обязанность: Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    27	      "legal_object": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    28	      "matching_cues": [
    29	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    30	        "Банк может отказать в регистрации ТСТ без указания причины",
    31	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    32	        "Информация о новых устройствах предоставляется с указанием их количества"
    33	      ],
    34	      "legal_atoms": [
    35	        {
    36	          "atom_id": "a1",
    37	          "category": "obligation",
    38	          "text": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом"
    39	        },
    40	        {
    41	          "atom_id": "a2",
    42	          "category": "right",
    43	          "text": "Банк может отказать в регистрации ТСТ без указания причины"
    44	        },
    45	        {
    46	          "atom_id": "a3",
    47	          "category": "obligation",
    48	          "text": "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении"
    49	        },
    50	        {
    51	          "atom_id": "a4",
    52	          "category": "obligation",
    53	          "text": "Информация о новых устройствах предоставляется с указанием их количества"
    54	        },
    55	        {
    56	          "atom_id": "a5",
    57	          "category": "obligation",
    58	          "text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в"
    59	        },
    60	        {
    61	          "atom_id": "a6",
    62	          "category": "right",
    63	          "text": "Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п 2.3 Договора"
    64	        },
    65	        {
    66	          "atom_id": "a7",
    67	          "category": "obligation",
    68	          "text": "При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде"
    69	        },
    70	        {
    71	          "atom_id": "a8",
    72	          "category": "trigger",
    73	          "text": "При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а..."
    74	        },
    75	        {
    76	          "atom_id": "a9",
    77	          "category": "right",
    78	          "text": "для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать"
    79	        }
    80	      ],
    81	      "status_check_elements": [
    82	        "a1",
    83	        "a2",
    84	        "a3",
    85	        "a4",
    86	        "a5",
    87	        "a6",
    88	        "a7",
    89	        "a8",
    90	        "a9"
    91	      ],
    92	      "trigger": "При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде...; При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также...",
    93	      "procedure_channel": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в...; Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п 2.3 Договора",
    94	      "consequence": "Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п 2.3 Договора"
    95	    },
    96	    {
    97	      "id": "2.2",
    98	      "source_ref": {
    99	        "matrix_id": "2.2"
   100	      },
   101	      "materiality": "evaluable",
   102	      "required_type": "mandatory",
   103	      "applicability_filters": {
   104	        "only_for_product": "common",
   105	        "only_for_lot": "common",
   106	        "only_for_terminal": "common",
   107	        "payment_method": "common"
   108	      },
   109	      "bank_standard": "валюта рубль РФ, другая валюта недопустима",
   110	      "protected_party": "Bank",
   111	      "bound_party": "counterparty",
   112	      "right_or_obligation": "сумма/формула: Расчёты производятся в рублях Российской Федерации",
   113	      "legal_object": "Расчёты производятся в рублях Российской Федерации",
   114	      "matching_cues": [
   115	        "Расчёты производятся в рублях Российской Федерации",
   116	        "валюта рубль РФ, другая валюта недопустима"
   117	      ],
   118	      "legal_atoms": [
   119	        {
   120	          "atom_id": "a1",
   121	          "category": "amount",
   122	          "text": "Расчёты производятся в рублях Российской Федерации"
   123	        },
   124	        {
   125	          "atom_id": "a2",
   126	          "category": "amount",
   127	          "text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации"
   128	        },
   129	        {
   130	          "atom_id": "a3",
   131	          "category": "amount",
   132	          "text": "валюта рубль РФ, другая валюта недопустима"
   133	        }
   134	      ],
   135	      "status_check_elements": [
   136	        "a1",
   137	        "a2",
   138	        "a3"
   139	      ],
   140	      "hard_term_atom_ids": [
   141	        "a1",
   142	        "a2",
   143	        "a3"
   144	      ],
   145	      "amount_formula_cap": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации"
   146	    },
   147	    {
   148	      "id": "2.3.1",
   149	      "source_ref": {
   150	        "matrix_id": "2.3.1"
   151	      },
   152	      "materiality": "evaluable",
   153	      "required_type": "mandatory",
   154	      "applicability_filters": {
   155	        "only_for_product": "common",
   156	        "only_for_lot": "common",
   157	        "only_for_terminal": "common",
   158	        "payment_method": "common"
   159	      },
   160	      "bank_standard": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса",
   161	      "protected_party": "Bank",
   162	      "bound_party": "counterparty",
   163	      "right_or_obligation": "процедура: Обмен информацией по электронной почте",
   164	      "legal_object": "Обмен информацией по электронной почте",
   165	      "matching_cues": [
   166	        "Обмен информацией по электронной почте",
   167	        "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
   168	        "Информация и документы, направленные по электронной почте, имеют юридическую силу",
   169	        "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса"
   170	      ],
   171	      "legal_atoms": [
   172	        {
   173	          "atom_id": "a1",
   174	          "category": "procedure",
   175	          "text": "Обмен информацией по электронной почте"
   176	        },
   177	        {
   178	          "atom_id": "a2",
   179	          "category": "procedure",
   180	          "text": "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту"
   181	        },
   182	        {
   183	          "atom_id": "a3",
   184	          "category": "procedure",
   185	          "text": "Информация и документы, направленные по электронной почте, имеют юридическую силу"
   186	        },
   187	        {
   188	          "atom_id": "a4",
   189	          "category": "procedure",
   190	          "text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по"
   191	        },
   192	        {
   193	          "atom_id": "a5",
   194	          "category": "procedure",
   195	          "text": "В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в"
   196	        },
   197	        {
   198	          "atom_id": "a6",
   199	          "category": "other",
   200	          "text": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса"
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
AI: Now I need to see the matrix sections 7-11. Let me find those sections in the matrix file and also continue reading the contract.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\',\'r\') as f:\n    m = json.load(f)\n# Find all numbers starting with 7, 8, 9, 10, 11\nfor row in m:\n    n = row[\'number\']\n    parts = n.split(\'.\')\n    if parts[0] in [\'7\',\'8\',\'9\',\'10\',\'11\']:\n        print(f\\"{n} | {row[\'required_type\']} | {row[\'only_for_product\']} | {row[\'only_for_lot\']} | {row[\'only_for_terminal\']} | {row[\'payment_method\']} | {row[\'main_idea\'][:120]}\\")\n"'}, 'id': 'call_00_Rvycy1LEf4CfX1aJBynl4862', 'type': 'tool_call'}]
Tool: [stderr] At line:41 char:24
[stderr] +         print(f\"{n} | {row['required_type']} | {row['only_for_produc ...
[stderr] +                        ~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:41 char:49
[stderr] + ... t(f\"{n} | {row['required_type']} | {row['only_for_product']} | {row[ ...
[stderr] +                                         ~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:41 char:77
[stderr] + ... d_type']} | {row['only_for_product']} | {row['only_for_lot']} | {row[ ...
[stderr] +                                             ~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:41 char:101
[stderr] + ... oduct']} | {row['only_for_lot']} | {row['only_for_terminal']} | {row[ ...
[stderr] +                                        ~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:41 char:130
[stderr] + ... lot']} | {row['only_for_terminal']} | {row['payment_method']} | {row[ ...
[stderr] +                                           ~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:41 char:156
[stderr] + ... r_terminal']} | {row['payment_method']} | {row['main_idea'][:120]}\")
[stderr] +                                               ~~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:41 char:180
[stderr] + ... r_terminal']} | {row['payment_method']} | {row['main_idea'][:120]}\")
[stderr] +                                                                       ~~~
[stderr] Unexpected token '\")
[stderr] "' in expression or statement.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : ExpressionsMustBeFirstInPipeline

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 /tools/run_matrix_sections.py'}, 'id': 'call_00_7yIh8eNLfcY4KVlARmQC9997', 'type': 'tool_call'}]
Tool: [stderr] C:\Python314\python.exe: can't open file 'C:\\tools\\run_matrix_sections.py': [Errno 2] No such file or directory

Exit code: 2
[Command failed with exit code 2]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/_list_matrix_batch4.py', 'content': 'import json\nwith open(\'/inputs/matrix.json\',\'r\') as f:\n    m = json.load(f)\nfor row in m:\n    n = row[\'number\']\n    parts = n.split(\'.\')\n    if parts[0] in [\'7\',\'8\',\'9\',\'10\',\'11\']:\n        print(f"{n} | {row[\'required_type\']} | {row[\'only_for_product\']} | {row[\'only_for_lot\']} | {row[\'only_for_terminal\']} | {row[\'payment_method\']} | {row[\'main_idea\'][:150]}")\n'}, 'id': 'call_00_Ebi2BpkeyqGCZ50tpIKv0112', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/_list_matrix_batch4.py
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/_list_matrix_batch4.py'}, 'id': 'call_00_YmjPwj85jZbwXkZi97fI1824', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\_list_matrix_batch4.py", line 2, in <module>
[stderr]     with open('/inputs/matrix.json','r') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/inputs/matrix.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'ls /inputs/'}, 'id': 'call_00_XITgJTvc8etlZJC5RJgq1747', 'type': 'tool_call'}]
Tool: 

    РљР°С‚Р°Р»РѕРі: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\inputs


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        25.06.2026     17:31         135560 contract.txt                                                         
-a----        23.06.2026     10:26         231542 matrix.json                                                          
-a----        26.06.2026     18:55         554881 matrix_legal_propositions.json                                       

[Command succeeded with exit code 0]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import json; m=json.load(open(\'C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2/inputs/matrix.json\',\'r\',encoding=\'utf-8\')); [print(f\\"{r[\'number\']} | {r[\'required_type\']} | {r[\'only_for_product\']} | {r[\'only_for_lot\']} | {r[\'only_for_terminal\']} | {r[\'payment_method\']} | {r[\'main_idea\'][:150]}\\") for r in m if r[\'number\'].split(\'.\')[0] in [\'7\',\'8\',\'9\',\'10\',\'11\']]"'}, 'id': 'call_00_7baKUDQPhBWpa3IsR8rS2064', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:178
[stderr] + ... ing='utf-8')); [print(f\"{r['number']} | {r['required_type']} | {r['o ...
[stderr] +                                              ~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:32 char:201
[stderr] + ... r['number']} | {r['required_type']} | {r['only_for_product']} | {r['o ...
[stderr] +                                           ~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:32 char:227
[stderr] + ... uired_type']} | {r['only_for_product']} | {r['only_for_lot']} | {r['o ...
[stderr] +                                               ~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:32 char:249
[stderr] + ... r_product']} | {r['only_for_lot']} | {r['only_for_terminal']} | {r['p ...
[stderr] +                                          ~~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:32 char:276
[stderr] + ... for_lot']} | {r['only_for_terminal']} | {r['payment_method']} | {r['m ...
[stderr] +                                             ~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:32 char:300
[stderr] + ... _terminal']} | {r['payment_method']} | {r['main_idea'][:150]}\") for  ...
[stderr] +                                            ~~~~~~~~~~~~~~~~~~~~~~
[stderr] Expressions are only allowed as the first element of a pipeline.
[stderr] At line:32 char:322
[stderr] + ... dea'][:150]}\") for r in m if r['number'].split('.')[0] in ['7','8',' ...
[stderr] +                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr] Unexpected token '\") for r in m if r['number'].split('.')[0] in ['7','8','9','10','11']]"' in expression or statement.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : ExpressionsMustBeFirstInPipeline

Exit code: 1
[Command failed with exit code 1]
AI: The shell is PowerShell, not bash. Let me use a script file approach.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/list_batch4.py', 'content': 'import json, os\nbase = r"C:\\Users\\gogel\\OneDrive\\Рабочий стол\\Проекты\\skillshot_manual_2"\nwith open(os.path.join(base, \'inputs\', \'matrix.json\'), \'r\', encoding=\'utf-8\') as f:\n    m = json.load(f)\nfor r in m:\n    n = r[\'number\']\n    parts = n.split(\'.\')\n    if parts[0] in [\'7\',\'8\',\'9\',\'10\',\'11\']:\n        print(f"{n} | {r[\'required_type\']} | {r[\'only_for_product\']} | {r[\'only_for_lot\']} | {r[\'only_for_terminal\']} | {r[\'payment_method\']} | {r[\'main_idea\'][:150]}")\n'}, 'id': 'call_00_6AAIKk3DUrRiuyA15aWl6827', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/list_batch4.py
AI: [{'name': 'execute', 'args': {'command': 'python3 C:/Users/gogel/OneDrive/Рабочий\\ стол/Проекты/skillshot_manual_2/outputs/working/list_batch4.py'}, 'id': 'call_00_jOkRueScoc4RKn68ldbF9358', 'type': 'tool_call'}]
Tool: [stderr] C:\Python314\python.exe: can't open file 'C:\\Users\\gogel\\OneDrive\\Р Р°Р±РѕС‡РёР№\\': [Errno 2] No such file or directory

Exit code: 2
[Command failed with exit code 2]
AI: [{'name': 'execute', 'args': {'command': 'python3 "/outputs/working/list_batch4.py"'}, 'id': 'call_00_3pv0Mx4ZMO6eBrWq1nvo5907', 'type': 'tool_call'}]
Tool: 7.1 | mandatory | common | common | common | common | 
7.2 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р°
7.3 | mandatory | common | common | common | common | 
7.4 | mandatory | common | common | common | common | 
7.5 | mandatory | common | common | common | common | 
7.6 | mandatory | common | common | common | common | 
7.7 | mandatory | common | common | common | common | 
7.8 | optional | common | common | common | common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ(Р—Р°РєР°Р·С‡РёРєР°) Рё РџРѕРєСѓРїР°С‚РµР»СЏ (РєР»РёРµРЅС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ)
7.9 | optional | common | common | common | common | 
7.10 | optional | common | common | common | common | 
7.11 | optional | common | common | common | common | 
7.12 | optional | common | common | common | common | 
7.13 | mandatory | internet_acquiring | common | common | common | 
7.14 | mandatory | common | common | common | common | 
7.15 | mandatory | common | common | common | common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅРµСЃРµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ РіРѕРІРѕСЂРёС‚СЃСЏ РїСЂРѕ РЅРµСЃРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РґРµР№СЃС‚РІРёСЏ РїРµСЂСЃРѕРЅР°Р»Р°, Р·РЅР°С‡РёС‚ СЌС‚РѕС‚ РїСѓРЅРєС‚ РЅРµ РѕС‚РЅРѕСЃРёС‚СЃСЏ
7.16 | mandatory | common | common | common | common | 
7.17 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹  РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ Р±С‹Р»Рѕ СЃСѓР¶РµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё.
8.1 | mandatory | common | common | common | common | 
8.2 | mandatory | common | common | common | common | 
9.1 | mandatory | common | common | common | common | 
9.2 | mandatory | common | common | common | common | Р’Р°Р¶РµРЅ СЃСЂРѕРє СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№
9.3 | mandatory | common | common | common | common | 
10.1 | mandatory | common | common | common | common | 
10.2 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ РѕРїРёСЃР°РЅРёРµ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ. Р’Р°Р¶РµРЅ СЃСЂРѕРє СѓРІРµРґРѕРјР»РµРЅРёСЏ Рѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёРё.
10.3 | mandatory | common | common | common | common | 
11.1 | optional | common | common | common | common | 
11.2 | optional | common | common | common | common | 
11.3 | optional | common | common | common | common | 
11.4 | optional | common | common | common | common | 
11.5 | optional | common | common | common | common | 
11.6 | optional | common | common | common | common | 
11.7 | optional | common | common | common | common | 
11.8 | optional | common | common | common | common | 
11.9 | optional | common | common | common | common | 
11.10 | optional | common | common | common | common | 
11.11 | optional | common | common | common | common | Р•СЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ СѓРєР°Р·Р°РЅ СЃР°Р№С‚ - СЌС‚Рѕ РЅРµ СЏРІР»СЏРµС‚СЃСЏ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј
11.12 | optional | common | common | common | common | Р’Р°Р¶РЅРѕ СЃР°РјРѕ РЅР°Р»РёС‡РёРµ С‚Р°РєРѕР№ РёР»Рё РїРѕС…РѕР¶РµР№ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё
11.13 | optional | common | common | common | common | 

[Command succeeded with exit code 0]
AI: Good, I can see the matrix IDs for sections 7-11. The output is garbled due to encoding but I can see the structure. Now let me read the full enriched_text for each of these matrix rows and the contract sections 7-11.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'completed'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'in_progress'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract', 'status': 'pending'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]}, 'id': 'call_00_hRiEYmxM5TrIHYxTTOIz2755', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'completed'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'in_progress'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract', 'status': 'pending'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]
AI: [{'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_00_TXvE1IKOiU1RUty1CwAQ7069', 'type': 'tool_call'}]
Tool: ['/outputs/working/_list_matrix_batch4.py', '/outputs/working/_preflight_check.py', '/outputs/working/batch3_matrix_legal.json', '/outputs/working/bootstrap_report.json', '/outputs/working/clause_index.json', '/outputs/working/contract_legal_propositions.json', '/outputs/working/contract_product_profile.json', '/outputs/working/derive_working_artifacts_report.json', '/outputs/working/legal_propositions.json', '/outputs/working/list_batch4.py', '/outputs/working/list_evaluable.py', '/outputs/working/preflight_check.py', '/outputs/working/repair_contract_ledger.py', '/outputs/working/working_artifact_validation.json']
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_00_bcq5Pb0G88ac8RuIxlv86035', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/working_artifact_validation.json'}, 'id': 'call_01_n61NeMErWJJozsPRoZV65265', 'type': 'tool_call'}]
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos_terminal", "smart_terminal"],
     5	  "payment_method": ["cards", "qr", "nfc"],
     6	  "legal_regime": "44_fz",
     7	  "profile_notes": [
     8	    "Contract is a 44-FZ public procurement contract for acquiring services",
     9	    "Customer: Federal State Budgetary Institution 'Caucasian State Nature Biosphere Reserve'",
    10	    "Services: trade acquiring with POS terminals and smart terminals",
    11	    "Payment methods: MIR, VISA, MasterCard cards; QR codes; NFC contactless",
    12	    "Terminals provided by Bank (Executor) free of charge for contract duration",
    13	    "Contract period: 01.03.2025 - 30.11.2025 or until max price exhausted",
    14	    "Max contract price: 1,900,000 RUB",
    15	    "Commission: included in unit price, no separate terminal fee or subscription",
    16	    "Settlement currency: RUB",
    17	    "No internet acquiring, no SberPay, no biometric payment in scope"
    18	  ],
    19	  "applicability_filters": {
    20	    "only_for_product": "trade_acquiring",
    21	    "only_for_lot": "44_fz",
    22	    "only_for_terminal": ["pos_terminal", "smart_terminal"],
    23	    "payment_method": ["cards", "qr", "nfc"]
    24	  }
    25	}
Tool:      1	{
     2	  "valid": true,
     3	  "errors": [],
     4	  "warnings": [],
     5	  "counts": {
     6	    "expected_matrix_ids": 169,
     7	    "matrix_legal_rows": 169,
     8	    "clause_index_matrix_ids": 169,
     9	    "clause_index_contract_rows": 185,
    10	    "source_contract_unique_ids": 185,
    11	    "duplicate_contract_ids": 0,
    12	    "contract_legal_proposition_rows": 185,
    13	    "legal_proposition_matrix_rows": 169,
    14	    "legal_proposition_contract_rows": 185,
    15	    "legal_proposition_rows": 354
    16	  },
    17	  "samples": {
    18	    "missing_matrix_ids": []
    19	  }
    20	}
AI: Good. Now let me read the full matrix rows for sections 7-11 and the contract sections 7-11. Let me get the matrix data first.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/dump_batch4.py', 'content': 'import json, os\nbase = r"C:\\Users\\gogel\\OneDrive\\Рабочий стол\\Проекты\\skillshot_manual_2"\nwith open(os.path.join(base, \'inputs\', \'matrix.json\'), \'r\', encoding=\'utf-8\') as f:\n    m = json.load(f)\n\nbatch4 = [r for r in m if r[\'number\'].split(\'.\')[0] in [\'7\',\'8\',\'9\',\'10\',\'11\']]\nwith open(os.path.join(base, \'outputs\', \'working\', \'batch4_matrix.json\'), \'w\', encoding=\'utf-8\') as f:\n    json.dump(batch4, f, ensure_ascii=False, indent=2)\nprint(f"Dumped {len(batch4)} rows")\nfor r in batch4:\n    print(f"\\n=== {r[\'number\']} ===")\n    print(f"required_type: {r[\'required_type\']}")\n    print(f"only_for_product: {r[\'only_for_product\']}")\n    print(f"only_for_lot: {r[\'only_for_lot\']}")\n    print(f"only_for_terminal: {r[\'only_for_terminal\']}")\n    print(f"payment_method: {r[\'payment_method\']}")\n    print(f"main_idea: {r[\'main_idea\']}")\n    print(f"enriched_text: {r[\'enriched_text\'][:300]}")\n    print(f"topics: {r[\'topics\']}")\n'}, 'id': 'call_00_60r0MIyPKMpMM7M2n7s55458', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/dump_batch4.py
AI: [{'name': 'execute', 'args': {'command': 'python3 "/outputs/working/dump_batch4.py"'}, 'id': 'call_00_lx6T5tTIyGQhi1e7g1iK7902', 'type': 'tool_call'}]
Tool: Dumped 38 rows

=== 7.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР° Рё Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤.
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР°', 'РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== 7.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р°
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ.
topics: ['РЁС‚СЂР°С„ РџСЂРµРґРїСЂРёСЏС‚РёСЋ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё.']

=== 7.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°.
topics: ['РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°']

=== 7.4 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµ
topics: ['Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№)', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РќР°С‡РёСЃР»РµРЅРёРµ РїРµРЅРё Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ.РћРїСЂРµРґРµР»РµРЅРёСЏ СЃСЂРѕРєР° РЅР°С‡Р°Р»Р° РЅР°С‡РёСЃР»РµРЅРёСЏ РїРµРЅРё', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РћРїСЂРµРґРµР»РµРЅРёРµ СЂР°Р·РјРµСЂР° РїРµРЅРё']

=== 7.5 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 10 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ
topics: ['Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё, РёРјРµСЋС‰РёС… СЃС‚РѕРёРјРѕСЃС‚РЅРѕРµ РІС‹СЂР°Р¶РµРЅРёСЏ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РґРѕРіРѕРІРѕСЂР°']

=== 7.6 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5
topics: ['Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, РЅРµ РёРјРµСЋС‰РµРіРѕ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ']

=== 7.7 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ Р¦РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°']

=== 7.8 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ(Р—Р°РєР°Р·С‡РёРєР°) Рё РџРѕРєСѓРїР°С‚РµР»СЏ (РєР»РёРµРЅС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ)
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј, РІРѕР·РЅРёРєР°СЋС‰РёРј РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј Рё РџРѕРєСѓРїР°С‚РµР»РµРј РІРѕ РІСЃРµС… СЃР»СѓС‡Р°СЏС…, РєРѕРіРґР° С‚Р°РєРёРµ СЃРїРѕСЂС‹ Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє РїСЂРµРґРјРµС‚Сѓ Р”РѕРіРѕРІРѕСЂР°, Р° С‚Р°РєР¶Рµ РїРѕ СЃРїРѕСЂР°Рј РІ РѕС‚РЅРѕС€РµРЅРёРё РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РѕРїР»Р°С‡РµРЅРЅС‹С… СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚С‹ /
topics: ['РћС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР° (Р�СЃРїРѕР»РЅРёС‚РµР»СЏ) Р·Р° СЃРїРѕСЂС‹ РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј (Р—Р°РєР°Р·С‡РёРєРѕРј) Рё РџРѕРєСѓРїР°С‚РµР»РµРј (РљР»РёРµРЅС‚ Р—Р°РєР°Р·С‡РёРєР°)']

=== 7.9 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєРё РїРµСЂРµРІРѕРґР° РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РµСЃР»Рё Р·Р°РґРµСЂР¶РєРё РїСЂРѕРёР·РѕС€Р»Рё РЅРµ РїРѕ РІРёРЅРµ Р‘Р°РЅРєР°.
topics: ['Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё Р·Р°РґРµСЂР¶РєР°С… РїРµСЂРµРІРѕРґРѕРІ Р±РµР· СЃРІРѕРµР№ РІРёРЅС‹']

=== 7.10 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°, РѕР±СѓСЃР»РѕРІР»РµРЅРЅРѕРµ РґРµР№СЃС‚РІРёСЏРјРё РёР»Рё Р±РµР·РґРµР№СЃС‚РІРёСЏРјРё С‚СЂРµС‚СЊРёС… Р»РёС†, РІ С‚РѕРј С‡РёСЃР»Рµ СѓС‡Р°СЃС‚РЅРёРєР°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹
topics: ['Р‘Р°РЅРє РЅРµ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РІ СЃРІСЏР·Рё СЃ РґРµР№СЃС‚РІРёРµРј Рё Р±РµР·РґРµР№СЃС‚РІРёРµРј С‚СЂРµС‚СЊРёС… Р»РёС†']

=== 7.11 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСѓРјРј РћРїРµСЂР°С†РёР№ РїРѕ РїСЂРёС‡РёРЅРµ РїСЂРѕРІРµРґРµРЅРёСЏ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ Р‘Р°РЅРєРѕРј РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РїСЂРѕРІРµРґРµРЅРёРµ РћРїРµСЂР°С†РёРё СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°
topics: ['Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ РІ СЃР»СѓС‡Р°Рµ РёРЅРёС†РёРёСЂРѕРІР°РЅРёСЏ РёРј СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ РѕРїРµСЂР°С†РёР№']

=== 7.12 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РІ СЃР»СѓС‡Р°Рµ РїСЂРµРІС‹С€РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р±Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё РїСЂРµРІС‹С€РµРЅРёРё Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°']

=== 7.13 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№, СЃРѕРІРµСЂС€РµРЅРЅС‹С… РЅР° Р РµСЃСѓСЂСЃРµ, РІ СЃР»СѓС‡Р°Рµ РЅРµРІС‹РїРѕР»РЅРµРЅРёСЏ Рї. 4.2.21.1 Р”РѕРіРѕРІРѕСЂР°
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅС‹Рµ РѕРїРµСЂР°С†РёРё РЅР° Р РµСЃСѓСЂСЃРµ']

=== 7.14 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјС‹Рµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў РІ РЎРџР­Рџ
topics: ['РћР±С‰РµРµ СѓС‚РІРµСЂР¶РґРµРЅРёРµ Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ РІ РЎРџР­Рџ']

=== 7.15 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅРµСЃРµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ РіРѕРІРѕСЂРёС‚СЃСЏ РїСЂРѕ РЅРµСЃРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РґРµР№СЃС‚РІРёСЏ РїРµСЂСЃРѕРЅР°Р»Р°, Р·РЅР°С‡РёС‚ СЌС‚РѕС‚ РїСѓРЅРєС‚ РЅРµ РѕС‚РЅРѕСЃРёС‚СЃСЏ Рє РґР°РЅРЅРѕРјСѓ
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРѕР»РЅРѕСЃС‚СЊСЋ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РґРµР№СЃС‚РІРёСЏ СЃРІРѕРµРіРѕ РїРµСЂСЃРѕРЅР°Р»Р°, СЃРІСЏР·Р°РЅРЅС‹Рµ СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° Рё РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹С… Р‘Р°РЅРєРѕРј
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ РїРµСЂСЃРѕРЅР°Р»Р° СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР°', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ РїРµСЂСЃРѕРЅР°Р»Р° РёРЅСЃС‚СЂСѓРєС†РёР№ Р‘Р°РЅРєР°']

=== 7.16 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё, РёСЃРїРѕР»РЅРµРЅРёРё, РёР·РјРµРЅРµРЅРёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РЎС‚РѕСЂРѕРЅС‹ РїСЂРёРЅРёРјР°СЋС‚ РЅР° СЃРµР±СЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РЅРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРµР№СЃС‚РІРёР№, РєРІР°Р»РёС„РёС†РёСЂСѓРµРјС‹С… РїСЂРёРјРµРЅРёРјС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј РєР°Рє В«РєРѕСЂСЂСѓРїС†РёСЏВ» , Р° С‚Р°РєР¶Рµ РёРЅС‹С… РґРµР№СЃС‚РІРёР№ (Р±РµР·РґРµР№СЃС‚РІРёСЏ), РЅР°СЂСѓС€Р°СЋС‰РёС… С‚СЂРµР±РѕРІР°РЅРёСЏ РїСЂРёРјРµРЅРёРјРѕРіРѕ Р·Р°Рє
topics: ['РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РЅРµ СЃРѕРІРµСЂС€Р°С‚СЊ РєРѕСЂСЂСѓРїС†РёРѕРЅРЅС‹С… Рё РёРЅС‹С… РїСЂРѕС‚РёРІРѕР·Р°РєРѕРЅРЅС‹С… РґРµР№СЃС‚РІРёР№ РїСЂРё Р»СЋР±С‹С… РѕРїРµСЂР°С†РёСЏС… РїРѕ РґРѕРіРѕРІРѕСЂСѓ']

=== 7.17 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹  РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ Р±С‹Р»Рѕ СЃСѓР¶РµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё.
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РїСЂРѕРІРµРґРµРЅРЅС‹С… РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ С‚СЂРµР±РѕРІР°РЅРёСЏРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё, РІ С‚РѕРј С‡РёСЃР»Рµ РЅРѕСЂРјР°С‚РёРІРЅС‹С… Р°РєС‚РѕРІ Р‘Р°РЅРєР° Р РѕСЃСЃРёРё, РїСЂР°РІРёР» РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё (РёР»Рё) Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ Р Р¤', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕС‚РІРµС‡Р°РµС‚ Р·Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РЅРѕСЂРјР°С‚РёРІРЅС‹Рј Р°РєС‚Р°Рј Р‘Р°РЅРєР° Р РѕСЃСЃРёРё', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕР±Р»СЋРґР°С‚СЊ РїСЂР°РІРёР»Р° РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РІ С‡Р°СЃС‚Рё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РѕС‚РЅРѕСЃРёС‚РµР»СЊРЅРѕ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№']

=== 8.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 8 В«Р¤РћР РЎ-РњРђР–РћР РќР«Р• РћР‘РЎРўРћРЇРўР•Р›Р¬РЎРўР’РђВ» в†’ РЎС‚РѕСЂРѕРЅР° Р”РѕРіРѕРІРѕСЂР° РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° С‡Р°СЃС‚РёС‡РЅРѕРµ РёР»Рё РїРѕР»РЅРѕРµ РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, РµСЃР»Рё СЌС‚Рѕ РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СЏРІРёР»РѕСЃСЊ СЃР»РµРґСЃС‚РІРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹, РІРѕР·РЅРёРєС€РёС… РІ СЂРµР·СѓР»СЊС‚Р°С‚Рµ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ С‡СЂРµР·РІС‹С‡Р°Р№РЅРѕРіРѕ С…Р°СЂР°РєС‚РµСЂР°, РєРѕС‚РѕСЂС‹Рµ 
topics: ['РѕРїРёСЃР°РЅРёРµ С„РѕСЂСЃ-РјР°Р¶РѕСЂРЅС‹С… РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РєР°Рє РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕСЃРІРѕР±РѕР¶РґРµРЅРёСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё', 'РїРµСЂРµС‡РµРЅСЊ РєРѕРЅРєСЂРµС‚РЅС‹С… С„РѕСЂСЃ-РјР°Р¶РѕСЂРЅС‹С… СЃРѕР±С‹С‚РёР№ (СЃС‚РёС…РёР№РЅС‹Рµ Р±РµРґСЃС‚РІРёСЏ, РїРѕР¶Р°СЂС‹ Рё С‚.Рґ.)', 'РїСЂРѕРґР»РµРЅРёРµ СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РґРѕРіРѕРІРѕСЂРЅС‹С… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ СЃРѕСЂР°Р·РјРµСЂРЅРѕ РІСЂРµРјРµРЅРё РґРµР№СЃС‚РІРёСЏ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРіРѕ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°']

=== 8.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 8 В«Р¤РћР РЎ-РњРђР–РћР РќР«Р• РћР‘РЎРўРћРЇРўР•Р›Р¬РЎРўР’РђВ» в†’ РџСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ, СѓРєР°Р·Р°РЅРЅС‹С… РІ Рї. 8.1 Р”РѕРіРѕРІРѕСЂР°, РЎС‚РѕСЂРѕРЅР°, РґР»СЏ РєРѕС‚РѕСЂРѕР№ СЃРѕР·РґР°Р»Р°СЃСЊ РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РёСЃРїРѕР»РЅРµРЅРёСЏ РµРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, РґРѕР»Р¶РЅР° РІ С‚РµС‡РµРЅРёРµ 24 (РґРІР°РґС†Р°С‚Рё С‡РµС‚С‹СЂРµС…) С‡Р°СЃРѕРІ РёР·РІРµСЃС‚РёС‚СЊ Рѕ РЅРёС… РґСЂСѓРіСѓСЋ РЎС‚РѕСЂРѕРЅСѓ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї.2.3 Р”РѕРіРѕРІРѕСЂР°, СЃ РѕР±
topics: ['РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹ РїСЂРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°С… РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹', 'РЎСЂРѕРє СѓРІРµРґРѕРјР»РµРЅРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹ РїСЂРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°С… РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹', 'СѓРєР°Р·Р°РЅРёРµ С…Р°СЂР°РєС‚РµСЂР° С„РѕСЂСЃ-РјР°Р¶РѕСЂРЅС‹С… РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ', 'РѕС†РµРЅРєР° РІР»РёСЏРЅРёСЏ РЅР° РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ', 'РїСЂРµРґРїРѕР»Р°РіР°РµРјС‹Р№ СЃСЂРѕРє РёСЃРїРѕР»РЅРµРЅРёСЏ РїСЂРё РЅР°Р»РёС‡РёРё РёРЅС„РѕСЂРјР°С†РёРё', 'РїСЂР°РІРѕ РЅР° СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РґРѕРіРѕРІРѕСЂР° РїСЂРё Р·Р°РґРµСЂР¶РєРµ Р±РѕР»РµРµ 3 РјРµСЃСЏС†РµРІ']

=== 9.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 9 В«РЈР Р•Р“РЈР›Р�Р РћР’РђРќР�Р• РЎРџРћР РћР’В» в†’ РЈСЂРµРіСѓР»РёСЂРѕРІР°РЅРёРµ СЃРїРѕСЂРѕРІ РЎС‚РѕСЂРѕРЅ СЃРѕРІРµСЂС€Р°РµС‚СЃСЏ РІ РїСЂРµС‚РµРЅР·РёРѕРЅРЅРѕРј РїРѕСЂСЏРґРєРµ
topics: ['СЃРѕР±Р»СЋРґРµРЅ РїСЂРµС‚РµРЅР·РёРѕРЅРЅС‹Р№ РїРѕСЂСЏРґРѕРє СѓСЂРµРіСѓР»РёСЂРѕРІР°РЅРёСЏ СЃРїРѕСЂРѕРІ', 'СѓРєР°Р·Р°РЅ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РґРѕСЃСѓРґРµР±РЅС‹Р№ РїРѕСЂСЏРґРѕРє СЃ СѓРєР°Р·Р°РЅРёРµРј СЃСЂРѕРєР° СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№']

=== 9.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ СЃСЂРѕРє СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№
enriched_text: Р РђР—Р”Р•Р› 9 В«РЈР Р•Р“РЈР›Р�Р РћР’РђРќР�Р• РЎРџРћР РћР’В» в†’ РџСЂРµС‚РµРЅР·РёРё СЂР°СЃСЃРјР°С‚СЂРёРІР°СЋС‚СЃСЏ РЎС‚РѕСЂРѕРЅР°РјРё РІ С‚РµС‡РµРЅРёРµ 10 (РґРµСЃСЏС‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ РёС… РїРѕР»СѓС‡РµРЅРёСЏ РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ.
topics: ['РЎСЂРѕРє СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№']

=== 9.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 9 В«РЈР Р•Р“РЈР›Р�Р РћР’РђРќР�Р• РЎРџРћР РћР’В» в†’ РЎРїРѕСЂС‹, РЅРµ СѓСЂРµРіСѓР»РёСЂРѕРІР°РЅРЅС‹Рµ РІ РїСЂРµС‚РµРЅР·РёРѕРЅРЅРѕРј РїРѕСЂСЏРґРєРµ, РїРѕРґР»РµР¶Р°С‚ СЂР°Р·СЂРµС€РµРЅРёСЋ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤.
topics: []

=== 10.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 10 В«РЎР РћРљ Р”Р•Р™РЎРўР’Р�РЇ Р”РћР“РћР’РћР Рђ Р� РџРћР РЇР”РћРљ Р•Р“Рћ Р РђРЎРўРћР Р–Р•РќР�РЇ в†’ РќР°СЃС‚РѕСЏС‰РёР№ Р”РѕРіРѕРІРѕСЂ РІСЃС‚СѓРїР°РµС‚ РІ СЃРёР»Сѓ СЃ РґР°С‚С‹ РµРіРѕ РїРѕРґРїРёСЃР°РЅРёСЏ РѕР±РµРёРјРё РЎС‚РѕСЂРѕРЅР°РјРё Рё РґРµР№СЃС‚РІСѓРµС‚ РїРѕ ___________ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ) РёР»Рё РґРѕ РёСЃС‡РµСЂРїР°РЅРёСЏ Р¦РµРЅС‹ РґРѕРіРѕРІРѕСЂР° (РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ С‚РѕРіРѕ, РєР°РєРѕРµ СЃРѕР±С‹С‚РёРµ РЅР°СЃС‚СѓРїРёС‚ РїРµСЂРІС‹Рј). РћРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР° РЅ
topics: ['СѓРєР°Р·Р°РЅР° РґР°С‚Р° РѕРєРѕРЅС‡Р°РЅРёСЏ РґРµР№СЃС‚РІРёСЏ РґРѕРіРѕРІРѕСЂР°', 'РѕРїСЂРµРґРµР»РµРЅ РїРѕСЂСЏРґРѕРє СѓС‡РµС‚Р° С†РµРЅС‹ РґРѕРіРѕРІРѕСЂР° РїСЂРё РѕРїСЂРµРґРµР»РµРЅРёРё СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ', 'СѓСЃС‚Р°РЅРѕРІР»РµРЅРѕ СЃРѕС…СЂР°РЅРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїРѕСЃР»Рµ РѕРєРѕРЅС‡Р°РЅРёСЏ СЃСЂРѕРєР° РґРѕРіРѕРІРѕСЂР°']

=== 10.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ РѕРїРёСЃР°РЅРёРµ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ. Р’Р°Р¶РµРЅ СЃСЂРѕРє СѓРІРµРґРѕРјР»РµРЅРёСЏ Рѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёРё.
enriched_text: Р РђР—Р”Р•Р› 10 В«РЎР РћРљ Р”Р•Р™РЎРўР’Р�РЇ Р”РћР“РћР’РћР Рђ Р� РџРћР РЇР”РћРљ Р•Р“Рћ Р РђРЎРўРћР Р–Р•РќР�РЇ в†’ Р›СЋР±Р°СЏ РЎС‚РѕСЂРѕРЅР° РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РІРїСЂР°РІРµ РµРіРѕ РґРѕСЃСЂРѕС‡РЅРѕ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РІРЅРµСЃСѓРґРµР±РЅРѕРј РїРѕСЂСЏРґРєРµ, РїРёСЃСЊРјРµРЅРЅРѕ СѓРІРµРґРѕРјРёРІ РѕР± СЌС‚РѕРј РґСЂСѓРіСѓСЋ РЎС‚РѕСЂРѕРЅСѓ РЅРµ РјРµРЅРµРµ С‡РµРј Р·Р° 30 (С‚СЂРёРґС†Р°С‚СЊ) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РґРѕ РґР°С‚С‹ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°РµРІ, РїСЂРµРґСѓСЃРјРѕС‚
topics: ['РџСЂР°РІРѕ Р»СЋР±РѕР№ СЃС‚РѕСЂРѕРЅС‹ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ', 'РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹ Рѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ', 'РџСЂР°РІРѕ Р‘Р°РЅРєР° СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ', 'РџСЂР°РІРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ']

=== 10.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 10 В«РЎР РћРљ Р”Р•Р™РЎРўР’Р�РЇ Р”РћР“РћР’РћР Рђ Р� РџРћР РЇР”РћРљ Р•Р“Рћ Р РђРЎРўРћР Р–Р•РќР�РЇ в†’ РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР° Р‘Р°РЅРєРѕРј РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РІРЅРµСЃСѓРґРµР±РЅРѕРј РїРѕСЂСЏРґРєРµ РІ СЃР»СѓС‡Р°СЏС…, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Рї. 5.1.8. РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР°, Р”РѕРіРѕРІРѕСЂ СЃС‡РёС‚Р°РµС‚СЃСЏ СЂР°СЃС‚РѕСЂРіРЅСѓС‚С‹Рј СЃ РґР°С‚С‹, СѓРєР°Р·Р°РЅРЅРѕР№ РІ РїРёСЃСЊРјРµРЅРЅРѕРј СѓРІРµРґРѕРјР»РµРЅРёРё Р‘Р°РЅРєР° Рѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёРё. РЎС‚РѕСЂРѕРЅ
topics: ['РЎСЂРѕРєРё, РІ РєРѕС‚РѕСЂС‹Рµ РґРѕРіРѕРІРѕСЂ СЃС‡РёС‚Р°РµС‚СЃСЏ СЂР°СЃС‚РѕСЂРіРЅСѓС‚С‹Рј РІ СЃР»СѓС‡Р°Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РІРЅРµСЃСѓРґРµР±РЅРѕРј РїРѕСЂСЏРґРєРµ', 'РЎСЂРѕРєРё СЂР°СЃС‡РµС‚РѕРІ РїРѕСЃР»Рµ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРіРѕ РІРЅРµСЃСѓРґРµР±РЅРѕРіРѕ РїРѕСЂСЏРґРєР° СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ - 18 РјРµСЃСЏС†РµРІ', 'РџРѕСЂСЏРґРѕРє РІС‹РїР»Р°С‚С‹ СЃСѓРјРј РѕРїРµСЂР°С†РёР№ РѕРїСЂРµРґРµР»РµРЅ РІ РїСѓРЅРєС‚Р°С… 5.1.3, 5.1.4 Рё СЂР°Р·РґРµР»Рµ 6']

=== 11.1 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ РЎС‚РѕСЂРѕРЅС‹ СЃРѕРіР»Р°С€Р°СЋС‚СЃСЏ, С‡С‚Рѕ РёСЃС‚РѕС‡РЅРёРєР°РјРё РїСЂР°РІРѕРІРѕРіРѕ СЂРµРіСѓР»РёСЂРѕРІР°РЅРёСЏ РѕС‚РЅРѕС€РµРЅРёР№ РЎС‚РѕСЂРѕРЅ РІ СЂР°РјРєР°С… Р”РѕРіРѕРІРѕСЂР° СЏРІР»СЏСЋС‚СЃСЏ РЅР°СЃС‚РѕСЏС‰РёРµ Р”РѕРіРѕРІРѕСЂ, РґРµР№СЃС‚РІСѓСЋС‰РµРµ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕ Р Р¤, РїСЂР°РІРёР»Р°, СЃС‚Р°РЅРґР°СЂС‚С‹ Рё СЂРµРєРѕРјРµРЅРґР°С†РёРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РїСЂРё СѓСЃР»РѕРІРёРё РёС… РЅРµ РїСЂРѕС‚РёРІРѕСЂРµС‡РёСЏ РґРµР№СЃС‚РІСѓСЋС‰РµРјСѓ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ Р Р¤
topics: ['РџРµСЂРµС‡РёСЃР»РµРЅРёРµ РёСЃС‚РѕС‡РЅРёРєРѕРІ РїСЂР°РІРѕРІРѕРіРѕ СЂРµРіСѓР»РёСЂРѕРІР°РЅРёСЏ РѕС‚РЅРѕС€РµРЅРёР№ РЎС‚РѕСЂРѕРЅ', 'РўСЂРµР±РѕРІР°РЅРёРµ СЃРѕР±Р»СЋРґР°С‚СЊ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕ Р Р¤', 'РЈСЃР»РѕРІРёСЏ Рё РїРѕР»РѕР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°, РїСЂРѕС‚РёРІРѕСЂРµС‡Р°С‰РёРµ РїСЂР°РІРёР»Р° РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РїСЂРёРІРµРґРµРЅС‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ']

=== 11.2 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Р�РЅС„РѕСЂРјР°С†РёСЏ, РїРѕР»СѓС‡РµРЅРЅР°СЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ СЂР°РјРєР°С… РёСЃРїРѕР»РЅРµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° (РЅРѕРјРµСЂР° РљР°СЂС‚/РџР»Р°С‚РµР¶РЅС‹С… СЃС‡РµС‚РѕРІ, РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ РџРѕРєСѓРїР°С‚РµР»РµР№, СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РёРЅС„РѕСЂРјР°С†РёСЏ Рѕ РїР»Р°С‚РµР¶Рµ), СЏРІР»СЏРµС‚СЃСЏ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕР№ Рё РЅРµ РїРѕРґР»РµР¶РёС‚ РїРµСЂРµРґР°С‡Рµ С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°РµРІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… 
topics: ['РќРѕРјРµСЂР° РљР°СЂС‚/РџР»Р°С‚РµР¶РЅС‹С… СЃС‡РµС‚РѕРІ, РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ РџРѕРєСѓРїР°С‚РµР»РµР№, СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РёРЅС„РѕСЂРјР°С†РёСЏ Рѕ РїР»Р°С‚РµР¶Рµ СЏРІР»СЏСЋС‚СЃСЏ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРµР№', 'РћР±СЉСЏРІР»СЏРµС‚СЃСЏ Р·Р°РїСЂРµС‚ РЅР° РїРµСЂРµРґР°С‡Сѓ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј', 'Р”Р°С‘С‚СЃСЏ СЂР°Р·СЂРµС€РµРЅРёРµ РЅР° РїРµСЂРµРґР°С‡Сѓ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё СЂР°Р·СЂРµС€РµРЅР°, С‚РѕР»СЊРєРѕ РµСЃР»Рё СЌС‚Рѕ С‚СЂРµР±РѕРІР°РЅРёРµ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° РёР»Рё СѓСЃР»РѕРІРёРµ РґРѕРіРѕРІРѕСЂР°']

=== 11.3 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РїРѕР»СѓС‡РµРЅРЅС‹Рµ РІ С…РѕРґРµ РёСЃРїРѕР»РЅРµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° СЃРІРµРґРµРЅРёСЏ, РІРєР»СЋС‡Р°СЏ:
вЂў РѕРїРёСЃР°РЅРёРµ Р·Р°С‰РёС‚РЅС‹С… СЌР»РµРјРµРЅС‚РѕРІ РљР°СЂС‚;
вЂў С‚РµС…РЅРѕР»РѕРіРёСЋ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№;
вЂў РёРЅС„РѕСЂРјР°С†РёСЋ РѕР± СѓРїСЂР°РІР»РµРЅРёРё, С„РёРЅР°РЅСЃРѕРІРѕР№ Рё РёРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РЎС‚РѕСЂРѕРЅ;
вЂў РёРЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёСЋ, СЂР°Р·РіР»Р°С€РµРЅРёРµ РєРѕС‚РѕСЂРѕР№ РјРѕР¶РµС‚ Рї
topics: ['РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РёРЅС‹Рј Р»РёС†Р°Рј РїРѕР»СѓС‡РµРЅРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ Рѕ Р·Р°С‰РёС‚РЅС‹С… СЌР»РµРјРµРЅС‚РѕРІ РєР°СЂС‚', 'РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РёРЅС‹Рј Р»РёС†Р°Рј РїРѕР»СѓС‡РµРЅРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ Рѕ С‚РµС…РЅРѕР»РѕРіРёРё РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№', 'РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РёРЅС‹Рј Р»РёС†Р°Рј РїРѕР»СѓС‡РµРЅРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ Рѕ С„РёРЅР°РЅСЃРѕРІРѕРј СЃРѕСЃС‚РѕСЏРЅРёРё СЃС‚РѕСЂРѕРЅ', 'РЎС‚РѕСЂРѕРЅС‹ РѕР±СЏР·СѓСЋС‚СЃСЏ РЅРµ СЂР°Р·РіР»Р°С€Р°С‚СЊ РёРЅС‹Рј Р»РёС†Р°Рј РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёСЋ Р±РµР· СЃРѕРіР»Р°СЃРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹']

=== 11.4 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Р’СЃРµ РёР·РјРµРЅРµРЅРёСЏ Рё РґРѕРїРѕР»РЅРµРЅРёСЏ Рє РЅР°СЃС‚РѕСЏС‰РµРјСѓ Р”РѕРіРѕРІРѕСЂСѓ, РєСЂРѕРјРµ РґРѕРєСѓРјРµРЅС‚РѕРІ, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р”РѕРіРѕРІРѕСЂРµ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рµ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°, РґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹ Р»РёС€СЊ РІ С‚РѕРј СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РѕРЅРё СЃРѕРІРµСЂС€РµРЅС‹ РІ РїРёСЃСЊРјРµРЅРЅРѕР№ С„РѕСЂРјРµ, Рё РїРѕРґРїРёСЃР°РЅС‹ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹РјРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏРјРё РЎ
topics: ['РёР·РјРµРЅРµРЅРёСЏ Рё РґРѕРїРѕР»РЅРµРЅРёСЏ РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РІ РїРёСЃСЊРјРµРЅРЅРѕР№ С„РѕСЂРјРµ', 'РїРѕРґРїРёСЃР°РЅС‹ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹РјРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏРјРё РѕР±РµРёС… СЃС‚РѕСЂРѕРЅ']

=== 11.5 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Р’СЃРµ РёРјРµРІС€РёРµ РјРµСЃС‚Рѕ РґРѕ РїРѕРґРїРёСЃР°РЅРёСЏ РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР° СЃРѕРіР»Р°С€РµРЅРёСЏ, РїРµСЂРµРіРѕРІРѕСЂС‹ Рё РїРµСЂРµРїРёСЃРєР° РјРµР¶РґСѓ РЎС‚РѕСЂРѕРЅР°РјРё РїРѕ РІРѕРїСЂРѕСЃР°Рј, РёР·Р»РѕР¶РµРЅРЅС‹Рј РІ РЅР°СЃС‚РѕСЏС‰РµРј Р”РѕРіРѕРІРѕСЂРµ, СѓС‚СЂР°С‡РёРІР°СЋС‚ СЃРёР»Сѓ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР°.
topics: []

=== 11.6 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ РќР°СЃС‚РѕСЏС‰РёР№ Р”РѕРіРѕРІРѕСЂ СЃРѕСЃС‚Р°РІР»РµРЅ РІ ________ СЌРєР·РµРјРїР»СЏСЂР°С…, _________ СЌРєР·РµРјРїР»СЏСЂ(-Р°) РґР»СЏ Р‘Р°РЅРєР°, РѕРґРёРЅ СЌРєР·РµРјРїР»СЏСЂ РґР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ
topics: ['Р”РѕРіРѕРІРѕСЂ СЃРѕСЃС‚Р°РІР»РµРЅ РІ РѕРїСЂРµРґРµР»РµРЅРЅРѕРј РєРѕР»РёС‡РµСЃС‚РІРµ СЌРєР·РµРјРїР»СЏСЂРѕРІ', 'СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЌРєР·РµРјРїР»СЏСЂРѕРІ Р”РѕРіРѕРІРѕСЂР° РґР»СЏ Р‘Р°РЅРєР°', 'СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЌРєР·РµРјРїР»СЏСЂРѕРІ Р”РѕРіРѕРІРѕСЂР° РґР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']

=== 11.7 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Р’СЃРµ РџСЂРёР»РѕР¶РµРЅРёСЏ Рє РЅР°СЃС‚РѕСЏС‰РµРјСѓ Р”РѕРіРѕРІРѕСЂСѓ СЏРІР»СЏСЋС‚СЃСЏ РµРіРѕ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РїСЂРёР»РѕР¶РµРЅРёСЏ СЏРІР»СЏСЋС‚СЃСЏ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ РґРѕРіРѕРІРѕСЂР°']

=== 11.8 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ Р·Р°РІРµСЂСЏРµС‚, С‡С‚Рѕ СЂРµР°Р»РёР·Р°С†РёСЏ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РІ РўРЎРў РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р Р¤
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ (Р—Р°РєР°Р·С‡РёРє) Р·Р°РІРµСЂСЏРµС‚, С‡С‚Рѕ СЂРµР°Р»РёР·Р°С†РёСЏ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р Р¤']

=== 11.9 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ РќРё РѕРґРЅР° РёР· РЎС‚РѕСЂРѕРЅ РЅРµ РІРїСЂР°РІРµ РїРµСЂРµРґР°РІР°С‚СЊ СЃРІРѕРё РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё Рё/РёР»Рё РїСЂР°РІР° РїРѕ Р”РѕРіРѕРІРѕСЂСѓ С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј Р±РµР· РїРёСЃСЊРјРµРЅРЅРѕРіРѕ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ СЃ РґСЂСѓРіРѕР№ РЎС‚РѕСЂРѕРЅРѕР№, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°СЏ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ
topics: ['Р·Р°РїСЂРµС‚ РїРµСЂРµРґР°С‡Рё РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Рё РїСЂР°РІ Р±РµР· РїРёСЃСЊРјРµРЅРЅРѕРіРѕ СЃРѕРіР»Р°СЃРёСЏ РґСЂСѓРіРѕР№ СЃС‚РѕСЂРѕРЅС‹', 'РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїРµСЂРµРґР°С‡Рё РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РґР»СЏ СЃР»СѓС‡Р°РµРІ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё СЃС‚РѕСЂРѕРЅС‹']

=== 11.10 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’  Р’ СЃР»СѓС‡Р°Рµ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР° РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РІ РїРѕР»РЅРѕРј РѕР±СЉРµРјРµ РїРµСЂРµС…РѕРґСЏС‚ Рє РїСЂР°РІРѕРїСЂРµРµРјРЅРёРєСѓ. Р’ СЃР»СѓС‡Р°Рµ Р»РёРєРІРёРґР°С†РёРё РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ РёРјСѓС‰РµСЃС‚РІРµРЅРЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ РґСЂСѓРіРѕР№ РЎС‚РѕСЂРѕРЅС‹ СѓРґРѕРІР»РµС‚РІРѕСЂСЏСЋС‚СЃСЏ Р·Р° СЃС‡РµС‚ РёРјСѓС‰РµСЃС‚РІР° Р»РёРєРІРёРґРёСЂСѓРµРјРѕР№ РЎС‚РѕСЂРѕРЅС‹ РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚
topics: ['РџСЂРё СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР° РїРµСЂРµС…РѕРґСЏС‚ Рє РїСЂР°РІРѕРїСЂРµРµРјРЅРёРєСѓ', 'Р’ СЃР»СѓС‡Р°Рµ Р»РёРєРІРёРґР°С†РёРё РѕРґРЅРѕР№ РёР· СЃС‚РѕСЂРѕРЅ - СѓРґРѕРІР»РµС‚РІРѕСЂРµРЅРёРµ РёРјСѓС‰РµСЃС‚РІРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёР№ Р·Р° СЃС‡РµС‚ РёРјСѓС‰РµСЃС‚РІР° Р»РёРєРІРёРґРёСЂСѓРµРјРѕР№ СЃС‚РѕСЂРѕРЅС‹']

=== 11.11 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р•СЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ СѓРєР°Р·Р°РЅ СЃР°Р№С‚ - СЌС‚Рѕ РЅРµ СЏРІР»СЏРµС‚СЃСЏ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Р�РЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, РєР°СЃР°СЋС‰РёРµСЃСЏ РїСЂРµРґРјРµС‚Р° Р”РѕРіРѕРІРѕСЂР°, РІРєР»СЋС‡Р°СЏ РґРѕРєСѓРјРµРЅС‚С‹, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р”РѕРіРѕРІРѕСЂРµ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рµ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°, СЃС‚Р°РЅРѕРІСЏС‚СЃСЏ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹РјРё Рє РёСЃРїРѕР»РЅРµРЅРёСЋ СЃРѕ СЃР»РµРґСѓСЋС‰РµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ Р·Р° РґРЅРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РёС… РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅ
topics: ['РЎСЂРѕРє, СЃ РєРѕС‚РѕСЂРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЃС‚Р°РЅРѕРІСЏС‚СЃСЏ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹РјРё Рє РІС‹РїРѕР»РµРЅРµРЅРёСЋ РїРѕСЃР»Рµ СЂР°Р·РјРµС‰РµРЅРёСЏ РЅР° РѕС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ']

=== 11.12 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ СЃР°РјРѕ РЅР°Р»РёС‡РёРµ С‚Р°РєРѕР№ РёР»Рё РїРѕС…РѕР¶РµР№ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Р’СЃРµ СѓРІРµРґРѕРјР»РµРЅРёСЏ Рё Р·Р°РїСЂРѕСЃС‹ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°РµРІ, РєРѕРіРґР° Р”РѕРіРѕРІРѕСЂРѕРј РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅ РёРЅРѕР№ РїРѕСЂСЏРґРѕРє РёС… РЅР°РїСЂР°РІР»РµРЅРёСЏ, СЃС‡РёС‚Р°СЋС‚СЃСЏ РЅР°РїСЂР°РІР»РµРЅРЅС‹РјРё РЅР°РґР»РµР¶Р°С‰РёРј РѕР±СЂР°Р·РѕРј РґСЂСѓРіРѕР№ РЎС‚РѕСЂРѕРЅРµ, РµСЃР»Рё РѕРЅРё РЅР°РїСЂР°РІР»РµРЅС‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї. 2.3 Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚СЊ РѕС‚РїСЂР°РІРєРё СѓРІРµРґРѕРјР»РµРЅРёР№ Рё Р·Р°РїСЂРѕСЃРѕРІ, РµСЃР»Рё РѕС‚РїСЂР°РІР»РµРЅС‹ СЃРїРѕСЃРѕР±Р°РјРё РѕРїРёСЃР°РЅРЅС‹РјРё РІ РґРѕРіРѕРІРѕСЂРµ']

=== 11.13 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 11 В«РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ в†’ Рљ РЅР°СЃС‚РѕСЏС‰РµРјСѓ Р”РѕРіРѕРІРѕСЂСѓ РїСЂРёР»Р°РіР°СЋС‚СЃСЏ:
1) РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1 вЂ“ Р—Р°СЏРІР»РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі.
2) РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 вЂ“ Р�РЅС„РѕСЂРјР°С†РёСЏ Рѕ РўРѕСЂРіРѕРІРѕ-РЎРµСЂРІРёСЃРЅРѕР№ РўРѕС‡РєРµ/Р РµСЃСѓСЂСЃРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ.
3) РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 вЂ“ РђРєС‚ Рѕ РїРµСЂРµС‡РёСЃР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРј Рѕ
topics: ['РџРµСЂРµС‡РµРЅСЊ РґРѕРєСѓРјРµРЅС‚РѕРІ, РїСЂРёР»РѕР¶РµРЅРЅС‹С… Рє РґРѕРіРѕРІРѕСЂСѓ']

[Command succeeded with exit code 0]
AI: The output is garbled due to encoding issues in the shell. Let me read the matrix.json directly for sections 7-11 using the file I already dumped.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch4_matrix.json', 'limit': 200}, 'id': 'call_00_ypRDCn1YgFEsKtOTJokI7591', 'type': 'tool_call'}]
Tool:      1	[
     2	  {
     3	    "number": "7.1",
     4	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с условиями Договора и законодательством РФ.",
     5	    "required_type": "mandatory",
     6	    "main_idea": "",
     7	    "only_for_product": "common",
     8	    "only_for_lot": "common",
     9	    "only_for_terminal": "common",
    10	    "topics": [
    11	      "Общие слова о том, что за неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с условиями Договора",
    12	      "Общие слова о том, что за неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с законодательством РФ"
    13	    ],
    14	    "payment_method": "common"
    15	  },
    16	  {
    17	    "number": "7.2",
    18	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За каждый факт неисполнения Предприятием обязательств, предусмотренных Договором, за исключением просрочки исполнения обязательств, предусмотренных Договором, размер штрафа устанавливается в следующем порядке:\nа) 1000 рублей, если Цена Договора не превышает 3 млн. рублей (включительно);\nб) 5000 рублей, если Цена Договора составляет от 3 млн. рублей до 50 млн. рублей (включительно);\nв) 10000 рублей, если Цена Договора составляет от 50 млн. рублей до 100 млн. рублей (включительно);\nг) 100000 рублей, если Цена Договора превышает 100 млн. рублей.",
    19	    "required_type": "mandatory",
    20	    "main_idea": "Важно, что штраф именно Предприятию, важен размер штрафа",
    21	    "only_for_product": "common",
    22	    "only_for_lot": "common",
    23	    "only_for_terminal": "common",
    24	    "topics": [
    25	      "Штраф Предприятию за неисполнение или ненадлежащее исполнение обязательств, за исключением просрочки."
    26	    ],
    27	    "payment_method": "common"
    28	  },
    29	  {
    30	    "number": "7.3",
    31	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Общая сумма начисленных штрафов за ненадлежащее исполнение Предприятием обязательств, предусмотренных Договором, не может превышать цену Договора.",
    32	    "required_type": "mandatory",
    33	    "main_idea": "",
    34	    "only_for_product": "common",
    35	    "only_for_lot": "common",
    36	    "only_for_terminal": "common",
    37	    "topics": [
    38	      "Общая сумма штрафов за ненадлежащее исполнение Предприятием обязательств не превышает цену договора"
    39	    ],
    40	    "payment_method": "common"
    41	  },
    42	  {
    43	    "number": "7.4",
    44	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → В случае просрочки исполнения Банком обязательств, предусмотренных Договором, а также в иных случаях неисполнения или ненадлежащего исполнения Банком обязательств, предусмотренных Договором, Предприятие направляет Банку требование об уплате неустоек (штрафов, пеней).Пеня начисляется за каждый день просрочки исполнения Банком обязательства, предусмотренного Договором, начиная со дня, следующего после дня истечения установленного Договором срока исполнения обязательства, и устанавливается Договором в размере одной трехсотой действующей на дату уплаты пени ключевой ставки Центрального банка РФ от Цены Договора, уменьшенной на сумму, пропорциональную объему обязательств, предусмотренных Договором и фактически исполненных Банком, за исключением случаев, если законодательством РФ установлен иной порядок начисления пени.   ",
    45	    "required_type": "mandatory",
    46	    "main_idea": "",
    47	    "only_for_product": "common",
    48	    "only_for_lot": "common",
    49	    "only_for_terminal": "common",
    50	    "topics": [
    51	      "В случае просрочки исполнения Банком обязательств, Предприятие направляет Банку требование об уплате неустоек (штрафов, пеней)",
    52	      "Штраф Банку. Начисление пени за каждый день просрочки",
    53	      "Штраф Банку.Определения срока начала начисления пени",
    54	      "Штраф Банку. Определение размера пени"
    55	    ],
    56	    "payment_method": "common"
    57	  },
    58	  {
    59	    "number": "7.5",
    60	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За каждый факт неисполнения или ненадлежащего исполнения Банком обязательств, предусмотренных Договором, за исключением просрочки исполнения обязательств, предусмотренных Договором, размер штрафа устанавливается в следующем порядке:\nа) 10 процентов Цены Договора в случае, если Цена Договора не превышает 3 млн. рублей;\nб) 5 процентов Цены Договора в случае, если Цена Договора составляет от 3 млн. рублей до 50 млн. рублей (включительно);\nв) 1 процент Цены Договора в случае, если Цена Договора составляет от 50 млн. рублей до 100 млн. рублей (включительно);\nг) 0,5 процента Цены Договора в случае, если Цена Договора составляет от 100 млн. рублей до 500 млн. рублей (включительно);\nд) 0,4 процента Цены Договора в случае, если Цена Договора составляет от 500 млн. рублей до 1 млрд. рублей (включительно);\nе) 0,3 процента Цены Договора в случае, если Цена Договора составляет от 1 млрд. рублей до 2 млрд. рублей (включительно);\nж) 0,25 процента Цены Договора в случае, если Цена Договора составляет от 2 млрд. рублей до 5 млрд. рублей (включительно);\nз) 0,2 процента Цены Договора в случае, если Цена Договора составляет от 5 млрд. рублей до 10 млрд. рублей (включительно);\nи) 0,1 процента Цены Договора в случае, если Цена Договора превышает 10 млрд. рублей.",
    61	    "required_type": "mandatory",
    62	    "main_idea": "",
    63	    "only_for_product": "common",
    64	    "only_for_lot": "common",
    65	    "only_for_terminal": "common",
    66	    "topics": [
    67	      "Размер штрафа за неисполнение или ненадлежащее исполнение обязательств Банком, за исключением просрочки, имеющих стоимостное выражения в процентах от суммы договора"
    68	    ],
    69	    "payment_method": "common"
    70	  },
    71	  {
    72	    "number": "7.6",
    73	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За каждый факт неисполнения или ненадлежащего исполнения Банком обязательств, предусмотренных Договором, которое не имеет стоимостного выражения, размер штрафа устанавливается в следующем порядке:\nа) 1000 рублей, если Цена Договора не превышает 3 млн. рублей;\nб) 5000 рублей, если Цена Договора составляет от 3 млн. рублей до 50 млн. рублей (включительно);\nв) 10000 рублей, если Цена Договора составляет от 50 млн. рублей до 100 млн. рублей (включительно);\nг) 100000 рублей, если Цена Договора превышает 100 млн. рублей.",
    74	    "required_type": "mandatory",
    75	    "main_idea": "",
    76	    "only_for_product": "common",
    77	    "only_for_lot": "common",
    78	    "only_for_terminal": "common",
    79	    "topics": [
    80	      "Размер штрафа за неисполнение или ненадлежащее исполнение обязательств Банком, не имеющего стоимостного выражения"
    81	    ],
    82	    "payment_method": "common"
    83	  },
    84	  {
    85	    "number": "7.7",
    86	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Банком обязательств, предусмотренных Договором, не может превышать Цену Договора",
    87	    "required_type": "mandatory",
    88	    "main_idea": "",
    89	    "only_for_product": "common",
    90	    "only_for_lot": "common",
    91	    "only_for_terminal": "common",
    92	    "topics": [
    93	      "Общая сумма штрафов за нарушения Банка не превышает цену договора"
    94	    ],
    95	    "payment_method": "common"
    96	  },
    97	  {
    98	    "number": "7.8",
    99	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности по спорам и разногласиям, возникающим между Предприятием и Покупателем во всех случаях, когда такие споры и разногласия не относятся к предмету Договора, а также по спорам в отношении Товаров/услуг, оплаченных с использованием Карты / ее реквизитов / NFС-карты / SberPay / Плати QR / Платежного счета.",
   100	    "required_type": "optional",
   101	    "main_idea": "Важен факт, что Банк (Исполнитель) не несет ответственности по спорам и разногласиям Предприятия(Заказчика) и Покупателя (клиент Предприятия)",
   102	    "only_for_product": "common",
   103	    "only_for_lot": "common",
   104	    "only_for_terminal": "common",
   105	    "topics": [
   106	      "Ответственность Банка (Исполнителя) за споры между Предприятием (Заказчиком) и Покупателем (Клиент Заказчика)"
   107	    ],
   108	    "payment_method": "common"
   109	  },
   110	  {
   111	    "number": "7.9",
   112	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности за задержки перевода денежных средств на счет Предприятия, если задержки произошли не по вине Банка.",
   113	    "required_type": "optional",
   114	    "main_idea": "",
   115	    "only_for_product": "common",
   116	    "only_for_lot": "common",
   117	    "only_for_terminal": "common",
   118	    "topics": [
   119	      "Банк освобожден от ответственности при задержках переводов без своей вины"
   120	    ],
   121	    "payment_method": "common"
   122	  },
   123	  {
   124	    "number": "7.10",
   125	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности за неисполнение условий Договора, обусловленное действиями или бездействиями третьих лиц, в том числе участниками Платежной системы",
   126	    "required_type": "optional",
   127	    "main_idea": "",
   128	    "only_for_product": "common",
   129	    "only_for_lot": "common",
   130	    "only_for_terminal": "common",
   131	    "topics": [
   132	      "Банк не несёт ответственность за неисполнение условий Договора в связи с действием и бездействием третьих лиц"
   133	    ],
   134	    "payment_method": "common"
   135	  },
   136	  {
   137	    "number": "7.11",
   138	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности за несвоевременное перечисление сумм Операций по причине проведения расследования Банком при подозрении на проведение Операции с нарушением условий Договора",
   139	    "required_type": "optional",
   140	    "main_idea": "",
   141	    "only_for_product": "common",
   142	    "only_for_lot": "common",
   143	    "only_for_terminal": "common",
   144	    "topics": [
   145	      "Банк освобождается от ответственности за задержку перечисления средств в случае инициирования им расследования операций"
   146	    ],
   147	    "payment_method": "common"
   148	  },
   149	  {
   150	    "number": "7.12",
   151	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности в случае превышения установленной Цены Договора",
   152	    "required_type": "optional",
   153	    "main_idea": "",
   154	    "only_for_product": "common",
   155	    "only_for_lot": "common",
   156	    "only_for_terminal": "common",
   157	    "topics": [
   158	      "Общие слова о том, что банк освобожден от ответственности при превышении Цены Договора"
   159	    ],
   160	    "payment_method": "common"
   161	  },
   162	  {
   163	    "number": "7.13",
   164	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие несет ответственность за некорректность проведенных Операций, совершенных на Ресурсе, в случае невыполнения п. 4.2.21.1 Договора",
   165	    "required_type": "mandatory",
   166	    "main_idea": "",
   167	    "only_for_product": "internet_acquiring",
   168	    "only_for_lot": "common",
   169	    "only_for_terminal": "common",
   170	    "topics": [
   171	      "Предприятие несет ответственность за некорректные операции на Ресурсе"
   172	    ],
   173	    "payment_method": "common"
   174	  },
   175	  {
   176	    "number": "7.14",
   177	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие несет ответственность за все действия, осуществляемые Предприятием/ТСТ в СПЭП",
   178	    "required_type": "mandatory",
   179	    "main_idea": "",
   180	    "only_for_product": "common",
   181	    "only_for_lot": "common",
   182	    "only_for_terminal": "common",
   183	    "topics": [
   184	      "Общее утверждение о том, что Предприятие несет ответственность за все действия в СПЭП"
   185	    ],
   186	    "payment_method": "common"
   187	  },
   188	  {
   189	    "number": "7.15",
   190	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие полностью несет ответственность за действия своего персонала, связанные с нарушением условий Договора и инструктивных материалов, предоставленных Банком",
   191	    "required_type": "mandatory",
   192	    "main_idea": "Важен сам факт несения ответственности, если в договоре не говорится про несение ответственности за действия персонала, значит этот пункт не относится к данному",
   193	    "only_for_product": "common",
   194	    "only_for_lot": "common",
   195	    "only_for_terminal": "common",
   196	    "topics": [
   197	      "Предприятие несет полную ответственность за нарушения персонала условий договора",
   198	      "Предприятие несет полную ответственность за нарушения персонала инструкций Банка"
   199	    ],
   200	    "payment_method": "common"
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch4_matrix.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_Mg3Am18fcsK6zIv6wG4u9410', 'type': 'tool_call'}]
Tool:    201	  },
   202	  {
   203	    "number": "7.16",
   204	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → При заключении, исполнении, изменении и расторжении Договора Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция» , а также иных действий (бездействия), нарушающих требования применимого законодательства, применимых норм международного права в области противодействия коррупции",
   205	    "required_type": "mandatory",
   206	    "main_idea": "",
   207	    "only_for_product": "common",
   208	    "only_for_lot": "common",
   209	    "only_for_terminal": "common",
   210	    "topics": [
   211	      "Обязательство не совершать коррупционных и иных противозаконных действий при любых операциях по договору"
   212	    ],
   213	    "payment_method": "common"
   214	  },
   215	  {
   216	    "number": "7.17",
   217	    "enriched_text": "РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие несет полную финансовую ответственность перед Банком в случае несоответствия проведенных Повторяющихся платежей требованиям законодательства Российской Федерации, в том числе нормативных актов Банка России, правил Платежной системы и (или) Договора",
   218	    "required_type": "mandatory",
   219	    "main_idea": "Важно, чтобы  в договоре не было сужения ответственности.",
   220	    "only_for_product": "common",
   221	    "only_for_lot": "common",
   222	    "only_for_terminal": "common",
   223	    "topics": [
   224	      "Общие слова про то, что Предприятие несет финансовую ответственность за несоответствие Повторяющихся платежей законодательству РФ",
   225	      "Общие слова про то, что Предприятие отвечает за соответствие Повторяющихся платежей нормативным актам Банка России",
   226	      "Общие слова про то, что Предприятие обязано соблюдать правила Платежной системы в части Повторяющихся платежей",
   227	      "Общие слова про то, что Предприятие несет ответственность за нарушение условий Договора относительно Повторяющихся платежей"
   228	    ],
   229	    "payment_method": "common"
   230	  },
   231	  {
   232	    "number": "8.1",
   233	    "enriched_text": "РАЗДЕЛ 8 «ФОРС-МАЖОРНЫЕ ОБСТОЯТЕЛЬСТВА» → Сторона Договора освобождается от ответственности за частичное или полное неисполнение обязательств по Договору, если это неисполнение явилось следствием обстоятельств непреодолимой силы, возникших в результате обстоятельств чрезвычайного характера, которые сторона не могла ни предвидеть, ни предотвратить разумными мерами. К таким обстоятельствам чрезвычайного характера относятся стихийные бедствия, аварии, пожары, массовые беспорядки, забастовки, революции, военные действия, а также любые другие обстоятельства вне разумного контроля сторон.При возникновении указанных обстоятельств, срок исполнения договорных обязательств соразмерно откладывается на время действия соответствующего обстоятельства.",
   234	    "required_type": "mandatory",
   235	    "main_idea": "",
   236	    "only_for_product": "common",
   237	    "only_for_lot": "common",
   238	    "only_for_terminal": "common",
   239	    "topics": [
   240	      "описание форс-мажорных обстоятельств как основание для освобождения от ответственности",
   241	      "перечень конкретных форс-мажорных событий (стихийные бедствия, пожары и т.д.)",
   242	      "продление срока исполнения договорных обязательств соразмерно времени действия соответствующего обстоятельства"
   243	    ],
   244	    "payment_method": "common"
   245	  },
   246	  {
   247	    "number": "8.2",
   248	    "enriched_text": "РАЗДЕЛ 8 «ФОРС-МАЖОРНЫЕ ОБСТОЯТЕЛЬСТВА» → При наступлении обстоятельств, указанных в п. 8.1 Договора, Сторона, для которой создалась невозможность исполнения ее обязательств по Договору, должна в течение 24 (двадцати четырех) часов известить о них другую Сторону в соответствии с п.2.3 Договора, с обязательным указанием данных о характере обстоятельств, оценку их влияния на возможность исполнения стороной своих обязательств по Договору и предполагаемый срок их исполнения (при наличии такой возможности). При невозможности исполнения обязательств в срок свыше 3-х (трех) месяцев каждая из Сторон имеет право расторгнуть Договор.",
   249	    "required_type": "mandatory",
   250	    "main_idea": "",
   251	    "only_for_product": "common",
   252	    "only_for_lot": "common",
   253	    "only_for_terminal": "common",
   254	    "topics": [
   255	      "Обязанность уведомления другой стороны при обстоятельствах непреодолимой силы",
   256	      "Срок уведомления другой стороны при обстоятельствах непреодолимой силы",
   257	      "указание характера форс-мажорных обстоятельств",
   258	      "оценка влияния на исполнение обязательств",
   259	      "предполагаемый срок исполнения при наличии информации",
   260	      "право на расторжение договора при задержке более 3 месяцев"
   261	    ],
   262	    "payment_method": "common"
   263	  },
   264	  {
   265	    "number": "9.1",
   266	    "enriched_text": "РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Урегулирование споров Сторон совершается в претензионном порядке",
   267	    "required_type": "mandatory",
   268	    "main_idea": "",
   269	    "only_for_product": "common",
   270	    "only_for_lot": "common",
   271	    "only_for_terminal": "common",
   272	    "topics": [
   273	      "соблюден претензионный порядок урегулирования споров",
   274	      "указан обязательный досудебный порядок с указанием срока рассмотрения претензий"
   275	    ],
   276	    "payment_method": "common"
   277	  },
   278	  {
   279	    "number": "9.2",
   280	    "enriched_text": "РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Претензии рассматриваются Сторонами в течение 10 (десяти) календарных дней с даты их получения одной из Сторон.",
   281	    "required_type": "mandatory",
   282	    "main_idea": "Важен срок рассмотрения претензий",
   283	    "only_for_product": "common",
   284	    "only_for_lot": "common",
   285	    "only_for_terminal": "common",
   286	    "topics": [
   287	      "Срок рассмотрения претензий"
   288	    ],
   289	    "payment_method": "common"
   290	  },
   291	  {
   292	    "number": "9.3",
   293	    "enriched_text": "РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Споры, не урегулированные в претензионном порядке, подлежат разрешению в соответствии с действующим законодательством РФ.",
   294	    "required_type": "mandatory",
   295	    "main_idea": "",
   296	    "only_for_product": "common",
   297	    "only_for_lot": "common",
   298	    "only_for_terminal": "common",
   299	    "topics": [],
   300	    "payment_method": "common"
   301	  },
   302	  {
   303	    "number": "10.1",
   304	    "enriched_text": "РАЗДЕЛ 10 «СРОК ДЕЙСТВИЯ ДОГОВОРА И ПОРЯДОК ЕГО РАСТОРЖЕНИЯ → Настоящий Договор вступает в силу с даты его подписания обеими Сторонами и действует по ___________ (включительно) или до исчерпания Цены договора (в зависимости от того, какое событие наступит первым). Окончание срока действия Договора не освобождает Стороны от ответственности за неисполнение обязательств по Договору.",
   305	    "required_type": "mandatory",
   306	    "main_idea": "",
   307	    "only_for_product": "common",
   308	    "only_for_lot": "common",
   309	    "only_for_terminal": "common",
   310	    "topics": [
   311	      "указана дата окончания действия договора",
   312	      "определен порядок учета цены договора при определении срока действия",
   313	      "установлено сохранение ответственности сторон после окончания срока договора"
   314	    ],
   315	    "payment_method": "common"
   316	  },
   317	  {
   318	    "number": "10.2",
   319	    "enriched_text": "РАЗДЕЛ 10 «СРОК ДЕЙСТВИЯ ДОГОВОРА И ПОРЯДОК ЕГО РАСТОРЖЕНИЯ → Любая Сторона по Договору вправе его досрочно расторгнуть в одностороннем внесудебном порядке, письменно уведомив об этом другую Сторону не менее чем за 30 (тридцать) календарных дней до даты расторжения, за исключением случаев, предусмотренных п. 5.1.8 настоящего Договора",
   320	    "required_type": "mandatory",
   321	    "main_idea": "Важно описание возможности расторгнуть договор в одностороннем порядке. Важен срок уведомления о расторжении.",
   322	    "only_for_product": "common",
   323	    "only_for_lot": "common",
   324	    "only_for_terminal": "common",
   325	    "topics": [
   326	      "Право любой стороны расторгнуть договор в одностороннем порядке",
   327	      "Обязанность уведомления другой стороны о расторжении в одностороннем порядке",
   328	      "Право Банка расторгнуть договор в одностороннем порядке",
   329	      "Право Предприятия расторгнуть договор в одностороннем порядке"
   330	    ],
   331	    "payment_method": "common"
   332	  },
   333	  {
   334	    "number": "10.3",
   335	    "enriched_text": "РАЗДЕЛ 10 «СРОК ДЕЙСТВИЯ ДОГОВОРА И ПОРЯДОК ЕГО РАСТОРЖЕНИЯ → При расторжении настоящего Договора Банком в одностороннем внесудебном порядке в случаях, предусмотренных п. 5.1.8. настоящего Договора, Договор считается расторгнутым с даты, указанной в письменном уведомлении Банка о расторжении. Стороны осуществляют расчеты/взаиморасчеты в течение 18 (восемнадцать) месяцев с даты расторжения Договора. Предприятие выплачивает Банку суммы Операций в порядке, установленном п.п. 5.1.3, 5.1.4 и разделом 6 настоящего Договора",
   336	    "required_type": "mandatory",
   337	    "main_idea": "",
   338	    "only_for_product": "common",
   339	    "only_for_lot": "common",
   340	    "only_for_terminal": "common",
   341	    "topics": [
   342	      "Сроки, в которые договор считается расторгнутым в случае расторжения в одностороннем внесудебном порядке",
   343	      "Сроки расчетов после одностороннего внесудебного порядка расторжения - 18 месяцев",
   344	      "Порядок выплаты сумм операций определен в пунктах 5.1.3, 5.1.4 и разделе 6"
   345	    ],
   346	    "payment_method": "common"
   347	  },
   348	  {
   349	    "number": "11.1",
   350	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Стороны соглашаются, что источниками правового регулирования отношений Сторон в рамках Договора являются настоящие Договор, действующее законодательство РФ, правила, стандарты и рекомендации Платежной системы при условии их не противоречия действующему законодательству РФ.Любые условия и положения Договора, которые противоречат положениям правил Платежной системы (как известных в момент заключения Договора, так и введенных в действие в будущем), должны быть приведены в соответствие с правилами Платежной системы, если это не противоречит законодательству РФ.\n",
   351	    "required_type": "optional",
   352	    "main_idea": "",
   353	    "only_for_product": "common",
   354	    "only_for_lot": "common",
   355	    "only_for_terminal": "common",
   356	    "topics": [
   357	      "Перечисление источников правового регулирования отношений Сторон",
   358	      "Требование соблюдать законодательство РФ",
   359	      "Условия и положения Договора, противоречащие правила Платежной системы должны быть приведены в соответствие"
   360	    ],
   361	    "payment_method": "common"
   362	  },
   363	  {
   364	    "number": "11.2",
   365	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Информация, полученная Предприятием в рамках исполнения Договора (номера Карт/Платежных счетов, персональные данные Покупателей, суммы Операций, информация о платеже), является конфиденциальной и не подлежит передаче третьим лицам, за исключением случаев, предусмотренных действующим законодательством РФ или условиями Договором.",
   366	    "required_type": "optional",
   367	    "main_idea": "",
   368	    "only_for_product": "common",
   369	    "only_for_lot": "common",
   370	    "only_for_terminal": "common",
   371	    "topics": [
   372	      "Номера Карт/Платежных счетов, персональные данные Покупателей, суммы Операций, информация о платеже являются конфиденциальной информацией",
   373	      "Объявляется запрет на передачу конфиденциальной информации третьим лицам",
   374	      "Даётся разрешение на передачу конфиденциальной информации разрешена, только если это требование законодательства или условие договора"
   375	    ],
   376	    "payment_method": "common"
   377	  },
   378	  {
   379	    "number": "11.3",
   380	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Стороны обязуются не разглашать полученные в ходе исполнения Договора сведения, включая:\n• описание защитных элементов Карт;\n• технологию проведения Операций;\n• информацию об управлении, финансовой и иной деятельности Сторон;\n• иную информацию, разглашение которой может привести к возникновению убытков или негативно повлиять на деловую репутацию Сторон.\nПредоставление указанной информации допускается только при согласии обеих Сторон.\nДанное положение не отменяет п. 5.1.7 Договора",
   381	    "required_type": "optional",
   382	    "main_idea": "",
   383	    "only_for_product": "common",
   384	    "only_for_lot": "common",
   385	    "only_for_terminal": "common",
   386	    "topics": [
   387	      "Стороны обязуются не разглашать иным лицам полученные сведения о защитных элементов карт",
   388	      "Стороны обязуются не разглашать иным лицам полученные сведения о технологии проведения операций",
   389	      "Стороны обязуются не разглашать иным лицам полученные сведения о финансовом состоянии сторон",
   390	      "Стороны обязуются не разглашать иным лицам конфиденциальную информацию без согласия другой стороны"
   391	    ],
   392	    "payment_method": "common"
   393	  },
   394	  {
   395	    "number": "11.4",
   396	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все изменения и дополнения к настоящему Договору, кроме документов, ссылки на которые даются в настоящем Договоре, размещенные на Официальном сайте Банка, действительны лишь в том случае, если они совершены в письменной форме, и подписаны уполномоченными представителями Сторон",
   397	    "required_type": "optional",
   398	    "main_idea": "",
   399	    "only_for_product": "common",
   400	    "only_for_lot": "common",
   401	    "only_for_terminal": "common",
   402	    "topics": [
   403	      "изменения и дополнения должны быть в письменной форме",
   404	      "подписаны уполномоченными представителями обеих сторон"
   405	    ],
   406	    "payment_method": "common"
   407	  },
   408	  {
   409	    "number": "11.5",
   410	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все имевшие место до подписания настоящего Договора соглашения, переговоры и переписка между Сторонами по вопросам, изложенным в настоящем Договоре, утрачивают силу с даты подписания настоящего Договора.",
   411	    "required_type": "optional",
   412	    "main_idea": "",
   413	    "only_for_product": "common",
   414	    "only_for_lot": "common",
   415	    "only_for_terminal": "common",
   416	    "topics": [],
   417	    "payment_method": "common"
   418	  },
   419	  {
   420	    "number": "11.6",
   421	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Настоящий Договор составлен в ________ экземплярах, _________ экземпляр(-а) для Банка, один экземпляр для Предприятия",
   422	    "required_type": "optional",
   423	    "main_idea": "",
   424	    "only_for_product": "common",
   425	    "only_for_lot": "common",
   426	    "only_for_terminal": "common",
   427	    "topics": [
   428	      "Договор составлен в определенном количестве экземпляров",
   429	      "указано количество экземпляров Договора для Банка",
   430	      "указано количество экземпляров Договора для Предприятия"
   431	    ],
   432	    "payment_method": "common"
   433	  },
   434	  {
   435	    "number": "11.7",
   436	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все Приложения к настоящему Договору являются его неотъемлемой частью",
   437	    "required_type": "optional",
   438	    "main_idea": "",
   439	    "only_for_product": "common",
   440	    "only_for_lot": "common",
   441	    "only_for_terminal": "common",
   442	    "topics": [
   443	      "Общие слова про то, что приложения являются неотъемлемой частью договора"
   444	    ],
   445	    "payment_method": "common"
   446	  },
   447	  {
   448	    "number": "11.8",
   449	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Предприятие заверяет, что реализация Товаров/услуг в ТСТ осуществляется в соответствии с требованиями действующего законодательства РФ",
   450	    "required_type": "optional",
   451	    "main_idea": "",
   452	    "only_for_product": "common",
   453	    "only_for_lot": "common",
   454	    "only_for_terminal": "common",
   455	    "topics": [
   456	      "Предприятие (Заказчик) заверяет, что реализация Товаров/услуг осуществляется в соответствии с требованиями законодательства РФ"
   457	    ],
   458	    "payment_method": "common"
   459	  },
   460	  {
   461	    "number": "11.9",
   462	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Ни одна из Сторон не вправе передавать свои обязанности и/или права по Договору третьим лицам без письменного согласования с другой Стороной, за исключением случая реорганизации одной из Сторон",
   463	    "required_type": "optional",
   464	    "main_idea": "",
   465	    "only_for_product": "common",
   466	    "only_for_lot": "common",
   467	    "only_for_terminal": "common",
   468	    "topics": [
   469	      "запрет передачи обязательств и прав без письменного согласия другой стороны",
   470	      "возможность передачи обязательств для случаев реорганизации стороны"
   471	    ],
   472	    "payment_method": "common"
   473	  },
   474	  {
   475	    "number": "11.10",
   476	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ →  В случае реорганизации одной из Сторон обязательства по Договору в полном объеме переходят к правопреемнику. В случае ликвидации одной из Сторон имущественные требования другой Стороны удовлетворяются за счет имущества ликвидируемой Стороны в установленном законодательством РФ порядке",
   477	    "required_type": "optional",
   478	    "main_idea": "",
   479	    "only_for_product": "common",
   480	    "only_for_lot": "common",
   481	    "only_for_terminal": "common",
   482	    "topics": [
   483	      "При реорганизации одной из Сторон обязательства переходят к правопреемнику",
   484	      "В случае ликвидации одной из сторон - удовлетворение имущественных требований за счет имущества ликвидируемой стороны"
   485	    ],
   486	    "payment_method": "common"
   487	  },
   488	  {
   489	    "number": "11.11",
   490	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Инструктивные материалы, касающиеся предмета Договора, включая документы, ссылки на которые даются в настоящем Договоре, размещенные на Официальном сайте Банка, становятся обязательными к исполнению со следующего рабочего дня за днем размещения их на Официальном сайте Банка: https://www.sberbank.ru, если не указаны иные сроки ввода их в действие",
   491	    "required_type": "optional",
   492	    "main_idea": "Если в договоре не указан сайт - это не является разногласием",
   493	    "only_for_product": "common",
   494	    "only_for_lot": "common",
   495	    "only_for_terminal": "common",
   496	    "topics": [
   497	      "Срок, с которого инструктивные материалы становятся обязательными к выполенению после размещения на официальном сайте"
   498	    ],
   499	    "payment_method": "common"
   500	  },
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch4_matrix.json', 'offset': 500, 'limit': 100}, 'id': 'call_00_ZOadnsnwfAWTt19NakxT3795', 'type': 'tool_call'}]
Tool:    501	  {
   502	    "number": "11.12",
   503	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все уведомления и запросы по Договору, за исключением случаев, когда Договором предусмотрен иной порядок их направления, считаются направленными надлежащим образом другой Стороне, если они направлены в соответствии с п. 2.3 Договора",
   504	    "required_type": "optional",
   505	    "main_idea": "Важно само наличие такой или похожей формулировки",
   506	    "only_for_product": "common",
   507	    "only_for_lot": "common",
   508	    "only_for_terminal": "common",
   509	    "topics": [
   510	      "Общие слова про правомерность отправки уведомлений и запросов, если отправлены способами описанными в договоре"
   511	    ],
   512	    "payment_method": "common"
   513	  },
   514	  {
   515	    "number": "11.13",
   516	    "enriched_text": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → К настоящему Договору прилагаются:\n1) Приложение № 1 – Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг.\n2) Приложение № 1.1 – Информация о Торгово-Сервисной Точке/Ресурсе Предприятия.\n3) Приложение № 2 – Акт о перечислении Предприятию сумм операций по картам.\nПриложение № 3 – Описание услуг, формирующих тарифы и параметры сервиса для Смарт-терминалов",
   517	    "required_type": "optional",
   518	    "main_idea": "",
   519	    "only_for_product": "common",
   520	    "only_for_lot": "common",
   521	    "only_for_terminal": "common",
   522	    "topics": [
   523	      "Перечень документов, приложенных к договору"
   524	    ],
   525	    "payment_method": "common"
   526	  }
   527	]
AI: Now let me read the contract sections 7-11 and the matrix_legal_propositions for these sections. Let me also read the existing working artifacts to understand what's already been done.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 170, 'limit': 200}, 'id': 'call_00_dz8YQ5EpPIamfoLpPiP59805', 'type': 'tool_call'}]
Tool:    171	7. ОТВЕТСТВЕННОСТЬ СТОРОН
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
   201	1 процент начальной (максимальной) цены контракта, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
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
AI: Now I have a comprehensive picture. Let me also read the matrix_legal_propositions for sections 7-11 and the existing coverage_ledger to understand what's already been done.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 50}, 'id': 'call_00_6PLXdeUlMjem8OtKczWK2858', 'type': 'tool_call'}]
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_ref": {
     6	        "matrix_id": "2.1"
     7	      },
     8	      "materiality": "evaluable",
     9	      "required_type": "mandatory",
    10	      "applicability_filters": {
    11	        "only_for_product": "common",
    12	        "only_for_lot": "common",
    13	        "only_for_terminal": "common",
    14	        "payment_method": "common"
    15	      },
    16	      "bank_standard": "для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать...",
    17	      "protected_party": "Bank",
    18	      "bound_party": "counterparty",
    19	      "right_or_obligation": "обязанность: Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    20	      "legal_object": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    21	      "matching_cues": [
    22	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    23	        "Банк может отказать в регистрации ТСТ без указания причины",
    24	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    25	        "Информация о новых устройствах предоставляется с указанием их количества"
    26	      ],
    27	      "legal_atoms": [
    28	        {
    29	          "atom_id": "a1",
    30	          "category": "obligation",
    31	          "text": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом"
    32	        },
    33	        {
    34	          "atom_id": "a2",
    35	          "category": "right",
    36	          "text": "Банк может отказать в регистрации ТСТ без указания причины"
    37	        },
    38	        {
    39	          "atom_id": "a3",
    40	          "category": "obligation",
    41	          "text": "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении"
    42	        },
    43	        {
    44	          "atom_id": "a4",
    45	          "category": "obligation",
    46	          "text": "Информация о новых устройствах предоставляется с указанием их количества"
    47	        },
    48	        {
    49	          "atom_id": "a5",
    50	          "category": "obligation",
AI: Let me check if there's already a coverage_ledger or any batch outputs.[{'name': 'glob', 'args': {'pattern': '**/coverage_ledger*', 'path': '/outputs'}, 'id': 'call_00_0mEhSBg9X6xylrhGnaql7864', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/batch*', 'path': '/outputs'}, 'id': 'call_01_a53YG4O3GnfyTQcamoeg2430', 'type': 'tool_call'}]
Tool: []
Tool: ['/outputs/working/batch3_filter.py', '/outputs/working/batch3_list.py', '/outputs/working/batch3_matrix_legal.json', '/outputs/working/batch4_matrix.json']
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch3_matrix_legal.json', 'limit': 50}, 'id': 'call_00_u9NAubJKvzpzalaW6iYh8088', 'type': 'tool_call'}]
Tool:      1	[
     2	  {
     3	    "id": "5.1.1.1",
     4	    "source_ref": {
     5	      "matrix_id": "5.1.1.1"
     6	    },
     7	    "materiality": "evaluable",
     8	    "required_type": "mandatory",
     9	    "applicability_filters": {
    10	      "only_for_product": "common",
    11	      "only_for_lot": "common",
    12	      "only_for_terminal": "common",
    13	      "payment_method": "common"
    14	    },
    15	    "bank_standard": "Банк имеет право удерживать суммы операций, являющиеся недействительными",
    16	    "protected_party": "Bank",
    17	    "bound_party": "counterparty",
    18	    "right_or_obligation": "сумма/формула: Банк имеет право удерживать суммы операций, являющиеся недействительными",
    19	    "legal_object": "имеет право удерживать суммы операций, являющиеся недействительными",
    20	    "matching_cues": [
    21	      "Банк имеет право удерживать суммы операций, являющиеся недействительными"
    22	    ],
    23	    "legal_atoms": [
    24	      {
    25	        "atom_id": "a1",
    26	        "category": "amount",
    27	        "text": "Банк имеет право удерживать суммы операций, являющиеся недействительными"
    28	      },
    29	      {
    30	        "atom_id": "a2",
    31	        "category": "deadline",
    32	        "text": "6) по требованию Банка в течение 3 (трех) рабочих дней со дня получения запроса не предоставлены или предоставлены не в полном объеме (или не соответствующие правилам"
    33	      },
    34	      {
    35	        "atom_id": "a3",
    36	        "category": "amount",
    37	        "text": "Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: : Суммы Операций, являющихся недействительными, в следующих случаях: 1) Операция"
    38	      },
    39	      {
    40	        "atom_id": "a4",
    41	        "category": "amount",
    42	        "text": "3) Документ по операции заполнен не полностью, имеются исправления или отсутствует возможность определить сумму Операции, код Авторизации"
    43	      },
    44	      {
    45	        "atom_id": "a5",
    46	        "category": "amount",
    47	        "text": "10) сумма Товара/услуги была разбита на несколько Операций"
    48	      },
    49	      {
    50	        "atom_id": "a6",
AI: Now I have a good understanding of the data. Let me now do the substantive analysis. Let me update my todos and start the analysis.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'completed'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'completed'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract - apply applicability filters', 'status': 'in_progress'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]}, 'id': 'call_00_zBhZ6IvVmfQyn32oR1Gq6492', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read reference files: matching-rules.md, status-rules.md, comparison-patterns.md, output-contract.md', 'status': 'completed'}, {'content': 'Read inputs: matrix.json, matrix_legal_propositions.json, contract.txt', 'status': 'completed'}, {'content': 'Read existing working artifacts to understand current state', 'status': 'completed'}, {'content': 'Analyze matrix batch 4 (sections 7-11) against contract - apply applicability filters', 'status': 'in_progress'}, {'content': 'Build many-to-many legal links, classify uncovered/missing/out-of-scope', 'status': 'pending'}, {'content': 'Write working output files with links, atomic_links, unmatched_matrix, coverage-ledger rows', 'status': 'pending'}]
AI: Now let me do the systematic analysis. First, let me apply the product profile filters to determine which matrix rows are applicable.

**Product Profile (from contract_product_profile.json):**
- Product: trade_acquiring
- Lot: 44_fz
- Terminal: pos_terminal, smart_terminal
- Payment methods: cards, qr, nfc
- Legal regime: 44_fz

Now let me go through each matrix row in sections 7-11:

**Section 7 - Liability:**

- **7.1**: common/common/common/common → APPLICABLE. General liability clause.
- **7.2**: common/common/common/common → APPLICABLE. Counterparty fine for non-performance (non-delay).
- **7.3**: common/common/common/common → APPLICABLE. Cap on counterparty fines.
- **7.4**: common/common/common/common → APPLICABLE. Bank delay penalty.
- **7.5**: common/common/common/common → APPLICABLE. Bank non-delay fine (cost-based).
- **7.6**: common/common/common/common → APPLICABLE. Bank non-delay fine (non-cost).
- **7.7**: common/common/common/common → APPLICABLE. Cap on Bank fines.
- **7.8**: common/common/common/common → APPLICABLE. Bank not liable for customer-merchant disputes.
- **7.9**: common/common/common/common → APPLICABLE. Bank not liable for transfer delays not its fault.
- **7.10**: common/common/common/common → APPLICABLE. Bank not liable for third-party actions.
- **7.11**: common/common/common/common → APPLICABLE. Bank not liable for delayed transfers during investigation.
- **7.12**: common/common/common/common → APPLICABLE. Bank not liable if contract price exceeded.
- **7.13**: internet_acquiring → OUT_OF_SCOPE (product is trade_acquiring, not internet_acquiring).
- **7.14**: common/common/common/common → APPLICABLE. Counterparty liable for all actions in СПЭП.
- **7.15**: common/common/common/common → APPLICABLE. Counterparty liable for personnel actions.
- **7.16**: common/common/common/common → APPLICABLE. Anti-corruption clause.
- **7.17**: common/common/common/common → APPLICABLE. Counterparty financial liability for recurring payments.

**Section 8 - Force Majeure:**
- **8.1**: common/common/common/common → APPLICABLE.
- **8.2**: common/common/common/common → APPLICABLE.

**Section 9 - Dispute Resolution:**
- **9.1**: common/common/common/common → APPLICABLE.
- **9.2**: common/common/common/common → APPLICABLE.
- **9.3**: common/common/common/common → APPLICABLE.

**Section 10 - Term and Termination:**
- **10.1**: common/common/common/common → APPLICABLE.
- **10.2**: common/common/common/common → APPLICABLE.
- **10.3**: common/common/common/common → APPLICABLE.

**Section 11 - Miscellaneous:**
- **11.1**: common/common/common/common → APPLICABLE.
- **11.2**: common/common/common/common → APPLICABLE.
- **11.3**: common/common/common/common → APPLICABLE.
- **11.4**: common/common/common/common → APPLICABLE.
- **11.5**: common/common/common/common → APPLICABLE.
- **11.6**: common/common/common/common → APPLICABLE.
- **11.7**: common/common/common/common → APPLICABLE.
- **11.8**: common/common/common/common → APPLICABLE.
- **11.9**: common/common/common/common → APPLICABLE.
- **11.10**: common/common/common/common → APPLICABLE.
- **11.11**: common/common/common/common → APPLICABLE.
- **11.12**: common/common/common/common → APPLICABLE.
- **11.13**: common/common/common/common → APPLICABLE.

Now let me do the detailed matching. I need to read the contract sections 7-11 carefully and match against each matrix row.

Let me now build the analysis systematically. I'll read the contract_legal_propositions for the relevant contract clauses.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/extract_contract_clauses.py', 'content': 'import json, os\nbase = r"C:\\Users\\gogel\\OneDrive\\Рабочий стол\\Проекты\\skillshot_manual_2"\nwith open(os.path.join(base, \'outputs\', \'working\', \'contract_legal_propositions.json\'), \'r\', encoding=\'utf-8\') as f:\n    clp = json.load(f)\n\n# Find clauses in sections 7-12\nfor row in clp:\n    cid = row.get(\'id\', \'\')\n    # Check if id starts with 7., 8., 9., 10., 11., 12.\n    parts = cid.split(\'.\')\n    if parts[0] in [\'7\',\'8\',\'9\',\'10\',\'11\',\'12\']:\n        print(f"\\n=== {cid} ===")\n        print(f"type: {row.get(\'type\',\'\')}")\n        print(f"materiality: {row.get(\'materiality\',\'\')}")\n        print(f"protected_party: {row.get(\'protected_party\',\'\')}")\n        print(f"bound_party: {row.get(\'bound_party\',\'\')}")\n        print(f"right_or_obligation: {row.get(\'right_or_obligation\',\'\')}")\n        print(f"legal_object: {row.get(\'legal_object\',\'\')}")\n        print(f"trigger: {row.get(\'trigger\',\'\')}")\n        print(f"deadline: {row.get(\'deadline\',\'\')}")\n        print(f"amount_formula_cap: {row.get(\'amount_formula_cap\',\'\')}")\n        print(f"liability_remedy: {row.get(\'liability_remedy\',\'\')}")\n        print(f"consequence: {row.get(\'consequence\',\'\')}")\n        print(f"source_excerpt: {row.get(\'source_excerpt\',\'\')[:200]}")\n'}, 'id': 'call_00_40gM96W2XsQLXEqD922m5560', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/extract_contract_clauses.py
AI: [{'name': 'execute', 'args': {'command': 'python3 "/outputs/working/extract_contract_clauses.py"'}, 'id': 'call_00_YJL0GBKXdBsXIVs8GMz99965', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\extract_contract_clauses.py", line 8, in <module>
[stderr]     cid = row.get('id', '')
[stderr]           ^^^^^^^
[stderr] AttributeError: 'str' object has no attribute 'get'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_legal_propositions.json', 'limit': 30}, 'id': 'call_00_GHLNcbSjDyBWqmhiI2xR8902', 'type': 'tool_call'}]
Tool:      1	{
     2	  "schema_version": "1.0",
     3	  "source_file": "inputs\\contract.txt",
     4	  "generation": "seed for agent-led extraction and enrichment",
     5	  "contract": [
     6	    {
     7	      "id": "1",
     8	      "source_text": "ПРЕДМЕТ КОНТРАКТА",
     9	      "source_excerpt": "ПРЕДМЕТ КОНТРАКТА",
    10	      "type": "heading",
    11	      "materiality": "heading",
    12	      "protected_party": "",
    13	      "bound_party": "",
    14	      "right_or_obligation": "",
    15	      "legal_object": "",
    16	      "trigger": "",
    17	      "deadline": "",
    18	      "amount_formula_cap": "",
    19	      "procedure_channel": "",
    20	      "liability_remedy": "",
    21	      "scope_options": [],
    22	      "consequence": "",
    23	      "source_locator": "1",
    24	      "line_start": 5,
    25	      "line_end": 5,
    26	      "section_context": "г. Сочи «___»________20_ г.",
    27	      "final_allowed": false,
    28	      "evidence_only": true
    29	    },
    30	    {
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/extract_contract_clauses2.py', 'content': 'import json, os\nbase = r"C:\\Users\\gogel\\OneDrive\\Рабочий стол\\Проекты\\skillshot_manual_2"\nwith open(os.path.join(base, \'outputs\', \'working\', \'contract_legal_propositions.json\'), \'r\', encoding=\'utf-8\') as f:\n    data = json.load(f)\n\nclp = data.get(\'contract\', data) if isinstance(data, dict) else data\n\nfor row in clp:\n    if not isinstance(row, dict):\n        continue\n    cid = row.get(\'id\', \'\')\n    parts = cid.split(\'.\')\n    if parts[0] in [\'7\',\'8\',\'9\',\'10\',\'11\',\'12\']:\n        print(f"\\n=== {cid} ===")\n        print(f"type: {row.get(\'type\',\'\')}")\n        print(f"materiality: {row.get(\'materiality\',\'\')}")\n        print(f"protected_party: {row.get(\'protected_party\',\'\')}")\n        print(f"bound_party: {row.get(\'bound_party\',\'\')}")\n        print(f"right_or_obligation: {row.get(\'right_or_obligation\',\'\')}")\n        print(f"legal_object: {row.get(\'legal_object\',\'\')}")\n        print(f"trigger: {row.get(\'trigger\',\'\')}")\n        print(f"deadline: {row.get(\'deadline\',\'\')}")\n        print(f"amount_formula_cap: {row.get(\'amount_formula_cap\',\'\')}")\n        print(f"liability_remedy: {row.get(\'liability_remedy\',\'\')}")\n        print(f"consequence: {row.get(\'consequence\',\'\')}")\n        print(f"source_excerpt: {str(row.get(\'source_excerpt\',\'\'))[:200]}")\n        print(f"final_allowed: {row.get(\'final_allowed\',\'\')}")\n'}, 'id': 'call_00_eQLUgAej6i1mxUWPdQR43674', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/extract_contract_clauses2.py
AI: [{'name': 'execute', 'args': {'command': 'python3 "/outputs/working/extract_contract_clauses2.py"'}, 'id': 'call_00_rmQvCMRKNcJXGkGgaj7d6108', 'type': 'tool_call'}]
Tool: 
=== 7 ===
type: heading
materiality: heading
protected_party: 
bound_party: 
right_or_obligation: 
legal_object: 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќ
final_allowed: False

=== 7.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё. РЎС‚РѕСЂРѕРЅР° РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ СѓРїР»Р°С‚С‹
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё. РЎС‚РѕСЂРѕРЅР° РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ СѓРїР»Р°С‚С‹
final_allowed: True

=== 7.2 ===
type: operative
materiality: evaluable
protected_party: Bank
bound_party: Customer
right_or_obligation: right
legal_object: Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј,
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј,
final_allowed: True

=== 7.3 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ РїРѕСЃР»Рµ РґРЅСЏ РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ РїРѕСЃР»Рµ РґРЅСЏ РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±
final_allowed: True

=== 7.4 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РЁС‚СЂР°С„С‹ РЅР°С‡РёСЃР»СЏСЋС‚СЃСЏ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РЁС‚СЂР°С„С‹ РЅР°С‡РёСЃР»СЏСЋС‚СЃСЏ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј.
final_allowed: True

=== 7.4.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚
trigger: РІ СЃР»СѓС‡Р°Рµ РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р·Р°РєР°Р·С‡РёРєРѕРј
deadline: 
amount_formula_cap: 1000 СЂСѓР±Р»РµР№
liability_remedy: 
consequence: penalty
source_excerpt: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚
final_allowed: True

=== 7.5 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚РёР№РЅРѕРіРѕ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°), РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚Рµ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚РёР№РЅРѕРіРѕ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°), РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚Рµ
final_allowed: True

=== 7.6 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РґРЅРµРј РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РґРЅРµРј РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±
final_allowed: True

=== 7.7 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РЁС‚СЂР°С„С‹ РЅР°С‡РёСЃР»СЏСЋС‚СЃСЏ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚Рё
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РЁС‚СЂР°С„С‹ РЅР°С‡РёСЃР»СЏСЋС‚СЃСЏ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚Рё
final_allowed: True

=== 7.7.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚РёР№РЅРѕ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚РёР№РЅРѕ
final_allowed: True

=== 7.7.2 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РєР°Рє РїРѕР±РµРґРёС‚РµР»СЏ Р·Р°РєСѓРїРєРё (РёР»Рё РёРЅРѕРіРѕ СѓС‡Р°СЃС‚РЅРёРєР° Р·Р°РєСѓРїРєРё РІ СЃР»СѓС‡Р°СЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 05.04.2013 в„– 44-Р¤Р—), РїСЂРµРґР»РѕР¶РёРІС€РµРіРѕ РЅР°РёР±РѕР»РµРµ РІС‹СЃРѕРєСѓСЋ С†РµРЅСѓ Р·Р° РїСЂР°РІРѕ Р·Р°РєР»СЋС‡Рµ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РєР°Рє РїРѕР±РµРґРёС‚РµР»СЏ Р·Р°РєСѓРїРєРё (РёР»Рё РёРЅРѕРіРѕ СѓС‡Р°СЃС‚РЅРёРєР° Р·Р°РєСѓРїРєРё РІ СЃР»СѓС‡Р°СЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 05.04.2013 в„– 44-Р¤Р—), РїСЂРµРґР»РѕР¶РёРІС€РµРіРѕ РЅР°РёР±РѕР»РµРµ РІС‹СЃРѕРєСѓСЋ С†РµРЅСѓ Р·Р° РїСЂР°РІРѕ Р·Р°РєР»СЋС‡Рµ
final_allowed: True

=== 7.7.3 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ (РїСЂРё РЅР°Р»РёС‡РёРё РІ РљРѕРЅС‚СЂР°РєС‚Рµ С‚Р°РєРёС…
trigger: РїСЂРё РЅР°Р»РёС‡РёРё РІ РљРѕРЅС‚СЂР°РєС‚Рµ С‚Р°РєРёС… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ)
deadline: 
amount_formula_cap: 1000 СЂСѓР±Р»РµР№
liability_remedy: 
consequence: penalty
source_excerpt: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ (РїСЂРё РЅР°Р»РёС‡РёРё РІ РљРѕРЅС‚СЂР°РєС‚Рµ С‚Р°РєРёС…
final_allowed: True

=== 7.8 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ РѕР±РјРµРЅР° РґРѕРєСѓРјРµРЅС‚Р°РјРё РїСЂРё РїСЂРёРјРµРЅРµРЅРёРё РјРµСЂ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Рё СЃРѕРІРµСЂС€РµРЅРёРё РёРЅС‹С… РґРµР№СЃС‚РІРёР№ РІ СЃРІСЏР·Рё СЃ РЅР°СЂСѓС€РµРЅРёРµРј Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РёР»Рё Р—Р°РєР°Р·С‡РёРєРѕРј СѓСЃР»РѕРІРёР№ РљРѕРЅС‚СЂР°РєС‚Р°, С‚Р°РєРѕР№ РѕР±РјРµРЅ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ
trigger: РїСЂРё РїСЂРёРјРµРЅРµРЅРёРё РјРµСЂ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Рё СЃРѕРІРµСЂС€РµРЅРёРё РёРЅС‹С… РґРµР№СЃС‚РІРёР№ РІ СЃРІСЏР·Рё СЃ РЅР°СЂСѓС€РµРЅРёРµРј Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РёР»Рё Р—Р°РєР°Р·С‡РёРєРѕРј СѓСЃР»РѕРІРёР№ РљРѕРЅС‚СЂР°РєС‚Р°
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РѕР±РјРµРЅР° РґРѕРєСѓРјРµРЅС‚Р°РјРё РїСЂРё РїСЂРёРјРµРЅРµРЅРёРё РјРµСЂ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Рё СЃРѕРІРµСЂС€РµРЅРёРё РёРЅС‹С… РґРµР№СЃС‚РІРёР№ РІ СЃРІСЏР·Рё СЃ РЅР°СЂСѓС€РµРЅРёРµРј Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РёР»Рё Р—Р°РєР°Р·С‡РёРєРѕРј СѓСЃР»РѕРІРёР№ РљРѕРЅС‚СЂР°РєС‚Р°, С‚Р°РєРѕР№ РѕР±РјРµРЅ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ
final_allowed: True

=== 7.9 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРёРјРµРЅРµРЅРёРµ РЅРµСѓСЃС‚РѕР№РєРё (С€С‚СЂР°С„Р°, РїРµРЅРё) РЅРµ РѕСЃРІРѕР±РѕР¶РґР°РµС‚ РЎС‚РѕСЂРѕРЅС‹ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РџСЂРёРјРµРЅРµРЅРёРµ РЅРµСѓСЃС‚РѕР№РєРё (С€С‚СЂР°С„Р°, РїРµРЅРё) РЅРµ РѕСЃРІРѕР±РѕР¶РґР°РµС‚ РЎС‚РѕСЂРѕРЅС‹ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ.
final_allowed: True

=== 7.10 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ РљРѕРЅС‚СЂР°РєС‚Р°.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ РљРѕРЅС‚СЂР°РєС‚Р°.
final_allowed: True

=== 7.11 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ РљРѕРЅС‚СЂР°РєС‚Р°.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: penalty
source_excerpt: РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ РљРѕРЅС‚СЂР°РєС‚Р°.
final_allowed: True

=== 7.12 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РІ СЃРІСЏР·Рё СЃ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРёРј РѕС‚РєР°Р·РѕРј РЎС‚РѕСЂРѕРЅС‹ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РґСЂСѓРіР°СЏ РЎС‚РѕСЂРѕРЅР° РІРїСЂР°РІРµ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РјРµС‰РµРЅРёСЏ С‚РѕР»СЊРєРѕ С„Р°РєС‚РёС‡РµСЃРєРё РїРѕРЅРµСЃРµРЅРЅРѕРіРѕ СѓС‰РµСЂР±Р°, РЅРµРїРѕСЃСЂРµРґСЃС‚РІРµРЅРЅРѕ РѕР±СѓСЃР»Рѕ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: right granted
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РІ СЃРІСЏР·Рё СЃ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРёРј РѕС‚РєР°Р·РѕРј РЎС‚РѕСЂРѕРЅС‹ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РґСЂСѓРіР°СЏ РЎС‚РѕСЂРѕРЅР° РІРїСЂР°РІРµ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РјРµС‰РµРЅРёСЏ С‚РѕР»СЊРєРѕ С„Р°РєС‚РёС‡РµСЃРєРё РїРѕРЅРµСЃРµРЅРЅРѕРіРѕ СѓС‰РµСЂР±Р°, РЅРµРїРѕСЃСЂРµРґСЃС‚РІРµРЅРЅРѕ РѕР±СѓСЃР»Рѕ
final_allowed: True

=== 8 ===
type: heading
materiality: heading
protected_party: 
bound_party: 
right_or_obligation: 
legal_object: 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РљРђР§Р•РЎРўР’Рћ РћРљРђР—РђРќРќР«РҐ РЈРЎР›РЈР“, РџРћР РЇР”РћРљ Р�РҐ РџР Р�Р•РњРљР�. Р“РђР РђРќРўР�РЇ РљРђР§Р•РЎРўР’Рђ РЈРЎР›РЈР“
final_allowed: False

=== 8.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ Р—Р°РєР°Р·С‡РёРєСѓ РєР°С‡РµСЃС‚РІРѕ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РџСЂРёР»РѕР¶РµРЅРёСЏ в„–1 РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЃСЂРѕРєР°, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ РЅРѕСЂРјР°С‚РёРІРЅРѕ-РїСЂР°РІРѕРІС‹РјРё Р°РєС‚Р°РјРё Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ Р—Р°РєР°Р·С‡РёРєСѓ РєР°С‡РµСЃС‚РІРѕ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РџСЂРёР»РѕР¶РµРЅРёСЏ в„–1 РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЃСЂРѕРєР°, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ РЅРѕСЂРјР°С‚РёРІРЅРѕ-РїСЂР°РІРѕРІС‹РјРё Р°РєС‚Р°РјРё Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
final_allowed: True

=== 8.2 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РїРѕРІСЂРµР¶РґРµРЅРёСЏ, РІРѕР·РЅРёРєС€РёРµ РІСЃР»РµРґСЃС‚РІРёРµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РµРіРѕ СЃРїРµС†РёР°Р»РёСЃС‚Р°РјРё.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: liability
source_excerpt: Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РїРѕРІСЂРµР¶РґРµРЅРёСЏ, РІРѕР·РЅРёРєС€РёРµ РІСЃР»РµРґСЃС‚РІРёРµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РµРіРѕ СЃРїРµС†РёР°Р»РёСЃС‚Р°РјРё.
final_allowed: True

=== 8.3 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРёРµРјРєР° СЂРµР·СѓР»СЊС‚Р°С‚Р° РёСЃРїРѕР»РЅРµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё Рё РЅР°СЃС‚РѕСЏС‰РёРј РљРѕРЅС‚СЂР°РєС‚РѕРј.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџСЂРёРµРјРєР° СЂРµР·СѓР»СЊС‚Р°С‚Р° РёСЃРїРѕР»РЅРµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё Рё РЅР°СЃС‚РѕСЏС‰РёРј РљРѕРЅС‚СЂР°РєС‚РѕРј.
final_allowed: True

=== 8.3.1 ===
type: operative
materiality: evaluable
protected_party: Customer
bound_party: Bank
right_or_obligation: obligation
legal_object: Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј, С„РѕСЂРјРёСЂСѓРµС‚ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјС‹, РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅ
trigger: РїСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё Р·Р°РєСѓРїРєРё С‚РѕРІР°СЂР°); Р±) РЅР°РёРјРµРЅРѕРІР°РЅРёРµ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё; Рґ) РёРЅС„РѕСЂРјР°С†РёСЋ РѕР± РѕР±СЉРµРјРµ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё; Рµ) СЃС‚РѕРёРјРѕСЃС‚СЊ РёСЃРїРѕР»РЅРµРЅРЅС‹С… Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј, С„РѕСЂРјРёСЂСѓРµС‚ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјС‹, РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅ
final_allowed: True

=== 8.3.2 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Рљ РґРѕРєСѓРјРµРЅС‚Сѓ Рѕ РїСЂРёРµРјРєРµ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРјСѓ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р°, Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РїСЂРёР»Р°РіР°РµС‚ РґРѕРєСѓРјРµРЅС‚С‹, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹Рµ РљРѕРЅС‚СЂР°РєС‚РѕРј, РєРѕС‚РѕСЂС‹Рµ СЃС‡РёС‚Р°СЋС‚СЃСЏ РµРіРѕ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ: СЃС‡РµС‚-С„Р°РєС‚СѓСЂСѓ (РїСЂРё РЅР°Р»РёС‡РёРё), Р°Рє
trigger: РїСЂРё РЅР°Р»РёС‡РёРё)
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Рљ РґРѕРєСѓРјРµРЅС‚Сѓ Рѕ РїСЂРёРµРјРєРµ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРјСѓ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р°, Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РїСЂРёР»Р°РіР°РµС‚ РґРѕРєСѓРјРµРЅС‚С‹, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹Рµ РљРѕРЅС‚СЂР°РєС‚РѕРј, РєРѕС‚РѕСЂС‹Рµ СЃС‡РёС‚Р°СЋС‚СЃСЏ РµРіРѕ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ: СЃС‡РµС‚-С„Р°РєС‚СѓСЂСѓ (РїСЂРё РЅР°Р»РёС‡РёРё), Р°Рє
final_allowed: True

=== 8.4 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р”Р°С‚РѕР№ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј, СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° С‚Р°РєРѕРіРѕ РґРѕРєСѓРјРµРЅС‚Р° РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РІ СЃРѕРѕС‚РІ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р”Р°С‚РѕР№ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј, СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° С‚Р°РєРѕРіРѕ РґРѕРєСѓРјРµРЅС‚Р° РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РІ СЃРѕРѕС‚РІ
final_allowed: True

=== 8.5 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРёРµРјРєР° СѓСЃР»СѓРі РѕС‚ РёРјРµРЅРё Р—Р°РєР°Р·С‡РёРєР° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј, (Р»РёР±Рѕ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ вЂ“ Рї. 8.5.8) РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџСЂРёРµРјРєР° СѓСЃР»СѓРі РѕС‚ РёРјРµРЅРё Р—Р°РєР°Р·С‡РёРєР° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј, (Р»РёР±Рѕ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ вЂ“ Рї. 8.5.8) РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
final_allowed: True

=== 8.5.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р—Р°РєР°Р·С‡РёРє РІ СЃСЂРѕРє РЅРµ Р±РѕР»РµРµ 10 (РґРµСЃСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃРѕ РґРЅСЏ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 3 С‡Р°СЃС‚Рё 13 СЃС‚Р°С‚СЊРё 94 Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° в„– 44-Р¤Р—, РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РїРѕ
trigger: 
deadline: РІ СЃСЂРѕРє РЅРµ Р±РѕР»РµРµ 10 (РґРµСЃСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р—Р°РєР°Р·С‡РёРє РІ СЃСЂРѕРє РЅРµ Р±РѕР»РµРµ 10 (РґРµСЃСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃРѕ РґРЅСЏ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 3 С‡Р°СЃС‚Рё 13 СЃС‚Р°С‚СЊРё 94 Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° в„– 44-Р¤Р—, РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РїРѕ
final_allowed: True

=== 8.5.2 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ СѓРІРµРґРѕРјР»РµРЅРёСЋ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј Р—Р°РєР°Р·С‡РёРєР°, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РјРѕР¶РµС‚ РїСЂРѕРёР·РІРѕРґРёС‚СЊСЃСЏ С‚РѕР»СЊРєРѕ РІ РїСЂРёСЃСѓС‚СЃС‚РІРёРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, РёРјРµСЋС‰РµРіРѕ РЅР°РґР»РµР¶Р°С‰РёРј РѕР±СЂР°Р·РѕРј РѕС„РѕСЂРјР»РµРЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РЅР° СѓС‡Р°СЃ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: duty imposed
source_excerpt: РџРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ СѓРІРµРґРѕРјР»РµРЅРёСЋ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј Р—Р°РєР°Р·С‡РёРєР°, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РјРѕР¶РµС‚ РїСЂРѕРёР·РІРѕРґРёС‚СЊСЃСЏ С‚РѕР»СЊРєРѕ РІ РїСЂРёСЃСѓС‚СЃС‚РІРёРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, РёРјРµСЋС‰РµРіРѕ РЅР°РґР»РµР¶Р°С‰РёРј РѕР±СЂР°Р·РѕРј РѕС„РѕСЂРјР»РµРЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РЅР° СѓС‡Р°СЃ
final_allowed: True

=== 8.5.3 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РїРѕСЃС‚СѓРїРёР»Рѕ СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Р№ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРє, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ РІ РґРІСѓСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РїРѕСЃС‚СѓРїРёР»Рѕ СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Р№ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРє, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ РІ РґРІСѓСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.
final_allowed: True

=== 8.5.4 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РЅРµ РїРѕСЃС‚СѓРїРёР»Рѕ, Р»РёР±Рѕ РїРѕСЃС‚СѓРїРёР»Рѕ РІ Р±РѕР»РµРµ РїРѕР·РґРЅРёР№ СЃСЂРѕРє, С‡РµРј РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Р—Р°РєР°Р·С‡РёРєРѕРј РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РЅРµ РїРѕСЃС‚СѓРїРёР»Рѕ, Р»РёР±Рѕ РїРѕСЃС‚СѓРїРёР»Рѕ РІ Р±РѕР»РµРµ РїРѕР·РґРЅРёР№ СЃСЂРѕРє, С‡РµРј РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Р—Р°РєР°Р·С‡РёРєРѕРј РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј 
final_allowed: True

=== 8.5.5 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р”Р»СЏ РїСЂРѕРІРµСЂРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РІ С‡Р°СЃС‚Рё РёС… СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р°, Р—Р°РєР°Р·С‡РёРє РїСЂРѕРІРѕРґРёС‚ СЌРєСЃРїРµСЂС‚РёР·Сѓ.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р”Р»СЏ РїСЂРѕРІРµСЂРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РІ С‡Р°СЃС‚Рё РёС… СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р°, Р—Р°РєР°Р·С‡РёРє РїСЂРѕРІРѕРґРёС‚ СЌРєСЃРїРµСЂС‚РёР·Сѓ.
final_allowed: True

=== 8.5.6 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р­РєСЃРїРµСЂС‚РёР·Р° СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РјРѕР¶РµС‚ РїСЂРѕРІРѕРґРёС‚СЊСЃСЏ Р—Р°РєР°Р·С‡РёРєРѕРј СЃРІРѕРёРјРё СЃРёР»Р°РјРё РёР»Рё Рє РµРµ РїСЂРѕРІРµРґРµРЅРёСЋ РјРѕРіСѓС‚ РїСЂРёРІР»РµРєР°С‚СЊСЃСЏ СЌРєСЃРїРµСЂС‚С‹, СЌРєСЃРїРµСЂС‚РЅС‹Рµ РѕСЂРіР°РЅРёР·Р°С†РёРё РЅР° РѕСЃРЅРѕРІР°РЅРёРё РєРѕРЅС‚СЂР°РєС‚РѕРІ, Р·Р°РєР»СЋС‡РµРЅ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р­РєСЃРїРµСЂС‚РёР·Р° СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РјРѕР¶РµС‚ РїСЂРѕРІРѕРґРёС‚СЊСЃСЏ Р—Р°РєР°Р·С‡РёРєРѕРј СЃРІРѕРёРјРё СЃРёР»Р°РјРё РёР»Рё Рє РµРµ РїСЂРѕРІРµРґРµРЅРёСЋ РјРѕРіСѓС‚ РїСЂРёРІР»РµРєР°С‚СЊСЃСЏ СЌРєСЃРїРµСЂС‚С‹, СЌРєСЃРїРµСЂС‚РЅС‹Рµ РѕСЂРіР°РЅРёР·Р°С†РёРё РЅР° РѕСЃРЅРѕРІР°РЅРёРё РєРѕРЅС‚СЂР°РєС‚РѕРІ, Р·Р°РєР»СЋС‡РµРЅ
final_allowed: True

=== 8.5.7 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р·Р°РјРµС‡Р°РЅРёР№ Р—Р°РєР°Р·С‡РёРє (СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅРѕРµ Р»РёС†Рѕ) РІ С‚РµС‡РµРЅРёРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹, СЃР»РµРґСѓСЋС‰РµР№ Р·Р° РґРЅРµРј РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.4 РљРѕРЅС‚СЂР°РєС‚Р° РїРѕРґРїРёСЃС‹РІР°РµС‚ 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р·Р°РјРµС‡Р°РЅРёР№ Р—Р°РєР°Р·С‡РёРє (СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅРѕРµ Р»РёС†Рѕ) РІ С‚РµС‡РµРЅРёРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹, СЃР»РµРґСѓСЋС‰РµР№ Р·Р° РґРЅРµРј РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.4 РљРѕРЅС‚СЂР°РєС‚Р° РїРѕРґРїРёСЃС‹РІР°РµС‚ 
final_allowed: True

=== 8.5.8 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј Р±СѓРґСѓС‚ СѓСЃС‚Р°РЅРѕРІР»РµРЅС‹ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ С‚СЂРµР±РѕРІР°РЅРёСЏРј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ РљРѕРЅС‚СЂР°РєС‚Рµ, РґР°Р»СЊРЅРµР№С€Р°СЏ РїСЂРёРµРјРєР° РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊСЃСЏ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№. РќРµ РїРѕР·РґРЅРµРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№, СЃ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј Р±СѓРґСѓС‚ СѓСЃС‚Р°РЅРѕРІР»РµРЅС‹ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ С‚СЂРµР±РѕРІР°РЅРёСЏРј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ РљРѕРЅС‚СЂР°РєС‚Рµ, РґР°Р»СЊРЅРµР№С€Р°СЏ РїСЂРёРµРјРєР° РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊСЃСЏ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№. РќРµ РїРѕР·РґРЅРµРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№, СЃ
final_allowed: True

=== 8.5.9 ===
type: operative
materiality: evaluable
protected_party: Bank
bound_party: Customer
right_or_obligation: right
legal_object: Р’ СЃР»СѓС‡Р°Рµ РїРѕР»СѓС‡РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.5.8. РљРѕРЅС‚СЂР°РєС‚Р° РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРіРѕ РѕС‚РєР°Р·Р° РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІРїСЂР°РІРµ СѓСЃС‚СЂР°РЅРёС‚СЊ РїСЂРёС‡РёРЅС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ С‚Р°РєРѕРј РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРј РѕС‚РєР°Р·Рµ, Рё РЅ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: right granted
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РїРѕР»СѓС‡РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.5.8. РљРѕРЅС‚СЂР°РєС‚Р° РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРіРѕ РѕС‚РєР°Р·Р° РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІРїСЂР°РІРµ СѓСЃС‚СЂР°РЅРёС‚СЊ РїСЂРёС‡РёРЅС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ С‚Р°РєРѕРј РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРј РѕС‚РєР°Р·Рµ, Рё РЅ
final_allowed: True

=== 8.6 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р”Р°С‚РѕР№ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј РёР»Рё РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ Р—Р°РєР°Р·С‡РёРєР°.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р”Р°С‚РѕР№ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј РёР»Рё РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ Р—Р°РєР°Р·С‡РёРєР°.
final_allowed: True

=== 8.7 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’РЅРµСЃРµРЅРёРµ РёСЃРїСЂР°РІР»РµРЅРёР№ РІ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ, РѕС„РѕСЂРјР»РµРЅРЅС‹Р№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°СЃС‚РѕСЏС‰РёРј СЂР°Р·РґРµР»РѕРј РљРѕРЅС‚СЂР°РєС‚Р°, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСѓС‚РµРј С„РѕСЂРјРёСЂРѕРІР°РЅРёСЏ, РїРѕРґРїРёСЃР°РЅРёСЏ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹С… Р»РёС†
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’РЅРµСЃРµРЅРёРµ РёСЃРїСЂР°РІР»РµРЅРёР№ РІ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ, РѕС„РѕСЂРјР»РµРЅРЅС‹Р№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°СЃС‚РѕСЏС‰РёРј СЂР°Р·РґРµР»РѕРј РљРѕРЅС‚СЂР°РєС‚Р°, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСѓС‚РµРј С„РѕСЂРјРёСЂРѕРІР°РЅРёСЏ, РїРѕРґРїРёСЃР°РЅРёСЏ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹С… Р»РёС†
final_allowed: True

=== 8.8 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РћС„РѕСЂРјР»РµРЅРёРµ СЂРµР·СѓР»СЊС‚Р°С‚Р° РїСЂРѕРІРµРґРµРЅРёСЏ РїСЂРѕС†РµРґСѓСЂС‹ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ Рё РІ СЃСЂРѕРєРё, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ РЅР°СЃС‚РѕСЏС‰РµРј СЂР°Р·РґРµР»Рµ РљРѕРЅС‚СЂР°РєС‚Р°.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РћС„РѕСЂРјР»РµРЅРёРµ СЂРµР·СѓР»СЊС‚Р°С‚Р° РїСЂРѕРІРµРґРµРЅРёСЏ РїСЂРѕС†РµРґСѓСЂС‹ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ Рё РІ СЃСЂРѕРєРё, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ РЅР°СЃС‚РѕСЏС‰РµРј СЂР°Р·РґРµР»Рµ РљРѕРЅС‚СЂР°РєС‚Р°.
final_allowed: True

=== 8.9 ===
type: operative
materiality: evaluable
protected_party: Customer
bound_party: Bank
right_or_obligation: right
legal_object: Р’ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ РЅРµ РѕС‚РєР°Р·С‹РІР°С‚СЊ РІ РїСЂРёРµРјРєРµ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё, РµСЃР»Рё РІС‹СЏРІР»РµРЅРЅРѕРµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РїСЂРёРµРјРєРµ Рё СѓСЃС‚СЂР°РЅРµРЅРѕ Р�СЃРїРѕР»
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: right granted
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ РЅРµ РѕС‚РєР°Р·С‹РІР°С‚СЊ РІ РїСЂРёРµРјРєРµ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё, РµСЃР»Рё РІС‹СЏРІР»РµРЅРЅРѕРµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РїСЂРёРµРјРєРµ Рё СѓСЃС‚СЂР°РЅРµРЅРѕ Р�СЃРїРѕР»
final_allowed: True

=== 8.10 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР° Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·Р°РЅ Р±РµР·РІРѕР·РјРµР·РґРЅРѕ СѓСЃС‚СЂР°РЅРёС‚СЊ РЅРµРґРѕСЃС‚Р°С‚РєРё РІ С‚РµС‡РµРЅРёРµ 3 РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°СЏРІР»РµРЅРёСЏ Рѕ РЅРёС… Р—Р°РєР°Р·С‡РёРєРѕРј.
trigger: СЃ РґР°С‚С‹ Р·Р°СЏРІР»РµРЅРёСЏ Рѕ РЅРёС… Р—Р°РєР°Р·С‡РёРєРѕРј
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: duty imposed
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР° Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·Р°РЅ Р±РµР·РІРѕР·РјРµР·РґРЅРѕ СѓСЃС‚СЂР°РЅРёС‚СЊ РЅРµРґРѕСЃС‚Р°С‚РєРё РІ С‚РµС‡РµРЅРёРµ 3 РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°СЏРІР»РµРЅРёСЏ Рѕ РЅРёС… Р—Р°РєР°Р·С‡РёРєРѕРј.
final_allowed: True

=== 8.11 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџРѕРґРїРёСЃР°РЅРЅС‹Р№ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё Р—Р°РєР°Р·С‡РёРєР° Рё Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РѕРїР»Р°С‚С‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџРѕРґРїРёСЃР°РЅРЅС‹Р№ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё Р—Р°РєР°Р·С‡РёРєР° Рё Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РѕРїР»Р°С‚С‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі.
final_allowed: True

=== 9 ===
type: heading
materiality: heading
protected_party: 
bound_party: 
right_or_obligation: 
legal_object: 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р”Р•Р™РЎРўР’Р�Р• РћР‘РЎРўРћРЇРўР•Р›Р¬РЎРўР’ РќР•РџР Р•РћР”РћР›Р�РњРћР™ РЎР�Р›Р«
final_allowed: False

=== 9.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РЎС‚РѕСЂРѕРЅС‹ РѕСЃРІРѕР±РѕР¶РґР°СЋС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° С‡Р°СЃС‚РёС‡РЅРѕРµ РёР»Рё РїРѕР»РЅРѕРµ РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СЃРІРѕРёС… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ, РµСЃР»Рё РёС… РёСЃРїРѕР»РЅРµРЅРёСЋ РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ С‡СЂРµР·РІС‹С‡Р°Р№РЅРѕРµ Рё РЅРµРїСЂРµРѕРґРѕР»РёРјРѕРµ РїСЂРё РґР°РЅРЅС‹С… СѓСЃР»РѕРІРё
trigger: РїСЂРё РґР°РЅРЅС‹С… СѓСЃР»РѕРІРёСЏС… РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІРѕ (РЅРµРїСЂРµРѕРґРѕР»РёРјР°СЏ СЃРёР»Р°)
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РЎС‚РѕСЂРѕРЅС‹ РѕСЃРІРѕР±РѕР¶РґР°СЋС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° С‡Р°СЃС‚РёС‡РЅРѕРµ РёР»Рё РїРѕР»РЅРѕРµ РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СЃРІРѕРёС… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ, РµСЃР»Рё РёС… РёСЃРїРѕР»РЅРµРЅРёСЋ РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ С‡СЂРµР·РІС‹С‡Р°Р№РЅРѕРµ Рё РЅРµРїСЂРµРѕРґРѕР»РёРјРѕРµ РїСЂРё РґР°РЅРЅС‹С… СѓСЃР»РѕРІРё
final_allowed: True

=== 9.2 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРё РІРѕР·РЅРёРєРЅРѕРІРµРЅРёРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РёС… РёСЃРїРѕР»РЅРµРЅРёСЋ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ, РѕРЅР° РѕР±СЏР·Р°РЅР° РѕРїРѕРІРµСЃС‚РёС‚СЊ РґСЂСѓРіСѓСЋ РЎС‚РѕСЂРѕРЅСѓ РЅРµ РїРѕР·РґРЅРµРµ РїСЏС‚Рё РґРЅРµР№ СЃ РјРѕРјРµРЅС‚Р°
trigger: РїСЂРё СЌС‚РѕРј СЃСЂРѕРє РІС‹РїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РїРµСЂРµРЅРѕСЃРёС‚СЃСЏ СЃРѕСЂР°Р·РјРµСЂРЅРѕ РІСЂРµРјРµРЅРё
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: duty imposed
source_excerpt: РџСЂРё РІРѕР·РЅРёРєРЅРѕРІРµРЅРёРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РёС… РёСЃРїРѕР»РЅРµРЅРёСЋ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РѕРґРЅРѕР№ РёР· РЎС‚РѕСЂРѕРЅ, РѕРЅР° РѕР±СЏР·Р°РЅР° РѕРїРѕРІРµСЃС‚РёС‚СЊ РґСЂСѓРіСѓСЋ РЎС‚РѕСЂРѕРЅСѓ РЅРµ РїРѕР·РґРЅРµРµ РїСЏС‚Рё РґРЅРµР№ СЃ РјРѕРјРµРЅС‚Р°
final_allowed: True

=== 9.3 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРё СЂР°СЃСЃРјРѕС‚СЂРµРЅРёРё СЃРїРѕСЂРѕРІ РІ СЃРІСЏР·Рё СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹ СЃС‚РѕСЂРѕРЅР°, СЃСЃС‹Р»Р°СЋС‰Р°СЏСЃСЏ РЅР° СЌС‚Рё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°, РѕР±СЏР·Р°РЅР° РїСЂРµРґСЃС‚Р°РІРёС‚СЊ РґРѕРєСѓРјРµРЅС‚Р°Р»СЊРЅРѕРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РёС… РЅР°СЃС‚СѓРїР»РµРЅРёСЏ (РІС‹РґР°РЅРЅС‹Р№ Р»РёС†РѕРј, СѓРїРѕР»РЅ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: duty imposed
source_excerpt: РџСЂРё СЂР°СЃСЃРјРѕС‚СЂРµРЅРёРё СЃРїРѕСЂРѕРІ РІ СЃРІСЏР·Рё СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹ СЃС‚РѕСЂРѕРЅР°, СЃСЃС‹Р»Р°СЋС‰Р°СЏСЃСЏ РЅР° СЌС‚Рё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°, РѕР±СЏР·Р°РЅР° РїСЂРµРґСЃС‚Р°РІРёС‚СЊ РґРѕРєСѓРјРµРЅС‚Р°Р»СЊРЅРѕРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РёС… РЅР°СЃС‚СѓРїР»РµРЅРёСЏ (РІС‹РґР°РЅРЅС‹Р№ Р»РёС†РѕРј, СѓРїРѕР»РЅ
final_allowed: True

=== 10 ===
type: heading
materiality: heading
protected_party: 
bound_party: 
right_or_obligation: 
legal_object: 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџРћР РЇР”РћРљ Р РђР—Р Р•РЁР•РќР�РЇ РЎРџРћР РћР’
final_allowed: False

=== 10.1 ===
type: operative
materiality: evaluable
protected_party: Customer
bound_party: Bank
right_or_obligation: right
legal_object: Р’СЃРµ СЃРїРѕСЂС‹ РёР»Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ, РІРѕР·РЅРёРєР°СЋС‰РёРµ РјРµР¶РґСѓ РЎС‚РѕСЂРѕРЅР°РјРё РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РёР»Рё РІ СЃРІСЏР·Рё СЃ РЅРёРј, СЂР°Р·СЂРµС€Р°СЋС‚СЃСЏ РїСѓС‚РµРј РїРµСЂРµРіРѕРІРѕСЂРѕРІ (РІ РґРѕСЃСѓРґРµР±РЅРѕРј РїРѕСЂСЏРґРєРµ). РЎСЂРѕРє РѕС‚РІРµС‚Р° РЅР° РїСЂРµС‚РµРЅР·РёРё, РїРёСЃСЊРјР° Рё РѕР±СЂР°С‰РµРЅРёСЏ вЂ“ 1
trigger: РІ СЃР»СѓС‡Р°Рµ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРіРѕ РѕС‚РєР°Р·Р° РЎС‚РѕСЂРѕРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р° РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РіСЂР°Р¶РґР°РЅСЃРєРёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё
deadline: 10 (РґРµСЃСЏС‚СЊ) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№
amount_formula_cap: 
liability_remedy: 
consequence: duty imposed
source_excerpt: Р’СЃРµ СЃРїРѕСЂС‹ РёР»Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ, РІРѕР·РЅРёРєР°СЋС‰РёРµ РјРµР¶РґСѓ РЎС‚РѕСЂРѕРЅР°РјРё РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РёР»Рё РІ СЃРІСЏР·Рё СЃ РЅРёРј, СЂР°Р·СЂРµС€Р°СЋС‚СЃСЏ РїСѓС‚РµРј РїРµСЂРµРіРѕРІРѕСЂРѕРІ (РІ РґРѕСЃСѓРґРµР±РЅРѕРј РїРѕСЂСЏРґРєРµ). РЎСЂРѕРє РѕС‚РІРµС‚Р° РЅР° РїСЂРµС‚РµРЅР·РёРё, РїРёСЃСЊРјР° Рё РѕР±СЂР°С‰РµРЅРёСЏ вЂ“ 1
final_allowed: True

=== 11.6 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р�Р·РјРµРЅРµРЅРёРµ Рё(РёР»Рё) СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РєРѕРЅС‚СЂР°РєС‚Р° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ, СЃСЂРѕРєРё, СЃР»СѓС‡Р°СЏС… Рё РЅР° СѓСЃР»РѕРІРёСЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… СЃС‚Р°С‚СЊСЏРјРё 34, 95, 96, 112 Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° в„– 44-Р¤Р—.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р�Р·РјРµРЅРµРЅРёРµ Рё(РёР»Рё) СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РєРѕРЅС‚СЂР°РєС‚Р° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ, СЃСЂРѕРєРё, СЃР»СѓС‡Р°СЏС… Рё РЅР° СѓСЃР»РѕРІРёСЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… СЃС‚Р°С‚СЊСЏРјРё 34, 95, 96, 112 Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° в„– 44-Р¤Р—.
final_allowed: True

=== 11.7 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’Рѕ РІСЃРµРј, С‡С‚Рѕ РЅРµ РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РЅР°СЃС‚РѕСЏС‰РёРј РєРѕРЅС‚СЂР°РєС‚РѕРј, РЎС‚РѕСЂРѕРЅС‹ СЂСѓРєРѕРІРѕРґСЃС‚РІСѓСЋС‚СЃСЏ РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: Р’Рѕ РІСЃРµРј, С‡С‚Рѕ РЅРµ РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РЅР°СЃС‚РѕСЏС‰РёРј РєРѕРЅС‚СЂР°РєС‚РѕРј, РЎС‚РѕСЂРѕРЅС‹ СЂСѓРєРѕРІРѕРґСЃС‚РІСѓСЋС‚СЃСЏ РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
final_allowed: True

=== 11.8 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РЎС‚РѕСЂРѕРЅС‹ РїСЂРµРґСѓСЃРјРѕС‚СЂРµР»Рё, С‡С‚Рѕ РёР·РјРµРЅРµРЅРёРµ СЃСѓС‰РµСЃС‚РІРµРЅРЅС‹С… СѓСЃР»РѕРІРёР№ РєРѕРЅС‚СЂР°РєС‚Р° РїСЂРё РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёРё РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃСЏ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РёС… РёР·РјРµРЅРµРЅРёСЏ РїРѕ СЃРѕРіР»Р°С€РµРЅРёСЋ РЎС‚РѕСЂРѕРЅ РІ СЃР»СѓС‡Р°СЏС…, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј в„–
trigger: РїСЂРё РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёРё РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃСЏ
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РЎС‚РѕСЂРѕРЅС‹ РїСЂРµРґСѓСЃРјРѕС‚СЂРµР»Рё, С‡С‚Рѕ РёР·РјРµРЅРµРЅРёРµ СЃСѓС‰РµСЃС‚РІРµРЅРЅС‹С… СѓСЃР»РѕРІРёР№ РєРѕРЅС‚СЂР°РєС‚Р° РїСЂРё РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёРё РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃСЏ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РёС… РёР·РјРµРЅРµРЅРёСЏ РїРѕ СЃРѕРіР»Р°С€РµРЅРёСЋ РЎС‚РѕСЂРѕРЅ РІ СЃР»СѓС‡Р°СЏС…, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј в„–
final_allowed: True

=== 12 ===
type: heading
materiality: heading
protected_party: 
bound_party: 
right_or_obligation: 
legal_object: 
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ
final_allowed: False

=== 12.1 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРё РёСЃРїРѕР»РЅРµРЅРёРё РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РїРµСЂРµРјРµРЅР° Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°СЏ, РєРѕРіРґР° РЅРѕРІС‹Р№ РёСЃРїРѕР»РЅРёС‚РµР»СЊ СЏРІР»СЏРµС‚СЃСЏ РїСЂР°РІРѕРїСЂРµРµРјРЅРёРєРѕРј Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РІСЃР»РµРґСЃС‚РІРёРµ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё СЋСЂРёРґРё
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџСЂРё РёСЃРїРѕР»РЅРµРЅРёРё РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РїРµСЂРµРјРµРЅР° Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°СЏ, РєРѕРіРґР° РЅРѕРІС‹Р№ РёСЃРїРѕР»РЅРёС‚РµР»СЊ СЏРІР»СЏРµС‚СЃСЏ РїСЂР°РІРѕРїСЂРµРµРјРЅРёРєРѕРј Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РІСЃР»РµРґСЃС‚РІРёРµ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё СЋСЂРёРґРё
final_allowed: True

=== 12.2 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: Р’ СЃР»СѓС‡Р°Рµ РїРµСЂРµРјРµРЅС‹ Р—Р°РєР°Р·С‡РёРєР° РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РїСЂР°РІР° Рё РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё Р—Р°РєР°Р·С‡РёРєР° РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РїРµСЂРµС…РѕРґСЏС‚ Рє РЅРѕРІРѕРјСѓ Р—Р°РєР°Р·С‡РёРєСѓ РІ С‚РѕРј Р¶Рµ РѕР±СЉРµРјРµ Рё РЅР° С‚РµС… Р¶Рµ СѓСЃР»РѕРІРёСЏС….
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: duty imposed
source_excerpt: Р’ СЃР»СѓС‡Р°Рµ РїРµСЂРµРјРµРЅС‹ Р—Р°РєР°Р·С‡РёРєР° РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РїСЂР°РІР° Рё РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё Р—Р°РєР°Р·С‡РёРєР° РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РїРµСЂРµС…РѕРґСЏС‚ Рє РЅРѕРІРѕРјСѓ Р—Р°РєР°Р·С‡РёРєСѓ РІ С‚РѕРј Р¶Рµ РѕР±СЉРµРјРµ Рё РЅР° С‚РµС… Р¶Рµ СѓСЃР»РѕРІРёСЏС….
final_allowed: True

=== 12.3 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РџСЂРё РёСЃРїРѕР»РЅРµРЅРёРё РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЋ Р—Р°РєР°Р·С‡РёРєР° СЃ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РѕРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРіРё, РєР°С‡РµСЃС‚РІРѕ, С‚РµС…РЅРёС‡РµСЃРєРёРµ Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹Рµ С…Р°СЂР°РєС‚РµСЂРёСЃС‚РёРєРё (РїРѕС‚СЂРµР±РёС‚РµР»СЊСЃРєРёРµ СЃРІРѕР№СЃС‚РІР°) РєРѕС‚РѕСЂС‹С… СЏРІР»СЏСЋС‚СЃСЏ СѓР»СѓС‡С€РµРЅ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РџСЂРё РёСЃРїРѕР»РЅРµРЅРёРё РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЋ Р—Р°РєР°Р·С‡РёРєР° СЃ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РѕРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРіРё, РєР°С‡РµСЃС‚РІРѕ, С‚РµС…РЅРёС‡РµСЃРєРёРµ Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹Рµ С…Р°СЂР°РєС‚РµСЂРёСЃС‚РёРєРё (РїРѕС‚СЂРµР±РёС‚РµР»СЊСЃРєРёРµ СЃРІРѕР№СЃС‚РІР°) РєРѕС‚РѕСЂС‹С… СЏРІР»СЏСЋС‚СЃСЏ СѓР»СѓС‡С€РµРЅ
final_allowed: True

=== 12.4 ===
type: operative
materiality: evaluable
protected_party: Both
bound_party: Both
right_or_obligation: mixed
legal_object: РљРѕРЅС‚СЂР°РєС‚ СЃРѕСЃС‚Р°РІР»РµРЅ РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ С„РѕСЂРјРµ Рё РїРѕРґРїРёСЃР°РЅ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ РЎС‚РѕСЂРѕРЅ. 12.5. РџСЂРёР»РѕР¶РµРЅРёСЏ: в„– 1 В«РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµВ» в„– 2 В«РЎРїРµС†РёС„РёРєР°С†РёСЏВ» 13. РњР•РЎРўРђ РќРђРҐРћР–Р”Р•РќР�РЇ, Р‘РђРќРљРћР’РЎРљ
trigger: 
deadline: 
amount_formula_cap: 
liability_remedy: 
consequence: 
source_excerpt: РљРѕРЅС‚СЂР°РєС‚ СЃРѕСЃС‚Р°РІР»РµРЅ РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ С„РѕСЂРјРµ Рё РїРѕРґРїРёСЃР°РЅ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ РЎС‚РѕСЂРѕРЅ. 12.5. РџСЂРёР»РѕР¶РµРЅРёСЏ: в„– 1 В«РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµВ» в„– 2 В«РЎРїРµС†РёС„РёРєР°С†РёСЏВ» 13. РњР•РЎРўРђ РќРђРҐРћР–Р”Р•РќР�РЇ, Р‘РђРќРљРћР’РЎРљ
final_allowed: True

[Command succeeded with exit code 0]
AI: Now I have a comprehensive picture of both the matrix and contract clauses. Let me also check for the remaining contract clauses in sections 10 and 11 that I need.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/extract_remaining.py', 'content': 'import json, os\nbase = r"C:\\Users\\gogel\\OneDrive\\Рабочий стол\\Проекты\\skillshot_manual_2"\nwith open(os.path.join(base, \'outputs\', \'working\', \'contract_legal_propositions.json\'), \'r\', encoding=\'utf-8\') as f:\n    data = json.load(f)\n\nclp = data.get(\'contract\', data) if isinstance(data, dict) else data\n\n# Find clauses 10.2, 11.1-11.5\ntargets = [\'10.2\',\'11.1\',\'11.2\',\'11.3\',\'11.4\',\'11.5\']\nfor row in clp:\n    if not isinstance(row, dict):\n        continue\n    cid = row.get(\'id\', \'\')\n    if cid in targets:\n        print(f"\\n=== {cid} ===")\n        print(f"type: {row.get(\'type\',\'\')}")\n        print(f"materiality: {row.get(\'materiality\',\'\')}")\n        print(f"protected_party: {row.get(\'protected_party\',\'\')}")\n        print(f"bound_party: {row.get(\'bound_party\',\'\')}")\n        print(f"right_or_obligation: {row.get(\'right_or_obligation\',\'\')}")\n        print(f"legal_object: {row.get(\'legal_object\',\'\')}")\n        print(f"deadline: {row.get(\'deadline\',\'\')}")\n        print(f"consequence: {row.get(\'consequence\',\'\')}")\n        print(f"source_excerpt: {str(row.get(\'source_excerpt\',\'\'))[:200]}")\n        print(f"final_allowed: {row.get(\'final_allowed\',\'\')}")\n'}, 'id': 'call_00_sEm3LMHHhkTnt5mZWL4r8356', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/extract_remaining.py
AI: [{'name': 'execute', 'args': {'command': 'python3 "/outputs/working/extract_remaining.py"'}, 'id': 'call_00_uCMKPSMSPF7E7pGP1cql6670', 'type': 'tool_call'}]
Tool: <no output>
[Command succeeded with exit code 0]
AI: Those clauses aren't in the contract_legal_propositions. Let me check what contract clauses exist in sections 10-11.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/find_missing.py', 'content': 'import json, os\nbase = r"C:\\Users\\gogel\\OneDrive\\Рабочий стол\\Проекты\\skillshot_manual_2"\nwith open(os.path.join(base, \'outputs\', \'working\', \'contract_legal_propositions.json\'), \'r\', encoding=\'utf-8\') as f:\n    data = json.load(f)\n\nclp = data.get(\'contract\', data) if isinstance(data, dict) else data\n\nall_ids = set()\nfor row in clp:\n    if not isinstance(row, dict):\n        continue\n    cid = row.get(\'id\', \'\')\n    all_ids.add(cid)\n\n# Find all ids starting with 10 or 11\nfor cid in sorted(all_ids):\n    parts = cid.split(\'.\')\n    if parts[0] in [\'10\',\'11\']:\n        print(cid)\n'}, 'id': 'call_00_oO5eMT9QZekt6P6zV3pV6717', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/find_missing.py

