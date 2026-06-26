## Summarized at 2026-06-26T07:32:09.262403+00:00

Human: Contract-extra review
AI: I'll start by reading the skill file and understanding the project structure.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_rkzuymgCXYMO6OCVI2HC8698', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_01_WW7SIEbFltW9SMA7B8tG0551', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs'}, 'id': 'call_02_0nlUL3ylfLprfBnTFF3N4421', 'type': 'tool_call'}]
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
Tool: ['/outputs/working/clause_index.json', '/outputs/working/contract_locator_registry.json', '/outputs/working/contract_product_profile.json', '/outputs/working/legal_propositions.json', '/outputs/working/source_preflight.json']
Tool: ['/outputs/working/']
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_product_profile.json'}, 'id': 'call_00_9LjECY1pWrXupukJnjLl0658', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_locator_registry.json'}, 'id': 'call_01_9mqMTAZKY6f1arTVpXTN5055', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 200}, 'id': 'call_02_7Fqo1ygaoJzhkRH9OfGI2698', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/clause_index.json', 'limit': 100}, 'id': 'call_03_NLyYrjzR5t8kN9naSCQn5760', 'type': 'tool_call'}]
Tool:      1	{
     2	  "product": ["trade_acquiring"],
     3	  "lot": "44_fz",
     4	  "terminal": ["pos"],
     5	  "payment_method": ["cards", "qr"],
     6	  "legal_regime": "44_fz",
     7	  "notes": "Contract is a 44-FZ public procurement for trade acquiring services with POS terminals at physical TST locations. QR-code display capability mentioned in Technical Assignment. No internet acquiring, no SberPay, no smart terminals explicitly in scope. Terminal type is standard POS (Электронные терминалы)."
     8	}
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
   101	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами посредством системы ДБО или аналогичных систем Банка Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним и",
   102	      "type": "operative",
   103	      "materiality": "needs_source_review",
   104	      "protected_party": "",
   105	      "bound_party": "",
   106	      "right_or_obligation": "",
   107	      "legal_object": "",
   108	      "trigger": "",
   109	      "deadline": "",
   110	      "amount_formula_cap": "",
   111	      "procedure_channel": "",
   112	      "liability_remedy": "",
   113	      "scope_options": [],
   114	      "consequence": "",
   115	      "applicability_filters": {
   116	        "required_type": "mandatory",
   117	        "only_for_product": "common",
   118	        "only_for_lot": "common",
   119	        "only_for_terminal": "common",
   120	        "payment_method": "common"
   121	      },
   122	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   123	      "topics": [
   124	        "Обмен документами посредством системы ДБО или аналогичных систем Банка"
   125	      ],
   126	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.2 посредством системы ДБО или аналогичных систем Банка;"
   127	    },
   128	    {
   129	      "id": "2.3.3",
   130	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   131	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами с доставкой нарочным или курьером Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способо",
   132	      "type": "operative",
   133	      "materiality": "needs_source_review",
   134	      "protected_party": "",
   135	      "bound_party": "",
   136	      "right_or_obligation": "",
   137	      "legal_object": "",
   138	      "trigger": "",
   139	      "deadline": "",
   140	      "amount_formula_cap": "",
   141	      "procedure_channel": "",
   142	      "liability_remedy": "",
   143	      "scope_options": [],
   144	      "consequence": "",
   145	      "applicability_filters": {
   146	        "required_type": "optional",
   147	        "only_for_product": "common",
   148	        "only_for_lot": "common",
   149	        "only_for_terminal": "common",
   150	        "payment_method": "common"
   151	      },
   152	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   153	      "topics": [
   154	        "Обмен документами с доставкой нарочным или курьером"
   155	      ],
   156	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
   157	    },
   158	    {
   159	      "id": "2.3.4",
   160	      "source_text": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами через заказное письмо Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;",
   161	      "source_excerpt": "Важен сам факт возможности отправки информации / документов таким способом Обмен документами через заказное письмо Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемы",
   162	      "type": "operative",
   163	      "materiality": "needs_source_review",
   164	      "protected_party": "",
   165	      "bound_party": "",
   166	      "right_or_obligation": "",
   167	      "legal_object": "",
   168	      "trigger": "",
   169	      "deadline": "",
   170	      "amount_formula_cap": "",
   171	      "procedure_channel": "",
   172	      "liability_remedy": "",
   173	      "scope_options": [],
   174	      "consequence": "",
   175	      "applicability_filters": {
   176	        "required_type": "optional",
   177	        "only_for_product": "common",
   178	        "only_for_lot": "common",
   179	        "only_for_terminal": "common",
   180	        "payment_method": "common"
   181	      },
   182	      "main_idea": "Важен сам факт возможности отправки информации / документов таким способом",
   183	      "topics": [
   184	        "Обмен документами через заказное письмо"
   185	      ],
   186	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Предприятия на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;"
   187	    },
   188	    {
   189	      "id": "2.3.5",
   190	      "source_text": "Важна равнозначность документов Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП; электронные документы имеют юридическую силу документов на бумаге Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   191	      "source_excerpt": "Важна равнозначность документов Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП; электронные документы имеют юридическую силу документов на бумаге Банк и Предприятие в рамках нас",
   192	      "type": "operative",
   193	      "materiality": "needs_source_review",
   194	      "protected_party": "",
   195	      "bound_party": "",
   196	      "right_or_obligation": "",
   197	      "legal_object": "",
   198	      "trigger": "",
   199	      "deadline": "",
   200	      "amount_formula_cap": "",
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
AI: Now let me read the remaining key files - the references, the contract text, the matrix, and the rest of the working artifacts.[{'name': 'read_file', 'args': {'file_path': '/references/output-contract.md', 'limit': 500}, 'id': 'call_00_kuoiMAEMqdw6p3MjZHFN5498', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_01_Bj7O5YFQwgjdUVgX1yrq9755', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/references/delegation-contract.md', 'limit': 500}, 'id': 'call_02_3P82jTMKR9EoZOiL2EED6773', 'type': 'tool_call'}]
Tool: Error: File '/references/output-contract.md' not found
Tool: Error: File '/references/comparison-patterns.md' not found
Tool: Error: File '/references/delegation-contract.md' not found
AI: [{'name': 'glob', 'args': {'pattern': '**/references/**'}, 'id': 'call_00_pRUS4uYWWFTgxZFHL4pV7636', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/output-contract.md'}, 'id': 'call_01_IoGtjhhD9d5JOn1dRUq99537', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/comparison-patterns.md'}, 'id': 'call_02_kdrMAbXtPNU1UmDhphYt8845', 'type': 'tool_call'}]
Tool: ['/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/delegation-contract.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md']
Tool: ['/skills/acquiring-discrepancy-analysis/references/output-contract.md']
Tool: ['/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md']
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 500}, 'id': 'call_00_gzqZ70ettVRz2IuUHGdc4772', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 500}, 'id': 'call_01_AJdRsmwIN7FpuzrRkqJa5774', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/delegation-contract.md', 'limit': 500}, 'id': 'call_02_Pzho1VMYLUaWLjfkwTyw5847', 'type': 'tool_call'}]
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
    28	## Locator Rules
    29	
    30	- Use final `contract_id` values only from
    31	  `/outputs/working/contract_locator_registry.json` where `final_allowed = true`.
    32	- Use `evidence_locators` for appendix starts, table anchors, and unnumbered
    33	  source anchors.
    34	- Evidence-only locators cannot be used as accepted candidates, rejected
    35	  candidates, atomic link ids, or extra contract ids.
    36	- Do not create semantic or derived ids such as `Приложение_1_п5` or
    37	  `Приложение_1_п5_комиссия`.
    38	
    39	## Fragment Acceptance
    40	
    41	Before a fragment is merged, run:
    42	
    43	```bash
    44	python skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py <fragment-path> --registry outputs/working/contract_locator_registry.json
    45	```
    46	
    47	For matrix batches, also pass assigned ids:
    48	
    49	```bash
    50	python skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py <fragment-path> --registry outputs/working/contract_locator_registry.json --assigned-matrix-ids "<comma-separated ids>"
    51	```
    52	
    53	If validation fails, repair the fragment once using only the reported errors.
    54	If it still fails, do not merge it; write the validator report under
    55	`/outputs/working/` and mark the run incomplete for orchestration recovery.
    56	
    57	## Merge Rules
    58	
    59	- Merge only validated fragments.
    60	- Do not merge fragments whose final links/statuses are justified by automatic
    61	  scores, keyword overlap, token overlap, section proximity, or other mechanical
    62	  ranking.
    63	- Do not merge overbroad same-topic or same-parent groups unless every listed
    64	  contract locator contributes a named material element to the same legal
    65	  result.
    66	- Do not merge a fragment that spreads one placeholder, channel, deadline,
    67	  amount, consent, or liability gap across independent sibling requirements.
    68	- A contract locator cannot be both linked and `extra_in_contract`.
    69	- `coverage_ledger` is derived from validated final arrays and accepted
    70	  out-of-scope / not-applicable matrix closures.
    71	- Structural QA blocks invalid ids, duplicate closure conflicts, schema gaps,
    72	  and summary mismatch.
    73	- Legal QA is focused on unresolved `deviation`, `missing_in_contract`, and
    74	  `extra_in_contract` findings; it does not rewrite valid aligned groups without
    75	  a named legal reason.
