## Summarized at 2026-06-26T07:38:26.885119+00:00

Human: Matrix batch 3 comparison (5.1.1.6 - 7.17)
AI: Let me start by reading the skill file and understanding the methodology, then examine the working files and source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_O3S5cXuINS36GUkjMwdJ0516', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_locator_registry.json'}, 'id': 'call_01_53yT7BprrYLa1gceJkJ58172', 'type': 'tool_call'}]
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
    68	### 1. Source Preflight
    69	
    70	Check `inputs/contract.txt` before analysis:
    71	
    72	- real clause numbering is present;
    73	- deep clause numbers are not visibly collapsed or shifted;
    74	- repeated locators have enough context to distinguish source rows;
    75	- text is readable and not corrupted by encoding.
    76	
    77	If the contract text is not usable, stop and write
    78	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
    79	invalid text.
    80	
    81	### 2. Clause Index
    82	
    83	Create `/outputs/working/clause_index.json`.
    84	
    85	It is a source map only. It must include:
    86	
    87	- every matrix `number`;
    88	- every contract clause, operative parent, definition, appendix/table row, and
    89	  unnumbered operative provision;
    90	- source text or source locator for each row;
    91	- context for duplicate printed contract ids.
    92	
    93	Do not use `clause_index` to decide legal status. It only proves source
    94	coverage and valid ids. Never overwrite it with a batch subset.
    95	
    96	Create `/outputs/working/contract_locator_registry.json` from the same source
    97	map. It is the closed list of contract locators:
    98	
    99	- final `contract_id` values must be copied from registry rows with
   100	  `final_allowed = true`;
   101	- appendix starts, table headings, and unnumbered anchors may be
   102	  `evidence_only = true` and cited only in `evidence_locators`;
   103	- do not create semantic, translated, corrected, parenthetical, or synthetic
   104	  contract ids.
   105	
   106	### 3. Legal Proposition Ledger
   107	
   108	Create `/outputs/working/legal_propositions.json`.
   109	
   110	This is the mandatory legal evidence ledger. It must contain `matrix` and
   111	`contract` arrays. Every evaluable proposition should include:
   112	
   113	- `id`: matrix number or printed contract locator;
   114	- `source_text`: text used for legal comparison;
   115	- `source_excerpt`: short quote supporting the normalized proposition;
   116	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   117	  `appendix`, `table`, or `technical`;
   118	- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
   119	- `protected_party`, `bound_party`;
   120	- `right_or_obligation`;
   121	- `legal_object`;
   122	- `trigger`;
   123	- `deadline`;
   124	- `amount_formula_cap`;
   125	- `procedure_channel`;
   126	- `liability_remedy`;
   127	- `scope_options`;
   128	- `consequence`;
   129	- `applicability_filters` where available.
   130	
   131	If a legally meaningful row cannot be normalized, mark it
   132	`needs_source_review` and explain the missing element. It is not fully
   133	processed until the source text has been reviewed. Do not proceed to final
   134	matching with unresolved source-review rows that could affect status.
   135	
   136	The ledger is an evidence table, not a substitute for the source. Matching may
   137	use it to find candidates. Status must still be confirmed against source text.
   138	
   139	Run the mechanical check before matching:
   140	
   141	```bash
   142	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working
   143	```
   144	
   145	Fix invalid working artifacts before delegating comparison work.
   146	
   147	### 4. Contract Product Profile
   148	
   149	Create `/outputs/working/contract_product_profile.json`.
   150	
   151	Extract from the contract:
   152	
   153	- product and payment channels;
   154	- lot/procurement type;
   155	- terminal/payment-device scope;
   156	- payment methods;
   157	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   158	
   159	Apply matrix filters before status:
   160	
   161	- `common` applies to every contract.
   162	- A filtered matrix item applies only when the profile matches
   163	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   164	- Mandatory applicable missing = high risk.
   165	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   166	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   167	  profile-based reason. Do not put them in final `unmatched_matrix`.
   168	- Optional applicable missing = low or conditional risk.
   169	- Slash-separated alternatives are options unless the matrix says all options
   170	  are mandatory.
   171	- Placeholder or blank in an applicable material term creates low-risk
   172	  `deviation` only for the exact requirement where the blank is a material
   173	  element. It must not downgrade neighboring channels, sibling duties, or an
   174	  entire package whose legal result is otherwise preserved.
   175	
   176	## Analogue Threshold
   177	
   178	Create a final link only when the contract proposition is a true legal analogue
   179	of the matrix proposition. Test:
   180	
   181	- same or equivalent protected party;
   182	- same or equivalent bound party;
   183	- same legal object;
   184	- same operative right, duty, prohibition, permission, remedy, or allocation of
   185	  risk;
   186	- material trigger, scope, procedure, and consequence are the same or legally
   187	  equivalent.
   188	
   189	Reject weak thematic candidates. A clause about the same broad topic is not a
   190	legal analogue when it governs a different object, party, trigger, procedure,
   191	or consequence.
   192	
   193	Common weak candidates to reject:
   194	
   195	- technical QR/card/terminal capability, advertising, or product description
   196	  does not satisfy a duty to provide a named payment product or operational
   197	  mechanism;
   198	- a general duty to provide personal data or consent does not satisfy a Bank
   199	  right to transfer fraud, payment-system, or issuer-verification information;
   200	- a general right to request documents does not satisfy a special right to
   201	  verify an operation through an issuer, payment system, or other named source;
   202	- general fault-based liability does not satisfy a special Bank exemption from
   203	  transfer delays, payment-system failures, or third-party delays.
   204	
   205	## Bidirectional Matching
   206	
   207	Perform both directions.
   208	
   209	Matrix to contract:
   210	
   211	- for each applicable evaluable matrix proposition, retrieve all contract
   212	  clauses that collectively cover the Bank-standard requirement;
   213	- use focused package recall: every final `contract_id` must cover a named
   214	  material element of the analyzed matrix proposition;
   215	- include a parent/root clause only when it creates the same right, duty,
   216	  procedure, basis, list of grounds, or consequence for that proposition;
   217	- include a child/detail clause only when it carries the same proposition's
   218	  deadline, amount, fee, penalty, formula, cap, ground, exception, procedure,
   219	  channel, remedy, or consequence;
   220	- include companion payment, acceptance, liability, termination,
   221	  document-exchange, appendix, or table clauses only when they govern the same
   222	  legal object and cure, change, or evidence a specific material element;
   223	- do not include clauses that are merely adjacent by section, same parent, same
   224	  topic, or useful background; record them as rejected or considered context;
   225	- if a material element remains uncovered, continue checking the source index
   226	  and ledger for possible clauses, but the purpose is to accept true analogues
   227	  or reject weak candidates, not to enlarge the final group;
   228	- a framework or legal-compliance clause may be a standalone analogue only when
   229	  it carries the same legal object or allocates the same risk, duty, or remedy.
   230	
   231	Contract to matrix:
   232	
   233	- for each evaluable contract proposition, find the matrix analogue group;
   234	- if none exists and the term has independent legal effect, classify it as
   235	  `extra_in_contract`;
   236	- close it as `not_material` only for headings, non-operative definitions,
   237	  requisites, signatures, blank forms, or other rows without standalone legal
   238	  effect. Do not use generic reasons such as "no final legal finding produced".
   239	- procurement/customer clauses with independent control, rejection,
   240	  acceptance, withholding, unilateral refusal, penalty, defect-cure,
   241	  force-majeure proof, reporting, audit, or no-change effect are
   242	  `extra_in_contract` when there is no true matrix analogue.
   243	
   244	Group related ids into many-to-many `links`. One matrix id may need several
   245	contract clauses. One contract clause may cover several matrix ids.
   246	
   247	A group link is allowed only for an indivisible legal package. Sibling matrix
   248	ids under the same parent are not automatically one group. Channels, grounds
   249	for withholding, termination bases, personal-data duties, liability children,
   250	and document-exchange subrequirements should stay as focused links when each
   251	has its own legal element.
   252	
   253	## Group-Level Status
   254	
   255	Assign status to the group, not to each atomic pair.
   256	
   257	- `aligned`: the contract package preserves the matrix legal result.
   258	- `deviation`: a true analogue exists, but any material element is changed,
   259	  narrowed, weakened, omitted, shifted, or blank.
   260	- `missing_in_contract`: no true contract analogue exists for an applicable
   261	  matrix requirement.
   262	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   263	  analogue.
   264	- `not_material`: internal ledger closure only; exclude from final report.
   265	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
   266	  final report because the requirement does not apply to the current product,
   267	  lot, terminal, payment method, or legal regime.
   268	
   269	Material elements include party, legal object, operative act, trigger,
   270	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   271	remedy, exception, Bank right, merchant duty, and consequence.
   272	
   273	Status containment:
   274	
   275	- a gap affects only the matrix id where that gap is a material element;
   276	- do not spread one missing deadline, blank channel, absent consent, changed
   277	  amount, or weak candidate across sibling requirements;
   278	- if one large group mixes aligned and deviating siblings, split it before
   279	  assigning status;
   280	- root/parent clauses may appear in several focused groups, but their presence
   281	  does not make all children share one status.
   282	
   283	Hard terms must be compared directly:
   284	
   285	- same material deadline/amount/procedure in the same legal obligation can be
   286	  `aligned`;
   287	- changed value or missing value is `deviation`;
   288	- a hard term from another clause counts only when that clause expressly
   289	  governs the same obligation or is explicitly incorporated;
   290	- a neighboring date, amount, or procedure for another legal object cannot cure
   291	  the gap.
   292	
   293	Do not downgrade for formal differences alone: heading, title, appendix label,
   294	permitted option selection, equivalent mandatory-law mechanism, or wording
   295	style.
   296	
   297	Do not downgrade for low-risk notes when the legal result is preserved. If the
   298	reason says the difference is merely terminological, beneficial to the Bank,
   299	already incorporated through another clause, or caused only by a mandatory
   300	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
   301	
   302	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
   303	when it materially worsens or changes a Bank-standard term: payment timing,
   304	acceptance control, withholding right, penalty/cap, termination power, protected
   305	party, evidence channel, or enforceability.
   306	
   307	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
   308	Before marking a liability group `aligned`, check the amount, formula, cap,
   309	trigger, protected party, excluded delay/non-delay buckets, and claim procedure
   310	across the whole package.
   311	
   312	## Risk Calibration
   313	
   314	Use `risk_level` consistently:
   315	
   316	- `none`: only for `aligned`;
   317	- `low`: optional applicable missing, placeholder, formal but legally manageable
   318	  gap;
   319	- `medium`: material deviation that can affect performance, evidence, payment,
   320	  control, liability, or enforceability;
   321	- `high`: mandatory missing, changed protected party, major payment/remedy
   322	  change, important Bank right omitted, or broad contract-only risk.
   323	
   324	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   325	a short evidence-based reason. Use concise quotes rather than long excerpts.
   326	
   327	## Final QA
   328	
   329	Before writing final artifacts:
   330	
   331	- verify `clause_index` covers all source ids;
   332	- verify `legal_proposition_ledger` has no unresolved
   333	  `needs_source_review` rows that can affect final status;
   334	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   335	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   336	  `coverage_ledger`;
   337	- verify every applicable evaluable matrix id is linked or in
   338	  `unmatched_matrix`;
   339	- verify out-of-scope / non-applicable matrix ids are not in final
   340	  `unmatched_matrix`;
   341	- verify every material contract id is closed as linked or extra;
   342	- verify `coverage_ledger` is derived from final `links`,
   343	  `unmatched_matrix`, and `unmatched_contract`;
   344	- verify every final id is visible in source text;
   345	- verify final `contract_id` values are registry-final-allowed and evidence-only
   346	  locators appear only in `evidence_locators`;
   347	- verify each final `contract_id` contributes a named element to its focused
   348	  group; otherwise split the group or reject the clause;
   349	- verify same-parent siblings do not share a deviation merely because they are
   350	  near each other;
   351	- verify `aligned` has no material discrepancy;
   352	- verify every `deviation` has a named legal gap and evidence;
   353	- verify weak candidates are not in final `links`;
   354	- verify `not_material` closures have a source-based legal reason and are not
   355	  placeholders for unreviewed contract terms;
   356	- verify non-material contract rows are absent from final `unmatched_contract`;
   357	- verify summary counts equal final arrays.
   358	
   359	## Output Discipline
   360	
   361	Follow `references/output-contract.md`.
   362	
   363	The final JSON must contain:
   364	
   365	- `analysis_profile`
   366	- `links`
   367	- `atomic_links`
   368	- `unmatched_matrix`
   369	- `unmatched_contract`
   370	- `coverage_ledger`
   371	- `summary`
   372	
   373	`links` carry group-level legal findings. `atomic_links` are traceability
   374	projections only and must inherit the group relationship. Do not assign
   375	separate final pair-level statuses.
   376	
   377	## Tools And Scripts
   378	
   379	Use helper scripts for mechanical work: source extraction, indexing,
   380	normalization checks, batch completeness, coverage validation, JSON schema
   381	checks, and Excel export. Do not put legal mapping or status decisions into
   382	hardcoded scripts.
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
AI: Let me continue reading the registry and also read the reference documents and source files.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_locator_registry.json', 'offset': 100, 'limit': 500}, 'id': 'call_00_3ThIrhMa1X5VfVRycPpS2650', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_01_YfsnqSdK1fOjZWed0QQg4035', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_02_4Nqg5q4RpYM8MLFSIFjN4432', 'type': 'tool_call'}]
Tool:    101	    "source_text": "банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;",
   102	    "source_excerpt": "банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;",
   103	    "source_locator": "2.1.3",
   104	    "line_start": 14,
   105	    "line_end": 14,
   106	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   107	    "final_allowed": true,
   108	    "evidence_only": false
   109	  },
   110	  {
   111	    "locator": "2.1.4",
   112	    "type": "operative",
   113	    "source_text": "возврат платежа – операция, инициируемая банком-эмитентом в соответствии с правилами платежной системы и оспаривающая предъявленную банком-эквайрером операцию (транзакцию). Результатом операции «Возврат платежа» является списание денежных средств со счета банка-эквайрера и зачисление на счет банка-эмитента;",
   114	    "source_excerpt": "возврат платежа – операция, инициируемая банком-эмитентом в соответствии с правилами платежной системы и оспаривающая предъявленную банком-эквайрером операцию (транзакцию). Результатом операции «Возврат платежа» является списание денежных с",
   115	    "source_locator": "2.1.4",
   116	    "line_start": 15,
   117	    "line_end": 15,
   118	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   119	    "final_allowed": true,
   120	    "evidence_only": false
   121	  },
   122	  {
   123	    "locator": "2.1.5",
   124	    "type": "operative",
   125	    "source_text": "держатель карты (держатель) – покупатель-физическое лицо, на имя которого выпущена карта;",
   126	    "source_excerpt": "держатель карты (держатель) – покупатель-физическое лицо, на имя которого выпущена карта;",
   127	    "source_locator": "2.1.5",
   128	    "line_start": 16,
   129	    "line_end": 16,
   130	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   131	    "final_allowed": true,
   132	    "evidence_only": false
   133	  },
   134	  {
   135	    "locator": "2.1.6",
   136	    "type": "operative",
   137	    "source_text": "документ по операции - документ на бумажном носителе или в электронном виде, являющийся основанием для осуществления расчетов по операциям, совершенным с использованием карты;",
   138	    "source_excerpt": "документ по операции - документ на бумажном носителе или в электронном виде, являющийся основанием для осуществления расчетов по операциям, совершенным с использованием карты;",
   139	    "source_locator": "2.1.6",
   140	    "line_start": 17,
   141	    "line_end": 17,
   142	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   143	    "final_allowed": true,
   144	    "evidence_only": false
   145	  },
   146	  {
   147	    "locator": "2.1.7",
   148	    "type": "operative",
   149	    "source_text": "код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации;",
   150	    "source_excerpt": "код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации;",
   151	    "source_locator": "2.1.7",
   152	    "line_start": 18,
   153	    "line_end": 18,
   154	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   155	    "final_allowed": true,
   156	    "evidence_only": false
   157	  },
   158	  {
   159	    "locator": "2.1.8",
   160	    "type": "operative",
   161	    "source_text": "контрольно-кассовая техника (ККТ) – программно-технические средства и их комплексы, обеспечивающие запись и хранение фискальных данных в фискальных накопителях, формирующие фискальные документы, обеспечивающие передачу фискальных документов в налоговые органы через оператора фискальных данных и печать фискальных документов на бумажных носителях в соответствии с правилами, установленными законодательством Российской Федерации о применении контрольно-кассовой техники;",
   162	    "source_excerpt": "контрольно-кассовая техника (ККТ) – программно-технические средства и их комплексы, обеспечивающие запись и хранение фискальных данных в фискальных накопителях, формирующие фискальные документы, обеспечивающие передачу фискальных документов",
   163	    "source_locator": "2.1.8",
   164	    "line_start": 19,
   165	    "line_end": 19,
   166	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   167	    "final_allowed": true,
   168	    "evidence_only": false
   169	  },
   170	  {
   171	    "locator": "2.1.9",
   172	    "type": "operative",
   173	    "source_text": "контрольная лента - отчет, распечатываемый на электронном терминале и содержащий информацию о транзакциях, совершенных в ТСТ на электронном терминале за определенный период;",
   174	    "source_excerpt": "контрольная лента - отчет, распечатываемый на электронном терминале и содержащий информацию о транзакциях, совершенных в ТСТ на электронном терминале за определенный период;",
   175	    "source_locator": "2.1.9",
   176	    "line_start": 20,
   177	    "line_end": 20,
   178	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   179	    "final_allowed": true,
   180	    "evidence_only": false
   181	  },
   182	  {
   183	    "locator": "2.1.10",
   184	    "type": "operative",
   185	    "source_text": "отложенный платеж - операция оплаты, осуществляемая на основании полученного от Заказчика/ТСТ сообщения, направленного с использованием электронного терминала, о наличии задолженности покупателя перед Заказчиком/ТСТ, после окончательного расчета;",
   186	    "source_excerpt": "отложенный платеж - операция оплаты, осуществляемая на основании полученного от Заказчика/ТСТ сообщения, направленного с использованием электронного терминала, о наличии задолженности покупателя перед Заказчиком/ТСТ, после окончательного ра",
   187	    "source_locator": "2.1.10",
   188	    "line_start": 21,
   189	    "line_end": 21,
   190	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   191	    "final_allowed": true,
   192	    "evidence_only": false
   193	  },
   194	  {
   195	    "locator": "2.1.11",
   196	    "type": "operative",
   197	    "source_text": "операция – действие, осуществляемое Заказчиком/ТСТ/покупателем на электронном терминале, в том числе операция оплаты, операция отмены, операция возврата, совершенная с использованием карты/реквизитов карты/NFС-карты/ без предъявления карты;",
   198	    "source_excerpt": "операция – действие, осуществляемое Заказчиком/ТСТ/покупателем на электронном терминале, в том числе операция оплаты, операция отмены, операция возврата, совершенная с использованием карты/реквизитов карты/NFС-карты/ без предъявления карты;",
   199	    "source_locator": "2.1.11",
   200	    "line_start": 22,
   201	    "line_end": 22,
   202	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   203	    "final_allowed": true,
   204	    "evidence_only": false
   205	  },
   206	  {
   207	    "locator": "2.1.12",
   208	    "type": "operative",
   209	    "source_text": "операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;",
   210	    "source_excerpt": "операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;",
   211	    "source_locator": "2.1.12",
   212	    "line_start": 23,
   213	    "line_end": 23,
   214	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   215	    "final_allowed": true,
   216	    "evidence_only": false
   217	  },
   218	  {
   219	    "locator": "2.1.13",
   220	    "type": "operative",
   221	    "source_text": "операция отмены – операция, выполняемая Заказчиком/ТСТ на электронном терминале/смарт-терминале, с целью отмены авторизации. Операция отмены авторизации выполняется до проведения операции «Сверка итогов»;",
   222	    "source_excerpt": "операция отмены – операция, выполняемая Заказчиком/ТСТ на электронном терминале/смарт-терминале, с целью отмены авторизации. Операция отмены авторизации выполняется до проведения операции «Сверка итогов»;",
   223	    "source_locator": "2.1.13",
   224	    "line_start": 24,
   225	    "line_end": 24,
   226	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   227	    "final_allowed": true,
   228	    "evidence_only": false
   229	  },
   230	  {
   231	    "locator": "2.1.14",
   232	    "type": "operative",
   233	    "source_text": "операция возврата – операция, оформляемая Заказчиком/ТСТ при возврате товаров/отказе от услуг или от части товаров/услуг, оплаченных картой, после проведения операции «Сверка итогов», следствием которой является возврат суммы операции оплаты или ее части на карту, предъявленную покупателем;",
   234	    "source_excerpt": "операция возврата – операция, оформляемая Заказчиком/ТСТ при возврате товаров/отказе от услуг или от части товаров/услуг, оплаченных картой, после проведения операции «Сверка итогов», следствием которой является возврат суммы операции оплат",
   235	    "source_locator": "2.1.14",
   236	    "line_start": 25,
   237	    "line_end": 25,
   238	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   239	    "final_allowed": true,
   240	    "evidence_only": false
   241	  },
   242	  {
   243	    "locator": "2.1.15",
   244	    "type": "operative",
   245	    "source_text": "платежная система – совокупность организаций, взаимодействующих по правилам платежной системы в целях осуществления перевода денежных средств;",
   246	    "source_excerpt": "платежная система – совокупность организаций, взаимодействующих по правилам платежной системы в целях осуществления перевода денежных средств;",
   247	    "source_locator": "2.1.15",
   248	    "line_start": 26,
   249	    "line_end": 26,
   250	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   251	    "final_allowed": true,
   252	    "evidence_only": false
   253	  },
   254	  {
   255	    "locator": "2.1.16",
   256	    "type": "operative",
   257	    "source_text": "покупатель - физическое лицо, осуществляющее оплату товара/услуги в ТСТ при помощи карты, а также лицо, осуществляющее возврат/отказ от товара/услуги в ТСТ;",
   258	    "source_excerpt": "покупатель - физическое лицо, осуществляющее оплату товара/услуги в ТСТ при помощи карты, а также лицо, осуществляющее возврат/отказ от товара/услуги в ТСТ;",
   259	    "source_locator": "2.1.16",
   260	    "line_start": 27,
   261	    "line_end": 27,
   262	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   263	    "final_allowed": true,
   264	    "evidence_only": false
   265	  },
   266	  {
   267	    "locator": "2.1.17",
   268	    "type": "operative",
   269	    "source_text": "повторяющиеся платежи – платежи в оплату товаров/услуг, осуществляемые регулярно в течение определенного периода времени;",
   270	    "source_excerpt": "повторяющиеся платежи – платежи в оплату товаров/услуг, осуществляемые регулярно в течение определенного периода времени;",
   271	    "source_locator": "2.1.17",
   272	    "line_start": 28,
   273	    "line_end": 28,
   274	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   275	    "final_allowed": true,
   276	    "evidence_only": false
   277	  },
   278	  {
   279	    "locator": "2.1.18",
   280	    "type": "operative",
   281	    "source_text": "предавторизация - операция по резервированию денежных средств на карте для последующей оплаты, требующая подтверждения со стороны Заказчика/ТСТ с указанием суммы списания;",
   282	    "source_excerpt": "предавторизация - операция по резервированию денежных средств на карте для последующей оплаты, требующая подтверждения со стороны Заказчика/ТСТ с указанием суммы списания;",
   283	    "source_locator": "2.1.18",
   284	    "line_start": 29,
   285	    "line_end": 29,
   286	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   287	    "final_allowed": true,
   288	    "evidence_only": false
   289	  },
   290	  {
   291	    "locator": "2.1.19",
   292	    "type": "operative",
   293	    "source_text": "предприятие (Заказчик) – торгово-сервисное предприятие (ТСП): юридическое лицо/ индивидуальный предприниматель (ИП), принимающие карты в качестве средства оплаты товаров/услуг на основании условий настоящего контракта. Заказчик может иметь одну торгово-сервисную точку или сеть из двух и более торгово-сервисных точек; расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   294	    "source_excerpt": "предприятие (Заказчик) – торгово-сервисное предприятие (ТСП): юридическое лицо/ индивидуальный предприниматель (ИП), принимающие карты в качестве средства оплаты товаров/услуг на основании условий настоящего контракта. Заказчик может иметь ",
   295	    "source_locator": "2.1.19",
   296	    "line_start": 30,
   297	    "line_end": 31,
   298	    "section_context": "Идентификационный код закупки 251231702678823170100100060016619244.",
   299	    "final_allowed": true,
   300	    "evidence_only": false
   301	  },
   302	  {
   303	    "locator": "2.1.20",
   304	    "type": "operative",
   305	    "source_text": "рабочий день – день, который не признается в соответствие с законодательством Российской Федерации выходным и (или) нерабочим праздничным днем;",
   306	    "source_excerpt": "рабочий день – день, который не признается в соответствие с законодательством Российской Федерации выходным и (или) нерабочим праздничным днем;",
   307	    "source_locator": "2.1.20",
   308	    "line_start": 32,
   309	    "line_end": 32,
   310	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   311	    "final_allowed": true,
   312	    "evidence_only": false
   313	  },
   314	  {
   315	    "locator": "2.1.21",
   316	    "type": "operative",
   317	    "source_text": "реверсивная транзакция – финансово-информационное сообщение, которое банк-эквайрер направляет в платежную систему для отмены ранее направленной транзакции (например, в случае ошибочного предъявления транзакции). В результате обработки этого сообщения происходит списание денежных средств со счета банка-эквайрера (со счета Заказчика) и зачисление их на счет банка-эмитента (на счет карты покупателя);",
   318	    "source_excerpt": "реверсивная транзакция – финансово-информационное сообщение, которое банк-эквайрер направляет в платежную систему для отмены ранее направленной транзакции (например, в случае ошибочного предъявления транзакции). В результате обработки этого",
   319	    "source_locator": "2.1.21",
   320	    "line_start": 33,
   321	    "line_end": 33,
   322	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   323	    "final_allowed": true,
   324	    "evidence_only": false
   325	  },
   326	  {
   327	    "locator": "2.1.22",
   328	    "type": "operative",
   329	    "source_text": "сводный чек электронного терминала – бумажный отчет, распечатываемый электронным терминалом и содержащий итоговую информацию по операциям за определенный промежуток времени;",
   330	    "source_excerpt": "сводный чек электронного терминала – бумажный отчет, распечатываемый электронным терминалом и содержащий итоговую информацию по операциям за определенный промежуток времени;",
   331	    "source_locator": "2.1.22",
   332	    "line_start": 34,
   333	    "line_end": 34,
   334	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   335	    "final_allowed": true,
   336	    "evidence_only": false
   337	  },
   338	  {
   339	    "locator": "2.1.23",
   340	    "type": "operative",
   341	    "source_text": "тарифы банка– стоимость услуг банка за выполнение расчетов по операциям оплаты в виде процента от суммы каждой операции оплаты и размера платы за сервисное обслуживание;",
   342	    "source_excerpt": "тарифы банка– стоимость услуг банка за выполнение расчетов по операциям оплаты в виде процента от суммы каждой операции оплаты и размера платы за сервисное обслуживание;",
   343	    "source_locator": "2.1.23",
   344	    "line_start": 35,
   345	    "line_end": 35,
   346	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   347	    "final_allowed": true,
   348	    "evidence_only": false
   349	  },
   350	  {
   351	    "locator": "2.1.24",
   352	    "type": "operative",
   353	    "source_text": "товар/услуга – товар, работа, услуга, результат интеллектуальной деятельности, реализуемые Заказчиком в ТСТ;",
   354	    "source_excerpt": "товар/услуга – товар, работа, услуга, результат интеллектуальной деятельности, реализуемые Заказчиком в ТСТ;",
   355	    "source_locator": "2.1.24",
   356	    "line_start": 36,
   357	    "line_end": 36,
   358	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   359	    "final_allowed": true,
   360	    "evidence_only": false
   361	  },
   362	  {
   363	    "locator": "2.1.25",
   364	    "type": "operative",
   365	    "source_text": "торгово-сервисная точка (ТСТ) – подразделение Заказчика, зарегистрированное банком на основании информации о ТСТ, в котором осуществляется реализация товаров/ услуг покупателям;",
   366	    "source_excerpt": "торгово-сервисная точка (ТСТ) – подразделение Заказчика, зарегистрированное банком на основании информации о ТСТ, в котором осуществляется реализация товаров/ услуг покупателям;",
   367	    "source_locator": "2.1.25",
   368	    "line_start": 37,
   369	    "line_end": 37,
   370	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   371	    "final_allowed": true,
   372	    "evidence_only": false
   373	  },
   374	  {
   375	    "locator": "2.1.26",
   376	    "type": "operative",
   377	    "source_text": "торговый эквайринг – осуществление банком-эквайрером расчетов с предприятиями, осуществляющими реализацию товаров/услуг с использованием карт в ТСТ; транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   378	    "source_excerpt": "торговый эквайринг – осуществление банком-эквайрером расчетов с предприятиями, осуществляющими реализацию товаров/услуг с использованием карт в ТСТ; транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   379	    "source_locator": "2.1.26",
   380	    "line_start": 38,
   381	    "line_end": 39,
   382	    "section_context": "расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;",
   383	    "final_allowed": true,
   384	    "evidence_only": false
   385	  },
   386	  {
   387	    "locator": "2.1.27",
   388	    "type": "operative",
   389	    "source_text": "чек электронного терминала (чек) – документ по операции, распечатываемый электронным терминалом и содержащий информацию о проведенной операции;",
   390	    "source_excerpt": "чек электронного терминала (чек) – документ по операции, распечатываемый электронным терминалом и содержащий информацию о проведенной операции;",
   391	    "source_locator": "2.1.27",
   392	    "line_start": 40,
   393	    "line_end": 40,
   394	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   395	    "final_allowed": true,
   396	    "evidence_only": false
   397	  },
   398	  {
   399	    "locator": "2.1.28",
   400	    "type": "operative",
   401	    "source_text": "электронная сверка итогов – процедура передачи от электронного терминала исполнителю расчетной информации об операциях за определенный период;",
   402	    "source_excerpt": "электронная сверка итогов – процедура передачи от электронного терминала исполнителю расчетной информации об операциях за определенный период;",
   403	    "source_locator": "2.1.28",
   404	    "line_start": 41,
   405	    "line_end": 41,
   406	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   407	    "final_allowed": true,
   408	    "evidence_only": false
   409	  },
   410	  {
   411	    "locator": "2.2",
   412	    "type": "operative",
   413	    "source_text": "электронный терминал – электронное программно-техническое устройство исполнителя (в том числе дополнительное оборудование и/или специальное программное обеспечение ККТ), позволяющее осуществлять прием карт в ТСТ для проведения операций. Электронный терминал может включать в себя в том числе мобильный терминал (mPOS), биометрический терминал. Электронный терминал предоставляется исполнителем и устанавливается на срок действия контракта. Электронный терминал предназначен и может использоваться только в целях исполнения контракта.",
   414	    "source_excerpt": "электронный терминал – электронное программно-техническое устройство исполнителя (в том числе дополнительное оборудование и/или специальное программное обеспечение ККТ), позволяющее осуществлять прием карт в ТСТ для проведения операций. Эле",
   415	    "source_locator": "2.2",
   416	    "line_start": 42,
   417	    "line_end": 42,
   418	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   419	    "final_allowed": true,
   420	    "evidence_only": false
   421	  },
   422	  {
   423	    "locator": "2.3",
   424	    "type": "operative",
   425	    "source_text": "Банк и Заказчик в рамках настоящего Контракта обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Контрактом:",
   426	    "source_excerpt": "Банк и Заказчик в рамках настоящего Контракта обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Контрактом:",
   427	    "source_locator": "2.3",
   428	    "line_start": 43,
   429	    "line_end": 43,
   430	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   431	    "final_allowed": true,
   432	    "evidence_only": false
   433	  },
   434	  {
   435	    "locator": "2.3.1",
   436	    "type": "operative",
   437	    "source_text": "с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Заказчиком в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Заказчика за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Контракте, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;",
   438	    "source_excerpt": "с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Заказчиком в Заявлении Заказчика на проведение расчетов по операциям оплаты товар",
   439	    "source_locator": "2.3.1",
   440	    "line_start": 44,
   441	    "line_end": 44,
   442	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   443	    "final_allowed": true,
   444	    "evidence_only": false
   445	  },
   446	  {
   447	    "locator": "2.3.2",
   448	    "type": "operative",
   449	    "source_text": "посредством системы ДБО или аналогичных систем Банка;",
   450	    "source_excerpt": "посредством системы ДБО или аналогичных систем Банка;",
   451	    "source_locator": "2.3.2",
   452	    "line_start": 45,
   453	    "line_end": 45,
   454	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   455	    "final_allowed": true,
   456	    "evidence_only": false
   457	  },
   458	  {
   459	    "locator": "2.3.3",
   460	    "type": "operative",
   461	    "source_text": "путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   462	    "source_excerpt": "путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   463	    "source_locator": "2.3.3",
   464	    "line_start": 46,
   465	    "line_end": 46,
   466	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   467	    "final_allowed": true,
   468	    "evidence_only": false
   469	  },
   470	  {
   471	    "locator": "2.3.4",
   472	    "type": "operative",
   473	    "source_text": "путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   474	    "source_excerpt": "путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   475	    "source_locator": "2.3.4",
   476	    "line_start": 47,
   477	    "line_end": 47,
   478	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   479	    "final_allowed": true,
   480	    "evidence_only": false
   481	  },
   482	  {
   483	    "locator": "2.3.5",
   484	    "type": "operative",
   485	    "source_text": "путем обмена электронными документами посредством автоматизированной системы _________________. В этом случае документы подписываются усиленной квалифицированной электронной подписью (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   486	    "source_excerpt": "путем обмена электронными документами посредством автоматизированной системы _________________. В этом случае документы подписываются усиленной квалифицированной электронной подписью (далее – УКЭП) Сторон и признаются равнозначными документ",
   487	    "source_locator": "2.3.5",
   488	    "line_start": 48,
   489	    "line_end": 48,
   490	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   491	    "final_allowed": true,
   492	    "evidence_only": false
   493	  },
   494	  {
   495	    "locator": "2.3.6",
   496	    "type": "operative",
   497	    "source_text": "путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   498	    "source_excerpt": "путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактно",
   499	    "source_locator": "2.3.6",
   500	    "line_start": 49,
   501	    "line_end": 49,
   502	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   503	    "final_allowed": true,
   504	    "evidence_only": false
   505	  },
   506	  {
   507	    "locator": "2.3.7",
   508	    "type": "operative",
   509	    "source_text": "через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе. Сторона считается получившей информацию/документ в случае направления способом, указанным в: • п. 2.3.1, п. 2.3.2 Контракта – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно; • п. 2.3.3, п. 2.3.4 Контракта – в дату доставки получающей стороне письма/почтового отправления (заказного письма); • п. 2.3.5. Контракта – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции; • п. 2.3.6. Контракта – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке ; • п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   510	    "source_excerpt": "через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе. Сторона считается получившей информацию/документ в случае направления способом, указанным в: • п. 2.3.",
   511	    "source_locator": "2.3.7",
   512	    "line_start": 50,
   513	    "line_end": 56,
   514	    "section_context": "транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;",
   515	    "final_allowed": true,
   516	    "evidence_only": false
   517	  },
   518	  {
   519	    "locator": "3",
   520	    "type": "operative",
   521	    "source_text": "ЦЕНА КОНТРАКТА",
   522	    "source_excerpt": "ЦЕНА КОНТРАКТА",
   523	    "source_locator": "3",
   524	    "line_start": 57,
   525	    "line_end": 57,
   526	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   527	    "final_allowed": true,
   528	    "evidence_only": false
   529	  },
   530	  {
   531	    "locator": "3.1",
   532	    "type": "operative",
   533	    "source_text": "Максимальное значение цены контракта (стоимость услуг) (далее – цена контракта) составляет 1 900 000,00 рублей (один миллион девятьсот тысяч рублей 00 копеек), в том числе НДС ______________ (в случае если Исполнитель не является плательщиком НДС, указать «НДС не облагается»).",
   534	    "source_excerpt": "Максимальное значение цены контракта (стоимость услуг) (далее – цена контракта) составляет 1 900 000,00 рублей (один миллион девятьсот тысяч рублей 00 копеек), в том числе НДС ______________ (в случае если Исполнитель не является плательщик",
   535	    "source_locator": "3.1",
   536	    "line_start": 58,
   537	    "line_end": 58,
   538	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   539	    "final_allowed": true,
   540	    "evidence_only": false
   541	  },
   542	  {
   543	    "locator": "3.1.1",
   544	    "type": "operative",
   545	    "source_text": "Цена за единицу услуги указана в спецификации (Приложение № 1), являющейся неотъемлемой частью настоящего контракта.",
   546	    "source_excerpt": "Цена за единицу услуги указана в спецификации (Приложение № 1), являющейся неотъемлемой частью настоящего контракта.",
   547	    "source_locator": "3.1.1",
   548	    "line_start": 59,
   549	    "line_end": 59,
   550	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   551	    "final_allowed": true,
   552	    "evidence_only": false
   553	  },
   554	  {
   555	    "locator": "3.2",
   556	    "type": "operative",
   557	    "source_text": "Цена единицы услуги включает в себя расходы Исполнителя, связанные с оказанием услуг Банка за выполнение расчетов с Заказчиком по Операциям оплаты в виде процента от суммы каждой Операции оплаты.",
   558	    "source_excerpt": "Цена единицы услуги включает в себя расходы Исполнителя, связанные с оказанием услуг Банка за выполнение расчетов с Заказчиком по Операциям оплаты в виде процента от суммы каждой Операции оплаты.",
   559	    "source_locator": "3.2",
   560	    "line_start": 60,
   561	    "line_end": 60,
   562	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   563	    "final_allowed": true,
   564	    "evidence_only": false
   565	  },
   566	  {
   567	    "locator": "3.3",
   568	    "type": "operative",
   569	    "source_text": "Положения настоящего Контракта, касающиеся применения цены контракта или начальной максимальной цены Контракта применяются к максимальному значению цены Контракта, указанному в настоящем разделе Контракта, если Федеральным законом №44-ФЗ не установлено иное.",
   570	    "source_excerpt": "Положения настоящего Контракта, касающиеся применения цены контракта или начальной максимальной цены Контракта применяются к максимальному значению цены Контракта, указанному в настоящем разделе Контракта, если Федеральным законом №44-ФЗ не",
   571	    "source_locator": "3.3",
   572	    "line_start": 61,
   573	    "line_end": 61,
   574	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   575	    "final_allowed": true,
   576	    "evidence_only": false
   577	  },
   578	  {
   579	    "locator": "4",
   580	    "type": "operative",
   581	    "source_text": "СРОКИ, УСЛОВИЯ ОКАЗАНИЯ УСЛУГ, ПОРЯДОК ОПЛАТЫ",
   582	    "source_excerpt": "СРОКИ, УСЛОВИЯ ОКАЗАНИЯ УСЛУГ, ПОРЯДОК ОПЛАТЫ",
   583	    "source_locator": "4",
   584	    "line_start": 62,
   585	    "line_end": 62,
   586	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   587	    "final_allowed": true,
   588	    "evidence_only": false
   589	  },
   590	  {
   591	    "locator": "4.1",
   592	    "type": "operative",
   593	    "source_text": "Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее.",
   594	    "source_excerpt": "Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ране",
   595	    "source_locator": "4.1",
   596	    "line_start": 63,
   597	    "line_end": 63,
   598	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   599	    "final_allowed": true,
   600	    "evidence_only": false
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
    16	- `/outputs/working/contract_locator_registry.json`
    17	- `/outputs/working/contract_product_profile.json`
    18	- `/outputs/working/coverage_ledger.json`
    19	
    20	`clause_index.json` is a source map. It contains source ids and text, but no
    21	final legal status.
    22	
    23	`contract_locator_registry.json` is the canonical source of contract locators.
    24	Every final `contract_id` must be a registry `locator` with
    25	`final_allowed = true`. Real appendix/table rows may be final locators when
    26	they contain independent legal content and are source-derived registry rows.
    27	Appendix starts, table headings, and unnumbered source anchors may be registry
    28	rows with `evidence_only = true`; cite them only in `evidence_locators`, never
    29	in `contract_ids`, `candidate_contract_ids`, `atomic_links[].contract_id`,
    30	`unmatched_contract[].contract_id`, `rejected_contract_ids[].contract_id`, or
    31	`unmatched_matrix[].rejected_candidates[].contract_id`.
    32	
    33	`legal_propositions.json` is the legal evidence ledger. It must contain:
    34	
    35	```json
    36	{
    37	  "matrix": [
    38	    {
    39	      "id": "<matrix number>",
    40	      "source_text": "<matrix enriched/source text>",
    41	      "source_excerpt": "<short quote>",
    42	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    43	      "materiality": "evaluable|not_material|heading|needs_source_review",
    44	      "protected_party": "<party protected by the rule>",
    45	      "bound_party": "<party bound by the rule>",
    46	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    47	      "legal_object": "<regulated object>",
    48	      "trigger": "<event/condition>",
    49	      "deadline": "<deadline if any>",
    50	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    51	      "procedure_channel": "<procedure/channel if any>",
    52	      "liability_remedy": "<liability/remedy if any>",
    53	      "scope_options": ["<scope option>"],
    54	      "consequence": "<legal consequence>",
    55	      "applicability_filters": {}
    56	    }
    57	  ],
    58	  "contract": [
    59	    {
    60	      "id": "<printed contract locator>",
    61	      "source_text": "<contract clause text>",
    62	      "source_excerpt": "<short quote>",
    63	      "type": "operative|definition|heading|parent_framework|appendix|table|technical",
    64	      "materiality": "evaluable|not_material|heading|needs_source_review",
    65	      "protected_party": "<party protected by the rule>",
    66	      "bound_party": "<party bound by the rule>",
    67	      "right_or_obligation": "<right/duty/remedy/prohibition>",
    68	      "legal_object": "<regulated object>",
    69	      "trigger": "<event/condition>",
    70	      "deadline": "<deadline if any>",
    71	      "amount_formula_cap": "<amount/formula/cap/penalty if any>",
    72	      "procedure_channel": "<procedure/channel if any>",
    73	      "liability_remedy": "<liability/remedy if any>",
    74	      "scope_options": ["<scope option>"],
    75	      "consequence": "<legal consequence>"
    76	    }
    77	  ]
    78	}
    79	```
    80	
    81	Rows marked `needs_source_review` are not complete. Resolve them before final
    82	status if they can affect a link, missing item, or contract-only finding.
    83	
    84	## Final JSON Shape
    85	
    86	```json
    87	{
    88	  "analysis_profile": {
    89	    "contract_product_profile": {
    90	      "product": ["<selected product/channel>"],
    91	      "lot": "<44_fz|223_fz|commercial|common|unknown>",
    92	      "terminal": ["<selected terminal/payment device>"],
    93	      "payment_method": ["<selected payment method>"],
    94	      "legal_regime": "<44_fz|223_fz|commercial|unknown>"
    95	    },
    96	    "source_preflight": {
    97	      "contract_numbering_valid": true,
    98	      "notes": []
    99	    }
   100	  },
   101	  "links": [
   102	    {
   103	      "matrix_ids": ["<matrix id>"],
   104	      "contract_ids": ["<contract locator>"],
   105	      "relationship": "aligned|deviation",
   106	      "legal_topic": "<short legal topic>",
   107	      "matrix_standard": "<bank standard requirement group>",
   108	      "contract_position": "<counterparty contract position group>",
   109	      "matrix_evidence": "<short matrix quote>",
   110	      "contract_evidence": "<short contract quote>",
   111	      "evidence_locators": ["<registry locator used only as supporting evidence>"],
   112	      "status_reason": "<group-level reason>",
   113	      "risk_level": "none|low|medium|high",
   114	      "covered_elements": ["<matrix provisions covered by contract candidates>"],
   115	      "uncovered_elements": ["<matrix provisions still missing/changed/weak>"],
   116	      "candidate_contract_ids": ["<accepted candidate contract locator>"],
   117	      "rejected_contract_ids": [
   118	        {
   119	          "contract_id": "<reviewed non-candidate locator>",
   120	          "reason": "<why it is not a true analogue or cannot cure the gap>"
   121	        }
   122	      ],
   123	      "candidate_search_exhausted": true,
   124	      "search_scope": "full_contract|targeted_domain",
   125	      "discrepancies": [
   126	        {
   127	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
   128	          "description": "<material difference>",
   129	          "risk": "<why this matters for the Bank>"
   130	        }
   131	      ]
   132	    }
   133	  ],
   134	  "atomic_links": [
   135	    {
   136	      "matrix_id": "<one matrix id>",
   137	      "contract_id": "<one contract locator>",
   138	      "relationship": "aligned|deviation",
   139	      "link_index": 0,
   140	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
   141	      "coverage": "<what this contract locator contributes to the group>"
   142	    }
   143	  ],
   144	  "unmatched_matrix": [
   145	    {
   146	      "matrix_id": "<matrix id>",
   147	      "requirement": "<missing bank standard requirement>",
   148	      "source_evidence": "<short matrix quote>",
   149	      "evidence_locators": ["<registry locator used only as supporting evidence>"],
   150	      "status": "missing_in_contract",
   151	      "required_type": "mandatory|optional|unknown",
   152	      "applicability": "applicable|conditional|unknown",
   153	      "risk_level": "low|medium|high",
   154	      "risk": "<risk of omission>",
   155	      "covered_elements": ["<matrix provisions covered by weak/partial context, if any>"],
   156	      "uncovered_elements": ["<matrix provisions not covered by any true analogue>"],
   157	      "candidate_contract_ids": [],
   158	      "candidate_search_exhausted": true,
   159	      "search_scope": "full_contract",
   160	      "rejected_candidates": [
   161	        {
   162	          "contract_id": "<weak candidate considered>",
   163	          "reason": "<why it is not a true analogue>"
   164	        }
   165	      ]
   166	    }
   167	  ],
   168	  "unmatched_contract": [
   169	    {
   170	      "contract_id": "<contract locator>",
   171	      "contract_position": "<extra legally significant contract term>",
   172	      "source_evidence": "<short contract quote>",
   173	      "evidence_locators": ["<registry locator used only as supporting evidence>"],
   174	      "status": "extra_in_contract",
   175	      "risk_level": "low|medium|high",
   176	      "risk": "<risk or impact for the Bank>",
   177	      "materiality_reason": "<why this has independent legal effect>"
   178	    }
   179	  ],
   180	  "coverage_ledger": {
   181	    "matrix": [
   182	      {
   183	        "matrix_id": "<matrix id>",
   184	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
   185	        "link_indices": [0],
   186	        "reason": "<short closure reason>"
   187	      }
   188	    ],
   189	    "contract": [
   190	      {
   191	        "contract_id": "<contract locator>",
   192	        "closure": "linked|extra_in_contract|not_material",
   193	        "link_indices": [0],
   194	        "reason": "<short closure reason>"
   195	      }
   196	    ]
   197	  },
   198	  "summary": {
   199	    "aligned_count": 0,
   200	    "deviation_count": 0,
   201	    "missing_in_contract_count": 0,
   202	    "extra_in_contract_count": 0
   203	  }
   204	}
   205	```
   206	
   207	## JSON Rules
   208	
   209	- `links` are group-level legal findings. One status applies to the whole
   210	  many-to-many group.
   211	- `atomic_links` are traceability rows only. They inherit the group
   212	  `relationship`; do not invent pair-level final statuses.
   213	- `contract_ids` contain clauses that provide material coverage for the focused
   214	  group. Each listed id must correspond to at least one named item in
   215	  `covered_elements`, `uncovered_elements`, `discrepancies`, or
   216	  `status_reason`. Background clauses can be cited in reasoning, but should not
   217	  become final candidates unless they affect coverage or status.
   218	- `links` are reasoning-backed legal findings. Do not generate them from
   219	  keyword overlap, token overlap, section proximity, vector similarity, regular
   220	  expressions, or match scores. Phrases such as `auto-matched`, `score`,
   221	  `threshold`, or `keyword overlap` are not valid status reasons.
   222	- A link group must be a focused legal package. If many same-topic or
   223	  same-parent clauses are grouped together, each clause must contribute a named
   224	  right, duty, trigger, deadline, amount, procedure, liability term, or
   225	  consequence to the same legal result. Otherwise split the group or reject the
   226	  extra clauses.
   227	- Final contract ids are closed-class values: they must come from
   228	  `/outputs/working/contract_locator_registry.json` with `final_allowed = true`.
   229	  Do not create corrected, translated, internal, parenthetical, semantic-suffix,
   230	  or derived appendix ids. A source-derived appendix/table row may be final only
   231	  when the registry row itself is final-allowed and contains an operative
   232	  amount, fee, deadline, product scope, procedure, liability term, or other
   233	  standalone legal condition.
   234	- `evidence_locators` are for source anchors that support the evidence but are
   235	  not independent final contract clauses. Evidence-only locators do not count
   236	  as coverage candidates and cannot cure a missing or deviation finding.
   237	- `coverage_ledger` is derived from final `links`, `unmatched_matrix`, and
   238	  `unmatched_contract`, plus profile-based `out_of_scope` / `not_applicable`
   239	  matrix closures. Do not use it to invent final conclusions.
   240	- Merge/finalizer helpers may normalize explicit findings, but they must not
   241	  infer `missing_in_contract` only because a matrix id has no link. An
   242	  applicable matrix id without an explicit link, explicit missing row, or
   243	  profile-based closure is an incomplete run.
   244	- `out_of_scope` and `not_applicable` matrix closures mean the requirement is
   245	  not a risk for the current product, lot, terminal, payment method, or legal
   246	  regime. They stay in `coverage_ledger.matrix` only and do not appear in
   247	  final `unmatched_matrix`.
   248	- `unmatched_contract` contains only legally significant `extra_in_contract`
   249	  rows. Non-material rows stay in `coverage_ledger.contract`.
   250	- `relationship = aligned` requires empty `discrepancies`, empty
   251	  `uncovered_elements`, `risk_level = none`, and text-grounded confirmation
   252	  that the contract package preserves the matrix legal result.
   253	- `relationship = deviation` requires at least one discrepancy with `type`,
   254	  `description`, and `risk`; `candidate_search_exhausted = true`; and
   255	  `search_scope = full_contract`.
   256	- Missing mandatory applicable requirements should normally be `high` risk.
   257	  Missing optional applicable requirements should normally be `low` or
   258	  conditional risk.
   259	- `unmatched_matrix` requires `candidate_search_exhausted = true` and
   260	  `search_scope = full_contract`; it is invalid to mark an applicable matrix
   261	  item missing before completing a documented legal sweep through the source
   262	  index. The sweep may use the ledger to find plausible clauses, but acceptance
   263	  or rejection must be based on legal object, party, trigger, procedure,
   264	  consequence, and source text. Search exhaustion means the agent reviewed and
   265	  rejected weak candidates; it does not mean adding all nearby clauses to the
   266	  final group.
   267	- All final ids must be visible in source files. Do not use corrected,
   268	  inferred, translated, parenthetical, or internal ids.
   269	- All final ids must also be registry-final-allowed. A visible appendix heading
   270	  is not a final `contract_id` unless the registry marks it `final_allowed`.
   271	- Weak candidates do not appear in final `links`; use
   272	  `unmatched_matrix[].rejected_candidates`.
   273	- Focused package recall is required for final links: if a child/detail row is
   274	  a true analogue, include its operative parent/root only when that parent
   275	  carries the same right, duty, procedure, basis, or consequence. Do not include
   276	  sibling children, headings, adjacent topic clauses, or evidence-only anchors
   277	  unless they cover a named material element of the same group.
   278	- Matrix missing findings require strict-link audit: if only broad thematic
   279	  candidates exist, keep them in `rejected_candidates` and leave the matrix item
   280	  in `unmatched_matrix`.
   281	- Status gaps are contained to the focused group where the gap is material. A
   282	  missing placeholder, deadline, channel, consent, amount, or procedure must not
   283	  downgrade sibling matrix ids unless that element belongs to those siblings.
   284	
   285	## Excel Output
   286	
   287	Create `/outputs/discrepancy_analysis.xlsx` from the JSON with two sheets.
   288	
   289	Sheet 1: `Contract-Matrix`
   290	
   291	Columns:
   292	
   293	1. `contract_id`
   294	2. `contract_summary`
   295	3. `matrix_ids`
   296	4. `status`
   297	5. `risk_level`
   298	6. `comment`
   299	
   300	Rules:
   301	
   302	- one row per group-level contract-to-matrix finding;
   303	- `matrix_ids` contains the full matrix id set for the group;
   304	- status is `aligned`, `deviation`, or `extra_in_contract`;
   305	- contract-only extras have blank `matrix_ids`.
   306	
   307	Sheet 2: `Only in Matrix`
   308	
   309	Columns:
   310	
   311	1. `matrix_id`
   312	2. `requirement`
   313	3. `required_type`
   314	4. `risk_level`
   315	5. `comment`
   316	
   317	Rules:
   318	
   319	- one row per final `unmatched_matrix` item;
   320	- include optional applicable missing as low/conditional risk;
   321	- do not include out-of-scope / not-applicable requirements;
   322	- do not include non-evaluable headings or purely technical rows.
   323	
   324	## Bad Output Patterns
   325	
   326	Do not output:
   327	
   328	- multiple competing final JSON files;
   329	- pair-level final statuses as the primary answer;
   330	- `deviation` for unselected slash alternatives;
   331	- `deviation` for heading/title/label changes alone;
   332	- final `unmatched_contract` rows for definitions without legal effect;
   333	- final `unmatched_matrix` rows for out-of-scope or not-applicable matrix
   334	  requirements;
   335	- final ids that exist only in helper scripts or working ledgers;
   336	- final `contract_id` values that are evidence-only registry locators;
   337	- evidence-only registry locators used as `rejected_candidates[].contract_id` or
   338	  `rejected_contract_ids[].contract_id`; keep them in `evidence_locators`
   339	  instead;
   340	- final links, statuses, or missing findings generated from legal match scores,
   341	  keyword overlap, token overlap, section proximity, vector similarity, or
   342	  regular-expression rules;
   343	- `status_reason` values such as `Auto-matched with score ...`,
   344	  `keyword match`, `high similarity`, or `same section`;
   345	- overbroad same-topic link groups where most `contract_ids` do not contribute
   346	  a named material element to the same legal result;
   347	- overbroad same-parent groups where one child gap changes the status of
   348	  independent sibling requirements;
   349	- synthetic appendix ids such as `Приложение_1_п5`,
   350	  `Приложение_1_п5_комиссия`, or `Appendix_1_fee`;
   351	- final appendix/table locators invented from semantics instead of copied from
   352	  `contract_locator_registry.json`;
   353	- `extra_in_contract` with empty risk;
   354	- `aligned` with non-empty discrepancies;
   355	- `aligned` with non-empty `uncovered_elements`;
   356	- `deviation` or `missing_in_contract` with `candidate_search_exhausted = false`;
   357	- `deviation` or `missing_in_contract` with `search_scope = targeted_domain`
   358	  or `not_completed`;
   359	- `missing_in_contract` where a weak candidate is silently treated as a link;
   360	- `not_material` closure explained only as `No final legal finding produced`,
   361	  `not analyzed`, or another non-legal placeholder reason;
   362	- implicit `missing_in_contract` rows produced by a script without an explicit
   363	  agent finding and documented rejected/covered/uncovered elements;
   364	- final conclusions based only on extracted fields without source-text evidence.
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
   101	Matrix or contract requires a filled penalty, fee, account, deadline, appendix,
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
   201	Result: apply the product profile first. Generic capability is not enough for a
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
   301	Matrix has one requirement for confirming personal-data authority within a
   302	deadline and another requirement for obtaining consent to process personal data.
   303	Contract has consent language but no deadline for authority confirmation.
   304	
   305	Result: the missing deadline affects only the confirmation requirement. It does
   306	not downgrade the separate consent requirement if consent is preserved.
   307	
   308	### weak-qr-advertising-rejected
   309	
   310	Matrix requires providing a named QR payment code or product-specific QR
   311	operation. Contract contains advertising materials, a terminal capability, or a
   312	generic statement that QR display is technically possible.
   313	
   314	Result: reject the contract text as weak context unless it imposes the same
   315	operational duty for the named payment product.
   316	
   317	### generic-check-rejected-for-issuer-verification
   318	
   319	Matrix gives the Bank a special right to verify an operation through an issuer,
   320	payment system, or named verification source. Contract only allows a general
   321	document request or general inspection.
   322	
   323	Result: no final link. Record the general clause as rejected context; it cannot
   324	cure the missing special verification right.
   325	
   326	### generic-liability-rejected-for-bank-exemption
   327	
   328	Matrix exempts the Bank from liability for transfer delays caused by a payment
   329	system, correspondent bank, third party, or other non-Bank reason. Contract has
   330	only a general liability rule based on fault.
   331	
   332	Result: no final link unless the exemption or equivalent risk allocation is
   333	present. General fault liability cannot satisfy the Bank-specific exemption.
   334	
   335	### contract-only-material-vs-not-material
   336	
   337	Contract gives the customer an independent right to control performance,
   338	reject acceptance, withhold payment, demand defect correction, terminate
   339	unilaterally, impose penalties, require force-majeure proof, or ban material
   340	condition changes. Matrix has no analogue.
   341	
   342	Result: `extra_in_contract`. Headings, requisites, signatures, blank forms, and
   343	definitions without independent legal effect stay out of the final report.
   344	
   345	### root-plus-child-without-broad-grouping
   346	
   347	Contract root clause creates a right to withhold money. Child clauses list
   348	separate grounds: missing documents, overpayment, penalties, and third-party
   349	claims. Matrix separately regulates only one of those grounds.
   350	
   351	Result: include the root and the relevant child for that focused requirement.
   352	Do not link every child or combine all matrix withholding rows into one broad
   353	group unless they are one indivisible legal result.
AI: Now let me read the matrix file for the batch range (5.1.1.6 - 7.17) and the contract text, plus the existing working files.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 100}, 'id': 'call_00_nQRT0h6QNRmgEhs8jVRR4894', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_01_JIezHxjDPYpeZbuMa6f39668', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 100}, 'id': 'call_02_SWqdG5v2BYaLQLsk4G098454', 'type': 'tool_call'}]
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
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos"],
     5	  "payment_method": ["cards", "qr"],
     6	  "legal_regime": "44_fz",
     7	  "notes": "Contract is a 44-FZ public procurement for trade acquiring services with POS terminals at physical TST locations. QR-code display capability mentioned in Technical Assignment. No internet acquiring, no SberPay, no smart terminals explicitly in scope. Terminal type is standard POS (Электронные терминалы)."
     8	}
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
AI: Let me now find the matrix entries for the batch range 5.1.1.6 - 7.17. I need to search for these specific matrix numbers.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\n# Find all matrix numbers\nnumbers = [m[\'number\'] for m in matrix]\n# Find indices for range 5.1.1.6 to 7.17\nfor i, n in enumerate(numbers):\n    print(f\'{i}: {n}\')\n"'}, 'id': 'call_00_VhsJGzrULS8FlTHriVJp6347', 'type': 'tool_call'}]
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
AI: Now I can see the batch range: indices 70 (5.1.1.6) through 147 (7.17). Let me set up my task list and start reading the matrix entries and contract text for this range.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read all matrix entries 5.1.1.6 through 7.17 from inputs/matrix.json', 'status': 'in_progress'}, {'content': 'Read contract text for relevant sections (clauses 5-7 and related)', 'status': 'pending'}, {'content': 'Read existing legal_propositions.json for matrix and contract entries in range', 'status': 'pending'}, {'content': 'Read existing coverage_ledger.json and previous batch outputs for context', 'status': 'pending'}, {'content': 'Perform legal comparison for each matrix id in batch range', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, and coverage_ledger fragments', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Return final fragment', 'status': 'pending'}]}, 'id': 'call_00_kZSBf5oQWihbiMPm4wxf1559', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read all matrix entries 5.1.1.6 through 7.17 from inputs/matrix.json', 'status': 'in_progress'}, {'content': 'Read contract text for relevant sections (clauses 5-7 and related)', 'status': 'pending'}, {'content': 'Read existing legal_propositions.json for matrix and contract entries in range', 'status': 'pending'}, {'content': 'Read existing coverage_ledger.json and previous batch outputs for context', 'status': 'pending'}, {'content': 'Perform legal comparison for each matrix id in batch range', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, and coverage_ledger fragments', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Return final fragment', 'status': 'pending'}]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\n# Extract entries from index 70 (5.1.1.6) to 147 (7.17)\nbatch = matrix[70:148]\nfor m in batch:\n    print(f\'=== {m[\\"number\\"]} ===\')\n    print(f\'required_type: {m[\\"required_type\\"]}\')\n    print(f\'main_idea: {m[\\"main_idea\\"]}\')\n    print(f\'only_for_product: {m[\\"only_for_product\\"]}\')\n    print(f\'only_for_lot: {m[\\"only_for_lot\\"]}\')\n    print(f\'only_for_terminal: {m[\\"only_for_terminal\\"]}\')\n    print(f\'payment_method: {m[\\"payment_method\\"]}\')\n    print(f\'topics: {m[\\"topics\\"]}\')\n    print(f\'enriched_text: {m[\\"enriched_text\\"][:300]}...\')\n    print()\n" 2>&1 | head -500'}, 'id': 'call_00_rEbey41V4Y5ytMsdSkMr7614', 'type': 'tool_call'}]
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
[stderr] with open('inputs/matrix.json', 'r') as f:
[stderr]     matrix = json.load(f)
[stderr] # Extract entries from index 70 (5.1.1.6) to 147 (7.17)
[stderr] batch = matrix[70:148]
[stderr] for m in batch:
[stderr]     print(f'=== {m[\"number\"]} ===')
[stderr]     print(f'required_type: {m[\"required_type\"]}')
[stderr]     print(f'main_idea: {m[\"main_idea\"]}')
[stderr]     print(f'only_for_product: {m[\"only_for_product\"]}')
[stderr]     print(f'only_for_lot: {m[\"only_for_lot\"]}')
[stderr]     print(f'only_for_terminal: {m[\"only_for_terminal\"]}')
[stderr]     print(f'payment_method: {m[\"payment_method\"]}')
[stderr]     print(f'topics: {m[\"topics\"]}')
[stderr]     print(f'enriched_text: {m[\"enriched_text\"][:300]}...')
[stderr]     print()
[stderr] " 2>&1 | head -500
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
AI: [{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\') as f:\n    matrix = json.load(f)\nbatch = matrix[70:148]\nfor m in batch:\n    print(f\'=== {m[\\"number\\"]} ===\')\n    print(f\'required_type: {m[\\"required_type\\"]}\')\n    print(f\'main_idea: {m[\\"main_idea\\"]}\')\n    print(f\'only_for_product: {m[\\"only_for_product\\"]}\')\n    print(f\'only_for_lot: {m[\\"only_for_lot\\"]}\')\n    print(f\'only_for_terminal: {m[\\"only_for_terminal\\"]}\')\n    print(f\'payment_method: {m[\\"payment_method\\"]}\')\n    print(f\'topics: {m[\\"topics\\"]}\')\n    et = m[\'enriched_text\']\n    print(f\'enriched_text: {et[:400]}\')\n    print()\n"'}, 'id': 'call_00_CTUumqF1src0LlRWT1u19980', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 7
[stderr]     print(f'=== {m[" number\]}
[stderr]                    ^
[stderr] SyntaxError: unterminated string literal (detected at line 7)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python -c "import json; f=open(\'/inputs/matrix.json\',\'r\'); matrix=json.load(f); f.close(); batch=matrix[70:148]; [print(\'===\', m[\'number\'], \'===\', chr(10), \'required_type:\', m[\'required_type\'], chr(10), \'main_idea:\', m[\'main_idea\'], chr(10), \'only_for_product:\', m[\'only_for_product\'], chr(10), \'only_for_lot:\', m[\'only_for_lot\'], chr(10), \'only_for_terminal:\', m[\'only_for_terminal\'], chr(10), \'payment_method:\', m[\'payment_method\'], chr(10), \'topics:\', m[\'topics\'], chr(10), \'enriched_text:\', m[\'enriched_text\'][:400], chr(10)) for m in batch]"'}, 'id': 'call_00_rYYGlUZ42Kma6435JRHR5205', 'type': 'tool_call'}]
Tool: Tool result too large, the result of this tool call call_00_rYYGlUZ42Kma6435JRHR5205 was saved in the filesystem at this path: /large_tool_results/call_00_rYYGlUZ42Kma6435JRHR5205

You can read the result from the filesystem by using the read_file tool, but make sure to only read part of the result at a time.

You can do this by specifying an offset and limit in the read_file tool call. For example, to read the first 100 lines, you can use the read_file tool with offset=0 and limit=100.

Here is a preview showing the head and tail of the result (lines of the form `... [N lines truncated] ...` indicate omitted lines in the middle of the content):

     1	=== 5.1.1.6 === 
     2	 required_type: mandatory 
     3	 main_idea: Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ.  
     4	 only_for_product: trade_acquiring 
     5	 only_for_lot: common 
... [786 lines truncated] ...
   792	 topics: ['РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ Р Р¤', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕС‚РІРµС‡Р°РµС‚ Р·Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РЅРѕСЂРјР°С‚РёРІРЅС‹Рј Р°РєС‚Р°Рј Р‘Р°РЅРєР° Р РѕСЃСЃРёРё', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕР±Р»СЋРґР°С‚СЊ РїСЂР°РІРёР»Р° РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РІ С‡Р°СЃС‚Рё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№', 'РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РѕС‚РЅРѕСЃРёС‚РµР»СЊРЅРѕ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№'] 
   793	 enriched_text: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РїСЂРѕРІРµРґРµРЅРЅС‹С… РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ С‚СЂРµР±РѕРІР°РЅРёСЏРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё, РІ С‚РѕРј С‡РёСЃР»Рµ РЅРѕСЂРјР°С‚РёРІРЅС‹С… Р°РєС‚РѕРІ Р‘Р°РЅРєР° Р РѕСЃСЃРёРё, РїСЂР°РІРёР» РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё (РёР»Рё) Р”РѕРіРѕРІРѕСЂР° 
   794	
   795	
   796	[Command succeeded with exit code 0]

AI: The output has encoding issues. Let me read the matrix entries directly from the file.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 700, 'limit': 200}, 'id': 'call_00_4VIabf5hfOL7MsihPY7M6073', 'type': 'tool_call'}]
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
AI: Let me now read the matrix entries for the batch range more efficiently. Let me extract them with a script that handles encoding properly.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json, sys\nsys.stdout.reconfigure(encoding=\'utf-8\')\nwith open(\'/inputs/matrix.json\', \'r\', encoding=\'utf-8\') as f:\n    matrix = json.load(f)\nbatch = matrix[70:148]\nfor m in batch:\n    print(\'MATRIX_ID:\', m[\'number\'])\n    print(\'REQUIRED:\', m[\'required_type\'])\n    print(\'PRODUCT:\', m[\'only_for_product\'])\n    print(\'LOT:\', m[\'only_for_lot\'])\n    print(\'TERMINAL:\', m[\'only_for_terminal\'])\n    print(\'PAYMENT:\', m[\'payment_method\'])\n    print(\'MAIN_IDEA:\', m[\'main_idea\'][:200])\n    print(\'TOPICS:\', \' | \'.join(m[\'topics\']))\n    print(\'ENRICHED:\', m[\'enriched_text\'][:500])\n    print(\'---END---\')\n"'}, 'id': 'call_00_9JMOpc2pKLVe2XSilsh68210', 'type': 'tool_call'}]
Tool: MATRIX_ID: 5.1.1.6
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СѓРґРµСЂР¶РёРІР°С‚СЊ СЃСѓРјРјС‹ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РЈРґРµСЂР¶РёРІР°С‚СЊ РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ, СЃР»РµРґСѓСЋС‰РёРµ СЃСѓРјРјС‹: в†’ РЎСѓРјРјС‹ С€С‚СЂР°С„РѕРІ РІ СЃР»СѓС‡Р°Рµ РЅРµРІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї. 4.2.20.7 Р”РѕРіРѕРІРѕСЂР°.
---END---
MATRIX_ID: 5.1.2
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРёРѕСЃС‚Р°РЅР°РІР»РёРІР°С‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅР°Р»РёС‡РёРё Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ | РџСЂРёРѕСЃС‚Р°РЅРѕРІРєР° РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РґРѕ РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёРµРј
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РІРѕР·РЅРёРєРЅРѕРІРµРЅРёСЏ Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РїСЂРёРѕСЃС‚Р°РЅРѕРІРёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґРѕ РјРѕРјРµРЅС‚Р° РїРѕР»РЅРѕРіРѕ РїРѕРіР°С€РµРЅРёСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё.
---END---
MATRIX_ID: 5.1.3
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: СЃРїРёСЃР°РЅРёРµ СЃСЂРµРґСЃС‚РІ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ | СѓСЃР»РѕРІРёРµ Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р° | РѕСЃРЅРѕРІР°РЅРёРµ - Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ Рѕ РїСЂРѕРІРµРґРµРЅРёРё СЂР°СЃС‡РµС‚РѕРІ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРё РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СѓРґРµСЂР¶Р°С‚СЊ СЃСѓРјРјС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї. 5.1.1 Р”РѕРіРѕРІРѕСЂР°, РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРѕСЃР»РµРґСѓСЋС‰РµРјСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, СЃРїРёСЃС‹РІР°С‚СЊ Р±РµР· РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРіРѕ СЂР°СЃРїРѕСЂСЏР¶РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ (РЅР° СѓСЃР»РѕРІРёСЏС… Р·Р°СЂР°РЅРµРµ РґР°РЅРЅРѕРіРѕ Р°РєС†РµРїС‚Р°, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅРѕРіРѕ Р‘Р°РЅРєСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі) РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° СЃ СЂР°СЃС‡РµС‚РЅРѕРіРѕ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РѕС‚РєСЂС‹С‚РѕРіРѕ РІ Р‘Р°РЅРєРµ. 
---END---
MATRIX_ID: 5.1.4
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: СѓРєР°Р·Р°РЅ РЅРѕРјРµСЂ СЂР°СЃС‡РµС‚РЅРѕРіРѕ СЃС‡РµС‚Р° РџСЂРµРґРїСЂРёСЏС‚РёСЏ | СѓРєР°Р·Р°РЅРѕ РЅР°РёРјРµРЅРѕРІР°РЅРёРµ Р‘Р°РЅРєР°, РІ РєРѕС‚РѕСЂРѕРј Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РѕС‚РєСЂС‹С‚ СЃС‡РµС‚
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРё РЅРµРІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СѓРґРµСЂР¶Р°С‚СЊ СЃСѓРјРјС‹, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Рї. 5.1.1 Р”РѕРіРѕРІРѕСЂР°, РёР· СЃСѓРјРј, РїРѕРґР»РµР¶Р°С‰РёС… РїРѕСЃР»РµРґСѓСЋС‰РµРјСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЋ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅР° РѕРїР»Р°С‚Сѓ РёР»Рё РїР»Р°С‚РµР¶РЅРѕРµ С‚СЂРµР±РѕРІР°РЅРёРµ Рѕ СЃРїРёСЃР°РЅРёРё РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ Рє СЂР°СЃС‡РµС‚РЅРѕРјСѓ СЃС‡РµС‚Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ в„– --------------------------- РІ ----------------------- (РЅР°РёРјРµРЅРѕРІР°РЅРёРµ Р‘Р°РЅРєР°, РєРѕС‚РѕСЂРѕРј Сѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РѕС‚РєСЂС‹С‚ СЃС‡РµС‚). 
---END---
MATRIX_ID: 5.1.5
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅРµ РІРѕР·РјРµС‰Р°С‚СЊ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РќРµ РІРѕР·РјРµС‰Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№, РїСЂРѕРІРµРґРµРЅРЅС‹С… СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°.
---END---
MATRIX_ID: 5.1.6
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРµСЂСЏС‚СЊ С‚РµС…РЅРёС‡РµСЃРєРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ С‚РµСЂРјРёРЅР°Р»РѕРІ РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РїСЂРµРґРїСЂРёСЏС‚РёСЏ | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·Р°РєР°Р·С‡РёРєР° Р·Р° 2 СЂР°Р±РѕС‡РёС… РґРЅСЏ | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±РЅРѕРІР»СЏС‚СЊ РџРћ С‚РµСЂРјРёРЅР°Р»РѕРІ СЃ СѓРІРµРґРѕРјР»РµРЅРёРµРј Р·Р°РєР°Р·С‡РёРєР° Р·Р° 2 СЂР°Р±РѕС‡РёС… РґРЅСЏ | Р”РѕРїСѓСЃРєР°РµС‚СЃСЏ СѓРґР°Р»РµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ РџРћ С‚РµСЂРјРёРЅР°Р»РѕРІ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ РїРѕСЂСЏРґРєР° РѕРїРµСЂР°С†РёР№ Рё Р±РµР· РїСЂРµРґРІР°СЂРёС‚РµР»СЊРЅРѕРіРѕ СѓРІРµРґРѕРјР»РµРЅРёСЏ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїСЂРѕРІРµСЂРєСѓ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ Рё РїРѕСЂСЏРґРєР° СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР°, СЂР°СЃРїРѕР»РѕР¶РµРЅРЅС‹С… РЅР° С‚РµСЂСЂРёС‚РѕСЂРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў. РџСЂРѕРёР·РІРѕРґРёС‚СЊ Р·Р°РјРµРЅСѓ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР°, Р° С‚Р°РєР¶Рµ РѕР±РЅРѕРІР»СЏС‚СЊ РїСЂРѕРіСЂР°РјРјРЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, СѓРІРµРґРѕРјРёРІ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµ РјРµРЅРµРµ С‡РµРј Р·Р° 2 (РґРІР°) СЂР°Р±РѕС‡РёС… РґРЅСЏ РґРѕ РґР°С‚С‹ Р·Р°РјРµРЅС‹ РёР»Рё РѕР±РЅРѕРІР»РµРЅРёСЏ. Р”РѕРїСѓСЃРєР°РµС‚СЃСЏ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ СѓРґР°Р»РµРЅРЅРѕРµ РѕР±РЅРѕРІР»РµРЅРёРµ РїСЂРѕРіСЂР°Рј
---END---
MATRIX_ID: 5.1.7
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РїСЂРё РІС‹СЏРІР»РµРЅРёРё РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РѕРїРµСЂР°С†РёР№ | Р‘Р°РЅРє РїРµСЂРµРґР°РµС‚ РґР°РЅРЅС‹Рµ РІ РџР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РњР�Р  РїСЂРё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё РґРѕРіРѕРІРѕСЂР° РёР·-Р·Р° РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° | РџРµСЂРµРґР°РІР°РµРјР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ РІРєР»СЋС‡Р°РµС‚ РґР°С‚Сѓ Р·Р°РєР»СЋС‡РµРЅРёСЏ Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°, РїСЂРёС‡РёРЅСѓ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Рё РґСЂСѓРіРёРµ СЃРІРµРґРµРЅРёСЏ Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РќРµР·Р°РІРёСЃРёРјРѕ РѕС‚ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ РІС‹СЏРІР»РµРЅРёСЏ РїРѕРґРѕР·СЂРёС‚РµР»СЊРЅС‹С… РёР»Рё РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РћРїРµСЂР°С†РёР№ РїРµСЂРµРґР°РІР°С‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ, РІ С‚РѕРј С‡РёСЃР»Рµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РїРµСЂРµРґР°С‡Сѓ РґР°РЅРЅС‹С… (СЃРІРµРґРµРЅРёСЏ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў/Р РµСЃСѓСЂСЃРµ, РІ С‚РѕРј С‡РёСЃР»Рµ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ/РїСЂРµРґСЃС‚Р°РІРёС‚РµР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅС‹Рµ РІ Р—Р°СЏРІР»РµРЅРёРё/Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў) РІ РџР»Р°С‚РµР¶РЅСѓСЋ СЃРёСЃС‚РµРјСѓ РњР�Р  РІ С†РµР»СЏС… РёСЃРїРѕР»РЅРµРЅРёСЏ Р·Р°РїСЂРѕСЃРѕРІ, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ СѓРєР°Р·Р°РЅРЅРѕР№ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹.Р’ СЃР»СѓС‡Р°Рµ РїСЂРёРЅСЏС‚РёСЏ Р‘Р°РЅРєРѕРј СЂРµС€РµРЅРёСЏ Рѕ СЂР°СЃС‚РѕСЂР¶Рµ
---END---
MATRIX_ID: 5.1.8.1
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ Р”РѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅР°СЂСѓС€РµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°;
---END---
MATRIX_ID: 5.1.8.2
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РїСЂРёС‡Р°СЃС‚РЅС‹С… Рє СЌРєСЃС‚СЂРµРјРёР·РјСѓ, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЋ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РђРІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІРЅРµСЃРµРЅРёРµ РґР°РЅРЅС‹С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІ РїРµСЂРµС‡РµРЅСЊ РѕСЂРіР°РЅРёР·Р°С†РёР№ Рё С„РёР·РёС‡РµСЃРєРёС… Р»РёС†, РІ РѕС‚РЅРѕС€РµРЅРёРё РєРѕС‚РѕСЂС‹С… РёРјРµСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕР± РёС… РїСЂРёС‡Р°СЃС‚РЅРѕСЃС‚Рё Рє СЌРєСЃС‚СЂРµРјРёСЃС‚СЃРєРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, С‚РµСЂСЂРѕСЂРёР·РјСѓ РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёСЋ СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЏ РѕСЂСѓР¶РёСЏ РјР°СЃСЃРѕРІРѕРіРѕ СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ;
---END---
MATRIX_ID: 5.1.8.3
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РѕС‚РјС‹РІР°РЅРёРµ РґРµРЅРµРі РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёРµ С‚РµСЂСЂРѕСЂРёР·РјР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїСЂРё РЅР°Р»РёС‡РёРё Сѓ Р‘Р°РЅРєР° РїРѕРґРѕР·СЂРµРЅРёР№, С‡С‚Рѕ РћРїРµСЂР°С†РёРё РІ РўРЎРў/РЅР° Р РµСЃСѓСЂСЃРµ СЃРѕРІРµСЂС€Р°СЋС‚СЃСЏ РІ С†РµР»СЏС… Р»РµРіР°Р»РёР·Р°С†РёРё (РѕС‚РјС‹РІР°РЅРёСЏ) РґРѕС…РѕРґРѕРІ, РїРѕР»СѓС‡РµРЅРЅС‹С… РїСЂРµСЃС‚СѓРїРЅС‹Рј РїСѓС‚РµРј, РёР»Рё С„РёРЅР°РЅСЃРёСЂРѕРІР°РЅРёСЏ С‚РµСЂСЂРѕСЂРёР·РјР°;
---END---
MATRIX_ID: 5.1.8.4
REQUIRED: optional
PRODUCT: internet_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ Р РµСЃСѓСЂСЃР° РўСЂРµР±РѕРІР°РЅРёСЏРј Р‘Р°РЅРєР° Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ;
---END---
MATRIX_ID: 5.1.8.5
REQUIRED: optional
PRODUCT: internet_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРё Р—Р°РєР°Р·С‡РёРєРѕРј Р·Р°РїСЂРµС‰РµРЅРЅС‹С… РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё СЃРѕРіР»Р°СЃРЅРѕ РўСЂРµР±РѕРІР°РЅРёСЏРј Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ РІРёРґРѕРІ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё, СѓРєР°Р·Р°РЅРЅС‹С… РІ РўСЂРµР±РѕРІР°РЅРёСЏС… Рє Р РµСЃСѓСЂСЃСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ;
---END---
MATRIX_ID: 5.1.8.6
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРё РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ СЂРµСЃСѓСЂСЃРµ РѕС‚ РїР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїРѕР»СѓС‡РµРЅРёРµ РЅРµРіР°С‚РёРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў /Р РµСЃСѓСЂСЃРµ  РѕС‚ РѕСЂРіР°РЅРѕРІ РіРѕСЃСѓРґР°СЂСЃС‚РІРµРЅРЅРѕР№ РІР»Р°СЃС‚Рё Р Р¤ Рё/РёР»Рё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹;
---END---
MATRIX_ID: 5.1.8.7
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РђРІС‚РѕСЂРёР·Р°С†РёСЋ РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ | Р”РѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° СЏРІР»СЏСЋС‚СЃСЏ СЃРІРµРґРµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР°-СЌРјРёС‚РµРЅС‚Р° РёР»Рё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ | РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РјРѕР¶РµС‚ Р±С‹С‚СЊ РїРѕР»СѓС‡РµРЅРѕ РїРѕ С„Р°РєСЃСѓ РёР»Рё СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚Рµ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РїРѕР»СѓС‡РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІРµ РІ РўРЎРў /РЅР° Р РµСЃСѓСЂСЃРµ ;СЃС‚РѕСЂРѕРЅС‹ РґРѕРіРѕРІРѕСЂРёР»РёСЃСЊ, С‡С‚Рѕ РґРѕСЃС‚Р°С‚РѕС‡РЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµРј РјРѕС€РµРЅРЅРёС‡РµСЃРєРѕРіРѕ С…Р°СЂР°РєС‚РµСЂР° РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№ СЏРІР»СЏРµС‚СЃСЏ РёРЅС„РѕСЂРјР°С†РёСЏ, РїРѕСЃС‚СѓРїРёРІС€Р°СЏ РѕС‚ Р‘Р°РЅРєРѕРІ-СЌРјРёС‚РµРЅС‚РѕРІ РІ Р‘Р°РЅРє, РёР»Рё СѓРІРµРґРѕРјР»РµРЅРёСЏ РѕС‚ РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹, РїРѕР»СѓС‡РµРЅРЅС‹Рµ c РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј С„Р°РєСЃРёРјРёР»СЊРЅРѕР№ СЃ
---END---
MATRIX_ID: 5.1.8.8
REQUIRED: optional
PRODUCT: trade_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў РїСЂРµРїСЏС‚СЃС‚РІСѓРµС‚ РѕРїРµСЂР°С†РёСЏРј | Р±Р°РЅРє РІРїСЂР°РІРµ РїСЂРµРєСЂР°С‚РёС‚СЊ Р°РІС‚РѕСЂРёР·Р°С†РёСЋ РґР»СЏ РўРЎРў | Р±Р°РЅРє РІРїСЂР°РІРµ РёРЅРёС†РёРёСЂРѕРІР°С‚СЊ СЂР°СЃС‚РѕСЂР¶РµРЅРёРµ РґРѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂРµРјРѕРЅС‚Р° РїРѕРјРµС‰РµРЅРёР№ РўРЎРў, РїСЂРµРїСЏС‚СЃС‚РІСѓСЋС‰РµРµ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЋ РћРїРµСЂР°С†РёР№;
---END---
MATRIX_ID: 5.1.8.9
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ | РІРѕР·Р±СѓР¶РґРµРЅРёРµ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ Р·Р°РєРѕРЅСѓ в„–127-Р¤Р—
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ Р»РёРєРІРёРґР°С†РёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ Р»РёР±Рѕ РІРѕР·Р±СѓР¶РґРµРЅРёРµ РІ РѕС‚РЅРѕС€РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РґРµР»Р° Рѕ Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р¤РµРґРµСЂР°Р»СЊРЅС‹Рј Р·Р°РєРѕРЅРѕРј РѕС‚ 26.10.2002 в„– 127-Р¤Р— В«Рћ РЅРµСЃРѕСЃС‚РѕСЏС‚РµР»СЊРЅРѕСЃС‚Рё (Р±Р°РЅРєСЂРѕС‚СЃС‚РІРµ)В»;
---END---
MATRIX_ID: 5.1.8.10
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё | РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РўРЎРў | РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ РџСЂРµРґРїСЂРёСЏС‚РёСЏ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РІС‹СЏРІР»РµРЅРёРµ РЅРµРґРѕСЃС‚РѕРІРµСЂРЅС‹С… СЃРІРµРґРµРЅРёР№ Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, СЂСѓРєРѕРІРѕРґРёС‚РµР»Рµ(-СЏС…) РІ РёРЅС„РѕСЂРјР°С†РёРё, СѓРєР°Р·Р°РЅРЅРѕР№ РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР°;

