## Summarized at 2026-06-26T08:23:07.490456+00:00

Human: Matrix batch 2: items 5.1.8.10-6.20
AI: I'll start by reading the skill file and understanding the current state of the project.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 200}, 'id': 'call_00_K7uBG9AqgHuq5YF5Abiy9061', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_locator_registry.json'}, 'id': 'call_01_salJjXBzOfw1N2LtfVRQ7067', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '/outputs/working/**/*'}, 'id': 'call_02_c8qyAfW4t0aLOo1ezeCf0865', 'type': 'tool_call'}]
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
    13	Before analysis and before delegating tasks, read:
    14	
    15	- `references/output-contract.md` for artifact shape and field contracts.
    16	- `references/comparison-patterns.md` for calibration examples.
    17	- `references/delegation-contract.md` for subagent task-packet protocol.
    18	
    19	## Purpose
    20	
    21	Find and explain:
    22	
    23	- Bank-standard matrix requirements preserved by the contract;
    24	- true analogues that deviate from the Bank standard;
    25	- applicable matrix requirements absent from the contract;
    26	- legally meaningful contract terms with no matrix analogue.
    27	- matrix requirements that are out of scope for the current contract profile,
    28	  closed in the internal ledger without final risk reporting.
    29	
    30	The review is risk-oriented. Missing a real risk is worse than marking a
    31	borderline issue as `deviation`, but weak thematic matches must not be promoted
    32	into legal links.
    33	
    34	## Inputs And Outputs
    35	
    36	Inputs:
    37	
    38	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    39	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    40	  applicability filters.
    41	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    42	  ids or real document locators visible in this file.
    43	
    44	Final outputs:
    45	
    46	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    47	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    48	
    49	Working artifacts belong under `/outputs/working/`.
    50	
    51	## Source Hierarchy
    52	
    53	Use the source text as the legal authority:
    54	
    55	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    56	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    57	3. Working ledgers as indexes and evidence aids.
    58	
    59	Do not decide status from extracted fields alone. When a status depends on a
    60	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    61	consequence, re-read the source text.
    62	
    63	## Required Artifacts And Contracts
    64	
    65	Create the artifacts in this order. Each later step depends on the earlier
    66	artifact contract.
    67	
    68	Each step has a hard acceptance gate:
    69	
    70	- the agent or subagent writes the artifact for that step;
    71	- the orchestrator immediately validates the artifact's completeness;
    72	- if the artifact is incomplete, the orchestrator sends that artifact back for
    73	  repair with the validator errors and does not start the next step;
    74	- only an accepted artifact may become input to later legal analysis.
    75	
    76	Final QA is only a release check. It must not be the first time a critical
    77	working artifact is checked.
    78	
    79	### 1. Source Preflight
    80	
    81	Check `inputs/contract.txt` before analysis:
    82	
    83	- real clause numbering is present;
    84	- deep clause numbers are not visibly collapsed or shifted;
    85	- repeated locators have enough context to distinguish source rows;
    86	- text is readable and not corrupted by encoding.
    87	
    88	If the contract text is not usable, stop and write
    89	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
    90	invalid text.
    91	
    92	Gate before source indexing:
    93	
    94	```bash
    95	python skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py inputs/contract.txt --json-out outputs/working/source_preflight.json
    96	```
    97	
    98	Proceed only if the report confirms usable numbering and no fatal extraction
    99	problem. Otherwise stop with the error artifact.
   100	
   101	### 2. Clause Index
   102	
   103	Create `/outputs/working/clause_index.json`.
   104	
   105	It is a source map only. It must include:
   106	
   107	- every matrix `number`;
   108	- every contract clause, operative parent, definition, appendix/table row, and
   109	  unnumbered operative provision;
   110	- source text or source locator for each row;
   111	- context for duplicate printed contract ids.
   112	
   113	Do not use `clause_index` to decide legal status. It only proves source
   114	coverage and valid ids. Never overwrite it with a batch subset.
   115	
   116	Create `/outputs/working/contract_locator_registry.json` from the same source
   117	map. It is the closed list of contract locators:
   118	
   119	- final `contract_id` values must be copied from registry rows with
   120	  `final_allowed = true`;
   121	- appendix starts, table headings, and unnumbered anchors may be
   122	  `evidence_only = true` and cited only in `evidence_locators`;
   123	- do not create semantic, translated, corrected, parenthetical, or synthetic
   124	  contract ids.
   125	
   126	Gate before legal normalization:
   127	
   128	- `clause_index.json` covers every matrix `number`;
   129	- contract rows cover the full source text, including appendices/tables with
   130	  legal content;
   131	- `contract_locator_registry.json` exists and has final-allowed rows for real
   132	  contract clauses;
   133	- evidence-only locators are separated from final-allowed contract ids.
   134	
   135	If the source map is only a subset, repair it before creating or enriching the
   136	legal proposition ledger.
   137	
   138	### 3. Legal Proposition Ledger
   139	
   140	Create and enrich `/outputs/working/legal_propositions.json`.
   141	
   142	This is the mandatory legal evidence ledger. It must contain `matrix` and
   143	`contract` arrays. Every evaluable proposition should include:
   144	
   145	- `id`: matrix number or printed contract locator;
   146	- `source_text`: text used for legal comparison;
   147	- `source_excerpt`: short quote supporting the normalized proposition;
   148	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   149	  `appendix`, `table`, or `technical`;
   150	- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
   151	- `protected_party`, `bound_party`;
   152	- `right_or_obligation`;
   153	- `legal_object`;
   154	- `trigger`;
   155	- `deadline`;
   156	- `amount_formula_cap`;
   157	- `procedure_channel`;
   158	- `liability_remedy`;
   159	- `scope_options`;
   160	- `consequence`;
   161	- `applicability_filters` where available.
   162	
   163	If a legally meaningful row cannot be normalized, mark it
   164	`needs_source_review` and explain the missing element. It is not fully
   165	processed until the source text has been reviewed. Do not proceed to final
   166	matching with unresolved source-review rows that could affect status.
   167	
   168	The bootstrap script may create a seed ledger with many `needs_source_review`
   169	rows. That seed is not accepted for matching. A ledger is accepted only after
   170	all legally meaningful rows have been reviewed and normalized or deliberately
   171	classified as `not_material` / `heading`.
   172	
   173	The ledger is an evidence table, not a substitute for the source. Matching may
   174	use it to find candidates. Status must still be confirmed against source text.
   175	
   176	Run the mechanical check before matching:
   177	
   178	```bash
   179	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working --json-out outputs/working/working_artifact_validation.json
   180	```
   181	
   182	Gate before product/profile analysis and before any matching delegation:
   183	
   184	- the command exits successfully;
   185	- `outputs/working/working_artifact_validation.json` has `"valid": true`;
   186	- no error such as `legal_propositions_needs_source_review`,
   187	  `legal_propositions_missing_source_text`, missing matrix ids, or missing
   188	  registry rows remains.
   189	
   190	If the report is invalid, delegate a repair task for
   191	`legal_propositions.json`, `clause_index.json`, or
   192	`contract_locator_registry.json` as appropriate, then rerun this gate. Do not
   193	start matrix matching, contract-extra review, finalization, or QA while this
   194	gate is failing.
   195	
   196	### 4. Contract Product Profile
   197	
   198	Create `/outputs/working/contract_product_profile.json`.
   199	
   200	Extract from the contract:
Tool:      1	[
     2	  {
     3	    "locator": "1",
     4	    "type": "operative",
     5	    "source_text": "ПРЕДМЕТ КОНТРАКТА",
     6	    "source_excerpt": "ПРЕДМЕТ КОНТРАКТА",
     7	    "source_locator": "1",
     8	    "line_start": 5,
     9	    "line_end": 5,
    10	    "section_context": "г. Сочи «___»________20_ г.",
    11	    "final_allowed": true,
    12	    "evidence_only": false
    13	  },
    14	  {
    15	    "locator": "1.1",
    16	    "type": "operative",
    17	    "source_text": "По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга) (далее - услуги) в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта, а Заказчик обязуется принять и оплатить указанные услуги в порядке и размере установленном настоящим контрактом. Идентификационный код закупки 251231702678823170100100060016619244.",
    18	    "source_excerpt": "По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга) (далее - услуги) в соответс",
    19	    "source_locator": "1.1",
    20	    "line_start": 6,
    21	    "line_end": 7,
    22	    "section_context": "г. Сочи «___»________20_ г.",
    23	    "final_allowed": true,
    24	    "evidence_only": false
    25	  },
    26	  {
    27	    "locator": "1.2",
    28	    "type": "operative",
    29	    "source_text": "Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.",
    30	    "source_excerpt": "Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.",
    31	    "source_locator": "1.2",
    32	    "line_start": 8,
    33	    "line_end": 8,
    34	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    35	    "final_allowed": true,
    36	    "evidence_only": false
    37	  },
    38	  {
    39	    "locator": "1.3",
    40	    "type": "operative",
    41	    "source_text": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.",
    42	    "source_excerpt": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.",
    43	    "source_locator": "1.3",
    44	    "line_start": 9,
    45	    "line_end": 9,
    46	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    47	    "final_allowed": true,
    48	    "evidence_only": false
    49	  },
    50	  {
    51	    "locator": "2",
    52	    "type": "heading",
    53	    "source_text": "ТЕРМИНЫ, ОПРЕДЕЛЕНИЯ И ВЗАИМОДЕЙСТВИЕ",
    54	    "source_excerpt": "ТЕРМИНЫ, ОПРЕДЕЛЕНИЯ И ВЗАИМОДЕЙСТВИЕ",
    55	    "source_locator": "2",
    56	    "line_start": 10,
    57	    "line_end": 10,
    58	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    59	    "final_allowed": false,
    60	    "evidence_only": true
    61	  },
    62	  {
    63	    "locator": "2.1",
    64	    "type": "operative",
    65	    "source_text": "Авторизация – процедура получения разрешения от банка-эмитента или иного юридического лица, действующего от его имени, на проведение операции;",
    66	    "source_excerpt": "Авторизация – процедура получения разрешения от банка-эмитента или иного юридического лица, действующего от его имени, на проведение операции;",
    67	    "source_locator": "2.1",
    68	    "line_start": 11,
    69	    "line_end": 11,
    70	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    71	    "final_allowed": true,
    72	    "evidence_only": false
    73	  },
    74	  {
    75	    "locator": "2.1.1",
    76	    "type": "operative",
    77	    "source_text": "банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы, являющаяся электронным средством платежа. Для совершения операций в ТСТ. Карта может быть представлена на физическом носителе, путем указания её реквизитов, а также через мобильное устройство, которое позволяет его покупателю совершать операции по технологии беспроводной высокочастотной связи малого радиуса действия (NFC);",
    78	    "source_excerpt": "банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы, являющаяся электронным средством платежа. Для совершения операций в ТСТ. Карта может быть представлена на физическом носител",
    79	    "source_locator": "2.1.1",
    80	    "line_start": 12,
    81	    "line_end": 12,
    82	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    83	    "final_allowed": true,
    84	    "evidence_only": false
    85	  },
    86	  {
    87	    "locator": "2.1.2",
    88	    "type": "operative",
    89	    "source_text": "банк-эквайрер - кредитная организация, являющаяся участником платежной системы, организующая точки приема карт и осуществляющая весь комплекс финансовых операций, связанных с выполнением расчетов и платежей по картам в этих точках;",
    90	    "source_excerpt": "банк-эквайрер - кредитная организация, являющаяся участником платежной системы, организующая точки приема карт и осуществляющая весь комплекс финансовых операций, связанных с выполнением расчетов и платежей по картам в этих точках;",
    91	    "source_locator": "2.1.2",
    92	    "line_start": 13,
    93	    "line_end": 13,
    94	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
    95	    "final_allowed": true,
    96	    "evidence_only": false
    97	  },
    98	  {
    99	    "locator": "2.1.3",
   100	    "type": "operative",
Tool: ['/outputs/working/bootstrap_report.json', '/outputs/working/clause_index.json', '/outputs/working/contract_locator_registry.json', '/outputs/working/contract_product_profile.json', '/outputs/working/enrich_ledger.py', '/outputs/working/legal_propositions.json', '/outputs/working/source_preflight.json', '/outputs/working/validate_profile.py', '/outputs/working/working_artifact_validation.json']
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'offset': 200, 'limit': 200}, 'id': 'call_00_sE4JtRHQL6GKCnKKS3Qn6580', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md'}, 'id': 'call_01_F537rPZ4YbmiXhgxT9ar2678', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md'}, 'id': 'call_02_LAzt0hVTwBcUTmnGLnpE2617', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/delegation-contract.md'}, 'id': 'call_03_uH0oXq8VXeWq0O5AWHnL2623', 'type': 'tool_call'}]
Tool:    201	
   202	- product and payment channels;
   203	- lot/procurement type;
   204	- terminal/payment-device scope;
   205	- payment methods;
   206	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   207	
   208	Apply matrix filters before status:
   209	
   210	- `common` applies to every contract.
   211	- A filtered matrix item applies only when the profile matches
   212	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   213	- Mandatory applicable missing = high risk.
   214	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   215	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   216	  profile-based reason. Do not put them in final `unmatched_matrix`.
   217	- Optional applicable missing = low or conditional risk.
   218	- Slash-separated alternatives are options unless the matrix says all options
   219	  are mandatory.
   220	- Placeholder or blank in an applicable material term creates low-risk
   221	  `deviation` only for the exact requirement where the blank is a material
   222	  element. It must not downgrade neighboring channels, sibling duties, or an
   223	  entire package whose legal result is otherwise preserved.
   224	
   225	Gate before matching:
   226	
   227	- the profile is sourced from contract text, not guessed;
   228	- every profile-based `out_of_scope` or `not_applicable` closure has a matrix
   229	  filter reason tied to product, lot, terminal, payment method, or legal
   230	  regime;
   231	- applicable matrix ids remain available for matching and are not silently
   232	  removed by profile filtering.
   233	
   234	Write profile-based matrix closures to the working coverage ledger or to the
   235	matrix batch fragment that owns the id. They are internal closures, not final
   236	risks.
   237	
   238	## Analogue Threshold
   239	
   240	Create a final link only when the contract proposition is a true legal analogue
   241	of the matrix proposition. Test:
   242	
   243	- same or equivalent protected party;
   244	- same or equivalent bound party;
   245	- same legal object;
   246	- same operative right, duty, prohibition, permission, remedy, or allocation of
   247	  risk;
   248	- material trigger, scope, procedure, and consequence are the same or legally
   249	  equivalent.
   250	
   251	Reject weak thematic candidates. A clause about the same broad topic is not a
   252	legal analogue when it governs a different object, party, trigger, procedure,
   253	or consequence.
   254	
   255	Common weak candidates to reject:
   256	
   257	- technical QR/card/terminal capability, advertising, or product description
   258	  does not satisfy a duty to provide a named payment product or operational
   259	  mechanism;
   260	- a general duty to provide personal data or consent does not satisfy a Bank
   261	  right to transfer fraud, payment-system, or issuer-verification information;
   262	- a general right to request documents does not satisfy a special right to
   263	  verify an operation through an issuer, payment system, or other named source;
   264	- general fault-based liability does not satisfy a special Bank exemption from
   265	  transfer delays, payment-system failures, or third-party delays.
   266	
   267	## Bidirectional Matching
   268	
   269	Perform both directions.
   270	
   271	Matrix to contract:
   272	
   273	- for each applicable evaluable matrix proposition, retrieve all contract
   274	  clauses that collectively cover the Bank-standard requirement;
   275	- use focused package recall: every final `contract_id` must cover a named
   276	  material element of the analyzed matrix proposition;
   277	- include a parent/root clause only when it creates the same right, duty,
   278	  procedure, basis, list of grounds, or consequence for that proposition;
   279	- include a child/detail clause only when it carries the same proposition's
   280	  deadline, amount, fee, penalty, formula, cap, ground, exception, procedure,
   281	  channel, remedy, or consequence;
   282	- include companion payment, acceptance, liability, termination,
   283	  document-exchange, appendix, or table clauses only when they govern the same
   284	  legal object and cure, change, or evidence a specific material element;
   285	- do not include clauses that are merely adjacent by section, same parent, same
   286	  topic, or useful background; record them as rejected or considered context;
   287	- if a material element remains uncovered, continue checking the source index
   288	  and ledger for possible clauses, but the purpose is to accept true analogues
   289	  or reject weak candidates, not to enlarge the final group;
   290	- a framework or legal-compliance clause may be a standalone analogue only when
   291	  it carries the same legal object or allocates the same risk, duty, or remedy.
   292	
   293	Matrix-batch gate:
   294	
   295	- every assigned matrix id appears in the fragment coverage ledger as
   296	  `linked`, `missing_in_contract`, `out_of_scope`, `not_applicable`, or
   297	  source-based `not_evaluable`;
   298	- each `linked` id has at least one focused final link;
   299	- each applicable missing id has an explicit `unmatched_matrix` row with
   300	  rejected weak candidates and `candidate_search_exhausted = true`;
   301	- no assigned id is left only for the finalizer to infer later.
   302	
   303	Contract to matrix:
   304	
   305	- for each evaluable contract proposition, find the matrix analogue group;
   306	- if none exists and the term has independent legal effect, classify it as
   307	  `extra_in_contract`;
   308	- close it as `not_material` only for headings, non-operative definitions,
   309	  requisites, signatures, blank forms, or other rows without standalone legal
   310	  effect. Do not use generic reasons such as "no final legal finding produced".
   311	- procurement/customer clauses with independent control, rejection,
   312	  acceptance, withholding, unilateral refusal, penalty, defect-cure,
   313	  force-majeure proof, reporting, audit, or no-change effect are
   314	  `extra_in_contract` when there is no true matrix analogue.
   315	
   316	Contract-review gate:
   317	
   318	- every assigned evaluable contract locator is closed as linked,
   319	  `extra_in_contract`, or source-based `not_material`;
   320	- `not_material` has a legal reason tied to the source text;
   321	- `extra_in_contract` has non-empty risk and materiality reason;
   322	- the same final-allowed contract locator is not both linked and extra.
   323	
   324	Group related ids into many-to-many `links`. One matrix id may need several
   325	contract clauses. One contract clause may cover several matrix ids.
   326	
   327	A group link is allowed only for an indivisible legal package. Sibling matrix
   328	ids under the same parent are not automatically one group. Channels, grounds
   329	for withholding, termination bases, personal-data duties, liability children,
   330	and document-exchange subrequirements should stay as focused links when each
   331	has its own legal element.
   332	
   333	Before merge, validate each fragment immediately:
   334	
   335	```bash
   336	python skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py <fragment-path> --registry outputs/working/contract_locator_registry.json --json-out <fragment-validation-path>
   337	```
   338	
   339	For matrix batches, also pass the assigned matrix ids. Merge only fragments
   340	whose validation report is accepted. Repair invalid fragments before merging.
   341	
   342	## Group-Level Status
   343	
   344	Assign status to the group, not to each atomic pair.
   345	
   346	- `aligned`: the contract package preserves the matrix legal result.
   347	- `deviation`: a true analogue exists, but any material element is changed,
   348	  narrowed, weakened, omitted, shifted, or blank.
   349	- `missing_in_contract`: no true contract analogue exists for an applicable
   350	  matrix requirement.
   351	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   352	  analogue.
   353	- `not_material`: internal ledger closure only; exclude from final report.
   354	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
   355	  final report because the requirement does not apply to the current product,
   356	  lot, terminal, payment method, or legal regime.
   357	
   358	Material elements include party, legal object, operative act, trigger,
   359	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   360	remedy, exception, Bank right, merchant duty, and consequence.
   361	
   362	Status containment:
   363	
   364	- a gap affects only the matrix id where that gap is a material element;
   365	- do not spread one missing deadline, blank channel, absent consent, changed
   366	  amount, or weak candidate across sibling requirements;
   367	- if one large group mixes aligned and deviating siblings, split it before
   368	  assigning status;
   369	- root/parent clauses may appear in several focused groups, but their presence
   370	  does not make all children share one status.
   371	
   372	Hard terms must be compared directly:
   373	
   374	- same material deadline/amount/procedure in the same legal obligation can be
   375	  `aligned`;
   376	- changed value or missing value is `deviation`;
   377	- a hard term from another clause counts only when that clause expressly
   378	  governs the same obligation or is explicitly incorporated;
   379	- a neighboring date, amount, or procedure for another legal object cannot cure
   380	  the gap.
   381	
   382	Do not downgrade for formal differences alone: heading, title, appendix label,
   383	permitted option selection, equivalent mandatory-law mechanism, or wording
   384	style.
   385	
   386	Do not downgrade for low-risk notes when the legal result is preserved. If the
   387	reason says the difference is merely terminological, beneficial to the Bank,
   388	already incorporated through another clause, or caused only by a mandatory
   389	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
   390	
   391	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
   392	when it materially worsens or changes a Bank-standard term: payment timing,
   393	acceptance control, withholding right, penalty/cap, termination power, protected
   394	party, evidence channel, or enforceability.
   395	
   396	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
   397	Before marking a liability group `aligned`, check the amount, formula, cap,
   398	trigger, protected party, excluded delay/non-delay buckets, and claim procedure
   399	across the whole package.
   400	
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
    14	- `/outputs/working/source_preflight.json`
    15	- `/outputs/working/clause_index.json`
    16	- `/outputs/working/legal_propositions.json`
    17	- `/outputs/working/contract_locator_registry.json`
    18	- `/outputs/working/contract_product_profile.json`
    19	- `/outputs/working/working_artifact_validation.json`
    20	- fragment validation reports under `/outputs/working/`
    21	
    22	Each working artifact is accepted at the stage where it is produced. Do not
    23	wait for final QA to discover that a preflight, source map, legal proposition
    24	ledger, profile, or fragment is incomplete.
    25	
    26	Stage acceptance reports:
    27	
    28	- `source_preflight.json`: contract text is usable for analysis.
    29	- `working_artifact_validation.json`: `clause_index.json`,
    30	  `legal_propositions.json`, and `contract_locator_registry.json` are complete
    31	  enough for legal comparison.
    32	- fragment validation reports: assigned ids were processed and all final
    33	  contract locators are registry-allowed.
    34	- `coverage_validation.json`: final JSON closes matrix and contract coverage
    35	  according to this output contract.
    36	
    37	`clause_index.json` is a source map. It contains source ids and text, but no
    38	final legal status.
    39	
    40	`contract_locator_registry.json` is the canonical source of contract locators.
    41	Every final `contract_id` must be a registry `locator` with
    42	`final_allowed = true`. Real appendix/table rows may be final locators when
    43	they contain independent legal content and are source-derived registry rows.
    44	Appendix starts, table headings, and unnumbered source anchors may be registry
    45	rows with `evidence_only = true`; cite them only in `evidence_locators`, never
    46	in `contract_ids`, `candidate_contract_ids`, `atomic_links[].contract_id`,
    47	`unmatched_contract[].contract_id`, `rejected_contract_ids[].contract_id`, or
    48	`unmatched_matrix[].rejected_candidates[].contract_id`.
    49	
    50	`legal_propositions.json` is the legal evidence ledger. It must contain:
    51	
    52	```json
    53	{
    54	  "matrix": [
    55	    {
    56	      "id": "<matrix number>",
    57	      "source_text": "<matrix enriched/source text>",
    58	      "source_excerpt": "<short quote>",
    59	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    60	      "materiality": "evaluable|not_material|heading|needs_source_review",
    61	      "protected_party": "<party protected by the rule>",
    62	      "bound_party": "<party bound by the rule>",
    63	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    64	      "legal_object": "<regulated object>",
    65	      "trigger": "<event/condition>",
    66	      "deadline": "<deadline if any>",
    67	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    68	      "procedure_channel": "<procedure/channel if any>",
    69	      "liability_remedy": "<liability/remedy if any>",
    70	      "scope_options": ["<scope option>"],
    71	      "consequence": "<legal consequence>",
    72	      "applicability_filters": {}
    73	    }
    74	  ],
    75	  "contract": [
    76	    {
    77	      "id": "<printed contract locator>",
    78	      "source_text": "<contract clause text>",
    79	      "source_excerpt": "<short quote>",
    80	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    81	      "materiality": "evaluable|not_material|heading|needs_source_review",
    82	      "protected_party": "<party protected by the rule>",
    83	      "bound_party": "<party bound by the rule>",
    84	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    85	      "legal_object": "<regulated object>",
    86	      "trigger": "<event/condition>",
    87	      "deadline": "<deadline if any>",
    88	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    89	      "procedure_channel": "<procedure/channel if any>",
    90	      "liability_remedy": "<liability/remedy if any>",
    91	      "scope_options": ["<scope option>"],
    92	      "consequence": "<legal consequence>"
    93	    }
    94	  ]
    95	}
    96	```
    97	
    98	Rows marked `needs_source_review` are not complete. Resolve them before final
    99	status if they can affect a link, missing item, or contract-only finding.
   100	The seed ledger created by mechanical bootstrap is not accepted for matching
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
    63	legal object and effect are genuinely shared. If the listed duties are
    64	independent sibling requirements, split them into focused links even if they
    65	come from the same parent clause.
    66	
    67	## 7. Mandatory Missing
    68	
    69	Matrix item is mandatory and applicable to the contract profile. No true
    70	contract analogue exists.
    71	
    72	Result: `missing_in_contract` with high risk.
    73	
    74	## 8. Out Of Scope Matrix Requirement
    75	
    76	Matrix item is filtered to a product, lot, terminal, payment method, or legal
    77	regime not used by the contract.
    78	
    79	Result: close it in `coverage_ledger.matrix` as `out_of_scope` or
    80	`not_applicable` with the profile reason. Do not put it in final
    81	`unmatched_matrix`, and do not force a weak link.
    82	
    83	## 9. Optional Applicable Missing
    84	
    85	Matrix item is optional but applicable to the selected product/profile. No true
    86	contract analogue exists.
    87	
    88	Result: `missing_in_contract` with low or conditional risk.
    89	
    90	## 10. Slash Options
    91	
    92	Matrix lists `cards / QR / mobile pay / smart terminal` as alternatives.
    93	Contract selects `cards / QR`, and the profile confirms only those services are
    94	in scope.
    95	
    96	Result: `aligned` for scope. Absence of unselected alternatives is not a
    97	deviation.
    98	
    99	## 11. Placeholder In Applicable Term
   100	
