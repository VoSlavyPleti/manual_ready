## Summarized at 2026-06-25T15:12:03.165177+00:00

Human: Matrix coverage batch 03 (ids 4.2.17-5.1.8.13)
AI: I'll start by reading the skill file and understanding the scope of work, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_1umNn2KkXtmtLSyjJSRW8040', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/*', 'path': '/'}, 'id': 'call_01_rQrmrhnfIdlzquIzg1ql8860', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-discrepancy-analysis
     3	description: "Build a complete JSON coverage artifact for comparing a bank acquiring matrix with a counterparty acquiring contract."
     4	---
     5	
     6	# Acquiring Discrepancy Analysis
     7	
     8	Use this skill to produce one complete JSON artifact for matrix-contract
     9	coverage analysis. At this stage, prioritize a stable end-to-end pipeline over
    10	fine legal calibration. Do not stop after partial batch files.
    11	
    12	Read `references/output-contract.md` before writing the final JSON.
    13	
    14	## Inputs
    15	
    16	- `inputs/matrix.json`: Bank matrix. Use `number` as the matrix id.
    17	- `inputs/contract.txt`: counterparty contract text. Use only ids visible in
    18	  this file.
    19	
    20	## Required Final Output
    21	
    22	- `/outputs/discrepancy_analysis.json`
    23	
    24	Do not create alternative final JSON files. Intermediate files are allowed only
    25	under `/outputs/working/`.
    26	
    27	## Pipeline Contract
    28	
    29	Complete the stages below in order. Each stage must leave the expected artifact
    30	before moving to the next stage.
    31	
    32	### Stage 1. Source Preflight
    33	
    34	Goal: confirm the input text is usable.
    35	
    36	Actions:
    37	
    38	1. Check that `inputs/contract.txt` contains visible numbered clauses.
    39	2. If numbering is unusable, write `/outputs/working/source_preflight_error.json`
    40	   and stop.
    41	3. Otherwise write `/outputs/working/source_preflight.json`.
    42	
    43	Expected artifact:
    44	
    45	```json
    46	{
    47	  "contract_numbering_valid": true,
    48	  "notes": []
    49	}
    50	```
    51	
    52	You may use:
    53	
    54	```bash
    55	python skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py inputs/contract.txt --json-out outputs/working/source_preflight.json
    56	```
    57	
    58	### Stage 2. Source Index
    59	
    60	Goal: build a complete mechanical source map.
    61	
    62	Actions:
    63	
    64	1. Create `/outputs/working/clause_index.json`.
    65	2. Create `/outputs/working/legal_propositions.json`.
    66	3. Create `/outputs/working/contract_product_profile.json`.
    67	4. Validate the working source artifacts before analysis.
    68	
    69	Use the bundled bootstrap helper unless you have a better mechanical parser:
    70	
    71	```bash
    72	python skills/acquiring-discrepancy-analysis/scripts/bootstrap_source_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/bootstrap_report.json
    73	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/working_artifact_validation.json
    74	```
    75	
    76	`clause_index.json` is a source map, not the legal answer. Do not overwrite it
    77	with a batch subset.
    78	
    79	### Stage 3. Matrix Coverage Draft
    80	
    81	Goal: give every matrix item an initial closure.
    82	
    83	Actions:
    84	
    85	1. Split matrix ids into manageable batches.
    86	2. For each matrix id, either identify contract ids that appear legally related
    87	   or mark the item as currently unmatched.
    88	3. Write batch artifacts under `/outputs/working/`.
    89	
    90	Suggested artifact names:
    91	
    92	- `/outputs/working/matrix_batch_01.json`
    93	- `/outputs/working/matrix_batch_02.json`
    94	- `/outputs/working/matrix_batch_03.json`
    95	- `/outputs/working/matrix_batch_04.json`
    96	
    97	Each batch artifact should use this shape:
    98	
    99	```json
   100	{
   101	  "links": [],
   102	  "unmatched_matrix": [],
   103	  "notes": []
   104	}
   105	```
   106	
   107	At skeleton stage, a conservative imperfect legal call is acceptable. A missing
   108	final artifact is not acceptable.
   109	
   110	### Stage 4. Contract Coverage Draft
   111	
   112	Goal: give every material contract clause an initial closure.
   113	
   114	Actions:
   115	
   116	1. Review contract clauses from `clause_index.json`.
   117	2. For each material clause, either link it to matrix ids or mark it as
   118	   `extra_in_contract`.
   119	3. Keep definitions, headings, requisites, signatures, and purely technical
   120	   rows out of final `unmatched_contract`.
   121	
   122	Suggested artifact names:
   123	
   124	- `/outputs/working/contract_batch_01.json`
   125	- `/outputs/working/contract_batch_02.json`
   126	
   127	Each contract batch should use this shape:
   128	
   129	```json
   130	{
   131	  "links": [],
   132	  "unmatched_contract": [],
   133	  "notes": []
   134	}
   135	```
   136	
   137	### Stage 5. Reconciliation Draft
   138	
   139	Goal: merge both directions into one coherent graph.
   140	
   141	Actions:
   142	
   143	1. Start this stage only after the matrix coverage draft and contract coverage
   144	   draft are complete or explicitly documented as empty.
   145	2. Do not write `/outputs/discrepancy_analysis.json` before this stage.
   146	3. Combine matrix-side and contract-side batch links.
   147	4. Remove invalid ids.
   148	5. Keep `missing_in_contract` only in `unmatched_matrix`, never in `links`.
   149	6. Keep `extra_in_contract` only in `unmatched_contract`, never as a link
   150	   relationship.
   151	7. Recompute `atomic_links`, `coverage_ledger`, and `summary`.
   152	
   153	If manual reconciliation is incomplete, run the mechanical finalizer to create a
   154	draft final JSON:
   155	
   156	```bash
   157	python skills/acquiring-discrepancy-analysis/scripts/finalize_discrepancy_json.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --final outputs/discrepancy_analysis.json
   158	```
   159	
   160	The finalizer is allowed as a safety net. It must not replace substantive
   161	analysis when batch findings exist; it preserves valid findings and closes
   162	missing rows mechanically.
   163	
   164	### Stage 6. Acceptance QA
   165	
   166	Goal: decide whether the merged JSON is the accepted final artifact or only a
   167	draft that needs one mechanical repair pass.
   168	
   169	The first `/outputs/discrepancy_analysis.json` is a draft until validation
   170	passes. Do not treat every post-merge check as a new analysis stage. Use this
   171	stage only to catch structural failures and dropped batch work.
   172	
   173	Actions:
   174	
   175	1. Validate that the final JSON exists and has the required top-level keys.
   176	2. Validate that no `missing_in_contract` rows are placed inside `links`.
   177	3. Validate that no `extra_in_contract` rows are placed inside `links`.
   178	4. Validate that summary counts match arrays.
   179	5. Validate that matrix ids and contract ids are source-grounded.
   180	6. If a planned batch clearly produced findings that are absent from the JSON,
   181	   merge those findings mechanically and rerun validation once.
   182	
   183	Expected artifacts:
   184	
   185	- `/outputs/working/final_validation.json`
   186	- updated `/outputs/discrepancy_analysis.json` only if QA repaired structural
   187	  or dropped-fragment defects.
   188	
   189	After final validation succeeds, stop. Do not continue improving legal quality
   190	inside the same run. Legal quality improvements happen in later iterations
   191	after the produced artifact is evaluated.
   192	
   193	Use:
   194	
   195	```bash
   196	python skills/acquiring-discrepancy-analysis/scripts/validate_coverage_ledger.py outputs/discrepancy_analysis.json --matrix inputs/matrix.json --contract inputs/contract.txt --json-out outputs/working/final_validation.json
   197	```
   198	
   199	## Minimal Status Semantics
   200	
   201	Use only these final statuses:
   202	
   203	- `aligned`: a matrix requirement and contract package appear to match.
   204	- `deviation`: a related contract package exists but appears materially
   205	  different.
   206	- `missing_in_contract`: a matrix requirement has no contract analogue.
   207	- `extra_in_contract`: a material contract clause has no matrix analogue.
   208	
   209	At this stage, keep reasoning short and source-grounded. Detailed business
   210	logic and calibration examples can be added in later iterations after the
   211	pipeline reliably produces a final JSON.
   212	
   213	## Final JSON Requirements
   214	
   215	The final JSON must contain these top-level keys:
   216	
   217	- `analysis_profile`
   218	- `links`
   219	- `atomic_links`
   220	- `unmatched_matrix`
   221	- `unmatched_contract`
   222	- `coverage_ledger`
   223	- `summary`
   224	
   225	Rules:
   226	
   227	- `links[].relationship` is only `aligned` or `deviation`.
   228	- `links[].matrix_ids` and `links[].contract_ids` are non-empty arrays.
   229	- `unmatched_matrix[].status` is `missing_in_contract`.
   230	- `unmatched_contract[].status` is `extra_in_contract`.
   231	- `summary` counts must equal the final arrays.
   232	- All matrix ids come from `inputs/matrix.json`.
   233	- All contract ids are visible in `inputs/contract.txt`.
   234	
   235	## Completion Checklist
   236	
   237	Finish only when all are true:
   238	
   239	- `source_preflight.json` exists or a clear source error artifact exists.
   240	- `clause_index.json` exists and validates.
   241	- Matrix batch artifacts exist.
   242	- Contract batch artifacts exist or contract review is documented as empty.
   243	- `/outputs/discrepancy_analysis.json` exists.
   244	- Final validation report exists under `/outputs/working/`.
   245	- The final answer is a single JSON artifact, not competing partial files.
Tool: ['/.env', '/.git/COMMIT_EDITMSG', '/.git/FETCH_HEAD', '/.git/HEAD', '/.git/ORIG_HEAD', '/.git/config', '/.git/description', '/.git/hooks/applypatch-msg.sample', '/.git/hooks/commit-msg.sample', '/.git/hooks/fsmonitor-watchman.sample', '/.git/hooks/post-update.sample', '/.git/hooks/pre-applypatch.sample', '/.git/hooks/pre-commit.sample', '/.git/hooks/pre-merge-commit.sample', '/.git/hooks/pre-push.sample', '/.git/hooks/pre-rebase.sample', '/.git/hooks/pre-receive.sample', '/.git/hooks/prepare-commit-msg.sample', '/.git/hooks/push-to-checkout.sample', '/.git/hooks/sendemail-validate.sample', '/.git/hooks/update.sample', '/.git/index', '/.git/info/exclude', '/.git/logs/HEAD', '/.git/logs/refs/heads/clear-branch', '/.git/logs/refs/heads/codex/clear_one_skill', '/.git/logs/refs/heads/demo', '/.git/logs/refs/heads/main', '/.git/logs/refs/heads/one_skill', '/.git/logs/refs/heads/pre=agent', '/.git/logs/refs/heads/test', '/.git/logs/refs/heads/test2', '/.git/logs/refs/heads/test3', '/.git/logs/refs/remotes/origin/HEAD', '/.git/logs/refs/remotes/origin/clear-branch', '/.git/logs/refs/remotes/origin/demo', '/.git/logs/refs/remotes/origin/main', '/.git/logs/refs/remotes/origin/one_skill', '/.git/logs/refs/remotes/origin/pre=agent', '/.git/logs/refs/remotes/origin/test', '/.git/logs/refs/remotes/origin/test2', '/.git/logs/refs/remotes/origin/test3', '/.git/lost-found/other/003f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/lost-found/other/016411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/lost-found/other/0189548f4f27fcb26840150f585a64515d77c26d', '/.git/lost-found/other/01a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/lost-found/other/02e3706e34f211187bd64efa7a9ad51760195d39', '/.git/lost-found/other/02e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/lost-found/other/0312d61983ef80179bfac79abbba1359052f115c', '/.git/lost-found/other/040be927181b9604d69593ffe36ab7303b1a94bc', '/.git/lost-found/other/04378a998f4a8686eb28f62e8833b0f539229714', '/.git/lost-found/other/04602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/lost-found/other/048703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/lost-found/other/0488481d528674a76807703e6625d6284ca8293e', '/.git/lost-found/other/04eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/lost-found/other/057e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/lost-found/other/05c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/lost-found/other/05e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/lost-found/other/0631461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/lost-found/other/074930d053a799cc4f9095e89196437f704205d6', '/.git/lost-found/other/077efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/lost-found/other/07d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/lost-found/other/082169d84ac7751152d7134fa37292c00ba029d0', '/.git/lost-found/other/0846bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/lost-found/other/0a05a2808a79fe98d007bccb3b1060551300dec8', '/.git/lost-found/other/0a32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/lost-found/other/0a401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/lost-found/other/0a56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/lost-found/other/0a962ce910aa746587b34755922bae542449fba9', '/.git/lost-found/other/0b32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/lost-found/other/0b5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/lost-found/other/0bc5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/lost-found/other/0bebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/lost-found/other/0bf720f21f41ce829add4aab5a9a05012208c3f7', '/.git/lost-found/other/0c4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/lost-found/other/0d72d0b2349a404cc4cddb87c836194765377d74', '/.git/lost-found/other/0d753acfba917272cd72f418e9c1352ed20054f6', '/.git/lost-found/other/0e189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/lost-found/other/0f0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/lost-found/other/0f86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/lost-found/other/0f9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/lost-found/other/108486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/lost-found/other/1152abac92eac8d8b605f61e7608e5151d222f07', '/.git/lost-found/other/11b6a93338766923a8e6379405e6fcf4ab828169', '/.git/lost-found/other/11c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/lost-found/other/13360394a41c8fabc39419ab404191a8575e2799', '/.git/lost-found/other/14394b47e18f572003e3d82368702dfd474b70c4', '/.git/lost-found/other/1474c8f7cf8bc22cda503322795cac94ac621675', '/.git/lost-found/other/159a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/lost-found/other/159bfd26b659195df8c8486d12b5e15f948cb808', '/.git/lost-found/other/15be2e474eb938a89e4d7c19737994893197e781', '/.git/lost-found/other/163d050dd4db671d29be7efff1a35864f91ca61d', '/.git/lost-found/other/1645e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/lost-found/other/1683c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/lost-found/other/16de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/lost-found/other/17a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/lost-found/other/17c6782b615441baeb457ee93a458ed7371c9f99', '/.git/lost-found/other/1862eec0af25e420dee69a16ba235f610f20756d', '/.git/lost-found/other/1876a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/lost-found/other/18d512a4ebe9f93cc357a19059984b3398799bee', '/.git/lost-found/other/18fe30c098f75b96caa54450040279f8727780ea', '/.git/lost-found/other/19928324ad53403e47456f49785dd300a6abc1e0', '/.git/lost-found/other/19ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/lost-found/other/1a3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/lost-found/other/1a412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/lost-found/other/1ae3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/lost-found/other/1bb6184cbc8ec7b0b92597da642ddb7baea3f9f0', '/.git/lost-found/other/1bb94dc37fa7ba202e37fb9f730b2c1ffe60c9f8', '/.git/lost-found/other/1bd948006afad9d92ba0af0d9d6aac84b81201ee', '/.git/lost-found/other/1c5c64af7a4a179928feb3e438ba9aeca2b21785', '/.git/lost-found/other/1c6f0d2fcead6d6b9af167efe84b68ab9867253d', '/.git/lost-found/other/1cb460853dbc76ecd603937b1385d60dfe4544da', '/.git/lost-found/other/1ce139b0630235d7cccd5e7233e06fb27e4b7e92', '/.git/lost-found/other/1d80ca727f627adf666f395a0c85e26662ed0d20', '/.git/lost-found/other/1fb978ebe70aba71b3e2d74d673c0459d8480ac6', '/.git/lost-found/other/2083461eff88321aa0feceaab497bc202e7d110e', '/.git/lost-found/other/20d6d5fa6f6982c1d4d8d927ae5e9e121fe42018', '/.git/lost-found/other/21637826d1d04950f4a4d796a9571a8c4d86b806', '/.git/lost-found/other/21c428f3247ee9fb40e38b78c925eea08e7175aa', '/.git/lost-found/other/21d13a0a40c505324dab511aa407e5dc471bcf1c', '/.git/lost-found/other/226a93510d33d1c407aef258f9c39f42e3f298ad', '/.git/lost-found/other/228c08f34331c47620b55794c64c0ff9897f15c0', '/.git/lost-found/other/22baf3300cc31a3540ca4314fd8c58bcb7018353', '/.git/lost-found/other/22e7afb00fe5b7c7602b761800024ed40d25fe21', '/.git/lost-found/other/230d67a0590a4d61346d6dd5ced3f53dd0f1bea2', '/.git/lost-found/other/238faa3816f1afd26933d98bd81001eb92a2c876', '/.git/lost-found/other/242b028657099781ee5f230d30afc0a8af8423df', '/.git/lost-found/other/245ed230dee59261acbdfe117c3db0280411df76', '/.git/lost-found/other/248a3917f8467ac0cc6218d4b046e8e4b2cba851', '/.git/lost-found/other/248fd8353332111067158f2d11e7087f1ac3fe69', '/.git/lost-found/other/2533d1949584c2a0a3b143a5cb4de3f8c1d17758', '/.git/lost-found/other/253f5f1950cdce8f3dd7dca88b26bfcfcb68ad9e', '/.git/lost-found/other/26194e93e2a767b3f44b2bb12906aad486311c49', '/.git/lost-found/other/26204973c5913550889f7735c6c91e3f23eb971d', '/.git/lost-found/other/2676a4fb754239d1306066ad2d8f58004874245b', '/.git/lost-found/other/26bc257b7c543df579db1afcb9248ced695a5433', '/.git/lost-found/other/27e9ed80c1396df06710f8c7782e989d2230e035', '/.git/lost-found/other/2912b2774fce14827260d4c8ec3a58acaebd30aa', '/.git/lost-found/other/29b9a8951ad9517c1953a163da020fe28852bba9', '/.git/lost-found/other/29f91579b798fbdf2436d2f21c966d128bba04fd', '/.git/lost-found/other/2afee31d90e375b801139b051605dc6f5599d9f1', '/.git/lost-found/other/2b77f7188e91b5f41905b979e1453716042a88d6', '/.git/lost-found/other/2b84077d254fc2a1d66d0b4ea82ef3a7fa125c3a', '/.git/lost-found/other/2ba1ae4723622dd7a36a624626a298bc4aede590', '/.git/lost-found/other/2baa9b4b0fd3a53e07dbaa15098f4c45e7419cd6', '/.git/lost-found/other/2bf2efefce1765ad78030310ed9900afb0cd5522', '/.git/lost-found/other/2c59ee393814f03d894d5d8c75ab7512af596f2b', '/.git/lost-found/other/2ca2261abaa3459cab2e6b5aac65911448fb906a', '/.git/lost-found/other/2d209cca9eecd6d9519f21ae66f180d2001554ef', '/.git/lost-found/other/2d808e55af2eb9b6c496d06a8de71c32578f172a', '/.git/lost-found/other/2d926e4fa759b1b3235635ba6668898a635443f9', '/.git/lost-found/other/2d98f0a835a91e49cb26869dc16dea0583feafbe', '/.git/lost-found/other/2e107635a41522a90f0ea3c1f8fbbb3ff8685f1f', '/.git/lost-found/other/2e395785e7e850594fe6874f052e55a0733d4549', '/.git/lost-found/other/2f29d9394aab14b49d63b7303c6549458f4f7158', '/.git/lost-found/other/2f785e870024de3ac7ca3a834b25ca25e9d9cb8e', '/.git/lost-found/other/2f7887c4fbfd68a3721f5d2cdc896c48bf353c5a', '/.git/lost-found/other/2f807662ed402a67cdc3a86d525264af5ff4fb7d', '/.git/lost-found/other/306a8becbe8f0d8eab7964b3986c9f94ff283e20', '/.git/lost-found/other/312308f273d963ad2f881e414e6dc908c7de72c6', '/.git/lost-found/other/313257cee583598c2b1e76531aee4382a34ae791', '/.git/lost-found/other/31919cbc2e7b9a6268f7bd5ade6a59d4902b52dd', '/.git/lost-found/other/31e88c3eb7be2600a07f8a293e0d521af54d6577', '/.git/lost-found/other/31f64f6e3b537ebaddf428c4cb7764d746510f2b', '/.git/lost-found/other/322ad23a9b2322a5eafbb97fd34f393402a04544', '/.git/lost-found/other/323f82bbbb2a2f435ba1a70ab85e6e604de01b6e', '/.git/lost-found/other/325706343725c6011b78dbccbe34e242657d5d49', '/.git/lost-found/other/327e8f6219bc9ac3aaf5c4e5f8a88559dd9c8d9c', '/.git/lost-found/other/328bc3afc9053e448e43ac838fbde8b5a6bff782', '/.git/lost-found/other/32f8032b0690c3e5ab5788e9a392fb328fdde7e4', '/.git/lost-found/other/332c5bfc92dcc95b0fdab72fec060f0f1fde04f7', '/.git/lost-found/other/33a71c56250cf2a2cf3bc20447d3bc0f4722b8c0', '/.git/lost-found/other/3407448373b50404341f30cfe3e19da4562e5b61', '/.git/lost-found/other/341580a820d2cd018774a99fd90cdd4928badc68', '/.git/lost-found/other/34c6a03cca3744f90eb635e4a427cf083aad4110', '/.git/lost-found/other/353eeeb90d31595d072017c457bdb335470c0b79', '/.git/lost-found/other/35425eeca676d4342ab62ffff6195d41b11f03ba', '/.git/lost-found/other/357377a3e9d1596994eb7db5c89ea3b40161b48a', '/.git/lost-found/other/3598090e6a420d70ef76bde587c93ade0de2721e', '/.git/lost-found/other/36228b5f70a00e5ce49800e5c4e6f423a864ae65', '/.git/lost-found/other/3627eb8009d622db55d0b115ad04a86af57dc99d', '/.git/lost-found/other/376c1e88772f0558744c3ec5bf33e514bcbfa5f4', '/.git/lost-found/other/378b9fa979fd0cdcd74fb98be8f965fc64ba96ab', '/.git/lost-found/other/37ab16fcbeb235841f49b53dda4f8a4cb8576605', '/.git/lost-found/other/37eb658dd959056bdc91ca5add0c61677dd55131', '/.git/lost-found/other/3893a9d23c221f7a7587b3bd1bbce3e53451a36b', '/.git/lost-found/other/393d937812a14bacba39114d3fbc6ba4b6f687e1', '/.git/lost-found/other/393f72379d2551529e19191f444ca8ac0324cc09', '/.git/lost-found/other/398f7fdb157e0e718ddb1b583446c83525a9c8c8', '/.git/lost-found/other/3aa11aec8ea158ebe6fa2976edaac47f213d098c', '/.git/lost-found/other/3ae1b05c2a5d648e1e234162415c93a2d566455a', '/.git/lost-found/other/3b05a03bfb9b84a6f82a3f6b6d4fddb652001ca6', '/.git/lost-found/other/3cc5321661d71bea5e919b2dd222d55638ef6474', '/.git/lost-found/other/3d2058541bd6f85fa9d3041eeb94773535041b4e', '/.git/lost-found/other/3d4090fbbcedee422c984f49d6951366d6e87331', '/.git/lost-found/other/3d76e8038eb8c5d0065da0f378418b0929a3e1c7', '/.git/lost-found/other/3dee1d10be4dc43fdf33e57816608eb7f5f762e9', '/.git/lost-found/other/3ec37580b08a3f792df050067bd3383ad9c01df9', '/.git/lost-found/other/3ecc52a19ba9501ffdc2b0775d42316e3eb031db', '/.git/lost-found/other/3f5e76235147c70911902e9f103daf1a7314e95a', '/.git/lost-found/other/3feb49e8ddc04e5c3e85ae2ec34908b7ea1236c6', '/.git/lost-found/other/40758f589a15d70a0fb173d1dd0cd93c2b280b20', '/.git/lost-found/other/40a857d2f4d88afe60d9d223c3874cb9ccb4a55c', '/.git/lost-found/other/421881dda370e44a27a3e93dc9caa1d44579a990', '/.git/lost-found/other/428a345dcc183804917d5077052693bb113f74e0', '/.git/lost-found/other/429074a78b514abba6f272bd54f3011a72c28afc', '/.git/lost-found/other/42fcf8ab7e1224020d789b4b47b37e4eff58c62f', '/.git/lost-found/other/433079b36165ec24a2b3bfa3208be0e72c68112c', '/.git/lost-found/other/447720e79a8bf68b0570557e2603109333a4a04a', '/.git/lost-found/other/44d6e7a95ef488d9350b45e9cfa358ce04beec08', '/.git/lost-found/other/4678157d773d5c250ee875f3fc5ad8cfbb06ae38', '/.git/lost-found/other/46c6456223387aec0a7b111a58be75f442f3c342', '/.git/lost-found/other/46f574b31ea9c081d10dbc24fb57ba3e4b447b6f', '/.git/lost-found/other/472070c0c081ef4c9ea5e73fce87dec51a5e50bd', '/.git/lost-found/other/473daf24f1e540b2f25a569f819a238aacb81035', '/.git/lost-found/other/47eec38c60613993ebddfe34b03b3c993405009b', '/.git/lost-found/other/48355610f438c75b706f3d1b9bb15c49f849800d', '/.git/lost-found/other/49e4545b844c30e3a2dfd5283289f27650feed77', '/.git/lost-found/other/49e5c2487096098aa82596f7c3bf4b154b03263b', '/.git/lost-found/other/4b0ca8a212de55c027ab38e37ffcd17e341d57bc', '/.git/lost-found/other/4b1106adc7b4c0535779dc0c2df302e2e4f26afb', '/.git/lost-found/other/4b4e6a0046c053a95f57754b9088a81834674349', '/.git/lost-found/other/4b5c220106e4b150f1785aca51b4c1516ee7f6f7', '/.git/lost-found/other/4b825dc642cb6eb9a060e54bf8d69288fbee4904', '/.git/lost-found/other/4c109c4291b72213236a54418e69bc70989d3d23', '/.git/lost-found/other/4d64eae0c3986894803d586d4c44ae16906d23f8', '/.git/lost-found/other/4dae699298c4e827eb777a620bc2b0b622a3d043', '/.git/lost-found/other/4daf2d4fb4be2002d0c6f0783065cd4aaa2ef9d5', '/.git/lost-found/other/4db248d2d0362a2baa123bce350af1c3cf725718', '/.git/lost-found/other/4dba40158ad402bdb18ab94f570242af2ecb9f72', '/.git/lost-found/other/4ddb67d026b4d1d9533591627008838db3040342', '/.git/lost-found/other/4e560d39e66ee48393ac86adf8bf92f390ab6282', '/.git/lost-found/other/4e80ac0c1f3b8a9f86cdccef454912a80077d15a', '/.git/lost-found/other/4ed608f4d1b961b4b069673f0dac7b286868f1d4', '/.git/lost-found/other/4f03978e25b1d70dd18b2f1ce83f070616bee53c', '/.git/lost-found/other/4f6403a8bcb6c19a368e929b9a4e12741e1ab55a', '/.git/lost-found/other/4fb85fbb7c372a0b84cd78fa6b55e410e220239f', '/.git/lost-found/other/503b52b471cf3c48677445669dda1dda8fd71c51', '/.git/lost-found/other/50446582fea97fa549a6039a5f0c504364f69e73', '/.git/lost-found/other/509ba1ee9c66d67aa12183a23911275c84c1be12', '/.git/lost-found/other/50ab5d3cf546c8b875e8c8fecb728a69ed6129e1', '/.git/lost-found/other/50c32b19907ec29e0df34ae3dcb64ccbad1bfeed', '/.git/lost-found/other/5135c970168de2f80375b8e8223d8b65ebe722d9', '/.git/lost-found/other/514ef7a257573e892fef8efdc8092aa113f301a6', '/.git/lost-found/other/515672a3eac687eeaa0d5331a88ae03e9eec92ff', '/.git/lost-found/other/51eddaf2d727e3973ab74f8d0d4d5d6925dfccf8', '/.git/lost-found/other/523cfd7c6c11e165293fcbe926464d35abe0f7ea', '/.git/lost-found/other/526cbab8a8237857d96750d81938f8548229fdd4', '/.git/lost-found/other/52a9fd5d5a39c98cf011809f1954ce924858033a', '/.git/lost-found/other/53c00c790d7213e762a416ccbd9fa61f2cc6b27c', '/.git/lost-found/other/549ef64d2ed3890a06bd03ef59952b31b70a5027', '/.git/lost-found/other/54a41810fd052d9463f8d60abf2c75184362b839', '/.git/lost-found/other/55616d36043061c1a3c7f616e099f6a5abde1e72', '/.git/lost-found/other/55769048317ffd40eca0be3cea5a4b9e5ab7cdba', '/.git/lost-found/other/55b747cbbaf511f4d5424f0f1301ed30b1916007', '/.git/lost-found/other/56e2a20d652ee923dad7ebb9d8aeda679efae502', '/.git/lost-found/other/56ea5e17523abc029922afcc9f23f2306cfef729', '/.git/lost-found/other/56f07bf7f1652d395100a1b2e0b96ed2b54e171c', '/.git/lost-found/other/56f3b2f52e650607bcb68a0a89e36251acb754f3', '/.git/lost-found/other/57b04ada3b0285ca34c1a7fdbb9c904e484a2d14', '/.git/lost-found/other/58bf0f7e675b7588a79421a3fabaf0f35e219290', '/.git/lost-found/other/5928f67430c179dc2031c576bf0b24b51d2bca5b', '/.git/lost-found/other/5983ea75fd9362c5a8709fb10cdfa4920f085b40', '/.git/lost-found/other/59a6d7ca7e0bd39f24f74469da806dd2659236c9', '/.git/lost-found/other/59d110fe6522d55e8e5f8650763f5ff86c935b7e', '/.git/lost-found/other/5a1e4a159d9cbf9d18e6e0da20f04e709b36e923', '/.git/lost-found/other/5a41118850b5b97764e3861fc59a901f69f18298', '/.git/lost-found/other/5aed03d61d3a40a4e4d8859a43e5ff373d789afb', '/.git/lost-found/other/5b03c014dcf3dab20b88f5a62dd0865020292ed4', '/.git/lost-found/other/5b3c284ca03de4c25ced51e9aa3a4b488804a44e', '/.git/lost-found/other/5b42a5fe2abb1393cf2b9ac7359176e4aed00c0a', '/.git/lost-found/other/5c40fd7e30b0ae67c6188ae7825d3ecbe2c432b0', '/.git/lost-found/other/5d51b2cf47c9bec0fd8dfc6a5c742839aead66d3', '/.git/lost-found/other/5dc8c414c8a6dcb39eead75672e29a6c7705fa1c', '/.git/lost-found/other/5fc241b5fc5ee3126714b7ec6bb1218f256b2f9d', '/.git/lost-found/other/5ff9751d696b33f83abfca804807e09e998cc015', '/.git/lost-found/other/604dca6b26bd18ef8041517b5520080d7d019360', '/.git/lost-found/other/608826a2afc590737f32a764a625ef1f8c685dd5', '/.git/lost-found/other/60cd35607497b333c4e689ec8c3d7beefb76d5aa', '/.git/lost-found/other/60e755f3531398a88cb2ba67af858c57dd0ab90d', '/.git/lost-found/other/6128184c716e17ff7c4382e61719214b88a65240', '/.git/lost-found/other/612b7e3dac1b05bc83204b5091634dc99d745a5f', '/.git/lost-found/other/613d1efee79b495719629da39214f79500635967', '/.git/lost-found/other/61c62badbeadcca961fde66023da79591e056332', '/.git/lost-found/other/623e4c399c3cf78aa7bff72e26554c85f6869fe6', '/.git/lost-found/other/62a41bba70c8083d3e9792ce06fcf891c6fa24d5', '/.git/lost-found/other/62b286e180ad3b353b79c522e41cac008f3512b0', '/.git/lost-found/other/6372d5b36494f138c1638b3930d8543e77265803', '/.git/lost-found/other/63e70e5456461721b42c484bbee1886cfc8ba39c', '/.git/lost-found/other/63f2e29d53169726763ff4581e6fdcd3236cdb45', '/.git/lost-found/other/640ebd997c31281a5274fbfcdaf9624d3dca7042', '/.git/lost-found/other/64e4f4a1d9a5c5f3af3076ec413de73a3f5a4100', '/.git/lost-found/other/6589cb9582ca26898931b1ff9fa713b99a51fd69', '/.git/lost-found/other/66161534878c9a2771f904c86c37771812f852de', '/.git/lost-found/other/6638f29e468c5eb3550c99e26aff88a106344cba', '/.git/lost-found/other/668ed8f54785171df27bcc3dd3ca6946b7c47b03', '/.git/lost-found/other/669527a55303ac3089986dfdd5be5379da40b8d6', '/.git/lost-found/other/66b958f32ddafa4f75a7a2cb2f24a9e9ccf2a097', '/.git/lost-found/other/66dc9fe2e67543e8bee36d8b809fc2488132e8d1', '/.git/lost-found/other/66f40ce43c80179972266b9fb98da995998b53c3', '/.git/lost-found/other/6702cfd9756562bfb0a3ba9b5abecffb3edd3d4d', '/.git/lost-found/other/6842fe827192bab8f1180cc0a667d476df9cd850', '/.git/lost-found/other/687cde57acd639e44b9f6ecf4bb3b29996c10bc3', '/.git/lost-found/other/6916bfc4ae8a8656910be8213444648b53a2352d', '/.git/lost-found/other/695a1fc4aabfb29ae1d4eb53d8262b001cf0b268', '/.git/lost-found/other/69ba46d4e80a1ca1f7e61de30c5a0973bcf9949f', '/.git/lost-found/other/6a0e4ee850e4136089b231c7385181f3833d64e5', '/.git/lost-found/other/6a10a4c99f71d892813817d6e131c32de5a3a0b8', '/.git/lost-found/other/6ab43d1c8712b075016024e6de4b2cedad30d4fb', '/.git/lost-found/other/6ab5f05565940fa70b59ade18d5824d49687af69', '/.git/lost-found/other/6ac3752495b076c748fd4e5c4984925643feef75', '/.git/lost-found/other/6b7cbd1cdc3ecae6259e767ec077682ab8140d37', '/.git/lost-found/other/6b874d512a6169e56875de8896ae72ca50462b5a', '/.git/lost-found/other/6bb4e0d4dd0ee5445099c82b2bd2f64a53e8d294', '/.git/lost-found/other/6c03949654187bb18a9d56abf3fa548d35436fac', '/.git/lost-found/other/6c5fc2bdd3439593a8643d755e206e6dfc9fc170', '/.git/lost-found/other/6c8a6bf7a8364e9f3c66b02e8af3048c191749db', '/.git/lost-found/other/6ca4f377708c5ecf6907a214a05573cc42b26244', '/.git/lost-found/other/6cabcbec99c44d58b07d21563b56e3e3ecc9cfe5', '/.git/lost-found/other/6d52ba52a8e301203cf321217bf466872849a86e', '/.git/lost-found/other/6df408815ccc8efcd933582508681c4b44e1d871', '/.git/lost-found/other/6e5315c52f4cb6f8f50c68116b2f12db8d110b4c', '/.git/lost-found/other/6f2516ff42249437779576cb418ec04cb76f8024', '/.git/lost-found/other/6f88ec227ecf2f7b141024b1d501544126a224f2', '/.git/lost-found/other/6fba22d4dc0eb6400d9414150d5b70602d6564bf', '/.git/lost-found/other/6fcf161c510c9b98c91a405a36236d1e7e6111f0', '/.git/lost-found/other/7053cc71e49faa648cb55ce0f0bf2b206c62ad69', '/.git/lost-found/other/7065f6674fe7a8235b352054611ce3983ec2b558', '/.git/lost-found/other/70adf55db7d632e16f7262dbf14637069fc748f0', '/.git/lost-found/other/70d153a9884e3f575ceee6df23bed28105af19ad', '/.git/lost-found/other/70f09f86714b5f1a6772acc9824b08e5148482f8', '/.git/lost-found/other/714397ace6f967f7f6c94a8446aad82e62242f3d', '/.git/lost-found/other/719a970b7bedabe76e51c19aef9d38a694ea8de8', '/.git/lost-found/other/721c0dd9c7733231be83aaabfd84464df8fb6044', '/.git/lost-found/other/728c2ace778aeceb83e85f1bcde65cb271b6a15a', '/.git/lost-found/other/72ebd6a7cfdb38fcc2e0b29564a3b301f7782e32', '/.git/lost-found/other/73fa97fd287d2dbdf544f5995bf4f80996e8dc14', '/.git/lost-found/other/7563c407d2437ca7e9fe67a0bdcfbe9439559381', '/.git/lost-found/other/757a9f890df07ca2d991d61cbaabe564c1e908eb', '/.git/lost-found/other/75e403200b7c6f1e192ff409078d9539db59d5f9', '/.git/lost-found/other/762405ef38fefcce716ce0ce148eeeb530e1e89a', '/.git/lost-found/other/769c1bb07714a82c3cd25c50f256f28519da231c', '/.git/lost-found/other/771d4dfee6367426c05c3d82559b5c866bf59ed8', '/.git/lost-found/other/77349909732fef77c64241e680e95994b7ab6894', '/.git/lost-found/other/776a4bea95d8e9f4deeb6e136104a5d9080dbf4b', '/.git/lost-found/other/777c96837cb78e1e50a9d82e0c0bf6c555dba8a3', '/.git/lost-found/other/77de4ba2f2aef9696037ea20f5e791ec8fc33796', '/.git/lost-found/other/77e3948ebbd8863edb49b35b86613591d4c3a2fc', '/.git/lost-found/other/782871526d2a991f40100b5e32cd3ef1fa465125', '/.git/lost-found/other/78dda83637c001a3bbb5b46fbed552151ed51365', '/.git/lost-found/other/790cbbdb4670edaa8647b93e6e6c5a9fc4aaac3a', '/.git/lost-found/other/7996e753f0d39ff8510fa714661f86e7b916a821', '/.git/lost-found/other/79ae734789ab6ce0d184cc720e51c101d3ee0f59', '/.git/lost-found/other/7a60567d3255257a8ec8ffd90b47253fbb7779e1', '/.git/lost-found/other/7a761a5bd14d2eb15e7fc3dfa4290f5d112ec66c', '/.git/lost-found/other/7aa8a776509d35c4b416ce478c310947105abb78', '/.git/lost-found/other/7b00b279b725540bd5e801557be40c425fec033e', '/.git/lost-found/other/7bed1a58912ef89bb40536ec81317ad4e857a3af', '/.git/lost-found/other/7c31bb200ac9ee3c8526031f3f462dcfbc0c6dcd', '/.git/lost-found/other/7c63e8f7e164de6eac3bf0e4c2c3b86a7006969d', '/.git/lost-found/other/7c6466d64311464b5cc235f012e7eefa7a3f7dec', '/.git/lost-found/other/7c7e207d982350b509a2ff479318fe62ed1103fd', '/.git/lost-found/other/7d1fa3cfc7a26b23468ef0231a6be425c10c39c0', '/.git/lost-found/other/7f1ccef0257eae07e1a9d96c9a419839eb69012b', '/.git/lost-found/other/7fbedd5325332884808b4f13376b20b608ba153d', '/.git/lost-found/other/80417b62ee231928cf6e1894ee78ae9d52dced8f', '/.git/lost-found/other/80525b0220584bb2859e90b7b1ecd96124809e0c', '/.git/lost-found/other/806c3e29a41d7902dc4bfb90b274f7bcdd692396', '/.git/lost-found/other/807fe9f45b577f7b4e832f53598c9132f4634217', '/.git/lost-found/other/80d57ddd52a3d347c46ca1ec7bd6611c3832991f', '/.git/lost-found/other/81b0c9d26060eac103e503fee24c4dc875d73a3d', '/.git/lost-found/other/81b84d2f9246fe95414efaf594ce0d66642af224', '/.git/lost-found/other/81c8e0c1332f8beac34dab5b2d8addd868c78d37', '/.git/lost-found/other/83f433e75ff687ed7ad6e622082b3771f4be902a', '/.git/lost-found/other/83fcd0a4b90b111dd78f24830b0cf0fd6f6662e5', '/.git/lost-found/other/8479528c7d38418a08b92817a5605425c6c65ea9', '/.git/lost-found/other/8507cc0d8827de0caf78209b1bc8b409c30929c3', '/.git/lost-found/other/852f59ef505774d2e1cded9189583af9a7fabfbe', '/.git/lost-found/other/8598ecf10a790316c773068fc621b1ec6a8c7462', '/.git/lost-found/other/85efd595e03f195168517e451a0f6351e2f9e69f', '/.git/lost-found/other/877dbd89e8209c09b4e6117d45aa1ffa5c29123a', '/.git/lost-found/other/87bdeed1fa7053bf3f3ee36c8996eb1a85ca4581', '/.git/lost-found/other/884ad461f9de46bba7b5fb8b37d1f4fb913b128f', '/.git/lost-found/other/88a12ae4891c84ce446aaf38698e7f684d05465d', '/.git/lost-found/other/88de5d8898855804a10e46a2b8ed2efdded56c2d', '/.git/lost-found/other/88ee53c9ece8ef43612f9db4cc25aa5614aa26ad', '/.git/lost-found/other/896dd57e7a94ddfe4430921fddcf78e252b7053e', '/.git/lost-found/other/8a2e1744f8d60b47acee31323eb9be5252f3bb71', '/.git/lost-found/other/8a5e5ad2e568b464c38258b18b07105fa93c8eeb', '/.git/lost-found/other/8b0fe43b479ecc9b599ccb21386dcf6243fab6ef', '/.git/lost-found/other/8badb259266160ed2ae90c6d544e84c1f16bdfa2', '/.git/lost-found/other/8bd53ac2f88091ca967b218668ddeb2b8b901b3b', '/.git/lost-found/other/8c532b7669a3fd0dc35dabdd43d2b34db2726089', '/.git/lost-found/other/8c7f0d1ecd32895777182562810997d842a1cc5a', '/.git/lost-found/other/8cdaba2214ca080e13141a212a14fa3492dee9a6', '/.git/lost-found/other/8dcf63db4819ce835831f19b7f843f66cf331057', '/.git/lost-found/other/8e147d7dafa9de53bdfdf1afdd2288c7015dab9b', '/.git/lost-found/other/8e1df140ffb6a1a2e0e1dbc48231a1341416d5ef', '/.git/lost-found/other/8e624b995ed2e8b2f8a1fde05616b92165f1b612', '/.git/lost-found/other/8e6e6dca3e2142e6450e31de9dcc15e1315d11d1', '/.git/lost-found/other/8e8cc43769b3e51927bb486257e5d2389bdfe3e7', '/.git/lost-found/other/8f29fcc619ffc635697fc2d2d468888819a7c05d', '/.git/lost-found/other/8f8a2153b54a03fb30f2d21c11b2fc65b5071796', '/.git/lost-found/other/903e19a32e203d03671b31f6e27ebaa907166d90', '/.git/lost-found/other/9040ad1040d2f81d6eba6d481dc29f2a5f5b2f73', '/.git/lost-found/other/9052c9897d84020cc14786b82536af8a94cad0e3', '/.git/lost-found/other/9124c4e8d7b6925e2de9f96ba7ee66e9cfbd5b4f', '/.git/lost-found/other/91364a90eb688a950083474549ee42e8e0eaf78f', '/.git/lost-found/other/91897ad77d725aab215d18fc41d34a68ad6b142b', '/.git/lost-found/other/91e214a28a493c3c2e35325fb7245d6983ea71ca', '/.git/lost-found/other/921a6caed41c95b6bba1e56724fe34b038245416', '/.git/lost-found/other/924d93052389d0b9434705bfe32ef317528044d9', '/.git/lost-found/other/92f0a102283a69d06abb892c5d78980a6a4d2652', '/.git/lost-found/other/932ab411aba0a979eb6a54f3c43832011843338f', '/.git/lost-found/other/9437d9d6ad6a559a5d535231870cc81d2e5f61e2', '/.git/lost-found/other/94ddb92592b2844dab2a6dbf6b54c3ec65c53adc', '/.git/lost-found/other/9596ea8c380e21e2936eebc4d43cc3da5c3945dc', '/.git/lost-found/other/95b3c141d6f33fa02247dc87531e793b05061531', '/.git/lost-found/other/960849ac9a576a80ffaaf0a558644a959e85d725', '/.git/lost-found/other/96947147a4afca1db6085e927b1a9a03d61ffd73', '/.git/lost-found/other/96f0c3a29711baf739f8d206549147833769309f', '/.git/lost-found/other/970b3536b39e69354428d28cb4461dc2b51077a4', '/.git/lost-found/other/979c845eeee9c7ea69e9be82ea0152129d99ab94', '/.git/lost-found/other/98330f2a74870e2eacf010a3dc6ebf02ba786210', '/.git/lost-found/other/98634d3201e655b428c3720dfc45a1deaf0fd370', '/.git/lost-found/other/98ddac6847239f0b68e04184b7c57cbffa12398f', '/.git/lost-found/other/98e1a00c29c13261193d33d35e8b870695aabfbc', '/.git/lost-found/other/9900a37055c69f4e8b8b84d6c679c7340cf21a2a', '/.git/lost-found/other/990b82d5c7737e7d79db4d7ee986945bee8c8b04', '/.git/lost-found/other/9964532f1952d9499823130c76cd62602dea68b4', '/.git/lost-found/other/99c369006665885b83433b1cada3e5998e5155b2', '/.git/lost-found/other/99d222d5d2d4742cfd70b247b8bceadd95fc4706', '/.git/lost-found/other/9a0d0a46f1f98aeebacd8915237221e8debc95fc', '/.git/lost-found/other/9abb4897f6f8e61f116f836df7fc815e683a5611', '/.git/lost-found/other/9ac9a25da69a69c9c6ecb565b8e855d3d39d4dd0', '/.git/lost-found/other/9ad7f9e4369acab40cfded3808876b7574f9390b', '/.git/lost-found/other/9b3627817278c3f1ea9f6f4fe2f8301d898b829c', '/.git/lost-found/other/9b4e06037e8da97ab1ce8591a052374860695c5f', '/.git/lost-found/other/9bf0e2c09edf77769e6856ecc475bb3bb86e45be', '/.git/lost-found/other/9c27c00a245e6db44d7f5dc05a9cda11bd241541', '/.git/lost-found/other/9c74f64ab7aa883b162a1b9a609b5647bf5cd115', '/.git/lost-found/other/9ca456f075c2c0aaebd5b2ee1a4529343cae45c7', '/.git/lost-found/other/9ce852637d31e71fc377559d79ac748027fea48e', '/.git/lost-found/other/9d3c14c4f7938219293f9b76798d587e36c29b99', '/.git/lost-found/other/9e7bd621f9a76c674f8c274753799ccaf07ab55a', '/.git/lost-found/other/9e7f02dc92c9bc10fba29f964c50c9f139a1f589', '/.git/lost-found/other/9ea482d56803dd81be7b63e60097e6171c004ce5', '/.git/lost-found/other/9ebd3ce8fe0e3f922060aacac32204ed38da03a8', '/.git/lost-found/other/9f2eec154f15568fdd976cb3ae4e296109e7642f', '/.git/lost-found/other/9fc8d58ef08ad56a92992a215cc0d76a5a8e94c9', '/.git/lost-found/other/a04ce92e7a6147503abde51c6d85c05f86763678', '/.git/lost-found/other/a0c6bdb727822d3ab28dd61c67b3b37832815978', '/.git/lost-found/other/a10ae35925626c8b16596f15a53aeab6a11ab5e5', '/.git/lost-found/other/a1ed013aa410ae8695f45a7019736ba3aa4fb275', '/.git/lost-found/other/a25b902ee65824da9fde90776f0ce686e07a4581', '/.git/lost-found/other/a2f2284bc6fa8fc3a142bcbc0414b14049c57475', '/.git/lost-found/other/a338a909318e642c29073226649ebc4667d40b25', '/.git/lost-found/other/a36298d1d7b41881fac3c262062753c14127c8a7', '/.git/lost-found/other/a3caec65273aae2d693f4bfa2ee2a2c3752c2ff6', '/.git/lost-found/other/a3ecb7025e3ede63635a7694860348298f2e6e77', '/.git/lost-found/other/a414fe1ef5a241eff31f88d267edb7378955ec3f', '/.git/lost-found/other/a4309913d0cf5df6e6ccc045ae0f19920001c3eb', '/.git/lost-found/other/a58d7bef5dcad55f29f6dd15f0fc3987e451d1f4', '/.git/lost-found/other/a59b9efc0a9636dce78f5c92fbac5d12d6da5647', '/.git/lost-found/other/a6091b6528df1b125c8e9a0fe31343e9b7e139eb', '/.git/lost-found/other/a60b71d615d71869dca5168f0a99487c02d7cf8d', '/.git/lost-found/other/a67d281fc3a06505d1f68688b8d19c1e7fd55d3c', '/.git/lost-found/other/a6a759f6ee5fe3e0998931bc1eb5f57b6d0a609e', '/.git/lost-found/other/a6bb3453ea72177cf803ae97da3ec7274f8bbe65', '/.git/lost-found/other/a6cc2e6efe55819439b2708bc7ef7d10a3dec179', '/.git/lost-found/other/a7417b0977cd4198ec223dbc7fe686683e6a56d7', '/.git/lost-found/other/a7b0ac4f7ba3b423ba8809cfca928693e9e1b555', '/.git/lost-found/other/a7f0b07ebde57e5af0354e2e76d73b8117ef9cd8', '/.git/lost-found/other/a8767737857edbde46d7c5760f644a3b145c4ec9', '/.git/lost-found/other/a907f6a155563583a84747b32b7897bc06d314d6', '/.git/lost-found/other/a93a02538f4107b5f0f6ba68d1e05106976618c7', '/.git/lost-found/other/a93f4d121ad5241432d6cece42ace11ef7d0d2dc', '/.git/lost-found/other/a9853bc470d2fd3c56ce24576650041dbddde66d', '/.git/lost-found/other/a9ab2c49d5af7d6df614bb0d578636ab64f181e7', '/.git/lost-found/other/aaceb0768852c7f4f7b7c086357a2b8319a67929', '/.git/lost-found/other/aad8d903158dca56e2301e3ac4a33d5c6765216f', '/.git/lost-found/other/ac48e387584c53d2cfd7867eb6983ca441277203', '/.git/lost-found/other/ad01876a896dd65578176da823c8d3eaf54a42cc', '/.git/lost-found/other/ad3b3036bc53b249ae74260b5df361c826ac41ab', '/.git/lost-found/other/ada35cdc23336af6d19f92c7bf023f84ef2c151f', '/.git/lost-found/other/ae67253d3690c041ae2f59e4d478510f04b183f5', '/.git/lost-found/other/af52068b4ddd08dafc65e05439cf72aa219d5e83', '/.git/lost-found/other/af9ff336b88c378508e3cd7eadd284d262242cc6', '/.git/lost-found/other/afa3bad6ecc1a686d44b7bf918da7c679e035577', '/.git/lost-found/other/afb28756840a3cd65e4389c4517d9216301057f4', '/.git/lost-found/other/b07a4b8db64b3990643478d8e05cc9b47efd6416', '/.git/lost-found/other/b11605b4c79cd6f830bc45162a5c28bc0dd0f013', '/.git/lost-found/other/b2913bc33fef9ceb13bae2b1c447cdc6fd1ae360', '/.git/lost-found/other/b2a71cf28f23bb8095e044f07a944b9ca46e36a5', '/.git/lost-found/other/b2f9faaf121213671fb5a7774e930d58f70151a4', '/.git/lost-found/other/b33fdbf692bc1bf33c45a12649e6d8805a7f12ec', '/.git/lost-found/other/b3e1f079730f15c805b6b1810f74a8950f7a5ee5', '/.git/lost-found/other/b40b773210056f26f750cfee0483ec7aa5a89590', '/.git/lost-found/other/b44c8d334c2720cedf3955e92d3a023f4d935c56', '/.git/lost-found/other/b52f477c7218624d8ec93a1acb97bc9bcfa8b9b0', '/.git/lost-found/other/b61fc9ec0d624a6fb5a3ee24de53e66839f36032', '/.git/lost-found/other/b7be51217a56e37c6e38cbbe732a0be92de0bc07', '/.git/lost-found/other/b817d6933884dd6c456522fa9c7215cbedbbc519', '/.git/lost-found/other/b8752d4fdff6b8b0ca56bc1b4d9697f1fa622767', '/.git/lost-found/other/b90b713046a8a15ec14fb0e8ac68bb50d20a22da', '/.git/lost-found/other/ba377d4c5675fe1b5496849fe1448ddee13cdf6d', '/.git/lost-found/other/bb53afb3ef890767ea09e0ec09cc8cf2f9d8b39c', '/.git/lost-found/other/bb920cc2a629754a612a360ab11e2e8a41929ffa', '/.git/lost-found/other/bbfa79a5aaac10800f659c1cf83de2b8f8f90d87', '/.git/lost-found/other/bc4e5bb47af0514e26b1fe0c3254b632c96c026c', '/.git/lost-found/other/bca71aa7a50f8e50f169ad8d7add475fcc88bae9', '/.git/lost-found/other/bcc4a536f944a78bc04830054c79a409585ee7a4', '/.git/lost-found/other/bcdda04baefba90a18ba44b74c2c6eaaddc5d028', '/.git/lost-found/other/bd2a1d030621759771ad4027c2a94150eac7a09f', '/.git/lost-found/other/bd9261ab35b09829e088a6da1aa076e98c524ead', '/.git/lost-found/other/bdbf5e7bd9efb4d363a7232fdec9cad6567d4cbb', '/.git/lost-found/other/be7d6b812f8433589a87bb6495b4dddbe12a0ee9', '/.git/lost-found/other/beb000038b4da9845ad1a638aade10236c7d7703', '/.git/lost-found/other/bef0994468110ae1fc1694af7188bcf5ca0918f1', '/.git/lost-found/other/bf29bfe9c49976b90984553d373029c8f53d8040', '/.git/lost-found/other/c03390e5b753aa22c85f2068144225856150c11c', '/.git/lost-found/other/c0577eb4a15bbf25fd3a5c58452d7f966970a69a', '/.git/lost-found/other/c194da9b62f88b61252dbfce48b0b5362f5e1a35', '/.git/lost-found/other/c198cf463656fd32c0cded88779f2e22d72c4c4d', '/.git/lost-found/other/c19bc78a96c49ef4677eea5af4526afe0617162a', '/.git/lost-found/other/c1d668567275777ab9130946e2e3a7195bb5920c', '/.git/lost-found/other/c1f6cc14efbc61641331679fb61606b1ae829c0f', '/.git/lost-found/other/c2a0ac42490e5986b165952d7702d65c06970ed2', '/.git/lost-found/other/c346cb932c8beb66f5dc30c662c2c41289d3598b', '/.git/lost-found/other/c3f599b00b12002d2a61a73ff0aa13d7524e832d', '/.git/lost-found/other/c415f7c2b19c281f1d670ac1c62606ef4ef79a2b', '/.git/lost-found/other/c4a684183d09535a773af72d1041476920339632', '/.git/lost-found/other/c4e7a00850f5045485ea31f07d406a573c62d04c', '/.git/lost-found/other/c4eb1dcec6f8749915f0f71285c5393955d98c6a', '/.git/lost-found/other/c52fe8f0592d844cbd901ce7bc44e0b1f11e64a7', '/.git/lost-found/other/c574d09175f0180319b6842ccfb2ede440e3a125', '/.git/lost-found/other/c5fdc494e96d7e2815ec1b92abd6cae192d0b95a', '/.git/lost-found/other/c63908d1df7973f503b327b3a48148ecb2a139a7', '/.git/lost-found/other/c68ffcfe5aef9991dd01696a443428d38a0c03a0', '/.git/lost-found/other/c6984ab03c0317af14fcb24630b38be6eca741bd', '/.git/lost-found/other/c6a161ff323e566d554ab18b7d4f58c2e3946d8e', '/.git/lost-found/other/c6a5564c6dd6cdd3429cd3326281f442e6c96cc1', '/.git/lost-found/other/c7a5ab9a45bc9a2e82c6cc9544c5b3c2d09abba8', '/.git/lost-found/other/c7afbe4ad776d0eaa7ec1e8b758d36a48572595d', '/.git/lost-found/other/c7f226c68b6c7fd47dc744bb8e0bdcfcd59110c3', '/.git/lost-found/other/c7fda2d48e4ec697b6ef93c8d41788cd050dd1c3', '/.git/lost-found/other/c829c60a45724554da4b097b17581af2e8a5216e', '/.git/lost-found/other/c8378ac3c120fd9b632b99b60e2700265d8f2195', '/.git/lost-found/other/ca0c53580589aaab2e623db4b1a3811974e04c03', '/.git/lost-found/other/cb68ee666c8f1f8773633ecd067416094eedab53', '/.git/lost-found/other/cb8d4858190a15278307f18d5ea943d1be41019c', '/.git/lost-found/other/cbe58ca7e55701aa03b44dfefd37ab577c6e2699', '/.git/lost-found/other/cd216e02b02ab615377718fc9d57a85fe3bed359', '/.git/lost-found/other/cdfd8467dc6ab25e4cb3c9fbad0356f018dd0263', '/.git/lost-found/other/ce0f148e5050d5462b9fa4a7218443611f540662', '/.git/lost-found/other/ce4226f7495b39011397a2f6a1352391068b55c0', '/.git/lost-found/other/ce57928fd558f7fbc027f3aafbcc951a0a5ff7d8', '/.git/lost-found/other/ce8b9095bbe8c455e3a083d1d2bf00fc3f95b68f', '/.git/lost-found/other/ceaf0b0c7041d998228f7cc55d506013d4e2660f', '/.git/lost-found/other/cf21155b406ffe5d1ec58b2bfb3280f9adc9d734', '/.git/lost-found/other/cf589f7e7cd10bc0893d142bf2b1787bd13a98a9', '/.git/lost-found/other/cf9d67c816b6afce8b699b4509d0482602be5a42', '/.git/lost-found/other/cff0d14042e370123492e5b41e77144ae2b6a234', '/.git/lost-found/other/d04428fc4d2377186583fd4be601a67be5de3ae2', '/.git/lost-found/other/d06cdb63841efd6f9d57da0a49d556d1e0193d21', '/.git/lost-found/other/d0fcc1e31590864b6d8ff451e2fdb118673f4f27', '/.git/lost-found/other/d11859d8b7f96cecfa199c1d97d294e7edb9b643', '/.git/lost-found/other/d16351fb26ba3350c0a7cbe33983581748916efe', '/.git/lost-found/other/d1924c37cf129b3171b889e6d0595a74de2dddce', '/.git/lost-found/other/d196bd9551e1cb5459af29b2dd471c413a752b2c', '/.git/lost-found/other/d1c237bf893070207c137c6b4c8692712bfdd8ff', '/.git/lost-found/other/d21237aa1e63fd7757ca66048f14e65990c070a2', '/.git/lost-found/other/d2453b4648cfb34f34b9758f6146f469b0a57607', '/.git/lost-found/other/d2b4354cce6142de4373869d6869d8d3fc5384dd', '/.git/lost-found/other/d3584209a11765fd9897e316865f6378b924fb08', '/.git/lost-found/other/d3701779a329a7ad2f0c33373d48687b0325a176', '/.git/lost-found/other/d5d57e5acef03490f3e11000082c513a6947397a', '/.git/lost-found/other/d5fe79282acedc0c62e6f1f058c20fec777f0753', '/.git/lost-found/other/d69e4e4828e0e860c901c27d846fdd2695d13a7b', '/.git/lost-found/other/d6a97a089030a7edd8b329c8ae905eda7d8cb77d', '/.git/lost-found/other/d6db780d0f4b775d5c38a76758fbd072c433fc5b', '/.git/lost-found/other/d6ec37f282939964e41bf2de2675c39731b21cf8', '/.git/lost-found/other/d6f6b42a5113049affff24f3057a16240e5b761e', '/.git/lost-found/other/d767ea26e44c64d7e9b3803c0fe5b09b0172b5eb', '/.git/lost-found/other/d77b3a691e389d0ab088e72c10008c645344b08c', '/.git/lost-found/other/d80cd503dfa13d070109f2dab443f74be8f41ab2', '/.git/lost-found/other/d856d9cd9646a8c8567ee9af9551b2e43eb2b2b9', '/.git/lost-found/other/d91fea1942d87936873c4497ea5f8398dbbd1259', '/.git/lost-found/other/d95654384b6318ecb9abec998e2c64599769f652', '/.git/lost-found/other/d9e204dc5438684c55642ac4c4f5edb79aac85b0', '/.git/lost-found/other/da122377427fb4592c6703f54c9850535bb57e00', '/.git/lost-found/other/da129bba6bb8d62d9de2da9a239c1cb59e1a06bf', '/.git/lost-found/other/db1d00fcc5c8d09c5303493b6802f45e19162edc', '/.git/lost-found/other/dbda401cd34b991d08fe06946884135f0eeaaec6', '/.git/lost-found/other/dcac869fe6630d02093d2d6d4d423c3abfc5414f', '/.git/lost-found/other/dd13313f0b99c3e5722ba2f169ec1630d4090956', '/.git/lost-found/other/dd9df54fb86de4a812d2d5c14f9d5d302eb0a895', '/.git/lost-found/other/df212e1724e830f02c6f7c48baa386937ef8a8e4', '/.git/lost-found/other/dfd989fa24c652eda8b3caacf8465401d8a15fe1', '/.git/lost-found/other/dfed33fa2c962d9b941e06eb1904add340c5c1a6', '/.git/lost-found/other/e043fdbdecb337c2509db1da715bc608c7e5c457', '/.git/lost-found/other/e05eb2e28b2f121792aecb7cc2c9d3835a99f45d', '/.git/lost-found/other/e0c9d873acdde10922f8b3fe006a65790cf1d033', '/.git/lost-found/other/e0d3f4acaad9831a78cde41b9465650d8ac882c0', '/.git/lost-found/other/e17608611f7ca0f1bc68ff088dff1d0b226934ef', '/.git/lost-found/other/e1af2f444391dc6bed835532f09731b5f9991ea4', '/.git/lost-found/other/e2391518db03b590ccce8e1cbd97c243d3495201', '/.git/lost-found/other/e25b83ade139fd5d022aeba14351f302855bc80c', '/.git/lost-found/other/e2c5ecab8eb12e570a291601bacaf7b9d74279fa', '/.git/lost-found/other/e2ff6027c01c11460a38172570e89c9eaf403cc7', '/.git/lost-found/other/e31315b59db6da959c44aae02afdea6a956d6749', '/.git/lost-found/other/e3362e7b28e5bc000858f79e7808bca8378d65c3', '/.git/lost-found/other/e3dd33d57725ad5c51131c5a4ff2a6baa90a7bff', '/.git/lost-found/other/e418f732044b83b44c55a3d8bcdce822dda2d201', '/.git/lost-found/other/e44f18e830600f291259dd01272612bfa620c51b', '/.git/lost-found/other/e49b0ca82b56b90bebb8278e7399bca8a0664fcb', '/.git/lost-found/other/e503ca98487014da5da23cb42963fc8f1ba24da0', '/.git/lost-found/other/e520acb374bf8c6935bc34fa047d318e675611e9', '/.git/lost-found/other/e5a46d4f237e3ab7c53f212cb9b976ea970e1344', '/.git/lost-found/other/e5d997d2e7d0dfa63294bb5eb482acc1e88f8980', '/.git/lost-found/other/e674b96ab8e8f0f47f0a21b11a6aab353fd952ad', '/.git/lost-found/other/e780940b9beb3aa95c0e8141615546cc43e3beb2', '/.git/lost-found/other/e82ce186470aab5d29d55e09ed28c972a6631138', '/.git/lost-found/other/e8602005a19d6eee72b7e70d9ac70f5da48bc0f8', '/.git/lost-found/other/e88fed00aaa2ce25272c7f42ea7f6aa0216dbd2a', '/.git/lost-found/other/e988e0b91b3e936c0b22dc2471b12b685e7a32d4', '/.git/lost-found/other/e98a51c0a5e69d042a9a6831d845e3f47b6f877b', '/.git/lost-found/other/e9b1d8f0265d0958e8a5b4a6e8c822f1703e561b', '/.git/lost-found/other/e9e3231e30ffc553ddbfc6f85432deba73d86ba7', '/.git/lost-found/other/ea0d0f9b7b627a6646f6d51864ff418f34902679', '/.git/lost-found/other/eb014d2e1a941a9af381c2744eace9fb4eee73cf', '/.git/lost-found/other/eb19f3b0cff3fca757d4ca80219f4ae1fe43e6e3', '/.git/lost-found/other/eb9cbadf8efbb1fc517fa7295d03720da31509d2', '/.git/lost-found/other/eba33a9bd67e3209a6c680d5018f3a68c9a1efe0', '/.git/lost-found/other/ebceda64425af0c067023a8307110a93375ffd45', '/.git/lost-found/other/ebe2ec685146f680a315f128c349c1dbf90adb00', '/.git/lost-found/other/eccd1e176da943989ae2606c2b88b88a9fc437b9', '/.git/lost-found/other/ece03b567137bf1de7f0e8bf9c5a4966a5713149', '/.git/lost-found/other/ed6fea00087480c1025065a44af8ebd9d7579ceb', '/.git/lost-found/other/ed87c4d1b13d5253f80f8e338600741e25e76691', '/.git/lost-found/other/edd4de5068941df19e47f2c46ba92c179e006fc1', '/.git/lost-found/other/edecb464de5a85816f1a834eabb5a70fda930567', '/.git/lost-found/other/eec85fbed6da5a379fb1231e3cdd297457f45913', '/.git/lost-found/other/eef1dbc15dfd6b66e0695323ee6b6a27d8c8d620', '/.git/lost-found/other/ef2ed056c509290708f0af3df007e352c215f659', '/.git/lost-found/other/ef417fe36253d71abb1df1c24cb00c029f36c191', '/.git/lost-found/other/efc42a741226285057099f826136a954c9f60f10', '/.git/lost-found/other/eff77e32c35f9ef44aabbcab2d36737b118026bd', '/.git/lost-found/other/f06da463f9b4911fb844b3fdf989eb2e4b65229c', '/.git/lost-found/other/f09d1df8015f8bb959b34440b1dd8b37cfb11008', '/.git/lost-found/other/f0bd3f073c0d35a30be9e8db6196f98c10bc36e8', '/.git/lost-found/other/f0d1fee8f3aa5faee3a47eff72cb5f72b64144b8', '/.git/lost-found/other/f0f15c5214e9b65a671bf8c8a746fd62bd3bbb04', '/.git/lost-found/other/f157b9093d30086676020a187f11fac6aa511ac4', '/.git/lost-found/other/f1d80bcd5b7b96a9d8b84da0aa1e0456f8b81c80', '/.git/lost-found/other/f22f4f45cf11ce898f3bb59999bcfb92bcf27878', '/.git/lost-found/other/f2667bb108c5556bddb66621a82124d94e57ffa2', '/.git/lost-found/other/f2a49c9f94a304cbdd8c63e63618f514dd430fdf', '/.git/lost-found/other/f3a1936aa92f749281b00a97f46c85c0f3faeb3d', '/.git/lost-found/other/f42b592f53441bc52a46117d0dd396eb602408a7', '/.git/lost-found/other/f4434f6a34c53588be267f04ba5c83f53c63bcf0', '/.git/lost-found/other/f44a8e423549bc7bdb6a49e232c498f4f4ac1fbf', '/.git/lost-found/other/f6eee227d2cffdc9cd3c598fdd731988f75dab78', '/.git/lost-found/other/f74174bc51b61272e8d1106c065feeb9270bb198', '/.git/lost-found/other/f79731037b392d638382b00776eb115ad82d5a10', '/.git/lost-found/other/f798ab67c883b2c2437da785757dd4acc8ec2802', '/.git/lost-found/other/f7ae7eebd292d07443f6b71fcf69a4d58e600dcf', '/.git/lost-found/other/f7e04c7b89185faa008005238823e991d473d6b9', '/.git/lost-found/other/f809cda2ab8e302b1f5d8d456bc48517331888fa', '/.git/lost-found/other/f83d5ab03367fb5642286c45e104911a5f07b3d7', '/.git/lost-found/other/f8e82125cb443505eecb0d55785a053fdca7692e', '/.git/lost-found/other/f8f69ff5df79ea2afc60bcd584898e85d69dbe70', '/.git/lost-found/other/f9e6c91fc25475e54f13be5d3b540a079341fc2b', '/.git/lost-found/other/fa6978edc179dd7f5080701f86e4b87dba737809', '/.git/lost-found/other/fa71d85dac9e3a9dcafb1eddff0a06d6a1f8d89e', '/.git/lost-found/other/fad5f2c59e6ac92d7d2c2bbda552b8bbaff05be0', '/.git/lost-found/other/fb26b03b1c71350bb0cad1dfdf58d62963cc8c83', '/.git/lost-found/other/fb374affc79708bc948a360c508e21faaab4ebb9', '/.git/lost-found/other/fb69ef7c7afa41527b8ea058d3a983d41b9a6b39', '/.git/lost-found/other/fba48324fd82a30093cb9276fb462866dca04776', '/.git/lost-found/other/fbd5050d803a8bc8ede5dc38f21b85f0d6340f20', '/.git/lost-found/other/fc2ab51db9df28d1cea1ad609b1f6a4be02876d9', '/.git/lost-found/other/fc6e8d45ae5418dae578e0a5cc014fe2cef7d73f', '/.git/lost-found/other/fcc1871fd0b91f9512edff43cb9f9c6d93381ab1', '/.git/lost-found/other/fd209fbb5c2ecd03c306b65055023886d98a12fb', '/.git/lost-found/other/fd618bcb1a6d81feccfa30bda3c1ec83f6c99da9', '/.git/lost-found/other/fd7391d5c0e8395ad01076f9710de2fd352e0f91', '/.git/lost-found/other/fd7996fc223885596b22d096f1c130f9ecca483a', '/.git/lost-found/other/fdc7410fe2c49ac323b138a6420b1573d24b0e87', '/.git/lost-found/other/fdee2ee54a319f9fe963492c028efea79eca32cd', '/.git/lost-found/other/fe7bb38beba7a69323458420123e865a56856a48', '/.git/lost-found/other/fe7cebff670146550df068f2f90bd7399ac8739d', '/.git/lost-found/other/ffbdb38129ee775fef20071909e5ff669e40abf4', '/.git/lost-found/other/ffe72238f13a07462b349f317290814b1d8a21d5', '/.git/objects/00/025daef50b48b9a7c3aa0957f67692b7cf9644', '/.git/objects/00/2531ad23eafab03d76205914b3760606265e11', '/.git/objects/00/279ba916b80ee7f054dcfe4bcad5fdf3d0cad4', '/.git/objects/00/3f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/objects/00/5291f4fcabd5eeb99dea4a438422225f9104fc', '/.git/objects/00/52dd8f0d35e7d44cabe09971d6e0f21ca39cd2', '/.git/objects/00/560ef0fbd6334815132007e408901acbace1e8', '/.git/objects/00/646ef1f6f7efeaeb3e5c6a38e238fa5728b8e7', '/.git/objects/00/6f8e8695b0a66ae47eb9f76ad1bc0e7b0f036d', '/.git/objects/00/85d4e575161ca79d7c14bb62cf89246ac6e4cd', '/.git/objects/00/9107e59a300c960ee6ec2a0fd55630b53e6a77', '/.git/objects/00/a92ed33a5c9c699f84cf5e7ac486d7789874d9', '/.git/objects/00/bb4eb3c57678c53ecdb996159c28d816ca8abe', '/.git/objects/00/bf2ee6092a4428c1c240774794e6c695ff4722', '/.git/objects/00/bfb9f789c6aa35ba63147502679a101296cb0c', '/.git/objects/01/03d9023b3c0be99b13d162789304c2695289b2', '/.git/objects/01/08acc654101c39e74de3cb6404c4fa80bc7bad', '/.git/objects/01/10b4b49800261c96b2f11847c83fdd04e60b20', '/.git/objects/01/1eb16c1ca5cd43dfe08ae67835808b35c8afe0', '/.git/objects/01/4d2f0fd6dffe4835f741728459499991b22962', '/.git/objects/01/5abae91e08022c92cb6c24e1e1097ec60a9c6b', '/.git/objects/01/6411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/objects/01/686fb3f6afa2208defd34a9188169a7884eccf', '/.git/objects/01/72babe377620bb36cde7d6318983b28943f5e9', '/.git/objects/01/7b31bf525f3b189f3119394c79bb4284fddfb0', '/.git/objects/01/81bd6955aab80579d81db279fbd9cf97044fca', '/.git/objects/01/89548f4f27fcb26840150f585a64515d77c26d', '/.git/objects/01/8bd6292885242b8fc321e98611b86abbef7035', '/.git/objects/01/92dc92789e642707957b713071f72a8450b714', '/.git/objects/01/a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/objects/01/bd8bbf0fc579feada35ebba3beadd61b3fa934', '/.git/objects/01/d51ab31a7a5ba8671eb706887eb123d0ec57f9', '/.git/objects/01/d9bb05d576e6db8b5775d37cbac01368f4fb94', '/.git/objects/01/f4c581d56f69b4e25af1f5ebc05ebec603c3f7', '/.git/objects/01/f88f8377947a49ec1cfa7a9b32b89b69dbef4b', '/.git/objects/02/02764beb43a71df5e2d8c411b8c22833417961', '/.git/objects/02/0c91471cd156225ca0b6684340335e17c9587d', '/.git/objects/02/1d956a833b156e5835bb90f20f2fb257686999', '/.git/objects/02/4337837f4b10ca80598d1b777c7ddb3382a7db', '/.git/objects/02/4da679e39764f8e2a1862074bc7d3a67b39a2e', '/.git/objects/02/500954f54d824bf47a0c40e7249570c8ae35a6', '/.git/objects/02/54144a053e6691f5da797289b3815221e244ee', '/.git/objects/02/5c0c10f9864685f955733e39cfd79d22ae1352', '/.git/objects/02/6d0d210de6d3b148a6616c9a49368f14c09c7f', '/.git/objects/02/7cd9077d41da5280567175993abb09c6e81add', '/.git/objects/02/7e36728d1dcc8ff7c167c7c719f406b537c61f', '/.git/objects/02/97c9b7194e6e16e58b7fad80617595ec60797a', '/.git/objects/02/9f3344bdabc6fa51d3a3317b8344c9d12fda27', '/.git/objects/02/b6d03e7eec58ab7e5edb099c5e17243fdcae88', '/.git/objects/02/b6d0803b43000eff745e76727f7a0785cfb736', '/.git/objects/02/c139017e618c759476e436e3fb5fea75a042b4', '/.git/objects/02/ce21bab26cb69adfd9643ec4c839dc7a316ed4', '/.git/objects/02/e3706e34f211187bd64efa7a9ad51760195d39', '/.git/objects/02/e5c435ffbd7357cd76f7c19bf5f4451ea88c3d', '/.git/objects/02/e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/objects/03/098a8322f9458ba797697f7cfdf272e30f91a7', '/.git/objects/03/09d7c803accd0e64d899fd8e0cfb1098a815d6', '/.git/objects/03/12d61983ef80179bfac79abbba1359052f115c', '/.git/objects/03/21b0ebc8efdee894f75380930206da9f16ece5', '/.git/objects/03/21cc3ec2443f4d85700dfe3f808368fbed568b', '/.git/objects/03/46900bf395f5f0160d317d392abb7aa026c7a3', '/.git/objects/03/56133446ed7dfa697229a2b5c19f243e35f443', '/.git/objects/03/7233cb441e842bfda192053568fe3488f544f4', '/.git/objects/03/732f0c6e6eeaef66eda4e4a6de308b7e7e1e95', '/.git/objects/03/7e5e882489a7413c4a62c63d0617b5931284f5', '/.git/objects/03/992f453ea274349984b8262b02650fd1b8bca9', '/.git/objects/03/9efba89af1d0d8bc7aae3c352c34e0c51701af', '/.git/objects/03/c02ba7211ba7f8588931520e8be278972d8269', '/.git/objects/03/c3557176983f991148ff39a6afd493bdf711df', '/.git/objects/03/cdbdebe4e5bc4b0f7a70e153e8be75dafe3324', '/.git/objects/03/d1d893b164cdfc9957a88495c3449fc4538ccb', '/.git/objects/03/f10215da3a690e8f4a1155755ae2b506c5f1b6', '/.git/objects/03/f8520645287e09c8ad96bea9bcb878a9022206', '/.git/objects/03/ff6a156c8ba598cf1be27fb2371810888a927a', '/.git/objects/04/099990dadacd5c2f9cac501abf5448595db03f', '/.git/objects/04/0be927181b9604d69593ffe36ab7303b1a94bc', '/.git/objects/04/0e0ff5a310da50070b4caaa390e93cc8c45ee2', '/.git/objects/04/29762b630e33054c1f093d314dbc1558dffa89', '/.git/objects/04/29ceebd0dfc380db49c94ca9da53cf3d0c76c1', '/.git/objects/04/2e02d97cc4abc6a96b55d97f34fc76924c9cf9', '/.git/objects/04/378a998f4a8686eb28f62e8833b0f539229714', '/.git/objects/04/3f51145222bf3b3e811ab6d29c229b25b3b1d3', '/.git/objects/04/42d29efa0ea05d53ea9a8c2b6f9d4d76a65123', '/.git/objects/04/4e235175ddef6dd6b9a05edbd34b9ab69cbbd3', '/.git/objects/04/4ea84e87f27f536235093b99f1e70ff6b0d79a', '/.git/objects/04/5a95c2c2c83fbdc5489e26541666beca91b0c7', '/.git/objects/04/602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/objects/04/6afebd6ef9bb313d1003864d38f1939470c17c', '/.git/objects/04/6ec8df046968b6bd4058a151de39c720533f28', '/.git/objects/04/74599cf24230b2e6acf617ed53f19eaac1d8b9', '/.git/objects/04/754e0dd161f613e2726da459e85cfbfc1edd59', '/.git/objects/04/771a2ae371a6d614730f8a857a8b401fa5049d', '/.git/objects/04/78eb80cc9a8041214bf273295064af3ab7f7d7', '/.git/objects/04/7fd372aaadd7a538f968712fdbd0e0e9c86415', '/.git/objects/04/80586953887e797aaabcce4f0226ecccea02bd', '/.git/objects/04/8703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/objects/04/88481d528674a76807703e6625d6284ca8293e', '/.git/objects/04/89842c6d2c5ddbc9550902039e9b25701d08db', '/.git/objects/04/8f509ce5eadba0a89792ec7f9a5691cecb00b5', '/.git/objects/04/921744c623863c7465f82f0d1af98ebc5ecffa', '/.git/objects/04/99e3e328e479da772baf0797e2fa34d5146993', '/.git/objects/04/9cf58812f1ec14cd7c43edc82532b64bab5b4c', '/.git/objects/04/ba7faa5aee31cca7feb4058574f06ec3a9b645', '/.git/objects/04/bf8e699f88900a6960b666079dba19a77ee7eb', '/.git/objects/04/d51f0de077d3b810718bfa2ca6ac4f3567c07f', '/.git/objects/04/d557d3b8c74f15dc8b1039d196b50cb8924950', '/.git/objects/04/eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/objects/04/fc92e910c95c87a567fba0d8e4566649816c3f', '/.git/objects/05/04a514448e0c3c3e4f771ffc84479295824920', '/.git/objects/05/09e635b91d457d88001ca19f7deb59d571fc46', '/.git/objects/05/0b372c851b0ea84569f8654c65fbc6c371b718', '/.git/objects/05/0b84f0c04495d82204b41f3442a74cc6a1c071', '/.git/objects/05/16754f01d0be542a9cfc9c1543fc07b1724272', '/.git/objects/05/429119c92c1ee2c4044621244195ae8bc33e03', '/.git/objects/05/58ff9439de64e491ee9c3bd2097b5b118029b6', '/.git/objects/05/5ecd0695e622dcadcedc29409753f35d106433', '/.git/objects/05/6e214d9916a67615b4d789712bca658fa03435', '/.git/objects/05/7e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/objects/05/829e3696de2908b0d40f37f6c20fa8fff8a1c2', '/.git/objects/05/82cd30dd9e7c52791e8f1cefab0bf33f600dc6', '/.git/objects/05/880b7872ddc08ae82b821f1b3abd5c3e5341a3', '/.git/objects/05/91ddc9768f4c685c5053ca3185eb6a633a3717', '/.git/objects/05/a402c383746da97299cc12b9c33d5a2274fcd1', '/.git/objects/05/ae7f245bb7130dc464d00b710cce251cb7bc91', '/.git/objects/05/bc40edd4cc79dbed5bfe63bd8e89ac3473040e', '/.git/objects/05/c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/objects/05/dcaaad2921ef5e63bdab6f62ab24662b8634bb', '/.git/objects/05/e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/objects/06/0b348f7160e9612f996a74560ee786364ec5fe', '/.git/objects/06/121995b0950d829e4f685adf8bef846269580f', '/.git/objects/06/17f381a59a452478a8f34cabb652beadf361cd', '/.git/objects/06/1c9d02a136ba7adc607ed7074cd148595a2030', '/.git/objects/06/2a4e7b25731d2674574bbd21c7931dcc0a5baa', '/.git/objects/06/2ba3dc08a841ecebcec4c5c7c0efa5068edf7e', '/.git/objects/06/31461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/objects/06/3554b9d4f0504b72bcaf1ed91888688b8df1bc', '/.git/objects/06/3b0eb2461a6c575fabd0087334058e3e7d387d', '/.git/objects/06/418747a855c7847e27bfe23508610c20a60493', '/.git/objects/06/440e122972eb6c98407112d4abcd39c31e9321', '/.git/objects/06/4b36eebdc18055d9b9efab453b240dfd5f9421', '/.git/objects/06/4d3ab3dae901a7e93f7ab74c73b3fe334dc151', '/.git/objects/06/4efa3154548faf37f72f6e16da0f94681fa86a', '/.git/objects/06/6b29f4d826413b9c2bc0110e7b223e10001962', '/.git/objects/06/79676e67109edbe58db2ca2e345cc2b73ceb03', '/.git/objects/06/7d6f976c743dba9947cd7a355dfab293594cc1', '/.git/objects/06/839a7dad1e830ff2ba4cc5228781681333e75b', '/.git/objects/06/8a3e4f76b33c5dc916fe32afb54fd4c055f658', '/.git/objects/06/a8e8ac333fed73af47212fe4626cbaa3b74e82', '/.git/objects/06/b4fa32525254b94d62c83a59084454f8f705fb', '/.git/objects/06/c43ec225095ee1df544729b8b8fec79c0fea0d', '/.git/objects/06/d100f39aeef4de6917bbbbdd2f28021b8ef8f1', '/.git/objects/06/dc438ba2f37c478b6445fb82540037236de6d3', '/.git/objects/07/01a09ce6bf7c6c4f6224a7842d756b53a2a88c', '/.git/objects/07/1acfc4227f2b22c838b0a56a59509105e4c2df', '/.git/objects/07/2872ca40aa53c5fcb11aa9a7edd5041033fa64', '/.git/objects/07/2de9a5fdb1ef44cd0b059e266bcf024ebf4697', '/.git/objects/07/358e5fb83f8aa10e322bdff64aa40398232a59', '/.git/objects/07/4930d053a799cc4f9095e89196437f704205d6', '/.git/objects/07/50d849bd563021aa1b9de4dc745fa43bc77e6e', '/.git/objects/07/522cfeed14b2118b137544acb215fd0d23a276', '/.git/objects/07/668e6b5dbd6277a6a85728db272e0b820a459e', '/.git/objects/07/682e77b603150eac6f657df236ac3dced0586d', '/.git/objects/07/7efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/objects/07/8adb64a12dcb95981db04caf7568546f5a88b6', '/.git/objects/07/91e2c492831faaf144a90e6af25adaabad38fa', '/.git/objects/07/997cbc1661d4546af788172b66486e4dbaefdf', '/.git/objects/07/c5d56f1363e06e73172965496ce16246dce1f2', '/.git/objects/07/ce7e8216ecdc557e1f1ec524242dd409b4067c', '/.git/objects/07/d0f29a2d244a75911191faf176cc0c7edf4bda', '/.git/objects/07/d150470e12425cb0b2d6a1cd55cd35ff2ff2fb', '/.git/objects/07/d79d89a08562d80d6890844f66241e32b443ba', '/.git/objects/07/d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/objects/07/ebcf391bfe46a07fd685402467db2e86ed4e0d', '/.git/objects/07/fa40d49088bd7d8511abca903641e6ad199f20', '/.git/objects/07/fb0409a65ce96873f20fbecc016dc5ee8d9d0f', '/.git/objects/07/fcb01a9b6e469e5b52f9ac3ab3bbe83a63d95f', '/.git/objects/08/0554e8ddc2a1a87275a26e5457e1b2a6046657', '/.git/objects/08/080c1aef87cedbe163497ddad8cc3005a73f7d', '/.git/objects/08/1eef64297df0ea2e464cf48c1520acd132cbd5', '/.git/objects/08/2169d84ac7751152d7134fa37292c00ba029d0', '/.git/objects/08/28873634fdb24f4318a443877f6106b5ff213e', '/.git/objects/08/377760400a919e539db754b0b66ea7ce0cef58', '/.git/objects/08/3a576c7606386c1daaca88824c281693d0ef0f', '/.git/objects/08/42d15769f312e00dbce38c79a209d783d115ea', '/.git/objects/08/46bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/objects/08/4d44439e48fbd75cbc5ae0b0132693e7d839b8', '/.git/objects/08/6f557632720c84a78f3d5389fe19e2f1a94791', '/.git/objects/08/749be2799a1a1f0697ed2571a4682426ea12ff', '/.git/objects/08/7809de3bad36c3f85c48e62edb51c147e48b77', '/.git/objects/08/7d31d51dfb5a1137d4f25be244cc284a37a076', '/.git/objects/08/8409712f5c920b0dbf4a4c818e977f34f91873', '/.git/objects/08/9cb3c61a7acbf2a05ce9d4926088affe4663a1', '/.git/objects/08/ba0a8ee50af5b8ff5eb0a82d30bb5229fe2e86', '/.git/objects/08/c54ae1104de2c9eff8155db294aae27e432897', '/.git/objects/08/cd05987a9baa7c8e5f6caa20e79a8a63d3d0d4', '/.git/objects/08/d2a116f15f569082d9e41973dd7e570d5b17d0', '/.git/objects/08/dec4893dc318d55b9f67e5c489081528a17a93', '/.git/objects/08/f07511d3e089cb96e804567644ce5381392e51', '/.git/objects/08/f6269206fa970d1130cf6e232eb0ee7f43ddcf', '/.git/objects/08/feb11d7a524e0e04e556a3b0fac0a6a7b24657', '/.git/objects/09/04682cc174ebeaaf2e9f366af211a401fbbd99', '/.git/objects/09/0826b708d0c9dcaddbfe121559c5b1486529f8', '/.git/objects/09/1739e89e6bfb98fd5f431dcd801487dba344cd', '/.git/objects/09/25e45208545d1857f69551356dcb6ec82edda1', '/.git/objects/09/2a3dcb3669da7adc41965ed57e1fe8cb86f429', '/.git/objects/09/384094c714fa3c73aeab22ac4fd18d06e8dbf8', '/.git/objects/09/3d21dba99b105a0e82051ab2639b5151325793', '/.git/objects/09/45bee1723c5de6847e799c08785083db839a6c', '/.git/objects/09/46862f3f15d72c8b71d2af4522b4921f6cab96', '/.git/objects/09/4ded1d397e3e5a80c619217287287fb729622c', '/.git/objects/09/4e04d13c87f5a327a7f44ffedc0ce41d9214d0', '/.git/objects/09/6bea492cbfb9768d845115c7a6a4d079f034a1', '/.git/objects/09/8b34de8f71069fae9082ecd1903b6faedce4e6', '/.git/objects/09/916958db8eaa97c465c9bec51a3d1a29863ab8', '/.git/objects/09/b3cd47a8afc2c0c4de3af709b99566a5bf6f37', '/.git/objects/09/d354f2506d543f99742b506f1c5e20b41d2691', '/.git/objects/09/dc1f89767f23768719cb5094eff75ce635e0f2', '/.git/objects/09/fcb1fee7452e61ee700d2679429371977f92d3', '/.git/objects/09/fdf0167d154d7e4538373b8df76e056ef8b1af', '/.git/objects/0a/05a2808a79fe98d007bccb3b1060551300dec8', '/.git/objects/0a/0c8795605b604d1e687339be45eb17e8812bb5', '/.git/objects/0a/13e8776d7323deb5daf4abf20d914e5d0c9092', '/.git/objects/0a/2311bad25eea12e3670b5f0c36155e5890d27e', '/.git/objects/0a/32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/objects/0a/401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/objects/0a/56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/objects/0a/597e37cfb13fe9af1875fc0606d2f7cc0e7ada', '/.git/objects/0a/59bca84a5ae11bd02571a6bf55d97bbeeda3d6', '/.git/objects/0a/5abee36b52e3cd5aff769a0108ab1a3ca51a82', '/.git/objects/0a/613832d0a99485a26bdc2a2a347669c76d3ef1', '/.git/objects/0a/8b1aeacb86cb7efa0c8582e6f109cd1ba8c46a', '/.git/objects/0a/962ce910aa746587b34755922bae542449fba9', '/.git/objects/0a/9c45c7913ebf7c65a190c9b4623116c5083db1', '/.git/objects/0a/a39c684754ee62dfc0ef9866f409e95d192bb7', '/.git/objects/0a/a4f3386b7abde99d77a8a42c0e0c9a6e0c4514', '/.git/objects/0a/bc810e4c97279e80fa5610d8d2838b94e3bb03', '/.git/objects/0a/c6e9b1d42c10b456adb801699291acf3e7a7f8', '/.git/objects/0a/cc9185dc5580459d7b19eaf9bc4561109d5cbb', '/.git/objects/0a/cdf25eb887c3e132a436a866bcecd8a7a83e56', '/.git/objects/0a/d395ba510ce17075f27e7d6f4920547464887a', '/.git/objects/0a/e25708036bf7db64f0327ea004917ad42ea679', '/.git/objects/0a/f7b1d6071a1948ae9d76d28fbb7c496bea8020', '/.git/objects/0b/32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/objects/0b/3664959c7d794a1e8758860565e6c252546143', '/.git/objects/0b/4829e05344126422455e538c3f872330bac02b', '/.git/objects/0b/4ba29f97f87d85705e1dbacdbd901e825ab2a4', '/.git/objects/0b/5c093d67b5443b9efe596880b950fe478e93c9', '/.git/objects/0b/5d3ac18d6fbd99afb581479554b58fc4183e02', '/.git/objects/0b/5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/objects/0b/735cb54163379d90cea83320d93157240b00bb', '/.git/objects/0b/94a8d00ef25b126437e3b831d3c47331ec09ef', '/.git/objects/0b/9c1ff14d0729b8ca054bf3b70a31ed6ea3724f', '/.git/objects/0b/aa622887f5563517e122f9b16213710af9e5cb', '/.git/objects/0b/bcef51f80d0155f83a276423028a01a50cd92e', '/.git/objects/0b/be894f6158df6217aac34e5062d723091507dd', '/.git/objects/0b/c26acc5a1d060a7a7085eab6ce811422715108', '/.git/objects/0b/c5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/objects/0b/d9338bbd511117b1f70cc1e59c6bd691580e94', '/.git/objects/0b/dd4f1e5c19bd4b4c56e20da562449970b54134', '/.git/objects/0b/ebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/objects/0b/eeb928e68e50f79b601ffeb2721e89a635ed95', '/.git/objects/0b/f720f21f41ce829add4aab5a9a05012208c3f7', '/.git/objects/0b/fb909231e10a90dcfd4ca08fc34ad154b9686a', '/.git/objects/0c/00cb9ca737f2be5b9cff166bcef532262ec699', '/.git/objects/0c/03f3f202ea13e8d79942013dd4334cc5e7ebea', '/.git/objects/0c/0bdbfa2459da2f07c4ab0c874834200ff6278e', '/.git/objects/0c/3e4d5d6ea3196693b9472f7d8b823513fa235a', '/.git/objects/0c/4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/objects/0c/55eb9a5a6f0f2c00a7d6a578505a35c3c881f8', '/.git/objects/0c/60a48fe702d1f4eb0d7dc24a73a35b850c8eb1', '/.git/objects/0c/614b8e0f3afd25e895d9491c2a30e5913af606', '/.git/objects/0c/6358b6057a1b224be62ad80a00d87614631b60', '/.git/objects/0c/63913c8162a44efd3e5ce01fdd7fe5c3875f45', '/.git/objects/0c/64a4d48bda41945b4888b51a9e960d8fbfcf0f', '/.git/objects/0c/81eca4c8d2b7bf0a503cdacdfdc66ed1715c2a', '/.git/objects/0c/973feb4df661c4fbc19f236f825bffeb3df257', '/.git/objects/0c/9d4a1d27f542f5c5fdf5684e73c718676e06a7', '/.git/objects/0c/a878bc7c1f09046bb15719383794b9ecba57f8', '/.git/objects/0c/b3be9041c3eaf49139e8d49ef95f361352c397', '/.git/objects/0c/c5b534f4425eeb8b3f6bb9a32803cb055d7ff3', '/.git/objects/0c/c625939a9cc324e29d3b2de079d11735728b58', '/.git/objects/0c/d0ce18b1d6a46a554b87e2dc0bd115429eb484', '/.git/objects/0c/d26a469771b69762f53b5ae2a322bf170091d1', '/.git/objects/0c/e0b926ac0c36b6e353c377ebc74e59bc0561c0', '/.git/objects/0c/e65ae661206b963a23be69dbcc77c2bfdba45a', '/.git/objects/0c/f07378ed3afd105c193d8b1b209dfec5785402', '/.git/objects/0c/f6c89b58f55c9aaff91eca9869cd2c17c0a47f', '/.git/objects/0c/fed93b45cb80e866637f3e266fde5459ea49fb', '/.git/objects/0d/15ae1524fab34c31c9c1ed0bb3e65a55951524', '/.git/objects/0d/195c3ade96d5880482daa65889a072069468be', '/.git/objects/0d/2b4e5c9def6a898a4064dd6adf23d978807b49', '/.git/objects/0d/315a864dbeb1ff8b62f267f614e3fb239b3518', '/.git/objects/0d/354cd6d3e0fa3aedf54d9b9eeabec3593aedc9', '/.git/objects/0d/3b08adf9c7ed270b6d5889540ad4437d5f0b98', '/.git/objects/0d/453df5063969c6130eb9ab5f086b45b2321f9f', '/.git/objects/0d/5256345daf7cbdefa3bc826d1e64513a214cf8', '/.git/objects/0d/5d4ed9115a075bdb83c3da8e5d5d95bfebf06a', '/.git/objects/0d/72d0b2349a404cc4cddb87c836194765377d74', '/.git/objects/0d/753acfba917272cd72f418e9c1352ed20054f6', '/.git/objects/0d/85d92161c5e9da30deaa248e028278f143e5b9', '/.git/objects/0d/8780f3e4c97dc70ba82cc61c5cef46d57b0b33', '/.git/objects/0d/8883bb012284d6c3c617deaf7758946852971f', '/.git/objects/0d/97da9f70aa97244bea12a6d8024c006575e5c8', '/.git/objects/0d/bcae139c196ceada45a4720daaf5908702ecc7', '/.git/objects/0d/c7d460490f110521abbce48d8939e546425dc5', '/.git/objects/0d/d1ac693951729e6c496cb1a42a310eb0cdad93', '/.git/objects/0d/d9afc1c58e48f8e6e7af3414041106af38ff05', '/.git/objects/0d/db7f9b502bca441642e7d54c6c212f0b6673ff', '/.git/objects/0e/0761bb314058c32679440d8686420159c31db0', '/.git/objects/0e/189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/objects/0e/19651c4d48fa439f5123ab04cd94245f216743', '/.git/objects/0e/1a64777e82a3954e604e96907e1cc37168d3c2', '/.git/objects/0e/31d5d75617658d5871f0af7cd6e2572f65d5a7', '/.git/objects/0e/33d9681c3f231054d16d613b34097e7e8b59e7', '/.git/objects/0e/5f82aa92d0553cc9b4fd2cb4dbd2739e2ee8f0', '/.git/objects/0e/7262601e46c40b320da44a929f151c2c114032', '/.git/objects/0e/abd83d251910f3dbe9afcb67d962c186a2ca8c', '/.git/objects/0e/b37de8ca5ba7a34797b3355f41cf01b22ff008', '/.git/objects/0e/be1fc27f8d238046aea951e6caa693563a5db1', '/.git/objects/0e/ddffee3cce42079be92d29e9858c7f31c0a906', '/.git/objects/0e/f556b4beacab982c37a6ba626b68c12a03a3ae', '/.git/objects/0e/fcc5d9fbd21558e1d5c24872e4a1bfab7f3685', '/.git/objects/0f/0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/objects/0f/138f0796a06e405b352d9b196d634fe03272bd', '/.git/objects/0f/17f23b4277ae965b175409f9ef0ca8fe5faca8', '/.git/objects/0f/272f7f62bbef400af52029018e0b40f2e84d63', '/.git/objects/0f/2c1f18c6195cd349bfc1bcf75c63a4676aa178', '/.git/objects/0f/375603ef57e02e9fb0b574a426b1efba49d8e8', '/.git/objects/0f/3a6ec84962b576c06d6f3836465b86e5b3f10e', '/.git/objects/0f/3f373dbe68457e2f332b53419313c5297f50fa', '/.git/objects/0f/54a10edafd4f6d7e03edbb6dc48a45c44aad67', '/.git/objects/0f/56092d56b18c5734f3dd8b63ea6ce5355e0e36', '/.git/objects/0f/573afb56cf5cd6dd86621f5e5c4d7eeff7c726', '/.git/objects/0f/5968785d1283804001ca49ccf77d63eac98e02', '/.git/objects/0f/6c72d33101537f80a5c00d3919b4759f4364cf', '/.git/objects/0f/7e32dc222c7d9c81f5f3e241496ba69be2baad', '/.git/objects/0f/7f43f84fd8d72c7f119c1bfbdda8468f6ad8ae', '/.git/objects/0f/86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/objects/0f/904c72f18187d5c05f93cb546a711f8c3a9f02', '/.git/objects/0f/9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/objects/0f/a19e3e148a3e82579b6e266e89dc11d898930c', '/.git/objects/0f/b3ec07ae5333277f64ed812af5f0f22e48fb1f', '/.git/objects/0f/dd7178536e6fa45b29cf9ce871f435d79711d1', '/.git/objects/0f/ebdd5aed4ccb535776cb3ecf5f7292598d83cf', '/.git/objects/0f/f56f42c9ecca878a4c0e2e836e52a449662082', '/.git/objects/10/18a2334d5c1968f40c2f478fb1f2867e67b8b5', '/.git/objects/10/261e06f4cf6f32be1271762e4e2656d3227141', '/.git/objects/10/36c4359913cb364e8129ef0b26eb5dec343083', '/.git/objects/10/565c0176f2173424386bbc1502cb879a9dce9e', '/.git/objects/10/5a4c0156c9645530e6e2b046d9fdfb72c075e0', '/.git/objects/10/64453d1e30d78cd388f816b907f7b742375e31', '/.git/objects/10/7c2333f5bcbcad6ce31755c9b4b4c72e960d28', '/.git/objects/10/8486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/objects/10/8d20d49b8c9df755feb7040b27dd500650d6f1', '/.git/objects/10/9488d1db9f25b656ca5a4eed3b42ca6c3bd9f0', '/.git/objects/10/9674e0533514d7be518ce93f1318966acdaffa', '/.git/objects/10/97e656055bf30481bf2c943278f0eecb5b5d8e', '/.git/objects/10/ac366f495ba690682ed41a0ddb0004802f5ee2', '/.git/objects/10/ae7490a1f6894c54b727bd84a05889b1db8ffc', '/.git/objects/10/b37de565a520d0c743bf3d148cffdb597a14df', '/.git/objects/10/b4f635a80dd5742205f90e9a48383eb5a45dac', '/.git/objects/10/b5e2bbd4086ddc791db7fc3a786213e5107286', '/.git/objects/10/b839896461248c56e80d5915ed1ec52914b2d9', '/.git/objects/10/c0ec718241239bc7cf5ca80f26cb03180e8d7c', '/.git/objects/10/c8846d5380b664959d63759591c3a6f604540a', '/.git/objects/10/cc3dd9ffce62367bfd3e274024a84fa4bbf4fc', '/.git/objects/10/e1a2f389c4804375ce951f98069ea0e864c3f6', '/.git/objects/10/e40fb159305494893b1e94e62c18dc14acec9a', '/.git/objects/10/e5e5a2fb3b0739fa07632f8bacc69cd115ba17', '/.git/objects/10/f2d16efc502b92c02236be19116a8906b3b167', '/.git/objects/11/073d080b9f772afb962eaa10e3583a841100fd', '/.git/objects/11/0a03a57b065c62b17946ce2f9c27ae14cd09e9', '/.git/objects/11/52abac92eac8d8b605f61e7608e5151d222f07', '/.git/objects/11/562ae195fafe5127b0a1577159048b0af6fbc4', '/.git/objects/11/6084d6edde5547795dd38c98bb045777a4105f', '/.git/objects/11/671344533a154f203e9bbcff2201bc5befae76', '/.git/objects/11/68066a747c3bef2d6e633b2347c20cc6b56404', '/.git/objects/11/6968b47e00996915b67531127f0954c7ddd1a4', '/.git/objects/11/7f881842de701288d44a04738aeddf2eb62771', '/.git/objects/11/848596c43002718041db85d44d4f17fef2fd2d', '/.git/objects/11/85dd4cec3236757225d3d2261831614c12c71b', '/.git/objects/11/95185617fa4e3585174859ed5709d013f5937a', '/.git/objects/11/a8a92beabf4c3b84689c4b3815e4c19b948151', '/.git/objects/11/b6a93338766923a8e6379405e6fcf4ab828169', '/.git/objects/11/c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/objects/11/e01dd8395bcb4499bbae87a8fa5d396b5bb9a0', '/.git/objects/11/e234b29ee21a975610c871bc3aca80ba403997', '/.git/objects/11/e65f017f9956f02db9d750e814db9c0eb996f6', '/.git/objects/11/ef1e147dfda045cf78a1cbda76be5f212cf533', '/.git/objects/11/f3df8ac49a0be182d46132407e50090bc85a7e', '/.git/objects/12/1b52d4dde57209a1c5d7fad41433f9d7507e7e', '/.git/objects/12/3bbafac5135532670900b0daeade243b64415e', '/.git/objects/12/46c37c3be32064b636700c62bc59120a41a208', '/.git/objects/12/482204acdc7b5906f6985edd7052cf24e81715', '/.git/objects/12/60fee99a4cfcbd9d4ffb0eb2de091a7a472b7b', '/.git/objects/12/782408d18b12ea7c1fd9e5d39ddbfa2040ef21', '/.git/objects/12/8150674170b66350257cc719da038a61a568bf', '/.git/objects/12/8991f222be89980a285c1a719170f19cebd863', '/.git/objects/12/a298fd576dee88bdd1d5b4f72dedf5ebe264d9', '/.git/objects/12/bac80bceda99fedc73290309b748399405be41', '/.git/objects/12/d12afbdb51a82ea91470a68c5936ef307758b3', '/.git/objects/12/db0c6cc3d0ec7d7834be73cbded60279418c53', '/.git/objects/12/ecf89d4939f447a2a13eb6a8584268d822df06', '/.git/objects/12/f27c213102a0ac8c26ec5d35886d36e011d04c', '/.git/objects/13/0454723003170e9f3e6ed225d66f809f6b6dad', '/.git/objects/13/049a15f6a54c096b02c7573999db421178a726', '/.git/objects/13/0b070345feb323ae3fde1c7d932945f3191106', '/.git/objects/13/2b510d6d7bcd743b4cbf1ea79259bf32a0098f', '/.git/objects/13/2c537172da3f2875b3ce54f4b1f5af4cd1eb1f', '/.git/objects/13/2ce036f2fe47610a5925b048748ef75eb541db', '/.git/objects/13/31cd4e5b63c9aa3bfc3c37f80674cc03c74071', '/.git/objects/13/360394a41c8fabc39419ab404191a8575e2799', '/.git/objects/13/3c2a7f8f0c8e8798adb0c95502b796e8304aa0', '/.git/objects/13/53a7a4fc4f5419b52d1dc280f7536194c60122', '/.git/objects/13/92a68ba7c0702c66b4fb266ffd087081b1e141', '/.git/objects/13/afea111e981b60139f5b4ac6b833043651c7b4', '/.git/objects/13/c40173739fb7e84b979f3c6ac5261cec02e012', '/.git/objects/13/c4d03b4a81e20903904c198b11442354c752ac', '/.git/objects/13/d4e7409000e6a4b0bf0196e7c4db9005e68a3a', '/.git/objects/13/dd0ea3ac7cf3fa815ff54ed379ac145c2200aa', '/.git/objects/13/e514857a46401864fca0265d1d7e83a40fc30c', '/.git/objects/13/fb8a33b9d96c2a9ff445c20dea718e895df5e4', '/.git/objects/13/fc3c0fa0f80a29ecc8c44e234a0e433e5e20db', '/.git/objects/14/1292c88425a51c07a6093b433d9954224e31b4', '/.git/objects/14/1a9684900d25f2e7007f7f96c30774a1835b6e', '/.git/objects/14/1b7a38a5eb915f5b73a167f77208e4d2286b00', '/.git/objects/14/28bfd5a05e95735a945cf34906ebf3948fa13a', '/.git/objects/14/3334e584ff71080c606f29c1ef42924bbe453d', '/.git/objects/14/394b47e18f572003e3d82368702dfd474b70c4', '/.git/objects/14/3df4c79cc8ee0249f8509549e5377882a28010', '/.git/objects/14/740e00ca060ea5ea55d359d8e94b78c9b27bad', '/.git/objects/14/74c8f7cf8bc22cda503322795cac94ac621675', '/.git/objects/14/818693e025769bce36db9ab228de95282c660c', '/.git/objects/14/8a5ec5787afd3f553071ecc831a805312f6ece', '/.git/objects/14/8c20fa8c56ae81068aded6b9a8f2a59fc229dd', '/.git/objects/14/9215c98341f0291662bea80be4491d80cce454', '/.git/objects/14/93fb5b0b0a7a8c28aa2e0e11e3024fdd6605a4', '/.git/objects/14/9a72f18b0f5ac8ed9bf713a2c26c76d8158588', '/.git/objects/14/a51ee6f2160b21205c9afd9f7cc99748092bde', '/.git/objects/14/a5b829f9591df4d9d656268f7ad309be05e97f', '/.git/objects/14/b14cb4896fb71ae400bad91fd17aca2dc37cdd', '/.git/objects/14/c258aa37b196e7602622c9d90721c7cdfc96e5', '/.git/objects/14/c2a807581505e916cb62d8d2195af8a6c9fe9b', '/.git/objects/14/dcb371d5f4cc65cc76297ddc5125507b9752fc', '/.git/objects/14/e09849fda36affbc8abb417ca8b46778461bc7', '/.git/objects/14/e4ef69520a217c61e1dfd2f8b23fab0b8f65dc', '/.git/objects/14/ee55bfeb961e36bd64cb902cc11ff3a907a4ba', '/.git/objects/14/f842403e89680c08c9e914aa7da06da74192d5', '/.git/objects/14/fe9bb6670802ae36d1022630b687088b71c35d', '/.git/objects/15/098da0ba5b0e2d399d8688a8a0b6a0fcd68d1d', '/.git/objects/15/3e02e9a9c73af7f51d590516702350390c0c12', '/.git/objects/15/5f8df967724158d80873e629c6c12bb65c8d00', '/.git/objects/15/6916239719ce4eaa5eb0e4105e9537ccd5734c', '/.git/objects/15/6d79f56790f38a4c9d716aa1e76e0d9eaa5ee3', '/.git/objects/15/709f6e54c6706e2d1debd66e87ab969ed3cb3b', '/.git/objects/15/80c27de69b78994d59b6f22fa0e0da62c8705f', '/.git/objects/15/934046b41baa7c1df153b1fa8b4f7b45d6d363', '/.git/objects/15/9a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/objects/15/9bfd26b659195df8c8486d12b5e15f948cb808', '/.git/objects/15/bcd112607d47deea3216fc8137482fd0a57dfd', '/.git/objects/15/be2e474eb938a89e4d7c19737994893197e781', '... [results truncated, try being more specific with your parameters]']
AI: Let me find the actual input files and working artifacts more specifically.[{'name': 'glob', 'args': {'pattern': 'inputs/**/*', 'path': '/'}, 'id': 'call_00_9Z21RcKu6CjOlSt4tJPl2453', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'outputs/**/*', 'path': '/'}, 'id': 'call_01_J8K8GtFFgr97Yufc8aNb8002', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'skills/**/*', 'path': '/'}, 'id': 'call_02_UK1GPQrJQosTcTCWEkdE7765', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/.venv/Lib/site-packages/langchain_core/outputs/__init__.py', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/llm_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/run_info.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/chat_generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/chat_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/llm_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/run_info.py', '/outputs/working/bootstrap_report.json', '/outputs/working/clause_index.json', '/outputs/working/contract_product_profile.json', '/outputs/working/legal_propositions.json', '/outputs/working/source_preflight.json', '/outputs/working/working_artifact_validation.json']
Tool: ['/.venv/Lib/site-packages/anthropic/resources/beta/skills/__init__.py', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/__pycache__/skills.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/__pycache__/versions.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/skills.py', '/.venv/Lib/site-packages/anthropic/resources/beta/skills/versions.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__init__.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_create_params.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_create_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_delete_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_list_params.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_list_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/__pycache__/version_retrieve_response.cpython-314.pyc', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_create_params.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_create_response.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_delete_response.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_list_params.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_list_response.py', '/.venv/Lib/site-packages/anthropic/types/beta/skills/version_retrieve_response.py', '/.venv/Lib/site-packages/openai/resources/skills/__init__.py', '/.venv/Lib/site-packages/openai/resources/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/__pycache__/content.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/__pycache__/skills.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/content.py', '/.venv/Lib/site-packages/openai/resources/skills/skills.py', '/.venv/Lib/site-packages/openai/resources/skills/versions/__init__.py', '/.venv/Lib/site-packages/openai/resources/skills/versions/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/versions/__pycache__/content.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/versions/__pycache__/versions.cpython-314.pyc', '/.venv/Lib/site-packages/openai/resources/skills/versions/content.py', '/.venv/Lib/site-packages/openai/resources/skills/versions/versions.py', '/.venv/Lib/site-packages/openai/types/skills/__init__.py', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/deleted_skill_version.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/skill_version.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/skill_version_list.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/version_create_params.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/__pycache__/version_list_params.cpython-314.pyc', '/.venv/Lib/site-packages/openai/types/skills/deleted_skill_version.py', '/.venv/Lib/site-packages/openai/types/skills/skill_version.py', '/.venv/Lib/site-packages/openai/types/skills/skill_version_list.py', '/.venv/Lib/site-packages/openai/types/skills/version_create_params.py', '/.venv/Lib/site-packages/openai/types/skills/version_list_params.py', '/.venv/Lib/site-packages/openai/types/skills/versions/__init__.py', '/.venv/Lib/site-packages/openai/types/skills/versions/__pycache__/__init__.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/SKILL.md', '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/bootstrap_source_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/export_review_xlsx.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/finalize_discrepancy_json.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_coverage_ledger.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_source_numbering.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/__pycache__/validate_working_artifacts.cpython-314.pyc', '/skills/acquiring-discrepancy-analysis/scripts/bootstrap_source_artifacts.py', '/skills/acquiring-discrepancy-analysis/scripts/export_review_xlsx.py', '/skills/acquiring-discrepancy-analysis/scripts/extract_docx_numbered.py', '/skills/acquiring-discrepancy-analysis/scripts/finalize_discrepancy_json.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_coverage_ledger.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py']
AI: Good. Now let me read the key inputs and existing working artifacts to understand the current state.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_kGi4FfEu8VVY7oEfPcCV7352', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 200}, 'id': 'call_01_o9vSe9hxgsnYZnX7CqqG0876', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/source_preflight.json'}, 'id': 'call_02_EDGxAgLA5TFCL2ZEUjXF0395', 'type': 'tool_call'}]
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
     2	  "path": "inputs\\contract.txt",
     3	  "valid": true,
     4	  "contract_numbering_valid": true,
     5	  "numbered_clause_count": 226,
     6	  "deep_clause_count": 179,
     7	  "top_level_sections": [
     8	    "1",
     9	    "10",
    10	    "11",
    11	    "12",
    12	    "13",
    13	    "2",
    14	    "3",
    15	    "4",
    16	    "5",
    17	    "6",
    18	    "7",
    19	    "8",
    20	    "9"
    21	  ],
    22	  "broken_zero_ids": [],
    23	  "duplicate_ids": [
    24	    "1",
    25	    "1.1",
    26	    "1.2",
    27	    "1.3",
    28	    "10",
    29	    "2",
    30	    "3",
    31	    "4",
    32	    "5"
    33	  ],
    34	  "warnings": []
    35	}
