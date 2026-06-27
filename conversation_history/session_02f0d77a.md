## Summarized at 2026-06-27T05:52:54.556969+00:00

Human: 
Read `inputs/matrix.json` and `inputs/contract.txt`, perform the many-to-many
discrepancy analysis, verify you covered every matrix id and every material
contract clause, and write `outputs/discrepancy_analysis.json`.

AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-single-agent-review/SKILL.md', 'limit': 1000}, 'id': 'call_00_76EPg04j96AbV0OB6IEd4029', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json'}, 'id': 'call_01_lUPQHieA9zhWRtSX3rvF5391', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'inputs/contract.txt'}, 'id': 'call_02_NIkW5Yam9K1m7LrIbQT47612', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-single-agent-review
     3	description: "Reference: legal review of an acquiring contract against a Bank standard matrix. Finds aligned coverage, deviations, missing matrix requirements, out-of-scope matrix rows, and material contract-only terms."
     4	---
     5	
     6	# Acquiring Single Agent Review
     7	
     8	## Purpose
     9	
    10	Review a counterparty acquiring contract against the Bank's standard matrix.
    11	The matrix is the Bank's playbook: it states the rights, duties, procedures,
    12	protections, products, and risk allocation the Bank expects to see.
    13	
    14	The goal is a source-grounded legal coverage report:
    15	
    16	- which matrix requirements are preserved by the contract;
    17	- which true analogues exist but deviate from the Bank standard;
    18	- which applicable matrix requirements are missing from the contract;
    19	- which material contract terms have no matrix analogue and create extra risk.
    20	
    21	This is a many-to-many comparison. One contract clause can cover several
    22	matrix requirements, and several contract clauses can collectively satisfy one
    23	matrix requirement.
    24	
    25	## Source Of Truth
    26	
    27	Use the source text as authority:
    28	
    29	- matrix `enriched_text`, `main_idea`, `topics`, `required_type`, and
    30	  applicability filters;
    31	- `inputs/contract.txt` and the exact printed contract locators visible there.
    32	
    33	Pre-normalized matrix propositions can help navigation. They do not replace
    34	the matrix source text. Final links and statuses must be grounded in the
    35	matrix source text and contract source text.
    36	
    37	Re-read source text before deciding hard terms: deadlines, amounts, formulas,
    38	caps, penalties, protected party, bound party, trigger, procedure, forum,
    39	termination, liability, and consequence.
    40	
    41	Every final `contract_id` must be a locator visible in the contract text. Do
    42	not invent suffixes, translated ids, semantic ids, or range labels as final
    43	contract ids. Use explanation fields for interpretation.
    44	
    45	Keep matrix ids and contract ids in separate namespaces even when printed
    46	numbers match. A contract clause `5.1.3` and a matrix row `5.1.3` are different
    47	source objects until their texts pass the analogue threshold.
    48	
    49	## Review Stance
    50	
    51	Protect the Bank standard. The main risk is missing an applicable Bank
    52	protection, missing a material deviation, or failing to report a material
    53	contract-only term.
    54	
    55	Do not create artificial risk from formal wording differences. Labels, party
    56	aliases, document names, procurement mechanics, or broader Bank protections are
    57	not deviations when the legal result required by the matrix is preserved.
    58	
    59	When a public-procurement or mandatory-law mechanism replaces Bank template
    60	wording, compare legal effect rather than labels. It can be an analogue, a
    61	deviation, an extra term, or the reason a matrix row is not applicable.
    62	
    63	## Output
    64	
    65	Write the final artifact to `outputs/discrepancy_analysis.json`.
    66	
    67	- `analysis_profile`;
    68	- `links` with `relationship: aligned|deviation`;
    69	- `unmatched_matrix` for `missing_in_contract`;
    70	- `unmatched_contract` for `extra_in_contract`;
    71	- `coverage_ledger.matrix`;
    72	- `coverage_ledger.contract`;
    73	- `summary`.
    74	
    75	Do not put missing or extra items in `links`. `aligned` links must have empty
    76	`discrepancies`. `deviation` links must name the material legal gap and explain
    77	why it matters for the Bank. Make `summary` counts match the final arrays.
    78	Use `references/output-contract.md` for the exact machine-readable schema.
    79	
    80	`not_material` is only an internal contract closure. Do not include
    81	not-material clauses in the final business report.
    82	
    83	## Workflow
    84	
    85	### Step 1: Orient
    86	
    87	Read enough of both sources to determine:
    88	
    89	- product and payment method;
    90	- terminal/device scope;
    91	- lot and legal regime;
    92	- 44-FZ, 223-FZ, commercial, or common mechanics;
    93	- active and inactive product/channel options;
    94	- party roles despite local labels such as customer, contractor, executor,
    95	  provider, supplier, merchant, enterprise, or Bank.
    96	
    97	Close a matrix row as `out_of_scope` or `not_applicable` only when source text,
    98	matrix filters, or the contract profile make it inactive. Do not scope out
    99	common or optional rows merely because no analogue was found.
   100	
   101	Do not use `not_applicable` as a softer version of missing. If the matrix
   102	filter matches the contract profile but the contract lacks the required product
   103	mechanism, QR procedure, smart-terminal fee, Bank right, channel, amount, or
   104	deadline, the row is applicable and must be closed as `missing_in_contract` or
   105	linked `deviation`, not `not_applicable`.
   106	
   107	Slash-separated product/channel lists are alternatives unless the source says
   108	all options are mandatory. If the contract selects one applicable option, the
   109	absence of other inactive options is not a deviation.
   110	
   111	### Step 2: Build The Source Map
   112	
   113	Identify the real matrix ids and printed contract locators that can appear in
   114	the final answer. If helper scripts are used, derive locators from
   115	`inputs/contract.txt`; do not maintain a hand-picked subset.
   116	
   117	For each non-technical source item, understand the legal proposition:
   118	
   119	- who is bound and who is protected;
   120	- right, duty, restriction, procedure, or remedy;
   121	- legal object;
   122	- trigger;
   123	- deadline, amount, formula, cap, or penalty if present;
   124	- procedure, channel, or evidence requirement;
   125	- consequence;
   126	- applicability and materiality.
   127	
   128	Headings, signatures, requisites, blank forms, and definitions without
   129	operative effect may be closed internally as `not_material` or
   130	`not_evaluable`. Operative public-procurement, payment, acceptance, liability,
   131	termination, assignment, communication, governing-law, price, and appendix or
   132	table terms are material unless source text shows otherwise.
   133	
   134	A contract clause is `not_material` only if deleting it would not change any
   135	party's right, duty, deadline, evidence burden, acceptance or payment trigger,
   136	remedy, control right, refusal right, correction duty, withholding right,
   137	termination route, or consequence.
   138	
   139	### Step 3: Find Legal Analogues
   140	
   141	For each applicable matrix requirement, find true contract analogues by legal
   142	object and legal effect, not by number, heading, or word overlap.
   143	
   144	A final link is allowed only when the contract package answers the same legal
   145	question for the relevant parties. Weak thematic similarity is not enough.
   146	Reject candidates that only share generic payment, notice, liability, law,
   147	acceptance, procurement, or compliance wording without the concrete right,
   148	duty, procedure, consequence, or hard term required by the matrix.
   149	
   150	Use focused packages. Add a parent, child, companion, appendix, or table row
   151	only when it covers a named legal element of the same matrix requirement. Do
   152	not merge sibling matrix requirements into a broad thematic group when each
   153	sibling has its own legal object or could have a different status.
   154	
   155	Run a weak-link audit before finalizing links. If your reason for a link says
   156	the contract only mentions a capability, general compliance, general document
   157	request, generic liability, or that no explicit same right/procedure exists,
   158	that candidate usually does not close the matrix requirement. Convert the row
   159	to `missing_in_contract` unless another contract clause creates the same active
   160	right, duty, procedure, trigger, or consequence. Do not convert it to
   161	`not_applicable` unless the matrix applicability filter itself is inactive for
   162	the contract profile.
   163	
   164	For product-specific matrix rows, require the same active product or mechanism.
   165	Technical capability, appendix equipment descriptions, advertising material, or
   166	generic operation wording do not become final links for named QR, SberPay,
   167	QR-API, biometric, or automatic-connection obligations.
   168	
   169	Use `references/mapping-patterns.md` for analogue threshold and mapping
   170	calibration.
   171	
   172	### Step 4: Sweep Contract-Only Terms
   173	
   174	After matrix-to-contract mapping, review each material contract clause for a
   175	matrix analogue before reporting it as extra.
   176	
   177	Clauses about price, maximum price, service term, payment, acceptance, document
   178	exchange, liability, penalties, termination/change, governing law, dispute
   179	forum, assignment/succession, appendix lists, product scope, and payment
   180	methods often have matrix analogues. Link them when the same legal object and
   181	effect exist.
   182	
   183	When a child clause is linked, check whether an operative root or chapeau clause
   184	creates the legal mechanism for that child: document-exchange methods,
   185	acceptance through EIS, payment basis, withholding right, liability formula,
   186	termination route, or appendix/table incorporation. Add the root only when it is
   187	operative; do not add headings.
   188	
   189	A clause can appear in `links` for an analogue and in `unmatched_contract` for
   190	a separate independent extra proposition if the same source text contains both.
   191	
   192	Do not let a broad matrix analogue absorb an independent customer,
   193	procurement, or counterparty right that burdens the Bank. If a clause used as
   194	context also creates a customer monitoring right, refusal right,
   195	correction/refund/damages remedy, quality warranty, EIS receipt/date rule,
   196	evidence burden, or special liability rule with no matrix analogue, report that
   197	independent proposition as `extra_in_contract`.
   198	
   199	If a helper script assigns a contract locator to `not_material` only by default
   200	or because it was not selected for `links` / `unmatched_contract`, re-read that
   201	locator. A printed operative clause with a right, duty, deadline, review step,
   202	refusal, correction, signing, evidence, withholding, termination, liability, or
   203	consequence cannot be closed by a default `not_material` bucket.
   204	
   205	Use `references/missing-and-extra-patterns.md` for missing and extra
   206	calibration.
   207	
   208	### Step 5: Decide Status
   209	
   210	Decide status at group level for each focused linked package:
   211	
   212	- `aligned`: the contract preserves the Bank-standard legal result;
   213	- `deviation`: a true analogue exists, but the contract changes, weakens,
   214	  omits, narrows, shifts, inverts, or leaves blank a material element;
   215	- `missing_in_contract`: an applicable matrix requirement has no true analogue;
   216	- `extra_in_contract`: a material contract term has no matrix analogue;
   217	- `out_of_scope` / `not_applicable`: a matrix requirement is inactive for the
   218	  current profile.
   219	
   220	Functional equivalence cannot be silent on a hard term. If the matrix contains
   221	a hard term, `aligned` requires the same material element in the contract
   222	package or a source-grounded explanation that mandatory law preserves that
   223	exact legal result. If the analogue preserves only the broad topic or duty but
   224	omits the hard term, use `deviation`.
   225	
   226	Do not use low-risk `deviation` for a difference that your own analysis
   227	describes as formal, equivalent, mandatory-law routing, or preserving the same
   228	Bank-standard legal result. Low-risk `deviation` is appropriate for an
   229	applicable blank/placeholder, an omitted hard term, a changed amount/deadline
   230	not preserved by mandatory law, or a weakened Bank protection.
   231	
   232	An applicable blank or placeholder is `deviation`, normally low risk. Raise the
   233	risk when the blank prevents identifying a named system, channel, counterparty,
   234	amount, date, or condition needed for performance or enforcement.
   235	
   236	Use `references/status-patterns.md` for status calibration.
   237	
   238	## Decision Rules
   239	
   240	### Analogue Threshold
   241	
   242	A true analogue must match the legal object and legal consequence for the
   243	relevant parties. Same section, same topic, or same vocabulary is only a search
   244	signal, not proof. If a candidate is only context or capability, reject it.
   245	Use `deviation` only after a true analogue is found.
   246	
   247	### Package Boundaries
   248	
   249	Several contract clauses can collectively satisfy one matrix requirement.
   250	However, each added clause must explain which element it covers. A broad parent
   251	or framework clause is included only if it creates the right, duty, procedure,
   252	trigger, consequence, amount, cap, or legal basis used in the comparison.
   253	
   254	A gap in one sibling channel, product, right, or procedure does not downgrade
   255	neighboring sibling requirements. Conversely, a missing or weaker hard term in
   256	the true analogue package prevents `aligned`.
   257	
   258	### Public Procurement Bridge
   259	
   260	44-FZ, 223-FZ, EIS, acceptance, payment, termination, withholding, and
   261	correction mechanics can be:
   262	
   263	- an analogue, if they answer the same legal question as the matrix;
   264	- a deviation, if they alter a material Bank-standard element;
   265	- an extra term, if they create an independent customer/procurement right with
   266	  no matrix analogue;
   267	- out of scope, if the matrix row is inactive for the contract profile.
   268	
   269	Do not treat mandatory-law wording as automatically extra or automatically
   270	aligned. Compare the legal effect.
   271	
   272	If mandatory-law mechanics merely explain why the Bank-standard right is absent
   273	and do not give the Bank the same enforceable right or protection, do not force
   274	a weak `deviation` link. Use `missing_in_contract` for the applicable matrix
   275	requirement and explain the lower or regime-specific risk.
   276	
   277	### Bank-Risk Priority
   278	
   279	Prefer flagging real `deviation`, `missing_in_contract`, and
   280	`extra_in_contract` risks over smoothing them into `aligned`.
   281	
   282	Do not downgrade to `deviation` when the only difference is a formal channel or
   283	document label, a party alias, an inactive product option, a broader or
   284	beneficial Bank right, or a mandatory-law route that preserves the same right,
   285	duty, trigger, amount, deadline, or consequence.
   286	
   287	## What This Skill Does Not Do
   288	
   289	- It does not compare clauses by numbering.
   290	- It does not treat the counterparty contract as equal to the Bank matrix.
   291	- It does not report headings, requisites, signatures, empty forms, or
   292	  non-operative definitions as business findings.
   293	- It does not create final ids that are not visible in the source text.
   294	- It does not use calibration examples as document-specific answers.
   295	
   296	## Quality Checks Before Finishing
   297	
   298	- Every source matrix id is closed once in `coverage_ledger.matrix`.
   299	- Every linked matrix id appears in `links`.
   300	- Every `missing_in_contract` matrix id appears in `unmatched_matrix`.
   301	- Out-of-scope/not-applicable rows state the source-based profile reason.
   302	- Every material contract locator is closed as linked, extra, or not material.
   303	- Every linked contract id appears in `links`.
   304	- Every extra contract id appears in `unmatched_contract`.
   305	- No matrix id is both linked and missing.
   306	- No contract id is extra only if it is merely a heading, definition,
   307	  signature, requisite, or empty form.
   308	- Every `deviation` has a named material gap and risk.
   309	- Every `aligned` link has no material discrepancy.
   310	
   311	Verify by exact source ids, not by counts alone.
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
AI: Let me continue reading the remaining files. The matrix is large, so let me get the rest:[{'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json', 'offset': 100, 'limit': 300}, 'id': 'call_00_iTLfW4f88S2edXGFjQen3281', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'inputs/contract.txt', 'offset': 100, 'limit': 300}, 'id': 'call_01_mfdQDUxdZw3xMmxxJvqR9671', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'skills/acquiring-single-agent-review/references/output-contract.md', 'limit': 1000}, 'id': 'call_02_bL7uBtHaLP1dqiOXgx1x8191', 'type': 'tool_call'}]
Tool:    101	  "enriched_text":"Банк и Предприятие в рамках настоящего Договора обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию\/документ по своему усмотрению, если иное не предусмотрено Договором: → путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;",
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
   201	 },
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
Tool:      1	# Output Contract
     2	
     3	Use this reference when writing `outputs/discrepancy_analysis.json`.
     4	
     5	The final artifact is one JSON object:
     6	
     7	```json
     8	{
     9	  "analysis_profile": {
    10	    "product": [],
    11	    "legal_regime": "44_fz|223_fz|commercial|common"
    12	  },
    13	  "links": [
    14	    {
    15	      "contract_ids": ["<contract locator>"],
    16	      "matrix_ids": ["<matrix number>"],
    17	      "relationship": "aligned|deviation",
    18	      "status_reason": "<short legal reason>",
    19	      "risk_level": "none|low|medium|high",
    20	      "discrepancies": [
    21	        {
    22	          "type": "deadline|amount|party|scope|trigger|procedure|liability|other",
    23	          "description": "<material difference>",
    24	          "risk": "<why it matters for the Bank>"
    25	        }
    26	      ]
    27	    }
    28	  ],
    29	  "unmatched_matrix": [
    30	    {
    31	      "matrix_id": "<matrix number>",
    32	      "status": "missing_in_contract",
    33	      "requirement": "<missing Bank-standard requirement>",
    34	      "required_type": "mandatory|optional",
    35	      "risk_level": "low|medium|high",
    36	      "risk": "<risk of omission>"
    37	    }
    38	  ],
    39	  "unmatched_contract": [
    40	    {
    41	      "contract_id": "<contract locator>",
    42	      "status": "extra_in_contract",
    43	      "contract_position": "<extra contract term>",
    44	      "risk_level": "low|medium|high",
    45	      "risk": "<impact for the Bank>",
    46	      "materiality_reason": "<why it has legal effect>"
    47	    }
    48	  ],
    49	  "coverage_ledger": {
    50	    "matrix": [
    51	      {
    52	        "matrix_id": "<matrix number>",
    53	        "closure": "linked|missing_in_contract|out_of_scope|not_applicable|not_evaluable",
    54	        "reason": "<short source-grounded reason>"
    55	      }
    56	    ],
    57	    "contract": [
    58	      {
    59	        "contract_id": "<contract locator>",
    60	        "closure": "linked|extra_in_contract|not_material",
    61	        "reason": "<short source-grounded reason>"
    62	      }
    63	    ]
    64	  },
    65	  "summary": {
    66	    "aligned_count": 0,
    67	    "deviation_count": 0,
    68	    "missing_in_contract_count": 0,
    69	    "extra_in_contract_count": 0
    70	  }
    71	}
    72	```
    73	
    74	## Structural Rules
    75	
    76	- `links[].relationship` is only `aligned` or `deviation`.
    77	- Missing matrix rows go only to `unmatched_matrix`, not to `links`.
    78	- Extra contract rows go only to `unmatched_contract`, not to `links`.
    79	- A clause may appear in both `links` and `unmatched_contract` only when the
    80	  same source text contains a true matrix analogue plus a separate independent
    81	  extra proposition.
    82	- `aligned` links have empty `discrepancies`.
    83	- Every `deviation` has at least one named discrepancy.
    84	- `summary` counts equal the final array counts.
    85	
    86	## Coverage Rules
    87	
    88	- Every source matrix id appears once in `coverage_ledger.matrix`.
    89	- Every `coverage_ledger.matrix` row with `closure: "linked"` appears in at
    90	  least one `links[].matrix_ids`.
    91	- Every `coverage_ledger.matrix` row with `closure: "missing_in_contract"`
    92	  appears in `unmatched_matrix[].matrix_id`.
    93	- `out_of_scope` and `not_applicable` rows state the source-based applicability
    94	  reason.
    95	- Every material contract locator appears in `coverage_ledger.contract`.
    96	- Every `coverage_ledger.contract` row with `closure: "linked"` appears in at
    97	  least one `links[].contract_ids`.
    98	- Every `coverage_ledger.contract` row with `closure: "extra_in_contract"`
    99	  appears in `unmatched_contract[].contract_id`.
   100	
   101	Verify by exact source id sets, not by row counts alone.
AI: [{'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json', 'offset': 400, 'limit': 400}, 'id': 'call_00_OQy5KBHxVj8Cdj28DUMo1792', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'inputs/contract.txt', 'offset': 400, 'limit': 200}, 'id': 'call_01_qHYMm3B3XO1FlzNx8vbB7791', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'skills/acquiring-single-agent-review/references/mapping-patterns.md', 'limit': 1000}, 'id': 'call_02_UpN7DdFcaw1F705jFGpD6648', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'skills/acquiring-single-agent-review/references/missing-and-extra-patterns.md', 'limit': 1000}, 'id': 'call_03_Css6NXlUqHgx1flaXP8K5907', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': 'skills/acquiring-single-agent-review/references/status-patterns.md', 'limit': 1000}, 'id': 'call_04_q1u7U42FAj7w3WnPv16E1249', 'type': 'tool_call'}]
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
Tool:      1	# Mapping Patterns
     2	
     3	Use this reference while building `links`. The goal of mapping is not to find
     4	similar words; it is to find true legal analogues by legal object and legal
     5	effect.
     6	
     7	## Stage Logic
     8	
     9	1. Read the matrix source text for the requirement: `enriched_text`,
    10	   `main_idea`, `topics`, required type, and applicability filters.
    11	2. Identify the material legal elements: party, protected party, right/duty,
    12	   object, trigger, deadline, amount/formula/cap, procedure, consequence.
    13	3. Search the contract for clauses that regulate the same legal object and
    14	   consequence. Numbers, headings, and shared vocabulary are only navigation.
    15	4. Build a focused package only from clauses that cover a named element of the
    16	   matrix requirement.
    17	5. Keep weak thematic candidates out of final `contract_ids`. Record the legal
    18	   result as `missing_in_contract` when no true analogue exists.
    19	6. For public-procurement contracts, first test 44-FZ/EIS clauses as possible
    20	   analogues for payment, acceptance, liability, termination, documents, and
    21	   control before calling them extras.
    22	
    23	## Calibration Examples
    24	
    25	### Same Number Is Not Analogue
    26	
    27	Wrong:
    28	The contract clause and matrix row both have the same number, so they are
    29	linked.
    30	
    31	Right:
    32	Link only if the source texts regulate the same legal object and effect.
    33	When using scripts or tables, store them as separate namespaces such as
    34	`contract_id` and `matrix_id`; never let a shared printed number close both
    35	sources automatically.
    36	
    37	### General Law Clause Is Not Universal Coverage
    38	
    39	Contract:
    40	Services are provided according to law, contract terms, and incorporated rules.
    41	
    42	Right:
    43	Use this only for matrix rows about compliance with law or incorporated rules.
    44	It does not cure missing deadlines, payment mechanisms, Bank rights, liability
    45	formulas, product scope, or procedural hard terms.
    46	
    47	### Matrix Requirement Covered By Package
    48	
    49	Matrix:
    50	One requirement includes a duty, trigger, payment formula, and deadline.
    51	
    52	Contract:
    53	The duty is in one clause, the formula in an appendix, and the deadline in a
    54	payment clause.
    55	
    56	Result:
    57	Use all clauses as the contract package if together they cover the same matrix
    58	legal result. If a material element remains changed or absent, status is
    59	`deviation`.
    60	
    61	### Child Found, Operative Root Also Needed
    62	
    63	Contract:
    64	A child clause gives the deadline, while the parent clause creates the payment
    65	obligation or legal mechanism.
    66	
    67	Right:
    68	Use the child and the operative parent together when the matrix requirement
    69	contains both the mechanism and the detail.
    70	
    71	### Same Parent Does Not Mean Same Link
    72	
    73	Contract:
    74	Several child clauses sit under one parent: one is about document exchange,
    75	one about payment, one about liability.
    76	
    77	Right:
    78	Do not merge them into one broad link only because they share a parent. Link
    79	each child only to matrix requirements whose legal object it actually covers.
    80	
    81	### Public-Procurement Role Names
    82	
    83	Contract:
    84	The Bank is called contractor/executor/provider, and the merchant is called
    85	customer.
    86	
    87	Right:
    88	Map by legal role, not by label. A customer duty can be the matrix merchant
    89	duty, and an executor right can be the matrix Bank right when the legal object
    90	and consequence match.
    91	
    92	### Public Procurement Acceptance As Analogue
    93	
    94	Matrix:
    95	Payment starts after a legally sufficient operation/acceptance document.
    96	
    97	Contract:
    98	The public-procurement contract uses an EIS acceptance document as the payment
    99	trigger.
   100	
   101	Result:
   102	Treat the EIS acceptance provision as a possible analogue. Classify by the
   103	actual trigger, deadline, party, and consequence.
   104	
   105	### QR Terminal Capability Is Not QR Product
   106	
   107	Contract:
   108	The terminal can display a QR code, but the contract does not create a QR
   109	acquiring product, QR auto-connection duty, QR API, or SberPay mechanism.
   110	
   111	Result:
   112	Do not use terminal QR capability as a final analogue for named QR product
   113	obligations.
   114	
   115	### QR API Or Auto-Connection Requires Active Mechanism
   116	
   117	Matrix:
   118	The Bank standard requires QR-API, automatic QR connection with a smart
   119	terminal, or a named SberPay/QR payment product.
   120	
   121	Contract:
   122	Only a terminal model, technical QR display capability, or a generic reference
   123	to QR in an appendix appears.
   124	
   125	Result:
   126	Reject the candidate. Use `missing_in_contract` for the applicable matrix
   127	requirement unless the contract creates the same active product, API, automatic
   128	connection, or payment mechanism.
   129	
   130	### Term And Price Cap Link To Contract Duration
   131	
   132	Matrix:
   133	The contract is effective until a date or until the contract price is exhausted.
   134	
   135	Contract:
   136	One clause states maximum contract price or volume by customer need, and
   137	another states the service period or price-exhaustion stop.
   138	
   139	Result:
   140	Treat the clauses as a focused package for the duration/price-exhaustion
   141	standard. Do not report them as unrelated extras before checking matrix term
   142	and price-cap rows.
   143	
   144	### Final Locator Must Be Printed Exactly
   145	
   146	Wrong:
   147	Use final ids like `Appendix_fee`, `8.5.2-8.5.4`, `8.1-8.5.9`, or a semantic
   148	suffix.
   149	
   150	Right:
   151	Use exact visible locators from the contract text. Put descriptions in
   152	evidence/reason fields, not inside `contract_id`.
   153	
   154	### Weak Candidate Does Not Cure Missing
   155	
   156	Matrix:
   157	The Bank has a specific right to suspend authorization, verify through an
   158	issuer, transmit fraud information, or require all listed cards to be accepted.
   159	
   160	Contract:
   161	Only general cooperation, information exchange, technical capability, or broad
   162	compliance exists.
   163	
   164	Result:
   165	Reject the candidate and use `missing_in_contract` for an applicable matrix
   166	requirement.
   167	
   168	### Contract-Side Analogue Sweep
   169	
   170	Contract:
   171	A clause states maximum price, service period, payment basis, dispute forum,
   172	termination route, assignment rule, appendix list, or governing-law fallback.
   173	
   174	Right:
   175	Search the matrix for the same legal object and effect before final
   176	classification. Use `extra_in_contract` only when no true matrix analogue
   177	exists.
   178	
   179	### Liability Root, Formula, And Cap Stay Together
   180	
   181	Contract:
   182	A liability section has one clause granting the penalty right, child clauses
   183	with the fine formula, and another child clause with a total cap.
   184	
   185	Right:
   186	For the same breach direction, map root, formula, and cap together. Do not mark
   187	the formula aligned while missing the cap row, and do not classify the cap as
   188	extra before checking neighboring matrix liability rows.
   189	
   190	### Weak Link Must Become Missing
   191	
   192	Matrix:
   193	The Bank standard requires a specific active right or mechanism: QR provision,
   194	automatic QR connection, compliance with Bank instructions, fraud information
   195	transfer, issuer/payment-system verification, or Bank liability exemption.
   196	
   197	Contract:
   198	The contract only mentions technical capability, general compliance, general
   199	document requests, reimbursement, or broad cooperation, and the analysis says
   200	there is "no explicit" same right or procedure.
   201	
   202	Right:
   203	Do not keep the weak candidate in final `contract_ids`. Use
   204	`missing_in_contract` unless another clause creates the same active legal
   205	mechanism.
   206	
   207	### Operative Chapeau Travels With Child
   208	
   209	Contract:
   210	A child clause contains a deadline or detail, but a nearby operative chapeau
   211	creates the list of document-exchange methods, acceptance mechanism, payment
   212	trigger, liability regime, withholding right, or termination route.
   213	
   214	Right:
   215	Include the operative chapeau with the child when it supplies a legal element
   216	of the same focused requirement. Do not include a non-operative heading.
   217	
   218	### Appendix Table Row Can Be Final Locator
   219	
   220	Contract:
   221	A technical specification, appendix, or table row states a currency, device
   222	condition, product scope, commission basis, payment method, or service
   223	condition.
   224	
   225	Right:
   226	Use the exact visible appendix/table locator as a final `contract_id` when that
   227	row itself carries the legal term. Do not demote it to evidence-only merely
   228	because it is in an appendix.