Tool:      1	# Delegation Contract
     2	
     3	This is an orchestration protocol, not legal methodology.
     4	
     5	## Task Packet
     6	
     7	Every subagent task must include:
     8	
     9	- assigned scope: matrix ids, contract ids, or artifact path to review;
    10	- input paths: `/inputs/matrix.json`, `/inputs/contract.txt`;
    11	- working paths: `/outputs/working/clause_index.json`,
    12	  `/outputs/working/legal_propositions.json`,
    13	  `/outputs/working/contract_locator_registry.json`;
    14	- expected fragment path under `/outputs/working/`;
    15	- required output arrays for the role;
    16	- validation command to run before returning.
    17	
    18	The orchestrator may pass neutral orientation, such as contract type, party
    19	roles, product scope, and legal regime. It must not pass preselected legal
    20	pairs, expected statuses, or answer-like clause lists.
    21	
    22	The subagent must produce reasoning-backed legal findings. It may use helper
    23	scripts for mechanical parsing, filtering, validation, and formatting, but it
    24	must not use scripts or formulas to score legal similarity, select final links,
    25	or decide statuses. The task packet should say this explicitly when the scope is
    26	matching or status review.
    27	
    28	## Stage-Gate Protocol
    29	
    30	The orchestrator controls the pipeline through artifact handoffs.
    31	
    32	For every critical artifact:
    33	
    34	1. Assign a producer task or create the artifact directly.
    35	2. Require the producer to write the artifact under `/outputs/working/`.
    36	3. Run the relevant validator immediately after the artifact appears.
    37	4. If validation fails, send the same artifact back for repair with the exact
    38	   validator errors.
    39	5. Do not start the next stage until the gate report is accepted.
    40	
    41	Critical gates:
    42	
    43	- source preflight before source indexing;
    44	- clause index and locator registry before legal proposition enrichment;
    45	- legal proposition ledger before product/profile filtering and matching;
    46	- product profile and scope closures before matrix batches;
    47	- each matrix or contract fragment before merge;
    48	- merged final JSON before export/release.
    49	
    50	`legal_propositions.json` is the most important early gate. A mechanically
    51	seeded ledger with unresolved `needs_source_review` rows is an unfinished
    52	artifact, not a usable matching input.
    53	
    54	## Locator Rules
    55	
    56	- Use final `contract_id` values only from
    57	  `/outputs/working/contract_locator_registry.json` where `final_allowed = true`.
    58	- Use `evidence_locators` for appendix starts, table anchors, and unnumbered
    59	  source anchors.
    60	- Evidence-only locators cannot be used as accepted candidates, rejected
    61	  candidates, atomic link ids, or extra contract ids.
    62	- Do not create semantic or derived ids such as `Приложение_1_п5` or
    63	  `Приложение_1_п5_комиссия`.
    64	
    65	## Fragment Acceptance
    66	
    67	Before a fragment is merged, run:
    68	
    69	```bash
    70	python skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py <fragment-path> --registry outputs/working/contract_locator_registry.json
    71	```
    72	
    73	For matrix batches, also pass assigned ids:
    74	
    75	```bash
    76	python skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py <fragment-path> --registry outputs/working/contract_locator_registry.json --assigned-matrix-ids "<comma-separated ids>"
    77	```
    78	
    79	If validation fails, repair the fragment once using only the reported errors.
    80	If it still fails, do not merge it; write the validator report under
    81	`/outputs/working/` and mark the run incomplete for orchestration recovery.
    82	
    83	Fragment validation is a handoff gate, not a final QA task. The orchestrator
    84	must run it when the fragment is returned, before any merge/finalizer step.
    85	
    86	## Merge Rules
    87	
    88	- Merge only validated fragments.
    89	- Do not merge fragments whose final links/statuses are justified by automatic
    90	  scores, keyword overlap, token overlap, section proximity, or other mechanical
    91	  ranking.
    92	- Do not merge overbroad same-topic or same-parent groups unless every listed
    93	  contract locator contributes a named material element to the same legal
    94	  result.
    95	- Do not merge a fragment that spreads one placeholder, channel, deadline,
    96	  amount, consent, or liability gap across independent sibling requirements.
    97	- A contract locator cannot be both linked and `extra_in_contract`.
    98	- `coverage_ledger` is derived from validated final arrays and accepted
    99	  out-of-scope / not-applicable matrix closures.
   100	- Structural QA blocks invalid ids, duplicate closure conflicts, schema gaps,
AI: Now let me read the rest of the skill file and the output contract, plus examine the existing working artifacts:[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'offset': 400, 'limit': 200}, 'id': 'call_00_vYSTE1xkQ0IujDRSIaRz8220', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'offset': 100, 'limit': 200}, 'id': 'call_01_7DqpM1TOt2iJ2QWxCsCc5727', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'offset': 100}, 'id': 'call_02_0CqjSgAoNBxTUdKVrf8E9971', 'type': 'tool_call'}]
Tool:    401	## Risk Calibration
   402	
   403	Use `risk_level` consistently:
   404	
   405	- `none`: only for `aligned`;
   406	- `low`: optional applicable missing, placeholder, formal but legally manageable
   407	  gap;
   408	- `medium`: material deviation that can affect performance, evidence, payment,
   409	  control, liability, or enforceability;
   410	- `high`: mandatory missing, changed protected party, major payment/remedy
   411	  change, important Bank right omitted, or broad contract-only risk.
   412	
   413	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   414	a short evidence-based reason. Use concise quotes rather than long excerpts.
   415	
   416	## Final QA
   417	
   418	Before writing final artifacts, perform only release checks over already
   419	accepted stage artifacts:
   420	
   421	- verify the source preflight, source-map, legal-ledger, profile/scope,
   422	  fragment, and merge gates were completed before finalization;
   423	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   424	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   425	  `coverage_ledger`;
   426	- verify every applicable evaluable matrix id is linked or in
   427	  `unmatched_matrix`;
   428	- verify out-of-scope / non-applicable matrix ids are not in final
   429	  `unmatched_matrix`;
   430	- verify every material contract id is closed as linked or extra;
   431	- verify `coverage_ledger` is derived from final `links`,
   432	  `unmatched_matrix`, and `unmatched_contract`;
   433	- verify every final id is visible in source text;
   434	- verify final `contract_id` values are registry-final-allowed and evidence-only
   435	  locators appear only in `evidence_locators`;
   436	- verify each final `contract_id` contributes a named element to its focused
   437	  group; otherwise split the group or reject the clause;
   438	- verify same-parent siblings do not share a deviation merely because they are
   439	  near each other;
   440	- verify `aligned` has no material discrepancy;
   441	- verify every `deviation` has a named legal gap and evidence;
   442	- verify weak candidates are not in final `links`;
   443	- verify `not_material` closures have a source-based legal reason and are not
   444	  placeholders for unreviewed contract terms;
   445	- verify non-material contract rows are absent from final `unmatched_contract`;
   446	- verify summary counts equal final arrays.
   447	
   448	If Final QA finds a critical working-artifact problem, do not patch only the
   449	final JSON. Return to the failed stage, repair that artifact, rerun its gate,
   450	and rebuild downstream artifacts.
   451	
   452	## Output Discipline
   453	
   454	Follow `references/output-contract.md`.
   455	
   456	The final JSON must contain:
   457	
   458	- `analysis_profile`
   459	- `links`
   460	- `atomic_links`
   461	- `unmatched_matrix`
   462	- `unmatched_contract`
   463	- `coverage_ledger`
   464	- `summary`
   465	
   466	`links` carry group-level legal findings. `atomic_links` are traceability
   467	projections only and must inherit the group relationship. Do not assign
   468	separate final pair-level statuses.
   469	
   470	## Tools And Scripts
   471	
   472	Use helper scripts for mechanical work: source extraction, indexing,
   473	normalization checks, batch completeness, coverage validation, JSON schema
   474	checks, and Excel export. Do not put legal mapping or status decisions into
   475	hardcoded scripts.