AI: Now let me understand the scope. I need to work on batch 03 covering matrix IDs from 4.2.17 to 5.1.8.13. Let me find these in the matrix and also read the contract text.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix.json to identify all IDs in scope 4.2.17-5.1.8.13', 'status': 'in_progress'}, {'content': 'Read contract.txt to understand contract clause numbering and content', 'status': 'pending'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile)', 'status': 'pending'}, {'content': 'Read existing batch files (batch_01, batch_02) for context', 'status': 'pending'}, {'content': 'Build matrix_batch_03.json with links and unmatched_matrix for IDs 4.2.17-5.1.8.13', 'status': 'pending'}, {'content': 'Write batch_03 to /outputs/working/matrix_batch_03.json', 'status': 'pending'}]}, 'id': 'call_00_E4SbAq0rXLfokIJ1ieHb0828', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix.json to identify all IDs in scope 4.2.17-5.1.8.13', 'status': 'in_progress'}, {'content': 'Read contract.txt to understand contract clause numbering and content', 'status': 'pending'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile)', 'status': 'pending'}, {'content': 'Read existing batch files (batch_01, batch_02) for context', 'status': 'pending'}, {'content': 'Build matrix_batch_03.json with links and unmatched_matrix for IDs 4.2.17-5.1.8.13', 'status': 'pending'}, {'content': 'Write batch_03 to /outputs/working/matrix_batch_03.json', 'status': 'pending'}]
AI: [{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\', encoding=\'utf-8\') as f:\n    matrix = json.load(f)\n# Find all IDs and their indices\nfor i, item in enumerate(matrix):\n    n = item[\'number\']\n    # Check if in range 4.2.17 to 5.1.8.13\n    print(f\'idx={i}  number={n}\')\n"'}, 'id': 'call_00_OpQVR6WbsRUzEljBvyEN9037', 'type': 'tool_call'}]
Tool: idx=0  number=2.1
idx=1  number=2.2
idx=2  number=2.3.1
idx=3  number=2.3.2
idx=4  number=2.3.3
idx=5  number=2.3.4
idx=6  number=2.3.5
idx=7  number=2.3.6
idx=8  number=2.3.7
idx=9  number=2.4
idx=10  number=2.5.1.1
idx=11  number=2.5.2.1
idx=12  number=2.6.1.1
idx=13  number=2.6.2.1
idx=14  number=2.6.2.2
idx=15  number=2.6.3.1
idx=16  number=2.6.3.2
idx=17  number=2.7
idx=18  number=3.1
idx=19  number=3.2
idx=20  number=3.3
idx=21  number=4.1.1
idx=22  number=4.1.2
idx=23  number=4.1.3
idx=24  number=4.2.1
idx=25  number=4.2.2
idx=26  number=4.2.3
idx=27  number=4.2.4
idx=28  number=4.2.5
idx=29  number=4.2.6
idx=30  number=4.2.7
idx=31  number=4.2.8
idx=32  number=4.2.9
idx=33  number=4.2.10
idx=34  number=4.2.11
idx=35  number=4.2.12
idx=36  number=4.2.13
idx=37  number=4.2.14
idx=38  number=4.2.15
idx=39  number=4.2.16.1
idx=40  number=4.2.16.2
idx=41  number=4.2.16.3
idx=42  number=4.2.17
idx=43  number=4.2.18
idx=44  number=4.2.19
idx=45  number=4.2.20.1
idx=46  number=4.2.20.2
idx=47  number=4.2.20.3
idx=48  number=4.2.20.4
idx=49  number=4.2.20.5
idx=50  number=4.2.20.6
idx=51  number=4.2.20.7
idx=52  number=4.2.21.1
idx=53  number=4.2.21.2
idx=54  number=4.2.21.3
idx=55  number=4.2.21.4
idx=56  number=4.2.21.5
idx=57  number=4.2.21.6
idx=58  number=4.2.21.7
idx=59  number=4.2.21.8
idx=60  number=4.2.22
idx=61  number=4.2.23
idx=62  number=4.2.24
idx=63  number=4.2.25
idx=64  number=4.2.26
idx=65  number=5.1.1.1
idx=66  number=5.1.1.2
idx=67  number=5.1.1.3
idx=68  number=5.1.1.4
idx=69  number=5.1.1.5
idx=70  number=5.1.1.6
idx=71  number=5.1.2
idx=72  number=5.1.3
idx=73  number=5.1.4
idx=74  number=5.1.5
idx=75  number=5.1.6
idx=76  number=5.1.7
idx=77  number=5.1.8.1
idx=78  number=5.1.8.2
idx=79  number=5.1.8.3
idx=80  number=5.1.8.4
idx=81  number=5.1.8.5
idx=82  number=5.1.8.6
idx=83  number=5.1.8.7
idx=84  number=5.1.8.8
idx=85  number=5.1.8.9
idx=86  number=5.1.8.10
idx=87  number=5.1.8.11
idx=88  number=5.1.8.12
idx=89  number=5.1.8.13
idx=90  number=5.1.9
idx=91  number=5.1.10
idx=92  number=5.1.11
idx=93  number=5.1.12
idx=94  number=5.1.13
idx=95  number=5.1.14
idx=96  number=5.1.15
idx=97  number=5.1.16
idx=98  number=5.1.17.1
idx=99  number=5.1.17.2
idx=100  number=5.2.1
idx=101  number=5.2.2
idx=102  number=5.2.3
idx=103  number=5.2.4
idx=104  number=5.2.5
idx=105  number=5.2.6
idx=106  number=5.2.7
idx=107  number=5.2.8
idx=108  number=5.2.9
idx=109  number=5.2.10
idx=110  number=5.2.12
idx=111  number=6.1
idx=112  number=6.2
idx=113  number=6.3
idx=114  number=6.4
idx=115  number=6.5
idx=116  number=6.6
idx=117  number=6.7
idx=118  number=6.8
idx=119  number=6.9
idx=120  number=6.10
idx=121  number=6.11
idx=122  number=6.12
idx=123  number=6.13
idx=124  number=6.14
idx=125  number=6.15
idx=126  number=6.16
idx=127  number=6.17
idx=128  number=6.18
idx=129  number=6.20
idx=130  number=6.21
idx=131  number=7.1
idx=132  number=7.2
idx=133  number=7.3
idx=134  number=7.4
idx=135  number=7.5
idx=136  number=7.6
idx=137  number=7.7
idx=138  number=7.8
idx=139  number=7.9
idx=140  number=7.10
idx=141  number=7.11
idx=142  number=7.12
idx=143  number=7.13
idx=144  number=7.14
idx=145  number=7.15
idx=146  number=7.16
idx=147  number=7.17
idx=148  number=8.1
idx=149  number=8.2
idx=150  number=9.1
idx=151  number=9.2
idx=152  number=9.3
idx=153  number=10.1
idx=154  number=10.2
idx=155  number=10.3
idx=156  number=11.1
idx=157  number=11.2
idx=158  number=11.3
idx=159  number=11.4
idx=160  number=11.5
idx=161  number=11.6
idx=162  number=11.7
idx=163  number=11.8
idx=164  number=11.9
idx=165  number=11.10
idx=166  number=11.11
idx=167  number=11.12
idx=168  number=11.13

