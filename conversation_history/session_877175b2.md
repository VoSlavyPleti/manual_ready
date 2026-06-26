## Summarized at 2026-06-25T18:53:32.064965+00:00

Human: Contract extra review
AI: I'll start by reading the skill file to understand the full workflow, then examine the available data files.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_j5aGzeiAXQtrUi13MVbE3457', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/'}, 'id': 'call_01_7c4Ex4SrZp81bu8grmFU3928', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-discrepancy-analysis
     3	description: "Compare a bank acquiring standard matrix with a counterparty acquiring contract using bidirectional legal proposition coverage, group-level statuses, missing bank-standard requirements, and material contract-only terms."
     4	---
     5	
     6	# Acquiring Discrepancy Analysis
     7	
     8	Use this skill to compare a Bank standard acquiring matrix with a counterparty
     9	acquiring contract. The matrix is the Bank standard. The contract is checked
    10	against that standard. The output is a many-to-many legal coverage graph plus a
    11	two-sheet review table generated from the JSON.
    12	
    13	Before finalization, read:
    14	
    15	- `references/output-contract.md` for artifact shape and field contracts.
    16	- `references/comparison-patterns.md` for calibration examples.
    17	
    18	## Purpose
    19	
    20	Find and explain:
    21	
    22	- Bank-standard matrix requirements preserved by the contract;
    23	- true analogues that deviate from the Bank standard;
    24	- applicable matrix requirements absent from the contract;
    25	- legally meaningful contract terms with no matrix analogue.
    26	- matrix requirements that are out of scope for the current contract profile,
    27	  closed in the internal ledger without final risk reporting.
    28	
    29	The review is risk-oriented. Missing a real risk is worse than marking a
    30	borderline issue as `deviation`, but weak thematic matches must not be promoted
    31	into legal links.
    32	
    33	## Inputs And Outputs
    34	
    35	Inputs:
    36	
    37	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    38	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    39	  applicability filters.
    40	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    41	  ids or real document locators visible in this file.
    42	
    43	Final outputs:
    44	
    45	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    46	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    47	
    48	Working artifacts belong under `/outputs/working/`.
    49	
    50	## Source Hierarchy
    51	
    52	Use the source text as the legal authority:
    53	
    54	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    55	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    56	3. Working ledgers as indexes and evidence aids.
    57	
    58	Do not decide status from extracted fields alone. When a status depends on a
    59	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    60	consequence, re-read the source text.
    61	
    62	## Required Artifacts And Contracts
    63	
    64	Create the artifacts in this order. Each later step depends on the earlier
    65	artifact contract.
    66	
    67	### 1. Source Preflight
    68	
    69	Check `inputs/contract.txt` before analysis:
    70	
    71	- real clause numbering is present;
    72	- deep clause numbers are not visibly collapsed or shifted;
    73	- repeated locators have enough context to distinguish source rows;
    74	- text is readable and not corrupted by encoding.
    75	
    76	If the contract text is not usable, stop and write
    77	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
    78	invalid text.
    79	
    80	### 2. Clause Index
    81	
    82	Create `/outputs/working/clause_index.json`.
    83	
    84	It is a source map only. It must include:
    85	
    86	- every matrix `number`;
    87	- every contract clause, operative parent, definition, appendix/table row, and
    88	  unnumbered operative provision;
    89	- source text or source locator for each row;
    90	- context for duplicate printed contract ids.
    91	
    92	Do not use `clause_index` to decide legal status. It only proves source
    93	coverage and valid ids. Never overwrite it with a batch subset.
    94	
    95	### 3. Legal Proposition Ledger
    96	
    97	Create `/outputs/working/legal_propositions.json`.
    98	
    99	This is the mandatory legal evidence ledger. It must contain `matrix` and
   100	`contract` arrays. Every evaluable proposition should include:
   101	
   102	- `id`: matrix number or printed contract locator;
   103	- `source_text`: text used for legal comparison;
   104	- `source_excerpt`: short quote supporting the normalized proposition;
   105	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   106	  `appendix`, `table`, or `technical`;
   107	- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
   108	- `protected_party`, `bound_party`;
   109	- `right_or_obligation`;
   110	- `legal_object`;
   111	- `trigger`;
   112	- `deadline`;
   113	- `amount_formula_cap`;
   114	- `procedure_channel`;
   115	- `liability_remedy`;
   116	- `scope_options`;
   117	- `consequence`;
   118	- `applicability_filters` where available.
   119	
   120	If a legally meaningful row cannot be normalized, mark it
   121	`needs_source_review` and explain the missing element. It is not fully
   122	processed until the source text has been reviewed. Do not proceed to final
   123	matching with unresolved source-review rows that could affect status.
   124	
   125	The ledger is an evidence table, not a substitute for the source. Matching may
   126	use it to find candidates. Status must still be confirmed against source text.
   127	
   128	Run the mechanical check before matching:
   129	
   130	```bash
   131	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working
   132	```
   133	
   134	Fix invalid working artifacts before delegating comparison work.
   135	
   136	### 4. Contract Product Profile
   137	
   138	Create `/outputs/working/contract_product_profile.json`.
   139	
   140	Extract from the contract:
   141	
   142	- product and payment channels;
   143	- lot/procurement type;
   144	- terminal/payment-device scope;
   145	- payment methods;
   146	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   147	
   148	Apply matrix filters before status:
   149	
   150	- `common` applies to every contract.
   151	- A filtered matrix item applies only when the profile matches
   152	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   153	- Mandatory applicable missing = high risk.
   154	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   155	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   156	  profile-based reason. Do not put them in final `unmatched_matrix`.
   157	- Optional applicable missing = low or conditional risk.
   158	- Slash-separated alternatives are options unless the matrix says all options
   159	  are mandatory.
   160	- Placeholder or blank in an applicable material term = low-risk `deviation`.
   161	
   162	### 5. Domain Crosswalk
   163	
   164	Create `/outputs/working/domain_crosswalk.json` before final JSON assembly.
   165	
   166	This is the mandatory mapping ledger. It is where legal candidate groups are
   167	formed and checked before they become final `links`, `unmatched_matrix`, or
   168	`unmatched_contract`. Do not let first-time legal mapping decisions appear only
   169	inside a final-builder script.
   170	
   171	Split the review into legal domains so each domain can be checked for complete
   172	assigned/processed coverage:
   173	
   174	- `scope_price_subject`;
   175	- `payment_acceptance_documents`;
   176	- `operational_obligations_products`;
   177	- `liability_penalties_indemnities`;
   178	- `term_termination_suspension`;
   179	- `confidentiality_pdn_disputes_assignment`;
   180	- `appendices_tables_locations`.
   181	
   182	Each domain row must contain:
   183	
   184	- `domain`;
   185	- `assigned_matrix_ids`;
   186	- `assigned_contract_ids`;
   187	- `processed_matrix_ids`;
   188	- `processed_contract_ids`;
   189	- `candidate_groups`;
   190	- `provisional_missing_matrix`;
   191	- `provisional_extra_contract`;
   192	- `explicitly_skipped_ids` with reasons such as `out_of_scope`,
   193	  `not_applicable`, `heading`, or `not_material`;
   194	- `unresolved_ids`.
   195	
   196	The orchestrator may not finalize while `unresolved_ids` is non-empty or while
   197	assigned ids are missing from `processed_*` plus `explicitly_skipped_ids`.
   198	
   199	After creating the crosswalk, run:
   200	
   201	```bash
   202	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --require-crosswalk
   203	```
   204	
   205	Fix incomplete domains before final JSON assembly.
   206	
   207	Use the crosswalk to reconcile both directions:
   208	
   209	- if matrix-to-contract finds a candidate, contract-to-matrix must either keep
   210	  the same link or explain why it is weak context;
   211	- if contract-to-matrix finds a true analogue not found in matrix-to-contract,
   212	  add it to the candidate group;
   213	- if a contract clause is final `extra_in_contract`, it must have no true matrix
   214	  analogue in the crosswalk;
   215	- if a matrix id is final `missing_in_contract`, every considered contract
   216	  candidate must be weak, out of scope, or legally different.
   217	
   218	## Analogue Threshold
   219	
   220	Create a final link only when the contract proposition is a true legal analogue
   221	of the matrix proposition. Test:
   222	
   223	- same or equivalent protected party;
   224	- same or equivalent bound party;
   225	- same legal object;
   226	- same operative right, duty, prohibition, permission, remedy, or allocation of
   227	  risk;
   228	- material trigger, scope, procedure, and consequence are the same or legally
   229	  equivalent.
   230	
   231	Reject weak thematic candidates. A clause about the same broad topic is not a
   232	legal analogue when it governs a different object, party, trigger, procedure,
   233	or consequence.
   234	
   235	## Bidirectional Matching
   236	
   237	Perform both directions.
   238	
   239	Matrix to contract:
   240	
   241	- for each applicable evaluable matrix proposition, retrieve all contract
   242	  clauses that collectively cover the Bank-standard requirement;
   243	- include parent, child, appendix, payment, procedure, liability, and framework
   244	  clauses only when they provide material coverage or legally cure a gap.
   245	- if a child clause is selected, check whether its parent carries operative
   246	  legal meaning for the same topic; if a parent is selected, check whether its
   247	  children contain the material elements;
   248	- for payment, acceptance, liability, termination, and document-exchange
   249	  requirements, keep the legal package together: operative clause, basis,
   250	  deadline, procedure, remedy, consequence, and any incorporated appendix/table
   251	  row that changes coverage;
   252	- a framework or legal-compliance clause may be a standalone analogue only when
   253	  it carries the same legal object or allocates the same risk, duty, or remedy.
   254	
   255	Contract to matrix:
   256	
   257	- for each evaluable contract proposition, find the matrix analogue group;
   258	- if an analogue exists, the contract locator must appear in final `links`;
   259	- if none exists and the term has independent legal effect, classify it as
   260	  provisional `extra_in_contract` in the crosswalk and final
   261	  `extra_in_contract` after reconciliation;
   262	- if it is non-operative, close it as `not_material` only in the ledger after
   263	  checking the materiality ladder below.
   264	
   265	Group related ids into many-to-many `links`. One matrix id may need several
   266	contract clauses. One contract clause may cover several matrix ids.
   267	
   268	### Contract Row Preservation
   269	
   270	If a contract clause is a standalone legal analogue for a matrix requirement,
   271	preserve its printed `contract_id` in final `links`. Do not replace a material
   272	child row with only a broad parent row, and do not replace a material parent
   273	row with only children when the parent carries the operative legal object.
   274	
   275	Large contract clauses often cover many matrix requirements at once. When a
   276	contract clause regulates several duties, documents, payments, liabilities,
   277	procedures, or remedies, keep all relevant matrix ids in the group instead of
   278	selecting only the most obvious one.
   279	
   280	Appendices and tables are legal evidence when they define services, terminal
   281	locations, tariffs, payment scope, acceptance documents, implementation
   282	details, or incorporated obligations. They are not technical residue merely
   283	because they are outside the main body.
   284	
   285	### No Silent Matrix Closure
   286	
   287	Every in-scope evaluable matrix id must be visibly closed:
   288	
   289	- in final `links`;
   290	- in final `unmatched_matrix`; or
   291	- in `coverage_ledger.matrix` as `out_of_scope`, `not_applicable`, or
   292	  source-based `not_evaluable`.
   293	
   294	`coverage_ledger.matrix.closure = linked` is allowed only when the matrix id
   295	appears in final `links`. A weak thematic candidate is not a link; keep the
   296	matrix id as `missing_in_contract` and record the candidate as rejected.
   297	
   298	Before finalizing `unmatched_matrix`, perform a short targeted rescue pass:
   299	
   300	- re-read matrix `source_text` / `enriched_text`;
   301	- search contract source text in the same legal domain;
   302	- check parent, child, sibling, referenced appendix/table, and procurement
   303	  analogue clauses;
   304	- if no true analogue exists, keep `missing_in_contract`.
   305	
   306	### Contract-Only Materiality Ladder
   307	
   308	Start from the presumption that every evaluable unlinked contract clause is an
   309	`extra_in_contract` candidate. Downgrade to `not_material` only when source text
   310	shows that the row is:
   311	
   312	- a heading or section label;
   313	- requisites, signatures, addresses, purely administrative notice data;
   314	- a blank technical form without legal effect;
   315	- a definition that does not change scope, liability, parties, remedies, or
   316	  procedure;
   317	- a parent row with no independent right, duty, limitation, procedure, or
   318	  consequence;
   319	- a duplicate child row that adds no legal element beyond a linked row.
   320	
   321	Do not downgrade a contract clause to `not_material` if it contains an
   322	independent legal effect, including:
   323	
   324	- inspection, audit, control, correction, rejection, refusal, or acceptance
   325	  rights;
   326	- expert examination or document-signing procedure;
   327	- payment, acceptance, or reporting deadline;
   328	- withholding, suspension, set-off, or budget/treasury payment condition;
   329	- fine, penalty, damages, cap, formula, or claim procedure;
   330	- unilateral termination/refusal;
   331	- assignment restriction;
   332	- anti-corruption, confidentiality, personal-data, sanctions, or statutory
   333	  compliance duty;
   334	- mandatory EIS/44-FZ/223-FZ procedure with its own consequence.
   335	
   336	For contract-only reporting, prefer the most specific material child clauses.
   337	Report a parent as final `extra_in_contract` only when the parent itself creates
   338	an independent right, duty, limitation, procedure, or consequence. Do not
   339	replace a set of material children with one generic parent.
   340	
   341	## Group-Level Status
   342	
   343	Assign status to the group, not to each atomic pair.
   344	
   345	- `aligned`: the contract package preserves the matrix legal result.
   346	- `deviation`: a true analogue exists, but any material element is changed,
   347	  narrowed, weakened, omitted, shifted, or blank.
   348	- `missing_in_contract`: no true contract analogue exists for an applicable
   349	  matrix requirement.
   350	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   351	  analogue.
   352	- `not_material`: internal ledger closure only; exclude from final report.
   353	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
   354	  final report because the requirement does not apply to the current product,
   355	  lot, terminal, payment method, or legal regime.
   356	
   357	Material elements include party, legal object, operative act, trigger,
   358	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   359	remedy, exception, Bank right, merchant duty, and consequence.
   360	
   361	Hard terms must be compared directly:
   362	
   363	- same material deadline/amount/procedure in the same legal obligation can be
   364	  `aligned`;
   365	- changed value or missing value is `deviation`;
   366	- a hard term from another clause counts only when that clause expressly
   367	  governs the same obligation or is explicitly incorporated;
   368	- a neighboring date, amount, or procedure for another legal object cannot cure
   369	  the gap.
   370	
   371	Do not downgrade for formal differences alone: heading, title, appendix label,
   372	permitted option selection, equivalent mandatory-law mechanism, or wording
   373	style.
   374	
   375	Do not downgrade for low-risk notes when the legal result is preserved. If the
   376	reason says the difference is merely terminological, beneficial to the Bank,
   377	already incorporated through another clause, or caused only by a mandatory
   378	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
   379	
   380	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
   381	when it materially worsens or changes a Bank-standard term: payment timing,
   382	acceptance control, withholding right, penalty/cap, termination power, protected
   383	party, evidence channel, or enforceability.
   384	
   385	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
   386	Before marking a liability group `aligned`, check the amount, formula, cap,
   387	trigger, protected party, excluded delay/non-delay buckets, and claim procedure
   388	across the whole package.
   389	
   390	## Risk Calibration
   391	
   392	Use `risk_level` consistently:
   393	
   394	- `none`: only for `aligned`;
   395	- `low`: optional applicable missing, placeholder, formal but legally manageable
   396	  gap;
   397	- `medium`: material deviation that can affect performance, evidence, payment,
   398	  control, liability, or enforceability;
   399	- `high`: mandatory missing, changed protected party, major payment/remedy
   400	  change, important Bank right omitted, or broad contract-only risk.
   401	
   402	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   403	a short evidence-based reason. Use concise quotes rather than long excerpts.
   404	
   405	## Final QA
   406	
   407	Before writing final artifacts:
   408	
   409	- verify `clause_index` covers all source ids;
   410	- verify `legal_proposition_ledger` has no unresolved
   411	  `needs_source_review` rows that can affect final status;
   412	- verify `domain_crosswalk` exists and every domain has complete
   413	  assigned/processed coverage;
   414	- verify `unresolved_ids` is empty in every crosswalk domain;
   415	- verify every final `link`, `unmatched_matrix`, and `unmatched_contract` can be
   416	  traced to a crosswalk candidate group, provisional missing row, or
   417	  provisional extra row;
   418	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   419	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   420	  `coverage_ledger`;
   421	- verify every applicable evaluable matrix id is linked or in
   422	  `unmatched_matrix`;
   423	- verify out-of-scope / non-applicable matrix ids are not in final
   424	  `unmatched_matrix`;
   425	- verify every material contract id is closed as linked or extra;
   426	- verify every contract id closed as `not_material` satisfies the materiality
   427	  ladder and does not contain independent legal effect;
   428	- verify `coverage_ledger` is derived from final `links`,
   429	  `unmatched_matrix`, and `unmatched_contract`;
   430	- verify every final id is visible in source text;
   431	- verify `aligned` has no material discrepancy;
   432	- verify every `deviation` has a named legal gap and evidence;
   433	- verify weak candidates are not in final `links`;
   434	- verify non-material contract rows are absent from final `unmatched_contract`;
   435	- verify summary counts equal final arrays.
   436	
   437	## Output Discipline
   438	
   439	Follow `references/output-contract.md`.
   440	
   441	The final JSON must contain:
   442	
   443	- `analysis_profile`
   444	- `links`
   445	- `atomic_links`
   446	- `unmatched_matrix`
   447	- `unmatched_contract`
   448	- `coverage_ledger`
   449	- `summary`
   450	
   451	`links` carry group-level legal findings. `atomic_links` are traceability
   452	projections only and must inherit the group relationship. Do not assign
   453	separate final pair-level statuses.
   454	
   455	## Tools And Scripts
   456	
   457	Use helper scripts for mechanical work: source extraction, indexing,
   458	normalization checks, batch completeness, coverage validation, JSON schema
   459	checks, and Excel export. Do not put legal mapping or status decisions into
   460	hardcoded scripts.