Tool:    101	until the working-artifact gate passes with `valid = true`.
   102	
   103	Do not delegate matrix matching, contract-only review, merge, finalization, or
   104	QA while `working_artifact_validation.json` reports any
   105	`legal_propositions_needs_source_review`, missing source text, missing matrix
   106	ids, or missing registry rows.
   107	
   108	## Final JSON Shape
   109	
   110	```json
   111	{
   112	  "analysis_profile": {
   113	    "contract_product_profile": {
   114	      "product": ["<selected product/channel>"],
   115	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
   116	      "terminal": ["<selected terminal/payment device>"],
   117	      "payment_method": ["<selected payment method>"],
   118	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
   119	    },
   120	    "source_preflight": {
   121	      "contract_numbering_valid": true,
   122	      "notes": []
   123	    }
   124	  },
   125	  "links": [
   126	    {
   127	      "matrix_ids": ["<matrix id>"],
   128	      "contract_ids": ["<contract locator>"],
   129	      "relationship": "aligned|deviation",
   130	      "legal_topic": "<short legal topic>",
   131	      "matrix_standard": "<bank standard requirement group>",
   132	      "contract_position": "<counterparty contract position group>",
   133	      "matrix_evidence": "<short matrix quote>",
   134	      "contract_evidence": "<short contract quote>",
   135	      "evidence_locators": ["<registry locator used only as supporting evidence>"],
   136	      "status_reason": "<group-level reason>",
   137	      "risk_level": "none|low|medium|high",
   138	      "covered_elements": ["<matrix provisions covered by contract candidates>"],
   139	      "uncovered_elements": ["<matrix provisions still missing/changed/weak>"],
   140	      "candidate_contract_ids": ["<accepted candidate contract locator>"],
   141	      "rejected_contract_ids": [
   142	        {
   143	          "contract_id": "<reviewed non-candidate locator>",
   144	          "reason": "<why it is not a true analogue or cannot cure the gap>"
   145	        }
   146	      ],
   147	      "candidate_search_exhausted": true,
   148	      "search_scope": "full_contract|targeted_domain",
   149	      "discrepancies": [
   150	        {
   151	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   152	          "description": "<material difference>",
   153	          "risk": "<why this matters for the Bank>"
   154	        }
   155	      ]
   156	    }
   157	  ],
   158	  "atomic_links": [
   159	    {
   160	      "matrix_id": "<one matrix id>",
   161	      "contract_id": "<one contract locator>",
   162	      "relationship": "aligned|deviation",
   163	      "link_index": 0,
   164	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   165	      "coverage": "<what this contract locator contributes to the group>"
   166	    }
   167	  ],
   168	  "unmatched_matrix": [
   169	    {
   170	      "matrix_id": "<matrix id>",
   171	      "requirement": "<missing bank standard requirement>",
   172	      "source_evidence": "<short matrix quote>",
   173	      "evidence_locators": ["<registry locator used only as supporting evidence>"],
   174	      "status": "missing_in_contract",
   175	      "required_type": "mandatory|optional|unknown",
   176	      "applicability": "applicable|conditional|unknown",
   177	      "risk_level": "low|medium|high",
   178	      "risk": "<risk of omission>",
   179	      "covered_elements": ["<matrix provisions covered by weak/partial context, if any>"],
   180	      "uncovered_elements": ["<matrix provisions not covered by any true analogue>"],
   181	      "candidate_contract_ids": [],
   182	      "candidate_search_exhausted": true,
   183	      "search_scope": "full_contract",
   184	      "rejected_candidates": [
   185	        {
   186	          "contract_id": "<weak candidate considered>",
   187	          "reason": "<why it is not a true analogue>"
   188	        }
   189	      ]
   190	    }
   191	  ],
   192	  "unmatched_contract": [
   193	    {
   194	      "contract_id": "<contract locator>",
   195	      "contract_position": "<extra legally significant contract term>",
   196	      "source_evidence": "<short contract quote>",
   197	      "evidence_locators": ["<registry locator used only as supporting evidence>"],
   198	      "status": "extra_in_contract",
   199	      "risk_level": "low|medium|high",
   200	      "risk": "<risk or impact for the Bank>",
   201	      "materiality_reason": "<why this has independent legal effect>"
   202	    }
   203	  ],
   204	  "coverage_ledger": {
   205	    "matrix": [
   206	      {
   207	        "matrix_id": "<matrix id>",
   208	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
   209	        "link_indices": [0],
   210	        "reason": "<short closure reason>"
   211	      }
   212	    ],
   213	    "contract": [
   214	      {
   215	        "contract_id": "<contract locator>",
   216	        "closure": "linked|extra_in_contract|not_material",
   217	        "link_indices": [0],
   218	        "reason": "<short closure reason>"
   219	      }
   220	    ]
   221	  },
   222	  "summary": {
   223	    "aligned_count": 0,
   224	    "deviation_count": 0,
   225	    "missing_in_contract_count": 0,
   226	    "extra_in_contract_count": 0
   227	  }
   228	}
   229	```
   230	
   231	## JSON Rules
   232	
   233	- `links` are group-level legal findings. One status applies to the whole
   234	  many-to-many group.
   235	- `atomic_links` are traceability rows only. They inherit the group
   236	  `relationship`; do not invent pair-level final statuses.
   237	- `contract_ids` contain clauses that provide material coverage for the focused
   238	  group. Each listed id must correspond to at least one named item in
   239	  `covered_elements`, `uncovered_elements`, `discrepancies`, or
   240	  `status_reason`. Background clauses can be cited in reasoning, but should not
   241	  become final candidates unless they affect coverage or status.
   242	- `links` are reasoning-backed legal findings. Do not generate them from
   243	  keyword overlap, token overlap, section proximity, vector similarity, regular
   244	  expressions, or match scores. Phrases such as `auto-matched`, `score`,
   245	  `threshold`, or `keyword overlap` are not valid status reasons.
   246	- A link group must be a focused legal package. If many same-topic or
   247	  same-parent clauses are grouped together, each clause must contribute a named
   248	  right, duty, trigger, deadline, amount, procedure, liability term, or
   249	  consequence to the same legal result. Otherwise split the group or reject the
   250	  extra clauses.
   251	- Final contract ids are closed-class values: they must come from
   252	  `/outputs/working/contract_locator_registry.json` with `final_allowed = true`.
   253	  Do not create corrected, translated, internal, parenthetical, semantic-suffix,
   254	  or derived appendix ids. A source-derived appendix/table row may be final only
   255	  when the registry row itself is final-allowed and contains an operative
   256	  amount, fee, deadline, product scope, procedure, liability term, or other
   257	  standalone legal condition.
   258	- `evidence_locators` are for source anchors that support the evidence but are
   259	  not independent final contract clauses. Evidence-only locators do not count
   260	  as coverage candidates and cannot cure a missing or deviation finding.
   261	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   262	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   263	  matrix closures. Do not use it to invent final conclusions.
   264	- Merge/finalizer helpers may normalize explicit findings, but they must not
   265	  infer `missing_in_contract` only because a matrix id has no link. An
   266	  applicable matrix id without an explicit link, explicit missing row, or
   267	  profile-based closure is an incomplete run.
   268	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   269	  not a risk for the current product, lot, terminal, payment method, or legal
   270	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   271	  final `unmatched_matrix`.
   272	- `unmatched_contract` contains only legally significant `extra_in_contract`
   273	  rows. Non-material rows stay in `coverage_ledger.contract`.
   274	- Working-stage gates are inputs to reliability, not final legal conclusions.
   275	  A validation report can block the next step; it cannot create links,
   276	  statuses, missing rows, or extra rows by itself.
   277	- `relationship = aligned` requires empty `discrepancies`, empty
   278	  `uncovered_elements`, `risk_level = none`, and text-grounded confirmation
   279	  that the contract package preserves the matrix legal result.
   280	- `relationship = deviation` requires at least one discrepancy with `type`,
   281	  `description`, and `risk`; `candidate_search_exhausted = true`; and
   282	  `search_scope = full_contract`.
   283	- Missing mandatory applicable requirements should normally be `high` risk.
   284	  Missing optional applicable requirements should normally be `low` or
   285	  conditional risk.
   286	- `unmatched_matrix` requires `candidate_search_exhausted = true` and
   287	  `search_scope = full_contract`; it is invalid to mark an applicable matrix
   288	  item missing before completing a documented legal sweep through the source
   289	  index. The sweep may use the ledger to find plausible clauses, but acceptance
   290	  or rejection must be based on legal object, party, trigger, procedure,
   291	  consequence, and source text. Search exhaustion means the agent reviewed and
   292	  rejected weak candidates; it does not mean adding all nearby clauses to the
   293	  final group.
   294	- All final ids must be visible in source files. Do not use corrected,
   295	  inferred, translated, parenthetical, or internal ids.
   296	- All final ids must also be registry-final-allowed. A visible appendix heading
   297	  is not a final `contract_id` unless the registry marks it `final_allowed`.
   298	- Weak candidates do not appear in final `links`; use
   299	  `unmatched_matrix[].rejected_candidates`.
   300	- Focused package recall is required for final links: if a child/detail row is
Tool:    101	Matrix or contract requires a filled penalty, fee, account, deadline, appendix,
   102	or system name. The applicable field is blank.
   103	
   104	Result: `deviation` only for the requirement where the blank is material,
   105	usually low risk unless the blank blocks enforcement. Do not downgrade sibling
   106	channels, sibling duties, or the whole block because one field is blank.
   107	
   108	## 12. Same Deadline
   109	
   110	Matrix requires a document within 3 business days. Contract imposes the same
   111	3-business-day deadline on the same duty.
   112	
   113	Result: deadline element is covered.
   114	
   115	## 13. Changed Or Missing Deadline
   116	
   117	Matrix requires 3 business days. Contract says 5 business days, uses another
   118	period, or states the duty without a deadline.
   119	
   120	Result: `deviation`; discrepancy type `deadline`.
   121	
   122	## 14. Borrowed Hard Term Does Not Cure Gap
   123	
   124	Contract clause A covers the same duty but lacks the matrix deadline. Clause B
   125	has the same number of days but governs a different request or procedure and is
   126	not incorporated into clause A.
   127	
   128	Result: clause B cannot make clause A aligned. Record a deadline deviation.
   129	
   130	## 15. Changed Amount, Formula, Cap, Or Penalty
   131	
   132	Matrix requires a fixed penalty, no cap, full damages, or a specific formula.
   133	Contract lowers the amount, adds a cap, changes the base, or requires an extra
   134	demand.
   135	
   136	Result: `deviation`; discrepancy type `amount` or `liability`.
   137	
   138	## 16. Party Inversion
   139	
   140	Matrix protects the Bank or imposes a duty on the counterparty. Contract gives
   141	the analogous right to the customer or shifts the burden to the Bank.
   142	
   143	Result: `deviation` if it is an analogue; `extra_in_contract` if it creates a
   144	new independent right.
   145	
   146	## 17. Procurement Mechanism As Analogue
   147	
   148	Public-contract acceptance, EIS signing, budget payment, statutory penalties,
   149	or unilateral termination regulates the same legal object as the matrix.
   150	
   151	Result: link it. Use `aligned` if the Bank standard is preserved or stronger.
   152	Do not mark `deviation` merely because the mechanism is 44-FZ/EIS.
   153	
   154	## 18. Procurement Mechanism With Material Deviation
   155	
   156	Public-contract mechanics regulate the same legal object, but the contract
   157	changes a material element: longer payment deadline, weaker withholding right,
   158	different acceptance consequence, penalty cap, lost termination power, or
   159	changed protected party.
   160	
   161	Result: grouped `deviation` with the specific changed element.
   162	
   163	## 19. Procurement Mechanism As Extra
   164	
   165	Contract gives the customer an independent inspection, rejection, correction,
   166	withholding, reporting, or convenience termination right with no matrix
   167	analogue.
   168	
   169	Result: `extra_in_contract` with materiality reason and risk.
   170	
   171	## 20. Formal Label Difference
   172	
   173	The same legal content appears under another appendix title, report label, or
   174	document name.
   175	
   176	Result: `aligned` if rights, duties, timing, evidence, and consequences are
   177	preserved.
   178	
   179	## 21. Low-Risk Note Does Not Force Deviation
   180	
   181	The contract uses another label for the same channel, another party label for
   182	the same legal role, or adds language beneficial to the Bank. The legal result,
   183	timing, enforceability, and protected party are preserved.
   184	
   185	Result: `aligned`. The note can appear in `status_reason`, but it is not a
   186	discrepancy.
   187	
   188	## 22. Named Channel Or Legal Force Missing
   189	
   190	Matrix requires a named EDI/email/site/channel or legal-force effect. Contract
   191	has a generic document exchange clause and omits the named element.
   192	
   193	Result: `deviation` when it is the same exchange mechanism with a missing
   194	material element. If it is only broad-topic context, use `missing_in_contract`.
   195	
   196	## 23. Generic Product Capability
   197	
   198	Contract says a terminal can display QR or accept cards. Matrix requires a
   199	named Bank product or product-specific procedure.
   200	
AI: Now let me read the rest of the comparison patterns and then look at the matrix and contract inputs:[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'offset': 200}, 'id': 'call_00_qUHgvmid2Z1320HXldnc1124', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'offset': 300}, 'id': 'call_01_OQrMcMPsF7M0o2ap1HKM3195', 'type': 'tool_call'}]
Tool:    201	Result: apply the product profile first. Generic capability is not enough for a
   202	named product obligation.
   203	
   204	## 24. Parent And Child Package Retention
   205	
   206	Parent clause states the operative right or duty. Child clauses enumerate
   207	events, exceptions, deadlines, or remedies. Either parent or child alone would
   208	be incomplete.
   209	
   210	Result: final group includes the material parent and the children that cover
   211	the same legal result. Do not add all children under the parent; each child must
   212	cover a named element of the analyzed requirement.
   213	
   214	## 25. Framework Clause As Analogue
   215	
   216	Contract clause requires compliance with applicable law, payment-system rules,
   217	contract specifications, or incorporated operating procedures. A matrix row
   218	uses that same framework as the legal object or risk-allocation rule.
   219	
   220	Result: include the framework clause as a legal analogue. Do not use it to
   221	inflate unrelated rows where it is only background context.
   222	
   223	## 26. Liability Group Review
   224	
   225	Matrix separates delay penalties, non-delay fines, caps, exceptions, claim
   226	procedure, and damages. Contract distributes the same topics across several
   227	clauses.
   228	
   229	Result: compare the liability package as a group. Before `aligned`, verify
   230	amounts, formulas, caps, triggers, protected party, and excluded buckets.
   231	
   232	## 27. Definition Without Legal Effect
   233	
   234	Definition has no analogue in the matrix and creates no standalone right, duty,
   235	risk, amount, procedure, liability, or consequence.
   236	
   237	Result: `not_material` in the working ledger only.
   238	
   239	## 28. Definition With Legal Effect
   240	
   241	Definition expands a key term so that it changes scope, liability, covered
   242	transactions, parties, or remedies.
   243	
   244	Result: evaluable. Link it if it modifies a matrix analogue; otherwise classify
   245	as `extra_in_contract`.
   246	
   247	## 29. Contract-Only Material Clause
   248	
   249	Contract adds maximum price, budget source, customer control, acceptance,
   250	withholding, unilateral refusal, penalty cap, reporting, anti-corruption,
   251	confidentiality, audit, data, or evidence procedure with no matrix analogue.
   252	
   253	Result: `extra_in_contract`.
   254	
   255	## 30. Duplicate Gap Propagation
   256	
   257	One payment deadline gap affects a payment package with parent and child
   258	clauses.
   259	
   260	Result: record one grouped `deviation`. Do not duplicate the same gap across
   261	unrelated companion clauses, and do not downgrade sibling matrix requirements
   262	where the deadline is not a material element.
   263	
   264	## 31. Non-Informative Parent
   265	
   266	A parent row merely names a section and all legal effect is in children.
   267	
   268	Result: close as non-evaluable or `not_material` in the ledger. Do not report
   269	it as a final risk.
   270	
   271	## 32. Group-Level Status
   272	
   273	A group contains several matrix ids and several contract ids. One status
   274	applies to the group as a whole.
   275	
   276	Result: do not assign separate final statuses per pair. `atomic_links` are only
   277	traceability rows and inherit the group relationship. If the matrix ids are not
   278	one indivisible legal package, split the group before assigning status.
   279	
   280	## Focused Recall Examples
   281	
   282	### same-parent-siblings-do-not-share-status
   283	
   284	Several matrix subrequirements share the same parent: email exchange, EDI
   285	exchange, courier delivery, and platform delivery. The contract preserves email,
   286	courier, and platform delivery, but one named EDI system is blank.
   287	
   288	Result: only the EDI requirement is `deviation`. The shared parent may be cited
   289	as context, but the preserved sibling channels remain `aligned`.
   290	
   291	### document-channel-placeholder-contained
   292	
   293	Matrix requires separate document channels. Contract has one blank URL or
   294	system name in the electronic-channel row, while other channels are complete.
   295	
   296	Result: the blank creates `deviation` only for that channel. Do not turn the
   297	whole document-exchange package into `deviation`.
   298	
   299	### pdn-deadline-contained
   300	
Tool:    301	  a true analogue, include its operative parent/root only when that parent
   302	  carries the same right, duty, procedure, basis, or consequence. Do not include
   303	  sibling children, headings, adjacent topic clauses, or evidence-only anchors
   304	  unless they cover a named material element of the same group.
   305	- Matrix missing findings require strict-link audit: if only broad thematic
   306	  candidates exist, keep them in `rejected_candidates` and leave the matrix item
   307	  in `unmatched_matrix`.
   308	- Status gaps are contained to the focused group where the gap is material. A
   309	  missing placeholder, deadline, channel, consent, amount, or procedure must not
   310	  downgrade sibling matrix ids unless that element belongs to those siblings.
   311	
   312	## Excel Output
   313	
   314	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   315	
   316	Sheet 1: `Contract-Matrix`
   317	
   318	Columns:
   319	
   320	1. `contract_id`
   321	2. `contract_summary`
   322	3. `matrix_ids`
   323	4. `status`
   324	5. `risk_level`
   325	6. `comment`
   326	
   327	Rules:
   328	
   329	- one row per group-level contract-to-matrix finding;
   330	- `matrix_ids` contains the full matrix id set for the group;
   331	- status is `aligned`, `deviation`, or `extra_in_contract`;
   332	- contract-only extras have blank `matrix_ids`.
   333	
   334	Sheet 2: `Only in Matrix`
   335	
   336	Columns:
   337	
   338	1. `matrix_id`
   339	2. `requirement`
   340	3. `required_type`
   341	4. `risk_level`
   342	5. `comment`
   343	
   344	Rules:
   345	
   346	- one row per final `unmatched_matrix` item;
   347	- include optional applicable missing as low/conditional risk;
   348	- do not include out-of-scope / not-applicable requirements;
   349	- do not include non-evaluable headings or purely technical rows.
   350	
   351	## Bad Output Patterns
   352	
   353	Do not output:
   354	
   355	- multiple competing final JSON files;
   356	- pair-level final statuses as the primary answer;
   357	- `deviation` for unselected slash alternatives;
   358	- `deviation` for heading/title/label changes alone;
   359	- final `unmatched_contract` rows for definitions without legal effect;
   360	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   361	  requirements;
   362	- final ids that exist only in helper scripts or working ledgers;
   363	- final `contract_id` values that are evidence-only registry locators;
   364	- evidence-only registry locators used as `rejected_candidates[].contract_id` or
   365	  `rejected_contract_ids[].contract_id`; keep them in `evidence_locators`
   366	  instead;
   367	- final links, statuses, or missing findings generated from legal match scores,
   368	  keyword overlap, token overlap, section proximity, vector similarity, or
   369	  regular-expression rules;
   370	- `status_reason` values such as `Auto-matched with score ...`,
   371	  `keyword match`, `high similarity`, or `same section`;
   372	- overbroad same-topic link groups where most `contract_ids` do not contribute
   373	  a named material element to the same legal result;
   374	- overbroad same-parent groups where one child gap changes the status of
   375	  independent sibling requirements;
   376	- synthetic appendix ids such as `Приложение_1_п5`,
   377	  `Приложение_1_п5_комиссия`, or `Appendix_1_fee`;
   378	- final appendix/table locators invented from semantics instead of copied from
   379	  `contract_locator_registry.json`;
   380	- `extra_in_contract` with empty risk;
   381	- `aligned` with non-empty discrepancies;
   382	- `aligned` with non-empty `uncovered_elements`;
   383	- `deviation` or `missing_in_contract` with `candidate_search_exhausted = false`;
   384	- `deviation` or `missing_in_contract` with `search_scope = targeted_domain`
   385	  or `not_completed`;
   386	- `missing_in_contract` where a weak candidate is silently treated as a link;
   387	- `not_material` closure explained only as `No final legal finding produced`,
   388	  `not analyzed`, or another non-legal placeholder reason;
   389	- implicit `missing_in_contract` rows produced by a script without an explicit
   390	  agent finding and documented rejected/covered/uncovered elements;
   391	- final conclusions based only on extracted fields without source-text evidence.
   392	- final JSON written after a failed source preflight, failed
   393	  `working_artifact_validation.json`, failed fragment validation, or missing
   394	  stage-gate report.