[Command succeeded with exit code 0]
AI: Now I can see the scope. Batch 03 covers IDs from 4.2.17 (idx=42) to 5.1.8.13 (idx=89). That's 48 matrix items. Let me read those specific items and the contract text.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\', encoding=\'utf-8\') as f:\n    matrix = json.load(f)\n# Print items 42-89 (4.2.17 to 5.1.8.13)\nfor i in range(42, 90):\n    item = matrix[i]\n    print(f\'--- idx={i} number={item[\\"number\\"]} ---\')\n    print(f\'required_type: {item[\\"required_type\\"]}\')\n    print(f\'main_idea: {item[\\"main_idea\\"]}\')\n    print(f\'only_for_product: {item[\\"only_for_product\\"]}\')\n    print(f\'only_for_lot: {item[\\"only_for_lot\\"]}\')\n    print(f\'only_for_terminal: {item[\\"only_for_terminal\\"]}\')\n    print(f\'payment_method: {item[\\"payment_method\\"]}\')\n    print(f\'topics: {item[\\"topics\\"]}\')\n    print(f\'enriched_text (first 300 chars): {item[\\"enriched_text\\"][:300]}\')\n    print()\n"'}, 'id': 'call_00_eG7ADpZ38CjjaozNSSoe3453', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 8
[stderr]     print(f'--- idx={i} number={item[" number\]}
[stderr]                                      ^
[stderr] SyntaxError: unterminated string literal (detected at line 8)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\', encoding=\'utf-8\') as f:\n    matrix = json.load(f)\nfor i in range(42, 90):\n    item = matrix[i]\n    print(\'--- idx=\' + str(i) + \' number=\' + item[\'number\'] + \' ---\')\n    print(\'required_type: \' + item[\'required_type\'])\n    print(\'main_idea: \' + item[\'main_idea\'])\n    print(\'only_for_product: \' + item[\'only_for_product\'])\n    print(\'only_for_lot: \' + item[\'only_for_lot\'])\n    print(\'only_for_terminal: \' + item[\'only_for_terminal\'])\n    print(\'payment_method: \' + item[\'payment_method\'])\n    print(\'topics: \' + str(item[\'topics\']))\n    print(\'enriched_text (first 300): \' + item[\'enriched_text\'][:300])\n    print()\n"'}, 'id': 'call_00_acRcBN7Y4MMfPOdNtKcx7285', 'type': 'tool_call'}]
Tool: --- idx=42 number=4.2.17 ---
required_type: mandatory
main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґРµРЅРёСЏ СЃС‚Р°РЅРґР°СЂС‚Р°, Р° С‚Р°Рє Р¶Рµ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ СЃРѕР±Р»СЋРґР°С‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ PCI DSS', 'РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ Р°С‚С‚РµСЃС‚Р°С‚Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РёР»Рё Р»РёСЃС‚Р° СЃР°РјРѕРѕС†РµРЅРєРё РїРѕ Р·Р°РїСЂРѕСЃСѓ Р±Р°РЅРєР°', 'РЈРєР°Р·Р°РЅРЅС‹Р№ email РґР»СЏ РѕС‚РїСЂР°РІРєРё РґРѕРєСѓРјРµРЅС‚РѕРІ:pcidss@sberbank.ru']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ СЃРѕР±Р»СЋРґРµРЅРёРµ С‚СЂРµР±РѕРІР°РЅРёР№ РЎС‚Р°РЅРґР°СЂС‚Р° PCI DSS, СЂР°Р·РјРµС‰РµРЅРЅРѕРіРѕ РЅР° СЃР°Р№С‚Рµ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚: https://www.pcisecuritystandards.org Рё РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕ Р·Р°РїСЂРѕСЃСѓ Р‘Р°РЅРєР° СЂРµР·СѓР»СЊС‚Р°С‚С‹ РїСЂРѕРІРµРґРµРЅРёСЏ РѕС†РµРЅРєРё СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РІ РІРёРґРµ Р°С‚С‚РµСЃС‚Р°С‚Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РёР»Рё Р»Рё

