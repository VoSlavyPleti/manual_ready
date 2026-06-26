## Summarized at 2026-06-26T11:26:36.256910+00:00

Human: QA validate final discrepancy JSON
AI: I'll start by reading the skill file and the reference documents to understand the validation requirements.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_fekN3xNSC0b7IQleaAdl5314', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/output-contract.md'}, 'id': 'call_01_tR5PdhMJs5HBt94Y9vQD7041', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/outputs/**'}, 'id': 'call_02_j4q1Wp280jAo6XWKtwGE9797', 'type': 'tool_call'}]
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
Tool: ['/skills/acquiring-discrepancy-analysis/references/output-contract.md']
Tool: ['/.venv/Lib/site-packages/langchain_core/outputs/__init__.py', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/llm_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/run_info.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/chat_generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/chat_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/llm_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/run_info.py', '/outputs/discrepancy_analysis.json', '/outputs/discrepancy_analysis.xlsx', '/outputs/working/build_discrepancy_analysis.py', '/outputs/working/build_full_matching.py', '/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/enrich_legal_propositions.py', '/outputs/working/generate_xlsx.py', '/outputs/working/legal_propositions.json', '/outputs/working/qa_check.py', '/outputs/working/working_artifact_validation.json']
AI: Good. Now let me read the output contract reference and the final JSON artifact, plus the working artifacts needed for validation.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 1000}, 'id': 'call_00_Et94vk0MsiguXUW6YUwc0611', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'limit': 200}, 'id': 'call_01_x1VDoDrMtLaJcH9UVXK55851', 'type': 'tool_call'}]
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
Tool:      1	{
     2	  "analysis_profile": {
     3	    "contract_product_profile": {
     4	      "product": [
     5	        "trade_acquiring"
     6	      ],
     7	      "lot": "44_fz",
     8	      "terminal": [
     9	        "electronic_terminal"
    10	      ],
    11	      "payment_method": [
    12	        "cards",
    13	        "nfc",
    14	        "qr"
    15	      ],
    16	      "legal_regime": "44_fz"
    17	    },
    18	    "source_preflight": {
    19	      "contract_numbering_valid": true,
    20	      "notes": [
    21	        "Контракт 44-ФЗ с полной нумерацией пунктов. Приложения №1 и №1.1 включены."
    22	      ]
    23	    }
    24	  },
    25	  "links": [
    26	    {
    27	      "matrix_ids": [
    28	        "2.1"
    29	      ],
    30	      "contract_ids": [
    31	        "4.3",
    32	        "5.2.9"
    33	      ],
    34	      "relationship": "aligned",
    35	      "legal_topic": "Регистрация ТСТ и отказ Банка",
    36	      "matrix_standard": "Предприятие предоставляет заявление и информацию о ТСТ; Банк вправе отказать в регистрации ТСТ без объяснения причин; Предприятие обновляет информацию при изменении; информация о новых устройствах с указанием количества",
    37	      "contract_position": "п.4.3: Заказчик предоставляет заявление и информацию о ТСТ; п.5.2.9: Банк вправе в одностороннем порядке приостановить авторизации и расторгнуть контракт при нарушениях",
    38	      "matrix_evidence": "Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин",
    39	      "contract_evidence": "Заказчик после заключения контракта предоставляет Исполнителю заявление... и информацию о ТСТ",
    40	      "status_reason": "Контракт сохраняет право Банка на отказ в регистрации и приостановление. Процедура регистрации ТСТ и право отказа сохранены.",
    41	      "risk_level": "none",
    42	      "discrepancies": []
    43	    },
    44	    {
    45	      "matrix_ids": [
    46	        "2.2"
    47	      ],
    48	      "contract_ids": [
    49	        "5.1.8",
    50	        "Приложение_1_п5"
    51	      ],
    52	      "relationship": "aligned",
    53	      "legal_topic": "Валюта расчетов - рубли РФ",
    54	      "matrix_standard": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации",
    55	      "contract_position": "п.5.1.8: перечисление сумм в валюте проведения операции (рубли РФ); Приложение №1 п.5: Расчеты производятся в валюте РФ",
    56	      "matrix_evidence": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации",
    57	      "contract_evidence": "перечислять на расчетный счет Заказчика суммы Операций оплаты в валюте проведения операции (рубли РФ)",
    58	      "status_reason": "Валюта расчетов - рубли РФ - сохранена в контракте.",
    59	      "risk_level": "none",
    60	      "discrepancies": []
    61	    },
    62	    {
    63	      "matrix_ids": [
    64	        "2.3.1"
    65	      ],
    66	      "contract_ids": [
    67	        "2.3.1"
    68	      ],
    69	      "relationship": "aligned",
    70	      "legal_topic": "Обмен информацией по электронной почте с юридической силой",
    71	      "matrix_standard": "Обмен по email; исключение персональных данных, коммерческой и банковской тайны; полная юридическая сила email-сообщений",
    72	      "contract_position": "п.2.3.1: обмен по email с адресов Заказчика; исключение персональных данных, коммерческой и банковской тайны; полная юридическая сила",
    73	      "matrix_evidence": "информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу",
    74	      "contract_evidence": "информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств",
    75	      "status_reason": "Канал email, исключения по видам сведений и юридическая сила полностью сохранены.",
    76	      "risk_level": "none",
    77	      "discrepancies": []
    78	    },
    79	    {
    80	      "matrix_ids": [
    81	        "2.3.2"
    82	      ],
    83	      "contract_ids": [
    84	        "2.3.2"
    85	      ],
    86	      "relationship": "aligned",
    87	      "legal_topic": "Обмен документами через систему ДБО",
    88	      "matrix_standard": "Обмен документами посредством системы ДБО или аналогичных систем Банка",
    89	      "contract_position": "п.2.3.2: посредством системы ДБО или аналогичных систем Банка",
    90	      "matrix_evidence": "посредством системы ДБО или аналогичных систем Банка",
    91	      "contract_evidence": "посредством системы ДБО или аналогичных систем Банка",
    92	      "status_reason": "Канал ДБО полностью сохранен.",
    93	      "risk_level": "none",
    94	      "discrepancies": []
    95	    },
    96	    {
    97	      "matrix_ids": [
    98	        "2.3.3"
    99	      ],
   100	      "contract_ids": [
   101	        "2.3.3"
   102	      ],
   103	      "relationship": "aligned",
   104	      "legal_topic": "Обмен документами нарочным/курьером",
   105	      "matrix_standard": "Обмен документами с доставкой нарочным или курьером (опционально)",
   106	      "contract_position": "п.2.3.3: направление письма с доставкой нарочным или курьерской почтой",
   107	      "matrix_evidence": "путем направления письма с доставкой нарочным или курьерской почтой",
   108	      "contract_evidence": "путем направления письма с доставкой нарочным или курьерской почтой",
   109	      "status_reason": "Канал нарочным/курьером сохранен.",
   110	      "risk_level": "none",
   111	      "discrepancies": []
   112	    },
   113	    {
   114	      "matrix_ids": [
   115	        "2.3.4"
   116	      ],
   117	      "contract_ids": [
   118	        "2.3.4"
   119	      ],
   120	      "relationship": "aligned",
   121	      "legal_topic": "Обмен документами заказным письмом",
   122	      "matrix_standard": "Обмен документами через заказное письмо (опционально)",
   123	      "contract_position": "п.2.3.4: направление почтового отправления (заказного письма)",
   124	      "matrix_evidence": "путем направления почтового отправления (заказного письма)",
   125	      "contract_evidence": "путем направления почтового отправления (заказного письма)",
   126	      "status_reason": "Канал заказного письма сохранен.",
   127	      "risk_level": "none",
   128	      "discrepancies": []
   129	    },
   130	    {
   131	      "matrix_ids": [
   132	        "2.3.5"
   133	      ],
   134	      "contract_ids": [
   135	        "2.3.5"
   136	      ],
   137	      "relationship": "deviation",
   138	      "legal_topic": "Обмен через E-invoicing/СФЕРА-Курьер с УКЭП",
   139	      "matrix_standard": "Обмен через E-invoicing/СФЕРА-Курьер с УКЭП; равнозначность бумажным документам",
   140	      "contract_position": "п.2.3.5: обмен через автоматизированную систему _________ (название не заполнено); УКЭП; равнозначность",
   141	      "matrix_evidence": "путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер»",
   142	      "contract_evidence": "путем обмена электронными документами посредством автоматизированной системы _________________",
   143	      "status_reason": "Название системы ЭДО не заполнено (placeholder). Юридическая сила УКЭП сохранена, но конкретная система не указана.",
   144	      "risk_level": "low",
   145	      "discrepancies": [
   146	        {
   147	          "type": "missing_element",
   148	          "description": "Название автоматизированной системы ЭДО не заполнено (_________________)",
   149	          "risk": "Низкий риск: система не идентифицирована, но УКЭП и равнозначность сохранены. Может быть заполнено при заключении."
   150	        }
   151	      ]
   152	    },
   153	    {
   154	      "matrix_ids": [
   155	        "2.3.6"
   156	      ],
   157	      "contract_ids": [
   158	        "2.3.6"
   159	      ],
   160	      "relationship": "aligned",
   161	      "legal_topic": "Обмен через ЕИС и ЭТП (44-ФЗ)",
   162	      "matrix_standard": "Обмен через ЕИС и ЭТП с УКЭП; равнозначность бумажным документам",
   163	      "contract_position": "п.2.3.6: обмен через ЕИС и ЭТП с УКЭП; равнозначность",
   164	      "matrix_evidence": "путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках",
   165	      "contract_evidence": "путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках",
   166	      "status_reason": "Канал ЕИС/ЭТП полностью сохранен. Обязательный для 44-ФЗ.",
   167	      "risk_level": "none",
   168	      "discrepancies": []
   169	    },
   170	    {
   171	      "matrix_ids": [
   172	        "2.3.7"
   173	      ],
   174	      "contract_ids": [
   175	        "2.3.7"
   176	      ],
   177	      "relationship": "aligned",
   178	      "legal_topic": "Служба поддержки и даты получения информации",
   179	      "matrix_standard": "Канал через службу поддержки Банка 24/7; даты получения для каждого способа",
   180	      "contract_position": "п.2.3.7: служба поддержки Банка 24/7; даты получения для каждого способа",
   181	      "matrix_evidence": "через контактные данные службы поддержки Банка (24/7)",
   182	      "contract_evidence": "через контактные данные службы поддержки Банка (24/7)",
   183	      "status_reason": "Канал службы поддержки и все даты получения сохранены. Незначительное отличие: в матрице указан конкретный оператор ЭДО (ООО КОРУС Консалтинг СНГ), в контракте - «дочерняя компания Банка».",
   184	      "risk_level": "none",
   185	      "discrepancies": []
   186	    },
   187	    {
   188	      "matrix_ids": [
   189	        "2.4"
   190	      ],
   191	      "contract_ids": [
   192	        "1.1",
   193	        "8.3.2"
   194	      ],
   195	      "relationship": "aligned",
   196	      "legal_topic": "Признание ссылочных документов неотъемлемой частью",
   197	      "matrix_standard": "Документы, ссылки на которые даются в Договоре, являются неотъемлемой частью Договора",
   198	      "contract_position": "п.1.1: Приложения №1 и №2 - неотъемлемая часть контракта; п.8.3.2: прилагаемые документы - неотъемлемая часть",
   199	      "matrix_evidence": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора",
   200	      "contract_evidence": "в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта",
AI: Let me continue reading the full JSON and also read the working artifacts.[{'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_os9WdZP1iVSHiyvf5xtd0878', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/working_artifact_validation.json', 'limit': 100}, 'id': 'call_01_y0o7Tc9WtfFkxqBKVY1B6670', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 100}, 'id': 'call_02_XZYEZ6WkYi61g3w67E2s3602', 'type': 'tool_call'}]
Tool:    201	      "status_reason": "Принцип неотъемлемости приложений и ссылочных документов сохранен через п.1.1 и п.8.3.2.",
   202	      "risk_level": "none",
   203	      "discrepancies": []
   204	    },
   205	    {
   206	      "matrix_ids": [
   207	        "2.6.3.1"
   208	      ],
   209	      "contract_ids": [
   210	        "Приложение_1_п5"
   211	      ],
   212	      "relationship": "aligned",
   213	      "legal_topic": "QR-код на электронных терминалах Банка",
   214	      "matrix_standard": "QR-код подключается при установке Электронного терминала в ТСТ (Вендор - Банк)",
   215	      "contract_position": "Приложение №1 п.5: терминалы должны иметь возможность вывода QR-кода на дисплей; Возможность вывода QR-кода для безналичной оплаты на дисплей терминала",
   216	      "matrix_evidence": "QR-код подключается при установке Электронного терминала в ТСТ",
   217	      "contract_evidence": "Терминалы Исполнителя должны иметь возможность принятия бесконтактной оплаты. Возможность вывода QR-кода для безналичной оплаты на дисплей терминала",
   218	      "status_reason": "Контракт предусматривает QR-код на терминалах Банка. Функциональность сохранена.",
   219	      "risk_level": "none",
   220	      "discrepancies": []
   221	    },
   222	    {
   223	      "matrix_ids": [
   224	        "2.6.3.2"
   225	      ],
   226	      "contract_ids": [
   227	        "2.3.1",
   228	        "2.3.2",
   229	        "2.3.7"
   230	      ],
   231	      "relationship": "aligned",
   232	      "legal_topic": "Отключение QR-кода по инициативе Заказчика",
   233	      "matrix_standard": "Отключение QR-кода по инициативе Предприятия через обращение в Банк способами п.2.3.1-2.3.4, 2.3.7",
   234	      "contract_position": "Каналы обращения в Банк (email, ДБО, служба поддержки) доступны через п.2.3.1, 2.3.2, 2.3.7",
   235	      "matrix_evidence": "отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк",
   236	      "contract_evidence": "Банк и Заказчик обмениваются информацией... через контактные данные службы поддержки Банка (24/7)",
   237	      "status_reason": "Каналы для обращения в Банк сохранены. Явная процедура отключения QR отсутствует, но каналы связи доступны.",
   238	      "risk_level": "none",
   239	      "discrepancies": []
   240	    },
   241	    {
   242	      "matrix_ids": [
   243	        "2.7"
   244	      ],
   245	      "contract_ids": [
   246	        "12.4"
   247	      ],
   248	      "relationship": "aligned",
   249	      "legal_topic": "Заключение договора в электронном виде с УКЭП",
   250	      "matrix_standard": "Договор может быть заключен на бумаге или в электронном виде с УКЭП; равная юридическая сила",
   251	      "contract_position": "п.12.4: Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон",
   252	      "matrix_evidence": "Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон",
   253	      "contract_evidence": "Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон",
   254	      "status_reason": "Электронная форма с УКЭП подтверждена.",
   255	      "risk_level": "none",
   256	      "discrepancies": []
   257	    },
   258	    {
   259	      "matrix_ids": [
   260	        "3.1"
   261	      ],
   262	      "contract_ids": [
   263	        "1.3",
   264	        "5.3.7",
   265	        "5.3.8"
   266	      ],
   267	      "relationship": "aligned",
   268	      "legal_topic": "Организация приема карт Предприятием",
   269	      "matrix_standard": "Предприятие организует прием оплаты картами/реквизитами/NFC/SberPay/Плати QR; перечень карт на сайте Банка",
   270	      "contract_position": "п.1.3: Заказчик организует прием карт; п.5.3.7: размещение информационных материалов; п.5.3.8: запрет разбивки сумм",
   271	      "matrix_evidence": "Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR",
   272	      "contract_evidence": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах",
   273	      "status_reason": "Обязанность Заказчика организовать прием карт сохранена. Перечень карт в Приложении №1 (МИР, VISA, MasterCard) - стандартные ПС.",
   274	      "risk_level": "none",
   275	      "discrepancies": []
   276	    },
   277	    {
   278	      "matrix_ids": [
   279	        "3.2"
   280	      ],
   281	      "contract_ids": [
   282	        "5.1.8",
   283	        "5.1.10"
   284	      ],
   285	      "relationship": "aligned",
   286	      "legal_topic": "Перечисление Банком сумм операций",
   287	      "matrix_standard": "Банк перечисляет Предприятию суммы Операций оплаты",
   288	      "contract_position": "п.5.1.8: перечисление сумм не позднее 2 рабочих дней; п.5.1.10: перечисление сумм операций",
   289	      "matrix_evidence": "Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты",
   290	      "contract_evidence": "перечислять на расчетный счет Заказчика суммы Операций оплаты",
   291	      "status_reason": "Обязанность Банка перечислять суммы сохранена с конкретным сроком (2 рабочих дня).",
   292	      "risk_level": "none",
   293	      "discrepancies": []
   294	    },
   295	    {
   296	      "matrix_ids": [
   297	        "3.3"
   298	      ],
   299	      "contract_ids": [
   300	        "3.2",
   301	        "4.5"
   302	      ],
   303	      "relationship": "aligned",
   304	      "legal_topic": "Ежемесячная плата за услуги Банка",
   305	      "matrix_standard": "Предприятие ежемесячно перечисляет Банку плату за проведение расчетов",
   306	      "contract_position": "п.3.2: цена единицы услуги включает расходы Банка в виде процента от суммы операции; п.4.5: оплата ежемесячно",
   307	      "matrix_evidence": "Предприятие ежемесячно перечисляет Банку сумму платы за проведение расчетов по Операциям оплаты",
   308	      "contract_evidence": "Цена единицы услуги включает в себя расходы Исполнителя... в виде процента от суммы каждой Операции оплаты",
   309	      "status_reason": "Обязанность оплаты и периодичность (ежемесячно) сохранены. Конкретный тариф (процент) не раскрыт в контракте - определяется спецификацией.",
   310	      "risk_level": "none",
   311	      "discrepancies": []
   312	    },
   313	    {
   314	      "matrix_ids": [
   315	        "4.1.1"
   316	      ],
   317	      "contract_ids": [
   318	        "5.4.5"
   319	      ],
   320	      "relationship": "aligned",
   321	      "legal_topic": "Право ссылаться на оплату картами в рекламе",
   322	      "matrix_standard": "Предприятие вправе ссылаться на возможность оплаты картами/QR после согласования с Банком",
   323	      "contract_position": "п.5.4.5: Заказчик вправе ссылаться на возможность оплаты картами в рекламных материалах, предварительно согласовав их с Исполнителем",
   324	      "matrix_evidence": "Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком",
   325	      "contract_evidence": "Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем",
   326	      "status_reason": "Право и условие согласования сохранены.",
   327	      "risk_level": "none",
   328	      "discrepancies": []
   329	    },
   330	    {
   331	      "matrix_ids": [
   332	        "4.1.2"
   333	      ],
   334	      "contract_ids": [
   335	        "5.9"
   336	      ],
   337	      "relationship": "aligned",
   338	      "legal_topic": "Право на консультации Банка",
   339	      "matrix_standard": "Предприятие вправе получать консультации по эксплуатации терминалов и проведению операций через службу поддержки",
   340	      "contract_position": "п.5.9: Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации терминалов и проведению операций",
   341	      "matrix_evidence": "Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций",
   342	      "contract_evidence": "Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций",
   343	      "status_reason": "Право на консультации полностью сохранено.",
   344	      "risk_level": "none",
   345	      "discrepancies": []
   346	    },
   347	    {
   348	      "matrix_ids": [
   349	        "4.2.1"
   350	      ],
   351	      "contract_ids": [
   352	        "3.2",
   353	        "4.5",
   354	        "5.3.2"
   355	      ],
   356	      "relationship": "aligned",
   357	      "legal_topic": "Обязанность оплаты услуг Банка",
   358	      "matrix_standard": "Предприятие обязуется оплачивать услуги Банка по тарифам",
   359	      "contract_position": "п.3.2: цена включает процент от операций; п.4.5: оплата ежемесячно; п.5.3.2: обязанность оплатить",
   360	      "matrix_evidence": "Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание",
   361	      "contract_evidence": "Оплатить стоимость услуг, оказанных Исполнителем, согласно условиям настоящего контракта",
   362	      "status_reason": "Обязанность оплаты сохранена.",
   363	      "risk_level": "none",
   364	      "discrepancies": []
   365	    },
   366	    {
   367	      "matrix_ids": [
   368	        "4.2.2"
   369	      ],
   370	      "contract_ids": [
   371	        "5.3.10",
   372	        "5.10"
   373	      ],
   374	      "relationship": "deviation",
   375	      "legal_topic": "Соблюдение договора и инструктивных материалов",
   376	      "matrix_standard": "Предприятие обязуется соблюдать Договор и выполнять требования инструктивных материалов Банка",
   377	      "contract_position": "п.5.3.10: проводить операции и оформлять документы в соответствии с контрактом; п.5.10: инструктаж на сайте (адрес не заполнен)",
   378	      "matrix_evidence": "Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/инструктивных материалах, предоставляемых Банком",
   379	      "contract_evidence": "Проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту",
   380	      "status_reason": "Общая формулировка о соблюдении инструктивных материалов Банка отсутствует. Есть обязанность проводить операции по контракту и проходить инструктаж, но нет прямой обязанности соблюдать все инструктивные материалы Банка. Адрес сайта с инструктажем не заполнен.",
   381	      "risk_level": "low",
   382	      "discrepancies": [
   383	        {
   384	          "type": "obligation",
   385	          "description": "Отсутствует прямая формулировка об обязанности соблюдать инструктивные материалы Банка",
   386	          "risk": "Низкий риск: есть обязанность соблюдать контракт и проходить инструктаж. Адрес сайта с инструктажем не заполнен (placeholder)."
   387	        }
   388	      ]
   389	    },
   390	    {
   391	      "matrix_ids": [
   392	        "4.2.4"
   393	      ],
   394	      "contract_ids": [
   395	        "5.3.7"
   396	      ],
   397	      "relationship": "aligned",
   398	      "legal_topic": "Размещение информационных материалов Банка",
   399	      "matrix_standard": "Предприятие размещает информационные материалы Банка о возможности оплаты картами/QR на видных местах",
   400	      "contract_position": "п.5.3.7: Заказчик обязуется размещать на видных местах ТСТ рекламно-информационные материалы",
   401	      "matrix_evidence": "Размещать на видных местах ТСТ/общедоступных местах Ресурса, предоставляемые Банком информационные материалы",
   402	      "contract_evidence": "Размещать на видных местах ТСТ, предоставляемые исполнителем рекламно-информационные материалы, извещающие покупателей о возможности оплаты услуг с использованием карт",
   403	      "status_reason": "Обязанность размещения информационных материалов сохранена.",
   404	      "risk_level": "none",
   405	      "discrepancies": []
   406	    },
   407	    {
   408	      "matrix_ids": [
   409	        "4.2.5"
   410	      ],
   411	      "contract_ids": [
   412	        "5.3.8"
   413	      ],
   414	      "relationship": "deviation",
   415	      "legal_topic": "Прием всех карт, запрет наличных, ограничение числа карт",
   416	      "matrix_standard": "Принимать все карты из перечня; не выдавать наличные; не принимать более 2 карт от одного покупателя",
   417	      "contract_position": "п.5.3.8: запрет разбивки суммы одной операции; нет явного запрета на выдачу наличных и ограничения в 2 карты",
   418	      "matrix_evidence": "Принимать в оплату Товаров/услуг все Карты... Не выдавать по Картам наличные денежные средства. Не принимать от Покупателя более 2 (двух) различных Карт",
   419	      "contract_evidence": "Не разбивать сумму одной операции оплаты на несколько сумм",
   420	      "status_reason": "В контракте отсутствуют явные запреты на выдачу наличных по картам и ограничение не более 2 карт от одного покупателя. Запрет разбивки сумм сохранен.",
   421	      "risk_level": "medium",
   422	      "discrepancies": [
   423	        {
   424	          "type": "missing_element",
   425	          "description": "Отсутствует запрет на выдачу наличных денежных средств по картам",
   426	          "risk": "Средний риск: возможность выдачи наличных создает риск использования терминала как банкомата"
   427	        },
   428	        {
   429	          "type": "missing_element",
   430	          "description": "Отсутствует ограничение на прием не более 2 различных карт от одного покупателя",
   431	          "risk": "Средний риск: повышает риск мошеннического дробления транзакций"
   432	        }
   433	      ]
   434	    },
   435	    {
   436	      "matrix_ids": [
   437	        "4.2.6"
   438	      ],
   439	      "contract_ids": [
   440	        "5.3.8"
   441	      ],
   442	      "relationship": "aligned",
   443	      "legal_topic": "Запрет разбивки суммы операции",
   444	      "matrix_standard": "Не разбивать сумму одной Операции оплаты на несколько сумм",
   445	      "contract_position": "п.5.3.8: Не разбивать сумму одной операции оплаты на несколько сумм",
   446	      "matrix_evidence": "Не разбивать сумму одной Операции оплаты на несколько сумм",
   447	      "contract_evidence": "Не разбивать сумму одной операции оплаты на несколько сумм и не проводить отдельные операции на каждую из этих сумм",
   448	      "status_reason": "Запрет разбивки сумм полностью сохранен.",
   449	      "risk_level": "none",
   450	      "discrepancies": []
   451	    },
   452	    {
   453	      "matrix_ids": [
   454	        "4.2.7"
   455	      ],
   456	      "contract_ids": [
   457	        "5.3.9"
   458	      ],
   459	      "relationship": "aligned",
   460	      "legal_topic": "Запрет использования реквизитов карт для иных целей",
   461	      "matrix_standard": "Не использовать реквизиты карт для иных целей кроме проведения операций",
   462	      "contract_position": "п.5.3.9: Не использовать реквизиты карты для иных целей, кроме как проведение операций",
   463	      "matrix_evidence": "Не использовать реквизиты Карты/Платежного счета... для иных целей, кроме как проведение Операций",
   464	      "contract_evidence": "Не использовать реквизиты карты, которые стали доступны заказчику/ТСТ, для иных целей, кроме как проведение операций",
   465	      "status_reason": "Запрет полностью сохранен.",
   466	      "risk_level": "none",
   467	      "discrepancies": []
   468	    },
   469	    {
   470	      "matrix_ids": [
   471	        "4.2.8"
   472	      ],
   473	      "contract_ids": [],
   474	      "relationship": "missing_in_contract",
   475	      "legal_topic": "Цены не выше чем при наличном расчете",
   476	      "matrix_standard": "Предприятие предоставляет товары/услуги по ценам не выше цен при наличном расчете",
   477	      "contract_position": "Отсутствует в контракте",
   478	      "matrix_evidence": "Предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства",
   479	      "contract_evidence": "",
   480	      "status_reason": "В контракте отсутствует требование о непревышении цен при оплате картами над ценами при наличном расчете.",
   481	      "risk_level": "medium",
   482	      "discrepancies": [
   483	        {
   484	          "type": "missing_element",
   485	          "description": "Отсутствует обязательство не завышать цены при оплате картами по сравнению с наличными",
   486	          "risk": "Средний риск: Заказчик может устанавливать разные цены, что снижает привлекательность безналичной оплаты"
   487	        }
   488	      ]
   489	    },
   490	    {
   491	      "matrix_ids": [
   492	        "4.2.9"
   493	      ],
   494	      "contract_ids": [
   495	        "5.3.10"
   496	      ],
   497	      "relationship": "aligned",
   498	      "legal_topic": "Проведение операций и ответственность за информацию",
   499	      "matrix_standard": "Проводить операции и оформлять документы по Порядку; нести ответственность за правильность информации",
   500	      "contract_position": "п.5.3.10: Проводить операции и оформлять документы по операциям в ТСТ к контракту и нести ответственность за правильность информации",
Tool:      1	{
     2	  "valid": true,
     3	  "errors": [],
     4	  "warnings": [
     5	    "legal_propositions_weak_evaluable_rows:172"
     6	  ],
     7	  "counts": {
     8	    "expected_matrix_ids": 169,
     9	    "clause_index_matrix_ids": 169,
    10	    "clause_index_contract_rows": 219,
    11	    "source_contract_unique_ids": 198,
    12	    "duplicate_contract_ids": 12,
    13	    "legal_proposition_matrix_rows": 169,
    14	    "legal_proposition_contract_rows": 219,
    15	    "legal_proposition_rows": 388
    16	  },
    17	  "samples": {
    18	    "missing_matrix_ids": []
    19	  }
    20	}
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
AI: Now let me read the rest of the final JSON to see all links, unmatched_matrix, unmatched_contract, coverage_ledger, and summary.[{'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 500, 'limit': 300}, 'id': 'call_00_nAF57Wb24uxCSDMRInL87240', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 800, 'limit': 300}, 'id': 'call_01_HtL7IhGMZzQgJvy2pWKj4684', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 1100, 'limit': 300}, 'id': 'call_02_iP1LgiVRdlTBjoz7FxqB7203', 'type': 'tool_call'}]
Tool:    501	      "matrix_evidence": "Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций... и нести ответственность за правильность указанной в документах информации",
   502	      "contract_evidence": "Проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту и нести ответственность за правильность указанной в документах информации",
   503	      "status_reason": "Обязанность и ответственность сохранены.",
   504	      "risk_level": "none",
   505	      "discrepancies": []
   506	    },
   507	    {
   508	      "matrix_ids": [
   509	        "4.2.10"
   510	      ],
   511	      "contract_ids": [
   512	        "5.3.11"
   513	      ],
   514	      "relationship": "aligned",
   515	      "legal_topic": "Хранение документов по операциям 13 месяцев",
   516	      "matrix_standard": "Хранить документы не менее 13 месяцев; передавать копии Банку в течение 3 рабочих дней",
   517	      "contract_position": "п.5.3.11: хранить документы не менее 13 месяцев; передавать копии в течение 3 рабочих дней",
   518	      "matrix_evidence": "Хранить... Документы по операциям... не менее 13 (тринадцати) месяцев с даты совершения Операции и передавать их копии в Банк... в течение 3 (трех) рабочих дней",
   519	      "contract_evidence": "Хранить... документы по операциям... не менее тринадцати месяцев с даты совершения операции и передавать их копии... в течение трех рабочих дней",
   520	      "status_reason": "Срок хранения (13 месяцев) и срок передачи копий (3 рабочих дня) полностью сохранены.",
   521	      "risk_level": "none",
   522	      "discrepancies": []
   523	    },
   524	    {
   525	      "matrix_ids": [
   526	        "4.2.11"
   527	      ],
   528	      "contract_ids": [
   529	        "5.3.12",
   530	        "5.5"
   531	      ],
   532	      "relationship": "aligned",
   533	      "legal_topic": "Предоставление заявления об обстоятельствах операции",
   534	      "matrix_standard": "Передавать письменное заявление об обстоятельствах операции в течение 3 рабочих дней; немедленно сообщать об утрате документов",
   535	      "contract_position": "п.5.3.12: передавать заявление в течение 3 рабочих дней; п.5.5: аналогичная обязанность",
   536	      "matrix_evidence": "Передавать в Банк по его запросу в течение 3 (трех) рабочих дней... письменное заявление с изложением обстоятельств проведения Операции",
   537	      "contract_evidence": "Передавать исполнителю по его запросу в течение трех рабочих дней... письменное заявление с изложением обстоятельств проведения операции",
   538	      "status_reason": "Обязанность и срок (3 рабочих дня) полностью сохранены.",
   539	      "risk_level": "none",
   540	      "discrepancies": []
   541	    },
   542	    {
   543	      "matrix_ids": [
   544	        "4.2.13"
   545	      ],
   546	      "contract_ids": [
   547	        "5.3.19"
   548	      ],
   549	      "relationship": "aligned",
   550	      "legal_topic": "Возмещение Банку всех сумм и убытков",
   551	      "matrix_standard": "Предприятие возмещает Банку в полном объеме: спорные суммы, недействительные операции, сборы ПС, убытки от штрафов",
   552	      "contract_position": "п.5.3.19: возмещение в полном объеме спорных сумм, недействительных операций, сборов ПС, убытков от штрафов",
   553	      "matrix_evidence": "Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере средств... списанных со счета Банка",
   554	      "contract_evidence": "Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере средств... списанных со счета Исполнителя",
   555	      "status_reason": "Обязанность полного возмещения сохранена. Перечень случаев покрытия совпадает.",
   556	      "risk_level": "none",
   557	      "discrepancies": []
   558	    },
   559	    {
   560	      "matrix_ids": [
   561	        "4.2.14"
   562	      ],
   563	      "contract_ids": [
   564	        "5.3.13"
   565	      ],
   566	      "relationship": "aligned",
   567	      "legal_topic": "Уведомление Банка об изменениях",
   568	      "matrix_standard": "Информировать Банк о реорганизации, изменениях, банкротстве, смене руководства, адреса, реквизитов в течение 3 рабочих дней",
   569	      "contract_position": "п.5.3.13: информировать о реорганизации, изменениях, банкротстве, смене руководства, адреса, реквизитов не позднее 3 рабочих дней",
   570	      "matrix_evidence": "информировать Банк и передать... документы... не позднее 3 (трех) рабочих дней с даты дополнений/изменений",
   571	      "contract_evidence": "обязуется информировать исполнителя и передать... документы... не позднее трех рабочих дней с даты дополнений/изменений",
   572	      "status_reason": "Обязанность и срок (3 рабочих дня) полностью сохранены.",
   573	      "risk_level": "none",
   574	      "discrepancies": []
   575	    },
   576	    {
   577	      "matrix_ids": [
   578	        "4.2.15"
   579	      ],
   580	      "contract_ids": [
   581	        "5.3.14"
   582	      ],
   583	      "relationship": "aligned",
   584	      "legal_topic": "Предоставление достоверных сведений и обновление",
   585	      "matrix_standard": "Предоставлять достоверные сведения; обновлять не реже 1 раза в год; по запросу в течение 7 рабочих дней",
   586	      "contract_position": "п.5.3.14: предоставлять достоверные сведения; обновлять не реже 1 раза в год; по запросу в течение 7 рабочих дней",
   587	      "matrix_evidence": "Предоставлять в Банк достоверные документы и сведения... не реже одного раза в год, а также по отдельному запросу Банка в течение 7 (семи) рабочих дней",
   588	      "contract_evidence": "Предоставлять исполнителю достоверные документы и сведения... не реже одного раза в год, а также по отдельному запросу исполнителя в течение семи рабочих дней",
   589	      "status_reason": "Обязанность и сроки полностью сохранены.",
   590	      "risk_level": "none",
   591	      "discrepancies": []
   592	    },
   593	    {
   594	      "matrix_ids": [
   595	        "4.2.16.1"
   596	      ],
   597	      "contract_ids": [
   598	        "5.3.20"
   599	      ],
   600	      "relationship": "aligned",
   601	      "legal_topic": "Персональные данные руководителя",
   602	      "matrix_standard": "Предприятие гарантирует правовые основания на передачу ПДн руководителя (ФИО, адрес, паспорт); передача в ПС МИР",
   603	      "contract_position": "п.5.3.20: Заказчик гарантирует правовые основания на передачу ПДн руководителя (ФИО, адрес, паспортные данные); передача в ПС МИР",
   604	      "matrix_evidence": "Предприятие гарантирует наличие правовых оснований на передачу в Банк персональных данных руководителя Предприятия... состав которых включает: ФИО, адрес, паспортные данные",
   605	      "contract_evidence": "Заказчик гарантирует наличие правовых оснований на передачу Исполнителю персональных данных руководителя Заказчика, состав которых включает: ФИО, адрес, паспортные данные",
   606	      "status_reason": "Гарантия правовых оснований и состав ПДн полностью сохранены.",
   607	      "risk_level": "none",
   608	      "discrepancies": []
   609	    },
   610	    {
   611	      "matrix_ids": [
   612	        "4.2.16.2"
   613	      ],
   614	      "contract_ids": [
   615	        "5.3.20"
   616	      ],
   617	      "relationship": "deviation",
   618	      "legal_topic": "Персональные данные сотрудников",
   619	      "matrix_standard": "Предприятие гарантирует наличие согласий на обработку ПДн сотрудников (ФИО, мобильный телефон, email, должность, место работы); передача в обслуживающие компании",
   620	      "contract_position": "п.5.3.20: только ПДн руководителя. ПДн сотрудников отдельно не урегулированы",
   621	      "matrix_evidence": "Предприятие гарантирует наличие согласий на обработку Банком персональных данных своих работников, состав которых включает: ФИО, мобильный телефон, электронная почта, должность и место работы",
   622	      "contract_evidence": "Заказчик передает Исполнителю персональные данные руководителя Заказчика, состав которых включает: ФИО, адрес, паспортные данные",
   623	      "status_reason": "Контракт регулирует только ПДн руководителя. ПДн сотрудников (согласия, состав, передача в обслуживающие компании) отсутствуют.",
   624	      "risk_level": "medium",
   625	      "discrepancies": [
   626	        {
   627	          "type": "missing_element",
   628	          "description": "Отсутствует регулирование персональных данных сотрудников (кроме руководителя)",
   629	          "risk": "Средний риск: отсутствие согласий сотрудников на обработку ПДн создает регуляторный риск по 152-ФЗ"
   630	        }
   631	      ]
   632	    },
   633	    {
   634	      "matrix_ids": [
   635	        "4.2.16.3"
   636	      ],
   637	      "contract_ids": [
   638	        "5.3.15"
   639	      ],
   640	      "relationship": "deviation",
   641	      "legal_topic": "Подтверждение правомерности передачи ПДн",
   642	      "matrix_standard": "По запросу Банка в течение 3 рабочих дней предоставить подтверждение правомерности передачи ПДн; иначе урегулировать претензии за свой счет",
   643	      "contract_position": "п.5.3.15: по запросу предоставить подтверждение правомерности передачи ПДн; урегулировать претензии за свой счет",
   644	      "matrix_evidence": "По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней... предоставить подтверждение правомерности передачи ПДн",
   645	      "contract_evidence": "По письменному запросу исполнителя заказчик обязуется предоставить подтверждение правомерности передачи ПДн",
   646	      "status_reason": "Обязанность подтверждения сохранена, но срок изменен: матрица требует 3 рабочих дня, контракт устанавливает общий срок ответа 10 календарных дней (п.10.1).",
   647	      "risk_level": "low",
   648	      "discrepancies": [
   649	        {
   650	          "type": "deadline",
   651	          "description": "Срок предоставления подтверждения (3 рабочих дня) заменен на общий срок ответа 10 календарных дней (п.10.1)",
   652	          "risk": "Низкий риск: срок увеличен, но остается разумным"
   653	        }
   654	      ]
   655	    },
   656	    {
   657	      "matrix_ids": [
   658	        "4.2.18"
   659	      ],
   660	      "contract_ids": [
   661	        "5.3.16"
   662	      ],
   663	      "relationship": "aligned",
   664	      "legal_topic": "Прекращение приема карт при расторжении",
   665	      "matrix_standard": "С даты расторжения прекратить прием карт, снять информационные материалы",
   666	      "contract_position": "п.5.3.16: с даты расторжения прекратить прием карт, снять рекламно-информационные материалы",
   667	      "matrix_evidence": "С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы",
   668	      "contract_evidence": "С даты расторжения контракта прекратить прием к оплате карт, снять рекламно-информационные материалы",
   669	      "status_reason": "Обязанность полностью сохранена.",
   670	      "risk_level": "none",
   671	      "discrepancies": []
   672	    },
   673	    {
   674	      "matrix_ids": [
   675	        "4.2.19"
   676	      ],
   677	      "contract_ids": [
   678	        "5.3.17"
   679	      ],
   680	      "relationship": "aligned",
   681	      "legal_topic": "Содействие проверкам Банка",
   682	      "matrix_standard": "Не противодействовать проверкам Банка; оказывать содействие в расследовании подозрительных операций",
   683	      "contract_position": "п.5.3.17: не принимать мер противодействия проверкам; оказывать содействие в разбирательстве",
   684	      "matrix_evidence": "Не принимать мер противодействия Банку в проведении проверки... а также оказывать содействие Банку в проведении разбирательства",
   685	      "contract_evidence": "Не принимать мер противодействия исполнителю в проведение проверки... а также оказывать содействие исполнителю в проведении разбирательства",
   686	      "status_reason": "Обязанность полностью сохранена.",
   687	      "risk_level": "none",
   688	      "discrepancies": []
   689	    },
   690	    {
   691	      "matrix_ids": [
   692	        "4.2.20.1"
   693	      ],
   694	      "contract_ids": [
   695	        "5.10"
   696	      ],
   697	      "relationship": "deviation",
   698	      "legal_topic": "Самостоятельный инструктаж сотрудников",
   699	      "matrix_standard": "Предприятие самостоятельно обеспечивает прохождение инструктажа сотрудниками на сайте Банка",
   700	      "contract_position": "п.5.10: Заказчик обязуется обеспечить прохождение инструктажа на сайте ________ (адрес не заполнен)",
   701	      "matrix_evidence": "Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа... размещенном на сайте: https://www.sberbank.ru/help/business/acquiring",
   702	      "contract_evidence": "Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________",
   703	      "status_reason": "Обязанность инструктажа сохранена, но адрес сайта не заполнен (placeholder).",
   704	      "risk_level": "low",
   705	      "discrepancies": [
   706	        {
   707	          "type": "missing_element",
   708	          "description": "Адрес сайта с инструктажем не заполнен (_________________)",
   709	          "risk": "Низкий риск: обязанность инструктажа есть, адрес может быть заполнен при заключении"
   710	        }
   711	      ]
   712	    },
   713	    {
   714	      "matrix_ids": [
   715	        "4.2.20.2"
   716	      ],
   717	      "contract_ids": [
   718	        "5.3.18.1"
   719	      ],
   720	      "relationship": "aligned",
   721	      "legal_topic": "Использование оборудования Банка только для целей контракта",
   722	      "matrix_standard": "Использовать терминалы и ПО Банка только для целей договора; не изменять, не ремонтировать, не передавать третьим лицам",
   723	      "contract_position": "п.5.3.18.1: использовать терминалы только для целей контракта; не изменять ПО; не ремонтировать; не передавать третьим лицам",
   724	      "matrix_evidence": "Использовать Электронные терминалы... только для целей реализации настоящего Договора... Не вносить изменения... Не осуществлять самостоятельно ремонт... Не передавать третьим лицам",
   725	      "contract_evidence": "Использовать электронные терминалы... только для целей реализации настоящего контракта... Не вносить изменения... не осуществлять самостоятельно их ремонт... Не передавать третьим лицам",
   726	      "status_reason": "Все ограничения использования полностью сохранены.",
   727	      "risk_level": "none",
   728	      "discrepancies": []
   729	    },
   730	    {
   731	      "matrix_ids": [
   732	        "4.2.20.3"
   733	      ],
   734	      "contract_ids": [
   735	        "5.3.18.2"
   736	      ],
   737	      "relationship": "aligned",
   738	      "legal_topic": "Доступ к местам установки терминалов",
   739	      "matrix_standard": "Предоставлять доступ работникам обслуживающей компании для подключения, настройки, ремонта, замены, обслуживания",
   740	      "contract_position": "п.5.3.18.2: предоставлять доступ для подключения, настройки, ремонта, замены, технического обслуживания",
   741	      "matrix_evidence": "Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов",
   742	      "contract_evidence": "Предоставлять исполнителю доступ к местам установки электронных терминалов для проведения работ по его подключению, настройке, ремонту, замене, техническому обслуживанию",
   743	      "status_reason": "Обязанность доступа сохранена.",
   744	      "risk_level": "none",
   745	      "discrepancies": []
   746	    },
   747	    {
   748	      "matrix_ids": [
   749	        "4.2.20.4"
   750	      ],
   751	      "contract_ids": [
   752	        "5.3.18.3"
   753	      ],
   754	      "relationship": "aligned",
   755	      "legal_topic": "Приемка терминалов по акту",
   756	      "matrix_standard": "Принять терминалы по акту в 2 экземплярах, подписанных уполномоченными работниками",
   757	      "contract_position": "п.5.3.18.3: Принять электронные терминалы по акту принятия оказанных услуг в двух экземплярах",
   758	      "matrix_evidence": "Принять Электронные терминалы... по акту принятия оказанных услуг... составленному в 2-х экземплярах",
   759	      "contract_evidence": "Принять электронные терминалы по акту принятия оказанных услуг, составленному в двух экземплярах",
   760	      "status_reason": "Процедура приемки по акту сохранена.",
   761	      "risk_level": "none",
   762	      "discrepancies": []
   763	    },
   764	    {
   765	      "matrix_ids": [
   766	        "4.2.20.5"
   767	      ],
   768	      "contract_ids": [
   769	        "5.3.20.4"
   770	      ],
   771	      "relationship": "aligned",
   772	      "legal_topic": "Уведомление о выходе терминала из строя",
   773	      "matrix_standard": "Немедленно информировать Банк о выходе терминала из строя или утрате",
   774	      "contract_position": "п.5.3.20.4: В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя",
   775	      "matrix_evidence": "В случае выхода Электронного терминала... из строя или его утраты немедленно информировать об этом Банк",
   776	      "contract_evidence": "В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя",
   777	      "status_reason": "Обязанность немедленного уведомления сохранена.",
   778	      "risk_level": "none",
   779	      "discrepancies": []
   780	    },
   781	    {
   782	      "matrix_ids": [
   783	        "4.2.20.6"
   784	      ],
   785	      "contract_ids": [
   786	        "5.3.18.5",
   787	        "5.6"
   788	      ],
   789	      "relationship": "aligned",
   790	      "legal_topic": "Возврат терминалов после расторжения",
   791	      "matrix_standard": "Вернуть терминалы в течение 5 рабочих дней с даты расторжения или получения требования",
   792	      "contract_position": "п.5.3.18.5: вернуть в течение 5 рабочих дней с даты расторжения или получения требования; п.5.6: аналогично",
   793	      "matrix_evidence": "Вернуть Банку... Электронные терминалы... в течение 5 (пяти) рабочих дней с даты расторжения Договора",
   794	      "contract_evidence": "Вернуть исполнителю... электронные терминалы... в течение пяти рабочих дней с даты расторжения контракта",
   795	      "status_reason": "Срок возврата (5 рабочих дней) и условия полностью сохранены.",
   796	      "risk_level": "none",
   797	      "discrepancies": []
   798	    },
   799	    {
   800	      "matrix_ids": [
Tool:    801	        "4.2.20.7"
   802	      ],
   803	      "contract_ids": [
   804	        "5.7"
   805	      ],
   806	      "relationship": "deviation",
   807	      "legal_topic": "Штраф за невозврат терминалов",
   808	      "matrix_standard": "Штраф 25 000 руб. за каждый электронный терминал и 25 000 руб. за каждый смарт-терминал",
   809	      "contract_position": "п.5.7: штраф 10 000 руб. за электронный терминал, 25 000 руб. за смарт-терминал",
   810	      "matrix_evidence": "уплатить Банку штраф в размере 25 000... за каждый Электронный терминал и 25 000... за каждый Смарт-терминал",
   811	      "contract_evidence": "Заказчик обязан уплатить Исполнителю штраф в размере 10 000... за каждый Электронный терминал, в размере 25 000... за каждый Смарт-терминал",
   812	      "status_reason": "Штраф за электронный терминал снижен с 25 000 до 10 000 руб. Штраф за смарт-терминал сохранен (25 000 руб.).",
   813	      "risk_level": "medium",
   814	      "discrepancies": [
   815	        {
   816	          "type": "amount",
   817	          "description": "Штраф за невозврат электронного терминала: 10 000 руб. в контракте против 25 000 руб. в матрице",
   818	          "risk": "Средний риск: снижение штрафа ослабляет стимул к возврату оборудования"
   819	        }
   820	      ]
   821	    },
   822	    {
   823	      "matrix_ids": [
   824	        "5.1.1.1"
   825	      ],
   826	      "contract_ids": [
   827	        "5.2.10.1"
   828	      ],
   829	      "relationship": "aligned",
   830	      "legal_topic": "Удержание сумм недействительных операций",
   831	      "matrix_standard": "Банк удерживает суммы недействительных операций (12 оснований)",
   832	      "contract_position": "п.5.2.10.1: Исполнитель удерживает суммы недействительных операций (аналогичный перечень оснований)",
   833	      "matrix_evidence": "Банк имеет право: Удерживать из сумм... Суммы Операций, являющихся недействительными",
   834	      "contract_evidence": "Удерживать из сумм, подлежащих перечислению Заказчику... Суммы Операций, являющихся недействительными",
   835	      "status_reason": "Право удержания и перечень оснований сохранены.",
   836	      "risk_level": "none",
   837	      "discrepancies": []
   838	    },
   839	    {
   840	      "matrix_ids": [
   841	        "5.1.1.2"
   842	      ],
   843	      "contract_ids": [
   844	        "5.2.10.2"
   845	      ],
   846	      "relationship": "aligned",
   847	      "legal_topic": "Удержание ошибочно перечисленных сумм",
   848	      "matrix_standard": "Банк удерживает суммы, ошибочно перечисленные на счет Предприятия",
   849	      "contract_position": "п.5.2.10.2: Суммы, ошибочно перечисленные на счет Заказчика",
   850	      "matrix_evidence": "Удерживать... Суммы, ошибочно перечисленные на счет Предприятия",
   851	      "contract_evidence": "Суммы, ошибочно перечисленные на счет Заказчика",
   852	      "status_reason": "Право удержания ошибочно перечисленных сумм сохранено.",
   853	      "risk_level": "none",
   854	      "discrepancies": []
   855	    },
   856	    {
   857	      "matrix_ids": [
   858	        "5.1.1.3"
   859	      ],
   860	      "contract_ids": [
   861	        "5.2.10.3"
   862	      ],
   863	      "relationship": "aligned",
   864	      "legal_topic": "Удержание сумм возвратов и реверсивных транзакций",
   865	      "matrix_standard": "Банк удерживает суммы операций возврата, возврата платежа и реверсивных транзакций",
   866	      "contract_position": "п.5.2.10.3: Суммы Операций возврата, Возврата платежа и Реверсивные транзакции",
   867	      "matrix_evidence": "Удерживать... Суммы Операций возврата, Возврата платежа и Реверсивные транзакции",
   868	      "contract_evidence": "Суммы Операций возврата, Возврата платежа и Реверсивные транзакции",
   869	      "status_reason": "Право удержания полностью сохранено.",
   870	      "risk_level": "none",
   871	      "discrepancies": []
   872	    },
   873	    {
   874	      "matrix_ids": [
   875	        "5.1.1.4"
   876	      ],
   877	      "contract_ids": [
   878	        "5.2.10.4"
   879	      ],
   880	      "relationship": "aligned",
   881	      "legal_topic": "Удержание оспоренных сумм",
   882	      "matrix_standard": "Банк удерживает суммы оспоренных/списанных операций по правилам ПС",
   883	      "contract_position": "п.5.2.10.4: удержание сумм оспоренных/списанных операций",
   884	      "matrix_evidence": "Удерживать... Суммы Операций, которые были оспорены и/или списаны со счета Банка",
   885	      "contract_evidence": "Исполнитель удерживает... суммы операций, которые были оспорены и/или списаны со счета Исполнителя",
   886	      "status_reason": "Право удержания сохранено.",
   887	      "risk_level": "none",
   888	      "discrepancies": []
   889	    },
   890	    {
   891	      "matrix_ids": [
   892	        "5.1.1.5"
   893	      ],
   894	      "contract_ids": [
   895	        "5.2.10.5"
   896	      ],
   897	      "relationship": "aligned",
   898	      "legal_topic": "Удержание штрафов ПС и убытков",
   899	      "matrix_standard": "Банк удерживает суммы штрафов ПС и убытков от ответственности из-за Предприятия",
   900	      "contract_position": "п.5.2.10.5: удержание штрафов ПС и убытков от ответственности",
   901	      "matrix_evidence": "Удерживать... суммы штрафов и иных убытков, возникших у Банка в результате применения к нему штрафных санкций",
   902	      "contract_evidence": "Банк удерживает... суммы штрафов и иных убытков, возникших у Исполнителя в результате применения к нему штрафных санкций",
   903	      "status_reason": "Право удержания полностью сохранено.",
   904	      "risk_level": "none",
   905	      "discrepancies": []
   906	    },
   907	    {
   908	      "matrix_ids": [
   909	        "5.1.1.6"
   910	      ],
   911	      "contract_ids": [
   912	        "5.7"
   913	      ],
   914	      "relationship": "aligned",
   915	      "legal_topic": "Удержание штрафов за невозврат терминалов",
   916	      "matrix_standard": "Возможность удержания штрафов за невозврат терминалов",
   917	      "contract_position": "п.5.7: штраф за невозврат терминалов",
   918	      "matrix_evidence": "Возможность удержания штрафов за невозврат терминалов",
   919	      "contract_evidence": "Заказчик обязан уплатить Исполнителю штраф... за каждый Электронный терминал",
   920	      "status_reason": "Механизм штрафа сохранен (размер см. 4.2.20.7).",
   921	      "risk_level": "none",
   922	      "discrepancies": []
   923	    },
   924	    {
   925	      "matrix_ids": [
   926	        "5.1.2"
   927	      ],
   928	      "contract_ids": [
   929	        "5.2.1"
   930	      ],
   931	      "relationship": "aligned",
   932	      "legal_topic": "Право требовать исполнения обязательств",
   933	      "matrix_standard": "Банк вправе требовать от Предприятия своевременного исполнения обязательств",
   934	      "contract_position": "п.5.2.1: Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате",
   935	      "matrix_evidence": "Требовать от Предприятия своевременного исполнения обязательств",
   936	      "contract_evidence": "Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате стоимости услуг",
   937	      "status_reason": "Право требования сохранено.",
   938	      "risk_level": "none",
   939	      "discrepancies": []
   940	    },
   941	    {
   942	      "matrix_ids": [
   943	        "5.1.3"
   944	      ],
   945	      "contract_ids": [
   946	        "5.2.2"
   947	      ],
   948	      "relationship": "aligned",
   949	      "legal_topic": "Односторонний отказ от исполнения",
   950	      "matrix_standard": "Банк вправе принять решение об одностороннем отказе по основаниям 44-ФЗ и ГК РФ",
   951	      "contract_position": "п.5.2.2: Принять решение об одностороннем отказе по основаниям 44-ФЗ и ГК РФ",
   952	      "matrix_evidence": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ",
   953	      "contract_evidence": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ",
   954	      "status_reason": "Право одностороннего отказа полностью сохранено.",
   955	      "risk_level": "none",
   956	      "discrepancies": []
   957	    },
   958	    {
   959	      "matrix_ids": [
   960	        "5.1.4"
   961	      ],
   962	      "contract_ids": [
   963	        "5.2.3"
   964	      ],
   965	      "relationship": "aligned",
   966	      "legal_topic": "Проверка и замена терминалов",
   967	      "matrix_standard": "Банк вправе проверять состояние терминалов, заменять и обновлять ПО с уведомлением за 2 рабочих дня",
   968	      "contract_position": "п.5.2.3: проверка технического состояния, замена, обновление ПО с уведомлением не менее чем за 2 рабочих дня",
   969	      "matrix_evidence": "Осуществлять проверку технического состояния... Производить замену... обновлять программное обеспечение... уведомив... не менее чем за два рабочих дня",
   970	      "contract_evidence": "Осуществлять проверку технического состояния... Производить замену... обновлять программное обеспечение... уведомив заказчика не менее чем за два рабочих дня",
   971	      "status_reason": "Права проверки, замены и обновления с уведомлением за 2 рабочих дня сохранены.",
   972	      "risk_level": "none",
   973	      "discrepancies": []
   974	    },
   975	    {
   976	      "matrix_ids": [
   977	        "5.1.5"
   978	      ],
   979	      "contract_ids": [
   980	        "5.2.4"
   981	      ],
   982	      "relationship": "aligned",
   983	      "legal_topic": "Удаленное обновление ПО",
   984	      "matrix_standard": "Допускается удаленное обновление ПО, не затрагивающее порядок операций",
   985	      "contract_position": "п.5.2.4: Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций",
   986	      "matrix_evidence": "Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций",
   987	      "contract_evidence": "Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций",
   988	      "status_reason": "Право удаленного обновления полностью сохранено.",
   989	      "risk_level": "none",
   990	      "discrepancies": []
   991	    },
   992	    {
   993	      "matrix_ids": [
   994	        "5.1.6"
   995	      ],
   996	      "contract_ids": [
   997	        "5.2.5"
   998	      ],
   999	      "relationship": "aligned",
  1000	      "legal_topic": "Запрос документов по операциям",
  1001	      "matrix_standard": "Банк вправе запрашивать документы по операциям не позднее 13 месяцев с даты операции",
  1002	      "contract_position": "п.5.2.5: Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции",
  1003	      "matrix_evidence": "Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции",
  1004	      "contract_evidence": "Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции",
  1005	      "status_reason": "Право запроса и срок (13 месяцев) сохранены.",
  1006	      "risk_level": "none",
  1007	      "discrepancies": []
  1008	    },
  1009	    {
  1010	      "matrix_ids": [
  1011	        "5.1.7"
  1012	      ],
  1013	      "contract_ids": [
  1014	        "5.2.6"
  1015	      ],
  1016	      "relationship": "aligned",
  1017	      "legal_topic": "Уведомление об изменении реквизитов Банка",
  1018	      "matrix_standard": "Банк уведомляет об изменении реквизитов в течение 3 рабочих дней",
  1019	      "contract_position": "п.5.2.6: уведомить об изменении реквизитов в течение трех рабочих дней",
  1020	      "matrix_evidence": "В случае изменения реквизитов... уведомить об этом... в течение трех рабочих дней",
  1021	      "contract_evidence": "В случае изменения реквизитов исполнителя... уведомить об этом заказчика... в течение трех рабочих дней",
  1022	      "status_reason": "Обязанность и срок сохранены.",
  1023	      "risk_level": "none",
  1024	      "discrepancies": []
  1025	    },
  1026	    {
  1027	      "matrix_ids": [
  1028	        "5.1.8.1"
  1029	      ],
  1030	      "contract_ids": [
  1031	        "5.1.1"
  1032	      ],
  1033	      "relationship": "deviation",
  1034	      "legal_topic": "Установка терминалов",
  1035	      "matrix_standard": "Установить терминалы в течение 3 рабочих дней с даты подписания договора",
  1036	      "contract_position": "п.5.1.1: установить в течение 5 рабочих дней с даты подписания контракта",
  1037	      "matrix_evidence": "Установить Заказчику и подготовить к эксплуатации Электронные терминалы... в течение 3 рабочих дней",
  1038	      "contract_evidence": "Установить Заказчику и подготовить к эксплуатации Электронные терминалы... в течение 5 (пяти) рабочих дней",
  1039	      "status_reason": "Срок установки увеличен с 3 до 5 рабочих дней.",
  1040	      "risk_level": "low",
  1041	      "discrepancies": [
  1042	        {
  1043	          "type": "deadline",
  1044	          "description": "Срок установки терминалов: 5 рабочих дней в контракте против 3 рабочих дней в матрице",
  1045	          "risk": "Низкий риск: увеличение срока на 2 дня несущественно для операционной деятельности"
  1046	        }
  1047	      ]
  1048	    },
  1049	    {
  1050	      "matrix_ids": [
  1051	        "5.1.8.2"
  1052	      ],
  1053	      "contract_ids": [
  1054	        "5.1.2"
  1055	      ],
  1056	      "relationship": "aligned",
  1057	      "legal_topic": "Ежемесячное формирование документа о приемке",
  1058	      "matrix_standard": "Ежемесячно формировать и направлять документ о приемке",
  1059	      "contract_position": "п.5.1.2: Ежемесячно формировать и направлять Заказчику документ о приемке",
  1060	      "matrix_evidence": "Ежемесячно формировать и направлять... документ о приемке",
  1061	      "contract_evidence": "Ежемесячно формировать и направлять Заказчику документ о приемке",
  1062	      "status_reason": "Обязанность сохранена.",
  1063	      "risk_level": "none",
  1064	      "discrepancies": []
  1065	    },
  1066	    {
  1067	      "matrix_ids": [
  1068	        "5.1.8.3"
  1069	      ],
  1070	      "contract_ids": [
  1071	        "5.1.3"
  1072	      ],
  1073	      "relationship": "aligned",
  1074	      "legal_topic": "Соответствие услуг законодательству",
  1075	      "matrix_standard": "Обеспечить соответствие услуг требованиям законодательства РФ",
  1076	      "contract_position": "п.5.1.3: Обеспечить соответствие оказанных услуг требованиям законодательства РФ",
  1077	      "matrix_evidence": "Обеспечить соответствие оказанных услуг предъявляемым к ним требованиям законодательства",
  1078	      "contract_evidence": "Обеспечить соответствие оказанных услуг предъявляемым к ним требованиям законодательства Российской Федерации",
  1079	      "status_reason": "Обязанность сохранена.",
  1080	      "risk_level": "none",
  1081	      "discrepancies": []
  1082	    },
  1083	    {
  1084	      "matrix_ids": [
  1085	        "5.1.8.4"
  1086	      ],
  1087	      "contract_ids": [
  1088	        "5.1.4"
  1089	      ],
  1090	      "relationship": "aligned",
  1091	      "legal_topic": "Круглосуточная работоспособность и замена терминалов",
  1092	      "matrix_standard": "Обеспечить круглосуточную работоспособность; замена неисправного терминала не позднее 3 рабочих дней",
  1093	      "contract_position": "п.5.1.4: круглосуточная работоспособность; замена не позднее 3 рабочих дней",
  1094	      "matrix_evidence": "Обеспечивать круглосуточную работоспособность... обеспечить исправным терминалом не позднее 3 рабочих дней",
  1095	      "contract_evidence": "Обеспечивать круглосуточную работоспособность... обеспечить Заказчика исправным Электронным терминалом Банка не позднее 3 (трех) рабочих дней",
  1096	      "status_reason": "Обязанность и срок замены (3 рабочих дня) сохранены.",
  1097	      "risk_level": "none",
  1098	      "discrepancies": []
  1099	    },
  1100	    {
Tool:   1101	      "matrix_ids": [
  1102	        "5.1.8.5"
  1103	      ],
  1104	      "contract_ids": [
  1105	        "5.1.5"
  1106	      ],
  1107	      "relationship": "aligned",
  1108	      "legal_topic": "Предоставление информации об услугах",
  1109	      "matrix_standard": "Предоставлять полную и точную информацию об услугах и ходе исполнения",
  1110	      "contract_position": "п.5.1.5: Предоставлять Заказчику полную и точную информацию об услугах, а также о ходе исполнения",
  1111	      "matrix_evidence": "Предоставлять... полную и точную информацию об услугах, а также о ходе исполнения своих обязательств",
  1112	      "contract_evidence": "Предоставлять Заказчику полную и точную информацию об услугах, а также о ходе исполнения своих обязательств",
  1113	      "status_reason": "Обязанность сохранена.",
  1114	      "risk_level": "none",
  1115	      "discrepancies": []
  1116	    },
  1117	    {
  1118	      "matrix_ids": [
  1119	        "5.1.8.6"
  1120	      ],
  1121	      "contract_ids": [
  1122	        "5.1.6"
  1123	      ],
  1124	      "relationship": "aligned",
  1125	      "legal_topic": "Круглосуточная авторизация",
  1126	      "matrix_standard": "Осуществлять круглосуточную авторизацию",
  1127	      "contract_position": "п.5.1.6: Осуществлять круглосуточную авторизацию",
  1128	      "matrix_evidence": "Осуществлять круглосуточную авторизацию",
  1129	      "contract_evidence": "Осуществлять круглосуточную авторизацию",
  1130	      "status_reason": "Обязанность сохранена.",
  1131	      "risk_level": "none",
  1132	      "discrepancies": []
  1133	    },
  1134	    {
  1135	      "matrix_ids": [
  1136	        "5.1.8.7"
  1137	      ],
  1138	      "contract_ids": [
  1139	        "5.1.7"
  1140	      ],
  1141	      "relationship": "aligned",
  1142	      "legal_topic": "Обеспечение рекламно-информационными материалами",
  1143	      "matrix_standard": "Обеспечивать терминалы рекламно-информационными материалами",
  1144	      "contract_position": "п.5.1.7: Обеспечивать электронные терминалы рекламно-информационными материалами",
  1145	      "matrix_evidence": "Обеспечивать электронные терминалы... рекламно-информационными материалами",
  1146	      "contract_evidence": "Обеспечивать электронные терминалы, установленные у заказчика/ТСТ, рекламно-информационными материалами",
  1147	      "status_reason": "Обязанность сохранена.",
  1148	      "risk_level": "none",
  1149	      "discrepancies": []
  1150	    },
  1151	    {
  1152	      "matrix_ids": [
  1153	        "5.1.8.8"
  1154	      ],
  1155	      "contract_ids": [
  1156	        "5.1.8"
  1157	      ],
  1158	      "relationship": "aligned",
  1159	      "legal_topic": "Перечисление сумм не позднее 2 рабочих дней",
  1160	      "matrix_standard": "Перечислять суммы операций не позднее 2 рабочих дней с даты получения расчетной информации",
  1161	      "contract_position": "п.5.1.8: перечислять не позднее 2 рабочих дней с даты получения расчетной информации",
  1162	      "matrix_evidence": "не позднее 2 (двух) рабочих дней с даты получения расчетной информации... перечислять на расчетный счет... суммы Операций оплаты",
  1163	      "contract_evidence": "не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный счет Заказчика суммы Операций оплаты",
  1164	      "status_reason": "Срок перечисления (2 рабочих дня) сохранен.",
  1165	      "risk_level": "none",
  1166	      "discrepancies": []
  1167	    },
  1168	    {
  1169	      "matrix_ids": [
  1170	        "5.1.8.9"
  1171	      ],
  1172	      "contract_ids": [
  1173	        "5.1.8"
  1174	      ],
  1175	      "relationship": "aligned",
  1176	      "legal_topic": "Дата получения расчетной информации",
  1177	      "matrix_standard": "Дата получения расчетной информации - рабочий день, следующий за днем электронной сверки итогов",
  1178	      "contract_position": "п.5.1.8: Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов",
  1179	      "matrix_evidence": "Датой получения расчетной информации... является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов",
  1180	      "contract_evidence": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов",
  1181	      "status_reason": "Определение даты полностью сохранено.",
  1182	      "risk_level": "none",
  1183	      "discrepancies": []
  1184	    },
  1185	    {
  1186	      "matrix_ids": [
  1187	        "5.1.8.10"
  1188	      ],
  1189	      "contract_ids": [
  1190	        "5.1.8"
  1191	      ],
  1192	      "relationship": "aligned",
  1193	      "legal_topic": "Оплата при техническом сбое сверки",
  1194	      "matrix_standard": "При техническом сбое/невозможности сверки - перечислять суммы по истечении 3 календарных дней",
  1195	      "contract_position": "п.5.1.8: при техническом сбое/невозможности сверки - перечислять по истечении 3 календарных дней",
  1196	      "matrix_evidence": "В случае технического сбоя... перечислять Заказчику суммы Операций, по истечении 3 (трех) календарных дней",
  1197	      "contract_evidence": "В случае технического сбоя при передаче Электронной сверки итогов... перечислять Заказчику суммы Операций, по истечении 3 (трех) календарных дней",
  1198	      "status_reason": "Резервный механизм и срок (3 календарных дня) сохранены.",
  1199	      "risk_level": "none",
  1200	      "discrepancies": []
  1201	    },
  1202	    {
  1203	      "matrix_ids": [
  1204	        "5.1.8.11"
  1205	      ],
  1206	      "contract_ids": [
  1207	        "5.1.9"
  1208	      ],
  1209	      "relationship": "aligned",
  1210	      "legal_topic": "Обработка персональных данных (152-ФЗ)",
  1211	      "matrix_standard": "Обрабатывать ПДн, обеспечивать конфиденциальность и защиту по 152-ФЗ",
  1212	      "contract_position": "п.5.1.9: обработка ПДн, конфиденциальность и защита по 152-ФЗ",
  1213	      "matrix_evidence": "Осуществлять обработку персональных данных... обеспечить конфиденциальность и защиту... в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ",
  1214	      "contract_evidence": "Осуществлять обработку персональных данных... обеспечить конфиденциальность и защиту обрабатываемых персональных данных в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ",
  1215	      "status_reason": "Обязанность по 152-ФЗ сохранена.",
  1216	      "risk_level": "none",
  1217	      "discrepancies": []
  1218	    },
  1219	    {
  1220	      "matrix_ids": [
  1221	        "5.1.8.12"
  1222	      ],
  1223	      "contract_ids": [
  1224	        "5.1.10"
  1225	      ],
  1226	      "relationship": "aligned",
  1227	      "legal_topic": "Перечисление сумм операций",
  1228	      "matrix_standard": "Банк перечисляет Заказчику суммы операций оплаты",
  1229	      "contract_position": "п.5.1.10: Исполнитель перечисляет Заказчику суммы операций оплаты",
  1230	      "matrix_evidence": "Исполнитель... перечисляет Заказчику суммы операций оплаты услуг",
  1231	      "contract_evidence": "Исполнитель в соответствии с контрактом перечисляет Заказчику суммы операций оплаты услуг",
  1232	      "status_reason": "Обязанность сохранена.",
  1233	      "risk_level": "none",
  1234	      "discrepancies": []
  1235	    },
  1236	    {
  1237	      "matrix_ids": [
  1238	        "5.1.8.13"
  1239	      ],
  1240	      "contract_ids": [
  1241	        "Приложение_1_п5"
  1242	      ],
  1243	      "relationship": "aligned",
  1244	      "legal_topic": "Отсутствие платы за возвраты",
  1245	      "matrix_standard": "По операциям возврата плата за проведение расчетов не взимается; ранее удержанная плата не возвращается",
  1246	      "contract_position": "Приложение №1 п.5: по Операциям возврата, Возврат платежа и Реверсивным транзакциям плата не взимается; ранее удержанная плата не возвращается",
  1247	      "matrix_evidence": "по Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается",
  1248	      "contract_evidence": "по Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается. В этом случае плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается",
  1249	      "status_reason": "Условие о невозврате комиссии при возвратах сохранено.",
  1250	      "risk_level": "none",
  1251	      "discrepancies": []
  1252	    },
  1253	    {
  1254	      "matrix_ids": [
  1255	        "5.1.9"
  1256	      ],
  1257	      "contract_ids": [
  1258	        "5.2.9"
  1259	      ],
  1260	      "relationship": "aligned",
  1261	      "legal_topic": "Приостановление авторизации и расторжение",
  1262	      "matrix_standard": "Банк вправе приостановить авторизации и расторгнуть договор при нарушениях (11 оснований)",
  1263	      "contract_position": "п.5.2.9: одностороннее приостановление авторизации и расторжение (11 оснований)",
  1264	      "matrix_evidence": "В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению",
  1265	      "contract_evidence": "В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению Контракта",
  1266	      "status_reason": "Право приостановления и перечень оснований сохранены.",
  1267	      "risk_level": "none",
  1268	      "discrepancies": []
  1269	    },
  1270	    {
  1271	      "matrix_ids": [
  1272	        "5.1.10"
  1273	      ],
  1274	      "contract_ids": [
  1275	        "5.2.10"
  1276	      ],
  1277	      "relationship": "aligned",
  1278	      "legal_topic": "Общее право удержания из сумм к перечислению",
  1279	      "matrix_standard": "Банк удерживает из сумм к перечислению: недействительные операции, ошибочные суммы, возвраты, оспоренные суммы, штрафы",
  1280	      "contract_position": "п.5.2.10: общее право удержания (5 категорий)",
  1281	      "matrix_evidence": "Удерживать из сумм, подлежащих перечислению Заказчику по Контракту, следующие суммы",
  1282	      "contract_evidence": "Удерживать из сумм, подлежащих перечислению Заказчику по Контракту, следующие суммы",
  1283	      "status_reason": "Общее право удержания сохранено.",
  1284	      "risk_level": "none",
  1285	      "discrepancies": []
  1286	    },
  1287	    {
  1288	      "matrix_ids": [
  1289	        "5.1.11"
  1290	      ],
  1291	      "contract_ids": [
  1292	        "5.2.8"
  1293	      ],
  1294	      "relationship": "aligned",
  1295	      "legal_topic": "Запрос документов для функций Банка",
  1296	      "matrix_standard": "Банк вправе требовать документы и сведения для осуществления функций по законодательству",
  1297	      "contract_position": "п.5.2.8: Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций",
  1298	      "matrix_evidence": "Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций",
  1299	      "contract_evidence": "Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства",
  1300	      "status_reason": "Право запроса сохранено.",
  1301	      "risk_level": "none",
  1302	      "discrepancies": []
  1303	    },
  1304	    {
  1305	      "matrix_ids": [
  1306	        "5.1.12"
  1307	      ],
  1308	      "contract_ids": [
  1309	        "5.2.7"
  1310	      ],
  1311	      "relationship": "aligned",
  1312	      "legal_topic": "Направление запросов на email Заказчика",
  1313	      "matrix_standard": "Банк направляет запросы на email Заказчика, указанный в заявлении",
  1314	      "contract_position": "п.5.2.7: направлять запросы на адрес электронной почты заказчика, указанный в заявлении",
  1315	      "matrix_evidence": "В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика",
  1316	      "contract_evidence": "В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении",
  1317	      "status_reason": "Право направления запросов сохранено.",
  1318	      "risk_level": "none",
  1319	      "discrepancies": []
  1320	    },
  1321	    {
  1322	      "matrix_ids": [
  1323	        "5.1.13"
  1324	      ],
  1325	      "contract_ids": [
  1326	        "5.1.1"
  1327	      ],
  1328	      "relationship": "deviation",
  1329	      "legal_topic": "Размещение информации на сайте Банка",
  1330	      "matrix_standard": "Информация (обучающие материалы) размещается на официальном сайте Банка",
  1331	      "contract_position": "п.5.1.1: сайт для обучающих материалов не заполнен (___________________)",
  1332	      "matrix_evidence": "Разместить на сайте: ___________________ обучающие материалы",
  1333	      "contract_evidence": "Разместить на сайте: ___________________ обучающие материалы для прохождения инструктажа",
  1334	      "status_reason": "Адрес сайта с обучающими материалами не заполнен (placeholder).",
  1335	      "risk_level": "low",
  1336	      "discrepancies": [
  1337	        {
  1338	          "type": "missing_element",
  1339	          "description": "Адрес сайта с обучающими материалами не заполнен",
  1340	          "risk": "Низкий риск: адрес может быть заполнен при заключении контракта"
  1341	        }
  1342	      ]
  1343	    },
  1344	    {
  1345	      "matrix_ids": [
  1346	        "5.1.14"
  1347	      ],
  1348	      "contract_ids": [
  1349	        "5.1.1"
  1350	      ],
  1351	      "relationship": "aligned",
  1352	      "legal_topic": "Первичный инструктаж сотрудников",
  1353	      "matrix_standard": "Провести первичный инструктаж работников ТСТ по инструктивным материалам Банка",
  1354	      "contract_position": "п.5.1.1: Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами",
  1355	      "matrix_evidence": "Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком",
  1356	      "contract_evidence": "Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком",
  1357	      "status_reason": "Обязанность первичного инструктажа сохранена.",
  1358	      "risk_level": "none",
  1359	      "discrepancies": []
  1360	    },
  1361	    {
  1362	      "matrix_ids": [
  1363	        "5.1.15"
  1364	      ],
  1365	      "contract_ids": [
  1366	        "7.8"
  1367	      ],
  1368	      "relationship": "aligned",
  1369	      "legal_topic": "Банк не несет ответственности по спорам Заказчик-Покупатель",
  1370	      "matrix_standard": "Банк не несет ответственности по спорам и разногласиям между Покупателями и Предприятием",
  1371	      "contract_position": "п.7.8: Банк не участвует в спорах между Заказчиком и покупателями (имплицитно через механизм возмещения)",
  1372	      "matrix_evidence": "Банк не несет ответственности по спорам и разногласиям между Покупателями и Предприятием",
  1373	      "contract_evidence": "Сторона освобождается от уплаты неустойки... если докажет, что неисполнение... произошло вследствие непреодолимой силы или по вине другой стороны",
  1374	      "status_reason": "Принцип отсутствия ответственности Банка за споры Заказчика с покупателями сохранен через механизм возмещения (п.5.3.19).",
  1375	      "risk_level": "none",
  1376	      "discrepancies": []
  1377	    },
  1378	    {
  1379	      "matrix_ids": [
  1380	        "5.1.16"
  1381	      ],
  1382	      "contract_ids": [
  1383	        "3.2"
  1384	      ],
  1385	      "relationship": "aligned",
  1386	      "legal_topic": "Взимание платы за расчеты",
  1387	      "matrix_standard": "Банк взимает плату за проведение расчетов по операциям",
  1388	      "contract_position": "п.3.2: цена единицы услуги включает расходы Банка в виде процента от суммы операции",
  1389	      "matrix_evidence": "Банк взимает плату за проведение расчетов",
  1390	      "contract_evidence": "Цена единицы услуги включает в себя расходы Исполнителя... в виде процента от суммы каждой Операции оплаты",
  1391	      "status_reason": "Право взимания платы сохранено.",
  1392	      "risk_level": "none",
  1393	      "discrepancies": []
  1394	    },
  1395	    {
  1396	      "matrix_ids": [
  1397	        "5.2.1"
  1398	      ],
  1399	      "contract_ids": [
  1400	        "5.4.1"
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 1400, 'limit': 300}, 'id': 'call_00_O8esjmkG0NrPxxdjYQza6795', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 1700, 'limit': 300}, 'id': 'call_01_FF4gCQfefQcav2aihbpt0186', 'type': 'tool_call'}]
Tool:   1401	      ],
  1402	      "relationship": "aligned",
  1403	      "legal_topic": "Право Заказчика требовать исполнения",
  1404	      "matrix_standard": "Заказчик вправе требовать от Банка надлежащего исполнения обязательств",
  1405	      "contract_position": "п.5.4.1: Требовать от Исполнителя исполнения обязательств надлежащим образом",
  1406	      "matrix_evidence": "Требовать от Исполнителя исполнения обязательств... надлежащим образом",
  1407	      "contract_evidence": "Требовать от Исполнителя исполнения обязательств, предусмотренных контрактом, надлежащим образом",
  1408	      "status_reason": "Право сохранено.",
  1409	      "risk_level": "none",
  1410	      "discrepancies": []
  1411	    },
  1412	    {
  1413	      "matrix_ids": [
  1414	        "5.2.2"
  1415	      ],
  1416	      "contract_ids": [
  1417	        "5.4.2"
  1418	      ],
  1419	      "relationship": "aligned",
  1420	      "legal_topic": "Отказ в приемке некачественных услуг",
  1421	      "matrix_standard": "Заказчик вправе отказать в приемке услуг ненадлежащего качества",
  1422	      "contract_position": "п.5.4.2: Отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества",
  1423	      "matrix_evidence": "Отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества",
  1424	      "contract_evidence": "Отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества",
  1425	      "status_reason": "Право отказа в приемке сохранено.",
  1426	      "risk_level": "none",
  1427	      "discrepancies": []
  1428	    },
  1429	    {
  1430	      "matrix_ids": [
  1431	        "5.2.3"
  1432	      ],
  1433	      "contract_ids": [
  1434	        "5.4.3"
  1435	      ],
  1436	      "relationship": "aligned",
  1437	      "legal_topic": "Односторонний отказ Заказчика (44-ФЗ)",
  1438	      "matrix_standard": "Заказчик вправе принять решение об одностороннем отказе по 44-ФЗ и ГК РФ",
  1439	      "contract_position": "п.5.4.3: Принять решение об одностороннем отказе от исполнения контракта по основаниям 44-ФЗ и ГК РФ",
  1440	      "matrix_evidence": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ",
  1441	      "contract_evidence": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ",
  1442	      "status_reason": "Право сохранено.",
  1443	      "risk_level": "none",
  1444	      "discrepancies": []
  1445	    },
  1446	    {
  1447	      "matrix_ids": [
  1448	        "5.2.4"
  1449	      ],
  1450	      "contract_ids": [
  1451	        "5.4.4"
  1452	      ],
  1453	      "relationship": "aligned",
  1454	      "legal_topic": "Отказ от оплаты некачественных услуг",
  1455	      "matrix_standard": "Заказчик вправе отказаться от оплаты некачественных услуг и потребовать возврата",
  1456	      "contract_position": "п.5.4.4: Отказаться от оплаты услуг ненадлежащего качества, потребовать возврата уплаченных сумм",
  1457	      "matrix_evidence": "Отказаться от оплаты услуг ненадлежащего качества, а если услуги оплачены, потребовать возврата уплаченных сумм",
  1458	      "contract_evidence": "Отказаться от оплаты услуг ненадлежащего качества, а если услуги оплачены, потребовать возврата уплаченных сумм",
  1459	      "status_reason": "Право сохранено.",
  1460	      "risk_level": "none",
  1461	      "discrepancies": []
  1462	    },
  1463	    {
  1464	      "matrix_ids": [
  1465	        "5.2.5"
  1466	      ],
  1467	      "contract_ids": [
  1468	        "5.4.5"
  1469	      ],
  1470	      "relationship": "aligned",
  1471	      "legal_topic": "Ссылка на оплату картами в рекламе",
  1472	      "matrix_standard": "Заказчик вправе ссылаться на оплату картами в рекламных материалах после согласования с Банком",
  1473	      "contract_position": "п.5.4.5: ссылаться на возможность оплаты картами, предварительно согласовав с исполнителем",
  1474	      "matrix_evidence": "Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем",
  1475	      "contract_evidence": "Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем",
  1476	      "status_reason": "Право и условие согласования сохранены.",
  1477	      "risk_level": "none",
  1478	      "discrepancies": []
  1479	    },
  1480	    {
  1481	      "matrix_ids": [
  1482	        "5.2.6"
  1483	      ],
  1484	      "contract_ids": [
  1485	        "5.3.5"
  1486	      ],
  1487	      "relationship": "aligned",
  1488	      "legal_topic": "Требование неустоек с Банка",
  1489	      "matrix_standard": "Заказчик вправе требовать уплаты неустоек при просрочке/неисполнении Банком",
  1490	      "contract_position": "п.5.3.5: Требовать уплаты неустоек (штрафов, пеней) в случае просрочки исполнения Исполнителем",
  1491	      "matrix_evidence": "Требовать уплаты неустоек (штрафов, пеней) в случае просрочки исполнения Исполнителем обязательств",
  1492	      "contract_evidence": "Требовать уплаты неустоек (штрафов, пеней) в случае просрочки исполнения Исполнителем обязательств",
  1493	      "status_reason": "Право требования неустоек сохранено.",
  1494	      "risk_level": "none",
  1495	      "discrepancies": []
  1496	    },
  1497	    {
  1498	      "matrix_ids": [
  1499	        "5.2.7"
  1500	      ],
  1501	      "contract_ids": [
  1502	        "5.3.6"
  1503	      ],
  1504	      "relationship": "aligned",
  1505	      "legal_topic": "Уменьшение оплаты на размер налогов",
  1506	      "matrix_standard": "Заказчик уменьшает сумму оплаты на размер налогов и обязательных платежей",
  1507	      "contract_position": "п.5.3.6: Уменьшить сумму, подлежащую уплате, на размер налогов, сборов и иных обязательных платежей",
  1508	      "matrix_evidence": "Уменьшить сумму, подлежащую уплате... на размер налогов, сборов и иных обязательных платежей",
  1509	      "contract_evidence": "Уменьшить сумму, подлежащую уплате Заказчиком... на размер налогов, сборов и иных обязательных платежей",
  1510	      "status_reason": "Право уменьшения оплаты сохранено.",
  1511	      "risk_level": "none",
  1512	      "discrepancies": []
  1513	    },
  1514	    {
  1515	      "matrix_ids": [
  1516	        "5.2.8"
  1517	      ],
  1518	      "contract_ids": [
  1519	        "5.3.3"
  1520	      ],
  1521	      "relationship": "aligned",
  1522	      "legal_topic": "Контроль за ходом оказания услуг",
  1523	      "matrix_standard": "Заказчик осуществляет контроль за ходом оказания услуг",
  1524	      "contract_position": "п.5.3.3: Осуществлять контроль за ходом оказания услуг Исполнителем",
  1525	      "matrix_evidence": "Осуществлять контроль за ходом оказания услуг",
  1526	      "contract_evidence": "Осуществлять контроль за ходом оказания услуг Исполнителем",
  1527	      "status_reason": "Право контроля сохранено.",
  1528	      "risk_level": "none",
  1529	      "discrepancies": []
  1530	    },
  1531	    {
  1532	      "matrix_ids": [
  1533	        "5.2.9"
  1534	      ],
  1535	      "contract_ids": [
  1536	        "5.3.4"
  1537	      ],
  1538	      "relationship": "aligned",
  1539	      "legal_topic": "Односторонний отказ при несоответствии Банка",
  1540	      "matrix_standard": "Заказчик отказывается от контракта, если Банк не соответствует требованиям закупки",
  1541	      "contract_position": "п.5.3.4: Принять решение об одностороннем отказе, если Исполнитель не соответствует требованиям",
  1542	      "matrix_evidence": "Принять решение об одностороннем отказе от исполнения... если... Исполнитель не соответствует установленным... требованиям",
  1543	      "contract_evidence": "Принять решение об одностороннем отказе от исполнения настоящего контракта в случае, если... Исполнитель не соответствует установленным извещением о проведении закупки требованиям",
  1544	      "status_reason": "Право одностороннего отказа сохранено.",
  1545	      "risk_level": "none",
  1546	      "discrepancies": []
  1547	    },
  1548	    {
  1549	      "matrix_ids": [
  1550	        "5.2.10"
  1551	      ],
  1552	      "contract_ids": [
  1553	        "5.3.1"
  1554	      ],
  1555	      "relationship": "aligned",
  1556	      "legal_topic": "Приемка оказанных услуг",
  1557	      "matrix_standard": "Заказчик принимает оказанные услуги по документу о приемке",
  1558	      "contract_position": "п.5.3.1: Принять оказанные услуги по документу о приемке оказанных услуг",
  1559	      "matrix_evidence": "Принять оказанные услуги по документу о приемке",
  1560	      "contract_evidence": "Принять оказанные услуги по документу о приемке оказанных услуг",
  1561	      "status_reason": "Обязанность приемки сохранена.",
  1562	      "risk_level": "none",
  1563	      "discrepancies": []
  1564	    },
  1565	    {
  1566	      "matrix_ids": [
  1567	        "5.2.12"
  1568	      ],
  1569	      "contract_ids": [
  1570	        "5.9"
  1571	      ],
  1572	      "relationship": "aligned",
  1573	      "legal_topic": "Консультации Банка",
  1574	      "matrix_standard": "Заказчик вправе получать консультации по эксплуатации терминалов",
  1575	      "contract_position": "п.5.9: Заказчик вправе получать консультацию у исполнителя",
  1576	      "matrix_evidence": "Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации",
  1577	      "contract_evidence": "Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций",
  1578	      "status_reason": "Право на консультации сохранено.",
  1579	      "risk_level": "none",
  1580	      "discrepancies": []
  1581	    },
  1582	    {
  1583	      "matrix_ids": [
  1584	        "6.1"
  1585	      ],
  1586	      "contract_ids": [
  1587	        "3.2"
  1588	      ],
  1589	      "relationship": "aligned",
  1590	      "legal_topic": "Плата за услуги в виде процента от операций",
  1591	      "matrix_standard": "Плата за услуги Банка в виде процента от суммы каждой операции оплаты",
  1592	      "contract_position": "п.3.2: цена единицы услуги включает расходы в виде процента от суммы каждой операции оплаты",
  1593	      "matrix_evidence": "стоимость услуг Банка за выполнение расчетов по операциям оплаты в виде процента от суммы каждой операции оплаты",
  1594	      "contract_evidence": "Цена единицы услуги включает в себя расходы Исполнителя... в виде процента от суммы каждой Операции оплаты",
  1595	      "status_reason": "Принцип расчета платы (процент от операции) сохранен.",
  1596	      "risk_level": "none",
  1597	      "discrepancies": []
  1598	    },
  1599	    {
  1600	      "matrix_ids": [
  1601	        "6.2"
  1602	      ],
  1603	      "contract_ids": [
  1604	        "8.3.2"
  1605	      ],
  1606	      "relationship": "aligned",
  1607	      "legal_topic": "УПД и закрывающие документы",
  1608	      "matrix_standard": "УПД (универсальный передаточный документ) как документ о приемке",
  1609	      "contract_position": "п.8.3.2: счет-фактура, акт о перечислении сумм, счет ф.363",
  1610	      "matrix_evidence": "УПД - это универсальный передаточный документ (документ о приёмке, документ на оплату)",
  1611	      "contract_evidence": "К документу о приемке... Исполнитель прилагает... счет-фактуру (при наличии), акт о перечислении Заказчику сумм операций по картам и счет ф.363 на оплату услуг",
  1612	      "status_reason": "Механизм закрывающих документов сохранен через 44-ФЗ процедуру приемки.",
  1613	      "risk_level": "none",
  1614	      "discrepancies": []
  1615	    },
  1616	    {
  1617	      "matrix_ids": [
  1618	        "6.3"
  1619	      ],
  1620	      "contract_ids": [
  1621	        "3.1.1"
  1622	      ],
  1623	      "relationship": "aligned",
  1624	      "legal_topic": "Тарифы Банка",
  1625	      "matrix_standard": "Тарифы Банка указаны в спецификации / на сайте Банка",
  1626	      "contract_position": "п.3.1.1: Цена за единицу услуги указана в спецификации (Приложение №1)",
  1627	      "matrix_evidence": "Тарифы Банка... в виде процента от суммы каждой операции оплаты и размера платы за сервисное обслуживание",
  1628	      "contract_evidence": "Цена за единицу услуги указана в спецификации (Приложение № 1)",
  1629	      "status_reason": "Тарифы определены через спецификацию.",
  1630	      "risk_level": "none",
  1631	      "discrepancies": []
  1632	    },
  1633	    {
  1634	      "matrix_ids": [
  1635	        "6.4"
  1636	      ],
  1637	      "contract_ids": [
  1638	        "4.5"
  1639	      ],
  1640	      "relationship": "aligned",
  1641	      "legal_topic": "Ежемесячная оплата услуг",
  1642	      "matrix_standard": "Оплата услуг производится ежемесячно",
  1643	      "contract_position": "п.4.5: оплата... производится ежемесячно",
  1644	      "matrix_evidence": "Оплата оказанной услуги... производится ежемесячно",
  1645	      "contract_evidence": "Срок оплаты оказанных услуг... производится ежемесячно",
  1646	      "status_reason": "Периодичность оплаты сохранена.",
  1647	      "risk_level": "none",
  1648	      "discrepancies": []
  1649	    },
  1650	    {
  1651	      "matrix_ids": [
  1652	        "6.5"
  1653	      ],
  1654	      "contract_ids": [
  1655	        "4.5"
  1656	      ],
  1657	      "relationship": "aligned",
  1658	      "legal_topic": "Срок оплаты - 7 рабочих дней",
  1659	      "matrix_standard": "Оплата в течение 7 рабочих дней с даты подписания документа о приемке",
  1660	      "contract_position": "п.4.5: не более 7 рабочих дней с даты подписания Заказчиком документа о приемке",
  1661	      "matrix_evidence": "Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания... документа о приемке",
  1662	      "contract_evidence": "Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке",
  1663	      "status_reason": "Срок оплаты (7 рабочих дней) сохранен.",
  1664	      "risk_level": "none",
  1665	      "discrepancies": []
  1666	    },
  1667	    {
  1668	      "matrix_ids": [
  1669	        "6.6"
  1670	      ],
  1671	      "contract_ids": [
  1672	        "4.5.1"
  1673	      ],
  1674	      "relationship": "aligned",
  1675	      "legal_topic": "Оплата за ноябрь до 30 декабря",
  1676	      "matrix_standard": "Услуги ноября оплачиваются не позднее 30 декабря",
  1677	      "contract_position": "п.4.5.1: Услуги, оказанные в ноябре оплачиваются... не позднее 30 декабря 2025 года",
  1678	      "matrix_evidence": "Услуги, оказанные в ноябре оплачиваются в срок... не позднее 30 декабря",
  1679	      "contract_evidence": "Услуги, оказанные в ноябре оплачиваются в срок не позднее 7 рабочих дней... но не позднее 30 декабря 2025 года",
  1680	      "status_reason": "Предельный срок оплаты за ноябрь сохранен.",
  1681	      "risk_level": "none",
  1682	      "discrepancies": []
  1683	    },
  1684	    {
  1685	      "matrix_ids": [
  1686	        "6.7"
  1687	      ],
  1688	      "contract_ids": [
  1689	        "4.4"
  1690	      ],
  1691	      "relationship": "aligned",
  1692	      "legal_topic": "Оплата платежным поручением",
  1693	      "matrix_standard": "Оплата по безналичному расчету платежным поручением на счет Банка",
  1694	      "contract_position": "п.4.4: Оплата по контракту осуществляется по безналичному расчёту платёжным поручением",
  1695	      "matrix_evidence": "Оплата по контракту осуществляется по безналичному расчёту платёжным поручением",
  1696	      "contract_evidence": "Оплата по контракту осуществляется по безналичному расчёту платёжным поручением путём перечисления Заказчиком денежных средств на счёт Исполнителя",
  1697	      "status_reason": "Способ оплаты сохранен.",
  1698	      "risk_level": "none",
  1699	      "discrepancies": []
  1700	    },
Tool:   1701	    {
  1702	      "matrix_ids": [
  1703	        "6.8"
  1704	      ],
  1705	      "contract_ids": [
  1706	        "4.4"
  1707	      ],
  1708	      "relationship": "aligned",
  1709	      "legal_topic": "Уведомление о смене счета Банка",
  1710	      "matrix_standard": "Банк уведомляет о смене счета в 2-дневный срок",
  1711	      "contract_position": "п.4.4: обязан в двухдневный срок в письменной форме сообщить об изменении счета",
  1712	      "matrix_evidence": "В случае изменения счета Исполнителя он обязан в двухдневный срок... сообщить об этом Заказчику",
  1713	      "contract_evidence": "В случае изменения счета Исполнителя он обязан в двухдневный срок в письменной форме сообщить об этом Заказчику",
  1714	      "status_reason": "Срок уведомления (2 дня) сохранен.",
  1715	      "risk_level": "none",
  1716	      "discrepancies": []
  1717	    },
  1718	    {
  1719	      "matrix_ids": [
  1720	        "6.9"
  1721	      ],
  1722	      "contract_ids": [
  1723	        "4.4"
  1724	      ],
  1725	      "relationship": "aligned",
  1726	      "legal_topic": "Оплата по факту, не более макс. цены",
  1727	      "matrix_standard": "Оплата по цене единицы исходя из фактического объема, не более максимальной цены контракта",
  1728	      "contract_position": "п.4.4: Оплата оказанной услуги осуществляется по цене единицы услуги исходя из объема фактически оказанной услуги, но в размере, не превышающем максимального значения цены контракта",
  1729	      "matrix_evidence": "Оплата оказанной услуги осуществляется по цене единицы услуги исходя из объема фактически оказанной услуги, но в размере, не превышающем максимального значения цены контракта",
  1730	      "contract_evidence": "Оплата оказанной услуги осуществляется по цене единицы услуги исходя из объема фактически оказанной услуги, но в размере, не превышающем максимального значения цены контракта",
  1731	      "status_reason": "Принцип оплаты по факту с потолком цены сохранен.",
  1732	      "risk_level": "none",
  1733	      "discrepancies": []
  1734	    },
  1735	    {
  1736	      "matrix_ids": [
  1737	        "6.10"
  1738	      ],
  1739	      "contract_ids": [
  1740	        "3.1"
  1741	      ],
  1742	      "relationship": "aligned",
  1743	      "legal_topic": "Максимальная цена контракта",
  1744	      "matrix_standard": "Максимальное значение цены контракта",
  1745	      "contract_position": "п.3.1: Максимальное значение цены контракта составляет 1 900 000,00 рублей",
  1746	      "matrix_evidence": "Максимальное значение цены контракта",
  1747	      "contract_evidence": "Максимальное значение цены контракта (стоимость услуг) составляет 1 900 000,00 рублей",
  1748	      "status_reason": "Максимальная цена установлена.",
  1749	      "risk_level": "none",
  1750	      "discrepancies": []
  1751	    },
  1752	    {
  1753	      "matrix_ids": [
  1754	        "6.11"
  1755	      ],
  1756	      "contract_ids": [
  1757	        "3.1.1"
  1758	      ],
  1759	      "relationship": "aligned",
  1760	      "legal_topic": "Цена единицы услуги в спецификации",
  1761	      "matrix_standard": "Цена за единицу услуги указана в спецификации",
  1762	      "contract_position": "п.3.1.1: Цена за единицу услуги указана в спецификации (Приложение № 1)",
  1763	      "matrix_evidence": "Цена за единицу услуги указана в спецификации",
  1764	      "contract_evidence": "Цена за единицу услуги указана в спецификации (Приложение № 1)",
  1765	      "status_reason": "Отсылка к спецификации сохранена.",
  1766	      "risk_level": "none",
  1767	      "discrepancies": []
  1768	    },
  1769	    {
  1770	      "matrix_ids": [
  1771	        "6.12"
  1772	      ],
  1773	      "contract_ids": [
  1774	        "3.3"
  1775	      ],
  1776	      "relationship": "aligned",
  1777	      "legal_topic": "Применение правил 44-ФЗ к цене",
  1778	      "matrix_standard": "Положения о цене контракта применяются с учетом 44-ФЗ",
  1779	      "contract_position": "п.3.3: Положения... касающиеся применения цены контракта... применяются... если Федеральным законом №44-ФЗ не установлено иное",
  1780	      "matrix_evidence": "Положения настоящего Контракта, касающиеся применения цены контракта... применяются... если Федеральным законом №44-ФЗ не установлено иное",
  1781	      "contract_evidence": "Положения настоящего Контракта, касающиеся применения цены контракта... применяются... если Федеральным законом №44-ФЗ не установлено иное",
  1782	      "status_reason": "Оговорка о приоритете 44-ФЗ сохранена.",
  1783	      "risk_level": "none",
  1784	      "discrepancies": []
  1785	    },
  1786	    {
  1787	      "matrix_ids": [
  1788	        "6.13"
  1789	      ],
  1790	      "contract_ids": [
  1791	        "4.1"
  1792	      ],
  1793	      "relationship": "aligned",
  1794	      "legal_topic": "Срок оказания услуг",
  1795	      "matrix_standard": "Оказание услуг с 01.03.2025 по 30.11.2025 или до исчерпания цены",
  1796	      "contract_position": "п.4.1: с 01 марта 2025 по 30 ноября 2025 или до исчерпания цены",
  1797	      "matrix_evidence": "Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта",
  1798	      "contract_evidence": "Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта",
  1799	      "status_reason": "Период оказания услуг сохранен.",
  1800	      "risk_level": "none",
  1801	      "discrepancies": []
  1802	    },
  1803	    {
  1804	      "matrix_ids": [
  1805	        "6.14"
  1806	      ],
  1807	      "contract_ids": [
  1808	        "4.2"
  1809	      ],
  1810	      "relationship": "aligned",
  1811	      "legal_topic": "Наличие лицензии Банка",
  1812	      "matrix_standard": "Исполнитель должен иметь лицензию на банковские операции",
  1813	      "contract_position": "п.4.2: Исполнитель должен иметь лицензию на осуществление банковских операций",
  1814	      "matrix_evidence": "Исполнитель должен иметь лицензию на осуществление банковских операций",
  1815	      "contract_evidence": "Исполнитель должен иметь лицензию на осуществление банковских операций, соответствующих виду предмета контракта",
  1816	      "status_reason": "Требование лицензии сохранено.",
  1817	      "risk_level": "none",
  1818	      "discrepancies": []
  1819	    },
  1820	    {
  1821	      "matrix_ids": [
  1822	        "6.15"
  1823	      ],
  1824	      "contract_ids": [
  1825	        "4.3"
  1826	      ],
  1827	      "relationship": "aligned",
  1828	      "legal_topic": "Адреса ТСТ в Приложении №1",
  1829	      "matrix_standard": "Оказание услуг по адресам ТСТ, перечень в Приложении №1",
  1830	      "contract_position": "п.4.3: Перечень ТСТ указан в Приложении № 1",
  1831	      "matrix_evidence": "Оказание услуг осуществляется Исполнителем по адресу местоположения точек приема... Перечень ТСТ указан в Приложении № 1",
  1832	      "contract_evidence": "Оказание услуг осуществляется Исполнителем по адресу местоположения точек приема к оплате пластиковых карт (эквайринга) торгово-сервисных точек (ТСТ). Перечень ТСТ указан в Приложении № 1",
  1833	      "status_reason": "Адреса ТСТ определены в Приложении №1.",
  1834	      "risk_level": "none",
  1835	      "discrepancies": []
  1836	    },
  1837	    {
  1838	      "matrix_ids": [
  1839	        "6.16"
  1840	      ],
  1841	      "contract_ids": [
  1842	        "4.3"
  1843	      ],
  1844	      "relationship": "aligned",
  1845	      "legal_topic": "Регистрация ТСТ после заключения контракта",
  1846	      "matrix_standard": "Регистрация нового ТСТ после заключения контракта",
  1847	      "contract_position": "п.4.3: В целях регистрации нового ТСТ... Заказчик после заключения контракта предоставляет Исполнителю заявление",
  1848	      "matrix_evidence": "В целях регистрации нового ТСТ в рамках настоящего контракта Заказчик после заключения контракта предоставляет Исполнителю заявление",
  1849	      "contract_evidence": "В целях регистрации нового ТСТ в рамках настоящего контракта Заказчик после заключения контракта предоставляет Исполнителю заявление",
  1850	      "status_reason": "Процедура регистрации ТСТ сохранена.",
  1851	      "risk_level": "none",
  1852	      "discrepancies": []
  1853	    },
  1854	    {
  1855	      "matrix_ids": [
  1856	        "6.17"
  1857	      ],
  1858	      "contract_ids": [
  1859	        "4.2"
  1860	      ],
  1861	      "relationship": "aligned",
  1862	      "legal_topic": "Исключение из требования лицензии",
  1863	      "matrix_standard": "Исключение: ч.9 ст.13 395-ФЗ и закон о НПС",
  1864	      "contract_position": "п.4.2: за исключением случая, указанного в части 9 статьи 13 Федерального закона от 02.12.1990 № 395-1",
  1865	      "matrix_evidence": "за исключением случая, указанного в части 9 статьи 13 Федерального закона от 02.12.1990 № 395-1",
  1866	      "contract_evidence": "за исключением случая, указанного в части 9 статьи 13 Федерального закона от 02.12.1990 № 395-1 «О банках и банковской деятельности» и в Федеральном законе «О национальной платежной системе»",
  1867	      "status_reason": "Исключение сохранено.",
  1868	      "risk_level": "none",
  1869	      "discrepancies": []
  1870	    },
  1871	    {
  1872	      "matrix_ids": [
  1873	        "6.18"
  1874	      ],
  1875	      "contract_ids": [
  1876	        "4.2"
  1877	      ],
  1878	      "relationship": "aligned",
  1879	      "legal_topic": "Соответствие требованиям извещения о закупке",
  1880	      "matrix_standard": "Исполнитель должен соответствовать требованиям извещения о закупке",
  1881	      "contract_position": "п.4.2: если... извещением о проведении закупки предусмотрены требования... Исполнитель должен соответствовать таким требованиям",
  1882	      "matrix_evidence": "В случае если действующим законодательством... и извещением о проведении закупки предусмотрены требования... Исполнитель должен соответствовать таким требованиям",
  1883	      "contract_evidence": "В случае если действующим законодательством Российской Федерации и извещением о проведении закупки предусмотрены требования... Исполнитель должен соответствовать таким требованиям",
  1884	      "status_reason": "Требование соответствия сохранено.",
  1885	      "risk_level": "none",
  1886	      "discrepancies": []
  1887	    },
  1888	    {
  1889	      "matrix_ids": [
  1890	        "6.20"
  1891	      ],
  1892	      "contract_ids": [
  1893	        "Приложение_1_п5"
  1894	      ],
  1895	      "relationship": "aligned",
  1896	      "legal_topic": "Отсутствие повторной комиссии при возвратах",
  1897	      "matrix_standard": "Банк не берет новую комиссию при возврате; первоначальная комиссия не возвращается",
  1898	      "contract_position": "Приложение №1 п.5: плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается",
  1899	      "matrix_evidence": "Банк не берёт новую комиссию, а так же, что первоначальная комиссия не возвращается",
  1900	      "contract_evidence": "плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается",
  1901	      "status_reason": "Условие о невозврате комиссии сохранено.",
  1902	      "risk_level": "none",
  1903	      "discrepancies": []
  1904	    },
  1905	    {
  1906	      "matrix_ids": [
  1907	        "6.21"
  1908	      ],
  1909	      "contract_ids": [
  1910	        "3.1"
  1911	      ],
  1912	      "relationship": "aligned",
  1913	      "legal_topic": "Отсутствие конкретной цены не является противоречием",
  1914	      "matrix_standard": "Отсутствие конкретной цены не является противоречием (определяется спецификацией)",
  1915	      "contract_position": "п.3.1: максимальная цена 1 900 000 руб.; конкретная цена единицы - в спецификации",
  1916	      "matrix_evidence": "Отсутствие конкретнной цены не является противоречием",
  1917	      "contract_evidence": "Максимальное значение цены контракта... составляет 1 900 000,00 рублей",
  1918	      "status_reason": "Цена определена через максимальное значение и спецификацию.",
  1919	      "risk_level": "none",
  1920	      "discrepancies": []
  1921	    },
  1922	    {
  1923	      "matrix_ids": [
  1924	        "7.1"
  1925	      ],
  1926	      "contract_ids": [
  1927	        "7.1"
  1928	      ],
  1929	      "relationship": "aligned",
  1930	      "legal_topic": "Ответственность по законодательству РФ",
  1931	      "matrix_standard": "Ответственность по действующему законодательству РФ",
  1932	      "contract_position": "п.7.1: За неисполнение или ненадлежащее исполнение обязательств... Стороны несут ответственность в соответствии с действующим законодательством РФ",
  1933	      "matrix_evidence": "За неисполнение или ненадлежащее исполнение обязательств по Контракту Стороны несут ответственность в соответствии с действующим законодательством",
  1934	      "contract_evidence": "За неисполнение или ненадлежащее исполнение обязательств по Контракту Стороны несут ответственность в соответствии с действующим законодательством Российской Федерации",
  1935	      "status_reason": "Общий принцип ответственности сохранен.",
  1936	      "risk_level": "none",
  1937	      "discrepancies": []
  1938	    },
  1939	    {
  1940	      "matrix_ids": [
  1941	        "7.2"
  1942	      ],
  1943	      "contract_ids": [
  1944	        "7.3"
  1945	      ],
  1946	      "relationship": "aligned",
  1947	      "legal_topic": "Пени за просрочку Заказчика",
  1948	      "matrix_standard": "Пеня 1/300 ключевой ставки ЦБ РФ за каждый день просрочки Заказчика",
  1949	      "contract_position": "п.7.3: пеня 1/300 ключевой ставки ЦБ РФ за каждый день просрочки Заказчика",
  1950	      "matrix_evidence": "Пеня начисляется за каждый день просрочки... в размере 1/300 действующей на день уплаты пеней ключевой ставки Центрального банка Российской Федерации",
  1951	      "contract_evidence": "Пеня начисляется за каждый день просрочки исполнения Заказчиком обязательства... в размере 1/300 действующей на день уплаты пеней ключевой ставки Центрального банка Российской Федерации",
  1952	      "status_reason": "Размер пени (1/300) сохранен.",
  1953	      "risk_level": "none",
  1954	      "discrepancies": []
  1955	    },
  1956	    {
  1957	      "matrix_ids": [
  1958	        "7.3"
  1959	      ],
  1960	      "contract_ids": [
  1961	        "7.4",
  1962	        "7.4.1"
  1963	      ],
  1964	      "relationship": "aligned",
  1965	      "legal_topic": "Штрафы Заказчика по ПП 1042",
  1966	      "matrix_standard": "Штрафы за ненадлежащее исполнение Заказчиком по ПП 1042",
  1967	      "contract_position": "п.7.4, 7.4.1: штрафы по ПП 1042 (1000 руб. при цене до 3 млн.)",
  1968	      "matrix_evidence": "Размер штрафа... устанавливается в соответствии с постановлением Правительства РФ от 30.08.2017 № 1042",
  1969	      "contract_evidence": "Размер штрафа... устанавливается в соответствии с постановлением Правительства РФ от 30.08.2017 № 1042",
  1970	      "status_reason": "Штрафы по ПП 1042 сохранены.",
  1971	      "risk_level": "none",
  1972	      "discrepancies": []
  1973	    },
  1974	    {
  1975	      "matrix_ids": [
  1976	        "7.4"
  1977	      ],
  1978	      "contract_ids": [
  1979	        "7.6"
  1980	      ],
  1981	      "relationship": "aligned",
  1982	      "legal_topic": "Пени за просрочку Банка",
  1983	      "matrix_standard": "Пеня 1/300 ключевой ставки ЦБ РФ за каждый день просрочки Банка",
  1984	      "contract_position": "п.7.6: пеня 1/300 ключевой ставки ЦБ РФ за каждый день просрочки Исполнителя",
  1985	      "matrix_evidence": "Пеня начисляется за каждый день просрочки исполнения Исполнителем обязательства... в размере 1/300 действующей на дату уплаты пеней ключевой ставки",
  1986	      "contract_evidence": "Пеня начисляется за каждый день просрочки исполнения Исполнителем обязательства... в размере 1/300 действующей на дату уплаты пеней ключевой ставки Центрального банка Российской Федерации",
  1987	      "status_reason": "Размер пени (1/300) сохранен.",
  1988	      "risk_level": "none",
  1989	      "discrepancies": []
  1990	    },
  1991	    {
  1992	      "matrix_ids": [
  1993	        "7.5"
  1994	      ],
  1995	      "contract_ids": [
  1996	        "7.7",
  1997	        "7.7.1"
  1998	      ],
  1999	      "relationship": "aligned",
  2000	      "legal_topic": "Штрафы Банка по ПП 1042",
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 2000, 'limit': 300}, 'id': 'call_00_Uqee0I6VrdpCVrzuOtpb6005', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 2300, 'limit': 300}, 'id': 'call_01_ncmvkDupqV59frqnIOYc7103', 'type': 'tool_call'}]
Tool:   2001	      "matrix_standard": "Штрафы за неисполнение Банком по ПП 1042",
  2002	      "contract_position": "п.7.7, 7.7.1: штрафы по ПП 1042 (10% цены контракта при цене до 3 млн.)",
  2003	      "matrix_evidence": "Размер штрафа... устанавливается в соответствии с Постановлением № 1042",
  2004	      "contract_evidence": "Размер штрафа... устанавливается в соответствии с Постановлением № 1042",
  2005	      "status_reason": "Штрафы по ПП 1042 сохранены.",
  2006	      "risk_level": "none",
  2007	      "discrepancies": []
  2008	    },
  2009	    {
  2010	      "matrix_ids": [
  2011	        "7.6"
  2012	      ],
  2013	      "contract_ids": [
  2014	        "7.10",
  2015	        "7.11"
  2016	      ],
  2017	      "relationship": "aligned",
  2018	      "legal_topic": "Общий потолок штрафов - цена контракта",
  2019	      "matrix_standard": "Общая сумма штрафов не может превышать цену контракта",
  2020	      "contract_position": "п.7.10, 7.11: общая сумма штрафов не может превышать цену контракта",
  2021	      "matrix_evidence": "Общая сумма начисленных штрафов... не может превышать цену контракта",
  2022	      "contract_evidence": "Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств... не может превышать цену Контракта",
  2023	      "status_reason": "Потолок штрафов сохранен.",
  2024	      "risk_level": "none",
  2025	      "discrepancies": []
  2026	    },
  2027	    {
  2028	      "matrix_ids": [
  2029	        "7.7"
  2030	      ],
  2031	      "contract_ids": [
  2032	        "7.9"
  2033	      ],
  2034	      "relationship": "aligned",
  2035	      "legal_topic": "Неустойка не освобождает от исполнения",
  2036	      "matrix_standard": "Применение неустойки не освобождает от исполнения обязательств",
  2037	      "contract_position": "п.7.9: Применение неустойки (штрафа, пени) не освобождает Стороны от исполнения обязательств по Контракту",
  2038	      "matrix_evidence": "Применение неустойки (штрафа, пени) не освобождает Стороны от исполнения обязательств",
  2039	      "contract_evidence": "Применение неустойки (штрафа, пени) не освобождает Стороны от исполнения обязательств по Контракту",
  2040	      "status_reason": "Принцип сохранен.",
  2041	      "risk_level": "none",
  2042	      "discrepancies": []
  2043	    },
  2044	    {
  2045	      "matrix_ids": [
  2046	        "7.8"
  2047	      ],
  2048	      "contract_ids": [
  2049	        "5.3.19"
  2050	      ],
  2051	      "relationship": "aligned",
  2052	      "legal_topic": "Банк не отвечает по спорам Заказчик-Покупатель",
  2053	      "matrix_standard": "Банк не несет ответственности по спорам между Покупателями и Предприятием",
  2054	      "contract_position": "п.5.3.19: Заказчик возмещает Банку все суммы по спорам с покупателями",
  2055	      "matrix_evidence": "Банк (Исполнитель) не несет ответственности по спорам и разногласиям между Покупателями и Предприятием",
  2056	      "contract_evidence": "Возместить Исполнителю в полном объеме... средства... ставшим предметом каких-либо споров и разногласий",
  2057	      "status_reason": "Защита Банка от споров Заказчика с покупателями реализована через механизм возмещения.",
  2058	      "risk_level": "none",
  2059	      "discrepancies": []
  2060	    },
  2061	    {
  2062	      "matrix_ids": [
  2063	        "7.9"
  2064	      ],
  2065	      "contract_ids": [
  2066	        "7.1",
  2067	        "9.1"
  2068	      ],
  2069	      "relationship": "aligned",
  2070	      "legal_topic": "Освобождение от ответственности при форс-мажоре",
  2071	      "matrix_standard": "Сторона освобождается от ответственности при непреодолимой силе или вине другой стороны",
  2072	      "contract_position": "п.7.1: освобождение при непреодолимой силе или вине другой стороны; п.9.1: обстоятельства непреодолимой силы",
  2073	      "matrix_evidence": "Сторона освобождается от уплаты неустойки... если докажет, что неисполнение... произошло вследствие непреодолимой силы или по вине другой стороны",
  2074	      "contract_evidence": "Сторона освобождается от уплаты неустойки (штрафа, пени), если докажет, что неисполнение или ненадлежащее исполнение обязательства... произошло вследствие непреодолимой силы или по вине другой стороны",
  2075	      "status_reason": "Основания освобождения сохранены.",
  2076	      "risk_level": "none",
  2077	      "discrepancies": []
  2078	    },
  2079	    {
  2080	      "matrix_ids": [
  2081	        "7.10"
  2082	      ],
  2083	      "contract_ids": [
  2084	        "9.2"
  2085	      ],
  2086	      "relationship": "aligned",
  2087	      "legal_topic": "Уведомление о форс-мажоре в течение 5 дней",
  2088	      "matrix_standard": "Уведомить другую сторону о форс-мажоре не позднее 5 дней",
  2089	      "contract_position": "п.9.2: оповестить другую Сторону не позднее пяти дней с момента возникновения",
  2090	      "matrix_evidence": "обязана оповестить другую Сторону не позднее пяти дней с момента возникновения таких обстоятельств",
  2091	      "contract_evidence": "она обязана оповестить другую Сторону не позднее пяти дней с момента возникновения таких обстоятельств",
  2092	      "status_reason": "Срок уведомления (5 дней) сохранен.",
  2093	      "risk_level": "none",
  2094	      "discrepancies": []
  2095	    },
  2096	    {
  2097	      "matrix_ids": [
  2098	        "7.11"
  2099	      ],
  2100	      "contract_ids": [
  2101	        "9.2"
  2102	      ],
  2103	      "relationship": "aligned",
  2104	      "legal_topic": "Право расторжения при форс-мажоре > 1 месяца",
  2105	      "matrix_standard": "Если форс-мажор длится более 1 месяца - право расторгнуть контракт",
  2106	      "contract_position": "п.9.2: если обстоятельства длятся более одного календарного месяца Стороны праве расторгнуть настоящий контракт",
  2107	      "matrix_evidence": "В случае если такие обстоятельства длятся более одного календарного месяца Стороны праве расторгнуть",
  2108	      "contract_evidence": "В случае если такие обстоятельства длятся более одного календарного месяца Стороны праве расторгнуть настоящий контракт по соглашению Сторон",
  2109	      "status_reason": "Право расторжения при длительном форс-мажоре сохранено.",
  2110	      "risk_level": "none",
  2111	      "discrepancies": []
  2112	    },
  2113	    {
  2114	      "matrix_ids": [
  2115	        "7.12"
  2116	      ],
  2117	      "contract_ids": [
  2118	        "9.3"
  2119	      ],
  2120	      "relationship": "aligned",
  2121	      "legal_topic": "Документальное подтверждение форс-мажора",
  2122	      "matrix_standard": "Сторона, ссылающаяся на форс-мажор, обязана представить документальное подтверждение",
  2123	      "contract_position": "п.9.3: сторона, ссылающаяся на эти обстоятельства, обязана представить документальное подтверждение их наступления",
  2124	      "matrix_evidence": "сторона, ссылающаяся на эти обстоятельства, обязана представить документальное подтверждение их наступления",
  2125	      "contract_evidence": "сторона, ссылающаяся на эти обстоятельства, обязана представить документальное подтверждение их наступления",
  2126	      "status_reason": "Требование документального подтверждения сохранено.",
  2127	      "risk_level": "none",
  2128	      "discrepancies": []
  2129	    },
  2130	    {
  2131	      "matrix_ids": [
  2132	        "7.13"
  2133	      ],
  2134	      "contract_ids": [
  2135	        "7.8"
  2136	      ],
  2137	      "relationship": "aligned",
  2138	      "legal_topic": "Обмен документами через ЕИС при ответственности",
  2139	      "matrix_standard": "Обмен документами при применении мер ответственности через ЕИС с УКЭП",
  2140	      "contract_position": "п.7.8: обмен документами при применении мер ответственности с использованием ЕИС путем направления электронных уведомлений",
  2141	      "matrix_evidence": "В случае обмена документами при применении мер ответственности... такой обмен осуществляется с использованием ЕИС",
  2142	      "contract_evidence": "В случае обмена документами при применении мер ответственности и совершении иных действий в связи с нарушением... такой обмен осуществляется с использованием ЕИС",
  2143	      "status_reason": "Процедура ЕИС для ответственности сохранена.",
  2144	      "risk_level": "none",
  2145	      "discrepancies": []
  2146	    },
  2147	    {
  2148	      "matrix_ids": [
  2149	        "7.14"
  2150	      ],
  2151	      "contract_ids": [
  2152	        "7.12"
  2153	      ],
  2154	      "relationship": "aligned",
  2155	      "legal_topic": "Только фактический ущерб при одностороннем отказе",
  2156	      "matrix_standard": "При одностороннем отказе - возмещение только фактического ущерба сверх неустоек",
  2157	      "contract_position": "п.7.12: другая Сторона вправе потребовать возмещения только фактически понесенного ущерба... сверх начисленных неустоек",
  2158	      "matrix_evidence": "В случае расторжения Контракта в связи с односторонним отказом... другая Сторона вправе потребовать возмещения только фактически понесенного ущерба",
  2159	      "contract_evidence": "В случае расторжения Контракта в связи с односторонним отказом Стороны от исполнения Контракта другая Сторона вправе потребовать возмещения только фактически понесенного ущерба",
  2160	      "status_reason": "Ограничение возмещения фактическим ущербом сохранено.",
  2161	      "risk_level": "none",
  2162	      "discrepancies": []
  2163	    },
  2164	    {
  2165	      "matrix_ids": [
  2166	        "7.15"
  2167	      ],
  2168	      "contract_ids": [
  2169	        "8.2"
  2170	      ],
  2171	      "relationship": "aligned",
  2172	      "legal_topic": "Ответственность Банка за ущерб от услуг",
  2173	      "matrix_standard": "Банк несет ответственность за повреждения, возникшие вследствие оказания услуг",
  2174	      "contract_position": "п.8.2: Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг его специалистами",
  2175	      "matrix_evidence": "Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг",
  2176	      "contract_evidence": "Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг его специалистами",
  2177	      "status_reason": "Ответственность Банка за ущерб сохранена.",
  2178	      "risk_level": "none",
  2179	      "discrepancies": []
  2180	    },
  2181	    {
  2182	      "matrix_ids": [
  2183	        "7.16"
  2184	      ],
  2185	      "contract_ids": [
  2186	        "7.5"
  2187	      ],
  2188	      "relationship": "aligned",
  2189	      "legal_topic": "Право Заказчика требовать неустойки с Банка",
  2190	      "matrix_standard": "Заказчик направляет требование об уплате неустоек при нарушении Банком",
  2191	      "contract_position": "п.7.5: Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней)",
  2192	      "matrix_evidence": "Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней)",
  2193	      "contract_evidence": "Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней)",
  2194	      "status_reason": "Право требования неустоек сохранено.",
  2195	      "risk_level": "none",
  2196	      "discrepancies": []
  2197	    },
  2198	    {
  2199	      "matrix_ids": [
  2200	        "7.17"
  2201	      ],
  2202	      "contract_ids": [
  2203	        "7.1"
  2204	      ],
  2205	      "relationship": "aligned",
  2206	      "legal_topic": "Отсутствие сужения ответственности",
  2207	      "matrix_standard": "В договоре не должно быть сужения ответственности",
  2208	      "contract_position": "п.7.1: ответственность по действующему законодательству РФ (не сужена)",
  2209	      "matrix_evidence": "Важно, чтобы в договоре не было сужения ответственности",
  2210	      "contract_evidence": "Стороны несут ответственность в соответствии с действующим законодательством Российской Федерации",
  2211	      "status_reason": "Ответственность не сужена - применяется общее законодательство РФ.",
  2212	      "risk_level": "none",
  2213	      "discrepancies": []
  2214	    },
  2215	    {
  2216	      "matrix_ids": [
  2217	        "8.1"
  2218	      ],
  2219	      "contract_ids": [
  2220	        "8.1"
  2221	      ],
  2222	      "relationship": "aligned",
  2223	      "legal_topic": "Гарантия качества услуг",
  2224	      "matrix_standard": "Банк гарантирует качество услуг в течение срока, установленного НПА",
  2225	      "contract_position": "п.8.1: Исполнитель гарантирует Заказчику качество оказанных услуг... в течение всего срока, установленного нормативно-правовыми актами РФ",
  2226	      "matrix_evidence": "Исполнитель гарантирует Заказчику качество оказанных услуг",
  2227	      "contract_evidence": "Исполнитель гарантирует Заказчику качество оказанных услуг, предусмотренных требованиями Приложения №1 в течение всего срока, установленного нормативно-правовыми актами Российской Федерации",
  2228	      "status_reason": "Гарантия качества сохранена.",
  2229	      "risk_level": "none",
  2230	      "discrepancies": []
  2231	    },
  2232	    {
  2233	      "matrix_ids": [
  2234	        "8.2"
  2235	      ],
  2236	      "contract_ids": [
  2237	        "8.3",
  2238	        "8.5"
  2239	      ],
  2240	      "relationship": "aligned",
  2241	      "legal_topic": "Приемка по 44-ФЗ",
  2242	      "matrix_standard": "Приемка в порядке, установленном законодательством РФ и контрактом",
  2243	      "contract_position": "п.8.3, 8.5: приемка в соответствии с 44-ФЗ и контрактом",
  2244	      "matrix_evidence": "Приемка результата исполнения Контракта осуществляется в порядке, установленном законодательством РФ и настоящим Контрактом",
  2245	      "contract_evidence": "Приемка результата исполнения Контракта осуществляется в порядке, установленном законодательством Российской Федерации и настоящим Контрактом",
  2246	      "status_reason": "Процедура приемки по 44-ФЗ сохранена.",
  2247	      "risk_level": "none",
  2248	      "discrepancies": []
  2249	    },
  2250	    {
  2251	      "matrix_ids": [
  2252	        "9.1"
  2253	      ],
  2254	      "contract_ids": [
  2255	        "10.1"
  2256	      ],
  2257	      "relationship": "aligned",
  2258	      "legal_topic": "Разрешение споров путем переговоров",
  2259	      "matrix_standard": "Споры разрешаются путем переговоров (досудебный порядок)",
  2260	      "contract_position": "п.10.1: Все споры или разногласия... разрешаются путем переговоров (в досудебном порядке)",
  2261	      "matrix_evidence": "Все споры или разногласия... разрешаются путем переговоров (в досудебном порядке)",
  2262	      "contract_evidence": "Все споры или разногласия, возникающие между Сторонами по настоящему контракту или в связи с ним, разрешаются путем переговоров (в досудебном порядке)",
  2263	      "status_reason": "Досудебный порядок сохранен.",
  2264	      "risk_level": "none",
  2265	      "discrepancies": []
  2266	    },
  2267	    {
  2268	      "matrix_ids": [
  2269	        "9.2"
  2270	      ],
  2271	      "contract_ids": [
  2272	        "10.1"
  2273	      ],
  2274	      "relationship": "aligned",
  2275	      "legal_topic": "Срок ответа на претензию - 10 календарных дней",
  2276	      "matrix_standard": "Срок ответа на претензии - 10 календарных дней",
  2277	      "contract_position": "п.10.1: Срок ответа на претензии, письма и обращения – 10 (десять) календарных дней с даты их получения",
  2278	      "matrix_evidence": "Срок ответа на претензии, письма и обращения – 10 (десять) календарных дней",
  2279	      "contract_evidence": "Срок ответа на претензии, письма и обращения – 10 (десять) календарных дней с даты их получения",
  2280	      "status_reason": "Срок ответа (10 календарных дней) сохранен.",
  2281	      "risk_level": "none",
  2282	      "discrepancies": []
  2283	    },
  2284	    {
  2285	      "matrix_ids": [
  2286	        "9.3"
  2287	      ],
  2288	      "contract_ids": [
  2289	        "10.2"
  2290	      ],
  2291	      "relationship": "aligned",
  2292	      "legal_topic": "Подсудность - Арбитражный суд Краснодарского края",
  2293	      "matrix_standard": "Споры рассматриваются в арбитражном суде по месту нахождения Банка",
  2294	      "contract_position": "п.10.2: подлежат рассмотрению в Арбитражном суде Краснодарского края",
  2295	      "matrix_evidence": "В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в Арбитражном суде",
  2296	      "contract_evidence": "В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в Арбитражном суде Краснодарского края",
  2297	      "status_reason": "Подсудность определена. Арбитражный суд Краснодарского края (место нахождения Заказчика, не Банка) - стандартно для 44-ФЗ.",
  2298	      "risk_level": "none",
  2299	      "discrepancies": []
  2300	    },