AI: Now let me read the full contract text and matrix to understand the scope:[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_00_cRIXaESPZTd97euqQkt17844', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_01_GhtaWNtzqzfRNlT3RKiR6787', 'type': 'tool_call'}]
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
AI: Now let me continue reading the contract and matrix to understand the full scope:[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 200}, 'id': 'call_00_0hyw5ZNNU4SMRkZr3GqZ9018', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 200}, 'id': 'call_01_LmaS03zz2C2ckrKAzu0T4007', 'type': 'tool_call'}]
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
AI: Now let me understand the full scope of the task. Let me read the rest of the contract and matrix, and also check what's already been done:[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 400, 'limit': 200}, 'id': 'call_00_sOcOoR1hmxYgAGZOLPaU4587', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 400, 'limit': 200}, 'id': 'call_01_VZ0caplxOy9ivnHXWvaU9208', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 200, 'limit': 200}, 'id': 'call_02_HDnNw3ZZXsQMsSnUNVSY6201', 'type': 'tool_call'}]
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
Tool:    201	      "procedure_channel": "",
   202	      "liability_remedy": "",
   203	      "scope_options": [],
   204	      "consequence": "",
   205	      "applicability_filters": {
   206	        "required_type": "mandatory",
   207	        "only_for_product": "common",
   208	        "only_for_lot": "common",
   209	        "only_for_terminal": "common",
   210	        "payment_method": "common"
   211	      },
   212	      "main_idea": "Важна равнозначность документов",
   213	      "topics": [
   214	        "Обмен информацией и документами осуществляется через систему E-invoicing/«СФЕРА-Курьер» с использованием УКЭП",
   215	        "электронные документы имеют юридическую силу документов на бумаге"
   216	      ],
   217	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами посредством автоматизированной системы E-invoicing/ «СФЕРА-Курьер». В этом случае документы подписываются усиленной квалифицированной электронной подписью   (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;"
   218	    },
   219	    {
   220	      "id": "2.3.6",
   221	      "source_text": "Важен сам факт наличия данного канала для обмена электронными документами Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок); Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП) Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
   222	      "source_excerpt": "Важен сам факт наличия данного канала для обмена электронными документами Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок); Перечисление способов обмена документами: обмен документами через",
   223	      "type": "operative",
   224	      "materiality": "needs_source_review",
   225	      "protected_party": "",
   226	      "bound_party": "",
   227	      "right_or_obligation": "",
   228	      "legal_object": "",
   229	      "trigger": "",
   230	      "deadline": "",
   231	      "amount_formula_cap": "",
   232	      "procedure_channel": "",
   233	      "liability_remedy": "",
   234	      "scope_options": [],
   235	      "consequence": "",
   236	      "applicability_filters": {
   237	        "required_type": "mandatory",
   238	        "only_for_product": "common",
   239	        "only_for_lot": "fz_44",
   240	        "only_for_terminal": "common",
   241	        "payment_method": "common"
   242	      },
   243	      "main_idea": "Важен сам факт наличия данного канала для обмена электронными документами",
   244	      "topics": [
   245	        "Перечисление способов обмена документами: через ЕИС (Единую информационную систему в сфере закупок)",
   246	        "Перечисление способов обмена документами: обмен документами через иные электронные торговые площадки (ЭТП)"
   247	      ],
   248	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;"
   249	    },
   250	    {
   251	      "id": "2.3.7",
   252	      "source_text": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию Обмен информацией через обращение в службу поддержки Банка; Дата с которой сторона считается получившей информацию в случае её направления на электронную почту; Дата с которой сторона считается получившей информацию в случае запроса в ДБО; Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма; Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»; Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в: • п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно; • п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма); • п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции; • п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке; • п. 2.3.7. Договора – в дату обращения в службу поддержки Банка.",
   253	      "source_excerpt": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию Обмен информацией через обращение в службу поддержки Банка;",
   254	      "type": "operative",
   255	      "materiality": "needs_source_review",
   256	      "protected_party": "",
   257	      "bound_party": "",
   258	      "right_or_obligation": "",
   259	      "legal_object": "",
   260	      "trigger": "",
   261	      "deadline": "",
   262	      "amount_formula_cap": "",
   263	      "procedure_channel": "",
   264	      "liability_remedy": "",
   265	      "scope_options": [],
   266	      "consequence": "",
   267	      "applicability_filters": {
   268	        "required_type": "optional",
   269	        "only_for_product": "common",
   270	        "only_for_lot": "common",
   271	        "only_for_terminal": "common",
   272	        "payment_method": "common"
   273	      },
   274	      "main_idea": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию",
   275	      "topics": [
   276	        "Обмен информацией через обращение в службу поддержки Банка",
   277	        "Дата с которой сторона считается получившей информацию в случае её направления на электронную почту",
   278	        "Дата с которой сторона считается получившей информацию в случае запроса в ДБО",
   279	        "Дата с которой сторона считается получившей информацию / документы в случае отправки заказного письма",
   280	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по E-invoicing/«СФЕРА-Курьер»",
   281	        "Дата с которой сторона считается получившей информацию / документы в случае отправки по ЕИС"
   282	      ],
   283	      "enriched_text": "Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Договором: → 2.3.7 через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.Сторона считается получившей информацию/документ в случае направления способом, указанным в:\n• п. 2.3.1, п. 2.3.2 Договора – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;\n• п. 2.3.3, п. 2.3.4 Договора – в дату доставки получающей стороне письма/почтового отправления (заказного письма);\n• п. 2.3.5. Договора – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка – ООО «КОРУС Консалтинг СНГ»). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;\n•  п. 2.3.6. Договора – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке;\n• п. 2.3.7. Договора – в дату обращения в службу поддержки Банка."
   284	    },
   285	    {
   286	      "id": "2.4",
   287	      "source_text": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   288	      "source_excerpt": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора.",
   289	      "type": "operative",
   290	      "materiality": "needs_source_review",
   291	      "protected_party": "",
   292	      "bound_party": "",
   293	      "right_or_obligation": "",
   294	      "legal_object": "",
   295	      "trigger": "",
   296	      "deadline": "",
   297	      "amount_formula_cap": "",
   298	      "procedure_channel": "",
   299	      "liability_remedy": "",
   300	      "scope_options": [],
   301	      "consequence": "",
   302	      "applicability_filters": {
   303	        "required_type": "optional",
   304	        "only_for_product": "common",
   305	        "only_for_lot": "common",
   306	        "only_for_terminal": "common",
   307	        "payment_method": "common"
   308	      },
   309	      "main_idea": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   310	      "topics": [],
   311	      "enriched_text": "Документы, ссылки на которые даются в настоящем Договоре, являются неотъемлемой частью Договора."
   312	    },
   313	    {
   314	      "id": "2.5.1.1",
   315	      "source_text": "Важен факт, что бесконтактная оплата подключается автоматически SberPayOnline подключается автоматически при подключении Интернет-эквайринга; используется единый тариф по Интернет-эквайрингу Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;",
   316	      "source_excerpt": "Важен факт, что бесконтактная оплата подключается автоматически SberPayOnline подключается автоматически при подключении Интернет-эквайринга; используется единый тариф по Интернет-эквайрингу Возможность совершения Операций оплаты с использо",
   317	      "type": "operative",
   318	      "materiality": "needs_source_review",
   319	      "protected_party": "",
   320	      "bound_party": "",
   321	      "right_or_obligation": "",
   322	      "legal_object": "",
   323	      "trigger": "",
   324	      "deadline": "",
   325	      "amount_formula_cap": "",
   326	      "procedure_channel": "",
   327	      "liability_remedy": "",
   328	      "scope_options": [],
   329	      "consequence": "",
   330	      "applicability_filters": {
   331	        "required_type": "mandatory",
   332	        "only_for_product": "internet_acquiring",
   333	        "only_for_lot": "common",
   334	        "only_for_terminal": "common",
   335	        "payment_method": "common"
   336	      },
   337	      "main_idea": "Важен факт, что бесконтактная оплата подключается автоматически",
   338	      "topics": [
   339	        "SberPayOnline подключается автоматически при подключении Интернет-эквайринга",
   340	        "используется единый тариф по Интернет-эквайрингу"
   341	      ],
   342	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;"
   343	    },
   344	    {
   345	      "id": "2.5.2.1",
   346	      "source_text": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; наличие документа 'Информация о ТСТ' Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.",
   347	      "source_excerpt": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; н",
   348	      "type": "operative",
   349	      "materiality": "needs_source_review",
   350	      "protected_party": "",
   351	      "bound_party": "",
   352	      "right_or_obligation": "",
   353	      "legal_object": "",
   354	      "trigger": "",
   355	      "deadline": "",
   356	      "amount_formula_cap": "",
   357	      "procedure_channel": "",
   358	      "liability_remedy": "",
   359	      "scope_options": [],
   360	      "consequence": "",
   361	      "applicability_filters": {
   362	        "required_type": "mandatory",
   363	        "only_for_product": "trade_acquiring",
   364	        "only_for_lot": "common",
   365	        "only_for_terminal": "common",
   366	        "payment_method": "sber_pay_face_scan"
   367	      },
   368	      "main_idea": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением",
   369	      "topics": [
   370	        "подключение SberPayFaceScan оформляется на бумажном носителе",
   371	        "подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия",
   372	        "наличие документа 'Информация о ТСТ'"
   373	      ],
   374	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ."
   375	    },
   376	    {
   377	      "id": "2.6.1.1",
   378	      "source_text": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.",
   379	      "source_excerpt": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-код",
   380	      "type": "operative",
   381	      "materiality": "needs_source_review",
   382	      "protected_party": "",
   383	      "bound_party": "",
   384	      "right_or_obligation": "",
   385	      "legal_object": "",
   386	      "trigger": "",
   387	      "deadline": "",
   388	      "amount_formula_cap": "",
   389	      "procedure_channel": "",
   390	      "liability_remedy": "",
   391	      "scope_options": [],
   392	      "consequence": "",
   393	      "applicability_filters": {
   394	        "required_type": "mandatory",
   395	        "only_for_product": "trade_acquiring",
   396	        "only_for_lot": "common",
   397	        "only_for_terminal": "smart",
   398	        "payment_method": "qr"
   399	      },
   400	      "main_idea": "Для приема QR на смарт-терминал не нужно отдельное ПО",
AI: This is a very large task. Let me understand the scope: I need to process the "contract-extra" review — meaning I need to identify `unmatched_contract` items (contract-only terms with no matrix analogue) and produce the `coverage_ledger.contract` rows. Let me set up my task plan and understand the full matrix and contract scope.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix.json to understand all matrix IDs and their applicability filters', 'status': 'in_progress'}, {'content': 'Read full contract.txt to understand all contract clauses', 'status': 'pending'}, {'content': 'Read full legal_propositions.json (contract side) to understand existing contract propositions', 'status': 'pending'}, {'content': 'Read full contract_locator_registry.json to know all final_allowed locators', 'status': 'pending'}, {'content': 'Identify contract-only terms (extra_in_contract) - contract clauses with no matrix analogue', 'status': 'pending'}, {'content': 'Identify not_material contract clauses for coverage_ledger.contract', 'status': 'pending'}, {'content': 'Produce unmatched_contract fragment and coverage_ledger.contract rows', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Fix any validation errors and finalize', 'status': 'pending'}]}, 'id': 'call_00_I2uuoK5x9nEGrvuTuM5X0093', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix.json to understand all matrix IDs and their applicability filters', 'status': 'in_progress'}, {'content': 'Read full contract.txt to understand all contract clauses', 'status': 'pending'}, {'content': 'Read full legal_propositions.json (contract side) to understand existing contract propositions', 'status': 'pending'}, {'content': 'Read full contract_locator_registry.json to know all final_allowed locators', 'status': 'pending'}, {'content': 'Identify contract-only terms (extra_in_contract) - contract clauses with no matrix analogue', 'status': 'pending'}, {'content': 'Identify not_material contract clauses for coverage_ledger.contract', 'status': 'pending'}, {'content': 'Produce unmatched_contract fragment and coverage_ledger.contract rows', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Fix any validation errors and finalize', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 600, 'limit': 500}, 'id': 'call_00_tDSidC84qAV7BQqHyx1s0763', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'offset': 400, 'limit': 500}, 'id': 'call_01_Ishdq9i4lc1KsJzLvWaP9579', 'type': 'tool_call'}]
Tool:    601	  "enriched_text":"«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → По письменному запросу Банка, не позднее, чем по истечении 3 (трех) рабочих дней с даты получения соответствующего запроса, Предприятие обязуется предоставить подтверждение правомерности передачи ПДн. В случае если Предприятие не предоставит подтверждение наличия таких оснований, оно обязуется за свой счет урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные Банку, а также возместить любые убытки и расходы, понесенные Банком в результате не предоставления таких доказательств.",
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
Tool:    401	      "topics": [
   402	        "OR-код подключается при установке Смарт-терминала Банка",
   403	        "OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ"
   404	      ],
   405	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ."
   406	    },
   407	    {
   408	      "id": "2.6.2.1",
   409	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка возможность использования QR-кода на ККТ с собственным ПО Предприятия; подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API); порядок и условия подключения QR-API описаны на Официальном сайте Банка Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;",
   410	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте бан",
   411	      "type": "operative",
   412	      "materiality": "needs_source_review",
   413	      "protected_party": "",
   414	      "bound_party": "",
   415	      "right_or_obligation": "",
   416	      "legal_object": "",
   417	      "trigger": "",
   418	      "deadline": "",
   419	      "amount_formula_cap": "",
   420	      "procedure_channel": "",
   421	      "liability_remedy": "",
   422	      "scope_options": [],
   423	      "consequence": "",
   424	      "applicability_filters": {
   425	        "required_type": "mandatory",
   426	        "only_for_product": "trade_acquiring",
   427	        "only_for_lot": "common",
   428	        "only_for_terminal": "common",
   429	        "payment_method": "qr"
   430	      },
   431	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре.  Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка",
   432	      "topics": [
   433	        "возможность использования QR-кода на ККТ с собственным ПО Предприятия",
   434	        "подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API)",
   435	        "порядок и условия подключения QR-API описаны на Официальном сайте Банка"
   436	      ],
   437	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;"
   438	    },
   439	    {
   440	      "id": "2.6.2.2",
   441	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ; подключение динамического QR-кода зависит от ПО ККТ; при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора; первая операция оплаты QR-кодом активирует услугу; Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора; подключение QR-кода производится согласно Приложениям №1 и №1.1 Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору.",
   442	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на",
   443	      "type": "operative",
   444	      "materiality": "needs_source_review",
   445	      "protected_party": "",
   446	      "bound_party": "",
   447	      "right_or_obligation": "",
   448	      "legal_object": "",
   449	      "trigger": "",
   450	      "deadline": "",
   451	      "amount_formula_cap": "",
   452	      "procedure_channel": "",
   453	      "liability_remedy": "",
   454	      "scope_options": [],
   455	      "consequence": "",
   456	      "applicability_filters": {
   457	        "required_type": "mandatory",
   458	        "only_for_product": "trade_acquiring",
   459	        "only_for_lot": "common",
   460	        "only_for_terminal": "common",
   461	        "payment_method": "qr"
   462	      },
   463	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия",
   464	      "topics": [
   465	        "возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ",
   466	        "подключение динамического QR-кода зависит от ПО ККТ",
   467	        "при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора",
   468	        "первая операция оплаты QR-кодом активирует услугу",
   469	        "Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора",
   470	        "подключение QR-кода производится согласно Приложениям №1 и №1.1"
   471	      ],
   472	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору."
   473	    },
   474	    {
   475	      "id": "2.6.3.1",
   476	      "source_text": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → QR-код подключается при установке Электронного терминала в ТСТ;",
   477	      "source_excerpt": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-",
   478	      "type": "operative",
   479	      "materiality": "needs_source_review",
   480	      "protected_party": "",
   481	      "bound_party": "",
   482	      "right_or_obligation": "",
   483	      "legal_object": "",
   484	      "trigger": "",
   485	      "deadline": "",
   486	      "amount_formula_cap": "",
   487	      "procedure_channel": "",
   488	      "liability_remedy": "",
   489	      "scope_options": [],
   490	      "consequence": "",
   491	      "applicability_filters": {
   492	        "required_type": "mandatory",
   493	        "only_for_product": "trade_acquiring",
   494	        "only_for_lot": "common",
   495	        "only_for_terminal": "common",
   496	        "payment_method": "qr"
   497	      },
   498	      "main_idea": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке",
   499	      "topics": [
   500	        "QR-код подключается при установке Электронного терминала в ТСТ"
   501	      ],
   502	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: →  QR-код подключается при установке Электронного терминала в ТСТ;"
   503	    },
   504	    {
   505	      "id": "2.6.3.2",
   506	      "source_text": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк отключение QR-кода возможно по инициативе Предприятия; инициатива отключения реализуется через обращение в Банк Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора.",
   507	      "source_excerpt": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк отключение QR-кода возможно по инициативе Предприятия; инициатива отключения реализуется через обращение в Банк Возможность",
   508	      "type": "operative",
   509	      "materiality": "needs_source_review",
   510	      "protected_party": "",
   511	      "bound_party": "",
   512	      "right_or_obligation": "",
   513	      "legal_object": "",
   514	      "trigger": "",
   515	      "deadline": "",
   516	      "amount_formula_cap": "",
   517	      "procedure_channel": "",
   518	      "liability_remedy": "",
   519	      "scope_options": [],
   520	      "consequence": "",
   521	      "applicability_filters": {
   522	        "required_type": "mandatory",
   523	        "only_for_product": "trade_acquiring",
   524	        "only_for_lot": "common",
   525	        "only_for_terminal": "common",
   526	        "payment_method": "qr"
   527	      },
   528	      "main_idea": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк",
   529	      "topics": [
   530	        "отключение QR-кода возможно по инициативе Предприятия",
   531	        "инициатива отключения реализуется через обращение в Банк"
   532	      ],
   533	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → отключение QR-кода по инициативе Предприятия осуществляется при обращении в Банк одним из способов, указанных в п.2.3.1. – п.2.3.4., п.2.3.7. Договора."
   534	    },
   535	    {
   536	      "id": "2.7",
   537	      "source_text": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юридическую силу с Договором, оформленным на бумажном носителе, подписанным собственноручными подписями уполномоченных представителей Банка и Предприятия.",
   538	      "source_excerpt": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и под",
   539	      "type": "operative",
   540	      "materiality": "needs_source_review",
   541	      "protected_party": "",
   542	      "bound_party": "",
   543	      "right_or_obligation": "",
   544	      "legal_object": "",
   545	      "trigger": "",
   546	      "deadline": "",
   547	      "amount_formula_cap": "",
   548	      "procedure_channel": "",
   549	      "liability_remedy": "",
   550	      "scope_options": [],
   551	      "consequence": "",
   552	      "applicability_filters": {
   553	        "required_type": "optional",
   554	        "only_for_product": "common",
   555	        "only_for_lot": "common",
   556	        "only_for_terminal": "common",
   557	        "payment_method": "common"
   558	      },
   559	      "main_idea": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП ",
   560	      "topics": [],
   561	      "enriched_text": "Договор может быть заключен на бумажном носителе или в электронном виде с использованием УКЭП Сторон. Договор, оформленный в виде электронного документа и подписанный УКЭП уполномоченных представителей Банка и Предприятия, имеет равную юридическую силу с Договором, оформленным на бумажном носителе, подписанным собственноручными подписями уполномоченных представителей Банка и Предприятия."
   562	    },
   563	    {
   564	      "id": "3.1",
   565	      "source_text": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Плати QR); Приём оплаты осуществляется в ТСТ (торгово-сервисных точках) и/или на Ресурсе (сайт/приложение Предприятия); Обработка информации производится через Электронные терминалы, Смарт-терминалы или СПЭП; Перечень допустимых к приёму Карт «ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ/на Ресурсе и обработку информации на Электронных терминалах/Смарт-терминалах [1]/через СПЭП. Перечень Карт перечислен в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе к Договору, размещенном на Официальном сайте Банка",
   566	      "source_excerpt": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Пл",
   567	      "type": "operative",
   568	      "materiality": "needs_source_review",
   569	      "protected_party": "",
   570	      "bound_party": "",
   571	      "right_or_obligation": "",
   572	      "legal_object": "",
   573	      "trigger": "",
   574	      "deadline": "",
   575	      "amount_formula_cap": "",
   576	      "procedure_channel": "",
   577	      "liability_remedy": "",
   578	      "scope_options": [],
   579	      "consequence": "",
   580	      "applicability_filters": {
   581	        "required_type": "optional",
   582	        "only_for_product": "common",
   583	        "only_for_lot": "common",
   584	        "only_for_terminal": "common",
   585	        "payment_method": "common"
   586	      },
   587	      "main_idea": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР",
   588	      "topics": [
   589	        "Предприятие обязано организовать приём оплаты за Товары/услуги с использованием платёжных инструментов (Карта, реквизиты Карты, NFC-карта, SberPay, Плати QR)",
   590	        "Приём оплаты осуществляется в ТСТ (торгово-сервисных точках) и/или на Ресурсе (сайт/приложение Предприятия)",
   591	        "Обработка информации производится через Электронные терминалы, Смарт-терминалы или СПЭП",
   592	        "Перечень допустимых к приёму Карт"
   593	      ],
   594	      "enriched_text": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие организует прием оплаты за реализуемые им Товары/услуги с использованием Карты/ее реквизитов/NFC-карты/SberPay/Плати QR в ТСТ/на Ресурсе и обработку информации на Электронных терминалах/Смарт-терминалах [1]/через СПЭП. Перечень Карт перечислен в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе к Договору, размещенном на Официальном сайте Банка"
   595	    },
   596	    {
   597	      "id": "3.2",
   598	      "source_text": "Важен сам факт обязанности Банка в перечислении сумм Предприятию Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию «ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ/на Ресурсе.",
   599	      "source_excerpt": "Важен сам факт обязанности Банка в перечислении сумм Предприятию Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию «ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Това",
   600	      "type": "operative",
   601	      "materiality": "needs_source_review",
   602	      "protected_party": "",
   603	      "bound_party": "",
   604	      "right_or_obligation": "",
   605	      "legal_object": "",
   606	      "trigger": "",
   607	      "deadline": "",
   608	      "amount_formula_cap": "",
   609	      "procedure_channel": "",
   610	      "liability_remedy": "",
   611	      "scope_options": [],
   612	      "consequence": "",
   613	      "applicability_filters": {
   614	        "required_type": "optional",
   615	        "only_for_product": "common",
   616	        "only_for_lot": "common",
   617	        "only_for_terminal": "common",
   618	        "payment_method": "common"
   619	      },
   620	      "main_idea": "Важен сам факт обязанности Банка в перечислении сумм Предприятию",
   621	      "topics": [
   622	        "Банк обязан перечислять суммы операций оплаты товаров/услуг Предприятию"
   623	      ],
   624	      "enriched_text": "«ПРЕДМЕТ ДОГОВОРА» → Банк в соответствии с Договором перечисляет Предприятию суммы Операций оплаты Товаров/услуг в ТСТ/на Ресурсе."
   625	    },
   626	    {
   627	      "id": "3.3",
   628	      "source_text": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору Предприятие перечисляет Банку плату за проведение расчётов ежемесячно «ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров/услуг в ТСТ[7]/на Ресурсе – к ИЭ[8]",
   629	      "source_excerpt": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору Предприятие перечисляет Банку плату за проведение расчётов ежемесячно «ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Раздел",
   630	      "type": "operative",
   631	      "materiality": "needs_source_review",
   632	      "protected_party": "",
   633	      "bound_party": "",
   634	      "right_or_obligation": "",
   635	      "legal_object": "",
   636	      "trigger": "",
   637	      "deadline": "",
   638	      "amount_formula_cap": "",
   639	      "procedure_channel": "",
   640	      "liability_remedy": "",
   641	      "scope_options": [],
   642	      "consequence": "",
   643	      "applicability_filters": {
   644	        "required_type": "mandatory",
   645	        "only_for_product": "common",
   646	        "only_for_lot": "common",
   647	        "only_for_terminal": "common",
   648	        "payment_method": "common"
   649	      },
   650	      "main_idea": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору",
   651	      "topics": [
   652	        "Предприятие перечисляет Банку плату за проведение расчётов ежемесячно"
   653	      ],
   654	      "enriched_text": "«ПРЕДМЕТ ДОГОВОРА» → Предприятие ежемесячно перечисляет Банку в соответствии с Разделом 6 Договора сумму платы за проведение расчетов по Операциям оплаты Товаров/услуг в ТСТ[7]/на Ресурсе – к ИЭ[8]"
   655	    },
   656	    {
   657	      "id": "4.1.1",
   658	      "source_text": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов с Банком; Согласование информационных материалов осуществляется в соответствии с пунктами 2.3.1 и 2.3.2 «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3.1 и п. 2.3.2 настоящего Договора.",
   659	      "source_excerpt": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов",
   660	      "type": "operative",
   661	      "materiality": "needs_source_review",
   662	      "protected_party": "",
   663	      "bound_party": "",
   664	      "right_or_obligation": "",
   665	      "legal_object": "",
   666	      "trigger": "",
   667	      "deadline": "",
   668	      "amount_formula_cap": "",
   669	      "procedure_channel": "",
   670	      "liability_remedy": "",
   671	      "scope_options": [],
   672	      "consequence": "",
   673	      "applicability_filters": {
   674	        "required_type": "optional",
   675	        "only_for_product": "common",
   676	        "only_for_lot": "common",
   677	        "only_for_terminal": "common",
   678	        "payment_method": "qr"
   679	      },
   680	      "main_idea": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком",
   681	      "topics": [
   682	        "Предприятие имеет право ссылаться на возможность оплаты с использованием Карт/QR-кода после согласования материалов с Банком",
   683	        "Согласование информационных материалов осуществляется в соответствии с пунктами 2.3.1 и 2.3.2"
   684	      ],
   685	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Ссылаться на возможность оплаты Товаров/услуг с использованием Карт/QR-кода в собственных информационных материалах, предварительно согласовав их с Банком в соответствии с п.2.3.1 и п. 2.3.2 настоящего Договора."
   686	    },
   687	    {
   688	      "id": "4.1.2",
   689	      "source_text": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов; закреплено право Заказчика на получение консультаций по проведению Операций «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, указанному в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.",
   690	      "source_excerpt": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов; закреплено право Заказчика на получение ко",
   691	      "type": "operative",
   692	      "materiality": "needs_source_review",
   693	      "protected_party": "",
   694	      "bound_party": "",
   695	      "right_or_obligation": "",
   696	      "legal_object": "",
   697	      "trigger": "",
   698	      "deadline": "",
   699	      "amount_formula_cap": "",
   700	      "procedure_channel": "",
   701	      "liability_remedy": "",
   702	      "scope_options": [],
   703	      "consequence": "",
   704	      "applicability_filters": {
   705	        "required_type": "optional",
   706	        "only_for_product": "common",
   707	        "only_for_lot": "common",
   708	        "only_for_terminal": "common",
   709	        "payment_method": "common"
   710	      },
   711	      "main_idea": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования",
   712	      "topics": [
   713	        "закреплено право Заказчика на получение консультаций по эксплуатации Электронных терминалов/Смарт-терминалов",
   714	        "закреплено право Заказчика на получение консультаций по проведению Операций"
   715	      ],
   716	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Получать консультацию в Банке по вопросам эксплуатации Электронных терминалов/Смарт-терминалов Банка и проведению Операций путем обращения в службу поддержки Банка по телефону, указанному в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе."
   717	    },
   718	    {
   719	      "id": "4.1.3",
   720	      "source_text": "Важен сам факт, что QR выдаёт Банк Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Мобильных устройствах Предприятия, а также на ККТ, принадлежащей Предприятию, или на видном месте, в том числе на бумажном носителе.",
   721	      "source_excerpt": "Важен сам факт, что QR выдаёт Банк Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Т",
   722	      "type": "operative",
   723	      "materiality": "needs_source_review",
   724	      "protected_party": "",
   725	      "bound_party": "",
   726	      "right_or_obligation": "",
   727	      "legal_object": "",
   728	      "trigger": "",
   729	      "deadline": "",
   730	      "amount_formula_cap": "",
   731	      "procedure_channel": "",
   732	      "liability_remedy": "",
   733	      "scope_options": [],
   734	      "consequence": "",
   735	      "applicability_filters": {
   736	        "required_type": "optional",
   737	        "only_for_product": "trade_acquiring",
   738	        "only_for_lot": "common",
   739	        "only_for_terminal": "common",
   740	        "payment_method": "qr_sber_pay"
   741	      },
   742	      "main_idea": "Важен сам факт, что QR выдаёт Банк",
   743	      "topics": [
   744	        "Предприятие имеет право использовать полученные от Банка QR-коды для приема платежей через SberPayQR/Плати QR"
   745	      ],
   746	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие имеет право: → Использовать для приема оплаты Товаров/услуг по SberPayQR/Плати QR один или несколько QR-кодов, полученных в Банке и размещенных на Смарт-терминалах, Электронных терминалах, Мобильных устройствах Предприятия, а также на ККТ, принадлежащей Предприятию, или на видном месте, в том числе на бумажном носителе."
   747	    },
   748	    {
   749	      "id": "4.2.1",
   750	      "source_text": "Важен факт, что предприятие обязуется оплачивать услуги Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям; Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настоящего Договора.",
   751	      "source_excerpt": "Важен факт, что предприятие обязуется оплачивать услуги Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям; Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена) «ПРАВА И ОБЯЗАННОС",
   752	      "type": "operative",
   753	      "materiality": "needs_source_review",
   754	      "protected_party": "",
   755	      "bound_party": "",
   756	      "right_or_obligation": "",
   757	      "legal_object": "",
   758	      "trigger": "",
   759	      "deadline": "",
   760	      "amount_formula_cap": "",
   761	      "procedure_channel": "",
   762	      "liability_remedy": "",
   763	      "scope_options": [],
   764	      "consequence": "",
   765	      "applicability_filters": {
   766	        "required_type": "mandatory",
   767	        "only_for_product": "common",
   768	        "only_for_lot": "common",
   769	        "only_for_terminal": "common",
   770	        "payment_method": "common"
   771	      },
   772	      "main_idea": "Важен факт, что предприятие обязуется оплачивать услуги",
   773	      "topics": [
   774	        "Предприятие обязуется оплачивать услуги банка по выполнению расчётов по операциям",
   775	        "Предприятие обязуется вносить плату за сервисное обслуживание (если предусмотрена)"
   776	      ],
   777	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → 4.2.1. Оплачивать услуги Банка по выполнению расчетов по Операциям и плату за сервисное обслуживание (при наличии) в соответствии с Тарифами Банка, указанными в разделе 6 настоящего Договора. "
   778	    },
   779	    {
   780	      "id": "4.2.2",
   781	      "source_text": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее нет, то пункты не относятся к теме матрицы Обязанность Предприятия соблюдать положения Договора (наличие формулировки об обязанности соблюдать); Обязанность Предприятия выполнять требования, содержащиеся в информационных / инструктивных материалах, предоставляемых Банком (наличие формулировки об обязанности выполнять) «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/ инструктивных материалах, предоставляемых Банком.",
   782	      "source_excerpt": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее ",
   783	      "type": "operative",
   784	      "materiality": "needs_source_review",
   785	      "protected_party": "",
   786	      "bound_party": "",
   787	      "right_or_obligation": "",
   788	      "legal_object": "",
   789	      "trigger": "",
   790	      "deadline": "",
   791	      "amount_formula_cap": "",
   792	      "procedure_channel": "",
   793	      "liability_remedy": "",
   794	      "scope_options": [],
   795	      "consequence": "",
   796	      "applicability_filters": {
   797	        "required_type": "optional",
   798	        "only_for_product": "common",
   799	        "only_for_lot": "common",
   800	        "only_for_terminal": "common",
   801	        "payment_method": "common"
   802	      },
   803	      "main_idea": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее нет, то пункты не относятся к теме матрицы",
   804	      "topics": [
   805	        "Обязанность Предприятия соблюдать положения Договора (наличие формулировки об обязанности соблюдать)",
   806	        "Обязанность Предприятия выполнять требования, содержащиеся в информационных / инструктивных материалах, предоставляемых Банком (наличие формулировки об обязанности выполнять)"
   807	      ],
   808	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Соблюдать положения Договора, а также выполнять требования, содержащиеся в информационных/ инструктивных материалах, предоставляемых Банком."
   809	    },
   810	    {
   811	      "id": "4.2.3",
   812	      "source_text": "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов; Несвоевременное ознакомление не является основанием для неприменения изменений «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление Предприятия с изменениями, внесенными в вышеуказанные документы, не является основанием для их неприменения Банком.",
   813	      "source_excerpt": "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов; Несвоевременное ознакомление не является основанием для неприменения изменений «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятель",
   814	      "type": "operative",
   815	      "materiality": "needs_source_review",
   816	      "protected_party": "",
   817	      "bound_party": "",
   818	      "right_or_obligation": "",
   819	      "legal_object": "",
   820	      "trigger": "",
   821	      "deadline": "",
   822	      "amount_formula_cap": "",
   823	      "procedure_channel": "",
   824	      "liability_remedy": "",
   825	      "scope_options": [],
   826	      "consequence": "",
   827	      "applicability_filters": {
   828	        "required_type": "optional",
   829	        "only_for_product": "common",
   830	        "only_for_lot": "fz_223",
   831	        "only_for_terminal": "common",
   832	        "payment_method": "common"
   833	      },
   834	      "main_idea": "",
   835	      "topics": [
   836	        "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов",
   837	        "Несвоевременное ознакомление не является основанием для неприменения изменений"
   838	      ],
   839	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Самостоятельно и своевременно знакомиться с изменениями, внесенными в документы, ссылки на которые даются в настоящем Договоре, размещенными на Официальном сайте Банка. Несвоевременное ознакомление Предприятия с изменениями, внесенными в вышеуказанные документы, не является основанием для их неприменения Банком."
   840	    },
   841	    {
   842	      "id": "4.2.4",
   843	      "source_text": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте Предприятие обязано размещать информационные материалы Банка о способах оплаты; Размещение материалов осуществляется в случае отсутствия противоречий с законодательством РФ «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с использованием Карт/NFC-карт/SberPay/Плати QR, в случае если это не противоречит требованиям законодательства Российской Федерации.",
   844	      "source_excerpt": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте Предприятие обязано размещать ",
   845	      "type": "operative",
   846	      "materiality": "needs_source_review",
   847	      "protected_party": "",
   848	      "bound_party": "",
   849	      "right_or_obligation": "",
   850	      "legal_object": "",
   851	      "trigger": "",
   852	      "deadline": "",
   853	      "amount_formula_cap": "",
   854	      "procedure_channel": "",
   855	      "liability_remedy": "",
   856	      "scope_options": [],
   857	      "consequence": "",
   858	      "applicability_filters": {
   859	        "required_type": "optional",
   860	        "only_for_product": "common",
   861	        "only_for_lot": "common",
   862	        "only_for_terminal": "common",
   863	        "payment_method": "common"
   864	      },
   865	      "main_idea": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте",
   866	      "topics": [
   867	        "Предприятие обязано размещать информационные материалы Банка о способах оплаты",
   868	        "Размещение материалов осуществляется в случае отсутствия противоречий с законодательством РФ"
   869	      ],
   870	      "enriched_text": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: Размещать на видных местах ТСТ[1]/общедоступных местах Ресурса[2], предоставляемые Банком информационные материалы, извещающие Покупателей о возможности оплаты Товаров/услуг с использованием Карт/NFC-карт/SberPay/Плати QR, в случае если это не противоречит требованиям законодательства Российской Федерации."
   871	    },
   872	    {
   873	      "id": "4.2.5",
   874	      "source_text": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства Принимать к оплате все карты из списка в течение всего рабочего времени; Не выдавать наличные деньги по картам; Не принимать более двух разных карт от одного покупателя «ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → Принимать в оплату Товаров/услуг все Карты, перечисленные в Порядке проведения операций в Торгово-сервисных точках/на Ресурсе, в течение всего рабочего времени Предприятия. Не выдавать по Картам наличные денежные средства[3]. Не принимать от Покупателя более 2 (двух) различных Карт.",
   875	      "source_excerpt": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства Принимать к оплате все карты из списка в течение всего рабочего времени; Не выдавать наличные деньги по картам; Не принимать более двух ",
   876	      "type": "operative",
   877	      "materiality": "needs_source_review",
   878	      "protected_party": "",
   879	      "bound_party": "",
   880	      "right_or_obligation": "",
   881	      "legal_object": "",
   882	      "trigger": "",
   883	      "deadline": "",
   884	      "amount_formula_cap": "",
   885	      "procedure_channel": "",
   886	      "liability_remedy": "",
   887	      "scope_options": [],
   888	      "consequence": "",
   889	      "applicability_filters": {
   890	        "required_type": "mandatory",
   891	        "only_for_product": "common",
   892	        "only_for_lot": "common",
   893	        "only_for_terminal": "common",
   894	        "payment_method": "common"
   895	      },
   896	      "main_idea": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства",
   897	      "topics": [
   898	        "Принимать к оплате все карты из списка в течение всего рабочего времени",
   899	        "Не выдавать наличные деньги по картам",
   900	        "Не принимать более двух разных карт от одного покупателя"
AI: I now have a good understanding of the scope. This is a very large task. Let me focus on the "contract-extra" review — identifying contract clauses that have no matrix analogue. Let me now read the contract-side of the legal propositions ledger to understand what's already been mapped:[{'name': 'execute', 'args': {'command': 'python -c "\nimport json\nwith open(\'/outputs/working/legal_propositions.json\', \'r\') as f:\n    data = json.load(f)\nprint(\'Matrix count:\', len(data.get(\'matrix\', [])))\nprint(\'Contract count:\', len(data.get(\'contract\', [])))\n# Print contract ids\nfor c in data.get(\'contract\', []):\n    print(f\\"  {c[\'id\']} | type={c[\'type\']} | materiality={c[\'materiality\']}\\")\n"'}, 'id': 'call_00_0s7hlyP0W2L5rUfB8Qb26255', 'type': 'tool_call'}]
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
[stderr] with open('outputs/working/legal_propositions.json', 'r') as f:
[stderr]     data = json.load(f)
[stderr] print('Matrix count:', len(data.get('matrix', [])))
[stderr] print('Contract count:', len(data.get('contract', [])))
[stderr] # Print contract ids
[stderr] for c in data.get('contract', []):
[stderr]     print(f\"  {c['id']} | type={c['type']} | materiality={c['materiality']}\")
[stderr] "
[stderr]   if ($global:LASTEXITCODE -ne $null) { exit $global:LASTEXITCODE }
[stderr]   exit 0
[stderr] } catch {
[stderr]   Write-Error -Message $_.Exception.Message
[stderr]   exit 1
[stderr] }
[stderr]  : The term 'type=' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the sp
[stderr] elling of the name, or if a path was included, verify that the path is correct and try again.
[stderr] At line:45 char:3
[stderr] +   Write-Error -Message $_.Exception.Message
[stderr] +   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[stderr]     + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
[stderr]     + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/check_contract.py'}, 'id': 'call_00_aOd82Ed0YN75wl3jouW67399', 'type': 'tool_call'}]
Tool: [stderr] C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\.venv\Scripts\python.exe: can't open file 'C:\\Users\\gogel\\OneDrive\\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\\РџСЂРѕРµРєС‚С‹\\skillshot_manual_2\\outputs\\working\\check_contract.py': [Errno 2] No such file or directory

Exit code: 2
[Command failed with exit code 2]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/check_contract.py', 'content': 'import json\n\nwith open(\'/outputs/working/legal_propositions.json\', \'r\', encoding=\'utf-8\') as f:\n    data = json.load(f)\n\nprint(\'Matrix count:\', len(data.get(\'matrix\', [])))\nprint(\'Contract count:\', len(data.get(\'contract\', [])))\nprint()\nprint(\'=== CONTRACT PROPOSITIONS ===\')\nfor c in data.get(\'contract\', []):\n    print(f"  {c[\'id\']} | type={c[\'type\']} | materiality={c[\'materiality\']}")\n'}, 'id': 'call_00_SkqaKKYd4zQz6J4TveM59445', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/check_contract.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/check_contract.py'}, 'id': 'call_00_X869h2a2UW3BWm8ATZSm9496', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\check_contract.py", line 3, in <module>
[stderr]     with open('/outputs/working/legal_propositions.json', 'r', encoding='utf-8') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/legal_propositions.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'ls /outputs/working/'}, 'id': 'call_00_wUnPIYtSNoBjNNAjVu3e7442', 'type': 'tool_call'}]
Tool: 

    РљР°С‚Р°Р»РѕРі: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        26.06.2026     12:30            389 check_contract.py                                                    