--- idx=43 number=4.2.18 ---
required_type: mandatory
main_idea: Р’Р°Р¶РЅС‹ С„Р°РєС‚С‹ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, Р° С‚Р°Рє Р¶Рµ РІР°Р¶РµРЅ СЃСЂРѕРє
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РїСЂРµРєСЂР°С‰РµРЅРёРµ РїСЂРёРµРјР° РєР°СЂС‚ Рє РѕРїР»Р°С‚Рµ (СЂРµРіСѓР»РёСЂСѓРµС‚СЃСЏ РґР°С‚Р° РїСЂРµРєСЂР°С‰РµРЅРёСЏ)', 'РџСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° СЃРЅСЏС‚РёРµ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ Рѕ РїСЂРёРµРјРµ РєР°СЂС‚ (СЂРµРіСѓР»РёСЂСѓРµС‚СЃСЏ РґР°С‚Р° СЃРЅСЏС‚РёСЏ)']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЎ РґР°С‚С‹ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРёРµРј Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚СЊ/СѓРґР°Р»РёС‚СЊ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹, РёР·РІРµС‰Р°СЋС‰РёРµ РѕР± РѕР±СЃР»СѓР¶РёРІР°РЅРёРё РљР°СЂС‚. 

--- idx=44 number=4.2.19 ---
required_type: mandatory
main_idea: Р’Р°Р¶РµРЅ, С„Р°РєС‚ С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµ РґРѕР»Р¶РЅРѕ РјРµС€Р°С‚СЊ Р‘Р°РЅРєСѓ, Рё С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РґРѕР»Р¶РЅРѕ РїРѕРјРѕРіР°С‚СЊ Р‘Р°РЅРєСѓ РІ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёРё
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµ РїСЂРµРїСЏС‚СЃС‚РІРѕРІР°С‚СЊ РїСЂРѕРІРµСЂРєРµ СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р°РЅРєР°', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРґРµР№СЃС‚РІРѕРІР°С‚СЊ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЋ РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќРµ РїСЂРёРЅРёРјР°С‚СЊ РјРµСЂ РїСЂРѕС‚РёРІРѕРґРµР№СЃС‚РІРёСЏ Р‘Р°РЅРєСѓ РІ РїСЂРѕРІРµРґРµРЅРёРё РїСЂРѕРІРµСЂРєРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў / Р РµСЃСѓСЂСЃР°  РЅР° РїСЂРµРґРјРµС‚ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РћРїРµСЂР°С†РёР№ Рё/РёР»Рё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РЅРµ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёС… СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў, Р° С‚Р°Рє