Tool:   2301	    {
  2302	      "matrix_ids": [
  2303	        "10.1"
  2304	      ],
  2305	      "contract_ids": [
  2306	        "11.1"
  2307	      ],
  2308	      "relationship": "aligned",
  2309	      "legal_topic": "Срок действия контракта",
  2310	      "matrix_standard": "Контракт действует с даты заключения по 30.12.2025 или до исчерпания цены",
  2311	      "contract_position": "п.11.1: действует с даты заключения по 30 декабря 2025 года, или до момента исчерпания предельной Цены Контракта",
  2312	      "matrix_evidence": "Настоящий контракт действует с даты заключения по 30 декабря 2025 года, или до момента исчерпания предельной Цены Контракта",
  2313	      "contract_evidence": "Настоящий контракт действует с даты заключения по 30 декабря 2025 года, или до момента исчерпания предельной Цены Контракта",
  2314	      "status_reason": "Срок действия сохранен.",
  2315	      "risk_level": "none",
  2316	      "discrepancies": []
  2317	    },
  2318	    {
  2319	      "matrix_ids": [
  2320	        "10.2"
  2321	      ],
  2322	      "contract_ids": [
  2323	        "11.3",
  2324	        "11.4",
  2325	        "11.5"
  2326	      ],
  2327	      "relationship": "aligned",
  2328	      "legal_topic": "Односторонний отказ от исполнения",
  2329	      "matrix_standard": "Односторонний отказ по ГК РФ и 44-ФЗ",
  2330	      "contract_position": "п.11.3-11.5: односторонний отказ по ГК РФ и 44-ФЗ",
  2331	      "matrix_evidence": "Расторжение контракта допускается... в случае одностороннего отказа Стороны контракта от исполнения контракта в соответствии с гражданским законодательством",
  2332	      "contract_evidence": "Расторжение контракта допускается по соглашению Сторон, по решению суда, в случае одностороннего отказа Стороны контракта от исполнения контракта в соответствии с гражданским законодательством Российской Федерации",
  2333	      "status_reason": "Право одностороннего отказа сохранено.",
  2334	      "risk_level": "none",
  2335	      "discrepancies": []
  2336	    },
  2337	    {
  2338	      "matrix_ids": [
  2339	        "10.3"
  2340	      ],
  2341	      "contract_ids": [
  2342	        "11.6"
  2343	      ],
  2344	      "relationship": "aligned",
  2345	      "legal_topic": "Изменение и расторжение по 44-ФЗ",
  2346	      "matrix_standard": "Изменение и расторжение в порядке ст. 34, 95, 96, 112 44-ФЗ",
  2347	      "contract_position": "п.11.6: Изменение и(или) расторжение контракта осуществляется в порядке, сроки, случаях и на условиях, установленных статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ",
  2348	      "matrix_evidence": "Изменение и(или) расторжение контракта осуществляется в порядке... установленных статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ",
  2349	      "contract_evidence": "Изменение и(или) расторжение контракта осуществляется в порядке, сроки, случаях и на условиях, установленных статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ",
  2350	      "status_reason": "Процедура изменения/расторжения по 44-ФЗ сохранена.",
  2351	      "risk_level": "none",
  2352	      "discrepancies": []
  2353	    },
  2354	    {
  2355	      "matrix_ids": [
  2356	        "11.1"
  2357	      ],
  2358	      "contract_ids": [
  2359	        "12.1"
  2360	      ],
  2361	      "relationship": "aligned",
  2362	      "legal_topic": "Запрет перемены Исполнителя",
  2363	      "matrix_standard": "Не допускается перемена Исполнителя, кроме правопреемства при реорганизации",
  2364	      "contract_position": "п.12.1: не допускается перемена Исполнителя, за исключением правопреемства при реорганизации",
  2365	      "matrix_evidence": "При исполнении настоящего контракта не допускается перемена Исполнителя, за исключением случая, когда новый исполнитель является правопреемником",
  2366	      "contract_evidence": "При исполнении настоящего контракта не допускается перемена Исполнителя, за исключением случая, когда новый исполнитель является правопреемником Исполнителя",
  2367	      "status_reason": "Запрет перемены Исполнителя сохранен.",
  2368	      "risk_level": "none",
  2369	      "discrepancies": []
  2370	    },
  2371	    {
  2372	      "matrix_ids": [
  2373	        "11.2"
  2374	      ],
  2375	      "contract_ids": [
  2376	        "12.2"
  2377	      ],
  2378	      "relationship": "aligned",
  2379	      "legal_topic": "Переход прав при смене Заказчика",
  2380	      "matrix_standard": "При перемене Заказчика права и обязанности переходят к новому Заказчику",
  2381	      "contract_position": "п.12.2: В случае перемены Заказчика... права и обязанности Заказчика... переходят к новому Заказчику",
  2382	      "matrix_evidence": "В случае перемены Заказчика по контракту права и обязанности Заказчика... переходят к новому Заказчику",
  2383	      "contract_evidence": "В случае перемены Заказчика по контракту права и обязанности Заказчика по настоящему контракту переходят к новому Заказчику в том же объеме и на тех же условиях",
  2384	      "status_reason": "Правило перехода прав сохранено.",
  2385	      "risk_level": "none",
  2386	      "discrepancies": []
  2387	    },
  2388	    {
  2389	      "matrix_ids": [
  2390	        "11.3"
  2391	      ],
  2392	      "contract_ids": [
  2393	        "12.3"
  2394	      ],
  2395	      "relationship": "aligned",
  2396	      "legal_topic": "Улучшенные характеристики услуг",
  2397	      "matrix_standard": "Допускается оказание услуг с улучшенными характеристиками по согласованию",
  2398	      "contract_position": "п.12.3: допускается оказание услуги, качество, технические и функциональные характеристики которых являются улучшенными",
  2399	      "matrix_evidence": "При исполнении контракта по согласованию Заказчика с Исполнителем допускается оказание услуги... которые являются улучшенными",
  2400	      "contract_evidence": "При исполнении контракта по согласованию Заказчика с Исполнителем допускается оказание услуги, качество, технические и функциональные характеристики (потребительские свойства) которых являются улучшенными",
  2401	      "status_reason": "Возможность улучшенных услуг сохранена.",
  2402	      "risk_level": "none",
  2403	      "discrepancies": []
  2404	    },
  2405	    {
  2406	      "matrix_ids": [
  2407	        "11.4"
  2408	      ],
  2409	      "contract_ids": [
  2410	        "12.4"
  2411	      ],
  2412	      "relationship": "aligned",
  2413	      "legal_topic": "Электронная форма контракта с УКЭП",
  2414	      "matrix_standard": "Контракт в электронной форме с УКЭП Сторон",
  2415	      "contract_position": "п.12.4: Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон",
  2416	      "matrix_evidence": "Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон",
  2417	      "contract_evidence": "Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон",
  2418	      "status_reason": "Электронная форма с УКЭП сохранена.",
  2419	      "risk_level": "none",
  2420	      "discrepancies": []
  2421	    },
  2422	    {
  2423	      "matrix_ids": [
  2424	        "11.5"
  2425	      ],
  2426	      "contract_ids": [
  2427	        "11.2"
  2428	      ],
  2429	      "relationship": "aligned",
  2430	      "legal_topic": "Изменения в письменной форме",
  2431	      "matrix_standard": "Изменения и дополнения действительны в письменной форме за подписью обеих Сторон",
  2432	      "contract_position": "п.11.2: Любые изменения и дополнения... имеют силу только в том случае, если они оформлены в письменном виде и подписаны обеими Сторонами",
  2433	      "matrix_evidence": "Любые изменения и дополнения к настоящему контракту имеют силу только в том случае, если они оформлены в письменном виде и подписаны обеими Сторонами",
  2434	      "contract_evidence": "Любые изменения и дополнения к настоящему контракту имеют силу только в том случае, если они оформлены в письменном виде и подписаны обеими Сторонами",
  2435	      "status_reason": "Требование письменной формы изменений сохранено.",
  2436	      "risk_level": "none",
  2437	      "discrepancies": []
  2438	    },
  2439	    {
  2440	      "matrix_ids": [
  2441	        "11.6"
  2442	      ],
  2443	      "contract_ids": [
  2444	        "11.2"
  2445	      ],
  2446	      "relationship": "aligned",
  2447	      "legal_topic": "Уведомление о смене адреса/наименования",
  2448	      "matrix_standard": "Уведомить о смене адреса/наименования в течение 2 дней",
  2449	      "contract_position": "п.11.2: В случае изменения у какой-либо из Сторон места нахождения, названия она обязана в течение двух дней письменно известить об этом другую Сторону",
  2450	      "matrix_evidence": "В случае изменения у какой - либо из Сторон места нахождения, названия она обязана в течение двух дней письменно известить об этом другую Сторону",
  2451	      "contract_evidence": "В случае изменения у какой - либо из Сторон места нахождения, названия она обязана в течение двух дней письменно известить об этом другую Сторону",
  2452	      "status_reason": "Срок уведомления (2 дня) сохранен.",
  2453	      "risk_level": "none",
  2454	      "discrepancies": []
  2455	    },
  2456	    {
  2457	      "matrix_ids": [
  2458	        "11.7"
  2459	      ],
  2460	      "contract_ids": [
  2461	        "11.7"
  2462	      ],
  2463	      "relationship": "aligned",
  2464	      "legal_topic": "Применимое право - законодательство РФ",
  2465	      "matrix_standard": "Во всем, что не предусмотрено контрактом, применяется законодательство РФ",
  2466	      "contract_position": "п.11.7: Во всем, что не предусмотрено настоящим контрактом, Стороны руководствуются действующим законодательством Российской Федерации",
  2467	      "matrix_evidence": "Во всем, что не предусмотрено настоящим контрактом, Стороны руководствуются действующим законодательством Российской Федерации",
  2468	      "contract_evidence": "Во всем, что не предусмотрено настоящим контрактом, Стороны руководствуются действующим законодательством Российской Федерации",
  2469	      "status_reason": "Субсидиарное применение законодательства РФ сохранено.",
  2470	      "risk_level": "none",
  2471	      "discrepancies": []
  2472	    },
  2473	    {
  2474	      "matrix_ids": [
  2475	        "11.8"
  2476	      ],
  2477	      "contract_ids": [
  2478	        "11.8"
  2479	      ],
  2480	      "relationship": "aligned",
  2481	      "legal_topic": "Запрет изменения существенных условий",
  2482	      "matrix_standard": "Изменение существенных условий не допускается, кроме случаев по 44-ФЗ",
  2483	      "contract_position": "п.11.8: изменение существенных условий контракта при его исполнении не допускается, за исключением... случаев, предусмотренных Федеральным законом № 44-ФЗ",
  2484	      "matrix_evidence": "Стороны предусмотрели, что изменение существенных условий контракта при его исполнении не допускается, за исключением их изменения по соглашению Сторон в случаях, предусмотренных Федеральным законом № 44-ФЗ",
  2485	      "contract_evidence": "Стороны предусмотрели, что изменение существенных условий контракта при его исполнении не допускается, за исключением их изменения по соглашению Сторон в случаях, предусмотренных Федеральным законом № 44-ФЗ",
  2486	      "status_reason": "Запрет изменения существенных условий сохранен.",
  2487	      "risk_level": "none",
  2488	      "discrepancies": []
  2489	    },
  2490	    {
  2491	      "matrix_ids": [
  2492	        "11.9"
  2493	      ],
  2494	      "contract_ids": [
  2495	        "11.1"
  2496	      ],
  2497	      "relationship": "aligned",
  2498	      "legal_topic": "Сохранение обязательств после расторжения",
  2499	      "matrix_standard": "Обязательства, возникшие до окончания срока, действуют до полного исполнения",
  2500	      "contract_position": "п.11.1: по обязательствам, возникшим в период действия... но не исполненным до окончания срока действия Контракта – до полного исполнения",
  2501	      "matrix_evidence": "по обязательствам, возникшим в период действия настоящего Контракта, но не исполненным до окончания срока действия Контракта – до полного исполнения",
  2502	      "contract_evidence": "по обязательствам, возникшим в период действия настоящего Контракта, но не исполненным до окончания срока действия Контракта – до полного исполнения принятых сторонами обязательств",
  2503	      "status_reason": "Сохранение обязательств после истечения срока сохранено.",
  2504	      "risk_level": "none",
  2505	      "discrepancies": []
  2506	    },
  2507	    {
  2508	      "matrix_ids": [
  2509	        "11.10"
  2510	      ],
  2511	      "contract_ids": [
  2512	        "11.1"
  2513	      ],
  2514	      "relationship": "aligned",
  2515	      "legal_topic": "Ответственность после окончания срока",
  2516	      "matrix_standard": "Окончание срока не освобождает от ответственности за нарушение",
  2517	      "contract_position": "п.11.1: Окончание срока действия контракта не освобождает Стороны от ответственности за его нарушение",
  2518	      "matrix_evidence": "Окончание срока действия контракта не освобождает Стороны от ответственности за его нарушение",
  2519	      "contract_evidence": "Окончание срока действия контракта не освобождает Стороны от ответственности за его нарушение",
  2520	      "status_reason": "Сохранение ответственности после истечения срока сохранено.",
  2521	      "risk_level": "none",
  2522	      "discrepancies": []
  2523	    },
  2524	    {
  2525	      "matrix_ids": [
  2526	        "11.11"
  2527	      ],
  2528	      "contract_ids": [
  2529	        "5.1.1"
  2530	      ],
  2531	      "relationship": "deviation",
  2532	      "legal_topic": "Ссылка на сайт Банка",
  2533	      "matrix_standard": "Если в договоре не указан сайт - это не является разногласием",
  2534	      "contract_position": "п.5.1.1: сайт для обучающих материалов не заполнен",
  2535	      "matrix_evidence": "Если в договоре не указан сайт - это не является разногласием",
  2536	      "contract_evidence": "Разместить на сайте: ___________________ обучающие материалы",
  2537	      "status_reason": "Адрес сайта не заполнен, но согласно матрице это не является разногласием. Однако placeholder остается.",
  2538	      "risk_level": "low",
  2539	      "discrepancies": [
  2540	        {
  2541	          "type": "missing_element",
  2542	          "description": "Адрес сайта Банка не заполнен в контракте",
  2543	          "risk": "Низкий риск: может быть заполнен при заключении"
  2544	        }
  2545	      ]
  2546	    },
  2547	    {
  2548	      "matrix_ids": [
  2549	        "11.12"
  2550	      ],
  2551	      "contract_ids": [
  2552	        "6.1"
  2553	      ],
  2554	      "relationship": "aligned",
  2555	      "legal_topic": "Антикоррупционная оговорка",
  2556	      "matrix_standard": "Наличие антикоррупционной оговорки",
  2557	      "contract_position": "п.6.1: Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых как коррупция",
  2558	      "matrix_evidence": "Важно само наличие такой или похожей формулировки",
  2559	      "contract_evidence": "При заключении, исполнении, изменении и расторжении Контракта Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция»",
  2560	      "status_reason": "Антикоррупционная оговорка присутствует.",
  2561	      "risk_level": "none",
  2562	      "discrepancies": []
  2563	    },
  2564	    {
  2565	      "matrix_ids": [
  2566	        "11.13"
  2567	      ],
  2568	      "contract_ids": [
  2569	        "12.5"
  2570	      ],
  2571	      "relationship": "aligned",
  2572	      "legal_topic": "Перечень приложений",
  2573	      "matrix_standard": "Приложения: Техническое задание, Спецификация",
  2574	      "contract_position": "п.12.5: Приложения: №1 Техническое задание, №2 Спецификация",
  2575	      "matrix_evidence": "Приложения: № 1 «Техническое задание», № 2 «Спецификация»",
  2576	      "contract_evidence": "Приложения: № 1 «Техническое задание», № 2 «Спецификация»",
  2577	      "status_reason": "Перечень приложений соответствует.",
  2578	      "risk_level": "none",
  2579	      "discrepancies": []
  2580	    },
  2581	    {
  2582	      "matrix_ids": [
  2583	        "4.2.22"
  2584	      ],
  2585	      "contract_ids": [
  2586	        "Приложение_1_п5"
  2587	      ],
  2588	      "relationship": "aligned",
  2589	      "legal_topic": "Предоставление QR-кода покупателю",
  2590	      "matrix_standard": "Предприятие предоставляет QR-код для оплаты через SberPayQR/Плати QR",
  2591	      "contract_position": "Приложение №1 п.5: Возможность вывода QR-кода для безналичной оплаты на дисплей терминала",
  2592	      "matrix_evidence": "Предоставить Покупателю для считывания QR-код с целью осуществления оплаты",
  2593	      "contract_evidence": "Возможность вывода QR-кода для безналичной оплаты на дисплей терминала",
  2594	      "status_reason": "Функциональность QR-кода сохранена через техническое задание.",
  2595	      "risk_level": "none",
  2596	      "discrepancies": []
  2597	    },
  2598	    {
  2599	      "matrix_ids": [
  2600	        "4.2.23"
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/discrepancy_analysis.json', 'offset': 2600, 'limit': 300}, 'id': 'call_00_GOIyMAkt0Ty9ckAxfMnh2279', 'type': 'tool_call'}]
Tool:   2601	      ],
  2602	      "contract_ids": [],
  2603	      "relationship": "missing_in_contract",
  2604	      "legal_topic": "Запрет одностороннего изменения QR-кода",
  2605	      "matrix_standard": "Предприятие не изменяет QR-код партнера в одностороннем порядке",
  2606	      "contract_position": "Отсутствует в контракте",
  2607	      "matrix_evidence": "Не изменять QR-код партнера в одностороннем порядке",
  2608	      "contract_evidence": "",
  2609	      "status_reason": "Прямой запрет на одностороннее изменение QR-кода отсутствует в контракте.",
  2610	      "risk_level": "low",
  2611	      "discrepancies": [
  2612	        {
  2613	          "type": "missing_element",
  2614	          "description": "Отсутствует запрет на одностороннее изменение QR-кода",
  2615	          "risk": "Низкий риск: технически QR-код генерируется терминалом Банка"
  2616	        }
  2617	      ]
  2618	    },
  2619	    {
  2620	      "matrix_ids": [
  2621	        "4.2.24"
  2622	      ],
  2623	      "contract_ids": [],
  2624	      "relationship": "missing_in_contract",
  2625	      "legal_topic": "Использование QR-API в рамках функциональных возможностей",
  2626	      "matrix_standard": "Использовать API в границах прав и функциональных возможностей QR-API",
  2627	      "contract_position": "Отсутствует в контракте (контракт не предусматривает QR-API)",
  2628	      "matrix_evidence": "Использовать API и сведения, передаваемые посредством QR-API, в границах прав и функциональных возможностей такого API",
  2629	      "contract_evidence": "",
  2630	      "status_reason": "Контракт не предусматривает интеграцию через QR-API (терминалы предоставляются Банком). Требование неприменимо к данной модели.",
  2631	      "risk_level": "low",
  2632	      "discrepancies": [
  2633	        {
  2634	          "type": "missing_element",
  2635	          "description": "Положения о QR-API отсутствуют - не применимо к модели с терминалами Банка",
  2636	          "risk": "Низкий риск: терминалы предоставляются Банком, интеграция через API не требуется"
  2637	        }
  2638	      ]
  2639	    },
  2640	    {
  2641	      "matrix_ids": [
  2642	        "4.2.25"
  2643	      ],
  2644	      "contract_ids": [],
  2645	      "relationship": "missing_in_contract",
  2646	      "legal_topic": "Приостановка API при нарушении безопасности",
  2647	      "matrix_standard": "При нарушении безопасности QR-API - приостановить использование и уведомить Банк",
  2648	      "contract_position": "Отсутствует в контракте (контракт не предусматривает QR-API)",
  2649	      "matrix_evidence": "При выявлении фактов или признаков нарушения безопасности использования QR-API... немедленно приостановить использование API",
  2650	      "contract_evidence": "",
  2651	      "status_reason": "Контракт не предусматривает интеграцию через QR-API. Требование неприменимо.",
  2652	      "risk_level": "low",
  2653	      "discrepancies": [
  2654	        {
  2655	          "type": "missing_element",
  2656	          "description": "Процедура приостановки QR-API отсутствует - не применимо к модели с терминалами Банка",
  2657	          "risk": "Низкий риск: терминалы предоставляются Банком, API не используется"
  2658	        }
  2659	      ]
  2660	    },
  2661	    {
  2662	      "matrix_ids": [
  2663	        "4.2.12"
  2664	      ],
  2665	      "contract_ids": [],
  2666	      "relationship": "missing_in_contract",
  2667	      "legal_topic": "Акцепт платежных требований",
  2668	      "matrix_standard": "Предприятие акцептует платежные требования Банка в течение 5 рабочих дней",
  2669	      "contract_position": "Отсутствует (44-ФЗ контракт, оплата через казначейство)",
  2670	      "matrix_evidence": "Акцептовать платежные требования и счета на оплату... в течение 5 (пяти) рабочих дней",
  2671	      "contract_evidence": "",
  2672	      "status_reason": "В 44-ФЗ контракте оплата производится через казначейство по документу о приемке, механизм акцепта платежных требований не применяется.",
  2673	      "risk_level": "low",
  2674	      "discrepancies": [
  2675	        {
  2676	          "type": "procedure",
  2677	          "description": "Механизм акцепта платежных требований отсутствует (44-ФЗ)",
  2678	          "risk": "Низкий риск: оплата по 44-ФЗ производится через казначейство на основании документа о приемке"
  2679	        }
  2680	      ]
  2681	    }
  2682	  ],
  2683	  "atomic_links": [
  2684	    {
  2685	      "matrix_id": "2.1",
  2686	      "contract_id": "4.3",
  2687	      "relationship": "aligned",
  2688	      "link_index": 0,
  2689	      "coverage_role": "direct",
  2690	      "coverage": "Покрытие требования матрицы 2.1 положением контракта 4.3"
  2691	    },
  2692	    {
  2693	      "matrix_id": "2.1",
  2694	      "contract_id": "5.2.9",
  2695	      "relationship": "aligned",
  2696	      "link_index": 0,
  2697	      "coverage_role": "direct",
  2698	      "coverage": "Покрытие требования матрицы 2.1 положением контракта 5.2.9"
  2699	    },
  2700	    {
  2701	      "matrix_id": "2.2",
  2702	      "contract_id": "5.1.8",
  2703	      "relationship": "aligned",
  2704	      "link_index": 1,
  2705	      "coverage_role": "direct",
  2706	      "coverage": "Покрытие требования матрицы 2.2 положением контракта 5.1.8"
  2707	    },
  2708	    {
  2709	      "matrix_id": "2.2",
  2710	      "contract_id": "Приложение_1_п5",
  2711	      "relationship": "aligned",
  2712	      "link_index": 1,
  2713	      "coverage_role": "direct",
  2714	      "coverage": "Покрытие требования матрицы 2.2 положением контракта Приложение_1_п5"
  2715	    },
  2716	    {
  2717	      "matrix_id": "2.3.1",
  2718	      "contract_id": "2.3.1",
  2719	      "relationship": "aligned",
  2720	      "link_index": 2,
  2721	      "coverage_role": "direct",
  2722	      "coverage": "Покрытие требования матрицы 2.3.1 положением контракта 2.3.1"
  2723	    },
  2724	    {
  2725	      "matrix_id": "2.3.2",
  2726	      "contract_id": "2.3.2",
  2727	      "relationship": "aligned",
  2728	      "link_index": 3,
  2729	      "coverage_role": "direct",
  2730	      "coverage": "Покрытие требования матрицы 2.3.2 положением контракта 2.3.2"
  2731	    },
  2732	    {
  2733	      "matrix_id": "2.3.3",
  2734	      "contract_id": "2.3.3",
  2735	      "relationship": "aligned",
  2736	      "link_index": 4,
  2737	      "coverage_role": "direct",
  2738	      "coverage": "Покрытие требования матрицы 2.3.3 положением контракта 2.3.3"
  2739	    },
  2740	    {
  2741	      "matrix_id": "2.3.4",
  2742	      "contract_id": "2.3.4",
  2743	      "relationship": "aligned",
  2744	      "link_index": 5,
  2745	      "coverage_role": "direct",
  2746	      "coverage": "Покрытие требования матрицы 2.3.4 положением контракта 2.3.4"
  2747	    },
  2748	    {
  2749	      "matrix_id": "2.3.5",
  2750	      "contract_id": "2.3.5",
  2751	      "relationship": "deviation",
  2752	      "link_index": 6,
  2753	      "coverage_role": "direct",
  2754	      "coverage": "Покрытие требования матрицы 2.3.5 положением контракта 2.3.5"
  2755	    },
  2756	    {
  2757	      "matrix_id": "2.3.6",
  2758	      "contract_id": "2.3.6",
  2759	      "relationship": "aligned",
  2760	      "link_index": 7,
  2761	      "coverage_role": "direct",
  2762	      "coverage": "Покрытие требования матрицы 2.3.6 положением контракта 2.3.6"
  2763	    },
  2764	    {
  2765	      "matrix_id": "2.3.7",
  2766	      "contract_id": "2.3.7",
  2767	      "relationship": "aligned",
  2768	      "link_index": 8,
  2769	      "coverage_role": "direct",
  2770	      "coverage": "Покрытие требования матрицы 2.3.7 положением контракта 2.3.7"
  2771	    },
  2772	    {
  2773	      "matrix_id": "2.4",
  2774	      "contract_id": "1.1",
  2775	      "relationship": "aligned",
  2776	      "link_index": 9,
  2777	      "coverage_role": "direct",
  2778	      "coverage": "Покрытие требования матрицы 2.4 положением контракта 1.1"
  2779	    },
  2780	    {
  2781	      "matrix_id": "2.4",
  2782	      "contract_id": "8.3.2",
  2783	      "relationship": "aligned",
  2784	      "link_index": 9,
  2785	      "coverage_role": "direct",
  2786	      "coverage": "Покрытие требования матрицы 2.4 положением контракта 8.3.2"
  2787	    },
  2788	    {
  2789	      "matrix_id": "2.6.3.1",
  2790	      "contract_id": "Приложение_1_п5",
  2791	      "relationship": "aligned",
  2792	      "link_index": 10,
  2793	      "coverage_role": "direct",
  2794	      "coverage": "Покрытие требования матрицы 2.6.3.1 положением контракта Приложение_1_п5"
  2795	    },
  2796	    {
  2797	      "matrix_id": "2.6.3.2",
  2798	      "contract_id": "2.3.1",
  2799	      "relationship": "aligned",
  2800	      "link_index": 11,
  2801	      "coverage_role": "direct",
  2802	      "coverage": "Покрытие требования матрицы 2.6.3.2 положением контракта 2.3.1"
  2803	    },
  2804	    {
  2805	      "matrix_id": "2.6.3.2",
  2806	      "contract_id": "2.3.2",
  2807	      "relationship": "aligned",
  2808	      "link_index": 11,
  2809	      "coverage_role": "direct",
  2810	      "coverage": "Покрытие требования матрицы 2.6.3.2 положением контракта 2.3.2"
  2811	    },
  2812	    {
  2813	      "matrix_id": "2.6.3.2",
  2814	      "contract_id": "2.3.7",
  2815	      "relationship": "aligned",
  2816	      "link_index": 11,
  2817	      "coverage_role": "direct",
  2818	      "coverage": "Покрытие требования матрицы 2.6.3.2 положением контракта 2.3.7"
  2819	    },
  2820	    {
  2821	      "matrix_id": "2.7",
  2822	      "contract_id": "12.4",
  2823	      "relationship": "aligned",
  2824	      "link_index": 12,
  2825	      "coverage_role": "direct",
  2826	      "coverage": "Покрытие требования матрицы 2.7 положением контракта 12.4"
  2827	    },
  2828	    {
  2829	      "matrix_id": "3.1",
  2830	      "contract_id": "1.3",
  2831	      "relationship": "aligned",
  2832	      "link_index": 13,
  2833	      "coverage_role": "direct",
  2834	      "coverage": "Покрытие требования матрицы 3.1 положением контракта 1.3"
  2835	    },
  2836	    {
  2837	      "matrix_id": "3.1",
  2838	      "contract_id": "5.3.7",
  2839	      "relationship": "aligned",
  2840	      "link_index": 13,
  2841	      "coverage_role": "direct",
  2842	      "coverage": "Покрытие требования матрицы 3.1 положением контракта 5.3.7"
  2843	    },
  2844	    {
  2845	      "matrix_id": "3.1",
  2846	      "contract_id": "5.3.8",
  2847	      "relationship": "aligned",
  2848	      "link_index": 13,
  2849	      "coverage_role": "direct",
  2850	      "coverage": "Покрытие требования матрицы 3.1 положением контракта 5.3.8"
  2851	    },
  2852	    {
  2853	      "matrix_id": "3.2",
  2854	      "contract_id": "5.1.8",
  2855	      "relationship": "aligned",
  2856	      "link_index": 14,
  2857	      "coverage_role": "direct",
  2858	      "coverage": "Покрытие требования матрицы 3.2 положением контракта 5.1.8"
  2859	    },
  2860	    {
  2861	      "matrix_id": "3.2",
  2862	      "contract_id": "5.1.10",
  2863	      "relationship": "aligned",
  2864	      "link_index": 14,
  2865	      "coverage_role": "direct",
  2866	      "coverage": "Покрытие требования матрицы 3.2 положением контракта 5.1.10"
  2867	    },
  2868	    {
  2869	      "matrix_id": "3.3",
  2870	      "contract_id": "3.2",
  2871	      "relationship": "aligned",
  2872	      "link_index": 15,
  2873	      "coverage_role": "direct",
  2874	      "coverage": "Покрытие требования матрицы 3.3 положением контракта 3.2"
  2875	    },
  2876	    {
  2877	      "matrix_id": "3.3",
  2878	      "contract_id": "4.5",
  2879	      "relationship": "aligned",
  2880	      "link_index": 15,
  2881	      "coverage_role": "direct",
  2882	      "coverage": "Покрытие требования матрицы 3.3 положением контракта 4.5"
  2883	    },
  2884	    {
  2885	      "matrix_id": "4.1.1",
  2886	      "contract_id": "5.4.5",
  2887	      "relationship": "aligned",
  2888	      "link_index": 16,
  2889	      "coverage_role": "direct",
  2890	      "coverage": "Покрытие требования матрицы 4.1.1 положением контракта 5.4.5"
  2891	    },
  2892	    {
  2893	      "matrix_id": "4.1.2",
  2894	      "contract_id": "5.9",
  2895	      "relationship": "aligned",
  2896	      "link_index": 17,
  2897	      "coverage_role": "direct",
  2898	      "coverage": "Покрытие требования матрицы 4.1.2 положением контракта 5.9"
  2899	    },
  2900	    {
AI: Now let me read the remaining sections: unmatched_matrix, unmatched_contract, coverage_ledger, and summary.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/outputs/discrepancy_analysis.json\', \'r\') as f:\n    data = json.load(f)\n\n# Print unmatched_matrix\nprint(\'=== UNMATCHED_MATRIX ===\')\nfor item in data.get(\'unmatched_matrix\', []):\n    print(json.dumps(item, ensure_ascii=False, indent=2))\nprint()\n\nprint(\'=== UNMATCHED_CONTRACT ===\')\nfor item in data.get(\'unmatched_contract\', []):\n    print(json.dumps(item, ensure_ascii=False, indent=2))\nprint()\n\nprint(\'=== COVERAGE_LEDGER MATRIX ===\')\nfor item in data.get(\'coverage_ledger\', {}).get(\'matrix\', []):\n    print(json.dumps(item, ensure_ascii=False))\nprint()\n\nprint(\'=== COVERAGE_LEDGER CONTRACT ===\')\nfor item in data.get(\'coverage_ledger\', {}).get(\'contract\', []):\n    print(json.dumps(item, ensure_ascii=False))\nprint()\n\nprint(\'=== SUMMARY ===\')\nprint(json.dumps(data.get(\'summary\', {}), ensure_ascii=False, indent=2))\n"\n', 'timeout': 30}, 'id': 'call_00_F9LPpckW9NuoQ8y8ZvyT9165', 'type': 'tool_call'}]
Tool: Tool result too large, the result of this tool call call_00_F9LPpckW9NuoQ8y8ZvyT9165 was saved in the filesystem at this path: /large_tool_results/call_00_F9LPpckW9NuoQ8y8ZvyT9165