Tool:      1	# Missing And Extra Patterns
     2	
     3	Use this reference for `unmatched_matrix`, `unmatched_contract`, and coverage
     4	ledger closure. The goal is to avoid both false missing and hidden contract-only
     5	risk.
     6	
     7	## Stage Logic
     8	
     9	1. Every applicable/evaluable matrix id must be closed as `linked` or
    10	   `missing_in_contract`.
    11	2. Use `missing_in_contract` only after rejecting weak candidates that do not
    12	   share the same legal object and effect.
    13	3. Use `out_of_scope` / `not_applicable` only when source text or applicability
    14	   filters make the matrix row inactive for the current product, terminal,
    15	   payment method, lot, or legal regime.
    16	4. Every material contract clause must be closed as `linked` or
    17	   `extra_in_contract`. Use `not_material` only for headings, requisites,
    18	   signatures, blank forms, or definitions without independent legal effect.
    19	5. Public-procurement and EIS clauses are not automatically extra. First test
    20	   them as analogues. If they create independent customer control, refusal,
    21	   correction, withholding, proof, or termination rights with no matrix
    22	   analogue, report `extra_in_contract`.
    23	6. Coverage must be exact-id based. Do not validate by row counts alone.
    24	
    25	## Calibration Examples
    26	
    27	### Bank Right Missing
    28	
    29	Matrix:
    30	The Bank may refuse service, verify information, suspend an operation, withhold
    31	funds, receive evidence, or transmit information to a payment system.
    32	
    33	Contract:
    34	Only a general cooperation, document request, or lawful-processing clause
    35	exists.
    36	
    37	Result:
    38	Use `missing_in_contract` if the specific Bank right is absent.
    39	
    40	### Mandatory-Law Displacement Without Same Bank Right
    41	
    42	Matrix:
    43	The Bank has a specific unilateral right, refusal right, direct-debit right, or
    44	pre-contract discretion.
    45	
    46	Contract:
    47	The public-procurement regime explains a different statutory process but does
    48	not give the Bank the same enforceable right.
    49	
    50	Result:
    51	Use `missing_in_contract` for the matrix protection. Do not create a weak
    52	`deviation` link solely because mandatory law explains why the template right
    53	is absent.
    54	
    55	### Out Of Scope Is Not Missing
    56	
    57	Matrix:
    58	Requirement applies only to internet acquiring, QR-API, SberPay/biometric
    59	payment, 223-FZ, or another unused product/regime.
    60	
    61	Contract:
    62	The profile is card-present trade acquiring under another regime.
    63	
    64	Result:
    65	Close as `out_of_scope` or `not_applicable`, not `missing_in_contract`.
    66	
    67	### Applicable But Absent Is Missing
    68	
    69	Matrix:
    70	The filter matches the contract profile or the row is common/optional but
    71	applicable. The required mechanism, QR procedure, Bank right, channel, amount,
    72	fee, deadline, or smart-terminal term is not present in the contract.
    73	
    74	Wrong:
    75	Close the row as `not_applicable` because the contract did not implement that
    76	mechanism.
    77	
    78	Right:
    79	Use `missing_in_contract` unless the matrix source itself limits the row to an
    80	inactive product, terminal, payment method, lot, or legal regime.
    81	
    82	### Blank Active Term Is Not Out Of Scope
    83	
    84	Matrix:
    85	The standard expects an active fee, amount, percentage, website, QR/smart
    86	terminal term, or other filled commercial term for the current profile.
    87	
    88	Contract:
    89	The corresponding place is blank, omitted, or only says that the term will be
    90	filled elsewhere.
    91	
    92	Result:
    93	Do not use `not_applicable`. Use `deviation` if there is a true analogue with a
    94	blank hard term; use `missing_in_contract` if no true analogue exists.
    95	
    96	### Product Mechanism Missing Despite Technical Mention
    97	
    98	Matrix:
    99	An applicable row requires a named QR/SberPay/QR-API mechanism, auto-connection
   100	rule, or Bank-issued QR code.
   101	
   102	Contract:
   103	Only terminal capability, a product name in a device table, or generic QR
   104	language appears, with no active mechanism or duty.
   105	
   106	Result:
   107	Use `missing_in_contract`. Technical mention is not a final analogue and should
   108	not become a weak `deviation` link.
   109	
   110	### Optional Applicable Row Still Requires Classification
   111	
   112	Matrix:
   113	An optional applicable row has a true analogue or is absent.
   114	
   115	Result:
   116	If analogue exists, classify normally. If absent, use low-risk
   117	`missing_in_contract`. Optional means lower criticality, not non-evaluable.
   118	
   119	### Matrix Closure Must Mirror Final Report
   120	
   121	Matrix:
   122	An applicable row has no true contract analogue after source review.
   123	
   124	Right:
   125	Close the id in `coverage_ledger.matrix` as `missing_in_contract` and also
   126	include it in `unmatched_matrix`.
   127	
   128	### Optional Or Common Is Not Out Of Scope
   129	
   130	Matrix:
   131	A row is optional or in a common/general section, but applicable to the
   132	contract profile.
   133	
   134	Wrong:
   135	Mark it `not_applicable` because no close analogue was found.
   136	
   137	Right:
   138	Use low-risk `missing_in_contract` if applicable and absent.
   139	
   140	### Contract-Only Procurement Right
   141	
   142	Contract:
   143	The customer has an independent right to inspect, reject, demand correction,
   144	withhold payment, impose a penalty, or terminate.
   145	
   146	Matrix:
   147	No matrix row regulates the same customer right or procurement remedy.
   148	
   149	Result:
   150	Report `extra_in_contract` with non-empty risk.
   151	
   152	### Not Material Deletion Test
   153	
   154	Contract:
   155	A printed clause creates a review period, evidence obligation, commission
   156	signing step, motivated refusal, correction duty, payment withholding right,
   157	quality-control right, or termination route.
   158	
   159	Wrong:
   160	Close it as `not_material` because it is procedural, standard, or covered by a
   161	neighboring acceptance/payment section.
   162	
   163	Right:
   164	Ask whether deleting the clause would change any party's legal position. If
   165	yes, it is material. Link it to a true matrix analogue or report it as
   166	`extra_in_contract`.
   167	
   168	### Acceptance Procedure Package
   169	
   170	Contract:
   171	Acceptance is split across EIS clauses: document placement, review period,
   172	motivated refusal, correction, and final signed acceptance.
   173	
   174	Result:
   175	Use clauses that supply a matrix payment/acceptance trigger in `links`.
   176	Report independent customer review, refusal, correction, or withholding rights
   177	as `extra_in_contract` when no matrix analogue exists.
   178	
   179	### Acceptance Children Are Not Headings
   180	
   181	Contract:
   182	Separate EIS child clauses create review deadlines, expert involvement,
   183	motivated refusal, correction by the Bank, signing by a commission, or deemed
   184	acceptance consequences.
   185	
   186	Result:
   187	These are material contract-only candidates. Do not drop them as headings or
   188	not-material merely because a neighboring payment/acceptance clause is linked.
   189	
   190	### EIS Acceptance Children Are Separate
   191	
   192	Contract:
   193	Separate printed child clauses create receipt date, representative
   194	participation, expert review, motivated refusal, correction, commission
   195	signing, defect remedy, or final acceptance steps.
   196	
   197	Right:
   198	Close each operative child separately as linked, extra, or not material. Do
   199	not hide all sibling clauses inside one payment analogue.
   200	
   201	### No Range Id For Material Children
   202	
   203	Wrong:
   204	Report one item such as `8.1-8.5.9` for a whole acceptance section.
   205	
   206	Right:
   207	Use each printed locator that has its own legal effect. A section range can be
   208	mentioned in reasoning, but final `contract_id` values must be exact source
   209	locators.
   210	
   211	### Linked Clause With Extra Proposition
   212	
   213	Contract:
   214	One clause supplies a matrix payment trigger and also gives the customer an
   215	additional refusal/correction/control right.
   216	
   217	Result:
   218	Use the clause in `links` for the analogue and also report the independent
   219	extra proposition in `unmatched_contract`.
   220	
   221	### Context Link Does Not Consume Independent Customer Right
   222	
   223	Contract:
   224	A clause helps explain an aligned payment, acceptance, quality, liability, or
   225	termination mechanism, but also gives the customer a separate monitoring,
   226	refusal, refund, damages, correction, evidence, or quality-control right.
   227	
   228	Wrong:
   229	Treat the clause as fully closed by the matrix analogue and omit it from
   230	`unmatched_contract`.
   231	
   232	Right:
   233	Keep the link for the shared legal object. Also report the independent
   234	customer/procurement right as `extra_in_contract` when no matrix row gives the
   235	same right.
   236	
   237	### Operative Root Is Not Not Material
   238	
   239	Contract:
   240	A root clause states that a party may withhold amounts, charge penalties,
   241	exchange documents by listed methods, accept services through EIS, assign
   242	rights, or rely on applicable law.
   243	
   244	Result:
   245	Treat it as material when it creates the legal mechanism.
   246	
   247	### Contract Locator Inventory Must Come From Source
   248	
   249	Wrong:
   250	Build the contract coverage ledger from a manually selected list containing
   251	only clauses already used in links.
   252	
   253	Right:
   254	Derive printed locators from the contract text, then close each operative
   255	child clause.
   256	
   257	### No Default Not Material Bucket
   258	
   259	Wrong:
   260	A helper script assigns every contract locator not listed in `links` or
   261	`unmatched_contract` to `not_material` with a generic reason such as "covered by
   262	parent/child clause mapping."
   263	
   264	Right:
   265	Re-read each such locator. If it contains a right, duty, deadline, acceptance
   266	step, EIS signing/placement rule, motivated refusal, correction route,
   267	withholding right, termination route, evidence burden, or liability
   268	consequence, it is material. Link it to a true matrix analogue or report it as
   269	`extra_in_contract`.
   270	
   271	### EIS Acceptance Step Is Material
   272	
   273	Contract:
   274	Separate public-procurement acceptance clauses define document placement,
   275	receipt date, representative participation, bilateral acceptance, unilateral
   276	acceptance, motivated refusal, correction, commission signing, or final
   277	acceptance date.
   278	
   279	Wrong:
   280	Treat all children as not material because the general payment/acceptance
   281	mechanism was already linked.
   282	
   283	Right:
   284	Each operative child gets its own closure. If no matrix row gives the customer
   285	the same procedural right or imposes the same procedural burden on the Bank,
   286	report that child as `extra_in_contract`.
   287	
   288	### Force-Majeure Evidence Burden Is Material
   289	
   290	Contract:
   291	A force-majeure clause requires a party relying on force majeure to provide
   292	documentary confirmation from an authorized body.
   293	
   294	Right:
   295	This is a material evidence burden. Link it to a matrix force-majeure evidence
   296	requirement if one exists; otherwise report `extra_in_contract`.
Tool:      1	# Status Patterns
     2	
     3	Use this reference after a true legal analogue or package has been found. The
     4	status answers whether the contract preserves the Bank standard, not whether a
     5	candidate exists.
     6	
     7	## Stage Logic
     8	
     9	1. Status is group-level: evaluate the focused package of contract ids against
    10	   the focused matrix requirement(s).
    11	2. Use `aligned` when the legal result is preserved.
    12	3. Use `deviation` only when a true analogue exists and a material element is
    13	   changed, weakened, omitted, narrowed, shifted, inverted, or left blank.
    14	4. Re-read source text before deciding hard terms: deadlines, amounts, caps,
    15	   formulas, protected party, trigger, procedure, forum, termination, and
    16	   liability consequences.
    17	5. Do not downgrade for labels, document names, mandatory-law route, inactive
    18	   product options, or beneficial expansions if the legal result is preserved.
    19	6. Do not spread one gap across sibling requirements.
    20	
    21	## Calibration Examples
    22	
    23	### Missing Deadline Is Deviation
    24	
    25	Matrix:
    26	The merchant must provide confirmation within 3 working days.
    27	
    28	Contract:
    29	The same confirmation duty exists, but no response period is stated.
    30	
    31	Result:
    32	`deviation`, because the duty exists but the hard-term deadline is missing.
    33	
    34	### Personal-Data Confirmation Deadline Is A Hard Term
    35	
    36	Matrix:
    37	The counterparty must provide proof of lawful personal-data transfer within a
    38	specified period after the Bank's written request.
    39	
    40	Contract:
    41	The same proof/indemnity duty exists, but the response period is absent.
    42	
    43	Result:
    44	`deviation`. Do not mark `aligned` merely because the proof duty and indemnity
    45	exist; the response period is part of the Bank protection.
    46	
    47	### Changed Payment Deadline Is Deviation
    48	
    49	Matrix:
    50	Payment must occur within 5 working days.
    51	
    52	Contract:
    53	Payment occurs within 7 working days, and no mandatory-law equivalence
    54	preserves the Bank standard.
    55	
    56	Result:
    57	`deviation` for the payment-deadline requirement only.
    58	
    59	### Summary Omits Hard Term
    60	
    61	Matrix proposition summary:
    62	The merchant must provide confirmation.
    63	
    64	Matrix source text:
    65	The merchant must provide confirmation within 3 working days.
    66	
    67	Result:
    68	Use the source text, not the summary. Missing the period is `deviation`.
    69	
    70	### Liability Direction Matters
    71	
    72	Matrix:
    73	The Bank is protected from liability or the merchant must compensate the Bank.
    74	
    75	Contract:
    76	General liability exists for culpable breach.
    77	
    78	Result:
    79	Compare protected party, breach trigger, formula/cap, exceptions, and
    80	consequence. General liability is not automatically enough.
    81	
    82	### Penalty Amount And Cap Are One Package
    83	
    84	Matrix:
    85	One row sets penalty amount/formula and a neighboring row sets cap or
    86	exception for the same breach direction.
    87	
    88	Contract:
    89	The amount is present but the cap/exception is absent or different.
    90	
    91	Result:
    92	The liability package is `deviation`.
    93	
    94	### Sibling Status Does Not Spread
    95	
    96	Matrix:
    97	Neighboring rows regulate separate channels, grounds, products, or rights.
    98	
    99	Contract:
   100	One sibling is missing a deadline or named channel.
   101	
   102	Result:
   103	Only that sibling receives `deviation` or `missing_in_contract`.
   104	
   105	### Formal Procurement Route Is Not Deviation
   106	
   107	Matrix:
   108	Payment or acceptance must be documented and enforceable.
   109	
   110	Contract:
   111	The same legal result is implemented through mandatory public-procurement,
   112	EIS, or statutory acceptance.
   113	
   114	Result:
   115	Do not mark `deviation` merely because the form, system, or route differs.
   116	
   117	### EIS Acceptance Can Preserve Payment Acceptance
   118	
   119	Matrix:
   120	The customer must sign/return an acceptance or payment document by a template
   121	deadline.
   122	
   123	Contract:
   124	Mandatory public-procurement/EIS acceptance creates an enforceable acceptance
   125	document, review period, motivated refusal mechanism, and payment trigger.
   126	
   127	Result:
   128	Use `aligned` when the legal result is preserved by the mandatory route. Do not
   129	create a low-risk `deviation` solely because the template document name or
   130	calendar formulation differs.
   131	
   132	### Low-Risk Formal Difference Is Not Deviation
   133	
   134	Contract:
   135	The same right or duty exists and is enforceable, but the channel label,
   136	document name, appendix label, or wording differs.
   137	
   138	Result:
   139	Use `aligned` unless the difference weakens a right, changes a hard term,
   140	removes required proof, or makes performance unenforceable.
   141	
   142	### Preserved Approval Right With Different Channel
   143	
   144	Matrix:
   145	The counterparty may use advertising, materials, or notices only after Bank
   146	approval through named communication channels.
   147	
   148	Contract:
   149	The same Bank approval right exists, but the contract does not repeat the exact
   150	template channel cross-reference.
   151	
   152	Result:
   153	Use `aligned` if the Bank approval right is enforceable and general contract
   154	communication channels are available. Use `deviation` only if the approval
   155	right itself is absent or unenforceable.
   156	
   157	### Named Appendices Can Satisfy Incorporation
   158	
   159	Matrix:
   160	Referenced documents or appendices must be integral parts of the contract.
   161	
   162	Contract:
   163	The contract names the operative appendices, technical assignment, specification,
   164	or acceptance documents as contract components.
   165	
   166	Result:
   167	Use `aligned` for the incorporation requirement unless a specific referenced
   168	document needed for enforcement is left outside the contract.
   169	
   170	### Beneficial Expansion Does Not Lower Status
   171	
   172	Contract:
   173	The same Bank right is present and the contract adds a broader instrument,
   174	extra method, additional protective ground, or wider technical option.
   175	
   176	Result:
   177	Use `aligned` when the matrix protection is preserved.
   178	
   179	### Inactive Product Option Does Not Create Gap
   180	
   181	Matrix:
   182	The standard mentions alternatives such as Cards/QR/SberPay, electronic
   183	terminal/smart terminal, or several notice channels.
   184	
   185	Contract:
   186	The current contract profile activates one alternative and that alternative is
   187	covered.
   188	
   189	Result:
   190	Use `aligned` for the active alternative unless all alternatives are mandatory.
   191	
   192	### Mandatory-Law Route With Preserved Result
   193	
   194	Contract:
   195	Mandatory procurement, EIS, statutory acceptance, or statutory termination
   196	wording replaces the Bank template route.
   197	
   198	Result:
   199	Use `aligned` when the same enforceable right, duty, trigger, amount, deadline,
   200	and consequence are preserved. Use `deviation` when the Bank standard is
   201	actually weakened or a hard term is missing.
   202	
   203	### Procurement Acceptance Route Can Align
   204	
   205	Matrix:
   206	The counterparty must return a signed acceptance/payment document or motivated
   207	refusal.
   208	
   209	Contract:
   210	A mandatory public-procurement route uses EIS acceptance documents, motivated
   211	refusal, and statutory signing periods.
   212	
   213	Result:
   214	Use `aligned` when the route gives the Bank an enforceable acceptance/payment
   215	trigger and refusal mechanism. Do not downgrade only because the document is
   216	not called UPD or the deadline is expressed through EIS statutory timing.
   217	
   218	### Statutory Succession Exception Is Not Assignment Gap
   219	
   220	Matrix:
   221	Rights and obligations may not be transferred without consent, except legal
   222	succession or reorganization.
   223	
   224	Contract:
   225	The public-procurement contract allows replacement or succession only in cases
   226	permitted by law.
   227	
   228	Result:
   229	Use `aligned` when the practical restriction is the same and the only
   230	difference is mandatory-law succession wording.
   231	
   232	### Separate Extra Does Not Contaminate Linked Status
   233	
   234	Matrix:
   235	A standard clause is matched by a contract analogue.
   236	
   237	Contract:
   238	The same section also contains an additional independent customer or
   239	procurement right that should be reported as `extra_in_contract`.
   240	
   241	Result:
   242	Keep the linked analogue `aligned` if it preserves the matrix result. Report
   243	the independent proposition separately as extra; do not downgrade the linked
   244	status merely because the neighboring extra exists.
   245	
   246	### Placeholder Is Deviation
   247	
   248	Matrix or contract:
   249	An applicable material field is blank or represented by `___`.
   250	
   251	Result:
   252	`deviation`, usually low risk. Raise risk when the blank prevents identifying
   253	a named system, channel, counterparty, amount, term, or enforcement route.
