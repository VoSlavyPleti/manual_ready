## Summarized at 2026-06-25T16:51:20.108342+00:00

Human: Contract-extra review for material terms
AI: I'll start by reading the skill file to understand the full workflow, then explore the project structure.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_a37yZdRd7qevMU07JEwx7706', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/'}, 'id': 'call_01_GnYzFISTJxMTPa8YQNKq5662', 'type': 'tool_call'}]
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
    26	
    27	The review is risk-oriented. Missing a real risk is worse than marking a
    28	borderline issue as `deviation`, but weak thematic matches must not be promoted
    29	into legal links.
    30	
    31	## Inputs And Outputs
    32	
    33	Inputs:
    34	
    35	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    36	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    37	  applicability filters.
    38	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    39	  ids or real document locators visible in this file.
    40	
    41	Final outputs:
    42	
    43	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    44	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    45	
    46	Working artifacts belong under `/outputs/working/`.
    47	
    48	## Source Hierarchy
    49	
    50	Use the source text as the legal authority:
    51	
    52	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    53	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    54	3. Working ledgers as indexes and evidence aids.
    55	
    56	Do not decide status from extracted fields alone. When a status depends on a
    57	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    58	consequence, re-read the source text.
    59	
    60	## Required Artifacts And Contracts
    61	
    62	Create the artifacts in this order. Each later step depends on the earlier
    63	artifact contract.
    64	
    65	### 1. Source Preflight
    66	
    67	Check `inputs/contract.txt` before analysis:
    68	
    69	- real clause numbering is present;
    70	- deep clause numbers are not visibly collapsed or shifted;
    71	- repeated locators have enough context to distinguish source rows;
    72	- text is readable and not corrupted by encoding.
    73	
    74	If the contract text is not usable, stop and write
    75	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
    76	invalid text.
    77	
    78	### 2. Clause Index
    79	
    80	Create `/outputs/working/clause_index.json`.
    81	
    82	It is a source map only. It must include:
    83	
    84	- every matrix `number`;
    85	- every contract clause, operative parent, definition, appendix/table row, and
    86	  unnumbered operative provision;
    87	- source text or source locator for each row;
    88	- context for duplicate printed contract ids.
    89	
    90	Do not use `clause_index` to decide legal status. It only proves source
    91	coverage and valid ids. Never overwrite it with a batch subset.
    92	
    93	### 3. Legal Proposition Ledger
    94	
    95	Create `/outputs/working/legal_propositions.json`.
    96	
    97	This is the mandatory legal evidence ledger. It must contain `matrix` and
    98	`contract` arrays. Every evaluable proposition should include:
    99	
   100	- `id`: matrix number or printed contract locator;
   101	- `source_text`: text used for legal comparison;
   102	- `source_excerpt`: short quote supporting the normalized proposition;
   103	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   104	  `appendix`, `table`, or `technical`;
   105	- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
   106	- `protected_party`, `bound_party`;
   107	- `right_or_obligation`;
   108	- `legal_object`;
   109	- `trigger`;
   110	- `deadline`;
   111	- `amount_formula_cap`;
   112	- `procedure_channel`;
   113	- `liability_remedy`;
   114	- `scope_options`;
   115	- `consequence`;
   116	- `applicability_filters` where available.
   117	
   118	If a legally meaningful row cannot be normalized, mark it
   119	`needs_source_review` and explain the missing element. It is not fully
   120	processed until the source text has been reviewed. Do not proceed to final
   121	matching with unresolved source-review rows that could affect status.
   122	
   123	The ledger is an evidence table, not a substitute for the source. Matching may
   124	use it to find candidates. Status must still be confirmed against source text.
   125	
   126	Run the mechanical check before matching:
   127	
   128	```bash
   129	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working
   130	```
   131	
   132	Fix invalid working artifacts before delegating comparison work.
   133	
   134	### 4. Contract Product Profile
   135	
   136	Create `/outputs/working/contract_product_profile.json`.
   137	
   138	Extract from the contract:
   139	
   140	- product and payment channels;
   141	- lot/procurement type;
   142	- terminal/payment-device scope;
   143	- payment methods;
   144	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   145	
   146	Apply matrix filters before status:
   147	
   148	- `common` applies to every contract.
   149	- A filtered matrix item applies only when the profile matches
   150	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   151	- Mandatory applicable missing = high risk.
   152	- Optional or non-applicable missing = low or conditional risk.
   153	- Slash-separated alternatives are options unless the matrix says all options
   154	  are mandatory.
   155	- Placeholder or blank in an applicable material term = low-risk `deviation`.
   156	
   157	## Analogue Threshold
   158	
   159	Create a final link only when the contract proposition is a true legal analogue
   160	of the matrix proposition. Test:
   161	
   162	- same or equivalent protected party;
   163	- same or equivalent bound party;
   164	- same legal object;
   165	- same operative right, duty, prohibition, permission, remedy, or allocation of
   166	  risk;
   167	- material trigger, scope, procedure, and consequence are the same or legally
   168	  equivalent.
   169	
   170	Reject weak thematic candidates. A clause about the same broad topic is not a
   171	legal analogue when it governs a different object, party, trigger, procedure,
   172	or consequence.
   173	
   174	## Bidirectional Matching
   175	
   176	Perform both directions.
   177	
   178	Matrix to contract:
   179	
   180	- for each applicable evaluable matrix proposition, retrieve all contract
   181	  clauses that collectively cover the Bank-standard requirement;
   182	- include parent, child, appendix, payment, procedure, liability, and framework
   183	  clauses only when they provide material coverage or legally cure a gap.
   184	
   185	Contract to matrix:
   186	
   187	- for each evaluable contract proposition, find the matrix analogue group;
   188	- if none exists and the term has independent legal effect, classify it as
   189	  `extra_in_contract`;
   190	- if it is non-operative, close it as `not_material` only in the ledger.
   191	
   192	Group related ids into many-to-many `links`. One matrix id may need several
   193	contract clauses. One contract clause may cover several matrix ids.
   194	
   195	## Group-Level Status
   196	
   197	Assign status to the group, not to each atomic pair.
   198	
   199	- `aligned`: the contract package preserves the matrix legal result.
   200	- `deviation`: a true analogue exists, but any material element is changed,
   201	  narrowed, weakened, omitted, shifted, or blank.
   202	- `missing_in_contract`: no true contract analogue exists for an applicable
   203	  matrix requirement.
   204	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   205	  analogue.
   206	- `not_material`: internal ledger closure only; exclude from final report.
   207	
   208	Material elements include party, legal object, operative act, trigger,
   209	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   210	remedy, exception, Bank right, merchant duty, and consequence.
   211	
   212	Hard terms must be compared directly:
   213	
   214	- same material deadline/amount/procedure in the same legal obligation can be
   215	  `aligned`;
   216	- changed value or missing value is `deviation`;
   217	- a hard term from another clause counts only when that clause expressly
   218	  governs the same obligation or is explicitly incorporated;
   219	- a neighboring date, amount, or procedure for another legal object cannot cure
   220	  the gap.
   221	
   222	Do not downgrade for formal differences alone: heading, title, appendix label,
   223	permitted option selection, equivalent mandatory-law mechanism, or wording
   224	style.
   225	
   226	## Risk Calibration
   227	
   228	Use `risk_level` consistently:
   229	
   230	- `none`: only for `aligned`;
   231	- `low`: optional/non-applicable missing, placeholder, formal but legally
   232	  manageable gap;
   233	- `medium`: material deviation that can affect performance, evidence, payment,
   234	  control, liability, or enforceability;
   235	- `high`: mandatory missing, changed protected party, major payment/remedy
   236	  change, important Bank right omitted, or broad contract-only risk.
   237	
   238	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   239	a short evidence-based reason. Use concise quotes rather than long excerpts.
   240	
   241	## Final QA
   242	
   243	Before writing final artifacts:
   244	
   245	- verify `clause_index` covers all source ids;
   246	- verify `legal_proposition_ledger` has no unresolved
   247	  `needs_source_review` rows that can affect final status;
   248	- verify every evaluable matrix id is closed as linked or missing;
   249	- verify every material contract id is closed as linked or extra;
   250	- verify `coverage_ledger` is derived from final `links`,
   251	  `unmatched_matrix`, and `unmatched_contract`;
   252	- verify every final id is visible in source text;
   253	- verify `aligned` has no material discrepancy;
   254	- verify every `deviation` has a named legal gap and evidence;
   255	- verify weak candidates are not in final `links`;
   256	- verify non-material contract rows are absent from final `unmatched_contract`;
   257	- verify summary counts equal final arrays.
   258	
   259	## Output Discipline
   260	
   261	Follow `references/output-contract.md`.
   262	
   263	The final JSON must contain:
   264	
   265	- `analysis_profile`
   266	- `links`
   267	- `atomic_links`
   268	- `unmatched_matrix`
   269	- `unmatched_contract`
   270	- `coverage_ledger`
   271	- `summary`
   272	
   273	`links` carry group-level legal findings. `atomic_links` are traceability
   274	projections only and must inherit the group relationship. Do not assign
   275	separate final pair-level statuses.
   276	
   277	## Tools And Scripts
   278	
   279	Use helper scripts for mechanical work: source extraction, indexing,
   280	normalization checks, batch completeness, coverage validation, JSON schema
   281	checks, and Excel export. Do not put legal mapping or status decisions into
   282	hardcoded scripts.