---END---
MATRIX_ID: 5.1.8.11
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ Р°РІС‚РѕСЂРёР·Р°С†РёРё РїСЂРё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РїСЂРµРґРїСЂРёСЏС‚РёСЏ | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РїСЂРё РІС‹СЏРІР»РµРЅРЅРѕРј РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі Р·Р°СЏРІР»РµРЅРЅРѕР№ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РїСЂРµРґР»Р°РіР°РµРјС‹С… РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў;
---END---
MATRIX_ID: 5.1.8.12
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ СЏРІР»СЏРµС‚СЃСЏ РѕСЃРЅРѕРІР°РЅРёРµРј РґР»СЏ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РІС‚РѕСЂРёР·Р°С†РёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёСЏ РґРѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РѕС‚СЃСѓС‚СЃС‚РІРёРµ РѕРїРµСЂР°С†РёР№ РІ С‚РµС‡РµРЅРёРµ 30 (С‚СЂРёРґС†Р°С‚Рё) РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РїРѕРґСЂСЏРґ;
---END---
MATRIX_ID: 5.1.8.13
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° | РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РїСЂРµРєСЂР°С‚РёС‚СЊ РїСЂРѕРІРµРґРµРЅРёРµ РђРІС‚РѕСЂРёР·Р°С†РёРё РґР»СЏ РўРЎРў Рё/РёР»Рё РїСЂРѕРІРµСЃС‚Рё РјРµСЂРѕРїСЂРёСЏС‚РёСЏ РїРѕ СЂР°СЃС‚РѕСЂР¶РµРЅРёСЋ Р”РѕРіРѕРІРѕСЂР° РїСЂРё РЅР°СЃС‚СѓРїР»РµРЅРёРё СЃР»РµРґСѓСЋС‰РёС… СЃРѕР±С‹С‚РёР№: в†’ РёСЃС‡РµСЂРїР°РЅРёРµ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° Рё/РёР»Рё РѕРєРѕРЅС‡Р°РЅРёРµ СЃСЂРѕРєР° РґРµР№СЃС‚РІРёСЏ Р”РѕРіРѕРІРѕСЂР°, СѓРєР°Р·Р°РЅРЅРѕРіРѕ РІ Рї. 10.1 Р”РѕРіРѕРІРѕСЂР°.
---END---
MATRIX_ID: 5.1.9
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў | Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ РўРЎРў, РІ С‚.С‡. РѕР±СЂР°С‰Р°С‚СЊСЃСЏ РІ Р‘Р°РЅРє-СЌРјРёС‚РµРЅС‚ РґР»СЏ РїСЂРѕРІРµСЂРєРё РїСЂР°РІРѕРјРµСЂРЅРѕСЃС‚Рё РћРїРµСЂР°С†РёРё.
---END---
MATRIX_ID: 5.1.10
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РїСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ | РџСЂРѕРІРµСЂРєРё РїСЂРѕРІРѕРґСЏС‚СЃСЏ РґР»СЏ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃС‚РІР° Рё РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ СЂРѕРґР° РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РЅРµРј | РџСЂРѕРІРµСЂРєРё РІРєР»СЋС‡Р°СЋС‚ РєРѕРЅС‚СЂРѕР»СЊ СЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј С‚СЂРµР±РѕРІР°РЅРёР№ Р”РѕРіРѕРІРѕСЂР° Рє Р РµСЃСѓСЂСЃСѓ | Р‘Р°РЅРє РјРѕР¶РµС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРѕСЃС‚СѓРї Рє РѕС‚РґРµР»СЊРЅС‹Рј Р·Р°РєСЂС‹С‚С‹Рј СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° РїСЂРё РїСЂРѕРІРµСЂРєР°С…
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РџСЂРѕРІРѕРґРёС‚СЊ РїСЂРѕРІРµСЂРєСѓ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РІ С‚.С‡. РЅР° РїСЂРµРґРјРµС‚ РІС‹СЏРІР»РµРЅРёСЏ РјРѕС€РµРЅРЅРёС‡РµСЃРєРёС… РѕРїРµСЂР°С†РёР№, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РџРѕРєСѓРїР°С‚РµР»СЏРј РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёС… СЂРѕРґСѓ РґРµСЏС‚РµР»СЊРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ, СѓРєР°Р·Р°РЅРЅРѕРјСѓ РІ Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў, РЅРµСЃРѕР±Р»СЋРґРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў С‚СЂРµР±РѕРІР°РЅРёР№, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹С… РЅР°СЃС‚РѕСЏС‰РёРј Р”РѕРіРѕРІРѕСЂРѕРј Рє Р РµСЃСѓСЂСЃСѓ[1].
[2]РџСЂРѕРІРµСЂРєРё РјРѕРіСѓС‚ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊСЃСЏ Р‘Р°РЅРєРѕРј, РІ С‚РѕРј С‡РёСЃР»Рµ СЃ РґРѕСЃС‚СѓРїРѕРј Рє СЂР°Р·РґРµР»Р°Рј Р РµСЃСѓСЂСЃР° СЃ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Рј РґРѕСЃС‚СѓРїРѕРј, РЅРµ СЃРІСЏР·Р°РЅРЅС‹Рј СЃ Р°РґРјРёРЅРёСЃС‚СЂРёСЂРѕРІР°РЅРёРµРј Рё СЃРѕРїСЂРѕРІРѕР¶РґРµ
---END---
MATRIX_ID: 5.1.11
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ Р·Р°РїСЂР°С€РёРІР°С‚СЊ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј | Р‘Р°РЅРє РјРѕР¶РµС‚ С‚СЂРµР±РѕРІР°С‚СЊ РїРёСЃСЊРјРµРЅРЅРѕРµ Р·Р°СЏРІР»РµРЅРёРµ РїСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІР°РјРё РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё | РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ СЃС‡РµС‚Р°, С‡РµРєРё Рё РёРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ С‚СЂРµР±РѕРІР°РЅРёСЋ Р±Р°РЅРєР° | РћР±РјРµРЅ РґРѕРєСѓРјРµРЅС‚Р°РјРё РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· СЌР»РµРєС‚СЂРѕРЅРЅС‹Рµ РєР°РЅР°Р»С‹ СЃРІСЏР·Рё СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ РґРѕРіРѕРІРѕСЂР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р—Р°РїСЂР°С€РёРІР°С‚СЊ Р”РѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј РЅРµ РїРѕР·РґРЅРµРµ 13 (С‚СЂРёРЅР°РґС†Р°С‚Рё) РјРµСЃСЏС†РµРІ СЃ РґР°С‚С‹ СЃРѕРІРµСЂС€РµРЅРёСЏ РћРїРµСЂР°С†РёРё РІ СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РІ Рї. 4.2.10 Р”РѕРіРѕРІРѕСЂР°. Р”Р»СЏ Р°РЅР°Р»РёР·Р° СЃРїРѕСЂРЅС‹С… СЃРёС‚СѓР°С†РёР№ Р‘Р°РЅРє С‚Р°РєР¶Рµ РјРѕР¶РµС‚ РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРёСЃСЊРјРµРЅРЅРѕРіРѕ Р·Р°СЏРІР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃ РёР·Р»РѕР¶РµРЅРёРµРј РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёРё, СЃС‡РµС‚РѕРІ Р·Р° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹Рµ РўРѕРІР°СЂС‹/СѓСЃР»СѓРіРё, С‚РѕРІР°СЂРЅС‹Рµ РёР»Рё РєР°СЃСЃРѕРІС‹Рµ С‡РµРєРё Рё РґСЂСѓРіРёРµ РґРѕРєСѓРјРµРЅС‚С‹, РЅРµРѕР±С…РѕРґРёРјС‹Рµ РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ Р°РЅР°Р»РёР·Р° РѕР±СЃС‚РѕСЏС‚РµР»СЊСЃС‚РІ Рї
---END---
MATRIX_ID: 5.1.12
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РІРїСЂР°РІРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ СЃРІСЏР·Р°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ unilateral_in_one_day_right | РћРїСѓР±Р»РёРєРѕРІР°РЅРёРµ РёР·РјРµРЅРµРЅРёР№ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ РІРЅРѕСЃРёС‚СЊ РёР·РјРµРЅРµРЅРёСЏ РІ РґРѕРєСѓРјРµРЅС‚С‹, СЃСЃС‹Р»РєРё РЅР° РєРѕС‚РѕСЂС‹Рµ РґР°СЋС‚СЃСЏ РІ Р”РѕРіРѕРІРѕСЂРµ, РїСѓС‚РµРј РїСѓР±Р»РёРєР°С†РёРё РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР° РЅРµ РјРµРЅРµРµ С‡РµРј Р·Р° 1 (РѕРґРёРЅ) РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РґРµРЅСЊ РґРѕ РІРІРµРґРµРЅРёСЏ РІ РґРµР№СЃС‚РІРёРµ СѓРєР°Р·Р°РЅРЅС‹С… РёР·РјРµРЅРµРЅРёР№.
---END---
MATRIX_ID: 5.1.13
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµРґРѕРјР»РµРЅРёСЏ, С‚Рѕ СЌС‚Рѕ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РёР·РјРµРЅСЏС‚СЊ СЃРІРѕРё СЂРµРєРІРёР·РёС‚С‹ | РЈРІРµРґРѕРјР»РµРЅРёРµ РѕР± РёР·РјРµРЅРµРЅРёРё СЂРµРєРІРёР·РёС‚РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ С‡РµСЂРµР· РћС„РёС†РёР°Р»СЊРЅС‹Р№ СЃР°Р№С‚ Р‘Р°РЅРєР°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ СЃР»СѓС‡Р°Рµ РёР·РјРµРЅРµРЅРёСЏ СЂРµРєРІРёР·РёС‚РѕРІ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹С… РІ Р”РѕРіРѕРІРѕСЂРµ, СѓРІРµРґРѕРјРёС‚СЊ РѕР± СЌС‚РѕРј РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСѓС‚РµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РЅР° РћС„РёС†РёР°Р»СЊРЅРѕРј СЃР°Р№С‚Рµ Р‘Р°РЅРєР°. 
---END---
MATRIX_ID: 5.1.14
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ | РђРґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ СѓРєР°Р·Р°РЅ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ | Р—Р°РїСЂРѕСЃС‹ РЅР°РїСЂР°РІР»РµРЅС‹ РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р’ С†РµР»СЏС… РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё РїРѕ РћРїРµСЂР°С†РёСЏРј РЅР°РїСЂР°РІР»СЏС‚СЊ Р·Р°РїСЂРѕСЃС‹ РЅР° Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹ РџСЂРµРґРїСЂРёСЏС‚РёСЏ/РўРЎРў, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ Р—Р°СЏРІР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅР° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ С‚РѕРІР°СЂРѕРІ/СѓСЃР»СѓРі /Р�РЅС„РѕСЂРјР°С†РёРё Рѕ РўРЎРў.
---END---
MATRIX_ID: 5.1.15
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ РѕС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· СѓРєР°Р·Р°РЅРёСЏ РїСЂРёС‡РёРЅ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РћС‚РєР°Р·Р°С‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РІ Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° Р±РµР· РѕР±СЉСЏСЃРЅРµРЅРёСЏ РїСЂРёС‡РёРЅ.
---END---
MATRIX_ID: 5.1.16
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ С‚СЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ | РџРµСЂРµС‡РµРЅСЊ С‚СЂРµР±СѓРµРјС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ РўСЂРµР±РѕРІР°С‚СЊ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚РѕРІ Рё СЃРІРµРґРµРЅРёР№, РЅРµРѕР±С…РѕРґРёРјС‹С… РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ С„СѓРЅРєС†РёР№, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёСЏРјРё РґРµР№СЃС‚РІСѓСЋС‰РµРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°
---END---
MATRIX_ID: 5.1.17.1
REQUIRED: optional
PRODUCT: trade_acquiring
LOT: common
TERMINAL: pos
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ СЂРµРіРёРѕРЅРѕРІ | РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. Р·Р° РјРµСЃСЏС† РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР±
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р° РїРѕСЃР»РµРґРЅРёР№ РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РјРµСЃСЏС† (Р±РµР· СѓС‡РµС‚Р° РІ РѕР±РѕСЂРѕС‚Рµ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°);
---END---
MATRIX_ID: 5.1.17.2
REQUIRED: optional
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 40 000 СЂСѓР±. РґР»СЏ СЂРµРіРёРѕРЅРѕРІ | С‚РѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РјРµРЅРµРµ 80 000 СЂСѓР±. РґР»СЏ РњРѕСЃРєРІС‹ Рё РЎРџР± | РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ СЃРµСЂРІРёСЃРЅРѕРјСѓ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЋ | РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏРј Р±Р°РЅРєР° | РЅР°Р»РёС‡РёРµ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚Рё РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РёРјРµРµС‚ РїСЂР°РІРѕ: в†’ Р‘Р°РЅРє РІРїСЂР°РІРµ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ Р”РѕРіРѕРІРѕСЂ Рё РїРѕС‚СЂРµР±РѕРІР°С‚СЊ РІРѕР·РІСЂР°С‚Р° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ, РЅР°С…РѕРґСЏС‰РёС…СЃСЏ РІ СЃРѕР±СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР°, РІ СЃР»СѓС‡Р°Рµ РµСЃР»Рё: в†’ 5.1.17.2. РўРѕСЂРіРѕРІС‹Р№ РѕР±РѕСЂРѕС‚ РЅР° РѕРґРёРЅ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 40 000 (СЃРѕСЂРѕРє С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№ (РґР»СЏ Рі. РњРѕСЃРєРІР° Рё Рі. РЎР°РЅРєС‚-РџРµС‚РµСЂР±СѓСЂРі РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 80 000 (РІРѕСЃРµРјСЊРґРµСЃСЏС‚ С‚С‹СЃСЏС‡) СЂСѓР±Р»РµР№) Р·Р° РїРѕСЃР»РµРґРЅРёР№ РєР°Р»РµРЅРґР°СЂРЅС‹Р№ РјРµСЃСЏС† (Р±РµР· СѓС‡РµС‚Р° РІ РѕР±РѕСЂРѕС‚Рµ РћРїРµСЂР°С†РёР№ РІРѕР·РІСЂР°С‚Р°) РёР»Рё РёРјРµРµС‚СЃСЏ Р·Р°РґРѕР»Р¶РµРЅРЅРѕСЃС‚СЊ Рї
---END---
MATRIX_ID: 5.2.1
REQUIRED: mandatory
PRODUCT: internet_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РѕР±РµСЃРїРµС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ | РѕРїРёСЃР°РЅРёРµ РїРѕСЂСЏРґРєР° РґРѕСЃС‚СѓРїР° Рє РЎРџР­Рџ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РґРѕСЃС‚СѓРї Рє РЎРџР­Рџ РґР»СЏ РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёСЏ РћРїРµСЂР°С†РёР№.
---END---
MATRIX_ID: 5.2.2
REQUIRED: mandatory
PRODUCT: internet_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё | РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ С‚РµС…РЅРѕР»РѕРіРёР№ 3DSecure
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёС‚СЊ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№ РІ Р�РЅС‚РµСЂРЅРµС‚-СЌРєРІР°Р№СЂРёРЅРіРµ РїРѕСЃСЂРµРґСЃС‚РІРѕРј РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РїСЂРѕС‚РѕРєРѕР»РѕРІ Рё РўРµС…РЅРѕР»РѕРіРёР№ 3DSecure
---END---
MATRIX_ID: 5.2.3
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° РЅРµ РґРµРєР»Р°СЂРёСЂСѓРµС‚СЃСЏ. РћС‚СЃСѓС‚СЃС‚РІРёРµ РѕС‚СЃС‹Р»РєРё РЅР° СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј РЅРµ СЏРІР»СЏРµС‚СЃСЏ
TOPICS: СѓСЃС‚Р°РЅРѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё | РїРѕРґРіРѕС‚РѕРІРєР° Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р‘Р°РЅРєР° Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё | РїСЂРѕРІРµРґРµРЅРёРµ РїРµСЂРІРёС‡РЅРѕРіРѕ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РЈСЃС‚Р°РЅРѕРІРёС‚СЊ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё Рё РїРѕРґРіРѕС‚РѕРІРёС‚СЊ Рє СЌРєСЃРїР»СѓР°С‚Р°С†РёРё Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹ Р‘Р°РЅРєР° РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№. РџСЂРѕРІРµСЃС‚Рё РїРµСЂРІРёС‡РЅС‹Р№ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶ СЂР°Р±РѕС‚РЅРёРєРѕРІ РўРЎРў РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹РјРё Р‘Р°РЅРєРѕРј
---END---
MATRIX_ID: 5.2.4
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚ РђРІС‚РѕСЂРёР·Р°С†РёСЋ Р±РµР· РїРµСЂРµСЂС‹РІРѕРІ 24 С‡Р°СЃР° РІ СЃСѓС‚РєРё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ РђРІС‚РѕСЂРёР·Р°С†РёСЋ
---END---
MATRIX_ID: 5.2.5
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃР°Р№С‚Р° РїСЂРѕС‡РµСЂРє, С‚Рѕ СЌС‚Рѕ РЅРµ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ
TOPICS: РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ СЂР°Р·РјРµС‰РµРЅС‹ РїРѕ СѓРєР°Р·Р°РЅРЅРѕР№ СЃСЃС‹Р»РєРµ | РјР°С‚РµСЂРёР°Р»С‹ РґРѕСЃС‚СѓРїРЅС‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р Р°Р·РјРµСЃС‚РёС‚СЊ РЅР° СЃР°Р№С‚Рµ:  https://www.sberbank.ru/help/business/acquiring РѕР±СѓС‡Р°СЋС‰РёРµ РјР°С‚РµСЂРёР°Р»С‹ РґР»СЏ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРёРєР°РјРё РџСЂРµРґРїСЂРёСЏС‚РёСЏ
---END---
MATRIX_ID: 5.2.6
REQUIRED: optional
PRODUCT: trade_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±РµСЃРїРµС‡РµРЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё | РћР±РµСЃРїРµС‡РµРЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рµ С‚РµСЂРјРёРЅР°Р»С‹/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»С‹, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РЅР° РџСЂРµРґРїСЂРёСЏС‚РёРё/РўРЎРў, РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹РјРё РјР°С‚РµСЂРёР°Р»Р°РјРё, РЅРµРѕР±С…РѕРґРёРјС‹РјРё РґР»СЏ РїСЂРѕРІРµРґРµРЅРёСЏ РћРїРµСЂР°С†РёР№
---END---
MATRIX_ID: 5.2.7
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅР°СЏ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ | Р·Р°РјРµРЅР° РЅРµРёСЃРїСЂР°РІРЅРѕРіРѕ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РЅР° РёСЃРїСЂР°РІРЅС‹Р№ РЅРµ РїРѕР·РґРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ Р·Р°СЏРІРєРё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћР±РµСЃРїРµС‡РёРІР°С‚СЊ РєСЂСѓРіР»РѕСЃСѓС‚РѕС‡РЅСѓСЋ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚СЊ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ. Р’ СЃР»СѓС‡Р°Рµ РІС‹С…РѕРґР° РёР· СЃС‚СЂРѕСЏ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° Р‘Р°РЅРєР°, РѕР±РµСЃРїРµС‡РёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїСЂР°РІРЅС‹Рј Р­Р»РµРєС‚СЂРѕРЅРЅС‹Рј С‚РµСЂРјРёРЅР°Р»РѕРј/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРј Р‘Р°РЅРєР° РЅРµ РїРѕР·РґРЅРµРµ 3 (С‚СЂРµС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ Р‘Р°РЅРєРѕРј Р·Р°СЏРІРєРё РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕ РЅРѕРјРµСЂСѓ СЃР»СѓР¶Р±С‹ РїРѕРґРґРµСЂР¶РєРё Р‘Р°РЅРєР° РїРѕ С‚РµР»РµС„РѕРЅР°Рј, СѓРєР°Р·Р°РЅРЅС‹Рј РІ Рї..2. РџРѕСЂСЏРґРєР° РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёР№ РІ РўРѕСЂРіРѕРІРѕ-СЃРµСЂРІРёСЃРЅС‹С… С‚РѕС‡РєР°С…/РЅР° Р РµСЃСѓСЂСЃРµ.
---END---
MATRIX_ID: 5.2.8
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
TOPICS: РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РЅРµ РїРѕР·РґРЅРµРµ 2 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё | РґР°С‚Р° РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё - СЂР°Р±РѕС‡РёР№ РґРµРЅСЊ, СЃР»РµРґСѓСЋС‰РёР№ Р·Р° РґРЅРµРј СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ СЃРІРµСЂРєРё РёС‚РѕРіРѕРІ | РїСЂРё С‚РµС…РЅРёС‡РµСЃРєРѕРј СЃР±РѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёСЃС…РѕРґРёС‚ С‡РµСЂРµР· 3 РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅСЏ РїРѕСЃР»Рµ РїРѕСЃР»РµРґРЅРµР№ СѓСЃРїРµС€РЅРѕР№ СЃРІРµСЂРєРё
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РќР° РѕСЃРЅРѕРІР°РЅРёРё РїРѕР»СѓС‡РµРЅРЅРѕР№ РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё, РїРµСЂРµРґР°РЅРЅРѕР№ РѕС‚ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р°/РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р°  / Р РµСЃСѓСЂСЃР° /QR-РєРѕРґР°  РІ Р‘Р°РЅРє, РЅРµ РїРѕР·РґРЅРµРµ 2 (РґРІСѓС…) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј РїРµСЂРµС‡РёСЃР»СЏС‚СЊ РЅР° СЂР°СЃС‡РµС‚РЅС‹Р№ (С‚РµРєСѓС‰РёР№) СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚С‹ РІ РІР°Р»СЋС‚Рµ РїСЂРѕРІРµРґРµРЅРёСЏ РѕРїРµСЂР°С†РёРё (СЂСѓР±Р»Рё Р Р¤) Р·Р° РІС‹С‡РµС‚РѕРј СЃСѓРјРј, РїРµСЂРµС‡РёСЃР»РµРЅРЅС‹С… РІ Рї.5.1.1 РЅР°СЃС‚РѕСЏС‰РµРіРѕ Р”РѕРіРѕРІРѕСЂР°. Р”Р°С‚РѕР№ РїРѕР»СѓС‡РµРЅРёСЏ СЂР°СЃС‡РµС‚РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Р‘Р°РЅРєРѕРј СЏРІР»СЏРµС‚СЃСЏ РґР°
---END---
MATRIX_ID: 5.2.9
REQUIRED: optional
PRODUCT: trade_acquiring
LOT: common
TERMINAL: common
PAYMENT: qr
MAIN_IDEA: 
TOPICS: РџСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ QR-РєРѕРґР° РїР°СЂС‚РЅРµСЂР° РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РџСЂРµРґРїСЂРёСЏС‚РёСЋ QR-РєРѕРґ РїР°СЂС‚РЅРµСЂР° РїРѕ СЌР»РµРєС‚СЂРѕРЅРЅС‹Рј РєР°РЅР°Р»Р°Рј СЃРІСЏР·Рё РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ РёР»Рё РЅР° Р±СѓРјР°Р¶РЅРѕРј РЅРѕСЃРёС‚РµР»Рµ
---END---
MATRIX_ID: 5.2.10
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: 
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ РћСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РѕР±СЂР°Р±РѕС‚РєСѓ РџР”РЅ, РїРѕР»СѓС‡РµРЅРЅС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, Р° С‚Р°РєР¶Рµ РѕР±РµСЃРїРµС‡РёС‚СЊ РєРѕРЅС„РёРґРµРЅС†РёР°Р»СЊРЅРѕСЃС‚СЊ Рё Р·Р°С‰РёС‚Сѓ РѕР±СЂР°Р±Р°С‚С‹РІР°РµРјС‹С… РџР”РЅ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚СЂРµР±РѕРІР°РЅРёСЏРјРё Р¤РµРґРµСЂР°Р»СЊРЅРѕРіРѕ Р·Р°РєРѕРЅР° РѕС‚ 27 РёСЋР»СЏ 2006 в„– 152-Р¤Р— В«Рћ РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹С… РґР°РЅРЅС‹С…В». РџСЂРёРЅРёРјР°С‚СЊ РЅРµРѕР±С…РѕРґРёРјС‹Рµ РїСЂР°РІРѕРІС‹Рµ, РѕСЂРіР°РЅРёР·Р°С†РёРѕРЅРЅС‹Рµ Рё С‚РµС…РЅРёС‡РµСЃРєРёРµ РјРµСЂС‹ РёР»Рё РѕР±РµСЃРїРµС‡РёРІР°С‚СЊ РёС… РїСЂРёРЅСЏС‚РёРµ РґР»СЏ Р·Р°С‰РёС‚С‹ РїРѕР»СѓС‡Р°РµРјС‹С… РѕС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РџР”РЅ РѕС‚ РЅРµРїСЂР°РІРѕРјРµСЂРЅРѕРіРѕ РёР»Рё СЃР»СѓС‡Р°Р№РЅРѕРіРѕ РґРѕСЃС‚СѓРїР° Рє РЅРёРј, СѓРЅРёС‡С‚РѕР¶РµРЅРёСЏ, РёР·РјРµРЅРµРЅРёСЏ, Р±Р»РѕРєРёСЂРѕРІР°РЅРёСЏ, РєРѕРїРёСЂРѕРІР°
---END---
MATRIX_ID: 5.2.12
REQUIRED: optional
PRODUCT: internet_acquiring
LOT: common
TERMINAL: common
PAYMENT: qr
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API Р±РµР· РіР°СЂР°РЅС‚РёР№
ENRICHED: В«РџР РђР’Рђ Р� РћР‘РЇР—РђРќРќРћРЎРўР� Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РѕР±СЏР·СѓРµС‚СЃСЏ: в†’ Р‘Р°РЅРє РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ QR-API (РІ С‚.С‡. РІСЃС‘, С‡С‚Рѕ СЃРІСЏР·Р°РЅРѕ СЃ РѕСЂРіР°РЅРёР·Р°С†РёРµР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕ-С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ РїРѕСЃСЂРµРґСЃС‚РІРѕРј С‚Р°РєРѕРіРѕ API) В«РєР°Рє РµСЃС‚СЊВ» Р±РµР· РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РєР°РєРёС…-Р»РёР±Рѕ РіР°СЂР°РЅС‚РёР№
---END---
MATRIX_ID: 6.1
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РЅРѕ
TOPICS: СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РѕРїРµСЂР°С†РёР№
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р—Р° РѕСЃСѓС‰РµСЃС‚РІР»РµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹, РџСЂРµРґРїСЂРёСЏС‚РёРµ СѓРїР»Р°С‡РёРІР°РµС‚ Р‘Р°РЅРєСѓ РїР»Р°С‚Сѓ РІ СЂР°Р·РјРµСЂРµ:
В«(____________) РїСЂРѕС†РµРЅС‚ РѕС‚ СЃСѓРјРјС‹ РћРїРµСЂР°С†РёР№ РѕРїР»Р°С‚В».
---END---
MATRIX_ID: 6.2
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі). Р’Р°Р¶РЅРѕ РїСЂРѕРІРµСЂРёС‚СЊ СЃСЂРѕРєРё Рё РїРµСЂРёРѕРґРёС‡РЅРѕСЃС‚СЊ РѕРїР»Р°С‚С‹
TOPICS: Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РґРѕРєСѓРјРµРЅС‚ РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° | РІ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РІРєР»СЋС‡РµРЅ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРј | РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚[2] (РґР°Р»РµРµ вЂ“ РЈРџР”) РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†. 
Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р‘Р°РЅРєР°, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРµ Рї.6.1 Р”РѕРіРѕРІРѕСЂР°, РІРєР»СЋС‡Р°РµС‚ РќР”РЎ РїРѕ СЃС‚Р°РІРєРµ, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
---END---
MATRIX_ID: 6.3
REQUIRED: mandatory
PRODUCT: common
LOT: fz_223
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РђРєС‚ РґРѕ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РђРєС‚ РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РІРјРµСЃС‚Рµ СЃРѕ СЃС‡РµС‚РѕРј-С„Р°РєС‚СѓСЂРѕР№ С„РѕСЂРјС‹ 363 | Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ СЃРѕРіР»Р°СЃРЅРѕ РїСѓРЅРєС‚Сѓ 6.1 РґРѕРіРѕРІРѕСЂР° | Р’РѕР·РЅР°РіСЂР°Р¶РґРµРЅРёРµ Р±Р°РЅРєР° РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї.3 СЃС‚.149 РќРљ Р Р¤ | РЎСЂРѕРє РЅР°РїСЂР°РІР»РµРЅРёСЏ Р‘Р°РЅРєРѕРј РґРѕРєСѓРјРµРЅС‚Р° РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР°
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РјРµСЃСЏС†РµРј РѕРєР°Р·Р°РЅРёСЏ СѓСЃР»СѓРі (РґР°Р»РµРµ вЂ“ РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†), РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РђРєС‚ Рѕ РїРµСЂРµС‡РёСЃР»РµРЅРёРё РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃСѓРјРј РѕРїРµСЂР°С†РёР№ РїРѕ РєР°СЂС‚Р°Рј РїРѕ С„РѕСЂРјРµ РџСЂРёР»РѕР¶РµРЅРёСЏ 2 Рє Р”РѕРіРѕРІРѕСЂСѓ (РґР°Р»РµРµ вЂ“ РђРєС‚) Рё СЃС‡РµС‚ С„.363 РЅР° РѕРїР»Р°С‚Сѓ СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.Р Р°Р·РјРµСЂ РІРѕР·РЅР°РіСЂР°Р¶РґРµРЅРёСЏ, РїСЂРёС‡РёС‚Р°СЋС‰РµРіРѕСЃСЏ Р‘Р°РЅРєСѓ, РѕРїСЂРµРґРµР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Рї.6.1 Р”РѕРіРѕРІРѕСЂР° Рё РЅРµ РѕР±Р»Р°РіР°РµС‚СЃСЏ РќР”РЎ РЅР° РѕСЃРЅРѕРІР°РЅРёРё Рї. 3 СЃС‚
---END---
MATRIX_ID: 6.4
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ РїСЂРёРЅСЏС‚СЊ Рё РІРѕР·РІСЂР°С‚РёС‚СЊ РЈРџР” (РїСЂРёРЅСЏС‚СЊ РѕРєР°Р·Р°РЅРЅС‹Рµ СѓСЃР»СѓРіРё) | РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
---END---
MATRIX_ID: 6.5
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” | С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ | РґРµРЅРµР¶РЅС‹Рµ СЃСЂРµРґСЃС‚РІР° РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р±Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
---END---
MATRIX_ID: 6.6
REQUIRED: mandatory
PRODUCT: common
LOT: fz_223
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕРїР»Р°С‚Р° СѓСЃР»СѓРі Р±Р°РЅРєР° РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕР»СѓС‡РµРЅРёСЏ Р°РєС‚Р° Рё СЃС‡РµС‚Р° С„РѕСЂРјС‹ 363 | С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ | РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСЂРµРґСЃС‚РІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РЅР° СЃС‡РµС‚, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„РѕСЂРјС‹ 363
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° СѓСЃР»СѓРі Р‘Р°РЅРєР° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РћРїРµСЂР°С†РёСЏРј РѕРїР»Р°С‚С‹ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° РђРєС‚Р° Рё СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.
---END---
MATRIX_ID: 6.7
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: СѓРєР°Р·Р°РЅ СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅРѕРіРѕ С‚РµСЂРјРёРЅР°Р»Р° | СѓРєР°Р·Р°РЅРѕ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂСѓР±Р»РµР№ РІРєР»СЋС‡Р°СЏ РќР”РЎ | СѓСЃС‚Р°РЅРѕРІР»РµРЅ РµР¶РµРјРµСЃСЏС‡РЅС‹Р№ РїРѕСЂСЏРґРѕРє РѕРїР»Р°С‚С‹
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ РІ СЂР°Р·РјРµСЂРµ _____ (__________________) СЂСѓР±Р»РµР№ (РІРєР»СЋС‡Р°СЏ РќР”РЎ) Р·Р° РєР°Р¶РґС‹Р№ Р­Р»РµРєС‚СЂРѕРЅРЅС‹Р№ С‚РµСЂРјРёРЅР°Р».
---END---
MATRIX_ID: 6.8
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.

---END---
MATRIX_ID: 6.9
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: fz_223
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РЎС‡РµС‚ РІС‹СЃС‚Р°РІР»СЏРµС‚СЃСЏ РїРѕ С„РѕСЂРјРµ в„–363 | РЎС‡РµС‚ СЃРѕРґРµСЂР¶РёС‚ СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ | РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё
---END---
MATRIX_ID: 6.10
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓРєР°Р·Р°РЅРЅС‹Рµ СЃСЂРѕРєРё
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
---END---
MATRIX_ID: 6.11
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ | СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ С„РѕСЂРјР° | РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
---END---
MATRIX_ID: 6.12
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: fz_223
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ | РЎРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ | РћСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363 | РџРѕР»СѓС‡Р°С‚РµР»СЊ РїР»Р°С‚РµР¶Р° - СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ Р­Р»РµРєС‚СЂРѕРЅРЅС‹С… С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363.
---END---
MATRIX_ID: 6.13
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РµР¶РµРјРµСЃСЏС‡РЅР°СЏ | СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РґРЅСЏРј РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё С‚РµСЂРјРёРЅР°Р»Р° | РїРµСЂРµСЃС‡РµС‚ РїР»Р°С‚С‹ РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° Р·Р° РѕС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† | СѓРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ СѓРїР»Р°С‡РёРІР°РµС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РµР¶РµРјРµСЃСЏС‡РЅРѕ Р·Р° РєР°Р¶РґС‹Р№ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ С‚Р°СЂРёС„РѕРј, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рј РїСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РІ РџСЂРёР»РѕР¶РµРЅРёРё 1.1 Рє Р”РѕРіРѕРІРѕСЂСѓ. РџСЂРё СЌС‚РѕРј СЂР°СЃС‡РµС‚ РїР»Р°С‚С‹ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РїСЂРѕРїРѕСЂС†РёРѕРЅР°Р»СЊРЅРѕ РєРѕР»РёС‡РµСЃС‚РІСѓ РєР°Р»РµРЅРґР°СЂРЅС‹С… РґРЅРµР№ РјРµСЃСЏС†Р° СЃ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»Р° РІ РўРЎРў. РџСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё/РѕС‚РєР»СЋС‡РµРЅРёРё 2D СЃРєР°РЅРµСЂР° СЂР°Р·РјРµСЂ РїР»Р°С‚С‹ Р·Р° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РїРµСЂРµСЃС‡РёС‚С‹РІР°РµС‚СЃСЏ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РЅРµР·Р°РІРёСЃРёРјРѕ РѕС‚ РґР°С‚С‹ СѓСЃС‚Р°РЅРѕРІРєРё/СЃРЅСЏС‚РёСЏ СЃРєР°РЅРµСЂ
---END---
MATRIX_ID: 6.14
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РЅР°РїСЂР°РІР»СЏРµС‚ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 5 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РЈРџР” РЅР°РїСЂР°РІР»СЏРµС‚СЃСЏ РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 5 (РїСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ РЈРџР”  РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
---END---
MATRIX_ID: 6.15
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: fz_223
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РІС‹СЃС‚Р°РІР»СЏРµС‚ СЃС‡РµС‚ РЅРµ РїРѕР·РґРЅРµРµ 10 СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р‘Р°РЅРє РµР¶РµРјРµСЃСЏС‡РЅРѕ, РЅРµ РїРѕР·РґРЅРµРµ 10 (РґРµСЃСЏС‚РѕРіРѕ) СЂР°Р±РѕС‡РµРіРѕ РґРЅСЏ РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РЅР°РїСЂР°РІР»СЏРµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЋ СЃС‡РµС‚ С„.363 РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС†.
РЎС‡РµС‚-С„Р°РєС‚СѓСЂР° РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚СЃСЏ Р‘Р°РЅРєРѕРј РІ РїРѕСЂСЏРґРєРµ Рё СЃСЂРѕРєРё, СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РґРµР№СЃС‚РІСѓСЋС‰РёРј РЅР°Р»РѕРіРѕРІС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё.
---END---
MATRIX_ID: 6.16
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РџСЂРµРґРїСЂРёСЏС‚РёРµ РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РЈРџР” РЅРµ РїРѕР·РґРЅРµРµ 25 С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РѕС‚С‡РµС‚РЅС‹Рј | РџСЂРµРґРїСЂРёСЏС‚РёРµ РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµС‚ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ СЃСЂРѕРєРё
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РІ СЃСЂРѕРє РЅРµ РїРѕР·РґРЅРµРµ 25 (РґРІР°РґС†Р°С‚СЊ РїСЏС‚РѕРіРѕ) С‡РёСЃР»Р° РјРµСЃСЏС†Р°, СЃР»РµРґСѓСЋС‰РµРіРѕ Р·Р° РћС‚С‡РµС‚РЅС‹Рј РјРµСЃСЏС†РµРј, РѕР±СЏР·Р°РЅРѕ РІРѕР·РІСЂР°С‚РёС‚СЊ РІ Р‘Р°РЅРє РїРѕРґРїРёСЃР°РЅРЅС‹Р№ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РЈРџР” РЅР° СЃСѓРјРјСѓ РїР»Р°С‚С‹ Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† Р»РёР±Рѕ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РјРѕС‚РёРІРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚РєР°Р· РѕС‚ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР”.
---END---
MATRIX_ID: 6.17
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: common
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕРїР»Р°С‚Р° СЃРµСЂРІРёСЃР° РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ РѕСЃСѓС‰РµСЃС‚РІР»СЏРµС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ РїРѕСЃР»Рµ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” | С„РѕСЂРјР° РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅР°СЏ | РґРµРЅСЊРіРё РїРµСЂРµС‡РёСЃР»СЏСЋС‚СЃСЏ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕРґРїРёСЃР°РЅРёСЏ РЈРџР” РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ РЈРџР”.
---END---
MATRIX_ID: 6.18
REQUIRED: mandatory
PRODUCT: trade_acquiring
LOT: fz_223
TERMINAL: smart
PAYMENT: common
MAIN_IDEA: 
TOPICS: РѕРїР»Р°С‚Р° РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РІ С‚РµС‡РµРЅРёРµ 5 СЂР°Р±РѕС‡РёС… РґРЅРµР№ | СЃРїРѕСЃРѕР± РѕРїР»Р°С‚С‹ - Р±РµР·РЅР°Р»РёС‡РЅС‹Р№ РїРµСЂРµРІРѕРґ | РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ РѕРїР»Р°С‚С‹ - СЃС‡РµС‚ С„РѕСЂРјС‹ 363 | СЃСЂРѕРє РѕРїР»Р°С‚С‹ СЃС‡РёС‚Р°РµС‚СЃСЏ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ СЃС‡РµС‚Р°
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РћРїР»Р°С‚Р° Р·Р° СЃРµСЂРІРёСЃРЅРѕРµ РѕР±СЃР»СѓР¶РёРІР°РЅРёРµ РЎРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р»РѕРІ Р·Р° РћС‚С‡РµС‚РЅС‹Р№ РјРµСЃСЏС† РїСЂРѕРёР·РІРѕРґРёС‚СЃСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РІ С‚РµС‡РµРЅРёРµ 5 (РїСЏС‚Рё) СЂР°Р±РѕС‡РёС… РґРЅРµР№ СЃ РґР°С‚С‹ РїРѕР»СѓС‡РµРЅРёСЏ РѕС‚ Р‘Р°РЅРєР° СЃС‡РµС‚Р° С„.363 РІ Р±РµР·РЅР°Р»РёС‡РЅРѕР№ С„РѕСЂРјРµ РїСѓС‚РµРј РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ Р‘Р°РЅРєР°, СѓРєР°Р·Р°РЅРЅС‹Р№ РІ СЃС‡РµС‚Рµ С„.363
---END---
MATRIX_ID: 6.20
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ РєРѕРјРёСЃСЃРёСЏ РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
TOPICS: РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РїРѕ РѕРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р° РЅРµ РІР·РёРјР°РµС‚СЃСЏ | СѓРґРµСЂР¶Р°РЅРЅР°СЏ РїР»Р°С‚Р° Р·Р° СЂР°СЃС‡РµС‚С‹ РїСЂРё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РѕРїРµСЂР°С†РёРё РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ РџРѕ РћРїРµСЂР°С†РёСЏРј РІРѕР·РІСЂР°С‚Р°, Р’РѕР·РІСЂР°С‚ РїР»Р°С‚РµР¶Р° Рё Р РµРІРµСЂСЃРёРІРЅС‹Рј С‚СЂР°РЅР·Р°РєС†РёСЏРј РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ РЅРµ РІР·РёРјР°РµС‚СЃСЏ. Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ РїР»Р°С‚Р° Р·Р° РїСЂРѕРІРµРґРµРЅРёРµ СЂР°СЃС‡РµС‚РѕРІ, СѓРґРµСЂР¶Р°РЅРЅР°СЏ Р‘Р°РЅРєРѕРј РїСЂРё РѕР±СЂР°Р±РѕС‚РєРµ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅРѕР№ РћРїРµСЂР°С†РёРё РѕРїР»Р°С‚С‹, РЅРµ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ.
---END---
MATRIX_ID: 6.21
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: РћС‚СЃСѓС‚СЃС‚РІРёРµ РєРѕРЅРєСЂРµС‚РЅРѕР№ С†РµРЅРЅС‹ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёРµРј
TOPICS: Р¦РµРЅР° РґРѕРіРѕРІРѕСЂР° РІ СЂСѓР±Р»СЏС… | РЈРєР°Р·Р°РЅР° С‚РѕС‡РЅР°СЏ СЃСѓРјРјР° РІ СЂСѓР±Р»СЏС… Рё РєРѕРїРµР№РєР°С… | РЈРїРѕРјРёРЅР°РЅРёРµ Рѕ РІРєР»СЋС‡РµРЅРёРё РќР”РЎ
ENRICHED: В«РћРџР›РђРўРђ РЈРЎР›РЈР“ Р‘РђРќРљРђВ» в†’ Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ _________ (______________________) СЂСѓР±Р»РµР№ __ РєРѕРїРµРµРє. ( РІ С‚РѕРј С‡РёСЃР»Рµ РќР”РЎ)
---END---
MATRIX_ID: 7.1
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР° | РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РїРѕ Р”РѕРіРѕРІРѕСЂСѓ РЎС‚РѕСЂРѕРЅС‹ РЅРµСЃСѓС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРё СЃ СѓСЃР»РѕРІРёСЏРјРё Р”РѕРіРѕРІРѕСЂР° Рё Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј Р Р¤.
---END---
MATRIX_ID: 7.2
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р°
TOPICS: РЁС‚СЂР°С„ РџСЂРµРґРїСЂРёСЏС‚РёСЋ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё.
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
Р±) 5000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 10000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓ
---END---
MATRIX_ID: 7.3
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ С†РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°.
---END---
MATRIX_ID: 7.4
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№) | РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РќР°С‡РёСЃР»РµРЅРёРµ РїРµРЅРё Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё | РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ.РћРїСЂРµРґРµР»РµРЅРёСЏ СЃСЂРѕРєР° РЅР°С‡Р°Р»Р° РЅР°С‡РёСЃР»РµРЅРёСЏ РїРµРЅРё | РЁС‚СЂР°С„ Р‘Р°РЅРєСѓ. РћРїСЂРµРґРµР»РµРЅРёРµ СЂР°Р·РјРµСЂР° РїРµРЅРё
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р’ СЃР»СѓС‡Р°Рµ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р° С‚Р°РєР¶Рµ РІ РёРЅС‹С… СЃР»СѓС‡Р°СЏС… РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅР°РїСЂР°РІР»СЏРµС‚ Р‘Р°РЅРєСѓ С‚СЂРµР±РѕРІР°РЅРёРµ РѕР± СѓРїР»Р°С‚Рµ РЅРµСѓСЃС‚РѕРµРє (С€С‚СЂР°С„РѕРІ, РїРµРЅРµР№).РџРµРЅСЏ РЅР°С‡РёСЃР»СЏРµС‚СЃСЏ Р·Р° РєР°Р¶РґС‹Р№ РґРµРЅСЊ РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІР°, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅРѕРіРѕ Р”РѕРіРѕРІРѕСЂРѕРј, РЅР°С‡РёРЅР°СЏ СЃРѕ РґРЅСЏ, СЃР»РµРґСѓСЋС‰РµРіРѕ РїРѕСЃР»Рµ РґРЅСЏ РёСЃС‚РµС‡РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕРіРѕ Р”РѕРіРѕРІРѕСЂРѕРј СЃСЂРѕРєР° РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°
---END---
MATRIX_ID: 7.5
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё, РёРјРµСЋС‰РёС… СЃС‚РѕРёРјРѕСЃС‚РЅРѕРµ РІС‹СЂР°Р¶РµРЅРёСЏ РІ РїСЂРѕС†РµРЅС‚Р°С… РѕС‚ СЃСѓРјРјС‹ РґРѕРіРѕРІРѕСЂР°
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, Р·Р° РёСЃРєР»СЋС‡РµРЅРёРµРј РїСЂРѕСЃСЂРѕС‡РєРё РёСЃРїРѕР»РЅРµРЅРёСЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 10 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5 РїСЂРѕС†РµРЅС‚РѕРІ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР° РІ СЃР»СѓС‡Р°Рµ, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 1 РїСЂРѕС†РµРЅС‚ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕ
---END---
MATRIX_ID: 7.6
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р Р°Р·РјРµСЂ С€С‚СЂР°С„Р° Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ Р‘Р°РЅРєРѕРј, РЅРµ РёРјРµСЋС‰РµРіРѕ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р—Р° РєР°Р¶РґС‹Р№ С„Р°РєС‚ РЅРµРёСЃРїРѕР»РЅРµРЅРёСЏ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРіРѕ РёСЃРїРѕР»РЅРµРЅРёСЏ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РєРѕС‚РѕСЂРѕРµ РЅРµ РёРјРµРµС‚ СЃС‚РѕРёРјРѕСЃС‚РЅРѕРіРѕ РІС‹СЂР°Р¶РµРЅРёСЏ, СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р° СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ РІ СЃР»РµРґСѓСЋС‰РµРј РїРѕСЂСЏРґРєРµ:
Р°) 1000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№;
Р±) 5000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 3 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 50 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
РІ) 10000 СЂСѓР±Р»РµР№, РµСЃР»Рё Р¦РµРЅР° Р”РѕРіРѕРІРѕСЂР° СЃРѕСЃС‚Р°РІР»СЏРµС‚ РѕС‚ 50 РјР»РЅ. СЂСѓР±Р»РµР№ РґРѕ 100 РјР»РЅ. СЂСѓР±Р»РµР№ (РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ);
Рі) 1000
---END---
MATRIX_ID: 7.7
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±С‰Р°СЏ СЃСѓРјРјР° С€С‚СЂР°С„РѕРІ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ Р‘Р°РЅРєР° РЅРµ РїСЂРµРІС‹С€Р°РµС‚ С†РµРЅСѓ РґРѕРіРѕРІРѕСЂР°
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РћР±С‰Р°СЏ СЃСѓРјРјР° РЅР°С‡РёСЃР»РµРЅРЅС‹С… С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ РёР»Рё РЅРµРЅР°РґР»РµР¶Р°С‰РµРµ РёСЃРїРѕР»РЅРµРЅРёРµ Р‘Р°РЅРєРѕРј РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІ, РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅРЅС‹С… Р”РѕРіРѕРІРѕСЂРѕРј, РЅРµ РјРѕР¶РµС‚ РїСЂРµРІС‹С€Р°С‚СЊ Р¦РµРЅСѓ Р”РѕРіРѕРІРѕСЂР°
---END---
MATRIX_ID: 7.8
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј РџСЂРµРґРїСЂРёСЏС‚РёСЏ(Р—Р°РєР°Р·С‡РёРєР°) Рё РџРѕРєСѓРїР°С‚РµР»СЏ (РєР»РёРµРЅС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ)
TOPICS: РћС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р‘Р°РЅРєР° (Р�СЃРїРѕР»РЅРёС‚РµР»СЏ) Р·Р° СЃРїРѕСЂС‹ РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј (Р—Р°РєР°Р·С‡РёРєРѕРј) Рё РџРѕРєСѓРїР°С‚РµР»РµРј (РљР»РёРµРЅС‚ Р—Р°РєР°Р·С‡РёРєР°)
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏРј, РІРѕР·РЅРёРєР°СЋС‰РёРј РјРµР¶РґСѓ РџСЂРµРґРїСЂРёСЏС‚РёРµРј Рё РџРѕРєСѓРїР°С‚РµР»РµРј РІРѕ РІСЃРµС… СЃР»СѓС‡Р°СЏС…, РєРѕРіРґР° С‚Р°РєРёРµ СЃРїРѕСЂС‹ Рё СЂР°Р·РЅРѕРіР»Р°СЃРёСЏ РЅРµ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє РїСЂРµРґРјРµС‚Сѓ Р”РѕРіРѕРІРѕСЂР°, Р° С‚Р°РєР¶Рµ РїРѕ СЃРїРѕСЂР°Рј РІ РѕС‚РЅРѕС€РµРЅРёРё РўРѕРІР°СЂРѕРІ/СѓСЃР»СѓРі, РѕРїР»Р°С‡РµРЅРЅС‹С… СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РљР°СЂС‚С‹ / РµРµ СЂРµРєРІРёР·РёС‚РѕРІ / NFРЎ-РєР°СЂС‚С‹ / SberPay / РџР»Р°С‚Рё QR / РџР»Р°С‚РµР¶РЅРѕРіРѕ СЃС‡РµС‚Р°.
---END---
MATRIX_ID: 7.9
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё Р·Р°РґРµСЂР¶РєР°С… РїРµСЂРµРІРѕРґРѕРІ Р±РµР· СЃРІРѕРµР№ РІРёРЅС‹
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєРё РїРµСЂРµРІРѕРґР° РґРµРЅРµР¶РЅС‹С… СЃСЂРµРґСЃС‚РІ РЅР° СЃС‡РµС‚ РџСЂРµРґРїСЂРёСЏС‚РёСЏ, РµСЃР»Рё Р·Р°РґРµСЂР¶РєРё РїСЂРѕРёР·РѕС€Р»Рё РЅРµ РїРѕ РІРёРЅРµ Р‘Р°РЅРєР°.
---END---
MATRIX_ID: 7.10
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РЅРµ РЅРµСЃС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РІ СЃРІСЏР·Рё СЃ РґРµР№СЃС‚РІРёРµРј Рё Р±РµР·РґРµР№СЃС‚РІРёРµРј С‚СЂРµС‚СЊРёС… Р»РёС†
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµРёСЃРїРѕР»РЅРµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°, РѕР±СѓСЃР»РѕРІР»РµРЅРЅРѕРµ РґРµР№СЃС‚РІРёСЏРјРё РёР»Рё Р±РµР·РґРµР№СЃС‚РІРёСЏРјРё С‚СЂРµС‚СЊРёС… Р»РёС†, РІ С‚РѕРј С‡РёСЃР»Рµ СѓС‡Р°СЃС‚РЅРёРєР°РјРё РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹
---END---
MATRIX_ID: 7.11
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: Р‘Р°РЅРє РѕСЃРІРѕР±РѕР¶РґР°РµС‚СЃСЏ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° Р·Р°РґРµСЂР¶РєСѓ РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ РІ СЃР»СѓС‡Р°Рµ РёРЅРёС†РёРёСЂРѕРІР°РЅРёСЏ РёРј СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ РѕРїРµСЂР°С†РёР№
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РЅРµСЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РїРµСЂРµС‡РёСЃР»РµРЅРёРµ СЃСѓРјРј РћРїРµСЂР°С†РёР№ РїРѕ РїСЂРёС‡РёРЅРµ РїСЂРѕРІРµРґРµРЅРёСЏ СЂР°СЃСЃР»РµРґРѕРІР°РЅРёСЏ Р‘Р°РЅРєРѕРј РїСЂРё РїРѕРґРѕР·СЂРµРЅРёРё РЅР° РїСЂРѕРІРµРґРµРЅРёРµ РћРїРµСЂР°С†РёРё СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР°
---END---
MATRIX_ID: 7.12
REQUIRED: optional
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±С‰РёРµ СЃР»РѕРІР° Рѕ С‚РѕРј, С‡С‚Рѕ Р±Р°РЅРє РѕСЃРІРѕР±РѕР¶РґРµРЅ РѕС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїСЂРё РїСЂРµРІС‹С€РµРЅРёРё Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ Р‘Р°РЅРє РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РІ СЃР»СѓС‡Р°Рµ РїСЂРµРІС‹С€РµРЅРёСЏ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅРѕР№ Р¦РµРЅС‹ Р”РѕРіРѕРІРѕСЂР°
---END---
MATRIX_ID: 7.13
REQUIRED: mandatory
PRODUCT: internet_acquiring
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅС‹Рµ РѕРїРµСЂР°С†РёРё РЅР° Р РµСЃСѓСЂСЃРµ
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµРєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РїСЂРѕРІРµРґРµРЅРЅС‹С… РћРїРµСЂР°С†РёР№, СЃРѕРІРµСЂС€РµРЅРЅС‹С… РЅР° Р РµСЃСѓСЂСЃРµ, РІ СЃР»СѓС‡Р°Рµ РЅРµРІС‹РїРѕР»РЅРµРЅРёСЏ Рї. 4.2.21.1 Р”РѕРіРѕРІРѕСЂР°
---END---
MATRIX_ID: 7.14
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±С‰РµРµ СѓС‚РІРµСЂР¶РґРµРЅРёРµ Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ РІ РЎРџР­Рџ
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РІСЃРµ РґРµР№СЃС‚РІРёСЏ, РѕСЃСѓС‰РµСЃС‚РІР»СЏРµРјС‹Рµ РџСЂРµРґРїСЂРёСЏС‚РёРµРј/РўРЎРў РІ РЎРџР­Рџ
---END---
MATRIX_ID: 7.15
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅРµСЃРµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ РіРѕРІРѕСЂРёС‚СЃСЏ РїСЂРѕ РЅРµСЃРµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё Р·Р° РґРµР№СЃС‚РІРёСЏ РїРµСЂСЃРѕРЅР°Р»Р°, Р·РЅР°С‡РёС‚ СЌС‚РѕС‚ РїСѓРЅРєС‚ РЅРµ РѕС‚РЅРѕСЃРёС‚СЃСЏ Рє РґР°РЅРЅРѕРјСѓ
TOPICS: РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ РїРµСЂСЃРѕРЅР°Р»Р° СѓСЃР»РѕРІРёР№ РґРѕРіРѕРІРѕСЂР° | РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёСЏ РїРµСЂСЃРѕРЅР°Р»Р° РёРЅСЃС‚СЂСѓРєС†РёР№ Р‘Р°РЅРєР°
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РїРѕР»РЅРѕСЃС‚СЊСЋ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РґРµР№СЃС‚РІРёСЏ СЃРІРѕРµРіРѕ РїРµСЂСЃРѕРЅР°Р»Р°, СЃРІСЏР·Р°РЅРЅС‹Рµ СЃ РЅР°СЂСѓС€РµРЅРёРµРј СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° Рё РёРЅСЃС‚СЂСѓРєС‚РёРІРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹С… Р‘Р°РЅРєРѕРј
---END---
MATRIX_ID: 7.16
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: 
TOPICS: РћР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РЅРµ СЃРѕРІРµСЂС€Р°С‚СЊ РєРѕСЂСЂСѓРїС†РёРѕРЅРЅС‹С… Рё РёРЅС‹С… РїСЂРѕС‚РёРІРѕР·Р°РєРѕРЅРЅС‹С… РґРµР№СЃС‚РІРёР№ РїСЂРё Р»СЋР±С‹С… РѕРїРµСЂР°С†РёСЏС… РїРѕ РґРѕРіРѕРІРѕСЂСѓ
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРё Р·Р°РєР»СЋС‡РµРЅРёРё, РёСЃРїРѕР»РЅРµРЅРёРё, РёР·РјРµРЅРµРЅРёРё Рё СЂР°СЃС‚РѕСЂР¶РµРЅРёРё Р”РѕРіРѕРІРѕСЂР° РЎС‚РѕСЂРѕРЅС‹ РїСЂРёРЅРёРјР°СЋС‚ РЅР° СЃРµР±СЏ РѕР±СЏР·Р°С‚РµР»СЊСЃС‚РІРѕ РЅРµ РѕСЃСѓС‰РµСЃС‚РІР»СЏС‚СЊ РґРµР№СЃС‚РІРёР№, РєРІР°Р»РёС„РёС†РёСЂСѓРµРјС‹С… РїСЂРёРјРµРЅРёРјС‹Рј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІРѕРј РєР°Рє В«РєРѕСЂСЂСѓРїС†РёСЏВ» , Р° С‚Р°РєР¶Рµ РёРЅС‹С… РґРµР№СЃС‚РІРёР№ (Р±РµР·РґРµР№СЃС‚РІРёСЏ), РЅР°СЂСѓС€Р°СЋС‰РёС… С‚СЂРµР±РѕРІР°РЅРёСЏ РїСЂРёРјРµРЅРёРјРѕРіРѕ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР°, РїСЂРёРјРµРЅРёРјС‹С… РЅРѕСЂРј РјРµР¶РґСѓРЅР°СЂРѕРґРЅРѕРіРѕ РїСЂР°РІР° РІ РѕР±Р»Р°СЃС‚Рё РїСЂРѕС‚РёРІРѕРґРµР№СЃС‚РІРёСЏ РєРѕСЂСЂСѓРїС†РёРё
---END---
MATRIX_ID: 7.17
REQUIRED: mandatory
PRODUCT: common
LOT: common
TERMINAL: common
PAYMENT: common
MAIN_IDEA: Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹  РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ Р±С‹Р»Рѕ СЃСѓР¶РµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё.
TOPICS: РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІСѓ Р Р¤ | РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕС‚РІРµС‡Р°РµС‚ Р·Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ РЅРѕСЂРјР°С‚РёРІРЅС‹Рј Р°РєС‚Р°Рј Р‘Р°РЅРєР° Р РѕСЃСЃРёРё | РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·Р°РЅРѕ СЃРѕР±Р»СЋРґР°С‚СЊ РїСЂР°РІРёР»Р° РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ РІ С‡Р°СЃС‚Рё РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ | РћР±С‰РёРµ СЃР»РѕРІР° РїСЂРѕ С‚Рѕ, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РЅР°СЂСѓС€РµРЅРёРµ СѓСЃР»РѕРІРёР№ Р”РѕРіРѕРІРѕСЂР° РѕС‚РЅРѕСЃРёС‚РµР»СЊРЅРѕ РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№
ENRICHED: Р РђР—Р”Р•Р› 7 В«РћРўР’Р•РўРЎРўР’Р•РќРќРћРЎРўР¬ РЎРўРћР РћРќВ» в†’ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµСЃРµС‚ РїРѕР»РЅСѓСЋ С„РёРЅР°РЅСЃРѕРІСѓСЋ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ РїРµСЂРµРґ Р‘Р°РЅРєРѕРј РІ СЃР»СѓС‡Р°Рµ РЅРµСЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ РїСЂРѕРІРµРґРµРЅРЅС‹С… РџРѕРІС‚РѕСЂСЏСЋС‰РёС…СЃСЏ РїР»Р°С‚РµР¶РµР№ С‚СЂРµР±РѕРІР°РЅРёСЏРј Р·Р°РєРѕРЅРѕРґР°С‚РµР»СЊСЃС‚РІР° Р РѕСЃСЃРёР№СЃРєРѕР№ Р¤РµРґРµСЂР°С†РёРё, РІ С‚РѕРј С‡РёСЃР»Рµ РЅРѕСЂРјР°С‚РёРІРЅС‹С… Р°РєС‚РѕРІ Р‘Р°РЅРєР° Р РѕСЃСЃРёРё, РїСЂР°РІРёР» РџР»Р°С‚РµР¶РЅРѕР№ СЃРёСЃС‚РµРјС‹ Рё (РёР»Рё) Р”РѕРіРѕРІРѕСЂР°
---END---

