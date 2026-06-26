## Summarized at 2026-06-26T09:29:28.098795+00:00

Human: Contract-extra-review
AI: I'll start by reading the skill file to understand the full workflow, then explore the project structure.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_m6mkVLfEumTPfGIWgNxF1095', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/'}, 'id': 'call_01_vNyiWHGTyzjmzEWdWp725056', 'type': 'tool_call'}]
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
   122	processed until the source text has been reviewed. Do not proceed to matching
   123	with unresolved source-review rows that could affect status.
   124	
   125	The ledger is an evidence table, not a substitute for the source. Matching may
   126	use it to find candidates. Status must still be confirmed against source text.
   127	
   128	Run the mechanical check before matching:
   129	
   130	```bash
   131	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/working_artifact_validation.json
   132	```
   133	
   134	This is a stage gate, not a final QA item. Before starting matrix matching,
   135	contract-only review, merge, or status work:
   136	
   137	- `outputs/working/working_artifact_validation.json` must have `"valid": true`;
   138	- `legal_propositions.json` must not contain unresolved
   139	  `needs_source_review` rows;
   140	- every evaluable row must have source text and enough normalized legal fields
   141	  to preserve its legal meaning.
   142	
   143	If the check fails, repair the working artifact that failed and rerun this
   144	validator. Do not defer incomplete legal proposition rows to Final QA.
   145	
   146	### 4. Contract Product Profile
   147	
   148	Create `/outputs/working/contract_product_profile.json`.
   149	
   150	Extract from the contract:
   151	
   152	- product and payment channels;
   153	- lot/procurement type;
   154	- terminal/payment-device scope;
   155	- payment methods;
   156	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   157	
   158	Apply matrix filters before status:
   159	
   160	- `common` applies to every contract.
   161	- A filtered matrix item applies only when the profile matches
   162	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   163	- Mandatory applicable missing = high risk.
   164	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   165	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   166	  profile-based reason. Do not put them in final `unmatched_matrix`.
   167	- Optional applicable missing = low or conditional risk.
   168	- Slash-separated alternatives are options unless the matrix says all options
   169	  are mandatory.
   170	- Placeholder or blank in an applicable material term = low-risk `deviation`.
   171	
   172	## Analogue Threshold
   173	
   174	Create a final link only when the contract proposition is a true legal analogue
   175	of the matrix proposition. Test:
   176	
   177	- same or equivalent protected party;
   178	- same or equivalent bound party;
   179	- same legal object;
   180	- same operative right, duty, prohibition, permission, remedy, or allocation of
   181	  risk;
   182	- material trigger, scope, procedure, and consequence are the same or legally
   183	  equivalent.
   184	
   185	Reject weak thematic candidates. A clause about the same broad topic is not a
   186	legal analogue when it governs a different object, party, trigger, procedure,
   187	or consequence.
   188	
   189	## Bidirectional Matching
   190	
   191	Perform both directions.
   192	
   193	Matrix to contract:
   194	
   195	- for each applicable evaluable matrix proposition, retrieve all contract
   196	  clauses that collectively cover the Bank-standard requirement;
   197	- include parent, child, appendix, payment, procedure, liability, and framework
   198	  clauses only when they provide material coverage or legally cure a gap.
   199	- if a child clause is selected, check whether its parent carries operative
   200	  legal meaning for the same topic; if a parent is selected, check whether its
   201	  children contain the material elements;
   202	- for payment, acceptance, liability, termination, and document-exchange
   203	  requirements, keep the legal package together: operative clause, basis,
   204	  deadline, procedure, remedy, consequence, and any incorporated appendix/table
   205	  row that changes coverage;
   206	- a framework or legal-compliance clause may be a standalone analogue only when
   207	  it carries the same legal object or allocates the same risk, duty, or remedy.
   208	
   209	Contract to matrix:
   210	
   211	- for each evaluable contract proposition, find the matrix analogue group;
   212	- if none exists and the term has independent legal effect, classify it as
   213	  `extra_in_contract`;
   214	- if it is non-operative, close it as `not_material` only in the ledger.
   215	
   216	Group related ids into many-to-many `links`. One matrix id may need several
   217	contract clauses. One contract clause may cover several matrix ids.
   218	
   219	## Group-Level Status
   220	
   221	Assign status to the group, not to each atomic pair.
   222	
   223	- `aligned`: the contract package preserves the matrix legal result.
   224	- `deviation`: a true analogue exists, but any material element is changed,
   225	  narrowed, weakened, omitted, shifted, or blank.
   226	- `missing_in_contract`: no true contract analogue exists for an applicable
   227	  matrix requirement.
   228	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   229	  analogue.
   230	- `not_material`: internal ledger closure only; exclude from final report.
   231	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
   232	  final report because the requirement does not apply to the current product,
   233	  lot, terminal, payment method, or legal regime.
   234	
   235	Material elements include party, legal object, operative act, trigger,
   236	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   237	remedy, exception, Bank right, merchant duty, and consequence.
   238	
   239	Hard terms must be compared directly:
   240	
   241	- same material deadline/amount/procedure in the same legal obligation can be
   242	  `aligned`;
   243	- changed value or missing value is `deviation`;
   244	- a hard term from another clause counts only when that clause expressly
   245	  governs the same obligation or is explicitly incorporated;
   246	- a neighboring date, amount, or procedure for another legal object cannot cure
   247	  the gap.
   248	
   249	Do not downgrade for formal differences alone: heading, title, appendix label,
   250	permitted option selection, equivalent mandatory-law mechanism, or wording
   251	style.
   252	
   253	Do not downgrade for low-risk notes when the legal result is preserved. If the
   254	reason says the difference is merely terminological, beneficial to the Bank,
   255	already incorporated through another clause, or caused only by a mandatory
   256	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
   257	
   258	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
   259	when it materially worsens or changes a Bank-standard term: payment timing,
   260	acceptance control, withholding right, penalty/cap, termination power, protected
   261	party, evidence channel, or enforceability.
   262	
   263	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
   264	Before marking a liability group `aligned`, check the amount, formula, cap,
   265	trigger, protected party, excluded delay/non-delay buckets, and claim procedure
   266	across the whole package.
   267	
   268	## Risk Calibration
   269	
   270	Use `risk_level` consistently:
   271	
   272	- `none`: only for `aligned`;
   273	- `low`: optional applicable missing, placeholder, formal but legally manageable
   274	  gap;
   275	- `medium`: material deviation that can affect performance, evidence, payment,
   276	  control, liability, or enforceability;
   277	- `high`: mandatory missing, changed protected party, major payment/remedy
   278	  change, important Bank right omitted, or broad contract-only risk.
   279	
   280	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   281	a short evidence-based reason. Use concise quotes rather than long excerpts.
   282	
   283	## Final QA
   284	
   285	Before writing final artifacts:
   286	
   287	- verify `clause_index` covers all source ids;
   288	- verify `outputs/working/working_artifact_validation.json` exists and is
   289	  valid; if it is missing or invalid, return to the Legal Proposition Ledger
   290	  stage instead of patching only the final JSON;
   291	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   292	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   293	  `coverage_ledger`;
   294	- verify every applicable evaluable matrix id is linked or in
   295	  `unmatched_matrix`;
   296	- verify out-of-scope / non-applicable matrix ids are not in final
   297	  `unmatched_matrix`;
   298	- verify every material contract id is closed as linked or extra;
   299	- verify `coverage_ledger` is derived from final `links`,
   300	  `unmatched_matrix`, and `unmatched_contract`;
   301	- verify every final id is visible in source text;
   302	- verify `aligned` has no material discrepancy;
   303	- verify every `deviation` has a named legal gap and evidence;
   304	- verify weak candidates are not in final `links`;
   305	- verify non-material contract rows are absent from final `unmatched_contract`;
   306	- verify summary counts equal final arrays.
   307	
   308	## Output Discipline
   309	
   310	Follow `references/output-contract.md`.
   311	
   312	The final JSON must contain:
   313	
   314	- `analysis_profile`
   315	- `links`
   316	- `atomic_links`
   317	- `unmatched_matrix`
   318	- `unmatched_contract`
   319	- `coverage_ledger`
   320	- `summary`
   321	
   322	`links` carry group-level legal findings. `atomic_links` are traceability
   323	projections only and must inherit the group relationship. Do not assign
   324	separate final pair-level statuses.
   325	
   326	## Tools And Scripts
   327	
   328	Use helper scripts for mechanical work: source extraction, indexing,
   329	normalization checks, batch completeness, coverage validation, JSON schema
   330	checks, and Excel export. Do not put legal mapping or status decisions into
   331	hardcoded scripts.