AI: Now let me look at the matrix and contract inputs, focusing on the batch 2 range (5.1.8.10 through 6.20):[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 50}, 'id': 'call_00_X2DCwgWvK2QDYciSMxLf4185', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_01_TQicNkPVqWW1psBhVLzv8978', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 100}, 'id': 'call_02_Bm5t7KB6Tm4y0qVFWYXp7538', 'type': 'tool_call'}]
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
    11	    "qr"
    12	  ],
    13	  "legal_regime": "44_fz",
    14	  "evidence": {
    15	    "product": {
    16	      "value": "trade_acquiring",
    17	      "source": "Контракт, п. 1.1, п. 5.3.18, Приложение №1 (Техническое задание), Приложение №1..2 (Информация о ТСТ)",
    18	      "quote": "п. 1.1: «услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)»; п. 5.3.18: «При осуществлении операций у заказчика в ТСТ (торговый эквайринг)»; Приложение №1: перечень адресов установки POS-терминалов в торгово-сервисных точках (8 адресов, 14 терминалов); Приложение №1..2: форма «Информация о ТСТ» с разделом «ТОРГОВЫЙ ЭКВАЙРИНГ»",
    19	      "excludes": "internet_acquiring — в контракте отсутствует интернет-эквайринг (нет интернет-сайта/мобильного приложения для приёма оплаты, в форме Заявления Предприятия (Приложение №1.1) опция «Интернет-эквайринг» не отмечена, в Информации о ТСТ (Приложение №1..2) раздел «ИНТЕРНЕТ ЭКВАЙРИНГ» не заполнен)"
    20	    },
    21	    "lot": {
    22	      "value": "44_fz",
    23	      "source": "Преамбула контракта, п. 3.3, п. 5.2.2, п. 5.4.3, п. 8.3.1, раздел 11",
    24	      "quote": "Преамбула: «с соблюдением требований Федерального закона от 5 апреля 2013 г. № 44-ФЗ «О контрактной системе в сфере закупок товаров, работ, услуг для обеспечения государственных и муниципальных нужд»»; п. 3.3: «если Федеральным законом №44-ФЗ не установлено иное»; п. 8.3.1: ссылка на «пункт 1 части 2 статьи 51 Федерального закона № 44-ФЗ»; раздел 11: «в порядке и сроки, предусмотренные статьей 95 Федерального закона № 44-ФЗ»"
    25	    },
    26	    "terminal": {
    27	      "value": ["pos", "smart"],
    28	      "source": "Контракт, п. 2.2, п. 5.1.1, п. 5.3.18, Приложение №1 (Техническое задание), Приложение №1..2 (Информация о ТСТ)",
    29	      "quote": "п. 2.2: «электронный терминал – электронное программно-техническое устройство исполнителя... Электронный терминал может включать в себя в том числе мобильный терминал (mPOS), биометрический терминал»; Приложение №1: «количество необходимых POS-терминалов» — 14 шт.; Приложение №1..2: раздел «Смарт-терминал Банка» с указанием модели «Эвотор+», «СТ-7.3» — 3 шт.; п. 5.1.1: «Установить Заказчику и подготовить к эксплуатации Электронные терминалы»",
    30	      "note": "Контракт предусматривает как обычные POS-терминалы (pos), так и смарт-терминалы (smart). В форме Информации о ТСТ отмечен «Торговый эквайринг + Cмарт-терминал + QR-код» с моделью «Эвотор+». Также в Приложении №1..2 указаны смарт-терминалы СТ-7.3 в количестве 3 шт."
    31	    },
    32	    "payment_method": {
    33	      "value": ["qr"],
    34	      "source": "Приложение №1 (Техническое задание), п. 5, Приложение №1..2 (Информация о ТСТ)",
    35	      "quote": "Приложение №1, п. 5: «Терминалы Исполнителя должны иметь возможность принятия бесконтактной оплаты»; «Возможность вывода QR-кода для безналичной оплаты на дисплей терминала»; Приложение №1..2: в разделе «ТОРГОВЫЙ ЭКВАЙРИНГ» отмечен «QR-код», в форме Заявления отмечен «Торговый эквайринг + Cмарт-терминал + QR-код»",
    36	      "excludes": {
    37	        "sber_pay_face_scan": "В контракте отсутствует упоминание SberPay FaceScan / биометрической оплаты. В форме Информации о ТСТ (Приложение №1..2) опция «проведение операций с биометрическим методом идентификации» не отмечена.",
    38	        "qr_sber_pay": "В контракте упоминается только «QR-код» без привязки к SberPay QR / Плати QR. Специфические условия SberPay QR отсутствуют."
    39	      }
    40	    },
    41	    "legal_regime": {
    42	      "value": "44_fz",
    43	      "source": "Преамбула контракта, множественные ссылки на 44-ФЗ по всему тексту",
    44	      "quote": "Преамбула: «с соблюдением требований Федерального закона от 5 апреля 2013 г. № 44-ФЗ»; ИКЗ: 251231702678823170100100060016619244"
    45	    }
    46	  },
    47	  "matrix_filter_application": {
    48	    "only_for_product": {
    49	      "contract_value": "trade_acquiring",
    50	      "applicable_filters": ["common", "trade_acquiring"],
    51	      "not_applicable_filters": ["internet_acquiring"],
    52	      "affected_matrix_ids_note": "Матричные пункты с only_for_product = 'internet_acquiring' не применяются к данному контракту (например, 2.5.1.1 — SberPayOnline для интернет-эквайринга)"
    53	    },
    54	    "only_for_lot": {
    55	      "contract_value": "44_fz",
    56	      "applicable_filters": ["common", "fz_44"],
    57	      "not_applicable_filters": ["fz_223"],
    58	      "affected_matrix_ids_note": "Матричные пункты с only_for_lot = 'fz_223' не применяются к данному контракту (например, 4.2.3 — самостоятельное ознакомление с изменениями на сайте Банка)"
    59	    },
    60	    "only_for_terminal": {
    61	      "contract_value": ["pos", "smart"],
    62	      "applicable_filters": ["common", "pos", "smart"],
    63	      "not_applicable_filters": [],
    64	      "affected_matrix_ids_note": "Все матричные фильтры по терминалам применимы, так как контракт включает и pos, и smart терминалы"
    65	    },
    66	    "payment_method": {
    67	      "contract_value": ["qr"],
    68	      "applicable_filters": ["common", "qr"],
    69	      "not_applicable_filters": ["sber_pay_face_scan", "qr_sber_pay"],
    70	      "affected_matrix_ids_note": "Матричные пункты с payment_method = 'sber_pay_face_scan' (например, 2.5.2.1) и 'qr_sber_pay' (например, 4.1.3) не применяются к данному контракту"
    71	    }
    72	  },
    73	  "profile_based_closures": {
    74	    "out_of_scope": [
    75	      {
    76	        "matrix_id": "2.5.1.1",
    77	        "reason": "only_for_product = 'internet_acquiring' — контракт не предусматривает интернет-эквайринг (торговый эквайринг с POS/смарт-терминалами в ТСТ)"
    78	      },
    79	      {
    80	        "matrix_id": "2.5.2.1",
    81	        "reason": "payment_method = 'sber_pay_face_scan' — контракт не предусматривает биометрическую оплату SberPay FaceScan"
    82	      },
    83	      {
    84	        "matrix_id": "4.1.3",
    85	        "reason": "payment_method = 'qr_sber_pay' — контракт предусматривает только общий QR-код, без специфики SberPay QR / Плати QR"
    86	      },
    87	      {
    88	        "matrix_id": "4.2.17",
    89	        "reason": "only_for_product = 'internet_acquiring' — контракт не предусматривает интернет-эквайринг"
    90	      },
    91	      {
    92	        "matrix_id": "4.2.21.1",
    93	        "reason": "only_for_product = 'internet_acquiring' — контракт не предусматривает интернет-эквайринг"
    94	      },
    95	      {
    96	        "matrix_id": "4.2.21.2",
    97	        "reason": "only_for_product = 'internet_acquiring' — контракт не предусматривает интернет-эквайринг"
    98	      },
    99	      {
   100	        "matrix_id": "4.2.21.3",
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предостав",
     7	      "type": "operative",
     8	      "materiality": "evaluable",
     9	      "protected_party": "Банк/Предприятие",
    10	      "bound_party": "Предприятие/Банк",
    11	      "right_or_obligation": "обязанность Предприятия предоставить документы; право Банка отказать в регистрации",
    12	      "legal_object": "регистрация ТСТ",
    13	      "trigger": "подача заявления Предприятием",
    14	      "deadline": "",
    15	      "amount_formula_cap": "",
    16	      "procedure_channel": "заявление по форме Приложения 1, информация о ТСТ по форме Приложения 1.1",
    17	      "liability_remedy": "",
    18	      "scope_options": [],
    19	      "consequence": "Банк вправе отказать в регистрации ТСТ без объяснения причин",
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
    39	      "source_excerpt": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    40	      "type": "operative",
    41	      "materiality": "evaluable",
    42	      "protected_party": "Банк/Предприятие",
    43	      "bound_party": "Предприятие/Банк",
    44	      "right_or_obligation": "обязанность сторон",
    45	      "legal_object": "валюта расчетов",
    46	      "trigger": "",
    47	      "deadline": "",
    48	      "amount_formula_cap": "",
    49	      "procedure_channel": "",
    50	      "liability_remedy": "",
    51	      "scope_options": [],
    52	      "consequence": "расчеты только в рублях РФ",
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
    71	      "materiality": "evaluable",
    72	      "protected_party": "Банк/Предприятие",
    73	      "bound_party": "Предприятие/Банк",
    74	      "right_or_obligation": "право сторон на выбор способа обмена",
    75	      "legal_object": "обмен информацией по электронной почте",
    76	      "trigger": "",
    77	      "deadline": "",
    78	      "amount_formula_cap": "",
    79	      "procedure_channel": "электронная почта, исключая персональные данные, коммерческую и банковскую тайну",
    80	      "liability_remedy": "",
    81	      "scope_options": [],
    82	      "consequence": "информация имеет полную юридическую силу",
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
AI: Now I need to find the matrix items in the range 5.1.8.10 through 6.20. Let me search for these in the matrix:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\n# Find all matrix numbers\nnumbers = [m[\'number\'] for m in matrix]\n# Filter for range 5.1.8.10 through 6.20\n# We need to find items that sort between these\nfor n in numbers:\n    print(n)\n" 2>&1 | head -200\n'}, 'id': 'call_00_cFOMB8iujeZe4f1fhPCa7899', 'type': 'tool_call'}]
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
[stderr] with open('inputs/matrix.json', 'r') as f:
[stderr]     matrix = json.load(f)
[stderr] # Find all matrix numbers
[stderr] numbers = [m['number'] for m in matrix]
[stderr] # Filter for range 5.1.8.10 through 6.20
[stderr] # We need to find items that sort between these
[stderr] for n in numbers:
[stderr]     print(n)
[stderr] " 2>&1 | head -200
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : The term 'head' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
[stderr] lling of the name, or if a path was included, verify that the path is correct and try again.
[stderr] At line:47 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "import json; matrix = json.load(open(\'/inputs/matrix.json\', \'r\')); numbers = [m[\'number\'] for m in matrix]; [print(n) for n in numbers]"'}, 'id': 'call_00_6SFjaFtX0fTdVXBtzPGS9456', 'type': 'tool_call'}]
Tool: 2.1
2.2
2.3.1
2.3.2
2.3.3
2.3.4
2.3.5
2.3.6
2.3.7
2.4
2.5.1.1
2.5.2.1
2.6.1.1
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
4.1.3
4.2.1
4.2.2
4.2.3
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
4.2.17
4.2.18
4.2.19
4.2.20.1
4.2.20.2
4.2.20.3
4.2.20.4
4.2.20.5
4.2.20.6
4.2.20.7
4.2.21.1
4.2.21.2
4.2.21.3
4.2.21.4
4.2.21.5
4.2.21.6
4.2.21.7
4.2.21.8
4.2.22
4.2.23
4.2.24
4.2.25
4.2.26
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
5.1.8.4
5.1.8.5
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
5.1.17.2
5.2.1
5.2.2
5.2.3
5.2.4
5.2.5
5.2.6
5.2.7
5.2.8
5.2.9
5.2.10
5.2.12
6.1
6.2
6.3
6.4
6.5
6.6
6.7
6.8
6.9
6.10
6.11
6.12
6.13
6.14
6.15
6.16
6.17
6.18
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
7.13
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
AI: Now I can see the batch 2 range: 5.1.8.10 through 6.20. Let me identify the exact matrix ids:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nmatrix = json.load(open(\'/inputs/matrix.json\', \'r\'))\nnumbers = [m[\'number\'] for m in matrix]\n# Find items from 5.1.8.10 to 6.20\nbatch = [n for n in numbers if (\n    (n.startswith(\'5.1.8.\') and int(n.split(\'.\')[-1]) >= 10) or\n    (n.startswith(\'5.1.\') and n > \'5.1.8.13\') or\n    (n.startswith(\'5.2.\')) or\n    (n.startswith(\'6.\') and n <= \'6.20\')\n)]\n# But we need to be more precise - sort and filter\ndef sort_key(n):\n    parts = n.split(\'.\')\n    return tuple(int(p) for p in parts)\n\nsorted_nums = sorted(numbers, key=sort_key)\nstart_idx = sorted_nums.index(\'5.1.8.10\')\nend_idx = sorted_nums.index(\'6.20\')\nbatch = sorted_nums[start_idx:end_idx+1]\nprint(\'Batch 2 items:\')\nfor n in batch:\n    print(n)\nprint(f\'Total: {len(batch)}\')\n"'}, 'id': 'call_00_cGwOrhmBlBHn8YaYPtc18861', 'type': 'tool_call'}]
Tool: Batch 2 items:
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
5.1.17.2
5.2.1
5.2.2
5.2.3
5.2.4
5.2.5
5.2.6
5.2.7
5.2.8
5.2.9
5.2.10
5.2.12
6.1
6.2
6.3
6.4
6.5
6.6
6.7
6.8
6.9
6.10
6.11
6.12
6.13
6.14
6.15
6.16
6.17
6.18
6.20
Total: 44

[Command succeeded with exit code 0]
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read all 44 matrix items (5.1.8.10-6.20) from matrix.json', 'status': 'in_progress'}, {'content': 'Read contract.txt for relevant clauses', 'status': 'pending'}, {'content': 'Read legal_propositions.json for batch 2 matrix and contract rows', 'status': 'pending'}, {'content': 'Read contract_locator_registry.json for all final-allowed locators', 'status': 'pending'}, {'content': 'Perform legal analysis: matrix-to-contract and contract-to-matrix matching', 'status': 'pending'}, {'content': 'Write fragment JSON with links, atomic_links, unmatched_matrix, coverage_ledger', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Fix any validation errors and re-validate', 'status': 'pending'}]}, 'id': 'call_00_yr2NY36RFLdJDNs7kdHU1701', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read all 44 matrix items (5.1.8.10-6.20) from matrix.json', 'status': 'in_progress'}, {'content': 'Read contract.txt for relevant clauses', 'status': 'pending'}, {'content': 'Read legal_propositions.json for batch 2 matrix and contract rows', 'status': 'pending'}, {'content': 'Read contract_locator_registry.json for all final-allowed locators', 'status': 'pending'}, {'content': 'Perform legal analysis: matrix-to-contract and contract-to-matrix matching', 'status': 'pending'}, {'content': 'Write fragment JSON with links, atomic_links, unmatched_matrix, coverage_ledger', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Fix any validation errors and re-validate', 'status': 'pending'}]
AI: Let me read all the matrix items in batch 2:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nmatrix = json.load(open(\'/inputs/matrix.json\', \'r\'))\nbatch_ids = [\'5.1.8.10\',\'5.1.8.11\',\'5.1.8.12\',\'5.1.8.13\',\'5.1.9\',\'5.1.10\',\'5.1.11\',\'5.1.12\',\'5.1.13\',\'5.1.14\',\'5.1.15\',\'5.1.16\',\'5.1.17.1\',\'5.1.17.2\',\'5.2.1\',\'5.2.2\',\'5.2.3\',\'5.2.4\',\'5.2.5\',\'5.2.6\',\'5.2.7\',\'5.2.8\',\'5.2.9\',\'5.2.10\',\'5.2.12\',\'6.1\',\'6.2\',\'6.3\',\'6.4\',\'6.5\',\'6.6\',\'6.7\',\'6.8\',\'6.9\',\'6.10\',\'6.11\',\'6.12\',\'6.13\',\'6.14\',\'6.15\',\'6.16\',\'6.17\',\'6.18\',\'6.20\']\nmatrix_by_id = {m[\'number\']: m for m in matrix}\nfor mid in batch_ids:\n    m = matrix_by_id.get(mid)\n    if m:\n        print(f\'=== {mid} ===\')\n        print(f\'  main_idea: {m[\\"main_idea\\"][:200]}\')\n        print(f\'  required_type: {m[\\"required_type\\"]}\')\n        print(f\'  only_for_product: {m[\\"only_for_product\\"]}\')\n        print(f\'  only_for_lot: {m[\\"only_for_lot\\"]}\')\n        print(f\'  only_for_terminal: {m[\\"only_for_terminal\\"]}\')\n        print(f\'  payment_method: {m[\\"payment_method\\"]}\')\n        print(f\'  topics: {m[\\"topics\\"]}\')\n        print(f\'  enriched_text: {m[\\"enriched_text\\"][:300]}\')\n        print()\n    else:\n        print(f\'=== {mid} === NOT FOUND\')\n"'}, 'id': 'call_00_yAdl3RKoW4112eD3i3AD9646', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 10
[stderr]     print(f'  main_idea: {m[" main_idea\][:200]}')
[stderr]                             ^
[stderr] SyntaxError: unterminated string literal (detected at line 10)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nmatrix = json.load(open(\'/inputs/matrix.json\', \'r\'))\nbatch_ids = [\'5.1.8.10\',\'5.1.8.11\',\'5.1.8.12\',\'5.1.8.13\',\'5.1.9\',\'5.1.10\',\'5.1.11\',\'5.1.12\',\'5.1.13\',\'5.1.14\',\'5.1.15\',\'5.1.16\',\'5.1.17.1\',\'5.1.17.2\',\'5.2.1\',\'5.2.2\',\'5.2.3\',\'5.2.4\',\'5.2.5\',\'5.2.6\',\'5.2.7\',\'5.2.8\',\'5.2.9\',\'5.2.10\',\'5.2.12\',\'6.1\',\'6.2\',\'6.3\',\'6.4\',\'6.5\',\'6.6\',\'6.7\',\'6.8\',\'6.9\',\'6.10\',\'6.11\',\'6.12\',\'6.13\',\'6.14\',\'6.15\',\'6.16\',\'6.17\',\'6.18\',\'6.20\']\nmatrix_by_id = {m[\'number\']: m for m in matrix}\nfor mid in batch_ids:\n    m = matrix_by_id.get(mid)\n    if m:\n        print(\'=== \' + mid + \' ===\')\n        print(\'  main_idea: \' + m[\'main_idea\'][:200])\n        print(\'  required_type: \' + m[\'required_type\'])\n        print(\'  only_for_product: \' + m[\'only_for_product\'])\n        print(\'  only_for_lot: \' + m[\'only_for_lot\'])\n        print(\'  only_for_terminal: \' + m[\'only_for_terminal\'])\n        print(\'  payment_method: \' + m[\'payment_method\'])\n        print(\'  topics: \' + str(m[\'topics\']))\n        print(\'  enriched_text: \' + m[\'enriched_text\'][:300])\n        print()\n    else:\n        print(\'=== \' + mid + \' === NOT FOUND\')\n"'}, 'id': 'call_00_CkEO4z7oQGc8pRS0L6yo8597', 'type': 'tool_call'}]
Tool: === 5.1.8.10 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РўРЎРў', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂ

=== 5.1.8.11 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РїСЂРµРґРїСЂРёСЏС‚РёСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РІС‹СЏРІР»РµРЅРЅРѕРј РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі Р·Р°СЏРІР»РµРЅРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ 

=== 5.1.8.12 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ;

=== 5.1.8.13 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°', 'РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°, СѓРєР°Р·Р°РЅРЅРѕРіРѕ РІ Рї. 10.1 Р”РѕРіРѕРІРѕСЂР°.

=== 5.1.9 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў, РІ С‚.С‡. РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё.

=== 5.1.10 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РџСЂРѕРІРµСЂРєРё РїСЂРѕРІРѕРґСЏС‚СЃСЏ РґР»СЏ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° Рё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СЂРѕРґР° РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РЅРµРј', 'РџСЂРѕРІРµСЂРєРё РІРєР»СЋС‡Р°СЋС‚ РєРѕРЅС‚СЂРѕР»СЊ СЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј С‚СЂРµР±РѕРІР°РЅРёР№ Р”РѕРіРѕРІРѕСЂР° Рє Р РµСЃСѓСЂСЃСѓ', 'Р‘Р°РЅРє РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕСЃС‚СѓРї Рє РѕС‚РґРµР»СЊРЅС‹Рј Р·Р°РєСЂС‹С‚С‹Рј СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° РїСЂРё РїСЂРѕРІРµСЂРєР°С…']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІ С‚.С‡. РЅР° РїСЂРµРґРјРµС‚ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РѕРїРµСЂР°С†РёР№, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёС… СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў, РЅРµСЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў С‚СЂРµР±РѕРІР°РЅРёР№, СѓСЃ