[Command succeeded with exit code 0]
AI: The encoding is corrupted in the output. Let me read the matrix file directly for the batch range. This is a large batch (78 matrix IDs). Let me now read the contract text and the existing working files to understand what's already been done.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 100}, 'id': 'call_00_xSR3GG2bPgoCi9tydQtl3610', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '/outputs/working/*.json'}, 'id': 'call_01_7c7dgncKxj77pT1nyTsg1810', 'type': 'tool_call'}]
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
Tool: ['/outputs/working/clause_index.json', '/outputs/working/contract_locator_registry.json', '/outputs/working/contract_product_profile.json', '/outputs/working/legal_propositions.json', '/outputs/working/source_preflight.json']
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 100, 'limit': 200}, 'id': 'call_00_FEe5gLCNbJTocFHojvaH9099', 'type': 'tool_call'}]
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
AI: Now I have a good understanding of the contract structure. This is a large batch (78 matrix IDs from 5.1.1.6 to 7.17). Let me now read the existing working files and the validate_fragment.py script to understand the expected format.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/source_preflight.json'}, 'id': 'call_00_pDX53MrNiMvW46s89y3s6073', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '/skills/acquiring-discrepancy-analysis/scripts/*.py'}, 'id': 'call_01_Py5jd7lBfeT4Dru9HVba3797', 'type': 'tool_call'}]
Tool:      1	{
     2	  "path": "inputs\\contract.txt",
     3	  "valid": true,
     4	  "contract_numbering_valid": true,
     5	  "numbered_clause_count": 243,
     6	  "deep_clause_count": 187,
     7	  "top_level_sections": [
     8	    "1",
     9	    "10",
    10	    "11",
    11	    "12",
    12	    "13",
    13	    "2",
    14	    "3",
    15	    "354340",
    16	    "4",
    17	    "5",
    18	    "6",
    19	    "7",
    20	    "8",
    21	    "9"
    22	  ],
    23	  "broken_zero_ids": [],
    24	  "duplicate_ids": [
    25	    "1",
    26	    "1.1",
    27	    "1.2",
    28	    "1.3",
    29	    "10",
    30	    "2",
    31	    "3",
    32	    "4",
    33	    "5",
    34	    "6",
    35	    "7",
    36	    "8"
    37	  ],
    38	  "warnings": []
    39	}
Tool: ['/skills/acquiring-discrepancy-analysis/scripts/bootstrap_source_artifacts.py', '/skills/acquiring-discrepancy-analysis/scripts/export_review_xlsx.py', '/skills/acquiring-discrepancy-analysis/scripts/extract_docx_numbered.py', '/skills/acquiring-discrepancy-analysis/scripts/finalize_discrepancy_json.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_coverage_ledger.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_source_numbering.py', '/skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py']
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py', 'limit': 100}, 'id': 'call_00_9jGWE83H7eRoLmX4hW9h9882', 'type': 'tool_call'}]
Tool:      1	"""Validate a subagent discrepancy-analysis fragment before merge.
     2	
     3	This helper is mechanical. It checks locator integrity, fragment coverage, and
     4	structural conflicts only; it does not decide legal analogues or statuses.
     5	"""
     6	
     7	from __future__ import annotations
     8	
     9	import argparse
    10	import json
    11	import re
    12	from pathlib import Path
    13	from typing import Any
    14	
    15	
    16	FORBIDDEN_MECHANICAL_REASON_RE = re.compile(
    17	    r"\b(auto[-\s]?matched|match\s+score|similarity\s+score|keyword\s+match|"
    18	    r"keyword\s+overlap|token\s+overlap|high\s+similarity|same\s+section|"
    19	    r"score\s*[=:]|threshold\s*[=:])\b",
    20	    re.I,
    21	)
    22	
    23	
    24	def read_json(path: Path) -> Any:
    25	    return json.loads(path.read_text(encoding="utf-8-sig"))
    26	
    27	
    28	def as_list(value: Any) -> list[Any]:
    29	    if value is None:
    30	        return []
    31	    return value if isinstance(value, list) else [value]
    32	
    33	
    34	def text(value: Any) -> str:
    35	    return str(value or "").strip()
    36	
    37	
    38	def mechanical_reason(value: Any) -> bool:
    39	    return bool(FORBIDDEN_MECHANICAL_REASON_RE.search(text(value)))
    40	
    41	
    42	def add_mechanical_reason_errors(errors: list[str], path: str, *values: Any) -> None:
    43	    for value in values:
    44	        if mechanical_reason(value):
    45	            errors.append(f"{path}:mechanical_reason_not_allowed")
    46	            return
    47	
    48	
    49	def load_registry(path: Path) -> tuple[set[str], set[str]]:
    50	    data = read_json(path)
    51	    if not isinstance(data, list):
    52	        raise ValueError("contract locator registry must be a JSON array")
    53	    final_allowed: set[str] = set()
    54	    evidence_allowed: set[str] = set()
    55	    for row in data:
    56	        if not isinstance(row, dict):
    57	            continue
    58	        locator = text(row.get("locator"))
    59	        if not locator:
    60	            continue
    61	        evidence_allowed.add(locator)
    62	        if row.get("final_allowed") is True:
    63	            final_allowed.add(locator)
    64	    return final_allowed, evidence_allowed
    65	
    66	
    67	def load_assigned_ids(args: argparse.Namespace) -> set[str]:
    68	    assigned: set[str] = set()
    69	    if args.assigned_matrix_ids:
    70	        assigned.update(
    71	            item.strip()
    72	            for item in re.split(r"[,;\s]+", args.assigned_matrix_ids)
    73	            if item.strip()
    74	        )
    75	    if args.assigned_matrix_file:
    76	        data = read_json(args.assigned_matrix_file)
    77	        if isinstance(data, list):
    78	            assigned.update(text(item) for item in data if text(item))
    79	        elif isinstance(data, dict):
    80	            for key in ("assigned_ids", "assigned_matrix_ids", "matrix_ids"):
    81	                values = data.get(key)
    82	                if isinstance(values, list):
    83	                    assigned.update(text(item) for item in values if text(item))
    84	    return assigned
    85	
    86	
    87	def reject_suspicious_locator(locator: str) -> str | None:
    88	    if not locator:
    89	        return "empty"
    90	    lowered = locator.lower()
    91	    if "(" in locator or ")" in locator:
    92	        return "parenthetical_or_composite_id"
    93	    if re.search(r"(приложение|appendix)[_\s-]*\d+[_\s-]*п", lowered, re.I):
    94	        return "derived_appendix_clause_id"
    95	    if lowered.startswith(("приложение_", "appendix_")):
    96	        return "derived_appendix_id"
    97	    if "_" in locator and not re.fullmatch(r"\d+(?:\.\d+)*", locator):
    98	        return "semantic_suffix_or_internal_id"
    99	    return None
   100	
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py', 'offset': 100, 'limit': 300}, 'id': 'call_00_3U7mPrtvbDefdxOep1LP4006', 'type': 'tool_call'}]
Tool:    101	
   102	def add_final_locator_errors(
   103	    errors: list[str],
   104	    path: str,
   105	    values: Any,
   106	    final_allowed: set[str],
   107	    evidence_allowed: set[str],
   108	) -> None:
   109	    for value in as_list(values):
   110	        locator = text(value)
   111	        suspicious = reject_suspicious_locator(locator)
   112	        if suspicious:
   113	            errors.append(f"{path}:invalid_final_locator:{suspicious}:{locator}")
   114	            continue
   115	        if locator not in final_allowed:
   116	            if locator in evidence_allowed:
   117	                errors.append(f"{path}:evidence_only_used_as_contract_id:{locator}")
   118	            else:
   119	                errors.append(f"{path}:unknown_contract_locator:{locator}")
   120	
   121	
   122	def add_evidence_locator_errors(
   123	    errors: list[str],
   124	    path: str,
   125	    values: Any,
   126	    evidence_allowed: set[str],
   127	) -> None:
   128	    for value in as_list(values):
   129	        locator = text(value)
   130	        if locator and locator not in evidence_allowed:
   131	            errors.append(f"{path}:unknown_evidence_locator:{locator}")
   132	
   133	
   134	def validate_fragment(
   135	    fragment: dict[str, Any],
   136	    final_allowed: set[str],
   137	    evidence_allowed: set[str],
   138	    assigned_matrix_ids: set[str],
   139	) -> dict[str, Any]:
   140	    errors: list[str] = []
   141	    warnings: list[str] = []
   142	    processed_matrix_ids: set[str] = set()
   143	    linked_contract_ids: set[str] = set()
   144	    extra_contract_ids: set[str] = set()
   145	
   146	    for idx, link in enumerate(fragment.get("links", []) or []):
   147	        if not isinstance(link, dict):
   148	            errors.append(f"links[{idx}]:not_object")
   149	            continue
   150	        relationship = text(link.get("relationship"))
   151	        if relationship not in {"aligned", "deviation"}:
   152	            errors.append(f"links[{idx}]:invalid_relationship:{relationship}")
   153	        add_mechanical_reason_errors(
   154	            errors,
   155	            f"links[{idx}]",
   156	            link.get("status_reason"),
   157	            link.get("legal_topic"),
   158	            link.get("coverage"),
   159	        )
   160	        matrix_ids = {text(item) for item in as_list(link.get("matrix_ids")) if text(item)}
   161	        processed_matrix_ids.update(matrix_ids)
   162	        contract_ids = {text(item) for item in as_list(link.get("contract_ids")) if text(item)}
   163	        linked_contract_ids.update(contract_ids)
   164	        add_final_locator_errors(
   165	            errors,
   166	            f"links[{idx}].contract_ids",
   167	            link.get("contract_ids"),
   168	            final_allowed,
   169	            evidence_allowed,
   170	        )
   171	        add_final_locator_errors(
   172	            errors,
   173	            f"links[{idx}].candidate_contract_ids",
   174	            link.get("candidate_contract_ids"),
   175	            final_allowed,
   176	            evidence_allowed,
   177	        )
   178	        add_evidence_locator_errors(
   179	            errors,
   180	            f"links[{idx}].evidence_locators",
   181	            link.get("evidence_locators"),
   182	            evidence_allowed,
   183	        )
   184	        candidate_ids = {text(item) for item in as_list(link.get("candidate_contract_ids")) if text(item)}
   185	        if not isinstance(link.get("covered_elements"), list):
   186	            errors.append(f"links[{idx}]:missing_covered_elements")
   187	        uncovered_elements = link.get("uncovered_elements")
   188	        if not isinstance(uncovered_elements, list):
   189	            errors.append(f"links[{idx}]:missing_uncovered_elements")
   190	            uncovered_elements = []
   191	        if not isinstance(link.get("candidate_contract_ids"), list):
   192	            errors.append(f"links[{idx}]:missing_candidate_contract_ids")
   193	        if candidate_ids and not contract_ids <= candidate_ids:
   194	            errors.append(f"links[{idx}]:contract_ids_not_subset_of_candidate_contract_ids")
   195	        if link.get("candidate_search_exhausted") is not True:
   196	            errors.append(f"links[{idx}]:candidate_search_not_exhausted")
   197	        search_scope = text(link.get("search_scope"))
   198	        if search_scope not in {"full_contract", "targeted_domain"}:
   199	            errors.append(f"links[{idx}]:invalid_search_scope:{search_scope}")
   200	        discrepancies = link.get("discrepancies")
   201	        if relationship == "aligned":
   202	            if uncovered_elements:
   203	                errors.append(f"links[{idx}]:aligned_with_uncovered_elements")
   204	            if discrepancies not in ([], None):
   205	                errors.append(f"links[{idx}]:aligned_with_discrepancies")
   206	        if relationship == "deviation":
   207	            if search_scope != "full_contract":
   208	                errors.append(f"links[{idx}]:deviation_without_full_contract_search")
   209	            if not isinstance(discrepancies, list) or not discrepancies:
   210	                errors.append(f"links[{idx}]:deviation_without_discrepancies")
   211	            else:
   212	                for didx, discrepancy in enumerate(discrepancies):
   213	                    if not isinstance(discrepancy, dict):
   214	                        errors.append(f"links[{idx}].discrepancies[{didx}]:not_object")
   215	                        continue
   216	                    if not discrepancy.get("type") or not discrepancy.get("description") or not discrepancy.get("risk"):
   217	                        errors.append(f"links[{idx}].discrepancies[{didx}]:missing_required_fields")
   218	                    add_mechanical_reason_errors(
   219	                        errors,
   220	                        f"links[{idx}].discrepancies[{didx}]",
   221	                        discrepancy.get("description"),
   222	                        discrepancy.get("risk"),
   223	                    )
   224	        for ridx, rejected in enumerate(link.get("rejected_contract_ids", []) or []):
   225	            if isinstance(rejected, dict):
   226	                add_final_locator_errors(
   227	                    errors,
   228	                    f"links[{idx}].rejected_contract_ids[{ridx}].contract_id",
   229	                    rejected.get("contract_id"),
   230	                    final_allowed,
   231	                    evidence_allowed,
   232	                )
   233	                if not text(rejected.get("reason")):
   234	                    errors.append(f"links[{idx}].rejected_contract_ids[{ridx}]:missing_reason")
   235	                add_mechanical_reason_errors(
   236	                    errors,
   237	                    f"links[{idx}].rejected_contract_ids[{ridx}]",
   238	                    rejected.get("reason"),
   239	                )
   240	            else:
   241	                errors.append(f"links[{idx}].rejected_contract_ids[{ridx}]:not_object")
   242	
   243	    for idx, row in enumerate(fragment.get("unmatched_matrix", []) or []):
   244	        if not isinstance(row, dict):
   245	            errors.append(f"unmatched_matrix[{idx}]:not_object")
   246	            continue
   247	        matrix_id = text(row.get("matrix_id"))
   248	        if matrix_id:
   249	            processed_matrix_ids.add(matrix_id)
   250	        if row.get("status") != "missing_in_contract":
   251	            errors.append(f"unmatched_matrix[{idx}]:invalid_status")
   252	        add_mechanical_reason_errors(
   253	            errors,
   254	            f"unmatched_matrix[{idx}]",
   255	            row.get("risk"),
   256	            row.get("reason"),
   257	            row.get("status_reason"),
   258	        )
   259	        if not text(row.get("requirement")) or not text(row.get("risk")):
   260	            errors.append(f"unmatched_matrix[{idx}]:missing_requirement_or_risk")
   261	        if not isinstance(row.get("covered_elements"), list):
   262	            errors.append(f"unmatched_matrix[{idx}]:missing_covered_elements")
   263	        uncovered_elements = row.get("uncovered_elements")
   264	        if not isinstance(uncovered_elements, list) or not uncovered_elements:
   265	            errors.append(f"unmatched_matrix[{idx}]:missing_uncovered_elements")
   266	        if not isinstance(row.get("candidate_contract_ids"), list):
   267	            errors.append(f"unmatched_matrix[{idx}]:missing_candidate_contract_ids")
   268	        if row.get("candidate_search_exhausted") is not True:
   269	            errors.append(f"unmatched_matrix[{idx}]:candidate_search_not_exhausted")
   270	        if row.get("search_scope") != "full_contract":
   271	            errors.append(f"unmatched_matrix[{idx}]:search_scope_not_full_contract")
   272	        add_final_locator_errors(
   273	            errors,
   274	            f"unmatched_matrix[{idx}].candidate_contract_ids",
   275	            row.get("candidate_contract_ids"),
   276	            final_allowed,
   277	            evidence_allowed,
   278	        )
   279	        add_evidence_locator_errors(
   280	            errors,
   281	            f"unmatched_matrix[{idx}].evidence_locators",
   282	            row.get("evidence_locators"),
   283	            evidence_allowed,
   284	        )
   285	        for ridx, rejected in enumerate(row.get("rejected_candidates", []) or []):
   286	            if isinstance(rejected, dict):
   287	                add_final_locator_errors(
   288	                    errors,
   289	                    f"unmatched_matrix[{idx}].rejected_candidates[{ridx}].contract_id",
   290	                    rejected.get("contract_id"),
   291	                    final_allowed,
   292	                    evidence_allowed,
   293	                )
   294	                if not text(rejected.get("reason")):
   295	                    errors.append(f"unmatched_matrix[{idx}].rejected_candidates[{ridx}]:missing_reason")
   296	                add_mechanical_reason_errors(
   297	                    errors,
   298	                    f"unmatched_matrix[{idx}].rejected_candidates[{ridx}]",
   299	                    rejected.get("reason"),
   300	                )
   301	            else:
   302	                warnings.append(f"unmatched_matrix[{idx}].rejected_candidates[{ridx}]:not_object")
   303	
   304	    for idx, row in enumerate(fragment.get("unmatched_contract", []) or []):
   305	        if not isinstance(row, dict):
   306	            errors.append(f"unmatched_contract[{idx}]:not_object")
   307	            continue
   308	        contract_id = text(row.get("contract_id"))
   309	        if contract_id:
   310	            extra_contract_ids.add(contract_id)
   311	        if row.get("status") != "extra_in_contract":
   312	            errors.append(f"unmatched_contract[{idx}]:invalid_status")
   313	        if not text(row.get("risk")) or not text(row.get("materiality_reason")):
   314	            errors.append(f"unmatched_contract[{idx}]:missing_risk_or_materiality_reason")
   315	        add_mechanical_reason_errors(
   316	            errors,
   317	            f"unmatched_contract[{idx}]",
   318	            row.get("risk"),
   319	            row.get("materiality_reason"),
   320	        )
   321	        add_final_locator_errors(
   322	            errors,
   323	            f"unmatched_contract[{idx}].contract_id",
   324	            contract_id,
   325	            final_allowed,
   326	            evidence_allowed,
   327	        )
   328	        add_evidence_locator_errors(
   329	            errors,
   330	            f"unmatched_contract[{idx}].evidence_locators",
   331	            row.get("evidence_locators"),
   332	            evidence_allowed,
   333	        )
   334	
   335	    for idx, atom in enumerate(fragment.get("atomic_links", []) or []):
   336	        if not isinstance(atom, dict):
   337	            errors.append(f"atomic_links[{idx}]:not_object")
   338	            continue
   339	        add_mechanical_reason_errors(
   340	            errors,
   341	            f"atomic_links[{idx}]",
   342	            atom.get("coverage"),
   343	        )
   344	        add_final_locator_errors(
   345	            errors,
   346	            f"atomic_links[{idx}].contract_id",
   347	            atom.get("contract_id"),
   348	            final_allowed,
   349	            evidence_allowed,
   350	        )
   351	        matrix_id = text(atom.get("matrix_id"))
   352	        if matrix_id:
   353	            processed_matrix_ids.add(matrix_id)
   354	
   355	    coverage = fragment.get("coverage_ledger")
   356	    if isinstance(coverage, dict):
   357	        for idx, row in enumerate(coverage.get("matrix", []) or []):
   358	            if isinstance(row, dict):
   359	                matrix_id = text(row.get("matrix_id"))
   360	                if matrix_id:
   361	                    processed_matrix_ids.add(matrix_id)
   362	        for idx, row in enumerate(coverage.get("contract", []) or []):
   363	            if isinstance(row, dict):
   364	                add_final_locator_errors(
   365	                    errors,
   366	                    f"coverage_ledger.contract[{idx}].contract_id",
   367	                    row.get("contract_id"),
   368	                    final_allowed,
   369	                    evidence_allowed,
   370	                )
   371	
   372	    duplicate_closure = sorted(linked_contract_ids & extra_contract_ids)
   373	    for contract_id in duplicate_closure:
   374	        errors.append(f"contract_linked_and_extra:{contract_id}")
   375	
   376	    if assigned_matrix_ids:
   377	        missing = sorted(assigned_matrix_ids - processed_matrix_ids)
   378	        extra = sorted(processed_matrix_ids - assigned_matrix_ids)
   379	        if missing:
   380	            errors.append(f"assigned_matrix_ids_not_processed:{missing[:20]}")
   381	        if extra:
   382	            warnings.append(f"processed_matrix_ids_outside_assignment:{extra[:20]}")
   383	
   384	    return {
   385	        "valid": not errors,
   386	        "error_count": len(errors),
   387	        "warning_count": len(warnings),
   388	        "errors": errors,
   389	        "warnings": warnings,
   390	        "counts": {
   391	            "processed_matrix_ids": len(processed_matrix_ids),
   392	            "linked_contract_ids": len(linked_contract_ids),
   393	            "extra_contract_ids": len(extra_contract_ids),
   394	        },
   395	    }
   396	
   397	
   398	def main() -> None:
   399	    parser = argparse.ArgumentParser()
   400	    parser.add_argument("fragment", type=Path)
AI: Now I have a thorough understanding of the methodology and validation requirements. This is a very large batch. Let me now systematically work through the matrix IDs. Given the size, I'll need to be efficient. Let me first read the matrix entries directly from the file for the batch range, then read the contract sections that are relevant.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read all matrix entries 5.1.1.6 through 7.17 from inputs/matrix.json', 'status': 'completed'}, {'content': 'Read contract text for relevant sections (clauses 5-7 and related)', 'status': 'completed'}, {'content': 'Read existing legal_propositions.json for matrix and contract entries in range', 'status': 'in_progress'}, {'content': 'Read existing coverage_ledger.json and previous batch outputs for context', 'status': 'pending'}, {'content': 'Perform legal comparison for each matrix id in batch range', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, and coverage_ledger fragments', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Return final fragment', 'status': 'pending'}]}, 'id': 'call_00_3w8xHaah7FOHkKPXo1NZ2724', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read all matrix entries 5.1.1.6 through 7.17 from inputs/matrix.json', 'status': 'completed'}, {'content': 'Read contract text for relevant sections (clauses 5-7 and related)', 'status': 'completed'}, {'content': 'Read existing legal_propositions.json for matrix and contract entries in range', 'status': 'in_progress'}, {'content': 'Read existing coverage_ledger.json and previous batch outputs for context', 'status': 'pending'}, {'content': 'Perform legal comparison for each matrix id in batch range', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, and coverage_ledger fragments', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Return final fragment', 'status': 'pending'}]
AI: Let me now read the matrix entries directly from the file for the batch range. I'll use a Python script to extract them properly.[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/inputs/matrix.json\', \'r\', encoding=\'utf-8\') as f:\n    matrix = json.load(f)\nbatch = matrix[70:148]\n# Write to a temp file for reading\nwith open(\'/outputs/working/batch3_matrix.json\', \'w\', encoding=\'utf-8\') as f:\n    json.dump(batch, f, ensure_ascii=False, indent=2)\nprint(\'Done, wrote\', len(batch), \'entries\')\n"'}, 'id': 'call_00_aglweCWZfoFTmRO1ROWV5940', 'type': 'tool_call'}]
Tool: Done, wrote 78 entries

[Command succeeded with exit code 0]
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch3_matrix.json', 'limit': 200}, 'id': 'call_00_MC0mihqPdptVYGpTFZnN5382', 'type': 'tool_call'}]
Tool:      1	[
     2	  {
     3	    "number": "5.1.1.6",
     4	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Удерживать из сумм, подлежащих перечислению Предприятию по Договору, следующие суммы: → Суммы штрафов в случае невозврата Электронных терминалов/Смарт-терминалов Банка в соответствии с п. 4.2.20.7 Договора.",
     5	    "required_type": "mandatory",
     6	    "main_idea": "Возможность удержания штрафов за невозврат терминалов. ",
     7	    "only_for_product": "trade_acquiring",
     8	    "only_for_lot": "common",
     9	    "only_for_terminal": "common",
    10	    "topics": [
    11	      "Банк имеет право удерживать суммы штрафов за невозврат Электронных терминалов/Смарт-терминалов"
    12	    ],
    13	    "payment_method": "common"
    14	  },
    15	  {
    16	    "number": "5.1.2",
    17	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае возникновения у Предприятия задолженности перед Банком приостановить проведение Авторизации до момента полного погашения задолженности.",
    18	    "required_type": "mandatory",
    19	    "main_idea": "",
    20	    "only_for_product": "common",
    21	    "only_for_lot": "common",
    22	    "only_for_terminal": "common",
    23	    "topics": [
    24	      "Банк вправе приостанавливать авторизацию при наличии задолженности у Предприятия",
    25	      "Приостановка допускается до полного погашения задолженности Предприятием"
    26	    ],
    27	    "payment_method": "common"
    28	  },
    29	  {
    30	    "number": "5.1.3",
    31	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, списывать без дополнительного распоряжения Предприятия (на условиях заранее данного акцепта, предоставленного Банку Предприятием в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг) денежные средства с расчетного счета Предприятия, открытого в Банке. ",
    32	    "required_type": "mandatory",
    33	    "main_idea": "",
    34	    "only_for_product": "common",
    35	    "only_for_lot": "common",
    36	    "only_for_terminal": "common",
    37	    "topics": [
    38	      "списание средств без дополнительного распоряжения",
    39	      "условие заранее данного акцепта",
    40	      "основание - заявление предприятия о проведении расчетов"
    41	    ],
    42	    "payment_method": "common"
    43	  },
    44	  {
    45	    "number": "5.1.4",
    46	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → При невозможности удержать суммы, указанные в п. 5.1.1 Договора, из сумм, подлежащих последующему перечислению Предприятию, Банк выставляет счет на оплату или платежное требование о списании денежных средств к расчетному счету Предприятия № --------------------------- в ----------------------- (наименование Банка, котором у Предприятия открыт счет). ",
    47	    "required_type": "mandatory",
    48	    "main_idea": "",
    49	    "only_for_product": "common",
    50	    "only_for_lot": "common",
    51	    "only_for_terminal": "common",
    52	    "topics": [
    53	      "указан номер расчетного счета Предприятия",
    54	      "указано наименование Банка, в котором у Предприятия открыт счет"
    55	    ],
    56	    "payment_method": "common"
    57	  },
    58	  {
    59	    "number": "5.1.5",
    60	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Не возмещать Предприятию суммы Операций, проведенных с нарушением условий Договора.",
    61	    "required_type": "mandatory",
    62	    "main_idea": "",
    63	    "only_for_product": "common",
    64	    "only_for_lot": "common",
    65	    "only_for_terminal": "common",
    66	    "topics": [
    67	      "Банк имеет право не возмещать суммы операций, проведенных с нарушением условий договора"
    68	    ],
    69	    "payment_method": "common"
    70	  },
    71	  {
    72	    "number": "5.1.6",
    73	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять проверку технического состояния и порядка эксплуатации Электронных терминалов/Смарт-терминалов Банка, расположенных на территории Предприятия/ТСТ. Производить замену Электронных терминалов/Смарт-терминалов Банка, а также обновлять программное обеспечение Электронных терминалов/Смарт-терминалов, уведомив Предприятие не менее чем за 2 (два) рабочих дня до даты замены или обновления. Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения Операций, изложенный в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, без предварительного уведомления Предприятия.",
    74	    "required_type": "mandatory",
    75	    "main_idea": "",
    76	    "only_for_product": "common",
    77	    "only_for_lot": "common",
    78	    "only_for_terminal": "common",
    79	    "topics": [
    80	      "Банк имеет право проверять техническое состояние терминалов на территории предприятия",
    81	      "Банк имеет право производить замену терминалов с уведомлением заказчика за 2 рабочих дня",
    82	      "Банк имеет право обновлять ПО терминалов с уведомлением заказчика за 2 рабочих дня",
    83	      "Допускается удаленное обновление ПО терминалов без изменения порядка операций и без предварительного уведомления"
    84	    ],
    85	    "payment_method": "common"
    86	  },
    87	  {
    88	    "number": "5.1.7",
    89	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Независимо от срока действия Договора в случае выявления подозрительных или мошеннических Операций передавать информацию, в том числе осуществлять передачу данных (сведения о Предприятии/ТСТ/Ресурсе, в том числе персональные данные руководителя/представителя Предприятия, указанные в Заявлении/Информации о ТСТ) в Платежную систему МИР в целях исполнения запросов, полученных от указанной платежной системы.В случае принятия Банком решения о расторжении Договора по причине мошеннической деятельности Предприятия сообщать в Платежную систему МИР: даты заключения и расторжения Договора, а также причины расторжения Договора, иные сведения о Предприятии.",
    90	    "required_type": "mandatory",
    91	    "main_idea": "",
    92	    "only_for_product": "common",
    93	    "only_for_lot": "common",
    94	    "only_for_terminal": "common",
    95	    "topics": [
    96	      "Банк имеет право передавать информацию о предприятии при выявлении подозрительных операций",
    97	      "Банк передает данные в Платежную систему МИР при расторжении договора из-за мошенничества",
    98	      "Передаваемая информация включает дату заключения и расторжения договора, причину расторжения и другие сведения о предприятии"
    99	    ],
   100	    "payment_method": "common"
   101	  },
   102	  {
   103	    "number": "5.1.8.1",
   104	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → нарушение Предприятием условий Договора;",
   105	    "required_type": "optional",
   106	    "main_idea": "",
   107	    "only_for_product": "common",
   108	    "only_for_lot": "common",
   109	    "only_for_terminal": "common",
   110	    "topics": [
   111	      "нарушение Предприятием условий Договора является основанием для прекращения Авторизации и расторжения Договора"
   112	    ],
   113	    "payment_method": "common"
   114	  },
   115	  {
   116	    "number": "5.1.8.2",
   117	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → внесение данных Предприятия в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;",
   118	    "required_type": "optional",
   119	    "main_idea": "",
   120	    "only_for_product": "common",
   121	    "only_for_lot": "common",
   122	    "only_for_terminal": "common",
   123	    "topics": [
   124	      "внесение данных Предприятия в перечень организаций и физических лиц, причастных к экстремизму, терроризму или распространению оружия массового уничтожения является основанием для прекращения Авторизации и расторжения договора"
   125	    ],
   126	    "payment_method": "common"
   127	  },
   128	  {
   129	    "number": "5.1.8.3",
   130	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → при наличии у Банка подозрений, что Операции в ТСТ/на Ресурсе совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;",
   131	    "required_type": "optional",
   132	    "main_idea": "",
   133	    "only_for_product": "common",
   134	    "only_for_lot": "common",
   135	    "only_for_terminal": "common",
   136	    "topics": [
   137	      "Банк вправе прекратить Авторизацию при подозрении на отмывание денег или финансирование терроризма"
   138	    ],
   139	    "payment_method": "common"
   140	  },
   141	  {
   142	    "number": "5.1.8.4",
   143	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → несоответствие Ресурса Требованиям Банка к Ресурсу Предприятия;",
   144	    "required_type": "optional",
   145	    "main_idea": "",
   146	    "only_for_product": "internet_acquiring",
   147	    "only_for_lot": "common",
   148	    "only_for_terminal": "common",
   149	    "topics": [
   150	      "Банк вправе прекратить Авторизацию при несоответствии Ресурса Требованиям Банка"
   151	    ],
   152	    "payment_method": "common"
   153	  },
   154	  {
   155	    "number": "5.1.8.5",
   156	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → осуществление видов деятельности, указанных в Требованиях к Ресурсу Предприятия;",
   157	    "required_type": "optional",
   158	    "main_idea": "",
   159	    "only_for_product": "internet_acquiring",
   160	    "only_for_lot": "common",
   161	    "only_for_terminal": "common",
   162	    "topics": [
   163	      "Банк имеет право в одностороннем порядке прекратить проведение авторизации при осуществлении Заказчиком запрещенных видов деятельности согласно Требованиям к Ресурсу Предприятия"
   164	    ],
   165	    "payment_method": "common"
   166	  },
   167	  {
   168	    "number": "5.1.8.6",
   169	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → получение негативной информации о Предприятии/ТСТ /Ресурсе  от органов государственной власти РФ и/или Платежной системы;",
   170	    "required_type": "optional",
   171	    "main_idea": "",
   172	    "only_for_product": "common",
   173	    "only_for_lot": "common",
   174	    "only_for_terminal": "common",
   175	    "topics": [
   176	      "Банк имеет право прекратить проведение авторизации при получении негативной информации о предприятии от органов государственной власти",
   177	      "Банк имеет право расторгнуть договор при получении негативной информации о ресурсе от платежной системы"
   178	    ],
   179	    "payment_method": "common"
   180	  },
   181	  {
   182	    "number": "5.1.8.7",
   183	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → получение информации о мошенничестве в ТСТ /на Ресурсе ;стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов в Банк, или уведомления от Платежной системы, полученные c использованием факсимильной связи, по электронной почте (e-mail);",
   184	    "required_type": "optional",
   185	    "main_idea": "",
   186	    "only_for_product": "common",
   187	    "only_for_lot": "common",
   188	    "only_for_terminal": "common",
   189	    "topics": [
   190	      "Банк имеет право прекратить Авторизацию при получении информации о мошенничестве",
   191	      "Достаточным подтверждением мошенничества являются сведения от Банка-эмитента или Платежной системы",
   192	      "Подтверждение может быть получено по факсу или электронной почте"
   193	    ],
   194	    "payment_method": "common"
   195	  },
   196	  {
   197	    "number": "5.1.8.8",
   198	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций;",
   199	    "required_type": "optional",
   200	    "main_idea": "",
AI: Good, I can read the matrix entries properly now. Let me continue reading the rest of the batch.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/batch3_matrix.json', 'offset': 200, 'limit': 400}, 'id': 'call_00_hrUrafC9B4P2RFbiLIYF3083', 'type': 'tool_call'}]
Tool:    201	    "only_for_product": "trade_acquiring",
   202	    "only_for_lot": "common",
   203	    "only_for_terminal": "common",
   204	    "topics": [
   205	      "осуществление ремонта помещений ТСТ препятствует операциям",
   206	      "банк вправе прекратить авторизацию для ТСТ",
   207	      "банк вправе инициировать расторжение договора"
   208	    ],
   209	    "payment_method": "common"
   210	  },
   211	  {
   212	    "number": "5.1.8.9",
   213	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → ликвидация Предприятия либо возбуждение в отношении Предприятия дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)»;",
   214	    "required_type": "optional",
   215	    "main_idea": "",
   216	    "only_for_product": "common",
   217	    "only_for_lot": "common",
   218	    "only_for_terminal": "common",
   219	    "topics": [
   220	      "ликвидация Предприятия",
   221	      "возбуждение дела о банкротстве Предприятия по закону №127-ФЗ"
   222	    ],
   223	    "payment_method": "common"
   224	  },
   225	  {
   226	    "number": "5.1.8.10",
   227	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → выявление недостоверных сведений о Предприятии/ТСТ, руководителе(-ях) в информации, указанной при заключении Договора;\n",
   228	    "required_type": "optional",
   229	    "main_idea": "",
   230	    "only_for_product": "common",
   231	    "only_for_lot": "common",
   232	    "only_for_terminal": "common",
   233	    "topics": [
   234	      "выявление недостоверных сведений о Предприятии",
   235	      "выявление недостоверных сведений о ТСТ",
   236	      "выявление недостоверных сведений о руководителе Предприятия"
   237	    ],
   238	    "payment_method": "common"
   239	  },
   240	  {
   241	    "number": "5.1.8.11",
   242	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Предприятия, указанному в Информации о ТСТ;",
   243	    "required_type": "optional",
   244	    "main_idea": "",
   245	    "only_for_product": "common",
   246	    "only_for_lot": "common",
   247	    "only_for_terminal": "common",
   248	    "topics": [
   249	      "Банк имеет право прекратить проведение авторизации при несоответствии товаров/услуг роду деятельности предприятия",
   250	      "Банк имеет право в одностороннем порядке расторгнуть договор при выявленном несоответствии товаров/услуг заявленной деятельности"
   251	    ],
   252	    "payment_method": "common"
   253	  },
   254	  {
   255	    "number": "5.1.8.12",
   256	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → отсутствие операций в течение 30 (тридцати) календарных дней подряд;",
   257	    "required_type": "optional",
   258	    "main_idea": "",
   259	    "only_for_product": "common",
   260	    "only_for_lot": "common",
   261	    "only_for_terminal": "common",
   262	    "topics": [
   263	      "отсутствие операций в течение 30 календарных дней подряд является основанием для прекращения проведения авторизации и расторжения договора"
   264	    ],
   265	    "payment_method": "common"
   266	  },
   267	  {
   268	    "number": "5.1.8.13",
   269	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке прекратить проведение Авторизации для ТСТ и/или провести мероприятия по расторжению Договора при наступлении следующих событий: → исчерпание Цены Договора и/или окончание срока действия Договора, указанного в п. 10.1 Договора.",
   270	    "required_type": "optional",
   271	    "main_idea": "",
   272	    "only_for_product": "common",
   273	    "only_for_lot": "common",
   274	    "only_for_terminal": "common",
   275	    "topics": [
   276	      "исчерпание Цены Договора",
   277	      "окончание срока действия Договора"
   278	    ],
   279	    "payment_method": "common"
   280	  },
   281	  {
   282	    "number": "5.1.9",
   283	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Осуществлять дополнительные проверки проведения Операции в ТСТ, в т.ч. обращаться в Банк-эмитент для проверки правомерности Операции.",
   284	    "required_type": "mandatory",
   285	    "main_idea": "",
   286	    "only_for_product": "common",
   287	    "only_for_lot": "common",
   288	    "only_for_terminal": "common",
   289	    "topics": [
   290	      "Банк имеет право осуществлять дополнительные проверки проведения Операции в ТСТ",
   291	      "Банк имеет право обращаться в Банк-эмитент для проверки правомерности Операции"
   292	    ],
   293	    "payment_method": "common"
   294	  },
   295	  {
   296	    "number": "5.1.10",
   297	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Проводить проверку Предприятия, в т.ч. на предмет выявления мошеннических операций, предоставления Покупателям Товаров/услуг, несоответствующих роду деятельности Предприятия, указанному в Информации о ТСТ, несоблюдения Предприятием/ТСТ требований, установленных настоящим Договором к Ресурсу[1].\n[2]Проверки могут осуществляться Банком, в том числе с доступом к разделам Ресурса с ограниченным доступом, не связанным с администрированием и сопровождением (VIP, Оптовое, Клубное обслуживание, и т.п.).",
   298	    "required_type": "mandatory",
   299	    "main_idea": "",
   300	    "only_for_product": "common",
   301	    "only_for_lot": "common",
   302	    "only_for_terminal": "common",
   303	    "topics": [
   304	      "Банк имеет право проводить проверки Предприятия",
   305	      "Проверки проводятся для выявления мошенничества и несоответствия рода деятельности Предприятия информации о нем",
   306	      "Проверки включают контроль соблюдения Предприятием требований Договора к Ресурсу",
   307	      "Банк может осуществлять доступ к отдельным закрытым разделам Ресурса при проверках"
   308	    ],
   309	    "payment_method": "common"
   310	  },
   311	  {
   312	    "number": "5.1.11",
   313	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Запрашивать Документы по операциям не позднее 13 (тринадцати) месяцев с даты совершения Операции в сроки, установленные в п. 4.2.10 Договора. Для анализа спорных ситуаций Банк также может потребовать от Предприятия предоставления письменного заявления Предприятия с изложением обстоятельств проведения Операции, счетов за предоставленные Товары/услуги, товарные или кассовые чеки и другие документы, необходимые для проведения анализа обстоятельств проведения операции или претензионной работы по электронным каналам связи одним из способов, указанных в п. 2.3 Договора.",
   314	    "required_type": "mandatory",
   315	    "main_idea": "",
   316	    "only_for_product": "common",
   317	    "only_for_lot": "common",
   318	    "only_for_terminal": "common",
   319	    "topics": [
   320	      "Банк имеет право запрашивать документы по операциям",
   321	      "Банк может требовать письменное заявление предприятия с обстоятельствами проведения операции",
   322	      "Предприятие обязано предоставить счета, чеки и иные документы по требованию банка",
   323	      "Обмен документами осуществляется через электронные каналы связи согласно пункту договора"
   324	    ],
   325	    "payment_method": "common"
   326	  },
   327	  {
   328	    "number": "5.1.12",
   329	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В одностороннем порядке вносить изменения в документы, ссылки на которые даются в Договоре, путем публикации информации на Официальном сайте Банка не менее чем за 1 (один) календарный день до введения в действие указанных изменений.",
   330	    "required_type": "optional",
   331	    "main_idea": "",
   332	    "only_for_product": "common",
   333	    "only_for_lot": "common",
   334	    "only_for_terminal": "common",
   335	    "topics": [
   336	      "Банк вправе вносить изменения в связанные документы unilateral_in_one_day_right",
   337	      "Опубликование изменений осуществляется на Официальном сайте Банка"
   338	    ],
   339	    "payment_method": "common"
   340	  },
   341	  {
   342	    "number": "5.1.13",
   343	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В случае изменения реквизитов Банка, указанных в Договоре, уведомить об этом Предприятие путем размещения информации на Официальном сайте Банка. ",
   344	    "required_type": "optional",
   345	    "main_idea": "Важно именно размещение информации на сайте. Если предусмотрены иные способы уведомления, то это разногласие",
   346	    "only_for_product": "common",
   347	    "only_for_lot": "common",
   348	    "only_for_terminal": "common",
   349	    "topics": [
   350	      "Банк имеет право изменять свои реквизиты",
   351	      "Уведомление об изменении реквизитов осуществляется через Официальный сайт Банка"
   352	    ],
   353	    "payment_method": "common"
   354	  },
   355	  {
   356	    "number": "5.1.14",
   357	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → В целях получения информации по Операциям направлять запросы на адрес электронной почты Предприятия/ТСТ, указанный в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ.",
   358	    "required_type": "mandatory",
   359	    "main_idea": "",
   360	    "only_for_product": "common",
   361	    "only_for_lot": "common",
   362	    "only_for_terminal": "common",
   363	    "topics": [
   364	      "Банк имеет право направлять запросы на адрес электронной почты Предприятия",
   365	      "Адрес электронной почты указан в Заявлении Предприятия на проведение расчетов",
   366	      "Запросы направлены для получения информации по Операциям"
   367	    ],
   368	    "payment_method": "common"
   369	  },
   370	  {
   371	    "number": "5.1.15",
   372	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Отказать Предприятию в заключении Договора без объяснения причин.",
   373	    "required_type": "optional",
   374	    "main_idea": "",
   375	    "only_for_product": "common",
   376	    "only_for_lot": "common",
   377	    "only_for_terminal": "common",
   378	    "topics": [
   379	      "Банк имеет право отказать Предприятию в заключении Договора без указания причин"
   380	    ],
   381	    "payment_method": "common"
   382	  },
   383	  {
   384	    "number": "5.1.16",
   385	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Требовать от Предприятия предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства",
   386	    "required_type": "mandatory",
   387	    "main_idea": "",
   388	    "only_for_product": "common",
   389	    "only_for_lot": "common",
   390	    "only_for_terminal": "common",
   391	    "topics": [
   392	      "Банк имеет право требовать от Предприятия предоставления документов",
   393	      "Перечень требуемых документов определяется законодательством"
   394	    ],
   395	    "payment_method": "common"
   396	  },
   397	  {
   398	    "number": "5.1.17.1",
   399	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов/Смарт-терминалов, находящихся в собственности Банка, в случае если: → Торговый оборот на один Электронный терминал Банка не превышает 40 000 (сорок тысяч) рублей (для г. Москва и г. Санкт-Петербург не превышает 80 000 (восемьдесят тысяч) рублей) за последний календарный месяц (без учета в обороте Операций возврата);",
   400	    "required_type": "optional",
   401	    "main_idea": "",
   402	    "only_for_product": "trade_acquiring",
   403	    "only_for_lot": "common",
   404	    "only_for_terminal": "pos",
   405	    "topics": [
   406	      "оборот менее 40 000 руб. за месяц для регионов",
   407	      "оборот менее 80 000 руб. за месяц для Москвы и СПб"
   408	    ],
   409	    "payment_method": "common"
   410	  },
   411	  {
   412	    "number": "5.1.17.2",
   413	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк имеет право: → Банк вправе в одностороннем порядке расторгнуть Договор и потребовать возврата Электронных терминалов/Смарт-терминалов, находящихся в собственности Банка, в случае если: → 5.1.17.2. Торговый оборот на один Смарт-терминал Банка не превышает 40 000 (сорок тысяч) рублей (для г. Москва и г. Санкт-Петербург не превышает 80 000 (восемьдесят тысяч) рублей) за последний календарный месяц (без учета в обороте Операций возврата) или имеется задолженность перед Банком по плате за сервисное обслуживание/вознаграждения Банка/Операциям возврата Смарт-терминала Банка.",
   414	    "required_type": "optional",
   415	    "main_idea": "",
   416	    "only_for_product": "trade_acquiring",
   417	    "only_for_lot": "common",
   418	    "only_for_terminal": "smart",
   419	    "topics": [
   420	      "торговый оборот менее 40 000 руб. для регионов",
   421	      "торговый оборот менее 80 000 руб. для Москвы и СПб",
   422	      "наличие задолженности по сервисному обслуживанию",
   423	      "наличие задолженности по вознаграждениям банка",
   424	      "наличие задолженности по операциям возврата смарт-терминала"
   425	    ],
   426	    "payment_method": "common"
   427	  },
   428	  {
   429	    "number": "5.2.1",
   430	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечить Предприятию доступ к СПЭП для осуществления Операций.",
   431	    "required_type": "mandatory",
   432	    "main_idea": "",
   433	    "only_for_product": "internet_acquiring",
   434	    "only_for_lot": "common",
   435	    "only_for_terminal": "common",
   436	    "topics": [
   437	      "обязательство обеспечить доступ к СПЭП",
   438	      "описание порядка доступа к СПЭП"
   439	    ],
   440	    "payment_method": "common"
   441	  },
   442	  {
   443	    "number": "5.2.2",
   444	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечить безопасность проведения Операций в Интернет-эквайринге посредством использования современных протоколов и Технологий 3DSecure",
   445	    "required_type": "mandatory",
   446	    "main_idea": "",
   447	    "only_for_product": "internet_acquiring",
   448	    "only_for_lot": "common",
   449	    "only_for_terminal": "common",
   450	    "topics": [
   451	      "использование современных протоколов безопасности",
   452	      "использование технологий 3DSecure"
   453	    ],
   454	    "payment_method": "common"
   455	  },
   456	  {
   457	    "number": "5.2.3",
   458	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Установить на Предприятии и подготовить к эксплуатации Электронные терминалы/Смарт-терминалы Банка для проведения Операций. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком",
   459	    "required_type": "mandatory",
   460	    "main_idea": "Важно, чтобы в договоре срок установки был не менее 3 рабочих дней. Срок инструктажа не декларируется. Отсутствие отсылки на с инструктивные материалы разногласием не является",
   461	    "only_for_product": "trade_acquiring",
   462	    "only_for_lot": "common",
   463	    "only_for_terminal": "common",
   464	    "topics": [
   465	      "установка Электронных терминалов/Смарт-терминалов Банка на Предприятии",
   466	      "подготовка Электронных терминалов/Смарт-терминалов Банка к эксплуатации",
   467	      "проведение первичного инструктажа работников ТСТ"
   468	    ],
   469	    "payment_method": "common"
   470	  },
   471	  {
   472	    "number": "5.2.4",
   473	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять круглосуточную Авторизацию",
   474	    "required_type": "optional",
   475	    "main_idea": "",
   476	    "only_for_product": "common",
   477	    "only_for_lot": "common",
   478	    "only_for_terminal": "common",
   479	    "topics": [
   480	      "Банк осуществляет Авторизацию без перерывов 24 часа в сутки"
   481	    ],
   482	    "payment_method": "common"
   483	  },
   484	  {
   485	    "number": "5.2.5",
   486	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Разместить на сайте:  https://www.sberbank.ru/help/business/acquiring обучающие материалы для прохождения инструктажа сотрудниками Предприятия",
   487	    "required_type": "optional",
   488	    "main_idea": "Подсвечивать разногласие, если только сайты отличаются, если в договоре вместо сайта прочерк, то это не разногласие",
   489	    "only_for_product": "common",
   490	    "only_for_lot": "common",
   491	    "only_for_terminal": "common",
   492	    "topics": [
   493	      "обучающие материалы размещены по указанной ссылке",
   494	      "материалы доступны для прохождения инструктажа сотрудниками Предприятия"
   495	    ],
   496	    "payment_method": "common"
   497	  },
   498	  {
   499	    "number": "5.2.6",
   500	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечивать Электронные терминалы/Смарт-терминалы, установленные на Предприятии/ТСТ, информационными материалами, необходимыми для проведения Операций",
   501	    "required_type": "optional",
   502	    "main_idea": "",
   503	    "only_for_product": "trade_acquiring",
   504	    "only_for_lot": "common",
   505	    "only_for_terminal": "common",
   506	    "topics": [
   507	      "Обеспечение Электронных терминалов информационными материалами",
   508	      "Обеспечение Смарт-терминалов информационными материалами"
   509	    ],
   510	    "payment_method": "common"
   511	  },
   512	  {
   513	    "number": "5.2.7",
   514	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Обеспечивать круглосуточную работоспособность Электронных терминалов/Смарт-терминалов. В случае выхода из строя Электронного терминала/Смарт-терминала Банка, обеспечить Предприятие исправным Электронным терминалом/Смарт-терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Банком заявки от Предприятия по номеру службы поддержки Банка по телефонам, указанным в п..2. Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.",
   515	    "required_type": "optional",
   516	    "main_idea": "",
   517	    "only_for_product": "common",
   518	    "only_for_lot": "common",
   519	    "only_for_terminal": "common",
   520	    "topics": [
   521	      "круглосуточная работоспособность Электронных терминалов/Смарт-терминалов",
   522	      "замена неисправного Электронного терминала/Смарт-терминала на исправный не позднее 3 рабочих дней после заявки"
   523	    ],
   524	    "payment_method": "common"
   525	  },
   526	  {
   527	    "number": "5.2.8",
   528	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → На основании полученной от Предприятия расчетной информации, переданной от Электронного терминала/Смарт-терминала  / Ресурса /QR-кода  в Банк, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Банком перечислять на расчетный (текущий) счет Предприятия суммы Операций оплаты в валюте проведения операции (рубли РФ) за вычетом сумм, перечисленных в п.5.1.1 настоящего Договора. Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. ➜ «ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Датой получения расчетной информации Банком является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. ➜ «ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → В случае технического сбоя при передаче Электронной сверки итогов/ невозможности проведения Предприятием/ТСТ или отсутствия Электронной сверки итогов по иным причинам, перечислять Предприятию суммы Операций, за исключением сумм, указанных в первом абзаце настоящего пункта (п.5.2.8), по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов, проводить расчеты по всем Операциям с данной ТСТ. ",
   529	    "required_type": "mandatory",
   530	    "main_idea": "Важен срок перечисления средств",
   531	    "only_for_product": "common",
   532	    "only_for_lot": "common",
   533	    "only_for_terminal": "common",
   534	    "topics": [
   535	      "перечисление средств на счет Предприятия не позднее 2 рабочих дней после получения расчетной информации",
   536	      "дата получения расчетной информации - рабочий день, следующий за днем электронной сверки итогов",
   537	      "при техническом сбое перечисление средств происходит через 3 календарных дня после последней успешной сверки"
   538	    ],
   539	    "payment_method": "common"
   540	  },
   541	  {
   542	    "number": "5.2.9",
   543	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Предоставить Предприятию QR-код партнера по электронным каналам связи в электронном виде или на бумажном носителе",
   544	    "required_type": "optional",
   545	    "main_idea": "",
   546	    "only_for_product": "trade_acquiring",
   547	    "only_for_lot": "common",
   548	    "only_for_terminal": "common",
   549	    "topics": [
   550	      "Предоставление QR-кода партнера в электронном виде или на бумажном носителе"
   551	    ],
   552	    "payment_method": "qr"
   553	  },
   554	  {
   555	    "number": "5.2.10",
   556	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять обработку ПДн, полученных от Предприятия, а также обеспечить конфиденциальность и защиту обрабатываемых ПДн в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных». Принимать необходимые правовые, организационные и технические меры или обеспечивать их принятие для защиты получаемых от Предприятия ПДн от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения ПДн, а также от иных неправомерных действий в отношении получаемых от Предприятия ПДн",
   557	    "required_type": "mandatory",
   558	    "main_idea": "",
   559	    "only_for_product": "common",
   560	    "only_for_lot": "common",
   561	    "only_for_terminal": "common",
   562	    "topics": [],
   563	    "payment_method": "common"
   564	  },
   565	  {
   566	    "number": "5.2.12",
   567	    "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Банк предоставляет QR-API (в т.ч. всё, что связано с организацией информационно-технологического взаимодействия посредством такого API) «как есть» без предоставления каких-либо гарантий",
   568	    "required_type": "optional",
   569	    "main_idea": "",
   570	    "only_for_product": "internet_acquiring",
   571	    "only_for_lot": "common",
   572	    "only_for_terminal": "common",
   573	    "topics": [
   574	      "Банк предоставляет QR-API без гарантий"
   575	    ],
   576	    "payment_method": "qr"
   577	  },
   578	  {
   579	    "number": "6.1",
   580	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → За осуществление расчетов по Операциям оплаты, Предприятие уплачивает Банку плату в размере:\n«(____________) процент от суммы Операций оплат».",
   581	    "required_type": "mandatory",
   582	    "main_idea": "Важно",
   583	    "only_for_product": "common",
   584	    "only_for_lot": "common",
   585	    "only_for_terminal": "common",
   586	    "topics": [
   587	      "размер платы в процентах от суммы операций"
   588	    ],
   589	    "payment_method": "common"
   590	  },
   591	  {
   592	    "number": "6.2",
   593	    "enriched_text": "«ОПЛАТА УСЛУГ БАНКА» → Банк ежемесячно, не позднее 5 (пятого) рабочего дня месяца, следующего за месяцем оказания услуг (далее – Отчетный месяц), направляет Предприятию Универсальный передаточный документ[2] (далее – УПД) на оплату услуг Банка за проведение расчетов по Операциям оплаты за Отчетный месяц. \nВознаграждение Банка, установленное п.6.1 Договора, включает НДС по ставке, установленной законодательством Российской Федерации.",
   594	    "required_type": "mandatory",
   595	    "main_idea": "УПД - это универсальный передаточный документ (документ о приёмке, документ на оплату услуг). Важно проверить сроки и периодичность оплаты",
   596	    "only_for_product": "common",
   597	    "only_for_lot": "common",
   598	    "only_for_terminal": "common",
   599	    "topics": [
   600	      "Банк направляет документ на оплату услуг Банка",