Tool: ['/.agents/', '/.codex/', '/.env', '/.git/', '/.gitignore', '/.venv/', '/ALL_DATA/', '/README.md', '/__pycache__/', '/conversation_history/', '/inputs/', '/llm.py', '/main.py', '/output/', '/outputs/', '/run_logs/', '/runs/', '/skills/', '/tools/']
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_00_jsOjJDBIfwHla3NyBLkf7911', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_01_WSOpP8tXhuJEDdnSx6yb1056', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/inputs'}, 'id': 'call_02_StRgnuuxGHpgEoWZZ84G5780', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs'}, 'id': 'call_03_ntqvF9uqtTvJHKGTbuBZ1308', 'type': 'tool_call'}]
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
    17	- `/outputs/working/domain_crosswalk.json`
    18	- `/outputs/working/coverage_ledger.json`
    19	
    20	`clause_index.json` is a source map. It contains source ids and text, but no
    21	final legal status.
    22	
    23	`legal_propositions.json` is the legal evidence ledger. It must contain:
    24	
    25	```json
    26	{
    27	  "matrix": [
    28	    {
    29	      "id": "<matrix number>",
    30	      "source_text": "<matrix enriched/source text>",
    31	      "source_excerpt": "<short quote>",
    32	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    33	      "materiality": "evaluable|not_material|heading|needs_source_review",
    34	      "protected_party": "<party protected by the rule>",
    35	      "bound_party": "<party bound by the rule>",
    36	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    37	      "legal_object": "<regulated object>",
    38	      "trigger": "<event/condition>",
    39	      "deadline": "<deadline if any>",
    40	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    41	      "procedure_channel": "<procedure/channel if any>",
    42	      "liability_remedy": "<liability/remedy if any>",
    43	      "scope_options": ["<scope option>"],
    44	      "consequence": "<legal consequence>",
    45	      "applicability_filters": {}
    46	    }
    47	  ],
    48	  "contract": [
    49	    {
    50	      "id": "<printed contract locator>",
    51	      "source_text": "<contract clause text>",
    52	      "source_excerpt": "<short quote>",
    53	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    54	      "materiality": "evaluable|not_material|heading|needs_source_review",
    55	      "protected_party": "<party protected by the rule>",
    56	      "bound_party": "<party bound by the rule>",
    57	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    58	      "legal_object": "<regulated object>",
    59	      "trigger": "<event/condition>",
    60	      "deadline": "<deadline if any>",
    61	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    62	      "procedure_channel": "<procedure/channel if any>",
    63	      "liability_remedy": "<liability/remedy if any>",
    64	      "scope_options": ["<scope option>"],
    65	      "consequence": "<legal consequence>"
    66	    }
    67	  ]
    68	}
    69	```
    70	
    71	Rows marked `needs_source_review` are not complete. Resolve them before final
    72	status if they can affect a link, missing item, or contract-only finding.
    73	
    74	`domain_crosswalk.json` is the mapping ledger. It must contain domain-level
    75	batches with assigned and processed ids so incompletely processed work cannot
    76	silently become a final answer.
    77	
    78	```json
    79	{
    80	  "domains": [
    81	    {
    82	      "domain": "payment_acceptance_documents",
    83	      "assigned_matrix_ids": ["<matrix id>"],
    84	      "assigned_contract_ids": ["<contract locator>"],
    85	      "processed_matrix_ids": ["<matrix id>"],
    86	      "processed_contract_ids": ["<contract locator>"],
    87	      "candidate_groups": [
    88	        {
    89	          "matrix_ids": ["<matrix id>"],
    90	          "contract_ids": ["<contract locator>"],
    91	          "relationship_candidate": "aligned|deviation|missing_in_contract|extra_in_contract",
    92	          "candidate_strength": "true_analogue|package_analogue|weak_context|none",
    93	          "matrix_evidence": "<short matrix quote>",
    94	          "contract_evidence": "<short contract quote>",
    95	          "reason": "<why this group is or is not a legal analogue>",
    96	          "unresolved": false
    97	        }
    98	      ],
    99	      "provisional_missing_matrix": [
   100	        {
   101	          "matrix_id": "<matrix id>",
   102	          "rejected_candidates": [
   103	            {
   104	              "contract_id": "<contract locator>",
   105	              "reason": "<why weak or legally different>"
   106	            }
   107	          ],
   108	          "source_review_complete": true
   109	        }
   110	      ],
   111	      "provisional_extra_contract": [
   112	        {
   113	          "contract_id": "<contract locator>",
   114	          "materiality_reason": "<independent legal effect>",
   115	          "analogue_search_complete": true
   116	        }
   117	      ],
   118	      "explicitly_skipped_ids": [
   119	        {
   120	          "id": "<matrix or contract id>",
   121	          "side": "matrix|contract",
   122	          "reason": "out_of_scope|not_applicable|heading|not_material"
   123	        }
   124	      ],
   125	      "unresolved_ids": []
   126	    }
   127	  ]
   128	}
   129	```
   130	
   131	Rules:
   132	
   133	- `assigned_matrix_ids` must equal `processed_matrix_ids` plus matrix-side
   134	  `explicitly_skipped_ids` plus `unresolved_ids`.
   135	- `assigned_contract_ids` must equal `processed_contract_ids` plus contract-side
   136	  `explicitly_skipped_ids` plus `unresolved_ids`.
   137	- Final `links` must be traceable to `candidate_groups` with
   138	  `candidate_strength = true_analogue|package_analogue`.
   139	- Final `unmatched_matrix` must be traceable to `provisional_missing_matrix`
   140	  after source review and rejected candidate checks.
   141	- Final `unmatched_contract` must be traceable to `provisional_extra_contract`
   142	  after analogue search and materiality review.
   143	- `weak_context` candidates never become final `links`.
   144	
   145	## Final JSON Shape
   146	
   147	```json
   148	{
   149	  "analysis_profile": {
   150	    "contract_product_profile": {
   151	      "product": ["<selected product/channel>"],
   152	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
   153	      "terminal": ["<selected terminal/payment device>"],
   154	      "payment_method": ["<selected payment method>"],
   155	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
   156	    },
   157	    "source_preflight": {
   158	      "contract_numbering_valid": true,
   159	      "notes": []
   160	    }
   161	  },
   162	  "links": [
   163	    {
   164	      "matrix_ids": ["<matrix id>"],
   165	      "contract_ids": ["<contract locator>"],
   166	      "relationship": "aligned|deviation",
   167	      "legal_topic": "<short legal topic>",
   168	      "matrix_standard": "<bank standard requirement group>",
   169	      "contract_position": "<counterparty contract position group>",
   170	      "matrix_evidence": "<short matrix quote>",
   171	      "contract_evidence": "<short contract quote>",
   172	      "status_reason": "<group-level reason>",
   173	      "risk_level": "none|low|medium|high",
   174	      "discrepancies": [
   175	        {
   176	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   177	          "description": "<material difference>",
   178	          "risk": "<why this matters for the Bank>"
   179	        }
   180	      ]
   181	    }
   182	  ],
   183	  "atomic_links": [
   184	    {
   185	      "matrix_id": "<one matrix id>",
   186	      "contract_id": "<one contract locator>",
   187	      "relationship": "aligned|deviation",
   188	      "link_index": 0,
   189	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   190	      "coverage": "<what this contract locator contributes to the group>"
   191	    }
   192	  ],
   193	  "unmatched_matrix": [
   194	    {
   195	      "matrix_id": "<matrix id>",
   196	      "requirement": "<missing bank standard requirement>",
   197	      "source_evidence": "<short matrix quote>",
   198	      "status": "missing_in_contract",
   199	      "required_type": "mandatory|optional|unknown",
   200	      "applicability": "applicable|conditional|unknown",
   201	      "risk_level": "low|medium|high",
   202	      "risk": "<risk of omission>",
   203	      "rejected_candidates": [
   204	        {
   205	          "contract_id": "<weak candidate considered>",
   206	          "reason": "<why it is not a true analogue>"
   207	        }
   208	      ]
   209	    }
   210	  ],
   211	  "unmatched_contract": [
   212	    {
   213	      "contract_id": "<contract locator>",
   214	      "contract_position": "<extra legally significant contract term>",
   215	      "source_evidence": "<short contract quote>",
   216	      "status": "extra_in_contract",
   217	      "risk_level": "low|medium|high",
   218	      "risk": "<risk or impact for the Bank>",
   219	      "materiality_reason": "<why this has independent legal effect>"
   220	    }
   221	  ],
   222	  "coverage_ledger": {
   223	    "matrix": [
   224	      {
   225	        "matrix_id": "<matrix id>",
   226	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
   227	        "link_indices": [0],
   228	        "reason": "<short closure reason>"
   229	      }
   230	    ],
   231	    "contract": [
   232	      {
   233	        "contract_id": "<contract locator>",
   234	        "closure": "linked|extra_in_contract|not_material",
   235	        "link_indices": [0],
   236	        "reason": "<short closure reason>"
   237	      }
   238	    ]
   239	  },
   240	  "summary": {
   241	    "aligned_count": 0,
   242	    "deviation_count": 0,
   243	    "missing_in_contract_count": 0,
   244	    "extra_in_contract_count": 0
   245	  }
   246	}
   247	```
   248	
   249	## JSON Rules
   250	
   251	- `links` are group-level legal findings. One status applies to the whole
   252	  many-to-many group.
   253	- `atomic_links` are traceability rows only. They inherit the group
   254	  `relationship`; do not invent pair-level final statuses.
   255	- `contract_ids` contain clauses that provide material coverage for the group.
   256	  Background clauses can be cited in reasoning, but should not become final
   257	  candidates unless they affect coverage or status.
   258	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   259	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   260	  matrix closures. Do not use it to invent final conclusions.
   261	- `coverage_ledger.matrix.closure = linked` is valid only when the matrix id
   262	  appears in final `links`.
   263	- `coverage_ledger.contract.closure = linked` is valid only when the contract id
   264	  appears in final `links`.
   265	- `coverage_ledger.contract.closure = not_material` is valid only when the
   266	  contract row has no independent legal effect under the materiality ladder in
   267	  `SKILL.md`.
   268	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   269	  not a risk for the current product, lot, terminal, payment method, or legal
   270	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   271	  final `unmatched_matrix`.
   272	- `unmatched_contract` contains only legally significant `extra_in_contract`
   273	  rows. Non-material rows stay in `coverage_ledger.contract`.
   274	- Do not replace material contract-only child rows with one generic parent. If
   275	  children create independent rights, duties, penalties, procedures, deadlines,
   276	  or consequences, report those child locators.
   277	- `relationship = aligned` requires empty `discrepancies`, `risk_level = none`,
   278	  and text-grounded confirmation that the contract package preserves the matrix
   279	  legal result.
   280	- `relationship = deviation` requires at least one discrepancy with `type`,
   281	  `description`, and `risk`.
   282	- Missing mandatory applicable requirements should normally be `high` risk.
   283	  Missing optional applicable requirements should normally be `low` or
   284	  conditional risk.
   285	- All final ids must be visible in source files. Do not use corrected,
   286	  inferred, translated, parenthetical, or internal ids.
   287	- Weak candidates do not appear in final `links`; use
   288	  `unmatched_matrix[].rejected_candidates`.
   289	
   290	## Excel Output
   291	
   292	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   293	
   294	Sheet 1: `Contract-Matrix`
   295	
   296	Columns:
   297	
   298	1. `contract_id`
   299	2. `contract_summary`
   300	3. `matrix_ids`
   301	4. `status`
   302	5. `risk_level`
   303	6. `comment`
   304	
   305	Rules:
   306	
   307	- one row per group-level contract-to-matrix finding;
   308	- `matrix_ids` contains the full matrix id set for the group;
   309	- status is `aligned`, `deviation`, or `extra_in_contract`;
   310	- contract-only extras have blank `matrix_ids`.
   311	
   312	Sheet 2: `Only in Matrix`
   313	
   314	Columns:
   315	
   316	1. `matrix_id`
   317	2. `requirement`
   318	3. `required_type`
   319	4. `risk_level`
   320	5. `comment`
   321	
   322	Rules:
   323	
   324	- one row per final `unmatched_matrix` item;
   325	- include optional applicable missing as low/conditional risk;
   326	- do not include out-of-scope / not-applicable requirements;
   327	- do not include non-evaluable headings or purely technical rows.
   328	
   329	## Bad Output Patterns
   330	
   331	Do not output:
   332	
   333	- multiple competing final JSON files;
   334	- pair-level final statuses as the primary answer;
   335	- `deviation` for unselected slash alternatives;
   336	- `deviation` for heading/title/label changes alone;
   337	- final `unmatched_contract` rows for definitions without legal effect;
   338	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   339	  requirements;
   340	- final ids that exist only in helper scripts or working ledgers;
   341	- `extra_in_contract` with empty risk;
   342	- `aligned` with non-empty discrepancies;
   343	- `missing_in_contract` where a weak candidate is silently treated as a link;
   344	- `coverage_ledger.matrix.closure = linked` for a matrix id absent from
   345	  `links`;
   346	- `coverage_ledger.contract.closure = linked` for a contract id absent from
   347	  `links`;
   348	- `coverage_ledger.contract.closure = not_material` for a row containing an
   349	  independent right, duty, deadline, penalty, acceptance, refusal, withholding,
   350	  termination, compliance, or evidence procedure;
   351	- a final JSON whose legal mappings first appear only in a helper script rather
   352	  than in `domain_crosswalk.json`;
   353	- final conclusions based only on extracted fields without source-text evidence.
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
   102	Result: `deviation`, usually low risk unless the blank blocks enforcement.
   103	
   104	## 12. Same Deadline
   105	
   106	Matrix requires a document within 3 business days. Contract imposes the same
   107	3-business-day deadline on the same duty.
   108	
   109	Result: deadline element is covered.
   110	
   111	## 13. Changed Or Missing Deadline
   112	
   113	Matrix requires 3 business days. Contract says 5 business days, uses another
   114	period, or states the duty without a deadline.
   115	
   116	Result: `deviation`; discrepancy type `deadline`.
   117	
   118	## 14. Borrowed Hard Term Does Not Cure Gap
   119	
   120	Contract clause A covers the same duty but lacks the matrix deadline. Clause B
   121	has the same number of days but governs a different request or procedure and is
   122	not incorporated into clause A.
   123	
   124	Result: clause B cannot make clause A aligned. Record a deadline deviation.
   125	
   126	## 15. Changed Amount, Formula, Cap, Or Penalty
   127	
   128	Matrix requires a fixed penalty, no cap, full damages, or a specific formula.
   129	Contract lowers the amount, adds a cap, changes the base, or requires an extra
   130	demand.
   131	
   132	Result: `deviation`; discrepancy type `amount` or `liability`.
   133	
   134	## 16. Party Inversion
   135	
   136	Matrix protects the Bank or imposes a duty on the counterparty. Contract gives
   137	the analogous right to the customer or shifts the burden to the Bank.
   138	
   139	Result: `deviation` if it is an analogue; `extra_in_contract` if it creates a
   140	new independent right.
   141	
   142	## 17. Procurement Mechanism As Analogue
   143	
   144	Public-contract acceptance, EIS signing, budget payment, statutory penalties,
   145	or unilateral termination regulates the same legal object as the matrix.
   146	
   147	Result: link it. Use `aligned` if the Bank standard is preserved or stronger.
   148	Do not mark `deviation` merely because the mechanism is 44-FZ/EIS.
   149	
   150	## 18. Procurement Mechanism With Material Deviation
   151	
   152	Public-contract mechanics regulate the same legal object, but the contract
   153	changes a material element: longer payment deadline, weaker withholding right,
   154	different acceptance consequence, penalty cap, lost termination power, or
   155	changed protected party.
   156	
   157	Result: grouped `deviation` with the specific changed element.
   158	
   159	## 19. Procurement Mechanism As Extra
   160	
   161	Contract gives the customer an independent inspection, rejection, correction,
   162	withholding, reporting, or convenience termination right with no matrix
   163	analogue.
   164	
   165	Result: `extra_in_contract` with materiality reason and risk.
   166	
   167	## 20. Formal Label Difference
   168	
   169	The same legal content appears under another appendix title, report label, or
   170	document name.
   171	
   172	Result: `aligned` if rights, duties, timing, evidence, and consequences are
   173	preserved.
   174	
   175	## 21. Low-Risk Note Does Not Force Deviation
   176	
   177	The contract uses another label for the same channel, another party label for
   178	the same legal role, or adds language beneficial to the Bank. The legal result,
   179	timing, enforceability, and protected party are preserved.
   180	
   181	Result: `aligned`. The note can appear in `status_reason`, but it is not a
   182	discrepancy.
   183	
   184	## 22. Named Channel Or Legal Force Missing
   185	
   186	Matrix requires a named EDI/email/site/channel or legal-force effect. Contract
   187	has a generic document exchange clause and omits the named element.
   188	
   189	Result: `deviation` when it is the same exchange mechanism with a missing
   190	material element. If it is only broad-topic context, use `missing_in_contract`.
   191	
   192	## 23. Generic Product Capability
   193	
   194	Contract says a terminal can display QR or accept cards. Matrix requires a
   195	named Bank product or product-specific procedure.
   196	
   197	Result: apply the product profile first. Generic capability is not enough for a
   198	named product obligation.
   199	
   200	## 24. Parent And Child Package Retention
   201	
   202	Parent clause states the operative right or duty. Child clauses enumerate
   203	events, exceptions, deadlines, or remedies. Either parent or child alone would
   204	be incomplete.
   205	
   206	Result: final group includes the material parent and children. Do not drop the
   207	parent only because children contain more detail, and do not drop children when
   208	they carry the hard term.
   209	
   210	## 25. Framework Clause As Analogue
   211	
   212	Contract clause requires compliance with applicable law, payment-system rules,
   213	contract specifications, or incorporated operating procedures. A matrix row
   214	uses that same framework as the legal object or risk-allocation rule.
   215	
   216	Result: include the framework clause as a legal analogue. Do not use it to
   217	inflate unrelated rows where it is only background context.
   218	
   219	## 26. Liability Group Review
   220	
   221	Matrix separates delay penalties, non-delay fines, caps, exceptions, claim
   222	procedure, and damages. Contract distributes the same topics across several
   223	clauses.
   224	
   225	Result: compare the liability package as a group. Before `aligned`, verify
   226	amounts, formulas, caps, triggers, protected party, and excluded buckets.
   227	
   228	## 27. Definition Without Legal Effect
   229	
   230	Definition has no analogue in the matrix and creates no standalone right, duty,
   231	risk, amount, procedure, liability, or consequence.
   232	
   233	Result: `not_material` in the working ledger only.
   234	
   235	## 28. Definition With Legal Effect
   236	
   237	Definition expands a key term so that it changes scope, liability, covered
   238	transactions, parties, or remedies.
   239	
   240	Result: evaluable. Link it if it modifies a matrix analogue; otherwise classify
   241	as `extra_in_contract`.
   242	
   243	## 29. Contract-Only Material Clause
   244	
   245	Contract adds maximum price, budget source, customer control, acceptance,
   246	withholding, unilateral refusal, penalty cap, reporting, anti-corruption,
   247	confidentiality, audit, data, or evidence procedure with no matrix analogue.
   248	
   249	Result: `extra_in_contract`.
   250	
   251	## 30. Duplicate Gap Propagation
   252	
   253	One payment deadline gap affects a payment package with parent and child
   254	clauses.
   255	
   256	Result: record one grouped `deviation`. Do not duplicate the same gap across
   257	unrelated companion clauses.
   258	
   259	## 31. Non-Informative Parent
   260	
   261	A parent row merely names a section and all legal effect is in children.
   262	
   263	Result: close as non-evaluable or `not_material` in the ledger. Do not report
   264	it as a final risk.
   265	
   266	## 32. Group-Level Status
   267	
   268	A group contains several matrix ids and several contract ids. One status
   269	applies to the group as a whole.
   270	
   271	Result: do not assign separate final statuses per pair. `atomic_links` are only
   272	traceability rows and inherit the group relationship.
   273	
   274	## 33. Contract Row Preservation
   275	
   276	A contract child clause contains the operative duty and a parent clause only
   277	introduces the section. The child is a true analogue to a matrix requirement.
   278	
   279	Result: keep the child `contract_id` in final `links`. Do not replace it with
   280	the parent merely because the parent has broader topic language.
   281	
   282	## 34. Parent And Child Both Material
   283	
   284	A parent clause creates a general inspection right. Several children define
   285	deadlines, refusal consequences, correction rights, and expert review.
   286	
   287	Result: if the parent and children each add legal effect, keep all material
   288	locators in the package. If no matrix analogue exists, report the material
   289	children as `extra_in_contract` rather than collapsing them into one parent.
   290	
   291	## 35. Appendix Or Table As Analogue
   292	
   293	The main contract body incorporates an appendix with terminal addresses,
   294	service locations, tariffs, document forms, or technical-product scope. Matrix
   295	requirements regulate the same service or scope.
   296	
   297	Result: the appendix/table row can be a legal analogue or package member. Do
   298	not classify it as technical unless it has no legal effect.
   299	
   300	## 36. Large Clause With Many Analogues
   301	
   302	One long contract clause contains several independent duties: confidentiality,
   303	documents, authorization, reporting, payment evidence, and liability. The
   304	matrix splits those duties into many rows.
   305	
   306	Result: include all legally corresponding matrix ids in the group. Do not stop
   307	after the first obvious analogue.
   308	
   309	## 37. No Silent Matrix Closure
   310	
   311	A matrix requirement is applicable and evaluable. The contract has only a
   312	generic clause on the same broad topic, but not the same legal object,
   313	protected party, trigger, or consequence.
   314	
   315	Result: reject the generic clause as weak context and put the matrix id in
   316	`unmatched_matrix`. Do not mark it as linked in `coverage_ledger`.
   317	
   318	## 38. Provisional Missing Rescue
   319	
   320	A matrix item is about a specific Bank right. Initial search finds no analogue.
   321	Before final missing, source review finds a sibling contract clause and an
   322	appendix row that together create the same right.
   323	
   324	Result: rescue the item from missing and create a package link. If source
   325	review still finds only broad context, keep `missing_in_contract`.
   326	
   327	## 39. Contract-Only Child With Independent Effect
   328	
   329	A contract child clause gives the customer a right to reject services, demand
   330	correction, withhold payment, conduct expert review, impose a penalty, or
   331	terminate unilaterally. No matrix analogue exists.
   332	
   333	Result: `extra_in_contract`. Do not close it as `not_material` merely because
   334	the parent section already appears in the ledger.
   335	
   336	## 40. Contract-Only Parent Without Independent Effect
   337	
   338	A parent row only says "Liability of the parties" or "Acceptance procedure" and
   339	all operative rights, duties, amounts, deadlines, and consequences are in
   340	children.
   341	
   342	Result: the parent can be `not_material` in the coverage ledger. Report the
   343	children if they create independent legal effects.
   344	
   345	## 41. Procurement Clause As Analogue Before Extra
   346	
   347	A public-procurement clause sets acceptance, payment, penalties, or termination
   348	for the same legal object as a matrix row.
   349	
   350	Result: first test it as a matrix analogue. Classify as `extra_in_contract`
   351	only if no matrix analogue exists and the clause adds an independent right,
   352	restriction, procedure, or consequence.
   353	
   354	## 42. Domain Crosswalk Completeness
   355	
   356	A worker receives five matrix ids and twenty contract ids in a legal domain.
   357	It finds links for three matrix ids, rejects candidates for one, and marks one
   358	out of scope. It also reviews all twenty contract ids as linked, extra, or
   359	not material.
   360	
   361	Result: the domain is complete only if `processed_*` plus explicit skips cover
   362	the assigned ids and `unresolved_ids` is empty. Incomplete batches must not be
   363	merged into the final answer.
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/outputs/working/']
AI: Now let me read the input files and check what's already in the working directory.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_lwOKYgT8cjiO4x0NPc1k7203', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_R1jOfGF39apFrEurFeYZ3209', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_02_AryzvW4pn09wb9xeExgV2045', 'type': 'tool_call'}]
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
Tool: ['/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/legal_propositions.json']
AI: Let me continue reading the contract and matrix files, and also check the existing working artifacts.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_MG6G2xw3EzOZjoNKrAR11687', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 200}, 'id': 'call_01_jGhrAOob3x39MELvtwiP9512', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 200}, 'id': 'call_02_rNj0clVBhlGWlzdzM64F5570', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_03_YBZYBNuuNxXt7E5NglLC7966', 'type': 'tool_call'}]
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
Tool:      1	{
     2	  "matrix_items": [
     3	    {
     4	      "id": "2.1",
     5	      "number": "2.1",
     6	      "source_index": 0,
     7	      "type": "operative",
     8	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений\nДля регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества\nВ целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     9	      "main_idea": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
    10	      "topics": [
    11	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    12	        "Банк может отказать в регистрации ТСТ без указания причины",
    13	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    14	        "Информация о новых устройствах предоставляется с указанием их количества"
    15	      ],
    16	      "enriched_text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора.\nПри изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
    17	      "applicability": {
    18	        "required_type": "mandatory",
    19	        "only_for_product": "common",
    20	        "only_for_lot": "common",
    21	        "only_for_terminal": "common",
    22	        "payment_method": "common"
    23	      }
    24	    },
    25	    {
    26	      "id": "2.2",
    27	      "number": "2.2",
    28	      "source_index": 1,
    29	      "type": "operative",
    30	      "source_text": "Важен факт, что валюта рубль РФ, другая валюта недопустима\nРасчёты производятся в рублях Российской Федерации\nРасчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    31	      "main_idea": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    32	      "topics": [
    33	        "Расчёты производятся в рублях Российской Федерации"
    34	      ],
    35	      "enriched_text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. ",
    36	      "applicability": {
    37	        "required_type": "mandatory",
    38	        "only_for_product": "common",
    39	        "only_for_lot": "common",
    40	        "only_for_terminal": "common",
    41	        "payment_method": "common"
    42	      }
    43	    },
    44	    {
    45	      "id": "2.3.1",
    46	      "number": "2.3.1",
    47	      "source_index": 2,
    48	      "type": "operative",
    49	      "source_text": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.\nОбмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту; Информация и документы, направленные по электронной почте, имеют юридическую силу\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    50	      "main_idea": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    51	      "topics": [
    52	        "Обмен информацией по электронной почте",
    53	        "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
    54	        "Информация и документы, направленные по электронной почте, имеют юридическую силу"
    55	      ],
    56	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    57	      "applicability": {
    58	        "required_type": "mandatory",
    59	        "only_for_product": "common",
    60	        "only_for_lot": "common",
    61	        "only_for_terminal": "common",
    62	        "payment_method": "common"
    63	      }
    64	    },
    65	    {
    66	      "id": "2.3.2",
    67	      "number": "2.3.2",
    68	      "source_index": 3,
    69	      "type": "operative",
    70	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом\nОбмен документами посредством системы ДБО или аналогичных систем Банка\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
    71	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    72	      "topics": [
    73	        "Обмен документами посредством системы ДБО или аналогичных систем Банка"
    74	      ],
    75	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
    76	      "applicability": {
    77	        "required_type": "mandatory",
    78	        "only_for_product": "common",
    79	        "only_for_lot": "common",
    80	        "only_for_terminal": "common",
    81	        "payment_method": "common"
    82	      }
    83	    },
    84	    {
    85	      "id": "2.3.3",
    86	      "number": "2.3.3",
    87	      "source_index": 4,
    88	      "type": "operative",
    89	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом\nОбмен документами с доставкой нарочным или курьером\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
    90	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    91	      "topics": [
    92	        "Обмен документами с доставкой нарочным или курьером"
    93	      ],
    94	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
    95	      "applicability": {
    96	        "required_type": "optional",
    97	        "only_for_product": "common",
    98	        "only_for_lot": "common",
    99	        "only_for_terminal": "common",
   100	        "payment_method": "common"
   101	      }
   102	    },
   103	    {
   104	      "id": "2.3.4",
   105	      "number": "2.3.4",
   106	      "source_index": 5,
   107	      "type": "operative",
   108	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом\nОбмен документами через заказное письмо\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   109	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   110	      "topics": [
   111	        "Обмен документами через заказное письмо"
   112	      ],
   113	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   114	      "applicability": {
   115	        "required_type": "optional",
   116	        "only_for_product": "common",
   117	        "only_for_lot": "common",
   118	        "only_for_terminal": "common",
   119	        "payment_method": "common"
   120	      }
   121	    },
   122	    {
   123	      "id": "2.3.5",
   124	      "number": "2.3.5",
   125	      "source_index": 6,
   126	      "type": "operative",
   127	      "source_text": "Важна равнозначность документов\nОбмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП; электронные документы имеют юридическую силу документов на бумаге\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   128	      "main_idea": "Важна равнозначность документов",
   129	      "topics": [
   130	        "Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП",
   131	        "электронные документы имеют юридическую силу документов на бумаге"
   132	      ],
   133	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью   (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   134	      "applicability": {
   135	        "required_type": "mandatory",
   136	        "only_for_product": "common",
   137	        "only_for_lot": "common",
   138	        "only_for_terminal": "common",
   139	        "payment_method": "common"
   140	      }
   141	    },
   142	    {
   143	      "id": "2.3.6",
   144	      "number": "2.3.6",
   145	      "source_index": 7,
   146	      "type": "operative",
   147	      "source_text": "Важен сам факт наличия данного канала для обмена электронными документами\nПеречисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок); Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП)\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   148	      "main_idea": "Важен сам факт наличия данного канала для обмена электронными документами",
   149	      "topics": [
   150	        "Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок)",
   151	        "Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП)"
   152	      ],
   153	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   154	      "applicability": {
   155	        "required_type": "mandatory",
   156	        "only_for_product": "common",
   157	        "only_for_lot": "fz_44",
   158	        "only_for_terminal": "common",
   159	        "payment_method": "common"
   160	      }
   161	    },
   162	    {
   163	      "id": "2.3.7",
   164	      "number": "2.3.7",
   165	      "source_index": 8,
   166	      "type": "operative",
   167	      "source_text": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию\nОбмен информацией через обращение в службу поддержки Банка; Дата с которой сторона считается получившей информацию в случае её направления на электронную почту; Дата с которой сторона считается получившей информацию в случае запроса в ДБО; Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма; Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»; Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС\nБанк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в: • п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно; • п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма); • п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции; • п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке; • п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   168	      "main_idea": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию",
   169	      "topics": [
   170	        "Обмен информацией через обращение в службу поддержки Банка",
   171	        "Дата с которой сторона считается получившей информацию в случае её направления на электронную почту",
   172	        "Дата с которой сторона считается получившей информацию в случае запроса в ДБО",
   173	        "Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма",
   174	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»",
   175	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС"
   176	      ],
   177	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в:\n• п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;\n• п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма);\n• п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;\n•  п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке;\n• п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   178	      "applicability": {
   179	        "required_type": "optional",
   180	        "only_for_product": "common",
   181	        "only_for_lot": "common",
   182	        "only_for_terminal": "common",
   183	        "payment_method": "common"
   184	      }
   185	    },
   186	    {
   187	      "id": "2.4",
   188	      "number": "2.4",
   189	      "source_index": 9,
   190	      "type": "operative",
   191	      "source_text": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью\nДокументы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   192	      "main_idea": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   193	      "topics": [],
   194	      "enriched_text": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   195	      "applicability": {
   196	        "required_type": "optional",
   197	        "only_for_product": "common",
   198	        "only_for_lot": "common",
   199	        "only_for_terminal": "common",
   200	        "payment_method": "common"
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos"],
     5	  "payment_method": ["cards", "qr"],
     6	  "legal_regime": "44_fz",
     7	  "notes": "Contract is a 44-FZ public procurement for trade acquiring services with POS terminals (Электронные терминалы) and QR-code capability. No internet acquiring, no smart terminals, no SberPay, no biometrics. Payment cards: MIR, VISA, MasterCard. Terminal type: POS terminals (Электронные терминалы), not Smart terminals."
     8	}
AI: Now let me read the legal propositions file and the rest of the matrix and contract to understand the full scope.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 200}, 'id': 'call_00_O98XOPkLVVait6DqYe4H9611', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 400, 'limit': 300}, 'id': 'call_01_TISkDfeozVr1SPtBBrHs9194', 'type': 'tool_call'}]
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предостав",
     7	      "type": "operative",
     8	      "materiality": "needs_source_review",
     9	      "protected_party": "",
    10	      "bound_party": "",
    11	      "right_or_obligation": "",
    12	      "legal_object": "",
    13	      "trigger": "",
    14	      "deadline": "",
    15	      "amount_formula_cap": "",
    16	      "procedure_channel": "",
    17	      "liability_remedy": "",
    18	      "scope_options": [],
    19	      "consequence": "",
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
    41	      "materiality": "needs_source_review",
    42	      "protected_party": "",
    43	      "bound_party": "",
    44	      "right_or_obligation": "",
    45	      "legal_object": "",
    46	      "trigger": "",
    47	      "deadline": "",
    48	      "amount_formula_cap": "",
    49	      "procedure_channel": "",
    50	      "liability_remedy": "",
    51	      "scope_options": [],
    52	      "consequence": "",
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
    71	      "materiality": "needs_source_review",
    72	      "protected_party": "",
    73	      "bound_party": "",
    74	      "right_or_obligation": "",
    75	      "legal_object": "",
    76	      "trigger": "",
    77	      "deadline": "",
    78	      "amount_formula_cap": "",
    79	      "procedure_channel": "",
    80	      "liability_remedy": "",
    81	      "scope_options": [],
    82	      "consequence": "",
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
   103	      "materiality": "needs_source_review",
   104	      "protected_party": "",
   105	      "bound_party": "",
   106	      "right_or_obligation": "",
   107	      "legal_object": "",
   108	      "trigger": "",
   109	      "deadline": "",
   110	      "amount_formula_cap": "",
   111	      "procedure_channel": "",
   112	      "liability_remedy": "",
   113	      "scope_options": [],
   114	      "consequence": "",
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
   133	      "materiality": "needs_source_review",
   134	      "protected_party": "",
   135	      "bound_party": "",
   136	      "right_or_obligation": "",
   137	      "legal_object": "",
   138	      "trigger": "",
   139	      "deadline": "",
   140	      "amount_formula_cap": "",
   141	      "procedure_channel": "",
   142	      "liability_remedy": "",
   143	      "scope_options": [],
   144	      "consequence": "",
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
   163	      "materiality": "needs_source_review",
   164	      "protected_party": "",
   165	      "bound_party": "",
   166	      "right_or_obligation": "",
   167	      "legal_object": "",
   168	      "trigger": "",
   169	      "deadline": "",
   170	      "amount_formula_cap": "",
   171	      "procedure_channel": "",
   172	      "liability_remedy": "",
   173	      "scope_options": [],
   174	      "consequence": "",
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
   193	      "materiality": "needs_source_review",
   194	      "protected_party": "",
   195	      "bound_party": "",
   196	      "right_or_obligation": "",
   197	      "legal_object": "",
   198	      "trigger": "",
   199	      "deadline": "",
   200	      "amount_formula_cap": "",
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
   601	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней с даты получения соответствующего запроса, Предприятие обязуется предоставить подтверждение правомерности передачи ПДн. В случае если Предприятие не предоставит подтверждение наличия таких оснований, оно обязуется за свой счет урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные Банку, а также возместить любые убытки и расходы, понесенные Банком в результате не предоставления таких доказательств.",
   602	  "required_type":"mandatory",
   603	  "main_idea":"Важно, что данный пункт относится только к данным по всем сотрудникам. Важен срок предоставления подтверждения",
   604	  "only_for_product":"common",
   605	  "only_for_lot":"common",
   606	  "only_for_terminal":"common",
   607	  "topics":[
   608	   "Предприятие обязано предоставлять подтверждение согласий на обработку персональных данных сотрудников (включая руководителя) по письменному запросу банка",
   609	   "Сроки предоставления подтверждения согласия руководителя",
   610	   "В случае отсутствия подтверждения Предприятие урегулирует претензии третьих лиц за свой счет",
   611	   "Предприятие возмещает Банку убытки и расходы при непредставлении обоснования передачи персональных данных"
   612	  ],
   613	  "payment_method":"common"
   614	 },
   615	 {
   616	  "number":"4.2.17",
   617	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Обеспечить соблюдение требований Стандарта PCI DSS, размещенного на сайте в сети интернет: https:\/\/www.pcisecuritystandards.org и предоставлять по запросу Банка результаты проведения оценки соответствия в виде аттестата соответствия или листа самооценки на электронный адрес: pcidss@sberbank.ru. ",
   618	  "required_type":"mandatory",
   619	  "main_idea":"Важен сам факт обязанности соблюдения стандарта, а так же факт обязанности предоставления подтверждения",
   620	  "only_for_product":"internet_acquiring",
   621	  "only_for_lot":"common",
   622	  "only_for_terminal":"common",
   623	  "topics":[
   624	   "Обязательство соблюдать требования PCI DSS",
   625	   "Предоставление аттестата соответствия или листа самооценки по запросу банка",
   626	   "Указанный email для отправки документов:pcidss@sberbank.ru"
   627	  ],
   628	  "payment_method":"common"
   629	 },
   630	 {
   631	  "number":"4.2.18",
   632	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → С даты расторжения Договора прекратить прием к оплате Карт, снять\/удалить информационные материалы, извещающие об обслуживании Карт. ",
   633	  "required_type":"mandatory",
   634	  "main_idea":"Важны факты прекращения приема к оплате Карт, снятия информационных материалов, а так же важен срок",
   635	  "only_for_product":"common",
   636	  "only_for_lot":"common",
   637	  "only_for_terminal":"common",
   638	  "topics":[
   639	   "При расторжении договора прекращение приема карт к оплате (регулируется дата прекращения)",
   640	   "При расторжении договора снятие информационных материалов о приеме карт (регулируется дата снятия)"
   641	  ],
   642	  "payment_method":"common"
   643	 },
   644	 {
   645	  "number":"4.2.19",
   646	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не принимать мер противодействия Банку в проведении проверки Предприятия\/ТСТ \/ Ресурса  на предмет выявления мошеннических Операций и\/или предоставления Покупателям Товаров\/услуг, не соответствующих роду деятельности Предприятия\/ТСТ, а также оказывать содействие Банку в проведении разбирательства по факту совершения подозрительных Операций.",
   647	  "required_type":"mandatory",
   648	  "main_idea":"Важен, факт что Предприятие не должно мешать Банку, и факт, что Предприятие должно помогать Банку в расследовании",
   649	  "only_for_product":"common",
   650	  "only_for_lot":"common",
   651	  "only_for_terminal":"common",
   652	  "topics":[
   653	   "Предприятие обязано не препятствовать проверке со стороны Банка",
   654	   "Предприятие обязано содействовать расследованию подозрительных операций"
   655	  ],
   656	  "payment_method":"common"
   657	 },
   658	 {
   659	  "number":"4.2.20.1",
   660	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: https:\/\/www.sberbank.ru\/help\/business\/acquiring.",
   661	  "required_type":"mandatory",
   662	  "main_idea":"Важен сам факт, что Предприятие само следит за прохождением инструктажа сотрудниками, размещенного на сайте Банка",
   663	  "only_for_product":"trade_acquiring",
   664	  "only_for_lot":"common",
   665	  "only_for_terminal":"common",
   666	  "topics":[
   667	   "обязательство предприятия проводить инструктаж сотрудников самостоятельно",
   668	   "ссылка на инструкцию о порядке проведения Операций"
   669	  ],
   670	  "payment_method":"common"
   671	 },
   672	 {
   673	  "number":"4.2.20.2",
   674	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → Использовать Электронные терминалы (в том числе технологические sim-карты)\/Смарт-терминалы и программное обеспечение, предоставленное Банком, только для целей реализации настоящего Договора и на территории регистрации ТСТ\/фактической установки Электронного терминала\/Смарт-терминала. Не вносить изменения в программное обеспечение и Электронные терминалы\/Смарт-терминалы, предоставленные Банком. Не осуществлять самостоятельно ремонт Электронных терминалов\/Смарт-терминалов Банка. Не передавать третьим лицам Электронные терминалы\/Смарт-терминалы Банка, Документы по операциям и инструктивные материалы, предоставленные Банком, за исключением работников Обслуживающей компании.",
   675	  "required_type":"mandatory",
   676	  "main_idea":"Важно, чтобы предприятие использовало терминалы и ПО Банка только для целей договора и по месту установки, не менять и не ремонтировать их самостоятельно и не передавать третьим лицам (кроме обслуживающей компании)",
   677	  "only_for_product":"trade_acquiring",
   678	  "only_for_lot":"common",
   679	  "only_for_terminal":"common",
   680	  "topics":[
   681	   "использование Электронных терминалов и программного обеспечения только для целей договора и на территории регистрации ТСТ\/установки устройства",
   682	   "запрет внесения изменений в ПО и оборудование",
   683	   "запрет самостоятельного ремонта оборудования",
   684	   "запрет передачи оборудования и документов третьим лицам, кроме сотрудников обслуживающей компании"
   685	  ],
   686	  "payment_method":"common"
   687	 },
   688	 {
   689	  "number":"4.2.20.3",
   690	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов\/Смарт-терминалов для проведения работ по их подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке.",
   691	  "required_type":"mandatory",
   692	  "main_idea":"Важно, что если в договоре стоит запрет на предоставление доступа третьим лицам, то это разногласие",
   693	  "only_for_product":"trade_acquiring",
   694	  "only_for_lot":"common",
   695	  "only_for_terminal":"common",
   696	  "topics":[
   697	   "Предоставление доступа третьим лицам к местам установки терминалов",
   698	   "Доступ для подключения терминалов",
   699	   "Доступ для настройки терминалов",
   700	   "Доступ для ремонта терминалов",
AI: I now have a good understanding of the data. Let me continue reading the rest of the matrix and the legal propositions to understand the full scope, then focus on my task: identifying material contract-only terms.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 700, 'limit': 500}, 'id': 'call_00_cgqjRnQzrZSJGSWjXdGD8123', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 200, 'limit': 500}, 'id': 'call_01_U5V6L2RAAI3a6eDo8MI10330', 'type': 'tool_call'}]
Tool:    701	   "Доступ для замены терминалов",
   702	   "Доступ для технического обслуживания терминалов",
   703	   "Доступ для визуальной проверки терминалов"
   704	  ],
   705	  "payment_method":"common"
   706	 },
   707	 {
   708	  "number":"4.2.20.4",
   709	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → Принять Электронные терминалы\/Смарт-терминалы Банка и\/или программное обеспечение для Смарт-терминалов Предприятия по акту принятия оказанных услуг по форме Обслуживающей компании, составленному в 2-х (два) экземплярах, подписанных уполномоченными работниками Обслуживающей компании и Предприятия. Один экземпляр акта находится на хранении в Обслуживающей компании, второй – у Предприятия. Форма акта размещена на Официальном сайте Банка.",
   710	  "required_type":"mandatory",
   711	  "main_idea":"Важно, если указано, что оборудование Предприятие без документов или акта передачи, то всё ок, разногласия нет",
   712	  "only_for_product":"trade_acquiring",
   713	  "only_for_lot":"common",
   714	  "only_for_terminal":"common",
   715	  "topics":[
   716	   "Предприятие обязано принять Электронные терминалы \/ Смарт-терминалв по акту",
   717	   "подписание акта уполномоченными лицами",
   718	   "наличие двух экземпляров акта",
   719	   "хранение одного экземпляра акта в Обслуживающей компании",
   720	   "хранение второго экземпляра акта у Предприятия"
   721	  ],
   722	  "payment_method":"common"
   723	 },
   724	 {
   725	  "number":"4.2.20.5",
   726	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → В случае выхода Электронного терминала\/Смарт-терминала, в том числе Мобильного устройства Предприятия, из строя или его утраты немедленно информировать об этом Банк в соответствии с п. 2.3.1, п. 2.3.2 Договора или путем обращения в службу поддержки Банка по телефону, указанному в п. 2 Порядка проведения операций в Торгово-сервисных точках\/на Ресурсе.\n",
   727	  "required_type":"mandatory",
   728	  "main_idea":"",
   729	  "only_for_product":"trade_acquiring",
   730	  "only_for_lot":"common",
   731	  "only_for_terminal":"common",
   732	  "topics":[
   733	   "Предприятие обязано немедленно информировать Банк о выходе из строя или утрате Электронного терминала\/Смарт-терминала или Мобильного устройства",
   734	   "Информирование осуществляется согласно пунктам 2.3.1 и 2.3.2 Договора или через службу поддержки Банка"
   735	  ],
   736	  "payment_method":"common"
   737	 },
   738	 {
   739	  "number":"4.2.20.6",
   740	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → Вернуть Банку или Обслуживающей компании Электронные терминалы\/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Договора или с даты получения письменного\/устного требования Банка о возврате Электронных терминалов\/Смарт-терминалов Банка.",
   741	  "required_type":"mandatory",
   742	  "main_idea":"",
   743	  "only_for_product":"trade_acquiring",
   744	  "only_for_lot":"common",
   745	  "only_for_terminal":"common",
   746	  "topics":[
   747	   "вернуть терминал в течение 5 рабочих дней после расторжения договора",
   748	   "вернуть терминал после получения письменного\/устного требования банка"
   749	  ],
   750	  "payment_method":"common"
   751	 },
   752	 {
   753	  "number":"4.2.20.7",
   754	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии\/в ТСТ (Торговый эквайринг): → В случае невозврата Электронных терминалов \/Смарт-терминалов Банка в соответствии с п. 4.2.20.6 Договора, уплатить Банку штраф в размере 25 000 (двадцать пять тысяч) рублей, в том числе НДС, за каждый Электронный терминал и 25 000 (двадцать пять тысяч) рублей, в том числе НДС за каждый Смарт-терминал Банка.",
   755	  "required_type":"mandatory",
   756	  "main_idea":"Важно, чтобы в соответствующем пункте договора шла речь про штраф за невозврат терминала и его размер, иначе данный пункт матрицы не относится к пункту договора",
   757	  "only_for_product":"trade_acquiring",
   758	  "only_for_lot":"common",
   759	  "only_for_terminal":"common",
   760	  "topics":[
   761	   "Невозврат терминалов. Обязанность предприятия об уплате штрафа за невозврат"
   762	  ],
   763	  "payment_method":"common"
   764	 },
   765	 {
   766	  "number":"4.2.21.1",
   767	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Приступить к проведению Операций на Ресурсе только после успешного завершения проверки выбранных Предприятием\/ТСТ Операций на тестовой среде.",
   768	  "required_type":"mandatory",
   769	  "main_idea":"",
   770	  "only_for_product":"internet_acquiring",
   771	  "only_for_lot":"common",
   772	  "only_for_terminal":"common",
   773	  "topics":[
   774	   "Приступить к проведению операций на ресурсе только после успешного завершения проверки операций на тестовой среде"
   775	  ],
   776	  "payment_method":"common"
   777	 },
   778	 {
   779	  "number":"4.2.21.2",
   780	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соответствовать Требованиям Банка к Ресурсу Предприятия, размещенным на Официальном сайте Банка.",
   781	  "required_type":"mandatory",
   782	  "main_idea":"",
   783	  "only_for_product":"internet_acquiring",
   784	  "only_for_lot":"common",
   785	  "only_for_terminal":"common",
   786	  "topics":[
   787	   "Предприятие обязано соответствовать Требованиям Банка к Ресурсу, размещенным на Официальном сайте Банка"
   788	  ],
   789	  "payment_method":"common"
   790	 },
   791	 {
   792	  "number":"4.2.21.3",
   793	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Подтверждать авторизованные с использованием Предавторизации суммы к списанию через СПЭП не позднее 5 (пяти) календарных дней с даты совершения Операции на сумму фактически оказанных Товаров\/услуг, в соответствии с Порядком проведения операций в Торгово-сервисных точках\/на Ресурсе.",
   794	  "required_type":"mandatory",
   795	  "main_idea":"",
   796	  "only_for_product":"internet_acquiring",
   797	  "only_for_lot":"common",
   798	  "only_for_terminal":"common",
   799	  "topics":[
   800	   "Подтверждение сумм к списанию не позднее 5 календарных дней",
   801	   "Соответствие подтвержденной суммы фактически оказанным товарам\/услугам",
   802	   "Соблюдение Порядка проведения операций на Ресурсе"
   803	  ],
   804	  "payment_method":"common"
   805	 },
   806	 {
   807	  "number":"4.2.21.4",
   808	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Согласовывать с Банком дизайн Платежной страницы, включая электронные варианты информационных наклеек.\n",
   809	  "required_type":"mandatory",
   810	  "main_idea":"",
   811	  "only_for_product":"internet_acquiring",
   812	  "only_for_lot":"common",
   813	  "only_for_terminal":"common",
   814	  "topics":[
   815	   "Согласование дизайна Платежной страницы с Банком",
   816	   "Согласование электронных вариантов информационных наклеек с Банком"
   817	  ],
   818	  "payment_method":"common"
   819	 },
   820	 {
   821	  "number":"4.2.21.5",
   822	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Провести мероприятия по интеграции Ресурса со СПЭП и соответствующие интеграционные тесты в течение 30 (тридцати) календарных дней с даты заключения Договора.",
   823	  "required_type":"mandatory",
   824	  "main_idea":"",
   825	  "only_for_product":"internet_acquiring",
   826	  "only_for_lot":"common",
   827	  "only_for_terminal":"common",
   828	  "topics":[
   829	   "Предприятие проводит интеграцию Ресурса со СПЭП в течение 30 календарных дней с даты заключения Договора",
   830	   "Предприятие проводит интеграционные тесты в течение 30 календарных дней с даты заключения Договора"
   831	  ],
   832	  "payment_method":"common"
   833	 },
   834	 {
   835	  "number":"4.2.21.6",
   836	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Самостоятельно обеспечивать безопасность своих информационных ресурсов в сети интернет.",
   837	  "required_type":"mandatory",
   838	  "main_idea":"",
   839	  "only_for_product":"internet_acquiring",
   840	  "only_for_lot":"common",
   841	  "only_for_terminal":"common",
   842	  "topics":[
   843	   "Самостоятельное обеспечение безопасности информационных ресурсов в сети интернет"
   844	  ],
   845	  "payment_method":"common"
   846	 },
   847	 {
   848	  "number":"4.2.21.7",
   849	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Предоставлять по требованию Банка доступ к разделам Ресурса с ограниченным доступом, не связанным с администрированием и сопровождением (VIP, Оптовое, Клубное обслуживание, и т.п.).",
   850	  "required_type":"mandatory",
   851	  "main_idea":"",
   852	  "only_for_product":"internet_acquiring",
   853	  "only_for_lot":"common",
   854	  "only_for_terminal":"common",
   855	  "topics":[
   856	   "Предоставление доступа к разделам Ресурса с ограниченным доступом по требованию Банка"
   857	  ],
   858	  "payment_method":"common"
   859	 },
   860	 {
   861	  "number":"4.2.21.8",
   862	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соблюдать правила пользования Личным кабинетом Интернет-эквайринга, размещенным на Официальном сайте Банка.",
   863	  "required_type":"mandatory",
   864	  "main_idea":"",
   865	  "only_for_product":"internet_acquiring",
   866	  "only_for_lot":"common",
   867	  "only_for_terminal":"common",
   868	  "topics":[
   869	   "Соблюдение правил пользования Личным кабинетом Интернет-эквайринга"
   870	  ],
   871	  "payment_method":"common"
   872	 },
   873	 {
   874	  "number":"4.2.22",
   875	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставить Покупателю для считывания QR-код с целью осуществления оплаты Товаров\/услуг с использованием SberPayQR\/Плати QR",
   876	  "required_type":"optional",
   877	  "main_idea":"Важно, чтобы в пункте было прямо указано, что он про QR-код",
   878	  "only_for_product":"trade_acquiring",
   879	  "only_for_lot":"common",
   880	  "only_for_terminal":"common",
   881	  "topics":[
   882	   "Предприятие обязуется предоставлять QR-код для использования SberPayQR\/Плати QR (должна быть прямая отсылка к QR-коду)"
   883	  ],
   884	  "payment_method":"qr"
   885	 },
   886	 {
   887	  "number":"4.2.23",
   888	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не изменять QR-код партнера в одностороннем порядке.",
   889	  "required_type":"optional",
   890	  "main_idea":"Важно, чтобы в пункте было прямо указано, что он про QR-код",
   891	  "only_for_product":"trade_acquiring",
   892	  "only_for_lot":"common",
   893	  "only_for_terminal":"common",
   894	  "topics":[
   895	   "Предприятие обязуется не изменять QR-код партнера в одностороннем порядке (должна быть прямая отсылка к QR-коду)"
   896	  ],
   897	  "payment_method":"qr"
   898	 },
   899	 {
   900	  "number":"4.2.24",
   901	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Использовать API и сведения, передаваемые посредством QR-API, в границах прав и функциональных возможностей такого API и его описания, изложенного в Порядке, условиях и ответственности сторон при подключении QR-API, размещенном на Официальном сайте Банка.",
   902	  "required_type":"optional",
   903	  "main_idea":"Важно, чтобы в пункте было прямо указано, что он про QR-API",
   904	  "only_for_product":"common",
   905	  "only_for_lot":"common",
   906	  "only_for_terminal":"common",
   907	  "topics":[
   908	   "использование API в рамках функциональных возможностей (должна быть прямая отсылка к QR-API)",
   909	   "соблюдение порядка использования QR-API (должна быть прямая отсылка к QR-API)",
   910	   "учет условий и ответственности сторон при использовании QR-API (должна быть прямая отсылка к QR-API)"
   911	  ],
   912	  "payment_method":"qr"
   913	 },
   914	 {
   915	  "number":"4.2.25",
   916	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При выявлении фактов или признаков нарушения безопасности использования QR-API и функциональных возможностей организации информационно-технологического взаимодействия немедленно приостановить использование API и оповестить об этом Банк любым из способов, указанных в п.2.3.1. – п.2.3.4. Договора.",
   917	  "required_type":"optional",
   918	  "main_idea":"Важно, чтобы в пункте было прямо указано, что он про QR-API",
   919	  "only_for_product":"common",
   920	  "only_for_lot":"common",
   921	  "only_for_terminal":"common",
   922	  "topics":[
   923	   "При выявлении нарушения безопасности использования QR-API - приостановить использование API (должна быть прямая отсылка к QR-API)",
   924	   "При выявлении нарушения безопасности использования QR-API оповестить Банка (должна быть прямая отсылка к QR-API)"
   925	  ],
   926	  "payment_method":"qr"
   927	 },
   928	 {
   929	  "number":"4.2.26",
   930	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В дополнение к соблюдению требований, указанных в Условиях, в том числе приложениях к Условиям, в целях осуществлении Повторяющихся платежей Предприятие обязано:\n• размещать на Ресурсе пользовательское соглашение\/оферту Предприятия, содержащее условия проведения Повторяющихся платежей (в случае их применения), а также хранить письменное соглашение с Держателем (согласие\/ поручение Держателя) об условиях проведения Повторяющихся платежей;\n• получать от Держателя согласие на совершение Повторяющихся платежей, в том числе с суммой Повторяющихся платежей, периодом времени, в течение которого совершаются Повторяющиеся платежи, регулярностью совершения Повторяющихся платежей, порядком прекращения неосуществленных Повторяющихся платежей;\n• обеспечить Покупателю возможность отмены неосуществленных Повторяющихся платежей в порядке, определенном договором, заключенным с Покупателем;\n• прекратить осуществление Повторяющихся платежей в порядке, установленном договором с Покупателем, в случае получения от такого Покупателя уведомления об отказе от осуществления Повторяющихся платежей и (или) прекращения действия договора, заключенного между Покупателем и Предприятием.",
   931	  "required_type":"mandatory",
   932	  "main_idea":"",
   933	  "only_for_product":"internet_acquiring",
   934	  "only_for_lot":"common",
   935	  "only_for_terminal":"common",
   936	  "topics":[
   937	
   938	  ],
   939	  "payment_method":"common"
   940	 },
   941	 {
   942	  "number":"5.1.1.1",
   943	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, являющихся недействительными, в следующих случаях:\n1) Операция совершена с нарушением Договора, требований законодательства РФ и\/или правил Платежной системы и инструктивных материалов Банка;\n2) Операция совершена по поддельной или недействительной Карте;\n3) Документ по операции заполнен не полностью, имеются исправления или отсутствует возможность определить сумму Операции, код Авторизации;\n4) экземпляр Документа по операции, переданный в Банк, не соответствует экземпляру Документа по операции, переданному Покупателю;\n5)  подпись Покупателя на Чеке электронного терминала отсутствует, при этом на Чеке электронного терминала присутствует поле «Подпись Клиента»;\n6) по требованию Банка в течение 3 (трех) рабочих дней со дня получения запроса не предоставлены или предоставлены не в полном объеме (или не соответствующие правилам Платежной системы) или в ненадлежащем качестве подтверждающие Документы по операции\/объяснения обстоятельств Операции;\n7) оплаченные с использованием Карты \/ее реквизитов \/ NFС-карты \/ SberPay \/ Плати QR \/ Платежного счета  Товары\/услуги были возвращены Предприятию, или не доставлены Покупателю\/услуги отменены\/не оказаны, но возврат денежных средств Покупателю произведен не был (за исключением случаев, когда Товары\/услуги не были приняты\/возврат Товара\/отказ от услуг не предусмотрен законодательством РФ или правилами работы Предприятия и Покупатель был об этом проинформирован до совершения сделки);\n8) Товар\/услуга уже был оплачен Покупателем ранее (о чем имеется документальное подтверждение);\n9) на совершенную Операцию Банком не был получен код Авторизации согласно Порядка проведения операций в Торгово-сервисных точках\/на Ресурсе. Код Авторизации считается полученным Банком в том случае, если он содержится в электронных реестрах кодов Авторизации Банка и относится к указанной Операции. Код Авторизации указывается на Чеке Электронного терминала, который передается в ККТ Предприятия от Электронного терминала ;\n10) сумма Товара\/услуги была разбита на несколько Операций;\n11) от Банка-эмитента получена информация о мошенническом характере Операции;\n12)  Операция была проведена без считывания Карты в Электронном терминале (реквизиты Карты были введены в Электронный терминал вручную), за исключением случаев, когда данные действия согласованы  с Банком.\n",
   944	  "required_type":"mandatory",
   945	  "main_idea":"",
   946	  "only_for_product":"common",
   947	  "only_for_lot":"common",
   948	  "only_for_terminal":"common",
   949	  "topics":[
   950	   "Банк имеет право удерживать суммы операций, являющиеся недействительными"
   951	  ],
   952	  "payment_method":"common"
   953	 },
   954	 {
   955	  "number":"5.1.1.2",
   956	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы, ошибочно перечисленные на счет Предприятия.",
   957	  "required_type":"mandatory",
   958	  "main_idea":"",
   959	  "only_for_product":"common",
   960	  "only_for_lot":"common",
   961	  "only_for_terminal":"common",
   962	  "topics":[
   963	   "Банк имеет право удерживать ошибочно перечисленные суммы с счета Предприятия"
   964	  ],
   965	  "payment_method":"common"
   966	 },
   967	 {
   968	  "number":"5.1.1.3",
   969	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.",
   970	  "required_type":"mandatory",
   971	  "main_idea":"",
   972	  "only_for_product":"common",
   973	  "only_for_lot":"common",
   974	  "only_for_terminal":"common",
   975	  "topics":[
   976	   "Банк имеет право удерживать суммы операций возврата, возврата платежа, реверсивные транзакции. Важно не рассматривать пункты в которых не указана хотя бы одна из этих сумм"
   977	  ],
   978	  "payment_method":"common"
   979	 },
   980	 {
   981	  "number":"5.1.1.4",
   982	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, которые были оспорены и\/или списаны со счета Банка Банком – эмитентом в соответствии с правилами Платежной системы по Операциям, проведенным в ТСТ, суммы оспоренных Операций, проведенных с использованием SberPay\/Плати QR, а также суммы оспоренных Операций в отношении Товаров\/услуг, реализуемых Предприятием как агентом.",
   983	  "required_type":"mandatory",
   984	  "main_idea":"",
   985	  "only_for_product":"common",
   986	  "only_for_lot":"common",
   987	  "only_for_terminal":"common",
   988	  "topics":[
   989	   "Банк имеет право удерживать суммы оспоренных операций или списанных со счёта испольнителя банком-эмитентом",
   990	   "Банк удерживает суммы оспоренных операций в случае реализации товаров\/услуг Предприятием как агентом"
   991	  ],
   992	  "payment_method":"common"
   993	 },
   994	 {
   995	  "number":"5.1.1.5",
   996	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов и иных убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору.",
   997	  "required_type":"mandatory",
   998	  "main_idea":"",
   999	  "only_for_product":"common",
  1000	  "only_for_lot":"common",
  1001	  "only_for_terminal":"common",
  1002	  "topics":[
  1003	   "Банк вправе удерживать штрафы из сумм Предприятия, возникшие у Банка в связи недобросовестным исполнением Заказчика контракта",
  1004	   "Банк вправе удерживать убытки из сумм Предприятия, возникшие в связи с привлечением Банка к гражданской или административной ответственности из-за недобросовестного исполнением Заказчика контракта"
  1005	  ],
  1006	  "payment_method":"common"
  1007	 },
  1008	 {
  1009	  "number":"5.1.1.6",
  1010	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов в случае невозврата Электронных терминалов\/Смарт-терминалов Банка в соответствии с п. 4.2.20.7 Договора.",
  1011	  "required_type":"mandatory",
  1012	  "main_idea":"Возможность удержания штрафов за невозврат терминалов. ",
  1013	  "only_for_product":"trade_acquiring",
  1014	  "only_for_lot":"common",
  1015	  "only_for_terminal":"common",
  1016	  "topics":[
  1017	   "Банк имеет право удерживать суммы штрафов за невозврат Электронных терминалов\/Смарт-терминалов"
  1018	  ],
  1019	  "payment_method":"common"
  1020	 },
  1021	 {
  1022	  "number":"5.1.2",
  1023	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае возникновения у Предприятия задолженности перед Банком приостановить проведение Авторизации до момента полного погашения задолженности.",
  1024	  "required_type":"mandatory",
  1025	  "main_idea":"",
  1026	  "only_for_product":"common",
  1027	  "only_for_lot":"common",
  1028	  "only_for_terminal":"common",
  1029	  "topics":[
  1030	   "Банк вправе приостанавливать авторизацию при наличии задолженности у Предприятия",
  1031	   "Приостановка допускается до полного погашения задолженности Предприятием"
  1032	  ],
  1033	  "payment_method":"common"
  1034	 },
  1035	 {
  1036	  "number":"5.1.3",
  1037	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, списывать без дополнительного распоряжения Предприятия (на условиях заранее данного акцепта, предоставленного Банку Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг) денежные средства с расчетного счета Предприятия, открытого в Банке. ",
  1038	  "required_type":"mandatory",
  1039	  "main_idea":"",
  1040	  "only_for_product":"common",
  1041	  "only_for_lot":"common",
  1042	  "only_for_terminal":"common",
  1043	  "topics":[
  1044	   "списание средств без дополнительного распоряжения",
  1045	   "условие заранее данного акцепта",
  1046	   "основание - заявление предприятия о проведении расчетов"
  1047	  ],
  1048	  "payment_method":"common"
  1049	 },
  1050	 {
  1051	  "number":"5.1.4",
  1052	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, Банк выставляет счет на оплату или платежное требование о списании денежных средств к расчетному счету Предприятия № --------------------------- в ----------------------- (наименование Банка, котором у Предприятия открыт счет). ",
  1053	  "required_type":"mandatory",
  1054	  "main_idea":"",
  1055	  "only_for_product":"common",
  1056	  "only_for_lot":"common",
  1057	  "only_for_terminal":"common",
  1058	  "topics":[
  1059	   "указан номер расчетного счета Предприятия",
  1060	   "указано наименование Банка, в котором у Предприятия открыт счет"
  1061	  ],
  1062	  "payment_method":"common"
  1063	 },
  1064	 {
  1065	  "number":"5.1.5",
  1066	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Не возмещать Предприятию суммы Операций, проведенных с нарушением условий Договора.",
  1067	  "required_type":"mandatory",
  1068	  "main_idea":"",
  1069	  "only_for_product":"common",
  1070	  "only_for_lot":"common",
  1071	  "only_for_terminal":"common",
  1072	  "topics":[
  1073	   "Банк имеет право не возмещать суммы операций, проведенных с нарушением условий договора"
  1074	  ],
  1075	  "payment_method":"common"
  1076	 },
  1077	 {
  1078	  "number":"5.1.6",
  1079	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять проверку технического состояния и порядка эксплуатации Электронных терминалов\/Смарт-терминалов Банка, расположенных на территории Предприятия\/ТСТ. Производить замену Электронных терминалов\/Смарт-терминалов Банка, а также обновлять программное обеспечение Электронных терминалов\/Смарт-терминалов, уведомив Предприятие не менее чем за 2 (два) рабочих дня до даты замены или обновления. Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения Операций, изложенный в Порядке проведения операций в Торгово-сервисных точках\/на Ресурсе, без предварительного уведомления Предприятия.",
  1080	  "required_type":"mandatory",
  1081	  "main_idea":"",
  1082	  "only_for_product":"common",
  1083	  "only_for_lot":"common",
  1084	  "only_for_terminal":"common",
  1085	  "topics":[
  1086	   "Банк имеет право проверять техническое состояние терминалов на территории предприятия",
  1087	   "Банк имеет право производить замену терминалов с уведомлением заказчика за 2 рабочих дня",
  1088	   "Банк имеет право обновлять ПО терминалов с уведомлением заказчика за 2 рабочих дня",
  1089	   "Допускается удаленное обновление ПО терминалов без изменения порядка операций и без предварительного уведомления"
  1090	  ],
  1091	  "payment_method":"common"
  1092	 },
  1093	 {
  1094	  "number":"5.1.7",
  1095	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Независимо от срока действия Договора в случае выявления подозрительных или мошеннических Операций передавать информацию, в том числе осуществлять передачу данных (сведения о Предприятии\/ТСТ\/Ресурсе, в том числе персональные данные руководителя\/представителя Предприятия, указанные в Заявлении\/Информации о ТСТ) в Платежную систему МИР в целях исполнения запросов, полученных от указанной платежной системы.В случае принятия Банком решения о расторжении Договора по причине мошеннической деятельности Предприятия сообщать в Платежную систему МИР: даты заключения и расторжения Договора, а также причины расторжения Договора, иные сведения о Предприятии.",
  1096	  "required_type":"mandatory",
  1097	  "main_idea":"",
  1098	  "only_for_product":"common",
  1099	  "only_for_lot":"common",
  1100	  "only_for_terminal":"common",
  1101	  "topics":[
  1102	   "Банк имеет право передавать информацию о предприятии при выявлении подозрительных операций",
  1103	   "Банк передает данные в Платежную систему МИР при расторжении договора из-за мошенничества",
  1104	   "Передаваемая информация включает дату заключения и расторжения договора, причину расторжения и другие сведения о предприятии"
  1105	  ],
  1106	  "payment_method":"common"
  1107	 },
  1108	 {
  1109	  "number":"5.1.8.1",
  1110	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → нарушение Предприятием условий Договора;",
  1111	  "required_type":"optional",
  1112	  "main_idea":"",
  1113	  "only_for_product":"common",
  1114	  "only_for_lot":"common",
  1115	  "only_for_terminal":"common",
  1116	  "topics":[
  1117	   "нарушение Предприятием условий Договора является основанием для прекращения Авторизации и расторжения Договора"
  1118	  ],
  1119	  "payment_method":"common"
  1120	 },
  1121	 {
  1122	  "number":"5.1.8.2",
  1123	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → внесение данных Предприятия в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;",
  1124	  "required_type":"optional",
  1125	  "main_idea":"",
  1126	  "only_for_product":"common",
  1127	  "only_for_lot":"common",
  1128	  "only_for_terminal":"common",
  1129	  "topics":[
  1130	   "внесение данных Предприятия в перечень организаций и физических лиц, причастных к экстремизму, терроризму или распространению оружия массового уничтожения является основанием для прекращения Авторизации и расторжения договора"
  1131	  ],
  1132	  "payment_method":"common"
  1133	 },
  1134	 {
  1135	  "number":"5.1.8.3",
  1136	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → при наличии у Банка подозрений, что Операции в ТСТ\/на Ресурсе совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;",
  1137	  "required_type":"optional",
  1138	  "main_idea":"",
  1139	  "only_for_product":"common",
  1140	  "only_for_lot":"common",
  1141	  "only_for_terminal":"common",
  1142	  "topics":[
  1143	   "Банк вправе прекратить Авторизацию при подозрении на отмывание денег или финансирование терроризма"
  1144	  ],
  1145	  "payment_method":"common"
  1146	 },
  1147	 {
  1148	  "number":"5.1.8.4",
  1149	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → несоответствие Ресурса Требованиям Банка к Ресурсу Предприятия;",
  1150	  "required_type":"optional",
  1151	  "main_idea":"",
  1152	  "only_for_product":"internet_acquiring",
  1153	  "only_for_lot":"common",
  1154	  "only_for_terminal":"common",
  1155	  "topics":[
  1156	   "Банк вправе прекратить Авторизацию при несоответствии Ресурса Требованиям Банка"
  1157	  ],
  1158	  "payment_method":"common"
  1159	 },
  1160	 {
  1161	  "number":"5.1.8.5",
  1162	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → осуществление видов деятельности, указанных в Требованиях к Ресурсу Предприятия;",
  1163	  "required_type":"optional",
  1164	  "main_idea":"",
  1165	  "only_for_product":"internet_acquiring",
  1166	  "only_for_lot":"common",
  1167	  "only_for_terminal":"common",
  1168	  "topics":[
  1169	   "Банк имеет право в одностороннем порядке прекратить проведение авторизации при осуществлении Заказчиком запрещенных видов деятельности согласно Требованиям к Ресурсу Предприятия"
  1170	  ],
  1171	  "payment_method":"common"
  1172	 },
  1173	 {
  1174	  "number":"5.1.8.6",
  1175	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → получение негативной информации о Предприятии\/ТСТ \/Ресурсе  от органов государственной власти РФ и\/или Платежной системы;",
  1176	  "required_type":"optional",
  1177	  "main_idea":"",
  1178	  "only_for_product":"common",
  1179	  "only_for_lot":"common",
  1180	  "only_for_terminal":"common",
  1181	  "topics":[
  1182	   "Банк имеет право прекратить проведение авторизации при получении негативной информации о предприятии от органов государственной власти",
  1183	   "Банк имеет право расторгнуть договор при получении негативной информации о ресурсе от платежной системы"
  1184	  ],
  1185	  "payment_method":"common"
  1186	 },
  1187	 {
  1188	  "number":"5.1.8.7",
  1189	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → получение информации о мошенничестве в ТСТ \/на Ресурсе ;стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов в Банк, или уведомления от Платежной системы, полученные c использованием факсимильной связи, по электронной почте (e-mail);",
  1190	  "required_type":"optional",
  1191	  "main_idea":"",
  1192	  "only_for_product":"common",
  1193	  "only_for_lot":"common",
  1194	  "only_for_terminal":"common",
  1195	  "topics":[
  1196	   "Банк имеет право прекратить Авторизацию при получении информации о мошенничестве",
  1197	   "Достаточным подтверждением мошенничества являются сведения от Банка-эмитента или Платежной системы",
  1198	   "Подтверждение может быть получено по факсу или электронной почте"
  1199	  ],
  1200	  "payment_method":"common"
Tool:    201	      "procedure_channel": "",
   202	      "liability_remedy": "",
   203	      "scope_options": [],
   204	      "consequence": "",
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
   224	      "materiality": "needs_source_review",
   225	      "protected_party": "",
   226	      "bound_party": "",
   227	      "right_or_obligation": "",
   228	      "legal_object": "",
   229	      "trigger": "",
   230	      "deadline": "",
   231	      "amount_formula_cap": "",
   232	      "procedure_channel": "",
   233	      "liability_remedy": "",
   234	      "scope_options": [],
   235	      "consequence": "",
   236	      "applicability_filters": {
   237	        "required_type": "mandatory",
   238	        "only_for_product": "common",
   239	        "only_for_lot": "fz_44",
   240	        "only_for_terminal": "common",
   241	        "payment_method": "common"
   242	      },
   243	      "main_idea": "Важен сам факт наличия данного канала для обмена электронными документами",
   244	      "topics": [
   245	        "Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок)",
   246	        "Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП)"
   247	      ],
   248	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;"
   249	    },
   250	    {
   251	      "id": "2.3.7",
   252	      "source_text": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию Обмен информацией через обращение в службу поддержки Банка; Дата с которой сторона считается получившей информацию в случае её направления на электронную почту; Дата с которой сторона считается получившей информацию в случае запроса в ДБО; Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма; Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»; Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в: • п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно; • п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма); • п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции; • п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке; • п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   253	      "source_excerpt": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию Обмен информацией через обращение в службу поддержки Банка;",
   254	      "type": "operative",
   255	      "materiality": "needs_source_review",
   256	      "protected_party": "",
   257	      "bound_party": "",
   258	      "right_or_obligation": "",
   259	      "legal_object": "",
   260	      "trigger": "",
   261	      "deadline": "",
   262	      "amount_formula_cap": "",
   263	      "procedure_channel": "",
   264	      "liability_remedy": "",
   265	      "scope_options": [],
   266	      "consequence": "",
   267	      "applicability_filters": {
   268	        "required_type": "optional",
   269	        "only_for_product": "common",
   270	        "only_for_lot": "common",
   271	        "only_for_terminal": "common",
   272	        "payment_method": "common"
   273	      },
   274	      "main_idea": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию",
   275	      "topics": [
   276	        "Обмен информацией через обращение в службу поддержки Банка",
   277	        "Дата с которой сторона считается получившей информацию в случае её направления на электронную почту",
   278	        "Дата с которой сторона считается получившей информацию в случае запроса в ДБО",
   279	        "Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма",
   280	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»",
   281	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС"
   282	      ],
   283	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в:\n• п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;\n• п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма);\n• п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;\n•  п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке;\n• п. 2.3.7. Договора – в дату обращения в службу поддержки Банка."
   284	    },
   285	    {
   286	      "id": "2.4",
   287	      "source_text": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   288	      "source_excerpt": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   289	      "type": "operative",
   290	      "materiality": "needs_source_review",
   291	      "protected_party": "",
   292	      "bound_party": "",
   293	      "right_or_obligation": "",
   294	      "legal_object": "",
   295	      "trigger": "",
   296	      "deadline": "",
   297	      "amount_formula_cap": "",
   298	      "procedure_channel": "",
   299	      "liability_remedy": "",
   300	      "scope_options": [],
   301	      "consequence": "",
   302	      "applicability_filters": {
   303	        "required_type": "optional",
   304	        "only_for_product": "common",
   305	        "only_for_lot": "common",
   306	        "only_for_terminal": "common",
   307	        "payment_method": "common"
   308	      },
   309	      "main_idea": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   310	      "topics": [],
   311	      "enriched_text": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора."
   312	    },
   313	    {
   314	      "id": "2.5.1.1",
   315	      "source_text": "Важен факт, что бесконтактная оплата подключается автоматически SberPayOnline подключается автоматически при подключении Интернет-эквайринга; используется единый тариф по Интернет-эквайрингу Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;",
   316	      "source_excerpt": "Важен факт, что бесконтактная оплата подключается автоматически SberPayOnline подключается автоматически при подключении Интернет-эквайринга; используется единый тариф по Интернет-эквайрингу Возможность совершения Операций оплаты с использо",
   317	      "type": "operative",
   318	      "materiality": "needs_source_review",
   319	      "protected_party": "",
   320	      "bound_party": "",
   321	      "right_or_obligation": "",
   322	      "legal_object": "",
   323	      "trigger": "",
   324	      "deadline": "",
   325	      "amount_formula_cap": "",
   326	      "procedure_channel": "",
   327	      "liability_remedy": "",
   328	      "scope_options": [],
   329	      "consequence": "",
   330	      "applicability_filters": {
   331	        "required_type": "mandatory",
   332	        "only_for_product": "internet_acquiring",
   333	        "only_for_lot": "common",
   334	        "only_for_terminal": "common",
   335	        "payment_method": "common"
   336	      },
   337	      "main_idea": "Важен факт, что бесконтактная оплата подключается автоматически",
   338	      "topics": [
   339	        "SberPayOnline подключается автоматически при подключении Интернет-эквайринга",
   340	        "используется единый тариф по Интернет-эквайрингу"
   341	      ],
   342	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;"
   343	    },
   344	    {
   345	      "id": "2.5.2.1",
   346	      "source_text": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; наличие документа 'Информация о ТСТ' Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.",
   347	      "source_excerpt": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; н",
   348	      "type": "operative",
   349	      "materiality": "needs_source_review",
   350	      "protected_party": "",
   351	      "bound_party": "",
   352	      "right_or_obligation": "",
   353	      "legal_object": "",
   354	      "trigger": "",
   355	      "deadline": "",
   356	      "amount_formula_cap": "",
   357	      "procedure_channel": "",
   358	      "liability_remedy": "",
   359	      "scope_options": [],
   360	      "consequence": "",
   361	      "applicability_filters": {
   362	        "required_type": "mandatory",
   363	        "only_for_product": "trade_acquiring",
   364	        "only_for_lot": "common",
   365	        "only_for_terminal": "common",
   366	        "payment_method": "sber_pay_face_scan"
   367	      },
   368	      "main_idea": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением",
   369	      "topics": [
   370	        "подключение SberPayFaceScan оформляется на бумажном носителе",
   371	        "подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия",
   372	        "наличие документа 'Информация о ТСТ'"
   373	      ],
   374	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ."
   375	    },
   376	    {
   377	      "id": "2.6.1.1",
   378	      "source_text": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.",
   379	      "source_excerpt": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-код",
   380	      "type": "operative",
   381	      "materiality": "needs_source_review",
   382	      "protected_party": "",
   383	      "bound_party": "",
   384	      "right_or_obligation": "",
   385	      "legal_object": "",
   386	      "trigger": "",
   387	      "deadline": "",
   388	      "amount_formula_cap": "",
   389	      "procedure_channel": "",
   390	      "liability_remedy": "",
   391	      "scope_options": [],
   392	      "consequence": "",
   393	      "applicability_filters": {
   394	        "required_type": "mandatory",
   395	        "only_for_product": "trade_acquiring",
   396	        "only_for_lot": "common",
   397	        "only_for_terminal": "smart",
   398	        "payment_method": "qr"
   399	      },
   400	      "main_idea": "Для приема QR на смарт-терминал не нужно отдельное ПО",
   401	      "topics": [
   402	        "OR-код подключается при установке Смарт-терминала Банка",
   403	        "OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ"
   404	      ],
   405	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ."
   406	    },
   407	    {
   408	      "id": "2.6.2.1",
   409	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка возможность использования QR-кода на ККТ с собственным ПО Предприятия; подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API); порядок и условия подключения QR-API описаны на Официальном сайте Банка Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;",
   410	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте бан",
   411	      "type": "operative",
   412	      "materiality": "needs_source_review",
   413	      "protected_party": "",
   414	      "bound_party": "",
   415	      "right_or_obligation": "",
   416	      "legal_object": "",
   417	      "trigger": "",
   418	      "deadline": "",
   419	      "amount_formula_cap": "",
   420	      "procedure_channel": "",
   421	      "liability_remedy": "",
   422	      "scope_options": [],
   423	      "consequence": "",
   424	      "applicability_filters": {
   425	        "required_type": "mandatory",
   426	        "only_for_product": "trade_acquiring",
   427	        "only_for_lot": "common",
   428	        "only_for_terminal": "common",
   429	        "payment_method": "qr"
   430	      },
   431	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре.  Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка",
   432	      "topics": [
   433	        "возможность использования QR-кода на ККТ с собственным ПО Предприятия",
   434	        "подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API)",
   435	        "порядок и условия подключения QR-API описаны на Официальном сайте Банка"
   436	      ],
   437	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;"
   438	    },
   439	    {
   440	      "id": "2.6.2.2",
   441	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ; подключение динамического QR-кода зависит от ПО ККТ; при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора; первая операция оплаты QR-кодом активирует услугу; Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора; подключение QR-кода производится согласно Приложениям №1 и №1.1 Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору.",
   442	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на",
   443	      "type": "operative",
   444	      "materiality": "needs_source_review",
   445	      "protected_party": "",
   446	      "bound_party": "",
   447	      "right_or_obligation": "",
   448	      "legal_object": "",
   449	      "trigger": "",
   450	      "deadline": "",
   451	      "amount_formula_cap": "",
   452	      "procedure_channel": "",
   453	      "liability_remedy": "",
   454	      "scope_options": [],
   455	      "consequence": "",
   456	      "applicability_filters": {
   457	        "required_type": "mandatory",
   458	        "only_for_product": "trade_acquiring",
   459	        "only_for_lot": "common",
   460	        "only_for_terminal": "common",
   461	        "payment_method": "qr"
   462	      },
   463	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия",
   464	      "topics": [
   465	        "возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ",
   466	        "подключение динамического QR-кода зависит от ПО ККТ",
   467	        "при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора",
   468	        "первая операция оплаты QR-кодом активирует услугу",
   469	        "Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора",
   470	        "подключение QR-кода производится согласно Приложениям №1 и №1.1"
   471	      ],
   472	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору."
   473	    },
   474	    {
   475	      "id": "2.6.3.1",
   476	      "source_text": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → QR-код подключается при установке Электронного терминала в ТСТ;",
   477	      "source_excerpt": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-",
   478	      "type": "operative",
   479	      "materiality": "needs_source_review",
   480	      "protected_party": "",
   481	      "bound_party": "",
   482	      "right_or_obligation": "",
   483	      "legal_object": "",
   484	      "trigger": "",
   485	      "deadline": "",
   486	      "amount_formula_cap": "",
   487	      "procedure_channel": "",
   488	      "liability_remedy": "",
   489	      "scope_options": [],
   490	      "consequence": "",
   491	      "applicability_filters": {
   492	        "required_type": "mandatory",
   493	        "only_for_product": "trade_acquiring",
   494	        "only_for_lot": "common",
   495	        "only_for_terminal": "common",
   496	        "payment_method": "qr"
   497	      },
   498	      "main_idea": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке",
   499	      "topics": [
   500	        "QR-код подключается при установке Электронного терминала в ТСТ"
   501	      ],
   502	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: →  QR-код подключается при установке Электронного терминала в ТСТ;"
   503	    },
   504	    {
   505	      "id": "2.6.3.2",
   506	      "source_text": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк отключение QR-кода возможно по инициативе Предприятия; инициатива отключения реализуется через обращение в Банк Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора.",
   507	      "source_excerpt": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк отключение QR-кода возможно по инициативе Предприятия; инициатива отключения реализуется через обращение в Банк Возможность",
   508	      "type": "operative",
   509	      "materiality": "needs_source_review",
   510	      "protected_party": "",
   511	      "bound_party": "",
   512	      "right_or_obligation": "",
   513	      "legal_object": "",
   514	      "trigger": "",
   515	      "deadline": "",
   516	      "amount_formula_cap": "",
   517	      "procedure_channel": "",
   518	      "liability_remedy": "",
   519	      "scope_options": [],
   520	      "consequence": "",
   521	      "applicability_filters": {
   522	        "required_type": "mandatory",
   523	        "only_for_product": "trade_acquiring",
   524	        "only_for_lot": "common",
   525	        "only_for_terminal": "common",
   526	        "payment_method": "qr"
   527	      },
   528	      "main_idea": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк",
   529	      "topics": [
   530	        "отключение QR-кода возможно по инициативе Предприятия",
   531	        "инициатива отключения реализуется через обращение в Банк"
   532	      ],
   533	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора."
   534	    },
   535	    {
   536	      "id": "2.7",
   537	      "source_text": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юридическую силу с Договором, оформленным на бумажном носителе, подписанным собственноручными подписями уполномоченных представителей Банка и Предприятия.",
   538	      "source_excerpt": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и под",
   539	      "type": "operative",
   540	      "materiality": "needs_source_review",
   541	      "protected_party": "",
   542	      "bound_party": "",
   543	      "right_or_obligation": "",
   544	      "legal_object": "",
   545	      "trigger": "",
   546	      "deadline": "",
   547	      "amount_formula_cap": "",
   548	      "procedure_channel": "",
   549	      "liability_remedy": "",
   550	      "scope_options": [],
   551	      "consequence": "",
   552	      "applicability_filters": {
   553	        "required_type": "optional",
   554	        "only_for_product": "common",
   555	        "only_for_lot": "common",
   556	        "only_for_terminal": "common",
   557	        "payment_method": "common"
   558	      },
   559	      "main_idea": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП ",
   560	      "topics": [],
   561	      "enriched_text": "Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юридическую силу с Договором, оформленным на бумажном носителе, подписанным собственноручными подписями уполномоченных представителей Банка и Предприятия."
   562	    },
   563	    {
   564	      "id": "3.1",
   565	      "source_text": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Плати QR); Приём оплаты осуществляется в ТСТ (торгово-сервисных точках) и/или на Ресурсе (сайт/приложение Предприятия); Обработка информации производится через Электронные терминалы, Смарт-терминалы или СПЭП; Перечень допустимых к приёму Карт «ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ/на Ресурсе и обработку информации на Электронных терминалах/Смарт-терминалах [1]/через СПЭП. Перечень Карт перечислен в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе к Договору, размещенном на Официальном сайте Банка",
   566	      "source_excerpt": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Пл",
   567	      "type": "operative",
   568	      "materiality": "needs_source_review",
   569	      "protected_party": "",
   570	      "bound_party": "",
   571	      "right_or_obligation": "",
   572	      "legal_object": "",
   573	      "trigger": "",
   574	      "deadline": "",
   575	      "amount_formula_cap": "",
   576	      "procedure_channel": "",
   577	      "liability_remedy": "",
   578	      "scope_options": [],
   579	      "consequence": "",
   580	      "applicability_filters": {
   581	        "required_type": "optional",
   582	        "only_for_product": "common",
   583	        "only_for_lot": "common",
   584	        "only_for_terminal": "common",
   585	        "payment_method": "common"
   586	      },
   587	      "main_idea": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР",
   588	      "topics": [
   589	        "Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Плати QR)",
   590	        "Приём оплаты осуществляется в ТСТ (торгово-сервисных точках) и/или на Ресурсе (сайт/приложение Предприятия)",
   591	        "Обработка информации производится через Электронные терминалы, Смарт-терминалы или СПЭП",
   592	        "Перечень допустимых к приёму Карт"
   593	      ],
   594	      "enriched_text": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ/на Ресурсе и обработку информации на Электронных терминалах/Смарт-терминалах [1]/через СПЭП. Перечень Карт перечислен в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе к Договору, размещенном на Официальном сайте Банка"
   595	    },
   596	    {
   597	      "id": "3.2",
   598	      "source_text": "Важен сам факт обязанности Банка в перечислении сумм Предприятию Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию «ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ/на Ресурсе.",
   599	      "source_excerpt": "Важен сам факт обязанности Банка в перечислении сумм Предприятию Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию «ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Това",
   600	      "type": "operative",
   601	      "materiality": "needs_source_review",
   602	      "protected_party": "",
   603	      "bound_party": "",
   604	      "right_or_obligation": "",
   605	      "legal_object": "",
   606	      "trigger": "",
   607	      "deadline": "",
   608	      "amount_formula_cap": "",
   609	      "procedure_channel": "",
   610	      "liability_remedy": "",
   611	      "scope_options": [],
   612	      "consequence": "",
   613	      "applicability_filters": {
   614	        "required_type": "optional",
   615	        "only_for_product": "common",
   616	        "only_for_lot": "common",
   617	        "only_for_terminal": "common",
   618	        "payment_method": "common"
   619	      },
   620	      "main_idea": "Важен сам факт обязанности Банка в перечислении сумм Предприятию",
   621	      "topics": [
   622	        "Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию"
   623	      ],
   624	      "enriched_text": "«ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ/на Ресурсе."
   625	    },
   626	    {
   627	      "id": "3.3",
   628	      "source_text": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору Предприятие перечисляет Банку плату за проведение расчётов ежемесячно «ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров/услуг в ТСТ[7]/на Ресурсе – к ИЭ[8]",
   629	      "source_excerpt": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору Предприятие перечисляет Банку плату за проведение расчётов ежемесячно «ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Раздел",
   630	      "type": "operative",
   631	      "materiality": "needs_source_review",
   632	      "protected_party": "",
   633	      "bound_party": "",
   634	      "right_or_obligation": "",
   635	      "legal_object": "",
   636	      "trigger": "",
   637	      "deadline": "",
   638	      "amount_formula_cap": "",
   639	      "procedure_channel": "",
   640	      "liability_remedy": "",
   641	      "scope_options": [],
   642	      "consequence": "",
   643	      "applicability_filters": {
   644	        "required_type": "mandatory",
   645	        "only_for_product": "common",
   646	        "only_for_lot": "common",
   647	        "only_for_terminal": "common",
   648	        "payment_method": "common"
   649	      },
   650	      "main_idea": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору",
   651	      "topics": [
   652	        "Предприятие перечисляет Банку плату за проведение расчётов ежемесячно"
   653	      ],
   654	      "enriched_text": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров/услуг в ТСТ[7]/на Ресурсе – к ИЭ[8]"
   655	    },
   656	    {
   657	      "id": "4.1.1",
   658	      "source_text": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов с Банком; Согласование информационных материалов осуществляется в соответствии с пунктами 2.3.1 и 2.3.2 «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3.1 и п. 2.3.2 настоящего Договора.",
   659	      "source_excerpt": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов",
   660	      "type": "operative",
   661	      "materiality": "needs_source_review",
   662	      "protected_party": "",
   663	      "bound_party": "",
   664	      "right_or_obligation": "",
   665	      "legal_object": "",
   666	      "trigger": "",
   667	      "deadline": "",
   668	      "amount_formula_cap": "",
   669	      "procedure_channel": "",
   670	      "liability_remedy": "",
   671	      "scope_options": [],
   672	      "consequence": "",
   673	      "applicability_filters": {
   674	        "required_type": "optional",
   675	        "only_for_product": "common",
   676	        "only_for_lot": "common",
   677	        "only_for_terminal": "common",
   678	        "payment_method": "qr"
   679	      },
   680	      "main_idea": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком",
   681	      "topics": [
   682	        "Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов с Банком",
   683	        "Согласование информационных материалов осуществляется в соответствии с пунктами 2.3.1 и 2.3.2"
   684	      ],
   685	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3.1 и п. 2.3.2 настоящего Договора."
   686	    },
   687	    {
   688	      "id": "4.1.2",
   689	      "source_text": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов; закреплено право Заказчика на получение консультаций по проведению Операций «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, указанному в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.",
   690	      "source_excerpt": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов; закреплено право Заказчика на получение ко",
   691	      "type": "operative",
   692	      "materiality": "needs_source_review",
   693	      "protected_party": "",
   694	      "bound_party": "",
   695	      "right_or_obligation": "",
   696	      "legal_object": "",
   697	      "trigger": "",
   698	      "deadline": "",
   699	      "amount_formula_cap": "",
   700	      "procedure_channel": "",
AI: I now have a solid understanding of the data. Let me plan my task. I need to identify **material contract-only terms** — contract clauses that have no matrix analogue and have independent legal effect. Let me set up my task list and systematically work through the contract.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full contract text and identify all contract clause IDs', 'status': 'in_progress'}, {'content': 'Read full matrix to understand all matrix requirements and their applicability filters', 'status': 'pending'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile) for context', 'status': 'pending'}, {'content': 'Identify contract clauses with no matrix analogue using materiality ladder', 'status': 'pending'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Build domain_crosswalk fragment with processed/assigned/skipped/unresolved IDs', 'status': 'pending'}, {'content': 'Write output to /outputs/working/contract_extra_review.json', 'status': 'pending'}]}, 'id': 'call_00_vbMFQEDhdiaKLfG6tEaC5528', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full contract text and identify all contract clause IDs', 'status': 'in_progress'}, {'content': 'Read full matrix to understand all matrix requirements and their applicability filters', 'status': 'pending'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile) for context', 'status': 'pending'}, {'content': 'Identify contract clauses with no matrix analogue using materiality ladder', 'status': 'pending'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Build domain_crosswalk fragment with processed/assigned/skipped/unresolved IDs', 'status': 'pending'}, {'content': 'Write output to /outputs/working/contract_extra_review.json', 'status': 'pending'}]
AI: Let me read the remaining parts of the contract and matrix, and the rest of the legal propositions.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 400, 'limit': 200}, 'id': 'call_00_sShzQNOyPi5Az8415JEB9341', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 1200, 'limit': 500}, 'id': 'call_01_Pky3tFx28m5JIXgM9Mqt1826', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 700, 'limit': 500}, 'id': 'call_02_hd7HPWH8VKpVKGs2QHex6167', 'type': 'tool_call'}]
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
Tool:   1201	 },
  1202	 {
  1203	  "number":"5.1.8.8",
  1204	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций;",
  1205	  "required_type":"optional",
  1206	  "main_idea":"",
  1207	  "only_for_product":"trade_acquiring",
  1208	  "only_for_lot":"common",
  1209	  "only_for_terminal":"common",
  1210	  "topics":[
  1211	   "осуществление ремонта помещений ТСТ препятствует операциям",
  1212	   "банк вправе прекратить авторизацию для ТСТ",
  1213	   "банк вправе инициировать расторжение договора"
  1214	  ],
  1215	  "payment_method":"common"
  1216	 },
  1217	 {
  1218	  "number":"5.1.8.9",
  1219	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → ликвидация Предприятия либо возбуждение в отношении Предприятия дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)»;",
  1220	  "required_type":"optional",
  1221	  "main_idea":"",
  1222	  "only_for_product":"common",
  1223	  "only_for_lot":"common",
  1224	  "only_for_terminal":"common",
  1225	  "topics":[
  1226	   "ликвидация Предприятия",
  1227	   "возбуждение дела о банкротстве Предприятия по закону №127-ФЗ"
  1228	  ],
  1229	  "payment_method":"common"
  1230	 },
  1231	 {
  1232	  "number":"5.1.8.10",
  1233	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → выявление недостоверных сведений о Предприятии\/ТСТ, руководителе(-ях) в информации, указанной при заключении Договора;\n",
  1234	  "required_type":"optional",
  1235	  "main_idea":"",
  1236	  "only_for_product":"common",
  1237	  "only_for_lot":"common",
  1238	  "only_for_terminal":"common",
  1239	  "topics":[
  1240	   "выявление недостоверных сведений о Предприятии",
  1241	   "выявление недостоверных сведений о ТСТ",
  1242	   "выявление недостоверных сведений о руководителе Предприятия"
  1243	  ],
  1244	  "payment_method":"common"
  1245	 },
  1246	 {
  1247	  "number":"5.1.8.11",
  1248	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → несоответствие предлагаемых Покупателям Товаров\/услуг роду деятельности Предприятия, указанному в Информации о ТСТ;",
  1249	  "required_type":"optional",
  1250	  "main_idea":"",
  1251	  "only_for_product":"common",
  1252	  "only_for_lot":"common",
  1253	  "only_for_terminal":"common",
  1254	  "topics":[
  1255	   "Банк имеет право прекратить проведение авторизации при несоответствии товаров\/услуг роду деятельности предприятия",
  1256	   "Банк имеет право в одностороннем порядке расторгнуть договор при выявленном несоответствии товаров\/услуг заявленной деятельности"
  1257	  ],
  1258	  "payment_method":"common"
  1259	 },
  1260	 {
  1261	  "number":"5.1.8.12",
  1262	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → отсутствие операций в течение 30 (тридцати) календарных дней подряд;",
  1263	  "required_type":"optional",
  1264	  "main_idea":"",
  1265	  "only_for_product":"common",
  1266	  "only_for_lot":"common",
  1267	  "only_for_terminal":"common",
  1268	  "topics":[
  1269	   "отсутствие операций в течение 30 календарных дней подряд является основанием для прекращения проведения авторизации и расторжения договора"
  1270	  ],
  1271	  "payment_method":"common"
  1272	 },
  1273	 {
  1274	  "number":"5.1.8.13",
  1275	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и\/или провести мероприятия по расторжению Договора при наступлении следующих событий: → исчерпание Цены Договора и\/или окончание срока действия Договора, указанного в п. 10.1 Договора.",
  1276	  "required_type":"optional",
  1277	  "main_idea":"",
  1278	  "only_for_product":"common",
  1279	  "only_for_lot":"common",
  1280	  "only_for_terminal":"common",
  1281	  "topics":[
  1282	   "исчерпание Цены Договора",
  1283	   "окончание срока действия Договора"
  1284	  ],
  1285	  "payment_method":"common"
  1286	 },
  1287	 {
  1288	  "number":"5.1.9",
  1289	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять дополнительные проверки проведения Операции в ТСТ, в т.ч. обращаться в Банк-эмитент для проверки правомерности Операции.",
  1290	  "required_type":"mandatory",
  1291	  "main_idea":"",
  1292	  "only_for_product":"common",
  1293	  "only_for_lot":"common",
  1294	  "only_for_terminal":"common",
  1295	  "topics":[
  1296	   "Банк имеет право осуществлять дополнительные проверки проведения Операции в ТСТ",
  1297	   "Банк имеет право обращаться в Банк-эмитент для проверки правомерности Операции"
  1298	  ],
  1299	  "payment_method":"common"
  1300	 },
  1301	 {
  1302	  "number":"5.1.10",
  1303	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Проводить проверку Предприятия, в т.ч. на предмет выявления мошеннических операций, предоставления Покупателям Товаров\/услуг, несоответствующих роду деятельности Предприятия, указанному в Информации о ТСТ, несоблюдения Предприятием\/ТСТ требований, установленных настоящим Договором к Ресурсу[1].\n[2]Проверки могут осуществляться Банком, в том числе с доступом к разделам Ресурса с ограниченным доступом, не связанным с администрированием и сопровождением (VIP, Оптовое, Клубное обслуживание, и т.п.).",
  1304	  "required_type":"mandatory",
  1305	  "main_idea":"",
  1306	  "only_for_product":"common",
  1307	  "only_for_lot":"common",
  1308	  "only_for_terminal":"common",
  1309	  "topics":[
  1310	   "Банк имеет право проводить проверки Предприятия",
  1311	   "Проверки проводятся для выявления мошенничества и несоответствия рода деятельности Предприятия информации о нем",
  1312	   "Проверки включают контроль соблюдения Предприятием требований Договора к Ресурсу",
  1313	   "Банк может осуществлять доступ к отдельным закрытым разделам Ресурса при проверках"
  1314	  ],
  1315	  "payment_method":"common"
  1316	 },
  1317	 {
  1318	  "number":"5.1.11",
  1319	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Запрашивать Документы по операциям не позднее 13 (тринадцати) месяцев с даты совершения Операции в сроки, установленные в п. 4.2.10 Договора. Для анализа спорных ситуаций Банк также может потребовать от Предприятия предоставления письменного заявления Предприятия с изложением обстоятельств проведения Операции, счетов за предоставленные Товары\/услуги, товарные или кассовые чеки и другие документы, необходимые для проведения анализа обстоятельств проведения операции или претензионной работы по электронным каналам связи одним из способов, указанных в п. 2.3 Договора.",
  1320	  "required_type":"mandatory",
  1321	  "main_idea":"",
  1322	  "only_for_product":"common",
  1323	  "only_for_lot":"common",
  1324	  "only_for_terminal":"common",
  1325	  "topics":[
  1326	   "Банк имеет право запрашивать документы по операциям",
  1327	   "Банк может требовать письменное заявление предприятия с обстоятельствами проведения операции",
  1328	   "Предприятие обязано предоставить счета, чеки и иные документы по требованию банка",
  1329	   "Обмен документами осуществляется через электронные каналы связи согласно пункту договора"
  1330	  ],
  1331	  "payment_method":"common"
  1332	 },
  1333	 {
  1334	  "number":"5.1.12",
  1335	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке вносить изменения в документы, ссылки на которые даются в Договоре, путем публикации информации на Официальном сайте Банка не менее чем за 1 (один) календарный день до введения в действие указанных изменений.",
  1336	  "required_type":"optional",
  1337	  "main_idea":"",
  1338	  "only_for_product":"common",
  1339	  "only_for_lot":"common",
  1340	  "only_for_terminal":"common",
  1341	  "topics":[
  1342	   "Банк вправе вносить изменения в связанные документы unilateral_in_one_day_right",
  1343	   "Опубликование изменений осуществляется на Официальном сайте Банка"
  1344	  ],
  1345	  "payment_method":"common"
  1346	 },
  1347	 {
  1348	  "number":"5.1.13",
  1349	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае изменения реквизитов Банка, указанных в Договоре, уведомить об этом Предприятие путем размещения информации на Официальном сайте Банка. ",
  1350	  "required_type":"optional",
  1351	  "main_idea":"Важно именно размещение информации на сайте. Если предусмотрены иные способы уведомления, то это разногласие",
  1352	  "only_for_product":"common",
  1353	  "only_for_lot":"common",
  1354	  "only_for_terminal":"common",
  1355	  "topics":[
  1356	   "Банк имеет право изменять свои реквизиты",
  1357	   "Уведомление об изменении реквизитов осуществляется через Официальный сайт Банка"
  1358	  ],
  1359	  "payment_method":"common"
  1360	 },
  1361	 {
  1362	  "number":"5.1.14",
  1363	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В целях получения информации по Операциям направлять запросы на адрес электронной почты Предприятия\/ТСТ, указанный в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг \/Информации о ТСТ.",
  1364	  "required_type":"mandatory",
  1365	  "main_idea":"",
  1366	  "only_for_product":"common",
  1367	  "only_for_lot":"common",
  1368	  "only_for_terminal":"common",
  1369	  "topics":[
  1370	   "Банк имеет право направлять запросы на адрес электронной почты Предприятия",
  1371	   "Адрес электронной почты указан в Заявлении Предприятия на проведение расчетов",
  1372	   "Запросы направлены для получения информации по Операциям"
  1373	  ],
  1374	  "payment_method":"common"
  1375	 },
  1376	 {
  1377	  "number":"5.1.15",
  1378	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Отказать Предприятию в заключении Договора без объяснения причин.",
  1379	  "required_type":"optional",
  1380	  "main_idea":"",
  1381	  "only_for_product":"common",
  1382	  "only_for_lot":"common",
  1383	  "only_for_terminal":"common",
  1384	  "topics":[
  1385	   "Банк имеет право отказать Предприятию в заключении Договора без указания причин"
  1386	  ],
  1387	  "payment_method":"common"
  1388	 },
  1389	 {
  1390	  "number":"5.1.16",
  1391	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Требовать от Предприятия предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства",
  1392	  "required_type":"mandatory",
  1393	  "main_idea":"",
  1394	  "only_for_product":"common",
  1395	  "only_for_lot":"common",
  1396	  "only_for_terminal":"common",
  1397	  "topics":[
  1398	   "Банк имеет право требовать от Предприятия предоставления документов",
  1399	   "Перечень требуемых документов определяется законодательством"
  1400	  ],
  1401	  "payment_method":"common"
  1402	 },
  1403	 {
  1404	  "number":"5.1.17.1",
  1405	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов\/Смарт-терминалов, находящихся в собственности Банка, в случае если: → Торговый оборот на один Электронный терминал Банка не превышает 40 000 (сорок тысяч) рублей (для г. Москва и г. Санкт-Петербург не превышает 80 000 (восемьдесят тысяч) рублей) за последний календарный месяц (без учета в обороте Операций возврата);",
  1406	  "required_type":"optional",
  1407	  "main_idea":"",
  1408	  "only_for_product":"trade_acquiring",
  1409	  "only_for_lot":"common",
  1410	  "only_for_terminal":"pos",
  1411	  "topics":[
  1412	   "оборот менее 40 000 руб. за месяц для регионов",
  1413	   "оборот менее 80 000 руб. за месяц для Москвы и СПб"
  1414	  ],
  1415	  "payment_method":"common"
  1416	 },
  1417	 {
  1418	  "number":"5.1.17.2",
  1419	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов\/Смарт-терминалов, находящихся в собственности Банка, в случае если: → 5.1.17.2. Торговый оборот на один Смарт-терминал Банка не превышает 40 000 (сорок тысяч) рублей (для г. Москва и г. Санкт-Петербург не превышает 80 000 (восемьдесят тысяч) рублей) за последний календарный месяц (без учета в обороте Операций возврата) или имеется задолженность перед Банком по плате за сервисное обслуживание\/вознаграждения Банка\/Операциям возврата Смарт-терминала Банка.",
  1420	  "required_type":"optional",
  1421	  "main_idea":"",
  1422	  "only_for_product":"trade_acquiring",
  1423	  "only_for_lot":"common",
  1424	  "only_for_terminal":"smart",
  1425	  "topics":[
  1426	   "торговый оборот менее 40 000 руб. для регионов",
  1427	   "торговый оборот менее 80 000 руб. для Москвы и СПб",
  1428	   "наличие задолженности по сервисному обслуживанию",
  1429	   "наличие задолженности по вознаграждениям банка",
  1430	   "наличие задолженности по операциям возврата смарт-терминала"
  1431	  ],
  1432	  "payment_method":"common"
  1433	 },
  1434	 {
  1435	  "number":"5.2.1",
  1436	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечить Предприятию доступ к СПЭП для осуществления Операций.",
  1437	  "required_type":"mandatory",
  1438	  "main_idea":"",
  1439	  "only_for_product":"internet_acquiring",
  1440	  "only_for_lot":"common",
  1441	  "only_for_terminal":"common",
  1442	  "topics":[
  1443	   "обязательство обеспечить доступ к СПЭП",
  1444	   "описание порядка доступа к СПЭП"
  1445	  ],
  1446	  "payment_method":"common"
  1447	 },
  1448	 {
  1449	  "number":"5.2.2",
  1450	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечить безопасность проведения Операций в Интернет-эквайринге посредством использования современных протоколов и Технологий 3DSecure",
  1451	  "required_type":"mandatory",
  1452	  "main_idea":"",
  1453	  "only_for_product":"internet_acquiring",
  1454	  "only_for_lot":"common",
  1455	  "only_for_terminal":"common",
  1456	  "topics":[
  1457	   "использование современных протоколов безопасности",
  1458	   "использование технологий 3DSecure"
  1459	  ],
  1460	  "payment_method":"common"
  1461	 },
  1462	 {
  1463	  "number":"5.2.3",
  1464	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Установить на Предприятии и подготовить к эксплуатации Электронные терминалы\/Смарт-терминалы Банка для проведения Операций. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком",
  1465	  "required_type":"mandatory",
  1466	  "main_idea":"Важно, чтобы в договоре срок установки был не менее 3 рабочих дней. Срок инструктажа не декларируется. Отсутствие отсылки на с инструктивные материалы разногласием не является",
  1467	  "only_for_product":"trade_acquiring",
  1468	  "only_for_lot":"common",
  1469	  "only_for_terminal":"common",
  1470	  "topics":[
  1471	   "установка Электронных терминалов\/Смарт-терминалов Банка на Предприятии",
  1472	   "подготовка Электронных терминалов\/Смарт-терминалов Банка к эксплуатации",
  1473	   "проведение первичного инструктажа работников ТСТ"
  1474	  ],
  1475	  "payment_method":"common"
  1476	 },
  1477	 {
  1478	  "number":"5.2.4",
  1479	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять круглосуточную Авторизацию",
  1480	  "required_type":"optional",
  1481	  "main_idea":"",
  1482	  "only_for_product":"common",
  1483	  "only_for_lot":"common",
  1484	  "only_for_terminal":"common",
  1485	  "topics":[
  1486	   "Банк осуществляет Авторизацию без перерывов 24 часа в сутки"
  1487	  ],
  1488	  "payment_method":"common"
  1489	 },
  1490	 {
  1491	  "number":"5.2.5",
  1492	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Разместить на сайте:  https:\/\/www.sberbank.ru\/help\/business\/acquiring обучающие материалы для прохождения инструктажа сотрудниками Предприятия",
  1493	  "required_type":"optional",
  1494	  "main_idea":"Подсвечивать разногласие, если только сайты отличаются, если в договоре вместо сайта прочерк, то это не разногласие",
  1495	  "only_for_product":"common",
  1496	  "only_for_lot":"common",
  1497	  "only_for_terminal":"common",
  1498	  "topics":[
  1499	   "обучающие материалы размещены по указанной ссылке",
  1500	   "материалы доступны для прохождения инструктажа сотрудниками Предприятия"
  1501	  ],
  1502	  "payment_method":"common"
  1503	 },
  1504	 {
  1505	  "number":"5.2.6",
  1506	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечивать Электронные терминалы\/Смарт-терминалы, установленные на Предприятии\/ТСТ, информационными материалами, необходимыми для проведения Операций",
  1507	  "required_type":"optional",
  1508	  "main_idea":"",
  1509	  "only_for_product":"trade_acquiring",
  1510	  "only_for_lot":"common",
  1511	  "only_for_terminal":"common",
  1512	  "topics":[
  1513	   "Обеспечение Электронных терминалов информационными материалами",
  1514	   "Обеспечение Смарт-терминалов информационными материалами"
  1515	  ],
  1516	  "payment_method":"common"
  1517	 },
  1518	 {
  1519	  "number":"5.2.7",
  1520	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечивать круглосуточную работоспособность Электронных терминалов\/Смарт-терминалов. В случае выхода из строя Электронного терминала\/Смарт-терминала Банка, обеспечить Предприятие исправным Электронным терминалом\/Смарт-терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Банком заявки от Предприятия по номеру службы поддержки Банка по телефонам, указанным в п..2. Порядка проведения операций в Торгово-сервисных точках\/на Ресурсе.",
  1521	  "required_type":"optional",
  1522	  "main_idea":"",
  1523	  "only_for_product":"common",
  1524	  "only_for_lot":"common",
  1525	  "only_for_terminal":"common",
  1526	  "topics":[
  1527	   "круглосуточная работоспособность Электронных терминалов\/Смарт-терминалов",
  1528	   "замена неисправного Электронного терминала\/Смарт-терминала на исправный не позднее 3 рабочих дней после заявки"
  1529	  ],
  1530	  "payment_method":"common"
  1531	 },
  1532	 {
  1533	  "number":"5.2.8",
  1534	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → На основании полученной от Предприятия расчетной информации, переданной от Электронного терминала\/Смарт-терминала  \/ Ресурса \/QR-кода  в Банк, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Банком перечислять на расчетный (текущий) счет Предприятия суммы Операций оплаты в валюте проведения операции (рубли РФ) за вычетом сумм, перечисленных в п.5.1.1 настоящего Договора. Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. ➜ «ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. ➜ «ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → В случае технического сбоя при передаче Электронной сверки итогов\/ невозможности проведения Предприятием\/ТСТ или отсутствия Электронной сверки итогов по иным причинам, перечислять Предприятию суммы Операций, за исключением сумм, указанных в первом абзаце настоящего пункта (п.5.2.8), по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов, проводить расчеты по всем Операциям с данной ТСТ. ",
  1535	  "required_type":"mandatory",
  1536	  "main_idea":"Важен срок перечисления средств",
  1537	  "only_for_product":"common",
  1538	  "only_for_lot":"common",
  1539	  "only_for_terminal":"common",
  1540	  "topics":[
  1541	   "перечисление средств на счет Предприятия не позднее 2 рабочих дней после получения расчетной информации",
  1542	   "дата получения расчетной информации - рабочий день, следующий за днем электронной сверки итогов",
  1543	   "при техническом сбое перечисление средств происходит через 3 календарных дня после последней успешной сверки"
  1544	  ],
  1545	  "payment_method":"common"
  1546	 },
  1547	 {
  1548	  "number":"5.2.9",
  1549	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Предоставить Предприятию QR-код партнера по электронным каналам связи в электронном виде или на бумажном носителе",
  1550	  "required_type":"optional",
  1551	  "main_idea":"",
  1552	  "only_for_product":"trade_acquiring",
  1553	  "only_for_lot":"common",
  1554	  "only_for_terminal":"common",
  1555	  "topics":[
  1556	   "Предоставление QR-кода партнера в электронном виде или на бумажном носителе"
  1557	  ],
  1558	  "payment_method":"qr"
  1559	 },
  1560	 {
  1561	  "number":"5.2.10",
  1562	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять обработку ПДн, полученных от Предприятия, а также обеспечить конфиденциальность и защиту обрабатываемых ПДн в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных». Принимать необходимые правовые, организационные и технические меры или обеспечивать их принятие для защиты получаемых от Предприятия ПДн от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения ПДн, а также от иных неправомерных действий в отношении получаемых от Предприятия ПДн",
  1563	  "required_type":"mandatory",
  1564	  "main_idea":"",
  1565	  "only_for_product":"common",
  1566	  "only_for_lot":"common",
  1567	  "only_for_terminal":"common",
  1568	  "topics":[
  1569	
  1570	  ],
  1571	  "payment_method":"common"
  1572	 },
  1573	 {
  1574	  "number":"5.2.12",
  1575	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Банк предоставляет QR-API (в т.ч. всё, что связано с организацией информационно-технологического взаимодействия посредством такого API) «как есть» без предоставления каких-либо гарантий",
  1576	  "required_type":"optional",
  1577	  "main_idea":"",
  1578	  "only_for_product":"internet_acquiring",
  1579	  "only_for_lot":"common",
  1580	  "only_for_terminal":"common",
  1581	  "topics":[
  1582	   "Банк предоставляет QR-API без гарантий"
  1583	  ],
  1584	  "payment_method":"qr"
  1585	 },
  1586	 {
  1587	  "number":"6.1",
  1588	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → За осуществление расчетов по Операциям оплаты, Предприятие уплачивает Банку плату в размере:\n«(____________) процент от суммы Операций оплат».",
  1589	  "required_type":"mandatory",
  1590	  "main_idea":"Важно",
  1591	  "only_for_product":"common",
  1592	  "only_for_lot":"common",
  1593	  "only_for_terminal":"common",
  1594	  "topics":[
  1595	   "размер платы в процентах от суммы операций"
  1596	  ],
  1597	  "payment_method":"common"
  1598	 },
  1599	 {
  1600	  "number":"6.2",
  1601	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за месяцем оказания услуг (далее – Отчетный месяц), направляет Предприятию Универсальный передаточный документ[2] (далее – УПД) на оплату услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц. \nВознаграждение Банка, установленное п.6.1 Договора, включает НДС по ставке, установленной законодательством Российской Федерации.",
  1602	  "required_type":"mandatory",
  1603	  "main_idea":"УПД - это универсальный передаточный документ (документ о приёмке, документ на оплату услуг). Важно проверить сроки и периодичность оплаты",
  1604	  "only_for_product":"common",
  1605	  "only_for_lot":"common",
  1606	  "only_for_terminal":"common",
  1607	  "topics":[
  1608	   "Банк направляет документ на оплату услуг Банка",
  1609	   "в вознаграждение банка включен НДС по ставке, установленной законом",
  1610	   "Срок направления документа на оплату услуг Банка"
  1611	  ],
  1612	  "payment_method":"common"
  1613	 },
  1614	 {
  1615	  "number":"6.3",
  1616	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за месяцем оказания услуг (далее – Отчетный месяц), направляет Предприятию Акт о перечислении Предприятию сумм операций по картам по форме Приложения 2 к Договору (далее – Акт) и счет ф.363 на оплату услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц.Размер вознаграждения, причитающегося Банку, определяется в соответствии с п.6.1 Договора и не облагается НДС на основании п. 3 ст. 149 Налогового кодекса Российской Федерации.",
  1617	  "required_type":"mandatory",
  1618	  "main_idea":"",
  1619	  "only_for_product":"common",
  1620	  "only_for_lot":"fz_223",
  1621	  "only_for_terminal":"common",
  1622	  "topics":[
  1623	   "Банк направляет Акт до 10 рабочего дня месяца, следующего за отчетным",
  1624	   "Акт направляется вместе со счетом-фактурой формы 363",
  1625	   "Размер вознаграждения определяется согласно пункту 6.1 договора",
  1626	   "Вознаграждение банка не облагается НДС на основании п.3 ст.149 НК РФ",
  1627	   "Срок направления Банком документа на оплату услуг Банка"
  1628	  ],
  1629	  "payment_method":"common"
  1630	 },
  1631	 {
  1632	  "number":"6.4",
  1633	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД либо предоставить мотивированный отказ от подписания УПД.",
  1634	  "required_type":"mandatory",
  1635	  "main_idea":"",
  1636	  "only_for_product":"common",
  1637	  "only_for_lot":"common",
  1638	  "only_for_terminal":"common",
  1639	  "topics":[
  1640	   "Предприятие обязано принять и возвратить УПД (принять оказанные услуги)",
  1641	   "Предприятие предоставляет мотивированный отказ от подписания УПД в установленные сроки"
  1642	  ],
  1643	  "payment_method":"common"
  1644	 },
  1645	 {
  1646	  "number":"6.5",
  1647	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Оплата услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
  1648	  "required_type":"mandatory",
  1649	  "main_idea":"",
  1650	  "only_for_product":"common",
  1651	  "only_for_lot":"common",
  1652	  "only_for_terminal":"common",
  1653	  "topics":[
  1654	   "оплата услуг банка осуществляется в течение 5 рабочих дней после подписания УПД",
  1655	   "форма оплаты - безналичная",
  1656	   "денежные средства перечисляются на счет банка, указанный в УПД"
  1657	  ],
  1658	  "payment_method":"common"
  1659	 },
  1660	 {
  1661	  "number":"6.6",
  1662	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Оплата услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты получения от Банка Акта и счета ф.363 в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в счете ф.363.",
  1663	  "required_type":"mandatory",
  1664	  "main_idea":"",
  1665	  "only_for_product":"common",
  1666	  "only_for_lot":"fz_223",
  1667	  "only_for_terminal":"common",
  1668	  "topics":[
  1669	   "оплата услуг банка осуществляется в течение 5 рабочих дней после получения акта и счета формы 363",
  1670	   "форма оплаты - безналичная",
  1671	   "перечисление средств производится на счет, указанный в счете формы 363"
  1672	  ],
  1673	  "payment_method":"common"
  1674	 },
  1675	 {
  1676	  "number":"6.7",
  1677	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Плата за сервисное обслуживание Электронных терминалов уплачивается Предприятием ежемесячно в размере _____ (__________________) рублей (включая НДС) за каждый Электронный терминал.",
  1678	  "required_type":"mandatory",
  1679	  "main_idea":"",
  1680	  "only_for_product":"trade_acquiring",
  1681	  "only_for_lot":"common",
  1682	  "only_for_terminal":"smart",
  1683	  "topics":[
  1684	   "указан размер платы за сервисное обслуживание Электронного терминала",
  1685	   "указано количество рублей включая НДС",
  1686	   "установлен ежемесячный порядок оплаты"
  1687	  ],
  1688	  "payment_method":"common"
  1689	 },
  1690	 {
  1691	  "number":"6.8",
  1692	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию УПД  на сумму платы за сервисное обслуживание Электронных терминалов за Отчетный месяц.\n",
  1693	  "required_type":"mandatory",
  1694	  "main_idea":"",
  1695	  "only_for_product":"trade_acquiring",
  1696	  "only_for_lot":"common",
  1697	  "only_for_terminal":"smart",
  1698	  "topics":[
  1699	   "Банк направляет УПД не позднее 5 рабочего дня месяца, следующего за отчетным",
  1700	   "УПД направляется на сумму платы за сервисное обслуживание Электронных терминалов"
Tool:    701	      "liability_remedy": "",
   702	      "scope_options": [],
   703	      "consequence": "",
   704	      "applicability_filters": {
   705	        "required_type": "optional",
   706	        "only_for_product": "common",
   707	        "only_for_lot": "common",
   708	        "only_for_terminal": "common",
   709	        "payment_method": "common"
   710	      },
   711	      "main_idea": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования",
   712	      "topics": [
   713	        "закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов",
   714	        "закреплено право Заказчика на получение консультаций по проведению Операций"
   715	      ],
   716	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, указанному в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе."
   717	    },
   718	    {
   719	      "id": "4.1.3",
   720	      "source_text": "Важен сам факт, что QR выдаёт Банк Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Мобильных устройствах Предприятия, а также на ККТ, принадлежащей Предприятию, или на видном месте, в том числе на бумажном носителе.",
   721	      "source_excerpt": "Важен сам факт, что QR выдаёт Банк Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Т",
   722	      "type": "operative",
   723	      "materiality": "needs_source_review",
   724	      "protected_party": "",
   725	      "bound_party": "",
   726	      "right_or_obligation": "",
   727	      "legal_object": "",
   728	      "trigger": "",
   729	      "deadline": "",
   730	      "amount_formula_cap": "",
   731	      "procedure_channel": "",
   732	      "liability_remedy": "",
   733	      "scope_options": [],
   734	      "consequence": "",
   735	      "applicability_filters": {
   736	        "required_type": "optional",
   737	        "only_for_product": "trade_acquiring",
   738	        "only_for_lot": "common",
   739	        "only_for_terminal": "common",
   740	        "payment_method": "qr_sber_pay"
   741	      },
   742	      "main_idea": "Важен сам факт, что QR выдаёт Банк",
   743	      "topics": [
   744	        "Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR"
   745	      ],
   746	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Мобильных устройствах Предприятия, а также на ККТ, принадлежащей Предприятию, или на видном месте, в том числе на бумажном носителе."
   747	    },
   748	    {
   749	      "id": "4.2.1",
   750	      "source_text": "Важен факт, что предприятие обязуется оплачивать услуги Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям; Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настоящего Договора.",
   751	      "source_excerpt": "Важен факт, что предприятие обязуется оплачивать услуги Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям; Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена) «ПРАВА И ОБЯЗАННОС",
   752	      "type": "operative",
   753	      "materiality": "needs_source_review",
   754	      "protected_party": "",
   755	      "bound_party": "",
   756	      "right_or_obligation": "",
   757	      "legal_object": "",
   758	      "trigger": "",
   759	      "deadline": "",
   760	      "amount_formula_cap": "",
   761	      "procedure_channel": "",
   762	      "liability_remedy": "",
   763	      "scope_options": [],
   764	      "consequence": "",
   765	      "applicability_filters": {
   766	        "required_type": "mandatory",
   767	        "only_for_product": "common",
   768	        "only_for_lot": "common",
   769	        "only_for_terminal": "common",
   770	        "payment_method": "common"
   771	      },
   772	      "main_idea": "Важен факт, что предприятие обязуется оплачивать услуги",
   773	      "topics": [
   774	        "Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям",
   775	        "Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена)"
   776	      ],
   777	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настоящего Договора. "
   778	    },
   779	    {
   780	      "id": "4.2.2",
   781	      "source_text": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее нет, то пункты не относятся к теме матрицы Обязанность Предприятия соблюдать положения Договора (наличие формулировки об обязанности соблюдать); Обязанность Предприятия выполнять требования, содержащиеся в информационных / инструктивных материалах, предоставляемых Банком (наличие формулировки об обязанности выполнять) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/ инструктивных материалах, предоставляемых Банком.",
   782	      "source_excerpt": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее ",
   783	      "type": "operative",
   784	      "materiality": "needs_source_review",
   785	      "protected_party": "",
   786	      "bound_party": "",
   787	      "right_or_obligation": "",
   788	      "legal_object": "",
   789	      "trigger": "",
   790	      "deadline": "",
   791	      "amount_formula_cap": "",
   792	      "procedure_channel": "",
   793	      "liability_remedy": "",
   794	      "scope_options": [],
   795	      "consequence": "",
   796	      "applicability_filters": {
   797	        "required_type": "optional",
   798	        "only_for_product": "common",
   799	        "only_for_lot": "common",
   800	        "only_for_terminal": "common",
   801	        "payment_method": "common"
   802	      },
   803	      "main_idea": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее нет, то пункты не относятся к теме матрицы",
   804	      "topics": [
   805	        "Обязанность Предприятия соблюдать положения Договора (наличие формулировки об обязанности соблюдать)",
   806	        "Обязанность Предприятия выполнять требования, содержащиеся в информационных / инструктивных материалах, предоставляемых Банком (наличие формулировки об обязанности выполнять)"
   807	      ],
   808	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/ инструктивных материалах, предоставляемых Банком."
   809	    },
   810	    {
   811	      "id": "4.2.3",
   812	      "source_text": "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов; Несвоевременное ознакомление не является основанием для неприменения изменений «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление Предприятия с изменениями, внесенными в вышеуказанные документы, не является основанием для их неприменения Банком.",
   813	      "source_excerpt": "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов; Несвоевременное ознакомление не является основанием для неприменения изменений «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятель",
   814	      "type": "operative",
   815	      "materiality": "needs_source_review",
   816	      "protected_party": "",
   817	      "bound_party": "",
   818	      "right_or_obligation": "",
   819	      "legal_object": "",
   820	      "trigger": "",
   821	      "deadline": "",
   822	      "amount_formula_cap": "",
   823	      "procedure_channel": "",
   824	      "liability_remedy": "",
   825	      "scope_options": [],
   826	      "consequence": "",
   827	      "applicability_filters": {
   828	        "required_type": "optional",
   829	        "only_for_product": "common",
   830	        "only_for_lot": "fz_223",
   831	        "only_for_terminal": "common",
   832	        "payment_method": "common"
   833	      },
   834	      "main_idea": "",
   835	      "topics": [
   836	        "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов",
   837	        "Несвоевременное ознакомление не является основанием для неприменения изменений"
   838	      ],
   839	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление Предприятия с изменениями, внесенными в вышеуказанные документы, не является основанием для их неприменения Банком."
   840	    },
   841	    {
   842	      "id": "4.2.4",
   843	      "source_text": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте Предприятие обязано размещать информационные материалы Банка о способах оплаты; Размещение материалов осуществляется в случае отсутствия противоречий с законодательством РФ «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с использованием Карт/NFC-карт/SberPay/Плати QR, в случае если это не противоречит требованиям законодательства Российской Федерации.",
   844	      "source_excerpt": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте Предприятие обязано размещать ",
   845	      "type": "operative",
   846	      "materiality": "needs_source_review",
   847	      "protected_party": "",
   848	      "bound_party": "",
   849	      "right_or_obligation": "",
   850	      "legal_object": "",
   851	      "trigger": "",
   852	      "deadline": "",
   853	      "amount_formula_cap": "",
   854	      "procedure_channel": "",
   855	      "liability_remedy": "",
   856	      "scope_options": [],
   857	      "consequence": "",
   858	      "applicability_filters": {
   859	        "required_type": "optional",
   860	        "only_for_product": "common",
   861	        "only_for_lot": "common",
   862	        "only_for_terminal": "common",
   863	        "payment_method": "common"
   864	      },
   865	      "main_idea": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте",
   866	      "topics": [
   867	        "Предприятие обязано размещать информационные материалы Банка о способах оплаты",
   868	        "Размещение материалов осуществляется в случае отсутствия противоречий с законодательством РФ"
   869	      ],
   870	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с использованием Карт/NFC-карт/SberPay/Плати QR, в случае если это не противоречит требованиям законодательства Российской Федерации."
   871	    },
   872	    {
   873	      "id": "4.2.5",
   874	      "source_text": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства Принимать к оплате все карты из списка в течение всего рабочего времени; Не выдавать наличные деньги по картам; Не принимать более двух разных карт от одного покупателя «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, в течение всего рабочего времени Предприятия. Не выдавать по Картам наличные денежные средства[3]. Не принимать от Покупателя более 2 (двух) различных Карт.",
   875	      "source_excerpt": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства Принимать к оплате все карты из списка в течение всего рабочего времени; Не выдавать наличные деньги по картам; Не принимать более двух ",
   876	      "type": "operative",
   877	      "materiality": "needs_source_review",
   878	      "protected_party": "",
   879	      "bound_party": "",
   880	      "right_or_obligation": "",
   881	      "legal_object": "",
   882	      "trigger": "",
   883	      "deadline": "",
   884	      "amount_formula_cap": "",
   885	      "procedure_channel": "",
   886	      "liability_remedy": "",
   887	      "scope_options": [],
   888	      "consequence": "",
   889	      "applicability_filters": {
   890	        "required_type": "mandatory",
   891	        "only_for_product": "common",
   892	        "only_for_lot": "common",
   893	        "only_for_terminal": "common",
   894	        "payment_method": "common"
   895	      },
   896	      "main_idea": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства",
   897	      "topics": [
   898	        "Принимать к оплате все карты из списка в течение всего рабочего времени",
   899	        "Не выдавать наличные деньги по картам",
   900	        "Не принимать более двух разных карт от одного покупателя"
   901	      ],
   902	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, в течение всего рабочего времени Предприятия. Не выдавать по Картам наличные денежные средства[3]. Не принимать от Покупателя более 2 (двух) различных Карт."
   903	    },
   904	    {
   905	      "id": "4.2.6",
   906	      "source_text": "Важен сам факт, что нельзя разбивать Операцию на нескольку сумм Предприятие обязано проводить Операцию оплаты единой суммой без разделения на части «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм.",
   907	      "source_excerpt": "Важен сам факт, что нельзя разбивать Операцию на нескольку сумм Предприятие обязано проводить Операцию оплаты единой суммой без разделения на части «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не разбивать сумму одной Операц",
   908	      "type": "operative",
   909	      "materiality": "needs_source_review",
   910	      "protected_party": "",
   911	      "bound_party": "",
   912	      "right_or_obligation": "",
   913	      "legal_object": "",
   914	      "trigger": "",
   915	      "deadline": "",
   916	      "amount_formula_cap": "",
   917	      "procedure_channel": "",
   918	      "liability_remedy": "",
   919	      "scope_options": [],
   920	      "consequence": "",
   921	      "applicability_filters": {
   922	        "required_type": "mandatory",
   923	        "only_for_product": "common",
   924	        "only_for_lot": "common",
   925	        "only_for_terminal": "common",
   926	        "payment_method": "common"
   927	      },
   928	      "main_idea": "Важен сам факт, что нельзя разбивать Операцию на нескольку сумм",
   929	      "topics": [
   930	        "Предприятие обязано проводить Операцию оплаты единой суммой без разделения на части"
   931	      ],
   932	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм."
   933	    },
   934	    {
   935	      "id": "4.2.7",
   936	      "source_text": "Не использовать реквизиты Карты без присутствия или распоряжения Покупателя; Использовать реквизиты Карты только для проведения операций «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не использовать реквизиты Карты/Платежного счета, которые стали доступны Предприятию/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупателя.",
   937	      "source_excerpt": "Не использовать реквизиты Карты без присутствия или распоряжения Покупателя; Использовать реквизиты Карты только для проведения операций «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не использовать реквизиты Карты/Платежного",
   938	      "type": "operative",
   939	      "materiality": "needs_source_review",
   940	      "protected_party": "",
   941	      "bound_party": "",
   942	      "right_or_obligation": "",
   943	      "legal_object": "",
   944	      "trigger": "",
   945	      "deadline": "",
   946	      "amount_formula_cap": "",
   947	      "procedure_channel": "",
   948	      "liability_remedy": "",
   949	      "scope_options": [],
   950	      "consequence": "",
   951	      "applicability_filters": {
   952	        "required_type": "mandatory",
   953	        "only_for_product": "common",
   954	        "only_for_lot": "common",
   955	        "only_for_terminal": "common",
   956	        "payment_method": "common"
   957	      },
   958	      "main_idea": "",
   959	      "topics": [
   960	        "Не использовать реквизиты Карты без присутствия или распоряжения Покупателя",
   961	        "Использовать реквизиты Карты только для проведения операций"
   962	      ],
   963	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не использовать реквизиты Карты/Платежного счета, которые стали доступны Предприятию/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупателя."
   964	    },
   965	    {
   966	      "id": "4.2.8",
   967	      "source_text": "Важно, что цена не зависит от способа оплаты Предприятие предоставляет полный набор товаров/услуг покупателям; цены для расчетов с использованием банковской карты не превышают цены за наличный расчет «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства.",
   968	      "source_excerpt": "Важно, что цена не зависит от способа оплаты Предприятие предоставляет полный набор товаров/услуг покупателям; цены для расчетов с использованием банковской карты не превышают цены за наличный расчет «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Пред",
   969	      "type": "operative",
   970	      "materiality": "needs_source_review",
   971	      "protected_party": "",
   972	      "bound_party": "",
   973	      "right_or_obligation": "",
   974	      "legal_object": "",
   975	      "trigger": "",
   976	      "deadline": "",
   977	      "amount_formula_cap": "",
   978	      "procedure_channel": "",
   979	      "liability_remedy": "",
   980	      "scope_options": [],
   981	      "consequence": "",
   982	      "applicability_filters": {
   983	        "required_type": "mandatory",
   984	        "only_for_product": "common",
   985	        "only_for_lot": "common",
   986	        "only_for_terminal": "common",
   987	        "payment_method": "common"
   988	      },
   989	      "main_idea": "Важно, что цена не зависит от способа оплаты",
   990	      "topics": [
   991	        "Предприятие предоставляет полный набор товаров/услуг покупателям",
   992	        "цены для расчетов с использованием банковской карты не превышают цены за наличный расчет"
   993	      ],
   994	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства."
   995	    },
   996	    {
   997	      "id": "4.2.9",
   998	      "source_text": "Заказчик несет ответственность за информацию которую он указывает в документах при проведении платежей Предприятие обязано проводить операции в соответствии с Порядком проведения операций; Предприятие обязано оформлять документы по операциям в соответствии с Порядком проведения операций; Предприятие несет ответственность за корректность информации в документах по операциям «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций в Торгово-сервисных точках/на Ресурсе к Договору и нести ответственность за правильность указанной в документах информации.",
   999	      "source_excerpt": "Заказчик несет ответственность за информацию которую он указывает в документах при проведении платежей Предприятие обязано проводить операции в соответствии с Порядком проведения операций; Предприятие обязано оформлять документы по операция",
  1000	      "type": "operative",
  1001	      "materiality": "needs_source_review",
  1002	      "protected_party": "",
  1003	      "bound_party": "",
  1004	      "right_or_obligation": "",
  1005	      "legal_object": "",
  1006	      "trigger": "",
  1007	      "deadline": "",
  1008	      "amount_formula_cap": "",
  1009	      "procedure_channel": "",
  1010	      "liability_remedy": "",
  1011	      "scope_options": [],
  1012	      "consequence": "",
  1013	      "applicability_filters": {
  1014	        "required_type": "mandatory",
  1015	        "only_for_product": "common",
  1016	        "only_for_lot": "common",
  1017	        "only_for_terminal": "common",
  1018	        "payment_method": "common"
  1019	      },
  1020	      "main_idea": "Заказчик несет ответственность за информацию которую он указывает в документах при проведении платежей",
  1021	      "topics": [
  1022	        "Предприятие обязано проводить операции в соответствии с Порядком проведения операций",
  1023	        "Предприятие обязано оформлять документы по операциям в соответствии с Порядком проведения операций",
  1024	        "Предприятие несет ответственность за корректность информации в документах по операциям"
  1025	      ],
  1026	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций в Торгово-сервисных точках/на Ресурсе к Договору и нести ответственность за правильность указанной в документах информации."
  1027	    },
  1028	    {
  1029	      "id": "4.2.10",
  1030	      "source_text": "Важен факт необходимости хранения документы по операциям, срок в течении которого их нужно хранить, факт передачи копий по опревцияс, а так же срок в течение которого обязаны их передать хранение документов по операциям (сам факт хранения и срок храннеия); передача копий документов Банку в течение 3 рабочих дней; надлежащее качество предоставленных документов «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Хранить в недоступном для третьих лиц месте Документы по операциям (Чеки, кассовые чеки, распоряжения Покупателя, документы, подтверждающие факт заключения договора и проведения каждой Операции при проведении Повторяющихся платежей, документы, подтверждающие факт передачи Товара/оказания услуги и т.п.) не менее 13 (тринадцати) месяцев с даты совершения Операции и передавать их копии в Банк по его запросу путем направления ответа на первоначальный запрос по электронным каналам связи, указанным в п.2.3.1., п.2.3.2. Договора в течение 3 (трех) рабочих дней с даты получения запроса. Предоставленные документы должны быть надлежащего качества (изображение четкое, размер не менее оригинального документа).",
  1031	      "source_excerpt": "Важен факт необходимости хранения документы по операциям, срок в течении которого их нужно хранить, факт передачи копий по опревцияс, а так же срок в течение которого обязаны их передать хранение документов по операциям (сам факт хранения и",
  1032	      "type": "operative",
  1033	      "materiality": "needs_source_review",
  1034	      "protected_party": "",
  1035	      "bound_party": "",
  1036	      "right_or_obligation": "",
  1037	      "legal_object": "",
  1038	      "trigger": "",
  1039	      "deadline": "",
  1040	      "amount_formula_cap": "",
  1041	      "procedure_channel": "",
  1042	      "liability_remedy": "",
  1043	      "scope_options": [],
  1044	      "consequence": "",
  1045	      "applicability_filters": {
  1046	        "required_type": "mandatory",
  1047	        "only_for_product": "common",
  1048	        "only_for_lot": "common",
  1049	        "only_for_terminal": "common",
  1050	        "payment_method": "common"
  1051	      },
  1052	      "main_idea": "Важен факт необходимости хранения документы по операциям, срок в течении которого их нужно хранить, факт передачи копий по опревцияс, а так же срок в течение которого обязаны их передать",
  1053	      "topics": [
  1054	        "хранение документов по операциям (сам факт хранения и срок храннеия)",
  1055	        "передача копий документов Банку в течение 3 рабочих дней",
  1056	        "надлежащее качество предоставленных документов"
  1057	      ],
  1058	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Хранить в недоступном для третьих лиц месте Документы по операциям (Чеки, кассовые чеки, распоряжения Покупателя, документы, подтверждающие факт заключения договора и проведения каждой Операции при проведении Повторяющихся платежей, документы, подтверждающие факт передачи Товара/оказания услуги и т.п.) не менее 13 (тринадцати) месяцев с даты совершения Операции и передавать их копии в Банк по его запросу путем направления ответа на первоначальный запрос по электронным каналам связи, указанным в п.2.3.1., п.2.3.2. Договора в течение 3 (трех) рабочих дней с даты получения запроса. Предоставленные документы должны быть надлежащего качества (изображение четкое, размер не менее оригинального документа). "
  1059	    },
  1060	    {
  1061	      "id": "4.2.11",
  1062	      "source_text": "Важен факт обязанности передавать заявление Банку, а так же сроки в течение которых оно должно быть передано Передача заявления в банк с изложением обстоятельств проведения Операции в течение 3 рабочих дней после получения запроса; немедленное уведомление банка об утрате документов «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Передавать в Банк по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Банка письменное заявление с изложением обстоятельств проведения Операции в ТСТ /на Ресурсе . В случае утраты составленных Документов по операции немедленно сообщить об утрате в Банк одним из способов, указанных в п. 2.3.1, п. 2.3.2 Договора.",
  1063	      "source_excerpt": "Важен факт обязанности передавать заявление Банку, а так же сроки в течение которых оно должно быть передано Передача заявления в банк с изложением обстоятельств проведения Операции в течение 3 рабочих дней после получения запроса; немедлен",
  1064	      "type": "operative",
  1065	      "materiality": "needs_source_review",
  1066	      "protected_party": "",
  1067	      "bound_party": "",
  1068	      "right_or_obligation": "",
  1069	      "legal_object": "",
  1070	      "trigger": "",
  1071	      "deadline": "",
  1072	      "amount_formula_cap": "",
  1073	      "procedure_channel": "",
  1074	      "liability_remedy": "",
  1075	      "scope_options": [],
  1076	      "consequence": "",
  1077	      "applicability_filters": {
  1078	        "required_type": "mandatory",
  1079	        "only_for_product": "common",
  1080	        "only_for_lot": "common",
  1081	        "only_for_terminal": "common",
  1082	        "payment_method": "common"
  1083	      },
  1084	      "main_idea": "Важен факт обязанности передавать заявление Банку, а так же сроки в течение которых оно должно быть передано",
  1085	      "topics": [
  1086	        "Передача заявления в банк с изложением обстоятельств проведения Операции в течение 3 рабочих дней после получения запроса",
  1087	        "немедленное уведомление банка об утрате документов"
  1088	      ],
  1089	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Передавать в Банк по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Банка письменное заявление с изложением обстоятельств проведения Операции в ТСТ /на Ресурсе . В случае утраты составленных Документов по операции немедленно сообщить об утрате в Банк одним из способов, указанных в п. 2.3.1, п. 2.3.2 Договора. "
  1090	    },
  1091	    {
  1092	      "id": "4.2.12",
  1093	      "source_text": "Важен факт обязанности Предприятия подписать закрывающие документы по оплате, а так же сроки в течение которых оно должно это сделать Предприятие обязано акцептовать платежные требования и счета на оплату. Пункт относится только к оплате счетов; Срок оплаты платежных требований и счетов «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг, в течение 5 (пяти) рабочих дней с даты их выставления.",
  1094	      "source_excerpt": "Важен факт обязанности Предприятия подписать закрывающие документы по оплате, а так же сроки в течение которых оно должно это сделать Предприятие обязано акцептовать платежные требования и счета на оплату. Пункт относится только к оплате сч",
  1095	      "type": "operative",
  1096	      "materiality": "needs_source_review",
  1097	      "protected_party": "",
  1098	      "bound_party": "",
  1099	      "right_or_obligation": "",
  1100	      "legal_object": "",
  1101	      "trigger": "",
  1102	      "deadline": "",
  1103	      "amount_formula_cap": "",
  1104	      "procedure_channel": "",
  1105	      "liability_remedy": "",
  1106	      "scope_options": [],
  1107	      "consequence": "",
  1108	      "applicability_filters": {
  1109	        "required_type": "optional",
  1110	        "only_for_product": "common",
  1111	        "only_for_lot": "common",
  1112	        "only_for_terminal": "common",
  1113	        "payment_method": "common"
  1114	      },
  1115	      "main_idea": "Важен факт обязанности Предприятия подписать закрывающие документы по оплате, а так же сроки в течение которых оно должно это сделать",
  1116	      "topics": [
  1117	        "Предприятие обязано акцептовать платежные требования и счета на оплату. Пункт относится только к оплате счетов",
  1118	        "Срок оплаты платежных требований и счетов"
  1119	      ],
  1120	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг, в течение 5 (пяти) рабочих дней с даты их выставления."
  1121	    },
  1122	    {
  1123	      "id": "4.2.13",
  1124	      "source_text": "Важен сам факт обязанности Предприятия возмещать все суммы и убытки, которые Банк понёс из-за Предприятия, все возмещения - в полном объеме. Сранвнить случаи в которых возникает обязанность в возмещении возмещение средств, списанных со счета Банка в пользу Банка-эмитента или Держателей карт; возмещение средств, уплаченных Банком Банку-эмитенту или Держателям карт; возмещение средств при спорах и разногласиях по операциям; возмещение сборов, комиссий и расходов Банка при рассмотрении споров; возмещение убытков Банка от штрафных санкций и ответственности «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере: • средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка в пользу Банка-эмитента либо уплачены Банком Банку-эмитенту и (или) Держателям карт, эмитированных Банком, по Операциям : - ставшим предметом каких-либо споров и разногласий в соответствии с законодательством Российской Федерации и (или) в соответствии с правилами Платежной системы; - являющимся недействительными в соответствии с Договором; • средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка либо уплачены Банком в связи с рассмотрением споров и разногласий между Покупателями и Предприятием касательно Операций, указанных в настоящем пункте Договора, в том числе любые сборы, комиссии, платы и (или) иные расходы Банка, связанные с рассмотрением споров и разногласий по таким Операциям; • убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с законодательством Российской Федерации и (или) правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору.",
  1125	      "source_excerpt": "Важен сам факт обязанности Предприятия возмещать все суммы и убытки, которые Банк понёс из-за Предприятия, все возмещения - в полном объеме. Сранвнить случаи в которых возникает обязанность в возмещении возмещение средств, списанных со счет",
  1126	      "type": "operative",
  1127	      "materiality": "needs_source_review",
  1128	      "protected_party": "",
  1129	      "bound_party": "",
  1130	      "right_or_obligation": "",
  1131	      "legal_object": "",
  1132	      "trigger": "",
  1133	      "deadline": "",
  1134	      "amount_formula_cap": "",
  1135	      "procedure_channel": "",
  1136	      "liability_remedy": "",
  1137	      "scope_options": [],
  1138	      "consequence": "",
  1139	      "applicability_filters": {
  1140	        "required_type": "mandatory",
  1141	        "only_for_product": "common",
  1142	        "only_for_lot": "common",
  1143	        "only_for_terminal": "common",
  1144	        "payment_method": "common"
  1145	      },
  1146	      "main_idea": "Важен сам факт обязанности Предприятия возмещать все суммы и убытки, которые Банк понёс из-за Предприятия, все возмещения - в полном объеме. Сранвнить случаи в которых возникает обязанность в возмещении",
  1147	      "topics": [
  1148	        "возмещение средств, списанных со счета Банка в пользу Банка-эмитента или Держателей карт",
  1149	        "возмещение средств, уплаченных Банком Банку-эмитенту или Держателям карт",
  1150	        "возмещение средств при спорах и разногласиях по операциям",
  1151	        "возмещение сборов, комиссий и расходов Банка при рассмотрении споров",
  1152	        "возмещение убытков Банка от штрафных санкций и ответственности"
  1153	      ],
  1154	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере:\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка в пользу Банка-эмитента либо уплачены Банком Банку-эмитенту и (или) Держателям карт, эмитированных Банком, по Операциям :\n- ставшим предметом каких-либо споров и разногласий в соответствии с законодательством Российской Федерации и (или) в соответствии с правилами Платежной системы;\n- являющимся недействительными в соответствии с Договором;\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка либо уплачены Банком в связи с рассмотрением споров и разногласий между Покупателями и Предприятием касательно Операций, указанных в настоящем пункте Договора, в том числе любые сборы, комиссии, платы и (или) иные расходы Банка, связанные с рассмотрением споров и разногласий по таким Операциям;\n• убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с законодательством Российской Федерации и (или) правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору."
  1155	    },
  1156	    {
  1157	      "id": "4.2.14",
  1158	      "source_text": "Важен факт предоставления подтверждающих документов, важны сроки предоставления, а так же нужно сравнить события, при которых это допустимо информирование Банка о реорганизации предприятия в течение 3 рабочих дней; уведомление об изменениях документов в течение 3 рабочих дней; сообщение об открытии или смене стадии банкротства в течение 3 рабочих дней; предоставление сведений о смене руководства в течение 3 рабочих дней; оповещение об изменении адреса нахождения в течение 3 рабочих дней; передача информации об изменении реквизитов в течение 3 рабочих дней «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В случае реорганизации, внесения изменений и дополнений в документы, представленные Предприятием при заключении Договора, при открытии в отношении Предприятия/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса местонахождения Предприятия/ТСТ, внесенного в ЕГРЮЛ, реквизитов Предприятие/ТСТ обязуется информировать Банк и передать (по месту заключения Договора) надлежащим образом заверенные и оформленные документы, подтверждающие внесение изменений и дополнений одним из способов, указанных в п. 2.3 Договора, не позднее 3 (трех) рабочих дней с даты дополнений/изменений.",
  1159	      "source_excerpt": "Важен факт предоставления подтверждающих документов, важны сроки предоставления, а так же нужно сравнить события, при которых это допустимо информирование Банка о реорганизации предприятия в течение 3 рабочих дней; уведомление об изменениях",
  1160	      "type": "operative",
  1161	      "materiality": "needs_source_review",
  1162	      "protected_party": "",
  1163	      "bound_party": "",
  1164	      "right_or_obligation": "",
  1165	      "legal_object": "",
  1166	      "trigger": "",
  1167	      "deadline": "",
  1168	      "amount_formula_cap": "",
  1169	      "procedure_channel": "",
  1170	      "liability_remedy": "",
  1171	      "scope_options": [],
  1172	      "consequence": "",
  1173	      "applicability_filters": {
  1174	        "required_type": "mandatory",
  1175	        "only_for_product": "common",
  1176	        "only_for_lot": "common",
  1177	        "only_for_terminal": "common",
  1178	        "payment_method": "common"
  1179	      },
  1180	      "main_idea": "Важен факт предоставления подтверждающих документов, важны сроки предоставления, а так же нужно сравнить события, при которых это допустимо",
  1181	      "topics": [
  1182	        "информирование Банка о реорганизации предприятия в течение 3 рабочих дней",
  1183	        "уведомление об изменениях документов в течение 3 рабочих дней",
  1184	        "сообщение об открытии или смене стадии банкротства в течение 3 рабочих дней",
  1185	        "предоставление сведений о смене руководства в течение 3 рабочих дней",
  1186	        "оповещение об изменении адреса нахождения в течение 3 рабочих дней",
  1187	        "передача информации об изменении реквизитов в течение 3 рабочих дней"
  1188	      ],
  1189	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В случае реорганизации, внесения изменений и дополнений в документы, представленные Предприятием при заключении Договора, при открытии в отношении Предприятия/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса местонахождения Предприятия/ТСТ, внесенного в ЕГРЮЛ, реквизитов Предприятие/ТСТ обязуется информировать Банк и передать (по месту заключения Договора) надлежащим образом заверенные и оформленные документы, подтверждающие внесение изменений и дополнений одним из способов, указанных в п. 2.3 Договора, не позднее 3 (трех) рабочих дней с даты дополнений/изменений. "
  1190	    },
  1191	    {
  1192	      "id": "4.2.15",
  1193	      "source_text": "Важен факт необходимости предоставлять достоверные сведения, своевременное обновление сведений. Важен факт и срок периодичного предоставления. Важен факт и срок предоставления по запросу Предприятие обязано предоставлять документы не реже одного раза в год; Предприятие обязано предоставлять сведения по запросу Банка в течение 7 рабочих дней; Сведения о целях финансово-хозяйственной деятельности; Информация о финансовом положении предприятия; Данные о деловой репутации предприятия; Сведения о представителях предприятия; Информация о выгодоприобретателях; Сведения о бенефициарных владельцах (если имеются) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять в Банк достоверные документы и сведения, необходимые Банку для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе, но не исключительно: не реже одного раза в год, а также по отдельному запросу Банка в течение 7 (семи) рабочих дней со дня получения запроса обновлять сведения и документы, представленные Банку при заключении настоящего Договора, включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации Предприятия, а также сведения о своих представителях, выгодоприобретателях и бенефициарных владельцах (при наличии).",
  1194	      "source_excerpt": "Важен факт необходимости предоставлять достоверные сведения, своевременное обновление сведений. Важен факт и срок периодичного предоставления. Важен факт и срок предоставления по запросу Предприятие обязано предоставлять документы не реже о",
  1195	      "type": "operative",
  1196	      "materiality": "needs_source_review",
  1197	      "protected_party": "",
  1198	      "bound_party": "",
  1199	      "right_or_obligation": "",
  1200	      "legal_object": "",
AI: I now have a comprehensive view of the data. Let me read the remaining matrix items and the rest of the legal propositions to complete my understanding, then proceed to the contract-only analysis.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 1700, 'limit': 500}, 'id': 'call_00_uLqpDhht8VUaZ0ZDNtsE0584', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 1200, 'limit': 500}, 'id': 'call_01_stXEiJiCYh4eXiCmoXFZ2924', 'type': 'tool_call'}]
Tool:   1701	  ],
  1702	  "payment_method":"common"
  1703	 },
  1704	 {
  1705	  "number":"6.9",
  1706	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию счет ф.363 на сумму платы за сервисное обслуживание Электронных терминалов за Отчетный месяц.\nСчет-фактура предоставляется Банком в порядке и сроки, установленные действующим налоговым законодательством Российской Федерации",
  1707	  "required_type":"mandatory",
  1708	  "main_idea":"",
  1709	  "only_for_product":"trade_acquiring",
  1710	  "only_for_lot":"fz_223",
  1711	  "only_for_terminal":"smart",
  1712	  "topics":[
  1713	   "Банк выставляет счет не позднее 10 рабочего дня месяца, следующего за отчетным",
  1714	   "Счет выставляется по форме №363",
  1715	   "Счет содержит сумму платы за сервисное обслуживание Электронных терминалов",
  1716	   "Счет-фактура предоставляется в соответствии с налоговым законодательством РФ"
  1717	  ],
  1718	  "payment_method":"common"
  1719	 },
  1720	 {
  1721	  "number":"6.10",
  1722	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД на сумму платы за сервисное обслуживание Электронных терминалов за Отчетный месяц либо предоставить мотивированный отказ от подписания УПД.",
  1723	  "required_type":"mandatory",
  1724	  "main_idea":"",
  1725	  "only_for_product":"trade_acquiring",
  1726	  "only_for_lot":"common",
  1727	  "only_for_terminal":"smart",
  1728	  "topics":[
  1729	   "Предприятие возвращает подписанный УПД не позднее 25 числа месяца, следующего за отчетным",
  1730	   "Предприятие предоставляет мотивированный отказ от подписания УПД в указанные сроки"
  1731	  ],
  1732	  "payment_method":"common"
  1733	 },
  1734	 {
  1735	  "number":"6.11",
  1736	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Электронных терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
  1737	  "required_type":"mandatory",
  1738	  "main_idea":"",
  1739	  "only_for_product":"trade_acquiring",
  1740	  "only_for_lot":"common",
  1741	  "only_for_terminal":"smart",
  1742	  "topics":[
  1743	   "оплата за сервисное обслуживание Электронных терминалов производится в течение 5 рабочих дней",
  1744	   "способ оплаты - безналичная форма",
  1745	   "деньги перечисляются на счет Банка, указанный в УПД"
  1746	  ],
  1747	  "payment_method":"common"
  1748	 },
  1749	 {
  1750	  "number":"6.12",
  1751	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Электронных терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты получения от Банка счета ф.363 в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в счете ф.363.",
  1752	  "required_type":"mandatory",
  1753	  "main_idea":"",
  1754	  "only_for_product":"trade_acquiring",
  1755	  "only_for_lot":"fz_223",
  1756	  "only_for_terminal":"smart",
  1757	  "topics":[
  1758	   "Оплата производится в течение 5 рабочих дней",
  1759	   "Способ оплаты - безналичный перевод",
  1760	   "Основание для оплаты - счет формы 363",
  1761	   "Получатель платежа - счет Банка, указанный в счете"
  1762	  ],
  1763	  "payment_method":"common"
  1764	 },
  1765	 {
  1766	  "number":"6.13",
  1767	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Плата за сервисное обслуживание Смарт-терминалов уплачивается Предприятием ежемесячно за каждый Смарт-терминал в соответствии с тарифом, установленным при заключении Договора в Приложении 1.1 к Договору. При этом расчет платы осуществляется пропорционально количеству календарных дней месяца с даты установки Смарт-терминала в ТСТ. При подключении\/отключении 2D сканера размер платы за Смарт-терминал пересчитывается за Отчетный месяц независимо от даты установки\/снятия сканера:\n           - в размере _____ (__________________) рублей (включая НДС) за каждый Смарт-терминал;",
  1768	  "required_type":"mandatory",
  1769	  "main_idea":"",
  1770	  "only_for_product":"trade_acquiring",
  1771	  "only_for_lot":"common",
  1772	  "only_for_terminal":"smart",
  1773	  "topics":[
  1774	   "плата за сервисное обслуживание Смарт-терминалов ежемесячная",
  1775	   "расчет платы пропорционально дням месяца с даты установки терминала",
  1776	   "пересчет платы при подключении\/отключении 2D сканера за отчетный месяц",
  1777	   "указана точная стоимость обслуживания"
  1778	  ],
  1779	  "payment_method":"common"
  1780	 },
  1781	 {
  1782	  "number":"6.14",
  1783	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию УПД  на сумму платы за сервисное обслуживание Смарт-терминалов за Отчетный месяц.",
  1784	  "required_type":"mandatory",
  1785	  "main_idea":"",
  1786	  "only_for_product":"trade_acquiring",
  1787	  "only_for_lot":"common",
  1788	  "only_for_terminal":"smart",
  1789	  "topics":[
  1790	   "Банк направляет УПД не позднее 5 рабочего дня месяца, следующего за отчетным",
  1791	   "УПД направляется на сумму платы за сервисное обслуживание Смарт-терминалов"
  1792	  ],
  1793	  "payment_method":"common"
  1794	 },
  1795	 {
  1796	  "number":"6.15",
  1797	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию счет ф.363 на сумму платы за сервисное обслуживание Смарт-терминалов за Отчетный месяц.\nСчет-фактура предоставляется Банком в порядке и сроки, установленные действующим налоговым законодательством Российской Федерации.",
  1798	  "required_type":"mandatory",
  1799	  "main_idea":"",
  1800	  "only_for_product":"trade_acquiring",
  1801	  "only_for_lot":"fz_223",
  1802	  "only_for_terminal":"smart",
  1803	  "topics":[
  1804	   "Банк выставляет счет не позднее 10 рабочего дня месяца, следующего за отчетным",
  1805	   "Счет-фактура предоставляется в соответствии с налоговым законодательством РФ"
  1806	  ],
  1807	  "payment_method":"common"
  1808	 },
  1809	 {
  1810	  "number":"6.16",
  1811	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД на сумму платы за сервисное обслуживание Смарт-терминалов за Отчетный месяц либо предоставить мотивированный отказ от подписания УПД.",
  1812	  "required_type":"mandatory",
  1813	  "main_idea":"",
  1814	  "only_for_product":"trade_acquiring",
  1815	  "only_for_lot":"common",
  1816	  "only_for_terminal":"smart",
  1817	  "topics":[
  1818	   "Предприятие возвращает подписанный УПД не позднее 25 числа месяца, следующего за отчетным",
  1819	   "Предприятие предоставляет мотивированный отказ от подписания УПД в установленные сроки"
  1820	  ],
  1821	  "payment_method":"common"
  1822	 },
  1823	 {
  1824	  "number":"6.17",
  1825	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Смарт-терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
  1826	  "required_type":"mandatory",
  1827	  "main_idea":"",
  1828	  "only_for_product":"trade_acquiring",
  1829	  "only_for_lot":"common",
  1830	  "only_for_terminal":"smart",
  1831	  "topics":[
  1832	   "оплата сервиса Смарт-терминалов осуществляется в течение 5 рабочих дней после подписания УПД",
  1833	   "форма оплаты - безналичная",
  1834	   "деньги перечисляются на счет Банка, указанный в УПД"
  1835	  ],
  1836	  "payment_method":"common"
  1837	 },
  1838	 {
  1839	  "number":"6.18",
  1840	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Смарт-терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты получения от Банка счета ф.363 в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в счете ф.363",
  1841	  "required_type":"mandatory",
  1842	  "main_idea":"",
  1843	  "only_for_product":"trade_acquiring",
  1844	  "only_for_lot":"fz_223",
  1845	  "only_for_terminal":"smart",
  1846	  "topics":[
  1847	   "оплата производится в течение 5 рабочих дней",
  1848	   "способ оплаты - безналичный перевод",
  1849	   "основание для оплаты - счет формы 363",
  1850	   "срок оплаты считается с даты получения счета"
  1851	  ],
  1852	  "payment_method":"common"
  1853	 },
  1854	 {
  1855	  "number":"6.20",
  1856	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → По Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается. В этом случае плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается.",
  1857	  "required_type":"mandatory",
  1858	  "main_idea":"Важен сам факт, что Банк не берёт новую комиссию, а так же, что первоначальная комиссия не возвращается",
  1859	  "only_for_product":"common",
  1860	  "only_for_lot":"common",
  1861	  "only_for_terminal":"common",
  1862	  "topics":[
  1863	   "плата за проведение расчетов по операциям возврата не взимается",
  1864	   "удержанная плата за расчеты при первоначальной операции не возвращается"
  1865	  ],
  1866	  "payment_method":"common"
  1867	 },
  1868	 {
  1869	  "number":"6.21",
  1870	  "enriched_text":"«ОПЛАТА УСЛУГ БАНКА» → Цена Договора составляет _________ (______________________) рублей __ копеек. ( в том числе НДС)",
  1871	  "required_type":"mandatory",
  1872	  "main_idea":"Отсутствие конкретной ценны не является противоречием",
  1873	  "only_for_product":"common",
  1874	  "only_for_lot":"common",
  1875	  "only_for_terminal":"common",
  1876	  "topics":[
  1877	   "Цена договора в рублях",
  1878	   "Указана точная сумма в рублях и копейках",
  1879	   "Упоминание о включении НДС"
  1880	  ],
  1881	  "payment_method":"common"
  1882	 },
  1883	 {
  1884	  "number":"7.1",
  1885	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с условиями Договора и законодательством РФ.",
  1886	  "required_type":"mandatory",
  1887	  "main_idea":"",
  1888	  "only_for_product":"common",
  1889	  "only_for_lot":"common",
  1890	  "only_for_terminal":"common",
  1891	  "topics":[
  1892	   "Общие слова о том, что за неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с условиями Договора",
  1893	   "Общие слова о том, что за неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с законодательством РФ"
  1894	  ],
  1895	  "payment_method":"common"
  1896	 },
  1897	 {
  1898	  "number":"7.2",
  1899	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За каждый факт неисполнения Предприятием обязательств, предусмотренных Договором, за исключением просрочки исполнения обязательств, предусмотренных Договором, размер штрафа устанавливается в следующем порядке:\nа) 1000 рублей, если Цена Договора не превышает 3 млн. рублей (включительно);\nб) 5000 рублей, если Цена Договора составляет от 3 млн. рублей до 50 млн. рублей (включительно);\nв) 10000 рублей, если Цена Договора составляет от 50 млн. рублей до 100 млн. рублей (включительно);\nг) 100000 рублей, если Цена Договора превышает 100 млн. рублей.",
  1900	  "required_type":"mandatory",
  1901	  "main_idea":"Важно, что штраф именно Предприятию, важен размер штрафа",
  1902	  "only_for_product":"common",
  1903	  "only_for_lot":"common",
  1904	  "only_for_terminal":"common",
  1905	  "topics":[
  1906	   "Штраф Предприятию за неисполнение или ненадлежащее исполнение обязательств, за исключением просрочки."
  1907	  ],
  1908	  "payment_method":"common"
  1909	 },
  1910	 {
  1911	  "number":"7.3",
  1912	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Общая сумма начисленных штрафов за ненадлежащее исполнение Предприятием обязательств, предусмотренных Договором, не может превышать цену Договора.",
  1913	  "required_type":"mandatory",
  1914	  "main_idea":"",
  1915	  "only_for_product":"common",
  1916	  "only_for_lot":"common",
  1917	  "only_for_terminal":"common",
  1918	  "topics":[
  1919	   "Общая сумма штрафов за ненадлежащее исполнение Предприятием обязательств не превышает цену договора"
  1920	  ],
  1921	  "payment_method":"common"
  1922	 },
  1923	 {
  1924	  "number":"7.4",
  1925	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → В случае просрочки исполнения Банком обязательств, предусмотренных Договором, а также в иных случаях неисполнения или ненадлежащего исполнения Банком обязательств, предусмотренных Договором, Предприятие направляет Банку требование об уплате неустоек (штрафов, пеней).Пеня начисляется за каждый день просрочки исполнения Банком обязательства, предусмотренного Договором, начиная со дня, следующего после дня истечения установленного Договором срока исполнения обязательства, и устанавливается Договором в размере одной трехсотой действующей на дату уплаты пени ключевой ставки Центрального банка РФ от Цены Договора, уменьшенной на сумму, пропорциональную объему обязательств, предусмотренных Договором и фактически исполненных Банком, за исключением случаев, если законодательством РФ установлен иной порядок начисления пени.   ",
  1926	  "required_type":"mandatory",
  1927	  "main_idea":"",
  1928	  "only_for_product":"common",
  1929	  "only_for_lot":"common",
  1930	  "only_for_terminal":"common",
  1931	  "topics":[
  1932	   "В случае просрочки исполнения Банком обязательств, Предприятие направляет Банку требование об уплате неустоек (штрафов, пеней)",
  1933	   "Штраф Банку. Начисление пени за каждый день просрочки",
  1934	   "Штраф Банку.Определения срока начала начисления пени",
  1935	   "Штраф Банку. Определение размера пени"
  1936	  ],
  1937	  "payment_method":"common"
  1938	 },
  1939	 {
  1940	  "number":"7.5",
  1941	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За каждый факт неисполнения или ненадлежащего исполнения Банком обязательств, предусмотренных Договором, за исключением просрочки исполнения обязательств, предусмотренных Договором, размер штрафа устанавливается в следующем порядке:\nа) 10 процентов Цены Договора в случае, если Цена Договора не превышает 3 млн. рублей;\nб) 5 процентов Цены Договора в случае, если Цена Договора составляет от 3 млн. рублей до 50 млн. рублей (включительно);\nв) 1 процент Цены Договора в случае, если Цена Договора составляет от 50 млн. рублей до 100 млн. рублей (включительно);\nг) 0,5 процента Цены Договора в случае, если Цена Договора составляет от 100 млн. рублей до 500 млн. рублей (включительно);\nд) 0,4 процента Цены Договора в случае, если Цена Договора составляет от 500 млн. рублей до 1 млрд. рублей (включительно);\nе) 0,3 процента Цены Договора в случае, если Цена Договора составляет от 1 млрд. рублей до 2 млрд. рублей (включительно);\nж) 0,25 процента Цены Договора в случае, если Цена Договора составляет от 2 млрд. рублей до 5 млрд. рублей (включительно);\nз) 0,2 процента Цены Договора в случае, если Цена Договора составляет от 5 млрд. рублей до 10 млрд. рублей (включительно);\nи) 0,1 процента Цены Договора в случае, если Цена Договора превышает 10 млрд. рублей.",
  1942	  "required_type":"mandatory",
  1943	  "main_idea":"",
  1944	  "only_for_product":"common",
  1945	  "only_for_lot":"common",
  1946	  "only_for_terminal":"common",
  1947	  "topics":[
  1948	   "Размер штрафа за неисполнение или ненадлежащее исполнение обязательств Банком, за исключением просрочки, имеющих стоимостное выражения в процентах от суммы договора"
  1949	  ],
  1950	  "payment_method":"common"
  1951	 },
  1952	 {
  1953	  "number":"7.6",
  1954	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → За каждый факт неисполнения или ненадлежащего исполнения Банком обязательств, предусмотренных Договором, которое не имеет стоимостного выражения, размер штрафа устанавливается в следующем порядке:\nа) 1000 рублей, если Цена Договора не превышает 3 млн. рублей;\nб) 5000 рублей, если Цена Договора составляет от 3 млн. рублей до 50 млн. рублей (включительно);\nв) 10000 рублей, если Цена Договора составляет от 50 млн. рублей до 100 млн. рублей (включительно);\nг) 100000 рублей, если Цена Договора превышает 100 млн. рублей.",
  1955	  "required_type":"mandatory",
  1956	  "main_idea":"",
  1957	  "only_for_product":"common",
  1958	  "only_for_lot":"common",
  1959	  "only_for_terminal":"common",
  1960	  "topics":[
  1961	   "Размер штрафа за неисполнение или ненадлежащее исполнение обязательств Банком, не имеющего стоимостного выражения"
  1962	  ],
  1963	  "payment_method":"common"
  1964	 },
  1965	 {
  1966	  "number":"7.7",
  1967	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Банком обязательств, предусмотренных Договором, не может превышать Цену Договора",
  1968	  "required_type":"mandatory",
  1969	  "main_idea":"",
  1970	  "only_for_product":"common",
  1971	  "only_for_lot":"common",
  1972	  "only_for_terminal":"common",
  1973	  "topics":[
  1974	   "Общая сумма штрафов за нарушения Банка не превышает цену договора"
  1975	  ],
  1976	  "payment_method":"common"
  1977	 },
  1978	 {
  1979	  "number":"7.8",
  1980	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности по спорам и разногласиям, возникающим между Предприятием и Покупателем во всех случаях, когда такие споры и разногласия не относятся к предмету Договора, а также по спорам в отношении Товаров\/услуг, оплаченных с использованием Карты \/ ее реквизитов \/ NFС-карты \/ SberPay \/ Плати QR \/ Платежного счета.",
  1981	  "required_type":"optional",
  1982	  "main_idea":"Важен факт, что Банк (Исполнитель) не несет ответственности по спорам и разногласиям Предприятия(Заказчика) и Покупателя (клиент Предприятия)",
  1983	  "only_for_product":"common",
  1984	  "only_for_lot":"common",
  1985	  "only_for_terminal":"common",
  1986	  "topics":[
  1987	   "Ответственность Банка (Исполнителя) за споры между Предприятием (Заказчиком) и Покупателем (Клиент Заказчика)"
  1988	  ],
  1989	  "payment_method":"common"
  1990	 },
  1991	 {
  1992	  "number":"7.9",
  1993	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности за задержки перевода денежных средств на счет Предприятия, если задержки произошли не по вине Банка.",
  1994	  "required_type":"optional",
  1995	  "main_idea":"",
  1996	  "only_for_product":"common",
  1997	  "only_for_lot":"common",
  1998	  "only_for_terminal":"common",
  1999	  "topics":[
  2000	   "Банк освобожден от ответственности при задержках переводов без своей вины"
  2001	  ],
  2002	  "payment_method":"common"
  2003	 },
  2004	 {
  2005	  "number":"7.10",
  2006	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности за неисполнение условий Договора, обусловленное действиями или бездействиями третьих лиц, в том числе участниками Платежной системы",
  2007	  "required_type":"optional",
  2008	  "main_idea":"",
  2009	  "only_for_product":"common",
  2010	  "only_for_lot":"common",
  2011	  "only_for_terminal":"common",
  2012	  "topics":[
  2013	   "Банк не несёт ответственность за неисполнение условий Договора в связи с действием и бездействием третьих лиц"
  2014	  ],
  2015	  "payment_method":"common"
  2016	 },
  2017	 {
  2018	  "number":"7.11",
  2019	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности за несвоевременное перечисление сумм Операций по причине проведения расследования Банком при подозрении на проведение Операции с нарушением условий Договора",
  2020	  "required_type":"optional",
  2021	  "main_idea":"",
  2022	  "only_for_product":"common",
  2023	  "only_for_lot":"common",
  2024	  "only_for_terminal":"common",
  2025	  "topics":[
  2026	   "Банк освобождается от ответственности за задержку перечисления средств в случае инициирования им расследования операций"
  2027	  ],
  2028	  "payment_method":"common"
  2029	 },
  2030	 {
  2031	  "number":"7.12",
  2032	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Банк не несет ответственности в случае превышения установленной Цены Договора",
  2033	  "required_type":"optional",
  2034	  "main_idea":"",
  2035	  "only_for_product":"common",
  2036	  "only_for_lot":"common",
  2037	  "only_for_terminal":"common",
  2038	  "topics":[
  2039	   "Общие слова о том, что банк освобожден от ответственности при превышении Цены Договора"
  2040	  ],
  2041	  "payment_method":"common"
  2042	 },
  2043	 {
  2044	  "number":"7.13",
  2045	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие несет ответственность за некорректность проведенных Операций, совершенных на Ресурсе, в случае невыполнения п. 4.2.21.1 Договора",
  2046	  "required_type":"mandatory",
  2047	  "main_idea":"",
  2048	  "only_for_product":"internet_acquiring",
  2049	  "only_for_lot":"common",
  2050	  "only_for_terminal":"common",
  2051	  "topics":[
  2052	   "Предприятие несет ответственность за некорректные операции на Ресурсе"
  2053	  ],
  2054	  "payment_method":"common"
  2055	 },
  2056	 {
  2057	  "number":"7.14",
  2058	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие несет ответственность за все действия, осуществляемые Предприятием\/ТСТ в СПЭП",
  2059	  "required_type":"mandatory",
  2060	  "main_idea":"",
  2061	  "only_for_product":"common",
  2062	  "only_for_lot":"common",
  2063	  "only_for_terminal":"common",
  2064	  "topics":[
  2065	   "Общее утверждение о том, что Предприятие несет ответственность за все действия в СПЭП"
  2066	  ],
  2067	  "payment_method":"common"
  2068	 },
  2069	 {
  2070	  "number":"7.15",
  2071	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие полностью несет ответственность за действия своего персонала, связанные с нарушением условий Договора и инструктивных материалов, предоставленных Банком",
  2072	  "required_type":"mandatory",
  2073	  "main_idea":"Важен сам факт несения ответственности, если в договоре не говорится про несение ответственности за действия персонала, значит этот пункт не относится к данному",
  2074	  "only_for_product":"common",
  2075	  "only_for_lot":"common",
  2076	  "only_for_terminal":"common",
  2077	  "topics":[
  2078	   "Предприятие несет полную ответственность за нарушения персонала условий договора",
  2079	   "Предприятие несет полную ответственность за нарушения персонала инструкций Банка"
  2080	  ],
  2081	  "payment_method":"common"
  2082	 },
  2083	 {
  2084	  "number":"7.16",
  2085	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → При заключении, исполнении, изменении и расторжении Договора Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция» , а также иных действий (бездействия), нарушающих требования применимого законодательства, применимых норм международного права в области противодействия коррупции",
  2086	  "required_type":"mandatory",
  2087	  "main_idea":"",
  2088	  "only_for_product":"common",
  2089	  "only_for_lot":"common",
  2090	  "only_for_terminal":"common",
  2091	  "topics":[
  2092	   "Обязательство не совершать коррупционных и иных противозаконных действий при любых операциях по договору"
  2093	  ],
  2094	  "payment_method":"common"
  2095	 },
  2096	 {
  2097	  "number":"7.17",
  2098	  "enriched_text":"РАЗДЕЛ 7 «ОТВЕТСТВЕННОСТЬ СТОРОН» → Предприятие несет полную финансовую ответственность перед Банком в случае несоответствия проведенных Повторяющихся платежей требованиям законодательства Российской Федерации, в том числе нормативных актов Банка России, правил Платежной системы и (или) Договора",
  2099	  "required_type":"mandatory",
  2100	  "main_idea":"Важно, чтобы  в договоре не было сужения ответственности.",
  2101	  "only_for_product":"common",
  2102	  "only_for_lot":"common",
  2103	  "only_for_terminal":"common",
  2104	  "topics":[
  2105	   "Общие слова про то, что Предприятие несет финансовую ответственность за несоответствие Повторяющихся платежей законодательству РФ",
  2106	   "Общие слова про то, что Предприятие отвечает за соответствие Повторяющихся платежей нормативным актам Банка России",
  2107	   "Общие слова про то, что Предприятие обязано соблюдать правила Платежной системы в части Повторяющихся платежей",
  2108	   "Общие слова про то, что Предприятие несет ответственность за нарушение условий Договора относительно Повторяющихся платежей"
  2109	  ],
  2110	  "payment_method":"common"
  2111	 },
  2112	 {
  2113	  "number":"8.1",
  2114	  "enriched_text":"РАЗДЕЛ 8 «ФОРС-МАЖОРНЫЕ ОБСТОЯТЕЛЬСТВА» → Сторона Договора освобождается от ответственности за частичное или полное неисполнение обязательств по Договору, если это неисполнение явилось следствием обстоятельств непреодолимой силы, возникших в результате обстоятельств чрезвычайного характера, которые сторона не могла ни предвидеть, ни предотвратить разумными мерами. К таким обстоятельствам чрезвычайного характера относятся стихийные бедствия, аварии, пожары, массовые беспорядки, забастовки, революции, военные действия, а также любые другие обстоятельства вне разумного контроля сторон.При возникновении указанных обстоятельств, срок исполнения договорных обязательств соразмерно откладывается на время действия соответствующего обстоятельства.",
  2115	  "required_type":"mandatory",
  2116	  "main_idea":"",
  2117	  "only_for_product":"common",
  2118	  "only_for_lot":"common",
  2119	  "only_for_terminal":"common",
  2120	  "topics":[
  2121	   "описание форс-мажорных обстоятельств как основание для освобождения от ответственности",
  2122	   "перечень конкретных форс-мажорных событий (стихийные бедствия, пожары и т.д.)",
  2123	   "продление срока исполнения договорных обязательств соразмерно времени действия соответствующего обстоятельства"
  2124	  ],
  2125	  "payment_method":"common"
  2126	 },
  2127	 {
  2128	  "number":"8.2",
  2129	  "enriched_text":"РАЗДЕЛ 8 «ФОРС-МАЖОРНЫЕ ОБСТОЯТЕЛЬСТВА» → При наступлении обстоятельств, указанных в п. 8.1 Договора, Сторона, для которой создалась невозможность исполнения ее обязательств по Договору, должна в течение 24 (двадцати четырех) часов известить о них другую Сторону в соответствии с п.2.3 Договора, с обязательным указанием данных о характере обстоятельств, оценку их влияния на возможность исполнения стороной своих обязательств по Договору и предполагаемый срок их исполнения (при наличии такой возможности). При невозможности исполнения обязательств в срок свыше 3-х (трех) месяцев каждая из Сторон имеет право расторгнуть Договор.",
  2130	  "required_type":"mandatory",
  2131	  "main_idea":"",
  2132	  "only_for_product":"common",
  2133	  "only_for_lot":"common",
  2134	  "only_for_terminal":"common",
  2135	  "topics":[
  2136	   "Обязанность уведомления другой стороны при обстоятельствах непреодолимой силы",
  2137	   "Срок уведомления другой стороны при обстоятельствах непреодолимой силы",
  2138	   "указание характера форс-мажорных обстоятельств",
  2139	   "оценка влияния на исполнение обязательств",
  2140	   "предполагаемый срок исполнения при наличии информации",
  2141	   "право на расторжение договора при задержке более 3 месяцев"
  2142	  ],
  2143	  "payment_method":"common"
  2144	 },
  2145	 {
  2146	  "number":"9.1",
  2147	  "enriched_text":"РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Урегулирование споров Сторон совершается в претензионном порядке",
  2148	  "required_type":"mandatory",
  2149	  "main_idea":"",
  2150	  "only_for_product":"common",
  2151	  "only_for_lot":"common",
  2152	  "only_for_terminal":"common",
  2153	  "topics":[
  2154	   "соблюден претензионный порядок урегулирования споров",
  2155	   "указан обязательный досудебный порядок с указанием срока рассмотрения претензий"
  2156	  ],
  2157	  "payment_method":"common"
  2158	 },
  2159	 {
  2160	  "number":"9.2",
  2161	  "enriched_text":"РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Претензии рассматриваются Сторонами в течение 10 (десяти) календарных дней с даты их получения одной из Сторон.",
  2162	  "required_type":"mandatory",
  2163	  "main_idea":"Важен срок рассмотрения претензий",
  2164	  "only_for_product":"common",
  2165	  "only_for_lot":"common",
  2166	  "only_for_terminal":"common",
  2167	  "topics":[
  2168	   "Срок рассмотрения претензий"
  2169	  ],
  2170	  "payment_method":"common"
  2171	 },
  2172	 {
  2173	  "number":"9.3",
  2174	  "enriched_text":"РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Споры, не урегулированные в претензионном порядке, подлежат разрешению в соответствии с действующим законодательством РФ.",
  2175	  "required_type":"mandatory",
  2176	  "main_idea":"",
  2177	  "only_for_product":"common",
  2178	  "only_for_lot":"common",
  2179	  "only_for_terminal":"common",
  2180	  "topics":[
  2181	
  2182	  ],
  2183	  "payment_method":"common"
  2184	 },
  2185	 {
  2186	  "number":"10.1",
  2187	  "enriched_text":"РАЗДЕЛ 10 «СРОК ДЕЙСТВИЯ ДОГОВОРА И ПОРЯДОК ЕГО РАСТОРЖЕНИЯ → Настоящий Договор вступает в силу с даты его подписания обеими Сторонами и действует по ___________ (включительно) или до исчерпания Цены договора (в зависимости от того, какое событие наступит первым). Окончание срока действия Договора не освобождает Стороны от ответственности за неисполнение обязательств по Договору.",
  2188	  "required_type":"mandatory",
  2189	  "main_idea":"",
  2190	  "only_for_product":"common",
  2191	  "only_for_lot":"common",
  2192	  "only_for_terminal":"common",
  2193	  "topics":[
  2194	   "указана дата окончания действия договора",
  2195	   "определен порядок учета цены договора при определении срока действия",
  2196	   "установлено сохранение ответственности сторон после окончания срока договора"
  2197	  ],
  2198	  "payment_method":"common"
  2199	 },
  2200	 {
Tool:   1201	      "trigger": "",
  1202	      "deadline": "",
  1203	      "amount_formula_cap": "",
  1204	      "procedure_channel": "",
  1205	      "liability_remedy": "",
  1206	      "scope_options": [],
  1207	      "consequence": "",
  1208	      "applicability_filters": {
  1209	        "required_type": "mandatory",
  1210	        "only_for_product": "common",
  1211	        "only_for_lot": "common",
  1212	        "only_for_terminal": "common",
  1213	        "payment_method": "common"
  1214	      },
  1215	      "main_idea": "Важен факт необходимости предоставлять достоверные сведения, своевременное обновление сведений. Важен факт и срок периодичного предоставления. Важен факт и срок предоставления по запросу",
  1216	      "topics": [
  1217	        "Предприятие обязано предоставлять документы не реже одного раза в год",
  1218	        "Предприятие обязано предоставлять сведения по запросу Банка в течение 7 рабочих дней",
  1219	        "Сведения о целях финансово-хозяйственной деятельности",
  1220	        "Информация о финансовом положении предприятия",
  1221	        "Данные о деловой репутации предприятия",
  1222	        "Сведения о представителях предприятия",
  1223	        "Информация о выгодоприобретателях",
  1224	        "Сведения о бенефициарных владельцах (если имеются)"
  1225	      ],
  1226	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять в Банк достоверные документы и сведения, необходимые Банку для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе, но не исключительно: не реже одного раза в год, а также по отдельному запросу Банка в течение 7 (семи) рабочих дней со дня получения запроса обновлять сведения и документы, представленные Банку при заключении настоящего Договора, включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации Предприятия, а также сведения о своих представителях, выгодоприобретателях и бенефициарных владельцах (при наличии)."
  1227	    },
  1228	    {
  1229	      "id": "4.2.16.1",
  1230	      "source_text": "Важно, чтобы было действующее согласие на передачу ПДн руководителя Предприятия. Состав ПДн: ФИО, адрес, паспортные данные. Важно, чтобы не была предусмотрена передача данных другим лицам / системам Предприятие гарантирует наличие правовых оснований на передачу ПДн; Предприятие передает ФИО руководителя; Предприятие передает адрес руководителя; Предприятие передает паспортные данные руководителя; Обязанность уведомления Банка о прекращении правовых оснований обработки ПДн «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) руководителя Предприятия, указанные в Заявлении/Информации о ТСТ: → Предприятие гарантирует наличие правовых оснований на передачу в Банк персональных данных руководителя Предприятия, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные в целях, указанных в п.5.1.7 Договора. Предприятие обязано уведомить Банк о прекращении правовых оснований на обработку ПДн руководителя Предприятия, указанных в настоящем пункте Договора.",
  1231	      "source_excerpt": "Важно, чтобы было действующее согласие на передачу ПДн руководителя Предприятия. Состав ПДн: ФИО, адрес, паспортные данные. Важно, чтобы не была предусмотрена передача данных другим лицам / системам Предприятие гарантирует наличие правовых ",
  1232	      "type": "operative",
  1233	      "materiality": "needs_source_review",
  1234	      "protected_party": "",
  1235	      "bound_party": "",
  1236	      "right_or_obligation": "",
  1237	      "legal_object": "",
  1238	      "trigger": "",
  1239	      "deadline": "",
  1240	      "amount_formula_cap": "",
  1241	      "procedure_channel": "",
  1242	      "liability_remedy": "",
  1243	      "scope_options": [],
  1244	      "consequence": "",
  1245	      "applicability_filters": {
  1246	        "required_type": "mandatory",
  1247	        "only_for_product": "common",
  1248	        "only_for_lot": "common",
  1249	        "only_for_terminal": "common",
  1250	        "payment_method": "common"
  1251	      },
  1252	      "main_idea": "Важно, чтобы было действующее согласие на передачу ПДн руководителя Предприятия.  Состав ПДн: ФИО, адрес, паспортные данные. Важно, чтобы не была предусмотрена передача данных другим лицам / системам",
  1253	      "topics": [
  1254	        "Предприятие гарантирует наличие правовых оснований на передачу ПДн",
  1255	        "Предприятие передает ФИО руководителя",
  1256	        "Предприятие передает адрес руководителя",
  1257	        "Предприятие передает паспортные данные руководителя",
  1258	        "Обязанность уведомления Банка о прекращении правовых оснований обработки ПДн"
  1259	      ],
  1260	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) руководителя Предприятия, указанные в Заявлении/Информации о ТСТ: → Предприятие гарантирует наличие правовых оснований на передачу в Банк персональных данных руководителя Предприятия, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные в целях, указанных в п.5.1.7 Договора. Предприятие обязано уведомить Банк о прекращении правовых оснований на обработку ПДн руководителя Предприятия, указанных в настоящем пункте Договора.\n"
  1261	    },
  1262	    {
  1263	      "id": "4.2.16.2",
  1264	      "source_text": "Важно, что данный пункт относится ко всем сотрудникам кроме руководителя, важно наличие согласий, обязанность подтвердить наличие согласий, важен состав ПДн Предприятие гарантирует наличие согласий сотрудников(кроме руководтитела) на обработку его персональных данных; Состав персональных данных сотрудников (кроме руководителя) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) сотрудников Предприятия: → Предприятие гарантирует наличие согласий на обработку Банком персональных данных своих работников, состав которых включает: ФИО, мобильный телефон, электронная почта, должность и место работы, а также на их дальнейшую передачу в Обслуживающие компании, действующие от лица Банка, необходимых для целей заключения и исполнения настоящего Договора. Договора. Предприятие обязуется предоставить подтверждение наличия согласий по письменному запросу Банка в соответствии с пунктом 4.2.16.3 Договора.",
  1265	      "source_excerpt": "Важно, что данный пункт относится ко всем сотрудникам кроме руководителя, важно наличие согласий, обязанность подтвердить наличие согласий, важен состав ПДн Предприятие гарантирует наличие согласий сотрудников(кроме руководтитела) на обрабо",
  1266	      "type": "operative",
  1267	      "materiality": "needs_source_review",
  1268	      "protected_party": "",
  1269	      "bound_party": "",
  1270	      "right_or_obligation": "",
  1271	      "legal_object": "",
  1272	      "trigger": "",
  1273	      "deadline": "",
  1274	      "amount_formula_cap": "",
  1275	      "procedure_channel": "",
  1276	      "liability_remedy": "",
  1277	      "scope_options": [],
  1278	      "consequence": "",
  1279	      "applicability_filters": {
  1280	        "required_type": "mandatory",
  1281	        "only_for_product": "common",
  1282	        "only_for_lot": "common",
  1283	        "only_for_terminal": "common",
  1284	        "payment_method": "common"
  1285	      },
  1286	      "main_idea": "Важно, что данный пункт относится ко всем сотрудникам кроме руководителя, важно наличие согласий, обязанность подтвердить наличие согласий, важен состав ПДн",
  1287	      "topics": [
  1288	        "Предприятие гарантирует наличие согласий сотрудников(кроме руководтитела) на обработку его персональных данных",
  1289	        "Состав персональных данных сотрудников (кроме руководителя)"
  1290	      ],
  1291	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) сотрудников Предприятия: → Предприятие гарантирует наличие согласий на обработку Банком персональных данных своих работников, состав которых включает: ФИО, мобильный телефон, электронная почта, должность и место работы, а также на их дальнейшую передачу в Обслуживающие компании, действующие от лица Банка, необходимых для целей заключения и исполнения настоящего Договора. Договора. Предприятие обязуется предоставить подтверждение наличия согласий по письменному запросу Банка в соответствии с пунктом 4.2.16.3 Договора."
  1292	    },
  1293	    {
  1294	      "id": "4.2.16.3",
  1295	      "source_text": "Важно, что данный пункт относится только к данным по всем сотрудникам. Важен срок предоставления подтверждения Предприятие обязано предоставлять подтверждение согласий на обработку персональных данных сотрудников (включая руководителя) по письменному запросу банка; Сроки предоставления подтверждения согласия руководителя; В случае отсутствия подтверждения Предприятие урегулирует претензии третьих лиц за свой счет; Предприятие возмещает Банку убытки и расходы при непредставлении обоснования передачи персональных данных «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней с даты получения соответствующего запроса, Предприятие обязуется предоставить подтверждение правомерности передачи ПДн. В случае если Предприятие не предоставит подтверждение наличия таких оснований, оно обязуется за свой счет урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные Банку, а также возместить любые убытки и расходы, понесенные Банком в результате не предоставления таких доказательств.",
  1296	      "source_excerpt": "Важно, что данный пункт относится только к данным по всем сотрудникам. Важен срок предоставления подтверждения Предприятие обязано предоставлять подтверждение согласий на обработку персональных данных сотрудников (включая руководителя) по п",
  1297	      "type": "operative",
  1298	      "materiality": "needs_source_review",
  1299	      "protected_party": "",
  1300	      "bound_party": "",
  1301	      "right_or_obligation": "",
  1302	      "legal_object": "",
  1303	      "trigger": "",
  1304	      "deadline": "",
  1305	      "amount_formula_cap": "",
  1306	      "procedure_channel": "",
  1307	      "liability_remedy": "",
  1308	      "scope_options": [],
  1309	      "consequence": "",
  1310	      "applicability_filters": {
  1311	        "required_type": "mandatory",
  1312	        "only_for_product": "common",
  1313	        "only_for_lot": "common",
  1314	        "only_for_terminal": "common",
  1315	        "payment_method": "common"
  1316	      },
  1317	      "main_idea": "Важно, что данный пункт относится только к данным по всем сотрудникам. Важен срок предоставления подтверждения",
  1318	      "topics": [
  1319	        "Предприятие обязано предоставлять подтверждение согласий на обработку персональных данных сотрудников (включая руководителя) по письменному запросу банка",
  1320	        "Сроки предоставления подтверждения согласия руководителя",
  1321	        "В случае отсутствия подтверждения Предприятие урегулирует претензии третьих лиц за свой счет",
  1322	        "Предприятие возмещает Банку убытки и расходы при непредставлении обоснования передачи персональных данных"
  1323	      ],
  1324	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней с даты получения соответствующего запроса, Предприятие обязуется предоставить подтверждение правомерности передачи ПДн. В случае если Предприятие не предоставит подтверждение наличия таких оснований, оно обязуется за свой счет урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные Банку, а также возместить любые убытки и расходы, понесенные Банком в результате не предоставления таких доказательств."
  1325	    },
  1326	    {
  1327	      "id": "4.2.17",
  1328	      "source_text": "Важен сам факт обязанности соблюдения стандарта, а так же факт обязанности предоставления подтверждения Обязательство соблюдать требования PCI DSS; Предоставление аттестата соответствия или листа самооценки по запросу банка; Указанный email для отправки документов:pcidss@sberbank.ru «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Обеспечить соблюдение требований Стандарта PCI DSS, размещенного на сайте в сети интернет: https://www.pcisecuritystandards.org и предоставлять по запросу Банка результаты проведения оценки соответствия в виде аттестата соответствия или листа самооценки на электронный адрес: pcidss@sberbank.ru.",
  1329	      "source_excerpt": "Важен сам факт обязанности соблюдения стандарта, а так же факт обязанности предоставления подтверждения Обязательство соблюдать требования PCI DSS; Предоставление аттестата соответствия или листа самооценки по запросу банка; Указанный email",
  1330	      "type": "operative",
  1331	      "materiality": "needs_source_review",
  1332	      "protected_party": "",
  1333	      "bound_party": "",
  1334	      "right_or_obligation": "",
  1335	      "legal_object": "",
  1336	      "trigger": "",
  1337	      "deadline": "",
  1338	      "amount_formula_cap": "",
  1339	      "procedure_channel": "",
  1340	      "liability_remedy": "",
  1341	      "scope_options": [],
  1342	      "consequence": "",
  1343	      "applicability_filters": {
  1344	        "required_type": "mandatory",
  1345	        "only_for_product": "internet_acquiring",
  1346	        "only_for_lot": "common",
  1347	        "only_for_terminal": "common",
  1348	        "payment_method": "common"
  1349	      },
  1350	      "main_idea": "Важен сам факт обязанности соблюдения стандарта, а так же факт обязанности предоставления подтверждения",
  1351	      "topics": [
  1352	        "Обязательство соблюдать требования PCI DSS",
  1353	        "Предоставление аттестата соответствия или листа самооценки по запросу банка",
  1354	        "Указанный email для отправки документов:pcidss@sberbank.ru"
  1355	      ],
  1356	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Обеспечить соблюдение требований Стандарта PCI DSS, размещенного на сайте в сети интернет: https://www.pcisecuritystandards.org и предоставлять по запросу Банка результаты проведения оценки соответствия в виде аттестата соответствия или листа самооценки на электронный адрес: pcidss@sberbank.ru. "
  1357	    },
  1358	    {
  1359	      "id": "4.2.18",
  1360	      "source_text": "Важны факты прекращения приема к оплате Карт, снятия информационных материалов, а так же важен срок При расторжении договора прекращение приема карт к оплате (регулируется дата прекращения); При расторжении договора снятие информационных материалов о приеме карт (регулируется дата снятия) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы, извещающие об обслуживании Карт.",
  1361	      "source_excerpt": "Важны факты прекращения приема к оплате Карт, снятия информационных материалов, а так же важен срок При расторжении договора прекращение приема карт к оплате (регулируется дата прекращения); При расторжении договора снятие информационных ма",
  1362	      "type": "operative",
  1363	      "materiality": "needs_source_review",
  1364	      "protected_party": "",
  1365	      "bound_party": "",
  1366	      "right_or_obligation": "",
  1367	      "legal_object": "",
  1368	      "trigger": "",
  1369	      "deadline": "",
  1370	      "amount_formula_cap": "",
  1371	      "procedure_channel": "",
  1372	      "liability_remedy": "",
  1373	      "scope_options": [],
  1374	      "consequence": "",
  1375	      "applicability_filters": {
  1376	        "required_type": "mandatory",
  1377	        "only_for_product": "common",
  1378	        "only_for_lot": "common",
  1379	        "only_for_terminal": "common",
  1380	        "payment_method": "common"
  1381	      },
  1382	      "main_idea": "Важны факты прекращения приема к оплате Карт, снятия информационных материалов, а так же важен срок",
  1383	      "topics": [
  1384	        "При расторжении договора прекращение приема карт к оплате (регулируется дата прекращения)",
  1385	        "При расторжении договора снятие информационных материалов о приеме карт (регулируется дата снятия)"
  1386	      ],
  1387	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы, извещающие об обслуживании Карт. "
  1388	    },
  1389	    {
  1390	      "id": "4.2.19",
  1391	      "source_text": "Важен, факт что Предприятие не должно мешать Банку, и факт, что Предприятие должно помогать Банку в расследовании Предприятие обязано не препятствовать проверке со стороны Банка; Предприятие обязано содействовать расследованию подозрительных операций «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не принимать мер противодействия Банку в проведении проверки Предприятия/ТСТ / Ресурса на предмет выявления мошеннических Операций и/или предоставления Покупателям Товаров/услуг, не соответствующих роду деятельности Предприятия/ТСТ, а также оказывать содействие Банку в проведении разбирательства по факту совершения подозрительных Операций.",
  1392	      "source_excerpt": "Важен, факт что Предприятие не должно мешать Банку, и факт, что Предприятие должно помогать Банку в расследовании Предприятие обязано не препятствовать проверке со стороны Банка; Предприятие обязано содействовать расследованию подозрительны",
  1393	      "type": "operative",
  1394	      "materiality": "needs_source_review",
  1395	      "protected_party": "",
  1396	      "bound_party": "",
  1397	      "right_or_obligation": "",
  1398	      "legal_object": "",
  1399	      "trigger": "",
  1400	      "deadline": "",
  1401	      "amount_formula_cap": "",
  1402	      "procedure_channel": "",
  1403	      "liability_remedy": "",
  1404	      "scope_options": [],
  1405	      "consequence": "",
  1406	      "applicability_filters": {
  1407	        "required_type": "mandatory",
  1408	        "only_for_product": "common",
  1409	        "only_for_lot": "common",
  1410	        "only_for_terminal": "common",
  1411	        "payment_method": "common"
  1412	      },
  1413	      "main_idea": "Важен, факт что Предприятие не должно мешать Банку, и факт, что Предприятие должно помогать Банку в расследовании",
  1414	      "topics": [
  1415	        "Предприятие обязано не препятствовать проверке со стороны Банка",
  1416	        "Предприятие обязано содействовать расследованию подозрительных операций"
  1417	      ],
  1418	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не принимать мер противодействия Банку в проведении проверки Предприятия/ТСТ / Ресурса  на предмет выявления мошеннических Операций и/или предоставления Покупателям Товаров/услуг, не соответствующих роду деятельности Предприятия/ТСТ, а также оказывать содействие Банку в проведении разбирательства по факту совершения подозрительных Операций."
  1419	    },
  1420	    {
  1421	      "id": "4.2.20.1",
  1422	      "source_text": "Важен сам факт, что Предприятие само следит за прохождением инструктажа сотрудниками, размещенного на сайте Банка обязательство предприятия проводить инструктаж сотрудников самостоятельно; ссылка на инструкцию о порядке проведения Операций «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: https://www.sberbank.ru/help/business/acquiring.",
  1423	      "source_excerpt": "Важен сам факт, что Предприятие само следит за прохождением инструктажа сотрудниками, размещенного на сайте Банка обязательство предприятия проводить инструктаж сотрудников самостоятельно; ссылка на инструкцию о порядке проведения Операций ",
  1424	      "type": "operative",
  1425	      "materiality": "needs_source_review",
  1426	      "protected_party": "",
  1427	      "bound_party": "",
  1428	      "right_or_obligation": "",
  1429	      "legal_object": "",
  1430	      "trigger": "",
  1431	      "deadline": "",
  1432	      "amount_formula_cap": "",
  1433	      "procedure_channel": "",
  1434	      "liability_remedy": "",
  1435	      "scope_options": [],
  1436	      "consequence": "",
  1437	      "applicability_filters": {
  1438	        "required_type": "mandatory",
  1439	        "only_for_product": "trade_acquiring",
  1440	        "only_for_lot": "common",
  1441	        "only_for_terminal": "common",
  1442	        "payment_method": "common"
  1443	      },
  1444	      "main_idea": "Важен сам факт, что Предприятие само следит за прохождением инструктажа сотрудниками, размещенного на сайте Банка",
  1445	      "topics": [
  1446	        "обязательство предприятия проводить инструктаж сотрудников самостоятельно",
  1447	        "ссылка на инструкцию о порядке проведения Операций"
  1448	      ],
  1449	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: https://www.sberbank.ru/help/business/acquiring."
  1450	    },
  1451	    {
  1452	      "id": "4.2.20.2",
  1453	      "source_text": "Важно, чтобы предприятие использовало терминалы и ПО Банка только для целей договора и по месту установки, не менять и не ремонтировать их самостоятельно и не передавать третьим лицам (кроме обслуживающей компании) использование Электронных терминалов и программного обеспечения только для целей договора и на территории регистрации ТСТ/установки устройства; запрет внесения изменений в ПО и оборудование; запрет самостоятельного ремонта оборудования; запрет передачи оборудования и документов третьим лицам, кроме сотрудников обслуживающей компании «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Использовать Электронные терминалы (в том числе технологические sim-карты)/Смарт-терминалы и программное обеспечение, предоставленное Банком, только для целей реализации настоящего Договора и на территории регистрации ТСТ/фактической установки Электронного терминала/Смарт-терминала. Не вносить изменения в программное обеспечение и Электронные терминалы/Смарт-терминалы, предоставленные Банком. Не осуществлять самостоятельно ремонт Электронных терминалов/Смарт-терминалов Банка. Не передавать третьим лицам Электронные терминалы/Смарт-терминалы Банка, Документы по операциям и инструктивные материалы, предоставленные Банком, за исключением работников Обслуживающей компании.",
  1454	      "source_excerpt": "Важно, чтобы предприятие использовало терминалы и ПО Банка только для целей договора и по месту установки, не менять и не ремонтировать их самостоятельно и не передавать третьим лицам (кроме обслуживающей компании) использование Электронных",
  1455	      "type": "operative",
  1456	      "materiality": "needs_source_review",
  1457	      "protected_party": "",
  1458	      "bound_party": "",
  1459	      "right_or_obligation": "",
  1460	      "legal_object": "",
  1461	      "trigger": "",
  1462	      "deadline": "",
  1463	      "amount_formula_cap": "",
  1464	      "procedure_channel": "",
  1465	      "liability_remedy": "",
  1466	      "scope_options": [],
  1467	      "consequence": "",
  1468	      "applicability_filters": {
  1469	        "required_type": "mandatory",
  1470	        "only_for_product": "trade_acquiring",
  1471	        "only_for_lot": "common",
  1472	        "only_for_terminal": "common",
  1473	        "payment_method": "common"
  1474	      },
  1475	      "main_idea": "Важно, чтобы предприятие использовало терминалы и ПО Банка только для целей договора и по месту установки, не менять и не ремонтировать их самостоятельно и не передавать третьим лицам (кроме обслуживающей компании)",
  1476	      "topics": [
  1477	        "использование Электронных терминалов и программного обеспечения только для целей договора и на территории регистрации ТСТ/установки устройства",
  1478	        "запрет внесения изменений в ПО и оборудование",
  1479	        "запрет самостоятельного ремонта оборудования",
  1480	        "запрет передачи оборудования и документов третьим лицам, кроме сотрудников обслуживающей компании"
  1481	      ],
  1482	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Использовать Электронные терминалы (в том числе технологические sim-карты)/Смарт-терминалы и программное обеспечение, предоставленное Банком, только для целей реализации настоящего Договора и на территории регистрации ТСТ/фактической установки Электронного терминала/Смарт-терминала. Не вносить изменения в программное обеспечение и Электронные терминалы/Смарт-терминалы, предоставленные Банком. Не осуществлять самостоятельно ремонт Электронных терминалов/Смарт-терминалов Банка. Не передавать третьим лицам Электронные терминалы/Смарт-терминалы Банка, Документы по операциям и инструктивные материалы, предоставленные Банком, за исключением работников Обслуживающей компании."
  1483	    },
  1484	    {
  1485	      "id": "4.2.20.3",
  1486	      "source_text": "Важно, что если в договоре стоит запрет на предоставление доступа третьим лицам, то это разногласие Предоставление доступа третьим лицам к местам установки терминалов; Доступ для подключения терминалов; Доступ для настройки терминалов; Доступ для ремонта терминалов; Доступ для замены терминалов; Доступ для технического обслуживания терминалов; Доступ для визуальной проверки терминалов «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов/Смарт-терминалов для проведения работ по их подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке.",
  1487	      "source_excerpt": "Важно, что если в договоре стоит запрет на предоставление доступа третьим лицам, то это разногласие Предоставление доступа третьим лицам к местам установки терминалов; Доступ для подключения терминалов; Доступ для настройки терминалов; Дост",
  1488	      "type": "operative",
  1489	      "materiality": "needs_source_review",
  1490	      "protected_party": "",
  1491	      "bound_party": "",
  1492	      "right_or_obligation": "",
  1493	      "legal_object": "",
  1494	      "trigger": "",
  1495	      "deadline": "",
  1496	      "amount_formula_cap": "",
  1497	      "procedure_channel": "",
  1498	      "liability_remedy": "",
  1499	      "scope_options": [],
  1500	      "consequence": "",
  1501	      "applicability_filters": {
  1502	        "required_type": "mandatory",
  1503	        "only_for_product": "trade_acquiring",
  1504	        "only_for_lot": "common",
  1505	        "only_for_terminal": "common",
  1506	        "payment_method": "common"
  1507	      },
  1508	      "main_idea": "Важно, что если в договоре стоит запрет на предоставление доступа третьим лицам, то это разногласие",
  1509	      "topics": [
  1510	        "Предоставление доступа третьим лицам к местам установки терминалов",
  1511	        "Доступ для подключения терминалов",
  1512	        "Доступ для настройки терминалов",
  1513	        "Доступ для ремонта терминалов",
  1514	        "Доступ для замены терминалов",
  1515	        "Доступ для технического обслуживания терминалов",
  1516	        "Доступ для визуальной проверки терминалов"
  1517	      ],
  1518	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов/Смарт-терминалов для проведения работ по их подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке."
  1519	    },
  1520	    {
  1521	      "id": "4.2.20.4",
  1522	      "source_text": "Важно, если указано, что оборудование Предприятие без документов или акта передачи, то всё ок, разногласия нет Предприятие обязано принять Электронные терминалы / Смарт-терминалв по акту; подписание акта уполномоченными лицами; наличие двух экземпляров акта; хранение одного экземпляра акта в Обслуживающей компании; хранение второго экземпляра акта у Предприятия «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Принять Электронные терминалы/Смарт-терминалы Банка и/или программное обеспечение для Смарт-терминалов Предприятия по акту принятия оказанных услуг по форме Обслуживающей компании, составленному в 2-х (два) экземплярах, подписанных уполномоченными работниками Обслуживающей компании и Предприятия. Один экземпляр акта находится на хранении в Обслуживающей компании, второй – у Предприятия. Форма акта размещена на Официальном сайте Банка.",
  1523	      "source_excerpt": "Важно, если указано, что оборудование Предприятие без документов или акта передачи, то всё ок, разногласия нет Предприятие обязано принять Электронные терминалы / Смарт-терминалв по акту; подписание акта уполномоченными лицами; наличие двух",
  1524	      "type": "operative",
  1525	      "materiality": "needs_source_review",
  1526	      "protected_party": "",
  1527	      "bound_party": "",
  1528	      "right_or_obligation": "",
  1529	      "legal_object": "",
  1530	      "trigger": "",
  1531	      "deadline": "",
  1532	      "amount_formula_cap": "",
  1533	      "procedure_channel": "",
  1534	      "liability_remedy": "",
  1535	      "scope_options": [],
  1536	      "consequence": "",
  1537	      "applicability_filters": {
  1538	        "required_type": "mandatory",
  1539	        "only_for_product": "trade_acquiring",
  1540	        "only_for_lot": "common",
  1541	        "only_for_terminal": "common",
  1542	        "payment_method": "common"
  1543	      },
  1544	      "main_idea": "Важно, если указано, что оборудование Предприятие без документов или акта передачи, то всё ок, разногласия нет",
  1545	      "topics": [
  1546	        "Предприятие обязано принять Электронные терминалы / Смарт-терминалв по акту",
  1547	        "подписание акта уполномоченными лицами",
  1548	        "наличие двух экземпляров акта",
  1549	        "хранение одного экземпляра акта в Обслуживающей компании",
  1550	        "хранение второго экземпляра акта у Предприятия"
  1551	      ],
  1552	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Принять Электронные терминалы/Смарт-терминалы Банка и/или программное обеспечение для Смарт-терминалов Предприятия по акту принятия оказанных услуг по форме Обслуживающей компании, составленному в 2-х (два) экземплярах, подписанных уполномоченными работниками Обслуживающей компании и Предприятия. Один экземпляр акта находится на хранении в Обслуживающей компании, второй – у Предприятия. Форма акта размещена на Официальном сайте Банка."
  1553	    },
  1554	    {
  1555	      "id": "4.2.20.5",
  1556	      "source_text": "Предприятие обязано немедленно информировать Банк о выходе из строя или утрате Электронного терминала/Смарт-терминала или Мобильного устройства; Информирование осуществляется согласно пунктам 2.3.1 и 2.3.2 Договора или через службу поддержки Банка «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае выхода Электронного терминала/Смарт-терминала, в том числе Мобильного устройства Предприятия, из строя или его утраты немедленно информировать об этом Банк в соответствии с п. 2.3.1, п. 2.3.2 Договора или путем обращения в службу поддержки Банка по телефону, указанному в п. 2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.",
  1557	      "source_excerpt": "Предприятие обязано немедленно информировать Банк о выходе из строя или утрате Электронного терминала/Смарт-терминала или Мобильного устройства; Информирование осуществляется согласно пунктам 2.3.1 и 2.3.2 Договора или через службу поддержк",
  1558	      "type": "operative",
  1559	      "materiality": "needs_source_review",
  1560	      "protected_party": "",
  1561	      "bound_party": "",
  1562	      "right_or_obligation": "",
  1563	      "legal_object": "",
  1564	      "trigger": "",
  1565	      "deadline": "",
  1566	      "amount_formula_cap": "",
  1567	      "procedure_channel": "",
  1568	      "liability_remedy": "",
  1569	      "scope_options": [],
  1570	      "consequence": "",
  1571	      "applicability_filters": {
  1572	        "required_type": "mandatory",
  1573	        "only_for_product": "trade_acquiring",
  1574	        "only_for_lot": "common",
  1575	        "only_for_terminal": "common",
  1576	        "payment_method": "common"
  1577	      },
  1578	      "main_idea": "",
  1579	      "topics": [
  1580	        "Предприятие обязано немедленно информировать Банк о выходе из строя или утрате Электронного терминала/Смарт-терминала или Мобильного устройства",
  1581	        "Информирование осуществляется согласно пунктам 2.3.1 и 2.3.2 Договора или через службу поддержки Банка"
  1582	      ],
  1583	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае выхода Электронного терминала/Смарт-терминала, в том числе Мобильного устройства Предприятия, из строя или его утраты немедленно информировать об этом Банк в соответствии с п. 2.3.1, п. 2.3.2 Договора или путем обращения в службу поддержки Банка по телефону, указанному в п. 2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.\n"
  1584	    },
  1585	    {
  1586	      "id": "4.2.20.6",
  1587	      "source_text": "вернуть терминал в течение 5 рабочих дней после расторжения договора; вернуть терминал после получения письменного/устного требования банка «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Вернуть Банку или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Договора или с даты получения письменного/устного требования Банка о возврате Электронных терминалов/Смарт-терминалов Банка.",
  1588	      "source_excerpt": "вернуть терминал в течение 5 рабочих дней после расторжения договора; вернуть терминал после получения письменного/устного требования банка «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприят",
  1589	      "type": "operative",
  1590	      "materiality": "needs_source_review",
  1591	      "protected_party": "",
  1592	      "bound_party": "",
  1593	      "right_or_obligation": "",
  1594	      "legal_object": "",
  1595	      "trigger": "",
  1596	      "deadline": "",
  1597	      "amount_formula_cap": "",
  1598	      "procedure_channel": "",
  1599	      "liability_remedy": "",
  1600	      "scope_options": [],
  1601	      "consequence": "",
  1602	      "applicability_filters": {
  1603	        "required_type": "mandatory",
  1604	        "only_for_product": "trade_acquiring",
  1605	        "only_for_lot": "common",
  1606	        "only_for_terminal": "common",
  1607	        "payment_method": "common"
  1608	      },
  1609	      "main_idea": "",
  1610	      "topics": [
  1611	        "вернуть терминал в течение 5 рабочих дней после расторжения договора",
  1612	        "вернуть терминал после получения письменного/устного требования банка"
  1613	      ],
  1614	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Вернуть Банку или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Договора или с даты получения письменного/устного требования Банка о возврате Электронных терминалов/Смарт-терминалов Банка."
  1615	    },
  1616	    {
  1617	      "id": "4.2.20.7",
  1618	      "source_text": "Важно, чтобы в соответствующем пункте договора шла речь про штраф за невозврат терминала и его размер, иначе данный пункт матрицы не относится к пункту договора Невозврат терминалов. Обязанность предприятия об уплате штрафа за невозврат «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае невозврата Электронных терминалов /Смарт-терминалов Банка в соответствии с п. 4.2.20.6 Договора, уплатить Банку штраф в размере 25 000 (двадцать пять тысяч) рублей, в том числе НДС, за каждый Электронный терминал и 25 000 (двадцать пять тысяч) рублей, в том числе НДС за каждый Смарт-терминал Банка.",
  1619	      "source_excerpt": "Важно, чтобы в соответствующем пункте договора шла речь про штраф за невозврат терминала и его размер, иначе данный пункт матрицы не относится к пункту договора Невозврат терминалов. Обязанность предприятия об уплате штрафа за невозврат «ПР",
  1620	      "type": "operative",
  1621	      "materiality": "needs_source_review",
  1622	      "protected_party": "",
  1623	      "bound_party": "",
  1624	      "right_or_obligation": "",
  1625	      "legal_object": "",
  1626	      "trigger": "",
  1627	      "deadline": "",
  1628	      "amount_formula_cap": "",
  1629	      "procedure_channel": "",
  1630	      "liability_remedy": "",
  1631	      "scope_options": [],
  1632	      "consequence": "",
  1633	      "applicability_filters": {
  1634	        "required_type": "mandatory",
  1635	        "only_for_product": "trade_acquiring",
  1636	        "only_for_lot": "common",
  1637	        "only_for_terminal": "common",
  1638	        "payment_method": "common"
  1639	      },
  1640	      "main_idea": "Важно, чтобы в соответствующем пункте договора шла речь про штраф за невозврат терминала и его размер, иначе данный пункт матрицы не относится к пункту договора",
  1641	      "topics": [
  1642	        "Невозврат терминалов. Обязанность предприятия об уплате штрафа за невозврат"
  1643	      ],
  1644	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае невозврата Электронных терминалов /Смарт-терминалов Банка в соответствии с п. 4.2.20.6 Договора, уплатить Банку штраф в размере 25 000 (двадцать пять тысяч) рублей, в том числе НДС, за каждый Электронный терминал и 25 000 (двадцать пять тысяч) рублей, в том числе НДС за каждый Смарт-терминал Банка."
  1645	    },
  1646	    {
  1647	      "id": "4.2.21.1",
  1648	      "source_text": "Приступить к проведению операций на ресурсе только после успешного завершения проверки операций на тестовой среде «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Приступить к проведению Операций на Ресурсе только после успешного завершения проверки выбранных Предприятием/ТСТ Операций на тестовой среде.",
  1649	      "source_excerpt": "Приступить к проведению операций на ресурсе только после успешного завершения проверки операций на тестовой среде «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): прове",
  1650	      "type": "operative",
  1651	      "materiality": "needs_source_review",
  1652	      "protected_party": "",
  1653	      "bound_party": "",
  1654	      "right_or_obligation": "",
  1655	      "legal_object": "",
  1656	      "trigger": "",
  1657	      "deadline": "",
  1658	      "amount_formula_cap": "",
  1659	      "procedure_channel": "",
  1660	      "liability_remedy": "",
  1661	      "scope_options": [],
  1662	      "consequence": "",
  1663	      "applicability_filters": {
  1664	        "required_type": "mandatory",
  1665	        "only_for_product": "internet_acquiring",
  1666	        "only_for_lot": "common",
  1667	        "only_for_terminal": "common",
  1668	        "payment_method": "common"
  1669	      },
  1670	      "main_idea": "",
  1671	      "topics": [
  1672	        "Приступить к проведению операций на ресурсе только после успешного завершения проверки операций на тестовой среде"
  1673	      ],
  1674	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Приступить к проведению Операций на Ресурсе только после успешного завершения проверки выбранных Предприятием/ТСТ Операций на тестовой среде."
  1675	    },
  1676	    {
  1677	      "id": "4.2.21.2",
  1678	      "source_text": "Предприятие обязано соответствовать Требованиям Банка к Ресурсу, размещенным на Официальном сайте Банка «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соответствовать Требованиям Банка к Ресурсу Предприятия, размещенным на Официальном сайте Банка.",
  1679	      "source_excerpt": "Предприятие обязано соответствовать Требованиям Банка к Ресурсу, размещенным на Официальном сайте Банка «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на эта",
  1680	      "type": "operative",
  1681	      "materiality": "needs_source_review",
  1682	      "protected_party": "",
  1683	      "bound_party": "",
  1684	      "right_or_obligation": "",
  1685	      "legal_object": "",
  1686	      "trigger": "",
  1687	      "deadline": "",
  1688	      "amount_formula_cap": "",
  1689	      "procedure_channel": "",
  1690	      "liability_remedy": "",
  1691	      "scope_options": [],
  1692	      "consequence": "",
  1693	      "applicability_filters": {
  1694	        "required_type": "mandatory",
  1695	        "only_for_product": "internet_acquiring",
  1696	        "only_for_lot": "common",
  1697	        "only_for_terminal": "common",
  1698	        "payment_method": "common"
  1699	      },
  1700	      "main_idea": "",
AI: I now have a thorough understanding of the data. Let me update my task list and proceed with the core analysis. I have enough context to identify contract-only terms. Let me now systematically work through the contract text to identify clauses that have no matrix analogue and have independent legal effect.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full contract text and identify all contract clause IDs', 'status': 'completed'}, {'content': 'Read full matrix to understand all matrix requirements and their applicability filters', 'status': 'completed'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile) for context', 'status': 'completed'}, {'content': 'Identify contract clauses with no matrix analogue using materiality ladder', 'status': 'in_progress'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Build domain_crosswalk fragment with processed/assigned/skipped/unresolved IDs', 'status': 'pending'}, {'content': 'Write output to /outputs/working/contract_extra_review.json', 'status': 'pending'}]}, 'id': 'call_00_R3q7MBSIq80IKyJBH5sD2812', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full contract text and identify all contract clause IDs', 'status': 'completed'}, {'content': 'Read full matrix to understand all matrix requirements and their applicability filters', 'status': 'completed'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile) for context', 'status': 'completed'}, {'content': 'Identify contract clauses with no matrix analogue using materiality ladder', 'status': 'in_progress'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Build domain_crosswalk fragment with processed/assigned/skipped/unresolved IDs', 'status': 'pending'}, {'content': 'Write output to /outputs/working/contract_extra_review.json', 'status': 'pending'}]
AI: Now let me do the systematic contract-only analysis. I'll go through the contract clause by clause, comparing against the matrix. The contract product profile tells us: trade_acquiring, 44_fz, POS terminals, cards + QR payment methods. Matrix items filtered for `internet_acquiring`, `smart` terminals, `sber_pay_face_scan`, `fz_223` are out of scope.

