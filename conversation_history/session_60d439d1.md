## Summarized at 2026-06-26T09:49:15.743699+00:00

Human: Matrix batch 2: items 4.2.22 through 7.17
AI: I'll start by reading the skill file and understanding the task structure, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_GOHYGTBc3j9VGDoQqIzp5075', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/*', 'path': '/'}, 'id': 'call_01_SmoWU78RRDmJmDdYE9Vl5418', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-discrepancy-analysis
     3	description: "Use this skill whenever you need to compare an acquiring bank's standard requirements matrix against a counterparty acquiring contract: find missing contract terms, deviations from the Bank standard, aligned legal coverage, and material contract-only terms. Trigger on requests such as matrix vs contract comparison, acquiring contract review, discrepancy analysis, what's missing in the contract, or many-to-many legal coverage between a bank standard matrix and a counterparty agreement."
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
    20	  grouped coverage, weak-candidate rejection, hard terms, and risk status.
    21	- Read `references/output-contract.md` before writing or validating final
    22	  artifacts. It is the field contract for JSON and XLSX outputs.
    23	
    24	## Quick Start
    25	
    26	1. Preflight `inputs/contract.txt`; stop with a source error artifact if the
    27	   text is not legally usable.
    28	2. Build `clause_index.json` as the complete source map.
    29	3. Build and validate `legal_propositions.json`; do not start matching until
    30	   `working_artifact_validation.json` is valid.
    31	4. Build the contract product profile and close out-of-scope matrix rows only
    32	   in the internal ledger.
    33	5. Read `references/matching-rules.md`; compare both directions: matrix
    34	   requirements to contract package, and material contract terms back to matrix
    35	   analogues.
    36	6. Read `references/status-rules.md`; assign group-level `aligned`,
    37	   `deviation`, `missing_in_contract`, or `extra_in_contract` based on source
    38	   text.
    39	7. Run Final QA, then write one final JSON and the mechanical XLSX export.
    40	
    41	## Purpose
    42	
    43	Find and explain:
    44	
    45	- Bank-standard matrix requirements preserved by the contract;
    46	- true analogues that deviate from the Bank standard;
    47	- applicable matrix requirements absent from the contract;
    48	- legally meaningful contract terms with no matrix analogue.
    49	- matrix requirements that are out of scope for the current contract profile,
    50	  closed in the internal ledger without final risk reporting.
    51	
    52	The review is risk-oriented. Missing a real risk is worse than marking a
    53	borderline issue as `deviation`, but weak thematic matches must not be promoted
    54	into legal links.
    55	
    56	## Inputs And Outputs
    57	
    58	Inputs:
    59	
    60	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    61	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    62	  applicability filters.
    63	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    64	  ids or real document locators visible in this file.
    65	
    66	Final outputs:
    67	
    68	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    69	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    70	
    71	Working artifacts belong under `/outputs/working/`.
    72	
    73	## Source Hierarchy
    74	
    75	Use the source text as the legal authority:
    76	
    77	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    78	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    79	3. Working ledgers as indexes and evidence aids.
    80	
    81	Do not decide status from extracted fields alone. When a status depends on a
    82	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    83	consequence, re-read the source text. Extracted fields are useful for recall,
    84	but they can omit facts that appear in related clauses; source text controls
    85	the legal conclusion.
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
   205	
   206	## Matching Method
   207	
   208	Read and follow `references/matching-rules.md` before matching. The short rule:
   209	final links require true legal analogues, not broad topic overlap. Perform both
   210	directions:
   211	
   212	- matrix to contract: find the contract package that covers each applicable
   213	  Bank-standard requirement;
   214	- contract to matrix: find matrix analogues for each material contract term or
   215	  classify it as `extra_in_contract`;
   216	- keep weak candidates out of final `links`; use them only as rejected
   217	  candidates or reasoning;
   218	- group ids only when they form one legal package.
   219	
   220	Use `references/comparison-patterns.md` for calibration examples such as weak
   221	candidate rejection, parent/child package retention, contract-only materiality,
   222	and grouped coverage.
   223	
   224	## Status And Risk Method
   225	
   226	Read and follow `references/status-rules.md` before status classification. The
   227	short rule: status is group-level and source-text based.
   228	
   229	- `aligned`: the contract package preserves the matrix legal result.
   230	- `deviation`: a true analogue exists, but a material element is changed,
   231	  narrowed, weakened, omitted, shifted, or blank.
   232	- `missing_in_contract`: no true contract analogue exists for an applicable
   233	  matrix requirement.
   234	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   235	  analogue.
   236	- `not_material`, `out_of_scope`, and `not_applicable` are internal ledger
   237	  closures unless the output contract says otherwise.
   238	
   239	Compare hard terms directly: deadlines, amounts, formulas, caps, penalties,
   240	protected parties, triggers, procedures, liability, remedies, and consequences.
   241	Formal labels and mandatory-law mechanics do not create `deviation` when the
   242	legal result is preserved.
   243	
   244	## Final QA
   245	
   246	Before writing final artifacts, perform release checks over already-built
   247	artifacts. Do not use Final QA as the first pass over missing working data.
   248	
   249	Blocking checks; repair before final JSON:
   250	
   251	- verify `clause_index` covers all source ids;
   252	- verify `outputs/working/working_artifact_validation.json` exists and is
   253	  valid; if it is missing or invalid, return to the Legal Proposition Ledger
   254	  stage instead of patching only the final JSON;
   255	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   256	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   257	  `coverage_ledger`;
   258	- verify every applicable evaluable matrix id is linked or in
   259	  `unmatched_matrix`;
   260	- verify out-of-scope / non-applicable matrix ids are not in final
   261	  `unmatched_matrix`;
   262	- verify every material contract id is closed as linked or extra;
   263	- verify `coverage_ledger` is derived from final `links`,
   264	  `unmatched_matrix`, and `unmatched_contract`;
   265	- verify every final id is visible in source text;
   266	- verify `aligned` has no material discrepancy;
   267	- verify every `deviation` has a named legal gap and evidence;
   268	- verify weak candidates are not in final `links`;
   269	- verify non-material contract rows are absent from final `unmatched_contract`;
   270	- verify summary counts equal final arrays.
   271	
   272	Advisory cleanup; fix when practical, but do not rewrite legal conclusions
   273	without source support:
   274	
   275	- keep quotes concise;
   276	- keep risk explanations specific to the Bank;
   277	- keep XLSX as a mechanical export from JSON;
   278	- keep working files under `/outputs/working/`.
   279	
   280	## Output Discipline
   281	
   282	Read and follow `references/output-contract.md` before writing any final
   283	artifact. Do not duplicate or reinterpret the field contract locally.
   284	
   285	`links` carry group-level legal findings. `atomic_links` are traceability
   286	projections only and must inherit the group relationship. Do not assign
   287	separate final pair-level statuses.
   288	
   289	## Tools And Scripts
   290	
   291	Use helper scripts for mechanical work: source extraction, indexing,
   292	normalization checks, batch completeness, coverage validation, JSON schema
   293	checks, and Excel export. Do not put legal mapping or status decisions into
   294	hardcoded scripts.
   295	
   296	Required scripts live under `skills/acquiring-discrepancy-analysis/scripts/`
   297	and run with the project Python environment. If a script fails because of a
   298	path or environment issue, repair the command/path and rerun it. If a required
   299	validator is genuinely unavailable, do not skip the gate: perform the same
   300	mechanical checks manually, write the expected validation report under
   301	`/outputs/working/`, and state that the fallback was used.
Tool: ['/.env', '/.git/COMMIT_EDITMSG', '/.git/FETCH_HEAD', '/.git/HEAD', '/.git/ORIG_HEAD', '/.git/config', '/.git/description', '/.git/hooks/applypatch-msg.sample', '/.git/hooks/commit-msg.sample', '/.git/hooks/fsmonitor-watchman.sample', '/.git/hooks/post-update.sample', '/.git/hooks/pre-applypatch.sample', '/.git/hooks/pre-commit.sample', '/.git/hooks/pre-merge-commit.sample', '/.git/hooks/pre-push.sample', '/.git/hooks/pre-rebase.sample', '/.git/hooks/pre-receive.sample', '/.git/hooks/prepare-commit-msg.sample', '/.git/hooks/push-to-checkout.sample', '/.git/hooks/sendemail-validate.sample', '/.git/hooks/update.sample', '/.git/index', '/.git/info/exclude', '/.git/info/refs', '/.git/logs/HEAD', '/.git/logs/refs/heads/20_min_80', '/.git/logs/refs/heads/clear-branch', '/.git/logs/refs/heads/codex/clear_one_skill', '/.git/logs/refs/heads/demo', '/.git/logs/refs/heads/main', '/.git/logs/refs/heads/one_skill', '/.git/logs/refs/heads/pre=agent', '/.git/logs/refs/heads/test', '/.git/logs/refs/heads/test2', '/.git/logs/refs/heads/test3', '/.git/logs/refs/remotes/origin/20_min_80', '/.git/logs/refs/remotes/origin/HEAD', '/.git/logs/refs/remotes/origin/clear-branch', '/.git/logs/refs/remotes/origin/demo', '/.git/logs/refs/remotes/origin/main', '/.git/logs/refs/remotes/origin/one_skill', '/.git/logs/refs/remotes/origin/pre=agent', '/.git/logs/refs/remotes/origin/test', '/.git/logs/refs/remotes/origin/test2', '/.git/logs/refs/remotes/origin/test3', '/.git/lost-found/commit/a9784911cc1c5b5eab6643175e5ec45caf25eee4', '/.git/lost-found/other/00025daef50b48b9a7c3aa0957f67692b7cf9644', '/.git/lost-found/other/00279ba916b80ee7f054dcfe4bcad5fdf3d0cad4', '/.git/lost-found/other/003f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/lost-found/other/0052dd8f0d35e7d44cabe09971d6e0f21ca39cd2', '/.git/lost-found/other/009107e59a300c960ee6ec2a0fd55630b53e6a77', '/.git/lost-found/other/00bf2ee6092a4428c1c240774794e6c695ff4722', '/.git/lost-found/other/0108acc654101c39e74de3cb6404c4fa80bc7bad', '/.git/lost-found/other/011eb16c1ca5cd43dfe08ae67835808b35c8afe0', '/.git/lost-found/other/015abae91e08022c92cb6c24e1e1097ec60a9c6b', '/.git/lost-found/other/016411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/lost-found/other/01686fb3f6afa2208defd34a9188169a7884eccf', '/.git/lost-found/other/0189548f4f27fcb26840150f585a64515d77c26d', '/.git/lost-found/other/01a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/lost-found/other/024da679e39764f8e2a1862074bc7d3a67b39a2e', '/.git/lost-found/other/02500954f54d824bf47a0c40e7249570c8ae35a6', '/.git/lost-found/other/027cd9077d41da5280567175993abb09c6e81add', '/.git/lost-found/other/02955e2401b4f817cc67ef6094697af860f2d18e', '/.git/lost-found/other/02b7b9d7d9324409084e9f2b00eae11901589864', '/.git/lost-found/other/02e3706e34f211187bd64efa7a9ad51760195d39', '/.git/lost-found/other/02e5c435ffbd7357cd76f7c19bf5f4451ea88c3d', '/.git/lost-found/other/02e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/lost-found/other/0312d61983ef80179bfac79abbba1359052f115c', '/.git/lost-found/other/03732f0c6e6eeaef66eda4e4a6de308b7e7e1e95', '/.git/lost-found/other/03ff6a156c8ba598cf1be27fb2371810888a927a', '/.git/lost-found/other/040be927181b9604d69593ffe36ab7303b1a94bc', '/.git/lost-found/other/042e02d97cc4abc6a96b55d97f34fc76924c9cf9', '/.git/lost-found/other/04378a998f4a8686eb28f62e8833b0f539229714', '/.git/lost-found/other/043f51145222bf3b3e811ab6d29c229b25b3b1d3', '/.git/lost-found/other/044e235175ddef6dd6b9a05edbd34b9ab69cbbd3', '/.git/lost-found/other/04602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/lost-found/other/0478eb80cc9a8041214bf273295064af3ab7f7d7', '/.git/lost-found/other/048703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/lost-found/other/0488481d528674a76807703e6625d6284ca8293e', '/.git/lost-found/other/0489842c6d2c5ddbc9550902039e9b25701d08db', '/.git/lost-found/other/04ba7faa5aee31cca7feb4058574f06ec3a9b645', '/.git/lost-found/other/04bf8e699f88900a6960b666079dba19a77ee7eb', '/.git/lost-found/other/04d51f0de077d3b810718bfa2ca6ac4f3567c07f', '/.git/lost-found/other/04d557d3b8c74f15dc8b1039d196b50cb8924950', '/.git/lost-found/other/04eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/lost-found/other/0504a514448e0c3c3e4f771ffc84479295824920', '/.git/lost-found/other/0558ff9439de64e491ee9c3bd2097b5b118029b6', '/.git/lost-found/other/055ecd0695e622dcadcedc29409753f35d106433', '/.git/lost-found/other/057e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/lost-found/other/05c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/lost-found/other/05e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/lost-found/other/0617f381a59a452478a8f34cabb652beadf361cd', '/.git/lost-found/other/061c9d02a136ba7adc607ed7074cd148595a2030', '/.git/lost-found/other/0631461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/lost-found/other/06418747a855c7847e27bfe23508610c20a60493', '/.git/lost-found/other/064efa3154548faf37f72f6e16da0f94681fa86a', '/.git/lost-found/other/06a8e8ac333fed73af47212fe4626cbaa3b74e82', '/.git/lost-found/other/074930d053a799cc4f9095e89196437f704205d6', '/.git/lost-found/other/07682e77b603150eac6f657df236ac3dced0586d', '/.git/lost-found/other/077efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/lost-found/other/0791e2c492831faaf144a90e6af25adaabad38fa', '/.git/lost-found/other/07d0f29a2d244a75911191faf176cc0c7edf4bda', '/.git/lost-found/other/07d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/lost-found/other/080554e8ddc2a1a87275a26e5457e1b2a6046657', '/.git/lost-found/other/08080c1aef87cedbe163497ddad8cc3005a73f7d', '/.git/lost-found/other/080d85bb922b72b159fc03f3f1a84d23a9d2568c', '/.git/lost-found/other/082169d84ac7751152d7134fa37292c00ba029d0', '/.git/lost-found/other/08377760400a919e539db754b0b66ea7ce0cef58', '/.git/lost-found/other/0842d15769f312e00dbce38c79a209d783d115ea', '/.git/lost-found/other/0846bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/lost-found/other/08749be2799a1a1f0697ed2571a4682426ea12ff', '/.git/lost-found/other/088409712f5c920b0dbf4a4c818e977f34f91873', '/.git/lost-found/other/08ba0a8ee50af5b8ff5eb0a82d30bb5229fe2e86', '/.git/lost-found/other/08feb11d7a524e0e04e556a3b0fac0a6a7b24657', '/.git/lost-found/other/0937353c8f0a794e6ea7d64c5904fa44ffbc61aa', '/.git/lost-found/other/093d21dba99b105a0e82051ab2639b5151325793', '/.git/lost-found/other/0946862f3f15d72c8b71d2af4522b4921f6cab96', '/.git/lost-found/other/094e04d13c87f5a327a7f44ffedc0ce41d9214d0', '/.git/lost-found/other/098b34de8f71069fae9082ecd1903b6faedce4e6', '/.git/lost-found/other/09916958db8eaa97c465c9bec51a3d1a29863ab8', '/.git/lost-found/other/0a05a2808a79fe98d007bccb3b1060551300dec8', '/.git/lost-found/other/0a32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/lost-found/other/0a401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/lost-found/other/0a56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/lost-found/other/0a597e37cfb13fe9af1875fc0606d2f7cc0e7ada', '/.git/lost-found/other/0a962ce910aa746587b34755922bae542449fba9', '/.git/lost-found/other/0abc810e4c97279e80fa5610d8d2838b94e3bb03', '/.git/lost-found/other/0ae25708036bf7db64f0327ea004917ad42ea679', '/.git/lost-found/other/0b32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/lost-found/other/0b5d3ac18d6fbd99afb581479554b58fc4183e02', '/.git/lost-found/other/0b5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/lost-found/other/0b9c1ff14d0729b8ca054bf3b70a31ed6ea3724f', '/.git/lost-found/other/0baa622887f5563517e122f9b16213710af9e5cb', '/.git/lost-found/other/0bbcef51f80d0155f83a276423028a01a50cd92e', '/.git/lost-found/other/0bbe894f6158df6217aac34e5062d723091507dd', '/.git/lost-found/other/0bc5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/lost-found/other/0bebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/lost-found/other/0bf720f21f41ce829add4aab5a9a05012208c3f7', '/.git/lost-found/other/0c00cb9ca737f2be5b9cff166bcef532262ec699', '/.git/lost-found/other/0c4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/lost-found/other/0c55eb9a5a6f0f2c00a7d6a578505a35c3c881f8', '/.git/lost-found/other/0c614b8e0f3afd25e895d9491c2a30e5913af606', '/.git/lost-found/other/0c64a4d48bda41945b4888b51a9e960d8fbfcf0f', '/.git/lost-found/other/0cd26a469771b69762f53b5ae2a322bf170091d1', '/.git/lost-found/other/0ce0b926ac0c36b6e353c377ebc74e59bc0561c0', '/.git/lost-found/other/0d2b4e5c9def6a898a4064dd6adf23d978807b49', '/.git/lost-found/other/0d3b08adf9c7ed270b6d5889540ad4437d5f0b98', '/.git/lost-found/other/0d72d0b2349a404cc4cddb87c836194765377d74', '/.git/lost-found/other/0d753acfba917272cd72f418e9c1352ed20054f6', '/.git/lost-found/other/0d8780f3e4c97dc70ba82cc61c5cef46d57b0b33', '/.git/lost-found/other/0dbcae139c196ceada45a4720daaf5908702ecc7', '/.git/lost-found/other/0e189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/lost-found/other/0e31d5d75617658d5871f0af7cd6e2572f65d5a7', '/.git/lost-found/other/0e33d9681c3f231054d16d613b34097e7e8b59e7', '/.git/lost-found/other/0eb37de8ca5ba7a34797b3355f41cf01b22ff008', '/.git/lost-found/other/0ebe1fc27f8d238046aea951e6caa693563a5db1', '/.git/lost-found/other/0eddffee3cce42079be92d29e9858c7f31c0a906', '/.git/lost-found/other/0ef556b4beacab982c37a6ba626b68c12a03a3ae', '/.git/lost-found/other/0f0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/lost-found/other/0f138f0796a06e405b352d9b196d634fe03272bd', '/.git/lost-found/other/0f3f373dbe68457e2f332b53419313c5297f50fa', '/.git/lost-found/other/0f573afb56cf5cd6dd86621f5e5c4d7eeff7c726', '/.git/lost-found/other/0f5968785d1283804001ca49ccf77d63eac98e02', '/.git/lost-found/other/0f86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/lost-found/other/0f9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/lost-found/other/0febdd5aed4ccb535776cb3ecf5f7292598d83cf', '/.git/lost-found/other/1018a2334d5c1968f40c2f478fb1f2867e67b8b5', '/.git/lost-found/other/1064453d1e30d78cd388f816b907f7b742375e31', '/.git/lost-found/other/108486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/lost-found/other/108d20d49b8c9df755feb7040b27dd500650d6f1', '/.git/lost-found/other/1152abac92eac8d8b605f61e7608e5151d222f07', '/.git/lost-found/other/1168066a747c3bef2d6e633b2347c20cc6b56404', '/.git/lost-found/other/116968b47e00996915b67531127f0954c7ddd1a4', '/.git/lost-found/other/1195185617fa4e3585174859ed5709d013f5937a', '/.git/lost-found/other/11b6a93338766923a8e6379405e6fcf4ab828169', '/.git/lost-found/other/11c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/lost-found/other/11e01dd8395bcb4499bbae87a8fa5d396b5bb9a0', '/.git/lost-found/other/11f3df8ac49a0be182d46132407e50090bc85a7e', '/.git/lost-found/other/1260fee99a4cfcbd9d4ffb0eb2de091a7a472b7b', '/.git/lost-found/other/12782408d18b12ea7c1fd9e5d39ddbfa2040ef21', '/.git/lost-found/other/128150674170b66350257cc719da038a61a568bf', '/.git/lost-found/other/12d12afbdb51a82ea91470a68c5936ef307758b3', '/.git/lost-found/other/12ecf89d4939f447a2a13eb6a8584268d822df06', '/.git/lost-found/other/132ce036f2fe47610a5925b048748ef75eb541db', '/.git/lost-found/other/13360394a41c8fabc39419ab404191a8575e2799', '/.git/lost-found/other/133c2a7f8f0c8e8798adb0c95502b796e8304aa0', '/.git/lost-found/other/1392a68ba7c0702c66b4fb266ffd087081b1e141', '/.git/lost-found/other/13c40173739fb7e84b979f3c6ac5261cec02e012', '/.git/lost-found/other/13dd0ea3ac7cf3fa815ff54ed379ac145c2200aa', '/.git/lost-found/other/13fb8a33b9d96c2a9ff445c20dea718e895df5e4', '/.git/lost-found/other/143334e584ff71080c606f29c1ef42924bbe453d', '/.git/lost-found/other/14394b47e18f572003e3d82368702dfd474b70c4', '/.git/lost-found/other/143df4c79cc8ee0249f8509549e5377882a28010', '/.git/lost-found/other/1474c8f7cf8bc22cda503322795cac94ac621675', '/.git/lost-found/other/148a5ec5787afd3f553071ecc831a805312f6ece', '/.git/lost-found/other/148c20fa8c56ae81068aded6b9a8f2a59fc229dd', '/.git/lost-found/other/149a72f18b0f5ac8ed9bf713a2c26c76d8158588', '/.git/lost-found/other/14fe9bb6670802ae36d1022630b687088b71c35d', '/.git/lost-found/other/15098da0ba5b0e2d399d8688a8a0b6a0fcd68d1d', '/.git/lost-found/other/155f8df967724158d80873e629c6c12bb65c8d00', '/.git/lost-found/other/159a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/lost-found/other/159bfd26b659195df8c8486d12b5e15f948cb808', '/.git/lost-found/other/15be2e474eb938a89e4d7c19737994893197e781', '/.git/lost-found/other/15fc480833c1c814d413e14a2421b5ffed74028f', '/.git/lost-found/other/15fd3d807851be39f668587b875d1bd9356e1171', '/.git/lost-found/other/163d050dd4db671d29be7efff1a35864f91ca61d', '/.git/lost-found/other/1645e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/lost-found/other/164b7fafb2c4bcbb6315f95870ae3efbf8a82241', '/.git/lost-found/other/165d22d6f5554de58d1281ade7295158d4e62312', '/.git/lost-found/other/167230ee6e97a40999b7b1b46b089e48951a1158', '/.git/lost-found/other/1683c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/lost-found/other/16a2cab9c4e32851d2754116ca26b4ead49cd1a3', '/.git/lost-found/other/16bc644bbb95c0d296bea492b5595b361a93b9fa', '/.git/lost-found/other/16d466f5d6f6422fc565801d9d97c0bd71bf6a5a', '/.git/lost-found/other/16de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/lost-found/other/171b3e26763b46f7034313a38879dcb5e511f770', '/.git/lost-found/other/177a3761fec84c8776563bc7d9edcd67544feca6', '/.git/lost-found/other/17875ecd8901fa5f6f1ffd63a3f4ac41cd695e3e', '/.git/lost-found/other/179165971d58c6643a8bf303e8bf53e64a143ed8', '/.git/lost-found/other/17a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/lost-found/other/17c6782b615441baeb457ee93a458ed7371c9f99', '/.git/lost-found/other/1805f56abd31c9fa832a4d2e4d2a6525282bd60f', '/.git/lost-found/other/180e3f7a759491581027a4970076148d69b10348', '/.git/lost-found/other/185c9bede1c02917cd4743d154dc42b2cd03cb25', '/.git/lost-found/other/1862eec0af25e420dee69a16ba235f610f20756d', '/.git/lost-found/other/1876a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/lost-found/other/1888c3e87775cf3cfca934be2e7ec03a6696f1da', '/.git/lost-found/other/18d512a4ebe9f93cc357a19059984b3398799bee', '/.git/lost-found/other/18fe30c098f75b96caa54450040279f8727780ea', '/.git/lost-found/other/1929b4d821dbc5d88f2c4c6d8839d0fedf3fa95f', '/.git/lost-found/other/19704e0cd5db5fec06dd7c57009e47296c0c4411', '/.git/lost-found/other/19928324ad53403e47456f49785dd300a6abc1e0', '/.git/lost-found/other/1994bb1252910ca25e7dd1c7eaee69a59f99d597', '/.git/lost-found/other/19bc9e08c030c0958b8cfcb118ef4e6a076e1bfe', '/.git/lost-found/other/19d15ee65c1ad2342c69a499567a3d8e33d985d2', '/.git/lost-found/other/19ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/lost-found/other/19eac84456408b48017f9b8f7012a31d357f9ded', '/.git/lost-found/other/19ef249a5908e6c6f084c18763897a644a28241b', '/.git/lost-found/other/1a04525ea6855d36a41a4720d225e21887989682', '/.git/lost-found/other/1a3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/lost-found/other/1a412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/lost-found/other/1a7b119a11b008be1ded0bd9ca1ddfad0e5a5260', '/.git/lost-found/other/1a955782d22785e3c692639e34ac42ecd1ad95be', '/.git/lost-found/other/1ae3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/lost-found/other/1afcc87003afe09c0245ee2e2f90a48f107eea91', '/.git/lost-found/other/1afe522d67bb11ef6df1ef598c4a6077cbdbf43f', '/.git/lost-found/other/1b2651a7254d50dd505d130cb119b1e0f63b274d', '/.git/lost-found/other/1b297017feb7427e872083cfba46fdd2d1f5d1f1', '/.git/lost-found/other/1bb304e8afd560b9be58336068f17f0f453cd33d', '/.git/lost-found/other/1bb6184cbc8ec7b0b92597da642ddb7baea3f9f0', '/.git/lost-found/other/1bb94dc37fa7ba202e37fb9f730b2c1ffe60c9f8', '/.git/lost-found/other/1bd62bc3162bcc0924c6b11dcc91aea034a50dda', '/.git/lost-found/other/1bd948006afad9d92ba0af0d9d6aac84b81201ee', '/.git/lost-found/other/1be15396b1a24634af2755f0315d590d8f5efb56', '/.git/lost-found/other/1c3b26b30ba44895a4b99ed6b8361e4fe8d6e96e', '/.git/lost-found/other/1c5c64af7a4a179928feb3e438ba9aeca2b21785', '/.git/lost-found/other/1c6f0d2fcead6d6b9af167efe84b68ab9867253d', '/.git/lost-found/other/1c8f3931f4569a257832b968b4b4e0122f827992', '/.git/lost-found/other/1cb460853dbc76ecd603937b1385d60dfe4544da', '/.git/lost-found/other/1cc87e753d217d64955f9f7594e5c51e9515e117', '/.git/lost-found/other/1cc883a61f30b9ef594ac9e9119fba4fb6e6b38a', '/.git/lost-found/other/1cd48831e92cfedee75b4f2bd298004c09a02e41', '/.git/lost-found/other/1ce139b0630235d7cccd5e7233e06fb27e4b7e92', '/.git/lost-found/other/1d116b842cd0f57b27060be476644b86e101adbc', '/.git/lost-found/other/1d486741fb9e843d4c02664be20ce398200e3031', '/.git/lost-found/other/1d62dd77221b120231127e20a3d046857e9e43d4', '/.git/lost-found/other/1d80ca727f627adf666f395a0c85e26662ed0d20', '/.git/lost-found/other/1dd3c6fbd22c1169a906849b6be2a41c24aa2fd9', '/.git/lost-found/other/1de732b38d658fd3ce936527e47cac6259f9592a', '/.git/lost-found/other/1dfc607d1dcba5edcbf0de542ba2777324f237ac', '/.git/lost-found/other/1e350fcaa9e1ea22a0fa61a8b01f206f7ac9dd0a', '/.git/lost-found/other/1e5a8be244c1322fa76b77784e582f480009958d', '/.git/lost-found/other/1e73f11f4d9826d98dd02d4b053bf4f4f144542d', '/.git/lost-found/other/1ed6e6a5f1c7d86cbcffec476f2d43c3a3b164cc', '/.git/lost-found/other/1f604bc809b0d41096d17b0050c153e858717c6c', '/.git/lost-found/other/1f70a2d4551510dfb5fdd95b27b6bf486639e5ef', '/.git/lost-found/other/1f9bc9625cc3b8c37c1c971597ee9e3158f57f4e', '/.git/lost-found/other/1fb978ebe70aba71b3e2d74d673c0459d8480ac6', '/.git/lost-found/other/1fe3e3bfa8d6df8f7d0aae939c931eb1d654bd6b', '/.git/lost-found/other/1ffa5ed33b6108ed57142c1be928988a7761b6dd', '/.git/lost-found/other/201c519c93b3b77bbe0555abc3e68c9a0d24c28b', '/.git/lost-found/other/2077ea20e01da4d37e629d77f92bd01657842631', '/.git/lost-found/other/2083461eff88321aa0feceaab497bc202e7d110e', '/.git/lost-found/other/20a95d03ea8998b75a0379c47b79d67138d097ba', '/.git/lost-found/other/20d6d5fa6f6982c1d4d8d927ae5e9e121fe42018', '/.git/lost-found/other/20edff68991fb4c628d2281dddb40df64282d6e1', '/.git/lost-found/other/20f6f17a1e15763482af8451d3da4498642ba0fb', '/.git/lost-found/other/2125a26d3c69f2df90b281937dc82deb6c57cb20', '/.git/lost-found/other/21637826d1d04950f4a4d796a9571a8c4d86b806', '/.git/lost-found/other/2187ac3ff0237618615d7b487a0d1a6403ef49d2', '/.git/lost-found/other/21b0396817724695b99c77d49474607c4516b8f1', '/.git/lost-found/other/21c099aa1a03294014130368b917b2c6eef94753', '/.git/lost-found/other/21c428f3247ee9fb40e38b78c925eea08e7175aa', '/.git/lost-found/other/21d13a0a40c505324dab511aa407e5dc471bcf1c', '/.git/lost-found/other/21dc7c101abb0ba003e36a25d3686c48c4182328', '/.git/lost-found/other/21eea7a19ea8fa9c7d004bc61a994b42b88b8ac8', '/.git/lost-found/other/21f7a4f54ed4863b3ff2ff03747f55590badc90e', '/.git/lost-found/other/221fbbc53f621f91a6220c85cd506af3f790086e', '/.git/lost-found/other/226a93510d33d1c407aef258f9c39f42e3f298ad', '/.git/lost-found/other/227c0e6634ea1ea9f9c9e1068c1c55f53917c14a', '/.git/lost-found/other/228c08f34331c47620b55794c64c0ff9897f15c0', '/.git/lost-found/other/22b435aac92e50eca2ee89fc748441e81cfcd88d', '/.git/lost-found/other/22baf3300cc31a3540ca4314fd8c58bcb7018353', '/.git/lost-found/other/22e7afb00fe5b7c7602b761800024ed40d25fe21', '/.git/lost-found/other/230d67a0590a4d61346d6dd5ced3f53dd0f1bea2', '/.git/lost-found/other/2339b673bf04246da4977d2a1c82e1f447ea3544', '/.git/lost-found/other/2354041ddba6abd34193e615b4cf804c6e2fd520', '/.git/lost-found/other/2358432f1d03d54e5ede647bf656376dae10e349', '/.git/lost-found/other/237e83f06ebd406dcc11507e0cf8c3be65e684d3', '/.git/lost-found/other/238faa3816f1afd26933d98bd81001eb92a2c876', '/.git/lost-found/other/23b597c126b6815d23f022bce47ef1f8815c532b', '/.git/lost-found/other/241dfb0157cfff0271813dfb80667be5a95deb89', '/.git/lost-found/other/242b028657099781ee5f230d30afc0a8af8423df', '/.git/lost-found/other/245ed230dee59261acbdfe117c3db0280411df76', '/.git/lost-found/other/247b2894f7b921a2585eed175a225fa8e7dee8bd', '/.git/lost-found/other/248a3917f8467ac0cc6218d4b046e8e4b2cba851', '/.git/lost-found/other/248fd8353332111067158f2d11e7087f1ac3fe69', '/.git/lost-found/other/24ec11aadf71bebef0b0658c378b43788974a6c2', '/.git/lost-found/other/24ed3535539a46584ebcd6609d0ecdf3a0f86ddc', '/.git/lost-found/other/250d15ac2ac893edafa629b15e07ede0747d8e78', '/.git/lost-found/other/2516e2d96db3ff349b2fec7f85e9958f93292621', '/.git/lost-found/other/25240eaa758f5a58e2ece8cd89c1ad44a88971ec', '/.git/lost-found/other/2533d1949584c2a0a3b143a5cb4de3f8c1d17758', '/.git/lost-found/other/25393416d634a457748f6167634a4d86955a9774', '/.git/lost-found/other/253f5f1950cdce8f3dd7dca88b26bfcfcb68ad9e', '/.git/lost-found/other/25908607dbe19286a4b0f7b6927619cec2531bf0', '/.git/lost-found/other/25e89d80677a94a06bfb564749370a97050e61ab', '/.git/lost-found/other/25e9c1f9b50b6f8773736712f54f64d323d415f9', '/.git/lost-found/other/261067ca7aa2c677fcce286ae23ffb3e3e3c4b68', '/.git/lost-found/other/26194e93e2a767b3f44b2bb12906aad486311c49', '/.git/lost-found/other/26204973c5913550889f7735c6c91e3f23eb971d', '/.git/lost-found/other/2663b05e98e130e359c6f704963f2e68068a829c', '/.git/lost-found/other/2667e6553b593b2789c084f20b09c8e100fec7e6', '/.git/lost-found/other/2676a4fb754239d1306066ad2d8f58004874245b', '/.git/lost-found/other/268340e1ad4d5df681a7c90f17f4dc772b726e70', '/.git/lost-found/other/268f3c416fe521d519da01323f305123fa54f3aa', '/.git/lost-found/other/26bc257b7c543df579db1afcb9248ced695a5433', '/.git/lost-found/other/26ee19281818f2ab393398d7cdfab1cc1a73aa44', '/.git/lost-found/other/270866455342b36d58ba2ee755f781bbdb564dc4', '/.git/lost-found/other/27cefe5d09eccdf969bbe7c4bd03ba88866dbdd5', '/.git/lost-found/other/27cf296e191cf1e3f150c9cfc6dbb191d17554f6', '/.git/lost-found/other/27e9ed80c1396df06710f8c7782e989d2230e035', '/.git/lost-found/other/289dbec76c204f3703abb10c34cdad5888f18f05', '/.git/lost-found/other/28c2c11c8dfff1aa3fa7b6add9019a0af59a46fc', '/.git/lost-found/other/29017f09af575575dc32524be2294103c1bab658', '/.git/lost-found/other/2912b2774fce14827260d4c8ec3a58acaebd30aa', '/.git/lost-found/other/292fc6f6555ddd8ee1d1baf819d59b7704bd34b9', '/.git/lost-found/other/29b9a8951ad9517c1953a163da020fe28852bba9', '/.git/lost-found/other/29f91579b798fbdf2436d2f21c966d128bba04fd', '/.git/lost-found/other/2a3288a1f6616175a2448df2069d345263d3ceab', '/.git/lost-found/other/2a92a9d4eaa55a8e8264ef2a4ec0a1712f8d8bf7', '/.git/lost-found/other/2aa35d99f6a8fdbe078c97cbf1990f66ca61c0cb', '/.git/lost-found/other/2ac0ccfefd5c151ca5de3ddf23b9bddfc1c8cf4e', '/.git/lost-found/other/2afee31d90e375b801139b051605dc6f5599d9f1', '/.git/lost-found/other/2b1c9b3d9439d122a26ecb89328b50c78ea7dbeb', '/.git/lost-found/other/2b1e035dd765108817ac13695374505ff9a7d9d4', '/.git/lost-found/other/2b33a12233bf94d423b84df484fbd4936841f0ff', '/.git/lost-found/other/2b77f7188e91b5f41905b979e1453716042a88d6', '/.git/lost-found/other/2b84077d254fc2a1d66d0b4ea82ef3a7fa125c3a', '/.git/lost-found/other/2ba1ae4723622dd7a36a624626a298bc4aede590', '/.git/lost-found/other/2baa9b4b0fd3a53e07dbaa15098f4c45e7419cd6', '/.git/lost-found/other/2be2042f9a6e321e9ae96e9becee05d609390c6b', '/.git/lost-found/other/2bf2efefce1765ad78030310ed9900afb0cd5522', '/.git/lost-found/other/2bf5bb558ff589653f528af8bedb778c46df101d', '/.git/lost-found/other/2c24c73a4a5af1d5a5ec1c117c520c7056ea55b1', '/.git/lost-found/other/2c39548b92ad9ddcc9c291ce39e44ed6c6b6cf3e', '/.git/lost-found/other/2c4e1eb30367408711d432986d0b075531aa3a92', '/.git/lost-found/other/2c59ee393814f03d894d5d8c75ab7512af596f2b', '/.git/lost-found/other/2c8ab9af72c1dcf6d59f4a77eb53ad7631241c8c', '/.git/lost-found/other/2c8bd2401a11ab4f8b5e2313cc59bab1b11cd988', '/.git/lost-found/other/2ca2261abaa3459cab2e6b5aac65911448fb906a', '/.git/lost-found/other/2cab5b28db8404259e58a97c72d97538899d23ef', '/.git/lost-found/other/2d201015b65cbcd6a4fe0082bf6d4a65076dc4e1', '/.git/lost-found/other/2d209cca9eecd6d9519f21ae66f180d2001554ef', '/.git/lost-found/other/2d3f8b0777fb0252760bfa45abbb7726b967cc4b', '/.git/lost-found/other/2d5822675d64a208d26431a0cb3bd4a9ee1ad7e1', '/.git/lost-found/other/2d808e55af2eb9b6c496d06a8de71c32578f172a', '/.git/lost-found/other/2d926e4fa759b1b3235635ba6668898a635443f9', '/.git/lost-found/other/2d98f0a835a91e49cb26869dc16dea0583feafbe', '/.git/lost-found/other/2dad60a817385f78660e338a688f9699f3790810', '/.git/lost-found/other/2dfb63554d59caccc63b4addb234c135c283d1f4', '/.git/lost-found/other/2e00a61f618f743393ca83058702b25b950de8ba', '/.git/lost-found/other/2e107635a41522a90f0ea3c1f8fbbb3ff8685f1f', '/.git/lost-found/other/2e395785e7e850594fe6874f052e55a0733d4549', '/.git/lost-found/other/2e91b71a0e65135085d8a12d86bbfd6658dd36de', '/.git/lost-found/other/2eb6a12922b18a340dcf58a23feb13e0e2b1f88b', '/.git/lost-found/other/2f14cb77a3fe840c167ec7c363ba895d3a809b68', '/.git/lost-found/other/2f29d9394aab14b49d63b7303c6549458f4f7158', '/.git/lost-found/other/2f785e870024de3ac7ca3a834b25ca25e9d9cb8e', '/.git/lost-found/other/2f7887c4fbfd68a3721f5d2cdc896c48bf353c5a', '/.git/lost-found/other/2f807662ed402a67cdc3a86d525264af5ff4fb7d', '/.git/lost-found/other/2fb9df715c3a1ff4dbeed9b729ca8722ebabe729', '/.git/lost-found/other/2fe7004545a2ce0c6214b6c75bcad75dbec8f434', '/.git/lost-found/other/2fff44f43f90bd8988761555f56630209e29f777', '/.git/lost-found/other/302b17514cd5a0c86a73900453a45021c8a6c77f', '/.git/lost-found/other/3040605d4918eca0701e2a541826d735e153871a', '/.git/lost-found/other/306a8becbe8f0d8eab7964b3986c9f94ff283e20', '/.git/lost-found/other/306e5950b0fcee534e38083a1536591ce18ed5e8', '/.git/lost-found/other/30ab4115f80c0bf921117640ff7c490947ad6202', '/.git/lost-found/other/30fcd7b29e19f40daebc1ce7d83b37c394250cff', '/.git/lost-found/other/30fe180b7dc5a182beaa893a2cea5b43e407312b', '/.git/lost-found/other/312308f273d963ad2f881e414e6dc908c7de72c6', '/.git/lost-found/other/312e11e2186827cecd4ccdb5f99b25b16de8e422', '/.git/lost-found/other/313257cee583598c2b1e76531aee4382a34ae791', '/.git/lost-found/other/316871d9d0ef4a615b8cd3e853225ef2a3b19c95', '/.git/lost-found/other/3168c2f06a254ab33a036ed9a99965494aa89e44', '/.git/lost-found/other/3176ec4eb6c6c275fe82fa458715a968e6073475', '/.git/lost-found/other/318a95b28c7fa29873933d535636860233bfe2a2', '/.git/lost-found/other/31919cbc2e7b9a6268f7bd5ade6a59d4902b52dd', '/.git/lost-found/other/319c61cf6810319b6333dbda3ffcf61438c2b9db', '/.git/lost-found/other/31e4b72c2638192bd9b6ff9894f15b4365be6f7e', '/.git/lost-found/other/31e88c3eb7be2600a07f8a293e0d521af54d6577', '/.git/lost-found/other/31f64f6e3b537ebaddf428c4cb7764d746510f2b', '/.git/lost-found/other/322ad23a9b2322a5eafbb97fd34f393402a04544', '/.git/lost-found/other/323f82bbbb2a2f435ba1a70ab85e6e604de01b6e', '/.git/lost-found/other/325706343725c6011b78dbccbe34e242657d5d49', '/.git/lost-found/other/327e8f6219bc9ac3aaf5c4e5f8a88559dd9c8d9c', '/.git/lost-found/other/32858e6be0b09a988b9b7722bed3b4ac6acf2711', '/.git/lost-found/other/328bc3afc9053e448e43ac838fbde8b5a6bff782', '/.git/lost-found/other/32b556713e2c319d927537477bda7dd391634e9a', '/.git/lost-found/other/32f8032b0690c3e5ab5788e9a392fb328fdde7e4', '/.git/lost-found/other/332c5bfc92dcc95b0fdab72fec060f0f1fde04f7', '/.git/lost-found/other/338787f9553f8178de800ae15ef7a23d4f096f13', '/.git/lost-found/other/33a71c56250cf2a2cf3bc20447d3bc0f4722b8c0', '/.git/lost-found/other/33c258c67e23b0e16815b8156accbe52ea0f47ae', '/.git/lost-found/other/33d111952f9df6dd8776978e49e1067a8bbcc82b', '/.git/lost-found/other/3407448373b50404341f30cfe3e19da4562e5b61', '/.git/lost-found/other/341580a820d2cd018774a99fd90cdd4928badc68', '/.git/lost-found/other/3480592152b095df8c4308029978a60900113bbf', '/.git/lost-found/other/34c6a03cca3744f90eb635e4a427cf083aad4110', '/.git/lost-found/other/34e68b2d3472d9f5c822bb72c9fc2c4ddb3f31a6', '/.git/lost-found/other/353eeeb90d31595d072017c457bdb335470c0b79', '/.git/lost-found/other/35425eeca676d4342ab62ffff6195d41b11f03ba', '/.git/lost-found/other/355ff84b964cd582bf1f677e33941403e9647582', '/.git/lost-found/other/357377a3e9d1596994eb7db5c89ea3b40161b48a', '/.git/lost-found/other/35942a0a0c5905e8a31fbdd947ee83d6135330d6', '/.git/lost-found/other/3598090e6a420d70ef76bde587c93ade0de2721e', '/.git/lost-found/other/35c6bf791767e8c12735840b07aaff1273f0435d', '/.git/lost-found/other/36228b5f70a00e5ce49800e5c4e6f423a864ae65', '/.git/lost-found/other/362381263cf3f80b5818de655e9053e7f11cdd9f', '/.git/lost-found/other/3627eb8009d622db55d0b115ad04a86af57dc99d', '/.git/lost-found/other/362dfe3c7cf298171bd42d395215477fc4996729', '/.git/lost-found/other/3632196771add5fcb90e466f66e477f671b35212', '/.git/lost-found/other/365be8f94d80e5067929f7549396a0e85134c387', '/.git/lost-found/other/36943e9cf8334b2d66b1b289b0477923183c99ce', '/.git/lost-found/other/36d35fe01b77481fe1e61d9f5cb7270df4fe7a68', '/.git/lost-found/other/36e7091b7fbff7d70e65f68a180bd36231bbeaae', '/.git/lost-found/other/36f21339d64c30f61addd97c3c411376231a882d', '/.git/lost-found/other/371991836494764af4d1bf157fb9ef9baf12051a', '/.git/lost-found/other/3731c5b1a9613854aafe4ca48509e0a5447058b5', '/.git/lost-found/other/376c1e88772f0558744c3ec5bf33e514bcbfa5f4', '/.git/lost-found/other/378b9fa979fd0cdcd74fb98be8f965fc64ba96ab', '/.git/lost-found/other/37a0ca6cc8794e5b4800cad42666f43d1593da69', '/.git/lost-found/other/37ab16fcbeb235841f49b53dda4f8a4cb8576605', '/.git/lost-found/other/37b0cc2012a9a29b9126c2222045b25cf5b61c05', '/.git/lost-found/other/37b1dbfa62553742da17b93f4fb2997a706ad491', '/.git/lost-found/other/37c80b6e3cd1ba73b73a863658651fedc19934d8', '/.git/lost-found/other/37eb658dd959056bdc91ca5add0c61677dd55131', '/.git/lost-found/other/38078e333be4a14ae2436aba441dd97d2d37acd1', '/.git/lost-found/other/3893a9d23c221f7a7587b3bd1bbce3e53451a36b', '/.git/lost-found/other/38a1a54a9daf5b271d9479b93a8af42e6c3731d2', '/.git/lost-found/other/38c69c470dbb40ae7c309888b1d1250f91ecdfe3', '/.git/lost-found/other/3928dccc158026c5d3bd664415ca5ce646555231', '/.git/lost-found/other/3932a7771a6417aaa5625d39bb52f63e9d5ecf03', '/.git/lost-found/other/393d937812a14bacba39114d3fbc6ba4b6f687e1', '/.git/lost-found/other/393f72379d2551529e19191f444ca8ac0324cc09', '/.git/lost-found/other/393f9a985c2a03394a2e4a7eecdf783ab4ad0993', '/.git/lost-found/other/39654433fd10a74f799c2e6d20c1faa49b0ec715', '/.git/lost-found/other/397ec1001cf0afcf62fe6b20e898ed46571f0cd5', '/.git/lost-found/other/398f7fdb157e0e718ddb1b583446c83525a9c8c8', '/.git/lost-found/other/39e7fb971ecd00a92d0ac87b16b10fd7dfc091a2', '/.git/lost-found/other/3a6fb490b61ef395f241c15652f46c571c0d4ff0', '/.git/lost-found/other/3a9c2f93081539b6786aaecb9961f15db261b7cc', '/.git/lost-found/other/3aa11aec8ea158ebe6fa2976edaac47f213d098c', '/.git/lost-found/other/3abda6ffef0e775951dfeda9637eb16314baaead', '/.git/lost-found/other/3acc108aed44025f56b47a7481ef7df3bdba7c98', '/.git/lost-found/other/3ad3ad101a41a3f5f7cb1ff2f8ac7fdbd4fbb1e4', '/.git/lost-found/other/3ae1b05c2a5d648e1e234162415c93a2d566455a', '/.git/lost-found/other/3b05a03bfb9b84a6f82a3f6b6d4fddb652001ca6', '/.git/lost-found/other/3ba38eeb4c4dc8a5029fa4c435a97b9bf9cb9c5b', '/.git/lost-found/other/3bdfe3e50659109f92b7cea294e2c2ccded7e07f', '/.git/lost-found/other/3c27c38977ce104a2f4a88b49b560e41090430d1', '/.git/lost-found/other/3c2a0da42d395f055ae2c4ece3d6d56b95ed0f01', '/.git/lost-found/other/3c8b5c679d9eb3dbd857a4bc2414e018507dfacd', '/.git/lost-found/other/3cbae7783af35d2629fd5daa444b860b54c1c541', '/.git/lost-found/other/3cc5321661d71bea5e919b2dd222d55638ef6474', '/.git/lost-found/other/3d1412302b68c0d01f1afda6130e8ef38906d800', '/.git/lost-found/other/3d2058541bd6f85fa9d3041eeb94773535041b4e', '/.git/lost-found/other/3d4090fbbcedee422c984f49d6951366d6e87331', '/.git/lost-found/other/3d5b8e81ff03360ac6eace0f9658f95dc3aaaab4', '/.git/lost-found/other/3d6ce554450436c4ee02e9238d7bee54a5c98a8a', '/.git/lost-found/other/3d76e8038eb8c5d0065da0f378418b0929a3e1c7', '/.git/lost-found/other/3dee1d10be4dc43fdf33e57816608eb7f5f762e9', '/.git/lost-found/other/3dfafe83a756a154636a42148009fc2f995374b6', '/.git/lost-found/other/3e66b1694740b2e545f26acf8a011934e713ac32', '/.git/lost-found/other/3e6ff38fa95be1c55c68ef2ea46946f569926f38', '/.git/lost-found/other/3e846e06d434e3be0646f8d8c73c8be9f548eb22', '/.git/lost-found/other/3ec37580b08a3f792df050067bd3383ad9c01df9', '/.git/lost-found/other/3ecc52a19ba9501ffdc2b0775d42316e3eb031db', '/.git/lost-found/other/3ede7dabe843ee07ced13269bd65b72c34b9b5d6', '/.git/lost-found/other/3edf7805dd24b80e8c991aefa453b6e60371e47b', '/.git/lost-found/other/3eea2cd0368389b3b358ffb2050310a8e5f01084', '/.git/lost-found/other/3f24447ae77e74087e11e85cdb792de9af39d23b', '/.git/lost-found/other/3f325646ce7bfe0e26c28c1e3ed2d2717812bda7', '/.git/lost-found/other/3f343eb336812ac82de7a282f46dd867f06f141d', '/.git/lost-found/other/3f5e76235147c70911902e9f103daf1a7314e95a', '/.git/lost-found/other/3f77999b57ace248e5dc167ef4e26b985531f944', '/.git/lost-found/other/3f980f549b46e7260f2214367a43deb12d0ef4b7', '/.git/lost-found/other/3f9fdb89a31a02a343b2b0b6b3e21fc7ca7d581b', '/.git/lost-found/other/3fca9ac2547a9940b5a04731b6524c73b9b17c78', '/.git/lost-found/other/3fdcc274f28047cac793cf86aed310300180bc2d', '/.git/lost-found/other/3feb49e8ddc04e5c3e85ae2ec34908b7ea1236c6', '/.git/lost-found/other/4022468256542bc3fe6c5cead30dd9c90615fd3b', '/.git/lost-found/other/402864b837e70ae54de89eb82cbe93546cf2695a', '/.git/lost-found/other/40758f589a15d70a0fb173d1dd0cd93c2b280b20', '/.git/lost-found/other/40a67f757ceef8b9e10d6f06e5b2ec8c75529ae6', '/.git/lost-found/other/40a857d2f4d88afe60d9d223c3874cb9ccb4a55c', '/.git/lost-found/other/410fd0e93a275523e38efd323fcbb83b8c8831fd', '/.git/lost-found/other/411b53810429fd3db2d870952d8c267659517b00', '/.git/lost-found/other/4158634eeaf9ee3f387b133b1fad878f8bf4c596', '/.git/lost-found/other/41d692718cca7d01e7f6785a5d39d34b0cd79664', '/.git/lost-found/other/41ebfa1a4e684dff0756a2297687708b98e178ac', '/.git/lost-found/other/421881dda370e44a27a3e93dc9caa1d44579a990', '/.git/lost-found/other/423b3458604e6efbe12f4620e1e5e7d0044acda1', '/.git/lost-found/other/4262aa86595198148b5c5af75bd5b347d55e6d4a', '/.git/lost-found/other/428a345dcc183804917d5077052693bb113f74e0', '/.git/lost-found/other/429074a78b514abba6f272bd54f3011a72c28afc', '/.git/lost-found/other/42b5b3341164d4bfd41c4b45e85850bf626b8ebc', '/.git/lost-found/other/42ca4054cbaf5d4c01d024bd7ee0918efc52ab07', '/.git/lost-found/other/42ebc146732d966d28b3dc12887b8f73ce4c4fd7', '/.git/lost-found/other/42ed76e3d2c1af07d1c2b357409e0630ded68c74', '/.git/lost-found/other/42fcf8ab7e1224020d789b4b47b37e4eff58c62f', '/.git/lost-found/other/43294817109e7ecb22f6b65e069a13b8270d1053', '/.git/lost-found/other/433079b36165ec24a2b3bfa3208be0e72c68112c', '/.git/lost-found/other/435a5c0d738969e6f5c3f22e6c83e385fbfd025a', '/.git/lost-found/other/4367533bb415365afca5247c8006e707527136df', '/.git/lost-found/other/4371fbe557c2492b0303af5861b007b2b20ea8c4', '/.git/lost-found/other/4379e78e42681a9c944ced94d3e215fef675fe57', '/.git/lost-found/other/437a496118d962d30110b9550c9933470f544b31', '/.git/lost-found/other/4396b48a65707e8d7917f9be1a2f6c18bc175683', '/.git/lost-found/other/43cd46747974e7eaefd6bc4515e802a3f16a787b', '/.git/lost-found/other/43d8aa62d08f1788f22545bcad2bdf344ae95c64', '/.git/lost-found/other/445b7add6b22f31d6169b6fb04c94aaeaafd23c7', '/.git/lost-found/other/4464c2c8a128a1cd27d261d90e6d66fa913160e9', '/.git/lost-found/other/447720e79a8bf68b0570557e2603109333a4a04a', '/.git/lost-found/other/447def406e0b202e5959a50704be5779c5793fa2', '/.git/lost-found/other/44d6e7a95ef488d9350b45e9cfa358ce04beec08', '/.git/lost-found/other/44e59e3cec45d7396ac73e863ced62a8d7f5c46b', '/.git/lost-found/other/44ebc6510ba8445a4f02160a7d4562395a9db5a5', '/.git/lost-found/other/45055281879d94949ebe9a279d805f909fa52808', '/.git/lost-found/other/45485f8473f8fb74c608c1215de7a9ae5b767a32', '/.git/lost-found/other/45969488a2aa771c9c0a5ac56fa58505d7aeecc5', '/.git/lost-found/other/45c2226188811a624b5a22e20465e156c9863894', '/.git/lost-found/other/460a7a8399d7b7db69e999894ed5f6a244e69d20', '/.git/lost-found/other/461886c6ac2b8d4e6ba0943a72403df1d6968569', '/.git/lost-found/other/4630a38916d765d913e0e6040a11b6132baa36e6', '/.git/lost-found/other/464073b94e8df746f5abf60322e5bc23c78508e7', '/.git/lost-found/other/4660835e392b7dd46c5e7ffc6a6f765a7a67478f', '/.git/lost-found/other/4678157d773d5c250ee875f3fc5ad8cfbb06ae38', '/.git/lost-found/other/46c6456223387aec0a7b111a58be75f442f3c342', '/.git/lost-found/other/46f574b31ea9c081d10dbc24fb57ba3e4b447b6f', '/.git/lost-found/other/472070c0c081ef4c9ea5e73fce87dec51a5e50bd', '/.git/lost-found/other/473daf24f1e540b2f25a569f819a238aacb81035', '/.git/lost-found/other/47b03dd951e4d464d01dd59f62c2b67f84506cc5', '/.git/lost-found/other/47eec38c60613993ebddfe34b03b3c993405009b', '/.git/lost-found/other/480ca1cfc93e3be2b2d88a08f067f9f8875022e2', '/.git/lost-found/other/48355610f438c75b706f3d1b9bb15c49f849800d', '/.git/lost-found/other/485ebc0e3b351a9997f0bd7231ed34ebdc5eba4e', '/.git/lost-found/other/48e9b14b31df8db282aeb8c13c7196186d5eaf72', '/.git/lost-found/other/497261e3c8906476c12d6208e965b9194d2ccd9f', '/.git/lost-found/other/49750a24fedc98c1d3f489355165462ef5f0c3a6', '/.git/lost-found/other/49e4545b844c30e3a2dfd5283289f27650feed77', '/.git/lost-found/other/49e5c2487096098aa82596f7c3bf4b154b03263b', '/.git/lost-found/other/4a1b4edccdef931f7401b221ca7b97904c5f9eca', '/.git/lost-found/other/4a4fed6a266a06c70783a57203e735d40084f4b5', '/.git/lost-found/other/4a561130f0ef82f6839112aea65b7c41d857f15a', '/.git/lost-found/other/4a64f6a423d13664596ad8952e9a991142c575b3', '/.git/lost-found/other/4a7421627f436e26ec2e56d8ebfee4e5b009e05f', '/.git/lost-found/other/4a9614ed45b8c3c446af97804ee70fae5cee33ee', '/.git/lost-found/other/4aa09bd0167a59b088b2c27f326b600029e93e56', '/.git/lost-found/other/4aa9736811f8b92b79e2fb5044fedd3827eaae85', '/.git/lost-found/other/4acce9508c07accfcb472ac7b53df59993547757', '/.git/lost-found/other/4addd3a9cd275d18232024a8986d0a71719be52f', '/.git/lost-found/other/4b0ca8a212de55c027ab38e37ffcd17e341d57bc', '/.git/lost-found/other/4b1106adc7b4c0535779dc0c2df302e2e4f26afb', '/.git/lost-found/other/4b16c36c5bbdd7a8a0aeeb449e081c80e2b75d01', '/.git/lost-found/other/4b4e6a0046c053a95f57754b9088a81834674349', '/.git/lost-found/other/4b5c220106e4b150f1785aca51b4c1516ee7f6f7', '/.git/lost-found/other/4b825dc642cb6eb9a060e54bf8d69288fbee4904', '/.git/lost-found/other/4ba7d47f279b001eb96215df8833b8c2cb201c3e', '/.git/lost-found/other/4c109c4291b72213236a54418e69bc70989d3d23', '/.git/lost-found/other/4c3c101d419f879404ff9994e148420b95f8ad60', '/.git/lost-found/other/4c493eb24622138649cb71acb19118998e7e55d5', '/.git/lost-found/other/4c5e7bcd16c8cb7d806fb0fff610e8f4c5db8de2', '/.git/lost-found/other/4caa0b8605ba9a8a10d09fa28ab020b5634c8f6d', '/.git/lost-found/other/4cd6f7724ce8848c6e3b4a92fbd8d8ee2c9fd8bf', '/.git/lost-found/other/4cde126dbb4465d93bf6a56e0f7557664cad7052', '/.git/lost-found/other/4d64eae0c3986894803d586d4c44ae16906d23f8', '/.git/lost-found/other/4d77a00c84211f3b1f7d0b33a9c650a0068ca57c', '/.git/lost-found/other/4dae699298c4e827eb777a620bc2b0b622a3d043', '/.git/lost-found/other/4daf2d4fb4be2002d0c6f0783065cd4aaa2ef9d5', '/.git/lost-found/other/4db248d2d0362a2baa123bce350af1c3cf725718', '/.git/lost-found/other/4dba40158ad402bdb18ab94f570242af2ecb9f72', '/.git/lost-found/other/4dc581629639bdbf6136e78e94203ab183c60871', '/.git/lost-found/other/4ddb67d026b4d1d9533591627008838db3040342', '/.git/lost-found/other/4ddead2405965902636a6bf032847bea1dcec5e7', '/.git/lost-found/other/4e560d39e66ee48393ac86adf8bf92f390ab6282', '/.git/lost-found/other/4e57556929f069e1d92ef1cedeadbdd46be69462', '/.git/lost-found/other/4e6cbaaa682013b3b168c0079f78acc0ccfe0552', '/.git/lost-found/other/4e80ac0c1f3b8a9f86cdccef454912a80077d15a', '/.git/lost-found/other/4ed608f4d1b961b4b069673f0dac7b286868f1d4', '/.git/lost-found/other/4eded7a6a9ba555dac903ab553ad0640bfafd803', '/.git/lost-found/other/4ef1590a8b7ddbc3f4fa8977aac9094f931283b4', '/.git/lost-found/other/4ef73eba22c74702bab0fa911b27145fe6efd727', '/.git/lost-found/other/4efd0c308d4fa547f805bf82210e817bc8739939', '/.git/lost-found/other/4f03978e25b1d70dd18b2f1ce83f070616bee53c', '/.git/lost-found/other/4f6403a8bcb6c19a368e929b9a4e12741e1ab55a', '/.git/lost-found/other/4f7bed90c38a4cbb348c4ad64255d11ed01043f3', '/.git/lost-found/other/4fb85fbb7c372a0b84cd78fa6b55e410e220239f', '/.git/lost-found/other/4ff93b7412dfd5e731ca509fefec5e2a910528fd', '/.git/lost-found/other/503b52b471cf3c48677445669dda1dda8fd71c51', '/.git/lost-found/other/50446582fea97fa549a6039a5f0c504364f69e73', '/.git/lost-found/other/5052541bd836a255d6414f0d6caf7cb46ce878a9', '/.git/lost-found/other/5056e85cfcdc5e48302a6ea6e308e29ec17154a3', '/.git/lost-found/other/50641e34bbca5261e3460924a6ad4cca4eb1e681', '/.git/lost-found/other/509b71d4704b84a1ffce51e2639bd836b3493ff4', '/.git/lost-found/other/509ba1ee9c66d67aa12183a23911275c84c1be12', '/.git/lost-found/other/50ab5d3cf546c8b875e8c8fecb728a69ed6129e1', '/.git/lost-found/other/50bf8437d9f0ba4f1b5bda9f3cfdff66feafd872', '/.git/lost-found/other/50c32b19907ec29e0df34ae3dcb64ccbad1bfeed', '/.git/lost-found/other/50cf16ba1f7cdef0e11f3e689c2ac0c4146c23df', '/.git/lost-found/other/510a9de17bb3cb81c8d9dffaff39e6a1ffc8d46e', '/.git/lost-found/other/5135c970168de2f80375b8e8223d8b65ebe722d9', '/.git/lost-found/other/514ef7a257573e892fef8efdc8092aa113f301a6', '/.git/lost-found/other/515672a3eac687eeaa0d5331a88ae03e9eec92ff', '/.git/lost-found/other/516400f538a8bb12359bf8121ffc8de0d1ece0a5', '/.git/lost-found/other/5177cddf0421903b5a7667854f6e1447853266df', '/.git/lost-found/other/517936a6f2e958e3c291ca7426694acc1c9ed684', '/.git/lost-found/other/51ead710372b626f38f784b6b56245267e896e06', '/.git/lost-found/other/51eddaf2d727e3973ab74f8d0d4d5d6925dfccf8', '/.git/lost-found/other/51fc32836d05581c65f4f62453fd8461eae64d47', '/.git/lost-found/other/5207df72e6c942df0f5a50074a13d02c5c6fcf92', '/.git/lost-found/other/520f6d14e206018e609af947049cff9cc8242353', '/.git/lost-found/other/5212c909d3b94b54efd1b8e83b0ae14bfd060e6b', '/.git/lost-found/other/523cfd7c6c11e165293fcbe926464d35abe0f7ea', '/.git/lost-found/other/52510e1da02780de64cb636dbeb5322763d39bc0', '/.git/lost-found/other/52631f7dd5d612089d235a84853c538dcfc63d39', '/.git/lost-found/other/526cbab8a8237857d96750d81938f8548229fdd4', '/.git/lost-found/other/528c0f551f1529db0685ebfb83fb5bcc0d13a715', '/.git/lost-found/other/52a9fd5d5a39c98cf011809f1954ce924858033a', '/.git/lost-found/other/52bd08e69825f02027ca3f99833ed05df89c9347', '/.git/lost-found/other/52ee24e4476554b49c7f5f84227ce066a0a46f9f', '/.git/lost-found/other/5321249b535a38dd91115955e2aa31639d2a7306', '/.git/lost-found/other/53989b292aea8588bedee021ac45dcefddb3caf5', '/.git/lost-found/other/539c77ebea4b39f981394f47d5682778d9282819', '/.git/lost-found/other/53c00c790d7213e762a416ccbd9fa61f2cc6b27c', '/.git/lost-found/other/53f1494b9ccdf2520caf09f9b6c9b0b6fe832f22', '/.git/lost-found/other/53fbe0eab185e254c6f27d57abc84dcdfd0223a9', '/.git/lost-found/other/5400429d73c66a98a7d7f803984889b2cf64f643', '/.git/lost-found/other/5415418c0097755bce371e51342cd16532d8fbe5', '/.git/lost-found/other/5424e6ee1e37bb5033742e0579176168ba0eb42e', '/.git/lost-found/other/54348c264bfa80b99bc179182d9d4400da05a8c1', '/.git/lost-found/other/54437ef622b766cd31a65735951ceb6b1f3dbd97', '/.git/lost-found/other/5444fe59b494246baf22bfe218d9f62cea416fc8', '/.git/lost-found/other/5459e50a37091210db1c5703a61149ff7366f367', '/.git/lost-found/other/5483d2dab97c022bd6d8bdbe5e7e91a0bb14d17d', '/.git/lost-found/other/54946c6df52fbea6e5f86390fa9fd5a6d9b8c581', '/.git/lost-found/other/549ef64d2ed3890a06bd03ef59952b31b70a5027', '/.git/lost-found/other/54a23401d7ac4923367c12c897f2444dcc00fe83', '/.git/lost-found/other/54a41810fd052d9463f8d60abf2c75184362b839', '/.git/lost-found/other/5541601d03b6f8e0c6c01342973a66430d8b0a50', '/.git/lost-found/other/55616d36043061c1a3c7f616e099f6a5abde1e72', '/.git/lost-found/other/55769048317ffd40eca0be3cea5a4b9e5ab7cdba', '/.git/lost-found/other/55804d3108a2a367b825f5cf1bb797755f5ada1a', '/.git/lost-found/other/55853255cc94e3efded0c03bbd00de39d57a7ce5', '/.git/lost-found/other/55992f60276d8ca420b03e6af91ed8af74fab670', '/.git/lost-found/other/559baa54efe7fb5e41f2551d2ca8e03f87ca5f0c', '/.git/lost-found/other/55b747cbbaf511f4d5424f0f1301ed30b1916007', '/.git/lost-found/other/5624bee17cfdf365584b8229349e7d5778a96c07', '/.git/lost-found/other/564f7f5c55645405bd63d23bc0315154baa54c18', '/.git/lost-found/other/56943cdf18ab772ff17cd18821c0cb38f040c874', '/.git/lost-found/other/56a2b9f0ddb3eea735b36c89c4433d9800483f7a', '/.git/lost-found/other/56e2a20d652ee923dad7ebb9d8aeda679efae502', '/.git/lost-found/other/56ea5e17523abc029922afcc9f23f2306cfef729', '/.git/lost-found/other/56f07bf7f1652d395100a1b2e0b96ed2b54e171c', '/.git/lost-found/other/56f3b2f52e650607bcb68a0a89e36251acb754f3', '/.git/lost-found/other/57707d21bc0c5ccc78a5b479538fa8f4af03b517', '/.git/lost-found/other/5796390469d48d2c75ad156f8f3c2e1054695731', '/.git/lost-found/other/57b04ada3b0285ca34c1a7fdbb9c904e484a2d14', '/.git/lost-found/other/57d46027e0e2507d28ac3ab8a433fb6035544f95', '/.git/lost-found/other/57d4a6120719f112e80cebbf59c497f211238fe7', '/.git/lost-found/other/57ef49de52a2d19fe06f40aa614014bbea9935bb', '/.git/lost-found/other/581d582546277573b28d5812835faa2ade024e61', '/.git/lost-found/other/589ef170d33fd55b085f70295ceebad9b7d6eb8d', '/.git/lost-found/other/58bf0f7e675b7588a79421a3fabaf0f35e219290', '/.git/lost-found/other/58cee47fb9ef92895314fdb4ea00faa945434e52', '/.git/lost-found/other/58d03866cf23187801f46939ec2328e2dc8c05b1', '/.git/lost-found/other/5905f9d6c104fcf3db9d8f19e6dcbde6149a6d03', '/.git/lost-found/other/590af4dd3c7d105d3ad2866312585bff30d02804', '/.git/lost-found/other/5928f67430c179dc2031c576bf0b24b51d2bca5b', '/.git/lost-found/other/5971fe317cc2404af9f0717140a87f15b0c0b55f', '/.git/lost-found/other/5983ea75fd9362c5a8709fb10cdfa4920f085b40', '/.git/lost-found/other/599223087cf2abf27e92dbb63ca3402862306cb5', '/.git/lost-found/other/59a6d7ca7e0bd39f24f74469da806dd2659236c9', '/.git/lost-found/other/59b78eed07eafbf8ed57b97a459a61e949c07b14', '/.git/lost-found/other/59d110fe6522d55e8e5f8650763f5ff86c935b7e', '/.git/lost-found/other/5a1e4a159d9cbf9d18e6e0da20f04e709b36e923', '/.git/lost-found/other/5a41118850b5b97764e3861fc59a901f69f18298', '/.git/lost-found/other/5ab3284a5abce4c25306590d08b3b50e8d0dfe01', '/.git/lost-found/other/5ae30190da5996be8b0111d18fe276b95d8e3ba6', '/.git/lost-found/other/5aed03d61d3a40a4e4d8859a43e5ff373d789afb', '/.git/lost-found/other/5af7955eaaa535c9f41527d8cab24ed5c1388305', '/.git/lost-found/other/5b03c014dcf3dab20b88f5a62dd0865020292ed4', '/.git/lost-found/other/5b3c284ca03de4c25ced51e9aa3a4b488804a44e', '/.git/lost-found/other/5b42a5fe2abb1393cf2b9ac7359176e4aed00c0a', '/.git/lost-found/other/5b5d27407a7bd2a7d7a767409ea402d354a9a684', '/.git/lost-found/other/5ba55edd28d0248f250495d47f6ab87821817c15', '/.git/lost-found/other/5bf68c1c51dae67f6a925c6ffcc4e45d0ee9c27f', '/.git/lost-found/other/5c1ab9aa3ef25014cdaf48ecc250f106e4abe387', '/.git/lost-found/other/5c40fd7e30b0ae67c6188ae7825d3ecbe2c432b0', '/.git/lost-found/other/5c5231a09008229e8e269d9a71bb646de28c0bd3', '/.git/lost-found/other/5c6ac7789c226f1cb333033c83401c787362e213', '/.git/lost-found/other/5c9d49cd48ff71491ca95509f601ff732142d86a', '/.git/lost-found/other/5d0c31c8d4c3150abb326fe441cf29550e85229f', '/.git/lost-found/other/5d51b2cf47c9bec0fd8dfc6a5c742839aead66d3', '/.git/lost-found/other/5d5c0bdce3886c23ef6aa2478091b71980c7b558', '/.git/lost-found/other/5d9ca220d74f6f62928d7fe74439558ac0eaddc7', '/.git/lost-found/other/5dad81834d096b45968ce3db534e06ef01cb7962', '/.git/lost-found/other/5dc8c414c8a6dcb39eead75672e29a6c7705fa1c', '/.git/lost-found/other/5dd53689515fdcdb933986493ce832b0fc154869', '/.git/lost-found/other/5df4f9798bc7768bbc0cdeaaf89cbb71fc7e2519', '/.git/lost-found/other/5e620fd25168e7c134890f30749078a81a7b6245', '/.git/lost-found/other/5e99e7ca5804c491ec01e5498d13b271c4c2f5b8', '/.git/lost-found/other/5ef0127085448a90356cab02f54d9ec9c190d13e', '/.git/lost-found/other/5f114962f8c95cc3d3e6d07ad8aceeef21cb42bc', '/.git/lost-found/other/5f278d44ee3cc96d3c7c582b2baa956cd2cedeea', '/.git/lost-found/other/5f7c76357de6ec1ef7872600c6c0d99d6fb29350', '/.git/lost-found/other/5fa52d56651eb41b51a76e9489bc3a1e803320aa', '/.git/lost-found/other/5fc241b5fc5ee3126714b7ec6bb1218f256b2f9d', '/.git/lost-found/other/5fd65f63e326d2a5a2305d4023ee3f9f9a1c7ba8', '/.git/lost-found/other/5ff9751d696b33f83abfca804807e09e998cc015', '/.git/lost-found/other/60055836c05f4130a75aa75b465c2932391fcfa7', '/.git/lost-found/other/601f2c09dd519075bfeb9db5b995db629718c821', '/.git/lost-found/other/604dca6b26bd18ef8041517b5520080d7d019360', '/.git/lost-found/other/60549f042a38455f36259a61d55c2a8a26a84f77', '/.git/lost-found/other/60737bccecfba65d47f6ce9e98a60da40dd51ab2', '/.git/lost-found/other/608826a2afc590737f32a764a625ef1f8c685dd5', '/.git/lost-found/other/608eab5a999f1dacde5212a37bb0b10c89bd5f2a', '/.git/lost-found/other/60cb3c25c404aaebac03a48a50958503db52145c', '/.git/lost-found/other/60cd35607497b333c4e689ec8c3d7beefb76d5aa', '/.git/lost-found/other/60cea4218c9d2d340270861f9084015f542aa19e', '/.git/lost-found/other/60e755f3531398a88cb2ba67af858c57dd0ab90d', '/.git/lost-found/other/61206657bd31e3e2e564ba4130c5cf5db80199d6', '/.git/lost-found/other/61240f34ff36c6a9ed178e7f3b0769d90d505ae9', '/.git/lost-found/other/6128184c716e17ff7c4382e61719214b88a65240', '/.git/lost-found/other/612b7e3dac1b05bc83204b5091634dc99d745a5f', '/.git/lost-found/other/613d1efee79b495719629da39214f79500635967', '/.git/lost-found/other/61731703e939fce963fa49e55b4af95286342a87', '/.git/lost-found/other/61ab639fb396a69f456a8a0e8161c81a66b36b50', '/.git/lost-found/other/61c62badbeadcca961fde66023da79591e056332', '/.git/lost-found/other/623e4c399c3cf78aa7bff72e26554c85f6869fe6', '/.git/lost-found/other/625248a511b95b56bb088ae1f70dfb5dee830348', '/.git/lost-found/other/625fa42e650c174cda286bf390e545c6354e1f44', '/.git/lost-found/other/627b2245b8bd0bb9433125096bdd64b99e749544', '/.git/lost-found/other/628b4dd0a93a7e16d3cbf73766ec9bae336e6116', '/.git/lost-found/other/62a41bba70c8083d3e9792ce06fcf891c6fa24d5', '/.git/lost-found/other/62b286e180ad3b353b79c522e41cac008f3512b0', '/.git/lost-found/other/62d1113d6b19143c69097fc9eddb4de615bdb653', '/.git/lost-found/other/62d972d5d66da2dc69c96c10b87c2fae3639a25d', '/.git/lost-found/other/63144637a3bd9f8474fbeb8463792c71442047b2', '/.git/lost-found/other/63491f18503bb3346888baa308185d2196d689a3', '/.git/lost-found/other/636d99342c41a4943fa0ca86f1619d0573375bc6', '/.git/lost-found/other/6372d5b36494f138c1638b3930d8543e77265803', '/.git/lost-found/other/639aff1317ae109c623652e0970c161d9a80a821', '/.git/lost-found/other/63d868359a2df3e9c0ed61a522b42a15afe9462a', '/.git/lost-found/other/63e70e5456461721b42c484bbee1886cfc8ba39c', '/.git/lost-found/other/63f2e29d53169726763ff4581e6fdcd3236cdb45', '/.git/lost-found/other/64068a5fd20e95303d2a58a8f948e08cab89c31c', '/.git/lost-found/other/640ebd997c31281a5274fbfcdaf9624d3dca7042', '/.git/lost-found/other/6417cfd675c0269adda74c4af4984a8e5523b5bb', '/.git/lost-found/other/6421734fb5e632258add15277e10f9d075b83131', '/.git/lost-found/other/64e4f4a1d9a5c5f3af3076ec413de73a3f5a4100', '/.git/lost-found/other/64e99286b0f3b21b065d94749079fd3fd4e94ff1', '/.git/lost-found/other/64f99c86919eab0648c3a2fb4b9b58576a85203b', '/.git/lost-found/other/652f440f92ba723251ba6ba470744e6d192a0ea7', '/.git/lost-found/other/6589cb9582ca26898931b1ff9fa713b99a51fd69', '/.git/lost-found/other/6604d0071186e48178e9b0dfe7e979040c3e54d1', '/.git/lost-found/other/66161534878c9a2771f904c86c37771812f852de', '/.git/lost-found/other/661bf6799d7caeff91a59255c0749bb0c19e430c', '/.git/lost-found/other/6638f29e468c5eb3550c99e26aff88a106344cba', '/.git/lost-found/other/66899d38c422ab75f0919f5714961b39fb244dd4', '/.git/lost-found/other/668a493ef1fcb9d584aefd1e500fe080eb2b7488', '/.git/lost-found/other/668ed8f54785171df27bcc3dd3ca6946b7c47b03', '/.git/lost-found/other/669527a55303ac3089986dfdd5be5379da40b8d6', '/.git/lost-found/other/66a367c89a095a293497c3606593eed3675b7bab', '/.git/lost-found/other/66b958f32ddafa4f75a7a2cb2f24a9e9ccf2a097', '/.git/lost-found/other/66d6a8e4d9ed60f991a0a185966cb717770690b6', '/.git/lost-found/other/66dc9fe2e67543e8bee36d8b809fc2488132e8d1', '/.git/lost-found/other/66f40ce43c80179972266b9fb98da995998b53c3', '/.git/lost-found/other/6701c178ad1a4b00372bae3c25cfaac2c80c9c62', '/.git/lost-found/other/6702cfd9756562bfb0a3ba9b5abecffb3edd3d4d', '/.git/lost-found/other/674604affdb240288071ea569d52f55c530b19b0', '/.git/lost-found/other/674f596c4dacebc48590bc262602ede7478a42f3', '/.git/lost-found/other/676fa0f11b62b954662d9a796a91c01408e97449', '/.git/lost-found/other/67b20ca14055482a477dddac64582ac8ae5767e0', '/.git/lost-found/other/67ce18851f37a03dbd8f1912f40b0333196a565e', '/.git/lost-found/other/682c9758c717f786de009b535f7b4809bcfcb68a', '/.git/lost-found/other/6842fe827192bab8f1180cc0a667d476df9cd850', '/.git/lost-found/other/68680d91ac416db504df57a84291d630e94eab46', '/.git/lost-found/other/68749693c84ef5a049465b1b192d56aa094cafc4', '/.git/lost-found/other/687cde57acd639e44b9f6ecf4bb3b29996c10bc3', '/.git/lost-found/other/689b7fb39f59c02e4fbbcde071296721398eb013', '/.git/lost-found/other/689d0da7d061471f4527308c48e26efb792ff379', '/.git/lost-found/other/68acc160c191f8f39dd69ea2c9fd1bd132519e31', '/.git/lost-found/other/68c62d74946ba59bc95c49aa23daa2faa9d50df0', '/.git/lost-found/other/68e38676e7f2aba51f365c5246a25b26eaf7c93a', '/.git/lost-found/other/68ed276d325e028f6520a3a2139e590b668d16ba', '/.git/lost-found/other/68ee67a9c8c69cc7b4387076d19412bf6fa55a91', '/.git/lost-found/other/6916bfc4ae8a8656910be8213444648b53a2352d', '/.git/lost-found/other/6924feb7662147552bee9698d879ef0e54b6d8ac', '/.git/lost-found/other/694b515cd1cc0b2492e6d20ed85c4e0a9212cf18', '/.git/lost-found/other/695a1fc4aabfb29ae1d4eb53d8262b001cf0b268', '/.git/lost-found/other/695c4393b98dcf12334da13f5dee4b09f2e56f61', '/.git/lost-found/other/69b678f6e53c24601108dacf7be78a0f4dc9297c', '/.git/lost-found/other/69ba46d4e80a1ca1f7e61de30c5a0973bcf9949f', '/.git/lost-found/other/69d86a739e9bcdaca05986856237308c2e352b4f', '/.git/lost-found/other/69e0d35ba51506e2a6b1c82fb10836e2944f7d41', '/.git/lost-found/other/69e6486640b279c4c27df16fa42efacdf5fd5318', '/.git/lost-found/other/69ea2e3abac381e1239cca65d1ff4425a100bd06', '/.git/lost-found/other/69ef08f9dd58c1307d87a9d77fe60fa99d0c0540', '/.git/lost-found/other/69fd638c548168d2d60451a27b06ab1f4168253e', '/.git/lost-found/other/6a0e4ee850e4136089b231c7385181f3833d64e5', '/.git/lost-found/other/6a10a4c99f71d892813817d6e131c32de5a3a0b8', '/.git/lost-found/other/6a5ca58dd7f7d4ff96beef4b05385fa608ce1276', '/.git/lost-found/other/6a61b1a3a9cdedf1639d353de4c161efb37613bb', '/.git/lost-found/other/6a7c5cbb6e250ce2534ddc459ec58e94ad59daa9', '/.git/lost-found/other/6ab43d1c8712b075016024e6de4b2cedad30d4fb', '/.git/lost-found/other/6ab5f05565940fa70b59ade18d5824d49687af69', '/.git/lost-found/other/6ab7a9816bb2bb377a0dbebd922c0f16d81c7db3', '/.git/lost-found/other/6ac3752495b076c748fd4e5c4984925643feef75', '/.git/lost-found/other/6ad46cb805dbdc2933f7591e26cf9223d5c4c09d', '/.git/lost-found/other/6add66c47d463964ce1f625054a2e62c78de0052', '/.git/lost-found/other/6af52eaf8a4268931a8ec6a132d7ee779f9b53f7', '/.git/lost-found/other/6b00c19ac5ad98cb682b6aa371330eca5c5137ea', '/.git/lost-found/other/6b22042beba9d91f0d97ac16821226b69175c861', '/.git/lost-found/other/6b35464eeba949dd63b3800fd407ec64ad156c85', '/.git/lost-found/other/6b7cbd1cdc3ecae6259e767ec077682ab8140d37', '/.git/lost-found/other/6b874d512a6169e56875de8896ae72ca50462b5a', '/.git/lost-found/other/6bb3e94d1d720c1348861e7a1dbe524b51eaace7', '/.git/lost-found/other/6bb4e0d4dd0ee5445099c82b2bd2f64a53e8d294', '/.git/lost-found/other/6c03949654187bb18a9d56abf3fa548d35436fac', '/.git/lost-found/other/6c0d651cafe38a80077e3f039cef23d0a74f61f4', '/.git/lost-found/other/6c22da847b3c7def6cd69370256886cb3df72bb1', '/.git/lost-found/other/6c5fc2bdd3439593a8643d755e206e6dfc9fc170', '/.git/lost-found/other/6c76334a601f051983003c01c0a4a9c9647d9409', '/.git/lost-found/other/6c84c530995aeb77ea4f06496152518f193072cc', '/.git/lost-found/other/6c8a6bf7a8364e9f3c66b02e8af3048c191749db', '/.git/lost-found/other/6ca4f377708c5ecf6907a214a05573cc42b26244', '/.git/lost-found/other/6cabcbec99c44d58b07d21563b56e3e3ecc9cfe5', '/.git/lost-found/other/6cdb8c84c0d8288f817da1bfc5af9d5ea100f691', '/.git/lost-found/other/6ce65d7b31135ccacfff2b3d2ab53e743f0fd75d', '/.git/lost-found/other/6d14e456c1a77b86235f00f27b0d7ff404895330', '/.git/lost-found/other/6d3808be278c3451214e6436726830d41ba7b8ea', '/.git/lost-found/other/6d3bebbbfb578533ce3e6ab76d4cfe41bc2c2802', '/.git/lost-found/other/6d4cc26ae5764ee023fc9a552bb075bfa762903b', '/.git/lost-found/other/6d52ba52a8e301203cf321217bf466872849a86e', '/.git/lost-found/other/6da26546fa1246aa176dd104defde990f03fb2d8', '/.git/lost-found/other/6dab0e6afdd91c28e48f63d3688707a18eb7dac3', '/.git/lost-found/other/6db056fef046577bfd43bd0b8f438aa337f406b2', '/.git/lost-found/other/6df408815ccc8efcd933582508681c4b44e1d871', '/.git/lost-found/other/6df878640493277c4d70736151c30bfa36d4c930', '/.git/lost-found/other/6e1a4dde1913195bcdcb1ab2c38819fdabd889a7', '/.git/lost-found/other/6e22f463b1ec7d2cd140e6e0b0e03a632aa90f06', '/.git/lost-found/other/6e4284250937e9e1f0201611e6096d4101d2d653', '/.git/lost-found/other/6e5315c52f4cb6f8f50c68116b2f12db8d110b4c', '/.git/lost-found/other/6edc0bdb4fd041efdbe26e3db5c16b7b8eeca310', '/.git/lost-found/other/6ee8d33c6149cc513fff7a4bb33af1cba643681d', '/.git/lost-found/other/6f21d6a0aeb79b7c4d3605725f306d44d94c8d27', '/.git/lost-found/other/6f2516ff42249437779576cb418ec04cb76f8024', '/.git/lost-found/other/6f2e1fed7351e51786da8d13cd287a382305f2ac', '/.git/lost-found/other/6f43d382fa76287088af7b112df53a49cba251ad', '/.git/lost-found/other/6f453918535498db9b0ac365f2433265782b6945', '/.git/lost-found/other/6f88ec227ecf2f7b141024b1d501544126a224f2', '/.git/lost-found/other/6fba22d4dc0eb6400d9414150d5b70602d6564bf', '/.git/lost-found/other/6fcf161c510c9b98c91a405a36236d1e7e6111f0', '/.git/lost-found/other/70268d1c998cfd8ff0496f00635f779488913cfc', '/.git/lost-found/other/7053cc71e49faa648cb55ce0f0bf2b206c62ad69', '/.git/lost-found/other/705469fe281823f80b2cf27ac4e097c432c0fbb8', '/.git/lost-found/other/7065f6674fe7a8235b352054611ce3983ec2b558', '/.git/lost-found/other/706a12e583fe32e25dda3d328dda9d590f7ac56f', '/.git/lost-found/other/7073db0d222f367a044b7b9a76927f51f6854823', '/.git/lost-found/other/708e1960cb8892a8a08ccca0fcb666ae281b2a16', '/.git/lost-found/other/70adf55db7d632e16f7262dbf14637069fc748f0', '/.git/lost-found/other/70d153a9884e3f575ceee6df23bed28105af19ad', '/.git/lost-found/other/70f09f86714b5f1a6772acc9824b08e5148482f8', '/.git/lost-found/other/71037982231de4a8c00ad8f13b4a6cdd81871edc', '/.git/lost-found/other/714397ace6f967f7f6c94a8446aad82e62242f3d', '/.git/lost-found/other/717ca515e3896ef68f1c05dace103215d030de33', '/.git/lost-found/other/71864276193f717598a3844fdcd23105f607a358', '/.git/lost-found/other/719a970b7bedabe76e51c19aef9d38a694ea8de8', '/.git/lost-found/other/71d32e4dda142850902ad5f13e7d833455cc1af5', '/.git/lost-found/other/71e14735682c30c4ee07a6cec6df1200444e6d14', '/.git/lost-found/other/71eff9cb705ba5e300fa3c97d8d889d379c26055', '/.git/lost-found/other/7205122093388382cab2ef86f8ca360144cf840e', '/.git/lost-found/other/721c0dd9c7733231be83aaabfd84464df8fb6044', '/.git/lost-found/other/7262a805bc2dddcb9400604a9c1e96b639fe1980', '/.git/lost-found/other/728c2ace778aeceb83e85f1bcde65cb271b6a15a', '/.git/lost-found/other/72b893688930c0a1af79d22f43abdb9006cee638', '/.git/lost-found/other/72bd91acc1b928d0be23a4a1256e69866fef734d', '/.git/lost-found/other/72ebd6a7cfdb38fcc2e0b29564a3b301f7782e32', '/.git/lost-found/other/734c82bc74fe1b035bf19a2c11233de87a528867', '/.git/lost-found/other/736a5f16704e8ac0e55a5a0eb3ca0341a6876e2b', '/.git/lost-found/other/738f6025afd72bb0175981a02cdbe76332d58329', '/.git/lost-found/other/739407bd14c0325d37aa5425b9ba3a92ddd47492', '/.git/lost-found/other/73dbad59cff4bd2f2c9349d428ea128acd9bff1c', '/.git/lost-found/other/73dfb5017aa8a0422396ca3bab010f8b0cf8340e', '/.git/lost-found/other/73fa97fd287d2dbdf544f5995bf4f80996e8dc14', '/.git/lost-found/other/7430dfa1e58986db8aacad7d76e64ea2a4a867eb', '/.git/lost-found/other/746b115d9387d45539bfaa7450c2d5af731614ef', '/.git/lost-found/other/74a77663a7cdfae6de127ccbfd7657aa043d6968', '/.git/lost-found/other/74c55be61fc8e1927fa6bf118fe52417a16ea98e', '/.git/lost-found/other/74ee664d939f3792fbf8c5de69ff5000a85e823a', '/.git/lost-found/other/74f0c172448a0aa50fb351f2512e47ab598c02ce', '/.git/lost-found/other/74fe5ea272dbcc8fddcdda0f3dc95a4baf6cc2d5', '/.git/lost-found/other/7521408ed06b94dc61465eb18f0de0112d662dfd', '/.git/lost-found/other/754093e7ab1ec13ed0596ba6c02d18dfb8f63104', '/.git/lost-found/other/75526bb0823b577cea9abea7a8e2d68880b4a56a', '/.git/lost-found/other/7563c407d2437ca7e9fe67a0bdcfbe9439559381', '/.git/lost-found/other/757a9f890df07ca2d991d61cbaabe564c1e908eb', '/.git/lost-found/other/75c449fb1c46c708d4282f2fc0c05d84b330728d', '/.git/lost-found/other/75ce886dd4b67eacf026e8976df7fdebbd4bbf15', '/.git/lost-found/other/75e403200b7c6f1e192ff409078d9539db59d5f9', '/.git/lost-found/other/75e83fad04dd51437daa3c32f8f69a6d0f1327c1', '/.git/lost-found/other/762405ef38fefcce716ce0ce148eeeb530e1e89a', '/.git/lost-found/other/763ddec02d2f9992db9e15ccdd04bc7a7eaf6b88', '/.git/lost-found/other/76645041e232c0adaa22acfe2ec719c5a504da3b', '/.git/lost-found/other/766c4871825fe6833348baad04d8aa11521a76c0', '/.git/lost-found/other/768bd9115951b30cf63873a24273425fea0d9460', '/.git/lost-found/other/769c1bb07714a82c3cd25c50f256f28519da231c', '/.git/lost-found/other/76d1f0ada5f99a0596db6f9b5f474d237450a49a', '/.git/lost-found/other/76fe1b6791b8ade1abf97bc01a4f669ca22bdf25', '/.git/lost-found/other/771d4dfee6367426c05c3d82559b5c866bf59ed8', '/.git/lost-found/other/77349909732fef77c64241e680e95994b7ab6894', '/.git/lost-found/other/7758d6660a098f9b40547314cac71582703a5c42', '/.git/lost-found/other/776a4bea95d8e9f4deeb6e136104a5d9080dbf4b', '/.git/lost-found/other/7776476fe91837a89851f29a87883844a29f1065', '/.git/lost-found/other/777c96837cb78e1e50a9d82e0c0bf6c555dba8a3', '/.git/lost-found/other/77de4ba2f2aef9696037ea20f5e791ec8fc33796', '/.git/lost-found/other/77e3948ebbd8863edb49b35b86613591d4c3a2fc', '/.git/lost-found/other/782871526d2a991f40100b5e32cd3ef1fa465125', '/.git/lost-found/other/783170539a1f735ce74f00faf966344072add26c', '/.git/lost-found/other/784048e81a3c695bf56127d23ce99557dbf5795f', '/.git/lost-found/other/784354371cba3231fbd5c9e2238ecabb9294c35f', '/.git/lost-found/other/78597a307d1679b079e99777b55023130a6905a8', '/.git/lost-found/other/78dda83637c001a3bbb5b46fbed552151ed51365', '/.git/lost-found/other/78e7d0c901ee8eeda3825be8d83a7bd2a65ac2c8', '/.git/lost-found/other/790cbbdb4670edaa8647b93e6e6c5a9fc4aaac3a', '/.git/lost-found/other/794f8566651960a583962f1445dd3f2b2cec3a1a', '/.git/lost-found/other/79824891a2ff44dd5a6b02039d317d363d9acc31', '/.git/lost-found/other/7996e753f0d39ff8510fa714661f86e7b916a821', '/.git/lost-found/other/79ae734789ab6ce0d184cc720e51c101d3ee0f59', '/.git/lost-found/other/79d34e1c1b4ef979275fb6c28c00dcc936dbbb31', '/.git/lost-found/other/79e13fdae10173de3edfc81b7d1f5cf09e950ccf', '/.git/lost-found/other/79f4d07757c8ada811eacfaa0ffc677b0b6993c4', '/.git/lost-found/other/79f69779814971b10ed2d61cb420b58981837c5c', '/.git/lost-found/other/7a37e0c59d04f44e91bee825ca3178653503fe27', '/.git/lost-found/other/7a60567d3255257a8ec8ffd90b47253fbb7779e1', '/.git/lost-found/other/7a72a47df56ffd23bb383a56ae637e4045424316', '/.git/lost-found/other/7a761a5bd14d2eb15e7fc3dfa4290f5d112ec66c', '/.git/lost-found/other/7aa8a776509d35c4b416ce478c310947105abb78', '/.git/lost-found/other/7ad2274d82286b18ce5a0790edb400eb0246c04f', '/.git/lost-found/other/7ad4e5dfb7fe46e62e7ee90c8437b3cd1c98569e', '/.git/lost-found/other/7af76ad5f51ab852da29c8d0a5e75dd9cca94159', '/.git/lost-found/other/7afee14e783f58433d2ed72b25963ebfcb9ebd46', '/.git/lost-found/other/7b00b279b725540bd5e801557be40c425fec033e', '/.git/lost-found/other/7b554508a7883735a7262ffdb1925e70187a153a', '/.git/lost-found/other/7b6cc09cce20fabad0e43645e6521e9c01be4a1e', '/.git/lost-found/other/7b8bcda56aa1fb97e405498e9e342bde05c8863b', '/.git/lost-found/other/7b92ce8b462acb10ee7b3cd6dc02c7d60ed4526f', '/.git/lost-found/other/7bed1a58912ef89bb40536ec81317ad4e857a3af', '/.git/lost-found/other/7c054b66a898848ce6abc261795be460993ac3d5', '/.git/lost-found/other/7c31bb200ac9ee3c8526031f3f462dcfbc0c6dcd', '/.git/lost-found/other/7c5bff6ad3b31492b0ea35a60e3b1d567f5ece3e', '/.git/lost-found/other/7c63e8f7e164de6eac3bf0e4c2c3b86a7006969d', '/.git/lost-found/other/7c6466d64311464b5cc235f012e7eefa7a3f7dec', '/.git/lost-found/other/7c7106db340073127212c46b54764a7d5c52e087', '/.git/lost-found/other/7c7e207d982350b509a2ff479318fe62ed1103fd', '/.git/lost-found/other/7d096caa38d54e011864833826dae24415d66cbe', '/.git/lost-found/other/7d1fa3cfc7a26b23468ef0231a6be425c10c39c0', '/.git/lost-found/other/7d81eca17a7079421b153be35661242578b7fe4b', '/.git/lost-found/other/7d98aa8ec82c154d18bf0e39b24127fd2869c35c', '/.git/lost-found/other/7dff8c856fc62009ba04eab81b3d92ea8b342e7a', '/.git/lost-found/other/7e3e2c020369ec22896955e111fb75738e082b9e', '/.git/lost-found/other/7eaffe3bf399b2a747c76d625eed26950f8832be', '/.git/lost-found/other/7edc089948c55fed4ed96c4947d60561584833d4', '/.git/lost-found/other/7ee4ad885aec0b6786ee1a6ea747a4f012e0478b', '/.git/lost-found/other/7f17877bb03dc7a4b1da8e34bd24c635c8f1fc85', '/.git/lost-found/other/7f1ccef0257eae07e1a9d96c9a419839eb69012b', '/.git/lost-found/other/7fa989db3783a9017443ea55642686cebe2d31bc', '/.git/lost-found/other/7fb7f2e1a4f005e0ed97213f366b2a44d2b5f65a', '/.git/lost-found/other/7fbedd5325332884808b4f13376b20b608ba153d', '/.git/lost-found/other/8039eca3d631d25a1a6d81d08eff05b10453a080', '/.git/lost-found/other/80417b62ee231928cf6e1894ee78ae9d52dced8f', '/.git/lost-found/other/80525b0220584bb2859e90b7b1ecd96124809e0c', '/.git/lost-found/other/805a2540e6e5e0069b0845c8c0d64cc013c0c921', '/.git/lost-found/other/806c3e29a41d7902dc4bfb90b274f7bcdd692396', '/.git/lost-found/other/807fe9f45b577f7b4e832f53598c9132f4634217', '/.git/lost-found/other/80aa6242175a7dfe9cc180151a3c2506287ed78e', '/.git/lost-found/other/80b101102e4af9e39d14d4724273ad6c8673bf8b', '/.git/lost-found/other/80be9d64780cb8215aa9e33cc9f7225d9e763c45', '/.git/lost-found/other/80c7cbf169b9a7de67f1c1d510ead12a86092a6a', '/.git/lost-found/other/80d57ddd52a3d347c46ca1ec7bd6611c3832991f', '/.git/lost-found/other/8135df1518b818e32969ee29a72deecb538a4932', '/.git/lost-found/other/81919ab913ed8acf77c6c0d10a4011b81929dd15', '/.git/lost-found/other/81a82ea2302eda7a5d9cfc93dc15d7aac51acb7b', '/.git/lost-found/other/81b0c9d26060eac103e503fee24c4dc875d73a3d', '/.git/lost-found/other/81b84d2f9246fe95414efaf594ce0d66642af224', '/.git/lost-found/other/81c8e0c1332f8beac34dab5b2d8addd868c78d37', '/.git/lost-found/other/81c929641ff4bb9378d8f539707794ef0bbc35ab', '/.git/lost-found/other/81d135cdcdf753f12ffe7875cd8b84a1aa949a33', '/.git/lost-found/other/81de4211ddd55af9724945af37c733222887a4a9', '/.git/lost-found/other/8208ad133751cbfe78ea16f128cd7bbc1d8c8384', '/.git/lost-found/other/823eb92c648fdf767079c3d6ce64a4e1acfd1d51', '/.git/lost-found/other/824f35363eb09575efb61b59e2a3f4a491629ff3', '/.git/lost-found/other/827a08acc83b7c7a0ccbc1e77bed49435faa6c14', '/.git/lost-found/other/82a5b244d810b0f28e1c0ed826c6b90c3fcdeb69', '/.git/lost-found/other/82a62bb26671ed1e264c244a53da765fdfb6b534', '/.git/lost-found/other/82d66f9855421d3b02581bf6cc776b9401f31a91', '/.git/lost-found/other/82fe660600bda9fb261c64b3d868893a616c6f6b', '/.git/lost-found/other/8326d463947af356e07709d303b413cf1e06dc28', '/.git/lost-found/other/8327ca0d029a9aa0dc380a0ecd1a1ba295fdb6f2', '/.git/lost-found/other/8329fb9ca2717aaf3c0f538bda50030d0f9a88a6', '/.git/lost-found/other/83522d5d571930293dee7c041f9baa0d8c5be22e', '/.git/lost-found/other/83793f9f677aef3ad5f0496d7189d41a71f84c46', '/.git/lost-found/other/838b4934b5ce8b997c97a179ae31efe0df8d69c3', '/.git/lost-found/other/83a1cd018182bd007961c0c1a384f90721538a41', '/.git/lost-found/other/83f433e75ff687ed7ad6e622082b3771f4be902a', '/.git/lost-found/other/83fcd0a4b90b111dd78f24830b0cf0fd6f6662e5', '/.git/lost-found/other/84032ab70aec1220efafe862badb544ab9136474', '/.git/lost-found/other/846fd5afd14b372c7b10c236929e87409bd9ff93', '/.git/lost-found/other/8479528c7d38418a08b92817a5605425c6c65ea9', '/.git/lost-found/other/84a3459111e3b7fc5e8b3db7becf37841bb9af09', '/.git/lost-found/other/84e98f7d23fd1e49868aad7b88e4c25ce27b5f98', '/.git/lost-found/other/8506bc72a2d41cd6d60a4fbb7e3e3e441c831ea6', '/.git/lost-found/other/8507cc0d8827de0caf78209b1bc8b409c30929c3', '/.git/lost-found/other/852f59ef505774d2e1cded9189583af9a7fabfbe', '/.git/lost-found/other/8530702851e912a09461c1b3641ed4447c267bf6', '/.git/lost-found/other/856a9d9a9af9342cb38e84fb97d0ec8be25c4979', '/.git/lost-found/other/856aa17c270d6d6f2b9f0df34ac3aae243b43f0e', '/.git/lost-found/other/8575593501bfc3c1fb9f444dfce8ed8866d583aa', '/.git/lost-found/other/85775c0cf59c7c0a7c8c01be3dc92e2b76038b2b', '/.git/lost-found/other/85888b8c832f86d827cb9fc78205aac1c40bc919', '/.git/lost-found/other/85911b7b0a87b6ef634ba88ee35c9ea798547413', '/.git/lost-found/other/8598ecf10a790316c773068fc621b1ec6a8c7462', '/.git/lost-found/other/85cf7fffe0d71feeb57e13553129f631dd706fe2', '/.git/lost-found/other/85efd595e03f195168517e451a0f6351e2f9e69f', '/.git/lost-found/other/85f0a8f1420aabbd7a4472ee3ed2f9d968be657c', '/.git/lost-found/other/8636b42068ee84f766948b4f22e52bc3280e9eb7', '/.git/lost-found/other/868d17c19fc94e4da1a657e07258f027e37a183f', '/.git/lost-found/other/877dbd89e8209c09b4e6117d45aa1ffa5c29123a', '/.git/lost-found/other/878572383d5cca030620695db137e5d8befb60e2', '/.git/lost-found/other/878ec5f103298fd245bffbc77e9b4122705d6caf', '/.git/lost-found/other/87a3f4559d75c1fce1baae89b3777b9bef57f4c6', '/.git/lost-found/other/87b4d789046bbf43385acd61e5c3e70a1bec50eb', '/.git/lost-found/other/87bdeed1fa7053bf3f3ee36c8996eb1a85ca4581', '/.git/lost-found/other/87c156c8531b9854f8913b8ca70249dacd305771', '/.git/lost-found/other/87f508dde1d80fd527a62801ed475fdcfa1199d0', '/.git/lost-found/other/884ad461f9de46bba7b5fb8b37d1f4fb913b128f', '/.git/lost-found/other/8862c16224430bf0aa6f410ce9df8777453427c3', '/.git/lost-found/other/888114b868b7b1a10c7b8aedadfab6a0b198d938', '/.git/lost-found/other/88a12ae4891c84ce446aaf38698e7f684d05465d', '/.git/lost-found/other/88a57a29b1fe7fc24955b3c475d2587cfc2b2168', '/.git/lost-found/other/88c4d478b40dec9953b90c124136cb8ca6aabac6', '/.git/lost-found/other/88de5d8898855804a10e46a2b8ed2efdded56c2d', '/.git/lost-found/other/88ee53c9ece8ef43612f9db4cc25aa5614aa26ad', '/.git/lost-found/other/8969067bcbecde61a44d7cf0f5d364fe265ac08a', '/.git/lost-found/other/896dd57e7a94ddfe4430921fddcf78e252b7053e', '/.git/lost-found/other/8972d0e0bf6c14c869c716e06845e43ee7d373ed', '/.git/lost-found/other/899125167a136688cdca3cfc2a02bd8767aae87b', '/.git/lost-found/other/89a8667eaaa858b441ca2b4cf8f783a98017c631', '/.git/lost-found/other/89c09fa5bbb4ec88f5f5586334bbc9b5ee4def63', '/.git/lost-found/other/89ee971a3b572fa574374f7d8789267118bfdc5d', '/.git/lost-found/other/89ff128aa63e61990193840dfa90762d4f8f3652', '/.git/lost-found/other/8a1b068cf37d71278de5478ecea3b17e478bc53a', '/.git/lost-found/other/8a2e1744f8d60b47acee31323eb9be5252f3bb71', '/.git/lost-found/other/8a5e5ad2e568b464c38258b18b07105fa93c8eeb', '/.git/lost-found/other/8ad6631101557add7e9f03d4438ee6d4bd81fcd1', '/.git/lost-found/other/8b0fe43b479ecc9b599ccb21386dcf6243fab6ef', '/.git/lost-found/other/8b166483db6ab554b4ed7cfa227dcec5c0b5c4d1', '/.git/lost-found/other/8b474e9468a368ca615b1d5b7e8ae43995e7ed6b', '/.git/lost-found/other/8badb259266160ed2ae90c6d544e84c1f16bdfa2', '/.git/lost-found/other/8bc007bd8099a368761f7a85d69e8c62e91751d7', '/.git/lost-found/other/8bd53ac2f88091ca967b218668ddeb2b8b901b3b', '/.git/lost-found/other/8bf56f827628f29cc78ef7e19693f5b957efcb55', '/.git/lost-found/other/8c032fd3bc85f561863400e177168dcf3ace645e', '/.git/lost-found/other/8c193116cbb53901051d2a1d16301a18a0dcefcb', '/.git/lost-found/other/8c32101bf52c685290b17f8f9152446952caaef4', '/.git/lost-found/other/8c532b7669a3fd0dc35dabdd43d2b34db2726089', '/.git/lost-found/other/8c768de675b19dbd6d0328fda1e54fd350b3621b', '/.git/lost-found/other/8c7f0d1ecd32895777182562810997d842a1cc5a', '/.git/lost-found/other/8ca05df80017a216b6e9c040a13de4ef1c762f3e', '/.git/lost-found/other/8cdaba2214ca080e13141a212a14fa3492dee9a6', '/.git/lost-found/other/8cea1e553faca94727050f1666f760a5b579a34d', '/.git/lost-found/other/8cef1dc2bb0c10cac3165c3672402be4fe31054c', '/.git/lost-found/other/8d39cd48167f79c08783e996e5054ba4430f3918', '/.git/lost-found/other/8d87692ec4508add82fc7bcfb11627594c76759f', '/.git/lost-found/other/8db2dc5e2da502d8be60f83c29b6bd8cdece283d', '/.git/lost-found/other/8dcf63db4819ce835831f19b7f843f66cf331057', '/.git/lost-found/other/8de773e9097a8f0dcbed369e6c3e3f3dd481cb8d', '/.git/lost-found/other/8dfb262567a945bd38c2f444dd5a91c0c674ded1', '/.git/lost-found/other/8e147d7dafa9de53bdfdf1afdd2288c7015dab9b', '/.git/lost-found/other/8e1df140ffb6a1a2e0e1dbc48231a1341416d5ef', '/.git/lost-found/other/8e30c681e95c989c9194668613784ec1fb70c362', '/.git/lost-found/other/8e508aca87513c614f529e35534a6f510f5fecc4', '/.git/lost-found/other/8e624b995ed2e8b2f8a1fde05616b92165f1b612', '/.git/lost-found/other/8e6e6dca3e2142e6450e31de9dcc15e1315d11d1', '/.git/lost-found/other/8e886852a0b8f8effe43f3249827b417df2987c2', '/.git/lost-found/other/8e8cc43769b3e51927bb486257e5d2389bdfe3e7', '/.git/lost-found/other/8ed2f0dd8617bf639e3528efcc136bd64ff48295', '/.git/lost-found/other/8ed475a3ae2bbea45fbe48ab50f5ea73d830fd2f', '/.git/lost-found/other/8efb95334e4dfd7238406b637b87d38bc7df7971', '/.git/lost-found/other/8f29fcc619ffc635697fc2d2d468888819a7c05d', '/.git/lost-found/other/8f5819fda3698f87172becd15cd54ad20cdbc350', '/.git/lost-found/other/8f872767673fc75e5c1421d89521e998af4f8d39', '/.git/lost-found/other/8f8836cd2c592cc7a626577ab0c78aa97314cb80', '/.git/lost-found/other/8f8a2153b54a03fb30f2d21c11b2fc65b5071796', '/.git/lost-found/other/8fe85b124c02b0a063a255461fdcf4462b871849', '/.git/lost-found/other/9025e7e99615220286bf75c93d3246d302f1375a', '/.git/lost-found/other/903e19a32e203d03671b31f6e27ebaa907166d90', '/.git/lost-found/other/9040ad1040d2f81d6eba6d481dc29f2a5f5b2f73', '/.git/lost-found/other/9052c9897d84020cc14786b82536af8a94cad0e3', '/.git/lost-found/other/910bcc380d91aea78d4bab200472aee82a8e9f96', '/.git/lost-found/other/91129c883e5f0e47819acbc2aad8d6314c0310a4', '/.git/lost-found/other/9117e524aeb011990bc54777f70d56955ef716a3', '/.git/lost-found/other/9124c4e8d7b6925e2de9f96ba7ee66e9cfbd5b4f', '/.git/lost-found/other/91364a90eb688a950083474549ee42e8e0eaf78f', '/.git/lost-found/other/91501834e260e8d218dadf002c167daf1d7a99e4', '/.git/lost-found/other/915fd7b0567afe8725f78a286a8d8155d5b1a361', '/.git/lost-found/other/91897ad77d725aab215d18fc41d34a68ad6b142b', '/.git/lost-found/other/91a71c4d7e7cc2cc27852d2b1a6c5a1931fa1f11', '/.git/lost-found/other/91d3aafcff2a3ea74c1cfa946fa955c62abd89c2', '/.git/lost-found/other/91e214a28a493c3c2e35325fb7245d6983ea71ca', '/.git/lost-found/other/921a6caed41c95b6bba1e56724fe34b038245416', '/.git/lost-found/other/92301588927b94a7a8d688c5220721145e377e38', '/.git/lost-found/other/923210f734a2e995f200388e83d5fed3cf26053f', '/.git/lost-found/other/924d93052389d0b9434705bfe32ef317528044d9', '/.git/lost-found/other/92612a56a21f153339abb5c4efb074765d36aceb', '/.git/lost-found/other/926e20ae59a15432cc966c029407288466bdcddb', '/.git/lost-found/other/92dc8ccd7943e2b3163be459d4fb36f013ffff6d', '/.git/lost-found/other/92f0a102283a69d06abb892c5d78980a6a4d2652', '/.git/lost-found/other/932ab411aba0a979eb6a54f3c43832011843338f', '/.git/lost-found/other/93424d534c936bf6e468285533db39e19a47cc4e', '/.git/lost-found/other/93767a88113b92a54fdb35d82ba698c50f0af898', '/.git/lost-found/other/9387b3fd7de48b7e14efafef2ed67c4eb5015716', '/.git/lost-found/other/939be16e271fbe69d578fdb0ef909996a506933e', '/.git/lost-found/other/93c6ae943c48d1c8fe60cf11e869de7401a70e9d', '/.git/lost-found/other/9437d9d6ad6a559a5d535231870cc81d2e5f61e2', '/.git/lost-found/other/9441b1dcc2d951a7881cdde15f1bb4aa78e01801', '/.git/lost-found/other/944e4ac44eaf17d1c2a0a2149c670b79db3b81bc', '/.git/lost-found/other/948a2574e766a7def043341e9d592244e5f656cd', '/.git/lost-found/other/9494d7d02c4efa7814192147f9cd95198b968706', '/.git/lost-found/other/94bf9b9cb3ad20e5e40e68b19d2d967351fd7043', '/.git/lost-found/other/94ddb92592b2844dab2a6dbf6b54c3ec65c53adc', '/.git/lost-found/other/94f86597692644521fcb91b65ebfa1d6698b721e', '/.git/lost-found/other/9523046c930fc423ff2f2d964b0ad1f0f8dcc561', '/.git/lost-found/other/952dad6cd5e0a77bbc998b01cf76b786dcf86bd2', '/.git/lost-found/other/953728dff60b9ee56f8f94c427b6512b881a532f', '/.git/lost-found/other/9596ea8c380e21e2936eebc4d43cc3da5c3945dc', '/.git/lost-found/other/95b3c141d6f33fa02247dc87531e793b05061531', '/.git/lost-found/other/960849ac9a576a80ffaaf0a558644a959e85d725', '/.git/lost-found/other/962e546dcc1ccf96804fc035e0c053e640867b9e', '/.git/lost-found/other/9683a32d2a5b6572a83f7b012fa1bf38660ae712', '/.git/lost-found/other/96947147a4afca1db6085e927b1a9a03d61ffd73', '/.git/lost-found/other/96b583ead2754801cabadeaa6310962d9484b35c', '/.git/lost-found/other/96c55467020eb5967190ef67ea5af73bd8557293', '/.git/lost-found/other/96f0c3a29711baf739f8d206549147833769309f', '/.git/lost-found/other/96fd88067893385c0765030c47af266de862e670', '/.git/lost-found/other/970b3536b39e69354428d28cb4461dc2b51077a4', '/.git/lost-found/other/979c845eeee9c7ea69e9be82ea0152129d99ab94', '/.git/lost-found/other/97ade8382b5461f3e7dba16ee4cb7b21e3428693', '/.git/lost-found/other/97b5c66faefdec6e1e3f9511ffa5352ba6aed231', '/.git/lost-found/other/97d1c714bdd88d2c18292f04270b1d088b7ab423', '/.git/lost-found/other/98330f2a74870e2eacf010a3dc6ebf02ba786210', '/.git/lost-found/other/984da4d425592c6728086f770d46015c2774fb7f', '/.git/lost-found/other/98570cf2f3892aeb6a60317d3c5f2395551fa126', '/.git/lost-found/other/98634d3201e655b428c3720dfc45a1deaf0fd370', '/.git/lost-found/other/98a5ec496c33e52dbeece3cd0ce79df9d837d56b', '/.git/lost-found/other/98b214d389c3b000b67c73ef23a93e020caa45ce', '/.git/lost-found/other/98d9cd7743f231620723d495810cd1f76180c10e', '/.git/lost-found/other/98ddac6847239f0b68e04184b7c57cbffa12398f', '/.git/lost-found/other/98e1a00c29c13261193d33d35e8b870695aabfbc', '/.git/lost-found/other/9900a37055c69f4e8b8b84d6c679c7340cf21a2a', '/.git/lost-found/other/990b82d5c7737e7d79db4d7ee986945bee8c8b04', '/.git/lost-found/other/9964532f1952d9499823130c76cd62602dea68b4', '/.git/lost-found/other/996acb6402c94e8606049daf81862a1b810911df', '/.git/lost-found/other/996fca5689f017cbec23de29b1c8f9dc02a3b8e2', '/.git/lost-found/other/998187ffe021319b3cd3f43f9d7f7abe4aba6b90', '/.git/lost-found/other/99c369006665885b83433b1cada3e5998e5155b2', '/.git/lost-found/other/99d222d5d2d4742cfd70b247b8bceadd95fc4706', '/.git/lost-found/other/99e9be780090b056920e343370328c22ba0ecc8b', '/.git/lost-found/other/9a0d0a46f1f98aeebacd8915237221e8debc95fc', '/.git/lost-found/other/9a3ecb7700bef0e0c4bd76dd2a5bbe456f4eb302', '/.git/lost-found/other/9a4616a547f0ed364e71860ef4ffc26169a6f73c', '/.git/lost-found/other/9a94aec61779e9b91b8ab36885ab378ed5381c05', '/.git/lost-found/other/9a9a7e3f5a41b5c06d2f01bae830cafb07662606', '/.git/lost-found/other/9abb4897f6f8e61f116f836df7fc815e683a5611', '/.git/lost-found/other/9ac9a25da69a69c9c6ecb565b8e855d3d39d4dd0', '/.git/lost-found/other/9acd9309209b08b5353508e51b9107bb633a3b64', '/.git/lost-found/other/9ad7f9e4369acab40cfded3808876b7574f9390b', '/.git/lost-found/other/9ae4de87cb7ccdf07bb847d053307a3ab4196481', '/.git/lost-found/other/9b135bc75fb31913ebac007ca795c8a3e4e48b59', '/.git/lost-found/other/9b14110138d38f3594da82ed0abfb4d21ebdc2d4', '/.git/lost-found/other/9b151ebe22fb8c68a8f49571c62ea3f3f871c496', '/.git/lost-found/other/9b3627817278c3f1ea9f6f4fe2f8301d898b829c', '/.git/lost-found/other/9b4e06037e8da97ab1ce8591a052374860695c5f', '/.git/lost-found/other/9b6792f2b4c9ff8862bce79bb1422fe2735f6917', '/.git/lost-found/other/9b6a05c434791a48c447099ee3ce5ec6b9e1f586', '/.git/lost-found/other/9b79025bbb1e34766f6443b40eb90bb0bba6c9dc', '/.git/lost-found/other/9badb09849de0c3f46533ec92a264f923bc149b6', '/.git/lost-found/other/9bdf7450b467a385642426ac89ef2005f566bba0', '/.git/lost-found/other/9bf0e2c09edf77769e6856ecc475bb3bb86e45be', '/.git/lost-found/other/9bfa97bbb437b4b931b0f513c1a1e9c010d63eae', '/.git/lost-found/other/9c02ba73b9be8a9da49a3b46b30d7c34bc0517de', '/.git/lost-found/other/9c15049e5cfa12c8399e9351b7c79a3c5c0a35dd', '/.git/lost-found/other/9c27c00a245e6db44d7f5dc05a9cda11bd241541', '... [results truncated, try being more specific with your parameters]']
AI: Let me find the actual project files and the specific matrix batch range.[{'name': 'glob', 'args': {'pattern': 'inputs/**/*', 'path': '/'}, 'id': 'call_00_2Xeqm2DvJASGKZBV65d65236', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'outputs/**/*', 'path': '/'}, 'id': 'call_01_ZTcljk1ZYFbg8sVqH4Iw8736', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'skills/acquiring-discrepancy-analysis/**/*', 'path': '/'}, 'id': 'call_02_XpQfdyZoVNUSlcyi4T3p3794', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/.venv/Lib/site-packages/langchain_core/outputs/__init__.py', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/llm_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/run_info.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/chat_generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/chat_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/llm_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/run_info.py', '/outputs/working/bootstrap_report.json', '/outputs/working/build_coverage_ledger.py', '/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/coverage_ledger.json', '/outputs/working/enrich_propositions.py', '/outputs/working/legal_propositions.json', '/outputs/working/working_artifact_validation.json']
Tool: ['/skills/acquiring-discrepancy-analysis/SKILL.md', '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/matching-rules.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md', '/skills/acquiring-discrepancy-analysis/references/status-rules.md', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/bootstrap_source_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/export_review_xlsx.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/finalize_discrepancy_json.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_coverage_ledger.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_source_numbering.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_working_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/bootstrap_source_artifacts.py', '/skills/acquiring-discrepancy-analysis/scripts/export_review_xlsx.py', '/skills/acquiring-discrepancy-analysis/scripts/extract_docx_numbered.py', '/skills/acquiring-discrepancy-analysis/scripts/finalize_discrepancy_json.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_coverage_ledger.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py']
AI: Good. Now let me read the key reference documents and the existing working artifacts to understand the current state.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/matching-rules.md', 'limit': 500}, 'id': 'call_00_So6HNsGGnGCQGqDwNhsi2565', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/status-rules.md', 'limit': 500}, 'id': 'call_01_1RZM0wSR5WuaoXoV5k0Z2446', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_02_R2BfgH09kJgM6962GdRb0324', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_03_ecQmlfgbOLx168qW2DdD4697', 'type': 'tool_call'}]
Tool:      1	# Matching Rules
     2	
     3	Read this before substantive matrix-contract matching. Use
     4	`comparison-patterns.md` for short calibration examples when a candidate looks
     5	ambiguous.
     6	
     7	## Analogue Threshold
     8	
     9	Create a final link only when the contract proposition is a true legal analogue
    10	of the matrix proposition. This protects the review from false comfort: a broad
    11	topic match can hide a missing Bank-standard right.
    12	
    13	Test the candidate against the matrix requirement:
    14	
    15	- same or equivalent protected party;
    16	- same or equivalent bound party;
    17	- same legal object;
    18	- same operative right, duty, prohibition, permission, remedy, or allocation of
    19	  risk;
    20	- material trigger, scope, procedure, and consequence are the same or legally
    21	  equivalent.
    22	
    23	Reject weak thematic candidates. A clause about the same broad topic is not a
    24	legal analogue when it governs a different object, party, trigger, procedure,
    25	or consequence. Keep weak candidates only as rejected evidence for
    26	`unmatched_matrix`.
    27	
    28	See examples: `True Analogue`, `Weak Thematic Candidate`,
    29	`Generic Product Capability`, `Framework Clause As Analogue`.
    30	
    31	## Matrix To Contract
    32	
    33	For each applicable evaluable matrix proposition, retrieve all contract clauses
    34	that collectively cover the Bank-standard requirement.
    35	
    36	Include a contract clause in final `contract_ids` only when it provides
    37	material coverage for the matrix item or legally cures a gap:
    38	
    39	- operative parent/root clause that creates the relevant right, duty,
    40	  procedure, basis, list of cases, or consequence;
    41	- child/detail clause with deadline, amount, formula, trigger, exception,
    42	  remedy, or procedure for that same legal object;
    43	- appendix/table row that contains an operative term, price, procedure,
    44	  liability, or scope item;
    45	- payment, acceptance, liability, termination, and document-exchange companion
    46	  clauses that are part of the same legal package;
    47	- framework/legal-compliance clause only when the matrix item itself concerns
    48	  that framework or the clause allocates the same risk/duty/remedy.
    49	
    50	If a child clause is selected, check whether its parent carries operative legal
    51	meaning for the same topic. If a parent is selected, check whether children
    52	contain hard terms that change coverage. This prevents losing deadlines,
    53	amounts, penalties, and exceptions that are split across related clauses.
    54	
    55	Do not add clauses that are only near the same topic. Broad background clauses
    56	can be mentioned in reasoning or rejected candidates, but they should not make
    57	the final link.
    58	
    59	See examples: `One Matrix Requirement Covered By Several Clauses`,
    60	`Parent And Child Package Retention`, `Non-Informative Parent`.
    61	
    62	## Contract To Matrix
    63	
    64	For each evaluable contract proposition, find the matrix analogue group.
    65	
    66	- If a true matrix analogue exists, link the contract proposition to that group.
    67	- If no analogue exists and the term has independent legal effect, classify it
    68	  as `extra_in_contract`.
    69	- If it is a heading, signature, requisites row, blank form, or non-operative
    70	  definition, close it as `not_material` only in the working ledger.
    71	
    72	A contract-only term is material when it creates or changes a right, duty,
    73	control mechanism, acceptance/rejection process, payment/withholding rule,
    74	liability, termination power, reporting/audit duty, confidentiality/data duty,
    75	anti-corruption duty, evidence procedure, or enforceability consequence.
    76	
    77	See examples: `Contract-Only Material Clause`, `Definition Without Legal
    78	Effect`, `Definition With Legal Effect`, `Procurement Mechanism As Extra`.
    79	
    80	## Grouping
    81	
    82	Group related ids into many-to-many `links`. One matrix id may need several
    83	contract clauses. One contract clause may cover several matrix ids.
    84	
    85	Use one group only for a shared legal package. Do not merge sibling matrix
    86	items merely because they share a parent heading. If siblings have different
    87	legal objects, triggers, channels, amounts, or consequences, keep focused
    88	groups so a gap in one sibling does not spread to the others.
    89	
    90	`atomic_links` are traceability projections of group links. They inherit the
    91	group relationship and do not carry independent final statuses.
    92	
    93	See examples: `One Contract Clause Covers Several Matrix Requirements`,
    94	`Group-Level Status`, `Duplicate Gap Propagation`.