-a----        26.06.2026     12:27         737755 clause_index.json                                                    
-a----        26.06.2026     12:27         328332 contract_locator_registry.json                                       
-a----        26.06.2026     12:28            481 contract_product_profile.json                                        
-a----        26.06.2026     12:27        1053637 legal_propositions.json                                              
-a----        26.06.2026     12:27            535 source_preflight.json                                                

[Command succeeded with exit code 0]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/check_contract.py', 'content': 'import json, os\n\nbase = os.path.dirname(os.path.abspath(__file__))\npath = os.path.join(base, \'legal_propositions.json\')\n\nwith open(path, \'r\', encoding=\'utf-8\') as f:\n    data = json.load(f)\n\nprint(\'Matrix count:\', len(data.get(\'matrix\', [])))\nprint(\'Contract count:\', len(data.get(\'contract\', [])))\nprint()\nprint(\'=== CONTRACT PROPOSITIONS ===\')\nfor c in data.get(\'contract\', []):\n    print(f"  {c[\'id\']} | type={c[\'type\']} | materiality={c[\'materiality\']}")\n'}, 'id': 'call_00_9fdUsE3YvjIplus58Qq24017', 'type': 'tool_call'}]
Tool: Cannot write to /outputs/working/check_contract.py because it already exists. Read and then make an edit, or write to a new path.
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/check_contract.py'}, 'id': 'call_00_OEr2R76HLG6V9jIL4YfJ4103', 'type': 'tool_call'}]
Tool:      1	import json
     2	
     3	with open('/outputs/working/legal_propositions.json', 'r', encoding='utf-8') as f:
     4	    data = json.load(f)
     5	
     6	print('Matrix count:', len(data.get('matrix', [])))
     7	print('Contract count:', len(data.get('contract', [])))
     8	print()
     9	print('=== CONTRACT PROPOSITIONS ===')
    10	for c in data.get('contract', []):
    11	    print(f"  {c['id']} | type={c['type']} | materiality={c['materiality']}")
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/check_contract.py', 'old_string': "import json\n\nwith open('/outputs/working/legal_propositions.json', 'r', encoding='utf-8') as f:\n    data = json.load(f)", 'new_string': "import json, os\n\nbase = os.path.dirname(os.path.abspath(__file__))\npath = os.path.join(base, 'legal_propositions.json')\n\nwith open(path, 'r', encoding='utf-8') as f:\n    data = json.load(f)"}, 'id': 'call_00_IyOSIoivVIKIULprkTkA1039', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/check_contract.py'
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/check_contract.py'}, 'id': 'call_00_KJ9JIbwl401Ws9JaxacX0430', 'type': 'tool_call'}]
Tool: Matrix count: 169
Contract count: 321