Let me now build the comprehensive analysis. I'll create a Python script to help organize this systematically.[{'name': 'execute', 'args': {'command': 'cd / && python3 -c "\nimport json\n\n# Load matrix\nwith open(\'inputs/matrix.json\') as f:\n    matrix = json.load(f)\n\n# Get all matrix IDs and their applicability\nmatrix_ids = set()\nmatrix_applicable = set()\nfor m in matrix:\n    mid = m[\'number\']\n    matrix_ids.add(mid)\n    # Check if applicable to this contract profile: trade_acquiring, 44_fz, pos, cards+qr\n    product = m.get(\'only_for_product\', \'common\')\n    lot = m.get(\'only_for_lot\', \'common\')\n    terminal = m.get(\'only_for_terminal\', \'common\')\n    payment = m.get(\'payment_method\', \'common\')\n    \n    # Contract: trade_acquiring, 44_fz, pos, cards+qr\n    product_ok = product in (\'common\', \'trade_acquiring\')\n    lot_ok = lot in (\'common\', \'fz_44\')\n    terminal_ok = terminal in (\'common\', \'pos\')\n    payment_ok = payment in (\'common\', \'cards\', \'qr\')\n    \n    if product_ok and lot_ok and terminal_ok and payment_ok:\n        matrix_applicable.add(mid)\n\nprint(f\'Total matrix items: {len(matrix_ids)}\')\nprint(f\'Applicable matrix items: {len(matrix_applicable)}\')\nprint(f\'Non-applicable: {len(matrix_ids - matrix_applicable)}\')\n\n# Print non-applicable with reasons\nfor m in matrix:\n    mid = m[\'number\']\n    if mid not in matrix_applicable:\n        reasons = []\n        if m.get(\'only_for_product\',\'\') not in (\'common\',\'trade_acquiring\'):\n            reasons.append(f\'product={m.get(\\"only_for_product\\")}\')\n        if m.get(\'only_for_lot\',\'\') not in (\'common\',\'fz_44\'):\n            reasons.append(f\'lot={m.get(\\"only_for_lot\\")}\')\n        if m.get(\'only_for_terminal\',\'\') not in (\'common\',\'pos\'):\n            reasons.append(f\'terminal={m.get(\\"only_for_terminal\\")}\')\n        if m.get(\'payment_method\',\'\') not in (\'common\',\'cards\',\'qr\'):\n            reasons.append(f\'payment={m.get(\\"payment_method\\")}\')\n        print(f\'  {mid}: {reasons}\')\n"\n'}, 'id': 'call_00_ApCYhq9X0IbvOyh6gAv98540', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:6
[stderr] + cd / && python3 -c "
[stderr] +      ~~
[stderr] The token '&&' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\') as f:\n    matrix = json.load(f)\nmatrix_ids = set()\nmatrix_applicable = set()\nfor m in matrix:\n    mid = m[\'number\']\n    matrix_ids.add(mid)\n    product = m.get(\'only_for_product\', \'common\')\n    lot = m.get(\'only_for_lot\', \'common\')\n    terminal = m.get(\'only_for_terminal\', \'common\')\n    payment = m.get(\'payment_method\', \'common\')\n    product_ok = product in (\'common\', \'trade_acquiring\')\n    lot_ok = lot in (\'common\', \'fz_44\')\n    terminal_ok = terminal in (\'common\', \'pos\')\n    payment_ok = payment in (\'common\', \'cards\', \'qr\')\n    if product_ok and lot_ok and terminal_ok and payment_ok:\n        matrix_applicable.add(mid)\nprint(f\'Total: {len(matrix_ids)}, Applicable: {len(matrix_applicable)}, Non-applicable: {len(matrix_ids - matrix_applicable)}\')\nfor m in matrix:\n    mid = m[\'number\']\n    if mid not in matrix_applicable:\n        reasons = []\n        if m.get(\'only_for_product\',\'\') not in (\'common\',\'trade_acquiring\'):\n            reasons.append(f\'product={m.get(\\"only_for_product\\")}\')\n        if m.get(\'only_for_lot\',\'\') not in (\'common\',\'fz_44\'):\n            reasons.append(f\'lot={m.get(\\"only_for_lot\\")}\')\n        if m.get(\'only_for_terminal\',\'\') not in (\'common\',\'pos\'):\n            reasons.append(f\'terminal={m.get(\\"only_for_terminal\\")}\')\n        if m.get(\'payment_method\',\'\') not in (\'common\',\'cards\',\'qr\'):\n            reasons.append(f\'payment={m.get(\\"payment_method\\")}\')\n        print(f\'  {mid}: {reasons}\')\n"\n'}, 'id': 'call_00_hWLGADkuxt8tr0K23M5M9466', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 26
[stderr]     reasons.append(f'product={m.get(" only_for_product\)}')
[stderr]                                     ^
[stderr] SyntaxError: unterminated string literal (detected at line 26)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/check_applicability.py', 'content': "import json\n\nwith open('/inputs/matrix.json') as f:\n    matrix = json.load(f)\n\nmatrix_ids = set()\nmatrix_applicable = set()\n\nfor m in matrix:\n    mid = m['number']\n    matrix_ids.add(mid)\n    product = m.get('only_for_product', 'common')\n    lot = m.get('only_for_lot', 'common')\n    terminal = m.get('only_for_terminal', 'common')\n    payment = m.get('payment_method', 'common')\n    \n    product_ok = product in ('common', 'trade_acquiring')\n    lot_ok = lot in ('common', 'fz_44')\n    terminal_ok = terminal in ('common', 'pos')\n    payment_ok = payment in ('common', 'cards', 'qr')\n    \n    if product_ok and lot_ok and terminal_ok and payment_ok:\n        matrix_applicable.add(mid)\n\nprint(f'Total: {len(matrix_ids)}, Applicable: {len(matrix_applicable)}, Non-applicable: {len(matrix_ids - matrix_applicable)}')\n\nfor m in matrix:\n    mid = m['number']\n    if mid not in matrix_applicable:\n        reasons = []\n        p = m.get('only_for_product','')\n        l = m.get('only_for_lot','')\n        t = m.get('only_for_terminal','')\n        pm = m.get('payment_method','')\n        if p not in ('common','trade_acquiring'):\n            reasons.append('product=' + p)\n        if l not in ('common','fz_44'):\n            reasons.append('lot=' + l)\n        if t not in ('common','pos'):\n            reasons.append('terminal=' + t)\n        if pm not in ('common','cards','qr'):\n            reasons.append('payment=' + pm)\n        print(f'  {mid}: {reasons}')\n\n# Print applicable IDs sorted\nprint('\\nApplicable matrix IDs:')\nfor mid in sorted(matrix_applicable, key=lambda x: tuple(int(i) if i.isdigit() else i for i in x.split('.'))):\n    print(f'  {mid}')\n"}, 'id': 'call_00_4DYFwcnxo8vrIgUDWM6v6824', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/check_applicability.py
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/check_applicability.py'}, 'id': 'call_00_cpYLmIVY8TjK8QKuyo1l9207', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\check_applicability.py", line 3, in <module>
[stderr]     with open('/inputs/matrix.json') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/inputs/matrix.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'ls /inputs/'}, 'id': 'call_00_kcPR9Hw9lw56AKahb1BH8941', 'type': 'tool_call'}]
Tool: 

    РљР°С‚Р°Р»РѕРі: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\inputs


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        25.06.2026     17:31         135560 contract.txt                                                         
-a----        23.06.2026     10:26         231542 matrix.json                                                          