Tool:      1	# Status Rules
     2	
     3	Read this before classifying group-level status, risk, or final missing/extra
     4	findings. Use `comparison-patterns.md` when a result turns on a common legal
     5	pattern.
     6	
     7	## Group-Level Status
     8	
     9	Assign status to the group, not to each atomic pair.
    10	
    11	- `aligned`: the contract package preserves the matrix legal result.
    12	- `deviation`: a true analogue exists, but any material element is changed,
    13	  narrowed, weakened, omitted, shifted, or blank.
    14	- `missing_in_contract`: no true contract analogue exists for an applicable
    15	  matrix requirement.
    16	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
    17	  analogue.
    18	- `not_material`: internal ledger closure only; exclude from final report.
    19	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
    20	  final report because the requirement does not apply to the current product,
    21	  lot, terminal, payment method, or legal regime.
    22	
    23	Material elements include party, legal object, operative act, trigger,
    24	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
    25	remedy, exception, Bank right, merchant duty, and consequence.
    26	
    27	## Hard Terms
    28	
    29	Hard terms must be compared directly because they usually carry the economic or
    30	enforcement risk that the Bank standard is designed to control.
    31	
    32	- Same material deadline, amount, formula, penalty, cap, procedure, or
    33	  protected party in the same legal obligation can be `aligned`.
    34	- Changed value or missing value is `deviation`.
    35	- A hard term from another clause counts only when that clause expressly
    36	  governs the same obligation or is explicitly incorporated.
    37	- A neighboring date, amount, or procedure for another legal object cannot cure
    38	  the gap.
    39	
    40	See examples: `Same Deadline`, `Changed Or Missing Deadline`, `Borrowed Hard
    41	Term Does Not Cure Gap`, `Changed Amount, Formula, Cap, Or Penalty`.
    42	
    43	## Functional Equivalence
    44	
    45	Do not downgrade for formal differences alone: heading, title, appendix label,
    46	permitted option selection, equivalent mandatory-law mechanism, or wording
    47	style.
    48	
    49	Do not downgrade for low-risk notes when the legal result is preserved. If the
    50	reason says the difference is merely terminological, beneficial to the Bank,
    51	already incorporated through another clause, or caused only by a mandatory
    52	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
    53	
    54	Functional equivalence cannot override a missing or changed hard term. If the
    55	source text shows the required deadline, amount, party, procedure, or remedy is
    56	different, classify the group as `deviation`.
    57	
    58	See examples: `Formal Label Difference`, `Low-Risk Note Does Not Force
    59	Deviation`, `Slash Options`, `Placeholder In Applicable Term`.
    60	
    61	## Procurement And Mandatory-Law Mechanisms
    62	
    63	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
    64	when it materially worsens or changes a Bank-standard term: payment timing,
    65	acceptance control, withholding right, penalty/cap, termination power,
    66	protected party, evidence channel, or enforceability.
    67	
    68	Public-contract mechanics can be:
    69	
    70	- an analogue when they regulate the same legal object as the matrix;
    71	- aligned when they preserve or strengthen the Bank-standard result;
    72	- deviation when they change a material element;
    73	- extra when they create an independent customer right with no matrix analogue.
    74	
    75	See examples: `Procurement Mechanism As Analogue`, `Procurement Mechanism With
    76	Material Deviation`, `Procurement Mechanism As Extra`.
    77	
    78	## Liability Package
    79	
    80	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
    81	Before marking a liability group `aligned`, check:
    82	
    83	- amount and formula;
    84	- cap or no-cap position;
    85	- trigger and breach bucket;
    86	- protected party;
    87	- excluded delay/non-delay categories;
    88	- claim procedure and remedy consequence.
    89	
    90	If the package preserves the Bank-standard allocation, classify it as
    91	`aligned`. If any material element is weaker, missing, or shifted, classify it
    92	as `deviation`.
    93	
    94	See examples: `Liability Group Review`, `Changed Amount, Formula, Cap, Or
    95	Penalty`.
    96	
    97	## Risk Calibration
    98	
    99	Use `risk_level` consistently:
   100	
   101	- `none`: only for `aligned`;
   102	- `low`: optional applicable missing, placeholder, formal but legally
   103	  manageable gap;
   104	- `medium`: material deviation that can affect performance, evidence, payment,
   105	  control, liability, or enforceability;
   106	- `high`: mandatory missing, changed protected party, major payment/remedy
   107	  change, important Bank right omitted, or broad contract-only risk.
   108	
   109	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   110	a short evidence-based reason. Use concise quotes rather than long excerpts.
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
   216	## Minimal Traceability Example
   217	
   218	Use this as a shape example only, not as a document-specific answer:
   219	
   220	```json
   221	{
   222	  "links": [
   223	    {
   224	      "matrix_ids": ["matrix-payment-deadline"],
   225	      "contract_ids": ["contract-payment-clause", "contract-acceptance-clause"],
   226	      "relationship": "deviation",
   227	      "legal_topic": "payment deadline after acceptance",
   228	      "matrix_standard": "Bank standard requires payment within 5 business days after acceptance.",
   229	      "contract_position": "Contract links payment to acceptance but gives 10 business days.",
   230	      "matrix_evidence": "payment within 5 business days",
   231	      "contract_evidence": "payment within 10 business days after acceptance",
   232	      "status_reason": "The same payment obligation is covered, but the deadline is longer.",
   233	      "risk_level": "medium",
   234	      "discrepancies": [
   235	        {
   236	          "type": "deadline",
   237	          "description": "Payment deadline changed from 5 to 10 business days.",
   238	          "risk": "Longer payment timing delays Bank-standard settlement economics."
   239	        }
   240	      ]
   241	    }
   242	  ],
   243	  "atomic_links": [
   244	    {
   245	      "matrix_id": "matrix-payment-deadline",
   246	      "contract_id": "contract-payment-clause",
   247	      "relationship": "deviation",
   248	      "link_index": 0,
   249	      "coverage_role": "payment",
   250	      "coverage": "sets the payment obligation and changed deadline"
   251	    },
   252	    {
   253	      "matrix_id": "matrix-payment-deadline",
   254	      "contract_id": "contract-acceptance-clause",
   255	      "relationship": "deviation",
   256	      "link_index": 0,
   257	      "coverage_role": "procedure",
   258	      "coverage": "defines the acceptance trigger for payment"
   259	    }
   260	  ]
   261	}
   262	```
   263	
   264	## Excel Output
   265	
   266	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   267	
   268	Sheet 1: `Contract-Matrix`
   269	
   270	Columns:
   271	
   272	1. `contract_id`
   273	2. `contract_summary`
   274	3. `matrix_ids`
   275	4. `status`
   276	5. `risk_level`
   277	6. `comment`
   278	
   279	Rules:
   280	
   281	- one row per group-level contract-to-matrix finding;
   282	- `matrix_ids` contains the full matrix id set for the group;
   283	- status is `aligned`, `deviation`, or `extra_in_contract`;
   284	- contract-only extras have blank `matrix_ids`.
   285	
   286	Sheet 2: `Only in Matrix`
   287	
   288	Columns:
   289	
   290	1. `matrix_id`
   291	2. `requirement`
   292	3. `required_type`
   293	4. `risk_level`
   294	5. `comment`
   295	
   296	Rules:
   297	
   298	- one row per final `unmatched_matrix` item;
   299	- include optional applicable missing as low/conditional risk;
   300	- do not include out-of-scope / not-applicable requirements;
   301	- do not include non-evaluable headings or purely technical rows.
   302	
   303	## Bad Output Patterns
   304	
   305	Do not output:
   306	
   307	- multiple competing final JSON files;
   308	- pair-level final statuses as the primary answer;
   309	- `deviation` for unselected slash alternatives;
   310	- `deviation` for heading/title/label changes alone;
   311	- final `unmatched_contract` rows for definitions without legal effect;
   312	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   313	  requirements;
   314	- final ids that exist only in helper scripts or working ledgers;
   315	- `extra_in_contract` with empty risk;
   316	- `aligned` with non-empty discrepancies;
   317	- `missing_in_contract` where a weak candidate is silently treated as a link;
   318	- final conclusions based only on extracted fields without source-text evidence.