Tool: ['/.agents/', '/.codex/', '/.env', '/.git/', '/.gitignore', '/.venv/', '/ALL_DATA/', '/README.md', '/__pycache__/', '/conversation_history/', '/inputs/', '/llm.py', '/main.py', '/output/', '/outputs/', '/results/', '/run_logs/', '/runs/', '/skills/', '/tools/']
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_00_khxtYrAbZPz8whovLC1K1177', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_01_mZtdGaqu9apXa2l1UtL45931', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/inputs'}, 'id': 'call_02_3P0tHlkOClvTOfiYX03J1264', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs'}, 'id': 'call_03_ehgARr6lF3AZPld3aMWJ2641', 'type': 'tool_call'}]
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
    70	Rows marked `needs_source_review` are not complete. Resolve them before final
    71	status if they can affect a link, missing item, or contract-only finding.
    72	
    73	## Final JSON Shape
    74	
    75	```json
    76	{
    77	  "analysis_profile": {
    78	    "contract_product_profile": {
    79	      "product": ["<selected product/channel>"],
    80	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
    81	      "terminal": ["<selected terminal/payment device>"],
    82	      "payment_method": ["<selected payment method>"],
    83	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
    84	    },
    85	    "source_preflight": {
    86	      "contract_numbering_valid": true,
    87	      "notes": []
    88	    }
    89	  },
    90	  "links": [
    91	    {
    92	      "matrix_ids": ["<matrix id>"],
    93	      "contract_ids": ["<contract locator>"],
    94	      "relationship": "aligned|deviation",
    95	      "legal_topic": "<short legal topic>",
    96	      "matrix_standard": "<bank standard requirement group>",
    97	      "contract_position": "<counterparty contract position group>",
    98	      "matrix_evidence": "<short matrix quote>",
    99	      "contract_evidence": "<short contract quote>",
   100	      "status_reason": "<group-level reason>",
   101	      "risk_level": "none|low|medium|high",
   102	      "discrepancies": [
   103	        {
   104	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   105	          "description": "<material difference>",
   106	          "risk": "<why this matters for the Bank>"
   107	        }
   108	      ]
   109	    }
   110	  ],
   111	  "atomic_links": [
   112	    {
   113	      "matrix_id": "<one matrix id>",
   114	      "contract_id": "<one contract locator>",
   115	      "relationship": "aligned|deviation",
   116	      "link_index": 0,
   117	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   118	      "coverage": "<what this contract locator contributes to the group>"
   119	    }
   120	  ],
   121	  "unmatched_matrix": [
   122	    {
   123	      "matrix_id": "<matrix id>",
   124	      "requirement": "<missing bank standard requirement>",
   125	      "source_evidence": "<short matrix quote>",
   126	      "status": "missing_in_contract",
   127	      "required_type": "mandatory|optional|unknown",
   128	      "applicability": "applicable|not_applicable|conditional|unknown",
   129	      "risk_level": "low|medium|high",
   130	      "risk": "<risk of omission>",
   131	      "rejected_candidates": [
   132	        {
   133	          "contract_id": "<weak candidate considered>",
   134	          "reason": "<why it is not a true analogue>"
   135	        }
   136	      ]
   137	    }
   138	  ],
   139	  "unmatched_contract": [
   140	    {
   141	      "contract_id": "<contract locator>",
   142	      "contract_position": "<extra legally significant contract term>",
   143	      "source_evidence": "<short contract quote>",
   144	      "status": "extra_in_contract",
   145	      "risk_level": "low|medium|high",
   146	      "risk": "<risk or impact for the Bank>",
   147	      "materiality_reason": "<why this has independent legal effect>"
   148	    }
   149	  ],
   150	  "coverage_ledger": {
   151	    "matrix": [
   152	      {
   153	        "matrix_id": "<matrix id>",
   154	        "closure": "linked|missing_in_contract|not_evaluable",
   155	        "link_indices": [0],
   156	        "reason": "<short closure reason>"
   157	      }
   158	    ],
   159	    "contract": [
   160	      {
   161	        "contract_id": "<contract locator>",
   162	        "closure": "linked|extra_in_contract|not_material",
   163	        "link_indices": [0],
   164	        "reason": "<short closure reason>"
   165	      }
   166	    ]
   167	  },
   168	  "summary": {
   169	    "aligned_count": 0,
   170	    "deviation_count": 0,
   171	    "missing_in_contract_count": 0,
   172	    "extra_in_contract_count": 0
   173	  }
   174	}
   175	```
   176	
   177	## JSON Rules
   178	
   179	- `links` are group-level legal findings. One status applies to the whole
   180	  many-to-many group.
   181	- `atomic_links` are traceability rows only. They inherit the group
   182	  `relationship`; do not invent pair-level final statuses.
   183	- `contract_ids` contain clauses that provide material coverage for the group.
   184	  Background clauses can be cited in reasoning, but should not become final
   185	  candidates unless they affect coverage or status.
   186	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   187	  `unmatched_contract`. Do not use it to invent final conclusions.
   188	- `unmatched_contract` contains only legally significant `extra_in_contract`
   189	  rows. Non-material rows stay in `coverage_ledger.contract`.
   190	- `relationship = aligned` requires empty `discrepancies`, `risk_level = none`,
   191	  and text-grounded confirmation that the contract package preserves the matrix
   192	  legal result.
   193	- `relationship = deviation` requires at least one discrepancy with `type`,
   194	  `description`, and `risk`.
   195	- Missing mandatory applicable requirements should normally be `high` risk.
   196	  Missing optional or non-applicable requirements should normally be `low` or
   197	  conditional risk.
   198	- All final ids must be visible in source files. Do not use corrected,
   199	  inferred, translated, parenthetical, or internal ids.
   200	- Weak candidates do not appear in final `links`; use
   201	  `unmatched_matrix[].rejected_candidates`.
   202	
   203	## Excel Output
   204	
   205	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   206	
   207	Sheet 1: `Contract-Matrix`
   208	
   209	Columns:
   210	
   211	1. `contract_id`
   212	2. `contract_summary`
   213	3. `matrix_ids`
   214	4. `status`
   215	5. `risk_level`
   216	6. `comment`
   217	
   218	Rules:
   219	
   220	- one row per group-level contract-to-matrix finding;
   221	- `matrix_ids` contains the full matrix id set for the group;
   222	- status is `aligned`, `deviation`, or `extra_in_contract`;
   223	- contract-only extras have blank `matrix_ids`.
   224	
   225	Sheet 2: `Only in Matrix`
   226	
   227	Columns:
   228	
   229	1. `matrix_id`
   230	2. `requirement`
   231	3. `required_type`
   232	4. `risk_level`
   233	5. `comment`
   234	
   235	Rules:
   236	
   237	- one row per final `unmatched_matrix` item;
   238	- include optional and non-applicable missing as low/conditional risk;
   239	- do not include non-evaluable headings or purely technical rows.
   240	
   241	## Bad Output Patterns
   242	
   243	Do not output:
   244	
   245	- multiple competing final JSON files;
   246	- pair-level final statuses as the primary answer;
   247	- `deviation` for unselected slash alternatives;
   248	- `deviation` for heading/title/label changes alone;
   249	- final `unmatched_contract` rows for definitions without legal effect;
   250	- final ids that exist only in helper scripts or working ledgers;
   251	- `extra_in_contract` with empty risk;
   252	- `aligned` with non-empty discrepancies;
   253	- `missing_in_contract` where a weak candidate is silently treated as a link;
   254	- final conclusions based only on extracted fields without source-text evidence.
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
    72	## 8. Optional Or Non-Applicable Missing
    73	
    74	Matrix item is optional or filtered to a product, lot, terminal, or payment
    75	method not used by the contract. No true analogue exists.
    76	
    77	Result: `missing_in_contract` with low or conditional risk. Do not force a weak
    78	link.
    79	
    80	## 9. Slash Options
    81	
    82	Matrix lists `cards / QR / mobile pay / smart terminal` as alternatives.
    83	Contract selects `cards / QR`, and the profile confirms only those services are
    84	in scope.
    85	
    86	Result: `aligned` for scope. Absence of unselected alternatives is not a
    87	deviation.
    88	
    89	## 10. Placeholder In Applicable Term
    90	
    91	Matrix or contract requires a filled penalty, fee, account, deadline, appendix,
    92	or system name. The applicable field is blank.
    93	
    94	Result: `deviation`, usually low risk unless the blank blocks enforcement.
    95	
    96	## 11. Same Deadline
    97	
    98	Matrix requires a document within 3 business days. Contract imposes the same
    99	3-business-day deadline on the same duty.
   100	
   101	Result: deadline element is covered.
   102	
   103	## 12. Changed Or Missing Deadline
   104	
   105	Matrix requires 3 business days. Contract says 5 business days, uses another
   106	period, or states the duty without a deadline.
   107	
   108	Result: `deviation`; discrepancy type `deadline`.
   109	
   110	## 13. Borrowed Hard Term Does Not Cure Gap
   111	
   112	Contract clause A covers the same duty but lacks the matrix deadline. Clause B
   113	has the same number of days but governs a different request or procedure and is
   114	not incorporated into clause A.
   115	
   116	Result: clause B cannot make clause A aligned. Record a deadline deviation.
   117	
   118	## 14. Changed Amount, Formula, Cap, Or Penalty
   119	
   120	Matrix requires a fixed penalty, no cap, full damages, or a specific formula.
   121	Contract lowers the amount, adds a cap, changes the base, or requires an extra
   122	demand.
   123	
   124	Result: `deviation`; discrepancy type `amount` or `liability`.
   125	
   126	## 15. Party Inversion
   127	
   128	Matrix protects the Bank or imposes a duty on the counterparty. Contract gives
   129	the analogous right to the customer or shifts the burden to the Bank.
   130	
   131	Result: `deviation` if it is an analogue; `extra_in_contract` if it creates a
   132	new independent right.
   133	
   134	## 16. Procurement Mechanism As Analogue
   135	
   136	Public-contract acceptance, EIS signing, budget payment, statutory penalties,
   137	or unilateral termination regulates the same legal object as the matrix.
   138	
   139	Result: link it. Use `aligned` if the Bank standard is preserved or stronger;
   140	use `deviation` if timing, payment path, acceptance, remedy, or control changes.
   141	
   142	## 17. Procurement Mechanism As Extra
   143	
   144	Contract gives the customer an independent inspection, rejection, correction,
   145	withholding, reporting, or convenience termination right with no matrix
   146	analogue.
   147	
   148	Result: `extra_in_contract` with materiality reason and risk.
   149	
   150	## 18. Formal Label Difference
   151	
   152	The same legal content appears under another appendix title, report label, or
   153	document name.
   154	
   155	Result: `aligned` if rights, duties, timing, evidence, and consequences are
   156	preserved.
   157	
   158	## 19. Named Channel Or Legal Force Missing
   159	
   160	Matrix requires a named EDI/email/site/channel or legal-force effect. Contract
   161	has a generic document exchange clause and omits the named element.
   162	
   163	Result: `deviation` when it is the same exchange mechanism with a missing
   164	material element. If it is only broad-topic context, use `missing_in_contract`.
   165	
   166	## 20. Generic Product Capability
   167	
   168	Contract says a terminal can display QR or accept cards. Matrix requires a
   169	named Bank product or product-specific procedure.
   170	
   171	Result: apply the product profile first. Generic capability is not enough for a
   172	named product obligation.
   173	
   174	## 21. Definition Without Legal Effect
   175	
   176	Definition has no analogue in the matrix and creates no standalone right, duty,
   177	risk, amount, procedure, liability, or consequence.
   178	
   179	Result: `not_material` in the working ledger only.
   180	
   181	## 22. Definition With Legal Effect
   182	
   183	Definition expands a key term so that it changes scope, liability, covered
   184	transactions, parties, or remedies.
   185	
   186	Result: evaluable. Link it if it modifies a matrix analogue; otherwise classify
   187	as `extra_in_contract`.
   188	
   189	## 23. Contract-Only Material Clause
   190	
   191	Contract adds maximum price, budget source, customer control, acceptance,
   192	withholding, unilateral refusal, penalty cap, reporting, anti-corruption,
   193	confidentiality, audit, data, or evidence procedure with no matrix analogue.
   194	
   195	Result: `extra_in_contract`.
   196	
   197	## 24. Duplicate Gap Propagation
   198	
   199	One payment deadline gap affects a payment package with parent and child
   200	clauses.
   201	
   202	Result: record one grouped `deviation`. Do not duplicate the same gap across
   203	unrelated companion clauses.
   204	
   205	## 25. Non-Informative Parent
   206	
   207	A parent row merely names a section and all legal effect is in children.
   208	
   209	Result: close as non-evaluable or `not_material` in the ledger. Do not report
   210	it as a final risk.
   211	
   212	## 26. Group-Level Status
   213	
   214	A group contains several matrix ids and several contract ids. One status
   215	applies to the group as a whole.
   216	
   217	Result: do not assign separate final statuses per pair. `atomic_links` are only
   218	traceability rows and inherit the group relationship.
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/outputs/working/']
AI: Good, I have the skill instructions, output contract, and comparison patterns. Now let me read the input files and check what's already in the working directory.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_pUv5E89BPySW9dOSAS023229', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_Fup6z1Wn1ZENTmVu5ipC9450', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_02_Wvj2pBLHf38a4rQWHWsc6379', 'type': 'tool_call'}]
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
Tool: ['/outputs/working/batch4_analysis.py', '/outputs/working/batch4_list.py', '/outputs/working/batch4_list2.py', '/outputs/working/batch4_matrix_dump.txt', '/outputs/working/batch_1_output.json', '/outputs/working/batch_2_output.json', '/outputs/working/batch_3_output.json', '/outputs/working/batch_4_output.json', '/outputs/working/build_batch2.py', '/outputs/working/check_extra.py', '/outputs/working/check_unmatched.py', '/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/enrich_propositions.py', '/outputs/working/extract_batch4.py', '/outputs/working/final_validate.py', '/outputs/working/fix_missing.py', '/outputs/working/fix_overlap.py', '/outputs/working/fix_req_types.py', '/outputs/working/generate_atomic.py', '/outputs/working/legal_propositions.json', '/outputs/working/validate_batch1.py', '/outputs/working/validate_batch2.py', '/outputs/working/validate_batch3.py']
AI: I can see there are already working artifacts. Let me read the existing working files to understand the current state of analysis, particularly the legal propositions, clause index, and contract product profile.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json', 'limit': 100}, 'id': 'call_00_J2po50ag0ys0SpxhWe2G3485', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 200}, 'id': 'call_01_JUUlhgab4Uu0sBJVw9E35832', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 200}, 'id': 'call_02_3zLZWb6LYyCiuUZSk94e1482', 'type': 'tool_call'}]
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos"],
     5	  "payment_method": ["cards", "qr", "nfc"],
     6	  "legal_regime": "44_fz",
     7	  "notes": {
     8	    "contract_type": "44-FZ procurement contract for acquiring services",
     9	    "customer": "Federal State Budgetary Institution (ФГБУ)",
    10	    "terminals": "POS-terminals (Электронные терминалы) provided by the Bank, installed at 8+ locations",
    11	    "payment_systems": "МИР, VISA, MasterCard",
    12	    "qr_support": "Terminals must have QR-code display capability for cashless payment",
    13	    "nfc_support": "Terminals must support contactless payment",
    14	    "sberpay_reference": "Contract mentions SberPay in definitions but not as a separately activated product",
    15	    "internet_acquiring": "Not in scope - this is trade acquiring only",
    16	    "smart_terminals": "Not explicitly distinguished from POS terminals in this contract"
    17	  }
    18	}
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
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
     7	      "type": "operative",
     8	      "materiality": "evaluable",
     9	      "protected_party": "Bank",
    10	      "bound_party": "Merchant",
    11	      "right_or_obligation": "Bank right",
    12	      "legal_object": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    13	      "trigger": "",
    14	      "deadline": "",
    15	      "amount_formula_cap": "",
    16	      "procedure_channel": "",
    17	      "liability_remedy": "",
    18	      "scope_options": [
    19	        "common",
    20	        "common",
    21	        "common",
    22	        "common"
    23	      ],
    24	      "consequence": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
    25	      "applicability_filters": {
    26	        "required_type": "mandatory",
    27	        "only_for_product": "common",
    28	        "only_for_lot": "common",
    29	        "only_for_terminal": "common",
    30	        "payment_method": "common"
    31	      },
    32	      "main_idea": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
    33	      "topics": [
    34	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    35	        "Банк может отказать в регистрации ТСТ без указания причины",
    36	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    37	        "Информация о новых устройствах предоставляется с указанием их количества"
    38	      ],
    39	      "enriched_text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора.\nПри изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров."
    40	    },
    41	    {
    42	      "id": "2.2",
    43	      "source_text": "Важен факт, что валюта рубль РФ, другая валюта недопустима Расчёты производятся в рублях Российской Федерации Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    44	      "source_excerpt": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    45	      "type": "operative",
    46	      "materiality": "evaluable",
    47	      "protected_party": "Both",
    48	      "bound_party": "Both",
    49	      "right_or_obligation": "Mutual obligation",
    50	      "legal_object": "Расчёты производятся в рублях Российской Федерации",
    51	      "trigger": "",
    52	      "deadline": "",
    53	      "amount_formula_cap": "",
    54	      "procedure_channel": "",
    55	      "liability_remedy": "",
    56	      "scope_options": [
    57	        "common",
    58	        "common",
    59	        "common",
    60	        "common"
    61	      ],
    62	      "consequence": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    63	      "applicability_filters": {
    64	        "required_type": "mandatory",
    65	        "only_for_product": "common",
    66	        "only_for_lot": "common",
    67	        "only_for_terminal": "common",
    68	        "payment_method": "common"
    69	      },
    70	      "main_idea": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    71	      "topics": [
    72	        "Расчёты производятся в рублях Российской Федерации"
    73	      ],
    74	      "enriched_text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. "
    75	    },
    76	    {
    77	      "id": "2.3.1",
    78	      "source_text": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса. Обмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту; Информация и документы, направленные по электронной почте, имеют юридическую силу Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    79	      "source_excerpt": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    80	      "type": "operative",
    81	      "materiality": "evaluable",
    82	      "protected_party": "Both",
    83	      "bound_party": "Both",
    84	      "right_or_obligation": "Mutual obligation",
    85	      "legal_object": "Обмен информацией по электронной почте",
    86	      "trigger": "",
    87	      "deadline": "",
    88	      "amount_formula_cap": "",
    89	      "procedure_channel": "",
    90	      "liability_remedy": "",
    91	      "scope_options": [
    92	        "common",
    93	        "common",
    94	        "common",
    95	        "common"
    96	      ],
    97	      "consequence": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    98	      "applicability_filters": {
    99	        "required_type": "mandatory",
   100	        "only_for_product": "common",
   101	        "only_for_lot": "common",
   102	        "only_for_terminal": "common",
   103	        "payment_method": "common"
   104	      },
   105	      "main_idea": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
   106	      "topics": [
   107	        "Обмен информацией по электронной почте",
   108	        "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
   109	        "Информация и документы, направленные по электронной почте, имеют юридическую силу"
   110	      ],
   111	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;"
   112	    },
   113	    {
   114	      "id": "2.3.2",
   115	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами посредством системы ДБО или аналогичных систем Банка Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
   116	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом",
   117	      "type": "operative",
   118	      "materiality": "evaluable",
   119	      "protected_party": "Both",
   120	      "bound_party": "Both",
   121	      "right_or_obligation": "Mutual obligation",
   122	      "legal_object": "Обмен документами посредством системы ДБО или аналогичных систем Банка",
   123	      "trigger": "",
   124	      "deadline": "",
   125	      "amount_formula_cap": "",
   126	      "procedure_channel": "",
   127	      "liability_remedy": "",
   128	      "scope_options": [
   129	        "common",
   130	        "common",
   131	        "common",
   132	        "common"
   133	      ],
   134	      "consequence": "Важен сам факт возможности отправки информации / документов таким способом",
   135	      "applicability_filters": {
   136	        "required_type": "mandatory",
   137	        "only_for_product": "common",
   138	        "only_for_lot": "common",
   139	        "only_for_terminal": "common",
   140	        "payment_method": "common"
   141	      },
   142	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   143	      "topics": [
   144	        "Обмен документами посредством системы ДБО или аналогичных систем Банка"
   145	      ],
   146	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;"
   147	    },
   148	    {
   149	      "id": "2.3.3",
   150	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   151	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом",
   152	      "type": "operative",
   153	      "materiality": "evaluable",
   154	      "protected_party": "Both",
   155	      "bound_party": "Both",
   156	      "right_or_obligation": "Mutual obligation",
   157	      "legal_object": "Обмен документами с доставкой нарочным или курьером",
   158	      "trigger": "",
   159	      "deadline": "",
   160	      "amount_formula_cap": "",
   161	      "procedure_channel": "",
   162	      "liability_remedy": "",
   163	      "scope_options": [
   164	        "common",
   165	        "common",
   166	        "common",
   167	        "common"
   168	      ],
   169	      "consequence": "Важен сам факт возможности отправки информации / документов таким способом",
   170	      "applicability_filters": {
   171	        "required_type": "optional",
   172	        "only_for_product": "common",
   173	        "only_for_lot": "common",
   174	        "only_for_terminal": "common",
   175	        "payment_method": "common"
   176	      },
   177	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   178	      "topics": [
   179	        "Обмен документами с доставкой нарочным или курьером"
   180	      ],
   181	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
   182	    },
   183	    {
   184	      "id": "2.3.4",
   185	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами через заказное письмо Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   186	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом",
   187	      "type": "operative",
   188	      "materiality": "evaluable",
   189	      "protected_party": "Both",
   190	      "bound_party": "Both",
   191	      "right_or_obligation": "Mutual obligation",
   192	      "legal_object": "Обмен документами через заказное письмо",
   193	      "trigger": "",
   194	      "deadline": "",
   195	      "amount_formula_cap": "",
   196	      "procedure_channel": "",
   197	      "liability_remedy": "",
   198	      "scope_options": [
   199	        "common",
   200	        "common",
AI: Let me now read the rest of the contract text and the existing batch outputs to understand what's already been analyzed and what contract-only terms have been identified.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 300}, 'id': 'call_00_11oPv6b6IQS2QAi4WIRJ1898', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_1_output.json', 'limit': 200}, 'id': 'call_01_tCQp8FDdcp0UmUVOMwhD1818', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_2_output.json', 'limit': 200}, 'id': 'call_02_WvZ0cSPDbjMxtL6a0xSt9578', 'type': 'tool_call'}]
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
   401	¨ Интернет сайт                    http://__________
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
Tool:      1	{
     2	  "batch": "1",
     3	  "matrix_ids": ["2.1", "2.2", "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "2.4", "2.5.1.1", "2.5.2.1", "2.6.1.1", "2.6.2.1", "2.6.2.2", "2.6.3.1", "2.6.3.2", "2.7"],
     4	  "links": [
     5	    {
     6	      "matrix_ids": ["2.1"],
     7	      "contract_ids": ["4.3"],
     8	      "relationship": "deviation",
     9	      "legal_topic": "Регистрация ТСТ и отказ Банка",
    10	      "matrix_standard": "Для регистрации новой ТСТ Предприятие предоставляет Заявление и Информацию о ТСТ по формам Приложений 1 и 1.1; Банк вправе отказать в регистрации ТСТ без объяснения причин с уведомлением по п.2.3; при изменении информации о ТСТ Предприятие предоставляет обновлённую Информацию о ТСТ; при подключении дополнительных устройств — информация с указанием количества.",
    11	      "contract_position": "Пункт 4.3 (абз. 2): Заказчик после заключения контракта предоставляет Исполнителю заявление Заказчика на проведение расчетов и информацию о ТСТ/изменение информации о ТСТ, подписанную уполномоченным представителем. Отсутствует право Банка на отказ в регистрации ТСТ без объяснения причин. Отсутствует требование об указании количества подключаемых устройств. Отсутствует отсылка к процедуре уведомления об отказе.",
    12	      "matrix_evidence": "«Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора.» (матрица 2.1)",
    13	      "contract_evidence": "«В целях регистрации нового ТСТ в рамках настоящего контракта Заказчик после заключения контракта предоставляет Исполнителю заявление Заказчика на проведение расчетов по операциям с использованием банковских карт и информацию о ТСТ Заказчика/изменение информации о ТСТ заказчика, подписанную уполномоченным представителем заказчика.» (п. 4.3 Контракта)",
    14	      "status_reason": "Контракт содержит обязанность Заказчика предоставить заявление и информацию о ТСТ (частичный аналог), но не содержит ключевого права Банка отказать в регистрации ТСТ без объяснения причин. Также отсутствуют: требование об указании количества подключаемых устройств, отсылка к конкретным формам Приложений 1 и 1.1 (в контракте используются Приложения 1.1 и 1.2 с иной нумерацией), процедура уведомления об отказе по п.2.3.",
    15	      "risk_level": "high",
    16	      "discrepancies": [
    17	        {
    18	          "type": "right",
    19	          "description": "Отсутствует право Банка отказать в регистрации ТСТ без объяснения причин — ключевой элемент матричного стандарта, защищающий Банк.",
    20	          "risk": "Банк лишается одностороннего контрольного механизма при регистрации новых ТСТ. Любая ТСТ, по которой Заказчик подал заявление, может считаться зарегистрированной, что создаёт операционный и комплаенс-риск."
    21	        },
    22	        {
    23	          "type": "missing_element",
    24	          "description": "Отсутствует требование об указании количества вновь подключаемых устройств (терминалов/сканеров) при подаче информации о ТСТ.",
    25	          "risk": "Банк не получает structured data о количестве устройств, что затрудняет управление терминальным парком и сверку."
    26	        },
    27	        {
    28	          "type": "procedure",
    29	          "description": "Отсутствует отсылка к процедуре уведомления об отказе (п. 2.3 матрицы).",
    30	          "risk": "Даже если право отказа будет подразумеваться, отсутствует процедурный механизм его реализации."
    31	        }
    32	      ]
    33	    },
    34	    {
    35	      "matrix_ids": ["2.2"],
    36	      "contract_ids": ["5.1.8", "Приложение_1_п5"],
    37	      "relationship": "aligned",
    38	      "legal_topic": "Валюта расчётов — рубли РФ",
    39	      "matrix_standard": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    40	      "contract_position": "Пункт 5.1.8: Банк перечисляет суммы Операций оплаты в валюте проведения операции (рубли РФ). Приложение №1 (Техническое задание) п. 5: «Расчеты при совершении операций производятся в валюте Российской Федерации.»",
    41	      "matrix_evidence": "«Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.» (матрица 2.2)",
    42	      "contract_evidence": "«перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты в валюте проведения операции (рубли РФ)» (п. 5.1.8); «Расчеты при совершении операций производятся в валюте Российской Федерации» (Приложение №1, п. 5)",
    43	      "status_reason": "Контракт прямо и недвусмысленно устанавливает рубль РФ в качестве валюты расчётов по операциям в двух независимых положениях. Матричный стандарт полностью сохранён.",
    44	      "risk_level": "none",
    45	      "discrepancies": []
    46	    },
    47	    {
    48	      "matrix_ids": ["2.3.1"],
    49	      "contract_ids": ["2.3.1"],
    50	      "relationship": "aligned",
    51	      "legal_topic": "Обмен информацией по электронной почте с юридической силой",
    52	      "matrix_standard": "Обмен по email с адресов, указанных в Заявлении/Информации о ТСТ; исключение персональных данных, коммерческой и банковской тайны; полная юридическая сила email-документов.",
    53	      "contract_position": "Пункт 2.3.1 Контракта: дословное совпадение с матричным стандартом — те же адреса, те же исключения, та же полная юридическая сила.",
    54	      "matrix_evidence": "«...информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств» (матрица 2.3.1)",
    55	      "contract_evidence": "«...информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств» (п. 2.3.1 Контракта)",
    56	      "status_reason": "Текст контракта практически дословно воспроизводит матричный стандарт. Все материальные элементы (канал, адреса, исключения, юридическая сила) совпадают.",
    57	      "risk_level": "none",
    58	      "discrepancies": []
    59	    },
    60	    {
    61	      "matrix_ids": ["2.3.2"],
    62	      "contract_ids": ["2.3.2"],
    63	      "relationship": "aligned",
    64	      "legal_topic": "Обмен через систему ДБО или аналогичные системы Банка",
    65	      "matrix_standard": "Обмен информацией/документами посредством системы ДБО или аналогичных систем Банка.",
    66	      "contract_position": "Пункт 2.3.2 Контракта: «посредством системы ДБО или аналогичных систем Банка» — дословное совпадение.",
    67	      "matrix_evidence": "«посредством системы ДБО или аналогичных систем Банка» (матрица 2.3.2)",
    68	      "contract_evidence": "«посредством системы ДБО или аналогичных систем Банка» (п. 2.3.2 Контракта)",
    69	      "status_reason": "Дословное совпадение. Матричный стандарт полностью сохранён.",
    70	      "risk_level": "none",
    71	      "discrepancies": []
    72	    },
    73	    {
    74	      "matrix_ids": ["2.3.3"],
    75	      "contract_ids": ["2.3.3"],
    76	      "relationship": "aligned",
    77	      "legal_topic": "Обмен документами нарочным/курьерской почтой",
    78	      "matrix_standard": "Обмен письмами с доставкой нарочным или курьерской почтой по адресу из Заявления/Информации о ТСТ (опциональный канал).",
    79	      "contract_position": "Пункт 2.3.3 Контракта: дословное совпадение с матричным стандартом.",
    80	      "matrix_evidence": "«путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении...» (матрица 2.3.3)",
    81	      "contract_evidence": "«путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Заказчика...» (п. 2.3.3 Контракта)",
    82	      "status_reason": "Дословное совпадение. Опциональный канал сохранён.",
    83	      "risk_level": "none",
    84	      "discrepancies": []
    85	    },
    86	    {
    87	      "matrix_ids": ["2.3.4"],
    88	      "contract_ids": ["2.3.4"],
    89	      "relationship": "aligned",
    90	      "legal_topic": "Обмен документами заказным письмом",
    91	      "matrix_standard": "Обмен почтовыми отправлениями (заказным письмом) по адресу из Заявления/Информации о ТСТ (опциональный канал).",
    92	      "contract_position": "Пункт 2.3.4 Контракта: дословное совпадение с матричным стандартом.",
    93	      "matrix_evidence": "«путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении...» (матрица 2.3.4)",
    94	      "contract_evidence": "«путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Заказчика...» (п. 2.3.4 Контракта)",
    95	      "status_reason": "Дословное совпадение. Опциональный канал сохранён.",
    96	      "risk_level": "none",
    97	      "discrepancies": []
    98	    },
    99	    {
   100	      "matrix_ids": ["2.3.5"],
   101	      "contract_ids": ["2.3.5"],
   102	      "relationship": "deviation",
   103	      "legal_topic": "Обмен через E-invoicing/СФЕРА-Курьер с УКЭП",
   104	      "matrix_standard": "Обмен электронными документами посредством автоматизированной системы E-invoicing/«СФЕРА-Курьер»; документы подписываются УКЭП; равнозначны бумажным.",
   105	      "contract_position": "Пункт 2.3.5 Контракта: «путем обмена электронными документами посредством автоматизированной системы _________________.» Наименование системы не заполнено (пустое поле). УКЭП и равнозначность бумажным документам сохранены.",
   106	      "matrix_evidence": "«путем обмена электронными документами посредством автоматизированной системы E-invoicing/«СФЕРА-Курьер»» (матрица 2.3.5)",
   107	      "contract_evidence": "«путем обмена электронными документами посредством автоматизированной системы _________________.» (п. 2.3.5 Контракта)",
   108	      "status_reason": "Контракт содержит канал обмена через автоматизированную систему с УКЭП и равной юридической силой, но наименование системы оставлено незаполненным (placeholder). Это не позволяет идентифицировать конкретную систему, что делает канал юридически неопределённым.",
   109	      "risk_level": "low",
   110	      "discrepancies": [
   111	        {
   112	          "type": "missing_element",
   113	          "description": "Наименование автоматизированной системы ЭДО не заполнено (matrix: «E-invoicing/СФЕРА-Курьер»; contract: «_________________»).",
   114	          "risk": "Низкий риск на стадии заключения — поле может быть заполнено перед подписанием. Однако в текущем виде канал не идентифицирован, что создаёт неопределённость при обмене юридически значимыми документами."
   115	        }
   116	      ]
   117	    },
   118	    {
   119	      "matrix_ids": ["2.3.6"],
   120	      "contract_ids": ["2.3.6"],
   121	      "relationship": "aligned",
   122	      "legal_topic": "Обмен через ЕИС и электронные торговые площадки с УКЭП",
   123	      "matrix_standard": "Обмен электронными документами в ЕИС и на ЭТП в случаях, предусмотренных законодательством о контрактной системе; УКЭП; равнозначность бумажным. (mandatory, only_for_lot=fz_44)",
   124	      "contract_position": "Пункт 2.3.6 Контракта: дословное совпадение с матричным стандартом. Контракт заключён по 44-ФЗ, фильтр применим.",
   125	      "matrix_evidence": "«путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках...» (матрица 2.3.6)",
   126	      "contract_evidence": "«путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках...» (п. 2.3.6 Контракта)",
   127	      "status_reason": "Дословное совпадение. Контракт 44-ФЗ, фильтр only_for_lot=fz_44 применим. Все материальные элементы сохранены.",
   128	      "risk_level": "none",
   129	      "discrepancies": []
   130	    },
   131	    {
   132	      "matrix_ids": ["2.3.7"],
   133	      "contract_ids": ["2.3.7", "2.3_receipt_dates"],
   134	      "relationship": "deviation",
   135	      "legal_topic": "Даты получения информации/документов по каналам обмена",
   136	      "matrix_standard": "Канал через службу поддержки Банка (24/7); даты получения: email/ДБО — дата направления; нарочный/заказное — дата доставки; E-invoicing — дата поступления оператору ЭДО (ООО «КОРУС Консалтинг СНГ») по квитанции; ЕИС — дата направления; служба поддержки — дата обращения.",
   137	      "contract_position": "Пункт 2.3.7 + абзацы о датах получения: все правила определения дат совпадают, кроме наименования оператора ЭДО — в контракте «дочерней компании Банка» (generic) вместо «ООО «КОРУС Консалтинг СНГ» (named).",
   138	      "matrix_evidence": "«в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»)» (матрица 2.3.7)",
   139	      "contract_evidence": "«в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка)» (п. 2.3.5 абз. дат Контракта)",
   140	      "status_reason": "Все правила определения даты получения документов совпадают с матричным стандартом. Единственное отклонение: конкретное наименование оператора ЭДО (ООО «КОРУС Консалтинг СНГ») заменено на родовое «дочерней компании Банка». Это снижает определённость, но не меняет правового механизма.",
   141	      "risk_level": "low",
   142	      "discrepancies": [
   143	        {
   144	          "type": "missing_element",
   145	          "description": "Оператор ЭДО не поименован: матрица указывает «ООО «КОРУС Консалтинг СНГ»», контракт — «дочерней компании Банка» (generic).",
   146	          "risk": "Низкий риск: родовое указание на дочернюю компанию Банка сохраняет функциональность канала, но снижает определённость в случае спора о том, какая именно компания является оператором."
   147	        }
   148	      ]
   149	    },
   150	    {
   151	      "matrix_ids": ["2.4"],
   152	      "contract_ids": ["1.1", "8.3.2"],
   153	      "relationship": "deviation",
   154	      "legal_topic": "Документы по ссылкам — неотъемлемая часть Договора",
   155	      "matrix_standard": "Общая норма: «Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.» (optional)",
   156	      "contract_position": "Пункт 1.1: Приложения №1 и №2 являются неотъемлемой частью контракта. Пункт 8.3.2: прилагаемые к документу о приёмке документы являются неотъемлемой частью. Общая норма о всех документах по ссылкам отсутствует.",
   157	      "matrix_evidence": "«Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.» (матрица 2.4)",
   158	      "contract_evidence": "«в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта» (п. 1.1); «считаются его неотъемлемой частью» (п. 8.3.2)",
   159	      "status_reason": "Контракт содержит точечные указания на неотъемлемость конкретных приложений (№1, №2) и прилагаемых к приёмке документов, но не содержит общей нормы о том, что все документы по ссылкам в контракте являются его неотъемлемой частью. Это снижает правовую интеграцию внешних документов (например, Порядка проведения операций, размещённого на сайте Банка).",
   160	      "risk_level": "low",
   161	      "discrepancies": [
   162	        {
   163	          "type": "scope",
   164	          "description": "Общая норма матрицы заменена точечными указаниями на неотъемлемость конкретных приложений. Отсутствует норма, делающая неотъемлемой частью все документы, на которые даны ссылки в контракте.",
   165	          "risk": "Низкий риск (матрица optional). Однако при возникновении спора о применимости документа, на который контракт ссылается без прямой оговорки о неотъемлемости (например, Порядок проведения операций), позиция Банка может быть слабее."
   166	        }
   167	      ]
   168	    },
   169	    {
   170	      "matrix_ids": ["2.7"],
   171	      "contract_ids": ["12.4"],
   172	      "relationship": "aligned",
   173	      "legal_topic": "Заключение договора в электронной форме с УКЭП",
   174	      "matrix_standard": "Договор может быть заключён на бумажном носителе или в электронном виде с УКЭП; электронный договор имеет равную юридическую силу с бумажным. (optional)",
   175	      "contract_position": "Пункт 12.4: «Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон.»",
   176	      "matrix_evidence": "«Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон.» (матрица 2.7)",
   177	      "contract_evidence": "«Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон.» (п. 12.4 Контракта)",
   178	      "status_reason": "Контракт реализует электронную опцию, предусмотренную матрицей: заключён в электронной форме с УКЭП. Матричный стандарт выполнен — контракт выбрал один из допустимых вариантов.",
   179	      "risk_level": "none",
   180	      "discrepancies": []
   181	    }
   182	  ],
   183	  "atomic_links": [
   184	    {"matrix_id": "2.1", "contract_id": "4.3", "relationship": "deviation", "link_index": 0, "coverage_role": "direct", "coverage": "Основной аналог: обязанность Заказчика предоставить заявление и информацию о ТСТ. Не покрывает право Банка на отказ, количество устройств, процедуру уведомления."},
   185	    {"matrix_id": "2.2", "contract_id": "5.1.8", "relationship": "aligned", "link_index": 1, "coverage_role": "direct", "coverage": "Прямое указание валюты расчётов (рубли РФ) в обязательстве Банка по перечислению сумм."},
   186	    {"matrix_id": "2.2", "contract_id": "Приложение_1_п5", "relationship": "aligned", "link_index": 1, "coverage_role": "context", "coverage": "Дополнительное подтверждение валюты расчётов в Техническом задании."},
   187	    {"matrix_id": "2.3.1", "contract_id": "2.3.1", "relationship": "aligned", "link_index": 2, "coverage_role": "direct", "coverage": "Полный аналог: email-канал, исключения, юридическая сила."},
   188	    {"matrix_id": "2.3.2", "contract_id": "2.3.2", "relationship": "aligned", "link_index": 3, "coverage_role": "direct", "coverage": "Полный аналог: канал ДБО."},
   189	    {"matrix_id": "2.3.3", "contract_id": "2.3.3", "relationship": "aligned", "link_index": 4, "coverage_role": "direct", "coverage": "Полный аналог: нарочный/курьерский канал."},
   190	    {"matrix_id": "2.3.4", "contract_id": "2.3.4", "relationship": "aligned", "link_index": 5, "coverage_role": "direct", "coverage": "Полный аналог: канал заказного письма."},
   191	    {"matrix_id": "2.3.5", "contract_id": "2.3.5", "relationship": "deviation", "link_index": 6, "coverage_role": "direct", "coverage": "Аналог канала ЭДО с УКЭП, но наименование системы не заполнено."},
   192	    {"matrix_id": "2.3.6", "contract_id": "2.3.6", "relationship": "aligned", "link_index": 7, "coverage_role": "direct", "coverage": "Полный аналог: канал ЕИС/ЭТП с УКЭП."},
   193	    {"matrix_id": "2.3.7", "contract_id": "2.3.7", "relationship": "deviation", "link_index": 8, "coverage_role": "direct", "coverage": "Канал службы поддержки и правила дат получения."},
   194	    {"matrix_id": "2.3.7", "contract_id": "2.3_receipt_dates", "relationship": "deviation", "link_index": 8, "coverage_role": "procedure", "coverage": "Правила определения дат получения; оператор ЭДО указан generic."},
   195	    {"matrix_id": "2.4", "contract_id": "1.1", "relationship": "deviation", "link_index": 9, "coverage_role": "direct", "coverage": "Указание на неотъемлемость Приложений №1 и №2."},
   196	    {"matrix_id": "2.4", "contract_id": "8.3.2", "relationship": "deviation", "link_index": 9, "coverage_role": "context", "coverage": "Указание на неотъемлемость прилагаемых к приёмке документов."},
   197	    {"matrix_id": "2.7", "contract_id": "12.4", "relationship": "aligned", "link_index": 10, "coverage_role": "direct", "coverage": "Контракт в электронной форме с УКЭП."}
   198	  ],
   199	  "unmatched_matrix": [
   200	    {
Tool:      1	{
     2	  "batch": "batch_2",
     3	  "matrix_range": "3.1-4.2.16",
     4	  "matrix_indices": [
     5	    18,
     6	    19,
     7	    20,
     8	    21,
     9	    22,
    10	    23,
    11	    24,
    12	    25,
    13	    26,
    14	    27,
    15	    28,
    16	    29,
    17	    30,
    18	    31,
    19	    32,
    20	    33,
    21	    34,
    22	    35,
    23	    36,
    24	    37,
    25	    38,
    26	    39,
    27	    40,
    28	    41
    29	  ],
    30	  "contract_product_profile": {
    31	    "product": [
    32	      "trade_acquiring"
    33	    ],
    34	    "lot": "44_fz",
    35	    "terminal": [
    36	      "pos"
    37	    ],
    38	    "payment_method": [
    39	      "cards",
    40	      "qr",
    41	      "nfc"
    42	    ],
    43	    "legal_regime": "44_fz"
    44	  },
    45	  "links": [
    46	    {
    47	      "matrix_ids": [
    48	        "3.1"
    49	      ],
    50	      "contract_ids": [
    51	        "1.3",
    52	        "Приложение №1 п.3",
    53	        "Приложение №1 п.5"
    54	      ],
    55	      "relationship": "aligned",
    56	      "legal_topic": "Предмет договора — организация приема оплаты с использованием карт",
    57	      "matrix_standard": "Предприятие организует прием оплаты с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ и обработку информации на Электронных терминалах. Перечень Карт — в Порядке проведения операций.",
    58	      "contract_position": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах (п.1.3). Перечень карт: МИР, VISA, MasterCard (Приложение №1 п.3). QR-код упомянут в Техническом задании (Приложение №1 п.5).",
    59	      "matrix_evidence": "Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ... Перечень Карт перечислен в Порядке проведения операций",
    60	      "contract_evidence": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах (п.1.3); Перечень карт включает НСПК МИР, VISA International, MasterCard (Приложение №1 п.3); Возможность вывода QR-кода для безналичной оплаты на дисплей терминала (Приложение №1 п.5)",
    61	      "status_reason": "Контракт содержит прямой аналог: Заказчик организует прием карт и обработку информации на электронных терминалах. Перечень карт включает НСПК МИР, VISA, MasterCard — стандартные платежные системы, не противоречащие матрице. Отсутствие упоминания SberPay и Плати QR в п.1.3 не является отклонением, так как матричный перечень — это варианты (slash-альтернативы), а контракт выбирает карты как основной инструмент. QR-код упомянут в Техническом задании.",
    62	      "risk_level": "none",
    63	      "discrepancies": []
    64	    },
    65	    {
    66	      "matrix_ids": [
    67	        "3.2"
    68	      ],
    69	      "contract_ids": [
    70	        "5.1.8",
    71	        "5.1.10",
    72	        "Приложение №1 п.5"
    73	      ],
    74	      "relationship": "aligned",
    75	      "legal_topic": "Обязанность Банка перечислять суммы операций Предприятию",
    76	      "matrix_standard": "Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ.",
    77	      "contract_position": "Исполнитель перечисляет Заказчику суммы Операций оплаты не позднее 2 рабочих дней с даты получения расчетной информации (п.5.1.8). Исполнитель перечисляет Заказчику суммы операций оплаты услуг, совершенных в ТСТ с использованием карт (п.5.1.10). Возмещение Заказчику денежных средств по операциям — в Приложении №1 п.5.",
    78	      "matrix_evidence": "Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ",
    79	      "contract_evidence": "не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты (п.5.1.8); Исполнитель в соответствии с контрактом перечисляет Заказчику суммы операций оплаты услуг (п.5.1.10)",
    80	      "status_reason": "Прямой аналог: обязанность Банка/Исполнителя перечислять суммы операций Заказчику закреплена в п.5.1.8 и п.5.1.10. Срок (2 рабочих дня) и механизм (на расчетный счет) конкретизированы, что усиливает позицию Банка по сравнению с общей формулировкой матрицы.",
    81	      "risk_level": "none",
    82	      "discrepancies": []
    83	    },
    84	    {
    85	      "matrix_ids": [
    86	        "3.3"
    87	      ],
    88	      "contract_ids": [
    89	        "3.2",
    90	        "4.5",
    91	        "5.3.2",
    92	        "8.3.1",
    93	        "8.3.2"
    94	      ],
    95	      "relationship": "deviation",
    96	      "legal_topic": "Обязанность Предприятия ежемесячно оплачивать услуги Банка",
    97	      "matrix_standard": "Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты.",
    98	      "contract_position": "Цена единицы услуги включает расходы Исполнителя за выполнение расчетов в виде процента от суммы каждой Операции оплаты (п.3.2). Оплата — по безналичному расчету, ежемесячно, не более 7 рабочих дней с даты подписания документа о приемке (п.4.5). Заказчик обязуется оплатить стоимость услуг (п.5.3.2). Документ о приемке формируется ежемесячно через ЕИС (п.8.3.1).",
    99	      "matrix_evidence": "Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты",
   100	      "contract_evidence": "Цена единицы услуги включает в себя расходы Исполнителя, связанные с оказанием услуг Банка за выполнение расчетов с Заказчиком по Операциям оплаты в виде процента от суммы каждой Операции оплаты (п.3.2); Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке (п.4.5)",
   101	      "status_reason": "Контракт содержит аналог обязанности оплаты, но с существенными отклонениями: (1) механизм оплаты — через 44-ФЗ (ЕИС, документ о приемке), а не прямой платеж по Разделу 6; (2) плата определена как процент от суммы операций, а не фиксированный тариф; (3) срок оплаты — 7 рабочих дней после приемки, а не календарно ежемесячно; (4) отсутствует ссылка на Раздел 6/Тарифы Банка как отдельный документ. Это стандартная для 44-ФЗ модель постоплаты.",
   102	      "risk_level": "low",
   103	      "discrepancies": [
   104	        {
   105	          "type": "procedure",
   106	          "description": "Оплата производится через механизм 44-ФЗ (ЕИС, документ о приемке), а не прямым перечислением по Разделу 6/Тарифам Банка",
   107	          "risk": "Процедура оплаты обусловлена бюджетным законодательством, что может задержать платеж, но является стандартным для госконтрактов"
   108	        },
   109	        {
   110	          "type": "deadline",
   111	          "description": "Срок оплаты — 7 рабочих дней после подписания документа о приемке, а не календарное ежемесячное перечисление",
   112	          "risk": "Незначительное procedural отличие, не создающее существенного риска для Банка"
   113	        }
   114	      ]
   115	    },
   116	    {
   117	      "matrix_ids": [
   118	        "4.1.1"
   119	      ],
   120	      "contract_ids": [
   121	        "5.4.5"
   122	      ],
   123	      "relationship": "aligned",
   124	      "legal_topic": "Право Предприятия ссылаться на возможность оплаты картами/QR с согласования Банка",
   125	      "matrix_standard": "Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода в информационных материалах, предварительно согласовав их с Банком.",
   126	      "contract_position": "Заказчик вправе ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем (п.5.4.5).",
   127	      "matrix_evidence": "Предприятие имеет право: Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком",
   128	      "contract_evidence": "Заказчик вправе: Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем настоящего контракта (п.5.4.5)",
   129	      "status_reason": "Прямой аналог: право Заказчика ссылаться на оплату картами с предварительным согласованием с Исполнителем. Отсутствие упоминания QR-кода в п.5.4.5 не является отклонением, так как QR-код — это опциональный метод (payment_method=qr), а контракт фокусируется на картах. Согласование через п.2.3.1 и 2.3.2 в матрице заменено на общее согласование с Исполнителем, что не меняет существа права.",
   130	      "risk_level": "none",
   131	      "discrepancies": []
   132	    },
   133	    {
   134	      "matrix_ids": [
   135	        "4.1.2"
   136	      ],
   137	      "contract_ids": [
   138	        "5.9",
   139	        "Приложение №1 п.5"
   140	      ],
   141	      "relationship": "aligned",
   142	      "legal_topic": "Право Предприятия на получение консультаций Банка",
   143	      "matrix_standard": "Предприятие имеет право получать консультацию в Банке по вопросам эксплуатации терминалов и проведению Операций путем обращения в службу поддержки Банка.",
   144	      "contract_position": "Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций с использованием карт путем обращения в службу поддержки исполнителя (п.5.9). Консультации персонала Заказчика по работе POS-терминала в телефонном режиме на горячей линии — неограниченное количество (Приложение №1 п.5).",
   145	      "matrix_evidence": "Предприятие имеет право: Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка",
   146	      "contract_evidence": "Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций с использованием карт путем обращения в службу поддержки исполнителя (п.5.9)",
   147	      "status_reason": "Прямой аналог: право Заказчика на консультации по эксплуатации терминалов и проведению операций через службу поддержки. Дополнительно в Техническом задании указан неограниченный объем консультаций.",
   148	      "risk_level": "none",
   149	      "discrepancies": []
   150	    },
   151	    {
   152	      "matrix_ids": [
   153	        "4.1.3"
   154	      ],
   155	      "contract_ids": [
   156	        "Приложение №1 п.5"
   157	      ],
   158	      "relationship": "deviation",
   159	      "legal_topic": "Право Предприятия использовать QR-коды, полученные от Банка",
   160	      "matrix_standard": "Предприятие имеет право использовать для приема оплаты по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на терминалах, мобильных устройствах, ККТ или на видном месте.",
   161	      "contract_position": "Терминалы Исполнителя должны иметь возможность вывода QR-кода для безналичной оплаты на дисплей терминала (Приложение №1 п.5).",
   162	      "matrix_evidence": "Предприятие имеет право: Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке",
   163	      "contract_evidence": "Терминалы Исполнителя должны иметь возможность вывода QR-кода для безналичной оплаты на дисплей терминала (Приложение №1 п.5)",
   164	      "status_reason": "Контракт упоминает QR-код только как техническую возможность терминала, но не содержит явного права Заказчика использовать QR-коды, полученные от Банка, для SberPayQR/Плати QR. Отсутствует указание на источник получения QR-кодов (Банк) и на конкретные платежные сервисы SberPayQR/Плати QR. Это ослабленная формулировка.",
   165	      "risk_level": "low",
   166	      "discrepancies": [
   167	        {
   168	          "type": "right",
   169	          "description": "Отсутствует прямое право Предприятия использовать QR-коды, полученные от Банка, для SberPayQR/Плати QR. QR-код упомянут только как техническая характеристика терминала",
   170	          "risk": "Низкий риск, так как контракт является 44-ФЗ и QR-функциональность заложена в техническом задании. Отсутствие явного права не блокирует использование QR"
   171	        }
   172	      ]
   173	    },
   174	    {
   175	      "matrix_ids": [
   176	        "4.2.1"
   177	      ],
   178	      "contract_ids": [
   179	        "3.2",
   180	        "4.5",
   181	        "5.3.2"
   182	      ],
   183	      "relationship": "deviation",
   184	      "legal_topic": "Обязанность Предприятия оплачивать услуги Банка",
   185	      "matrix_standard": "Предприятие обязуется оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка (Раздел 6).",
   186	      "contract_position": "Цена единицы услуги включает расходы Исполнителя в виде процента от суммы каждой Операции оплаты (п.3.2). Оплата ежемесячно, не более 7 рабочих дней после приемки (п.4.5). Заказчик обязуется оплатить стоимость услуг (п.5.3.2).",
   187	      "matrix_evidence": "Предприятие обязуется: Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6",
   188	      "contract_evidence": "Цена единицы услуги включает в себя расходы Исполнителя... в виде процента от суммы каждой Операции оплаты (п.3.2); Срок оплаты... не более 7 рабочих дней с даты подписания Заказчиком документа о приемке (п.4.5)",
   189	      "status_reason": "Обязанность оплаты присутствует, но с отклонениями: (1) оплата через 44-ФЗ (ЕИС, документ о приемке), а не по Тарифам Банка/Разделу 6; (2) плата за сервисное обслуживание не выделена отдельно (в Техническом задании указано: комиссия за терминалы — отсутствует, абонентская плата — отсутствует); (3) цена определена как процент от операций, а не через Тарифы. Это стандартная модель 44-ФЗ.",
   190	      "risk_level": "low",
   191	      "discrepancies": [
   192	        {
   193	          "type": "procedure",
   194	          "description": "Оплата производится через механизм 44-ФЗ, а не по Тарифам Банка/Разделу 6. Плата за сервисное обслуживание не предусмотрена (комиссия и абонентская плата за терминалы отсутствуют)",
   195	          "risk": "Низкий риск: модель постоплаты через 44-ФЗ является стандартной для госконтрактов. Отсутствие платы за сервисное обслуживание отражено в Техническом задании"
   196	        }
   197	      ]
   198	    },
   199	    {
   200	      "matrix_ids": [
AI: Now let me read the remaining batch outputs and check for any existing `unmatched_contract` / `extra_in_contract` findings:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_3_output.json', 'limit': 200}, 'id': 'call_00_MtUw22aXZ6tooWsRz5P02902', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_4_output.json', 'limit': 200}, 'id': 'call_01_ARNMsj6c48hkBoA7nJJr8134', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/check_extra.py', 'limit': 200}, 'id': 'call_02_kGWX6fygPvfHYVQCy89x2818', 'type': 'tool_call'}]
Tool:      1	{
     2	  "batch": "batch_3",
     3	  "matrix_range": "4.2.17-5.1.17.2",
     4	  "contract_product_profile": {
     5	    "product": [
     6	      "trade_acquiring"
     7	    ],
     8	    "lot": "44_fz",
     9	    "terminal": [
    10	      "pos"
    11	    ],
    12	    "payment_method": [
    13	      "cards",
    14	      "qr",
    15	      "nfc"
    16	    ],
    17	    "legal_regime": "44_fz"
    18	  },
    19	  "links": [
    20	    {
    21	      "matrix_ids": [
    22	        "4.2.18"
    23	      ],
    24	      "contract_ids": [
    25	        "5.3.16"
    26	      ],
    27	      "relationship": "aligned",
    28	      "legal_topic": "Обязанность прекратить прием карт и снять информационные материалы при расторжении",
    29	      "matrix_standard": "С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы, извещающие об обслуживании Карт.",
    30	      "contract_position": "Пункт 5.3.16: С даты расторжения контракта прекратить прием к оплате карт, снять рекламно-информационные материалы, извещающие об обслуживании карт.",
    31	      "matrix_evidence": "«С даты расторжения Договора прекратить прием к оплате Карт, снять/удалить информационные материалы, извещающие об обслуживании Карт.» (матрица 4.2.18)",
    32	      "contract_evidence": "«С даты расторжения контракта прекратить прием к оплате карт, снять рекламно-информационные материалы, извещающие об обслуживании карт» (п. 5.3.16 Контракта)",
    33	      "status_reason": "Прямой аналог: обязанность Заказчика прекратить прием карт и снять информационные материалы с даты расторжения контракта полностью соответствует матричному стандарту. Формулировка практически идентична.",
    34	      "risk_level": "none",
    35	      "discrepancies": []
    36	    },
    37	    {
    38	      "matrix_ids": [
    39	        "4.2.19"
    40	      ],
    41	      "contract_ids": [
    42	        "5.3.17"
    43	      ],
    44	      "relationship": "aligned",
    45	      "legal_topic": "Обязанность не препятствовать проверкам Банка и содействовать расследованиям",
    46	      "matrix_standard": "Предприятие обязуется не принимать мер противодействия Банку в проведении проверки Предприятия/ТСТ/Ресурса на предмет выявления мошеннических Операций и/или предоставления Покупателям Товаров/услуг, не соответствующих роду деятельности Предприятия/ТСТ, а также оказывать содействие Банку в проведении разбирательства по факту совершения подозрительных Операций.",
    47	      "contract_position": "Пункт 5.3.17: Заказчик обязуется не принимать мер противодействия исполнителю в проведение проверки заказчика/ТСТ на предмет выявления мошеннических операций и/или предоставления покупателям товаров/услуг, не соответствующих роду деятельности заказчика/ТСТ, а также оказывать содействие исполнителю в проведении разбирательства по факту совершения подозрительных операций.",
    48	      "matrix_evidence": "«Предприятие обязуется: → Не принимать мер противодействия Банку в проведении проверки Предприятия/ТСТ/Ресурса на предмет выявления мошеннических Операций... а также оказывать содействие Банку в проведении разбирательства по факту совершения подозрительных Операций.» (матрица 4.2.19)",
    49	      "contract_evidence": "«Не принимать мер противодействия исполнителю в проведение проверки заказчика/ТСТ на предмет выявления мошеннических операций и/или предоставления покупателям товаров/услуг, не соответствующих роду деятельности заказчика/ТСТ, а также оказывать содействие исполнителю в проведении разбирательства по факту совершения подозрительных операций» (п. 5.3.17 Контракта)",
    50	      "status_reason": "Прямой аналог: обе обязанности — не препятствовать проверкам и содействовать расследованиям — полностью сохранены. Формулировка практически идентична матричной. Отсутствие упоминания Ресурса несущественно для trade_acquiring.",
    51	      "risk_level": "none",
    52	      "discrepancies": []
    53	    },
    54	    {
    55	      "matrix_ids": [
    56	        "4.2.20.1"
    57	      ],
    58	      "contract_ids": [
    59	        "5.10"
    60	      ],
    61	      "relationship": "deviation",
    62	      "legal_topic": "Обязанность Предприятия обеспечить прохождение инструктажа сотрудниками",
    63	      "matrix_standard": "Предприятие обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: https://www.sberbank.ru/help/business/acquiring.",
    64	      "contract_position": "Пункт 5.10: Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________ (адрес сайта не заполнен).",
    65	      "matrix_evidence": "«Обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: https://www.sberbank.ru/help/business/acquiring.» (матрица 4.2.20.1)",
    66	      "contract_evidence": "«Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________» (п. 5.10 Контракта)",
    67	      "status_reason": "Обязанность проведения инструктажа сохранена, но адрес сайта с инструктивными материалами оставлен незаполненным (placeholder). Это отклонение, так как отсутствие конкретного адреса создает неопределенность относительно источника инструктивных материалов.",
    68	      "risk_level": "low",
    69	      "discrepancies": [
    70	        {
    71	          "type": "missing_element",
    72	          "description": "Адрес сайта с инструктивными материалами (https://www.sberbank.ru/help/business/acquiring) не заполнен в контракте — поле оставлено пустым (placeholder).",
    73	          "risk": "Низкий риск: адрес может быть заполнен при подписании. Однако в текущем виде создает неопределенность относительно источника инструктивных материалов."
    74	        }
    75	      ]
    76	    },
    77	    {
    78	      "matrix_ids": [
    79	        "4.2.20.2"
    80	      ],
    81	      "contract_ids": [
    82	        "5.3.18.1"
    83	      ],
    84	      "relationship": "aligned",
    85	      "legal_topic": "Обязанность использовать терминалы и ПО Банка только для целей договора, не изменять, не ремонтировать, не передавать третьим лицам",
    86	      "matrix_standard": "Использовать Электронные терминалы/Смарт-терминалы и ПО Банка только для целей Договора и на территории регистрации ТСТ. Не вносить изменения в ПО и терминалы. Не осуществлять самостоятельный ремонт. Не передавать третьим лицам терминалы, документы и инструктивные материалы (кроме Обслуживающей компании).",
    87	      "contract_position": "Пункт 5.3.18.1: Использовать электронные терминалы/смарт-терминалы и ПО только для целей контракта и на территории регистрации ТСТ. Не вносить изменения в ПО и терминалы, не осуществлять самостоятельно их ремонт. Не передавать третьим лицам терминалы, документы, термоленту и рекламно-инструктивные материалы (кроме работников обслуживающей компании).",
    88	      "matrix_evidence": "«Использовать Электронные терминалы... только для целей реализации настоящего Договора и на территории регистрации ТСТ... Не вносить изменения в программное обеспечение и Электронные терминалы... Не осуществлять самостоятельно ремонт... Не передавать третьим лицам...» (матрица 4.2.20.2)",
    89	      "contract_evidence": "«Использовать электронные терминалы... только для целей реализации настоящего контракта и на территории регистрации ТСТ... Не вносить изменения в программное обеспечение и электронные терминалы... не осуществлять самостоятельно их ремонт... Не передавать третьим лицам...» (п. 5.3.18.1 Контракта)",
    90	      "status_reason": "Прямой аналог: все четыре обязанности (использование по назначению и на территории ТСТ, запрет изменений, запрет самостоятельного ремонта, запрет передачи третьим лицам) полностью сохранены. Добавлено упоминание термоленты, что не противоречит матрице.",
    91	      "risk_level": "none",
    92	      "discrepancies": []
    93	    },
    94	    {
    95	      "matrix_ids": [
    96	        "4.2.20.3"
    97	      ],
    98	      "contract_ids": [
    99	        "5.3.18.2"
   100	      ],
   101	      "relationship": "aligned",
   102	      "legal_topic": "Обязанность предоставлять доступ к местам установки терминалов для обслуживания",
   103	      "matrix_standard": "Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов/Смарт-терминалов для проведения работ по их подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке.",
   104	      "contract_position": "Пункт 5.3.18.2: Предоставлять исполнителю доступ к местам установки электронных терминалов для проведения работ по его подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке.",
   105	      "matrix_evidence": "«Предоставлять уполномоченным работникам Обслуживающей компании доступ к местам установки Электронных терминалов/Смарт-терминалов для проведения работ по их подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке.» (матрица 4.2.20.3)",
   106	      "contract_evidence": "«Предоставлять исполнителю доступ к местам установки электронных терминалов для проведения работ по его подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке» (п. 5.3.18.2 Контракта)",
   107	      "status_reason": "Прямой аналог: обязанность предоставлять доступ для всех перечисленных видов работ (подключение, настройка, ремонт, замена, техобслуживание, визуальная проверка) полностью сохранена. В контракте доступ предоставляется Исполнителю (а не Обслуживающей компании), что не меняет существа обязанности.",
   108	      "risk_level": "none",
   109	      "discrepancies": []
   110	    },
   111	    {
   112	      "matrix_ids": [
   113	        "4.2.20.4"
   114	      ],
   115	      "contract_ids": [
   116	        "5.3.18.3"
   117	      ],
   118	      "relationship": "deviation",
   119	      "legal_topic": "Обязанность принять терминалы по акту принятия оказанных услуг",
   120	      "matrix_standard": "Принять Электронные терминалы/Смарт-терминалы Банка и/или ПО для Смарт-терминалов по акту принятия оказанных услуг по форме Обслуживающей компании, составленному в 2-х экземплярах, подписанных уполномоченными работниками Обслуживающей компании и Предприятия. Один экземпляр — в Обслуживающей компании, второй — у Предприятия. Форма акта размещена на Официальном сайте Банка.",
   121	      "contract_position": "Пункт 5.3.18.3: Принять электронные терминалы по акту принятия оказанных услуг, составленному в двух экземплярах и подписанных исполнителем и заказчиком. Один экземпляр акта находится на хранении у исполнителя, второй — у заказчика.",
   122	      "matrix_evidence": "«Принять Электронные терминалы/Смарт-терминалы Банка... по акту принятия оказанных услуг по форме Обслуживающей компании, составленному в 2-х (два) экземплярах... Форма акта размещена на Официальном сайте Банка.» (матрица 4.2.20.4)",
   123	      "contract_evidence": "«Принять электронные терминалы по акту принятия оказанных услуг, составленному в двух экземплярах и подписанных исполнителем и заказчиком. один экземпляр акта находится на хранении у исполнителя, второй – у заказчика» (п. 5.3.18.3 Контракта)",
   124	      "status_reason": "Аналог присутствует, но с отклонениями: (1) акт подписывается Исполнителем и Заказчиком, а не Обслуживающей компанией и Предприятием — допустимое терминологическое различие для 44-ФЗ; (2) отсутствует указание на форму акта, размещенную на Официальном сайте Банка; (3) отсутствует упоминание ПО для Смарт-терминалов (не применимо к pos-профилю).",
   125	      "risk_level": "low",
   126	      "discrepancies": [
   127	        {
   128	          "type": "procedure",
   129	          "description": "Отсутствует указание на форму акта, размещенную на Официальном сайте Банка. Акт подписывается Исполнителем, а не Обслуживающей компанией.",
   130	          "risk": "Низкий риск: для 44-ФЗ контракта подписание акта Исполнителем (а не Обслуживающей компанией) является стандартной практикой. Отсутствие ссылки на форму акта на сайте Банка не блокирует приемку."
   131	        }
   132	      ]
   133	    },
   134	    {
   135	      "matrix_ids": [
   136	        "4.2.20.5"
   137	      ],
   138	      "contract_ids": [
   139	        "5.3.20.4"
   140	      ],
   141	      "relationship": "deviation",
   142	      "legal_topic": "Обязанность немедленно информировать Банк о выходе терминала из строя или утрате",
   143	      "matrix_standard": "В случае выхода Электронного терминала/Смарт-терминала, в том числе Мобильного устройства Предприятия, из строя или его утраты немедленно информировать об этом Банк в соответствии с п. 2.3.1, п. 2.3.2 Договора или путем обращения в службу поддержки Банка.",
   144	      "contract_position": "Пункт 5.3.20.4: В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя.",
   145	      "matrix_evidence": "«В случае выхода Электронного терминала/Смарт-терминала... из строя или его утраты немедленно информировать об этом Банк в соответствии с п. 2.3.1, п. 2.3.2 Договора или путем обращения в службу поддержки Банка.» (матрица 4.2.20.5)",
   146	      "contract_evidence": "«В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя» (п. 5.3.20.4 Контракта)",
   147	      "status_reason": "Обязанность информирования сохранена, но отсутствует указание на конкретные каналы информирования (п. 2.3.1, 2.3.2 или служба поддержки). Также отсутствует упоминание Смарт-терминалов и Мобильных устройств (не применимо к pos-профилю). Отсутствие указания каналов связи создает неопределенность.",
   148	      "risk_level": "low",
   149	      "discrepancies": [
   150	        {
   151	          "type": "procedure",
   152	          "description": "Отсутствует указание на конкретные каналы информирования Банка (п. 2.3.1, 2.3.2 или служба поддержки).",
   153	          "risk": "Низкий риск: общая обязанность информирования сохранена. Каналы связи определены в разделе 2.3 контракта и могут применяться по умолчанию."
   154	        }
   155	      ]
   156	    },
   157	    {
   158	      "matrix_ids": [
   159	        "4.2.20.6"
   160	      ],
   161	      "contract_ids": [
   162	        "5.3.18.5",
   163	        "5.6"
   164	      ],
   165	      "relationship": "aligned",
   166	      "legal_topic": "Обязанность вернуть терминалы в течение 5 рабочих дней после расторжения или требования Банка",
   167	      "matrix_standard": "Вернуть Банку или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Договора или с даты получения письменного/устного требования Банка о возврате.",
   168	      "contract_position": "Пункт 5.3.18.5: Вернуть исполнителю или обслуживающей компании электронные терминалы/смарт-терминала в течение пяти рабочих дней с даты расторжения контракта или с даты получения письменного/устного требования исполнителя о возврате. Пункт 5.6 дублирует эту обязанность.",
   169	      "matrix_evidence": "«Вернуть Банку или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Договора или с даты получения письменного/устного требования Банка о возврате.» (матрица 4.2.20.6)",
   170	      "contract_evidence": "«Вернуть исполнителю или обслуживающей компании электронные терминалы/смарт-терминала в течение пяти рабочих дней с даты расторжения контракта или с даты получения письменного/устного требования исполнителя о возврате электронных терминалов» (п. 5.3.18.5); «Вернуть Исполнителю или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней...» (п. 5.6)",
   171	      "status_reason": "Прямой аналог: срок (5 рабочих дней), альтернативные основания (расторжение или требование), форма требования (письменное/устное) и адресат возврата (Банк/Исполнитель или Обслуживающая компания) полностью сохранены. Обязанность дублируется в п. 5.6, что усиливает позицию.",
   172	      "risk_level": "none",
   173	      "discrepancies": []
   174	    },
   175	    {
   176	      "matrix_ids": [
   177	        "4.2.20.7"
   178	      ],
   179	      "contract_ids": [
   180	        "5.7"
   181	      ],
   182	      "relationship": "deviation",
   183	      "legal_topic": "Штраф за невозврат терминалов",
   184	      "matrix_standard": "В случае невозврата Электронных терминалов/Смарт-терминалов Банка уплатить Банку штраф в размере 25 000 рублей, в том числе НДС, за каждый Электронный терминал и 25 000 рублей, в том числе НДС за каждый Смарт-терминал Банка.",
   185	      "contract_position": "Пункт 5.7: В случае невозврата Электронных терминалов/Смарт-терминалов Исполнителя Заказчик обязан уплатить Исполнителю штраф в размере 10 000 рублей, включая НДС, за каждый Электронный терминал, в размере 25 000 рублей, включая НДС, за каждый Смарт-терминал Банка.",
   186	      "matrix_evidence": "«В случае невозврата Электронных терминалов/Смарт-терминалов Банка... уплатить Банку штраф в размере 25 000 (двадцать пять тысяч) рублей, в том числе НДС, за каждый Электронный терминал и 25 000 (двадцать пять тысяч) рублей, в том числе НДС за каждый Смарт-терминал Банка.» (матрица 4.2.20.7)",
   187	      "contract_evidence": "«В случае невозврата Электронных терминалов/Смарт-терминалов Исполнителя Заказчик обязан уплатить Исполнителю штраф в размере 10 000 (десяти тысяч) рублей, включая НДС, за каждый Электронный терминал, в размере 25 000 (двадцати пяти тысяч) рублей, включая НДС, за каждый Смарт-терминал Банка.» (п. 5.7 Контракта)",
   188	      "status_reason": "Аналог присутствует, но размер штрафа за Электронный терминал снижен с 25 000 до 10 000 рублей. Штраф за Смарт-терминал сохранен (25 000 рублей). Это существенное снижение штрафной санкции для pos-терминалов.",
   189	      "risk_level": "medium",
   190	      "discrepancies": [
   191	        {
   192	          "type": "amount",
   193	          "description": "Штраф за невозврат Электронного терминала снижен с 25 000 до 10 000 рублей (снижение на 60%). Штраф за Смарт-терминал сохранен на уровне 25 000 рублей.",
   194	          "risk": "Средний риск: снижение штрафа за pos-терминал ослабляет стимул Заказчика к своевременному возврату оборудования. При утрате терминала Банк получит меньшую компенсацию."
   195	        }
   196	      ]
   197	    },
   198	    {
   199	      "matrix_ids": [
   200	        "4.2.22"
Tool:      1	{
     2	  "batch": "batch_4",
     3	  "scope": "5.2.1-11.13",
     4	  "profile_applied": {
     5	    "product": [
     6	      "trade_acquiring"
     7	    ],
     8	    "lot": "44_fz",
     9	    "terminal": [
    10	      "pos"
    11	    ],
    12	    "payment_method": [
    13	      "cards",
    14	      "qr",
    15	      "nfc"
    16	    ],
    17	    "legal_regime": "44_fz"
    18	  },
    19	  "filtered_out": [
    20	    {
    21	      "matrix_id": "5.2.1",
    22	      "reason": "product filter: internet_acquiring only, contract is trade_acquiring"
    23	    },
    24	    {
    25	      "matrix_id": "5.2.2",
    26	      "reason": "product filter: internet_acquiring only, contract is trade_acquiring"
    27	    },
    28	    {
    29	      "matrix_id": "5.2.12",
    30	      "reason": "product filter: internet_acquiring only, contract is trade_acquiring"
    31	    },
    32	    {
    33	      "matrix_id": "6.3",
    34	      "reason": "lot filter: fz_223 only, contract is 44_fz"
    35	    },
    36	    {
    37	      "matrix_id": "6.6",
    38	      "reason": "lot filter: fz_223 only, contract is 44_fz"
    39	    },
    40	    {
    41	      "matrix_id": "6.7",
    42	      "reason": "terminal filter: smart only, contract has pos terminals"
    43	    },
    44	    {
    45	      "matrix_id": "6.8",
    46	      "reason": "terminal filter: smart only, contract has pos terminals"
    47	    },
    48	    {
    49	      "matrix_id": "6.9",
    50	      "reason": "lot filter: fz_223 + terminal: smart; contract is 44_fz with pos"
    51	    },
    52	    {
    53	      "matrix_id": "6.10",
    54	      "reason": "terminal filter: smart only, contract has pos terminals"
    55	    },
    56	    {
    57	      "matrix_id": "6.11",
    58	      "reason": "terminal filter: smart only, contract has pos terminals"
    59	    },
    60	    {
    61	      "matrix_id": "6.12",
    62	      "reason": "lot filter: fz_223 + terminal: smart; contract is 44_fz with pos"
    63	    },
    64	    {
    65	      "matrix_id": "6.13",
    66	      "reason": "terminal filter: smart only, contract has pos terminals"
    67	    },
    68	    {
    69	      "matrix_id": "6.14",
    70	      "reason": "terminal filter: smart only, contract has pos terminals"
    71	    },
    72	    {
    73	      "matrix_id": "6.15",
    74	      "reason": "lot filter: fz_223 + terminal: smart; contract is 44_fz with pos"
    75	    },
    76	    {
    77	      "matrix_id": "6.16",
    78	      "reason": "terminal filter: smart only, contract has pos terminals"
    79	    },
    80	    {
    81	      "matrix_id": "6.17",
    82	      "reason": "terminal filter: smart only, contract has pos terminals"
    83	    },
    84	    {
    85	      "matrix_id": "6.18",
    86	      "reason": "lot filter: fz_223 + terminal: smart; contract is 44_fz with pos"
    87	    },
    88	    {
    89	      "matrix_id": "7.13",
    90	      "reason": "product filter: internet_acquiring only, contract is trade_acquiring"
    91	    }
    92	  ],
    93	  "links": [
    94	    {
    95	      "matrix_ids": [
    96	        "5.2.3"
    97	      ],
    98	      "contract_ids": [
    99	        "5.1.1",
   100	        "Tech_5"
   101	      ],
   102	      "relationship": "deviation",
   103	      "legal_topic": "Bank obligation to install and prepare terminals, conduct staff training",
   104	      "matrix_standard": "Bank shall install and prepare for operation Electronic terminals/Smart-terminals at the Enterprise. Conduct initial training of TST employees in accordance with instructional materials provided by the Bank. Installation deadline: not less than 3 working days.",
   105	      "contract_position": "Contractor shall install and prepare for operation Electronic terminals within 5 working days from contract signing. Conduct initial training of TST employees in accordance with instructional materials provided by the Bank. Post training materials on website: _______. Technical specification also requires installation, training, and instructional materials.",
   106	      "matrix_evidence": "Установить на Предприятии и подготовить к эксплуатации Электронные терминалы/Смарт-терминалы Банка для проведения Операций. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком",
   107	      "contract_evidence": "5.1.1: Установить Заказчику и подготовить к эксплуатации Электронные терминалы для проведения операций в течение 5 (пяти) рабочих дней с даты подписания контракта. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком.",
   108	      "status_reason": "Contract covers installation, preparation, and training obligations. However, the matrix requires installation within 'not less than 3 working days' (meaning the Bank standard expects at least 3 days for installation), while the contract sets a 5-working-day deadline. The matrix main_idea states: 'Важно, чтобы в договоре срок установки был не менее 3 рабочих дней' — meaning the Bank wants at least 3 days. The contract's 5-day deadline is actually more favorable to the Bank (longer period). However, the matrix also references Smart-terminals which are not in scope. The training website URL is blank (_______) in the contract vs. a specific Sberbank URL in the matrix.",
   109	      "risk_level": "low",
   110	      "discrepancies": [
   111	        {
   112	          "type": "deadline",
   113	          "description": "Matrix expects installation deadline of not less than 3 working days; contract sets 5 working days. This is actually more favorable to the Bank (longer period).",
   114	          "risk": "Low — longer deadline benefits the Bank. No adverse risk."
   115	        },
   116	        {
   117	          "type": "other",
   118	          "description": "Training materials website URL is blank (_______) in contract clause 5.1.1 vs. specific URL https://www.sberbank.ru/help/business/acquiring in matrix item 5.2.5.",
   119	          "risk": "Low — placeholder for website; per matrix main_idea for 5.2.5, a blank/procherk is not a discrepancy."
   120	        }
   121	      ]
   122	    },
   123	    {
   124	      "matrix_ids": [
   125	        "5.2.4"
   126	      ],
   127	      "contract_ids": [
   128	        "5.1.6"
   129	      ],
   130	      "relationship": "aligned",
   131	      "legal_topic": "Bank obligation to provide 24/7 authorization",
   132	      "matrix_standard": "Bank shall carry out round-the-clock Authorization",
   133	      "contract_position": "Contractor shall carry out round-the-clock authorization",
   134	      "matrix_evidence": "Осуществлять круглосуточную Авторизацию",
   135	      "contract_evidence": "5.1.6: Осуществлять круглосуточную авторизацию;",
   136	      "status_reason": "Exact match. Both matrix and contract require 24/7 authorization by the Bank/Contractor.",
   137	      "risk_level": "none",
   138	      "discrepancies": []
   139	    },
   140	    {
   141	      "matrix_ids": [
   142	        "5.2.5"
   143	      ],
   144	      "contract_ids": [
   145	        "5.1.1",
   146	        "5.10"
   147	      ],
   148	      "relationship": "deviation",
   149	      "legal_topic": "Bank obligation to post training materials on website",
   150	      "matrix_standard": "Bank shall post training materials at https://www.sberbank.ru/help/business/acquiring for employee training",
   151	      "contract_position": "Contractor shall post training materials on website: _______ (blank). Customer shall ensure employees independently complete training posted at: _______ (blank).",
   152	      "matrix_evidence": "Разместить на сайте: https://www.sberbank.ru/help/business/acquiring обучающие материалы для прохождения инструктажа сотрудниками Предприятия",
   153	      "contract_evidence": "5.1.1: Разместить на сайте: ___________________ обучающие материалы для прохождения инструктажа сотрудниками Заказчика. 5.10: Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________.",
   154	      "status_reason": "Contract contains the training materials obligation but the website URL is a blank placeholder. Per matrix main_idea for 5.2.5: 'Подсвечивать разногласие, если только сайты отличаются, если в договоре вместо сайта прочерк, то это не разногласие' — a blank/procherk is explicitly NOT a discrepancy per the matrix author. However, the blank creates operational uncertainty.",
   155	      "risk_level": "low",
   156	      "discrepancies": [
   157	        {
   158	          "type": "other",
   159	          "description": "Training materials website URL is blank placeholder (_______) in both 5.1.1 and 5.10. Per matrix guidance, blank is not a discrepancy but creates operational gap.",
   160	          "risk": "Low — per matrix author guidance, blank URL is not treated as a deviation. However, without a filled URL, employees cannot access training materials."
   161	        }
   162	      ]
   163	    },
   164	    {
   165	      "matrix_ids": [
   166	        "5.2.6"
   167	      ],
   168	      "contract_ids": [
   169	        "5.1.7"
   170	      ],
   171	      "relationship": "aligned",
   172	      "legal_topic": "Bank obligation to provide informational materials for terminals",
   173	      "matrix_standard": "Bank shall provide Electronic terminals/Smart-terminals installed at the Enterprise/TST with informational materials necessary for conducting Operations",
   174	      "contract_position": "Contractor shall provide electronic terminals installed at the customer/TST with advertising and informational materials necessary for conducting operations using cards",
   175	      "matrix_evidence": "Обеспечивать Электронные терминалы/Смарт-терминалы, установленные на Предприятии/ТСТ, информационными материалами, необходимыми для проведения Операций",
   176	      "contract_evidence": "5.1.7: Обеспечивать электронные терминалы, установленные у заказчика/ТСТ, рекламно-информационными материалами, необходимыми для проведения операций с использованием карт;",
   177	      "status_reason": "Substantially aligned. Contract adds 'рекламно-' (advertising) qualifier and specifies 'с использованием карт' (using cards), but the core obligation to provide informational materials for terminals is preserved.",
   178	      "risk_level": "none",
   179	      "discrepancies": []
   180	    },
   181	    {
   182	      "matrix_ids": [
   183	        "5.2.7"
   184	      ],
   185	      "contract_ids": [
   186	        "5.1.4"
   187	      ],
   188	      "relationship": "aligned",
   189	      "legal_topic": "Bank obligation to ensure 24/7 terminal operability and replacement within 3 working days",
   190	      "matrix_standard": "Bank shall ensure round-the-clock operability of Electronic terminals/Smart-terminals. In case of failure, provide the Enterprise with a working terminal within 3 working days from receipt of the Enterprise's request via Bank support service phone numbers.",
   191	      "contract_position": "Contractor shall ensure round-the-clock operability of Electronic terminals. In case of failure, provide the Customer with a working Bank terminal within 3 working days from receipt of the Customer's request via Bank support service number.",
   192	      "matrix_evidence": "Обеспечивать круглосуточную работоспособность Электронных терминалов/Смарт-терминалов. В случае выхода из строя Электронного терминала/Смарт-терминала Банка, обеспечить Предприятие исправным Электронным терминалом/Смарт-терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Банком заявки от Предприятия по номеру службы поддержки Банка",
   193	      "contract_evidence": "5.1.4: Обеспечивать круглосуточную работоспособность Электронных терминалов. В случае выхода из строя Электронного терминала, обеспечить Заказчика исправным Электронным терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Исполнителем заявки от Заказчикам по номеру службы поддержки Банка.",
   194	      "status_reason": "Aligned. Same 24/7 operability obligation, same 3-working-day replacement deadline, same trigger (request via support service). Contract omits Smart-terminals (not in scope).",
   195	      "risk_level": "none",
   196	      "discrepancies": []
   197	    },
   198	    {
   199	      "matrix_ids": [
   200	        "5.2.8"
Tool:      1	import json
     2	data = json.load(open('outputs/working/batch_4_output.json','r'))
     3	print('Extra in contract:')
     4	for e in data['unmatched_contract']:
     5	    print(f"  {e['contract_id']}: {e['contract_position'][:120]}")
     6	    print(f"    risk: {e['risk_level']}")
     7	    print()
AI: Let me now read the rest of the batch outputs to see what unmatched_contract items have already been identified, and also read the full contract text to identify any remaining contract-only terms:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_1_output.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_leTkRfOSnb7q2EXOD34S6092', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_2_output.json', 'offset': 200, 'limit': 300}, 'id': 'call_01_eijCro88eUQDEjXIUhyL6255', 'type': 'tool_call'}]
Tool:    201	      "matrix_id": "2.5.1.1",
   202	      "requirement": "SberPayOnline подключается автоматически при подключении Интернет-эквайринга с единым тарифом.",
   203	      "source_evidence": "«при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу» (матрица 2.5.1.1)",
   204	      "status": "missing_in_contract",
   205	      "required_type": "mandatory",
   206	      "applicability": "not_applicable",
   207	      "risk_level": "low",
   208	      "risk": "Матричный фильтр only_for_product=internet_acquiring. Контракт покрывает только торговый эквайринг (trade_acquiring). Интернет-эквайринг не входит в предмет контракта. Требование неприменимо.",
   209	      "rejected_candidates": []
   210	    },
   211	    {
   212	      "matrix_id": "2.5.2.1",
   213	      "requirement": "SberPayFaceScan подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе Информации о ТСТ.",
   214	      "source_evidence": "«Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.» (матрица 2.5.2.1)",
   215	      "status": "missing_in_contract",
   216	      "required_type": "mandatory",
   217	      "applicability": "not_applicable",
   218	      "risk_level": "low",
   219	      "risk": "Матричный фильтр payment_method=sber_pay_face_scan. Контракт не предусматривает биометрическую оплату (SberPay Face Scan). В Приложении 1.2 есть поле «проведение операций с биометрическим методом идентификации», но оно не заполнено (☐). Требование неприменимо.",
   220	      "rejected_candidates": [
   221	        {
   222	          "contract_id": "Приложение_1.2_биометрия",
   223	          "reason": "Поле «проведение операций с биометрическим методом идентификации» в форме Информации о ТСТ не отмечено (пустой чекбокс). Это не активирует SberPayFaceScan."
   224	        }
   225	      ]
   226	    },
   227	    {
   228	      "matrix_id": "2.6.1.1",
   229	      "requirement": "QR-код на Смарт-терминалах подключается при установке Смарт-терминала Банка/ПО Банка для Смарт-терминала Предприятия в ТСТ.",
   230	      "source_evidence": "«ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.» (матрица 2.6.1.1)",
   231	      "status": "missing_in_contract",
   232	      "required_type": "mandatory",
   233	      "applicability": "conditional",
   234	      "risk_level": "medium",
   235	      "risk": "Матричный фильтр only_for_terminal=smart. Контракт содержит упоминания смарт-терминалов в определениях (п. 2.1.13) и формах Приложения 1.2, но не содержит положения об автоматической активации QR-кода при установке смарт-терминала. Отсутствие данной нормы создаёт неопределённость: должен ли QR активироваться отдельным заявлением или автоматически.",
   236	      "rejected_candidates": [
   237	        {
   238	          "contract_id": "Приложение_1_QR_дисплей",
   239	          "reason": "Техническое задание требует «Возможность вывода QR-кода для безналичной оплаты на дисплей терминала», но это общая техническая спецификация, а не норма о порядке подключения QR на смарт-терминалах."
   240	        }
   241	      ]
   242	    },
   243	    {
   244	      "matrix_id": "2.6.2.1",
   245	      "requirement": "При наличии у Предприятия собственного ПО — QR-код через QR-API; порядок и условия на Официальном сайте Банка.",
   246	      "source_evidence": "«при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка» (матрица 2.6.2.1)",
   247	      "status": "missing_in_contract",
   248	      "required_type": "mandatory",
   249	      "applicability": "applicable",
   250	      "risk_level": "medium",
   251	      "risk": "Контракт предусматривает QR-оплату (Техническое задание), но не содержит механизма QR-API для собственного ПО Предприятия и не содержит отсылки к сайту Банка с порядком подключения. При наличии у Заказчика собственного ПО ККТ (в контракте упоминается система «Барс» НПО «Дата Крат») отсутствие QR-API механизма может заблокировать интеграцию.",
   252	      "rejected_candidates": [
   253	        {
   254	          "contract_id": "Приложение_1_QR_дисплей",
   255	          "reason": "Общая спецификация о возможности вывода QR-кода не является аналогом конкретного механизма QR-API."
   256	        },
   257	        {
   258	          "contract_id": "Приложение_1.2_QR_API",
   259	          "reason": "В форме Информации о ТСТ (Приложение 1.2) есть поле «QR-API» с чекбоксом, но это форма заявления, а не материальное договорное условие о порядке подключения."
   260	        }
   261	      ]
   262	    },
   263	    {
   264	      "matrix_id": "2.6.2.2",
   265	      "requirement": "При отсутствии у Предприятия собственного ПО — доработка через Вендора; Банк передаёт параметры QR-кода Вендору через API; подключение по Приложениям №1 и №1.1.",
   266	      "source_evidence": "«при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора... Банк может передавать Вендору параметры формирования QR-кода...» (матрица 2.6.2.2)",
   267	      "status": "missing_in_contract",
   268	      "required_type": "mandatory",
   269	      "applicability": "applicable",
   270	      "risk_level": "medium",
   271	      "risk": "Контракт не содержит механизма QR-Вендор для случая отсутствия у Заказчика собственного ПО с поддержкой QR. Отсутствует норма о том, что Банк не дорабатывает ПО Предприятия, и что первая операция активирует услугу. Это создаёт неопределённость в распределении обязанностей по доработке ПО.",
   272	      "rejected_candidates": [
   273	        {
   274	          "contract_id": "Приложение_1.2_QR_Вендор",
   275	          "reason": "В форме Информации о ТСТ есть поле «QR-Вендор» с перечнем типов, но это форма заявления, а не материальное условие о порядке взаимодействия с Вендором."
   276	        }
   277	      ]
   278	    },
   279	    {
   280	      "matrix_id": "2.6.3.1",
   281	      "requirement": "QR-код на Электронных терминалах при подключении Вендором-Банком: QR-код подключается при установке Электронного терминала в ТСТ.",
   282	      "source_evidence": "«QR-код подключается при установке Электронного терминала в ТСТ» (матрица 2.6.3.1)",
   283	      "status": "missing_in_contract",
   284	      "required_type": "mandatory",
   285	      "applicability": "applicable",
   286	      "risk_level": "medium",
   287	      "risk": "Контракт предусматривает установку Электронных терминалов (п. 5.1.1) и возможность вывода QR-кода (Техническое задание), но не содержит нормы о том, что QR-код активируется автоматически при установке терминала, когда Вендором является Банк. Это создаёт неопределённость относительно необходимости отдельного заявления на активацию QR.",
   288	      "rejected_candidates": [
   289	        {
   290	          "contract_id": "5.1.1",
   291	          "reason": "Пункт 5.1.1 регулирует установку терминалов и инструктаж, но не упоминает активацию QR-кода."
   292	        }
   293	      ]
   294	    },
   295	    {
   296	      "matrix_id": "2.6.3.2",
   297	      "requirement": "Отключение QR-кода по инициативе Предприятия через обращение в Банк способами по п.2.3.1–2.3.4, 2.3.7.",
   298	      "source_evidence": "«отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора.» (матрица 2.6.3.2)",
   299	      "status": "missing_in_contract",
   300	      "required_type": "mandatory",
   301	      "applicability": "applicable",
   302	      "risk_level": "medium",
   303	      "risk": "Контракт не содержит процедуры отключения QR-кода. Отсутствие данной нормы означает, что у Заказчика нет договорного механизма для отключения QR-функциональности, что может привести к спорам или несанкционированному отключению.",
   304	      "rejected_candidates": []
   305	    }
   306	  ],
   307	  "unmatched_contract": [],
   308	  "coverage_ledger": {
   309	    "matrix": [
   310	      {"matrix_id": "2.1", "closure": "linked", "link_indices": [0], "reason": "Частичный аналог в п. 4.3; отклонение по праву отказа Банка и другим элементам."},
   311	      {"matrix_id": "2.2", "closure": "linked", "link_indices": [1], "reason": "Полный аналог в п. 5.1.8 и Приложении 1."},
   312	      {"matrix_id": "2.3.1", "closure": "linked", "link_indices": [2], "reason": "Дословный аналог в п. 2.3.1."},
   313	      {"matrix_id": "2.3.2", "closure": "linked", "link_indices": [3], "reason": "Дословный аналог в п. 2.3.2."},
   314	      {"matrix_id": "2.3.3", "closure": "linked", "link_indices": [4], "reason": "Дословный аналог в п. 2.3.3."},
   315	      {"matrix_id": "2.3.4", "closure": "linked", "link_indices": [5], "reason": "Дословный аналог в п. 2.3.4."},
   316	      {"matrix_id": "2.3.5", "closure": "linked", "link_indices": [6], "reason": "Аналог в п. 2.3.5; отклонение — незаполненное наименование системы."},
   317	      {"matrix_id": "2.3.6", "closure": "linked", "link_indices": [7], "reason": "Дословный аналог в п. 2.3.6."},
   318	      {"matrix_id": "2.3.7", "closure": "linked", "link_indices": [8], "reason": "Аналог в п. 2.3.7 и абзацах дат; отклонение — generic оператор ЭДО."},
   319	      {"matrix_id": "2.4", "closure": "linked", "link_indices": [9], "reason": "Частичный аналог в п. 1.1 и 8.3.2; отклонение — отсутствие общей нормы."},
   320	      {"matrix_id": "2.5.1.1", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: only_for_product=internet_acquiring; контракт — trade_acquiring."},
   321	      {"matrix_id": "2.5.2.1", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: payment_method=sber_pay_face_scan; биометрия не активирована."},
   322	      {"matrix_id": "2.6.1.1", "closure": "missing_in_contract", "link_indices": [], "reason": "Условно применимо (smart-терминалы упоминаются); нет нормы об автоактивации QR."},
   323	      {"matrix_id": "2.6.2.1", "closure": "missing_in_contract", "link_indices": [], "reason": "Применимо (QR в контракте); нет механизма QR-API."},
   324	      {"matrix_id": "2.6.2.2", "closure": "missing_in_contract", "link_indices": [], "reason": "Применимо (QR в контракте); нет механизма QR-Вендор."},
   325	      {"matrix_id": "2.6.3.1", "closure": "missing_in_contract", "link_indices": [], "reason": "Применимо (терминалы Банка); нет нормы об автоактивации QR при установке."},
   326	      {"matrix_id": "2.6.3.2", "closure": "missing_in_contract", "link_indices": [], "reason": "Применимо (QR в контракте); нет процедуры отключения QR."},
   327	      {"matrix_id": "2.7", "closure": "linked", "link_indices": [10], "reason": "Аналог в п. 12.4: контракт в электронной форме с УКЭП."}
   328	    ],
   329	    "contract": [
   330	      {"contract_id": "4.3", "closure": "linked", "link_indices": [0], "reason": "Связан с матрицей 2.1 (регистрация ТСТ)."},
   331	      {"contract_id": "5.1.8", "closure": "linked", "link_indices": [1], "reason": "Связан с матрицей 2.2 (валюта расчётов)."},
   332	      {"contract_id": "Приложение_1_п5", "closure": "linked", "link_indices": [1], "reason": "Связан с матрицей 2.2 (валюта расчётов, контекст)."},
   333	      {"contract_id": "2.3.1", "closure": "linked", "link_indices": [2], "reason": "Связан с матрицей 2.3.1 (email-канал)."},
   334	      {"contract_id": "2.3.2", "closure": "linked", "link_indices": [3], "reason": "Связан с матрицей 2.3.2 (ДБО-канал)."},
   335	      {"contract_id": "2.3.3", "closure": "linked", "link_indices": [4], "reason": "Связан с матрицей 2.3.3 (нарочный/курьер)."},
   336	      {"contract_id": "2.3.4", "closure": "linked", "link_indices": [5], "reason": "Связан с матрицей 2.3.4 (заказное письмо)."},
   337	      {"contract_id": "2.3.5", "closure": "linked", "link_indices": [6], "reason": "Связан с матрицей 2.3.5 (ЭДО с УКЭП)."},
   338	      {"contract_id": "2.3.6", "closure": "linked", "link_indices": [7], "reason": "Связан с матрицей 2.3.6 (ЕИС/ЭТП)."},
   339	      {"contract_id": "2.3.7", "closure": "linked", "link_indices": [8], "reason": "Связан с матрицей 2.3.7 (даты получения)."},
   340	      {"contract_id": "2.3_receipt_dates", "closure": "linked", "link_indices": [8], "reason": "Связан с матрицей 2.3.7 (правила дат)."},
   341	      {"contract_id": "1.1", "closure": "linked", "link_indices": [9], "reason": "Связан с матрицей 2.4 (неотъемлемость приложений)."},
   342	      {"contract_id": "8.3.2", "closure": "linked", "link_indices": [9], "reason": "Связан с матрицей 2.4 (неотъемлемость, контекст)."},
   343	      {"contract_id": "12.4", "closure": "linked", "link_indices": [10], "reason": "Связан с матрицей 2.7 (электронная форма)."}
   344	    ]
   345	  },
   346	  "summary": {
   347	    "aligned_count": 7,
   348	    "deviation_count": 4,
   349	    "missing_in_contract_count": 7,
   350	    "extra_in_contract_count": 0,
   351	    "aligned_matrix_ids": ["2.2", "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.6", "2.7"],
   352	    "deviation_matrix_ids": ["2.1", "2.3.5", "2.3.7", "2.4"],
   353	    "missing_matrix_ids": ["2.5.1.1", "2.5.2.1", "2.6.1.1", "2.6.2.1", "2.6.2.2", "2.6.3.1", "2.6.3.2"]
   354	  }
   355	}
Tool:    201	        "4.2.2"
   202	      ],
   203	      "contract_ids": [
   204	        "5.1.1",
   205	        "5.3.10"
   206	      ],
   207	      "relationship": "deviation",
   208	      "legal_topic": "Обязанность Предприятия соблюдать положения Договора и инструктивные материалы Банка",
   209	      "matrix_standard": "Предприятие обязуется соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/инструктивных материалах, предоставляемых Банком.",
   210	      "contract_position": "Исполнитель обязуется провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком (п.5.1.1). Заказчик обязуется проводить операции и оформлять документы по операциям в ТСТ к контракту (п.5.3.10).",
   211	      "matrix_evidence": "Предприятие обязуется: Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/инструктивных материалах, предоставляемых Банком",
   212	      "contract_evidence": "Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком (п.5.1.1); Проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту (п.5.3.10)",
   213	      "status_reason": "Контракт не содержит прямой формулировки об обязанности Заказчика соблюдать положения Договора и выполнять требования инструктивных материалов. П.5.1.1 говорит об инструктаже (обязанность Исполнителя), а не об обязанности Заказчика соблюдать. П.5.3.10 касается только проведения операций. Отсутствует общая норма о соблюдении всех инструктивных материалов Банка.",
   214	      "risk_level": "medium",
   215	      "discrepancies": [
   216	        {
   217	          "type": "obligation",
   218	          "description": "Отсутствует прямая обязанность Заказчика соблюдать положения Договора и выполнять требования инструктивных материалов Банка. Инструктаж упомянут как обязанность Исполнителя, а не Заказчика",
   219	          "risk": "Средний риск: без явной обязанности соблюдать инструктивные материалы Банка, Заказчик может оспаривать применимость инструкций, не включенных прямо в контракт"
   220	        }
   221	      ]
   222	    },
   223	    {
   224	      "matrix_ids": [
   225	        "4.2.3"
   226	      ],
   227	      "contract_ids": [],
   228	      "relationship": "missing_in_contract",
   229	      "legal_topic": "Обязанность Предприятия самостоятельно знакомиться с изменениями документов Банка",
   230	      "matrix_standard": "Предприятие обязуется самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление не является основанием для неприменения изменений.",
   231	      "contract_position": "Аналог отсутствует. Контракт 44-ФЗ не содержит механизма одностороннего изменения условий через сайт Банка.",
   232	      "matrix_evidence": "Предприятие обязуется: Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка",
   233	      "contract_evidence": "",
   234	      "status_reason": "В контракте отсутствует обязанность Заказчика отслеживать изменения документов на сайте Банка. Более того, п.11.8 прямо запрещает изменение существенных условий контракта, а п.11.2 требует оформления изменений в письменном виде и подписания обеими Сторонами. Механизм одностороннего изменения через сайт несовместим с 44-ФЗ.",
   235	      "risk_level": "low",
   236	      "discrepancies": []
   237	    },
   238	    {
   239	      "matrix_ids": [
   240	        "4.2.4"
   241	      ],
   242	      "contract_ids": [
   243	        "5.3.7",
   244	        "5.1.7"
   245	      ],
   246	      "relationship": "aligned",
   247	      "legal_topic": "Обязанность Предприятия размещать информационные материалы Банка",
   248	      "matrix_standard": "Предприятие обязуется размещать на видных местах ТСТ предоставляемые Банком информационные материалы, извещающие о возможности оплаты с использованием Карт/NFC-карт/SberPay/Плати QR.",
   249	      "contract_position": "Заказчик обязуется размещать на видных местах ТСТ предоставляемые исполнителем рекламно-информационные материалы, извещающие покупателей о возможности оплаты услуг с использованием карт (п.5.3.7). Исполнитель обязуется обеспечивать электронные терминалы рекламно-информационными материалами (п.5.1.7).",
   250	      "matrix_evidence": "Предприятие обязуется: Размещать на видных местах ТСТ, предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с использованием Карт/NFC-карт/SberPay/Плати QR",
   251	      "contract_evidence": "Размещать на видных местах ТСТ, предоставляемые исполнителем рекламно-информационные материалы, извещающие покупателей о возможности оплаты услуг с использованием карт (п.5.3.7)",
   252	      "status_reason": "Прямой аналог: обязанность Заказчика размещать информационные материалы Исполнителя о возможности оплаты картами. Отсутствие упоминания NFC-карт, SberPay, Плати QR не является отклонением — это slash-альтернативы, и контракт фокусируется на картах. Обязанность Исполнителя предоставлять материалы закреплена в п.5.1.7.",
   253	      "risk_level": "none",
   254	      "discrepancies": []
   255	    },
   256	    {
   257	      "matrix_ids": [
   258	        "4.2.5"
   259	      ],
   260	      "contract_ids": [
   261	        "Приложение №1 п.3"
   262	      ],
   263	      "relationship": "deviation",
   264	      "legal_topic": "Обязанность принимать все карты, не выдавать наличные, не принимать более 2 карт",
   265	      "matrix_standard": "Предприятие обязуется принимать все Карты из перечня в течение всего рабочего времени, не выдавать наличные по Картам, не принимать от Покупателя более 2 различных Карт.",
   266	      "contract_position": "Перечень карт: МИР, VISA, MasterCard (Приложение №1 п.3). Обязанность принимать все перечисленные карты и ограничения (наличные, более 2 карт) прямо не закреплены.",
   267	      "matrix_evidence": "Принимать в оплату Товаров/услуг все Карты, перечисленные в Порядке проведения операций, в течение всего рабочего времени. Не выдавать по Картам наличные денежные средства. Не принимать от Покупателя более 2 (двух) различных Карт",
   268	      "contract_evidence": "Перечень карт: НСПК МИР, VISA International, MasterCard (Приложение №1 п.3)",
   269	      "status_reason": "Контракт содержит перечень принимаемых карт (МИР, VISA, MasterCard), но отсутствуют три ключевых операционных ограничения: (1) обязанность принимать все карты в течение всего рабочего времени; (2) запрет выдачи наличных по картам; (3) запрет приема более 2 различных карт от одного покупателя. Это существенные операционные пробелы.",
   270	      "risk_level": "medium",
   271	      "discrepancies": [
   272	        {
   273	          "type": "obligation",
   274	          "description": "Отсутствует обязанность принимать все карты из перечня в течение всего рабочего времени",
   275	          "risk": "Заказчик может выборочно принимать карты или ограничивать время приема, что снижает объем операций"
   276	        },
   277	        {
   278	          "type": "obligation",
   279	          "description": "Отсутствует запрет выдачи наличных денежных средств по картам",
   280	          "risk": "Риск использования терминала для выдачи наличных, что может быть квалифицировано как обналичивание"
   281	        },
   282	        {
   283	          "type": "obligation",
   284	          "description": "Отсутствует запрет приема более 2 различных карт от одного покупателя",
   285	          "risk": "Риск дробления платежей и мошеннических операций"
   286	        }
   287	      ]
   288	    },
   289	    {
   290	      "matrix_ids": [
   291	        "4.2.6"
   292	      ],
   293	      "contract_ids": [
   294	        "5.3.8"
   295	      ],
   296	      "relationship": "aligned",
   297	      "legal_topic": "Запрет разбивать сумму одной операции на несколько",
   298	      "matrix_standard": "Предприятие обязуется не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм.",
   299	      "contract_position": "Заказчик обязуется не разбивать сумму одной операции оплаты на несколько сумм и не проводить отдельные операции на каждую из этих сумм (п.5.3.8).",
   300	      "matrix_evidence": "Не разбивать сумму одной Операции оплаты на несколько сумм и не проводить отдельные Операции на каждую из этих сумм",
   301	      "contract_evidence": "Не разбивать сумму одной операции оплаты на несколько сумм и не проводить отдельные операции на каждую из этих сумм (п.5.3.8)",
   302	      "status_reason": "Прямой текстуальный аналог: формулировка контракта практически дословно воспроизводит матричное требование.",
   303	      "risk_level": "none",
   304	      "discrepancies": []
   305	    },
   306	    {
   307	      "matrix_ids": [
   308	        "4.2.7"
   309	      ],
   310	      "contract_ids": [
   311	        "5.3.9"
   312	      ],
   313	      "relationship": "aligned",
   314	      "legal_topic": "Запрет использования реквизитов карты для иных целей",
   315	      "matrix_standard": "Предприятие обязуется не использовать реквизиты Карты/Платежного счета, которые стали доступны Предприятию/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупателя.",
   316	      "contract_position": "Заказчик обязуется не использовать реквизиты карты, которые стали доступны заказчику/ТСТ, для иных целей, кроме как проведение операций в присутствии или по распоряжению покупателя (п.5.3.9).",
   317	      "matrix_evidence": "Не использовать реквизиты Карты/Платежного счета, которые стали доступны Предприятию/ТСТ, для иных целей, кроме как проведение Операций в присутствии или по распоряжению Покупателя",
   318	      "contract_evidence": "Не использовать реквизиты карты, которые стали доступны заказчику/ТСТ, для иных целей, кроме как проведение операций в присутствии или по распоряжению покупателя (п.5.3.9)",
   319	      "status_reason": "Прямой текстуальный аналог: формулировка контракта практически дословно воспроизводит матричное требование. Отсутствие упоминания Платежного счета несущественно.",
   320	      "risk_level": "none",
   321	      "discrepancies": []
   322	    },
   323	    {
   324	      "matrix_ids": [
   325	        "4.2.8"
   326	      ],
   327	      "contract_ids": [],
   328	      "relationship": "missing_in_contract",
   329	      "legal_topic": "Цены при оплате картами не выше цен при наличном расчете",
   330	      "matrix_standard": "Предприятие обязуется предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства.",
   331	      "contract_position": "Аналог отсутствует. Контракт не содержит положений о соотношении цен при оплате картами и наличными.",
   332	      "matrix_evidence": "Предоставлять Покупателям полный набор Товаров/услуг по ценам, не превышающим цены Предприятия при расчетах за наличные денежные средства",
   333	      "contract_evidence": "",
   334	      "status_reason": "В контракте отсутствует обязанность Заказчика не завышать цены при оплате картами по сравнению с наличными. Это стандартное требование эквайринга, защищающее интересы платежных систем и Банка.",
   335	      "risk_level": "medium",
   336	      "discrepancies": []
   337	    },
   338	    {
   339	      "matrix_ids": [
   340	        "4.2.9"
   341	      ],
   342	      "contract_ids": [
   343	        "5.3.10"
   344	      ],
   345	      "relationship": "aligned",
   346	      "legal_topic": "Обязанность проводить операции по Порядку и нести ответственность за информацию в документах",
   347	      "matrix_standard": "Предприятие обязуется проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций и нести ответственность за правильность указанной в документах информации.",
   348	      "contract_position": "Заказчик обязуется проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту и нести ответственность за правильность указанной в документах информации (п.5.3.10).",
   349	      "matrix_evidence": "Проводить Операции и оформлять Документы по операциям в соответствии с Порядком проведения операций в Торгово-сервисных точках к Договору и нести ответственность за правильность указанной в документах информации",
   350	      "contract_evidence": "Проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту и нести ответственность за правильность указанной в документах информации (п.5.3.10)",
   351	      "status_reason": "Прямой аналог: формулировка контракта воспроизводит матричное требование. Отсутствие явной ссылки на Порядок проведения операций компенсируется ссылкой на контракт в целом, который включает Техническое задание с детальным порядком.",
   352	      "risk_level": "none",
   353	      "discrepancies": []
   354	    },
   355	    {
   356	      "matrix_ids": [
   357	        "4.2.10"
   358	      ],
   359	      "contract_ids": [
   360	        "5.3.11"
   361	      ],
   362	      "relationship": "aligned",
   363	      "legal_topic": "Хранение документов по операциям и передача копий Банку",
   364	      "matrix_standard": "Хранить документы по операциям не менее 13 месяцев с даты совершения Операции и передавать копии Банку по запросу в течение 3 рабочих дней. Документы должны быть надлежащего качества.",
   365	      "contract_position": "Заказчик обязуется хранить документы по операциям не менее тринадцати месяцев с даты совершения операции и передавать их копии надлежащего качества исполнителю по его запросу в течение трех рабочих дней с даты получения запроса (п.5.3.11).",
   366	      "matrix_evidence": "Хранить в недоступном для третьих лиц месте Документы по операциям... не менее 13 (тринадцати) месяцев с даты совершения Операции и передавать их копии в Банк по его запросу... в течение 3 (трех) рабочих дней",
   367	      "contract_evidence": "Хранить в недоступном для третьих лиц месте документы по операциям... не менее тринадцати месяцев с даты совершения операции и передавать их копии надлежащего качества... исполнителю по его запросу в течение трех рабочих дней (п.5.3.11)",
   368	      "status_reason": "Прямой текстуальный аналог: срок хранения (13 месяцев), срок передачи копий (3 рабочих дня), требование к качеству — все элементы сохранены. Перечень документов в контракте несколько уже (чеки, кассовые чеки, распоряжения покупателя, документы о передаче товара/услуги, контрольные ленты), но охватывает основные категории.",
   369	      "risk_level": "none",
   370	      "discrepancies": []
   371	    },
   372	    {
   373	      "matrix_ids": [
   374	        "4.2.11"
   375	      ],
   376	      "contract_ids": [
   377	        "5.3.12",
   378	        "5.5"
   379	      ],
   380	      "relationship": "aligned",
   381	      "legal_topic": "Обязанность передавать заявление об обстоятельствах операции по запросу Банка",
   382	      "matrix_standard": "Передавать в Банк по запросу в течение 3 рабочих дней письменное заявление с изложением обстоятельств проведения Операции. В случае утраты документов — немедленно сообщить.",
   383	      "contract_position": "Заказчик обязуется передавать исполнителю по запросу в течение трех рабочих дней письменное заявление с изложением обстоятельств проведения операции в ТСТ. В случае утраты документов — немедленно сообщить (п.5.3.12). Дублируется в п.5.5.",
   384	      "matrix_evidence": "Передавать в Банк по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Банка письменное заявление с изложением обстоятельств проведения Операции",
   385	      "contract_evidence": "Передавать исполнителю по его запросу в течение трех рабочих дней с даты получения запроса от исполнителя письменное заявление с изложением обстоятельств проведения операции в ТСТ (п.5.3.12)",
   386	      "status_reason": "Прямой текстуальный аналог: срок (3 рабочих дня), содержание (письменное заявление об обстоятельствах), обязанность немедленного сообщения об утрате — все элементы сохранены.",
   387	      "risk_level": "none",
   388	      "discrepancies": []
   389	    },
   390	    {
   391	      "matrix_ids": [
   392	        "4.2.12"
   393	      ],
   394	      "contract_ids": [
   395	        "8.3.1",
   396	        "8.5.1",
   397	        "8.5.7"
   398	      ],
   399	      "relationship": "deviation",
   400	      "legal_topic": "Обязанность акцептовать платежные требования и счета Банка",
   401	      "matrix_standard": "Предприятие обязуется акцептовать платежные требования и счета на оплату, выставленные Банком, в течение 5 рабочих дней с даты их выставления.",
   402	      "contract_position": "Приемка через ЕИС: Заказчик подписывает документ о приемке в течение 10 рабочих дней (п.8.5.1, п.8.5.7). Исполнитель формирует документ о приемке ежемесячно не позднее 10 рабочего дня следующего месяца (п.8.3.1).",
   403	      "matrix_evidence": "Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, в течение 5 (пяти) рабочих дней",
   404	      "contract_evidence": "Заказчик в срок не более 10 (десяти) рабочих дней со дня поступления документа о приемке... подписывает усиленной электронной подписью... документ о приемке (п.8.5.1)",
   405	      "status_reason": "Контракт 44-ФЗ заменяет механизм акцепта платежных требований на процедуру приемки через ЕИС. Срок увеличен с 5 до 10 рабочих дней. Это стандартное отклонение для госконтрактов, где приемка формализована через ЕИС.",
   406	      "risk_level": "low",
   407	      "discrepancies": [
   408	        {
   409	          "type": "procedure",
   410	          "description": "Акцепт платежных требований заменен на подписание документа о приемке через ЕИС",
   411	          "risk": "Низкий риск: механизм ЕИС является стандартным для 44-ФЗ и обеспечивает юридическую значимость приемки"
   412	        },
   413	        {
   414	          "type": "deadline",
   415	          "description": "Срок увеличен с 5 до 10 рабочих дней",
   416	          "risk": "Незначительное увеличение срока, стандартное для 44-ФЗ"
   417	        }
   418	      ]
   419	    },
   420	    {
   421	      "matrix_ids": [
   422	        "4.2.13"
   423	      ],
   424	      "contract_ids": [
   425	        "5.3.19"
   426	      ],
   427	      "relationship": "aligned",
   428	      "legal_topic": "Обязанность возместить Банку все суммы и убытки",
   429	      "matrix_standard": "Возместить Банку в полном объеме и в безусловном порядке: средства, списанные в пользу Банка-эмитента по спорным/недействительным операциям; сборы и комиссии по спорам; убытки от штрафных санкций и ответственности.",
   430	      "contract_position": "Заказчик обязуется возместить Исполнителю в полном объеме и в безусловном порядке денежные средства по тем же категориям: списанные средства, сборы/комиссии по спорам, убытки от штрафных санкций (п.5.3.19).",
   431	      "matrix_evidence": "Возместить Банку в полном объеме и в безусловном порядке денежные средства в размере: средств, которые... были списаны со счета Банка в пользу Банка-эмитента...; средств... в связи с рассмотрением споров...; убытков, возникших у Банка в результате применения... штрафных санкций",
   432	      "contract_evidence": "Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере: средств, которые... были списаны со счета Исполнителя в пользу Банка-эмитента...; средств... в связи с рассмотрением споров...; убытков, возникших у Исполнителя в результате применения... штрафных санкций (п.5.3.19)",
   433	      "status_reason": "Прямой текстуальный аналог: все три категории возмещения (списанные средства, сборы по спорам, убытки от штрафов) сохранены. Формулировка «в полном объеме и в безусловном порядке» идентична. Перечень оснований практически дословно совпадает.",
   434	      "risk_level": "none",
   435	      "discrepancies": []
   436	    },
   437	    {
   438	      "matrix_ids": [
   439	        "4.2.14"
   440	      ],
   441	      "contract_ids": [
   442	        "5.3.13"
   443	      ],
   444	      "relationship": "aligned",
   445	      "legal_topic": "Обязанность информировать Банк об изменениях в документах и статусе",
   446	      "matrix_standard": "При реорганизации, изменении документов, банкротстве, смене руководства, изменении адреса/реквизитов — информировать Банк и передать заверенные документы не позднее 3 рабочих дней.",
   447	      "contract_position": "Заказчик обязуется информировать исполнителя и передать надлежаще заверенные документы при реорганизации, изменении документов, банкротстве, смене руководства, изменении адреса/реквизитов не позднее 3 рабочих дней (п.5.3.13).",
   448	      "matrix_evidence": "В случае реорганизации, внесения изменений и дополнений в документы... при открытии/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса... реквизитов... обязуется информировать Банк и передать... документы... не позднее 3 (трех) рабочих дней",
   449	      "contract_evidence": "В случае реорганизации, внесения изменений и дополнений в документы... при открытии/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса... реквизитов... обязуется информировать исполнителя и передать... документы... не позднее трех рабочих дней (п.5.3.13)",
   450	      "status_reason": "Прямой текстуальный аналог: перечень событий и срок (3 рабочих дня) идентичны матрице.",
   451	      "risk_level": "none",
   452	      "discrepancies": []
   453	    },
   454	    {
   455	      "matrix_ids": [
   456	        "4.2.15"
   457	      ],
   458	      "contract_ids": [
   459	        "5.3.14"
   460	      ],
   461	      "relationship": "aligned",
   462	      "legal_topic": "Обязанность предоставлять достоверные сведения и обновлять их",
   463	      "matrix_standard": "Предоставлять достоверные документы и сведения, обновлять не реже одного раза в год, а также по запросу Банка в течение 7 рабочих дней, включая сведения о деятельности, финансовом положении, деловой репутации, представителях, выгодоприобретателях, бенефициарах.",
   464	      "contract_position": "Заказчик обязуется предоставлять исполнителю достоверные документы и сведения, обновлять не реже одного раза в год, а также по запросу в течение 7 рабочих дней, включая сведения о деятельности, финансовом положении, деловой репутации, представителях, выгодоприобретателях, бенефициарах (п.5.3.14).",
   465	      "matrix_evidence": "Предоставлять в Банк достоверные документы и сведения... не реже одного раза в год, а также по отдельному запросу Банка в течение 7 (семи) рабочих дней... включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации... представителях, выгодоприобретателях и бенефициарных владельцах",
   466	      "contract_evidence": "Предоставлять исполнителю достоверные документы и сведения... не реже одного раза в год, а также по отдельному запросу исполнителя в течение семи рабочих дней... включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации... представителях, выгодоприобретателях и бенефициарных владельцах (п.5.3.14)",
   467	      "status_reason": "Прямой текстуальный аналог: периодичность (раз в год), срок по запросу (7 рабочих дней), состав сведений — все элементы идентичны матрице.",
   468	      "risk_level": "none",
   469	      "discrepancies": []
   470	    },
   471	    {
   472	      "matrix_ids": [
   473	        "4.2.16.1"
   474	      ],
   475	      "contract_ids": [
   476	        "5.3.20"
   477	      ],
   478	      "relationship": "deviation",
   479	      "legal_topic": "Передача персональных данных руководителя Предприятия",
   480	      "matrix_standard": "Предприятие гарантирует наличие правовых оснований на передачу ПДн руководителя (ФИО, адрес, паспортные данные), в том числе в Платежную систему МИР. Обязано уведомить Банк о прекращении правовых оснований.",
   481	      "contract_position": "Заказчик передает Исполнителю ПДн руководителя (ФИО, адрес, паспортные данные). Заказчик гарантирует наличие правовых оснований, в том числе на передачу в Платежную систему МИР (п.5.3.20).",
   482	      "matrix_evidence": "Предприятие гарантирует наличие правовых оснований на передачу в Банк персональных данных руководителя Предприятия, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные... Предприятие обязано уведомить Банк о прекращении правовых оснований",
   483	      "contract_evidence": "Заказчик передает Исполнителю персональные данные руководителя Заказчика, состав которых включает: ФИО, адрес, паспортные данные. Заказчик гарантирует наличие правовых оснований на передачу Исполнителю персональных данных руководителя Заказчика, в том числе на передачу в Платежную систему МИР (п.5.3.20)",
   484	      "status_reason": "Контракт содержит аналог с составом ПДн (ФИО, адрес, паспортные данные) и гарантией правовых оснований. Однако обязанность уведомления о прекращении правовых оснований вынесена в отдельный пункт 5.3.15 (частично). Кроме того, в контракте отсутствует указание на то, что ПДн передаются в целях, указанных в п.5.1.7 Договора (матрица ссылается на этот пункт для целей обработки).",
   485	      "risk_level": "low",
   486	      "discrepancies": [
   487	        {
   488	          "type": "obligation",
   489	          "description": "Обязанность уведомления о прекращении правовых оснований на обработку ПДн руководителя вынесена в п.5.3.15 в формулировке об отзыве согласия, а не о прекращении правовых оснований",
   490	          "risk": "Низкий риск: механизм уведомления присутствует, хотя и в другой формулировке"
   491	        }
   492	      ]
   493	    },
   494	    {
   495	      "matrix_ids": [
   496	        "4.2.16.2"
   497	      ],
   498	      "contract_ids": [],
   499	      "relationship": "missing_in_contract",
   500	      "legal_topic": "Передача персональных данных сотрудников Предприятия (кроме руководителя)",
AI: Now let me check the batch 3 and 4 outputs for unmatched_contract items, and also look at the full contract text for sections I haven't seen yet:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_3_output.json', 'offset': 200, 'limit': 400}, 'id': 'call_00_SnhoWefTWMQbpttvGK2s0300', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_4_output.json', 'offset': 200, 'limit': 400}, 'id': 'call_01_Rp4fjJKp8LHISuMfirQG9711', 'type': 'tool_call'}]
Tool:    201	      ],
   202	      "contract_ids": [
   203	        "Приложение_№1_п5"
   204	      ],
   205	      "relationship": "deviation",
   206	      "legal_topic": "Обязанность предоставлять QR-код для SberPayQR/Плати QR",
   207	      "matrix_standard": "Предприятие обязуется предоставить Покупателю для считывания QR-код с целью осуществления оплаты Товаров/услуг с использованием SberPayQR/Плати QR.",
   208	      "contract_position": "Приложение №1 п.5: Терминалы Исполнителя должны иметь возможность вывода QR-кода для безналичной оплаты на дисплей терминала.",
   209	      "matrix_evidence": "«Предприятие обязуется: → Предоставить Покупателю для считывания QR-код с целью осуществления оплаты Товаров/услуг с использованием SberPayQR/Плати QR.» (матрица 4.2.22)",
   210	      "contract_evidence": "«Возможность вывода QR-кода для безналичной оплаты на дисплей терминала» (Приложение №1, п. 5)",
   211	      "status_reason": "Контракт упоминает QR-код как техническую характеристику терминала, но не содержит явной обязанности Заказчика предоставлять QR-код покупателю. Отсутствует указание на конкретные платежные сервисы SberPayQR/Плати QR. Матричный пункт имеет required_type=optional и payment_method=qr. QR включен в профиль контракта, поэтому требование применимо, но реализовано в ослабленной форме.",
   212	      "risk_level": "low",
   213	      "discrepancies": [
   214	        {
   215	          "type": "obligation",
   216	          "description": "Отсутствует прямая обязанность Заказчика предоставлять QR-код покупателю. QR-код упомянут только как техническая возможность терминала, а не как обязанность Предприятия.",
   217	          "risk": "Низкий риск: пункт матрицы имеет required_type=optional. Техническая возможность вывода QR-кода заложена в характеристиках терминала."
   218	        }
   219	      ]
   220	    },
   221	    {
   222	      "matrix_ids": [
   223	        "5.1.1.1"
   224	      ],
   225	      "contract_ids": [
   226	        "5.2.10.1"
   227	      ],
   228	      "relationship": "aligned",
   229	      "legal_topic": "Право Банка удерживать суммы недействительных операций",
   230	      "matrix_standard": "Банк имеет право удерживать суммы Операций, являющихся недействительными, в 12 перечисленных случаях (нарушение договора/законодательства/правил ПС, поддельная карта, неполный документ, несоответствие экземпляров, отсутствие подписи, непредоставление документов по запросу, возврат товара без возврата средств, двойная оплата, отсутствие кода авторизации, разбивка суммы, мошенничество, ручной ввод без согласования).",
   231	      "contract_position": "Пункт 5.2.10.1: Исполнитель удерживает суммы Операций, являющихся недействительными, с перечислением 12 аналогичных случаев.",
   232	      "matrix_evidence": "«Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций, являющихся недействительными, в следующих случаях: 1)...12)...» (матрица 5.1.1.1)",
   233	      "contract_evidence": "«Удерживать из сумм, подлежащих перечислению Заказчику по Контракту, следующие суммы: 5.2.10.1 Суммы Операций, являющихся недействительными, в следующих случаях:...» (п. 5.2.10.1 Контракта)",
   234	      "status_reason": "Прямой аналог: все 12 оснований для удержания недействительных операций сохранены в контракте. Перечень практически идентичен матричному. Право Банка на удержание полностью сохранено.",
   235	      "risk_level": "none",
   236	      "discrepancies": []
   237	    },
   238	    {
   239	      "matrix_ids": [
   240	        "5.1.1.2"
   241	      ],
   242	      "contract_ids": [
   243	        "5.2.10.2"
   244	      ],
   245	      "relationship": "aligned",
   246	      "legal_topic": "Право Банка удерживать ошибочно перечисленные суммы",
   247	      "matrix_standard": "Банк имеет право удерживать суммы, ошибочно перечисленные на счет Предприятия.",
   248	      "contract_position": "Пункт 5.2.10.2: Суммы, ошибочно перечисленные на счет Заказчика.",
   249	      "matrix_evidence": "«Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы, ошибочно перечисленные на счет Предприятия.» (матрица 5.1.1.2)",
   250	      "contract_evidence": "«5.2.10.2 Суммы, ошибочно перечисленные на счет Заказчика.» (п. 5.2.10.2 Контракта)",
   251	      "status_reason": "Прямой аналог: право Банка удерживать ошибочно перечисленные суммы полностью сохранено.",
   252	      "risk_level": "none",
   253	      "discrepancies": []
   254	    },
   255	    {
   256	      "matrix_ids": [
   257	        "5.1.1.3"
   258	      ],
   259	      "contract_ids": [
   260	        "5.2.10.3"
   261	      ],
   262	      "relationship": "aligned",
   263	      "legal_topic": "Право Банка удерживать суммы операций возврата, возврата платежа и реверсивных транзакций",
   264	      "matrix_standard": "Банк имеет право удерживать суммы Операций возврата, Возврата платежа и Реверсивные транзакции.",
   265	      "contract_position": "Пункт 5.2.10.3: Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.",
   266	      "matrix_evidence": "«Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.» (матрица 5.1.1.3)",
   267	      "contract_evidence": "«5.2.10.3 Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.» (п. 5.2.10.3 Контракта)",
   268	      "status_reason": "Прямой аналог: все три категории удерживаемых сумм (операции возврата, возврат платежа, реверсивные транзакции) полностью сохранены.",
   269	      "risk_level": "none",
   270	      "discrepancies": []
   271	    },
   272	    {
   273	      "matrix_ids": [
   274	        "5.1.1.4"
   275	      ],
   276	      "contract_ids": [
   277	        "5.2.10.4"
   278	      ],
   279	      "relationship": "deviation",
   280	      "legal_topic": "Право Банка удерживать суммы оспоренных операций",
   281	      "matrix_standard": "Банк имеет право удерживать суммы Операций, которые были оспорены и/или списаны со счета Банка Банком-эмитентом в соответствии с правилами Платежной системы по Операциям, проведенным в ТСТ, суммы оспоренных Операций, проведенных с использованием SberPay/Плати QR, а также суммы оспоренных Операций в отношении Товаров/услуг, реализуемых Предприятием как агентом.",
   282	      "contract_position": "Пункт 5.2.10.4: Исполнитель удерживает суммы операций, которые были оспорены и/или списаны со счета Исполнителя Банком-эмитентом в соответствии с правилами Платежных систем по операциям, проведенным в ТСТ, а также суммы оспоренных операций в отношении Товаров/услуг, реализуемых Заказчиком как агентом.",
   283	      "matrix_evidence": "«Банк имеет право: → Удерживать... суммы Операций, которые были оспорены и/или списаны со счета Банка Банком – эмитентом... суммы оспоренных Операций, проведенных с использованием SberPay/Плати QR, а также суммы оспоренных Операций в отношении Товаров/услуг, реализуемых Предприятием как агентом.» (матрица 5.1.1.4)",
   284	      "contract_evidence": "«5.2.10.4 Исполнитель удерживает из общих сумм... суммы операций, которые были оспорены и/или списаны со счета Исполнителя Банком – эмитентом в соответствии с правилами Платежных систем по операциям, проведенным в ТСТ, а также суммы оспоренных операций в отношении Товаров/услуг, реализуемых Заказчиком как агентом.» (п. 5.2.10.4 Контракта)",
   285	      "status_reason": "Аналог присутствует, но отсутствует упоминание SberPay/Плати QR в перечне оспоренных операций. Основные категории (оспоренные/списанные эмитентом, агентские операции) сохранены.",
   286	      "risk_level": "low",
   287	      "discrepancies": [
   288	        {
   289	          "type": "scope",
   290	          "description": "Отсутствует указание на удержание сумм оспоренных операций, проведенных с использованием SberPay/Плати QR.",
   291	          "risk": "Низкий риск: SberPay/Плати QR не является активированным продуктом в контракте. Основные категории оспоренных операций сохранены."
   292	        }
   293	      ]
   294	    },
   295	    {
   296	      "matrix_ids": [
   297	        "5.1.1.5"
   298	      ],
   299	      "contract_ids": [
   300	        "5.2.10.5"
   301	      ],
   302	      "relationship": "aligned",
   303	      "legal_topic": "Право Банка удерживать суммы штрафов и убытков, возникших по вине Предприятия",
   304	      "matrix_standard": "Банк имеет право удерживать суммы штрафов и иных убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности вследствие неисполнения или ненадлежащего исполнения Предприятием обязательств по Договору.",
   305	      "contract_position": "Пункт 5.2.10.5: Банк удерживает суммы штрафов и иных убытков, возникших у Исполнителя в результате применения к нему штрафных санкций в соответствии с правилами Платежных систем, а также привлечения Исполнителя к гражданской или административной ответственности вследствие неисполнения или ненадлежащего исполнения Заказчиком обязательств по Контракту.",
   306	      "matrix_evidence": "«Банк имеет право: → Удерживать... суммы штрафов и иных убытков, возникших у Банка в результате применения к нему штрафных санкций в соответствии с правилами Платежной системы, а также привлечения Банка к гражданской или административной ответственности...» (матрица 5.1.1.5)",
   307	      "contract_evidence": "«5.2.10.5 Банк удерживает из общих сумм... суммы штрафов и иных убытков, возникших у Исполнителя в результате применения к нему штрафных санкций в соответствии с правилами Платежных систем, а также привлечения Исполнителя к гражданской или административной ответственности...» (п. 5.2.10.5 Контракта)",
   308	      "status_reason": "Прямой аналог: право Банка удерживать штрафы и убытки, возникшие по вине Заказчика, полностью сохранено. Оба основания (штрафные санкции ПС и ответственность перед госорганами) присутствуют.",
   309	      "risk_level": "none",
   310	      "discrepancies": []
   311	    },
   312	    {
   313	      "matrix_ids": [
   314	        "5.1.3"
   315	      ],
   316	      "contract_ids": [
   317	        "Заявление_п1.3"
   318	      ],
   319	      "relationship": "deviation",
   320	      "legal_topic": "Право Банка на безакцептное списание при невозможности удержания",
   321	      "matrix_standard": "При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, списывать без дополнительного распоряжения Предприятия (на условиях заранее данного акцепта) денежные средства с расчетного счета Предприятия, открытого в Банке.",
   322	      "contract_position": "Заявление (Приложение): п. 1.3 — Предоставляет Банку согласие (заранее данный акцепт) на списание со счета без дополнительных распоряжений сумм, перечисленных в п.5.1.1 Контракта, при невозможности удержать указанные суммы из сумм, подлежащих последующему перечислению Предприятию.",
   323	      "matrix_evidence": "«При невозможности удержать суммы, указанные в п. 5.1.1 Договора... списывать без дополнительного распоряжения Предприятия (на условиях заранее данного акцепта, предоставленного Банку Предприятием в Заявлении...) денежные средства с расчетного счета Предприятия, открытого в Банке.» (матрица 5.1.3)",
   324	      "contract_evidence": "«Предоставляет Банку согласие (заранее данный акцепт) на списание со счета, указанного в настоящем Заявлении, без дополнительных распоряжений сумм, перечисленных в п.5.1.1 Контракта, при невозможности удержать указанные суммы из сумм, подлежащих последующему перечислению Предприятию.» (Заявление, п. 1.3)",
   325	      "status_reason": "Аналог присутствует в Заявлении (приложении к контракту), но с ограничением: списание возможно только со счета, открытого в Банке. В 44-ФЗ контракте счет Заказчика может быть открыт в Казначействе, а не в Банке, что делает механизм безакцептного списания практически нереализуемым для бюджетного учреждения.",
   326	      "risk_level": "medium",
   327	      "discrepancies": [
   328	        {
   329	          "type": "procedure",
   330	          "description": "Безакцептное списание ограничено счетом, открытым в Банке. Для бюджетного учреждения (44-ФЗ) счет typically открыт в Казначействе, что делает механизм нереализуемым на практике.",
   331	          "risk": "Средний риск: механизм прямого дебетования счета Заказчика может быть недоступен из-за особенностей казначейского обслуживания бюджетных учреждений."
   332	        }
   333	      ]
   334	    },
   335	    {
   336	      "matrix_ids": [
   337	        "5.1.6"
   338	      ],
   339	      "contract_ids": [
   340	        "5.2.3",
   341	        "5.2.4"
   342	      ],
   343	      "relationship": "aligned",
   344	      "legal_topic": "Право Банка проверять техническое состояние терминалов, заменять и обновлять ПО",
   345	      "matrix_standard": "Банк имеет право осуществлять проверку технического состояния и порядка эксплуатации терминалов, производить замену и обновлять ПО с уведомлением за 2 рабочих дня. Допускается удаленное обновление ПО без уведомления, если оно не затрагивает порядок проведения Операций.",
   346	      "contract_position": "Пункт 5.2.3: Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов, производить замену и обновлять ПО с уведомлением за 2 рабочих дня. Пункт 5.2.4: Допускается удаленное обновление ПО, не затрагивающее порядок проведения операций.",
   347	      "matrix_evidence": "«Банк имеет право: → Осуществлять проверку технического состояния и порядка эксплуатации Электронных терминалов/Смарт-терминалов Банка... Производить замену... обновлять программное обеспечение... уведомив Предприятие не менее чем за 2 (два) рабочих дня... Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения Операций... без предварительного уведомления.» (матрица 5.1.6)",
   348	      "contract_evidence": "«Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов... Производить замену электронных терминалов, а также обновлять программное обеспечение электронного терминала, уведомив заказчика не менее чем за два рабочих дня» (п. 5.2.3); «Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций» (п. 5.2.4)",
   349	      "status_reason": "Прямой аналог: все элементы права Банка (проверка, замена, обновление ПО с уведомлением за 2 рабочих дня, удаленное обновление без уведомления) полностью сохранены. Отсутствие упоминания Смарт-терминалов несущественно для pos-профиля.",
   350	      "risk_level": "none",
   351	      "discrepancies": []
   352	    },
   353	    {
   354	      "matrix_ids": [
   355	        "5.1.7"
   356	      ],
   357	      "contract_ids": [
   358	        "5.3.20"
   359	      ],
   360	      "relationship": "deviation",
   361	      "legal_topic": "Право Банка передавать информацию о Предприятии в Платежную систему МИР",
   362	      "matrix_standard": "Банк имеет право независимо от срока действия Договора передавать информацию о Предприятии/ТСТ/Ресурсе (включая персональные данные) в Платежную систему МИР при выявлении подозрительных/мошеннических операций. При расторжении по причине мошенничества — сообщать даты, причины и иные сведения.",
   363	      "contract_position": "Пункт 5.3.20: Заказчик передает Исполнителю персональные данные руководителя и гарантирует наличие правовых оснований на передачу в Платежную систему МИР. Однако это обязанность Заказчика, а не право Банка. Отсутствует активное право Банка на передачу информации о мошенничестве.",
   364	      "matrix_evidence": "«Банк имеет право: → Независимо от срока действия Договора в случае выявления подозрительных или мошеннических Операций передавать информацию... в Платежную систему МИР... В случае принятия Банком решения о расторжении Договора по причине мошеннической деятельности Предприятия сообщать в Платежную систему МИР: даты заключения и расторжения Договора, а также причины расторжения...» (матрица 5.1.7)",
   365	      "contract_evidence": "«Заказчик гарантирует наличие правовых оснований на передачу Исполнителю персональных данных руководителя Заказчика, в том числе на передачу в Платежную систему МИР» (п. 5.3.20 — только согласие на передачу ПДн, но не право Банка на передачу информации о мошенничестве).",
   366	      "status_reason": "Контракт содержит только пассивное согласие Заказчика на передачу ПДн в ПС МИР, но не содержит активного права Банка передавать информацию о подозрительных/мошеннических операциях и о расторжении договора по причине мошенничества. Это существенное сужение права Банка.",
   367	      "risk_level": "medium",
   368	      "discrepancies": [
   369	        {
   370	          "type": "right",
   371	          "description": "Отсутствует активное право Банка передавать информацию о подозрительных/мошеннических операциях в ПС МИР. Контракт содержит только согласие Заказчика на передачу ПДн, но не право Банка на информирование ПС о мошенничестве и расторжении.",
   372	          "risk": "Средний риск: ограничивает возможность Банка выполнять обязательства перед ПС МИР по информированию о мошеннических операциях."
   373	        }
   374	      ]
   375	    },
   376	    {
   377	      "matrix_ids": [
   378	        "5.1.8.1"
   379	      ],
   380	      "contract_ids": [
   381	        "5.2.9.1"
   382	      ],
   383	      "relationship": "aligned",
   384	      "legal_topic": "Право Банка прекратить Авторизацию/расторгнуть Договор при нарушении условий Предприятием",
   385	      "matrix_standard": "Банк вправе в одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при нарушении Предприятием условий Договора.",
   386	      "contract_position": "Пункт 5.2.9.1: нарушение Заказчиком условий Контракта.",
   387	      "matrix_evidence": "«Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → нарушение Предприятием условий Договора» (матрица 5.1.8.1)",
   388	      "contract_evidence": "«5.2.9.1. нарушение Заказчиком условий Контракта» (п. 5.2.9.1 Контракта)",
   389	      "status_reason": "Прямой аналог: основание для прекращения авторизации и расторжения — нарушение условий контракта — полностью сохранено.",
   390	      "risk_level": "none",
   391	      "discrepancies": []
   392	    },
   393	    {
   394	      "matrix_ids": [
   395	        "5.1.8.2"
   396	      ],
   397	      "contract_ids": [
   398	        "5.2.9.2"
   399	      ],
   400	      "relationship": "aligned",
   401	      "legal_topic": "Право Банка прекратить Авторизацию/расторгнуть Договор при внесении в перечень экстремистов/террористов",
   402	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при внесении данных Предприятия в перечень организаций и физических лиц, причастных к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения.",
   403	      "contract_position": "Пункт 5.2.9.2: внесение данных Заказчика в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения.",
   404	      "matrix_evidence": "«внесение данных Предприятия в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения» (матрица 5.1.8.2)",
   405	      "contract_evidence": "«5.2.9.2. внесение данных Заказчика в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения» (п. 5.2.9.2 Контракта)",
   406	      "status_reason": "Прямой аналог: основание полностью сохранено.",
   407	      "risk_level": "none",
   408	      "discrepancies": []
   409	    },
   410	    {
   411	      "matrix_ids": [
   412	        "5.1.8.3"
   413	      ],
   414	      "contract_ids": [
   415	        "5.2.9.3"
   416	      ],
   417	      "relationship": "aligned",
   418	      "legal_topic": "Право Банка прекратить Авторизацию при подозрении на отмывание доходов/финансирование терроризма",
   419	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при наличии подозрений, что Операции совершаются в целях легализации (отмывания) доходов или финансирования терроризма.",
   420	      "contract_position": "Пункт 5.2.9.3: при наличии у Исполнителя подозрений, что Операции в ТСТ совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма.",
   421	      "matrix_evidence": "«при наличии у Банка подозрений, что Операции в ТСТ/на Ресурсе совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма» (матрица 5.1.8.3)",
   422	      "contract_evidence": "«5.2.9.3. при наличии у Исполнителя подозрений, что Операции в ТСТ совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма» (п. 5.2.9.3 Контракта)",
   423	      "status_reason": "Прямой аналог: основание полностью сохранено.",
   424	      "risk_level": "none",
   425	      "discrepancies": []
   426	    },
   427	    {
   428	      "matrix_ids": [
   429	        "5.1.8.6"
   430	      ],
   431	      "contract_ids": [
   432	        "5.2.9.4"
   433	      ],
   434	      "relationship": "aligned",
   435	      "legal_topic": "Право Банка прекратить Авторизацию при получении негативной информации от госорганов/ПС",
   436	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при получении негативной информации о Предприятии/ТСТ/Ресурсе от органов государственной власти РФ и/или Платежной системы.",
   437	      "contract_position": "Пункт 5.2.9.4: получение негативной информации о Заказчике/ТСТ от органов государственной власти РФ и/или Платежных систем.",
   438	      "matrix_evidence": "«получение негативной информации о Предприятии/ТСТ/Ресурсе от органов государственной власти РФ и/или Платежной системы» (матрица 5.1.8.6)",
   439	      "contract_evidence": "«5.2.9.4. получение негативной информации о Заказчике/ТСТ от органов государственной власти РФ и/или Платежных систем» (п. 5.2.9.4 Контракта)",
   440	      "status_reason": "Прямой аналог: основание сохранено. Отсутствие упоминания Ресурса несущественно для trade_acquiring.",
   441	      "risk_level": "none",
   442	      "discrepancies": []
   443	    },
   444	    {
   445	      "matrix_ids": [
   446	        "5.1.8.7"
   447	      ],
   448	      "contract_ids": [
   449	        "5.2.9.5"
   450	      ],
   451	      "relationship": "aligned",
   452	      "legal_topic": "Право Банка прекратить Авторизацию при получении информации о мошенничестве",
   453	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при получении информации о мошенничестве в ТСТ/на Ресурсе. Достаточным подтверждением является информация от Банков-эмитентов или уведомления от Платежной системы, полученные по факсу или email.",
   454	      "contract_position": "Пункт 5.2.9.5: получение информации о мошенничестве в ТСТ; стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных систем, полученные с использованием факсимильной связи, по электронной почте (e-mail).",
   455	      "matrix_evidence": "«получение информации о мошенничестве в ТСТ/на Ресурсе; стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов в Банк, или уведомления от Платежной системы, полученные c использованием факсимильной связи, по электронной почте (e-mail)» (матрица 5.1.8.7)",
   456	      "contract_evidence": "«5.2.9.5. получение информации о мошенничестве в ТСТ; стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных систем, полученные c использованием факсимильной связи, по электронной почте (e-mail)» (п. 5.2.9.5 Контракта)",
   457	      "status_reason": "Прямой аналог: основание и стандарт доказывания (информация от банков-эмитентов или ПС по факсу/email) полностью сохранены.",
   458	      "risk_level": "none",
   459	      "discrepancies": []
   460	    },
   461	    {
   462	      "matrix_ids": [
   463	        "5.1.8.8"
   464	      ],
   465	      "contract_ids": [
   466	        "5.2.9.6"
   467	      ],
   468	      "relationship": "aligned",
   469	      "legal_topic": "Право Банка прекратить Авторизацию при ремонте помещений ТСТ",
   470	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при осуществлении ремонта помещений ТСТ, препятствующего осуществлению Операций.",
   471	      "contract_position": "Пункт 5.2.9.6: осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций.",
   472	      "matrix_evidence": "«осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций» (матрица 5.1.8.8)",
   473	      "contract_evidence": "«5.2.9.6. осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций» (п. 5.2.9.6 Контракта)",
   474	      "status_reason": "Прямой аналог: основание полностью сохранено. Матричный пункт имеет only_for_product=trade_acquiring — применим.",
   475	      "risk_level": "none",
   476	      "discrepancies": []
   477	    },
   478	    {
   479	      "matrix_ids": [
   480	        "5.1.8.9"
   481	      ],
   482	      "contract_ids": [
   483	        "5.2.9.7"
   484	      ],
   485	      "relationship": "aligned",
   486	      "legal_topic": "Право Банка прекратить Авторизацию при ликвидации/банкротстве Предприятия",
   487	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при ликвидации Предприятия либо возбуждении дела о банкротстве в соответствии с ФЗ № 127-ФЗ.",
   488	      "contract_position": "Пункт 5.2.9.7: ликвидация Заказчика либо возбуждение в отношении Заказчика дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)».",
   489	      "matrix_evidence": "«ликвидация Предприятия либо возбуждение в отношении Предприятия дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)»» (матрица 5.1.8.9)",
   490	      "contract_evidence": "«5.2.9.7. ликвидация Заказчика либо возбуждение в отношении Заказчика дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)»» (п. 5.2.9.7 Контракта)",
   491	      "status_reason": "Прямой аналог: основание полностью сохранено, включая ссылку на 127-ФЗ.",
   492	      "risk_level": "none",
   493	      "discrepancies": []
   494	    },
   495	    {
   496	      "matrix_ids": [
   497	        "5.1.8.10"
   498	      ],
   499	      "contract_ids": [
   500	        "5.2.9.8"
   501	      ],
   502	      "relationship": "aligned",
   503	      "legal_topic": "Право Банка прекратить Авторизацию при выявлении недостоверных сведений",
   504	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при выявлении недостоверных сведений о Предприятии/ТСТ, руководителе(-ях) в информации, указанной при заключении Договора.",
   505	      "contract_position": "Пункт 5.2.9.8: выявление недостоверных сведений о Заказчике/ТСТ, руководителе(-ях) в информации, указанной при заключении Контракта.",
   506	      "matrix_evidence": "«выявление недостоверных сведений о Предприятии/ТСТ, руководителе(-ях) в информации, указанной при заключении Договора» (матрица 5.1.8.10)",
   507	      "contract_evidence": "«5.2.9.8. выявление недостоверных сведений о Заказчике/ТСТ, руководителе(-ях) в информации, указанной при заключении Контракта» (п. 5.2.9.8 Контракта)",
   508	      "status_reason": "Прямой аналог: основание полностью сохранено.",
   509	      "risk_level": "none",
   510	      "discrepancies": []
   511	    },
   512	    {
   513	      "matrix_ids": [
   514	        "5.1.8.11"
   515	      ],
   516	      "contract_ids": [
   517	        "5.2.9.9"
   518	      ],
   519	      "relationship": "aligned",
   520	      "legal_topic": "Право Банка прекратить Авторизацию при несоответствии товаров/услуг роду деятельности",
   521	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при несоответствии предлагаемых Покупателям Товаров/услуг роду деятельности Предприятия, указанному в Информации о ТСТ.",
   522	      "contract_position": "Пункт 5.2.9.9: несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Заказчика, указанному в Информации о ТСТ.",
   523	      "matrix_evidence": "«несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Предприятия, указанному в Информации о ТСТ» (матрица 5.1.8.11)",
   524	      "contract_evidence": "«5.2.9.9. несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Заказчика, указанному в Информации о ТСТ» (п. 5.2.9.9 Контракта)",
   525	      "status_reason": "Прямой аналог: основание полностью сохранено.",
   526	      "risk_level": "none",
   527	      "discrepancies": []
   528	    },
   529	    {
   530	      "matrix_ids": [
   531	        "5.1.8.12"
   532	      ],
   533	      "contract_ids": [
   534	        "5.2.9.10"
   535	      ],
   536	      "relationship": "aligned",
   537	      "legal_topic": "Право Банка прекратить Авторизацию при отсутствии операций в течение 30 дней",
   538	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при отсутствии операций в течение 30 (тридцати) календарных дней подряд.",
   539	      "contract_position": "Пункт 5.2.9.10: отсутствие операций в течение 30 (тридцати) календарных дней подряд.",
   540	      "matrix_evidence": "«отсутствие операций в течение 30 (тридцати) календарных дней подряд» (матрица 5.1.8.12)",
   541	      "contract_evidence": "«5.2.9.10. отсутствие операций в течение 30 (тридцати) календарных дней подряд» (п. 5.2.9.10 Контракта)",
   542	      "status_reason": "Прямой аналог: основание и срок (30 календарных дней) полностью сохранены.",
   543	      "risk_level": "none",
   544	      "discrepancies": []
   545	    },
   546	    {
   547	      "matrix_ids": [
   548	        "5.1.8.13"
   549	      ],
   550	      "contract_ids": [
   551	        "5.2.9.11"
   552	      ],
   553	      "relationship": "aligned",
   554	      "legal_topic": "Право Банка прекратить Авторизацию при исчерпании Цены Договора или окончании срока",
   555	      "matrix_standard": "Банк вправе прекратить Авторизацию и/или расторгнуть Договор при исчерпании Цены Договора и/или окончании срока действия Договора, указанного в п. 10.1 Договора.",
   556	      "contract_position": "Пункт 5.2.9.11: исчерпание Цены Контракта и/или окончание срока действия Контракта.",
   557	      "matrix_evidence": "«исчерпание Цены Договора и/или окончание срока действия Договора, указанного в п. 10.1 Договора» (матрица 5.1.8.13)",
   558	      "contract_evidence": "«5.2.9.11. исчерпание Цены Контракта и/или окончание срока действия Контракта» (п. 5.2.9.11 Контракта)",
   559	      "status_reason": "Прямой аналог: оба основания (исчерпание цены и окончание срока) полностью сохранены. Отсутствие ссылки на конкретный пункт (п. 10.1) несущественно — срок действия указан в п. 11.1 контракта.",
   560	      "risk_level": "none",
   561	      "discrepancies": []
   562	    },
   563	    {
   564	      "matrix_ids": [
   565	        "5.1.11"
   566	      ],
   567	      "contract_ids": [
   568	        "5.2.5"
   569	      ],
   570	      "relationship": "deviation",
   571	      "legal_topic": "Право Банка запрашивать документы по операциям",
   572	      "matrix_standard": "Банк имеет право запрашивать Документы по операциям не позднее 13 месяцев с даты совершения Операции в сроки, установленные в п. 4.2.10 Договора. Для анализа спорных ситуаций Банк может потребовать письменное заявление Предприятия, счета, чеки и другие документы по электронным каналам связи согласно п. 2.3 Договора.",
   573	      "contract_position": "Пункт 5.2.5: Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции. Для анализа спорных ситуаций исполнитель также может потребовать от заказчика предоставления копии контрольной ленты, письменного заявления заказчика с изложением обстоятельств проведения операции, счетов за предоставленные товары/услуги, товарные или кассовые чеки и другие документы.",
   574	      "matrix_evidence": "«Банк имеет право: → Запрашивать Документы по операциям не позднее 13 (тринадцати) месяцев с даты совершения Операции в сроки, установленные в п. 4.2.10 Договора. Для анализа спорных ситуаций Банк также может потребовать от Предприятия предоставления письменного заявления... по электронным каналам связи одним из способов, указанных в п. 2.3 Договора.» (матрица 5.1.11)",
   575	      "contract_evidence": "«Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции. Для анализа спорных ситуаций исполнитель также может потребовать от заказчика предоставления копии контрольной ленты, письменного заявления заказчика...» (п. 5.2.5 Контракта)",
   576	      "status_reason": "Аналог присутствует, но с отклонениями: (1) отсутствует ссылка на сроки предоставления документов по п. 4.2.10; (2) отсутствует указание на передачу документов по электронным каналам связи согласно п. 2.3; (3) добавлена копия контрольной ленты (расширение перечня). Срок в 13 месяцев сохранен.",
   577	      "risk_level": "low",
   578	      "discrepancies": [
   579	        {
   580	          "type": "procedure",
   581	          "description": "Отсутствует указание на конкретные каналы передачи документов (п. 2.3) и сроки предоставления (п. 4.2.10).",
   582	          "risk": "Низкий риск: общий механизм запроса документов сохранен. Каналы связи определены в разделе 2.3 контракта и применимы по умолчанию."
   583	        }
   584	      ]
   585	    },
   586	    {
   587	      "matrix_ids": [
   588	        "5.1.13"
   589	      ],
   590	      "contract_ids": [
   591	        "5.2.6"
   592	      ],
   593	      "relationship": "deviation",
   594	      "legal_topic": "Право Банка уведомлять об изменении реквизитов через Официальный сайт",
   595	      "matrix_standard": "В случае изменения реквизитов Банка уведомить об этом Предприятие путем размещения информации на Официальном сайте Банка.",
   596	      "contract_position": "Пункт 5.2.6: В случае изменения реквизитов исполнителя, указанных в контракте, уведомить об этом заказчика в письменном виде путем направления информации в адрес заказчика в течение трех рабочих дней.",
   597	      "matrix_evidence": "«Банк имеет право: → В случае изменения реквизитов Банка, указанных в Договоре, уведомить об этом Предприятие путем размещения информации на Официальном сайте Банка.» (матрица 5.1.13)",
   598	      "contract_evidence": "«В случае изменения реквизитов исполнителя, указанных в контракте, уведомить об этом заказчика в письменном виде путем направления информации в адрес заказчика в течение трех рабочих дней» (п. 5.2.6 Контракта)",
   599	      "status_reason": "Аналог присутствует, но способ уведомления изменен: вместо публикации на Официальном сайте Банка — письменное уведомление в адрес Заказчика в течение 3 рабочих дней. Матричный main_idea подчеркивает важность уведомления именно через сайт. Это создает дополнительную административную нагрузку на Банк.",
   600	      "risk_level": "low",
Tool:    201	      ],
   202	      "contract_ids": [
   203	        "5.1.8",
   204	        "Tech_5"
   205	      ],
   206	      "relationship": "aligned",
   207	      "legal_topic": "Bank obligation to transfer funds to Enterprise within 2 working days",
   208	      "matrix_standard": "Bank shall transfer to Enterprise's settlement account the amounts of Payment Operations within 2 working days from receipt of settlement information. Date of receipt is the working day following the day of Electronic reconciliation of totals. In case of technical failure, transfer within 3 calendar days from last successful reconciliation.",
   209	      "contract_position": "Contractor shall transfer to Customer's settlement account the amounts of Payment Operations within 2 working days from receipt of settlement information. Date of receipt is the working day following the day of Electronic reconciliation of totals. In case of technical failure, transfer within 3 calendar days from last Electronic reconciliation. Technical specification confirms same terms.",
   210	      "matrix_evidence": "не позднее 2 (двух) рабочих дней с даты получения расчетной информации Банком перечислять на расчетный (текущий) счет Предприятия суммы Операций оплаты... Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов... по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов",
   211	      "contract_evidence": "5.1.8: не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты... Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов... по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов",
   212	      "status_reason": "Exact match on all material elements: 2-working-day transfer deadline, same definition of receipt date, same 3-calendar-day fallback for technical failures.",
   213	      "risk_level": "none",
   214	      "discrepancies": []
   215	    },
   216	    {
   217	      "matrix_ids": [
   218	        "5.2.9"
   219	      ],
   220	      "contract_ids": [
   221	        "Tech_5"
   222	      ],
   223	      "relationship": "deviation",
   224	      "legal_topic": "Bank obligation to provide partner QR code",
   225	      "matrix_standard": "Bank shall provide the Enterprise with a partner QR code via electronic communication channels in electronic form or on paper",
   226	      "contract_position": "Technical specification requires terminals to have QR-code display capability for cashless payment. No explicit obligation for Bank to provide a separate partner QR code.",
   227	      "matrix_evidence": "Предоставить Предприятию QR-код партнера по электронным каналам связи в электронном виде или на бумажном носителе",
   228	      "contract_evidence": "Tech_5: Возможность вывода QR-кода для безналичной оплаты на дисплей терминала",
   229	      "status_reason": "Matrix requires Bank to provide a partner QR code (static QR on paper or electronic). Contract only requires terminals to have QR-code display capability (dynamic QR on terminal screen). These are different QR mechanisms. The contract's QR capability is about terminal functionality, not about providing a separate partner QR code. However, the contract's Appendix 1.2 (Information about TST) includes QR-code options suggesting QR may be in scope. The matrix item is optional.",
   230	      "risk_level": "low",
   231	      "discrepancies": [
   232	        {
   233	          "type": "obligation",
   234	          "description": "Matrix requires Bank to provide a partner QR code (static QR); contract only requires terminal QR display capability (dynamic QR). Different QR delivery mechanisms.",
   235	          "risk": "Low — matrix item is optional. If partner QR codes are needed, the contract does not explicitly obligate the Bank to provide them."
   236	        }
   237	      ]
   238	    },
   239	    {
   240	      "matrix_ids": [
   241	        "5.2.10"
   242	      ],
   243	      "contract_ids": [
   244	        "5.1.9"
   245	      ],
   246	      "relationship": "aligned",
   247	      "legal_topic": "Bank obligation to process and protect personal data per Federal Law 152-FZ",
   248	      "matrix_standard": "Bank shall process personal data received from the Enterprise and ensure confidentiality and protection of processed personal data in accordance with Federal Law No. 152-FZ. Take necessary legal, organizational and technical measures to protect personal data.",
   249	      "contract_position": "Contractor shall process personal data received from the Customer and ensure confidentiality and protection of processed personal data in accordance with Federal Law No. 152-FZ. Take necessary legal, organizational and technical measures to protect personal data.",
   250	      "matrix_evidence": "Осуществлять обработку ПДн, полученных от Предприятия, а также обеспечить конфиденциальность и защиту обрабатываемых ПДн в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных». Принимать необходимые правовые, организационные и технические меры",
   251	      "contract_evidence": "5.1.9: Осуществлять обработку персональных данных, полученных от заказчика, а также обеспечить конфиденциальность и защиту обрабатываемых персональных данных в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных»... Принимать необходимые правовые, организационные и технические меры",
   252	      "status_reason": "Exact match. Same obligations, same legal reference (152-FZ), same scope of measures.",
   253	      "risk_level": "none",
   254	      "discrepancies": []
   255	    },
   256	    {
   257	      "matrix_ids": [
   258	        "6.1"
   259	      ],
   260	      "contract_ids": [
   261	        "3.2",
   262	        "Spec"
   263	      ],
   264	      "relationship": "deviation",
   265	      "legal_topic": "Bank fee as percentage of payment operations",
   266	      "matrix_standard": "Enterprise pays Bank a fee in the amount of: (________) percent of the amount of Payment Operations",
   267	      "contract_position": "Price per unit of service includes Contractor's expenses for Bank services for settlements with Customer on Payment Operations as a percentage of each Payment Operation. Specification shows maximum contract value of 1,900,000 RUB but the commission percentage is blank.",
   268	      "matrix_evidence": "За осуществление расчетов по Операциям оплаты, Предприятие уплачивает Банку плату в размере: «(____________) процент от суммы Операций оплат».",
   269	      "contract_evidence": "3.2: Цена единицы услуги включает в себя расходы Исполнителя, связанные с оказанием услуг Банка за выполнение расчетов с Заказчиком по Операциям оплаты в виде процента от суммы каждой Операции оплаты. Spec: размер комиссии, % (цена в процентном соотношении) — blank.",
   270	      "status_reason": "Both matrix and contract have blank/placeholder for the actual commission percentage. The contract structure confirms fee-as-percentage model. Per matrix main_idea for 6.21: 'Отсутствие конкретной цены не является противоречием' — absence of a specific value is not a contradiction. However, the blank commission rate is a material gap for both sides.",
   271	      "risk_level": "low",
   272	      "discrepancies": [
   273	        {
   274	          "type": "amount",
   275	          "description": "Commission percentage is blank/placeholder in both matrix and contract. Neither document specifies the actual rate.",
   276	          "risk": "Low — both documents have the same gap. The fee structure (percentage of operations) is aligned. The specific rate would need to be filled before execution."
   277	        }
   278	      ]
   279	    },
   280	    {
   281	      "matrix_ids": [
   282	        "6.2"
   283	      ],
   284	      "contract_ids": [
   285	        "8.3.1",
   286	        "8.3.2"
   287	      ],
   288	      "relationship": "deviation",
   289	      "legal_topic": "Bank's monthly invoicing — UPD delivery deadline",
   290	      "matrix_standard": "Bank monthly, no later than the 5th working day of the month following the reporting month, sends the Enterprise a Universal Transfer Document (UPD) for Bank services. Bank remuneration includes VAT at the rate established by Russian law.",
   291	      "contract_position": "Contractor monthly, no later than the 10th working day of the month following the reporting month, generates and places in EIS a document of acceptance (document o priemke) signed with UKEP. Attaches invoice (schet-faktura) and act of fund transfer. This is the 44-FZ acceptance mechanism.",
   292	      "matrix_evidence": "Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за месяцем оказания услуг... направляет Предприятию Универсальный передаточный документ (УПД) на оплату услуг Банка... Вознаграждение Банка... включает НДС",
   293	      "contract_evidence": "8.3.1: Исполнитель ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за отчетным, формирует с использованием единой информационной системы, подписывает усиленной квалифицированной электронной подписью... и размещает в единой информационной системе документ о приемке",
   294	      "status_reason": "Contract uses 44-FZ EIS-based acceptance document (document o priemke) instead of UPD. The deadline is 10th working day vs. matrix 5th working day. The document type differs (UPD vs. EIS acceptance document), but both serve the same function: monthly invoicing/acceptance for Bank services. The 44-FZ mechanism is a legally equivalent procurement analogue per comparison pattern 16.",
   295	      "risk_level": "medium",
   296	      "discrepancies": [
   297	        {
   298	          "type": "deadline",
   299	          "description": "Matrix requires UPD by 5th working day; contract requires EIS acceptance document by 10th working day. 5-day delay in invoicing.",
   300	          "risk": "Medium — delays Bank's invoicing cycle by 5 working days, affecting cash flow timing."
   301	        },
   302	        {
   303	          "type": "procedure",
   304	          "description": "Matrix uses UPD (Universal Transfer Document); contract uses 44-FZ EIS document of acceptance (document o priemke) with UKEP signature. Different document forms but legally equivalent under 44-FZ.",
   305	          "risk": "Low — 44-FZ EIS mechanism is a legally recognized equivalent. The procedural difference is inherent to the procurement regime."
   306	        }
   307	      ]
   308	    },
   309	    {
   310	      "matrix_ids": [
   311	        "6.4"
   312	      ],
   313	      "contract_ids": [
   314	        "8.5.1",
   315	        "8.5.7"
   316	      ],
   317	      "relationship": "deviation",
   318	      "legal_topic": "Enterprise obligation to accept and return signed UPD or provide motivated refusal",
   319	      "matrix_standard": "Enterprise shall, no later than the 25th day of the month following the Reporting month, return to Bank the signed UPD or provide a motivated refusal to sign the UPD.",
   320	      "contract_position": "Customer shall, within 10 working days from receipt of acceptance document via EIS, sign with UKEP and place in EIS the acceptance document or form a motivated refusal with reasons. This is the 44-FZ acceptance procedure.",
   321	      "matrix_evidence": "Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД либо предоставить мотивированный отказ от подписания УПД.",
   322	      "contract_evidence": "8.5.1: Заказчик в срок не более 10 (десяти) рабочих дней со дня поступления документа о приемке... подписывает усиленной электронной подписью... и размещает в ЕИС документ о приемке либо формирует... мотивированный отказ от подписания документа о приемке",
   323	      "status_reason": "Both provide for acceptance or motivated refusal. Matrix uses 25th calendar day deadline; contract uses 10-working-day deadline from EIS receipt. The 44-FZ mechanism is a procurement analogue. The deadlines differ in structure (calendar day vs. working days) and reference point.",
   324	      "risk_level": "low",
   325	      "discrepancies": [
   326	        {
   327	          "type": "deadline",
   328	          "description": "Matrix: 25th calendar day of month following reporting month. Contract: 10 working days from EIS receipt. Different deadline structures — contract deadline may be shorter or longer depending on when document is posted.",
   329	          "risk": "Low — 44-FZ statutory acceptance timeline. The 10-working-day period is standard under 44-FZ and may actually be shorter than the 25th calendar day, which benefits the Bank."
   330	        },
   331	        {
   332	          "type": "procedure",
   333	          "description": "Matrix uses UPD paper/electronic return; contract uses EIS-based UKEP signing and placement. Different channels but legally equivalent under 44-FZ.",
   334	          "risk": "Low — EIS is the mandatory channel for 44-FZ contracts."
   335	        }
   336	      ]
   337	    },
   338	    {
   339	      "matrix_ids": [
   340	        "6.5"
   341	      ],
   342	      "contract_ids": [
   343	        "4.5"
   344	      ],
   345	      "relationship": "deviation",
   346	      "legal_topic": "Enterprise payment for Bank services within 5 working days after UPD signing",
   347	      "matrix_standard": "Payment for Bank services shall be made by Enterprise within 5 working days from the date of signing the UPD, in non-cash form by transferring funds to Bank's account specified in the UPD.",
   348	      "contract_position": "Payment term for rendered services is no more than 7 working days from the date of signing by Customer of the acceptance document, made monthly.",
   349	      "matrix_evidence": "Оплата услуг Банка... производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
   350	      "contract_evidence": "4.5: Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг и производится ежемесячно.",
   351	      "status_reason": "Both require payment after acceptance document signing. Matrix: 5 working days. Contract: 7 working days. The 2-day extension is a material deviation in payment timing.",
   352	      "risk_level": "medium",
   353	      "discrepancies": [
   354	        {
   355	          "type": "deadline",
   356	          "description": "Matrix: 5 working days from UPD signing. Contract: 7 working days from acceptance document signing. 2-working-day delay in payment to Bank.",
   357	          "risk": "Medium — delays Bank's receipt of payment by 2 working days, affecting cash flow."
   358	        }
   359	      ]
   360	    },
   361	    {
   362	      "matrix_ids": [
   363	        "6.20"
   364	      ],
   365	      "contract_ids": [
   366	        "Tech_5"
   367	      ],
   368	      "relationship": "aligned",
   369	      "legal_topic": "No fee charged for return operations; original fee not refunded",
   370	      "matrix_standard": "For Return operations, Chargeback, and Reversal transactions, the fee for conducting settlements is not charged. The fee for settlements withheld by the Bank when processing the original Payment Operation is not returned.",
   371	      "contract_position": "For Return operations, Chargeback, and Reversal transactions, the fee for conducting settlements is not charged. In this case, the fee for settlements withheld by the Bank when processing the original Payment Operation is not returned.",
   372	      "matrix_evidence": "По Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается. В этом случае плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается.",
   373	      "contract_evidence": "Tech_5: по Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается. В этом случае плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается;",
   374	      "status_reason": "Exact match. Same rule: no fee on returns/chargebacks/reversals, and original fee is not refunded.",
   375	      "risk_level": "none",
   376	      "discrepancies": []
   377	    },
   378	    {
   379	      "matrix_ids": [
   380	        "6.21"
   381	      ],
   382	      "contract_ids": [
   383	        "3.1"
   384	      ],
   385	      "relationship": "aligned",
   386	      "legal_topic": "Contract price specification",
   387	      "matrix_standard": "Contract Price is _________ (__________) rubles __ kopecks (including VAT)",
   388	      "contract_position": "Maximum contract price is 1,900,000.00 rubles (one million nine hundred thousand rubles 00 kopecks), including VAT ________ (if Contractor is not a VAT payer, indicate 'VAT not assessed')",
   389	      "matrix_evidence": "Цена Договора составляет _________ (______________________) рублей __ копеек. ( в том числе НДС)",
   390	      "contract_evidence": "3.1: Максимальное значение цены контракта (стоимость услуг) составляет 1 900 000,00 рублей... в том числе НДС ______________",
   391	      "status_reason": "Matrix has blank placeholder; contract has a filled amount (1,900,000 RUB). Per matrix main_idea: 'Отсутствие конкретной цены не является противоречием' — absence of specific price is not a contradiction. The contract provides a concrete maximum price which is consistent with the matrix structure.",
   392	      "risk_level": "none",
   393	      "discrepancies": []
   394	    },
   395	    {
   396	      "matrix_ids": [
   397	        "7.1"
   398	      ],
   399	      "contract_ids": [
   400	        "7.1"
   401	      ],
   402	      "relationship": "aligned",
   403	      "legal_topic": "General liability clause — parties liable per contract and law",
   404	      "matrix_standard": "For non-performance or improper performance of obligations under the Contract, the Parties shall bear liability in accordance with the terms of the Contract and the legislation of the Russian Federation.",
   405	      "contract_position": "For non-performance or improper performance of obligations under the Contract, the Parties shall bear liability in accordance with the current legislation of the Russian Federation.",
   406	      "matrix_evidence": "За неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с условиями Договора и законодательством РФ.",
   407	      "contract_evidence": "7.1: За неисполнение или ненадлежащее исполнение обязательств по Контракту Стороны несут ответственность в соответствии с действующим законодательством Российской Федерации.",
   408	      "status_reason": "Aligned. Both establish general liability under Russian law. Contract omits 'условиями Договора' (contract terms) but this is implicit in the contract structure and 44-FZ framework.",
   409	      "risk_level": "none",
   410	      "discrepancies": []
   411	    },
   412	    {
   413	      "matrix_ids": [
   414	        "7.2"
   415	      ],
   416	      "contract_ids": [
   417	        "7.4",
   418	        "7.4.1"
   419	      ],
   420	      "relationship": "aligned",
   421	      "legal_topic": "Enterprise (Customer) fines for non-performance excluding delay",
   422	      "matrix_standard": "For each fact of non-performance by Enterprise of obligations under the Contract, excluding delay, the fine is: a) 1000 RUB if Contract Price ≤ 3M RUB; b) 5000 RUB if 3M-50M RUB; c) 10000 RUB if 50M-100M RUB; d) 100000 RUB if >100M RUB.",
   423	      "contract_position": "For each fact of non-performance by Customer of obligations under the Contract, excluding delay, the fine is set per Government Resolution No. 1042: a) 1000 RUB if ≤ 3M RUB; b) 5000 RUB if 3M-50M RUB; c) 10000 RUB if 50M-100M RUB; d) 100000 RUB if >100M RUB.",
   424	      "matrix_evidence": "За каждый факт неисполнения Предприятием обязательств... размер штрафа устанавливается в следующем порядке: а) 1000 рублей, если Цена Договора не превышает 3 млн. рублей...",
   425	      "contract_evidence": "7.4.1: а) 1000 рублей, если цена контракта не превышает 3 млн. рублей (включительно); б) 5000 рублей, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно)...",
   426	      "status_reason": "Aligned. Same fine amounts and brackets. Both follow Government Resolution No. 1042 structure. The contract applies fines to Customer (Заказчик) which is the same party as Enterprise (Предприятие) in the matrix.",
   427	      "risk_level": "none",
   428	      "discrepancies": []
   429	    },
   430	    {
   431	      "matrix_ids": [
   432	        "7.3"
   433	      ],
   434	      "contract_ids": [
   435	        "7.1"
   436	      ],
   437	      "relationship": "aligned",
   438	      "legal_topic": "Cap on total Enterprise fines — not exceeding Contract Price",
   439	      "matrix_standard": "The total amount of accrued fines for improper performance by the Enterprise of obligations under the Contract may not exceed the Contract Price.",
   440	      "contract_position": "The total amount of accrued fines for improper performance by the Customer of obligations under the Contract may not exceed the Contract Price.",
   441	      "matrix_evidence": "Общая сумма начисленных штрафов за ненадлежащее исполнение Предприятием обязательств, предусмотренных Договором, не может превышать цену Договора.",
   442	      "contract_evidence": "7.1: Общая сумма начисленных штрафов за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, не может превышать цену контракта.",
   443	      "status_reason": "Aligned. Same cap: total fines ≤ Contract Price.",
   444	      "risk_level": "none",
   445	      "discrepancies": []
   446	    },
   447	    {
   448	      "matrix_ids": [
   449	        "7.4"
   450	      ],
   451	      "contract_ids": [
   452	        "7.5",
   453	        "7.6"
   454	      ],
   455	      "relationship": "aligned",
   456	      "legal_topic": "Bank (Contractor) liability — penalties for delay",
   457	      "matrix_standard": "In case of delay by Bank, Enterprise sends Bank a demand for payment of penalties (fines, late fees). Penalty accrues for each day of delay starting from the day after the deadline, at 1/300 of CBR key rate of the Contract Price reduced by proportionally fulfilled obligations.",
   458	      "contract_position": "In case of delay by Contractor, Customer sends Contractor a demand for payment of penalties (fines, late fees). Penalty accrues for each day of delay at 1/300 of CBR key rate of the Contract Price reduced by proportionally fulfilled obligations.",
   459	      "matrix_evidence": "В случае просрочки исполнения Банком обязательств... Предприятие направляет Банку требование об уплате неустоек (штрафов, пеней). Пеня начисляется за каждый день просрочки... в размере 1/300 действующей на дату уплаты пеней ключевой ставки Центрального банка Российской Федерации от Цены Договора, уменьшенной на сумму, пропорциональную объему обязательств",
   460	      "contract_evidence": "7.5-7.6: В случае просрочки исполнения Исполнителем обязательств... Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней). Пеня начисляется за каждый день просрочки... в размере 1/300 действующей на дату уплаты пеней ключевой ставки Центрального банка Российской Федерации от цены контракта, уменьшенной на сумму, пропорциональную объему обязательств",
   461	      "status_reason": "Aligned. Same penalty mechanism: 1/300 CBR key rate, same base (Contract Price minus fulfilled proportion), same trigger (delay).",
   462	      "risk_level": "none",
   463	      "discrepancies": []
   464	    },
   465	    {
   466	      "matrix_ids": [
   467	        "7.5"
   468	      ],
   469	      "contract_ids": [
   470	        "7.7",
   471	        "7.7.1"
   472	      ],
   473	      "relationship": "aligned",
   474	      "legal_topic": "Bank (Contractor) fines for non-performance with monetary value",
   475	      "matrix_standard": "For each fact of non-performance by Bank of obligations with monetary value, excluding delay: a) 10% of Contract Price if ≤ 3M RUB; b) 5% if 3M-50M RUB; c) 1% if 50M-100M RUB; etc.",
   476	      "contract_position": "For each fact of non-performance by Contractor of obligations, excluding delay: a) 10% of Contract Price if ≤ 3M RUB; b) 5% if 3M-50M RUB; c) 1% if 50M-100M RUB; etc. Per Government Resolution No. 1042.",
   477	      "matrix_evidence": "За каждый факт неисполнения или ненадлежащего исполнения Банком обязательств... размер штрафа устанавливается в следующем порядке: а) 10 процентов Цены Договора в случае, если Цена Договора не превышает 3 млн. рублей; б) 5 процентов...",
   478	      "contract_evidence": "7.7.1: а) 10 процентов цены контракта (этапа) в случае, если цена контракта (этапа) не превышает 3 млн. рублей; б) 5 процентов цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 3 млн. рублей до 50 млн. рублей...",
   479	      "status_reason": "Aligned. Same percentage brackets. Both follow 44-FZ / Resolution 1042 structure.",
   480	      "risk_level": "none",
   481	      "discrepancies": []
   482	    },
   483	    {
   484	      "matrix_ids": [
   485	        "7.6"
   486	      ],
   487	      "contract_ids": [
   488	        "7.7.3"
   489	      ],
   490	      "relationship": "aligned",
   491	      "legal_topic": "Bank (Contractor) fines for non-performance without monetary value",
   492	      "matrix_standard": "For each fact of non-performance by Bank of obligations without monetary value: a) 1000 RUB if ≤ 3M RUB; b) 5000 RUB if 3M-50M RUB; c) 10000 RUB if 50M-100M RUB; d) 100000 RUB if >100M RUB.",
   493	      "contract_position": "For each fact of non-performance by Contractor of obligations without monetary value: a) 1000 RUB if ≤ 3M RUB; b) 5000 RUB if 3M-50M RUB; c) 10000 RUB if 50M-100M RUB; d) 100000 RUB if >100M RUB.",
   494	      "matrix_evidence": "За каждый факт неисполнения или ненадлежащего исполнения Банком обязательств... которое не имеет стоимостного выражения, размер штрафа устанавливается в следующем порядке: а) 1000 рублей... б) 5000 рублей...",
   495	      "contract_evidence": "7.7.3: а) 1000 рублей, если цена контракта не превышает 3 млн. рублей... б) 5000 рублей, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей...",
   496	      "status_reason": "Aligned. Same fixed fine amounts and brackets.",
   497	      "risk_level": "none",
   498	      "discrepancies": []
   499	    },
   500	    {
   501	      "matrix_ids": [
   502	        "7.7"
   503	      ],
   504	      "contract_ids": [
   505	        "7.10"
   506	      ],
   507	      "relationship": "aligned",
   508	      "legal_topic": "Cap on total Bank fines — not exceeding Contract Price",
   509	      "matrix_standard": "The total amount of accrued fines for non-performance or improper performance by the Bank of obligations under the Contract may not exceed the Contract Price.",
   510	      "contract_position": "The total amount of accrued fines for non-performance or improper performance by the Contractor of obligations under the Contract may not exceed the Contract Price.",
   511	      "matrix_evidence": "Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Банком обязательств, предусмотренных Договором, не может превышать Цену Договора",
   512	      "contract_evidence": "7.10: Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, не может превышать цену Контракта.",
   513	      "status_reason": "Aligned. Same cap: total fines ≤ Contract Price.",
   514	      "risk_level": "none",
   515	      "discrepancies": []
   516	    },
   517	    {
   518	      "matrix_ids": [
   519	        "7.8"
   520	      ],
   521	      "contract_ids": [
   522	        "5.3.19"
   523	      ],
   524	      "relationship": "deviation",
   525	      "legal_topic": "Bank not liable for disputes between Enterprise and Buyer",
   526	      "matrix_standard": "Bank shall not be liable for disputes and disagreements arising between the Enterprise and the Buyer in all cases where such disputes do not relate to the subject of the Contract, as well as for disputes regarding Goods/services paid for using Cards.",
   527	      "contract_position": "Customer shall reimburse Contractor in full for: funds debited from Contractor per Payment System rules for disputed operations; losses from fines applied to Contractor due to Customer's non-performance. This is an indemnity approach rather than a liability exclusion.",
   528	      "matrix_evidence": "Банк не несет ответственности по спорам и разногласиям, возникающим между Предприятием и Покупателем во всех случаях, когда такие споры и разногласия не относятся к предмету Договора, а также по спорам в отношении Товаров/услуг, оплаченных с использованием Карты",
   529	      "contract_evidence": "5.3.19: Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере: средств, которые... были списаны со счета Исполнителя в пользу Банка-эмитента... по Операциям ставшим предметом каких-либо споров... убытков, возникших у Исполнителя в результате применения к нему штрафных санкций",
   530	      "status_reason": "Matrix provides a direct liability exclusion for Bank regarding Enterprise-Buyer disputes. Contract takes a different approach: it imposes an indemnity obligation on the Customer to reimburse the Bank for losses from disputed operations. The contract approach is actually stronger for the Bank — instead of merely excluding liability, it creates an affirmative reimbursement obligation. However, the matrix's explicit liability exclusion language is not directly present.",
   531	      "risk_level": "low",
   532	      "discrepancies": [
   533	        {
   534	          "type": "liability",
   535	          "description": "Matrix: direct liability exclusion for Bank. Contract: affirmative indemnity from Customer for disputed operations. Different legal mechanisms but contract provides stronger Bank protection.",
   536	          "risk": "Low — contract's indemnity approach is more protective of Bank than a simple liability exclusion."
   537	        }
   538	      ]
   539	    },
   540	    {
   541	      "matrix_ids": [
   542	        "7.16"
   543	      ],
   544	      "contract_ids": [
   545	        "6.1"
   546	      ],
   547	      "relationship": "aligned",
   548	      "legal_topic": "Anti-corruption clause",
   549	      "matrix_standard": "When concluding, performing, amending and terminating the Contract, the Parties undertake not to carry out actions qualified by applicable law as 'corruption', as well as other actions violating anti-corruption legislation.",
   550	      "contract_position": "When concluding, performing, amending and terminating the Contract, the Parties undertake not to carry out actions qualified by applicable law as 'corruption', as well as other actions violating applicable anti-corruption legislation.",
   551	      "matrix_evidence": "При заключении, исполнении, изменении и расторжении Договора Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция», а также иных действий (бездействия), нарушающих требования применимого законодательства... в области противодействия коррупции",
   552	      "contract_evidence": "6.1: При заключении, исполнении, изменении и расторжении Контракта Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция», а также иных действий (бездействия), нарушающих требования применимого законодательства, применимых норм международного права в области противодействия коррупции.",
   553	      "status_reason": "Exact match. Same anti-corruption undertaking covering all contract phases.",
   554	      "risk_level": "none",
   555	      "discrepancies": []
   556	    },
   557	    {
   558	      "matrix_ids": [
   559	        "8.1"
   560	      ],
   561	      "contract_ids": [
   562	        "9.1"
   563	      ],
   564	      "relationship": "deviation",
   565	      "legal_topic": "Force majeure — grounds for exemption from liability",
   566	      "matrix_standard": "A Party shall be released from liability for partial or full non-performance if caused by force majeure circumstances of an extraordinary nature that the Party could neither foresee nor prevent by reasonable measures. Such circumstances include: natural disasters, accidents, fires, mass disorders, strikes, revolutions, military actions, unlawful actions of third parties, prohibitive acts of state authorities, and other circumstances beyond the Parties' control.",
   567	      "contract_position": "Parties shall be released from liability for partial or full non-performance if prevented by extraordinary and insurmountable circumstances (force majeure): natural disasters, floods, earthquakes, fires, military actions, strikes, mass diseases (epidemics) leading to heightened readiness or emergency regime.",
   568	      "matrix_evidence": "Сторона Договора освобождается от ответственности за частичное или полное неисполнение обязательств по Договору, если это неисполнение явилось следствием обстоятельств непреодолимой силы, возникших в результате обстоятельств чрезвычайного характера, которые сторона не могла ни предвидеть, ни предотвратить разумными мерами. К таким обстоятельствам... относятся стихийные бедствия, аварии, пожары, массовые беспорядки, забастовки, революции, военные действия, неправомерные действия третьих лиц, запретительные акты государственных органов",
   569	      "contract_evidence": "9.1: Стороны освобождаются от ответственности за частичное или полное неисполнение своих обязательств по настоящему контракту, если их исполнению препятствует чрезвычайное и непреодолимое при данных условиях обстоятельство (непреодолимая сила), а именно: стихийные бедствия, наводнения, землетрясения, пожары, военные действия, забастовки, массовые заболевания(эпидемия), повлекшие введение режима повышенной готовности или чрезвычайной ситуации.",
   570	      "status_reason": "Both contain force majeure clauses. Contract list is narrower: omits 'accidents', 'mass disorders', 'revolutions', 'unlawful actions of third parties', 'prohibitive acts of state authorities'. Contract adds 'floods', 'earthquakes', 'epidemics'. The contract's narrower list could expose the Bank to liability for events covered by matrix but not by contract.",
   571	      "risk_level": "medium",
   572	      "discrepancies": [
   573	        {
   574	          "type": "scope",
   575	          "description": "Contract force majeure list is narrower than matrix. Matrix includes: accidents, mass disorders, revolutions, unlawful third-party actions, prohibitive state acts — none of which appear in the contract. Contract adds epidemics but omits several matrix categories.",
   576	          "risk": "Medium — narrower force majeure definition could expose Bank to liability for events that would be excused under the matrix standard."
   577	        }
   578	      ]
   579	    },
   580	    {
   581	      "matrix_ids": [
   582	        "8.2"
   583	      ],
   584	      "contract_ids": [
   585	        "9.2"
   586	      ],
   587	      "relationship": "deviation",
   588	      "legal_topic": "Force majeure — notification deadline and consequences",
   589	      "matrix_standard": "Upon occurrence of force majeure, the affected Party must notify the other Party within 24 hours via clause 2.3, specifying the nature of circumstances, assessment of impact, and estimated performance timeline. If circumstances last more than 3 months, either Party may terminate the Contract.",
   590	      "contract_position": "Upon occurrence of force majeure, the affected Party must notify the other Party within 5 days from occurrence. Performance deadline is extended proportionally. If circumstances last more than 1 calendar month, Parties may terminate by agreement.",
   591	      "matrix_evidence": "При наступлении обстоятельств... Сторона... должна в течение 24 (двадцати четырех) часов известить о них другую Сторону в соответствии с п.2.3 Договора, с обязательным указанием данных о характере обстоятельств, оценку их влияния... и предполагаемый срок их исполнения... Если обстоятельства длятся более 3 месяцев, любая Сторона вправе расторгнуть Договор",
   592	      "contract_evidence": "9.2: При возникновении обстоятельств непреодолимой силы... она обязана оповестить другую Сторону не позднее пяти дней с момента возникновения таких обстоятельств, при этом срок выполнения обязательств по контракту переносится соразмерно времени... В случае если такие обстоятельства длятся более одного календарного месяца Стороны праве расторгнуть настоящий контракт по соглашению Сторон.",
   593	      "status_reason": "Material deviations in both notification deadline and termination trigger. Matrix: 24-hour notification; Contract: 5-day notification. Matrix: termination right after 3 months; Contract: termination by agreement after 1 month. The shorter notification deadline in the matrix is more protective of the counterparty; the longer force majeure duration before termination in the matrix is more protective of contract stability.",
   594	      "risk_level": "medium",
   595	      "discrepancies": [
   596	        {
   597	          "type": "deadline",
   598	          "description": "Matrix: 24-hour force majeure notification. Contract: 5-day notification. 5-day delay in notification could prejudice the Bank's ability to respond.",
   599	          "risk": "Medium — delayed notification reduces Bank's ability to mitigate force majeure impacts."
   600	        },
AI: Now let me check the remaining batch 4 output for unmatched_contract items and also look at the full contract for sections I haven't reviewed:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_4_output.json', 'offset': 600, 'limit': 500}, 'id': 'call_00_82Sn1ZKfMUqEbNaeoKln6580', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_3_output.json', 'offset': 600, 'limit': 500}, 'id': 'call_01_IUwdIdyS8MT6nqLw0Uyg2888', 'type': 'tool_call'}]
Tool:    601	        {
   602	          "type": "deadline",
   603	          "description": "Matrix: termination right after 3 months of force majeure. Contract: termination by mutual agreement after 1 month. Contract allows earlier exit but requires mutual consent rather than unilateral right.",
   604	          "risk": "Medium — earlier termination possibility (1 month vs 3) but requires agreement rather than unilateral right."
   605	        }
   606	      ]
   607	    },
   608	    {
   609	      "matrix_ids": [
   610	        "9.1"
   611	      ],
   612	      "contract_ids": [
   613	        "10.1"
   614	      ],
   615	      "relationship": "aligned",
   616	      "legal_topic": "Mandatory pre-trial dispute resolution procedure",
   617	      "matrix_standard": "Dispute resolution between the Parties shall be conducted through a claims (pre-trial) procedure.",
   618	      "contract_position": "All disputes or disagreements between the Parties under this contract or in connection with it shall be resolved through negotiations (pre-trial procedure).",
   619	      "matrix_evidence": "Урегулирование споров Сторон совершается в претензионном порядке",
   620	      "contract_evidence": "10.1: Все споры или разногласия, возникающие между Сторонами по настоящему контракту или в связи с ним, разрешаются путем переговоров (в досудебном порядке).",
   621	      "status_reason": "Aligned. Both establish mandatory pre-trial/claims procedure for dispute resolution.",
   622	      "risk_level": "none",
   623	      "discrepancies": []
   624	    },
   625	    {
   626	      "matrix_ids": [
   627	        "9.2"
   628	      ],
   629	      "contract_ids": [
   630	        "10.1"
   631	      ],
   632	      "relationship": "aligned",
   633	      "legal_topic": "Claim consideration period — 10 calendar days",
   634	      "matrix_standard": "Claims shall be considered by the Parties within 10 (ten) calendar days from the date of their receipt by one of the Parties.",
   635	      "contract_position": "Response period for claims, letters and appeals — 10 (ten) calendar days from the date of their receipt.",
   636	      "matrix_evidence": "Претензии рассматриваются Сторонами в течение 10 (десяти) календарных дней с даты их получения одной из Сторон.",
   637	      "contract_evidence": "10.1: Срок ответа на претензии, письма и обращения – 10 (десять) календарных дней с даты их получения.",
   638	      "status_reason": "Exact match. Same 10-calendar-day claim consideration period.",
   639	      "risk_level": "none",
   640	      "discrepancies": []
   641	    },
   642	    {
   643	      "matrix_ids": [
   644	        "9.3"
   645	      ],
   646	      "contract_ids": [
   647	        "10.2"
   648	      ],
   649	      "relationship": "deviation",
   650	      "legal_topic": "Court resolution of unresolved disputes",
   651	      "matrix_standard": "Disputes not resolved through the claims procedure shall be resolved in accordance with the current legislation of the Russian Federation.",
   652	      "contract_position": "If disagreements cannot be resolved through negotiations, they shall be considered in the Arbitration Court of Krasnodar Krai.",
   653	      "matrix_evidence": "Споры, не урегулированные в претензионном порядке, подлежат разрешению в соответствии с действующим законодательством РФ.",
   654	      "contract_evidence": "10.2: В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в Арбитражном суде Краснодарского края.",
   655	      "status_reason": "Matrix provides general reference to Russian legislation for dispute resolution. Contract specifies a particular arbitration court (Arbitration Court of Krasnodar Krai). This is a jurisdictional specification rather than a deviation — the matrix's general reference to legislation would include court jurisdiction rules. However, fixing a specific court may affect the Bank if its location differs from Krasnodar Krai.",
   656	      "risk_level": "low",
   657	      "discrepancies": [
   658	        {
   659	          "type": "procedure",
   660	          "description": "Matrix: general reference to RF legislation. Contract: specifies Arbitration Court of Krasnodar Krai. This fixes venue to the Customer's location.",
   661	          "risk": "Low — jurisdictional specification is standard in contracts. The Bank would need to litigate in Krasnodar Krai rather than its own location."
   662	        }
   663	      ]
   664	    },
   665	    {
   666	      "matrix_ids": [
   667	        "10.1"
   668	      ],
   669	      "contract_ids": [
   670	        "11.1"
   671	      ],
   672	      "relationship": "deviation",
   673	      "legal_topic": "Contract duration and termination",
   674	      "matrix_standard": "Contract enters into force from the date of signing by both Parties and is valid until _________ (inclusive) or until the Contract Price is exhausted (whichever occurs first). Expiry does not release Parties from liability for non-performance.",
   675	      "contract_position": "Contract is valid from the date of conclusion until 30 December 2025, or until the maximum Contract Price is exhausted (whichever occurs first). For obligations arising during the contract period but not fulfilled by expiry — until full performance. Expiry does not release Parties from liability.",
   676	      "matrix_evidence": "Настоящий Договор вступает в силу с даты его подписания обеими Сторонами и действует по ___________ (включительно) или до исчерпания Цены договора (в зависимости от того, какое событие наступит первым). Окончание срока действия Договора не освобождает Стороны от ответственности",
   677	      "contract_evidence": "11.1: Настоящий контракт действует с даты заключения по 30 декабря 2025 года, или до момента исчерпания предельной Цены Контракта... в зависимости от того, какое из событий условие наступит ранее, а по обязательствам, возникшим в период действия настоящего Контракта, но не исполненным до окончания срока действия Контракта – до полного исполнения принятых сторонами обязательств. Окончание срока действия контракта не освобождает Стороны от ответственности за его нарушение.",
   678	      "status_reason": "Contract fills the blank end date (30 December 2025) and adds survival clause for unfulfilled obligations. The matrix has a blank end date. The contract's additional survival-of-obligations language is actually more protective. Core structure aligned.",
   679	      "risk_level": "low",
   680	      "discrepancies": [
   681	        {
   682	          "type": "other",
   683	          "description": "Contract adds survival clause: obligations arising during contract period survive until full performance. Matrix does not have this explicit survival language. This is beneficial to the Bank.",
   684	          "risk": "Low — additional survival language benefits the Bank by preserving post-expiry obligations."
   685	        }
   686	      ]
   687	    },
   688	    {
   689	      "matrix_ids": [
   690	        "10.2"
   691	      ],
   692	      "contract_ids": [
   693	        "5.2.2",
   694	        "5.4.3",
   695	        "11.3",
   696	        "11.4",
   697	        "11.5"
   698	      ],
   699	      "relationship": "deviation",
   700	      "legal_topic": "Unilateral extrajudicial termination right with 30-day notice",
   701	      "matrix_standard": "Either Party may early terminate the Contract unilaterally out of court by notifying the other Party in writing at least 30 calendar days before the termination date, except for cases provided in clause 5.1.8 of the Contract.",
   702	      "contract_position": "Contract termination is permitted by agreement of the Parties, by court decision, or by unilateral refusal under the Civil Code. Customer may unilaterally refuse under Civil Code grounds. Unilateral refusal is implemented per Article 95 of Federal Law 44-FZ. Changes/termination per Articles 34, 95, 96, 112 of 44-FZ. Contractor may unilaterally refuse under 44-FZ and Civil Code (5.2.2).",
   703	      "matrix_evidence": "Любая Сторона по Договору вправе его досрочно расторгнуть в одностороннем внесудебном порядке, письменно уведомив об этом другую Сторону не менее чем за 30 (тридцать) календарных дней до даты расторжения, за исключением случаев, предусмотренных п. 5.1.8 настоящего Договора",
   704	      "contract_evidence": "11.3-11.5: Расторжение контракта допускается по соглашению Сторон, по решению суда, в случае одностороннего отказа Стороны контракта от исполнения контракта в соответствии с гражданским законодательством... Решение Сторон об одностороннем отказе от исполнения контракта... принимается и реализуется в порядке и сроки, предусмотренные статьей 95 Федерального закона № 44-ФЗ.",
   705	      "status_reason": "Matrix provides a simple 30-day notice unilateral termination right for either party. Contract ties termination to 44-FZ statutory procedures (Article 95), which have specific notice periods, EIS publication requirements, and cure periods. The 44-FZ mechanism is a procurement analogue but materially changes the termination procedure. The 30-day simple notice is replaced by the more complex 44-FZ regime.",
   706	      "risk_level": "medium",
   707	      "discrepancies": [
   708	        {
   709	          "type": "procedure",
   710	          "description": "Matrix: simple 30-day written notice for unilateral termination. Contract: 44-FZ Article 95 procedure with EIS publication, specific timelines, and cure periods. More complex and restrictive termination process.",
   711	          "risk": "Medium — 44-FZ termination procedure is more burdensome than simple 30-day notice. Bank cannot terminate quickly for convenience; must follow statutory 44-FZ process."
   712	        },
   713	        {
   714	          "type": "deadline",
   715	          "description": "Matrix: 30 calendar days notice. Contract: 44-FZ statutory timelines which may differ from 30 days.",
   716	          "risk": "Medium — different and potentially longer termination timeline under 44-FZ."
   717	        }
   718	      ]
   719	    },
   720	    {
   721	      "matrix_ids": [
   722	        "11.1"
   723	      ],
   724	      "contract_ids": [
   725	        "11.7"
   726	      ],
   727	      "relationship": "deviation",
   728	      "legal_topic": "Sources of legal regulation and Payment System rules primacy",
   729	      "matrix_standard": "Parties agree that sources of legal regulation are: the Contract, current RF legislation, Payment System rules/standards/recommendations (provided they do not contradict RF legislation). Any Contract terms contradicting Payment System rules must be brought into compliance. Payment System rules prevail over Contract terms.",
   730	      "contract_position": "In all matters not provided for by this contract, the Parties shall be governed by the current legislation of the Russian Federation.",
   731	      "matrix_evidence": "Стороны соглашаются, что источниками правового регулирования отношений Сторон в рамках Договора являются настоящие Договор, действующее законодательство РФ, правила, стандарты и рекомендации Платежной системы при условии их не противоречия действующему законодательству РФ. Любые условия и положения Договора, которые противоречат положениям правил Платежной системы... должны быть приведены в соответствие",
   732	      "contract_evidence": "11.7: Во всем, что не предусмотрено настоящим контрактом, Стороны руководствуются действующим законодательством Российской Федерации.",
   733	      "status_reason": "Matrix explicitly incorporates Payment System rules as a source of regulation and gives them primacy over conflicting contract terms. Contract only references RF legislation as the gap-filling source. The absence of Payment System rules incorporation is a material gap — Payment System rules (e.g., MIR, VISA, MasterCard) contain critical operational requirements that the Bank must comply with.",
   734	      "risk_level": "high",
   735	      "discrepancies": [
   736	        {
   737	          "type": "scope",
   738	          "description": "Matrix incorporates Payment System rules as binding and gives them primacy over contract terms. Contract only references RF legislation. Payment System rules are not mentioned as a regulatory source.",
   739	          "risk": "High — without Payment System rules incorporation, the Bank may face conflicts between Payment System requirements and contract terms, with no contractual mechanism to resolve in favor of Payment System rules."
   740	        }
   741	      ]
   742	    },
   743	    {
   744	      "matrix_ids": [
   745	        "11.4"
   746	      ],
   747	      "contract_ids": [
   748	        "11.2"
   749	      ],
   750	      "relationship": "deviation",
   751	      "legal_topic": "Amendments must be in writing and signed by both parties",
   752	      "matrix_standard": "All amendments and supplements to this Contract, except for documents referenced in the Contract and posted on the Bank's Official Website, are valid only if made in writing and signed by authorized representatives of the Parties.",
   753	      "contract_position": "Any amendments and supplements to this contract are valid only if made in writing and signed by both Parties. If either Party changes its location or name, it must notify the other Party in writing within two days.",
   754	      "matrix_evidence": "Все изменения и дополнения к настоящему Договору, кроме документов, ссылки на которые даются в настоящем Договоре, размещенные на Официальном сайте Банка, действительны лишь в том случае, если они совершены в письменной форме, и подписаны уполномоченными представителями Сторон",
   755	      "contract_evidence": "11.2: Любые изменения и дополнения к настоящему контракту имеют силу только в том случае, если они оформлены в письменном виде и подписаны обеими Сторонами.",
   756	      "status_reason": "Both require written form and signatures. However, matrix contains an important exception: documents posted on the Bank's Official Website can be amended without bilateral signatures. The contract does not have this exception, meaning all changes require bilateral agreement. This limits the Bank's ability to unilaterally update operational documents via its website.",
   757	      "risk_level": "medium",
   758	      "discrepancies": [
   759	        {
   760	          "type": "procedure",
   761	          "description": "Matrix allows unilateral amendment of documents posted on Bank's Official Website without bilateral signatures. Contract requires bilateral signatures for all amendments with no website exception.",
   762	          "risk": "Medium — Bank loses ability to unilaterally update operational procedures, tariffs, and instructional materials via its website."
   763	        }
   764	      ]
   765	    },
   766	    {
   767	      "matrix_ids": [
   768	        "11.6"
   769	      ],
   770	      "contract_ids": [
   771	        "12.4"
   772	      ],
   773	      "relationship": "aligned",
   774	      "legal_topic": "Number of contract copies",
   775	      "matrix_standard": "This Contract is executed in ________ copies, _________ copy(ies) for the Bank, one copy for the Enterprise.",
   776	      "contract_position": "The Contract is executed in electronic form and signed with enhanced qualified electronic signatures of the Parties.",
   777	      "matrix_evidence": "Настоящий Договор составлен в ________ экземплярах, _________ экземпляр(-а) для Банка, один экземпляр для Предприятия",
   778	      "contract_evidence": "12.4: Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон.",
   779	      "status_reason": "Matrix contemplates paper copies with blank for number. Contract is electronic with UKEP signatures — this is the standard form for 44-FZ contracts concluded electronically. The electronic form is a functional equivalent under 44-FZ.",
   780	      "risk_level": "none",
   781	      "discrepancies": []
   782	    },
   783	    {
   784	      "matrix_ids": [
   785	        "11.7"
   786	      ],
   787	      "contract_ids": [
   788	        "1.1",
   789	        "12.5"
   790	      ],
   791	      "relationship": "aligned",
   792	      "legal_topic": "Appendices are integral parts of the Contract",
   793	      "matrix_standard": "All Appendices to this Contract are its integral part.",
   794	      "contract_position": "Technical Assignment (Appendix No. 1) and Specification (Appendix No. 2) are integral parts of this contract. Section 12.5 lists all appendices.",
   795	      "matrix_evidence": "Все Приложения к настоящему Договору являются его неотъемлемой частью",
   796	      "contract_evidence": "1.1: в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта. 12.5: lists all appendices.",
   797	      "status_reason": "Aligned. Both state that appendices are integral parts of the contract.",
   798	      "risk_level": "none",
   799	      "discrepancies": []
   800	    },
   801	    {
   802	      "matrix_ids": [
   803	        "11.9"
   804	      ],
   805	      "contract_ids": [
   806	        "12.1"
   807	      ],
   808	      "relationship": "aligned",
   809	      "legal_topic": "Prohibition on assignment of rights/obligations without consent",
   810	      "matrix_standard": "Neither Party may transfer its obligations and/or rights under the Contract to third parties without the written consent of the other Party, except in the case of reorganization of one of the Parties.",
   811	      "contract_position": "During performance of this contract, substitution of the Contractor is not permitted, except when the new contractor is the legal successor of the Contractor due to reorganization in the form of transformation, merger, or accession.",
   812	      "matrix_evidence": "Ни одна из Сторон не вправе передавать свои обязанности и/или права по Договору третьим лицам без письменного согласования с другой Стороной, за исключением случая реорганизации одной из Сторон",
   813	      "contract_evidence": "12.1: При исполнении настоящего контракта не допускается перемена Исполнителя, за исключением случая, когда новый исполнитель является правопреемником Исполнителя по контракту вследствие реорганизации юридического лица в форме преобразования, слияния или присоединения.",
   814	      "status_reason": "Aligned in substance. Both prohibit assignment except for reorganization. Contract is more specific about reorganization forms (transformation, merger, accession) and only addresses Contractor substitution (not Customer). Matrix covers both parties. The 44-FZ regime also restricts Customer substitution.",
   815	      "risk_level": "none",
   816	      "discrepancies": []
   817	    },
   818	    {
   819	      "matrix_ids": [
   820	        "11.10"
   821	      ],
   822	      "contract_ids": [
   823	        "12.1",
   824	        "12.2"
   825	      ],
   826	      "relationship": "aligned",
   827	      "legal_topic": "Succession upon reorganization; claims against liquidated party",
   828	      "matrix_standard": "In case of reorganization of one of the Parties, obligations under the Contract pass in full to the legal successor. In case of liquidation of one of the Parties, property claims of the other Party shall be satisfied from the property of the liquidated Party in accordance with RF legislation.",
   829	      "contract_position": "Contractor substitution permitted only for legal succession via reorganization (transformation, merger, accession). In case of Customer substitution, rights and obligations pass to the new Customer in the same scope and on the same terms.",
   830	      "matrix_evidence": "В случае реорганизации одной из Сторон обязательства по Договору в полном объеме переходят к правопреемнику. В случае ликвидации одной из Сторон имущественные требования другой Стороны удовлетворяются за счет имущества ликвидируемой Стороны в установленном законодательством РФ порядке",
   831	      "contract_evidence": "12.1-12.2: перемена Исполнителя... вследствие реорганизации юридического лица в форме преобразования, слияния или присоединения. В случае перемены Заказчика по контракту права и обязанности Заказчика... переходят к новому Заказчику в том же объеме и на тех же условиях.",
   832	      "status_reason": "Aligned in substance. Both provide for succession upon reorganization. The contract does not explicitly address liquidation claims but this is governed by general Russian civil law.",
   833	      "risk_level": "none",
   834	      "discrepancies": []
   835	    },
   836	    {
   837	      "matrix_ids": [
   838	        "11.12"
   839	      ],
   840	      "contract_ids": [
   841	        "10.1"
   842	      ],
   843	      "relationship": "aligned",
   844	      "legal_topic": "Notices and requests deemed properly sent if sent per clause 2.3",
   845	      "matrix_standard": "All notifications and requests under the Contract, except where the Contract provides a different procedure, are considered duly sent to the other Party if sent in accordance with clause 2.3 of the Contract.",
   846	      "contract_position": "Any notification that one Party sends to the other Party in accordance with the Contract shall be sent in writing, by registered mail or delivered personally to the legal (postal) addresses of the other Party with confirmation of receipt. For 44-FZ electronic procedures, exchange via EIS with UKEP.",
   847	      "matrix_evidence": "Все уведомления и запросы по Договору, за исключением случаев, когда Договором предусмотрен иной порядок их направления, считаются направленными надлежащим образом другой Стороне, если они направлены в соответствии с п. 2.3 Договора",
   848	      "contract_evidence": "10.1: Любое уведомление, которое одна Сторона направляет другой Стороне в соответствии с Контрактом, высылается в письменном виде, заказным письмом или доставляется лично по юридическим (почтовым) адресам другой Стороны с подтверждением о получении.",
   849	      "status_reason": "Both establish that notices are properly sent when following specified channels. Matrix references its clause 2.3 (multiple channels including email, DBO, EIS, etc.). Contract specifies written form, registered mail, or personal delivery, plus EIS for 44-FZ matters. The contract's notice channels are narrower than the matrix's multi-channel approach, but the contract's clause 2.3 already provides the same multi-channel framework.",
   850	      "risk_level": "none",
   851	      "discrepancies": []
   852	    },
   853	    {
   854	      "matrix_ids": [
   855	        "11.13"
   856	      ],
   857	      "contract_ids": [
   858	        "12.5"
   859	      ],
   860	      "relationship": "aligned",
   861	      "legal_topic": "List of appendices to the Contract",
   862	      "matrix_standard": "The following are attached to this Contract: 1) Appendix No. 1 — Enterprise Application for settlements; 2) Appendix No. 1.1 — Information about TST/Enterprise Resource; 3) Appendix No. 2 — Act of transfer of Operation amounts to Enterprise; Appendix No. 3 — Description of services forming tariffs and service parameters for Smart-terminals.",
   863	      "contract_position": "Appendices: No. 1 'Technical Assignment', No. 2 'Specification'. Additionally, the contract includes Appendix No. 1.1 (Enterprise Application) and Appendix No. 1.2 (Information about TST) in the text.",
   864	      "matrix_evidence": "К настоящему Договору прилагаются: 1) Приложение № 1 – Заявление Предприятия... 2) Приложение № 1.1 – Информация о Торгово-Сервисной Точке... 3) Приложение № 2 – Акт о перечислении Предприятию сумм операций по картам. Приложение № 3 – Описание услуг, формирующих тарифы и параметры сервиса для Смарт-терминалов",
   865	      "contract_evidence": "12.5: Приложения: № 1 «Техническое задание», № 2 «Спецификация». Also includes Приложение № 1.1 (Заявление) and Приложение № 1.2 (Информация о ТСТ) in the contract body.",
   866	      "status_reason": "Both list appendices. The specific appendices differ in content and numbering due to the different contract structure (44-FZ procurement vs. standard Bank acquiring contract). The contract has Technical Assignment and Specification as its primary appendices, while the matrix has Enterprise Application, TST Information, and Fund Transfer Act. The contract also includes the Enterprise Application (Appendix 1.1) and TST Information (Appendix 1.2) forms within its text. This is a structural difference inherent to the 44-FZ format.",
   867	      "risk_level": "none",
   868	      "discrepancies": []
   869	    }
   870	  ],
   871	  "unmatched_matrix": [
   872	    {
   873	      "matrix_id": "7.9",
   874	      "requirement": "Bank not liable for transfer delays not caused by Bank",
   875	      "source_evidence": "Банк не несет ответственности за задержки перевода денежных средств на счет Предприятия, если задержки произошли не по вине Банка.",
   876	      "status": "missing_in_contract",
   877	      "required_type": "optional",
   878	      "applicability": "applicable",
   879	      "risk_level": "low",
   880	      "risk": "No direct analogue found in contract. The contract's force majeure clause (9.1) covers extraordinary circumstances but does not specifically address Bank's non-liability for transfer delays not caused by Bank. The general liability clause (7.1) references legislation but does not contain this specific exclusion.",
   881	      "rejected_candidates": []
   882	    },
   883	    {
   884	      "matrix_id": "7.10",
   885	      "requirement": "Bank not liable for non-performance due to third party actions",
   886	      "source_evidence": "Банк не несет ответственности за неисполнение условий Договора, обусловленное действиями или бездействиями третьих лиц, в том числе участниками Платежной системы",
   887	      "status": "missing_in_contract",
   888	      "required_type": "optional",
   889	      "applicability": "applicable",
   890	      "risk_level": "low",
   891	      "risk": "No direct analogue found. Contract's force majeure clause (9.1) lists specific extraordinary events but does not include third-party actions generally. The general liability provisions do not contain this specific exclusion for Payment System participants.",
   892	      "rejected_candidates": []
   893	    },
   894	    {
   895	      "matrix_id": "7.11",
   896	      "requirement": "Bank not liable for delayed transfer during investigation of suspicious operations",
   897	      "source_evidence": "Банк не несет ответственности за несвоевременное перечисление сумм Операций по причине проведения расследования Банком при подозрении на проведение Операции с нарушением условий Договора",
   898	      "status": "missing_in_contract",
   899	      "required_type": "optional",
   900	      "applicability": "applicable",
   901	      "risk_level": "low",
   902	      "risk": "No direct analogue found. Contract gives Bank the right to suspend authorization (5.2.9) and withhold amounts (5.2.10) but does not explicitly exclude Bank liability for transfer delays during investigations.",
   903	      "rejected_candidates": []
   904	    },
   905	    {
   906	      "matrix_id": "7.12",
   907	      "requirement": "Bank not liable when Contract Price is exceeded",
   908	      "source_evidence": "Банк не несет ответственности в случае превышения установленной Цены Договора",
   909	      "status": "missing_in_contract",
   910	      "required_type": "optional",
   911	      "applicability": "applicable",
   912	      "risk_level": "low",
   913	      "risk": "No direct analogue found. Contract defines maximum price (3.1) and states services end when price is exhausted (4.1, 11.1), but does not explicitly exclude Bank liability for price exceedance.",
   914	      "rejected_candidates": []
   915	    },
   916	    {
   917	      "matrix_id": "7.14",
   918	      "requirement": "Enterprise liability for all actions in SPEP (special payment acceptance system)",
   919	      "source_evidence": "Предприятие несет ответственность за все действия, осуществляемые Предприятием/ТСТ в СПЭП",
   920	      "status": "missing_in_contract",
   921	      "required_type": "mandatory",
   922	      "applicability": "applicable",
   923	      "risk_level": "low",
   924	      "risk": "SPEP (СПЭП) is a system specific to internet acquiring. Since this contract is trade acquiring only, this matrix item is filtered as not applicable. However, the applicability filter shows it as applicable (product=common). Re-checking: the matrix item 7.14 has only_for_product=common, so it passes the product filter. But the concept of СПЭП relates to internet acquiring. No contract analogue exists for this specific system-based liability.",
   925	      "rejected_candidates": []
   926	    },
   927	    {
   928	      "matrix_id": "7.15",
   929	      "requirement": "Enterprise fully liable for personnel actions violating contract and Bank instructions",
   930	      "source_evidence": "Предприятие полностью несет ответственность за действия своего персонала, связанные с нарушением условий Договора и инструктивных материалов, предоставленных Банком",
   931	      "status": "missing_in_contract",
   932	      "required_type": "mandatory",
   933	      "applicability": "applicable",
   934	      "risk_level": "low",
   935	      "risk": "Per matrix main_idea: 'Важен сам факт несения ответственности, если в договоре не говорится про несение ответственности за действия персонала, значит этот пункт не относится к данному' — if the contract does not mention liability for personnel actions, this item does not apply. The contract does not contain an explicit clause making the Customer liable for personnel actions violating Bank instructions. However, general liability principles under Russian civil law would cover this.",
   936	      "rejected_candidates": []
   937	    },
   938	    {
   939	      "matrix_id": "7.17",
   940	      "requirement": "Enterprise financial liability for non-compliant Recurring Payments",
   941	      "source_evidence": "Предприятие несет полную финансовую ответственность перед Банком в случае несоответствия проведенных Повторяющихся платежей требованиям законодательства Российской Федерации, в том числе нормативных актов Банка России, правил Платежной системы и (или) Договора",
   942	      "status": "missing_in_contract",
   943	      "required_type": "mandatory",
   944	      "applicability": "applicable",
   945	      "risk_level": "medium",
   946	      "risk": "Per matrix main_idea: 'Важно, чтобы в договоре не было сужения ответственности.' The contract does not contain a specific clause on Enterprise liability for non-compliant Recurring Payments. The contract defines 'Повторяющиеся платежи' (recurring payments) in clause 2.1.17 but does not assign specific liability for non-compliance. The general liability provisions (Section 7) would apply but do not specifically address this risk.",
   947	      "rejected_candidates": []
   948	    },
   949	    {
   950	      "matrix_id": "10.3",
   951	      "requirement": "Post-termination settlement within 18 months",
   952	      "source_evidence": "При расторжении настоящего Договора Банком в одностороннем внесудебном порядке в случаях, предусмотренных п. 5.1.8. настоящего Договора, Договор считается расторгнутым с даты, указанной в письменном уведомлении Банка о расторжении. Стороны осуществляют расчеты/взаиморасчеты в течение 18 (восемнадцать) месяцев с даты расторжения Договора.",
   953	      "status": "missing_in_contract",
   954	      "required_type": "mandatory",
   955	      "applicability": "applicable",
   956	      "risk_level": "high",
   957	      "risk": "No direct analogue found. The contract does not contain an 18-month post-termination settlement period. The contract's termination provisions (Section 11) reference 44-FZ procedures but do not specify a post-termination settlement window. This is a significant gap for the Bank's ability to resolve outstanding payments after termination.",
   958	      "rejected_candidates": []
   959	    },
   960	    {
   961	      "matrix_id": "11.2",
   962	      "requirement": "Confidentiality of card numbers, personal data, transaction amounts",
   963	      "source_evidence": "Информация, полученная Предприятием в рамках исполнения Договора (номера Карт/Платежных счетов, персональные данные Покупателей, суммы Операций, информация о платеже), является конфиденциальной и не подлежит передаче третьим лицам, за исключением случаев, предусмотренных действующим законодательством РФ или условиями Договором.",
   964	      "status": "missing_in_contract",
   965	      "required_type": "optional",
   966	      "applicability": "applicable",
   967	      "risk_level": "medium",
   968	      "risk": "No direct analogue found. The contract has a personal data processing clause (5.1.9, 5.3.20) but these address the Bank's/Contractor's obligations, not the Customer's confidentiality obligations regarding card numbers and transaction data. The contract does not explicitly make card numbers, transaction amounts, and payment information confidential.",
   969	      "rejected_candidates": []
   970	    },
   971	    {
   972	      "matrix_id": "11.3",
   973	      "requirement": "Non-disclosure of card security features, transaction technology, financial information",
   974	      "source_evidence": "Стороны обязуются не разглашать полученные в ходе исполнения Договора сведения, включая: описание защитных элементов Карт; технологию проведения Операций; информацию об управлении, финансовой и иной деятельности Сторон; иную информацию, разглашение которой может привести к возникновению убытков или негативно повлиять на деловую репутацию Сторон.",
   975	      "status": "missing_in_contract",
   976	      "required_type": "optional",
   977	      "applicability": "applicable",
   978	      "risk_level": "medium",
   979	      "risk": "No direct analogue found. The contract does not contain a comprehensive confidentiality clause covering card security features, transaction technology, or financial information of the parties. The anti-corruption clause (Section 6) and personal data provisions are narrower in scope.",
   980	      "rejected_candidates": []
   981	    },
   982	    {
   983	      "matrix_id": "11.5",
   984	      "requirement": "Prior agreements superseded by the Contract",
   985	      "source_evidence": "Все имевшие место до подписания настоящего Договора соглашения, переговоры и переписка между Сторонами по вопросам, изложенным в настоящем Договоре, утрачивают силу с даты подписания настоящего Договора.",
   986	      "status": "missing_in_contract",
   987	      "required_type": "optional",
   988	      "applicability": "applicable",
   989	      "risk_level": "low",
   990	      "risk": "No direct analogue found. This is a standard merger/integration clause. Its absence does not create material risk since the contract itself supersedes prior agreements as a matter of contract law, but explicit language is preferable.",
   991	      "rejected_candidates": []
   992	    },
   993	    {
   994	      "matrix_id": "11.8",
   995	      "requirement": "Enterprise warranty that goods/services are sold in compliance with RF law",
   996	      "source_evidence": "Предприятие заверяет, что реализация Товаров/услуг в ТСТ осуществляется в соответствии с требованиями действующего законодательства РФ",
   997	      "status": "missing_in_contract",
   998	      "required_type": "optional",
   999	      "applicability": "applicable",
  1000	      "risk_level": "low",
  1001	      "risk": "No direct analogue found. The contract does not contain an explicit warranty from the Customer that its goods/services comply with Russian law. This is a representation/warranty that could be important for the Bank's reputational and compliance risk.",
  1002	      "rejected_candidates": []
  1003	    },
  1004	    {
  1005	      "matrix_id": "11.11",
  1006	      "requirement": "Instructional materials on Bank website become binding next working day after posting",
  1007	      "source_evidence": "Инструктивные материалы, касающиеся предмета Договора, включая документы, ссылки на которые даются в настоящем Договоре, размещенные на Официальном сайте Банка, становятся обязательными к исполнению со следующего рабочего дня за днем размещения их на Официальном сайте Банка: https://www.sberbank.ru, если не указаны иные сроки ввода их в действие",
  1008	      "status": "missing_in_contract",
  1009	      "required_type": "optional",
  1010	      "applicability": "applicable",
  1011	      "risk_level": "medium",
  1012	      "risk": "No direct analogue found. Per matrix main_idea: 'Если в договоре не указан сайт - это не является разногласием' — if the website is not specified in the contract, this is not a discrepancy. The contract does not contain a mechanism for Bank's instructional materials posted on its website to become automatically binding. This limits the Bank's ability to update operational procedures unilaterally.",
  1013	      "rejected_candidates": []
  1014	    }
  1015	  ],
  1016	  "unmatched_contract": [
  1017	    {
  1018	      "contract_id": "5.2.9",
  1019	      "contract_position": "Bank right to unilaterally suspend Authorization and/or terminate Contract for 11 specified events including: contract breach, extremism/terrorism lists, money laundering suspicion, negative government/Payment System information, fraud in TST, TST renovation, Customer liquidation/bankruptcy, false information, activity mismatch, 30-day inactivity, price exhaustion/contract expiry.",
  1020	      "source_evidence": "5.2.9: В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению Контракта при наступлении следующих событий: 5.2.9.1-5.2.9.11",
  1021	      "status": "extra_in_contract",
  1022	      "risk_level": "low",
  1023	      "risk": "Contract provides detailed grounds for Bank to suspend authorization and terminate. This is more specific than the matrix's general termination provisions. The detailed grounds are beneficial to the Bank as they provide clear contractual authority for suspension/termination in specific risk scenarios.",
  1024	      "materiality_reason": "Creates specific Bank rights to suspend authorization and terminate for enumerated risk events including fraud, money laundering, and regulatory concerns. These are operationally significant rights not enumerated in the matrix."
  1025	    },
  1026	    {
  1027	      "contract_id": "5.2.10",
  1028	      "contract_position": "Bank right to withhold from amounts payable to Customer: invalid operation amounts (with 11 specific grounds), erroneously transferred amounts, return/chargeback/reversal amounts, disputed amounts debited by issuing bank per Payment System rules, fines and losses from Payment System sanctions or government penalties due to Customer's non-performance.",
  1029	      "source_evidence": "5.2.10: Удерживать из сумм, подлежащих перечислению Заказчику по Контракту, следующие суммы: 5.2.10.1-5.2.10.5",
  1030	      "status": "extra_in_contract",
  1031	      "risk_level": "low",
  1032	      "risk": "Contract provides detailed Bank withholding rights with specific grounds. This is more comprehensive than the matrix's general provisions and is beneficial to the Bank. The detailed enumeration of withholdable amounts strengthens the Bank's position.",
  1033	      "materiality_reason": "Creates specific Bank rights to withhold amounts for 11 categories of invalid operations plus chargebacks, reversals, fines, and Payment System sanctions. These are operationally critical rights."
  1034	    },
  1035	    {
  1036	      "contract_id": "5.3.19",
  1037	      "contract_position": "Customer obligation to reimburse Contractor in full and unconditionally for: funds debited from Contractor per Payment System rules for disputed operations; funds debited for invalid operations per Contract; costs of dispute resolution between Buyers and Customer; losses from fines/sanctions applied to Contractor due to Customer's non-performance.",
  1038	      "source_evidence": "5.3.19: Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере: средств, которые... были списаны со счета Исполнителя... по Операциям ставшим предметом каких-либо споров... убытков, возникших у Исполнителя в результате применения к нему штрафных санкций",
  1039	      "status": "extra_in_contract",
  1040	      "risk_level": "low",
  1041	      "risk": "Comprehensive indemnity from Customer to Bank for disputed operations, Payment System debits, and regulatory fines. This is strongly protective of the Bank and goes beyond the matrix's general liability provisions. Beneficial to the Bank.",
  1042	      "materiality_reason": "Creates broad, unconditional indemnity obligation covering Payment System chargebacks, dispute costs, and regulatory fines — a material risk allocation mechanism not present in the matrix."
  1043	    },
  1044	    {
  1045	      "contract_id": "5.7",
  1046	      "contract_position": "Customer penalty for non-return of equipment: 10,000 RUB per Electronic terminal, 25,000 RUB per Smart-terminal (including VAT).",
  1047	      "source_evidence": "5.7: В случае невозврата Электронных терминалов/Смарт-терминалов Исполнителя Заказчик обязан уплатить Исполнителю штраф в размере 10 000 рублей... за каждый Электронный терминал, в размере 25 000 рублей... за каждый Смарт-терминал Банка.",
  1048	      "status": "extra_in_contract",
  1049	      "risk_level": "low",
  1050	      "risk": "Specific penalty for equipment non-return. This is beneficial to the Bank as it creates a clear, liquidated damages mechanism for unreturned terminals. Low risk to Bank.",
  1051	      "materiality_reason": "Creates specific liquidated damages for equipment non-return — a material remedy not present in the matrix."
  1052	    },
  1053	    {
  1054	      "contract_id": "7.8",
  1055	      "contract_position": "Exchange of documents for liability measures and other actions related to breach shall use EIS with electronic notifications signed with UKEP, placed in EIS without publication on the official website.",
  1056	      "source_evidence": "7.8: В случае обмена документами при применении мер ответственности и совершении иных действий в связи с нарушением Исполнителем или Заказчиком условий Контракта, такой обмен осуществляется с использованием ЕИС путем направления электронных уведомлений.",
  1057	      "status": "extra_in_contract",
  1058	      "risk_level": "low",
  1059	      "risk": "44-FZ specific requirement for EIS-based exchange of liability-related documents. This is a procedural requirement inherent to the 44-FZ regime. Low risk — standard for 44-FZ contracts.",
  1060	      "materiality_reason": "Mandates EIS as the exclusive channel for liability-related document exchange — a procedural requirement specific to 44-FZ procurement regime."
  1061	    },
  1062	    {
  1063	      "contract_id": "7.12",
  1064	      "contract_position": "In case of contract termination due to unilateral refusal, the other Party may demand compensation only for actually incurred damage directly caused by circumstances forming the basis for the unilateral refusal decision, beyond accrued penalties.",
  1065	      "source_evidence": "7.12: В случае расторжения Контракта в связи с односторонним отказом Стороны от исполнения Контракта другая Сторона вправе потребовать возмещения только фактически понесенного ущерба, непосредственно обусловленного обстоятельствами, являющимися основанием для принятия решения об одностороннем отказе от исполнения Контракта сверх начисленных неустоек.",
  1066	      "status": "extra_in_contract",
  1067	      "risk_level": "medium",
  1068	      "risk": "Limits damages upon unilateral termination to actual damage directly caused by the termination grounds, beyond accrued penalties. This could limit the Bank's recovery in a termination scenario compared to full damages under general contract law.",
  1069	      "materiality_reason": "Creates a damage limitation for unilateral termination scenarios — restricts recovery to actual damage directly caused by termination grounds, potentially limiting Bank's remedies."
  1070	    },
  1071	    {
  1072	      "contract_id": "8.3",
  1073	      "contract_position": "Detailed 44-FZ acceptance procedure: monthly EIS document generation by 10th working day, UKEP signature, specific required content (IKZ, service name, volume, cost, unit price), attachment of invoice and fund transfer act. Priority of EIS document information over attached documents.",
  1074	      "source_evidence": "8.3-8.11: Detailed acceptance procedure with EIS, UKEP, specific content requirements, timelines, expert review, and correction mechanisms.",
  1075	      "status": "extra_in_contract",
  1076	      "risk_level": "low",
  1077	      "risk": "44-FZ statutory acceptance procedure. This is more detailed than the matrix's simple UPD exchange. The procedure is mandatory for 44-FZ contracts and provides structured acceptance with clear timelines. Low risk — standard 44-FZ mechanism.",
  1078	      "materiality_reason": "Comprehensive 44-FZ acceptance procedure with EIS integration, expert review rights, and correction mechanisms — a material procedural framework not present in the matrix."
  1079	    },
  1080	    {
  1081	      "contract_id": "11.6",
  1082	      "contract_position": "Contract amendment and/or termination shall be carried out in accordance with the procedure, timelines, cases and conditions established by Articles 34, 95, 96, 112 of Federal Law No. 44-FZ.",
  1083	      "source_evidence": "11.6: Изменение и(или) расторжение контракта осуществляется в порядке, сроки, случаях и на условиях, установленных статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ.",
  1084	      "status": "extra_in_contract",
  1085	      "risk_level": "low",
  1086	      "risk": "44-FZ statutory reference for amendment and termination procedures. This is standard for 44-FZ contracts and provides the legal framework for contract changes. Low risk — mandatory under 44-FZ.",
  1087	      "materiality_reason": "Incorporates 44-FZ statutory amendment/termination regime by reference — a material legal framework not present in the matrix."
  1088	    },
  1089	    {
  1090	      "contract_id": "11.8",
  1091	      "contract_position": "Parties have stipulated that changes to essential contract terms during performance are not permitted, except by agreement of the Parties in cases provided by Federal Law No. 44-FZ.",
  1092	      "source_evidence": "11.8: Стороны предусмотрели, что изменение существенных условий контракта при его исполнении не допускается, за исключением их изменения по соглашению Сторон в случаях, предусмотренных Федеральным законом № 44-ФЗ.",
  1093	      "status": "extra_in_contract",
  1094	      "risk_level": "medium",
  1095	      "risk": "44-FZ restriction on changing essential terms. This limits flexibility to adjust key contract terms (price, scope, timeline) during performance. Could constrain the Bank if operational adjustments are needed.",
  1096	      "materiality_reason": "Statutory prohibition on changing essential contract terms except in specific 44-FZ cases — a material restriction on contract flexibility."
  1097	    },
  1098	    {
  1099	      "contract_id": "12.3",
  1100	      "contract_position": "During contract performance, by agreement between Customer and Contractor, provision of services with improved quality, technical and functional characteristics compared to those specified in the contract is permitted.",
Tool:    601	      "discrepancies": [
   602	        {
   603	          "type": "procedure",
   604	          "description": "Способ уведомления изменен с публикации на Официальном сайте Банка на письменное уведомление в адрес Заказчика в течение 3 рабочих дней.",
   605	          "risk": "Низкий риск: письменное уведомление является более формальным, но создает дополнительную административную нагрузку на Банк. Матричный пункт optional."
   606	        }
   607	      ]
   608	    },
   609	    {
   610	      "matrix_ids": [
   611	        "5.1.14"
   612	      ],
   613	      "contract_ids": [
   614	        "5.2.7"
   615	      ],
   616	      "relationship": "aligned",
   617	      "legal_topic": "Право Банка направлять запросы на адрес электронной почты Предприятия",
   618	      "matrix_standard": "Банк имеет право направлять запросы на адрес электронной почты Предприятия/ТСТ, указанный в Заявлении Предприятия на проведение расчетов/Информации о ТСТ, в целях получения информации по Операциям.",
   619	      "contract_position": "Пункт 5.2.7: В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении заказчика на проведение расчетов по операциям с использованием банковских карт/информации о ТСТ.",
   620	      "matrix_evidence": "«Банк имеет право: → В целях получения информации по Операциям направлять запросы на адрес электронной почты Предприятия/ТСТ, указанный в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг/Информации о ТСТ.» (матрица 5.1.14)",
   621	      "contract_evidence": "«В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении заказчика на проведение расчетов по операциям с использованием банковских карт/информации о ТСТ» (п. 5.2.7 Контракта)",
   622	      "status_reason": "Прямой аналог: право Банка направлять запросы на email Заказчика для получения информации по операциям полностью сохранено.",
   623	      "risk_level": "none",
   624	      "discrepancies": []
   625	    },
   626	    {
   627	      "matrix_ids": [
   628	        "5.1.16"
   629	      ],
   630	      "contract_ids": [
   631	        "5.2.8"
   632	      ],
   633	      "relationship": "aligned",
   634	      "legal_topic": "Право Банка требовать предоставления документов и сведений для осуществления функций по законодательству",
   635	      "matrix_standard": "Банк имеет право требовать от Предприятия предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.",
   636	      "contract_position": "Пункт 5.2.8: Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.",
   637	      "matrix_evidence": "«Банк имеет право: → Требовать от Предприятия предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.» (матрица 5.1.16)",
   638	      "contract_evidence": "«Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства» (п. 5.2.8 Контракта)",
   639	      "status_reason": "Прямой аналог: право Банка требовать документы и сведения для выполнения законодательных функций полностью сохранено.",
   640	      "risk_level": "none",
   641	      "discrepancies": []
   642	    }
   643	  ],
   644	  "atomic_links": [
   645	    {
   646	      "matrix_id": "4.2.18",
   647	      "contract_id": "5.3.16",
   648	      "relationship": "aligned",
   649	      "link_index": 0,
   650	      "coverage_role": "direct",
   651	      "coverage": "Прямая обязанность прекратить прием карт и снять информационные материалы с даты расторжения"
   652	    },
   653	    {
   654	      "matrix_id": "4.2.19",
   655	      "contract_id": "5.3.17",
   656	      "relationship": "aligned",
   657	      "link_index": 1,
   658	      "coverage_role": "direct",
   659	      "coverage": "Прямая обязанность не препятствовать проверкам и содействовать расследованиям"
   660	    },
   661	    {
   662	      "matrix_id": "4.2.20.1",
   663	      "contract_id": "5.10",
   664	      "relationship": "deviation",
   665	      "link_index": 2,
   666	      "coverage_role": "direct",
   667	      "coverage": "Обязанность проведения инструктажа сохранена, но адрес сайта не заполнен"
   668	    },
   669	    {
   670	      "matrix_id": "4.2.20.2",
   671	      "contract_id": "5.3.18.1",
   672	      "relationship": "aligned",
   673	      "link_index": 3,
   674	      "coverage_role": "direct",
   675	      "coverage": "Все четыре обязанности по использованию терминалов и ПО полностью сохранены"
   676	    },
   677	    {
   678	      "matrix_id": "4.2.20.3",
   679	      "contract_id": "5.3.18.2",
   680	      "relationship": "aligned",
   681	      "link_index": 4,
   682	      "coverage_role": "direct",
   683	      "coverage": "Обязанность предоставлять доступ для всех видов обслуживания сохранена"
   684	    },
   685	    {
   686	      "matrix_id": "4.2.20.4",
   687	      "contract_id": "5.3.18.3",
   688	      "relationship": "deviation",
   689	      "link_index": 5,
   690	      "coverage_role": "direct",
   691	      "coverage": "Приемка по акту сохранена, но отсутствует ссылка на форму акта на сайте Банка"
   692	    },
   693	    {
   694	      "matrix_id": "4.2.20.5",
   695	      "contract_id": "5.3.20.4",
   696	      "relationship": "deviation",
   697	      "link_index": 6,
   698	      "coverage_role": "direct",
   699	      "coverage": "Обязанность информирования сохранена, но без указания конкретных каналов связи"
   700	    },
   701	    {
   702	      "matrix_id": "4.2.20.6",
   703	      "contract_id": "5.3.18.5",
   704	      "relationship": "aligned",
   705	      "link_index": 7,
   706	      "coverage_role": "direct",
   707	      "coverage": "Срок 5 рабочих дней и альтернативные основания возврата сохранены"
   708	    },
   709	    {
   710	      "matrix_id": "4.2.20.6",
   711	      "contract_id": "5.6",
   712	      "relationship": "aligned",
   713	      "link_index": 7,
   714	      "coverage_role": "direct",
   715	      "coverage": "Дублирующая обязанность возврата терминалов в течение 5 рабочих дней"
   716	    },
   717	    {
   718	      "matrix_id": "4.2.20.7",
   719	      "contract_id": "5.7",
   720	      "relationship": "deviation",
   721	      "link_index": 8,
   722	      "coverage_role": "direct",
   723	      "coverage": "Штраф за невозврат: сумма за Электронный терминал снижена с 25 000 до 10 000 руб."
   724	    },
   725	    {
   726	      "matrix_id": "4.2.22",
   727	      "contract_id": "Приложение_№1_п5",
   728	      "relationship": "deviation",
   729	      "link_index": 9,
   730	      "coverage_role": "context",
   731	      "coverage": "QR-код упомянут как техническая характеристика терминала, но не как обязанность Заказчика"
   732	    },
   733	    {
   734	      "matrix_id": "5.1.1.1",
   735	      "contract_id": "5.2.10.1",
   736	      "relationship": "aligned",
   737	      "link_index": 10,
   738	      "coverage_role": "direct",
   739	      "coverage": "Все 12 оснований для удержания недействительных операций сохранены"
   740	    },
   741	    {
   742	      "matrix_id": "5.1.1.2",
   743	      "contract_id": "5.2.10.2",
   744	      "relationship": "aligned",
   745	      "link_index": 11,
   746	      "coverage_role": "direct",
   747	      "coverage": "Право удержания ошибочно перечисленных сумм сохранено"
   748	    },
   749	    {
   750	      "matrix_id": "5.1.1.3",
   751	      "contract_id": "5.2.10.3",
   752	      "relationship": "aligned",
   753	      "link_index": 12,
   754	      "coverage_role": "direct",
   755	      "coverage": "Все три категории удерживаемых сумм сохранены"
   756	    },
   757	    {
   758	      "matrix_id": "5.1.1.4",
   759	      "contract_id": "5.2.10.4",
   760	      "relationship": "deviation",
   761	      "link_index": 13,
   762	      "coverage_role": "direct",
   763	      "coverage": "Право удержания оспоренных операций сохранено, но без SberPay/Плати QR"
   764	    },
   765	    {
   766	      "matrix_id": "5.1.1.5",
   767	      "contract_id": "5.2.10.5",
   768	      "relationship": "aligned",
   769	      "link_index": 14,
   770	      "coverage_role": "direct",
   771	      "coverage": "Право удержания штрафов и убытков по вине Заказчика сохранено"
   772	    },
   773	    {
   774	      "matrix_id": "5.1.3",
   775	      "contract_id": "Заявление_п1.3",
   776	      "relationship": "deviation",
   777	      "link_index": 15,
   778	      "coverage_role": "direct",
   779	      "coverage": "Заранее данный акцепт на списание сохранен, но ограничен счетом в Банке"
   780	    },
   781	    {
   782	      "matrix_id": "5.1.6",
   783	      "contract_id": "5.2.3",
   784	      "relationship": "aligned",
   785	      "link_index": 16,
   786	      "coverage_role": "direct",
   787	      "coverage": "Право проверки, замены и обновления ПО с уведомлением за 2 дня сохранено"
   788	    },
   789	    {
   790	      "matrix_id": "5.1.6",
   791	      "contract_id": "5.2.4",
   792	      "relationship": "aligned",
   793	      "link_index": 16,
   794	      "coverage_role": "direct",
   795	      "coverage": "Право удаленного обновления ПО без уведомления сохранено"
   796	    },
   797	    {
   798	      "matrix_id": "5.1.7",
   799	      "contract_id": "5.3.20",
   800	      "relationship": "deviation",
   801	      "link_index": 17,
   802	      "coverage_role": "context",
   803	      "coverage": "Только согласие на передачу ПДн в ПС МИР, но не активное право Банка на информирование о мошенничестве"
   804	    },
   805	    {
   806	      "matrix_id": "5.1.8.1",
   807	      "contract_id": "5.2.9.1",
   808	      "relationship": "aligned",
   809	      "link_index": 18,
   810	      "coverage_role": "direct",
   811	      "coverage": "Основание: нарушение условий контракта"
   812	    },
   813	    {
   814	      "matrix_id": "5.1.8.2",
   815	      "contract_id": "5.2.9.2",
   816	      "relationship": "aligned",
   817	      "link_index": 19,
   818	      "coverage_role": "direct",
   819	      "coverage": "Основание: внесение в перечень экстремистов/террористов"
   820	    },
   821	    {
   822	      "matrix_id": "5.1.8.3",
   823	      "contract_id": "5.2.9.3",
   824	      "relationship": "aligned",
   825	      "link_index": 20,
   826	      "coverage_role": "direct",
   827	      "coverage": "Основание: подозрение на отмывание доходов/финансирование терроризма"
   828	    },
   829	    {
   830	      "matrix_id": "5.1.8.6",
   831	      "contract_id": "5.2.9.4",
   832	      "relationship": "aligned",
   833	      "link_index": 21,
   834	      "coverage_role": "direct",
   835	      "coverage": "Основание: негативная информация от госорганов/ПС"
   836	    },
   837	    {
   838	      "matrix_id": "5.1.8.7",
   839	      "contract_id": "5.2.9.5",
   840	      "relationship": "aligned",
   841	      "link_index": 22,
   842	      "coverage_role": "direct",
   843	      "coverage": "Основание: информация о мошенничестве со стандартом доказывания"
   844	    },
   845	    {
   846	      "matrix_id": "5.1.8.8",
   847	      "contract_id": "5.2.9.6",
   848	      "relationship": "aligned",
   849	      "link_index": 23,
   850	      "coverage_role": "direct",
   851	      "coverage": "Основание: ремонт помещений ТСТ"
   852	    },
   853	    {
   854	      "matrix_id": "5.1.8.9",
   855	      "contract_id": "5.2.9.7",
   856	      "relationship": "aligned",
   857	      "link_index": 24,
   858	      "coverage_role": "direct",
   859	      "coverage": "Основание: ликвидация/банкротство Заказчика"
   860	    },
   861	    {
   862	      "matrix_id": "5.1.8.10",
   863	      "contract_id": "5.2.9.8",
   864	      "relationship": "aligned",
   865	      "link_index": 25,
   866	      "coverage_role": "direct",
   867	      "coverage": "Основание: недостоверные сведения"
   868	    },
   869	    {
   870	      "matrix_id": "5.1.8.11",
   871	      "contract_id": "5.2.9.9",
   872	      "relationship": "aligned",
   873	      "link_index": 26,
   874	      "coverage_role": "direct",
   875	      "coverage": "Основание: несоответствие товаров/услуг роду деятельности"
   876	    },
   877	    {
   878	      "matrix_id": "5.1.8.12",
   879	      "contract_id": "5.2.9.10",
   880	      "relationship": "aligned",
   881	      "link_index": 27,
   882	      "coverage_role": "direct",
   883	      "coverage": "Основание: отсутствие операций 30 дней"
   884	    },
   885	    {
   886	      "matrix_id": "5.1.8.13",
   887	      "contract_id": "5.2.9.11",
   888	      "relationship": "aligned",
   889	      "link_index": 28,
   890	      "coverage_role": "direct",
   891	      "coverage": "Основание: исчерпание цены/окончание срока"
   892	    },
   893	    {
   894	      "matrix_id": "5.1.11",
   895	      "contract_id": "5.2.5",
   896	      "relationship": "deviation",
   897	      "link_index": 29,
   898	      "coverage_role": "direct",
   899	      "coverage": "Право запроса документов сохранено, но без указания каналов и сроков"
   900	    },
   901	    {
   902	      "matrix_id": "5.1.13",
   903	      "contract_id": "5.2.6",
   904	      "relationship": "deviation",
   905	      "link_index": 30,
   906	      "coverage_role": "direct",
   907	      "coverage": "Уведомление об изменении реквизитов: письменно вместо публикации на сайте"
   908	    },
   909	    {
   910	      "matrix_id": "5.1.14",
   911	      "contract_id": "5.2.7",
   912	      "relationship": "aligned",
   913	      "link_index": 31,
   914	      "coverage_role": "direct",
   915	      "coverage": "Право направлять запросы на email Заказчика сохранено"
   916	    },
   917	    {
   918	      "matrix_id": "5.1.16",
   919	      "contract_id": "5.2.8",
   920	      "relationship": "aligned",
   921	      "link_index": 32,
   922	      "coverage_role": "direct",
   923	      "coverage": "Право требовать документы для законодательных функций сохранено"
   924	    }
   925	  ],
   926	  "unmatched_matrix": [
   927	    {
   928	      "matrix_id": "4.2.17",
   929	      "requirement": "Обязанность Предприятия соблюдать PCI DSS и предоставлять подтверждение (аттестат/лист самооценки)",
   930	      "source_evidence": "«Обеспечить соблюдение требований Стандарта PCI DSS... и предоставлять по запросу Банка результаты проведения оценки соответствия в виде аттестата соответствия или листа самооценки на электронный адрес: pcidss@sberbank.ru.»",
   931	      "status": "missing_in_contract",
   932	      "required_type": "mandatory",
   933	      "applicability": "not_applicable",
   934	      "risk_level": "low",
   935	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
   936	      "rejected_candidates": []
   937	    },
   938	    {
   939	      "matrix_id": "4.2.21.1",
   940	      "requirement": "Приступить к проведению Операций на Ресурсе только после успешного завершения проверки на тестовой среде",
   941	      "source_evidence": "«Приступить к проведению Операций на Ресурсе только после успешного завершения проверки выбранных Предприятием/ТСТ Операций на тестовой среде.»",
   942	      "status": "missing_in_contract",
   943	      "required_type": "mandatory",
   944	      "applicability": "not_applicable",
   945	      "risk_level": "low",
   946	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
   947	      "rejected_candidates": []
   948	    },
   949	    {
   950	      "matrix_id": "4.2.21.2",
   951	      "requirement": "Соответствовать Требованиям Банка к Ресурсу Предприятия",
   952	      "source_evidence": "«Соответствовать Требованиям Банка к Ресурсу Предприятия, размещенным на Официальном сайте Банка.»",
   953	      "status": "missing_in_contract",
   954	      "required_type": "mandatory",
   955	      "applicability": "not_applicable",
   956	      "risk_level": "low",
   957	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
   958	      "rejected_candidates": []
   959	    },
   960	    {
   961	      "matrix_id": "4.2.21.3",
   962	      "requirement": "Подтверждать авторизованные суммы к списанию через СПЭП не позднее 5 календарных дней",
   963	      "source_evidence": "«Подтверждать авторизованные с использованием Предавторизации суммы к списанию через СПЭП не позднее 5 (пяти) календарных дней с даты совершения Операции...»",
   964	      "status": "missing_in_contract",
   965	      "required_type": "mandatory",
   966	      "applicability": "not_applicable",
   967	      "risk_level": "low",
   968	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
   969	      "rejected_candidates": []
   970	    },
   971	    {
   972	      "matrix_id": "4.2.21.4",
   973	      "requirement": "Согласовывать с Банком дизайн Платежной страницы и электронные варианты информационных наклеек",
   974	      "source_evidence": "«Согласовывать с Банком дизайн Платежной страницы, включая электронные варианты информационных наклеек.»",
   975	      "status": "missing_in_contract",
   976	      "required_type": "mandatory",
   977	      "applicability": "not_applicable",
   978	      "risk_level": "low",
   979	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
   980	      "rejected_candidates": []
   981	    },
   982	    {
   983	      "matrix_id": "4.2.21.5",
   984	      "requirement": "Провести мероприятия по интеграции Ресурса со СПЭП и интеграционные тесты в течение 30 календарных дней",
   985	      "source_evidence": "«Провести мероприятия по интеграции Ресурса со СПЭП и соответствующие интеграционные тесты в течение 30 (тридцати) календарных дней с даты заключения Договора.»",
   986	      "status": "missing_in_contract",
   987	      "required_type": "mandatory",
   988	      "applicability": "not_applicable",
   989	      "risk_level": "low",
   990	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
   991	      "rejected_candidates": []
   992	    },
   993	    {
   994	      "matrix_id": "4.2.21.6",
   995	      "requirement": "Самостоятельно обеспечивать безопасность своих информационных ресурсов в сети интернет",
   996	      "source_evidence": "«Самостоятельно обеспечивать безопасность своих информационных ресурсов в сети интернет.»",
   997	      "status": "missing_in_contract",
   998	      "required_type": "mandatory",
   999	      "applicability": "not_applicable",
  1000	      "risk_level": "low",
  1001	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
  1002	      "rejected_candidates": []
  1003	    },
  1004	    {
  1005	      "matrix_id": "4.2.21.7",
  1006	      "requirement": "Предоставлять по требованию Банка доступ к разделам Ресурса с ограниченным доступом",
  1007	      "source_evidence": "«Предоставлять по требованию Банка доступ к разделам Ресурса с ограниченным доступом, не связанным с администрированием и сопровождением (VIP, Оптовое, Клубное обслуживание, и т.п.).»",
  1008	      "status": "missing_in_contract",
  1009	      "required_type": "mandatory",
  1010	      "applicability": "not_applicable",
  1011	      "risk_level": "low",
  1012	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
  1013	      "rejected_candidates": []
  1014	    },
  1015	    {
  1016	      "matrix_id": "4.2.21.8",
  1017	      "requirement": "Соблюдать правила пользования Личным кабинетом Интернет-эквайринга",
  1018	      "source_evidence": "«Соблюдать правила пользования Личным кабинетом Интернет-эквайринга, размещенным на Официальном сайте Банка.»",
  1019	      "status": "missing_in_contract",
  1020	      "required_type": "mandatory",
  1021	      "applicability": "not_applicable",
  1022	      "risk_level": "low",
  1023	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
  1024	      "rejected_candidates": []
  1025	    },
  1026	    {
  1027	      "matrix_id": "4.2.23",
  1028	      "requirement": "Не изменять QR-код партнера в одностороннем порядке",
  1029	      "source_evidence": "«Предприятие обязуется: → Не изменять QR-код партнера в одностороннем порядке.»",
  1030	      "status": "missing_in_contract",
  1031	      "required_type": "optional",
  1032	      "applicability": "applicable",
  1033	      "risk_level": "low",
  1034	      "risk": "Пункт optional, payment_method=qr. QR включен в профиль контракта. Отсутствие данного ограничения создает незначительный риск.",
  1035	      "rejected_candidates": []
  1036	    },
  1037	    {
  1038	      "matrix_id": "4.2.24",
  1039	      "requirement": "Использовать API и сведения QR-API в границах прав и функциональных возможностей",
  1040	      "source_evidence": "«Использовать API и сведения, передаваемые посредством QR-API, в границах прав и функциональных возможностей такого API...»",
  1041	      "status": "missing_in_contract",
  1042	      "required_type": "optional",
  1043	      "applicability": "applicable",
  1044	      "risk_level": "low",
  1045	      "risk": "Пункт optional, payment_method=qr. QR включен в профиль. Отметка QR-API в Приложении №1 не раскрывает обязательств.",
  1046	      "rejected_candidates": [
  1047	        {
  1048	          "contract_id": "Приложение_№1_QR-API_checkbox",
  1049	          "reason": "Отметка (checkbox) «QR-API» в Приложении №1 является лишь указанием на тип подключения, а не операционной обязанностью."
  1050	        }
  1051	      ]
  1052	    },
  1053	    {
  1054	      "matrix_id": "4.2.25",
  1055	      "requirement": "Приостановить использование API при нарушении безопасности и оповестить Банк",
  1056	      "source_evidence": "«При выявлении фактов или признаков нарушения безопасности использования QR-API... немедленно приостановить использование API и оповестить об этом Банк...»",
  1057	      "status": "missing_in_contract",
  1058	      "required_type": "optional",
  1059	      "applicability": "applicable",
  1060	      "risk_level": "low",
  1061	      "risk": "Пункт optional, payment_method=qr. QR включен в профиль. Отсутствие процедуры реагирования на инциденты безопасности QR-API.",
  1062	      "rejected_candidates": []
  1063	    },
  1064	    {
  1065	      "matrix_id": "4.2.26",
  1066	      "requirement": "Обязанности Предприятия при проведении Повторяющихся платежей (размещение соглашения, получение согласия, отмена, прекращение)",
  1067	      "source_evidence": "«В дополнение к соблюдению требований... в целях осуществлении Повторяющихся платежей Предприятие обязано: размещать на Ресурсе пользовательское соглашение... получать от Держателя согласие...»",
  1068	      "status": "missing_in_contract",
  1069	      "required_type": "mandatory",
  1070	      "applicability": "not_applicable",
  1071	      "risk_level": "low",
  1072	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
  1073	      "rejected_candidates": []
  1074	    },
  1075	    {
  1076	      "matrix_id": "5.1.1.6",
  1077	      "requirement": "Право Банка удерживать штрафы за невозврат терминалов из сумм, подлежащих перечислению",
  1078	      "source_evidence": "«Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов в случае невозврата Электронных терминалов/Смарт-терминалов Банка...»",
  1079	      "status": "missing_in_contract",
  1080	      "required_type": "mandatory",
  1081	      "applicability": "applicable",
  1082	      "risk_level": "medium",
  1083	      "risk": "Контракт содержит обязанность уплаты штрафа (п. 5.7), но не содержит права Банка удержать этот штраф из сумм перечисления. Это ослабляет механизм взыскания.",
  1084	      "rejected_candidates": [
  1085	        {
  1086	          "contract_id": "5.7",
  1087	          "reason": "Пункт 5.7 содержит обязанность Заказчика уплатить штраф, но не право Банка удержать его из сумм перечисления — это разные правовые механизмы."
  1088	        }
  1089	      ]
  1090	    },
  1091	    {
  1092	      "matrix_id": "5.1.2",
  1093	      "requirement": "Право Банка приостановить Авторизацию при задолженности Предприятия до полного погашения",
  1094	      "source_evidence": "«Банк имеет право: → В случае возникновения у Предприятия задолженности перед Банком приостановить проведение Авторизации до момента полного погашения задолженности.»",
  1095	      "status": "missing_in_contract",
  1096	      "required_type": "mandatory",
  1097	      "applicability": "applicable",
  1098	      "risk_level": "high",
  1099	      "risk": "Отсутствие права приостановки авторизации при задолженности лишает Банк ключевого оперативного рычага воздействия на должника. Риск высокий.",
  1100	      "rejected_candidates": []
AI: Now let me see the rest of batch 4's unmatched_contract and also check the remaining contract text:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_4_output.json', 'offset': 1100, 'limit': 200}, 'id': 'call_00_xkyDKIEjS0AeW1e0ETOH2097', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_3_output.json', 'offset': 1100, 'limit': 200}, 'id': 'call_01_aGp1qr7cAn1AiPeCi0qW7700', 'type': 'tool_call'}]
Tool:   1101	      "source_evidence": "12.3: При исполнении контракта по согласованию Заказчика с Исполнителем допускается оказание услуги, качество, технические и функциональные характеристики (потребительские свойства) которых являются улучшенными по сравнению с качеством и соответствующими техническими и функциональными характеристиками, указанными в контракте.",
  1102	      "status": "extra_in_contract",
  1103	      "risk_level": "low",
  1104	      "risk": "44-FZ provision allowing improved services by agreement. This is beneficial as it permits service upgrades without formal amendment. Low risk.",
  1105	      "materiality_reason": "Allows service quality improvements by agreement — a flexibility mechanism specific to 44-FZ."
  1106	    }
  1107	  ],
  1108	  "atomic_links": [
  1109	    {
  1110	      "matrix_id": "5.2.3",
  1111	      "contract_id": "5.1.1",
  1112	      "relationship": "deviation",
  1113	      "link_index": 0,
  1114	      "coverage_role": "direct",
  1115	      "coverage": "Primary operative clause covering the matrix requirement"
  1116	    },
  1117	    {
  1118	      "matrix_id": "5.2.3",
  1119	      "contract_id": "Tech_5",
  1120	      "relationship": "deviation",
  1121	      "link_index": 0,
  1122	      "coverage_role": "appendix",
  1123	      "coverage": "Technical specification appendix providing operational details"
  1124	    },
  1125	    {
  1126	      "matrix_id": "5.2.4",
  1127	      "contract_id": "5.1.6",
  1128	      "relationship": "aligned",
  1129	      "link_index": 1,
  1130	      "coverage_role": "direct",
  1131	      "coverage": "Primary operative clause covering the matrix requirement"
  1132	    },
  1133	    {
  1134	      "matrix_id": "5.2.5",
  1135	      "contract_id": "5.1.1",
  1136	      "relationship": "deviation",
  1137	      "link_index": 2,
  1138	      "coverage_role": "direct",
  1139	      "coverage": "Primary operative clause covering the matrix requirement"
  1140	    },
  1141	    {
  1142	      "matrix_id": "5.2.5",
  1143	      "contract_id": "5.10",
  1144	      "relationship": "deviation",
  1145	      "link_index": 2,
  1146	      "coverage_role": "context",
  1147	      "coverage": "Supplementary clause providing additional coverage"
  1148	    },
  1149	    {
  1150	      "matrix_id": "5.2.6",
  1151	      "contract_id": "5.1.7",
  1152	      "relationship": "aligned",
  1153	      "link_index": 3,
  1154	      "coverage_role": "direct",
  1155	      "coverage": "Primary operative clause covering the matrix requirement"
  1156	    },
  1157	    {
  1158	      "matrix_id": "5.2.7",
  1159	      "contract_id": "5.1.4",
  1160	      "relationship": "aligned",
  1161	      "link_index": 4,
  1162	      "coverage_role": "direct",
  1163	      "coverage": "Primary operative clause covering the matrix requirement"
  1164	    },
  1165	    {
  1166	      "matrix_id": "5.2.8",
  1167	      "contract_id": "5.1.8",
  1168	      "relationship": "aligned",
  1169	      "link_index": 5,
  1170	      "coverage_role": "direct",
  1171	      "coverage": "Primary operative clause covering the matrix requirement"
  1172	    },
  1173	    {
  1174	      "matrix_id": "5.2.8",
  1175	      "contract_id": "Tech_5",
  1176	      "relationship": "aligned",
  1177	      "link_index": 5,
  1178	      "coverage_role": "appendix",
  1179	      "coverage": "Technical specification appendix providing operational details"
  1180	    },
  1181	    {
  1182	      "matrix_id": "5.2.9",
  1183	      "contract_id": "Tech_5",
  1184	      "relationship": "deviation",
  1185	      "link_index": 6,
  1186	      "coverage_role": "appendix",
  1187	      "coverage": "Technical specification appendix providing operational details"
  1188	    },
  1189	    {
  1190	      "matrix_id": "5.2.10",
  1191	      "contract_id": "5.1.9",
  1192	      "relationship": "aligned",
  1193	      "link_index": 7,
  1194	      "coverage_role": "direct",
  1195	      "coverage": "Primary operative clause covering the matrix requirement"
  1196	    },
  1197	    {
  1198	      "matrix_id": "6.1",
  1199	      "contract_id": "3.2",
  1200	      "relationship": "deviation",
  1201	      "link_index": 8,
  1202	      "coverage_role": "direct",
  1203	      "coverage": "Primary operative clause covering the matrix requirement"
  1204	    },
  1205	    {
  1206	      "matrix_id": "6.1",
  1207	      "contract_id": "Spec",
  1208	      "relationship": "deviation",
  1209	      "link_index": 8,
  1210	      "coverage_role": "appendix",
  1211	      "coverage": "Specification appendix providing price/volume details"
  1212	    },
  1213	    {
  1214	      "matrix_id": "6.2",
  1215	      "contract_id": "8.3.1",
  1216	      "relationship": "deviation",
  1217	      "link_index": 9,
  1218	      "coverage_role": "direct",
  1219	      "coverage": "Primary operative clause covering the matrix requirement"
  1220	    },
  1221	    {
  1222	      "matrix_id": "6.2",
  1223	      "contract_id": "8.3.2",
  1224	      "relationship": "deviation",
  1225	      "link_index": 9,
  1226	      "coverage_role": "context",
  1227	      "coverage": "Supplementary clause providing additional coverage"
  1228	    },
  1229	    {
  1230	      "matrix_id": "6.4",
  1231	      "contract_id": "8.5.1",
  1232	      "relationship": "deviation",
  1233	      "link_index": 10,
  1234	      "coverage_role": "direct",
  1235	      "coverage": "Primary operative clause covering the matrix requirement"
  1236	    },
  1237	    {
  1238	      "matrix_id": "6.4",
  1239	      "contract_id": "8.5.7",
  1240	      "relationship": "deviation",
  1241	      "link_index": 10,
  1242	      "coverage_role": "context",
  1243	      "coverage": "Supplementary clause providing additional coverage"
  1244	    },
  1245	    {
  1246	      "matrix_id": "6.5",
  1247	      "contract_id": "4.5",
  1248	      "relationship": "deviation",
  1249	      "link_index": 11,
  1250	      "coverage_role": "direct",
  1251	      "coverage": "Primary operative clause covering the matrix requirement"
  1252	    },
  1253	    {
  1254	      "matrix_id": "6.20",
  1255	      "contract_id": "Tech_5",
  1256	      "relationship": "aligned",
  1257	      "link_index": 12,
  1258	      "coverage_role": "appendix",
  1259	      "coverage": "Technical specification appendix providing operational details"
  1260	    },
  1261	    {
  1262	      "matrix_id": "6.21",
  1263	      "contract_id": "3.1",
  1264	      "relationship": "aligned",
  1265	      "link_index": 13,
  1266	      "coverage_role": "direct",
  1267	      "coverage": "Primary operative clause covering the matrix requirement"
  1268	    },
  1269	    {
  1270	      "matrix_id": "7.1",
  1271	      "contract_id": "7.1",
  1272	      "relationship": "aligned",
  1273	      "link_index": 14,
  1274	      "coverage_role": "direct",
  1275	      "coverage": "Primary operative clause covering the matrix requirement"
  1276	    },
  1277	    {
  1278	      "matrix_id": "7.2",
  1279	      "contract_id": "7.4",
  1280	      "relationship": "aligned",
  1281	      "link_index": 15,
  1282	      "coverage_role": "direct",
  1283	      "coverage": "Primary operative clause covering the matrix requirement"
  1284	    },
  1285	    {
  1286	      "matrix_id": "7.2",
  1287	      "contract_id": "7.4.1",
  1288	      "relationship": "aligned",
  1289	      "link_index": 15,
  1290	      "coverage_role": "context",
  1291	      "coverage": "Supplementary clause providing additional coverage"
  1292	    },
  1293	    {
  1294	      "matrix_id": "7.3",
  1295	      "contract_id": "7.1",
  1296	      "relationship": "aligned",
  1297	      "link_index": 16,
  1298	      "coverage_role": "direct",
  1299	      "coverage": "Primary operative clause covering the matrix requirement"
  1300	    },
Tool:   1101	    },
  1102	    {
  1103	      "matrix_id": "5.1.4",
  1104	      "requirement": "Право Банка выставить счет/платежное требование при невозможности удержания",
  1105	      "source_evidence": "«При невозможности удержать суммы, указанные в п. 5.1.1 Договора... Банк выставляет счет на оплату или платежное требование о списании денежных средств к расчетному счету Предприятия...»",
  1106	      "status": "missing_in_contract",
  1107	      "required_type": "mandatory",
  1108	      "applicability": "applicable",
  1109	      "risk_level": "medium",
  1110	      "risk": "Отсутствие альтернативного механизма взыскания (счет/платежное требование) при невозможности удержания из текущих перечислений ослабляет позицию Банка.",
  1111	      "rejected_candidates": []
  1112	    },
  1113	    {
  1114	      "matrix_id": "5.1.5",
  1115	      "requirement": "Право Банка не возмещать суммы операций, проведенных с нарушением условий Договора",
  1116	      "source_evidence": "«Банк имеет право: → Не возмещать Предприятию суммы Операций, проведенных с нарушением условий Договора.»",
  1117	      "status": "missing_in_contract",
  1118	      "required_type": "mandatory",
  1119	      "applicability": "applicable",
  1120	      "risk_level": "medium",
  1121	      "risk": "Отсутствие прямого права не возмещать суммы операций с нарушениями. Частично покрывается правом удержания недействительных операций (п. 5.2.10.1), но это разные механизмы.",
  1122	      "rejected_candidates": [
  1123	        {
  1124	          "contract_id": "5.2.10.1",
  1125	          "reason": "Право удержания недействительных операций (п. 5.2.10.1) покрывает уже перечисленные суммы, но не является аналогом права отказа в возмещении (предотвращение перечисления)."
  1126	        }
  1127	      ]
  1128	    },
  1129	    {
  1130	      "matrix_id": "5.1.8.4",
  1131	      "requirement": "Право Банка прекратить Авторизацию при несоответствии Ресурса Требованиям Банка",
  1132	      "source_evidence": "«несоответствие Ресурса Требованиям Банка к Ресурсу Предприятия»",
  1133	      "status": "missing_in_contract",
  1134	      "required_type": "optional",
  1135	      "applicability": "not_applicable",
  1136	      "risk_level": "low",
  1137	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
  1138	      "rejected_candidates": []
  1139	    },
  1140	    {
  1141	      "matrix_id": "5.1.8.5",
  1142	      "requirement": "Право Банка прекратить Авторизацию при осуществлении запрещенных видов деятельности",
  1143	      "source_evidence": "«осуществление видов деятельности, указанных в Требованиях к Ресурсу Предприятия»",
  1144	      "status": "missing_in_contract",
  1145	      "required_type": "optional",
  1146	      "applicability": "not_applicable",
  1147	      "risk_level": "low",
  1148	      "risk": "Требование имеет фильтр only_for_product=internet_acquiring. Контракт является trade_acquiring — не применимо.",
  1149	      "rejected_candidates": []
  1150	    },
  1151	    {
  1152	      "matrix_id": "5.1.9",
  1153	      "requirement": "Право Банка осуществлять дополнительные проверки проведения Операции, включая обращение в Банк-эмитент",
  1154	      "source_evidence": "«Банк имеет право: → Осуществлять дополнительные проверки проведения Операции в ТСТ, в т.ч. обращаться в Банк-эмитент для проверки правомерности Операции.»",
  1155	      "status": "missing_in_contract",
  1156	      "required_type": "mandatory",
  1157	      "applicability": "applicable",
  1158	      "risk_level": "medium",
  1159	      "risk": "Отсутствие права на дополнительные проверки операций ограничивает возможности Банка по верификации подозрительных транзакций.",
  1160	      "rejected_candidates": []
  1161	    },
  1162	    {
  1163	      "matrix_id": "5.1.10",
  1164	      "requirement": "Право Банка проводить проверку Предприятия на предмет мошенничества и соответствия",
  1165	      "source_evidence": "«Банк имеет право: → Проводить проверку Предприятия, в т.ч. на предмет выявления мошеннических операций, предоставления Покупателям Товаров/услуг, несоответствующих роду деятельности...»",
  1166	      "status": "missing_in_contract",
  1167	      "required_type": "mandatory",
  1168	      "applicability": "applicable",
  1169	      "risk_level": "medium",
  1170	      "risk": "Отсутствует активное право Банка на проведение проверок. Есть только пассивная обязанность Заказчика не препятствовать (п. 5.3.17), что не равнозначно.",
  1171	      "rejected_candidates": [
  1172	        {
  1173	          "contract_id": "5.3.17",
  1174	          "reason": "Пункт 5.3.17 содержит обязанность Заказчика не препятствовать проверкам, но не предоставляет Банку активное право инициировать и проводить проверки."
  1175	        }
  1176	      ]
  1177	    },
  1178	    {
  1179	      "matrix_id": "5.1.12",
  1180	      "requirement": "Право Банка в одностороннем порядке вносить изменения в документы по ссылкам в Договоре",
  1181	      "source_evidence": "«Банк имеет право: → В одностороннем порядке вносить изменения в документы, ссылки на которые даются в Договоре, путем публикации информации на Официальном сайте Банка не менее чем за 1 календарный день...»",
  1182	      "status": "missing_in_contract",
  1183	      "required_type": "optional",
  1184	      "applicability": "applicable",
  1185	      "risk_level": "medium",
  1186	      "risk": "Отсутствие права одностороннего изменения связанных документов. В 44-ФЗ контракте изменения существенных условий требуют соглашения сторон (п. 11.8), что может блокировать оперативное обновление инструктивных материалов.",
  1187	      "rejected_candidates": []
  1188	    },
  1189	    {
  1190	      "matrix_id": "5.1.15",
  1191	      "requirement": "Право Банка отказать в заключении Договора без объяснения причин",
  1192	      "source_evidence": "«Банк имеет право: → Отказать Предприятию в заключении Договора без объяснения причин.»",
  1193	      "status": "missing_in_contract",
  1194	      "required_type": "optional",
  1195	      "applicability": "not_applicable",
  1196	      "risk_level": "low",
  1197	      "risk": "Право относится к преддоговорной стадии. Для заключенного 44-ФЗ контракта нерелевантно. В 44-ФЗ отказ в заключении после победы в закупке невозможен.",
  1198	      "rejected_candidates": []
  1199	    },
  1200	    {
  1201	      "matrix_id": "5.1.17.1",
  1202	      "requirement": "Право Банка расторгнуть Договор при низком торговом обороте на Электронный терминал (<40 000/80 000 руб.)",
  1203	      "source_evidence": "«Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов... если Торговый оборот на один Электронный терминал Банка не превышает 40 000...»",
  1204	      "status": "missing_in_contract",
  1205	      "required_type": "optional",
  1206	      "applicability": "applicable",
  1207	      "risk_level": "low",
  1208	      "risk": "Пункт optional, only_for_terminal=pos. Применим к контракту. Отсутствие ограничивает право Банка на расторжение при неэффективном использовании терминалов.",
  1209	      "rejected_candidates": []
  1210	    },
  1211	    {
  1212	      "matrix_id": "5.1.17.2",
  1213	      "requirement": "Право Банка расторгнуть Договор при низком торговом обороте на Смарт-терминал (<40 000/80 000 руб.) или задолженности",
  1214	      "source_evidence": "«Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата... Смарт-терминалов... если Торговый оборот на один Смарт-терминал Банка не превышает 40 000...»",
  1215	      "status": "missing_in_contract",
  1216	      "required_type": "optional",
  1217	      "applicability": "not_applicable",
  1218	      "risk_level": "low",
  1219	      "risk": "Пункт optional, only_for_terminal=smart. Контракт имеет профиль terminal=pos. Смарт-терминалы не входят в профиль — не применимо.",
  1220	      "rejected_candidates": []
  1221	    }
  1222	  ],
  1223	  "unmatched_contract": [],
  1224	  "summary": {
  1225	    "aligned_count": 23,
  1226	    "deviation_count": 10,
  1227	    "missing_in_contract_count": 25,
  1228	    "extra_in_contract_count": 0,
  1229	    "note": "25 missing_in_contract включает 13 неприменимых (internet_acquiring/smart-terminal фильтры) и 12 применимых отсутствующих требований. 10 deviation включают 2 существенных (штраф за терминал снижен, безакцептное списание ограничено) и 8 низкорисковых."
  1230	  }
  1231	}
AI: Now I have a comprehensive picture. Let me now focus on my specific task: identifying **material contract-only terms** (`extra_in_contract`). I need to review what's already been identified in the batch outputs and check for any remaining contract clauses that haven't been evaluated.

Let me now systematically go through the contract to identify all contract clauses and check which ones have already been classified. Let me also check the `check_unmatched.py` script:[{'name': 'read_file', 'args': {'file_path': '/outputs/working/check_unmatched.py', 'limit': 100}, 'id': 'call_00_tVCLbVWHKBjxgghgnTDh6793', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/final_validate.py', 'limit': 100}, 'id': 'call_01_4FuhoCbYI06iAfrVytce3421', 'type': 'tool_call'}]
Tool:      1	import json
     2	data = json.load(open('outputs/working/batch_4_output.json','r'))
     3	matrix = json.load(open('inputs/matrix.json','r'))
     4	matrix_by_id = {m['number']: m for m in matrix}
     5	
     6	print('=== UNMATCHED MATRIX ITEMS ===')
     7	for m in data['unmatched_matrix']:
     8	    mid = m['matrix_id']
     9	    mi = matrix_by_id.get(mid, {})
    10	    req = mi.get('required_type','?')
    11	    print(f"{mid}: req_type={req}, current={m.get('required_type','?')}")
    12	    print(f"  main_idea: {mi.get('main_idea','')[:150]}")
    13	    print()
Tool:      1	import json
     2	from collections import Counter
     3	
     4	data = json.load(open('outputs/working/batch_4_output.json','r'))
     5	
     6	print('=== FINAL VALIDATION ===')
     7	print(f"Links: {len(data['links'])}")
     8	print(f"Atomic links: {len(data['atomic_links'])}")
     9	print(f"Unmatched matrix: {len(data['unmatched_matrix'])}")
    10	print(f"Unmatched contract: {len(data['unmatched_contract'])}")
    11	print(f"Filtered out: {len(data['filtered_out'])}")
    12	print()
    13	
    14	rels = Counter(l['relationship'] for l in data['links'])
    15	print(f"Link relationships: {dict(rels)}")
    16	
    17	risks = Counter(l['risk_level'] for l in data['links'])
    18	print(f"Link risk levels: {dict(risks)}")
    19	
    20	um_risks = Counter(m['risk_level'] for m in data['unmatched_matrix'])
    21	print(f"Unmatched matrix risk levels: {dict(um_risks)}")
    22	
    23	uc_risks = Counter(c['risk_level'] for c in data['unmatched_contract'])
    24	print(f"Unmatched contract risk levels: {dict(uc_risks)}")
    25	
    26	# Verify aligned have no discrepancies
    27	errors = []
    28	for l in data['links']:
    29	    if l['relationship'] == 'aligned' and len(l['discrepancies']) > 0:
    30	        errors.append(f"ERROR: aligned link {l['matrix_ids']} has discrepancies!")
    31	    if l['relationship'] == 'deviation' and len(l['discrepancies']) == 0:
    32	        errors.append(f"ERROR: deviation link {l['matrix_ids']} has no discrepancies!")
    33	
    34	link_count = len(data['links'])
    35	for a in data['atomic_links']:
    36	    if a['link_index'] >= link_count:
    37	        errors.append(f"ERROR: atomic link references non-existent link_index {a['link_index']}")
    38	
    39	if errors:
    40	    for e in errors:
    41	        print(e)
    42	else:
    43	    print("No structural errors found.")
    44	
    45	# Verify summary
    46	aligned = sum(1 for l in data['links'] if l['relationship'] == 'aligned')
    47	deviation = sum(1 for l in data['links'] if l['relationship'] == 'deviation')
    48	print(f"\nSummary check: aligned={aligned} (reported={data['summary']['aligned_count']}), deviation={deviation} (reported={data['summary']['deviation_count']})")
    49	print(f"missing={len(data['unmatched_matrix'])} (reported={data['summary']['missing_in_contract_count']}), extra={len(data['unmatched_contract'])} (reported={data['summary']['extra_in_contract_count']})")
    50	
    51	print("\nValidation complete.")
AI: Now I have a thorough understanding of the existing analysis. Let me now focus on my specific task: **identifying material contract-only terms** (`extra_in_contract`). 

Let me review what's already been identified as `extra_in_contract` across all batches and check for any remaining contract clauses that haven't been evaluated. Let me also look at the contract more carefully for clauses that may have been missed:[{'name': 'write_todos', 'args': {'todos': [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'in_progress'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'pending'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'pending'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'pending'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]}, 'id': 'call_00_HdHmIBYTq0aMtqXWSsGS1922', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'in_progress'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'pending'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'pending'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'pending'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]
AI: Let me now compile all existing `extra_in_contract` findings from batch_4 and check for any missing contract clauses. Let me also look at the contract more carefully:[{'name': 'execute', 'args': {'command': 'cd / && python3 -c "\nimport json\n\n# Load batch 4 which has unmatched_contract\nb4 = json.load(open(\'outputs/working/batch_4_output.json\',\'r\'))\nprint(\'=== EXISTING extra_in_contract from batch_4 ===\')\nfor e in b4[\'unmatched_contract\']:\n    print(f\\"  {e[\'contract_id\']}: risk={e[\'risk_level\']}\\")\n    print(f\\"    position: {e[\'contract_position\'][:150]}\\")\n    print(f\\"    materiality: {e[\'materiality_reason\'][:150]}\\")\n    print()\n\n# Check batch 1, 2, 3 for unmatched_contract\nfor bn in [\'batch_1_output\', \'batch_2_output\', \'batch_3_output\']:\n    b = json.load(open(f\'outputs/working/{bn}.json\',\'r\'))\n    if b.get(\'unmatched_contract\'):\n        print(f\'=== {bn} unmatched_contract ===\')\n        for e in b[\'unmatched_contract\']:\n            print(f\\"  {e[\'contract_id\']}: risk={e[\'risk_level\']}\\")\n    else:\n        print(f\'{bn}: unmatched_contract is empty\')\n"\n'}, 'id': 'call_00_dQwwjunn4TUcYl33iww68207', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:6
[stderr] + cd / && python3 -c "
[stderr] +      ~~
[stderr] The token '&&' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import json; b4 = json.load(open(\'/outputs/working/batch_4_output.json\',\'r\')); print(\'=== EXISTING extra_in_contract from batch_4 ===\'); [print(f\\"  {e[\'contract_id\']}: risk={e[\'risk_level\']}\\n    position: {e[\'contract_position\'][:150]}\\n    materiality: {e[\'materiality_reason\'][:150]}\\n\\") for e in b4[\'unmatched_contract\']]"'}, 'id': 'call_00_9yjNehBUz0ixPBRtGNHy3653', 'type': 'tool_call'}]
Tool: [stderr] $ErrorActionPreference = 'Stop'
[stderr] $env:PYTHONIOENCODING = 'utf-8'
[stderr] $env:PYTHONUTF8 = '1'
[stderr] if (Test-Path -LiteralPath 'C:\Users\gogel\OneDrive\Рабочий стол\Проекты\skillshot_manual_2\.venv\Scripts') {
[stderr]   $env:Path = 'C:\Users\gogel\OneDrive\Рабочий стол\Проекты\skillshot_manual_2\.venv\Scripts;' + $env:Path
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
[stderr] python3 -c "import json; b4 = json.load(open('outputs/working/batch_4_output.json','r')); print('=== EXISTING extra_in_
[stderr] contract from batch_4 ==='); [print(f\"  {e['contract_id']}: risk={e['risk_level']}\n    position: {e['contract_positio
[stderr] n'][:150]}\n    materiality: {e['materiality_reason'][:150]}\n\") for e in b4['unmatched_contract']]"
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : ScriptBlock should only be specified as a value of the Command parameter.
[stderr] At line:36 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/check_extra.py'}, 'id': 'call_00_xHygS3yL5taHp91RgXsP4882', 'type': 'tool_call'}]
Tool: Extra in contract:
  5.2.9: Bank right to unilaterally suspend Authorization and/or terminate Contract for 11 specified events including: contract b
    risk: low

  5.2.10: Bank right to withhold from amounts payable to Customer: invalid operation amounts (with 11 specific grounds), erroneous
    risk: low

  5.3.19: Customer obligation to reimburse Contractor in full and unconditionally for: funds debited from Contractor per Payment S
    risk: low

  5.7: Customer penalty for non-return of equipment: 10,000 RUB per Electronic terminal, 25,000 RUB per Smart-terminal (includi
    risk: low

  7.8: Exchange of documents for liability measures and other actions related to breach shall use EIS with electronic notificat
    risk: low

  7.12: In case of contract termination due to unilateral refusal, the other Party may demand compensation only for actually inc
    risk: medium

  8.3: Detailed 44-FZ acceptance procedure: monthly EIS document generation by 10th working day, UKEP signature, specific requi
    risk: low

  11.6: Contract amendment and/or termination shall be carried out in accordance with the procedure, timelines, cases and condit
    risk: low

  11.8: Parties have stipulated that changes to essential contract terms during performance are not permitted, except by agreeme
    risk: medium

  12.3: During contract performance, by agreement between Customer and Contractor, provision of services with improved quality, 
    risk: low


[Command succeeded with exit code 0]
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'completed'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'in_progress'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'pending'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'pending'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]}, 'id': 'call_00_yiUXAQYv23Dcc9sar0nJ6916', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'completed'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'in_progress'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'pending'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'pending'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]
AI: Now let me systematically go through the contract to identify all clauses and check which ones have been evaluated. Let me build a comprehensive list of contract clauses and cross-reference with the coverage ledgers:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\n\n# Load all batch outputs\nbatches = []\nfor fn in [\'batch_1_output\', \'batch_2_output\', \'batch_3_output\', \'batch_4_output\']:\n    batches.append(json.load(open(f\'/outputs/working/{fn}.json\', \'r\')))\n\n# Collect all contract_ids from coverage_ledgers and links\nall_covered = set()\nfor b in batches:\n    if \'coverage_ledger\' in b and \'contract\' in b[\'coverage_ledger\']:\n        for c in b[\'coverage_ledger\'][\'contract\']:\n            all_covered.add(c[\'contract_id\'])\n    for l in b.get(\'links\', []):\n        for cid in l.get(\'contract_ids\', []):\n            all_covered.add(cid)\n    for uc in b.get(\'unmatched_contract\', []):\n        all_covered.add(uc[\'contract_id\'])\n\nprint(\'=== All covered contract IDs ===\')\nfor cid in sorted(all_covered):\n    print(f\'  {cid}\')\nprint(f\'Total: {len(all_covered)}\')\n"\n'}, 'id': 'call_00_CM3cF5t8mmas6eLs6xE38995', 'type': 'tool_call'}]
Tool: === All covered contract IDs ===
  1.1
  1.3
  10.1
  10.2
  11.1
  11.2
  11.3
  11.4
  11.5
  11.6
  11.7
  11.8
  12.1
  12.2
  12.3
  12.4
  12.5
  2.3.1
  2.3.2
  2.3.3
  2.3.4
  2.3.5
  2.3.6
  2.3.7
  2.3_receipt_dates
  3.1
  3.2
  4.3
  4.5
  5.1.1
  5.1.10
  5.1.4
  5.1.6
  5.1.7
  5.1.8
  5.1.9
  5.10
  5.2.10
  5.2.10.1
  5.2.10.2
  5.2.10.3
  5.2.10.4
  5.2.10.5
  5.2.2
  5.2.3
  5.2.4
  5.2.5
  5.2.6
  5.2.7
  5.2.8
  5.2.9
  5.2.9.1
  5.2.9.10
  5.2.9.11
  5.2.9.2
  5.2.9.3
  5.2.9.4
  5.2.9.5
  5.2.9.6
  5.2.9.7
  5.2.9.8
  5.2.9.9
  5.3.10
  5.3.11
  5.3.12
  5.3.13
  5.3.14
  5.3.15
  5.3.16
  5.3.17
  5.3.18.1
  5.3.18.2
  5.3.18.3
  5.3.18.5
  5.3.19
  5.3.2
  5.3.20
  5.3.20.4
  5.3.7
  5.3.8
  5.3.9
  5.4.3
  5.4.5
  5.5
  5.6
  5.7
  5.9
  6.1
  7.1
  7.10
  7.12
  7.4
  7.4.1
  7.5
  7.6
  7.7
  7.7.1
  7.7.3
  7.8
  8.3
  8.3.1
  8.3.2
  8.5.1
  8.5.7
  9.1
  9.2
  Spec
  Tech_5
  Заявление_п1.3
  Приложение №1 п.3
  Приложение №1 п.5
  Приложение_1_п5
  Приложение_№1_п5
Total: 113

[Command succeeded with exit code 0]
AI: Now let me identify contract clauses that are NOT yet covered. Let me map the contract structure:[{'name': 'execute', 'args': {'command': 'python -c "\n# List all contract clauses from the contract text\n# Based on my reading, here are the main contract sections/clauses:\n\ncontract_clauses = [\n    # Preamble/Header\n    \'header\',  # Contract header - requisites\n    # Section 1\n    \'1.1\', \'1.2\', \'1.3\',\n    # Section 2 - Definitions\n    \'2.1\', \'2.1.1\', \'2.1.2\', \'2.1.3\', \'2.1.4\', \'2.1.5\', \'2.1.6\', \'2.1.7\', \'2.1.8\',\n    \'2.1.9\', \'2.1.10\', \'2.1.11\', \'2.1.12\', \'2.1.13\', \'2.1.14\', \'2.1.15\', \'2.1.16\',\n    \'2.1.17\', \'2.1.18\', \'2.1.19\', \'2.1.20\', \'2.1.21\', \'2.1.22\', \'2.1.23\', \'2.1.24\',\n    \'2.1.25\', \'2.1.26\', \'2.1.27\', \'2.1.28\',\n    \'2.2\', \'2.3\', \'2.3.1\', \'2.3.2\', \'2.3.3\', \'2.3.4\', \'2.3.5\', \'2.3.6\', \'2.3.7\',\n    # Section 3\n    \'3.1\', \'3.1.1\', \'3.2\', \'3.3\',\n    # Section 4\n    \'4.1\', \'4.2\', \'4.3\', \'4.4\', \'4.5\', \'4.5.1\',\n    # Section 5\n    \'5.1\', \'5.1.1\', \'5.1.2\', \'5.1.3\', \'5.1.4\', \'5.1.5\', \'5.1.6\', \'5.1.7\', \'5.1.8\', \'5.1.9\', \'5.1.10\',\n    \'5.2\', \'5.2.1\', \'5.2.2\', \'5.2.3\', \'5.2.4\', \'5.2.5\', \'5.2.6\', \'5.2.7\', \'5.2.8\', \'5.2.9\',\n    \'5.2.9.1\', \'5.2.9.2\', \'5.2.9.3\', \'5.2.9.4\', \'5.2.9.5\', \'5.2.9.6\', \'5.2.9.7\', \'5.2.9.8\', \'5.2.9.9\', \'5.2.9.10\', \'5.2.9.11\',\n    \'5.2.10\', \'5.2.10.1\', \'5.2.10.2\', \'5.2.10.3\', \'5.2.10.4\', \'5.2.10.5\',\n    \'5.3\', \'5.3.1\', \'5.3.2\', \'5.3.3\', \'5.3.4\', \'5.3.5\', \'5.3.6\', \'5.3.7\', \'5.3.8\', \'5.3.9\', \'5.3.10\',\n    \'5.3.11\', \'5.3.12\', \'5.3.13\', \'5.3.14\', \'5.3.15\', \'5.3.16\', \'5.3.17\',\n    \'5.3.18\', \'5.3.18.1\', \'5.3.18.2\', \'5.3.18.3\', \'5.3.20.4\', \'5.3.18.5\',\n    \'5.3.19\', \'5.3.20\',\n    \'5.4\', \'5.4.1\', \'5.4.2\', \'5.4.3\', \'5.4.4\', \'5.4.5\',\n    \'5.5\', \'5.6\', \'5.7\', \'5.9\', \'5.10\',\n    # Section 6\n    \'6.1\',\n    # Section 7\n    \'7.1\', \'7.2\', \'7.3\', \'7.4\', \'7.4.1\', \'7.5\', \'7.6\', \'7.7\', \'7.7.1\', \'7.7.2\', \'7.7.3\',\n    \'7.8\', \'7.9\', \'7.10\', \'7.11\', \'7.12\',\n    # Section 8\n    \'8.1\', \'8.2\', \'8.3\', \'8.3.1\', \'8.3.2\', \'8.4\', \'8.5\', \'8.5.1\', \'8.5.2\', \'8.5.3\', \'8.5.4\', \'8.5.5\',\n    \'8.5.6\', \'8.5.7\', \'8.5.8\', \'8.5.9\', \'8.6\', \'8.7\', \'8.8\', \'8.9\', \'8.10\', \'8.11\',\n    # Section 9\n    \'9.1\', \'9.2\', \'9.3\',\n    # Section 10\n    \'10.1\', \'10.2\',\n    # Section 11\n    \'11.1\', \'11.2\', \'11.3\', \'11.4\', \'11.5\', \'11.6\', \'11.7\', \'11.8\',\n    # Section 12\n    \'12.1\', \'12.2\', \'12.3\', \'12.4\', \'12.5\',\n    # Section 13\n    \'13\',\n    # Appendices\n    \'App1\', \'App1.1\', \'App1.2\',\n]\n\nimport json\nbatches = []\nfor fn in [\'batch_1_output\', \'batch_2_output\', \'batch_3_output\', \'batch_4_output\']:\n    batches.append(json.load(open(f\'/outputs/working/{fn}.json\', \'r\')))\n\nall_covered = set()\nfor b in batches:\n    if \'coverage_ledger\' in b and \'contract\' in b[\'coverage_ledger\']:\n        for c in b[\'coverage_ledger\'][\'contract\']:\n            all_covered.add(c[\'contract_id\'])\n    for l in b.get(\'links\', []):\n        for cid in l.get(\'contract_ids\', []):\n            all_covered.add(cid)\n    for uc in b.get(\'unmatched_contract\', []):\n        all_covered.add(uc[\'contract_id\'])\n\n# Find uncovered\nuncovered = []\nfor c in contract_clauses:\n    if c not in all_covered:\n        uncovered.append(c)\n\nprint(\'=== UNCOVERED contract clauses ===\')\nfor c in sorted(uncovered):\n    print(f\'  {c}\')\nprint(f\'Total uncovered: {len(uncovered)}\')\n"\n'}, 'id': 'call_00_mtLKGNSABCGFjV1bATzc4078', 'type': 'tool_call'}]
Tool: === UNCOVERED contract clauses ===
  1.2
  13
  2.1
  2.1.1
  2.1.10
  2.1.11
  2.1.12
  2.1.13
  2.1.14
  2.1.15
  2.1.16
  2.1.17
  2.1.18
  2.1.19
  2.1.2
  2.1.20
  2.1.21
  2.1.22
  2.1.23
  2.1.24
  2.1.25
  2.1.26
  2.1.27
  2.1.28
  2.1.3
  2.1.4
  2.1.5
  2.1.6
  2.1.7
  2.1.8
  2.1.9
  2.2
  2.3
  3.1.1
  3.3
  4.1
  4.2
  4.4
  4.5.1
  5.1
  5.1.2
  5.1.3
  5.1.5
  5.2
  5.2.1
  5.3
  5.3.1
  5.3.18
  5.3.3
  5.3.4
  5.3.5
  5.3.6
  5.4
  5.4.1
  5.4.2
  5.4.4
  7.11
  7.2
  7.3
  7.7.2
  7.9
  8.1
  8.10
  8.11
  8.2
  8.4
  8.5
  8.5.2
  8.5.3
  8.5.4
  8.5.5
  8.5.6
  8.5.8
  8.5.9
  8.6
  8.7
  8.8
  8.9
  9.3
  App1
  App1.1
  App1.2
  header
Total uncovered: 83

[Command succeeded with exit code 0]
AI: Now I need to evaluate these uncovered clauses. Many are definitions (2.1.x), headings, or non-operative provisions. Let me categorize them systematically. Let me read the specific uncovered clauses from the contract to determine which are material:[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 0, 'limit': 100}, 'id': 'call_00_rIwDHIYmB6Kb4cthJb7r2092', 'type': 'tool_call'}]
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
AI: Now I have a thorough understanding. Let me now systematically evaluate the uncovered clauses and identify which are material contract-only terms. Let me categorize them:[{'name': 'write_todos', 'args': {'todos': [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'completed'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'completed'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'in_progress'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'pending'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]}, 'id': 'call_00_ayVseQDBccXCxUGr4vce3675', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'completed'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'completed'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'in_progress'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'pending'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]
AI: Now let me carefully evaluate each uncovered clause. I'll go through them systematically:

**Already classified as `extra_in_contract` in batch_4:**
- 5.2.9, 5.2.10, 5.3.19, 5.7, 7.8, 7.12, 8.3, 11.6, 11.8, 12.3

Now let me evaluate the uncovered clauses for materiality:

**Definitions (2.1 - 2.1.28, 2.2):** These are all definitions. Per the skill instructions and comparison pattern 21, definitions without legal effect are `not_material`. However, per pattern 22, a definition with legal effect is evaluable. Let me check a few key ones:

- **2.2 (электронный терминал):** This definition has operative effect — it states "Электронный терминал предоставляется исполнителем и устанавливается на срок действия контракта. Электронный терминал предназначен и может использоваться только в целях исполнения контракта." This creates obligations (Bank provides, Customer uses only for contract purposes). However, these obligations are already covered by 5.1.1, 5.3.18.1, etc. The definition itself is not independently material beyond what's already covered.

- **2.1.23 (тарифы банка):** Defines tariffs as percentage + service fee. This is a definition that supports operative clauses. Not independently material.

- **2.1.19 (предприятие/Заказчик):** Defines the Customer. Standard definition.

All 2.1.x definitions are standard definitions without independent legal effect → `not_material`.

**Headings and parent clauses:**
- **2.3 (parent):** Just the chapeau for 2.3.1-2.3.7. Non-operative parent → `not_material`.
- **5.1 (parent):** "Исполнитель обязуется:" → heading → `not_material`.
- **5.2 (parent):** "Исполнитель вправе:" → heading → `not_material`.
- **5.3 (parent):** "Заказчик обязуется:" → heading → `not_material`.
- **5.4 (parent):** "Заказчик вправе:" → heading → `not_material`.
- **8.5 (parent):** Heading → `not_material`.
- **header:** Contract header with requisites → `not_material`.

Now let me check the operative clauses that are uncovered:

- **1.2:** "Объем услуг... определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта" — This is a volume/scope limitation. It says the volume is determined by Customer's need within the max price. This is a material term because it makes the volume demand-driven rather than fixed. No matrix analogue for this demand-driven volume mechanism. → **extra_in_contract**.

- **3.1.1:** "Цена за единицу услуги указана в спецификации (Приложение № 1)" — This is a reference to the Specification appendix. Procedural, not independently material. → `not_material`.

- **3.3:** "Положения настоящего Контракта, касающиеся применения цены контракта или начальной максимальной цены Контракта применяются к максимальному значению цены Контракта... если Федеральным законом №44-ФЗ не установлено иное." — This is a 44-FZ price application rule. It clarifies that references to "contract price" mean the maximum price. This is a 44-FZ specific interpretative rule. → **extra_in_contract** (material because it affects how price-related provisions are interpreted).

- **4.1:** Service period: March 1, 2025 to November 30, 2025 or until price exhausted. This is already covered via link to matrix 10.1 (contract duration). The specific dates are contract-specific but the structure is aligned. → Already covered via 11.1 link.

- **4.2:** Contractor must comply with legal requirements and have a banking license. This is a 44-FZ specific requirement. No matrix analogue for the explicit license requirement. → **extra_in_contract** (material because it imposes a specific licensing obligation on the Bank).

- **4.4:** Payment procedure — безналичный расчет, платежное поручение. Also: Bank must notify of account changes within 2 days, otherwise bears risks. This is partially covered (payment procedure linked to matrix 3.3/4.2.1). But the 2-day notification and risk allocation for account changes is a specific obligation not in the matrix. → The payment procedure part is covered. The 2-day notification + risk allocation is **extra_in_contract**.

- **4.5.1:** November services paid by December 30, 2025. This is a specific deadline for the final month. → **extra_in_contract** (material because it creates a hard year-end payment deadline).

- **5.1.2:** Monthly document of acceptance per 8.3.1-8.3.2. This is covered via the 8.3.1/8.3.2 links. → Already covered.

- **5.1.3:** Ensure services comply with RF legislation. This is a general compliance obligation. → **extra_in_contract** (material because it creates an independent warranty of legal compliance).

- **5.1.5:** Provide full and accurate information about services and performance, including difficulties. This is a transparency obligation on the Bank. No matrix analogue. → **extra_in_contract** (material because it creates an affirmative disclosure duty).

- **5.2.1:** Right to demand timely acceptance and payment. This is a general enforcement right. → **extra_in_contract** (material because it creates an explicit Bank right to demand performance).

- **5.3.1:** Accept services per acceptance document. Covered via acceptance procedure links. → Already covered.

- **5.3.3:** Monitor the Contractor's service delivery. This is a Customer oversight right. → **extra_in_contract** (material because it creates a Customer monitoring right).

- **5.3.4:** Unilaterally refuse contract if Contractor doesn't meet procurement requirements or provided false information. This is a 44-FZ specific termination right for the Customer. → **extra_in_contract** (material because it creates a Customer termination right).

- **5.3.5:** Demand penalties for Contractor delay/non-performance. This is a general enforcement right. → **extra_in_contract** (material because it creates an explicit Customer right to penalties).

- **5.3.6:** Reduce payment by tax amounts if taxes must be paid to budget. This is a 44-FZ tax withholding mechanism. → **extra_in_contract** (material because it allows Customer to withhold taxes from payment).

- **5.3.15:** Provide confirmation of legal basis for personal data transfer; indemnify Bank for lack of such confirmation; notify of consent withdrawal. This is partially covered via 4.2.16.1 link. The indemnity and notification elements may be extra. → Check: 5.3.15 is in the coverage_ledger as linked. Let me verify.

- **5.3.18:** Parent heading for trade acquiring obligations → `not_material`.

- **5.4.1:** Right to demand proper performance. General enforcement right. → **extra_in_contract** (material).

- **5.4.2:** Right to refuse acceptance of substandard services. This is a 44-FZ acceptance refusal right. → **extra_in_contract** (material because it creates a Customer right to refuse acceptance).

- **5.4.4:** Right to refuse payment for substandard services and demand refund. → **extra_in_contract** (material because it creates a Customer payment refusal right).

- **7.2:** Contractor's right to demand penalties from Customer for delay. This is a general enforcement right. → **extra_in_contract** (material).

- **7.3:** Penalty calculation for Customer delay — 1/300 key rate. This is a specific penalty formula. → **extra_in_contract** (material because it sets a specific penalty rate).

- **7.7.2:** Special fine calculation for winner who bid above NMCK. This is a 44-FZ specific penalty mechanism. → **extra_in_contract** (material).

- **7.9:** Penalty application doesn't release from performance. → **extra_in_contract** (material).

- **7.11:** Cap on Customer fines ≤ Contract Price. Already covered via 7.3 link. → Already covered.

- **8.1:** Quality guarantee per Appendix 1 requirements and regulations. → **extra_in_contract** (material because it creates a quality warranty).

- **8.2:** Contractor liable for damage caused by its specialists. → **extra_in_contract** (material because it creates specific liability for personnel actions).

- **8.4:** Date of receipt of acceptance document = date of EIS placement per Customer's time zone. → **extra_in_contract** (material because it defines a key procedural timestamp).

- **8.5.2:** Acceptance may require Contractor representative presence with proper documents; 15-day advance notice. → **extra_in_contract** (material because it creates a procedural right for Contractor to participate in acceptance).

- **8.5.3:** If notice received timely, acceptance is bilateral. → **extra_in_contract** (material, procedural).

- **8.5.4:** If no timely notice, acceptance is unilateral by Customer. → **extra_in_contract** (material, procedural).

- **8.5.5:** Customer conducts expert review of services. → **extra_in_contract** (material because it creates a Customer inspection right).

- **8.5.6:** Expert review may be internal or external. → **extra_in_contract** (material, procedural).

- **8.5.8:** Acceptance commission procedure with UKEP signatures. → **extra_in_contract** (material, procedural).

- **8.5.9:** Contractor may correct deficiencies and resubmit. → **extra_in_contract** (material, procedural).

- **8.6:** Acceptance date = date of EIS placement of signed document. → **extra_in_contract** (material, defines key date).

- **8.7:** Corrections to acceptance document via EIS with UKEP. → **extra_in_contract** (material, procedural).

- **8.8:** Acceptance results formalized per this section. → `not_material` (procedural reference).

- **8.9:** Customer may accept despite non-conformity if it doesn't prevent acceptance and is cured. → **extra_in_contract** (material because it modifies acceptance standards).

- **8.10:** Contractor must cure defects within 3 days of Customer's notice. → **extra_in_contract** (material because it creates a specific cure deadline).

- **8.11:** Signed acceptance document is basis for payment. → **extra_in_contract** (material because it links acceptance to payment obligation).

- **9.3:** Party claiming force majeure must provide documentary proof from authorized body. → **extra_in_contract** (material because it creates an evidentiary requirement).

- **13:** Addresses and bank details. → `not_material` (requisites).

- **App1, App1.1, App1.2:** Appendices. App1 (Technical Assignment) is already covered via Tech_5 and Приложение references. App1.1 (Application) is covered via Заявление_п1.3. App1.2 (TST Information) is a form. → Already covered or `not_material` (blank forms).

Now let me also check some clauses that are in the covered list but may have been misclassified. Let me look at 5.3.15, 5.3.18, 5.3.3, 5.3.4, 5.3.5, 5.3.6 more carefully:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nbatches = []\nfor fn in [\'batch_1_output\', \'batch_2_output\', \'batch_3_output\', \'batch_4_output\']:\n    batches.append(json.load(open(f\'/outputs/working/{fn}.json\', \'r\')))\n\n# Check if 5.3.15, 5.3.3, 5.3.4, 5.3.5, 5.3.6 are in coverage_ledger\ntargets = [\'5.3.15\', \'5.3.3\', \'5.3.4\', \'5.3.5\', \'5.3.6\', \'5.3.1\', \'5.4.1\', \'5.4.2\', \'5.4.4\', \'5.1.2\', \'5.1.3\', \'5.1.5\', \'5.2.1\', \'4.2\', \'4.4\', \'4.5.1\', \'3.3\', \'1.2\', \'7.2\', \'7.3\', \'7.7.2\', \'7.9\', \'8.1\', \'8.2\', \'8.4\', \'8.5.2\', \'8.5.3\', \'8.5.4\', \'8.5.5\', \'8.5.6\', \'8.5.8\', \'8.5.9\', \'8.6\', \'8.7\', \'8.9\', \'8.10\', \'8.11\', \'9.3\']\nfor t in targets:\n    found = False\n    for b in batches:\n        if \'coverage_ledger\' in b and \'contract\' in b[\'coverage_ledger\']:\n            for c in b[\'coverage_ledger\'][\'contract\']:\n                if c[\'contract_id\'] == t:\n                    print(f\'{t}: FOUND in coverage_ledger - closure={c[\\"closure\\"]}\')\n                    found = True\n        for l in b.get(\'links\', []):\n            if t in l.get(\'contract_ids\', []):\n                print(f\'{t}: FOUND in links - matrix={l[\\"matrix_ids\\"]}\')\n                found = True\n        for uc in b.get(\'unmatched_contract\', []):\n            if uc[\'contract_id\'] == t:\n                print(f\'{t}: FOUND in unmatched_contract\')\n                found = True\n    if not found:\n        print(f\'{t}: NOT FOUND in any batch\')\n"\n'}, 'id': 'call_00_bNgJ3mFRtWDvvmyXw7m22655', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 15
[stderr]     print(f'{t}: FOUND in coverage_ledger - closure={c[" closure\]}')
[stderr]                                                        ^
[stderr] SyntaxError: unterminated string literal (detected at line 15)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/check_coverage.py', 'content': 'import json\n\nbatches = []\nfor fn in [\'batch_1_output\', \'batch_2_output\', \'batch_3_output\', \'batch_4_output\']:\n    batches.append(json.load(open(f\'/outputs/working/{fn}.json\', \'r\')))\n\ntargets = [\'5.3.15\', \'5.3.3\', \'5.3.4\', \'5.3.5\', \'5.3.6\', \'5.3.1\', \'5.4.1\', \'5.4.2\', \'5.4.4\', \'5.1.2\', \'5.1.3\', \'5.1.5\', \'5.2.1\', \'4.2\', \'4.4\', \'4.5.1\', \'3.3\', \'1.2\', \'7.2\', \'7.3\', \'7.7.2\', \'7.9\', \'8.1\', \'8.2\', \'8.4\', \'8.5.2\', \'8.5.3\', \'8.5.4\', \'8.5.5\', \'8.5.6\', \'8.5.8\', \'8.5.9\', \'8.6\', \'8.7\', \'8.9\', \'8.10\', \'8.11\', \'9.3\']\nfor t in targets:\n    found = False\n    for b in batches:\n        if \'coverage_ledger\' in b and \'contract\' in b[\'coverage_ledger\']:\n            for c in b[\'coverage_ledger\'][\'contract\']:\n                if c[\'contract_id\'] == t:\n                    print(f\'{t}: FOUND in coverage_ledger - closure={c["closure"]}\')\n                    found = True\n        for l in b.get(\'links\', []):\n            if t in l.get(\'contract_ids\', []):\n                print(f\'{t}: FOUND in links - matrix={l["matrix_ids"]}\')\n                found = True\n        for uc in b.get(\'unmatched_contract\', []):\n            if uc[\'contract_id\'] == t:\n                print(f\'{t}: FOUND in unmatched_contract\')\n                found = True\n    if not found:\n        print(f\'{t}: NOT FOUND in any batch\')\n'}, 'id': 'call_00_3JCS4u5VUSh2ow4PNnp26573', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/check_coverage.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/check_coverage.py'}, 'id': 'call_00_uq0V9NzhsYj6DQeczV1U7963', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Рабочий стол\Проекты\skillshot_manual_2\outputs\working\check_coverage.py", line 5, in <module>
[stderr]     batches.append(json.load(open(f'/outputs/working/{fn}.json', 'r')))
[stderr]                              ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/batch_1_output.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "import os; print(os.getcwd()); print(os.listdir(\'outputs/working/\'))"'}, 'id': 'call_00_5IdUMuRF0B4gMr1cNirI1212', 'type': 'tool_call'}]
Tool: C:\Users\gogel\OneDrive\Рабочий стол\Проекты\skillshot_manual_2
['batch4_analysis.py', 'batch4_list.py', 'batch4_list2.py', 'batch4_matrix_dump.txt', 'batch_1_output.json', 'batch_2_output.json', 'batch_3_output.json', 'batch_4_output.json', 'build_batch2.py', 'check_coverage.py', 'check_extra.py', 'check_unmatched.py', 'clause_index.json', 'contract_product_profile.json', 'enrich_propositions.py', 'extract_batch4.py', 'final_validate.py', 'fix_missing.py', 'fix_overlap.py', 'fix_req_types.py', 'generate_atomic.py', 'legal_propositions.json', 'validate_batch1.py', 'validate_batch2.py', 'validate_batch3.py']

[Command succeeded with exit code 0]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/check_coverage.py', 'old_string': "    batches.append(json.load(open(f'/outputs/working/{fn}.json', 'r')))", 'new_string': "    batches.append(json.load(open(f'outputs/working/{fn}.json', 'r')))"}, 'id': 'call_00_mrszk9Kypmq8jkRIVXw26796', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/check_coverage.py'
AI: [{'name': 'execute', 'args': {'command': 'python outputs/working/check_coverage.py'}, 'id': 'call_00_hFpX9Z2xzw5Nu8PWWcX59274', 'type': 'tool_call'}]
Tool: 5.3.15: FOUND in coverage_ledger - closure=linked
5.3.15: FOUND in links - matrix=['4.2.16.3']
5.3.3: NOT FOUND in any batch
5.3.4: NOT FOUND in any batch
5.3.5: NOT FOUND in any batch
5.3.6: NOT FOUND in any batch
5.3.1: NOT FOUND in any batch
5.4.1: NOT FOUND in any batch
5.4.2: NOT FOUND in any batch
5.4.4: NOT FOUND in any batch
5.1.2: NOT FOUND in any batch
5.1.3: NOT FOUND in any batch
5.1.5: NOT FOUND in any batch
5.2.1: NOT FOUND in any batch
4.2: NOT FOUND in any batch
4.4: NOT FOUND in any batch
4.5.1: NOT FOUND in any batch
3.3: NOT FOUND in any batch
1.2: NOT FOUND in any batch
7.2: NOT FOUND in any batch
7.3: NOT FOUND in any batch
7.7.2: NOT FOUND in any batch
7.9: NOT FOUND in any batch
8.1: NOT FOUND in any batch
8.2: NOT FOUND in any batch
8.4: NOT FOUND in any batch
8.5.2: NOT FOUND in any batch
8.5.3: NOT FOUND in any batch
8.5.4: NOT FOUND in any batch
8.5.5: NOT FOUND in any batch
8.5.6: NOT FOUND in any batch
8.5.8: NOT FOUND in any batch
8.5.9: NOT FOUND in any batch
8.6: NOT FOUND in any batch
8.7: NOT FOUND in any batch
8.9: NOT FOUND in any batch
8.10: NOT FOUND in any batch
8.11: NOT FOUND in any batch
9.3: NOT FOUND in any batch

[Command succeeded with exit code 0]
AI: Good. Now I have a clear picture. Let me now compile the complete list of material contract-only terms. I need to evaluate each uncovered clause and separate `extra_in_contract` from `not_material`. Let me now write the comprehensive analysis:[{'name': 'write_todos', 'args': {'todos': [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'completed'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'completed'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'completed'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'in_progress'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]}, 'id': 'call_00_5kS86NO5jS9XttmAdEVI8169', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Review existing extra_in_contract findings from batch_4_output.json', 'status': 'completed'}, {'content': 'Cross-check all contract clauses against existing coverage_ledger to find unevaluated clauses', 'status': 'completed'}, {'content': 'Identify any remaining material contract-only terms not yet classified', 'status': 'completed'}, {'content': 'Separate extra_in_contract from not_material for each finding', 'status': 'in_progress'}, {'content': 'Write final contract-only findings to /outputs/working/contract_only_terms.json', 'status': 'pending'}]