[Command succeeded with exit code 0]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import os; print(os.getcwd())"'}, 'id': 'call_00_1U6r8MZ3MqC6UVWPoYJ81285', 'type': 'tool_call'}]
Tool: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2

[Command succeeded with exit code 0]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/check_applicability.py', 'old_string': "with open('/inputs/matrix.json') as f:", 'new_string': "import os\nbase = os.getcwd()\nwith open(os.path.join(base, 'inputs/matrix.json')) as f:"}, 'id': 'call_00_HdkYIYnhMVbVnifQP2635445', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/check_applicability.py'
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/check_applicability.py'}, 'id': 'call_00_1opAq0ggZMO31SLItfa78181', 'type': 'tool_call'}]
Tool: Total: 169, Applicable: 133, Non-applicable: 36
  2.5.1.1: ['product=internet_acquiring']
  2.5.2.1: ['payment=sber_pay_face_scan']
  2.6.1.1: ['terminal=smart']
  4.1.3: ['payment=qr_sber_pay']
  4.2.3: ['lot=fz_223']
  4.2.17: ['product=internet_acquiring']
  4.2.21.1: ['product=internet_acquiring']
  4.2.21.2: ['product=internet_acquiring']
  4.2.21.3: ['product=internet_acquiring']
  4.2.21.4: ['product=internet_acquiring']
  4.2.21.5: ['product=internet_acquiring']
  4.2.21.6: ['product=internet_acquiring']
  4.2.21.7: ['product=internet_acquiring']
  4.2.21.8: ['product=internet_acquiring']
  4.2.26: ['product=internet_acquiring']
  5.1.8.4: ['product=internet_acquiring']
  5.1.8.5: ['product=internet_acquiring']
  5.1.17.2: ['terminal=smart']
  5.2.1: ['product=internet_acquiring']
  5.2.2: ['product=internet_acquiring']
  5.2.12: ['product=internet_acquiring']
  6.3: ['lot=fz_223']
  6.6: ['lot=fz_223']
  6.7: ['terminal=smart']
  6.8: ['terminal=smart']
  6.9: ['lot=fz_223', 'terminal=smart']
  6.10: ['terminal=smart']
  6.11: ['terminal=smart']
  6.12: ['lot=fz_223', 'terminal=smart']
  6.13: ['terminal=smart']
  6.14: ['terminal=smart']
  6.15: ['lot=fz_223', 'terminal=smart']
  6.16: ['terminal=smart']
  6.17: ['terminal=smart']
  6.18: ['lot=fz_223', 'terminal=smart']
  7.13: ['product=internet_acquiring']