=== 5.1.11 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ Р·Р°РїСЂР°С€РёРІР°С‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј', 'Р‘Р°РЅРє РјРѕР¶РµС‚ С‚СЂРµР±РѕРІР°С‚СЊ РїРёСЃСЊРјРµРЅРЅРѕРµ Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ СЃС‡РµС‚Р°, С‡РµРєРё Рё РёРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р±Р°РЅРєР°', 'РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ РєР°РЅР°Р»С‹ СЃРІСЏР·Рё СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р—Р°РїСЂР°С€РёРІР°С‚СЊ Р”РѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РЅРµ РїРѕР·РґРЅРµРµ 13 (С‚СЂРёРЅР°РґС†Р°С‚Рё) РјРµСЃСЏС†РµРІ СЃ РґР°С‚С‹ СЃРѕРІРµСЂС€РµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РІ Рї. 4.2.10 Р”РѕРіРѕРІРѕСЂР°. Р”Р»СЏ Р°РЅР°Р»РёР·Р° СЃРїРѕСЂРЅС‹С… СЃРёС‚СѓР°С†РёР№ Р‘Р°РЅРє С‚Р°РєР¶Рµ РјРѕР¶РµС‚ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ Р·Р°СЏРІР»РµРЅРё

=== 5.1.12 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ СЃРІСЏР·Р°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ unilateral_in_one_day_right', 'РћРїСѓР±Р»РёРєРѕРІР°РЅРёРµ РёР·РјРµРЅРµРЅРёР№ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ РґРѕРєСѓРјРµРЅС‚С‹, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ Р”РѕРіРѕРІРѕСЂРµ, РїСѓС‚РµРј РїСѓР±Р»РёРєР°С†РёРё РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР° РЅРµ РјРµРЅРµРµ С‡РµРј Р·Р° 1 (РѕРґРёРЅ) РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РґРµРЅСЊ РґРѕ РІРІРµРґРµРЅРёСЏ РІ РґРµР№СЃС‚РІРёРµ СѓРєР°Р·Р°РЅРЅС‹С… РёР·РјРµРЅРµРЅРёР№.

=== 5.1.13 ===
  main_idea: Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµРґРѕРјР»РµРЅРёСЏ, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РёР·РјРµРЅСЏС‚СЊ СЃРІРѕРё СЂРµРєРІРёР·РёС‚С‹', 'РЈРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёРё СЂРµРєРІРёР·РёС‚РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· РћС„РёС†РёР°Р»СЊРЅС‹Р№ СЃР°Р№С‚ Р‘Р°РЅРєР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РёР·РјРµРЅРµРЅРёСЏ СЂРµРєРІРёР·РёС‚РѕРІ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹С… РІ Р”РѕРіРѕРІРѕСЂРµ, СѓРІРµРґРѕРјРёС‚СЊ РѕР± СЌС‚РѕРј РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСѓС‚РµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°. 

=== 5.1.14 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РђРґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ СѓРєР°Р·Р°РЅ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ', 'Р—Р°РїСЂРѕСЃС‹ РЅР°РїСЂР°РІР»РµРЅС‹ РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ С†РµР»СЏС… РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі /Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў.

=== 5.1.15 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· СѓРєР°Р·Р°РЅРёСЏ РїСЂРёС‡РёРЅ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· РѕР±СЉСЏСЃРЅРµРЅРёСЏ РїСЂРёС‡РёРЅ.

=== 5.1.16 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°