AI: Now let me read the existing working artifacts and the matrix/contract inputs to understand the current state and the batch I need to work on.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/coverage_ledger.json', 'limit': 200}, 'id': 'call_00_BWRsBn5EQI9sDLTFRDDt7071', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_01_GP432b0fHyHZurH3xSVJ6060', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/working_artifact_validation.json'}, 'id': 'call_02_eNnmmFjwQUBY7uRCCjzO9950', 'type': 'tool_call'}]
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "matrix_id": "2.1",
     5	      "closure": "linked",
     6	      "link_indices": [],
     7	      "reason": ""
     8	    },
     9	    {
    10	      "matrix_id": "2.2",
    11	      "closure": "linked",
    12	      "link_indices": [],
    13	      "reason": ""
    14	    },
    15	    {
    16	      "matrix_id": "2.3.1",
    17	      "closure": "linked",
    18	      "link_indices": [],
    19	      "reason": ""
    20	    },
    21	    {
    22	      "matrix_id": "2.3.2",
    23	      "closure": "linked",
    24	      "link_indices": [],
    25	      "reason": ""
    26	    },
    27	    {
    28	      "matrix_id": "2.3.3",
    29	      "closure": "linked",
    30	      "link_indices": [],
    31	      "reason": ""
    32	    },
    33	    {
    34	      "matrix_id": "2.3.4",
    35	      "closure": "linked",
    36	      "link_indices": [],
    37	      "reason": ""
    38	    },
    39	    {
    40	      "matrix_id": "2.3.5",
    41	      "closure": "linked",
    42	      "link_indices": [],
    43	      "reason": ""
    44	    },
    45	    {
    46	      "matrix_id": "2.3.6",
    47	      "closure": "linked",
    48	      "link_indices": [],
    49	      "reason": ""
    50	    },
    51	    {
    52	      "matrix_id": "2.3.7",
    53	      "closure": "linked",
    54	      "link_indices": [],
    55	      "reason": ""
    56	    },
    57	    {
    58	      "matrix_id": "2.4",
    59	      "closure": "linked",
    60	      "link_indices": [],
    61	      "reason": ""
    62	    },
    63	    {
    64	      "matrix_id": "2.5.1.1",
    65	      "closure": "out_of_scope",
    66	      "link_indices": [],
    67	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
    68	    },
    69	    {
    70	      "matrix_id": "2.5.2.1",
    71	      "closure": "out_of_scope",
    72	      "link_indices": [],
    73	      "reason": "Matrix requires payment method \"sber_pay_face_scan\" but contract uses cards, qr"
    74	    },
    75	    {
    76	      "matrix_id": "2.6.1.1",
    77	      "closure": "out_of_scope",
    78	      "link_indices": [],
    79	      "reason": "Matrix requires terminal \"smart\" but contract uses pos terminals"
    80	    },
    81	    {
    82	      "matrix_id": "2.6.2.1",
    83	      "closure": "linked",
    84	      "link_indices": [],
    85	      "reason": ""
    86	    },
    87	    {
    88	      "matrix_id": "2.6.2.2",
    89	      "closure": "linked",
    90	      "link_indices": [],
    91	      "reason": ""
    92	    },
    93	    {
    94	      "matrix_id": "2.6.3.1",
    95	      "closure": "linked",
    96	      "link_indices": [],
    97	      "reason": ""
    98	    },
    99	    {
   100	      "matrix_id": "2.6.3.2",
   101	      "closure": "linked",
   102	      "link_indices": [],
   103	      "reason": ""
   104	    },
   105	    {
   106	      "matrix_id": "2.7",
   107	      "closure": "linked",
   108	      "link_indices": [],
   109	      "reason": ""
   110	    },
   111	    {
   112	      "matrix_id": "3.1",
   113	      "closure": "linked",
   114	      "link_indices": [],
   115	      "reason": ""
   116	    },
   117	    {
   118	      "matrix_id": "3.2",
   119	      "closure": "linked",
   120	      "link_indices": [],
   121	      "reason": ""
   122	    },
   123	    {
   124	      "matrix_id": "3.3",
   125	      "closure": "linked",
   126	      "link_indices": [],
   127	      "reason": ""
   128	    },
   129	    {
   130	      "matrix_id": "4.1.1",
   131	      "closure": "linked",
   132	      "link_indices": [],
   133	      "reason": ""
   134	    },
   135	    {
   136	      "matrix_id": "4.1.2",
   137	      "closure": "linked",
   138	      "link_indices": [],
   139	      "reason": ""
   140	    },
   141	    {
   142	      "matrix_id": "4.1.3",
   143	      "closure": "out_of_scope",
   144	      "link_indices": [],
   145	      "reason": "Matrix requires payment method \"qr_sber_pay\" but contract uses cards, qr"
   146	    },
   147	    {
   148	      "matrix_id": "4.2.1",
   149	      "closure": "linked",
   150	      "link_indices": [],
   151	      "reason": ""
   152	    },
   153	    {
   154	      "matrix_id": "4.2.2",
   155	      "closure": "linked",
   156	      "link_indices": [],
   157	      "reason": ""
   158	    },
   159	    {
   160	      "matrix_id": "4.2.3",
   161	      "closure": "out_of_scope",
   162	      "link_indices": [],
   163	      "reason": "Matrix requires lot \"fz_223\" but contract is 44_fz"
   164	    },
   165	    {
   166	      "matrix_id": "4.2.4",
   167	      "closure": "linked",
   168	      "link_indices": [],
   169	      "reason": ""
   170	    },
   171	    {
   172	      "matrix_id": "4.2.5",
   173	      "closure": "linked",
   174	      "link_indices": [],
   175	      "reason": ""
   176	    },
   177	    {
   178	      "matrix_id": "4.2.6",
   179	      "closure": "linked",
   180	      "link_indices": [],
   181	      "reason": ""
   182	    },
   183	    {
   184	      "matrix_id": "4.2.7",
   185	      "closure": "linked",
   186	      "link_indices": [],
   187	      "reason": ""
   188	    },
   189	    {
   190	      "matrix_id": "4.2.8",
   191	      "closure": "linked",
   192	      "link_indices": [],
   193	      "reason": ""
   194	    },
   195	    {
   196	      "matrix_id": "4.2.9",
   197	      "closure": "linked",
   198	      "link_indices": [],
   199	      "reason": ""
   200	    },