Applicable matrix IDs:
  2.1
  2.2
  2.3.1
  2.3.2
  2.3.3
  2.3.4
  2.3.5
  2.3.6
  2.3.7
  2.4
  2.6.2.1
  2.6.2.2
  2.6.3.1
  2.6.3.2
  2.7
  3.1
  3.2
  3.3
  4.1.1
  4.1.2
  4.2.1
  4.2.2
  4.2.4
  4.2.5
  4.2.6
  4.2.7
  4.2.8
  4.2.9
  4.2.10
  4.2.11
  4.2.12
  4.2.13
  4.2.14
  4.2.15
  4.2.16.1
  4.2.16.2
  4.2.16.3
  4.2.18
  4.2.19
  4.2.20.1
  4.2.20.2
  4.2.20.3
  4.2.20.4
  4.2.20.5
  4.2.20.6
  4.2.20.7
  4.2.22
  4.2.23
  4.2.24
  4.2.25
  5.1.1.1
  5.1.1.2
  5.1.1.3
  5.1.1.4
  5.1.1.5
  5.1.1.6
  5.1.2
  5.1.3
  5.1.4
  5.1.5
  5.1.6
  5.1.7
  5.1.8.1
  5.1.8.2
  5.1.8.3
  5.1.8.6
  5.1.8.7
  5.1.8.8
  5.1.8.9
  5.1.8.10
  5.1.8.11
  5.1.8.12
  5.1.8.13
  5.1.9
  5.1.10
  5.1.11
  5.1.12
  5.1.13
  5.1.14
  5.1.15
  5.1.16
  5.1.17.1
  5.2.3
  5.2.4
  5.2.5
  5.2.6
  5.2.7
  5.2.8
  5.2.9
  5.2.10
  6.1
  6.2
  6.4
  6.5
  6.20
  6.21
  7.1
  7.2
  7.3
  7.4
  7.5
  7.6
  7.7
  7.8
  7.9
  7.10
  7.11
  7.12
  7.14
  7.15
  7.16
  7.17
  8.1
  8.2
  9.1
  9.2
  9.3
  10.1
  10.2
  10.3
  11.1
  11.2
  11.3
  11.4
  11.5
  11.6
  11.7
  11.8
  11.9
  11.10
  11.11
  11.12
  11.13