Tool: ['/.agents/', '/.codex/', '/.env', '/.git/', '/.gitignore', '/.venv/', '/ALL_DATA/', '/README.md', '/__pycache__/', '/acquiring-contract-review.skill', '/conversation_history/', '/inputs/', '/large_tool_results/', '/llm.py', '/main.py', '/output/', '/outputs/', '/run_logs/', '/runs/', '/skills/', '/tmp/', '/tools/', '/workspace/']
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_00_gIITypZR1fTIcZLMCAvr1722', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_01_gJqrxlYPWSX6dL6AUPge4378', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/inputs'}, 'id': 'call_02_tGGqmo4KifwbAyVe5vgZ3265', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs'}, 'id': 'call_03_W4oKUiT7QoINBXbw7CVV9814', 'type': 'tool_call'}]
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
   189	- `atomic_links` are traceability rows only. They inherit the group
   190	  `relationship`; do not invent pair-level final statuses.
   191	- `contract_ids` contain clauses that provide material coverage for the group.
   192	  Background clauses can be cited in reasoning, but should not become final
   193	  candidates unless they affect coverage or status.
   194	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   195	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   196	  matrix closures. Do not use it to invent final conclusions.
   197	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   198	  not a risk for the current product, lot, terminal, payment method, or legal
   199	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   200	  final `unmatched_matrix`.
   201	- `unmatched_contract` contains only legally significant `extra_in_contract`
   202	  rows. Non-material rows stay in `coverage_ledger.contract`.
   203	- `relationship = aligned` requires empty `discrepancies`, `risk_level = none`,
   204	  and text-grounded confirmation that the contract package preserves the matrix
   205	  legal result.
   206	- `relationship = deviation` requires at least one discrepancy with `type`,
   207	  `description`, and `risk`.
   208	- Missing mandatory applicable requirements should normally be `high` risk.
   209	  Missing optional applicable requirements should normally be `low` or
   210	  conditional risk.
   211	- All final ids must be visible in source files. Do not use corrected,
   212	  inferred, translated, parenthetical, or internal ids.
   213	- Weak candidates do not appear in final `links`; use
   214	  `unmatched_matrix[].rejected_candidates`.
   215	
   216	## Excel Output
   217	
   218	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   219	
   220	Sheet 1: `Contract-Matrix`
   221	
   222	Columns:
   223	
   224	1. `contract_id`
   225	2. `contract_summary`
   226	3. `matrix_ids`
   227	4. `status`
   228	5. `risk_level`
   229	6. `comment`
   230	
   231	Rules:
   232	
   233	- one row per group-level contract-to-matrix finding;
   234	- `matrix_ids` contains the full matrix id set for the group;
   235	- status is `aligned`, `deviation`, or `extra_in_contract`;
   236	- contract-only extras have blank `matrix_ids`.
   237	
   238	Sheet 2: `Only in Matrix`
   239	
   240	Columns:
   241	
   242	1. `matrix_id`
   243	2. `requirement`
   244	3. `required_type`
   245	4. `risk_level`
   246	5. `comment`
   247	
   248	Rules:
   249	
   250	- one row per final `unmatched_matrix` item;
   251	- include optional applicable missing as low/conditional risk;
   252	- do not include out-of-scope / not-applicable requirements;
   253	- do not include non-evaluable headings or purely technical rows.
   254	
   255	## Bad Output Patterns
   256	
   257	Do not output:
   258	
   259	- multiple competing final JSON files;
   260	- pair-level final statuses as the primary answer;
   261	- `deviation` for unselected slash alternatives;
   262	- `deviation` for heading/title/label changes alone;
   263	- final `unmatched_contract` rows for definitions without legal effect;
   264	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   265	  requirements;
   266	- final ids that exist only in helper scripts or working ledgers;
   267	- `extra_in_contract` with empty risk;
   268	- `aligned` with non-empty discrepancies;
   269	- `missing_in_contract` where a weak candidate is silently treated as a link;
   270	- final conclusions based only on extracted fields without source-text evidence.
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
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/outputs/working/']
AI: Now let me read the input files and check what's already in the working directory.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_EXssZ54ZGcXBRKCO7Zun5331', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_KagRrLVCYpBcnGmG4b1c6714', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_02_UjuAvfgN4XX3ELQTzfNO5480', 'type': 'tool_call'}]
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
Tool: ['/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/coverage_ledger.json', '/outputs/working/create_coverage_ledger.py', '/outputs/working/enrich_propositions.py', '/outputs/working/legal_propositions.json', '/outputs/working/working_artifact_validation.json']
AI: Good. I can see that working artifacts already exist. Let me now read the rest of the contract and matrix, and also check the existing working artifacts to understand the current state.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_pAVwOYq5bpdzTFI9wXpW6055', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 200}, 'id': 'call_01_OeZor4iXdkLgHOCLDjpD4807', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 200}, 'id': 'call_02_B73FjE6I4Uh4baiuc1RT4278', 'type': 'tool_call'}]
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
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора.\nПри изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о Т",
     7	      "type": "operative",
     8	      "materiality": "evaluable",
     9	      "protected_party": "Bank",
    10	      "bound_party": "Merchant",
    11	      "right_or_obligation": "right",
    12	      "legal_object": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    13	      "trigger": "изменении информации о тст предприятие предоставляет в банк в соответствии с п",
    14	      "deadline": "",
    15	      "amount_formula_cap": "",
    16	      "procedure_channel": "electronic",
    17	      "liability_remedy": "",
    18	      "scope_options": [],
    19	      "consequence": "refusal_right",
    20	      "applicability_filters": {
    21	        "required_type": "mandatory",
    22	        "only_for_product": "common",
    23	        "only_for_lot": "common",
    24	        "only_for_terminal": "common",
    25	        "payment_method": "common"
    26	      }
    27	    },
    28	    {
    29	      "id": "2.2",
    30	      "source_text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. ",
    31	      "source_excerpt": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. ",
    32	      "type": "operative",
    33	      "materiality": "evaluable",
    34	      "protected_party": "Both",
    35	      "bound_party": "Both",
    36	      "right_or_obligation": "duty",
    37	      "legal_object": "Расчёты производятся в рублях Российской Федерации",
    38	      "trigger": "",
    39	      "deadline": "",
    40	      "amount_formula_cap": "",
    41	      "procedure_channel": "",
    42	      "liability_remedy": "",
    43	      "scope_options": [],
    44	      "consequence": "",
    45	      "applicability_filters": {
    46	        "required_type": "mandatory",
    47	        "only_for_product": "common",
    48	        "only_for_lot": "common",
    49	        "only_for_terminal": "common",
    50	        "payment_method": "common"
    51	      }
    52	    },
    53	    {
    54	      "id": "2.3.1",
    55	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    56	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с исполь",
    57	      "type": "operative",
    58	      "materiality": "evaluable",
    59	      "protected_party": "Both",
    60	      "bound_party": "Both",
    61	      "right_or_obligation": "duty",
    62	      "legal_object": "Обмен информацией по электронной почте",
    63	      "trigger": "если иное не предусмотрено в договоре",
    64	      "deadline": "",
    65	      "amount_formula_cap": "",
    66	      "procedure_channel": "electronic",
    67	      "liability_remedy": "",
    68	      "scope_options": [],
    69	      "consequence": "",
    70	      "applicability_filters": {
    71	        "required_type": "mandatory",
    72	        "only_for_product": "common",
    73	        "only_for_lot": "common",
    74	        "only_for_terminal": "common",
    75	        "payment_method": "common"
    76	      }
    77	    },
    78	    {
    79	      "id": "2.3.2",
    80	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
    81	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 по",
    82	      "type": "operative",
    83	      "materiality": "evaluable",
    84	      "protected_party": "Both",
    85	      "bound_party": "Both",
    86	      "right_or_obligation": "duty",
    87	      "legal_object": "Обмен документами посредством системы ДБО или аналогичных систем Банка",
    88	      "trigger": "",
    89	      "deadline": "",
    90	      "amount_formula_cap": "",
    91	      "procedure_channel": "DBO",
    92	      "liability_remedy": "",
    93	      "scope_options": [],
    94	      "consequence": "",
    95	      "applicability_filters": {
    96	        "required_type": "mandatory",
    97	        "only_for_product": "common",
    98	        "only_for_lot": "common",
    99	        "only_for_terminal": "common",
   100	        "payment_method": "common"
   101	      }
   102	    },
   103	    {
   104	      "id": "2.3.3",
   105	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   106	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем на",
   107	      "type": "operative",
   108	      "materiality": "evaluable",
   109	      "protected_party": "Both",
   110	      "bound_party": "Both",
   111	      "right_or_obligation": "duty",
   112	      "legal_object": "Обмен документами с доставкой нарочным или курьером",
   113	      "trigger": "",
   114	      "deadline": "",
   115	      "amount_formula_cap": "",
   116	      "procedure_channel": "postal",
   117	      "liability_remedy": "",
   118	      "scope_options": [],
   119	      "consequence": "",
   120	      "applicability_filters": {
   121	        "required_type": "optional",
   122	        "only_for_product": "common",
   123	        "only_for_lot": "common",
   124	        "only_for_terminal": "common",
   125	        "payment_method": "common"
   126	      }
   127	    },
   128	    {
   129	      "id": "2.3.4",
   130	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   131	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем на",
   132	      "type": "operative",
   133	      "materiality": "evaluable",
   134	      "protected_party": "Both",
   135	      "bound_party": "Both",
   136	      "right_or_obligation": "duty",
   137	      "legal_object": "Обмен документами через заказное письмо",
   138	      "trigger": "",
   139	      "deadline": "",
   140	      "amount_formula_cap": "",
   141	      "procedure_channel": "postal",
   142	      "liability_remedy": "",
   143	      "scope_options": [],
   144	      "consequence": "",
   145	      "applicability_filters": {
   146	        "required_type": "optional",
   147	        "only_for_product": "common",
   148	        "only_for_lot": "common",
   149	        "only_for_terminal": "common",
   150	        "payment_method": "common"
   151	      }
   152	    },
   153	    {
   154	      "id": "2.3.5",
   155	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью   (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   156	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем об",
   157	      "type": "operative",
   158	      "materiality": "evaluable",
   159	      "protected_party": "Both",
   160	      "bound_party": "Both",
   161	      "right_or_obligation": "duty",
   162	      "legal_object": "Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП",
   163	      "trigger": "",
   164	      "deadline": "",
   165	      "amount_formula_cap": "",
   166	      "procedure_channel": "electronic",
   167	      "liability_remedy": "",
   168	      "scope_options": [],
   169	      "consequence": "",
   170	      "applicability_filters": {
   171	        "required_type": "mandatory",
   172	        "only_for_product": "common",
   173	        "only_for_lot": "common",
   174	        "only_for_terminal": "common",
   175	        "payment_method": "common"
   176	      }
   177	    },
   178	    {
   179	      "id": "2.3.6",
   180	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   181	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем об",
   182	      "type": "operative",
   183	      "materiality": "evaluable",
   184	      "protected_party": "Both",
   185	      "bound_party": "Both",
   186	      "right_or_obligation": "duty",
   187	      "legal_object": "Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок)",
   188	      "trigger": "",
   189	      "deadline": "",
   190	      "amount_formula_cap": "",
   191	      "procedure_channel": "electronic",
   192	      "liability_remedy": "",
   193	      "scope_options": [],
   194	      "consequence": "",
   195	      "applicability_filters": {
   196	        "required_type": "mandatory",
   197	        "only_for_product": "common",
   198	        "only_for_lot": "fz_44",
   199	        "only_for_terminal": "common",
   200	        "payment_method": "common"
AI: Let me continue reading the remaining parts of the matrix and the existing working artifacts to understand the full picture.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 400, 'limit': 500}, 'id': 'call_00_THf1uj7MxrxMrIMZD6OY7835', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 200, 'limit': 300}, 'id': 'call_01_iqOV0PG6GJydFed3ygeW8163', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_02_4AvJERAKWq9wQWCMl7Ke4671', 'type': 'tool_call'}]
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
   701	   "Доступ для замены терминалов",
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
Tool:    201	      }
   202	    },
   203	    {
   204	      "id": "2.3.7",
   205	      "source_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в:\n• п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;\n• п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма);\n• п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;\n•  п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке;\n• п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   206	      "source_excerpt": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 че",
   207	      "type": "operative",
   208	      "materiality": "evaluable",
   209	      "protected_party": "Both",
   210	      "bound_party": "Both",
   211	      "right_or_obligation": "duty",
   212	      "legal_object": "Обмен информацией через обращение в службу поддержки Банка",
   213	      "trigger": "направления способом",
   214	      "deadline": "",
   215	      "amount_formula_cap": "",
   216	      "procedure_channel": "electronic",
   217	      "liability_remedy": "",
   218	      "scope_options": [],
   219	      "consequence": "",
   220	      "applicability_filters": {
   221	        "required_type": "optional",
   222	        "only_for_product": "common",
   223	        "only_for_lot": "common",
   224	        "only_for_terminal": "common",
   225	        "payment_method": "common"
   226	      }
   227	    },
   228	    {
   229	      "id": "2.4",
   230	      "source_text": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   231	      "source_excerpt": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   232	      "type": "operative",
   233	      "materiality": "evaluable",
   234	      "protected_party": "Both",
   235	      "bound_party": "Both",
   236	      "right_or_obligation": "duty",
   237	      "legal_object": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   238	      "trigger": "",
   239	      "deadline": "",
   240	      "amount_formula_cap": "",
   241	      "procedure_channel": "",
   242	      "liability_remedy": "",
   243	      "scope_options": [],
   244	      "consequence": "",
   245	      "applicability_filters": {
   246	        "required_type": "optional",
   247	        "only_for_product": "common",
   248	        "only_for_lot": "common",
   249	        "only_for_terminal": "common",
   250	        "payment_method": "common"
   251	      }
   252	    },
   253	    {
   254	      "id": "2.5.1.1",
   255	      "source_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;",
   256	      "source_excerpt": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением едино",
   257	      "type": "operative",
   258	      "materiality": "evaluable",
   259	      "protected_party": "Both",
   260	      "bound_party": "Both",
   261	      "right_or_obligation": "duty",
   262	      "legal_object": "SberPayOnline подключается автоматически при подключении Интернет-эквайринга",
   263	      "trigger": "",
   264	      "deadline": "",
   265	      "amount_formula_cap": "",
   266	      "procedure_channel": "",
   267	      "liability_remedy": "",
   268	      "scope_options": [],
   269	      "consequence": "",
   270	      "applicability_filters": {
   271	        "required_type": "mandatory",
   272	        "only_for_product": "internet_acquiring",
   273	        "only_for_lot": "common",
   274	        "only_for_terminal": "common",
   275	        "payment_method": "common"
   276	      }
   277	    },
   278	    {
   279	      "id": "2.5.2.1",
   280	      "source_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.",
   281	      "source_excerpt": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носител",
   282	      "type": "operative",
   283	      "materiality": "evaluable",
   284	      "protected_party": "Both",
   285	      "bound_party": "Both",
   286	      "right_or_obligation": "duty",
   287	      "legal_object": "подключение SberPayFaceScan оформляется на бумажном носителе",
   288	      "trigger": "",
   289	      "deadline": "",
   290	      "amount_formula_cap": "",
   291	      "procedure_channel": "",
   292	      "liability_remedy": "",
   293	      "scope_options": [],
   294	      "consequence": "",
   295	      "applicability_filters": {
   296	        "required_type": "mandatory",
   297	        "only_for_product": "trade_acquiring",
   298	        "only_for_lot": "common",
   299	        "only_for_terminal": "common",
   300	        "payment_method": "sber_pay_face_scan"
   301	      }
   302	    },
   303	    {
   304	      "id": "2.6.1.1",
   305	      "source_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.",
   306	      "source_excerpt": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-те",
   307	      "type": "operative",
   308	      "materiality": "evaluable",
   309	      "protected_party": "Both",
   310	      "bound_party": "Both",
   311	      "right_or_obligation": "duty",
   312	      "legal_object": "OR-код подключается при установке Смарт-терминала Банка",
   313	      "trigger": "установке программного обеспечения банка для смарт-терминала предприятия в тст",
   314	      "deadline": "",
   315	      "amount_formula_cap": "",
   316	      "procedure_channel": "electronic",
   317	      "liability_remedy": "",
   318	      "scope_options": [],
   319	      "consequence": "",
   320	      "applicability_filters": {
   321	        "required_type": "mandatory",
   322	        "only_for_product": "trade_acquiring",
   323	        "only_for_lot": "common",
   324	        "only_for_terminal": "smart",
   325	        "payment_method": "qr"
   326	      }
   327	    },
   328	    {
   329	      "id": "2.6.2.1",
   330	      "source_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;",
   331	      "source_excerpt": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предпри",
   332	      "type": "operative",
   333	      "materiality": "evaluable",
   334	      "protected_party": "Both",
   335	      "bound_party": "Both",
   336	      "right_or_obligation": "duty",
   337	      "legal_object": "возможность использования QR-кода на ККТ с собственным ПО Предприятия",
   338	      "trigger": "подключении qr-api размещены на официальном сайте банка",
   339	      "deadline": "",
   340	      "amount_formula_cap": "",
   341	      "procedure_channel": "electronic",
   342	      "liability_remedy": "liability",
   343	      "scope_options": [],
   344	      "consequence": "",
   345	      "applicability_filters": {
   346	        "required_type": "mandatory",
   347	        "only_for_product": "trade_acquiring",
   348	        "only_for_lot": "common",
   349	        "only_for_terminal": "common",
   350	        "payment_method": "qr"
   351	      }
   352	    },
   353	    {
   354	      "id": "2.6.2.2",
   355	      "source_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору.",
   356	      "source_excerpt": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предпри",
   357	      "type": "operative",
   358	      "materiality": "evaluable",
   359	      "protected_party": "Both",
   360	      "bound_party": "Both",
   361	      "right_or_obligation": "duty",
   362	      "legal_object": "возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ",
   363	      "trigger": "",
   364	      "deadline": "",
   365	      "amount_formula_cap": "",
   366	      "procedure_channel": "electronic",
   367	      "liability_remedy": "",
   368	      "scope_options": [],
   369	      "consequence": "",
   370	      "applicability_filters": {
   371	        "required_type": "mandatory",
   372	        "only_for_product": "trade_acquiring",
   373	        "only_for_lot": "common",
   374	        "only_for_terminal": "common",
   375	        "payment_method": "qr"
   376	      }
   377	    },
   378	    {
   379	      "id": "2.6.3.1",
   380	      "source_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: →  QR-код подключается при установке Электронного терминала в ТСТ;",
   381	      "source_excerpt": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором",
   382	      "type": "operative",
   383	      "materiality": "evaluable",
   384	      "protected_party": "Both",
   385	      "bound_party": "Both",
   386	      "right_or_obligation": "duty",
   387	      "legal_object": "QR-код подключается при установке Электронного терминала в ТСТ",
   388	      "trigger": "подключении на них qr-кода вендором",
   389	      "deadline": "",
   390	      "amount_formula_cap": "",
   391	      "procedure_channel": "electronic",
   392	      "liability_remedy": "",
   393	      "scope_options": [],
   394	      "consequence": "",
   395	      "applicability_filters": {
   396	        "required_type": "mandatory",
   397	        "only_for_product": "trade_acquiring",
   398	        "only_for_lot": "common",
   399	        "only_for_terminal": "common",
   400	        "payment_method": "qr"
   401	      }
   402	    },
   403	    {
   404	      "id": "2.6.3.2",
   405	      "source_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора.",
   406	      "source_excerpt": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором",
   407	      "type": "operative",
   408	      "materiality": "evaluable",
   409	      "protected_party": "Both",
   410	      "bound_party": "Both",
   411	      "right_or_obligation": "duty",
   412	      "legal_object": "отключение QR-кода возможно по инициативе Предприятия",
   413	      "trigger": "подключении на них qr-кода вендором",
   414	      "deadline": "",
   415	      "amount_formula_cap": "",
   416	      "procedure_channel": "electronic",
   417	      "liability_remedy": "",
   418	      "scope_options": [],
   419	      "consequence": "",
   420	      "applicability_filters": {
   421	        "required_type": "mandatory",
   422	        "only_for_product": "trade_acquiring",
   423	        "only_for_lot": "common",
   424	        "only_for_terminal": "common",
   425	        "payment_method": "qr"
   426	      }
   427	    },
   428	    {
   429	      "id": "2.7",
   430	      "source_text": "Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юридическую силу с Договором, оформленным на бумажном носителе, подписанным собственноручными подписями уполномоченных представителей Банка и Предприятия.",
   431	      "source_excerpt": "Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юрид",
   432	      "type": "operative",
   433	      "materiality": "evaluable",
   434	      "protected_party": "Both",
   435	      "bound_party": "Both",
   436	      "right_or_obligation": "duty",
   437	      "legal_object": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП ",
   438	      "trigger": "",
   439	      "deadline": "",
   440	      "amount_formula_cap": "",
   441	      "procedure_channel": "electronic",
   442	      "liability_remedy": "",
   443	      "scope_options": [],
   444	      "consequence": "",
   445	      "applicability_filters": {
   446	        "required_type": "optional",
   447	        "only_for_product": "common",
   448	        "only_for_lot": "common",
   449	        "only_for_terminal": "common",
   450	        "payment_method": "common"
   451	      }
   452	    },
   453	    {
   454	      "id": "3.1",
   455	      "source_text": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ/на Ресурсе и обработку информации на Электронных терминалах/Смарт-терминалах [1]/через СПЭП. Перечень Карт перечислен в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе к Договору, размещенном на Официальном сайте Банка",
   456	      "source_excerpt": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ/на Ресурсе и обработку информации на Электронных терминалах/Смарт-терминалах [1]/",
   457	      "type": "operative",
   458	      "materiality": "evaluable",
   459	      "protected_party": "Both",
   460	      "bound_party": "Both",
   461	      "right_or_obligation": "duty",
   462	      "legal_object": "Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Плати QR)",
   463	      "trigger": "",
   464	      "deadline": "",
   465	      "amount_formula_cap": "",
   466	      "procedure_channel": "electronic",
   467	      "liability_remedy": "",
   468	      "scope_options": [],
   469	      "consequence": "",
   470	      "applicability_filters": {
   471	        "required_type": "optional",
   472	        "only_for_product": "common",
   473	        "only_for_lot": "common",
   474	        "only_for_terminal": "common",
   475	        "payment_method": "common"
   476	      }
   477	    },
   478	    {
   479	      "id": "3.2",
   480	      "source_text": "«ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ/на Ресурсе.",
   481	      "source_excerpt": "«ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ/на Ресурсе.",
   482	      "type": "operative",
   483	      "materiality": "evaluable",
   484	      "protected_party": "Both",
   485	      "bound_party": "Both",
   486	      "right_or_obligation": "obligation",
   487	      "legal_object": "Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию",
   488	      "trigger": "",
   489	      "deadline": "",
   490	      "amount_formula_cap": "",
   491	      "procedure_channel": "",
   492	      "liability_remedy": "",
   493	      "scope_options": [],
   494	      "consequence": "",
   495	      "applicability_filters": {
   496	        "required_type": "optional",
   497	        "only_for_product": "common",
   498	        "only_for_lot": "common",
   499	        "only_for_terminal": "common",
   500	        "payment_method": "common"
Tool:      1	{
     2	  "product": [
     3	    "trade_acquiring"
     4	  ],
     5	  "lot": "44_fz",
     6	  "terminal": [
     7	    "pos",
     8	    "smart"
     9	  ],
    10	  "payment_method": [
    11	    "card",
    12	    "nfc",
    13	    "qr"
    14	  ],
    15	  "legal_regime": "44_fz",
    16	  "profile_evidence": {
    17	    "product": {
    18	      "determination": "trade_acquiring",
    19	      "evidence": [
    20	        "Контракт на оказание услуг по приему к оплате платежных (банковских) карт (услуги эквайринга) — п.1.1",
    21	        "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах — п.1.3",
    22	        "Техническое задание (Приложение №1) перечисляет 8 физических адресов ТСТ с указанием количества POS-терминалов для каждого",
    23	        "В Приложении №1.1 отмечен выбор: «Торговый эквайринг + Электронный терминал + QR-код» и «Торговый эквайринг + Cмарт-терминал + QR-код»",
    24	        "Интернет-эквайринг в Приложении №1.1 не выбран (поля для интернет-сайта и мобильного приложения не заполнены)",
    25	        "Платежно-пропускная система Заказчика — «Барс» НПО «Дата Крат» (не интернет-ресурс)"
    26	      ],
    27	      "excluded_products": {
    28	        "internet_acquiring": "В Приложении №1.1 раздел «ИНТЕРНЕТ ЭКВАЙРИНГ» не заполнен — не указаны ни сайт, ни мобильное приложение, ни SberPay Online для интернет-эквайринга. Контракт касается только физических ТСТ."
    29	      }
    30	    },
    31	    "lot": {
    32	      "determination": "44_fz",
    33	      "evidence": [
    34	        "Прямая ссылка на Федеральный закон № 44-ФЗ в преамбуле контракта",
    35	        "Идентификационный код закупки (ИКЗ) 251231702678823170100060016619244 — п.1.1",
    36	        "Ссылки на статьи 34, 51, 94, 95, 96, 112 Федерального закона № 44-ФЗ в тексте контракта",
    37	        "Процедура приемки через ЕИС с УКЭП — раздел 8",
    38	        "Штрафы по Постановлению № 1042 — раздел 7",
    39	        "Заказчик — ФГБУ (федеральное государственное бюджетное учреждение)"
    40	      ]
    41	    },
    42	    "terminal": {
    43	      "determination": ["pos", "smart"],
    44	      "evidence": {
    45	        "pos": [
    46	          "Техническое задание (Приложение №1) требует установку POS-терминалов в 8 ТСТ (всего 14 POS-терминалов)",
    47	          "Термин «Электронный терминал» определён в п.2.2 как «электронное программно-техническое устройство исполнителя... позволяющее осуществлять прием карт в ТСТ»",
    48	          "В Приложении №1.1 раздел «ТОРГОВЫЙ ЭКВАЙРИНГ» — «Электронные терминалы (без учета mPOS)»",
    49	          "Типы подключения: выделенная линия (Ethernet), WI-FI, GPRS"
    50	        ],
    51	        "smart": [
    52	          "В Приложении №1.1 отмечен выбор «Торговый эквайринг + Cмарт-терминал + QR-код»",
    53	          "Указан тип смарт-терминала: Эвотор+",
    54	          "Указаны СТ-7.3 — 3 шт.",
    55	          "Пакет: «Максимальный» с ФН-36",
    56	          "В контракте п.5.7: штраф за невозврат Смарт-терминала — 25 000 руб."
    57	        ]
    58	      },
    59	      "excluded_terminals": {
    60	        "biometric": "Биометрические терминалы в Приложении №1.1 не отмечены (поле «Биометрические терминалы» пустое)",
    61	        "mpos": "mPOS терминалы в Приложении №1.1 не отмечены (поле «Мобильные терминалы (mPOS)» пустое)",
    62	        "trade_automate": "Торговый автомат в Приложении №1.1 не отмечен"
    63	      }
    64	    },
    65	    "payment_method": {
    66	      "determination": ["card", "nfc", "qr"],
    67	      "evidence": {
    68	        "card": [
    69	          "Предмет контракта — «прием к оплате платежных (банковских) карт» — п.1.1",
    70	          "Перечень карт в Техническом задании: НСПК «МИР», VISA International, MasterCard (MasterCard, MasterCard Electronic, Maestro)",
    71	          "Определение банковской карты в п.2.1.1"
    72	        ],
    73	        "nfc": [
    74	          "Определение карты в п.2.1.1 включает «мобильное устройство, которое позволяет его покупателю совершать операции по технологии беспроводной высокочастотной связи малого радиуса действия (NFC)»",
    75	          "Техническое задание п.5: «Терминалы Исполнителя должны иметь возможность принятия бесконтактной оплаты»"
    76	        ],
    77	        "qr": [
    78	          "Техническое задание п.5: «Возможность вывода QR-кода для безналичной оплаты на дисплей терминала»",
    79	          "В Приложении №1.1 отмечен выбор «QR-код» в разделе альтернативных способов приема оплаты",
    80	          "В Приложении №1.1 отмечены типы подключения QR-кода: QR-API и QR-Вендор (Эвотор)",
    81	          "В Приложении №1.1 раздел «ИНФОРМАЦИЯ ОБ УСЛУГАХ»: «Торговый эквайринг + Электронный терминал + QR-код» и «Торговый эквайринг + Cмарт-терминал + QR-код»"
    82	        ]
    83	      },
    84	      "excluded_payment_methods": {
    85	        "sber_pay": "SberPay (SberPayOnline, SberPayFaceScan) не упоминается в контракте. В Приложении №1.1 поле SberPay Online не заполнено.",
    86	        "sber_pay_face_scan": "Биометрическая идентификация в Приложении №1.1 не отмечена (поле «проведение операций с биометрическим методом идентификации» пустое)",
    87	        "qr_sber_pay": "SberPayQR отдельно не упоминается; QR-код указан как общий способ оплаты без привязки к SberPay"
    88	      }
    89	    },
    90	    "legal_regime": {
    91	      "determination": "44_fz",
    92	      "evidence": [
    93	        "Прямое указание в преамбуле: «с соблюдением требований Федерального закона от 5 апреля 2013 г. № 44-ФЗ»",
    94	        "ИКЗ: 251231702678823170100060016619244",
    95	        "Заказчик — ФГБУ «Кавказский государственный заповедник» (бюджетное учреждение)",
    96	        "Процедуры приемки, расторжения, ответственности — по 44-ФЗ",
    97	        "Электронный документооборот через ЕИС с УКЭП"
    98	      ]
    99	    }
   100	  },
AI: Now let me read the rest of the matrix and the contract legal propositions to understand the full scope. Let me also check the existing coverage ledger and validation.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 900, 'limit': 500}, 'id': 'call_00_l0aoImY5Plv1I0a3wPFI3357', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 500, 'limit': 500}, 'id': 'call_01_vGG4Xax7cP0KevIP5gMo1050', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/working_artifact_validation.json'}, 'id': 'call_02_8Dxvt4Jowa3D3OAn4Kie2867', 'type': 'tool_call'}]
Tool:    901	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Использовать API и сведения, передаваемые посредством QR-API, в границах прав и функциональных возможностей такого API и его описания, изложенного в Порядке, условиях и ответственности сторон при подключении QR-API, размещенном на Официальном сайте Банка.",
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
  1201	 },
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
Tool:    501	      }
   502	    },
   503	    {
   504	      "id": "3.3",
   505	      "source_text": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров/услуг в ТСТ[7]/на Ресурсе – к ИЭ[8]",
   506	      "source_excerpt": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров/услуг в ТСТ[7]/на Ресурсе – к ИЭ[8]",
   507	      "type": "operative",
   508	      "materiality": "evaluable",
   509	      "protected_party": "Both",
   510	      "bound_party": "Both",
   511	      "right_or_obligation": "duty",
   512	      "legal_object": "Предприятие перечисляет Банку плату за проведение расчётов ежемесячно",
   513	      "trigger": "",
   514	      "deadline": "",
   515	      "amount_formula_cap": "",
   516	      "procedure_channel": "",
   517	      "liability_remedy": "",
   518	      "scope_options": [],
   519	      "consequence": "",
   520	      "applicability_filters": {
   521	        "required_type": "mandatory",
   522	        "only_for_product": "common",
   523	        "only_for_lot": "common",
   524	        "only_for_terminal": "common",
   525	        "payment_method": "common"
   526	      }
   527	    },
   528	    {
   529	      "id": "4.1.1",
   530	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3.1 и п. 2.3.2 настоящего Договора.",
   531	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3",
   532	      "type": "operative",
   533	      "materiality": "evaluable",
   534	      "protected_party": "Merchant",
   535	      "bound_party": "Bank",
   536	      "right_or_obligation": "right",
   537	      "legal_object": "Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов с Банком",
   538	      "trigger": "",
   539	      "deadline": "",
   540	      "amount_formula_cap": "",
   541	      "procedure_channel": "",
   542	      "liability_remedy": "",
   543	      "scope_options": [],
   544	      "consequence": "",
   545	      "applicability_filters": {
   546	        "required_type": "optional",
   547	        "only_for_product": "common",
   548	        "only_for_lot": "common",
   549	        "only_for_terminal": "common",
   550	        "payment_method": "qr"
   551	      }
   552	    },
   553	    {
   554	      "id": "4.1.2",
   555	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, указанному в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.",
   556	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, ",
   557	      "type": "operative",
   558	      "materiality": "evaluable",
   559	      "protected_party": "Merchant",
   560	      "bound_party": "Bank",
   561	      "right_or_obligation": "right",
   562	      "legal_object": "закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов",
   563	      "trigger": "",
   564	      "deadline": "",
   565	      "amount_formula_cap": "",
   566	      "procedure_channel": "electronic",
   567	      "liability_remedy": "",
   568	      "scope_options": [],
   569	      "consequence": "",
   570	      "applicability_filters": {
   571	        "required_type": "optional",
   572	        "only_for_product": "common",
   573	        "only_for_lot": "common",
   574	        "only_for_terminal": "common",
   575	        "payment_method": "common"
   576	      }
   577	    },
   578	    {
   579	      "id": "4.1.3",
   580	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Мобильных устройствах Предприятия, а также на ККТ, принадлежащей Предприятию, или на видном месте, в том числе на бумажном носителе.",
   581	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Моб",
   582	      "type": "operative",
   583	      "materiality": "evaluable",
   584	      "protected_party": "Merchant",
   585	      "bound_party": "Bank",
   586	      "right_or_obligation": "right",
   587	      "legal_object": "Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR",
   588	      "trigger": "",
   589	      "deadline": "",
   590	      "amount_formula_cap": "",
   591	      "procedure_channel": "electronic",
   592	      "liability_remedy": "",
   593	      "scope_options": [],
   594	      "consequence": "",
   595	      "applicability_filters": {
   596	        "required_type": "optional",
   597	        "only_for_product": "trade_acquiring",
   598	        "only_for_lot": "common",
   599	        "only_for_terminal": "common",
   600	        "payment_method": "qr_sber_pay"
   601	      }
   602	    },
   603	    {
   604	      "id": "4.2.1",
   605	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настоящего Договора. ",
   606	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настояще",
   607	      "type": "operative",
   608	      "materiality": "evaluable",
   609	      "protected_party": "Bank",
   610	      "bound_party": "Merchant",
   611	      "right_or_obligation": "obligation",
   612	      "legal_object": "Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям",
   613	      "trigger": "наличии) в соответствии с тарифами банка",
   614	      "deadline": "",
   615	      "amount_formula_cap": "",
   616	      "procedure_channel": "",
   617	      "liability_remedy": "",
   618	      "scope_options": [],
   619	      "consequence": "",
   620	      "applicability_filters": {
   621	        "required_type": "mandatory",
   622	        "only_for_product": "common",
   623	        "only_for_lot": "common",
   624	        "only_for_terminal": "common",
   625	        "payment_method": "common"
   626	      }
   627	    },
   628	    {
   629	      "id": "4.2.2",
   630	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/ инструктивных материалах, предоставляемых Банком.",
   631	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/ инструктивных материалах, предоставляемых Банком.",
   632	      "type": "operative",
   633	      "materiality": "evaluable",
   634	      "protected_party": "Bank",
   635	      "bound_party": "Merchant",
   636	      "right_or_obligation": "obligation",
   637	      "legal_object": "Обязанность Предприятия соблюдать положения Договора (наличие формулировки об обязанности соблюдать)",
   638	      "trigger": "",
   639	      "deadline": "",
   640	      "amount_formula_cap": "",
   641	      "procedure_channel": "",
   642	      "liability_remedy": "",
   643	      "scope_options": [],
   644	      "consequence": "",
   645	      "applicability_filters": {
   646	        "required_type": "optional",
   647	        "only_for_product": "common",
   648	        "only_for_lot": "common",
   649	        "only_for_terminal": "common",
   650	        "payment_method": "common"
   651	      }
   652	    },
   653	    {
   654	      "id": "4.2.3",
   655	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление Предприятия с изменениями, внесенными в вышеуказанные документы, не является основанием для их неприменения Банком.",
   656	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоеврем",
   657	      "type": "operative",
   658	      "materiality": "evaluable",
   659	      "protected_party": "Bank",
   660	      "bound_party": "Merchant",
   661	      "right_or_obligation": "obligation",
   662	      "legal_object": "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов",
   663	      "trigger": "",
   664	      "deadline": "",
   665	      "amount_formula_cap": "",
   666	      "procedure_channel": "",
   667	      "liability_remedy": "",
   668	      "scope_options": [],
   669	      "consequence": "",
   670	      "applicability_filters": {
   671	        "required_type": "optional",
   672	        "only_for_product": "common",
   673	        "only_for_lot": "fz_223",
   674	        "only_for_terminal": "common",
   675	        "payment_method": "common"
   676	      }
   677	    },
   678	    {
   679	      "id": "4.2.4",
   680	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с использованием Карт/NFC-карт/SberPay/Плати QR, в случае если это не противоречит требованиям законодательства Российской Федерации.",
   681	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с испол",
   682	      "type": "operative",
   683	      "materiality": "evaluable",
   684	      "protected_party": "Bank",
   685	      "bound_party": "Merchant",
   686	      "right_or_obligation": "obligation",
   687	      "legal_object": "Предприятие обязано размещать информационные материалы Банка о способах оплаты",
   688	      "trigger": "если это не противоречит требованиям законодательства российской федерации",
   689	      "deadline": "",
   690	      "amount_formula_cap": "",
   691	      "procedure_channel": "",
   692	      "liability_remedy": "",
   693	      "scope_options": [],
   694	      "consequence": "",
   695	      "applicability_filters": {
   696	        "required_type": "optional",
   697	        "only_for_product": "common",
   698	        "only_for_lot": "common",
   699	        "only_for_terminal": "common",
   700	        "payment_method": "common"
   701	      }
   702	    },
   703	    {
   704	      "id": "4.2.5",
   705	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, в течение всего рабочего времени Предприятия. Не выдавать по Картам наличные денежные средства[3]. Не принимать от Покупателя более 2 (двух) различных Карт.",
   706	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, в течение всего рабочего времени Предприятия. Не выд",
   707	      "type": "operative",
   708	      "materiality": "evaluable",
   709	      "protected_party": "Bank",
   710	      "bound_party": "Merchant",
   711	      "right_or_obligation": "obligation",
   712	      "legal_object": "Принимать к оплате все карты из списка в течение всего рабочего времени",
   713	      "trigger": "",
   714	      "deadline": "всего рабочего времени предприятия",
   715	      "amount_formula_cap": "",
   716	      "procedure_channel": "",
   717	      "liability_remedy": "",
   718	      "scope_options": [],
   719	      "consequence": "",
   720	      "applicability_filters": {
   721	        "required_type": "mandatory",
   722	        "only_for_product": "common",
   723	        "only_for_lot": "common",
   724	        "only_for_terminal": "common",
   725	        "payment_method": "common"
   726	      }
   727	    },
   728	    {
   729	      "id": "4.2.6",
   730	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм.",
   731	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм.",
   732	      "type": "operative",
   733	      "materiality": "evaluable",
   734	      "protected_party": "Bank",
   735	      "bound_party": "Merchant",
   736	      "right_or_obligation": "obligation",
   737	      "legal_object": "Предприятие обязано проводить Операцию оплаты единой суммой без разделения на части",
   738	      "trigger": "",
   739	      "deadline": "",
   740	      "amount_formula_cap": "",
   741	      "procedure_channel": "",
   742	      "liability_remedy": "",
   743	      "scope_options": [],
   744	      "consequence": "",
   745	      "applicability_filters": {
   746	        "required_type": "mandatory",
   747	        "only_for_product": "common",
   748	        "only_for_lot": "common",
   749	        "only_for_terminal": "common",
   750	        "payment_method": "common"
   751	      }
   752	    },
   753	    {
   754	      "id": "4.2.7",
   755	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не использовать реквизиты Карты/Платежного счета, которые стали доступны Предприятию/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупателя.",
   756	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не использовать реквизиты Карты/Платежного счета, которые стали доступны Предприятию/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупател",
   757	      "type": "operative",
   758	      "materiality": "evaluable",
   759	      "protected_party": "Bank",
   760	      "bound_party": "Merchant",
   761	      "right_or_obligation": "obligation",
   762	      "legal_object": "Не использовать реквизиты Карты без присутствия или распоряжения Покупателя",
   763	      "trigger": "",
   764	      "deadline": "",
   765	      "amount_formula_cap": "",
   766	      "procedure_channel": "",
   767	      "liability_remedy": "",
   768	      "scope_options": [],
   769	      "consequence": "",
   770	      "applicability_filters": {
   771	        "required_type": "mandatory",
   772	        "only_for_product": "common",
   773	        "only_for_lot": "common",
   774	        "only_for_terminal": "common",
   775	        "payment_method": "common"
   776	      }
   777	    },
   778	    {
   779	      "id": "4.2.8",
   780	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства.",
   781	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства.",
   782	      "type": "operative",
   783	      "materiality": "evaluable",
   784	      "protected_party": "Bank",
   785	      "bound_party": "Merchant",
   786	      "right_or_obligation": "obligation",
   787	      "legal_object": "Предприятие предоставляет полный набор товаров/услуг покупателям",
   788	      "trigger": "расчетах за наличные денежные средства",
   789	      "deadline": "",
   790	      "amount_formula_cap": "",
   791	      "procedure_channel": "",
   792	      "liability_remedy": "",
   793	      "scope_options": [],
   794	      "consequence": "",
   795	      "applicability_filters": {
   796	        "required_type": "mandatory",
   797	        "only_for_product": "common",
   798	        "only_for_lot": "common",
   799	        "only_for_terminal": "common",
   800	        "payment_method": "common"
   801	      }
   802	    },
   803	    {
   804	      "id": "4.2.9",
   805	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций в Торгово-сервисных точках/на Ресурсе к Договору и нести ответственность за правильность указанной в документах информации.",
   806	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций в Торгово-сервисных точках/на Ресурсе к Договору и нести ответственность за пра",
   807	      "type": "operative",
   808	      "materiality": "evaluable",
   809	      "protected_party": "Bank",
   810	      "bound_party": "Merchant",
   811	      "right_or_obligation": "obligation",
   812	      "legal_object": "Предприятие обязано проводить операции в соответствии с Порядком проведения операций",
   813	      "trigger": "",
   814	      "deadline": "",
   815	      "amount_formula_cap": "",
   816	      "procedure_channel": "",
   817	      "liability_remedy": "liability",
   818	      "scope_options": [],
   819	      "consequence": "",
   820	      "applicability_filters": {
   821	        "required_type": "mandatory",
   822	        "only_for_product": "common",
   823	        "only_for_lot": "common",
   824	        "only_for_terminal": "common",
   825	        "payment_method": "common"
   826	      }
   827	    },
   828	    {
   829	      "id": "4.2.10",
   830	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Хранить в недоступном для третьих лиц месте Документы по операциям (Чеки, кассовые чеки, распоряжения Покупателя, документы, подтверждающие факт заключения договора и проведения каждой Операции при проведении Повторяющихся платежей, документы, подтверждающие факт передачи Товара/оказания услуги и т.п.) не менее 13 (тринадцати) месяцев с даты совершения Операции и передавать их копии в Банк по его запросу путем направления ответа на первоначальный запрос по электронным каналам связи, указанным в п.2.3.1., п.2.3.2. Договора в течение 3 (трех) рабочих дней с даты получения запроса. Предоставленные документы должны быть надлежащего качества (изображение четкое, размер не менее оригинального документа). ",
   831	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Хранить в недоступном для третьих лиц месте Документы по операциям (Чеки, кассовые чеки, распоряжения Покупателя, документы, подтверждающие факт заключения договора и проведения к",
   832	      "type": "operative",
   833	      "materiality": "evaluable",
   834	      "protected_party": "Bank",
   835	      "bound_party": "Merchant",
   836	      "right_or_obligation": "obligation",
   837	      "legal_object": "хранение документов по операциям (сам факт хранения и срок храннеия)",
   838	      "trigger": "проведении повторяющихся платежей",
   839	      "deadline": "3 (трех) рабочих дней",
   840	      "amount_formula_cap": "",
   841	      "procedure_channel": "electronic",
   842	      "liability_remedy": "",
   843	      "scope_options": [],
   844	      "consequence": "",
   845	      "applicability_filters": {
   846	        "required_type": "mandatory",
   847	        "only_for_product": "common",
   848	        "only_for_lot": "common",
   849	        "only_for_terminal": "common",
   850	        "payment_method": "common"
   851	      }
   852	    },
   853	    {
   854	      "id": "4.2.11",
   855	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Передавать в Банк по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Банка письменное заявление с изложением обстоятельств проведения Операции в ТСТ /на Ресурсе . В случае утраты составленных Документов по операции немедленно сообщить об утрате в Банк одним из способов, указанных в п. 2.3.1, п. 2.3.2 Договора. ",
   856	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Передавать в Банк по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Банка письменное заявление с изложением обстоятельств проведения Операции в ТСТ /на Ре",
   857	      "type": "operative",
   858	      "materiality": "evaluable",
   859	      "protected_party": "Bank",
   860	      "bound_party": "Merchant",
   861	      "right_or_obligation": "obligation",
   862	      "legal_object": "Передача заявления в банк с изложением обстоятельств проведения Операции в течение 3 рабочих дней после получения запроса",
   863	      "trigger": "",
   864	      "deadline": "3 (трех) рабочих дней",
   865	      "amount_formula_cap": "",
   866	      "procedure_channel": "",
   867	      "liability_remedy": "",
   868	      "scope_options": [],
   869	      "consequence": "",
   870	      "applicability_filters": {
   871	        "required_type": "mandatory",
   872	        "only_for_product": "common",
   873	        "only_for_lot": "common",
   874	        "only_for_terminal": "common",
   875	        "payment_method": "common"
   876	      }
   877	    },
   878	    {
   879	      "id": "4.2.12",
   880	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг, в течение 5 (пяти) рабочих дней с даты их выставления.",
   881	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, указанному в Заявлении Предприятия на пр",
   882	      "type": "operative",
   883	      "materiality": "evaluable",
   884	      "protected_party": "Bank",
   885	      "bound_party": "Merchant",
   886	      "right_or_obligation": "obligation",
   887	      "legal_object": "Предприятие обязано акцептовать платежные требования и счета на оплату. Пункт относится только к оплате счетов",
   888	      "trigger": "",
   889	      "deadline": "5 (пяти) рабочих дней",
   890	      "amount_formula_cap": "",
   891	      "procedure_channel": "",
   892	      "liability_remedy": "",
   893	      "scope_options": [],
   894	      "consequence": "",
   895	      "applicability_filters": {
   896	        "required_type": "optional",
   897	        "only_for_product": "common",
   898	        "only_for_lot": "common",
   899	        "only_for_terminal": "common",
   900	        "payment_method": "common"
   901	      }
   902	    },
   903	    {
   904	      "id": "4.2.13",
   905	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере:\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка в пользу Банка-эмитента либо уплачены Банком Банку-эмитенту и (или) Держателям карт, эмитированных Банком, по Операциям :\n- ставшим предметом каких-либо споров и разногласий в соответствии с законодательством Российской Федерации и (или) в соответствии с правилами Платежной системы;\n- являющимся недействительными в соответствии с Договором;\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка либо уплачены Банком в связи с рассмотрением споров и разногласий между Покупателями и Предприятием касательно Операций, указанных в настоящем пункте Договора, в том числе любые сборы, комиссии, платы и (или) иные расходы Банка, связанные с рассмотрением споров и разногласий по таким Операциям;\n• убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с законодательством Российской Федерации и (или) правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору.",
   906	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере:\n• средств, которые в соответствии с правилами Платежной системы были списаны со счета Банка в",
   907	      "type": "operative",
   908	      "materiality": "evaluable",
   909	      "protected_party": "Bank",
   910	      "bound_party": "Merchant",
   911	      "right_or_obligation": "obligation",
   912	      "legal_object": "возмещение средств, списанных со счета Банка в пользу Банка-эмитента или Держателей карт",
   913	      "trigger": "",
   914	      "deadline": "",
   915	      "amount_formula_cap": "",
   916	      "procedure_channel": "EIS",
   917	      "liability_remedy": "penalty",
   918	      "scope_options": [],
   919	      "consequence": "",
   920	      "applicability_filters": {
   921	        "required_type": "mandatory",
   922	        "only_for_product": "common",
   923	        "only_for_lot": "common",
   924	        "only_for_terminal": "common",
   925	        "payment_method": "common"
   926	      }
   927	    },
   928	    {
   929	      "id": "4.2.14",
   930	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В случае реорганизации, внесения изменений и дополнений в документы, представленные Предприятием при заключении Договора, при открытии в отношении Предприятия/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса местонахождения Предприятия/ТСТ, внесенного в ЕГРЮЛ, реквизитов Предприятие/ТСТ обязуется информировать Банк и передать (по месту заключения Договора) надлежащим образом заверенные и оформленные документы, подтверждающие внесение изменений и дополнений одним из способов, указанных в п. 2.3 Договора, не позднее 3 (трех) рабочих дней с даты дополнений/изменений. ",
   931	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В случае реорганизации, внесения изменений и дополнений в документы, представленные Предприятием при заключении Договора, при открытии в отношении Предприятия/смены стадии процеду",
   932	      "type": "operative",
   933	      "materiality": "evaluable",
   934	      "protected_party": "Bank",
   935	      "bound_party": "Merchant",
   936	      "right_or_obligation": "obligation",
   937	      "legal_object": "информирование Банка о реорганизации предприятия в течение 3 рабочих дней",
   938	      "trigger": "реорганизации",
   939	      "deadline": "3 (трех) рабочих дней",
   940	      "amount_formula_cap": "",
   941	      "procedure_channel": "",
   942	      "liability_remedy": "",
   943	      "scope_options": [],
   944	      "consequence": "",
   945	      "applicability_filters": {
   946	        "required_type": "mandatory",
   947	        "only_for_product": "common",
   948	        "only_for_lot": "common",
   949	        "only_for_terminal": "common",
   950	        "payment_method": "common"
   951	      }
   952	    },
   953	    {
   954	      "id": "4.2.15",
   955	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять в Банк достоверные документы и сведения, необходимые Банку для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе, но не исключительно: не реже одного раза в год, а также по отдельному запросу Банка в течение 7 (семи) рабочих дней со дня получения запроса обновлять сведения и документы, представленные Банку при заключении настоящего Договора, включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации Предприятия, а также сведения о своих представителях, выгодоприобретателях и бенефициарных владельцах (при наличии).",
   956	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставлять в Банк достоверные документы и сведения, необходимые Банку для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе",
   957	      "type": "operative",
   958	      "materiality": "evaluable",
   959	      "protected_party": "Bank",
   960	      "bound_party": "Merchant",
   961	      "right_or_obligation": "obligation",
   962	      "legal_object": "Предприятие обязано предоставлять документы не реже одного раза в год",
   963	      "trigger": "заключении настоящего договора",
   964	      "deadline": "7 (семи) рабочих дней",
   965	      "amount_formula_cap": "",
   966	      "procedure_channel": "",
   967	      "liability_remedy": "",
   968	      "scope_options": [],
   969	      "consequence": "",
   970	      "applicability_filters": {
   971	        "required_type": "mandatory",
   972	        "only_for_product": "common",
   973	        "only_for_lot": "common",
   974	        "only_for_terminal": "common",
   975	        "payment_method": "common"
   976	      }
   977	    },
   978	    {
   979	      "id": "4.2.16.1",
   980	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) руководителя Предприятия, указанные в Заявлении/Информации о ТСТ: → Предприятие гарантирует наличие правовых оснований на передачу в Банк персональных данных руководителя Предприятия, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные в целях, указанных в п.5.1.7 Договора. Предприятие обязано уведомить Банк о прекращении правовых оснований на обработку ПДн руководителя Предприятия, указанных в настоящем пункте Договора.\n",
   981	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) руководителя Предприятия, указанные в Заявлении/Информации о ТСТ: → Предприятие гарантир",
   982	      "type": "operative",
   983	      "materiality": "evaluable",
   984	      "protected_party": "Bank",
   985	      "bound_party": "Merchant",
   986	      "right_or_obligation": "obligation",
   987	      "legal_object": "Предприятие гарантирует наличие правовых оснований на передачу ПДн",
   988	      "trigger": "",
   989	      "deadline": "",
   990	      "amount_formula_cap": "",
   991	      "procedure_channel": "",
   992	      "liability_remedy": "",
   993	      "scope_options": [],
   994	      "consequence": "",
   995	      "applicability_filters": {
   996	        "required_type": "mandatory",
   997	        "only_for_product": "common",
   998	        "only_for_lot": "common",
   999	        "only_for_terminal": "common",
  1000	        "payment_method": "common"
Tool:      1	{
     2	  "valid": true,
     3	  "errors": [],
     4	  "warnings": [],
     5	  "counts": {
     6	    "expected_matrix_ids": 169,
     7	    "clause_index_matrix_ids": 169,
     8	    "clause_index_contract_rows": 219,
     9	    "source_contract_unique_ids": 198,
    10	    "duplicate_contract_ids": 12,
    11	    "legal_proposition_matrix_rows": 169,
    12	    "legal_proposition_contract_rows": 219,
    13	    "legal_proposition_rows": 388
    14	  },
    15	  "samples": {
    16	    "missing_matrix_ids": []
    17	  }
    18	}
AI: Good. The validation is valid. Now let me understand my specific task: I need to identify **material contract-only terms** — i.e., `extra_in_contract` findings. Let me now read the contract legal propositions to find terms that have no matrix analogue. Let me also read the existing coverage ledger to understand what's already been classified.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/coverage_ledger.json', 'limit': 300}, 'id': 'call_00_Da0oUlDmoObtnJztd0S03810', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 1000, 'limit': 500}, 'id': 'call_01_cm8hdeKArtnyiAACwMwS3056', 'type': 'tool_call'}]
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "matrix_id": "2.1",
     5	      "closure": "pending",
     6	      "link_indices": [],
     7	      "reason": "Awaiting matching"
     8	    },
     9	    {
    10	      "matrix_id": "2.2",
    11	      "closure": "pending",
    12	      "link_indices": [],
    13	      "reason": "Awaiting matching"
    14	    },
    15	    {
    16	      "matrix_id": "2.3.1",
    17	      "closure": "pending",
    18	      "link_indices": [],
    19	      "reason": "Awaiting matching"
    20	    },
    21	    {
    22	      "matrix_id": "2.3.2",
    23	      "closure": "pending",
    24	      "link_indices": [],
    25	      "reason": "Awaiting matching"
    26	    },
    27	    {
    28	      "matrix_id": "2.3.3",
    29	      "closure": "pending",
    30	      "link_indices": [],
    31	      "reason": "Awaiting matching"
    32	    },
    33	    {
    34	      "matrix_id": "2.3.4",
    35	      "closure": "pending",
    36	      "link_indices": [],
    37	      "reason": "Awaiting matching"
    38	    },
    39	    {
    40	      "matrix_id": "2.3.5",
    41	      "closure": "pending",
    42	      "link_indices": [],
    43	      "reason": "Awaiting matching"
    44	    },
    45	    {
    46	      "matrix_id": "2.3.6",
    47	      "closure": "pending",
    48	      "link_indices": [],
    49	      "reason": "Awaiting matching"
    50	    },
    51	    {
    52	      "matrix_id": "2.3.7",
    53	      "closure": "pending",
    54	      "link_indices": [],
    55	      "reason": "Awaiting matching"
    56	    },
    57	    {
    58	      "matrix_id": "2.4",
    59	      "closure": "pending",
    60	      "link_indices": [],
    61	      "reason": "Awaiting matching"
    62	    },
    63	    {
    64	      "matrix_id": "2.5.1.1",
    65	      "closure": "out_of_scope",
    66	      "link_indices": [],
    67	      "reason": "Profile filter: product:internet_acquiring_not_in_profile"
    68	    },
    69	    {
    70	      "matrix_id": "2.5.2.1",
    71	      "closure": "out_of_scope",
    72	      "link_indices": [],
    73	      "reason": "Profile filter: payment_method:sber_pay_face_scan_not_in_profile"
    74	    },
    75	    {
    76	      "matrix_id": "2.6.1.1",
    77	      "closure": "pending",
    78	      "link_indices": [],
    79	      "reason": "Awaiting matching"
    80	    },
    81	    {
    82	      "matrix_id": "2.6.2.1",
    83	      "closure": "pending",
    84	      "link_indices": [],
    85	      "reason": "Awaiting matching"
    86	    },
    87	    {
    88	      "matrix_id": "2.6.2.2",
    89	      "closure": "pending",
    90	      "link_indices": [],
    91	      "reason": "Awaiting matching"
    92	    },
    93	    {
    94	      "matrix_id": "2.6.3.1",
    95	      "closure": "pending",
    96	      "link_indices": [],
    97	      "reason": "Awaiting matching"
    98	    },
    99	    {
   100	      "matrix_id": "2.6.3.2",
   101	      "closure": "pending",
   102	      "link_indices": [],
   103	      "reason": "Awaiting matching"
   104	    },
   105	    {
   106	      "matrix_id": "2.7",
   107	      "closure": "pending",
   108	      "link_indices": [],
   109	      "reason": "Awaiting matching"
   110	    },
   111	    {
   112	      "matrix_id": "3.1",
   113	      "closure": "pending",
   114	      "link_indices": [],
   115	      "reason": "Awaiting matching"
   116	    },
   117	    {
   118	      "matrix_id": "3.2",
   119	      "closure": "pending",
   120	      "link_indices": [],
   121	      "reason": "Awaiting matching"
   122	    },
   123	    {
   124	      "matrix_id": "3.3",
   125	      "closure": "pending",
   126	      "link_indices": [],
   127	      "reason": "Awaiting matching"
   128	    },
   129	    {
   130	      "matrix_id": "4.1.1",
   131	      "closure": "pending",
   132	      "link_indices": [],
   133	      "reason": "Awaiting matching"
   134	    },
   135	    {
   136	      "matrix_id": "4.1.2",
   137	      "closure": "pending",
   138	      "link_indices": [],
   139	      "reason": "Awaiting matching"
   140	    },
   141	    {
   142	      "matrix_id": "4.1.3",
   143	      "closure": "out_of_scope",
   144	      "link_indices": [],
   145	      "reason": "Profile filter: payment_method:qr_sber_pay_not_in_profile"
   146	    },
   147	    {
   148	      "matrix_id": "4.2.1",
   149	      "closure": "pending",
   150	      "link_indices": [],
   151	      "reason": "Awaiting matching"
   152	    },
   153	    {
   154	      "matrix_id": "4.2.2",
   155	      "closure": "pending",
   156	      "link_indices": [],
   157	      "reason": "Awaiting matching"
   158	    },
   159	    {
   160	      "matrix_id": "4.2.3",
   161	      "closure": "out_of_scope",
   162	      "link_indices": [],
   163	      "reason": "Profile filter: lot:fz_223_not_matched"
   164	    },
   165	    {
   166	      "matrix_id": "4.2.4",
   167	      "closure": "pending",
   168	      "link_indices": [],
   169	      "reason": "Awaiting matching"
   170	    },
   171	    {
   172	      "matrix_id": "4.2.5",
   173	      "closure": "pending",
   174	      "link_indices": [],
   175	      "reason": "Awaiting matching"
   176	    },
   177	    {
   178	      "matrix_id": "4.2.6",
   179	      "closure": "pending",
   180	      "link_indices": [],
   181	      "reason": "Awaiting matching"
   182	    },
   183	    {
   184	      "matrix_id": "4.2.7",
   185	      "closure": "pending",
   186	      "link_indices": [],
   187	      "reason": "Awaiting matching"
   188	    },
   189	    {
   190	      "matrix_id": "4.2.8",
   191	      "closure": "pending",
   192	      "link_indices": [],
   193	      "reason": "Awaiting matching"
   194	    },
   195	    {
   196	      "matrix_id": "4.2.9",
   197	      "closure": "pending",
   198	      "link_indices": [],
   199	      "reason": "Awaiting matching"
   200	    },
   201	    {
   202	      "matrix_id": "4.2.10",
   203	      "closure": "pending",
   204	      "link_indices": [],
   205	      "reason": "Awaiting matching"
   206	    },
   207	    {
   208	      "matrix_id": "4.2.11",
   209	      "closure": "pending",
   210	      "link_indices": [],
   211	      "reason": "Awaiting matching"
   212	    },
   213	    {
   214	      "matrix_id": "4.2.12",
   215	      "closure": "pending",
   216	      "link_indices": [],
   217	      "reason": "Awaiting matching"
   218	    },
   219	    {
   220	      "matrix_id": "4.2.13",
   221	      "closure": "pending",
   222	      "link_indices": [],
   223	      "reason": "Awaiting matching"
   224	    },
   225	    {
   226	      "matrix_id": "4.2.14",
   227	      "closure": "pending",
   228	      "link_indices": [],
   229	      "reason": "Awaiting matching"
   230	    },
   231	    {
   232	      "matrix_id": "4.2.15",
   233	      "closure": "pending",
   234	      "link_indices": [],
   235	      "reason": "Awaiting matching"
   236	    },
   237	    {
   238	      "matrix_id": "4.2.16.1",
   239	      "closure": "pending",
   240	      "link_indices": [],
   241	      "reason": "Awaiting matching"
   242	    },
   243	    {
   244	      "matrix_id": "4.2.16.2",
   245	      "closure": "pending",
   246	      "link_indices": [],
   247	      "reason": "Awaiting matching"
   248	    },
   249	    {
   250	      "matrix_id": "4.2.16.3",
   251	      "closure": "pending",
   252	      "link_indices": [],
   253	      "reason": "Awaiting matching"
   254	    },
   255	    {
   256	      "matrix_id": "4.2.17",
   257	      "closure": "out_of_scope",
   258	      "link_indices": [],
   259	      "reason": "Profile filter: product:internet_acquiring_not_in_profile"
   260	    },
   261	    {
   262	      "matrix_id": "4.2.18",
   263	      "closure": "pending",
   264	      "link_indices": [],
   265	      "reason": "Awaiting matching"
   266	    },
   267	    {
   268	      "matrix_id": "4.2.19",
   269	      "closure": "pending",
   270	      "link_indices": [],
   271	      "reason": "Awaiting matching"
   272	    },
   273	    {
   274	      "matrix_id": "4.2.20.1",
   275	      "closure": "pending",
   276	      "link_indices": [],
   277	      "reason": "Awaiting matching"
   278	    },
   279	    {
   280	      "matrix_id": "4.2.20.2",
   281	      "closure": "pending",
   282	      "link_indices": [],
   283	      "reason": "Awaiting matching"
   284	    },
   285	    {
   286	      "matrix_id": "4.2.20.3",
   287	      "closure": "pending",
   288	      "link_indices": [],
   289	      "reason": "Awaiting matching"
   290	    },
   291	    {
   292	      "matrix_id": "4.2.20.4",
   293	      "closure": "pending",
   294	      "link_indices": [],
   295	      "reason": "Awaiting matching"
   296	    },
   297	    {
   298	      "matrix_id": "4.2.20.5",
   299	      "closure": "pending",
   300	      "link_indices": [],
Tool:   1001	      }
  1002	    },
  1003	    {
  1004	      "id": "4.2.16.2",
  1005	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) сотрудников Предприятия: → Предприятие гарантирует наличие согласий на обработку Банком персональных данных своих работников, состав которых включает: ФИО, мобильный телефон, электронная почта, должность и место работы, а также на их дальнейшую передачу в Обслуживающие компании, действующие от лица Банка, необходимых для целей заключения и исполнения настоящего Договора. Договора. Предприятие обязуется предоставить подтверждение наличия согласий по письменному запросу Банка в соответствии с пунктом 4.2.16.3 Договора.",
  1006	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В рамках настоящего Договора Предприятие передает в Банк персональные данные (далее – ПДн) сотрудников Предприятия: → Предприятие гарантирует наличие согласий на обработку Банком ",
  1007	      "type": "operative",
  1008	      "materiality": "evaluable",
  1009	      "protected_party": "Bank",
  1010	      "bound_party": "Merchant",
  1011	      "right_or_obligation": "obligation",
  1012	      "legal_object": "Предприятие гарантирует наличие согласий сотрудников(кроме руководтитела) на обработку его персональных данных",
  1013	      "trigger": "",
  1014	      "deadline": "",
  1015	      "amount_formula_cap": "",
  1016	      "procedure_channel": "electronic",
  1017	      "liability_remedy": "",
  1018	      "scope_options": [],
  1019	      "consequence": "",
  1020	      "applicability_filters": {
  1021	        "required_type": "mandatory",
  1022	        "only_for_product": "common",
  1023	        "only_for_lot": "common",
  1024	        "only_for_terminal": "common",
  1025	        "payment_method": "common"
  1026	      }
  1027	    },
  1028	    {
  1029	      "id": "4.2.16.3",
  1030	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней с даты получения соответствующего запроса, Предприятие обязуется предоставить подтверждение правомерности передачи ПДн. В случае если Предприятие не предоставит подтверждение наличия таких оснований, оно обязуется за свой счет урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные Банку, а также возместить любые убытки и расходы, понесенные Банком в результате не предоставления таких доказательств.",
  1031	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней с даты получения соответствующего запроса, Предприятие обязуется предоставить подтверждение правом",
  1032	      "type": "operative",
  1033	      "materiality": "evaluable",
  1034	      "protected_party": "Bank",
  1035	      "bound_party": "Merchant",
  1036	      "right_or_obligation": "obligation",
  1037	      "legal_object": "Предприятие обязано предоставлять подтверждение согласий на обработку персональных данных сотрудников (включая руководителя) по письменному запросу банка",
  1038	      "trigger": "если предприятие не предоставит подтверждение наличия таких оснований",
  1039	      "deadline": "3 (трех) рабочих дней",
  1040	      "amount_formula_cap": "",
  1041	      "procedure_channel": "",
  1042	      "liability_remedy": "indemnification",
  1043	      "scope_options": [],
  1044	      "consequence": "",
  1045	      "applicability_filters": {
  1046	        "required_type": "mandatory",
  1047	        "only_for_product": "common",
  1048	        "only_for_lot": "common",
  1049	        "only_for_terminal": "common",
  1050	        "payment_method": "common"
  1051	      }
  1052	    },
  1053	    {
  1054	      "id": "4.2.17",
  1055	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Обеспечить соблюдение требований Стандарта PCI DSS, размещенного на сайте в сети интернет: https://www.pcisecuritystandards.org и предоставлять по запросу Банка результаты проведения оценки соответствия в виде аттестата соответствия или листа самооценки на электронный адрес: pcidss@sberbank.ru. ",
  1056	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Обеспечить соблюдение требований Стандарта PCI DSS, размещенного на сайте в сети интернет: https://www.pcisecuritystandards.org и предоставлять по запросу Банка результаты проведе",
  1057	      "type": "operative",
  1058	      "materiality": "evaluable",
  1059	      "protected_party": "Bank",
  1060	      "bound_party": "Merchant",
  1061	      "right_or_obligation": "obligation",
  1062	      "legal_object": "Обязательство соблюдать требования PCI DSS",
  1063	      "trigger": "",
  1064	      "deadline": "",
  1065	      "amount_formula_cap": "",
  1066	      "procedure_channel": "electronic",
  1067	      "liability_remedy": "",
  1068	      "scope_options": [],
  1069	      "consequence": "",
  1070	      "applicability_filters": {
  1071	        "required_type": "mandatory",
  1072	        "only_for_product": "internet_acquiring",
  1073	        "only_for_lot": "common",
  1074	        "only_for_terminal": "common",
  1075	        "payment_method": "common"
  1076	      }
  1077	    },
  1078	    {
  1079	      "id": "4.2.18",
  1080	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы, извещающие об обслуживании Карт. ",
  1081	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы, извещающие об обслуживании Карт. ",
  1082	      "type": "operative",
  1083	      "materiality": "evaluable",
  1084	      "protected_party": "Bank",
  1085	      "bound_party": "Merchant",
  1086	      "right_or_obligation": "obligation",
  1087	      "legal_object": "При расторжении договора прекращение приема карт к оплате (регулируется дата прекращения)",
  1088	      "trigger": "",
  1089	      "deadline": "",
  1090	      "amount_formula_cap": "",
  1091	      "procedure_channel": "",
  1092	      "liability_remedy": "",
  1093	      "scope_options": [],
  1094	      "consequence": "",
  1095	      "applicability_filters": {
  1096	        "required_type": "mandatory",
  1097	        "only_for_product": "common",
  1098	        "only_for_lot": "common",
  1099	        "only_for_terminal": "common",
  1100	        "payment_method": "common"
  1101	      }
  1102	    },
  1103	    {
  1104	      "id": "4.2.19",
  1105	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не принимать мер противодействия Банку в проведении проверки Предприятия/ТСТ / Ресурса  на предмет выявления мошеннических Операций и/или предоставления Покупателям Товаров/услуг, не соответствующих роду деятельности Предприятия/ТСТ, а также оказывать содействие Банку в проведении разбирательства по факту совершения подозрительных Операций.",
  1106	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не принимать мер противодействия Банку в проведении проверки Предприятия/ТСТ / Ресурса  на предмет выявления мошеннических Операций и/или предоставления Покупателям Товаров/услуг,",
  1107	      "type": "operative",
  1108	      "materiality": "evaluable",
  1109	      "protected_party": "Bank",
  1110	      "bound_party": "Merchant",
  1111	      "right_or_obligation": "obligation",
  1112	      "legal_object": "Предприятие обязано не препятствовать проверке со стороны Банка",
  1113	      "trigger": "",
  1114	      "deadline": "",
  1115	      "amount_formula_cap": "",
  1116	      "procedure_channel": "",
  1117	      "liability_remedy": "",
  1118	      "scope_options": [],
  1119	      "consequence": "",
  1120	      "applicability_filters": {
  1121	        "required_type": "mandatory",
  1122	        "only_for_product": "common",
  1123	        "only_for_lot": "common",
  1124	        "only_for_terminal": "common",
  1125	        "payment_method": "common"
  1126	      }
  1127	    },
  1128	    {
  1129	      "id": "4.2.20.1",
  1130	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: https://www.sberbank.ru/help/business/acquiring.",
  1131	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке",
  1132	      "type": "operative",
  1133	      "materiality": "evaluable",
  1134	      "protected_party": "Bank",
  1135	      "bound_party": "Merchant",
  1136	      "right_or_obligation": "obligation",
  1137	      "legal_object": "обязательство предприятия проводить инструктаж сотрудников самостоятельно",
  1138	      "trigger": "",
  1139	      "deadline": "",
  1140	      "amount_formula_cap": "",
  1141	      "procedure_channel": "",
  1142	      "liability_remedy": "",
  1143	      "scope_options": [],
  1144	      "consequence": "",
  1145	      "applicability_filters": {
  1146	        "required_type": "mandatory",
  1147	        "only_for_product": "trade_acquiring",
  1148	        "only_for_lot": "common",
  1149	        "only_for_terminal": "common",
  1150	        "payment_method": "common"
  1151	      }
  1152	    },
  1153	    {
  1154	      "id": "4.2.20.2",
  1155	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Использовать Электронные терминалы (в том числе технологические sim-карты)/Смарт-терминалы и программное обеспечение, предоставленное Банком, только для целей реализации настоящего Договора и на территории регистрации ТСТ/фактической установки Электронного терминала/Смарт-терминала. Не вносить изменения в программное обеспечение и Электронные терминалы/Смарт-терминалы, предоставленные Банком. Не осуществлять самостоятельно ремонт Электронных терминалов/Смарт-терминалов Банка. Не передавать третьим лицам Электронные терминалы/Смарт-терминалы Банка, Документы по операциям и инструктивные материалы, предоставленные Банком, за исключением работников Обслуживающей компании.",
  1156	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Использовать Электронные терминалы (в том числе технологические sim-карты)/Смарт-терминалы и программное об",
  1157	      "type": "operative",
  1158	      "materiality": "evaluable",
  1159	      "protected_party": "Bank",
  1160	      "bound_party": "Merchant",
  1161	      "right_or_obligation": "obligation",
  1162	      "legal_object": "использование Электронных терминалов и программного обеспечения только для целей договора и на территории регистрации ТСТ/установки устройства",
  1163	      "trigger": "",
  1164	      "deadline": "",
  1165	      "amount_formula_cap": "",
  1166	      "procedure_channel": "electronic",
  1167	      "liability_remedy": "",
  1168	      "scope_options": [],
  1169	      "consequence": "",
  1170	      "applicability_filters": {
  1171	        "required_type": "mandatory",
  1172	        "only_for_product": "trade_acquiring",
  1173	        "only_for_lot": "common",
  1174	        "only_for_terminal": "common",
  1175	        "payment_method": "common"
  1176	      }
  1177	    },
  1178	    {
  1179	      "id": "4.2.20.3",
  1180	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов/Смарт-терминалов для проведения работ по их подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке.",
  1181	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных термин",
  1182	      "type": "operative",
  1183	      "materiality": "evaluable",
  1184	      "protected_party": "Bank",
  1185	      "bound_party": "Merchant",
  1186	      "right_or_obligation": "obligation",
  1187	      "legal_object": "Предоставление доступа третьим лицам к местам установки терминалов",
  1188	      "trigger": "",
  1189	      "deadline": "",
  1190	      "amount_formula_cap": "",
  1191	      "procedure_channel": "electronic",
  1192	      "liability_remedy": "",
  1193	      "scope_options": [],
  1194	      "consequence": "",
  1195	      "applicability_filters": {
  1196	        "required_type": "mandatory",
  1197	        "only_for_product": "trade_acquiring",
  1198	        "only_for_lot": "common",
  1199	        "only_for_terminal": "common",
  1200	        "payment_method": "common"
  1201	      }
  1202	    },
  1203	    {
  1204	      "id": "4.2.20.4",
  1205	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Принять Электронные терминалы/Смарт-терминалы Банка и/или программное обеспечение для Смарт-терминалов Предприятия по акту принятия оказанных услуг по форме Обслуживающей компании, составленному в 2-х (два) экземплярах, подписанных уполномоченными работниками Обслуживающей компании и Предприятия. Один экземпляр акта находится на хранении в Обслуживающей компании, второй – у Предприятия. Форма акта размещена на Официальном сайте Банка.",
  1206	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Принять Электронные терминалы/Смарт-терминалы Банка и/или программное обеспечение для Смарт-терминалов Пред",
  1207	      "type": "operative",
  1208	      "materiality": "evaluable",
  1209	      "protected_party": "Bank",
  1210	      "bound_party": "Merchant",
  1211	      "right_or_obligation": "obligation",
  1212	      "legal_object": "Предприятие обязано принять Электронные терминалы / Смарт-терминалв по акту",
  1213	      "trigger": "",
  1214	      "deadline": "",
  1215	      "amount_formula_cap": "",
  1216	      "procedure_channel": "electronic",
  1217	      "liability_remedy": "",
  1218	      "scope_options": [],
  1219	      "consequence": "",
  1220	      "applicability_filters": {
  1221	        "required_type": "mandatory",
  1222	        "only_for_product": "trade_acquiring",
  1223	        "only_for_lot": "common",
  1224	        "only_for_terminal": "common",
  1225	        "payment_method": "common"
  1226	      }
  1227	    },
  1228	    {
  1229	      "id": "4.2.20.5",
  1230	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае выхода Электронного терминала/Смарт-терминала, в том числе Мобильного устройства Предприятия, из строя или его утраты немедленно информировать об этом Банк в соответствии с п. 2.3.1, п. 2.3.2 Договора или путем обращения в службу поддержки Банка по телефону, указанному в п. 2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.\n",
  1231	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае выхода Электронного терминала/Смарт-терминала, в том числе Мобильного устройства Предприятия, из с",
  1232	      "type": "operative",
  1233	      "materiality": "evaluable",
  1234	      "protected_party": "Bank",
  1235	      "bound_party": "Merchant",
  1236	      "right_or_obligation": "obligation",
  1237	      "legal_object": "Предприятие обязано немедленно информировать Банк о выходе из строя или утрате Электронного терминала/Смарт-терминала или Мобильного устройства",
  1238	      "trigger": "выхода электронного терминала/смарт-терминала",
  1239	      "deadline": "",
  1240	      "amount_formula_cap": "",
  1241	      "procedure_channel": "electronic",
  1242	      "liability_remedy": "",
  1243	      "scope_options": [],
  1244	      "consequence": "",
  1245	      "applicability_filters": {
  1246	        "required_type": "mandatory",
  1247	        "only_for_product": "trade_acquiring",
  1248	        "only_for_lot": "common",
  1249	        "only_for_terminal": "common",
  1250	        "payment_method": "common"
  1251	      }
  1252	    },
  1253	    {
  1254	      "id": "4.2.20.6",
  1255	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Вернуть Банку или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Договора или с даты получения письменного/устного требования Банка о возврате Электронных терминалов/Смарт-терминалов Банка.",
  1256	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → Вернуть Банку или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) раб",
  1257	      "type": "operative",
  1258	      "materiality": "evaluable",
  1259	      "protected_party": "Bank",
  1260	      "bound_party": "Merchant",
  1261	      "right_or_obligation": "obligation",
  1262	      "legal_object": "вернуть терминал в течение 5 рабочих дней после расторжения договора",
  1263	      "trigger": "",
  1264	      "deadline": "5 (пяти) рабочих дней",
  1265	      "amount_formula_cap": "",
  1266	      "procedure_channel": "electronic",
  1267	      "liability_remedy": "",
  1268	      "scope_options": [],
  1269	      "consequence": "",
  1270	      "applicability_filters": {
  1271	        "required_type": "mandatory",
  1272	        "only_for_product": "trade_acquiring",
  1273	        "only_for_lot": "common",
  1274	        "only_for_terminal": "common",
  1275	        "payment_method": "common"
  1276	      }
  1277	    },
  1278	    {
  1279	      "id": "4.2.20.7",
  1280	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае невозврата Электронных терминалов /Смарт-терминалов Банка в соответствии с п. 4.2.20.6 Договора, уплатить Банку штраф в размере 25 000 (двадцать пять тысяч) рублей, в том числе НДС, за каждый Электронный терминал и 25 000 (двадцать пять тысяч) рублей, в том числе НДС за каждый Смарт-терминал Банка.",
  1281	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Предприятии/в ТСТ (Торговый эквайринг): → В случае невозврата Электронных терминалов /Смарт-терминалов Банка в соответствии с п. 4.2.20.6 Договора, у",
  1282	      "type": "operative",
  1283	      "materiality": "evaluable",
  1284	      "protected_party": "Bank",
  1285	      "bound_party": "Merchant",
  1286	      "right_or_obligation": "obligation",
  1287	      "legal_object": "Невозврат терминалов. Обязанность предприятия об уплате штрафа за невозврат",
  1288	      "trigger": "невозврата электронных терминалов /смарт-терминалов банка в соответствии с п",
  1289	      "deadline": "",
  1290	      "amount_formula_cap": "25 000 (двадцать пять тысяч) рублей",
  1291	      "procedure_channel": "electronic",
  1292	      "liability_remedy": "penalty",
  1293	      "scope_options": [],
  1294	      "consequence": "",
  1295	      "applicability_filters": {
  1296	        "required_type": "mandatory",
  1297	        "only_for_product": "trade_acquiring",
  1298	        "only_for_lot": "common",
  1299	        "only_for_terminal": "common",
  1300	        "payment_method": "common"
  1301	      }
  1302	    },
  1303	    {
  1304	      "id": "4.2.21.1",
  1305	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Приступить к проведению Операций на Ресурсе только после успешного завершения проверки выбранных Предприятием/ТСТ Операций на тестовой среде.",
  1306	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Приступить к проведению Операций на Ресурсе только после ",
  1307	      "type": "operative",
  1308	      "materiality": "evaluable",
  1309	      "protected_party": "Bank",
  1310	      "bound_party": "Merchant",
  1311	      "right_or_obligation": "obligation",
  1312	      "legal_object": "Приступить к проведению операций на ресурсе только после успешного завершения проверки операций на тестовой среде",
  1313	      "trigger": "",
  1314	      "deadline": "",
  1315	      "amount_formula_cap": "",
  1316	      "procedure_channel": "",
  1317	      "liability_remedy": "",
  1318	      "scope_options": [],
  1319	      "consequence": "",
  1320	      "applicability_filters": {
  1321	        "required_type": "mandatory",
  1322	        "only_for_product": "internet_acquiring",
  1323	        "only_for_lot": "common",
  1324	        "only_for_terminal": "common",
  1325	        "payment_method": "common"
  1326	      }
  1327	    },
  1328	    {
  1329	      "id": "4.2.21.2",
  1330	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соответствовать Требованиям Банка к Ресурсу Предприятия, размещенным на Официальном сайте Банка.",
  1331	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соответствовать Требованиям Банка к Ресурсу Предприятия, ",
  1332	      "type": "operative",
  1333	      "materiality": "evaluable",
  1334	      "protected_party": "Bank",
  1335	      "bound_party": "Merchant",
  1336	      "right_or_obligation": "obligation",
  1337	      "legal_object": "Предприятие обязано соответствовать Требованиям Банка к Ресурсу, размещенным на Официальном сайте Банка",
  1338	      "trigger": "",
  1339	      "deadline": "",
  1340	      "amount_formula_cap": "",
  1341	      "procedure_channel": "",
  1342	      "liability_remedy": "",
  1343	      "scope_options": [],
  1344	      "consequence": "",
  1345	      "applicability_filters": {
  1346	        "required_type": "mandatory",
  1347	        "only_for_product": "internet_acquiring",
  1348	        "only_for_lot": "common",
  1349	        "only_for_terminal": "common",
  1350	        "payment_method": "common"
  1351	      }
  1352	    },
  1353	    {
  1354	      "id": "4.2.21.3",
  1355	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Подтверждать авторизованные с использованием Предавторизации суммы к списанию через СПЭП не позднее 5 (пяти) календарных дней с даты совершения Операции на сумму фактически оказанных Товаров/услуг, в соответствии с Порядком проведения операций в Торгово-сервисных точках/на Ресурсе.",
  1356	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Подтверждать авторизованные с использованием Предавториза",
  1357	      "type": "operative",
  1358	      "materiality": "evaluable",
  1359	      "protected_party": "Bank",
  1360	      "bound_party": "Merchant",
  1361	      "right_or_obligation": "obligation",
  1362	      "legal_object": "Подтверждение сумм к списанию не позднее 5 календарных дней",
  1363	      "trigger": "",
  1364	      "deadline": "5 (пяти) календарных дней",
  1365	      "amount_formula_cap": "",
  1366	      "procedure_channel": "",
  1367	      "liability_remedy": "",
  1368	      "scope_options": [],
  1369	      "consequence": "",
  1370	      "applicability_filters": {
  1371	        "required_type": "mandatory",
  1372	        "only_for_product": "internet_acquiring",
  1373	        "only_for_lot": "common",
  1374	        "only_for_terminal": "common",
  1375	        "payment_method": "common"
  1376	      }
  1377	    },
  1378	    {
  1379	      "id": "4.2.21.4",
  1380	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Согласовывать с Банком дизайн Платежной страницы, включая электронные варианты информационных наклеек.\n",
  1381	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Согласовывать с Банком дизайн Платежной страницы, включая",
  1382	      "type": "operative",
  1383	      "materiality": "evaluable",
  1384	      "protected_party": "Bank",
  1385	      "bound_party": "Merchant",
  1386	      "right_or_obligation": "obligation",
  1387	      "legal_object": "Согласование дизайна Платежной страницы с Банком",
  1388	      "trigger": "",
  1389	      "deadline": "",
  1390	      "amount_formula_cap": "",
  1391	      "procedure_channel": "electronic",
  1392	      "liability_remedy": "",
  1393	      "scope_options": [],
  1394	      "consequence": "",
  1395	      "applicability_filters": {
  1396	        "required_type": "mandatory",
  1397	        "only_for_product": "internet_acquiring",
  1398	        "only_for_lot": "common",
  1399	        "only_for_terminal": "common",
  1400	        "payment_method": "common"
  1401	      }
  1402	    },
  1403	    {
  1404	      "id": "4.2.21.5",
  1405	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Провести мероприятия по интеграции Ресурса со СПЭП и соответствующие интеграционные тесты в течение 30 (тридцати) календарных дней с даты заключения Договора.",
  1406	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Провести мероприятия по интеграции Ресурса со СПЭП и соот",
  1407	      "type": "operative",
  1408	      "materiality": "evaluable",
  1409	      "protected_party": "Bank",
  1410	      "bound_party": "Merchant",
  1411	      "right_or_obligation": "obligation",
  1412	      "legal_object": "Предприятие проводит интеграцию Ресурса со СПЭП в течение 30 календарных дней с даты заключения Договора",
  1413	      "trigger": "",
  1414	      "deadline": "30 (тридцати) календарных дней",
  1415	      "amount_formula_cap": "",
  1416	      "procedure_channel": "",
  1417	      "liability_remedy": "",
  1418	      "scope_options": [],
  1419	      "consequence": "",
  1420	      "applicability_filters": {
  1421	        "required_type": "mandatory",
  1422	        "only_for_product": "internet_acquiring",
  1423	        "only_for_lot": "common",
  1424	        "only_for_terminal": "common",
  1425	        "payment_method": "common"
  1426	      }
  1427	    },
  1428	    {
  1429	      "id": "4.2.21.6",
  1430	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Самостоятельно обеспечивать безопасность своих информационных ресурсов в сети интернет.",
  1431	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Самостоятельно обеспечивать безопасность своих информацио",
  1432	      "type": "operative",
  1433	      "materiality": "evaluable",
  1434	      "protected_party": "Bank",
  1435	      "bound_party": "Merchant",
  1436	      "right_or_obligation": "obligation",
  1437	      "legal_object": "Самостоятельное обеспечение безопасности информационных ресурсов в сети интернет",
  1438	      "trigger": "",
  1439	      "deadline": "",
  1440	      "amount_formula_cap": "",
  1441	      "procedure_channel": "",
  1442	      "liability_remedy": "",
  1443	      "scope_options": [],
  1444	      "consequence": "",
  1445	      "applicability_filters": {
  1446	        "required_type": "mandatory",
  1447	        "only_for_product": "internet_acquiring",
  1448	        "only_for_lot": "common",
  1449	        "only_for_terminal": "common",
  1450	        "payment_method": "common"
  1451	      }
  1452	    },
  1453	    {
  1454	      "id": "4.2.21.7",
  1455	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Предоставлять по требованию Банка доступ к разделам Ресурса с ограниченным доступом, не связанным с администрированием и сопровождением (VIP, Оптовое, Клубное обслуживание, и т.п.).",
  1456	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Предоставлять по требованию Банка доступ к разделам Ресур",
  1457	      "type": "operative",
  1458	      "materiality": "evaluable",
  1459	      "protected_party": "Bank",
  1460	      "bound_party": "Merchant",
  1461	      "right_or_obligation": "obligation",
  1462	      "legal_object": "Предоставление доступа к разделам Ресурса с ограниченным доступом по требованию Банка",
  1463	      "trigger": "",
  1464	      "deadline": "",
  1465	      "amount_formula_cap": "",
  1466	      "procedure_channel": "",
  1467	      "liability_remedy": "",
  1468	      "scope_options": [],
  1469	      "consequence": "",
  1470	      "applicability_filters": {
  1471	        "required_type": "mandatory",
  1472	        "only_for_product": "internet_acquiring",
  1473	        "only_for_lot": "common",
  1474	        "only_for_terminal": "common",
  1475	        "payment_method": "common"
  1476	      }
  1477	    },
  1478	    {
  1479	      "id": "4.2.21.8",
  1480	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соблюдать правила пользования Личным кабинетом Интернет-эквайринга, размещенным на Официальном сайте Банка.",
  1481	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При осуществлении Операций на Ресурсе (Интернет-эквайринг): проверка на этапе согласования контракта со стороны БР ГОСБ → Соблюдать правила пользования Личным кабинетом Интернет-э",
  1482	      "type": "operative",
  1483	      "materiality": "evaluable",
  1484	      "protected_party": "Bank",
  1485	      "bound_party": "Merchant",
  1486	      "right_or_obligation": "obligation",
  1487	      "legal_object": "Соблюдение правил пользования Личным кабинетом Интернет-эквайринга",
  1488	      "trigger": "",
  1489	      "deadline": "",
  1490	      "amount_formula_cap": "",
  1491	      "procedure_channel": "",
  1492	      "liability_remedy": "",
  1493	      "scope_options": [],
  1494	      "consequence": "",
  1495	      "applicability_filters": {
  1496	        "required_type": "mandatory",
  1497	        "only_for_product": "internet_acquiring",
  1498	        "only_for_lot": "common",
  1499	        "only_for_terminal": "common",
  1500	        "payment_method": "common"
AI: Now I have a good understanding of the landscape. Let me now focus on my specific task: identifying **contract-only terms** (`extra_in_contract`). I need to read the contract legal propositions (the `contract` array in `legal_propositions.json`) and identify which contract clauses have no matrix analogue and are materially significant.

Let me read the contract portion of the legal propositions:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 1500, 'limit': 500}, 'id': 'call_00_hnjO47xX3cMOwzxx6p0r0966', 'type': 'tool_call'}]
Tool:   1501	      }
  1502	    },
  1503	    {
  1504	      "id": "4.2.22",
  1505	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставить Покупателю для считывания QR-код с целью осуществления оплаты Товаров/услуг с использованием SberPayQR/Плати QR",
  1506	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Предоставить Покупателю для считывания QR-код с целью осуществления оплаты Товаров/услуг с использованием SberPayQR/Плати QR",
  1507	      "type": "operative",
  1508	      "materiality": "evaluable",
  1509	      "protected_party": "Bank",
  1510	      "bound_party": "Merchant",
  1511	      "right_or_obligation": "obligation",
  1512	      "legal_object": "Предприятие обязуется предоставлять QR-код для использования SberPayQR/Плати QR (должна быть прямая отсылка к QR-коду)",
  1513	      "trigger": "",
  1514	      "deadline": "",
  1515	      "amount_formula_cap": "",
  1516	      "procedure_channel": "",
  1517	      "liability_remedy": "",
  1518	      "scope_options": [],
  1519	      "consequence": "",
  1520	      "applicability_filters": {
  1521	        "required_type": "optional",
  1522	        "only_for_product": "trade_acquiring",
  1523	        "only_for_lot": "common",
  1524	        "only_for_terminal": "common",
  1525	        "payment_method": "qr"
  1526	      }
  1527	    },
  1528	    {
  1529	      "id": "4.2.23",
  1530	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не изменять QR-код партнера в одностороннем порядке.",
  1531	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Не изменять QR-код партнера в одностороннем порядке.",
  1532	      "type": "operative",
  1533	      "materiality": "evaluable",
  1534	      "protected_party": "Bank",
  1535	      "bound_party": "Merchant",
  1536	      "right_or_obligation": "obligation",
  1537	      "legal_object": "Предприятие обязуется не изменять QR-код партнера в одностороннем порядке (должна быть прямая отсылка к QR-коду)",
  1538	      "trigger": "",
  1539	      "deadline": "",
  1540	      "amount_formula_cap": "",
  1541	      "procedure_channel": "",
  1542	      "liability_remedy": "",
  1543	      "scope_options": [],
  1544	      "consequence": "",
  1545	      "applicability_filters": {
  1546	        "required_type": "optional",
  1547	        "only_for_product": "trade_acquiring",
  1548	        "only_for_lot": "common",
  1549	        "only_for_terminal": "common",
  1550	        "payment_method": "qr"
  1551	      }
  1552	    },
  1553	    {
  1554	      "id": "4.2.24",
  1555	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Использовать API и сведения, передаваемые посредством QR-API, в границах прав и функциональных возможностей такого API и его описания, изложенного в Порядке, условиях и ответственности сторон при подключении QR-API, размещенном на Официальном сайте Банка.",
  1556	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Использовать API и сведения, передаваемые посредством QR-API, в границах прав и функциональных возможностей такого API и его описания, изложенного в Порядке, условиях и ответствен",
  1557	      "type": "operative",
  1558	      "materiality": "evaluable",
  1559	      "protected_party": "Bank",
  1560	      "bound_party": "Merchant",
  1561	      "right_or_obligation": "obligation",
  1562	      "legal_object": "использование API в рамках функциональных возможностей (должна быть прямая отсылка к QR-API)",
  1563	      "trigger": "подключении qr-api",
  1564	      "deadline": "",
  1565	      "amount_formula_cap": "",
  1566	      "procedure_channel": "",
  1567	      "liability_remedy": "",
  1568	      "scope_options": [],
  1569	      "consequence": "",
  1570	      "applicability_filters": {
  1571	        "required_type": "optional",
  1572	        "only_for_product": "common",
  1573	        "only_for_lot": "common",
  1574	        "only_for_terminal": "common",
  1575	        "payment_method": "qr"
  1576	      }
  1577	    },
  1578	    {
  1579	      "id": "4.2.25",
  1580	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При выявлении фактов или признаков нарушения безопасности использования QR-API и функциональных возможностей организации информационно-технологического взаимодействия немедленно приостановить использование API и оповестить об этом Банк любым из способов, указанных в п.2.3.1. – п.2.3.4. Договора.",
  1581	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → При выявлении фактов или признаков нарушения безопасности использования QR-API и функциональных возможностей организации информационно-технологического взаимодействия немедленно п",
  1582	      "type": "operative",
  1583	      "materiality": "evaluable",
  1584	      "protected_party": "Bank",
  1585	      "bound_party": "Merchant",
  1586	      "right_or_obligation": "obligation",
  1587	      "legal_object": "При выявлении нарушения безопасности использования QR-API - приостановить использование API (должна быть прямая отсылка к QR-API)",
  1588	      "trigger": "",
  1589	      "deadline": "",
  1590	      "amount_formula_cap": "",
  1591	      "procedure_channel": "",
  1592	      "liability_remedy": "",
  1593	      "scope_options": [],
  1594	      "consequence": "suspension_right",
  1595	      "applicability_filters": {
  1596	        "required_type": "optional",
  1597	        "only_for_product": "common",
  1598	        "only_for_lot": "common",
  1599	        "only_for_terminal": "common",
  1600	        "payment_method": "qr"
  1601	      }
  1602	    },
  1603	    {
  1604	      "id": "4.2.26",
  1605	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В дополнение к соблюдению требований, указанных в Условиях, в том числе приложениях к Условиям, в целях осуществлении Повторяющихся платежей Предприятие обязано:\n• размещать на Ресурсе пользовательское соглашение/оферту Предприятия, содержащее условия проведения Повторяющихся платежей (в случае их применения), а также хранить письменное соглашение с Держателем (согласие/ поручение Держателя) об условиях проведения Повторяющихся платежей;\n• получать от Держателя согласие на совершение Повторяющихся платежей, в том числе с суммой Повторяющихся платежей, периодом времени, в течение которого совершаются Повторяющиеся платежи, регулярностью совершения Повторяющихся платежей, порядком прекращения неосуществленных Повторяющихся платежей;\n• обеспечить Покупателю возможность отмены неосуществленных Повторяющихся платежей в порядке, определенном договором, заключенным с Покупателем;\n• прекратить осуществление Повторяющихся платежей в порядке, установленном договором с Покупателем, в случае получения от такого Покупателя уведомления об отказе от осуществления Повторяющихся платежей и (или) прекращения действия договора, заключенного между Покупателем и Предприятием.",
  1606	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В дополнение к соблюдению требований, указанных в Условиях, в том числе приложениях к Условиям, в целях осуществлении Повторяющихся платежей Предприятие обязано:\n• размещать на Ре",
  1607	      "type": "operative",
  1608	      "materiality": "evaluable",
  1609	      "protected_party": "Bank",
  1610	      "bound_party": "Merchant",
  1611	      "right_or_obligation": "obligation",
  1612	      "legal_object": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В дополнение к соблюдению требований, указанных в Условиях, в том числе приложениях к Условиям, в целях осуществлении Повторяющихся платеже",
  1613	      "trigger": "их применения)",
  1614	      "deadline": "",
  1615	      "amount_formula_cap": "",
  1616	      "procedure_channel": "",
  1617	      "liability_remedy": "",
  1618	      "scope_options": [],
  1619	      "consequence": "refusal_right",
  1620	      "applicability_filters": {
  1621	        "required_type": "mandatory",
  1622	        "only_for_product": "internet_acquiring",
  1623	        "only_for_lot": "common",
  1624	        "only_for_terminal": "common",
  1625	        "payment_method": "common"
  1626	      }
  1627	    },
  1628	    {
  1629	      "id": "5.1.1.1",
  1630	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, являющихся недействительными, в следующих случаях:\n1) Операция совершена с нарушением Договора, требований законодательства РФ и/или правил Платежной системы и инструктивных материалов Банка;\n2) Операция совершена по поддельной или недействительной Карте;\n3) Документ по операции заполнен не полностью, имеются исправления или отсутствует возможность определить сумму Операции, код Авторизации;\n4) экземпляр Документа по операции, переданный в Банк, не соответствует экземпляру Документа по операции, переданному Покупателю;\n5)  подпись Покупателя на Чеке электронного терминала отсутствует, при этом на Чеке электронного терминала присутствует поле «Подпись Клиента»;\n6) по требованию Банка в течение 3 (трех) рабочих дней со дня получения запроса не предоставлены или предоставлены не в полном объеме (или не соответствующие правилам Платежной системы) или в ненадлежащем качестве подтверждающие Документы по операции/объяснения обстоятельств Операции;\n7) оплаченные с использованием Карты /ее реквизитов / NFС-карты / SberPay / Плати QR / Платежного счета  Товары/услуги были возвращены Предприятию, или не доставлены Покупателю/услуги отменены/не оказаны, но возврат денежных средств Покупателю произведен не был (за исключением случаев, когда Товары/услуги не были приняты/возврат Товара/отказ от услуг не предусмотрен законодательством РФ или правилами работы Предприятия и Покупатель был об этом проинформирован до совершения сделки);\n8) Товар/услуга уже был оплачен Покупателем ранее (о чем имеется документальное подтверждение);\n9) на совершенную Операцию Банком не был получен код Авторизации согласно Порядка проведения операций в Торгово-сервисных точках/на Ресурсе. Код Авторизации считается полученным Банком в том случае, если он содержится в электронных реестрах кодов Авторизации Банка и относится к указанной Операции. Код Авторизации указывается на Чеке Электронного терминала, который передается в ККТ Предприятия от Электронного терминала ;\n10) сумма Товара/услуги была разбита на несколько Операций;\n11) от Банка-эмитента получена информация о мошенническом характере Операции;\n12)  Операция была проведена без считывания Карты в Электронном терминале (реквизиты Карты были введены в Электронный терминал вручную), за исключением случаев, когда данные действия согласованы  с Банком.\n",
  1631	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, являющихся недействительными, в следующих случаях:\n1) Операция совершена с нарушением ",
  1632	      "type": "operative",
  1633	      "materiality": "evaluable",
  1634	      "protected_party": "Bank",
  1635	      "bound_party": "Merchant",
  1636	      "right_or_obligation": "right",
  1637	      "legal_object": "Банк имеет право удерживать суммы операций, являющиеся недействительными",
  1638	      "trigger": "этом на чеке электронного терминала присутствует поле «подпись клиента»",
  1639	      "deadline": "3 (трех) рабочих дней",
  1640	      "amount_formula_cap": "",
  1641	      "procedure_channel": "electronic",
  1642	      "liability_remedy": "",
  1643	      "scope_options": [],
  1644	      "consequence": "refusal_right",
  1645	      "applicability_filters": {
  1646	        "required_type": "mandatory",
  1647	        "only_for_product": "common",
  1648	        "only_for_lot": "common",
  1649	        "only_for_terminal": "common",
  1650	        "payment_method": "common"
  1651	      }
  1652	    },
  1653	    {
  1654	      "id": "5.1.1.2",
  1655	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы, ошибочно перечисленные на счет Предприятия.",
  1656	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы, ошибочно перечисленные на счет Предприятия.",
  1657	      "type": "operative",
  1658	      "materiality": "evaluable",
  1659	      "protected_party": "Bank",
  1660	      "bound_party": "Merchant",
  1661	      "right_or_obligation": "right",
  1662	      "legal_object": "Банк имеет право удерживать ошибочно перечисленные суммы с счета Предприятия",
  1663	      "trigger": "",
  1664	      "deadline": "",
  1665	      "amount_formula_cap": "",
  1666	      "procedure_channel": "",
  1667	      "liability_remedy": "",
  1668	      "scope_options": [],
  1669	      "consequence": "withholding_right",
  1670	      "applicability_filters": {
  1671	        "required_type": "mandatory",
  1672	        "only_for_product": "common",
  1673	        "only_for_lot": "common",
  1674	        "only_for_terminal": "common",
  1675	        "payment_method": "common"
  1676	      }
  1677	    },
  1678	    {
  1679	      "id": "5.1.1.3",
  1680	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.",
  1681	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.",
  1682	      "type": "operative",
  1683	      "materiality": "evaluable",
  1684	      "protected_party": "Bank",
  1685	      "bound_party": "Merchant",
  1686	      "right_or_obligation": "right",
  1687	      "legal_object": "Банк имеет право удерживать суммы операций возврата, возврата платежа, реверсивные транзакции. Важно не рассматривать пункты в которых не указана хотя бы одна из этих сумм",
  1688	      "trigger": "",
  1689	      "deadline": "",
  1690	      "amount_formula_cap": "",
  1691	      "procedure_channel": "",
  1692	      "liability_remedy": "",
  1693	      "scope_options": [],
  1694	      "consequence": "withholding_right",
  1695	      "applicability_filters": {
  1696	        "required_type": "mandatory",
  1697	        "only_for_product": "common",
  1698	        "only_for_lot": "common",
  1699	        "only_for_terminal": "common",
  1700	        "payment_method": "common"
  1701	      }
  1702	    },
  1703	    {
  1704	      "id": "5.1.1.4",
  1705	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, которые были оспорены и/или списаны со счета Банка Банком – эмитентом в соответствии с правилами Платежной системы по Операциям, проведенным в ТСТ, суммы оспоренных Операций, проведенных с использованием SberPay/Плати QR, а также суммы оспоренных Операций в отношении Товаров/услуг, реализуемых Предприятием как агентом.",
  1706	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, которые были оспорены и/или списаны со счета Банка Банком – эмитентом в соответствии с",
  1707	      "type": "operative",
  1708	      "materiality": "evaluable",
  1709	      "protected_party": "Bank",
  1710	      "bound_party": "Merchant",
  1711	      "right_or_obligation": "right",
  1712	      "legal_object": "Банк имеет право удерживать суммы оспоренных операций или списанных со счёта испольнителя банком-эмитентом",
  1713	      "trigger": "",
  1714	      "deadline": "",
  1715	      "amount_formula_cap": "",
  1716	      "procedure_channel": "",
  1717	      "liability_remedy": "",
  1718	      "scope_options": [],
  1719	      "consequence": "withholding_right",
  1720	      "applicability_filters": {
  1721	        "required_type": "mandatory",
  1722	        "only_for_product": "common",
  1723	        "only_for_lot": "common",
  1724	        "only_for_terminal": "common",
  1725	        "payment_method": "common"
  1726	      }
  1727	    },
  1728	    {
  1729	      "id": "5.1.1.5",
  1730	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов и иных убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору.",
  1731	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов и иных убытков, возникших у Банка в результате применения к нему штрафных санкций в соот",
  1732	      "type": "operative",
  1733	      "materiality": "evaluable",
  1734	      "protected_party": "Bank",
  1735	      "bound_party": "Merchant",
  1736	      "right_or_obligation": "right",
  1737	      "legal_object": "Банк вправе удерживать штрафы из сумм Предприятия, возникшие у Банка в связи недобросовестным исполнением Заказчика контракта",
  1738	      "trigger": "",
  1739	      "deadline": "",
  1740	      "amount_formula_cap": "",
  1741	      "procedure_channel": "EIS",
  1742	      "liability_remedy": "penalty",
  1743	      "scope_options": [],
  1744	      "consequence": "withholding_right",
  1745	      "applicability_filters": {
  1746	        "required_type": "mandatory",
  1747	        "only_for_product": "common",
  1748	        "only_for_lot": "common",
  1749	        "only_for_terminal": "common",
  1750	        "payment_method": "common"
  1751	      }
  1752	    },
  1753	    {
  1754	      "id": "5.1.1.6",
  1755	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов в случае невозврата Электронных терминалов/Смарт-терминалов Банка в соответствии с п. 4.2.20.7 Договора.",
  1756	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов в случае невозврата Электронных терминалов/Смарт-терминалов Банка в соответствии с п. 4.",
  1757	      "type": "operative",
  1758	      "materiality": "evaluable",
  1759	      "protected_party": "Bank",
  1760	      "bound_party": "Merchant",
  1761	      "right_or_obligation": "right",
  1762	      "legal_object": "Банк имеет право удерживать суммы штрафов за невозврат Электронных терминалов/Смарт-терминалов",
  1763	      "trigger": "невозврата электронных терминалов/смарт-терминалов банка в соответствии с п",
  1764	      "deadline": "",
  1765	      "amount_formula_cap": "",
  1766	      "procedure_channel": "electronic",
  1767	      "liability_remedy": "penalty",
  1768	      "scope_options": [],
  1769	      "consequence": "withholding_right",
  1770	      "applicability_filters": {
  1771	        "required_type": "mandatory",
  1772	        "only_for_product": "trade_acquiring",
  1773	        "only_for_lot": "common",
  1774	        "only_for_terminal": "common",
  1775	        "payment_method": "common"
  1776	      }
  1777	    },
  1778	    {
  1779	      "id": "5.1.2",
  1780	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае возникновения у Предприятия задолженности перед Банком приостановить проведение Авторизации до момента полного погашения задолженности.",
  1781	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае возникновения у Предприятия задолженности перед Банком приостановить проведение Авторизации до момента полного погашения задолженности.",
  1782	      "type": "operative",
  1783	      "materiality": "evaluable",
  1784	      "protected_party": "Bank",
  1785	      "bound_party": "Merchant",
  1786	      "right_or_obligation": "right",
  1787	      "legal_object": "Банк вправе приостанавливать авторизацию при наличии задолженности у Предприятия",
  1788	      "trigger": "",
  1789	      "deadline": "",
  1790	      "amount_formula_cap": "",
  1791	      "procedure_channel": "",
  1792	      "liability_remedy": "",
  1793	      "scope_options": [],
  1794	      "consequence": "suspension_right",
  1795	      "applicability_filters": {
  1796	        "required_type": "mandatory",
  1797	        "only_for_product": "common",
  1798	        "only_for_lot": "common",
  1799	        "only_for_terminal": "common",
  1800	        "payment_method": "common"
  1801	      }
  1802	    },
  1803	    {
  1804	      "id": "5.1.3",
  1805	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, списывать без дополнительного распоряжения Предприятия (на условиях заранее данного акцепта, предоставленного Банку Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг) денежные средства с расчетного счета Предприятия, открытого в Банке. ",
  1806	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, списывать без дополнительного распоряжения Предприятия (на условия",
  1807	      "type": "operative",
  1808	      "materiality": "evaluable",
  1809	      "protected_party": "Bank",
  1810	      "bound_party": "Merchant",
  1811	      "right_or_obligation": "right",
  1812	      "legal_object": "списание средств без дополнительного распоряжения",
  1813	      "trigger": "невозможности удержать суммы",
  1814	      "deadline": "",
  1815	      "amount_formula_cap": "",
  1816	      "procedure_channel": "",
  1817	      "liability_remedy": "",
  1818	      "scope_options": [],
  1819	      "consequence": "withholding_right",
  1820	      "applicability_filters": {
  1821	        "required_type": "mandatory",
  1822	        "only_for_product": "common",
  1823	        "only_for_lot": "common",
  1824	        "only_for_terminal": "common",
  1825	        "payment_method": "common"
  1826	      }
  1827	    },
  1828	    {
  1829	      "id": "5.1.4",
  1830	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, Банк выставляет счет на оплату или платежное требование о списании денежных средств к расчетному счету Предприятия № --------------------------- в ----------------------- (наименование Банка, котором у Предприятия открыт счет). ",
  1831	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, Банк выставляет счет на оплату или платежное требование о списании",
  1832	      "type": "operative",
  1833	      "materiality": "evaluable",
  1834	      "protected_party": "Bank",
  1835	      "bound_party": "Merchant",
  1836	      "right_or_obligation": "right",
  1837	      "legal_object": "указан номер расчетного счета Предприятия",
  1838	      "trigger": "невозможности удержать суммы",
  1839	      "deadline": "",
  1840	      "amount_formula_cap": "",
  1841	      "procedure_channel": "",
  1842	      "liability_remedy": "",
  1843	      "scope_options": [],
  1844	      "consequence": "withholding_right",
  1845	      "applicability_filters": {
  1846	        "required_type": "mandatory",
  1847	        "only_for_product": "common",
  1848	        "only_for_lot": "common",
  1849	        "only_for_terminal": "common",
  1850	        "payment_method": "common"
  1851	      }
  1852	    },
  1853	    {
  1854	      "id": "5.1.5",
  1855	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Не возмещать Предприятию суммы Операций, проведенных с нарушением условий Договора.",
  1856	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Не возмещать Предприятию суммы Операций, проведенных с нарушением условий Договора.",
  1857	      "type": "operative",
  1858	      "materiality": "evaluable",
  1859	      "protected_party": "Bank",
  1860	      "bound_party": "Merchant",
  1861	      "right_or_obligation": "right",
  1862	      "legal_object": "Банк имеет право не возмещать суммы операций, проведенных с нарушением условий договора",
  1863	      "trigger": "",
  1864	      "deadline": "",
  1865	      "amount_formula_cap": "",
  1866	      "procedure_channel": "",
  1867	      "liability_remedy": "",
  1868	      "scope_options": [],
  1869	      "consequence": "",
  1870	      "applicability_filters": {
  1871	        "required_type": "mandatory",
  1872	        "only_for_product": "common",
  1873	        "only_for_lot": "common",
  1874	        "only_for_terminal": "common",
  1875	        "payment_method": "common"
  1876	      }
  1877	    },
  1878	    {
  1879	      "id": "5.1.6",
  1880	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять проверку технического состояния и порядка эксплуатации Электронных терминалов/Смарт-терминалов Банка, расположенных на территории Предприятия/ТСТ. Производить замену Электронных терминалов/Смарт-терминалов Банка, а также обновлять программное обеспечение Электронных терминалов/Смарт-терминалов, уведомив Предприятие не менее чем за 2 (два) рабочих дня до даты замены или обновления. Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения Операций, изложенный в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, без предварительного уведомления Предприятия.",
  1881	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять проверку технического состояния и порядка эксплуатации Электронных терминалов/Смарт-терминалов Банка, расположенных на территории Предприятия/ТСТ. Производить замену Электронных",
  1882	      "type": "operative",
  1883	      "materiality": "evaluable",
  1884	      "protected_party": "Bank",
  1885	      "bound_party": "Merchant",
  1886	      "right_or_obligation": "right",
  1887	      "legal_object": "Банк имеет право проверять техническое состояние терминалов на территории предприятия",
  1888	      "trigger": "",
  1889	      "deadline": "2 (два) рабочих дня",
  1890	      "amount_formula_cap": "",
  1891	      "procedure_channel": "electronic",
  1892	      "liability_remedy": "",
  1893	      "scope_options": [],
  1894	      "consequence": "",
  1895	      "applicability_filters": {
  1896	        "required_type": "mandatory",
  1897	        "only_for_product": "common",
  1898	        "only_for_lot": "common",
  1899	        "only_for_terminal": "common",
  1900	        "payment_method": "common"
  1901	      }
  1902	    },
  1903	    {
  1904	      "id": "5.1.7",
  1905	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Независимо от срока действия Договора в случае выявления подозрительных или мошеннических Операций передавать информацию, в том числе осуществлять передачу данных (сведения о Предприятии/ТСТ/Ресурсе, в том числе персональные данные руководителя/представителя Предприятия, указанные в Заявлении/Информации о ТСТ) в Платежную систему МИР в целях исполнения запросов, полученных от указанной платежной системы.В случае принятия Банком решения о расторжении Договора по причине мошеннической деятельности Предприятия сообщать в Платежную систему МИР: даты заключения и расторжения Договора, а также причины расторжения Договора, иные сведения о Предприятии.",
  1906	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Независимо от срока действия Договора в случае выявления подозрительных или мошеннических Операций передавать информацию, в том числе осуществлять передачу данных (сведения о Предприятии/ТСТ",
  1907	      "type": "operative",
  1908	      "materiality": "evaluable",
  1909	      "protected_party": "Bank",
  1910	      "bound_party": "Merchant",
  1911	      "right_or_obligation": "right",
  1912	      "legal_object": "Банк имеет право передавать информацию о предприятии при выявлении подозрительных операций",
  1913	      "trigger": "выявления подозрительных или мошеннических операций передавать информацию",
  1914	      "deadline": "",
  1915	      "amount_formula_cap": "",
  1916	      "procedure_channel": "",
  1917	      "liability_remedy": "",
  1918	      "scope_options": [],
  1919	      "consequence": "",
  1920	      "applicability_filters": {
  1921	        "required_type": "mandatory",
  1922	        "only_for_product": "common",
  1923	        "only_for_lot": "common",
  1924	        "only_for_terminal": "common",
  1925	        "payment_method": "common"
  1926	      }
  1927	    },
  1928	    {
  1929	      "id": "5.1.8.1",
  1930	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → нарушение Предприятием условий Договора;",
  1931	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → нарушение Предприятием условий Догов",
  1932	      "type": "operative",
  1933	      "materiality": "evaluable",
  1934	      "protected_party": "Bank",
  1935	      "bound_party": "Merchant",
  1936	      "right_or_obligation": "right",
  1937	      "legal_object": "нарушение Предприятием условий Договора является основанием для прекращения Авторизации и расторжения Договора",
  1938	      "trigger": "наступлении следующих событий: → нарушение предприятием условий договора",
  1939	      "deadline": "",
  1940	      "amount_formula_cap": "",
  1941	      "procedure_channel": "",
  1942	      "liability_remedy": "",
  1943	      "scope_options": [],
  1944	      "consequence": "",
  1945	      "applicability_filters": {
  1946	        "required_type": "optional",
  1947	        "only_for_product": "common",
  1948	        "only_for_lot": "common",
  1949	        "only_for_terminal": "common",
  1950	        "payment_method": "common"
  1951	      }
  1952	    },
  1953	    {
  1954	      "id": "5.1.8.2",
  1955	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → внесение данных Предприятия в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;",
  1956	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → внесение данных Предприятия в перече",
  1957	      "type": "operative",
  1958	      "materiality": "evaluable",
  1959	      "protected_party": "Bank",
  1960	      "bound_party": "Merchant",
  1961	      "right_or_obligation": "right",
  1962	      "legal_object": "внесение данных Предприятия в перечень организаций и физических лиц, причастных к экстремизму, терроризму или распространению оружия массового уничтожения является основанием для прекращения Авторизац",
  1963	      "trigger": "",
  1964	      "deadline": "",
  1965	      "amount_formula_cap": "",
  1966	      "procedure_channel": "",
  1967	      "liability_remedy": "",
  1968	      "scope_options": [],
  1969	      "consequence": "",
  1970	      "applicability_filters": {
  1971	        "required_type": "optional",
  1972	        "only_for_product": "common",
  1973	        "only_for_lot": "common",
  1974	        "only_for_terminal": "common",
  1975	        "payment_method": "common"
  1976	      }
  1977	    },
  1978	    {
  1979	      "id": "5.1.8.3",
  1980	      "source_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → при наличии у Банка подозрений, что Операции в ТСТ/на Ресурсе совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;",
  1981	      "source_excerpt": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → при наличии у Банка подозрений, что ",
  1982	      "type": "operative",
  1983	      "materiality": "evaluable",
  1984	      "protected_party": "Bank",
  1985	      "bound_party": "Merchant",
  1986	      "right_or_obligation": "right",
  1987	      "legal_object": "Банк вправе прекратить Авторизацию при подозрении на отмывание денег или финансирование терроризма",
  1988	      "trigger": "наступлении следующих событий: → при наличии у банка подозрений",
  1989	      "deadline": "",
  1990	      "amount_formula_cap": "",
  1991	      "procedure_channel": "",
  1992	      "liability_remedy": "",
  1993	      "scope_options": [],
  1994	      "consequence": "",
  1995	      "applicability_filters": {
  1996	        "required_type": "optional",
  1997	        "only_for_product": "common",
  1998	        "only_for_lot": "common",
  1999	        "only_for_terminal": "common",
  2000	        "payment_method": "common"
AI: I now have a solid understanding of the matrix propositions. Let me now focus on the **contract** side of the legal propositions to identify contract-only terms. Let me read the contract array from the legal propositions:[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/outputs/working/legal_propositions.json\', \'r\') as f:\n    data = json.load(f)\n# Print the first 30 contract entries to understand structure\nfor i, entry in enumerate(data[\'contract\'][:30]):\n    print(f\\"{i}: id={entry[\'id\']}, type={entry[\'type\']}, materiality={entry[\'materiality\']}, legal_object={entry[\'legal_object\'][:100]}\\")\nprint(f\'... total contract entries: {len(data[\\"contract\\"])}\')\n"'}, 'id': 'call_00_Vo7lzFRUFzItvDpYSzwk6785', 'type': 'tool_call'}]
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
[stderr] # Print the first 30 contract entries to understand structure
[stderr] for i, entry in enumerate(data['contract'][:30]):
[stderr]     print(f\"{i}: id={entry['id']}, type={entry['type']}, materiality={entry['materiality']}, legal_object={entry['lega
[stderr] l_object'][:100]}\")
[stderr] print(f'... total contract entries: {len(data[\"contract\"])}')
[stderr] "
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : ScriptBlock should only be specified as a value of the Command parameter.
[stderr] At line:44 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/enrich_propositions.py 2>&1 || echo "script not runnable, using direct python"'}, 'id': 'call_00_CGu6fJBtE9wS18WOmBAR4451', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:52
[stderr] + python outputs/working/enrich_propositions.py 2>&1 || echo "script no ...
[stderr] +                                                    ~~
[stderr] The token '||' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "import json; data=json.load(open(\'/outputs/working/legal_propositions.json\',\'r\')); [print(f\'{i}: id={e[\\"id\\"]}, type={e[\\"type\\"]}, mat={e[\\"materiality\\"]}, obj={e[\\"legal_object\\"][:80]}\') for i,e in enumerate(data[\'contract\'][:40])]; print(f\'Total contract: {len(data[\\"contract\\"])}\')"'}, 'id': 'call_00_q90RYkvXgmsgyigE3LKt2472', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 1
[stderr]     import json; data=json.load(open('outputs/working/legal_propositions.json','r')); [print(f'{i}: id={e[" id\]},
[stderr]                                                                                                           ^
[stderr] SyntaxError: unterminated string literal (detected at line 1)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/inspect_contract.py', 'content': 'import json\n\nwith open(\'/outputs/working/legal_propositions.json\', \'r\') as f:\n    data = json.load(f)\n\nprint("=== CONTRACT PROPOSITIONS ===")\nfor i, entry in enumerate(data[\'contract\']):\n    print(f"{i}: id={entry[\'id\']}, type={entry[\'type\']}, mat={entry[\'materiality\']}, obj={entry[\'legal_object\'][:100]}")\nprint(f"\\nTotal contract entries: {len(data[\'contract\'])}")\n'}, 'id': 'call_00_CfIJyEUf4lLnuyJ0ecpP7410', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/inspect_contract.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/inspect_contract.py'}, 'id': 'call_00_m8ypfSdaL1SSQHhtLXXp7138', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\inspect_contract.py", line 3, in <module>
[stderr]     with open('/outputs/working/legal_propositions.json', 'r') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/legal_propositions.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python C:/Users/gogel/OneDrive/Рабочий\\ стол/Проекты/skillshot_manual_2/outputs/working/inspect_contract.py'}, 'id': 'call_00_6X1n3GrTr0dh9cZ2nJrB5723', 'type': 'tool_call'}]
Tool: [stderr] C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\.venv\Scripts\python.exe: can't open file 'C:\\Users\\gogel\\OneDrive\\Р Р°Р±РѕС‡РёР№\\': [Errno 2] No such file or directory

Exit code: 2
[Command failed with exit code 2]
AI: [{'name': 'execute', 'args': {'command': 'cd "C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2" && python outputs/working/inspect_contract.py'}, 'id': 'call_00_Gcals79aVKN06LaNiggV6259', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:70
[stderr] + ... rs/gogel/OneDrive/Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»/РџСЂРѕРµРєС‚С‹/skillshot_manual_2" && python  ...
[stderr] +                                                                ~~
[stderr] The token '&&' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'Set-Location "C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2"; python outputs/working/inspect_contract.py'}, 'id': 'call_00_cwMuwKxTHN3R7aODuqJC3882', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\inspect_contract.py", line 3, in <module>
[stderr]     with open('/outputs/working/legal_propositions.json', 'r') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/legal_propositions.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/inspect_contract.py', 'old_string': "with open('/outputs/working/legal_propositions.json', 'r') as f:", 'new_string': "import os\nbase = os.path.dirname(os.path.abspath(__file__))\nwith open(os.path.join(base, 'legal_propositions.json'), 'r') as f:"}, 'id': 'call_00_ZtMuvNHpMRerEPVeAWZc8442', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/inspect_contract.py'
AI: [{'name': 'execute', 'args': {'command': 'Set-Location "C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2"; python outputs/working/inspect_contract.py'}, 'id': 'call_00_PQpyzN3bMsipbuyvcl291093', 'type': 'tool_call'}]
Tool: === CONTRACT PROPOSITIONS ===
0: id=1, type=operative, mat=evaluable, obj=РџР Р•Р”РњР•Рў РљРћРќРўР РђРљРўРђ
1: id=1.1, type=operative, mat=evaluable, obj=РџРѕ СѓСЃР»РѕРІРёСЏРј РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРєР°Р·Р°С‚СЊ Р—Р°РєР°Р·С‡РёРєСѓ СѓСЃР»СѓРіРё РїРѕ РїСЂРёРµРјСѓ Рє РѕРїР»Р°С‚Рµ Рї
2: id=1.2, type=operative, mat=evaluable, obj=РћР±СЉРµРј СѓСЃР»СѓРі, СѓРєР°Р·Р°РЅРЅС‹С… РІ РїСѓРЅРєС‚Рµ 1.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ РїРѕС‚СЂРµР±РЅРѕСЃС‚СЊСЋ Р—Р°РєР°Р·С‡РёРєР° РЅР° СЃСѓРј
3: id=1.3, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РѕСЂРіР°РЅРёР·СѓРµС‚ РїСЂРёРµРј РєР°СЂС‚ РІ РєР°С‡РµСЃС‚РІРµ СЃСЂРµРґСЃС‚РІР° РѕРїР»Р°С‚С‹ Р·Р° СЂРµР°Р»РёР·СѓРµРјС‹Рµ РёРј С‚РѕРІР°СЂС‹/СѓСЃР»СѓРіРё Рё РѕР±СЂР°Р±РѕС‚Рє
4: id=2, type=heading, mat=heading, obj=РўР•Р РњР�РќР«, РћРџР Р•Р”Р•Р›Р•РќР�РЇ Р� Р’Р—РђР�РњРћР”Р•Р™РЎРўР’Р�Р•
5: id=2.1, type=operative, mat=evaluable, obj=РђРІС‚РѕСЂРёР·Р°С†РёСЏ вЂ“ РїСЂРѕС†РµРґСѓСЂР° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°Р·СЂРµС€РµРЅРёСЏ РѕС‚ Р±Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё РёРЅРѕРіРѕ СЋСЂРёРґРёС‡РµСЃРєРѕРіРѕ Р»РёС†Р°, РґРµР№СЃС‚РІСѓСЋ
6: id=2.1.1, type=operative, mat=evaluable, obj=Р±Р°РЅРєРѕРІСЃРєР°СЏ РєР°СЂС‚Р° (РєР°СЂС‚Р°) вЂ“ СЂР°СЃС‡РµС‚РЅР°СЏ (РґРµР±РµС‚РѕРІР°СЏ), РєСЂРµРґРёС‚РЅР°СЏ РёР»Рё РїСЂРµРґРѕРїР»Р°С‡РµРЅРЅР°СЏ РєР°СЂС‚Р° СЃ Р»РѕРіРѕС‚РёРїРѕРј РїР»Р°
7: id=2.1.2, type=operative, mat=evaluable, obj=Р±Р°РЅРє-СЌРєРІР°Р№СЂРµСЂ - РєСЂРµРґРёС‚РЅР°СЏ РѕСЂРіР°РЅРёР·Р°С†РёСЏ, СЏРІР»СЏСЋС‰Р°СЏСЃСЏ СѓС‡Р°СЃС‚РЅРёРєРѕРј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, РѕСЂРіР°РЅРёР·СѓСЋС‰Р°СЏ С‚РѕС‡РєРё Рї
8: id=2.1.3, type=operative, mat=evaluable, obj=Р±Р°РЅРє-СЌРјРёС‚РµРЅС‚ вЂ“ РєСЂРµРґРёС‚РЅР°СЏ РѕСЂРіР°РЅРёР·Р°С†РёСЏ, СЏРІР»СЏСЋС‰Р°СЏСЃСЏ СѓС‡Р°СЃС‚РЅРёРєРѕРј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰Р°СЏ СЌРјРёСЃСЃ
9: id=2.1.4, type=operative, mat=evaluable, obj=РІРѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° вЂ“ РѕРїРµСЂР°С†РёСЏ, РёРЅРёС†РёРёСЂСѓРµРјР°СЏ Р±Р°РЅРєРѕРј-СЌРјРёС‚РµРЅС‚РѕРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚Рµ
10: id=2.1.5, type=operative, mat=evaluable, obj=РґРµСЂР¶Р°С‚РµР»СЊ РєР°СЂС‚С‹ (РґРµСЂР¶Р°С‚РµР»СЊ) вЂ“ РїРѕРєСѓРїР°С‚РµР»СЊ-С„РёР·РёС‡РµСЃРєРѕРµ Р»РёС†Рѕ, РЅР° РёРјСЏ РєРѕС‚РѕСЂРѕРіРѕ РІС‹РїСѓС‰РµРЅР° РєР°СЂС‚Р°;
11: id=2.1.6, type=operative, mat=evaluable, obj=РґРѕРєСѓРјРµРЅС‚ РїРѕ РѕРїРµСЂР°С†РёРё - РґРѕРєСѓРјРµРЅС‚ РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ РёР»Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ, СЏРІР»СЏСЋС‰РёР№СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј Рґ
12: id=2.1.7, type=operative, mat=evaluable, obj=РєРѕРґ Р°РІС‚РѕСЂРёР·Р°С†РёРё - Р±СѓРєРІРµРЅРЅРѕ-С†РёС„СЂРѕРІРѕР№ РєРѕРґ, РїРѕРґС‚РІРµСЂР¶РґР°СЋС‰РёР№ СѓСЃРїРµС€РЅРѕРµ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё;
13: id=2.1.8, type=operative, mat=evaluable, obj=РєРѕРЅС‚СЂРѕР»СЊРЅРѕ-РєР°СЃСЃРѕРІР°СЏ С‚РµС…РЅРёРєР° (РљРљРў) вЂ“ РїСЂРѕРіСЂР°РјРјРЅРѕ-С‚РµС…РЅРёС‡РµСЃРєРёРµ СЃСЂРµРґСЃС‚РІР° Рё РёС… РєРѕРјРїР»РµРєСЃС‹, РѕР±РµСЃРїРµС‡РёРІР°СЋС‰РёРµ Р·
14: id=2.1.9, type=operative, mat=evaluable, obj=РєРѕРЅС‚СЂРѕР»СЊРЅР°СЏ Р»РµРЅС‚Р° - РѕС‚С‡РµС‚, СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµРјС‹Р№ РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ Рё СЃРѕРґРµСЂР¶Р°С‰РёР№ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ С‚СЂР°РЅР·Р°
15: id=2.1.10, type=operative, mat=evaluable, obj=РѕС‚Р»РѕР¶РµРЅРЅС‹Р№ РїР»Р°С‚РµР¶ - РѕРїРµСЂР°С†РёСЏ РѕРїР»Р°С‚С‹, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјР°СЏ РЅР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕРіРѕ РѕС‚ Р—Р°РєР°Р·С‡РёРєР°/РўРЎРў СЃРѕРѕР±С‰Рµ
16: id=2.1.11, type=operative, mat=evaluable, obj=РѕРїРµСЂР°С†РёСЏ вЂ“ РґРµР№СЃС‚РІРёРµ, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјРѕРµ Р—Р°РєР°Р·С‡РёРєРѕРј/РўРЎРў/РїРѕРєСѓРїР°С‚РµР»РµРј РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ, РІ С‚РѕРј С‡РёСЃР»Рµ
17: id=2.1.12, type=operative, mat=evaluable, obj=РѕРїРµСЂР°С†РёСЏ РѕРїР»Р°С‚С‹ вЂ“ РѕРїРµСЂР°С†РёСЏ РїРѕ РѕРїР»Р°С‚Рµ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РєР°СЂС‚С‹ РІ СѓС‡СЂРµР¶РґРµРЅРёРё Р—Р°РєР°Р·С‡РёРєР°/ РўРЎ
18: id=2.1.13, type=operative, mat=evaluable, obj=РѕРїРµСЂР°С†РёСЏ РѕС‚РјРµРЅС‹ вЂ“ РѕРїРµСЂР°С†РёСЏ, РІС‹РїРѕР»РЅСЏРµРјР°СЏ Р—Р°РєР°Р·С‡РёРєРѕРј/РўРЎРў РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ/СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Рµ, СЃ С†
19: id=2.1.14, type=operative, mat=evaluable, obj=РѕРїРµСЂР°С†РёСЏ РІРѕР·РІСЂР°С‚Р° вЂ“ РѕРїРµСЂР°С†РёСЏ, РѕС„РѕСЂРјР»СЏРµРјР°СЏ Р—Р°РєР°Р·С‡РёРєРѕРј/РўРЎРў РїСЂРё РІРѕР·РІСЂР°С‚Рµ С‚РѕРІР°СЂРѕРІ/РѕС‚РєР°Р·Рµ РѕС‚ СѓСЃР»СѓРі РёР»Рё РѕС‚
20: id=2.1.15, type=operative, mat=evaluable, obj=РїР»Р°С‚РµР¶РЅР°СЏ СЃРёСЃС‚РµРјР° вЂ“ СЃРѕРІРѕРєСѓРїРЅРѕСЃС‚СЊ РѕСЂРіР°РЅРёР·Р°С†РёР№, РІР·Р°РёРјРѕРґРµР№СЃС‚РІСѓСЋС‰РёС… РїРѕ РїСЂР°РІРёР»Р°Рј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РІ С†РµР»СЏ
21: id=2.1.16, type=operative, mat=evaluable, obj=РїРѕРєСѓРїР°С‚РµР»СЊ - С„РёР·РёС‡РµСЃРєРѕРµ Р»РёС†Рѕ, РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰РµРµ РѕРїР»Р°С‚Сѓ С‚РѕРІР°СЂР°/СѓСЃР»СѓРіРё РІ РўРЎРў РїСЂРё РїРѕРјРѕС‰Рё РєР°СЂС‚С‹, Р° С‚Р°РєР¶Рµ Р»Рё
22: id=2.1.17, type=operative, mat=evaluable, obj=РїРѕРІС‚РѕСЂСЏСЋС‰РёРµСЃСЏ РїР»Р°С‚РµР¶Рё вЂ“ РїР»Р°С‚РµР¶Рё РІ РѕРїР»Р°С‚Сѓ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјС‹Рµ СЂРµРіСѓР»СЏСЂРЅРѕ РІ С‚РµС‡РµРЅРёРµ РѕРїСЂРµРґРµР»РµРЅ
23: id=2.1.18, type=operative, mat=evaluable, obj=РїСЂРµРґР°РІС‚РѕСЂРёР·Р°С†РёСЏ - РѕРїРµСЂР°С†РёСЏ РїРѕ СЂРµР·РµСЂРІРёСЂРѕРІР°РЅРёСЋ РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° РєР°СЂС‚Рµ РґР»СЏ РїРѕСЃР»РµРґСѓСЋС‰РµР№ РѕРїР»Р°С‚С‹, С‚СЂРµР±Сѓ
24: id=2.1.19, type=operative, mat=evaluable, obj=РїСЂРµРґРїСЂРёСЏС‚РёРµ (Р—Р°РєР°Р·С‡РёРє) вЂ“ С‚РѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅРѕРµ РїСЂРµРґРїСЂРёСЏС‚РёРµ (РўРЎРџ): СЋСЂРёРґРёС‡РµСЃРєРѕРµ Р»РёС†Рѕ/ РёРЅРґРёРІРёРґСѓР°Р»СЊРЅС‹Р№ РїСЂРµРґРї
25: id=2.1.20, type=operative, mat=evaluable, obj=СЂР°Р±РѕС‡РёР№ РґРµРЅСЊ вЂ“ РґРµРЅСЊ, РєРѕС‚РѕСЂС‹Р№ РЅРµ РїСЂРёР·РЅР°РµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё РІ
26: id=2.1.21, type=operative, mat=evaluable, obj=СЂРµРІРµСЂСЃРёРІРЅР°СЏ С‚СЂР°РЅР·Р°РєС†РёСЏ вЂ“ С„РёРЅР°РЅСЃРѕРІРѕ-РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ, РєРѕС‚РѕСЂРѕРµ Р±Р°РЅРє-СЌРєРІР°Р№СЂРµСЂ РЅР°РїСЂР°РІР»СЏРµС‚ РІ РїР»Р°С‚
27: id=2.1.22, type=operative, mat=evaluable, obj=СЃРІРѕРґРЅС‹Р№ С‡РµРє СЌР»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° вЂ“ Р±СѓРјР°Р¶РЅС‹Р№ РѕС‚С‡РµС‚, СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµРјС‹Р№ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј Рё СЃРѕРґРµСЂР¶
28: id=2.1.23, type=operative, mat=evaluable, obj=С‚Р°СЂРёС„С‹ Р±Р°РЅРєР°вЂ“ СЃС‚РѕРёРјРѕСЃС‚СЊ СѓСЃР»СѓРі Р±Р°РЅРєР° Р·Р° РІС‹РїРѕР»РЅРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ РІ РІРёРґРµ РїСЂРѕС†РµРЅС‚Р° РѕС‚ СЃСѓ
29: id=2.1.24, type=operative, mat=evaluable, obj=С‚РѕРІР°СЂ/СѓСЃР»СѓРіР° вЂ“ С‚РѕРІР°СЂ, СЂР°Р±РѕС‚Р°, СѓСЃР»СѓРіР°, СЂРµР·СѓР»СЊС‚Р°С‚ РёРЅС‚РµР»Р»РµРєС‚СѓР°Р»СЊРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, СЂРµР°Р»РёР·СѓРµРјС‹Рµ Р—Р°РєР°Р·С‡РёРєРѕ
30: id=2.1.25, type=operative, mat=evaluable, obj=С‚РѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅР°СЏ С‚РѕС‡РєР° (РўРЎРў) вЂ“ РїРѕРґСЂР°Р·РґРµР»РµРЅРёРµ Р—Р°РєР°Р·С‡РёРєР°, Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°РЅРЅРѕРµ Р±Р°РЅРєРѕРј РЅР° РѕСЃРЅРѕРІР°РЅРёРё РёРЅС„Рѕ
31: id=2.1.26, type=operative, mat=evaluable, obj=С‚РѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі вЂ“ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ Р±Р°РЅРєРѕРј-СЌРєРІР°Р№СЂРµСЂРѕРј СЂР°СЃС‡РµС‚РѕРІ СЃ РїСЂРµРґРїСЂРёСЏС‚РёСЏРјРё, РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰РёРјРё СЂРµР°Р»Рё
32: id=2.1.27, type=operative, mat=evaluable, obj=С‡РµРє СЌР»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° (С‡РµРє) вЂ“ РґРѕРєСѓРјРµРЅС‚ РїРѕ РѕРїРµСЂР°С†РёРё, СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµРјС‹Р№ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј Рё СЃРѕ
33: id=2.1.28, type=operative, mat=evaluable, obj=СЌР»РµРєС‚СЂРѕРЅРЅР°СЏ СЃРІРµСЂРєР° РёС‚РѕРіРѕРІ вЂ“ РїСЂРѕС†РµРґСѓСЂР° РїРµСЂРµРґР°С‡Рё РѕС‚ СЌР»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° РёСЃРїРѕР»РЅРёС‚РµР»СЋ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂ
34: id=2.2, type=operative, mat=evaluable, obj=СЌР»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» вЂ“ СЌР»РµРєС‚СЂРѕРЅРЅРѕРµ РїСЂРѕРіСЂР°РјРјРЅРѕ-С‚РµС…РЅРёС‡РµСЃРєРѕРµ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ РёСЃРїРѕР»РЅРёС‚РµР»СЏ (РІ С‚РѕРј С‡РёСЃР»Рµ РґРѕРїРѕР»РЅ
35: id=2.3, type=operative, mat=evaluable, obj=Р‘Р°РЅРє Рё Р—Р°РєР°Р·С‡РёРє РІ СЂР°РјРєР°С… РЅР°СЃС‚РѕСЏС‰РµРіРѕ РљРѕРЅС‚СЂР°РєС‚Р° РѕР±РјРµРЅРёРІР°СЋС‚СЃСЏ РёРЅС„РѕСЂРјР°С†РёРµР№ Рё РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕРґРЅРёРј РёР· СЃР»РµРґСѓСЋ
36: id=2.3.1, type=operative, mat=evaluable, obj=СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј СЌР»РµРєС‚СЂРѕРЅРЅС‹С… РєР°РЅР°Р»РѕРІ СЃРІСЏР·Рё РїСѓС‚РµРј РЅР°РїСЂР°РІР»РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё/РґРѕРєСѓРјРµРЅС‚Р° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ
37: id=2.3.2, type=operative, mat=evaluable, obj=РїРѕСЃСЂРµРґСЃС‚РІРѕРј СЃРёСЃС‚РµРјС‹ Р”Р‘Рћ РёР»Рё Р°РЅР°Р»РѕРіРёС‡РЅС‹С… СЃРёСЃС‚РµРј Р‘Р°РЅРєР°;
38: id=2.3.3, type=operative, mat=evaluable, obj=РїСѓС‚РµРј РЅР°РїСЂР°РІР»РµРЅРёСЏ РїРёСЃСЊРјР° СЃ РґРѕСЃС‚Р°РІРєРѕР№ РЅР°СЂРѕС‡РЅС‹Рј РёР»Рё РєСѓСЂСЊРµСЂСЃРєРѕР№ РїРѕС‡С‚РѕР№ РїРѕ РїРѕС‡С‚РѕРІРѕРјСѓ Р°РґСЂРµСЃСѓ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ 
39: id=2.3.4, type=operative, mat=evaluable, obj=РїСѓС‚РµРј РЅР°РїСЂР°РІР»РµРЅРёСЏ РїРѕС‡С‚РѕРІРѕРіРѕ РѕС‚РїСЂР°РІР»РµРЅРёСЏ (Р·Р°РєР°Р·РЅРѕРіРѕ РїРёСЃСЊРјР°) РїРѕ РїРѕС‡С‚РѕРІРѕРјСѓ Р°РґСЂРµСЃСѓ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р—Р°СЏРІР»РµРЅ
40: id=2.3.5, type=operative, mat=evaluable, obj=РїСѓС‚РµРј РѕР±РјРµРЅР° СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РґРѕРєСѓРјРµРЅС‚Р°РјРё РїРѕСЃСЂРµРґСЃС‚РІРѕРј Р°РІС‚РѕРјР°С‚РёР·РёСЂРѕРІР°РЅРЅРѕР№ СЃРёСЃС‚РµРјС‹ _________________. Р’ СЌС‚
41: id=2.3.6, type=operative, mat=evaluable, obj=РїСѓС‚РµРј РѕР±РјРµРЅР° СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РґРѕРєСѓРјРµРЅС‚Р°РјРё РІ Р•РґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РІ СЃС„РµСЂРµ Р·Р°РєСѓРїРѕРє Рё РёРЅС‹С… СЌР»РµРєС‚СЂРѕ
42: id=2.3.7, type=operative, mat=evaluable, obj=С‡РµСЂРµР· РєРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ СЃР»СѓР¶Р±С‹ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР° (24/7), СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї.2 РџРѕСЂСЏРґРєР° РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ
43: id=3, type=operative, mat=evaluable, obj=Р¦Р•РќРђ РљРћРќРўР РђРљРўРђ
44: id=3.1, type=operative, mat=evaluable, obj=РњР°РєСЃРёРјР°Р»СЊРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р° (СЃС‚РѕРёРјРѕСЃС‚СЊ СѓСЃР»СѓРі) (РґР°Р»РµРµ вЂ“ С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р°) СЃРѕСЃС‚Р°РІР»СЏРµС‚ 1 900 000
45: id=3.1.1, type=operative, mat=evaluable, obj=Р¦РµРЅР° Р·Р° РµРґРёРЅРёС†Сѓ СѓСЃР»СѓРіРё СѓРєР°Р·Р°РЅР° РІ СЃРїРµС†РёС„РёРєР°С†РёРё (РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1), СЏРІР»СЏСЋС‰РµР№СЃСЏ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ РЅР°СЃС‚Рѕ
46: id=3.2, type=operative, mat=evaluable, obj=Р¦РµРЅР° РµРґРёРЅРёС†С‹ СѓСЃР»СѓРіРё РІРєР»СЋС‡Р°РµС‚ РІ СЃРµР±СЏ СЂР°СЃС…РѕРґС‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, СЃРІСЏР·Р°РЅРЅС‹Рµ СЃ РѕРєР°Р·Р°РЅРёРµРј СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РІС‹РїРѕР»РЅ
47: id=3.3, type=operative, mat=evaluable, obj=РџРѕР»РѕР¶РµРЅРёСЏ РЅР°СЃС‚РѕСЏС‰РµРіРѕ РљРѕРЅС‚СЂР°РєС‚Р°, РєР°СЃР°СЋС‰РёРµСЃСЏ РїСЂРёРјРµРЅРµРЅРёСЏ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р° РёР»Рё РЅР°С‡Р°Р»СЊРЅРѕР№ РјР°РєСЃРёРјР°Р»СЊРЅРѕР№ С†РµРЅС‹
48: id=4, type=operative, mat=evaluable, obj=РЎР РћРљР�, РЈРЎР›РћР’Р�РЇ РћРљРђР—РђРќР�РЇ РЈРЎР›РЈР“, РџРћР РЇР”РћРљ РћРџР›РђРўР«
49: id=4.1, type=operative, mat=evaluable, obj=РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃ В«01В» РјР°СЂС‚Р° 2025 РіРѕРґР° РїРѕ В«30В» РЅРѕСЏР±СЂСЏ 2025 РіРѕРґР° (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ) РёР»Рё РґРѕ 
50: id=4.2, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РµСЃР»Рё РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё Рё РёР·РІРµС‰РµРЅРёРµРј Рѕ РїСЂРѕРІРµРґРµРЅРёРё Р·Р°РєСѓРїРєРё Рї
51: id=4.3, type=operative, mat=evaluable, obj=РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РїРѕ Р°РґСЂРµСЃСѓ РјРµСЃС‚РѕРїРѕР»РѕР¶РµРЅРёСЏ С‚РѕС‡РµРє РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РїР»Р°СЃС‚РёРєРѕРІС‹
52: id=4.4, type=operative, mat=evaluable, obj=РћРїР»Р°С‚Р° РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїРѕ Р±РµР·РЅР°Р»РёС‡РЅРѕРјСѓ СЂР°СЃС‡С‘С‚Сѓ РїР»Р°С‚С‘Р¶РЅС‹Рј РїРѕСЂСѓС‡РµРЅРёРµРј РїСѓС‚С‘Рј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ Р—
53: id=4.5, type=operative, mat=evaluable, obj=РЎСЂРѕРє РѕРїР»Р°С‚С‹ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі СЃРѕСЃС‚Р°РІР»СЏРµС‚ РЅРµ Р±РѕР»РµРµ 7 (СЃРµРјРё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј Рґ
54: id=4.5.1, type=operative, mat=evaluable, obj=РЈСЃР»СѓРіРё, РѕРєР°Р·Р°РЅРЅС‹Рµ РІ РЅРѕСЏР±СЂРµ РѕРїР»Р°С‡РёРІР°СЋС‚СЃСЏ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 7 (СЃРµРјРё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ Р—Р°
55: id=5, type=operative, mat=evaluable, obj=РћР‘РЇР—РђРўР•Р›Р¬РЎРўР’Рђ РЎРўРћР РћРќ
56: id=5.1, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·СѓРµС‚СЃСЏ:
57: id=5.1.1, type=operative, mat=evaluable, obj=РЈСЃС‚Р°РЅРѕРІРёС‚СЊ Р—Р°РєР°Р·С‡РёРєСѓ Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ С‚Рµ
58: id=5.1.2, type=operative, mat=evaluable, obj=Р•Р¶РµРјРµСЃСЏС‡РЅРѕ С„РѕСЂРјРёСЂРѕРІР°С‚СЊ Рё РЅР°РїСЂР°РІР»СЏС‚СЊ Р—Р°РєР°Р·С‡РёРєСѓ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚Р°РјРё 8.3.1 Рё 8
59: id=5.1.3, type=operative, mat=evaluable, obj=РћР±РµСЃРїРµС‡РёС‚СЊ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРµРґСЉСЏРІР»СЏРµРјС‹Рј Рє РЅРёРј С‚СЂРµР±РѕРІР°РЅРёСЏРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р РѕСЃСЃРёР№СЃРєРѕР№ 
60: id=5.1.4, type=operative, mat=evaluable, obj=РћР±РµСЃРїРµС‡РёРІР°С‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ. Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° РёР· СЃС‚СЂРѕСЏ Р­Р»РµРєС‚
61: id=5.1.5, type=operative, mat=evaluable, obj=РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ Р—Р°РєР°Р·С‡РёРєСѓ РїРѕР»РЅСѓСЋ Рё С‚РѕС‡РЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёСЋ РѕР± СѓСЃР»СѓРіР°С…, Р° С‚Р°РєР¶Рµ Рѕ С…РѕРґРµ РёСЃРїРѕР»РЅРµРЅРёСЏ СЃРІРѕРёС… РѕР±СЏР·Р°
62: id=5.1.6, type=operative, mat=evaluable, obj=РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ;
63: id=5.1.7, type=operative, mat=evaluable, obj=РћР±РµСЃРїРµС‡РёРІР°С‚СЊ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ Сѓ Р·Р°РєР°Р·С‡РёРєР°/РўРЎРў, СЂРµРєР»Р°РјРЅРѕ-РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»
64: id=5.1.8, type=operative, mat=evaluable, obj=РќР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕР№ РѕС‚ Р—Р°РєР°Р·С‡РёРєР° СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё, РїРµСЂРµРґР°РЅРЅРѕР№ РѕС‚ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° Р�СЃРїРѕ
65: id=5.1.9, type=operative, mat=evaluable, obj=РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РѕР±СЂР°Р±РѕС‚РєСѓ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ Р·Р°РєР°Р·С‡РёРєР°, Р° С‚Р°РєР¶Рµ РѕР±РµСЃРїРµС‡РёС‚СЊ РєРѕРЅС„РёРґРµРЅС†РёР°Р»
66: id=5.1.10, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј РїРµСЂРµС‡РёСЃР»СЏРµС‚ Р—Р°РєР°Р·С‡РёРєСѓ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ СѓСЃР»СѓРі, СЃРѕРІРµСЂС€РµРЅРЅ
67: id=5.2, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІРїСЂР°РІРµ:
68: id=5.2.1, type=operative, mat=evaluable, obj=РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ Р—Р°РєР°Р·С‡РёРєР° СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РїСЂРёРµРјРєРµ Рё РѕРїР»Р°С‚Рµ СЃС‚РѕРёРјРѕСЃС‚Рё СѓСЃР»СѓРі РїРѕ
69: id=5.2.2, type=operative, mat=evaluable, obj=РџСЂРёРЅСЏС‚СЊ СЂРµС€РµРЅРёРµ РѕР± РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РѕС‚РєР°Р·Рµ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ РѕСЃРЅРѕРІР°РЅРёСЏРј, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹Рј Р¤РµРґРµСЂ
70: id=5.2.3, type=operative, mat=evaluable, obj=РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїСЂРѕРІРµСЂРєСѓ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ Рё РїРѕСЂСЏРґРєР° СЌРєСЃРїР»СѓР°С‚Р°С†РёРё СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ, СЂР°СЃРїРѕР»РѕР¶
71: id=5.2.4, type=operative, mat=evaluable, obj=Р”РѕРїСѓСЃРєР°РµС‚СЃСЏ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ СѓРґР°Р»РµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ, РЅРµ Р·Р°С‚СЂР°РіРёРІР°СЋС‰РµРµ РїРѕСЂСЏРґРѕРє РїСЂРѕ
72: id=5.2.5, type=operative, mat=evaluable, obj=Р—Р°РїСЂР°С€РёРІР°С‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РЅРµ РїРѕР·РґРЅРµРµ С‚СЂРёРЅР°РґС†Р°С‚Рё РјРµСЃСЏС†РµРІ СЃ РґР°С‚С‹ СЃРѕРІРµСЂС€РµРЅРёСЏ РѕРїРµСЂР°С†РёРё. Р”Р»СЏ Р°РЅР°
73: id=5.2.6, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РёР·РјРµРЅРµРЅРёСЏ СЂРµРєРІРёР·РёС‚РѕРІ РёСЃРїРѕР»РЅРёС‚РµР»СЏ, СѓРєР°Р·Р°РЅРЅС‹С… РІ РєРѕРЅС‚СЂР°РєС‚Рµ, СѓРІРµРґРѕРјРёС‚СЊ РѕР± СЌС‚РѕРј Р·Р°РєР°Р·С‡РёРєР° РІ РїРёСЃСЊ
74: id=5.2.7, type=operative, mat=evaluable, obj=Р’ С†РµР»СЏС… РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РѕРїРµСЂР°С†РёСЏРј РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ Р·Р°РєР°Р·С‡РёРєР°/РўРЎ
75: id=5.2.8, type=operative, mat=evaluable, obj=РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ Р·Р°РєР°Р·С‡РёРєР° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, 
76: id=5.2.9, type=operative, mat=evaluable, obj=Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ 
77: id=5.2.9.1, type=operative, mat=evaluable, obj=РЅР°СЂСѓС€РµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј СѓСЃР»РѕРІРёР№ РљРѕРЅС‚СЂР°РєС‚Р°;
78: id=5.2.9.2, type=operative, mat=evaluable, obj=РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… Р—Р°РєР°Р·С‡РёРєР° РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РІ РѕС‚РЅРѕС€РµРЅРёРё РєРѕС‚РѕСЂС‹С… РёРјРµСЋС‚СЃСЏ СЃРІРµРґРµ
79: id=5.2.9.3, type=operative, mat=evaluable, obj=РїСЂРё РЅР°Р»РёС‡РёРё Сѓ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РїРѕРґРѕР·СЂРµРЅРёР№, С‡С‚Рѕ РћРїРµСЂР°С†РёРё РІ РўРЎРў СЃРѕРІРµСЂС€Р°СЋС‚СЃСЏ РІ С†РµР»СЏС… Р»РµРіР°Р»РёР·Р°С†РёРё (РѕС‚РјС‹РІР°РЅРёСЏ)
80: id=5.2.9.4, type=operative, mat=evaluable, obj=РїРѕР»СѓС‡РµРЅРёРµ РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ Р—Р°РєР°Р·С‡РёРєРµ/РўРЎРў РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё Р Р¤ Рё/РёР»Рё РџР»Р°С‚РµР¶РЅС‹С…
81: id=5.2.9.5, type=operative, mat=evaluable, obj=РїРѕР»СѓС‡РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ РІ РўРЎРў СЃС‚РѕСЂРѕРЅС‹ РґРѕРіРѕРІРѕСЂРёР»РёСЃСЊ, С‡С‚Рѕ РґРѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€Рµ
82: id=5.2.9.6, type=operative, mat=evaluable, obj=РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЋ РћРїРµСЂР°С†РёР№;
83: id=5.2.9.7, type=operative, mat=evaluable, obj=Р»РёРєРІРёРґР°С†РёСЏ Р—Р°РєР°Р·С‡РёРєР° Р»РёР±Рѕ РІРѕР·Р±СѓР¶РґРµРЅРёРµ РІ РѕС‚РЅРѕС€РµРЅРёРё Р—Р°РєР°Р·С‡РёРєР° РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р¤РµРґРµ
84: id=5.2.9.8, type=operative, mat=evaluable, obj=РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ Р—Р°РєР°Р·С‡РёРєРµ/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂРё Р·Р°РєР»
85: id=5.2.9.9, type=operative, mat=evaluable, obj=РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё Р—Р°РєР°Р·С‡РёРєР°, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„Рѕ
86: id=5.2.9.10, type=operative, mat=evaluable, obj=РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ
87: id=5.2.9.11, type=operative, mat=evaluable, obj=РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ РљРѕРЅС‚СЂР°РєС‚Р° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ РљРѕРЅС‚СЂР°РєС‚Р°.
88: id=5.2.10, type=operative, mat=evaluable, obj=РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ Р—Р°РєР°Р·С‡РёРєСѓ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹:
89: id=5.2.10.1, type=operative, mat=evaluable, obj=РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№, СЏРІР»СЏСЋС‰РёС…СЃСЏ РЅРµРґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё, РІ СЃР»РµРґСѓСЋС‰РёС… СЃР»СѓС‡Р°СЏС…: РћРїРµСЂР°С†РёСЏ СЃРѕРІРµСЂС€РµРЅР° СЃ РЅР°СЂСѓС€РµРЅРёРµРј Рљ
90: id=5.2.10.2, type=operative, mat=evaluable, obj=РЎСѓРјРјС‹, РѕС€РёР±РѕС‡РЅРѕ РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ РЅР° СЃС‡РµС‚ Р—Р°РєР°Р·С‡РёРєР°.
91: id=5.2.10.3, type=operative, mat=evaluable, obj=РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚Р° РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рµ С‚СЂР°РЅР·Р°РєС†РёРё.
92: id=5.2.10.4, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ СѓРґРµСЂР¶РёРІР°РµС‚ РёР· РѕР±С‰РёС… СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РЅР° РЎС‡РµС‚ Р—Р°РєР°Р·С‡РёРєР° СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, РєРѕС‚Рѕ
93: id=5.2.10.5, type=operative, mat=evaluable, obj=Р‘Р°РЅРє СѓРґРµСЂР¶РёРІР°РµС‚ РёР· РѕР±С‰РёС… СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РЅР° РЎС‡РµС‚ Р—Р°РєР°Р·С‡РёРєР° СЃСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Рё РёРЅС‹С… СѓР±С‹С‚РєРѕ
94: id=5.3, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РѕР±СЏР·СѓРµС‚СЃСЏ:
95: id=5.3.1, type=operative, mat=evaluable, obj=РџСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё РїРѕ РґРѕРєСѓРјРµРЅС‚Сѓ Рѕ РїСЂРёРµРјРєРµ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі.
96: id=5.3.2, type=operative, mat=evaluable, obj=РћРїР»Р°С‚РёС‚СЊ СЃС‚РѕРёРјРѕСЃС‚СЊ СѓСЃР»СѓРі, РѕРєР°Р·Р°РЅРЅС‹С… Р�СЃРїРѕР»РЅРёС‚РµР»РµРј, СЃРѕРіР»Р°СЃРЅРѕ СѓСЃР»РѕРІРёСЏРј РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°.
97: id=5.3.3, type=operative, mat=evaluable, obj=РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєРѕРЅС‚СЂРѕР»СЊ Р·Р° С…РѕРґРѕРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі Р�СЃРїРѕР»РЅРёС‚РµР»РµРј.
98: id=5.3.4, type=operative, mat=evaluable, obj=РџСЂРёРЅСЏС‚СЊ СЂРµС€РµРЅРёРµ РѕР± РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РѕС‚РєР°Р·Рµ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РІ С…РѕРґРµ РёСЃРї
99: id=5.3.5, type=operative, mat=evaluable, obj=РўСЂРµР±РѕРІР°С‚СЊ СѓРїР»Р°С‚С‹ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№) РІ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, 
100: id=5.3.6, type=operative, mat=evaluable, obj=РЈРјРµРЅСЊС€РёС‚СЊ СЃСѓРјРјСѓ, РїРѕРґР»РµР¶Р°С‰СѓСЋ СѓРїР»Р°С‚Рµ Р—Р°РєР°Р·С‡РёРєРѕРј СЋСЂРёРґРёС‡РµСЃРєРѕРјСѓ Р»РёС†Сѓ РёР»Рё С„РёР·РёС‡РµСЃРєРѕРјСѓ Р»РёС†Сѓ, РІ С‚РѕРј С‡РёСЃР»Рµ Р·Р°
101: id=5.3.7, type=operative, mat=evaluable, obj=Р Р°Р·РјРµС‰Р°С‚СЊ РЅР° РІРёРґРЅС‹С… РјРµСЃС‚Р°С… РўРЎРў, РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµРјС‹Рµ РёСЃРїРѕР»РЅРёС‚РµР»РµРј СЂРµРєР»Р°РјРЅРѕ-РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, РёР·РІРµ
102: id=5.3.8, type=operative, mat=evaluable, obj=РќРµ СЂР°Р·Р±РёРІР°С‚СЊ СЃСѓРјРјСѓ РѕРґРЅРѕР№ РѕРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹ РЅР° РЅРµСЃРєРѕР»СЊРєРѕ СЃСѓРјРј Рё РЅРµ РїСЂРѕРІРѕРґРёС‚СЊ РѕС‚РґРµР»СЊРЅС‹Рµ РѕРїРµСЂР°С†РёРё РЅР° РєР°Р¶Рґ
103: id=5.3.9, type=operative, mat=evaluable, obj=РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РєР°СЂС‚С‹, РєРѕС‚РѕСЂС‹Рµ СЃС‚Р°Р»Рё РґРѕСЃС‚СѓРїРЅС‹ Р·Р°РєР°Р·С‡РёРєСѓ/РўРЎРў, РґР»СЏ РёРЅС‹С… С†РµР»РµР№, РєСЂРѕРјРµ РєР°Рє РїСЂРѕ
104: id=5.3.10, type=operative, mat=evaluable, obj=РџСЂРѕРІРѕРґРёС‚СЊ РѕРїРµСЂР°С†РёРё Рё РѕС„РѕСЂРјР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІ С‚РѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅС‹С… С‚РѕС‡РєР°С… Рє РєРѕРЅС‚СЂР°РєС‚Сѓ Рё РЅРµСЃС‚Рё
105: id=5.3.11, type=operative, mat=evaluable, obj=РҐСЂР°РЅРёС‚СЊ РІ РЅРµРґРѕСЃС‚СѓРїРЅРѕРј РґР»СЏ С‚СЂРµС‚СЊРёС… Р»РёС† РјРµСЃС‚Рµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј (С‡РµРєРё, РєР°СЃСЃРѕРІС‹Рµ С‡РµРєРё, СЂР°СЃРїРѕСЂСЏР¶РµРЅРё
106: id=5.3.12, type=operative, mat=evaluable, obj=РџРµСЂРµРґР°РІР°С‚СЊ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РїРѕ РµРіРѕ Р·Р°РїСЂРѕСЃСѓ РІ С‚РµС‡РµРЅРёРµ С‚СЂРµС… СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ Р·Р°РїСЂРѕСЃР° РѕС‚ РёСЃРїРѕР»РЅ
107: id=5.3.13, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё, РІРЅРµСЃРµРЅРёСЏ РёР·РјРµРЅРµРЅРёР№ Рё РґРѕРїРѕР»РЅРµРЅРёР№ РІ РґРѕРєСѓРјРµРЅС‚С‹, РїСЂРµРґСЃС‚Р°РІР»РµРЅРЅС‹Рµ Р·Р°РєР°Р·С‡РёРєРѕРј РїСЂРё Р·
108: id=5.3.14, type=operative, mat=evaluable, obj=РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РґРѕСЃС‚РѕРІРµСЂРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ Рё СЃРІРµРґРµРЅРёСЏ, РЅРµРѕР±С…РѕРґРёРјС‹Рµ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РґР»СЏ РёСЃРїРѕР»РЅРµРЅРёСЏ С‚
109: id=5.3.15, type=operative, mat=evaluable, obj=РџРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ Р·Р°РїСЂРѕСЃСѓ РёСЃРїРѕР»РЅРёС‚РµР»СЏ Р·Р°РєР°Р·С‡РёРє РѕР±СЏР·СѓРµС‚СЃСЏ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РїРµСЂРµРґ
110: id=5.3.16, type=operative, mat=evaluable, obj=РЎ РґР°С‚С‹ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРёРµРј Рє РѕРїР»Р°С‚Рµ РєР°СЂС‚, СЃРЅСЏС‚СЊ СЂРµРєР»Р°РјРЅРѕ-РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹
111: id=5.3.17, type=operative, mat=evaluable, obj=РќРµ РїСЂРёРЅРёРјР°С‚СЊ РјРµСЂ РїСЂРѕС‚РёРІРѕРґРµР№СЃС‚РІРёСЏ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РІ РїСЂРѕРІРµРґРµРЅРёРµ РїСЂРѕРІРµСЂРєРё Р·Р°РєР°Р·С‡РёРєР°/РўРЎРў РЅР° РїСЂРµРґРјРµС‚ РІС‹СЏРІР»РµРЅРё
112: id=5.3.18, type=operative, mat=evaluable, obj=РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РѕРїРµСЂР°С†РёР№ Сѓ Р·Р°РєР°Р·С‡РёРєР° РІ РўРЎРў (С‚РѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі):
113: id=5.3.18.1, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ (РІ С‚РѕРј С‡РёСЃР»Рµ С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРёРµ sim-РєР°СЂС‚С‹)/СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Рё РїСЂРѕРіСЂР°Рј
114: id=5.3.18.2, type=operative, mat=evaluable, obj=РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РґРѕСЃС‚СѓРї Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ СЂР°Р±РѕС‚ РїРѕ Рµ
115: id=5.3.18.3, type=operative, mat=evaluable, obj=РџСЂРёРЅСЏС‚СЊ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ РїРѕ Р°РєС‚Сѓ РїСЂРёРЅСЏС‚РёСЏ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, СЃРѕСЃС‚Р°РІР»РµРЅРЅРѕРјСѓ РІ РґРІСѓС… СЌРєР·РµРјРїР»СЏСЂР°С… Рё Рї
116: id=5.3.20.4, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° РёР· СЃС‚СЂРѕСЏ РёР»Рё РµРіРѕ СѓС‚СЂР°С‚С‹ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ РѕР± СЌС‚РѕРј РёСЃРїРѕ
117: id=5.3.18.5, type=operative, mat=evaluable, obj=Р’РµСЂРЅСѓС‚СЊ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РёР»Рё РѕР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РІ С‚РµС‡РµРЅРёРµ РїСЏС‚Рё 
118: id=5.3.19, type=operative, mat=evaluable, obj=Р’РѕР·РјРµСЃС‚РёС‚СЊ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РІ РїРѕР»РЅРѕРј РѕР±СЉРµРјРµ Рё РІ Р±РµР·СѓСЃР»РѕРІРЅРѕРј РїРѕСЂСЏРґРєРµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РІ СЂР°Р·РјРµСЂРµ: вЂў СЃСЂРµРґСЃС‚
119: id=5.3.20, type=operative, mat=evaluable, obj=Р’ СЂР°РјРєР°С… РЅР°СЃС‚РѕСЏС‰РµРіРѕ РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РїРµСЂРµРґР°РµС‚ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ (РґР°Р»РµРµ вЂ“ РџР”РЅ) СЂСѓРєРѕРІРѕ
120: id=5.4, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ:
121: id=5.4.1, type=operative, mat=evaluable, obj=РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РєРѕРЅС‚СЂР°РєС‚РѕРј, РЅР°РґР»РµР¶Р°С‰РёРј РѕР±СЂР°Р·РѕРј РІ СЃ
122: id=5.4.2, type=operative, mat=evaluable, obj=РћС‚РєР°Р·Р°С‚СЊ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РІ РїСЂРёРµРјРєРµ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РІ СЃР»СѓС‡Р°Рµ РёС… РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР°.
123: id=5.4.3, type=operative, mat=evaluable, obj=РџСЂРёРЅСЏС‚СЊ СЂРµС€РµРЅРёРµ РѕР± РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РѕС‚РєР°Р·Рµ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ РѕСЃРЅРѕРІР°РЅРёСЏРј, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹Рј Р¤РµРґРµСЂ
124: id=5.4.4, type=operative, mat=evaluable, obj=РћС‚РєР°Р·Р°С‚СЊСЃСЏ РѕС‚ РѕРїР»Р°С‚С‹ СѓСЃР»СѓРі РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР°, Р° РµСЃР»Рё СѓСЃР»СѓРіРё РѕРїР»Р°С‡РµРЅС‹, РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° СѓРїР»Р°
125: id=5.4.5, type=operative, mat=evaluable, obj=РЎСЃС‹Р»Р°С‚СЊСЃСЏ РЅР° РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РєР°СЂС‚ РІ СЃРѕР±СЃС‚РІРµРЅРЅС‹С… СЂРµРєР»Р°РјРЅС‹С… РјР°С‚РµСЂРёР°Р»
126: id=5.5, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РѕР±СЏР·СѓРµС‚СЃСЏ РїРµСЂРµРґР°РІР°С‚СЊ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РїРѕ РµРіРѕ Р·Р°РїСЂРѕСЃСѓ РІ С‚РµС‡РµРЅРёРµ 3 (С‚СЂРµС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»Сѓ
127: id=5.6, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РѕР±СЏР·СѓРµС‚СЃСЏ РІ СЃР»СѓС‡Р°Рµ СѓС‚РµСЂРё РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј: Р’РµСЂРЅСѓС‚СЊ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РёР»Рё РћР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРј
128: id=5.7, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РЅРµРІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ Р—Р°РєР°Р·С‡РёРє РѕР±СЏР·Р°РЅ СѓРїР»Р°С‚РёС‚СЊ Р�СЃРї
129: id=5.9, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ РїРѕР»СѓС‡Р°С‚СЊ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЋ Сѓ РёСЃРїРѕР»РЅРёС‚РµР»СЏ РїРѕ РІРѕРїСЂРѕСЃР°Рј СЌРєСЃРїР»СѓР°С‚Р°С†РёРё СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ 
130: id=5.10, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РѕР±СЏР·СѓРµС‚СЃСЏ РѕР±РµСЃРїРµС‡РёС‚СЊ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РїСЂРѕС…РѕР¶РґРµРЅРёРµ РІСЃРµРјРё СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРё
131: id=6, type=operative, mat=evaluable, obj=РђРќРўР�РљРћР Р РЈРџР¦Р�РћРќРќРђРЇ РћР“РћР’РћР РљРђ
132: id=6.1, type=operative, mat=evaluable, obj=РџСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё, РёСЃРїРѕР»РЅРµРЅРёРё, РёР·РјРµРЅРµРЅРёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РљРѕРЅС‚СЂР°РєС‚Р° РЎС‚РѕСЂРѕРЅС‹ РїСЂРёРЅРёРјР°СЋС‚ РЅР° СЃРµР±СЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ
133: id=7, type=operative, mat=evaluable, obj=РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќ
134: id=7.1, type=operative, mat=evaluable, obj=Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ 
135: id=7.2, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»
136: id=7.3, type=operative, mat=evaluable, obj=РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚
137: id=7.4, type=operative, mat=evaluable, obj=РЁС‚СЂР°С„С‹ РЅР°С‡РёСЃР»СЏСЋС‚СЃСЏ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·
138: id=7.4.1, type=operative, mat=evaluable, obj=Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р·Р° 
139: id=7.5, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ (РІ С‚РѕРј С‡РёСЃР»Рµ РіР°СЂР°РЅС‚РёР№РЅРѕРіРѕ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°), РїСЂ
140: id=7.6, type=operative, mat=evaluable, obj=РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕ
141: id=7.7, type=operative, mat=evaluable, obj=РЁС‚СЂР°С„С‹ РЅР°С‡РёСЃР»СЏСЋС‚СЃСЏ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂ
142: id=7.7.1, type=operative, mat=evaluable, obj=Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, 
143: id=7.7.2, type=operative, mat=evaluable, obj=Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РєР°Рє РїРѕР±РµРґРёС‚РµР»СЏ Р·Р°РєСѓРїРєРё (РёР»Рё РёРЅРѕРіРѕ СѓС‡Р°СЃС‚РЅРёРєР° Р·Р°РєСѓРїРєРё РІ СЃР»СѓС‡Р°СЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅ
144: id=10, type=operative, mat=evaluable, obj=РїСЂРѕС†РµРЅС‚РѕРІ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
145: id=5, type=operative, mat=evaluable, obj=РїСЂРѕС†РµРЅС‚РѕРІ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ Рґ
146: id=1, type=operative, mat=evaluable, obj=РїСЂРѕС†РµРЅС‚ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ
147: id=10, type=operative, mat=evaluable, obj=РїСЂРѕС†РµРЅС‚РѕРІ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
148: id=5, type=operative, mat=evaluable, obj=РїСЂРѕС†РµРЅС‚РѕРІ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚
149: id=1, type=operative, mat=evaluable, obj=РїСЂРѕС†РµРЅС‚ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚
150: id=7.7.3, type=operative, mat=evaluable, obj=Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°,
151: id=7.8, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РѕР±РјРµРЅР° РґРѕРєСѓРјРµРЅС‚Р°РјРё РїСЂРё РїСЂРёРјРµРЅРµРЅРёРё РјРµСЂ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Рё СЃРѕРІРµСЂС€РµРЅРёРё РёРЅС‹С… РґРµР№СЃС‚РІРёР№ РІ СЃРІСЏР·Рё СЃ 
152: id=7.9, type=operative, mat=evaluable, obj=РџСЂРёРјРµРЅРµРЅРёРµ РЅРµСѓСЃС‚РѕР№РєРё (С€С‚СЂР°С„Р°, РїРµРЅРё) РЅРµ РѕСЃРІРѕР±РѕР¶РґР°РµС‚ РЎС‚РѕСЂРѕРЅС‹ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РљРѕРЅС‚СЂР°РєС‚Сѓ.
153: id=7.10, type=operative, mat=evaluable, obj=РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚
154: id=7.11, type=operative, mat=evaluable, obj=РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… 
155: id=7.12, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РІ СЃРІСЏР·Рё СЃ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРёРј РѕС‚РєР°Р·РѕРј РЎС‚РѕСЂРѕРЅС‹ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РґСЂСѓРіР°
156: id=8, type=operative, mat=evaluable, obj=РљРђР§Р•РЎРўР’Рћ РћРљРђР—РђРќРќР«РҐ РЈРЎР›РЈР“, РџРћР РЇР”РћРљ Р�РҐ РџР Р�Р•РњРљР�. Р“РђР РђРќРўР�РЇ РљРђР§Р•РЎРўР’Рђ РЈРЎР›РЈР“
157: id=8.1, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ Р—Р°РєР°Р·С‡РёРєСѓ РєР°С‡РµСЃС‚РІРѕ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РџСЂРёР»РѕР¶РµРЅРёСЏ 
158: id=8.2, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РїРѕРІСЂРµР¶РґРµРЅРёСЏ, РІРѕР·РЅРёРєС€РёРµ РІСЃР»РµРґСЃС‚РІРёРµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РµРіРѕ СЃРїРµС†РёР°Р»РёСЃС‚
159: id=8.3, type=operative, mat=evaluable, obj=РџСЂРёРµРјРєР° СЂРµР·СѓР»СЊС‚Р°С‚Р° РёСЃРїРѕР»РЅРµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Рѕ
160: id=8.3.1, type=operative, mat=evaluable, obj=Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј, С„РѕСЂРјРёСЂ
161: id=8.3.2, type=operative, mat=evaluable, obj=Рљ РґРѕРєСѓРјРµРЅС‚Сѓ Рѕ РїСЂРёРµРјРєРµ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРјСѓ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р°, Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РїСЂРёР»Р°РіР°РµС‚ РґРѕРєСѓРјРµРЅС‚С‹, Рї
162: id=8.4, type=operative, mat=evaluable, obj=Р”Р°С‚РѕР№ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј, СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРё
163: id=8.5, type=operative, mat=evaluable, obj=РџСЂРёРµРјРєР° СѓСЃР»СѓРі РѕС‚ РёРјРµРЅРё Р—Р°РєР°Р·С‡РёРєР° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј, (Р»РёР±Рѕ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ вЂ“ Рї. 
164: id=8.5.1, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РІ СЃСЂРѕРє РЅРµ Р±РѕР»РµРµ 10 (РґРµСЃСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃРѕ РґРЅСЏ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚
165: id=8.5.2, type=operative, mat=evaluable, obj=РџРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ СѓРІРµРґРѕРјР»РµРЅРёСЋ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј Р—Р°РєР°Р·С‡РёРєР°, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РјРѕР¶РµС‚ РїСЂРѕРёР·РІРѕРґРёС‚СЊСЃСЏ С‚РѕР»СЊРє
166: id=8.5.3, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РїРѕСЃС‚СѓРїРёР»Рѕ СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Р№ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРє, РїСЂРёРµРјРєР° Рѕ
167: id=8.5.4, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РЅРµ РїРѕСЃС‚СѓРїРёР»Рѕ, Р»РёР±Рѕ РїРѕСЃС‚СѓРїРёР»Рѕ РІ Р±РѕР»РµРµ РїРѕР·РґРЅРёР№ СЃСЂРѕРє, С‡
168: id=8.5.5, type=operative, mat=evaluable, obj=Р”Р»СЏ РїСЂРѕРІРµСЂРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РІ С‡Р°СЃС‚Рё РёС… СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р°
169: id=8.5.6, type=operative, mat=evaluable, obj=Р­РєСЃРїРµСЂС‚РёР·Р° СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РјРѕР¶РµС‚ РїСЂРѕРІРѕРґРёС‚СЊСЃСЏ Р—Р°РєР°Р·С‡РёРєРѕРј СЃРІРѕРёРјРё СЃРёР»Р°РјРё РёР»Рё Рє
170: id=8.5.7, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р·Р°РјРµС‡Р°РЅРёР№ Р—Р°РєР°Р·С‡РёРє (СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅРѕРµ Р»РёС†Рѕ) РІ С‚РµС‡РµРЅРёРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹, СЃ
171: id=8.5.8, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј Р±СѓРґСѓС‚ СѓСЃС‚Р°РЅРѕРІР»РµРЅС‹ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ С‚СЂРµР±РѕРІР°РЅРёСЏРј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ РљРѕРЅС‚СЂР°
172: id=8.5.9, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РїРѕР»СѓС‡РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.5.8. РљРѕРЅС‚СЂР°РєС‚Р° РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРіРѕ РѕС‚РєР°Р·Р° РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РґРѕ
173: id=8.6, type=operative, mat=evaluable, obj=Р”Р°С‚РѕР№ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РґРѕРєСѓРјРµРЅС‚Р° Рѕ 
174: id=8.7, type=operative, mat=evaluable, obj=Р’РЅРµСЃРµРЅРёРµ РёСЃРїСЂР°РІР»РµРЅРёР№ РІ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ, РѕС„РѕСЂРјР»РµРЅРЅС‹Р№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°СЃС‚РѕСЏС‰РёРј СЂР°Р·РґРµР»РѕРј РљРѕРЅС‚СЂР°РєС‚Р°
175: id=8.8, type=operative, mat=evaluable, obj=РћС„РѕСЂРјР»РµРЅРёРµ СЂРµР·СѓР»СЊС‚Р°С‚Р° РїСЂРѕРІРµРґРµРЅРёСЏ РїСЂРѕС†РµРґСѓСЂС‹ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ Рё РІ СЃСЂРѕРє
176: id=8.9, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ РЅРµ РѕС‚РєР°Р·С‹РІР°С‚СЊ 
177: id=8.10, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР° Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·Р°РЅ Р±РµР·РІРѕР·РјРµР·РґРЅРѕ СѓСЃС‚СЂР°РЅРёС‚СЊ РЅРµРґРѕСЃС‚Р°С‚РєРё 
178: id=8.11, type=operative, mat=evaluable, obj=РџРѕРґРїРёСЃР°РЅРЅС‹Р№ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё Р—Р°РєР°Р·С‡РёРєР° Рё Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃ
179: id=9, type=operative, mat=evaluable, obj=Р”Р•Р™РЎРўР’Р�Р• РћР‘РЎРўРћРЇРўР•Р›Р¬РЎРўР’ РќР•РџР Р•РћР”РћР›Р�РњРћР™ РЎР�Р›Р«
180: id=9.1, type=operative, mat=evaluable, obj=РЎС‚РѕСЂРѕРЅС‹ РѕСЃРІРѕР±РѕР¶РґР°СЋС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° С‡Р°СЃС‚РёС‡РЅРѕРµ РёР»Рё РїРѕР»РЅРѕРµ РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СЃРІРѕРёС… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ 
181: id=9.2, type=operative, mat=evaluable, obj=РџСЂРё РІРѕР·РЅРёРєРЅРѕРІРµРЅРёРё РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РёС… РёСЃРїРѕР»РЅРµРЅРёСЋ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ РЅР°СЃС‚РѕСЏ
182: id=9.3, type=operative, mat=evaluable, obj=РџСЂРё СЂР°СЃСЃРјРѕС‚СЂРµРЅРёРё СЃРїРѕСЂРѕРІ РІ СЃРІСЏР·Рё СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РЅРµРїСЂРµРѕРґРѕР»РёРјРѕР№ СЃРёР»С‹ СЃС‚РѕСЂРѕРЅР°, СЃСЃС‹Р»Р°СЋС‰Р°СЏСЃСЏ РЅР° СЌС‚Рё РѕР±
183: id=10, type=operative, mat=evaluable, obj=РџРћР РЇР”РћРљ Р РђР—Р Р•РЁР•РќР�РЇ РЎРџРћР РћР’
184: id=10.1, type=operative, mat=evaluable, obj=Р’СЃРµ СЃРїРѕСЂС‹ РёР»Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ, РІРѕР·РЅРёРєР°СЋС‰РёРµ РјРµР¶РґСѓ РЎС‚РѕСЂРѕРЅР°РјРё РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РёР»Рё РІ СЃРІСЏР·Рё СЃ РЅРёРј, СЂР°
185: id=10.2, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СЂР°Р·СЂРµС€РµРЅРёСЏ СЂР°Р·РЅРѕРіР»Р°СЃРёР№ РїСѓС‚РµРј РїРµСЂРµРіРѕРІРѕСЂРѕРІ РѕРЅРё РїРѕРґР»РµР¶Р°С‚ СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЋ РІ РђСЂР±РёС‚СЂР°Р¶
186: id=11, type=operative, mat=evaluable, obj=РЎР РћРљ Р”Р•Р™РЎРўР’Р�РЇ, РџРћР РЇР”РћРљ Р�Р—РњР•РќР•РќР�РЇР�Р РђРЎРўРћР Р–Р•РќР�РЇ РљРћРќРўР РђРљРўРђ
187: id=11.1, type=operative, mat=evaluable, obj=РќР°СЃС‚РѕСЏС‰РёР№ РєРѕРЅС‚СЂР°РєС‚ РґРµР№СЃС‚РІСѓРµС‚ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ РїРѕ 30 РґРµРєР°Р±СЂСЏ 2025 РіРѕРґР°, РёР»Рё РґРѕ РјРѕРјРµРЅС‚Р° РёСЃС‡РµСЂРїР°РЅРёСЏ РїСЂ
188: id=11.2, type=operative, mat=evaluable, obj=Р›СЋР±С‹Рµ РёР·РјРµРЅРµРЅРёСЏ Рё РґРѕРїРѕР»РЅРµРЅРёСЏ Рє РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РёРјРµСЋС‚ СЃРёР»Сѓ С‚РѕР»СЊРєРѕ РІ С‚РѕРј СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РѕРЅРё РѕС„РѕСЂРјР»Рµ
189: id=11.3, type=operative, mat=evaluable, obj=Р Р°СЃС‚РѕСЂР¶РµРЅРёРµ РєРѕРЅС‚СЂР°РєС‚Р° РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РїРѕ СЃРѕРіР»Р°С€РµРЅРёСЋ РЎС‚РѕСЂРѕРЅ, РїРѕ СЂРµС€РµРЅРёСЋ СЃСѓРґР°, РІ СЃР»СѓС‡Р°Рµ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРіРѕ РѕС‚Рє
190: id=11.4, type=operative, mat=evaluable, obj=Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ РїСЂРёРЅСЏС‚СЊ СЂРµС€РµРЅРёРµ РѕР± РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РѕС‚РєР°Р·Рµ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ РѕСЃРЅРѕРІР°РЅРёСЏРј, РїСЂРµРґСѓ
191: id=11.5, type=operative, mat=evaluable, obj=Р РµС€РµРЅРёРµ РЎС‚РѕСЂРѕРЅ РѕР± РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РѕС‚РєР°Р·Рµ РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ РѕСЃРЅРѕРІР°РЅРёСЏРј, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹Рј Р“Рљ Р Р¤ 
192: id=11.6, type=operative, mat=evaluable, obj=Р�Р·РјРµРЅРµРЅРёРµ Рё(РёР»Рё) СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РєРѕРЅС‚СЂР°РєС‚Р° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ, СЃСЂРѕРєРё, СЃР»СѓС‡Р°СЏС… Рё РЅР° СѓСЃР»РѕРІРёСЏС…, СѓСЃС‚Р°РЅ
193: id=11.7, type=operative, mat=evaluable, obj=Р’Рѕ РІСЃРµРј, С‡С‚Рѕ РЅРµ РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РЅР°СЃС‚РѕСЏС‰РёРј РєРѕРЅС‚СЂР°РєС‚РѕРј, РЎС‚РѕСЂРѕРЅС‹ СЂСѓРєРѕРІРѕРґСЃС‚РІСѓСЋС‚СЃСЏ РґРµР№СЃС‚РІСѓСЋС‰РёРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊ
194: id=11.8, type=operative, mat=evaluable, obj=РЎС‚РѕСЂРѕРЅС‹ РїСЂРµРґСѓСЃРјРѕС‚СЂРµР»Рё, С‡С‚Рѕ РёР·РјРµРЅРµРЅРёРµ СЃСѓС‰РµСЃС‚РІРµРЅРЅС‹С… СѓСЃР»РѕРІРёР№ РєРѕРЅС‚СЂР°РєС‚Р° РїСЂРё РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёРё РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃ
195: id=12, type=operative, mat=evaluable, obj=РџР РћР§Р�Р• РЈРЎР›РћР’Р�РЇ
196: id=12.1, type=operative, mat=evaluable, obj=РџСЂРё РёСЃРїРѕР»РЅРµРЅРёРё РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РїРµСЂРµРјРµРЅР° Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј СЃР»СѓС‡Р°СЏ, РєРѕРіРґ
197: id=12.2, type=operative, mat=evaluable, obj=Р’ СЃР»СѓС‡Р°Рµ РїРµСЂРµРјРµРЅС‹ Р—Р°РєР°Р·С‡РёРєР° РїРѕ РєРѕРЅС‚СЂР°РєС‚Сѓ РїСЂР°РІР° Рё РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё Р—Р°РєР°Р·С‡РёРєР° РїРѕ РЅР°СЃС‚РѕСЏС‰РµРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ РїРµСЂРµС…
198: id=12.3, type=operative, mat=evaluable, obj=РџСЂРё РёСЃРїРѕР»РЅРµРЅРёРё РєРѕРЅС‚СЂР°РєС‚Р° РїРѕ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЋ Р—Р°РєР°Р·С‡РёРєР° СЃ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РѕРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРіРё, РєР°С‡РµСЃ
199: id=12.4, type=operative, mat=evaluable, obj=РљРѕРЅС‚СЂР°РєС‚ СЃРѕСЃС‚Р°РІР»РµРЅ РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ С„РѕСЂРјРµ Рё РїРѕРґРїРёСЃР°РЅ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ РЎ
200: id=12.5, type=operative, mat=evaluable, obj=РџСЂРёР»РѕР¶РµРЅРёСЏ: в„– 1 В«РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµВ» в„– 2 В«РЎРїРµС†РёС„РёРєР°С†РёСЏВ»
201: id=13, type=operative, mat=evaluable, obj=РњР•РЎРўРђ РќРђРҐРћР–Р”Р•РќР�РЇ, Р‘РђРќРљРћР’РЎРљР�Р• Р Р•РљР’Р�Р—Р�РўР«РЎРўРћР РћРќ Р—РђРљРђР—Р§Р�Рљ Р¤РµРґРµСЂР°Р»СЊРЅРѕРµ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕРµ Р±СЋРґР¶РµС‚РЅРѕРµ СѓС‡СЂРµР¶РґРµРЅ
202: id=354340, type=operative, mat=evaluable, obj=, Рі. РЎРѕС‡Рё, РђРґР»РµСЂСЃРєРёР№ СЂР°Р№РѕРЅ СѓР». РљР°СЂР»Р° РњР°СЂРєСЃР°, Рґ.8 Р�РќРќ 2317026788 РљРџРџ231701001 РћР“Р Рќ: 1022302723409 СЂ\СЃ
203: id=1, type=operative, mat=evaluable, obj=РћР±СЉРµРєС‚РѕРј Р·Р°РєСѓРїРєРё СЏРІР»СЏРµС‚СЃСЏ: РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РїРѕ РїСЂРёРµРјСѓ Рє РѕРїР»Р°С‚Рµ РїР»Р°С‚РµР¶РЅС‹С… (Р±Р°РЅРєРѕРІСЃРєРёС…) РєР°СЂС‚ РІ РєР°С‡РµСЃС‚РІРµ 
204: id=2, type=operative, mat=evaluable, obj=РњРµСЃС‚РѕРїРѕР»РѕР¶РµРЅРёРµ С‚РѕС‡РµРє РїСЂРёРµРјР° Р—Р°РєР°Р·С‡РёРєР° СѓСЃС‚Р°РЅРѕРІРєРё СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі, Р° С‚Р°РєР¶Рµ РєРѕР»
205: id=3, type=operative, mat=evaluable, obj=РџРµСЂРµС‡РµРЅСЊ РєР°СЂС‚, РєРѕС‚РѕСЂС‹Рµ СЃРµСЂРІРёСЃРЅР°СЏ С‚РѕС‡РєР° РїСЂРёРЅРёРјР°РµС‚ РІ РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі: в„–Рї/Рї РќР°РёРјРµРЅРѕРІР°РЅРёРµ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹
206: id=4, type=operative, mat=evaluable, obj=РЎСЂРѕРєРё РѕРєР°Р·Р°РЅРёСЏ РЈСЃР»СѓРі: РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃ В«01В» РјР°СЂС‚Р° 2025 РіРѕРґР° РїРѕ В«30В» РЅРѕСЏР±СЂСЏ 2025 РіРѕРґР° 
207: id=5, type=operative, mat=evaluable, obj=РЈСЃР»РѕРІРёСЏ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі: РљРѕРјРёСЃСЃРёСЏ Р·Р° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ- РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚. РђР±РѕРЅРµРЅС‚СЃРєР°СЏ РїР»Р°С‚Р° Р·Р° РїРѕР»
208: id=9.2.1, type=operative, mat=evaluable, obj=РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРІРїР°РґРµРЅРёСЏ РёС‚РѕРіРѕРІ РёР»Рё С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃР±РѕСЏ СЂР°Р±РѕС‚РЅРёРє РўРЎРў: a) СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµС‚ РљРѕРЅС‚СЂРѕР»СЊРЅСѓСЋ Р»РµРЅС‚Сѓ;
209: id=1, type=operative, mat=evaluable, obj=РЎР’Р•Р”Р•РќР�РЇ Рћ РџР Р•Р”РџР Р�РЇРўР�Р� РќР°РёРјРµРЅРѕРІР°РЅРёРµ: ______________________________ (СѓРєР°Р·С‹РІР°РµС‚СЃСЏ РїРѕР»РЅРѕРµ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ
210: id=2, type=operative, mat=evaluable, obj=Р�РќР¤РћР РњРђР¦Р�РЇ РћР‘ РЈРЎР›РЈР“РђРҐ ВЁ РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі + Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» + QR-РєРѕРґ ВЁ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі + Sb
211: id=3, type=operative, mat=evaluable, obj=РџРћР”РўР’Р•Р Р–Р”Р•РќР�Р• Р—РђРљР›Р®Р§Р•РќР�РЇ РљРћРќРўР РђРљРўРђ
212: id=1.1, type=operative, mat=evaluable, obj=РџРѕРґС‚РІРµСЂР¶РґР°РµС‚, С‡С‚Рѕ РІСЃСЏ РёРЅС„РѕСЂРјР°С†РёСЏ, СѓРєР°Р·Р°РЅРЅР°СЏ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р—Р°СЏРІР»РµРЅРёРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРѕРєСѓ
213: id=1.2, type=operative, mat=evaluable, obj=РЎРѕРіР»Р°СЃРЅРѕ, С‡С‚Рѕ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃРІРµРґРµРЅРёСЏ, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р—Р°СЏРІР»РµРЅРёРё Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹С…
214: id=1.3, type=operative, mat=evaluable, obj=РџСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ СЃРѕРіР»Р°СЃРёРµ (Р·Р°СЂР°РЅРµРµ РґР°РЅРЅС‹Р№ Р°РєС†РµРїС‚) РЅР° СЃРїРёСЃР°РЅРёРµ СЃРѕ СЃС‡РµС‚Р°, СѓРєР°Р·Р°РЅРЅРѕРіРѕ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р—Р°
215: id=4, type=operative, mat=evaluable, obj=РћРўРњР•РўРљР� Р‘РђРќРљРђ _______________________ ______________________________________ _______________________
216: id=10, type=operative, mat=evaluable, obj=000 РўРµР»РµС„РѕРЅ РґР»СЏ РѕС‚СЂР°Р¶РµРЅРёСЏ РІ С‡РµРєРµ РЅРµС‚ РљРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂР° (РІ С‚РѕРј С‡РёСЃР»Рµ РґР»СЏ РЅР°РїСЂР°РІР»РµРЅРёСЏ Рї
217: id=1, type=operative, mat=evaluable, obj=900 000,00 РњР°РєСЃРёРјР°Р»СЊРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, СЂСѓР±.
218: id=1, type=operative, mat=evaluable, obj=900 000,00 Р—Р°РєР°Р·С‡РёРє: Р¤Р“Р‘РЈ В«РљР°РІРєР°Р·СЃРєРёР№ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅС‹Р№ Р·Р°РїРѕРІРµРґРЅРёРєВ» РћС‚ В«Р‘Р°РЅРєР°/Р�СЃРїРѕР»РЅРёС‚РµР»СЏВ»:

Total contract entries: 219

[Command succeeded with exit code 0]