Tool:      1	{
     2	  "product": [
     3	    "trade_acquiring"
     4	  ],
     5	  "lot": "fz_44",
     6	  "terminal": [
     7	    "pos"
     8	  ],
     9	  "payment_method": [
    10	    "cards",
    11	    "qr"
    12	  ],
    13	  "legal_regime": "fz_44",
    14	  "profile_notes": [
    15	    "Contract is a 44-FZ public procurement for acquiring services",
    16	    "Customer: ФГБУ Кавказский государственный заповедник",
    17	    "Terminals: POS-терминалы provided by Bank",
    18	    "Payment methods: cards (МИР, VISA, MasterCard), QR-код",
    19	    "No internet acquiring - trade acquiring only",
    20	    "No SberPay, no SberPayFaceScan",
    21	    "Smart terminal (Эвотор+) only in application form checkbox, not operative",
    22	    "Contract price: 1,900,000 RUB max",
    23	    "Term: 01.03.2025 - 30.11.2025",
    24	    "Commission: percentage-based per specification",
    25	    "No terminal provision fee, no subscription fee"
    26	  ]
    27	}
Tool:      1	{
     2	  "valid": true,
     3	  "errors": [],
     4	  "warnings": [
     5	    "legal_propositions_weak_evaluable_rows:222"
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
AI: Good. Now let me read the rest of the coverage ledger and the matrix to understand the batch range 4.2.22 through 7.17.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/coverage_ledger.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_TezMR7zr25sQQo4qDYlm7994', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_01_FJw23kmajtDjhIexVXZM6324', 'type': 'tool_call'}]
Tool:    201	    {
   202	      "matrix_id": "4.2.10",
   203	      "closure": "linked",
   204	      "link_indices": [],
   205	      "reason": ""
   206	    },
   207	    {
   208	      "matrix_id": "4.2.11",
   209	      "closure": "linked",
   210	      "link_indices": [],
   211	      "reason": ""
   212	    },
   213	    {
   214	      "matrix_id": "4.2.12",
   215	      "closure": "linked",
   216	      "link_indices": [],
   217	      "reason": ""
   218	    },
   219	    {
   220	      "matrix_id": "4.2.13",
   221	      "closure": "linked",
   222	      "link_indices": [],
   223	      "reason": ""
   224	    },
   225	    {
   226	      "matrix_id": "4.2.14",
   227	      "closure": "linked",
   228	      "link_indices": [],
   229	      "reason": ""
   230	    },
   231	    {
   232	      "matrix_id": "4.2.15",
   233	      "closure": "linked",
   234	      "link_indices": [],
   235	      "reason": ""
   236	    },
   237	    {
   238	      "matrix_id": "4.2.16.1",
   239	      "closure": "linked",
   240	      "link_indices": [],
   241	      "reason": ""
   242	    },
   243	    {
   244	      "matrix_id": "4.2.16.2",
   245	      "closure": "linked",
   246	      "link_indices": [],
   247	      "reason": ""
   248	    },
   249	    {
   250	      "matrix_id": "4.2.16.3",
   251	      "closure": "linked",
   252	      "link_indices": [],
   253	      "reason": ""
   254	    },
   255	    {
   256	      "matrix_id": "4.2.17",
   257	      "closure": "out_of_scope",
   258	      "link_indices": [],
   259	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   260	    },
   261	    {
   262	      "matrix_id": "4.2.18",
   263	      "closure": "linked",
   264	      "link_indices": [],
   265	      "reason": ""
   266	    },
   267	    {
   268	      "matrix_id": "4.2.19",
   269	      "closure": "linked",
   270	      "link_indices": [],
   271	      "reason": ""
   272	    },
   273	    {
   274	      "matrix_id": "4.2.20.1",
   275	      "closure": "linked",
   276	      "link_indices": [],
   277	      "reason": ""
   278	    },
   279	    {
   280	      "matrix_id": "4.2.20.2",
   281	      "closure": "linked",
   282	      "link_indices": [],
   283	      "reason": ""
   284	    },
   285	    {
   286	      "matrix_id": "4.2.20.3",
   287	      "closure": "linked",
   288	      "link_indices": [],
   289	      "reason": ""
   290	    },
   291	    {
   292	      "matrix_id": "4.2.20.4",
   293	      "closure": "linked",
   294	      "link_indices": [],
   295	      "reason": ""
   296	    },
   297	    {
   298	      "matrix_id": "4.2.20.5",
   299	      "closure": "linked",
   300	      "link_indices": [],
   301	      "reason": ""
   302	    },
   303	    {
   304	      "matrix_id": "4.2.20.6",
   305	      "closure": "linked",
   306	      "link_indices": [],
   307	      "reason": ""
   308	    },
   309	    {
   310	      "matrix_id": "4.2.20.7",
   311	      "closure": "linked",
   312	      "link_indices": [],
   313	      "reason": ""
   314	    },
   315	    {
   316	      "matrix_id": "4.2.21.1",
   317	      "closure": "out_of_scope",
   318	      "link_indices": [],
   319	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   320	    },
   321	    {
   322	      "matrix_id": "4.2.21.2",
   323	      "closure": "out_of_scope",
   324	      "link_indices": [],
   325	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   326	    },
   327	    {
   328	      "matrix_id": "4.2.21.3",
   329	      "closure": "out_of_scope",
   330	      "link_indices": [],
   331	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   332	    },
   333	    {
   334	      "matrix_id": "4.2.21.4",
   335	      "closure": "out_of_scope",
   336	      "link_indices": [],
   337	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   338	    },
   339	    {
   340	      "matrix_id": "4.2.21.5",
   341	      "closure": "out_of_scope",
   342	      "link_indices": [],
   343	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   344	    },
   345	    {
   346	      "matrix_id": "4.2.21.6",
   347	      "closure": "out_of_scope",
   348	      "link_indices": [],
   349	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   350	    },
   351	    {
   352	      "matrix_id": "4.2.21.7",
   353	      "closure": "out_of_scope",
   354	      "link_indices": [],
   355	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   356	    },
   357	    {
   358	      "matrix_id": "4.2.21.8",
   359	      "closure": "out_of_scope",
   360	      "link_indices": [],
   361	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   362	    },
   363	    {
   364	      "matrix_id": "4.2.22",
   365	      "closure": "linked",
   366	      "link_indices": [],
   367	      "reason": ""
   368	    },
   369	    {
   370	      "matrix_id": "4.2.23",
   371	      "closure": "linked",
   372	      "link_indices": [],
   373	      "reason": ""
   374	    },
   375	    {
   376	      "matrix_id": "4.2.24",
   377	      "closure": "linked",
   378	      "link_indices": [],
   379	      "reason": ""
   380	    },
   381	    {
   382	      "matrix_id": "4.2.25",
   383	      "closure": "linked",
   384	      "link_indices": [],
   385	      "reason": ""
   386	    },
   387	    {
   388	      "matrix_id": "4.2.26",
   389	      "closure": "out_of_scope",
   390	      "link_indices": [],
   391	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   392	    },
   393	    {
   394	      "matrix_id": "5.1.1.1",
   395	      "closure": "linked",
   396	      "link_indices": [],
   397	      "reason": ""
   398	    },
   399	    {
   400	      "matrix_id": "5.1.1.2",
   401	      "closure": "linked",
   402	      "link_indices": [],
   403	      "reason": ""
   404	    },
   405	    {
   406	      "matrix_id": "5.1.1.3",
   407	      "closure": "linked",
   408	      "link_indices": [],
   409	      "reason": ""
   410	    },
   411	    {
   412	      "matrix_id": "5.1.1.4",
   413	      "closure": "linked",
   414	      "link_indices": [],
   415	      "reason": ""
   416	    },
   417	    {
   418	      "matrix_id": "5.1.1.5",
   419	      "closure": "linked",
   420	      "link_indices": [],
   421	      "reason": ""
   422	    },
   423	    {
   424	      "matrix_id": "5.1.1.6",
   425	      "closure": "linked",
   426	      "link_indices": [],
   427	      "reason": ""
   428	    },
   429	    {
   430	      "matrix_id": "5.1.2",
   431	      "closure": "linked",
   432	      "link_indices": [],
   433	      "reason": ""
   434	    },
   435	    {
   436	      "matrix_id": "5.1.3",
   437	      "closure": "linked",
   438	      "link_indices": [],
   439	      "reason": ""
   440	    },
   441	    {
   442	      "matrix_id": "5.1.4",
   443	      "closure": "linked",
   444	      "link_indices": [],
   445	      "reason": ""
   446	    },
   447	    {
   448	      "matrix_id": "5.1.5",
   449	      "closure": "linked",
   450	      "link_indices": [],
   451	      "reason": ""
   452	    },
   453	    {
   454	      "matrix_id": "5.1.6",
   455	      "closure": "linked",
   456	      "link_indices": [],
   457	      "reason": ""
   458	    },
   459	    {
   460	      "matrix_id": "5.1.7",
   461	      "closure": "linked",
   462	      "link_indices": [],
   463	      "reason": ""
   464	    },
   465	    {
   466	      "matrix_id": "5.1.8.1",
   467	      "closure": "linked",
   468	      "link_indices": [],
   469	      "reason": ""
   470	    },
   471	    {
   472	      "matrix_id": "5.1.8.2",
   473	      "closure": "linked",
   474	      "link_indices": [],
   475	      "reason": ""
   476	    },
   477	    {
   478	      "matrix_id": "5.1.8.3",
   479	      "closure": "linked",
   480	      "link_indices": [],
   481	      "reason": ""
   482	    },
   483	    {
   484	      "matrix_id": "5.1.8.4",
   485	      "closure": "out_of_scope",
   486	      "link_indices": [],
   487	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   488	    },
   489	    {
   490	      "matrix_id": "5.1.8.5",
   491	      "closure": "out_of_scope",
   492	      "link_indices": [],
   493	      "reason": "Matrix requires product \"internet_acquiring\" but contract is trade_acquiring only"
   494	    },
   495	    {
   496	      "matrix_id": "5.1.8.6",
   497	      "closure": "linked",
   498	      "link_indices": [],
   499	      "reason": ""
   500	    },
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
AI: Now let me find the specific matrix items in the batch range 4.2.22 through 7.17. Let me search for these in the matrix.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\',\'r\') as f:\n    matrix = json.load(f)\n# Find items from 4.2.22 to 7.17\nbatch = [m for m in matrix if m[\'number\'] >= \'4.2.22\' and m[\'number\'] <= \'7.17\']\nfor m in batch:\n    print(m[\'number\'], \'|\', m.get(\'required_type\',\'\'), \'|\', m.get(\'only_for_product\',\'\'), \'|\', m.get(\'only_for_lot\',\'\'), \'|\', m.get(\'only_for_terminal\',\'\'), \'|\', m.get(\'payment_method\',\'\'), \'|\', m.get(\'main_idea\',\'\')[:120])\nprint(\'---\')\nprint(\'Total batch items:\', len(batch))\n"\n'}, 'id': 'call_00_gChmAs2iHPg0vlWcN3hT3299', 'type': 'tool_call'}]
Tool: 4.2.3 | optional | common | fz_223 | common | common | 
4.2.4 | optional | common | common | common | common | Р’Р°Р¶РµРЅ С„Р°РєС‚, РµСЃР»Рё Р±Р°РЅРє РїРµСЂРµРґР°РµС‚ РїРѕ РґРѕРіРѕРІРѕСЂСѓ РїСЂРµРґРїСЂРёСЏС‚РёСЋ - Р·Р°РєР°Р·С‡РёРєСѓ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, С‚Рѕ Р·Р°РєР°Р·С‡РёРє РґРѕР»Р¶РµРЅ РёС… СЂР°Р·РјРµ
4.2.5 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ, РЅРµ РїСЂРёРЅРёРјР°С‚СЊ РѕС‚ РџРѕРєСѓРїР°С‚РµР»СЏ Р±РѕР»РµРµ 2 (РґРІСѓС…) СЂР°Р·Р»РёС‡РЅС‹С… РљР°СЂС‚. РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР°
4.2.6 | mandatory | common | common | common | common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РЅРµР»СЊР·СЏ СЂР°Р·Р±РёРІР°С‚СЊ РћРїРµСЂР°С†РёСЋ РЅР° РЅРµСЃРєРѕР»СЊРєСѓ СЃСѓРјРј
4.2.7 | mandatory | common | common | common | common | 
4.2.8 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С†РµРЅР° РЅРµ Р·Р°РІРёСЃРёС‚ РѕС‚ СЃРїРѕСЃРѕР±Р° РѕРїР»Р°С‚С‹
4.2.9 | mandatory | common | common | common | common | Р—Р°РєР°Р·С‡РёРє РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РёРЅС„РѕСЂРјР°С†РёСЋ РєРѕС‚РѕСЂСѓСЋ РѕРЅ СѓРєР°Р·С‹РІР°РµС‚ РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїСЂРё РїСЂРѕРІРµРґРµРЅРёРё РїР»Р°С‚РµР¶РµР№
4.2.22 | optional | trade_acquiring | common | common | qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
4.2.23 | optional | trade_acquiring | common | common | qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
4.2.24 | optional | common | common | common | qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
4.2.25 | optional | common | common | common | qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
4.2.26 | mandatory | internet_acquiring | common | common | common | 
5.1.1.1 | mandatory | common | common | common | common | 
5.1.1.2 | mandatory | common | common | common | common | 
5.1.1.3 | mandatory | common | common | common | common | 
5.1.1.4 | mandatory | common | common | common | common | 
5.1.1.5 | mandatory | common | common | common | common | 
5.1.1.6 | mandatory | trade_acquiring | common | common | common | Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. 
5.1.2 | mandatory | common | common | common | common | 
5.1.3 | mandatory | common | common | common | common | 
5.1.4 | mandatory | common | common | common | common | 
5.1.5 | mandatory | common | common | common | common | 
5.1.6 | mandatory | common | common | common | common | 
5.1.7 | mandatory | common | common | common | common | 
5.1.8.1 | optional | common | common | common | common | 
5.1.8.2 | optional | common | common | common | common | 
5.1.8.3 | optional | common | common | common | common | 
5.1.8.4 | optional | internet_acquiring | common | common | common | 
5.1.8.5 | optional | internet_acquiring | common | common | common | 
5.1.8.6 | optional | common | common | common | common | 
5.1.8.7 | optional | common | common | common | common | 
5.1.8.8 | optional | trade_acquiring | common | common | common | 
5.1.8.9 | optional | common | common | common | common | 
5.1.8.10 | optional | common | common | common | common | 
5.1.8.11 | optional | common | common | common | common | 
5.1.8.12 | optional | common | common | common | common | 
5.1.8.13 | optional | common | common | common | common | 
5.1.9 | mandatory | common | common | common | common | 
5.1.10 | mandatory | common | common | common | common | 
5.1.11 | mandatory | common | common | common | common | 
5.1.12 | optional | common | common | common | common | 
5.1.13 | optional | common | common | common | common | Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµРґРѕРјР»РµРЅРёСЏ, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
5.1.14 | mandatory | common | common | common | common | 
5.1.15 | optional | common | common | common | common | 
5.1.16 | mandatory | common | common | common | common | 
5.1.17.1 | optional | trade_acquiring | common | pos | common | 
5.1.17.2 | optional | trade_acquiring | common | smart | common | 
5.2.1 | mandatory | internet_acquiring | common | common | common | 
5.2.2 | mandatory | internet_acquiring | common | common | common | 
5.2.3 | mandatory | trade_acquiring | common | common | common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»Рє
5.2.4 | optional | common | common | common | common | 
5.2.5 | optional | common | common | common | common | РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
5.2.6 | optional | trade_acquiring | common | common | common | 
5.2.7 | optional | common | common | common | common | 
5.2.8 | mandatory | common | common | common | common | Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
5.2.9 | optional | trade_acquiring | common | common | qr | 
5.2.10 | mandatory | common | common | common | common | 
5.2.12 | optional | internet_acquiring | common | common | qr | 
6.1 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ
6.2 | mandatory | common | common | common | common | РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµ
6.3 | mandatory | common | fz_223 | common | common | 
6.4 | mandatory | common | common | common | common | 
6.5 | mandatory | common | common | common | common | 
6.6 | mandatory | common | fz_223 | common | common | 
6.7 | mandatory | trade_acquiring | common | smart | common | 
6.8 | mandatory | trade_acquiring | common | smart | common | 
6.9 | mandatory | trade_acquiring | fz_223 | smart | common | 
6.10 | mandatory | trade_acquiring | common | smart | common | 
6.11 | mandatory | trade_acquiring | common | smart | common | 
6.12 | mandatory | trade_acquiring | fz_223 | smart | common | 
6.13 | mandatory | trade_acquiring | common | smart | common | 
6.14 | mandatory | trade_acquiring | common | smart | common | 
6.15 | mandatory | trade_acquiring | fz_223 | smart | common | 
6.16 | mandatory | trade_acquiring | common | smart | common | 
6.17 | mandatory | trade_acquiring | common | smart | common | 
6.18 | mandatory | trade_acquiring | fz_223 | smart | common | 
6.20 | mandatory | common | common | common | common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
6.21 | mandatory | common | common | common | common | РћС‚СЃСѓС‚СЃС‚РІРёРµ РєРѕРЅРєСЂРµС‚РЅРѕР№ С†РµРЅРЅС‹ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёРµРј
7.1 | mandatory | common | common | common | common | 
7.10 | optional | common | common | common | common | 
7.11 | optional | common | common | common | common | 
7.12 | optional | common | common | common | common | 
7.13 | mandatory | internet_acquiring | common | common | common | 
7.14 | mandatory | common | common | common | common | 
7.15 | mandatory | common | common | common | common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅРµСЃРµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ РіРѕРІРѕСЂРёС‚СЃСЏ РїСЂРѕ РЅРµСЃРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РґРµР№СЃС‚РІРёСЏ РїРµСЂСЃРѕРЅР°Р»Р°, 
7.16 | mandatory | common | common | common | common | 
7.17 | mandatory | common | common | common | common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹  РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ Р±С‹Р»Рѕ СЃСѓР¶РµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё.
---
Total batch items: 87