[Command succeeded with exit code 0]
AI: Good. Now I have the 133 applicable matrix IDs. Let me now systematically go through the contract text and identify all contract clause IDs, then determine which have no matrix analogue. Let me write a comprehensive analysis script.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full contract text and identify all contract clause IDs', 'status': 'completed'}, {'content': 'Read full matrix to understand all matrix requirements and their applicability filters', 'status': 'completed'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile) for context', 'status': 'completed'}, {'content': 'Identify contract clauses with no matrix analogue using materiality ladder', 'status': 'in_progress'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Build domain_crosswalk fragment with processed/assigned/skipped/unresolved IDs', 'status': 'pending'}, {'content': 'Write output to /outputs/working/contract_extra_review.json', 'status': 'pending'}]}, 'id': 'call_00_FWAFxRvnIR5ukjPOosUw0696', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full contract text and identify all contract clause IDs', 'status': 'completed'}, {'content': 'Read full matrix to understand all matrix requirements and their applicability filters', 'status': 'completed'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile) for context', 'status': 'completed'}, {'content': 'Identify contract clauses with no matrix analogue using materiality ladder', 'status': 'in_progress'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Build domain_crosswalk fragment with processed/assigned/skipped/unresolved IDs', 'status': 'pending'}, {'content': 'Write output to /outputs/working/contract_extra_review.json', 'status': 'pending'}]
AI: Now let me do the deep legal analysis. I'll go through the contract systematically, clause by clause, and identify which contract clauses have no matrix analogue. This is the core legal work.