--- idx=45 number=4.2.20.1 ---
required_type: mandatory
main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ СЃР°РјРѕ СЃР»РµРґРёС‚ Р·Р° РїСЂРѕС…РѕР¶РґРµРЅРёРµРј РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё, СЂР°Р·РјРµС‰РµРЅРЅРѕРіРѕ РЅР° СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРѕРІРѕРґРёС‚СЊ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ', 'СЃСЃС‹Р»РєР° РЅР° РёРЅСЃС‚СЂСѓРєС†РёСЋ Рѕ РїРѕСЂСЏРґРєРµ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ РћР±РµСЃРїРµС‡РёС‚СЊ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ Рё СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РїСЂРѕС…РѕР¶РґРµРЅРёРµ РІСЃРµРјРё СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° Рѕ РїРѕСЂСЏРґРєРµ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№, СЂР°Р·РјРµС‰РµРЅРЅРѕРј РЅР° СЃР°Р№С‚Рµ: https://www.sber

--- idx=46 number=4.2.20.2 ---
required_type: mandatory
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РїСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїРѕР»СЊР·РѕРІР°Р»Рѕ С‚РµСЂРјРёРЅР°Р»С‹ Рё РџРћ Р‘Р°РЅРєР° С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РїРѕ РјРµСЃС‚Сѓ СѓСЃС‚Р°РЅРѕРІРєРё, РЅРµ РјРµРЅСЏС‚СЊ Рё РЅРµ СЂРµРјРѕРЅС‚РёСЂРѕРІР°С‚СЊ РёС… СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ Рё РЅРµ РїРµСЂРµРґР°РІР°С‚СЊ С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј (РєСЂРѕРјРµ РѕР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё)
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Рё РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕРІРѕСЂР° Рё РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё СЂРµРіРёСЃС‚СЂР°С†РёРё РўРЎРў/СѓСЃС‚Р°РЅРѕРІРєРё СѓСЃС‚СЂРѕР№СЃС‚РІР°', 'Р·Р°РїСЂРµС‚ РІРЅРµСЃРµРЅРёСЏ РёР·РјРµРЅРµРЅРёР№ РІ РџРћ Рё РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ', 'Р·Р°РїСЂРµС‚ СЃР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРіРѕ СЂРµРјРѕРЅС‚Р° РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ', 'Р·Р°РїСЂРµС‚ РїРµСЂРµРґР°С‡Рё РѕР±РѕСЂСѓРґРѕРІР°РЅРёСЏ Рё РґРѕРєСѓРјРµРЅС‚РѕРІ С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, РєСЂРѕРјРµ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ РѕР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ (РІ С‚РѕРј С‡РёСЃР»Рµ С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРёРµ sim-РєР°СЂС‚С‹)/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Рё РїСЂРѕРіСЂР°РјРјРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅРѕРµ Р‘Р°РЅРєРѕРј, С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ СЂРµР°Р»РёР·Р°С†