AI: [{'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json', 'offset': 800, 'limit': 400}, 'id': 'call_00_pj42VewqWPYEjyUr7rDf9273', 'type': 'tool_call'}]
Tool:    801	   "Соответствие подтвержденной суммы фактически оказанным товарам\/услугам",
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
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'inputs/matrix.json\') as f:\n    data = json.load(f)\nprint(f\'Total matrix items: {len(data)}\')\nfor i, item in enumerate(data):\n    print(f\'{i}: {item[\\"number\\"]} | required: {item[\\"required_type\\"]} | product: {item[\\"only_for_product\\"]} | lot: {item[\\"only_for_lot\\"]} | terminal: {item[\\"only_for_terminal\\"]} | payment: {item[\\"payment_method\\"]}\')\n"'}, 'id': 'call_00_CFKrP4RF2TH2VZYzlrG14581', 'type': 'tool_call'}]
Tool:   File "<string>", line 7
    print(f'{i}: {item[" number\]}
                       ^
SyntaxError: unterminated string literal (detected at line 7)

[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c \'\nimport json\nwith open("inputs/matrix.json") as f:\n    data = json.load(f)\nprint("Total matrix items:", len(data))\nfor i, item in enumerate(data):\n    print(i, item["number"], "|", item["required_type"], "|", item["only_for_product"], "|", item["only_for_lot"], "|", item["only_for_terminal"], "|", item["payment_method"])\n\''}, 'id': 'call_00_1b4glXkzirIPFz2YRmpS4462', 'type': 'tool_call'}]
Tool:   File "<string>", line 5
    print(Total
         ^
SyntaxError: '(' was never closed

[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': 'outputs/working/list_matrix.py', 'content': 'import json\n\nwith open("inputs/matrix.json") as f:\n    data = json.load(f)\n\nprint("Total matrix items:", len(data))\nfor i, item in enumerate(data):\n    n = item["number"]\n    rt = item["required_type"]\n    prod = item["only_for_product"]\n    lot = item["only_for_lot"]\n    term = item["only_for_terminal"]\n    pm = item["payment_method"]\n    print(f"{i}|{n}|{rt}|{prod}|{lot}|{term}|{pm}")\n'}, 'id': 'call_00_BgukzcACacTdeWTOQyE30939', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/list_matrix.py
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/list_matrix.py'}, 'id': 'call_00_IJgGoYGC5ew8YjZWCHHU6844', 'type': 'tool_call'}]
Tool: Total matrix items: 169
0|2.1|mandatory|common|common|common|common
1|2.2|mandatory|common|common|common|common
2|2.3.1|mandatory|common|common|common|common
3|2.3.2|mandatory|common|common|common|common
4|2.3.3|optional|common|common|common|common
5|2.3.4|optional|common|common|common|common
6|2.3.5|mandatory|common|common|common|common
7|2.3.6|mandatory|common|fz_44|common|common
8|2.3.7|optional|common|common|common|common
9|2.4|optional|common|common|common|common
10|2.5.1.1|mandatory|internet_acquiring|common|common|common
11|2.5.2.1|mandatory|trade_acquiring|common|common|sber_pay_face_scan
12|2.6.1.1|mandatory|trade_acquiring|common|smart|qr
13|2.6.2.1|mandatory|trade_acquiring|common|common|qr
14|2.6.2.2|mandatory|trade_acquiring|common|common|qr
15|2.6.3.1|mandatory|trade_acquiring|common|common|qr
16|2.6.3.2|mandatory|trade_acquiring|common|common|qr
17|2.7|optional|common|common|common|common
18|3.1|optional|common|common|common|common
19|3.2|optional|common|common|common|common
20|3.3|mandatory|common|common|common|common
21|4.1.1|optional|common|common|common|qr
22|4.1.2|optional|common|common|common|common
23|4.1.3|optional|trade_acquiring|common|common|qr_sber_pay
24|4.2.1|mandatory|common|common|common|common
25|4.2.2|optional|common|common|common|common
26|4.2.3|optional|common|fz_223|common|common
27|4.2.4|optional|common|common|common|common
28|4.2.5|mandatory|common|common|common|common
29|4.2.6|mandatory|common|common|common|common
30|4.2.7|mandatory|common|common|common|common
31|4.2.8|mandatory|common|common|common|common
32|4.2.9|mandatory|common|common|common|common
33|4.2.10|mandatory|common|common|common|common
34|4.2.11|mandatory|common|common|common|common
35|4.2.12|optional|common|common|common|common
36|4.2.13|mandatory|common|common|common|common
37|4.2.14|mandatory|common|common|common|common
38|4.2.15|mandatory|common|common|common|common
39|4.2.16.1|mandatory|common|common|common|common
40|4.2.16.2|mandatory|common|common|common|common
41|4.2.16.3|mandatory|common|common|common|common
42|4.2.17|mandatory|internet_acquiring|common|common|common
43|4.2.18|mandatory|common|common|common|common
44|4.2.19|mandatory|common|common|common|common
45|4.2.20.1|mandatory|trade_acquiring|common|common|common
46|4.2.20.2|mandatory|trade_acquiring|common|common|common
47|4.2.20.3|mandatory|trade_acquiring|common|common|common
48|4.2.20.4|mandatory|trade_acquiring|common|common|common
49|4.2.20.5|mandatory|trade_acquiring|common|common|common
50|4.2.20.6|mandatory|trade_acquiring|common|common|common
51|4.2.20.7|mandatory|trade_acquiring|common|common|common
52|4.2.21.1|mandatory|internet_acquiring|common|common|common
53|4.2.21.2|mandatory|internet_acquiring|common|common|common
54|4.2.21.3|mandatory|internet_acquiring|common|common|common
55|4.2.21.4|mandatory|internet_acquiring|common|common|common
56|4.2.21.5|mandatory|internet_acquiring|common|common|common
57|4.2.21.6|mandatory|internet_acquiring|common|common|common
58|4.2.21.7|mandatory|internet_acquiring|common|common|common
59|4.2.21.8|mandatory|internet_acquiring|common|common|common
60|4.2.22|optional|trade_acquiring|common|common|qr
61|4.2.23|optional|trade_acquiring|common|common|qr
62|4.2.24|optional|common|common|common|qr
63|4.2.25|optional|common|common|common|qr
64|4.2.26|mandatory|internet_acquiring|common|common|common
65|5.1.1.1|mandatory|common|common|common|common
66|5.1.1.2|mandatory|common|common|common|common
67|5.1.1.3|mandatory|common|common|common|common
68|5.1.1.4|mandatory|common|common|common|common
69|5.1.1.5|mandatory|common|common|common|common
70|5.1.1.6|mandatory|trade_acquiring|common|common|common
71|5.1.2|mandatory|common|common|common|common
72|5.1.3|mandatory|common|common|common|common
73|5.1.4|mandatory|common|common|common|common
74|5.1.5|mandatory|common|common|common|common
75|5.1.6|mandatory|common|common|common|common
76|5.1.7|mandatory|common|common|common|common
77|5.1.8.1|optional|common|common|common|common
78|5.1.8.2|optional|common|common|common|common
79|5.1.8.3|optional|common|common|common|common
80|5.1.8.4|optional|internet_acquiring|common|common|common
81|5.1.8.5|optional|internet_acquiring|common|common|common
82|5.1.8.6|optional|common|common|common|common
83|5.1.8.7|optional|common|common|common|common
84|5.1.8.8|optional|trade_acquiring|common|common|common
85|5.1.8.9|optional|common|common|common|common
86|5.1.8.10|optional|common|common|common|common
87|5.1.8.11|optional|common|common|common|common
88|5.1.8.12|optional|common|common|common|common
89|5.1.8.13|optional|common|common|common|common
90|5.1.9|mandatory|common|common|common|common
91|5.1.10|mandatory|common|common|common|common
92|5.1.11|mandatory|common|common|common|common
93|5.1.12|optional|common|common|common|common
94|5.1.13|optional|common|common|common|common
95|5.1.14|mandatory|common|common|common|common
96|5.1.15|optional|common|common|common|common
97|5.1.16|mandatory|common|common|common|common
98|5.1.17.1|optional|trade_acquiring|common|pos|common
99|5.1.17.2|optional|trade_acquiring|common|smart|common
100|5.2.1|mandatory|internet_acquiring|common|common|common
101|5.2.2|mandatory|internet_acquiring|common|common|common
102|5.2.3|mandatory|trade_acquiring|common|common|common
103|5.2.4|optional|common|common|common|common
104|5.2.5|optional|common|common|common|common
105|5.2.6|optional|trade_acquiring|common|common|common
106|5.2.7|optional|common|common|common|common
107|5.2.8|mandatory|common|common|common|common
108|5.2.9|optional|trade_acquiring|common|common|qr
109|5.2.10|mandatory|common|common|common|common
110|5.2.12|optional|internet_acquiring|common|common|qr
111|6.1|mandatory|common|common|common|common
112|6.2|mandatory|common|common|common|common
113|6.3|mandatory|common|fz_223|common|common
114|6.4|mandatory|common|common|common|common
115|6.5|mandatory|common|common|common|common
116|6.6|mandatory|common|fz_223|common|common
117|6.7|mandatory|trade_acquiring|common|smart|common
118|6.8|mandatory|trade_acquiring|common|smart|common
119|6.9|mandatory|trade_acquiring|fz_223|smart|common
120|6.10|mandatory|trade_acquiring|common|smart|common
121|6.11|mandatory|trade_acquiring|common|smart|common
122|6.12|mandatory|trade_acquiring|fz_223|smart|common
123|6.13|mandatory|trade_acquiring|common|smart|common
124|6.14|mandatory|trade_acquiring|common|smart|common
125|6.15|mandatory|trade_acquiring|fz_223|smart|common
126|6.16|mandatory|trade_acquiring|common|smart|common
127|6.17|mandatory|trade_acquiring|common|smart|common
128|6.18|mandatory|trade_acquiring|fz_223|smart|common
129|6.20|mandatory|common|common|common|common
130|6.21|mandatory|common|common|common|common
131|7.1|mandatory|common|common|common|common
132|7.2|mandatory|common|common|common|common
133|7.3|mandatory|common|common|common|common
134|7.4|mandatory|common|common|common|common
135|7.5|mandatory|common|common|common|common
136|7.6|mandatory|common|common|common|common
137|7.7|mandatory|common|common|common|common
138|7.8|optional|common|common|common|common
139|7.9|optional|common|common|common|common
140|7.10|optional|common|common|common|common
141|7.11|optional|common|common|common|common
142|7.12|optional|common|common|common|common
143|7.13|mandatory|internet_acquiring|common|common|common
144|7.14|mandatory|common|common|common|common
145|7.15|mandatory|common|common|common|common
146|7.16|mandatory|common|common|common|common
147|7.17|mandatory|common|common|common|common
148|8.1|mandatory|common|common|common|common
149|8.2|mandatory|common|common|common|common
150|9.1|mandatory|common|common|common|common
151|9.2|mandatory|common|common|common|common
152|9.3|mandatory|common|common|common|common
153|10.1|mandatory|common|common|common|common
154|10.2|mandatory|common|common|common|common
155|10.3|mandatory|common|common|common|common
156|11.1|optional|common|common|common|common
157|11.2|optional|common|common|common|common
158|11.3|optional|common|common|common|common
159|11.4|optional|common|common|common|common
160|11.5|optional|common|common|common|common
161|11.6|optional|common|common|common|common
162|11.7|optional|common|common|common|common
163|11.8|optional|common|common|common|common
164|11.9|optional|common|common|common|common
165|11.10|optional|common|common|common|common
166|11.11|optional|common|common|common|common
167|11.12|optional|common|common|common|common
168|11.13|optional|common|common|common|common

[Command succeeded with exit code 0]
AI: [{'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json', 'offset': 1200, 'limit': 500}, 'id': 'call_00_pGUah9jmSQ0XjfAESWVP5424', 'type': 'tool_call'}]
Tool:   1201	 },
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
  1301	 {
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
AI: [{'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json', 'limit': 500, 'offset': 1700}, 'id': 'call_00_WwS5QcKR9ErYe57AR8pq8160', 'type': 'tool_call'}]
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
  2101	  "only_for_product":"common",
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
AI: [{'name': 'read_file', 'args': {'file_path': 'inputs/matrix.json', 'limit': 400, 'offset': 2200}, 'id': 'call_00_LyiWw9AVsGGPJJ8CP8AR0272', 'type': 'tool_call'}]
Tool:   2201	  "number":"10.2",
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
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read all source files (matrix, contract, reference docs)', 'status': 'completed'}, {'content': 'Determine contract profile and applicability filters', 'status': 'completed'}, {'content': 'Build coverage_ledger.matrix - classify all 169 matrix items', 'status': 'in_progress'}, {'content': 'Build links (aligned + deviation) with contract packages', 'status': 'pending'}, {'content': 'Build unmatched_matrix (missing_in_contract)', 'status': 'pending'}, {'content': 'Build coverage_ledger.contract - classify all material contract clauses', 'status': 'pending'}, {'content': 'Build unmatched_contract (extra_in_contract)', 'status': 'pending'}, {'content': 'Verify all quality checks and write outputs/discrepancy_analysis.json', 'status': 'pending'}]}, 'id': 'call_00_0ImngBzEy1ln9m5lksrO4513', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read all source files (matrix, contract, reference docs)', 'status': 'completed'}, {'content': 'Determine contract profile and applicability filters', 'status': 'completed'}, {'content': 'Build coverage_ledger.matrix - classify all 169 matrix items', 'status': 'in_progress'}, {'content': 'Build links (aligned + deviation) with contract packages', 'status': 'pending'}, {'content': 'Build unmatched_matrix (missing_in_contract)', 'status': 'pending'}, {'content': 'Build coverage_ledger.contract - classify all material contract clauses', 'status': 'pending'}, {'content': 'Build unmatched_contract (extra_in_contract)', 'status': 'pending'}, {'content': 'Verify all quality checks and write outputs/discrepancy_analysis.json', 'status': 'pending'}]
AI: Given the 169 matrix items and extensive contract text, I'll build the analysis systematically using a Python script for structural accuracy, then produce the final JSON.[{'name': 'write_file', 'args': {'content': '#!/usr/bin/env pytho...(argument truncated)', 'file_path': 'outputs/working/build_analysis.py'}, 'id': 'call_00_saWoUU4uQefCBCsS0zQK7990', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/build_analysis.py
AI: Let me take a more direct approach and write the complete analysis as a single comprehensive Python script:[{'name': 'write_file', 'args': {'content': '#!/usr/bin/env python3\n"""Build the complete discrepancy_analysis.json for acquiring contract review."""\nimport json\n\n# ============================================================\n# PROFILE\n# ============================================================\nprofile = {\n    "product": ["trade_acquiring"],\n    "legal_regime": "44_fz"\n}\n\n# ============================================================\n# MATRIX COVERAGE LEDGER — all 169 rows\n# ============================================================\n# Format: (matrix_id, closure, reason)\n# Closure: linked | missing_in_contract | out_of_scope | not_applicable\n\nmatrix_rows = [\n    # === Section 2: Registration, Currency, Document Exchange ===\n    ("2.1", "linked",\n     "Contract 4.3 requires TST registration application + info; Bank right to refuse without explanation is absent → deviation"),\n    ("2.2", "linked",\n     "Contract 4.4 + Technical Assignment p.5 confirm settlement in RUB; aligned"),\n    ("2.3.1", "linked",\n     "Contract 2.3.1 mirrors email exchange with full legal force; aligned"),\n    ("2.3.2", "linked",\n     "Contract 2.3.2 mirrors DBO system exchange; aligned"),\n    ("2.3.3", "linked",\n     "Contract 2.3.3 mirrors courier delivery; aligned"),\n    ("2.3.4", "linked",\n     "Contract 2.3.4 mirrors registered mail; aligned"),\n    ("2.3.5", "linked",\n     "Contract 2.3.5 analogue exists but automated system name is blank placeholder → deviation"),\n    ("2.3.6", "linked",\n     "Contract 2.3.6 — EIS channel present and applicable for 44-FZ regime; aligned"),\n    ("2.3.7", "linked",\n     "Contract 2.3.7 support service channel + receipt-date rules match matrix; aligned"),\n    ("2.4", "linked",\n     "Contract 1.1 + 12.5 declare appendices integral parts of contract; aligned"),\n    ("2.5.1.1", "out_of_scope",\n     "only_for_product=internet_acquiring; contract is trade_acquiring only, no internet acquiring"),\n    ("2.5.2.1", "out_of_scope",\n     "payment_method=sber_pay_face_scan; no biometric/SberPay Face Scan product in contract"),\n    ("2.6.1.1", "out_of_scope",\n     "only_for_terminal=smart; contract has POS terminals only, no smart terminals"),\n    ("2.6.2.1", "missing_in_contract",\n     "QR-API mechanism absent; contract has QR display capability on terminals (Technical Assignment) but no active QR-API product or own KKT software integration"),\n    ("2.6.2.2", "missing_in_contract",\n     "QR-Vendor mechanism absent; no own KKT software requiring Vendor QR integration"),\n    ("2.6.3.1", "missing_in_contract",\n     "QR auto-connect on Bank terminal absent; QR display capability mentioned in Technical Assignment is not an active QR acquiring product mechanism"),\n    ("2.6.3.2", "missing_in_contract",\n     "QR disconnect by merchant initiative absent; no active QR product to disconnect"),\n    ("2.7", "linked",\n     "Contract 12.4 — electronic form with UKEP, equal legal force to paper; aligned"),\n\n    # === Section 3: Subject ===\n    ("3.1", "linked",\n     "Contract 1.3 — Customer organizes card acceptance; Technical Assignment p.3 lists accepted card systems (МИР, VISA, MC); aligned"),\n    ("3.2", "linked",\n     "Contract 5.1.10 + 5.1.8 — Bank duty to transfer operation sums to Customer; aligned"),\n    ("3.3", "linked",\n     "Contract 3.2 + 4.4 + Specification — Customer pays Bank fee from each operation; aligned"),\n\n    # === Section 4: Merchant Rights & Duties ===\n    ("4.1.1", "missing_in_contract",\n     "No right for Customer to reference card/QR payment in own materials requiring Bank pre-approval; payment_method=qr, no active QR product; for card-only aspect, contract 5.4.5 provides right to reference cards with Bank approval — see links"),\n    ("4.1.2", "linked",\n     "Contract 5.9 — Customer right to consultation on terminal operation via support service; aligned"),\n    ("4.1.3", "out_of_scope",\n     "payment_method=qr_sber_pay; no SberPay or active QR product in contract"),\n    ("4.2.1", "linked",\n     "Contract 3.2 + 4.4 + Specification — Customer pays Bank for settlement services; aligned"),\n    ("4.2.2", "missing_in_contract",\n     "No explicit duty for Customer to comply with Bank instructive materials; Contract 5.10 covers self-training on website but no obligation to comply with Bank instructions"),\n    ("4.2.3", "out_of_scope",\n     "only_for_lot=fz_223; contract is 44-FZ regime"),\n    ("4.2.4", "linked",\n     "Contract 5.3.7 — Customer duty to place Bank informational materials at TST; aligned"),\n    ("4.2.5", "linked",\n     "Contract 5.3.8 + 5.3.9 partially cover — no splitting sums, no misuse of card details; but \'accept all listed cards during all working hours\', \'no cash disbursement\', and \'max 2 cards per buyer\' are absent → deviation"),\n    ("4.2.6", "linked",\n     "Contract 5.3.8 — Customer duty not to split one operation into multiple sums; aligned"),\n    ("4.2.7", "linked",\n     "Contract 5.3.9 — Customer duty not to use card details for purposes other than operations; aligned"),\n    ("4.2.8", "missing_in_contract",\n     "No provision that card-payment prices do not exceed cash prices; absent from contract"),\n    ("4.2.9", "linked",\n     "Contract 5.3.10 — Customer duty to conduct operations and prepare documents per rules, bears responsibility for correctness; aligned"),\n    ("4.2.10", "linked",\n     "Contract 5.3.11 — store documents 13+ months, provide copies within 3 working days of Bank request, proper quality; aligned"),\n    ("4.2.11", "linked",\n     "Contract 5.5 — provide written statement of operation circumstances within 3 working days of Bank request, immediate notice of document loss; aligned"),\n    ("4.2.12", "missing_in_contract",\n     "No acceptance of Bank payment claims/invoices within 5 working days; EIS acceptance procedure (Contract 8.3-8.5) replaces but does not create the same direct-debit/acceptance mechanism for Bank fees"),\n    ("4.2.13", "linked",\n     "Contract 5.3.19 — Customer duty to reimburse Bank for disputed/invalid operation amounts, chargeback fees, and Bank losses from payment system penalties; aligned in scope but missing \'безусловном порядке\' (unconditional) and some detail → deviation"),\n    ("4.2.14", "linked",\n     "Contract 5.3.13 — notify Bank within 3 working days of reorganization, changes, bankruptcy, leadership/address/rekvizit changes; aligned"),\n    ("4.2.15", "linked",\n     "Contract 5.3.14 — provide reliable documents/s info annually and within 7 working days of Bank request, including beneficial owners; aligned"),\n    ("4.2.16.1", "linked",\n     "Contract 5.3.20 — transfer of director PDn (full name, address, passport) with guarantee of legal basis, consent for Mir transfer, duty to notify of consent withdrawal; aligned"),\n    ("4.2.16.2", "missing_in_contract",\n     "No provision for employee PDn consent (non-director staff: full name, mobile, email, position, workplace) with transfer to service companies; contract 5.3.20 only covers director"),\n    ("4.2.16.3", "linked",\n     "Contract 5.3.15 — provide proof of lawful PDn transfer within 3 working days of written Bank request; indemnify Bank for claims/losses if proof not provided; covers director per 5.3.20 context, employee scope missing → deviation"),\n    ("4.2.17", "out_of_scope",\n     "only_for_product=internet_acquiring; contract is trade_acquiring only"),\n    ("4.2.18", "linked",\n     "Contract 5.3.16 — from termination date, cease card acceptance, remove informational materials; aligned"),\n    ("4.2.19", "linked",\n     "Contract 5.3.17 — not obstruct Bank checks for fraud/activity mismatch, assist in suspicious operation investigation; aligned"),\n    ("4.2.20.1", "linked",\n     "Contract 5.10 — Customer ensures employees self-train on operation procedures posted at Bank website; aligned, website is blank placeholder → deviation"),\n    ("4.2.20.2", "linked",\n     "Contract 5.3.18.1 — use terminals/SIM/software only for contract purposes at registration/installation address, no modifications, no self-repair, no transfer to third parties except service company; aligned"),\n    ("4.2.20.3", "linked",\n     "Contract 5.3.18.2 — provide Bank/service company access to terminal installation sites for connection, setup, repair, replacement, maintenance, inspection; aligned"),\n    ("4.2.20.4", "linked",\n     "Contract 5.3.18.3 — accept terminals by acceptance act in 2 copies, one kept by each party; form per service company; aligned"),\n    ("4.2.20.5", "linked",\n     "Contract 5.3.20.4 [sic — 5.3.18.4] — immediately inform Bank of terminal malfunction or loss; aligned"),\n    ("4.2.20.6", "linked",\n     "Contract 5.3.18.5 — return terminals within 5 working days of termination or Bank demand; aligned"),\n    ("4.2.20.7", "linked",\n     "Contract 5.6 + 5.7 — штраф 10 000 руб for each electronic terminal, 25 000 руб for smart terminal on non-return; matrix expects 25 000 for both → deviation on electronic terminal штраф amount"),\n    ("4.2.21.1", "out_of_scope",\n     "only_for_product=internet_acquiring; contract is trade_acquiring only"),\n    ("4.2.21.2", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.21.3", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.21.4", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.21.5", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.21.6", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.21.7", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.21.8", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("4.2.22", "missing_in_contract",\n     "No duty to provide QR code to buyer for SberPayQR/Plati QR; payment_method=qr, no active QR product"),\n    ("4.2.23", "missing_in_contract",\n     "No prohibition on unilateral QR code change; payment_method=qr, no active QR product"),\n    ("4.2.24", "missing_in_contract",\n     "No API usage within QR-API functional boundaries; payment_method=qr, no active QR-API"),\n    ("4.2.25", "missing_in_contract",\n     "No duty to suspend API and notify Bank on QR-API security breach; payment_method=qr, no active QR-API"),\n    ("4.2.26", "out_of_scope",\n     "only_for_product=internet_acquiring; recurring payments in internet acquiring context"),\n\n    # === Section 5.1: Bank Rights ===\n    ("5.1.1.1", "linked",\n     "Contract 5.2.10 + 5.2.10.1 — Bank right to withhold invalid operation amounts with substantively matching 12 grounds; aligned"),\n    ("5.1.1.2", "linked",\n     "Contract 5.2.10.2 — Bank right to withhold erroneously transferred sums; aligned"),\n    ("5.1.1.3", "linked",\n     "Contract 5.2.10.3 — Bank right to withhold return/chargeback/reversal amounts; aligned"),\n    ("5.1.1.4", "linked",\n     "Contract 5.2.10.4 — Bank right to withhold disputed/charged-back sums; aligned (SberPay/Plati QR element not applicable)"),\n    ("5.1.1.5", "linked",\n     "Contract 5.2.10.5 — Bank right to withhold штраф/loss amounts from payment system penalties and government liability due to Customer breach; aligned"),\n    ("5.1.1.6", "linked",\n     "Contract 5.2.10 read with 5.6/5.7 — Bank can withhold штраф for terminal non-return; aligned"),\n    ("5.1.2", "missing_in_contract",\n     "No Bank right to suspend authorization when Customer has debt until full repayment; contract 5.2.9 covers specific termination/pause grounds but not a general debt-suspension right"),\n    ("5.1.3", "linked",\n     "Contract 5.2.10 + Приложение 1.1 p.3 (заранее данный акцепт) — Bank right to direct debit from Customer account for amounts in 5.1.1 when unable to withhold from future transfers; aligned"),\n    ("5.1.4", "linked",\n     "Contract 4.4 — Bank payment claim/invoice mechanism using Customer bank account details; account number and bank name are filled (Южное ГУ Банка России/УФК); aligned"),\n    ("5.1.5", "missing_in_contract",\n     "No explicit Bank right not to reimburse operations conducted in violation of contract terms; general liability/reimbursement clauses do not create this specific Bank protection"),\n    ("5.1.6", "linked",\n     "Contract 5.2.3 + 5.2.4 — Bank right to inspect terminals, replace with 2 working days notice, remote software update without notice; aligned"),\n    ("5.1.7", "missing_in_contract",\n     "No Bank right to transmit fraud/suspicious operation data including director PDn to Mir payment system independently of contract term; contract covers PDn transfer to Mir only in 5.3.20 context for service provision, not for fraud reporting"),\n    ("5.1.8.1", "linked",\n     "Contract 5.2.9.1 — Bank right to suspend auth/terminate for Customer breach of contract; aligned"),\n    ("5.1.8.2", "linked",\n     "Contract 5.2.9.2 — Bank right to suspend/terminate for extremism/terrorism/WMD financing listing; aligned"),\n    ("5.1.8.3", "linked",\n     "Contract 5.2.9.3 — Bank right to suspend/terminate on money laundering/terrorism financing suspicion; aligned"),\n    ("5.1.8.4", "out_of_scope",\n     "only_for_product=internet_acquiring; contract is trade_acquiring only"),\n    ("5.1.8.5", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("5.1.8.6", "linked",\n     "Contract 5.2.9.4 — Bank right to suspend/terminate on negative info from state authorities/payment systems; aligned"),\n    ("5.1.8.7", "linked",\n     "Contract 5.2.9.5 + 5.2.9 preamble — Bank right to suspend/terminate on fraud info from issuer banks/payment systems; aligned"),\n    ("5.1.8.8", "linked",\n     "Contract 5.2.9.6 — Bank right to suspend/terminate for TST premises renovation preventing operations; aligned"),\n    ("5.1.8.9", "linked",\n     "Contract 5.2.9.7 — Bank right to suspend/terminate for Customer liquidation/bankruptcy; aligned"),\n    ("5.1.8.10", "linked",\n     "Contract 5.2.9.8 — Bank right to suspend/terminate for false Customer/TST/manager info at contract conclusion; aligned"),\n    ("5.1.8.11", "linked",\n     "Contract 5.2.9.9 — Bank right to suspend/terminate for goods/services mismatch with declared activity; aligned"),\n    ("5.1.8.12", "linked",\n     "Contract 5.2.9.10 — Bank right to suspend/terminate for 30 calendar days without operations; aligned"),\n    ("5.1.8.13", "linked",\n     "Contract 5.2.9.11 — Bank right to suspend/terminate on price exhaustion or contract term expiry; aligned"),\n    ("5.1.9", "missing_in_contract",\n     "No Bank right to conduct additional operation checks including contacting issuer bank for legitimacy verification; contract 5.2.5 allows document requests but not issuer verification"),\n    ("5.1.10", "linked",\n     "Contract 5.2.3 (inspection of terminals/order of operation) + Contract 5.3.17 (Customer duty not to obstruct fraud checks) — Bank right to inspect for fraud/activity mismatch partially covered; explicit \'проверка Предприятия\' right and resource access missing → deviation"),\n    ("5.1.11", "linked",\n     "Contract 5.2.5 — Bank right to request operation documents within 13 months, written statements, invoices, receipts; aligned"),\n    ("5.1.12", "missing_in_contract",\n     "No Bank right to unilaterally amend referenced documents by website publication with 1 calendar day notice; contract 11.2 variation procedure requires bilateral written form"),\n    ("5.1.13", "missing_in_contract",\n     "No Bank right to notify of own rekvizit changes via official website; contract 5.2.6 requires written notification to Customer within 3 working days — different channel (written vs website)"),\n    ("5.1.14", "linked",\n     "Contract 5.2.7 — Bank right to send operation-info requests to Customer email from Application/Info; aligned"),\n    ("5.1.15", "missing_in_contract",\n     "No Bank right to refuse contract conclusion without explanation; 44-FZ procurement regime makes this right inapplicable in practice but matrix requires it as a standard protection"),\n    ("5.1.16", "linked",\n     "Contract 5.2.8 — Bank right to demand documents/info needed for statutory functions; aligned"),\n    ("5.1.17.1", "linked",\n     "Contract has POS terminals; matrix 5.1.17.1 (POS terminal turnover threshold for unilateral termination) — not present in contract → missing_in_contract. Reclassified."),\n    ("5.1.17.2", "out_of_scope",\n     "only_for_terminal=smart; contract has no smart terminals"),\n\n    # === Section 5.2: Bank Duties ===\n    ("5.2.1", "out_of_scope",\n     "only_for_product=internet_acquiring; contract is trade_acquiring only"),\n    ("5.2.2", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("5.2.3", "linked",\n     "Contract 5.1.1 — install and prepare terminals within 5 working days, conduct initial staff instruction with Bank materials; matrix expects \'not less than 3 working days\', contract has 5 — beneficial to Bank → aligned"),\n    ("5.2.4", "linked",\n     "Contract 5.1.6 — Bank duty to provide 24/7 authorization; aligned"),\n    ("5.2.5", "linked",\n     "Contract 5.1.1 — Bank to place training materials at website (URL blank/placeholder → deviation on specific URL); aligned on duty"),\n    ("5.2.6", "linked",\n     "Contract 5.1.7 — Bank duty to provide terminals with informational materials needed for operations; aligned"),\n    ("5.2.7", "linked",\n     "Contract 5.1.4 — Bank duty for 24/7 terminal operability, replacement within 3 working days of Customer support call; aligned"),\n    ("5.2.8", "linked",\n     "Contract 5.1.8 — Bank duty to transfer operation sums within 2 working days of receiving settlement info (date = working day after electronic reconciliation), or within 3 calendar days after last reconciliation on technical failure; aligned"),\n    ("5.2.9", "missing_in_contract",\n     "No Bank duty to provide QR code to merchant in electronic or paper form; payment_method=qr, no active QR product"),\n    ("5.2.10", "linked",\n     "Contract 5.1.9 — Bank duty to process PDn per 152-FZ, ensure confidentiality and protection; aligned"),\n    ("5.2.12", "out_of_scope",\n     "only_for_product=internet_acquiring; contract is trade_acquiring only"),\n\n    # === Section 6: Bank Service Fees ===\n    ("6.1", "linked",\n     "Contract 3.2 + Specification — fee as percentage of each operation; Specification has blank percentage field → deviation on exact rate"),\n    ("6.2", "linked",\n     "Contract 8.3.1 + 8.3.2 — EIS acceptance document replaces UPD; monthly, not later than 10th working day (vs matrix 5th); VAT inclusion covered → deviation on document type and timing"),\n    ("6.3", "out_of_scope",\n     "only_for_lot=fz_223; contract is 44-FZ"),\n    ("6.4", "linked",\n     "Contract 8.5 — EIS acceptance procedure: Customer signs within 10 working days or motivated refusal; matrix requires UPD return by 25th of following month → different mechanism but preserved acceptance → aligned"),\n    ("6.5", "linked",\n     "Contract 4.5 — payment within 7 working days of acceptance document signing (vs matrix 5 working days) → deviation on payment deadline"),\n    ("6.6", "out_of_scope",\n     "only_for_lot=fz_223"),\n    ("6.7", "out_of_scope",\n     "only_for_terminal=smart; no smart terminals in contract"),\n    ("6.8", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.9", "out_of_scope",\n     "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.10", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.11", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.12", "out_of_scope",\n     "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.13", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.14", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.15", "out_of_scope",\n     "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.16", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.17", "out_of_scope",\n     "only_for_terminal=smart"),\n    ("6.18", "out_of_scope",\n     "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.20", "linked",\n     "Technical Assignment p.5 — no fee for return/chargeback/reversal operations, original fee not refunded; aligned"),\n    ("6.21", "linked",\n     "Contract 3.1 — maximum contract price 1 900 000 RUB specified; aligned"),\n\n    # === Section 7: Liability ===\n    ("7.1", "linked",\n     "Contract 7.1 — parties bear liability per contract and RF legislation for non-performance; aligned"),\n    ("7.2", "linked",\n     "Contract 7.4 + 7.4.1 — штраф for Customer non-performance (excluding delay) per PP 1042: 1000 RUB for contract ≤3M; contract price 1.9M → 1000 RUB штраф; aligned"),\n    ("7.3", "linked",\n     "Contract 7.1 para 4 — total штраф for Customer cannot exceed contract price; aligned"),\n    ("7.4", "linked",\n     "Contract 7.5-7.6 — Bank delay penalty 1/300 key rate from contract price reduced by performed volume; aligned"),\n    ("7.5", "linked",\n     "Contract 7.7 + 7.7.1 — Bank штраф per PP 1042: 10% of contract price for ≤3M; aligned"),\n    ("7.6", "linked",\n     "Contract 7.7.3 — Bank штраф for non-pecuniary obligations: 1000 RUB for ≤3M; aligned"),\n    ("7.7", "linked",\n     "Contract 7.10 — total Bank штраф cannot exceed contract price; aligned"),\n    ("7.8", "missing_in_contract",\n     "No Bank exemption from liability for disputes between Customer and Buyer not related to contract subject or for goods/services paid by card; contract 7.1 only has general liability clause"),\n    ("7.9", "missing_in_contract",\n     "No Bank exemption from liability for fund transfer delays not caused by Bank; absent from contract"),\n    ("7.10", "missing_in_contract",\n     "No Bank exemption from liability for third-party actions/inactions including payment system participants; absent from contract"),\n    ("7.11", "missing_in_contract",\n     "No Bank exemption from liability for delayed transfer during Bank investigation of suspected violation; absent from contract"),\n    ("7.12", "missing_in_contract",\n     "No Bank exemption from liability for exceeding contract price; absent from contract"),\n    ("7.13", "out_of_scope",\n     "only_for_product=internet_acquiring"),\n    ("7.14", "missing_in_contract",\n     "No Customer liability for all actions in SPEP; SPEP not applicable to trade_acquiring but matrix row is common. Contract has no SPEP mechanism."),\n    ("7.15", "missing_in_contract",\n     "No Customer full liability for personnel actions violating contract/Bank instructions; contract 5.3.10 covers document correctness but not explicit personnel liability"),\n    ("7.16", "linked",\n     "Contract 6.1 — anti-corruption clause; aligned"),\n    ("7.17", "missing_in_contract",\n     "No Customer financial liability for recurring payments non-compliance; recurring payments not present in trade_acquiring contract but matrix row is common"),\n\n    # === Section 8: Force Majeure ===\n    ("8.1", "linked",\n     "Contract 9.1 — force majeure definition, examples, proportional extension of deadline; aligned"),\n    ("8.2", "linked",\n     "Contract 9.2 — notification within 5 days (vs matrix 24 hours — deviation on notice period), right to terminate after 1 month (vs matrix 3 months — deviation on period); aligned on mechanism, deviation on hard terms"),\n\n    # === Section 9: Dispute Resolution ===\n    ("9.1", "linked",\n     "Contract 10.1 — mandatory pre-trial dispute resolution by negotiations; aligned"),\n    ("9.2", "linked",\n     "Contract 10.1 — 10 calendar days for claim response; aligned"),\n    ("9.3", "linked",\n     "Contract 10.2 — unresolved disputes to Arbitration Court of Krasnodar Krai per RF legislation; aligned"),\n\n    # === Section 10: Term and Termination ===\n    ("10.1", "linked",\n     "Contract 11.1 — effective from signing to 30.12.2025 or price exhaustion; liability survives termination; aligned"),\n    ("10.2", "linked",\n     "Contract 11.3 + 11.5 — unilateral termination per 44-FZ and GK RF; 44-FZ procedure replaces 30-day notice → deviation on notice period for non-44-FZ grounds"),\n    ("10.3", "linked",\n     "Contract 11.1 — post-termination settlement period per 44-FZ; matrix 18-month settlement period absent → deviation on settlement timeline"),\n\n    # === Section 11: Miscellaneous ===\n    ("11.1", "missing_in_contract",\n     "No clause that payment system rules prevail over contract if consistent with RF law; absent from contract"),\n    ("11.2", "missing_in_contract",\n     "No confidentiality of card numbers, PDn, operation amounts, payment info with prohibition on third-party transfer; absent from contract"),\n    ("11.3", "missing_in_contract",\n     "No non-disclosure of card security elements, operation technology, financial/management info; absent from contract"),\n    ("11.4", "linked",\n     "Contract 11.2 — changes/additions valid only if written and signed by both parties; aligned"),\n    ("11.5", "linked",\n     "Contract 11.7 — prior agreements/negotiations/correspondence superseded by contract; aligned via general hierarchy"),\n    ("11.6", "linked",\n     "Contract 12.4 — electronic form signed by UKEP, replaces physical copies; aligned via 44-FZ electronic conclusion"),\n    ("11.7", "linked",\n     "Contract 1.1 + 12.5 — appendices are integral parts; aligned"),\n    ("11.8", "missing_in_contract",\n     "No Customer warranty that goods/services sales comply with RF legislation; absent from contract"),\n    ("11.9", "linked",\n     "Contract 12.1 — no substitution of Executor except legal succession by reorganization; Customer substitution 12.2 — rights transfer to new Customer; aligned"),\n    ("11.10", "linked",\n     "Contract 12.1-12.2 — reorganization succession, liquidation claims per legislation; aligned"),\n    ("11.11", "missing_in_contract",\n     "No provision that Bank instructive materials posted on official website become binding next working day; absent"),\n    ("11.12", "linked",\n     "Contract 10.1 para 2 — notices per contract communication channels; aligned"),\n    ("11.13", "linked",\n     "Contract 12.5 — list of appendices (Technical Assignment, Specification, Application Form, TST Info); aligned"),\n]\n\n# ============================================================\n# LINKS\n# ============================================================\n\nlinks = [\n    # --- 2.1 TST Registration ---\n    {\n        "contract_ids": ["4.3"],\n        "matrix_ids": ["2.1"],\n        "relationship": "deviation",\n        "status_reason": "Contract 4.3 requires post-conclusion TST registration application + info; matrix 2.1 Bank right to refuse registration without explanation is absent from contract",\n        "risk_level": "medium",\n        "discrepancies": [{\n            "type": "other",\n            "description": "Matrix 2.1: Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин. Contract 4.3 provides no Bank refusal right — Customer provides documents after contract conclusion but Bank cannot refuse TST registration.",\n            "risk": "Bank loses pre-registration screening right; TST may be registered that does not meet Bank standards, creating operational and fraud risk"\n        }]\n    },\n\n    # --- 2.2 Currency ---\n    {\n        "contract_ids": ["4.4", "Technical Assignment p.5"],\n        "matrix_ids": ["2.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 4.4 and Technical Assignment confirm RUB settlement; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.3.1 Email ---\n    {\n        "contract_ids": ["2.3.1"],\n        "matrix_ids": ["2.3.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 2.3.1 mirrors matrix email exchange with full legal force; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.3.2 DBO ---\n    {\n        "contract_ids": ["2.3.2"],\n        "matrix_ids": ["2.3.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 2.3.2 mirrors matrix DBO system exchange; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.3.3 Courier ---\n    {\n        "contract_ids": ["2.3.3"],\n        "matrix_ids": ["2.3.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 2.3.3 mirrors courier delivery option; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.3.4 Registered Mail ---\n    {\n        "contract_ids": ["2.3.4"],\n        "matrix_ids": ["2.3.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 2.3.4 mirrors registered mail option; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.3.5 E-invoicing ---\n    {\n        "contract_ids": ["2.3.5"],\n        "matrix_ids": ["2.3.5"],\n        "relationship": "deviation",\n        "status_reason": "Contract 2.3.5 provides E-invoicing channel with UKEP but system name is blank placeholder \'___________________\'",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "other",\n            "description": "Matrix requires named automated system (E-invoicing/СФЕРА-Курьер); contract has blank placeholder preventing identification of the specific EDI operator.",\n            "risk": "Without named system, Bank cannot ensure the EDI channel is operational; low risk as other communication channels remain available"\n        }]\n    },\n\n    # --- 2.3.6 EIS ---\n    {\n        "contract_ids": ["2.3.6"],\n        "matrix_ids": ["2.3.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 2.3.6 EIS channel present for 44-FZ regime with UKEP; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.3.7 Support Service + Receipt Rules ---\n    {\n        "contract_ids": ["2.3.7", "2.3"],\n        "matrix_ids": ["2.3.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 2.3.7 support service channel + receipt-date rules in 2.3 chapeau match matrix; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.4 Integral Documents ---\n    {\n        "contract_ids": ["1.1", "12.5"],\n        "matrix_ids": ["2.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 1.1 and 12.5 declare appendices integral parts; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 2.7 Electronic Conclusion ---\n    {\n        "contract_ids": ["12.4"],\n        "matrix_ids": ["2.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 12.4 — electronic form signed with UKEP, equal legal force to paper; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 3.1 Merchant Card Acceptance ---\n    {\n        "contract_ids": ["1.3", "Technical Assignment p.3"],\n        "matrix_ids": ["3.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 1.3 — Customer organizes card acceptance; Technical Assignment p.3 lists accepted payment systems (МИР, VISA, MC); aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 3.2 Bank Transfers ---\n    {\n        "contract_ids": ["5.1.10", "5.1.8"],\n        "matrix_ids": ["3.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.10 + 5.1.8 — Bank duty to transfer operation sums to Customer; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 3.3 Merchant Pays Bank ---\n    {\n        "contract_ids": ["3.2", "4.4", "Specification"],\n        "matrix_ids": ["3.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 3.2 + 4.4 + Specification — Customer pays Bank fee from each operation monthly; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.1.2 Consultation Right ---\n    {\n        "contract_ids": ["5.9"],\n        "matrix_ids": ["4.1.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.9 — Customer right to consultation on terminal operation via support service; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.1 Payment Duty ---\n    {\n        "contract_ids": ["3.2", "4.4", "Specification"],\n        "matrix_ids": ["4.2.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 3.2 + 4.4 + Specification — Customer pays Bank for settlement services per tariff; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.4 Place Info Materials ---\n    {\n        "contract_ids": ["5.3.7"],\n        "matrix_ids": ["4.2.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.7 — Customer places Bank informational materials at TST; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.5 Card Acceptance Rules ---\n    {\n        "contract_ids": ["5.3.8", "5.3.9", "Technical Assignment p.3"],\n        "matrix_ids": ["4.2.5"],\n        "relationship": "deviation",\n        "status_reason": "Contract covers no-splitting (5.3.8) and no-misuse of card details (5.3.9) and lists accepted cards (Technical Assignment p.3); but \'accept all listed cards during all working hours\', \'no cash disbursement\', and \'max 2 different cards per buyer\' are absent",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "scope",\n            "description": "Matrix requires: (1) accept ALL listed cards during ALL working hours, (2) no cash disbursement on cards, (3) max 2 different cards from one buyer. Contract omits all three specific protections.",\n            "risk": "Customer could selectively accept cards, issue cash, or allow a buyer to split payment across many cards, increasing fraud/operational risk"\n        }]\n    },\n\n    # --- 4.2.6 No Splitting ---\n    {\n        "contract_ids": ["5.3.8"],\n        "matrix_ids": ["4.2.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.8 — Customer duty not to split one operation into multiple sums; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.7 No Misuse of Card Data ---\n    {\n        "contract_ids": ["5.3.9"],\n        "matrix_ids": ["4.2.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.9 — Customer duty not to use card details for purposes other than operations; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.9 Operations per Rules ---\n    {\n        "contract_ids": ["5.3.10"],\n        "matrix_ids": ["4.2.9"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.10 — Customer conducts operations and prepares documents per rules, bears responsibility for correctness; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.10 Document Storage ---\n    {\n        "contract_ids": ["5.3.11"],\n        "matrix_ids": ["4.2.10"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.11 — store documents 13+ months, provide copies within 3 working days of Bank request, proper quality; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.11 Statement on Operations ---\n    {\n        "contract_ids": ["5.5"],\n        "matrix_ids": ["4.2.11"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.5 — provide written statement of operation circumstances within 3 working days of Bank request, immediate notice of document loss; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.13 Reimbursement Duty ---\n    {\n        "contract_ids": ["5.3.19"],\n        "matrix_ids": ["4.2.13"],\n        "relationship": "deviation",\n        "status_reason": "Contract 5.3.19 covers reimbursement for disputed/invalid operations, chargeback fees, and Bank losses from payment system penalties; matrix requires \'в полном объеме и в безусловном порядке\' (unconditional and in full) and broader scope",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "scope",\n            "description": "Matrix requires unconditional (безусловном) reimbursement; contract 5.3.19 lacks the unconditional qualifier. Matrix also covers Bank payments to holders of Bank-issued cards specifically.",\n            "risk": "Customer could dispute reimbursement obligation rather than it being automatic; low residual risk given substantive coverage of reimbursement grounds"\n        }]\n    },\n\n    # --- 4.2.14 Change Notification ---\n    {\n        "contract_ids": ["5.3.13"],\n        "matrix_ids": ["4.2.14"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.13 — notify Bank within 3 working days of reorganization, changes, bankruptcy, leadership/address/rekvizit changes; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.15 KYC/Compliance Docs ---\n    {\n        "contract_ids": ["5.3.14"],\n        "matrix_ids": ["4.2.15"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.14 — provide reliable documents/info annually and within 7 working days of Bank request, including beneficial owners; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.16.1 Director PDn ---\n    {\n        "contract_ids": ["5.3.20"],\n        "matrix_ids": ["4.2.16.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.20 — transfer of director PDn (full name, address, passport) with guarantee of legal basis, consent for Mir transfer, duty to notify of consent withdrawal; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.16.3 PDn Proof ---\n    {\n        "contract_ids": ["5.3.15"],\n        "matrix_ids": ["4.2.16.3"],\n        "relationship": "deviation",\n        "status_reason": "Contract 5.3.15 covers proof of lawful PDn transfer and indemnity; but response deadline is absent (matrix requires 3 working days) and scope limited to director per 5.3.20 context",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "deadline",\n            "description": "Matrix 4.2.16.3 requires proof of lawful PDn transfer within 3 working days of written Bank request. Contract 5.3.15 provides the proof/indemnity mechanism but without a stated response deadline.",\n            "risk": "Without deadline, Customer could delay PDn compliance proof indefinitely, leaving Bank exposed to data-protection liability"\n        }]\n    },\n\n    # --- 4.2.18 Post-Termination ---\n    {\n        "contract_ids": ["5.3.16"],\n        "matrix_ids": ["4.2.18"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.16 — from termination date, cease card acceptance, remove informational materials; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.19 Non-Obstruction ---\n    {\n        "contract_ids": ["5.3.17"],\n        "matrix_ids": ["4.2.19"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.17 — not obstruct Bank checks for fraud/activity mismatch, assist in suspicious operation investigation; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.20.1 Staff Instruction ---\n    {\n        "contract_ids": ["5.10"],\n        "matrix_ids": ["4.2.20.1"],\n        "relationship": "deviation",\n        "status_reason": "Contract 5.10 — Customer ensures employees self-train on operation procedures at Bank website; website URL is blank placeholder",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "other",\n            "description": "Matrix requires instruction materials posted at specific URL (https://www.sberbank.ru/help/business/acquiring); contract has blank placeholder \'___________________________\' for the website.",\n            "risk": "Without specified URL, Customer may not know where to access training materials, reducing effectiveness of staff instruction obligation"\n        }]\n    },\n\n    # --- 4.2.20.2 Terminal Use Restrictions ---\n    {\n        "contract_ids": ["5.3.18.1"],\n        "matrix_ids": ["4.2.20.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.18.1 — use terminals/SIM/software only for contract purposes at installation address, no modifications, no self-repair, no transfer except service company; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.20.3 Access for Service ---\n    {\n        "contract_ids": ["5.3.18.2"],\n        "matrix_ids": ["4.2.20.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.18.2 — provide Bank/service company access to terminal installation sites for connection, setup, repair, replacement, maintenance, inspection; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.20.4 Terminal Acceptance Act ---\n    {\n        "contract_ids": ["5.3.18.3"],\n        "matrix_ids": ["4.2.20.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.18.3 — accept terminals by acceptance act in 2 copies, one kept by each party; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.20.5 Malfunction Notice ---\n    {\n        "contract_ids": ["5.3.20.4"],\n        "matrix_ids": ["4.2.20.5"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.20.4 [5.3.18.4] — immediately inform Bank of terminal malfunction or loss; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.20.6 Terminal Return ---\n    {\n        "contract_ids": ["5.3.18.5", "5.6"],\n        "matrix_ids": ["4.2.20.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.3.18.5 + 5.6 — return terminals within 5 working days of termination or Bank demand; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.2.20.7 Non-Return Penalty ---\n    {\n        "contract_ids": ["5.7"],\n        "matrix_ids": ["4.2.20.7"],\n        "relationship": "deviation",\n        "status_reason": "Contract 5.7 штраф: 10 000 RUB for electronic terminal, 25 000 RUB for smart terminal; matrix requires 25 000 RUB for both types",\n        "risk_level": "medium",\n        "discrepancies": [{\n            "type": "amount",\n            "description": "Matrix 4.2.20.7: штраф 25 000 RUB for each electronic terminal and 25 000 RUB for each smart terminal. Contract 5.7: 10 000 RUB for electronic terminal, 25 000 RUB for smart terminal.",\n            "risk": "Electronic terminal non-return penalty is 60% lower than Bank standard (10 000 vs 25 000 RUB), reducing incentive to return Bank equipment. With 14 terminals deployed, potential loss exposure is significant."\n        }]\n    },\n\n    # --- 5.1.1.1 Invalid Operations Withholding ---\n    {\n        "contract_ids": ["5.2.10", "5.2.10.1"],\n        "matrix_ids": ["5.1.1.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10 + 5.2.10.1 — Bank right to withhold invalid operation amounts; all 12 matrix grounds substantively covered; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.1.2 Erroneous Transfer Withholding ---\n    {\n        "contract_ids": ["5.2.10.2"],\n        "matrix_ids": ["5.1.1.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10.2 — Bank right to withhold erroneously transferred sums; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.1.3 Return/Chargeback Withholding ---\n    {\n        "contract_ids": ["5.2.10.3"],\n        "matrix_ids": ["5.1.1.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10.3 — Bank right to withhold return/chargeback/reversal amounts; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.1.4 Disputed Operations Withholding ---\n    {\n        "contract_ids": ["5.2.10.4"],\n        "matrix_ids": ["5.1.1.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10.4 — Bank right to withhold disputed/charged-back sums; SberPay/Plati QR element not applicable to contract profile; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.1.5 Penalty/Loss Withholding ---\n    {\n        "contract_ids": ["5.2.10.5"],\n        "matrix_ids": ["5.1.1.5"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10.5 — Bank right to withhold штраф/loss amounts from payment system penalties and government liability due to Customer breach; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.1.6 Terminal Non-Return Penalty Withholding ---\n    {\n        "contract_ids": ["5.2.10", "5.7"],\n        "matrix_ids": ["5.1.1.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10 read with 5.7 — Bank can withhold штраф for terminal non-return; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.3 Direct Debit ---\n    {\n        "contract_ids": ["5.2.10", "Приложение 1.1"],\n        "matrix_ids": ["5.1.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.10 + Приложение 1.1 p.3 (заранее данный акцепт) — Bank right to direct debit from Customer account for amounts in 5.1.1 when unable to withhold from future transfers; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.4 Payment Claim ---\n    {\n        "contract_ids": ["4.4"],\n        "matrix_ids": ["5.1.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 4.4 — Bank payment claim/invoice mechanism using Customer bank account details (filled with treasury account); aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.6 Terminal Inspection/Replacement ---\n    {\n        "contract_ids": ["5.2.3", "5.2.4"],\n        "matrix_ids": ["5.1.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.3 + 5.2.4 — Bank right to inspect terminals, replace with 2 working days notice, remote software update without notice; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.1 Contract Breach ---\n    {\n        "contract_ids": ["5.2.9.1"],\n        "matrix_ids": ["5.1.8.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.1 — Bank right to suspend auth/terminate for Customer breach; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.2 Extremism/Terrorism ---\n    {\n        "contract_ids": ["5.2.9.2"],\n        "matrix_ids": ["5.1.8.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.2 — Bank right to suspend/terminate for extremism/terrorism/WMD listing; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.3 AML/CFT ---\n    {\n        "contract_ids": ["5.2.9.3"],\n        "matrix_ids": ["5.1.8.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.3 — Bank right to suspend/terminate on money laundering/terrorism financing suspicion; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.6 Negative Government Info ---\n    {\n        "contract_ids": ["5.2.9.4"],\n        "matrix_ids": ["5.1.8.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.4 — Bank right to suspend/terminate on negative info from state authorities/payment systems; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.7 Fraud Info ---\n    {\n        "contract_ids": ["5.2.9.5", "5.2.9"],\n        "matrix_ids": ["5.1.8.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.5 + 5.2.9 preamble — Bank right to suspend/terminate on fraud info; sufficient confirmation from issuer banks/payment systems via fax/email; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.8 Premises Renovation ---\n    {\n        "contract_ids": ["5.2.9.6"],\n        "matrix_ids": ["5.1.8.8"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.6 — Bank right to suspend/terminate for TST premises renovation preventing operations; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.9 Liquidation/Bankruptcy ---\n    {\n        "contract_ids": ["5.2.9.7"],\n        "matrix_ids": ["5.1.8.9"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.7 — Bank right to suspend/terminate for Customer liquidation/bankruptcy; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.10 False Info ---\n    {\n        "contract_ids": ["5.2.9.8"],\n        "matrix_ids": ["5.1.8.10"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.8 — Bank right to suspend/terminate for false Customer/TST/manager info; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.11 Activity Mismatch ---\n    {\n        "contract_ids": ["5.2.9.9"],\n        "matrix_ids": ["5.1.8.11"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.9 — Bank right to suspend/terminate for goods/services mismatch with declared activity; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.12 30-Day Inactivity ---\n    {\n        "contract_ids": ["5.2.9.10"],\n        "matrix_ids": ["5.1.8.12"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.10 — Bank right to suspend/terminate for 30 calendar days without operations; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.8.13 Price Exhaustion/Term ---\n    {\n        "contract_ids": ["5.2.9.11"],\n        "matrix_ids": ["5.1.8.13"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.9.11 — Bank right to suspend/terminate on price exhaustion or contract term expiry; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.10 Inspection Right ---\n    {\n        "contract_ids": ["5.2.3", "5.3.17"],\n        "matrix_ids": ["5.1.10"],\n        "relationship": "deviation",\n        "status_reason": "Contract covers terminal inspection and non-obstruction but lacks explicit right to \'проверка Предприятия\' for fraud/activity mismatch with resource access",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "scope",\n            "description": "Matrix 5.1.10: Bank right to conduct enterprise checks including for fraud, activity mismatch, and contract compliance, with access to restricted resource sections. Contract 5.2.3 covers terminal inspection only; 5.3.17 covers non-obstruction but does not grant Bank affirmative inspection right.",\n            "risk": "Bank\'s ability to conduct comprehensive enterprise-level checks (beyond terminals) is not explicitly granted; Customer could resist broader inspections"\n        }]\n    },\n\n    # --- 5.1.11 Document Requests ---\n    {\n        "contract_ids": ["5.2.5"],\n        "matrix_ids": ["5.1.11"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.5 — Bank right to request operation documents within 13 months, written statements, invoices, receipts; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.14 Email Requests ---\n    {\n        "contract_ids": ["5.2.7"],\n        "matrix_ids": ["5.1.14"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.7 — Bank right to send operation-info requests to Customer email per Application/Info; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.1.16 Statutory Docs ---\n    {\n        "contract_ids": ["5.2.8"],\n        "matrix_ids": ["5.1.16"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.2.8 — Bank right to demand documents/info needed for statutory functions; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.2.3 Terminal Installation ---\n    {\n        "contract_ids": ["5.1.1"],\n        "matrix_ids": ["5.2.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.1 — install and prepare terminals within 5 working days, conduct initial staff instruction; matrix expects not less than 3 days, 5 days is beneficial; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.2.4 24/7 Authorization ---\n    {\n        "contract_ids": ["5.1.6"],\n        "matrix_ids": ["5.2.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.6 — Bank duty to provide 24/7 authorization; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.2.5 Training Materials ---\n    {\n        "contract_ids": ["5.1.1"],\n        "matrix_ids": ["5.2.5"],\n        "relationship": "deviation",\n        "status_reason": "Contract 5.1.1 — Bank to place training materials at website; URL is blank placeholder",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "other",\n            "description": "Matrix requires training materials at https://www.sberbank.ru/help/business/acquiring. Contract 5.1.1 has blank placeholder for website URL.",\n            "risk": "Without specified URL, Customers cannot locate training materials, undermining staff instruction quality"\n        }]\n    },\n\n    # --- 5.2.6 Terminal Info Materials ---\n    {\n        "contract_ids": ["5.1.7"],\n        "matrix_ids": ["5.2.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.7 — Bank duty to provide terminals with informational materials needed for operations; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.2.7 24/7 Operability ---\n    {\n        "contract_ids": ["5.1.4"],\n        "matrix_ids": ["5.2.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.4 — Bank duty for 24/7 terminal operability, replacement within 3 working days of Customer support call; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.2.8 Fund Transfer ---\n    {\n        "contract_ids": ["5.1.8"],\n        "matrix_ids": ["5.2.8"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.8 — Bank duty to transfer operation sums within 2 working days of receiving settlement info, or within 3 calendar days after last reconciliation on technical failure; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 5.2.10 PDn Processing ---\n    {\n        "contract_ids": ["5.1.9"],\n        "matrix_ids": ["5.2.10"],\n        "relationship": "aligned",\n        "status_reason": "Contract 5.1.9 — Bank duty to process PDn per 152-FZ, ensure confidentiality and protection; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 6.1 Fee Rate ---\n    {\n        "contract_ids": ["3.2", "Specification"],\n        "matrix_ids": ["6.1"],\n        "relationship": "deviation",\n        "status_reason": "Contract 3.2 + Specification establish fee as percentage of each operation but exact percentage is blank in Specification",\n        "risk_level": "medium",\n        "discrepancies": [{\n            "type": "amount",\n            "description": "Matrix 6.1: fee as (______) % of operation sums. Contract Specification has blank field for commission percentage. Neither source fills the rate.",\n            "risk": "Without agreed commission rate, the price term is incomplete; payment calculation is unenforceable until the blank is filled"\n        }]\n    },\n\n    # --- 6.2 Billing Document ---\n    {\n        "contract_ids": ["8.3.1", "8.3.2"],\n        "matrix_ids": ["6.2"],\n        "relationship": "deviation",\n        "status_reason": "Contract uses EIS acceptance document instead of UPD; submission by 10th working day (vs matrix 5th); 44-FZ EIS mechanism replaces template",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "deadline",\n            "description": "Matrix 6.2: Bank sends UPD by 5th working day. Contract 8.3.1: EIS document by 10th working day. Document type differs (EIS document vs UPD) and 5-day delay.",\n            "risk": "Later billing document submission shifts Customer payment timeline later; 44-FZ EIS acceptance mechanism is mandatory and provides enforceable alternative, so risk is low"\n        }]\n    },\n\n    # --- 6.4 Acceptance ---\n    {\n        "contract_ids": ["8.5", "8.5.1", "8.5.7"],\n        "matrix_ids": ["6.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 8.5 — EIS acceptance: Customer signs within 10 working days or motivated refusal; 44-FZ mechanism preserves enforceable acceptance, replaces UPD-by-25th template; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 6.5 Payment Deadline ---\n    {\n        "contract_ids": ["4.5"],\n        "matrix_ids": ["6.5"],\n        "relationship": "deviation",\n        "status_reason": "Contract 4.5: payment within 7 working days of acceptance; matrix 6.5: within 5 working days of UPD signing",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "deadline",\n            "description": "Matrix: 5 working days from UPD signing. Contract: 7 working days from acceptance document signing (November invoices by 30 Dec). 2-day extension.",\n            "risk": "Payment deferral by 2 working days provides marginal cash-flow delay for Bank"\n        }]\n    },\n\n    # --- 6.20 Return/Chargeback Fee ---\n    {\n        "contract_ids": ["Technical Assignment p.5"],\n        "matrix_ids": ["6.20"],\n        "relationship": "aligned",\n        "status_reason": "Technical Assignment p.5 — no fee for return/chargeback/reversal operations, original fee not refunded; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 6.21 Contract Price ---\n    {\n        "contract_ids": ["3.1"],\n        "matrix_ids": ["6.21"],\n        "relationship": "aligned",\n        "status_reason": "Contract 3.1 — maximum contract price 1 900 000 RUB specified; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.1 General Liability ---\n    {\n        "contract_ids": ["7.1"],\n        "matrix_ids": ["7.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.1 — parties bear liability per contract and RF legislation for non-performance; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.2 Customer Penalty ---\n    {\n        "contract_ids": ["7.4", "7.4.1"],\n        "matrix_ids": ["7.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.4 + 7.4.1 — штраф for Customer per PP 1042: 1000 RUB for ≤3M contract; contract price 1.9M matches 1000 RUB bracket; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.3 Customer Penalty Cap ---\n    {\n        "contract_ids": ["7.1", "7.11"],\n        "matrix_ids": ["7.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.1 para 4 + 7.11 — total Customer штраф cannot exceed contract price; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.4 Bank Delay Penalty ---\n    {\n        "contract_ids": ["7.5", "7.6"],\n        "matrix_ids": ["7.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.5-7.6 — Bank delay penalty 1/300 key rate from contract price reduced by performed volume; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.5 Bank Penalty Amount ---\n    {\n        "contract_ids": ["7.7", "7.7.1"],\n        "matrix_ids": ["7.5"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.7 + 7.7.1 — Bank штраф per PP 1042: 10% of contract price for ≤3M; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.6 Bank Non-Pecuniary Penalty ---\n    {\n        "contract_ids": ["7.7.3"],\n        "matrix_ids": ["7.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.7.3 — Bank штраф for non-pecuniary obligations: 1000 RUB for ≤3M; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.7 Bank Penalty Cap ---\n    {\n        "contract_ids": ["7.10"],\n        "matrix_ids": ["7.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 7.10 — total Bank штраф cannot exceed contract price; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 7.16 Anti-Corruption ---\n    {\n        "contract_ids": ["6.1"],\n        "matrix_ids": ["7.16"],\n        "relationship": "aligned",\n        "status_reason": "Contract 6.1 — anti-corruption clause; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 8.1 Force Majeure ---\n    {\n        "contract_ids": ["9.1"],\n        "matrix_ids": ["8.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 9.1 — force majeure definition, examples, proportional extension of deadline; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 8.2 Force Majeure Notice ---\n    {\n        "contract_ids": ["9.2"],\n        "matrix_ids": ["8.2"],\n        "relationship": "deviation",\n        "status_reason": "Contract 9.2: notification within 5 days (vs matrix 24 hours); termination right after 1 month (vs matrix 3 months); material hard-term differences",\n        "risk_level": "medium",\n        "discrepancies": [\n            {\n                "type": "deadline",\n                "description": "Matrix 8.2: force majeure notice within 24 hours. Contract 9.2: notice within 5 days. 5-day vs 24-hour notice period.",\n                "risk": "5-day delay in force majeure notification prevents Bank from taking timely mitigation measures, increasing exposure during operational disruptions"\n            },\n            {\n                "type": "deadline",\n                "description": "Matrix 8.2: termination right after 3 months of force majeure. Contract 9.2: termination right after 1 month. Shorter period benefits Bank.",\n                "risk": "Earlier termination right is beneficial to Bank; this deviation is protective rather than risky"\n            }\n        ]\n    },\n\n    # --- 9.1 Pre-Trial Disputes ---\n    {\n        "contract_ids": ["10.1"],\n        "matrix_ids": ["9.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 10.1 — mandatory pre-trial dispute resolution by negotiations; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 9.2 Claim Period ---\n    {\n        "contract_ids": ["10.1"],\n        "matrix_ids": ["9.2"],\n        "relationship": "aligned",\n        "status_reason": "Contract 10.1 — 10 calendar days for claim response; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 9.3 Court ---\n    {\n        "contract_ids": ["10.2"],\n        "matrix_ids": ["9.3"],\n        "relationship": "aligned",\n        "status_reason": "Contract 10.2 — unresolved disputes to Arbitration Court of Krasnodar Krai per RF legislation; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 10.1 Contract Term ---\n    {\n        "contract_ids": ["11.1", "4.1"],\n        "matrix_ids": ["10.1"],\n        "relationship": "aligned",\n        "status_reason": "Contract 11.1 + 4.1 — effective to 30.12.2025 or price exhaustion; liability survives termination; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 10.2 Unilateral Termination ---\n    {\n        "contract_ids": ["11.3", "11.5"],\n        "matrix_ids": ["10.2"],\n        "relationship": "deviation",\n        "status_reason": "Contract uses 44-FZ unilateral termination procedure (Art. 95) instead of 30-day notice; 44-FZ regime makes this different from matrix template but enforceable",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "procedure",\n            "description": "Matrix 10.2: either party may terminate with 30 calendar days written notice. Contract 11.3/11.5: termination per 44-FZ Art. 95 procedure with specific statutory grounds and EIS notification.",\n            "risk": "44-FZ termination procedure is more restrictive than template 30-day notice; Bank cannot terminate for convenience and must meet statutory grounds"\n        }]\n    },\n\n    # --- 10.3 Post-Termination Settlement ---\n    {\n        "contract_ids": ["11.1"],\n        "matrix_ids": ["10.3"],\n        "relationship": "deviation",\n        "status_reason": "Contract 11.1 — obligations survive until full performance; matrix 10.3 requires 18-month settlement period and specific payment mechanism via 5.1.3/5.1.4/Section 6",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "deadline",\n            "description": "Matrix 10.3: 18-month settlement period after Bank unilateral termination, with specific payment procedure. Contract 11.1: general survival clause without specified settlement period.",\n            "risk": "Without fixed 18-month settlement window, post-termination reconciliation could extend indefinitely or close prematurely"\n        }]\n    },\n\n    # --- 11.4 Written Amendments ---\n    {\n        "contract_ids": ["11.2"],\n        "matrix_ids": ["11.4"],\n        "relationship": "aligned",\n        "status_reason": "Contract 11.2 — changes/additions valid only if written and signed by both parties; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.5 Entire Agreement ---\n    {\n        "contract_ids": ["11.7"],\n        "matrix_ids": ["11.5"],\n        "relationship": "aligned",\n        "status_reason": "Contract 11.7 — parties governed by contract and RF legislation for matters not covered; prior agreements superseded; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.6 Copies ---\n    {\n        "contract_ids": ["12.4"],\n        "matrix_ids": ["11.6"],\n        "relationship": "aligned",\n        "status_reason": "Contract 12.4 — electronic form with UKEP replaces physical copies; 44-FZ electronic conclusion is the governing form; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.7 Appendices Integral ---\n    {\n        "contract_ids": ["1.1", "12.5"],\n        "matrix_ids": ["11.7"],\n        "relationship": "aligned",\n        "status_reason": "Contract 1.1 + 12.5 — appendices are integral parts; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.9 Assignment ---\n    {\n        "contract_ids": ["12.1", "12.2"],\n        "matrix_ids": ["11.9"],\n        "relationship": "aligned",\n        "status_reason": "Contract 12.1 — no Executor substitution except legal succession by reorganization; Contract 12.2 — Customer rights transfer to new Customer; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.10 Succession ---\n    {\n        "contract_ids": ["12.1", "12.2"],\n        "matrix_ids": ["11.10"],\n        "relationship": "aligned",\n        "status_reason": "Contract 12.1-12.2 — reorganization succession, liquidation claims per legislation; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.12 Notice Validity ---\n    {\n        "contract_ids": ["10.1"],\n        "matrix_ids": ["11.12"],\n        "relationship": "aligned",\n        "status_reason": "Contract 10.1 para 2 — notices and requests deemed properly sent if per contract communication channels; aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 11.13 Appendix List ---\n    {\n        "contract_ids": ["12.5"],\n        "matrix_ids": ["11.13"],\n        "relationship": "aligned",\n        "status_reason": "Contract 12.5 — list of appendices (Technical Assignment, Specification, Application Form, TST Info); aligned",\n        "risk_level": "none",\n        "discrepancies": []\n    },\n\n    # --- 4.1.1 Card reference right (partial: card aspect only in 5.4.5) ---\n    {\n        "contract_ids": ["5.4.5"],\n        "matrix_ids": ["4.1.1"],\n        "relationship": "deviation",\n        "status_reason": "Contract 5.4.5: Customer right to reference card payment in own materials with Bank pre-approval; matrix 4.1.1 also covers QR-code reference; QR aspect out of scope",\n        "risk_level": "low",\n        "discrepancies": [{\n            "type": "scope",\n            "description": "Matrix 4.1.1 covers referencing both card and QR payment in Customer materials with Bank approval through 2.3.1/2.3.2 channels. Contract 5.4.5 covers cards only; QR aspect is absent.",\n            "risk": "Low risk given no active QR product in contract; card-only approval right is preserved"\n        }]\n    },\n]\n\n# ============================================================\n# UNMATCHED MATRIX (missing_in_contract)\n# ============================================================\n\nunmatched_matrix = []\n\ndef add_missing(mid, req, req_type, risk_level, risk):\n    unmatched_matrix.append({\n        "matrix_id": mid,\n        "status": "missing_in_contract",\n        "requirement": req,\n        "required_type": req_type,\n        "risk_level": risk_level,\n        "risk": risk\n    })\n\nadd_missing("2.6.2.1", "QR-API mechanism for own KKT software: Bank provides QR-API for dynamic QR code generation via API", "mandatory", "low",\n    "Contract mentions QR display capability on terminals but does not create active QR-API product. Without QR-API, Bank cannot provide QR acquiring service through Customer\'s own KKT software. Low risk as Customer may not need QR-API if not using own KKT with QR.")\n\nadd_missing("2.6.2.2", "QR-Vendor mechanism: when Customer lacks own QR-capable software, Bank transfers QR parameters via QR-Vendor through separate Vendor contract", "mandatory", "low",\n    "No QR-Vendor integration established. Low risk given Customer uses Bank-provided terminals, not own KKT software requiring Vendor integration.")\n\nadd_missing("2.6.3.1", "QR auto-connection on Bank electronic terminal installation at TST", "mandatory", "low",\n    "QR display capability mentioned in Technical Assignment but no active QR product mechanism. QR code cannot be used for payment without active product configuration. Low risk as core service is card acquiring.")\n\nadd_missing("2.6.3.2", "QR deactivation procedure on merchant initiative via Bank notification through specified channels", "mandatory", "low",\n    "No active QR product to deactivate. Low risk.")\n\nadd_missing("4.2.2", "Customer duty to comply with Bank instructive/ informational materials provided by Bank", "optional", "low",\n    "Contract 5.10 covers self-training only, not an affirmative duty to comply with Bank instructions. Low risk as operational procedures are covered by other clauses.")\n\nadd_missing("4.2.8", "Customer duty to provide full range of goods/services at prices not exceeding cash prices (no card surcharge)", "mandatory", "medium",\n    "No anti-surcharge provision. Customer could charge higher prices for card payments, discouraging card use and reducing acquiring volumes. Medium risk for Bank\'s transaction revenue.")\n\nadd_missing("4.2.12", "Customer duty to accept Bank payment claims/invoices within 5 working days of issuance", "optional", "low",\n    "EIS acceptance replaces this mechanism; 44-FZ mandatory acceptance route provides alternative enforceable procedure. Low risk.")\n\nadd_missing("4.2.16.2", "Customer guarantee of employee (non-director) PDn consent: full name, mobile, email, position, workplace; with transfer to service companies", "mandatory", "medium",\n    "Contract only covers director PDn (5.3.20). Employee PDn needed for terminal servicing and support is not addressed. Bank and service companies process employee data without documented consent framework. Medium risk due to 152-FZ exposure.")\n\nadd_missing("4.2.22", "Customer duty to provide QR code to buyer for SberPayQR/Plati QR payment", "optional", "low",\n    "No active QR product. Low risk.")\n\nadd_missing("4.2.23", "Customer duty not to unilaterally change partner QR code", "optional", "low",\n    "No active QR product. Low risk.")\n\nadd_missing("4.2.24", "Customer duty to use API within QR-API functional boundaries and description on Bank official website", "optional", "low",\n    "No active QR-API product. Low risk.")\n\nadd_missing("4.2.25", "Customer duty to immediately suspend API use and notify Bank on QR-API security breach detection", "optional", "low",\n    "No active QR-API product. Low risk.")\n\nadd_missing("5.1.2", "Bank right to suspend authorization when Customer has debt until full repayment", "mandatory", "medium",\n    "Contract 5.2.9 lists specific suspension/termination grounds but does not include general debt-based authorization suspension. Bank cannot quickly stop transaction flow for delinquent Customers. Medium risk for credit exposure.")\n\nadd_missing("5.1.5", "Bank right not to reimburse Customer for operations conducted in violation of contract terms", "mandatory", "medium",\n    "Without explicit non-reimbursement right, Customer may claim payment for non-compliant operations. Bank\'s withholding rights (5.2.10) partially mitigate but do not create the same standalone protection. Medium risk.")\n\nadd_missing("5.1.7", "Bank right to transmit fraud/suspicious operation data including director PDn to Mir payment system regardless of contract term", "mandatory", "medium",\n    "PDn transfer to Mir is only covered in 5.3.20 for service provision purposes, not for independent fraud reporting. Bank needs this right to comply with payment system fraud monitoring obligations. Medium risk for regulatory compliance.")\n\nadd_missing("5.1.9", "Bank right to conduct additional operation checks including contacting issuer bank for legitimacy verification", "mandatory", "medium",\n    "Contract allows document requests (5.2.5) but not issuer-bank verification. This limits Bank\'s fraud investigation toolkit. Medium risk for fraud management.")\n\nadd_missing("5.1.12", "Bank right to unilaterally amend referenced documents by publication on official website with 1 calendar day notice", "optional", "low",\n    "Contract 11.2 requires bilateral written amendments. Bank cannot quickly update operational procedures/ tariffs. 44-FZ restricts unilateral changes. Low risk given 44-FZ mandatory constraints.")\n\nadd_missing("5.1.13", "Bank right to notify of own rekvizit changes via official website publication", "optional", "low",\n    "Contract 5.2.6 requires written notification within 3 working days. Different channel but same practical effect. Low risk.")\n\nadd_missing("5.1.15", "Bank right to refuse contract conclusion without explanation", "optional", "low",\n    "44-FZ procurement rules make this right practically inapplicable — Bank enters contract as winner of competitive procurement. Low risk given regulatory context.")\n\nadd_missing("5.1.17.1", "Bank right to unilaterally terminate and demand terminal return if POS terminal turnover below 40 000 RUB/month (80 000 for Moscow/SPb)", "optional", "low",\n    "No turnover threshold termination right. Bank cannot exit unprofitable terminal deployments. Low risk given fixed-term 44-FZ contract with defined price cap.")\n\nadd_missing("5.2.9", "Bank duty to provide QR code to merchant in electronic or paper form", "optional", "low",\n    "No active QR product. Low risk.")\n\nadd_missing("7.8", "Bank exemption from liability for disputes between Customer and Buyer not related to contract subject or for card-paid goods/services", "optional", "medium",\n    "Without this exemption, Bank could be drawn into Customer-Buyer disputes. Customer or Buyer might claim Bank liability for transaction-related issues. Medium risk for litigation exposure.")\n\nadd_missing("7.9", "Bank exemption from liability for fund transfer delays not caused by Bank", "optional", "medium",\n    "Bank could be held liable for delays caused by payment system, intermediary banks, or technical infrastructure outside Bank control. Medium risk.")\n\nadd_missing("7.10", "Bank exemption from liability for third-party actions/inactions including payment system participants", "optional", "medium",\n    "Without this, Bank bears liability for payment system/third-party failures. Medium risk given Bank\'s limited control over payment system infrastructure.")\n\nadd_missing("7.11", "Bank exemption from liability for delayed transfer during Bank investigation of suspected violation", "optional", "low",\n    "Bank may face conflicting obligations: investigate suspicious operations vs meet transfer deadlines. Low risk as withholding rights partially mitigate.")\n\nadd_missing("7.12", "Bank exemption from liability for exceeding contract price", "optional", "low",\n    "Contract price cap provides structural protection; this exemption clarifies Bank non-liability. Low risk.")\n\nadd_missing("7.14", "Customer liability for all actions in SPEP (payment acceptance system)", "mandatory", "low",\n    "SPEP not applicable to trade_acquiring (relevant for internet acquiring). Low risk for this contract profile.")\n\nadd_missing("7.15", "Customer full liability for personnel actions violating contract/Bank instructions", "mandatory", "medium",\n    "Without explicit personnel liability, Customer could argue it is not responsible for employee misconduct. Bank could face uncompensated losses from employee-caused violations. Medium risk.")\n\nadd_missing("7.17", "Customer full financial liability for recurring payments non-compliance with legislation/Bank of Russia regulations/payment system rules/contract", "mandatory", "low",\n    "Recurring payments not present in this trade_acquiring contract. Low risk for this profile.")\n\nadd_missing("11.1", "Payment system rules prevail over contract if consistent with RF law; conflicting contract terms must be aligned with payment system rules", "optional", "medium",\n    "Without this hierarchy clause, contract terms could conflict with payment system rules. Bank could face compliance violations or payment system penalties. Medium risk.")\n\nadd_missing("11.2", "Confidentiality of card numbers, payment account numbers, buyer PDn, operation amounts, payment info; prohibition on third-party transfer except as required by law/contract", "optional", "medium",\n    "No comprehensive confidentiality clause protecting payment data. Customer could disclose sensitive payment information. Medium risk for data security and PCI DSS compliance.")\n\nadd_missing("11.3", "Non-disclosure of card security elements, operation technology, financial/management info of parties; disclosure only with both parties\' consent", "optional", "low",\n    "No mutual non-disclosure of technical and financial information. Low risk given general confidentiality obligations under RF law.")\n\nadd_missing("11.8", "Customer warranty that goods/services sales in TST comply with RF legislation", "optional", "low",\n    "No explicit compliance warranty. Low risk as compliance with law is generally implied.")\n\nadd_missing("11.11", "Bank instructive materials posted on official website become binding next working day after posting", "optional", "medium",\n    "Without this provision, Bank cannot unilaterally update operational procedures. Contract 11.2 requires bilateral written amendments. 44-FZ constraints apply. Medium risk for operational flexibility.")\n\n# ============================================================\n# UNMATCHED CONTRACT (extra_in_contract)\n# ============================================================\n\nunmatched_contract = []\n\ndef add_extra(cid, pos, risk_level, risk, reason):\n    unmatched_contract.append({\n        "contract_id": cid,\n        "status": "extra_in_contract",\n        "contract_position": pos,\n        "risk_level": risk_level,\n        "risk": risk,\n        "materiality_reason": reason\n    })\n\nadd_extra("5.3.3", "Заказчик обязуется осуществлять контроль за ходом оказания услуг Исполнителем",\n    "low", "Customer monitoring right over Bank service delivery progress; no matrix analogue for this affirmative Customer oversight right",\n    "Creates an independent Customer right to monitor Bank\'s service delivery, which could be used for intrusive oversight or as basis for claims")\n\nadd_extra("5.3.4", "Заказчик обязуется принять решение об одностороннем отказе от исполнения контракта если Исполнитель не соответствует требованиям закупки или предоставил недостоверную информацию",\n    "medium", "Mandatory Customer duty to terminate if Bank fails procurement eligibility; creates Customer termination right beyond standard contract grounds",\n    "44-FZ statutory duty forcing Customer to terminate if Bank\'s procurement eligibility lapses; could force contract termination for purely formal/procedural reasons unrelated to service quality")\n\nadd_extra("5.3.5", "Заказчик обязуется требовать уплаты неустоек (штрафов, пеней) в случае просрочки или иного неисполнения Исполнителем обязательств",\n    "low", "Mandatory Customer duty to demand penalties from Bank for any breach; 44-FZ requirement without matrix analogue",\n    "Creates affirmative Customer obligation to pursue penalties; could generate additional claims against Bank even for minor issues")\n\nadd_extra("5.3.6", "Заказчик обязуется уменьшить сумму оплаты на размер налогов, сборов и иных обязательных платежей, связанных с оплатой контракта",\n    "medium", "Customer duty to reduce payment by tax amounts; 44-FZ tax withholding mechanism allows unilateral payment reduction",\n    "Customer can unilaterally deduct taxes from Bank payments; reduces Bank\'s receivable without consent or verification mechanism")\n\nadd_extra("5.4.2", "Заказчик вправе отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества",\n    "medium", "Customer right to refuse acceptance of services for inadequate quality; broad refusal right without objective criteria",\n    "Unqualified acceptance refusal right could be used to delay or deny payment; no matrix analogue for this broad Customer remedy")\n\nadd_extra("5.4.3", "Заказчик вправе принять решение об одностороннем отказе от исполнения контракта по основаниям 44-ФЗ и ГК РФ",\n    "medium", "Customer unilateral termination right under 44-FZ and Civil Code; independent of Bank termination rights",\n    "Customer can terminate for statutory grounds; creates counterparty risk for Bank\'s service continuity and terminal investment recovery")\n\nadd_extra("5.4.4", "Заказчик вправе отказаться от оплаты услуг ненадлежащего качества, потребовать возврата уплаченных сумм и возмещения убытков",\n    "high", "Customer right to refuse payment, demand refund, and claim damages for poor quality services; broad cumulative remedies",\n    "Triple remedy (non-payment + refund + damages) for quality claims without defined quality standards; significant financial exposure for Bank")\n\nadd_extra("7.8", "Обмен документами при применении мер ответственности осуществляется с использованием ЕИС путем направления электронных уведомлений с УКЭП",\n    "low", "Mandatory EIS channel for penalty-related document exchange; 44-FZ procedural requirement",\n    "Restricts penalty communication to EIS channel; low risk as this is standard 44-FZ procedure providing audit trail")\n\nadd_extra("7.9", "Применение неустойки не освобождает Стороны от исполнения обязательств по Контракту",\n    "low", "Penalty payment does not release parties from performance; standard cumulative remedy provision",\n    "Standard provision preserving performance obligation alongside penalties; low incremental risk")\n\nadd_extra("7.12", "В случае расторжения Контракта в связи с односторонним отказом, другая Сторона вправе потребовать возмещения фактически понесенного ущерба сверх начисленных неустоек",\n    "medium", "Post-termination actual damages claim beyond accrued penalties; expands Bank\'s liability exposure",\n    "Allows Customer to claim actual damages beyond contractual penalties after unilateral termination; uncapped liability exposure for Bank")\n\nadd_extra("8.2", "Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг его специалистами",\n    "medium", "Bank liability for damages caused by Bank specialists during service delivery; no matrix analogue for this specific liability channel",\n    "Creates additional liability channel for Bank beyond general contract liability; covers \'damages\' without limitation or causation standard")\n\nadd_extra("8.5.5", "Для проверки оказанных услуг в части их соответствия условиям Контракта Заказчик проводит экспертизу",\n    "low", "Mandatory Customer expert review of services for contract compliance; 44-FZ requirement",\n    "Customer must conduct expert review; could generate additional scrutiny and challenge to Bank service quality")\n\nadd_extra("8.5.6", "Экспертиза может проводиться Заказчиком своими силами или с привлечением экспертов, экспертных организаций",\n    "low", "Customer may engage external experts for service review; 44-FZ procedural right",\n    "External experts add cost and adversarial dimension to acceptance; low risk for Bank with proper documentation")\n\nadd_extra("8.5.8", "Приемочная комиссия: члены подписывают решение или мотивированный отказ; Заказчик подписывает итоговый документ",\n    "low", "Acceptance commission procedure with multiple signatories; 44-FZ acceptance formalization",\n    "Multi-level acceptance with commission review; procedural complexity but standard 44-FZ mechanism")\n\nadd_extra("8.5.9", "При получении мотивированного отказа Исполнитель вправе устранить причины и направить исправленный документ о приемке",\n    "low", "Bank right to cure defects and resubmit acceptance document after motivated refusal",\n    "Beneficial to Bank — provides correction opportunity; low risk")\n\nadd_extra("8.6", "Датой приемки оказанных услуг считается дата размещения в ЕИС документа о приемке, подписанного Заказчиком",\n    "low", "Acceptance date defined as EIS posting date of Customer-signed document; 44-FZ rule",\n    "Acceptance date tied to EIS posting; provides clear trigger for payment timeline")\n\nadd_extra("8.7", "Внесение исправлений в документ о приемке осуществляется путем формирования и подписания исправленного документа в ЕИС",\n    "low", "Correction procedure for acceptance documents via EIS; 44-FZ procedural rule",\n    "Formal correction mechanism; low risk procedural provision")\n\nadd_extra("8.9", "Заказчик вправе не отказывать в приемке если выявленное несоответствие не препятствует приемке и устранено Исполнителем",\n    "low", "Customer discretion to accept services despite non-conformity if cured; 44-FZ acceptance flexibility",\n    "Beneficial to Bank — allows acceptance despite minor non-conformities; low risk")\n\nadd_extra("8.10", "В случае оказания услуг ненадлежащего качества Исполнитель обязан безвозмездно устранить недостатки в течение 3 дней",\n    "medium", "Bank duty to cure quality defects within 3 days at no cost; short cure period without materiality threshold",\n    "3-day cure period is very short for terminal-related issues at remote locations (mountain reserves); could be impossible to meet for hardware replacement at distant TSTs")\n\nadd_extra("9.3", "Сторона, ссылающаяся на обстоятельства непреодолимой силы, обязана представить документальное подтверждение их наступления от уполномоченного лица",\n    "low", "Force majeure documentary proof requirement from authorized body; evidence burden",\n    "Additional evidence burden for force majeure claims; standard provision but requires third-party documentation")\n\nadd_extra("11.6", "Изменение и(или) расторжение контракта осуществляется в порядке, сроки, случаях и на условиях, установленных статьями 34, 95, 96, 112 44-ФЗ",\n    "low", "44-FZ statutory framework for contract modification/termination; mandatory law reference",\n    "Incorporates 44-FZ constraints on amendments; low risk as mandatory law anyway")\n\nadd_extra("11.8", "Изменение существенных условий контракта при его исполнении не допускается, за исключением случаев, предусмотренных 44-ФЗ",\n    "medium", "Prohibition on material contract term changes except per 44-FZ; limits Bank\'s ability to adjust commercial terms",\n    "Freezes material terms for contract duration; Bank cannot adjust fees, service scope, or operational procedures even if business conditions change")\n\nadd_extra("12.3", "Допускается оказание услуги с улучшенными характеристиками по сравнению с указанными в контракте по согласованию Сторон",\n    "low", "Permits improved service characteristics by mutual agreement; 44-FZ flexibility provision",\n    "Beneficial flexibility; allows service improvements without formal amendment")\n\nadd_extra("4.5.1", "Услуги, оказанные в ноябре оплачиваются в срок не позднее 7 рабочих дней с даты подписания документа о приемке, но не позднее 30 декабря 2025 года",\n    "low", "Specific November payment deadline with 30 December hard stop; budget-year constraint",\n    "Annual budget cycle payment constraint; standard for 44-FZ, ensures year-end settlement")\n\nadd_extra("4.2", "Исполнитель должен иметь лицензию на осуществление банковских операций",\n    "low", "Bank must hold banking license; statutory requirement incorporated in contract",\n    "Restates statutory licensing requirement; low risk")\n\nadd_extra("8.3.2", "К документу о приемке прилагаются счет-фактура, акт о перечислении сумм операций и счет ф.363; при расхождении приоритет имеет информация в документе о приемке",\n    "low", "Supporting documents hierarchy: EIS acceptance document prevails over attached invoice/act in case of discrepancies",\n    "Establishes documentary priority rule; potentially beneficial to Bank as EIS document controls")\n\nadd_extra("8.5.2", "По письменному уведомлению Исполнителя приемка может производиться только в присутствии представителя Исполнителя",\n    "low", "Bank right to participate in acceptance via representative with documented authority; 15 working days advance notice required",\n    "Beneficial to Bank — ensures presence at acceptance; but 15-day notice requirement is administratively burdensome")\n\nadd_extra("8.5.3", "В случае поступления уведомления об участии в приемке в срок, приемка производится только в двустороннем порядке",\n    "low", "Bilateral acceptance mandatory if Bank timely notifies participation; prevents unilateral Customer acceptance",\n    "Protects Bank by requiring bilateral acceptance when Bank elects to participate")\n\nadd_extra("8.5.4", "Если уведомление об участии в приемке не поступило либо поступило с опозданием, приемка производится Заказчиком в одностороннем порядке",\n    "low", "Unilateral Customer acceptance if Bank fails to timely notify participation",\n    "Risk if Bank misses 15-day notice deadline; low risk with proper internal processes")\n]\n\n# ============================================================\n# CONTRACT COVERAGE LEDGER\n# ============================================================\n# List all material contract locators and their closure\n\ncontract_ledger = []\n\ndef add_contract(cid, closure, reason):\n    contract_ledger.append({"contract_id": cid, "closure": closure, "reason": reason})\n\n# Chapeau/heading\nadd_contract("1", "not_material", "Heading: предмет контракта — covered by children")\nadd_contract("1.1", "linked", "Subject: Bank provides acquiring services, Customer pays; incorporated in links for 2.4, 3.3, 11.7")\nadd_contract("1.2", "linked", "Service volume determined by Customer need within max price; linked via 6.21/3.3 package")\nadd_contract("1.3", "linked", "Customer organizes card acceptance; linked via 3.1")\n\nadd_contract("2", "not_material", "Heading: термины и определения — no operative effect")\nadd_contract("2.1", "not_material", "Definition: авторизация")\nadd_contract("2.1.1", "not_material", "Definition: банковская карта")\nadd_contract("2.1.2", "not_material", "Definition: банк-эквайрер")\nadd_contract("2.1.3", "not_material", "Definition: банк-эмитент")\nadd_contract("2.1.4", "not_material", "Definition: возврат платежа")\nadd_contract("2.1.5", "not_material", "Definition: держатель карты")\nadd_contract("2.1.6", "not_material", "Definition: документ по операции")\nadd_contract("2.1.7", "not_material", "Definition: код авторизации")\nadd_contract("2.1.8", "not_material", "Definition: ККТ")\nadd_contract("2.1.9", "not_material", "Definition: контрольная лента")\nadd_contract("2.1.10", "not_material", "Definition: отложенный платеж")\nadd_contract("2.1.11", "not_material", "Definition: операция")\nadd_contract("2.1.12", "not_material", "Definition: операция оплаты")\nadd_contract("2.1.13", "not_material", "Definition: операция отмены")\nadd_contract("2.1.14", "not_material", "Definition: операция возврата")\nadd_contract("2.1.15", "not_material", "Definition: платежная система")\nadd_contract("2.1.16", "not_material", "Definition: покупатель")\nadd_contract("2.1.17", "not_material", "Definition: повторяющиеся платежи")\nadd_contract("2.1.18", "not_material", "Definition: предавторизация")\nadd_contract("2.1.19", "not_material", "Definition: предприятие (Заказчик)")\nadd_contract("2.1.20", "not_material", "Definition: рабочий день")\nadd_contract("2.1.21", "not_material", "Definition: реверсивная транзакция")\nadd_contract("2.1.22", "not_material", "Definition: сводный чек")\nadd_contract("2.1.23", "not_material", "Definition: тарифы банка")\nadd_contract("2.1.24", "not_material", "Definition: товар/услуга")\nadd_contract("2.1.25", "not_material", "Definition: ТСТ")\nadd_contract("2.1.26", "not_material", "Definition: торговый эквайринг")\nadd_contract("2.1.27", "not_material", "Definition: чек электронного терминала")\nadd_contract("2.1.28", "not_material", "Definition: электронная сверка итогов")\nadd_contract("2.2", "not_material", "Definition: электронный терминал — descriptive only")\nadd_contract("2.3", "linked", "Document exchange chapeau + receipt rules; linked via 2.3.7")\nadd_contract("2.3.1", "linked", "Email exchange; linked via 2.3.1")\nadd_contract("2.3.2", "linked", "DBO exchange; linked via 2.3.2")\nadd_contract("2.3.3", "linked", "Courier; linked via 2.3.3")\nadd_contract("2.3.4", "linked", "Registered mail; linked via 2.3.4")\nadd_contract("2.3.5", "linked", "E-invoicing with UKEP (blank system name); linked via 2.3.5")\nadd_contract("2.3.6", "linked", "EIS exchange; linked via 2.3.6")\nadd_contract("2.3.7", "linked", "Support service; linked via 2.3.7")\n\nadd_contract("3", "not_material", "Heading: цена контракта")\nadd_contract("3.1", "linked", "Max contract price 1 900 000 RUB; linked via 6.21")\nadd_contract("3.1.1", "linked", "Unit price in Specification; linked via 6.1")\nadd_contract("3.2", "linked", "Unit price includes Bank settlement fee as % of each operation; linked via 3.3, 4.2.1, 6.1")\nadd_contract("3.3", "not_material", "44-FZ reference for price application; no independent operative effect")\n\nadd_contract("4", "not_material", "Heading: сроки, условия, порядок оплаты")\nadd_contract("4.1", "linked", "Service period 01.03.2025-30.11.2025 or price exhaustion; linked via 10.1")\nadd_contract("4.2", "extra_in_contract", "Bank must hold banking license; reported as extra")\nadd_contract("4.3", "linked", "TST registration + terminal installation locations; linked via 2.1")\nadd_contract("4.4", "linked", "Payment procedure, Bank account details; linked via 5.1.4, 2.2")\nadd_contract("4.5", "linked", "Payment within 7 working days of acceptance; linked via 6.5")\nadd_contract("4.5.1", "extra_in_contract", "November payment deadline 30 Dec 2025; reported as extra")\n\nadd_contract("5", "not_material", "Heading: обязательства сторон")\nadd_contract("5.1", "not_material", "Heading: Исполнитель обязуется")\nadd_contract("5.1.1", "linked", "Terminal installation within 5 days + instruction + training materials; linked via 5.2.3, 5.2.5")\nadd_contract("5.1.2", "linked", "Monthly acceptance document via EIS; linked via 6.2")\nadd_contract("5.1.3", "linked", "Service compliance with RF legislation; linked via 7.1")\nadd_contract("5.1.4", "linked", "24/7 terminal operability, replacement within 3 working days; linked via 5.2.7")\nadd_contract("5.1.5", "linked", "Provide full and accurate service info; linked via 5.1.16 context")\nadd_contract("5.1.6", "linked", "24/7 authorization; linked via 5.2.4")\nadd_contract("5.1.7", "linked", "Terminals with informational materials; linked via 5.2.6")\nadd_contract("5.1.8", "linked", "Transfer operation sums within 2 working days; linked via 5.2.8")\nadd_contract("5.1.9", "linked", "PDn processing per 152-FZ; linked via 5.2.10")\nadd_contract("5.1.10", "linked", "Transfer operation sums to Customer; linked via 3.2")\n\nadd_contract("5.2", "not_material", "Heading: Исполнитель вправе")\nadd_contract("5.2.1", "linked", "Demand timely payment/acceptance; linked via 4.2.1")\nadd_contract("5.2.2", "linked", "Unilateral termination per 44-FZ/GK RF; linked via 10.2")\nadd_contract("5.2.3", "linked", "Inspect terminals, replace with 2 days notice; linked via 5.1.6, 5.1.10")\nadd_contract("5.2.4", "linked", "Remote software update without changing operations; linked via 5.1.6")\nadd_contract("5.2.5", "linked", "Request operation documents within 13 months; linked via 5.1.11")\nadd_contract("5.2.6", "linked", "Notify of rekvizit changes in writing within 3 working days; linked via 5.1.13 deviation")\nadd_contract("5.2.7", "linked", "Send operation-info requests to Customer email; linked via 5.1.14")\nadd_contract("5.2.8", "linked", "Demand documents/info for statutory functions; linked via 5.1.16")\nadd_contract("5.2.9", "linked", "Unilateral auth suspension/termination chapeau; linked via 5.1.8.1-5.1.8.13")\nadd_contract("5.2.9.1", "linked", "Customer breach ground; linked via 5.1.8.1")\nadd_contract("5.2.9.2", "linked", "Extremism/terrorism listing ground; linked via 5.1.8.2")\nadd_contract("5.2.9.3", "linked", "AML/CFT suspicion ground; linked via 5.1.8.3")\nadd_contract("5.2.9.4", "linked", "Negative government/payment system info ground; linked via 5.1.8.6")\nadd_contract("5.2.9.5", "linked", "Fraud info ground; linked via 5.1.8.7")\nadd_contract("5.2.9.6", "linked", "TST renovation ground; linked via 5.1.8.8")\nadd_contract("5.2.9.7", "linked", "Liquidation/bankruptcy ground; linked via 5.1.8.9")\nadd_contract("5.2.9.8", "linked", "False info ground; linked via 5.1.8.10")\nadd_contract("5.2.9.9", "linked", "Activity mismatch ground; linked via 5.1.8.11")\nadd_contract("5.2.9.10", "linked", "30-day inactivity ground; linked via 5.1.8.12")\nadd_contract("5.2.9.11", "linked", "Price exhaustion/term expiry ground; linked via 5.1.8.13")\nadd_contract("5.2.10", "linked", "Withholding right chapeau; linked via 5.1.1.1-5.1.1.6, 5.1.3")\nadd_contract("5.2.10.1", "linked", "Invalid operations withholding grounds; linked via 5.1.1.1")\nadd_contract("5.2.10.2", "linked", "Erroneous transfer withholding; linked via 5.1.1.2")\nadd_contract("5.2.10.3", "linked", "Return/chargeback/reversal withholding; linked via 5.1.1.3")\nadd_contract("5.2.10.4", "linked", "Disputed operations withholding; linked via 5.1.1.4")\nadd_contract("5.2.10.5", "linked", "Penalty/loss withholding; linked via 5.1.1.5")\n\nadd_contract("5.3", "not_material", "Heading: Заказчик обязуется")\nadd_contract("5.3.1", "linked", "Accept services per acceptance document; linked via 6.4")\nadd_contract("5.3.2", "linked", "Pay for services per contract; linked via 4.2.1")\nadd_contract("5.3.3", "extra_in_contract", "Customer control over Bank service delivery; reported as extra")\nadd_contract("5.3.4", "extra_in_contract", "Customer duty to terminate if Bank fails procurement requirements; reported as extra")\nadd_contract("5.3.5", "extra_in_contract", "Customer duty to demand penalties from Bank; reported as extra")\nadd_contract("5.3.6", "extra_in_contract", "Customer duty to reduce payment by tax amounts; reported as extra")\nadd_contract("5.3.7", "linked", "Place Bank informational materials at TST; linked via 4.2.4")\nadd_contract("5.3.8", "linked", "No splitting one operation into multiple sums; linked via 4.2.6")\nadd_contract("5.3.9", "linked", "No use of card details for other purposes; linked via 4.2.7")\nadd_contract("5.3.10", "linked", "Conduct operations and prepare documents correctly; linked via 4.2.9")\nadd_contract("5.3.11", "linked", "Store documents 13+ months, provide copies in 3 working days; linked via 4.2.10")\nadd_contract("5.3.12", "linked", "Provide written statement of operation circumstances; linked via 4.2.11")\nadd_contract("5.3.13", "linked", "Notify Bank of changes within 3 working days; linked via 4.2.14")\nadd_contract("5.3.14", "linked", "Provide reliable docs/info annually and within 7 working days; linked via 4.2.15")\nadd_contract("5.3.15", "linked", "Provide PDn transfer proof, indemnify Bank; linked via 4.2.16.3")\nadd_contract("5.3.16", "linked", "Cease card acceptance, remove materials post-termination; linked via 4.2.18")\nadd_contract("5.3.17", "linked", "Not obstruct Bank checks, assist investigations; linked via 4.2.19")\nadd_contract("5.3.18", "not_material", "Chapeau: при осуществлении операций в ТСТ (торговый эквайринг)")\nadd_contract("5.3.18.1", "linked", "Terminal use restrictions; linked via 4.2.20.2")\nadd_contract("5.3.18.2", "linked", "Access for terminal service; linked via 4.2.20.3")\nadd_contract("5.3.18.3", "linked", "Terminal acceptance act; linked via 4.2.20.4")\nadd_contract("5.3.20.4", "linked", "Immediate notice of malfunction/loss; linked via 4.2.20.5")\nadd_contract("5.3.18.5", "linked", "Return terminals within 5 working days; linked via 4.2.20.6")\nadd_contract("5.3.19", "linked", "Reimburse Bank for disputed/invalid operations and losses; linked via 4.2.13")\nadd_contract("5.3.20", "linked", "Transfer director PDn with guarantees; linked via 4.2.16.1")\n\nadd_contract("5.4", "not_material", "Heading: Заказчик вправе")\nadd_contract("5.4.1", "linked", "Demand proper performance per contract/law; linked via 7.1")\nadd_contract("5.4.2", "extra_in_contract", "Refuse acceptance for inadequate quality; reported as extra")\nadd_contract("5.4.3", "extra_in_contract", "Unilateral termination per 44-FZ/GK RF; reported as extra")\nadd_contract("5.4.4", "extra_in_contract", "Refuse payment, demand refund and damages; reported as extra")\nadd_contract("5.4.5", "linked", "Reference card payment in materials with Bank approval; linked via 4.1.1")\n\nadd_contract("5.5", "linked", "Provide written statement within 3 working days, notify of document loss; linked via 4.2.11")\nadd_contract("5.6", "linked", "Return terminals within 5 working days of termination/demand; linked via 4.2.20.6")\nadd_contract("5.7", "linked", "Penalty for terminal non-return: 10 000/25 000 RUB; linked via 4.2.20.7, 5.1.1.6")\nadd_contract("5.9", "linked", "Consultation right via support service; linked via 4.1.2")\nadd_contract("5.10", "linked", "Employee self-training on operations; linked via 4.2.20.1")\n\nadd_contract("6", "not_material", "Heading: антикоррупционная оговорка")\nadd_contract("6.1", "linked", "Anti-corruption clause; linked via 7.16")\n\nadd_contract("7", "not_material", "Heading: ответственность сторон")\nadd_contract("7.1", "linked", "General liability + force majeure exemption + штраф cap; linked via 7.1, 7.3")\nadd_contract("7.2", "linked", "Bank right to demand Customer penalties; linked via 7.2")\nadd_contract("7.3", "linked", "Customer delay penalty 1/300 key rate; linked via 7.4")\nadd_contract("7.4", "linked", "Customer штраф (non-delay) per PP 1042; linked via 7.2")\nadd_contract("7.4.1", "linked", "Customer штраф brackets; linked via 7.2")\nadd_contract("7.5", "linked", "Customer right to demand Bank penalties; linked via 7.4")\nadd_contract("7.6", "linked", "Bank delay penalty 1/300 key rate; linked via 7.4")\nadd_contract("7.7", "linked", "Bank штраф (non-delay) chapeau; linked via 7.5")\nadd_contract("7.7.1", "linked", "Bank штраф brackets; linked via 7.5")\nadd_contract("7.7.2", "linked", "Bank штраф for price-above-NMCK winner; linked via 7.5")\nadd_contract("7.7.3", "linked", "Bank штраф non-pecuniary; linked via 7.6")\nadd_contract("7.8", "extra_in_contract", "EIS channel for penalty documents; reported as extra")\nadd_contract("7.9", "extra_in_contract", "Penalty does not release from performance; reported as extra")\nadd_contract("7.10", "linked", "Total Bank штраф cap = contract price; linked via 7.7")\nadd_contract("7.11", "linked", "Total Customer штраф cap = contract price; linked via 7.3")\nadd_contract("7.12", "extra_in_contract", "Post-termination actual damages beyond penalties; reported as extra")\n\nadd_contract("8", "not_material", "Heading: качество, приемка, гарантия")\nadd_contract("8.1", "linked", "Quality guarantee per Technical Assignment; linked via 7.1")\nadd_contract("8.2", "extra_in_contract", "Bank liability for damages caused by specialists; reported as extra")\nadd_contract("8.3", "not_material", "Chapeau: приемка per legislation and contract")\nadd_contract("8.3.1", "linked", "Monthly EIS acceptance document by 10th working day; linked via 6.2")\nadd_contract("8.3.2", "extra_in_contract", "Supporting documents hierarchy rule; reported as extra")\nadd_contract("8.4", "linked", "Acceptance document receipt date = EIS posting date; linked via 6.4")\nadd_contract("8.5", "linked", "Acceptance procedure: 10 working days for Customer to sign or refuse; linked via 6.4")\nadd_contract("8.5.1", "linked", "Customer signs or motivated refusal within 10 working days; linked via 6.4")\nadd_contract("8.5.2", "extra_in_contract", "Bank representative participation in acceptance; reported as extra")\nadd_contract("8.5.3", "extra_in_contract", "Bilateral acceptance if Bank notifies timely; reported as extra")\nadd_contract("8.5.4", "extra_in_contract", "Unilateral acceptance if Bank does not notify; reported as extra")\nadd_contract("8.5.5", "extra_in_contract", "Mandatory Customer expert review; reported as extra")\nadd_contract("8.5.6", "extra_in_contract", "External expert engagement; reported as extra")\nadd_contract("8.5.7", "linked", "Customer signs acceptance within 10 working days if no objections; linked via 6.4")\nadd_contract("8.5.8", "extra_in_contract", "Acceptance commission procedure; reported as extra")\nadd_contract("8.5.9", "extra_in_contract", "Bank right to cure and resubmit after refusal; reported as extra")\nadd_contract("8.6", "extra_in_contract", "Acceptance date = EIS posting date of signed document; reported as extra")\nadd_contract("8.7", "extra_in_contract", "Correction procedure via EIS; reported as extra")\nadd_contract("8.8", "not_material", "Reference to acceptance procedure per this section; no independent effect")\nadd_contract("8.9", "extra_in_contract", "Customer may accept despite non-conformity if cured; reported as extra")\nadd_contract("8.10", "extra_in_contract", "Bank duty to cure defects within 3 days at no cost; reported as extra")\nadd_contract("8.11", "linked", "Signed acceptance document = basis for payment; linked via 6.4")\n\nadd_contract("9", "not_material", "Heading: действие обстоятельств непреодолимой силы")\nadd_contract("9.1", "linked", "Force majeure definition + examples; linked via 8.1")\nadd_contract("9.2", "linked", "Force majeure notice + termination after 1 month; linked via 8.2")\nadd_contract("9.3", "extra_in_contract", "Force majeure documentary proof requirement; reported as extra")\n\nadd_contract("10", "not_material", "Heading: порядок разрешения споров")\nadd_contract("10.1", "linked", "Pre-trial negotiations, 10-day claim response, notice delivery; linked via 9.1, 9.2, 11.12")\nadd_contract("10.2", "linked", "Arbitration Court of Krasnodar Krai; linked via 9.3")\n\nadd_contract("11", "not_material", "Heading: срок действия, изменение, расторжение")\nadd_contract("11.1", "linked", "Contract term to 30.12.2025 or price exhaustion; obligations survive; linked via 10.1, 10.3")\nadd_contract("11.2", "linked", "Written amendments signed by both parties; linked via 11.4")\nadd_contract("11.3", "linked", "Termination by agreement, court, or unilateral per GK RF; linked via 10.2")\nadd_contract("11.4", "linked", "Customer unilateral termination per GK RF; linked via 10.2")\nadd_contract("11.5", "linked", "Unilateral termination per 44-FZ Art. 95; linked via 10.2")\nadd_contract("11.6", "extra_in_contract", "44-FZ Arts. 34, 95, 96, 112 framework for changes/termination; reported as extra")\nadd_contract("11.7", "linked", "Matters not covered: RF legislation governs; linked via 11.5")\nadd_contract("11.8", "extra_in_contract", "No material term changes except per 44-FZ; reported as extra")\n\nadd_contract("12", "not_material", "Heading: прочие условия")\nadd_contract("12.1", "linked", "No Executor substitution except reorganization succession; linked via 11.9, 11.10")\nadd_contract("12.2", "linked", "Customer rights/obligations transfer to new Customer; linked via 11.9, 11.10")\nadd_contract("12.3", "extra_in_contract", "Improved service characteristics permitted by agreement; reported as extra")\nadd_contract("12.4", "linked", "Electronic form with UKEP; linked via 2.7, 11.6")\nadd_contract("12.5", "linked", "Appendix list; linked via 2.4, 11.7, 11.13")\n\nadd_contract("13", "not_material", "Реквизиты сторон — signatures and bank details")\nadd_contract("Technical Assignment", "linked", "Technical Assignment content incorporated via multiple links")\nadd_contract("Technical Assignment p.3", "linked", "Accepted card system list; linked via 3.1, 4.2.5")\nadd_contract("Technical Assignment p.5", "linked", "Settlement currency RUB + return fee rule; linked via 2.2, 6.20")\nadd_contract("Specification", "linked", "Price specification; linked via 3.3, 6.1")\nadd_contract("Приложение 1.1", "linked", "Customer application form + direct debit consent; linked via 5.1.3")\nadd_contract("Приложение 1.2", "not_material", "TST Info form — blank template, no operative terms")\nadd_contract("Приложение 2", "not_material", "Specification form — linked via Specification reference")\n\n# ============================================================\n# ASSEMBLE FINAL OUTPUT\n# ============================================================\n\noutput = {\n    "analysis_profile": {\n        "product": ["trade_acquiring"],\n        "legal_regime": "44_fz"\n    },\n    "links": links,\n    "unmatched_matrix": unmatched_matrix,\n    "unmatched_contract": unmatched_contract,\n    "coverage_ledger": {\n        "matrix": matrix_rows,\n        "contract": contract_ledger\n    },\n    "summary": {\n        "aligned_count": sum(1 for l in links if l["relationship"] == "aligned"),\n        "deviation_count": sum(1 for l in links if l["relationship"] == "deviation"),\n        "missing_in_contract_count": len(unmatched_matrix),\n        "extra_in_contract_count": len(unmatched_contract)\n    }\n}\n\nwith open("outputs/discrepancy_analysis.json", "w", encoding="utf-8") as f:\n    json.dump(output, f, ensure_ascii=False, indent=2)\n\nprint(f"Written outputs/discrepancy_analysis.json")\nprint(f"Links: {len(links)} total ({output[\'summary\'][\'aligned_count\']} aligned, {output[\'summary\'][\'deviation_count\']} deviation)")\nprint(f"Missing in contract: {output[\'summary\'][\'missing_in_contract_count\']}")\nprint(f"Extra in contract: {output[\'summary\'][\'extra_in_contract_count\']}")\nprint(f"Matrix ledger rows: {len(matrix_rows)}")\nprint(f"Contract ledger rows: {len(contract_ledger)}")\n', 'file_path': 'outputs/working/build_analysis.py'}, 'id': 'call_00_xwVF1f11L4G2KIs5Idn77746', 'type': 'tool_call'}]
Tool: Cannot write to /outputs/working/build_analysis.py because it already exists. Read and then make an edit, or write to a new path.
AI: [{'name': 'execute', 'args': {'command': 'rm outputs/working/build_analysis.py && python3 -c "print(\'deleted\')"'}, 'id': 'call_00_u4TJ4Vx9ZnY7q7817Oby7501', 'type': 'tool_call'}]
Tool: At C:\Users\gogel\OneDrive\Рабочий стол\Проекты\skillshot_manual_2\outputs\working\agent_execute_vp1xomqn.ps1:32 char:3
8
+ rm outputs/working/build_analysis.py && python3 -c "print('deleted')"
+                                      ~~
The token '&&' is not a valid statement separator in this version.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : InvalidEndOfLine
 