=== CONTRACT PROPOSITIONS ===
  1 | type=operative | materiality=needs_source_review
  1.1 | type=operative | materiality=needs_source_review
  1.2 | type=operative | materiality=needs_source_review
  1.3 | type=operative | materiality=needs_source_review
  2 | type=heading | materiality=heading
  2.1 | type=operative | materiality=needs_source_review
  2.1.1 | type=operative | materiality=needs_source_review
  2.1.2 | type=operative | materiality=needs_source_review
  2.1.3 | type=operative | materiality=needs_source_review
  2.1.4 | type=operative | materiality=needs_source_review
  2.1.5 | type=operative | materiality=needs_source_review
  2.1.6 | type=operative | materiality=needs_source_review
  2.1.7 | type=operative | materiality=needs_source_review
  2.1.8 | type=operative | materiality=needs_source_review
  2.1.9 | type=operative | materiality=needs_source_review
  2.1.10 | type=operative | materiality=needs_source_review
  2.1.11 | type=operative | materiality=needs_source_review
  2.1.12 | type=operative | materiality=needs_source_review
  2.1.13 | type=operative | materiality=needs_source_review
  2.1.14 | type=operative | materiality=needs_source_review
  2.1.15 | type=operative | materiality=needs_source_review
  2.1.16 | type=operative | materiality=needs_source_review
  2.1.17 | type=operative | materiality=needs_source_review
  2.1.18 | type=operative | materiality=needs_source_review
  2.1.19 | type=operative | materiality=needs_source_review
  2.1.20 | type=operative | materiality=needs_source_review
  2.1.21 | type=operative | materiality=needs_source_review
  2.1.22 | type=operative | materiality=needs_source_review
  2.1.23 | type=operative | materiality=needs_source_review
  2.1.24 | type=operative | materiality=needs_source_review
  2.1.25 | type=operative | materiality=needs_source_review
  2.1.26 | type=operative | materiality=needs_source_review
  2.1.27 | type=operative | materiality=needs_source_review
  2.1.28 | type=operative | materiality=needs_source_review
  2.2 | type=operative | materiality=needs_source_review
  2.3 | type=operative | materiality=needs_source_review
  2.3.1 | type=operative | materiality=needs_source_review
  2.3.2 | type=operative | materiality=needs_source_review
  2.3.3 | type=operative | materiality=needs_source_review
  2.3.4 | type=operative | materiality=needs_source_review
  2.3.5 | type=operative | materiality=needs_source_review
  2.3.6 | type=operative | materiality=needs_source_review
  2.3.7 | type=operative | materiality=needs_source_review
  3 | type=operative | materiality=needs_source_review
  3.1 | type=operative | materiality=needs_source_review
  3.1.1 | type=operative | materiality=needs_source_review
  3.2 | type=operative | materiality=needs_source_review
  3.3 | type=operative | materiality=needs_source_review
  4 | type=operative | materiality=needs_source_review
  4.1 | type=operative | materiality=needs_source_review
  4.2 | type=operative | materiality=needs_source_review
  4.3 | type=operative | materiality=needs_source_review
  4.4 | type=operative | materiality=needs_source_review
  4.5 | type=operative | materiality=needs_source_review
  4.5.1 | type=operative | materiality=needs_source_review
  5 | type=operative | materiality=needs_source_review
  5.1 | type=operative | materiality=needs_source_review
  5.1.1 | type=operative | materiality=needs_source_review
  5.1.2 | type=operative | materiality=needs_source_review
  5.1.3 | type=operative | materiality=needs_source_review
  5.1.4 | type=operative | materiality=needs_source_review
  5.1.5 | type=operative | materiality=needs_source_review
  5.1.6 | type=operative | materiality=needs_source_review
  5.1.7 | type=operative | materiality=needs_source_review
  5.1.8 | type=operative | materiality=needs_source_review
  5.1.9 | type=operative | materiality=needs_source_review
  5.1.10 | type=operative | materiality=needs_source_review
  5.2 | type=operative | materiality=needs_source_review
  5.2.1 | type=operative | materiality=needs_source_review
  5.2.2 | type=operative | materiality=needs_source_review
  5.2.3 | type=operative | materiality=needs_source_review
  5.2.4 | type=operative | materiality=needs_source_review
  5.2.5 | type=operative | materiality=needs_source_review
  5.2.6 | type=operative | materiality=needs_source_review
  5.2.7 | type=operative | materiality=needs_source_review
  5.2.8 | type=operative | materiality=needs_source_review
  5.2.9 | type=operative | materiality=needs_source_review
  5.2.9.1 | type=operative | materiality=needs_source_review
  5.2.9.2 | type=operative | materiality=needs_source_review
  5.2.9.3 | type=operative | materiality=needs_source_review
  5.2.9.4 | type=operative | materiality=needs_source_review
  5.2.9.5 | type=operative | materiality=needs_source_review
  5.2.9.6 | type=operative | materiality=needs_source_review
  5.2.9.7 | type=operative | materiality=needs_source_review
  5.2.9.8 | type=operative | materiality=needs_source_review
  5.2.9.9 | type=operative | materiality=needs_source_review
  5.2.9.10 | type=operative | materiality=needs_source_review
  5.2.9.11 | type=operative | materiality=needs_source_review
  5.2.10 | type=operative | materiality=needs_source_review
  5.2.10.1 | type=operative | materiality=needs_source_review
  5.2.10.2 | type=operative | materiality=needs_source_review
  5.2.10.3 | type=operative | materiality=needs_source_review
  5.2.10.4 | type=operative | materiality=needs_source_review
  5.2.10.5 | type=operative | materiality=needs_source_review
  5.3 | type=operative | materiality=needs_source_review
  5.3.1 | type=operative | materiality=needs_source_review
  5.3.2 | type=operative | materiality=needs_source_review
  5.3.3 | type=operative | materiality=needs_source_review
  5.3.4 | type=operative | materiality=needs_source_review
  5.3.5 | type=operative | materiality=needs_source_review
  5.3.6 | type=operative | materiality=needs_source_review
  5.3.7 | type=operative | materiality=needs_source_review
  5.3.8 | type=operative | materiality=needs_source_review
  5.3.9 | type=operative | materiality=needs_source_review
  5.3.10 | type=operative | materiality=needs_source_review
  5.3.11 | type=operative | materiality=needs_source_review
  5.3.12 | type=operative | materiality=needs_source_review
  5.3.13 | type=operative | materiality=needs_source_review
  5.3.14 | type=operative | materiality=needs_source_review
  5.3.15 | type=operative | materiality=needs_source_review
  5.3.16 | type=operative | materiality=needs_source_review
  5.3.17 | type=operative | materiality=needs_source_review
  5.3.18 | type=operative | materiality=needs_source_review
  5.3.18.1 | type=operative | materiality=needs_source_review
  5.3.18.2 | type=operative | materiality=needs_source_review
  5.3.18.3 | type=operative | materiality=needs_source_review
  5.3.20.4 | type=operative | materiality=needs_source_review
  5.3.18.5 | type=operative | materiality=needs_source_review
  5.3.19 | type=operative | materiality=needs_source_review
  5.3.20 | type=operative | materiality=needs_source_review
  5.4 | type=operative | materiality=needs_source_review
  5.4.1 | type=operative | materiality=needs_source_review
  5.4.2 | type=operative | materiality=needs_source_review
  5.4.3 | type=operative | materiality=needs_source_review
  5.4.4 | type=operative | materiality=needs_source_review
  5.4.5 | type=operative | materiality=needs_source_review
  5.5 | type=operative | materiality=needs_source_review
  5.6 | type=operative | materiality=needs_source_review
  5.7 | type=operative | materiality=needs_source_review
  5.9 | type=operative | materiality=needs_source_review
  5.10 | type=operative | materiality=needs_source_review
  6 | type=operative | materiality=needs_source_review
  6.1 | type=operative | materiality=needs_source_review
  7 | type=operative | materiality=needs_source_review
  7.1 | type=operative | materiality=needs_source_review
  7.2 | type=operative | materiality=needs_source_review
  7.3 | type=operative | materiality=needs_source_review
  7.4 | type=operative | materiality=needs_source_review
  7.4.1 | type=operative | materiality=needs_source_review
  7.5 | type=operative | materiality=needs_source_review
  7.6 | type=operative | materiality=needs_source_review
  7.7 | type=operative | materiality=needs_source_review
  7.7.1 | type=operative | materiality=needs_source_review
  7.7.2 | type=operative | materiality=needs_source_review
  10 | type=operative | materiality=needs_source_review
  5 | type=operative | materiality=needs_source_review
  1 | type=operative | materiality=needs_source_review
  10 | type=operative | materiality=needs_source_review
  5 | type=operative | materiality=needs_source_review
  1 | type=operative | materiality=needs_source_review
  7.7.3 | type=operative | materiality=needs_source_review
  7.8 | type=operative | materiality=needs_source_review
  7.9 | type=operative | materiality=needs_source_review
  7.10 | type=operative | materiality=needs_source_review
  7.11 | type=operative | materiality=needs_source_review
  7.12 | type=operative | materiality=needs_source_review
  8 | type=operative | materiality=needs_source_review
  8.1 | type=operative | materiality=needs_source_review
  8.2 | type=operative | materiality=needs_source_review
  8.3 | type=operative | materiality=needs_source_review
  8.3.1 | type=operative | materiality=needs_source_review
  8.3.2 | type=operative | materiality=needs_source_review
  8.4 | type=operative | materiality=needs_source_review
  8.5 | type=operative | materiality=needs_source_review
  8.5.1 | type=operative | materiality=needs_source_review
  8.5.2 | type=operative | materiality=needs_source_review
  8.5.3 | type=operative | materiality=needs_source_review
  8.5.4 | type=operative | materiality=needs_source_review
  8.5.5 | type=operative | materiality=needs_source_review
  8.5.6 | type=operative | materiality=needs_source_review
  8.5.7 | type=operative | materiality=needs_source_review
  8.5.8 | type=operative | materiality=needs_source_review
  8.5.9 | type=operative | materiality=needs_source_review
  8.6 | type=operative | materiality=needs_source_review
  8.7 | type=operative | materiality=needs_source_review
  8.8 | type=operative | materiality=needs_source_review
  8.9 | type=operative | materiality=needs_source_review
  8.10 | type=operative | materiality=needs_source_review
  8.11 | type=operative | materiality=needs_source_review
  9 | type=operative | materiality=needs_source_review
  9.1 | type=operative | materiality=needs_source_review
  9.2 | type=operative | materiality=needs_source_review
  9.3 | type=operative | materiality=needs_source_review
  10 | type=operative | materiality=needs_source_review
  10.1 | type=operative | materiality=needs_source_review
  10.2 | type=operative | materiality=needs_source_review
  11 | type=operative | materiality=needs_source_review
  11.1 | type=operative | materiality=needs_source_review
  11.2 | type=operative | materiality=needs_source_review
  11.3 | type=operative | materiality=needs_source_review
  11.4 | type=operative | materiality=needs_source_review
  11.5 | type=operative | materiality=needs_source_review
  11.6 | type=operative | materiality=needs_source_review
  11.7 | type=operative | materiality=needs_source_review
  11.8 | type=operative | materiality=needs_source_review
  12 | type=operative | materiality=needs_source_review
  12.1 | type=operative | materiality=needs_source_review
  12.2 | type=operative | materiality=needs_source_review
  12.3 | type=operative | materiality=needs_source_review
  12.4 | type=operative | materiality=needs_source_review
  12.5 | type=operative | materiality=needs_source_review
  13 | type=operative | materiality=needs_source_review
  354340 | type=operative | materiality=needs_source_review
  1 | type=operative | materiality=needs_source_review
  2 | type=operative | materiality=needs_source_review
  3 | type=operative | materiality=needs_source_review
  4 | type=operative | materiality=needs_source_review
  5 | type=operative | materiality=needs_source_review
  9.2.1 | type=operative | materiality=needs_source_review
  1 | type=operative | materiality=needs_source_review
  2 | type=operative | materiality=needs_source_review
  3 | type=operative | materiality=needs_source_review
  1.1 | type=operative | materiality=needs_source_review
  1.2 | type=operative | materiality=needs_source_review
  1.3 | type=operative | materiality=needs_source_review
  4 | type=operative | materiality=needs_source_review
  10 | type=operative | materiality=needs_source_review
  1 | type=operative | materiality=needs_source_review
  1 | type=operative | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1 | type=appendix | materiality=not_material
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ | type=table | materiality=not_material
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 295 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / Рї.1 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / Рї.2 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 315 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 324 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / Рї.3 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 331 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / Рї.4 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / Рї.5 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 338 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 339 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 340 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 341 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 342 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 343 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 345 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 346 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 347 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 349 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 350 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 351 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 352 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 353 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 354 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 355 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 356 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 357 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 358 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 361 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 362 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 363 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 364 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 369 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 372 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 375 | type=table | materiality=needs_source_review
  РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ / СЃС‚СЂРѕРєР° 378 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 | type=appendix | materiality=not_material
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 382 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 383 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 397 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / Рї.2 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 399 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 400 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 403 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 408 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 409 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / Рї.1.3 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1.1 / СЃС‚СЂРѕРєР° 424 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 | type=appendix | materiality=not_material
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 431 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 449 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 450 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 456 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 463 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 464 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 465 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 466 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 467 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 468 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 469 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 471 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 476 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 477 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 478 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 484 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 485 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 486 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 495 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 500 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 503 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 504 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 508 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 509 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 512 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 513 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 516 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 517 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 520 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 521 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 522 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 524 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 528 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 529 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 532 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 534 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 536 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 544 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 545 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 549 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 551 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 553 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 559 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 560 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 1..2 / СЃС‚СЂРѕРєР° 569 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 | type=appendix | materiality=not_material
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 / СЃС‚СЂРѕРєР° 579 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 / СЃС‚СЂРѕРєР° 580 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 / СЃС‚СЂРѕРєР° 582 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 / СЃС‚СЂРѕРєР° 585 | type=table | materiality=needs_source_review
  РџСЂРёР»РѕР¶РµРЅРёРµ в„– 2 / СЃС‚СЂРѕРєР° 588 | type=table | materiality=needs_source_review