--- idx=47 number=4.2.20.3 ---
required_type: mandatory
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ СЃС‚РѕРёС‚ Р·Р°РїСЂРµС‚ РЅР° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ РїРѕРґРєР»СЋС‡РµРЅРёСЏ С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ РЅР°СЃС‚СЂРѕР№РєРё С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ СЂРµРјРѕРЅС‚Р° С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ Р·Р°РјРµРЅС‹ С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р”РѕСЃС‚СѓРї РґР»СЏ РІРёР·СѓР°Р»СЊРЅРѕР№ РїСЂРѕРІРµСЂРєРё С‚РµСЂРјРёРЅР°Р»РѕРІ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј СЂР°Р±РѕС‚РЅРёРєР°Рј РћР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё РґРѕСЃС‚СѓРї Рє РјРµСЃС‚Р°Рј СѓСЃС‚Р°РЅРѕРІРєРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ СЂР°Р±РѕС‚ РїРѕ РёС… РїРѕРґРєР»СЋС‡РµРЅРёСЋ

--- idx=48 number=4.2.20.4 ---
required_type: mandatory
main_idea: Р’Р°Р¶РЅРѕ, РµСЃР»Рё СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµ Р±РµР· РґРѕРєСѓРјРµРЅС‚РѕРІ РёР»Рё Р°РєС‚Р° РїРµСЂРµРґР°С‡Рё, С‚Рѕ РІСЃС‘ РѕРє, СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµС‚
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹ / РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РІ РїРѕ Р°РєС‚Сѓ', 'РїРѕРґРїРёСЃР°РЅРёРµ Р°РєС‚Р° СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹РјРё Р»РёС†Р°РјРё', 'РЅР°Р»РёС‡РёРµ РґРІСѓС… СЌРєР·РµРјРїР»СЏСЂРѕРІ Р°РєС‚Р°', 'С…СЂР°РЅРµРЅРёРµ РѕРґРЅРѕРіРѕ СЌРєР·РµРјРїР»СЏСЂР° Р°РєС‚Р° РІ РћР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё', 'С…СЂР°РЅРµРЅРёРµ РІС‚РѕСЂРѕРіРѕ СЌРєР·РµРјРїР»СЏСЂР° Р°РєС‚Р° Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ РџСЂРёРЅСЏС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° Рё/РёР»Рё РїСЂРѕРіСЂР°РјРјРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ РґР»СЏ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ Р°РєС‚Сѓ РїСЂРёРЅСЏС‚РёСЏ РѕРєР°Р·Р°РЅРЅС‹С… СѓСЃР»СѓРі РїРѕ С„РѕСЂРјРµ РћР±СЃР»СѓР¶РёРІР°СЋ

