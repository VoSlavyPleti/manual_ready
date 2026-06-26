## Summarized at 2026-06-25T20:15:57.385826+00:00

Human: Matrix batch 3 comparison (items 97-144)
AI: I'll start by reading the skill file and understanding the task structure, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_bxrqgNTAY1QwQNYILxYr0141', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/*', 'path': '/'}, 'id': 'call_01_ufCVpayBw1GiO6eGfmDK5964', 'type': 'tool_call'}]
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
   162	## Analogue Threshold
   163	
   164	Create a final link only when the contract proposition is a true legal analogue
   165	of the matrix proposition. Test:
   166	
   167	- same or equivalent protected party;
   168	- same or equivalent bound party;
   169	- same legal object;
   170	- same operative right, duty, prohibition, permission, remedy, or allocation of
   171	  risk;
   172	- material trigger, scope, procedure, and consequence are the same or legally
   173	  equivalent.
   174	
   175	Reject weak thematic candidates. A clause about the same broad topic is not a
   176	legal analogue when it governs a different object, party, trigger, procedure,
   177	or consequence.
   178	
   179	## Bidirectional Matching
   180	
   181	Perform both directions.
   182	
   183	Matrix to contract:
   184	
   185	- for each applicable evaluable matrix proposition, retrieve all contract
   186	  clauses that collectively cover the Bank-standard requirement;
   187	- include parent, child, appendix, payment, procedure, liability, and framework
   188	  clauses only when they provide material coverage or legally cure a gap.
   189	- if a child clause is selected, check whether its parent carries operative
   190	  legal meaning for the same topic; if a parent is selected, check whether its
   191	  children contain the material elements;
   192	- for payment, acceptance, liability, termination, and document-exchange
   193	  requirements, keep the legal package together: operative clause, basis,
   194	  deadline, procedure, remedy, consequence, and any incorporated appendix/table
   195	  row that changes coverage;
   196	- a framework or legal-compliance clause may be a standalone analogue only when
   197	  it carries the same legal object or allocates the same risk, duty, or remedy.
   198	
   199	Contract to matrix:
   200	
   201	- for each evaluable contract proposition, find the matrix analogue group;
   202	- if none exists and the term has independent legal effect, classify it as
   203	  `extra_in_contract`;
   204	- if it is non-operative, close it as `not_material` only in the ledger.
   205	
   206	Group related ids into many-to-many `links`. One matrix id may need several
   207	contract clauses. One contract clause may cover several matrix ids.
   208	
   209	### Uncovered Element Closure Rule
   210	
   211	For every applicable evaluable matrix item, identify the material provisions
   212	that must be covered: party, legal object, duty/right, trigger, deadline,
   213	amount, formula, cap, penalty, scope, procedure, channel, liability, remedy,
   214	exception, and consequence.
   215	
   216	If any material provision remains uncovered after the first candidates are
   217	found, continue candidate search across the full contract index before
   218	finalizing status. This rule applies to both `missing_in_contract` and
   219	`deviation`.
   220	
   221	Document the closure for each final matrix-side finding:
   222	
   223	- `covered_elements`: provisions actually covered by final contract candidates;
   224	- `uncovered_elements`: provisions still missing, changed, narrowed, or
   225	  weakened;
   226	- `candidate_contract_ids`: contract clauses accepted as true analogues or
   227	  package candidates;
   228	- `rejected_contract_ids`: clauses reviewed but rejected, with short legal
   229	  reasons;
   230	- `candidate_search_exhausted`: `true` only after all contract clauses have
   231	  been checked through `clause_index` / `legal_propositions`;
   232	- `search_scope`: `full_contract`, `targeted_domain`, or `not_completed`.
   233	
   234	Status rules for the closure:
   235	
   236	- `aligned` is allowed only when `uncovered_elements` is empty.
   237	- `deviation` is allowed only when true analogue candidates exist and the
   238	  remaining changed/missing provisions were not cured by any other contract
   239	  clause after a full-contract sweep.
   240	- `missing_in_contract` is allowed only when the full-contract sweep found no
   241	  true analogue.
   242	- `candidate_search_exhausted = false` or `search_scope = not_completed` means
   243	  the matrix item is not ready for final output.
   244	
   245	Keep the sweep efficient. Use `clause_index` and `legal_propositions` to scan
   246	all clauses. Re-read source text only for plausible candidates, hard terms, and
   247	rejected clauses whose legal object is close enough to need explanation.
   248	
   249	## Group-Level Status
   250	
   251	Assign status to the group, not to each atomic pair.
   252	
   253	- `aligned`: the contract package preserves the matrix legal result.
   254	- `deviation`: a true analogue exists, but any material element is changed,
   255	  narrowed, weakened, omitted, shifted, or blank.
   256	- `missing_in_contract`: no true contract analogue exists for an applicable
   257	  matrix requirement.
   258	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   259	  analogue.
   260	- `not_material`: internal ledger closure only; exclude from final report.
   261	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
   262	  final report because the requirement does not apply to the current product,
   263	  lot, terminal, payment method, or legal regime.
   264	
   265	Material elements include party, legal object, operative act, trigger,
   266	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   267	remedy, exception, Bank right, merchant duty, and consequence.
   268	
   269	Hard terms must be compared directly:
   270	
   271	- same material deadline/amount/procedure in the same legal obligation can be
   272	  `aligned`;
   273	- changed value or missing value is `deviation`;
   274	- a hard term from another clause counts only when that clause expressly
   275	  governs the same obligation or is explicitly incorporated;
   276	- a neighboring date, amount, or procedure for another legal object cannot cure
   277	  the gap.
   278	
   279	Do not downgrade for formal differences alone: heading, title, appendix label,
   280	permitted option selection, equivalent mandatory-law mechanism, or wording
   281	style.
   282	
   283	Do not downgrade for low-risk notes when the legal result is preserved. If the
   284	reason says the difference is merely terminological, beneficial to the Bank,
   285	already incorporated through another clause, or caused only by a mandatory
   286	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
   287	
   288	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
   289	when it materially worsens or changes a Bank-standard term: payment timing,
   290	acceptance control, withholding right, penalty/cap, termination power, protected
   291	party, evidence channel, or enforceability.
   292	
   293	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
   294	Before marking a liability group `aligned`, check the amount, formula, cap,
   295	trigger, protected party, excluded delay/non-delay buckets, and claim procedure
   296	across the whole package.
   297	
   298	## Risk Calibration
   299	
   300	Use `risk_level` consistently:
   301	
   302	- `none`: only for `aligned`;
   303	- `low`: optional applicable missing, placeholder, formal but legally manageable
   304	  gap;
   305	- `medium`: material deviation that can affect performance, evidence, payment,
   306	  control, liability, or enforceability;
   307	- `high`: mandatory missing, changed protected party, major payment/remedy
   308	  change, important Bank right omitted, or broad contract-only risk.
   309	
   310	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   311	a short evidence-based reason. Use concise quotes rather than long excerpts.
   312	
   313	## Final QA
   314	
   315	Before writing final artifacts:
   316	
   317	- verify `clause_index` covers all source ids;
   318	- verify `legal_proposition_ledger` has no unresolved
   319	  `needs_source_review` rows that can affect final status;
   320	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   321	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   322	  `coverage_ledger`;
   323	- verify every applicable evaluable matrix id is linked or in
   324	  `unmatched_matrix`;
   325	- verify every final matrix-side link or missing row has exhausted candidate
   326	  search evidence: covered/uncovered elements, accepted candidates, rejected
   327	  close candidates, and `candidate_search_exhausted = true`;
   328	- verify out-of-scope / non-applicable matrix ids are not in final
   329	  `unmatched_matrix`;
   330	- verify every material contract id is closed as linked or extra;
   331	- verify `coverage_ledger` is derived from final `links`,
   332	  `unmatched_matrix`, and `unmatched_contract`;
   333	- verify every final id is visible in source text;
   334	- verify `aligned` has no material discrepancy;
   335	- verify every `deviation` has a named legal gap and evidence;
   336	- verify weak candidates are not in final `links`;
   337	- verify non-material contract rows are absent from final `unmatched_contract`;
   338	- verify summary counts equal final arrays.
   339	
   340	## Output Discipline
   341	
   342	Follow `references/output-contract.md`.
   343	
   344	The final JSON must contain:
   345	
   346	- `analysis_profile`
   347	- `links`
   348	- `atomic_links`
   349	- `unmatched_matrix`
   350	- `unmatched_contract`
   351	- `coverage_ledger`
   352	- `summary`
   353	
   354	`links` carry group-level legal findings. `atomic_links` are traceability
   355	projections only and must inherit the group relationship. Do not assign
   356	separate final pair-level statuses.
   357	
   358	## Tools And Scripts
   359	
   360	Use helper scripts for mechanical work: source extraction, indexing,
   361	normalization checks, batch completeness, coverage validation, JSON schema
   362	checks, and Excel export. Do not put legal mapping or status decisions into
   363	hardcoded scripts.
Tool: ['/.env', '/.git/COMMIT_EDITMSG', '/.git/FETCH_HEAD', '/.git/HEAD', '/.git/ORIG_HEAD', '/.git/config', '/.git/description', '/.git/hooks/applypatch-msg.sample', '/.git/hooks/commit-msg.sample', '/.git/hooks/fsmonitor-watchman.sample', '/.git/hooks/post-update.sample', '/.git/hooks/pre-applypatch.sample', '/.git/hooks/pre-commit.sample', '/.git/hooks/pre-merge-commit.sample', '/.git/hooks/pre-push.sample', '/.git/hooks/pre-rebase.sample', '/.git/hooks/pre-receive.sample', '/.git/hooks/prepare-commit-msg.sample', '/.git/hooks/push-to-checkout.sample', '/.git/hooks/sendemail-validate.sample', '/.git/hooks/update.sample', '/.git/index', '/.git/info/exclude', '/.git/logs/HEAD', '/.git/logs/refs/heads/20_min_80', '/.git/logs/refs/heads/clear-branch', '/.git/logs/refs/heads/codex/clear_one_skill', '/.git/logs/refs/heads/demo', '/.git/logs/refs/heads/main', '/.git/logs/refs/heads/one_skill', '/.git/logs/refs/heads/pre=agent', '/.git/logs/refs/heads/test', '/.git/logs/refs/heads/test2', '/.git/logs/refs/heads/test3', '/.git/logs/refs/remotes/origin/20_min_80', '/.git/logs/refs/remotes/origin/HEAD', '/.git/logs/refs/remotes/origin/clear-branch', '/.git/logs/refs/remotes/origin/demo', '/.git/logs/refs/remotes/origin/main', '/.git/logs/refs/remotes/origin/one_skill', '/.git/logs/refs/remotes/origin/pre=agent', '/.git/logs/refs/remotes/origin/test', '/.git/logs/refs/remotes/origin/test2', '/.git/logs/refs/remotes/origin/test3', '/.git/lost-found/commit/a9784911cc1c5b5eab6643175e5ec45caf25eee4', '/.git/lost-found/other/00025daef50b48b9a7c3aa0957f67692b7cf9644', '/.git/lost-found/other/00279ba916b80ee7f054dcfe4bcad5fdf3d0cad4', '/.git/lost-found/other/003f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/lost-found/other/0052dd8f0d35e7d44cabe09971d6e0f21ca39cd2', '/.git/lost-found/other/009107e59a300c960ee6ec2a0fd55630b53e6a77', '/.git/lost-found/other/00bf2ee6092a4428c1c240774794e6c695ff4722', '/.git/lost-found/other/0108acc654101c39e74de3cb6404c4fa80bc7bad', '/.git/lost-found/other/011eb16c1ca5cd43dfe08ae67835808b35c8afe0', '/.git/lost-found/other/015abae91e08022c92cb6c24e1e1097ec60a9c6b', '/.git/lost-found/other/016411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/lost-found/other/01686fb3f6afa2208defd34a9188169a7884eccf', '/.git/lost-found/other/0189548f4f27fcb26840150f585a64515d77c26d', '/.git/lost-found/other/01a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/lost-found/other/024da679e39764f8e2a1862074bc7d3a67b39a2e', '/.git/lost-found/other/02500954f54d824bf47a0c40e7249570c8ae35a6', '/.git/lost-found/other/027cd9077d41da5280567175993abb09c6e81add', '/.git/lost-found/other/02955e2401b4f817cc67ef6094697af860f2d18e', '/.git/lost-found/other/02b7b9d7d9324409084e9f2b00eae11901589864', '/.git/lost-found/other/02e3706e34f211187bd64efa7a9ad51760195d39', '/.git/lost-found/other/02e5c435ffbd7357cd76f7c19bf5f4451ea88c3d', '/.git/lost-found/other/02e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/lost-found/other/0312d61983ef80179bfac79abbba1359052f115c', '/.git/lost-found/other/03732f0c6e6eeaef66eda4e4a6de308b7e7e1e95', '/.git/lost-found/other/03ff6a156c8ba598cf1be27fb2371810888a927a', '/.git/lost-found/other/040be927181b9604d69593ffe36ab7303b1a94bc', '/.git/lost-found/other/042e02d97cc4abc6a96b55d97f34fc76924c9cf9', '/.git/lost-found/other/04378a998f4a8686eb28f62e8833b0f539229714', '/.git/lost-found/other/043f51145222bf3b3e811ab6d29c229b25b3b1d3', '/.git/lost-found/other/044e235175ddef6dd6b9a05edbd34b9ab69cbbd3', '/.git/lost-found/other/04602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/lost-found/other/0478eb80cc9a8041214bf273295064af3ab7f7d7', '/.git/lost-found/other/048703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/lost-found/other/0488481d528674a76807703e6625d6284ca8293e', '/.git/lost-found/other/0489842c6d2c5ddbc9550902039e9b25701d08db', '/.git/lost-found/other/04ba7faa5aee31cca7feb4058574f06ec3a9b645', '/.git/lost-found/other/04bf8e699f88900a6960b666079dba19a77ee7eb', '/.git/lost-found/other/04d51f0de077d3b810718bfa2ca6ac4f3567c07f', '/.git/lost-found/other/04d557d3b8c74f15dc8b1039d196b50cb8924950', '/.git/lost-found/other/04eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/lost-found/other/0504a514448e0c3c3e4f771ffc84479295824920', '/.git/lost-found/other/0558ff9439de64e491ee9c3bd2097b5b118029b6', '/.git/lost-found/other/055ecd0695e622dcadcedc29409753f35d106433', '/.git/lost-found/other/057e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/lost-found/other/05c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/lost-found/other/05e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/lost-found/other/0617f381a59a452478a8f34cabb652beadf361cd', '/.git/lost-found/other/061c9d02a136ba7adc607ed7074cd148595a2030', '/.git/lost-found/other/0631461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/lost-found/other/06418747a855c7847e27bfe23508610c20a60493', '/.git/lost-found/other/064efa3154548faf37f72f6e16da0f94681fa86a', '/.git/lost-found/other/06a8e8ac333fed73af47212fe4626cbaa3b74e82', '/.git/lost-found/other/074930d053a799cc4f9095e89196437f704205d6', '/.git/lost-found/other/07682e77b603150eac6f657df236ac3dced0586d', '/.git/lost-found/other/077efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/lost-found/other/0791e2c492831faaf144a90e6af25adaabad38fa', '/.git/lost-found/other/07d0f29a2d244a75911191faf176cc0c7edf4bda', '/.git/lost-found/other/07d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/lost-found/other/080554e8ddc2a1a87275a26e5457e1b2a6046657', '/.git/lost-found/other/08080c1aef87cedbe163497ddad8cc3005a73f7d', '/.git/lost-found/other/080d85bb922b72b159fc03f3f1a84d23a9d2568c', '/.git/lost-found/other/082169d84ac7751152d7134fa37292c00ba029d0', '/.git/lost-found/other/08377760400a919e539db754b0b66ea7ce0cef58', '/.git/lost-found/other/0842d15769f312e00dbce38c79a209d783d115ea', '/.git/lost-found/other/0846bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/lost-found/other/08749be2799a1a1f0697ed2571a4682426ea12ff', '/.git/lost-found/other/088409712f5c920b0dbf4a4c818e977f34f91873', '/.git/lost-found/other/08ba0a8ee50af5b8ff5eb0a82d30bb5229fe2e86', '/.git/lost-found/other/08feb11d7a524e0e04e556a3b0fac0a6a7b24657', '/.git/lost-found/other/0937353c8f0a794e6ea7d64c5904fa44ffbc61aa', '/.git/lost-found/other/093d21dba99b105a0e82051ab2639b5151325793', '/.git/lost-found/other/0946862f3f15d72c8b71d2af4522b4921f6cab96', '/.git/lost-found/other/094e04d13c87f5a327a7f44ffedc0ce41d9214d0', '/.git/lost-found/other/098b34de8f71069fae9082ecd1903b6faedce4e6', '/.git/lost-found/other/09916958db8eaa97c465c9bec51a3d1a29863ab8', '/.git/lost-found/other/0a05a2808a79fe98d007bccb3b1060551300dec8', '/.git/lost-found/other/0a32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/lost-found/other/0a401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/lost-found/other/0a56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/lost-found/other/0a597e37cfb13fe9af1875fc0606d2f7cc0e7ada', '/.git/lost-found/other/0a962ce910aa746587b34755922bae542449fba9', '/.git/lost-found/other/0abc810e4c97279e80fa5610d8d2838b94e3bb03', '/.git/lost-found/other/0ae25708036bf7db64f0327ea004917ad42ea679', '/.git/lost-found/other/0b32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/lost-found/other/0b5d3ac18d6fbd99afb581479554b58fc4183e02', '/.git/lost-found/other/0b5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/lost-found/other/0b9c1ff14d0729b8ca054bf3b70a31ed6ea3724f', '/.git/lost-found/other/0baa622887f5563517e122f9b16213710af9e5cb', '/.git/lost-found/other/0bbcef51f80d0155f83a276423028a01a50cd92e', '/.git/lost-found/other/0bbe894f6158df6217aac34e5062d723091507dd', '/.git/lost-found/other/0bc5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/lost-found/other/0bebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/lost-found/other/0bf720f21f41ce829add4aab5a9a05012208c3f7', '/.git/lost-found/other/0c00cb9ca737f2be5b9cff166bcef532262ec699', '/.git/lost-found/other/0c4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/lost-found/other/0c55eb9a5a6f0f2c00a7d6a578505a35c3c881f8', '/.git/lost-found/other/0c614b8e0f3afd25e895d9491c2a30e5913af606', '/.git/lost-found/other/0c64a4d48bda41945b4888b51a9e960d8fbfcf0f', '/.git/lost-found/other/0cd26a469771b69762f53b5ae2a322bf170091d1', '/.git/lost-found/other/0ce0b926ac0c36b6e353c377ebc74e59bc0561c0', '/.git/lost-found/other/0d2b4e5c9def6a898a4064dd6adf23d978807b49', '/.git/lost-found/other/0d3b08adf9c7ed270b6d5889540ad4437d5f0b98', '/.git/lost-found/other/0d72d0b2349a404cc4cddb87c836194765377d74', '/.git/lost-found/other/0d753acfba917272cd72f418e9c1352ed20054f6', '/.git/lost-found/other/0d8780f3e4c97dc70ba82cc61c5cef46d57b0b33', '/.git/lost-found/other/0dbcae139c196ceada45a4720daaf5908702ecc7', '/.git/lost-found/other/0e189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/lost-found/other/0e31d5d75617658d5871f0af7cd6e2572f65d5a7', '/.git/lost-found/other/0e33d9681c3f231054d16d613b34097e7e8b59e7', '/.git/lost-found/other/0eb37de8ca5ba7a34797b3355f41cf01b22ff008', '/.git/lost-found/other/0ebe1fc27f8d238046aea951e6caa693563a5db1', '/.git/lost-found/other/0eddffee3cce42079be92d29e9858c7f31c0a906', '/.git/lost-found/other/0ef556b4beacab982c37a6ba626b68c12a03a3ae', '/.git/lost-found/other/0f0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/lost-found/other/0f138f0796a06e405b352d9b196d634fe03272bd', '/.git/lost-found/other/0f3f373dbe68457e2f332b53419313c5297f50fa', '/.git/lost-found/other/0f573afb56cf5cd6dd86621f5e5c4d7eeff7c726', '/.git/lost-found/other/0f5968785d1283804001ca49ccf77d63eac98e02', '/.git/lost-found/other/0f86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/lost-found/other/0f9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/lost-found/other/0febdd5aed4ccb535776cb3ecf5f7292598d83cf', '/.git/lost-found/other/1018a2334d5c1968f40c2f478fb1f2867e67b8b5', '/.git/lost-found/other/1064453d1e30d78cd388f816b907f7b742375e31', '/.git/lost-found/other/108486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/lost-found/other/108d20d49b8c9df755feb7040b27dd500650d6f1', '/.git/lost-found/other/1152abac92eac8d8b605f61e7608e5151d222f07', '/.git/lost-found/other/1168066a747c3bef2d6e633b2347c20cc6b56404', '/.git/lost-found/other/116968b47e00996915b67531127f0954c7ddd1a4', '/.git/lost-found/other/1195185617fa4e3585174859ed5709d013f5937a', '/.git/lost-found/other/11b6a93338766923a8e6379405e6fcf4ab828169', '/.git/lost-found/other/11c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/lost-found/other/11e01dd8395bcb4499bbae87a8fa5d396b5bb9a0', '/.git/lost-found/other/11f3df8ac49a0be182d46132407e50090bc85a7e', '/.git/lost-found/other/1260fee99a4cfcbd9d4ffb0eb2de091a7a472b7b', '/.git/lost-found/other/12782408d18b12ea7c1fd9e5d39ddbfa2040ef21', '/.git/lost-found/other/128150674170b66350257cc719da038a61a568bf', '/.git/lost-found/other/12d12afbdb51a82ea91470a68c5936ef307758b3', '/.git/lost-found/other/12ecf89d4939f447a2a13eb6a8584268d822df06', '/.git/lost-found/other/132ce036f2fe47610a5925b048748ef75eb541db', '/.git/lost-found/other/13360394a41c8fabc39419ab404191a8575e2799', '/.git/lost-found/other/133c2a7f8f0c8e8798adb0c95502b796e8304aa0', '/.git/lost-found/other/1392a68ba7c0702c66b4fb266ffd087081b1e141', '/.git/lost-found/other/13c40173739fb7e84b979f3c6ac5261cec02e012', '/.git/lost-found/other/13dd0ea3ac7cf3fa815ff54ed379ac145c2200aa', '/.git/lost-found/other/13fb8a33b9d96c2a9ff445c20dea718e895df5e4', '/.git/lost-found/other/143334e584ff71080c606f29c1ef42924bbe453d', '/.git/lost-found/other/14394b47e18f572003e3d82368702dfd474b70c4', '/.git/lost-found/other/143df4c79cc8ee0249f8509549e5377882a28010', '/.git/lost-found/other/1474c8f7cf8bc22cda503322795cac94ac621675', '/.git/lost-found/other/148a5ec5787afd3f553071ecc831a805312f6ece', '/.git/lost-found/other/148c20fa8c56ae81068aded6b9a8f2a59fc229dd', '/.git/lost-found/other/149a72f18b0f5ac8ed9bf713a2c26c76d8158588', '/.git/lost-found/other/14fe9bb6670802ae36d1022630b687088b71c35d', '/.git/lost-found/other/15098da0ba5b0e2d399d8688a8a0b6a0fcd68d1d', '/.git/lost-found/other/155f8df967724158d80873e629c6c12bb65c8d00', '/.git/lost-found/other/159a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/lost-found/other/159bfd26b659195df8c8486d12b5e15f948cb808', '/.git/lost-found/other/15be2e474eb938a89e4d7c19737994893197e781', '/.git/lost-found/other/15fc480833c1c814d413e14a2421b5ffed74028f', '/.git/lost-found/other/15fd3d807851be39f668587b875d1bd9356e1171', '/.git/lost-found/other/163d050dd4db671d29be7efff1a35864f91ca61d', '/.git/lost-found/other/1645e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/lost-found/other/164b7fafb2c4bcbb6315f95870ae3efbf8a82241', '/.git/lost-found/other/165d22d6f5554de58d1281ade7295158d4e62312', '/.git/lost-found/other/167230ee6e97a40999b7b1b46b089e48951a1158', '/.git/lost-found/other/1683c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/lost-found/other/16a2cab9c4e32851d2754116ca26b4ead49cd1a3', '/.git/lost-found/other/16bc644bbb95c0d296bea492b5595b361a93b9fa', '/.git/lost-found/other/16d466f5d6f6422fc565801d9d97c0bd71bf6a5a', '/.git/lost-found/other/16de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/lost-found/other/171b3e26763b46f7034313a38879dcb5e511f770', '/.git/lost-found/other/177a3761fec84c8776563bc7d9edcd67544feca6', '/.git/lost-found/other/17875ecd8901fa5f6f1ffd63a3f4ac41cd695e3e', '/.git/lost-found/other/179165971d58c6643a8bf303e8bf53e64a143ed8', '/.git/lost-found/other/17a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/lost-found/other/17c6782b615441baeb457ee93a458ed7371c9f99', '/.git/lost-found/other/1805f56abd31c9fa832a4d2e4d2a6525282bd60f', '/.git/lost-found/other/180e3f7a759491581027a4970076148d69b10348', '/.git/lost-found/other/185c9bede1c02917cd4743d154dc42b2cd03cb25', '/.git/lost-found/other/1862eec0af25e420dee69a16ba235f610f20756d', '/.git/lost-found/other/1876a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/lost-found/other/1888c3e87775cf3cfca934be2e7ec03a6696f1da', '/.git/lost-found/other/18d512a4ebe9f93cc357a19059984b3398799bee', '/.git/lost-found/other/18fe30c098f75b96caa54450040279f8727780ea', '/.git/lost-found/other/1929b4d821dbc5d88f2c4c6d8839d0fedf3fa95f', '/.git/lost-found/other/19704e0cd5db5fec06dd7c57009e47296c0c4411', '/.git/lost-found/other/19928324ad53403e47456f49785dd300a6abc1e0', '/.git/lost-found/other/1994bb1252910ca25e7dd1c7eaee69a59f99d597', '/.git/lost-found/other/19bc9e08c030c0958b8cfcb118ef4e6a076e1bfe', '/.git/lost-found/other/19d15ee65c1ad2342c69a499567a3d8e33d985d2', '/.git/lost-found/other/19ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/lost-found/other/19eac84456408b48017f9b8f7012a31d357f9ded', '/.git/lost-found/other/19ef249a5908e6c6f084c18763897a644a28241b', '/.git/lost-found/other/1a04525ea6855d36a41a4720d225e21887989682', '/.git/lost-found/other/1a3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/lost-found/other/1a412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/lost-found/other/1a7b119a11b008be1ded0bd9ca1ddfad0e5a5260', '/.git/lost-found/other/1a955782d22785e3c692639e34ac42ecd1ad95be', '/.git/lost-found/other/1ae3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/lost-found/other/1afcc87003afe09c0245ee2e2f90a48f107eea91', '/.git/lost-found/other/1afe522d67bb11ef6df1ef598c4a6077cbdbf43f', '/.git/lost-found/other/1b2651a7254d50dd505d130cb119b1e0f63b274d', '/.git/lost-found/other/1b297017feb7427e872083cfba46fdd2d1f5d1f1', '/.git/lost-found/other/1bb304e8afd560b9be58336068f17f0f453cd33d', '/.git/lost-found/other/1bb6184cbc8ec7b0b92597da642ddb7baea3f9f0', '/.git/lost-found/other/1bb94dc37fa7ba202e37fb9f730b2c1ffe60c9f8', '/.git/lost-found/other/1bd62bc3162bcc0924c6b11dcc91aea034a50dda', '/.git/lost-found/other/1bd948006afad9d92ba0af0d9d6aac84b81201ee', '/.git/lost-found/other/1be15396b1a24634af2755f0315d590d8f5efb56', '/.git/lost-found/other/1c3b26b30ba44895a4b99ed6b8361e4fe8d6e96e', '/.git/lost-found/other/1c5c64af7a4a179928feb3e438ba9aeca2b21785', '/.git/lost-found/other/1c6f0d2fcead6d6b9af167efe84b68ab9867253d', '/.git/lost-found/other/1c8f3931f4569a257832b968b4b4e0122f827992', '/.git/lost-found/other/1cb460853dbc76ecd603937b1385d60dfe4544da', '/.git/lost-found/other/1cc87e753d217d64955f9f7594e5c51e9515e117', '/.git/lost-found/other/1cc883a61f30b9ef594ac9e9119fba4fb6e6b38a', '/.git/lost-found/other/1cd48831e92cfedee75b4f2bd298004c09a02e41', '/.git/lost-found/other/1ce139b0630235d7cccd5e7233e06fb27e4b7e92', '/.git/lost-found/other/1d116b842cd0f57b27060be476644b86e101adbc', '/.git/lost-found/other/1d486741fb9e843d4c02664be20ce398200e3031', '/.git/lost-found/other/1d62dd77221b120231127e20a3d046857e9e43d4', '/.git/lost-found/other/1d80ca727f627adf666f395a0c85e26662ed0d20', '/.git/lost-found/other/1dd3c6fbd22c1169a906849b6be2a41c24aa2fd9', '/.git/lost-found/other/1de732b38d658fd3ce936527e47cac6259f9592a', '/.git/lost-found/other/1dfc607d1dcba5edcbf0de542ba2777324f237ac', '/.git/lost-found/other/1e350fcaa9e1ea22a0fa61a8b01f206f7ac9dd0a', '/.git/lost-found/other/1e5a8be244c1322fa76b77784e582f480009958d', '/.git/lost-found/other/1e73f11f4d9826d98dd02d4b053bf4f4f144542d', '/.git/lost-found/other/1ed6e6a5f1c7d86cbcffec476f2d43c3a3b164cc', '/.git/lost-found/other/1f604bc809b0d41096d17b0050c153e858717c6c', '/.git/lost-found/other/1f70a2d4551510dfb5fdd95b27b6bf486639e5ef', '/.git/lost-found/other/1f9bc9625cc3b8c37c1c971597ee9e3158f57f4e', '/.git/lost-found/other/1fb978ebe70aba71b3e2d74d673c0459d8480ac6', '/.git/lost-found/other/1fe3e3bfa8d6df8f7d0aae939c931eb1d654bd6b', '/.git/lost-found/other/1ffa5ed33b6108ed57142c1be928988a7761b6dd', '/.git/lost-found/other/201c519c93b3b77bbe0555abc3e68c9a0d24c28b', '/.git/lost-found/other/2077ea20e01da4d37e629d77f92bd01657842631', '/.git/lost-found/other/2083461eff88321aa0feceaab497bc202e7d110e', '/.git/lost-found/other/20a95d03ea8998b75a0379c47b79d67138d097ba', '/.git/lost-found/other/20d6d5fa6f6982c1d4d8d927ae5e9e121fe42018', '/.git/lost-found/other/20edff68991fb4c628d2281dddb40df64282d6e1', '/.git/lost-found/other/20f6f17a1e15763482af8451d3da4498642ba0fb', '/.git/lost-found/other/2125a26d3c69f2df90b281937dc82deb6c57cb20', '/.git/lost-found/other/21637826d1d04950f4a4d796a9571a8c4d86b806', '/.git/lost-found/other/2187ac3ff0237618615d7b487a0d1a6403ef49d2', '/.git/lost-found/other/21b0396817724695b99c77d49474607c4516b8f1', '/.git/lost-found/other/21c099aa1a03294014130368b917b2c6eef94753', '/.git/lost-found/other/21c428f3247ee9fb40e38b78c925eea08e7175aa', '/.git/lost-found/other/21d13a0a40c505324dab511aa407e5dc471bcf1c', '/.git/lost-found/other/21dc7c101abb0ba003e36a25d3686c48c4182328', '/.git/lost-found/other/21eea7a19ea8fa9c7d004bc61a994b42b88b8ac8', '/.git/lost-found/other/21f7a4f54ed4863b3ff2ff03747f55590badc90e', '/.git/lost-found/other/221fbbc53f621f91a6220c85cd506af3f790086e', '/.git/lost-found/other/226a93510d33d1c407aef258f9c39f42e3f298ad', '/.git/lost-found/other/227c0e6634ea1ea9f9c9e1068c1c55f53917c14a', '/.git/lost-found/other/228c08f34331c47620b55794c64c0ff9897f15c0', '/.git/lost-found/other/22b435aac92e50eca2ee89fc748441e81cfcd88d', '/.git/lost-found/other/22baf3300cc31a3540ca4314fd8c58bcb7018353', '/.git/lost-found/other/22e7afb00fe5b7c7602b761800024ed40d25fe21', '/.git/lost-found/other/230d67a0590a4d61346d6dd5ced3f53dd0f1bea2', '/.git/lost-found/other/2339b673bf04246da4977d2a1c82e1f447ea3544', '/.git/lost-found/other/2354041ddba6abd34193e615b4cf804c6e2fd520', '/.git/lost-found/other/2358432f1d03d54e5ede647bf656376dae10e349', '/.git/lost-found/other/237e83f06ebd406dcc11507e0cf8c3be65e684d3', '/.git/lost-found/other/238faa3816f1afd26933d98bd81001eb92a2c876', '/.git/lost-found/other/23b597c126b6815d23f022bce47ef1f8815c532b', '/.git/lost-found/other/241dfb0157cfff0271813dfb80667be5a95deb89', '/.git/lost-found/other/242b028657099781ee5f230d30afc0a8af8423df', '/.git/lost-found/other/245ed230dee59261acbdfe117c3db0280411df76', '/.git/lost-found/other/247b2894f7b921a2585eed175a225fa8e7dee8bd', '/.git/lost-found/other/248a3917f8467ac0cc6218d4b046e8e4b2cba851', '/.git/lost-found/other/248fd8353332111067158f2d11e7087f1ac3fe69', '/.git/lost-found/other/24ec11aadf71bebef0b0658c378b43788974a6c2', '/.git/lost-found/other/24ed3535539a46584ebcd6609d0ecdf3a0f86ddc', '/.git/lost-found/other/250d15ac2ac893edafa629b15e07ede0747d8e78', '/.git/lost-found/other/2516e2d96db3ff349b2fec7f85e9958f93292621', '/.git/lost-found/other/25240eaa758f5a58e2ece8cd89c1ad44a88971ec', '/.git/lost-found/other/2533d1949584c2a0a3b143a5cb4de3f8c1d17758', '/.git/lost-found/other/25393416d634a457748f6167634a4d86955a9774', '/.git/lost-found/other/253f5f1950cdce8f3dd7dca88b26bfcfcb68ad9e', '/.git/lost-found/other/25908607dbe19286a4b0f7b6927619cec2531bf0', '/.git/lost-found/other/25e89d80677a94a06bfb564749370a97050e61ab', '/.git/lost-found/other/25e9c1f9b50b6f8773736712f54f64d323d415f9', '/.git/lost-found/other/261067ca7aa2c677fcce286ae23ffb3e3e3c4b68', '/.git/lost-found/other/26194e93e2a767b3f44b2bb12906aad486311c49', '/.git/lost-found/other/26204973c5913550889f7735c6c91e3f23eb971d', '/.git/lost-found/other/2663b05e98e130e359c6f704963f2e68068a829c', '/.git/lost-found/other/2667e6553b593b2789c084f20b09c8e100fec7e6', '/.git/lost-found/other/2676a4fb754239d1306066ad2d8f58004874245b', '/.git/lost-found/other/268340e1ad4d5df681a7c90f17f4dc772b726e70', '/.git/lost-found/other/268f3c416fe521d519da01323f305123fa54f3aa', '/.git/lost-found/other/26bc257b7c543df579db1afcb9248ced695a5433', '/.git/lost-found/other/26ee19281818f2ab393398d7cdfab1cc1a73aa44', '/.git/lost-found/other/270866455342b36d58ba2ee755f781bbdb564dc4', '/.git/lost-found/other/27cefe5d09eccdf969bbe7c4bd03ba88866dbdd5', '/.git/lost-found/other/27cf296e191cf1e3f150c9cfc6dbb191d17554f6', '/.git/lost-found/other/27e9ed80c1396df06710f8c7782e989d2230e035', '/.git/lost-found/other/289dbec76c204f3703abb10c34cdad5888f18f05', '/.git/lost-found/other/28c2c11c8dfff1aa3fa7b6add9019a0af59a46fc', '/.git/lost-found/other/29017f09af575575dc32524be2294103c1bab658', '/.git/lost-found/other/2912b2774fce14827260d4c8ec3a58acaebd30aa', '/.git/lost-found/other/292fc6f6555ddd8ee1d1baf819d59b7704bd34b9', '/.git/lost-found/other/29b9a8951ad9517c1953a163da020fe28852bba9', '/.git/lost-found/other/29f91579b798fbdf2436d2f21c966d128bba04fd', '/.git/lost-found/other/2a3288a1f6616175a2448df2069d345263d3ceab', '/.git/lost-found/other/2a92a9d4eaa55a8e8264ef2a4ec0a1712f8d8bf7', '/.git/lost-found/other/2aa35d99f6a8fdbe078c97cbf1990f66ca61c0cb', '/.git/lost-found/other/2ac0ccfefd5c151ca5de3ddf23b9bddfc1c8cf4e', '/.git/lost-found/other/2afee31d90e375b801139b051605dc6f5599d9f1', '/.git/lost-found/other/2b1c9b3d9439d122a26ecb89328b50c78ea7dbeb', '/.git/lost-found/other/2b1e035dd765108817ac13695374505ff9a7d9d4', '/.git/lost-found/other/2b33a12233bf94d423b84df484fbd4936841f0ff', '/.git/lost-found/other/2b77f7188e91b5f41905b979e1453716042a88d6', '/.git/lost-found/other/2b84077d254fc2a1d66d0b4ea82ef3a7fa125c3a', '/.git/lost-found/other/2ba1ae4723622dd7a36a624626a298bc4aede590', '/.git/lost-found/other/2baa9b4b0fd3a53e07dbaa15098f4c45e7419cd6', '/.git/lost-found/other/2be2042f9a6e321e9ae96e9becee05d609390c6b', '/.git/lost-found/other/2bf2efefce1765ad78030310ed9900afb0cd5522', '/.git/lost-found/other/2bf5bb558ff589653f528af8bedb778c46df101d', '/.git/lost-found/other/2c24c73a4a5af1d5a5ec1c117c520c7056ea55b1', '/.git/lost-found/other/2c39548b92ad9ddcc9c291ce39e44ed6c6b6cf3e', '/.git/lost-found/other/2c4e1eb30367408711d432986d0b075531aa3a92', '/.git/lost-found/other/2c59ee393814f03d894d5d8c75ab7512af596f2b', '/.git/lost-found/other/2c8ab9af72c1dcf6d59f4a77eb53ad7631241c8c', '/.git/lost-found/other/2c8bd2401a11ab4f8b5e2313cc59bab1b11cd988', '/.git/lost-found/other/2ca2261abaa3459cab2e6b5aac65911448fb906a', '/.git/lost-found/other/2cab5b28db8404259e58a97c72d97538899d23ef', '/.git/lost-found/other/2d201015b65cbcd6a4fe0082bf6d4a65076dc4e1', '/.git/lost-found/other/2d209cca9eecd6d9519f21ae66f180d2001554ef', '/.git/lost-found/other/2d3f8b0777fb0252760bfa45abbb7726b967cc4b', '/.git/lost-found/other/2d5822675d64a208d26431a0cb3bd4a9ee1ad7e1', '/.git/lost-found/other/2d808e55af2eb9b6c496d06a8de71c32578f172a', '/.git/lost-found/other/2d926e4fa759b1b3235635ba6668898a635443f9', '/.git/lost-found/other/2d98f0a835a91e49cb26869dc16dea0583feafbe', '/.git/lost-found/other/2dad60a817385f78660e338a688f9699f3790810', '/.git/lost-found/other/2dfb63554d59caccc63b4addb234c135c283d1f4', '/.git/lost-found/other/2e00a61f618f743393ca83058702b25b950de8ba', '/.git/lost-found/other/2e107635a41522a90f0ea3c1f8fbbb3ff8685f1f', '/.git/lost-found/other/2e395785e7e850594fe6874f052e55a0733d4549', '/.git/lost-found/other/2e91b71a0e65135085d8a12d86bbfd6658dd36de', '/.git/lost-found/other/2eb6a12922b18a340dcf58a23feb13e0e2b1f88b', '/.git/lost-found/other/2f14cb77a3fe840c167ec7c363ba895d3a809b68', '/.git/lost-found/other/2f29d9394aab14b49d63b7303c6549458f4f7158', '/.git/lost-found/other/2f785e870024de3ac7ca3a834b25ca25e9d9cb8e', '/.git/lost-found/other/2f7887c4fbfd68a3721f5d2cdc896c48bf353c5a', '/.git/lost-found/other/2f807662ed402a67cdc3a86d525264af5ff4fb7d', '/.git/lost-found/other/2fb9df715c3a1ff4dbeed9b729ca8722ebabe729', '/.git/lost-found/other/2fe7004545a2ce0c6214b6c75bcad75dbec8f434', '/.git/lost-found/other/2fff44f43f90bd8988761555f56630209e29f777', '/.git/lost-found/other/302b17514cd5a0c86a73900453a45021c8a6c77f', '/.git/lost-found/other/3040605d4918eca0701e2a541826d735e153871a', '/.git/lost-found/other/306a8becbe8f0d8eab7964b3986c9f94ff283e20', '/.git/lost-found/other/306e5950b0fcee534e38083a1536591ce18ed5e8', '/.git/lost-found/other/30ab4115f80c0bf921117640ff7c490947ad6202', '/.git/lost-found/other/30fcd7b29e19f40daebc1ce7d83b37c394250cff', '/.git/lost-found/other/30fe180b7dc5a182beaa893a2cea5b43e407312b', '/.git/lost-found/other/312308f273d963ad2f881e414e6dc908c7de72c6', '/.git/lost-found/other/312e11e2186827cecd4ccdb5f99b25b16de8e422', '/.git/lost-found/other/313257cee583598c2b1e76531aee4382a34ae791', '/.git/lost-found/other/316871d9d0ef4a615b8cd3e853225ef2a3b19c95', '/.git/lost-found/other/3168c2f06a254ab33a036ed9a99965494aa89e44', '/.git/lost-found/other/3176ec4eb6c6c275fe82fa458715a968e6073475', '/.git/lost-found/other/318a95b28c7fa29873933d535636860233bfe2a2', '/.git/lost-found/other/31919cbc2e7b9a6268f7bd5ade6a59d4902b52dd', '/.git/lost-found/other/319c61cf6810319b6333dbda3ffcf61438c2b9db', '/.git/lost-found/other/31e4b72c2638192bd9b6ff9894f15b4365be6f7e', '/.git/lost-found/other/31e88c3eb7be2600a07f8a293e0d521af54d6577', '/.git/lost-found/other/31f64f6e3b537ebaddf428c4cb7764d746510f2b', '/.git/lost-found/other/322ad23a9b2322a5eafbb97fd34f393402a04544', '/.git/lost-found/other/323f82bbbb2a2f435ba1a70ab85e6e604de01b6e', '/.git/lost-found/other/325706343725c6011b78dbccbe34e242657d5d49', '/.git/lost-found/other/327e8f6219bc9ac3aaf5c4e5f8a88559dd9c8d9c', '/.git/lost-found/other/32858e6be0b09a988b9b7722bed3b4ac6acf2711', '/.git/lost-found/other/328bc3afc9053e448e43ac838fbde8b5a6bff782', '/.git/lost-found/other/32b556713e2c319d927537477bda7dd391634e9a', '/.git/lost-found/other/32f8032b0690c3e5ab5788e9a392fb328fdde7e4', '/.git/lost-found/other/332c5bfc92dcc95b0fdab72fec060f0f1fde04f7', '/.git/lost-found/other/338787f9553f8178de800ae15ef7a23d4f096f13', '/.git/lost-found/other/33a71c56250cf2a2cf3bc20447d3bc0f4722b8c0', '/.git/lost-found/other/33c258c67e23b0e16815b8156accbe52ea0f47ae', '/.git/lost-found/other/33d111952f9df6dd8776978e49e1067a8bbcc82b', '/.git/lost-found/other/3407448373b50404341f30cfe3e19da4562e5b61', '/.git/lost-found/other/341580a820d2cd018774a99fd90cdd4928badc68', '/.git/lost-found/other/3480592152b095df8c4308029978a60900113bbf', '/.git/lost-found/other/34c6a03cca3744f90eb635e4a427cf083aad4110', '/.git/lost-found/other/34e68b2d3472d9f5c822bb72c9fc2c4ddb3f31a6', '/.git/lost-found/other/353eeeb90d31595d072017c457bdb335470c0b79', '/.git/lost-found/other/35425eeca676d4342ab62ffff6195d41b11f03ba', '/.git/lost-found/other/355ff84b964cd582bf1f677e33941403e9647582', '/.git/lost-found/other/357377a3e9d1596994eb7db5c89ea3b40161b48a', '/.git/lost-found/other/35942a0a0c5905e8a31fbdd947ee83d6135330d6', '/.git/lost-found/other/3598090e6a420d70ef76bde587c93ade0de2721e', '/.git/lost-found/other/35c6bf791767e8c12735840b07aaff1273f0435d', '/.git/lost-found/other/36228b5f70a00e5ce49800e5c4e6f423a864ae65', '/.git/lost-found/other/362381263cf3f80b5818de655e9053e7f11cdd9f', '/.git/lost-found/other/3627eb8009d622db55d0b115ad04a86af57dc99d', '/.git/lost-found/other/362dfe3c7cf298171bd42d395215477fc4996729', '/.git/lost-found/other/3632196771add5fcb90e466f66e477f671b35212', '/.git/lost-found/other/365be8f94d80e5067929f7549396a0e85134c387', '/.git/lost-found/other/36943e9cf8334b2d66b1b289b0477923183c99ce', '/.git/lost-found/other/36d35fe01b77481fe1e61d9f5cb7270df4fe7a68', '/.git/lost-found/other/36e7091b7fbff7d70e65f68a180bd36231bbeaae', '/.git/lost-found/other/36f21339d64c30f61addd97c3c411376231a882d', '/.git/lost-found/other/371991836494764af4d1bf157fb9ef9baf12051a', '/.git/lost-found/other/3731c5b1a9613854aafe4ca48509e0a5447058b5', '/.git/lost-found/other/376c1e88772f0558744c3ec5bf33e514bcbfa5f4', '/.git/lost-found/other/378b9fa979fd0cdcd74fb98be8f965fc64ba96ab', '/.git/lost-found/other/37a0ca6cc8794e5b4800cad42666f43d1593da69', '/.git/lost-found/other/37ab16fcbeb235841f49b53dda4f8a4cb8576605', '/.git/lost-found/other/37b0cc2012a9a29b9126c2222045b25cf5b61c05', '/.git/lost-found/other/37b1dbfa62553742da17b93f4fb2997a706ad491', '/.git/lost-found/other/37c80b6e3cd1ba73b73a863658651fedc19934d8', '/.git/lost-found/other/37eb658dd959056bdc91ca5add0c61677dd55131', '/.git/lost-found/other/38078e333be4a14ae2436aba441dd97d2d37acd1', '/.git/lost-found/other/3893a9d23c221f7a7587b3bd1bbce3e53451a36b', '/.git/lost-found/other/38a1a54a9daf5b271d9479b93a8af42e6c3731d2', '/.git/lost-found/other/38c69c470dbb40ae7c309888b1d1250f91ecdfe3', '/.git/lost-found/other/3928dccc158026c5d3bd664415ca5ce646555231', '/.git/lost-found/other/3932a7771a6417aaa5625d39bb52f63e9d5ecf03', '/.git/lost-found/other/393d937812a14bacba39114d3fbc6ba4b6f687e1', '/.git/lost-found/other/393f72379d2551529e19191f444ca8ac0324cc09', '/.git/lost-found/other/393f9a985c2a03394a2e4a7eecdf783ab4ad0993', '/.git/lost-found/other/39654433fd10a74f799c2e6d20c1faa49b0ec715', '/.git/lost-found/other/397ec1001cf0afcf62fe6b20e898ed46571f0cd5', '/.git/lost-found/other/398f7fdb157e0e718ddb1b583446c83525a9c8c8', '/.git/lost-found/other/39e7fb971ecd00a92d0ac87b16b10fd7dfc091a2', '/.git/lost-found/other/3a6fb490b61ef395f241c15652f46c571c0d4ff0', '/.git/lost-found/other/3a9c2f93081539b6786aaecb9961f15db261b7cc', '/.git/lost-found/other/3aa11aec8ea158ebe6fa2976edaac47f213d098c', '/.git/lost-found/other/3abda6ffef0e775951dfeda9637eb16314baaead', '/.git/lost-found/other/3acc108aed44025f56b47a7481ef7df3bdba7c98', '/.git/lost-found/other/3ad3ad101a41a3f5f7cb1ff2f8ac7fdbd4fbb1e4', '/.git/lost-found/other/3ae1b05c2a5d648e1e234162415c93a2d566455a', '/.git/lost-found/other/3b05a03bfb9b84a6f82a3f6b6d4fddb652001ca6', '/.git/lost-found/other/3ba38eeb4c4dc8a5029fa4c435a97b9bf9cb9c5b', '/.git/lost-found/other/3bdfe3e50659109f92b7cea294e2c2ccded7e07f', '/.git/lost-found/other/3c27c38977ce104a2f4a88b49b560e41090430d1', '/.git/lost-found/other/3c2a0da42d395f055ae2c4ece3d6d56b95ed0f01', '/.git/lost-found/other/3c8b5c679d9eb3dbd857a4bc2414e018507dfacd', '/.git/lost-found/other/3cbae7783af35d2629fd5daa444b860b54c1c541', '/.git/lost-found/other/3cc5321661d71bea5e919b2dd222d55638ef6474', '/.git/lost-found/other/3d1412302b68c0d01f1afda6130e8ef38906d800', '/.git/lost-found/other/3d2058541bd6f85fa9d3041eeb94773535041b4e', '/.git/lost-found/other/3d4090fbbcedee422c984f49d6951366d6e87331', '/.git/lost-found/other/3d5b8e81ff03360ac6eace0f9658f95dc3aaaab4', '/.git/lost-found/other/3d6ce554450436c4ee02e9238d7bee54a5c98a8a', '/.git/lost-found/other/3d76e8038eb8c5d0065da0f378418b0929a3e1c7', '/.git/lost-found/other/3dee1d10be4dc43fdf33e57816608eb7f5f762e9', '/.git/lost-found/other/3dfafe83a756a154636a42148009fc2f995374b6', '/.git/lost-found/other/3e66b1694740b2e545f26acf8a011934e713ac32', '/.git/lost-found/other/3e6ff38fa95be1c55c68ef2ea46946f569926f38', '/.git/lost-found/other/3e846e06d434e3be0646f8d8c73c8be9f548eb22', '/.git/lost-found/other/3ec37580b08a3f792df050067bd3383ad9c01df9', '/.git/lost-found/other/3ecc52a19ba9501ffdc2b0775d42316e3eb031db', '/.git/lost-found/other/3ede7dabe843ee07ced13269bd65b72c34b9b5d6', '/.git/lost-found/other/3edf7805dd24b80e8c991aefa453b6e60371e47b', '/.git/lost-found/other/3eea2cd0368389b3b358ffb2050310a8e5f01084', '/.git/lost-found/other/3f24447ae77e74087e11e85cdb792de9af39d23b', '/.git/lost-found/other/3f325646ce7bfe0e26c28c1e3ed2d2717812bda7', '/.git/lost-found/other/3f343eb336812ac82de7a282f46dd867f06f141d', '/.git/lost-found/other/3f5e76235147c70911902e9f103daf1a7314e95a', '/.git/lost-found/other/3f77999b57ace248e5dc167ef4e26b985531f944', '/.git/lost-found/other/3f980f549b46e7260f2214367a43deb12d0ef4b7', '/.git/lost-found/other/3f9fdb89a31a02a343b2b0b6b3e21fc7ca7d581b', '/.git/lost-found/other/3fca9ac2547a9940b5a04731b6524c73b9b17c78', '/.git/lost-found/other/3fdcc274f28047cac793cf86aed310300180bc2d', '/.git/lost-found/other/3feb49e8ddc04e5c3e85ae2ec34908b7ea1236c6', '/.git/lost-found/other/4022468256542bc3fe6c5cead30dd9c90615fd3b', '/.git/lost-found/other/402864b837e70ae54de89eb82cbe93546cf2695a', '/.git/lost-found/other/40758f589a15d70a0fb173d1dd0cd93c2b280b20', '/.git/lost-found/other/40a67f757ceef8b9e10d6f06e5b2ec8c75529ae6', '/.git/lost-found/other/40a857d2f4d88afe60d9d223c3874cb9ccb4a55c', '/.git/lost-found/other/410fd0e93a275523e38efd323fcbb83b8c8831fd', '/.git/lost-found/other/411b53810429fd3db2d870952d8c267659517b00', '/.git/lost-found/other/4158634eeaf9ee3f387b133b1fad878f8bf4c596', '/.git/lost-found/other/41d692718cca7d01e7f6785a5d39d34b0cd79664', '/.git/lost-found/other/41ebfa1a4e684dff0756a2297687708b98e178ac', '/.git/lost-found/other/421881dda370e44a27a3e93dc9caa1d44579a990', '/.git/lost-found/other/423b3458604e6efbe12f4620e1e5e7d0044acda1', '/.git/lost-found/other/4262aa86595198148b5c5af75bd5b347d55e6d4a', '/.git/lost-found/other/428a345dcc183804917d5077052693bb113f74e0', '/.git/lost-found/other/429074a78b514abba6f272bd54f3011a72c28afc', '/.git/lost-found/other/42b5b3341164d4bfd41c4b45e85850bf626b8ebc', '/.git/lost-found/other/42ca4054cbaf5d4c01d024bd7ee0918efc52ab07', '/.git/lost-found/other/42ebc146732d966d28b3dc12887b8f73ce4c4fd7', '/.git/lost-found/other/42ed76e3d2c1af07d1c2b357409e0630ded68c74', '/.git/lost-found/other/42fcf8ab7e1224020d789b4b47b37e4eff58c62f', '/.git/lost-found/other/43294817109e7ecb22f6b65e069a13b8270d1053', '/.git/lost-found/other/433079b36165ec24a2b3bfa3208be0e72c68112c', '/.git/lost-found/other/435a5c0d738969e6f5c3f22e6c83e385fbfd025a', '/.git/lost-found/other/4367533bb415365afca5247c8006e707527136df', '/.git/lost-found/other/4371fbe557c2492b0303af5861b007b2b20ea8c4', '/.git/lost-found/other/4379e78e42681a9c944ced94d3e215fef675fe57', '/.git/lost-found/other/437a496118d962d30110b9550c9933470f544b31', '/.git/lost-found/other/4396b48a65707e8d7917f9be1a2f6c18bc175683', '/.git/lost-found/other/43cd46747974e7eaefd6bc4515e802a3f16a787b', '/.git/lost-found/other/43d8aa62d08f1788f22545bcad2bdf344ae95c64', '/.git/lost-found/other/445b7add6b22f31d6169b6fb04c94aaeaafd23c7', '/.git/lost-found/other/4464c2c8a128a1cd27d261d90e6d66fa913160e9', '/.git/lost-found/other/447720e79a8bf68b0570557e2603109333a4a04a', '/.git/lost-found/other/447def406e0b202e5959a50704be5779c5793fa2', '/.git/lost-found/other/44d6e7a95ef488d9350b45e9cfa358ce04beec08', '/.git/lost-found/other/44e59e3cec45d7396ac73e863ced62a8d7f5c46b', '/.git/lost-found/other/44ebc6510ba8445a4f02160a7d4562395a9db5a5', '/.git/lost-found/other/45055281879d94949ebe9a279d805f909fa52808', '/.git/lost-found/other/45485f8473f8fb74c608c1215de7a9ae5b767a32', '/.git/lost-found/other/45969488a2aa771c9c0a5ac56fa58505d7aeecc5', '/.git/lost-found/other/45c2226188811a624b5a22e20465e156c9863894', '/.git/lost-found/other/460a7a8399d7b7db69e999894ed5f6a244e69d20', '/.git/lost-found/other/461886c6ac2b8d4e6ba0943a72403df1d6968569', '/.git/lost-found/other/4630a38916d765d913e0e6040a11b6132baa36e6', '/.git/lost-found/other/464073b94e8df746f5abf60322e5bc23c78508e7', '/.git/lost-found/other/4660835e392b7dd46c5e7ffc6a6f765a7a67478f', '/.git/lost-found/other/4678157d773d5c250ee875f3fc5ad8cfbb06ae38', '/.git/lost-found/other/46c6456223387aec0a7b111a58be75f442f3c342', '/.git/lost-found/other/46f574b31ea9c081d10dbc24fb57ba3e4b447b6f', '/.git/lost-found/other/472070c0c081ef4c9ea5e73fce87dec51a5e50bd', '/.git/lost-found/other/473daf24f1e540b2f25a569f819a238aacb81035', '/.git/lost-found/other/47b03dd951e4d464d01dd59f62c2b67f84506cc5', '/.git/lost-found/other/47eec38c60613993ebddfe34b03b3c993405009b', '/.git/lost-found/other/480ca1cfc93e3be2b2d88a08f067f9f8875022e2', '/.git/lost-found/other/48355610f438c75b706f3d1b9bb15c49f849800d', '/.git/lost-found/other/485ebc0e3b351a9997f0bd7231ed34ebdc5eba4e', '/.git/lost-found/other/48e9b14b31df8db282aeb8c13c7196186d5eaf72', '/.git/lost-found/other/497261e3c8906476c12d6208e965b9194d2ccd9f', '/.git/lost-found/other/49750a24fedc98c1d3f489355165462ef5f0c3a6', '/.git/lost-found/other/49e4545b844c30e3a2dfd5283289f27650feed77', '/.git/lost-found/other/49e5c2487096098aa82596f7c3bf4b154b03263b', '/.git/lost-found/other/4a1b4edccdef931f7401b221ca7b97904c5f9eca', '/.git/lost-found/other/4a4fed6a266a06c70783a57203e735d40084f4b5', '/.git/lost-found/other/4a561130f0ef82f6839112aea65b7c41d857f15a', '/.git/lost-found/other/4a64f6a423d13664596ad8952e9a991142c575b3', '/.git/lost-found/other/4a7421627f436e26ec2e56d8ebfee4e5b009e05f', '/.git/lost-found/other/4a9614ed45b8c3c446af97804ee70fae5cee33ee', '/.git/lost-found/other/4aa09bd0167a59b088b2c27f326b600029e93e56', '/.git/lost-found/other/4aa9736811f8b92b79e2fb5044fedd3827eaae85', '/.git/lost-found/other/4acce9508c07accfcb472ac7b53df59993547757', '/.git/lost-found/other/4addd3a9cd275d18232024a8986d0a71719be52f', '/.git/lost-found/other/4b0ca8a212de55c027ab38e37ffcd17e341d57bc', '/.git/lost-found/other/4b1106adc7b4c0535779dc0c2df302e2e4f26afb', '/.git/lost-found/other/4b16c36c5bbdd7a8a0aeeb449e081c80e2b75d01', '/.git/lost-found/other/4b4e6a0046c053a95f57754b9088a81834674349', '/.git/lost-found/other/4b5c220106e4b150f1785aca51b4c1516ee7f6f7', '/.git/lost-found/other/4b825dc642cb6eb9a060e54bf8d69288fbee4904', '/.git/lost-found/other/4ba7d47f279b001eb96215df8833b8c2cb201c3e', '/.git/lost-found/other/4c109c4291b72213236a54418e69bc70989d3d23', '/.git/lost-found/other/4c3c101d419f879404ff9994e148420b95f8ad60', '/.git/lost-found/other/4c493eb24622138649cb71acb19118998e7e55d5', '/.git/lost-found/other/4c5e7bcd16c8cb7d806fb0fff610e8f4c5db8de2', '/.git/lost-found/other/4caa0b8605ba9a8a10d09fa28ab020b5634c8f6d', '/.git/lost-found/other/4cd6f7724ce8848c6e3b4a92fbd8d8ee2c9fd8bf', '/.git/lost-found/other/4cde126dbb4465d93bf6a56e0f7557664cad7052', '/.git/lost-found/other/4d64eae0c3986894803d586d4c44ae16906d23f8', '/.git/lost-found/other/4d77a00c84211f3b1f7d0b33a9c650a0068ca57c', '/.git/lost-found/other/4dae699298c4e827eb777a620bc2b0b622a3d043', '/.git/lost-found/other/4daf2d4fb4be2002d0c6f0783065cd4aaa2ef9d5', '/.git/lost-found/other/4db248d2d0362a2baa123bce350af1c3cf725718', '/.git/lost-found/other/4dba40158ad402bdb18ab94f570242af2ecb9f72', '/.git/lost-found/other/4dc581629639bdbf6136e78e94203ab183c60871', '/.git/lost-found/other/4ddb67d026b4d1d9533591627008838db3040342', '/.git/lost-found/other/4ddead2405965902636a6bf032847bea1dcec5e7', '/.git/lost-found/other/4e560d39e66ee48393ac86adf8bf92f390ab6282', '/.git/lost-found/other/4e57556929f069e1d92ef1cedeadbdd46be69462', '/.git/lost-found/other/4e6cbaaa682013b3b168c0079f78acc0ccfe0552', '/.git/lost-found/other/4e80ac0c1f3b8a9f86cdccef454912a80077d15a', '/.git/lost-found/other/4ed608f4d1b961b4b069673f0dac7b286868f1d4', '/.git/lost-found/other/4eded7a6a9ba555dac903ab553ad0640bfafd803', '/.git/lost-found/other/4ef1590a8b7ddbc3f4fa8977aac9094f931283b4', '/.git/lost-found/other/4ef73eba22c74702bab0fa911b27145fe6efd727', '/.git/lost-found/other/4efd0c308d4fa547f805bf82210e817bc8739939', '/.git/lost-found/other/4f03978e25b1d70dd18b2f1ce83f070616bee53c', '/.git/lost-found/other/4f6403a8bcb6c19a368e929b9a4e12741e1ab55a', '/.git/lost-found/other/4f7bed90c38a4cbb348c4ad64255d11ed01043f3', '/.git/lost-found/other/4fb85fbb7c372a0b84cd78fa6b55e410e220239f', '/.git/lost-found/other/4ff93b7412dfd5e731ca509fefec5e2a910528fd', '/.git/lost-found/other/503b52b471cf3c48677445669dda1dda8fd71c51', '/.git/lost-found/other/50446582fea97fa549a6039a5f0c504364f69e73', '/.git/lost-found/other/5052541bd836a255d6414f0d6caf7cb46ce878a9', '/.git/lost-found/other/5056e85cfcdc5e48302a6ea6e308e29ec17154a3', '/.git/lost-found/other/50641e34bbca5261e3460924a6ad4cca4eb1e681', '/.git/lost-found/other/509b71d4704b84a1ffce51e2639bd836b3493ff4', '/.git/lost-found/other/509ba1ee9c66d67aa12183a23911275c84c1be12', '/.git/lost-found/other/50ab5d3cf546c8b875e8c8fecb728a69ed6129e1', '/.git/lost-found/other/50bf8437d9f0ba4f1b5bda9f3cfdff66feafd872', '/.git/lost-found/other/50c32b19907ec29e0df34ae3dcb64ccbad1bfeed', '/.git/lost-found/other/50cf16ba1f7cdef0e11f3e689c2ac0c4146c23df', '/.git/lost-found/other/510a9de17bb3cb81c8d9dffaff39e6a1ffc8d46e', '/.git/lost-found/other/5135c970168de2f80375b8e8223d8b65ebe722d9', '/.git/lost-found/other/514ef7a257573e892fef8efdc8092aa113f301a6', '/.git/lost-found/other/515672a3eac687eeaa0d5331a88ae03e9eec92ff', '/.git/lost-found/other/516400f538a8bb12359bf8121ffc8de0d1ece0a5', '/.git/lost-found/other/5177cddf0421903b5a7667854f6e1447853266df', '/.git/lost-found/other/517936a6f2e958e3c291ca7426694acc1c9ed684', '/.git/lost-found/other/51ead710372b626f38f784b6b56245267e896e06', '/.git/lost-found/other/51eddaf2d727e3973ab74f8d0d4d5d6925dfccf8', '/.git/lost-found/other/51fc32836d05581c65f4f62453fd8461eae64d47', '/.git/lost-found/other/5207df72e6c942df0f5a50074a13d02c5c6fcf92', '/.git/lost-found/other/520f6d14e206018e609af947049cff9cc8242353', '/.git/lost-found/other/5212c909d3b94b54efd1b8e83b0ae14bfd060e6b', '/.git/lost-found/other/523cfd7c6c11e165293fcbe926464d35abe0f7ea', '/.git/lost-found/other/52510e1da02780de64cb636dbeb5322763d39bc0', '/.git/lost-found/other/52631f7dd5d612089d235a84853c538dcfc63d39', '/.git/lost-found/other/526cbab8a8237857d96750d81938f8548229fdd4', '/.git/lost-found/other/528c0f551f1529db0685ebfb83fb5bcc0d13a715', '/.git/lost-found/other/52a9fd5d5a39c98cf011809f1954ce924858033a', '/.git/lost-found/other/52bd08e69825f02027ca3f99833ed05df89c9347', '/.git/lost-found/other/52ee24e4476554b49c7f5f84227ce066a0a46f9f', '/.git/lost-found/other/5321249b535a38dd91115955e2aa31639d2a7306', '/.git/lost-found/other/53989b292aea8588bedee021ac45dcefddb3caf5', '/.git/lost-found/other/539c77ebea4b39f981394f47d5682778d9282819', '/.git/lost-found/other/53c00c790d7213e762a416ccbd9fa61f2cc6b27c', '/.git/lost-found/other/53f1494b9ccdf2520caf09f9b6c9b0b6fe832f22', '/.git/lost-found/other/53fbe0eab185e254c6f27d57abc84dcdfd0223a9', '/.git/lost-found/other/5400429d73c66a98a7d7f803984889b2cf64f643', '/.git/lost-found/other/5415418c0097755bce371e51342cd16532d8fbe5', '/.git/lost-found/other/5424e6ee1e37bb5033742e0579176168ba0eb42e', '/.git/lost-found/other/54348c264bfa80b99bc179182d9d4400da05a8c1', '/.git/lost-found/other/54437ef622b766cd31a65735951ceb6b1f3dbd97', '/.git/lost-found/other/5444fe59b494246baf22bfe218d9f62cea416fc8', '/.git/lost-found/other/5459e50a37091210db1c5703a61149ff7366f367', '/.git/lost-found/other/5483d2dab97c022bd6d8bdbe5e7e91a0bb14d17d', '/.git/lost-found/other/54946c6df52fbea6e5f86390fa9fd5a6d9b8c581', '/.git/lost-found/other/549ef64d2ed3890a06bd03ef59952b31b70a5027', '/.git/lost-found/other/54a23401d7ac4923367c12c897f2444dcc00fe83', '/.git/lost-found/other/54a41810fd052d9463f8d60abf2c75184362b839', '/.git/lost-found/other/5541601d03b6f8e0c6c01342973a66430d8b0a50', '/.git/lost-found/other/55616d36043061c1a3c7f616e099f6a5abde1e72', '/.git/lost-found/other/55769048317ffd40eca0be3cea5a4b9e5ab7cdba', '/.git/lost-found/other/55804d3108a2a367b825f5cf1bb797755f5ada1a', '/.git/lost-found/other/55853255cc94e3efded0c03bbd00de39d57a7ce5', '/.git/lost-found/other/55992f60276d8ca420b03e6af91ed8af74fab670', '/.git/lost-found/other/559baa54efe7fb5e41f2551d2ca8e03f87ca5f0c', '/.git/lost-found/other/55b747cbbaf511f4d5424f0f1301ed30b1916007', '/.git/lost-found/other/5624bee17cfdf365584b8229349e7d5778a96c07', '/.git/lost-found/other/564f7f5c55645405bd63d23bc0315154baa54c18', '/.git/lost-found/other/56943cdf18ab772ff17cd18821c0cb38f040c874', '/.git/lost-found/other/56a2b9f0ddb3eea735b36c89c4433d9800483f7a', '/.git/lost-found/other/56e2a20d652ee923dad7ebb9d8aeda679efae502', '/.git/lost-found/other/56ea5e17523abc029922afcc9f23f2306cfef729', '/.git/lost-found/other/56f07bf7f1652d395100a1b2e0b96ed2b54e171c', '/.git/lost-found/other/56f3b2f52e650607bcb68a0a89e36251acb754f3', '/.git/lost-found/other/57707d21bc0c5ccc78a5b479538fa8f4af03b517', '/.git/lost-found/other/5796390469d48d2c75ad156f8f3c2e1054695731', '/.git/lost-found/other/57b04ada3b0285ca34c1a7fdbb9c904e484a2d14', '/.git/lost-found/other/57d46027e0e2507d28ac3ab8a433fb6035544f95', '/.git/lost-found/other/57d4a6120719f112e80cebbf59c497f211238fe7', '/.git/lost-found/other/57ef49de52a2d19fe06f40aa614014bbea9935bb', '/.git/lost-found/other/581d582546277573b28d5812835faa2ade024e61', '/.git/lost-found/other/589ef170d33fd55b085f70295ceebad9b7d6eb8d', '/.git/lost-found/other/58bf0f7e675b7588a79421a3fabaf0f35e219290', '/.git/lost-found/other/58cee47fb9ef92895314fdb4ea00faa945434e52', '/.git/lost-found/other/58d03866cf23187801f46939ec2328e2dc8c05b1', '/.git/lost-found/other/5905f9d6c104fcf3db9d8f19e6dcbde6149a6d03', '/.git/lost-found/other/590af4dd3c7d105d3ad2866312585bff30d02804', '/.git/lost-found/other/5928f67430c179dc2031c576bf0b24b51d2bca5b', '/.git/lost-found/other/5971fe317cc2404af9f0717140a87f15b0c0b55f', '/.git/lost-found/other/5983ea75fd9362c5a8709fb10cdfa4920f085b40', '/.git/lost-found/other/599223087cf2abf27e92dbb63ca3402862306cb5', '/.git/lost-found/other/59a6d7ca7e0bd39f24f74469da806dd2659236c9', '/.git/lost-found/other/59b78eed07eafbf8ed57b97a459a61e949c07b14', '/.git/lost-found/other/59d110fe6522d55e8e5f8650763f5ff86c935b7e', '/.git/lost-found/other/5a1e4a159d9cbf9d18e6e0da20f04e709b36e923', '/.git/lost-found/other/5a41118850b5b97764e3861fc59a901f69f18298', '/.git/lost-found/other/5ab3284a5abce4c25306590d08b3b50e8d0dfe01', '/.git/lost-found/other/5ae30190da5996be8b0111d18fe276b95d8e3ba6', '/.git/lost-found/other/5aed03d61d3a40a4e4d8859a43e5ff373d789afb', '/.git/lost-found/other/5af7955eaaa535c9f41527d8cab24ed5c1388305', '/.git/lost-found/other/5b03c014dcf3dab20b88f5a62dd0865020292ed4', '/.git/lost-found/other/5b3c284ca03de4c25ced51e9aa3a4b488804a44e', '/.git/lost-found/other/5b42a5fe2abb1393cf2b9ac7359176e4aed00c0a', '/.git/lost-found/other/5b5d27407a7bd2a7d7a767409ea402d354a9a684', '/.git/lost-found/other/5ba55edd28d0248f250495d47f6ab87821817c15', '/.git/lost-found/other/5bf68c1c51dae67f6a925c6ffcc4e45d0ee9c27f', '/.git/lost-found/other/5c1ab9aa3ef25014cdaf48ecc250f106e4abe387', '/.git/lost-found/other/5c40fd7e30b0ae67c6188ae7825d3ecbe2c432b0', '/.git/lost-found/other/5c5231a09008229e8e269d9a71bb646de28c0bd3', '/.git/lost-found/other/5c6ac7789c226f1cb333033c83401c787362e213', '/.git/lost-found/other/5c9d49cd48ff71491ca95509f601ff732142d86a', '/.git/lost-found/other/5d0c31c8d4c3150abb326fe441cf29550e85229f', '/.git/lost-found/other/5d51b2cf47c9bec0fd8dfc6a5c742839aead66d3', '/.git/lost-found/other/5d5c0bdce3886c23ef6aa2478091b71980c7b558', '/.git/lost-found/other/5d9ca220d74f6f62928d7fe74439558ac0eaddc7', '/.git/lost-found/other/5dad81834d096b45968ce3db534e06ef01cb7962', '/.git/lost-found/other/5dc8c414c8a6dcb39eead75672e29a6c7705fa1c', '/.git/lost-found/other/5dd53689515fdcdb933986493ce832b0fc154869', '/.git/lost-found/other/5df4f9798bc7768bbc0cdeaaf89cbb71fc7e2519', '/.git/lost-found/other/5e620fd25168e7c134890f30749078a81a7b6245', '/.git/lost-found/other/5e99e7ca5804c491ec01e5498d13b271c4c2f5b8', '/.git/lost-found/other/5ef0127085448a90356cab02f54d9ec9c190d13e', '/.git/lost-found/other/5f114962f8c95cc3d3e6d07ad8aceeef21cb42bc', '/.git/lost-found/other/5f278d44ee3cc96d3c7c582b2baa956cd2cedeea', '/.git/lost-found/other/5f7c76357de6ec1ef7872600c6c0d99d6fb29350', '/.git/lost-found/other/5fa52d56651eb41b51a76e9489bc3a1e803320aa', '/.git/lost-found/other/5fc241b5fc5ee3126714b7ec6bb1218f256b2f9d', '/.git/lost-found/other/5fd65f63e326d2a5a2305d4023ee3f9f9a1c7ba8', '/.git/lost-found/other/5ff9751d696b33f83abfca804807e09e998cc015', '/.git/lost-found/other/60055836c05f4130a75aa75b465c2932391fcfa7', '/.git/lost-found/other/601f2c09dd519075bfeb9db5b995db629718c821', '/.git/lost-found/other/604dca6b26bd18ef8041517b5520080d7d019360', '/.git/lost-found/other/60549f042a38455f36259a61d55c2a8a26a84f77', '/.git/lost-found/other/60737bccecfba65d47f6ce9e98a60da40dd51ab2', '/.git/lost-found/other/608826a2afc590737f32a764a625ef1f8c685dd5', '/.git/lost-found/other/608eab5a999f1dacde5212a37bb0b10c89bd5f2a', '/.git/lost-found/other/60cb3c25c404aaebac03a48a50958503db52145c', '/.git/lost-found/other/60cd35607497b333c4e689ec8c3d7beefb76d5aa', '/.git/lost-found/other/60cea4218c9d2d340270861f9084015f542aa19e', '/.git/lost-found/other/60e755f3531398a88cb2ba67af858c57dd0ab90d', '/.git/lost-found/other/61206657bd31e3e2e564ba4130c5cf5db80199d6', '/.git/lost-found/other/61240f34ff36c6a9ed178e7f3b0769d90d505ae9', '/.git/lost-found/other/6128184c716e17ff7c4382e61719214b88a65240', '/.git/lost-found/other/612b7e3dac1b05bc83204b5091634dc99d745a5f', '/.git/lost-found/other/613d1efee79b495719629da39214f79500635967', '/.git/lost-found/other/61731703e939fce963fa49e55b4af95286342a87', '/.git/lost-found/other/61ab639fb396a69f456a8a0e8161c81a66b36b50', '/.git/lost-found/other/61c62badbeadcca961fde66023da79591e056332', '/.git/lost-found/other/623e4c399c3cf78aa7bff72e26554c85f6869fe6', '/.git/lost-found/other/625248a511b95b56bb088ae1f70dfb5dee830348', '/.git/lost-found/other/625fa42e650c174cda286bf390e545c6354e1f44', '/.git/lost-found/other/627b2245b8bd0bb9433125096bdd64b99e749544', '/.git/lost-found/other/628b4dd0a93a7e16d3cbf73766ec9bae336e6116', '/.git/lost-found/other/62a41bba70c8083d3e9792ce06fcf891c6fa24d5', '/.git/lost-found/other/62b286e180ad3b353b79c522e41cac008f3512b0', '/.git/lost-found/other/62d1113d6b19143c69097fc9eddb4de615bdb653', '/.git/lost-found/other/62d972d5d66da2dc69c96c10b87c2fae3639a25d', '/.git/lost-found/other/63144637a3bd9f8474fbeb8463792c71442047b2', '/.git/lost-found/other/63491f18503bb3346888baa308185d2196d689a3', '/.git/lost-found/other/636d99342c41a4943fa0ca86f1619d0573375bc6', '/.git/lost-found/other/6372d5b36494f138c1638b3930d8543e77265803', '/.git/lost-found/other/639aff1317ae109c623652e0970c161d9a80a821', '/.git/lost-found/other/63d868359a2df3e9c0ed61a522b42a15afe9462a', '/.git/lost-found/other/63e70e5456461721b42c484bbee1886cfc8ba39c', '/.git/lost-found/other/63f2e29d53169726763ff4581e6fdcd3236cdb45', '/.git/lost-found/other/64068a5fd20e95303d2a58a8f948e08cab89c31c', '/.git/lost-found/other/640ebd997c31281a5274fbfcdaf9624d3dca7042', '/.git/lost-found/other/6417cfd675c0269adda74c4af4984a8e5523b5bb', '/.git/lost-found/other/6421734fb5e632258add15277e10f9d075b83131', '/.git/lost-found/other/64e4f4a1d9a5c5f3af3076ec413de73a3f5a4100', '/.git/lost-found/other/64e99286b0f3b21b065d94749079fd3fd4e94ff1', '/.git/lost-found/other/64f99c86919eab0648c3a2fb4b9b58576a85203b', '/.git/lost-found/other/652f440f92ba723251ba6ba470744e6d192a0ea7', '/.git/lost-found/other/6589cb9582ca26898931b1ff9fa713b99a51fd69', '/.git/lost-found/other/6604d0071186e48178e9b0dfe7e979040c3e54d1', '/.git/lost-found/other/66161534878c9a2771f904c86c37771812f852de', '/.git/lost-found/other/661bf6799d7caeff91a59255c0749bb0c19e430c', '/.git/lost-found/other/6638f29e468c5eb3550c99e26aff88a106344cba', '/.git/lost-found/other/66899d38c422ab75f0919f5714961b39fb244dd4', '/.git/lost-found/other/668a493ef1fcb9d584aefd1e500fe080eb2b7488', '/.git/lost-found/other/668ed8f54785171df27bcc3dd3ca6946b7c47b03', '/.git/lost-found/other/669527a55303ac3089986dfdd5be5379da40b8d6', '/.git/lost-found/other/66a367c89a095a293497c3606593eed3675b7bab', '/.git/lost-found/other/66b958f32ddafa4f75a7a2cb2f24a9e9ccf2a097', '/.git/lost-found/other/66d6a8e4d9ed60f991a0a185966cb717770690b6', '/.git/lost-found/other/66dc9fe2e67543e8bee36d8b809fc2488132e8d1', '/.git/lost-found/other/66f40ce43c80179972266b9fb98da995998b53c3', '/.git/lost-found/other/6701c178ad1a4b00372bae3c25cfaac2c80c9c62', '/.git/lost-found/other/6702cfd9756562bfb0a3ba9b5abecffb3edd3d4d', '/.git/lost-found/other/674604affdb240288071ea569d52f55c530b19b0', '/.git/lost-found/other/674f596c4dacebc48590bc262602ede7478a42f3', '/.git/lost-found/other/676fa0f11b62b954662d9a796a91c01408e97449', '/.git/lost-found/other/67b20ca14055482a477dddac64582ac8ae5767e0', '/.git/lost-found/other/67ce18851f37a03dbd8f1912f40b0333196a565e', '/.git/lost-found/other/682c9758c717f786de009b535f7b4809bcfcb68a', '/.git/lost-found/other/6842fe827192bab8f1180cc0a667d476df9cd850', '/.git/lost-found/other/68680d91ac416db504df57a84291d630e94eab46', '/.git/lost-found/other/68749693c84ef5a049465b1b192d56aa094cafc4', '/.git/lost-found/other/687cde57acd639e44b9f6ecf4bb3b29996c10bc3', '/.git/lost-found/other/689b7fb39f59c02e4fbbcde071296721398eb013', '/.git/lost-found/other/689d0da7d061471f4527308c48e26efb792ff379', '/.git/lost-found/other/68acc160c191f8f39dd69ea2c9fd1bd132519e31', '/.git/lost-found/other/68c62d74946ba59bc95c49aa23daa2faa9d50df0', '/.git/lost-found/other/68e38676e7f2aba51f365c5246a25b26eaf7c93a', '/.git/lost-found/other/68ed276d325e028f6520a3a2139e590b668d16ba', '/.git/lost-found/other/68ee67a9c8c69cc7b4387076d19412bf6fa55a91', '/.git/lost-found/other/6916bfc4ae8a8656910be8213444648b53a2352d', '/.git/lost-found/other/6924feb7662147552bee9698d879ef0e54b6d8ac', '/.git/lost-found/other/694b515cd1cc0b2492e6d20ed85c4e0a9212cf18', '/.git/lost-found/other/695a1fc4aabfb29ae1d4eb53d8262b001cf0b268', '/.git/lost-found/other/695c4393b98dcf12334da13f5dee4b09f2e56f61', '/.git/lost-found/other/69b678f6e53c24601108dacf7be78a0f4dc9297c', '/.git/lost-found/other/69ba46d4e80a1ca1f7e61de30c5a0973bcf9949f', '/.git/lost-found/other/69d86a739e9bcdaca05986856237308c2e352b4f', '/.git/lost-found/other/69e0d35ba51506e2a6b1c82fb10836e2944f7d41', '/.git/lost-found/other/69e6486640b279c4c27df16fa42efacdf5fd5318', '/.git/lost-found/other/69ea2e3abac381e1239cca65d1ff4425a100bd06', '/.git/lost-found/other/69ef08f9dd58c1307d87a9d77fe60fa99d0c0540', '/.git/lost-found/other/69fd638c548168d2d60451a27b06ab1f4168253e', '/.git/lost-found/other/6a0e4ee850e4136089b231c7385181f3833d64e5', '/.git/lost-found/other/6a10a4c99f71d892813817d6e131c32de5a3a0b8', '/.git/lost-found/other/6a5ca58dd7f7d4ff96beef4b05385fa608ce1276', '/.git/lost-found/other/6a61b1a3a9cdedf1639d353de4c161efb37613bb', '/.git/lost-found/other/6a7c5cbb6e250ce2534ddc459ec58e94ad59daa9', '/.git/lost-found/other/6ab43d1c8712b075016024e6de4b2cedad30d4fb', '/.git/lost-found/other/6ab5f05565940fa70b59ade18d5824d49687af69', '/.git/lost-found/other/6ab7a9816bb2bb377a0dbebd922c0f16d81c7db3', '/.git/lost-found/other/6ac3752495b076c748fd4e5c4984925643feef75', '/.git/lost-found/other/6ad46cb805dbdc2933f7591e26cf9223d5c4c09d', '/.git/lost-found/other/6add66c47d463964ce1f625054a2e62c78de0052', '/.git/lost-found/other/6af52eaf8a4268931a8ec6a132d7ee779f9b53f7', '/.git/lost-found/other/6b00c19ac5ad98cb682b6aa371330eca5c5137ea', '/.git/lost-found/other/6b22042beba9d91f0d97ac16821226b69175c861', '/.git/lost-found/other/6b35464eeba949dd63b3800fd407ec64ad156c85', '/.git/lost-found/other/6b7cbd1cdc3ecae6259e767ec077682ab8140d37', '/.git/lost-found/other/6b874d512a6169e56875de8896ae72ca50462b5a', '/.git/lost-found/other/6bb3e94d1d720c1348861e7a1dbe524b51eaace7', '/.git/lost-found/other/6bb4e0d4dd0ee5445099c82b2bd2f64a53e8d294', '/.git/lost-found/other/6c03949654187bb18a9d56abf3fa548d35436fac', '/.git/lost-found/other/6c0d651cafe38a80077e3f039cef23d0a74f61f4', '/.git/lost-found/other/6c22da847b3c7def6cd69370256886cb3df72bb1', '/.git/lost-found/other/6c5fc2bdd3439593a8643d755e206e6dfc9fc170', '/.git/lost-found/other/6c76334a601f051983003c01c0a4a9c9647d9409', '/.git/lost-found/other/6c84c530995aeb77ea4f06496152518f193072cc', '/.git/lost-found/other/6c8a6bf7a8364e9f3c66b02e8af3048c191749db', '/.git/lost-found/other/6ca4f377708c5ecf6907a214a05573cc42b26244', '/.git/lost-found/other/6cabcbec99c44d58b07d21563b56e3e3ecc9cfe5', '/.git/lost-found/other/6cdb8c84c0d8288f817da1bfc5af9d5ea100f691', '/.git/lost-found/other/6ce65d7b31135ccacfff2b3d2ab53e743f0fd75d', '/.git/lost-found/other/6d14e456c1a77b86235f00f27b0d7ff404895330', '/.git/lost-found/other/6d3808be278c3451214e6436726830d41ba7b8ea', '/.git/lost-found/other/6d3bebbbfb578533ce3e6ab76d4cfe41bc2c2802', '/.git/lost-found/other/6d4cc26ae5764ee023fc9a552bb075bfa762903b', '/.git/lost-found/other/6d52ba52a8e301203cf321217bf466872849a86e', '/.git/lost-found/other/6da26546fa1246aa176dd104defde990f03fb2d8', '/.git/lost-found/other/6dab0e6afdd91c28e48f63d3688707a18eb7dac3', '/.git/lost-found/other/6db056fef046577bfd43bd0b8f438aa337f406b2', '/.git/lost-found/other/6df408815ccc8efcd933582508681c4b44e1d871', '/.git/lost-found/other/6df878640493277c4d70736151c30bfa36d4c930', '/.git/lost-found/other/6e1a4dde1913195bcdcb1ab2c38819fdabd889a7', '/.git/lost-found/other/6e22f463b1ec7d2cd140e6e0b0e03a632aa90f06', '/.git/lost-found/other/6e4284250937e9e1f0201611e6096d4101d2d653', '/.git/lost-found/other/6e5315c52f4cb6f8f50c68116b2f12db8d110b4c', '/.git/lost-found/other/6edc0bdb4fd041efdbe26e3db5c16b7b8eeca310', '/.git/lost-found/other/6ee8d33c6149cc513fff7a4bb33af1cba643681d', '/.git/lost-found/other/6f21d6a0aeb79b7c4d3605725f306d44d94c8d27', '/.git/lost-found/other/6f2516ff42249437779576cb418ec04cb76f8024', '/.git/lost-found/other/6f2e1fed7351e51786da8d13cd287a382305f2ac', '/.git/lost-found/other/6f43d382fa76287088af7b112df53a49cba251ad', '/.git/lost-found/other/6f453918535498db9b0ac365f2433265782b6945', '/.git/lost-found/other/6f88ec227ecf2f7b141024b1d501544126a224f2', '/.git/lost-found/other/6fba22d4dc0eb6400d9414150d5b70602d6564bf', '/.git/lost-found/other/6fcf161c510c9b98c91a405a36236d1e7e6111f0', '/.git/lost-found/other/70268d1c998cfd8ff0496f00635f779488913cfc', '/.git/lost-found/other/7053cc71e49faa648cb55ce0f0bf2b206c62ad69', '/.git/lost-found/other/705469fe281823f80b2cf27ac4e097c432c0fbb8', '/.git/lost-found/other/7065f6674fe7a8235b352054611ce3983ec2b558', '/.git/lost-found/other/706a12e583fe32e25dda3d328dda9d590f7ac56f', '/.git/lost-found/other/7073db0d222f367a044b7b9a76927f51f6854823', '/.git/lost-found/other/708e1960cb8892a8a08ccca0fcb666ae281b2a16', '/.git/lost-found/other/70adf55db7d632e16f7262dbf14637069fc748f0', '/.git/lost-found/other/70d153a9884e3f575ceee6df23bed28105af19ad', '/.git/lost-found/other/70f09f86714b5f1a6772acc9824b08e5148482f8', '/.git/lost-found/other/71037982231de4a8c00ad8f13b4a6cdd81871edc', '/.git/lost-found/other/714397ace6f967f7f6c94a8446aad82e62242f3d', '/.git/lost-found/other/717ca515e3896ef68f1c05dace103215d030de33', '/.git/lost-found/other/71864276193f717598a3844fdcd23105f607a358', '/.git/lost-found/other/719a970b7bedabe76e51c19aef9d38a694ea8de8', '/.git/lost-found/other/71d32e4dda142850902ad5f13e7d833455cc1af5', '/.git/lost-found/other/71e14735682c30c4ee07a6cec6df1200444e6d14', '/.git/lost-found/other/71eff9cb705ba5e300fa3c97d8d889d379c26055', '/.git/lost-found/other/7205122093388382cab2ef86f8ca360144cf840e', '/.git/lost-found/other/721c0dd9c7733231be83aaabfd84464df8fb6044', '/.git/lost-found/other/7262a805bc2dddcb9400604a9c1e96b639fe1980', '/.git/lost-found/other/728c2ace778aeceb83e85f1bcde65cb271b6a15a', '/.git/lost-found/other/72b893688930c0a1af79d22f43abdb9006cee638', '/.git/lost-found/other/72bd91acc1b928d0be23a4a1256e69866fef734d', '/.git/lost-found/other/72ebd6a7cfdb38fcc2e0b29564a3b301f7782e32', '/.git/lost-found/other/734c82bc74fe1b035bf19a2c11233de87a528867', '/.git/lost-found/other/736a5f16704e8ac0e55a5a0eb3ca0341a6876e2b', '/.git/lost-found/other/738f6025afd72bb0175981a02cdbe76332d58329', '/.git/lost-found/other/739407bd14c0325d37aa5425b9ba3a92ddd47492', '/.git/lost-found/other/73dbad59cff4bd2f2c9349d428ea128acd9bff1c', '/.git/lost-found/other/73dfb5017aa8a0422396ca3bab010f8b0cf8340e', '/.git/lost-found/other/73fa97fd287d2dbdf544f5995bf4f80996e8dc14', '/.git/lost-found/other/7430dfa1e58986db8aacad7d76e64ea2a4a867eb', '/.git/lost-found/other/746b115d9387d45539bfaa7450c2d5af731614ef', '/.git/lost-found/other/74a77663a7cdfae6de127ccbfd7657aa043d6968', '/.git/lost-found/other/74c55be61fc8e1927fa6bf118fe52417a16ea98e', '/.git/lost-found/other/74ee664d939f3792fbf8c5de69ff5000a85e823a', '/.git/lost-found/other/74f0c172448a0aa50fb351f2512e47ab598c02ce', '/.git/lost-found/other/74fe5ea272dbcc8fddcdda0f3dc95a4baf6cc2d5', '/.git/lost-found/other/7521408ed06b94dc61465eb18f0de0112d662dfd', '/.git/lost-found/other/754093e7ab1ec13ed0596ba6c02d18dfb8f63104', '/.git/lost-found/other/75526bb0823b577cea9abea7a8e2d68880b4a56a', '/.git/lost-found/other/7563c407d2437ca7e9fe67a0bdcfbe9439559381', '/.git/lost-found/other/757a9f890df07ca2d991d61cbaabe564c1e908eb', '/.git/lost-found/other/75c449fb1c46c708d4282f2fc0c05d84b330728d', '/.git/lost-found/other/75ce886dd4b67eacf026e8976df7fdebbd4bbf15', '/.git/lost-found/other/75e403200b7c6f1e192ff409078d9539db59d5f9', '/.git/lost-found/other/75e83fad04dd51437daa3c32f8f69a6d0f1327c1', '/.git/lost-found/other/762405ef38fefcce716ce0ce148eeeb530e1e89a', '/.git/lost-found/other/763ddec02d2f9992db9e15ccdd04bc7a7eaf6b88', '/.git/lost-found/other/76645041e232c0adaa22acfe2ec719c5a504da3b', '/.git/lost-found/other/766c4871825fe6833348baad04d8aa11521a76c0', '/.git/lost-found/other/768bd9115951b30cf63873a24273425fea0d9460', '/.git/lost-found/other/769c1bb07714a82c3cd25c50f256f28519da231c', '/.git/lost-found/other/76d1f0ada5f99a0596db6f9b5f474d237450a49a', '/.git/lost-found/other/76fe1b6791b8ade1abf97bc01a4f669ca22bdf25', '/.git/lost-found/other/771d4dfee6367426c05c3d82559b5c866bf59ed8', '/.git/lost-found/other/77349909732fef77c64241e680e95994b7ab6894', '/.git/lost-found/other/7758d6660a098f9b40547314cac71582703a5c42', '/.git/lost-found/other/776a4bea95d8e9f4deeb6e136104a5d9080dbf4b', '/.git/lost-found/other/7776476fe91837a89851f29a87883844a29f1065', '/.git/lost-found/other/777c96837cb78e1e50a9d82e0c0bf6c555dba8a3', '/.git/lost-found/other/77de4ba2f2aef9696037ea20f5e791ec8fc33796', '/.git/lost-found/other/77e3948ebbd8863edb49b35b86613591d4c3a2fc', '/.git/lost-found/other/782871526d2a991f40100b5e32cd3ef1fa465125', '/.git/lost-found/other/783170539a1f735ce74f00faf966344072add26c', '/.git/lost-found/other/784048e81a3c695bf56127d23ce99557dbf5795f', '/.git/lost-found/other/784354371cba3231fbd5c9e2238ecabb9294c35f', '/.git/lost-found/other/78597a307d1679b079e99777b55023130a6905a8', '/.git/lost-found/other/78dda83637c001a3bbb5b46fbed552151ed51365', '/.git/lost-found/other/78e7d0c901ee8eeda3825be8d83a7bd2a65ac2c8', '/.git/lost-found/other/790cbbdb4670edaa8647b93e6e6c5a9fc4aaac3a', '/.git/lost-found/other/794f8566651960a583962f1445dd3f2b2cec3a1a', '/.git/lost-found/other/79824891a2ff44dd5a6b02039d317d363d9acc31', '/.git/lost-found/other/7996e753f0d39ff8510fa714661f86e7b916a821', '/.git/lost-found/other/79ae734789ab6ce0d184cc720e51c101d3ee0f59', '/.git/lost-found/other/79d34e1c1b4ef979275fb6c28c00dcc936dbbb31', '/.git/lost-found/other/79e13fdae10173de3edfc81b7d1f5cf09e950ccf', '/.git/lost-found/other/79f4d07757c8ada811eacfaa0ffc677b0b6993c4', '/.git/lost-found/other/79f69779814971b10ed2d61cb420b58981837c5c', '/.git/lost-found/other/7a37e0c59d04f44e91bee825ca3178653503fe27', '/.git/lost-found/other/7a60567d3255257a8ec8ffd90b47253fbb7779e1', '/.git/lost-found/other/7a72a47df56ffd23bb383a56ae637e4045424316', '/.git/lost-found/other/7a761a5bd14d2eb15e7fc3dfa4290f5d112ec66c', '/.git/lost-found/other/7aa8a776509d35c4b416ce478c310947105abb78', '/.git/lost-found/other/7ad2274d82286b18ce5a0790edb400eb0246c04f', '/.git/lost-found/other/7ad4e5dfb7fe46e62e7ee90c8437b3cd1c98569e', '/.git/lost-found/other/7af76ad5f51ab852da29c8d0a5e75dd9cca94159', '/.git/lost-found/other/7afee14e783f58433d2ed72b25963ebfcb9ebd46', '/.git/lost-found/other/7b00b279b725540bd5e801557be40c425fec033e', '/.git/lost-found/other/7b554508a7883735a7262ffdb1925e70187a153a', '/.git/lost-found/other/7b6cc09cce20fabad0e43645e6521e9c01be4a1e', '/.git/lost-found/other/7b8bcda56aa1fb97e405498e9e342bde05c8863b', '/.git/lost-found/other/7b92ce8b462acb10ee7b3cd6dc02c7d60ed4526f', '/.git/lost-found/other/7bed1a58912ef89bb40536ec81317ad4e857a3af', '/.git/lost-found/other/7c054b66a898848ce6abc261795be460993ac3d5', '/.git/lost-found/other/7c31bb200ac9ee3c8526031f3f462dcfbc0c6dcd', '/.git/lost-found/other/7c5bff6ad3b31492b0ea35a60e3b1d567f5ece3e', '/.git/lost-found/other/7c63e8f7e164de6eac3bf0e4c2c3b86a7006969d', '/.git/lost-found/other/7c6466d64311464b5cc235f012e7eefa7a3f7dec', '/.git/lost-found/other/7c7106db340073127212c46b54764a7d5c52e087', '/.git/lost-found/other/7c7e207d982350b509a2ff479318fe62ed1103fd', '/.git/lost-found/other/7d096caa38d54e011864833826dae24415d66cbe', '/.git/lost-found/other/7d1fa3cfc7a26b23468ef0231a6be425c10c39c0', '/.git/lost-found/other/7d81eca17a7079421b153be35661242578b7fe4b', '/.git/lost-found/other/7d98aa8ec82c154d18bf0e39b24127fd2869c35c', '/.git/lost-found/other/7dff8c856fc62009ba04eab81b3d92ea8b342e7a', '/.git/lost-found/other/7e3e2c020369ec22896955e111fb75738e082b9e', '/.git/lost-found/other/7eaffe3bf399b2a747c76d625eed26950f8832be', '/.git/lost-found/other/7edc089948c55fed4ed96c4947d60561584833d4', '/.git/lost-found/other/7ee4ad885aec0b6786ee1a6ea747a4f012e0478b', '/.git/lost-found/other/7f17877bb03dc7a4b1da8e34bd24c635c8f1fc85', '/.git/lost-found/other/7f1ccef0257eae07e1a9d96c9a419839eb69012b', '/.git/lost-found/other/7fa989db3783a9017443ea55642686cebe2d31bc', '/.git/lost-found/other/7fb7f2e1a4f005e0ed97213f366b2a44d2b5f65a', '/.git/lost-found/other/7fbedd5325332884808b4f13376b20b608ba153d', '/.git/lost-found/other/8039eca3d631d25a1a6d81d08eff05b10453a080', '/.git/lost-found/other/80417b62ee231928cf6e1894ee78ae9d52dced8f', '/.git/lost-found/other/80525b0220584bb2859e90b7b1ecd96124809e0c', '/.git/lost-found/other/805a2540e6e5e0069b0845c8c0d64cc013c0c921', '/.git/lost-found/other/806c3e29a41d7902dc4bfb90b274f7bcdd692396', '/.git/lost-found/other/807fe9f45b577f7b4e832f53598c9132f4634217', '/.git/lost-found/other/80aa6242175a7dfe9cc180151a3c2506287ed78e', '/.git/lost-found/other/80b101102e4af9e39d14d4724273ad6c8673bf8b', '/.git/lost-found/other/80be9d64780cb8215aa9e33cc9f7225d9e763c45', '/.git/lost-found/other/80c7cbf169b9a7de67f1c1d510ead12a86092a6a', '/.git/lost-found/other/80d57ddd52a3d347c46ca1ec7bd6611c3832991f', '/.git/lost-found/other/8135df1518b818e32969ee29a72deecb538a4932', '/.git/lost-found/other/81919ab913ed8acf77c6c0d10a4011b81929dd15', '/.git/lost-found/other/81a82ea2302eda7a5d9cfc93dc15d7aac51acb7b', '/.git/lost-found/other/81b0c9d26060eac103e503fee24c4dc875d73a3d', '/.git/lost-found/other/81b84d2f9246fe95414efaf594ce0d66642af224', '/.git/lost-found/other/81c8e0c1332f8beac34dab5b2d8addd868c78d37', '/.git/lost-found/other/81c929641ff4bb9378d8f539707794ef0bbc35ab', '/.git/lost-found/other/81d135cdcdf753f12ffe7875cd8b84a1aa949a33', '/.git/lost-found/other/81de4211ddd55af9724945af37c733222887a4a9', '/.git/lost-found/other/8208ad133751cbfe78ea16f128cd7bbc1d8c8384', '/.git/lost-found/other/823eb92c648fdf767079c3d6ce64a4e1acfd1d51', '/.git/lost-found/other/824f35363eb09575efb61b59e2a3f4a491629ff3', '/.git/lost-found/other/827a08acc83b7c7a0ccbc1e77bed49435faa6c14', '/.git/lost-found/other/82a5b244d810b0f28e1c0ed826c6b90c3fcdeb69', '/.git/lost-found/other/82a62bb26671ed1e264c244a53da765fdfb6b534', '/.git/lost-found/other/82d66f9855421d3b02581bf6cc776b9401f31a91', '/.git/lost-found/other/82fe660600bda9fb261c64b3d868893a616c6f6b', '/.git/lost-found/other/8326d463947af356e07709d303b413cf1e06dc28', '/.git/lost-found/other/8327ca0d029a9aa0dc380a0ecd1a1ba295fdb6f2', '/.git/lost-found/other/8329fb9ca2717aaf3c0f538bda50030d0f9a88a6', '/.git/lost-found/other/83522d5d571930293dee7c041f9baa0d8c5be22e', '/.git/lost-found/other/83793f9f677aef3ad5f0496d7189d41a71f84c46', '/.git/lost-found/other/838b4934b5ce8b997c97a179ae31efe0df8d69c3', '/.git/lost-found/other/83a1cd018182bd007961c0c1a384f90721538a41', '/.git/lost-found/other/83f433e75ff687ed7ad6e622082b3771f4be902a', '/.git/lost-found/other/83fcd0a4b90b111dd78f24830b0cf0fd6f6662e5', '/.git/lost-found/other/84032ab70aec1220efafe862badb544ab9136474', '/.git/lost-found/other/846fd5afd14b372c7b10c236929e87409bd9ff93', '/.git/lost-found/other/8479528c7d38418a08b92817a5605425c6c65ea9', '/.git/lost-found/other/84a3459111e3b7fc5e8b3db7becf37841bb9af09', '/.git/lost-found/other/84e98f7d23fd1e49868aad7b88e4c25ce27b5f98', '/.git/lost-found/other/8506bc72a2d41cd6d60a4fbb7e3e3e441c831ea6', '/.git/lost-found/other/8507cc0d8827de0caf78209b1bc8b409c30929c3', '/.git/lost-found/other/852f59ef505774d2e1cded9189583af9a7fabfbe', '/.git/lost-found/other/8530702851e912a09461c1b3641ed4447c267bf6', '/.git/lost-found/other/856a9d9a9af9342cb38e84fb97d0ec8be25c4979', '/.git/lost-found/other/856aa17c270d6d6f2b9f0df34ac3aae243b43f0e', '/.git/lost-found/other/8575593501bfc3c1fb9f444dfce8ed8866d583aa', '/.git/lost-found/other/85775c0cf59c7c0a7c8c01be3dc92e2b76038b2b', '/.git/lost-found/other/85888b8c832f86d827cb9fc78205aac1c40bc919', '/.git/lost-found/other/85911b7b0a87b6ef634ba88ee35c9ea798547413', '/.git/lost-found/other/8598ecf10a790316c773068fc621b1ec6a8c7462', '/.git/lost-found/other/85cf7fffe0d71feeb57e13553129f631dd706fe2', '/.git/lost-found/other/85efd595e03f195168517e451a0f6351e2f9e69f', '/.git/lost-found/other/85f0a8f1420aabbd7a4472ee3ed2f9d968be657c', '/.git/lost-found/other/8636b42068ee84f766948b4f22e52bc3280e9eb7', '/.git/lost-found/other/868d17c19fc94e4da1a657e07258f027e37a183f', '/.git/lost-found/other/877dbd89e8209c09b4e6117d45aa1ffa5c29123a', '/.git/lost-found/other/878572383d5cca030620695db137e5d8befb60e2', '/.git/lost-found/other/878ec5f103298fd245bffbc77e9b4122705d6caf', '/.git/lost-found/other/87a3f4559d75c1fce1baae89b3777b9bef57f4c6', '/.git/lost-found/other/87b4d789046bbf43385acd61e5c3e70a1bec50eb', '/.git/lost-found/other/87bdeed1fa7053bf3f3ee36c8996eb1a85ca4581', '/.git/lost-found/other/87c156c8531b9854f8913b8ca70249dacd305771', '/.git/lost-found/other/87f508dde1d80fd527a62801ed475fdcfa1199d0', '/.git/lost-found/other/884ad461f9de46bba7b5fb8b37d1f4fb913b128f', '/.git/lost-found/other/8862c16224430bf0aa6f410ce9df8777453427c3', '/.git/lost-found/other/888114b868b7b1a10c7b8aedadfab6a0b198d938', '/.git/lost-found/other/88a12ae4891c84ce446aaf38698e7f684d05465d', '/.git/lost-found/other/88a57a29b1fe7fc24955b3c475d2587cfc2b2168', '/.git/lost-found/other/88c4d478b40dec9953b90c124136cb8ca6aabac6', '/.git/lost-found/other/88de5d8898855804a10e46a2b8ed2efdded56c2d', '/.git/lost-found/other/88ee53c9ece8ef43612f9db4cc25aa5614aa26ad', '/.git/lost-found/other/8969067bcbecde61a44d7cf0f5d364fe265ac08a', '/.git/lost-found/other/896dd57e7a94ddfe4430921fddcf78e252b7053e', '/.git/lost-found/other/8972d0e0bf6c14c869c716e06845e43ee7d373ed', '/.git/lost-found/other/899125167a136688cdca3cfc2a02bd8767aae87b', '/.git/lost-found/other/89a8667eaaa858b441ca2b4cf8f783a98017c631', '/.git/lost-found/other/89c09fa5bbb4ec88f5f5586334bbc9b5ee4def63', '/.git/lost-found/other/89ee971a3b572fa574374f7d8789267118bfdc5d', '/.git/lost-found/other/89ff128aa63e61990193840dfa90762d4f8f3652', '/.git/lost-found/other/8a1b068cf37d71278de5478ecea3b17e478bc53a', '/.git/lost-found/other/8a2e1744f8d60b47acee31323eb9be5252f3bb71', '/.git/lost-found/other/8a5e5ad2e568b464c38258b18b07105fa93c8eeb', '/.git/lost-found/other/8ad6631101557add7e9f03d4438ee6d4bd81fcd1', '/.git/lost-found/other/8b0fe43b479ecc9b599ccb21386dcf6243fab6ef', '/.git/lost-found/other/8b166483db6ab554b4ed7cfa227dcec5c0b5c4d1', '/.git/lost-found/other/8b474e9468a368ca615b1d5b7e8ae43995e7ed6b', '/.git/lost-found/other/8badb259266160ed2ae90c6d544e84c1f16bdfa2', '/.git/lost-found/other/8bc007bd8099a368761f7a85d69e8c62e91751d7', '/.git/lost-found/other/8bd53ac2f88091ca967b218668ddeb2b8b901b3b', '/.git/lost-found/other/8bf56f827628f29cc78ef7e19693f5b957efcb55', '/.git/lost-found/other/8c032fd3bc85f561863400e177168dcf3ace645e', '/.git/lost-found/other/8c193116cbb53901051d2a1d16301a18a0dcefcb', '/.git/lost-found/other/8c32101bf52c685290b17f8f9152446952caaef4', '/.git/lost-found/other/8c532b7669a3fd0dc35dabdd43d2b34db2726089', '/.git/lost-found/other/8c768de675b19dbd6d0328fda1e54fd350b3621b', '/.git/lost-found/other/8c7f0d1ecd32895777182562810997d842a1cc5a', '/.git/lost-found/other/8ca05df80017a216b6e9c040a13de4ef1c762f3e', '/.git/lost-found/other/8cdaba2214ca080e13141a212a14fa3492dee9a6', '/.git/lost-found/other/8cea1e553faca94727050f1666f760a5b579a34d', '/.git/lost-found/other/8cef1dc2bb0c10cac3165c3672402be4fe31054c', '/.git/lost-found/other/8d39cd48167f79c08783e996e5054ba4430f3918', '/.git/lost-found/other/8d87692ec4508add82fc7bcfb11627594c76759f', '/.git/lost-found/other/8db2dc5e2da502d8be60f83c29b6bd8cdece283d', '/.git/lost-found/other/8dcf63db4819ce835831f19b7f843f66cf331057', '/.git/lost-found/other/8de773e9097a8f0dcbed369e6c3e3f3dd481cb8d', '/.git/lost-found/other/8dfb262567a945bd38c2f444dd5a91c0c674ded1', '/.git/lost-found/other/8e147d7dafa9de53bdfdf1afdd2288c7015dab9b', '/.git/lost-found/other/8e1df140ffb6a1a2e0e1dbc48231a1341416d5ef', '/.git/lost-found/other/8e30c681e95c989c9194668613784ec1fb70c362', '/.git/lost-found/other/8e508aca87513c614f529e35534a6f510f5fecc4', '/.git/lost-found/other/8e624b995ed2e8b2f8a1fde05616b92165f1b612', '/.git/lost-found/other/8e6e6dca3e2142e6450e31de9dcc15e1315d11d1', '/.git/lost-found/other/8e886852a0b8f8effe43f3249827b417df2987c2', '/.git/lost-found/other/8e8cc43769b3e51927bb486257e5d2389bdfe3e7', '/.git/lost-found/other/8ed2f0dd8617bf639e3528efcc136bd64ff48295', '/.git/lost-found/other/8ed475a3ae2bbea45fbe48ab50f5ea73d830fd2f', '/.git/lost-found/other/8efb95334e4dfd7238406b637b87d38bc7df7971', '/.git/lost-found/other/8f29fcc619ffc635697fc2d2d468888819a7c05d', '/.git/lost-found/other/8f5819fda3698f87172becd15cd54ad20cdbc350', '/.git/lost-found/other/8f872767673fc75e5c1421d89521e998af4f8d39', '/.git/lost-found/other/8f8836cd2c592cc7a626577ab0c78aa97314cb80', '/.git/lost-found/other/8f8a2153b54a03fb30f2d21c11b2fc65b5071796', '/.git/lost-found/other/8fe85b124c02b0a063a255461fdcf4462b871849', '/.git/lost-found/other/9025e7e99615220286bf75c93d3246d302f1375a', '/.git/lost-found/other/903e19a32e203d03671b31f6e27ebaa907166d90', '/.git/lost-found/other/9040ad1040d2f81d6eba6d481dc29f2a5f5b2f73', '/.git/lost-found/other/9052c9897d84020cc14786b82536af8a94cad0e3', '/.git/lost-found/other/910bcc380d91aea78d4bab200472aee82a8e9f96', '/.git/lost-found/other/91129c883e5f0e47819acbc2aad8d6314c0310a4', '/.git/lost-found/other/9117e524aeb011990bc54777f70d56955ef716a3', '/.git/lost-found/other/9124c4e8d7b6925e2de9f96ba7ee66e9cfbd5b4f', '/.git/lost-found/other/91364a90eb688a950083474549ee42e8e0eaf78f', '/.git/lost-found/other/91501834e260e8d218dadf002c167daf1d7a99e4', '/.git/lost-found/other/915fd7b0567afe8725f78a286a8d8155d5b1a361', '/.git/lost-found/other/91897ad77d725aab215d18fc41d34a68ad6b142b', '/.git/lost-found/other/91a71c4d7e7cc2cc27852d2b1a6c5a1931fa1f11', '/.git/lost-found/other/91d3aafcff2a3ea74c1cfa946fa955c62abd89c2', '/.git/lost-found/other/91e214a28a493c3c2e35325fb7245d6983ea71ca', '/.git/lost-found/other/921a6caed41c95b6bba1e56724fe34b038245416', '/.git/lost-found/other/92301588927b94a7a8d688c5220721145e377e38', '/.git/lost-found/other/923210f734a2e995f200388e83d5fed3cf26053f', '/.git/lost-found/other/924d93052389d0b9434705bfe32ef317528044d9', '/.git/lost-found/other/92612a56a21f153339abb5c4efb074765d36aceb', '/.git/lost-found/other/926e20ae59a15432cc966c029407288466bdcddb', '/.git/lost-found/other/92dc8ccd7943e2b3163be459d4fb36f013ffff6d', '/.git/lost-found/other/92f0a102283a69d06abb892c5d78980a6a4d2652', '/.git/lost-found/other/932ab411aba0a979eb6a54f3c43832011843338f', '/.git/lost-found/other/93424d534c936bf6e468285533db39e19a47cc4e', '/.git/lost-found/other/93767a88113b92a54fdb35d82ba698c50f0af898', '/.git/lost-found/other/9387b3fd7de48b7e14efafef2ed67c4eb5015716', '/.git/lost-found/other/939be16e271fbe69d578fdb0ef909996a506933e', '/.git/lost-found/other/93c6ae943c48d1c8fe60cf11e869de7401a70e9d', '/.git/lost-found/other/9437d9d6ad6a559a5d535231870cc81d2e5f61e2', '/.git/lost-found/other/9441b1dcc2d951a7881cdde15f1bb4aa78e01801', '/.git/lost-found/other/944e4ac44eaf17d1c2a0a2149c670b79db3b81bc', '/.git/lost-found/other/948a2574e766a7def043341e9d592244e5f656cd', '/.git/lost-found/other/9494d7d02c4efa7814192147f9cd95198b968706', '/.git/lost-found/other/94bf9b9cb3ad20e5e40e68b19d2d967351fd7043', '/.git/lost-found/other/94ddb92592b2844dab2a6dbf6b54c3ec65c53adc', '/.git/lost-found/other/94f86597692644521fcb91b65ebfa1d6698b721e', '/.git/lost-found/other/9523046c930fc423ff2f2d964b0ad1f0f8dcc561', '/.git/lost-found/other/952dad6cd5e0a77bbc998b01cf76b786dcf86bd2', '/.git/lost-found/other/953728dff60b9ee56f8f94c427b6512b881a532f', '/.git/lost-found/other/9596ea8c380e21e2936eebc4d43cc3da5c3945dc', '/.git/lost-found/other/95b3c141d6f33fa02247dc87531e793b05061531', '/.git/lost-found/other/960849ac9a576a80ffaaf0a558644a959e85d725', '/.git/lost-found/other/962e546dcc1ccf96804fc035e0c053e640867b9e', '/.git/lost-found/other/9683a32d2a5b6572a83f7b012fa1bf38660ae712', '/.git/lost-found/other/96947147a4afca1db6085e927b1a9a03d61ffd73', '/.git/lost-found/other/96b583ead2754801cabadeaa6310962d9484b35c', '/.git/lost-found/other/96c55467020eb5967190ef67ea5af73bd8557293', '/.git/lost-found/other/96f0c3a29711baf739f8d206549147833769309f', '/.git/lost-found/other/96fd88067893385c0765030c47af266de862e670', '/.git/lost-found/other/970b3536b39e69354428d28cb4461dc2b51077a4', '/.git/lost-found/other/979c845eeee9c7ea69e9be82ea0152129d99ab94', '/.git/lost-found/other/97ade8382b5461f3e7dba16ee4cb7b21e3428693', '/.git/lost-found/other/97b5c66faefdec6e1e3f9511ffa5352ba6aed231', '/.git/lost-found/other/97d1c714bdd88d2c18292f04270b1d088b7ab423', '/.git/lost-found/other/98330f2a74870e2eacf010a3dc6ebf02ba786210', '/.git/lost-found/other/984da4d425592c6728086f770d46015c2774fb7f', '/.git/lost-found/other/98570cf2f3892aeb6a60317d3c5f2395551fa126', '/.git/lost-found/other/98634d3201e655b428c3720dfc45a1deaf0fd370', '/.git/lost-found/other/98a5ec496c33e52dbeece3cd0ce79df9d837d56b', '/.git/lost-found/other/98b214d389c3b000b67c73ef23a93e020caa45ce', '/.git/lost-found/other/98d9cd7743f231620723d495810cd1f76180c10e', '/.git/lost-found/other/98ddac6847239f0b68e04184b7c57cbffa12398f', '/.git/lost-found/other/98e1a00c29c13261193d33d35e8b870695aabfbc', '/.git/lost-found/other/9900a37055c69f4e8b8b84d6c679c7340cf21a2a', '/.git/lost-found/other/990b82d5c7737e7d79db4d7ee986945bee8c8b04', '/.git/lost-found/other/9964532f1952d9499823130c76cd62602dea68b4', '/.git/lost-found/other/996acb6402c94e8606049daf81862a1b810911df', '/.git/lost-found/other/996fca5689f017cbec23de29b1c8f9dc02a3b8e2', '/.git/lost-found/other/998187ffe021319b3cd3f43f9d7f7abe4aba6b90', '/.git/lost-found/other/99c369006665885b83433b1cada3e5998e5155b2', '/.git/lost-found/other/99d222d5d2d4742cfd70b247b8bceadd95fc4706', '/.git/lost-found/other/99e9be780090b056920e343370328c22ba0ecc8b', '... [results truncated, try being more specific with your parameters]']
AI: Let me find the actual working files and inputs more specifically.[{'name': 'glob', 'args': {'pattern': 'inputs/**/*', 'path': '/'}, 'id': 'call_00_MSO2hPypukWXqmRaqWgZ4354', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'outputs/**/*', 'path': '/'}, 'id': 'call_01_ipUSQxxtY3UEzeihEnKv8194', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'skills/acquiring-discrepancy-analysis/**/*', 'path': '/'}, 'id': 'call_02_NikmBo7VZsXNhvSTi44n5533', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/.venv/Lib/site-packages/langchain_core/outputs/__init__.py', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/llm_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/run_info.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/chat_generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/chat_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/llm_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/run_info.py', '/outputs/working/applicability_filter.json', '/outputs/working/batch_1_results.json', '/outputs/working/batch_2_results.json', '/outputs/working/check_enrichment.py', '/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/enrich_ledger.py', '/outputs/working/filter_matrix.py', '/outputs/working/fix_batch1.py', '/outputs/working/fix_batch2.py', '/outputs/working/legal_propositions.json', '/outputs/working/list_matrix.py', '/outputs/working/validate_batch2.py', '/outputs/working/verify_batch1.py', '/outputs/working/verify_batch2.py']
Tool: ['/skills/acquiring-discrepancy-analysis/SKILL.md', '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/bootstrap_source_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/export_review_xlsx.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/finalize_discrepancy_json.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_coverage_ledger.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_source_numbering.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_working_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/bootstrap_source_artifacts.py', '/skills/acquiring-discrepancy-analysis/scripts/export_review_xlsx.py', '/skills/acquiring-discrepancy-analysis/scripts/extract_docx_numbered.py', '/skills/acquiring-discrepancy-analysis/scripts/finalize_discrepancy_json.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_coverage_ledger.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py']
AI: Good. Now let me read the reference documents, the existing working artifacts, and the source inputs. Let me start with the references and the matrix/contract inputs.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_00_UKPY3FaxKKMv9bakm9Mf1375', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_01_EVAe0p84872T8aWTs5sy4617', 'type': 'tool_call'}]
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
   102	      "covered_elements": ["<matrix provisions covered by contract candidates>"],
   103	      "uncovered_elements": ["<matrix provisions still missing/changed/weak>"],
   104	      "candidate_contract_ids": ["<accepted candidate contract locator>"],
   105	      "rejected_contract_ids": [
   106	        {
   107	          "contract_id": "<reviewed non-candidate locator>",
   108	          "reason": "<why it is not a true analogue or cannot cure the gap>"
   109	        }
   110	      ],
   111	      "candidate_search_exhausted": true,
   112	      "search_scope": "full_contract|targeted_domain",
   113	      "discrepancies": [
   114	        {
   115	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   116	          "description": "<material difference>",
   117	          "risk": "<why this matters for the Bank>"
   118	        }
   119	      ]
   120	    }
   121	  ],
   122	  "atomic_links": [
   123	    {
   124	      "matrix_id": "<one matrix id>",
   125	      "contract_id": "<one contract locator>",
   126	      "relationship": "aligned|deviation",
   127	      "link_index": 0,
   128	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   129	      "coverage": "<what this contract locator contributes to the group>"
   130	    }
   131	  ],
   132	  "unmatched_matrix": [
   133	    {
   134	      "matrix_id": "<matrix id>",
   135	      "requirement": "<missing bank standard requirement>",
   136	      "source_evidence": "<short matrix quote>",
   137	      "status": "missing_in_contract",
   138	      "required_type": "mandatory|optional|unknown",
   139	      "applicability": "applicable|conditional|unknown",
   140	      "risk_level": "low|medium|high",
   141	      "risk": "<risk of omission>",
   142	      "covered_elements": ["<matrix provisions covered by weak/partial context, if any>"],
   143	      "uncovered_elements": ["<matrix provisions not covered by any true analogue>"],
   144	      "candidate_contract_ids": [],
   145	      "candidate_search_exhausted": true,
   146	      "search_scope": "full_contract",
   147	      "rejected_candidates": [
   148	        {
   149	          "contract_id": "<weak candidate considered>",
   150	          "reason": "<why it is not a true analogue>"
   151	        }
   152	      ]
   153	    }
   154	  ],
   155	  "unmatched_contract": [
   156	    {
   157	      "contract_id": "<contract locator>",
   158	      "contract_position": "<extra legally significant contract term>",
   159	      "source_evidence": "<short contract quote>",
   160	      "status": "extra_in_contract",
   161	      "risk_level": "low|medium|high",
   162	      "risk": "<risk or impact for the Bank>",
   163	      "materiality_reason": "<why this has independent legal effect>"
   164	    }
   165	  ],
   166	  "coverage_ledger": {
   167	    "matrix": [
   168	      {
   169	        "matrix_id": "<matrix id>",
   170	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
   171	        "link_indices": [0],
   172	        "reason": "<short closure reason>"
   173	      }
   174	    ],
   175	    "contract": [
   176	      {
   177	        "contract_id": "<contract locator>",
   178	        "closure": "linked|extra_in_contract|not_material",
   179	        "link_indices": [0],
   180	        "reason": "<short closure reason>"
   181	      }
   182	    ]
   183	  },
   184	  "summary": {
   185	    "aligned_count": 0,
   186	    "deviation_count": 0,
   187	    "missing_in_contract_count": 0,
   188	    "extra_in_contract_count": 0
   189	  }
   190	}
   191	```
   192	
   193	## JSON Rules
   194	
   195	- `links` are group-level legal findings. One status applies to the whole
   196	  many-to-many group.
   197	- `atomic_links` are traceability rows only. They inherit the group
   198	  `relationship`; do not invent pair-level final statuses.
   199	- `contract_ids` contain clauses that provide material coverage for the group.
   200	  Background clauses can be cited in reasoning, but should not become final
   201	  candidates unless they affect coverage or status.
   202	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   203	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   204	  matrix closures. Do not use it to invent final conclusions.
   205	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   206	  not a risk for the current product, lot, terminal, payment method, or legal
   207	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   208	  final `unmatched_matrix`.
   209	- `unmatched_contract` contains only legally significant `extra_in_contract`
   210	  rows. Non-material rows stay in `coverage_ledger.contract`.
   211	- `relationship = aligned` requires empty `discrepancies`, empty
   212	  `uncovered_elements`, `risk_level = none`, and text-grounded confirmation
   213	  that the contract package preserves the matrix legal result.
   214	- `relationship = deviation` requires at least one discrepancy with `type`,
   215	  `description`, and `risk`; `candidate_search_exhausted = true`; and
   216	  `search_scope = full_contract`.
   217	- Missing mandatory applicable requirements should normally be `high` risk.
   218	  Missing optional applicable requirements should normally be `low` or
   219	  conditional risk.
   220	- `unmatched_matrix` requires `candidate_search_exhausted = true` and
   221	  `search_scope = full_contract`; it is invalid to mark an applicable matrix
   222	  item missing before checking all contract clauses through the source index.
   223	- All final ids must be visible in source files. Do not use corrected,
   224	  inferred, translated, parenthetical, or internal ids.
   225	- Weak candidates do not appear in final `links`; use
   226	  `unmatched_matrix[].rejected_candidates`.
   227	
   228	## Excel Output
   229	
   230	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   231	
   232	Sheet 1: `Contract-Matrix`
   233	
   234	Columns:
   235	
   236	1. `contract_id`
   237	2. `contract_summary`
   238	3. `matrix_ids`
   239	4. `status`
   240	5. `risk_level`
   241	6. `comment`
   242	
   243	Rules:
   244	
   245	- one row per group-level contract-to-matrix finding;
   246	- `matrix_ids` contains the full matrix id set for the group;
   247	- status is `aligned`, `deviation`, or `extra_in_contract`;
   248	- contract-only extras have blank `matrix_ids`.
   249	
   250	Sheet 2: `Only in Matrix`
   251	
   252	Columns:
   253	
   254	1. `matrix_id`
   255	2. `requirement`
   256	3. `required_type`
   257	4. `risk_level`
   258	5. `comment`
   259	
   260	Rules:
   261	
   262	- one row per final `unmatched_matrix` item;
   263	- include optional applicable missing as low/conditional risk;
   264	- do not include out-of-scope / not-applicable requirements;
   265	- do not include non-evaluable headings or purely technical rows.
   266	
   267	## Bad Output Patterns
   268	
   269	Do not output:
   270	
   271	- multiple competing final JSON files;
   272	- pair-level final statuses as the primary answer;
   273	- `deviation` for unselected slash alternatives;
   274	- `deviation` for heading/title/label changes alone;
   275	- final `unmatched_contract` rows for definitions without legal effect;
   276	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   277	  requirements;
   278	- final ids that exist only in helper scripts or working ledgers;
   279	- `extra_in_contract` with empty risk;
   280	- `aligned` with non-empty discrepancies;
   281	- `aligned` with non-empty `uncovered_elements`;
   282	- `deviation` or `missing_in_contract` with `candidate_search_exhausted = false`;
   283	- `deviation` or `missing_in_contract` with `search_scope = targeted_domain`
   284	  or `not_completed`;
   285	- `missing_in_contract` where a weak candidate is silently treated as a link;
   286	- final conclusions based only on extracted fields without source-text evidence.
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
   274	## 33. Uncovered Deadline Requires Continued Search
   275	
   276	Matrix requires a duty plus a 3-business-day deadline. The first contract
   277	candidate covers the duty but is silent on timing.
   278	
   279	Result: do not finalize `deviation` yet. Continue a full-contract sweep for
   280	another clause, appendix, or incorporated procedure that supplies the deadline.
   281	If none exists, mark `deviation` with the deadline gap and
   282	`candidate_search_exhausted = true`.
   283	
   284	## 34. Missing Only After Full Sweep
   285	
   286	Matrix requires a specific Bank right. Contract clauses mention the same broad
   287	topic, but each governs another party, object, trigger, or consequence.
   288	
   289	Result: only after all contract clauses are checked and rejected can the matrix
   290	item become `missing_in_contract`. List reviewed close candidates in
   291	`rejected_candidates`.
   292	
   293	## 35. Similar Hard Term Cannot Cure Different Object
   294	
   295	Matrix requires a 3-day response to a fraud-monitoring request. Contract has a
   296	3-day deadline for signing an act, but it is not incorporated into the fraud
   297	request procedure.
   298	
   299	Result: reject the act clause for this matrix item. A matching number of days
   300	does not cure an uncovered element when the legal object differs.
   301	
   302	## 36. Collective Coverage Becomes Aligned
   303	
   304	Matrix requires duty, evidence channel, deadline, and consequence. Contract
   305	splits them across operative clause, document-exchange clause, appendix, and
   306	liability clause, all governing the same obligation.
   307	
   308	Result: include the whole package in one link. If no material provision remains
   309	uncovered, status is `aligned`.
   310	
   311	## 37. True Analogue But Remaining Changed Term
   312	
   313	Matrix and contract regulate the same payment obligation. Contract candidate
   314	exists, but after full-contract sweep the payment deadline remains longer than
   315	the Bank standard.
   316	
   317	Result: keep the true analogue link and mark `deviation`; do not downgrade to
   318	`missing_in_contract`, and do not upgrade to `aligned`.
AI: Now let me read the existing working artifacts and the source inputs. Let me start with the matrix (items 97-144) and the contract, plus the existing working files.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 100}, 'id': 'call_00_y0XnoqVHbfSAsOcfjQFX4407', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_01_R8I1OWrG19oxqADUqzAE6010', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/applicability_filter.json'}, 'id': 'call_02_jbC7ctNLIGiOAoimR6Vs7274', 'type': 'tool_call'}]
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
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos", "smart"],
     5	  "payment_method": ["cards", "qr", "nfc"],
     6	  "legal_regime": "44_fz",
     7	  "notes": {
     8	    "contract_type": "44-FZ government contract for acquiring services",
     9	    "customer": "FGBU Kavkazsky State Nature Biosphere Reserve",
    10	    "terminals_provided_by": "Bank (Executor)",
    11	    "smart_terminal_type": "Evotor+",
    12	    "card_systems": ["MIR", "VISA", "MasterCard"],
    13	    "qr_on_terminal_display": true,
    14	    "contactless_nfc": true,
    15	    "max_contract_price": "1,900,000 RUB",
    16	    "contract_period": "01.03.2025 - 30.11.2025 or until price exhaustion",
    17	    "no_internet_acquiring": true,
    18	    "no_sberpay_face_scan": true,
    19	    "no_recurring_payments": true
    20	  }
    21	}
Tool:      1	{
     2	  "profile": {
     3	    "product": "trade_acquiring",
     4	    "lot": "fz_44",
     5	    "terminal": [
     6	      "pos",
     7	      "smart"
     8	    ],
     9	    "payment_method": [
    10	      "cards",
    11	      "nfc",
    12	      "qr"
    13	    ]
    14	  },
    15	  "applicable_count": 144,
    16	  "not_applicable_count": 25,
    17	  "applicable_numbers": [
    18	    "2.1",
    19	    "2.2",
    20	    "2.3.1",
    21	    "2.3.2",
    22	    "2.3.3",
    23	    "2.3.4",
    24	    "2.3.5",
    25	    "2.3.6",
    26	    "2.3.7",
    27	    "2.4",
    28	    "2.6.1.1",
    29	    "2.6.2.1",
    30	    "2.6.2.2",
    31	    "2.6.3.1",
    32	    "2.6.3.2",
    33	    "2.7",
    34	    "3.1",
    35	    "3.2",
    36	    "3.3",
    37	    "4.1.1",
    38	    "4.1.2",
    39	    "4.1.3",
    40	    "4.2.1",
    41	    "4.2.2",
    42	    "4.2.4",
    43	    "4.2.5",
    44	    "4.2.6",
    45	    "4.2.7",
    46	    "4.2.8",
    47	    "4.2.9",
    48	    "4.2.10",
    49	    "4.2.11",
    50	    "4.2.12",
    51	    "4.2.13",
    52	    "4.2.14",
    53	    "4.2.15",
    54	    "4.2.16.1",
    55	    "4.2.16.2",
    56	    "4.2.16.3",
    57	    "4.2.18",
    58	    "4.2.19",
    59	    "4.2.20.1",
    60	    "4.2.20.2",
    61	    "4.2.20.3",
    62	    "4.2.20.4",
    63	    "4.2.20.5",
    64	    "4.2.20.6",
    65	    "4.2.20.7",
    66	    "4.2.22",
    67	    "4.2.23",
    68	    "4.2.24",
    69	    "4.2.25",
    70	    "5.1.1.1",
    71	    "5.1.1.2",
    72	    "5.1.1.3",
    73	    "5.1.1.4",
    74	    "5.1.1.5",
    75	    "5.1.1.6",
    76	    "5.1.2",
    77	    "5.1.3",
    78	    "5.1.4",
    79	    "5.1.5",
    80	    "5.1.6",
    81	    "5.1.7",
    82	    "5.1.8.1",
    83	    "5.1.8.2",
    84	    "5.1.8.3",
    85	    "5.1.8.6",
    86	    "5.1.8.7",
    87	    "5.1.8.8",
    88	    "5.1.8.9",
    89	    "5.1.8.10",
    90	    "5.1.8.11",
    91	    "5.1.8.12",
    92	    "5.1.8.13",
    93	    "5.1.9",
    94	    "5.1.10",
    95	    "5.1.11",
    96	    "5.1.12",
    97	    "5.1.13",
    98	    "5.1.14",
    99	    "5.1.15",
   100	    "5.1.16",
AI: Let me continue reading the applicability filter and also get the matrix items 97-144. Let me also read the existing batch results and the legal propositions.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/applicability_filter.json', 'offset': 100, 'limit': 100}, 'id': 'call_00_BA4t9w9wWPYYsj8TgGfz8981', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_1_results.json', 'limit': 50}, 'id': 'call_01_NINQMHDnzOKt5kDhVBZy8782', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_2_results.json', 'limit': 50}, 'id': 'call_02_a9IbiD2y2T6zkr3fb7bL4951', 'type': 'tool_call'}]
Tool:    101	    "5.1.17.1",
   102	    "5.1.17.2",
   103	    "5.2.3",
   104	    "5.2.4",
   105	    "5.2.5",
   106	    "5.2.6",
   107	    "5.2.7",
   108	    "5.2.8",
   109	    "5.2.9",
   110	    "5.2.10",
   111	    "6.1",
   112	    "6.2",
   113	    "6.4",
   114	    "6.5",
   115	    "6.7",
   116	    "6.8",
   117	    "6.10",
   118	    "6.11",
   119	    "6.13",
   120	    "6.14",
   121	    "6.16",
   122	    "6.17",
   123	    "6.20",
   124	    "6.21",
   125	    "7.1",
   126	    "7.2",
   127	    "7.3",
   128	    "7.4",
   129	    "7.5",
   130	    "7.6",
   131	    "7.7",
   132	    "7.8",
   133	    "7.9",
   134	    "7.10",
   135	    "7.11",
   136	    "7.12",
   137	    "7.14",
   138	    "7.15",
   139	    "7.16",
   140	    "7.17",
   141	    "8.1",
   142	    "8.2",
   143	    "9.1",
   144	    "9.2",
   145	    "9.3",
   146	    "10.1",
   147	    "10.2",
   148	    "10.3",
   149	    "11.1",
   150	    "11.2",
   151	    "11.3",
   152	    "11.4",
   153	    "11.5",
   154	    "11.6",
   155	    "11.7",
   156	    "11.8",
   157	    "11.9",
   158	    "11.10",
   159	    "11.11",
   160	    "11.12",
   161	    "11.13"
   162	  ],
   163	  "not_applicable": [
   164	    {
   165	      "number": "2.5.1.1",
   166	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   167	    },
   168	    {
   169	      "number": "2.5.2.1",
   170	      "reason": "out_of_scope: payment_method=sber_pay_face_scan, contract payment_methods=['cards', 'nfc', 'qr']"
   171	    },
   172	    {
   173	      "number": "4.2.3",
   174	      "reason": "out_of_scope: lot=fz_223, contract lot=fz_44"
   175	    },
   176	    {
   177	      "number": "4.2.17",
   178	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   179	    },
   180	    {
   181	      "number": "4.2.21.1",
   182	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   183	    },
   184	    {
   185	      "number": "4.2.21.2",
   186	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   187	    },
   188	    {
   189	      "number": "4.2.21.3",
   190	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   191	    },
   192	    {
   193	      "number": "4.2.21.4",
   194	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   195	    },
   196	    {
   197	      "number": "4.2.21.5",
   198	      "reason": "out_of_scope: product=internet_acquiring, contract product=trade_acquiring"
   199	    },
   200	    {
Tool:      1	{
     2	  "batch": "1",
     3	  "matrix_range": "1-48",
     4	  "analysis_profile": {
     5	    "contract_product_profile": {
     6	      "product": [
     7	        "trade_acquiring"
     8	      ],
     9	      "lot": "44_fz",
    10	      "terminal": [
    11	        "pos",
    12	        "smart"
    13	      ],
    14	      "payment_method": [
    15	        "cards",
    16	        "qr",
    17	        "nfc"
    18	      ],
    19	      "legal_regime": "44_fz"
    20	    }
    21	  },
    22	  "out_of_scope_matrix": [
    23	    {
    24	      "matrix_id": "2.5.1.1",
    25	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    26	      "closure": "out_of_scope"
    27	    },
    28	    {
    29	      "matrix_id": "2.5.2.1",
    30	      "reason": "payment_method=sber_pay_face_scan; contract has no sber_pay_face_scan",
    31	      "closure": "out_of_scope"
    32	    },
    33	    {
    34	      "matrix_id": "4.1.3",
    35	      "reason": "payment_method=qr_sber_pay; contract has no qr_sber_pay (only qr)",
    36	      "closure": "out_of_scope"
    37	    },
    38	    {
    39	      "matrix_id": "4.2.3",
    40	      "reason": "only_for_lot=fz_223; contract is 44_fz",
    41	      "closure": "out_of_scope"
    42	    },
    43	    {
    44	      "matrix_id": "4.2.17",
    45	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    46	      "closure": "out_of_scope"
    47	    }
    48	  ],
    49	  "links": [
    50	    {
Tool:      1	{
     2	  "batch": "2",
     3	  "matrix_range": "49-96",
     4	  "analysis_profile": {
     5	    "contract_product_profile": {
     6	      "product": [
     7	        "trade_acquiring"
     8	      ],
     9	      "lot": "44_fz",
    10	      "terminal": [
    11	        "pos",
    12	        "smart"
    13	      ],
    14	      "payment_method": [
    15	        "cards",
    16	        "qr",
    17	        "nfc"
    18	      ],
    19	      "legal_regime": "44_fz"
    20	    }
    21	  },
    22	  "out_of_scope_matrix": [
    23	    {
    24	      "matrix_id": "4.2.21.1",
    25	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    26	      "closure": "out_of_scope"
    27	    },
    28	    {
    29	      "matrix_id": "4.2.21.2",
    30	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    31	      "closure": "out_of_scope"
    32	    },
    33	    {
    34	      "matrix_id": "4.2.21.3",
    35	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    36	      "closure": "out_of_scope"
    37	    },
    38	    {
    39	      "matrix_id": "4.2.21.4",
    40	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    41	      "closure": "out_of_scope"
    42	    },
    43	    {
    44	      "matrix_id": "4.2.21.5",
    45	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
    46	      "closure": "out_of_scope"
    47	    },
    48	    {
    49	      "matrix_id": "4.2.21.6",
    50	      "reason": "only_for_product=internet_acquiring; contract has no internet_acquiring",
AI: Now I need to understand the batch structure. Let me check what matrix items 97-144 are. Let me first get the full matrix to identify these items, and also read the contract text.[{'name': 'execute', 'args': {'command': 'python /outputs/working/list_matrix.py 2>/dev/null | head -200'}, 'id': 'call_00_iXztRaPCGij1Z9OugjPu7917', 'type': 'tool_call'}]
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
[stderr] python outputs/working/list_matrix.py 2>$null | head -200
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : The term 'head' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
[stderr] lling of the name, or if a path was included, verify that the path is correct and try again.
[stderr] At line:36 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/list_matrix.py'}, 'id': 'call_00_tsosrIzQHUJF57ucaX0Q8960', 'type': 'tool_call'}]
Tool:      1	import json, os
     2	print(os.getcwd())
     3	with open('inputs/matrix.json') as f:
     4	    m = json.load(f)
     5	print(f'Total: {len(m)}')
     6	for i, it in enumerate(m):
     7	    print(f"Idx {i}: {it['number']} | req={it['required_type']} | prod={it['only_for_product']} | lot={it['only_for_lot']} | term={it['only_for_terminal']} | pm={it['payment_method']}")
AI: [{'name': 'execute', 'args': {'command': 'cd / && python outputs/working/list_matrix.py 2>&1 | Select-Object -First 200'}, 'id': 'call_00_iEqVX0BoosANSfdnVhal7169', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:6
[stderr] + cd / && python outputs/working/list_matrix.py 2>&1 | Select-Object -F ...
[stderr] +      ~~
[stderr] The token '&&' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/list_matrix.py'}, 'id': 'call_00_8d57GiK7rwAOAOhCG0Da3728', 'type': 'tool_call'}]
Tool: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2
Total: 169
Idx 0: 2.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 1: 2.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 2: 2.3.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 3: 2.3.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 4: 2.3.3 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 5: 2.3.4 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 6: 2.3.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 7: 2.3.6 | req=mandatory | prod=common | lot=fz_44 | term=common | pm=common
Idx 8: 2.3.7 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 9: 2.4 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 10: 2.5.1.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 11: 2.5.2.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=sber_pay_face_scan
Idx 12: 2.6.1.1 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=qr
Idx 13: 2.6.2.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 14: 2.6.2.2 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 15: 2.6.3.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 16: 2.6.3.2 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 17: 2.7 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 18: 3.1 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 19: 3.2 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 20: 3.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 21: 4.1.1 | req=optional | prod=common | lot=common | term=common | pm=qr
Idx 22: 4.1.2 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 23: 4.1.3 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr_sber_pay
Idx 24: 4.2.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 25: 4.2.2 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 26: 4.2.3 | req=optional | prod=common | lot=fz_223 | term=common | pm=common
Idx 27: 4.2.4 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 28: 4.2.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 29: 4.2.6 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 30: 4.2.7 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 31: 4.2.8 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 32: 4.2.9 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 33: 4.2.10 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 34: 4.2.11 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 35: 4.2.12 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 36: 4.2.13 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 37: 4.2.14 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 38: 4.2.15 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 39: 4.2.16.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 40: 4.2.16.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 41: 4.2.16.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 42: 4.2.17 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 43: 4.2.18 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 44: 4.2.19 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 45: 4.2.20.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 46: 4.2.20.2 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 47: 4.2.20.3 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 48: 4.2.20.4 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 49: 4.2.20.5 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 50: 4.2.20.6 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 51: 4.2.20.7 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 52: 4.2.21.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 53: 4.2.21.2 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 54: 4.2.21.3 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 55: 4.2.21.4 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 56: 4.2.21.5 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 57: 4.2.21.6 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 58: 4.2.21.7 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 59: 4.2.21.8 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 60: 4.2.22 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 61: 4.2.23 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 62: 4.2.24 | req=optional | prod=common | lot=common | term=common | pm=qr
Idx 63: 4.2.25 | req=optional | prod=common | lot=common | term=common | pm=qr
Idx 64: 4.2.26 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 65: 5.1.1.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 66: 5.1.1.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 67: 5.1.1.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 68: 5.1.1.4 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 69: 5.1.1.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 70: 5.1.1.6 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 71: 5.1.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 72: 5.1.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 73: 5.1.4 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 74: 5.1.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 75: 5.1.6 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 76: 5.1.7 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 77: 5.1.8.1 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 78: 5.1.8.2 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 79: 5.1.8.3 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 80: 5.1.8.4 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 81: 5.1.8.5 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 82: 5.1.8.6 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 83: 5.1.8.7 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 84: 5.1.8.8 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 85: 5.1.8.9 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 86: 5.1.8.10 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 87: 5.1.8.11 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 88: 5.1.8.12 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 89: 5.1.8.13 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 90: 5.1.9 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 91: 5.1.10 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 92: 5.1.11 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 93: 5.1.12 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 94: 5.1.13 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 95: 5.1.14 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 96: 5.1.15 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 97: 5.1.16 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 98: 5.1.17.1 | req=optional | prod=trade_acquiring | lot=common | term=pos | pm=common
Idx 99: 5.1.17.2 | req=optional | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 100: 5.2.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 101: 5.2.2 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 102: 5.2.3 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 103: 5.2.4 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 104: 5.2.5 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 105: 5.2.6 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common
Idx 106: 5.2.7 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 107: 5.2.8 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 108: 5.2.9 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr
Idx 109: 5.2.10 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 110: 5.2.12 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=qr
Idx 111: 6.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 112: 6.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 113: 6.3 | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common
Idx 114: 6.4 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 115: 6.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 116: 6.6 | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common
Idx 117: 6.7 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 118: 6.8 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 119: 6.9 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
Idx 120: 6.10 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 121: 6.11 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 122: 6.12 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
Idx 123: 6.13 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 124: 6.14 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 125: 6.15 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
Idx 126: 6.16 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 127: 6.17 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
Idx 128: 6.18 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
Idx 129: 6.20 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 130: 6.21 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 131: 7.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 132: 7.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 133: 7.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 134: 7.4 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 135: 7.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 136: 7.6 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 137: 7.7 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 138: 7.8 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 139: 7.9 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 140: 7.10 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 141: 7.11 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 142: 7.12 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 143: 7.13 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
Idx 144: 7.14 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 145: 7.15 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 146: 7.16 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 147: 7.17 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 148: 8.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 149: 8.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 150: 9.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 151: 9.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 152: 9.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 153: 10.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 154: 10.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 155: 10.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
Idx 156: 11.1 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 157: 11.2 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 158: 11.3 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 159: 11.4 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 160: 11.5 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 161: 11.6 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 162: 11.7 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 163: 11.8 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 164: 11.9 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 165: 11.10 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 166: 11.11 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 167: 11.12 | req=optional | prod=common | lot=common | term=common | pm=common
Idx 168: 11.13 | req=optional | prod=common | lot=common | term=common | pm=common

[Command succeeded with exit code 0]
AI: Now I can see the matrix structure. Batch 3 covers indices 97-144 (0-indexed), which are matrix items from index 97 to 144. Let me map these:

- Idx 97: 5.1.16
- Idx 98: 5.1.17.1
- Idx 99: 5.1.17.2
- Idx 100: 5.2.1 (internet_acquiring → out_of_scope)
- Idx 101: 5.2.2 (internet_acquiring → out_of_scope)
- Idx 102: 5.2.3
- Idx 103: 5.2.4
- Idx 104: 5.2.5
- Idx 105: 5.2.6
- Idx 106: 5.2.7
- Idx 107: 5.2.8
- Idx 108: 5.2.9
- Idx 109: 5.2.10
- Idx 110: 5.2.12 (internet_acquiring → out_of_scope)
- Idx 111: 6.1
- Idx 112: 6.2
- Idx 113: 6.3 (fz_223 → out_of_scope)
- Idx 114: 6.4
- Idx 115: 6.5
- Idx 116: 6.6 (fz_223 → out_of_scope)
- Idx 117: 6.7
- Idx 118: 6.8
- Idx 119: 6.9 (fz_223 → out_of_scope)
- Idx 120: 6.10
- Idx 121: 6.11
- Idx 122: 6.12 (fz_223 → out_of_scope)
- Idx 123: 6.13
- Idx 124: 6.14
- Idx 125: 6.15 (fz_223 → out_of_scope)
- Idx 126: 6.16
- Idx 127: 6.17
- Idx 128: 6.18 (fz_223 → out_of_scope)
- Idx 129: 6.20
- Idx 130: 6.21
- Idx 131: 7.1
- Idx 132: 7.2
- Idx 133: 7.3
- Idx 134: 7.4
- Idx 135: 7.5
- Idx 136: 7.6
- Idx 137: 7.7
- Idx 138: 7.8
- Idx 139: 7.9
- Idx 140: 7.10
- Idx 141: 7.11
- Idx 142: 7.12
- Idx 143: 7.13 (internet_acquiring → out_of_scope)
- Idx 144: 7.14

Now let me set up my task plan and read the matrix items and contract text.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read matrix items 97-144 (indices 97-144) from inputs/matrix.json', 'status': 'in_progress'}, {'content': 'Read contract text from inputs/contract.txt', 'status': 'pending'}, {'content': 'Read existing legal_propositions.json for contract-side propositions', 'status': 'pending'}, {'content': 'Identify out_of_scope items in batch 3 (5.2.1, 5.2.2, 5.2.12, 6.3, 6.6, 6.9, 6.12, 6.15, 6.18, 7.13)', 'status': 'pending'}, {'content': 'Analyze each applicable matrix item 97-144 against contract for legal analogues', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, coverage_ledger rows for batch 3', 'status': 'pending'}, {'content': 'Write batch_3_results.json to /outputs/working/', 'status': 'pending'}]}, 'id': 'call_00_1G7IAO6ReJrSKYGGxnPB1991', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read matrix items 97-144 (indices 97-144) from inputs/matrix.json', 'status': 'in_progress'}, {'content': 'Read contract text from inputs/contract.txt', 'status': 'pending'}, {'content': 'Read existing legal_propositions.json for contract-side propositions', 'status': 'pending'}, {'content': 'Identify out_of_scope items in batch 3 (5.2.1, 5.2.2, 5.2.12, 6.3, 6.6, 6.9, 6.12, 6.15, 6.18, 7.13)', 'status': 'pending'}, {'content': 'Analyze each applicable matrix item 97-144 against contract for legal analogues', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, coverage_ledger rows for batch 3', 'status': 'pending'}, {'content': 'Write batch_3_results.json to /outputs/working/', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 96, 'limit': 50}, 'id': 'call_00_8xwVsiLjDKEPmJhTVAgg9071', 'type': 'tool_call'}]
Tool:     97	  "payment_method":"common"
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
AI: The matrix JSON file seems to have a different structure than expected. Let me read it from the beginning to understand its format.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 30}, 'id': 'call_00_2dFN67isSCYU2ITmIdm53684', 'type': 'tool_call'}]
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
AI: Good. The matrix is a flat JSON array. Now I need to read items at indices 97-144. Let me use a Python script to extract them efficiently.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'inputs/matrix.json\') as f:\n    m = json.load(f)\nfor i in range(97, 145):\n    it = m[i]\n    print(f\'=== IDX {i}: {it[\\"number\\"]} ===\')\n    print(f\'required_type: {it[\\"required_type\\"]}\')\n    print(f\'only_for_product: {it[\\"only_for_product\\"]}\')\n    print(f\'only_for_lot: {it[\\"only_for_lot\\"]}\')\n    print(f\'only_for_terminal: {it[\\"only_for_terminal\\"]}\')\n    print(f\'payment_method: {it[\\"payment_method\\"]}\')\n    print(f\'main_idea: {it[\\"main_idea\\"]}\')\n    print(f\'enriched_text: {it[\\"enriched_text\\"][:300]}...\')\n    print(f\'topics: {it[\\"topics\\"]}\')\n    print()\n"'}, 'id': 'call_00_el3l4om4C00jtaO8fvY78355', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 7
[stderr]     print(f'=== IDX {i}: {it[" number\]}
[stderr]                              ^
[stderr] SyntaxError: unterminated string literal (detected at line 7)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/extract_batch3.py', 'content': 'import json\n\nwith open(\'inputs/matrix.json\') as f:\n    m = json.load(f)\n\nfor i in range(97, 145):\n    it = m[i]\n    print(f\'=== IDX {i}: {it["number"]} ===\')\n    print(f\'required_type: {it["required_type"]}\')\n    print(f\'only_for_product: {it["only_for_product"]}\')\n    print(f\'only_for_lot: {it["only_for_lot"]}\')\n    print(f\'only_for_terminal: {it["only_for_terminal"]}\')\n    print(f\'payment_method: {it["payment_method"]}\')\n    print(f\'main_idea: {it["main_idea"]}\')\n    print(f\'enriched_text: {it["enriched_text"][:500]}\')\n    print(f\'topics: {it["topics"]}\')\n    print()\n'}, 'id': 'call_00_kfcNa4os13ryP8Fup74z7672', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/extract_batch3.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/extract_batch3.py'}, 'id': 'call_00_8anFuNbdGDtW6rFlLV1x9493', 'type': 'tool_call'}]
Tool: === IDX 97: 5.1.16 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј']

=== IDX 98: 5.1.17.1 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: pos
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р° РїРѕСЃР»РµРґРЅРёР№ РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РјРµСЃСЏС† (Р±РµР· СѓС‡РµС‚Р° РІ РѕР±РѕСЂРѕС‚Рµ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°);
topics: ['РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±']

=== IDX 99: 5.1.17.2 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ 5.1.17.2. РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р° РїРѕСЃР»РµРґРЅРёР№ РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РјРµСЃСЏС† (Р±РµР· СѓС‡РµС‚Р° РІ РѕР±РѕСЂРѕС‚Рµ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°) РёР»Рё РёРјРµРµС‚СЃСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚СЊ Рї
topics: ['С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏРј Р±Р°РЅРєР°', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°']

=== IDX 100: 5.2.1 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РћРїРµСЂР°С†РёР№.
topics: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ', 'РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ']

=== IDX 101: 5.2.2 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№ РІ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіРµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Рё РўРµС…РЅРѕР»РѕРіРёР№ 3DSecure
topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё', 'РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure']

=== IDX 102: 5.2.3 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»РєРё РЅР° СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј РЅРµ СЏРІР»СЏРµС‚СЃСЏ
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЈСЃС‚Р°РЅРѕРІРёС‚СЊ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№. РџСЂРѕРІРµСЃС‚Рё РїРµСЂРІРёС‡РЅС‹Р№ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹РјРё Р‘Р°РЅРєРѕРј
topics: ['СѓСЃС‚Р°РЅРѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РїРѕРґРіРѕС‚РѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё', 'РїСЂРѕРІРµРґРµРЅРёРµ РїРµСЂРІРёС‡РЅРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў']

=== IDX 103: 5.2.4 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ РђРІС‚РѕСЂРёР·Р°С†РёСЋ
topics: ['Р‘Р°РЅРє РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚ РђРІС‚РѕСЂРёР·Р°С†РёСЋ Р±РµР· РїРµСЂРµСЂС‹РІРѕРІ 24 С‡Р°СЃР° РІ СЃСѓС‚РєРё']

=== IDX 104: 5.2.5 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р Р°Р·РјРµСЃС‚РёС‚СЊ РЅР° СЃР°Р№С‚Рµ:  https://www.sberbank.ru/help/business/acquiring РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ
topics: ['РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РјРµС‰РµРЅС‹ РїРѕ СѓРєР°Р·Р°РЅРЅРѕР№ СЃСЃС‹Р»РєРµ', 'РјР°С‚РµСЂРёР°Р»С‹ РґРѕСЃС‚СѓРїРЅС‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ']

=== IDX 105: 5.2.6 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РЅРµРѕР±С…РѕРґРёРјС‹РјРё РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№
topics: ['РћР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё', 'РћР±РµСЃРїРµС‡РµРЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё']

=== IDX 106: 5.2.7 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ. Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° РёР· СЃС‚СЂРѕСЏ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° Р‘Р°РЅРєР°, РѕР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїСЂР°РІРЅС‹Рј Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРј Р‘Р°РЅРєР° РЅРµ РїРѕР·РґРЅРµРµ 3 (С‚СЂРµС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ Р‘Р°РЅРєРѕРј Р·Р°СЏРІРєРё РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ РЅРѕРјРµСЂСѓ СЃР»СѓР¶Р±С‹ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР° РїРѕ С‚РµР»РµС„РѕРЅР°Рј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ Рї..2. РџРѕСЂСЏРґРєР° РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅС‹С… С‚РѕС‡РєР°С…/РЅР° Р РµСЃСѓСЂСЃРµ.
topics: ['РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅР°СЏ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р·Р°РјРµРЅР° РЅРµРёСЃРїСЂР°РІРЅРѕРіРѕ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РЅР° РёСЃРїСЂР°РІРЅС‹Р№ РЅРµ РїРѕР·РґРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ Р·Р°СЏРІРєРё']

=== IDX 107: 5.2.8 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕР№ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё, РїРµСЂРµРґР°РЅРЅРѕР№ РѕС‚ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°  / Р РµСЃСѓСЂСЃР° /QR-РєРѕРґР°  РІ Р‘Р°РЅРє, РЅРµ РїРѕР·РґРЅРµРµ 2 (РґРІСѓС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј РїРµСЂРµС‡РёСЃР»СЏС‚СЊ РЅР° СЂР°СЃС‡РµС‚РЅС‹Р№ (С‚РµРєСѓС‰РёР№) СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ РІ РІР°Р»СЋС‚Рµ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё (СЂСѓР±Р»Рё Р Р¤) Р·Р° РІС‹С‡РµС‚РѕРј СЃСѓРјРј, РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹С… РІ Рї.5.1.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР°. Р”Р°С‚РѕР№ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј СЏРІР»СЏРµС‚СЃСЏ РґР°
topics: ['РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅРµ РїРѕР·РґРЅРµРµ 2 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё', 'РґР°С‚Р° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё - СЂР°Р±РѕС‡РёР№ РґРµРЅСЊ, СЃР»РµРґСѓСЋС‰РёР№ Р·Р° РґРЅРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ СЃРІРµСЂРєРё РёС‚РѕРіРѕРІ', 'РїСЂРё С‚РµС…РЅРёС‡РµСЃРєРѕРј СЃР±РѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёСЃС…РѕРґРёС‚ С‡РµСЂРµР· 3 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅСЏ РїРѕСЃР»Рµ РїРѕСЃР»РµРґРЅРµР№ СѓСЃРїРµС€РЅРѕР№ СЃРІРµСЂРєРё']

=== IDX 108: 5.2.9 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: qr
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РїРѕ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј РєР°РЅР°Р»Р°Рј СЃРІСЏР·Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ
topics: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ QR-РєРѕРґР° РїР°СЂС‚РЅРµСЂР° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ']

=== IDX 109: 5.2.10 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РѕР±СЂР°Р±РѕС‚РєСѓ РџР”РЅ, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, Р° С‚Р°РєР¶Рµ РѕР±РµСЃРїРµС‡РёС‚СЊ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕСЃС‚СЊ Рё Р·Р°С‰РёС‚Сѓ РѕР±СЂР°Р±Р°С‚С‹РІР°РµРјС‹С… РџР”РЅ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° РѕС‚ 27 РёСЋР»СЏ 2006 в„– 152-Р¤Р— В«Рћ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…В». РџСЂРёРЅРёРјР°С‚СЊ РЅРµРѕР±С…РѕРґРёРјС‹Рµ РїСЂР°РІРѕРІС‹Рµ, РѕСЂРіР°РЅРёР·Р°С†РёРѕРЅРЅС‹Рµ Рё С‚РµС…РЅРёС‡РµСЃРєРёРµ РјРµСЂС‹ РёР»Рё РѕР±РµСЃРїРµС‡РёРІР°С‚СЊ РёС… РїСЂРёРЅСЏС‚РёРµ РґР»СЏ Р·Р°С‰РёС‚С‹ РїРѕР»СѓС‡Р°РµРјС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РџР”РЅ РѕС‚ РЅРµРїСЂР°РІРѕРјРµСЂРЅРѕРіРѕ РёР»Рё СЃР»СѓС‡Р°Р№РЅРѕРіРѕ РґРѕСЃС‚СѓРїР° Рє РЅРёРј, СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ, РёР·РјРµРЅРµРЅРёСЏ, Р±Р»РѕРєРёСЂРѕРІР°РЅРёСЏ, РєРѕРїРёСЂРѕРІР°
topics: []

=== IDX 110: 5.2.12 ===
required_type: optional
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: qr
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API (РІ С‚.С‡. РІСЃС‘, С‡С‚Рѕ СЃРІСЏР·Р°РЅРѕ СЃ РѕСЂРіР°РЅРёР·Р°С†РёРµР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РїРѕСЃСЂРµРґСЃС‚РІРѕРј С‚Р°РєРѕРіРѕ API) В«РєР°Рє РµСЃС‚СЊВ» Р±РµР· РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РєР°РєРёС…-Р»РёР±Рѕ РіР°СЂР°РЅС‚РёР№
topics: ['Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API Р±РµР· РіР°СЂР°РЅС‚РёР№']

=== IDX 111: 6.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р—Р° РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹, РџСЂРµРґРїСЂРёСЏС‚РёРµ СѓРїР»Р°С‡РёРІР°РµС‚ Р‘Р°РЅРєСѓ РїР»Р°С‚Сѓ РІ СЂР°Р·РјРµСЂРµ:
В«(____________) РїСЂРѕС†РµРЅС‚ РѕС‚ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚В».
topics: ['СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№']

=== IDX 112: 6.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµСЂРёРѕРґРёС‡РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚[2] (РґР°Р»РµРµ вЂ“ РЈРџР”) РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†. 
Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р‘Р°РЅРєР°, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРµ Рї.6.1 Р”РѕРіРѕРІРѕСЂР°, РІРєР»СЋС‡Р°РµС‚ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°', 'РІ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РІРєР»СЋС‡РµРЅ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРј', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']

=== IDX 113: 6.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: fz_223
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РђРєС‚ Рѕ РїРµСЂРµС‡РёСЃР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРј РѕРїРµСЂР°С†РёР№ РїРѕ РєР°СЂС‚Р°Рј РїРѕ С„РѕСЂРјРµ РџСЂРёР»РѕР¶РµРЅРёСЏ 2 Рє Р”РѕРіРѕРІРѕСЂСѓ (РґР°Р»РµРµ вЂ“ РђРєС‚) Рё СЃС‡РµС‚ С„.363 РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ, РїСЂРёС‡РёС‚Р°СЋС‰РµРіРѕСЃСЏ Р‘Р°РЅРєСѓ, РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї.6.1 Р”РѕРіРѕРІРѕСЂР° Рё РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї. 3 СЃС‚
topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РђРєС‚ РґРѕ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РђРєС‚ РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РІРјРµСЃС‚Рµ СЃРѕ СЃС‡РµС‚РѕРј-С„Р°РєС‚СѓСЂРѕР№ С„РѕСЂРјС‹ 363', 'Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ 6.1 РґРѕРіРѕРІРѕСЂР°', 'Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї.3 СЃС‚.149 РќРљ Р Р¤', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ Р‘Р°РЅРєРѕРј РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']

=== IDX 114: 6.4 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Рё РІРѕР·РІСЂР°С‚РёС‚СЊ РЈРџР” (РїСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё)', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']

=== IDX 115: 6.5 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р±Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']

=== IDX 116: 6.6 ===
required_type: mandatory
only_for_product: common
only_for_lot: fz_223
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° РђРєС‚Р° Рё СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.
topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р°РєС‚Р° Рё СЃС‡РµС‚Р° С„РѕСЂРјС‹ 363', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РЅР° СЃС‡РµС‚, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„РѕСЂРјС‹ 363']

=== IDX 117: 6.7 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ РІ СЂР°Р·РјРµСЂРµ _____ (__________________) СЂСѓР±Р»РµР№ (РІРєР»СЋС‡Р°СЏ РќР”РЎ) Р·Р° РєР°Р¶РґС‹Р№ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р».
topics: ['СѓРєР°Р·Р°РЅ СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°', 'СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂСѓР±Р»РµР№ РІРєР»СЋС‡Р°СЏ РќР”РЎ', 'СѓСЃС‚Р°РЅРѕРІР»РµРЅ РµР¶РµРјРµСЃСЏС‡РЅС‹Р№ РїРѕСЂСЏРґРѕРє РѕРїР»Р°С‚С‹']

=== IDX 118: 6.8 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.

topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ']

=== IDX 119: 6.9 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё
topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚ РІС‹СЃС‚Р°РІР»СЏРµС‚СЃСЏ РїРѕ С„РѕСЂРјРµ в„–363', 'РЎС‡РµС‚ СЃРѕРґРµСЂР¶РёС‚ СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== IDX 120: 6.10 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓРєР°Р·Р°РЅРЅС‹Рµ СЃСЂРѕРєРё']

=== IDX 121: 6.11 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
topics: ['РѕРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ С„РѕСЂРјР°', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']

=== IDX 122: 6.12 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.
topics: ['РћРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РЎРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РћСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'РџРѕР»СѓС‡Р°С‚РµР»СЊ РїР»Р°С‚РµР¶Р° - СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ']

=== IDX 123: 6.13 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ Р·Р° РєР°Р¶РґС‹Р№ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚Р°СЂРёС„РѕРј, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рј РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РІ РџСЂРёР»РѕР¶РµРЅРёРё 1.1 Рє Р”РѕРіРѕРІРѕСЂСѓ. РџСЂРё СЌС‚РѕРј СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РєРѕР»РёС‡РµСЃС‚РІСѓ РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РІ РўРЎРў. РџСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РїРµСЂРµСЃС‡РёС‚С‹РІР°РµС‚СЃСЏ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РЅРµР·Р°РІРёСЃРёРјРѕ РѕС‚ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё/СЃРЅСЏС‚РёСЏ СЃРєР°РЅРµСЂ
topics: ['РїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РµР¶РµРјРµСЃСЏС‡РЅР°СЏ', 'СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РґРЅСЏРј РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»Р°', 'РїРµСЂРµСЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° Р·Р° РѕС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†', 'СѓРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ']

=== IDX 124: 6.14 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ']

=== IDX 125: 6.15 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== IDX 126: 6.16 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']

=== IDX 127: 6.17 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
topics: ['РѕРїР»Р°С‚Р° СЃРµСЂРІРёСЃР° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']

=== IDX 128: 6.18 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363
topics: ['РѕРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'СЃСЂРѕРє РѕРїР»Р°С‚С‹ СЃС‡РёС‚Р°РµС‚СЃСЏ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЃС‡РµС‚Р°']

=== IDX 129: 6.20 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџРѕ РћРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рј С‚СЂР°РЅР·Р°РєС†РёСЏРј РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РЅРµ РІР·РёРјР°РµС‚СЃСЏ. Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ, СѓРґРµСЂР¶Р°РЅРЅР°СЏ Р‘Р°РЅРєРѕРј РїСЂРё РѕР±СЂР°Р±РѕС‚РєРµ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РћРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹, РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ.
topics: ['РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° РЅРµ РІР·РёРјР°РµС‚СЃСЏ', 'СѓРґРµСЂР¶Р°РЅРЅР°СЏ РїР»Р°С‚Р° Р·Р° СЂР°СЃС‡РµС‚С‹ РїСЂРё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РѕРїРµСЂР°С†РёРё РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ']

=== IDX 130: 6.21 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: РћС‚СЃСѓС‚СЃС‚РІРёРµ РєРѕРЅРєСЂРµС‚РЅРѕР№ С†РµРЅРЅС‹ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёРµРј
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ _________ (______________________) СЂСѓР±Р»РµР№ __ РєРѕРїРµРµРє. ( РІ С‚РѕРј С‡РёСЃР»Рµ РќР”РЎ)
topics: ['Р¦РµРЅР° РґРѕРіРѕРІРѕСЂР° РІ СЂСѓР±Р»СЏС…', 'РЈРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃСѓРјРјР° РІ СЂСѓР±Р»СЏС… Рё РєРѕРїРµР№РєР°С…', 'РЈРїРѕРјРёРЅР°РЅРёРµ Рѕ РІРєР»СЋС‡РµРЅРёРё РќР”РЎ']

=== IDX 131: 7.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР° Рё Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤.
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР°', 'РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== IDX 132: 7.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р°
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
Р±) 5000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 10000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓ
topics: ['РЁС‚СЂР°С„ РџСЂРµРґРїСЂРёСЏС‚РёСЋ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё.']

=== IDX 133: 7.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°.
topics: ['РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°']

=== IDX 134: 7.4 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№).РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ Р”РѕРіРѕРІРѕСЂРѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ РїРѕСЃР»Рµ РґРЅСЏ РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ Р”РѕРіРѕРІРѕСЂРѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°
topics: ['Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№)', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РќР°С‡РёСЃР»РµРЅРёРµ РїРµРЅРё Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ.РћРїСЂРµРґРµР»РµРЅРёСЏ СЃСЂРѕРєР° РЅР°С‡Р°Р»Р° РЅР°С‡РёСЃР»РµРЅРёСЏ РїРµРЅРё', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РћРїСЂРµРґРµР»РµРЅРёРµ СЂР°Р·РјРµСЂР° РїРµРЅРё']

=== IDX 135: 7.5 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 10 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 1 РїСЂРѕС†РµРЅС‚ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕ
topics: ['Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё, РёРјРµСЋС‰РёС… СЃС‚РѕРёРјРѕСЃС‚РЅРѕРµ РІС‹СЂР°Р¶РµРЅРёСЏ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РґРѕРіРѕРІРѕСЂР°']

=== IDX 136: 7.6 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 10000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
Рі) 1000
topics: ['Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, РЅРµ РёРјРµСЋС‰РµРіРѕ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ']

=== IDX 137: 7.7 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ Р¦РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°']

=== IDX 138: 7.8 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ(Р—Р°РєР°Р·С‡РёРєР°) Рё РџРѕРєСѓРїР°С‚РµР»СЏ (РєР»РёРµРЅС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ)
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј, РІРѕР·РЅРёРєР°СЋС‰РёРј РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј Рё РџРѕРєСѓРїР°С‚РµР»РµРј РІРѕ РІСЃРµС… СЃР»СѓС‡Р°СЏС…, РєРѕРіРґР° С‚Р°РєРёРµ СЃРїРѕСЂС‹ Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє РїСЂРµРґРјРµС‚Сѓ Р”РѕРіРѕРІРѕСЂР°, Р° С‚Р°РєР¶Рµ РїРѕ СЃРїРѕСЂР°Рј РІ РѕС‚РЅРѕС€РµРЅРёРё РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РѕРїР»Р°С‡РµРЅРЅС‹С… СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚С‹ / РµРµ СЂРµРєРІРёР·РёС‚РѕРІ / NFРЎ-РєР°СЂС‚С‹ / SberPay / РџР»Р°С‚Рё QR / РџР»Р°С‚РµР¶РЅРѕРіРѕ СЃС‡РµС‚Р°.
topics: ['РћС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР° (Р�СЃРїРѕР»РЅРёС‚РµР»СЏ) Р·Р° СЃРїРѕСЂС‹ РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј (Р—Р°РєР°Р·С‡РёРєРѕРј) Рё РџРѕРєСѓРїР°С‚РµР»РµРј (РљР»РёРµРЅС‚ Р—Р°РєР°Р·С‡РёРєР°)']

=== IDX 139: 7.9 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєРё РїРµСЂРµРІРѕРґР° РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РµСЃР»Рё Р·Р°РґРµСЂР¶РєРё РїСЂРѕРёР·РѕС€Р»Рё РЅРµ РїРѕ РІРёРЅРµ Р‘Р°РЅРєР°.
topics: ['Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё Р·Р°РґРµСЂР¶РєР°С… РїРµСЂРµРІРѕРґРѕРІ Р±РµР· СЃРІРѕРµР№ РІРёРЅС‹']

=== IDX 140: 7.10 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°, РѕР±СѓСЃР»РѕРІР»РµРЅРЅРѕРµ РґРµР№СЃС‚РІРёСЏРјРё РёР»Рё Р±РµР·РґРµР№СЃС‚РІРёСЏРјРё С‚СЂРµС‚СЊРёС… Р»РёС†, РІ С‚РѕРј С‡РёСЃР»Рµ СѓС‡Р°СЃС‚РЅРёРєР°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹
topics: ['Р‘Р°РЅРє РЅРµ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РІ СЃРІСЏР·Рё СЃ РґРµР№СЃС‚РІРёРµРј Рё Р±РµР·РґРµР№СЃС‚РІРёРµРј С‚СЂРµС‚СЊРёС… Р»РёС†']

=== IDX 141: 7.11 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСѓРјРј РћРїРµСЂР°С†РёР№ РїРѕ РїСЂРёС‡РёРЅРµ РїСЂРѕРІРµРґРµРЅРёСЏ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ Р‘Р°РЅРєРѕРј РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РїСЂРѕРІРµРґРµРЅРёРµ РћРїРµСЂР°С†РёРё СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°
topics: ['Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ РІ СЃР»СѓС‡Р°Рµ РёРЅРёС†РёРёСЂРѕРІР°РЅРёСЏ РёРј СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ РѕРїРµСЂР°С†РёР№']

=== IDX 142: 7.12 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РІ СЃР»СѓС‡Р°Рµ РїСЂРµРІС‹С€РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р±Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё РїСЂРµРІС‹С€РµРЅРёРё Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°']

=== IDX 143: 7.13 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№, СЃРѕРІРµСЂС€РµРЅРЅС‹С… РЅР° Р РµСЃСѓСЂСЃРµ, РІ СЃР»СѓС‡Р°Рµ РЅРµРІС‹РїРѕР»РЅРµРЅРёСЏ Рї. 4.2.21.1 Р”РѕРіРѕРІРѕСЂР°
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅС‹Рµ РѕРїРµСЂР°С†РёРё РЅР° Р РµСЃСѓСЂСЃРµ']

=== IDX 144: 7.14 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјС‹Рµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў РІ РЎРџР­Рџ
topics: ['РћР±С‰РµРµ СѓС‚РІРµСЂР¶РґРµРЅРёРµ Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ РІ РЎРџР­Рџ']


[Command succeeded with exit code 0]
AI: The text is garbled due to encoding issues. Let me read the matrix items directly from the JSON file using a Python script that properly handles the encoding.[{'name': 'write_file', 'args': {'content': 'import json\n\nwith open(\'inputs/matrix.json\', encoding=\'utf-8\') as f:\n    m = json.load(f)\n\nfor i in range(97, 145):\n    it = m[i]\n    print(f\'=== IDX {i}: {it["number"]} ===\')\n    print(f\'required_type: {it["required_type"]}\')\n    print(f\'only_for_product: {it["only_for_product"]}\')\n    print(f\'only_for_lot: {it["only_for_lot"]}\')\n    print(f\'only_for_terminal: {it["only_for_terminal"]}\')\n    print(f\'payment_method: {it["payment_method"]}\')\n    print(f\'main_idea: {it["main_idea"]}\')\n    print(f\'enriched_text: {it["enriched_text"][:500]}\')\n    print(f\'topics: {it["topics"]}\')\n    print()\n', 'file_path': '/outputs/working/extract_batch3.py'}, 'id': 'call_00_9kOvnXeBvvv4XxlKdUlI1849', 'type': 'tool_call'}]
Tool: Cannot write to /outputs/working/extract_batch3.py because it already exists. Read and then make an edit, or write to a new path.
AI: [{'name': 'write_file', 'args': {'content': 'import json\n\nwith open(\'inputs/matrix.json\', encoding=\'utf-8\') as f:\n    m = json.load(f)\n\nfor i in range(97, 145):\n    it = m[i]\n    print(f\'=== IDX {i}: {it["number"]} ===\')\n    print(f\'required_type: {it["required_type"]}\')\n    print(f\'only_for_product: {it["only_for_product"]}\')\n    print(f\'only_for_lot: {it["only_for_lot"]}\')\n    print(f\'only_for_terminal: {it["only_for_terminal"]}\')\n    print(f\'payment_method: {it["payment_method"]}\')\n    print(f\'main_idea: {it["main_idea"]}\')\n    print(f\'enriched_text: {it["enriched_text"][:500]}\')\n    print(f\'topics: {it["topics"]}\')\n    print()\n', 'file_path': '/outputs/working/extract_batch3_v2.py'}, 'id': 'call_00_YtgfxbHXXS9eBZhVNqbu8253', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/extract_batch3_v2.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/extract_batch3_v2.py'}, 'id': 'call_00_1J0boIIba2DmK1jV83674506', 'type': 'tool_call'}]
Tool: === IDX 97: 5.1.16 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј']

=== IDX 98: 5.1.17.1 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: pos
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р° РїРѕСЃР»РµРґРЅРёР№ РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РјРµСЃСЏС† (Р±РµР· СѓС‡РµС‚Р° РІ РѕР±РѕСЂРѕС‚Рµ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°);
topics: ['РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±']

=== IDX 99: 5.1.17.2 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ 5.1.17.2. РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р° РїРѕСЃР»РµРґРЅРёР№ РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РјРµСЃСЏС† (Р±РµР· СѓС‡РµС‚Р° РІ РѕР±РѕСЂРѕС‚Рµ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°) РёР»Рё РёРјРµРµС‚СЃСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚СЊ Рї
topics: ['С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏРј Р±Р°РЅРєР°', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°']

=== IDX 100: 5.2.1 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РћРїРµСЂР°С†РёР№.
topics: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ', 'РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ']

=== IDX 101: 5.2.2 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№ РІ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіРµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Рё РўРµС…РЅРѕР»РѕРіРёР№ 3DSecure
topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё', 'РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure']

=== IDX 102: 5.2.3 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»РєРё РЅР° СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј РЅРµ СЏРІР»СЏРµС‚СЃСЏ
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЈСЃС‚Р°РЅРѕРІРёС‚СЊ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№. РџСЂРѕРІРµСЃС‚Рё РїРµСЂРІРёС‡РЅС‹Р№ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹РјРё Р‘Р°РЅРєРѕРј
topics: ['СѓСЃС‚Р°РЅРѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РїРѕРґРіРѕС‚РѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё', 'РїСЂРѕРІРµРґРµРЅРёРµ РїРµСЂРІРёС‡РЅРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў']

=== IDX 103: 5.2.4 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ РђРІС‚РѕСЂРёР·Р°С†РёСЋ
topics: ['Р‘Р°РЅРє РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚ РђРІС‚РѕСЂРёР·Р°С†РёСЋ Р±РµР· РїРµСЂРµСЂС‹РІРѕРІ 24 С‡Р°СЃР° РІ СЃСѓС‚РєРё']

=== IDX 104: 5.2.5 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р Р°Р·РјРµСЃС‚РёС‚СЊ РЅР° СЃР°Р№С‚Рµ:  https://www.sberbank.ru/help/business/acquiring РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ
topics: ['РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РјРµС‰РµРЅС‹ РїРѕ СѓРєР°Р·Р°РЅРЅРѕР№ СЃСЃС‹Р»РєРµ', 'РјР°С‚РµСЂРёР°Р»С‹ РґРѕСЃС‚СѓРїРЅС‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ']

=== IDX 105: 5.2.6 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РЅРµРѕР±С…РѕРґРёРјС‹РјРё РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№
topics: ['РћР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё', 'РћР±РµСЃРїРµС‡РµРЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё']

=== IDX 106: 5.2.7 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ. Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° РёР· СЃС‚СЂРѕСЏ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° Р‘Р°РЅРєР°, РѕР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїСЂР°РІРЅС‹Рј Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРј Р‘Р°РЅРєР° РЅРµ РїРѕР·РґРЅРµРµ 3 (С‚СЂРµС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ Р‘Р°РЅРєРѕРј Р·Р°СЏРІРєРё РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ РЅРѕРјРµСЂСѓ СЃР»СѓР¶Р±С‹ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР° РїРѕ С‚РµР»РµС„РѕРЅР°Рј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ Рї..2. РџРѕСЂСЏРґРєР° РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅС‹С… С‚РѕС‡РєР°С…/РЅР° Р РµСЃСѓСЂСЃРµ.
topics: ['РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅР°СЏ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р·Р°РјРµРЅР° РЅРµРёСЃРїСЂР°РІРЅРѕРіРѕ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РЅР° РёСЃРїСЂР°РІРЅС‹Р№ РЅРµ РїРѕР·РґРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ Р·Р°СЏРІРєРё']

=== IDX 107: 5.2.8 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕР№ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё, РїРµСЂРµРґР°РЅРЅРѕР№ РѕС‚ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°  / Р РµСЃСѓСЂСЃР° /QR-РєРѕРґР°  РІ Р‘Р°РЅРє, РЅРµ РїРѕР·РґРЅРµРµ 2 (РґРІСѓС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј РїРµСЂРµС‡РёСЃР»СЏС‚СЊ РЅР° СЂР°СЃС‡РµС‚РЅС‹Р№ (С‚РµРєСѓС‰РёР№) СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ РІ РІР°Р»СЋС‚Рµ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё (СЂСѓР±Р»Рё Р Р¤) Р·Р° РІС‹С‡РµС‚РѕРј СЃСѓРјРј, РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹С… РІ Рї.5.1.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР°. Р”Р°С‚РѕР№ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј СЏРІР»СЏРµС‚СЃСЏ РґР°
topics: ['РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅРµ РїРѕР·РґРЅРµРµ 2 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё', 'РґР°С‚Р° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё - СЂР°Р±РѕС‡РёР№ РґРµРЅСЊ, СЃР»РµРґСѓСЋС‰РёР№ Р·Р° РґРЅРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ СЃРІРµСЂРєРё РёС‚РѕРіРѕРІ', 'РїСЂРё С‚РµС…РЅРёС‡РµСЃРєРѕРј СЃР±РѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёСЃС…РѕРґРёС‚ С‡РµСЂРµР· 3 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅСЏ РїРѕСЃР»Рµ РїРѕСЃР»РµРґРЅРµР№ СѓСЃРїРµС€РЅРѕР№ СЃРІРµСЂРєРё']

=== IDX 108: 5.2.9 ===
required_type: optional
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: qr
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РїРѕ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј РєР°РЅР°Р»Р°Рј СЃРІСЏР·Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ
topics: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ QR-РєРѕРґР° РїР°СЂС‚РЅРµСЂР° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ']

=== IDX 109: 5.2.10 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РѕР±СЂР°Р±РѕС‚РєСѓ РџР”РЅ, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, Р° С‚Р°РєР¶Рµ РѕР±РµСЃРїРµС‡РёС‚СЊ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕСЃС‚СЊ Рё Р·Р°С‰РёС‚Сѓ РѕР±СЂР°Р±Р°С‚С‹РІР°РµРјС‹С… РџР”РЅ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° РѕС‚ 27 РёСЋР»СЏ 2006 в„– 152-Р¤Р— В«Рћ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…В». РџСЂРёРЅРёРјР°С‚СЊ РЅРµРѕР±С…РѕРґРёРјС‹Рµ РїСЂР°РІРѕРІС‹Рµ, РѕСЂРіР°РЅРёР·Р°С†РёРѕРЅРЅС‹Рµ Рё С‚РµС…РЅРёС‡РµСЃРєРёРµ РјРµСЂС‹ РёР»Рё РѕР±РµСЃРїРµС‡РёРІР°С‚СЊ РёС… РїСЂРёРЅСЏС‚РёРµ РґР»СЏ Р·Р°С‰РёС‚С‹ РїРѕР»СѓС‡Р°РµРјС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РџР”РЅ РѕС‚ РЅРµРїСЂР°РІРѕРјРµСЂРЅРѕРіРѕ РёР»Рё СЃР»СѓС‡Р°Р№РЅРѕРіРѕ РґРѕСЃС‚СѓРїР° Рє РЅРёРј, СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ, РёР·РјРµРЅРµРЅРёСЏ, Р±Р»РѕРєРёСЂРѕРІР°РЅРёСЏ, РєРѕРїРёСЂРѕРІР°
topics: []

=== IDX 110: 5.2.12 ===
required_type: optional
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: qr
main_idea: 
enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API (РІ С‚.С‡. РІСЃС‘, С‡С‚Рѕ СЃРІСЏР·Р°РЅРѕ СЃ РѕСЂРіР°РЅРёР·Р°С†РёРµР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РїРѕСЃСЂРµРґСЃС‚РІРѕРј С‚Р°РєРѕРіРѕ API) В«РєР°Рє РµСЃС‚СЊВ» Р±РµР· РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РєР°РєРёС…-Р»РёР±Рѕ РіР°СЂР°РЅС‚РёР№
topics: ['Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API Р±РµР· РіР°СЂР°РЅС‚РёР№']

=== IDX 111: 6.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р—Р° РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹, РџСЂРµРґРїСЂРёСЏС‚РёРµ СѓРїР»Р°С‡РёРІР°РµС‚ Р‘Р°РЅРєСѓ РїР»Р°С‚Сѓ РІ СЂР°Р·РјРµСЂРµ:
В«(____________) РїСЂРѕС†РµРЅС‚ РѕС‚ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚В».
topics: ['СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№']

=== IDX 112: 6.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµСЂРёРѕРґРёС‡РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚[2] (РґР°Р»РµРµ вЂ“ РЈРџР”) РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†. 
Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р‘Р°РЅРєР°, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРµ Рї.6.1 Р”РѕРіРѕРІРѕСЂР°, РІРєР»СЋС‡Р°РµС‚ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°', 'РІ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РІРєР»СЋС‡РµРЅ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРј', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']

=== IDX 113: 6.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: fz_223
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РђРєС‚ Рѕ РїРµСЂРµС‡РёСЃР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРј РѕРїРµСЂР°С†РёР№ РїРѕ РєР°СЂС‚Р°Рј РїРѕ С„РѕСЂРјРµ РџСЂРёР»РѕР¶РµРЅРёСЏ 2 Рє Р”РѕРіРѕРІРѕСЂСѓ (РґР°Р»РµРµ вЂ“ РђРєС‚) Рё СЃС‡РµС‚ С„.363 РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ, РїСЂРёС‡РёС‚Р°СЋС‰РµРіРѕСЃСЏ Р‘Р°РЅРєСѓ, РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї.6.1 Р”РѕРіРѕРІРѕСЂР° Рё РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї. 3 СЃС‚
topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РђРєС‚ РґРѕ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РђРєС‚ РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РІРјРµСЃС‚Рµ СЃРѕ СЃС‡РµС‚РѕРј-С„Р°РєС‚СѓСЂРѕР№ С„РѕСЂРјС‹ 363', 'Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ 6.1 РґРѕРіРѕРІРѕСЂР°', 'Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї.3 СЃС‚.149 РќРљ Р Р¤', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ Р‘Р°РЅРєРѕРј РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']

=== IDX 114: 6.4 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Рё РІРѕР·РІСЂР°С‚РёС‚СЊ РЈРџР” (РїСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё)', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']

=== IDX 115: 6.5 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р±Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']

=== IDX 116: 6.6 ===
required_type: mandatory
only_for_product: common
only_for_lot: fz_223
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° РђРєС‚Р° Рё СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.
topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р°РєС‚Р° Рё СЃС‡РµС‚Р° С„РѕСЂРјС‹ 363', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РЅР° СЃС‡РµС‚, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„РѕСЂРјС‹ 363']

=== IDX 117: 6.7 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ РІ СЂР°Р·РјРµСЂРµ _____ (__________________) СЂСѓР±Р»РµР№ (РІРєР»СЋС‡Р°СЏ РќР”РЎ) Р·Р° РєР°Р¶РґС‹Р№ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р».
topics: ['СѓРєР°Р·Р°РЅ СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°', 'СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂСѓР±Р»РµР№ РІРєР»СЋС‡Р°СЏ РќР”РЎ', 'СѓСЃС‚Р°РЅРѕРІР»РµРЅ РµР¶РµРјРµСЃСЏС‡РЅС‹Р№ РїРѕСЂСЏРґРѕРє РѕРїР»Р°С‚С‹']

=== IDX 118: 6.8 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.

topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ']

=== IDX 119: 6.9 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё
topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚ РІС‹СЃС‚Р°РІР»СЏРµС‚СЃСЏ РїРѕ С„РѕСЂРјРµ в„–363', 'РЎС‡РµС‚ СЃРѕРґРµСЂР¶РёС‚ СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== IDX 120: 6.10 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓРєР°Р·Р°РЅРЅС‹Рµ СЃСЂРѕРєРё']

=== IDX 121: 6.11 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
topics: ['РѕРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ С„РѕСЂРјР°', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']

=== IDX 122: 6.12 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.
topics: ['РћРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РЎРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РћСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'РџРѕР»СѓС‡Р°С‚РµР»СЊ РїР»Р°С‚РµР¶Р° - СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ']

=== IDX 123: 6.13 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ Р·Р° РєР°Р¶РґС‹Р№ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚Р°СЂРёС„РѕРј, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рј РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РІ РџСЂРёР»РѕР¶РµРЅРёРё 1.1 Рє Р”РѕРіРѕРІРѕСЂСѓ. РџСЂРё СЌС‚РѕРј СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РєРѕР»РёС‡РµСЃС‚РІСѓ РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РІ РўРЎРў. РџСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РїРµСЂРµСЃС‡РёС‚С‹РІР°РµС‚СЃСЏ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РЅРµР·Р°РІРёСЃРёРјРѕ РѕС‚ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё/СЃРЅСЏС‚РёСЏ СЃРєР°РЅРµСЂ
topics: ['РїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РµР¶РµРјРµСЃСЏС‡РЅР°СЏ', 'СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РґРЅСЏРј РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»Р°', 'РїРµСЂРµСЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° Р·Р° РѕС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†', 'СѓРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ']

=== IDX 124: 6.14 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ']

=== IDX 125: 6.15 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== IDX 126: 6.16 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']

=== IDX 127: 6.17 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
topics: ['РѕРїР»Р°С‚Р° СЃРµСЂРІРёСЃР° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']

=== IDX 128: 6.18 ===
required_type: mandatory
only_for_product: trade_acquiring
only_for_lot: fz_223
only_for_terminal: smart
payment_method: common
main_idea: 
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363
topics: ['РѕРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'СЃСЂРѕРє РѕРїР»Р°С‚С‹ СЃС‡РёС‚Р°РµС‚СЃСЏ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЃС‡РµС‚Р°']

=== IDX 129: 6.20 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџРѕ РћРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рј С‚СЂР°РЅР·Р°РєС†РёСЏРј РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РЅРµ РІР·РёРјР°РµС‚СЃСЏ. Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ, СѓРґРµСЂР¶Р°РЅРЅР°СЏ Р‘Р°РЅРєРѕРј РїСЂРё РѕР±СЂР°Р±РѕС‚РєРµ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РћРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹, РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ.
topics: ['РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° РЅРµ РІР·РёРјР°РµС‚СЃСЏ', 'СѓРґРµСЂР¶Р°РЅРЅР°СЏ РїР»Р°С‚Р° Р·Р° СЂР°СЃС‡РµС‚С‹ РїСЂРё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РѕРїРµСЂР°С†РёРё РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ']

=== IDX 130: 6.21 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: РћС‚СЃСѓС‚СЃС‚РІРёРµ РєРѕРЅРєСЂРµС‚РЅРѕР№ С†РµРЅРЅС‹ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёРµРј
enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ _________ (______________________) СЂСѓР±Р»РµР№ __ РєРѕРїРµРµРє. ( РІ С‚РѕРј С‡РёСЃР»Рµ РќР”РЎ)
topics: ['Р¦РµРЅР° РґРѕРіРѕРІРѕСЂР° РІ СЂСѓР±Р»СЏС…', 'РЈРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃСѓРјРјР° РІ СЂСѓР±Р»СЏС… Рё РєРѕРїРµР№РєР°С…', 'РЈРїРѕРјРёРЅР°РЅРёРµ Рѕ РІРєР»СЋС‡РµРЅРёРё РќР”РЎ']

=== IDX 131: 7.1 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР° Рё Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤.
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР°', 'РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']

=== IDX 132: 7.2 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р°
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
Р±) 5000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 10000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓ
topics: ['РЁС‚СЂР°С„ РџСЂРµРґРїСЂРёСЏС‚РёСЋ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё.']

=== IDX 133: 7.3 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°.
topics: ['РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°']

=== IDX 134: 7.4 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№).РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ Р”РѕРіРѕРІРѕСЂРѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ РїРѕСЃР»Рµ РґРЅСЏ РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ Р”РѕРіРѕРІРѕСЂРѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°
topics: ['Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№)', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РќР°С‡РёСЃР»РµРЅРёРµ РїРµРЅРё Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ.РћРїСЂРµРґРµР»РµРЅРёСЏ СЃСЂРѕРєР° РЅР°С‡Р°Р»Р° РЅР°С‡РёСЃР»РµРЅРёСЏ РїРµРЅРё', 'РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РћРїСЂРµРґРµР»РµРЅРёРµ СЂР°Р·РјРµСЂР° РїРµРЅРё']

=== IDX 135: 7.5 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 10 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 1 РїСЂРѕС†РµРЅС‚ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕ
topics: ['Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё, РёРјРµСЋС‰РёС… СЃС‚РѕРёРјРѕСЃС‚РЅРѕРµ РІС‹СЂР°Р¶РµРЅРёСЏ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РґРѕРіРѕРІРѕСЂР°']

=== IDX 136: 7.6 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 10000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
Рі) 1000
topics: ['Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, РЅРµ РёРјРµСЋС‰РµРіРѕ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ']

=== IDX 137: 7.7 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ Р¦РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°']

=== IDX 138: 7.8 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ(Р—Р°РєР°Р·С‡РёРєР°) Рё РџРѕРєСѓРїР°С‚РµР»СЏ (РєР»РёРµРЅС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ)
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј, РІРѕР·РЅРёРєР°СЋС‰РёРј РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј Рё РџРѕРєСѓРїР°С‚РµР»РµРј РІРѕ РІСЃРµС… СЃР»СѓС‡Р°СЏС…, РєРѕРіРґР° С‚Р°РєРёРµ СЃРїРѕСЂС‹ Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє РїСЂРµРґРјРµС‚Сѓ Р”РѕРіРѕРІРѕСЂР°, Р° С‚Р°РєР¶Рµ РїРѕ СЃРїРѕСЂР°Рј РІ РѕС‚РЅРѕС€РµРЅРёРё РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РѕРїР»Р°С‡РµРЅРЅС‹С… СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚С‹ / РµРµ СЂРµРєРІРёР·РёС‚РѕРІ / NFРЎ-РєР°СЂС‚С‹ / SberPay / РџР»Р°С‚Рё QR / РџР»Р°С‚РµР¶РЅРѕРіРѕ СЃС‡РµС‚Р°.
topics: ['РћС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР° (Р�СЃРїРѕР»РЅРёС‚РµР»СЏ) Р·Р° СЃРїРѕСЂС‹ РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј (Р—Р°РєР°Р·С‡РёРєРѕРј) Рё РџРѕРєСѓРїР°С‚РµР»РµРј (РљР»РёРµРЅС‚ Р—Р°РєР°Р·С‡РёРєР°)']

=== IDX 139: 7.9 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєРё РїРµСЂРµРІРѕРґР° РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РµСЃР»Рё Р·Р°РґРµСЂР¶РєРё РїСЂРѕРёР·РѕС€Р»Рё РЅРµ РїРѕ РІРёРЅРµ Р‘Р°РЅРєР°.
topics: ['Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё Р·Р°РґРµСЂР¶РєР°С… РїРµСЂРµРІРѕРґРѕРІ Р±РµР· СЃРІРѕРµР№ РІРёРЅС‹']

=== IDX 140: 7.10 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°, РѕР±СѓСЃР»РѕРІР»РµРЅРЅРѕРµ РґРµР№СЃС‚РІРёСЏРјРё РёР»Рё Р±РµР·РґРµР№СЃС‚РІРёСЏРјРё С‚СЂРµС‚СЊРёС… Р»РёС†, РІ С‚РѕРј С‡РёСЃР»Рµ СѓС‡Р°СЃС‚РЅРёРєР°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹
topics: ['Р‘Р°РЅРє РЅРµ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РІ СЃРІСЏР·Рё СЃ РґРµР№СЃС‚РІРёРµРј Рё Р±РµР·РґРµР№СЃС‚РІРёРµРј С‚СЂРµС‚СЊРёС… Р»РёС†']

=== IDX 141: 7.11 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСѓРјРј РћРїРµСЂР°С†РёР№ РїРѕ РїСЂРёС‡РёРЅРµ РїСЂРѕРІРµРґРµРЅРёСЏ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ Р‘Р°РЅРєРѕРј РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РїСЂРѕРІРµРґРµРЅРёРµ РћРїРµСЂР°С†РёРё СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°
topics: ['Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ РІ СЃР»СѓС‡Р°Рµ РёРЅРёС†РёРёСЂРѕРІР°РЅРёСЏ РёРј СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ РѕРїРµСЂР°С†РёР№']

=== IDX 142: 7.12 ===
required_type: optional
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РІ СЃР»СѓС‡Р°Рµ РїСЂРµРІС‹С€РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°
topics: ['РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р±Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё РїСЂРµРІС‹С€РµРЅРёРё Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°']

=== IDX 143: 7.13 ===
required_type: mandatory
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№, СЃРѕРІРµСЂС€РµРЅРЅС‹С… РЅР° Р РµСЃСѓСЂСЃРµ, РІ СЃР»СѓС‡Р°Рµ РЅРµРІС‹РїРѕР»РЅРµРЅРёСЏ Рї. 4.2.21.1 Р”РѕРіРѕРІРѕСЂР°
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅС‹Рµ РѕРїРµСЂР°С†РёРё РЅР° Р РµСЃСѓСЂСЃРµ']

=== IDX 144: 7.14 ===
required_type: mandatory
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
main_idea: 
enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјС‹Рµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў РІ РЎРџР­Рџ
topics: ['РћР±С‰РµРµ СѓС‚РІРµСЂР¶РґРµРЅРёРµ Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ РІ РЎРџР­Рџ']


[Command succeeded with exit code 0]
AI: The text is still garbled. The issue is with the console encoding. Let me read the matrix items directly from the JSON file using the read_file tool, which handles encoding properly.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 970, 'limit': 200}, 'id': 'call_00_TdjF55CC68CgcKfq6OEy0018', 'type': 'tool_call'}]
Tool:    971	  "main_idea":"",
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
AI: Good, now I can read the matrix properly. Let me now find the exact location of items 97-144 in the matrix file. Let me use a more targeted approach.[{'name': 'write_file', 'args': {'content': 'import json\n\nwith open(\'inputs/matrix.json\', encoding=\'utf-8\') as f:\n    m = json.load(f)\n\n# Find line numbers for indices 97-144\nfor i in range(97, 145):\n    it = m[i]\n    print(f\'IDX {i}: {it["number"]} | req={it["required_type"]} | prod={it["only_for_product"]} | lot={it["only_for_lot"]} | term={it["only_for_terminal"]} | pm={it["payment_method"]}\')\n', 'file_path': '/outputs/working/batch3_ids.py'}, 'id': 'call_00_w7qAquaYWNXq3y4cNKrK1198', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/batch3_ids.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/batch3_ids.py'}, 'id': 'call_00_6FTQMPDFJaz8Rs0gpXMq5931', 'type': 'tool_call'}]
Tool: IDX 97: 5.1.16 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 98: 5.1.17.1 | req=optional | prod=trade_acquiring | lot=common | term=pos | pm=common
IDX 99: 5.1.17.2 | req=optional | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 100: 5.2.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
IDX 101: 5.2.2 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
IDX 102: 5.2.3 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common
IDX 103: 5.2.4 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 104: 5.2.5 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 105: 5.2.6 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common
IDX 106: 5.2.7 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 107: 5.2.8 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 108: 5.2.9 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr
IDX 109: 5.2.10 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 110: 5.2.12 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=qr
IDX 111: 6.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 112: 6.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 113: 6.3 | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common
IDX 114: 6.4 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 115: 6.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 116: 6.6 | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common
IDX 117: 6.7 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 118: 6.8 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 119: 6.9 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
IDX 120: 6.10 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 121: 6.11 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 122: 6.12 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
IDX 123: 6.13 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 124: 6.14 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 125: 6.15 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
IDX 126: 6.16 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 127: 6.17 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common
IDX 128: 6.18 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common
IDX 129: 6.20 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 130: 6.21 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 131: 7.1 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 132: 7.2 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 133: 7.3 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 134: 7.4 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 135: 7.5 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 136: 7.6 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 137: 7.7 | req=mandatory | prod=common | lot=common | term=common | pm=common
IDX 138: 7.8 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 139: 7.9 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 140: 7.10 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 141: 7.11 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 142: 7.12 | req=optional | prod=common | lot=common | term=common | pm=common
IDX 143: 7.13 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common
IDX 144: 7.14 | req=mandatory | prod=common | lot=common | term=common | pm=common

[Command succeeded with exit code 0]