[Command succeeded with exit code 0]
AI: Now I have a clear picture. The contract has 321 propositions, most marked `needs_source_review`. The task is to identify which contract clauses are `extra_in_contract` (no matrix analogue) and which are `not_material`. Let me now understand the full matrix scope and then systematically identify contract-only terms.

Let me get the full list of matrix IDs and their applicability:[{'name': 'write_file', 'args': {'file_path': '/outputs/working/analyze_matrix.py', 'content': 'import json, os\n\nbase = os.path.dirname(os.path.abspath(__file__))\n\n# Load matrix\nwith open(os.path.join(base, \'..\', \'..\', \'inputs\', \'matrix.json\'), \'r\', encoding=\'utf-8\') as f:\n    matrix = json.load(f)\n\nprint(f"Total matrix items: {len(matrix)}")\nprint()\n\n# Group by applicability\nfor m in matrix:\n    n = m[\'number\']\n    rt = m.get(\'required_type\', \'\')\n    prod = m.get(\'only_for_product\', \'\')\n    lot = m.get(\'only_for_lot\', \'\')\n    term = m.get(\'only_for_terminal\', \'\')\n    pm = m.get(\'payment_method\', \'\')\n    mi = m.get(\'main_idea\', \'\')[:80]\n    print(f"  {n} | req={rt} | prod={prod} | lot={lot} | term={term} | pm={pm} | {mi}")\n'}, 'id': 'call_00_Bzuxq9FLdl3xq0IqAURF1895', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/analyze_matrix.py
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/analyze_matrix.py 2>&1 | head -200'}, 'id': 'call_00_o7jfQukKy6YFKV2SnGdB6658', 'type': 'tool_call'}]
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
[stderr] python outputs/working/analyze_matrix.py 2>&1 | head -200
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
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/analyze_matrix.py'}, 'id': 'call_00_eyGycAZIgwkLXpBbXj1n6426', 'type': 'tool_call'}]
Tool: Total matrix items: 169

  2.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РґР»СЏ СЂРµРіРёСЃС‚СЂР°С†РёРё РґРѕРіРѕРІРѕСЂР° Р±Р°РЅРєСѓ РЅСѓР¶РЅРѕ Р·Р°СЏРІР»РµРЅРёРµ. Р’ Р·Р°СЏРІР»РµРЅРёРё РґРѕР»Р¶
  2.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РІР°Р»СЋС‚Р° СЂСѓР±Р»СЊ Р Р¤, РґСЂСѓРіР°СЏ РІР°Р»СЋС‚Р° РЅРµРґРѕРїСѓСЃС‚РёРјР°
  2.3.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | РќСѓР¶РЅРѕ РїСЂРѕРІРµСЂСЏС‚СЊ РїСЂРёР·РЅР°С‘С‚СЃСЏ Р»Рё РїРѕР»РЅР°СЏ СЋСЂРёРґРёС‡РµСЃРєР°СЏ СЃРёР»Р° eвЂ‘mail, РµСЃС‚СЊ Р»Рё РѕРіСЂР°РЅРёС‡РµРЅРё
  2.3.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕС‚РїСЂР°РІРєРё РёРЅС„РѕСЂРјР°С†РёРё / РґРѕРєСѓРјРµРЅС‚РѕРІ С‚Р°РєРёРј СЃРїРѕСЃРѕР±РѕРј
  2.3.3 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕС‚РїСЂР°РІРєРё РёРЅС„РѕСЂРјР°С†РёРё / РґРѕРєСѓРјРµРЅС‚РѕРІ С‚Р°РєРёРј СЃРїРѕСЃРѕР±РѕРј
  2.3.4 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕС‚РїСЂР°РІРєРё РёРЅС„РѕСЂРјР°С†РёРё / РґРѕРєСѓРјРµРЅС‚РѕРІ С‚Р°РєРёРј СЃРїРѕСЃРѕР±РѕРј
  2.3.5 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅР° СЂР°РІРЅРѕР·РЅР°С‡РЅРѕСЃС‚СЊ РґРѕРєСѓРјРµРЅС‚РѕРІ
  2.3.6 | req=mandatory | prod=common | lot=fz_44 | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅР°Р»РёС‡РёСЏ РґР°РЅРЅРѕРіРѕ РєР°РЅР°Р»Р° РґР»СЏ РѕР±РјРµРЅР° СЌР»РµРєС‚СЂРѕРЅРЅС‹РјРё РґРѕРєСѓРјРµРЅС‚Р°РјРё
  2.3.7 | req=optional | prod=common | lot=common | term=common | pm=common | Р”Р»СЏ РїСЂРµРґСЃС‚Р°РІР»РµРЅРЅС‹С… РІ РєРѕРЅС‚СЂР°РєС‚Рµ СЃРїРѕСЃРѕР±Р°С… РѕР±РјРµРЅР° РёРЅС„РѕСЂРјР°С†РёРµР№ / РґРѕРєСѓРјРµРЅС‚Р°РјРё, РЅРµ РґРѕР»
  2.4 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ РїСЂРёР·РЅР°РЅРёРµ СЃСЃС‹Р»РѕРє Рё РґРѕРєСѓРјРµРЅС‚РѕРІ РІ РґРѕРіРІРѕСЂРµ РµРіРѕ РЅРµРѕС‚СЉРµРјР»РµРјРѕР№ С‡Р°СЃС‚СЊСЋ
  2.5.1.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р±РµСЃРєРѕРЅС‚Р°РєС‚РЅР°СЏ РѕРїР»Р°С‚Р° РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё
  2.5.2.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=sber_pay_face_scan | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїСЂРёРЅСЏС‚РёСЏ РѕРїР»Р°С‚С‹ РїРѕ Р±РёРѕРјРµС‚СЂРёРё РѕС„РѕСЂРјР»СЏРµС‚СЃСЏ РѕС‚РґРµР»СЊРЅС‹Рј Р·
  2.6.1.1 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=qr | Р”Р»СЏ РїСЂРёРµРјР° QR РЅР° СЃРјР°СЂС‚-С‚РµСЂРјРёРЅР°Р» РЅРµ РЅСѓР¶РЅРѕ РѕС‚РґРµР»СЊРЅРѕРµ РџРћ
  2.6.2.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | Р’РђР–РќРћ РїСЂРѕРІРµСЂРёС‚СЊ, С‡С‚Рѕ РІ РґРѕРіРѕРІРѕСЂРµ РёРґС‘С‚ СЂРµС‡СЊ Рѕ РЎРћР‘РЎРўР’Р•РќРќР«РҐ С‚РµСЂРјРёРЅР°Р»Р°С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ. 
  2.6.2.2 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | Р’РђР–РќРћ РїСЂРѕРІРµСЂРёС‚СЊ, С‡С‚Рѕ РІ РґРѕРіРѕРІРѕСЂРµ РёРґС‘С‚ СЂРµС‡СЊ Рѕ РЎРћР‘РЎРўР’Р•РќРќР«РҐ С‚РµСЂРјРёРЅР°Р»Р°С… РџСЂРµРґРїСЂРёСЏС‚РёСЏ. 
  2.6.3.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | Р”Р°РЅРЅС‹Р№ СЂРёСЃРє РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє С‚РµСЂРјРёРЅР°Р»Р°Рј РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹Рј Р‘Р°РЅРєРѕРј. Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚
  2.6.3.2 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=qr | Р”Р°РЅРЅС‹Р№ СЂРёСЃРє РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє С‚РµСЂРјРёРЅР°Р»Р°Рј РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРЅС‹Рј Р‘Р°РЅРєРѕРј. Р”Р»СЏ РѕС‚РєР»СЋС‡РµРЅРёСЏ
  2.7 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РґРѕРіРѕРІРѕСЂ РјРѕР¶РµС‚ Р±С‹С‚СЊ Р·Р°РєР»СЋС‡РµРЅ РІ СЌР»РµРєС‚СЂРѕРЅРЅРѕРј РІРёРґРµ СЃ РїРѕРґРїРёСЃР°РЅРёРµРј РЈРљР­
  3.1 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ РїРѕРґСЃРІРµС‚РёС‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё РїРµСЂРµС‡РёСЃР»РµРЅР° РїР»Р°С‚С‘Р¶РЅР°СЏ СЃРёСЃС‚РµРјР° РѕС‚Р»РёС‡РЅР°СЏ РѕС‚ РќРЎРџ
  3.2 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё Р‘Р°РЅРєР° РІ РїРµСЂРµС‡РёСЃР»РµРЅРёРё СЃСѓРјРј РџСЂРµРґРїСЂРёСЏС‚РёСЋ
  3.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёСЏ РґРѕР»Р¶РЅРѕ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё РїСЂРµРґРѕСЃС‚Р°РІР»СЏРµРјС‹Рµ РїРѕ РґРѕРіРѕ
  4.1.1 | req=optional | prod=common | lot=common | term=common | pm=qr | Р’Р°Р¶РЅРѕ, РµСЃР»Рё РџСЂРµРґРїСЂРёСЏС‚РёРµ С…РѕС‡РµС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РІ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»Р°С… СѓРїРѕРјРёРЅР°РЅРё
  4.1.2 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РѕРєР°Р·С‹РІР°РµС‚ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЋ Р·Р°РєР°Р·С‡РёРєР° РїРѕ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЋ РѕР±РѕСЂСѓ
  4.1.3 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr_sber_pay | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ QR РІС‹РґР°С‘С‚ Р‘Р°РЅРє
  4.2.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ РїСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РѕРїР»Р°С‡РёРІР°С‚СЊ СѓСЃР»СѓРіРё
  4.2.2 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ РІ РєРѕРЅС‚СЂР°РєС‚Рµ РЅР°Р»РёС‡РёРµ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё Рѕ С‚РѕРј, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РѕР±СЏР·СѓРµС‚СЃСЏ РІС‹РїРѕР»РЅСЏС‚
  4.2.3 | req=optional | prod=common | lot=fz_223 | term=common | pm=common | 
  4.2.4 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, РµСЃР»Рё Р±Р°РЅРє РїРµСЂРµРґР°РµС‚ РїРѕ РґРѕРіРѕРІРѕСЂСѓ РїСЂРµРґРїСЂРёСЏС‚РёСЋ - Р·Р°РєР°Р·С‡РёРєСѓ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹
  4.2.5 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, РЅРµ РїСЂРёРЅРёРјР°С‚СЊ РѕС‚ РџРѕРєСѓРїР°С‚РµР»СЏ Р±РѕР»РµРµ 2 (РґРІСѓС…) СЂР°Р·Р»РёС‡РЅС‹С… РљР°СЂС‚. РќРµ РІС‹РґР°РІР°С‚СЊ РЅР°Р»
  4.2.6 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РЅРµР»СЊР·СЏ СЂР°Р·Р±РёРІР°С‚СЊ РћРїРµСЂР°С†РёСЋ РЅР° РЅРµСЃРєРѕР»СЊРєСѓ СЃСѓРјРј
  4.2.7 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  4.2.8 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С†РµРЅР° РЅРµ Р·Р°РІРёСЃРёС‚ РѕС‚ СЃРїРѕСЃРѕР±Р° РѕРїР»Р°С‚С‹
  4.2.9 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р—Р°РєР°Р·С‡РёРє РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РёРЅС„РѕСЂРјР°С†РёСЋ РєРѕС‚РѕСЂСѓСЋ РѕРЅ СѓРєР°Р·С‹РІР°РµС‚ РІ РґРѕРєСѓРјРµРЅС‚Р°С… Рї
  4.2.10 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё С…СЂР°РЅРµРЅРёСЏ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїРµСЂР°С†РёСЏРј, СЃСЂРѕРє РІ С‚РµС‡РµРЅРёРё РєРѕС‚РѕСЂРѕРі
  4.2.11 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїРµСЂРµРґР°РІР°С‚СЊ Р·Р°СЏРІР»РµРЅРёРµ Р‘Р°РЅРєСѓ, Р° С‚Р°Рє Р¶Рµ СЃСЂРѕРєРё РІ С‚РµС‡РµРЅРёРµ РєРѕС‚Рѕ
  4.2.12 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РїРѕРґРїРёСЃР°С‚СЊ Р·Р°РєСЂС‹РІР°СЋС‰РёРµ РґРѕРєСѓРјРµРЅС‚С‹ РїРѕ РѕРїР»Р°С‚Рµ, Р° 
  4.2.13 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РџСЂРµРґРїСЂРёСЏС‚РёСЏ РІРѕР·РјРµС‰Р°С‚СЊ РІСЃРµ СЃСѓРјРјС‹ Рё СѓР±С‹С‚РєРё, РєРѕС‚РѕСЂС‹Рµ Р‘Р°РЅ
  4.2.14 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚ РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ РїРѕРґС‚РІРµСЂР¶РґР°СЋС‰РёС… РґРѕРєСѓРјРµРЅС‚РѕРІ, РІР°Р¶РЅС‹ СЃСЂРѕРєРё РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёСЏ,
  4.2.15 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё РїСЂРµРґРѕСЃС‚Р°РІР»СЏС‚СЊ РґРѕСЃС‚РѕРІРµСЂРЅС‹Рµ СЃРІРµРґРµРЅРёСЏ, СЃРІРѕРµРІСЂРµРјРµРЅРЅРѕРµ РѕР±РЅРѕРІ
  4.2.16.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ Р±С‹Р»Рѕ РґРµР№СЃС‚РІСѓСЋС‰РµРµ СЃРѕРіР»Р°СЃРёРµ РЅР° РїРµСЂРµРґР°С‡Сѓ РџР”РЅ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ РџСЂРµРґРїСЂРёСЏС‚РёСЏ.
  4.2.16.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ РєРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј РєСЂРѕРјРµ СЂСѓРєРѕРІРѕРґРёС‚РµР»СЏ, РІР°Р¶РЅРѕ 
  4.2.16.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РґР°РЅРЅС‹Р№ РїСѓРЅРєС‚ РѕС‚РЅРѕСЃРёС‚СЃСЏ С‚РѕР»СЊРєРѕ Рє РґР°РЅРЅС‹Рј РїРѕ РІСЃРµРј СЃРѕС‚СЂСѓРґРЅРёРєР°Рј. Р’Р°Р¶РµРЅ СЃСЂРѕ
  4.2.17 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё СЃРѕР±Р»СЋРґРµРЅРёСЏ СЃС‚Р°РЅРґР°СЂС‚Р°, Р° С‚Р°Рє Р¶Рµ С„Р°РєС‚ РѕР±СЏР·Р°РЅРЅРѕСЃС‚Рё РїСЂРµРґРѕ
  4.2.18 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅС‹ С„Р°РєС‚С‹ РїСЂРµРєСЂР°С‰РµРЅРёСЏ РїСЂРёРµРјР° Рє РѕРїР»Р°С‚Рµ РљР°СЂС‚, СЃРЅСЏС‚РёСЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹С… РјР°С‚РµСЂРёР°Р»РѕРІ, 
  4.2.19 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ, С„Р°РєС‚ С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РЅРµ РґРѕР»Р¶РЅРѕ РјРµС€Р°С‚СЊ Р‘Р°РЅРєСѓ, Рё С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ РґРѕР»Р¶
  4.2.20.1 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ РџСЂРµРґРїСЂРёСЏС‚РёРµ СЃР°РјРѕ СЃР»РµРґРёС‚ Р·Р° РїСЂРѕС…РѕР¶РґРµРЅРёРµРј РёРЅСЃС‚СЂСѓРєС‚Р°Р¶Р° СЃРѕС‚СЂСѓРґРЅРё
  4.2.20.2 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РїСЂРµРґРїСЂРёСЏС‚РёРµ РёСЃРїРѕР»СЊР·РѕРІР°Р»Рѕ С‚РµСЂРјРёРЅР°Р»С‹ Рё РџРћ Р‘Р°РЅРєР° С‚РѕР»СЊРєРѕ РґР»СЏ С†РµР»РµР№ РґРѕРіРѕ
  4.2.20.3 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ СЃС‚РѕРёС‚ Р·Р°РїСЂРµС‚ РЅР° РїСЂРµРґРѕСЃС‚Р°РІР»РµРЅРёРµ РґРѕСЃС‚СѓРїР° С‚СЂРµС‚СЊРёРј Р»РёС†Р°Рј,
  4.2.20.4 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, РµСЃР»Рё СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕР±РѕСЂСѓРґРѕРІР°РЅРёРµ РџСЂРµРґРїСЂРёСЏС‚РёРµ Р±РµР· РґРѕРєСѓРјРµРЅС‚РѕРІ РёР»Рё Р°РєС‚Р° РїРµСЂРµРґР°
  4.2.20.5 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | 
  4.2.20.6 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | 
  4.2.20.7 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРј РїСѓРЅРєС‚Рµ РґРѕРіРѕРІРѕСЂР° С€Р»Р° СЂРµС‡СЊ РїСЂРѕ С€С‚СЂР°С„ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚
  4.2.21.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.2 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.3 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.4 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.5 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.6 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.7 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.21.8 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  4.2.22 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
  4.2.23 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-РєРѕРґ
  4.2.24 | req=optional | prod=common | lot=common | term=common | pm=qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
  4.2.25 | req=optional | prod=common | lot=common | term=common | pm=qr | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РїСѓРЅРєС‚Рµ Р±С‹Р»Рѕ РїСЂСЏРјРѕ СѓРєР°Р·Р°РЅРѕ, С‡С‚Рѕ РѕРЅ РїСЂРѕ QR-API
  4.2.26 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  5.1.1.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.1.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.1.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.1.4 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.1.5 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.1.6 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’РѕР·РјРѕР¶РЅРѕСЃС‚СЊ СѓРґРµСЂР¶Р°РЅРёСЏ С€С‚СЂР°С„РѕРІ Р·Р° РЅРµРІРѕР·РІСЂР°С‚ С‚РµСЂРјРёРЅР°Р»РѕРІ. 
  5.1.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.4 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.5 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.6 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.7 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.8.1 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.2 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.3 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.4 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=common | 
  5.1.8.5 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=common | 
  5.1.8.6 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.7 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.8 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common | 
  5.1.8.9 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.10 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.11 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.12 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.8.13 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.9 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.10 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.11 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.12 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.13 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ РёРјРµРЅРЅРѕ СЂР°Р·РјРµС‰РµРЅРёРµ РёРЅС„РѕСЂРјР°С†РёРё РЅР° СЃР°Р№С‚Рµ. Р•СЃР»Рё РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ РёРЅС‹Рµ СЃРїРѕСЃРѕР±С‹ СѓРІРµ
  5.1.14 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.15 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.1.16 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.1.17.1 | req=optional | prod=trade_acquiring | lot=common | term=pos | pm=common | 
  5.1.17.2 | req=optional | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  5.2.1 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  5.2.2 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  5.2.3 | req=mandatory | prod=trade_acquiring | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹ РІ РґРѕРіРѕРІРѕСЂРµ СЃСЂРѕРє СѓСЃС‚Р°РЅРѕРІРєРё Р±С‹Р» РЅРµ РјРµРЅРµРµ 3 СЂР°Р±РѕС‡РёС… РґРЅРµР№. РЎСЂРѕРє РёРЅСЃС‚СЂСѓРє
  5.2.4 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.2.5 | req=optional | prod=common | lot=common | term=common | pm=common | РџРѕРґСЃРІРµС‡РёРІР°С‚СЊ СЂР°Р·РЅРѕРіР»Р°СЃРёРµ, РµСЃР»Рё С‚РѕР»СЊРєРѕ СЃР°Р№С‚С‹ РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РІРјРµСЃС‚Рѕ СЃ
  5.2.6 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=common | 
  5.2.7 | req=optional | prod=common | lot=common | term=common | pm=common | 
  5.2.8 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃСЂРѕРє РїРµСЂРµС‡РёСЃР»РµРЅРёСЏ СЃСЂРµРґСЃС‚РІ
  5.2.9 | req=optional | prod=trade_acquiring | lot=common | term=common | pm=qr | 
  5.2.10 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  5.2.12 | req=optional | prod=internet_acquiring | lot=common | term=common | pm=qr | 
  6.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ
  6.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | РЈРџР” - СЌС‚Рѕ СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РїРµСЂРµРґР°С‚РѕС‡РЅС‹Р№ РґРѕРєСѓРјРµРЅС‚ (РґРѕРєСѓРјРµРЅС‚ Рѕ РїСЂРёС‘РјРєРµ, РґРѕРєСѓРјРµРЅС‚ РЅР° Рѕ
  6.3 | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common | 
  6.4 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  6.5 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  6.6 | req=mandatory | prod=common | lot=fz_223 | term=common | pm=common | 
  6.7 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.8 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.9 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | 
  6.10 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.11 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.12 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | 
  6.13 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.14 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.15 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | 
  6.16 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.17 | req=mandatory | prod=trade_acquiring | lot=common | term=smart | pm=common | 
  6.18 | req=mandatory | prod=trade_acquiring | lot=fz_223 | term=smart | pm=common | 
  6.20 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє РЅРµ Р±РµСЂС‘С‚ РЅРѕРІСѓСЋ РєРѕРјРёСЃСЃРёСЋ, Р° С‚Р°Рє Р¶Рµ, С‡С‚Рѕ РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅР°СЏ Рє
  6.21 | req=mandatory | prod=common | lot=common | term=common | pm=common | РћС‚СЃСѓС‚СЃС‚РІРёРµ РєРѕРЅРєСЂРµС‚РЅРѕР№ С†РµРЅРЅС‹ РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕС‚РёРІРѕСЂРµС‡РёРµРј
  7.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚Рѕ С€С‚СЂР°С„ РёРјРµРЅРЅРѕ РџСЂРµРґРїСЂРёСЏС‚РёСЋ, РІР°Р¶РµРЅ СЂР°Р·РјРµСЂ С€С‚СЂР°С„Р°
  7.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.4 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.5 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.6 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.7 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.8 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ С„Р°РєС‚, С‡С‚Рѕ Р‘Р°РЅРє (Р�СЃРїРѕР»РЅРёС‚РµР»СЊ) РЅРµ РЅРµСЃРµС‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё РїРѕ СЃРїРѕСЂР°Рј Рё СЂР°Р·РЅРѕРіР»Р°
  7.9 | req=optional | prod=common | lot=common | term=common | pm=common | 
  7.10 | req=optional | prod=common | lot=common | term=common | pm=common | 
  7.11 | req=optional | prod=common | lot=common | term=common | pm=common | 
  7.12 | req=optional | prod=common | lot=common | term=common | pm=common | 
  7.13 | req=mandatory | prod=internet_acquiring | lot=common | term=common | pm=common | 
  7.14 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.15 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃР°Рј С„Р°РєС‚ РЅРµСЃРµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё, РµСЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ РіРѕРІРѕСЂРёС‚СЃСЏ РїСЂРѕ РЅРµСЃРµРЅРёРµ
  7.16 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  7.17 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ, С‡С‚РѕР±С‹  РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ Р±С‹Р»Рѕ СЃСѓР¶РµРЅРёСЏ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё.
  8.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  8.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  9.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  9.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РµРЅ СЃСЂРѕРє СЂР°СЃСЃРјРѕС‚СЂРµРЅРёСЏ РїСЂРµС‚РµРЅР·РёР№
  9.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  10.1 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  10.2 | req=mandatory | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ РѕРїРёСЃР°РЅРёРµ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё СЂР°СЃС‚РѕСЂРіРЅСѓС‚СЊ РґРѕРіРѕРІРѕСЂ РІ РѕРґРЅРѕСЃС‚РѕСЂРѕРЅРЅРµРј РїРѕСЂСЏРґРєРµ. Р’Р°Р¶РµРЅ СЃСЂ
  10.3 | req=mandatory | prod=common | lot=common | term=common | pm=common | 
  11.1 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.2 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.3 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.4 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.5 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.6 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.7 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.8 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.9 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.10 | req=optional | prod=common | lot=common | term=common | pm=common | 
  11.11 | req=optional | prod=common | lot=common | term=common | pm=common | Р•СЃР»Рё РІ РґРѕРіРѕРІРѕСЂРµ РЅРµ СѓРєР°Р·Р°РЅ СЃР°Р№С‚ - СЌС‚Рѕ РЅРµ СЏРІР»СЏРµС‚СЃСЏ СЂР°Р·РЅРѕРіР»Р°СЃРёРµРј
  11.12 | req=optional | prod=common | lot=common | term=common | pm=common | Р’Р°Р¶РЅРѕ СЃР°РјРѕ РЅР°Р»РёС‡РёРµ С‚Р°РєРѕР№ РёР»Рё РїРѕС…РѕР¶РµР№ С„РѕСЂРјСѓР»РёСЂРѕРІРєРё
  11.13 | req=optional | prod=common | lot=common | term=common | pm=common | 

[Command succeeded with exit code 0]
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix.json to understand all matrix IDs and their applicability filters', 'status': 'completed'}, {'content': 'Read full contract.txt to understand all contract clauses', 'status': 'completed'}, {'content': 'Read full legal_propositions.json (contract side) to understand existing contract propositions', 'status': 'completed'}, {'content': 'Read full contract_locator_registry.json to know all final_allowed locators', 'status': 'completed'}, {'content': 'Identify contract-only terms (extra_in_contract) - contract clauses with no matrix analogue', 'status': 'in_progress'}, {'content': 'Identify not_material contract clauses for coverage_ledger.contract', 'status': 'pending'}, {'content': 'Produce unmatched_contract fragment and coverage_ledger.contract rows', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Fix any validation errors and finalize', 'status': 'pending'}]}, 'id': 'call_00_tXakpLnHveDyo3yCuw9k3080', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix.json to understand all matrix IDs and their applicability filters', 'status': 'completed'}, {'content': 'Read full contract.txt to understand all contract clauses', 'status': 'completed'}, {'content': 'Read full legal_propositions.json (contract side) to understand existing contract propositions', 'status': 'completed'}, {'content': 'Read full contract_locator_registry.json to know all final_allowed locators', 'status': 'completed'}, {'content': 'Identify contract-only terms (extra_in_contract) - contract clauses with no matrix analogue', 'status': 'in_progress'}, {'content': 'Identify not_material contract clauses for coverage_ledger.contract', 'status': 'pending'}, {'content': 'Produce unmatched_contract fragment and coverage_ledger.contract rows', 'status': 'pending'}, {'content': 'Validate fragment with validate_fragment.py', 'status': 'pending'}, {'content': 'Fix any validation errors and finalize', 'status': 'pending'}]