--- idx=49 number=4.2.20.5 ---
required_type: mandatory
main_idea: 
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ Р‘Р°РЅРє Рѕ РІС‹С…РѕРґРµ РёР· СЃС‚СЂРѕСЏ РёР»Рё СѓС‚СЂР°С‚Рµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РёР»Рё РњРѕР±РёР»СЊРЅРѕРіРѕ СѓСЃС‚СЂРѕР№СЃС‚РІР°', 'Р�РЅС„РѕСЂРјРёСЂРѕРІР°РЅРёРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Р°Рј 2.3.1 Рё 2.3.2 Р”РѕРіРѕРІРѕСЂР° РёР»Рё С‡РµСЂРµР· СЃР»СѓР¶Р±Сѓ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°, РІ С‚РѕРј С‡РёСЃР»Рµ РњРѕР±РёР»СЊРЅРѕРіРѕ СѓСЃС‚СЂРѕР№СЃС‚РІР° РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РёР· СЃС‚СЂРѕСЏ РёР»Рё РµРіРѕ СѓС‚СЂР°С‚С‹ РЅРµРјРµРґР»РµРЅРЅРѕ РёРЅС„РѕСЂРјРёСЂРѕРІР°С‚СЊ РѕР± СЌС‚РѕРј Р‘Р°РЅРє РІ 

--- idx=50 number=4.2.20.6 ---
required_type: mandatory
main_idea: 
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°', 'РІРµСЂРЅСѓС‚СЊ С‚РµСЂРјРёРЅР°Р» РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ/СѓСЃС‚РЅРѕРіРѕ С‚СЂРµР±РѕРІР°РЅРёСЏ Р±Р°РЅРєР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ Р’РµСЂРЅСѓС‚СЊ Р‘Р°РЅРєСѓ РёР»Рё РћР±СЃР»СѓР¶РёРІР°СЋС‰РµР№ РєРѕРјРїР°РЅРёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР° РёР»Рё СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ Рї

--- idx=51 number=4.2.20.7 ---
required_type: mandatory
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРј РїСѓРЅРєС‚Рµ РґРѕРіРѕРІРѕСЂР° С€Р»Р° СЂРµС‡СЊ РїСЂРѕ С€С‚СЂР°С„ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»Р° Рё РµРіРѕ СЂР°Р·РјРµСЂ, РёРЅР°С‡Рµ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РјР°С‚СЂРёС†С‹ РЅРµ РѕС‚РЅРѕСЃРёС‚СЃСЏ Рє РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РќРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. РћР±СЏР·Р°РЅРЅРѕСЃС‚СЊ РїСЂРµРґРїСЂРёСЏС‚РёСЏ РѕР± СѓРїР»Р°С‚Рµ С€С‚СЂР°С„Р° Р·Р° РЅРµРІРѕР·РІСЂР°С‚']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РІ РўРЎРў (РўРѕСЂРіРѕРІС‹Р№ СЌРєРІР°Р№СЂРёРЅРі): в†’ Р’ СЃР»СѓС‡Р°Рµ РЅРµРІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ /РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї. 4.2.20.6 Р”РѕРіРѕРІРѕСЂР°, СѓРїР»Р°С‚РёС‚СЊ Р‘Р°РЅРєСѓ С€С‚СЂР°С„ РІ СЂР°Р·РјРµСЂРµ 25 000 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚СЊ С‚С‹СЃСЏС‡) СЂ

--- idx=52 number=4.2.21.1 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РѕРїРµСЂР°С†РёР№ РЅР° СЂРµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РѕРїРµСЂР°С†РёР№ РЅР° С‚РµСЃС‚РѕРІРѕР№ СЃСЂРµРґРµ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РџСЂРёСЃС‚СѓРїРёС‚СЊ Рє РїСЂРѕРІРµРґРµРЅРёСЋ РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ РїСЂРѕРІРµСЂРєРё РІС‹Р±СЂР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў РћРїРµ

--- idx=53 number=4.2.21.2 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РЎРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°.

--- idx=54 number=4.2.21.3 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ СЃСѓРјРј Рє СЃРїРёСЃР°РЅРёСЋ РЅРµ РїРѕР·РґРЅРµРµ 5 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№', 'РЎРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРЅРѕР№ СЃСѓРјРјС‹ С„Р°РєС‚РёС‡РµСЃРєРё РѕРєР°Р·Р°РЅРЅС‹Рј С‚РѕРІР°СЂР°Рј/СѓСЃР»СѓРіР°Рј', 'РЎРѕР±Р»СЋРґРµРЅРёРµ РџРѕСЂСЏРґРєР° РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РџРѕРґС‚РІРµСЂР¶РґР°С‚СЊ Р°РІС‚РѕСЂРёР·РѕРІР°РЅРЅС‹Рµ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РџСЂРµРґР°РІС‚РѕСЂРёР·Р°С†РёРё СЃСѓРјРјС‹ Рє СЃРїРёСЃР°РЅРёСЋ С‡РµСЂРµР· РЎРџР­Рџ РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚Рё) РєР°Р»РµРЅРґР°СЂ

--- idx=55 number=4.2.21.4 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґРёР·Р°Р№РЅР° РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ СЃ Р‘Р°РЅРєРѕРј', 'РЎРѕРіР»Р°СЃРѕРІР°РЅРёРµ СЌР»РµРєС‚СЂРѕРЅРЅС‹С… РІР°СЂРёР°РЅС‚РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РЅР°РєР»РµРµРє СЃ Р‘Р°РЅРєРѕРј']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РЎРѕРіР»Р°СЃРѕРІС‹РІР°С‚СЊ СЃ Р‘Р°РЅРєРѕРј РґРёР·Р°Р№РЅ РџР»Р°С‚РµР¶РЅРѕР№ СЃС‚СЂР°РЅРёС†С‹, РІРєР»СЋС‡Р°СЏ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ РІР°СЂРёР°РЅС‚С‹ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РЅР°РєР»РµРµРє.


--- idx=56 number=4.2.21.5 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёСЋ Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРѕРІРѕРґРёС‚ РёРЅС‚РµРіСЂР°С†РёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ СЃ РґР°С‚С‹ Р·Р°РєР»СЋС‡РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РџСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ РёРЅС‚РµРіСЂР°С†РёРё Р РµСЃСѓСЂСЃР° СЃРѕ РЎРџР­Рџ Рё СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёРµ РёРЅС‚РµРіСЂР°С†РёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»

--- idx=57 number=4.2.21.6 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РЎР°РјРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕ РѕР±РµСЃРїРµС‡РёРІР°С‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ СЃРІРѕРёС… РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… СЂРµСЃСѓСЂСЃРѕРІ РІ СЃРµС‚Рё РёРЅС‚РµСЂРЅРµС‚.

--- idx=58 number=4.2.21.7 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РџСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р‘Р°РЅРєР° РґРѕСЃС‚СѓРї Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј, РЅРµ СЃРІСЏР·Р°РЅРЅС‹Рј СЃ Р°РґРјРёРЅРёСЃС‚СЂРёСЂРѕРІР°РЅРёРµ

--- idx=59 number=4.2.21.8 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РЎРѕР±Р»СЋРґРµРЅРёРµ РїСЂР°РІРёР» РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РћРїРµСЂР°С†РёР№ РЅР° Р РµСЃСѓСЂСЃРµ (Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРі): РїСЂРѕРІРµСЂРєР° РЅР° СЌС‚Р°РїРµ СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° СЃРѕ СЃС‚РѕСЂРѕРЅС‹ Р‘Р  Р“РћРЎР‘ в†’ РЎРѕР±Р»СЋРґР°С‚СЊ РїСЂР°РІРёР»Р° РїРѕР»СЊР·РѕРІР°РЅРёСЏ Р›РёС‡РЅС‹Рј РєР°Р±РёРЅРµС‚РѕРј Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіР°, СЂР°Р·РјРµС‰РµРЅРЅС‹Рј РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°.

--- idx=60 number=4.2.22 ---
required_type: optional
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: qr
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ QR-РєРѕРґ РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ SberPayQR/РџР»Р°С‚Рё QR (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџРѕРєСѓРїР°С‚РµР»СЋ РґР»СЏ СЃС‡РёС‚С‹РІР°РЅРёСЏ QR-РєРѕРґ СЃ С†РµР»СЊСЋ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РѕРїР»Р°С‚С‹ РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј SberPayQR/РџР»Р°С‚Рё QR

--- idx=61 number=4.2.23 ---
required_type: optional
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: qr
topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РЅРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-РєРѕРґСѓ)']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќРµ РёР·РјРµРЅСЏС‚СЊ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ.

--- idx=62 number=4.2.24 ---
required_type: optional
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: qr
topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API РІ СЂР°РјРєР°С… С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'СЃРѕР±Р»СЋРґРµРЅРёРµ РїРѕСЂСЏРґРєР° РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'СѓС‡РµС‚ СѓСЃР»РѕРІРёР№ Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїСЂРё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРё QR-API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р�СЃРїРѕР»СЊР·РѕРІР°С‚СЊ API Рё СЃРІРµРґРµРЅРёСЏ, РїРµСЂРµРґР°РІР°РµРјС‹Рµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј QR-API, РІ РіСЂР°РЅРёС†Р°С… РїСЂР°РІ Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ С‚Р°РєРѕРіРѕ API Рё РµРіРѕ РѕРїРёСЃР°РЅРёСЏ, РёР·Р»РѕР¶РµРЅРЅРѕРіРѕ РІ РџРѕСЂСЏРґРєРµ, СѓСЃР»РѕРІРёСЏС… Рё РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё СЃС‚РѕСЂРѕРЅ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё QR-API, СЂР°Р·РјРµС‰РµРЅРЅРѕРј РЅР° РћС„РёС†РёР°Р»СЊ