[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'del outputs\\working\\build_analysis.py'}, 'id': 'call_00_nzeYhr0Xxcm58e8E4N2p7269', 'type': 'tool_call'}]
Tool: 
[Command succeeded with exit code 0]
AI: [{'name': 'write_file', 'args': {'content': '#!/usr/bin/env python3\n"""Build the complete discrepancy_analysis.json for acquiring contract review."""\nimport json, os\n\n# Create working dir\nos.makedirs("outputs/working", exist_ok=True)\n\nprofile = {\n    "product": ["trade_acquiring"],\n    "legal_regime": "44_fz"\n}\n\n# ============================================================\n# MATRIX COVERAGE LEDGER — all 169 rows\n# ============================================================\nmatrix_rows = [\n    ("2.1", "linked", "Contract 4.3 requires TST registration application + info; Bank right to refuse without explanation is absent → deviation"),\n    ("2.2", "linked", "Contract 4.4 + Technical Assignment p.5 confirm settlement in RUB; aligned"),\n    ("2.3.1", "linked", "Contract 2.3.1 mirrors email exchange with full legal force; aligned"),\n    ("2.3.2", "linked", "Contract 2.3.2 mirrors DBO system exchange; aligned"),\n    ("2.3.3", "linked", "Contract 2.3.3 mirrors courier delivery; aligned"),\n    ("2.3.4", "linked", "Contract 2.3.4 mirrors registered mail; aligned"),\n    ("2.3.5", "linked", "Contract 2.3.5 analogue exists but automated system name is blank placeholder → deviation"),\n    ("2.3.6", "linked", "Contract 2.3.6 — EIS channel present and applicable for 44-FZ regime; aligned"),\n    ("2.3.7", "linked", "Contract 2.3.7 support service channel + receipt-date rules match matrix; aligned"),\n    ("2.4", "linked", "Contract 1.1 + 12.5 declare appendices integral parts of contract; aligned"),\n    ("2.5.1.1", "out_of_scope", "only_for_product=internet_acquiring; contract is trade_acquiring only, no internet acquiring"),\n    ("2.5.2.1", "out_of_scope", "payment_method=sber_pay_face_scan; no biometric/SberPay Face Scan product in contract"),\n    ("2.6.1.1", "out_of_scope", "only_for_terminal=smart; contract has POS terminals only, no smart terminals"),\n    ("2.6.2.1", "missing_in_contract", "QR-API mechanism absent; QR display capability on terminals (Technical Assignment) is not active QR product"),\n    ("2.6.2.2", "missing_in_contract", "QR-Vendor mechanism absent; no own KKT software requiring Vendor QR integration"),\n    ("2.6.3.1", "missing_in_contract", "QR auto-connect on Bank terminal absent; QR display capability ≠ QR product mechanism"),\n    ("2.6.3.2", "missing_in_contract", "QR disconnect by merchant initiative absent; no active QR product to disconnect"),\n    ("2.7", "linked", "Contract 12.4 — electronic form with UKEP, equal legal force to paper; aligned"),\n    ("3.1", "linked", "Contract 1.3 — Customer organizes card acceptance; Technical Assignment p.3 lists accepted card systems (MIR, VISA, MC); aligned"),\n    ("3.2", "linked", "Contract 5.1.10 + 5.1.8 — Bank duty to transfer operation sums to Customer; aligned"),\n    ("3.3", "linked", "Contract 3.2 + 4.4 + Specification — Customer pays Bank fee from each operation; aligned"),\n    ("4.1.1", "linked", "Contract 5.4.5 — card reference right with Bank approval; QR aspect absent (no active QR product) → deviation on scope"),\n    ("4.1.2", "linked", "Contract 5.9 — Customer right to consultation on terminal operation via support service; aligned"),\n    ("4.1.3", "out_of_scope", "payment_method=qr_sber_pay; no SberPay or active QR product in contract"),\n    ("4.2.1", "linked", "Contract 3.2 + 4.4 + Specification — Customer pays Bank for settlement services; aligned"),\n    ("4.2.2", "missing_in_contract", "No explicit duty for Customer to comply with Bank instructive materials; Contract 5.10 covers self-training only"),\n    ("4.2.3", "out_of_scope", "only_for_lot=fz_223; contract is 44-FZ regime"),\n    ("4.2.4", "linked", "Contract 5.3.7 — Customer duty to place Bank informational materials at TST; aligned"),\n    ("4.2.5", "linked", "Contract 5.3.8 + 5.3.9 + Technical Assignment p.3 — partial coverage; \'accept all cards all hours\', \'no cash\', \'max 2 cards\' absent → deviation"),\n    ("4.2.6", "linked", "Contract 5.3.8 — no splitting one operation into multiple sums; aligned"),\n    ("4.2.7", "linked", "Contract 5.3.9 — no use of card details for other purposes; aligned"),\n    ("4.2.8", "missing_in_contract", "No provision that card-payment prices do not exceed cash prices; absent from contract"),\n    ("4.2.9", "linked", "Contract 5.3.10 — Customer conducts operations and prepares documents per rules, bears responsibility; aligned"),\n    ("4.2.10", "linked", "Contract 5.3.11 — store documents 13+ months, provide copies within 3 working days, proper quality; aligned"),\n    ("4.2.11", "linked", "Contract 5.5 — provide written statement within 3 working days, immediate notice of document loss; aligned"),\n    ("4.2.12", "missing_in_contract", "No acceptance of Bank payment claims/invoices within 5 working days; EIS acceptance replaces but does not create same direct-debit mechanism for Bank fees"),\n    ("4.2.13", "linked", "Contract 5.3.19 — Customer reimburses Bank for disputed/invalid operations, chargeback fees, losses; lacks unconditional qualifier → deviation"),\n    ("4.2.14", "linked", "Contract 5.3.13 — notify Bank within 3 working days of changes; aligned"),\n    ("4.2.15", "linked", "Contract 5.3.14 — provide reliable docs/info annually and within 7 working days; aligned"),\n    ("4.2.16.1", "linked", "Contract 5.3.20 — director PDn transfer with guarantees, Mir consent; aligned"),\n    ("4.2.16.2", "missing_in_contract", "No employee (non-director) PDn consent provision; contract only covers director"),\n    ("4.2.16.3", "linked", "Contract 5.3.15 — proof of lawful PDn transfer + indemnity; response deadline absent → deviation"),\n    ("4.2.17", "out_of_scope", "only_for_product=internet_acquiring; contract is trade_acquiring only"),\n    ("4.2.18", "linked", "Contract 5.3.16 — cease card acceptance, remove materials post-termination; aligned"),\n    ("4.2.19", "linked", "Contract 5.3.17 — not obstruct Bank checks, assist fraud investigation; aligned"),\n    ("4.2.20.1", "linked", "Contract 5.10 — employee self-training on operations; website URL blank → deviation"),\n    ("4.2.20.2", "linked", "Contract 5.3.18.1 — terminal use restrictions; aligned"),\n    ("4.2.20.3", "linked", "Contract 5.3.18.2 — access for terminal service; aligned"),\n    ("4.2.20.4", "linked", "Contract 5.3.18.3 — terminal acceptance act; aligned"),\n    ("4.2.20.5", "linked", "Contract 5.3.20.4 — immediate notice of malfunction/loss; aligned"),\n    ("4.2.20.6", "linked", "Contract 5.3.18.5 + 5.6 — return terminals within 5 working days; aligned"),\n    ("4.2.20.7", "linked", "Contract 5.7 — штраф 10 000 RUB electronic, 25 000 RUB smart; matrix expects 25 000 both → deviation"),\n    ("4.2.21.1", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.2", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.3", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.4", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.5", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.6", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.7", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.21.8", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("4.2.22", "missing_in_contract", "No duty to provide QR code to buyer; payment_method=qr, no active QR product"),\n    ("4.2.23", "missing_in_contract", "No prohibition on unilateral QR code change; payment_method=qr, no active QR product"),\n    ("4.2.24", "missing_in_contract", "No API usage within QR-API boundaries; payment_method=qr, no active QR-API"),\n    ("4.2.25", "missing_in_contract", "No suspend API + notify Bank on QR-API breach; payment_method=qr, no active QR-API"),\n    ("4.2.26", "out_of_scope", "only_for_product=internet_acquiring; recurring payments in internet acquiring context"),\n    ("5.1.1.1", "linked", "Contract 5.2.10 + 5.2.10.1 — Bank right to withhold invalid operation amounts with 12 matching grounds; aligned"),\n    ("5.1.1.2", "linked", "Contract 5.2.10.2 — Bank right to withhold erroneously transferred sums; aligned"),\n    ("5.1.1.3", "linked", "Contract 5.2.10.3 — Bank right to withhold return/chargeback/reversal amounts; aligned"),\n    ("5.1.1.4", "linked", "Contract 5.2.10.4 — Bank right to withhold disputed/charged-back sums; aligned"),\n    ("5.1.1.5", "linked", "Contract 5.2.10.5 — Bank right to withhold штраф/loss from penalties; aligned"),\n    ("5.1.1.6", "linked", "Contract 5.2.10 with 5.7 — Bank can withhold штраф for terminal non-return; aligned"),\n    ("5.1.2", "missing_in_contract", "No Bank right to suspend authorization for Customer debt until full repayment"),\n    ("5.1.3", "linked", "Contract 5.2.10 + App 1.1 p.3 (direct debit consent) — Bank right to direct debit; aligned"),\n    ("5.1.4", "linked", "Contract 4.4 — Bank account details filled (Treasury account); aligned"),\n    ("5.1.5", "missing_in_contract", "No Bank right not to reimburse for operations violating contract terms"),\n    ("5.1.6", "linked", "Contract 5.2.3 + 5.2.4 — inspect, replace with 2-day notice, remote update; aligned"),\n    ("5.1.7", "missing_in_contract", "No Bank right to transmit fraud/suspicious data to Mir independently of contract term"),\n    ("5.1.8.1", "linked", "Contract 5.2.9.1 — suspend/terminate for Customer breach; aligned"),\n    ("5.1.8.2", "linked", "Contract 5.2.9.2 — suspend/terminate for extremism/terrorism listing; aligned"),\n    ("5.1.8.3", "linked", "Contract 5.2.9.3 — suspend/terminate for AML/CFT suspicion; aligned"),\n    ("5.1.8.4", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("5.1.8.5", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("5.1.8.6", "linked", "Contract 5.2.9.4 — suspend/terminate for negative government/payment system info; aligned"),\n    ("5.1.8.7", "linked", "Contract 5.2.9.5 + preamble — suspend/terminate for fraud info; aligned"),\n    ("5.1.8.8", "linked", "Contract 5.2.9.6 — suspend/terminate for TST renovation; aligned"),\n    ("5.1.8.9", "linked", "Contract 5.2.9.7 — suspend/terminate for liquidation/bankruptcy; aligned"),\n    ("5.1.8.10", "linked", "Contract 5.2.9.8 — suspend/terminate for false info; aligned"),\n    ("5.1.8.11", "linked", "Contract 5.2.9.9 — suspend/terminate for activity mismatch; aligned"),\n    ("5.1.8.12", "linked", "Contract 5.2.9.10 — suspend/terminate for 30-day inactivity; aligned"),\n    ("5.1.8.13", "linked", "Contract 5.2.9.11 — suspend/terminate for price exhaustion/term expiry; aligned"),\n    ("5.1.9", "missing_in_contract", "No Bank right to conduct additional checks including issuer bank contact"),\n    ("5.1.10", "linked", "Contract 5.2.3 + 5.3.17 — terminal inspection + non-obstruction; explicit enterprise-check right absent → deviation"),\n    ("5.1.11", "linked", "Contract 5.2.5 — request documents within 13 months; aligned"),\n    ("5.1.12", "missing_in_contract", "No Bank right to unilaterally amend referenced documents via website with 1-day notice"),\n    ("5.1.13", "missing_in_contract", "No Bank right to notify rekvizit changes via website; contract 5.2.6 uses written notice"),\n    ("5.1.14", "linked", "Contract 5.2.7 — send operation-info requests to Customer email; aligned"),\n    ("5.1.15", "missing_in_contract", "No Bank right to refuse contract conclusion without explanation; 44-FZ regime makes inapplicable in practice"),\n    ("5.1.16", "linked", "Contract 5.2.8 — demand documents/info for statutory functions; aligned"),\n    ("5.1.17.1", "missing_in_contract", "No POS terminal turnover threshold for unilateral termination; contract has POS terminals"),\n    ("5.1.17.2", "out_of_scope", "only_for_terminal=smart; no smart terminals in contract"),\n    ("5.2.1", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("5.2.2", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("5.2.3", "linked", "Contract 5.1.1 — install terminals within 5 working days + instruction; matrix expects ≥3 days, 5 is beneficial; aligned"),\n    ("5.2.4", "linked", "Contract 5.1.6 — 24/7 authorization; aligned"),\n    ("5.2.5", "linked", "Contract 5.1.1 — training materials at website; URL blank → deviation"),\n    ("5.2.6", "linked", "Contract 5.1.7 — terminals with informational materials; aligned"),\n    ("5.2.7", "linked", "Contract 5.1.4 — 24/7 operability, replacement within 3 working days; aligned"),\n    ("5.2.8", "linked", "Contract 5.1.8 — transfer within 2 working days or 3 calendar days on failure; aligned"),\n    ("5.2.9", "missing_in_contract", "No Bank duty to provide QR code; payment_method=qr, no active QR product"),\n    ("5.2.10", "linked", "Contract 5.1.9 — PDn processing per 152-FZ; aligned"),\n    ("5.2.12", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("6.1", "linked", "Contract 3.2 + Specification — fee as % of each operation; blank percentage → deviation"),\n    ("6.2", "linked", "Contract 8.3.1 + 8.3.2 — EIS acceptance document by 10th working day (vs matrix 5th); deviation on doc type and timing"),\n    ("6.3", "out_of_scope", "only_for_lot=fz_223"),\n    ("6.4", "linked", "Contract 8.5 — EIS acceptance: 10 working days sign or refuse; aligned"),\n    ("6.5", "linked", "Contract 4.5 — payment within 7 working days (vs matrix 5); deviation on deadline"),\n    ("6.6", "out_of_scope", "only_for_lot=fz_223"),\n    ("6.7", "out_of_scope", "only_for_terminal=smart"),\n    ("6.8", "out_of_scope", "only_for_terminal=smart"),\n    ("6.9", "out_of_scope", "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.10", "out_of_scope", "only_for_terminal=smart"),\n    ("6.11", "out_of_scope", "only_for_terminal=smart"),\n    ("6.12", "out_of_scope", "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.13", "out_of_scope", "only_for_terminal=smart"),\n    ("6.14", "out_of_scope", "only_for_terminal=smart"),\n    ("6.15", "out_of_scope", "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.16", "out_of_scope", "only_for_terminal=smart"),\n    ("6.17", "out_of_scope", "only_for_terminal=smart"),\n    ("6.18", "out_of_scope", "only_for_lot=fz_223 and only_for_terminal=smart"),\n    ("6.20", "linked", "Technical Assignment p.5 — no fee for return/chargeback/reversal, original fee not refunded; aligned"),\n    ("6.21", "linked", "Contract 3.1 — max price 1 900 000 RUB; aligned"),\n    ("7.1", "linked", "Contract 7.1 — parties bear liability per contract and RF law; aligned"),\n    ("7.2", "linked", "Contract 7.4 + 7.4.1 — Customer штраф per PP 1042: 1000 RUB for ≤3M; aligned"),\n    ("7.3", "linked", "Contract 7.1 para 4 + 7.11 — total Customer штраф ≤ contract price; aligned"),\n    ("7.4", "linked", "Contract 7.5-7.6 — Bank delay penalty 1/300 key rate; aligned"),\n    ("7.5", "linked", "Contract 7.7 + 7.7.1 — Bank штраф per PP 1042: 10% for ≤3M; aligned"),\n    ("7.6", "linked", "Contract 7.7.3 — Bank штраф non-pecuniary: 1000 RUB for ≤3M; aligned"),\n    ("7.7", "linked", "Contract 7.10 — total Bank штраф ≤ contract price; aligned"),\n    ("7.8", "missing_in_contract", "No Bank exemption from liability for Customer-Buyer disputes or card-paid goods/services"),\n    ("7.9", "missing_in_contract", "No Bank exemption from liability for transfer delays not caused by Bank"),\n    ("7.10", "missing_in_contract", "No Bank exemption from liability for third-party actions including payment system participants"),\n    ("7.11", "missing_in_contract", "No Bank exemption from liability for delayed transfer during investigation"),\n    ("7.12", "missing_in_contract", "No Bank exemption from liability for exceeding contract price"),\n    ("7.13", "out_of_scope", "only_for_product=internet_acquiring"),\n    ("7.14", "missing_in_contract", "No Customer liability for all SPEP actions; SPEP not applicable to trade_acquiring but matrix row is common"),\n    ("7.15", "missing_in_contract", "No Customer full liability for personnel actions violating contract/Bank instructions"),\n    ("7.16", "linked", "Contract 6.1 — anti-corruption clause; aligned"),\n    ("7.17", "missing_in_contract", "No Customer financial liability for recurring payments non-compliance"),\n    ("8.1", "linked", "Contract 9.1 — force majeure definition, examples, deadline extension; aligned"),\n    ("8.2", "linked", "Contract 9.2 — 5-day notice (vs 24h), 1-month termination (vs 3 months); deviation on hard terms"),\n    ("9.1", "linked", "Contract 10.1 — mandatory pre-trial negotiations; aligned"),\n    ("9.2", "linked", "Contract 10.1 — 10 calendar days for claim response; aligned"),\n    ("9.3", "linked", "Contract 10.2 — Arbitration Court of Krasnodar Krai; aligned"),\n    ("10.1", "linked", "Contract 11.1 + 4.1 — term to 30.12.2025 or price exhaustion; liability survives; aligned"),\n    ("10.2", "linked", "Contract 11.3 + 11.5 — 44-FZ unilateral termination replaces 30-day notice; deviation on procedure"),\n    ("10.3", "linked", "Contract 11.1 — general survival clause; 18-month settlement period absent → deviation"),\n    ("11.1", "missing_in_contract", "No clause that payment system rules prevail over contract if consistent with RF law"),\n    ("11.2", "missing_in_contract", "No confidentiality of card numbers, PDn, operation amounts, payment info"),\n    ("11.3", "missing_in_contract", "No non-disclosure of card security elements, operation technology, financial info"),\n    ("11.4", "linked", "Contract 11.2 — written amendments signed by both parties; aligned"),\n    ("11.5", "linked", "Contract 11.7 — matters not covered governed by RF legislation; aligned"),\n    ("11.6", "linked", "Contract 12.4 — electronic form with UKEP replaces physical copies; aligned"),\n    ("11.7", "linked", "Contract 1.1 + 12.5 — appendices are integral parts; aligned"),\n    ("11.8", "missing_in_contract", "No Customer warranty that goods/services sales comply with RF legislation"),\n    ("11.9", "linked", "Contract 12.1-12.2 — no substitution except succession; aligned"),\n    ("11.10", "linked", "Contract 12.1-12.2 — reorganization succession, liquidation claims; aligned"),\n    ("11.11", "missing_in_contract", "No provision that Bank instructive materials on website become binding next working day"),\n    ("11.12", "linked", "Contract 10.1 para 2 — notices per contract channels deemed proper; aligned"),\n    ("11.13", "linked", "Contract 12.5 — appendix list; aligned"),\n]\n\n# Verify 169 rows\nassert len(matrix_rows) == 169, f"Expected 169 matrix rows, got {len(matrix_rows)}"\n\n# Verify every matrix id appears exactly once\nmatrix_ids_in_ledger = [r[0] for r in matrix_rows]\n# Check for duplicates\nfrom collections import Counter\ncounts = Counter(matrix_ids_in_ledger)\ndups = [k for k, v in counts.items() if v > 1]\nif dups:\n    print(f"WARNING: Duplicate matrix_ids: {dups}")\nmissing_from_ledger = []\n# We\'d need the original matrix.json to verify every ID is covered\n\n# ============================================================\n# LINKS\n# ============================================================\n\nlinks = [\n    # 2.1 TST Registration\n    {"contract_ids": ["4.3"], "matrix_ids": ["2.1"], "relationship": "deviation",\n     "status_reason": "Contract 4.3 requires post-conclusion TST registration application + info; matrix 2.1 Bank right to refuse registration without explanation is absent from contract",\n     "risk_level": "medium",\n     "discrepancies": [{"type": "other", "description": "Matrix 2.1: Bank may refuse TST registration without explanation. Contract 4.3 provides no Bank refusal right — Customer provides documents after contract conclusion but Bank cannot refuse TST registration.", "risk": "Bank loses pre-registration screening right; TST may be registered that does not meet Bank standards, creating operational and fraud risk"}]},\n\n    # 2.2 Currency\n    {"contract_ids": ["4.4", "Technical Assignment p.5"], "matrix_ids": ["2.2"], "relationship": "aligned",\n     "status_reason": "Contract 4.4 and Technical Assignment confirm RUB settlement; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.3.1 Email\n    {"contract_ids": ["2.3.1"], "matrix_ids": ["2.3.1"], "relationship": "aligned",\n     "status_reason": "Contract 2.3.1 mirrors matrix email exchange with full legal force; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.3.2 DBO\n    {"contract_ids": ["2.3.2"], "matrix_ids": ["2.3.2"], "relationship": "aligned",\n     "status_reason": "Contract 2.3.2 mirrors matrix DBO system exchange; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.3.3 Courier\n    {"contract_ids": ["2.3.3"], "matrix_ids": ["2.3.3"], "relationship": "aligned",\n     "status_reason": "Contract 2.3.3 mirrors courier delivery option; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.3.4 Registered Mail\n    {"contract_ids": ["2.3.4"], "matrix_ids": ["2.3.4"], "relationship": "aligned",\n     "status_reason": "Contract 2.3.4 mirrors registered mail option; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.3.5 E-invoicing\n    {"contract_ids": ["2.3.5"], "matrix_ids": ["2.3.5"], "relationship": "deviation",\n     "status_reason": "Contract 2.3.5 provides E-invoicing channel with UKEP but system name is blank placeholder",\n     "risk_level": "low",\n     "discrepancies": [{"type": "other", "description": "Matrix requires named automated system (E-invoicing/СФЕРА-Курьер); contract has blank placeholder preventing identification of EDI operator.", "risk": "Without named system, Bank cannot ensure the EDI channel is operational; low risk as other channels remain available"}]},\n\n    # 2.3.6 EIS\n    {"contract_ids": ["2.3.6"], "matrix_ids": ["2.3.6"], "relationship": "aligned",\n     "status_reason": "Contract 2.3.6 EIS channel present for 44-FZ regime with UKEP; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.3.7 Support Service + Receipt Rules\n    {"contract_ids": ["2.3.7", "2.3"], "matrix_ids": ["2.3.7"], "relationship": "aligned",\n     "status_reason": "Contract 2.3.7 support service channel + receipt-date rules in 2.3 chapeau match matrix; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.4 Integral Documents\n    {"contract_ids": ["1.1", "12.5"], "matrix_ids": ["2.4"], "relationship": "aligned",\n     "status_reason": "Contract 1.1 and 12.5 declare appendices integral parts; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 2.7 Electronic Conclusion\n    {"contract_ids": ["12.4"], "matrix_ids": ["2.7"], "relationship": "aligned",\n     "status_reason": "Contract 12.4 — electronic form signed with UKEP, equal legal force to paper; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 3.1 Merchant Card Acceptance\n    {"contract_ids": ["1.3", "Technical Assignment p.3"], "matrix_ids": ["3.1"], "relationship": "aligned",\n     "status_reason": "Contract 1.3 — Customer organizes card acceptance; Technical Assignment p.3 lists accepted payment systems; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 3.2 Bank Transfers\n    {"contract_ids": ["5.1.10", "5.1.8"], "matrix_ids": ["3.2"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.10 + 5.1.8 — Bank duty to transfer operation sums; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 3.3 Merchant Pays Bank\n    {"contract_ids": ["3.2", "4.4", "Specification"], "matrix_ids": ["3.3"], "relationship": "aligned",\n     "status_reason": "Contract 3.2 + 4.4 + Specification — Customer pays Bank fee monthly; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.1.1 Card Reference Right\n    {"contract_ids": ["5.4.5"], "matrix_ids": ["4.1.1"], "relationship": "deviation",\n     "status_reason": "Contract 5.4.5: Customer right to reference card payment with Bank pre-approval; matrix 4.1.1 also covers QR-code reference; QR aspect absent",\n     "risk_level": "low",\n     "discrepancies": [{"type": "scope", "description": "Matrix covers referencing both card and QR payment with Bank approval. Contract 5.4.5 covers cards only; QR aspect is absent.", "risk": "Low risk given no active QR product; card-only approval right is preserved"}]},\n\n    # 4.1.2 Consultation Right\n    {"contract_ids": ["5.9"], "matrix_ids": ["4.1.2"], "relationship": "aligned",\n     "status_reason": "Contract 5.9 — Customer right to consultation on terminal operation via support service; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.1 Payment Duty\n    {"contract_ids": ["3.2", "4.4", "Specification"], "matrix_ids": ["4.2.1"], "relationship": "aligned",\n     "status_reason": "Contract 3.2 + 4.4 + Specification — Customer pays Bank per tariff; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.4 Place Info Materials\n    {"contract_ids": ["5.3.7"], "matrix_ids": ["4.2.4"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.7 — Customer places Bank informational materials at TST; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.5 Card Acceptance Rules\n    {"contract_ids": ["5.3.8", "5.3.9", "Technical Assignment p.3"], "matrix_ids": ["4.2.5"], "relationship": "deviation",\n     "status_reason": "Contract covers no-splitting (5.3.8) and no-misuse (5.3.9) and lists cards; but \'accept all cards all hours\', \'no cash\', \'max 2 cards\' absent",\n     "risk_level": "low",\n     "discrepancies": [{"type": "scope", "description": "Matrix requires: (1) accept ALL listed cards during ALL working hours, (2) no cash disbursement, (3) max 2 cards per buyer. Contract omits these protections.", "risk": "Customer could selectively accept cards, issue cash, or allow splitting across many cards, increasing fraud/operational risk"}]},\n\n    # 4.2.6 No Splitting\n    {"contract_ids": ["5.3.8"], "matrix_ids": ["4.2.6"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.8 — no splitting one operation into multiple sums; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.7 No Misuse of Card Data\n    {"contract_ids": ["5.3.9"], "matrix_ids": ["4.2.7"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.9 — no use of card details for other purposes; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.9 Operations per Rules\n    {"contract_ids": ["5.3.10"], "matrix_ids": ["4.2.9"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.10 — conduct operations and prepare documents per rules, bears responsibility; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.10 Document Storage\n    {"contract_ids": ["5.3.11"], "matrix_ids": ["4.2.10"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.11 — store documents 13+ months, provide copies within 3 working days; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.11 Statement on Operations\n    {"contract_ids": ["5.5"], "matrix_ids": ["4.2.11"], "relationship": "aligned",\n     "status_reason": "Contract 5.5 — written statement within 3 working days, immediate notice of document loss; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.13 Reimbursement Duty\n    {"contract_ids": ["5.3.19"], "matrix_ids": ["4.2.13"], "relationship": "deviation",\n     "status_reason": "Contract 5.3.19 covers reimbursement for disputed/invalid operations, chargeback fees, and Bank losses; lacks unconditional qualifier",\n     "risk_level": "low",\n     "discrepancies": [{"type": "scope", "description": "Matrix requires unconditional (безусловном) reimbursement. Contract 5.3.19 covers substantive grounds but lacks the unconditional qualifier.", "risk": "Customer could dispute reimbursement obligation rather than it being automatic; low residual risk given substantive coverage"}]},\n\n    # 4.2.14 Change Notification\n    {"contract_ids": ["5.3.13"], "matrix_ids": ["4.2.14"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.13 — notify Bank within 3 working days of changes; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.15 KYC/Compliance Docs\n    {"contract_ids": ["5.3.14"], "matrix_ids": ["4.2.15"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.14 — provide reliable docs/info annually and within 7 working days; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.16.1 Director PDn\n    {"contract_ids": ["5.3.20"], "matrix_ids": ["4.2.16.1"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.20 — director PDn transfer with legal basis guarantee, Mir consent, withdrawal notice duty; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.16.3 PDn Proof\n    {"contract_ids": ["5.3.15"], "matrix_ids": ["4.2.16.3"], "relationship": "deviation",\n     "status_reason": "Contract 5.3.15 covers proof of lawful PDn transfer + indemnity; response deadline absent, scope limited to director",\n     "risk_level": "low",\n     "discrepancies": [{"type": "deadline", "description": "Matrix requires proof within 3 working days of written Bank request. Contract 5.3.15 provides proof/indemnity mechanism without stated response deadline.", "risk": "Without deadline, Customer could delay PDn compliance proof indefinitely, leaving Bank exposed to data-protection liability"}]},\n\n    # 4.2.18 Post-Termination\n    {"contract_ids": ["5.3.16"], "matrix_ids": ["4.2.18"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.16 — cease card acceptance, remove materials post-termination; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.19 Non-Obstruction\n    {"contract_ids": ["5.3.17"], "matrix_ids": ["4.2.19"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.17 — not obstruct Bank checks, assist fraud investigation; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.20.1 Staff Instruction\n    {"contract_ids": ["5.10"], "matrix_ids": ["4.2.20.1"], "relationship": "deviation",\n     "status_reason": "Contract 5.10 — employee self-training at Bank website; website URL is blank placeholder",\n     "risk_level": "low",\n     "discrepancies": [{"type": "other", "description": "Matrix requires training at sberbank.ru/help/business/acquiring. Contract 5.10 has blank placeholder for website URL.", "risk": "Without specified URL, Customer may not know where to access training materials, reducing staff instruction effectiveness"}]},\n\n    # 4.2.20.2 Terminal Use Restrictions\n    {"contract_ids": ["5.3.18.1"], "matrix_ids": ["4.2.20.2"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.18.1 — use only for contract purposes at installation address, no modifications/self-repair/third-party transfer; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.20.3 Access for Service\n    {"contract_ids": ["5.3.18.2"], "matrix_ids": ["4.2.20.3"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.18.2 — provide access for connection, setup, repair, replacement, maintenance, inspection; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.20.4 Terminal Acceptance Act\n    {"contract_ids": ["5.3.18.3"], "matrix_ids": ["4.2.20.4"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.18.3 — accept terminals by act in 2 copies; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.20.5 Malfunction Notice\n    {"contract_ids": ["5.3.20.4"], "matrix_ids": ["4.2.20.5"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.20.4 — immediately inform Bank of terminal malfunction/loss; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.20.6 Terminal Return\n    {"contract_ids": ["5.3.18.5", "5.6"], "matrix_ids": ["4.2.20.6"], "relationship": "aligned",\n     "status_reason": "Contract 5.3.18.5 + 5.6 — return terminals within 5 working days; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 4.2.20.7 Non-Return Penalty\n    {"contract_ids": ["5.7"], "matrix_ids": ["4.2.20.7"], "relationship": "deviation",\n     "status_reason": "Contract 5.7: штраф 10 000 RUB electronic terminal, 25 000 RUB smart terminal; matrix requires 25 000 RUB for both",\n     "risk_level": "medium",\n     "discrepancies": [{"type": "amount", "description": "Matrix: 25 000 RUB each for electronic and smart terminals. Contract: 10 000 RUB for electronic, 25 000 RUB for smart. 60% lower for electronic terminals.", "risk": "Electronic terminal non-return penalty reduced from 25 000 to 10 000 RUB; with 14 terminals deployed, reduced incentive to return Bank equipment"}]},\n\n    # 5.1.1.1 Invalid Operations Withholding\n    {"contract_ids": ["5.2.10", "5.2.10.1"], "matrix_ids": ["5.1.1.1"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10 + 5.2.10.1 — 12 grounds for withholding invalid operation amounts substantively match matrix; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.1.2 Erroneous Transfer Withholding\n    {"contract_ids": ["5.2.10.2"], "matrix_ids": ["5.1.1.2"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10.2 — Bank right to withhold erroneously transferred sums; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.1.3 Return/Chargeback Withholding\n    {"contract_ids": ["5.2.10.3"], "matrix_ids": ["5.1.1.3"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10.3 — Bank right to withhold return/chargeback/reversal amounts; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.1.4 Disputed Operations Withholding\n    {"contract_ids": ["5.2.10.4"], "matrix_ids": ["5.1.1.4"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10.4 — Bank right to withhold disputed/charged-back sums; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.1.5 Penalty/Loss Withholding\n    {"contract_ids": ["5.2.10.5"], "matrix_ids": ["5.1.1.5"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10.5 — Bank right to withhold штраф/loss from penalties; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.1.6 Terminal Non-Return Penalty Withholding\n    {"contract_ids": ["5.2.10", "5.7"], "matrix_ids": ["5.1.1.6"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10 with 5.7 — Bank can withhold штраф for terminal non-return; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.3 Direct Debit\n    {"contract_ids": ["5.2.10", "Приложение 1.1"], "matrix_ids": ["5.1.3"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.10 + App 1.1 p.3 (заранее данный акцепт) — Bank right to direct debit; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.4 Payment Claim\n    {"contract_ids": ["4.4"], "matrix_ids": ["5.1.4"], "relationship": "aligned",\n     "status_reason": "Contract 4.4 — Customer bank details filled (Treasury account); aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.6 Terminal Inspection\n    {"contract_ids": ["5.2.3", "5.2.4"], "matrix_ids": ["5.1.6"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.3 + 5.2.4 — inspect, replace with 2-day notice, remote update without notice; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.1 Contract Breach\n    {"contract_ids": ["5.2.9.1"], "matrix_ids": ["5.1.8.1"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.1 — suspend/terminate for Customer breach; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.2 Extremism/Terrorism\n    {"contract_ids": ["5.2.9.2"], "matrix_ids": ["5.1.8.2"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.2 — suspend/terminate for extremism/terrorism listing; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.3 AML/CFT\n    {"contract_ids": ["5.2.9.3"], "matrix_ids": ["5.1.8.3"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.3 — suspend/terminate for AML/CFT suspicion; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.6 Negative Government Info\n    {"contract_ids": ["5.2.9.4"], "matrix_ids": ["5.1.8.6"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.4 — suspend/terminate for negative government/payment system info; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.7 Fraud Info\n    {"contract_ids": ["5.2.9.5", "5.2.9"], "matrix_ids": ["5.1.8.7"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.5 + preamble — suspend/terminate for fraud info; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.8 Premises Renovation\n    {"contract_ids": ["5.2.9.6"], "matrix_ids": ["5.1.8.8"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.6 — suspend/terminate for TST renovation preventing operations; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.9 Liquidation/Bankruptcy\n    {"contract_ids": ["5.2.9.7"], "matrix_ids": ["5.1.8.9"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.7 — suspend/terminate for liquidation/bankruptcy; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.10 False Info\n    {"contract_ids": ["5.2.9.8"], "matrix_ids": ["5.1.8.10"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.8 — suspend/terminate for false info; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.11 Activity Mismatch\n    {"contract_ids": ["5.2.9.9"], "matrix_ids": ["5.1.8.11"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.9 — suspend/terminate for activity mismatch; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.12 30-Day Inactivity\n    {"contract_ids": ["5.2.9.10"], "matrix_ids": ["5.1.8.12"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.10 — suspend/terminate for 30-day inactivity; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.8.13 Price Exhaustion/Term\n    {"contract_ids": ["5.2.9.11"], "matrix_ids": ["5.1.8.13"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.9.11 — suspend/terminate for price exhaustion/term expiry; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.10 Inspection Right\n    {"contract_ids": ["5.2.3", "5.3.17"], "matrix_ids": ["5.1.10"], "relationship": "deviation",\n     "status_reason": "Contract covers terminal inspection + non-obstruction but lacks explicit enterprise-level inspection right with resource access",\n     "risk_level": "low",\n     "discrepancies": [{"type": "scope", "description": "Matrix: Bank right to conduct enterprise checks for fraud/activity mismatch/contract compliance. Contract 5.2.3 covers terminals only; 5.3.17 covers non-obstruction but does not grant affirmative inspection right.", "risk": "Bank\'s ability to conduct comprehensive enterprise-level checks beyond terminals is not explicitly granted"}]},\n\n    # 5.1.11 Document Requests\n    {"contract_ids": ["5.2.5"], "matrix_ids": ["5.1.11"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.5 — request documents within 13 months; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.14 Email Requests\n    {"contract_ids": ["5.2.7"], "matrix_ids": ["5.1.14"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.7 — send operation-info requests to Customer email; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.1.16 Statutory Docs\n    {"contract_ids": ["5.2.8"], "matrix_ids": ["5.1.16"], "relationship": "aligned",\n     "status_reason": "Contract 5.2.8 — demand documents for statutory functions; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.2.3 Terminal Installation\n    {"contract_ids": ["5.1.1"], "matrix_ids": ["5.2.3"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.1 — install within 5 working days + instruction; matrix expects ≥3 days, 5 is beneficial; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.2.4 24/7 Authorization\n    {"contract_ids": ["5.1.6"], "matrix_ids": ["5.2.4"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.6 — 24/7 authorization; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.2.5 Training Materials\n    {"contract_ids": ["5.1.1"], "matrix_ids": ["5.2.5"], "relationship": "deviation",\n     "status_reason": "Contract 5.1.1 — Bank to place training materials at website; URL is blank placeholder",\n     "risk_level": "low",\n     "discrepancies": [{"type": "other", "description": "Matrix requires training at sberbank.ru/help/business/acquiring. Contract 5.1.1 has blank placeholder.", "risk": "Without specified URL, Customers cannot locate training materials"}]},\n\n    # 5.2.6 Terminal Info Materials\n    {"contract_ids": ["5.1.7"], "matrix_ids": ["5.2.6"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.7 — terminals with informational materials; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.2.7 24/7 Operability\n    {"contract_ids": ["5.1.4"], "matrix_ids": ["5.2.7"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.4 — 24/7 operability, replacement within 3 working days; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.2.8 Fund Transfer\n    {"contract_ids": ["5.1.8"], "matrix_ids": ["5.2.8"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.8 — transfer within 2 working days, or 3 calendar days on failure; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 5.2.10 PDn Processing\n    {"contract_ids": ["5.1.9"], "matrix_ids": ["5.2.10"], "relationship": "aligned",\n     "status_reason": "Contract 5.1.9 — PDn processing per 152-FZ; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 6.1 Fee Rate\n    {"contract_ids": ["3.2", "Specification"], "matrix_ids": ["6.1"], "relationship": "deviation",\n     "status_reason": "Contract 3.2 + Specification establish fee as % of each operation but exact percentage is blank",\n     "risk_level": "medium",\n     "discrepancies": [{"type": "amount", "description": "Matrix and Contract both have blank percentage field for commission rate. Neither source fills the rate.", "risk": "Without agreed commission rate, the price term is incomplete; payment calculation unenforceable until blank is filled"}]},\n\n    # 6.2 Billing Document\n    {"contract_ids": ["8.3.1", "8.3.2"], "matrix_ids": ["6.2"], "relationship": "deviation",\n     "status_reason": "Contract uses EIS acceptance document instead of UPD; 10th working day vs matrix 5th; 44-FZ mechanism replaces template",\n     "risk_level": "low",\n     "discrepancies": [{"type": "deadline", "description": "Matrix: Bank sends UPD by 5th working day. Contract: EIS document by 10th working day. Document type differs, 5-day delay.", "risk": "Later billing shifts payment timeline; 44-FZ EIS mechanism provides enforceable alternative, risk is low"}]},\n\n    # 6.4 Acceptance\n    {"contract_ids": ["8.5", "8.5.1", "8.5.7"], "matrix_ids": ["6.4"], "relationship": "aligned",\n     "status_reason": "Contract 8.5 — EIS acceptance within 10 working days; 44-FZ mechanism preserves enforceable acceptance; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 6.5 Payment Deadline\n    {"contract_ids": ["4.5"], "matrix_ids": ["6.5"], "relationship": "deviation",\n     "status_reason": "Contract 4.5: payment within 7 working days of acceptance; matrix: within 5 working days of UPD",\n     "risk_level": "low",\n     "discrepancies": [{"type": "deadline", "description": "Matrix: 5 working days from UPD signing. Contract: 7 working days from acceptance document. 2-day extension.", "risk": "Payment deferral by 2 working days provides marginal cash-flow delay for Bank"}]},\n\n    # 6.20 Return/Chargeback Fee\n    {"contract_ids": ["Technical Assignment p.5"], "matrix_ids": ["6.20"], "relationship": "aligned",\n     "status_reason": "Technical Assignment p.5 — no fee for return/chargeback/reversal, original fee not refunded; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 6.21 Contract Price\n    {"contract_ids": ["3.1"], "matrix_ids": ["6.21"], "relationship": "aligned",\n     "status_reason": "Contract 3.1 — max price 1 900 000 RUB; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.1 General Liability\n    {"contract_ids": ["7.1"], "matrix_ids": ["7.1"], "relationship": "aligned",\n     "status_reason": "Contract 7.1 — parties bear liability per contract and RF law; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.2 Customer Penalty\n    {"contract_ids": ["7.4", "7.4.1"], "matrix_ids": ["7.2"], "relationship": "aligned",\n     "status_reason": "Contract 7.4 + 7.4.1 — Customer штраф per PP 1042: 1000 RUB for ≤3M; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.3 Customer Penalty Cap\n    {"contract_ids": ["7.1", "7.11"], "matrix_ids": ["7.3"], "relationship": "aligned",\n     "status_reason": "Contract 7.1 para 4 + 7.11 — total Customer штраф ≤ contract price; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.4 Bank Delay Penalty\n    {"contract_ids": ["7.5", "7.6"], "matrix_ids": ["7.4"], "relationship": "aligned",\n     "status_reason": "Contract 7.5-7.6 — Bank delay penalty 1/300 key rate; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.5 Bank Penalty Amount\n    {"contract_ids": ["7.7", "7.7.1"], "matrix_ids": ["7.5"], "relationship": "aligned",\n     "status_reason": "Contract 7.7 + 7.7.1 — Bank штраф per PP 1042: 10% for ≤3M; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.6 Bank Non-Pecuniary Penalty\n    {"contract_ids": ["7.7.3"], "matrix_ids": ["7.6"], "relationship": "aligned",\n     "status_reason": "Contract 7.7.3 — Bank штраф non-pecuniary: 1000 RUB for ≤3M; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.7 Bank Penalty Cap\n    {"contract_ids": ["7.10"], "matrix_ids": ["7.7"], "relationship": "aligned",\n     "status_reason": "Contract 7.10 — total Bank штраф ≤ contract price; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 7.16 Anti-Corruption\n    {"contract_ids": ["6.1"], "matrix_ids": ["7.16"], "relationship": "aligned",\n     "status_reason": "Contract 6.1 — anti-corruption clause; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 8.1 Force Majeure\n    {"contract_ids": ["9.1"], "matrix_ids": ["8.1"], "relationship": "aligned",\n     "status_reason": "Contract 9.1 — force majeure definition, examples, proportional deadline extension; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 8.2 Force Majeure Notice\n    {"contract_ids": ["9.2"], "matrix_ids": ["8.2"], "relationship": "deviation",\n     "status_reason": "Contract 9.2: 5-day notice (vs 24h), 1-month termination (vs 3 months); material hard-term differences",\n     "risk_level": "medium",\n     "discrepancies": [\n         {"type": "deadline", "description": "Matrix: force majeure notice within 24 hours. Contract: within 5 days.", "risk": "5-day delay prevents Bank from taking timely mitigation measures during operational disruptions"},\n         {"type": "deadline", "description": "Matrix: termination right after 3 months of force majeure. Contract: after 1 month. Shorter period is beneficial to Bank.", "risk": "Earlier termination right is protective; this deviation benefits rather than harms Bank"}\n     ]},\n\n    # 9.1 Pre-Trial Disputes\n    {"contract_ids": ["10.1"], "matrix_ids": ["9.1"], "relationship": "aligned",\n     "status_reason": "Contract 10.1 — mandatory pre-trial negotiations; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 9.2 Claim Period\n    {"contract_ids": ["10.1"], "matrix_ids": ["9.2"], "relationship": "aligned",\n     "status_reason": "Contract 10.1 — 10 calendar days for claim response; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 9.3 Court\n    {"contract_ids": ["10.2"], "matrix_ids": ["9.3"], "relationship": "aligned",\n     "status_reason": "Contract 10.2 — Arbitration Court of Krasnodar Krai; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 10.1 Contract Term\n    {"contract_ids": ["11.1", "4.1"], "matrix_ids": ["10.1"], "relationship": "aligned",\n     "status_reason": "Contract 11.1 + 4.1 — term to 30.12.2025 or price exhaustion; liability survives; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 10.2 Unilateral Termination\n    {"contract_ids": ["11.3", "11.5"], "matrix_ids": ["10.2"], "relationship": "deviation",\n     "status_reason": "Contract uses 44-FZ unilateral termination (Art. 95) instead of 30-day notice; 44-FZ procedure is more restrictive",\n     "risk_level": "low",\n     "discrepancies": [{"type": "procedure", "description": "Matrix: either party may terminate with 30 calendar days notice. Contract: termination per 44-FZ Art. 95 with statutory grounds and EIS notification.", "risk": "44-FZ termination is more restrictive; Bank cannot terminate for convenience and must meet statutory grounds"}]},\n\n    # 10.3 Post-Termination Settlement\n    {"contract_ids": ["11.1"], "matrix_ids": ["10.3"], "relationship": "deviation",\n     "status_reason": "Contract 11.1 — general survival clause; matrix 10.3 requires 18-month settlement period with specific payment procedure",\n     "risk_level": "low",\n     "discrepancies": [{"type": "deadline", "description": "Matrix: 18-month settlement period after Bank unilateral termination with specific procedure. Contract: general survival clause without specified period.", "risk": "Without fixed 18-month window, post-termination reconciliation could extend indefinitely or close prematurely"}]},\n\n    # 11.4 Written Amendments\n    {"contract_ids": ["11.2"], "matrix_ids": ["11.4"], "relationship": "aligned",\n     "status_reason": "Contract 11.2 — changes/additions valid only if written and signed by both parties; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.5 Entire Agreement\n    {"contract_ids": ["11.7"], "matrix_ids": ["11.5"], "relationship": "aligned",\n     "status_reason": "Contract 11.7 — matters not covered governed by RF legislation; prior agreements superseded; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.6 Copies\n    {"contract_ids": ["12.4"], "matrix_ids": ["11.6"], "relationship": "aligned",\n     "status_reason": "Contract 12.4 — electronic form with UKEP replaces physical copies; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.7 Appendices Integral\n    {"contract_ids": ["1.1", "12.5"], "matrix_ids": ["11.7"], "relationship": "aligned",\n     "status_reason": "Contract 1.1 + 12.5 — appendices are integral parts; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.9 Assignment\n    {"contract_ids": ["12.1", "12.2"], "matrix_ids": ["11.9"], "relationship": "aligned",\n     "status_reason": "Contract 12.1-12.2 — no substitution except succession; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.10 Succession\n    {"contract_ids": ["12.1", "12.2"], "matrix_ids": ["11.10"], "relationship": "aligned",\n     "status_reason": "Contract 12.1-12.2 — reorganization succession, liquidation claims per legislation; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.12 Notice Validity\n    {"contract_ids": ["10.1"], "matrix_ids": ["11.12"], "relationship": "aligned",\n     "status_reason": "Contract 10.1 para 2 — notices per contract channels deemed proper; aligned", "risk_level": "none", "discrepancies": []},\n\n    # 11.13 Appendix List\n    {"contract_ids": ["12.5"], "matrix_ids": ["11.13"], "relationship": "aligned",\n     "status_reason": "Contract 12.5 — list of appendices; aligned", "risk_level": "none", "discrepancies": []},\n]\n\n# ============================================================\n# UNMATCHED MATRIX (missing_in_contract)\n# ============================================================\nunmatched_matrix = [\n    {"matrix_id": "2.6.2.1", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "QR-API mechanism for own KKT software: Bank provides QR-API for dynamic QR code via API, terms on Bank website",\n     "risk_level": "low",\n     "risk": "QR display capability mentioned in Technical Assignment but no active QR-API product. Low risk as Customer uses Bank-provided terminals, not own KKT with QR-API."},\n    {"matrix_id": "2.6.2.2", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "QR-Vendor mechanism: Bank transfers QR parameters via QR-Vendor through separate Vendor contract when Customer lacks own software",\n     "risk_level": "low",\n     "risk": "No QR-Vendor integration. Low risk given Customer uses Bank-provided terminals, not own KKT software."},\n    {"matrix_id": "2.6.3.1", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "QR auto-connection on Bank electronic terminal installation at TST",\n     "risk_level": "low",\n     "risk": "QR display capability is not an active QR product. Low risk as core service is card acquiring."},\n    {"matrix_id": "2.6.3.2", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "QR deactivation procedure on merchant initiative via Bank notification through specified channels",\n     "risk_level": "low",\n     "risk": "No active QR product to deactivate. Low risk."},\n    {"matrix_id": "4.2.2", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer duty to comply with Bank instructive/informational materials",\n     "risk_level": "low",\n     "risk": "Contract 5.10 covers self-training only, not affirmative duty to comply with Bank instructions. Low risk as operational procedures covered by other clauses."},\n    {"matrix_id": "4.2.8", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Customer duty to provide goods/services at prices not exceeding cash prices (no card surcharge)",\n     "risk_level": "medium",\n     "risk": "No anti-surcharge provision. Customer could charge higher prices for card payments, discouraging card use and reducing acquiring volumes."},\n    {"matrix_id": "4.2.12", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer duty to accept Bank payment claims/invoices within 5 working days of issuance",\n     "risk_level": "low",\n     "risk": "EIS acceptance replaces this mechanism; 44-FZ mandatory route provides alternative enforceable procedure."},\n    {"matrix_id": "4.2.16.2", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Customer guarantee of employee (non-director) PDn consent: full name, mobile, email, position, workplace; with transfer to service companies",\n     "risk_level": "medium",\n     "risk": "Contract only covers director PDn (5.3.20). Employee PDn for terminal servicing is not addressed. Bank and service companies process employee data without documented consent framework. Medium risk re 152-FZ."},\n    {"matrix_id": "4.2.22", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer duty to provide QR code to buyer for SberPayQR/Plati QR payment",\n     "risk_level": "low",\n     "risk": "No active QR product in contract. Low risk."},\n    {"matrix_id": "4.2.23", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer duty not to unilaterally change partner QR code",\n     "risk_level": "low",\n     "risk": "No active QR product. Low risk."},\n    {"matrix_id": "4.2.24", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer duty to use API within QR-API functional boundaries per Bank website description",\n     "risk_level": "low",\n     "risk": "No active QR-API product. Low risk."},\n    {"matrix_id": "4.2.25", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer duty to immediately suspend API use and notify Bank on QR-API security breach detection",\n     "risk_level": "low",\n     "risk": "No active QR-API product. Low risk."},\n    {"matrix_id": "5.1.2", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Bank right to suspend authorization when Customer has debt until full repayment",\n     "risk_level": "medium",\n     "risk": "Contract 5.2.9 lists specific suspension grounds but not general debt-based suspension. Bank cannot quickly stop transaction flow for delinquent Customers."},\n    {"matrix_id": "5.1.5", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Bank right not to reimburse Customer for operations conducted in violation of contract terms",\n     "risk_level": "medium",\n     "risk": "Without explicit non-reimbursement right, Customer may claim payment for non-compliant operations. Withholding rights partially mitigate but do not create same standalone protection."},\n    {"matrix_id": "5.1.7", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Bank right to transmit fraud/suspicious operation data including director PDn to Mir payment system regardless of contract term",\n     "risk_level": "medium",\n     "risk": "PDn transfer to Mir only covered for service provision (5.3.20), not for independent fraud reporting. Bank needs this for payment system fraud monitoring compliance."},\n    {"matrix_id": "5.1.9", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Bank right to conduct additional operation checks including contacting issuer bank for legitimacy verification",\n     "risk_level": "medium",\n     "risk": "Contract allows document requests but not issuer-bank verification. Limits Bank\'s fraud investigation toolkit."},\n    {"matrix_id": "5.1.12", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank right to unilaterally amend referenced documents by website publication with 1 calendar day notice",\n     "risk_level": "low",\n     "risk": "Contract 11.2 requires bilateral written amendments. 44-FZ restricts unilateral changes. Low risk given 44-FZ constraints."},\n    {"matrix_id": "5.1.13", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank right to notify of own rekvizit changes via official website",\n     "risk_level": "low",\n     "risk": "Contract 5.2.6 uses written notification. Different channel but same practical effect. Low risk."},\n    {"matrix_id": "5.1.15", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank right to refuse contract conclusion without explanation",\n     "risk_level": "low",\n     "risk": "44-FZ procurement makes this right practically inapplicable — Bank enters as winner of competitive procurement. Low risk given regulatory context."},\n    {"matrix_id": "5.1.17.1", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank right to unilaterally terminate and demand terminal return if POS terminal turnover below 40 000 RUB/month (80 000 for Moscow/SPb)",\n     "risk_level": "low",\n     "risk": "No turnover threshold termination right. Low risk given fixed-term 44-FZ contract with defined price cap."},\n    {"matrix_id": "5.2.9", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank duty to provide QR code to merchant in electronic or paper form",\n     "risk_level": "low",\n     "risk": "No active QR product. Low risk."},\n    {"matrix_id": "7.8", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank exemption from liability for disputes between Customer and Buyer not related to contract subject or for card-paid goods/services",\n     "risk_level": "medium",\n     "risk": "Without exemption, Bank could be drawn into Customer-Buyer disputes. Medium risk for litigation exposure."},\n    {"matrix_id": "7.9", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank exemption from liability for fund transfer delays not caused by Bank",\n     "risk_level": "medium",\n     "risk": "Bank could be held liable for delays caused by payment system, intermediary banks, or external technical infrastructure."},\n    {"matrix_id": "7.10", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank exemption from liability for third-party actions/inactions including payment system participants",\n     "risk_level": "medium",\n     "risk": "Bank bears liability for payment system/third-party failures beyond its control."},\n    {"matrix_id": "7.11", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank exemption from liability for delayed transfer during Bank investigation of suspected violation",\n     "risk_level": "low",\n     "risk": "Conflicting obligations: investigate vs meet transfer deadlines. Withholding rights partially mitigate."},\n    {"matrix_id": "7.12", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank exemption from liability for exceeding contract price",\n     "risk_level": "low",\n     "risk": "Contract price cap provides structural protection. Low risk."},\n    {"matrix_id": "7.14", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Customer liability for all actions in SPEP (payment acceptance system)",\n     "risk_level": "low",\n     "risk": "SPEP not applicable to trade_acquiring. Low risk for this contract profile."},\n    {"matrix_id": "7.15", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Customer full liability for personnel actions violating contract/Bank instructions",\n     "risk_level": "medium",\n     "risk": "Without explicit personnel liability, Customer could argue it is not responsible for employee misconduct. Bank faces uncompensated losses from employee-caused violations."},\n    {"matrix_id": "7.17", "status": "missing_in_contract", "required_type": "mandatory",\n     "requirement": "Customer full financial liability for recurring payments non-compliance with legislation/Bank of Russia/payment system rules/contract",\n     "risk_level": "low",\n     "risk": "Recurring payments not present in this trade_acquiring contract. Low risk for this profile."},\n    {"matrix_id": "11.1", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Payment system rules prevail over contract if consistent with RF law; conflicting contract terms must align with payment system rules",\n     "risk_level": "medium",\n     "risk": "Without hierarchy clause, contract terms could conflict with payment system rules. Bank could face compliance violations or payment system penalties."},\n    {"matrix_id": "11.2", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Confidentiality of card numbers, payment account numbers, buyer PDn, operation amounts, payment info; prohibition on third-party transfer",\n     "risk_level": "medium",\n     "risk": "No comprehensive confidentiality clause protecting payment data. Customer could disclose sensitive payment information. Medium risk for data security and PCI DSS compliance."},\n    {"matrix_id": "11.3", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Non-disclosure of card security elements, operation technology, financial/management info of parties; disclosure only with both parties\' consent",\n     "risk_level": "low",\n     "risk": "No mutual non-disclosure of technical and financial information. Low risk given general confidentiality obligations under RF law."},\n    {"matrix_id": "11.8", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Customer warranty that goods/services sales in TST comply with RF legislation",\n     "risk_level": "low",\n     "risk": "No explicit compliance warranty. Low risk as compliance with law is generally implied."},\n    {"matrix_id": "11.11", "status": "missing_in_contract", "required_type": "optional",\n     "requirement": "Bank instructive materials posted on official website become binding next working day after posting",\n     "risk_level": "medium",\n     "risk": "Without this, Bank cannot unilaterally update operational procedures. Contract 11.2 requires bilateral amendments. 44-FZ constraints apply."},\n]\n\n# ============================================================\n# UNMATCHED CONTRACT (extra_in_contract)\n# ============================================================\nunmatched_contract = [\n    {"contract_id": "5.3.3", "status": "extra_in_contract",\n     "contract_position": "Заказчик обязуется осуществлять контроль за ходом оказания услуг Исполнителем",\n     "risk_level": "low",\n     "risk": "Customer monitoring right over Bank service delivery; could be used for intrusive oversight or as basis for claims",\n     "materiality_reason": "Creates independent Customer right to monitor Bank\'s service delivery progress"},\n\n    {"contract_id": "5.3.4", "status": "extra_in_contract",\n     "contract_position": "Заказчик обязуется принять решение об одностороннем отказе если Исполнитель не соответствует требованиям закупки или предоставил недостоверную информацию",\n     "risk_level": "medium",\n     "risk": "Mandatory Customer duty to terminate if Bank fails procurement eligibility; could force termination for formal/procedural reasons unrelated to service quality",\n     "materiality_reason": "44-FZ statutory duty forcing Customer to terminate if Bank\'s procurement eligibility lapses"},\n\n    {"contract_id": "5.3.5", "status": "extra_in_contract",\n     "contract_position": "Заказчик обязуется требовать уплаты неустоек (штрафов, пеней) в случае просрочки или иного неисполнения Исполнителем обязательств",\n     "risk_level": "low",\n     "risk": "Mandatory Customer duty to demand penalties from Bank for any breach; could generate additional claims even for minor issues",\n     "materiality_reason": "Creates affirmative Customer obligation to pursue penalties"},\n\n    {"contract_id": "5.3.6", "status": "extra_in_contract",\n     "contract_position": "Заказчик обязуется уменьшить сумму оплаты на размер налогов, сборов и иных обязательных платежей, связанных с оплатой контракта",\n     "risk_level": "medium",\n     "risk": "Customer can unilaterally deduct taxes from Bank payments; reduces Bank\'s receivable without consent or verification",\n     "materiality_reason": "44-FZ tax withholding mechanism allows unilateral payment reduction"},\n\n    {"contract_id": "5.4.2", "status": "extra_in_contract",\n     "contract_position": "Заказчик вправе отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества",\n     "risk_level": "medium",\n     "risk": "Unqualified acceptance refusal right; could delay or deny payment without objective criteria",\n     "materiality_reason": "Broad Customer right to refuse acceptance for inadequate quality; no matrix analogue"},\n\n    {"contract_id": "5.4.3", "status": "extra_in_contract",\n     "contract_position": "Заказчик вправе принять решение об одностороннем отказе от исполнения контракта по основаниям 44-ФЗ и ГК РФ",\n     "risk_level": "medium",\n     "risk": "Customer can terminate for statutory grounds; counterparty risk for Bank\'s service continuity and terminal investment recovery",\n     "materiality_reason": "Independent Customer unilateral termination right under 44-FZ and Civil Code"},\n\n    {"contract_id": "5.4.4", "status": "extra_in_contract",\n     "contract_position": "Заказчик вправе отказаться от оплаты услуг ненадлежащего качества, потребовать возврата уплаченных сумм и возмещения убытков",\n     "risk_level": "high",\n     "risk": "Triple remedy (non-payment + refund + damages) for quality claims without defined quality standards; significant financial exposure",\n     "materiality_reason": "Cumulative remedies for quality claims creating substantial Bank liability exposure"},\n\n    {"contract_id": "7.8", "status": "extra_in_contract",\n     "contract_position": "Обмен документами при применении мер ответственности осуществляется с использованием ЕИС",\n     "risk_level": "low",\n     "risk": "Mandatory EIS channel for penalty-related documents; standard 44-FZ procedure providing audit trail",\n     "materiality_reason": "Restricts penalty communication to EIS channel; 44-FZ procedural requirement"},\n\n    {"contract_id": "7.9", "status": "extra_in_contract",\n     "contract_position": "Применение неустойки не освобождает Стороны от исполнения обязательств по Контракту",\n     "risk_level": "low",\n     "risk": "Penalty payment does not release from performance; standard cumulative remedy provision",\n     "materiality_reason": "Preserves performance obligation alongside penalties; standard cumulative remedy"},\n\n    {"contract_id": "7.12", "status": "extra_in_contract",\n     "contract_position": "В случае расторжения Контракта другая Сторона вправе потребовать возмещения фактически понесенного ущерба сверх начисленных неустоек",\n     "risk_level": "medium",\n     "risk": "Post-termination actual damages claim beyond contractual penalties; uncapped liability exposure for Bank",\n     "materiality_reason": "Allows claim for actual damages beyond penalties after unilateral termination"},\n\n    {"contract_id": "8.2", "status": "extra_in_contract",\n     "contract_position": "Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг его специалистами",\n     "risk_level": "medium",\n     "risk": "Additional Bank liability for damages caused by specialists; covers \'damages\' without limitation or causation standard",\n     "materiality_reason": "Creates additional liability channel beyond general contract liability"},\n\n    {"contract_id": "8.5.5", "status": "extra_in_contract",\n     "contract_position": "Заказчик проводит экспертизу для проверки соответствия услуг условиям Контракта",\n     "risk_level": "low",\n     "risk": "Mandatory Customer expert review; could generate additional scrutiny and challenge to Bank service quality",\n     "materiality_reason": "44-FZ requirement for Customer expert review of services"},\n\n    {"contract_id": "8.5.6", "status": "extra_in_contract",\n     "contract_position": "Экспертиза может проводиться Заказчиком своими силами или с привлечением экспертов",\n     "risk_level": "low",\n     "risk": "External experts add cost and adversarial dimension to acceptance; low risk with proper documentation",\n     "materiality_reason": "Customer may engage external experts for service review"},\n\n    {"contract_id": "8.5.8", "status": "extra_in_contract",\n     "contract_position": "Приемочная комиссия подписывает решение или мотивированный отказ; Заказчик подписывает итоговый документ",\n     "risk_level": "low",\n     "risk": "Multi-level acceptance with commission review; procedural complexity but standard 44-FZ mechanism",\n     "materiality_reason": "Acceptance commission procedure with multiple signatories"},\n\n    {"contract_id": "8.5.9", "status": "extra_in_contract",\n     "contract_position": "Исполнитель вправе устранить причины мотивированного отказа и направить исправленный документ о приемке",\n     "risk_level": "low",\n     "risk": "Beneficial to Bank — provides correction opportunity after refusal; low risk",\n     "materiality_reason": "Bank right to cure defects and resubmit acceptance document"},\n\n    {"contract_id": "8.6", "status": "extra_in_contract",\n     "contract_position": "Датой приемки считается дата размещения в ЕИС документа о приемке, подписанного Заказчиком",\n     "risk_level": "low",\n     "risk": "Acceptance date tied to EIS posting; provides clear trigger for payment timeline",\n     "materiality_reason": "Defines acceptance date as EIS posting date"},\n\n    {"contract_id": "8.7", "status": "extra_in_contract",\n     "contract_position": "Внесение исправлений в документ о приемке через формирование исправленного документа в ЕИС",\n     "risk_level": "low",\n     "risk": "Formal correction mechanism via EIS; low risk procedural provision",\n     "materiality_reason": "Correction procedure for acceptance documents"},\n\n    {"contract_id": "8.9", "status": "extra_in_contract",\n     "contract_position": "Заказчик вправе не отказывать в приемке если несоответствие не препятствует приемке и устранено Исполнителем",\n     "risk_level": "low",\n     "risk": "Customer discretion to accept despite non-conformity; beneficial to Bank",\n     "materiality_reason": "Allows acceptance despite minor curable non-conformities"},\n\n    {"contract_id": "8.10", "status": "extra_in_contract",\n     "contract_position": "Исполнитель обязан безвозмездно устранить недостатки в течение 3 дней с даты заявления о них Заказчиком",\n     "risk_level": "medium",\n     "risk": "3-day cure period is very short for terminal issues at remote mountain locations; may be impossible for hardware replacement at distant TSTs",\n     "materiality_reason": "Bank duty to cure defects within 3 days at no cost, without materiality threshold"},\n\n    {"contract_id": "9.3", "status": "extra_in_contract",\n     "contract_position": "Сторона, ссылающаяся на обстоятельства непреодолимой силы, обязана представить документальное подтверждение от уполномоченного лица",\n     "risk_level": "low",\n     "risk": "Additional evidence burden for force majeure claims requiring third-party documentation",\n     "materiality_reason": "Force majeure documentary proof requirement from authorized body"},\n\n    {"contract_id": "11.6", "status": "extra_in_contract",\n     "contract_position": "Изменение и расторжение контракта осуществляется по статьям 34, 95, 96, 112 44-ФЗ",\n     "risk_level": "low",\n     "risk": "Incorporates 44-FZ constraints on amendments; mandatory law reference",\n     "materiality_reason": "44-FZ statutory framework for contract modification/termination"},\n\n    {"contract_id": "11.8", "status": "extra_in_contract",\n     "contract_position": "Изменение существенных условий контракта не допускается, за исключением случаев по 44-ФЗ",\n     "risk_level": "medium",\n     "risk": "Freezes material terms for contract duration; Bank cannot adjust fees, service scope, or procedures",\n     "materiality_reason": "Prohibition on material term changes except per 44-FZ"},\n\n    {"contract_id": "12.3", "status": "extra_in_contract",\n     "contract_position": "Допускается оказание услуги с улучшенными характеристиками по согласованию Сторон",\n     "risk_level": "low",\n     "risk": "Permits improved service characteristics by mutual agreement; beneficial flexibility",\n     "materiality_reason": "Allows service improvements without formal amendment"},\n\n    {"contract_id": "4.5.1", "status": "extra_in_contract",\n     "contract_position": "Услуги в ноябре оплачиваются не позднее 7 рабочих дней с даты подписания, но не позднее 30 декабря 2025",\n     "risk_level": "low",\n     "risk": "Specific November payment deadline with 30 December hard stop; budget-year constraint",\n     "materiality_reason": "Annual budget cycle payment constraint; standard for 44-FZ"},\n\n    {"contract_id": "4.2", "status": "extra_in_contract",\n     "contract_position": "Исполнитель должен иметь лицензию на осуществление банковских операций",\n     "risk_level": "low",\n     "risk": "Restates statutory licensing requirement; low risk",\n     "materiality_reason": "Bank must hold banking license per statutory requirement"},\n\n    {"contract_id": "8.3.2", "status": "extra_in_contract",\n     "contract_position": "К документу о приемке прилагаются счет-фактура, акт и счет ф.363; при расхождении приоритет документа о приемке",\n     "risk_level": "low",\n     "risk": "Documentary priority rule; EIS acceptance document prevails over attached invoice/act",\n     "materiality_reason": "Supporting documents hierarchy rule with EIS document priority"},\n\n    {"contract_id": "8.5.2", "status": "extra_in_contract",\n     "contract_position": "Приемка может производиться только в присутствии представителя Исполнителя по его письменному уведомлению",\n     "risk_level": "low",\n     "risk": "Bank right to participate in acceptance; 15-day advance notice requirement is administratively burdensome",\n     "materiality_reason": "Bank representative participation right in acceptance with documented authority"},\n\n    {"contract_id": "8.5.3", "status": "extra_in_contract",\n     "contract_position": "При поступлении уведомления об участии в приемке в срок — приемка только в двустороннем порядке",\n     "risk_level": "low",\n     "risk": "Bilateral acceptance mandatory if Bank timely notifies; prevents unilateral Customer acceptance",\n     "materiality_reason": "Requires bilateral acceptance when Bank elects to participate"},\n\n    {"contract_id": "8.5.4", "status": "extra_in_contract",\n     "contract_position": "Если уведомление не поступило или поступило с опозданием — приемка Заказчиком в одностороннем порядке",\n     "risk_level": "low",\n     "risk": "Unilateral Customer acceptance if Bank fails to timely notify; low risk with proper processes",\n     "materiality_reason": "Unilateral acceptance if Bank misses 15-day notice deadline"},\n]\n\n# ============================================================\n# CONTRACT COVERAGE LEDGER\n# ============================================================\ncontract_ledger = [\n    ("1", "not_material", "Heading: предмет контракта"),\n    ("1.1", "linked", "Subject + appendices integral; linked via 2.4, 3.3, 11.7"),\n    ("1.2", "linked", "Volume by Customer need within max price; linked via 6.21"),\n    ("1.3", "linked", "Customer organizes card acceptance; linked via 3.1"),\n    ("2", "not_material", "Heading: термины и определения"),\n    ("2.1", "not_material", "Definition only"),\n    ("2.1.1", "not_material", "Definition only"),\n    ("2.1.2", "not_material", "Definition only"),\n    ("2.1.3", "not_material", "Definition only"),\n    ("2.1.4", "not_material", "Definition only"),\n    ("2.1.5", "not_material", "Definition only"),\n    ("2.1.6", "not_material", "Definition only"),\n    ("2.1.7", "not_material", "Definition only"),\n    ("2.1.8", "not_material", "Definition only"),\n    ("2.1.9", "not_material", "Definition only"),\n    ("2.1.10", "not_material", "Definition only"),\n    ("2.1.11", "not_material", "Definition only"),\n    ("2.1.12", "not_material", "Definition only"),\n    ("2.1.13", "not_material", "Definition only"),\n    ("2.1.14", "not_material", "Definition only"),\n    ("2.1.15", "not_material", "Definition only"),\n    ("2.1.16", "not_material", "Definition only"),\n    ("2.1.17", "not_material", "Definition only"),\n    ("2.1.18", "not_material", "Definition only"),\n    ("2.1.19", "not_material", "Definition only"),\n    ("2.1.20", "not_material", "Definition only"),\n    ("2.1.21", "not_material", "Definition only"),\n    ("2.1.22", "not_material", "Definition only"),\n    ("2.1.23", "not_material", "Definition only"),\n    ("2.1.24", "not_material", "Definition only"),\n    ("2.1.25", "not_material", "Definition only"),\n    ("2.1.26", "not_material", "Definition only"),\n    ("2.1.27", "not_material", "Definition only"),\n    ("2.1.28", "not_material", "Definition only"),\n    ("2.2", "not_material", "Descriptive definition of electronic terminal"),\n    ("2.3", "linked", "Document exchange chapeau + receipt rules; linked via 2.3.7"),\n    ("2.3.1", "linked", "Email exchange; linked via 2.3.1"),\n    ("2.3.2", "linked", "DBO exchange; linked via 2.3.2"),\n    ("2.3.3", "linked", "Courier; linked via 2.3.3"),\n    ("2.3.4", "linked", "Registered mail; linked via 2.3.4"),\n    ("2.3.5", "linked", "E-invoicing with UKEP; linked via 2.3.5"),\n    ("2.3.6", "linked", "EIS exchange; linked via 2.3.6"),\n    ("2.3.7", "linked", "Support service; linked via 2.3.7"),\n    ("3", "not_material", "Heading: цена контракта"),\n    ("3.1", "linked", "Max price 1 900 000 RUB; linked via 6.21"),\n    ("3.1.1", "linked", "Unit price in Specification; linked via 6.1"),\n    ("3.2", "linked", "Price includes Bank fee as %; linked via 3.3, 4.2.1, 6.1"),\n    ("3.3", "not_material", "44-FZ price reference; no independent operative effect"),\n    ("4", "not_material", "Heading: сроки, условия, порядок оплаты"),\n    ("4.1", "linked", "Service period + price exhaustion; linked via 10.1"),\n    ("4.2", "extra_in_contract", "Bank license requirement; reported as extra"),\n    ("4.3", "linked", "TST registration + terminal locations; linked via 2.1"),\n    ("4.4", "linked", "Payment procedure with treasury account; linked via 5.1.4, 2.2"),\n    ("4.5", "linked", "Payment within 7 working days; linked via 6.5"),\n    ("4.5.1", "extra_in_contract", "November deadline 30 Dec 2025; reported as extra"),\n    ("5", "not_material", "Heading: обязательства сторон"),\n    ("5.1", "not_material", "Subheading: Исполнитель обязуется"),\n    ("5.1.1", "linked", "Terminal install + instruction + training URL; linked via 5.2.3, 5.2.5"),\n    ("5.1.2", "linked", "Monthly EIS acceptance document; linked via 6.2"),\n    ("5.1.3", "linked", "Service per RF legislation; linked via 7.1"),\n    ("5.1.4", "linked", "24/7 operability + replacement 3 working days; linked via 5.2.7"),\n    ("5.1.5", "linked", "Full service info; linked via 5.1.16 context"),\n    ("5.1.6", "linked", "24/7 authorization; linked via 5.2.4"),\n    ("5.1.7", "linked", "Informational materials on terminals; linked via 5.2.6"),\n    ("5.1.8", "linked", "Transfer within 2 working days; linked via 5.2.8"),\n    ("5.1.9", "linked", "PDn processing per 152-FZ; linked via 5.2.10"),\n    ("5.1.10", "linked", "Transfer operation sums; linked via 3.2"),\n    ("5.2", "not_material", "Subheading: Исполнитель вправе"),\n    ("5.2.1", "linked", "Demand timely payment/acceptance; linked via 4.2.1"),\n    ("5.2.2", "linked", "Unilateral termination per 44-FZ/GK RF; linked via 10.2"),\n    ("5.2.3", "linked", "Inspect + replace terminals 2-day notice; linked via 5.1.6, 5.1.10"),\n    ("5.2.4", "linked", "Remote software update; linked via 5.1.6"),\n    ("5.2.5", "linked", "Request docs within 13 months; linked via 5.1.11"),\n    ("5.2.6", "linked", "Notify rekvizit changes 3 working days; linked via 5.1.13"),\n    ("5.2.7", "linked", "Operation-info requests to Customer email; linked via 5.1.14"),\n    ("5.2.8", "linked", "Demand docs for statutory functions; linked via 5.1.16"),\n    ("5.2.9", "linked", "Auth suspension/termination chapeau; linked via 5.1.8.1-13"),\n    ("5.2.9.1", "linked", "Customer breach ground; linked via 5.1.8.1"),\n    ("5.2.9.2", "linked", "Extremism/terrorism ground; linked via 5.1.8.2"),\n    ("5.2.9.3", "linked", "AML/CFT ground; linked via 5.1.8.3"),\n    ("5.2.9.4", "linked", "Negative info ground; linked via 5.1.8.6"),\n    ("5.2.9.5", "linked", "Fraud info ground; linked via 5.1.8.7"),\n    ("5.2.9.6", "linked", "Renovation ground; linked via 5.1.8.8"),\n    ("5.2.9.7", "linked", "Liquidation/bankruptcy ground; linked via 5.1.8.9"),\n    ("5.2.9.8", "linked", "False info ground; linked via 5.1.8.10"),\n    ("5.2.9.9", "linked", "Activity mismatch ground; linked via 5.1.8.11"),\n    ("5.2.9.10", "linked", "30-day inactivity ground; linked via 5.1.8.12"),\n    ("5.2.9.11", "linked", "Price exhaustion/term expiry ground; linked via 5.1.8.13"),\n    ("5.2.10", "linked", "Withholding right chapeau; linked via 5.1.1.1-6, 5.1.3"),\n    ("5.2.10.1", "linked", "Invalid operations withholding; linked via 5.1.1.1"),\n    ("5.2.10.2", "linked", "Erroneous transfer withholding; linked via 5.1.1.2"),\n    ("5.2.10.3", "linked", "Return/chargeback withholding; linked via 5.1.1.3"),\n    ("5.2.10.4", "linked", "Disputed operations withholding; linked via 5.1.1.4"),\n    ("5.2.10.5", "linked", "Penalty/loss withholding; linked via 5.1.1.5"),\n    ("5.3", "not_material", "Subheading: Заказчик обязуется"),\n    ("5.3.1", "linked", "Accept services per document; linked via 6.4"),\n    ("5.3.2", "linked", "Pay per contract; linked via 4.2.1"),\n    ("5.3.3", "extra_in_contract", "Control over Bank service delivery"),\n    ("5.3.4", "extra_in_contract", "Terminate if Bank fails procurement"),\n    ("5.3.5", "extra_in_contract", "Demand penalties from Bank"),\n    ("5.3.6", "extra_in_contract", "Reduce payment by tax amounts"),\n    ("5.3.7", "linked", "Place Bank info materials; linked via 4.2.4"),\n    ("5.3.8", "linked", "No splitting sums; linked via 4.2.6"),\n    ("5.3.9", "linked", "No card detail misuse; linked via 4.2.7"),\n    ("5.3.10", "linked", "Operations + documents per rules; linked via 4.2.9"),\n    ("5.3.11", "linked", "Store docs 13+ months; linked via 4.2.10"),\n    ("5.3.12", "linked", "Written statement of operations; linked via 4.2.11"),\n    ("5.3.13", "linked", "Notify Bank of changes 3 working days; linked via 4.2.14"),\n    ("5.3.14", "linked", "Reliable docs annually + 7 working days; linked via 4.2.15"),\n    ("5.3.15", "linked", "PDn transfer proof + indemnity; linked via 4.2.16.3"),\n    ("5.3.16", "linked", "Cease cards + remove materials; linked via 4.2.18"),\n    ("5.3.17", "linked", "Not obstruct checks + assist; linked via 4.2.19"),\n    ("5.3.18", "not_material", "Chapeau: торговый эквайринг"),\n    ("5.3.18.1", "linked", "Terminal use restrictions; linked via 4.2.20.2"),\n    ("5.3.18.2", "linked", "Access for terminal service; linked via 4.2.20.3"),\n    ("5.3.18.3", "linked", "Terminal acceptance act; linked via 4.2.20.4"),\n    ("5.3.20.4", "linked", "Immediate malfunction notice; linked via 4.2.20.5"),\n    ("5.3.18.5", "linked", "Return terminals 5 working days; linked via 4.2.20.6"),\n    ("5.3.19", "linked", "Reimburse Bank for disputed/loss; linked via 4.2.13"),\n    ("5.3.20", "linked", "Director PDn with guarantees; linked via 4.2.16.1"),\n    ("5.4", "not_material", "Subheading: Заказчик вправе"),\n    ("5.4.1", "linked", "Demand proper performance; linked via 7.1"),\n    ("5.4.2", "extra_in_contract", "Refuse acceptance for quality"),\n    ("5.4.3", "extra_in_contract", "Unilateral termination per 44-FZ/GK"),\n    ("5.4.4", "extra_in_contract", "Refuse payment + refund + damages"),\n    ("5.4.5", "linked", "Card reference with Bank approval; linked via 4.1.1"),\n    ("5.5", "linked", "Written statement 3 working days + loss notice; linked via 4.2.11"),\n    ("5.6", "linked", "Return terminals 5 working days; linked via 4.2.20.6"),\n    ("5.7", "linked", "Penalty for non-return; linked via 4.2.20.7, 5.1.1.6"),\n    ("5.9", "linked", "Consultation right; linked via 4.1.2"),\n    ("5.10", "linked", "Employee self-training; linked via 4.2.20.1"),\n    ("6", "not_material", "Heading: антикоррупционная оговорка"),\n    ("6.1", "linked", "Anti-corruption clause; linked via 7.16"),\n    ("7", "not_material", "Heading: ответственность сторон"),\n    ("7.1", "linked", "General liability + FM exemption + cap; linked via 7.1, 7.3"),\n    ("7.2", "linked", "Bank right to Customer penalties; linked via 7.2"),\n    ("7.3", "linked", "Customer delay penalty 1/300; linked via 7.4"),\n    ("7.4", "linked", "Customer штраф per PP 1042; linked via 7.2"),\n    ("7.4.1", "linked", "Customer штраф brackets; linked via 7.2"),\n    ("7.5", "linked", "Customer right to Bank penalties; linked via 7.4"),\n    ("7.6", "linked", "Bank delay penalty 1/300; linked via 7.4"),\n    ("7.7", "linked", "Bank штраф chapeau; linked via 7.5"),\n    ("7.7.1", "linked", "Bank штраф brackets; linked via 7.5"),\n    ("7.7.2", "linked", "Bank штраф above-NMCK winner; linked via 7.5"),\n    ("7.7.3", "linked", "Bank штраф non-pecuniary; linked via 7.6"),\n    ("7.8", "extra_in_contract", "EIS channel for penalty docs"),\n    ("7.9", "extra_in_contract", "Penalty does not release performance"),\n    ("7.10", "linked", "Bank штраф cap = price; linked via 7.7"),\n    ("7.11", "linked", "Customer штраф cap = price; linked via 7.3"),\n    ("7.12", "extra_in_contract", "Post-termination actual damages"),\n    ("8", "not_material", "Heading: качество, приемка, гарантия"),\n    ("8.1", "linked", "Quality per Technical Assignment; linked via 7.1"),\n    ("8.2", "extra_in_contract", "Bank liability for specialist damages"),\n    ("8.3", "not_material", "Chapeau: приемка per law and contract"),\n    ("8.3.1", "linked", "Monthly EIS doc by 10th working day; linked via 6.2"),\n    ("8.3.2", "extra_in_contract", "Supporting docs hierarchy"),\n    ("8.4", "linked", "Receipt date = EIS posting; linked via 6.4"),\n    ("8.5", "linked", "10 working days for sign/refuse; linked via 6.4"),\n    ("8.5.1", "linked", "Sign or motivated refusal; linked via 6.4"),\n    ("8.5.2", "extra_in_contract", "Bank rep participation right"),\n    ("8.5.3", "extra_in_contract", "Bilateral acceptance if Bank notifies"),\n    ("8.5.4", "extra_in_contract", "Unilateral if Bank misses deadline"),\n    ("8.5.5", "extra_in_contract", "Mandatory Customer expert review"),\n    ("8.5.6", "extra_in_contract", "External expert engagement"),\n    ("8.5.7", "linked", "Sign within 10 working days if no objections; linked via 6.4"),\n    ("8.5.8", "extra_in_contract", "Commission procedure"),\n    ("8.5.9", "extra_in_contract", "Bank right to cure + resubmit"),\n    ("8.6", "extra_in_contract", "Acceptance date = EIS posting signed doc"),\n    ("8.7", "extra_in_contract", "Correction via EIS"),\n    ("8.8", "not_material", "Reference to section procedure"),\n    ("8.9", "extra_in_contract", "Accept despite curable non-conformity"),\n    ("8.10", "extra_in_contract", "Cure defects 3 days free"),\n    ("8.11", "linked", "Signed doc = payment basis; linked via 6.4"),\n    ("9", "not_material", "Heading: обстоятельства непреодолимой силы"),\n    ("9.1", "linked", "FM definition + examples; linked via 8.1"),\n    ("9.2", "linked", "FM notice 5 days + termination 1 month; linked via 8.2"),\n    ("9.3", "extra_in_contract", "FM documentary proof"),\n    ("10", "not_material", "Heading: порядок разрешения споров"),\n    ("10.1", "linked", "Pre-trial + 10-day response + notices; linked via 9.1, 9.2, 11.12"),\n    ("10.2", "linked", "Arbitration Krasnodar Krai; linked via 9.3"),\n    ("11", "not_material", "Heading: срок действия, изменение, расторжение"),\n    ("11.1", "linked", "Term to 30.12.2025 + survival; linked via 10.1, 10.3"),\n    ("11.2", "linked", "Written amendments both sign; linked via 11.4"),\n    ("11.3", "linked", "Termination by agreement/court/unilateral; linked via 10.2"),\n    ("11.4", "linked", "Customer unilateral per GK RF; linked via 10.2"),\n    ("11.5", "linked", "Unilateral per 44-FZ Art.95; linked via 10.2"),\n    ("11.6", "extra_in_contract", "44-FZ framework for changes"),\n    ("11.7", "linked", "RF law for uncovered matters; linked via 11.5"),\n    ("11.8", "extra_in_contract", "No material changes except per 44-FZ"),\n    ("12", "not_material", "Heading: прочие условия"),\n    ("12.1", "linked", "No Executor substitution; linked via 11.9, 11.10"),\n    ("12.2", "linked", "Customer succession; linked via 11.9, 11.10"),\n    ("12.3", "extra_in_contract", "Improved characteristics permitted"),\n    ("12.4", "linked", "Electronic form UKEP; linked via 2.7, 11.6"),\n    ("12.5", "linked", "Appendix list; linked via 2.4, 11.7, 11.13"),\n    ("13", "not_material", "Signatures and bank details"),\n    ("Technical Assignment", "linked", "Technical Assignment as integral part"),\n    ("Technical Assignment p.3", "linked", "Accepted card systems list; linked via 3.1, 4.2.5"),\n    ("Technical Assignment p.5", "linked", "Settlement RUB + return fee rule; linked via 2.2, 6.20"),\n    ("Specification", "linked", "Price specification; linked via 3.3, 6.1"),\n    ("Приложение 1.1", "linked", "Customer application + direct debit consent; linked via 5.1.3"),\n    ("Приложение 1.2", "not_material", "TST Info blank form template"),\n    ("Приложение 2", "not_material", "Specification form — covered via Specification ref"),\n]\n\n# ============================================================\n# ASSEMBLE AND WRITE\n# ============================================================\n\noutput = {\n    "analysis_profile": profile,\n    "links": links,\n    "unmatched_matrix": unmatched_matrix,\n    "unmatched_contract": unmatched_contract,\n    "coverage_ledger": {\n        "matrix": [{"matrix_id": m[0], "closure": m[1], "reason": m[2]} for m in matrix_rows],\n        "contract": [{"contract_id": c[0], "closure": c[1], "reason": c[2]} for c in contract_ledger]\n    },\n    "summary": {\n        "aligned_count": sum(1 for l in links if l["relationship"] == "aligned"),\n        "deviation_count": sum(1 for l in links if l["relationship"] == "deviation"),\n        "missing_in_contract_count": len(unmatched_matrix),\n        "extra_in_contract_count": len(unmatched_contract)\n    }\n}\n\nwith open("outputs/discrepancy_analysis.json", "w", encoding="utf-8") as f:\n    json.dump(output, f, ensure_ascii=False, indent=2)\n\nprint(f"Written outputs/discrepancy_analysis.json")\nprint(f"Links: {len(links)} total ({output[\'summary\'][\'aligned_count\']} aligned, {output[\'summary\'][\'deviation_count\']} deviation)")\nprint(f"Missing in contract: {output[\'summary\'][\'missing_in_contract_count\']}")\nprint(f"Extra in contract: {output[\'summary\'][\'extra_in_contract_count\']}")\nprint(f"Matrix ledger rows: {len(matrix_rows)}")\nprint(f"Contract ledger rows: {len(contract_ledger)}")\nprint(f"out_of_scope: {sum(1 for m in matrix_rows if m[1] == \'out_of_scope\')}")\nprint(f"not_applicable: {sum(1 for m in matrix_rows if m[1] == \'not_applicable\')}")\n', 'file_path': 'outputs/working/build_analysis.py'}, 'id': 'call_00_QyBlcDuHwakMRjcT8r339271', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/build_analysis.py
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/build_analysis.py'}, 'id': 'call_00_1R9P9qhNrbouWr8g2Fqt6094', 'type': 'tool_call'}]
Tool: Written outputs/discrepancy_analysis.json
Links: 99 total (83 aligned, 16 deviation)
Missing in contract: 34
Extra in contract: 29
Matrix ledger rows: 169
Contract ledger rows: 203
out_of_scope: 36
not_applicable: 0

[Command succeeded with exit code 0]
AI: Now let me run comprehensive verification checks:[{'name': 'write_file', 'args': {'content': '#!/usr/bin/env python3\n"""Verify the output JSON against all quality checks from the skill."""\nimport json\n\nwith open("outputs/discrepancy_analysis.json", encoding="utf-8") as f:\n    data = json.load(f)\n\nerrors = []\n\n# Check 1: Every source matrix id is closed once\nmatrix_ids_in_ledger = [m["matrix_id"] for m in data["coverage_ledger"]["matrix"]]\nfrom collections import Counter\ncounts = Counter(matrix_ids_in_ledger)\ndups = {k: v for k, v in counts.items() if v > 1}\nif dups:\n    errors.append(f"Duplicate matrix_ids in ledger: {dups}")\n\n# Check 2: Every linked matrix id appears in links\nlinked_matrix_ids = set(m["matrix_id"] for m in data["coverage_ledger"]["matrix"] if m["closure"] == "linked")\nlink_matrix_ids = set()\nfor l in data["links"]:\n    for mid in l["matrix_ids"]:\n        link_matrix_ids.add(mid)\nmissing_from_links = linked_matrix_ids - link_matrix_ids\nif missing_from_links:\n    errors.append(f"Matrix ids in ledger as linked but not in links: {missing_from_links}")\n\n# Check 3: Every missing_in_contract matrix id appears in unmatched_matrix\nmissing_ids_ledger = set(m["matrix_id"] for m in data["coverage_ledger"]["matrix"] if m["closure"] == "missing_in_contract")\nmissing_ids_report = set(m["matrix_id"] for m in data["unmatched_matrix"])\nextra_in_report = missing_ids_report - missing_ids_ledger\nmissing_from_report = missing_ids_ledger - missing_ids_report\nif extra_in_report:\n    errors.append(f"Matrix ids in unmatched_matrix but not in ledger as missing: {extra_in_report}")\nif missing_from_report:\n    errors.append(f"Matrix ids in ledger as missing but not in unmatched_matrix: {missing_from_report}")\n\n# Check 4: No matrix id is both linked and missing\nif linked_matrix_ids & missing_ids_ledger:\n    errors.append(f"Matrix ids both linked and missing: {linked_matrix_ids & missing_ids_ledger}")\n\n# Check 5: Every linked contract id appears in links\nlinked_contract_ids = set(c["contract_id"] for c in data["coverage_ledger"]["contract"] if c["closure"] == "linked")\nlink_contract_ids = set()\nfor l in data["links"]:\n    for cid in l["contract_ids"]:\n        link_contract_ids.add(cid)\ncontract_missing_from_links = linked_contract_ids - link_contract_ids\nif contract_missing_from_links:\n    errors.append(f"Contract ids in ledger as linked but not in links: {contract_missing_from_links}")\n\n# Check 6: Every extra contract id appears in unmatched_contract\nextra_ids_ledger = set(c["contract_id"] for c in data["coverage_ledger"]["contract"] if c["closure"] == "extra_in_contract")\nextra_ids_report = set(c["contract_id"] for c in data["unmatched_contract"])\nextra_diff = extra_ids_ledger ^ extra_ids_report\nif extra_diff:\n    errors.append(f"Mismatch between ledger extra and unmatched_contract: {extra_diff}")\n\n# Check 7: Every aligned link has empty discrepancies\nfor l in data["links"]:\n    if l["relationship"] == "aligned" and l["discrepancies"]:\n        errors.append(f"Aligned link has discrepancies: {l[\'matrix_ids\']} -> {l[\'contract_ids\']}")\n\n# Check 8: Every deviation has at least one named discrepancy\nfor l in data["links"]:\n    if l["relationship"] == "deviation" and not l["discrepancies"]:\n        errors.append(f"Deviation link has no discrepancies: {l[\'matrix_ids\']} -> {l[\'contract_ids\']}")\n\n# Check 9: Summary counts match\nsummary = data["summary"]\nactual_aligned = sum(1 for l in data["links"] if l["relationship"] == "aligned")\nactual_deviation = sum(1 for l in data["links"] if l["relationship"] == "deviation")\nactual_missing = len(data["unmatched_matrix"])\nactual_extra = len(data["unmatched_contract"])\n\nif summary["aligned_count"] != actual_aligned:\n    errors.append(f"Aligned count mismatch: summary={summary[\'aligned_count\']}, actual={actual_aligned}")\nif summary["deviation_count"] != actual_deviation:\n    errors.append(f"Deviation count mismatch: summary={summary[\'deviation_count\']}, actual={actual_deviation}")\nif summary["missing_in_contract_count"] != actual_missing:\n    errors.append(f"Missing count mismatch: summary={summary[\'missing_in_contract_count\']}, actual={actual_missing}")\nif summary["extra_in_contract_count"] != actual_extra:\n    errors.append(f"Extra count mismatch: summary={summary[\'extra_in_contract_count\']}, actual={actual_extra}")\n\n# Check 10: No not_material clause with operative effect sneaking into extra\n# (This would need manual review; we\'ll flag suspicious patterns)\nfor c in data["unmatched_contract"]:\n    cid = c["contract_id"]\n    if not c.get("materiality_reason"):\n        errors.append(f"Extra contract {cid} missing materiality_reason")\n\n# Check 11: out_of_scope rows have source-based reason\nfor m in data["coverage_ledger"]["matrix"]:\n    if m["closure"] in ("out_of_scope", "not_applicable"):\n        if not m["reason"] or len(m["reason"]) < 10:\n            errors.append(f"Matrix {m[\'matrix_id\']} marked {m[\'closure\']} with insufficient reason: {m.get(\'reason\')}")\n\n# Check 12: Verify total matrix count = 169\nif len(data["coverage_ledger"]["matrix"]) != 169:\n    errors.append(f"Matrix ledger has {len(data[\'coverage_ledger\'][\'matrix\'])} rows, expected 169")\n\n# Check 13: relationship is only aligned or deviation\nfor l in data["links"]:\n    if l["relationship"] not in ("aligned", "deviation"):\n        errors.append(f"Invalid relationship: {l[\'relationship\']} for {l[\'matrix_ids\']}")\n\n# Check 14: No extra_in_contract items in links\nfor l in data["links"]:\n    if l["relationship"] == "extra_in_contract":\n        errors.append(f"Extra item in links: {l}")\n\n# Print results\nif errors:\n    print("VERIFICATION ERRORS FOUND:")\n    for e in errors:\n        print(f"  - {e}")\nelse:\n    print("ALL VERIFICATION CHECKS PASSED")\n\nprint(f"\\nSummary:")\nprint(f"  Matrix ledger: {len(data[\'coverage_ledger\'][\'matrix\'])} rows")\nprint(f"    linked: {sum(1 for m in data[\'coverage_ledger\'][\'matrix\'] if m[\'closure\'] == \'linked\')}")\nprint(f"    missing: {sum(1 for m in data[\'coverage_ledger\'][\'matrix\'] if m[\'closure\'] == \'missing_in_contract\')}")\nprint(f"    out_of_scope: {sum(1 for m in data[\'coverage_ledger\'][\'matrix\'] if m[\'closure\'] == \'out_of_scope\')}")\nprint(f"    not_applicable: {sum(1 for m in data[\'coverage_ledger\'][\'matrix\'] if m[\'closure\'] == \'not_applicable\')}")\nprint(f"  Contract ledger: {len(data[\'coverage_ledger\'][\'contract\'])} rows")\nprint(f"    linked: {sum(1 for c in data[\'coverage_ledger\'][\'contract\'] if c[\'closure\'] == \'linked\')}")\nprint(f"    extra: {sum(1 for c in data[\'coverage_ledger\'][\'contract\'] if c[\'closure\'] == \'extra_in_contract\')}")\nprint(f"    not_material: {sum(1 for c in data[\'coverage_ledger\'][\'contract\'] if c[\'closure\'] == \'not_material\')}")\nprint(f"  Links: {len(data[\'links\'])} ({data[\'summary\'][\'aligned_count\']} aligned, {data[\'summary\'][\'deviation_count\']} deviation)")\nprint(f"  Unmatched matrix: {len(data[\'unmatched_matrix\'])}")\nprint(f"  Unmatched contract: {len(data[\'unmatched_contract\'])}")\n', 'file_path': 'outputs/working/verify.py'}, 'id': 'call_00_xa1Hi1lR2Gd23lU5oUA96170', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/verify.py
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/verify.py'}, 'id': 'call_00_ET_iMn0RxVGVZBGJDRH9CoH3344', 'type': 'tool_call'}]
Tool: VERIFICATION ERRORS FOUND:
  - Contract ids in ledger as linked but not in links: {'11.4', '3.1.1', '7.7.2', '7.2', '5.3.1', '5.4.1', '8.11', '5.3.12', '5.1.2', '1.2', '5.2.1', '5.2.2', '5.3.2', '5.2.6', '7.3', 'Technical Assignment', '5.1.5', '8.4', '5.1.3', '8.1'}

Summary:
  Matrix ledger: 169 rows
    linked: 99
    missing: 34
    out_of_scope: 36
    not_applicable: 0
  Contract ledger: 203 rows
    linked: 121
    extra: 29
    not_material: 53
  Links: 99 (83 aligned, 16 deviation)
  Unmatched matrix: 34
  Unmatched contract: 29

[Command succeeded with exit code 0]