[Command succeeded with exit code 0]
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix entries for batch 4.2.22 through 7.17', 'status': 'in_progress'}, {'content': 'Read contract text for relevant clauses', 'status': 'pending'}, {'content': 'Read existing legal_propositions.json for batch items', 'status': 'pending'}, {'content': 'Apply product profile filters to determine applicability', 'status': 'pending'}, {'content': 'Perform matrix-to-contract matching for each applicable item', 'status': 'pending'}, {'content': 'Perform contract-to-matrix matching for material contract clauses', 'status': 'pending'}, {'content': 'Assign group-level status (aligned/deviation/missing_in_contract/extra_in_contract)', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, and coverage_ledger rows for batch', 'status': 'pending'}, {'content': 'Write batch output to /outputs/working/batch_2_output.json', 'status': 'pending'}]}, 'id': 'call_00_pNwIzkg03LwhIeg92lm76170', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix entries for batch 4.2.22 through 7.17', 'status': 'in_progress'}, {'content': 'Read contract text for relevant clauses', 'status': 'pending'}, {'content': 'Read existing legal_propositions.json for batch items', 'status': 'pending'}, {'content': 'Apply product profile filters to determine applicability', 'status': 'pending'}, {'content': 'Perform matrix-to-contract matching for each applicable item', 'status': 'pending'}, {'content': 'Perform contract-to-matrix matching for material contract clauses', 'status': 'pending'}, {'content': 'Assign group-level status (aligned/deviation/missing_in_contract/extra_in_contract)', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, and coverage_ledger rows for batch', 'status': 'pending'}, {'content': 'Write batch output to /outputs/working/batch_2_output.json', 'status': 'pending'}]
AI: Let me now read the full matrix entries for the batch and the contract text.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\',\'r\') as f:\n    matrix = json.load(f)\nbatch = [m for m in matrix if m[\'number\'] >= \'4.2.22\' and m[\'number\'] <= \'7.17\']\nfor m in batch:\n    print(\'===\', m[\'number\'], \'===\')\n    print(\'required_type:\', m.get(\'required_type\'))\n    print(\'only_for_product:\', m.get(\'only_for_product\'))\n    print(\'only_for_lot:\', m.get(\'only_for_lot\'))\n    print(\'only_for_terminal:\', m.get(\'only_for_terminal\'))\n    print(\'payment_method:\', m.get(\'payment_method\'))\n    print(\'main_idea:\', m.get(\'main_idea\',\'\'))\n    print(\'enriched_text:\', m.get(\'enriched_text\',\'\')[:300])\n    print(\'topics:\', m.get(\'topics\',[]))\n    print()\n" 2>&1 | head -3000\n'}, 'id': 'call_00_FMTozfP5HtXkzeCLdq9Z8902', 'type': 'tool_call'}]
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
[stderr] python -c "
[stderr] import json
[stderr] with open('inputs/matrix.json','r') as f:
[stderr]     matrix = json.load(f)
[stderr] batch = [m for m in matrix if m['number'] >= '4.2.22' and m['number'] <= '7.17']
[stderr] for m in batch:
[stderr]     print('===', m['number'], '===')
[stderr]     print('required_type:', m.get('required_type'))
[stderr]     print('only_for_product:', m.get('only_for_product'))
[stderr]     print('only_for_lot:', m.get('only_for_lot'))
[stderr]     print('only_for_terminal:', m.get('only_for_terminal'))
[stderr]     print('payment_method:', m.get('payment_method'))
[stderr]     print('main_idea:', m.get('main_idea',''))
[stderr]     print('enriched_text:', m.get('enriched_text','')[:300])
[stderr]     print('topics:', m.get('topics',[]))
[stderr]     print()
[stderr] " 2>&1 | head -3000
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : The term 'head' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
[stderr] lling of the name, or if a path was included, verify that the path is correct and try again.
[stderr] At line:53 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'inputs/matrix.json\',\'r\') as f:\n    matrix = json.load(f)\nbatch = [m for m in matrix if m[\'number\'] >= \'4.2.22\' and m[\'number\'] <= \'7.17\']\nfor m in batch:\n    print(\'===\', m[\'number\'], \'===\')\n    print(\'required_type:\', m.get(\'required_type\'))\n    print(\'only_for_product:\', m.get(\'only_for_product\'))\n    print(\'only_for_lot:\', m.get(\'only_for_lot\'))\n    print(\'only_for_terminal:\', m.get(\'only_for_terminal\'))\n    print(\'payment_method:\', m.get(\'payment_method\'))\n    print(\'main_idea:\', m.get(\'main_idea\',\'\'))\n    print(\'enriched_text:\', m.get(\'enriched_text\',\'\')[:300])\n    print(\'topics:\', m.get(\'topics\',[]))\n    print()\n" 2>&1\n'}, 'id': 'call_00_BCRggVyaRNuuvnDemcN92385', 'type': 'tool_call'}]
Tool: Tool result too large, the result of this tool call call_00_BCRggVyaRNuuvnDemcN92385 was saved in the filesystem at this path: /large_tool_results/call_00_BCRggVyaRNuuvnDemcN92385

