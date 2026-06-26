## Summarized at 2026-06-26T14:22:21.008967+00:00

Human: Matrix batch 2: section 4
AI: I'll start by reading the skill file and understanding the task structure, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_cZ7j4yCFktECipw7qr9p2519', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/*', 'path': '/'}, 'id': 'call_01_WIYMMbDkMGKBaxeDtEXB6294', 'type': 'tool_call'}]
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
Tool: ['/.env', '/.git/COMMIT_EDITMSG', '/.git/FETCH_HEAD', '/.git/HEAD', '/.git/ORIG_HEAD', '/.git/config', '/.git/description', '/.git/hooks/applypatch-msg.sample', '/.git/hooks/commit-msg.sample', '/.git/hooks/fsmonitor-watchman.sample', '/.git/hooks/post-update.sample', '/.git/hooks/pre-applypatch.sample', '/.git/hooks/pre-commit.sample', '/.git/hooks/pre-merge-commit.sample', '/.git/hooks/pre-push.sample', '/.git/hooks/pre-rebase.sample', '/.git/hooks/pre-receive.sample', '/.git/hooks/prepare-commit-msg.sample', '/.git/hooks/push-to-checkout.sample', '/.git/hooks/sendemail-validate.sample', '/.git/hooks/update.sample', '/.git/index', '/.git/info/exclude', '/.git/info/refs', '/.git/logs/HEAD', '/.git/logs/refs/heads/20_min_80', '/.git/logs/refs/heads/claude_skil', '/.git/logs/refs/heads/clear-branch', '/.git/logs/refs/heads/codex/clear_one_skill', '/.git/logs/refs/heads/demo', '/.git/logs/refs/heads/main', '/.git/logs/refs/heads/one_skill', '/.git/logs/refs/heads/pre=agent', '/.git/logs/refs/heads/test', '/.git/logs/refs/heads/test2', '/.git/logs/refs/heads/test3', '/.git/logs/refs/remotes/origin/20_min_80', '/.git/logs/refs/remotes/origin/HEAD', '/.git/logs/refs/remotes/origin/claude_skil', '/.git/logs/refs/remotes/origin/clear-branch', '/.git/logs/refs/remotes/origin/demo', '/.git/logs/refs/remotes/origin/main', '/.git/logs/refs/remotes/origin/one_skill', '/.git/logs/refs/remotes/origin/pre=agent', '/.git/logs/refs/remotes/origin/test', '/.git/logs/refs/remotes/origin/test2', '/.git/logs/refs/remotes/origin/test3', '/.git/lost-found/commit/a9784911cc1c5b5eab6643175e5ec45caf25eee4', '/.git/lost-found/other/00025daef50b48b9a7c3aa0957f67692b7cf9644', '/.git/lost-found/other/00279ba916b80ee7f054dcfe4bcad5fdf3d0cad4', '/.git/lost-found/other/003f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/lost-found/other/0052dd8f0d35e7d44cabe09971d6e0f21ca39cd2', '/.git/lost-found/other/009107e59a300c960ee6ec2a0fd55630b53e6a77', '/.git/lost-found/other/00bf2ee6092a4428c1c240774794e6c695ff4722', '/.git/lost-found/other/0108acc654101c39e74de3cb6404c4fa80bc7bad', '/.git/lost-found/other/011eb16c1ca5cd43dfe08ae67835808b35c8afe0', '/.git/lost-found/other/015abae91e08022c92cb6c24e1e1097ec60a9c6b', '/.git/lost-found/other/016411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/lost-found/other/01686fb3f6afa2208defd34a9188169a7884eccf', '/.git/lost-found/other/0189548f4f27fcb26840150f585a64515d77c26d', '/.git/lost-found/other/01a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/lost-found/other/024da679e39764f8e2a1862074bc7d3a67b39a2e', '/.git/lost-found/other/02500954f54d824bf47a0c40e7249570c8ae35a6', '/.git/lost-found/other/027cd9077d41da5280567175993abb09c6e81add', '/.git/lost-found/other/02955e2401b4f817cc67ef6094697af860f2d18e', '/.git/lost-found/other/02b7b9d7d9324409084e9f2b00eae11901589864', '/.git/lost-found/other/02e3706e34f211187bd64efa7a9ad51760195d39', '/.git/lost-found/other/02e5c435ffbd7357cd76f7c19bf5f4451ea88c3d', '/.git/lost-found/other/02e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/lost-found/other/0312d61983ef80179bfac79abbba1359052f115c', '/.git/lost-found/other/03732f0c6e6eeaef66eda4e4a6de308b7e7e1e95', '/.git/lost-found/other/03ff6a156c8ba598cf1be27fb2371810888a927a', '/.git/lost-found/other/040be927181b9604d69593ffe36ab7303b1a94bc', '/.git/lost-found/other/042e02d97cc4abc6a96b55d97f34fc76924c9cf9', '/.git/lost-found/other/04378a998f4a8686eb28f62e8833b0f539229714', '/.git/lost-found/other/043f51145222bf3b3e811ab6d29c229b25b3b1d3', '/.git/lost-found/other/044e235175ddef6dd6b9a05edbd34b9ab69cbbd3', '/.git/lost-found/other/04602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/lost-found/other/0478eb80cc9a8041214bf273295064af3ab7f7d7', '/.git/lost-found/other/048703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/lost-found/other/0488481d528674a76807703e6625d6284ca8293e', '/.git/lost-found/other/0489842c6d2c5ddbc9550902039e9b25701d08db', '/.git/lost-found/other/04ba7faa5aee31cca7feb4058574f06ec3a9b645', '/.git/lost-found/other/04bf8e699f88900a6960b666079dba19a77ee7eb', '/.git/lost-found/other/04d51f0de077d3b810718bfa2ca6ac4f3567c07f', '/.git/lost-found/other/04d557d3b8c74f15dc8b1039d196b50cb8924950', '/.git/lost-found/other/04eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/lost-found/other/0504a514448e0c3c3e4f771ffc84479295824920', '/.git/lost-found/other/0558ff9439de64e491ee9c3bd2097b5b118029b6', '/.git/lost-found/other/055ecd0695e622dcadcedc29409753f35d106433', '/.git/lost-found/other/057e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/lost-found/other/05c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/lost-found/other/05e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/lost-found/other/0617f381a59a452478a8f34cabb652beadf361cd', '/.git/lost-found/other/061c9d02a136ba7adc607ed7074cd148595a2030', '/.git/lost-found/other/0631461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/lost-found/other/06418747a855c7847e27bfe23508610c20a60493', '/.git/lost-found/other/064efa3154548faf37f72f6e16da0f94681fa86a', '/.git/lost-found/other/06a8e8ac333fed73af47212fe4626cbaa3b74e82', '/.git/lost-found/other/074930d053a799cc4f9095e89196437f704205d6', '/.git/lost-found/other/07682e77b603150eac6f657df236ac3dced0586d', '/.git/lost-found/other/077efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/lost-found/other/0791e2c492831faaf144a90e6af25adaabad38fa', '/.git/lost-found/other/07d0f29a2d244a75911191faf176cc0c7edf4bda', '/.git/lost-found/other/07d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/lost-found/other/080554e8ddc2a1a87275a26e5457e1b2a6046657', '/.git/lost-found/other/08080c1aef87cedbe163497ddad8cc3005a73f7d', '/.git/lost-found/other/080d85bb922b72b159fc03f3f1a84d23a9d2568c', '/.git/lost-found/other/082169d84ac7751152d7134fa37292c00ba029d0', '/.git/lost-found/other/08377760400a919e539db754b0b66ea7ce0cef58', '/.git/lost-found/other/0842d15769f312e00dbce38c79a209d783d115ea', '/.git/lost-found/other/0846bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/lost-found/other/08749be2799a1a1f0697ed2571a4682426ea12ff', '/.git/lost-found/other/088409712f5c920b0dbf4a4c818e977f34f91873', '/.git/lost-found/other/08ba0a8ee50af5b8ff5eb0a82d30bb5229fe2e86', '/.git/lost-found/other/08feb11d7a524e0e04e556a3b0fac0a6a7b24657', '/.git/lost-found/other/0937353c8f0a794e6ea7d64c5904fa44ffbc61aa', '/.git/lost-found/other/093d21dba99b105a0e82051ab2639b5151325793', '/.git/lost-found/other/0946862f3f15d72c8b71d2af4522b4921f6cab96', '/.git/lost-found/other/094e04d13c87f5a327a7f44ffedc0ce41d9214d0', '/.git/lost-found/other/098b34de8f71069fae9082ecd1903b6faedce4e6', '/.git/lost-found/other/09916958db8eaa97c465c9bec51a3d1a29863ab8', '/.git/lost-found/other/0a05a2808a79fe98d007bccb3b1060551300dec8', '/.git/lost-found/other/0a32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/lost-found/other/0a401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/lost-found/other/0a56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/lost-found/other/0a597e37cfb13fe9af1875fc0606d2f7cc0e7ada', '/.git/lost-found/other/0a962ce910aa746587b34755922bae542449fba9', '/.git/lost-found/other/0abc810e4c97279e80fa5610d8d2838b94e3bb03', '/.git/lost-found/other/0ae25708036bf7db64f0327ea004917ad42ea679', '/.git/lost-found/other/0b32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/lost-found/other/0b5d3ac18d6fbd99afb581479554b58fc4183e02', '/.git/lost-found/other/0b5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/lost-found/other/0b9c1ff14d0729b8ca054bf3b70a31ed6ea3724f', '/.git/lost-found/other/0baa622887f5563517e122f9b16213710af9e5cb', '/.git/lost-found/other/0bbcef51f80d0155f83a276423028a01a50cd92e', '/.git/lost-found/other/0bbe894f6158df6217aac34e5062d723091507dd', '/.git/lost-found/other/0bc5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/lost-found/other/0bebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/lost-found/other/0bf720f21f41ce829add4aab5a9a05012208c3f7', '/.git/lost-found/other/0c00cb9ca737f2be5b9cff166bcef532262ec699', '/.git/lost-found/other/0c4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/lost-found/other/0c55eb9a5a6f0f2c00a7d6a578505a35c3c881f8', '/.git/lost-found/other/0c614b8e0f3afd25e895d9491c2a30e5913af606', '/.git/lost-found/other/0c64a4d48bda41945b4888b51a9e960d8fbfcf0f', '/.git/lost-found/other/0cd26a469771b69762f53b5ae2a322bf170091d1', '/.git/lost-found/other/0ce0b926ac0c36b6e353c377ebc74e59bc0561c0', '/.git/lost-found/other/0d2b4e5c9def6a898a4064dd6adf23d978807b49', '/.git/lost-found/other/0d3b08adf9c7ed270b6d5889540ad4437d5f0b98', '/.git/lost-found/other/0d72d0b2349a404cc4cddb87c836194765377d74', '/.git/lost-found/other/0d753acfba917272cd72f418e9c1352ed20054f6', '/.git/lost-found/other/0d8780f3e4c97dc70ba82cc61c5cef46d57b0b33', '/.git/lost-found/other/0dbcae139c196ceada45a4720daaf5908702ecc7', '/.git/lost-found/other/0e189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/lost-found/other/0e31d5d75617658d5871f0af7cd6e2572f65d5a7', '/.git/lost-found/other/0e33d9681c3f231054d16d613b34097e7e8b59e7', '/.git/lost-found/other/0eb37de8ca5ba7a34797b3355f41cf01b22ff008', '/.git/lost-found/other/0ebe1fc27f8d238046aea951e6caa693563a5db1', '/.git/lost-found/other/0eddffee3cce42079be92d29e9858c7f31c0a906', '/.git/lost-found/other/0ef556b4beacab982c37a6ba626b68c12a03a3ae', '/.git/lost-found/other/0f0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/lost-found/other/0f138f0796a06e405b352d9b196d634fe03272bd', '/.git/lost-found/other/0f3f373dbe68457e2f332b53419313c5297f50fa', '/.git/lost-found/other/0f573afb56cf5cd6dd86621f5e5c4d7eeff7c726', '/.git/lost-found/other/0f5968785d1283804001ca49ccf77d63eac98e02', '/.git/lost-found/other/0f86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/lost-found/other/0f9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/lost-found/other/0febdd5aed4ccb535776cb3ecf5f7292598d83cf', '/.git/lost-found/other/1018a2334d5c1968f40c2f478fb1f2867e67b8b5', '/.git/lost-found/other/1064453d1e30d78cd388f816b907f7b742375e31', '/.git/lost-found/other/108486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/lost-found/other/108d20d49b8c9df755feb7040b27dd500650d6f1', '/.git/lost-found/other/1152abac92eac8d8b605f61e7608e5151d222f07', '/.git/lost-found/other/1168066a747c3bef2d6e633b2347c20cc6b56404', '/.git/lost-found/other/116968b47e00996915b67531127f0954c7ddd1a4', '/.git/lost-found/other/1195185617fa4e3585174859ed5709d013f5937a', '/.git/lost-found/other/11b6a93338766923a8e6379405e6fcf4ab828169', '/.git/lost-found/other/11c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/lost-found/other/11e01dd8395bcb4499bbae87a8fa5d396b5bb9a0', '/.git/lost-found/other/11f3df8ac49a0be182d46132407e50090bc85a7e', '/.git/lost-found/other/1260fee99a4cfcbd9d4ffb0eb2de091a7a472b7b', '/.git/lost-found/other/12782408d18b12ea7c1fd9e5d39ddbfa2040ef21', '/.git/lost-found/other/128150674170b66350257cc719da038a61a568bf', '/.git/lost-found/other/12d12afbdb51a82ea91470a68c5936ef307758b3', '/.git/lost-found/other/12ecf89d4939f447a2a13eb6a8584268d822df06', '/.git/lost-found/other/132ce036f2fe47610a5925b048748ef75eb541db', '/.git/lost-found/other/13360394a41c8fabc39419ab404191a8575e2799', '/.git/lost-found/other/133c2a7f8f0c8e8798adb0c95502b796e8304aa0', '/.git/lost-found/other/1392a68ba7c0702c66b4fb266ffd087081b1e141', '/.git/lost-found/other/13c40173739fb7e84b979f3c6ac5261cec02e012', '/.git/lost-found/other/13dd0ea3ac7cf3fa815ff54ed379ac145c2200aa', '/.git/lost-found/other/13fb8a33b9d96c2a9ff445c20dea718e895df5e4', '/.git/lost-found/other/143334e584ff71080c606f29c1ef42924bbe453d', '/.git/lost-found/other/14394b47e18f572003e3d82368702dfd474b70c4', '/.git/lost-found/other/143df4c79cc8ee0249f8509549e5377882a28010', '/.git/lost-found/other/1474c8f7cf8bc22cda503322795cac94ac621675', '/.git/lost-found/other/148a5ec5787afd3f553071ecc831a805312f6ece', '/.git/lost-found/other/148c20fa8c56ae81068aded6b9a8f2a59fc229dd', '/.git/lost-found/other/149a72f18b0f5ac8ed9bf713a2c26c76d8158588', '/.git/lost-found/other/14fe9bb6670802ae36d1022630b687088b71c35d', '/.git/lost-found/other/15098da0ba5b0e2d399d8688a8a0b6a0fcd68d1d', '/.git/lost-found/other/155f8df967724158d80873e629c6c12bb65c8d00', '/.git/lost-found/other/159a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/lost-found/other/159bfd26b659195df8c8486d12b5e15f948cb808', '/.git/lost-found/other/15be2e474eb938a89e4d7c19737994893197e781', '/.git/lost-found/other/15fc480833c1c814d413e14a2421b5ffed74028f', '/.git/lost-found/other/15fd3d807851be39f668587b875d1bd9356e1171', '/.git/lost-found/other/163d050dd4db671d29be7efff1a35864f91ca61d', '/.git/lost-found/other/1645e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/lost-found/other/164b7fafb2c4bcbb6315f95870ae3efbf8a82241', '/.git/lost-found/other/165d22d6f5554de58d1281ade7295158d4e62312', '/.git/lost-found/other/167230ee6e97a40999b7b1b46b089e48951a1158', '/.git/lost-found/other/1683c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/lost-found/other/16a2cab9c4e32851d2754116ca26b4ead49cd1a3', '/.git/lost-found/other/16bc644bbb95c0d296bea492b5595b361a93b9fa', '/.git/lost-found/other/16d466f5d6f6422fc565801d9d97c0bd71bf6a5a', '/.git/lost-found/other/16de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/lost-found/other/171b3e26763b46f7034313a38879dcb5e511f770', '/.git/lost-found/other/177a3761fec84c8776563bc7d9edcd67544feca6', '/.git/lost-found/other/17875ecd8901fa5f6f1ffd63a3f4ac41cd695e3e', '/.git/lost-found/other/179165971d58c6643a8bf303e8bf53e64a143ed8', '/.git/lost-found/other/17a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/lost-found/other/17c6782b615441baeb457ee93a458ed7371c9f99', '/.git/lost-found/other/1805f56abd31c9fa832a4d2e4d2a6525282bd60f', '/.git/lost-found/other/180e3f7a759491581027a4970076148d69b10348', '/.git/lost-found/other/185c9bede1c02917cd4743d154dc42b2cd03cb25', '/.git/lost-found/other/1862eec0af25e420dee69a16ba235f610f20756d', '/.git/lost-found/other/1876a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/lost-found/other/1888c3e87775cf3cfca934be2e7ec03a6696f1da', '/.git/lost-found/other/18d512a4ebe9f93cc357a19059984b3398799bee', '/.git/lost-found/other/18fe30c098f75b96caa54450040279f8727780ea', '/.git/lost-found/other/1929b4d821dbc5d88f2c4c6d8839d0fedf3fa95f', '/.git/lost-found/other/19704e0cd5db5fec06dd7c57009e47296c0c4411', '/.git/lost-found/other/19928324ad53403e47456f49785dd300a6abc1e0', '/.git/lost-found/other/1994bb1252910ca25e7dd1c7eaee69a59f99d597', '/.git/lost-found/other/19bc9e08c030c0958b8cfcb118ef4e6a076e1bfe', '/.git/lost-found/other/19d15ee65c1ad2342c69a499567a3d8e33d985d2', '/.git/lost-found/other/19ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/lost-found/other/19eac84456408b48017f9b8f7012a31d357f9ded', '/.git/lost-found/other/19ef249a5908e6c6f084c18763897a644a28241b', '/.git/lost-found/other/1a04525ea6855d36a41a4720d225e21887989682', '/.git/lost-found/other/1a3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/lost-found/other/1a412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/lost-found/other/1a7b119a11b008be1ded0bd9ca1ddfad0e5a5260', '/.git/lost-found/other/1a955782d22785e3c692639e34ac42ecd1ad95be', '/.git/lost-found/other/1ae3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/lost-found/other/1afcc87003afe09c0245ee2e2f90a48f107eea91', '/.git/lost-found/other/1afe522d67bb11ef6df1ef598c4a6077cbdbf43f', '/.git/lost-found/other/1b2651a7254d50dd505d130cb119b1e0f63b274d', '/.git/lost-found/other/1b297017feb7427e872083cfba46fdd2d1f5d1f1', '/.git/lost-found/other/1bb304e8afd560b9be58336068f17f0f453cd33d', '/.git/lost-found/other/1bb6184cbc8ec7b0b92597da642ddb7baea3f9f0', '/.git/lost-found/other/1bb94dc37fa7ba202e37fb9f730b2c1ffe60c9f8', '/.git/lost-found/other/1bd62bc3162bcc0924c6b11dcc91aea034a50dda', '/.git/lost-found/other/1bd948006afad9d92ba0af0d9d6aac84b81201ee', '/.git/lost-found/other/1be15396b1a24634af2755f0315d590d8f5efb56', '/.git/lost-found/other/1c3b26b30ba44895a4b99ed6b8361e4fe8d6e96e', '/.git/lost-found/other/1c5c64af7a4a179928feb3e438ba9aeca2b21785', '/.git/lost-found/other/1c6f0d2fcead6d6b9af167efe84b68ab9867253d', '/.git/lost-found/other/1c8f3931f4569a257832b968b4b4e0122f827992', '/.git/lost-found/other/1cb460853dbc76ecd603937b1385d60dfe4544da', '/.git/lost-found/other/1cc87e753d217d64955f9f7594e5c51e9515e117', '/.git/lost-found/other/1cc883a61f30b9ef594ac9e9119fba4fb6e6b38a', '/.git/lost-found/other/1cd48831e92cfedee75b4f2bd298004c09a02e41', '/.git/lost-found/other/1ce139b0630235d7cccd5e7233e06fb27e4b7e92', '/.git/lost-found/other/1d116b842cd0f57b27060be476644b86e101adbc', '/.git/lost-found/other/1d486741fb9e843d4c02664be20ce398200e3031', '/.git/lost-found/other/1d62dd77221b120231127e20a3d046857e9e43d4', '/.git/lost-found/other/1d80ca727f627adf666f395a0c85e26662ed0d20', '/.git/lost-found/other/1dd3c6fbd22c1169a906849b6be2a41c24aa2fd9', '/.git/lost-found/other/1de732b38d658fd3ce936527e47cac6259f9592a', '/.git/lost-found/other/1dfc607d1dcba5edcbf0de542ba2777324f237ac', '/.git/lost-found/other/1e350fcaa9e1ea22a0fa61a8b01f206f7ac9dd0a', '/.git/lost-found/other/1e5a8be244c1322fa76b77784e582f480009958d', '/.git/lost-found/other/1e73f11f4d9826d98dd02d4b053bf4f4f144542d', '/.git/lost-found/other/1ed6e6a5f1c7d86cbcffec476f2d43c3a3b164cc', '/.git/lost-found/other/1f604bc809b0d41096d17b0050c153e858717c6c', '/.git/lost-found/other/1f70a2d4551510dfb5fdd95b27b6bf486639e5ef', '/.git/lost-found/other/1f9bc9625cc3b8c37c1c971597ee9e3158f57f4e', '/.git/lost-found/other/1fb978ebe70aba71b3e2d74d673c0459d8480ac6', '/.git/lost-found/other/1fe3e3bfa8d6df8f7d0aae939c931eb1d654bd6b', '/.git/lost-found/other/1ffa5ed33b6108ed57142c1be928988a7761b6dd', '/.git/lost-found/other/201c519c93b3b77bbe0555abc3e68c9a0d24c28b', '/.git/lost-found/other/2077ea20e01da4d37e629d77f92bd01657842631', '/.git/lost-found/other/2083461eff88321aa0feceaab497bc202e7d110e', '/.git/lost-found/other/20a95d03ea8998b75a0379c47b79d67138d097ba', '/.git/lost-found/other/20d6d5fa6f6982c1d4d8d927ae5e9e121fe42018', '/.git/lost-found/other/20edff68991fb4c628d2281dddb40df64282d6e1', '/.git/lost-found/other/20f6f17a1e15763482af8451d3da4498642ba0fb', '/.git/lost-found/other/2125a26d3c69f2df90b281937dc82deb6c57cb20', '/.git/lost-found/other/21637826d1d04950f4a4d796a9571a8c4d86b806', '/.git/lost-found/other/2187ac3ff0237618615d7b487a0d1a6403ef49d2', '/.git/lost-found/other/21b0396817724695b99c77d49474607c4516b8f1', '/.git/lost-found/other/21c099aa1a03294014130368b917b2c6eef94753', '/.git/lost-found/other/21c428f3247ee9fb40e38b78c925eea08e7175aa', '/.git/lost-found/other/21d13a0a40c505324dab511aa407e5dc471bcf1c', '/.git/lost-found/other/21dc7c101abb0ba003e36a25d3686c48c4182328', '/.git/lost-found/other/21eea7a19ea8fa9c7d004bc61a994b42b88b8ac8', '/.git/lost-found/other/21f7a4f54ed4863b3ff2ff03747f55590badc90e', '/.git/lost-found/other/221fbbc53f621f91a6220c85cd506af3f790086e', '/.git/lost-found/other/226a93510d33d1c407aef258f9c39f42e3f298ad', '/.git/lost-found/other/227c0e6634ea1ea9f9c9e1068c1c55f53917c14a', '/.git/lost-found/other/228c08f34331c47620b55794c64c0ff9897f15c0', '/.git/lost-found/other/22b435aac92e50eca2ee89fc748441e81cfcd88d', '/.git/lost-found/other/22baf3300cc31a3540ca4314fd8c58bcb7018353', '/.git/lost-found/other/22e7afb00fe5b7c7602b761800024ed40d25fe21', '/.git/lost-found/other/230d67a0590a4d61346d6dd5ced3f53dd0f1bea2', '/.git/lost-found/other/2339b673bf04246da4977d2a1c82e1f447ea3544', '/.git/lost-found/other/2354041ddba6abd34193e615b4cf804c6e2fd520', '/.git/lost-found/other/2358432f1d03d54e5ede647bf656376dae10e349', '/.git/lost-found/other/237e83f06ebd406dcc11507e0cf8c3be65e684d3', '/.git/lost-found/other/238faa3816f1afd26933d98bd81001eb92a2c876', '/.git/lost-found/other/23b597c126b6815d23f022bce47ef1f8815c532b', '/.git/lost-found/other/241dfb0157cfff0271813dfb80667be5a95deb89', '/.git/lost-found/other/242b028657099781ee5f230d30afc0a8af8423df', '/.git/lost-found/other/245ed230dee59261acbdfe117c3db0280411df76', '/.git/lost-found/other/247b2894f7b921a2585eed175a225fa8e7dee8bd', '/.git/lost-found/other/248a3917f8467ac0cc6218d4b046e8e4b2cba851', '/.git/lost-found/other/248fd8353332111067158f2d11e7087f1ac3fe69', '/.git/lost-found/other/24ec11aadf71bebef0b0658c378b43788974a6c2', '/.git/lost-found/other/24ed3535539a46584ebcd6609d0ecdf3a0f86ddc', '/.git/lost-found/other/250d15ac2ac893edafa629b15e07ede0747d8e78', '/.git/lost-found/other/2516e2d96db3ff349b2fec7f85e9958f93292621', '/.git/lost-found/other/25240eaa758f5a58e2ece8cd89c1ad44a88971ec', '/.git/lost-found/other/2533d1949584c2a0a3b143a5cb4de3f8c1d17758', '/.git/lost-found/other/25393416d634a457748f6167634a4d86955a9774', '/.git/lost-found/other/253f5f1950cdce8f3dd7dca88b26bfcfcb68ad9e', '/.git/lost-found/other/25908607dbe19286a4b0f7b6927619cec2531bf0', '/.git/lost-found/other/25e89d80677a94a06bfb564749370a97050e61ab', '/.git/lost-found/other/25e9c1f9b50b6f8773736712f54f64d323d415f9', '/.git/lost-found/other/261067ca7aa2c677fcce286ae23ffb3e3e3c4b68', '/.git/lost-found/other/26194e93e2a767b3f44b2bb12906aad486311c49', '/.git/lost-found/other/26204973c5913550889f7735c6c91e3f23eb971d', '/.git/lost-found/other/2663b05e98e130e359c6f704963f2e68068a829c', '/.git/lost-found/other/2667e6553b593b2789c084f20b09c8e100fec7e6', '/.git/lost-found/other/2676a4fb754239d1306066ad2d8f58004874245b', '/.git/lost-found/other/268340e1ad4d5df681a7c90f17f4dc772b726e70', '/.git/lost-found/other/268f3c416fe521d519da01323f305123fa54f3aa', '/.git/lost-found/other/26bc257b7c543df579db1afcb9248ced695a5433', '/.git/lost-found/other/26ee19281818f2ab393398d7cdfab1cc1a73aa44', '/.git/lost-found/other/270866455342b36d58ba2ee755f781bbdb564dc4', '/.git/lost-found/other/27cefe5d09eccdf969bbe7c4bd03ba88866dbdd5', '/.git/lost-found/other/27cf296e191cf1e3f150c9cfc6dbb191d17554f6', '/.git/lost-found/other/27e9ed80c1396df06710f8c7782e989d2230e035', '/.git/lost-found/other/289dbec76c204f3703abb10c34cdad5888f18f05', '/.git/lost-found/other/28c2c11c8dfff1aa3fa7b6add9019a0af59a46fc', '/.git/lost-found/other/29017f09af575575dc32524be2294103c1bab658', '/.git/lost-found/other/2912b2774fce14827260d4c8ec3a58acaebd30aa', '/.git/lost-found/other/292fc6f6555ddd8ee1d1baf819d59b7704bd34b9', '/.git/lost-found/other/29b9a8951ad9517c1953a163da020fe28852bba9', '/.git/lost-found/other/29f91579b798fbdf2436d2f21c966d128bba04fd', '/.git/lost-found/other/2a3288a1f6616175a2448df2069d345263d3ceab', '/.git/lost-found/other/2a92a9d4eaa55a8e8264ef2a4ec0a1712f8d8bf7', '/.git/lost-found/other/2aa35d99f6a8fdbe078c97cbf1990f66ca61c0cb', '/.git/lost-found/other/2ac0ccfefd5c151ca5de3ddf23b9bddfc1c8cf4e', '/.git/lost-found/other/2afee31d90e375b801139b051605dc6f5599d9f1', '/.git/lost-found/other/2b1c9b3d9439d122a26ecb89328b50c78ea7dbeb', '/.git/lost-found/other/2b1e035dd765108817ac13695374505ff9a7d9d4', '/.git/lost-found/other/2b33a12233bf94d423b84df484fbd4936841f0ff', '/.git/lost-found/other/2b77f7188e91b5f41905b979e1453716042a88d6', '/.git/lost-found/other/2b84077d254fc2a1d66d0b4ea82ef3a7fa125c3a', '/.git/lost-found/other/2ba1ae4723622dd7a36a624626a298bc4aede590', '/.git/lost-found/other/2baa9b4b0fd3a53e07dbaa15098f4c45e7419cd6', '/.git/lost-found/other/2be2042f9a6e321e9ae96e9becee05d609390c6b', '/.git/lost-found/other/2bf2efefce1765ad78030310ed9900afb0cd5522', '/.git/lost-found/other/2bf5bb558ff589653f528af8bedb778c46df101d', '/.git/lost-found/other/2c24c73a4a5af1d5a5ec1c117c520c7056ea55b1', '/.git/lost-found/other/2c39548b92ad9ddcc9c291ce39e44ed6c6b6cf3e', '/.git/lost-found/other/2c4e1eb30367408711d432986d0b075531aa3a92', '/.git/lost-found/other/2c59ee393814f03d894d5d8c75ab7512af596f2b', '/.git/lost-found/other/2c8ab9af72c1dcf6d59f4a77eb53ad7631241c8c', '/.git/lost-found/other/2c8bd2401a11ab4f8b5e2313cc59bab1b11cd988', '/.git/lost-found/other/2ca2261abaa3459cab2e6b5aac65911448fb906a', '/.git/lost-found/other/2cab5b28db8404259e58a97c72d97538899d23ef', '/.git/lost-found/other/2d201015b65cbcd6a4fe0082bf6d4a65076dc4e1', '/.git/lost-found/other/2d209cca9eecd6d9519f21ae66f180d2001554ef', '/.git/lost-found/other/2d3f8b0777fb0252760bfa45abbb7726b967cc4b', '/.git/lost-found/other/2d5822675d64a208d26431a0cb3bd4a9ee1ad7e1', '/.git/lost-found/other/2d808e55af2eb9b6c496d06a8de71c32578f172a', '/.git/lost-found/other/2d926e4fa759b1b3235635ba6668898a635443f9', '/.git/lost-found/other/2d98f0a835a91e49cb26869dc16dea0583feafbe', '/.git/lost-found/other/2dad60a817385f78660e338a688f9699f3790810', '/.git/lost-found/other/2dfb63554d59caccc63b4addb234c135c283d1f4', '/.git/lost-found/other/2e00a61f618f743393ca83058702b25b950de8ba', '/.git/lost-found/other/2e107635a41522a90f0ea3c1f8fbbb3ff8685f1f', '/.git/lost-found/other/2e395785e7e850594fe6874f052e55a0733d4549', '/.git/lost-found/other/2e91b71a0e65135085d8a12d86bbfd6658dd36de', '/.git/lost-found/other/2eb6a12922b18a340dcf58a23feb13e0e2b1f88b', '/.git/lost-found/other/2f14cb77a3fe840c167ec7c363ba895d3a809b68', '/.git/lost-found/other/2f29d9394aab14b49d63b7303c6549458f4f7158', '/.git/lost-found/other/2f785e870024de3ac7ca3a834b25ca25e9d9cb8e', '/.git/lost-found/other/2f7887c4fbfd68a3721f5d2cdc896c48bf353c5a', '/.git/lost-found/other/2f807662ed402a67cdc3a86d525264af5ff4fb7d', '/.git/lost-found/other/2fb9df715c3a1ff4dbeed9b729ca8722ebabe729', '/.git/lost-found/other/2fe7004545a2ce0c6214b6c75bcad75dbec8f434', '/.git/lost-found/other/2fff44f43f90bd8988761555f56630209e29f777', '/.git/lost-found/other/302b17514cd5a0c86a73900453a45021c8a6c77f', '/.git/lost-found/other/3040605d4918eca0701e2a541826d735e153871a', '/.git/lost-found/other/306a8becbe8f0d8eab7964b3986c9f94ff283e20', '/.git/lost-found/other/306e5950b0fcee534e38083a1536591ce18ed5e8', '/.git/lost-found/other/30ab4115f80c0bf921117640ff7c490947ad6202', '/.git/lost-found/other/30fcd7b29e19f40daebc1ce7d83b37c394250cff', '/.git/lost-found/other/30fe180b7dc5a182beaa893a2cea5b43e407312b', '/.git/lost-found/other/312308f273d963ad2f881e414e6dc908c7de72c6', '/.git/lost-found/other/312e11e2186827cecd4ccdb5f99b25b16de8e422', '/.git/lost-found/other/313257cee583598c2b1e76531aee4382a34ae791', '/.git/lost-found/other/316871d9d0ef4a615b8cd3e853225ef2a3b19c95', '/.git/lost-found/other/3168c2f06a254ab33a036ed9a99965494aa89e44', '/.git/lost-found/other/3176ec4eb6c6c275fe82fa458715a968e6073475', '/.git/lost-found/other/318a95b28c7fa29873933d535636860233bfe2a2', '/.git/lost-found/other/31919cbc2e7b9a6268f7bd5ade6a59d4902b52dd', '/.git/lost-found/other/319c61cf6810319b6333dbda3ffcf61438c2b9db', '/.git/lost-found/other/31e4b72c2638192bd9b6ff9894f15b4365be6f7e', '/.git/lost-found/other/31e88c3eb7be2600a07f8a293e0d521af54d6577', '/.git/lost-found/other/31f64f6e3b537ebaddf428c4cb7764d746510f2b', '/.git/lost-found/other/322ad23a9b2322a5eafbb97fd34f393402a04544', '/.git/lost-found/other/323f82bbbb2a2f435ba1a70ab85e6e604de01b6e', '/.git/lost-found/other/325706343725c6011b78dbccbe34e242657d5d49', '/.git/lost-found/other/327e8f6219bc9ac3aaf5c4e5f8a88559dd9c8d9c', '/.git/lost-found/other/32858e6be0b09a988b9b7722bed3b4ac6acf2711', '/.git/lost-found/other/328bc3afc9053e448e43ac838fbde8b5a6bff782', '/.git/lost-found/other/32b556713e2c319d927537477bda7dd391634e9a', '/.git/lost-found/other/32f8032b0690c3e5ab5788e9a392fb328fdde7e4', '/.git/lost-found/other/332c5bfc92dcc95b0fdab72fec060f0f1fde04f7', '/.git/lost-found/other/338787f9553f8178de800ae15ef7a23d4f096f13', '/.git/lost-found/other/33a71c56250cf2a2cf3bc20447d3bc0f4722b8c0', '/.git/lost-found/other/33c258c67e23b0e16815b8156accbe52ea0f47ae', '/.git/lost-found/other/33d111952f9df6dd8776978e49e1067a8bbcc82b', '/.git/lost-found/other/3407448373b50404341f30cfe3e19da4562e5b61', '/.git/lost-found/other/341580a820d2cd018774a99fd90cdd4928badc68', '/.git/lost-found/other/3480592152b095df8c4308029978a60900113bbf', '/.git/lost-found/other/34c6a03cca3744f90eb635e4a427cf083aad4110', '/.git/lost-found/other/34e68b2d3472d9f5c822bb72c9fc2c4ddb3f31a6', '/.git/lost-found/other/353eeeb90d31595d072017c457bdb335470c0b79', '/.git/lost-found/other/35425eeca676d4342ab62ffff6195d41b11f03ba', '/.git/lost-found/other/355ff84b964cd582bf1f677e33941403e9647582', '/.git/lost-found/other/357377a3e9d1596994eb7db5c89ea3b40161b48a', '/.git/lost-found/other/35942a0a0c5905e8a31fbdd947ee83d6135330d6', '/.git/lost-found/other/3598090e6a420d70ef76bde587c93ade0de2721e', '/.git/lost-found/other/35c6bf791767e8c12735840b07aaff1273f0435d', '/.git/lost-found/other/36228b5f70a00e5ce49800e5c4e6f423a864ae65', '/.git/lost-found/other/362381263cf3f80b5818de655e9053e7f11cdd9f', '/.git/lost-found/other/3627eb8009d622db55d0b115ad04a86af57dc99d', '/.git/lost-found/other/362dfe3c7cf298171bd42d395215477fc4996729', '/.git/lost-found/other/3632196771add5fcb90e466f66e477f671b35212', '/.git/lost-found/other/365be8f94d80e5067929f7549396a0e85134c387', '/.git/lost-found/other/36943e9cf8334b2d66b1b289b0477923183c99ce', '/.git/lost-found/other/36d35fe01b77481fe1e61d9f5cb7270df4fe7a68', '/.git/lost-found/other/36e7091b7fbff7d70e65f68a180bd36231bbeaae', '/.git/lost-found/other/36f21339d64c30f61addd97c3c411376231a882d', '/.git/lost-found/other/371991836494764af4d1bf157fb9ef9baf12051a', '/.git/lost-found/other/3731c5b1a9613854aafe4ca48509e0a5447058b5', '/.git/lost-found/other/376c1e88772f0558744c3ec5bf33e514bcbfa5f4', '/.git/lost-found/other/378b9fa979fd0cdcd74fb98be8f965fc64ba96ab', '/.git/lost-found/other/37a0ca6cc8794e5b4800cad42666f43d1593da69', '/.git/lost-found/other/37ab16fcbeb235841f49b53dda4f8a4cb8576605', '/.git/lost-found/other/37b0cc2012a9a29b9126c2222045b25cf5b61c05', '/.git/lost-found/other/37b1dbfa62553742da17b93f4fb2997a706ad491', '/.git/lost-found/other/37c80b6e3cd1ba73b73a863658651fedc19934d8', '/.git/lost-found/other/37eb658dd959056bdc91ca5add0c61677dd55131', '/.git/lost-found/other/38078e333be4a14ae2436aba441dd97d2d37acd1', '/.git/lost-found/other/3893a9d23c221f7a7587b3bd1bbce3e53451a36b', '/.git/lost-found/other/38a1a54a9daf5b271d9479b93a8af42e6c3731d2', '/.git/lost-found/other/38c69c470dbb40ae7c309888b1d1250f91ecdfe3', '/.git/lost-found/other/3928dccc158026c5d3bd664415ca5ce646555231', '/.git/lost-found/other/3932a7771a6417aaa5625d39bb52f63e9d5ecf03', '/.git/lost-found/other/393d937812a14bacba39114d3fbc6ba4b6f687e1', '/.git/lost-found/other/393f72379d2551529e19191f444ca8ac0324cc09', '/.git/lost-found/other/393f9a985c2a03394a2e4a7eecdf783ab4ad0993', '/.git/lost-found/other/39654433fd10a74f799c2e6d20c1faa49b0ec715', '/.git/lost-found/other/397ec1001cf0afcf62fe6b20e898ed46571f0cd5', '/.git/lost-found/other/398f7fdb157e0e718ddb1b583446c83525a9c8c8', '/.git/lost-found/other/39e7fb971ecd00a92d0ac87b16b10fd7dfc091a2', '/.git/lost-found/other/3a6fb490b61ef395f241c15652f46c571c0d4ff0', '/.git/lost-found/other/3a9c2f93081539b6786aaecb9961f15db261b7cc', '/.git/lost-found/other/3aa11aec8ea158ebe6fa2976edaac47f213d098c', '/.git/lost-found/other/3abda6ffef0e775951dfeda9637eb16314baaead', '/.git/lost-found/other/3acc108aed44025f56b47a7481ef7df3bdba7c98', '/.git/lost-found/other/3ad3ad101a41a3f5f7cb1ff2f8ac7fdbd4fbb1e4', '/.git/lost-found/other/3ae1b05c2a5d648e1e234162415c93a2d566455a', '/.git/lost-found/other/3b05a03bfb9b84a6f82a3f6b6d4fddb652001ca6', '/.git/lost-found/other/3ba38eeb4c4dc8a5029fa4c435a97b9bf9cb9c5b', '/.git/lost-found/other/3bdfe3e50659109f92b7cea294e2c2ccded7e07f', '/.git/lost-found/other/3c27c38977ce104a2f4a88b49b560e41090430d1', '/.git/lost-found/other/3c2a0da42d395f055ae2c4ece3d6d56b95ed0f01', '/.git/lost-found/other/3c8b5c679d9eb3dbd857a4bc2414e018507dfacd', '/.git/lost-found/other/3cbae7783af35d2629fd5daa444b860b54c1c541', '/.git/lost-found/other/3cc5321661d71bea5e919b2dd222d55638ef6474', '/.git/lost-found/other/3d1412302b68c0d01f1afda6130e8ef38906d800', '/.git/lost-found/other/3d2058541bd6f85fa9d3041eeb94773535041b4e', '/.git/lost-found/other/3d4090fbbcedee422c984f49d6951366d6e87331', '/.git/lost-found/other/3d5b8e81ff03360ac6eace0f9658f95dc3aaaab4', '/.git/lost-found/other/3d6ce554450436c4ee02e9238d7bee54a5c98a8a', '/.git/lost-found/other/3d76e8038eb8c5d0065da0f378418b0929a3e1c7', '/.git/lost-found/other/3dee1d10be4dc43fdf33e57816608eb7f5f762e9', '/.git/lost-found/other/3dfafe83a756a154636a42148009fc2f995374b6', '/.git/lost-found/other/3e66b1694740b2e545f26acf8a011934e713ac32', '/.git/lost-found/other/3e6ff38fa95be1c55c68ef2ea46946f569926f38', '/.git/lost-found/other/3e846e06d434e3be0646f8d8c73c8be9f548eb22', '/.git/lost-found/other/3ec37580b08a3f792df050067bd3383ad9c01df9', '/.git/lost-found/other/3ecc52a19ba9501ffdc2b0775d42316e3eb031db', '/.git/lost-found/other/3ede7dabe843ee07ced13269bd65b72c34b9b5d6', '/.git/lost-found/other/3edf7805dd24b80e8c991aefa453b6e60371e47b', '/.git/lost-found/other/3eea2cd0368389b3b358ffb2050310a8e5f01084', '/.git/lost-found/other/3f24447ae77e74087e11e85cdb792de9af39d23b', '/.git/lost-found/other/3f325646ce7bfe0e26c28c1e3ed2d2717812bda7', '/.git/lost-found/other/3f343eb336812ac82de7a282f46dd867f06f141d', '/.git/lost-found/other/3f5e76235147c70911902e9f103daf1a7314e95a', '/.git/lost-found/other/3f77999b57ace248e5dc167ef4e26b985531f944', '/.git/lost-found/other/3f980f549b46e7260f2214367a43deb12d0ef4b7', '/.git/lost-found/other/3f9fdb89a31a02a343b2b0b6b3e21fc7ca7d581b', '/.git/lost-found/other/3fca9ac2547a9940b5a04731b6524c73b9b17c78', '/.git/lost-found/other/3fdcc274f28047cac793cf86aed310300180bc2d', '/.git/lost-found/other/3feb49e8ddc04e5c3e85ae2ec34908b7ea1236c6', '/.git/lost-found/other/4022468256542bc3fe6c5cead30dd9c90615fd3b', '/.git/lost-found/other/402864b837e70ae54de89eb82cbe93546cf2695a', '/.git/lost-found/other/40758f589a15d70a0fb173d1dd0cd93c2b280b20', '/.git/lost-found/other/40a67f757ceef8b9e10d6f06e5b2ec8c75529ae6', '/.git/lost-found/other/40a857d2f4d88afe60d9d223c3874cb9ccb4a55c', '/.git/lost-found/other/410fd0e93a275523e38efd323fcbb83b8c8831fd', '/.git/lost-found/other/411b53810429fd3db2d870952d8c267659517b00', '/.git/lost-found/other/4158634eeaf9ee3f387b133b1fad878f8bf4c596', '/.git/lost-found/other/41d692718cca7d01e7f6785a5d39d34b0cd79664', '/.git/lost-found/other/41ebfa1a4e684dff0756a2297687708b98e178ac', '/.git/lost-found/other/421881dda370e44a27a3e93dc9caa1d44579a990', '/.git/lost-found/other/423b3458604e6efbe12f4620e1e5e7d0044acda1', '/.git/lost-found/other/4262aa86595198148b5c5af75bd5b347d55e6d4a', '/.git/lost-found/other/428a345dcc183804917d5077052693bb113f74e0', '/.git/lost-found/other/429074a78b514abba6f272bd54f3011a72c28afc', '/.git/lost-found/other/42b5b3341164d4bfd41c4b45e85850bf626b8ebc', '/.git/lost-found/other/42ca4054cbaf5d4c01d024bd7ee0918efc52ab07', '/.git/lost-found/other/42ebc146732d966d28b3dc12887b8f73ce4c4fd7', '/.git/lost-found/other/42ed76e3d2c1af07d1c2b357409e0630ded68c74', '/.git/lost-found/other/42fcf8ab7e1224020d789b4b47b37e4eff58c62f', '/.git/lost-found/other/43294817109e7ecb22f6b65e069a13b8270d1053', '/.git/lost-found/other/433079b36165ec24a2b3bfa3208be0e72c68112c', '/.git/lost-found/other/435a5c0d738969e6f5c3f22e6c83e385fbfd025a', '/.git/lost-found/other/4367533bb415365afca5247c8006e707527136df', '/.git/lost-found/other/4371fbe557c2492b0303af5861b007b2b20ea8c4', '/.git/lost-found/other/4379e78e42681a9c944ced94d3e215fef675fe57', '/.git/lost-found/other/437a496118d962d30110b9550c9933470f544b31', '/.git/lost-found/other/4396b48a65707e8d7917f9be1a2f6c18bc175683', '/.git/lost-found/other/43cd46747974e7eaefd6bc4515e802a3f16a787b', '/.git/lost-found/other/43d8aa62d08f1788f22545bcad2bdf344ae95c64', '/.git/lost-found/other/445b7add6b22f31d6169b6fb04c94aaeaafd23c7', '/.git/lost-found/other/4464c2c8a128a1cd27d261d90e6d66fa913160e9', '/.git/lost-found/other/447720e79a8bf68b0570557e2603109333a4a04a', '/.git/lost-found/other/447def406e0b202e5959a50704be5779c5793fa2', '/.git/lost-found/other/44d6e7a95ef488d9350b45e9cfa358ce04beec08', '/.git/lost-found/other/44e59e3cec45d7396ac73e863ced62a8d7f5c46b', '/.git/lost-found/other/44ebc6510ba8445a4f02160a7d4562395a9db5a5', '/.git/lost-found/other/45055281879d94949ebe9a279d805f909fa52808', '/.git/lost-found/other/45485f8473f8fb74c608c1215de7a9ae5b767a32', '/.git/lost-found/other/45969488a2aa771c9c0a5ac56fa58505d7aeecc5', '/.git/lost-found/other/45c2226188811a624b5a22e20465e156c9863894', '/.git/lost-found/other/460a7a8399d7b7db69e999894ed5f6a244e69d20', '/.git/lost-found/other/461886c6ac2b8d4e6ba0943a72403df1d6968569', '/.git/lost-found/other/4630a38916d765d913e0e6040a11b6132baa36e6', '/.git/lost-found/other/464073b94e8df746f5abf60322e5bc23c78508e7', '/.git/lost-found/other/4660835e392b7dd46c5e7ffc6a6f765a7a67478f', '/.git/lost-found/other/4678157d773d5c250ee875f3fc5ad8cfbb06ae38', '/.git/lost-found/other/46c6456223387aec0a7b111a58be75f442f3c342', '/.git/lost-found/other/46f574b31ea9c081d10dbc24fb57ba3e4b447b6f', '/.git/lost-found/other/472070c0c081ef4c9ea5e73fce87dec51a5e50bd', '/.git/lost-found/other/473daf24f1e540b2f25a569f819a238aacb81035', '/.git/lost-found/other/47b03dd951e4d464d01dd59f62c2b67f84506cc5', '/.git/lost-found/other/47eec38c60613993ebddfe34b03b3c993405009b', '/.git/lost-found/other/480ca1cfc93e3be2b2d88a08f067f9f8875022e2', '/.git/lost-found/other/48355610f438c75b706f3d1b9bb15c49f849800d', '/.git/lost-found/other/485ebc0e3b351a9997f0bd7231ed34ebdc5eba4e', '/.git/lost-found/other/48e9b14b31df8db282aeb8c13c7196186d5eaf72', '/.git/lost-found/other/497261e3c8906476c12d6208e965b9194d2ccd9f', '/.git/lost-found/other/49750a24fedc98c1d3f489355165462ef5f0c3a6', '/.git/lost-found/other/49e4545b844c30e3a2dfd5283289f27650feed77', '/.git/lost-found/other/49e5c2487096098aa82596f7c3bf4b154b03263b', '/.git/lost-found/other/4a1b4edccdef931f7401b221ca7b97904c5f9eca', '/.git/lost-found/other/4a4fed6a266a06c70783a57203e735d40084f4b5', '/.git/lost-found/other/4a561130f0ef82f6839112aea65b7c41d857f15a', '/.git/lost-found/other/4a64f6a423d13664596ad8952e9a991142c575b3', '/.git/lost-found/other/4a7421627f436e26ec2e56d8ebfee4e5b009e05f', '/.git/lost-found/other/4a9614ed45b8c3c446af97804ee70fae5cee33ee', '/.git/lost-found/other/4aa09bd0167a59b088b2c27f326b600029e93e56', '/.git/lost-found/other/4aa9736811f8b92b79e2fb5044fedd3827eaae85', '/.git/lost-found/other/4acce9508c07accfcb472ac7b53df59993547757', '/.git/lost-found/other/4addd3a9cd275d18232024a8986d0a71719be52f', '/.git/lost-found/other/4b0ca8a212de55c027ab38e37ffcd17e341d57bc', '/.git/lost-found/other/4b1106adc7b4c0535779dc0c2df302e2e4f26afb', '/.git/lost-found/other/4b16c36c5bbdd7a8a0aeeb449e081c80e2b75d01', '/.git/lost-found/other/4b4e6a0046c053a95f57754b9088a81834674349', '/.git/lost-found/other/4b5c220106e4b150f1785aca51b4c1516ee7f6f7', '/.git/lost-found/other/4b825dc642cb6eb9a060e54bf8d69288fbee4904', '/.git/lost-found/other/4ba7d47f279b001eb96215df8833b8c2cb201c3e', '/.git/lost-found/other/4c109c4291b72213236a54418e69bc70989d3d23', '/.git/lost-found/other/4c3c101d419f879404ff9994e148420b95f8ad60', '/.git/lost-found/other/4c493eb24622138649cb71acb19118998e7e55d5', '/.git/lost-found/other/4c5e7bcd16c8cb7d806fb0fff610e8f4c5db8de2', '/.git/lost-found/other/4caa0b8605ba9a8a10d09fa28ab020b5634c8f6d', '/.git/lost-found/other/4cd6f7724ce8848c6e3b4a92fbd8d8ee2c9fd8bf', '/.git/lost-found/other/4cde126dbb4465d93bf6a56e0f7557664cad7052', '/.git/lost-found/other/4d64eae0c3986894803d586d4c44ae16906d23f8', '/.git/lost-found/other/4d77a00c84211f3b1f7d0b33a9c650a0068ca57c', '/.git/lost-found/other/4dae699298c4e827eb777a620bc2b0b622a3d043', '/.git/lost-found/other/4daf2d4fb4be2002d0c6f0783065cd4aaa2ef9d5', '/.git/lost-found/other/4db248d2d0362a2baa123bce350af1c3cf725718', '/.git/lost-found/other/4dba40158ad402bdb18ab94f570242af2ecb9f72', '/.git/lost-found/other/4dc581629639bdbf6136e78e94203ab183c60871', '/.git/lost-found/other/4ddb67d026b4d1d9533591627008838db3040342', '/.git/lost-found/other/4ddead2405965902636a6bf032847bea1dcec5e7', '/.git/lost-found/other/4e560d39e66ee48393ac86adf8bf92f390ab6282', '/.git/lost-found/other/4e57556929f069e1d92ef1cedeadbdd46be69462', '/.git/lost-found/other/4e6cbaaa682013b3b168c0079f78acc0ccfe0552', '/.git/lost-found/other/4e80ac0c1f3b8a9f86cdccef454912a80077d15a', '/.git/lost-found/other/4ed608f4d1b961b4b069673f0dac7b286868f1d4', '/.git/lost-found/other/4eded7a6a9ba555dac903ab553ad0640bfafd803', '/.git/lost-found/other/4ef1590a8b7ddbc3f4fa8977aac9094f931283b4', '/.git/lost-found/other/4ef73eba22c74702bab0fa911b27145fe6efd727', '/.git/lost-found/other/4efd0c308d4fa547f805bf82210e817bc8739939', '/.git/lost-found/other/4f03978e25b1d70dd18b2f1ce83f070616bee53c', '/.git/lost-found/other/4f6403a8bcb6c19a368e929b9a4e12741e1ab55a', '/.git/lost-found/other/4f7bed90c38a4cbb348c4ad64255d11ed01043f3', '/.git/lost-found/other/4fb85fbb7c372a0b84cd78fa6b55e410e220239f', '/.git/lost-found/other/4ff93b7412dfd5e731ca509fefec5e2a910528fd', '/.git/lost-found/other/503b52b471cf3c48677445669dda1dda8fd71c51', '/.git/lost-found/other/50446582fea97fa549a6039a5f0c504364f69e73', '/.git/lost-found/other/5052541bd836a255d6414f0d6caf7cb46ce878a9', '/.git/lost-found/other/5056e85cfcdc5e48302a6ea6e308e29ec17154a3', '/.git/lost-found/other/50641e34bbca5261e3460924a6ad4cca4eb1e681', '/.git/lost-found/other/509b71d4704b84a1ffce51e2639bd836b3493ff4', '/.git/lost-found/other/509ba1ee9c66d67aa12183a23911275c84c1be12', '/.git/lost-found/other/50ab5d3cf546c8b875e8c8fecb728a69ed6129e1', '/.git/lost-found/other/50bf8437d9f0ba4f1b5bda9f3cfdff66feafd872', '/.git/lost-found/other/50c32b19907ec29e0df34ae3dcb64ccbad1bfeed', '/.git/lost-found/other/50cf16ba1f7cdef0e11f3e689c2ac0c4146c23df', '/.git/lost-found/other/510a9de17bb3cb81c8d9dffaff39e6a1ffc8d46e', '/.git/lost-found/other/5135c970168de2f80375b8e8223d8b65ebe722d9', '/.git/lost-found/other/514ef7a257573e892fef8efdc8092aa113f301a6', '/.git/lost-found/other/515672a3eac687eeaa0d5331a88ae03e9eec92ff', '/.git/lost-found/other/516400f538a8bb12359bf8121ffc8de0d1ece0a5', '/.git/lost-found/other/5177cddf0421903b5a7667854f6e1447853266df', '/.git/lost-found/other/517936a6f2e958e3c291ca7426694acc1c9ed684', '/.git/lost-found/other/51ead710372b626f38f784b6b56245267e896e06', '/.git/lost-found/other/51eddaf2d727e3973ab74f8d0d4d5d6925dfccf8', '/.git/lost-found/other/51fc32836d05581c65f4f62453fd8461eae64d47', '/.git/lost-found/other/5207df72e6c942df0f5a50074a13d02c5c6fcf92', '/.git/lost-found/other/520f6d14e206018e609af947049cff9cc8242353', '/.git/lost-found/other/5212c909d3b94b54efd1b8e83b0ae14bfd060e6b', '/.git/lost-found/other/523cfd7c6c11e165293fcbe926464d35abe0f7ea', '/.git/lost-found/other/52510e1da02780de64cb636dbeb5322763d39bc0', '/.git/lost-found/other/52631f7dd5d612089d235a84853c538dcfc63d39', '/.git/lost-found/other/526cbab8a8237857d96750d81938f8548229fdd4', '/.git/lost-found/other/528c0f551f1529db0685ebfb83fb5bcc0d13a715', '/.git/lost-found/other/52a9fd5d5a39c98cf011809f1954ce924858033a', '/.git/lost-found/other/52bd08e69825f02027ca3f99833ed05df89c9347', '/.git/lost-found/other/52ee24e4476554b49c7f5f84227ce066a0a46f9f', '/.git/lost-found/other/5321249b535a38dd91115955e2aa31639d2a7306', '/.git/lost-found/other/53989b292aea8588bedee021ac45dcefddb3caf5', '/.git/lost-found/other/539c77ebea4b39f981394f47d5682778d9282819', '/.git/lost-found/other/53c00c790d7213e762a416ccbd9fa61f2cc6b27c', '/.git/lost-found/other/53f1494b9ccdf2520caf09f9b6c9b0b6fe832f22', '/.git/lost-found/other/53fbe0eab185e254c6f27d57abc84dcdfd0223a9', '/.git/lost-found/other/5400429d73c66a98a7d7f803984889b2cf64f643', '/.git/lost-found/other/5415418c0097755bce371e51342cd16532d8fbe5', '/.git/lost-found/other/5424e6ee1e37bb5033742e0579176168ba0eb42e', '/.git/lost-found/other/54348c264bfa80b99bc179182d9d4400da05a8c1', '/.git/lost-found/other/54437ef622b766cd31a65735951ceb6b1f3dbd97', '/.git/lost-found/other/5444fe59b494246baf22bfe218d9f62cea416fc8', '/.git/lost-found/other/5459e50a37091210db1c5703a61149ff7366f367', '/.git/lost-found/other/5483d2dab97c022bd6d8bdbe5e7e91a0bb14d17d', '/.git/lost-found/other/54946c6df52fbea6e5f86390fa9fd5a6d9b8c581', '/.git/lost-found/other/549ef64d2ed3890a06bd03ef59952b31b70a5027', '/.git/lost-found/other/54a23401d7ac4923367c12c897f2444dcc00fe83', '/.git/lost-found/other/54a41810fd052d9463f8d60abf2c75184362b839', '/.git/lost-found/other/5541601d03b6f8e0c6c01342973a66430d8b0a50', '/.git/lost-found/other/55616d36043061c1a3c7f616e099f6a5abde1e72', '/.git/lost-found/other/55769048317ffd40eca0be3cea5a4b9e5ab7cdba', '/.git/lost-found/other/55804d3108a2a367b825f5cf1bb797755f5ada1a', '/.git/lost-found/other/55853255cc94e3efded0c03bbd00de39d57a7ce5', '/.git/lost-found/other/55992f60276d8ca420b03e6af91ed8af74fab670', '/.git/lost-found/other/559baa54efe7fb5e41f2551d2ca8e03f87ca5f0c', '/.git/lost-found/other/55b747cbbaf511f4d5424f0f1301ed30b1916007', '/.git/lost-found/other/5624bee17cfdf365584b8229349e7d5778a96c07', '/.git/lost-found/other/564f7f5c55645405bd63d23bc0315154baa54c18', '/.git/lost-found/other/56943cdf18ab772ff17cd18821c0cb38f040c874', '/.git/lost-found/other/56a2b9f0ddb3eea735b36c89c4433d9800483f7a', '/.git/lost-found/other/56e2a20d652ee923dad7ebb9d8aeda679efae502', '/.git/lost-found/other/56ea5e17523abc029922afcc9f23f2306cfef729', '/.git/lost-found/other/56f07bf7f1652d395100a1b2e0b96ed2b54e171c', '/.git/lost-found/other/56f3b2f52e650607bcb68a0a89e36251acb754f3', '/.git/lost-found/other/57707d21bc0c5ccc78a5b479538fa8f4af03b517', '/.git/lost-found/other/5796390469d48d2c75ad156f8f3c2e1054695731', '/.git/lost-found/other/57b04ada3b0285ca34c1a7fdbb9c904e484a2d14', '/.git/lost-found/other/57d46027e0e2507d28ac3ab8a433fb6035544f95', '/.git/lost-found/other/57d4a6120719f112e80cebbf59c497f211238fe7', '/.git/lost-found/other/57ef49de52a2d19fe06f40aa614014bbea9935bb', '/.git/lost-found/other/581d582546277573b28d5812835faa2ade024e61', '/.git/lost-found/other/589ef170d33fd55b085f70295ceebad9b7d6eb8d', '/.git/lost-found/other/58bf0f7e675b7588a79421a3fabaf0f35e219290', '/.git/lost-found/other/58cee47fb9ef92895314fdb4ea00faa945434e52', '/.git/lost-found/other/58d03866cf23187801f46939ec2328e2dc8c05b1', '/.git/lost-found/other/5905f9d6c104fcf3db9d8f19e6dcbde6149a6d03', '/.git/lost-found/other/590af4dd3c7d105d3ad2866312585bff30d02804', '/.git/lost-found/other/5928f67430c179dc2031c576bf0b24b51d2bca5b', '/.git/lost-found/other/5971fe317cc2404af9f0717140a87f15b0c0b55f', '/.git/lost-found/other/5983ea75fd9362c5a8709fb10cdfa4920f085b40', '/.git/lost-found/other/599223087cf2abf27e92dbb63ca3402862306cb5', '/.git/lost-found/other/59a6d7ca7e0bd39f24f74469da806dd2659236c9', '/.git/lost-found/other/59b78eed07eafbf8ed57b97a459a61e949c07b14', '/.git/lost-found/other/59d110fe6522d55e8e5f8650763f5ff86c935b7e', '/.git/lost-found/other/5a1e4a159d9cbf9d18e6e0da20f04e709b36e923', '/.git/lost-found/other/5a41118850b5b97764e3861fc59a901f69f18298', '/.git/lost-found/other/5ab3284a5abce4c25306590d08b3b50e8d0dfe01', '/.git/lost-found/other/5ae30190da5996be8b0111d18fe276b95d8e3ba6', '/.git/lost-found/other/5aed03d61d3a40a4e4d8859a43e5ff373d789afb', '/.git/lost-found/other/5af7955eaaa535c9f41527d8cab24ed5c1388305', '/.git/lost-found/other/5b03c014dcf3dab20b88f5a62dd0865020292ed4', '/.git/lost-found/other/5b3c284ca03de4c25ced51e9aa3a4b488804a44e', '/.git/lost-found/other/5b42a5fe2abb1393cf2b9ac7359176e4aed00c0a', '/.git/lost-found/other/5b5d27407a7bd2a7d7a767409ea402d354a9a684', '/.git/lost-found/other/5ba55edd28d0248f250495d47f6ab87821817c15', '/.git/lost-found/other/5bf68c1c51dae67f6a925c6ffcc4e45d0ee9c27f', '/.git/lost-found/other/5c1ab9aa3ef25014cdaf48ecc250f106e4abe387', '/.git/lost-found/other/5c40fd7e30b0ae67c6188ae7825d3ecbe2c432b0', '/.git/lost-found/other/5c5231a09008229e8e269d9a71bb646de28c0bd3', '/.git/lost-found/other/5c6ac7789c226f1cb333033c83401c787362e213', '/.git/lost-found/other/5c9d49cd48ff71491ca95509f601ff732142d86a', '/.git/lost-found/other/5d0c31c8d4c3150abb326fe441cf29550e85229f', '/.git/lost-found/other/5d51b2cf47c9bec0fd8dfc6a5c742839aead66d3', '/.git/lost-found/other/5d5c0bdce3886c23ef6aa2478091b71980c7b558', '/.git/lost-found/other/5d9ca220d74f6f62928d7fe74439558ac0eaddc7', '/.git/lost-found/other/5dad81834d096b45968ce3db534e06ef01cb7962', '/.git/lost-found/other/5dc8c414c8a6dcb39eead75672e29a6c7705fa1c', '/.git/lost-found/other/5dd53689515fdcdb933986493ce832b0fc154869', '/.git/lost-found/other/5df4f9798bc7768bbc0cdeaaf89cbb71fc7e2519', '/.git/lost-found/other/5e620fd25168e7c134890f30749078a81a7b6245', '/.git/lost-found/other/5e99e7ca5804c491ec01e5498d13b271c4c2f5b8', '/.git/lost-found/other/5ef0127085448a90356cab02f54d9ec9c190d13e', '/.git/lost-found/other/5f114962f8c95cc3d3e6d07ad8aceeef21cb42bc', '/.git/lost-found/other/5f278d44ee3cc96d3c7c582b2baa956cd2cedeea', '/.git/lost-found/other/5f7c76357de6ec1ef7872600c6c0d99d6fb29350', '/.git/lost-found/other/5fa52d56651eb41b51a76e9489bc3a1e803320aa', '/.git/lost-found/other/5fc241b5fc5ee3126714b7ec6bb1218f256b2f9d', '/.git/lost-found/other/5fd65f63e326d2a5a2305d4023ee3f9f9a1c7ba8', '/.git/lost-found/other/5ff9751d696b33f83abfca804807e09e998cc015', '/.git/lost-found/other/60055836c05f4130a75aa75b465c2932391fcfa7', '/.git/lost-found/other/601f2c09dd519075bfeb9db5b995db629718c821', '/.git/lost-found/other/604dca6b26bd18ef8041517b5520080d7d019360', '/.git/lost-found/other/60549f042a38455f36259a61d55c2a8a26a84f77', '/.git/lost-found/other/60737bccecfba65d47f6ce9e98a60da40dd51ab2', '/.git/lost-found/other/608826a2afc590737f32a764a625ef1f8c685dd5', '/.git/lost-found/other/608eab5a999f1dacde5212a37bb0b10c89bd5f2a', '/.git/lost-found/other/60cb3c25c404aaebac03a48a50958503db52145c', '/.git/lost-found/other/60cd35607497b333c4e689ec8c3d7beefb76d5aa', '/.git/lost-found/other/60cea4218c9d2d340270861f9084015f542aa19e', '/.git/lost-found/other/60e755f3531398a88cb2ba67af858c57dd0ab90d', '/.git/lost-found/other/61206657bd31e3e2e564ba4130c5cf5db80199d6', '/.git/lost-found/other/61240f34ff36c6a9ed178e7f3b0769d90d505ae9', '/.git/lost-found/other/6128184c716e17ff7c4382e61719214b88a65240', '/.git/lost-found/other/612b7e3dac1b05bc83204b5091634dc99d745a5f', '/.git/lost-found/other/613d1efee79b495719629da39214f79500635967', '/.git/lost-found/other/61731703e939fce963fa49e55b4af95286342a87', '/.git/lost-found/other/61ab639fb396a69f456a8a0e8161c81a66b36b50', '/.git/lost-found/other/61c62badbeadcca961fde66023da79591e056332', '/.git/lost-found/other/623e4c399c3cf78aa7bff72e26554c85f6869fe6', '/.git/lost-found/other/625248a511b95b56bb088ae1f70dfb5dee830348', '/.git/lost-found/other/625fa42e650c174cda286bf390e545c6354e1f44', '/.git/lost-found/other/627b2245b8bd0bb9433125096bdd64b99e749544', '/.git/lost-found/other/628b4dd0a93a7e16d3cbf73766ec9bae336e6116', '/.git/lost-found/other/62a41bba70c8083d3e9792ce06fcf891c6fa24d5', '/.git/lost-found/other/62b286e180ad3b353b79c522e41cac008f3512b0', '/.git/lost-found/other/62d1113d6b19143c69097fc9eddb4de615bdb653', '/.git/lost-found/other/62d972d5d66da2dc69c96c10b87c2fae3639a25d', '/.git/lost-found/other/63144637a3bd9f8474fbeb8463792c71442047b2', '/.git/lost-found/other/63491f18503bb3346888baa308185d2196d689a3', '/.git/lost-found/other/636d99342c41a4943fa0ca86f1619d0573375bc6', '/.git/lost-found/other/6372d5b36494f138c1638b3930d8543e77265803', '/.git/lost-found/other/639aff1317ae109c623652e0970c161d9a80a821', '/.git/lost-found/other/63d868359a2df3e9c0ed61a522b42a15afe9462a', '/.git/lost-found/other/63e70e5456461721b42c484bbee1886cfc8ba39c', '/.git/lost-found/other/63f2e29d53169726763ff4581e6fdcd3236cdb45', '/.git/lost-found/other/64068a5fd20e95303d2a58a8f948e08cab89c31c', '/.git/lost-found/other/640ebd997c31281a5274fbfcdaf9624d3dca7042', '/.git/lost-found/other/6417cfd675c0269adda74c4af4984a8e5523b5bb', '/.git/lost-found/other/6421734fb5e632258add15277e10f9d075b83131', '/.git/lost-found/other/64e4f4a1d9a5c5f3af3076ec413de73a3f5a4100', '/.git/lost-found/other/64e99286b0f3b21b065d94749079fd3fd4e94ff1', '/.git/lost-found/other/64f99c86919eab0648c3a2fb4b9b58576a85203b', '/.git/lost-found/other/652f440f92ba723251ba6ba470744e6d192a0ea7', '/.git/lost-found/other/6589cb9582ca26898931b1ff9fa713b99a51fd69', '/.git/lost-found/other/6604d0071186e48178e9b0dfe7e979040c3e54d1', '/.git/lost-found/other/66161534878c9a2771f904c86c37771812f852de', '/.git/lost-found/other/661bf6799d7caeff91a59255c0749bb0c19e430c', '/.git/lost-found/other/6638f29e468c5eb3550c99e26aff88a106344cba', '/.git/lost-found/other/66899d38c422ab75f0919f5714961b39fb244dd4', '/.git/lost-found/other/668a493ef1fcb9d584aefd1e500fe080eb2b7488', '/.git/lost-found/other/668ed8f54785171df27bcc3dd3ca6946b7c47b03', '/.git/lost-found/other/669527a55303ac3089986dfdd5be5379da40b8d6', '/.git/lost-found/other/66a367c89a095a293497c3606593eed3675b7bab', '/.git/lost-found/other/66b958f32ddafa4f75a7a2cb2f24a9e9ccf2a097', '/.git/lost-found/other/66d6a8e4d9ed60f991a0a185966cb717770690b6', '/.git/lost-found/other/66dc9fe2e67543e8bee36d8b809fc2488132e8d1', '/.git/lost-found/other/66f40ce43c80179972266b9fb98da995998b53c3', '/.git/lost-found/other/6701c178ad1a4b00372bae3c25cfaac2c80c9c62', '/.git/lost-found/other/6702cfd9756562bfb0a3ba9b5abecffb3edd3d4d', '/.git/lost-found/other/674604affdb240288071ea569d52f55c530b19b0', '/.git/lost-found/other/674f596c4dacebc48590bc262602ede7478a42f3', '/.git/lost-found/other/676fa0f11b62b954662d9a796a91c01408e97449', '/.git/lost-found/other/67b20ca14055482a477dddac64582ac8ae5767e0', '/.git/lost-found/other/67ce18851f37a03dbd8f1912f40b0333196a565e', '/.git/lost-found/other/682c9758c717f786de009b535f7b4809bcfcb68a', '/.git/lost-found/other/6842fe827192bab8f1180cc0a667d476df9cd850', '/.git/lost-found/other/68680d91ac416db504df57a84291d630e94eab46', '/.git/lost-found/other/68749693c84ef5a049465b1b192d56aa094cafc4', '/.git/lost-found/other/687cde57acd639e44b9f6ecf4bb3b29996c10bc3', '/.git/lost-found/other/689b7fb39f59c02e4fbbcde071296721398eb013', '/.git/lost-found/other/689d0da7d061471f4527308c48e26efb792ff379', '/.git/lost-found/other/68acc160c191f8f39dd69ea2c9fd1bd132519e31', '/.git/lost-found/other/68c62d74946ba59bc95c49aa23daa2faa9d50df0', '/.git/lost-found/other/68e38676e7f2aba51f365c5246a25b26eaf7c93a', '/.git/lost-found/other/68ed276d325e028f6520a3a2139e590b668d16ba', '/.git/lost-found/other/68ee67a9c8c69cc7b4387076d19412bf6fa55a91', '/.git/lost-found/other/6916bfc4ae8a8656910be8213444648b53a2352d', '/.git/lost-found/other/6924feb7662147552bee9698d879ef0e54b6d8ac', '/.git/lost-found/other/694b515cd1cc0b2492e6d20ed85c4e0a9212cf18', '/.git/lost-found/other/695a1fc4aabfb29ae1d4eb53d8262b001cf0b268', '/.git/lost-found/other/695c4393b98dcf12334da13f5dee4b09f2e56f61', '/.git/lost-found/other/69b678f6e53c24601108dacf7be78a0f4dc9297c', '/.git/lost-found/other/69ba46d4e80a1ca1f7e61de30c5a0973bcf9949f', '/.git/lost-found/other/69d86a739e9bcdaca05986856237308c2e352b4f', '/.git/lost-found/other/69e0d35ba51506e2a6b1c82fb10836e2944f7d41', '/.git/lost-found/other/69e6486640b279c4c27df16fa42efacdf5fd5318', '/.git/lost-found/other/69ea2e3abac381e1239cca65d1ff4425a100bd06', '/.git/lost-found/other/69ef08f9dd58c1307d87a9d77fe60fa99d0c0540', '/.git/lost-found/other/69fd638c548168d2d60451a27b06ab1f4168253e', '/.git/lost-found/other/6a0e4ee850e4136089b231c7385181f3833d64e5', '/.git/lost-found/other/6a10a4c99f71d892813817d6e131c32de5a3a0b8', '/.git/lost-found/other/6a5ca58dd7f7d4ff96beef4b05385fa608ce1276', '/.git/lost-found/other/6a61b1a3a9cdedf1639d353de4c161efb37613bb', '/.git/lost-found/other/6a7c5cbb6e250ce2534ddc459ec58e94ad59daa9', '/.git/lost-found/other/6ab43d1c8712b075016024e6de4b2cedad30d4fb', '/.git/lost-found/other/6ab5f05565940fa70b59ade18d5824d49687af69', '/.git/lost-found/other/6ab7a9816bb2bb377a0dbebd922c0f16d81c7db3', '/.git/lost-found/other/6ac3752495b076c748fd4e5c4984925643feef75', '/.git/lost-found/other/6ad46cb805dbdc2933f7591e26cf9223d5c4c09d', '/.git/lost-found/other/6add66c47d463964ce1f625054a2e62c78de0052', '/.git/lost-found/other/6af52eaf8a4268931a8ec6a132d7ee779f9b53f7', '/.git/lost-found/other/6b00c19ac5ad98cb682b6aa371330eca5c5137ea', '/.git/lost-found/other/6b22042beba9d91f0d97ac16821226b69175c861', '/.git/lost-found/other/6b35464eeba949dd63b3800fd407ec64ad156c85', '/.git/lost-found/other/6b7cbd1cdc3ecae6259e767ec077682ab8140d37', '/.git/lost-found/other/6b874d512a6169e56875de8896ae72ca50462b5a', '/.git/lost-found/other/6bb3e94d1d720c1348861e7a1dbe524b51eaace7', '/.git/lost-found/other/6bb4e0d4dd0ee5445099c82b2bd2f64a53e8d294', '/.git/lost-found/other/6c03949654187bb18a9d56abf3fa548d35436fac', '/.git/lost-found/other/6c0d651cafe38a80077e3f039cef23d0a74f61f4', '/.git/lost-found/other/6c22da847b3c7def6cd69370256886cb3df72bb1', '/.git/lost-found/other/6c5fc2bdd3439593a8643d755e206e6dfc9fc170', '/.git/lost-found/other/6c76334a601f051983003c01c0a4a9c9647d9409', '/.git/lost-found/other/6c84c530995aeb77ea4f06496152518f193072cc', '/.git/lost-found/other/6c8a6bf7a8364e9f3c66b02e8af3048c191749db', '/.git/lost-found/other/6ca4f377708c5ecf6907a214a05573cc42b26244', '/.git/lost-found/other/6cabcbec99c44d58b07d21563b56e3e3ecc9cfe5', '/.git/lost-found/other/6cdb8c84c0d8288f817da1bfc5af9d5ea100f691', '/.git/lost-found/other/6ce65d7b31135ccacfff2b3d2ab53e743f0fd75d', '/.git/lost-found/other/6d14e456c1a77b86235f00f27b0d7ff404895330', '/.git/lost-found/other/6d3808be278c3451214e6436726830d41ba7b8ea', '/.git/lost-found/other/6d3bebbbfb578533ce3e6ab76d4cfe41bc2c2802', '/.git/lost-found/other/6d4cc26ae5764ee023fc9a552bb075bfa762903b', '/.git/lost-found/other/6d52ba52a8e301203cf321217bf466872849a86e', '/.git/lost-found/other/6da26546fa1246aa176dd104defde990f03fb2d8', '/.git/lost-found/other/6dab0e6afdd91c28e48f63d3688707a18eb7dac3', '/.git/lost-found/other/6db056fef046577bfd43bd0b8f438aa337f406b2', '/.git/lost-found/other/6df408815ccc8efcd933582508681c4b44e1d871', '/.git/lost-found/other/6df878640493277c4d70736151c30bfa36d4c930', '/.git/lost-found/other/6e1a4dde1913195bcdcb1ab2c38819fdabd889a7', '/.git/lost-found/other/6e22f463b1ec7d2cd140e6e0b0e03a632aa90f06', '/.git/lost-found/other/6e4284250937e9e1f0201611e6096d4101d2d653', '/.git/lost-found/other/6e5315c52f4cb6f8f50c68116b2f12db8d110b4c', '/.git/lost-found/other/6edc0bdb4fd041efdbe26e3db5c16b7b8eeca310', '/.git/lost-found/other/6ee8d33c6149cc513fff7a4bb33af1cba643681d', '/.git/lost-found/other/6f21d6a0aeb79b7c4d3605725f306d44d94c8d27', '/.git/lost-found/other/6f2516ff42249437779576cb418ec04cb76f8024', '/.git/lost-found/other/6f2e1fed7351e51786da8d13cd287a382305f2ac', '/.git/lost-found/other/6f43d382fa76287088af7b112df53a49cba251ad', '/.git/lost-found/other/6f453918535498db9b0ac365f2433265782b6945', '/.git/lost-found/other/6f88ec227ecf2f7b141024b1d501544126a224f2', '/.git/lost-found/other/6fba22d4dc0eb6400d9414150d5b70602d6564bf', '/.git/lost-found/other/6fcf161c510c9b98c91a405a36236d1e7e6111f0', '/.git/lost-found/other/70268d1c998cfd8ff0496f00635f779488913cfc', '/.git/lost-found/other/7053cc71e49faa648cb55ce0f0bf2b206c62ad69', '/.git/lost-found/other/705469fe281823f80b2cf27ac4e097c432c0fbb8', '/.git/lost-found/other/7065f6674fe7a8235b352054611ce3983ec2b558', '/.git/lost-found/other/706a12e583fe32e25dda3d328dda9d590f7ac56f', '/.git/lost-found/other/7073db0d222f367a044b7b9a76927f51f6854823', '/.git/lost-found/other/708e1960cb8892a8a08ccca0fcb666ae281b2a16', '/.git/lost-found/other/70adf55db7d632e16f7262dbf14637069fc748f0', '/.git/lost-found/other/70d153a9884e3f575ceee6df23bed28105af19ad', '/.git/lost-found/other/70f09f86714b5f1a6772acc9824b08e5148482f8', '/.git/lost-found/other/71037982231de4a8c00ad8f13b4a6cdd81871edc', '/.git/lost-found/other/714397ace6f967f7f6c94a8446aad82e62242f3d', '/.git/lost-found/other/717ca515e3896ef68f1c05dace103215d030de33', '/.git/lost-found/other/71864276193f717598a3844fdcd23105f607a358', '/.git/lost-found/other/719a970b7bedabe76e51c19aef9d38a694ea8de8', '/.git/lost-found/other/71d32e4dda142850902ad5f13e7d833455cc1af5', '/.git/lost-found/other/71e14735682c30c4ee07a6cec6df1200444e6d14', '/.git/lost-found/other/71eff9cb705ba5e300fa3c97d8d889d379c26055', '/.git/lost-found/other/7205122093388382cab2ef86f8ca360144cf840e', '/.git/lost-found/other/721c0dd9c7733231be83aaabfd84464df8fb6044', '/.git/lost-found/other/7262a805bc2dddcb9400604a9c1e96b639fe1980', '/.git/lost-found/other/728c2ace778aeceb83e85f1bcde65cb271b6a15a', '/.git/lost-found/other/72b893688930c0a1af79d22f43abdb9006cee638', '/.git/lost-found/other/72bd91acc1b928d0be23a4a1256e69866fef734d', '/.git/lost-found/other/72ebd6a7cfdb38fcc2e0b29564a3b301f7782e32', '/.git/lost-found/other/734c82bc74fe1b035bf19a2c11233de87a528867', '/.git/lost-found/other/736a5f16704e8ac0e55a5a0eb3ca0341a6876e2b', '/.git/lost-found/other/738f6025afd72bb0175981a02cdbe76332d58329', '/.git/lost-found/other/739407bd14c0325d37aa5425b9ba3a92ddd47492', '/.git/lost-found/other/73dbad59cff4bd2f2c9349d428ea128acd9bff1c', '/.git/lost-found/other/73dfb5017aa8a0422396ca3bab010f8b0cf8340e', '/.git/lost-found/other/73fa97fd287d2dbdf544f5995bf4f80996e8dc14', '/.git/lost-found/other/7430dfa1e58986db8aacad7d76e64ea2a4a867eb', '/.git/lost-found/other/746b115d9387d45539bfaa7450c2d5af731614ef', '/.git/lost-found/other/74a77663a7cdfae6de127ccbfd7657aa043d6968', '/.git/lost-found/other/74c55be61fc8e1927fa6bf118fe52417a16ea98e', '/.git/lost-found/other/74ee664d939f3792fbf8c5de69ff5000a85e823a', '/.git/lost-found/other/74f0c172448a0aa50fb351f2512e47ab598c02ce', '/.git/lost-found/other/74fe5ea272dbcc8fddcdda0f3dc95a4baf6cc2d5', '/.git/lost-found/other/7521408ed06b94dc61465eb18f0de0112d662dfd', '/.git/lost-found/other/754093e7ab1ec13ed0596ba6c02d18dfb8f63104', '/.git/lost-found/other/75526bb0823b577cea9abea7a8e2d68880b4a56a', '/.git/lost-found/other/7563c407d2437ca7e9fe67a0bdcfbe9439559381', '/.git/lost-found/other/757a9f890df07ca2d991d61cbaabe564c1e908eb', '/.git/lost-found/other/75c449fb1c46c708d4282f2fc0c05d84b330728d', '/.git/lost-found/other/75ce886dd4b67eacf026e8976df7fdebbd4bbf15', '/.git/lost-found/other/75e403200b7c6f1e192ff409078d9539db59d5f9', '/.git/lost-found/other/75e83fad04dd51437daa3c32f8f69a6d0f1327c1', '/.git/lost-found/other/762405ef38fefcce716ce0ce148eeeb530e1e89a', '/.git/lost-found/other/763ddec02d2f9992db9e15ccdd04bc7a7eaf6b88', '/.git/lost-found/other/76645041e232c0adaa22acfe2ec719c5a504da3b', '/.git/lost-found/other/766c4871825fe6833348baad04d8aa11521a76c0', '/.git/lost-found/other/768bd9115951b30cf63873a24273425fea0d9460', '/.git/lost-found/other/769c1bb07714a82c3cd25c50f256f28519da231c', '/.git/lost-found/other/76d1f0ada5f99a0596db6f9b5f474d237450a49a', '/.git/lost-found/other/76fe1b6791b8ade1abf97bc01a4f669ca22bdf25', '/.git/lost-found/other/771d4dfee6367426c05c3d82559b5c866bf59ed8', '/.git/lost-found/other/77349909732fef77c64241e680e95994b7ab6894', '/.git/lost-found/other/7758d6660a098f9b40547314cac71582703a5c42', '/.git/lost-found/other/776a4bea95d8e9f4deeb6e136104a5d9080dbf4b', '/.git/lost-found/other/7776476fe91837a89851f29a87883844a29f1065', '/.git/lost-found/other/777c96837cb78e1e50a9d82e0c0bf6c555dba8a3', '/.git/lost-found/other/77de4ba2f2aef9696037ea20f5e791ec8fc33796', '/.git/lost-found/other/77e3948ebbd8863edb49b35b86613591d4c3a2fc', '/.git/lost-found/other/782871526d2a991f40100b5e32cd3ef1fa465125', '/.git/lost-found/other/783170539a1f735ce74f00faf966344072add26c', '/.git/lost-found/other/784048e81a3c695bf56127d23ce99557dbf5795f', '/.git/lost-found/other/784354371cba3231fbd5c9e2238ecabb9294c35f', '/.git/lost-found/other/78597a307d1679b079e99777b55023130a6905a8', '/.git/lost-found/other/78dda83637c001a3bbb5b46fbed552151ed51365', '/.git/lost-found/other/78e7d0c901ee8eeda3825be8d83a7bd2a65ac2c8', '/.git/lost-found/other/790cbbdb4670edaa8647b93e6e6c5a9fc4aaac3a', '/.git/lost-found/other/794f8566651960a583962f1445dd3f2b2cec3a1a', '/.git/lost-found/other/79824891a2ff44dd5a6b02039d317d363d9acc31', '/.git/lost-found/other/7996e753f0d39ff8510fa714661f86e7b916a821', '/.git/lost-found/other/79ae734789ab6ce0d184cc720e51c101d3ee0f59', '/.git/lost-found/other/79d34e1c1b4ef979275fb6c28c00dcc936dbbb31', '/.git/lost-found/other/79e13fdae10173de3edfc81b7d1f5cf09e950ccf', '/.git/lost-found/other/79f4d07757c8ada811eacfaa0ffc677b0b6993c4', '/.git/lost-found/other/79f69779814971b10ed2d61cb420b58981837c5c', '/.git/lost-found/other/7a37e0c59d04f44e91bee825ca3178653503fe27', '/.git/lost-found/other/7a60567d3255257a8ec8ffd90b47253fbb7779e1', '/.git/lost-found/other/7a72a47df56ffd23bb383a56ae637e4045424316', '/.git/lost-found/other/7a761a5bd14d2eb15e7fc3dfa4290f5d112ec66c', '/.git/lost-found/other/7aa8a776509d35c4b416ce478c310947105abb78', '/.git/lost-found/other/7ad2274d82286b18ce5a0790edb400eb0246c04f', '/.git/lost-found/other/7ad4e5dfb7fe46e62e7ee90c8437b3cd1c98569e', '/.git/lost-found/other/7af76ad5f51ab852da29c8d0a5e75dd9cca94159', '/.git/lost-found/other/7afee14e783f58433d2ed72b25963ebfcb9ebd46', '/.git/lost-found/other/7b00b279b725540bd5e801557be40c425fec033e', '/.git/lost-found/other/7b554508a7883735a7262ffdb1925e70187a153a', '/.git/lost-found/other/7b6cc09cce20fabad0e43645e6521e9c01be4a1e', '/.git/lost-found/other/7b8bcda56aa1fb97e405498e9e342bde05c8863b', '/.git/lost-found/other/7b92ce8b462acb10ee7b3cd6dc02c7d60ed4526f', '/.git/lost-found/other/7bed1a58912ef89bb40536ec81317ad4e857a3af', '/.git/lost-found/other/7c054b66a898848ce6abc261795be460993ac3d5', '/.git/lost-found/other/7c31bb200ac9ee3c8526031f3f462dcfbc0c6dcd', '/.git/lost-found/other/7c5bff6ad3b31492b0ea35a60e3b1d567f5ece3e', '/.git/lost-found/other/7c63e8f7e164de6eac3bf0e4c2c3b86a7006969d', '/.git/lost-found/other/7c6466d64311464b5cc235f012e7eefa7a3f7dec', '/.git/lost-found/other/7c7106db340073127212c46b54764a7d5c52e087', '/.git/lost-found/other/7c7e207d982350b509a2ff479318fe62ed1103fd', '/.git/lost-found/other/7d096caa38d54e011864833826dae24415d66cbe', '/.git/lost-found/other/7d1fa3cfc7a26b23468ef0231a6be425c10c39c0', '/.git/lost-found/other/7d81eca17a7079421b153be35661242578b7fe4b', '/.git/lost-found/other/7d98aa8ec82c154d18bf0e39b24127fd2869c35c', '/.git/lost-found/other/7dff8c856fc62009ba04eab81b3d92ea8b342e7a', '/.git/lost-found/other/7e3e2c020369ec22896955e111fb75738e082b9e', '/.git/lost-found/other/7eaffe3bf399b2a747c76d625eed26950f8832be', '/.git/lost-found/other/7edc089948c55fed4ed96c4947d60561584833d4', '/.git/lost-found/other/7ee4ad885aec0b6786ee1a6ea747a4f012e0478b', '/.git/lost-found/other/7f17877bb03dc7a4b1da8e34bd24c635c8f1fc85', '/.git/lost-found/other/7f1ccef0257eae07e1a9d96c9a419839eb69012b', '/.git/lost-found/other/7fa989db3783a9017443ea55642686cebe2d31bc', '/.git/lost-found/other/7fb7f2e1a4f005e0ed97213f366b2a44d2b5f65a', '/.git/lost-found/other/7fbedd5325332884808b4f13376b20b608ba153d', '/.git/lost-found/other/8039eca3d631d25a1a6d81d08eff05b10453a080', '/.git/lost-found/other/80417b62ee231928cf6e1894ee78ae9d52dced8f', '/.git/lost-found/other/80525b0220584bb2859e90b7b1ecd96124809e0c', '/.git/lost-found/other/805a2540e6e5e0069b0845c8c0d64cc013c0c921', '/.git/lost-found/other/806c3e29a41d7902dc4bfb90b274f7bcdd692396', '/.git/lost-found/other/807fe9f45b577f7b4e832f53598c9132f4634217', '/.git/lost-found/other/80aa6242175a7dfe9cc180151a3c2506287ed78e', '/.git/lost-found/other/80b101102e4af9e39d14d4724273ad6c8673bf8b', '/.git/lost-found/other/80be9d64780cb8215aa9e33cc9f7225d9e763c45', '/.git/lost-found/other/80c7cbf169b9a7de67f1c1d510ead12a86092a6a', '/.git/lost-found/other/80d57ddd52a3d347c46ca1ec7bd6611c3832991f', '/.git/lost-found/other/8135df1518b818e32969ee29a72deecb538a4932', '/.git/lost-found/other/81919ab913ed8acf77c6c0d10a4011b81929dd15', '/.git/lost-found/other/81a82ea2302eda7a5d9cfc93dc15d7aac51acb7b', '/.git/lost-found/other/81b0c9d26060eac103e503fee24c4dc875d73a3d', '/.git/lost-found/other/81b84d2f9246fe95414efaf594ce0d66642af224', '/.git/lost-found/other/81c8e0c1332f8beac34dab5b2d8addd868c78d37', '/.git/lost-found/other/81c929641ff4bb9378d8f539707794ef0bbc35ab', '/.git/lost-found/other/81d135cdcdf753f12ffe7875cd8b84a1aa949a33', '/.git/lost-found/other/81de4211ddd55af9724945af37c733222887a4a9', '/.git/lost-found/other/8208ad133751cbfe78ea16f128cd7bbc1d8c8384', '/.git/lost-found/other/823eb92c648fdf767079c3d6ce64a4e1acfd1d51', '/.git/lost-found/other/824f35363eb09575efb61b59e2a3f4a491629ff3', '/.git/lost-found/other/827a08acc83b7c7a0ccbc1e77bed49435faa6c14', '/.git/lost-found/other/82a5b244d810b0f28e1c0ed826c6b90c3fcdeb69', '/.git/lost-found/other/82a62bb26671ed1e264c244a53da765fdfb6b534', '/.git/lost-found/other/82d66f9855421d3b02581bf6cc776b9401f31a91', '/.git/lost-found/other/82fe660600bda9fb261c64b3d868893a616c6f6b', '/.git/lost-found/other/8326d463947af356e07709d303b413cf1e06dc28', '/.git/lost-found/other/8327ca0d029a9aa0dc380a0ecd1a1ba295fdb6f2', '/.git/lost-found/other/8329fb9ca2717aaf3c0f538bda50030d0f9a88a6', '/.git/lost-found/other/83522d5d571930293dee7c041f9baa0d8c5be22e', '/.git/lost-found/other/83793f9f677aef3ad5f0496d7189d41a71f84c46', '/.git/lost-found/other/838b4934b5ce8b997c97a179ae31efe0df8d69c3', '/.git/lost-found/other/83a1cd018182bd007961c0c1a384f90721538a41', '/.git/lost-found/other/83f433e75ff687ed7ad6e622082b3771f4be902a', '/.git/lost-found/other/83fcd0a4b90b111dd78f24830b0cf0fd6f6662e5', '/.git/lost-found/other/84032ab70aec1220efafe862badb544ab9136474', '/.git/lost-found/other/846fd5afd14b372c7b10c236929e87409bd9ff93', '/.git/lost-found/other/8479528c7d38418a08b92817a5605425c6c65ea9', '/.git/lost-found/other/84a3459111e3b7fc5e8b3db7becf37841bb9af09', '/.git/lost-found/other/84e98f7d23fd1e49868aad7b88e4c25ce27b5f98', '/.git/lost-found/other/8506bc72a2d41cd6d60a4fbb7e3e3e441c831ea6', '/.git/lost-found/other/8507cc0d8827de0caf78209b1bc8b409c30929c3', '/.git/lost-found/other/852f59ef505774d2e1cded9189583af9a7fabfbe', '/.git/lost-found/other/8530702851e912a09461c1b3641ed4447c267bf6', '/.git/lost-found/other/856a9d9a9af9342cb38e84fb97d0ec8be25c4979', '/.git/lost-found/other/856aa17c270d6d6f2b9f0df34ac3aae243b43f0e', '/.git/lost-found/other/8575593501bfc3c1fb9f444dfce8ed8866d583aa', '/.git/lost-found/other/85775c0cf59c7c0a7c8c01be3dc92e2b76038b2b', '/.git/lost-found/other/85888b8c832f86d827cb9fc78205aac1c40bc919', '/.git/lost-found/other/85911b7b0a87b6ef634ba88ee35c9ea798547413', '/.git/lost-found/other/8598ecf10a790316c773068fc621b1ec6a8c7462', '/.git/lost-found/other/85cf7fffe0d71feeb57e13553129f631dd706fe2', '/.git/lost-found/other/85efd595e03f195168517e451a0f6351e2f9e69f', '/.git/lost-found/other/85f0a8f1420aabbd7a4472ee3ed2f9d968be657c', '/.git/lost-found/other/8636b42068ee84f766948b4f22e52bc3280e9eb7', '/.git/lost-found/other/868d17c19fc94e4da1a657e07258f027e37a183f', '/.git/lost-found/other/877dbd89e8209c09b4e6117d45aa1ffa5c29123a', '/.git/lost-found/other/878572383d5cca030620695db137e5d8befb60e2', '/.git/lost-found/other/878ec5f103298fd245bffbc77e9b4122705d6caf', '/.git/lost-found/other/87a3f4559d75c1fce1baae89b3777b9bef57f4c6', '/.git/lost-found/other/87b4d789046bbf43385acd61e5c3e70a1bec50eb', '/.git/lost-found/other/87bdeed1fa7053bf3f3ee36c8996eb1a85ca4581', '/.git/lost-found/other/87c156c8531b9854f8913b8ca70249dacd305771', '/.git/lost-found/other/87f508dde1d80fd527a62801ed475fdcfa1199d0', '/.git/lost-found/other/884ad461f9de46bba7b5fb8b37d1f4fb913b128f', '/.git/lost-found/other/8862c16224430bf0aa6f410ce9df8777453427c3', '/.git/lost-found/other/888114b868b7b1a10c7b8aedadfab6a0b198d938', '/.git/lost-found/other/88a12ae4891c84ce446aaf38698e7f684d05465d', '/.git/lost-found/other/88a57a29b1fe7fc24955b3c475d2587cfc2b2168', '/.git/lost-found/other/88c4d478b40dec9953b90c124136cb8ca6aabac6', '/.git/lost-found/other/88de5d8898855804a10e46a2b8ed2efdded56c2d', '/.git/lost-found/other/88ee53c9ece8ef43612f9db4cc25aa5614aa26ad', '/.git/lost-found/other/8969067bcbecde61a44d7cf0f5d364fe265ac08a', '/.git/lost-found/other/896dd57e7a94ddfe4430921fddcf78e252b7053e', '/.git/lost-found/other/8972d0e0bf6c14c869c716e06845e43ee7d373ed', '/.git/lost-found/other/899125167a136688cdca3cfc2a02bd8767aae87b', '/.git/lost-found/other/89a8667eaaa858b441ca2b4cf8f783a98017c631', '/.git/lost-found/other/89c09fa5bbb4ec88f5f5586334bbc9b5ee4def63', '/.git/lost-found/other/89ee971a3b572fa574374f7d8789267118bfdc5d', '/.git/lost-found/other/89ff128aa63e61990193840dfa90762d4f8f3652', '/.git/lost-found/other/8a1b068cf37d71278de5478ecea3b17e478bc53a', '/.git/lost-found/other/8a2e1744f8d60b47acee31323eb9be5252f3bb71', '/.git/lost-found/other/8a5e5ad2e568b464c38258b18b07105fa93c8eeb', '/.git/lost-found/other/8ad6631101557add7e9f03d4438ee6d4bd81fcd1', '/.git/lost-found/other/8b0fe43b479ecc9b599ccb21386dcf6243fab6ef', '/.git/lost-found/other/8b166483db6ab554b4ed7cfa227dcec5c0b5c4d1', '/.git/lost-found/other/8b474e9468a368ca615b1d5b7e8ae43995e7ed6b', '/.git/lost-found/other/8badb259266160ed2ae90c6d544e84c1f16bdfa2', '/.git/lost-found/other/8bc007bd8099a368761f7a85d69e8c62e91751d7', '/.git/lost-found/other/8bd53ac2f88091ca967b218668ddeb2b8b901b3b', '/.git/lost-found/other/8bf56f827628f29cc78ef7e19693f5b957efcb55', '/.git/lost-found/other/8c032fd3bc85f561863400e177168dcf3ace645e', '/.git/lost-found/other/8c193116cbb53901051d2a1d16301a18a0dcefcb', '/.git/lost-found/other/8c32101bf52c685290b17f8f9152446952caaef4', '/.git/lost-found/other/8c532b7669a3fd0dc35dabdd43d2b34db2726089', '/.git/lost-found/other/8c768de675b19dbd6d0328fda1e54fd350b3621b', '/.git/lost-found/other/8c7f0d1ecd32895777182562810997d842a1cc5a', '/.git/lost-found/other/8ca05df80017a216b6e9c040a13de4ef1c762f3e', '/.git/lost-found/other/8cdaba2214ca080e13141a212a14fa3492dee9a6', '/.git/lost-found/other/8cea1e553faca94727050f1666f760a5b579a34d', '/.git/lost-found/other/8cef1dc2bb0c10cac3165c3672402be4fe31054c', '/.git/lost-found/other/8d39cd48167f79c08783e996e5054ba4430f3918', '/.git/lost-found/other/8d87692ec4508add82fc7bcfb11627594c76759f', '/.git/lost-found/other/8db2dc5e2da502d8be60f83c29b6bd8cdece283d', '/.git/lost-found/other/8dcf63db4819ce835831f19b7f843f66cf331057', '/.git/lost-found/other/8de773e9097a8f0dcbed369e6c3e3f3dd481cb8d', '/.git/lost-found/other/8dfb262567a945bd38c2f444dd5a91c0c674ded1', '/.git/lost-found/other/8e147d7dafa9de53bdfdf1afdd2288c7015dab9b', '/.git/lost-found/other/8e1df140ffb6a1a2e0e1dbc48231a1341416d5ef', '/.git/lost-found/other/8e30c681e95c989c9194668613784ec1fb70c362', '/.git/lost-found/other/8e508aca87513c614f529e35534a6f510f5fecc4', '/.git/lost-found/other/8e624b995ed2e8b2f8a1fde05616b92165f1b612', '/.git/lost-found/other/8e6e6dca3e2142e6450e31de9dcc15e1315d11d1', '/.git/lost-found/other/8e886852a0b8f8effe43f3249827b417df2987c2', '/.git/lost-found/other/8e8cc43769b3e51927bb486257e5d2389bdfe3e7', '/.git/lost-found/other/8ed2f0dd8617bf639e3528efcc136bd64ff48295', '/.git/lost-found/other/8ed475a3ae2bbea45fbe48ab50f5ea73d830fd2f', '/.git/lost-found/other/8efb95334e4dfd7238406b637b87d38bc7df7971', '/.git/lost-found/other/8f29fcc619ffc635697fc2d2d468888819a7c05d', '/.git/lost-found/other/8f5819fda3698f87172becd15cd54ad20cdbc350', '/.git/lost-found/other/8f872767673fc75e5c1421d89521e998af4f8d39', '/.git/lost-found/other/8f8836cd2c592cc7a626577ab0c78aa97314cb80', '/.git/lost-found/other/8f8a2153b54a03fb30f2d21c11b2fc65b5071796', '/.git/lost-found/other/8fe85b124c02b0a063a255461fdcf4462b871849', '/.git/lost-found/other/9025e7e99615220286bf75c93d3246d302f1375a', '/.git/lost-found/other/903e19a32e203d03671b31f6e27ebaa907166d90', '/.git/lost-found/other/9040ad1040d2f81d6eba6d481dc29f2a5f5b2f73', '/.git/lost-found/other/9052c9897d84020cc14786b82536af8a94cad0e3', '/.git/lost-found/other/910bcc380d91aea78d4bab200472aee82a8e9f96', '/.git/lost-found/other/91129c883e5f0e47819acbc2aad8d6314c0310a4', '/.git/lost-found/other/9117e524aeb011990bc54777f70d56955ef716a3', '/.git/lost-found/other/9124c4e8d7b6925e2de9f96ba7ee66e9cfbd5b4f', '/.git/lost-found/other/91364a90eb688a950083474549ee42e8e0eaf78f', '/.git/lost-found/other/91501834e260e8d218dadf002c167daf1d7a99e4', '/.git/lost-found/other/915fd7b0567afe8725f78a286a8d8155d5b1a361', '/.git/lost-found/other/91897ad77d725aab215d18fc41d34a68ad6b142b', '/.git/lost-found/other/91a71c4d7e7cc2cc27852d2b1a6c5a1931fa1f11', '/.git/lost-found/other/91d3aafcff2a3ea74c1cfa946fa955c62abd89c2', '/.git/lost-found/other/91e214a28a493c3c2e35325fb7245d6983ea71ca', '/.git/lost-found/other/921a6caed41c95b6bba1e56724fe34b038245416', '/.git/lost-found/other/92301588927b94a7a8d688c5220721145e377e38', '/.git/lost-found/other/923210f734a2e995f200388e83d5fed3cf26053f', '/.git/lost-found/other/924d93052389d0b9434705bfe32ef317528044d9', '/.git/lost-found/other/92612a56a21f153339abb5c4efb074765d36aceb', '/.git/lost-found/other/926e20ae59a15432cc966c029407288466bdcddb', '/.git/lost-found/other/92dc8ccd7943e2b3163be459d4fb36f013ffff6d', '/.git/lost-found/other/92f0a102283a69d06abb892c5d78980a6a4d2652', '/.git/lost-found/other/932ab411aba0a979eb6a54f3c43832011843338f', '/.git/lost-found/other/93424d534c936bf6e468285533db39e19a47cc4e', '/.git/lost-found/other/93767a88113b92a54fdb35d82ba698c50f0af898', '/.git/lost-found/other/9387b3fd7de48b7e14efafef2ed67c4eb5015716', '/.git/lost-found/other/939be16e271fbe69d578fdb0ef909996a506933e', '/.git/lost-found/other/93c6ae943c48d1c8fe60cf11e869de7401a70e9d', '/.git/lost-found/other/9437d9d6ad6a559a5d535231870cc81d2e5f61e2', '/.git/lost-found/other/9441b1dcc2d951a7881cdde15f1bb4aa78e01801', '/.git/lost-found/other/944e4ac44eaf17d1c2a0a2149c670b79db3b81bc', '/.git/lost-found/other/948a2574e766a7def043341e9d592244e5f656cd', '/.git/lost-found/other/9494d7d02c4efa7814192147f9cd95198b968706', '/.git/lost-found/other/94bf9b9cb3ad20e5e40e68b19d2d967351fd7043', '/.git/lost-found/other/94ddb92592b2844dab2a6dbf6b54c3ec65c53adc', '/.git/lost-found/other/94f86597692644521fcb91b65ebfa1d6698b721e', '/.git/lost-found/other/9523046c930fc423ff2f2d964b0ad1f0f8dcc561', '/.git/lost-found/other/952dad6cd5e0a77bbc998b01cf76b786dcf86bd2', '/.git/lost-found/other/953728dff60b9ee56f8f94c427b6512b881a532f', '/.git/lost-found/other/9596ea8c380e21e2936eebc4d43cc3da5c3945dc', '/.git/lost-found/other/95b3c141d6f33fa02247dc87531e793b05061531', '/.git/lost-found/other/960849ac9a576a80ffaaf0a558644a959e85d725', '/.git/lost-found/other/962e546dcc1ccf96804fc035e0c053e640867b9e', '/.git/lost-found/other/9683a32d2a5b6572a83f7b012fa1bf38660ae712', '/.git/lost-found/other/96947147a4afca1db6085e927b1a9a03d61ffd73', '/.git/lost-found/other/96b583ead2754801cabadeaa6310962d9484b35c', '/.git/lost-found/other/96c55467020eb5967190ef67ea5af73bd8557293', '/.git/lost-found/other/96f0c3a29711baf739f8d206549147833769309f', '/.git/lost-found/other/96fd88067893385c0765030c47af266de862e670', '/.git/lost-found/other/970b3536b39e69354428d28cb4461dc2b51077a4', '/.git/lost-found/other/979c845eeee9c7ea69e9be82ea0152129d99ab94', '/.git/lost-found/other/97ade8382b5461f3e7dba16ee4cb7b21e3428693', '/.git/lost-found/other/97b5c66faefdec6e1e3f9511ffa5352ba6aed231', '/.git/lost-found/other/97d1c714bdd88d2c18292f04270b1d088b7ab423', '/.git/lost-found/other/98330f2a74870e2eacf010a3dc6ebf02ba786210', '/.git/lost-found/other/984da4d425592c6728086f770d46015c2774fb7f', '/.git/lost-found/other/98570cf2f3892aeb6a60317d3c5f2395551fa126', '/.git/lost-found/other/98634d3201e655b428c3720dfc45a1deaf0fd370', '/.git/lost-found/other/98a5ec496c33e52dbeece3cd0ce79df9d837d56b', '/.git/lost-found/other/98b214d389c3b000b67c73ef23a93e020caa45ce', '/.git/lost-found/other/98d9cd7743f231620723d495810cd1f76180c10e', '/.git/lost-found/other/98ddac6847239f0b68e04184b7c57cbffa12398f', '/.git/lost-found/other/98e1a00c29c13261193d33d35e8b870695aabfbc', '/.git/lost-found/other/9900a37055c69f4e8b8b84d6c679c7340cf21a2a', '/.git/lost-found/other/990b82d5c7737e7d79db4d7ee986945bee8c8b04', '/.git/lost-found/other/9964532f1952d9499823130c76cd62602dea68b4', '/.git/lost-found/other/996acb6402c94e8606049daf81862a1b810911df', '/.git/lost-found/other/996fca5689f017cbec23de29b1c8f9dc02a3b8e2', '/.git/lost-found/other/998187ffe021319b3cd3f43f9d7f7abe4aba6b90', '/.git/lost-found/other/99c369006665885b83433b1cada3e5998e5155b2', '/.git/lost-found/other/99d222d5d2d4742cfd70b247b8bceadd95fc4706', '/.git/lost-found/other/99e9be780090b056920e343370328c22ba0ecc8b', '/.git/lost-found/other/9a0d0a46f1f98aeebacd8915237221e8debc95fc', '/.git/lost-found/other/9a3ecb7700bef0e0c4bd76dd2a5bbe456f4eb302', '/.git/lost-found/other/9a4616a547f0ed364e71860ef4ffc26169a6f73c', '/.git/lost-found/other/9a94aec61779e9b91b8ab36885ab378ed5381c05', '/.git/lost-found/other/9a9a7e3f5a41b5c06d2f01bae830cafb07662606', '/.git/lost-found/other/9abb4897f6f8e61f116f836df7fc815e683a5611', '/.git/lost-found/other/9ac9a25da69a69c9c6ecb565b8e855d3d39d4dd0', '/.git/lost-found/other/9acd9309209b08b5353508e51b9107bb633a3b64', '/.git/lost-found/other/9ad7f9e4369acab40cfded3808876b7574f9390b', '/.git/lost-found/other/9ae4de87cb7ccdf07bb847d053307a3ab4196481', '/.git/lost-found/other/9b135bc75fb31913ebac007ca795c8a3e4e48b59', '/.git/lost-found/other/9b14110138d38f3594da82ed0abfb4d21ebdc2d4', '/.git/lost-found/other/9b151ebe22fb8c68a8f49571c62ea3f3f871c496', '/.git/lost-found/other/9b3627817278c3f1ea9f6f4fe2f8301d898b829c', '/.git/lost-found/other/9b4e06037e8da97ab1ce8591a052374860695c5f', '/.git/lost-found/other/9b6792f2b4c9ff8862bce79bb1422fe2735f6917', '/.git/lost-found/other/9b6a05c434791a48c447099ee3ce5ec6b9e1f586', '/.git/lost-found/other/9b79025bbb1e34766f6443b40eb90bb0bba6c9dc', '/.git/lost-found/other/9badb09849de0c3f46533ec92a264f923bc149b6', '/.git/lost-found/other/9bdf7450b467a385642426ac89ef2005f566bba0', '/.git/lost-found/other/9bf0e2c09edf77769e6856ecc475bb3bb86e45be', '/.git/lost-found/other/9bfa97bbb437b4b931b0f513c1a1e9c010d63eae', '/.git/lost-found/other/9c02ba73b9be8a9da49a3b46b30d7c34bc0517de', '/.git/lost-found/other/9c15049e5cfa12c8399e9351b7c79a3c5c0a35dd', '/.git/lost-found/other/9c27c00a245e6db44d7f5dc05a9cda11bd241541', '/.git/lost-found/other/9c2c8551bed5180419eecfd0b4804adef7d17120', '/.git/lost-found/other/9c3f1705d62820bcd18c94af78df6d715cf689f0', '/.git/lost-found/other/9c424dd2b362e6d8a913bdce28ef6d8ded2b941d', '/.git/lost-found/other/9c4d69fa051f3a9ec86455cd25c9142fa58a6521', '/.git/lost-found/other/9c5cd6913b03e959899602abf1b0f95eab47bfd2', '... [results truncated, try being more specific with your parameters]']
AI: Let me find the actual project files more specifically.[{'name': 'glob', 'args': {'pattern': 'inputs/**/*', 'path': '/'}, 'id': 'call_00_dPGfOJk7QhVm3t6IFhnw8181', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'outputs/**/*', 'path': '/'}, 'id': 'call_01_KNxmoHRM6qMteGVriNnm0222', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'skills/**/*', 'path': '/'}, 'id': 'call_02_P2obqH7Xz1UsrrUAjmSG2038', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json', '/inputs/matrix_legal_propositions.json']
Tool: ['/.venv/Lib/site-packages/langchain_core/outputs/__init__.py', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/llm_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/run_info.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/chat_generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/chat_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/llm_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/run_info.py', '/outputs/working/_preflight_check.py', '/outputs/working/bootstrap_report.json', '/outputs/working/clause_index.json', '/outputs/working/contract_legal_propositions.json', '/outputs/working/contract_product_profile.json', '/outputs/working/derive_working_artifacts_report.json', '/outputs/working/legal_propositions.json', '/outputs/working/preflight_check.py', '/outputs/working/repair_contract_ledger.py', '/outputs/working/working_artifact_validation.json']
Tool: ['/.venv/Lib/site-packages/anthropic/resources/beta/skills/__init__.py', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/__pycache__/skills.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/__pycache__/versions.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/skills.py', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/versions.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__init__.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_create_params.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_create_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_delete_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_list_params.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_list_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_retrieve_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_create_params.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_create_response.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_delete_response.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_list_params.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_list_response.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_retrieve_response.py', '/.venv/Lib/site-packages/openai/resources/skills/__init__.py', '/.venv/Lib/site-packages/openai/resources/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/__pycache__/content.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/__pycache__/skills.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/content.py', '/.venv/Lib/site-packages/openai/resources/skills/skills.py', '/.venv/Lib/site-packages/openai/resources/skills/versions/__init__.py', '/.venv/Lib/site-packages/openai/resources/skills/versions/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/versions/__pycache__/content.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/versions/__pycache__/versions.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/versions/content.py', '/.venv/Lib/site-packages/openai/resources/skills/versions/versions.py', '/.venv/Lib/site-packages/openai/types/skills/__init__.py', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/deleted_skill_version.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/skill_version.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/skill_version_list.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/version_create_params.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/version_list_params.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/deleted_skill_version.py', '/.venv/Lib/site-packages/openai/types/skills/skill_version.py', '/.venv/Lib/site-packages/openai/types/skills/skill_version_list.py', '/.venv/Lib/site-packages/openai/types/skills/version_create_params.py', '/.venv/Lib/site-packages/openai/types/skills/version_list_params.py', '/.venv/Lib/site-packages/openai/types/skills/versions/__init__.py', '/.venv/Lib/site-packages/openai/types/skills/versions/__pycache__/__init__.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/SKILL.md', '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/matching-rules.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md', '/skills/acquiring-discrepancy-analysis/references/status-rules.md', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/bootstrap_source_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/build_matrix_legal_propositions.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/derive_working_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/export_review_xlsx.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/finalize_discrepancy_json.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_coverage_ledger.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_matrix_legal_propositions.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_source_numbering.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_working_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/bootstrap_source_artifacts.py', '/skills/acquiring-discrepancy-analysis/scripts/derive_working_artifacts.py', '/skills/acquiring-discrepancy-analysis/scripts/export_review_xlsx.py', '/skills/acquiring-discrepancy-analysis/scripts/extract_docx_numbered.py', '/skills/acquiring-discrepancy-analysis/scripts/finalize_discrepancy_json.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_coverage_ledger.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py']
AI: Good. Now let me read the key reference files and the existing working artifacts to understand the current state.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/matching-rules.md', 'limit': 200}, 'id': 'call_00_nXyfdgYIIs90tK02DvZF3617', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/status-rules.md', 'limit': 200}, 'id': 'call_01_pQvjVypb8CmAbhbEGrkN6056', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 200}, 'id': 'call_02_Fqw1ie98wkd4dxigUNZw0204', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'offset': 200}, 'id': 'call_00_V3krPrpATUAHIPopsKxo9672', 'type': 'tool_call'}]
Tool:    201	
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
AI: Now let me read the existing working artifacts and the matrix to understand what section 4 contains.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 100}, 'id': 'call_00_46PZlUBXULLaiQgOe15Q4390', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix_legal_propositions.json', 'limit': 100}, 'id': 'call_01_2ZvXTWSBqsQOpmSEg2dB0374', 'type': 'tool_call'}]
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
AI: Now let me find section 4 in the matrix. Let me search for matrix items starting with "4.".[{'name': 'grep', 'args': {'pattern': '"number":"4.', 'path': '/inputs', 'output_mode': 'content'}, 'id': 'call_00_5qn15fdcMRdplMv6Urxy6082', 'type': 'tool_call'}]
Tool: /inputs/matrix.json:
  303:   "number":"4.1.1",
  317:   "number":"4.1.2",
  331:   "number":"4.1.3",
  344:   "number":"4.2.1",
  358:   "number":"4.2.2",
  372:   "number":"4.2.3",
  386:   "number":"4.2.4",
  400:   "number":"4.2.5",
  415:   "number":"4.2.6",
  428:   "number":"4.2.7",
  442:   "number":"4.2.8",
  456:   "number":"4.2.9",
  471:   "number":"4.2.10",
  486:   "number":"4.2.11",
  500:   "number":"4.2.12",
  514:   "number":"4.2.13",
  531:   "number":"4.2.14",
  549:   "number":"4.2.15",
  569:   "number":"4.2.16.1",
  586:   "number":"4.2.16.2",
  600:   "number":"4.2.16.3",
  616:   "number":"4.2.17",
  631:   "number":"4.2.18",
  645:   "number":"4.2.19",
  659:   "number":"4.2.20.1",
  673:   "number":"4.2.20.2",
  689:   "number":"4.2.20.3",
  708:   "number":"4.2.20.4",
  725:   "number":"4.2.20.5",
  739:   "number":"4.2.20.6",
  753:   "number":"4.2.20.7",
  766:   "number":"4.2.21.1",
  779:   "number":"4.2.21.2",
  792:   "number":"4.2.21.3",
  807:   "number":"4.2.21.4",
  821:   "number":"4.2.21.5",
  835:   "number":"4.2.21.6",
  848:   "number":"4.2.21.7",
  861:   "number":"4.2.21.8",
  874:   "number":"4.2.22",
  887:   "number":"4.2.23",
  900:   "number":"4.2.24",
  915:   "number":"4.2.25",
  929:   "number":"4.2.26",