--- idx=63 number=4.2.25 ---
required_type: optional
main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: qr
topics: ['РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API - РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)', 'РџСЂРё РІС‹СЏРІР»РµРЅРёРё РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API РѕРїРѕРІРµСЃС‚РёС‚СЊ Р‘Р°РЅРєР° (РґРѕР»Р¶РЅР° Р±С‹С‚СЊ РїСЂСЏРјР°СЏ РѕС‚СЃС‹Р»РєР° Рє QR-API)']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРё РІС‹СЏРІР»РµРЅРёРё С„Р°РєС‚РѕРІ РёР»Рё РїСЂРёР·РЅР°РєРѕРІ РЅР°СЂСѓС€РµРЅРёСЏ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ QR-API Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРѕР·РјРѕР¶РЅРѕСЃС‚РµР№ РѕСЂРіР°РЅРёР·Р°С†РёРё РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РЅРµРјРµРґР»РµРЅРЅРѕ РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ API Рё РѕРїРѕРІРµСЃС‚РёС‚СЊ РѕР± СЌС‚РѕРј Р‘Р°РЅРє Р»СЋР±

--- idx=64 number=4.2.26 ---
required_type: mandatory
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: []
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� РџР Р•Р”РџР Р�РЇРўР�РЇВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р’ РґРѕРїРѕР»РЅРµРЅРёРµ Рє СЃРѕР±Р»СЋРґРµРЅРёСЋ С‚СЂРµР±РѕРІР°РЅРёР№, СѓРєР°Р·Р°РЅРЅС‹С… РІ РЈСЃР»РѕРІРёСЏС…, РІ С‚РѕРј С‡РёСЃР»Рµ РїСЂРёР»РѕР¶РµРЅРёСЏС… Рє РЈСЃР»РѕРІРёСЏРј, РІ С†РµР»СЏС… РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ:
вЂў СЂР°Р·РјРµС‰Р°С‚СЊ РЅР° Р РµСЃСѓСЂСЃРµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРѕРµ СЃРѕРіР»Р°С€РµРЅРёРµ/РѕС„РµСЂС‚Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СЃРѕРґРµСЂР¶

--- idx=65 number=5.1.1.1 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, СЏРІР»СЏСЋС‰РёРµСЃСЏ РЅРµРґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№, СЏРІР»СЏСЋС‰РёС…СЃСЏ РЅРµРґРµР№СЃС‚РІРёС‚РµР»СЊРЅС‹РјРё, РІ СЃР»РµРґСѓСЋС‰РёС… СЃР»СѓС‡Р°СЏС…:
1) РћРїРµСЂР°С†РёСЏ СЃРѕРІРµСЂС€РµРЅР° СЃ РЅР°СЂСѓС€РµРЅРёРµРј Р”РѕРіРѕРІРѕСЂР°, С‚СЂРµР±РѕРІР°РЅРёР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р Р¤ Рё/РёР»Рё РїСЂР°РІРёР» РџР»Р°С‚РµР¶

--- idx=66 number=5.1.1.2 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ РѕС€РёР±РѕС‡РЅРѕ РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ СЃСѓРјРјС‹ СЃ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹, РѕС€РёР±РѕС‡РЅРѕ РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹Рµ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ.

--- idx=67 number=5.1.1.3 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°, РІРѕР·РІСЂР°С‚Р° РїР»Р°С‚РµР¶Р°, СЂРµРІРµСЂСЃРёРІРЅС‹Рµ С‚СЂР°РЅР·Р°РєС†РёРё. Р’Р°Р¶РЅРѕ РЅРµ СЂР°СЃСЃРјР°С‚СЂРёРІР°С‚СЊ РїСѓРЅРєС‚С‹ РІ РєРѕС‚РѕСЂС‹С… РЅРµ СѓРєР°Р·Р°РЅР° С…РѕС‚СЏ Р±С‹ РѕРґРЅР° РёР· СЌС‚РёС… СЃСѓРјРј']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚Р° РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рµ С‚СЂР°РЅР·Р°РєС†РёРё.

--- idx=68 number=5.1.1.4 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ РѕСЃРїРѕСЂРµРЅРЅС‹С… РѕРїРµСЂР°С†РёР№ РёР»Рё СЃРїРёСЃР°РЅРЅС‹С… СЃРѕ СЃС‡С‘С‚Р° РёСЃРїРѕР»СЊРЅРёС‚РµР»СЏ Р±Р°РЅРєРѕРј-СЌРјРёС‚РµРЅС‚РѕРј', 'Р‘Р°РЅРє СѓРґРµСЂР¶РёРІР°РµС‚ СЃСѓРјРјС‹ РѕСЃРїРѕСЂРµРЅРЅС‹С… РѕРїРµСЂР°С†РёР№ РІ СЃР»СѓС‡Р°Рµ СЂРµР°Р»РёР·Р°С†РёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі РџСЂРµРґРїСЂРёСЏС‚РёРµРј РєР°Рє Р°РіРµРЅС‚РѕРј']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РєРѕС‚РѕСЂС‹Рµ Р±С‹Р»Рё РѕСЃРїРѕСЂРµРЅС‹ Рё/РёР»Рё СЃРїРёСЃР°РЅС‹ СЃРѕ СЃС‡РµС‚Р° Р‘Р°РЅРєР° Р‘Р°РЅРєРѕРј вЂ“ СЌРјРёС‚РµРЅС‚РѕРј РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РїРѕ РћРїРµСЂР°С†РёСЏРј, РїСЂРѕРІРµРґРµРЅРЅС‹Рј РІ РўРЎРў

--- idx=69 number=5.1.1.5 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ СѓРґРµСЂР¶РёРІР°С‚СЊ С€С‚СЂР°С„С‹ РёР· СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІРѕР·РЅРёРєС€РёРµ Сѓ Р‘Р°РЅРєР° РІ СЃРІСЏР·Рё РЅРµРґРѕР±СЂРѕСЃРѕРІРµСЃС‚РЅС‹Рј РёСЃРїРѕР»РЅРµРЅРёРµРј Р—Р°РєР°Р·С‡РёРєР° РєРѕРЅС‚СЂР°РєС‚Р°', 'Р‘Р°РЅРє РІРїСЂР°РІРµ СѓРґРµСЂР¶РёРІР°С‚СЊ СѓР±С‹С‚РєРё РёР· СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІРѕР·РЅРёРєС€РёРµ РІ СЃРІСЏР·Рё СЃ РїСЂРёРІР»РµС‡РµРЅРёРµРј Р‘Р°РЅРєР° Рє РіСЂР°Р¶РґР°РЅСЃРєРѕР№ РёР»Рё Р°РґРјРёРЅРёСЃС‚СЂР°С‚РёРІРЅРѕР№ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РёР·-Р·Р° РЅРµРґРѕР±СЂРѕСЃРѕРІРµСЃС‚РЅРѕРіРѕ РёСЃРїРѕР»РЅРµРЅРёРµРј Р—Р°РєР°Р·С‡РёРєР° РєРѕРЅС‚СЂР°РєС‚Р°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Рё РёРЅС‹С… СѓР±С‹С‚РєРѕРІ, РІРѕР·РЅРёРєС€РёС… Сѓ Р‘Р°РЅРєР° РІ СЂРµР·СѓР»СЊС‚Р°С‚Рµ РїСЂРёРјРµРЅРµРЅРёСЏ Рє РЅРµРјСѓ С€С‚СЂР°С„РЅС‹С… СЃР°РЅРєС†РёР№ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РїСЂР°РІРёР»Р°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, Р° С‚Р°РєР¶Рµ РїСЂРёРІР»РµС‡РµРЅРёСЏ 

--- idx=70 number=5.1.1.6 ---
required_type: mandatory
main_idea: Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. 
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ С€С‚СЂР°С„РѕРІ РІ СЃР»СѓС‡Р°Рµ РЅРµРІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї. 4.2.20.7 Р”РѕРіРѕРІРѕСЂР°.

--- idx=71 number=5.1.2 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРёРѕСЃС‚Р°РЅР°РІР»РёРІР°С‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅР°Р»РёС‡РёРё Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РџСЂРёРѕСЃС‚Р°РЅРѕРІРєР° РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РґРѕ РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёРµРј']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РІРѕР·РЅРёРєРЅРѕРІРµРЅРёСЏ Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґРѕ РјРѕРјРµРЅС‚Р° РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё.

--- idx=72 number=5.1.3 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['СЃРїРёСЃР°РЅРёРµ СЃСЂРµРґСЃС‚РІ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ', 'СѓСЃР»РѕРІРёРµ Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р°', 'РѕСЃРЅРѕРІР°РЅРёРµ - Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ Рѕ РїСЂРѕРІРµРґРµРЅРёРё СЂР°СЃС‡РµС‚РѕРІ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРё РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СѓРґРµСЂР¶Р°С‚СЊ СЃСѓРјРјС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї. 5.1.1 Р”РѕРіРѕРІРѕСЂР°, РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРѕСЃР»РµРґСѓСЋС‰РµРјСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, СЃРїРёСЃС‹РІР°С‚СЊ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ (РЅР° СѓСЃР»РѕРІРёСЏС… Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р°, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅРѕРіРѕ Р‘Р°РЅРєСѓ РџСЂРµРґРїСЂРёСЏС‚Рё

--- idx=73 number=5.1.4 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['СѓРєР°Р·Р°РЅ РЅРѕРјРµСЂ СЂР°СЃС‡РµС‚РЅРѕРіРѕ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'СѓРєР°Р·Р°РЅРѕ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ Р‘Р°РЅРєР°, РІ РєРѕС‚РѕСЂРѕРј Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РѕС‚РєСЂС‹С‚ СЃС‡РµС‚']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРё РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СѓРґРµСЂР¶Р°С‚СЊ СЃСѓРјРјС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї. 5.1.1 Р”РѕРіРѕРІРѕСЂР°, РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРѕСЃР»РµРґСѓСЋС‰РµРјСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅР° РѕРїР»Р°С‚Сѓ РёР»Рё РїР»Р°С‚РµР¶РЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ Рѕ СЃРїРёСЃР°РЅРёРё РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ Рє СЂР°СЃС‡РµС‚РЅРѕРјСѓ СЃС‡РµС‚Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ в„– ---------

--- idx=74 number=5.1.5 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅРµ РІРѕР·РјРµС‰Р°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РќРµ РІРѕР·РјРµС‰Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°.

--- idx=75 number=5.1.6 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРµСЂСЏС‚СЊ С‚РµС…РЅРёС‡РµСЃРєРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·Р°РєР°Р·С‡РёРєР° Р·Р° 2 СЂР°Р±РѕС‡РёС… РґРЅСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±РЅРѕРІР»СЏС‚СЊ РџРћ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·Р°РєР°Р·С‡РёРєР° Р·Р° 2 СЂР°Р±РѕС‡РёС… РґРЅСЏ', 'Р”РѕРїСѓСЃРєР°РµС‚СЃСЏ СѓРґР°Р»РµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ РџРћ С‚РµСЂРјРёРЅР°Р»РѕРІ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ РїРѕСЂСЏРґРєР° РѕРїРµСЂР°С†РёР№ Рё Р±РµР· РїСЂРµРґРІР°СЂРёС‚РµР»СЊРЅРѕРіРѕ СѓРІРµРґРѕРјР»РµРЅРёСЏ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїСЂРѕРІРµСЂРєСѓ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ Рё РїРѕСЂСЏРґРєР° СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР°, СЂР°СЃРїРѕР»РѕР¶РµРЅРЅС‹С… РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў. РџСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР°, Р° С‚Р°РєР¶Рµ РѕР±РЅРѕРІР»СЏС‚СЊ РїСЂРѕРіСЂР°

--- idx=76 number=5.1.7 ---
required_type: mandatory
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РїСЂРё РІС‹СЏРІР»РµРЅРёРё РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№', 'Р‘Р°РЅРє РїРµСЂРµРґР°РµС‚ РґР°РЅРЅС‹Рµ РІ РџР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РњР�Р  РїСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РёР·-Р·Р° РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР°', 'РџРµСЂРµРґР°РІР°РµРјР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ РІРєР»СЋС‡Р°РµС‚ РґР°С‚Сѓ Р·Р°РєР»СЋС‡РµРЅРёСЏ Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°, РїСЂРёС‡РёРЅСѓ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Рё РґСЂСѓРіРёРµ СЃРІРµРґРµРЅРёСЏ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РќРµР·Р°РІРёСЃРёРјРѕ РѕС‚ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РёР»Рё РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РћРїРµСЂР°С†РёР№ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ, РІ С‚РѕРј С‡РёСЃР»Рµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїРµСЂРµРґР°С‡Сѓ РґР°РЅРЅС‹С… (СЃРІРµРґРµРЅРёСЏ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў/Р РµСЃСѓСЂСЃРµ, РІ С‚РѕРј С‡РёСЃР»Рµ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ/РїСЂРµРґСЃ

--- idx=77 number=5.1.8.1 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°;

--- idx=78 number=5.1.8.2 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РїСЂРёС‡Р°СЃС‚РЅС‹С… Рє СЌРєСЃС‚СЂРµРјРёР·РјСѓ, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЋ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РІ РѕС‚РЅРѕС€РµРЅРёРё РєРѕС‚РѕСЂС‹С… РёРјРµСЋС‚СЃСЏ

--- idx=79 number=5.1.8.3 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РѕС‚РјС‹РІР°РЅРёРµ РґРµРЅРµРі РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёРµ С‚РµСЂСЂРѕСЂРёР·РјР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїСЂРё РЅР°Р»РёС‡РёРё Сѓ Р‘Р°РЅРєР° РїРѕРґРѕР·СЂРµРЅРёР№, С‡С‚Рѕ РћРїРµСЂР°С†РёРё РІ РўРЎРў/РЅР° Р РµСЃСѓСЂСЃРµ СЃРѕРІРµСЂС€Р°СЋС‚СЃСЏ РІ С†РµР»СЏС… Р»РµРіР°Р»РёР·Р°С†РёРё (Рѕ

--- idx=80 number=5.1.8.4 ---
required_type: optional
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ;

--- idx=81 number=5.1.8.5 ---
required_type: optional
main_idea: 
only_for_product: internet_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё Р—Р°РєР°Р·С‡РёРєРѕРј Р·Р°РїСЂРµС‰РµРЅРЅС‹С… РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё СЃРѕРіР»Р°СЃРЅРѕ РўСЂРµР±РѕРІР°РЅРёСЏРј Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, СѓРєР°Р·Р°РЅРЅС‹С… РІ РўСЂРµР±РѕРІР°РЅРёСЏС… Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ;

--- idx=82 number=5.1.8.6 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ СЂРµСЃСѓСЂСЃРµ РѕС‚ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїРѕР»СѓС‡РµРЅРёРµ РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў /Р РµСЃСѓСЂСЃРµ  РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё Р Р¤

--- idx=83 number=5.1.8.7 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ', 'Р”РѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° СЏРІР»СЏСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹', 'РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РјРѕР¶РµС‚ Р±С‹С‚СЊ РїРѕР»СѓС‡РµРЅРѕ РїРѕ С„Р°РєСЃСѓ РёР»Рё СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚Рµ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїРѕР»СѓС‡РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ РІ РўРЎРў /РЅР° Р РµСЃСѓСЂСЃРµ ;СЃС‚РѕСЂРѕРЅС‹ РґРѕРіРѕРІРѕСЂРёР»РёСЃСЊ, С‡С‚Рѕ РґРѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕ

--- idx=84 number=5.1.8.8 ---
required_type: optional
main_idea: 
only_for_product: trade_acquiring
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РѕРїРµСЂР°С†РёСЏРј', 'Р±Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РґР»СЏ РўРЎРў', 'Р±Р°РЅРє РІРїСЂР°РІРµ РёРЅРёС†РёРёСЂРѕРІР°С‚СЊ СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РґРѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЋ РћРїРµСЂР°С†РёР№;

--- idx=85 number=5.1.8.9 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РІРѕР·Р±СѓР¶РґРµРЅРёРµ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ Р·Р°РєРѕРЅСѓ в„–127-Р¤Р—']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ Р»РёР±Рѕ РІРѕР·Р±СѓР¶РґРµРЅРёРµ РІ РѕС‚РЅРѕС€РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРё

--- idx=86 number=5.1.8.10 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РўРЎРў', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂ

--- idx=87 number=5.1.8.11 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РїСЂРµРґРїСЂРёСЏС‚РёСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РІС‹СЏРІР»РµРЅРЅРѕРј РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі Р·Р°СЏРІР»РµРЅРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ 

--- idx=88 number=5.1.8.12 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ;

--- idx=89 number=5.1.8.13 ---
required_type: optional
main_idea: 
only_for_product: common
only_for_lot: common
only_for_terminal: common
payment_method: common
topics: ['РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°', 'РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°']
enriched_text (first 300): В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°, СѓРєР°Р·Р°РЅРЅРѕРіРѕ РІ Рї. 10.1 Р”РѕРіРѕРІРѕСЂР°.


[Command succeeded with exit code 0]
AI: Good, I now have all 48 matrix items. The output is garbled due to encoding issues but I can see the structure. Let me now read the contract text and the existing working artifacts to understand the contract clauses.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_00_rP1zk3JtoieuXvvdtNdw2114', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 100}, 'id': 'call_01_5IlvnrfjmiYZ8ZWGSfSO8048', 'type': 'tool_call'}]
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
Tool:      1	{
     2	  "matrix": [
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
AI: Now let me read the rest of the contract and the existing batch files to understand what's already been done.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_bRjlOqWbMXNEo5PT8OiX1643', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'outputs/working/matrix_batch_*.json', 'path': '/'}, 'id': 'call_01_ugF3Fji6D0CtswM3KmBU7830', 'type': 'tool_call'}]
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
Tool: []
AI: No existing batch files yet. Let me also check the existing working artifacts and the contract_product_profile.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json', 'limit': 100}, 'id': 'call_00_0uUnehr4Tzaz1pQ7TJMt5302', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/working_artifact_validation.json'}, 'id': 'call_01_seTnRaXbu5sRBByJFJVC8980', 'type': 'tool_call'}]
Tool:      1	{
     2	  "product": [
     3	    "acquiring",
     4	    "qr",
     5	    "sberpay",
     6	    "terminal"
     7	  ],
     8	  "lot": "44_fz",
     9	  "terminal": [],
    10	  "payment_method": [],
    11	  "legal_regime": "44_fz"
    12	}
Tool:      1	{
     2	  "valid": true,
     3	  "errors": [],
     4	  "warnings": [],
     5	  "counts": {
     6	    "expected_matrix_ids": 169,
     7	    "clause_index_matrix_ids": 169,
     8	    "clause_index_contract_rows": 209,
     9	    "source_contract_unique_ids": 189,
    10	    "duplicate_contract_ids": 9,
    11	    "legal_proposition_rows": 0
    12	  },
    13	  "samples": {
    14	    "missing_matrix_ids": []
    15	  }
    16	}
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix.json to identify all IDs in scope 4.2.17-5.1.8.13', 'status': 'completed'}, {'content': 'Read contract.txt to understand contract clause numbering and content', 'status': 'completed'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile)', 'status': 'completed'}, {'content': 'Read existing batch files (batch_01, batch_02) for context', 'status': 'completed'}, {'content': 'Build matrix_batch_03.json with links and unmatched_matrix for IDs 4.2.17-5.1.8.13', 'status': 'in_progress'}, {'content': 'Write batch_03 to /outputs/working/matrix_batch_03.json', 'status': 'pending'}]}, 'id': 'call_00_ZL2qbpubj1K22aVrnm7t9420', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix.json to identify all IDs in scope 4.2.17-5.1.8.13', 'status': 'completed'}, {'content': 'Read contract.txt to understand contract clause numbering and content', 'status': 'completed'}, {'content': 'Read existing working artifacts (clause_index, legal_propositions, contract_product_profile)', 'status': 'completed'}, {'content': 'Read existing batch files (batch_01, batch_02) for context', 'status': 'completed'}, {'content': 'Build matrix_batch_03.json with links and unmatched_matrix for IDs 4.2.17-5.1.8.13', 'status': 'in_progress'}, {'content': 'Write batch_03 to /outputs/working/matrix_batch_03.json', 'status': 'pending'}]