You can read the result from the filesystem by using the read_file tool, but make sure to only read part of the result at a time.

You can do this by specifying an offset and limit in the read_file tool call. For example, to read the first 100 lines, you can use the read_file tool with offset=0 and limit=100.

Here is a preview showing the head and tail of the result (lines of the form `... [N lines truncated] ...` indicate omitted lines in the middle of the content):

     1	=== UNMATCHED_MATRIX ===
     2	
     3	=== UNMATCHED_CONTRACT ===
     4	{
     5	  "contract_id": "1.2",
... [1043 lines truncated] ...
  1049	  "missing_in_contract_count": 0,
  1050	  "extra_in_contract_count": 72
  1051	}
  1052	
  1053	[Command succeeded with exit code 0]

AI: [{'name': 'read_file', 'args': {'file_path': '/large_tool_results/call_00_F9LPpckW9NuoQ8y8ZvyT9165', 'limit': 200}, 'id': 'call_00_YjhOWACVL3iocLSRjcNW3984', 'type': 'tool_call'}]
Tool:      1	=== UNMATCHED_MATRIX ===
     2	
     3	=== UNMATCHED_CONTRACT ===
     4	{
     5	  "contract_id": "1.2",
     6	  "contract_position": "РћР±СЉРµРј СѓСЃР»СѓРі, СѓРєР°Р·Р°РЅРЅС‹С… РІ РїСѓРЅРєС‚Рµ 1.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ РїРѕС‚СЂРµР±РЅРѕСЃС‚СЊСЋ Р—Р°РєР°Р·С‡РёРєР° РЅР° СЃСѓРјРјСѓ, РЅРµ РїСЂРµРІС‹С€Р°СЋС‰СѓСЋ РјР°РєСЃРёРјР°Р»СЊРЅСѓСЋ С†РµРЅСѓ РєРѕРЅС‚СЂР°РєС‚Р°, СѓРєР°Р·Р°РЅРЅСѓСЋ РІ РїСѓРЅРєС‚Рµ 3.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°.",
     7	  "source_evidence": "РћР±СЉРµРј СѓСЃР»СѓРі, СѓРєР°Р·Р°РЅРЅС‹С… РІ РїСѓРЅРєС‚Рµ 1.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ РїРѕС‚СЂРµР±РЅРѕСЃС‚СЊСЋ Р—Р°РєР°Р·С‡РёРєР° РЅР° СЃСѓРјРјСѓ, РЅРµ РїСЂРµРІС‹С€Р°СЋС‰СѓСЋ РјР°РєСЃРёРјР°Р»СЊРЅСѓСЋ С†РµРЅСѓ РєРѕРЅС‚СЂР°РєС‚Р°, СѓРєР°Р·Р°РЅРЅСѓСЋ РІ РїСѓРЅРєС‚Рµ 3.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°.",
     8	  "status": "extra_in_contract",
     9	  "risk_level": "medium",
    10	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    11	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    12	}
    13	{
    14	  "contract_id": "2.1.1",
    15	  "contract_position": "Р±Р°РЅРєРѕРІСЃРєР°СЏ РєР°СЂС‚Р° (РєР°СЂС‚Р°) вЂ“ СЂР°СЃС‡РµС‚РЅР°СЏ (РґРµР±РµС‚РѕРІР°СЏ), РєСЂРµРґРёС‚РЅР°СЏ РёР»Рё РїСЂРµРґРѕРїР»Р°С‡РµРЅРЅР°СЏ РєР°СЂС‚Р° СЃ Р»РѕРіРѕС‚РёРїРѕРј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, СЏРІР»СЏСЋС‰Р°СЏСЃСЏ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј СЃСЂРµРґСЃС‚РІРѕРј РїР»Р°С‚РµР¶Р°. Р”Р»СЏ СЃРѕРІРµСЂС€РµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРЎРў. РљР°СЂС‚Р° РјРѕР¶РµС‚ Р±С‹С‚СЊ РїСЂРµРґСЃС‚Р°РІР»РµРЅР° РЅР° С„РёР·РёС‡РµСЃРєРѕРј РЅРѕСЃРёС‚РµР»",
    16	  "source_evidence": "Р±Р°РЅРєРѕРІСЃРєР°СЏ РєР°СЂС‚Р° (РєР°СЂС‚Р°) вЂ“ СЂР°СЃС‡РµС‚РЅР°СЏ (РґРµР±РµС‚РѕРІР°СЏ), РєСЂРµРґРёС‚РЅР°СЏ РёР»Рё РїСЂРµРґРѕРїР»Р°С‡РµРЅРЅР°СЏ РєР°СЂС‚Р° СЃ Р»РѕРіРѕС‚РёРїРѕРј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, СЏРІР»СЏСЋС‰Р°СЏСЃСЏ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј СЃСЂРµРґСЃС‚РІРѕРј РїР»Р°С‚РµР¶Р°. Р”Р»СЏ СЃРѕРІРµСЂС€РµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРЎРў. РљР°СЂС‚Р° РјРѕР¶РµС‚ Р±С‹С‚СЊ РїСЂРµРґСЃС‚Р°РІР»РµРЅР° РЅР° С„РёР·РёС‡РµСЃРєРѕРј РЅРѕСЃРёС‚РµР»",
    17	  "status": "extra_in_contract",
    18	  "risk_level": "medium",
    19	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    20	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    21	}
    22	{
    23	  "contract_id": "2.1.2",
    24	  "contract_position": "Р±Р°РЅРє-СЌРєРІР°Р№СЂРµСЂ - РєСЂРµРґРёС‚РЅР°СЏ РѕСЂРіР°РЅРёР·Р°С†РёСЏ, СЏРІР»СЏСЋС‰Р°СЏСЃСЏ СѓС‡Р°СЃС‚РЅРёРєРѕРј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, РѕСЂРіР°РЅРёР·СѓСЋС‰Р°СЏ С‚РѕС‡РєРё РїСЂРёРµРјР° РєР°СЂС‚ Рё РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰Р°СЏ РІРµСЃСЊ РєРѕРјРїР»РµРєСЃ С„РёРЅР°РЅСЃРѕРІС‹С… РѕРїРµСЂР°С†РёР№, СЃРІСЏР·Р°РЅРЅС‹С… СЃ РІС‹РїРѕР»РЅРµРЅРёРµРј СЂР°СЃС‡РµС‚РѕРІ Рё РїР»Р°С‚РµР¶РµР№ РїРѕ РєР°СЂС‚Р°Рј РІ СЌС‚РёС… С‚РѕС‡РєР°С…;",
    25	  "source_evidence": "Р±Р°РЅРє-СЌРєРІР°Р№СЂРµСЂ - РєСЂРµРґРёС‚РЅР°СЏ РѕСЂРіР°РЅРёР·Р°С†РёСЏ, СЏРІР»СЏСЋС‰Р°СЏСЃСЏ СѓС‡Р°СЃС‚РЅРёРєРѕРј РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, РѕСЂРіР°РЅРёР·СѓСЋС‰Р°СЏ С‚РѕС‡РєРё РїСЂРёРµРјР° РєР°СЂС‚ Рё РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰Р°СЏ РІРµСЃСЊ РєРѕРјРїР»РµРєСЃ С„РёРЅР°РЅСЃРѕРІС‹С… РѕРїРµСЂР°С†РёР№, СЃРІСЏР·Р°РЅРЅС‹С… СЃ РІС‹РїРѕР»РЅРµРЅРёРµРј СЂР°СЃС‡РµС‚РѕРІ Рё РїР»Р°С‚РµР¶РµР№ РїРѕ РєР°СЂС‚Р°Рј РІ СЌС‚РёС… С‚РѕС‡РєР°С…;",
    26	  "status": "extra_in_contract",
    27	  "risk_level": "medium",
    28	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    29	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    30	}
    31	{
    32	  "contract_id": "2.1.4",
    33	  "contract_position": "РІРѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° вЂ“ РѕРїРµСЂР°С†РёСЏ, РёРЅРёС†РёРёСЂСѓРµРјР°СЏ Р±Р°РЅРєРѕРј-СЌРјРёС‚РµРЅС‚РѕРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё РѕСЃРїР°СЂРёРІР°СЋС‰Р°СЏ РїСЂРµРґСЉСЏРІР»РµРЅРЅСѓСЋ Р±Р°РЅРєРѕРј-СЌРєРІР°Р№СЂРµСЂРѕРј РѕРїРµСЂР°С†РёСЋ (С‚СЂР°РЅР·Р°РєС†РёСЋ). Р РµР·СѓР»СЊС‚Р°С‚РѕРј РѕРїРµСЂР°С†РёРё В«Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р°В» СЏРІР»СЏРµС‚СЃСЏ СЃРїРёСЃР°РЅРёРµ РґРµРЅРµР¶РЅС‹С… СЃ",
    34	  "source_evidence": "РІРѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° вЂ“ РѕРїРµСЂР°С†РёСЏ, РёРЅРёС†РёРёСЂСѓРµРјР°СЏ Р±Р°РЅРєРѕРј-СЌРјРёС‚РµРЅС‚РѕРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё РѕСЃРїР°СЂРёРІР°СЋС‰Р°СЏ РїСЂРµРґСЉСЏРІР»РµРЅРЅСѓСЋ Р±Р°РЅРєРѕРј-СЌРєРІР°Р№СЂРµСЂРѕРј РѕРїРµСЂР°С†РёСЋ (С‚СЂР°РЅР·Р°РєС†РёСЋ). Р РµР·СѓР»СЊС‚Р°С‚РѕРј РѕРїРµСЂР°С†РёРё В«Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р°В» СЏРІР»СЏРµС‚СЃСЏ СЃРїРёСЃР°РЅРёРµ РґРµРЅРµР¶РЅС‹С… СЃ",
    35	  "status": "extra_in_contract",
    36	  "risk_level": "medium",
    37	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    38	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    39	}
    40	{
    41	  "contract_id": "2.1.6",
    42	  "contract_position": "РґРѕРєСѓРјРµРЅС‚ РїРѕ РѕРїРµСЂР°С†РёРё - РґРѕРєСѓРјРµРЅС‚ РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ РёР»Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ, СЏРІР»СЏСЋС‰РёР№СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј, СЃРѕРІРµСЂС€РµРЅРЅС‹Рј СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РєР°СЂС‚С‹;",
    43	  "source_evidence": "РґРѕРєСѓРјРµРЅС‚ РїРѕ РѕРїРµСЂР°С†РёРё - РґРѕРєСѓРјРµРЅС‚ РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ РёР»Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ, СЏРІР»СЏСЋС‰РёР№СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј, СЃРѕРІРµСЂС€РµРЅРЅС‹Рј СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РєР°СЂС‚С‹;",
    44	  "status": "extra_in_contract",
    45	  "risk_level": "medium",
    46	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    47	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    48	}
    49	{
    50	  "contract_id": "2.1.7",
    51	  "contract_position": "РєРѕРґ Р°РІС‚РѕСЂРёР·Р°С†РёРё - Р±СѓРєРІРµРЅРЅРѕ-С†РёС„СЂРѕРІРѕР№ РєРѕРґ, РїРѕРґС‚РІРµСЂР¶РґР°СЋС‰РёР№ СѓСЃРїРµС€РЅРѕРµ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё;",
    52	  "source_evidence": "РєРѕРґ Р°РІС‚РѕСЂРёР·Р°С†РёРё - Р±СѓРєРІРµРЅРЅРѕ-С†РёС„СЂРѕРІРѕР№ РєРѕРґ, РїРѕРґС‚РІРµСЂР¶РґР°СЋС‰РёР№ СѓСЃРїРµС€РЅРѕРµ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё;",
    53	  "status": "extra_in_contract",
    54	  "risk_level": "medium",
    55	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    56	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    57	}
    58	{
    59	  "contract_id": "2.1.8",
    60	  "contract_position": "РєРѕРЅС‚СЂРѕР»СЊРЅРѕ-РєР°СЃСЃРѕРІР°СЏ С‚РµС…РЅРёРєР° (РљРљРў) вЂ“ РїСЂРѕРіСЂР°РјРјРЅРѕ-С‚РµС…РЅРёС‡РµСЃРєРёРµ СЃСЂРµРґСЃС‚РІР° Рё РёС… РєРѕРјРїР»РµРєСЃС‹, РѕР±РµСЃРїРµС‡РёРІР°СЋС‰РёРµ Р·Р°РїРёСЃСЊ Рё С…СЂР°РЅРµРЅРёРµ С„РёСЃРєР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… РІ С„РёСЃРєР°Р»СЊРЅС‹С… РЅР°РєРѕРїРёС‚РµР»СЏС…, С„РѕСЂРјРёСЂСѓСЋС‰РёРµ С„РёСЃРєР°Р»СЊРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹, РѕР±РµСЃРїРµС‡РёРІР°СЋС‰РёРµ РїРµСЂРµРґР°С‡Сѓ С„РёСЃРєР°Р»СЊРЅС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ",
    61	  "source_evidence": "РєРѕРЅС‚СЂРѕР»СЊРЅРѕ-РєР°СЃСЃРѕРІР°СЏ С‚РµС…РЅРёРєР° (РљРљРў) вЂ“ РїСЂРѕРіСЂР°РјРјРЅРѕ-С‚РµС…РЅРёС‡РµСЃРєРёРµ СЃСЂРµРґСЃС‚РІР° Рё РёС… РєРѕРјРїР»РµРєСЃС‹, РѕР±РµСЃРїРµС‡РёРІР°СЋС‰РёРµ Р·Р°РїРёСЃСЊ Рё С…СЂР°РЅРµРЅРёРµ С„РёСЃРєР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… РІ С„РёСЃРєР°Р»СЊРЅС‹С… РЅР°РєРѕРїРёС‚РµР»СЏС…, С„РѕСЂРјРёСЂСѓСЋС‰РёРµ С„РёСЃРєР°Р»СЊРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹, РѕР±РµСЃРїРµС‡РёРІР°СЋС‰РёРµ РїРµСЂРµРґР°С‡Сѓ С„РёСЃРєР°Р»СЊРЅС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ",
    62	  "status": "extra_in_contract",
    63	  "risk_level": "medium",
    64	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    65	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    66	}
    67	{
    68	  "contract_id": "2.1.9",
    69	  "contract_position": "РєРѕРЅС‚СЂРѕР»СЊРЅР°СЏ Р»РµРЅС‚Р° - РѕС‚С‡РµС‚, СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµРјС‹Р№ РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ Рё СЃРѕРґРµСЂР¶Р°С‰РёР№ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ С‚СЂР°РЅР·Р°РєС†РёСЏС…, СЃРѕРІРµСЂС€РµРЅРЅС‹С… РІ РўРЎРў РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ Р·Р° РѕРїСЂРµРґРµР»РµРЅРЅС‹Р№ РїРµСЂРёРѕРґ;",
    70	  "source_evidence": "РєРѕРЅС‚СЂРѕР»СЊРЅР°СЏ Р»РµРЅС‚Р° - РѕС‚С‡РµС‚, СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµРјС‹Р№ РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ Рё СЃРѕРґРµСЂР¶Р°С‰РёР№ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ С‚СЂР°РЅР·Р°РєС†РёСЏС…, СЃРѕРІРµСЂС€РµРЅРЅС‹С… РІ РўРЎРў РЅР° СЌР»РµРєС‚СЂРѕРЅРЅРѕРј С‚РµСЂРјРёРЅР°Р»Рµ Р·Р° РѕРїСЂРµРґРµР»РµРЅРЅС‹Р№ РїРµСЂРёРѕРґ;",
    71	  "status": "extra_in_contract",
    72	  "risk_level": "medium",
    73	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    74	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    75	}
    76	{
    77	  "contract_id": "2.1.10",
    78	  "contract_position": "РѕС‚Р»РѕР¶РµРЅРЅС‹Р№ РїР»Р°С‚РµР¶ - РѕРїРµСЂР°С†РёСЏ РѕРїР»Р°С‚С‹, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјР°СЏ РЅР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕРіРѕ РѕС‚ Р—Р°РєР°Р·С‡РёРєР°/РўРЎРў СЃРѕРѕР±С‰РµРЅРёСЏ, РЅР°РїСЂР°РІР»РµРЅРЅРѕРіРѕ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°, Рѕ РЅР°Р»РёС‡РёРё Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕРєСѓРїР°С‚РµР»СЏ РїРµСЂРµРґ Р—Р°РєР°Р·С‡РёРєРѕРј/РўРЎРў, РїРѕСЃР»Рµ РѕРєРѕРЅС‡Р°С‚РµР»СЊРЅРѕРіРѕ СЂР°",
    79	  "source_evidence": "РѕС‚Р»РѕР¶РµРЅРЅС‹Р№ РїР»Р°С‚РµР¶ - РѕРїРµСЂР°С†РёСЏ РѕРїР»Р°С‚С‹, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјР°СЏ РЅР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕРіРѕ РѕС‚ Р—Р°РєР°Р·С‡РёРєР°/РўРЎРў СЃРѕРѕР±С‰РµРЅРёСЏ, РЅР°РїСЂР°РІР»РµРЅРЅРѕРіРѕ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°, Рѕ РЅР°Р»РёС‡РёРё Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕРєСѓРїР°С‚РµР»СЏ РїРµСЂРµРґ Р—Р°РєР°Р·С‡РёРєРѕРј/РўРЎРў, РїРѕСЃР»Рµ РѕРєРѕРЅС‡Р°С‚РµР»СЊРЅРѕРіРѕ СЂР°",
    80	  "status": "extra_in_contract",
    81	  "risk_level": "medium",
    82	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    83	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    84	}
    85	{
    86	  "contract_id": "2.1.16",
    87	  "contract_position": "РїРѕРєСѓРїР°С‚РµР»СЊ - С„РёР·РёС‡РµСЃРєРѕРµ Р»РёС†Рѕ, РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰РµРµ РѕРїР»Р°С‚Сѓ С‚РѕРІР°СЂР°/СѓСЃР»СѓРіРё РІ РўРЎРў РїСЂРё РїРѕРјРѕС‰Рё РєР°СЂС‚С‹, Р° С‚Р°РєР¶Рµ Р»РёС†Рѕ, РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰РµРµ РІРѕР·РІСЂР°С‚/РѕС‚РєР°Р· РѕС‚ С‚РѕРІР°СЂР°/СѓСЃР»СѓРіРё РІ РўРЎРў;",
    88	  "source_evidence": "РїРѕРєСѓРїР°С‚РµР»СЊ - С„РёР·РёС‡РµСЃРєРѕРµ Р»РёС†Рѕ, РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰РµРµ РѕРїР»Р°С‚Сѓ С‚РѕРІР°СЂР°/СѓСЃР»СѓРіРё РІ РўРЎРў РїСЂРё РїРѕРјРѕС‰Рё РєР°СЂС‚С‹, Р° С‚Р°РєР¶Рµ Р»РёС†Рѕ, РѕСЃСѓС‰РµСЃС‚РІР»СЏСЋС‰РµРµ РІРѕР·РІСЂР°С‚/РѕС‚РєР°Р· РѕС‚ С‚РѕРІР°СЂР°/СѓСЃР»СѓРіРё РІ РўРЎРў;",
    89	  "status": "extra_in_contract",
    90	  "risk_level": "medium",
    91	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
    92	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
    93	}
    94	{
    95	  "contract_id": "2.1.18",
    96	  "contract_position": "РїСЂРµРґР°РІС‚РѕСЂРёР·Р°С†РёСЏ - РѕРїРµСЂР°С†РёСЏ РїРѕ СЂРµР·РµСЂРІРёСЂРѕРІР°РЅРёСЋ РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° РєР°СЂС‚Рµ РґР»СЏ РїРѕСЃР»РµРґСѓСЋС‰РµР№ РѕРїР»Р°С‚С‹, С‚СЂРµР±СѓСЋС‰Р°СЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р—Р°РєР°Р·С‡РёРєР°/РўРЎРў СЃ СѓРєР°Р·Р°РЅРёРµРј СЃСѓРјРјС‹ СЃРїРёСЃР°РЅРёСЏ;",
    97	  "source_evidence": "РїСЂРµРґР°РІС‚РѕСЂРёР·Р°С†РёСЏ - РѕРїРµСЂР°С†РёСЏ РїРѕ СЂРµР·РµСЂРІРёСЂРѕРІР°РЅРёСЋ РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° РєР°СЂС‚Рµ РґР»СЏ РїРѕСЃР»РµРґСѓСЋС‰РµР№ РѕРїР»Р°С‚С‹, С‚СЂРµР±СѓСЋС‰Р°СЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р—Р°РєР°Р·С‡РёРєР°/РўРЎРў СЃ СѓРєР°Р·Р°РЅРёРµРј СЃСѓРјРјС‹ СЃРїРёСЃР°РЅРёСЏ;",
    98	  "status": "extra_in_contract",
    99	  "risk_level": "medium",
   100	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   101	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   102	}
   103	{
   104	  "contract_id": "2.1.19",
   105	  "contract_position": "РїСЂРµРґРїСЂРёСЏС‚РёРµ (Р—Р°РєР°Р·С‡РёРє) вЂ“ С‚РѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅРѕРµ РїСЂРµРґРїСЂРёСЏС‚РёРµ (РўРЎРџ): СЋСЂРёРґРёС‡РµСЃРєРѕРµ Р»РёС†Рѕ/ РёРЅРґРёРІРёРґСѓР°Р»СЊРЅС‹Р№ РїСЂРµРґРїСЂРёРЅРёРјР°С‚РµР»СЊ (Р�Рџ), РїСЂРёРЅРёРјР°СЋС‰РёРµ РєР°СЂС‚С‹ РІ РєР°С‡РµСЃС‚РІРµ СЃСЂРµРґСЃС‚РІР° РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РЅР° РѕСЃРЅРѕРІР°РЅРёРё СѓСЃР»РѕРІРёР№ РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°. Р—Р°РєР°Р·С‡РёРє РјРѕР¶РµС‚ РёРјРµС‚СЊ ",
   106	  "source_evidence": "РїСЂРµРґРїСЂРёСЏС‚РёРµ (Р—Р°РєР°Р·С‡РёРє) вЂ“ С‚РѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅРѕРµ РїСЂРµРґРїСЂРёСЏС‚РёРµ (РўРЎРџ): СЋСЂРёРґРёС‡РµСЃРєРѕРµ Р»РёС†Рѕ/ РёРЅРґРёРІРёРґСѓР°Р»СЊРЅС‹Р№ РїСЂРµРґРїСЂРёРЅРёРјР°С‚РµР»СЊ (Р�Рџ), РїСЂРёРЅРёРјР°СЋС‰РёРµ РєР°СЂС‚С‹ РІ РєР°С‡РµСЃС‚РІРµ СЃСЂРµРґСЃС‚РІР° РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РЅР° РѕСЃРЅРѕРІР°РЅРёРё СѓСЃР»РѕРІРёР№ РЅР°СЃС‚РѕСЏС‰РµРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°. Р—Р°РєР°Р·С‡РёРє РјРѕР¶РµС‚ РёРјРµС‚СЊ ",
   107	  "status": "extra_in_contract",
   108	  "risk_level": "medium",
   109	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   110	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   111	}
   112	{
   113	  "contract_id": "2.1.21",
   114	  "contract_position": "СЂРµРІРµСЂСЃРёРІРЅР°СЏ С‚СЂР°РЅР·Р°РєС†РёСЏ вЂ“ С„РёРЅР°РЅСЃРѕРІРѕ-РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ, РєРѕС‚РѕСЂРѕРµ Р±Р°РЅРє-СЌРєРІР°Р№СЂРµСЂ РЅР°РїСЂР°РІР»СЏРµС‚ РІ РїР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РґР»СЏ РѕС‚РјРµРЅС‹ СЂР°РЅРµРµ РЅР°РїСЂР°РІР»РµРЅРЅРѕР№ С‚СЂР°РЅР·Р°РєС†РёРё (РЅР°РїСЂРёРјРµСЂ, РІ СЃР»СѓС‡Р°Рµ РѕС€РёР±РѕС‡РЅРѕРіРѕ РїСЂРµРґСЉСЏРІР»РµРЅРёСЏ С‚СЂР°РЅР·Р°РєС†РёРё). Р’ СЂРµР·СѓР»СЊС‚Р°С‚Рµ РѕР±СЂР°Р±РѕС‚РєРё СЌС‚РѕРіРѕ",
   115	  "source_evidence": "СЂРµРІРµСЂСЃРёРІРЅР°СЏ С‚СЂР°РЅР·Р°РєС†РёСЏ вЂ“ С„РёРЅР°РЅСЃРѕРІРѕ-РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ, РєРѕС‚РѕСЂРѕРµ Р±Р°РЅРє-СЌРєРІР°Р№СЂРµСЂ РЅР°РїСЂР°РІР»СЏРµС‚ РІ РїР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РґР»СЏ РѕС‚РјРµРЅС‹ СЂР°РЅРµРµ РЅР°РїСЂР°РІР»РµРЅРЅРѕР№ С‚СЂР°РЅР·Р°РєС†РёРё (РЅР°РїСЂРёРјРµСЂ, РІ СЃР»СѓС‡Р°Рµ РѕС€РёР±РѕС‡РЅРѕРіРѕ РїСЂРµРґСЉСЏРІР»РµРЅРёСЏ С‚СЂР°РЅР·Р°РєС†РёРё). Р’ СЂРµР·СѓР»СЊС‚Р°С‚Рµ РѕР±СЂР°Р±РѕС‚РєРё СЌС‚РѕРіРѕ",
   116	  "status": "extra_in_contract",
   117	  "risk_level": "medium",
   118	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   119	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   120	}
   121	{
   122	  "contract_id": "2.2",
   123	  "contract_position": "СЌР»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» вЂ“ СЌР»РµРєС‚СЂРѕРЅРЅРѕРµ РїСЂРѕРіСЂР°РјРјРЅРѕ-С‚РµС…РЅРёС‡РµСЃРєРѕРµ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ РёСЃРїРѕР»РЅРёС‚РµР»СЏ (РІ С‚РѕРј С‡РёСЃР»Рµ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРµ РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ Рё/РёР»Рё СЃРїРµС†РёР°Р»СЊРЅРѕРµ РїСЂРѕРіСЂР°РјРјРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ РљРљРў), РїРѕР·РІРѕР»СЏСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїСЂРёРµРј РєР°СЂС‚ РІ РўРЎРў РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№. Р­Р»Рµ",
   124	  "source_evidence": "СЌР»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» вЂ“ СЌР»РµРєС‚СЂРѕРЅРЅРѕРµ РїСЂРѕРіСЂР°РјРјРЅРѕ-С‚РµС…РЅРёС‡РµСЃРєРѕРµ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ РёСЃРїРѕР»РЅРёС‚РµР»СЏ (РІ С‚РѕРј С‡РёСЃР»Рµ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРµ РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ Рё/РёР»Рё СЃРїРµС†РёР°Р»СЊРЅРѕРµ РїСЂРѕРіСЂР°РјРјРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ РљРљРў), РїРѕР·РІРѕР»СЏСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїСЂРёРµРј РєР°СЂС‚ РІ РўРЎРў РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№. Р­Р»Рµ",
   125	  "status": "extra_in_contract",
   126	  "risk_level": "low",
   127	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   128	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   129	}
   130	{
   131	  "contract_id": "2.3",
   132	  "contract_position": "Р‘Р°РЅРє Рё Р—Р°РєР°Р·С‡РёРє РІ СЂР°РјРєР°С… РЅР°СЃС‚РѕСЏС‰РµРіРѕ РљРѕРЅС‚СЂР°РєС‚Р° РѕР±РјРµРЅРёРІР°СЋС‚СЃСЏ РёРЅС„РѕСЂРјР°С†РёРµР№ Рё РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕРґРЅРёРј РёР· СЃР»РµРґСѓСЋС‰РёС… СЃРїРѕСЃРѕР±РѕРІ, РІС‹Р±РёСЂР°РµРјС‹С… РЎС‚РѕСЂРѕРЅРѕР№, РЅР°РїСЂР°РІР»СЏСЋС‰РµР№ РёРЅС„РѕСЂРјР°С†РёСЋ/РґРѕРєСѓРјРµРЅС‚ РїРѕ СЃРІРѕРµРјСѓ СѓСЃРјРѕС‚СЂРµРЅРёСЋ, РµСЃР»Рё РёРЅРѕРµ РЅРµ РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј:",
   133	  "source_evidence": "Р‘Р°РЅРє Рё Р—Р°РєР°Р·С‡РёРє РІ СЂР°РјРєР°С… РЅР°СЃС‚РѕСЏС‰РµРіРѕ РљРѕРЅС‚СЂР°РєС‚Р° РѕР±РјРµРЅРёРІР°СЋС‚СЃСЏ РёРЅС„РѕСЂРјР°С†РёРµР№ Рё РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕРґРЅРёРј РёР· СЃР»РµРґСѓСЋС‰РёС… СЃРїРѕСЃРѕР±РѕРІ, РІС‹Р±РёСЂР°РµРјС‹С… РЎС‚РѕСЂРѕРЅРѕР№, РЅР°РїСЂР°РІР»СЏСЋС‰РµР№ РёРЅС„РѕСЂРјР°С†РёСЋ/РґРѕРєСѓРјРµРЅС‚ РїРѕ СЃРІРѕРµРјСѓ СѓСЃРјРѕС‚СЂРµРЅРёСЋ, РµСЃР»Рё РёРЅРѕРµ РЅРµ РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј:",
   134	  "status": "extra_in_contract",
   135	  "risk_level": "medium",
   136	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   137	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   138	}
   139	{
   140	  "contract_id": "5.1",
   141	  "contract_position": "РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ",
   142	  "source_evidence": "Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·СѓРµС‚СЃСЏ:",
   143	  "status": "extra_in_contract",
   144	  "risk_level": "medium",
   145	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   146	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   147	}
   148	{
   149	  "contract_id": "5.2",
   150	  "contract_position": "РџСЂР°РІРѕ",
   151	  "source_evidence": "Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІРїСЂР°РІРµ:",
   152	  "status": "extra_in_contract",
   153	  "risk_level": "medium",
   154	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   155	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   156	}
   157	{
   158	  "contract_id": "5.2.9.1",
   159	  "contract_position": "РЅР°СЂСѓС€РµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј СѓСЃР»РѕРІРёР№ РљРѕРЅС‚СЂР°РєС‚Р°;",
   160	  "source_evidence": "РЅР°СЂСѓС€РµРЅРёРµ Р—Р°РєР°Р·С‡РёРєРѕРј СѓСЃР»РѕРІРёР№ РљРѕРЅС‚СЂР°РєС‚Р°;",
   161	  "status": "extra_in_contract",
   162	  "risk_level": "medium",
   163	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   164	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   165	}
   166	{
   167	  "contract_id": "5.2.9.2",
   168	  "contract_position": "РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… Р—Р°РєР°Р·С‡РёРєР° РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РІ РѕС‚РЅРѕС€РµРЅРёРё РєРѕС‚РѕСЂС‹С… РёРјРµСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕР± РёС… РїСЂРёС‡Р°СЃС‚РЅРѕСЃС‚Рё Рє СЌРєСЃС‚СЂРµРјРёСЃС‚СЃРєРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёСЋ СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЏ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ;",
   169	  "source_evidence": "РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… Р—Р°РєР°Р·С‡РёРєР° РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РІ РѕС‚РЅРѕС€РµРЅРёРё РєРѕС‚РѕСЂС‹С… РёРјРµСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕР± РёС… РїСЂРёС‡Р°СЃС‚РЅРѕСЃС‚Рё Рє СЌРєСЃС‚СЂРµРјРёСЃС‚СЃРєРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёСЋ СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЏ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ;",
   170	  "status": "extra_in_contract",
   171	  "risk_level": "medium",
   172	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   173	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   174	}
   175	{
   176	  "contract_id": "5.2.9.3",
   177	  "contract_position": "РїСЂРё РЅР°Р»РёС‡РёРё Сѓ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РїРѕРґРѕР·СЂРµРЅРёР№, С‡С‚Рѕ РћРїРµСЂР°С†РёРё РІ РўРЎРў СЃРѕРІРµСЂС€Р°СЋС‚СЃСЏ РІ С†РµР»СЏС… Р»РµРіР°Р»РёР·Р°С†РёРё (РѕС‚РјС‹РІР°РЅРёСЏ) РґРѕС…РѕРґРѕРІ, РїРѕР»СѓС‡РµРЅРЅС‹С… РїСЂРµСЃС‚СѓРїРЅС‹Рј РїСѓС‚РµРј, РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёСЏ С‚РµСЂСЂРѕСЂРёР·РјР°;",
   178	  "source_evidence": "РїСЂРё РЅР°Р»РёС‡РёРё Сѓ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РїРѕРґРѕР·СЂРµРЅРёР№, С‡С‚Рѕ РћРїРµСЂР°С†РёРё РІ РўРЎРў СЃРѕРІРµСЂС€Р°СЋС‚СЃСЏ РІ С†РµР»СЏС… Р»РµРіР°Р»РёР·Р°С†РёРё (РѕС‚РјС‹РІР°РЅРёСЏ) РґРѕС…РѕРґРѕРІ, РїРѕР»СѓС‡РµРЅРЅС‹С… РїСЂРµСЃС‚СѓРїРЅС‹Рј РїСѓС‚РµРј, РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёСЏ С‚РµСЂСЂРѕСЂРёР·РјР°;",
   179	  "status": "extra_in_contract",
   180	  "risk_level": "medium",
   181	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   182	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   183	}
   184	{
   185	  "contract_id": "5.2.9.4",
   186	  "contract_position": "РїРѕР»СѓС‡РµРЅРёРµ РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ Р—Р°РєР°Р·С‡РёРєРµ/РўРЎРў РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё Р Р¤ Рё/РёР»Рё РџР»Р°С‚РµР¶РЅС‹С… СЃРёСЃС‚РµРј;",
   187	  "source_evidence": "РїРѕР»СѓС‡РµРЅРёРµ РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ Р—Р°РєР°Р·С‡РёРєРµ/РўРЎРў РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё Р Р¤ Рё/РёР»Рё РџР»Р°С‚РµР¶РЅС‹С… СЃРёСЃС‚РµРј;",
   188	  "status": "extra_in_contract",
   189	  "risk_level": "medium",
   190	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   191	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   192	}
   193	{
   194	  "contract_id": "5.2.9.5",
   195	  "contract_position": "РїРѕР»СѓС‡РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ РІ РўРЎРў СЃС‚РѕСЂРѕРЅС‹ РґРѕРіРѕРІРѕСЂРёР»РёСЃСЊ, С‡С‚Рѕ РґРѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃРєРѕРіРѕ С…Р°СЂР°РєС‚РµСЂР° РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№ СЏРІР»СЏРµС‚СЃСЏ РёРЅС„РѕСЂРјР°С†РёСЏ, РїРѕСЃС‚СѓРїРёРІС€Р°СЏ РѕС‚ Р‘Р°РЅРєРѕРІ-СЌРјРёС‚РµРЅС‚РѕРІ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ, РёР»Рё СѓРІРµРґРѕРјР»РµРЅРёСЏ РѕС‚ РџР»Р°С‚РµР¶РЅС‹С… СЃРёСЃ",
   196	  "source_evidence": "РїРѕР»СѓС‡РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ РІ РўРЎРў СЃС‚РѕСЂРѕРЅС‹ РґРѕРіРѕРІРѕСЂРёР»РёСЃСЊ, С‡С‚Рѕ РґРѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃРєРѕРіРѕ С…Р°СЂР°РєС‚РµСЂР° РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№ СЏРІР»СЏРµС‚СЃСЏ РёРЅС„РѕСЂРјР°С†РёСЏ, РїРѕСЃС‚СѓРїРёРІС€Р°СЏ РѕС‚ Р‘Р°РЅРєРѕРІ-СЌРјРёС‚РµРЅС‚РѕРІ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ, РёР»Рё СѓРІРµРґРѕРјР»РµРЅРёСЏ РѕС‚ РџР»Р°С‚РµР¶РЅС‹С… СЃРёСЃ",
   197	  "status": "extra_in_contract",
   198	  "risk_level": "medium",
   199	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   200	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
AI: [{'name': 'read_file', 'args': {'file_path': '/large_tool_results/call_00_F9LPpckW9NuoQ8y8ZvyT9165', 'offset': 200, 'limit': 200}, 'id': 'call_00_F8kG4LUTwBp1MZd3AqDl3047', 'type': 'tool_call'}]
Tool:    201	}
   202	{
   203	  "contract_id": "5.2.9.6",
   204	  "contract_position": "РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЋ РћРїРµСЂР°С†РёР№;",
   205	  "source_evidence": "РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЋ РћРїРµСЂР°С†РёР№;",
   206	  "status": "extra_in_contract",
   207	  "risk_level": "medium",
   208	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   209	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   210	}
   211	{
   212	  "contract_id": "5.2.9.7",
   213	  "contract_position": "Р»РёРєРІРёРґР°С†РёСЏ Р—Р°РєР°Р·С‡РёРєР° Р»РёР±Рѕ РІРѕР·Р±СѓР¶РґРµРЅРёРµ РІ РѕС‚РЅРѕС€РµРЅРёРё Р—Р°РєР°Р·С‡РёРєР° РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 26.10.2002 в„– 127-Р¤Р— В«Рћ РЅРµСЃРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕСЃС‚Рё (Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ)В»;",
   214	  "source_evidence": "Р»РёРєРІРёРґР°С†РёСЏ Р—Р°РєР°Р·С‡РёРєР° Р»РёР±Рѕ РІРѕР·Р±СѓР¶РґРµРЅРёРµ РІ РѕС‚РЅРѕС€РµРЅРёРё Р—Р°РєР°Р·С‡РёРєР° РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 26.10.2002 в„– 127-Р¤Р— В«Рћ РЅРµСЃРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕСЃС‚Рё (Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ)В»;",
   215	  "status": "extra_in_contract",
   216	  "risk_level": "medium",
   217	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   218	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   219	}
   220	{
   221	  "contract_id": "5.2.9.8",
   222	  "contract_position": "РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ Р—Р°РєР°Р·С‡РёРєРµ/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё РљРѕРЅС‚СЂР°РєС‚Р°;",
   223	  "source_evidence": "РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ Р—Р°РєР°Р·С‡РёРєРµ/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё РљРѕРЅС‚СЂР°РєС‚Р°;",
   224	  "status": "extra_in_contract",
   225	  "risk_level": "medium",
   226	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   227	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   228	}
   229	{
   230	  "contract_id": "5.2.9.9",
   231	  "contract_position": "РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё Р—Р°РєР°Р·С‡РёРєР°, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў;",
   232	  "source_evidence": "РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё Р—Р°РєР°Р·С‡РёРєР°, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў;",
   233	  "status": "extra_in_contract",
   234	  "risk_level": "medium",
   235	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   236	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   237	}
   238	{
   239	  "contract_id": "5.2.9.10",
   240	  "contract_position": "РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ",
   241	  "source_evidence": "РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ",
   242	  "status": "extra_in_contract",
   243	  "risk_level": "medium",
   244	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   245	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   246	}
   247	{
   248	  "contract_id": "5.2.9.11",
   249	  "contract_position": "РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ РљРѕРЅС‚СЂР°РєС‚Р° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ РљРѕРЅС‚СЂР°РєС‚Р°.",
   250	  "source_evidence": "РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ РљРѕРЅС‚СЂР°РєС‚Р° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ РљРѕРЅС‚СЂР°РєС‚Р°.",
   251	  "status": "extra_in_contract",
   252	  "risk_level": "medium",
   253	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   254	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   255	}
   256	{
   257	  "contract_id": "5.3",
   258	  "contract_position": "РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ",
   259	  "source_evidence": "Р—Р°РєР°Р·С‡РёРє РѕР±СЏР·СѓРµС‚СЃСЏ:",
   260	  "status": "extra_in_contract",
   261	  "risk_level": "medium",
   262	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   263	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   264	}
   265	{
   266	  "contract_id": "5.3.18",
   267	  "contract_position": "РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РѕРїРµСЂР°С†РёР№ Сѓ Р·Р°РєР°Р·С‡РёРєР° РІ РўРЎРў (С‚РѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі):",
   268	  "source_evidence": "РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РѕРїРµСЂР°С†РёР№ Сѓ Р·Р°РєР°Р·С‡РёРєР° РІ РўРЎРў (С‚РѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі):",
   269	  "status": "extra_in_contract",
   270	  "risk_level": "medium",
   271	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   272	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   273	}
   274	{
   275	  "contract_id": "5.4",
   276	  "contract_position": "РџСЂР°РІРѕ",
   277	  "source_evidence": "Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ:",
   278	  "status": "extra_in_contract",
   279	  "risk_level": "medium",
   280	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   281	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   282	}
   283	{
   284	  "contract_id": "7.2",
   285	  "contract_position": "РџСЂР°РІРѕ",
   286	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІРїСЂР°РІРµ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ СѓРїР»Р°С‚С‹ РЅ",
   287	  "status": "extra_in_contract",
   288	  "risk_level": "low",
   289	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   290	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   291	}
   292	{
   293	  "contract_id": "7.7.2",
   294	  "contract_position": "Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РєР°Рє РїРѕР±РµРґРёС‚РµР»СЏ Р·Р°РєСѓРїРєРё (РёР»Рё РёРЅРѕРіРѕ СѓС‡Р°СЃС‚РЅРёРєР° Р·Р°РєСѓРїРєРё РІ СЃР»СѓС‡Р°СЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 05.04.2013 в„– 44-Р¤Р—), РїСЂРµРґР»РѕР¶РёРІС€РµРіРѕ РЅР°РёР±РѕР»РµРµ РІС‹СЃРѕРєСѓСЋ С†РµРЅСѓ Р·Р° РїСЂР°РІРѕ Р·Р°РєР»СЋС‡РµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р°, РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅ",
   295	  "source_evidence": "Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РєР°Рє РїРѕР±РµРґРёС‚РµР»СЏ Р·Р°РєСѓРїРєРё (РёР»Рё РёРЅРѕРіРѕ СѓС‡Р°СЃС‚РЅРёРєР° Р·Р°РєСѓРїРєРё РІ СЃР»СѓС‡Р°СЏС…, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 05.04.2013 в„– 44-Р¤Р—), РїСЂРµРґР»РѕР¶РёРІС€РµРіРѕ РЅР°РёР±РѕР»РµРµ РІС‹СЃРѕРєСѓСЋ С†РµРЅСѓ Р·Р° РїСЂР°РІРѕ Р·Р°РєР»СЋС‡РµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р°, РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅ",
   296	  "status": "extra_in_contract",
   297	  "risk_level": "low",
   298	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   299	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   300	}
   301	{
   302	  "contract_id": "10",
   303	  "contract_position": "РїСЂРѕС†РµРЅС‚РѕРІ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;",
   304	  "source_evidence": "РїСЂРѕС†РµРЅС‚РѕРІ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;",
   305	  "status": "extra_in_contract",
   306	  "risk_level": "medium",
   307	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   308	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   309	}
   310	{
   311	  "contract_id": "5",
   312	  "contract_position": "РїСЂРѕС†РµРЅС‚РѕРІ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);",
   313	  "source_evidence": "РїСЂРѕС†РµРЅС‚РѕРІ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);",
   314	  "status": "extra_in_contract",
   315	  "risk_level": "medium",
   316	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   317	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   318	}
   319	{
   320	  "contract_id": "1",
   321	  "contract_position": "РїСЂРѕС†РµРЅС‚ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ); Р±) РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РїСЂРµРІС‹С€Р°РµС‚ РЅР°С‡Р°Р»СЊРЅСѓСЋ (РјР°РєСЃРёРјР°Р»СЊРЅСѓСЋ) С†РµРЅСѓ РєРѕРЅС‚СЂР°РєС‚Р°:",
   322	  "source_evidence": "РїСЂРѕС†РµРЅС‚ РЅР°С‡Р°Р»СЊРЅРѕР№ (РјР°РєСЃРёРјР°Р»СЊРЅРѕР№) С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ); Р±) РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РїСЂРµРІС‹С€Р°РµС‚ РЅР°С‡Р°Р»СЊРЅСѓСЋ (РјР°РєСЃРёРјР°Р»СЊРЅСѓСЋ) С†РµРЅСѓ РєРѕРЅС‚СЂР°РєС‚Р°:",
   323	  "status": "extra_in_contract",
   324	  "risk_level": "medium",
   325	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   326	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   327	}
   328	{
   329	  "contract_id": "10",
   330	  "contract_position": "РїСЂРѕС†РµРЅС‚РѕРІ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;",
   331	  "source_evidence": "РїСЂРѕС†РµРЅС‚РѕРІ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;",
   332	  "status": "extra_in_contract",
   333	  "risk_level": "medium",
   334	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   335	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   336	}
   337	{
   338	  "contract_id": "5",
   339	  "contract_position": "РїСЂРѕС†РµРЅС‚РѕРІ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);",
   340	  "source_evidence": "РїСЂРѕС†РµРЅС‚РѕРІ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);",
   341	  "status": "extra_in_contract",
   342	  "risk_level": "medium",
   343	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   344	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   345	}
   346	{
   347	  "contract_id": "1",
   348	  "contract_position": "РїСЂРѕС†РµРЅС‚ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ).",
   349	  "source_evidence": "РїСЂРѕС†РµРЅС‚ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, РµСЃР»Рё С†РµРЅР° РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ).",
   350	  "status": "extra_in_contract",
   351	  "risk_level": "medium",
   352	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   353	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   354	}
   355	{
   356	  "contract_id": "7.7.3",
   357	  "contract_position": "Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ (РїСЂРё РЅР°Р»РёС‡РёРё РІ РљРѕРЅС‚СЂР°РєС‚Рµ С‚Р°РєРёС… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ), СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµ",
   358	  "source_evidence": "Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° РїРѕ РєР°Р¶РґРѕРјСѓ С„Р°РєС‚Сѓ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ (РїСЂРё РЅР°Р»РёС‡РёРё РІ РљРѕРЅС‚СЂР°РєС‚Рµ С‚Р°РєРёС… РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ), СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµ",
   359	  "status": "extra_in_contract",
   360	  "risk_level": "low",
   361	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   362	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   363	}
   364	{
   365	  "contract_id": "8.3.1",
   366	  "contract_position": "Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј, С„РѕСЂРјРёСЂСѓРµС‚ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјС‹, РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ (РґР°Р»РµРµ вЂ“ СѓСЃРёР»РµРЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅ",
   367	  "source_evidence": "Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј, С„РѕСЂРјРёСЂСѓРµС‚ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјС‹, РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ РєРІР°Р»РёС„РёС†РёСЂРѕРІР°РЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ (РґР°Р»РµРµ вЂ“ СѓСЃРёР»РµРЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅ",
   368	  "status": "extra_in_contract",
   369	  "risk_level": "low",
   370	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   371	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   372	}
   373	{
   374	  "contract_id": "8.4",
   375	  "contract_position": "Р”Р°С‚РѕР№ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј, СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° С‚Р°РєРѕРіРѕ РґРѕРєСѓРјРµРЅС‚Р° РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‡Р°СЃРѕРІРѕР№ Р·РѕРЅРѕР№, РІ РєРѕС‚РѕСЂРѕР№ СЂР°СЃРїРѕ",
   376	  "source_evidence": "Р”Р°С‚РѕР№ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј, СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° С‚Р°РєРѕРіРѕ РґРѕРєСѓРјРµРЅС‚Р° РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‡Р°СЃРѕРІРѕР№ Р·РѕРЅРѕР№, РІ РєРѕС‚РѕСЂРѕР№ СЂР°СЃРїРѕ",
   377	  "status": "extra_in_contract",
   378	  "risk_level": "low",
   379	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   380	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   381	}
   382	{
   383	  "contract_id": "8.5.1",
   384	  "contract_position": "Р—Р°РєР°Р·С‡РёРє РІ СЃСЂРѕРє РЅРµ Р±РѕР»РµРµ 10 (РґРµСЃСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃРѕ РґРЅСЏ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 3 С‡Р°СЃС‚Рё 13 СЃС‚Р°С‚СЊРё 94 Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° в„– 44-Р¤Р—, РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ",
   385	  "source_evidence": "Р—Р°РєР°Р·С‡РёРє РІ СЃСЂРѕРє РЅРµ Р±РѕР»РµРµ 10 (РґРµСЃСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃРѕ РґРЅСЏ РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 3 С‡Р°СЃС‚Рё 13 СЃС‚Р°С‚СЊРё 94 Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° в„– 44-Р¤Р—, РїСѓРЅРєС‚РѕРј 8.3.1. РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ",
   386	  "status": "extra_in_contract",
   387	  "risk_level": "low",
   388	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   389	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   390	}
   391	{
   392	  "contract_id": "8.5.2",
   393	  "contract_position": "РџРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ СѓРІРµРґРѕРјР»РµРЅРёСЋ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј Р—Р°РєР°Р·С‡РёРєР°, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РјРѕР¶РµС‚ РїСЂРѕРёР·РІРѕРґРёС‚СЊСЃСЏ С‚РѕР»СЊРєРѕ РІ РїСЂРёСЃСѓС‚СЃС‚РІРёРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, РёРјРµСЋС‰РµРіРѕ РЅР°РґР»РµР¶Р°С‰РёРј РѕР±СЂР°Р·РѕРј РѕС„РѕСЂРјР»РµРЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РЅР° СѓС‡Р°СЃС‚РёРµ РІ РїСЂРёРµРјРєРµ СЃ С‚РѕС‡РЅРѕ РѕРіРѕРІРѕСЂРµРЅРЅС‹РјРё РїРѕР»РЅРѕ",
   394	  "source_evidence": "РџРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ СѓРІРµРґРѕРјР»РµРЅРёСЋ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј Р—Р°РєР°Р·С‡РёРєР°, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РјРѕР¶РµС‚ РїСЂРѕРёР·РІРѕРґРёС‚СЊСЃСЏ С‚РѕР»СЊРєРѕ РІ РїСЂРёСЃСѓС‚СЃС‚РІРёРё РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ, РёРјРµСЋС‰РµРіРѕ РЅР°РґР»РµР¶Р°С‰РёРј РѕР±СЂР°Р·РѕРј РѕС„РѕСЂРјР»РµРЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РЅР° СѓС‡Р°СЃС‚РёРµ РІ РїСЂРёРµРјРєРµ СЃ С‚РѕС‡РЅРѕ РѕРіРѕРІРѕСЂРµРЅРЅС‹РјРё РїРѕР»РЅРѕ",
   395	  "status": "extra_in_contract",
   396	  "risk_level": "low",
   397	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   398	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   399	}
   400	{
AI: Now let me read the coverage_ledger and summary sections, plus the remaining unmatched_contract items.[{'name': 'read_file', 'args': {'file_path': '/large_tool_results/call_00_F9LPpckW9NuoQ8y8ZvyT9165', 'offset': 400, 'limit': 300}, 'id': 'call_00_hXpNLnMI0tbCsehJXOoY9873', 'type': 'tool_call'}]
Tool:    401	  "contract_id": "8.5.3",
   402	  "contract_position": "Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РїРѕСЃС‚СѓРїРёР»Рѕ СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Р№ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРє, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ РІ РґРІСѓСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.",
   403	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё РїРѕСЃС‚СѓРїРёР»Рѕ СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Р№ РљРѕРЅС‚СЂР°РєС‚РѕРј СЃСЂРѕРє, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ РІ РґРІСѓСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.",
   404	  "status": "extra_in_contract",
   405	  "risk_level": "low",
   406	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   407	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   408	}
   409	{
   410	  "contract_id": "8.5.4",
   411	  "contract_position": "Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РЅРµ РїРѕСЃС‚СѓРїРёР»Рѕ, Р»РёР±Рѕ РїРѕСЃС‚СѓРїРёР»Рѕ РІ Р±РѕР»РµРµ РїРѕР·РґРЅРёР№ СЃСЂРѕРє, С‡РµРј РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Р—Р°РєР°Р·С‡РёРєРѕРј РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.",
   412	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± СѓС‡Р°СЃС‚РёРё РІ РїСЂРёРµРјРєРµ РЅРµ РїРѕСЃС‚СѓРїРёР»Рѕ, Р»РёР±Рѕ РїРѕСЃС‚СѓРїРёР»Рѕ РІ Р±РѕР»РµРµ РїРѕР·РґРЅРёР№ СЃСЂРѕРє, С‡РµРј РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРѕ РљРѕРЅС‚СЂР°РєС‚РѕРј, РїСЂРёРµРјРєР° РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Р—Р°РєР°Р·С‡РёРєРѕРј РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.",
   413	  "status": "extra_in_contract",
   414	  "risk_level": "low",
   415	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   416	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   417	}
   418	{
   419	  "contract_id": "8.5.5",
   420	  "contract_position": "Р”Р»СЏ РїСЂРѕРІРµСЂРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РІ С‡Р°СЃС‚Рё РёС… СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р°, Р—Р°РєР°Р·С‡РёРє РїСЂРѕРІРѕРґРёС‚ СЌРєСЃРїРµСЂС‚РёР·Сѓ.",
   421	  "source_evidence": "Р”Р»СЏ РїСЂРѕРІРµСЂРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РІ С‡Р°СЃС‚Рё РёС… СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р°, Р—Р°РєР°Р·С‡РёРє РїСЂРѕРІРѕРґРёС‚ СЌРєСЃРїРµСЂС‚РёР·Сѓ.",
   422	  "status": "extra_in_contract",
   423	  "risk_level": "medium",
   424	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   425	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   426	}
   427	{
   428	  "contract_id": "8.5.6",
   429	  "contract_position": "Р­РєСЃРїРµСЂС‚РёР·Р° СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РјРѕР¶РµС‚ РїСЂРѕРІРѕРґРёС‚СЊСЃСЏ Р—Р°РєР°Р·С‡РёРєРѕРј СЃРІРѕРёРјРё СЃРёР»Р°РјРё РёР»Рё Рє РµРµ РїСЂРѕРІРµРґРµРЅРёСЋ РјРѕРіСѓС‚ РїСЂРёРІР»РµРєР°С‚СЊСЃСЏ СЌРєСЃРїРµСЂС‚С‹, СЌРєСЃРїРµСЂС‚РЅС‹Рµ РѕСЂРіР°РЅРёР·Р°С†РёРё РЅР° РѕСЃРЅРѕРІР°РЅРёРё РєРѕРЅС‚СЂР°РєС‚РѕРІ, Р·Р°РєР»СЋС‡РµРЅРЅС‹С… РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј",
   430	  "source_evidence": "Р­РєСЃРїРµСЂС‚РёР·Р° СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… РљРѕРЅС‚СЂР°РєС‚РѕРј, РјРѕР¶РµС‚ РїСЂРѕРІРѕРґРёС‚СЊСЃСЏ Р—Р°РєР°Р·С‡РёРєРѕРј СЃРІРѕРёРјРё СЃРёР»Р°РјРё РёР»Рё Рє РµРµ РїСЂРѕРІРµРґРµРЅРёСЋ РјРѕРіСѓС‚ РїСЂРёРІР»РµРєР°С‚СЊСЃСЏ СЌРєСЃРїРµСЂС‚С‹, СЌРєСЃРїРµСЂС‚РЅС‹Рµ РѕСЂРіР°РЅРёР·Р°С†РёРё РЅР° РѕСЃРЅРѕРІР°РЅРёРё РєРѕРЅС‚СЂР°РєС‚РѕРІ, Р·Р°РєР»СЋС‡РµРЅРЅС‹С… РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј",
   431	  "status": "extra_in_contract",
   432	  "risk_level": "low",
   433	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   434	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   435	}
   436	{
   437	  "contract_id": "8.5.7",
   438	  "contract_position": "Р’ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р·Р°РјРµС‡Р°РЅРёР№ Р—Р°РєР°Р·С‡РёРє (СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅРѕРµ Р»РёС†Рѕ) РІ С‚РµС‡РµРЅРёРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹, СЃР»РµРґСѓСЋС‰РµР№ Р·Р° РґРЅРµРј РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.4 РљРѕРЅС‚СЂР°РєС‚Р° РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ Р»РёС†Р°, РёРјРµ",
   439	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р·Р°РјРµС‡Р°РЅРёР№ Р—Р°РєР°Р·С‡РёРє (СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅРѕРµ Р»РёС†Рѕ) РІ С‚РµС‡РµРЅРёРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹, СЃР»РµРґСѓСЋС‰РµР№ Р·Р° РґРЅРµРј РїРѕСЃС‚СѓРїР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.4 РљРѕРЅС‚СЂР°РєС‚Р° РїРѕРґРїРёСЃС‹РІР°РµС‚ СѓСЃРёР»РµРЅРЅРѕР№ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕРґРїРёСЃСЊСЋ Р»РёС†Р°, РёРјРµ",
   440	  "status": "extra_in_contract",
   441	  "risk_level": "low",
   442	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   443	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   444	}
   445	{
   446	  "contract_id": "8.5.8",
   447	  "contract_position": "Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј Р±СѓРґСѓС‚ СѓСЃС‚Р°РЅРѕРІР»РµРЅС‹ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ С‚СЂРµР±РѕРІР°РЅРёСЏРј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ РљРѕРЅС‚СЂР°РєС‚Рµ, РґР°Р»СЊРЅРµР№С€Р°СЏ РїСЂРёРµРјРєР° РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊСЃСЏ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№. РќРµ РїРѕР·РґРЅРµРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№, СЃР»РµРґСѓСЋС‰РёС… Р·Р° РґРЅРµРј РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ Рґ",
   448	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј Р±СѓРґСѓС‚ СѓСЃС‚Р°РЅРѕРІР»РµРЅС‹ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ С‚СЂРµР±РѕРІР°РЅРёСЏРј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ РљРѕРЅС‚СЂР°РєС‚Рµ, РґР°Р»СЊРЅРµР№С€Р°СЏ РїСЂРёРµРјРєР° РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊСЃСЏ РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№. РќРµ РїРѕР·РґРЅРµРµ РґРµСЃСЏС‚Рё СЂР°Р±РѕС‡РёС… РґРЅРµР№, СЃР»РµРґСѓСЋС‰РёС… Р·Р° РґРЅРµРј РїРѕСЃС‚СѓРїР»РµРЅРёСЏ Р—Р°РєР°Р·С‡РёРєСѓ Рґ",
   449	  "status": "extra_in_contract",
   450	  "risk_level": "low",
   451	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   452	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   453	}
   454	{
   455	  "contract_id": "8.5.9",
   456	  "contract_position": "РџСЂР°РІРѕ",
   457	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ РїРѕР»СѓС‡РµРЅРёСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚РѕРј 8.5.8. РљРѕРЅС‚СЂР°РєС‚Р° РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРіРѕ РѕС‚РєР°Р·Р° РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РІРїСЂР°РІРµ СѓСЃС‚СЂР°РЅРёС‚СЊ РїСЂРёС‡РёРЅС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ С‚Р°РєРѕРј РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅРѕРј РѕС‚РєР°Р·Рµ, Рё РЅР°РїСЂР°РІРёС‚СЊ Р·Р°РєР°Р·С‡РёРєСѓ РёСЃРїСЂР°РІР»РµРЅРЅС‹Р№ РґРѕРєСѓРјРµРЅС‚",
   458	  "status": "extra_in_contract",
   459	  "risk_level": "low",
   460	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   461	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   462	}
   463	{
   464	  "contract_id": "8.6",
   465	  "contract_position": "Р”Р°С‚РѕР№ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј РёР»Рё РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ Р—Р°РєР°Р·С‡РёРєР°.",
   466	  "source_evidence": "Р”Р°С‚РѕР№ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі СЃС‡РёС‚Р°РµС‚СЃСЏ РґР°С‚Р° СЂР°Р·РјРµС‰РµРЅРёСЏ РІ РµРґРёРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ СЃРёСЃС‚РµРјРµ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ, РїРѕРґРїРёСЃР°РЅРЅРѕРіРѕ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј Р»РёС†РѕРј РёР»Рё РїСЂРёРµРјРѕС‡РЅРѕР№ РєРѕРјРёСЃСЃРёРµР№ Р—Р°РєР°Р·С‡РёРєР°.",
   467	  "status": "extra_in_contract",
   468	  "risk_level": "low",
   469	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   470	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   471	}
   472	{
   473	  "contract_id": "8.7",
   474	  "contract_position": "Р’РЅРµСЃРµРЅРёРµ РёСЃРїСЂР°РІР»РµРЅРёР№ РІ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ, РѕС„РѕСЂРјР»РµРЅРЅС‹Р№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°СЃС‚РѕСЏС‰РёРј СЂР°Р·РґРµР»РѕРј РљРѕРЅС‚СЂР°РєС‚Р°, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСѓС‚РµРј С„РѕСЂРјРёСЂРѕРІР°РЅРёСЏ, РїРѕРґРїРёСЃР°РЅРёСЏ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹С… Р»РёС†, РёРјРµСЋС‰РёС… РїСЂР°РІРѕ РґРµР№СЃС‚РІРѕРІР°С‚СЊ РѕС‚ РёРјРµРЅРё Р�СЃРї",
   475	  "source_evidence": "Р’РЅРµСЃРµРЅРёРµ РёСЃРїСЂР°РІР»РµРЅРёР№ РІ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ, РѕС„РѕСЂРјР»РµРЅРЅС‹Р№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°СЃС‚РѕСЏС‰РёРј СЂР°Р·РґРµР»РѕРј РљРѕРЅС‚СЂР°РєС‚Р°, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСѓС‚РµРј С„РѕСЂРјРёСЂРѕРІР°РЅРёСЏ, РїРѕРґРїРёСЃР°РЅРёСЏ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹С… Р»РёС†, РёРјРµСЋС‰РёС… РїСЂР°РІРѕ РґРµР№СЃС‚РІРѕРІР°С‚СЊ РѕС‚ РёРјРµРЅРё Р�СЃРї",
   476	  "status": "extra_in_contract",
   477	  "risk_level": "low",
   478	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   479	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   480	}
   481	{
   482	  "contract_id": "8.8",
   483	  "contract_position": "РћС„РѕСЂРјР»РµРЅРёРµ СЂРµР·СѓР»СЊС‚Р°С‚Р° РїСЂРѕРІРµРґРµРЅРёСЏ РїСЂРѕС†РµРґСѓСЂС‹ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ Рё РІ СЃСЂРѕРєРё, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ РЅР°СЃС‚РѕСЏС‰РµРј СЂР°Р·РґРµР»Рµ РљРѕРЅС‚СЂР°РєС‚Р°.",
   484	  "source_evidence": "РћС„РѕСЂРјР»РµРЅРёРµ СЂРµР·СѓР»СЊС‚Р°С‚Р° РїСЂРѕРІРµРґРµРЅРёСЏ РїСЂРѕС†РµРґСѓСЂС‹ РїСЂРёРµРјРєРё РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ РїРѕСЂСЏРґРєРµ Рё РІ СЃСЂРѕРєРё, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ РЅР°СЃС‚РѕСЏС‰РµРј СЂР°Р·РґРµР»Рµ РљРѕРЅС‚СЂР°РєС‚Р°.",
   485	  "status": "extra_in_contract",
   486	  "risk_level": "low",
   487	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   488	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   489	}
   490	{
   491	  "contract_id": "8.9",
   492	  "contract_position": "РџСЂР°РІРѕ",
   493	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё СѓСЃР»РѕРІРёСЏРј РљРѕРЅС‚СЂР°РєС‚Р° Р—Р°РєР°Р·С‡РёРє РІРїСЂР°РІРµ РЅРµ РѕС‚РєР°Р·С‹РІР°С‚СЊ РІ РїСЂРёРµРјРєРµ РѕРєР°Р·Р°РЅРЅРѕР№ СѓСЃР»СѓРіРё, РµСЃР»Рё РІС‹СЏРІР»РµРЅРЅРѕРµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РїСЂРёРµРјРєРµ Рё СѓСЃС‚СЂР°РЅРµРЅРѕ Р�СЃРїРѕР»РЅРёС‚РµР»РµРј.",
   494	  "status": "extra_in_contract",
   495	  "risk_level": "low",
   496	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   497	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   498	}
   499	{
   500	  "contract_id": "8.10",
   501	  "contract_position": "Р’ СЃР»СѓС‡Р°Рµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР° Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·Р°РЅ Р±РµР·РІРѕР·РјРµР·РґРЅРѕ СѓСЃС‚СЂР°РЅРёС‚СЊ РЅРµРґРѕСЃС‚Р°С‚РєРё РІ С‚РµС‡РµРЅРёРµ 3 РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°СЏРІР»РµРЅРёСЏ Рѕ РЅРёС… Р—Р°РєР°Р·С‡РёРєРѕРј.",
   502	  "source_evidence": "Р’ СЃР»СѓС‡Р°Рµ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РєР°С‡РµСЃС‚РІР° Р�СЃРїРѕР»РЅРёС‚РµР»СЊ РѕР±СЏР·Р°РЅ Р±РµР·РІРѕР·РјРµР·РґРЅРѕ СѓСЃС‚СЂР°РЅРёС‚СЊ РЅРµРґРѕСЃС‚Р°С‚РєРё РІ С‚РµС‡РµРЅРёРµ 3 РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°СЏРІР»РµРЅРёСЏ Рѕ РЅРёС… Р—Р°РєР°Р·С‡РёРєРѕРј.",
   503	  "status": "extra_in_contract",
   504	  "risk_level": "medium",
   505	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   506	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   507	}
   508	{
   509	  "contract_id": "8.11",
   510	  "contract_position": "РџРѕРґРїРёСЃР°РЅРЅС‹Р№ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё Р—Р°РєР°Р·С‡РёРєР° Рё Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РѕРїР»Р°С‚С‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі.",
   511	  "source_evidence": "РџРѕРґРїРёСЃР°РЅРЅС‹Р№ СѓСЃРёР»РµРЅРЅС‹РјРё СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РїРѕРґРїРёСЃСЏРјРё Р—Р°РєР°Р·С‡РёРєР° Рё Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёРµРјРєРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РѕРїР»Р°С‚С‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЋ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі.",
   512	  "status": "extra_in_contract",
   513	  "risk_level": "low",
   514	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   515	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   516	}
   517	{
   518	  "contract_id": "354340",
   519	  "contract_position": ", Рі. РЎРѕС‡Рё, РђРґР»РµСЂСЃРєРёР№ СЂР°Р№РѕРЅ СѓР». РљР°СЂР»Р° РњР°СЂРєСЃР°, Рґ.8 Р�РќРќ 2317026788 РљРџРџ231701001 РћР“Р Рќ: 1022302723409 СЂ\\СЃ 03214643000000011800 Р±Р°РЅРє РїРѕР»СѓС‡Р°С‚РµР»СЊ: Р®Р¶РЅРѕРµ Р“РЈ Р±Р°РЅРєР° Р РѕСЃСЃРёРё//РЈР¤Рљ РїРѕ РљСЂР°СЃРЅРѕРґР°СЂСЃРєРѕРјСѓ РєСЂР°СЋ Рі.РљСЂР°СЃРЅРѕРґР°СЂ (Р»/СЃ 20186X56810) Р‘Р�Рљ РўРћР¤Рљ 010349101 Р•Рљ",
   520	  "source_evidence": ", Рі. РЎРѕС‡Рё, РђРґР»РµСЂСЃРєРёР№ СЂР°Р№РѕРЅ СѓР». РљР°СЂР»Р° РњР°СЂРєСЃР°, Рґ.8 Р�РќРќ 2317026788 РљРџРџ231701001 РћР“Р Рќ: 1022302723409 СЂ\\СЃ 03214643000000011800 Р±Р°РЅРє РїРѕР»СѓС‡Р°С‚РµР»СЊ: Р®Р¶РЅРѕРµ Р“РЈ Р±Р°РЅРєР° Р РѕСЃСЃРёРё//РЈР¤Рљ РїРѕ РљСЂР°СЃРЅРѕРґР°СЂСЃРєРѕРјСѓ РєСЂР°СЋ Рі.РљСЂР°СЃРЅРѕРґР°СЂ (Р»/СЃ 20186X56810) Р‘Р�Рљ РўРћР¤Рљ 010349101 Р•Рљ",
   521	  "status": "extra_in_contract",
   522	  "risk_level": "medium",
   523	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   524	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   525	}
   526	{
   527	  "contract_id": "1",
   528	  "contract_position": "РћР±СЉРµРєС‚РѕРј Р·Р°РєСѓРїРєРё СЏРІР»СЏРµС‚СЃСЏ: РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РїРѕ РїСЂРёРµРјСѓ Рє РѕРїР»Р°С‚Рµ РїР»Р°С‚РµР¶РЅС‹С… (Р±Р°РЅРєРѕРІСЃРєРёС…) РєР°СЂС‚ РІ РєР°С‡РµСЃС‚РІРµ СЃСЂРµРґСЃС‚РІР° РѕРїР»Р°С‚С‹ СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј Р±Р°РЅРєРѕРІСЃРєРёС… РєР°СЂС‚ (СѓСЃР»СѓРіРё СЌРєРІР°Р№СЂРёРЅРіР°) (РґР°Р»РµРµ РїРѕ С‚РµРєСЃС‚Сѓ- СѓСЃР»СѓРіР°, СЌРєРІР°Р№СЂРёРЅРі) РґР»СЏ РЅСѓР¶Рґ Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ РіРѕСЃСѓРґР°",
   529	  "source_evidence": "РћР±СЉРµРєС‚РѕРј Р·Р°РєСѓРїРєРё СЏРІР»СЏРµС‚СЃСЏ: РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РїРѕ РїСЂРёРµРјСѓ Рє РѕРїР»Р°С‚Рµ РїР»Р°С‚РµР¶РЅС‹С… (Р±Р°РЅРєРѕРІСЃРєРёС…) РєР°СЂС‚ РІ РєР°С‡РµСЃС‚РІРµ СЃСЂРµРґСЃС‚РІР° РѕРїР»Р°С‚С‹ СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј Р±Р°РЅРєРѕРІСЃРєРёС… РєР°СЂС‚ (СѓСЃР»СѓРіРё СЌРєРІР°Р№СЂРёРЅРіР°) (РґР°Р»РµРµ РїРѕ С‚РµРєСЃС‚Сѓ- СѓСЃР»СѓРіР°, СЌРєРІР°Р№СЂРёРЅРі) РґР»СЏ РЅСѓР¶Рґ Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ РіРѕСЃСѓРґР°",
   530	  "status": "extra_in_contract",
   531	  "risk_level": "medium",
   532	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   533	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   534	}
   535	{
   536	  "contract_id": "2",
   537	  "contract_position": "РњРµСЃС‚РѕРїРѕР»РѕР¶РµРЅРёРµ С‚РѕС‡РµРє РїСЂРёРµРјР° Р—Р°РєР°Р·С‡РёРєР° СѓСЃС‚Р°РЅРѕРІРєРё СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі, Р° С‚Р°РєР¶Рµ РєРѕР»РёС‡РµСЃС‚РІРѕ РЅРµРѕР±С…РѕРґРёРјС‹С… СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ (POS-С‚РµСЂРјРёРЅР°Р»РѕРІ): в„– Рї/Рї РђРґСЂРµСЃ РѕР±СЉРµРєС‚Р° Р—Р°РєР°Р·С‡РёРєР°, РЅР° РєРѕС‚РѕСЂС‹С… РЅРµРѕР±С…РѕРґРёРјРѕ СѓСЃС‚Р°РЅРѕРІРёС‚СЊ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂ",
   538	  "source_evidence": "РњРµСЃС‚РѕРїРѕР»РѕР¶РµРЅРёРµ С‚РѕС‡РµРє РїСЂРёРµРјР° Р—Р°РєР°Р·С‡РёРєР° СѓСЃС‚Р°РЅРѕРІРєРё СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі, Р° С‚Р°РєР¶Рµ РєРѕР»РёС‡РµСЃС‚РІРѕ РЅРµРѕР±С…РѕРґРёРјС‹С… СЌР»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ (POS-С‚РµСЂРјРёРЅР°Р»РѕРІ): в„– Рї/Рї РђРґСЂРµСЃ РѕР±СЉРµРєС‚Р° Р—Р°РєР°Р·С‡РёРєР°, РЅР° РєРѕС‚РѕСЂС‹С… РЅРµРѕР±С…РѕРґРёРјРѕ СѓСЃС‚Р°РЅРѕРІРёС‚СЊ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂ",
   539	  "status": "extra_in_contract",
   540	  "risk_level": "medium",
   541	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   542	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   543	}
   544	{
   545	  "contract_id": "3",
   546	  "contract_position": "РџРµСЂРµС‡РµРЅСЊ РєР°СЂС‚, РєРѕС‚РѕСЂС‹Рµ СЃРµСЂРІРёСЃРЅР°СЏ С‚РѕС‡РєР° РїСЂРёРЅРёРјР°РµС‚ РІ РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі: в„–Рї/Рї РќР°РёРјРµРЅРѕРІР°РЅРёРµ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ 1 РќР°С†РёРѕРЅР°Р»СЊРЅР°СЏ СЃРёСЃС‚РµРјР° РїР»Р°С‚РµР¶РЅС‹С… РєР°СЂС‚ В«РњР�Р В» 2 VISA International Service Association 3 MasterCard (MasterCard, MasterCard Electronic, Maest",
   547	  "source_evidence": "РџРµСЂРµС‡РµРЅСЊ РєР°СЂС‚, РєРѕС‚РѕСЂС‹Рµ СЃРµСЂРІРёСЃРЅР°СЏ С‚РѕС‡РєР° РїСЂРёРЅРёРјР°РµС‚ РІ РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі: в„–Рї/Рї РќР°РёРјРµРЅРѕРІР°РЅРёРµ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ 1 РќР°С†РёРѕРЅР°Р»СЊРЅР°СЏ СЃРёСЃС‚РµРјР° РїР»Р°С‚РµР¶РЅС‹С… РєР°СЂС‚ В«РњР�Р В» 2 VISA International Service Association 3 MasterCard (MasterCard, MasterCard Electronic, Maest",
   548	  "status": "extra_in_contract",
   549	  "risk_level": "medium",
   550	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   551	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   552	}
   553	{
   554	  "contract_id": "4",
   555	  "contract_position": "РЎСЂРѕРєРё РѕРєР°Р·Р°РЅРёСЏ РЈСЃР»СѓРі: РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃ В«01В» РјР°СЂС‚Р° 2025 РіРѕРґР° РїРѕ В«30В» РЅРѕСЏР±СЂСЏ 2025 РіРѕРґР° (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ) РёР»Рё РґРѕ РјРѕРјРµРЅС‚Р° РёСЃС‡РµСЂРїР°РЅРёСЏ РїСЂРµРґРµР»СЊРЅРѕР№ Р¦РµРЅС‹ РљРѕРЅС‚СЂР°РєС‚Р°, СѓРєР°Р·Р°РЅРЅРѕР№ РІ Рї. в„– 3.1. РљРѕРЅС‚СЂР°РєС‚Р°, РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ С‚РѕРіРѕ, РєР°РєРѕРµ РёР· СЃРѕР±С‹С‚РёР№",
   556	  "source_evidence": "РЎСЂРѕРєРё РѕРєР°Р·Р°РЅРёСЏ РЈСЃР»СѓРі: РћРєР°Р·Р°РЅРёРµ СѓСЃР»СѓРі РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃ В«01В» РјР°СЂС‚Р° 2025 РіРѕРґР° РїРѕ В«30В» РЅРѕСЏР±СЂСЏ 2025 РіРѕРґР° (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ) РёР»Рё РґРѕ РјРѕРјРµРЅС‚Р° РёСЃС‡РµСЂРїР°РЅРёСЏ РїСЂРµРґРµР»СЊРЅРѕР№ Р¦РµРЅС‹ РљРѕРЅС‚СЂР°РєС‚Р°, СѓРєР°Р·Р°РЅРЅРѕР№ РІ Рї. в„– 3.1. РљРѕРЅС‚СЂР°РєС‚Р°, РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ С‚РѕРіРѕ, РєР°РєРѕРµ РёР· СЃРѕР±С‹С‚РёР№",
   557	  "status": "extra_in_contract",
   558	  "risk_level": "medium",
   559	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   560	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   561	}
   562	{
   563	  "contract_id": "5",
   564	  "contract_position": "РЈСЃР»РѕРІРёСЏ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі: РљРѕРјРёСЃСЃРёСЏ Р·Р° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ- РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚. РђР±РѕРЅРµРЅС‚СЃРєР°СЏ РїР»Р°С‚Р° Р·Р° РїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµСЂРјРёРЅР°Р»Р°РјРё - РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚. РўРµСЂРјРёРЅР°Р»С‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕР»Р¶РЅС‹ РёРјРµС‚СЊ РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїСЂРёРЅСЏС‚РёСЏ Р±РµСЃРєРѕРЅС‚Р°РєС‚РЅРѕР№ РѕРїР»Р°С‚С‹ Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ РІС‹РІРѕРґР° QR-РєРѕРґР° ",
   565	  "source_evidence": "РЈСЃР»РѕРІРёСЏ РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі: РљРѕРјРёСЃСЃРёСЏ Р·Р° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ- РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚. РђР±РѕРЅРµРЅС‚СЃРєР°СЏ РїР»Р°С‚Р° Р·Р° РїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµСЂРјРёРЅР°Р»Р°РјРё - РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚. РўРµСЂРјРёРЅР°Р»С‹ Р�СЃРїРѕР»РЅРёС‚РµР»СЏ РґРѕР»Р¶РЅС‹ РёРјРµС‚СЊ РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїСЂРёРЅСЏС‚РёСЏ Р±РµСЃРєРѕРЅС‚Р°РєС‚РЅРѕР№ РѕРїР»Р°С‚С‹ Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ РІС‹РІРѕРґР° QR-РєРѕРґР° ",
   566	  "status": "extra_in_contract",
   567	  "risk_level": "low",
   568	  "risk": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ 44-Р¤Р— / РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р°, РЅРµ РёРјРµСЋС‰РµРµ Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   569	  "materiality_reason": "РћР±СЏР·Р°С‚РµР»СЊРЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ РїСѓР±Р»РёС‡РЅРѕРіРѕ РєРѕРЅС‚СЂР°РєС‚Р° (44-Р¤Р—)"
   570	}
   571	{
   572	  "contract_id": "9.2.1",
   573	  "contract_position": "РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРІРїР°РґРµРЅРёСЏ РёС‚РѕРіРѕРІ РёР»Рё С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃР±РѕСЏ СЂР°Р±РѕС‚РЅРёРє РўРЎРў: a) СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµС‚ РљРѕРЅС‚СЂРѕР»СЊРЅСѓСЋ Р»РµРЅС‚Сѓ; b) РїСЂРѕРІРµСЂСЏРµС‚ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РёРЅС„РѕСЂРјР°С†РёРё РІ РљРѕРЅС‚СЂРѕР»СЊРЅРѕР№ Р»РµРЅС‚Рµ СЃ СЂРµР°Р»СЊРЅРѕ РїСЂРѕРІРµРґРµРЅРЅС‹РјРё РћРїРµСЂР°С†РёСЏРјРё; c) СЃС‚Р°РІРёС‚ СЃРІРѕСЋ РїРѕРґРїРёСЃСЊ РЅР° РљРѕРЅС‚СЂРѕР»СЊРЅРѕР№ Р»РµРЅС‚Рµ Рё Рї",
   574	  "source_evidence": "РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРІРїР°РґРµРЅРёСЏ РёС‚РѕРіРѕРІ РёР»Рё С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃР±РѕСЏ СЂР°Р±РѕС‚РЅРёРє РўРЎРў: a) СЂР°СЃРїРµС‡Р°С‚С‹РІР°РµС‚ РљРѕРЅС‚СЂРѕР»СЊРЅСѓСЋ Р»РµРЅС‚Сѓ; b) РїСЂРѕРІРµСЂСЏРµС‚ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РёРЅС„РѕСЂРјР°С†РёРё РІ РљРѕРЅС‚СЂРѕР»СЊРЅРѕР№ Р»РµРЅС‚Рµ СЃ СЂРµР°Р»СЊРЅРѕ РїСЂРѕРІРµРґРµРЅРЅС‹РјРё РћРїРµСЂР°С†РёСЏРјРё; c) СЃС‚Р°РІРёС‚ СЃРІРѕСЋ РїРѕРґРїРёСЃСЊ РЅР° РљРѕРЅС‚СЂРѕР»СЊРЅРѕР№ Р»РµРЅС‚Рµ Рё Рї",
   575	  "status": "extra_in_contract",
   576	  "risk_level": "medium",
   577	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   578	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   579	}
   580	{
   581	  "contract_id": "1",
   582	  "contract_position": "РЎР’Р•Р”Р•РќР�РЇ Рћ РџР Р•Р”РџР Р�РЇРўР�Р� РќР°РёРјРµРЅРѕРІР°РЅРёРµ: ______________________________ (СѓРєР°Р·С‹РІР°РµС‚СЃСЏ РїРѕР»РЅРѕРµ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓС‡СЂРµРґРёС‚РµР»СЊРЅС‹РјРё РґРѕРєСѓРјРµРЅС‚Р°РјРё) Р�РќРќ: РљРџРџ: РљР‘Рљ: РћРљРђРўРћ: Р РѕРґ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ: СЂ/СЃ Рє/СЃ Р‘Р�Рљ 010349101 РђР”Р Р•РЎ Р Р•Р“Р�РЎРўР РђР¦Р�Р� (Сѓ",
   583	  "source_evidence": "РЎР’Р•Р”Р•РќР�РЇ Рћ РџР Р•Р”РџР Р�РЇРўР�Р� РќР°РёРјРµРЅРѕРІР°РЅРёРµ: ______________________________ (СѓРєР°Р·С‹РІР°РµС‚СЃСЏ РїРѕР»РЅРѕРµ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓС‡СЂРµРґРёС‚РµР»СЊРЅС‹РјРё РґРѕРєСѓРјРµРЅС‚Р°РјРё) Р�РќРќ: РљРџРџ: РљР‘Рљ: РћРљРђРўРћ: Р РѕРґ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ: СЂ/СЃ Рє/СЃ Р‘Р�Рљ 010349101 РђР”Р Р•РЎ Р Р•Р“Р�РЎРўР РђР¦Р�Р� (Сѓ",
   584	  "status": "extra_in_contract",
   585	  "risk_level": "medium",
   586	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   587	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   588	}
   589	{
   590	  "contract_id": "2",
   591	  "contract_position": "Р�РќР¤РћР РњРђР¦Р�РЇ РћР‘ РЈРЎР›РЈР“РђРҐ ВЁ РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі + Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» + QR-РєРѕРґ ВЁ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі + SberPay Online + РџР»Р°С‚РµР¶РЅС‹Рµ СЂРµС€РµРЅРёСЏ: ВЁ Р�РЅС‚РµСЂРЅРµС‚ СЃР°Р№С‚ http://__________ ВЁ РњРѕР±РёР»СЊРЅРѕРµ РїСЂРёР»РѕР¶РµРЅРёРµ http://__________ ВЁ SberPay Online ВЁ Р�РЅС‚РµСЂРЅРµС‚ СЃР°Р№",
   592	  "source_evidence": "Р�РќР¤РћР РњРђР¦Р�РЇ РћР‘ РЈРЎР›РЈР“РђРҐ ВЁ РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі + Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» + QR-РєРѕРґ ВЁ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі + SberPay Online + РџР»Р°С‚РµР¶РЅС‹Рµ СЂРµС€РµРЅРёСЏ: ВЁ Р�РЅС‚РµСЂРЅРµС‚ СЃР°Р№С‚ http://__________ ВЁ РњРѕР±РёР»СЊРЅРѕРµ РїСЂРёР»РѕР¶РµРЅРёРµ http://__________ ВЁ SberPay Online ВЁ Р�РЅС‚РµСЂРЅРµС‚ СЃР°Р№",
   593	  "status": "extra_in_contract",
   594	  "risk_level": "medium",
   595	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   596	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   597	}
   598	{
   599	  "contract_id": "3",
   600	  "contract_position": "РџРћР”РўР’Р•Р Р–Р”Р•РќР�Р• Р—РђРљР›Р®Р§Р•РќР�РЇ РљРћРќРўР РђРљРўРђ",
   601	  "source_evidence": "РџРћР”РўР’Р•Р Р–Р”Р•РќР�Р• Р—РђРљР›Р®Р§Р•РќР�РЇ РљРћРќРўР РђРљРўРђ",
   602	  "status": "extra_in_contract",
   603	  "risk_level": "medium",
   604	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   605	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   606	}
   607	{
   608	  "contract_id": "1.2",
   609	  "contract_position": "РџСЂР°РІРѕ",
   610	  "source_evidence": "РЎРѕРіР»Р°СЃРЅРѕ, С‡С‚Рѕ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃРІРµРґРµРЅРёСЏ, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р—Р°СЏРІР»РµРЅРёРё Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹С… РґРѕРєСѓРјРµРЅС‚Р°С….",
   611	  "status": "extra_in_contract",
   612	  "risk_level": "medium",
   613	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   614	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   615	}
   616	{
   617	  "contract_id": "4",
   618	  "contract_position": "РћРўРњР•РўРљР� Р‘РђРќРљРђ _______________________ ______________________________________ ______________________________________ (СѓРєР°Р·С‹РІР°РµС‚СЃСЏ РЅРѕРјРµСЂ/РЅР°РёРјРµРЅРѕРІР°РЅРёРµ, РјРµСЃС‚Рѕ РЅР°С…РѕР¶РґРµРЅРёСЏ Р“РћРЎР‘ РїРѕ РјРµСЃС‚Сѓ РѕС„РѕСЂРјР»РµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р°) Р‘Р°РЅРє РїРѕР»СѓС‡Р°С‚РµР»СЏ ____________ Р‘Р�Рљ Р‘Р°РЅРєР°",
   619	  "source_evidence": "РћРўРњР•РўРљР� Р‘РђРќРљРђ _______________________ ______________________________________ ______________________________________ (СѓРєР°Р·С‹РІР°РµС‚СЃСЏ РЅРѕРјРµСЂ/РЅР°РёРјРµРЅРѕРІР°РЅРёРµ, РјРµСЃС‚Рѕ РЅР°С…РѕР¶РґРµРЅРёСЏ Р“РћРЎР‘ РїРѕ РјРµСЃС‚Сѓ РѕС„РѕСЂРјР»РµРЅРёСЏ РљРѕРЅС‚СЂР°РєС‚Р°) Р‘Р°РЅРє РїРѕР»СѓС‡Р°С‚РµР»СЏ ____________ Р‘Р�Рљ Р‘Р°РЅРєР°",
   620	  "status": "extra_in_contract",
   621	  "risk_level": "medium",
   622	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   623	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   624	}
   625	{
   626	  "contract_id": "10",
   627	  "contract_position": "000 РўРµР»РµС„РѕРЅ РґР»СЏ РѕС‚СЂР°Р¶РµРЅРёСЏ РІ С‡РµРєРµ РЅРµС‚ РљРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂР° (РІ С‚РѕРј С‡РёСЃР»Рµ РґР»СЏ РЅР°РїСЂР°РІР»РµРЅРёСЏ РїР°СЂРѕР»РµР№ Рё РєРѕРґРѕРІ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ РґР»СЏ РЅР°СЃС‚СЂРѕР№РєРё РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°) РўРµР»РµС„РѕРЅ E-mail РљРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ РґР»СЏ Р»РёС‡РЅРѕРіРѕ РєР°Р±РёРЅРµС‚Р° РћРїРµСЂР°С‚РѕСЂР° С„РёСЃРєР°Р»СЊРЅС‹С… РґР°РЅРЅС‹",
   628	  "source_evidence": "000 РўРµР»РµС„РѕРЅ РґР»СЏ РѕС‚СЂР°Р¶РµРЅРёСЏ РІ С‡РµРєРµ РЅРµС‚ РљРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂР° (РІ С‚РѕРј С‡РёСЃР»Рµ РґР»СЏ РЅР°РїСЂР°РІР»РµРЅРёСЏ РїР°СЂРѕР»РµР№ Рё РєРѕРґРѕРІ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ РґР»СЏ РЅР°СЃС‚СЂРѕР№РєРё РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°) РўРµР»РµС„РѕРЅ E-mail РљРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ РґР»СЏ Р»РёС‡РЅРѕРіРѕ РєР°Р±РёРЅРµС‚Р° РћРїРµСЂР°С‚РѕСЂР° С„РёСЃРєР°Р»СЊРЅС‹С… РґР°РЅРЅС‹",
   629	  "status": "extra_in_contract",
   630	  "risk_level": "medium",
   631	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   632	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   633	}
   634	{
   635	  "contract_id": "1",
   636	  "contract_position": "900 000,00 РњР°РєСЃРёРјР°Р»СЊРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, СЂСѓР±.",
   637	  "source_evidence": "900 000,00 РњР°РєСЃРёРјР°Р»СЊРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ С†РµРЅС‹ РєРѕРЅС‚СЂР°РєС‚Р°, СЂСѓР±.",
   638	  "status": "extra_in_contract",
   639	  "risk_level": "medium",
   640	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   641	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   642	}
   643	{
   644	  "contract_id": "1",
   645	  "contract_position": "900 000,00 Р—Р°РєР°Р·С‡РёРє: Р¤Р“Р‘РЈ В«РљР°РІРєР°Р·СЃРєРёР№ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅС‹Р№ Р·Р°РїРѕРІРµРґРЅРёРєВ» РћС‚ В«Р‘Р°РЅРєР°/Р�СЃРїРѕР»РЅРёС‚РµР»СЏВ»:",
   646	  "source_evidence": "900 000,00 Р—Р°РєР°Р·С‡РёРє: Р¤Р“Р‘РЈ В«РљР°РІРєР°Р·СЃРєРёР№ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅС‹Р№ Р·Р°РїРѕРІРµРґРЅРёРєВ» РћС‚ В«Р‘Р°РЅРєР°/Р�СЃРїРѕР»РЅРёС‚РµР»СЏВ»:",
   647	  "status": "extra_in_contract",
   648	  "risk_level": "medium",
   649	  "risk": "РЈСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ Р‘Р°РЅРєР°",
   650	  "materiality_reason": "РџРѕР»РѕР¶РµРЅРёРµ РёРјРµРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РїСЂР°РІРѕРІРѕРµ Р·РЅР°С‡РµРЅРёРµ"
   651	}
   652	
   653	=== COVERAGE_LEDGER MATRIX ===
   654	{"matrix_id": "2.1", "closure": "linked", "link_indices": [0], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   655	{"matrix_id": "2.2", "closure": "linked", "link_indices": [1], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   656	{"matrix_id": "2.3.1", "closure": "linked", "link_indices": [2], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   657	{"matrix_id": "2.3.2", "closure": "linked", "link_indices": [3], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   658	{"matrix_id": "2.3.3", "closure": "linked", "link_indices": [4], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   659	{"matrix_id": "2.3.4", "closure": "linked", "link_indices": [5], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   660	{"matrix_id": "2.3.5", "closure": "linked", "link_indices": [6], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   661	{"matrix_id": "2.3.6", "closure": "linked", "link_indices": [7], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   662	{"matrix_id": "2.3.7", "closure": "linked", "link_indices": [8], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   663	{"matrix_id": "2.4", "closure": "linked", "link_indices": [9], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   664	{"matrix_id": "2.5.1.1", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   665	{"matrix_id": "2.5.2.1", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=common, payment_method=sber_pay_face_scan)"}
   666	{"matrix_id": "2.6.1.1", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=qr)"}
   667	{"matrix_id": "2.6.2.1", "closure": "out_of_scope", "link_indices": [], "reason": "РњР°С‚СЂРёС†Р° С‚СЂРµР±СѓРµС‚ РЎРћР‘РЎРўР’Р•РќРќР«РҐ С‚РµСЂРјРёРЅР°Р»РѕРІ РџСЂРµРґРїСЂРёСЏС‚РёСЏ. РљРѕРЅС‚СЂР°РєС‚ РёСЃРїРѕР»СЊР·СѓРµС‚ С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° - С‚СЂРµР±РѕРІР°РЅРёРµ РЅРµ РїСЂРёРјРµРЅРёРјРѕ."}
   668	{"matrix_id": "2.6.2.2", "closure": "out_of_scope", "link_indices": [], "reason": "РњР°С‚СЂРёС†Р° С‚СЂРµР±СѓРµС‚ РЎРћР‘РЎРўР’Р•РќРќР«РҐ С‚РµСЂРјРёРЅР°Р»РѕРІ РџСЂРµРґРїСЂРёСЏС‚РёСЏ. РљРѕРЅС‚СЂР°РєС‚ РёСЃРїРѕР»СЊР·СѓРµС‚ С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° - С‚СЂРµР±РѕРІР°РЅРёРµ РЅРµ РїСЂРёРјРµРЅРёРјРѕ."}
   669	{"matrix_id": "2.6.3.1", "closure": "linked", "link_indices": [10], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   670	{"matrix_id": "2.6.3.2", "closure": "linked", "link_indices": [11], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   671	{"matrix_id": "2.7", "closure": "linked", "link_indices": [12], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   672	{"matrix_id": "3.1", "closure": "linked", "link_indices": [13], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   673	{"matrix_id": "3.2", "closure": "linked", "link_indices": [14], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   674	{"matrix_id": "3.3", "closure": "linked", "link_indices": [15], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   675	{"matrix_id": "4.1.1", "closure": "linked", "link_indices": [16], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   676	{"matrix_id": "4.1.2", "closure": "linked", "link_indices": [17], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   677	{"matrix_id": "4.1.3", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=common, payment_method=qr_sber_pay)"}
   678	{"matrix_id": "4.2.1", "closure": "linked", "link_indices": [18], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   679	{"matrix_id": "4.2.2", "closure": "linked", "link_indices": [19], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   680	{"matrix_id": "4.2.3", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=common, terminal=common, payment_method=common)"}
   681	{"matrix_id": "4.2.4", "closure": "linked", "link_indices": [20], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   682	{"matrix_id": "4.2.5", "closure": "linked", "link_indices": [21], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   683	{"matrix_id": "4.2.6", "closure": "linked", "link_indices": [22], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   684	{"matrix_id": "4.2.7", "closure": "linked", "link_indices": [23], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   685	{"matrix_id": "4.2.8", "closure": "linked", "link_indices": [24], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   686	{"matrix_id": "4.2.9", "closure": "linked", "link_indices": [25], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   687	{"matrix_id": "4.2.10", "closure": "linked", "link_indices": [26], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   688	{"matrix_id": "4.2.11", "closure": "linked", "link_indices": [27], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   689	{"matrix_id": "4.2.12", "closure": "linked", "link_indices": [149], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   690	{"matrix_id": "4.2.13", "closure": "linked", "link_indices": [28], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   691	{"matrix_id": "4.2.14", "closure": "linked", "link_indices": [29], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   692	{"matrix_id": "4.2.15", "closure": "linked", "link_indices": [30], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   693	{"matrix_id": "4.2.16.1", "closure": "linked", "link_indices": [31], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   694	{"matrix_id": "4.2.16.2", "closure": "linked", "link_indices": [32], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   695	{"matrix_id": "4.2.16.3", "closure": "linked", "link_indices": [33], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   696	{"matrix_id": "4.2.17", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   697	{"matrix_id": "4.2.18", "closure": "linked", "link_indices": [34], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   698	{"matrix_id": "4.2.19", "closure": "linked", "link_indices": [35], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   699	{"matrix_id": "4.2.20.1", "closure": "linked", "link_indices": [36], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   700	{"matrix_id": "4.2.20.2", "closure": "linked", "link_indices": [37], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
AI: Now let me read the rest of the coverage_ledger and summary:[{'name': 'read_file', 'args': {'file_path': '/large_tool_results/call_00_F9LPpckW9NuoQ8y8ZvyT9165', 'offset': 700, 'limit': 400}, 'id': 'call_00_a4ttxiW53UjB6gcrU3QY9659', 'type': 'tool_call'}]
Tool:    701	{"matrix_id": "4.2.20.3", "closure": "linked", "link_indices": [38], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   702	{"matrix_id": "4.2.20.4", "closure": "linked", "link_indices": [39], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   703	{"matrix_id": "4.2.20.5", "closure": "linked", "link_indices": [40], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   704	{"matrix_id": "4.2.20.6", "closure": "linked", "link_indices": [41], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   705	{"matrix_id": "4.2.20.7", "closure": "linked", "link_indices": [42], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   706	{"matrix_id": "4.2.21.1", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   707	{"matrix_id": "4.2.21.2", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   708	{"matrix_id": "4.2.21.3", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   709	{"matrix_id": "4.2.21.4", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   710	{"matrix_id": "4.2.21.5", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   711	{"matrix_id": "4.2.21.6", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   712	{"matrix_id": "4.2.21.7", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   713	{"matrix_id": "4.2.21.8", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   714	{"matrix_id": "4.2.22", "closure": "linked", "link_indices": [145], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   715	{"matrix_id": "4.2.23", "closure": "linked", "link_indices": [146], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   716	{"matrix_id": "4.2.24", "closure": "linked", "link_indices": [147], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   717	{"matrix_id": "4.2.25", "closure": "linked", "link_indices": [148], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   718	{"matrix_id": "4.2.26", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   719	{"matrix_id": "5.1.1.1", "closure": "linked", "link_indices": [43], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   720	{"matrix_id": "5.1.1.2", "closure": "linked", "link_indices": [44], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   721	{"matrix_id": "5.1.1.3", "closure": "linked", "link_indices": [45], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   722	{"matrix_id": "5.1.1.4", "closure": "linked", "link_indices": [46], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   723	{"matrix_id": "5.1.1.5", "closure": "linked", "link_indices": [47], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   724	{"matrix_id": "5.1.1.6", "closure": "linked", "link_indices": [48], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   725	{"matrix_id": "5.1.2", "closure": "linked", "link_indices": [49], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   726	{"matrix_id": "5.1.3", "closure": "linked", "link_indices": [50], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   727	{"matrix_id": "5.1.4", "closure": "linked", "link_indices": [51], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   728	{"matrix_id": "5.1.5", "closure": "linked", "link_indices": [52], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   729	{"matrix_id": "5.1.6", "closure": "linked", "link_indices": [53], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   730	{"matrix_id": "5.1.7", "closure": "linked", "link_indices": [54], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   731	{"matrix_id": "5.1.8.1", "closure": "linked", "link_indices": [55], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   732	{"matrix_id": "5.1.8.2", "closure": "linked", "link_indices": [56], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   733	{"matrix_id": "5.1.8.3", "closure": "linked", "link_indices": [57], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   734	{"matrix_id": "5.1.8.4", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   735	{"matrix_id": "5.1.8.5", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   736	{"matrix_id": "5.1.8.6", "closure": "linked", "link_indices": [60], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   737	{"matrix_id": "5.1.8.7", "closure": "linked", "link_indices": [61], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   738	{"matrix_id": "5.1.8.8", "closure": "linked", "link_indices": [62], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   739	{"matrix_id": "5.1.8.9", "closure": "linked", "link_indices": [63], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   740	{"matrix_id": "5.1.8.10", "closure": "linked", "link_indices": [64], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   741	{"matrix_id": "5.1.8.11", "closure": "linked", "link_indices": [65], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   742	{"matrix_id": "5.1.8.12", "closure": "linked", "link_indices": [66], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   743	{"matrix_id": "5.1.8.13", "closure": "linked", "link_indices": [67], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   744	{"matrix_id": "5.1.9", "closure": "linked", "link_indices": [68], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   745	{"matrix_id": "5.1.10", "closure": "linked", "link_indices": [69], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   746	{"matrix_id": "5.1.11", "closure": "linked", "link_indices": [70], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   747	{"matrix_id": "5.1.12", "closure": "linked", "link_indices": [71], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   748	{"matrix_id": "5.1.13", "closure": "linked", "link_indices": [72], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   749	{"matrix_id": "5.1.14", "closure": "linked", "link_indices": [73], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   750	{"matrix_id": "5.1.15", "closure": "linked", "link_indices": [74], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   751	{"matrix_id": "5.1.16", "closure": "linked", "link_indices": [75], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   752	{"matrix_id": "5.1.17.1", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=pos, payment_method=common)"}
   753	{"matrix_id": "5.1.17.2", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   754	{"matrix_id": "5.2.1", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   755	{"matrix_id": "5.2.2", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   756	{"matrix_id": "5.2.3", "closure": "linked", "link_indices": [78], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   757	{"matrix_id": "5.2.4", "closure": "linked", "link_indices": [79], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   758	{"matrix_id": "5.2.5", "closure": "linked", "link_indices": [80], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   759	{"matrix_id": "5.2.6", "closure": "linked", "link_indices": [81], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   760	{"matrix_id": "5.2.7", "closure": "linked", "link_indices": [82], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   761	{"matrix_id": "5.2.8", "closure": "linked", "link_indices": [83], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   762	{"matrix_id": "5.2.9", "closure": "linked", "link_indices": [84], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   763	{"matrix_id": "5.2.10", "closure": "linked", "link_indices": [85], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   764	{"matrix_id": "5.2.12", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=qr)"}
   765	{"matrix_id": "6.1", "closure": "linked", "link_indices": [87], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   766	{"matrix_id": "6.2", "closure": "linked", "link_indices": [88], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   767	{"matrix_id": "6.3", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=common, terminal=common, payment_method=common)"}
   768	{"matrix_id": "6.4", "closure": "linked", "link_indices": [90], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   769	{"matrix_id": "6.5", "closure": "linked", "link_indices": [91], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   770	{"matrix_id": "6.6", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=common, terminal=common, payment_method=common)"}
   771	{"matrix_id": "6.7", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   772	{"matrix_id": "6.8", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   773	{"matrix_id": "6.9", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   774	{"matrix_id": "6.10", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   775	{"matrix_id": "6.11", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   776	{"matrix_id": "6.12", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   777	{"matrix_id": "6.13", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   778	{"matrix_id": "6.14", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   779	{"matrix_id": "6.15", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   780	{"matrix_id": "6.16", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   781	{"matrix_id": "6.17", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   782	{"matrix_id": "6.18", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=trade_acquiring, terminal=smart, payment_method=common)"}
   783	{"matrix_id": "6.20", "closure": "linked", "link_indices": [105], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   784	{"matrix_id": "6.21", "closure": "linked", "link_indices": [106], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   785	{"matrix_id": "7.1", "closure": "linked", "link_indices": [107], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   786	{"matrix_id": "7.2", "closure": "linked", "link_indices": [108], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   787	{"matrix_id": "7.3", "closure": "linked", "link_indices": [109], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   788	{"matrix_id": "7.4", "closure": "linked", "link_indices": [110], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   789	{"matrix_id": "7.5", "closure": "linked", "link_indices": [111], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   790	{"matrix_id": "7.6", "closure": "linked", "link_indices": [112], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   791	{"matrix_id": "7.7", "closure": "linked", "link_indices": [113], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   792	{"matrix_id": "7.8", "closure": "linked", "link_indices": [114], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   793	{"matrix_id": "7.9", "closure": "linked", "link_indices": [115], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   794	{"matrix_id": "7.10", "closure": "linked", "link_indices": [116], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   795	{"matrix_id": "7.11", "closure": "linked", "link_indices": [117], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   796	{"matrix_id": "7.12", "closure": "linked", "link_indices": [118], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   797	{"matrix_id": "7.13", "closure": "out_of_scope", "link_indices": [], "reason": "РќРµ РїСЂРёРјРµРЅРёРјРѕ Рє РїСЂРѕС„РёР»СЋ РєРѕРЅС‚СЂР°РєС‚Р° (product=internet_acquiring, terminal=common, payment_method=common)"}
   798	{"matrix_id": "7.14", "closure": "linked", "link_indices": [120], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   799	{"matrix_id": "7.15", "closure": "linked", "link_indices": [121], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   800	{"matrix_id": "7.16", "closure": "linked", "link_indices": [122], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   801	{"matrix_id": "7.17", "closure": "linked", "link_indices": [123], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   802	{"matrix_id": "8.1", "closure": "linked", "link_indices": [124], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   803	{"matrix_id": "8.2", "closure": "linked", "link_indices": [125], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   804	{"matrix_id": "9.1", "closure": "linked", "link_indices": [126], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   805	{"matrix_id": "9.2", "closure": "linked", "link_indices": [127], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   806	{"matrix_id": "9.3", "closure": "linked", "link_indices": [128], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   807	{"matrix_id": "10.1", "closure": "linked", "link_indices": [129], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   808	{"matrix_id": "10.2", "closure": "linked", "link_indices": [130], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   809	{"matrix_id": "10.3", "closure": "linked", "link_indices": [131], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   810	{"matrix_id": "11.1", "closure": "linked", "link_indices": [132], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   811	{"matrix_id": "11.2", "closure": "linked", "link_indices": [133], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   812	{"matrix_id": "11.3", "closure": "linked", "link_indices": [134], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   813	{"matrix_id": "11.4", "closure": "linked", "link_indices": [135], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   814	{"matrix_id": "11.5", "closure": "linked", "link_indices": [136], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   815	{"matrix_id": "11.6", "closure": "linked", "link_indices": [137], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   816	{"matrix_id": "11.7", "closure": "linked", "link_indices": [138], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   817	{"matrix_id": "11.8", "closure": "linked", "link_indices": [139], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   818	{"matrix_id": "11.9", "closure": "linked", "link_indices": [140], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   819	{"matrix_id": "11.10", "closure": "linked", "link_indices": [141], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   820	{"matrix_id": "11.11", "closure": "linked", "link_indices": [142], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   821	{"matrix_id": "11.12", "closure": "linked", "link_indices": [143], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   822	{"matrix_id": "11.13", "closure": "linked", "link_indices": [144], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РєРѕРЅС‚СЂР°РєС‚РѕРј"}
   823	
   824	=== COVERAGE_LEDGER CONTRACT ===
   825	{"contract_id": "1", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   826	{"contract_id": "1.1", "closure": "linked", "link_indices": [9], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   827	{"contract_id": "1.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   828	{"contract_id": "1.3", "closure": "linked", "link_indices": [13], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   829	{"contract_id": "2", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   830	{"contract_id": "2.1", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   831	{"contract_id": "2.1.1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   832	{"contract_id": "2.1.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   833	{"contract_id": "2.1.3", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   834	{"contract_id": "2.1.4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   835	{"contract_id": "2.1.5", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   836	{"contract_id": "2.1.6", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   837	{"contract_id": "2.1.7", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   838	{"contract_id": "2.1.8", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   839	{"contract_id": "2.1.9", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   840	{"contract_id": "2.1.10", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   841	{"contract_id": "2.1.11", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   842	{"contract_id": "2.1.12", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   843	{"contract_id": "2.1.13", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   844	{"contract_id": "2.1.14", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   845	{"contract_id": "2.1.15", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   846	{"contract_id": "2.1.16", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   847	{"contract_id": "2.1.17", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   848	{"contract_id": "2.1.18", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   849	{"contract_id": "2.1.19", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   850	{"contract_id": "2.1.20", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   851	{"contract_id": "2.1.21", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   852	{"contract_id": "2.1.22", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   853	{"contract_id": "2.1.23", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   854	{"contract_id": "2.1.24", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   855	{"contract_id": "2.1.25", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   856	{"contract_id": "2.1.26", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   857	{"contract_id": "2.1.27", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   858	{"contract_id": "2.1.28", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   859	{"contract_id": "2.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   860	{"contract_id": "2.3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   861	{"contract_id": "2.3.1", "closure": "linked", "link_indices": [2, 11], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   862	{"contract_id": "2.3.2", "closure": "linked", "link_indices": [3, 11], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   863	{"contract_id": "2.3.3", "closure": "linked", "link_indices": [4], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   864	{"contract_id": "2.3.4", "closure": "linked", "link_indices": [5], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   865	{"contract_id": "2.3.5", "closure": "linked", "link_indices": [6], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   866	{"contract_id": "2.3.6", "closure": "linked", "link_indices": [7], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   867	{"contract_id": "2.3.7", "closure": "linked", "link_indices": [8, 11], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   868	{"contract_id": "3", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   869	{"contract_id": "3.1", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   870	{"contract_id": "3.1.1", "closure": "linked", "link_indices": [89, 97], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   871	{"contract_id": "3.2", "closure": "linked", "link_indices": [15, 18, 75, 87], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   872	{"contract_id": "3.3", "closure": "linked", "link_indices": [98], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   873	{"contract_id": "4", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   874	{"contract_id": "4.1", "closure": "linked", "link_indices": [99], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   875	{"contract_id": "4.2", "closure": "linked", "link_indices": [100, 103, 104], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   876	{"contract_id": "4.3", "closure": "linked", "link_indices": [0, 101, 102], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   877	{"contract_id": "4.4", "closure": "linked", "link_indices": [93, 94, 95], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   878	{"contract_id": "4.5", "closure": "linked", "link_indices": [15, 18, 90, 91], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   879	{"contract_id": "4.5.1", "closure": "linked", "link_indices": [92], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   880	{"contract_id": "5", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   881	{"contract_id": "5.1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   882	{"contract_id": "5.1.1", "closure": "linked", "link_indices": [55, 72, 73, 142], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   883	{"contract_id": "5.1.2", "closure": "linked", "link_indices": [56], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   884	{"contract_id": "5.1.3", "closure": "linked", "link_indices": [57], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   885	{"contract_id": "5.1.4", "closure": "linked", "link_indices": [58], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   886	{"contract_id": "5.1.5", "closure": "linked", "link_indices": [59], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   887	{"contract_id": "5.1.6", "closure": "linked", "link_indices": [60], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   888	{"contract_id": "5.1.7", "closure": "linked", "link_indices": [61], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   889	{"contract_id": "5.1.8", "closure": "linked", "link_indices": [1, 14, 62, 63, 64], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   890	{"contract_id": "5.1.9", "closure": "linked", "link_indices": [65], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   891	{"contract_id": "5.1.10", "closure": "linked", "link_indices": [14, 66], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   892	{"contract_id": "5.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   893	{"contract_id": "5.2.1", "closure": "linked", "link_indices": [49], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   894	{"contract_id": "5.2.2", "closure": "linked", "link_indices": [50], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   895	{"contract_id": "5.2.3", "closure": "linked", "link_indices": [51], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   896	{"contract_id": "5.2.4", "closure": "linked", "link_indices": [52], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   897	{"contract_id": "5.2.5", "closure": "linked", "link_indices": [53], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   898	{"contract_id": "5.2.6", "closure": "linked", "link_indices": [54], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   899	{"contract_id": "5.2.7", "closure": "linked", "link_indices": [71], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   900	{"contract_id": "5.2.8", "closure": "linked", "link_indices": [70], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   901	{"contract_id": "5.2.9", "closure": "linked", "link_indices": [0, 68], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   902	{"contract_id": "5.2.9.1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   903	{"contract_id": "5.2.9.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   904	{"contract_id": "5.2.9.3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   905	{"contract_id": "5.2.9.4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   906	{"contract_id": "5.2.9.5", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   907	{"contract_id": "5.2.9.6", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   908	{"contract_id": "5.2.9.7", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   909	{"contract_id": "5.2.9.8", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   910	{"contract_id": "5.2.9.9", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   911	{"contract_id": "5.2.9.10", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   912	{"contract_id": "5.2.9.11", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   913	{"contract_id": "5.2.10", "closure": "linked", "link_indices": [69], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   914	{"contract_id": "5.2.10.1", "closure": "linked", "link_indices": [43], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   915	{"contract_id": "5.2.10.2", "closure": "linked", "link_indices": [44], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   916	{"contract_id": "5.2.10.3", "closure": "linked", "link_indices": [45], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   917	{"contract_id": "5.2.10.4", "closure": "linked", "link_indices": [46], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   918	{"contract_id": "5.2.10.5", "closure": "linked", "link_indices": [47], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   919	{"contract_id": "5.3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   920	{"contract_id": "5.3.1", "closure": "linked", "link_indices": [85], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   921	{"contract_id": "5.3.2", "closure": "linked", "link_indices": [18], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   922	{"contract_id": "5.3.3", "closure": "linked", "link_indices": [83], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   923	{"contract_id": "5.3.4", "closure": "linked", "link_indices": [84], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   924	{"contract_id": "5.3.5", "closure": "linked", "link_indices": [81], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   925	{"contract_id": "5.3.6", "closure": "linked", "link_indices": [82], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   926	{"contract_id": "5.3.7", "closure": "linked", "link_indices": [13, 20], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   927	{"contract_id": "5.3.8", "closure": "linked", "link_indices": [13, 21, 22], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   928	{"contract_id": "5.3.9", "closure": "linked", "link_indices": [23], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   929	{"contract_id": "5.3.10", "closure": "linked", "link_indices": [19, 25], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   930	{"contract_id": "5.3.11", "closure": "linked", "link_indices": [26], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   931	{"contract_id": "5.3.12", "closure": "linked", "link_indices": [27], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   932	{"contract_id": "5.3.13", "closure": "linked", "link_indices": [29], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   933	{"contract_id": "5.3.14", "closure": "linked", "link_indices": [30], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   934	{"contract_id": "5.3.15", "closure": "linked", "link_indices": [33], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   935	{"contract_id": "5.3.16", "closure": "linked", "link_indices": [34], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   936	{"contract_id": "5.3.17", "closure": "linked", "link_indices": [35], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   937	{"contract_id": "5.3.18", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   938	{"contract_id": "5.3.18.1", "closure": "linked", "link_indices": [37], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   939	{"contract_id": "5.3.18.2", "closure": "linked", "link_indices": [38], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   940	{"contract_id": "5.3.18.3", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   941	{"contract_id": "5.3.20.4", "closure": "linked", "link_indices": [40], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   942	{"contract_id": "5.3.18.5", "closure": "linked", "link_indices": [41], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   943	{"contract_id": "5.3.19", "closure": "linked", "link_indices": [28, 114], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   944	{"contract_id": "5.3.20", "closure": "linked", "link_indices": [31, 32], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   945	{"contract_id": "5.4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   946	{"contract_id": "5.4.1", "closure": "linked", "link_indices": [76], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   947	{"contract_id": "5.4.2", "closure": "linked", "link_indices": [77], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   948	{"contract_id": "5.4.3", "closure": "linked", "link_indices": [78], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   949	{"contract_id": "5.4.4", "closure": "linked", "link_indices": [79], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   950	{"contract_id": "5.4.5", "closure": "linked", "link_indices": [16, 80], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   951	{"contract_id": "5.5", "closure": "linked", "link_indices": [27], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   952	{"contract_id": "5.6", "closure": "linked", "link_indices": [41], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   953	{"contract_id": "5.7", "closure": "linked", "link_indices": [42, 48], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   954	{"contract_id": "5.9", "closure": "linked", "link_indices": [17, 86], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   955	{"contract_id": "5.10", "closure": "linked", "link_indices": [19, 36], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   956	{"contract_id": "6", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   957	{"contract_id": "6.1", "closure": "linked", "link_indices": [143], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   958	{"contract_id": "7", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   959	{"contract_id": "7.1", "closure": "linked", "link_indices": [107, 115, 123], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   960	{"contract_id": "7.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   961	{"contract_id": "7.3", "closure": "linked", "link_indices": [108], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   962	{"contract_id": "7.4", "closure": "linked", "link_indices": [109], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   963	{"contract_id": "7.4.1", "closure": "linked", "link_indices": [109], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   964	{"contract_id": "7.5", "closure": "linked", "link_indices": [122], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   965	{"contract_id": "7.6", "closure": "linked", "link_indices": [110], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   966	{"contract_id": "7.7", "closure": "linked", "link_indices": [111], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   967	{"contract_id": "7.7.1", "closure": "linked", "link_indices": [111], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   968	{"contract_id": "7.7.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   969	{"contract_id": "10", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   970	{"contract_id": "5", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   971	{"contract_id": "1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   972	{"contract_id": "10", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   973	{"contract_id": "5", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   974	{"contract_id": "1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   975	{"contract_id": "7.7.3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   976	{"contract_id": "7.8", "closure": "linked", "link_indices": [74, 119], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   977	{"contract_id": "7.9", "closure": "linked", "link_indices": [113], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   978	{"contract_id": "7.10", "closure": "linked", "link_indices": [112], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   979	{"contract_id": "7.11", "closure": "linked", "link_indices": [112], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   980	{"contract_id": "7.12", "closure": "linked", "link_indices": [120], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   981	{"contract_id": "8", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   982	{"contract_id": "8.1", "closure": "linked", "link_indices": [124], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   983	{"contract_id": "8.2", "closure": "linked", "link_indices": [121], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   984	{"contract_id": "8.3", "closure": "linked", "link_indices": [125], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   985	{"contract_id": "8.3.1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   986	{"contract_id": "8.3.2", "closure": "linked", "link_indices": [9, 88], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
   987	{"contract_id": "8.4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   988	{"contract_id": "8.5", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
   989	{"contract_id": "8.5.1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   990	{"contract_id": "8.5.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   991	{"contract_id": "8.5.3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   992	{"contract_id": "8.5.4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   993	{"contract_id": "8.5.5", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   994	{"contract_id": "8.5.6", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   995	{"contract_id": "8.5.7", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   996	{"contract_id": "8.5.8", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   997	{"contract_id": "8.5.9", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   998	{"contract_id": "8.6", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
   999	{"contract_id": "8.7", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1000	{"contract_id": "8.8", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1001	{"contract_id": "8.9", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1002	{"contract_id": "8.10", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1003	{"contract_id": "8.11", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1004	{"contract_id": "9", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
  1005	{"contract_id": "9.1", "closure": "linked", "link_indices": [115], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1006	{"contract_id": "9.2", "closure": "linked", "link_indices": [116, 117], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1007	{"contract_id": "9.3", "closure": "linked", "link_indices": [118], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1008	{"contract_id": "10", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
  1009	{"contract_id": "10.1", "closure": "linked", "link_indices": [126, 127], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1010	{"contract_id": "10.2", "closure": "linked", "link_indices": [128], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1011	{"contract_id": "11", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
  1012	{"contract_id": "11.1", "closure": "linked", "link_indices": [129, 140, 141], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1013	{"contract_id": "11.2", "closure": "linked", "link_indices": [136, 137], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1014	{"contract_id": "11.3", "closure": "linked", "link_indices": [130], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1015	{"contract_id": "11.4", "closure": "linked", "link_indices": [130], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1016	{"contract_id": "11.5", "closure": "linked", "link_indices": [130], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1017	{"contract_id": "11.6", "closure": "linked", "link_indices": [131], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1018	{"contract_id": "11.7", "closure": "linked", "link_indices": [138], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1019	{"contract_id": "11.8", "closure": "linked", "link_indices": [139], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1020	{"contract_id": "12", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
  1021	{"contract_id": "12.1", "closure": "linked", "link_indices": [132], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1022	{"contract_id": "12.2", "closure": "linked", "link_indices": [133], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1023	{"contract_id": "12.3", "closure": "linked", "link_indices": [134], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1024	{"contract_id": "12.4", "closure": "linked", "link_indices": [12, 135], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1025	{"contract_id": "12.5", "closure": "linked", "link_indices": [144], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1026	{"contract_id": "13", "closure": "not_material", "link_indices": [], "reason": "Р—Р°РіРѕР»РѕРІРѕРє, РѕРїСЂРµРґРµР»РµРЅРёРµ Р±РµР· РїСЂР°РІРѕРІРѕРіРѕ СЌС„С„РµРєС‚Р° РёР»Рё РЅРµРѕРїРµСЂР°С‚РёРІРЅР°СЏ СЃС‚СЂРѕРєР°"}
  1027	{"contract_id": "354340", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1028	{"contract_id": "1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1029	{"contract_id": "2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1030	{"contract_id": "3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1031	{"contract_id": "4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1032	{"contract_id": "5", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1033	{"contract_id": "9.2.1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1034	{"contract_id": "1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1035	{"contract_id": "2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1036	{"contract_id": "3", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1037	{"contract_id": "1.1", "closure": "linked", "link_indices": [9], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1038	{"contract_id": "1.2", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1039	{"contract_id": "1.3", "closure": "linked", "link_indices": [13], "reason": "РЎРІСЏР·Р°РЅРѕ СЃ РјР°С‚СЂРёС†РµР№"}
  1040	{"contract_id": "4", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1041	{"contract_id": "10", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1042	{"contract_id": "1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1043	{"contract_id": "1", "closure": "extra_in_contract", "link_indices": [], "reason": "РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ СѓСЃР»РѕРІРёРµ РєРѕРЅС‚СЂР°РєС‚Р° Р±РµР· Р°РЅР°Р»РѕРіР° РІ РјР°С‚СЂРёС†Рµ"}
  1044	
  1045	=== SUMMARY ===
  1046	{
  1047	  "aligned_count": 135,
  1048	  "deviation_count": 10,
  1049	  "missing_in_contract_count": 0,
  1050	  "extra_in_contract_count": 72
  1051	}
  1052	
  1053	[Command succeeded with exit code 0]