AI: [{'name': 'grep', 'args': {'pattern': '"number":"4.', 'path': '/inputs/matrix.json', 'output_mode': 'content'}, 'id': 'call_00_L9gane5KgBJnvCRKExUj4403', 'type': 'tool_call'}]
Tool: No matches found
AI: [{'name': 'grep', 'args': {'pattern': '"number":"4\\.', 'path': '/inputs/matrix.json', 'output_mode': 'content'}, 'id': 'call_00_JKXIT7h3r5I5gLWwOzS52523', 'type': 'tool_call'}]
Tool: No matches found
AI: [{'name': 'grep', 'args': {'pattern': '"number":"4', 'path': '/inputs/matrix.json', 'output_mode': 'content'}, 'id': 'call_00_S0L8BKC0ODmRLsp4rmod2142', 'type': 'tool_call'}]
Tool: No matches found
AI: [{'name': 'execute', 'args': {'command': 'python -c "import json; data=json.load(open(\'/inputs/matrix.json\')); nums=[r[\'number\'] for r in data]; print([n for n in nums if n.startswith(\'4.\')])"'}, 'id': 'call_00_itiY6GPLZGXtWLrs43Mk4002', 'type': 'tool_call'}]
Tool: ['4.1.1', '4.1.2', '4.1.3', '4.2.1', '4.2.2', '4.2.3', '4.2.4', '4.2.5', '4.2.6', '4.2.7', '4.2.8', '4.2.9', '4.2.10', '4.2.11', '4.2.12', '4.2.13', '4.2.14', '4.2.15', '4.2.16.1', '4.2.16.2', '4.2.16.3', '4.2.17', '4.2.18', '4.2.19', '4.2.20.1', '4.2.20.2', '4.2.20.3', '4.2.20.4', '4.2.20.5', '4.2.20.6', '4.2.20.7', '4.2.21.1', '4.2.21.2', '4.2.21.3', '4.2.21.4', '4.2.21.5', '4.2.21.6', '4.2.21.7', '4.2.21.8', '4.2.22', '4.2.23', '4.2.24', '4.2.25', '4.2.26']