You can read the result from the filesystem by using the read_file tool, but make sure to only read part of the result at a time.

You can do this by specifying an offset and limit in the read_file tool call. For example, to read the first 100 lines, you can use the read_file tool with offset=0 and limit=100.

Here is a preview showing the head and tail of the result (lines of the form `... [N lines truncated] ...` indicate omitted lines in the middle of the content):

     1	=== 4.2.3 ===
     2	required_type: optional
     3	only_for_product: common
     4	only_for_lot: fz_223
     5	only_for_terminal: common
... [868 lines truncated] ...
   874	enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РїСЂРѕРІРµРґРµРЅРЅС‹С… РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ С‚СЂРµР±РѕРІР°РЅРёСЏРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё, РІ С‚РѕРј С‡РёСЃР»Рµ РЅРѕСЂРјР°С‚РёРІРЅС‹С… Р°РєС‚РѕРІ Р‘Р°РЅРєР° Р РѕСЃСЃРёРё, РїСЂР°РІРёР» РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё (РёР»Рё) Р”РѕРіРѕРІРѕСЂР°
   875	topics: ['РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ Р Р¤', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕС‚РІРµС‡Р°РµС‚ Р·Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РЅРѕСЂРјР°С‚РёРІРЅС‹Рј Р°РєС‚Р°Рј Р‘Р°РЅРєР° Р РѕСЃСЃРёРё', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕР±Р»СЋРґР°С‚СЊ РїСЂР°РІРёР»Р° РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РІ С‡Р°СЃС‚Рё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РѕС‚РЅРѕСЃРёС‚РµР»СЊРЅРѕ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№']
   876	
   877	
   878	[Command succeeded with exit code 0]

