## Summarized at 2026-06-25T14:32:10.150088+00:00

Human: Contract coverage batch 2 (ids 5.3.18.2 to end)
AI: I'll start by reading the skill file and understanding the task, then locate the source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_DBIZQYzOaTTiGXeiRjDP4025', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/*', 'path': '/'}, 'id': 'call_01_GcXJ5acNiKoAv7M65y3K2497', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-discrepancy-analysis
     3	description: "Compare a bank acquiring standard matrix with a counterparty acquiring contract using bidirectional legal proposition coverage."
     4	---
     5	
     6	# Acquiring Discrepancy Analysis
     7	
     8	Use this skill to compare a Bank standard acquiring matrix with a counterparty
     9	acquiring contract. The matrix is the Bank standard. The contract is the checked
    10	document. The goal is a complete many-to-many legal proposition graph and a
    11	two-sheet legal review report.
    12	
    13	Before the final answer, read:
    14	
    15	- `references/output-contract.md`
    16	- `references/comparison-patterns.md`
    17	
    18	## Inputs And Outputs
    19	
    20	Inputs:
    21	
    22	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    23	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    24	  applicability filters.
    25	- `inputs/contract.txt`: full counterparty contract text. Use only printed
    26	  clause ids or real document locators visible in this file.
    27	
    28	Final outputs:
    29	
    30	- `/outputs/discrepancy_analysis.json`: machine-readable graph and ledgers.
    31	- `/outputs/discrepancy_analysis.xlsx`: two-sheet report:
    32	  `Contract-Matrix` and `Only in Matrix`.
    33	
    34	Working outputs under `/outputs/working/` are allowed. They are not final
    35	answers.
    36	
    37	## Core Model
    38	
    39	Normalize both documents into legal propositions before matching.
    40	
    41	A legal proposition has:
    42	
    43	- `id`: matrix number or printed contract locator;
    44	- `source_text`: short source excerpt or matrix requirement;
    45	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
    46	  `appendix`, `table`, or `technical`;
    47	- `protected_party`, `bound_party`, `right_or_obligation`, `legal_object`;
    48	- `trigger`, `deadline`, `amount_formula_cap`, `procedure_channel`;
    49	- `liability_remedy`, `scope_options`, `consequence`;
    50	- `applicability_filters`: product, lot, terminal, payment method, and legal
    51	  regime where available.
    52	
    53	Do not treat `definition`, `heading`, `signature`, `requisites`, blank forms,
    54	and purely technical text as final legal findings unless they contain an
    55	operative right, duty, procedure, amount, liability, restriction, or legal
    56	consequence.
    57	
    58	## Required Workflow
    59	
    60	### 1. Source Preflight
    61	
    62	Check that `inputs/contract.txt` has real clause numbering before analysis.
    63	If numbering is visibly broken, such as repeated `0.x`, missing deep clause
    64	numbers, or section children attached to the wrong parent, stop and write an
    65	error artifact under `/outputs/working/source_preflight_error.json`. Do not run
    66	legal analysis on invalid extracted text.
    67	
    68	Mechanical source repair belongs before the agent receives the contract. During
    69	legal analysis, do not silently "fix" contract ids in final outputs.
    70	
    71	### 2. Clause Index
    72	
    73	Create a complete source map:
    74	
    75	- `/outputs/working/clause_index.json`
    76	
    77	It must include every matrix item and every contract clause, definition,
    78	operative parent, appendix/table row, and unnumbered operative provision.
    79	This is a source map only. It is not the legal answer.
    80	
    81	Canonical artifact lock:
    82	
    83	- `/outputs/working/clause_index.json` is the canonical full source map. Do not
    84	  overwrite it with a scoped, batch, sampled, or range-limited index.
    85	- If you need a batch, write it to a separate file such as
    86	  `/outputs/working/matrix_batch_01.json`.
    87	- The canonical index must cover every `number` from `inputs/matrix.json`.
    88	  A matrix subset is invalid even if the current worker scope is narrower.
    89	- Contract locators that repeat in the main contract and appendices must keep
    90	  context in the working artifact, for example a section title, appendix title,
    91	  source line, or contextual locator. Do not collapse different source rows into
    92	  one ambiguous id during analysis.
    93	
    94	### 3. Text Evidence Ledger
    95	
    96	Create:
    97	
    98	- `/outputs/working/legal_propositions.json` or another text evidence ledger
    99	
   100	For each evaluable matrix and contract clause, preserve the source text needed
   101	for comparison:
   102	
   103	- matrix: `number`, `enriched_text`, `main_idea`, `topics`, applicability
   104	  filters, and required type;
   105	- contract: printed locator, full clause text, section/applicability context,
   106	  appendix/form context where relevant.
   107	
   108	Extracted fields such as `deadline`, `amount_formula_cap`, `trigger`, or
   109	`consequence` are optional navigation aids only. They are not the source of
   110	truth and they must not be the only basis for status. If an extracted field is
   111	empty or wrong, read and compare the underlying `enriched_text` and contract
   112	clause text directly.
   113	
   114	This step is mandatory as a text ledger, not as a binding entity extraction
   115	layer. The matching and status steps must use the actual source text.
   116	
   117	Before matching, run:
   118	
   119	```bash
   120	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working
   121	```
   122	
   123	Fix invalid source-map artifacts before delegating comparison work.
   124	
   125	### 4. Contract Product Profile
   126	
   127	Create:
   128	
   129	- `/outputs/working/contract_product_profile.json`
   130	
   131	Record the contract's product, lot, terminal scope, payment methods, and legal
   132	regime (`common`, `44_fz`, `223_fz`, or other). Use this profile before any
   133	missing or deviation decision.
   134	
   135	Rules:
   136	
   137	- `common` matrix items apply to every contract.
   138	- A matrix item with `only_for_product`, `only_for_lot`,
   139	  `only_for_terminal`, or `payment_method` applies only when the profile
   140	  matches that filter.
   141	- A non-applicable mandatory item is reported as `missing_in_contract` with low
   142	  or conditional risk, not as a linked deviation.
   143	- Slash-separated alternatives are options unless the matrix explicitly says
   144	  all options are mandatory. If the contract selects one permitted option, do
   145	  not mark deviation merely because other slash alternatives are absent.
   146	- A placeholder or blank in an applicable term is a low-risk `deviation` when
   147	  the legal element must be filled.
   148	
   149	### 5. Bidirectional Matching
   150	
   151	Run both directions:
   152	
   153	- Matrix to contract: for each applicable evaluable matrix proposition, find
   154	  all contract propositions that collectively cover the Bank standard.
   155	- Contract to matrix: for each evaluable contract proposition, find the matrix
   156	  proposition group it covers, or classify it as `extra_in_contract`.
   157	
   158	Create true many-to-many groups. One contract row may correspond to several
   159	matrix ids. One matrix id may require a contract package.
   160	
   161	Do not create links for weak topic matches. A legal analogue requires the same
   162	or closely equivalent protected party, bound party, legal object, operative act,
   163	trigger where material, and legal consequence. Weak candidates may be recorded
   164	as rejected evidence in `unmatched_matrix`.
   165	
   166	Coverage relevance:
   167	
   168	- Clauses used as legal coverage must relate to the analyzed matrix requirement:
   169	  same or closely equivalent legal object, protected/bound party, operative act,
   170	  material trigger, and consequence.
   171	- A clause that merely contains a useful date, amount, signature method,
   172	  notification rule, payment phrase, or liability phrase does not provide
   173	  coverage unless it governs the same duty/right being analyzed.
   174	- Context clauses may be mentioned as background, source location, or general
   175	  procedure. They do not need to be final candidates if they are not used to
   176	  cure a gap or change status.
   177	- If a context/framework clause is used to prove that a material element is
   178	  covered, or to cure a missing hard term, state why it legally applies to that
   179	  same obligation. Otherwise it cannot affect `aligned`/`deviation` status.
   180	- Include in final `contract_ids` the clauses that provide material coverage
   181	  for the group. Do not include purely background clauses only to satisfy a
   182	  formal pool rule.
   183	
   184	### 6. Group-Level Status
   185	
   186	Status is assigned to the linked group, not to each atomic pair.
   187	
   188	- `aligned`: the contract package preserves the Bank standard's legal result.
   189	- `deviation`: there is a true analogue, but a material element differs or is
   190	  missing.
   191	- `missing_in_contract`: the matrix requirement has no true contract analogue.
   192	  Mandatory missing is high risk; optional or non-applicable missing is low or
   193	  conditional risk.
   194	- `extra_in_contract`: a legally significant contract proposition has no matrix
   195	  analogue.
   196	- `not_material`: only for internal ledgers. Do not put non-material items into
   197	  final `unmatched_contract`.
   198	
   199	Material deviations include changed or missing deadline, amount, formula, cap,
   200	penalty, protected party, bound party, trigger, scope, procedure, channel,
   201	liability, Bank right, merchant duty, exception, or consequence.
   202	
   203	Hard-term comparison is text-grounded:
   204	
   205	- Compare the Bank standard text from `matrix.enriched_text`, `main_idea`, and
   206	  `topics` against the full text of legally relevant coverage clauses.
   207	- If the matrix text requires `3 working days` and the contract package also
   208	  contains the same legal deadline, the deadline is covered.
   209	- If the matrix text requires `3 working days` and the contract package has
   210	  `5 working days`, another materially different period, or no period at all,
   211	  the group is `deviation`.
   212	- Do not borrow a hard term from a neighboring or general clause unless that
   213	  clause expressly governs the same legal object and obligation, or the linked
   214	  clause explicitly incorporates it. A general deadline for other requests does
   215	  not cure a missing deadline in a specific Bank-standard duty.
   216	- Apply the same rule to amounts, percentages, caps, penalty formulas, named
   217	  procedures/channels, party allocation, trigger events, and consequences.
   218	- Do not rely on a pre-extracted `deadline` or `amount` field to decide this.
   219	  Re-read the source text whenever the status depends on a hard term.
   220	
   221	Do not downgrade aligned rows for wording style, heading/title changes,
   222	permitted option selection, equivalent mandatory-law mechanism, or missing
   223	slash alternatives outside the selected product/profile scope.
   224	
   225	### 7. Closure QA
   226	
   227	Create:
   228	
   229	- `/outputs/working/coverage_ledger.json`
   230	
   231	It must close:
   232	
   233	- every evaluable matrix id as `linked` or `missing_in_contract`;
   234	- every evaluable contract id as `linked` or `extra_in_contract`;
   235	- every non-evaluable contract id as `not_material` in the working ledger only.
   236	
   237	Before finalizing:
   238	
   239	- every `deviation` has a named legal gap and risk;
   240	- every `aligned` link was checked against the product profile;
   241	- every `aligned` link was checked directly against source text for hard-term
   242	  equality or legal equivalence;
   243	- every clause used as coverage or cited as curing a gap legally relates to the
   244	  same matrix requirement. Background/context clauses may be cited, but they
   245	  must not change status unless their applicability to the same duty/right is
   246	  explained;
   247	- every `missing_in_contract` states whether the item is mandatory, optional,
   248	  or non-applicable/conditional;
   249	- every `extra_in_contract` has independent legal effect and no matrix analogue;
   250	- no weak context appears in final `links`;
   251	- no invented ids or corrected numbering appear in final outputs.
   252	
   253	## Output Discipline
   254	
   255	The final JSON keeps these top-level keys:
   256	
   257	- `links`
   258	- `atomic_links`
   259	- `unmatched_matrix`
   260	- `unmatched_contract`
   261	- `coverage_ledger`
   262	- `analysis_profile`
   263	- `summary`
   264	
   265	`atomic_links` are traceability projections of group links. They do not carry
   266	independent pair-level status. Their `relationship` must match the group.
   267	
   268	The final Excel mirrors the legal answer:
   269	
   270	- sheet 1: contract rows with matrix analogue set and group status;
   271	- sheet 2: matrix requirements absent from the contract.
   272	
   273	## Use Of Tools And Scripts
   274	
   275	Helper scripts are allowed for source extraction, indexing, validation,
   276	coverage checks, metrics, and Excel export. Scripts must stay mechanical. Do
   277	not put legal mapping or status decisions into hardcoded Python tables.
   278	
   279	Allowed helper categories:
   280	
   281	- source numbering validation;
   282	- clause index validation;
   283	- coverage ledger validation;
   284	- JSON schema checks;
   285	- final Excel export from JSON.
   286	
   287	## Final Self-Check
   288	
   289	Finish only after:
   290	
   291	- `references/output-contract.md` was followed;
   292	- `references/comparison-patterns.md` was used for uncertain calls;
   293	- `/outputs/discrepancy_analysis.json` exists;
   294	- `/outputs/discrepancy_analysis.xlsx` exists or a clear export error is
   295	  recorded under `/outputs/working/`;
   296	- summary counts equal final arrays;
   297	- all final ids are source-grounded;
   298	- all legally significant propositions are closed.
Tool: ['/.env', '/.git/COMMIT_EDITMSG', '/.git/FETCH_HEAD', '/.git/HEAD', '/.git/ORIG_HEAD', '/.git/config', '/.git/description', '/.git/hooks/applypatch-msg.sample', '/.git/hooks/commit-msg.sample', '/.git/hooks/fsmonitor-watchman.sample', '/.git/hooks/post-update.sample', '/.git/hooks/pre-applypatch.sample', '/.git/hooks/pre-commit.sample', '/.git/hooks/pre-merge-commit.sample', '/.git/hooks/pre-push.sample', '/.git/hooks/pre-rebase.sample', '/.git/hooks/pre-receive.sample', '/.git/hooks/prepare-commit-msg.sample', '/.git/hooks/push-to-checkout.sample', '/.git/hooks/sendemail-validate.sample', '/.git/hooks/update.sample', '/.git/index', '/.git/info/exclude', '/.git/logs/HEAD', '/.git/logs/refs/heads/clear-branch', '/.git/logs/refs/heads/codex/clear_one_skill', '/.git/logs/refs/heads/demo', '/.git/logs/refs/heads/main', '/.git/logs/refs/heads/one_skill', '/.git/logs/refs/heads/pre=agent', '/.git/logs/refs/heads/test', '/.git/logs/refs/heads/test2', '/.git/logs/refs/heads/test3', '/.git/logs/refs/remotes/origin/HEAD', '/.git/logs/refs/remotes/origin/clear-branch', '/.git/logs/refs/remotes/origin/demo', '/.git/logs/refs/remotes/origin/main', '/.git/logs/refs/remotes/origin/one_skill', '/.git/logs/refs/remotes/origin/pre=agent', '/.git/logs/refs/remotes/origin/test', '/.git/logs/refs/remotes/origin/test2', '/.git/logs/refs/remotes/origin/test3', '/.git/lost-found/other/003f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/lost-found/other/016411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/lost-found/other/0189548f4f27fcb26840150f585a64515d77c26d', '/.git/lost-found/other/01a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/lost-found/other/02e3706e34f211187bd64efa7a9ad51760195d39', '/.git/lost-found/other/02e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/lost-found/other/0312d61983ef80179bfac79abbba1359052f115c', '/.git/lost-found/other/040be927181b9604d69593ffe36ab7303b1a94bc', '/.git/lost-found/other/04378a998f4a8686eb28f62e8833b0f539229714', '/.git/lost-found/other/04602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/lost-found/other/048703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/lost-found/other/0488481d528674a76807703e6625d6284ca8293e', '/.git/lost-found/other/04eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/lost-found/other/057e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/lost-found/other/05c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/lost-found/other/05e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/lost-found/other/0631461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/lost-found/other/074930d053a799cc4f9095e89196437f704205d6', '/.git/lost-found/other/077efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/lost-found/other/07d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/lost-found/other/082169d84ac7751152d7134fa37292c00ba029d0', '/.git/lost-found/other/0846bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/lost-found/other/0a05a2808a79fe98d007bccb3b1060551300dec8', '/.git/lost-found/other/0a32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/lost-found/other/0a401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/lost-found/other/0a56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/lost-found/other/0a962ce910aa746587b34755922bae542449fba9', '/.git/lost-found/other/0b32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/lost-found/other/0b5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/lost-found/other/0bc5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/lost-found/other/0bebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/lost-found/other/0bf720f21f41ce829add4aab5a9a05012208c3f7', '/.git/lost-found/other/0c4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/lost-found/other/0d72d0b2349a404cc4cddb87c836194765377d74', '/.git/lost-found/other/0d753acfba917272cd72f418e9c1352ed20054f6', '/.git/lost-found/other/0e189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/lost-found/other/0f0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/lost-found/other/0f86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/lost-found/other/0f9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/lost-found/other/108486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/lost-found/other/1152abac92eac8d8b605f61e7608e5151d222f07', '/.git/lost-found/other/11b6a93338766923a8e6379405e6fcf4ab828169', '/.git/lost-found/other/11c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/lost-found/other/13360394a41c8fabc39419ab404191a8575e2799', '/.git/lost-found/other/14394b47e18f572003e3d82368702dfd474b70c4', '/.git/lost-found/other/1474c8f7cf8bc22cda503322795cac94ac621675', '/.git/lost-found/other/159a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/lost-found/other/159bfd26b659195df8c8486d12b5e15f948cb808', '/.git/lost-found/other/15be2e474eb938a89e4d7c19737994893197e781', '/.git/lost-found/other/163d050dd4db671d29be7efff1a35864f91ca61d', '/.git/lost-found/other/1645e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/lost-found/other/1683c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/lost-found/other/16de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/lost-found/other/17a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/lost-found/other/17c6782b615441baeb457ee93a458ed7371c9f99', '/.git/lost-found/other/1862eec0af25e420dee69a16ba235f610f20756d', '/.git/lost-found/other/1876a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/lost-found/other/18d512a4ebe9f93cc357a19059984b3398799bee', '/.git/lost-found/other/18fe30c098f75b96caa54450040279f8727780ea', '/.git/lost-found/other/19928324ad53403e47456f49785dd300a6abc1e0', '/.git/lost-found/other/19ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/lost-found/other/1a3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/lost-found/other/1a412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/lost-found/other/1ae3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/lost-found/other/1bb6184cbc8ec7b0b92597da642ddb7baea3f9f0', '/.git/lost-found/other/1bb94dc37fa7ba202e37fb9f730b2c1ffe60c9f8', '/.git/lost-found/other/1bd948006afad9d92ba0af0d9d6aac84b81201ee', '/.git/lost-found/other/1c5c64af7a4a179928feb3e438ba9aeca2b21785', '/.git/lost-found/other/1c6f0d2fcead6d6b9af167efe84b68ab9867253d', '/.git/lost-found/other/1cb460853dbc76ecd603937b1385d60dfe4544da', '/.git/lost-found/other/1ce139b0630235d7cccd5e7233e06fb27e4b7e92', '/.git/lost-found/other/1d80ca727f627adf666f395a0c85e26662ed0d20', '/.git/lost-found/other/1fb978ebe70aba71b3e2d74d673c0459d8480ac6', '/.git/lost-found/other/2083461eff88321aa0feceaab497bc202e7d110e', '/.git/lost-found/other/20d6d5fa6f6982c1d4d8d927ae5e9e121fe42018', '/.git/lost-found/other/21637826d1d04950f4a4d796a9571a8c4d86b806', '/.git/lost-found/other/21c428f3247ee9fb40e38b78c925eea08e7175aa', '/.git/lost-found/other/21d13a0a40c505324dab511aa407e5dc471bcf1c', '/.git/lost-found/other/226a93510d33d1c407aef258f9c39f42e3f298ad', '/.git/lost-found/other/228c08f34331c47620b55794c64c0ff9897f15c0', '/.git/lost-found/other/22baf3300cc31a3540ca4314fd8c58bcb7018353', '/.git/lost-found/other/22e7afb00fe5b7c7602b761800024ed40d25fe21', '/.git/lost-found/other/230d67a0590a4d61346d6dd5ced3f53dd0f1bea2', '/.git/lost-found/other/238faa3816f1afd26933d98bd81001eb92a2c876', '/.git/lost-found/other/242b028657099781ee5f230d30afc0a8af8423df', '/.git/lost-found/other/245ed230dee59261acbdfe117c3db0280411df76', '/.git/lost-found/other/248a3917f8467ac0cc6218d4b046e8e4b2cba851', '/.git/lost-found/other/248fd8353332111067158f2d11e7087f1ac3fe69', '/.git/lost-found/other/2533d1949584c2a0a3b143a5cb4de3f8c1d17758', '/.git/lost-found/other/253f5f1950cdce8f3dd7dca88b26bfcfcb68ad9e', '/.git/lost-found/other/26194e93e2a767b3f44b2bb12906aad486311c49', '/.git/lost-found/other/26204973c5913550889f7735c6c91e3f23eb971d', '/.git/lost-found/other/2676a4fb754239d1306066ad2d8f58004874245b', '/.git/lost-found/other/26bc257b7c543df579db1afcb9248ced695a5433', '/.git/lost-found/other/27e9ed80c1396df06710f8c7782e989d2230e035', '/.git/lost-found/other/2912b2774fce14827260d4c8ec3a58acaebd30aa', '/.git/lost-found/other/29b9a8951ad9517c1953a163da020fe28852bba9', '/.git/lost-found/other/29f91579b798fbdf2436d2f21c966d128bba04fd', '/.git/lost-found/other/2afee31d90e375b801139b051605dc6f5599d9f1', '/.git/lost-found/other/2b77f7188e91b5f41905b979e1453716042a88d6', '/.git/lost-found/other/2b84077d254fc2a1d66d0b4ea82ef3a7fa125c3a', '/.git/lost-found/other/2ba1ae4723622dd7a36a624626a298bc4aede590', '/.git/lost-found/other/2baa9b4b0fd3a53e07dbaa15098f4c45e7419cd6', '/.git/lost-found/other/2bf2efefce1765ad78030310ed9900afb0cd5522', '/.git/lost-found/other/2c59ee393814f03d894d5d8c75ab7512af596f2b', '/.git/lost-found/other/2ca2261abaa3459cab2e6b5aac65911448fb906a', '/.git/lost-found/other/2d209cca9eecd6d9519f21ae66f180d2001554ef', '/.git/lost-found/other/2d808e55af2eb9b6c496d06a8de71c32578f172a', '/.git/lost-found/other/2d926e4fa759b1b3235635ba6668898a635443f9', '/.git/lost-found/other/2d98f0a835a91e49cb26869dc16dea0583feafbe', '/.git/lost-found/other/2e107635a41522a90f0ea3c1f8fbbb3ff8685f1f', '/.git/lost-found/other/2e395785e7e850594fe6874f052e55a0733d4549', '/.git/lost-found/other/2f29d9394aab14b49d63b7303c6549458f4f7158', '/.git/lost-found/other/2f785e870024de3ac7ca3a834b25ca25e9d9cb8e', '/.git/lost-found/other/2f7887c4fbfd68a3721f5d2cdc896c48bf353c5a', '/.git/lost-found/other/2f807662ed402a67cdc3a86d525264af5ff4fb7d', '/.git/lost-found/other/306a8becbe8f0d8eab7964b3986c9f94ff283e20', '/.git/lost-found/other/312308f273d963ad2f881e414e6dc908c7de72c6', '/.git/lost-found/other/313257cee583598c2b1e76531aee4382a34ae791', '/.git/lost-found/other/31919cbc2e7b9a6268f7bd5ade6a59d4902b52dd', '/.git/lost-found/other/31e88c3eb7be2600a07f8a293e0d521af54d6577', '/.git/lost-found/other/31f64f6e3b537ebaddf428c4cb7764d746510f2b', '/.git/lost-found/other/322ad23a9b2322a5eafbb97fd34f393402a04544', '/.git/lost-found/other/323f82bbbb2a2f435ba1a70ab85e6e604de01b6e', '/.git/lost-found/other/325706343725c6011b78dbccbe34e242657d5d49', '/.git/lost-found/other/327e8f6219bc9ac3aaf5c4e5f8a88559dd9c8d9c', '/.git/lost-found/other/328bc3afc9053e448e43ac838fbde8b5a6bff782', '/.git/lost-found/other/32f8032b0690c3e5ab5788e9a392fb328fdde7e4', '/.git/lost-found/other/332c5bfc92dcc95b0fdab72fec060f0f1fde04f7', '/.git/lost-found/other/33a71c56250cf2a2cf3bc20447d3bc0f4722b8c0', '/.git/lost-found/other/3407448373b50404341f30cfe3e19da4562e5b61', '/.git/lost-found/other/341580a820d2cd018774a99fd90cdd4928badc68', '/.git/lost-found/other/34c6a03cca3744f90eb635e4a427cf083aad4110', '/.git/lost-found/other/353eeeb90d31595d072017c457bdb335470c0b79', '/.git/lost-found/other/35425eeca676d4342ab62ffff6195d41b11f03ba', '/.git/lost-found/other/357377a3e9d1596994eb7db5c89ea3b40161b48a', '/.git/lost-found/other/3598090e6a420d70ef76bde587c93ade0de2721e', '/.git/lost-found/other/36228b5f70a00e5ce49800e5c4e6f423a864ae65', '/.git/lost-found/other/3627eb8009d622db55d0b115ad04a86af57dc99d', '/.git/lost-found/other/376c1e88772f0558744c3ec5bf33e514bcbfa5f4', '/.git/lost-found/other/378b9fa979fd0cdcd74fb98be8f965fc64ba96ab', '/.git/lost-found/other/37ab16fcbeb235841f49b53dda4f8a4cb8576605', '/.git/lost-found/other/37eb658dd959056bdc91ca5add0c61677dd55131', '/.git/lost-found/other/3893a9d23c221f7a7587b3bd1bbce3e53451a36b', '/.git/lost-found/other/393d937812a14bacba39114d3fbc6ba4b6f687e1', '/.git/lost-found/other/393f72379d2551529e19191f444ca8ac0324cc09', '/.git/lost-found/other/398f7fdb157e0e718ddb1b583446c83525a9c8c8', '/.git/lost-found/other/3aa11aec8ea158ebe6fa2976edaac47f213d098c', '/.git/lost-found/other/3ae1b05c2a5d648e1e234162415c93a2d566455a', '/.git/lost-found/other/3b05a03bfb9b84a6f82a3f6b6d4fddb652001ca6', '/.git/lost-found/other/3cc5321661d71bea5e919b2dd222d55638ef6474', '/.git/lost-found/other/3d2058541bd6f85fa9d3041eeb94773535041b4e', '/.git/lost-found/other/3d4090fbbcedee422c984f49d6951366d6e87331', '/.git/lost-found/other/3d76e8038eb8c5d0065da0f378418b0929a3e1c7', '/.git/lost-found/other/3dee1d10be4dc43fdf33e57816608eb7f5f762e9', '/.git/lost-found/other/3ec37580b08a3f792df050067bd3383ad9c01df9', '/.git/lost-found/other/3ecc52a19ba9501ffdc2b0775d42316e3eb031db', '/.git/lost-found/other/3f5e76235147c70911902e9f103daf1a7314e95a', '/.git/lost-found/other/3feb49e8ddc04e5c3e85ae2ec34908b7ea1236c6', '/.git/lost-found/other/40758f589a15d70a0fb173d1dd0cd93c2b280b20', '/.git/lost-found/other/40a857d2f4d88afe60d9d223c3874cb9ccb4a55c', '/.git/lost-found/other/421881dda370e44a27a3e93dc9caa1d44579a990', '/.git/lost-found/other/428a345dcc183804917d5077052693bb113f74e0', '/.git/lost-found/other/429074a78b514abba6f272bd54f3011a72c28afc', '/.git/lost-found/other/42fcf8ab7e1224020d789b4b47b37e4eff58c62f', '/.git/lost-found/other/433079b36165ec24a2b3bfa3208be0e72c68112c', '/.git/lost-found/other/447720e79a8bf68b0570557e2603109333a4a04a', '/.git/lost-found/other/44d6e7a95ef488d9350b45e9cfa358ce04beec08', '/.git/lost-found/other/4678157d773d5c250ee875f3fc5ad8cfbb06ae38', '/.git/lost-found/other/46c6456223387aec0a7b111a58be75f442f3c342', '/.git/lost-found/other/46f574b31ea9c081d10dbc24fb57ba3e4b447b6f', '/.git/lost-found/other/472070c0c081ef4c9ea5e73fce87dec51a5e50bd', '/.git/lost-found/other/473daf24f1e540b2f25a569f819a238aacb81035', '/.git/lost-found/other/47eec38c60613993ebddfe34b03b3c993405009b', '/.git/lost-found/other/48355610f438c75b706f3d1b9bb15c49f849800d', '/.git/lost-found/other/49e4545b844c30e3a2dfd5283289f27650feed77', '/.git/lost-found/other/49e5c2487096098aa82596f7c3bf4b154b03263b', '/.git/lost-found/other/4b0ca8a212de55c027ab38e37ffcd17e341d57bc', '/.git/lost-found/other/4b1106adc7b4c0535779dc0c2df302e2e4f26afb', '/.git/lost-found/other/4b4e6a0046c053a95f57754b9088a81834674349', '/.git/lost-found/other/4b5c220106e4b150f1785aca51b4c1516ee7f6f7', '/.git/lost-found/other/4b825dc642cb6eb9a060e54bf8d69288fbee4904', '/.git/lost-found/other/4c109c4291b72213236a54418e69bc70989d3d23', '/.git/lost-found/other/4d64eae0c3986894803d586d4c44ae16906d23f8', '/.git/lost-found/other/4dae699298c4e827eb777a620bc2b0b622a3d043', '/.git/lost-found/other/4daf2d4fb4be2002d0c6f0783065cd4aaa2ef9d5', '/.git/lost-found/other/4db248d2d0362a2baa123bce350af1c3cf725718', '/.git/lost-found/other/4dba40158ad402bdb18ab94f570242af2ecb9f72', '/.git/lost-found/other/4ddb67d026b4d1d9533591627008838db3040342', '/.git/lost-found/other/4e560d39e66ee48393ac86adf8bf92f390ab6282', '/.git/lost-found/other/4e80ac0c1f3b8a9f86cdccef454912a80077d15a', '/.git/lost-found/other/4ed608f4d1b961b4b069673f0dac7b286868f1d4', '/.git/lost-found/other/4f03978e25b1d70dd18b2f1ce83f070616bee53c', '/.git/lost-found/other/4f6403a8bcb6c19a368e929b9a4e12741e1ab55a', '/.git/lost-found/other/4fb85fbb7c372a0b84cd78fa6b55e410e220239f', '/.git/lost-found/other/503b52b471cf3c48677445669dda1dda8fd71c51', '/.git/lost-found/other/50446582fea97fa549a6039a5f0c504364f69e73', '/.git/lost-found/other/509ba1ee9c66d67aa12183a23911275c84c1be12', '/.git/lost-found/other/50ab5d3cf546c8b875e8c8fecb728a69ed6129e1', '/.git/lost-found/other/50c32b19907ec29e0df34ae3dcb64ccbad1bfeed', '/.git/lost-found/other/5135c970168de2f80375b8e8223d8b65ebe722d9', '/.git/lost-found/other/514ef7a257573e892fef8efdc8092aa113f301a6', '/.git/lost-found/other/515672a3eac687eeaa0d5331a88ae03e9eec92ff', '/.git/lost-found/other/51eddaf2d727e3973ab74f8d0d4d5d6925dfccf8', '/.git/lost-found/other/523cfd7c6c11e165293fcbe926464d35abe0f7ea', '/.git/lost-found/other/526cbab8a8237857d96750d81938f8548229fdd4', '/.git/lost-found/other/52a9fd5d5a39c98cf011809f1954ce924858033a', '/.git/lost-found/other/53c00c790d7213e762a416ccbd9fa61f2cc6b27c', '/.git/lost-found/other/549ef64d2ed3890a06bd03ef59952b31b70a5027', '/.git/lost-found/other/54a41810fd052d9463f8d60abf2c75184362b839', '/.git/lost-found/other/55616d36043061c1a3c7f616e099f6a5abde1e72', '/.git/lost-found/other/55769048317ffd40eca0be3cea5a4b9e5ab7cdba', '/.git/lost-found/other/55b747cbbaf511f4d5424f0f1301ed30b1916007', '/.git/lost-found/other/56e2a20d652ee923dad7ebb9d8aeda679efae502', '/.git/lost-found/other/56ea5e17523abc029922afcc9f23f2306cfef729', '/.git/lost-found/other/56f07bf7f1652d395100a1b2e0b96ed2b54e171c', '/.git/lost-found/other/56f3b2f52e650607bcb68a0a89e36251acb754f3', '/.git/lost-found/other/57b04ada3b0285ca34c1a7fdbb9c904e484a2d14', '/.git/lost-found/other/58bf0f7e675b7588a79421a3fabaf0f35e219290', '/.git/lost-found/other/5928f67430c179dc2031c576bf0b24b51d2bca5b', '/.git/lost-found/other/5983ea75fd9362c5a8709fb10cdfa4920f085b40', '/.git/lost-found/other/59a6d7ca7e0bd39f24f74469da806dd2659236c9', '/.git/lost-found/other/59d110fe6522d55e8e5f8650763f5ff86c935b7e', '/.git/lost-found/other/5a1e4a159d9cbf9d18e6e0da20f04e709b36e923', '/.git/lost-found/other/5a41118850b5b97764e3861fc59a901f69f18298', '/.git/lost-found/other/5aed03d61d3a40a4e4d8859a43e5ff373d789afb', '/.git/lost-found/other/5b03c014dcf3dab20b88f5a62dd0865020292ed4', '/.git/lost-found/other/5b3c284ca03de4c25ced51e9aa3a4b488804a44e', '/.git/lost-found/other/5b42a5fe2abb1393cf2b9ac7359176e4aed00c0a', '/.git/lost-found/other/5c40fd7e30b0ae67c6188ae7825d3ecbe2c432b0', '/.git/lost-found/other/5d51b2cf47c9bec0fd8dfc6a5c742839aead66d3', '/.git/lost-found/other/5dc8c414c8a6dcb39eead75672e29a6c7705fa1c', '/.git/lost-found/other/5fc241b5fc5ee3126714b7ec6bb1218f256b2f9d', '/.git/lost-found/other/5ff9751d696b33f83abfca804807e09e998cc015', '/.git/lost-found/other/604dca6b26bd18ef8041517b5520080d7d019360', '/.git/lost-found/other/608826a2afc590737f32a764a625ef1f8c685dd5', '/.git/lost-found/other/60cd35607497b333c4e689ec8c3d7beefb76d5aa', '/.git/lost-found/other/60e755f3531398a88cb2ba67af858c57dd0ab90d', '/.git/lost-found/other/6128184c716e17ff7c4382e61719214b88a65240', '/.git/lost-found/other/612b7e3dac1b05bc83204b5091634dc99d745a5f', '/.git/lost-found/other/613d1efee79b495719629da39214f79500635967', '/.git/lost-found/other/61c62badbeadcca961fde66023da79591e056332', '/.git/lost-found/other/623e4c399c3cf78aa7bff72e26554c85f6869fe6', '/.git/lost-found/other/62a41bba70c8083d3e9792ce06fcf891c6fa24d5', '/.git/lost-found/other/62b286e180ad3b353b79c522e41cac008f3512b0', '/.git/lost-found/other/6372d5b36494f138c1638b3930d8543e77265803', '/.git/lost-found/other/63e70e5456461721b42c484bbee1886cfc8ba39c', '/.git/lost-found/other/63f2e29d53169726763ff4581e6fdcd3236cdb45', '/.git/lost-found/other/640ebd997c31281a5274fbfcdaf9624d3dca7042', '/.git/lost-found/other/64e4f4a1d9a5c5f3af3076ec413de73a3f5a4100', '/.git/lost-found/other/6589cb9582ca26898931b1ff9fa713b99a51fd69', '/.git/lost-found/other/66161534878c9a2771f904c86c37771812f852de', '/.git/lost-found/other/6638f29e468c5eb3550c99e26aff88a106344cba', '/.git/lost-found/other/668ed8f54785171df27bcc3dd3ca6946b7c47b03', '/.git/lost-found/other/669527a55303ac3089986dfdd5be5379da40b8d6', '/.git/lost-found/other/66b958f32ddafa4f75a7a2cb2f24a9e9ccf2a097', '/.git/lost-found/other/66dc9fe2e67543e8bee36d8b809fc2488132e8d1', '/.git/lost-found/other/66f40ce43c80179972266b9fb98da995998b53c3', '/.git/lost-found/other/6702cfd9756562bfb0a3ba9b5abecffb3edd3d4d', '/.git/lost-found/other/6842fe827192bab8f1180cc0a667d476df9cd850', '/.git/lost-found/other/687cde57acd639e44b9f6ecf4bb3b29996c10bc3', '/.git/lost-found/other/6916bfc4ae8a8656910be8213444648b53a2352d', '/.git/lost-found/other/695a1fc4aabfb29ae1d4eb53d8262b001cf0b268', '/.git/lost-found/other/69ba46d4e80a1ca1f7e61de30c5a0973bcf9949f', '/.git/lost-found/other/6a0e4ee850e4136089b231c7385181f3833d64e5', '/.git/lost-found/other/6a10a4c99f71d892813817d6e131c32de5a3a0b8', '/.git/lost-found/other/6ab43d1c8712b075016024e6de4b2cedad30d4fb', '/.git/lost-found/other/6ab5f05565940fa70b59ade18d5824d49687af69', '/.git/lost-found/other/6ac3752495b076c748fd4e5c4984925643feef75', '/.git/lost-found/other/6b7cbd1cdc3ecae6259e767ec077682ab8140d37', '/.git/lost-found/other/6b874d512a6169e56875de8896ae72ca50462b5a', '/.git/lost-found/other/6bb4e0d4dd0ee5445099c82b2bd2f64a53e8d294', '/.git/lost-found/other/6c03949654187bb18a9d56abf3fa548d35436fac', '/.git/lost-found/other/6c5fc2bdd3439593a8643d755e206e6dfc9fc170', '/.git/lost-found/other/6c8a6bf7a8364e9f3c66b02e8af3048c191749db', '/.git/lost-found/other/6ca4f377708c5ecf6907a214a05573cc42b26244', '/.git/lost-found/other/6cabcbec99c44d58b07d21563b56e3e3ecc9cfe5', '/.git/lost-found/other/6d52ba52a8e301203cf321217bf466872849a86e', '/.git/lost-found/other/6df408815ccc8efcd933582508681c4b44e1d871', '/.git/lost-found/other/6e5315c52f4cb6f8f50c68116b2f12db8d110b4c', '/.git/lost-found/other/6f2516ff42249437779576cb418ec04cb76f8024', '/.git/lost-found/other/6f88ec227ecf2f7b141024b1d501544126a224f2', '/.git/lost-found/other/6fba22d4dc0eb6400d9414150d5b70602d6564bf', '/.git/lost-found/other/6fcf161c510c9b98c91a405a36236d1e7e6111f0', '/.git/lost-found/other/7053cc71e49faa648cb55ce0f0bf2b206c62ad69', '/.git/lost-found/other/7065f6674fe7a8235b352054611ce3983ec2b558', '/.git/lost-found/other/70adf55db7d632e16f7262dbf14637069fc748f0', '/.git/lost-found/other/70d153a9884e3f575ceee6df23bed28105af19ad', '/.git/lost-found/other/70f09f86714b5f1a6772acc9824b08e5148482f8', '/.git/lost-found/other/714397ace6f967f7f6c94a8446aad82e62242f3d', '/.git/lost-found/other/719a970b7bedabe76e51c19aef9d38a694ea8de8', '/.git/lost-found/other/721c0dd9c7733231be83aaabfd84464df8fb6044', '/.git/lost-found/other/728c2ace778aeceb83e85f1bcde65cb271b6a15a', '/.git/lost-found/other/72ebd6a7cfdb38fcc2e0b29564a3b301f7782e32', '/.git/lost-found/other/73fa97fd287d2dbdf544f5995bf4f80996e8dc14', '/.git/lost-found/other/7563c407d2437ca7e9fe67a0bdcfbe9439559381', '/.git/lost-found/other/757a9f890df07ca2d991d61cbaabe564c1e908eb', '/.git/lost-found/other/75e403200b7c6f1e192ff409078d9539db59d5f9', '/.git/lost-found/other/762405ef38fefcce716ce0ce148eeeb530e1e89a', '/.git/lost-found/other/769c1bb07714a82c3cd25c50f256f28519da231c', '/.git/lost-found/other/771d4dfee6367426c05c3d82559b5c866bf59ed8', '/.git/lost-found/other/77349909732fef77c64241e680e95994b7ab6894', '/.git/lost-found/other/776a4bea95d8e9f4deeb6e136104a5d9080dbf4b', '/.git/lost-found/other/777c96837cb78e1e50a9d82e0c0bf6c555dba8a3', '/.git/lost-found/other/77de4ba2f2aef9696037ea20f5e791ec8fc33796', '/.git/lost-found/other/77e3948ebbd8863edb49b35b86613591d4c3a2fc', '/.git/lost-found/other/782871526d2a991f40100b5e32cd3ef1fa465125', '/.git/lost-found/other/78dda83637c001a3bbb5b46fbed552151ed51365', '/.git/lost-found/other/790cbbdb4670edaa8647b93e6e6c5a9fc4aaac3a', '/.git/lost-found/other/7996e753f0d39ff8510fa714661f86e7b916a821', '/.git/lost-found/other/79ae734789ab6ce0d184cc720e51c101d3ee0f59', '/.git/lost-found/other/7a60567d3255257a8ec8ffd90b47253fbb7779e1', '/.git/lost-found/other/7a761a5bd14d2eb15e7fc3dfa4290f5d112ec66c', '/.git/lost-found/other/7aa8a776509d35c4b416ce478c310947105abb78', '/.git/lost-found/other/7b00b279b725540bd5e801557be40c425fec033e', '/.git/lost-found/other/7bed1a58912ef89bb40536ec81317ad4e857a3af', '/.git/lost-found/other/7c31bb200ac9ee3c8526031f3f462dcfbc0c6dcd', '/.git/lost-found/other/7c63e8f7e164de6eac3bf0e4c2c3b86a7006969d', '/.git/lost-found/other/7c6466d64311464b5cc235f012e7eefa7a3f7dec', '/.git/lost-found/other/7c7e207d982350b509a2ff479318fe62ed1103fd', '/.git/lost-found/other/7d1fa3cfc7a26b23468ef0231a6be425c10c39c0', '/.git/lost-found/other/7f1ccef0257eae07e1a9d96c9a419839eb69012b', '/.git/lost-found/other/7fbedd5325332884808b4f13376b20b608ba153d', '/.git/lost-found/other/80417b62ee231928cf6e1894ee78ae9d52dced8f', '/.git/lost-found/other/80525b0220584bb2859e90b7b1ecd96124809e0c', '/.git/lost-found/other/806c3e29a41d7902dc4bfb90b274f7bcdd692396', '/.git/lost-found/other/807fe9f45b577f7b4e832f53598c9132f4634217', '/.git/lost-found/other/80d57ddd52a3d347c46ca1ec7bd6611c3832991f', '/.git/lost-found/other/81b0c9d26060eac103e503fee24c4dc875d73a3d', '/.git/lost-found/other/81b84d2f9246fe95414efaf594ce0d66642af224', '/.git/lost-found/other/81c8e0c1332f8beac34dab5b2d8addd868c78d37', '/.git/lost-found/other/83f433e75ff687ed7ad6e622082b3771f4be902a', '/.git/lost-found/other/83fcd0a4b90b111dd78f24830b0cf0fd6f6662e5', '/.git/lost-found/other/8479528c7d38418a08b92817a5605425c6c65ea9', '/.git/lost-found/other/8507cc0d8827de0caf78209b1bc8b409c30929c3', '/.git/lost-found/other/852f59ef505774d2e1cded9189583af9a7fabfbe', '/.git/lost-found/other/8598ecf10a790316c773068fc621b1ec6a8c7462', '/.git/lost-found/other/85efd595e03f195168517e451a0f6351e2f9e69f', '/.git/lost-found/other/877dbd89e8209c09b4e6117d45aa1ffa5c29123a', '/.git/lost-found/other/87bdeed1fa7053bf3f3ee36c8996eb1a85ca4581', '/.git/lost-found/other/884ad461f9de46bba7b5fb8b37d1f4fb913b128f', '/.git/lost-found/other/88a12ae4891c84ce446aaf38698e7f684d05465d', '/.git/lost-found/other/88de5d8898855804a10e46a2b8ed2efdded56c2d', '/.git/lost-found/other/88ee53c9ece8ef43612f9db4cc25aa5614aa26ad', '/.git/lost-found/other/896dd57e7a94ddfe4430921fddcf78e252b7053e', '/.git/lost-found/other/8a2e1744f8d60b47acee31323eb9be5252f3bb71', '/.git/lost-found/other/8a5e5ad2e568b464c38258b18b07105fa93c8eeb', '/.git/lost-found/other/8b0fe43b479ecc9b599ccb21386dcf6243fab6ef', '/.git/lost-found/other/8badb259266160ed2ae90c6d544e84c1f16bdfa2', '/.git/lost-found/other/8bd53ac2f88091ca967b218668ddeb2b8b901b3b', '/.git/lost-found/other/8c532b7669a3fd0dc35dabdd43d2b34db2726089', '/.git/lost-found/other/8c7f0d1ecd32895777182562810997d842a1cc5a', '/.git/lost-found/other/8cdaba2214ca080e13141a212a14fa3492dee9a6', '/.git/lost-found/other/8dcf63db4819ce835831f19b7f843f66cf331057', '/.git/lost-found/other/8e147d7dafa9de53bdfdf1afdd2288c7015dab9b', '/.git/lost-found/other/8e1df140ffb6a1a2e0e1dbc48231a1341416d5ef', '/.git/lost-found/other/8e624b995ed2e8b2f8a1fde05616b92165f1b612', '/.git/lost-found/other/8e6e6dca3e2142e6450e31de9dcc15e1315d11d1', '/.git/lost-found/other/8e8cc43769b3e51927bb486257e5d2389bdfe3e7', '/.git/lost-found/other/8f29fcc619ffc635697fc2d2d468888819a7c05d', '/.git/lost-found/other/8f8a2153b54a03fb30f2d21c11b2fc65b5071796', '/.git/lost-found/other/903e19a32e203d03671b31f6e27ebaa907166d90', '/.git/lost-found/other/9040ad1040d2f81d6eba6d481dc29f2a5f5b2f73', '/.git/lost-found/other/9052c9897d84020cc14786b82536af8a94cad0e3', '/.git/lost-found/other/9124c4e8d7b6925e2de9f96ba7ee66e9cfbd5b4f', '/.git/lost-found/other/91364a90eb688a950083474549ee42e8e0eaf78f', '/.git/lost-found/other/91897ad77d725aab215d18fc41d34a68ad6b142b', '/.git/lost-found/other/91e214a28a493c3c2e35325fb7245d6983ea71ca', '/.git/lost-found/other/921a6caed41c95b6bba1e56724fe34b038245416', '/.git/lost-found/other/924d93052389d0b9434705bfe32ef317528044d9', '/.git/lost-found/other/92f0a102283a69d06abb892c5d78980a6a4d2652', '/.git/lost-found/other/932ab411aba0a979eb6a54f3c43832011843338f', '/.git/lost-found/other/9437d9d6ad6a559a5d535231870cc81d2e5f61e2', '/.git/lost-found/other/94ddb92592b2844dab2a6dbf6b54c3ec65c53adc', '/.git/lost-found/other/9596ea8c380e21e2936eebc4d43cc3da5c3945dc', '/.git/lost-found/other/95b3c141d6f33fa02247dc87531e793b05061531', '/.git/lost-found/other/960849ac9a576a80ffaaf0a558644a959e85d725', '/.git/lost-found/other/96947147a4afca1db6085e927b1a9a03d61ffd73', '/.git/lost-found/other/96f0c3a29711baf739f8d206549147833769309f', '/.git/lost-found/other/970b3536b39e69354428d28cb4461dc2b51077a4', '/.git/lost-found/other/979c845eeee9c7ea69e9be82ea0152129d99ab94', '/.git/lost-found/other/98330f2a74870e2eacf010a3dc6ebf02ba786210', '/.git/lost-found/other/98634d3201e655b428c3720dfc45a1deaf0fd370', '/.git/lost-found/other/98ddac6847239f0b68e04184b7c57cbffa12398f', '/.git/lost-found/other/98e1a00c29c13261193d33d35e8b870695aabfbc', '/.git/lost-found/other/9900a37055c69f4e8b8b84d6c679c7340cf21a2a', '/.git/lost-found/other/990b82d5c7737e7d79db4d7ee986945bee8c8b04', '/.git/lost-found/other/9964532f1952d9499823130c76cd62602dea68b4', '/.git/lost-found/other/99c369006665885b83433b1cada3e5998e5155b2', '/.git/lost-found/other/99d222d5d2d4742cfd70b247b8bceadd95fc4706', '/.git/lost-found/other/9a0d0a46f1f98aeebacd8915237221e8debc95fc', '/.git/lost-found/other/9abb4897f6f8e61f116f836df7fc815e683a5611', '/.git/lost-found/other/9ac9a25da69a69c9c6ecb565b8e855d3d39d4dd0', '/.git/lost-found/other/9ad7f9e4369acab40cfded3808876b7574f9390b', '/.git/lost-found/other/9b3627817278c3f1ea9f6f4fe2f8301d898b829c', '/.git/lost-found/other/9b4e06037e8da97ab1ce8591a052374860695c5f', '/.git/lost-found/other/9bf0e2c09edf77769e6856ecc475bb3bb86e45be', '/.git/lost-found/other/9c27c00a245e6db44d7f5dc05a9cda11bd241541', '/.git/lost-found/other/9c74f64ab7aa883b162a1b9a609b5647bf5cd115', '/.git/lost-found/other/9ca456f075c2c0aaebd5b2ee1a4529343cae45c7', '/.git/lost-found/other/9ce852637d31e71fc377559d79ac748027fea48e', '/.git/lost-found/other/9d3c14c4f7938219293f9b76798d587e36c29b99', '/.git/lost-found/other/9e7bd621f9a76c674f8c274753799ccaf07ab55a', '/.git/lost-found/other/9e7f02dc92c9bc10fba29f964c50c9f139a1f589', '/.git/lost-found/other/9ea482d56803dd81be7b63e60097e6171c004ce5', '/.git/lost-found/other/9ebd3ce8fe0e3f922060aacac32204ed38da03a8', '/.git/lost-found/other/9f2eec154f15568fdd976cb3ae4e296109e7642f', '/.git/lost-found/other/9fc8d58ef08ad56a92992a215cc0d76a5a8e94c9', '/.git/lost-found/other/a04ce92e7a6147503abde51c6d85c05f86763678', '/.git/lost-found/other/a0c6bdb727822d3ab28dd61c67b3b37832815978', '/.git/lost-found/other/a10ae35925626c8b16596f15a53aeab6a11ab5e5', '/.git/lost-found/other/a1ed013aa410ae8695f45a7019736ba3aa4fb275', '/.git/lost-found/other/a25b902ee65824da9fde90776f0ce686e07a4581', '/.git/lost-found/other/a2f2284bc6fa8fc3a142bcbc0414b14049c57475', '/.git/lost-found/other/a338a909318e642c29073226649ebc4667d40b25', '/.git/lost-found/other/a36298d1d7b41881fac3c262062753c14127c8a7', '/.git/lost-found/other/a3caec65273aae2d693f4bfa2ee2a2c3752c2ff6', '/.git/lost-found/other/a3ecb7025e3ede63635a7694860348298f2e6e77', '/.git/lost-found/other/a414fe1ef5a241eff31f88d267edb7378955ec3f', '/.git/lost-found/other/a4309913d0cf5df6e6ccc045ae0f19920001c3eb', '/.git/lost-found/other/a58d7bef5dcad55f29f6dd15f0fc3987e451d1f4', '/.git/lost-found/other/a59b9efc0a9636dce78f5c92fbac5d12d6da5647', '/.git/lost-found/other/a6091b6528df1b125c8e9a0fe31343e9b7e139eb', '/.git/lost-found/other/a60b71d615d71869dca5168f0a99487c02d7cf8d', '/.git/lost-found/other/a67d281fc3a06505d1f68688b8d19c1e7fd55d3c', '/.git/lost-found/other/a6a759f6ee5fe3e0998931bc1eb5f57b6d0a609e', '/.git/lost-found/other/a6bb3453ea72177cf803ae97da3ec7274f8bbe65', '/.git/lost-found/other/a6cc2e6efe55819439b2708bc7ef7d10a3dec179', '/.git/lost-found/other/a7417b0977cd4198ec223dbc7fe686683e6a56d7', '/.git/lost-found/other/a7b0ac4f7ba3b423ba8809cfca928693e9e1b555', '/.git/lost-found/other/a7f0b07ebde57e5af0354e2e76d73b8117ef9cd8', '/.git/lost-found/other/a8767737857edbde46d7c5760f644a3b145c4ec9', '/.git/lost-found/other/a907f6a155563583a84747b32b7897bc06d314d6', '/.git/lost-found/other/a93a02538f4107b5f0f6ba68d1e05106976618c7', '/.git/lost-found/other/a93f4d121ad5241432d6cece42ace11ef7d0d2dc', '/.git/lost-found/other/a9853bc470d2fd3c56ce24576650041dbddde66d', '/.git/lost-found/other/a9ab2c49d5af7d6df614bb0d578636ab64f181e7', '/.git/lost-found/other/aaceb0768852c7f4f7b7c086357a2b8319a67929', '/.git/lost-found/other/aad8d903158dca56e2301e3ac4a33d5c6765216f', '/.git/lost-found/other/ac48e387584c53d2cfd7867eb6983ca441277203', '/.git/lost-found/other/ad01876a896dd65578176da823c8d3eaf54a42cc', '/.git/lost-found/other/ad3b3036bc53b249ae74260b5df361c826ac41ab', '/.git/lost-found/other/ada35cdc23336af6d19f92c7bf023f84ef2c151f', '/.git/lost-found/other/ae67253d3690c041ae2f59e4d478510f04b183f5', '/.git/lost-found/other/af52068b4ddd08dafc65e05439cf72aa219d5e83', '/.git/lost-found/other/af9ff336b88c378508e3cd7eadd284d262242cc6', '/.git/lost-found/other/afa3bad6ecc1a686d44b7bf918da7c679e035577', '/.git/lost-found/other/afb28756840a3cd65e4389c4517d9216301057f4', '/.git/lost-found/other/b07a4b8db64b3990643478d8e05cc9b47efd6416', '/.git/lost-found/other/b11605b4c79cd6f830bc45162a5c28bc0dd0f013', '/.git/lost-found/other/b2913bc33fef9ceb13bae2b1c447cdc6fd1ae360', '/.git/lost-found/other/b2a71cf28f23bb8095e044f07a944b9ca46e36a5', '/.git/lost-found/other/b2f9faaf121213671fb5a7774e930d58f70151a4', '/.git/lost-found/other/b33fdbf692bc1bf33c45a12649e6d8805a7f12ec', '/.git/lost-found/other/b3e1f079730f15c805b6b1810f74a8950f7a5ee5', '/.git/lost-found/other/b40b773210056f26f750cfee0483ec7aa5a89590', '/.git/lost-found/other/b44c8d334c2720cedf3955e92d3a023f4d935c56', '/.git/lost-found/other/b52f477c7218624d8ec93a1acb97bc9bcfa8b9b0', '/.git/lost-found/other/b61fc9ec0d624a6fb5a3ee24de53e66839f36032', '/.git/lost-found/other/b7be51217a56e37c6e38cbbe732a0be92de0bc07', '/.git/lost-found/other/b817d6933884dd6c456522fa9c7215cbedbbc519', '/.git/lost-found/other/b8752d4fdff6b8b0ca56bc1b4d9697f1fa622767', '/.git/lost-found/other/b90b713046a8a15ec14fb0e8ac68bb50d20a22da', '/.git/lost-found/other/ba377d4c5675fe1b5496849fe1448ddee13cdf6d', '/.git/lost-found/other/bb53afb3ef890767ea09e0ec09cc8cf2f9d8b39c', '/.git/lost-found/other/bb920cc2a629754a612a360ab11e2e8a41929ffa', '/.git/lost-found/other/bbfa79a5aaac10800f659c1cf83de2b8f8f90d87', '/.git/lost-found/other/bc4e5bb47af0514e26b1fe0c3254b632c96c026c', '/.git/lost-found/other/bca71aa7a50f8e50f169ad8d7add475fcc88bae9', '/.git/lost-found/other/bcc4a536f944a78bc04830054c79a409585ee7a4', '/.git/lost-found/other/bcdda04baefba90a18ba44b74c2c6eaaddc5d028', '/.git/lost-found/other/bd2a1d030621759771ad4027c2a94150eac7a09f', '/.git/lost-found/other/bd9261ab35b09829e088a6da1aa076e98c524ead', '/.git/lost-found/other/bdbf5e7bd9efb4d363a7232fdec9cad6567d4cbb', '/.git/lost-found/other/be7d6b812f8433589a87bb6495b4dddbe12a0ee9', '/.git/lost-found/other/beb000038b4da9845ad1a638aade10236c7d7703', '/.git/lost-found/other/bef0994468110ae1fc1694af7188bcf5ca0918f1', '/.git/lost-found/other/bf29bfe9c49976b90984553d373029c8f53d8040', '/.git/lost-found/other/c03390e5b753aa22c85f2068144225856150c11c', '/.git/lost-found/other/c0577eb4a15bbf25fd3a5c58452d7f966970a69a', '/.git/lost-found/other/c194da9b62f88b61252dbfce48b0b5362f5e1a35', '/.git/lost-found/other/c198cf463656fd32c0cded88779f2e22d72c4c4d', '/.git/lost-found/other/c19bc78a96c49ef4677eea5af4526afe0617162a', '/.git/lost-found/other/c1d668567275777ab9130946e2e3a7195bb5920c', '/.git/lost-found/other/c1f6cc14efbc61641331679fb61606b1ae829c0f', '/.git/lost-found/other/c2a0ac42490e5986b165952d7702d65c06970ed2', '/.git/lost-found/other/c346cb932c8beb66f5dc30c662c2c41289d3598b', '/.git/lost-found/other/c3f599b00b12002d2a61a73ff0aa13d7524e832d', '/.git/lost-found/other/c415f7c2b19c281f1d670ac1c62606ef4ef79a2b', '/.git/lost-found/other/c4a684183d09535a773af72d1041476920339632', '/.git/lost-found/other/c4e7a00850f5045485ea31f07d406a573c62d04c', '/.git/lost-found/other/c4eb1dcec6f8749915f0f71285c5393955d98c6a', '/.git/lost-found/other/c52fe8f0592d844cbd901ce7bc44e0b1f11e64a7', '/.git/lost-found/other/c574d09175f0180319b6842ccfb2ede440e3a125', '/.git/lost-found/other/c5fdc494e96d7e2815ec1b92abd6cae192d0b95a', '/.git/lost-found/other/c63908d1df7973f503b327b3a48148ecb2a139a7', '/.git/lost-found/other/c68ffcfe5aef9991dd01696a443428d38a0c03a0', '/.git/lost-found/other/c6984ab03c0317af14fcb24630b38be6eca741bd', '/.git/lost-found/other/c6a161ff323e566d554ab18b7d4f58c2e3946d8e', '/.git/lost-found/other/c6a5564c6dd6cdd3429cd3326281f442e6c96cc1', '/.git/lost-found/other/c7a5ab9a45bc9a2e82c6cc9544c5b3c2d09abba8', '/.git/lost-found/other/c7afbe4ad776d0eaa7ec1e8b758d36a48572595d', '/.git/lost-found/other/c7f226c68b6c7fd47dc744bb8e0bdcfcd59110c3', '/.git/lost-found/other/c7fda2d48e4ec697b6ef93c8d41788cd050dd1c3', '/.git/lost-found/other/c829c60a45724554da4b097b17581af2e8a5216e', '/.git/lost-found/other/c8378ac3c120fd9b632b99b60e2700265d8f2195', '/.git/lost-found/other/ca0c53580589aaab2e623db4b1a3811974e04c03', '/.git/lost-found/other/cb68ee666c8f1f8773633ecd067416094eedab53', '/.git/lost-found/other/cb8d4858190a15278307f18d5ea943d1be41019c', '/.git/lost-found/other/cbe58ca7e55701aa03b44dfefd37ab577c6e2699', '/.git/lost-found/other/cd216e02b02ab615377718fc9d57a85fe3bed359', '/.git/lost-found/other/cdfd8467dc6ab25e4cb3c9fbad0356f018dd0263', '/.git/lost-found/other/ce0f148e5050d5462b9fa4a7218443611f540662', '/.git/lost-found/other/ce4226f7495b39011397a2f6a1352391068b55c0', '/.git/lost-found/other/ce57928fd558f7fbc027f3aafbcc951a0a5ff7d8', '/.git/lost-found/other/ce8b9095bbe8c455e3a083d1d2bf00fc3f95b68f', '/.git/lost-found/other/ceaf0b0c7041d998228f7cc55d506013d4e2660f', '/.git/lost-found/other/cf21155b406ffe5d1ec58b2bfb3280f9adc9d734', '/.git/lost-found/other/cf589f7e7cd10bc0893d142bf2b1787bd13a98a9', '/.git/lost-found/other/cf9d67c816b6afce8b699b4509d0482602be5a42', '/.git/lost-found/other/cff0d14042e370123492e5b41e77144ae2b6a234', '/.git/lost-found/other/d04428fc4d2377186583fd4be601a67be5de3ae2', '/.git/lost-found/other/d06cdb63841efd6f9d57da0a49d556d1e0193d21', '/.git/lost-found/other/d0fcc1e31590864b6d8ff451e2fdb118673f4f27', '/.git/lost-found/other/d11859d8b7f96cecfa199c1d97d294e7edb9b643', '/.git/lost-found/other/d16351fb26ba3350c0a7cbe33983581748916efe', '/.git/lost-found/other/d1924c37cf129b3171b889e6d0595a74de2dddce', '/.git/lost-found/other/d196bd9551e1cb5459af29b2dd471c413a752b2c', '/.git/lost-found/other/d1c237bf893070207c137c6b4c8692712bfdd8ff', '/.git/lost-found/other/d21237aa1e63fd7757ca66048f14e65990c070a2', '/.git/lost-found/other/d2453b4648cfb34f34b9758f6146f469b0a57607', '/.git/lost-found/other/d2b4354cce6142de4373869d6869d8d3fc5384dd', '/.git/lost-found/other/d3584209a11765fd9897e316865f6378b924fb08', '/.git/lost-found/other/d3701779a329a7ad2f0c33373d48687b0325a176', '/.git/lost-found/other/d5d57e5acef03490f3e11000082c513a6947397a', '/.git/lost-found/other/d5fe79282acedc0c62e6f1f058c20fec777f0753', '/.git/lost-found/other/d69e4e4828e0e860c901c27d846fdd2695d13a7b', '/.git/lost-found/other/d6a97a089030a7edd8b329c8ae905eda7d8cb77d', '/.git/lost-found/other/d6db780d0f4b775d5c38a76758fbd072c433fc5b', '/.git/lost-found/other/d6ec37f282939964e41bf2de2675c39731b21cf8', '/.git/lost-found/other/d6f6b42a5113049affff24f3057a16240e5b761e', '/.git/lost-found/other/d767ea26e44c64d7e9b3803c0fe5b09b0172b5eb', '/.git/lost-found/other/d77b3a691e389d0ab088e72c10008c645344b08c', '/.git/lost-found/other/d80cd503dfa13d070109f2dab443f74be8f41ab2', '/.git/lost-found/other/d856d9cd9646a8c8567ee9af9551b2e43eb2b2b9', '/.git/lost-found/other/d91fea1942d87936873c4497ea5f8398dbbd1259', '/.git/lost-found/other/d95654384b6318ecb9abec998e2c64599769f652', '/.git/lost-found/other/d9e204dc5438684c55642ac4c4f5edb79aac85b0', '/.git/lost-found/other/da122377427fb4592c6703f54c9850535bb57e00', '/.git/lost-found/other/da129bba6bb8d62d9de2da9a239c1cb59e1a06bf', '/.git/lost-found/other/db1d00fcc5c8d09c5303493b6802f45e19162edc', '/.git/lost-found/other/dbda401cd34b991d08fe06946884135f0eeaaec6', '/.git/lost-found/other/dcac869fe6630d02093d2d6d4d423c3abfc5414f', '/.git/lost-found/other/dd13313f0b99c3e5722ba2f169ec1630d4090956', '/.git/lost-found/other/dd9df54fb86de4a812d2d5c14f9d5d302eb0a895', '/.git/lost-found/other/df212e1724e830f02c6f7c48baa386937ef8a8e4', '/.git/lost-found/other/dfd989fa24c652eda8b3caacf8465401d8a15fe1', '/.git/lost-found/other/dfed33fa2c962d9b941e06eb1904add340c5c1a6', '/.git/lost-found/other/e043fdbdecb337c2509db1da715bc608c7e5c457', '/.git/lost-found/other/e05eb2e28b2f121792aecb7cc2c9d3835a99f45d', '/.git/lost-found/other/e0c9d873acdde10922f8b3fe006a65790cf1d033', '/.git/lost-found/other/e0d3f4acaad9831a78cde41b9465650d8ac882c0', '/.git/lost-found/other/e17608611f7ca0f1bc68ff088dff1d0b226934ef', '/.git/lost-found/other/e1af2f444391dc6bed835532f09731b5f9991ea4', '/.git/lost-found/other/e2391518db03b590ccce8e1cbd97c243d3495201', '/.git/lost-found/other/e25b83ade139fd5d022aeba14351f302855bc80c', '/.git/lost-found/other/e2c5ecab8eb12e570a291601bacaf7b9d74279fa', '/.git/lost-found/other/e2ff6027c01c11460a38172570e89c9eaf403cc7', '/.git/lost-found/other/e31315b59db6da959c44aae02afdea6a956d6749', '/.git/lost-found/other/e3362e7b28e5bc000858f79e7808bca8378d65c3', '/.git/lost-found/other/e3dd33d57725ad5c51131c5a4ff2a6baa90a7bff', '/.git/lost-found/other/e418f732044b83b44c55a3d8bcdce822dda2d201', '/.git/lost-found/other/e44f18e830600f291259dd01272612bfa620c51b', '/.git/lost-found/other/e49b0ca82b56b90bebb8278e7399bca8a0664fcb', '/.git/lost-found/other/e503ca98487014da5da23cb42963fc8f1ba24da0', '/.git/lost-found/other/e520acb374bf8c6935bc34fa047d318e675611e9', '/.git/lost-found/other/e5a46d4f237e3ab7c53f212cb9b976ea970e1344', '/.git/lost-found/other/e5d997d2e7d0dfa63294bb5eb482acc1e88f8980', '/.git/lost-found/other/e674b96ab8e8f0f47f0a21b11a6aab353fd952ad', '/.git/lost-found/other/e780940b9beb3aa95c0e8141615546cc43e3beb2', '/.git/lost-found/other/e82ce186470aab5d29d55e09ed28c972a6631138', '/.git/lost-found/other/e8602005a19d6eee72b7e70d9ac70f5da48bc0f8', '/.git/lost-found/other/e88fed00aaa2ce25272c7f42ea7f6aa0216dbd2a', '/.git/lost-found/other/e988e0b91b3e936c0b22dc2471b12b685e7a32d4', '/.git/lost-found/other/e98a51c0a5e69d042a9a6831d845e3f47b6f877b', '/.git/lost-found/other/e9b1d8f0265d0958e8a5b4a6e8c822f1703e561b', '/.git/lost-found/other/e9e3231e30ffc553ddbfc6f85432deba73d86ba7', '/.git/lost-found/other/ea0d0f9b7b627a6646f6d51864ff418f34902679', '/.git/lost-found/other/eb014d2e1a941a9af381c2744eace9fb4eee73cf', '/.git/lost-found/other/eb19f3b0cff3fca757d4ca80219f4ae1fe43e6e3', '/.git/lost-found/other/eb9cbadf8efbb1fc517fa7295d03720da31509d2', '/.git/lost-found/other/eba33a9bd67e3209a6c680d5018f3a68c9a1efe0', '/.git/lost-found/other/ebceda64425af0c067023a8307110a93375ffd45', '/.git/lost-found/other/ebe2ec685146f680a315f128c349c1dbf90adb00', '/.git/lost-found/other/eccd1e176da943989ae2606c2b88b88a9fc437b9', '/.git/lost-found/other/ece03b567137bf1de7f0e8bf9c5a4966a5713149', '/.git/lost-found/other/ed6fea00087480c1025065a44af8ebd9d7579ceb', '/.git/lost-found/other/ed87c4d1b13d5253f80f8e338600741e25e76691', '/.git/lost-found/other/edd4de5068941df19e47f2c46ba92c179e006fc1', '/.git/lost-found/other/edecb464de5a85816f1a834eabb5a70fda930567', '/.git/lost-found/other/eec85fbed6da5a379fb1231e3cdd297457f45913', '/.git/lost-found/other/eef1dbc15dfd6b66e0695323ee6b6a27d8c8d620', '/.git/lost-found/other/ef2ed056c509290708f0af3df007e352c215f659', '/.git/lost-found/other/ef417fe36253d71abb1df1c24cb00c029f36c191', '/.git/lost-found/other/efc42a741226285057099f826136a954c9f60f10', '/.git/lost-found/other/eff77e32c35f9ef44aabbcab2d36737b118026bd', '/.git/lost-found/other/f06da463f9b4911fb844b3fdf989eb2e4b65229c', '/.git/lost-found/other/f09d1df8015f8bb959b34440b1dd8b37cfb11008', '/.git/lost-found/other/f0bd3f073c0d35a30be9e8db6196f98c10bc36e8', '/.git/lost-found/other/f0d1fee8f3aa5faee3a47eff72cb5f72b64144b8', '/.git/lost-found/other/f0f15c5214e9b65a671bf8c8a746fd62bd3bbb04', '/.git/lost-found/other/f157b9093d30086676020a187f11fac6aa511ac4', '/.git/lost-found/other/f1d80bcd5b7b96a9d8b84da0aa1e0456f8b81c80', '/.git/lost-found/other/f22f4f45cf11ce898f3bb59999bcfb92bcf27878', '/.git/lost-found/other/f2667bb108c5556bddb66621a82124d94e57ffa2', '/.git/lost-found/other/f2a49c9f94a304cbdd8c63e63618f514dd430fdf', '/.git/lost-found/other/f3a1936aa92f749281b00a97f46c85c0f3faeb3d', '/.git/lost-found/other/f42b592f53441bc52a46117d0dd396eb602408a7', '/.git/lost-found/other/f4434f6a34c53588be267f04ba5c83f53c63bcf0', '/.git/lost-found/other/f44a8e423549bc7bdb6a49e232c498f4f4ac1fbf', '/.git/lost-found/other/f6eee227d2cffdc9cd3c598fdd731988f75dab78', '/.git/lost-found/other/f74174bc51b61272e8d1106c065feeb9270bb198', '/.git/lost-found/other/f79731037b392d638382b00776eb115ad82d5a10', '/.git/lost-found/other/f798ab67c883b2c2437da785757dd4acc8ec2802', '/.git/lost-found/other/f7ae7eebd292d07443f6b71fcf69a4d58e600dcf', '/.git/lost-found/other/f7e04c7b89185faa008005238823e991d473d6b9', '/.git/lost-found/other/f809cda2ab8e302b1f5d8d456bc48517331888fa', '/.git/lost-found/other/f83d5ab03367fb5642286c45e104911a5f07b3d7', '/.git/lost-found/other/f8e82125cb443505eecb0d55785a053fdca7692e', '/.git/lost-found/other/f8f69ff5df79ea2afc60bcd584898e85d69dbe70', '/.git/lost-found/other/f9e6c91fc25475e54f13be5d3b540a079341fc2b', '/.git/lost-found/other/fa6978edc179dd7f5080701f86e4b87dba737809', '/.git/lost-found/other/fa71d85dac9e3a9dcafb1eddff0a06d6a1f8d89e', '/.git/lost-found/other/fad5f2c59e6ac92d7d2c2bbda552b8bbaff05be0', '/.git/lost-found/other/fb26b03b1c71350bb0cad1dfdf58d62963cc8c83', '/.git/lost-found/other/fb374affc79708bc948a360c508e21faaab4ebb9', '/.git/lost-found/other/fb69ef7c7afa41527b8ea058d3a983d41b9a6b39', '/.git/lost-found/other/fba48324fd82a30093cb9276fb462866dca04776', '/.git/lost-found/other/fbd5050d803a8bc8ede5dc38f21b85f0d6340f20', '/.git/lost-found/other/fc2ab51db9df28d1cea1ad609b1f6a4be02876d9', '/.git/lost-found/other/fc6e8d45ae5418dae578e0a5cc014fe2cef7d73f', '/.git/lost-found/other/fcc1871fd0b91f9512edff43cb9f9c6d93381ab1', '/.git/lost-found/other/fd209fbb5c2ecd03c306b65055023886d98a12fb', '/.git/lost-found/other/fd618bcb1a6d81feccfa30bda3c1ec83f6c99da9', '/.git/lost-found/other/fd7391d5c0e8395ad01076f9710de2fd352e0f91', '/.git/lost-found/other/fd7996fc223885596b22d096f1c130f9ecca483a', '/.git/lost-found/other/fdc7410fe2c49ac323b138a6420b1573d24b0e87', '/.git/lost-found/other/fdee2ee54a319f9fe963492c028efea79eca32cd', '/.git/lost-found/other/fe7bb38beba7a69323458420123e865a56856a48', '/.git/lost-found/other/fe7cebff670146550df068f2f90bd7399ac8739d', '/.git/lost-found/other/ffbdb38129ee775fef20071909e5ff669e40abf4', '/.git/lost-found/other/ffe72238f13a07462b349f317290814b1d8a21d5', '/.git/objects/00/025daef50b48b9a7c3aa0957f67692b7cf9644', '/.git/objects/00/2531ad23eafab03d76205914b3760606265e11', '/.git/objects/00/279ba916b80ee7f054dcfe4bcad5fdf3d0cad4', '/.git/objects/00/3f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/objects/00/5291f4fcabd5eeb99dea4a438422225f9104fc', '/.git/objects/00/52dd8f0d35e7d44cabe09971d6e0f21ca39cd2', '/.git/objects/00/560ef0fbd6334815132007e408901acbace1e8', '/.git/objects/00/646ef1f6f7efeaeb3e5c6a38e238fa5728b8e7', '/.git/objects/00/6f8e8695b0a66ae47eb9f76ad1bc0e7b0f036d', '/.git/objects/00/85d4e575161ca79d7c14bb62cf89246ac6e4cd', '/.git/objects/00/9107e59a300c960ee6ec2a0fd55630b53e6a77', '/.git/objects/00/a92ed33a5c9c699f84cf5e7ac486d7789874d9', '/.git/objects/00/bb4eb3c57678c53ecdb996159c28d816ca8abe', '/.git/objects/00/bf2ee6092a4428c1c240774794e6c695ff4722', '/.git/objects/00/bfb9f789c6aa35ba63147502679a101296cb0c', '/.git/objects/01/03d9023b3c0be99b13d162789304c2695289b2', '/.git/objects/01/08acc654101c39e74de3cb6404c4fa80bc7bad', '/.git/objects/01/10b4b49800261c96b2f11847c83fdd04e60b20', '/.git/objects/01/4d2f0fd6dffe4835f741728459499991b22962', '/.git/objects/01/5abae91e08022c92cb6c24e1e1097ec60a9c6b', '/.git/objects/01/6411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/objects/01/686fb3f6afa2208defd34a9188169a7884eccf', '/.git/objects/01/72babe377620bb36cde7d6318983b28943f5e9', '/.git/objects/01/7b31bf525f3b189f3119394c79bb4284fddfb0', '/.git/objects/01/81bd6955aab80579d81db279fbd9cf97044fca', '/.git/objects/01/89548f4f27fcb26840150f585a64515d77c26d', '/.git/objects/01/8bd6292885242b8fc321e98611b86abbef7035', '/.git/objects/01/92dc92789e642707957b713071f72a8450b714', '/.git/objects/01/a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/objects/01/bd8bbf0fc579feada35ebba3beadd61b3fa934', '/.git/objects/01/d51ab31a7a5ba8671eb706887eb123d0ec57f9', '/.git/objects/01/d9bb05d576e6db8b5775d37cbac01368f4fb94', '/.git/objects/01/f4c581d56f69b4e25af1f5ebc05ebec603c3f7', '/.git/objects/01/f88f8377947a49ec1cfa7a9b32b89b69dbef4b', '/.git/objects/02/02764beb43a71df5e2d8c411b8c22833417961', '/.git/objects/02/0c91471cd156225ca0b6684340335e17c9587d', '/.git/objects/02/1d956a833b156e5835bb90f20f2fb257686999', '/.git/objects/02/4337837f4b10ca80598d1b777c7ddb3382a7db', '/.git/objects/02/4da679e39764f8e2a1862074bc7d3a67b39a2e', '/.git/objects/02/500954f54d824bf47a0c40e7249570c8ae35a6', '/.git/objects/02/54144a053e6691f5da797289b3815221e244ee', '/.git/objects/02/5c0c10f9864685f955733e39cfd79d22ae1352', '/.git/objects/02/6d0d210de6d3b148a6616c9a49368f14c09c7f', '/.git/objects/02/7cd9077d41da5280567175993abb09c6e81add', '/.git/objects/02/7e36728d1dcc8ff7c167c7c719f406b537c61f', '/.git/objects/02/97c9b7194e6e16e58b7fad80617595ec60797a', '/.git/objects/02/9f3344bdabc6fa51d3a3317b8344c9d12fda27', '/.git/objects/02/b6d03e7eec58ab7e5edb099c5e17243fdcae88', '/.git/objects/02/b6d0803b43000eff745e76727f7a0785cfb736', '/.git/objects/02/c139017e618c759476e436e3fb5fea75a042b4', '/.git/objects/02/ce21bab26cb69adfd9643ec4c839dc7a316ed4', '/.git/objects/02/e3706e34f211187bd64efa7a9ad51760195d39', '/.git/objects/02/e5c435ffbd7357cd76f7c19bf5f4451ea88c3d', '/.git/objects/02/e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/objects/03/098a8322f9458ba797697f7cfdf272e30f91a7', '/.git/objects/03/09d7c803accd0e64d899fd8e0cfb1098a815d6', '/.git/objects/03/12d61983ef80179bfac79abbba1359052f115c', '/.git/objects/03/21b0ebc8efdee894f75380930206da9f16ece5', '/.git/objects/03/21cc3ec2443f4d85700dfe3f808368fbed568b', '/.git/objects/03/46900bf395f5f0160d317d392abb7aa026c7a3', '/.git/objects/03/56133446ed7dfa697229a2b5c19f243e35f443', '/.git/objects/03/7233cb441e842bfda192053568fe3488f544f4', '/.git/objects/03/732f0c6e6eeaef66eda4e4a6de308b7e7e1e95', '/.git/objects/03/7e5e882489a7413c4a62c63d0617b5931284f5', '/.git/objects/03/992f453ea274349984b8262b02650fd1b8bca9', '/.git/objects/03/9efba89af1d0d8bc7aae3c352c34e0c51701af', '/.git/objects/03/c02ba7211ba7f8588931520e8be278972d8269', '/.git/objects/03/c3557176983f991148ff39a6afd493bdf711df', '/.git/objects/03/cdbdebe4e5bc4b0f7a70e153e8be75dafe3324', '/.git/objects/03/d1d893b164cdfc9957a88495c3449fc4538ccb', '/.git/objects/03/f10215da3a690e8f4a1155755ae2b506c5f1b6', '/.git/objects/03/f8520645287e09c8ad96bea9bcb878a9022206', '/.git/objects/03/ff6a156c8ba598cf1be27fb2371810888a927a', '/.git/objects/04/099990dadacd5c2f9cac501abf5448595db03f', '/.git/objects/04/0be927181b9604d69593ffe36ab7303b1a94bc', '/.git/objects/04/0e0ff5a310da50070b4caaa390e93cc8c45ee2', '/.git/objects/04/29762b630e33054c1f093d314dbc1558dffa89', '/.git/objects/04/29ceebd0dfc380db49c94ca9da53cf3d0c76c1', '/.git/objects/04/2e02d97cc4abc6a96b55d97f34fc76924c9cf9', '/.git/objects/04/378a998f4a8686eb28f62e8833b0f539229714', '/.git/objects/04/3f51145222bf3b3e811ab6d29c229b25b3b1d3', '/.git/objects/04/42d29efa0ea05d53ea9a8c2b6f9d4d76a65123', '/.git/objects/04/4e235175ddef6dd6b9a05edbd34b9ab69cbbd3', '/.git/objects/04/4ea84e87f27f536235093b99f1e70ff6b0d79a', '/.git/objects/04/5a95c2c2c83fbdc5489e26541666beca91b0c7', '/.git/objects/04/602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/objects/04/6ec8df046968b6bd4058a151de39c720533f28', '/.git/objects/04/74599cf24230b2e6acf617ed53f19eaac1d8b9', '/.git/objects/04/754e0dd161f613e2726da459e85cfbfc1edd59', '/.git/objects/04/771a2ae371a6d614730f8a857a8b401fa5049d', '/.git/objects/04/78eb80cc9a8041214bf273295064af3ab7f7d7', '/.git/objects/04/7fd372aaadd7a538f968712fdbd0e0e9c86415', '/.git/objects/04/80586953887e797aaabcce4f0226ecccea02bd', '/.git/objects/04/8703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/objects/04/88481d528674a76807703e6625d6284ca8293e', '/.git/objects/04/89842c6d2c5ddbc9550902039e9b25701d08db', '/.git/objects/04/8f509ce5eadba0a89792ec7f9a5691cecb00b5', '/.git/objects/04/921744c623863c7465f82f0d1af98ebc5ecffa', '/.git/objects/04/99e3e328e479da772baf0797e2fa34d5146993', '/.git/objects/04/9cf58812f1ec14cd7c43edc82532b64bab5b4c', '/.git/objects/04/ba7faa5aee31cca7feb4058574f06ec3a9b645', '/.git/objects/04/bf8e699f88900a6960b666079dba19a77ee7eb', '/.git/objects/04/d557d3b8c74f15dc8b1039d196b50cb8924950', '/.git/objects/04/eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/objects/04/fc92e910c95c87a567fba0d8e4566649816c3f', '/.git/objects/05/04a514448e0c3c3e4f771ffc84479295824920', '/.git/objects/05/09e635b91d457d88001ca19f7deb59d571fc46', '/.git/objects/05/0b372c851b0ea84569f8654c65fbc6c371b718', '/.git/objects/05/0b84f0c04495d82204b41f3442a74cc6a1c071', '/.git/objects/05/16754f01d0be542a9cfc9c1543fc07b1724272', '/.git/objects/05/429119c92c1ee2c4044621244195ae8bc33e03', '/.git/objects/05/58ff9439de64e491ee9c3bd2097b5b118029b6', '/.git/objects/05/6e214d9916a67615b4d789712bca658fa03435', '/.git/objects/05/7e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/objects/05/829e3696de2908b0d40f37f6c20fa8fff8a1c2', '/.git/objects/05/82cd30dd9e7c52791e8f1cefab0bf33f600dc6', '/.git/objects/05/880b7872ddc08ae82b821f1b3abd5c3e5341a3', '/.git/objects/05/91ddc9768f4c685c5053ca3185eb6a633a3717', '/.git/objects/05/a402c383746da97299cc12b9c33d5a2274fcd1', '/.git/objects/05/ae7f245bb7130dc464d00b710cce251cb7bc91', '/.git/objects/05/bc40edd4cc79dbed5bfe63bd8e89ac3473040e', '/.git/objects/05/c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/objects/05/dcaaad2921ef5e63bdab6f62ab24662b8634bb', '/.git/objects/05/e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/objects/06/0b348f7160e9612f996a74560ee786364ec5fe', '/.git/objects/06/121995b0950d829e4f685adf8bef846269580f', '/.git/objects/06/17f381a59a452478a8f34cabb652beadf361cd', '/.git/objects/06/1c9d02a136ba7adc607ed7074cd148595a2030', '/.git/objects/06/2a4e7b25731d2674574bbd21c7931dcc0a5baa', '/.git/objects/06/2ba3dc08a841ecebcec4c5c7c0efa5068edf7e', '/.git/objects/06/31461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/objects/06/3554b9d4f0504b72bcaf1ed91888688b8df1bc', '/.git/objects/06/3b0eb2461a6c575fabd0087334058e3e7d387d', '/.git/objects/06/418747a855c7847e27bfe23508610c20a60493', '/.git/objects/06/440e122972eb6c98407112d4abcd39c31e9321', '/.git/objects/06/4b36eebdc18055d9b9efab453b240dfd5f9421', '/.git/objects/06/4d3ab3dae901a7e93f7ab74c73b3fe334dc151', '/.git/objects/06/4efa3154548faf37f72f6e16da0f94681fa86a', '/.git/objects/06/79676e67109edbe58db2ca2e345cc2b73ceb03', '/.git/objects/06/839a7dad1e830ff2ba4cc5228781681333e75b', '/.git/objects/06/a8e8ac333fed73af47212fe4626cbaa3b74e82', '/.git/objects/06/b4fa32525254b94d62c83a59084454f8f705fb', '/.git/objects/06/c43ec225095ee1df544729b8b8fec79c0fea0d', '/.git/objects/07/01a09ce6bf7c6c4f6224a7842d756b53a2a88c', '/.git/objects/07/1acfc4227f2b22c838b0a56a59509105e4c2df', '/.git/objects/07/2872ca40aa53c5fcb11aa9a7edd5041033fa64', '/.git/objects/07/2de9a5fdb1ef44cd0b059e266bcf024ebf4697', '/.git/objects/07/358e5fb83f8aa10e322bdff64aa40398232a59', '/.git/objects/07/4930d053a799cc4f9095e89196437f704205d6', '/.git/objects/07/50d849bd563021aa1b9de4dc745fa43bc77e6e', '/.git/objects/07/522cfeed14b2118b137544acb215fd0d23a276', '/.git/objects/07/668e6b5dbd6277a6a85728db272e0b820a459e', '/.git/objects/07/682e77b603150eac6f657df236ac3dced0586d', '/.git/objects/07/7efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/objects/07/8adb64a12dcb95981db04caf7568546f5a88b6', '/.git/objects/07/91e2c492831faaf144a90e6af25adaabad38fa', '/.git/objects/07/997cbc1661d4546af788172b66486e4dbaefdf', '/.git/objects/07/c5d56f1363e06e73172965496ce16246dce1f2', '/.git/objects/07/ce7e8216ecdc557e1f1ec524242dd409b4067c', '/.git/objects/07/d0f29a2d244a75911191faf176cc0c7edf4bda', '/.git/objects/07/d150470e12425cb0b2d6a1cd55cd35ff2ff2fb', '/.git/objects/07/d79d89a08562d80d6890844f66241e32b443ba', '/.git/objects/07/d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/objects/07/ebcf391bfe46a07fd685402467db2e86ed4e0d', '/.git/objects/07/fa40d49088bd7d8511abca903641e6ad199f20', '/.git/objects/07/fb0409a65ce96873f20fbecc016dc5ee8d9d0f', '/.git/objects/07/fcb01a9b6e469e5b52f9ac3ab3bbe83a63d95f', '/.git/objects/08/0554e8ddc2a1a87275a26e5457e1b2a6046657', '/.git/objects/08/080c1aef87cedbe163497ddad8cc3005a73f7d', '/.git/objects/08/1eef64297df0ea2e464cf48c1520acd132cbd5', '/.git/objects/08/2169d84ac7751152d7134fa37292c00ba029d0', '/.git/objects/08/28873634fdb24f4318a443877f6106b5ff213e', '/.git/objects/08/377760400a919e539db754b0b66ea7ce0cef58', '/.git/objects/08/3a576c7606386c1daaca88824c281693d0ef0f', '/.git/objects/08/42d15769f312e00dbce38c79a209d783d115ea', '/.git/objects/08/46bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/objects/08/4d44439e48fbd75cbc5ae0b0132693e7d839b8', '/.git/objects/08/6f557632720c84a78f3d5389fe19e2f1a94791', '/.git/objects/08/749be2799a1a1f0697ed2571a4682426ea12ff', '/.git/objects/08/7809de3bad36c3f85c48e62edb51c147e48b77', '/.git/objects/08/7d31d51dfb5a1137d4f25be244cc284a37a076', '/.git/objects/08/9cb3c61a7acbf2a05ce9d4926088affe4663a1', '/.git/objects/08/ba0a8ee50af5b8ff5eb0a82d30bb5229fe2e86', '/.git/objects/08/cd05987a9baa7c8e5f6caa20e79a8a63d3d0d4', '/.git/objects/08/d2a116f15f569082d9e41973dd7e570d5b17d0', '/.git/objects/08/dec4893dc318d55b9f67e5c489081528a17a93', '/.git/objects/08/f07511d3e089cb96e804567644ce5381392e51', '/.git/objects/08/feb11d7a524e0e04e556a3b0fac0a6a7b24657', '/.git/objects/09/04682cc174ebeaaf2e9f366af211a401fbbd99', '/.git/objects/09/0826b708d0c9dcaddbfe121559c5b1486529f8', '/.git/objects/09/1739e89e6bfb98fd5f431dcd801487dba344cd', '/.git/objects/09/25e45208545d1857f69551356dcb6ec82edda1', '/.git/objects/09/2a3dcb3669da7adc41965ed57e1fe8cb86f429', '/.git/objects/09/384094c714fa3c73aeab22ac4fd18d06e8dbf8', '/.git/objects/09/3d21dba99b105a0e82051ab2639b5151325793', '/.git/objects/09/45bee1723c5de6847e799c08785083db839a6c', '/.git/objects/09/46862f3f15d72c8b71d2af4522b4921f6cab96', '/.git/objects/09/4ded1d397e3e5a80c619217287287fb729622c', '/.git/objects/09/4e04d13c87f5a327a7f44ffedc0ce41d9214d0', '/.git/objects/09/6bea492cbfb9768d845115c7a6a4d079f034a1', '/.git/objects/09/8b34de8f71069fae9082ecd1903b6faedce4e6', '/.git/objects/09/916958db8eaa97c465c9bec51a3d1a29863ab8', '/.git/objects/09/b3cd47a8afc2c0c4de3af709b99566a5bf6f37', '/.git/objects/09/d354f2506d543f99742b506f1c5e20b41d2691', '/.git/objects/09/dc1f89767f23768719cb5094eff75ce635e0f2', '/.git/objects/09/fcb1fee7452e61ee700d2679429371977f92d3', '/.git/objects/09/fdf0167d154d7e4538373b8df76e056ef8b1af', '/.git/objects/0a/05a2808a79fe98d007bccb3b1060551300dec8', '/.git/objects/0a/0c8795605b604d1e687339be45eb17e8812bb5', '/.git/objects/0a/2311bad25eea12e3670b5f0c36155e5890d27e', '/.git/objects/0a/32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/objects/0a/401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/objects/0a/56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/objects/0a/597e37cfb13fe9af1875fc0606d2f7cc0e7ada', '/.git/objects/0a/59bca84a5ae11bd02571a6bf55d97bbeeda3d6', '/.git/objects/0a/5abee36b52e3cd5aff769a0108ab1a3ca51a82', '/.git/objects/0a/613832d0a99485a26bdc2a2a347669c76d3ef1', '/.git/objects/0a/8b1aeacb86cb7efa0c8582e6f109cd1ba8c46a', '/.git/objects/0a/962ce910aa746587b34755922bae542449fba9', '/.git/objects/0a/9c45c7913ebf7c65a190c9b4623116c5083db1', '/.git/objects/0a/a39c684754ee62dfc0ef9866f409e95d192bb7', '/.git/objects/0a/a4f3386b7abde99d77a8a42c0e0c9a6e0c4514', '/.git/objects/0a/bc810e4c97279e80fa5610d8d2838b94e3bb03', '/.git/objects/0a/c6e9b1d42c10b456adb801699291acf3e7a7f8', '/.git/objects/0a/cc9185dc5580459d7b19eaf9bc4561109d5cbb', '/.git/objects/0a/cdf25eb887c3e132a436a866bcecd8a7a83e56', '/.git/objects/0a/d395ba510ce17075f27e7d6f4920547464887a', '/.git/objects/0a/e25708036bf7db64f0327ea004917ad42ea679', '/.git/objects/0a/f7b1d6071a1948ae9d76d28fbb7c496bea8020', '/.git/objects/0b/32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/objects/0b/3664959c7d794a1e8758860565e6c252546143', '/.git/objects/0b/4829e05344126422455e538c3f872330bac02b', '/.git/objects/0b/4ba29f97f87d85705e1dbacdbd901e825ab2a4', '/.git/objects/0b/5c093d67b5443b9efe596880b950fe478e93c9', '/.git/objects/0b/5d3ac18d6fbd99afb581479554b58fc4183e02', '/.git/objects/0b/5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/objects/0b/735cb54163379d90cea83320d93157240b00bb', '/.git/objects/0b/94a8d00ef25b126437e3b831d3c47331ec09ef', '/.git/objects/0b/9c1ff14d0729b8ca054bf3b70a31ed6ea3724f', '/.git/objects/0b/aa622887f5563517e122f9b16213710af9e5cb', '/.git/objects/0b/bcef51f80d0155f83a276423028a01a50cd92e', '/.git/objects/0b/be894f6158df6217aac34e5062d723091507dd', '/.git/objects/0b/c26acc5a1d060a7a7085eab6ce811422715108', '/.git/objects/0b/c5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/objects/0b/d9338bbd511117b1f70cc1e59c6bd691580e94', '/.git/objects/0b/dd4f1e5c19bd4b4c56e20da562449970b54134', '/.git/objects/0b/ebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/objects/0b/eeb928e68e50f79b601ffeb2721e89a635ed95', '/.git/objects/0b/f720f21f41ce829add4aab5a9a05012208c3f7', '/.git/objects/0b/fb909231e10a90dcfd4ca08fc34ad154b9686a', '/.git/objects/0c/00cb9ca737f2be5b9cff166bcef532262ec699', '/.git/objects/0c/03f3f202ea13e8d79942013dd4334cc5e7ebea', '/.git/objects/0c/0bdbfa2459da2f07c4ab0c874834200ff6278e', '/.git/objects/0c/3e4d5d6ea3196693b9472f7d8b823513fa235a', '/.git/objects/0c/4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/objects/0c/60a48fe702d1f4eb0d7dc24a73a35b850c8eb1', '/.git/objects/0c/614b8e0f3afd25e895d9491c2a30e5913af606', '/.git/objects/0c/6358b6057a1b224be62ad80a00d87614631b60', '/.git/objects/0c/63913c8162a44efd3e5ce01fdd7fe5c3875f45', '/.git/objects/0c/64a4d48bda41945b4888b51a9e960d8fbfcf0f', '/.git/objects/0c/81eca4c8d2b7bf0a503cdacdfdc66ed1715c2a', '/.git/objects/0c/973feb4df661c4fbc19f236f825bffeb3df257', '/.git/objects/0c/9d4a1d27f542f5c5fdf5684e73c718676e06a7', '/.git/objects/0c/a878bc7c1f09046bb15719383794b9ecba57f8', '/.git/objects/0c/b3be9041c3eaf49139e8d49ef95f361352c397', '/.git/objects/0c/c5b534f4425eeb8b3f6bb9a32803cb055d7ff3', '/.git/objects/0c/c625939a9cc324e29d3b2de079d11735728b58', '/.git/objects/0c/d0ce18b1d6a46a554b87e2dc0bd115429eb484', '/.git/objects/0c/d26a469771b69762f53b5ae2a322bf170091d1', '/.git/objects/0c/e0b926ac0c36b6e353c377ebc74e59bc0561c0', '/.git/objects/0c/e65ae661206b963a23be69dbcc77c2bfdba45a', '/.git/objects/0c/f07378ed3afd105c193d8b1b209dfec5785402', '/.git/objects/0c/f6c89b58f55c9aaff91eca9869cd2c17c0a47f', '/.git/objects/0c/fed93b45cb80e866637f3e266fde5459ea49fb', '/.git/objects/0d/15ae1524fab34c31c9c1ed0bb3e65a55951524', '/.git/objects/0d/195c3ade96d5880482daa65889a072069468be', '/.git/objects/0d/2b4e5c9def6a898a4064dd6adf23d978807b49', '/.git/objects/0d/315a864dbeb1ff8b62f267f614e3fb239b3518', '/.git/objects/0d/354cd6d3e0fa3aedf54d9b9eeabec3593aedc9', '/.git/objects/0d/3b08adf9c7ed270b6d5889540ad4437d5f0b98', '/.git/objects/0d/453df5063969c6130eb9ab5f086b45b2321f9f', '/.git/objects/0d/5256345daf7cbdefa3bc826d1e64513a214cf8', '/.git/objects/0d/5d4ed9115a075bdb83c3da8e5d5d95bfebf06a', '/.git/objects/0d/72d0b2349a404cc4cddb87c836194765377d74', '/.git/objects/0d/753acfba917272cd72f418e9c1352ed20054f6', '/.git/objects/0d/85d92161c5e9da30deaa248e028278f143e5b9', '/.git/objects/0d/8780f3e4c97dc70ba82cc61c5cef46d57b0b33', '/.git/objects/0d/8883bb012284d6c3c617deaf7758946852971f', '/.git/objects/0d/97da9f70aa97244bea12a6d8024c006575e5c8', '/.git/objects/0d/bcae139c196ceada45a4720daaf5908702ecc7', '/.git/objects/0d/c7d460490f110521abbce48d8939e546425dc5', '/.git/objects/0d/d1ac693951729e6c496cb1a42a310eb0cdad93', '/.git/objects/0d/d9afc1c58e48f8e6e7af3414041106af38ff05', '/.git/objects/0d/db7f9b502bca441642e7d54c6c212f0b6673ff', '/.git/objects/0e/0761bb314058c32679440d8686420159c31db0', '/.git/objects/0e/189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/objects/0e/19651c4d48fa439f5123ab04cd94245f216743', '/.git/objects/0e/31d5d75617658d5871f0af7cd6e2572f65d5a7', '/.git/objects/0e/33d9681c3f231054d16d613b34097e7e8b59e7', '/.git/objects/0e/5f82aa92d0553cc9b4fd2cb4dbd2739e2ee8f0', '/.git/objects/0e/7262601e46c40b320da44a929f151c2c114032', '/.git/objects/0e/abd83d251910f3dbe9afcb67d962c186a2ca8c', '/.git/objects/0e/b37de8ca5ba7a34797b3355f41cf01b22ff008', '/.git/objects/0e/be1fc27f8d238046aea951e6caa693563a5db1', '/.git/objects/0e/f556b4beacab982c37a6ba626b68c12a03a3ae', '/.git/objects/0e/fcc5d9fbd21558e1d5c24872e4a1bfab7f3685', '/.git/objects/0f/0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/objects/0f/138f0796a06e405b352d9b196d634fe03272bd', '/.git/objects/0f/17f23b4277ae965b175409f9ef0ca8fe5faca8', '/.git/objects/0f/272f7f62bbef400af52029018e0b40f2e84d63', '/.git/objects/0f/2c1f18c6195cd349bfc1bcf75c63a4676aa178', '/.git/objects/0f/375603ef57e02e9fb0b574a426b1efba49d8e8', '/.git/objects/0f/3a6ec84962b576c06d6f3836465b86e5b3f10e', '/.git/objects/0f/3f373dbe68457e2f332b53419313c5297f50fa', '/.git/objects/0f/54a10edafd4f6d7e03edbb6dc48a45c44aad67', '/.git/objects/0f/56092d56b18c5734f3dd8b63ea6ce5355e0e36', '/.git/objects/0f/573afb56cf5cd6dd86621f5e5c4d7eeff7c726', '/.git/objects/0f/5968785d1283804001ca49ccf77d63eac98e02', '/.git/objects/0f/6c72d33101537f80a5c00d3919b4759f4364cf', '/.git/objects/0f/7e32dc222c7d9c81f5f3e241496ba69be2baad', '/.git/objects/0f/86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/objects/0f/904c72f18187d5c05f93cb546a711f8c3a9f02', '/.git/objects/0f/9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/objects/0f/a19e3e148a3e82579b6e266e89dc11d898930c', '/.git/objects/0f/b3ec07ae5333277f64ed812af5f0f22e48fb1f', '/.git/objects/0f/ebdd5aed4ccb535776cb3ecf5f7292598d83cf', '/.git/objects/0f/f56f42c9ecca878a4c0e2e836e52a449662082', '/.git/objects/10/18a2334d5c1968f40c2f478fb1f2867e67b8b5', '/.git/objects/10/261e06f4cf6f32be1271762e4e2656d3227141', '/.git/objects/10/36c4359913cb364e8129ef0b26eb5dec343083', '/.git/objects/10/565c0176f2173424386bbc1502cb879a9dce9e', '/.git/objects/10/5a4c0156c9645530e6e2b046d9fdfb72c075e0', '/.git/objects/10/64453d1e30d78cd388f816b907f7b742375e31', '/.git/objects/10/7c2333f5bcbcad6ce31755c9b4b4c72e960d28', '/.git/objects/10/8486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/objects/10/8d20d49b8c9df755feb7040b27dd500650d6f1', '/.git/objects/10/9488d1db9f25b656ca5a4eed3b42ca6c3bd9f0', '/.git/objects/10/9674e0533514d7be518ce93f1318966acdaffa', '/.git/objects/10/97e656055bf30481bf2c943278f0eecb5b5d8e', '/.git/objects/10/ac366f495ba690682ed41a0ddb0004802f5ee2', '/.git/objects/10/ae7490a1f6894c54b727bd84a05889b1db8ffc', '/.git/objects/10/b37de565a520d0c743bf3d148cffdb597a14df', '/.git/objects/10/b4f635a80dd5742205f90e9a48383eb5a45dac', '/.git/objects/10/b5e2bbd4086ddc791db7fc3a786213e5107286', '/.git/objects/10/b839896461248c56e80d5915ed1ec52914b2d9', '/.git/objects/10/c0ec718241239bc7cf5ca80f26cb03180e8d7c', '/.git/objects/10/c8846d5380b664959d63759591c3a6f604540a', '/.git/objects/10/cc3dd9ffce62367bfd3e274024a84fa4bbf4fc', '/.git/objects/10/e1a2f389c4804375ce951f98069ea0e864c3f6', '/.git/objects/10/e40fb159305494893b1e94e62c18dc14acec9a', '/.git/objects/10/e5e5a2fb3b0739fa07632f8bacc69cd115ba17', '/.git/objects/11/073d080b9f772afb962eaa10e3583a841100fd', '/.git/objects/11/0a03a57b065c62b17946ce2f9c27ae14cd09e9', '/.git/objects/11/52abac92eac8d8b605f61e7608e5151d222f07', '/.git/objects/11/562ae195fafe5127b0a1577159048b0af6fbc4', '/.git/objects/11/6084d6edde5547795dd38c98bb045777a4105f', '/.git/objects/11/671344533a154f203e9bbcff2201bc5befae76', '/.git/objects/11/68066a747c3bef2d6e633b2347c20cc6b56404', '/.git/objects/11/6968b47e00996915b67531127f0954c7ddd1a4', '/.git/objects/11/7f881842de701288d44a04738aeddf2eb62771', '/.git/objects/11/848596c43002718041db85d44d4f17fef2fd2d', '/.git/objects/11/a8a92beabf4c3b84689c4b3815e4c19b948151', '/.git/objects/11/b6a93338766923a8e6379405e6fcf4ab828169', '/.git/objects/11/c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/objects/11/e01dd8395bcb4499bbae87a8fa5d396b5bb9a0', '/.git/objects/11/e234b29ee21a975610c871bc3aca80ba403997', '/.git/objects/11/e65f017f9956f02db9d750e814db9c0eb996f6', '/.git/objects/11/f3df8ac49a0be182d46132407e50090bc85a7e', '/.git/objects/12/1b52d4dde57209a1c5d7fad41433f9d7507e7e', '/.git/objects/12/3bbafac5135532670900b0daeade243b64415e', '/.git/objects/12/46c37c3be32064b636700c62bc59120a41a208', '/.git/objects/12/482204acdc7b5906f6985edd7052cf24e81715', '/.git/objects/12/60fee99a4cfcbd9d4ffb0eb2de091a7a472b7b', '/.git/objects/12/782408d18b12ea7c1fd9e5d39ddbfa2040ef21', '/.git/objects/12/8150674170b66350257cc719da038a61a568bf', '/.git/objects/12/8991f222be89980a285c1a719170f19cebd863', '/.git/objects/12/a298fd576dee88bdd1d5b4f72dedf5ebe264d9', '/.git/objects/12/bac80bceda99fedc73290309b748399405be41', '/.git/objects/12/d12afbdb51a82ea91470a68c5936ef307758b3', '/.git/objects/12/db0c6cc3d0ec7d7834be73cbded60279418c53', '/.git/objects/12/ecf89d4939f447a2a13eb6a8584268d822df06', '/.git/objects/12/f27c213102a0ac8c26ec5d35886d36e011d04c', '/.git/objects/13/0454723003170e9f3e6ed225d66f809f6b6dad', '/.git/objects/13/049a15f6a54c096b02c7573999db421178a726', '/.git/objects/13/0b070345feb323ae3fde1c7d932945f3191106', '/.git/objects/13/2b510d6d7bcd743b4cbf1ea79259bf32a0098f', '/.git/objects/13/2c537172da3f2875b3ce54f4b1f5af4cd1eb1f', '/.git/objects/13/31cd4e5b63c9aa3bfc3c37f80674cc03c74071', '/.git/objects/13/360394a41c8fabc39419ab404191a8575e2799', '/.git/objects/13/3c2a7f8f0c8e8798adb0c95502b796e8304aa0', '/.git/objects/13/53a7a4fc4f5419b52d1dc280f7536194c60122', '/.git/objects/13/92a68ba7c0702c66b4fb266ffd087081b1e141', '/.git/objects/13/afea111e981b60139f5b4ac6b833043651c7b4', '/.git/objects/13/c40173739fb7e84b979f3c6ac5261cec02e012', '/.git/objects/13/d4e7409000e6a4b0bf0196e7c4db9005e68a3a', '/.git/objects/13/dd0ea3ac7cf3fa815ff54ed379ac145c2200aa', '/.git/objects/13/e514857a46401864fca0265d1d7e83a40fc30c', '/.git/objects/13/fb8a33b9d96c2a9ff445c20dea718e895df5e4', '/.git/objects/13/fc3c0fa0f80a29ecc8c44e234a0e433e5e20db', '/.git/objects/14/1292c88425a51c07a6093b433d9954224e31b4', '/.git/objects/14/1b7a38a5eb915f5b73a167f77208e4d2286b00', '/.git/objects/14/28bfd5a05e95735a945cf34906ebf3948fa13a', '/.git/objects/14/3334e584ff71080c606f29c1ef42924bbe453d', '/.git/objects/14/394b47e18f572003e3d82368702dfd474b70c4', '/.git/objects/14/3df4c79cc8ee0249f8509549e5377882a28010', '/.git/objects/14/740e00ca060ea5ea55d359d8e94b78c9b27bad', '/.git/objects/14/74c8f7cf8bc22cda503322795cac94ac621675', '/.git/objects/14/818693e025769bce36db9ab228de95282c660c', '/.git/objects/14/8a5ec5787afd3f553071ecc831a805312f6ece', '/.git/objects/14/8c20fa8c56ae81068aded6b9a8f2a59fc229dd', '/.git/objects/14/9215c98341f0291662bea80be4491d80cce454', '/.git/objects/14/93fb5b0b0a7a8c28aa2e0e11e3024fdd6605a4', '/.git/objects/14/a51ee6f2160b21205c9afd9f7cc99748092bde', '/.git/objects/14/a5b829f9591df4d9d656268f7ad309be05e97f', '/.git/objects/14/b14cb4896fb71ae400bad91fd17aca2dc37cdd', '/.git/objects/14/c258aa37b196e7602622c9d90721c7cdfc96e5', '/.git/objects/14/c2a807581505e916cb62d8d2195af8a6c9fe9b', '/.git/objects/14/dcb371d5f4cc65cc76297ddc5125507b9752fc', '/.git/objects/14/e09849fda36affbc8abb417ca8b46778461bc7', '/.git/objects/14/e4ef69520a217c61e1dfd2f8b23fab0b8f65dc', '/.git/objects/14/ee55bfeb961e36bd64cb902cc11ff3a907a4ba', '/.git/objects/14/f842403e89680c08c9e914aa7da06da74192d5', '/.git/objects/14/fe9bb6670802ae36d1022630b687088b71c35d', '/.git/objects/15/098da0ba5b0e2d399d8688a8a0b6a0fcd68d1d', '/.git/objects/15/3e02e9a9c73af7f51d590516702350390c0c12', '/.git/objects/15/5f8df967724158d80873e629c6c12bb65c8d00', '/.git/objects/15/6916239719ce4eaa5eb0e4105e9537ccd5734c', '/.git/objects/15/6d79f56790f38a4c9d716aa1e76e0d9eaa5ee3', '/.git/objects/15/709f6e54c6706e2d1debd66e87ab969ed3cb3b', '/.git/objects/15/80c27de69b78994d59b6f22fa0e0da62c8705f', '/.git/objects/15/934046b41baa7c1df153b1fa8b4f7b45d6d363', '/.git/objects/15/9a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/objects/15/9bfd26b659195df8c8486d12b5e15f948cb808', '/.git/objects/15/bcd112607d47deea3216fc8137482fd0a57dfd', '/.git/objects/15/be2e474eb938a89e4d7c19737994893197e781', '/.git/objects/15/fc480833c1c814d413e14a2421b5ffed74028f', '/.git/objects/15/fd3d807851be39f668587b875d1bd9356e1171', '/.git/objects/15/ff558cf9cbc3541c227c019c1ff2b0afc0e4c8', '/.git/objects/16/22c65984231f8952831bb55b298781f51ed32a', '/.git/objects/16/27053cd99034a3907e840eaef7a0cb08f20e6e', '/.git/objects/16/282c3c9e7f94259ee473e3b448a4bf153f7faf', '/.git/objects/16/3d050dd4db671d29be7efff1a35864f91ca61d', '/.git/objects/16/45e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/objects/16/4b7fafb2c4bcbb6315f95870ae3efbf8a82241', '/.git/objects/16/50783e350f6307c3535eb8300baa648a123c58', '/.git/objects/16/5d22d6f5554de58d1281ade7295158d4e62312', '/.git/objects/16/6de2e7604a6a403e37c7580a2396b1c77703a9', '/.git/objects/16/7230ee6e97a40999b7b1b46b089e48951a1158', '/.git/objects/16/83c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/objects/16/9b7c3ac237ddbfd037e96566cae9579871112a', '/.git/objects/16/a2cab9c4e32851d2754116ca26b4ead49cd1a3', '/.git/objects/16/a6b6c10cf2c147d781304dcd12f19322706a4f', '/.git/objects/16/bc644bbb95c0d296bea492b5595b361a93b9fa', '/.git/objects/16/d1e49e991257dccbb3cf2869412da65640aa07', '/.git/objects/16/d466f5d6f6422fc565801d9d97c0bd71bf6a5a', '/.git/objects/16/de7d0bc43866f4573019d564ac08d4f8eea2f0', '... [results truncated, try being more specific with your parameters]']
AI: Let me look at the actual project structure more carefully, focusing on the inputs and working directories.[{'name': 'ls', 'args': {'path': '/inputs'}, 'id': 'call_00_rbSRy5lM5cAypGDwz7vq7600', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs'}, 'id': 'call_01_0atbRUemRWKC7RHfxVos6950', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_02_77QzQLGb2rnQ0sDjyz4e3621', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/skills/acquiring-discrepancy-analysis'}, 'id': 'call_03_sBeaG6NIk3QS8ksUykgz1752', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/outputs/working/']
Tool: ['/outputs/working/build_clause_index.py', '/outputs/working/build_legal_propositions.py', '/outputs/working/clause_index.json', '/outputs/working/contract_batch_01.json', '/outputs/working/contract_batch_02.json', '/outputs/working/contract_product_profile.json', '/outputs/working/legal_propositions.json', '/outputs/working/matrix_batch_01.json', '/outputs/working/matrix_batch_02.json', '/outputs/working/matrix_batch_03.json', '/outputs/working/matrix_batch_04.json', '/outputs/working/source_preflight.json']
Tool: ['/skills/acquiring-discrepancy-analysis/SKILL.md', '/skills/acquiring-discrepancy-analysis/references/', '/skills/acquiring-discrepancy-analysis/scripts/']
AI: Good. Let me now read the reference files, the existing working artifacts, and understand the scope. The task is "Contract coverage batch 2 (ids 5.3.18.2 to end)". Let me first understand what's already been done.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 1000}, 'id': 'call_00_uzQMPnIatvkiCf8mGxJo5269', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 1000}, 'id': 'call_01_kiMe0uxJtOrt3q2XuiYZ0700', 'type': 'tool_call'}]
Tool:      1	# Output Contract
     2	
     3	Write two final artifacts:
     4	
     5	- `/outputs/discrepancy_analysis.json`
     6	- `/outputs/discrepancy_analysis.xlsx`
     7	
     8	The JSON is the source of truth. The XLSX is a presentation generated from the
     9	JSON.
    10	
    11	## Final JSON Shape
    12	
    13	```json
    14	{
    15	  "analysis_profile": {
    16	    "contract_product_profile": {
    17	      "product": ["<selected product/channel>"],
    18	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
    19	      "terminal": ["<selected terminal/payment device>"],
    20	      "payment_method": ["<selected payment method>"],
    21	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
    22	    },
    23	    "source_preflight": {
    24	      "contract_numbering_valid": true,
    25	      "notes": []
    26	    }
    27	  },
    28	  "links": [
    29	    {
    30	      "matrix_ids": ["<matrix id>"],
    31	      "contract_ids": ["<contract locator>"],
    32	      "relationship": "aligned|deviation",
    33	      "legal_topic": "<short legal topic>",
    34	      "matrix_standard": "<bank standard requirement group>",
    35	      "contract_position": "<counterparty contract position group>",
    36	      "status_reason": "<group-level reason>",
    37	      "risk_level": "none|low|medium|high",
    38	      "discrepancies": [
    39	        {
    40	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
    41	          "description": "<material difference>",
    42	          "risk": "<why this matters for the Bank>"
    43	        }
    44	      ]
    45	    }
    46	  ],
    47	  "atomic_links": [
    48	    {
    49	      "matrix_id": "<one matrix id>",
    50	      "contract_id": "<one contract locator>",
    51	      "relationship": "aligned|deviation",
    52	      "link_index": 0,
    53	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
    54	      "coverage": "<what this contract locator contributes to the group>"
    55	    }
    56	  ],
    57	  "unmatched_matrix": [
    58	    {
    59	      "matrix_id": "<matrix id>",
    60	      "requirement": "<missing bank standard requirement>",
    61	      "status": "missing_in_contract",
    62	      "required_type": "mandatory|optional|unknown",
    63	      "risk_level": "low|medium|high",
    64	      "risk": "<risk of omission>",
    65	      "rejected_candidates": [
    66	        {
    67	          "contract_id": "<weak candidate considered>",
    68	          "reason": "<why it is not a true analogue>"
    69	        }
    70	      ]
    71	    }
    72	  ],
    73	  "unmatched_contract": [
    74	    {
    75	      "contract_id": "<contract locator>",
    76	      "contract_position": "<extra legally significant contract term>",
    77	      "status": "extra_in_contract",
    78	      "risk_level": "low|medium|high",
    79	      "risk": "<risk or impact for the Bank>",
    80	      "materiality_reason": "<why this has independent legal effect>"
    81	    }
    82	  ],
    83	  "coverage_ledger": {
    84	    "matrix": [
    85	      {
    86	        "matrix_id": "<matrix id>",
    87	        "closure": "linked|missing_in_contract|not_evaluable",
    88	        "link_indices": [0],
    89	        "reason": "<short closure reason>"
    90	      }
    91	    ],
    92	    "contract": [
    93	      {
    94	        "contract_id": "<contract locator>",
    95	        "closure": "linked|extra_in_contract|not_material",
    96	        "link_indices": [0],
    97	        "reason": "<short closure reason>"
    98	      }
    99	    ]
   100	  },
   101	  "summary": {
   102	    "aligned_count": 0,
   103	    "deviation_count": 0,
   104	    "missing_in_contract_count": 0,
   105	    "extra_in_contract_count": 0
   106	  }
   107	}
   108	```
   109	
   110	## JSON Rules
   111	
   112	- `links` are group-level legal findings. One status applies to the full
   113	  many-to-many group.
   114	- `atomic_links` are traceability rows only. They inherit the group
   115	  `relationship`; do not invent pair-level final statuses.
   116	- `contract_ids` should contain clauses that provide material coverage for the
   117	  group. Background or locator/context clauses may be mentioned without being
   118	  final candidates when they do not change status.
   119	- If `status_reason`, `contract_position`, or `discrepancies` relies on a
   120	  contract clause as legal coverage, or uses it to cure a gap, the reasoning
   121	  must explain why that clause governs the same legal object, duty/right,
   122	  trigger, and consequence. A clause that merely contains a useful date, amount,
   123	  channel, or liability phrase cannot change status by itself.
   124	- `unmatched_contract` contains only legally significant `extra_in_contract`
   125	  rows. Do not include headings, definitions without operative effect,
   126	  signatures, requisites, or blank technical forms.
   127	- Non-material contract rows belong only in `coverage_ledger.contract` with
   128	  `closure = not_material`.
   129	- `missing_in_contract` may be high, medium, or low risk depending on matrix
   130	  mandatory/optional status and applicability.
   131	- `relationship = aligned` requires empty `discrepancies` and direct
   132	  text-grounded confirmation that the contract package preserves the matrix
   133	  legal result.
   134	- For deadlines and economic terms, compare the actual text values. Matrix
   135	  `3 working days` and contract `3 working days` can be `aligned`; matrix
   136	  `3 working days` and contract `5 working days` or no deadline is
   137	  `deviation`.
   138	- A hard term found in another contract clause counts only when that clause
   139	  expressly governs the same obligation or is explicitly incorporated by the
   140	  linked clause. Do not treat a deadline for a different request/procedure as
   141	  coverage for the matrix hard term.
   142	- Do not rely on extracted proposition fields alone for status. Use
   143	  `matrix_standard` and `contract_position` to show the relevant source-text
   144	  basis for the comparison.
   145	- `relationship = deviation` requires at least one discrepancy with `type`,
   146	  `description`, and `risk`.
   147	- All final ids must be visible in source files. Do not use corrected,
   148	  inferred, parenthetical, translated, or internal ids.
   149	- Weak candidates do not appear in final `links`; use
   150	  `unmatched_matrix[].rejected_candidates`.
   151	
   152	## Working Artifact Rules
   153	
   154	Before final comparison starts, working artifacts must pass these checks:
   155	
   156	- `/outputs/working/clause_index.json` contains every matrix id from
   157	  `inputs/matrix.json`.
   158	- A scoped/batch matrix subset is never saved as the canonical
   159	  `clause_index.json`; use a separate batch file.
   160	- Any optional proposition/evidence ledger preserves the source text needed for
   161	  comparison. Extracted fields may help navigation but are not authoritative.
   162	- Duplicate printed contract ids from appendices or forms keep source context
   163	  in working artifacts. Final reporting may use the printed id plus enough
   164	  context to identify the source row.
   165	
   166	## Excel Output
   167	
   168	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   169	
   170	Sheet 1: `Contract-Matrix`
   171	
   172	Columns:
   173	
   174	1. `contract_id`
   175	2. `contract_summary`
   176	3. `matrix_ids`
   177	4. `status`
   178	5. `risk_level`
   179	6. `comment`
   180	
   181	Rules:
   182	
   183	- one row per group-level contract-to-matrix finding;
   184	- `matrix_ids` contains the full matrix id set for the group;
   185	- status is `aligned`, `deviation`, or `extra_in_contract`;
   186	- contract-only extras have blank `matrix_ids`.
   187	
   188	Sheet 2: `Only in Matrix`
   189	
   190	Columns:
   191	
   192	1. `matrix_id`
   193	2. `requirement`
   194	3. `required_type`
   195	4. `risk_level`
   196	5. `comment`
   197	
   198	Rules:
   199	
   200	- one row per final `unmatched_matrix` item;
   201	- do not include non-evaluable headings or purely parent rows.
   202	
   203	## Bad Output Patterns
   204	
   205	Do not output:
   206	
   207	- multiple competing final JSON files;
   208	- only a matrix-side list without contract-only review;
   209	- pair-level final statuses as the primary answer;
   210	- `deviation` for unselected slash alternatives;
   211	- `deviation` for heading/title/label changes alone;
   212	- final `unmatched_contract` rows for definitions without legal effect;
   213	- final ids that exist only in helper scripts or inventories;
   214	- `extra_in_contract` with empty risk;
   215	- `aligned` with non-empty discrepancies;
   216	- `missing_in_contract` without rejected weak candidates when weak candidates
   217	  were considered.
Tool:      1	# Comparison Patterns
     2	
     3	These examples calibrate legal judgment. They are universal patterns, not
     4	answers for a specific contract.
     5	
     6	## 1. Option List Via Slash
     7	
     8	Matrix standard lists `card / QR / mobile pay / smart terminal`.
     9	
    10	Contract selects `card / QR` and the product profile shows only those services
    11	are in scope.
    12	
    13	Result: `aligned` for scope. Do not mark missing/deviation merely because
    14	unselected slash alternatives are absent.
    15	
    16	## 2. Mandatory Product Missing
    17	
    18	Matrix filter says the requirement is `common` or matches the contract product.
    19	The contract contains no analogue.
    20	
    21	Result: `missing_in_contract`, high risk when mandatory and no true analogue is
    22	found.
    23	
    24	## 3. Optional Product Missing
    25	
    26	Matrix item is optional or filtered to a product not selected by the contract.
    27	No true analogue is present.
    28	
    29	Result: `missing_in_contract`, low or conditional risk. Do not create a weak
    30	deviation link.
    31	
    32	## 4. Placeholder In Applicable Term
    33	
    34	Matrix requires a filled system name, fee, penalty, account, appendix, or
    35	deadline. Contract has a blank placeholder.
    36	
    37	Result: `deviation`, usually low risk unless the blank blocks performance or
    38	enforcement.
    39	
    40	## 5. One Contract Row Covers Many Matrix Requirements
    41	
    42	One contract clause imposes several duties: acceptance, payment mechanics,
    43	documents, and liability. Final reporting may list one contract row with many
    44	matrix analogues.
    45	
    46	Result: create one group with one `contract_id`, several `matrix_ids`, and one
    47	group-level status.
    48	
    49	## 6. One Matrix Requirement Covered By A Package
    50	
    51	Matrix standard requires a parent right, operative duty, deadline, amount, and
    52	consequence. Contract splits them across several clauses.
    53	
    54	Result: link all necessary contract locators in one group. `aligned` is allowed
    55	when the package preserves every material element.
    56	
    57	## 7. Parent/Framework Informative
    58	
    59	A parent clause creates the operative right and child clauses define amount or
    60	procedure.
    61	
    62	Result: include the parent if it has independent legal effect. Exclude a parent
    63	heading if it only names a section and all legal effect is in children.
    64	
    65	## 8. Weak Topic Match Rejected
    66	
    67	Matrix gives the Bank a specific right to deduct a fee after a defined trigger.
    68	Contract has only a general payment clause.
    69	
    70	Result: no final link. Put the matrix item in `unmatched_matrix` and record the
    71	payment clause as rejected weak context if useful.
    72	
    73	## 9. Same Word, Different Legal Object
    74	
    75	Matrix concerns Bank refusal to register a merchant outlet. Contract concerns
    76	customer refusal to accept delivered services.
    77	
    78	Result: no link. Same verb is not enough when legal object and protected party
    79	differ.
    80	
    81	## 10. Changed Deadline
    82	
    83	Matrix says notice or document delivery is due within 3 business days. Contract
    84	says 5 business days or omits the deadline.
    85	
    86	Result: `deviation`; discrepancy type `deadline`.
    87	
    88	## 11. Borrowed Deadline Does Not Cure Missing Specific Deadline
    89	
    90	Matrix requires a specific duty to be performed within 3 business days. The
    91	contract has the same duty but no deadline in that clause. Other clauses contain
    92	3-business-day deadlines for different requests or procedures, and the duty
    93	clause does not incorporate them.
    94	
    95	Result: `deviation`; the deadline is missing for that specific duty. A hard term
    96	can be supplied by another clause only when that clause expressly governs the
    97	same obligation or is explicitly incorporated.
    98	
    99	## 12. Coverage Relevance
   100	
   101	Matrix requires a specific Bank right with a deadline. Contract clause A has the
   102	same right but no deadline. Contract clause B contains the same number of days,
   103	but regulates a different request or procedure and is not incorporated into
   104	clause A.
   105	
   106	Result: clause B may be mentioned as background or rejected context, but it
   107	cannot make clause A `aligned`. A clause can provide coverage only when it
   108	governs the same legal object and duty/right, or is explicitly incorporated
   109	into that duty.
   110	
   111	## 13. Changed Amount, Formula, Cap, Or Penalty
   112	
   113	Matrix requires a fixed penalty, no cap, specific formula, or full damages.
   114	Contract lowers the penalty, caps it, changes the base, or requires a demand
   115	not present in the standard.
   116	
   117	Result: `deviation`; discrepancy type `amount` or `liability`.
   118	
   119	## 14. Party Inversion
   120	
   121	Matrix protects the Bank or imposes a duty on the merchant. Contract gives the
   122	right to the counterparty or shifts the duty to the Bank.
   123	
   124	Result: `deviation` or `extra_in_contract` depending on whether it is an
   125	analogue or a new counterparty right.
   126	
   127	## 15. Procurement Mechanism As Analogue
   128	
   129	Public-contract acceptance, EIS signing, budget payment, statutory penalties,
   130	or unilateral termination regulates the same legal object as the matrix.
   131	
   132	Result: link it. Use `aligned` if the Bank standard is preserved or stronger;
   133	use `deviation` if timing, acceptance, payment, remedy, or control changes.
   134	
   135	## 16. Procurement Mechanism As Extra
   136	
   137	Contract gives the customer an independent inspection, rejection, correction,
   138	withholding, reporting, or convenience termination right with no matrix
   139	analogue.
   140	
   141	Result: `extra_in_contract` with material risk.
   142	
   143	## 17. Mandatory Law Preserves Result
   144	
   145	The contract uses mandatory-law wording that gives the Bank the same or stronger
   146	right/protection than the matrix and does not narrow enforcement.
   147	
   148	Result: `aligned`. Do not mark deviation just because the mechanism is
   149	statutory.
   150	
   151	## 18. Formal Label Difference
   152	
   153	The same legal content appears under another appendix title, report label, or
   154	document name.
   155	
   156	Result: `aligned` if rights, duties, timing, evidence, and consequences are
   157	preserved.
   158	
   159	## 19. Named Channel Or Legal Force Missing
   160	
   161	Matrix requires a named EDI/email/site/channel and legal-force effect. Contract
   162	allows generic exchange but omits the named channel or evidence effect.
   163	
   164	Result: `deviation` only when it is the same document-exchange mechanism with a
   165	missing material element. Otherwise it is weak context and the matrix item is
   166	`missing_in_contract`.
   167	
   168	## 20. Generic QR/Terminal Capability
   169	
   170	Contract says a terminal can display QR or accept cards. Matrix requires a named
   171	Bank product or product-specific procedure.
   172	
   173	Result: apply the product profile first. If the product is selected and the
   174	procedure is missing, use `missing_in_contract` or `deviation`. If not selected,
   175	use low-risk missing/non-applicable.
   176	
   177	## 21. Definition Without Legal Effect
   178	
   179	Contract definition has no analogue in the matrix and creates no standalone
   180	right, duty, risk, amount, procedure, liability, or consequence.
   181	
   182	Result: non-evaluable in working ledger. Do not include it in final
   183	`unmatched_contract` for legal metrics.
   184	
   185	## 22. Definition With Legal Effect
   186	
   187	A definition expands a key term so that it changes scope, liability, covered
   188	transactions, parties, or remedies.
   189	
   190	Result: evaluable. Link it if it modifies a matrix analogue; otherwise classify
   191	as `extra_in_contract`.
   192	
   193	## 23. Contract-Only Material Clause
   194	
   195	Contract adds maximum price, budget source, customer control, acceptance,
   196	withholding, unilateral refusal, penalty cap, reporting, or anti-corruption
   197	procedure with no matrix analogue.
   198	
   199	Result: `extra_in_contract`.
   200	
   201	## 24. Duplicate Gap Propagation
   202	
   203	One payment deadline gap affects a payment package with parent and child
   204	clauses.
   205	
   206	Result: record one grouped `deviation`. Do not duplicate the same gap across
   207	unrelated companion clauses.
   208	
   209	## 25. Parent Row In Gold-Like Output
   210	
   211	A parent row is evaluable only when it states an operative rule. A parent row
   212	that merely names a section is not a legal metric item.
   213	
   214	Result: include operative parents; omit non-informative headings.
   215	
   216	## 26. Group-Level Status
   217	
   218	A group contains one contract id and several matrix ids. One status applies to
   219	the group as a whole.
   220	
   221	Result: do not assign separate final statuses per pair. `atomic_links` are only
   222	traceability rows and inherit the group relationship.
AI: Now let me look at the existing working artifacts to understand what's been done and what batch 2 scope is.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 100}, 'id': 'call_00_009uod5RUb6vXRelDCLk7308', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_01_IiCgKDLvWgSw0bXoOPeE6062', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 100}, 'id': 'call_02_d5jbhX9iaE7Iauo1rj3p1748', 'type': 'tool_call'}]
Tool:      1	{
     2	  "matrix_items": [
     3	    {
     4	      "source": "matrix",
     5	      "id": "2.1",
     6	      "type": "matrix_requirement",
     7	      "required_type": "mandatory",
     8	      "product_filter": "common",
     9	      "lot_filter": "common",
    10	      "terminal_filter": "common",
    11	      "payment_method_filter": "common",
    12	      "main_idea": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
    13	      "topics": [
    14	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    15	        "Банк может отказать в регистрации ТСТ без указания причины",
    16	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    17	        "Информация о новых устройствах предоставляется с указанием их количества"
    18	      ],
    19	      "enriched_text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соо"
    20	    },
    21	    {
    22	      "source": "matrix",
    23	      "id": "2.2",
    24	      "type": "matrix_requirement",
    25	      "required_type": "mandatory",
    26	      "product_filter": "common",
    27	      "lot_filter": "common",
    28	      "terminal_filter": "common",
    29	      "payment_method_filter": "common",
    30	      "main_idea": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    31	      "topics": [
    32	        "Расчёты производятся в рублях Российской Федерации"
    33	      ],
    34	      "enriched_text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. "
    35	    },
    36	    {
    37	      "source": "matrix",
    38	      "id": "2.3.1",
    39	      "type": "matrix_requirement",
    40	      "required_type": "mandatory",
    41	      "product_filter": "common",
    42	      "lot_filter": "common",
    43	      "terminal_filter": "common",
    44	      "payment_method_filter": "common",
    45	      "main_idea": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    46	      "topics": [
    47	        "Обмен информацией по электронной почте",
    48	        "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
    49	        "Информация и документы, направленные по электронной почте, имеют юридическую силу"
    50	      ],
    51	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информаци"
    52	    },
    53	    {
    54	      "source": "matrix",
    55	      "id": "2.3.2",
    56	      "type": "matrix_requirement",
    57	      "required_type": "mandatory",
    58	      "product_filter": "common",
    59	      "lot_filter": "common",
    60	      "terminal_filter": "common",
    61	      "payment_method_filter": "common",
    62	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    63	      "topics": [
    64	        "Обмен документами посредством системы ДБО или аналогичных систем Банка"
    65	      ],
    66	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;"
    67	    },
    68	    {
    69	      "source": "matrix",
    70	      "id": "2.3.3",
    71	      "type": "matrix_requirement",
    72	      "required_type": "optional",
    73	      "product_filter": "common",
    74	      "lot_filter": "common",
    75	      "terminal_filter": "common",
    76	      "payment_method_filter": "common",
    77	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    78	      "topics": [
    79	        "Обмен документами с доставкой нарочным или курьером"
    80	      ],
    81	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
    82	    },
    83	    {
    84	      "source": "matrix",
    85	      "id": "2.3.4",
    86	      "type": "matrix_requirement",
    87	      "required_type": "optional",
    88	      "product_filter": "common",
    89	      "lot_filter": "common",
    90	      "terminal_filter": "common",
    91	      "payment_method_filter": "common",
    92	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    93	      "topics": [
    94	        "Обмен документами через заказное письмо"
    95	      ],
    96	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
    97	    },
    98	    {
    99	      "source": "matrix",
   100	      "id": "2.3.5",
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos"],
     5	  "payment_method": ["card", "qr"],
     6	  "legal_regime": "44_fz",
     7	  "notes": [
     8	    "Contract is a 44-FZ public procurement contract (Federal Law No. 44-FZ dated 05.04.2013)",
     9	    "Product is trade acquiring (торговый эквайринг) with POS terminals at physical TST locations",
    10	    "Contract mentions QR-code capability on terminals (Приложение №1, п.5: 'Возможность вывода QR-кода для безналичной оплаты на дисплей терминала')",
    11	    "Payment methods: bank cards (МИР, VISA, MasterCard) and QR-code",
    12	    "No internet acquiring, no SberPay, no smart terminals explicitly selected",
    13	    "Terminals are Bank-provided POS terminals (Электронные терминалы), not smart terminals",
    14	    "Contract price: 1,900,000 RUB max",
    15	    "Contract period: 01.03.2025 - 30.11.2025",
    16	    "Commission: to be filled (blank in specification)",
    17	    "Terminal service fee: absent (комиссия за предоставление терминалов - отсутствует, абонентская плата - отсутствует)"
    18	  ]
    19	}
Tool:      1	{
     2	  "matrix_propositions": [
     3	    {
     4	      "id": "2.1",
     5	      "source": "matrix",
     6	      "type": "matrix_requirement",
     7	      "required_type": "mandatory",
     8	      "product_filter": "common",
     9	      "lot_filter": "common",
    10	      "terminal_filter": "common",
    11	      "payment_method_filter": "common",
    12	      "main_idea": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
    13	      "topics": [
    14	        "Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом",
    15	        "Банк может отказать в регистрации ТСТ без указания причины",
    16	        "Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении",
    17	        "Информация о новых устройствах предоставляется с указанием их количества"
    18	      ],
    19	      "enriched_text": "В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору.\nБанк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соо"
    20	    },
    21	    {
    22	      "id": "2.2",
    23	      "source": "matrix",
    24	      "type": "matrix_requirement",
    25	      "required_type": "mandatory",
    26	      "product_filter": "common",
    27	      "lot_filter": "common",
    28	      "terminal_filter": "common",
    29	      "payment_method_filter": "common",
    30	      "main_idea": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    31	      "topics": [
    32	        "Расчёты производятся в рублях Российской Федерации"
    33	      ],
    34	      "enriched_text": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации. "
    35	    },
    36	    {
    37	      "id": "2.3.1",
    38	      "source": "matrix",
    39	      "type": "matrix_requirement",
    40	      "required_type": "mandatory",
    41	      "product_filter": "common",
    42	      "lot_filter": "common",
    43	      "terminal_filter": "common",
    44	      "payment_method_filter": "common",
    45	      "main_idea": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    46	      "topics": [
    47	        "Обмен информацией по электронной почте",
    48	        "Исключение передачи персональных данных, коммерческой и банковской тайны через электронную почту",
    49	        "Информация и документы, направленные по электронной почте, имеют юридическую силу"
    50	      ],
    51	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг и/или Информаци"
    52	    },
    53	    {
    54	      "id": "2.3.2",
    55	      "source": "matrix",
    56	      "type": "matrix_requirement",
    57	      "required_type": "mandatory",
    58	      "product_filter": "common",
    59	      "lot_filter": "common",
    60	      "terminal_filter": "common",
    61	      "payment_method_filter": "common",
    62	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    63	      "topics": [
    64	        "Обмен документами посредством системы ДБО или аналогичных систем Банка"
    65	      ],
    66	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;"
    67	    },
    68	    {
    69	      "id": "2.3.3",
    70	      "source": "matrix",
    71	      "type": "matrix_requirement",
    72	      "required_type": "optional",
    73	      "product_filter": "common",
    74	      "lot_filter": "common",
    75	      "terminal_filter": "common",
    76	      "payment_method_filter": "common",
    77	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    78	      "topics": [
    79	        "Обмен документами с доставкой нарочным или курьером"
    80	      ],
    81	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
    82	    },
    83	    {
    84	      "id": "2.3.4",
    85	      "source": "matrix",
    86	      "type": "matrix_requirement",
    87	      "required_type": "optional",
    88	      "product_filter": "common",
    89	      "lot_filter": "common",
    90	      "terminal_filter": "common",
    91	      "payment_method_filter": "common",
    92	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
    93	      "topics": [
    94	        "Обмен документами через заказное письмо"
    95	      ],
    96	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
    97	    },
    98	    {
    99	      "id": "2.3.5",
   100	      "source": "matrix",
AI: Now let me understand the scope better. I need to find matrix ids starting from "5.3.18.2" to the end. Let me look at the matrix to understand the numbering and find where 5.3.18.2 is.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\n# Get all ids\nids = [item[\'number\'] for item in matrix]\nprint(f\'Total matrix items: {len(ids)}\')\nprint(f\'First 5: {ids[:5]}\')\nprint(f\'Last 5: {ids[-5:]}\')\n# Find 5.3.18.2\nfor i, item in enumerate(matrix):\n    if item[\'number\'] == \'5.3.18.2\':\n        print(f\'Found 5.3.18.2 at index {i}\')\n        break\n# Print all ids from 5.3.18.2 onwards\nfound = False\nbatch2_ids = []\nfor item in matrix:\n    if item[\'number\'] == \'5.3.18.2\':\n        found = True\n    if found:\n        batch2_ids.append(item[\'number\'])\nprint(f\'Batch 2 ids count: {len(batch2_ids)}\')\nprint(f\'Batch 2 ids: {batch2_ids[:20]}...\')\nprint(f\'Batch 2 last: {batch2_ids[-5:]}\')\n"\n'}, 'id': 'call_00_Nr0zf5FAGBjHeHIjR1IJ7644', 'type': 'tool_call'}]
Tool: Total matrix items: 169
First 5: ['2.1', '2.2', '2.3.1', '2.3.2', '2.3.3']
Last 5: ['11.9', '11.10', '11.11', '11.12', '11.13']
Batch 2 ids count: 0
Batch 2 ids: []...
Batch 2 last: []

[Command succeeded with exit code 0]
AI: Hmm, 5.3.18.2 doesn't exist. Let me look at the full matrix structure more carefully.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\n# Print all ids\nids = [item[\'number\'] for item in matrix]\nfor i, id_val in enumerate(ids):\n    print(f\'{i}: {id_val}\')\n"\n'}, 'id': 'call_00_42rlQtfqPpOA1ZsA79Ym2845', 'type': 'tool_call'}]
Tool: 0: 2.1
1: 2.2
2: 2.3.1
3: 2.3.2
4: 2.3.3
5: 2.3.4
6: 2.3.5
7: 2.3.6
8: 2.3.7
9: 2.4
10: 2.5.1.1
11: 2.5.2.1
12: 2.6.1.1
13: 2.6.2.1
14: 2.6.2.2
15: 2.6.3.1
16: 2.6.3.2
17: 2.7
18: 3.1
19: 3.2
20: 3.3
21: 4.1.1
22: 4.1.2
23: 4.1.3
24: 4.2.1
25: 4.2.2
26: 4.2.3
27: 4.2.4
28: 4.2.5
29: 4.2.6
30: 4.2.7
31: 4.2.8
32: 4.2.9
33: 4.2.10
34: 4.2.11
35: 4.2.12
36: 4.2.13
37: 4.2.14
38: 4.2.15
39: 4.2.16.1
40: 4.2.16.2
41: 4.2.16.3
42: 4.2.17
43: 4.2.18
44: 4.2.19
45: 4.2.20.1
46: 4.2.20.2
47: 4.2.20.3
48: 4.2.20.4
49: 4.2.20.5
50: 4.2.20.6
51: 4.2.20.7
52: 4.2.21.1
53: 4.2.21.2
54: 4.2.21.3
55: 4.2.21.4
56: 4.2.21.5
57: 4.2.21.6
58: 4.2.21.7
59: 4.2.21.8
60: 4.2.22
61: 4.2.23
62: 4.2.24
63: 4.2.25
64: 4.2.26
65: 5.1.1.1
66: 5.1.1.2
67: 5.1.1.3
68: 5.1.1.4
69: 5.1.1.5
70: 5.1.1.6
71: 5.1.2
72: 5.1.3
73: 5.1.4
74: 5.1.5
75: 5.1.6
76: 5.1.7
77: 5.1.8.1
78: 5.1.8.2
79: 5.1.8.3
80: 5.1.8.4
81: 5.1.8.5
82: 5.1.8.6
83: 5.1.8.7
84: 5.1.8.8
85: 5.1.8.9
86: 5.1.8.10
87: 5.1.8.11
88: 5.1.8.12
89: 5.1.8.13
90: 5.1.9
91: 5.1.10
92: 5.1.11
93: 5.1.12
94: 5.1.13
95: 5.1.14
96: 5.1.15
97: 5.1.16
98: 5.1.17.1
99: 5.1.17.2
100: 5.2.1
101: 5.2.2
102: 5.2.3
103: 5.2.4
104: 5.2.5
105: 5.2.6
106: 5.2.7
107: 5.2.8
108: 5.2.9
109: 5.2.10
110: 5.2.12
111: 6.1
112: 6.2
113: 6.3
114: 6.4
115: 6.5
116: 6.6
117: 6.7
118: 6.8
119: 6.9
120: 6.10
121: 6.11
122: 6.12
123: 6.13
124: 6.14
125: 6.15
126: 6.16
127: 6.17
128: 6.18
129: 6.20
130: 6.21
131: 7.1
132: 7.2
133: 7.3
134: 7.4
135: 7.5
136: 7.6
137: 7.7
138: 7.8
139: 7.9
140: 7.10
141: 7.11
142: 7.12
143: 7.13
144: 7.14
145: 7.15
146: 7.16
147: 7.17
148: 8.1
149: 8.2
150: 9.1
151: 9.2
152: 9.3
153: 10.1
154: 10.2
155: 10.3
156: 11.1
157: 11.2
158: 11.3
159: 11.4
160: 11.5
161: 11.6
162: 11.7
163: 11.8
164: 11.9
165: 11.10
166: 11.11
167: 11.12
168: 11.13

[Command succeeded with exit code 0]
AI: There's no "5.3.18.2" in the matrix. The user said "Contract coverage batch 2 (ids 5.3.18.2 to end)". This might refer to contract clause ids, not matrix ids. Let me check the contract text and the existing batch files to understand the scope.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_batch_01.json', 'limit': 50}, 'id': 'call_00_qt8IM2dBucA7pi7LzSEk4269', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_batch_02.json', 'limit': 50}, 'id': 'call_01_LhehK0LGITyTHCu27wgY3656', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_batch_01.json', 'limit': 50}, 'id': 'call_02_vKxErnowjyUy9YcPMppz4713', 'type': 'tool_call'}]
Tool:      1	["1", "1.1", "1.2", "1.3", "2", "2.1", "2.1.1", "2.1.2", "2.1.3", "2.1.4", "2.1.5", "2.1.6", "2.1.7", "2.1.8", "2.1.13", "2.1.14", "2.1.15", "2.1.16", "2.1.17", "2.1.18", "2.1.19", "2.1.20", "2.1.21", "2.1.22", "2.1.23", "2.1.24", "2.1.25", "2.1.26", "2.1.27", "2.1.28", "2.2", "2.3", "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "3", "3.1", "3.1.1", "3.3", "4", "4.1", "4.2", "4.4", "4.5.1", "5.1.1", "5.1.2", "5.1.3", "5.1.4", "5.1.5", "5.1.6", "5.1.7", "5.1.8", "5.1.9", "5.1.10", "5.2", "5.2.1", "5.2.2", "5.2.3", "5.2.4", "5.2.5", "5.2.6", "5.2.7", "5.2.8", "5.2.9", "5.2.9.1", "5.2.9.2", "5.2.9.3", "5.2.9.4", "5.2.9.5", "5.2.9.6", "5.2.9.7", "5.2.9.8", "5.2.9.9", "5.2.9.10", "5.2.9.11", "5.2.10", "5.2.10.1", "5.2.10.2", "5.2.10.3", "5.2.10.4", "5.2.10.5", "5.3", "5.3.1", "5.3.2", "5.3.3", "5.3.4", "5.3.5", "5.3.6", "5.3.7", "5.3.8", "5.3.9", "5.3.10", "5.3.11", "5.3.12", "5.3.13", "5.3.14", "5.3.15", "5.3.16", "5.3.17", "5.3.18", "5.3.18.1"]
Tool:      1	["5.3.18.2", "5.3.18.3", "5.3.20.4", "5.3.18.5", "5.3.19", "5.3.20", "5.4", "5.4.1", "5.4.2", "5.4.3", "5.4.4", "5.4.5", "5.5", "5.6", "5.7", "5.9", "5.10", "6", "6.1", "7", "7.1", "7.2", "7.3", "7.4", "7.4.1", "7.5", "7.6", "7.7", "7.7.1", "7.7.2", "10", "5", "1", "10", "5", "1", "7.7.3", "7.8", "7.9", "7.10", "7.11", "7.12", "8", "8.1", "8.2", "8.3", "8.3.1", "8.3.2", "8.4", "8.5", "8.5.1", "8.5.2", "8.5.3", "8.5.4", "8.5.5", "8.5.6", "8.5.7", "8.5.8", "8.5.9", "8.6", "8.7", "8.8", "8.9", "8.10", "8.11", "9", "9.1", "9.2", "9.3", "10", "10.1", "10.2", "11", "11.1", "11.2", "11.3", "11.4", "11.5", "11.6", "11.7", "11.8", "12", "12.1", "12.2", "12.3", "12.4", "12.5", "13", "1", "2", "3", "4", "5", "9.2.1", "1", "2", "3", "1.1", "1.2", "1.3", "4", "10", "1", "1"]
Tool:      1	["2.1", "2.2", "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "2.4", "2.5.1.1", "2.5.2.1", "2.6.1.1", "2.6.2.1", "2.6.2.2", "2.6.3.1", "2.6.3.2", "2.7", "3.1", "3.2", "3.3", "4.1.1", "4.1.2", "4.1.3", "4.2.1", "4.2.2", "4.2.3", "4.2.4", "4.2.5", "4.2.6", "4.2.7", "4.2.8", "4.2.9", "4.2.10", "4.2.11", "4.2.12", "4.2.13", "4.2.14", "4.2.15", "4.2.16.1", "4.2.16.2", "4.2.16.3", "4.2.17"]
AI: Now I see. The contract_batch_01.json ends with "5.3.18.1" and contract_batch_02.json starts with "5.3.18.2". So the scope is contract clauses from "5.3.18.2" to the end of the contract. Let me also check the matrix batches to understand what matrix ids have been covered.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_batch_02.json', 'limit': 50}, 'id': 'call_00_a1AuDDmTzWetWsrb1OQ93873', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_batch_03.json', 'limit': 50}, 'id': 'call_01_D1SZuyDLCbQ7tB9qdrvW0899', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_batch_04.json', 'limit': 50}, 'id': 'call_02_iJenVvoPesmjmCQmFO575595', 'type': 'tool_call'}]
Tool:      1	["4.2.18", "4.2.19", "4.2.20.1", "4.2.20.2", "4.2.20.3", "4.2.20.4", "4.2.20.5", "4.2.20.6", "4.2.20.7", "4.2.21.1", "4.2.21.2", "4.2.21.3", "4.2.21.4", "4.2.21.5", "4.2.21.6", "4.2.21.7", "4.2.21.8", "4.2.22", "4.2.23", "4.2.24", "4.2.25", "4.2.26", "5.1.1.1", "5.1.1.2", "5.1.1.3", "5.1.1.4", "5.1.1.5", "5.1.1.6", "5.1.2", "5.1.3", "5.1.4", "5.1.5", "5.1.6", "5.1.7", "5.1.8.1", "5.1.8.2", "5.1.8.3", "5.1.8.4", "5.1.8.5", "5.1.8.6", "5.1.8.7", "5.1.8.8", "5.1.8.9"]
Tool:      1	["5.1.8.10", "5.1.8.11", "5.1.8.12", "5.1.8.13", "5.1.9", "5.1.10", "5.1.11", "5.1.12", "5.1.13", "5.1.14", "5.1.15", "5.1.16", "5.1.17.1", "5.1.17.2", "5.2.1", "5.2.2", "5.2.3", "5.2.4", "5.2.5", "5.2.6", "5.2.7", "5.2.8", "5.2.9", "5.2.10", "5.2.12", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9", "6.10", "6.11", "6.12", "6.13", "6.14", "6.15", "6.16", "6.17", "6.18"]
Tool:      1	["6.20", "6.21", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9", "7.10", "7.11", "7.12", "7.13", "7.14", "7.15", "7.16", "7.17", "8.1", "8.2", "9.1", "9.2", "9.3", "10.1", "10.2", "10.3", "11.1", "11.2", "11.3", "11.4", "11.5", "11.6", "11.7", "11.8", "11.9", "11.10", "11.11", "11.12", "11.13"]
AI: Now I understand the structure. The contract_batch_02.json contains contract clause ids from "5.3.18.2" to the end. My task is to perform the coverage analysis for these contract clauses against the matrix. Let me now read the contract text to understand the clauses in scope.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 100}, 'id': 'call_00_Dc1DoIIOZ8pi0Ht0Nu3Q3887', 'type': 'tool_call'}]
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
AI: Let me continue reading the contract to find the clauses from 5.3.18.2 onwards.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 100, 'limit': 100}, 'id': 'call_00_Aq0JzvviP6KUzpxgtdJs1371', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_Zx0KydBkP0R0yJ0CpjYv1194', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 400, 'limit': 200}, 'id': 'call_00_93yE2hoX6dCLRjzAjUf53063', 'type': 'tool_call'}]
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
AI: Now I have a good understanding of the contract. Let me set up my task plan and start the analysis. The scope is contract clauses from "5.3.18.2" to the end of the contract. Let me first understand what matrix items are relevant for this batch.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read and understand all contract clauses in batch 2 scope (5.3.18.2 to end)', 'status': 'in_progress'}, {'content': 'Read full matrix.json to understand all matrix requirements', 'status': 'pending'}, {'content': 'Create legal propositions for batch 2 contract clauses', 'status': 'pending'}, {'content': 'Perform bidirectional matching: matrix-to-contract and contract-to-matrix', 'status': 'pending'}, {'content': 'Assign group-level status (aligned/deviation/missing/extra)', 'status': 'pending'}, {'content': 'Build coverage ledger and closure QA', 'status': 'pending'}, {'content': 'Write batch 2 working output files', 'status': 'pending'}, {'content': 'Return compact JSON fragments and summary', 'status': 'pending'}]}, 'id': 'call_00_kUps1MsGEnMtEesmmIMj9893', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read and understand all contract clauses in batch 2 scope (5.3.18.2 to end)', 'status': 'in_progress'}, {'content': 'Read full matrix.json to understand all matrix requirements', 'status': 'pending'}, {'content': 'Create legal propositions for batch 2 contract clauses', 'status': 'pending'}, {'content': 'Perform bidirectional matching: matrix-to-contract and contract-to-matrix', 'status': 'pending'}, {'content': 'Assign group-level status (aligned/deviation/missing/extra)', 'status': 'pending'}, {'content': 'Build coverage ledger and closure QA', 'status': 'pending'}, {'content': 'Write batch 2 working output files', 'status': 'pending'}, {'content': 'Return compact JSON fragments and summary', 'status': 'pending'}]
AI: Let me now extract the contract clauses in batch 2 scope and read the full matrix.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/outputs/working/contract_batch_02.json\', \'r\') as f:\n    batch2 = json.load(f)\nprint(\'Batch 2 contract ids:\')\nfor i, cid in enumerate(batch2):\n    print(f\'{i}: {cid}\')\nprint(f\'\\nTotal: {len(batch2)}\')\n"\n'}, 'id': 'call_00_cyolzE5lXPRkvbnu7Gd99863', 'type': 'tool_call'}]
Tool: Batch 2 contract ids:
0: 5.3.18.2
1: 5.3.18.3
2: 5.3.20.4
3: 5.3.18.5
4: 5.3.19
5: 5.3.20
6: 5.4
7: 5.4.1
8: 5.4.2
9: 5.4.3
10: 5.4.4
11: 5.4.5
12: 5.5
13: 5.6
14: 5.7
15: 5.9
16: 5.10
17: 6
18: 6.1
19: 7
20: 7.1
21: 7.2
22: 7.3
23: 7.4
24: 7.4.1
25: 7.5
26: 7.6
27: 7.7
28: 7.7.1
29: 7.7.2
30: 10
31: 5
32: 1
33: 10
34: 5
35: 1
36: 7.7.3
37: 7.8
38: 7.9
39: 7.10
40: 7.11
41: 7.12
42: 8
43: 8.1
44: 8.2
45: 8.3
46: 8.3.1
47: 8.3.2
48: 8.4
49: 8.5
50: 8.5.1
51: 8.5.2
52: 8.5.3
53: 8.5.4
54: 8.5.5
55: 8.5.6
56: 8.5.7
57: 8.5.8
58: 8.5.9
59: 8.6
60: 8.7
61: 8.8
62: 8.9
63: 8.10
64: 8.11
65: 9
66: 9.1
67: 9.2
68: 9.3
69: 10
70: 10.1
71: 10.2
72: 11
73: 11.1
74: 11.2
75: 11.3
76: 11.4
77: 11.5
78: 11.6
79: 11.7
80: 11.8
81: 12
82: 12.1
83: 12.2
84: 12.3
85: 12.4
86: 12.5
87: 13
88: 1
89: 2
90: 3
91: 4
92: 5
93: 9.2.1
94: 1
95: 2
96: 3
97: 1.1
98: 1.2
99: 1.3
100: 4
101: 10
102: 1
103: 1

Total: 104

[Command succeeded with exit code 0]
AI: I notice the batch 2 list has some odd entries (like "10", "5", "1" appearing multiple times, and some that look like appendix references). Let me now read the full matrix to understand all requirements.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_JEoPmgN3HO3hsp9Ue5Nm6613', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_0Pv9Yymdjxt9JOQG1BQE4070', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 500, 'limit': 400}, 'id': 'call_00_d1vAeWMDo119bmbvzBBk7465', 'type': 'tool_call'}]
Tool:    501	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Акцептовать платежные требования и счета на оплату, выставленные Банком в соответствии с п. 5.1.4 Договора к расчетному счету Предприятия, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров\/услуг, в течение 5 (пяти) рабочих дней с даты их выставления.",
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 900, 'limit': 400}, 'id': 'call_00_QepQrQxVRGhFty9o4yUU4516', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 1300, 'limit': 400}, 'id': 'call_00_mrtTDyPZD273fcGgqezq8946', 'type': 'tool_call'}]
Tool:   1301	 {
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 1700, 'limit': 400}, 'id': 'call_00_D87arfhQlGeqGHQOy6JT1431', 'type': 'tool_call'}]
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
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 2100, 'limit': 400}, 'id': 'call_00_KIg80McPQFNr5y3BG5de8190', 'type': 'tool_call'}]
Tool:   2101	  "only_for_product":"common",
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
  2201	  "number":"10.2",
  2202	  "enriched_text":"РАЗДЕЛ 10 «СРОК ДЕЙСТВИЯ ДОГОВОРА И ПОРЯДОК ЕГО РАСТОРЖЕНИЯ → Любая Сторона по Договору вправе его досрочно расторгнуть в одностороннем внесудебном порядке, письменно уведомив об этом другую Сторону не менее чем за 30 (тридцать) календарных дней до даты расторжения, за исключением случаев, предусмотренных п. 5.1.8 настоящего Договора",
  2203	  "required_type":"mandatory",
  2204	  "main_idea":"Важно описание возможности расторгнуть договор в одностороннем порядке. Важен срок уведомления о расторжении.",
  2205	  "only_for_product":"common",
  2206	  "only_for_lot":"common",
  2207	  "only_for_terminal":"common",
  2208	  "topics":[
  2209	   "Право любой стороны расторгнуть договор в одностороннем порядке",
  2210	   "Обязанность уведомления другой стороны о расторжении в одностороннем порядке",
  2211	   "Право Банка расторгнуть договор в одностороннем порядке",
  2212	   "Право Предприятия расторгнуть договор в одностороннем порядке"
  2213	  ],
  2214	  "payment_method":"common"
  2215	 },
  2216	 {
  2217	  "number":"10.3",
  2218	  "enriched_text":"РАЗДЕЛ 10 «СРОК ДЕЙСТВИЯ ДОГОВОРА И ПОРЯДОК ЕГО РАСТОРЖЕНИЯ → При расторжении настоящего Договора Банком в одностороннем внесудебном порядке в случаях, предусмотренных п. 5.1.8. настоящего Договора, Договор считается расторгнутым с даты, указанной в письменном уведомлении Банка о расторжении. Стороны осуществляют расчеты\/взаиморасчеты в течение 18 (восемнадцать) месяцев с даты расторжения Договора. Предприятие выплачивает Банку суммы Операций в порядке, установленном п.п. 5.1.3, 5.1.4 и разделом 6 настоящего Договора",
  2219	  "required_type":"mandatory",
  2220	  "main_idea":"",
  2221	  "only_for_product":"common",
  2222	  "only_for_lot":"common",
  2223	  "only_for_terminal":"common",
  2224	  "topics":[
  2225	   "Сроки, в которые договор считается расторгнутым в случае расторжения в одностороннем внесудебном порядке",
  2226	   "Сроки расчетов после одностороннего внесудебного порядка расторжения - 18 месяцев",
  2227	   "Порядок выплаты сумм операций определен в пунктах 5.1.3, 5.1.4 и разделе 6"
  2228	  ],
  2229	  "payment_method":"common"
  2230	 },
  2231	 {
  2232	  "number":"11.1",
  2233	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Стороны соглашаются, что источниками правового регулирования отношений Сторон в рамках Договора являются настоящие Договор, действующее законодательство РФ, правила, стандарты и рекомендации Платежной системы при условии их не противоречия действующему законодательству РФ.Любые условия и положения Договора, которые противоречат положениям правил Платежной системы (как известных в момент заключения Договора, так и введенных в действие в будущем), должны быть приведены в соответствие с правилами Платежной системы, если это не противоречит законодательству РФ.\n",
  2234	  "required_type":"optional",
  2235	  "main_idea":"",
  2236	  "only_for_product":"common",
  2237	  "only_for_lot":"common",
  2238	  "only_for_terminal":"common",
  2239	  "topics":[
  2240	   "Перечисление источников правового регулирования отношений Сторон",
  2241	   "Требование соблюдать законодательство РФ",
  2242	   "Условия и положения Договора, противоречащие правила Платежной системы должны быть приведены в соответствие"
  2243	  ],
  2244	  "payment_method":"common"
  2245	 },
  2246	 {
  2247	  "number":"11.2",
  2248	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Информация, полученная Предприятием в рамках исполнения Договора (номера Карт\/Платежных счетов, персональные данные Покупателей, суммы Операций, информация о платеже), является конфиденциальной и не подлежит передаче третьим лицам, за исключением случаев, предусмотренных действующим законодательством РФ или условиями Договором.",
  2249	  "required_type":"optional",
  2250	  "main_idea":"",
  2251	  "only_for_product":"common",
  2252	  "only_for_lot":"common",
  2253	  "only_for_terminal":"common",
  2254	  "topics":[
  2255	   "Номера Карт\/Платежных счетов, персональные данные Покупателей, суммы Операций, информация о платеже являются конфиденциальной информацией",
  2256	   "Объявляется запрет на передачу конфиденциальной информации третьим лицам",
  2257	   "Даётся разрешение на передачу конфиденциальной информации разрешена, только если это требование законодательства или условие договора"
  2258	  ],
  2259	  "payment_method":"common"
  2260	 },
  2261	 {
  2262	  "number":"11.3",
  2263	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Стороны обязуются не разглашать полученные в ходе исполнения Договора сведения, включая:\n• описание защитных элементов Карт;\n• технологию проведения Операций;\n• информацию об управлении, финансовой и иной деятельности Сторон;\n• иную информацию, разглашение которой может привести к возникновению убытков или негативно повлиять на деловую репутацию Сторон.\nПредоставление указанной информации допускается только при согласии обеих Сторон.\nДанное положение не отменяет п. 5.1.7 Договора",
  2264	  "required_type":"optional",
  2265	  "main_idea":"",
  2266	  "only_for_product":"common",
  2267	  "only_for_lot":"common",
  2268	  "only_for_terminal":"common",
  2269	  "topics":[
  2270	   "Стороны обязуются не разглашать иным лицам полученные сведения о защитных элементов карт",
  2271	   "Стороны обязуются не разглашать иным лицам полученные сведения о технологии проведения операций",
  2272	   "Стороны обязуются не разглашать иным лицам полученные сведения о финансовом состоянии сторон",
  2273	   "Стороны обязуются не разглашать иным лицам конфиденциальную информацию без согласия другой стороны"
  2274	  ],
  2275	  "payment_method":"common"
  2276	 },
  2277	 {
  2278	  "number":"11.4",
  2279	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все изменения и дополнения к настоящему Договору, кроме документов, ссылки на которые даются в настоящем Договоре, размещенные на Официальном сайте Банка, действительны лишь в том случае, если они совершены в письменной форме, и подписаны уполномоченными представителями Сторон",
  2280	  "required_type":"optional",
  2281	  "main_idea":"",
  2282	  "only_for_product":"common",
  2283	  "only_for_lot":"common",
  2284	  "only_for_terminal":"common",
  2285	  "topics":[
  2286	   "изменения и дополнения должны быть в письменной форме",
  2287	   "подписаны уполномоченными представителями обеих сторон"
  2288	  ],
  2289	  "payment_method":"common"
  2290	 },
  2291	 {
  2292	  "number":"11.5",
  2293	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все имевшие место до подписания настоящего Договора соглашения, переговоры и переписка между Сторонами по вопросам, изложенным в настоящем Договоре, утрачивают силу с даты подписания настоящего Договора.",
  2294	  "required_type":"optional",
  2295	  "main_idea":"",
  2296	  "only_for_product":"common",
  2297	  "only_for_lot":"common",
  2298	  "only_for_terminal":"common",
  2299	  "topics":[
  2300	
  2301	  ],
  2302	  "payment_method":"common"
  2303	 },
  2304	 {
  2305	  "number":"11.6",
  2306	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Настоящий Договор составлен в ________ экземплярах, _________ экземпляр(-а) для Банка, один экземпляр для Предприятия",
  2307	  "required_type":"optional",
  2308	  "main_idea":"",
  2309	  "only_for_product":"common",
  2310	  "only_for_lot":"common",
  2311	  "only_for_terminal":"common",
  2312	  "topics":[
  2313	   "Договор составлен в определенном количестве экземпляров",
  2314	   "указано количество экземпляров Договора для Банка",
  2315	   "указано количество экземпляров Договора для Предприятия"
  2316	  ],
  2317	  "payment_method":"common"
  2318	 },
  2319	 {
  2320	  "number":"11.7",
  2321	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все Приложения к настоящему Договору являются его неотъемлемой частью",
  2322	  "required_type":"optional",
  2323	  "main_idea":"",
  2324	  "only_for_product":"common",
  2325	  "only_for_lot":"common",
  2326	  "only_for_terminal":"common",
  2327	  "topics":[
  2328	   "Общие слова про то, что приложения являются неотъемлемой частью договора"
  2329	  ],
  2330	  "payment_method":"common"
  2331	 },
  2332	 {
  2333	  "number":"11.8",
  2334	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Предприятие заверяет, что реализация Товаров\/услуг в ТСТ осуществляется в соответствии с требованиями действующего законодательства РФ",
  2335	  "required_type":"optional",
  2336	  "main_idea":"",
  2337	  "only_for_product":"common",
  2338	  "only_for_lot":"common",
  2339	  "only_for_terminal":"common",
  2340	  "topics":[
  2341	   "Предприятие (Заказчик) заверяет, что реализация Товаров\/услуг осуществляется в соответствии с требованиями законодательства РФ"
  2342	  ],
  2343	  "payment_method":"common"
  2344	 },
  2345	 {
  2346	  "number":"11.9",
  2347	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Ни одна из Сторон не вправе передавать свои обязанности и\/или права по Договору третьим лицам без письменного согласования с другой Стороной, за исключением случая реорганизации одной из Сторон",
  2348	  "required_type":"optional",
  2349	  "main_idea":"",
  2350	  "only_for_product":"common",
  2351	  "only_for_lot":"common",
  2352	  "only_for_terminal":"common",
  2353	  "topics":[
  2354	   "запрет передачи обязательств и прав без письменного согласия другой стороны",
  2355	   "возможность передачи обязательств для случаев реорганизации стороны"
  2356	  ],
  2357	  "payment_method":"common"
  2358	 },
  2359	 {
  2360	  "number":"11.10",
  2361	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ →  В случае реорганизации одной из Сторон обязательства по Договору в полном объеме переходят к правопреемнику. В случае ликвидации одной из Сторон имущественные требования другой Стороны удовлетворяются за счет имущества ликвидируемой Стороны в установленном законодательством РФ порядке",
  2362	  "required_type":"optional",
  2363	  "main_idea":"",
  2364	  "only_for_product":"common",
  2365	  "only_for_lot":"common",
  2366	  "only_for_terminal":"common",
  2367	  "topics":[
  2368	   "При реорганизации одной из Сторон обязательства переходят к правопреемнику",
  2369	   "В случае ликвидации одной из сторон - удовлетворение имущественных требований за счет имущества ликвидируемой стороны"
  2370	  ],
  2371	  "payment_method":"common"
  2372	 },
  2373	 {
  2374	  "number":"11.11",
  2375	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Инструктивные материалы, касающиеся предмета Договора, включая документы, ссылки на которые даются в настоящем Договоре, размещенные на Официальном сайте Банка, становятся обязательными к исполнению со следующего рабочего дня за днем размещения их на Официальном сайте Банка: https:\/\/www.sberbank.ru, если не указаны иные сроки ввода их в действие",
  2376	  "required_type":"optional",
  2377	  "main_idea":"Если в договоре не указан сайт - это не является разногласием",
  2378	  "only_for_product":"common",
  2379	  "only_for_lot":"common",
  2380	  "only_for_terminal":"common",
  2381	  "topics":[
  2382	   "Срок, с которого инструктивные материалы становятся обязательными к выполенению после размещения на официальном сайте"
  2383	  ],
  2384	  "payment_method":"common"
  2385	 },
  2386	 {
  2387	  "number":"11.12",
  2388	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все уведомления и запросы по Договору, за исключением случаев, когда Договором предусмотрен иной порядок их направления, считаются направленными надлежащим образом другой Стороне, если они направлены в соответствии с п. 2.3 Договора",
  2389	  "required_type":"optional",
  2390	  "main_idea":"Важно само наличие такой или похожей формулировки",
  2391	  "only_for_product":"common",
  2392	  "only_for_lot":"common",
  2393	  "only_for_terminal":"common",
  2394	  "topics":[
  2395	   "Общие слова про правомерность отправки уведомлений и запросов, если отправлены способами описанными в договоре"
  2396	  ],
  2397	  "payment_method":"common"
  2398	 },
  2399	 {
  2400	  "number":"11.13",
  2401	  "enriched_text":"РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → К настоящему Договору прилагаются:\n1) Приложение № 1 – Заявление Предприятия на проведение расчетов по операциям оплаты товаров\/услуг.\n2) Приложение № 1.1 – Информация о Торгово-Сервисной Точке\/Ресурсе Предприятия.\n3) Приложение № 2 – Акт о перечислении Предприятию сумм операций по картам.\nПриложение № 3 – Описание услуг, формирующих тарифы и параметры сервиса для Смарт-терминалов",
  2402	  "required_type":"optional",
  2403	  "main_idea":"",
  2404	  "only_for_product":"common",
  2405	  "only_for_lot":"common",
  2406	  "only_for_terminal":"common",
  2407	  "topics":[
  2408	   "Перечень документов, приложенных к договору"
  2409	  ],
  2410	  "payment_method":"common"
  2411	 }
  2412	]
AI: Now I have a complete picture of both the matrix and the contract. Let me now focus on the batch 2 scope. The contract clauses from 5.3.18.2 to end need to be analyzed. Let me now create a comprehensive analysis. Given the complexity, I'll use a Python script to help organize the work.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read and understand all contract clauses in batch 2 scope (5.3.18.2 to end)', 'status': 'completed'}, {'content': 'Read full matrix.json to understand all matrix requirements', 'status': 'completed'}, {'content': 'Create legal propositions for batch 2 contract clauses and perform bidirectional matching', 'status': 'in_progress'}, {'content': 'Assign group-level status (aligned/deviation/missing/extra)', 'status': 'pending'}, {'content': 'Build coverage ledger and closure QA', 'status': 'pending'}, {'content': 'Write batch 2 working output files', 'status': 'pending'}, {'content': 'Return compact JSON fragments and summary', 'status': 'pending'}]}, 'id': 'call_00_LNw2WCejwtFPGqjIqOx02683', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read and understand all contract clauses in batch 2 scope (5.3.18.2 to end)', 'status': 'completed'}, {'content': 'Read full matrix.json to understand all matrix requirements', 'status': 'completed'}, {'content': 'Create legal propositions for batch 2 contract clauses and perform bidirectional matching', 'status': 'in_progress'}, {'content': 'Assign group-level status (aligned/deviation/missing/extra)', 'status': 'pending'}, {'content': 'Build coverage ledger and closure QA', 'status': 'pending'}, {'content': 'Write batch 2 working output files', 'status': 'pending'}, {'content': 'Return compact JSON fragments and summary', 'status': 'pending'}]
AI: Now let me build the analysis. I'll create a comprehensive Python script to organize the matching, then produce the final output. Let me first identify the key contract clauses in batch 2 and their legal content, then match them against the matrix.[{'name': 'execute', 'args': {'command': 'python3 << \'PYEOF\'\nimport json\n\n# Contract clauses in batch 2 scope with their content\n# These are the clauses from 5.3.18.2 to end of contract\nbatch2_clauses = {\n    "5.3.18.2": "Предоставлять исполнителю доступ к местам установки электронных терминалов для проведения работ по его подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке",\n    "5.3.18.3": "Принять электронные терминалы по акту принятия оказанных услуг, составленному в двух экземплярах и подписанных исполнителем и заказчиком. один экземпляр акта находится на хранении у исполнителя, второй – у заказчика",\n    "5.3.20.4": "В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя",\n    "5.3.18.5": "Вернуть исполнителю или обслуживающей компании электронные терминалы/смарт-терминала в течение пяти рабочих дней с даты расторжения контракта или с даты получения письменного/устного требования исполнителя о возврате электронных терминалов",\n    "5.3.19": "Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере: средств, которые в соответствии с правилами Платежных систем были списаны со счета Исполнителя в пользу Банка-эмитента... убытков, возникших у Исполнителя в результате применения к нему штрафных санкций...",\n    "5.3.20": "В рамках настоящего Контракта Заказчик передает Исполнителю персональные данные руководителя Заказчика, состав которых включает: ФИО, адрес, паспортные данные. Заказчик гарантирует наличие правовых оснований на передачу...",\n    "5.4": "Заказчик вправе: (parent heading)",\n    "5.4.1": "Требовать от Исполнителя исполнения обязательств, предусмотренных контрактом, надлежащим образом",\n    "5.4.2": "Отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества",\n    "5.4.3": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ",\n    "5.4.4": "Отказаться от оплаты услуг ненадлежащего качества, а если услуги оплачены, потребовать возврата уплаченных сумм, а также требовать возмещения убытков",\n    "5.4.5": "Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем",\n    "5.5": "Заказчик обязуется передавать Исполнителю по его запросу в течение 3 рабочих дней письменное заявление с изложением обстоятельств проведения Операции. В случае утраты документов немедленно сообщить",\n    "5.6": "Заказчик обязуется в случае утери оборудования: Вернуть Исполнителю Электронные терминалы/Смарт-терминалы Банка в течение 5 рабочих дней с даты расторжения Контракта или с даты получения требования",\n    "5.7": "В случае невозврата Электронных терминалов/Смарт-терминалов Заказчик обязан уплатить Исполнителю штраф в размере 10 000 рублей за каждый Электронный терминал, 25 000 рублей за каждый Смарт-терминал",\n    "5.9": "Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций с использованием карт путем обращения в службу поддержки",\n    "5.10": "Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________",\n    "6": "АНТИКОРРУПЦИОННАЯ ОГОВОРКА (section heading)",\n    "6.1": "При заключении, исполнении, изменении и расторжении Контракта Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых как коррупция",\n    "7": "ОТВЕТСТВЕННОСТЬ СТОРОН (section heading)",\n    "7.1": "За неисполнение или ненадлежащее исполнение обязательств по Контракту Стороны несут ответственность в соответствии с действующим законодательством РФ. Сторона освобождается от уплаты неустойки если докажет что неисполнение произошло вследствие непреодолимой силы или по вине другой стороны. Общая сумма штрафов не может превышать цену контракта",\n    "7.2": "В случае просрочки исполнения Заказчиком обязательств Исполнитель вправе потребовать уплаты неустоек (штрафов, пеней)",\n    "7.3": "Пеня начисляется за каждый день просрочки исполнения Заказчиком обязательства в размере 1/300 ключевой ставки ЦБ РФ от не уплаченной в срок суммы",\n    "7.4": "Штрафы начисляются за ненадлежащее исполнение Заказчиком обязательств, за исключением просрочки",\n    "7.4.1": "Размер штрафа по каждому факту неисполнения Заказчиком обязательств устанавливается в соответствии с Постановлением № 1042: а) 1000 рублей если цена контракта не превышает 3 млн. рублей",\n    "7.5": "В случае просрочки исполнения Исполнителем обязательств Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней)",\n    "7.6": "Пеня начисляется за каждый день просрочки исполнения Исполнителем обязательства в размере 1/300 ключевой ставки ЦБ РФ от цены контракта, уменьшенной на сумму пропорциональную объему фактически исполненных обязательств",\n    "7.7": "Штрафы начисляются за неисполнение или ненадлежащее исполнение Исполнителем обязательств, за исключением просрочки",\n    "7.7.1": "Размер штрафа Исполнителю устанавливается в соответствии с Постановлением № 1042: а) 10 процентов цены контракта если цена не превышает 3 млн. рублей",\n    "7.7.2": "Размер штрафа Исполнителем как победителя закупки предложившего наиболее высокую цену за право заключения контракта",\n    "7.7.3": "Размер штрафа по каждому факту неисполнения Исполнителем обязательства которое не имеет стоимостного выражения: а) 1000 рублей если цена контракта не превышает 3 млн. рублей",\n    "7.8": "В случае обмена документами при применении мер ответственности такой обмен осуществляется с использованием ЕИС путем направления электронных уведомлений",\n    "7.9": "Применение неустойки (штрафа, пени) не освобождает Стороны от исполнения обязательств по Контракту",\n    "7.10": "Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств не может превышать цену Контракта",\n    "7.11": "Общая сумма начисленных штрафов за ненадлежащее исполнение Заказчиком обязательств не может превышать цену Контракта",\n    "7.12": "В случае расторжения Контракта в связи с односторонним отказом другая Сторона вправе потребовать возмещения только фактически понесенного ущерба сверх начисленных неустоек",\n    "8": "КАЧЕСТВО ОКАЗАННЫХ УСЛУГ, ПОРЯДОК ИХ ПРИЕМКИ. ГАРАНТИЯ КАЧЕСТВА УСЛУГ (section heading)",\n    "8.1": "Исполнитель гарантирует Заказчику качество оказанных услуг в течение всего срока установленного нормативно-правовыми актами РФ",\n    "8.2": "Исполнитель несёт ответственность за повреждения возникшие вследствие оказания услуг его специалистами",\n    "8.3": "Приемка результата исполнения Контракта осуществляется в порядке установленном законодательством РФ и настоящим Контрактом",\n    "8.3.1": "Исполнитель ежемесячно не позднее 10 рабочего дня месяца следующего за отчетным формирует с использованием ЕИС подписывает УКЭП и размещает в ЕИС документ о приемке",\n    "8.3.2": "К документу о приемке Исполнитель прилагает: счет-фактуру (при наличии), акт о перечислении Заказчику сумм операций по картам и счет ф.363 на оплату услуг",\n    "8.4": "Датой поступления Заказчику документа о приемке считается дата размещения в ЕИС",\n    "8.5": "Приемка услуг от имени Заказчика производится уполномоченным лицом (либо приемочной комиссией)",\n    "8.5.1": "Заказчик в срок не более 10 рабочих дней со дня поступления документа о приемке подписывает УКЭП и размещает в ЕИС документ о приемке либо мотивированный отказ",\n    "8.5.2": "По письменному уведомлению Исполнителем Заказчика приемка может производиться только в присутствии представителя Исполнителя",\n    "8.5.3": "В случае если поступило уведомление об участии в приемке приемка производится только в двустороннем порядке",\n    "8.5.4": "В случае если уведомление об участии в приемке не поступило приемка производится Заказчиком в одностороннем порядке",\n    "8.5.5": "Для проверки оказанных услуг Заказчик проводит экспертизу",\n    "8.5.6": "Экспертиза может проводиться Заказчиком своими силами или с привлечением экспертов",\n    "8.5.7": "В случае отсутствия замечаний Заказчик в течение 10 рабочих дней подписывает УКЭП и размещает в ЕИС документ о приемке",\n    "8.5.8": "В случае если будут установлены несоответствия дальнейшая приемка может осуществляться приемочной комиссией",\n    "8.5.9": "В случае получения мотивированного отказа Исполнитель вправе устранить причины и направить исправленный документ о приемке",\n    "8.6": "Датой приемки оказанных услуг считается дата размещения в ЕИС документа о приемке подписанного Заказчиком",\n    "8.7": "Внесение исправлений в документ о приемке осуществляется путем формирования подписания УКЭП и размещения в ЕИС исправленного документа",\n    "8.8": "Оформление результата проведения процедуры приемки осуществляется в порядке и в сроки указанные в настоящем разделе",\n    "8.9": "В случае выявления несоответствия Заказчик вправе не отказывать в приемке если выявленное несоответствие не препятствует приемке и устранено Исполнителем",\n    "8.10": "В случае оказания услуг ненадлежащего качества Исполнитель обязан безвозмездно устранить недостатки в течение 3 дней с даты заявления о них Заказчиком",\n    "8.11": "Подписанный УКЭП Заказчика и Исполнителя документ о приемке является основанием для оплаты Исполнителю оказанных услуг",\n    "9": "ДЕЙСТВИЕ ОБСТОЯТЕЛЬСТВ НЕПРЕОДОЛИМОЙ СИЛЫ (section heading)",\n    "9.1": "Стороны освобождаются от ответственности за частичное или полное неисполнение обязательств если их исполнению препятствует чрезвычайное и непреодолимое обстоятельство: стихийные бедствия, наводнения, землетрясения, пожары, военные действия, забастовки, эпидемия",\n    "9.2": "При возникновении обстоятельств непреодолимой силы сторона обязана оповестить другую не позднее пяти дней. Срок выполнения обязательств переносится соразмерно времени действия обстоятельств. Если обстоятельства длятся более одного календарного месяца Стороны вправе расторгнуть контракт",\n    "9.3": "Сторона ссылающаяся на обстоятельства непреодолимой силы обязана представить документальное подтверждение их наступления",\n    "10": "ПОРЯДОК РАЗРЕШЕНИЯ СПОРОВ (section heading)",\n    "10.1": "Все споры разрешаются путем переговоров в досудебном порядке. Срок ответа на претензии – 10 календарных дней. Уведомление высылается в письменном виде заказным письмом или доставляется лично. Обмен документами при применении мер ответственности осуществляется с использованием ЕИС",\n    "10.2": "В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в Арбитражном суде Краснодарского края",\n    "11": "СРОК ДЕЙСТВИЯ, ПОРЯДОК ИЗМЕНЕНИЯ И РАСТОРЖЕНИЯ КОНТРАКТА (section heading)",\n    "11.1": "Контракт действует с даты заключения по 30 декабря 2025 года или до момента исчерпания предельной Цены Контракта. Окончание срока действия не освобождает Стороны от ответственности",\n    "11.2": "Любые изменения и дополнения к контракту имеют силу только если они оформлены в письменном виде и подписаны обеими Сторонами. В случае изменения места нахождения сторона обязана в течение двух дней письменно известить другую",\n    "11.3": "Расторжение контракта допускается по соглашению Сторон, по решению суда, в случае одностороннего отказа в соответствии с гражданским законодательством РФ",\n    "11.4": "Заказчик вправе принять решение об одностороннем отказе от исполнения контракта по основаниям предусмотренным ГК РФ",\n    "11.5": "Решение Сторон об одностороннем отказе от исполнения контракта принимается и реализуется в порядке и сроки предусмотренные статьей 95 Федерального закона № 44-ФЗ",\n    "11.6": "Изменение и(или) расторжение контракта осуществляется в порядке установленном статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ",\n    "11.7": "Во всем что не предусмотрено контрактом Стороны руководствуются действующим законодательством РФ",\n    "11.8": "Изменение существенных условий контракта при его исполнении не допускается за исключением случаев предусмотренных Федеральным законом № 44-ФЗ",\n    "12": "ПРОЧИЕ УСЛОВИЯ (section heading)",\n    "12.1": "При исполнении контракта не допускается перемена Исполнителя за исключением случая правопреемства вследствие реорганизации юридического лица",\n    "12.2": "В случае перемены Заказчика права и обязанности переходят к новому Заказчику в том же объеме и на тех же условиях",\n    "12.3": "По согласованию Заказчика с Исполнителем допускается оказание услуги качество которых являются улучшенными",\n    "12.4": "Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон",\n    "12.5": "Приложения: № 1 «Техническое задание», № 2 «Спецификация»",\n    "13": "МЕСТА НАХОЖДЕНИЯ, БАНКОВСКИЕ РЕКВИЗИТЫ СТОРОН (section heading - requisites)"\n}\n\n# Print summary\nfor cid, summary in batch2_clauses.items():\n    print(f"{cid}: {summary[:120]}...")\nPYEOF\n'}, 'id': 'call_00_cftBV2i2CX7H6TaSMP136977', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:10
[stderr] + python3 << 'PYEOF'
[stderr] +          ~
[stderr] Missing file specification after redirection operator.
[stderr] At line:32 char:9
[stderr] + python3 << 'PYEOF'
[stderr] +         ~
[stderr] The '<' operator is reserved for future use.
[stderr] At line:32 char:10
[stderr] + python3 << 'PYEOF'
[stderr] +          ~
[stderr] The '<' operator is reserved for future use.
[stderr] At line:38 char:15
[stderr] +     "5.3.18.2": "РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РёСЃРїРѕР»РЅРёС‚РµР»СЋ РґРѕСЃС‚СѓРї Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё  ...
[stderr] +               ~
[stderr] Unexpected token ':' in expression or statement.
[stderr] At line:123 char:4
[stderr] + for cid, summary in batch2_clauses.items():
[stderr] +    ~
[stderr] Missing opening '(' after keyword 'for'.
[stderr] At line:123 char:8
[stderr] + for cid, summary in batch2_clauses.items():
[stderr] +        ~
[stderr] Missing argument in parameter list.
[stderr] At line:123 char:42
[stderr] + for cid, summary in batch2_clauses.items():
[stderr] +                                          ~
[stderr] An expression was expected after '('.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : MissingFileSpecification

Exit code: 1
[Command failed with exit code 1]
AI: Let me use a different approach - write the script to a file first.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/batch2_analysis.py', 'content': 'import json\n\n# Load ...(argument truncated)'}, 'id': 'call_00_AcVRsswu5LC9iYn5NOoR1663', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/batch2_analysis.py
AI: [{'name': 'execute', 'args': {'command': 'cd / && python3 /outputs/working/batch2_analysis.py'}, 'id': 'call_00_6CbRgON9qo92R5FQECWy5008', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:6
[stderr] + cd / && python3 outputs/working/batch2_analysis.py
[stderr] +      ~~
[stderr] The token '&&' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/batch2_analysis.py'}, 'id': 'call_00_IyXMt8hIJcG6wsqSfaeL2363', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\batch2_analysis.py", line 4, in <module>
[stderr]     with open('/inputs/matrix.json', 'r') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/inputs/matrix.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import os; print(os.getcwd())"'}, 'id': 'call_00_yP19UKBa3B6c66bDFK448005', 'type': 'tool_call'}]
Tool: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2

[Command succeeded with exit code 0]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import os; print([f for f in os.listdir(\'.\') if not f.startswith(\'.\')][:20])"'}, 'id': 'call_00_JTUvPzhY8ZIoopuEoQpr7762', 'type': 'tool_call'}]
Tool: ['ALL_DATA', 'conversation_history', 'inputs', 'llm.py', 'main.py', 'output', 'outputs', 'README.md', 'results', 'runs', 'skills', 'tools', '__pycache__']

[Command succeeded with exit code 0]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/batch2_analysis.py', 'old_string': "with open('/inputs/matrix.json', 'r') as f:", 'new_string': "with open('inputs/matrix.json', 'r') as f:"}, 'id': 'call_00_dFpNiSTRPOWHSt2IAYhX0105', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/batch2_analysis.py'
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/batch2_analysis.py'}, 'id': 'call_00_eVOIBk5E9yMx7J08p7SY7885', 'type': 'tool_call'}]
Tool: === MATRIX APPLICABILITY ===
Applicable: 133
Not applicable: 36

Not applicable items:
  2.5.1.1 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  2.5.2.1 (product=trade_acquiring, lot=common, terminal=common, pm=sber_pay_face_scan)
  2.6.1.1 (product=trade_acquiring, lot=common, terminal=smart, pm=qr)
  4.1.3 (product=trade_acquiring, lot=common, terminal=common, pm=qr_sber_pay)
  4.2.3 (product=common, lot=fz_223, terminal=common, pm=common)
  4.2.17 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.1 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.2 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.3 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.4 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.5 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.6 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.7 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.8 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.26 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.1.8.4 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.1.8.5 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.1.17.2 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  5.2.1 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.2.2 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.2.12 (product=internet_acquiring, lot=common, terminal=common, pm=qr)
  6.3 (product=common, lot=fz_223, terminal=common, pm=common)
  6.6 (product=common, lot=fz_223, terminal=common, pm=common)
  6.7 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.8 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.9 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  6.10 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.11 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.12 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  6.13 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.14 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.15 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  6.16 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.17 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.18 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  7.13 (product=internet_acquiring, lot=common, terminal=common, pm=common)

=== BATCH 2 CONTRACT CLAUSES AND MATRIX MATCHING ===

[stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\batch2_analysis.py", line 648, in <module>
[stderr]     with open('/outputs/working/batch2_matches.json', 'w', encoding='utf-8') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/batch2_matches.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/batch2_analysis.py', 'old_string': "with open('/outputs/working/batch2_matches.json', 'w', encoding='utf-8') as f:", 'new_string': "with open('outputs/working/batch2_matches.json', 'w', encoding='utf-8') as f:"}, 'id': 'call_00_RxUKCq6JjDqc3l09lyrR1419', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/batch2_analysis.py'
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/batch2_analysis.py'}, 'id': 'call_00_guoBcJmIQIimJOVL4JFd5555', 'type': 'tool_call'}]
Tool: === MATRIX APPLICABILITY ===
Applicable: 133
Not applicable: 36

Not applicable items:
  2.5.1.1 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  2.5.2.1 (product=trade_acquiring, lot=common, terminal=common, pm=sber_pay_face_scan)
  2.6.1.1 (product=trade_acquiring, lot=common, terminal=smart, pm=qr)
  4.1.3 (product=trade_acquiring, lot=common, terminal=common, pm=qr_sber_pay)
  4.2.3 (product=common, lot=fz_223, terminal=common, pm=common)
  4.2.17 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.1 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.2 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.3 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.4 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.5 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.6 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.7 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.21.8 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  4.2.26 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.1.8.4 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.1.8.5 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.1.17.2 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  5.2.1 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.2.2 (product=internet_acquiring, lot=common, terminal=common, pm=common)
  5.2.12 (product=internet_acquiring, lot=common, terminal=common, pm=qr)
  6.3 (product=common, lot=fz_223, terminal=common, pm=common)
  6.6 (product=common, lot=fz_223, terminal=common, pm=common)
  6.7 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.8 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.9 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  6.10 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.11 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.12 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  6.13 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.14 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.15 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  6.16 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.17 (product=trade_acquiring, lot=common, terminal=smart, pm=common)
  6.18 (product=trade_acquiring, lot=fz_223, terminal=smart, pm=common)
  7.13 (product=internet_acquiring, lot=common, terminal=common, pm=common)

=== BATCH 2 CONTRACT CLAUSES AND MATRIX MATCHING ===

Total matches: 56
Aligned: 28
Deviation: 5
Extra in contract: 23

[Command succeeded with exit code 0]
AI: Good. Now let me refine the analysis. I need to also check for matrix items that are missing from the contract (unmatched_matrix). Let me also review the matches more carefully and produce the final working output.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read and understand all contract clauses in batch 2 scope (5.3.18.2 to end)', 'status': 'completed'}, {'content': 'Read full matrix.json to understand all matrix requirements', 'status': 'completed'}, {'content': 'Create legal propositions for batch 2 contract clauses and perform bidirectional matching', 'status': 'completed'}, {'content': 'Assign group-level status (aligned/deviation/missing/extra) - refine and validate', 'status': 'in_progress'}, {'content': 'Build coverage ledger and closure QA', 'status': 'pending'}, {'content': 'Write batch 2 working output files', 'status': 'pending'}, {'content': 'Return compact JSON fragments and summary', 'status': 'pending'}]}, 'id': 'call_00_v28da5WsyMTEAK9M2cBG6428', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read and understand all contract clauses in batch 2 scope (5.3.18.2 to end)', 'status': 'completed'}, {'content': 'Read full matrix.json to understand all matrix requirements', 'status': 'completed'}, {'content': 'Create legal propositions for batch 2 contract clauses and perform bidirectional matching', 'status': 'completed'}, {'content': 'Assign group-level status (aligned/deviation/missing/extra) - refine and validate', 'status': 'in_progress'}, {'content': 'Build coverage ledger and closure QA', 'status': 'pending'}, {'content': 'Write batch 2 working output files', 'status': 'pending'}, {'content': 'Return compact JSON fragments and summary', 'status': 'pending'}]
AI: Now let me refine the analysis. I need to check which matrix items from the applicable set are NOT covered by any contract clause in batch 2. Let me also review the deviations more carefully and check for missing matrix items.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/batch2_refine.py', 'content': 'import json\n\n# Load matrix\nwith open(\'inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\n\n# Load batch 2 matches\nwith open(\'outputs/working/batch2_matches.json\', \'r\') as f:\n    batch2 = json.load(f)\n\n# Profile\nprofile = {\n    "product": ["trade_acquiring"],\n    "lot": "44_fz",\n    "terminal": ["pos"],\n    "payment_method": ["card", "qr"],\n    "legal_regime": "44_fz"\n}\n\ndef is_applicable(item, profile):\n    pf = item.get(\'only_for_product\', \'common\')\n    lf = item.get(\'only_for_lot\', \'common\')\n    tf = item.get(\'only_for_terminal\', \'common\')\n    pmf = item.get(\'payment_method\', \'common\')\n    \n    if pf != \'common\':\n        if pf == \'internet_acquiring\' and \'internet_acquiring\' not in profile[\'product\']:\n            return False\n        if pf == \'trade_acquiring\' and \'trade_acquiring\' not in profile[\'product\']:\n            return False\n    \n    if lf != \'common\':\n        if lf == \'fz_44\' and profile[\'lot\'] != \'44_fz\':\n            return False\n        if lf == \'fz_223\' and profile[\'lot\'] != \'223_fz\':\n            return False\n    \n    if tf != \'common\':\n        if tf == \'smart\' and \'smart\' not in profile[\'terminal\']:\n            return False\n        if tf == \'pos\' and \'pos\' not in profile[\'terminal\']:\n            return False\n    \n    if pmf != \'common\':\n        if pmf not in profile[\'payment_method\']:\n            return False\n    \n    return True\n\n# Get all matrix ids covered in batch 2\ncovered_matrix_ids = set()\nfor m in batch2[\'matches\']:\n    for mid in m[\'matrix_ids\']:\n        covered_matrix_ids.add(mid)\n\nprint("Matrix IDs covered in batch 2:")\nfor mid in sorted(covered_matrix_ids):\n    print(f"  {mid}")\n\n# Now find applicable matrix items NOT covered by batch 2\n# These would be items that should be matched to contract clauses in batch 1 or are genuinely missing\napplicable_ids = set()\nfor item in matrix:\n    if is_applicable(item, profile):\n        applicable_ids.add(item[\'number\'])\n\n# Items covered in batch 1 (from matrix_batch_01 through matrix_batch_04)\nbatch1_covered = set()\nfor batch_file in [\'outputs/working/matrix_batch_01.json\', \'outputs/working/matrix_batch_02.json\', \n                    \'outputs/working/matrix_batch_03.json\', \'outputs/working/matrix_batch_04.json\']:\n    with open(batch_file, \'r\') as f:\n        batch1_covered.update(json.load(f))\n\nprint(f"\\nApplicable matrix items: {len(applicable_ids)}")\nprint(f"Covered in batch 1 (matrix batches): {len(batch1_covered)}")\nprint(f"Covered in batch 2: {len(covered_matrix_ids)}")\n\n# Items not in any batch\nall_covered = batch1_covered | covered_matrix_ids\nuncovered = applicable_ids - all_covered\nprint(f"\\nUncovered applicable matrix items: {len(uncovered)}")\nfor uid in sorted(uncovered):\n    item = next((i for i in matrix if i[\'number\'] == uid), None)\n    if item:\n        print(f"  {uid}: {item.get(\'main_idea\', \'\')[:100]}")\n\n# Now let\'s also check which matrix items from batch 2 coverage are actually \n# in the batch 1 matrix batches (they shouldn\'t be double-counted)\noverlap = covered_matrix_ids & batch1_covered\nprint(f"\\nOverlap between batch 1 and batch 2 matrix coverage: {len(overlap)}")\nfor oid in sorted(overlap):\n    print(f"  {oid}")\n\n# Check which contract clauses in batch 2 are NOT matched to any matrix\ncontract_ids_in_batch2 = set()\nwith open(\'outputs/working/contract_batch_02.json\', \'r\') as f:\n    contract_ids_in_batch2 = set(json.load(f))\n\nmatched_contract_ids = set(m[\'contract_id\'] for m in batch2[\'matches\'])\nunmatched_contract = contract_ids_in_batch2 - matched_contract_ids\nprint(f"\\nContract clauses in batch 2 NOT matched: {len(unmatched_contract)}")\nfor cid in sorted(unmatched_contract):\n    print(f"  {cid}")\n'}, 'id': 'call_00_ti4QivZr7fRz2Hv6t8aD9953', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/batch2_refine.py
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/batch2_refine.py'}, 'id': 'call_00_LGsXKhbbZmo6W1V0SDzj5855', 'type': 'tool_call'}]
Tool: Matrix IDs covered in batch 2:
  10.1
  10.2
  11.13
  11.4
  11.7
  11.9
  2.7
  4.1.1
  4.1.2
  4.2.11
  4.2.13
  4.2.16.1
  4.2.20.1
  4.2.20.3
  4.2.20.4
  4.2.20.5
  4.2.20.6
  4.2.20.7
  5.1.1.6
  6.2
  6.3
  6.4
  7.1
  7.16
  7.2
  7.3
  7.4
  7.5
  7.6
  7.7
  8.1
  8.2
  9.1
  9.2
  9.3

[stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\batch2_refine.py", line 71, in <module>
[stderr]     with open(batch_file, 'r') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: 'outputs/working/matrix_batch_04.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "import os; print(os.listdir(\'outputs/working\'))"'}, 'id': 'call_00_jebHq3jeSXqGCUu9rY697024', 'type': 'tool_call'}]
Tool: ['batch2_analysis.py', 'batch2_matches.json', 'batch2_refine.py', 'batch_01_analysis.json', 'batch_03_analysis.py', 'build_analysis.py', 'build_clause_index.py', 'build_legal_propositions.py', 'check_applicability.py', 'clause_index.json', 'contract_batch_01.json', 'contract_batch_02.json', 'contract_product_profile.json', 'coverage_ledger_batch_02.json', 'extract_contract_sections.py', 'legal_propositions.json', 'list_applicable.py', 'matrix_batch_01.json', 'matrix_batch_02.json', 'matrix_batch_02_results.json', 'matrix_batch_03.json', 'matrix_batch_03_full.json', 'source_preflight.json']

[Command succeeded with exit code 0]
AI: I see - there's no matrix_batch_04.json. Let me check what's in the existing batch files and the coverage_ledger_batch_02.json.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/coverage_ledger_batch_02.json', 'limit': 50}, 'id': 'call_00_oXLUx5QaEu01if5UC9So5614', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/batch_01_analysis.json', 'limit': 50}, 'id': 'call_01_BzXEobQSljJceZzP238d1867', 'type': 'tool_call'}]
Tool:      1	{
     2	  "batch": "02",
     3	  "matrix": [
     4	    {"matrix_id": "4.2.18", "closure": "linked", "link_indices": [0], "reason": "Прямой аналог: п. 5.3.16 контракта."},
     5	    {"matrix_id": "4.2.19", "closure": "linked", "link_indices": [1], "reason": "Прямой аналог: п. 5.3.17 контракта."},
     6	    {"matrix_id": "4.2.20.1", "closure": "linked", "link_indices": [2], "reason": "Deviation: URL инструктажа не заполнен (placeholder)."},
     7	    {"matrix_id": "4.2.20.2", "closure": "linked", "link_indices": [3], "reason": "Прямой аналог: п. 5.3.18.1 контракта."},
     8	    {"matrix_id": "4.2.20.3", "closure": "linked", "link_indices": [4], "reason": "Прямой аналог: п. 5.3.18.2 контракта."},
     9	    {"matrix_id": "4.2.20.4", "closure": "linked", "link_indices": [5], "reason": "Прямой аналог: п. 5.3.18.3 контракта."},
    10	    {"matrix_id": "4.2.20.5", "closure": "linked", "link_indices": [6], "reason": "Прямой аналог: п. 5.3.20.4 контракта."},
    11	    {"matrix_id": "4.2.20.6", "closure": "linked", "link_indices": [7], "reason": "Прямой аналог: п. 5.3.18.5 контракта."},
    12	    {"matrix_id": "4.2.20.7", "closure": "linked", "link_indices": [8], "reason": "Deviation: штраф за Электронный терминал 10 000 вместо 25 000 руб."},
    13	    {"matrix_id": "4.2.21.1", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    14	    {"matrix_id": "4.2.21.2", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    15	    {"matrix_id": "4.2.21.3", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    16	    {"matrix_id": "4.2.21.4", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    17	    {"matrix_id": "4.2.21.5", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    18	    {"matrix_id": "4.2.21.6", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    19	    {"matrix_id": "4.2.21.7", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    20	    {"matrix_id": "4.2.21.8", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    21	    {"matrix_id": "4.2.22", "closure": "missing_in_contract", "link_indices": [], "reason": "Опциональное. QR-код упоминается как тех. возможность, но нет обязанности SberPayQR/Плати QR."},
    22	    {"matrix_id": "4.2.23", "closure": "missing_in_contract", "link_indices": [], "reason": "Опциональное. Прямой аналог отсутствует."},
    23	    {"matrix_id": "4.2.24", "closure": "missing_in_contract", "link_indices": [], "reason": "Опциональное. QR-API упоминается как опция, но нет operative clause."},
    24	    {"matrix_id": "4.2.25", "closure": "missing_in_contract", "link_indices": [], "reason": "Опциональное. Прямой аналог отсутствует."},
    25	    {"matrix_id": "4.2.26", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    26	    {"matrix_id": "5.1.1.1", "closure": "linked", "link_indices": [9], "reason": "Прямой аналог: п. 5.2.10.1 контракта (все 12 оснований)."},
    27	    {"matrix_id": "5.1.1.2", "closure": "linked", "link_indices": [10], "reason": "Прямой аналог: п. 5.2.10.2 контракта."},
    28	    {"matrix_id": "5.1.1.3", "closure": "linked", "link_indices": [11], "reason": "Прямой аналог: п. 5.2.10.3 контракта."},
    29	    {"matrix_id": "5.1.1.4", "closure": "linked", "link_indices": [12], "reason": "Прямой аналог: п. 5.2.10.4 контракта."},
    30	    {"matrix_id": "5.1.1.5", "closure": "linked", "link_indices": [13], "reason": "Прямой аналог: п. 5.2.10.5 контракта."},
    31	    {"matrix_id": "5.1.1.6", "closure": "linked", "link_indices": [14], "reason": "Функционально покрыто: штраф в п. 5.7, удержание через 5.2.10."},
    32	    {"matrix_id": "5.1.2", "closure": "missing_in_contract", "link_indices": [], "reason": "Обязательное. Задолженность не указана как основание приостановки авторизации в п. 5.2.9."},
    33	    {"matrix_id": "5.1.3", "closure": "linked", "link_indices": [15], "reason": "Прямой аналог: Приложение №1.1 п.1.3."},
    34	    {"matrix_id": "5.1.4", "closure": "missing_in_contract", "link_indices": [], "reason": "Обязательное. Механизм счета/платежного требования отсутствует (есть только заранее данный акцепт)."},
    35	    {"matrix_id": "5.1.5", "closure": "linked", "link_indices": [16], "reason": "Функционально покрыто через 5.2.10.1 (недействительные операции не возмещаются)."},
    36	    {"matrix_id": "5.1.6", "closure": "linked", "link_indices": [17], "reason": "Прямой аналог: п. 5.2.3 и 5.2.4 контракта."},
    37	    {"matrix_id": "5.1.7", "closure": "missing_in_contract", "link_indices": [], "reason": "Обязательное. Право передачи данных в ПС МИР отсутствует."},
    38	    {"matrix_id": "5.1.8.1", "closure": "linked", "link_indices": [18], "reason": "Прямой аналог: п. 5.2.9.1 контракта."},
    39	    {"matrix_id": "5.1.8.2", "closure": "linked", "link_indices": [19], "reason": "Прямой аналог: п. 5.2.9.2 контракта."},
    40	    {"matrix_id": "5.1.8.3", "closure": "linked", "link_indices": [20], "reason": "Прямой аналог: п. 5.2.9.3 контракта."},
    41	    {"matrix_id": "5.1.8.4", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    42	    {"matrix_id": "5.1.8.5", "closure": "missing_in_contract", "link_indices": [], "reason": "Неприменимо: internet_acquiring отсутствует в контракте."},
    43	    {"matrix_id": "5.1.8.6", "closure": "linked", "link_indices": [21], "reason": "Прямой аналог: п. 5.2.9.4 контракта."},
    44	    {"matrix_id": "5.1.8.7", "closure": "linked", "link_indices": [22], "reason": "Прямой аналог: п. 5.2.9.5 контракта."},
    45	    {"matrix_id": "5.1.8.8", "closure": "linked", "link_indices": [23], "reason": "Прямой аналог: п. 5.2.9.6 контракта."},
    46	    {"matrix_id": "5.1.8.9", "closure": "linked", "link_indices": [24], "reason": "Прямой аналог: п. 5.2.9.7 контракта."}
    47	  ],
    48	  "contract": [
    49	    {"contract_id": "5.3.16", "closure": "linked", "link_indices": [0], "reason": "Покрывает матрицу 4.2.18."},
    50	    {"contract_id": "5.3.17", "closure": "linked", "link_indices": [1], "reason": "Покрывает матрицу 4.2.19."},
Tool:      1	{
     2	  "batch": "01",
     3	  "matrix_ids": ["2.1","2.2","2.3.1","2.3.2","2.3.3","2.3.4","2.3.5","2.3.6","2.3.7","2.4","2.5.1.1","2.5.2.1","2.6.1.1","2.6.2.1","2.6.2.2","2.6.3.1","2.6.3.2","2.7","3.1","3.2","3.3","4.1.1","4.1.2","4.1.3","4.2.1","4.2.2","4.2.3","4.2.4","4.2.5","4.2.6","4.2.7","4.2.8","4.2.9","4.2.10","4.2.11","4.2.12","4.2.13","4.2.14","4.2.15","4.2.16.1","4.2.16.2","4.2.16.3","4.2.17"],
     4	  "product_profile": {
     5	    "product": ["trade_acquiring"],
     6	    "lot": "44_fz",
     7	    "terminal": ["pos"],
     8	    "payment_method": ["card", "qr"],
     9	    "legal_regime": "44_fz"
    10	  },
    11	  "links": [
    12	    {
    13	      "matrix_ids": ["2.1"],
    14	      "contract_ids": ["4.3"],
    15	      "relationship": "deviation",
    16	      "legal_topic": "Регистрация новой ТСТ и право Банка на отказ",
    17	      "matrix_standard": "Для регистрации новой ТСТ Предприятие предоставляет Заявление и Информацию о ТСТ по формам Приложений 1 и 1.1. Банк вправе отказать в регистрации ТСТ без объяснения причин с уведомлением по п.2.3. При изменении информации о ТСТ Предприятие предоставляет обновленную информацию.",
    18	      "contract_position": "П.4.3: Заказчик после заключения контракта предоставляет Исполнителю заявление и информацию о ТСТ, подписанную уполномоченным представителем. Не указаны конкретные формы приложений. Отсутствует право Банка отказать в регистрации ТСТ без объяснения причин.",
    19	      "status_reason": "Контракт содержит обязанность Заказчика предоставить заявление и информацию о ТСТ (п.4.3), но: (1) не указаны конкретные формы Приложений 1 и 1.1; (2) отсутствует право Банка отказать в регистрации ТСТ без объяснения причин — это существенное отсутствие права Банка.",
    20	      "risk_level": "high",
    21	      "discrepancies": [
    22	        {
    23	          "type": "right",
    24	          "description": "Отсутствует право Банка отказать в регистрации ТСТ без объяснения причин. Матрица даёт Банку безусловное право отказа, контракт такого права не содержит.",
    25	          "risk": "Банк не может отказать в регистрации ТСТ без объяснения причин, что ограничивает контроль Банка над регистрацией новых ТСТ."
    26	        },
    27	        {
    28	          "type": "procedure",
    29	          "description": "Не указаны конкретные формы Приложений 1 и 1.1 для заявления и информации о ТСТ.",
    30	          "risk": "Отсутствие стандартизированных форм может привести к неполноте предоставляемой информации."
    31	        }
    32	      ]
    33	    },
    34	    {
    35	      "matrix_ids": ["2.2"],
    36	      "contract_ids": ["5.1.8", "Приложение_1_п5"],
    37	      "relationship": "aligned",
    38	      "legal_topic": "Валюта расчетов — рубли РФ",
    39	      "matrix_standard": "Расчеты с Предприятием по Операциям осуществляются в рублях Российской Федерации.",
    40	      "contract_position": "П.5.1.8: перечисление сумм Операций оплаты в валюте проведения операции (рубли РФ). Приложение №1 п.5: «Расчеты при совершении операций производятся в валюте Российской Федерации.»",
    41	      "status_reason": "Контракт прямо устанавливает рубли РФ в качестве валюты расчетов — п.5.1.8 и Приложение №1 п.5. Требование матрицы полностью покрыто.",
    42	      "risk_level": "none",
    43	      "discrepancies": []
    44	    },
    45	    {
    46	      "matrix_ids": ["2.3.1"],
    47	      "contract_ids": ["2.3.1"],
    48	      "relationship": "aligned",
    49	      "legal_topic": "Обмен информацией по электронной почте с юридической силой",
    50	      "matrix_standard": "Обмен через электронную почту с адресов, указанных в Заявлении/Информации о ТСТ. Исключение: персональные данные, коммерческая и банковская тайна. Документы по email имеют полную юридическую силу.",