[Command succeeded with exit code 0]
AI: Good. Now let me read the full section 4 from the matrix and the matrix legal propositions. Let me also read the contract and existing working artifacts.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 300, 'limit': 700}, 'id': 'call_00_TXfHdL5H22VCCUtVtgZX8944', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 100}, 'id': 'call_01_HvtsvnphJVHgC1FDlB4C6981', 'type': 'tool_call'}]
Tool:    301	 },
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
   401	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров\/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках\/на Ресурсе, в течение всего рабочего времени Предприятия. Не выдавать по Картам наличные денежные средства[3]. Не принимать от Покупателя более 2 (двух) различных Карт.",
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 100, 'limit': 200}, 'id': 'call_00_0KBBp00d9dHZSfbyBT7f8793', 'type': 'tool_call'}]
Tool:    101	стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных систем, полученные c использованием факсимильной связи, по электронной почте (e-mail);
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 300, 'limit': 200}, 'id': 'call_00_mJfG3jbVCZkxUFkXjgWm9905', 'type': 'tool_call'}]
Tool:    301	Количество необходимых POS-терминалов
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
AI: Now let me read the existing working artifacts to understand the current state of the analysis.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_00_HJHqYGmCaXzRep3mQxAS6385', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_legal_propositions.json', 'limit': 100}, 'id': 'call_01_xY27Wlo7Eai8OFFALyAR3351', 'type': 'tool_call'}]
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
    31	      "id": "1.1",
    32	      "source_text": "По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга) (далее - услуги) в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта, а Заказчик обязуется принять и оплатить указанные услуги в порядке и размере установленном настоящим контрактом. Идентификационный код закупки 251231702678823170100100060016619244.",
    33	      "source_excerpt": "По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга) (далее - услуги) в соответс",
    34	      "type": "operative",
    35	      "materiality": "evaluable",
    36	      "protected_party": "Customer",
    37	      "bound_party": "Bank",
    38	      "right_or_obligation": "obligation",
    39	      "legal_object": "По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги",
    40	      "trigger": "",
    41	      "deadline": "",
    42	      "amount_formula_cap": "",
    43	      "procedure_channel": "",
    44	      "liability_remedy": "",
    45	      "scope_options": [],
    46	      "consequence": "duty imposed",
    47	      "source_locator": "1.1",
    48	      "line_start": 6,
    49	      "line_end": 7,
    50	      "section_context": "г. Сочи «___»________20_ г.",
    51	      "final_allowed": true,
    52	      "evidence_only": false
    53	    },
    54	    {
    55	      "id": "1.2",
    56	      "source_text": "Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.",
    57	      "source_excerpt": "Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.",
    58	      "type": "operative",
    59	      "materiality": "evaluable",
    60	      "protected_party": "Both",
    61	      "bound_party": "Both",
    62	      "right_or_obligation": "mixed",
    63	      "legal_object": "Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.",
    64	      "trigger": "",
    65	      "deadline": "",
    66	      "amount_formula_cap": "",
    67	      "procedure_channel": "",
    68	      "liability_remedy": "",
    69	      "scope_options": [],
    70	      "consequence": "",
    71	      "source_locator": "1.2",
    72	      "line_start": 8,
    73	      "line_end": 8,
    74	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    75	      "final_allowed": true,
    76	      "evidence_only": false
    77	    },
    78	    {
    79	      "id": "1.3",
    80	      "source_text": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.",
    81	      "source_excerpt": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.",
    82	      "type": "operative",
    83	      "materiality": "evaluable",
    84	      "protected_party": "Both",
    85	      "bound_party": "Both",
    86	      "right_or_obligation": "mixed",
    87	      "legal_object": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.",
    88	      "trigger": "",
    89	      "deadline": "",
    90	      "amount_formula_cap": "",
    91	      "procedure_channel": "electronic",
    92	      "liability_remedy": "",
    93	      "scope_options": [],
    94	      "consequence": "",
    95	      "source_locator": "1.3",
    96	      "line_start": 9,
    97	      "line_end": 9,
    98	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    99	      "final_allowed": true,
   100	      "evidence_only": false
AI: Now let me read the matrix legal propositions for section 4 to understand the Bank standard requirements.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nmlp = json.load(open(\'/inputs/matrix_legal_propositions.json\'))\nsec4 = [r for r in mlp[\'matrix\'] if r[\'id\'].startswith(\'4.\')]\nfor r in sec4:\n    print(f\\"ID: {r[\'id\']} | req_type: {r.get(\'required_type\',\'\')} | product: {r[\'applicability_filters\'][\'only_for_product\']} | lot: {r[\'applicability_filters\'][\'only_for_lot\']} | terminal: {r[\'applicability_filters\'][\'only_for_terminal\']} | pm: {r[\'applicability_filters\'][\'payment_method\']}\\")\n    print(f\\"  bank_standard: {r.get(\'bank_standard\',\'\')[:200]}\\")\n    print(f\\"  right_or_obligation: {r.get(\'right_or_obligation\',\'\')[:200]}\\")\n    print(f\\"  legal_object: {r.get(\'legal_object\',\'\')[:200]}\\")\n    print(f\\"  matching_cues: {r.get(\'matching_cues\',[])}\\")\n    print()\n"'}, 'id': 'call_00_7VBQBsa9itriihNwQ2C59770', 'type': 'tool_call'}]
Tool: [stderr] At line:38 char:58
[stderr] +     print(f\"  bank_standard: {r.get('bank_standard','')[:200]}\")
[stderr] +                                                          ~
[stderr] Array index expression is missing or not valid.
[stderr] At line:39 char:70
[stderr] + ... t(f\"  right_or_obligation: {r.get('right_or_obligation','')[:200]}\" ...
[stderr] +                                                                  ~
[stderr] Array index expression is missing or not valid.
[stderr] At line:40 char:56
[stderr] +     print(f\"  legal_object: {r.get('legal_object','')[:200]}\")
[stderr] +                                                        ~
[stderr] Array index expression is missing or not valid.
[stderr] At line:41 char:55
[stderr] +     print(f\"  matching_cues: {r.get('matching_cues',[])}\")
[stderr] +                                                       ~
[stderr] Missing type name after '['.
[stderr] At line:41 char:54
[stderr] +     print(f\"  matching_cues: {r.get('matching_cues',[])}\")
[stderr] +                                                      ~
[stderr] Missing expression after ','.
[stderr] At line:41 char:54
[stderr] +     print(f\"  matching_cues: {r.get('matching_cues',[])}\")
[stderr] +                                                      ~~
[stderr] Unexpected token '[]' in expression or statement.
[stderr] At line:41 char:54
[stderr] +     print(f\"  matching_cues: {r.get('matching_cues',[])}\")
[stderr] +                                                      ~
[stderr] Missing closing ')' in expression.
[stderr] At line:41 char:31
[stderr] +     print(f\"  matching_cues: {r.get('matching_cues',[])}\")
[stderr] +                               ~
[stderr] Missing closing '}' in statement block or type definition.
[stderr] At line:31 char:5
[stderr] + try {
[stderr] +     ~
[stderr] Missing closing '}' in statement block or type definition.
[stderr] At line:41 char:56
[stderr] +     print(f\"  matching_cues: {r.get('matching_cues',[])}\")
[stderr] +                                                        ~
[stderr] The Try statement is missing its Catch or Finally block.
[stderr] Not all parse errors were reported.  Correct the reported errors and try again.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : MissingArrayIndexExpression

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/_sec4_dump.py', 'content': 'import json\n\nmlp = json.load(open(\'/inputs/matrix_legal_propositions.json\'))\nsec4 = [r for r in mlp[\'matrix\'] if r[\'id\'].startswith(\'4.\')]\nfor r in sec4:\n    print(f"ID: {r[\'id\']} | req_type: {r.get(\'required_type\',\'\')} | product: {r[\'applicability_filters\'][\'only_for_product\']} | lot: {r[\'applicability_filters\'][\'only_for_lot\']} | terminal: {r[\'applicability_filters\'][\'only_for_terminal\']} | pm: {r[\'applicability_filters\'][\'payment_method\']}")\n    bs = r.get(\'bank_standard\',\'\')\n    print(f"  bank_standard: {bs[:300]}")\n    ro = r.get(\'right_or_obligation\',\'\')\n    print(f"  right_or_obligation: {ro[:300]}")\n    lo = r.get(\'legal_object\',\'\')\n    print(f"  legal_object: {lo[:300]}")\n    mc = r.get(\'matching_cues\',[])\n    print(f"  matching_cues: {mc}")\n    print()\n'}, 'id': 'call_00_iYynaJiY25tipiMahGus8844', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/_sec4_dump.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/_sec4_dump.py'}, 'id': 'call_00_KZeHRKmMckckGTPuF2P79855', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\_sec4_dump.py", line 3, in <module>
[stderr]     mlp = json.load(open('/inputs/matrix_legal_propositions.json'))
[stderr]                     ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/inputs/matrix_legal_propositions.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "import os; print(os.getcwd())"'}, 'id': 'call_00_KqdC9VaoZxuj6OHhZirv8707', 'type': 'tool_call'}]
Tool: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2

[Command succeeded with exit code 0]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/_sec4_dump.py', 'content': 'import json, os\n\nbase = os.getcwd()\nmlp = json.load(open(os.path.join(base, \'inputs\', \'matrix_legal_propositions.json\')))\nsec4 = [r for r in mlp[\'matrix\'] if r[\'id\'].startswith(\'4.\')]\nfor r in sec4:\n    print(f"ID: {r[\'id\']} | req_type: {r.get(\'required_type\',\'\')} | product: {r[\'applicability_filters\'][\'only_for_product\']} | lot: {r[\'applicability_filters\'][\'only_for_lot\']} | terminal: {r[\'applicability_filters\'][\'only_for_terminal\']} | pm: {r[\'applicability_filters\'][\'payment_method\']}")\n    bs = r.get(\'bank_standard\',\'\')\n    print(f"  bank_standard: {bs[:300]}")\n    ro = r.get(\'right_or_obligation\',\'\')\n    print(f"  right_or_obligation: {ro[:300]}")\n    lo = r.get(\'legal_object\',\'\')\n    print(f"  legal_object: {lo[:300]}")\n    mc = r.get(\'matching_cues\',[])\n    print(f"  matching_cues: {mc}")\n    print()\n'}, 'id': 'call_00_Vf0nd6mR5ox9qV3vAuRv4853', 'type': 'tool_call'}]
Tool: Cannot write to /outputs/working/_sec4_dump.py because it already exists. Read and then make an edit, or write to a new path.
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/_sec4_dump2.py', 'content': 'import json, os\n\nbase = os.getcwd()\nmlp = json.load(open(os.path.join(base, \'inputs\', \'matrix_legal_propositions.json\')))\nsec4 = [r for r in mlp[\'matrix\'] if r[\'id\'].startswith(\'4.\')]\nfor r in sec4:\n    print(f"ID: {r[\'id\']} | req_type: {r.get(\'required_type\',\'\')} | product: {r[\'applicability_filters\'][\'only_for_product\']} | lot: {r[\'applicability_filters\'][\'only_for_lot\']} | terminal: {r[\'applicability_filters\'][\'only_for_terminal\']} | pm: {r[\'applicability_filters\'][\'payment_method\']}")\n    bs = r.get(\'bank_standard\',\'\')\n    print(f"  bank_standard: {bs[:300]}")\n    ro = r.get(\'right_or_obligation\',\'\')\n    print(f"  right_or_obligation: {ro[:300]}")\n    lo = r.get(\'legal_object\',\'\')\n    print(f"  legal_object: {lo[:300]}")\n    mc = r.get(\'matching_cues\',[])\n    print(f"  matching_cues: {mc}")\n    print()\n'}, 'id': 'call_00_eVNoWVKeHernT5i27y4n1285', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/_sec4_dump2.py
AI: [{'name': 'execute', 'args': {'command': 'python outputs/working/_sec4_dump2.py 2>&1 | head -500'}, 'id': 'call_00_DJi1TNIs8Tlb0INZBkWU4319', 'type': 'tool_call'}]
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
[stderr] python outputs/working/_sec4_dump2.py 2>&1 | head -500
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
AI: [{'name': 'execute', 'args': {'command': 'python outputs/working/_sec4_dump2.py'}, 'id': 'call_00_4XyqPzwGM41E6AcKZNQ58288', 'type': 'tool_call'}]
Tool: ID: 4.1.1 | req_type: optional | product: common | lot: common | terminal: common | pm: qr
  bank_standard: Р’Р°Р¶РЅРѕ, РµСЃР»Рё РџСЂРµРґРїСЂРёСЏС‚РёРµ С…РѕС‡РµС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»Р°С… СѓРїРѕРјРёРЅР°РЅРёРµ Р±СЂРµРЅРґР° Р‘Р°РЅРєР° - РЅР°РґРѕ СЃРѕРіР»Р°СЃРѕРІС‹РІР°С‚СЊ СЃ Р‘Р°РЅРєРѕРј
  right_or_obligation: РїСЂР°РІРѕ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РёРјРµРµС‚ РїСЂР°РІРѕ СЃСЃС‹Р»Р°С‚СЊСЃСЏ РЅР° РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚/QR-РєРѕРґР° РїРѕСЃР»Рµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РјР°С‚РµСЂРёР°Р»РѕРІ СЃ Р‘Р°РЅРєРѕРј
  legal_object: РёРјРµРµС‚ РїСЂР°РІРѕ СЃСЃС‹Р»Р°С‚СЊСЃСЏ РЅР° РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚/QR-РєРѕРґР° РїРѕСЃР»Рµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РјР°С‚РµСЂРёР°Р»РѕРІ СЃ Р‘Р°РЅРєРѕРј
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РёРјРµРµС‚ РїСЂР°РІРѕ СЃСЃС‹Р»Р°С‚СЊСЃСЏ РЅР° РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚/QR-РєРѕРґР° РїРѕСЃР»Рµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РјР°С‚РµСЂРёР°Р»РѕРІ СЃ Р‘Р°РЅРєРѕРј', 'РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСѓРЅРєС‚Р°РјРё 2.3.1 Рё 2.3.2', 'Р’Р°Р¶РЅРѕ, РµСЃР»Рё РџСЂРµРґРїСЂРёСЏС‚РёРµ С…РѕС‡РµС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»Р°С… СѓРїРѕРјРёРЅР°РЅРёРµ Р±СЂРµРЅРґР° Р‘Р°РЅРєР° - РЅР°РґРѕ СЃРѕРіР»Р°СЃРѕРІС‹РІР°С‚СЊ СЃ Р‘Р°РЅРєРѕРј']

ID: 4.1.2 | req_type: optional | product: common | lot: common | terminal: common | pm: common
  bank_standard: СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РѕРєР°Р·С‹РІР°РµС‚ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЋ Р·Р°РєР°Р·С‡РёРєР° РїРѕ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЋ РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ
  right_or_obligation: РїСЂРѕС†РµРґСѓСЂР°: РџРѕР»СѓС‡Р°С‚СЊ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЋ РІ Р‘Р°РЅРєРµ РїРѕ РІРѕРїСЂРѕСЃР°Рј СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рё РїСЂРѕРІРµРґРµРЅРёСЋ РћРїРµСЂР°С†РёР№ РїСѓС‚РµРј...
  legal_object: Р·Р°РєСЂРµРїР»РµРЅРѕ РїСЂР°РІРѕ Р—Р°РєР°Р·С‡РёРєР° РЅР° РїРѕР»СѓС‡РµРЅРёРµ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёР№ РїРѕ СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ
  matching_cues: ['Р·Р°РєСЂРµРїР»РµРЅРѕ РїСЂР°РІРѕ Р—Р°РєР°Р·С‡РёРєР° РЅР° РїРѕР»СѓС‡РµРЅРёРµ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёР№ РїРѕ СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р·Р°РєСЂРµРїР»РµРЅРѕ РїСЂР°РІРѕ Р—Р°РєР°Р·С‡РёРєР° РЅР° РїРѕР»СѓС‡РµРЅРёРµ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёР№ РїРѕ РїСЂРѕРІРµРґРµРЅРёСЋ РћРїРµСЂР°С†РёР№', 'СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РѕРєР°Р·С‹РІР°РµС‚ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЋ Р·Р°РєР°Р·С‡РёРєР° РїРѕ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЋ РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ']

ID: 4.1.3 | req_type: optional | product: trade_acquiring | lot: common | terminal: common | pm: qr_sber_pay
  bank_standard: СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ QR РІС‹РґР°С‘С‚ Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РёРјРµРµС‚ РїСЂР°РІРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РїРѕР»СѓС‡РµРЅРЅС‹Рµ РѕС‚ Р‘Р°РЅРєР° QR-РєРѕРґС‹ РґР»СЏ РїСЂРёРµРјР° РїР»Р°С‚РµР¶РµР№ С‡РµСЂРµР· SberPayQR/РџР»Р°С‚Рё QR
  legal_object: РёРјРµРµС‚ РїСЂР°РІРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РїРѕР»СѓС‡РµРЅРЅС‹Рµ РѕС‚ Р‘Р°РЅРєР° QR-РєРѕРґС‹ РґР»СЏ РїСЂРёРµРјР° РїР»Р°С‚РµР¶РµР№ С‡РµСЂРµР· SberPayQR/РџР»Р°С‚Рё QR
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РёРјРµРµС‚ РїСЂР°РІРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РїРѕР»СѓС‡РµРЅРЅС‹Рµ РѕС‚ Р‘Р°РЅРєР° QR-РєРѕРґС‹ РґР»СЏ РїСЂРёРµРјР° РїР»Р°С‚РµР¶РµР№ С‡РµСЂРµР· SberPayQR/РџР»Р°С‚Рё QR', 'СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ QR РІС‹РґР°С‘С‚ Р‘Р°РЅРє']

ID: 4.2.1 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: РїСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё Р±Р°РЅРєР° РїРѕ РІС‹РїРѕР»РЅРµРЅРёСЋ СЂР°СЃС‡С‘С‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј
  legal_object: РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё Р±Р°РЅРєР° РїРѕ РІС‹РїРѕР»РЅРµРЅРёСЋ СЂР°СЃС‡С‘С‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё Р±Р°РЅРєР° РїРѕ РІС‹РїРѕР»РЅРµРЅРёСЋ СЂР°СЃС‡С‘С‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РІРЅРѕСЃРёС‚СЊ РїР»Р°С‚Сѓ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ (РµСЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅР°)']

ID: 4.2.2 | req_type: optional | product: common | lot: common | terminal: common | pm: common
  bank_standard: РІ РєРѕРЅС‚СЂР°РєС‚Рµ РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РІС‹РїРѕР»РЅСЏС‚СЊ Рё СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ РґРѕРіРѕРІРѕСЂР° Рё РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ. Р¤РћСЂРјСѓР»РёСЂРѕРІРєР° Рѕ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё...
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃРѕР±Р»СЋРґР°С‚СЊ РїРѕР»РѕР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° (РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё РѕР± РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґР°С‚СЊ)
  legal_object: РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃРѕР±Р»СЋРґР°С‚СЊ РїРѕР»РѕР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° (РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё РѕР± РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґР°С‚СЊ)
  matching_cues: ['РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃРѕР±Р»СЋРґР°С‚СЊ РїРѕР»РѕР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° (РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё РѕР± РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґР°С‚СЊ)', 'РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІС‹РїРѕР»РЅСЏС‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ, СЃРѕРґРµСЂР¶Р°С‰РёРµСЃСЏ РІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… / РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹С… РјР°С‚РµСЂРёР°Р»Р°С…, РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµРјС‹С… Р‘Р°РЅРєРѕРј (РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё РѕР± РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РІС‹РїРѕР»РЅСЏС‚СЊ)', 'РІ РєРѕРЅС‚СЂР°РєС‚Рµ РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РІС‹РїРѕР»РЅСЏС‚СЊ Рё СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ РґРѕРіРѕРІРѕСЂР° Рё РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ. Р¤РћСЂРјСѓР»РёСЂРѕРІРєР° Рѕ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё']

ID: 4.2.3 | req_type: optional | product: common | lot: fz_223 | terminal: common | pm: common
  bank_standard: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё РґРѕРєСѓРјРµРЅС‚РѕРІ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё РґРѕРєСѓРјРµРЅС‚РѕРІ
  legal_object: СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё РґРѕРєСѓРјРµРЅС‚РѕРІ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РќРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР·РЅР°РєРѕРјР»РµРЅРёРµ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РЅРµРїСЂРёРјРµРЅРµРЅРёСЏ РёР·РјРµРЅРµРЅРёР№']

ID: 4.2.4 | req_type: optional | product: common | lot: common | terminal: common | pm: common
  bank_standard: С„Р°РєС‚, РµСЃР»Рё Р±Р°РЅРє РїРµСЂРµРґР°РµС‚ РїРѕ РґРѕРіРѕРІРѕСЂСѓ РїСЂРµРґРїСЂРёСЏС‚РёСЋ - Р·Р°РєР°Р·С‡РёРєСѓ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, С‚Рѕ Р·Р°РєР°Р·С‡РёРє РґРѕР»Р¶РµРЅ РёС… СЂР°Р·РјРµСЃС‚РёС‚СЊ РЅР° РІРёРґРЅРѕРј РјРµСЃС‚Рµ, РµСЃР»Рё РёРЅС‚РµСЂРЅРµС‚- СЌРєРІР°Р№СЂРёРЅРі С‚Рѕ...
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЂР°Р·РјРµС‰Р°С‚СЊ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ Р‘Р°РЅРєР° Рѕ СЃРїРѕСЃРѕР±Р°С… РѕРїР»Р°С‚С‹
  legal_object: СЂР°Р·РјРµС‰Р°С‚СЊ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ Р‘Р°РЅРєР° Рѕ СЃРїРѕСЃРѕР±Р°С… РѕРїР»Р°С‚С‹
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЂР°Р·РјРµС‰Р°С‚СЊ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ Р‘Р°РЅРєР° Рѕ СЃРїРѕСЃРѕР±Р°С… РѕРїР»Р°С‚С‹', 'Р Р°Р·РјРµС‰РµРЅРёРµ РјР°С‚РµСЂРёР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёР№ СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤', 'С„Р°РєС‚, РµСЃР»Рё Р±Р°РЅРє РїРµСЂРµРґР°РµС‚ РїРѕ РґРѕРіРѕРІРѕСЂСѓ РїСЂРµРґРїСЂРёСЏС‚РёСЋ - Р·Р°РєР°Р·С‡РёРєСѓ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, С‚Рѕ Р·Р°РєР°Р·С‡РёРє РґРѕР»Р¶РµРЅ РёС… СЂР°Р·РјРµСЃС‚РёС‚СЊ РЅР° РІРёРґРЅРѕРј РјРµСЃС‚Рµ, РµСЃР»Рё РёРЅС‚РµСЂРЅРµС‚- СЌРєРІР°Р№СЂРёРЅРі С‚Рѕ']

ID: 4.2.5 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РЅРѕ, РЅРµ РїСЂРёРЅРёРјР°С‚СЊ РѕС‚ РџРѕРєСѓРїР°С‚РµР»СЏ Р±РѕР»РµРµ 2 (РґРІСѓС…) СЂР°Р·Р»РёС‡РЅС‹С… РљР°СЂС‚. РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР°
  right_or_obligation: СЃСЂРѕРє: РџСЂРёРЅРёРјР°С‚СЊ Рє РѕРїР»Р°С‚Рµ РІСЃРµ РєР°СЂС‚С‹ РёР· СЃРїРёСЃРєР° РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РІСЂРµРјРµРЅРё
  legal_object: РџСЂРёРЅРёРјР°С‚СЊ Рє РѕРїР»Р°С‚Рµ РІСЃРµ РєР°СЂС‚С‹ РёР· СЃРїРёСЃРєР° РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РІСЂРµРјРµРЅРё
  matching_cues: ['РџСЂРёРЅРёРјР°С‚СЊ Рє РѕРїР»Р°С‚Рµ РІСЃРµ РєР°СЂС‚С‹ РёР· СЃРїРёСЃРєР° РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РІСЂРµРјРµРЅРё', 'РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅСЊРіРё РїРѕ РєР°СЂС‚Р°Рј', 'РќРµ РїСЂРёРЅРёРјР°С‚СЊ Р±РѕР»РµРµ РґРІСѓС… СЂР°Р·РЅС‹С… РєР°СЂС‚ РѕС‚ РѕРґРЅРѕРіРѕ РїРѕРєСѓРїР°С‚РµР»СЏ', 'Р’Р°Р¶РЅРѕ, РЅРµ РїСЂРёРЅРёРјР°С‚СЊ РѕС‚ РџРѕРєСѓРїР°С‚РµР»СЏ Р±РѕР»РµРµ 2 (РґРІСѓС…) СЂР°Р·Р»РёС‡РЅС‹С… РљР°СЂС‚. РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР°']

ID: 4.2.6 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РЅРµР»СЊР·СЏ СЂР°Р·Р±РёРІР°С‚СЊ РћРїРµСЂР°С†РёСЋ РЅР° РЅРµСЃРєРѕР»СЊРєСѓ СЃСѓРјРј
  right_or_obligation: СЃСѓРјРјР°/С„РѕСЂРјСѓР»Р°: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РћРїРµСЂР°С†РёСЋ РѕРїР»Р°С‚С‹ РµРґРёРЅРѕР№ СЃСѓРјРјРѕР№ Р±РµР· СЂР°Р·РґРµР»РµРЅРёСЏ РЅР° С‡Р°СЃС‚Рё
  legal_object: РїСЂРѕРІРѕРґРёС‚СЊ РћРїРµСЂР°С†РёСЋ РѕРїР»Р°С‚С‹ РµРґРёРЅРѕР№ СЃСѓРјРјРѕР№ Р±РµР· СЂР°Р·РґРµР»РµРЅРёСЏ РЅР° С‡Р°СЃС‚Рё
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РћРїРµСЂР°С†РёСЋ РѕРїР»Р°С‚С‹ РµРґРёРЅРѕР№ СЃСѓРјРјРѕР№ Р±РµР· СЂР°Р·РґРµР»РµРЅРёСЏ РЅР° С‡Р°СЃС‚Рё', 'СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РЅРµР»СЊР·СЏ СЂР°Р·Р±РёРІР°С‚СЊ РћРїРµСЂР°С†РёСЋ РЅР° РЅРµСЃРєРѕР»СЊРєСѓ СЃСѓРјРј']

ID: 4.2.7 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ Р±РµР· РїСЂРёСЃСѓС‚СЃС‚РІРёСЏ РёР»Рё СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏ
  right_or_obligation: РѕР±СЉРµРј: РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ Р±РµР· РїСЂРёСЃСѓС‚СЃС‚РІРёСЏ РёР»Рё СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏ
  legal_object: РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ Р±РµР· РїСЂРёСЃСѓС‚СЃС‚РІРёСЏ РёР»Рё СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏ
  matching_cues: ['РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ Р±РµР· РїСЂРёСЃСѓС‚СЃС‚РІРёСЏ РёР»Рё СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏ', 'Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ С‚РѕР»СЊРєРѕ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№']

ID: 4.2.8 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: С†РµРЅР° РЅРµ Р·Р°РІРёСЃРёС‚ РѕС‚ СЃРїРѕСЃРѕР±Р° РѕРїР»Р°С‚С‹
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РїРѕР»РЅС‹Р№ РЅР°Р±РѕСЂ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РїРѕРєСѓРїР°С‚РµР»СЏРј
  legal_object: РїРѕР»РЅС‹Р№ РЅР°Р±РѕСЂ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РїРѕРєСѓРїР°С‚РµР»СЏРј
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РїРѕР»РЅС‹Р№ РЅР°Р±РѕСЂ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РїРѕРєСѓРїР°С‚РµР»СЏРј', 'С†РµРЅС‹ РґР»СЏ СЂР°СЃС‡РµС‚РѕРІ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј Р±Р°РЅРєРѕРІСЃРєРѕР№ РєР°СЂС‚С‹ РЅРµ РїСЂРµРІС‹С€Р°СЋС‚ С†РµРЅС‹ Р·Р° РЅР°Р»РёС‡РЅС‹Р№ СЂР°СЃС‡РµС‚', 'С†РµРЅР° РЅРµ Р·Р°РІРёСЃРёС‚ РѕС‚ СЃРїРѕСЃРѕР±Р° РѕРїР»Р°С‚С‹']

ID: 4.2.9 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: Р—Р°РєР°Р·С‡РёРє РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РёРЅС„РѕСЂРјР°С†РёСЋ РєРѕС‚РѕСЂСѓСЋ РѕРЅ СѓРєР°Р·С‹РІР°РµС‚ РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїСЂРё РїСЂРѕРІРµРґРµРЅРёРё РїР»Р°С‚РµР¶РµР№
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РѕРїРµСЂР°С†РёРё РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№
  legal_object: РїСЂРѕРІРѕРґРёС‚СЊ РѕРїРµСЂР°С†РёРё РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РѕРїРµСЂР°С†РёРё РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РѕС„РѕСЂРјР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РёРЅС„РѕСЂРјР°С†РёРё РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїРѕ РѕРїРµСЂР°С†РёСЏРј', 'Р—Р°РєР°Р·С‡РёРє РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РёРЅС„РѕСЂРјР°С†РёСЋ РєРѕС‚РѕСЂСѓСЋ РѕРЅ СѓРєР°Р·С‹РІР°РµС‚ РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїСЂРё РїСЂРѕРІРµРґРµРЅРёРё РїР»Р°С‚РµР¶РµР№']

ID: 4.2.10 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё С…СЂР°РЅРµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј, СЃСЂРѕРє РІ С‚РµС‡РµРЅРёРё РєРѕС‚РѕСЂРѕРіРѕ РёС… РЅСѓР¶РЅРѕ С…СЂР°РЅРёС‚СЊ, С„Р°РєС‚ РїРµСЂРµРґР°С‡Рё РєРѕРїРёР№ РїРѕ РѕРїСЂРµРІС†РёСЏСЃ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРє РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂРѕРіРѕ...
  right_or_obligation: СЃСЂРѕРє: С…СЂР°РЅРµРЅРёРµ РґРѕРєСѓРјРµРЅС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј (СЃР°Рј С„Р°РєС‚ С…СЂР°РЅРµРЅРёСЏ Рё СЃСЂРѕРє С…СЂР°РЅРЅРµРёСЏ)
  legal_object: С…СЂР°РЅРµРЅРёРµ РґРѕРєСѓРјРµРЅС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј (СЃР°Рј С„Р°РєС‚ С…СЂР°РЅРµРЅРёСЏ Рё СЃСЂРѕРє С…СЂР°РЅРЅРµРёСЏ)
  matching_cues: ['С…СЂР°РЅРµРЅРёРµ РґРѕРєСѓРјРµРЅС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј (СЃР°Рј С„Р°РєС‚ С…СЂР°РЅРµРЅРёСЏ Рё СЃСЂРѕРє С…СЂР°РЅРЅРµРёСЏ)', 'РїРµСЂРµРґР°С‡Р° РєРѕРїРёР№ РґРѕРєСѓРјРµРЅС‚РѕРІ Р‘Р°РЅРєСѓ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РЅР°РґР»РµР¶Р°С‰РµРµ РєР°С‡РµСЃС‚РІРѕ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ', 'С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё С…СЂР°РЅРµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј, СЃСЂРѕРє РІ С‚РµС‡РµРЅРёРё РєРѕС‚РѕСЂРѕРіРѕ РёС… РЅСѓР¶РЅРѕ С…СЂР°РЅРёС‚СЊ, С„Р°РєС‚ РїРµСЂРµРґР°С‡Рё РєРѕРїРёР№ РїРѕ РѕРїСЂРµРІС†РёСЏСЃ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРє РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂРѕРіРѕ']

ID: 4.2.11 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїРµСЂРµРґР°РІР°С‚СЊ Р·Р°СЏРІР»РµРЅРёРµ Р‘Р°РЅРєСѓ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… РѕРЅРѕ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РїРµСЂРµРґР°РЅРѕ
  right_or_obligation: СЃСЂРѕРє: РџРµСЂРµРґР°С‡Р° Р·Р°СЏРІР»РµРЅРёСЏ РІ Р±Р°РЅРє СЃ РёР·Р»РѕР¶РµРЅРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р·Р°РїСЂРѕСЃР°
  legal_object: РџРµСЂРµРґР°С‡Р° Р·Р°СЏРІР»РµРЅРёСЏ РІ Р±Р°РЅРє СЃ РёР·Р»РѕР¶РµРЅРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р·Р°РїСЂРѕСЃР°
  matching_cues: ['РџРµСЂРµРґР°С‡Р° Р·Р°СЏРІР»РµРЅРёСЏ РІ Р±Р°РЅРє СЃ РёР·Р»РѕР¶РµРЅРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р·Р°РїСЂРѕСЃР°', 'РЅРµРјРµРґР»РµРЅРЅРѕРµ СѓРІРµРґРѕРјР»РµРЅРёРµ Р±Р°РЅРєР° РѕР± СѓС‚СЂР°С‚Рµ РґРѕРєСѓРјРµРЅС‚РѕРІ', 'С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїРµСЂРµРґР°РІР°С‚СЊ Р·Р°СЏРІР»РµРЅРёРµ Р‘Р°РЅРєСѓ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… РѕРЅРѕ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РїРµСЂРµРґР°РЅРѕ']

ID: 4.2.12 | req_type: optional | product: common | lot: common | terminal: common | pm: common
  bank_standard: С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕРґРїРёСЃР°С‚СЊ Р·Р°РєСЂС‹РІР°СЋС‰РёРµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїР»Р°С‚Рµ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… РѕРЅРѕ РґРѕР»Р¶РЅРѕ СЌС‚Рѕ СЃРґРµР»Р°С‚СЊ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ Р°РєС†РµРїС‚РѕРІР°С‚СЊ РїР»Р°С‚РµР¶РЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ Рё СЃС‡РµС‚Р° РЅР° РѕРїР»Р°С‚Сѓ. РџСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РѕРїР»Р°С‚Рµ СЃС‡РµС‚РѕРІ
  legal_object: Р°РєС†РµРїС‚РѕРІР°С‚СЊ РїР»Р°С‚РµР¶РЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ Рё СЃС‡РµС‚Р° РЅР° РѕРїР»Р°С‚Сѓ. РџСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РѕРїР»Р°С‚Рµ СЃС‡РµС‚РѕРІ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ Р°РєС†РµРїС‚РѕРІР°С‚СЊ РїР»Р°С‚РµР¶РЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ Рё СЃС‡РµС‚Р° РЅР° РѕРїР»Р°С‚Сѓ. РџСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РѕРїР»Р°С‚Рµ СЃС‡РµС‚РѕРІ', 'РЎСЂРѕРє РѕРїР»Р°С‚С‹ РїР»Р°С‚РµР¶РЅС‹С… С‚СЂРµР±РѕРІР°РЅРёР№ Рё СЃС‡РµС‚РѕРІ', 'С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕРґРїРёСЃР°С‚СЊ Р·Р°РєСЂС‹РІР°СЋС‰РёРµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїР»Р°С‚Рµ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… РѕРЅРѕ РґРѕР»Р¶РЅРѕ СЌС‚Рѕ СЃРґРµР»Р°С‚СЊ']

ID: 4.2.13 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІРѕР·РјРµС‰Р°С‚СЊ РІСЃРµ СЃСѓРјРјС‹ Рё СѓР±С‹С‚РєРё, РєРѕС‚РѕСЂС‹Рµ Р‘Р°РЅРє РїРѕРЅС‘СЃ РёР·-Р·Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІСЃРµ РІРѕР·РјРµС‰РµРЅРёСЏ - РІ РїРѕР»РЅРѕРј РѕР±СЉРµРјРµ. РЎСЂР°РЅРІРЅРёС‚СЊ СЃР»СѓС‡Р°Рё РІ РєРѕС‚РѕСЂС‹С…...
  right_or_obligation: РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ: РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ, СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡РµС‚Р° Р‘Р°РЅРєР° РІ РїРѕР»СЊР·Сѓ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё Р”РµСЂР¶Р°С‚РµР»РµР№ РєР°СЂС‚
  legal_object: РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ, СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡РµС‚Р° Р‘Р°РЅРєР° РІ РїРѕР»СЊР·Сѓ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё Р”РµСЂР¶Р°С‚РµР»РµР№ РєР°СЂС‚
  matching_cues: ['РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ, СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡РµС‚Р° Р‘Р°РЅРєР° РІ РїРѕР»СЊР·Сѓ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё Р”РµСЂР¶Р°С‚РµР»РµР№ РєР°СЂС‚', 'РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ, СѓРїР»Р°С‡РµРЅРЅС‹С… Р‘Р°РЅРєРѕРј Р‘Р°РЅРєСѓ-СЌРјРёС‚РµРЅС‚Сѓ РёР»Рё Р”РµСЂР¶Р°С‚РµР»СЏРј РєР°СЂС‚', 'РІРѕР·РјРµС‰РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРё СЃРїРѕСЂР°С… Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏС… РїРѕ РѕРїРµСЂР°С†РёСЏРј', 'РІРѕР·РјРµС‰РµРЅРёРµ СЃР±РѕСЂРѕРІ, РєРѕРјРёСЃСЃРёР№ Рё СЂР°СЃС…РѕРґРѕРІ Р‘Р°РЅРєР° РїСЂРё СЂР°СЃСЃРјРѕС‚СЂРµРЅРёРё СЃРїРѕСЂРѕРІ']

ID: 4.2.14 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: С„Р°РєС‚ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґР°СЋС‰РёС… РґРѕРєСѓРјРµРЅС‚РѕРІ, РІР°Р¶РЅС‹ СЃСЂРѕРєРё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ, Р° С‚Р°Рє Р¶Рµ РЅСѓР¶РЅРѕ СЃСЂР°РІРЅРёС‚СЊ СЃРѕР±С‹С‚РёСЏ, РїСЂРё РєРѕС‚РѕСЂС‹С… СЌС‚Рѕ РґРѕРїСѓСЃС‚РёРјРѕ
  right_or_obligation: СЃСЂРѕРє: РёРЅС„РѕСЂРјРёСЂРѕРІР°РЅРёРµ Р‘Р°РЅРєР° Рѕ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№
  legal_object: РёРЅС„РѕСЂРјРёСЂРѕРІР°РЅРёРµ Р‘Р°РЅРєР° Рѕ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№
  matching_cues: ['РёРЅС„РѕСЂРјРёСЂРѕРІР°РЅРёРµ Р‘Р°РЅРєР° Рѕ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёСЏС… РґРѕРєСѓРјРµРЅС‚РѕРІ РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРѕРѕР±С‰РµРЅРёРµ РѕР± РѕС‚РєСЂС‹С‚РёРё РёР»Рё СЃРјРµРЅРµ СЃС‚Р°РґРёРё Р±Р°РЅРєСЂРѕС‚СЃС‚РІР° РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ СЃРІРµРґРµРЅРёР№ Рѕ СЃРјРµРЅРµ СЂСѓРєРѕРІРѕРґСЃС‚РІР° РІ С‚РµС‡РµРЅРёРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№']

ID: 4.2.15 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕСЃС‚РѕРІРµСЂРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ, СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ СЃРІРµРґРµРЅРёР№. Р’Р°Р¶РµРЅ С„Р°РєС‚ Рё СЃСЂРѕРє РїРµСЂРёРѕРґРёС‡РЅРѕРіРѕ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ. Р’Р°Р¶РµРЅ С„Р°РєС‚ Рё СЃСЂРѕРє...
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РЅРµ СЂРµР¶Рµ РѕРґРЅРѕРіРѕ СЂР°Р·Р° РІ РіРѕРґ
  legal_object: РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РЅРµ СЂРµР¶Рµ РѕРґРЅРѕРіРѕ СЂР°Р·Р° РІ РіРѕРґ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РЅРµ СЂРµР¶Рµ РѕРґРЅРѕРіРѕ СЂР°Р·Р° РІ РіРѕРґ', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ СЃРІРµРґРµРЅРёСЏ РїРѕ Р·Р°РїСЂРѕСЃСѓ Р‘Р°РЅРєР° РІ С‚РµС‡РµРЅРёРµ 7 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РЎРІРµРґРµРЅРёСЏ Рѕ С†РµР»СЏС… С„РёРЅР°РЅСЃРѕРІРѕ-С…РѕР·СЏР№СЃС‚РІРµРЅРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё', 'Р�РЅС„РѕСЂРјР°С†РёСЏ Рѕ С„РёРЅР°РЅСЃРѕРІРѕРј РїРѕР»РѕР¶РµРЅРёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ']

ID: 4.2.16.1 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ Р±С‹Р»Рѕ РґРµР№СЃС‚РІСѓСЋС‰РµРµ СЃРѕРіР»Р°СЃРёРµ РЅР° РїРµСЂРµРґР°С‡Сѓ РџР”РЅ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ. РЎРѕСЃС‚Р°РІ РџР”РЅ: Р¤Р�Рћ, Р°РґСЂРµСЃ, РїР°СЃРїРѕСЂС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ. Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РЅРµ Р±С‹Р»Р° РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅР°...
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµРґР°РµС‚ Р¤Р�Рћ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ
  legal_object: РіР°СЂР°РЅС‚РёСЂСѓРµС‚ РЅР°Р»РёС‡РёРµ РїСЂР°РІРѕРІС‹С… РѕСЃРЅРѕРІР°РЅРёР№ РЅР° РїРµСЂРµРґР°С‡Сѓ РџР”РЅ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ РЅР°Р»РёС‡РёРµ РїСЂР°РІРѕРІС‹С… РѕСЃРЅРѕРІР°РЅРёР№ РЅР° РїРµСЂРµРґР°С‡Сѓ РџР”РЅ', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµРґР°РµС‚ Р¤Р�Рћ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµРґР°РµС‚ Р°РґСЂРµСЃ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРµСЂРµРґР°РµС‚ РїР°СЃРїРѕСЂС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ']

ID: 4.2.16.2 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ РєРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ, РІР°Р¶РЅРѕ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№, РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїРѕРґС‚РІРµСЂРґРёС‚СЊ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№, РІР°Р¶РµРЅ СЃРѕСЃС‚Р°РІ РџР”РЅ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ РєРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ, РІР°Р¶РЅРѕ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№, РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїРѕРґС‚РІРµСЂРґРёС‚СЊ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№...
  legal_object: РіР°СЂР°РЅС‚РёСЂСѓРµС‚ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ(РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґС‚РёС‚РµР»Р°) РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РµРіРѕ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РіР°СЂР°РЅС‚РёСЂСѓРµС‚ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ(РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґС‚РёС‚РµР»Р°) РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РµРіРѕ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…', 'РЎРѕСЃС‚Р°РІ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ (РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ)', 'РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ РєРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ, РІР°Р¶РЅРѕ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№, РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїРѕРґС‚РІРµСЂРґРёС‚СЊ РЅР°Р»РёС‡РёРµ СЃРѕРіР»Р°СЃРёР№, РІР°Р¶РµРЅ СЃРѕСЃС‚Р°РІ РџР”РЅ']

ID: 4.2.16.3 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РґР°РЅРЅС‹Рј РїРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј. Р’Р°Р¶РµРЅ СЃСЂРѕРє РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃРѕРіР»Р°СЃРёР№ РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ (РІРєР»СЋС‡Р°СЏ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ) РїРѕ...
  legal_object: РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃРѕРіР»Р°СЃРёР№ РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ (РІРєР»СЋС‡Р°СЏ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ) РїРѕ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃРѕРіР»Р°СЃРёР№ РЅР° РѕР±СЂР°Р±РѕС‚РєСѓ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ (РІРєР»СЋС‡Р°СЏ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ) РїРѕ РїРёСЃСЊРјРµРЅРЅРѕРјСѓ Р·Р°РїСЂРѕСЃСѓ Р±Р°РЅРєР°', 'РЎСЂРѕРєРё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ СЃРѕРіР»Р°СЃРёСЏ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ', 'Р’ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµ СѓСЂРµРіСѓР»РёСЂСѓРµС‚ РїСЂРµС‚РµРЅР·РёРё С‚СЂРµС‚СЊРёС… Р»РёС† Р·Р° СЃРІРѕР№ СЃС‡РµС‚', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РјРµС‰Р°РµС‚ Р‘Р°РЅРєСѓ СѓР±С‹С‚РєРё Рё СЂР°СЃС…РѕРґС‹ РїСЂРё РЅРµРїСЂРµРґСЃС‚Р°РІР»РµРЅРёРё РѕР±РѕСЃРЅРѕРІР°РЅРёСЏ РїРµСЂРµРґР°С‡Рё РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…']

ID: 4.2.17 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґРµРЅРёСЏ СЃС‚Р°РЅРґР°СЂС‚Р°, Р° С‚Р°Рє Р¶Рµ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ PCI DSS
  legal_object: РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ PCI DSS
  matching_cues: ['РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ PCI DSS', 'РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ Р°С‚С‚РµСЃС‚Р°С‚Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РёР»Рё Р»РёСЃС‚Р° СЃР°РјРѕРѕС†РµРЅРєРё РїРѕ Р·Р°РїСЂРѕСЃСѓ Р±Р°РЅРєР°', 'РЈРєР°Р·Р°РЅРЅС‹Р№ email РґР»СЏ РѕС‚РїСЂР°РІРєРё РґРѕРєСѓРјРµРЅС‚РѕРІ:pcidss@sberbank.ru', 'СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґРµРЅРёСЏ СЃС‚Р°РЅРґР°СЂС‚Р°, Р° С‚Р°Рє Р¶Рµ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ']

ID: 4.2.18 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РЅС‹ С„Р°РєС‚С‹ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, Р° С‚Р°Рє Р¶Рµ РІР°Р¶РµРЅ СЃСЂРѕРє
  right_or_obligation: СЃСЂРѕРє: Р’Р°Р¶РЅС‹ С„Р°РєС‚С‹ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, Р° С‚Р°Рє Р¶Рµ РІР°Р¶РµРЅ СЃСЂРѕРє
  legal_object: РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РїСЂРµРєСЂР°С‰РµРЅРёРµ РїСЂРёРµРјР° РєР°СЂС‚ Рє РѕРїР»Р°С‚Рµ (СЂРµРіСѓР»РёСЂСѓРµС‚СЃСЏ РґР°С‚Р° РїСЂРµРєСЂР°С‰РµРЅРёСЏ)
  matching_cues: ['РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РїСЂРµРєСЂР°С‰РµРЅРёРµ РїСЂРёРµРјР° РєР°СЂС‚ Рє РѕРїР»Р°С‚Рµ (СЂРµРіСѓР»РёСЂСѓРµС‚СЃСЏ РґР°С‚Р° РїСЂРµРєСЂР°С‰РµРЅРёСЏ)', 'РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° СЃРЅСЏС‚РёРµ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ Рѕ РїСЂРёРµРјРµ РєР°СЂС‚ (СЂРµРіСѓР»РёСЂСѓРµС‚СЃСЏ РґР°С‚Р° СЃРЅСЏС‚РёСЏ)', 'Р’Р°Р¶РЅС‹ С„Р°РєС‚С‹ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, Р° С‚Р°Рє Р¶Рµ РІР°Р¶РµРЅ СЃСЂРѕРє']

ID: 4.2.19 | req_type: mandatory | product: common | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РµРЅ, С„Р°РєС‚ С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµ РґРѕР»Р¶РЅРѕ РјРµС€Р°С‚СЊ Р‘Р°РЅРєСѓ, Рё С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РґРѕР»Р¶РЅРѕ РїРѕРјРѕРіР°С‚СЊ Р‘Р°РЅРєСѓ РІ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёРё
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІРѕРІР°С‚СЊ РїСЂРѕРІРµСЂРєРµ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р°РЅРєР°
  legal_object: РЅРµ РїСЂРµРїСЏС‚СЃС‚РІРѕРІР°С‚СЊ РїСЂРѕРІРµСЂРєРµ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р°РЅРєР°
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІРѕРІР°С‚СЊ РїСЂРѕРІРµСЂРєРµ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р°РЅРєР°', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРґРµР№СЃС‚РІРѕРІР°С‚СЊ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЋ РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№', 'Р’Р°Р¶РµРЅ, С„Р°РєС‚ С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµ РґРѕР»Р¶РЅРѕ РјРµС€Р°С‚СЊ Р‘Р°РЅРєСѓ, Рё С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РґРѕР»Р¶РЅРѕ РїРѕРјРѕРіР°С‚СЊ Р‘Р°РЅРєСѓ РІ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёРё']

ID: 4.2.20.1 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ СЃР°РјРѕ СЃР»РµРґРёС‚ Р·Р° РїСЂРѕС…РѕР¶РґРµРЅРёРµРј РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё, СЂР°Р·РјРµС‰РµРЅРЅРѕРіРѕ РЅР° СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРѕРІРѕРґРёС‚СЊ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ
  legal_object: РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРѕРІРѕРґРёС‚СЊ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ
  matching_cues: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРѕРІРѕРґРёС‚СЊ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ', 'СЃСЃС‹Р»РєР° РЅР° РёРЅСЃС‚СЂСѓРєС†РёСЋ Рѕ РїРѕСЂСЏРґРєРµ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№', 'СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ СЃР°РјРѕ СЃР»РµРґРёС‚ Р·Р° РїСЂРѕС…РѕР¶РґРµРЅРёРµРј РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё, СЂР°Р·РјРµС‰РµРЅРЅРѕРіРѕ РЅР° СЃР°Р№С‚Рµ Р‘Р°РЅРєР°']

ID: 4.2.20.2 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РїСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїРѕР»СЊР·РѕРІР°Р»Рѕ С‚РµСЂРјРёРЅР°Р»С‹ Рё РџРћ Р‘Р°РЅРєР° С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РїРѕ РјРµСЃС‚Сѓ СѓСЃС‚Р°РЅРѕРІРєРё, РЅРµ РјРµРЅСЏС‚СЊ Рё РЅРµ СЂРµРјРѕРЅС‚РёСЂРѕРІР°С‚СЊ РёС… СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё РЅРµ...
  right_or_obligation: РїСЂРѕС†РµРґСѓСЂР°: Р·Р°РїСЂРµС‚ РїРµСЂРµРґР°С‡Рё РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ Рё РґРѕРєСѓРјРµРЅС‚РѕРІ С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, РєСЂРѕРјРµ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ РѕР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё
  legal_object: РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё СЂРµРіРёСЃС‚СЂР°С†РёРё РўРЎРў/СѓСЃС‚Р°РЅРѕРІРєРё
  matching_cues: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё СЂРµРіРёСЃС‚СЂР°С†РёРё РўРЎРў/СѓСЃС‚Р°РЅРѕРІРєРё СѓСЃС‚СЂРѕР№СЃС‚РІР°', 'Р·Р°РїСЂРµС‚ РІРЅРµСЃРµРЅРёСЏ РёР·РјРµРЅРµРЅРёР№ РІ РџРћ Рё РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ', 'Р·Р°РїСЂРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРіРѕ СЂРµРјРѕРЅС‚Р° РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ', 'Р·Р°РїСЂРµС‚ РїРµСЂРµРґР°С‡Рё РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ Рё РґРѕРєСѓРјРµРЅС‚РѕРІ С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, РєСЂРѕРјРµ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ РѕР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё']

ID: 4.2.20.3 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ СЃС‚РѕРёС‚ Р·Р°РїСЂРµС‚ РЅР° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
  right_or_obligation: РѕР±СЉРµРј: РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»РѕРІ
  legal_object: РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»РѕРІ
  matching_cues: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ РїРѕРґРєР»СЋС‡РµРЅРёСЏ С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ РЅР°СЃС‚СЂРѕР№РєРё С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ СЂРµРјРѕРЅС‚Р° С‚РµСЂРјРёРЅР°Р»РѕРІ']

ID: 4.2.20.4 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РЅРѕ, РµСЃР»Рё СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµ Р±РµР· РґРѕРєСѓРјРµРЅС‚РѕРІ РёР»Рё Р°РєС‚Р° РїРµСЂРµРґР°С‡Рё, С‚Рѕ РІСЃС‘ РѕРє, СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµС‚
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ / РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РІ РїРѕ Р°РєС‚Сѓ
  legal_object: РїСЂРёРЅСЏС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ / РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РІ РїРѕ Р°РєС‚Сѓ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ / РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РІ РїРѕ Р°РєС‚Сѓ', 'РїРѕРґРїРёСЃР°РЅРёРµ Р°РєС‚Р° СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹РјРё Р»РёС†Р°РјРё', 'РЅР°Р»РёС‡РёРµ РґРІСѓС… СЌРєР·РµРјРїР»СЏСЂРѕРІ Р°РєС‚Р°', 'С…СЂР°РЅРµРЅРёРµ РѕРґРЅРѕРіРѕ СЌРєР·РµРјРїР»СЏСЂР° Р°РєС‚Р° РІ РћР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё']

ID: 4.2.20.5 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ Р‘Р°РЅРє Рѕ РІС‹С…РѕРґРµ РёР· СЃС‚СЂРѕСЏ РёР»Рё СѓС‚СЂР°С‚Рµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РёР»Рё РњРѕР±РёР»СЊРЅРѕРіРѕ СѓСЃС‚СЂРѕР№СЃС‚РІР°
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ Р‘Р°РЅРє Рѕ РІС‹С…РѕРґРµ РёР· СЃС‚СЂРѕСЏ РёР»Рё СѓС‚СЂР°С‚Рµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РёР»Рё...
  legal_object: РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ Р‘Р°РЅРє Рѕ РІС‹С…РѕРґРµ РёР· СЃС‚СЂРѕСЏ РёР»Рё СѓС‚СЂР°С‚Рµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РёР»Рё РњРѕР±РёР»СЊРЅРѕРіРѕ
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ Р‘Р°РЅРє Рѕ РІС‹С…РѕРґРµ РёР· СЃС‚СЂРѕСЏ РёР»Рё СѓС‚СЂР°С‚Рµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РёР»Рё РњРѕР±РёР»СЊРЅРѕРіРѕ СѓСЃС‚СЂРѕР№СЃС‚РІР°', 'Р�РЅС„РѕСЂРјРёСЂРѕРІР°РЅРёРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Р°Рј 2.3.1 Рё 2.3.2 Р”РѕРіРѕРІРѕСЂР° РёР»Рё С‡РµСЂРµР· СЃР»СѓР¶Р±Сѓ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР°']

ID: 4.2.20.6 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°
  right_or_obligation: СЃСЂРѕРє: РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°
  legal_object: РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°
  matching_cues: ['РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°', 'РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ/СѓСЃС‚РЅРѕРіРѕ С‚СЂРµР±РѕРІР°РЅРёСЏ Р±Р°РЅРєР°']

ID: 4.2.20.7 | req_type: mandatory | product: trade_acquiring | lot: common | terminal: common | pm: common
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРј РїСѓРЅРєС‚Рµ РґРѕРіРѕРІРѕСЂР° С€Р»Р° СЂРµС‡СЊ РїСЂРѕ С€С‚СЂР°С„ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»Р° Рё РµРіРѕ СЂР°Р·РјРµСЂ, РёРЅР°С‡Рµ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РјР°С‚СЂРёС†С‹ РЅРµ РѕС‚РЅРѕСЃРёС‚СЃСЏ Рє РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°
  right_or_obligation: РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ: РќРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РѕР± СѓРїР»Р°С‚Рµ С€С‚СЂР°С„Р° Р·Р° РЅРµРІРѕР·РІСЂР°С‚
  legal_object: РќРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РѕР± СѓРїР»Р°С‚Рµ С€С‚СЂР°С„Р° Р·Р° РЅРµРІРѕР·РІСЂР°С‚
  matching_cues: ['РќРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РѕР± СѓРїР»Р°С‚Рµ С€С‚СЂР°С„Р° Р·Р° РЅРµРІРѕР·РІСЂР°С‚', 'Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРј РїСѓРЅРєС‚Рµ РґРѕРіРѕРІРѕСЂР° С€Р»Р° СЂРµС‡СЊ РїСЂРѕ С€С‚СЂР°С„ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»Р° Рё РµРіРѕ СЂР°Р·РјРµСЂ, РёРЅР°С‡Рµ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РјР°С‚СЂРёС†С‹ РЅРµ РѕС‚РЅРѕСЃРёС‚СЃСЏ Рє РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°']

ID: 4.2.21.1 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РѕРїРµСЂР°С†РёР№ РЅР° СЂРµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РѕРїРµСЂР°С†РёР№ РЅР° С‚РµСЃС‚РѕРІРѕР№ СЃСЂРµРґРµ
  right_or_obligation: СѓСЃР»РѕРІРёРµ: РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РѕРїРµСЂР°С†РёР№ РЅР° СЂРµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РѕРїРµСЂР°С†РёР№ РЅР° С‚РµСЃС‚РѕРІРѕР№ СЃСЂРµРґРµ
  legal_object: РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РѕРїРµСЂР°С†РёР№ РЅР° СЂРµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РѕРїРµСЂР°С†РёР№ РЅР° С‚РµСЃС‚РѕРІРѕР№ СЃСЂРµРґРµ
  matching_cues: ['РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РѕРїРµСЂР°С†РёР№ РЅР° СЂРµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РѕРїРµСЂР°С†РёР№ РЅР° С‚РµСЃС‚РѕРІРѕР№ СЃСЂРµРґРµ']

ID: 4.2.21.2 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
  legal_object: СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°']

ID: 4.2.21.3 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃСѓРјРј Рє СЃРїРёСЃР°РЅРёСЋ РЅРµ РїРѕР·РґРЅРµРµ 5 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№
  right_or_obligation: СЃСѓРјРјР°/С„РѕСЂРјСѓР»Р°: РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃСѓРјРј Рє СЃРїРёСЃР°РЅРёСЋ РЅРµ РїРѕР·РґРЅРµРµ 5 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№
  legal_object: РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃСѓРјРј Рє СЃРїРёСЃР°РЅРёСЋ РЅРµ РїРѕР·РґРЅРµРµ 5 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№
  matching_cues: ['РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃСѓРјРј Рє СЃРїРёСЃР°РЅРёСЋ РЅРµ РїРѕР·РґРЅРµРµ 5 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№', 'РЎРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРЅРѕР№ СЃСѓРјРјС‹ С„Р°РєС‚РёС‡РµСЃРєРё РѕРєР°Р·Р°РЅРЅС‹Рј С‚РѕРІР°СЂР°Рј/СѓСЃР»СѓРіР°Рј', 'РЎРѕР±Р»СЋРґРµРЅРёРµ РџРѕСЂСЏРґРєР° РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ']

ID: 4.2.21.4 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґРёР·Р°Р№РЅР° РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ СЃ Р‘Р°РЅРєРѕРј
  right_or_obligation: СѓСЃР»РѕРІРёРµ: РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґРёР·Р°Р№РЅР° РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ СЃ Р‘Р°РЅРєРѕРј
  legal_object: РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґРёР·Р°Р№РЅР° РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ СЃ Р‘Р°РЅРєРѕРј
  matching_cues: ['РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґРёР·Р°Р№РЅР° РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ СЃ Р‘Р°РЅРєРѕРј', 'РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ СЌР»РµРєС‚СЂРѕРЅРЅС‹С… РІР°СЂРёР°РЅС‚РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РЅР°РєР»РµРµРє СЃ Р‘Р°РЅРєРѕРј']

ID: 4.2.21.5 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёСЋ Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°
  right_or_obligation: СЃСЂРѕРє: РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёСЋ Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°
  legal_object: РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёСЋ Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёСЋ Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°']

ID: 4.2.21.6 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚
  right_or_obligation: РѕР±СЉРµРј: РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚
  legal_object: РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚
  matching_cues: ['РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚']

ID: 4.2.21.7 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР°
  right_or_obligation: СѓСЃР»РѕРІРёРµ: РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР°
  legal_object: РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР°
  matching_cues: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР°']

ID: 4.2.21.8 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: РЎРѕР±Р»СЋРґРµРЅРёРµ РїСЂР°РІРёР» РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°
  right_or_obligation: РїСЂРѕС†РµРґСѓСЂР°: РЎРѕР±Р»СЋРґР°С‚СЊ РїСЂР°РІРёР»Р° РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
  legal_object: РЎРѕР±Р»СЋРґРµРЅРёРµ РїСЂР°РІРёР» РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°
  matching_cues: ['РЎРѕР±Р»СЋРґРµРЅРёРµ РїСЂР°РІРёР» РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°']

ID: 4.2.22 | req_type: optional | product: trade_acquiring | lot: common | terminal: common | pm: qr
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ QR-РєРѕРґ РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ SberPayQR/РџР»Р°С‚Рё QR (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)
  legal_object: РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ QR-РєРѕРґ РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ SberPayQR/РџР»Р°С‚Рё QR (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ QR-РєРѕРґ РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ SberPayQR/РџР»Р°С‚Рё QR (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)', 'Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ']

ID: 4.2.23 | req_type: optional | product: trade_acquiring | lot: common | terminal: common | pm: qr
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РЅРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)
  legal_object: РЅРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)
  matching_cues: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РЅРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)', 'Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ']

ID: 4.2.24 | req_type: optional | product: common | lot: common | terminal: common | pm: qr
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
  right_or_obligation: РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ: СѓС‡РµС‚ СѓСЃР»РѕРІРёР№ Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїСЂРё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРё QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)
  legal_object: РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API РІ СЂР°РјРєР°С… С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)
  matching_cues: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API РІ СЂР°РјРєР°С… С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'СЃРѕР±Р»СЋРґРµРЅРёРµ РїРѕСЂСЏРґРєР° РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'СѓС‡РµС‚ СѓСЃР»РѕРІРёР№ Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїСЂРё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРё QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API']

ID: 4.2.25 | req_type: optional | product: common | lot: common | terminal: common | pm: qr
  bank_standard: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
  right_or_obligation: РїСЂРѕС†РµРґСѓСЂР°: РџСЂРё РІС‹СЏРІР»РµРЅРёРё С„Р°РєС‚РѕРІ РёР»Рё РїСЂРёР·РЅР°РєРѕРІ РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ РѕСЂРіР°РЅРёР·Р°С†РёРё...
  legal_object: РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API - РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)
  matching_cues: ['РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API - РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API РѕРїРѕРІРµСЃС‚РёС‚СЊ Р‘Р°РЅРєР° (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API']

ID: 4.2.26 | req_type: mandatory | product: internet_acquiring | lot: common | terminal: common | pm: common
  bank_standard: Р’ РґРѕРїРѕР»РЅРµРЅРёРµ Рє СЃРѕР±Р»СЋРґРµРЅРёСЋ С‚СЂРµР±РѕРІР°РЅРёР№, СѓРєР°Р·Р°РЅРЅС‹С… РІ РЈСЃР»РѕРІРёСЏС…, РІ С‚РѕРј С‡РёСЃР»Рµ РїСЂРёР»РѕР¶РµРЅРёСЏС… Рє РЈСЃР»РѕРІРёСЏРј, РІ С†РµР»СЏС… РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ: вЂў...
  right_or_obligation: СЃСѓРјРјР°/С„РѕСЂРјСѓР»Р°: вЂў РїРѕР»СѓС‡Р°С‚СЊ РѕС‚ Р”РµСЂР¶Р°С‚РµР»СЏ СЃРѕРіР»Р°СЃРёРµ РЅР° СЃРѕРІРµСЂС€РµРЅРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№, РІ С‚РѕРј С‡РёСЃР»Рµ СЃ СЃСѓРјРјРѕР№ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№, РїРµСЂРёРѕРґРѕРј...
  legal_object: Р’ РґРѕРїРѕР»РЅРµРЅРёРµ Рє СЃРѕР±Р»СЋРґРµРЅРёСЋ С‚СЂРµР±РѕРІР°РЅРёР№, СѓРєР°Р·Р°РЅРЅС‹С… РІ РЈСЃР»РѕРІРёСЏС…, РІ С‚РѕРј С‡РёСЃР»Рµ РїСЂРёР»РѕР¶РµРЅРёСЏС… Рє РЈСЃР»РѕРІРёСЏРј, РІ С†РµР»СЏС… РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ
  matching_cues: ['Р’ РґРѕРїРѕР»РЅРµРЅРёРµ Рє СЃРѕР±Р»СЋРґРµРЅРёСЋ С‚СЂРµР±РѕРІР°РЅРёР№, СѓРєР°Р·Р°РЅРЅС‹С… РІ РЈСЃР»РѕРІРёСЏС…, РІ С‚РѕРј С‡РёСЃР»Рµ РїСЂРёР»РѕР¶РµРЅРёСЏС… Рє РЈСЃР»РѕРІРёСЏРј, РІ С†РµР»СЏС… РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ: вЂў']


[Command succeeded with exit code 0]
AI: Now I have a comprehensive picture. Let me set up my task plan and begin the analysis. The contract is a 44-FZ public procurement contract for trade acquiring (POS terminals + smart terminals). Let me now systematically work through each matrix item in section 4.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Apply product profile filters to section 4 matrix items - classify out_of_scope items', 'status': 'in_progress'}, {'content': 'Build matrix-to-contract links for 4.1.x (rights) items', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.1-4.2.9 (core obligations)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.10-4.2.15 (document/notice obligations)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.16.1-4.2.16.3 (PDn obligations)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.17-4.2.19 (PCI DSS, termination, anti-fraud)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.20.x (trade acquiring specific)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.21.x (internet acquiring - out of scope)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.22-4.2.26 (QR, API, recurring payments)', 'status': 'pending'}, {'content': 'Contract-to-matrix pass for section 5 contract clauses', 'status': 'pending'}, {'content': 'Write final batch JSON fragment to /outputs/working/batch_section4.json', 'status': 'pending'}]}, 'id': 'call_00_gGYGtZHfHUDF5lYJQqRD6143', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Apply product profile filters to section 4 matrix items - classify out_of_scope items', 'status': 'in_progress'}, {'content': 'Build matrix-to-contract links for 4.1.x (rights) items', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.1-4.2.9 (core obligations)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.10-4.2.15 (document/notice obligations)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.16.1-4.2.16.3 (PDn obligations)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.17-4.2.19 (PCI DSS, termination, anti-fraud)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.20.x (trade acquiring specific)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.21.x (internet acquiring - out of scope)', 'status': 'pending'}, {'content': 'Build matrix-to-contract links for 4.2.22-4.2.26 (QR, API, recurring payments)', 'status': 'pending'}, {'content': 'Contract-to-matrix pass for section 5 contract clauses', 'status': 'pending'}, {'content': 'Write final batch JSON fragment to /outputs/working/batch_section4.json', 'status': 'pending'}]
AI: Let me first apply the product profile filters. The contract profile is:
- Product: trade_acquiring
- Lot: 44_fz
- Terminal: pos_terminal, smart_terminal
- Payment methods: cards, qr, nfc
- Legal regime: 44_fz