AI: [{'name': 'read_file', 'args': {'file_path': '/large_tool_results/call_00_BCRggVyaRNuuvnDemcN92385', 'offset': 0, 'limit': 200}, 'id': 'call_00_h36ulaTcyDFOyiOuNcRW8807', 'type': 'tool_call'}]
Tool:      1	=== 4.2.3 ===
     2	required_type: optional
     3	only_for_product: common
     4	only_for_lot: fz_223
     5	only_for_terminal: common
     6	payment_method: common
     7	main_idea: 
     8	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё, РІРЅРµСЃРµРЅРЅС‹РјРё РІ РґРѕРєСѓРјРµРЅС‚С‹, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ РЅР°СЃС‚РѕСЏС‰РµРј Р”РѕРіРѕРІРѕСЂРµ, СЂР°Р·РјРµС‰РµРЅРЅС‹РјРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°. РќРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР·РЅР°РєРѕРјР»РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё, РІРЅРµСЃРµРЅРЅС‹РјРё РІ РІ
     9	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕ Р·РЅР°РєРѕРјРёС‚СЊСЃСЏ СЃ РёР·РјРµРЅРµРЅРёСЏРјРё РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РќРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР·РЅР°РєРѕРјР»РµРЅРёРµ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РЅРµРїСЂРёРјРµРЅРµРЅРёСЏ РёР·РјРµРЅРµРЅРёР№']
    10	
    11	=== 4.2.4 ===
    12	required_type: optional
    13	only_for_product: common
    14	only_for_lot: common
    15	only_for_terminal: common
    16	payment_method: common
    17	main_idea: Р’Р°Р¶РµРЅ С„Р°РєС‚, РµСЃР»Рё Р±Р°РЅРє РїРµСЂРµРґР°РµС‚ РїРѕ РґРѕРіРѕРІРѕСЂСѓ РїСЂРµРґРїСЂРёСЏС‚РёСЋ - Р·Р°РєР°Р·С‡РёРєСѓ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, С‚Рѕ Р·Р°РєР°Р·С‡РёРє РґРѕР»Р¶РµРЅ РёС… СЂР°Р·РјРµСЃС‚РёС‚СЊ РЅР° РІРёРґРЅРѕРј РјРµСЃС‚Рµ, РµСЃР»Рё РёРЅС‚РµСЂРЅРµС‚- СЌРєРІР°Р№СЂРёРЅРі С‚Рѕ РІ РґРѕСЃС‚СѓРїРЅРѕРј РґР»СЏ РїРѕСЃРµС‚РёС‚РµР»СЏ СЃР°Р№С‚Р° РјРµСЃС‚Рµ
    18	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: Р Р°Р·РјРµС‰Р°С‚СЊ РЅР° РІРёРґРЅС‹С… РјРµСЃС‚Р°С… РўРЎРў[1]/РѕР±С‰РµРґРѕСЃС‚СѓРїРЅС‹С… РјРµСЃС‚Р°С… Р РµСЃСѓСЂСЃР°[2], РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµРјС‹Рµ Р‘Р°РЅРєРѕРј РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, РёР·РІРµС‰Р°СЋС‰РёРµ РџРѕРєСѓРїР°С‚РµР»РµР№ Рѕ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕРїР»Р°С‚С‹ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚/NFC-РєР°СЂС‚/SberPay/РџР»Р°С‚Рё QR, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё СЌС‚Рѕ 
    19	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЂР°Р·РјРµС‰Р°С‚СЊ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ Р‘Р°РЅРєР° Рѕ СЃРїРѕСЃРѕР±Р°С… РѕРїР»Р°С‚С‹', 'Р Р°Р·РјРµС‰РµРЅРёРµ РјР°С‚РµСЂРёР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ СЃР»СѓС‡Р°Рµ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёР№ СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']
    20	
    21	=== 4.2.5 ===
    22	required_type: mandatory
    23	only_for_product: common
    24	only_for_lot: common
    25	only_for_terminal: common
    26	payment_method: common
    27	main_idea: Р’Р°Р¶РЅРѕ, РЅРµ РїСЂРёРЅРёРјР°С‚СЊ РѕС‚ РџРѕРєСѓРїР°С‚РµР»СЏ Р±РѕР»РµРµ 2 (РґРІСѓС…) СЂР°Р·Р»РёС‡РЅС‹С… РљР°СЂС‚. РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР°
    28	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРёРЅРёРјР°С‚СЊ РІ РѕРїР»Р°С‚Сѓ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РІСЃРµ РљР°СЂС‚С‹, РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ РІ РџРѕСЂСЏРґРєРµ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅС‹С… С‚РѕС‡РєР°С…/РЅР° Р РµСЃСѓСЂСЃРµ, РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РІСЂРµРјРµРЅРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ. РќРµ РІС‹РґР°РІР°С‚СЊ РїРѕ РљР°СЂС‚Р°Рј РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР°[3]. РќРµ РїСЂРёРЅРёРјР°С‚СЊ 
    29	topics: ['РџСЂРёРЅРёРјР°С‚СЊ Рє РѕРїР»Р°С‚Рµ РІСЃРµ РєР°СЂС‚С‹ РёР· СЃРїРёСЃРєР° РІ С‚РµС‡РµРЅРёРµ РІСЃРµРіРѕ СЂР°Р±РѕС‡РµРіРѕ РІСЂРµРјРµРЅРё', 'РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅСЊРіРё РїРѕ РєР°СЂС‚Р°Рј', 'РќРµ РїСЂРёРЅРёРјР°С‚СЊ Р±РѕР»РµРµ РґРІСѓС… СЂР°Р·РЅС‹С… РєР°СЂС‚ РѕС‚ РѕРґРЅРѕРіРѕ РїРѕРєСѓРїР°С‚РµР»СЏ']
    30	
    31	=== 4.2.6 ===
    32	required_type: mandatory
    33	only_for_product: common
    34	only_for_lot: common
    35	only_for_terminal: common
    36	payment_method: common
    37	main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РЅРµР»СЊР·СЏ СЂР°Р·Р±РёРІР°С‚СЊ РћРїРµСЂР°С†РёСЋ РЅР° РЅРµСЃРєРѕР»СЊРєСѓ СЃСѓРјРј
    38	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќРµ СЂР°Р·Р±РёРІР°С‚СЊ СЃСѓРјРјСѓ РѕРґРЅРѕР№ РћРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹ РЅР° РЅРµСЃРєРѕР»СЊРєРѕ СЃСѓРјРј Рё РЅРµ РїСЂРѕРІРѕРґРёС‚СЊ РѕС‚РґРµР»СЊРЅС‹Рµ РћРїРµСЂР°С†РёРё РЅР° РєР°Р¶РґСѓСЋ РёР· СЌС‚РёС… СЃСѓРјРј.
    39	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РћРїРµСЂР°С†РёСЋ РѕРїР»Р°С‚С‹ РµРґРёРЅРѕР№ СЃСѓРјРјРѕР№ Р±РµР· СЂР°Р·РґРµР»РµРЅРёСЏ РЅР° С‡Р°СЃС‚Рё']
    40	
    41	=== 4.2.7 ===
    42	required_type: mandatory
    43	only_for_product: common
    44	only_for_lot: common
    45	only_for_terminal: common
    46	payment_method: common
    47	main_idea: 
    48	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹/РџР»Р°С‚РµР¶РЅРѕРіРѕ СЃС‡РµС‚Р°, РєРѕС‚РѕСЂС‹Рµ СЃС‚Р°Р»Рё РґРѕСЃС‚СѓРїРЅС‹ РџСЂРµРґРїСЂРёСЏС‚РёСЋ/РўРЎРў, РґР»СЏ РёРЅС‹С… С†РµР»РµР№, РєСЂРѕРјРµ РєР°Рє РїСЂРѕРІРµРґРµРЅРёРµ РћРїРµСЂР°С†РёР№ РІ РїСЂРёСЃСѓС‚СЃС‚РІРёРё РёР»Рё РїРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЋ РџРѕРєСѓРїР°С‚РµР»СЏ.
    49	topics: ['РќРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ Р±РµР· РїСЂРёСЃСѓС‚СЃС‚РІРёСЏ РёР»Рё СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏ', 'Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ СЂРµРєРІРёР·РёС‚С‹ РљР°СЂС‚С‹ С‚РѕР»СЊРєРѕ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№']
    50	
    51	=== 4.2.8 ===
    52	required_type: mandatory
    53	only_for_product: common
    54	only_for_lot: common
    55	only_for_terminal: common
    56	payment_method: common
    57	main_idea: Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С†РµРЅР° РЅРµ Р·Р°РІРёСЃРёС‚ РѕС‚ СЃРїРѕСЃРѕР±Р° РѕРїР»Р°С‚С‹
    58	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РџРѕРєСѓРїР°С‚РµР»СЏРј РїРѕР»РЅС‹Р№ РЅР°Р±РѕСЂ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РїРѕ С†РµРЅР°Рј, РЅРµ РїСЂРµРІС‹С€Р°СЋС‰РёРј С†РµРЅС‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРё СЂР°СЃС‡РµС‚Р°С… Р·Р° РЅР°Р»РёС‡РЅС‹Рµ РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР°.
    59	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РїРѕР»РЅС‹Р№ РЅР°Р±РѕСЂ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РїРѕРєСѓРїР°С‚РµР»СЏРј', 'С†РµРЅС‹ РґР»СЏ СЂР°СЃС‡РµС‚РѕРІ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј Р±Р°РЅРєРѕРІСЃРєРѕР№ РєР°СЂС‚С‹ РЅРµ РїСЂРµРІС‹С€Р°СЋС‚ С†РµРЅС‹ Р·Р° РЅР°Р»РёС‡РЅС‹Р№ СЂР°СЃС‡РµС‚']
    60	
    61	=== 4.2.9 ===
    62	required_type: mandatory
    63	only_for_product: common
    64	only_for_lot: common
    65	only_for_terminal: common
    66	payment_method: common
    67	main_idea: Р—Р°РєР°Р·С‡РёРє РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РёРЅС„РѕСЂРјР°С†РёСЋ РєРѕС‚РѕСЂСѓСЋ РѕРЅ СѓРєР°Р·С‹РІР°РµС‚ РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїСЂРё РїСЂРѕРІРµРґРµРЅРёРё РїР»Р°С‚РµР¶РµР№
    68	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРѕРІРѕРґРёС‚СЊ РћРїРµСЂР°С†РёРё Рё РѕС„РѕСЂРјР»СЏС‚СЊ Р”РѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅС‹С… С‚РѕС‡РєР°С…/РЅР° Р РµСЃСѓСЂСЃРµ Рє Р”РѕРіРѕРІРѕСЂСѓ Рё РЅРµСЃС‚Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РїСЂР°РІРёР»СЊРЅРѕСЃС‚СЊ СѓРєР°Р·Р°РЅРЅРѕР№ РІ РґРѕРєСѓРјРµРЅС‚Р°С… РёРЅС„РѕСЂРјР°С†РёРё.
    69	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРѕРІРѕРґРёС‚СЊ РѕРїРµСЂР°С†РёРё РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РѕС„РѕСЂРјР»СЏС‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РџРѕСЂСЏРґРєРѕРј РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РёРЅС„РѕСЂРјР°С†РёРё РІ РґРѕРєСѓРјРµРЅС‚Р°С… РїРѕ РѕРїРµСЂР°С†РёСЏРј']
    70	
    71	=== 4.2.22 ===
    72	required_type: optional
    73	only_for_product: trade_acquiring
    74	only_for_lot: common
    75	only_for_terminal: common
    76	payment_method: qr
    77	main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
    78	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџРѕРєСѓРїР°С‚РµР»СЋ РґР»СЏ СЃС‡РёС‚С‹РІР°РЅРёСЏ QR-РєРѕРґ СЃ С†РµР»СЊСЋ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РѕРїР»Р°С‚С‹ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј SberPayQR/РџР»Р°С‚Рё QR
    79	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ QR-РєРѕРґ РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ SberPayQR/РџР»Р°С‚Рё QR (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)']
    80	
    81	=== 4.2.23 ===
    82	required_type: optional
    83	only_for_product: trade_acquiring
    84	only_for_lot: common
    85	only_for_terminal: common
    86	payment_method: qr
    87	main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
    88	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.
    89	topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РЅРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)']
    90	
    91	=== 4.2.24 ===
    92	required_type: optional
    93	only_for_product: common
    94	only_for_lot: common
    95	only_for_terminal: common
    96	payment_method: qr
    97	main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
    98	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ API Рё СЃРІРµРґРµРЅРёСЏ, РїРµСЂРµРґР°РІР°РµРјС‹Рµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј QR-API, РІ РіСЂР°РЅРёС†Р°С… РїСЂР°РІ Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ С‚Р°РєРѕРіРѕ API Рё РµРіРѕ РѕРїРёСЃР°РЅРёСЏ, РёР·Р»РѕР¶РµРЅРЅРѕРіРѕ РІ РџРѕСЂСЏРґРєРµ, СѓСЃР»РѕРІРёСЏС… Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё QR-API, СЂР°Р·РјРµС‰РµРЅРЅРѕРј РЅР° РћС„РёС†РёР°Р»СЊ
    99	topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API РІ СЂР°РјРєР°С… С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'СЃРѕР±Р»СЋРґРµРЅРёРµ РїРѕСЂСЏРґРєР° РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'СѓС‡РµС‚ СѓСЃР»РѕРІРёР№ Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїСЂРё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРё QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)']
   100	
   101	=== 4.2.25 ===
   102	required_type: optional
   103	only_for_product: common
   104	only_for_lot: common
   105	only_for_terminal: common
   106	payment_method: qr
   107	main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
   108	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РІС‹СЏРІР»РµРЅРёРё С„Р°РєС‚РѕРІ РёР»Рё РїСЂРёР·РЅР°РєРѕРІ РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ РѕСЂРіР°РЅРёР·Р°С†РёРё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РЅРµРјРµРґР»РµРЅРЅРѕ РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API Рё РѕРїРѕРІРµСЃС‚РёС‚СЊ РѕР± СЌС‚РѕРј Р‘Р°РЅРє Р»СЋР±
   109	topics: ['РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API - РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API РѕРїРѕРІРµСЃС‚РёС‚СЊ Р‘Р°РЅРєР° (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)']
   110	
   111	=== 4.2.26 ===
   112	required_type: mandatory
   113	only_for_product: internet_acquiring
   114	only_for_lot: common
   115	only_for_terminal: common
   116	payment_method: common
   117	main_idea: 
   118	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р’ РґРѕРїРѕР»РЅРµРЅРёРµ Рє СЃРѕР±Р»СЋРґРµРЅРёСЋ С‚СЂРµР±РѕРІР°РЅРёР№, СѓРєР°Р·Р°РЅРЅС‹С… РІ РЈСЃР»РѕРІРёСЏС…, РІ С‚РѕРј С‡РёСЃР»Рµ РїСЂРёР»РѕР¶РµРЅРёСЏС… Рє РЈСЃР»РѕРІРёСЏРј, РІ С†РµР»СЏС… РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ:
   119	вЂў СЂР°Р·РјРµС‰Р°С‚СЊ РЅР° Р РµСЃСѓСЂСЃРµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРѕРµ СЃРѕРіР»Р°С€РµРЅРёРµ/РѕС„РµСЂС‚Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СЃРѕРґРµСЂР¶
   120	topics: []
   121	
   122	=== 5.1.1.1 ===
   123	required_type: mandatory
   124	only_for_product: common
   125	only_for_lot: common
   126	only_for_terminal: common
   127	payment_method: common
   128	main_idea: 
   129	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№, СЏРІР»СЏСЋС‰РёС…СЃСЏ РЅРµРґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё, РІ СЃР»РµРґСѓСЋС‰РёС… СЃР»СѓС‡Р°СЏС…:
   130	1) РћРїРµСЂР°С†РёСЏ СЃРѕРІРµСЂС€РµРЅР° СЃ РЅР°СЂСѓС€РµРЅРёРµРј Р”РѕРіРѕРІРѕСЂР°, С‚СЂРµР±РѕРІР°РЅРёР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р Р¤ Рё/РёР»Рё РїСЂР°РІРёР» РџР»Р°С‚РµР¶
   131	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, СЏРІР»СЏСЋС‰РёРµСЃСЏ РЅРµРґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё']
   132	
   133	=== 5.1.1.2 ===
   134	required_type: mandatory
   135	only_for_product: common
   136	only_for_lot: common
   137	only_for_terminal: common
   138	payment_method: common
   139	main_idea: 
   140	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹, РѕС€РёР±РѕС‡РЅРѕ РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ.
   141	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ РѕС€РёР±РѕС‡РЅРѕ РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ СЃСѓРјРјС‹ СЃ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
   142	
   143	=== 5.1.1.3 ===
   144	required_type: mandatory
   145	only_for_product: common
   146	only_for_lot: common
   147	only_for_terminal: common
   148	payment_method: common
   149	main_idea: 
   150	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚Р° РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рµ С‚СЂР°РЅР·Р°РєС†РёРё.
   151	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°, РІРѕР·РІСЂР°С‚Р° РїР»Р°С‚РµР¶Р°, СЂРµРІРµСЂСЃРёРІРЅС‹Рµ С‚СЂР°РЅР·Р°РєС†РёРё. Р’Р°Р¶РЅРѕ РЅРµ СЂР°СЃСЃРјР°С‚СЂРёРІР°С‚СЊ РїСѓРЅРєС‚С‹ РІ РєРѕС‚РѕСЂС‹С… РЅРµ СѓРєР°Р·Р°РЅР° С…РѕС‚СЏ Р±С‹ РѕРґРЅР° РёР· СЌС‚РёС… СЃСѓРјРј']
   152	
   153	=== 5.1.1.4 ===
   154	required_type: mandatory
   155	only_for_product: common
   156	only_for_lot: common
   157	only_for_terminal: common
   158	payment_method: common
   159	main_idea: 
   160	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РєРѕС‚РѕСЂС‹Рµ Р±С‹Р»Рё РѕСЃРїРѕСЂРµРЅС‹ Рё/РёР»Рё СЃРїРёСЃР°РЅС‹ СЃРѕ СЃС‡РµС‚Р° Р‘Р°РЅРєР° Р‘Р°РЅРєРѕРј вЂ“ СЌРјРёС‚РµРЅС‚РѕРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РїРѕ РћРїРµСЂР°С†РёСЏРј, РїСЂРѕРІРµРґРµРЅРЅС‹Рј РІ РўРЎРў
   161	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕСЃРїРѕСЂРµРЅРЅС‹С… РѕРїРµСЂР°С†РёР№ РёР»Рё СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡С‘С‚Р° РёСЃРїРѕР»СЊРЅРёС‚РµР»СЏ Р±Р°РЅРєРѕРј-СЌРјРёС‚РµРЅС‚РѕРј', 'Р‘Р°РЅРє СѓРґРµСЂР¶РёРІР°РµС‚ СЃСѓРјРјС‹ РѕСЃРїРѕСЂРµРЅРЅС‹С… РѕРїРµСЂР°С†РёР№ РІ СЃР»СѓС‡Р°Рµ СЂРµР°Р»РёР·Р°С†РёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РџСЂРµРґРїСЂРёСЏС‚РёРµРј РєР°Рє Р°РіРµРЅС‚РѕРј']
   162	
   163	=== 5.1.1.5 ===
   164	required_type: mandatory
   165	only_for_product: common
   166	only_for_lot: common
   167	only_for_terminal: common
   168	payment_method: common
   169	main_idea: 
   170	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Рё РёРЅС‹С… СѓР±С‹С‚РєРѕРІ, РІРѕР·РЅРёРєС€РёС… Сѓ Р‘Р°РЅРєР° РІ СЂРµР·СѓР»СЊС‚Р°С‚Рµ РїСЂРёРјРµРЅРµРЅРёСЏ Рє РЅРµРјСѓ С€С‚СЂР°С„РЅС‹С… СЃР°РЅРєС†РёР№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, Р° С‚Р°РєР¶Рµ РїСЂРёРІР»РµС‡РµРЅРёСЏ 
   171	topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ СѓРґРµСЂР¶РёРІР°С‚СЊ С€С‚СЂР°С„С‹ РёР· СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІРѕР·РЅРёРєС€РёРµ Сѓ Р‘Р°РЅРєР° РІ СЃРІСЏР·Рё РЅРµРґРѕР±СЂРѕСЃРѕРІРµСЃС‚РЅС‹Рј РёСЃРїРѕР»РЅРµРЅРёРµРј Р—Р°РєР°Р·С‡РёРєР° РєРѕРЅС‚СЂР°РєС‚Р°', 'Р‘Р°РЅРє РІРїСЂР°РІРµ СѓРґРµСЂР¶РёРІР°С‚СЊ СѓР±С‹С‚РєРё РёР· СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІРѕР·РЅРёРєС€РёРµ РІ СЃРІСЏР·Рё СЃ РїСЂРёРІР»РµС‡РµРЅРёРµРј Р‘Р°РЅРєР° Рє РіСЂР°Р¶РґР°РЅСЃРєРѕР№ РёР»Рё Р°РґРјРёРЅРёСЃС‚СЂР°С‚РёРІРЅРѕР№ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РёР·-Р·Р° РЅРµРґРѕР±СЂРѕСЃРѕРІРµСЃС‚РЅРѕРіРѕ РёСЃРїРѕР»РЅРµРЅРёРµРј Р—Р°РєР°Р·С‡РёРєР° РєРѕРЅС‚СЂР°РєС‚Р°']
   172	
   173	=== 5.1.1.6 ===
   174	required_type: mandatory
   175	only_for_product: trade_acquiring
   176	only_for_lot: common
   177	only_for_terminal: common
   178	payment_method: common
   179	main_idea: Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. 
   180	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ С€С‚СЂР°С„РѕРІ РІ СЃР»СѓС‡Р°Рµ РЅРµРІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї. 4.2.20.7 Р”РѕРіРѕРІРѕСЂР°.
   181	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ']
   182	
   183	=== 5.1.2 ===
   184	required_type: mandatory
   185	only_for_product: common
   186	only_for_lot: common
   187	only_for_terminal: common
   188	payment_method: common
   189	main_idea: 
   190	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РІРѕР·РЅРёРєРЅРѕРІРµРЅРёСЏ Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґРѕ РјРѕРјРµРЅС‚Р° РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё.
   191	topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРёРѕСЃС‚Р°РЅР°РІР»РёРІР°С‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅР°Р»РёС‡РёРё Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РџСЂРёРѕСЃС‚Р°РЅРѕРІРєР° РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РґРѕ РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёРµРј']
   192	
   193	=== 5.1.3 ===
   194	required_type: mandatory
   195	only_for_product: common
   196	only_for_lot: common
   197	only_for_terminal: common
   198	payment_method: common
   199	main_idea: 
   200	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРё РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СѓРґРµСЂР¶Р°С‚СЊ СЃСѓРјРјС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї. 5.1.1 Р”РѕРіРѕРІРѕСЂР°, РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРѕСЃР»РµРґСѓСЋС‰РµРјСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, СЃРїРёСЃС‹РІР°С‚СЊ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ (РЅР° СѓСЃР»РѕРІРёСЏС… Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р°, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅРѕРіРѕ Р‘Р°РЅРєСѓ РџСЂРµРґРїСЂРёСЏС‚Рё
AI: This is a large batch. Let me continue reading the rest of the matrix items and then read the contract text. Let me use a more efficient approach - I'll read the legal propositions and contract text directly.[{'name': 'read_file', 'args': {'file_path': '/large_tool_results/call_00_BCRggVyaRNuuvnDemcN92385', 'offset': 200, 'limit': 300}, 'id': 'call_00_9QuD5Xr4wRucQfFpJHX52560', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_rHzkfNKGqY1dHaVIO2H36978', 'type': 'tool_call'}]
Tool:    201	topics: ['СЃРїРёСЃР°РЅРёРµ СЃСЂРµРґСЃС‚РІ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ', 'СѓСЃР»РѕРІРёРµ Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р°', 'РѕСЃРЅРѕРІР°РЅРёРµ - Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ Рѕ РїСЂРѕРІРµРґРµРЅРёРё СЂР°СЃС‡РµС‚РѕРІ']
   202	
   203	=== 5.1.4 ===
   204	required_type: mandatory
   205	only_for_product: common
   206	only_for_lot: common
   207	only_for_terminal: common
   208	payment_method: common
   209	main_idea: 
   210	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРё РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СѓРґРµСЂР¶Р°С‚СЊ СЃСѓРјРјС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї. 5.1.1 Р”РѕРіРѕРІРѕСЂР°, РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРѕСЃР»РµРґСѓСЋС‰РµРјСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅР° РѕРїР»Р°С‚Сѓ РёР»Рё РїР»Р°С‚РµР¶РЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ Рѕ СЃРїРёСЃР°РЅРёРё РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ Рє СЂР°СЃС‡РµС‚РЅРѕРјСѓ СЃС‡РµС‚Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ в„– ---------
   211	topics: ['СѓРєР°Р·Р°РЅ РЅРѕРјРµСЂ СЂР°СЃС‡РµС‚РЅРѕРіРѕ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'СѓРєР°Р·Р°РЅРѕ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ Р‘Р°РЅРєР°, РІ РєРѕС‚РѕСЂРѕРј Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РѕС‚РєСЂС‹С‚ СЃС‡РµС‚']
   212	
   213	=== 5.1.5 ===
   214	required_type: mandatory
   215	only_for_product: common
   216	only_for_lot: common
   217	only_for_terminal: common
   218	payment_method: common
   219	main_idea: 
   220	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РќРµ РІРѕР·РјРµС‰Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°.
   221	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅРµ РІРѕР·РјРµС‰Р°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР°']
   222	
   223	=== 5.1.6 ===
   224	required_type: mandatory
   225	only_for_product: common
   226	only_for_lot: common
   227	only_for_terminal: common
   228	payment_method: common
   229	main_idea: 
   230	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїСЂРѕРІРµСЂРєСѓ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ Рё РїРѕСЂСЏРґРєР° СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР°, СЂР°СЃРїРѕР»РѕР¶РµРЅРЅС‹С… РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў. РџСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР°, Р° С‚Р°РєР¶Рµ РѕР±РЅРѕРІР»СЏС‚СЊ РїСЂРѕРіСЂР°
   231	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРµСЂСЏС‚СЊ С‚РµС…РЅРёС‡РµСЃРєРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·Р°РєР°Р·С‡РёРєР° Р·Р° 2 СЂР°Р±РѕС‡РёС… РґРЅСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±РЅРѕРІР»СЏС‚СЊ РџРћ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·Р°РєР°Р·С‡РёРєР° Р·Р° 2 СЂР°Р±РѕС‡РёС… РґРЅСЏ', 'Р”РѕРїСѓСЃРєР°РµС‚СЃСЏ СѓРґР°Р»РµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ РџРћ С‚РµСЂРјРёРЅР°Р»РѕРІ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ РїРѕСЂСЏРґРєР° РѕРїРµСЂР°С†РёР№ Рё Р±РµР· РїСЂРµРґРІР°СЂРёС‚РµР»СЊРЅРѕРіРѕ СѓРІРµРґРѕРјР»РµРЅРёСЏ']
   232	
   233	=== 5.1.7 ===
   234	required_type: mandatory
   235	only_for_product: common
   236	only_for_lot: common
   237	only_for_terminal: common
   238	payment_method: common
   239	main_idea: 
   240	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РќРµР·Р°РІРёСЃРёРјРѕ РѕС‚ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РёР»Рё РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РћРїРµСЂР°С†РёР№ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ, РІ С‚РѕРј С‡РёСЃР»Рµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїРµСЂРµРґР°С‡Сѓ РґР°РЅРЅС‹С… (СЃРІРµРґРµРЅРёСЏ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў/Р РµСЃСѓСЂСЃРµ, РІ С‚РѕРј С‡РёСЃР»Рµ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ/РїСЂРµРґСЃ
   241	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РїСЂРё РІС‹СЏРІР»РµРЅРёРё РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№', 'Р‘Р°РЅРє РїРµСЂРµРґР°РµС‚ РґР°РЅРЅС‹Рµ РІ РџР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РњР�Р  РїСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РёР·-Р·Р° РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР°', 'РџРµСЂРµРґР°РІР°РµРјР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ РІРєР»СЋС‡Р°РµС‚ РґР°С‚Сѓ Р·Р°РєР»СЋС‡РµРЅРёСЏ Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°, РїСЂРёС‡РёРЅСѓ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Рё РґСЂСѓРіРёРµ СЃРІРµРґРµРЅРёСЏ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё']
   242	
   243	=== 5.1.8.1 ===
   244	required_type: optional
   245	only_for_product: common
   246	only_for_lot: common
   247	only_for_terminal: common
   248	payment_method: common
   249	main_idea: 
   250	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°;
   251	topics: ['РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°']
   252	
   253	=== 5.1.8.2 ===
   254	required_type: optional
   255	only_for_product: common
   256	only_for_lot: common
   257	only_for_terminal: common
   258	payment_method: common
   259	main_idea: 
   260	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РІ РѕС‚РЅРѕС€РµРЅРёРё РєРѕС‚РѕСЂС‹С… РёРјРµСЋС‚СЃСЏ
   261	topics: ['РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РїСЂРёС‡Р°СЃС‚РЅС‹С… Рє СЌРєСЃС‚СЂРµРјРёР·РјСѓ, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЋ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°']
   262	
   263	=== 5.1.8.3 ===
   264	required_type: optional
   265	only_for_product: common
   266	only_for_lot: common
   267	only_for_terminal: common
   268	payment_method: common
   269	main_idea: 
   270	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїСЂРё РЅР°Р»РёС‡РёРё Сѓ Р‘Р°РЅРєР° РїРѕРґРѕР·СЂРµРЅРёР№, С‡С‚Рѕ РћРїРµСЂР°С†РёРё РІ РўРЎРў/РЅР° Р РµСЃСѓСЂСЃРµ СЃРѕРІРµСЂС€Р°СЋС‚СЃСЏ РІ С†РµР»СЏС… Р»РµРіР°Р»РёР·Р°С†РёРё (Рѕ
   271	topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РѕС‚РјС‹РІР°РЅРёРµ РґРµРЅРµРі РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёРµ С‚РµСЂСЂРѕСЂРёР·РјР°']
   272	
   273	=== 5.1.8.4 ===
   274	required_type: optional
   275	only_for_product: internet_acquiring
   276	only_for_lot: common
   277	only_for_terminal: common
   278	payment_method: common
   279	main_idea: 
   280	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ;
   281	topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР°']
   282	
   283	=== 5.1.8.5 ===
   284	required_type: optional
   285	only_for_product: internet_acquiring
   286	only_for_lot: common
   287	only_for_terminal: common
   288	payment_method: common
   289	main_idea: 
   290	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, СѓРєР°Р·Р°РЅРЅС‹С… РІ РўСЂРµР±РѕРІР°РЅРёСЏС… Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ;
   291	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё Р—Р°РєР°Р·С‡РёРєРѕРј Р·Р°РїСЂРµС‰РµРЅРЅС‹С… РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё СЃРѕРіР»Р°СЃРЅРѕ РўСЂРµР±РѕРІР°РЅРёСЏРј Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
   292	
   293	=== 5.1.8.6 ===
   294	required_type: optional
   295	only_for_product: common
   296	only_for_lot: common
   297	only_for_terminal: common
   298	payment_method: common
   299	main_idea: 
   300	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїРѕР»СѓС‡РµРЅРёРµ РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў /Р РµСЃСѓСЂСЃРµ  РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё Р Р¤
   301	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ СЂРµСЃСѓСЂСЃРµ РѕС‚ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹']
   302	
   303	=== 5.1.8.7 ===
   304	required_type: optional
   305	only_for_product: common
   306	only_for_lot: common
   307	only_for_terminal: common
   308	payment_method: common
   309	main_idea: 
   310	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїРѕР»СѓС‡РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ РІ РўРЎРў /РЅР° Р РµСЃСѓСЂСЃРµ ;СЃС‚РѕСЂРѕРЅС‹ РґРѕРіРѕРІРѕСЂРёР»РёСЃСЊ, С‡С‚Рѕ РґРѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕ
   311	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ', 'Р”РѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° СЏРІР»СЏСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹', 'РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РјРѕР¶РµС‚ Р±С‹С‚СЊ РїРѕР»СѓС‡РµРЅРѕ РїРѕ С„Р°РєСЃСѓ РёР»Рё СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚Рµ']
   312	
   313	=== 5.1.8.8 ===
   314	required_type: optional
   315	only_for_product: trade_acquiring
   316	only_for_lot: common
   317	only_for_terminal: common
   318	payment_method: common
   319	main_idea: 
   320	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЋ РћРїРµСЂР°С†РёР№;
   321	topics: ['РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РѕРїРµСЂР°С†РёСЏРј', 'Р±Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РґР»СЏ РўРЎРў', 'Р±Р°РЅРє РІРїСЂР°РІРµ РёРЅРёС†РёРёСЂРѕРІР°С‚СЊ СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РґРѕРіРѕРІРѕСЂР°']
   322	
   323	=== 5.1.8.9 ===
   324	required_type: optional
   325	only_for_product: common
   326	only_for_lot: common
   327	only_for_terminal: common
   328	payment_method: common
   329	main_idea: 
   330	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ Р»РёР±Рѕ РІРѕР·Р±СѓР¶РґРµРЅРёРµ РІ РѕС‚РЅРѕС€РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРё
   331	topics: ['Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РІРѕР·Р±СѓР¶РґРµРЅРёРµ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ Р·Р°РєРѕРЅСѓ в„–127-Р¤Р—']
   332	
   333	=== 5.1.8.10 ===
   334	required_type: optional
   335	only_for_product: common
   336	only_for_lot: common
   337	only_for_terminal: common
   338	payment_method: common
   339	main_idea: 
   340	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂ
   341	topics: ['РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РўРЎРў', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
   342	
   343	=== 5.1.8.11 ===
   344	required_type: optional
   345	only_for_product: common
   346	only_for_lot: common
   347	only_for_terminal: common
   348	payment_method: common
   349	main_idea: 
   350	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ 
   351	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РїСЂРµРґРїСЂРёСЏС‚РёСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РІС‹СЏРІР»РµРЅРЅРѕРј РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі Р·Р°СЏРІР»РµРЅРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё']
   352	
   353	=== 5.1.8.12 ===
   354	required_type: optional
   355	only_for_product: common
   356	only_for_lot: common
   357	only_for_terminal: common
   358	payment_method: common
   359	main_idea: 
   360	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ;
   361	topics: ['РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°']
   362	
   363	=== 5.1.8.13 ===
   364	required_type: optional
   365	only_for_product: common
   366	only_for_lot: common
   367	only_for_terminal: common
   368	payment_method: common
   369	main_idea: 
   370	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°, СѓРєР°Р·Р°РЅРЅРѕРіРѕ РІ Рї. 10.1 Р”РѕРіРѕРІРѕСЂР°.
   371	topics: ['РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°', 'РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°']
   372	
   373	=== 5.1.9 ===
   374	required_type: mandatory
   375	only_for_product: common
   376	only_for_lot: common
   377	only_for_terminal: common
   378	payment_method: common
   379	main_idea: 
   380	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў, РІ С‚.С‡. РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё.
   381	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё']
   382	
   383	=== 5.1.10 ===
   384	required_type: mandatory
   385	only_for_product: common
   386	only_for_lot: common
   387	only_for_terminal: common
   388	payment_method: common
   389	main_idea: 
   390	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІ С‚.С‡. РЅР° РїСЂРµРґРјРµС‚ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РѕРїРµСЂР°С†РёР№, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёС… СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў, РЅРµСЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў С‚СЂРµР±РѕРІР°РЅРёР№, СѓСЃ
   391	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РџСЂРѕРІРµСЂРєРё РїСЂРѕРІРѕРґСЏС‚СЃСЏ РґР»СЏ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° Рё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СЂРѕРґР° РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РЅРµРј', 'РџСЂРѕРІРµСЂРєРё РІРєР»СЋС‡Р°СЋС‚ РєРѕРЅС‚СЂРѕР»СЊ СЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј С‚СЂРµР±РѕРІР°РЅРёР№ Р”РѕРіРѕРІРѕСЂР° Рє Р РµСЃСѓСЂСЃСѓ', 'Р‘Р°РЅРє РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕСЃС‚СѓРї Рє РѕС‚РґРµР»СЊРЅС‹Рј Р·Р°РєСЂС‹С‚С‹Рј СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° РїСЂРё РїСЂРѕРІРµСЂРєР°С…']
   392	
   393	=== 5.1.11 ===
   394	required_type: mandatory
   395	only_for_product: common
   396	only_for_lot: common
   397	only_for_terminal: common
   398	payment_method: common
   399	main_idea: 
   400	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р—Р°РїСЂР°С€РёРІР°С‚СЊ Р”РѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РЅРµ РїРѕР·РґРЅРµРµ 13 (С‚СЂРёРЅР°РґС†Р°С‚Рё) РјРµСЃСЏС†РµРІ СЃ РґР°С‚С‹ СЃРѕРІРµСЂС€РµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РІ Рї. 4.2.10 Р”РѕРіРѕРІРѕСЂР°. Р”Р»СЏ Р°РЅР°Р»РёР·Р° СЃРїРѕСЂРЅС‹С… СЃРёС‚СѓР°С†РёР№ Р‘Р°РЅРє С‚Р°РєР¶Рµ РјРѕР¶РµС‚ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ Р·Р°СЏРІР»РµРЅРё
   401	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ Р·Р°РїСЂР°С€РёРІР°С‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј', 'Р‘Р°РЅРє РјРѕР¶РµС‚ С‚СЂРµР±РѕРІР°С‚СЊ РїРёСЃСЊРјРµРЅРЅРѕРµ Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ СЃС‡РµС‚Р°, С‡РµРєРё Рё РёРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р±Р°РЅРєР°', 'РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ РєР°РЅР°Р»С‹ СЃРІСЏР·Рё СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°']
   402	
   403	=== 5.1.12 ===
   404	required_type: optional
   405	only_for_product: common
   406	only_for_lot: common
   407	only_for_terminal: common
   408	payment_method: common
   409	main_idea: 
   410	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ РґРѕРєСѓРјРµРЅС‚С‹, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ Р”РѕРіРѕРІРѕСЂРµ, РїСѓС‚РµРј РїСѓР±Р»РёРєР°С†РёРё РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР° РЅРµ РјРµРЅРµРµ С‡РµРј Р·Р° 1 (РѕРґРёРЅ) РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РґРµРЅСЊ РґРѕ РІРІРµРґРµРЅРёСЏ РІ РґРµР№СЃС‚РІРёРµ СѓРєР°Р·Р°РЅРЅС‹С… РёР·РјРµРЅРµРЅРёР№.
   411	topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ СЃРІСЏР·Р°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ unilateral_in_one_day_right', 'РћРїСѓР±Р»РёРєРѕРІР°РЅРёРµ РёР·РјРµРЅРµРЅРёР№ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°']
   412	
   413	=== 5.1.13 ===
   414	required_type: optional
   415	only_for_product: common
   416	only_for_lot: common
   417	only_for_terminal: common
   418	payment_method: common
   419	main_idea: Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµРґРѕРјР»РµРЅРёСЏ, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
   420	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РёР·РјРµРЅРµРЅРёСЏ СЂРµРєРІРёР·РёС‚РѕРІ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹С… РІ Р”РѕРіРѕРІРѕСЂРµ, СѓРІРµРґРѕРјРёС‚СЊ РѕР± СЌС‚РѕРј РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСѓС‚РµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°. 
   421	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РёР·РјРµРЅСЏС‚СЊ СЃРІРѕРё СЂРµРєРІРёР·РёС‚С‹', 'РЈРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёРё СЂРµРєРІРёР·РёС‚РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· РћС„РёС†РёР°Р»СЊРЅС‹Р№ СЃР°Р№С‚ Р‘Р°РЅРєР°']
   422	
   423	=== 5.1.14 ===
   424	required_type: mandatory
   425	only_for_product: common
   426	only_for_lot: common
   427	only_for_terminal: common
   428	payment_method: common
   429	main_idea: 
   430	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ С†РµР»СЏС… РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі /Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў.
   431	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РђРґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ СѓРєР°Р·Р°РЅ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ', 'Р—Р°РїСЂРѕСЃС‹ РЅР°РїСЂР°РІР»РµРЅС‹ РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј']
   432	
   433	=== 5.1.15 ===
   434	required_type: optional
   435	only_for_product: common
   436	only_for_lot: common
   437	only_for_terminal: common
   438	payment_method: common
   439	main_idea: 
   440	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· РѕР±СЉСЏСЃРЅРµРЅРёСЏ РїСЂРёС‡РёРЅ.
   441	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· СѓРєР°Р·Р°РЅРёСЏ РїСЂРёС‡РёРЅ']
   442	
   443	=== 5.1.16 ===
   444	required_type: mandatory
   445	only_for_product: common
   446	only_for_lot: common
   447	only_for_terminal: common
   448	payment_method: common
   449	main_idea: 
   450	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°
   451	topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј']
   452	
   453	=== 5.1.17.1 ===
   454	required_type: optional
   455	only_for_product: trade_acquiring
   456	only_for_lot: common
   457	only_for_terminal: pos
   458	payment_method: common
   459	main_idea: 
   460	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє 
   461	topics: ['РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±']
   462	
   463	=== 5.1.17.2 ===
   464	required_type: optional
   465	only_for_product: trade_acquiring
   466	only_for_lot: common
   467	only_for_terminal: smart
   468	payment_method: common
   469	main_idea: 
   470	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ 5.1.17.2. РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕ
   471	topics: ['С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏРј Р±Р°РЅРєР°', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°']
   472	
   473	=== 5.2.1 ===
   474	required_type: mandatory
   475	only_for_product: internet_acquiring
   476	only_for_lot: common
   477	only_for_terminal: common
   478	payment_method: common
   479	main_idea: 
   480	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РћРїРµСЂР°С†РёР№.
   481	topics: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ', 'РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ']
   482	
   483	=== 5.2.2 ===
   484	required_type: mandatory
   485	only_for_product: internet_acquiring
   486	only_for_lot: common
   487	only_for_terminal: common
   488	payment_method: common
   489	main_idea: 
   490	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№ РІ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіРµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Рё РўРµС…РЅРѕР»РѕРіРёР№ 3DSecure
   491	topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё', 'РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure']
   492	
   493	=== 5.2.3 ===
   494	required_type: mandatory
   495	only_for_product: trade_acquiring
   496	only_for_lot: common
   497	only_for_terminal: common
   498	payment_method: common
   499	main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»РєРё РЅР° СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј РЅРµ СЏРІР»СЏРµС‚СЃСЏ
   500	enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЈСЃС‚Р°РЅРѕРІРёС‚СЊ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№. РџСЂРѕРІРµСЃС‚Рё РїРµСЂРІРёС‡РЅС‹Р№ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹РјРё Р‘Р°РЅРєРѕРј
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
AI: Let me continue reading the contract text and also read the legal propositions for the batch items.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_t2tXlJ9ueiG8P0nVBCVW0977', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 100}, 'id': 'call_01_0r5Mgn8tpmovrN2frusF2149', 'type': 'tool_call'}]
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
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предостав",
     7	      "type": "operative",
     8	      "materiality": "evaluable",
     9	      "protected_party": "Банк",
    10	      "bound_party": "Предприятие",
    11	      "right_or_obligation": "процедура/условие",
    12	      "legal_object": "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    13	      "trigger": "",
    14	      "deadline": "",
    15	      "amount_formula_cap": "",
    16	      "procedure_channel": "электронные каналы",
    17	      "liability_remedy": "",
    18	      "scope_options": [],
    19	      "consequence": "",
    20	      "applicability_filters": {}
    21	    },
    22	    {
    23	      "id": "2.2",
    24	      "source_text": "Важен факт, что валюта рубль РФ, другая валюта недопустима Расчёты производятся в рублях Российской Федерации Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    25	      "source_excerpt": "Важен факт, что валюта рубль РФ, другая валюта недопустима Расчёты производятся в рублях Российской Федерации Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    26	      "type": "operative",
    27	      "materiality": "evaluable",
    28	      "protected_party": "Банк",
    29	      "bound_party": "Предприятие",
    30	      "right_or_obligation": "процедура/условие",
    31	      "legal_object": "Расчёты производятся в рублях Российской Федерации",
    32	      "trigger": "",
    33	      "deadline": "",
    34	      "amount_formula_cap": "",
    35	      "procedure_channel": "",
    36	      "liability_remedy": "",
    37	      "scope_options": [],
    38	      "consequence": "",
    39	      "applicability_filters": {}
    40	    },
    41	    {
    42	      "id": "2.3.1",
    43	      "source_text": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса. Обмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту; Информация и документы, направленные по электронной почте, имеют юридическую силу Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Предприятия за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Договоре, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
    44	      "source_excerpt": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса. Обмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и бан",
    45	      "type": "operative",
    46	      "materiality": "evaluable",
    47	      "protected_party": "Банк",
    48	      "bound_party": "Предприятие",
    49	      "right_or_obligation": "процедура/условие",
    50	      "legal_object": "Обмен информацией по электронной почте; Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту; Информация и документы, направленные по электронной почте, имеют юридическую силу",
    51	      "trigger": "",
    52	      "deadline": "",
    53	      "amount_formula_cap": "",
    54	      "procedure_channel": "электронные каналы",
    55	      "liability_remedy": "",
    56	      "scope_options": [],
    57	      "consequence": "",
    58	      "applicability_filters": {}
    59	    },
    60	    {
    61	      "id": "2.3.2",
    62	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами посредством системы ДБО или аналогичных систем Банка Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;",
    63	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами посредством системы ДБО или аналогичных систем Банка Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним и",
    64	      "type": "operative",
    65	      "materiality": "evaluable",
    66	      "protected_party": "Банк",
    67	      "bound_party": "Предприятие",
    68	      "right_or_obligation": "процедура/условие",
    69	      "legal_object": "Обмен документами посредством системы ДБО или аналогичных систем Банка",
    70	      "trigger": "",
    71	      "deadline": "",
    72	      "amount_formula_cap": "",
    73	      "procedure_channel": "система ДБО",
    74	      "liability_remedy": "",
    75	      "scope_options": [],
    76	      "consequence": "",
    77	      "applicability_filters": {}
    78	    },
    79	    {
    80	      "id": "2.3.3",
    81	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
    82	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способо",
    83	      "type": "operative",
    84	      "materiality": "evaluable",
    85	      "protected_party": "Банк",
    86	      "bound_party": "Предприятие",
    87	      "right_or_obligation": "процедура/условие",
    88	      "legal_object": "Обмен документами с доставкой нарочным или курьером",
    89	      "trigger": "",
    90	      "deadline": "",
    91	      "amount_formula_cap": "",
    92	      "procedure_channel": "электронные каналы",
    93	      "liability_remedy": "",
    94	      "scope_options": [],
    95	      "consequence": "",
    96	      "applicability_filters": {}
    97	    },
    98	    {
    99	      "id": "2.3.4",
   100	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами через заказное письмо Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",