Let me first extract all contract clause IDs systematically:[{'name': 'write_file', 'args': {'file_path': '/outputs/working/extract_contract_ids.py', 'content': 'import os, re\n\nbase = os.getcwd()\nwith open(os.path.join(base, \'inputs/contract.txt\'), encoding=\'utf-8\') as f:\n    text = f.read()\n\n# Find all clause-like IDs\n# Patterns: X.Y, X.Y.Z, X.Y.Z.W, also appendix labels\nlines = text.split(\'\\n\')\nids = []\nfor i, line in enumerate(lines):\n    stripped = line.strip()\n    # Match patterns like "2.1.", "5.1.1.", "8.3.1.", "5.2.9.1.", etc.\n    m = re.match(r\'^(\\d+(?:\\.\\d+)+)\\.?\\s\', stripped)\n    if m:\n        cid = m.group(1)\n        # Get context\n        context = stripped[:120]\n        ids.append((cid, i+1, context))\n\n# Also find appendix/section headers\nfor i, line in enumerate(lines):\n    stripped = line.strip()\n    if re.match(r\'^(Приложение|Приложение\\s+№)\', stripped):\n        ids.append((stripped[:60], i+1, stripped[:120]))\n\n# Sort\nids.sort(key=lambda x: tuple(int(p) if p.isdigit() else p for p in x[0].replace(\'Приложение\',\'999\').split(\'.\')))\n\nprint("Contract clause IDs found:")\nfor cid, lineno, ctx in ids:\n    print(f"  Line {lineno}: [{cid}] {ctx}")\n'}, 'id': 'call_00_BdfyFsrFN97t79Lvg2mP8852', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/extract_contract_ids.py
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/extract_contract_ids.py'}, 'id': 'call_00_jxz9sfeiXdfemKJF37y33869', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\extract_contract_ids.py", line 28, in <module>
[stderr]     ids.sort(key=lambda x: tuple(int(p) if p.isdigit() else p for p in x[0].replace('РџСЂРёР»РѕР¶РµРЅРёРµ','999').split('.')))
[stderr]     ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] TypeError: '<' not supported between instances of 'str' and 'int'

Exit code: 1
[Command failed with exit code 1]