Now let me classify each matrix item:

**Out of scope (product filter):**
- 4.2.17: only_for_product = internet_acquiring → out_of_scope
- 4.2.21.1-4.2.21.8: only_for_product = internet_acquiring → out_of_scope
- 4.2.26: only_for_product = internet_acquiring → out_of_scope

**Out of scope (payment_method filter):**
- 4.1.1: payment_method = qr → but contract has QR capability. Let me check: the contract profile says payment_method includes "qr". So 4.1.1 is applicable.
- 4.1.3: payment_method = qr_sber_pay → contract has QR but not specifically SberPay. The profile says no SberPay. So 4.1.3 is out_of_scope (qr_sber_pay not in contract payment methods).
- 4.2.22: payment_method = qr → applicable (contract has QR)
- 4.2.23: payment_method = qr → applicable
- 4.2.24: payment_method = qr → applicable
- 4.2.25: payment_method = qr → applicable

**Out of scope (lot filter):**
- 4.2.3: only_for_lot = fz_223 → contract is 44_fz, not 223_fz → out_of_scope

Now let me proceed with the detailed matching. Let me read the contract clauses more carefully for the relevant sections.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_legal_propositions.json', 'offset': 100, 'limit': 300}, 'id': 'call_00_b729by7cfSg2ise5HtNu8433', 'type': 'tool_call'}]
Tool:    101	    },
   102	    {
   103	      "id": "2",
   104	      "source_text": "ТЕРМИНЫ, ОПРЕДЕЛЕНИЯ И ВЗАИМОДЕЙСТВИЕ",
   105	      "source_excerpt": "ТЕРМИНЫ, ОПРЕДЕЛЕНИЯ И ВЗАИМОДЕЙСТВИЕ",
   106	      "type": "heading",
   107	      "materiality": "heading",
   108	      "protected_party": "",
   109	      "bound_party": "",
   110	      "right_or_obligation": "",
   111	      "legal_object": "",
   112	      "trigger": "",
   113	      "deadline": "",
   114	      "amount_formula_cap": "",
   115	      "procedure_channel": "",
   116	      "liability_remedy": "",
   117	      "scope_options": [],
   118	      "consequence": "",
   119	      "source_locator": "2",
   120	      "line_start": 10,
   121	      "line_end": 10,
   122	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   123	      "final_allowed": false,
   124	      "evidence_only": true
   125	    },
   126	    {
   127	      "id": "2.1",
   128	      "source_text": "Авторизация – процедура получения разрешения от банка-эмитента или иного юридического лица, действующего от его имени, на проведение операции;",
   129	      "source_excerpt": "Авторизация – процедура получения разрешения от банка-эмитента или иного юридического лица, действующего от его имени, на проведение операции;",
   130	      "type": "definition",
   131	      "materiality": "not_material",
   132	      "protected_party": "",
   133	      "bound_party": "",
   134	      "right_or_obligation": "",
   135	      "legal_object": "",
   136	      "trigger": "",
   137	      "deadline": "",
   138	      "amount_formula_cap": "",
   139	      "procedure_channel": "",
   140	      "liability_remedy": "",
   141	      "scope_options": [],
   142	      "consequence": "",
   143	      "source_locator": "2.1",
   144	      "line_start": 11,
   145	      "line_end": 11,
   146	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   147	      "final_allowed": false,
   148	      "evidence_only": true
   149	    },
   150	    {
   151	      "id": "2.1.1",
   152	      "source_text": "банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы, являющаяся электронным средством платежа. Для совершения операций в ТСТ. Карта может быть представлена на физическом носителе, путем указания её реквизитов, а также через мобильное устройство, которое позволяет его покупателю совершать операции по технологии беспроводной высокочастотной связи малого радиуса действия (NFC);",
   153	      "source_excerpt": "банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы, являющаяся электронным средством платежа. Для совершения операций в ТСТ. Карта может быть представлена на физическом носител",
   154	      "type": "definition",
   155	      "materiality": "not_material",
   156	      "protected_party": "",
   157	      "bound_party": "",
   158	      "right_or_obligation": "",
   159	      "legal_object": "",
   160	      "trigger": "",
   161	      "deadline": "",
   162	      "amount_formula_cap": "",
   163	      "procedure_channel": "",
   164	      "liability_remedy": "",
   165	      "scope_options": [],
   166	      "consequence": "",
   167	      "source_locator": "2.1.1",
   168	      "line_start": 12,
   169	      "line_end": 12,
   170	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   171	      "final_allowed": false,
   172	      "evidence_only": true
   173	    },
   174	    {
   175	      "id": "2.1.2",
   176	      "source_text": "банк-эквайрер - кредитная организация, являющаяся участником платежной системы, организующая точки приема карт и осуществляющая весь комплекс финансовых операций, связанных с выполнением расчетов и платежей по картам в этих точках;",
   177	      "source_excerpt": "банк-эквайрер - кредитная организация, являющаяся участником платежной системы, организующая точки приема карт и осуществляющая весь комплекс финансовых операций, связанных с выполнением расчетов и платежей по картам в этих точках;",
   178	      "type": "definition",
   179	      "materiality": "not_material",
   180	      "protected_party": "",
   181	      "bound_party": "",
   182	      "right_or_obligation": "",
   183	      "legal_object": "",
   184	      "trigger": "",
   185	      "deadline": "",
   186	      "amount_formula_cap": "",
   187	      "procedure_channel": "",
   188	      "liability_remedy": "",
   189	      "scope_options": [],
   190	      "consequence": "",
   191	      "source_locator": "2.1.2",
   192	      "line_start": 13,
   193	      "line_end": 13,
   194	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   195	      "final_allowed": false,
   196	      "evidence_only": true
   197	    },
   198	    {
   199	      "id": "2.1.3",
   200	      "source_text": "банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;",
   201	      "source_excerpt": "банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;",
   202	      "type": "definition",
   203	      "materiality": "not_material",
   204	      "protected_party": "",
   205	      "bound_party": "",
   206	      "right_or_obligation": "",
   207	      "legal_object": "",
   208	      "trigger": "",
   209	      "deadline": "",
   210	      "amount_formula_cap": "",
   211	      "procedure_channel": "",
   212	      "liability_remedy": "",
   213	      "scope_options": [],
   214	      "consequence": "",
   215	      "source_locator": "2.1.3",
   216	      "line_start": 14,
   217	      "line_end": 14,
   218	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   219	      "final_allowed": false,
   220	      "evidence_only": true
   221	    },
   222	    {
   223	      "id": "2.1.4",
   224	      "source_text": "возврат платежа – операция, инициируемая банком-эмитентом в соответствии с правилами платежной системы и оспаривающая предъявленную банком-эквайрером операцию (транзакцию). Результатом операции «Возврат платежа» является списание денежных средств со счета банка-эквайрера и зачисление на счет банка-эмитента;",
   225	      "source_excerpt": "возврат платежа – операция, инициируемая банком-эмитентом в соответствии с правилами платежной системы и оспаривающая предъявленную банком-эквайрером операцию (транзакцию). Результатом операции «Возврат платежа» является списание денежных с",
   226	      "type": "definition",
   227	      "materiality": "not_material",
   228	      "protected_party": "",
   229	      "bound_party": "",
   230	      "right_or_obligation": "",
   231	      "legal_object": "",
   232	      "trigger": "",
   233	      "deadline": "",
   234	      "amount_formula_cap": "",
   235	      "procedure_channel": "",
   236	      "liability_remedy": "",
   237	      "scope_options": [],
   238	      "consequence": "",
   239	      "source_locator": "2.1.4",
   240	      "line_start": 15,
   241	      "line_end": 15,
   242	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   243	      "final_allowed": false,
   244	      "evidence_only": true
   245	    },
   246	    {
   247	      "id": "2.1.5",
   248	      "source_text": "держатель карты (держатель) – покупатель-физическое лицо, на имя которого выпущена карта;",
   249	      "source_excerpt": "держатель карты (держатель) – покупатель-физическое лицо, на имя которого выпущена карта;",
   250	      "type": "definition",
   251	      "materiality": "not_material",
   252	      "protected_party": "",
   253	      "bound_party": "",
   254	      "right_or_obligation": "",
   255	      "legal_object": "",
   256	      "trigger": "",
   257	      "deadline": "",
   258	      "amount_formula_cap": "",
   259	      "procedure_channel": "",
   260	      "liability_remedy": "",
   261	      "scope_options": [],
   262	      "consequence": "",
   263	      "source_locator": "2.1.5",
   264	      "line_start": 16,
   265	      "line_end": 16,
   266	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   267	      "final_allowed": false,
   268	      "evidence_only": true
   269	    },
   270	    {
   271	      "id": "2.1.6",
   272	      "source_text": "документ по операции - документ на бумажном носителе или в электронном виде, являющийся основанием для осуществления расчетов по операциям, совершенным с использованием карты;",
   273	      "source_excerpt": "документ по операции - документ на бумажном носителе или в электронном виде, являющийся основанием для осуществления расчетов по операциям, совершенным с использованием карты;",
   274	      "type": "definition",
   275	      "materiality": "not_material",
   276	      "protected_party": "",
   277	      "bound_party": "",
   278	      "right_or_obligation": "",
   279	      "legal_object": "",
   280	      "trigger": "",
   281	      "deadline": "",
   282	      "amount_formula_cap": "",
   283	      "procedure_channel": "",
   284	      "liability_remedy": "",
   285	      "scope_options": [],
   286	      "consequence": "",
   287	      "source_locator": "2.1.6",
   288	      "line_start": 17,
   289	      "line_end": 17,
   290	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   291	      "final_allowed": false,
   292	      "evidence_only": true
   293	    },
   294	    {
   295	      "id": "2.1.7",
   296	      "source_text": "код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации;",
   297	      "source_excerpt": "код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации;",
   298	      "type": "definition",
   299	      "materiality": "not_material",
   300	      "protected_party": "",
   301	      "bound_party": "",
   302	      "right_or_obligation": "",
   303	      "legal_object": "",
   304	      "trigger": "",
   305	      "deadline": "",
   306	      "amount_formula_cap": "",
   307	      "procedure_channel": "",
   308	      "liability_remedy": "",
   309	      "scope_options": [],
   310	      "consequence": "",
   311	      "source_locator": "2.1.7",
   312	      "line_start": 18,
   313	      "line_end": 18,
   314	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   315	      "final_allowed": false,
   316	      "evidence_only": true
   317	    },
   318	    {
   319	      "id": "2.1.8",
   320	      "source_text": "контрольно-кассовая техника (ККТ) – программно-технические средства и их комплексы, обеспечивающие запись и хранение фискальных данных в фискальных накопителях, формирующие фискальные документы, обеспечивающие передачу фискальных документов в налоговые органы через оператора фискальных данных и печать фискальных документов на бумажных носителях в соответствии с правилами, установленными законодательством Российской Федерации о применении контрольно-кассовой техники; 2.1.9.контрольная лента - отчет, распечатываемый на электронном терминале и содержащий информацию о транзакциях, совершенных в ТСТ на электронном терминале за определенный период; 2.1.10.отложенный платеж - операция оплаты, осуществляемая на основании полученного от Заказчика/ТСТ сообщения, направленного с использованием электронного терминала, о наличии задолженности покупателя перед Заказчиком/ТСТ, после окончательного расчета; 2.1.11.операция – действие, осуществляемое Заказчиком/ТСТ/покупателем на электронном терминале, в том числе операция оплаты, операция отмены, операция возврата, совершенная с использованием карты/реквизитов карты/NFС-карты/ без предъявления карты; 2.1.12.операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;",
   321	      "source_excerpt": "контрольно-кассовая техника (ККТ) – программно-технические средства и их комплексы, обеспечивающие запись и хранение фискальных данных в фискальных накопителях, формирующие фискальные документы, обеспечивающие передачу фискальных документов",
   322	      "type": "definition",
   323	      "materiality": "not_material",
   324	      "protected_party": "",
   325	      "bound_party": "",
   326	      "right_or_obligation": "",
   327	      "legal_object": "",
   328	      "trigger": "",
   329	      "deadline": "",
   330	      "amount_formula_cap": "",
   331	      "procedure_channel": "",
   332	      "liability_remedy": "",
   333	      "scope_options": [],
   334	      "consequence": "",
   335	      "source_locator": "2.1.8",
   336	      "line_start": 19,
   337	      "line_end": 23,
   338	      "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   339	      "final_allowed": false,
   340	      "evidence_only": true
   341	    },
   342	    {
   343	      "id": "2.1.13",
   344	      "source_text": "операция отмены – операция, выполняемая Заказчиком/ТСТ на электронном терминале/смарт-терминале, с целью отмены авторизации. Операция отмены авторизации выполняется до проведения операции «Сверка итогов»;",
   345	      "source_excerpt": "операция отмены – операция, выполняемая Заказчиком/ТСТ на электронном терминале/смарт-терминале, с целью отмены авторизации. Операция отмены авторизации выполняется до проведения операции «Сверка итогов»;",
   346	      "type": "definition",
   347	      "materiality": "not_material",
   348	      "protected_party": "",
   349	      "bound_party": "",
   350	      "right_or_obligation": "",
   351	      "legal_object": "",
   352	      "trigger": "",
   353	      "deadline": "",
   354	      "amount_formula_cap": "",
   355	      "procedure_channel": "",
   356	      "liability_remedy": "",
   357	      "scope_options": [],
   358	      "consequence": "",
   359	      "source_locator": "2.1.13",
   360	      "line_start": 24,
   361	      "line_end": 24,
   362	      "section_context": "2.1.12.операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;",
   363	      "final_allowed": false,
   364	      "evidence_only": true
   365	    },
   366	    {
   367	      "id": "2.1.14",
   368	      "source_text": "операция возврата – операция, оформляемая Заказчиком/ТСТ при возврате товаров/отказе от услуг или от части товаров/услуг, оплаченных картой, после проведения операции «Сверка итогов», следствием которой является возврат суммы операции оплаты или ее части на карту, предъявленную покупателем;",
   369	      "source_excerpt": "операция возврата – операция, оформляемая Заказчиком/ТСТ при возврате товаров/отказе от услуг или от части товаров/услуг, оплаченных картой, после проведения операции «Сверка итогов», следствием которой является возврат суммы операции оплат",
   370	      "type": "definition",
   371	      "materiality": "not_material",
   372	      "protected_party": "",
   373	      "bound_party": "",
   374	      "right_or_obligation": "",
   375	      "legal_object": "",
   376	      "trigger": "",
   377	      "deadline": "",
   378	      "amount_formula_cap": "",
   379	      "procedure_channel": "",
   380	      "liability_remedy": "",
   381	      "scope_options": [],
   382	      "consequence": "",
   383	      "source_locator": "2.1.14",
   384	      "line_start": 25,
   385	      "line_end": 25,
   386	      "section_context": "2.1.12.операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;",
   387	      "final_allowed": false,
   388	      "evidence_only": true
   389	    },
   390	    {
   391	      "id": "2.1.15",
   392	      "source_text": "платежная система – совокупность организаций, взаимодействующих по правилам платежной системы в целях осуществления перевода денежных средств;",
   393	      "source_excerpt": "платежная система – совокупность организаций, взаимодействующих по правилам платежной системы в целях осуществления перевода денежных средств;",
   394	      "type": "definition",
   395	      "materiality": "not_material",
   396	      "protected_party": "",
   397	      "bound_party": "",
   398	      "right_or_obligation": "",
   399	      "legal_object": "",
   400	      "trigger": "",
AI: Let me now look at the contract clauses that are relevant for section 4 matching - specifically the obligations of the Customer (section 5.3) and the rights of the Customer (section 5.4).[{'name': 'execute', 'args': {'command': 'python -c "import json; clp=json.load(open(\'outputs/working/contract_legal_propositions.json\')); ids=[r[\'id\'] for r in clp[\'contract\'] if r[\'id\'].startswith(\'5.\')]; print(ids)"'}, 'id': 'call_00_nqvCppmokGG6Nk4a2wRh6741', 'type': 'tool_call'}]
Tool: ['5.1.1', '5.1.2', '5.1.3', '5.1.4', '5.1.5', '5.1.6', '5.1.7', '5.1.8', '5.1.9', '5.1.10', '5.2', '5.2.1', '5.2.2', '5.2.3', '5.2.4', '5.2.5', '5.2.6', '5.2.7', '5.2.8', '5.2.9', '5.2.9.1', '5.2.9.2', '5.2.9.9', '5.2.9.10', '5.2.9.11', '5.2.10', '5.2.10.1', '5.2.10.2', '5.2.10.3', '5.2.10.4', '5.2.10.5', '5.3', '5.3.1', '5.3.2', '5.3.3', '5.3.4', '5.3.5', '5.3.6', '5.3.7', '5.3.8', '5.3.9', '5.3.10', '5.3.11', '5.3.12', '5.3.13', '5.3.14', '5.3.15', '5.3.16', '5.3.17', '5.3.18', '5.3.18.1', '5.3.18.2', '5.3.18.3', '5.3.20.4', '5.3.18.5', '5.3.19', '5.3.20', '5.4', '5.4.1', '5.4.2', '5.4.3', '5.4.4', '5.4.5', '5.5', '5.6', '5.7', '5.9', '5.10']

[Command succeeded with exit code 0]