=== 5.1.17.1 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: pos
  payment_method: common
  topics: ['РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє 

=== 5.1.17.2 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏРј Р±Р°РЅРєР°', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ 5.1.17.2. РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕ

=== 5.2.1 ===
  main_idea: 
  required_type: mandatory
  only_for_product: internet_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ', 'РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РћРїРµСЂР°С†РёР№.

=== 5.2.2 ===
  main_idea: 
  required_type: mandatory
  only_for_product: internet_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё', 'РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№ РІ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіРµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Рё РўРµС…РЅРѕР»РѕРіРёР№ 3DSecure

=== 5.2.3 ===
  main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»РєРё РЅР° СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј РЅРµ СЏРІР»СЏРµС‚СЃСЏ
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['СѓСЃС‚Р°РЅРѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РїРѕРґРіРѕС‚РѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё', 'РїСЂРѕРІРµРґРµРЅРёРµ РїРµСЂРІРёС‡РЅРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЈСЃС‚Р°РЅРѕРІРёС‚СЊ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№. РџСЂРѕРІРµСЃС‚Рё РїРµСЂРІРёС‡РЅС‹Р№ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹РјРё Р‘Р°РЅРєРѕРј

=== 5.2.4 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚ РђРІС‚РѕСЂРёР·Р°С†РёСЋ Р±РµР· РїРµСЂРµСЂС‹РІРѕРІ 24 С‡Р°СЃР° РІ СЃСѓС‚РєРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ РђРІС‚РѕСЂРёР·Р°С†РёСЋ

=== 5.2.5 ===
  main_idea: РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РјРµС‰РµРЅС‹ РїРѕ СѓРєР°Р·Р°РЅРЅРѕР№ СЃСЃС‹Р»РєРµ', 'РјР°С‚РµСЂРёР°Р»С‹ РґРѕСЃС‚СѓРїРЅС‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р Р°Р·РјРµСЃС‚РёС‚СЊ РЅР° СЃР°Р№С‚Рµ:  https://www.sberbank.ru/help/business/acquiring РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ

=== 5.2.6 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РћР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё', 'РћР±РµСЃРїРµС‡РµРЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РЅРµРѕР±С…РѕРґРёРјС‹РјРё РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№

=== 5.2.7 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅР°СЏ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р·Р°РјРµРЅР° РЅРµРёСЃРїСЂР°РІРЅРѕРіРѕ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РЅР° РёСЃРїСЂР°РІРЅС‹Р№ РЅРµ РїРѕР·РґРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ Р·Р°СЏРІРєРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ. Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° РёР· СЃС‚СЂРѕСЏ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° Р‘Р°РЅРєР°, РѕР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїСЂР°РІРЅС‹Рј Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРј Р‘Р°РЅРєР° РЅРµ РїРѕР·РґРЅРµРµ 3 (С‚

=== 5.2.8 ===
  main_idea: Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅРµ РїРѕР·РґРЅРµРµ 2 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё', 'РґР°С‚Р° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё - СЂР°Р±РѕС‡РёР№ РґРµРЅСЊ, СЃР»РµРґСѓСЋС‰РёР№ Р·Р° РґРЅРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ СЃРІРµСЂРєРё РёС‚РѕРіРѕРІ', 'РїСЂРё С‚РµС…РЅРёС‡РµСЃРєРѕРј СЃР±РѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёСЃС…РѕРґРёС‚ С‡РµСЂРµР· 3 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅСЏ РїРѕСЃР»Рµ РїРѕСЃР»РµРґРЅРµР№ СѓСЃРїРµС€РЅРѕР№ СЃРІРµСЂРєРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕР№ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё, РїРµСЂРµРґР°РЅРЅРѕР№ РѕС‚ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°  / Р РµСЃСѓСЂСЃР° /QR-РєРѕРґР°  РІ Р‘Р°РЅРє, РЅРµ РїРѕР·РґРЅРµРµ 2 (РґРІСѓС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј РїРµСЂРµС‡РёСЃР»СЏС‚СЊ РЅР° СЂР°СЃС‡РµС‚РЅС‹Р№ (С‚РµРєСѓС‰

=== 5.2.9 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: qr
  topics: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ QR-РєРѕРґР° РїР°СЂС‚РЅРµСЂР° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РїРѕ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј РєР°РЅР°Р»Р°Рј СЃРІСЏР·Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ

=== 5.2.10 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: []
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РѕР±СЂР°Р±РѕС‚РєСѓ РџР”РЅ, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, Р° С‚Р°РєР¶Рµ РѕР±РµСЃРїРµС‡РёС‚СЊ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕСЃС‚СЊ Рё Р·Р°С‰РёС‚Сѓ РѕР±СЂР°Р±Р°С‚С‹РІР°РµРјС‹С… РџР”РЅ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° РѕС‚ 27 РёСЋР»СЏ 2006 в„– 152-Р¤Р— В«Рћ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…В». РџСЂРёРЅРёРјР°С‚СЊ РЅРµРѕР±С…РѕРґРёРјС‹Рµ РїСЂР°РІРѕРІС‹Рµ,

=== 5.2.12 ===
  main_idea: 
  required_type: optional
  only_for_product: internet_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: qr
  topics: ['Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API Р±РµР· РіР°СЂР°РЅС‚РёР№']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API (РІ С‚.С‡. РІСЃС‘, С‡С‚Рѕ СЃРІСЏР·Р°РЅРѕ СЃ РѕСЂРіР°РЅРёР·Р°С†РёРµР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РїРѕСЃСЂРµРґСЃС‚РІРѕРј С‚Р°РєРѕРіРѕ API) В«РєР°Рє РµСЃС‚СЊВ» Р±РµР· РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РєР°РєРёС…-Р»РёР±Рѕ РіР°СЂР°РЅС‚РёР№

=== 6.1 ===
  main_idea: Р’Р°Р¶РЅРѕ
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р—Р° РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹, РџСЂРµРґРїСЂРёСЏС‚РёРµ СѓРїР»Р°С‡РёРІР°РµС‚ Р‘Р°РЅРєСѓ РїР»Р°С‚Сѓ РІ СЂР°Р·РјРµСЂРµ:
В«(____________) РїСЂРѕС†РµРЅС‚ РѕС‚ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚В».

=== 6.2 ===
  main_idea: РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµСЂРёРѕРґРёС‡РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°', 'РІ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РІРєР»СЋС‡РµРЅ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРј', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚[2] (РґР°Р»РµРµ вЂ“ РЈРџР”) РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ Рј

=== 6.3 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: fz_223
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РђРєС‚ РґРѕ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РђРєС‚ РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РІРјРµСЃС‚Рµ СЃРѕ СЃС‡РµС‚РѕРј-С„Р°РєС‚СѓСЂРѕР№ С„РѕСЂРјС‹ 363', 'Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ 6.1 РґРѕРіРѕРІРѕСЂР°', 'Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї.3 СЃС‚.149 РќРљ Р Р¤', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ Р‘Р°РЅРєРѕРј РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РђРєС‚ Рѕ РїРµСЂРµС‡РёСЃР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРј РѕРїРµСЂР°С†РёР№ РїРѕ РєР°СЂС‚Р°Рј РїРѕ С„РѕСЂРјРµ РџСЂРёР»РѕР¶РµРЅРёСЏ 2 Рє Р”РѕРіРѕРІРѕСЂСѓ (РґР°Р»РµРµ вЂ“ РђРєС‚) Рё СЃС‡РµС‚ С„.363 РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»

=== 6.4 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Рё РІРѕР·РІСЂР°С‚РёС‚СЊ РЈРџР” (РїСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё)', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.

=== 6.5 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р±Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.

=== 6.6 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: fz_223
  only_for_terminal: common
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р°РєС‚Р° Рё СЃС‡РµС‚Р° С„РѕСЂРјС‹ 363', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РЅР° СЃС‡РµС‚, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„РѕСЂРјС‹ 363']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° РђРєС‚Р° Рё СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ 

=== 6.7 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['СѓРєР°Р·Р°РЅ СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°', 'СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂСѓР±Р»РµР№ РІРєР»СЋС‡Р°СЏ РќР”РЎ', 'СѓСЃС‚Р°РЅРѕРІР»РµРЅ РµР¶РµРјРµСЃСЏС‡РЅС‹Р№ РїРѕСЂСЏРґРѕРє РѕРїР»Р°С‚С‹']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ РІ СЂР°Р·РјРµСЂРµ _____ (__________________) СЂСѓР±Р»РµР№ (РІРєР»СЋС‡Р°СЏ РќР”РЎ) Р·Р° РєР°Р¶РґС‹Р№ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р».

=== 6.8 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.


=== 6.9 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚ РІС‹СЃС‚Р°РІР»СЏРµС‚СЃСЏ РїРѕ С„РѕСЂРјРµ в„–363', 'РЎС‡РµС‚ СЃРѕРґРµСЂР¶РёС‚ СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅ

=== 6.10 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓРєР°Р·Р°РЅРЅС‹Рµ СЃСЂРѕРєРё']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ Рї

=== 6.11 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ С„РѕСЂРјР°', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.

=== 6.12 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['РћРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РЎРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РћСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'РџРѕР»СѓС‡Р°С‚РµР»СЊ РїР»Р°С‚РµР¶Р° - СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363

=== 6.13 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РµР¶РµРјРµСЃСЏС‡РЅР°СЏ', 'СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РґРЅСЏРј РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»Р°', 'РїРµСЂРµСЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° Р·Р° РѕС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†', 'СѓРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ Р·Р° РєР°Р¶РґС‹Р№ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚Р°СЂРёС„РѕРј, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рј РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РІ РџСЂРёР»РѕР¶РµРЅРёРё 1.1 Рє Р”РѕРіРѕРІРѕСЂСѓ. РџСЂРё СЌС‚РѕРј СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РєРѕР»РёС‡РµСЃС‚РІСѓ РєР°Р»РµРЅРґР°СЂРЅ

=== 6.14 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.

=== 6.15 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµ

=== 6.16 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°

=== 6.17 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° СЃРµСЂРІРёСЃР° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.

=== 6.18 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'СЃСЂРѕРє РѕРїР»Р°С‚С‹ СЃС‡РёС‚Р°РµС‚СЃСЏ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЃС‡РµС‚Р°']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363

=== 6.20 ===
  main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° РЅРµ РІР·РёРјР°РµС‚СЃСЏ', 'СѓРґРµСЂР¶Р°РЅРЅР°СЏ РїР»Р°С‚Р° Р·Р° СЂР°СЃС‡РµС‚С‹ РїСЂРё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РѕРїРµСЂР°С†РёРё РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџРѕ РћРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рј С‚СЂР°РЅР·Р°РєС†РёСЏРј РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РЅРµ РІР·РёРјР°РµС‚СЃСЏ. Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ, СѓРґРµСЂР¶Р°РЅРЅР°СЏ Р‘Р°РЅРєРѕРј РїСЂРё РѕР±СЂР°Р±РѕС‚РєРµ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РћРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹, РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ.


[Command succeeded with exit code 0]
AI: The matrix text appears to have encoding issues in the output. Let me read the raw matrix file directly for the batch 2 items:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nmatrix = json.load(open(\'/inputs/matrix.json\', \'r\'))\nbatch_ids = [\'5.1.8.10\',\'5.1.8.11\',\'5.1.8.12\',\'5.1.8.13\',\'5.1.9\',\'5.1.10\',\'5.1.11\',\'5.1.12\',\'5.1.13\',\'5.1.14\',\'5.1.15\',\'5.1.16\',\'5.1.17.1\',\'5.1.17.2\',\'5.2.1\',\'5.2.2\',\'5.2.3\',\'5.2.4\',\'5.2.5\',\'5.2.6\',\'5.2.7\',\'5.2.8\',\'5.2.9\',\'5.2.10\',\'5.2.12\',\'6.1\',\'6.2\',\'6.3\',\'6.4\',\'6.5\',\'6.6\',\'6.7\',\'6.8\',\'6.9\',\'6.10\',\'6.11\',\'6.12\',\'6.13\',\'6.14\',\'6.15\',\'6.16\',\'6.17\',\'6.18\',\'6.20\']\nmatrix_by_id = {m[\'number\']: m for m in matrix}\nfor mid in batch_ids:\n    m = matrix_by_id.get(mid)\n    if m:\n        print(\'=== \' + mid + \' ===\')\n        print(\'  main_idea: \' + str(m.get(\'main_idea\',\'\'))[:200])\n        print(\'  required_type: \' + m[\'required_type\'])\n        print(\'  only_for_product: \' + m[\'only_for_product\'])\n        print(\'  only_for_lot: \' + m[\'only_for_lot\'])\n        print(\'  only_for_terminal: \' + m[\'only_for_terminal\'])\n        print(\'  payment_method: \' + m[\'payment_method\'])\n        print(\'  topics: \' + str(m.get(\'topics\',[])))\n        print(\'  enriched_text: \' + str(m.get(\'enriched_text\',\'\'))[:400])\n        print()\n" 2>&1'}, 'id': 'call_00_SW6Yhp7ct2yUUmpWzCMk6578', 'type': 'tool_call'}]
Tool: === 5.1.8.10 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РўРЎРў', 'РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР°;


=== 5.1.8.11 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РїСЂРµРґРїСЂРёСЏС‚РёСЏ', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РІС‹СЏРІР»РµРЅРЅРѕРј РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі Р·Р°СЏРІР»РµРЅРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў;

=== 5.1.8.12 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ;

=== 5.1.8.13 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°', 'РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°, СѓРєР°Р·Р°РЅРЅРѕРіРѕ РІ Рї. 10.1 Р”РѕРіРѕРІРѕСЂР°.

=== 5.1.9 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў', 'Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў, РІ С‚.С‡. РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё.

=== 5.1.10 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РџСЂРѕРІРµСЂРєРё РїСЂРѕРІРѕРґСЏС‚СЃСЏ РґР»СЏ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° Рё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СЂРѕРґР° РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РЅРµРј', 'РџСЂРѕРІРµСЂРєРё РІРєР»СЋС‡Р°СЋС‚ РєРѕРЅС‚СЂРѕР»СЊ СЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј С‚СЂРµР±РѕРІР°РЅРёР№ Р”РѕРіРѕРІРѕСЂР° Рє Р РµСЃСѓСЂСЃСѓ', 'Р‘Р°РЅРє РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕСЃС‚СѓРї Рє РѕС‚РґРµР»СЊРЅС‹Рј Р·Р°РєСЂС‹С‚С‹Рј СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° РїСЂРё РїСЂРѕРІРµСЂРєР°С…']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІ С‚.С‡. РЅР° РїСЂРµРґРјРµС‚ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РѕРїРµСЂР°С†РёР№, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёС… СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў, РЅРµСЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў С‚СЂРµР±РѕРІР°РЅРёР№, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… РЅР°СЃС‚РѕСЏС‰РёРј Р”РѕРіРѕРІРѕСЂРѕРј Рє Р РµСЃСѓСЂСЃСѓ[1].
[2]РџСЂРѕРІРµСЂРєРё РјРѕРіСѓС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊСЃСЏ Р‘Р°РЅРєРѕРј, РІ С‚РѕРј С‡РёСЃР»Рµ СЃ

=== 5.1.11 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ Р·Р°РїСЂР°С€РёРІР°С‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј', 'Р‘Р°РЅРє РјРѕР¶РµС‚ С‚СЂРµР±РѕРІР°С‚СЊ РїРёСЃСЊРјРµРЅРЅРѕРµ Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ СЃС‡РµС‚Р°, С‡РµРєРё Рё РёРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р±Р°РЅРєР°', 'РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ РєР°РЅР°Р»С‹ СЃРІСЏР·Рё СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р—Р°РїСЂР°С€РёРІР°С‚СЊ Р”РѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РЅРµ РїРѕР·РґРЅРµРµ 13 (С‚СЂРёРЅР°РґС†Р°С‚Рё) РјРµСЃСЏС†РµРІ СЃ РґР°С‚С‹ СЃРѕРІРµСЂС€РµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РІ Рї. 4.2.10 Р”РѕРіРѕРІРѕСЂР°. Р”Р»СЏ Р°РЅР°Р»РёР·Р° СЃРїРѕСЂРЅС‹С… СЃРёС‚СѓР°С†РёР№ Р‘Р°РЅРє С‚Р°РєР¶Рµ РјРѕР¶РµС‚ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ Р·Р°СЏРІР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РёР·Р»РѕР¶РµРЅРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё, СЃС‡РµС‚РѕРІ Р·Р° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹Рµ РўРѕРІР°СЂС‹/СѓСЃР»СѓРі

=== 5.1.12 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РІРїСЂР°РІРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ СЃРІСЏР·Р°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ unilateral_in_one_day_right', 'РћРїСѓР±Р»РёРєРѕРІР°РЅРёРµ РёР·РјРµРЅРµРЅРёР№ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ РґРѕРєСѓРјРµРЅС‚С‹, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ Р”РѕРіРѕРІРѕСЂРµ, РїСѓС‚РµРј РїСѓР±Р»РёРєР°С†РёРё РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР° РЅРµ РјРµРЅРµРµ С‡РµРј Р·Р° 1 (РѕРґРёРЅ) РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РґРµРЅСЊ РґРѕ РІРІРµРґРµРЅРёСЏ РІ РґРµР№СЃС‚РІРёРµ СѓРєР°Р·Р°РЅРЅС‹С… РёР·РјРµРЅРµРЅРёР№.

=== 5.1.13 ===
  main_idea: Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµРґРѕРјР»РµРЅРёСЏ, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РёР·РјРµРЅСЏС‚СЊ СЃРІРѕРё СЂРµРєРІРёР·РёС‚С‹', 'РЈРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёРё СЂРµРєРІРёР·РёС‚РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· РћС„РёС†РёР°Р»СЊРЅС‹Р№ СЃР°Р№С‚ Р‘Р°РЅРєР°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РёР·РјРµРЅРµРЅРёСЏ СЂРµРєРІРёР·РёС‚РѕРІ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹С… РІ Р”РѕРіРѕРІРѕСЂРµ, СѓРІРµРґРѕРјРёС‚СЊ РѕР± СЌС‚РѕРј РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСѓС‚РµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°. 

=== 5.1.14 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ', 'РђРґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ СѓРєР°Р·Р°РЅ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ', 'Р—Р°РїСЂРѕСЃС‹ РЅР°РїСЂР°РІР»РµРЅС‹ РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ С†РµР»СЏС… РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі /Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў.

=== 5.1.15 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· СѓРєР°Р·Р°РЅРёСЏ РїСЂРёС‡РёРЅ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· РѕР±СЉСЏСЃРЅРµРЅРёСЏ РїСЂРёС‡РёРЅ.

=== 5.1.16 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ', 'РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°

=== 5.1.17.1 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: pos
  payment_method: common
  topics: ['РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р°

=== 5.1.17.2 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ', 'С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏРј Р±Р°РЅРєР°', 'РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ 5.1.17.2. РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№

=== 5.2.1 ===
  main_idea: 
  required_type: mandatory
  only_for_product: internet_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ', 'РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РћРїРµСЂР°С†РёР№.

=== 5.2.2 ===
  main_idea: 
  required_type: mandatory
  only_for_product: internet_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё', 'РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№ РІ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіРµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Рё РўРµС…РЅРѕР»РѕРіРёР№ 3DSecure

=== 5.2.3 ===
  main_idea: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»РєРё РЅР° СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј РЅРµ СЏРІР»СЏРµС‚СЃСЏ
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['СѓСЃС‚Р°РЅРѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё', 'РїРѕРґРіРѕС‚РѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё', 'РїСЂРѕРІРµРґРµРЅРёРµ РїРµСЂРІРёС‡РЅРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЈСЃС‚Р°РЅРѕРІРёС‚СЊ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№. РџСЂРѕРІРµСЃС‚Рё РїРµСЂРІРёС‡РЅС‹Р№ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹РјРё Р‘Р°РЅРєРѕРј

=== 5.2.4 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚ РђРІС‚РѕСЂРёР·Р°С†РёСЋ Р±РµР· РїРµСЂРµСЂС‹РІРѕРІ 24 С‡Р°СЃР° РІ СЃСѓС‚РєРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ РђРІС‚РѕСЂРёР·Р°С†РёСЋ

=== 5.2.5 ===
  main_idea: РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РјРµС‰РµРЅС‹ РїРѕ СѓРєР°Р·Р°РЅРЅРѕР№ СЃСЃС‹Р»РєРµ', 'РјР°С‚РµСЂРёР°Р»С‹ РґРѕСЃС‚СѓРїРЅС‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р Р°Р·РјРµСЃС‚РёС‚СЊ РЅР° СЃР°Р№С‚Рµ:  https://www.sberbank.ru/help/business/acquiring РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ

=== 5.2.6 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РћР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё', 'РћР±РµСЃРїРµС‡РµРЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РЅРµРѕР±С…РѕРґРёРјС‹РјРё РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№

=== 5.2.7 ===
  main_idea: 
  required_type: optional
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅР°СЏ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ', 'Р·Р°РјРµРЅР° РЅРµРёСЃРїСЂР°РІРЅРѕРіРѕ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РЅР° РёСЃРїСЂР°РІРЅС‹Р№ РЅРµ РїРѕР·РґРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ Р·Р°СЏРІРєРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ. Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° РёР· СЃС‚СЂРѕСЏ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° Р‘Р°РЅРєР°, РѕР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїСЂР°РІРЅС‹Рј Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРј Р‘Р°РЅРєР° РЅРµ РїРѕР·РґРЅРµРµ 3 (С‚СЂРµС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ Р‘Р°РЅРєРѕРј Р·Р°СЏРІРєРё РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ РЅРѕРјРµСЂСѓ СЃР»СѓР¶Р±С‹ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР° РїРѕ 

=== 5.2.8 ===
  main_idea: Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅРµ РїРѕР·РґРЅРµРµ 2 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё', 'РґР°С‚Р° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё - СЂР°Р±РѕС‡РёР№ РґРµРЅСЊ, СЃР»РµРґСѓСЋС‰РёР№ Р·Р° РґРЅРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ СЃРІРµСЂРєРё РёС‚РѕРіРѕРІ', 'РїСЂРё С‚РµС…РЅРёС‡РµСЃРєРѕРј СЃР±РѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёСЃС…РѕРґРёС‚ С‡РµСЂРµР· 3 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅСЏ РїРѕСЃР»Рµ РїРѕСЃР»РµРґРЅРµР№ СѓСЃРїРµС€РЅРѕР№ СЃРІРµСЂРєРё']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕР№ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё, РїРµСЂРµРґР°РЅРЅРѕР№ РѕС‚ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°  / Р РµСЃСѓСЂСЃР° /QR-РєРѕРґР°  РІ Р‘Р°РЅРє, РЅРµ РїРѕР·РґРЅРµРµ 2 (РґРІСѓС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј РїРµСЂРµС‡РёСЃР»СЏС‚СЊ РЅР° СЂР°СЃС‡РµС‚РЅС‹Р№ (С‚РµРєСѓС‰РёР№) СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ РІ РІР°Р»СЋС‚Рµ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё (СЂСѓР±Р»Рё Р Р¤) Р·Р° РІС‹С‡РµС‚РѕРј СЃСѓРјРј, 

=== 5.2.9 ===
  main_idea: 
  required_type: optional
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: qr
  topics: ['РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ QR-РєРѕРґР° РїР°СЂС‚РЅРµСЂР° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РїРѕ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј РєР°РЅР°Р»Р°Рј СЃРІСЏР·Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ

=== 5.2.10 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: []
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РѕР±СЂР°Р±РѕС‚РєСѓ РџР”РЅ, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, Р° С‚Р°РєР¶Рµ РѕР±РµСЃРїРµС‡РёС‚СЊ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕСЃС‚СЊ Рё Р·Р°С‰РёС‚Сѓ РѕР±СЂР°Р±Р°С‚С‹РІР°РµРјС‹С… РџР”РЅ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° РѕС‚ 27 РёСЋР»СЏ 2006 в„– 152-Р¤Р— В«Рћ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…В». РџСЂРёРЅРёРјР°С‚СЊ РЅРµРѕР±С…РѕРґРёРјС‹Рµ РїСЂР°РІРѕРІС‹Рµ, РѕСЂРіР°РЅРёР·Р°С†РёРѕРЅРЅС‹Рµ Рё С‚РµС…РЅРёС‡РµСЃРєРёРµ РјРµСЂС‹ РёР»Рё РѕР±РµСЃРїРµС‡РёРІР°С‚СЊ РёС… РїСЂРёРЅСЏС‚РёРµ РґР»СЏ Р·Р°С‰РёС‚С‹ РїРѕР»СѓС‡Р°РµРјС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚Рё

=== 5.2.12 ===
  main_idea: 
  required_type: optional
  only_for_product: internet_acquiring
  only_for_lot: common
  only_for_terminal: common
  payment_method: qr
  topics: ['Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API Р±РµР· РіР°СЂР°РЅС‚РёР№']
  enriched_text: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API (РІ С‚.С‡. РІСЃС‘, С‡С‚Рѕ СЃРІСЏР·Р°РЅРѕ СЃ РѕСЂРіР°РЅРёР·Р°С†РёРµР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РїРѕСЃСЂРµРґСЃС‚РІРѕРј С‚Р°РєРѕРіРѕ API) В«РєР°Рє РµСЃС‚СЊВ» Р±РµР· РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РєР°РєРёС…-Р»РёР±Рѕ РіР°СЂР°РЅС‚РёР№

=== 6.1 ===
  main_idea: Р’Р°Р¶РЅРѕ
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р—Р° РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹, РџСЂРµРґРїСЂРёСЏС‚РёРµ СѓРїР»Р°С‡РёРІР°РµС‚ Р‘Р°РЅРєСѓ РїР»Р°С‚Сѓ РІ СЂР°Р·РјРµСЂРµ:
В«(____________) РїСЂРѕС†РµРЅС‚ РѕС‚ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚В».

=== 6.2 ===
  main_idea: РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµСЂРёРѕРґРёС‡РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°', 'РІ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РІРєР»СЋС‡РµРЅ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРј', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚[2] (РґР°Р»РµРµ вЂ“ РЈРџР”) РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†. 
Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р‘Р°РЅРєР°, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРµ Рї.6.1 Р”РѕРіРѕРІРѕСЂР°, РІРєР»СЋС‡Р°РµС‚ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°Рє

=== 6.3 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: fz_223
  only_for_terminal: common
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РђРєС‚ РґРѕ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РђРєС‚ РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РІРјРµСЃС‚Рµ СЃРѕ СЃС‡РµС‚РѕРј-С„Р°РєС‚СѓСЂРѕР№ С„РѕСЂРјС‹ 363', 'Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ 6.1 РґРѕРіРѕРІРѕСЂР°', 'Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї.3 СЃС‚.149 РќРљ Р Р¤', 'РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ Р‘Р°РЅРєРѕРј РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РђРєС‚ Рѕ РїРµСЂРµС‡РёСЃР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРј РѕРїРµСЂР°С†РёР№ РїРѕ РєР°СЂС‚Р°Рј РїРѕ С„РѕСЂРјРµ РџСЂРёР»РѕР¶РµРЅРёСЏ 2 Рє Р”РѕРіРѕРІРѕСЂСѓ (РґР°Р»РµРµ вЂ“ РђРєС‚) Рё СЃС‡РµС‚ С„.363 РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ, РїСЂРёС‡РёС‚Р°

=== 6.4 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Рё РІРѕР·РІСЂР°С‚РёС‚СЊ РЈРџР” (РїСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё)', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.

=== 6.5 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р±Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.

=== 6.6 ===
  main_idea: 
  required_type: mandatory
  only_for_product: common
  only_for_lot: fz_223
  only_for_terminal: common
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р°РєС‚Р° Рё СЃС‡РµС‚Р° С„РѕСЂРјС‹ 363', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РЅР° СЃС‡РµС‚, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„РѕСЂРјС‹ 363']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° РђРєС‚Р° Рё СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.

=== 6.7 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['СѓРєР°Р·Р°РЅ СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°', 'СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂСѓР±Р»РµР№ РІРєР»СЋС‡Р°СЏ РќР”РЎ', 'СѓСЃС‚Р°РЅРѕРІР»РµРЅ РµР¶РµРјРµСЃСЏС‡РЅС‹Р№ РїРѕСЂСЏРґРѕРє РѕРїР»Р°С‚С‹']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ РІ СЂР°Р·РјРµСЂРµ _____ (__________________) СЂСѓР±Р»РµР№ (РІРєР»СЋС‡Р°СЏ РќР”РЎ) Р·Р° РєР°Р¶РґС‹Р№ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р».

=== 6.8 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.


=== 6.9 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚ РІС‹СЃС‚Р°РІР»СЏРµС‚СЃСЏ РїРѕ С„РѕСЂРјРµ в„–363', 'РЎС‡РµС‚ СЃРѕРґРµСЂР¶РёС‚ СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё

=== 6.10 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓРєР°Р·Р°РЅРЅС‹Рµ СЃСЂРѕРєРё']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.

=== 6.11 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ С„РѕСЂРјР°', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.

=== 6.12 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['РћРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'РЎРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РћСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'РџРѕР»СѓС‡Р°С‚РµР»СЊ РїР»Р°С‚РµР¶Р° - СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.

=== 6.13 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РµР¶РµРјРµСЃСЏС‡РЅР°СЏ', 'СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РґРЅСЏРј РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»Р°', 'РїРµСЂРµСЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° Р·Р° РѕС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†', 'СѓРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ Р·Р° РєР°Р¶РґС‹Р№ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚Р°СЂРёС„РѕРј, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рј РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РІ РџСЂРёР»РѕР¶РµРЅРёРё 1.1 Рє Р”РѕРіРѕРІРѕСЂСѓ. РџСЂРё СЌС‚РѕРј СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РєРѕР»РёС‡РµСЃС‚РІСѓ РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РІ РўРЎРў. РџСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° СЂР°Р·РјРµСЂ 

=== 6.14 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.

=== 6.15 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.

=== 6.16 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј', 'РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.

=== 6.17 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: common
  only_for_terminal: smart
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° СЃРµСЂРІРёСЃР° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”', 'С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ', 'РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.

=== 6.18 ===
  main_idea: 
  required_type: mandatory
  only_for_product: trade_acquiring
  only_for_lot: fz_223
  only_for_terminal: smart
  payment_method: common
  topics: ['РѕРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№', 'СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ', 'РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363', 'СЃСЂРѕРє РѕРїР»Р°С‚С‹ СЃС‡РёС‚Р°РµС‚СЃСЏ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЃС‡РµС‚Р°']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363

=== 6.20 ===
  main_idea: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
  required_type: mandatory
  only_for_product: common
  only_for_lot: common
  only_for_terminal: common
  payment_method: common
  topics: ['РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° РЅРµ РІР·РёРјР°РµС‚СЃСЏ', 'СѓРґРµСЂР¶Р°РЅРЅР°СЏ РїР»Р°С‚Р° Р·Р° СЂР°СЃС‡РµС‚С‹ РїСЂРё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РѕРїРµСЂР°С†РёРё РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ']
  enriched_text: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџРѕ РћРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рј С‚СЂР°РЅР·Р°РєС†РёСЏРј РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РЅРµ РІР·РёРјР°РµС‚СЃСЏ. Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ, СѓРґРµСЂР¶Р°РЅРЅР°СЏ Р‘Р°РЅРєРѕРј РїСЂРё РѕР±СЂР°Р±РѕС‚РєРµ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РћРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹, РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ.


[Command succeeded with exit code 0]
AI: The matrix text has encoding issues in the terminal output. Let me read the raw matrix file directly for the key items. Let me now read the contract text and the legal propositions for the batch 2 items:[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 100}, 'id': 'call_00_zcF90kk7g1CDyNEkdXjX1382', 'type': 'tool_call'}, {'name': 'execute', 'args': {'command': 'python -c "\nimport json\nlp = json.load(open(\'/outputs/working/legal_propositions.json\', \'r\'))\nbatch_ids = [\'5.1.8.10\',\'5.1.8.11\',\'5.1.8.12\',\'5.1.8.13\',\'5.1.9\',\'5.1.10\',\'5.1.11\',\'5.1.12\',\'5.1.13\',\'5.1.14\',\'5.1.15\',\'5.1.16\',\'5.1.17.1\',\'5.1.17.2\',\'5.2.1\',\'5.2.2\',\'5.2.3\',\'5.2.4\',\'5.2.5\',\'5.2.6\',\'5.2.7\',\'5.2.8\',\'5.2.9\',\'5.2.10\',\'5.2.12\',\'6.1\',\'6.2\',\'6.3\',\'6.4\',\'6.5\',\'6.6\',\'6.7\',\'6.8\',\'6.9\',\'6.10\',\'6.11\',\'6.12\',\'6.13\',\'6.14\',\'6.15\',\'6.16\',\'6.17\',\'6.18\',\'6.20\']\nmatrix_lp = {m[\'id\']: m for m in lp[\'matrix\']}\nfor mid in batch_ids:\n    m = matrix_lp.get(mid)\n    if m:\n        print(\'=== \' + mid + \' ===\')\n        print(\'  materiality: \' + m.get(\'materiality\',\'\'))\n        print(\'  protected_party: \' + m.get(\'protected_party\',\'\'))\n        print(\'  bound_party: \' + m.get(\'bound_party\',\'\'))\n        print(\'  right_or_obligation: \' + m.get(\'right_or_obligation\',\'\'))\n        print(\'  legal_object: \' + m.get(\'legal_object\',\'\'))\n        print()\n    else:\n        print(\'=== \' + mid + \' === NOT IN LEDGER\')\n"'}, 'id': 'call_01_NKXCfryMTLx0eEbWydLR8999', 'type': 'tool_call'}]
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
Tool: === 5.1.8.10 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РїРµСЂРµРґР°С‡Р° РґР°РЅРЅС‹С… РІ Р РѕСЃС„РёРЅРјРѕРЅРёС‚РѕСЂРёРЅРі

=== 5.1.8.11 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РїРµСЂРµРґР°С‡Р° РґР°РЅРЅС‹С… РІ Р¤РќРЎ

=== 5.1.8.12 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РїРµСЂРµРґР°С‡Р° РґР°РЅРЅС‹С… РІ РџР¤Р 

=== 5.1.8.13 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РїРµСЂРµРґР°С‡Р° РґР°РЅРЅС‹С… РёРЅС‹Рј СѓРїРѕР»РЅРѕРјРѕС‡РµРЅРЅС‹Рј РѕСЂРіР°РЅР°Рј

=== 5.1.9 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: РѕР±СЂР°Р±РѕС‚РєР° РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…

=== 5.1.10 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСѓРјРј РѕРїРµСЂР°С†РёР№

=== 5.1.11 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: РѕР±РµСЃРїРµС‡РµРЅРёРµ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚Рё С‚РµСЂРјРёРЅР°Р»РѕРІ

=== 5.1.12 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: Р°РІС‚РѕСЂРёР·Р°С†РёСЏ

=== 5.1.13 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ

=== 5.1.14 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РѕР± СѓСЃР»СѓРіР°С…

=== 5.1.15 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ СѓСЃР»СѓРі Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ

=== 5.1.16 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: С„РѕСЂРјРёСЂРѕРІР°РЅРёРµ РґРѕРєСѓРјРµРЅС‚Р° Рѕ РїСЂРёРµРјРєРµ

=== 5.1.17.1 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: СѓСЃС‚Р°РЅРѕРІРєР° С‚РµСЂРјРёРЅР°Р»РѕРІ

=== 5.1.17.2 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ

=== 5.2.1 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: С‚СЂРµР±РѕРІР°РЅРёРµ РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ

=== 5.2.2 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРёР№ РѕС‚РєР°Р· РѕС‚ РёСЃРїРѕР»РЅРµРЅРёСЏ

=== 5.2.3 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РїСЂРѕРІРµСЂРєР° С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ С‚РµСЂРјРёРЅР°Р»РѕРІ

=== 5.2.4 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: СѓРґР°Р»РµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ РџРћ

=== 5.2.5 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: Р·Р°РїСЂРѕСЃ РґРѕРєСѓРјРµРЅС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј

=== 5.2.6 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР°
  legal_object: СѓРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёРё СЂРµРєРІРёР·РёС‚РѕРІ

=== 5.2.7 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: Р·Р°РїСЂРѕСЃ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РѕРїРµСЂР°С†РёСЏРј

=== 5.2.8 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: С‚СЂРµР±РѕРІР°РЅРёРµ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№

=== 5.2.9 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РїСЂРёРѕСЃС‚Р°РЅРѕРІРєР° Р°РІС‚РѕСЂРёР·Р°С†РёРё / СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ

=== 5.2.10 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: СѓРґРµСЂР¶Р°РЅРёРµ СЃСѓРјРј

=== 5.2.12 ===
  materiality: evaluable
  protected_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: Р‘Р°РЅРє
  right_or_obligation: РїСЂР°РІРѕ Р‘Р°РЅРєР°
  legal_object: РёРЅС‹Рµ РїСЂР°РІР° Р‘Р°РЅРєР°

=== 6.1 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.2 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.3 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.4 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.5 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.6 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.7 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.8 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.9 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.10 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.11 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.12 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.13 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.14 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.15 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.16 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.17 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.18 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°

=== 6.20 ===
  materiality: evaluable
  protected_party: Р‘Р°РЅРє/РџСЂРµРґРїСЂРёСЏС‚РёРµ
  bound_party: РџСЂРµРґРїСЂРёСЏС‚РёРµ/Р‘Р°РЅРє
  right_or_obligation: РѕР±СЏР·Р°РЅРЅРѕСЃС‚СЊ СЃС‚РѕСЂРѕРЅ
  legal_object: Р°РЅС‚РёРєРѕСЂСЂСѓРїС†РёРѕРЅРЅР°СЏ РѕРіРѕРІРѕСЂРєР°


[Command succeeded with exit code 0]
AI: I notice the legal propositions ledger has encoding issues in the terminal output. Let me read the raw JSON directly. Also, I notice the matrix numbering in the ledger seems to have a different mapping than expected. Let me read the raw matrix JSON for the batch 2 items and the contract text more carefully. Let me also read the rest of the contract:[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 100, 'limit': 200}, 'id': 'call_00_jEowX4qacsYLApNIcFUx6652', 'type': 'tool_call'}, {'name': 'execute', 'args': {'command': 'python -c "\nimport json\n# Read raw matrix for batch 2 items\nmatrix = json.load(open(\'/inputs/matrix.json\', \'r\'))\nbatch_ids = [\'5.1.8.10\',\'5.1.8.11\',\'5.1.8.12\',\'5.1.8.13\',\'5.1.9\',\'5.1.10\',\'5.1.11\',\'5.1.12\',\'5.1.13\',\'5.1.14\',\'5.1.15\',\'5.1.16\',\'5.1.17.1\',\'5.1.17.2\',\'5.2.1\',\'5.2.2\',\'5.2.3\',\'5.2.4\',\'5.2.5\',\'5.2.6\',\'5.2.7\',\'5.2.8\',\'5.2.9\',\'5.2.10\',\'5.2.12\',\'6.1\',\'6.2\',\'6.3\',\'6.4\',\'6.5\',\'6.6\',\'6.7\',\'6.8\',\'6.9\',\'6.10\',\'6.11\',\'6.12\',\'6.13\',\'6.14\',\'6.15\',\'6.16\',\'6.17\',\'6.18\',\'6.20\']\nmatrix_by_id = {m[\'number\']: m for m in matrix}\n# Write to file for proper reading\nwith open(\'/outputs/working/batch2_matrix_dump.json\', \'w\', encoding=\'utf-8\') as f:\n    batch_data = {mid: matrix_by_id.get(mid) for mid in batch_ids}\n    json.dump(batch_data, f, ensure_ascii=False, indent=2)\nprint(\'Written batch2_matrix_dump.json\')\n"'}, 'id': 'call_01_2Qpon07XlK0ZJDwxF3hi5372', 'type': 'tool_call'}]
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
Tool: Written batch2_matrix_dump.json

[Command succeeded with exit code 0]
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch2_matrix_dump.json', 'limit': 200}, 'id': 'call_00_VDp4bioQ2itMByq10rfO3290', 'type': 'tool_call'}]
Tool:      1	{
     2	  "5.1.8.10": {
     3	    "number": "5.1.8.10",
     4	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → выявление недостоверных сведений о Предприятии/ТСТ, руководителе(-ях) в информации, указанной при заключении Договора;\n",
     5	    "required_type": "optional",
     6	    "main_idea": "",
     7	    "only_for_product": "common",
     8	    "only_for_lot": "common",
     9	    "only_for_terminal": "common",
    10	    "topics": [
    11	      "выявление недостоверных сведений о Предприятии",
    12	      "выявление недостоверных сведений о ТСТ",
    13	      "выявление недостоверных сведений о руководителе Предприятия"
    14	    ],
    15	    "payment_method": "common"
    16	  },
    17	  "5.1.8.11": {
    18	    "number": "5.1.8.11",
    19	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Предприятия, указанному в Информации о ТСТ;",
    20	    "required_type": "optional",
    21	    "main_idea": "",
    22	    "only_for_product": "common",
    23	    "only_for_lot": "common",
    24	    "only_for_terminal": "common",
    25	    "topics": [
    26	      "Банк имеет право прекратить проведение авторизации при несоответствии товаров/услуг роду деятельности предприятия",
    27	      "Банк имеет право в одностороннем порядке расторгнуть договор при выявленном несоответствии товаров/услуг заявленной деятельности"
    28	    ],
    29	    "payment_method": "common"
    30	  },
    31	  "5.1.8.12": {
    32	    "number": "5.1.8.12",
    33	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → отсутствие операций в течение 30 (тридцати) календарных дней подряд;",
    34	    "required_type": "optional",
    35	    "main_idea": "",
    36	    "only_for_product": "common",
    37	    "only_for_lot": "common",
    38	    "only_for_terminal": "common",
    39	    "topics": [
    40	      "отсутствие операций в течение 30 календарных дней подряд является основанием для прекращения проведения авторизации и расторжения договора"
    41	    ],
    42	    "payment_method": "common"
    43	  },
    44	  "5.1.8.13": {
    45	    "number": "5.1.8.13",
    46	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → исчерпание Цены Договора и/или окончание срока действия Договора, указанного в п. 10.1 Договора.",
    47	    "required_type": "optional",
    48	    "main_idea": "",
    49	    "only_for_product": "common",
    50	    "only_for_lot": "common",
    51	    "only_for_terminal": "common",
    52	    "topics": [
    53	      "исчерпание Цены Договора",
    54	      "окончание срока действия Договора"
    55	    ],
    56	    "payment_method": "common"
    57	  },
    58	  "5.1.9": {
    59	    "number": "5.1.9",
    60	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять дополнительные проверки проведения Операции в ТСТ, в т.ч. обращаться в Банк-эмитент для проверки правомерности Операции.",
    61	    "required_type": "mandatory",
    62	    "main_idea": "",
    63	    "only_for_product": "common",
    64	    "only_for_lot": "common",
    65	    "only_for_terminal": "common",
    66	    "topics": [
    67	      "Банк имеет право осуществлять дополнительные проверки проведения Операции в ТСТ",
    68	      "Банк имеет право обращаться в Банк-эмитент для проверки правомерности Операции"
    69	    ],
    70	    "payment_method": "common"
    71	  },
    72	  "5.1.10": {
    73	    "number": "5.1.10",
    74	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Проводить проверку Предприятия, в т.ч. на предмет выявления мошеннических операций, предоставления Покупателям Товаров/услуг, несоответствующих роду деятельности Предприятия, указанному в Информации о ТСТ, несоблюдения Предприятием/ТСТ требований, установленных настоящим Договором к Ресурсу[1].\n[2]Проверки могут осуществляться Банком, в том числе с доступом к разделам Ресурса с ограниченным доступом, не связанным с администрированием и сопровождением (VIP, Оптовое, Клубное обслуживание, и т.п.).",
    75	    "required_type": "mandatory",
    76	    "main_idea": "",
    77	    "only_for_product": "common",
    78	    "only_for_lot": "common",
    79	    "only_for_terminal": "common",
    80	    "topics": [
    81	      "Банк имеет право проводить проверки Предприятия",
    82	      "Проверки проводятся для выявления мошенничества и несоответствия рода деятельности Предприятия информации о нем",
    83	      "Проверки включают контроль соблюдения Предприятием требований Договора к Ресурсу",
    84	      "Банк может осуществлять доступ к отдельным закрытым разделам Ресурса при проверках"
    85	    ],
    86	    "payment_method": "common"
    87	  },
    88	  "5.1.11": {
    89	    "number": "5.1.11",
    90	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Запрашивать Документы по операциям не позднее 13 (тринадцати) месяцев с даты совершения Операции в сроки, установленные в п. 4.2.10 Договора. Для анализа спорных ситуаций Банк также может потребовать от Предприятия предоставления письменного заявления Предприятия с изложением обстоятельств проведения Операции, счетов за предоставленные Товары/услуги, товарные или кассовые чеки и другие документы, необходимые для проведения анализа обстоятельств проведения операции или претензионной работы по электронным каналам связи одним из способов, указанных в п. 2.3 Договора.",
    91	    "required_type": "mandatory",
    92	    "main_idea": "",
    93	    "only_for_product": "common",
    94	    "only_for_lot": "common",
    95	    "only_for_terminal": "common",
    96	    "topics": [
    97	      "Банк имеет право запрашивать документы по операциям",
    98	      "Банк может требовать письменное заявление предприятия с обстоятельствами проведения операции",
    99	      "Предприятие обязано предоставить счета, чеки и иные документы по требованию банка",
   100	      "Обмен документами осуществляется через электронные каналы связи согласно пункту договора"
   101	    ],
   102	    "payment_method": "common"
   103	  },
   104	  "5.1.12": {
   105	    "number": "5.1.12",
   106	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке вносить изменения в документы, ссылки на которые даются в Договоре, путем публикации информации на Официальном сайте Банка не менее чем за 1 (один) календарный день до введения в действие указанных изменений.",
   107	    "required_type": "optional",
   108	    "main_idea": "",
   109	    "only_for_product": "common",
   110	    "only_for_lot": "common",
   111	    "only_for_terminal": "common",
   112	    "topics": [
   113	      "Банк вправе вносить изменения в связанные документы unilateral_in_one_day_right",
   114	      "Опубликование изменений осуществляется на Официальном сайте Банка"
   115	    ],
   116	    "payment_method": "common"
   117	  },
   118	  "5.1.13": {
   119	    "number": "5.1.13",
   120	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае изменения реквизитов Банка, указанных в Договоре, уведомить об этом Предприятие путем размещения информации на Официальном сайте Банка. ",
   121	    "required_type": "optional",
   122	    "main_idea": "Важно именно размещение информации на сайте. Если предусмотрены иные способы уведомления, то это разногласие",
   123	    "only_for_product": "common",
   124	    "only_for_lot": "common",
   125	    "only_for_terminal": "common",
   126	    "topics": [
   127	      "Банк имеет право изменять свои реквизиты",
   128	      "Уведомление об изменении реквизитов осуществляется через Официальный сайт Банка"
   129	    ],
   130	    "payment_method": "common"
   131	  },
   132	  "5.1.14": {
   133	    "number": "5.1.14",
   134	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В целях получения информации по Операциям направлять запросы на адрес электронной почты Предприятия/ТСТ, указанный в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ.",
   135	    "required_type": "mandatory",
   136	    "main_idea": "",
   137	    "only_for_product": "common",
   138	    "only_for_lot": "common",
   139	    "only_for_terminal": "common",
   140	    "topics": [
   141	      "Банк имеет право направлять запросы на адрес электронной почты Предприятия",
   142	      "Адрес электронной почты указан в Заявлении Предприятия на проведение расчетов",
   143	      "Запросы направлены для получения информации по Операциям"
   144	    ],
   145	    "payment_method": "common"
   146	  },
   147	  "5.1.15": {
   148	    "number": "5.1.15",
   149	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Отказать Предприятию в заключении Договора без объяснения причин.",
   150	    "required_type": "optional",
   151	    "main_idea": "",
   152	    "only_for_product": "common",
   153	    "only_for_lot": "common",
   154	    "only_for_terminal": "common",
   155	    "topics": [
   156	      "Банк имеет право отказать Предприятию в заключении Договора без указания причин"
   157	    ],
   158	    "payment_method": "common"
   159	  },
   160	  "5.1.16": {
   161	    "number": "5.1.16",
   162	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Требовать от Предприятия предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства",
   163	    "required_type": "mandatory",
   164	    "main_idea": "",
   165	    "only_for_product": "common",
   166	    "only_for_lot": "common",
   167	    "only_for_terminal": "common",
   168	    "topics": [
   169	      "Банк имеет право требовать от Предприятия предоставления документов",
   170	      "Перечень требуемых документов определяется законодательством"
   171	    ],
   172	    "payment_method": "common"
   173	  },
   174	  "5.1.17.1": {
   175	    "number": "5.1.17.1",
   176	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов/Смарт-терминалов, находящихся в собственности Банка, в случае если: → Торговый оборот на один Электронный терминал Банка не превышает 40 000 (сорок тысяч) рублей (для г. Москва и г. Санкт-Петербург не превышает 80 000 (восемьдесят тысяч) рублей) за последний календарный месяц (без учета в обороте Операций возврата);",
   177	    "required_type": "optional",
   178	    "main_idea": "",
   179	    "only_for_product": "trade_acquiring",
   180	    "only_for_lot": "common",
   181	    "only_for_terminal": "pos",
   182	    "topics": [
   183	      "оборот менее 40 000 руб. за месяц для регионов",
   184	      "оборот менее 80 000 руб. за месяц для Москвы и СПб"
   185	    ],
   186	    "payment_method": "common"
   187	  },
   188	  "5.1.17.2": {
   189	    "number": "5.1.17.2",
   190	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов/Смарт-терминалов, находящихся в собственности Банка, в случае если: → 5.1.17.2. Торговый оборот на один Смарт-терминал Банка не превышает 40 000 (сорок тысяч) рублей (для г. Москва и г. Санкт-Петербург не превышает 80 000 (восемьдесят тысяч) рублей) за последний календарный месяц (без учета в обороте Операций возврата) или имеется задолженность перед Банком по плате за сервисное обслуживание/вознаграждения Банка/Операциям возврата Смарт-терминала Банка.",
   191	    "required_type": "optional",
   192	    "main_idea": "",
   193	    "only_for_product": "trade_acquiring",
   194	    "only_for_lot": "common",
   195	    "only_for_terminal": "smart",
   196	    "topics": [
   197	      "торговый оборот менее 40 000 руб. для регионов",
   198	      "торговый оборот менее 80 000 руб. для Москвы и СПб",
   199	      "наличие задолженности по сервисному обслуживанию",
   200	      "наличие задолженности по вознаграждениям банка",
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch2_matrix_dump.json', 'offset': 200}, 'id': 'call_00_3pHprSCkNRFjKAILlY485389', 'type': 'tool_call'}]
Tool:    201	      "наличие задолженности по операциям возврата смарт-терминала"
   202	    ],
   203	    "payment_method": "common"
   204	  },
   205	  "5.2.1": {
   206	    "number": "5.2.1",
   207	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечить Предприятию доступ к СПЭП для осуществления Операций.",
   208	    "required_type": "mandatory",
   209	    "main_idea": "",
   210	    "only_for_product": "internet_acquiring",
   211	    "only_for_lot": "common",
   212	    "only_for_terminal": "common",
   213	    "topics": [
   214	      "обязательство обеспечить доступ к СПЭП",
   215	      "описание порядка доступа к СПЭП"
   216	    ],
   217	    "payment_method": "common"
   218	  },
   219	  "5.2.2": {
   220	    "number": "5.2.2",
   221	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечить безопасность проведения Операций в Интернет-эквайринге посредством использования современных протоколов и Технологий 3DSecure",
   222	    "required_type": "mandatory",
   223	    "main_idea": "",
   224	    "only_for_product": "internet_acquiring",
   225	    "only_for_lot": "common",
   226	    "only_for_terminal": "common",
   227	    "topics": [
   228	      "использование современных протоколов безопасности",
   229	      "использование технологий 3DSecure"
   230	    ],
   231	    "payment_method": "common"
   232	  },
   233	  "5.2.3": {
   234	    "number": "5.2.3",
   235	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Установить на Предприятии и подготовить к эксплуатации Электронные терминалы/Смарт-терминалы Банка для проведения Операций. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком",
   236	    "required_type": "mandatory",
   237	    "main_idea": "Важно, чтобы в договоре срок установки был не менее 3 рабочих дней. Срок инструктажа не декларируется. Отсутствие отсылки на с инструктивные материалы разногласием не является",
   238	    "only_for_product": "trade_acquiring",
   239	    "only_for_lot": "common",
   240	    "only_for_terminal": "common",
   241	    "topics": [
   242	      "установка Электронных терминалов/Смарт-терминалов Банка на Предприятии",
   243	      "подготовка Электронных терминалов/Смарт-терминалов Банка к эксплуатации",
   244	      "проведение первичного инструктажа работников ТСТ"
   245	    ],
   246	    "payment_method": "common"
   247	  },
   248	  "5.2.4": {
   249	    "number": "5.2.4",
   250	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять круглосуточную Авторизацию",
   251	    "required_type": "optional",
   252	    "main_idea": "",
   253	    "only_for_product": "common",
   254	    "only_for_lot": "common",
   255	    "only_for_terminal": "common",
   256	    "topics": [
   257	      "Банк осуществляет Авторизацию без перерывов 24 часа в сутки"
   258	    ],
   259	    "payment_method": "common"
   260	  },
   261	  "5.2.5": {
   262	    "number": "5.2.5",
   263	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Разместить на сайте:  https://www.sberbank.ru/help/business/acquiring обучающие материалы для прохождения инструктажа сотрудниками Предприятия",
   264	    "required_type": "optional",
   265	    "main_idea": "Подсвечивать разногласие, если только сайты отличаются, если в договоре вместо сайта прочерк, то это не разногласие",
   266	    "only_for_product": "common",
   267	    "only_for_lot": "common",
   268	    "only_for_terminal": "common",
   269	    "topics": [
   270	      "обучающие материалы размещены по указанной ссылке",
   271	      "материалы доступны для прохождения инструктажа сотрудниками Предприятия"
   272	    ],
   273	    "payment_method": "common"
   274	  },
   275	  "5.2.6": {
   276	    "number": "5.2.6",
   277	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечивать Электронные терминалы/Смарт-терминалы, установленные на Предприятии/ТСТ, информационными материалами, необходимыми для проведения Операций",
   278	    "required_type": "optional",
   279	    "main_idea": "",
   280	    "only_for_product": "trade_acquiring",
   281	    "only_for_lot": "common",
   282	    "only_for_terminal": "common",
   283	    "topics": [
   284	      "Обеспечение Электронных терминалов информационными материалами",
   285	      "Обеспечение Смарт-терминалов информационными материалами"
   286	    ],
   287	    "payment_method": "common"
   288	  },
   289	  "5.2.7": {
   290	    "number": "5.2.7",
   291	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечивать круглосуточную работоспособность Электронных терминалов/Смарт-терминалов. В случае выхода из строя Электронного терминала/Смарт-терминала Банка, обеспечить Предприятие исправным Электронным терминалом/Смарт-терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Банком заявки от Предприятия по номеру службы поддержки Банка по телефонам, указанным в п..2. Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.",
   292	    "required_type": "optional",
   293	    "main_idea": "",
   294	    "only_for_product": "common",
   295	    "only_for_lot": "common",
   296	    "only_for_terminal": "common",
   297	    "topics": [
   298	      "круглосуточная работоспособность Электронных терминалов/Смарт-терминалов",
   299	      "замена неисправного Электронного терминала/Смарт-терминала на исправный не позднее 3 рабочих дней после заявки"
   300	    ],
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch2_matrix_dump.json', 'offset': 300}, 'id': 'call_00_JrjpSCCUYWqvQDzjp1Ig8579', 'type': 'tool_call'}]
Tool:    301	    "payment_method": "common"
   302	  },
   303	  "5.2.8": {
   304	    "number": "5.2.8",
   305	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → На основании полученной от Предприятия расчетной информации, переданной от Электронного терминала/Смарт-терминала  / Ресурса /QR-кода  в Банк, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Банком перечислять на расчетный (текущий) счет Предприятия суммы Операций оплаты в валюте проведения операции (рубли РФ) за вычетом сумм, перечисленных в п.5.1.1 настоящего Договора. Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. ➜ «ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. ➜ «ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → В случае технического сбоя при передаче Электронной сверки итогов/ невозможности проведения Предприятием/ТСТ или отсутствия Электронной сверки итогов по иным причинам, перечислять Предприятию суммы Операций, за исключением сумм, указанных в первом абзаце настоящего пункта (п.5.2.8), по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов, проводить расчеты по всем Операциям с данной ТСТ. ",
   306	    "required_type": "mandatory",
   307	    "main_idea": "Важен срок перечисления средств",
   308	    "only_for_product": "common",
   309	    "only_for_lot": "common",
   310	    "only_for_terminal": "common",
   311	    "topics": [
   312	      "перечисление средств на счет Предприятия не позднее 2 рабочих дней после получения расчетной информации",
   313	      "дата получения расчетной информации - рабочий день, следующий за днем электронной сверки итогов",
   314	      "при техническом сбое перечисление средств происходит через 3 календарных дня после последней успешной сверки"
   315	    ],
   316	    "payment_method": "common"
   317	  },
   318	  "5.2.9": {
   319	    "number": "5.2.9",
   320	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Предоставить Предприятию QR-код партнера по электронным каналам связи в электронном виде или на бумажном носителе",
   321	    "required_type": "optional",
   322	    "main_idea": "",
   323	    "only_for_product": "trade_acquiring",
   324	    "only_for_lot": "common",
   325	    "only_for_terminal": "common",
   326	    "topics": [
   327	      "Предоставление QR-кода партнера в электронном виде или на бумажном носителе"
   328	    ],
   329	    "payment_method": "qr"
   330	  },
   331	  "5.2.10": {
   332	    "number": "5.2.10",
   333	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять обработку ПДн, полученных от Предприятия, а также обеспечить конфиденциальность и защиту обрабатываемых ПДн в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных». Принимать необходимые правовые, организационные и технические меры или обеспечивать их принятие для защиты получаемых от Предприятия ПДн от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения ПДн, а также от иных неправомерных действий в отношении получаемых от Предприятия ПДн",
   334	    "required_type": "mandatory",
   335	    "main_idea": "",
   336	    "only_for_product": "common",
   337	    "only_for_lot": "common",
   338	    "only_for_terminal": "common",
   339	    "topics": [],
   340	    "payment_method": "common"
   341	  },
   342	  "5.2.12": {
   343	    "number": "5.2.12",
   344	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Банк предоставляет QR-API (в т.ч. всё, что связано с организацией информационно-технологического взаимодействия посредством такого API) «как есть» без предоставления каких-либо гарантий",
   345	    "required_type": "optional",
   346	    "main_idea": "",
   347	    "only_for_product": "internet_acquiring",
   348	    "only_for_lot": "common",
   349	    "only_for_terminal": "common",
   350	    "topics": [
   351	      "Банк предоставляет QR-API без гарантий"
   352	    ],
   353	    "payment_method": "qr"
   354	  },
   355	  "6.1": {
   356	    "number": "6.1",
   357	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → За осуществление расчетов по Операциям оплаты, Предприятие уплачивает Банку плату в размере:\n«(____________) процент от суммы Операций оплат».",
   358	    "required_type": "mandatory",
   359	    "main_idea": "Важно",
   360	    "only_for_product": "common",
   361	    "only_for_lot": "common",
   362	    "only_for_terminal": "common",
   363	    "topics": [
   364	      "размер платы в процентах от суммы операций"
   365	    ],
   366	    "payment_method": "common"
   367	  },
   368	  "6.2": {
   369	    "number": "6.2",
   370	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за месяцем оказания услуг (далее – Отчетный месяц), направляет Предприятию Универсальный передаточный документ[2] (далее – УПД) на оплату услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц. \nВознаграждение Банка, установленное п.6.1 Договора, включает НДС по ставке, установленной законодательством Российской Федерации.",
   371	    "required_type": "mandatory",
   372	    "main_idea": "УПД - это универсальный передаточный документ (документ о приёмке, документ на оплату услуг). Важно проверить сроки и периодичность оплаты",
   373	    "only_for_product": "common",
   374	    "only_for_lot": "common",
   375	    "only_for_terminal": "common",
   376	    "topics": [
   377	      "Банк направляет документ на оплату услуг Банка",
   378	      "в вознаграждение банка включен НДС по ставке, установленной законом",
   379	      "Срок направления документа на оплату услуг Банка"
   380	    ],
   381	    "payment_method": "common"
   382	  },
   383	  "6.3": {
   384	    "number": "6.3",
   385	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за месяцем оказания услуг (далее – Отчетный месяц), направляет Предприятию Акт о перечислении Предприятию сумм операций по картам по форме Приложения 2 к Договору (далее – Акт) и счет ф.363 на оплату услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц.Размер вознаграждения, причитающегося Банку, определяется в соответствии с п.6.1 Договора и не облагается НДС на основании п. 3 ст. 149 Налогового кодекса Российской Федерации.",
   386	    "required_type": "mandatory",
   387	    "main_idea": "",
   388	    "only_for_product": "common",
   389	    "only_for_lot": "fz_223",
   390	    "only_for_terminal": "common",
   391	    "topics": [
   392	      "Банк направляет Акт до 10 рабочего дня месяца, следующего за отчетным",
   393	      "Акт направляется вместе со счетом-фактурой формы 363",
   394	      "Размер вознаграждения определяется согласно пункту 6.1 договора",
   395	      "Вознаграждение банка не облагается НДС на основании п.3 ст.149 НК РФ",
   396	      "Срок направления Банком документа на оплату услуг Банка"
   397	    ],
   398	    "payment_method": "common"
   399	  },
   400	  "6.4": {
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch2_matrix_dump.json', 'offset': 400}, 'id': 'call_00_eOFOJ9v2tt64lw2uxkRA6754', 'type': 'tool_call'}]
Tool:    401	    "number": "6.4",
   402	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД либо предоставить мотивированный отказ от подписания УПД.",
   403	    "required_type": "mandatory",
   404	    "main_idea": "",
   405	    "only_for_product": "common",
   406	    "only_for_lot": "common",
   407	    "only_for_terminal": "common",
   408	    "topics": [
   409	      "Предприятие обязано принять и возвратить УПД (принять оказанные услуги)",
   410	      "Предприятие предоставляет мотивированный отказ от подписания УПД в установленные сроки"
   411	    ],
   412	    "payment_method": "common"
   413	  },
   414	  "6.5": {
   415	    "number": "6.5",
   416	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Оплата услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
   417	    "required_type": "mandatory",
   418	    "main_idea": "",
   419	    "only_for_product": "common",
   420	    "only_for_lot": "common",
   421	    "only_for_terminal": "common",
   422	    "topics": [
   423	      "оплата услуг банка осуществляется в течение 5 рабочих дней после подписания УПД",
   424	      "форма оплаты - безналичная",
   425	      "денежные средства перечисляются на счет банка, указанный в УПД"
   426	    ],
   427	    "payment_method": "common"
   428	  },
   429	  "6.6": {
   430	    "number": "6.6",
   431	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Оплата услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты получения от Банка Акта и счета ф.363 в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в счете ф.363.",
   432	    "required_type": "mandatory",
   433	    "main_idea": "",
   434	    "only_for_product": "common",
   435	    "only_for_lot": "fz_223",
   436	    "only_for_terminal": "common",
   437	    "topics": [
   438	      "оплата услуг банка осуществляется в течение 5 рабочих дней после получения акта и счета формы 363",
   439	      "форма оплаты - безналичная",
   440	      "перечисление средств производится на счет, указанный в счете формы 363"
   441	    ],
   442	    "payment_method": "common"
   443	  },
   444	  "6.7": {
   445	    "number": "6.7",
   446	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Плата за сервисное обслуживание Электронных терминалов уплачивается Предприятием ежемесячно в размере _____ (__________________) рублей (включая НДС) за каждый Электронный терминал.",
   447	    "required_type": "mandatory",
   448	    "main_idea": "",
   449	    "only_for_product": "trade_acquiring",
   450	    "only_for_lot": "common",
   451	    "only_for_terminal": "smart",
   452	    "topics": [
   453	      "указан размер платы за сервисное обслуживание Электронного терминала",
   454	      "указано количество рублей включая НДС",
   455	      "установлен ежемесячный порядок оплаты"
   456	    ],
   457	    "payment_method": "common"
   458	  },
   459	  "6.8": {
   460	    "number": "6.8",
   461	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию УПД  на сумму платы за сервисное обслуживание Электронных терминалов за Отчетный месяц.\n",
   462	    "required_type": "mandatory",
   463	    "main_idea": "",
   464	    "only_for_product": "trade_acquiring",
   465	    "only_for_lot": "common",
   466	    "only_for_terminal": "smart",
   467	    "topics": [
   468	      "Банк направляет УПД не позднее 5 рабочего дня месяца, следующего за отчетным",
   469	      "УПД направляется на сумму платы за сервисное обслуживание Электронных терминалов"
   470	    ],
   471	    "payment_method": "common"
   472	  },
   473	  "6.9": {
   474	    "number": "6.9",
   475	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию счет ф.363 на сумму платы за сервисное обслуживание Электронных терминалов за Отчетный месяц.\nСчет-фактура предоставляется Банком в порядке и сроки, установленные действующим налоговым законодательством Российской Федерации",
   476	    "required_type": "mandatory",
   477	    "main_idea": "",
   478	    "only_for_product": "trade_acquiring",
   479	    "only_for_lot": "fz_223",
   480	    "only_for_terminal": "smart",
   481	    "topics": [
   482	      "Банк выставляет счет не позднее 10 рабочего дня месяца, следующего за отчетным",
   483	      "Счет выставляется по форме №363",
   484	      "Счет содержит сумму платы за сервисное обслуживание Электронных терминалов",
   485	      "Счет-фактура предоставляется в соответствии с налоговым законодательством РФ"
   486	    ],
   487	    "payment_method": "common"
   488	  },
   489	  "6.10": {
   490	    "number": "6.10",
   491	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД на сумму платы за сервисное обслуживание Электронных терминалов за Отчетный месяц либо предоставить мотивированный отказ от подписания УПД.",
   492	    "required_type": "mandatory",
   493	    "main_idea": "",
   494	    "only_for_product": "trade_acquiring",
   495	    "only_for_lot": "common",
   496	    "only_for_terminal": "smart",
   497	    "topics": [
   498	      "Предприятие возвращает подписанный УПД не позднее 25 числа месяца, следующего за отчетным",
   499	      "Предприятие предоставляет мотивированный отказ от подписания УПД в указанные сроки"
   500	    ],
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch2_matrix_dump.json', 'offset': 500}, 'id': 'call_00_TvltkRfjCNz4wrEsyETJ4837', 'type': 'tool_call'}]
Tool:    501	    "payment_method": "common"
   502	  },
   503	  "6.11": {
   504	    "number": "6.11",
   505	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Электронных терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
   506	    "required_type": "mandatory",
   507	    "main_idea": "",
   508	    "only_for_product": "trade_acquiring",
   509	    "only_for_lot": "common",
   510	    "only_for_terminal": "smart",
   511	    "topics": [
   512	      "оплата за сервисное обслуживание Электронных терминалов производится в течение 5 рабочих дней",
   513	      "способ оплаты - безналичная форма",
   514	      "деньги перечисляются на счет Банка, указанный в УПД"
   515	    ],
   516	    "payment_method": "common"
   517	  },
   518	  "6.12": {
   519	    "number": "6.12",
   520	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Электронных терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты получения от Банка счета ф.363 в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в счете ф.363.",
   521	    "required_type": "mandatory",
   522	    "main_idea": "",
   523	    "only_for_product": "trade_acquiring",
   524	    "only_for_lot": "fz_223",
   525	    "only_for_terminal": "smart",
   526	    "topics": [
   527	      "Оплата производится в течение 5 рабочих дней",
   528	      "Способ оплаты - безналичный перевод",
   529	      "Основание для оплаты - счет формы 363",
   530	      "Получатель платежа - счет Банка, указанный в счете"
   531	    ],
   532	    "payment_method": "common"
   533	  },
   534	  "6.13": {
   535	    "number": "6.13",
   536	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Плата за сервисное обслуживание Смарт-терминалов уплачивается Предприятием ежемесячно за каждый Смарт-терминал в соответствии с тарифом, установленным при заключении Договора в Приложении 1.1 к Договору. При этом расчет платы осуществляется пропорционально количеству календарных дней месяца с даты установки Смарт-терминала в ТСТ. При подключении/отключении 2D сканера размер платы за Смарт-терминал пересчитывается за Отчетный месяц независимо от даты установки/снятия сканера:\n           - в размере _____ (__________________) рублей (включая НДС) за каждый Смарт-терминал;",
   537	    "required_type": "mandatory",
   538	    "main_idea": "",
   539	    "only_for_product": "trade_acquiring",
   540	    "only_for_lot": "common",
   541	    "only_for_terminal": "smart",
   542	    "topics": [
   543	      "плата за сервисное обслуживание Смарт-терминалов ежемесячная",
   544	      "расчет платы пропорционально дням месяца с даты установки терминала",
   545	      "пересчет платы при подключении/отключении 2D сканера за отчетный месяц",
   546	      "указана точная стоимость обслуживания"
   547	    ],
   548	    "payment_method": "common"
   549	  },
   550	  "6.14": {
   551	    "number": "6.14",
   552	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию УПД  на сумму платы за сервисное обслуживание Смарт-терминалов за Отчетный месяц.",
   553	    "required_type": "mandatory",
   554	    "main_idea": "",
   555	    "only_for_product": "trade_acquiring",
   556	    "only_for_lot": "common",
   557	    "only_for_terminal": "smart",
   558	    "topics": [
   559	      "Банк направляет УПД не позднее 5 рабочего дня месяца, следующего за отчетным",
   560	      "УПД направляется на сумму платы за сервисное обслуживание Смарт-терминалов"
   561	    ],
   562	    "payment_method": "common"
   563	  },
   564	  "6.15": {
   565	    "number": "6.15",
   566	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за Отчетным месяцем, направляет Предприятию счет ф.363 на сумму платы за сервисное обслуживание Смарт-терминалов за Отчетный месяц.\nСчет-фактура предоставляется Банком в порядке и сроки, установленные действующим налоговым законодательством Российской Федерации.",
   567	    "required_type": "mandatory",
   568	    "main_idea": "",
   569	    "only_for_product": "trade_acquiring",
   570	    "only_for_lot": "fz_223",
   571	    "only_for_terminal": "smart",
   572	    "topics": [
   573	      "Банк выставляет счет не позднее 10 рабочего дня месяца, следующего за отчетным",
   574	      "Счет-фактура предоставляется в соответствии с налоговым законодательством РФ"
   575	    ],
   576	    "payment_method": "common"
   577	  },
   578	  "6.16": {
   579	    "number": "6.16",
   580	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Предприятие в срок не позднее 25 (двадцать пятого) числа месяца, следующего за Отчетным месяцем, обязано возвратить в Банк подписанный Предприятием УПД на сумму платы за сервисное обслуживание Смарт-терминалов за Отчетный месяц либо предоставить мотивированный отказ от подписания УПД.",
   581	    "required_type": "mandatory",
   582	    "main_idea": "",
   583	    "only_for_product": "trade_acquiring",
   584	    "only_for_lot": "common",
   585	    "only_for_terminal": "smart",
   586	    "topics": [
   587	      "Предприятие возвращает подписанный УПД не позднее 25 числа месяца, следующего за отчетным",
   588	      "Предприятие предоставляет мотивированный отказ от подписания УПД в установленные сроки"
   589	    ],
   590	    "payment_method": "common"
   591	  },
   592	  "6.17": {
   593	    "number": "6.17",
   594	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Оплата за сервисное обслуживание Смарт-терминалов за Отчетный месяц производится Предприятием в течение 5 (пяти) рабочих дней с даты подписания УПД в безналичной форме путем перечисления Предприятием денежных средств на счет Банка, указанный в УПД.",
   595	    "required_type": "mandatory",
   596	    "main_idea": "",
   597	    "only_for_product": "trade_acquiring",
   598	    "only_for_lot": "common",
   599	    "only_for_terminal": "smart",
   600	    "topics": [

