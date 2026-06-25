## Summarized at 2026-06-25T08:42:04.840908+00:00

Human: Contract extra review
AI: I'll start by reading the skill file and understanding the task structure, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_NTSQ5w3KI9Jj3RXzSRgu2388', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/'}, 'id': 'call_01_Rhps3Rtopxl3pUr6feqy0289', 'type': 'tool_call'}]
Tool:      1	---
     2	name: acquiring-discrepancy-analysis
     3	description: "Use this skill when comparing a bank acquiring standard matrix with a counterparty acquiring contract to find many-to-many legal correspondences, deviations, missing bank-standard requirements, and material extra contract terms."
     4	---
     5	
     6	# Acquiring Discrepancy Analysis
     7	
     8	Use this skill for legal discrepancy analysis between a standard bank acquiring
     9	matrix and a counterparty acquiring contract.
    10	
    11	## Purpose
    12	
    13	Build a many-to-many legal comparison map:
    14	
    15	- which bank-standard requirements are preserved by the contract;
    16	- which contract terms deviate from the bank standard;
    17	- which matrix requirements are absent from the contract;
    18	- which material contract terms have no matrix analogue.
    19	
    20	The matrix is the Bank's standard. The contract is assessed against that
    21	standard. The documents are not equal sources of policy.
    22	
    23	## Inputs
    24	
    25	- `inputs/matrix.json`: bank standard matrix. Use `number` as the matrix id.
    26	  Analyze `main_idea`, `topics`, and `enriched_text` as the legal requirement.
    27	- `inputs/contract.txt`: counterparty contract text. Use exact printed clause
    28	  ids when available. If a provision has no printed number, use the exact
    29	  heading, definition label, appendix/table row label, or nearest real locator
    30	  from the document; do not invent numbering.
    31	- `/outputs/discrepancy_analysis.json`: the only final output. Treat this as an
    32	  absolute virtual path rooted at the project workspace.
    33	- `/outputs/working/`: required working area for temporary batch fragments,
    34	  helper scripts, notes, checks, and intermediate files.
    35	
    36	Before writing the final artifact, read `references/output-contract.md`.
    37	Use `references/comparison-patterns.md` when calibrating uncertain relationship
    38	or materiality calls.
    39	
    40	## Required Working Artifacts
    41	
    42	Before comparing the documents, create these working files:
    43	
    44	- `/outputs/working/matrix_inventory.json`
    45	- `/outputs/working/contract_inventory.json`
    46	- optional compact batch fragments under `/outputs/working/`
    47	
    48	Each inventory entry must contain:
    49	
    50	- `id`: exact matrix `number` or exact contract locator as written;
    51	- `proposition`: short legal proposition;
    52	- `party`: party protected or bound by the proposition, if identifiable;
    53	- `right_or_obligation`: operative right, obligation, prohibition, permission,
    54	  or allocation of risk;
    55	- `object`: legal object affected by the proposition;
    56	- `trigger`: event or condition that activates the proposition, if present;
    57	- `material_terms`: deadline, amount, formula, procedure, liability, penalty,
    58	  cap, exception, or consequence, if present;
    59	- `applicability`: `in_scope`, `out_of_scope`, `conditional`, or `unknown`;
    60	- `applicability_reason`: product, channel, terminal, party role, legal regime,
    61	  or document scope reason for the applicability call;
    62	- `materiality`: `material`, `technical`, or `heading`.
    63	
    64	Do not start the many-to-many comparison until both inventories exist. The
    65	inventories are legal working tables, not final deliverables.
    66	
    67	Keep inventories compact. Do not copy full clause text into inventory entries
    68	unless the text is needed to identify an unnumbered locator. The inventory is an
    69	index for coverage and ids, not the legal memo.
    70	
    71	Contract locator discipline:
    72	
    73	- final `contract_ids` must be exact printed locators from `inputs/contract.txt`;
    74	- do not use internal aliases such as `Appendix_1`, `app_1`, or translated
    75	  labels in the final artifact;
    76	- if a script needs aliases, store them in an `aliases` field, but keep `id` as
    77	  the printed locator;
    78	- never cite a parenthetical locator unless the parenthetical text is printed in
    79	  the contract.
    80	- the inventory cannot make a locator real. Before using an appendix, form,
    81	  table, or unnumbered paragraph as a final `contract_id`, verify that the same
    82	  locator text appears in `inputs/contract.txt`. If it does not, cite the
    83	  nearest real printed clause that incorporates or describes that text and put
    84	  the appendix/form detail in `coverage` or `contract_position`.
    85	- do not create final locators by subdividing a printed appendix, heading, or
    86	  parent clause unless that subdivision is printed in the contract text itself.
    87	
    88	## Legal Comparison Principles
    89	
    90	- Compare legal propositions, not numbering, order, or isolated words.
    91	- A proposition is material when it changes rights, duties, triggers, deadlines,
    92	  amounts, formulas, liability, procedures, scope, parties, exceptions, or
    93	  consequences.
    94	- The first question is applicability. A matrix requirement outside the
    95	  contract's product, channel, terminal type, party role, or legal regime is not
    96	  a weak `deviation`; it is normally `missing_in_contract` unless the contract
    97	  contains an operative analogue for that exact legal object.
    98	- One matrix requirement may be covered by several contract provisions.
    99	- One contract provision may cover several matrix requirements.
   100	- A package can be `aligned` even if no single clause covers the whole standard,
   101	  provided the linked clauses together preserve the legal result.
   102	- Grouped package result and atomic pair role are different. A grouped package
   103	  may be `aligned` because several clauses work together. An atomic row records
   104	  what one exact contract locator contributes to one matrix item; it must not
   105	  pretend that every locator in the package independently covers the whole
   106	  matrix item.
   107	- A package is `deviation` when there is an analogue but any material element is
   108	  changed, narrowed, weakened, omitted, or shifted against the Bank.
   109	- Any material difference from the Bank standard in deadline, amount, formula,
   110	  protected party, trigger, scope, procedure, liability, Bank right, merchant
   111	  obligation, exception, or consequence is a `deviation`.
   112	- A matrix requirement is `missing_in_contract` when no strong legal analogue
   113	  covers the same protected party, legal object, operative right or duty,
   114	  trigger or condition, and legal consequence.
   115	- Generic clauses about payment, notices, electronic documents, inspections,
   116	  confidentiality, compliance, or liability do not satisfy a specific Bank
   117	  standard unless they preserve the same protected party, legal object, trigger,
   118	  procedure, and consequence.
   119	- Weak thematic similarity is not enough for a link. If a clause is only from
   120	  the same broad area but does not pass the legal analogue threshold, keep the
   121	  matrix item in `unmatched_matrix` and record the rejected weak candidate
   122	  there.
   123	- Do not create a `deviation` link with empty `contract_ids`. If no useful
   124	  contract locator exists, the matrix item belongs in `unmatched_matrix`.
   125	- Do not force every matrix item into `links`. A real absence from the contract
   126	  is a required finding, not a failure to be hidden.
   127	- A contract provision is `extra_in_contract` when it has independent legal
   128	  effect and no matrix analogue.
   129	- Use `not_material` for administrative headings, recitals, party details,
   130	  definitions without operative effect, technical formatting, and service text
   131	  that creates no standalone legal risk.
   132	
   133	Full preservation is allowed when the difference is only formal:
   134	
   135	- blank placeholders or fields intended to be filled later;
   136	- one selected option from alternatives allowed by the standard;
   137	- different document label or appendix title with the same legal effect;
   138	- mandatory law provides the same or stronger result and the contract does not
   139	  waive or narrow it.
   140	
   141	Mandatory-law and procurement structures are not automatically formal. If
   142	Federal Law No. 44-FZ, public-system acceptance, customer approval, budget
   143	payment, statutory penalty, or unilateral customer termination governs the same
   144	legal object as the matrix but changes the Bank's right, payment path,
   145	acceptance condition, deadline, remedy, termination procedure, or control over
   146	performance, classify the true analogue as `deviation`. Use `aligned` only when
   147	the statutory structure preserves the same or stronger legal result for the
   148	Bank.
   149	
   150	## Legal Analogue Threshold
   151	
   152	Create a link only after testing these elements:
   153	
   154	- `protected_party`: who receives the right, protection, payment, remedy, or
   155	  procedural advantage;
   156	- `bound_party`: who bears the duty, restriction, liability, or burden;
   157	- `legal_object`: what transactions, terminal, channel, data, service, payment,
   158	  document, breach, or relationship the provision regulates;
   159	- `operative_act`: the actual right, duty, prohibition, permission, remedy, or
   160	  allocation of risk;
   161	- `trigger`: the event or condition that activates the provision;
   162	- `consequence`: payment, refusal, deduction, suspension, termination, evidence
   163	  effect, penalty, liability, approval, rejection, or other legal result.
   164	
   165	Classify the analogue strength before linking:
   166	
   167	- `strong`: same legal object and same operative legal result, with only
   168	  details left to compare;
   169	- `partial`: same legal object and operative area, but one material element is
   170	  narrower, weaker, changed, or incomplete;
   171	- `weak_context`: same broad topic only, adjacent procedure, background,
   172	  framework, appendix, or generic right without the same operative result.
   173	
   174	Only `strong` and `partial` analogues may appear in `links` and
   175	`atomic_links`. `weak_context` candidates must be rejected into
   176	`unmatched_matrix[].rejected_candidates` or used only as explanatory context.
   177	This is the main guard against false `deviation` findings.
   178	
   179	Use `missing_in_contract` instead of `deviation` when the contract contains:
   180	
   181	- generic payment text but not the Bank-standard settlement, deduction, fee,
   182	  holdback, or reconciliation mechanism;
   183	- generic notice or document exchange but not the named channel, evidentiary
   184	  effect, deadline, or delivery procedure required by the matrix;
   185	- generic inspection, acceptance, or request rights but not the same fraud,
   186	  issuer verification, profile, terminal, or payment-system control;
   187	- generic liability but not the specific trigger, protected party, amount,
   188	  formula, cap, exception, or remedy;
   189	- an appendix, form, table, heading, or framework clause that does not itself
   190	  set the operative right, duty, amount, deadline, scope, or consequence.
   191	- a generic QR display, terminal capability, card acceptance, contactless
   192	  payment, inspection, or request clause but not the same named Bank product,
   193	  channel, risk-control mechanism, or operational consequence.
   194	
   195	## Material Element Checklist
   196	
   197	For every linked group and every atomic pair, check the material elements below.
   198	Use these fixed results: `same`, `equivalent`, `different`, `missing`,
   199	`not_applicable`.
   200	
   201	- `party`
   202	- `legal_object`
   203	- `operative_right_or_duty`
   204	- `trigger`
   205	- `deadline`
   206	- `amount_formula_cap`
   207	- `procedure_channel`
   208	- `liability_remedy`
   209	- `scope_exceptions`
   210	- `consequence`
   211	
   212	Rules:
   213	
   214	- `aligned` requires every material element to be `same`, `equivalent`, or
   215	  `not_applicable`.
   216	- `deviation` requires at least one material element to be `different` or
   217	  `missing`, and the provision must first pass the legal analogue threshold.
   218	- each `different` or `missing` item must be evidenced in side-by-side form:
   219	  `matrix: ...; contract: ...; gap: ...`. Keep the text short, but make the
   220	  changed legal element explicit.
   221	- If any checklist item is `different` or `missing`, the relationship must be
   222	  `deviation` and `discrepancies` must be non-empty. Do not write `aligned` with
   223	  a checklist gap and then explain the gap only in `status_reason`.
   224	- If `discrepancies`, `status_reason`, or `coverage` says an element is absent,
   225	  incomplete, weaker, narrower, or changed, the same element must be marked
   226	  `missing` or `different` in `element_checklist`.
   227	- Never return a `deviation` pair whose checklist contains only `same`,
   228	  `equivalent`, and `not_applicable`.
   229	- If no material element can be named as `different` or `missing`, do not use
   230	  `deviation`.
   231	- Do not mark `deviation` because of document title, appendix label, placeholder
   232	  text, selected allowed option, or mandatory-law structure when the Bank's
   233	  legal result is preserved.
   234	
   235	## Workflow
   236	
   237	1. Read the full matrix and full contract.
   238	2. Build `/outputs/working/matrix_inventory.json`. Include every matrix item and
   239	   classify each as `material`, `technical`, or `heading`.
   240	3. Build `/outputs/working/contract_inventory.json`. Include every printed
   241	   clause, operative heading, definition with legal effect, appendix/table row,
   242	   and unnumbered provision that may affect rights or duties.
   243	4. Split material matrix ids into 3-5 batches and use `task` for substantive
   244	   batch analysis when the harness provides it. The orchestrator may prepare
   245	   inventories and merge results, but should not perform the full legal review
   246	   alone.
   247	5. For each material matrix proposition, perform candidate recall before
   248	   deciding absence:
   249	   - direct clause with the same legal object;
   250	   - parent or framework clause;
   251	   - child or detail clause;
   252	   - appendix, table, tariff, form, or definition;
   253	   - payment, procedure, liability, notice, termination, or survival companion;
   254	   - clause referenced by `clause`, `section`, `appendix`, `rules`, or similar
   255	     cross-reference language.
   256	6. Apply parent/child recall:
   257	   - if a child/detail clause is found, check the parent clause;
   258	   - if a parent/framework clause is found, check its children;
   259	   - if a clause points to an appendix or another section, check that referenced
   260	     locator when it sets scope, deadline, amount, procedure, liability, or
   261	     consequence.
   262	7. Apply the applicability and legal analogue threshold:
   263	   - reject weak-context candidates before creating a link;
   264	   - if every candidate is weak-context only, add the matrix item to
   265	     `unmatched_matrix` with the rejected candidates and reasons;
   266	   - if the matrix item is outside the contract's product, channel, terminal, or
   267	     legal regime and no operative analogue exists, use `missing_in_contract`.
   268	   - if a mandatory-law or procurement clause regulates the same legal object
   269	     but changes the mechanism, treat it as a candidate analogue and evaluate
   270	     `deviation` rather than dropping it as unrelated.
   271	8. Build relationship groups by legal meaning:
   272	   - link all matrix ids and contract ids that form one legal package;
   273	   - include parent, child, appendix, table, definition, and cross-reference
   274	     locators only when they materially affect the legal result;
   275	   - ignore numbering similarity unless the legal proposition also matches.
   276	9. For each linked group, decide whether the contract preserves the bank
   277	   standard:
   278	   - `aligned`: no material legal gap remains after reading the package;
   279	   - `deviation`: at least one material gap remains.
   280	10. Build `atomic_links` from the relationship groups. For each exact
   281	   `matrix_id` + `contract_id` pair that has a legal coverage relation:
   282	   - add one atomic row;
   283	   - state what that exact contract clause covers;
   284	   - state `coverage_role` and `analogue_strength`;
   285	   - include `element_checklist`;
   286	   - use the pair relationship that follows from that exact clause's legal
   287	     contribution; do not borrow coverage from unrelated clauses, but do not
   288	     automatically downgrade parent, child, or appendix clauses when they are a
   289	     necessary part of an aligned package and have no changed material element;
   290	   - do not create a Cartesian product from grouped ids. Add only real legal
   291	     pairs.
   292	11. Add every uncovered matrix item to `unmatched_matrix`.
   293	12. Run a contract-only review over the full `contract_inventory`. Each material
   294	   contract item must be classified as:
   295	   - `linked` when it appears in a relationship group;
   296	   - `extra_in_contract` when it has independent legal effect and no matrix
   297	     analogue;
   298	   - `not_material` only when it creates no standalone legal risk.
   299	13. During contract-only review, deliberately check for:
   300	   - procurement and mandatory-law mechanics, including Federal Law No. 44-FZ;
   301	   - electronic acceptance, acceptance in state systems, or customer acceptance
   302	     procedures;
   303	   - customer rights to inspect, reject, demand correction, suspend, or control
   304	     performance;
   305	   - price source, maximum price, budget/payment source, or settlement
   306	     mechanics;
   307	   - unilateral customer termination or convenience exit rights;
   308	   - reporting, act-signing, evidence, or document-exchange procedures.
   309	   When a parent section is material, sweep its operative child clauses. Report
   310	   child clauses that create their own right, duty, procedure, payment
   311	   condition, remedy, rejection right, correction duty, or termination effect.
   312	   Do not expand this into a heading inventory: omit headings and repeat-only
   313	   children that add no independent legal effect.
   314	14. Run the final QA checklist and write one JSON object to
   315	   `/outputs/discrepancy_analysis.json`.
   316	
   317	## Tool Use Discipline
   318	
   319	- Helper scripts are allowed for deterministic parsing, inventory creation,
   320	  schema checks, coverage checks, merge, and summary counts.
   321	- In shell commands, use workspace-relative paths such as `outputs/working/...`.
   322	  Treat `/outputs/...` as a virtual artifact path for the agent file tools, not
   323	  as a portable shell path. Do not spend turns debugging path errors caused by
   324	  mixing these conventions.
   325	- Do not encode substantive legal conclusions as a giant hardcoded script or a
   326	  table of hundreds of ids inside Python code. Put legal conclusions in JSON
   327	  fragments and merge those fragments.
   328	- Do not create multiple competing full artifacts. Draft fragments belong under
   329	  `/outputs/working/`; only the merged result goes to
   330	  `/outputs/discrepancy_analysis.json`.
   331	- Use at most one inventory script, one merge script, and one QA script. Use at
   332	  most one QA correction cycle. If QA finds defects, fix concrete defects once,
   333	  re-run a targeted validation, then finish. Do not keep launching new broad
   334	  revalidation scripts or agents.
   335	
   336	## Status Gates
   337	
   338	- `Aligned Package Rule`: several contract clauses may jointly satisfy one Bank
   339	  standard when the package preserves every material element.
   340	- `Atomic Pair Rule`: every final legal pair must be represented as one
   341	  `atomic_links` row. Pair status is evaluated for the exact matrix item and
   342	  exact contract locator, with `coverage_role`, `analogue_strength`, and a
   343	  material element checklist.
   344	- `No Cross-Clause Status Lifting`: do not mark a weak or unrelated clause
   345	  `aligned` merely because another clause in the package is strong. Also do not
   346	  mark a necessary parent, child, appendix, or procedure clause `deviation`
   347	  merely because it covers only its own part of an otherwise aligned package.
   348	  A pair needs a named material difference for `deviation`.
   349	- `Deviation Rule`: changed deadline, amount, formula, party, trigger, scope,
   350	  procedure, liability, Bank right, merchant obligation, exception, or
   351	  consequence is a deviation.
   352	- `Procurement Mechanism Rule`: 44-FZ, EIS, customer acceptance, budget payment,
   353	  statutory penalties, or public-contract termination can be a legal analogue
   354	  when it regulates the same obligation or remedy. Mark `deviation` if that
   355	  mechanism changes timing, payment, acceptance, control, remedy, termination,
   356	  or enforcement compared with the Bank standard.
   357	- `Missing Beats Weak Deviation`: a weak-context or merely thematic candidate
   358	  is not a legal analogue. Reject it and use `missing_in_contract` rather than
   359	  creating a false `deviation`.
   360	- `Generic Is Not Specific`: a generic clause is not enough for a named Bank
   361	  channel, fraud mechanism, card-system duty, terminal fee, electronic document
   362	  procedure, special liability trigger, or specific Bank remedy.
   363	- `No Formal Deviation`: do not mark deviation for a label, heading, appendix
   364	  title, placeholder, chosen allowed option, or mandatory-law structure when the
   365	  legal result for the Bank is preserved.
   366	- `Named Gap Required`: every `deviation` must identify the changed legal
   367	  element. If the gap cannot be named, re-check whether the package is actually
   368	  `aligned`.
   369	- `Contract-Only Materiality Gate`: `not_material` is limited to headings,
   370	  recitals, signatures, blank forms, administrative details, and definitions
   371	  without operative effect. Acceptance, public-system procedure, customer
   372	  control, rejection, correction, withholding, payment, termination, reporting,
   373	  evidence, liability, and mandatory-law mechanics are normally
   374	  `extra_in_contract` when they have no matrix analogue.
   375	
   376	## File Discipline
   377	
   378	- Write the final result only to `/outputs/discrepancy_analysis.json`.
   379	- Use `/outputs/working/` for intermediate artifacts, helper scripts,
   380	  validation notes, batch files, and calculations.
   381	- Treat files under `/outputs/working/` as working material, not final output.
   382	- The final answer must be assembled into `/outputs/discrepancy_analysis.json`.
   383	- Keep working files compact and purpose-specific. Prefer several small JSON
   384	  fragments over one very large generated script.
   385	
   386	## Output Shape
   387	
   388	The output is graph-like, not a matrix-only list:
   389	
   390	- `links`: many-to-many legal relationship groups.
   391	- `atomic_links`: exact `matrix_id` + `contract_id` legal pairs projected from
   392	  the grouped links for row-level verification.
   393	- `unmatched_matrix`: bank-standard requirements absent from the contract.
   394	- `unmatched_contract`: contract terms without a matrix analogue.
   395	- `summary`: exact counts derived from the arrays.
   396	
   397	Each `deviation` must name the legal gap and explain why it matters for the
   398	Bank. Do not use vague risk text such as "may be risky" without identifying the
   399	changed legal element.
   400	
   401	## Final QA
   402	
   403	Before finishing, verify:
   404	
   405	- `/outputs/working/matrix_inventory.json` and
   406	  `/outputs/working/contract_inventory.json` exist and were used;
   407	- every matrix `number` appears in exactly one of `links[].matrix_ids` or
   408	  `unmatched_matrix[].matrix_id`;
   409	- every real legal matrix-contract pair from grouped `links` appears in
   410	  `atomic_links`, and every `atomic_links` row points back to a grouped link;
   411	- every `atomic_links` row has one real matrix id, one real contract locator,
   412	  `relationship`, `coverage`, `coverage_role`, `analogue_strength`,
   413	  `element_checklist`, and pair-level discrepancies when relationship is
   414	  `deviation`;
   415	- no `atomic_links` row has `analogue_strength = weak_context`;
   416	- every material contract inventory item appears in a link, in
   417	  `unmatched_contract`, or is expressly classified as `not_material`;
   418	- no link has an empty `contract_ids` array;
   419	- every cited contract locator is present in `contract_inventory.json` and in
   420	  `inputs/contract.txt` as printed numbering, heading, definition label,
   421	  appendix/table label, or exact text;
   422	- every cited appendix or form locator passes the same test against
   423	  `inputs/contract.txt`; if not, replace it with the nearest real printed clause
   424	  and keep the appendix/form detail in evidence text;
   425	- no invented ids, internal aliases, translated appendix labels, parenthetical
   426	  ids, corrected numbering, or external answer labels;
   427	- `aligned` links have no discrepancies;
   428	- `deviation` links have at least one discrepancy with `type`, `description`,
   429	  and `risk`;
   430	- `missing_in_contract` items describe the absent bank-standard requirement and
   431	  the risk of omission, and include rejected weak candidates when any were
   432	  considered;
   433	- every `unmatched_matrix` item uses the field `status:
   434	  "missing_in_contract"`. Do not use `reason`, `classification`, or
   435	  `relationship` instead of `status`;
   436	- `extra_in_contract` items describe the extra contract term and its risk;
   437	- `not_material` is used only for non-operative or no-risk contract-only text
   438	  and includes a materiality reason;
   439	- `summary` counts equal the arrays.
Tool: ['/.agents/', '/.codex/', '/.env', '/.git/', '/.gitignore', '/.venv/', '/ALL_DATA/', '/__pycache__/', '/conversation_history/', '/inputs/', '/llm.py', '/main.py', '/output/', '/outputs/', '/runs/', '/skills/', '/tools/']
AI: [{'name': 'ls', 'args': {'path': '/inputs'}, 'id': 'call_00_D4hv62RTocoNJ8c5zvoL0900', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs'}, 'id': 'call_01_k5dAsg4LWOSEzcieguas4278', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/skills/acquiring-discrepancy-analysis'}, 'id': 'call_02_Zzvdyt6tArKDK4bcNRV72048', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/outputs/working/']
Tool: ['/skills/acquiring-discrepancy-analysis/SKILL.md', '/skills/acquiring-discrepancy-analysis/references/']
AI: [{'name': 'ls', 'args': {'path': '/skills/acquiring-discrepancy-analysis/references'}, 'id': 'call_00_QTzjKgBd0fJEXfnKdYav1962', 'type': 'tool_call'}, {'name': 'ls', 'args': {'path': '/outputs/working'}, 'id': 'call_01_qHbitf0EZjh4up9NPOrX2768', 'type': 'tool_call'}]
Tool: ['/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md']
Tool: ['/outputs/working/build_inventories.py', '/outputs/working/contract_inventory.json', '/outputs/working/matrix_inventory.json']
AI: Good — inventories already exist. Let me read all the key source documents and references.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_Zeo6vVR4ydvgmyLjgyZy5928', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_NCd4MDn2Ba06Bk8ik7rK2449', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'limit': 200}, 'id': 'call_02_XJMFRGe25Bm6EBeY5NDZ7446', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'limit': 200}, 'id': 'call_03_cJ4nsX3Ue6xxsuLhKXIk5727', 'type': 'tool_call'}]
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
     3	
     4	г. Сочи							                               «___»________20_ г.
     5	
     6	Федеральное государственное бюджетное учреждение «Кавказский государственный природный биосферный заповедник имени Х.Г. Шапошникова», именуемое в дальнейшем «Заказчик», в лице директора Шевелева Сергея Георгиевича, действующего на основании Устава, с одной стороны, и ___________  (Лицензия № ____ от __.___.___г.), именуемое в дальнейшем Банк/Исполнитель, в лице _______, действующего на основании _________, с другой стороны, вместе именуемые Стороны, с соблюдением требований Федерального закона от 5 апреля 2013 г. № 44-ФЗ «О контрактной системе в сфере закупок товаров, работ, услуг для обеспечения государственных и муниципальных нужд» (далее – Федеральный закон № 44-ФЗ), на основании проведения _______________________ (протокол № ____ от __.__.202__г.) заключили настоящий Контракт (далее - Контракт) о нижеследующем:
     7	
     8	1. ПРЕДМЕТ КОНТРАКТА
     9	
    10	1.1. По условиям настоящего контракта Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга) (далее - услуги) в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2), являющихся неотъемлемой частью настоящего контракта, а Заказчик обязуется принять и оплатить указанные услуги в порядке и размере установленном настоящим контрактом.
    11	Идентификационный код закупки 251231702678823170100100060016619244.
    12	1.2. Объем услуг, указанных в пункте 1.1 настоящего контракта, определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта, указанную в пункте 3.1 настоящего контракта.
    13	1.3. Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.
    14	
    15	2. ТЕРМИНЫ, ОПРЕДЕЛЕНИЯ И ВЗАИМОДЕЙСТВИЕ
    16	
    17	2.1. Авторизация – процедура получения разрешения от банка-эмитента или иного юридического лица, действующего от его имени, на проведение операции;
    18	2.1.1. банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы, являющаяся электронным средством платежа. Для совершения операций в ТСТ. Карта может быть представлена на  физическом носителе, путем указания её  реквизитов, а также через мобильное  устройство, которое позволяет его покупателю совершать операции по технологии беспроводной высокочастотной связи малого радиуса действия (NFC);    
    19	2.1.2. банк-эквайрер - кредитная организация, являющаяся участником платежной системы, организующая точки приема карт и осуществляющая весь комплекс финансовых операций, связанных с выполнением расчетов и платежей по картам в этих точках;
    20	2.1.3. банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;
    21	2.1.4. возврат платежа – операция, инициируемая банком-эмитентом в соответствии с правилами платежной системы и оспаривающая предъявленную банком-эквайрером операцию (транзакцию). Результатом операции «Возврат платежа» является списание денежных средств со счета банка-эквайрера и зачисление на счет банка-эмитента;
    22	2.1.5. держатель карты (держатель) – покупатель-физическое лицо, на имя которого выпущена карта;
    23	2.1.6. документ по операции - документ на бумажном носителе или в электронном виде, являющийся основанием для осуществления расчетов по операциям, совершенным с использованием карты;
    24	2.1.7. код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации;
    25	2.1.8. контрольно-кассовая техника (ККТ) – программно-технические средства и их комплексы, обеспечивающие запись и хранение фискальных данных в фискальных накопителях, формирующие фискальные документы, обеспечивающие передачу фискальных документов в налоговые органы через оператора фискальных данных и печать фискальных документов на бумажных носителях в соответствии с правилами, установленными законодательством Российской Федерации о применении контрольно-кассовой техники;
    26	2.1.9.контрольная лента - отчет, распечатываемый на электронном терминале и содержащий информацию о транзакциях, совершенных в ТСТ на электронном терминале за определенный период;
    27	2.1.10.отложенный платеж - операция оплаты, осуществляемая на основании полученного от Заказчика/ТСТ сообщения, направленного с использованием электронного терминала, о наличии задолженности покупателя перед Заказчиком/ТСТ, после окончательного расчета;
    28	2.1.11.операция – действие, осуществляемое Заказчиком/ТСТ/покупателем на электронном терминале, в том числе операция оплаты, операция отмены, операция возврата, совершенная с использованием карты/реквизитов карты/NFС-карты/ без предъявления карты;
    29	2.1.12.операция оплаты – операция по оплате товаров/услуг с использованием карты в учреждении Заказчика/ ТСТ с проведением авторизации;
    30	2.1.13. операция отмены – операция, выполняемая Заказчиком/ТСТ на электронном терминале/смарт-терминале, с целью отмены авторизации. Операция отмены авторизации выполняется до проведения операции «Сверка итогов»;
    31	2.1.14. операция возврата – операция, оформляемая  Заказчиком/ТСТ  при возврате товаров/отказе от услуг или от части товаров/услуг, оплаченных картой, после проведения операции «Сверка итогов», следствием которой является возврат суммы операции оплаты или ее части на карту, предъявленную покупателем;
    32	2.1.15. платежная система – совокупность организаций, взаимодействующих по правилам платежной системы в целях осуществления перевода денежных средств;
    33	2.1.16. покупатель - физическое лицо, осуществляющее оплату товара/услуги в ТСТ при помощи карты, а также лицо, осуществляющее возврат/отказ от товара/услуги в ТСТ;
    34	2.1.17. повторяющиеся платежи – платежи в оплату товаров/услуг, осуществляемые регулярно в течение определенного периода времени;
    35	2.1.18. предавторизация - операция по резервированию денежных средств на карте для последующей оплаты, требующая подтверждения со стороны Заказчика/ТСТ с указанием суммы списания;
    36	2.1.19. предприятие (Заказчик) – торгово-сервисное предприятие (ТСП): юридическое лицо/ индивидуальный предприниматель (ИП), принимающие карты в качестве средства оплаты товаров/услуг на основании условий настоящего контракта.  Заказчик может иметь одну торгово-сервисную точку или сеть из двух и более торгово-сервисных точек;
    37	расчетная информация–информация по операциям, передаваемая в банк-эквайрер, в рамках проведения процедуры электронной сверки итогов за определенный период;
    38	2.1.20. рабочий день – день, который не признается в соответствие с законодательством Российской Федерации выходным и (или) нерабочим праздничным днем;
    39	2.1.21. реверсивная транзакция – финансово-информационное сообщение, которое банк-эквайрер направляет в платежную систему для отмены ранее направленной транзакции (например, в случае ошибочного предъявления транзакции). В результате обработки этого сообщения происходит списание денежных средств со счета банка-эквайрера (со счета Заказчика) и зачисление их на счет банка-эмитента (на счет карты покупателя);
    40	2.1.22. сводный чек электронного терминала – бумажный отчет, распечатываемый электронным терминалом и содержащий итоговую информацию по операциям за определенный промежуток времени;
    41	2.1.23. тарифы банка– стоимость услуг банка за выполнение расчетов по операциям оплаты в виде процента от суммы каждой операции оплаты и размера платы за сервисное обслуживание; 
    42	2.1.24. товар/услуга – товар, работа, услуга, результат интеллектуальной деятельности, реализуемые Заказчиком в ТСТ;
    43	2.1.25. торгово-сервисная точка (ТСТ) – подразделение Заказчика, зарегистрированное банком на основании информации о ТСТ, в котором осуществляется реализация товаров/ услуг покупателям;
    44	2.1.26. торговый эквайринг – осуществление банком-эквайрером расчетов с предприятиями, осуществляющими реализацию товаров/услуг с использованием карт в ТСТ;
    45	транзакция – финансово-информационное сообщение о совершении операции с картой в ТСТ;
    46	2.1.27. чек электронного терминала (чек) – документ по операции, распечатываемый электронным терминалом и содержащий информацию о проведенной операции;
    47	2.1.28. электронная сверка итогов – процедура передачи от электронного терминала исполнителю расчетной информации об операциях за определенный период;
    48	2.2. электронный терминал – электронное программно-техническое устройство исполнителя (в том числе дополнительное оборудование и/или специальное программное обеспечение ККТ), позволяющее осуществлять прием карт в ТСТ для проведения операций. Электронный терминал может включать в себя в том числе мобильный терминал (mPOS), биометрический терминал. Электронный терминал предоставляется исполнителем и устанавливается на срок действия контракта. Электронный терминал предназначен и может использоваться только в целях исполнения контракта. 
    49	2.3.	Банк и Заказчик в рамках настоящего Контракта обмениваются информацией и документами одним из следующих способов, выбираемых Стороной, направляющей информацию/документ по своему усмотрению, если иное не предусмотрено Контрактом: 
    50	2.3.1.	с использованием электронных каналов связи путем направления информации/документа в электронном виде с адресов и по адресам электронной почты, предоставленных Заказчиком в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг и/или Информации о ТСТ Заказчика за исключением в передаваемой информации сведений, относящихся к персональным данным, коммерческой и банковской тайне. В случае если иное не предусмотрено в Контракте, информация/документы, направляемые по адресам электронной почты, имеют полную юридическую силу и могут быть использованы в суде в качестве доказательств;
    51	2.3.2.	посредством системы ДБО или аналогичных систем Банка;
    52	2.3.3.	путем направления письма с доставкой нарочным или курьерской почтой по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;
    53	2.3.4.	путем направления почтового отправления (заказного письма) по почтовому адресу, указанному в Заявлении Заказчика на проведение расчетов по операциям оплаты товаров/услуг /Информации о ТСТ получающей стороны;
    54	2.3.5.	путем обмена электронными документами посредством автоматизированной системы _________________. В этом случае документы подписываются усиленной квалифицированной электронной подписью  (далее – УКЭП) Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;
    55	2.3.6.	путем обмена электронными документами в Единой информационной системе в сфере закупок и иных электронных торговых площадках в случаях, предусмотренных законодательством Российской Федерации и иными нормативными правовыми актами о контрактной системе в сфере закупок. В этом случае документы подписываются УКЭП Сторон и признаются равнозначными документам, подписанным собственноручной подписью, и имеют юридическую силу, равнозначную документам, подписанным в бумажном виде;
    56	2.3.7.	через контактные данные службы поддержки Банка (24/7), указанные в п.2 Порядка проведения операций в Торгово-сервисных точках/на Ресурсе.
    57	Сторона считается получившей информацию/документ в случае направления способом, указанным в: 
    58	•	п. 2.3.1, п. 2.3.2 Контракта – в дату направления электронного письма на соответствующий адрес электронной почты, оформления запроса в системе ДБО/аналогичной системе Банка соответственно;
    59	•	п. 2.3.3, п. 2.3.4 Контракта – в дату доставки получающей стороне письма/почтового отправления (заказного письма);
    60	•	п. 2.3.5. Контракта – в дату поступления информации/документа от Банка Оператору электронного документооборота (дочерней компании Банка). Дата и время поступления информации/документа указываются в поступившей от Оператора электронного документооборота электронной квитанции;
    61	•	 п. 2.3.6. Контракта – в дату направления информации/документа в Единой информационной системе в сфере закупок или иной электронной торговой площадке ;
    62	•	п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка
    63	
    64	3. ЦЕНА КОНТРАКТА
    65	
    66	3.1. Максимальное значение цены контракта (стоимость услуг) (далее – цена контракта) составляет 1 900 000,00 рублей (один миллион девятьсот тысяч рублей 00 копеек), в том числе НДС ______________ (в случае если Исполнитель не является плательщиком НДС, указать «НДС не облагается»).
    67	3.1.1. Цена за единицу услуги указана в спецификации (Приложение № 1), являющейся неотъемлемой частью настоящего контракта.
    68	3.2.Цена единицы услуги включает в себя расходы Исполнителя, связанные с оказанием услуг Банка за выполнение расчетов с Заказчиком по Операциям оплаты в виде процента от суммы каждой Операции оплаты.
    69	3.3. Положения настоящего Контракта, касающиеся применения цены контракта или начальной максимальной цены Контракта применяются к максимальному значению цены Контракта, указанному в настоящем разделе Контракта, если Федеральным законом №44-ФЗ не установлено иное.
    70	
    71	4. СРОКИ, УСЛОВИЯ ОКАЗАНИЯ УСЛУГ, ПОРЯДОК ОПЛАТЫ
    72	
    73	4.1. Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее.
    74	4.2. В случае если действующим законодательством Российской Федерации и извещением о проведении закупки предусмотрены требования, предъявляемые к лицам, оказывающим услуги, составляющие предмет настоящего контракта (объект закупки), Исполнитель должен соответствовать таким требованиям.
    75	Исполнитель должен иметь лицензию на осуществление банковских операций, соответствующих виду предмета контракта (основание: Федеральный закон от 02.12.1990 N 395-1 "О банках и банковской деятельности"), за исключением случая, указанного в части 9 статьи 13 Федерального закона от 02.12.1990 № 395-1 «О банках и банковской деятельности» и в Федеральном законе «О национальной платежной системе».
    76	4.3.Оказание услуг осуществляется Исполнителем по адресу местоположения точек приема к оплате пластиковых карт (эквайринга) торгово-сервисных точек (ТСТ). Перечень ТСТ указан в Приложении № 1.
    77	В целях регистрации нового ТСТ в рамках настоящего контракта Заказчик после заключения контракта предоставляет Исполнителю заявление Заказчика на проведение расчетов по операциям с использованием банковских карт и информацию о ТСТ Заказчика/изменение информации о ТСТ заказчика, подписанную уполномоченным представителем заказчика.
    78	4.4. Оплата по контракту осуществляется по безналичному расчёту платёжным поручением путём перечисления Заказчиком денежных средств на счёт Исполнителя, указанный в настоящем контракте. В случае изменения счета Исполнителя он обязан в двухдневный срок в письменной форме сообщить об этом Заказчику с указанием новых реквизитов расчётного счёта. В противном случае все риски, связанные с перечислением Заказчиком денежных средств на указанный в настоящем контракте счёт Исполнителя, несёт Исполнитель.
    79	Оплата оказанной услуги осуществляется по цене единицы услуги исходя из объема фактически оказанной услуги, но в размере, не превышающем максимального значения цены контракта.
    80	4.5.Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг и производится ежемесячно. 
    81	4.5.1. Услуги, оказанные в ноябре оплачиваются в срок не позднее 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг, но не позднее 30 декабря 2025 года.
    82	
    83	5.ОБЯЗАТЕЛЬСТВА СТОРОН
    84	
    85	5.1.Исполнитель обязуется:
    86	5.1.1. Установить Заказчику и подготовить к эксплуатации Электронные терминалы для проведения операций в течение 5 (пяти) рабочих дней с даты подписания контракта. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком. Разместить на сайте: ___________________ обучающие материалы для прохождения инструктажа сотрудниками Заказчика.
    87	5.1.2. Ежемесячно формировать и направлять Заказчику документ о приемке в соответствии с пунктами 8.3.1 и 8.3.2. Контракта.
    88	5.1.3. Обеспечить соответствие оказанных услуг предъявляемым к ним требованиям законодательства Российской Федерации.
    89	5.1.4. Обеспечивать круглосуточную работоспособность Электронных терминалов. В случае выхода из строя Электронного терминала, обеспечить Заказчика исправным Электронным терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Исполнителем заявки от Заказчикам по номеру службы поддержки Банка.
    90	5.1.5. Предоставлять Заказчику полную и точную информацию об услугах, а также о ходе исполнения своих обязательств по настоящему контракту, в том числе о сложностях, возникающих при исполнении контракта.
    91	5.1.6. Осуществлять круглосуточную авторизацию;
    92	5.1.7. Обеспечивать электронные терминалы, установленные у заказчика/ТСТ, рекламно-информационными материалами, необходимыми для проведения операций с использованием карт;
    93	5.1.8. На основании полученной от Заказчика расчетной информации, переданной от Электронного терминала Исполнителю, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты в валюте проведения операции (рубли РФ).
    94	Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.
    95	В случае технического сбоя при передаче Электронной сверки итогов/ невозможности проведения Предприятием/ТСТ или отсутствия Электронной сверки итогов по иным причинам, перечислять Заказчику суммы Операций, по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов, проводить расчеты по всем Операциям с данной ТСТ;
    96	5.1.9. Осуществлять обработку персональных данных, полученных от заказчика, а также обеспечить конфиденциальность и защиту обрабатываемых персональных данных в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных» (далее – Закона 152-ФЗ). Принимать необходимые правовые, организационные и технические меры или обеспечивать их принятие для защиты получаемых от заказчика персональных данных от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения персональных данных, а также от иных неправомерных действий в отношении получаемых от заказчика персональных данных.
    97	5.1.10. Исполнитель в соответствии с контрактом перечисляет Заказчику суммы операций оплаты услуг, совершенных на предприятии Заказчика/торгово-сервисных точках (ТСТ) с использованием карт.
    98	5.2. Исполнитель вправе:
    99	5.2.1. Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате стоимости услуг по настоящему контракту.
   100	5.2.2. Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств.
   101	5.2.3. Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов, расположенных на территории заказчика/ТСТ. Производить замену электронных терминалов, а также обновлять программное обеспечение электронного терминала, уведомив заказчика не менее чем за два рабочих дня до даты замены или обновления; 
   102	5.2.4. Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций;
   103	5.2.5. Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции. Для анализа спорных ситуаций исполнитель также может потребовать от заказчика предоставления копии контрольной ленты, письменного заявления заказчика с изложением обстоятельств проведения операции, счетов за предоставленные товары/услуги, товарные или кассовые чеки и другие документы, необходимые для проведения анализа обстоятельств проведения операции или претензионной работы;
   104	5.2.6. В случае изменения реквизитов исполнителя, указанных в контракте, уведомить об этом заказчика в письменном виде путем направления информации в адрес заказчика в течение трех рабочих дней;
   105	5.2.7. В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении заказчика на проведение расчетов по операциям с использованием банковских карт/информации о ТСТ;
   106	5.2.8. Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.
   107	5.2.9. В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению Контракта при наступлении следующих событий:
   108	5.2.9.1. нарушение Заказчиком условий Контракта;
   109	5.2.9.2. внесение данных Заказчика в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;
   110	5.2.9.3. при наличии у Исполнителя подозрений, что Операции в ТСТ совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;
   111	5.2.9.4. получение негативной информации о Заказчике/ТСТ от органов государственной власти РФ и/или Платежных систем;
   112	5.2.9.5. получение информации о мошенничестве в ТСТ
   113	стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных систем, полученные c использованием факсимильной связи, по электронной почте (e-mail);
   114	5.2.9.6. осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций;
   115	5.2.9.7. ликвидация Заказчика либо возбуждение в отношении Заказчика дела о банкротстве в соответствии с Федеральным законом от 26.10.2002 № 127-ФЗ «О несостоятельности (банкротстве)»;
   116	5.2.9.8. выявление недостоверных сведений о Заказчике/ТСТ, руководителе(-ях) в информации, указанной при заключении Контракта;
   117	5.2.9.9. несоответствие предлагаемых Покупателям Товаров/услуг роду деятельности Заказчика, указанному в Информации о ТСТ; 
   118	5.2.9.10. отсутствие операций в течение 30 (тридцати) календарных дней подряд
   119	5.2.9.11. исчерпание Цены Контракта и/или окончание срока действия Контракта.
   120	5.2.10.	Удерживать из сумм, подлежащих перечислению Заказчику по Контракту, следующие суммы:
   121	5.2.10.1	Суммы Операций, являющихся недействительными, в следующих случаях:
   122	Операция совершена с нарушением Контракта, требований законодательства РФ и/или правил Платежной системы и инструктивных материалов Банка;
   123	 Операция совершена по поддельной или недействительной Карте;
   124	Документ по операции заполнен не полностью, имеются исправления или отсутствует возможность определить сумму Операции, код Авторизации; 
   125	экземпляр Документа по операции, переданный в Банк, не соответствует экземпляру Документа по операции, переданному Покупателю;
   126	 подпись Покупателя на Чеке электронного терминала отсутствует, при этом на Чеке электронного терминала присутствует поле «Подпись Клиента»; 
   127	по требованию Банка в течение 3 (трех) рабочих дней со дня получения запроса не предоставлены или предоставлены не в полном объеме (или не соответствующие правилам Платежной системы) или в ненадлежащем качестве подтверждающие Документы по операции/объяснения обстоятельств Операции;
   128	оплаченные с использованием Карты/ ее реквизитов/ NFС-карты/ SberPay/ Плати QR/ Платежного счета /Платежных решений  Товары/услуги были возвращены Предприятию, или не доставлены Покупателю/услуги отменены/не оказаны, но возврат денежных средств Покупателю произведен не был (за исключением случаев, когда Товары/услуги не были приняты/возврат Товара/отказ от услуг не предусмотрен законодательством РФ или правилами работы Предприятия и Покупатель был об этом проинформирован до совершения сделки);
   129	Товар/услуга уже был оплачен Покупателем ранее (о чем имеется документальное подтверждение);
   130	на совершенную Операцию Банком не был получен код Авторизации согласно Порядка проведения операций в Торгово-сервисных точках/на Ресурсе. Код Авторизации считается полученным Банком в том случае, если он содержится в электронных реестрах кодов Авторизации Банка и относится к указанной Операции. Код Авторизации указывается на Чеке Электронного терминала, который передается в ККТ Предприятия от Электронного терминала ;
   131	сумма Товара/услуги была разбита на несколько Операций;
   132	от Банка-эмитента получена информация о мошенническом характере Операции;
   133	Операция была проведена без считывания Карты в Электронном терминале (реквизиты Карты были введены в Электронный терминал вручную), за исключением случаев, когда данные действия согласованы  с Банком.
   134	5.2.10.2	Суммы, ошибочно перечисленные на счет Заказчика.
   135	5.2.10.3	Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.
   136	5.2.10.4	Исполнитель  удерживает из общих сумм, подлежащих перечислению на Счет Заказчика суммы операций, которые были оспорены и/или списаны со счета Исполнителя Банком – эмитентом в соответствии с правилами Платежных систем по операциям, проведенным в ТСТ, а также суммы оспоренных операций в отношении Товаров/услуг, реализуемых Заказчиком  как агентом.
   137	5.2.10.5 Банк удерживает из общих сумм, подлежащих перечислению на Счет Заказчика суммы штрафов и иных убытков, возникших у Исполнителя в результате применения к нему штрафных санкций в соответствии с правилами Платежных систем, а также привлечения Исполнителя к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Заказчиком обязательств по Контракту.
   138	5.3. Заказчик обязуется:
   139	5.3.1. Принять оказанные услуги по документу о приемке оказанных услуг.
   140	5.3.2. Оплатить стоимость услуг, оказанных Исполнителем, согласно условиям настоящего контракта.
   141	5.3.3. Осуществлять контроль за ходом оказания услуг Исполнителем.
   142	5.3.4. Принять решение об одностороннем отказе от исполнения настоящего контракта в случае, если в ходе исполнения контракта установлено, что Исполнитель не соответствует установленным извещением о проведении закупки требованиям к участникам закупки или предоставил недостоверную информацию о своем соответствии таким требованиям, что позволило ему стать победителем определения Исполнителя.
   143	5.3.5. Требовать уплаты неустоек (штрафов, пеней) в случае просрочки исполнения Исполнителем обязательств, предусмотренных контрактом, а также в иных случаях неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных контрактом.
   144	5.3.6. Уменьшить сумму, подлежащую уплате Заказчиком юридическому лицу или физическому лицу, в том числе зарегистрированному в качестве индивидуального предпринимателя, на размер налогов, сборов и иных обязательных платежей в бюджеты бюджетной системы Российской Федерации, связанных с оплатой контракта, если в соответствии с законодательством Российской Федерации о налогах и сборах такие налоги, сборы и иные обязательные платежи подлежат уплате в бюджеты бюджетной системы Российской Федерации.
   145	5.3.7. Размещать на видных местах ТСТ, предоставляемые исполнителем рекламно-информационные материалы, извещающие покупателей о возможности оплаты услуг с использованием карт, в случае если это не противоречит требованиям законодательства Российской Федерации;
   146	5.3.8. Не разбивать сумму одной операции оплаты на несколько сумм и не проводить отдельные операции на каждую из этих сумм;
   147	5.3.9. Не использовать реквизиты карты, которые стали доступны заказчику/ТСТ, для иных целей, кроме как проведение операций в присутствии или по распоряжению покупателя;
   148	5.3.10. Проводить операции и оформлять документы по операциям в торгово-сервисных точках к контракту и нести ответственность за правильность указанной в документах информации;
   149	5.3.11. Хранить в недоступном для третьих лиц месте документы по операциям (чеки, кассовые чеки, распоряжения покупателя, документы, подтверждающие факт передачи товара/оказания услуги, контрольные ленты и т.п.) не менее тринадцати месяцев с даты совершения операции и передавать их копии надлежащего качества (изображение четкое, размер не менее оригинального документа) исполнителю по его запросу  в течение трех рабочих дней с даты получения запроса;
   150	5.3.12. Передавать исполнителю по его запросу в течение трех рабочих дней с даты получения запроса от исполнителя письменное заявление с изложением обстоятельств проведения операции в ТСТ. В случае утраты составленных с использованием карты документов по операции немедленно сообщить об утрате исполнителю;
   151	5.3.13. В случае реорганизации, внесения изменений и дополнений в документы, представленные заказчиком при заключении  контракта, при открытии в отношении заказчика/смены стадии процедуры банкротства, а также при смене руководства ТСТ, изменении адреса местонахождения заказчика/ТСТ, внесенного в ЕГРЮЛ, реквизитов заказчика/ТСТ обязуется информировать исполнителя и передать (по месту заключения контракта) надлежащим образом заверенные и оформленные документы, подтверждающие внесение изменений и дополнений не позднее трех рабочих дней с даты дополнений/изменений;
   152	5.3.14. Предоставлять исполнителю достоверные документы и сведения, необходимые исполнителю для исполнения требований, предусмотренных действующим законодательством Российской Федерации, в том числе, но не исключительно: не реже одного раза в год, а также по отдельному запросу исполнителя в течение семи рабочих дней со дня получения запроса обновлять сведения и документы, представленные исполнителю при заключении настоящего контракта, включая сведения о целях финансово-хозяйственной деятельности, финансовом положении и деловой репутации заказчика, а также сведения о своих представителях, выгодоприобретателях и бенефициарных владельцах (при наличии);
   153	5.3.15. По письменному запросу исполнителя заказчик обязуется предоставить подтверждение правомерности передачи ПДн. В случае если заказчик не предоставит подтверждение наличия таких оснований, он обязуется за свой счёт урегулировать все претензии своих представителей, государственных органов и иных лиц, предъявленные исполнителю, а также возместить любые убытки и расходы, понесенные исполнителем в результате не предоставления таких доказательств. Заказчик обязан уведомить исполнителя об отзыве согласия руководителя заказчика на передачу указанных данных;
   154	5.3.16. С даты расторжения контракта прекратить прием к оплате карт, снять рекламно-информационные материалы, извещающие об обслуживании карт;
   155	5.3.17. Не принимать мер противодействия исполнителю в проведение проверки заказчика/ТСТ на предмет выявления мошеннических операций и/или предоставления покупателям товаров/услуг, не соответствующих роду деятельности заказчика/ТСТ, а также оказывать содействие исполнителю в проведении разбирательства по факту совершения подозрительных операций;
   156	5.3.18. При осуществлении операций у заказчика в ТСТ (торговый эквайринг):
   157	5.3.18.1. Использовать электронные терминалы (в том числе технологические sim-карты)/смарт-терминалы и программное обеспечение, предоставленное исполнителем, только для целей реализации настоящего контракта и на территории регистрации ТСТ/фактической установки электронного терминала. Не вносить изменения в программное обеспечение и электронные терминалы/смарт-терминалы, предоставленное исполнителем, и не осуществлять самостоятельно их ремонт. Использовать термоленту только для электронных терминалов, установленных в ТСТ. Не передавать третьим лицам электронные терминалы, документы по операциям, термоленту для электронных терминалов и рекламно-инструктивные материалы, предоставленные исполнителем, за исключением работников обслуживающей компании;
   158	5.3.18.2. Предоставлять исполнителю доступ к местам установки электронных терминалов для проведения работ по его подключению, настройке, ремонту, замене, техническому обслуживанию и визуальной проверке;
   159	5.3.18.3. Принять электронные терминалы по акту принятия оказанных услуг, составленному в двух экземплярах и подписанных исполнителем и заказчиком. один экземпляр акта находится на хранении у исполнителя, второй – у заказчика;
   160	5.3.20.4. В случае выхода электронного терминала из строя или его утраты немедленно информировать об этом исполнителя;
   161	5.3.18.5. Вернуть исполнителю или обслуживающей компании электронные терминалы/смарт-терминала в течение пяти рабочих дней с даты расторжения контракта или с даты получения письменного/устного требования исполнителя о возврате электронных терминалов;
   162	5.3.19. Возместить Исполнителю в полном объеме и в безусловном порядке денежные средства в размере: 
   163	•	средств, которые в соответствии с правилами Платежных систем были списаны со счета Исполнителя в пользу Банка-эмитента либо уплачены Исполнителем Банку-эмитенту и (или) Держателям карт, эмитированных Исполнителем, по Операциям :
   164		ставшим предметом каких-либо споров и разногласий в соответствии с законодательством Российской Федерации и (или) в соответствии с правилами Платежных систем;
   165		являющимся недействительными в соответствии с Контрактом;
   166	•	средств, которые в соответствии с правилами Платежных систем были списаны со счета Исполнителя либо уплачены Исполнителем в связи с рассмотрением споров и разногласий между Покупателями и Заказчиком касательно Операций, указанных в настоящем пункте Контракта, в том числе любые сборы, комиссии, платы и (или) иные расходы Исполнителя, связанные с рассмотрением споров и разногласий по таким Операциям;
   167	•	убытков, возникших у Исполнителя в результате применения к нему штрафных санкций в соответствии с законодательством Российской Федерации и (или) правилами Платежных систем, а также привлечения Исполнителя к гражданской или административной ответственности судебными органами или уполномоченными органами государственной власти вследствие неисполнения или ненадлежащего исполнения Заказчиком обязательств по Контракту.
   168	5.3.20. В рамках настоящего Контракта Заказчик передает Исполнителю персональные данные (далее – ПДн) руководителя Заказчика, состав которых включает: ФИО, адрес, паспортные данные. Заказчик гарантирует наличие правовых оснований на передачу Исполнителю персональных данных руководителя Заказчика, в том числе на передачу в Платежную систему МИР, состав которых включает: ФИО, адрес, паспортные данные в целях, оказания услуг по контракту.
   169	5.4. Заказчик вправе:
   170	5.4.1. Требовать от Исполнителя исполнения обязательств, предусмотренных контрактом, надлежащим образом в соответствии с действующим законодательством Российской Федерации и настоящим контрактом.
   171	5.4.2. Отказать Исполнителю в приемке оказанных услуг в случае их ненадлежащего качества.
   172	5.4.3. Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств.
   173	5.4.4. Отказаться от оплаты услуг ненадлежащего качества, а если услуги оплачены, потребовать возврата уплаченных сумм, а также требовать возмещения убытков.
   174	5.4.5. Ссылаться на возможность оплаты товаров/услуг с использованием карт в собственных рекламных материалах, предварительно согласовав их с исполнителем настоящего контракта;
   175	5.5.  Заказчик обязуется передавать Исполнителю по его запросу в течение 3 (трех) рабочих дней с даты получения запроса от Исполнителя письменное заявление с изложением обстоятельств проведения Операции. В случае утраты составленных Документов по операции немедленно сообщить об утрате Исполнителю  одним из способов, предусмотренных Контрактом.
   176	5.6. Заказчик обязуется в случае утери оборудования Заказчиком:
   177	Вернуть Исполнителю или Обслуживающей компании Электронные терминалы/Смарт-терминалы Банка в течение 5 (пяти) рабочих дней с даты расторжения Контракта или с даты получения письменного/устного требования Исполнителя о возврате Электронных терминалов/Смарт-терминалов Исполнителя. 
   178	5.7. В случае невозврата Электронных терминалов/Смарт-терминалов Исполнителя  Заказчик обязан уплатить Исполнителю  штраф в размере 10 000 (десяти тысяч) рублей, включая НДС, за каждый Электронный терминал, в размере 25 000 (двадцати пяти тысяч) рублей, включая НДС, за каждый Смарт-терминал Банка. 
   179	5.9. Заказчик вправе получать консультацию у исполнителя по вопросам эксплуатации электронных терминалов и проведению операций с использованием карт путем обращения в службу поддержки исполнителя.
   180	5.10. Заказчик обязуется обеспечить самостоятельное и своевременное прохождение всеми сотрудниками Предприятия инструктажа о порядке проведения Операций, размещенном на сайте: ______________________________.
   181	
   182	
   183	6. АНТИКОРРУПЦИОННАЯ ОГОВОРКА
   184	
   185	6.1. При заключении, исполнении, изменении и расторжении Контракта Стороны принимают на себя обязательство не осуществлять действий, квалифицируемых применимым законодательством как «коррупция» , а также иных действий (бездействия), нарушающих требования применимого законодательства, применимых норм международного права в области противодействия коррупции.
   186	
   187	
   188	7. ОТВЕТСТВЕННОСТЬ СТОРОН
   189	
   190	7.1.	За неисполнение или ненадлежащее исполнение обязательств по Контракту Стороны несут ответственность в соответствии с действующим законодательством Российской Федерации.
   191	Сторона освобождается от уплаты неустойки (штрафа, пени), если докажет, что неисполнение или ненадлежащее исполнение обязательства, предусмотренного Контрактом, произошло вследствие непреодолимой силы или по вине другой стороны.
   192	Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, не может превышать цену контракта.
   193	Общая сумма начисленных штрафов за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, не может превышать цену контракта.
   194	7.2. В случае просрочки исполнения Заказчиком обязательств, предусмотренных Контрактом, а также в иных случаях неисполнения или ненадлежащего исполнения Заказчиком обязательств, предусмотренных Контрактом, Исполнитель вправе потребовать уплаты неустоек (штрафов, пеней).
   195	7.3. Пеня начисляется за каждый день просрочки исполнения Заказчиком обязательства, предусмотренного Контрактом, начиная со дня, следующего после дня истечения установленного Контрактом срока исполнения обязательства. При этом размер пени устанавливается в размере 1/300 действующей на день уплаты пеней ключевой ставки Центрального банка Российской Федерации от не уплаченной в срок суммы.
   196	7.4. Штрафы начисляются за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств, предусмотренных Контрактом. 
   197	7.4.1. Размер штрафа по каждому факту неисполнения Заказчиком обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств, предусмотренных Контрактом, устанавливается в соответствии с постановлением Правительства РФ от 30.08.2017 № 1042 «Об утверждении Правил определения размера штрафа, начисляемого в случае ненадлежащего исполнения заказчиком, неисполнения или ненадлежащего исполнения поставщиком (Подрядчиком, исполнителем) обязательств, предусмотренных контрактом (за исключением просрочки исполнения обязательств заказчиком, поставщиком (Подрядчиком, исполнителем), о внесении изменений в постановление Правительства Российской Федерации от 15 мая 2017 г. № 570 и признании утратившим силу постановления Правительства Российской Федерации от 25 ноября 2013 г. N 1063» (далее – Постановление № 1042) в следующем порядке:
   198	а) 1000 рублей, если цена контракта не превышает 3 млн. рублей (включительно);
   199	б) 5000 рублей, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   200	в) 10000 рублей, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
Tool:      1	[
     2	  {
     3	    "id": "2.1",
     4	    "proposition": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений",
     5	    "party": "both/neutral",
     6	    "right_or_obligation": "declaration",
     7	    "object": "TST registration",
     8	    "trigger": "connection of service",
     9	    "material_terms": "none explicit",
    10	    "applicability": "in_scope",
    11	    "applicability_reason": "product=common, lot=common, terminal=common",
    12	    "materiality": "material"
    13	  },
    14	  {
    15	    "id": "2.2",
    16	    "proposition": "Важен факт, что валюта рубль РФ, другая валюта недопустима",
    17	    "party": "both/neutral",
    18	    "right_or_obligation": "declaration",
    19	    "object": "general",
    20	    "trigger": "standing obligation",
    21	    "material_terms": "none explicit",
    22	    "applicability": "in_scope",
    23	    "applicability_reason": "product=common, lot=common, terminal=common",
    24	    "materiality": "material"
    25	  },
    26	  {
    27	    "id": "2.3.1",
    28	    "proposition": "Нужно проверять признаётся ли полная юридическая сила e‑mail, есть ли ограничения по видам сведений и возможность изменять/обновлять адреса.",
    29	    "party": "both/neutral",
    30	    "right_or_obligation": "declaration",
    31	    "object": "document exchange",
    32	    "trigger": "standing obligation",
    33	    "material_terms": "none explicit",
    34	    "applicability": "in_scope",
    35	    "applicability_reason": "product=common, lot=common, terminal=common",
    36	    "materiality": "material"
    37	  },
    38	  {
    39	    "id": "2.3.2",
    40	    "proposition": "Важен сам факт возможности отправки информации / документов таким способом",
    41	    "party": "both/neutral",
    42	    "right_or_obligation": "declaration",
    43	    "object": "document exchange",
    44	    "trigger": "standing obligation",
    45	    "material_terms": "none explicit",
    46	    "applicability": "in_scope",
    47	    "applicability_reason": "product=common, lot=common, terminal=common",
    48	    "materiality": "material"
    49	  },
    50	  {
    51	    "id": "2.3.3",
    52	    "proposition": "Важен сам факт возможности отправки информации / документов таким способом",
    53	    "party": "both/neutral",
    54	    "right_or_obligation": "declaration",
    55	    "object": "document exchange",
    56	    "trigger": "standing obligation",
    57	    "material_terms": "none explicit",
    58	    "applicability": "in_scope",
    59	    "applicability_reason": "product=common, lot=common, terminal=common",
    60	    "materiality": "technical"
    61	  },
    62	  {
    63	    "id": "2.3.4",
    64	    "proposition": "Важен сам факт возможности отправки информации / документов таким способом",
    65	    "party": "both/neutral",
    66	    "right_or_obligation": "declaration",
    67	    "object": "document exchange",
    68	    "trigger": "standing obligation",
    69	    "material_terms": "none explicit",
    70	    "applicability": "in_scope",
    71	    "applicability_reason": "product=common, lot=common, terminal=common",
    72	    "materiality": "technical"
    73	  },
    74	  {
    75	    "id": "2.3.5",
    76	    "proposition": "Важна равнозначность документов",
    77	    "party": "both/neutral",
    78	    "right_or_obligation": "declaration",
    79	    "object": "document exchange",
    80	    "trigger": "standing obligation",
    81	    "material_terms": "none explicit",
    82	    "applicability": "in_scope",
    83	    "applicability_reason": "product=common, lot=common, terminal=common",
    84	    "materiality": "material"
    85	  },
    86	  {
    87	    "id": "2.3.6",
    88	    "proposition": "Важен сам факт наличия данного канала для обмена электронными документами",
    89	    "party": "both/neutral",
    90	    "right_or_obligation": "declaration",
    91	    "object": "document exchange",
    92	    "trigger": "standing obligation",
    93	    "material_terms": "none explicit",
    94	    "applicability": "in_scope",
    95	    "applicability_reason": "product=common, lot=fz_44, terminal=common",
    96	    "materiality": "material"
    97	  },
    98	  {
    99	    "id": "2.3.7",
   100	    "proposition": "Для представленных в контракте способах обмена информацией / документами, не должно быть расхождений в данном пункте на счёт даты, с которой сторона считается получившей информацию",
   101	    "party": "both/neutral",
   102	    "right_or_obligation": "declaration",
   103	    "object": "document exchange",
   104	    "trigger": "upon occurrence of specified event",
   105	    "material_terms": "none explicit",
   106	    "applicability": "in_scope",
   107	    "applicability_reason": "product=common, lot=common, terminal=common",
   108	    "materiality": "technical"
   109	  },
   110	  {
   111	    "id": "2.4",
   112	    "proposition": "Важно именно признание ссылок и документов в догворе его неотъемлемой частью",
   113	    "party": "both/neutral",
   114	    "right_or_obligation": "declaration",
   115	    "object": "general",
   116	    "trigger": "standing obligation",
   117	    "material_terms": "none explicit",
   118	    "applicability": "in_scope",
   119	    "applicability_reason": "product=common, lot=common, terminal=common",
   120	    "materiality": "technical"
   121	  },
   122	  {
   123	    "id": "2.5.1.1",
   124	    "proposition": "Важен факт, что бесконтактная оплата подключается автоматически",
   125	    "party": "both/neutral",
   126	    "right_or_obligation": "declaration",
   127	    "object": "SberPay",
   128	    "trigger": "connection of service",
   129	    "material_terms": "none explicit",
   130	    "applicability": "in_scope",
   131	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   132	    "materiality": "material"
   133	  },
   134	  {
   135	    "id": "2.5.2.1",
   136	    "proposition": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением",
   137	    "party": "both/neutral",
   138	    "right_or_obligation": "declaration",
   139	    "object": "SberPay",
   140	    "trigger": "standing obligation",
   141	    "material_terms": "none explicit",
   142	    "applicability": "in_scope",
   143	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   144	    "materiality": "material"
   145	  },
   146	  {
   147	    "id": "2.6.1.1",
   148	    "proposition": "Для приема QR на смарт-терминал не нужно отдельное ПО",
   149	    "party": "both/neutral",
   150	    "right_or_obligation": "declaration",
   151	    "object": "QR-code",
   152	    "trigger": "standing obligation",
   153	    "material_terms": "none explicit",
   154	    "applicability": "in_scope",
   155	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
   156	    "materiality": "material"
   157	  },
   158	  {
   159	    "id": "2.6.2.1",
   160	    "proposition": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре.  Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка",
   161	    "party": "both/neutral",
   162	    "right_or_obligation": "declaration",
   163	    "object": "QR-code",
   164	    "trigger": "connection of service",
   165	    "material_terms": "none explicit",
   166	    "applicability": "in_scope",
   167	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   168	    "materiality": "material"
   169	  },
   170	  {
   171	    "id": "2.6.2.2",
   172	    "proposition": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия",
   173	    "party": "both/neutral",
   174	    "right_or_obligation": "declaration",
   175	    "object": "QR-code",
   176	    "trigger": "standing obligation",
   177	    "material_terms": "none explicit",
   178	    "applicability": "in_scope",
   179	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   180	    "materiality": "material"
   181	  },
   182	  {
   183	    "id": "2.6.3.1",
   184	    "proposition": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке",
   185	    "party": "both/neutral",
   186	    "right_or_obligation": "declaration",
   187	    "object": "QR-code",
   188	    "trigger": "connection of service",
   189	    "material_terms": "none explicit",
   190	    "applicability": "in_scope",
   191	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   192	    "materiality": "material"
   193	  },
   194	  {
   195	    "id": "2.6.3.2",
   196	    "proposition": "Данный риск относится только к терминалам предоставленным Банком. Для отключения QR-кода необходимо обращение в банк",
   197	    "party": "both/neutral",
   198	    "right_or_obligation": "declaration",
   199	    "object": "QR-code",
   200	    "trigger": "connection of service",
Tool:      1	[
     2	  {
     3	    "id": "Preamble",
     4	    "proposition": "Контракт №_________. Федеральное государственное бюджетное учреждение «Кавказский государственный природный биосферный заповедник имени Х.Г. Шапошникова» (Заказчик) и Банк/Исполнитель. Заключен с соблюдением требований Федерального закона № 44-ФЗ.",
     5	    "party": "neutral/definitional",
     6	    "right_or_obligation": "declaration",
     7	    "object": "general",
     8	    "trigger": "upon event",
     9	    "material_terms": "",
    10	    "applicability": "in_scope",
    11	    "applicability_reason": "contract clause",
    12	    "materiality": "heading"
    13	  },
    14	  {
    15	    "id": "1.1",
    16	    "proposition": "Исполнитель обязуется оказать Заказчику услуги по приему к оплате платежных (банковских) карт (услуги эквайринга) в соответствии с Техническим заданием (Приложение №1) и Спецификацией (Приложение №2). Заказчик обязуется принять и оплатить услуги.",
    17	    "party": "Исполнитель (obligation-bearer)",
    18	    "right_or_obligation": "obligation",
    19	    "object": "payment for services",
    20	    "trigger": "standing",
    21	    "material_terms": "",
    22	    "applicability": "in_scope",
    23	    "applicability_reason": "contract clause",
    24	    "materiality": "material"
    25	  },
    26	  {
    27	    "id": "1.2",
    28	    "proposition": "Объем услуг определяется потребностью Заказчика на сумму, не превышающую максимальную цену контракта (п.3.1).",
    29	    "party": "neutral/definitional",
    30	    "right_or_obligation": "declaration",
    31	    "object": "general",
    32	    "trigger": "upon event",
    33	    "material_terms": "",
    34	    "applicability": "in_scope",
    35	    "applicability_reason": "contract clause",
    36	    "materiality": "material"
    37	  },
    38	  {
    39	    "id": "1.3",
    40	    "proposition": "Заказчик организует прием карт в качестве средства оплаты за реализуемые им товары/услуги и обработку информации на электронных терминалах.",
    41	    "party": "neutral/definitional",
    42	    "right_or_obligation": "declaration",
    43	    "object": "electronic terminals",
    44	    "trigger": "upon event",
    45	    "material_terms": "",
    46	    "applicability": "in_scope",
    47	    "applicability_reason": "contract clause",
    48	    "materiality": "material"
    49	  },
    50	  {
    51	    "id": "2.1",
    52	    "proposition": "Авторизация – процедура получения разрешения от банка-эмитента на проведение операции.",
    53	    "party": "neutral/definitional",
    54	    "right_or_obligation": "declaration",
    55	    "object": "general",
    56	    "trigger": "upon event",
    57	    "material_terms": "",
    58	    "applicability": "in_scope",
    59	    "applicability_reason": "contract clause",
    60	    "materiality": "material"
    61	  },
    62	  {
    63	    "id": "2.1.1",
    64	    "proposition": "банковская карта (карта) – расчетная (дебетовая), кредитная или предоплаченная карта с логотипом платежной системы.",
    65	    "party": "neutral/definitional",
    66	    "right_or_obligation": "declaration",
    67	    "object": "general",
    68	    "trigger": "upon event",
    69	    "material_terms": "",
    70	    "applicability": "in_scope",
    71	    "applicability_reason": "contract clause",
    72	    "materiality": "technical"
    73	  },
    74	  {
    75	    "id": "2.1.2",
    76	    "proposition": "банк-эквайрер - кредитная организация, организующая точки приема карт.",
    77	    "party": "neutral/definitional",
    78	    "right_or_obligation": "declaration",
    79	    "object": "general",
    80	    "trigger": "upon event",
    81	    "material_terms": "",
    82	    "applicability": "in_scope",
    83	    "applicability_reason": "contract clause",
    84	    "materiality": "technical"
    85	  },
    86	  {
    87	    "id": "2.1.3",
    88	    "proposition": "банк-эмитент – кредитная организация, осуществляющая эмиссию карт.",
    89	    "party": "neutral/definitional",
    90	    "right_or_obligation": "declaration",
    91	    "object": "general",
    92	    "trigger": "upon event",
    93	    "material_terms": "",
    94	    "applicability": "in_scope",
    95	    "applicability_reason": "contract clause",
    96	    "materiality": "technical"
    97	  },
    98	  {
    99	    "id": "2.1.4",
   100	    "proposition": "возврат платежа – операция, инициируемая банком-эмитентом, оспаривающая предъявленную операцию.",
   101	    "party": "neutral/definitional",
   102	    "right_or_obligation": "declaration",
   103	    "object": "general",
   104	    "trigger": "upon event",
   105	    "material_terms": "",
   106	    "applicability": "in_scope",
   107	    "applicability_reason": "contract clause",
   108	    "materiality": "technical"
   109	  },
   110	  {
   111	    "id": "2.1.5",
   112	    "proposition": "держатель карты – покупатель-физическое лицо, на имя которого выпущена карта.",
   113	    "party": "neutral/definitional",
   114	    "right_or_obligation": "declaration",
   115	    "object": "general",
   116	    "trigger": "upon event",
   117	    "material_terms": "",
   118	    "applicability": "in_scope",
   119	    "applicability_reason": "contract clause",
   120	    "materiality": "technical"
   121	  },
   122	  {
   123	    "id": "2.1.6",
   124	    "proposition": "документ по операции - документ на бумажном носителе или в электронном виде для расчетов по операциям.",
   125	    "party": "neutral/definitional",
   126	    "right_or_obligation": "declaration",
   127	    "object": "general",
   128	    "trigger": "upon event",
   129	    "material_terms": "",
   130	    "applicability": "in_scope",
   131	    "applicability_reason": "contract clause",
   132	    "materiality": "technical"
   133	  },
   134	  {
   135	    "id": "2.1.7",
   136	    "proposition": "код авторизации - буквенно-цифровой код, подтверждающий успешное проведение авторизации.",
   137	    "party": "neutral/definitional",
   138	    "right_or_obligation": "declaration",
   139	    "object": "authorization",
   140	    "trigger": "upon event",
   141	    "material_terms": "",
   142	    "applicability": "in_scope",
   143	    "applicability_reason": "contract clause",
   144	    "materiality": "technical"
   145	  },
   146	  {
   147	    "id": "2.1.8",
   148	    "proposition": "контрольно-кассовая техника (ККТ) – программно-технические средства.",
   149	    "party": "neutral/definitional",
   150	    "right_or_obligation": "declaration",
   151	    "object": "general",
   152	    "trigger": "upon event",
   153	    "material_terms": "",
   154	    "applicability": "in_scope",
   155	    "applicability_reason": "contract clause",
   156	    "materiality": "technical"
   157	  },
   158	  {
   159	    "id": "2.1.9",
   160	    "proposition": "контрольная лента - отчет электронного терминала.",
   161	    "party": "neutral/definitional",
   162	    "right_or_obligation": "declaration",
   163	    "object": "electronic terminals",
   164	    "trigger": "upon event",
   165	    "material_terms": "",
   166	    "applicability": "in_scope",
   167	    "applicability_reason": "contract clause",
   168	    "materiality": "technical"
   169	  },
   170	  {
   171	    "id": "2.1.10",
   172	    "proposition": "отложенный платеж - операция оплаты на основании сообщения о задолженности.",
   173	    "party": "neutral/definitional",
   174	    "right_or_obligation": "declaration",
   175	    "object": "general",
   176	    "trigger": "upon event",
   177	    "material_terms": "",
   178	    "applicability": "in_scope",
   179	    "applicability_reason": "contract clause",
   180	    "materiality": "technical"
   181	  },
   182	  {
   183	    "id": "2.1.11",
   184	    "proposition": "операция – действие на электронном терминале: операция оплаты, отмены, возврата.",
   185	    "party": "neutral/definitional",
   186	    "right_or_obligation": "declaration",
   187	    "object": "electronic terminals",
   188	    "trigger": "upon event",
   189	    "material_terms": "",
   190	    "applicability": "in_scope",
   191	    "applicability_reason": "contract clause",
   192	    "materiality": "material"
   193	  },
   194	  {
   195	    "id": "2.1.12",
   196	    "proposition": "операция оплаты – операция по оплате товаров/услуг с использованием карты с проведением авторизации.",
   197	    "party": "neutral/definitional",
   198	    "right_or_obligation": "declaration",
   199	    "object": "payment for services",
   200	    "trigger": "upon event",
AI: Let me continue reading the remaining documents to get the full picture.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 500}, 'id': 'call_00_2lASBDq8dzuqw1VTjSCh0256', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 500}, 'id': 'call_01_A0iCaRal4isHzXxfU9A89719', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 200, 'limit': 500}, 'id': 'call_02_ZZYKXc0R7b8CXv8Lh4LU2029', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'offset': 200, 'limit': 500}, 'id': 'call_03_LSefYvEew6bcXbZFBPCH7531', 'type': 'tool_call'}]
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
Tool:    201	г) 100000 рублей, если цена контракта превышает 100 млн. рублей.
   202	7.5. В случае просрочки исполнения Исполнителем обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом, а также в иных случаях неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных Контрактом, Заказчик направляет Исполнителю требование об уплате неустоек (штрафов, пеней).
   203	7.6. Пеня начисляется за каждый день просрочки исполнения Исполнителем обязательства, предусмотренного Контрактом, начиная со дня, следующего за днем истечения установленного Контрактом срока исполнения обязательства,  в размере 1/300 действующей на дату уплаты пеней ключевой ставки Центрального банка Российской Федерации от цены контракта, уменьшенной на сумму, пропорциональную объему обязательств, предусмотренных Контрактом (соответствующим отдельным этапом исполнения контракта) и фактически исполненных Исполнителем, за исключением случаев, если законодательством РФ установлен иной порядок начисления пени.
   204	7.7. Штрафы начисляются за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, за исключением просрочки исполнения Исполнителем обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом. 
   205	7.7.1. Размер штрафа по каждому факту неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом, и за исключением случаев, если законодательством РФ установлен иной порядок начисления пени, устанавливается в соответствии с Постановлением № 1042 в следующем порядке:
   206	а) 10 процентов цены контракта (этапа) в случае, если цена контракта (этапа) не превышает 3 млн. рублей;
   207	б) 5 процентов цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   208	в) 1 процент цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   209	г) 0,5 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 100 млн. рублей до 500 млн. рублей (включительно);
   210	д) 0,4 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 500 млн. рублей до 1 млрд. рублей (включительно);
   211	е) 0,3 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 1 млрд. рублей до 2 млрд. рублей (включительно);
   212	ж) 0,25 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 2 млрд. рублей до 5 млрд. рублей (включительно);
   213	з) 0,2 процента цены контракта (этапа) в случае, если цена контракта (этапа) составляет от 5 млрд. рублей до 10 млрд. рублей (включительно);
   214	и) 0,1 процента цены контракта (этапа) в случае, если цена контракта (этапа) превышает 10 млрд. рублей.
   215	7.7.2. Размер штрафа Исполнителем как победителя закупки (или иного участника закупки в случаях, установленных Федеральным законом от 05.04.2013 № 44-ФЗ), предложившего наиболее высокую цену за право заключения контракта, по каждому факту неисполнения или ненадлежащего исполнения Исполнителем обязательств, предусмотренных Контрактом, за исключением просрочки исполнения обязательств (в том числе гарантийного обязательства), предусмотренных Контрактом, устанавливается в соответствии с Постановлением № 1042 в следующем порядке:
   216	а) в случае, если цена контракта не превышает начальную (максимальную) цену контракта:
   217	10 процентов начальной (максимальной) цены контракта, если цена контракта не превышает 3 млн. рублей;
   218	5 процентов начальной (максимальной) цены контракта, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   219	1 процент начальной (максимальной) цены контракта, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   220	б) в случае, если цена контракта превышает начальную (максимальную) цену контракта:
   221	10 процентов цены контракта, если цена контракта не превышает 3 млн. рублей;
   222	5 процентов цены контракта, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   223	1 процент цены контракта, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно).
   224	7.7.3. Размер штрафа по каждому факту неисполнения или ненадлежащего исполнения Исполнителем обязательства, предусмотренного Контрактом, которое не имеет стоимостного выражения (при наличии в Контракте таких обязательств), устанавливается в соответствии с Постановлением № 1042 в следующем порядке:
   225	а) 1000 рублей, если цена контракта не превышает 3 млн. рублей (включительно);
   226	б) 5000 рублей, если цена контракта составляет от 3 млн. рублей до 50 млн. рублей (включительно);
   227	в) 10000 рублей, если цена контракта составляет от 50 млн. рублей до 100 млн. рублей (включительно);
   228	г) 100000 рублей, если цена контракта превышает 100 млн. рублей.
   229	7.8. В случае обмена документами при применении мер ответственности и совершении иных действий в связи с нарушением Исполнителем или Заказчиком условий Контракта, такой обмен осуществляется с использованием ЕИС путем направления электронных уведомлений. Такие уведомления формируются с использованием ЕИС, подписываются усиленной электронной подписью лица, имеющего право действовать от имени Заказчика или Исполнителя соответственно, и размещаются в ЕИС без размещения на официальном сайте.
   230	7.9.   Применение неустойки (штрафа, пени) не освобождает Стороны от исполнения обязательств по Контракту.
   231	7.10. Общая сумма начисленных штрафов за неисполнение или ненадлежащее исполнение Исполнителем обязательств, предусмотренных Контрактом, не может превышать цену Контракта.
   232	7.11. Общая сумма начисленных штрафов за ненадлежащее исполнение Заказчиком обязательств, предусмотренных Контрактом, не может превышать цену Контракта.
   233	7.12. В случае расторжения Контракта в связи с односторонним отказом Стороны от исполнения Контракта другая Сторона вправе потребовать возмещения только фактически понесенного ущерба, непосредственно обусловленного обстоятельствами, являющимися основанием для принятия решения об одностороннем отказе от исполнения Контракта сверх начисленных неустоек.
   234	
   235	8. КАЧЕСТВО ОКАЗАННЫХ УСЛУГ, ПОРЯДОК ИХ ПРИЕМКИ. 
   236	ГАРАНТИЯ КАЧЕСТВА УСЛУГ
   237	
   238	8.1. Исполнитель гарантирует Заказчику качество оказанных услуг, предусмотренных требованиями Приложения №1 в течение всего срока, установленного нормативно-правовыми актами Российской Федерации. 
   239	8.2. Исполнитель несёт ответственность за повреждения, возникшие вследствие оказания услуг его специалистами.
   240	8.3. Приемка результата исполнения Контракта осуществляется в порядке, установленном законодательством Российской Федерации и настоящим Контрактом.
   241	8.3.1. Исполнитель ежемесячно, не позднее 10 (десятого) рабочего дня месяца, следующего за отчетным, формирует с использованием единой информационной системы, подписывает усиленной квалифицированной электронной подписью (далее – усиленной электронной подписью) лица, имеющего право действовать от имени Исполнителя, и размещает в единой информационной системе документ о приемке, который должен содержать:
   242	а) включенные в контракт в соответствии с пунктом 1 части 2 статьи 51 Федерального закона № 44-ФЗ идентификационный код закупки, наименование, место нахождения заказчика, наименование объекта закупки, место оказания услуги, информацию о Исполнителе, предусмотренную подпунктами "а", "г" и "е" части 1 статьи 43 Федерального закона № 44-ФЗ, единицу измерения поставленного товара (при осуществлении закупки товара);
   243	б) наименование оказанной услуги;
   244	д) информацию об объеме оказанной услуги;
   245	е) стоимость исполненных Исполнителем обязательств, предусмотренных контрактом, с указанием цены за единицу оказанной услуги;
   246	ж) иную информацию (с учетом требований, установленных в соответствии с частью 3 статьи 5 Федерального закона № 44-ФЗ).
   247	8.3.2. К документу о приемке, предусмотренному пунктом 8.3.1. Контракта, Исполнитель прилагает документы, предусмотренные Контрактом, которые считаются его неотъемлемой частью: счет-фактуру (при наличии), акт о перечислении Заказчику сумм операций по картам и счет ф.363 на оплату услуг за проведение расчетов по Операциям оплаты за Отчетный месяц.
   248	При этом в случае, если информация, содержащаяся в прилагаемых документах, не соответствует информации, содержащейся в документе о приемке, приоритет имеет предусмотренная пунктом 8.3.1 Контракта информация, содержащаяся в документе о приемке.
   249	8.4. Датой поступления Заказчику документа о приемке, подписанного Исполнителем, считается дата размещения в соответствии с пунктом 8.3.1. Контракта такого документа в единой информационной системе в соответствии с часовой зоной, в которой расположен Заказчик.
   250	8.5. Приемка услуг от имени Заказчика производится уполномоченным лицом, (либо приемочной комиссией – п. 8.5.8) в следующем порядке:
   251	8.5.1. Заказчик в срок не более 10 (десяти) рабочих дней со дня поступления документа о приемке в соответствии с пунктом 3 части 13 статьи 94  Федерального закона № 44-ФЗ, пунктом 8.3.1. Контракта Заказчик подписывает усиленной электронной подписью лица, имеющего право действовать от имени Заказчика, и размещает в ЕИС документ о приемке либо формирует с использованием ЕИС, подписывает усиленной электронной подписью лица, имеющего право действовать от имени заказчика, и размещает в ЕИС мотивированный отказ от подписания документа о приемке с указанием причин такого отказа.
   252	8.5.2. По письменному уведомлению Исполнителем Заказчика, приемка оказанных услуг может производиться только в присутствии представителя Исполнителя, имеющего надлежащим образом оформленные документы на участие в приемке с точно оговоренными полномочиями. О намерении принять участие в приемке Исполнитель обязан сообщить до момента окончания оказания услуг Заказчику, указав в письменном уведомлении дату в пределах установленного п. 8.5.1 срока, но не позднее чем за 15 рабочих дней до истечения срока приемки, предусмотренного Контрактом. 
   253	8.5.3. В случае, если поступило уведомление об участии в приемке в установленный Контрактом срок, приемка оказанных услуг производится только в двустороннем порядке.
   254	8.5.4. В случае, если уведомление об участии в приемке не поступило, либо поступило в более поздний срок, чем предусмотрено Контрактом, приемка оказанных услуг производится только Заказчиком в одностороннем порядке.
   255	8.5.5. Для проверки оказанных услуг, предусмотренных Контрактом, в части их соответствия условиям Контракта, Заказчик проводит экспертизу. 
   256	8.5.6. Экспертиза результатов, предусмотренных Контрактом, может проводиться Заказчиком своими силами или к ее проведению могут привлекаться эксперты, экспертные организации на основании контрактов, заключенных в соответствии с Федеральным законом № 44-ФЗ.
   257	8.5.7. В случае отсутствия замечаний Заказчик (уполномоченное лицо) в течение десяти рабочих дней с даты, следующей за днем поступления документа о приемке в соответствии с пунктом 8.4 Контракта подписывает усиленной электронной подписью лица, имеющего право действовать от имени Заказчика, и размещает в единой информационной системе документ о приемке.
   258	8.5.8. В случае, если уполномоченным лицом будут установлены несоответствия требованиям, указанным в Контракте, дальнейшая приемка может осуществляться приемочной комиссией.
   259	Не позднее десяти рабочих дней, следующих за днем поступления Заказчику документа о приемке в соответствии с пунктом 8.4 Контракта:
   260	а) члены приемочной комиссии подписывают усиленными электронными подписями решение приемочной комиссии в составе поступившего документа о приемке или формируют с использованием единой информационной системы, подписывают усиленными электронными подписями мотивированный отказ от подписания документа о приемке с указанием причин такого отказа.
   261	б) После подписания членами приемочной комиссии в соответствии с подпунктом «а» настоящего пункта документа о приемке или мотивированного отказа от подписания документа о приемке Заказчик подписывает документ о приемке или мотивированный отказ от подписания документа о приемке усиленной электронной подписью лица, имеющего право действовать от имени Заказчика, и размещает их в единой информационной системе. 
   262	в) Датой поступления Исполнителю документа о приемке, мотивированного отказа от подписания документа о приемке считается дата размещения в соответствии с настоящим пунктом таких документа о приемке, мотивированного отказа в единой информационной системе в соответствии с часовой зоной, в которой расположен Исполнитель.
   263	8.5.9. В случае получения в соответствии с пунктом 8.5.8. Контракта мотивированного отказа от подписания документа о приемке Исполнитель вправе устранить причины, указанные в таком мотивированном отказе, и направить заказчику исправленный документ о приемке в порядке, предусмотренном настоящим разделом Контракта.
   264	8.6. Датой приемки оказанных услуг считается дата размещения в единой информационной системе документа о приемке, подписанного уполномоченным лицом или приемочной комиссией Заказчика.
   265	8.7. Внесение исправлений в документ о приемке, оформленный в соответствии с настоящим разделом Контракта, осуществляется путем формирования, подписания усиленными электронными подписями уполномоченных лиц, имеющих право действовать от имени Исполнителя, Заказчика, и размещения в единой информационной системе исправленного документа о приемке.
   266	8.8. Оформление результата проведения процедуры приемки оказанных услуг осуществляется в порядке и в сроки, указанные в настоящем разделе Контракта.
   267	8.9. В случае выявления несоответствия оказанной услуги условиям Контракта Заказчик вправе не отказывать в приемке оказанной услуги, если выявленное несоответствие не препятствует приемке и устранено Исполнителем.
   268	8.10. В случае оказания услуг ненадлежащего качества Исполнитель обязан безвозмездно устранить недостатки в течение 3 дней с даты заявления о них Заказчиком.
   269	8.11. Подписанный усиленными электронными подписями Заказчика и Исполнителя документ о приемке является основанием для оплаты Исполнителю оказанных услуг.
   270	
   271	9. ДЕЙСТВИЕ ОБСТОЯТЕЛЬСТВ НЕПРЕОДОЛИМОЙ СИЛЫ
   272	
   273	9.1. Стороны освобождаются от ответственности за частичное или полное неисполнение своих обязательств по настоящему контракту, если их исполнению препятствует чрезвычайное и непреодолимое при данных условиях обстоятельство (непреодолимая сила), а именно: стихийные бедствия, наводнения, землетрясения, пожары, военные действия, забастовки, массовые заболевания(эпидемия), повлекшие введение режима повышенной готовности или чрезвычайной ситуации.
   274	9.2. При возникновении обстоятельств непреодолимой силы, препятствующих исполнению обязательств по настоящему контракту одной из Сторон, она обязана оповестить другую Сторону не позднее пяти дней с момента возникновения таких обстоятельств, при этом срок выполнения обязательств по контракту переносится соразмерно времени, в течение которого действовали такие обстоятельства. В случае если такие обстоятельства длятся более одного календарного месяца Стороны праве расторгнуть настоящий контракт по соглашению Сторон.
   275	9.3. При рассмотрении споров в связи с обстоятельствами непреодолимой силы сторона, ссылающаяся на эти обстоятельства, обязана представить документальное подтверждение их наступления (выданный лицом, уполномоченным выдавать такие документы).
   276	
   277	10. ПОРЯДОК РАЗРЕШЕНИЯ СПОРОВ
   278	
   279	10.1. Все споры или разногласия, возникающие между Сторонами по настоящему контракту или в связи с ним, разрешаются путем переговоров (в досудебном порядке).
   280	Срок ответа на претензии, письма и обращения – 10 (десять) календарных дней с даты их получения. Любое уведомление, которое одна Сторона направляет другой Стороне в соответствии с Контрактом, высылается в письменном виде, заказным письмом или доставляется лично по юридическим (почтовым) адресам другой Стороны с подтверждением о получении.
   281	В случае обмена документами при применении мер ответственности и совершении иных действий в связи с нарушением Исполнителем или заказчиком условий контракта в отношении контракта, заключенного по результатам электронных процедур, такой обмен осуществляется с использованием единой информационной системы путем направления электронных уведомлений. Такие уведомления формируются с использованием единой информационной системы, подписываются усиленной электронной подписью лица, имеющего право действовать от имени заказчика, исполнителя и размещаются в единой информационной системе без размещения на официальном сайте.
   282	10.2. В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в Арбитражном суде Краснодарского края.
   283	
   284	11. СРОК ДЕЙСТВИЯ, ПОРЯДОК ИЗМЕНЕНИЯИРАСТОРЖЕНИЯ КОНТРАКТА
   285	
   286	11.1. Настоящий контракт действует с даты заключения по 30 декабря 2025 года, или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее, а по обязательствам, возникшим в период действия настоящего Контракта, но не исполненным до окончания срока действия Контракта – до полного исполнения принятых сторонами обязательств. Окончание срока действия контракта не освобождает Стороны от ответственности за его нарушение.
   287	11.2. Любые изменения и дополнения к настоящему контракту имеют силу только в том случае, если они оформлены в письменном виде и подписаны обеими Сторонами. В случае изменения у какой - либо из Сторон места нахождения, названия она обязана в течение двух дней письменно известить об этом другую Сторону.
   288	11.3. Расторжение контракта допускается по соглашению Сторон, по решению суда, в случае одностороннего отказа Стороны контракта от исполнения контракта в соответствии с гражданским законодательством Российской Федерации.
   289	11.4. Заказчик вправе принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Гражданским кодексом Российской Федерации для одностороннего отказа от исполнения отдельных видов обязательств.
   290	11.5. Решение Сторон об одностороннем отказе от исполнения контракта по основаниям, предусмотренным ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств, принимается и реализуется в порядке и сроки, предусмотренные статьей 95 Федерального закона № 44-ФЗ.
   291	11.6. Изменение и(или) расторжение контракта осуществляется в порядке, сроки, случаях и на условиях, установленных статьями 34, 95, 96, 112 Федерального закона № 44-ФЗ.
   292	11.7. Во всем, что не предусмотрено настоящим контрактом, Стороны руководствуются действующим законодательством Российской Федерации.
   293	11.8. Стороны предусмотрели, что изменение существенных условий контракта при его исполнении не допускается, за исключением их изменения по соглашению Сторон в случаях, предусмотренных Федеральным законом № 44-ФЗ.
   294	
   295	12. ПРОЧИЕ УСЛОВИЯ
   296	
   297	12.1. При исполнении настоящего контракта не допускается перемена Исполнителя, за исключением случая, когда новый исполнитель является правопреемником Исполнителя по контракту вследствие реорганизации юридического лица в форме преобразования, слияния или присоединения.
   298	12.2. В случае перемены Заказчика по контракту права и обязанности Заказчика по настоящему контракту переходят к новому Заказчику в том же объеме и на тех же условиях.
   299	12.3. При исполнении контракта по согласованию Заказчика с Исполнителем допускается оказание услуги, качество, технические и функциональные характеристики (потребительские свойства) которых являются улучшенными по сравнению с качеством и соответствующими техническими и функциональными характеристиками, указанными в контракте.
   300	12.4. Контракт составлен в электронной форме и подписан усиленной квалифицированной электронной подписью Сторон. 
   301	
   302	
   303	13. МЕСТА НАХОЖДЕНИЯ, БАНКОВСКИЕ РЕКВИЗИТЫСТОРОН
   304	
   305	
   306	
   307	
   308	
   309	Приложение № 1
   310	к контракту на оказание услуг 
   311	от _____________ № _______
   312	
   313	Техническое задание
   314	
   315	Оказание услуг по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)
   316	
   317	Объектом закупки является: Оказание услуг по приему к оплате платежных (банковских) карт в качестве средства оплаты услуг с использованием банковских карт (услуги эквайринга)  (далее по тексту- услуга, эквайринг) для нужд Федерального государственного бюджетного учреждения «Кавказский государственный природный биосферный заповедник имени Х. Г. Шапошникова» (далее - Заказчик). 
   318	Платежно-пропускная система, установленная у Заказчика - «Барс» НПО «Дата Крат». 
   319	2. Местоположение точек приема Заказчика установки электронных терминалов и оказания услуг, а также количество необходимых электронных терминалов (POS-терминалов):
   320	Данный перечень объектов Заказчика не является исчерпывающим и может изменяться.
   321	
   322	3. Перечень карт, которые сервисная точка принимает в оплату услуг:
   323	
   324	4. Сроки оказания Услуг: Оказание услуг осуществляется с «01» марта 2025 года по «30» ноября 2025 года (включительно) или до момента исчерпания предельной Цены Контракта, указанной в п. № 3.1. Контракта, в зависимости от того, какое из событий условие наступит ранее.
   325	5. Условия оказания услуг:
   326	Комиссия за предоставление терминалов- отсутствует.
   327	Абонентская плата за пользование терминалами - отсутствует.
   328	Терминалы Исполнителя должны иметь возможность принятия бесконтактной оплаты 
   329	Возможность вывода QR-кода для безналичной оплаты на дисплей терминала 
   330	Расчеты при совершении операций производятся в валюте Российской Федерации.
   331	Возмещение Заказчику денежных средств по операциям:
   332	- производится путем перечисления денежных средств на номер банковского счета, входящего в состав единого казначейского счета
   333	-на основании полученной от Заказчика расчетной информации, переданной от электронного терминала Исполнителю, не позднее 2 (двух) рабочих дней с даты ее получения перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты.
   334	Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.
   335	Требования к характеристикам услуг.
   336	Исполнитель должен будет: 
   337	установить и подключить к рабочим местам Заказчика бесплатно во временное пользование на весь срок действия контракта необходимое оборудование; 
   338	POS-терминалы, подбор которых осуществляет Исполнитель в соответствии с описанием объекта закупки;
   339	проводить дополнительный инструктаж сотрудников Заказчика в случае изменений порядка проведения операций с использованием банковских карт, изменения программного обеспечения, замены электронного терминала на другой вид, а также в иных случаях по письменному или устному запросу Заказчика;
   340	по Операциям возврата, Возврат платежа и Реверсивным транзакциям плата за проведение расчетов не взимается. В этом случае плата за проведение расчетов, удержанная Банком при обработке первоначальной Операции оплаты, не возвращается;
   341	 Для передачи в Банк информации о совершенных в течение дня Операциях на Электронном терминале ежедневно, не позднее 23.59.59 Московского времени, работник ТСТ должен выполнить следующие действия:
   342	a) распечатать Контрольную ленту Электронного терминала;
   343	b) инициировать закрытие смены в ККТ (в случае если Электронный терминал работает под управлением ККТ) или выбрать в меню Электронного терминала «Служебные операции» - «Сверка итогов»;
   344	c) подтвердить выбор операции «Сверка итогов» нажатием клавиши «ВВОД»;
   345	 d) распечатать Сводный чек Электронного терминала, передать Контрольную ленту и чеки ответственному работнику ТСТ для хранения.
   346	e) После проведения операции «Сверка итогов» список Операций сохраняется в памяти Электронного терминала до момента проведения следующей операции (включая «Сверку итогов»). При этом список операций обнуляется, и печать отчетов по проведенным ранее операциям станет невозможным.
   347	9.2.1 в случае несовпадения итогов или технического сбоя работник ТСТ:
   348	a) распечатывает Контрольную ленту;
   349	b) проверяет соответствие информации в Контрольной ленте с реально проведенными Операциями;
   350	c) ставит свою подпись на Контрольной ленте и передает ее ответственному работнику ТСТ.;
   351	Подключить ежедневную/еженедельную/ежемесячную (выбрать необходимую периодичность)  автоотчетность по успешно проведенным операциям на электронных терминалах  и направлять на электронную почту(ы) Заказчика _________;
   352	Объем услуг по сопровождению системы эквайринга:
   353	
   354	Приложение № 1.1
   355	        к Контракту на проведение расчетов по операциям оплаты товаров/услуг 
   356	с условием постоплаты оказанных Банком услуг
   357	 
   358	ЗАЯВЛЕНИЕ ПРЕДПРИЯТИЯ НА ПРОВЕДЕНИЕ РАСЧЕТОВ ПО ОПЕРАЦИЯМ ОПЛАТЫ ТОВАРОВ/УСЛУГ
   359	
   360	
   361	
   362	Приложение № 1..2
   363	к Контракту на проведение расчетов по операциям оплаты товаров/услуг
   364	с условием постоплаты оказанных Банком услуг
   365	
   366	ИНФОРМАЦИЯ О ТОРГОВО-СЕРВИСНОЙ ТОЧКЕ/РЕСУРСЕ ПРЕДПРИТИЯ 
   367	_________________________
   368	Информацию, указанную в настоящем документе, подтверждаю 
   369	_______________________________________________________	_______________	«__» ___________ 20____г.
   370	 (указывается ФИО руководителя/уполномоченного представителя Предприятия)	          (подпись)
   371	Отметки Банка: 
   372	Заявление принял: 
   373	_______________________________________________________	_______________	«__» ___________ 20____г.
   374	 (указывается ФИО работника Банка)			           (подпись)
   375	
   376	
   377	
   378	
   379	
   380	
   381	
   382	
   383	
   384	
   385	
   386	
   387	
   388	
   389	
   390	
   391	
   392	
   393	
   394	
   395	
   396	
   397	
   398	
   399	
   400	
   401	
   402	
   403	
   404	
   405	
   406	
   407	
   408	
   409	
   410	
   411	
   412	
   413	
   414	
   415	
   416	
   417	
   418	
   419	
   420	
   421	Приложение № 2
   422	к контракту на оказание услуг 
   423	от _____________ № _______
   424	
   425	СПЕЦФИКАЦИЯ
   426	
   427	
   428	
   429	
   430	
Tool:    201	    "material_terms": "",
   202	    "applicability": "in_scope",
   203	    "applicability_reason": "contract clause",
   204	    "materiality": "material"
   205	  },
   206	  {
   207	    "id": "2.1.13",
   208	    "proposition": "операция отмены – операция отмены авторизации до «Сверки итогов».",
   209	    "party": "neutral/definitional",
   210	    "right_or_obligation": "declaration",
   211	    "object": "authorization",
   212	    "trigger": "upon event",
   213	    "material_terms": "",
   214	    "applicability": "in_scope",
   215	    "applicability_reason": "contract clause",
   216	    "materiality": "technical"
   217	  },
   218	  {
   219	    "id": "2.1.14",
   220	    "proposition": "операция возврата – операция при возврате товаров/отказе от услуг после «Сверки итогов».",
   221	    "party": "neutral/definitional",
   222	    "right_or_obligation": "declaration",
   223	    "object": "termination/refusal",
   224	    "trigger": "upon event",
   225	    "material_terms": "",
   226	    "applicability": "in_scope",
   227	    "applicability_reason": "contract clause",
   228	    "materiality": "material"
   229	  },
   230	  {
   231	    "id": "2.1.15",
   232	    "proposition": "платежная система – совокупность организаций, взаимодействующих по правилам платежной системы.",
   233	    "party": "neutral/definitional",
   234	    "right_or_obligation": "declaration",
   235	    "object": "general",
   236	    "trigger": "upon event",
   237	    "material_terms": "",
   238	    "applicability": "in_scope",
   239	    "applicability_reason": "contract clause",
   240	    "materiality": "material"
   241	  },
   242	  {
   243	    "id": "2.1.16",
   244	    "proposition": "покупатель - физическое лицо, осуществляющее оплату товара/услуги в ТСТ.",
   245	    "party": "neutral/definitional",
   246	    "right_or_obligation": "declaration",
   247	    "object": "payment for services",
   248	    "trigger": "upon event",
   249	    "material_terms": "",
   250	    "applicability": "in_scope",
   251	    "applicability_reason": "contract clause",
   252	    "materiality": "technical"
   253	  },
   254	  {
   255	    "id": "2.1.17",
   256	    "proposition": "повторяющиеся платежи – платежи, осуществляемые регулярно в течение определенного периода.",
   257	    "party": "neutral/definitional",
   258	    "right_or_obligation": "declaration",
   259	    "object": "general",
   260	    "trigger": "upon event",
   261	    "material_terms": "",
   262	    "applicability": "in_scope",
   263	    "applicability_reason": "contract clause",
   264	    "materiality": "material"
   265	  },
   266	  {
   267	    "id": "2.1.18",
   268	    "proposition": "предавторизация - операция по резервированию денежных средств на карте.",
   269	    "party": "neutral/definitional",
   270	    "right_or_obligation": "declaration",
   271	    "object": "authorization",
   272	    "trigger": "upon event",
   273	    "material_terms": "",
   274	    "applicability": "in_scope",
   275	    "applicability_reason": "contract clause",
   276	    "materiality": "material"
   277	  },
   278	  {
   279	    "id": "2.1.19",
   280	    "proposition": "предприятие (Заказчик) – торгово-сервисное предприятие (ТСП).",
   281	    "party": "neutral/definitional",
   282	    "right_or_obligation": "declaration",
   283	    "object": "general",
   284	    "trigger": "upon event",
   285	    "material_terms": "",
   286	    "applicability": "in_scope",
   287	    "applicability_reason": "contract clause",
   288	    "materiality": "material"
   289	  },
   290	  {
   291	    "id": "2.1.20",
   292	    "proposition": "рабочий день – день, не признаваемый выходным или нерабочим праздничным.",
   293	    "party": "neutral/definitional",
   294	    "right_or_obligation": "declaration",
   295	    "object": "general",
   296	    "trigger": "upon event",
   297	    "material_terms": "",
   298	    "applicability": "in_scope",
   299	    "applicability_reason": "contract clause",
   300	    "materiality": "technical"
   301	  },
   302	  {
   303	    "id": "2.1.21",
   304	    "proposition": "реверсивная транзакция – сообщение для отмены ранее направленной транзакции.",
   305	    "party": "neutral/definitional",
   306	    "right_or_obligation": "declaration",
   307	    "object": "general",
   308	    "trigger": "upon event",
   309	    "material_terms": "",
   310	    "applicability": "in_scope",
   311	    "applicability_reason": "contract clause",
   312	    "materiality": "material"
   313	  },
   314	  {
   315	    "id": "2.1.22",
   316	    "proposition": "сводный чек электронного терминала – бумажный отчет с итоговой информацией.",
   317	    "party": "neutral/definitional",
   318	    "right_or_obligation": "declaration",
   319	    "object": "electronic terminals",
   320	    "trigger": "upon event",
   321	    "material_terms": "",
   322	    "applicability": "in_scope",
   323	    "applicability_reason": "contract clause",
   324	    "materiality": "technical"
   325	  },
   326	  {
   327	    "id": "2.1.23",
   328	    "proposition": "тарифы банка – стоимость услуг банка в виде процента от суммы операции.",
   329	    "party": "neutral/definitional",
   330	    "right_or_obligation": "declaration",
   331	    "object": "general",
   332	    "trigger": "upon event",
   333	    "material_terms": "",
   334	    "applicability": "in_scope",
   335	    "applicability_reason": "contract clause",
   336	    "materiality": "material"
   337	  },
   338	  {
   339	    "id": "2.1.24",
   340	    "proposition": "товар/услуга – товар, работа, услуга, реализуемые Заказчиком в ТСТ.",
   341	    "party": "neutral/definitional",
   342	    "right_or_obligation": "declaration",
   343	    "object": "general",
   344	    "trigger": "upon event",
   345	    "material_terms": "",
   346	    "applicability": "in_scope",
   347	    "applicability_reason": "contract clause",
   348	    "materiality": "technical"
   349	  },
   350	  {
   351	    "id": "2.1.25",
   352	    "proposition": "торгово-сервисная точка (ТСТ) – подразделение Заказчика.",
   353	    "party": "neutral/definitional",
   354	    "right_or_obligation": "declaration",
   355	    "object": "general",
   356	    "trigger": "upon event",
   357	    "material_terms": "",
   358	    "applicability": "in_scope",
   359	    "applicability_reason": "contract clause",
   360	    "materiality": "material"
   361	  },
   362	  {
   363	    "id": "2.1.26",
   364	    "proposition": "торговый эквайринг – осуществление банком-эквайрером расчетов с предприятиями.",
   365	    "party": "neutral/definitional",
   366	    "right_or_obligation": "declaration",
   367	    "object": "general",
   368	    "trigger": "upon event",
   369	    "material_terms": "",
   370	    "applicability": "in_scope",
   371	    "applicability_reason": "contract clause",
   372	    "materiality": "material"
   373	  },
   374	  {
   375	    "id": "2.1.27",
   376	    "proposition": "чек электронного терминала (чек) – документ по операции.",
   377	    "party": "neutral/definitional",
   378	    "right_or_obligation": "declaration",
   379	    "object": "electronic terminals",
   380	    "trigger": "upon event",
   381	    "material_terms": "",
   382	    "applicability": "in_scope",
   383	    "applicability_reason": "contract clause",
   384	    "materiality": "technical"
   385	  },
   386	  {
   387	    "id": "2.1.28",
   388	    "proposition": "электронная сверка итогов – процедура передачи расчетной информации.",
   389	    "party": "neutral/definitional",
   390	    "right_or_obligation": "declaration",
   391	    "object": "general",
   392	    "trigger": "upon event",
   393	    "material_terms": "",
   394	    "applicability": "in_scope",
   395	    "applicability_reason": "contract clause",
   396	    "materiality": "material"
   397	  },
   398	  {
   399	    "id": "2.2",
   400	    "proposition": "электронный терминал – электронное программно-техническое устройство исполнителя. Предоставляется исполнителем на срок действия контракта.",
   401	    "party": "neutral/definitional",
   402	    "right_or_obligation": "declaration",
   403	    "object": "electronic terminals",
   404	    "trigger": "upon event",
   405	    "material_terms": "",
   406	    "applicability": "in_scope",
   407	    "applicability_reason": "contract clause",
   408	    "materiality": "material"
   409	  },
   410	  {
   411	    "id": "2.3",
   412	    "proposition": "Банк и Заказчик обмениваются информацией и документами одним из следующих способов.",
   413	    "party": "both",
   414	    "right_or_obligation": "declaration",
   415	    "object": "document exchange",
   416	    "trigger": "upon event",
   417	    "material_terms": "",
   418	    "applicability": "in_scope",
   419	    "applicability_reason": "contract clause",
   420	    "materiality": "material"
   421	  },
   422	  {
   423	    "id": "2.3.1",
   424	    "proposition": "Обмен с использованием электронных каналов связи (email). Исключение персональных данных, коммерческой и банковской тайны. Документы имеют полную юридическую силу.",
   425	    "party": "neutral/definitional",
   426	    "right_or_obligation": "declaration",
   427	    "object": "personal data",
   428	    "trigger": "upon event",
   429	    "material_terms": "",
   430	    "applicability": "in_scope",
   431	    "applicability_reason": "contract clause",
   432	    "materiality": "material"
   433	  },
   434	  {
   435	    "id": "2.3.2",
   436	    "proposition": "Обмен посредством системы ДБО или аналогичных систем Банка.",
   437	    "party": "neutral/definitional",
   438	    "right_or_obligation": "declaration",
   439	    "object": "general",
   440	    "trigger": "upon event",
   441	    "material_terms": "",
   442	    "applicability": "in_scope",
   443	    "applicability_reason": "contract clause",
   444	    "materiality": "material"
   445	  },
   446	  {
   447	    "id": "2.3.3",
   448	    "proposition": "Обмен путем направления письма с доставкой нарочным или курьерской почтой.",
   449	    "party": "neutral/definitional",
   450	    "right_or_obligation": "declaration",
   451	    "object": "general",
   452	    "trigger": "upon event",
   453	    "material_terms": "",
   454	    "applicability": "in_scope",
   455	    "applicability_reason": "contract clause",
   456	    "materiality": "material"
   457	  },
   458	  {
   459	    "id": "2.3.4",
   460	    "proposition": "Обмен путем направления почтового отправления (заказного письма).",
   461	    "party": "neutral/definitional",
   462	    "right_or_obligation": "declaration",
   463	    "object": "general",
   464	    "trigger": "upon event",
   465	    "material_terms": "",
   466	    "applicability": "in_scope",
   467	    "applicability_reason": "contract clause",
   468	    "materiality": "material"
   469	  },
   470	  {
   471	    "id": "2.3.5",
   472	    "proposition": "Обмен электронными документами посредством автоматизированной системы _________. Документы подписываются УКЭП, равнозначны бумажным.",
   473	    "party": "neutral/definitional",
   474	    "right_or_obligation": "declaration",
   475	    "object": "general",
   476	    "trigger": "upon event",
   477	    "material_terms": "",
   478	    "applicability": "in_scope",
   479	    "applicability_reason": "contract clause",
   480	    "materiality": "material"
   481	  },
   482	  {
   483	    "id": "2.3.6",
   484	    "proposition": "Обмен электронными документами в ЕИС и иных ЭТП. Документы подписываются УКЭП, равнозначны бумажным.",
   485	    "party": "neutral/definitional",
   486	    "right_or_obligation": "declaration",
   487	    "object": "general",
   488	    "trigger": "upon event",
   489	    "material_terms": "",
   490	    "applicability": "in_scope",
   491	    "applicability_reason": "contract clause",
   492	    "materiality": "material"
   493	  },
   494	  {
   495	    "id": "2.3.7",
   496	    "proposition": "Обмен через контактные данные службы поддержки Банка (24/7).",
   497	    "party": "neutral/definitional",
   498	    "right_or_obligation": "declaration",
   499	    "object": "general",
   500	    "trigger": "upon event",
   501	    "material_terms": "",
   502	    "applicability": "in_scope",
   503	    "applicability_reason": "contract clause",
   504	    "materiality": "material"
   505	  },
   506	  {
   507	    "id": "2.3-receipt",
   508	    "proposition": "Сторона считается получившей информацию/документ: по п.2.3.1-2.3.2 – в дату направления; по п.2.3.3-2.3.4 – в дату доставки; по п.2.3.5 – в дату поступления Оператору ЭДО; по п.2.3.6 – в дату направления в ЕИС/ЭТП; по п.2.3.7 – в дату обращения в службу поддержки.",
   509	    "party": "neutral/definitional",
   510	    "right_or_obligation": "declaration",
   511	    "object": "document exchange",
   512	    "trigger": "upon event",
   513	    "material_terms": "",
   514	    "applicability": "in_scope",
   515	    "applicability_reason": "contract clause",
   516	    "materiality": "material"
   517	  },
   518	  {
   519	    "id": "3.1",
   520	    "proposition": "Максимальное значение цены контракта составляет 1 900 000,00 рублей.",
   521	    "party": "neutral/definitional",
   522	    "right_or_obligation": "declaration",
   523	    "object": "general",
   524	    "trigger": "upon event",
   525	    "material_terms": "",
   526	    "applicability": "in_scope",
   527	    "applicability_reason": "contract clause",
   528	    "materiality": "material"
   529	  },
   530	  {
   531	    "id": "3.1.1",
   532	    "proposition": "Цена за единицу услуги указана в спецификации (Приложение №1).",
   533	    "party": "neutral/definitional",
   534	    "right_or_obligation": "declaration",
   535	    "object": "contract price",
   536	    "trigger": "upon event",
   537	    "material_terms": "",
   538	    "applicability": "in_scope",
   539	    "applicability_reason": "contract clause",
   540	    "materiality": "material"
   541	  },
   542	  {
   543	    "id": "3.2",
   544	    "proposition": "Цена единицы услуги включает расходы Исполнителя за выполнение расчетов в виде процента от суммы каждой Операции оплаты.",
   545	    "party": "neutral/definitional",
   546	    "right_or_obligation": "declaration",
   547	    "object": "payment for services",
   548	    "trigger": "upon event",
   549	    "material_terms": "",
   550	    "applicability": "in_scope",
   551	    "applicability_reason": "contract clause",
   552	    "materiality": "material"
   553	  },
   554	  {
   555	    "id": "3.3",
   556	    "proposition": "Положения о цене контракта применяются к максимальному значению цены, если Федеральным законом №44-ФЗ не установлено иное.",
   557	    "party": "neutral/definitional",
   558	    "right_or_obligation": "declaration",
   559	    "object": "general",
   560	    "trigger": "upon event",
   561	    "material_terms": "",
   562	    "applicability": "in_scope",
   563	    "applicability_reason": "contract clause",
   564	    "materiality": "material"
   565	  },
   566	  {
   567	    "id": "4.1",
   568	    "proposition": "Оказание услуг с 01.03.2025 по 30.11.2025 или до исчерпания предельной Цены Контракта.",
   569	    "party": "neutral/definitional",
   570	    "right_or_obligation": "declaration",
   571	    "object": "general",
   572	    "trigger": "upon event",
   573	    "material_terms": "",
   574	    "applicability": "in_scope",
   575	    "applicability_reason": "contract clause",
   576	    "materiality": "material"
   577	  },
   578	  {
   579	    "id": "4.2",
   580	    "proposition": "Исполнитель должен соответствовать требованиям законодательства и иметь лицензию на банковские операции.",
   581	    "party": "neutral/definitional",
   582	    "right_or_obligation": "declaration",
   583	    "object": "general",
   584	    "trigger": "upon event",
   585	    "material_terms": "",
   586	    "applicability": "in_scope",
   587	    "applicability_reason": "contract clause",
   588	    "materiality": "material"
   589	  },
   590	  {
   591	    "id": "4.3",
   592	    "proposition": "Оказание услуг по адресу ТСТ. Перечень ТСТ в Приложении №1. Для регистрации новой ТСТ Заказчик предоставляет заявление и информацию о ТСТ.",
   593	    "party": "neutral/definitional",
   594	    "right_or_obligation": "declaration",
   595	    "object": "application/statement",
   596	    "trigger": "upon event",
   597	    "material_terms": "",
   598	    "applicability": "in_scope",
   599	    "applicability_reason": "contract clause",
   600	    "materiality": "material"
   601	  },
   602	  {
   603	    "id": "4.4",
   604	    "proposition": "Оплата по безналичному расчёту платежным поручением. Оплата по цене единицы услуги исходя из объема фактически оказанной услуги, не превышая максимального значения цены контракта.",
   605	    "party": "neutral/definitional",
   606	    "right_or_obligation": "declaration",
   607	    "object": "general",
   608	    "trigger": "upon event",
   609	    "material_terms": "",
   610	    "applicability": "in_scope",
   611	    "applicability_reason": "contract clause",
   612	    "materiality": "material"
   613	  },
   614	  {
   615	    "id": "4.5",
   616	    "proposition": "Срок оплаты оказанных услуг – не более 7 рабочих дней с даты подписания документа о приемке, ежемесячно.",
   617	    "party": "neutral/definitional",
   618	    "right_or_obligation": "declaration",
   619	    "object": "payment for services",
   620	    "trigger": "upon event",
   621	    "material_terms": "",
   622	    "applicability": "in_scope",
   623	    "applicability_reason": "contract clause",
   624	    "materiality": "material"
   625	  },
   626	  {
   627	    "id": "4.5.1",
   628	    "proposition": "Услуги за ноябрь оплачиваются не позднее 7 рабочих дней с даты подписания документа о приемке, но не позднее 30 декабря 2025 года.",
   629	    "party": "neutral/definitional",
   630	    "right_or_obligation": "declaration",
   631	    "object": "acceptance of services",
   632	    "trigger": "upon event",
   633	    "material_terms": "",
   634	    "applicability": "in_scope",
   635	    "applicability_reason": "contract clause",
   636	    "materiality": "material"
   637	  },
   638	  {
   639	    "id": "5.1",
   640	    "proposition": "Исполнитель обязуется:",
   641	    "party": "Исполнитель (obligation-bearer)",
   642	    "right_or_obligation": "obligation",
   643	    "object": "general",
   644	    "trigger": "standing",
   645	    "material_terms": "",
   646	    "applicability": "in_scope",
   647	    "applicability_reason": "contract clause",
   648	    "materiality": "material"
   649	  },
   650	  {
   651	    "id": "5.1.1",
   652	    "proposition": "Установить и подготовить к эксплуатации Электронные терминалы в течение 5 рабочих дней. Провести первичный инструктаж. Разместить обучающие материалы на сайте.",
   653	    "party": "neutral/definitional",
   654	    "right_or_obligation": "declaration",
   655	    "object": "terminal installation/maintenance",
   656	    "trigger": "upon event",
   657	    "material_terms": "",
   658	    "applicability": "in_scope",
   659	    "applicability_reason": "contract clause",
   660	    "materiality": "material"
   661	  },
   662	  {
   663	    "id": "5.1.2",
   664	    "proposition": "Ежемесячно формировать и направлять Заказчику документ о приемке.",
   665	    "party": "neutral/definitional",
   666	    "right_or_obligation": "declaration",
   667	    "object": "acceptance of services",
   668	    "trigger": "upon event",
   669	    "material_terms": "",
   670	    "applicability": "in_scope",
   671	    "applicability_reason": "contract clause",
   672	    "materiality": "material"
   673	  },
   674	  {
   675	    "id": "5.1.3",
   676	    "proposition": "Обеспечить соответствие оказанных услуг требованиям законодательства РФ.",
   677	    "party": "neutral/definitional",
   678	    "right_or_obligation": "declaration",
   679	    "object": "general",
   680	    "trigger": "upon event",
   681	    "material_terms": "",
   682	    "applicability": "in_scope",
   683	    "applicability_reason": "contract clause",
   684	    "materiality": "material"
   685	  },
   686	  {
   687	    "id": "5.1.4",
   688	    "proposition": "Обеспечивать круглосуточную работоспособность Электронных терминалов. При выходе из строя – замена не позднее 3 рабочих дней.",
   689	    "party": "neutral/definitional",
   690	    "right_or_obligation": "declaration",
   691	    "object": "electronic terminals",
   692	    "trigger": "upon event",
   693	    "material_terms": "",
   694	    "applicability": "in_scope",
   695	    "applicability_reason": "contract clause",
   696	    "materiality": "material"
   697	  },
   698	  {
   699	    "id": "5.1.5",
   700	    "proposition": "Предоставлять Заказчику полную и точную информацию об услугах и ходе исполнения обязательств.",
Tool:    201	    "material_terms": "none explicit",
   202	    "applicability": "in_scope",
   203	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   204	    "materiality": "material"
   205	  },
   206	  {
   207	    "id": "2.7",
   208	    "proposition": "Важен факт, что договор может быть заключен в электронном виде с подписанием УКЭП ",
   209	    "party": "both/neutral",
   210	    "right_or_obligation": "declaration",
   211	    "object": "general",
   212	    "trigger": "standing obligation",
   213	    "material_terms": "none explicit",
   214	    "applicability": "in_scope",
   215	    "applicability_reason": "product=common, lot=common, terminal=common",
   216	    "materiality": "technical"
   217	  },
   218	  {
   219	    "id": "3.1",
   220	    "proposition": "Важно подсветить разногласие, если перечислена платёжная система отличная от НСПК или МИР",
   221	    "party": "both/neutral",
   222	    "right_or_obligation": "declaration",
   223	    "object": "QR-code",
   224	    "trigger": "standing obligation",
   225	    "material_terms": "none explicit",
   226	    "applicability": "in_scope",
   227	    "applicability_reason": "product=common, lot=common, terminal=common",
   228	    "materiality": "technical"
   229	  },
   230	  {
   231	    "id": "3.2",
   232	    "proposition": "Важен сам факт обязанности Банка в перечислении сумм Предприятию",
   233	    "party": "both/neutral",
   234	    "right_or_obligation": "declaration",
   235	    "object": "service fees",
   236	    "trigger": "standing obligation",
   237	    "material_terms": "none explicit",
   238	    "applicability": "in_scope",
   239	    "applicability_reason": "product=common, lot=common, terminal=common",
   240	    "materiality": "technical"
   241	  },
   242	  {
   243	    "id": "3.3",
   244	    "proposition": "Важен сам факт, что Предприятия должно оплачивать услуги предоставляемые по договору",
   245	    "party": "both/neutral",
   246	    "right_or_obligation": "declaration",
   247	    "object": "service fees",
   248	    "trigger": "standing obligation",
   249	    "material_terms": "none explicit",
   250	    "applicability": "in_scope",
   251	    "applicability_reason": "product=common, lot=common, terminal=common",
   252	    "materiality": "material"
   253	  },
   254	  {
   255	    "id": "4.1.1",
   256	    "proposition": "Важно, если Предприятие хочет использовать в информационных материалах упоминание бренда Банка - надо согласовывать с Банком",
   257	    "party": "Предприятие (right-holder)",
   258	    "right_or_obligation": "right",
   259	    "object": "QR-code",
   260	    "trigger": "standing obligation",
   261	    "material_terms": "none explicit",
   262	    "applicability": "in_scope",
   263	    "applicability_reason": "product=common, lot=common, terminal=common",
   264	    "materiality": "material"
   265	  },
   266	  {
   267	    "id": "4.1.2",
   268	    "proposition": "Важен сам факт, что Банк оказывает консультацию заказчика по использованию оборудования",
   269	    "party": "Банк (right-holder)",
   270	    "right_or_obligation": "right",
   271	    "object": "electronic terminals",
   272	    "trigger": "standing obligation",
   273	    "material_terms": "none explicit",
   274	    "applicability": "in_scope",
   275	    "applicability_reason": "product=common, lot=common, terminal=common",
   276	    "materiality": "material"
   277	  },
   278	  {
   279	    "id": "4.1.3",
   280	    "proposition": "Важен сам факт, что QR выдаёт Банк",
   281	    "party": "Банк (right-holder)",
   282	    "right_or_obligation": "right",
   283	    "object": "QR-code",
   284	    "trigger": "standing obligation",
   285	    "material_terms": "none explicit",
   286	    "applicability": "in_scope",
   287	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   288	    "materiality": "material"
   289	  },
   290	  {
   291	    "id": "4.2.1",
   292	    "proposition": "Важен факт, что предприятие обязуется оплачивать услуги",
   293	    "party": "Предприятие (obligation-bearer)",
   294	    "right_or_obligation": "obligation",
   295	    "object": "general",
   296	    "trigger": "standing obligation",
   297	    "material_terms": "none explicit",
   298	    "applicability": "in_scope",
   299	    "applicability_reason": "product=common, lot=common, terminal=common",
   300	    "materiality": "material"
   301	  },
   302	  {
   303	    "id": "4.2.2",
   304	    "proposition": "Важно в контракте наличие формулировки о том, что Предприятие обязуется выполнять и соблюдать требования договора и инструктивных материалов. ФОрмулировка о необходимости провести инструктаж - не является требованием его соблюдать. Если ее нет, то пункты не относятся к теме матрицы",
   305	    "party": "Предприятие (obligation-bearer)",
   306	    "right_or_obligation": "obligation",
   307	    "object": "informational materials",
   308	    "trigger": "standing obligation",
   309	    "material_terms": "none explicit",
   310	    "applicability": "in_scope",
   311	    "applicability_reason": "product=common, lot=common, terminal=common",
   312	    "materiality": "material"
   313	  },
   314	  {
   315	    "id": "4.2.3",
   316	    "proposition": "Предприятие обязано самостоятельно и своевременно знакомиться с изменениями документов; Несвоевременное ознакомление не является основанием для неприменения изменений",
   317	    "party": "Предприятие (obligation-bearer)",
   318	    "right_or_obligation": "obligation",
   319	    "object": "general",
   320	    "trigger": "standing obligation",
   321	    "material_terms": "none explicit",
   322	    "applicability": "in_scope",
   323	    "applicability_reason": "product=common, lot=fz_223, terminal=common; 223-FZ lot",
   324	    "materiality": "material"
   325	  },
   326	  {
   327	    "id": "4.2.4",
   328	    "proposition": "Важен факт, если банк передает по договору предприятию - заказчику информационные материалы, то заказчик должен их разместить на видном месте, если интернет- эквайринг то в доступном для посетителя сайта месте",
   329	    "party": "Предприятие (obligation-bearer)",
   330	    "right_or_obligation": "obligation",
   331	    "object": "Resource (website)",
   332	    "trigger": "upon occurrence of specified event",
   333	    "material_terms": "none explicit",
   334	    "applicability": "in_scope",
   335	    "applicability_reason": "product=common, lot=common, terminal=common",
   336	    "materiality": "material"
   337	  },
   338	  {
   339	    "id": "4.2.5",
   340	    "proposition": "Важно, не принимать от Покупателя более 2 (двух) различных Карт. Не выдавать наличные денежные средства",
   341	    "party": "Предприятие (obligation-bearer)",
   342	    "right_or_obligation": "obligation",
   343	    "object": "service fees",
   344	    "trigger": "standing obligation",
   345	    "material_terms": "none explicit",
   346	    "applicability": "in_scope",
   347	    "applicability_reason": "product=common, lot=common, terminal=common",
   348	    "materiality": "material"
   349	  },
   350	  {
   351	    "id": "4.2.6",
   352	    "proposition": "Важен сам факт, что нельзя разбивать Операцию на нескольку сумм",
   353	    "party": "Предприятие (obligation-bearer)",
   354	    "right_or_obligation": "obligation",
   355	    "object": "general",
   356	    "trigger": "standing obligation",
   357	    "material_terms": "none explicit",
   358	    "applicability": "in_scope",
   359	    "applicability_reason": "product=common, lot=common, terminal=common",
   360	    "materiality": "material"
   361	  },
   362	  {
   363	    "id": "4.2.7",
   364	    "proposition": "Не использовать реквизиты Карты без присутствия или распоряжения Покупателя; Использовать реквизиты Карты только для проведения операций",
   365	    "party": "Предприятие (obligation-bearer)",
   366	    "right_or_obligation": "obligation",
   367	    "object": "general",
   368	    "trigger": "standing obligation",
   369	    "material_terms": "none explicit",
   370	    "applicability": "in_scope",
   371	    "applicability_reason": "product=common, lot=common, terminal=common",
   372	    "materiality": "material"
   373	  },
   374	  {
   375	    "id": "4.2.8",
   376	    "proposition": "Важно, что цена не зависит от способа оплаты",
   377	    "party": "Предприятие (obligation-bearer)",
   378	    "right_or_obligation": "obligation",
   379	    "object": "contract price",
   380	    "trigger": "standing obligation",
   381	    "material_terms": "none explicit",
   382	    "applicability": "in_scope",
   383	    "applicability_reason": "product=common, lot=common, terminal=common",
   384	    "materiality": "material"
   385	  },
   386	  {
   387	    "id": "4.2.9",
   388	    "proposition": "Заказчик несет ответственность за информацию которую он указывает в документах при проведении платежей",
   389	    "party": "Предприятие (obligation-bearer)",
   390	    "right_or_obligation": "obligation",
   391	    "object": "Resource (website)",
   392	    "trigger": "standing obligation",
   393	    "material_terms": "none explicit",
   394	    "applicability": "in_scope",
   395	    "applicability_reason": "product=common, lot=common, terminal=common",
   396	    "materiality": "material"
   397	  },
   398	  {
   399	    "id": "4.2.10",
   400	    "proposition": "Важен факт необходимости хранения документы по операциям, срок в течении которого их нужно хранить, факт передачи копий по опревцияс, а так же срок в течение которого обязаны их передать",
   401	    "party": "Предприятие (obligation-bearer)",
   402	    "right_or_obligation": "obligation",
   403	    "object": "disputes",
   404	    "trigger": "standing obligation",
   405	    "material_terms": "none explicit",
   406	    "applicability": "in_scope",
   407	    "applicability_reason": "product=common, lot=common, terminal=common",
   408	    "materiality": "material"
   409	  },
   410	  {
   411	    "id": "4.2.11",
   412	    "proposition": "Важен факт обязанности передавать заявление Банку, а так же сроки в течение которых оно должно быть передано",
   413	    "party": "Предприятие (obligation-bearer)",
   414	    "right_or_obligation": "obligation",
   415	    "object": "general",
   416	    "trigger": "standing obligation",
   417	    "material_terms": "none explicit",
   418	    "applicability": "in_scope",
   419	    "applicability_reason": "product=common, lot=common, terminal=common",
   420	    "materiality": "material"
   421	  },
   422	  {
   423	    "id": "4.2.12",
   424	    "proposition": "Важен факт обязанности Предприятия подписать закрывающие документы по оплате, а так же сроки в течение которых оно должно это сделать",
   425	    "party": "Предприятие (obligation-bearer)",
   426	    "right_or_obligation": "obligation",
   427	    "object": "general",
   428	    "trigger": "standing obligation",
   429	    "material_terms": "none explicit",
   430	    "applicability": "in_scope",
   431	    "applicability_reason": "product=common, lot=common, terminal=common",
   432	    "materiality": "material"
   433	  },
   434	  {
   435	    "id": "4.2.13",
   436	    "proposition": "Важен сам факт обязанности Предприятия возмещать все суммы и убытки, которые Банк понёс из-за Предприятия, все возмещения - в полном объеме. Сранвнить случаи в которых возникает обязанность в возмещении",
   437	    "party": "Предприятие (obligation-bearer)",
   438	    "right_or_obligation": "obligation",
   439	    "object": "general",
   440	    "trigger": "standing obligation",
   441	    "material_terms": "penalty",
   442	    "applicability": "in_scope",
   443	    "applicability_reason": "product=common, lot=common, terminal=common",
   444	    "materiality": "material"
   445	  },
   446	  {
   447	    "id": "4.2.14",
   448	    "proposition": "Важен факт предоставления подтверждающих документов, важны сроки предоставления, а так же нужно сравнить события, при которых это допустимо",
   449	    "party": "Предприятие (obligation-bearer)",
   450	    "right_or_obligation": "obligation",
   451	    "object": "general",
   452	    "trigger": "standing obligation",
   453	    "material_terms": "none explicit",
   454	    "applicability": "in_scope",
   455	    "applicability_reason": "product=common, lot=common, terminal=common",
   456	    "materiality": "material"
   457	  },
   458	  {
   459	    "id": "4.2.15",
   460	    "proposition": "Важен факт необходимости предоставлять достоверные сведения, своевременное обновление сведений. Важен факт и срок периодичного предоставления. Важен факт и срок предоставления по запросу",
   461	    "party": "Предприятие (obligation-bearer)",
   462	    "right_or_obligation": "obligation",
   463	    "object": "general",
   464	    "trigger": "standing obligation",
   465	    "material_terms": "none explicit",
   466	    "applicability": "in_scope",
   467	    "applicability_reason": "product=common, lot=common, terminal=common",
   468	    "materiality": "material"
   469	  },
   470	  {
   471	    "id": "4.2.16.1",
   472	    "proposition": "Важно, чтобы было действующее согласие на передачу ПДн руководителя Предприятия.  Состав ПДн: ФИО, адрес, паспортные данные. Важно, чтобы не была предусмотрена передача данных другим лицам / системам",
   473	    "party": "Предприятие (obligation-bearer)",
   474	    "right_or_obligation": "obligation",
   475	    "object": "personal data",
   476	    "trigger": "standing obligation",
   477	    "material_terms": "none explicit",
   478	    "applicability": "in_scope",
   479	    "applicability_reason": "product=common, lot=common, terminal=common",
   480	    "materiality": "material"
   481	  },
   482	  {
   483	    "id": "4.2.16.2",
   484	    "proposition": "Важно, что данный пункт относится ко всем сотрудникам кроме руководителя, важно наличие согласий, обязанность подтвердить наличие согласий, важен состав ПДн",
   485	    "party": "Предприятие (obligation-bearer)",
   486	    "right_or_obligation": "obligation",
   487	    "object": "personal data",
   488	    "trigger": "standing obligation",
   489	    "material_terms": "none explicit",
   490	    "applicability": "in_scope",
   491	    "applicability_reason": "product=common, lot=common, terminal=common",
   492	    "materiality": "material"
   493	  },
   494	  {
   495	    "id": "4.2.16.3",
   496	    "proposition": "Важно, что данный пункт относится только к данным по всем сотрудникам. Важен срок предоставления подтверждения",
   497	    "party": "Предприятие (obligation-bearer)",
   498	    "right_or_obligation": "obligation",
   499	    "object": "general",
   500	    "trigger": "standing obligation",
   501	    "material_terms": "none explicit",
   502	    "applicability": "in_scope",
   503	    "applicability_reason": "product=common, lot=common, terminal=common",
   504	    "materiality": "material"
   505	  },
   506	  {
   507	    "id": "4.2.17",
   508	    "proposition": "Важен сам факт обязанности соблюдения стандарта, а так же факт обязанности предоставления подтверждения",
   509	    "party": "Предприятие (obligation-bearer)",
   510	    "right_or_obligation": "obligation",
   511	    "object": "PCI DSS compliance",
   512	    "trigger": "upon Bank request",
   513	    "material_terms": "none explicit",
   514	    "applicability": "in_scope",
   515	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   516	    "materiality": "material"
   517	  },
   518	  {
   519	    "id": "4.2.18",
   520	    "proposition": "Важны факты прекращения приема к оплате Карт, снятия информационных материалов, а так же важен срок",
   521	    "party": "Предприятие (obligation-bearer)",
   522	    "right_or_obligation": "obligation",
   523	    "object": "termination",
   524	    "trigger": "standing obligation",
   525	    "material_terms": "none explicit",
   526	    "applicability": "in_scope",
   527	    "applicability_reason": "product=common, lot=common, terminal=common",
   528	    "materiality": "material"
   529	  },
   530	  {
   531	    "id": "4.2.19",
   532	    "proposition": "Важен, факт что Предприятие не должно мешать Банку, и факт, что Предприятие должно помогать Банку в расследовании",
   533	    "party": "Предприятие (obligation-bearer)",
   534	    "right_or_obligation": "obligation",
   535	    "object": "Resource (website)",
   536	    "trigger": "standing obligation",
   537	    "material_terms": "none explicit",
   538	    "applicability": "in_scope",
   539	    "applicability_reason": "product=common, lot=common, terminal=common",
   540	    "materiality": "material"
   541	  },
   542	  {
   543	    "id": "4.2.20.1",
   544	    "proposition": "Важен сам факт, что Предприятие само следит за прохождением инструктажа сотрудниками, размещенного на сайте Банка",
   545	    "party": "Предприятие (obligation-bearer)",
   546	    "right_or_obligation": "obligation",
   547	    "object": "general",
   548	    "trigger": "standing obligation",
   549	    "material_terms": "none explicit",
   550	    "applicability": "in_scope",
   551	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   552	    "materiality": "material"
   553	  },
   554	  {
   555	    "id": "4.2.20.2",
   556	    "proposition": "Важно, чтобы предприятие использовало терминалы и ПО Банка только для целей договора и по месту установки, не менять и не ремонтировать их самостоятельно и не передавать третьим лицам (кроме обслуживающей компании)",
   557	    "party": "Предприятие (obligation-bearer)",
   558	    "right_or_obligation": "obligation",
   559	    "object": "electronic terminals",
   560	    "trigger": "standing obligation",
   561	    "material_terms": "none explicit",
   562	    "applicability": "in_scope",
   563	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   564	    "materiality": "material"
   565	  },
   566	  {
   567	    "id": "4.2.20.3",
   568	    "proposition": "Важно, что если в договоре стоит запрет на предоставление доступа третьим лицам, то это разногласие",
   569	    "party": "Предприятие (obligation-bearer)",
   570	    "right_or_obligation": "obligation",
   571	    "object": "general",
   572	    "trigger": "standing obligation",
   573	    "material_terms": "none explicit",
   574	    "applicability": "in_scope",
   575	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   576	    "materiality": "material"
   577	  },
   578	  {
   579	    "id": "4.2.20.4",
   580	    "proposition": "Важно, если указано, что оборудование Предприятие без документов или акта передачи, то всё ок, разногласия нет",
   581	    "party": "Предприятие (obligation-bearer)",
   582	    "right_or_obligation": "obligation",
   583	    "object": "electronic terminals",
   584	    "trigger": "standing obligation",
   585	    "material_terms": "none explicit",
   586	    "applicability": "in_scope",
   587	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   588	    "materiality": "material"
   589	  },
   590	  {
   591	    "id": "4.2.20.5",
   592	    "proposition": "Предприятие обязано немедленно информировать Банк о выходе из строя или утрате Электронного терминала/Смарт-терминала или Мобильного устройства; Информирование осуществляется согласно пунктам 2.3.1 и 2.3.2 Договора или через службу поддержки Банка",
   593	    "party": "Предприятие (obligation-bearer)",
   594	    "right_or_obligation": "obligation",
   595	    "object": "electronic terminals",
   596	    "trigger": "standing obligation",
   597	    "material_terms": "none explicit",
   598	    "applicability": "in_scope",
   599	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   600	    "materiality": "material"
   601	  },
   602	  {
   603	    "id": "4.2.20.6",
   604	    "proposition": "вернуть терминал в течение 5 рабочих дней после расторжения договора; вернуть терминал после получения письменного/устного требования банка",
   605	    "party": "Предприятие (obligation-bearer)",
   606	    "right_or_obligation": "obligation",
   607	    "object": "electronic terminals",
   608	    "trigger": "upon contract termination",
   609	    "material_terms": "none explicit",
   610	    "applicability": "in_scope",
   611	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   612	    "materiality": "material"
   613	  },
   614	  {
   615	    "id": "4.2.20.7",
   616	    "proposition": "Важно, чтобы в соответствующем пункте договора шла речь про штраф за невозврат терминала и его размер, иначе данный пункт матрицы не относится к пункту договора",
   617	    "party": "Предприятие (obligation-bearer)",
   618	    "right_or_obligation": "obligation",
   619	    "object": "electronic terminals",
   620	    "trigger": "standing obligation",
   621	    "material_terms": "penalty; VAT",
   622	    "applicability": "in_scope",
   623	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   624	    "materiality": "material"
   625	  },
   626	  {
   627	    "id": "4.2.21.1",
   628	    "proposition": "Приступить к проведению операций на ресурсе только после успешного завершения проверки операций на тестовой среде",
   629	    "party": "Предприятие (obligation-bearer)",
   630	    "right_or_obligation": "obligation",
   631	    "object": "Resource (website)",
   632	    "trigger": "standing obligation",
   633	    "material_terms": "none explicit",
   634	    "applicability": "in_scope",
   635	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   636	    "materiality": "material"
   637	  },
   638	  {
   639	    "id": "4.2.21.2",
   640	    "proposition": "Предприятие обязано соответствовать Требованиям Банка к Ресурсу, размещенным на Официальном сайте Банка",
   641	    "party": "Предприятие (obligation-bearer)",
   642	    "right_or_obligation": "obligation",
   643	    "object": "Resource (website)",
   644	    "trigger": "standing obligation",
   645	    "material_terms": "none explicit",
   646	    "applicability": "in_scope",
   647	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   648	    "materiality": "material"
   649	  },
   650	  {
   651	    "id": "4.2.21.3",
   652	    "proposition": "Подтверждение сумм к списанию не позднее 5 календарных дней; Соответствие подтвержденной суммы фактически оказанным товарам/услугам; Соблюдение Порядка проведения операций на Ресурсе",
   653	    "party": "Предприятие (obligation-bearer)",
   654	    "right_or_obligation": "obligation",
   655	    "object": "Resource (website)",
   656	    "trigger": "standing obligation",
   657	    "material_terms": "none explicit",
   658	    "applicability": "in_scope",
   659	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   660	    "materiality": "material"
   661	  },
   662	  {
   663	    "id": "4.2.21.4",
   664	    "proposition": "Согласование дизайна Платежной страницы с Банком; Согласование электронных вариантов информационных наклеек с Банком",
   665	    "party": "Предприятие (obligation-bearer)",
   666	    "right_or_obligation": "obligation",
   667	    "object": "Resource (website)",
   668	    "trigger": "standing obligation",
   669	    "material_terms": "none explicit",
   670	    "applicability": "in_scope",
   671	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   672	    "materiality": "material"
   673	  },
   674	  {
   675	    "id": "4.2.21.5",
   676	    "proposition": "Предприятие проводит интеграцию Ресурса со СПЭП в течение 30 календарных дней с даты заключения Договора; Предприятие проводит интеграционные тесты в течение 30 календарных дней с даты заключения Договора",
   677	    "party": "Предприятие (obligation-bearer)",
   678	    "right_or_obligation": "obligation",
   679	    "object": "Resource (website)",
   680	    "trigger": "standing obligation",
   681	    "material_terms": "none explicit",
   682	    "applicability": "in_scope",
   683	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   684	    "materiality": "material"
   685	  },
   686	  {
   687	    "id": "4.2.21.6",
   688	    "proposition": "Самостоятельное обеспечение безопасности информационных ресурсов в сети интернет",
   689	    "party": "Предприятие (obligation-bearer)",
   690	    "right_or_obligation": "obligation",
   691	    "object": "Resource (website)",
   692	    "trigger": "standing obligation",
   693	    "material_terms": "none explicit",
   694	    "applicability": "in_scope",
   695	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   696	    "materiality": "material"
   697	  },
   698	  {
   699	    "id": "4.2.21.7",
   700	    "proposition": "Предоставление доступа к разделам Ресурса с ограниченным доступом по требованию Банка",
AI: Now let me read the remaining parts of both inventories and the references.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'offset': 700, 'limit': 500}, 'id': 'call_00_8iaQppei2Un2girwID7n1061', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 700, 'limit': 500}, 'id': 'call_01_fvyfn2yuf5x4zZmCJ1359074', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 200}, 'id': 'call_02_cHm2NB31AuDNPsKjhv2p7334', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 200}, 'id': 'call_03_GlVWYasKH5yMjhESwxAf7619', 'type': 'tool_call'}]
Tool:    701	    "party": "Предприятие (obligation-bearer)",
   702	    "right_or_obligation": "obligation",
   703	    "object": "Resource (website)",
   704	    "trigger": "standing obligation",
   705	    "material_terms": "none explicit",
   706	    "applicability": "in_scope",
   707	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   708	    "materiality": "material"
   709	  },
   710	  {
   711	    "id": "4.2.21.8",
   712	    "proposition": "Соблюдение правил пользования Личным кабинетом Интернет-эквайринга",
   713	    "party": "Предприятие (obligation-bearer)",
   714	    "right_or_obligation": "obligation",
   715	    "object": "Resource (website)",
   716	    "trigger": "standing obligation",
   717	    "material_terms": "none explicit",
   718	    "applicability": "in_scope",
   719	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   720	    "materiality": "material"
   721	  },
   722	  {
   723	    "id": "4.2.22",
   724	    "proposition": "Важно, чтобы в пункте было прямо указано, что он про QR-код",
   725	    "party": "Предприятие (obligation-bearer)",
   726	    "right_or_obligation": "obligation",
   727	    "object": "QR-code",
   728	    "trigger": "standing obligation",
   729	    "material_terms": "none explicit",
   730	    "applicability": "in_scope",
   731	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   732	    "materiality": "material"
   733	  },
   734	  {
   735	    "id": "4.2.23",
   736	    "proposition": "Важно, чтобы в пункте было прямо указано, что он про QR-код",
   737	    "party": "Предприятие (obligation-bearer)",
   738	    "right_or_obligation": "obligation",
   739	    "object": "QR-code",
   740	    "trigger": "standing obligation",
   741	    "material_terms": "none explicit",
   742	    "applicability": "in_scope",
   743	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   744	    "materiality": "material"
   745	  },
   746	  {
   747	    "id": "4.2.24",
   748	    "proposition": "Важно, чтобы в пункте было прямо указано, что он про QR-API",
   749	    "party": "Предприятие (obligation-bearer)",
   750	    "right_or_obligation": "obligation",
   751	    "object": "QR-API",
   752	    "trigger": "connection of service",
   753	    "material_terms": "none explicit",
   754	    "applicability": "in_scope",
   755	    "applicability_reason": "product=common, lot=common, terminal=common",
   756	    "materiality": "material"
   757	  },
   758	  {
   759	    "id": "4.2.25",
   760	    "proposition": "Важно, чтобы в пункте было прямо указано, что он про QR-API",
   761	    "party": "Предприятие (obligation-bearer)",
   762	    "right_or_obligation": "obligation",
   763	    "object": "QR-API",
   764	    "trigger": "standing obligation",
   765	    "material_terms": "none explicit",
   766	    "applicability": "in_scope",
   767	    "applicability_reason": "product=common, lot=common, terminal=common",
   768	    "materiality": "material"
   769	  },
   770	  {
   771	    "id": "4.2.26",
   772	    "proposition": "«ПРАВА И ОБЯЗАННОСТИ ПРЕДПРИЯТИЯ» → Предприятие обязуется: → В дополнение к соблюдению требований, указанных в Условиях, в том числе приложениях к Условиям, в целях осуществлении Повторяющихся платеже",
   773	    "party": "Предприятие (obligation-bearer)",
   774	    "right_or_obligation": "obligation",
   775	    "object": "recurring payments",
   776	    "trigger": "upon occurrence of specified event",
   777	    "material_terms": "none explicit",
   778	    "applicability": "in_scope",
   779	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   780	    "materiality": "material"
   781	  },
   782	  {
   783	    "id": "5.1.1.1",
   784	    "proposition": "Банк имеет право удерживать суммы операций, являющиеся недействительными",
   785	    "party": "Банк (right-holder)",
   786	    "right_or_obligation": "right",
   787	    "object": "settlement/payment",
   788	    "trigger": "standing obligation",
   789	    "material_terms": "none explicit",
   790	    "applicability": "in_scope",
   791	    "applicability_reason": "product=common, lot=common, terminal=common",
   792	    "materiality": "material"
   793	  },
   794	  {
   795	    "id": "5.1.1.2",
   796	    "proposition": "Банк имеет право удерживать ошибочно перечисленные суммы с счета Предприятия",
   797	    "party": "Банк (right-holder)",
   798	    "right_or_obligation": "right",
   799	    "object": "settlement/payment",
   800	    "trigger": "standing obligation",
   801	    "material_terms": "none explicit",
   802	    "applicability": "in_scope",
   803	    "applicability_reason": "product=common, lot=common, terminal=common",
   804	    "materiality": "material"
   805	  },
   806	  {
   807	    "id": "5.1.1.3",
   808	    "proposition": "Банк имеет право удерживать суммы операций возврата, возврата платежа, реверсивные транзакции. Важно не рассматривать пункты в которых не указана хотя бы одна из этих сумм",
   809	    "party": "Банк (right-holder)",
   810	    "right_or_obligation": "right",
   811	    "object": "settlement/payment",
   812	    "trigger": "standing obligation",
   813	    "material_terms": "none explicit",
   814	    "applicability": "in_scope",
   815	    "applicability_reason": "product=common, lot=common, terminal=common",
   816	    "materiality": "material"
   817	  },
   818	  {
   819	    "id": "5.1.1.4",
   820	    "proposition": "Банк имеет право удерживать суммы оспоренных операций или списанных со счёта испольнителя банком-эмитентом; Банк удерживает суммы оспоренных операций в случае реализации товаров/услуг Предприятием как агентом",
   821	    "party": "Банк (right-holder)",
   822	    "right_or_obligation": "right",
   823	    "object": "settlement/payment",
   824	    "trigger": "standing obligation",
   825	    "material_terms": "none explicit",
   826	    "applicability": "in_scope",
   827	    "applicability_reason": "product=common, lot=common, terminal=common",
   828	    "materiality": "material"
   829	  },
   830	  {
   831	    "id": "5.1.1.5",
   832	    "proposition": "Банк вправе удерживать штрафы из сумм Предприятия, возникшие у Банка в связи недобросовестным исполнением Заказчика контракта; Банк вправе удерживать убытки из сумм Предприятия, возникшие в связи с привлечением Банка к гражданской или административной ответственности из-за недобросовестного исполнен",
   833	    "party": "Банк (right-holder)",
   834	    "right_or_obligation": "right",
   835	    "object": "settlement/payment",
   836	    "trigger": "standing obligation",
   837	    "material_terms": "penalty",
   838	    "applicability": "in_scope",
   839	    "applicability_reason": "product=common, lot=common, terminal=common",
   840	    "materiality": "material"
   841	  },
   842	  {
   843	    "id": "5.1.1.6",
   844	    "proposition": "Возможность удержания штрафов за невозврат терминалов. ",
   845	    "party": "Банк (right-holder)",
   846	    "right_or_obligation": "right",
   847	    "object": "electronic terminals",
   848	    "trigger": "upon occurrence of specified event",
   849	    "material_terms": "penalty",
   850	    "applicability": "in_scope",
   851	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
   852	    "materiality": "material"
   853	  },
   854	  {
   855	    "id": "5.1.2",
   856	    "proposition": "Банк вправе приостанавливать авторизацию при наличии задолженности у Предприятия; Приостановка допускается до полного погашения задолженности Предприятием",
   857	    "party": "Банк (right-holder)",
   858	    "right_or_obligation": "right",
   859	    "object": "authorization",
   860	    "trigger": "standing obligation",
   861	    "material_terms": "none explicit",
   862	    "applicability": "in_scope",
   863	    "applicability_reason": "product=common, lot=common, terminal=common",
   864	    "materiality": "material"
   865	  },
   866	  {
   867	    "id": "5.1.3",
   868	    "proposition": "списание средств без дополнительного распоряжения; условие заранее данного акцепта; основание - заявление предприятия о проведении расчетов",
   869	    "party": "Банк (right-holder)",
   870	    "right_or_obligation": "right",
   871	    "object": "settlement/payment",
   872	    "trigger": "standing obligation",
   873	    "material_terms": "none explicit",
   874	    "applicability": "in_scope",
   875	    "applicability_reason": "product=common, lot=common, terminal=common",
   876	    "materiality": "material"
   877	  },
   878	  {
   879	    "id": "5.1.4",
   880	    "proposition": "указан номер расчетного счета Предприятия; указано наименование Банка, в котором у Предприятия открыт счет",
   881	    "party": "Банк (right-holder)",
   882	    "right_or_obligation": "right",
   883	    "object": "settlement/payment",
   884	    "trigger": "standing obligation",
   885	    "material_terms": "none explicit",
   886	    "applicability": "in_scope",
   887	    "applicability_reason": "product=common, lot=common, terminal=common",
   888	    "materiality": "material"
   889	  },
   890	  {
   891	    "id": "5.1.5",
   892	    "proposition": "Банк имеет право не возмещать суммы операций, проведенных с нарушением условий договора",
   893	    "party": "Банк (right-holder)",
   894	    "right_or_obligation": "right",
   895	    "object": "general",
   896	    "trigger": "standing obligation",
   897	    "material_terms": "none explicit",
   898	    "applicability": "in_scope",
   899	    "applicability_reason": "product=common, lot=common, terminal=common",
   900	    "materiality": "material"
   901	  },
   902	  {
   903	    "id": "5.1.6",
   904	    "proposition": "Банк имеет право проверять техническое состояние терминалов на территории предприятия; Банк имеет право производить замену терминалов с уведомлением заказчика за 2 рабочих дня; Банк имеет право обновлять ПО терминалов с уведомлением заказчика за 2 рабочих дня; Допускается удаленное обновление ПО тер",
   905	    "party": "Банк (right-holder)",
   906	    "right_or_obligation": "right",
   907	    "object": "electronic terminals",
   908	    "trigger": "standing obligation",
   909	    "material_terms": "none explicit",
   910	    "applicability": "in_scope",
   911	    "applicability_reason": "product=common, lot=common, terminal=common",
   912	    "materiality": "material"
   913	  },
   914	  {
   915	    "id": "5.1.7",
   916	    "proposition": "Банк имеет право передавать информацию о предприятии при выявлении подозрительных операций; Банк передает данные в Платежную систему МИР при расторжении договора из-за мошенничества; Передаваемая информация включает дату заключения и расторжения договора, причину расторжения и другие сведения о пред",
   917	    "party": "Банк (right-holder)",
   918	    "right_or_obligation": "right",
   919	    "object": "general",
   920	    "trigger": "upon occurrence of specified event",
   921	    "material_terms": "none explicit",
   922	    "applicability": "in_scope",
   923	    "applicability_reason": "product=common, lot=common, terminal=common",
   924	    "materiality": "material"
   925	  },
   926	  {
   927	    "id": "5.1.8.1",
   928	    "proposition": "нарушение Предприятием условий Договора является основанием для прекращения Авторизации и расторжения Договора",
   929	    "party": "Банк (right-holder)",
   930	    "right_or_obligation": "right",
   931	    "object": "authorization",
   932	    "trigger": "upon occurrence",
   933	    "material_terms": "none explicit",
   934	    "applicability": "in_scope",
   935	    "applicability_reason": "product=common, lot=common, terminal=common",
   936	    "materiality": "material"
   937	  },
   938	  {
   939	    "id": "5.1.8.2",
   940	    "proposition": "внесение данных Предприятия в перечень организаций и физических лиц, причастных к экстремизму, терроризму или распространению оружия массового уничтожения является основанием для прекращения Авторизации и расторжения договора",
   941	    "party": "Банк (right-holder)",
   942	    "right_or_obligation": "right",
   943	    "object": "authorization",
   944	    "trigger": "upon occurrence",
   945	    "material_terms": "none explicit",
   946	    "applicability": "in_scope",
   947	    "applicability_reason": "product=common, lot=common, terminal=common",
   948	    "materiality": "material"
   949	  },
   950	  {
   951	    "id": "5.1.8.3",
   952	    "proposition": "Банк вправе прекратить Авторизацию при подозрении на отмывание денег или финансирование терроризма",
   953	    "party": "Банк (right-holder)",
   954	    "right_or_obligation": "right",
   955	    "object": "authorization",
   956	    "trigger": "upon occurrence",
   957	    "material_terms": "none explicit",
   958	    "applicability": "in_scope",
   959	    "applicability_reason": "product=common, lot=common, terminal=common",
   960	    "materiality": "material"
   961	  },
   962	  {
   963	    "id": "5.1.8.4",
   964	    "proposition": "Банк вправе прекратить Авторизацию при несоответствии Ресурса Требованиям Банка",
   965	    "party": "Банк (right-holder)",
   966	    "right_or_obligation": "right",
   967	    "object": "authorization",
   968	    "trigger": "upon occurrence",
   969	    "material_terms": "none explicit",
   970	    "applicability": "in_scope",
   971	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   972	    "materiality": "material"
   973	  },
   974	  {
   975	    "id": "5.1.8.5",
   976	    "proposition": "Банк имеет право в одностороннем порядке прекратить проведение авторизации при осуществлении Заказчиком запрещенных видов деятельности согласно Требованиям к Ресурсу Предприятия",
   977	    "party": "Банк (right-holder)",
   978	    "right_or_obligation": "right",
   979	    "object": "authorization",
   980	    "trigger": "upon occurrence",
   981	    "material_terms": "none explicit",
   982	    "applicability": "in_scope",
   983	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
   984	    "materiality": "material"
   985	  },
   986	  {
   987	    "id": "5.1.8.6",
   988	    "proposition": "Банк имеет право прекратить проведение авторизации при получении негативной информации о предприятии от органов государственной власти; Банк имеет право расторгнуть договор при получении негативной информации о ресурсе от платежной системы",
   989	    "party": "Банк (right-holder)",
   990	    "right_or_obligation": "right",
   991	    "object": "authorization",
   992	    "trigger": "upon occurrence",
   993	    "material_terms": "none explicit",
   994	    "applicability": "in_scope",
   995	    "applicability_reason": "product=common, lot=common, terminal=common",
   996	    "materiality": "material"
   997	  },
   998	  {
   999	    "id": "5.1.8.7",
  1000	    "proposition": "Банк имеет право прекратить Авторизацию при получении информации о мошенничестве; Достаточным подтверждением мошенничества являются сведения от Банка-эмитента или Платежной системы; Подтверждение может быть получено по факсу или электронной почте",
  1001	    "party": "Банк (right-holder)",
  1002	    "right_or_obligation": "right",
  1003	    "object": "authorization",
  1004	    "trigger": "upon occurrence",
  1005	    "material_terms": "none explicit",
  1006	    "applicability": "in_scope",
  1007	    "applicability_reason": "product=common, lot=common, terminal=common",
  1008	    "materiality": "material"
  1009	  },
  1010	  {
  1011	    "id": "5.1.8.8",
  1012	    "proposition": "осуществление ремонта помещений ТСТ препятствует операциям; банк вправе прекратить авторизацию для ТСТ; банк вправе инициировать расторжение договора",
  1013	    "party": "Банк (right-holder)",
  1014	    "right_or_obligation": "right",
  1015	    "object": "authorization",
  1016	    "trigger": "upon occurrence",
  1017	    "material_terms": "none explicit",
  1018	    "applicability": "in_scope",
  1019	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
  1020	    "materiality": "material"
  1021	  },
  1022	  {
  1023	    "id": "5.1.8.9",
  1024	    "proposition": "ликвидация Предприятия; возбуждение дела о банкротстве Предприятия по закону №127-ФЗ",
  1025	    "party": "Банк (right-holder)",
  1026	    "right_or_obligation": "right",
  1027	    "object": "authorization",
  1028	    "trigger": "upon occurrence",
  1029	    "material_terms": "none explicit",
  1030	    "applicability": "in_scope",
  1031	    "applicability_reason": "product=common, lot=common, terminal=common",
  1032	    "materiality": "material"
  1033	  },
  1034	  {
  1035	    "id": "5.1.8.10",
  1036	    "proposition": "выявление недостоверных сведений о Предприятии; выявление недостоверных сведений о ТСТ; выявление недостоверных сведений о руководителе Предприятия",
  1037	    "party": "Банк (right-holder)",
  1038	    "right_or_obligation": "right",
  1039	    "object": "authorization",
  1040	    "trigger": "upon occurrence",
  1041	    "material_terms": "none explicit",
  1042	    "applicability": "in_scope",
  1043	    "applicability_reason": "product=common, lot=common, terminal=common",
  1044	    "materiality": "material"
  1045	  },
  1046	  {
  1047	    "id": "5.1.8.11",
  1048	    "proposition": "Банк имеет право прекратить проведение авторизации при несоответствии товаров/услуг роду деятельности предприятия; Банк имеет право в одностороннем порядке расторгнуть договор при выявленном несоответствии товаров/услуг заявленной деятельности",
  1049	    "party": "Банк (right-holder)",
  1050	    "right_or_obligation": "right",
  1051	    "object": "authorization",
  1052	    "trigger": "upon occurrence",
  1053	    "material_terms": "none explicit",
  1054	    "applicability": "in_scope",
  1055	    "applicability_reason": "product=common, lot=common, terminal=common",
  1056	    "materiality": "material"
  1057	  },
  1058	  {
  1059	    "id": "5.1.8.12",
  1060	    "proposition": "отсутствие операций в течение 30 календарных дней подряд является основанием для прекращения проведения авторизации и расторжения договора",
  1061	    "party": "Банк (right-holder)",
  1062	    "right_or_obligation": "right",
  1063	    "object": "authorization",
  1064	    "trigger": "upon occurrence",
  1065	    "material_terms": "none explicit",
  1066	    "applicability": "in_scope",
  1067	    "applicability_reason": "product=common, lot=common, terminal=common",
  1068	    "materiality": "material"
  1069	  },
  1070	  {
  1071	    "id": "5.1.8.13",
  1072	    "proposition": "исчерпание Цены Договора; окончание срока действия Договора",
  1073	    "party": "Банк (right-holder)",
  1074	    "right_or_obligation": "right",
  1075	    "object": "authorization",
  1076	    "trigger": "upon occurrence",
  1077	    "material_terms": "none explicit",
  1078	    "applicability": "in_scope",
  1079	    "applicability_reason": "product=common, lot=common, terminal=common",
  1080	    "materiality": "material"
  1081	  },
  1082	  {
  1083	    "id": "5.1.9",
  1084	    "proposition": "Банк имеет право осуществлять дополнительные проверки проведения Операции в ТСТ; Банк имеет право обращаться в Банк-эмитент для проверки правомерности Операции",
  1085	    "party": "Банк (right-holder)",
  1086	    "right_or_obligation": "right",
  1087	    "object": "inspections",
  1088	    "trigger": "standing obligation",
  1089	    "material_terms": "none explicit",
  1090	    "applicability": "in_scope",
  1091	    "applicability_reason": "product=common, lot=common, terminal=common",
  1092	    "materiality": "material"
  1093	  },
  1094	  {
  1095	    "id": "5.1.10",
  1096	    "proposition": "Банк имеет право проводить проверки Предприятия; Проверки проводятся для выявления мошенничества и несоответствия рода деятельности Предприятия информации о нем; Проверки включают контроль соблюдения Предприятием требований Договора к Ресурсу; Банк может осуществлять доступ к отдельным закрытым разд",
  1097	    "party": "Банк (right-holder)",
  1098	    "right_or_obligation": "right",
  1099	    "object": "inspections",
  1100	    "trigger": "standing obligation",
  1101	    "material_terms": "none explicit",
  1102	    "applicability": "in_scope",
  1103	    "applicability_reason": "product=common, lot=common, terminal=common",
  1104	    "materiality": "material"
  1105	  },
  1106	  {
  1107	    "id": "5.1.11",
  1108	    "proposition": "Банк имеет право запрашивать документы по операциям; Банк может требовать письменное заявление предприятия с обстоятельствами проведения операции; Предприятие обязано предоставить счета, чеки и иные документы по требованию банка; Обмен документами осуществляется через электронные каналы связи соглас",
  1109	    "party": "Банк (right-holder)",
  1110	    "right_or_obligation": "right",
  1111	    "object": "general",
  1112	    "trigger": "standing obligation",
  1113	    "material_terms": "none explicit",
  1114	    "applicability": "in_scope",
  1115	    "applicability_reason": "product=common, lot=common, terminal=common",
  1116	    "materiality": "material"
  1117	  },
  1118	  {
  1119	    "id": "5.1.12",
  1120	    "proposition": "Банк вправе вносить изменения в связанные документы unilateral_in_one_day_right; Опубликование изменений осуществляется на Официальном сайте Банка",
  1121	    "party": "Банк (right-holder)",
  1122	    "right_or_obligation": "right",
  1123	    "object": "general",
  1124	    "trigger": "standing obligation",
  1125	    "material_terms": "none explicit",
  1126	    "applicability": "in_scope",
  1127	    "applicability_reason": "product=common, lot=common, terminal=common",
  1128	    "materiality": "material"
  1129	  },
  1130	  {
  1131	    "id": "5.1.13",
  1132	    "proposition": "Важно именно размещение информации на сайте. Если предусмотрены иные способы уведомления, то это разногласие",
  1133	    "party": "Банк (right-holder)",
  1134	    "right_or_obligation": "right",
  1135	    "object": "general",
  1136	    "trigger": "standing obligation",
  1137	    "material_terms": "none explicit",
  1138	    "applicability": "in_scope",
  1139	    "applicability_reason": "product=common, lot=common, terminal=common",
  1140	    "materiality": "material"
  1141	  },
  1142	  {
  1143	    "id": "5.1.14",
  1144	    "proposition": "Банк имеет право направлять запросы на адрес электронной почты Предприятия; Адрес электронной почты указан в Заявлении Предприятия на проведение расчетов; Запросы направлены для получения информации по Операциям",
  1145	    "party": "Банк (right-holder)",
  1146	    "right_or_obligation": "right",
  1147	    "object": "general",
  1148	    "trigger": "standing obligation",
  1149	    "material_terms": "none explicit",
  1150	    "applicability": "in_scope",
  1151	    "applicability_reason": "product=common, lot=common, terminal=common",
  1152	    "materiality": "material"
  1153	  },
  1154	  {
  1155	    "id": "5.1.15",
  1156	    "proposition": "Банк имеет право отказать Предприятию в заключении Договора без указания причин",
  1157	    "party": "Банк (right-holder)",
  1158	    "right_or_obligation": "right",
  1159	    "object": "general",
  1160	    "trigger": "standing obligation",
  1161	    "material_terms": "none explicit",
  1162	    "applicability": "in_scope",
  1163	    "applicability_reason": "product=common, lot=common, terminal=common",
  1164	    "materiality": "material"
  1165	  },
  1166	  {
  1167	    "id": "5.1.16",
  1168	    "proposition": "Банк имеет право требовать от Предприятия предоставления документов; Перечень требуемых документов определяется законодательством",
  1169	    "party": "Банк (right-holder)",
  1170	    "right_or_obligation": "right",
  1171	    "object": "general",
  1172	    "trigger": "standing obligation",
  1173	    "material_terms": "none explicit",
  1174	    "applicability": "in_scope",
  1175	    "applicability_reason": "product=common, lot=common, terminal=common",
  1176	    "materiality": "material"
  1177	  },
  1178	  {
  1179	    "id": "5.1.17.1",
  1180	    "proposition": "оборот менее 40 000 руб. за месяц для регионов; оборот менее 80 000 руб. за месяц для Москвы и СПб",
  1181	    "party": "Банк (right-holder)",
  1182	    "right_or_obligation": "right",
  1183	    "object": "electronic terminals",
  1184	    "trigger": "upon occurrence of specified event",
  1185	    "material_terms": "none explicit",
  1186	    "applicability": "in_scope",
  1187	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=pos",
  1188	    "materiality": "material"
  1189	  },
  1190	  {
  1191	    "id": "5.1.17.2",
  1192	    "proposition": "торговый оборот менее 40 000 руб. для регионов; торговый оборот менее 80 000 руб. для Москвы и СПб; наличие задолженности по сервисному обслуживанию; наличие задолженности по вознаграждениям банка; наличие задолженности по операциям возврата смарт-терминала",
  1193	    "party": "Банк (right-holder)",
  1194	    "right_or_obligation": "right",
  1195	    "object": "electronic terminals",
  1196	    "trigger": "upon occurrence of specified event",
  1197	    "material_terms": "none explicit",
  1198	    "applicability": "in_scope",
  1199	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1200	    "materiality": "material"
Tool:    701	    "party": "neutral/definitional",
   702	    "right_or_obligation": "declaration",
   703	    "object": "general",
   704	    "trigger": "upon event",
   705	    "material_terms": "",
   706	    "applicability": "in_scope",
   707	    "applicability_reason": "contract clause",
   708	    "materiality": "material"
   709	  },
   710	  {
   711	    "id": "5.1.6",
   712	    "proposition": "Осуществлять круглосуточную авторизацию.",
   713	    "party": "neutral/definitional",
   714	    "right_or_obligation": "declaration",
   715	    "object": "authorization",
   716	    "trigger": "upon event",
   717	    "material_terms": "",
   718	    "applicability": "in_scope",
   719	    "applicability_reason": "contract clause",
   720	    "materiality": "material"
   721	  },
   722	  {
   723	    "id": "5.1.7",
   724	    "proposition": "Обеспечивать электронные терминалы рекламно-информационными материалами.",
   725	    "party": "neutral/definitional",
   726	    "right_or_obligation": "declaration",
   727	    "object": "electronic terminals",
   728	    "trigger": "upon event",
   729	    "material_terms": "",
   730	    "applicability": "in_scope",
   731	    "applicability_reason": "contract clause",
   732	    "materiality": "material"
   733	  },
   734	  {
   735	    "id": "5.1.8",
   736	    "proposition": "Перечислять на счет Заказчика суммы Операций оплаты не позднее 2 рабочих дней с даты получения расчетной информации. Дата получения – рабочий день, следующий за днем Электронной сверки итогов. При техническом сбое – перечисление по истечении 3 календарных дней.",
   737	    "party": "neutral/definitional",
   738	    "right_or_obligation": "declaration",
   739	    "object": "settlement/transfer",
   740	    "trigger": "upon event",
   741	    "material_terms": "",
   742	    "applicability": "in_scope",
   743	    "applicability_reason": "contract clause",
   744	    "materiality": "material"
   745	  },
   746	  {
   747	    "id": "5.1.9",
   748	    "proposition": "Осуществлять обработку персональных данных в соответствии с ФЗ-152. Обеспечить конфиденциальность и защиту ПДн.",
   749	    "party": "neutral/definitional",
   750	    "right_or_obligation": "declaration",
   751	    "object": "personal data",
   752	    "trigger": "upon event",
   753	    "material_terms": "",
   754	    "applicability": "in_scope",
   755	    "applicability_reason": "contract clause",
   756	    "materiality": "material"
   757	  },
   758	  {
   759	    "id": "5.1.10",
   760	    "proposition": "Исполнитель перечисляет Заказчику суммы операций оплаты услуг.",
   761	    "party": "neutral/definitional",
   762	    "right_or_obligation": "declaration",
   763	    "object": "payment for services",
   764	    "trigger": "upon event",
   765	    "material_terms": "",
   766	    "applicability": "in_scope",
   767	    "applicability_reason": "contract clause",
   768	    "materiality": "material"
   769	  },
   770	  {
   771	    "id": "5.2",
   772	    "proposition": "Исполнитель вправе:",
   773	    "party": "Исполнитель (right-holder)",
   774	    "right_or_obligation": "right",
   775	    "object": "general",
   776	    "trigger": "upon event",
   777	    "material_terms": "",
   778	    "applicability": "in_scope",
   779	    "applicability_reason": "contract clause",
   780	    "materiality": "material"
   781	  },
   782	  {
   783	    "id": "5.2.1",
   784	    "proposition": "Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате.",
   785	    "party": "neutral/definitional",
   786	    "right_or_obligation": "declaration",
   787	    "object": "acceptance of services",
   788	    "trigger": "upon event",
   789	    "material_terms": "",
   790	    "applicability": "in_scope",
   791	    "applicability_reason": "contract clause",
   792	    "materiality": "material"
   793	  },
   794	  {
   795	    "id": "5.2.2",
   796	    "proposition": "Принять решение об одностороннем отказе от исполнения контракта по основаниям 44-ФЗ и ГК РФ.",
   797	    "party": "neutral/definitional",
   798	    "right_or_obligation": "declaration",
   799	    "object": "termination/refusal",
   800	    "trigger": "upon event",
   801	    "material_terms": "",
   802	    "applicability": "in_scope",
   803	    "applicability_reason": "contract clause",
   804	    "materiality": "material"
   805	  },
   806	  {
   807	    "id": "5.2.3",
   808	    "proposition": "Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов. Производить замену и обновление ПО с уведомлением за 2 рабочих дня.",
   809	    "party": "neutral/definitional",
   810	    "right_or_obligation": "declaration",
   811	    "object": "terminal installation/maintenance",
   812	    "trigger": "upon event",
   813	    "material_terms": "",
   814	    "applicability": "in_scope",
   815	    "applicability_reason": "contract clause",
   816	    "materiality": "material"
   817	  },
   818	  {
   819	    "id": "5.2.4",
   820	    "proposition": "Допускается удаленное обновление ПО, не затрагивающее порядок проведения операций.",
   821	    "party": "neutral/definitional",
   822	    "right_or_obligation": "declaration",
   823	    "object": "general",
   824	    "trigger": "upon event",
   825	    "material_terms": "",
   826	    "applicability": "in_scope",
   827	    "applicability_reason": "contract clause",
   828	    "materiality": "material"
   829	  },
   830	  {
   831	    "id": "5.2.5",
   832	    "proposition": "Запрашивать документы по операциям не позднее 13 месяцев с даты операции. Требовать копии контрольной ленты, заявления, счета, чеки.",
   833	    "party": "neutral/definitional",
   834	    "right_or_obligation": "declaration",
   835	    "object": "application/statement",
   836	    "trigger": "upon event",
   837	    "material_terms": "",
   838	    "applicability": "in_scope",
   839	    "applicability_reason": "contract clause",
   840	    "materiality": "material"
   841	  },
   842	  {
   843	    "id": "5.2.6",
   844	    "proposition": "В случае изменения реквизитов уведомить заказчика в течение 3 рабочих дней.",
   845	    "party": "neutral/definitional",
   846	    "right_or_obligation": "declaration",
   847	    "object": "general",
   848	    "trigger": "upon event",
   849	    "material_terms": "",
   850	    "applicability": "in_scope",
   851	    "applicability_reason": "contract clause",
   852	    "materiality": "material"
   853	  },
   854	  {
   855	    "id": "5.2.7",
   856	    "proposition": "Направлять запросы на адрес электронной почты заказчика/ТСТ.",
   857	    "party": "neutral/definitional",
   858	    "right_or_obligation": "declaration",
   859	    "object": "general",
   860	    "trigger": "upon event",
   861	    "material_terms": "",
   862	    "applicability": "in_scope",
   863	    "applicability_reason": "contract clause",
   864	    "materiality": "material"
   865	  },
   866	  {
   867	    "id": "5.2.8",
   868	    "proposition": "Требовать от заказчика предоставления документов и сведений для осуществления функций.",
   869	    "party": "neutral/definitional",
   870	    "right_or_obligation": "declaration",
   871	    "object": "general",
   872	    "trigger": "upon event",
   873	    "material_terms": "",
   874	    "applicability": "in_scope",
   875	    "applicability_reason": "contract clause",
   876	    "materiality": "material"
   877	  },
   878	  {
   879	    "id": "5.2.9",
   880	    "proposition": "В одностороннем порядке приостановить Авторизации и/или расторгнуть Контракт при наступлении событий.",
   881	    "party": "neutral/definitional",
   882	    "right_or_obligation": "declaration",
   883	    "object": "general",
   884	    "trigger": "upon event",
   885	    "material_terms": "",
   886	    "applicability": "in_scope",
   887	    "applicability_reason": "contract clause",
   888	    "materiality": "material"
   889	  },
   890	  {
   891	    "id": "5.2.9.1",
   892	    "proposition": "нарушение Заказчиком условий Контракта.",
   893	    "party": "neutral/definitional",
   894	    "right_or_obligation": "declaration",
   895	    "object": "general",
   896	    "trigger": "upon event",
   897	    "material_terms": "",
   898	    "applicability": "in_scope",
   899	    "applicability_reason": "contract clause",
   900	    "materiality": "material"
   901	  },
   902	  {
   903	    "id": "5.2.9.2",
   904	    "proposition": "внесение данных Заказчика в перечень причастных к экстремизму/терроризму.",
   905	    "party": "neutral/definitional",
   906	    "right_or_obligation": "declaration",
   907	    "object": "general",
   908	    "trigger": "upon event",
   909	    "material_terms": "",
   910	    "applicability": "in_scope",
   911	    "applicability_reason": "contract clause",
   912	    "materiality": "material"
   913	  },
   914	  {
   915	    "id": "5.2.9.3",
   916	    "proposition": "подозрения в легализации доходов или финансировании терроризма.",
   917	    "party": "neutral/definitional",
   918	    "right_or_obligation": "declaration",
   919	    "object": "general",
   920	    "trigger": "upon event",
   921	    "material_terms": "",
   922	    "applicability": "in_scope",
   923	    "applicability_reason": "contract clause",
   924	    "materiality": "material"
   925	  },
   926	  {
   927	    "id": "5.2.9.4",
   928	    "proposition": "негативная информация от органов власти и/или Платежных систем.",
   929	    "party": "neutral/definitional",
   930	    "right_or_obligation": "declaration",
   931	    "object": "general",
   932	    "trigger": "upon event",
   933	    "material_terms": "",
   934	    "applicability": "in_scope",
   935	    "applicability_reason": "contract clause",
   936	    "materiality": "material"
   937	  },
   938	  {
   939	    "id": "5.2.9.5",
   940	    "proposition": "информация о мошенничестве в ТСТ. Подтверждение – информация от Банков-эмитентов или Платежных систем.",
   941	    "party": "neutral/definitional",
   942	    "right_or_obligation": "declaration",
   943	    "object": "general",
   944	    "trigger": "upon event",
   945	    "material_terms": "",
   946	    "applicability": "in_scope",
   947	    "applicability_reason": "contract clause",
   948	    "materiality": "material"
   949	  },
   950	  {
   951	    "id": "5.2.9.6",
   952	    "proposition": "ремонт помещений ТСТ, препятствующий Операциям.",
   953	    "party": "neutral/definitional",
   954	    "right_or_obligation": "declaration",
   955	    "object": "general",
   956	    "trigger": "upon event",
   957	    "material_terms": "",
   958	    "applicability": "in_scope",
   959	    "applicability_reason": "contract clause",
   960	    "materiality": "material"
   961	  },
   962	  {
   963	    "id": "5.2.9.7",
   964	    "proposition": "ликвидация Заказчика или дело о банкротстве.",
   965	    "party": "neutral/definitional",
   966	    "right_or_obligation": "declaration",
   967	    "object": "general",
   968	    "trigger": "upon event",
   969	    "material_terms": "",
   970	    "applicability": "in_scope",
   971	    "applicability_reason": "contract clause",
   972	    "materiality": "material"
   973	  },
   974	  {
   975	    "id": "5.2.9.8",
   976	    "proposition": "недостоверные сведения о Заказчике/ТСТ/руководителе.",
   977	    "party": "neutral/definitional",
   978	    "right_or_obligation": "declaration",
   979	    "object": "general",
   980	    "trigger": "upon event",
   981	    "material_terms": "",
   982	    "applicability": "in_scope",
   983	    "applicability_reason": "contract clause",
   984	    "materiality": "material"
   985	  },
   986	  {
   987	    "id": "5.2.9.9",
   988	    "proposition": "несоответствие товаров/услуг роду деятельности Заказчика.",
   989	    "party": "neutral/definitional",
   990	    "right_or_obligation": "declaration",
   991	    "object": "general",
   992	    "trigger": "upon event",
   993	    "material_terms": "",
   994	    "applicability": "in_scope",
   995	    "applicability_reason": "contract clause",
   996	    "materiality": "material"
   997	  },
   998	  {
   999	    "id": "5.2.9.10",
  1000	    "proposition": "отсутствие операций в течение 30 календарных дней подряд.",
  1001	    "party": "neutral/definitional",
  1002	    "right_or_obligation": "declaration",
  1003	    "object": "general",
  1004	    "trigger": "upon event",
  1005	    "material_terms": "",
  1006	    "applicability": "in_scope",
  1007	    "applicability_reason": "contract clause",
  1008	    "materiality": "material"
  1009	  },
  1010	  {
  1011	    "id": "5.2.9.11",
  1012	    "proposition": "исчерпание Цены Контракта и/или окончание срока действия.",
  1013	    "party": "neutral/definitional",
  1014	    "right_or_obligation": "declaration",
  1015	    "object": "general",
  1016	    "trigger": "upon event",
  1017	    "material_terms": "",
  1018	    "applicability": "in_scope",
  1019	    "applicability_reason": "contract clause",
  1020	    "materiality": "material"
  1021	  },
  1022	  {
  1023	    "id": "5.2.10",
  1024	    "proposition": "Удерживать из сумм, подлежащих перечислению Заказчику:",
  1025	    "party": "neutral/definitional",
  1026	    "right_or_obligation": "declaration",
  1027	    "object": "settlement/transfer",
  1028	    "trigger": "upon event",
  1029	    "material_terms": "",
  1030	    "applicability": "in_scope",
  1031	    "applicability_reason": "contract clause",
  1032	    "materiality": "material"
  1033	  },
  1034	  {
  1035	    "id": "5.2.10.1",
  1036	    "proposition": "Суммы недействительных Операций (12 оснований: нарушение контракта, поддельная карта, неполный документ, несоответствие экземпляров, отсутствие подписи, непредоставление документов, возврат товара без возврата средств, двойная оплата, отсутствие кода авторизации, разбивка суммы, мошенничество, ручно",
  1037	    "party": "neutral/definitional",
  1038	    "right_or_obligation": "declaration",
  1039	    "object": "authorization",
  1040	    "trigger": "upon event",
  1041	    "material_terms": "",
  1042	    "applicability": "in_scope",
  1043	    "applicability_reason": "contract clause",
  1044	    "materiality": "material"
  1045	  },
  1046	  {
  1047	    "id": "5.2.10.2",
  1048	    "proposition": "Суммы, ошибочно перечисленные на счет Заказчика.",
  1049	    "party": "neutral/definitional",
  1050	    "right_or_obligation": "declaration",
  1051	    "object": "settlement/transfer",
  1052	    "trigger": "upon event",
  1053	    "material_terms": "",
  1054	    "applicability": "in_scope",
  1055	    "applicability_reason": "contract clause",
  1056	    "materiality": "material"
  1057	  },
  1058	  {
  1059	    "id": "5.2.10.3",
  1060	    "proposition": "Суммы Операций возврата, Возврата платежа и Реверсивные транзакции.",
  1061	    "party": "neutral/definitional",
  1062	    "right_or_obligation": "declaration",
  1063	    "object": "general",
  1064	    "trigger": "upon event",
  1065	    "material_terms": "",
  1066	    "applicability": "in_scope",
  1067	    "applicability_reason": "contract clause",
  1068	    "materiality": "material"
  1069	  },
  1070	  {
  1071	    "id": "5.2.10.4",
  1072	    "proposition": "Суммы оспоренных операций, списанных Банком-эмитентом, а также оспоренных операций при реализации Заказчиком как агентом.",
  1073	    "party": "neutral/definitional",
  1074	    "right_or_obligation": "declaration",
  1075	    "object": "disputes",
  1076	    "trigger": "upon event",
  1077	    "material_terms": "",
  1078	    "applicability": "in_scope",
  1079	    "applicability_reason": "contract clause",
  1080	    "materiality": "material"
  1081	  },
  1082	  {
  1083	    "id": "5.2.10.5",
  1084	    "proposition": "Суммы штрафов и убытков Исполнителя от штрафных санкций Платежных систем и ответственности из-за нарушения Заказчиком.",
  1085	    "party": "neutral/definitional",
  1086	    "right_or_obligation": "declaration",
  1087	    "object": "liability/penalties",
  1088	    "trigger": "upon event",
  1089	    "material_terms": "",
  1090	    "applicability": "in_scope",
  1091	    "applicability_reason": "contract clause",
  1092	    "materiality": "material"
  1093	  },
  1094	  {
  1095	    "id": "5.3",
  1096	    "proposition": "Заказчик обязуется:",
  1097	    "party": "Заказчик (obligation-bearer)",
  1098	    "right_or_obligation": "obligation",
  1099	    "object": "general",
  1100	    "trigger": "standing",
  1101	    "material_terms": "",
  1102	    "applicability": "in_scope",
  1103	    "applicability_reason": "contract clause",
  1104	    "materiality": "material"
  1105	  },
  1106	  {
  1107	    "id": "5.3.1",
  1108	    "proposition": "Принять оказанные услуги по документу о приемке.",
  1109	    "party": "neutral/definitional",
  1110	    "right_or_obligation": "declaration",
  1111	    "object": "acceptance of services",
  1112	    "trigger": "upon event",
  1113	    "material_terms": "",
  1114	    "applicability": "in_scope",
  1115	    "applicability_reason": "contract clause",
  1116	    "materiality": "material"
  1117	  },
  1118	  {
  1119	    "id": "5.3.2",
  1120	    "proposition": "Оплатить стоимость услуг согласно условиям контракта.",
  1121	    "party": "neutral/definitional",
  1122	    "right_or_obligation": "declaration",
  1123	    "object": "general",
  1124	    "trigger": "upon event",
  1125	    "material_terms": "",
  1126	    "applicability": "in_scope",
  1127	    "applicability_reason": "contract clause",
  1128	    "materiality": "material"
  1129	  },
  1130	  {
  1131	    "id": "5.3.3",
  1132	    "proposition": "Осуществлять контроль за ходом оказания услуг.",
  1133	    "party": "neutral/definitional",
  1134	    "right_or_obligation": "declaration",
  1135	    "object": "general",
  1136	    "trigger": "upon event",
  1137	    "material_terms": "",
  1138	    "applicability": "in_scope",
  1139	    "applicability_reason": "contract clause",
  1140	    "materiality": "material"
  1141	  },
  1142	  {
  1143	    "id": "5.3.4",
  1144	    "proposition": "Принять решение об одностороннем отказе от контракта при несоответствии Исполнителя требованиям.",
  1145	    "party": "neutral/definitional",
  1146	    "right_or_obligation": "declaration",
  1147	    "object": "termination/refusal",
  1148	    "trigger": "upon event",
  1149	    "material_terms": "",
  1150	    "applicability": "in_scope",
  1151	    "applicability_reason": "contract clause",
  1152	    "materiality": "material"
  1153	  },
  1154	  {
  1155	    "id": "5.3.5",
  1156	    "proposition": "Требовать уплаты неустоек при просрочке или неисполнении Исполнителем.",
  1157	    "party": "neutral/definitional",
  1158	    "right_or_obligation": "declaration",
  1159	    "object": "general",
  1160	    "trigger": "upon event",
  1161	    "material_terms": "",
  1162	    "applicability": "in_scope",
  1163	    "applicability_reason": "contract clause",
  1164	    "materiality": "material"
  1165	  },
  1166	  {
  1167	    "id": "5.3.6",
  1168	    "proposition": "Уменьшить сумму оплаты на размер налогов и обязательных платежей.",
  1169	    "party": "neutral/definitional",
  1170	    "right_or_obligation": "declaration",
  1171	    "object": "general",
  1172	    "trigger": "upon event",
  1173	    "material_terms": "",
  1174	    "applicability": "in_scope",
  1175	    "applicability_reason": "contract clause",
  1176	    "materiality": "material"
  1177	  },
  1178	  {
  1179	    "id": "5.3.7",
  1180	    "proposition": "Размещать на видных местах ТСТ рекламно-информационные материалы.",
  1181	    "party": "neutral/definitional",
  1182	    "right_or_obligation": "declaration",
  1183	    "object": "informational materials",
  1184	    "trigger": "upon event",
  1185	    "material_terms": "",
  1186	    "applicability": "in_scope",
  1187	    "applicability_reason": "contract clause",
  1188	    "materiality": "material"
  1189	  },
  1190	  {
  1191	    "id": "5.3.8",
  1192	    "proposition": "Не разбивать сумму одной операции оплаты на несколько сумм.",
  1193	    "party": "neutral/definitional",
  1194	    "right_or_obligation": "declaration",
  1195	    "object": "general",
  1196	    "trigger": "upon event",
  1197	    "material_terms": "",
  1198	    "applicability": "in_scope",
  1199	    "applicability_reason": "contract clause",
  1200	    "materiality": "material"
Tool:      1	# Output Contract
     2	
     3	Write `/outputs/discrepancy_analysis.json` as one JSON object with this shape.
     4	Do not write this file anywhere else.
     5	
     6	Before writing the final file, create and use:
     7	
     8	- `/outputs/working/matrix_inventory.json`
     9	- `/outputs/working/contract_inventory.json`
    10	
    11	These working files prove that the comparison covered both documents. They are
    12	not part of the final JSON object.
    13	
    14	```json
    15	{
    16	  "links": [
    17	    {
    18	      "matrix_ids": ["<matrix id>"],
    19	      "contract_ids": ["<contract locator>"],
    20	      "relationship": "aligned|deviation",
    21	      "legal_topic": "<short legal topic>",
    22	      "matrix_standard": "<bank standard requirement>",
    23	      "contract_position": "<counterparty contract position>",
    24	      "discrepancies": [
    25	        {
    26	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
    27	          "description": "<material difference>",
    28	          "risk": "<why this matters for the Bank>"
    29	        }
    30	      ]
    31	    }
    32	  ],
    33	  "atomic_links": [
    34	    {
    35	      "matrix_id": "<one matrix id>",
    36	      "contract_id": "<one contract locator>",
    37	      "relationship": "aligned|deviation",
    38	      "link_index": 0,
    39	      "legal_topic": "<short legal topic>",
    40	      "analogue_strength": "strong|partial",
    41	      "coverage_role": "direct|parent|child|framework|procedure|liability|payment|appendix|context",
    42	      "coverage": "<what this exact contract clause contributes to this exact matrix item>",
    43	      "element_checklist": [
    44	        {
    45	          "element": "party|legal_object|operative_right_or_duty|trigger|deadline|amount_formula_cap|procedure_channel|liability_remedy|scope_exceptions|consequence",
    46	          "result": "same|equivalent|different|missing|not_applicable",
    47	          "note": "<short evidence-based note>"
    48	        }
    49	      ],
    50	      "status_reason": "<why this exact pair is aligned or deviation>",
    51	      "discrepancies": [
    52	        {
    53	          "type": "deadline|amount|party|scope|trigger|procedure|liability|right|obligation|missing_element|other",
    54	          "description": "<pair-level material difference>",
    55	          "risk": "<why this pair-level difference matters for the Bank>"
    56	        }
    57	      ]
    58	    }
    59	  ],
    60	  "unmatched_matrix": [
    61	    {
    62	      "matrix_id": "<matrix id>",
    63	      "requirement": "<missing bank standard requirement>",
    64	      "status": "missing_in_contract",
    65	      "risk": "<legal or business risk for the Bank>",
    66	      "rejected_candidates": [
    67	        {
    68	          "contract_id": "<contract locator considered but rejected>",
    69	          "reason": "<why this is only weak context and not a legal analogue>"
    70	        }
    71	      ]
    72	    }
    73	  ],
    74	  "unmatched_contract": [
    75	    {
    76	      "contract_id": "<contract locator>",
    77	      "contract_position": "<extra contract term>",
    78	      "status": "extra_in_contract|not_material",
    79	      "risk": "<risk if material; empty or low-risk explanation if not material>",
    80	      "materiality_reason": "<why this creates independent legal effect or why it is non-operative>"
    81	    }
    82	  ],
    83	  "summary": {
    84	    "aligned_count": 0,
    85	    "deviation_count": 0,
    86	    "missing_in_contract_count": 0,
    87	    "extra_in_contract_count": 0
    88	  }
    89	}
    90	```
    91	
    92	## Field Rules
    93	
    94	- `matrix_ids`: exact `number` values from `inputs/matrix.json`.
    95	- `contract_ids`: exact printed clause ids or real document locators from
    96	  `inputs/contract.txt` and `/outputs/working/contract_inventory.json`; never
    97	  use invented subparagraph labels.
    98	- `contract_ids`: the inventory is not authority by itself. A final contract
    99	  locator must also be visible in `inputs/contract.txt` as printed numbering,
   100	  printed appendix/table/form label, heading, definition label, or exact
   101	  unnumbered text.
   102	- `contract_ids`: if an appendix, form, table, or unnumbered paragraph cannot
   103	  pass that source-text test, cite the nearest real printed clause that
   104	  incorporates or describes it and put the appendix detail in `coverage`.
   105	- `contract_ids`: do not use internal aliases or translated labels such as
   106	  `Appendix_1`. If an alias is useful in a working file, keep it out of the
   107	  final artifact.
   108	- `contract_ids`: must be non-empty for every `links` item. If no contract
   109	  locator exists, use `unmatched_matrix` instead of a link.
   110	- `relationship`: only `aligned` or `deviation`.
   111	- `discrepancies`: empty array for `aligned`; non-empty array for `deviation`.
   112	- `unmatched_matrix[].status`: must be exactly `missing_in_contract`. Do not
   113	  use `reason`, `classification`, or `relationship` as a substitute for
   114	  `status`.
   115	- `atomic_links`: one object per legally related `matrix_id` + `contract_id`
   116	  pair. Do not omit atomic pairs just because a grouped `links` item already
   117	  contains them.
   118	- `atomic_links[].analogue_strength`: use only `strong` or `partial`. Do not put
   119	  weak-context candidates in `atomic_links`.
   120	- `atomic_links[].coverage_role`: describe the exact role of the contract
   121	  locator in the legal package.
   122	- `atomic_links[].relationship`: evaluate the exact pair and its role. Do not
   123	  borrow coverage from unrelated clauses. Do not automatically mark a necessary
   124	  parent, child, appendix, or procedure clause as `deviation` unless the pair
   125	  has a named material gap in `element_checklist`.
   126	- `atomic_links[].link_index`: zero-based index of the grouped `links` item that
   127	  contains the pair. Use `null` only if the pair cannot be placed into a grouped
   128	  link.
   129	- `atomic_links[].coverage`: short statement of the legal element this exact
   130	  contract locator covers for this exact matrix item.
   131	- `atomic_links[].element_checklist`: must include all material elements needed
   132	  to justify the pair result. Use `different` or `missing` only for real legal
   133	  gaps.
   134	- If an atomic pair has `relationship = deviation`, at least one checklist item
   135	  must be `different` or `missing`. If the discrepancy is an omitted sub-duty,
   136	  omitted remedy, omitted trigger, omitted amount, or narrower scope, record
   137	  that omission in the closest checklist element.
   138	- For each `different` or `missing` checklist item, write the note as compact
   139	  side-by-side evidence: `matrix: ...; contract: ...; gap: ...`.
   140	- If any checklist item is `different` or `missing`, the atomic pair cannot be
   141	  `aligned`; change the pair to `deviation` and put the same gap in
   142	  `discrepancies`.
   143	- `atomic_links[].status_reason`: one sentence connecting the checklist to
   144	  `aligned` or `deviation`.
   145	- `type`: choose the closest fixed value. Use `other` only when none fit.
   146	- `summary.aligned_count`: number of `links` with `relationship = aligned`.
   147	- `summary.deviation_count`: number of `links` with `relationship = deviation`.
   148	- `summary.missing_in_contract_count`: number of `unmatched_matrix` items.
   149	- `summary.extra_in_contract_count`: number of `unmatched_contract` items with
   150	  `status = extra_in_contract`.
   151	
   152	## Coverage Rules
   153	
   154	Each matrix id must appear once:
   155	
   156	- in one `links[].matrix_ids` array when the contract has a legal analogue; or
   157	- in one `unmatched_matrix[].matrix_id` when the contract has no useful analogue.
   158	
   159	Each linked matrix-contract pair must also appear in `atomic_links`:
   160	
   161	- for every legally meaningful pair from each grouped link, add exactly one
   162	  `atomic_links` row;
   163	- do not generate a Cartesian product automatically. Add a pair only when that
   164	  contract locator actually contributes legal coverage to that matrix item;
   165	- do not let one strong direct clause lift unrelated framework, context,
   166	  appendix, or procedure clauses to `aligned`;
   167	- do not downgrade a necessary package clause to `deviation` merely because it
   168	  covers only its own role; `deviation` needs a named material difference;
   169	- if the full legal result is achieved only by a package of several contract
   170	  clauses, the grouped link may be `aligned`, while atomic pairs show each
   171	  clause's role and checklist-supported relationship.
   172	
   173	Do not create links for weak context:
   174	
   175	- same broad topic without the same protected party, legal object, operative
   176	  act, trigger, and consequence belongs in
   177	  `unmatched_matrix[].rejected_candidates`;
   178	- a weak candidate may explain why a matrix item is still missing, but it must
   179	  not appear in `links` or `atomic_links`.
   180	- generic QR display, terminal capability, card acceptance, contactless payment,
   181	  inspection, request, or payment wording is weak context unless it preserves
   182	  the same named Bank product, channel, risk-control mechanism, trigger, and
   183	  legal consequence.
   184	
   185	Each material contract inventory item must be accounted for:
   186	
   187	- in `links[].contract_ids` when it is legally related to the matrix;
   188	- in `unmatched_contract` with `status = extra_in_contract` when it has
   189	  independent legal effect and no matrix analogue;
   190	- in `unmatched_contract` with `status = not_material` only when it is useful to
   191	  show that a reviewed provision creates no standalone risk.
   192	
   193	Do not let contract-only review become a list of headings. Report material
   194	contract-only provisions that affect procurement procedure, acceptance,
   195	customer control rights, payment mechanics, termination, evidence, reporting,
   196	liability, or enforceability.
   197	
   198	`not_material` is reserved for headings, recitals, signatures, requisites,
   199	blank forms, administrative details, and definitions with no operative effect.
   200	Every `unmatched_contract` row must explain materiality in
Tool:      1	# Comparison Patterns
     2	
     3	These examples calibrate legal judgment. Do not copy ids, facts, or wording into
     4	the final artifact unless they are present in the actual inputs.
     5	
     6	## 1. One Matrix Item Covered By Several Contract Clauses
     7	
     8	Matrix standard:
     9	- settlement occurs after reconciliation;
    10	- refunds and chargebacks may be deducted;
    11	- settlement currency is fixed.
    12	
    13	Contract position:
    14	- reconciliation is in an operations clause;
    15	- deductions are in a Bank-rights clause;
    16	- currency is in a payment clause.
    17	
    18	Result:
    19	- one grouped `links` item may include all relevant contract locators;
    20	- `aligned` if the package preserves every material element;
    21	- each `atomic_links` row states the exact role of the locator and uses an
    22	  element checklist.
    23	
    24	## 2. One Contract Clause Covers Several Matrix Requirements
    25	
    26	Matrix standard:
    27	- the merchant must follow payment-system rules;
    28	- the merchant must prevent fraud;
    29	- the merchant must provide documents on request.
    30	
    31	Contract position:
    32	- one compliance clause imposes all three duties with the same protected party,
    33	  object, triggers, and consequences.
    34	
    35	Result:
    36	- one contract locator may link to several matrix ids;
    37	- the link is valid only because the operative duties are actually preserved,
    38	  not because the clause is broadly worded.
    39	
    40	## 3. Weak Topic Match Is Missing, Not Deviation
    41	
    42	Matrix standard:
    43	- the Bank has a specific right to deduct a named fee from settlement amounts
    44	  after a defined trigger.
    45	
    46	Contract position:
    47	- the contract contains a general payment clause but does not give the same
    48	  deduction right, trigger, or settlement mechanism.
    49	
    50	Result:
    51	- do not create `deviation`;
    52	- put the matrix item in `unmatched_matrix`;
    53	- record the payment clause in `rejected_candidates` as weak context.
    54	
    55	## 4. Generic Notice Does Not Cover Named Bank Channel
    56	
    57	Matrix standard:
    58	- legally significant notices must be delivered through a named Bank channel
    59	  and have evidentiary force.
    60	
    61	Contract position:
    62	- a generic written-notice clause allows email or paper notices but does not
    63	  address the named channel or evidentiary force.
    64	
    65	Result:
    66	- `deviation` only if it governs the same legal notice process but changes the
    67	  channel, deadline, or evidence effect;
    68	- `missing_in_contract` if it is only a broad notice clause.
    69	
    70	## 5. Generic Liability Does Not Cover Specific Remedy
    71	
    72	Matrix standard:
    73	- a fixed penalty applies for a specific breach, protected party, trigger,
    74	  calculation method, and cap or no-cap position.
    75	
    76	Contract position:
    77	- the contract has only general damages or statutory liability.
    78	
    79	Result:
    80	- use `missing_in_contract` when the special remedy is absent;
    81	- use `deviation` only when a true analogue exists but amount, trigger, cap,
    82	  exception, or protected party differs.
    83	
    84	## 6. Changed Deadline, Amount, Formula, Or Party Is Deviation
    85	
    86	Matrix standard:
    87	- notice is due within one business day;
    88	- penalty is a fixed amount;
    89	- the Bank is the protected party.
    90	
    91	Contract position:
    92	- notice is due within five business days;
    93	- penalty is lower, capped, conditional, or absent;
    94	- another party receives the protection.
    95	
    96	Result:
    97	- `relationship = deviation`;
    98	- checklist marks `deadline`, `amount_formula_cap`, `party`, or
    99	  `liability_remedy` as `different`;
   100	- discrepancy explains the lost Bank protection.
   101	
   102	## 7. Formal Label Difference Is Not Deviation
   103	
   104	Matrix standard:
   105	- an appendix, act, form, or channel has a specific label.
   106	
   107	Contract position:
   108	- the same legal content appears under a different title.
   109	
   110	Result:
   111	- `aligned` if rights, duties, evidentiary effect, deadlines, and consequences
   112	  are preserved;
   113	- naming alone is not a legal gap.
   114	
   115	## 8. Mandatory Law Can Preserve The Result
   116	
   117	Matrix standard:
   118	- the Bank requires a protection that mandatory law already provides.
   119	
   120	Contract position:
   121	- the contract uses the statutory structure and does not waive, narrow, or shift
   122	  the Bank's protection.
   123	
   124	Result:
   125	- `aligned` if the legal result is at least as strong for the Bank;
   126	- `deviation` if the contract narrows the statutory protection or adds a
   127	  material burden.
   128	
   129	## 9. Mandatory-Law Procedure As Extra Contract Term
   130	
   131	Contract position:
   132	- the contract adds procurement, public-system acceptance, customer-control, or
   133	  mandatory-law procedures that create independent rights or duties for the
   134	  customer.
   135	
   136	Matrix standard:
   137	- the matrix does not contain an analogue for that customer-side procedure.
   138	
   139	Result:
   140	- `unmatched_contract`;
   141	- status `extra_in_contract`;
   142	- risk explains delay, customer leverage, payment control, termination risk, or
   143	  procedural burden for the Bank.
   144	
   145	## 10. Material Contract-Only Clause
   146	
   147	Contract position:
   148	- the customer may inspect performance, reject results, withhold payment, demand
   149	  corrections, suspend performance, or terminate for convenience.
   150	
   151	Matrix standard:
   152	- no matrix requirement creates the same customer-side right.
   153	
   154	Result:
   155	- `unmatched_contract`;
   156	- status `extra_in_contract`;
   157	- `materiality_reason` explains the independent legal effect.
   158	
   159	## 11. Technical Contract-Only Clause Is Not Material
   160	
   161	Contract position:
   162	- heading, signature block, blank requisites table, descriptive recital, or
   163	  definition without operative effect.
   164	
   165	Result:
   166	- omit it if unnecessary, or include as `not_material`;
   167	- `materiality_reason` states that it creates no standalone right, duty,
   168	  procedure, economic term, liability, or consequence.
   169	
   170	## 12. Parent And Child Locator Recall
   171	
   172	Matrix standard:
   173	- the Bank may demand penalties for late performance;
   174	- amount and calculation trigger are material.
   175	
   176	Contract position:
   177	- a parent clause grants the penalty right;
   178	- child clauses set amount, trigger, exceptions, and cap.
   179	
   180	Result:
   181	- include both parent and child locators when both have legal effect;
   182	- do not cite only the child if the parent contains the operative right;
   183	- do not cite only the parent if the child contains the amount, trigger, or cap.
   184	
   185	## 13. Grouped Package And Atomic Rows
   186	
   187	Matrix standard:
   188	- one requirement needs a parent right, an operative duty, and a formula.
   189	
   190	Contract position:
   191	- several clauses jointly preserve the complete result.
   192	
   193	Grouped result:
   194	- one `links` item may be `aligned`.
   195	
   196	Atomic result:
   197	- create one row for each real matrix-contract pair;
   198	- each row has `coverage_role`, `analogue_strength`, `element_checklist`, and
   199	  `status_reason`;
   200	- do not mark a necessary package clause as `deviation` merely because it covers
AI: Now I have a thorough understanding of the task. Let me set up my work plan and then proceed with the contract-only review. The task is specifically: identify material contract-only terms — i.e., `extra_in_contract` and `not_material` items for `unmatched_contract`.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read remaining contract_inventory.json entries to completion', 'status': 'in_progress'}, {'content': 'Read remaining matrix_inventory.json entries to completion', 'status': 'pending'}, {'content': 'Read remaining contract.txt to completion', 'status': 'pending'}, {'content': 'Identify all material contract inventory items not linked to any matrix item', 'status': 'pending'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]}, 'id': 'call_00_zbRW68e8nnUUZ9AMW7DS1846', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read remaining contract_inventory.json entries to completion', 'status': 'in_progress'}, {'content': 'Read remaining matrix_inventory.json entries to completion', 'status': 'pending'}, {'content': 'Read remaining contract.txt to completion', 'status': 'pending'}, {'content': 'Identify all material contract inventory items not linked to any matrix item', 'status': 'pending'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 1200, 'limit': 500}, 'id': 'call_00_JhNuuNwrR7mtOtlDXZ368500', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'offset': 1200, 'limit': 500}, 'id': 'call_01_49DLG0bQzrqdw5j3cuaz0429', 'type': 'tool_call'}]
Tool:   1201	  },
  1202	  {
  1203	    "id": "5.3.9",
  1204	    "proposition": "Не использовать реквизиты карты для иных целей, кроме операций в присутствии покупателя.",
  1205	    "party": "neutral/definitional",
  1206	    "right_or_obligation": "declaration",
  1207	    "object": "general",
  1208	    "trigger": "upon event",
  1209	    "material_terms": "",
  1210	    "applicability": "in_scope",
  1211	    "applicability_reason": "contract clause",
  1212	    "materiality": "material"
  1213	  },
  1214	  {
  1215	    "id": "5.3.10",
  1216	    "proposition": "Проводить операции и оформлять документы по операциям, нести ответственность за правильность информации.",
  1217	    "party": "neutral/definitional",
  1218	    "right_or_obligation": "declaration",
  1219	    "object": "liability/penalties",
  1220	    "trigger": "upon event",
  1221	    "material_terms": "",
  1222	    "applicability": "in_scope",
  1223	    "applicability_reason": "contract clause",
  1224	    "materiality": "material"
  1225	  },
  1226	  {
  1227	    "id": "5.3.11",
  1228	    "proposition": "Хранить документы по операциям не менее 13 месяцев, передавать копии надлежащего качества в течение 3 рабочих дней.",
  1229	    "party": "neutral/definitional",
  1230	    "right_or_obligation": "declaration",
  1231	    "object": "general",
  1232	    "trigger": "upon event",
  1233	    "material_terms": "",
  1234	    "applicability": "in_scope",
  1235	    "applicability_reason": "contract clause",
  1236	    "materiality": "material"
  1237	  },
  1238	  {
  1239	    "id": "5.3.12",
  1240	    "proposition": "Передавать письменное заявление об обстоятельствах операции в течение 3 рабочих дней. Немедленно сообщать об утрате документов.",
  1241	    "party": "neutral/definitional",
  1242	    "right_or_obligation": "declaration",
  1243	    "object": "application/statement",
  1244	    "trigger": "upon event",
  1245	    "material_terms": "",
  1246	    "applicability": "in_scope",
  1247	    "applicability_reason": "contract clause",
  1248	    "materiality": "material"
  1249	  },
  1250	  {
  1251	    "id": "5.3.13",
  1252	    "proposition": "Информировать о реорганизации, изменениях, банкротстве, смене руководства, адреса, реквизитов не позднее 3 рабочих дней.",
  1253	    "party": "neutral/definitional",
  1254	    "right_or_obligation": "declaration",
  1255	    "object": "general",
  1256	    "trigger": "upon event",
  1257	    "material_terms": "",
  1258	    "applicability": "in_scope",
  1259	    "applicability_reason": "contract clause",
  1260	    "materiality": "material"
  1261	  },
  1262	  {
  1263	    "id": "5.3.14",
  1264	    "proposition": "Предоставлять достоверные документы и сведения не реже раза в год и по запросу в течение 7 рабочих дней.",
  1265	    "party": "neutral/definitional",
  1266	    "right_or_obligation": "declaration",
  1267	    "object": "general",
  1268	    "trigger": "upon event",
  1269	    "material_terms": "",
  1270	    "applicability": "in_scope",
  1271	    "applicability_reason": "contract clause",
  1272	    "materiality": "material"
  1273	  },
  1274	  {
  1275	    "id": "5.3.15",
  1276	    "proposition": "По письменному запросу предоставить подтверждение правомерности передачи ПДн. Урегулировать претензии за свой счет. Уведомить об отзыве согласия руководителя.",
  1277	    "party": "neutral/definitional",
  1278	    "right_or_obligation": "declaration",
  1279	    "object": "personal data",
  1280	    "trigger": "upon event",
  1281	    "material_terms": "",
  1282	    "applicability": "in_scope",
  1283	    "applicability_reason": "contract clause",
  1284	    "materiality": "material"
  1285	  },
  1286	  {
  1287	    "id": "5.3.16",
  1288	    "proposition": "С даты расторжения контракта прекратить прием карт, снять рекламно-информационные материалы.",
  1289	    "party": "neutral/definitional",
  1290	    "right_or_obligation": "declaration",
  1291	    "object": "termination/refusal",
  1292	    "trigger": "upon event",
  1293	    "material_terms": "",
  1294	    "applicability": "in_scope",
  1295	    "applicability_reason": "contract clause",
  1296	    "materiality": "material"
  1297	  },
  1298	  {
  1299	    "id": "5.3.17",
  1300	    "proposition": "Не противодействовать проверке, оказывать содействие в разбирательстве подозрительных операций.",
  1301	    "party": "neutral/definitional",
  1302	    "right_or_obligation": "declaration",
  1303	    "object": "inspections",
  1304	    "trigger": "upon event",
  1305	    "material_terms": "",
  1306	    "applicability": "in_scope",
  1307	    "applicability_reason": "contract clause",
  1308	    "materiality": "material"
  1309	  },
  1310	  {
  1311	    "id": "5.3.18",
  1312	    "proposition": "При осуществлении операций в ТСТ (торговый эквайринг):",
  1313	    "party": "neutral/definitional",
  1314	    "right_or_obligation": "declaration",
  1315	    "object": "general",
  1316	    "trigger": "upon event",
  1317	    "material_terms": "",
  1318	    "applicability": "in_scope",
  1319	    "applicability_reason": "contract clause",
  1320	    "materiality": "material"
  1321	  },
  1322	  {
  1323	    "id": "5.3.18.1",
  1324	    "proposition": "Использовать терминалы и ПО только для целей контракта. Не вносить изменения, не ремонтировать самостоятельно. Не передавать третьим лицам (кроме обслуживающей компании).",
  1325	    "party": "neutral/definitional",
  1326	    "right_or_obligation": "declaration",
  1327	    "object": "electronic terminals",
  1328	    "trigger": "upon event",
  1329	    "material_terms": "",
  1330	    "applicability": "in_scope",
  1331	    "applicability_reason": "contract clause",
  1332	    "materiality": "material"
  1333	  },
  1334	  {
  1335	    "id": "5.3.18.2",
  1336	    "proposition": "Предоставлять доступ к местам установки терминалов для подключения, настройки, ремонта, замены, обслуживания и проверки.",
  1337	    "party": "neutral/definitional",
  1338	    "right_or_obligation": "declaration",
  1339	    "object": "terminal installation/maintenance",
  1340	    "trigger": "upon event",
  1341	    "material_terms": "",
  1342	    "applicability": "in_scope",
  1343	    "applicability_reason": "contract clause",
  1344	    "materiality": "material"
  1345	  },
  1346	  {
  1347	    "id": "5.3.18.3",
  1348	    "proposition": "Принять терминалы по акту в двух экземплярах, подписанных сторонами.",
  1349	    "party": "neutral/definitional",
  1350	    "right_or_obligation": "declaration",
  1351	    "object": "electronic terminals",
  1352	    "trigger": "upon event",
  1353	    "material_terms": "",
  1354	    "applicability": "in_scope",
  1355	    "applicability_reason": "contract clause",
  1356	    "materiality": "material"
  1357	  },
  1358	  {
  1359	    "id": "5.3.20.4",
  1360	    "proposition": "При выходе терминала из строя или утрате немедленно информировать исполнителя.",
  1361	    "party": "neutral/definitional",
  1362	    "right_or_obligation": "declaration",
  1363	    "object": "electronic terminals",
  1364	    "trigger": "upon event",
  1365	    "material_terms": "",
  1366	    "applicability": "in_scope",
  1367	    "applicability_reason": "contract clause",
  1368	    "materiality": "material"
  1369	  },
  1370	  {
  1371	    "id": "5.3.18.5",
  1372	    "proposition": "Вернуть терминалы в течение 5 рабочих дней с даты расторжения или получения требования.",
  1373	    "party": "neutral/definitional",
  1374	    "right_or_obligation": "declaration",
  1375	    "object": "electronic terminals",
  1376	    "trigger": "upon event",
  1377	    "material_terms": "",
  1378	    "applicability": "in_scope",
  1379	    "applicability_reason": "contract clause",
  1380	    "materiality": "material"
  1381	  },
  1382	  {
  1383	    "id": "5.3.19",
  1384	    "proposition": "Возместить Исполнителю в полном объеме: средства, списанные по спорам; средства по недействительным операциям; сборы и расходы по спорам; убытки от штрафных санкций и ответственности.",
  1385	    "party": "neutral/definitional",
  1386	    "right_or_obligation": "declaration",
  1387	    "object": "liability/penalties",
  1388	    "trigger": "upon event",
  1389	    "material_terms": "",
  1390	    "applicability": "in_scope",
  1391	    "applicability_reason": "contract clause",
  1392	    "materiality": "material"
  1393	  },
  1394	  {
  1395	    "id": "5.3.20",
  1396	    "proposition": "Заказчик передает ПДн руководителя (ФИО, адрес, паспортные данные). Гарантирует правовые основания, в т.ч. для передачи в Платежную систему МИР.",
  1397	    "party": "neutral/definitional",
  1398	    "right_or_obligation": "declaration",
  1399	    "object": "personal data",
  1400	    "trigger": "upon event",
  1401	    "material_terms": "",
  1402	    "applicability": "in_scope",
  1403	    "applicability_reason": "contract clause",
  1404	    "materiality": "material"
  1405	  },
  1406	  {
  1407	    "id": "5.4",
  1408	    "proposition": "Заказчик вправе:",
  1409	    "party": "Заказчик (right-holder)",
  1410	    "right_or_obligation": "right",
  1411	    "object": "general",
  1412	    "trigger": "upon event",
  1413	    "material_terms": "",
  1414	    "applicability": "in_scope",
  1415	    "applicability_reason": "contract clause",
  1416	    "materiality": "material"
  1417	  },
  1418	  {
  1419	    "id": "5.4.1",
  1420	    "proposition": "Требовать от Исполнителя надлежащего исполнения обязательств.",
  1421	    "party": "neutral/definitional",
  1422	    "right_or_obligation": "declaration",
  1423	    "object": "general",
  1424	    "trigger": "upon event",
  1425	    "material_terms": "",
  1426	    "applicability": "in_scope",
  1427	    "applicability_reason": "contract clause",
  1428	    "materiality": "material"
  1429	  },
  1430	  {
  1431	    "id": "5.4.2",
  1432	    "proposition": "Отказать в приемке услуг ненадлежащего качества.",
  1433	    "party": "neutral/definitional",
  1434	    "right_or_obligation": "declaration",
  1435	    "object": "acceptance of services",
  1436	    "trigger": "upon event",
  1437	    "material_terms": "",
  1438	    "applicability": "in_scope",
  1439	    "applicability_reason": "contract clause",
  1440	    "materiality": "material"
  1441	  },
  1442	  {
  1443	    "id": "5.4.3",
  1444	    "proposition": "Принять решение об одностороннем отказе от контракта по основаниям 44-ФЗ и ГК РФ.",
  1445	    "party": "neutral/definitional",
  1446	    "right_or_obligation": "declaration",
  1447	    "object": "termination/refusal",
  1448	    "trigger": "upon event",
  1449	    "material_terms": "",
  1450	    "applicability": "in_scope",
  1451	    "applicability_reason": "contract clause",
  1452	    "materiality": "material"
  1453	  },
  1454	  {
  1455	    "id": "5.4.4",
  1456	    "proposition": "Отказаться от оплаты некачественных услуг, потребовать возврата сумм и возмещения убытков.",
  1457	    "party": "neutral/definitional",
  1458	    "right_or_obligation": "declaration",
  1459	    "object": "payment for services",
  1460	    "trigger": "upon event",
  1461	    "material_terms": "",
  1462	    "applicability": "in_scope",
  1463	    "applicability_reason": "contract clause",
  1464	    "materiality": "material"
  1465	  },
  1466	  {
  1467	    "id": "5.4.5",
  1468	    "proposition": "Ссылаться на возможность оплаты картами в рекламных материалах, предварительно согласовав с исполнителем.",
  1469	    "party": "neutral/definitional",
  1470	    "right_or_obligation": "declaration",
  1471	    "object": "general",
  1472	    "trigger": "upon event",
  1473	    "material_terms": "",
  1474	    "applicability": "in_scope",
  1475	    "applicability_reason": "contract clause",
  1476	    "materiality": "material"
  1477	  },
  1478	  {
  1479	    "id": "5.5",
  1480	    "proposition": "Заказчик обязуется передавать письменное заявление об обстоятельствах операции в течение 3 рабочих дней. Немедленно сообщать об утрате документов.",
  1481	    "party": "Заказчик (obligation-bearer)",
  1482	    "right_or_obligation": "obligation",
  1483	    "object": "application/statement",
  1484	    "trigger": "standing",
  1485	    "material_terms": "",
  1486	    "applicability": "in_scope",
  1487	    "applicability_reason": "contract clause",
  1488	    "materiality": "material"
  1489	  },
  1490	  {
  1491	    "id": "5.6",
  1492	    "proposition": "Заказчик обязуется в случае утери оборудования вернуть терминалы в течение 5 рабочих дней.",
  1493	    "party": "Заказчик (obligation-bearer)",
  1494	    "right_or_obligation": "obligation",
  1495	    "object": "electronic terminals",
  1496	    "trigger": "standing",
  1497	    "material_terms": "",
  1498	    "applicability": "in_scope",
  1499	    "applicability_reason": "contract clause",
  1500	    "materiality": "material"
  1501	  },
  1502	  {
  1503	    "id": "5.7",
  1504	    "proposition": "Штраф за невозврат: 10 000 руб. за Электронный терминал, 25 000 руб. за Смарт-терминал.",
  1505	    "party": "neutral/definitional",
  1506	    "right_or_obligation": "declaration",
  1507	    "object": "electronic terminals",
  1508	    "trigger": "upon event",
  1509	    "material_terms": "",
  1510	    "applicability": "in_scope",
  1511	    "applicability_reason": "contract clause",
  1512	    "materiality": "material"
  1513	  },
  1514	  {
  1515	    "id": "5.9",
  1516	    "proposition": "Заказчик вправе получать консультацию у исполнителя по эксплуатации терминалов и проведению операций.",
  1517	    "party": "Заказчик (right-holder)",
  1518	    "right_or_obligation": "right",
  1519	    "object": "terminal installation/maintenance",
  1520	    "trigger": "upon event",
  1521	    "material_terms": "",
  1522	    "applicability": "in_scope",
  1523	    "applicability_reason": "contract clause",
  1524	    "materiality": "material"
  1525	  },
  1526	  {
  1527	    "id": "5.10",
  1528	    "proposition": "Заказчик обязуется обеспечить самостоятельное прохождение инструктажа сотрудниками на сайте.",
  1529	    "party": "Заказчик (obligation-bearer)",
  1530	    "right_or_obligation": "obligation",
  1531	    "object": "staff training",
  1532	    "trigger": "standing",
  1533	    "material_terms": "",
  1534	    "applicability": "in_scope",
  1535	    "applicability_reason": "contract clause",
  1536	    "materiality": "material"
  1537	  },
  1538	  {
  1539	    "id": "6",
  1540	    "proposition": "АНТИКОРРУПЦИОННАЯ ОГОВОРКА",
  1541	    "party": "neutral/definitional",
  1542	    "right_or_obligation": "declaration",
  1543	    "object": "general",
  1544	    "trigger": "upon event",
  1545	    "material_terms": "",
  1546	    "applicability": "in_scope",
  1547	    "applicability_reason": "contract clause",
  1548	    "materiality": "material"
  1549	  },
  1550	  {
  1551	    "id": "6.1",
  1552	    "proposition": "Стороны обязуются не осуществлять коррупционных действий.",
  1553	    "party": "both",
  1554	    "right_or_obligation": "declaration",
  1555	    "object": "anti-corruption",
  1556	    "trigger": "upon event",
  1557	    "material_terms": "",
  1558	    "applicability": "in_scope",
  1559	    "applicability_reason": "contract clause",
  1560	    "materiality": "material"
  1561	  },
  1562	  {
  1563	    "id": "7",
  1564	    "proposition": "ОТВЕТСТВЕННОСТЬ СТОРОН",
  1565	    "party": "neutral/definitional",
  1566	    "right_or_obligation": "declaration",
  1567	    "object": "general",
  1568	    "trigger": "upon event",
  1569	    "material_terms": "",
  1570	    "applicability": "in_scope",
  1571	    "applicability_reason": "contract clause",
  1572	    "materiality": "material"
  1573	  },
  1574	  {
  1575	    "id": "7.1",
  1576	    "proposition": "Ответственность по законодательству РФ. Освобождение при непреодолимой силе или вине другой стороны. Общая сумма штрафов не превышает цену контракта.",
  1577	    "party": "neutral/definitional",
  1578	    "right_or_obligation": "declaration",
  1579	    "object": "liability/penalties",
  1580	    "trigger": "upon event",
  1581	    "material_terms": "",
  1582	    "applicability": "in_scope",
  1583	    "applicability_reason": "contract clause",
  1584	    "materiality": "material"
  1585	  },
  1586	  {
  1587	    "id": "7.2",
  1588	    "proposition": "При просрочке Заказчика Исполнитель вправе потребовать неустойки.",
  1589	    "party": "Исполнитель (right-holder)",
  1590	    "right_or_obligation": "right",
  1591	    "object": "liability/penalties",
  1592	    "trigger": "upon event",
  1593	    "material_terms": "",
  1594	    "applicability": "in_scope",
  1595	    "applicability_reason": "contract clause",
  1596	    "materiality": "material"
  1597	  },
  1598	  {
  1599	    "id": "7.3",
  1600	    "proposition": "Пеня за просрочку Заказчика – 1/300 ключевой ставки ЦБ РФ от неуплаченной суммы.",
  1601	    "party": "neutral/definitional",
  1602	    "right_or_obligation": "declaration",
  1603	    "object": "general",
  1604	    "trigger": "upon event",
  1605	    "material_terms": "",
  1606	    "applicability": "in_scope",
  1607	    "applicability_reason": "contract clause",
  1608	    "materiality": "material"
  1609	  },
  1610	  {
  1611	    "id": "7.4",
  1612	    "proposition": "Штрафы за ненадлежащее исполнение Заказчиком (кроме просрочки).",
  1613	    "party": "neutral/definitional",
  1614	    "right_or_obligation": "declaration",
  1615	    "object": "general",
  1616	    "trigger": "upon event",
  1617	    "material_terms": "",
  1618	    "applicability": "in_scope",
  1619	    "applicability_reason": "contract clause",
  1620	    "materiality": "material"
  1621	  },
  1622	  {
  1623	    "id": "7.4.1",
  1624	    "proposition": "Размер штрафа Заказчику по Постановлению №1042: 1000-100000 руб. в зависимости от цены контракта.",
  1625	    "party": "neutral/definitional",
  1626	    "right_or_obligation": "declaration",
  1627	    "object": "liability/penalties",
  1628	    "trigger": "upon event",
  1629	    "material_terms": "",
  1630	    "applicability": "in_scope",
  1631	    "applicability_reason": "contract clause",
  1632	    "materiality": "material"
  1633	  },
  1634	  {
  1635	    "id": "7.5",
  1636	    "proposition": "При просрочке Исполнителя Заказчик направляет требование об уплате неустоек.",
  1637	    "party": "neutral/definitional",
  1638	    "right_or_obligation": "declaration",
  1639	    "object": "general",
  1640	    "trigger": "upon event",
  1641	    "material_terms": "",
  1642	    "applicability": "in_scope",
  1643	    "applicability_reason": "contract clause",
  1644	    "materiality": "material"
  1645	  },
  1646	  {
  1647	    "id": "7.6",
  1648	    "proposition": "Пеня за просрочку Исполнителя – 1/300 ключевой ставки ЦБ РФ от цены контракта.",
  1649	    "party": "neutral/definitional",
  1650	    "right_or_obligation": "declaration",
  1651	    "object": "general",
  1652	    "trigger": "upon event",
  1653	    "material_terms": "",
  1654	    "applicability": "in_scope",
  1655	    "applicability_reason": "contract clause",
  1656	    "materiality": "material"
  1657	  },
  1658	  {
  1659	    "id": "7.7",
  1660	    "proposition": "Штрафы за неисполнение Исполнителем (кроме просрочки).",
  1661	    "party": "neutral/definitional",
  1662	    "right_or_obligation": "declaration",
  1663	    "object": "general",
  1664	    "trigger": "upon event",
  1665	    "material_terms": "",
  1666	    "applicability": "in_scope",
  1667	    "applicability_reason": "contract clause",
  1668	    "materiality": "material"
  1669	  },
  1670	  {
  1671	    "id": "7.7.1",
  1672	    "proposition": "Размер штрафа Исполнителю по Постановлению №1042: от 0.1% до 10% цены контракта.",
  1673	    "party": "neutral/definitional",
  1674	    "right_or_obligation": "declaration",
  1675	    "object": "liability/penalties",
  1676	    "trigger": "upon event",
  1677	    "material_terms": "",
  1678	    "applicability": "in_scope",
  1679	    "applicability_reason": "contract clause",
  1680	    "materiality": "material"
  1681	  },
  1682	  {
  1683	    "id": "7.7.2",
  1684	    "proposition": "Штраф Исполнителю как победителю закупки.",
  1685	    "party": "neutral/definitional",
  1686	    "right_or_obligation": "declaration",
  1687	    "object": "general",
  1688	    "trigger": "upon event",
  1689	    "material_terms": "",
  1690	    "applicability": "in_scope",
  1691	    "applicability_reason": "contract clause",
  1692	    "materiality": "material"
  1693	  },
  1694	  {
  1695	    "id": "7.7.3",
  1696	    "proposition": "Штраф за обязательства без стоимостного выражения: 1000-100000 руб.",
  1697	    "party": "neutral/definitional",
  1698	    "right_or_obligation": "declaration",
  1699	    "object": "general",
  1700	    "trigger": "upon event",
Tool:   1201	  },
  1202	  {
  1203	    "id": "5.2.1",
  1204	    "proposition": "обязательство обеспечить доступ к СПЭП; описание порядка доступа к СПЭП",
  1205	    "party": "Банк (obligation-bearer)",
  1206	    "right_or_obligation": "obligation",
  1207	    "object": "SPEP",
  1208	    "trigger": "standing obligation",
  1209	    "material_terms": "none explicit",
  1210	    "applicability": "in_scope",
  1211	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
  1212	    "materiality": "material"
  1213	  },
  1214	  {
  1215	    "id": "5.2.2",
  1216	    "proposition": "использование современных протоколов безопасности; использование технологий 3DSecure",
  1217	    "party": "Банк (obligation-bearer)",
  1218	    "right_or_obligation": "obligation",
  1219	    "object": "general",
  1220	    "trigger": "standing obligation",
  1221	    "material_terms": "none explicit",
  1222	    "applicability": "in_scope",
  1223	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
  1224	    "materiality": "material"
  1225	  },
  1226	  {
  1227	    "id": "5.2.3",
  1228	    "proposition": "Важно, чтобы в договоре срок установки был не менее 3 рабочих дней. Срок инструктажа не декларируется. Отсутствие отсылки на с инструктивные материалы разногласием не является",
  1229	    "party": "Банк (obligation-bearer)",
  1230	    "right_or_obligation": "obligation",
  1231	    "object": "electronic terminals",
  1232	    "trigger": "standing obligation",
  1233	    "material_terms": "none explicit",
  1234	    "applicability": "in_scope",
  1235	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
  1236	    "materiality": "material"
  1237	  },
  1238	  {
  1239	    "id": "5.2.4",
  1240	    "proposition": "Банк осуществляет Авторизацию без перерывов 24 часа в сутки",
  1241	    "party": "Банк (obligation-bearer)",
  1242	    "right_or_obligation": "obligation",
  1243	    "object": "authorization",
  1244	    "trigger": "standing obligation",
  1245	    "material_terms": "none explicit",
  1246	    "applicability": "in_scope",
  1247	    "applicability_reason": "product=common, lot=common, terminal=common",
  1248	    "materiality": "material"
  1249	  },
  1250	  {
  1251	    "id": "5.2.5",
  1252	    "proposition": "Подсвечивать разногласие, если только сайты отличаются, если в договоре вместо сайта прочерк, то это не разногласие",
  1253	    "party": "Банк (obligation-bearer)",
  1254	    "right_or_obligation": "obligation",
  1255	    "object": "staff training",
  1256	    "trigger": "standing obligation",
  1257	    "material_terms": "none explicit",
  1258	    "applicability": "in_scope",
  1259	    "applicability_reason": "product=common, lot=common, terminal=common",
  1260	    "materiality": "material"
  1261	  },
  1262	  {
  1263	    "id": "5.2.6",
  1264	    "proposition": "Обеспечение Электронных терминалов информационными материалами; Обеспечение Смарт-терминалов информационными материалами",
  1265	    "party": "Банк (obligation-bearer)",
  1266	    "right_or_obligation": "obligation",
  1267	    "object": "electronic terminals",
  1268	    "trigger": "standing obligation",
  1269	    "material_terms": "none explicit",
  1270	    "applicability": "in_scope",
  1271	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
  1272	    "materiality": "material"
  1273	  },
  1274	  {
  1275	    "id": "5.2.7",
  1276	    "proposition": "круглосуточная работоспособность Электронных терминалов/Смарт-терминалов; замена неисправного Электронного терминала/Смарт-терминала на исправный не позднее 3 рабочих дней после заявки",
  1277	    "party": "Банк (obligation-bearer)",
  1278	    "right_or_obligation": "obligation",
  1279	    "object": "electronic terminals",
  1280	    "trigger": "standing obligation",
  1281	    "material_terms": "none explicit",
  1282	    "applicability": "in_scope",
  1283	    "applicability_reason": "product=common, lot=common, terminal=common",
  1284	    "materiality": "material"
  1285	  },
  1286	  {
  1287	    "id": "5.2.8",
  1288	    "proposition": "Важен срок перечисления средств",
  1289	    "party": "Банк (obligation-bearer)",
  1290	    "right_or_obligation": "obligation",
  1291	    "object": "QR-code",
  1292	    "trigger": "standing obligation",
  1293	    "material_terms": "none explicit",
  1294	    "applicability": "in_scope",
  1295	    "applicability_reason": "product=common, lot=common, terminal=common",
  1296	    "materiality": "material"
  1297	  },
  1298	  {
  1299	    "id": "5.2.9",
  1300	    "proposition": "Предоставление QR-кода партнера в электронном виде или на бумажном носителе",
  1301	    "party": "Банк (obligation-bearer)",
  1302	    "right_or_obligation": "obligation",
  1303	    "object": "QR-code",
  1304	    "trigger": "standing obligation",
  1305	    "material_terms": "none explicit",
  1306	    "applicability": "in_scope",
  1307	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=common",
  1308	    "materiality": "material"
  1309	  },
  1310	  {
  1311	    "id": "5.2.10",
  1312	    "proposition": "«ПРАВА И ОБЯЗАННОСТИ БАНКА» → Банк обязуется: → Осуществлять обработку ПДн, полученных от Предприятия, а также обеспечить конфиденциальность и защиту обрабатываемых ПДн в соответствии с требованиями Ф",
  1313	    "party": "Банк (obligation-bearer)",
  1314	    "right_or_obligation": "obligation",
  1315	    "object": "personal data",
  1316	    "trigger": "standing obligation",
  1317	    "material_terms": "none explicit",
  1318	    "applicability": "in_scope",
  1319	    "applicability_reason": "product=common, lot=common, terminal=common",
  1320	    "materiality": "material"
  1321	  },
  1322	  {
  1323	    "id": "5.2.12",
  1324	    "proposition": "Банк предоставляет QR-API без гарантий",
  1325	    "party": "Банк (obligation-bearer)",
  1326	    "right_or_obligation": "obligation",
  1327	    "object": "QR-API",
  1328	    "trigger": "standing obligation",
  1329	    "material_terms": "none explicit",
  1330	    "applicability": "in_scope",
  1331	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
  1332	    "materiality": "material"
  1333	  },
  1334	  {
  1335	    "id": "6.1",
  1336	    "proposition": "Важно",
  1337	    "party": "both/neutral",
  1338	    "right_or_obligation": "declaration",
  1339	    "object": "general",
  1340	    "trigger": "standing obligation",
  1341	    "material_terms": "none explicit",
  1342	    "applicability": "in_scope",
  1343	    "applicability_reason": "product=common, lot=common, terminal=common",
  1344	    "materiality": "material"
  1345	  },
  1346	  {
  1347	    "id": "6.2",
  1348	    "proposition": "УПД - это универсальный передаточный документ (документ о приёмке, документ на оплату услуг). Важно проверить сроки и периодичность оплаты",
  1349	    "party": "both/neutral",
  1350	    "right_or_obligation": "declaration",
  1351	    "object": "general",
  1352	    "trigger": "standing obligation",
  1353	    "material_terms": "VAT",
  1354	    "applicability": "in_scope",
  1355	    "applicability_reason": "product=common, lot=common, terminal=common",
  1356	    "materiality": "material"
  1357	  },
  1358	  {
  1359	    "id": "6.3",
  1360	    "proposition": "Банк направляет Акт до 10 рабочего дня месяца, следующего за отчетным; Акт направляется вместе со счетом-фактурой формы 363; Размер вознаграждения определяется согласно пункту 6.1 договора; Вознаграждение банка не облагается НДС на основании п.3 ст.149 НК РФ; Срок направления Банком документа на опл",
  1361	    "party": "both/neutral",
  1362	    "right_or_obligation": "declaration",
  1363	    "object": "settlement/payment",
  1364	    "trigger": "standing obligation",
  1365	    "material_terms": "VAT",
  1366	    "applicability": "in_scope",
  1367	    "applicability_reason": "product=common, lot=fz_223, terminal=common; 223-FZ lot",
  1368	    "materiality": "material"
  1369	  },
  1370	  {
  1371	    "id": "6.4",
  1372	    "proposition": "Предприятие обязано принять и возвратить УПД (принять оказанные услуги); Предприятие предоставляет мотивированный отказ от подписания УПД в установленные сроки",
  1373	    "party": "both/neutral",
  1374	    "right_or_obligation": "obligation",
  1375	    "object": "general",
  1376	    "trigger": "standing obligation",
  1377	    "material_terms": "none explicit",
  1378	    "applicability": "in_scope",
  1379	    "applicability_reason": "product=common, lot=common, terminal=common",
  1380	    "materiality": "material"
  1381	  },
  1382	  {
  1383	    "id": "6.5",
  1384	    "proposition": "оплата услуг банка осуществляется в течение 5 рабочих дней после подписания УПД; форма оплаты - безналичная; денежные средства перечисляются на счет банка, указанный в УПД",
  1385	    "party": "both/neutral",
  1386	    "right_or_obligation": "declaration",
  1387	    "object": "service fees",
  1388	    "trigger": "standing obligation",
  1389	    "material_terms": "none explicit",
  1390	    "applicability": "in_scope",
  1391	    "applicability_reason": "product=common, lot=common, terminal=common",
  1392	    "materiality": "material"
  1393	  },
  1394	  {
  1395	    "id": "6.6",
  1396	    "proposition": "оплата услуг банка осуществляется в течение 5 рабочих дней после получения акта и счета формы 363; форма оплаты - безналичная; перечисление средств производится на счет, указанный в счете формы 363",
  1397	    "party": "both/neutral",
  1398	    "right_or_obligation": "declaration",
  1399	    "object": "service fees",
  1400	    "trigger": "standing obligation",
  1401	    "material_terms": "none explicit",
  1402	    "applicability": "in_scope",
  1403	    "applicability_reason": "product=common, lot=fz_223, terminal=common; 223-FZ lot",
  1404	    "materiality": "material"
  1405	  },
  1406	  {
  1407	    "id": "6.7",
  1408	    "proposition": "указан размер платы за сервисное обслуживание Электронного терминала; указано количество рублей включая НДС; установлен ежемесячный порядок оплаты",
  1409	    "party": "both/neutral",
  1410	    "right_or_obligation": "declaration",
  1411	    "object": "electronic terminals",
  1412	    "trigger": "standing obligation",
  1413	    "material_terms": "VAT",
  1414	    "applicability": "in_scope",
  1415	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1416	    "materiality": "material"
  1417	  },
  1418	  {
  1419	    "id": "6.8",
  1420	    "proposition": "Банк направляет УПД не позднее 5 рабочего дня месяца, следующего за отчетным; УПД направляется на сумму платы за сервисное обслуживание Электронных терминалов",
  1421	    "party": "both/neutral",
  1422	    "right_or_obligation": "declaration",
  1423	    "object": "general",
  1424	    "trigger": "standing obligation",
  1425	    "material_terms": "none explicit",
  1426	    "applicability": "in_scope",
  1427	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1428	    "materiality": "material"
  1429	  },
  1430	  {
  1431	    "id": "6.9",
  1432	    "proposition": "Банк выставляет счет не позднее 10 рабочего дня месяца, следующего за отчетным; Счет выставляется по форме №363; Счет содержит сумму платы за сервисное обслуживание Электронных терминалов; Счет-фактура предоставляется в соответствии с налоговым законодательством РФ",
  1433	    "party": "both/neutral",
  1434	    "right_or_obligation": "declaration",
  1435	    "object": "general",
  1436	    "trigger": "standing obligation",
  1437	    "material_terms": "none explicit",
  1438	    "applicability": "in_scope",
  1439	    "applicability_reason": "product=trade_acquiring, lot=fz_223, terminal=smart; 223-FZ lot",
  1440	    "materiality": "material"
  1441	  },
  1442	  {
  1443	    "id": "6.10",
  1444	    "proposition": "Предприятие возвращает подписанный УПД не позднее 25 числа месяца, следующего за отчетным; Предприятие предоставляет мотивированный отказ от подписания УПД в указанные сроки",
  1445	    "party": "both/neutral",
  1446	    "right_or_obligation": "obligation",
  1447	    "object": "general",
  1448	    "trigger": "standing obligation",
  1449	    "material_terms": "none explicit",
  1450	    "applicability": "in_scope",
  1451	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1452	    "materiality": "material"
  1453	  },
  1454	  {
  1455	    "id": "6.11",
  1456	    "proposition": "оплата за сервисное обслуживание Электронных терминалов производится в течение 5 рабочих дней; способ оплаты - безналичная форма; деньги перечисляются на счет Банка, указанный в УПД",
  1457	    "party": "both/neutral",
  1458	    "right_or_obligation": "declaration",
  1459	    "object": "electronic terminals",
  1460	    "trigger": "standing obligation",
  1461	    "material_terms": "none explicit",
  1462	    "applicability": "in_scope",
  1463	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1464	    "materiality": "material"
  1465	  },
  1466	  {
  1467	    "id": "6.12",
  1468	    "proposition": "Оплата производится в течение 5 рабочих дней; Способ оплаты - безналичный перевод; Основание для оплаты - счет формы 363; Получатель платежа - счет Банка, указанный в счете",
  1469	    "party": "both/neutral",
  1470	    "right_or_obligation": "declaration",
  1471	    "object": "electronic terminals",
  1472	    "trigger": "standing obligation",
  1473	    "material_terms": "none explicit",
  1474	    "applicability": "in_scope",
  1475	    "applicability_reason": "product=trade_acquiring, lot=fz_223, terminal=smart; 223-FZ lot",
  1476	    "materiality": "material"
  1477	  },
  1478	  {
  1479	    "id": "6.13",
  1480	    "proposition": "плата за сервисное обслуживание Смарт-терминалов ежемесячная; расчет платы пропорционально дням месяца с даты установки терминала; пересчет платы при подключении/отключении 2D сканера за отчетный месяц; указана точная стоимость обслуживания",
  1481	    "party": "both/neutral",
  1482	    "right_or_obligation": "declaration",
  1483	    "object": "smart terminals",
  1484	    "trigger": "standing obligation",
  1485	    "material_terms": "VAT",
  1486	    "applicability": "in_scope",
  1487	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1488	    "materiality": "material"
  1489	  },
  1490	  {
  1491	    "id": "6.14",
  1492	    "proposition": "Банк направляет УПД не позднее 5 рабочего дня месяца, следующего за отчетным; УПД направляется на сумму платы за сервисное обслуживание Смарт-терминалов",
  1493	    "party": "both/neutral",
  1494	    "right_or_obligation": "declaration",
  1495	    "object": "smart terminals",
  1496	    "trigger": "standing obligation",
  1497	    "material_terms": "none explicit",
  1498	    "applicability": "in_scope",
  1499	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1500	    "materiality": "material"
  1501	  },
  1502	  {
  1503	    "id": "6.15",
  1504	    "proposition": "Банк выставляет счет не позднее 10 рабочего дня месяца, следующего за отчетным; Счет-фактура предоставляется в соответствии с налоговым законодательством РФ",
  1505	    "party": "both/neutral",
  1506	    "right_or_obligation": "declaration",
  1507	    "object": "general",
  1508	    "trigger": "standing obligation",
  1509	    "material_terms": "none explicit",
  1510	    "applicability": "in_scope",
  1511	    "applicability_reason": "product=trade_acquiring, lot=fz_223, terminal=smart; 223-FZ lot",
  1512	    "materiality": "material"
  1513	  },
  1514	  {
  1515	    "id": "6.16",
  1516	    "proposition": "Предприятие возвращает подписанный УПД не позднее 25 числа месяца, следующего за отчетным; Предприятие предоставляет мотивированный отказ от подписания УПД в установленные сроки",
  1517	    "party": "both/neutral",
  1518	    "right_or_obligation": "obligation",
  1519	    "object": "general",
  1520	    "trigger": "standing obligation",
  1521	    "material_terms": "none explicit",
  1522	    "applicability": "in_scope",
  1523	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1524	    "materiality": "material"
  1525	  },
  1526	  {
  1527	    "id": "6.17",
  1528	    "proposition": "оплата сервиса Смарт-терминалов осуществляется в течение 5 рабочих дней после подписания УПД; форма оплаты - безналичная; деньги перечисляются на счет Банка, указанный в УПД",
  1529	    "party": "both/neutral",
  1530	    "right_or_obligation": "declaration",
  1531	    "object": "smart terminals",
  1532	    "trigger": "standing obligation",
  1533	    "material_terms": "none explicit",
  1534	    "applicability": "in_scope",
  1535	    "applicability_reason": "product=trade_acquiring, lot=common, terminal=smart",
  1536	    "materiality": "material"
  1537	  },
  1538	  {
  1539	    "id": "6.18",
  1540	    "proposition": "оплата производится в течение 5 рабочих дней; способ оплаты - безналичный перевод; основание для оплаты - счет формы 363; срок оплаты считается с даты получения счета",
  1541	    "party": "both/neutral",
  1542	    "right_or_obligation": "declaration",
  1543	    "object": "smart terminals",
  1544	    "trigger": "standing obligation",
  1545	    "material_terms": "none explicit",
  1546	    "applicability": "in_scope",
  1547	    "applicability_reason": "product=trade_acquiring, lot=fz_223, terminal=smart; 223-FZ lot",
  1548	    "materiality": "material"
  1549	  },
  1550	  {
  1551	    "id": "6.20",
  1552	    "proposition": "Важен сам факт, что Банк не берёт новую комиссию, а так же, что первоначальная комиссия не возвращается",
  1553	    "party": "both/neutral",
  1554	    "right_or_obligation": "declaration",
  1555	    "object": "deduction/withholding",
  1556	    "trigger": "standing obligation",
  1557	    "material_terms": "none explicit",
  1558	    "applicability": "in_scope",
  1559	    "applicability_reason": "product=common, lot=common, terminal=common",
  1560	    "materiality": "material"
  1561	  },
  1562	  {
  1563	    "id": "6.21",
  1564	    "proposition": "Отсутствие конкретной ценны не является противоречием",
  1565	    "party": "both/neutral",
  1566	    "right_or_obligation": "declaration",
  1567	    "object": "contract price",
  1568	    "trigger": "standing obligation",
  1569	    "material_terms": "VAT",
  1570	    "applicability": "in_scope",
  1571	    "applicability_reason": "product=common, lot=common, terminal=common",
  1572	    "materiality": "material"
  1573	  },
  1574	  {
  1575	    "id": "7.1",
  1576	    "proposition": "Общие слова о том, что за неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с условиями Договора; Общие слова о том, что за неисполнение или ненадлежащее исполнение обязательств по Договору Стороны несут ответственность в соответствии с за",
  1577	    "party": "both/neutral",
  1578	    "right_or_obligation": "declaration",
  1579	    "object": "liability",
  1580	    "trigger": "standing obligation",
  1581	    "material_terms": "none explicit",
  1582	    "applicability": "in_scope",
  1583	    "applicability_reason": "product=common, lot=common, terminal=common",
  1584	    "materiality": "material"
  1585	  },
  1586	  {
  1587	    "id": "7.2",
  1588	    "proposition": "Важно, что штраф именно Предприятию, важен размер штрафа",
  1589	    "party": "both/neutral",
  1590	    "right_or_obligation": "declaration",
  1591	    "object": "general",
  1592	    "trigger": "standing obligation",
  1593	    "material_terms": "amount/formula; penalty",
  1594	    "applicability": "in_scope",
  1595	    "applicability_reason": "product=common, lot=common, terminal=common",
  1596	    "materiality": "material"
  1597	  },
  1598	  {
  1599	    "id": "7.3",
  1600	    "proposition": "Общая сумма штрафов за ненадлежащее исполнение Предприятием обязательств не превышает цену договора",
  1601	    "party": "both/neutral",
  1602	    "right_or_obligation": "declaration",
  1603	    "object": "penalties",
  1604	    "trigger": "standing obligation",
  1605	    "material_terms": "penalty",
  1606	    "applicability": "in_scope",
  1607	    "applicability_reason": "product=common, lot=common, terminal=common",
  1608	    "materiality": "material"
  1609	  },
  1610	  {
  1611	    "id": "7.4",
  1612	    "proposition": "В случае просрочки исполнения Банком обязательств, Предприятие направляет Банку требование об уплате неустоек (штрафов, пеней); Штраф Банку. Начисление пени за каждый день просрочки; Штраф Банку.Определения срока начала начисления пени; Штраф Банку. Определение размера пени",
  1613	    "party": "both/neutral",
  1614	    "right_or_obligation": "declaration",
  1615	    "object": "general",
  1616	    "trigger": "standing obligation",
  1617	    "material_terms": "penalty",
  1618	    "applicability": "in_scope",
  1619	    "applicability_reason": "product=common, lot=common, terminal=common",
  1620	    "materiality": "material"
  1621	  },
  1622	  {
  1623	    "id": "7.5",
  1624	    "proposition": "Размер штрафа за неисполнение или ненадлежащее исполнение обязательств Банком, за исключением просрочки, имеющих стоимостное выражения в процентах от суммы договора",
  1625	    "party": "both/neutral",
  1626	    "right_or_obligation": "declaration",
  1627	    "object": "general",
  1628	    "trigger": "upon occurrence of specified event",
  1629	    "material_terms": "amount/formula; penalty",
  1630	    "applicability": "in_scope",
  1631	    "applicability_reason": "product=common, lot=common, terminal=common",
  1632	    "materiality": "material"
  1633	  },
  1634	  {
  1635	    "id": "7.6",
  1636	    "proposition": "Размер штрафа за неисполнение или ненадлежащее исполнение обязательств Банком, не имеющего стоимостного выражения",
  1637	    "party": "both/neutral",
  1638	    "right_or_obligation": "declaration",
  1639	    "object": "penalties",
  1640	    "trigger": "standing obligation",
  1641	    "material_terms": "amount/formula; penalty",
  1642	    "applicability": "in_scope",
  1643	    "applicability_reason": "product=common, lot=common, terminal=common",
  1644	    "materiality": "material"
  1645	  },
  1646	  {
  1647	    "id": "7.7",
  1648	    "proposition": "Общая сумма штрафов за нарушения Банка не превышает цену договора",
  1649	    "party": "both/neutral",
  1650	    "right_or_obligation": "declaration",
  1651	    "object": "penalties",
  1652	    "trigger": "standing obligation",
  1653	    "material_terms": "penalty",
  1654	    "applicability": "in_scope",
  1655	    "applicability_reason": "product=common, lot=common, terminal=common",
  1656	    "materiality": "material"
  1657	  },
  1658	  {
  1659	    "id": "7.8",
  1660	    "proposition": "Важен факт, что Банк (Исполнитель) не несет ответственности по спорам и разногласиям Предприятия(Заказчика) и Покупателя (клиент Предприятия)",
  1661	    "party": "both/neutral",
  1662	    "right_or_obligation": "declaration",
  1663	    "object": "liability",
  1664	    "trigger": "standing obligation",
  1665	    "material_terms": "none explicit",
  1666	    "applicability": "in_scope",
  1667	    "applicability_reason": "product=common, lot=common, terminal=common",
  1668	    "materiality": "technical"
  1669	  },
  1670	  {
  1671	    "id": "7.9",
  1672	    "proposition": "Банк освобожден от ответственности при задержках переводов без своей вины",
  1673	    "party": "both/neutral",
  1674	    "right_or_obligation": "declaration",
  1675	    "object": "liability",
  1676	    "trigger": "standing obligation",
  1677	    "material_terms": "none explicit",
  1678	    "applicability": "in_scope",
  1679	    "applicability_reason": "product=common, lot=common, terminal=common",
  1680	    "materiality": "technical"
  1681	  },
  1682	  {
  1683	    "id": "7.10",
  1684	    "proposition": "Банк не несёт ответственность за неисполнение условий Договора в связи с действием и бездействием третьих лиц",
  1685	    "party": "both/neutral",
  1686	    "right_or_obligation": "declaration",
  1687	    "object": "liability",
  1688	    "trigger": "standing obligation",
  1689	    "material_terms": "none explicit",
  1690	    "applicability": "in_scope",
  1691	    "applicability_reason": "product=common, lot=common, terminal=common",
  1692	    "materiality": "technical"
  1693	  },
  1694	  {
  1695	    "id": "7.11",
  1696	    "proposition": "Банк освобождается от ответственности за задержку перечисления средств в случае инициирования им расследования операций",
  1697	    "party": "both/neutral",
  1698	    "right_or_obligation": "declaration",
  1699	    "object": "settlement/payment",
  1700	    "trigger": "standing obligation",
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 1700, 'limit': 500}, 'id': 'call_00_qH0Qp3oI6WB514ZhoLNN4346', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'offset': 1700, 'limit': 500}, 'id': 'call_01_WuKKu6B0in6bk3wpu9QT5728', 'type': 'tool_call'}]
Tool:   1701	    "material_terms": "",
  1702	    "applicability": "in_scope",
  1703	    "applicability_reason": "contract clause",
  1704	    "materiality": "material"
  1705	  },
  1706	  {
  1707	    "id": "7.8",
  1708	    "proposition": "Обмен документами по мерам ответственности через ЕИС с УКЭП.",
  1709	    "party": "neutral/definitional",
  1710	    "right_or_obligation": "declaration",
  1711	    "object": "liability/penalties",
  1712	    "trigger": "upon event",
  1713	    "material_terms": "",
  1714	    "applicability": "in_scope",
  1715	    "applicability_reason": "contract clause",
  1716	    "materiality": "material"
  1717	  },
  1718	  {
  1719	    "id": "7.9",
  1720	    "proposition": "Неустойка не освобождает от исполнения обязательств.",
  1721	    "party": "neutral/definitional",
  1722	    "right_or_obligation": "declaration",
  1723	    "object": "general",
  1724	    "trigger": "upon event",
  1725	    "material_terms": "",
  1726	    "applicability": "in_scope",
  1727	    "applicability_reason": "contract clause",
  1728	    "materiality": "material"
  1729	  },
  1730	  {
  1731	    "id": "7.10",
  1732	    "proposition": "Общая сумма штрафов Исполнителю не превышает цену контракта.",
  1733	    "party": "neutral/definitional",
  1734	    "right_or_obligation": "declaration",
  1735	    "object": "liability/penalties",
  1736	    "trigger": "upon event",
  1737	    "material_terms": "",
  1738	    "applicability": "in_scope",
  1739	    "applicability_reason": "contract clause",
  1740	    "materiality": "material"
  1741	  },
  1742	  {
  1743	    "id": "7.11",
  1744	    "proposition": "Общая сумма штрафов Заказчику не превышает цену контракта.",
  1745	    "party": "neutral/definitional",
  1746	    "right_or_obligation": "declaration",
  1747	    "object": "liability/penalties",
  1748	    "trigger": "upon event",
  1749	    "material_terms": "",
  1750	    "applicability": "in_scope",
  1751	    "applicability_reason": "contract clause",
  1752	    "materiality": "material"
  1753	  },
  1754	  {
  1755	    "id": "7.12",
  1756	    "proposition": "При расторжении в связи с односторонним отказом – возмещение только фактического ущерба сверх неустоек.",
  1757	    "party": "neutral/definitional",
  1758	    "right_or_obligation": "declaration",
  1759	    "object": "termination/refusal",
  1760	    "trigger": "upon event",
  1761	    "material_terms": "",
  1762	    "applicability": "in_scope",
  1763	    "applicability_reason": "contract clause",
  1764	    "materiality": "material"
  1765	  },
  1766	  {
  1767	    "id": "8",
  1768	    "proposition": "КАЧЕСТВО УСЛУГ, ПОРЯДОК ПРИЕМКИ. ГАРАНТИЯ КАЧЕСТВА",
  1769	    "party": "neutral/definitional",
  1770	    "right_or_obligation": "declaration",
  1771	    "object": "general",
  1772	    "trigger": "upon event",
  1773	    "material_terms": "",
  1774	    "applicability": "in_scope",
  1775	    "applicability_reason": "contract clause",
  1776	    "materiality": "material"
  1777	  },
  1778	  {
  1779	    "id": "8.1",
  1780	    "proposition": "Исполнитель гарантирует качество услуг в соответствии с Приложением №1.",
  1781	    "party": "neutral/definitional",
  1782	    "right_or_obligation": "declaration",
  1783	    "object": "general",
  1784	    "trigger": "upon event",
  1785	    "material_terms": "",
  1786	    "applicability": "in_scope",
  1787	    "applicability_reason": "contract clause",
  1788	    "materiality": "material"
  1789	  },
  1790	  {
  1791	    "id": "8.2",
  1792	    "proposition": "Исполнитель несет ответственность за повреждения от действий специалистов.",
  1793	    "party": "neutral/definitional",
  1794	    "right_or_obligation": "declaration",
  1795	    "object": "liability/penalties",
  1796	    "trigger": "upon event",
  1797	    "material_terms": "",
  1798	    "applicability": "in_scope",
  1799	    "applicability_reason": "contract clause",
  1800	    "materiality": "material"
  1801	  },
  1802	  {
  1803	    "id": "8.3",
  1804	    "proposition": "Приемка результата исполнения Контракта в порядке, установленном законодательством и Контрактом.",
  1805	    "party": "neutral/definitional",
  1806	    "right_or_obligation": "declaration",
  1807	    "object": "general",
  1808	    "trigger": "upon event",
  1809	    "material_terms": "",
  1810	    "applicability": "in_scope",
  1811	    "applicability_reason": "contract clause",
  1812	    "materiality": "material"
  1813	  },
  1814	  {
  1815	    "id": "8.3.1",
  1816	    "proposition": "Исполнитель ежемесячно не позднее 10 рабочего дня формирует в ЕИС документ о приемке с УКЭП.",
  1817	    "party": "neutral/definitional",
  1818	    "right_or_obligation": "declaration",
  1819	    "object": "acceptance of services",
  1820	    "trigger": "upon event",
  1821	    "material_terms": "",
  1822	    "applicability": "in_scope",
  1823	    "applicability_reason": "contract clause",
  1824	    "materiality": "material"
  1825	  },
  1826	  {
  1827	    "id": "8.3.2",
  1828	    "proposition": "К документу о приемке прилагаются: счет-фактура, акт о перечислении сумм, счет ф.363.",
  1829	    "party": "neutral/definitional",
  1830	    "right_or_obligation": "declaration",
  1831	    "object": "acceptance of services",
  1832	    "trigger": "upon event",
  1833	    "material_terms": "",
  1834	    "applicability": "in_scope",
  1835	    "applicability_reason": "contract clause",
  1836	    "materiality": "material"
  1837	  },
  1838	  {
  1839	    "id": "8.4",
  1840	    "proposition": "Датой поступления документа о приемке считается дата размещения в ЕИС.",
  1841	    "party": "neutral/definitional",
  1842	    "right_or_obligation": "declaration",
  1843	    "object": "acceptance of services",
  1844	    "trigger": "upon event",
  1845	    "material_terms": "",
  1846	    "applicability": "in_scope",
  1847	    "applicability_reason": "contract clause",
  1848	    "materiality": "material"
  1849	  },
  1850	  {
  1851	    "id": "8.5",
  1852	    "proposition": "Приемка услуг производится уполномоченным лицом или приемочной комиссией.",
  1853	    "party": "neutral/definitional",
  1854	    "right_or_obligation": "declaration",
  1855	    "object": "general",
  1856	    "trigger": "upon event",
  1857	    "material_terms": "",
  1858	    "applicability": "in_scope",
  1859	    "applicability_reason": "contract clause",
  1860	    "materiality": "material"
  1861	  },
  1862	  {
  1863	    "id": "8.5.1",
  1864	    "proposition": "Заказчик в срок не более 10 рабочих дней подписывает документ о приемке или формирует мотивированный отказ.",
  1865	    "party": "neutral/definitional",
  1866	    "right_or_obligation": "declaration",
  1867	    "object": "acceptance of services",
  1868	    "trigger": "upon event",
  1869	    "material_terms": "",
  1870	    "applicability": "in_scope",
  1871	    "applicability_reason": "contract clause",
  1872	    "materiality": "material"
  1873	  },
  1874	  {
  1875	    "id": "8.5.2",
  1876	    "proposition": "Приемка может производиться в присутствии представителя Исполнителя.",
  1877	    "party": "neutral/definitional",
  1878	    "right_or_obligation": "declaration",
  1879	    "object": "general",
  1880	    "trigger": "upon event",
  1881	    "material_terms": "",
  1882	    "applicability": "in_scope",
  1883	    "applicability_reason": "contract clause",
  1884	    "materiality": "material"
  1885	  },
  1886	  {
  1887	    "id": "8.5.3",
  1888	    "proposition": "При уведомлении об участии – приемка в двустороннем порядке.",
  1889	    "party": "neutral/definitional",
  1890	    "right_or_obligation": "declaration",
  1891	    "object": "acceptance of services",
  1892	    "trigger": "upon event",
  1893	    "material_terms": "",
  1894	    "applicability": "in_scope",
  1895	    "applicability_reason": "contract clause",
  1896	    "materiality": "material"
  1897	  },
  1898	  {
  1899	    "id": "8.5.4",
  1900	    "proposition": "Без уведомления – приемка Заказчиком в одностороннем порядке.",
  1901	    "party": "neutral/definitional",
  1902	    "right_or_obligation": "declaration",
  1903	    "object": "acceptance of services",
  1904	    "trigger": "upon event",
  1905	    "material_terms": "",
  1906	    "applicability": "in_scope",
  1907	    "applicability_reason": "contract clause",
  1908	    "materiality": "material"
  1909	  },
  1910	  {
  1911	    "id": "8.5.5",
  1912	    "proposition": "Заказчик проводит экспертизу оказанных услуг.",
  1913	    "party": "neutral/definitional",
  1914	    "right_or_obligation": "declaration",
  1915	    "object": "general",
  1916	    "trigger": "upon event",
  1917	    "material_terms": "",
  1918	    "applicability": "in_scope",
  1919	    "applicability_reason": "contract clause",
  1920	    "materiality": "material"
  1921	  },
  1922	  {
  1923	    "id": "8.5.6",
  1924	    "proposition": "Экспертиза своими силами или с привлечением экспертов.",
  1925	    "party": "neutral/definitional",
  1926	    "right_or_obligation": "declaration",
  1927	    "object": "general",
  1928	    "trigger": "upon event",
  1929	    "material_terms": "",
  1930	    "applicability": "in_scope",
  1931	    "applicability_reason": "contract clause",
  1932	    "materiality": "material"
  1933	  },
  1934	  {
  1935	    "id": "8.5.7",
  1936	    "proposition": "При отсутствии замечаний – подписание документа о приемке в течение 10 рабочих дней.",
  1937	    "party": "neutral/definitional",
  1938	    "right_or_obligation": "declaration",
  1939	    "object": "acceptance of services",
  1940	    "trigger": "upon event",
  1941	    "material_terms": "",
  1942	    "applicability": "in_scope",
  1943	    "applicability_reason": "contract clause",
  1944	    "materiality": "material"
  1945	  },
  1946	  {
  1947	    "id": "8.5.8",
  1948	    "proposition": "При несоответствиях – приемочная комиссия. Подписание или мотивированный отказ в течение 10 рабочих дней.",
  1949	    "party": "neutral/definitional",
  1950	    "right_or_obligation": "declaration",
  1951	    "object": "termination/refusal",
  1952	    "trigger": "upon event",
  1953	    "material_terms": "",
  1954	    "applicability": "in_scope",
  1955	    "applicability_reason": "contract clause",
  1956	    "materiality": "material"
  1957	  },
  1958	  {
  1959	    "id": "8.5.9",
  1960	    "proposition": "Исполнитель вправе устранить причины отказа и направить исправленный документ.",
  1961	    "party": "Исполнитель (right-holder)",
  1962	    "right_or_obligation": "right",
  1963	    "object": "termination/refusal",
  1964	    "trigger": "upon event",
  1965	    "material_terms": "",
  1966	    "applicability": "in_scope",
  1967	    "applicability_reason": "contract clause",
  1968	    "materiality": "material"
  1969	  },
  1970	  {
  1971	    "id": "8.6",
  1972	    "proposition": "Датой приемки считается дата размещения в ЕИС подписанного документа о приемке.",
  1973	    "party": "neutral/definitional",
  1974	    "right_or_obligation": "declaration",
  1975	    "object": "acceptance of services",
  1976	    "trigger": "upon event",
  1977	    "material_terms": "",
  1978	    "applicability": "in_scope",
  1979	    "applicability_reason": "contract clause",
  1980	    "materiality": "material"
  1981	  },
  1982	  {
  1983	    "id": "8.7",
  1984	    "proposition": "Исправления в документ о приемке – через формирование исправленного документа.",
  1985	    "party": "neutral/definitional",
  1986	    "right_or_obligation": "declaration",
  1987	    "object": "acceptance of services",
  1988	    "trigger": "upon event",
  1989	    "material_terms": "",
  1990	    "applicability": "in_scope",
  1991	    "applicability_reason": "contract clause",
  1992	    "materiality": "material"
  1993	  },
  1994	  {
  1995	    "id": "8.8",
  1996	    "proposition": "Оформление результата приемки в порядке и сроки раздела 8.",
  1997	    "party": "neutral/definitional",
  1998	    "right_or_obligation": "declaration",
  1999	    "object": "acceptance of services",
  2000	    "trigger": "upon event",
  2001	    "material_terms": "",
  2002	    "applicability": "in_scope",
  2003	    "applicability_reason": "contract clause",
  2004	    "materiality": "material"
  2005	  },
  2006	  {
  2007	    "id": "8.9",
  2008	    "proposition": "Заказчик вправе не отказывать в приемке при устранимом несоответствии.",
  2009	    "party": "Заказчик (right-holder)",
  2010	    "right_or_obligation": "right",
  2011	    "object": "acceptance of services",
  2012	    "trigger": "upon event",
  2013	    "material_terms": "",
  2014	    "applicability": "in_scope",
  2015	    "applicability_reason": "contract clause",
  2016	    "materiality": "material"
  2017	  },
  2018	  {
  2019	    "id": "8.10",
  2020	    "proposition": "При ненадлежащем качестве – безвозмездное устранение недостатков в течение 3 дней.",
  2021	    "party": "neutral/definitional",
  2022	    "right_or_obligation": "declaration",
  2023	    "object": "general",
  2024	    "trigger": "upon event",
  2025	    "material_terms": "",
  2026	    "applicability": "in_scope",
  2027	    "applicability_reason": "contract clause",
  2028	    "materiality": "material"
  2029	  },
  2030	  {
  2031	    "id": "8.11",
  2032	    "proposition": "Подписанный документ о приемке – основание для оплаты.",
  2033	    "party": "neutral/definitional",
  2034	    "right_or_obligation": "declaration",
  2035	    "object": "acceptance of services",
  2036	    "trigger": "upon event",
  2037	    "material_terms": "",
  2038	    "applicability": "in_scope",
  2039	    "applicability_reason": "contract clause",
  2040	    "materiality": "material"
  2041	  },
  2042	  {
  2043	    "id": "9",
  2044	    "proposition": "ДЕЙСТВИЕ ОБСТОЯТЕЛЬСТВ НЕПРЕОДОЛИМОЙ СИЛЫ",
  2045	    "party": "neutral/definitional",
  2046	    "right_or_obligation": "declaration",
  2047	    "object": "general",
  2048	    "trigger": "upon event",
  2049	    "material_terms": "",
  2050	    "applicability": "in_scope",
  2051	    "applicability_reason": "contract clause",
  2052	    "materiality": "material"
  2053	  },
  2054	  {
  2055	    "id": "9.1",
  2056	    "proposition": "Освобождение от ответственности при непреодолимой силе: стихийные бедствия, наводнения, землетрясения, пожары, военные действия, забастовки, эпидемии.",
  2057	    "party": "neutral/definitional",
  2058	    "right_or_obligation": "declaration",
  2059	    "object": "liability/penalties",
  2060	    "trigger": "upon event",
  2061	    "material_terms": "",
  2062	    "applicability": "in_scope",
  2063	    "applicability_reason": "contract clause",
  2064	    "materiality": "material"
  2065	  },
  2066	  {
  2067	    "id": "9.2",
  2068	    "proposition": "Уведомление не позднее 5 дней. Срок переносится соразмерно. При длительности более месяца – право расторгнуть.",
  2069	    "party": "neutral/definitional",
  2070	    "right_or_obligation": "declaration",
  2071	    "object": "general",
  2072	    "trigger": "upon event",
  2073	    "material_terms": "",
  2074	    "applicability": "in_scope",
  2075	    "applicability_reason": "contract clause",
  2076	    "materiality": "material"
  2077	  },
  2078	  {
  2079	    "id": "9.3",
  2080	    "proposition": "Сторона, ссылающаяся на обстоятельства, обязана представить документальное подтверждение.",
  2081	    "party": "neutral/definitional",
  2082	    "right_or_obligation": "obligation",
  2083	    "object": "general",
  2084	    "trigger": "upon event",
  2085	    "material_terms": "",
  2086	    "applicability": "in_scope",
  2087	    "applicability_reason": "contract clause",
  2088	    "materiality": "material"
  2089	  },
  2090	  {
  2091	    "id": "10",
  2092	    "proposition": "ПОРЯДОК РАЗРЕШЕНИЯ СПОРОВ",
  2093	    "party": "neutral/definitional",
  2094	    "right_or_obligation": "declaration",
  2095	    "object": "general",
  2096	    "trigger": "upon event",
  2097	    "material_terms": "",
  2098	    "applicability": "in_scope",
  2099	    "applicability_reason": "contract clause",
  2100	    "materiality": "material"
  2101	  },
  2102	  {
  2103	    "id": "10.1",
  2104	    "proposition": "Споры разрешаются путем переговоров. Срок ответа на претензии – 10 календарных дней. Обмен по мерам ответственности через ЕИС.",
  2105	    "party": "neutral/definitional",
  2106	    "right_or_obligation": "declaration",
  2107	    "object": "liability/penalties",
  2108	    "trigger": "upon event",
  2109	    "material_terms": "",
  2110	    "applicability": "in_scope",
  2111	    "applicability_reason": "contract clause",
  2112	    "materiality": "material"
  2113	  },
  2114	  {
  2115	    "id": "10.2",
  2116	    "proposition": "При невозможности разрешения – Арбитражный суд Краснодарского края.",
  2117	    "party": "neutral/definitional",
  2118	    "right_or_obligation": "declaration",
  2119	    "object": "general",
  2120	    "trigger": "upon event",
  2121	    "material_terms": "",
  2122	    "applicability": "in_scope",
  2123	    "applicability_reason": "contract clause",
  2124	    "materiality": "material"
  2125	  },
  2126	  {
  2127	    "id": "11",
  2128	    "proposition": "СРОК ДЕЙСТВИЯ, ПОРЯДОК ИЗМЕНЕНИЯ И РАСТОРЖЕНИЯ",
  2129	    "party": "neutral/definitional",
  2130	    "right_or_obligation": "declaration",
  2131	    "object": "general",
  2132	    "trigger": "upon event",
  2133	    "material_terms": "",
  2134	    "applicability": "in_scope",
  2135	    "applicability_reason": "contract clause",
  2136	    "materiality": "material"
  2137	  },
  2138	  {
  2139	    "id": "11.1",
  2140	    "proposition": "Контракт действует с даты заключения по 30.12.2025 или до исчерпания цены. По обязательствам – до полного исполнения.",
  2141	    "party": "neutral/definitional",
  2142	    "right_or_obligation": "declaration",
  2143	    "object": "general",
  2144	    "trigger": "upon event",
  2145	    "material_terms": "",
  2146	    "applicability": "in_scope",
  2147	    "applicability_reason": "contract clause",
  2148	    "materiality": "material"
  2149	  },
  2150	  {
  2151	    "id": "11.2",
  2152	    "proposition": "Изменения – в письменной форме, подписаны обеими Сторонами. Об изменении реквизитов – уведомление в течение 2 дней.",
  2153	    "party": "neutral/definitional",
  2154	    "right_or_obligation": "declaration",
  2155	    "object": "general",
  2156	    "trigger": "upon event",
  2157	    "material_terms": "",
  2158	    "applicability": "in_scope",
  2159	    "applicability_reason": "contract clause",
  2160	    "materiality": "material"
  2161	  },
  2162	  {
  2163	    "id": "11.3",
  2164	    "proposition": "Расторжение по соглашению, по решению суда, односторонний отказ по ГК РФ.",
  2165	    "party": "neutral/definitional",
  2166	    "right_or_obligation": "declaration",
  2167	    "object": "termination/refusal",
  2168	    "trigger": "upon event",
  2169	    "material_terms": "",
  2170	    "applicability": "in_scope",
  2171	    "applicability_reason": "contract clause",
  2172	    "materiality": "material"
  2173	  },
  2174	  {
  2175	    "id": "11.4",
  2176	    "proposition": "Заказчик вправе на односторонний отказ по основаниям ГК РФ.",
  2177	    "party": "Заказчик (right-holder)",
  2178	    "right_or_obligation": "right",
  2179	    "object": "termination/refusal",
  2180	    "trigger": "upon event",
  2181	    "material_terms": "",
  2182	    "applicability": "in_scope",
  2183	    "applicability_reason": "contract clause",
  2184	    "materiality": "material"
  2185	  },
  2186	  {
  2187	    "id": "11.5",
  2188	    "proposition": "Односторонний отказ – в порядке ст.95 44-ФЗ.",
  2189	    "party": "neutral/definitional",
  2190	    "right_or_obligation": "declaration",
  2191	    "object": "termination/refusal",
  2192	    "trigger": "upon event",
  2193	    "material_terms": "",
  2194	    "applicability": "in_scope",
  2195	    "applicability_reason": "contract clause",
  2196	    "materiality": "material"
  2197	  },
  2198	  {
  2199	    "id": "11.6",
  2200	    "proposition": "Изменение/расторжение – по ст.34, 95, 96, 112 44-ФЗ.",
Tool:   1701	    "material_terms": "none explicit",
  1702	    "applicability": "in_scope",
  1703	    "applicability_reason": "product=common, lot=common, terminal=common",
  1704	    "materiality": "technical"
  1705	  },
  1706	  {
  1707	    "id": "7.12",
  1708	    "proposition": "Общие слова о том, что банк освобожден от ответственности при превышении Цены Договора",
  1709	    "party": "both/neutral",
  1710	    "right_or_obligation": "declaration",
  1711	    "object": "liability",
  1712	    "trigger": "upon occurrence of specified event",
  1713	    "material_terms": "none explicit",
  1714	    "applicability": "in_scope",
  1715	    "applicability_reason": "product=common, lot=common, terminal=common",
  1716	    "materiality": "technical"
  1717	  },
  1718	  {
  1719	    "id": "7.13",
  1720	    "proposition": "Предприятие несет ответственность за некорректные операции на Ресурсе",
  1721	    "party": "both/neutral",
  1722	    "right_or_obligation": "declaration",
  1723	    "object": "liability",
  1724	    "trigger": "upon occurrence of specified event",
  1725	    "material_terms": "none explicit",
  1726	    "applicability": "in_scope",
  1727	    "applicability_reason": "product=internet_acquiring, lot=common, terminal=common",
  1728	    "materiality": "material"
  1729	  },
  1730	  {
  1731	    "id": "7.14",
  1732	    "proposition": "Общее утверждение о том, что Предприятие несет ответственность за все действия в СПЭП",
  1733	    "party": "both/neutral",
  1734	    "right_or_obligation": "declaration",
  1735	    "object": "liability",
  1736	    "trigger": "standing obligation",
  1737	    "material_terms": "none explicit",
  1738	    "applicability": "in_scope",
  1739	    "applicability_reason": "product=common, lot=common, terminal=common",
  1740	    "materiality": "material"
  1741	  },
  1742	  {
  1743	    "id": "7.15",
  1744	    "proposition": "Важен сам факт несения ответственности, если в договоре не говорится про несение ответственности за действия персонала, значит этот пункт не относится к данному",
  1745	    "party": "both/neutral",
  1746	    "right_or_obligation": "declaration",
  1747	    "object": "liability",
  1748	    "trigger": "standing obligation",
  1749	    "material_terms": "none explicit",
  1750	    "applicability": "in_scope",
  1751	    "applicability_reason": "product=common, lot=common, terminal=common",
  1752	    "materiality": "material"
  1753	  },
  1754	  {
  1755	    "id": "7.16",
  1756	    "proposition": "Обязательство не совершать коррупционных и иных противозаконных действий при любых операциях по договору",
  1757	    "party": "both/neutral",
  1758	    "right_or_obligation": "declaration",
  1759	    "object": "termination",
  1760	    "trigger": "standing obligation",
  1761	    "material_terms": "none explicit",
  1762	    "applicability": "in_scope",
  1763	    "applicability_reason": "product=common, lot=common, terminal=common",
  1764	    "materiality": "material"
  1765	  },
  1766	  {
  1767	    "id": "7.17",
  1768	    "proposition": "Важно, чтобы  в договоре не было сужения ответственности.",
  1769	    "party": "both/neutral",
  1770	    "right_or_obligation": "declaration",
  1771	    "object": "liability",
  1772	    "trigger": "upon occurrence of specified event",
  1773	    "material_terms": "none explicit",
  1774	    "applicability": "in_scope",
  1775	    "applicability_reason": "product=common, lot=common, terminal=common",
  1776	    "materiality": "material"
  1777	  },
  1778	  {
  1779	    "id": "8.1",
  1780	    "proposition": "описание форс-мажорных обстоятельств как основание для освобождения от ответственности; перечень конкретных форс-мажорных событий (стихийные бедствия, пожары и т.д.); продление срока исполнения договорных обязательств соразмерно времени действия соответствующего обстоятельства",
  1781	    "party": "both/neutral",
  1782	    "right_or_obligation": "declaration",
  1783	    "object": "liability",
  1784	    "trigger": "standing obligation",
  1785	    "material_terms": "none explicit",
  1786	    "applicability": "in_scope",
  1787	    "applicability_reason": "product=common, lot=common, terminal=common",
  1788	    "materiality": "material"
  1789	  },
  1790	  {
  1791	    "id": "8.2",
  1792	    "proposition": "Обязанность уведомления другой стороны при обстоятельствах непреодолимой силы; Срок уведомления другой стороны при обстоятельствах непреодолимой силы; указание характера форс-мажорных обстоятельств; оценка влияния на исполнение обязательств; предполагаемый срок исполнения при наличии информации; пра",
  1793	    "party": "both/neutral",
  1794	    "right_or_obligation": "declaration",
  1795	    "object": "general",
  1796	    "trigger": "standing obligation",
  1797	    "material_terms": "none explicit",
  1798	    "applicability": "in_scope",
  1799	    "applicability_reason": "product=common, lot=common, terminal=common",
  1800	    "materiality": "material"
  1801	  },
  1802	  {
  1803	    "id": "9.1",
  1804	    "proposition": "соблюден претензионный порядок урегулирования споров; указан обязательный досудебный порядок с указанием срока рассмотрения претензий",
  1805	    "party": "both/neutral",
  1806	    "right_or_obligation": "declaration",
  1807	    "object": "disputes",
  1808	    "trigger": "standing obligation",
  1809	    "material_terms": "none explicit",
  1810	    "applicability": "in_scope",
  1811	    "applicability_reason": "product=common, lot=common, terminal=common",
  1812	    "materiality": "material"
  1813	  },
  1814	  {
  1815	    "id": "9.2",
  1816	    "proposition": "Важен срок рассмотрения претензий",
  1817	    "party": "both/neutral",
  1818	    "right_or_obligation": "declaration",
  1819	    "object": "general",
  1820	    "trigger": "standing obligation",
  1821	    "material_terms": "none explicit",
  1822	    "applicability": "in_scope",
  1823	    "applicability_reason": "product=common, lot=common, terminal=common",
  1824	    "materiality": "material"
  1825	  },
  1826	  {
  1827	    "id": "9.3",
  1828	    "proposition": "РАЗДЕЛ 9 «УРЕГУЛИРОВАНИЕ СПОРОВ» → Споры, не урегулированные в претензионном порядке, подлежат разрешению в соответствии с действующим законодательством РФ.",
  1829	    "party": "both/neutral",
  1830	    "right_or_obligation": "declaration",
  1831	    "object": "general",
  1832	    "trigger": "standing obligation",
  1833	    "material_terms": "none explicit",
  1834	    "applicability": "in_scope",
  1835	    "applicability_reason": "product=common, lot=common, terminal=common",
  1836	    "materiality": "material"
  1837	  },
  1838	  {
  1839	    "id": "10.1",
  1840	    "proposition": "указана дата окончания действия договора; определен порядок учета цены договора при определении срока действия; установлено сохранение ответственности сторон после окончания срока договора",
  1841	    "party": "both/neutral",
  1842	    "right_or_obligation": "declaration",
  1843	    "object": "general",
  1844	    "trigger": "standing obligation",
  1845	    "material_terms": "none explicit",
  1846	    "applicability": "in_scope",
  1847	    "applicability_reason": "product=common, lot=common, terminal=common",
  1848	    "materiality": "material"
  1849	  },
  1850	  {
  1851	    "id": "10.2",
  1852	    "proposition": "Важно описание возможности расторгнуть договор в одностороннем порядке. Важен срок уведомления о расторжении.",
  1853	    "party": "both/neutral",
  1854	    "right_or_obligation": "right",
  1855	    "object": "general",
  1856	    "trigger": "standing obligation",
  1857	    "material_terms": "none explicit",
  1858	    "applicability": "in_scope",
  1859	    "applicability_reason": "product=common, lot=common, terminal=common",
  1860	    "materiality": "material"
  1861	  },
  1862	  {
  1863	    "id": "10.3",
  1864	    "proposition": "Сроки, в которые договор считается расторгнутым в случае расторжения в одностороннем внесудебном порядке; Сроки расчетов после одностороннего внесудебного порядка расторжения - 18 месяцев; Порядок выплаты сумм операций определен в пунктах 5.1.3, 5.1.4 и разделе 6",
  1865	    "party": "both/neutral",
  1866	    "right_or_obligation": "declaration",
  1867	    "object": "termination",
  1868	    "trigger": "upon contract termination",
  1869	    "material_terms": "none explicit",
  1870	    "applicability": "in_scope",
  1871	    "applicability_reason": "product=common, lot=common, terminal=common",
  1872	    "materiality": "material"
  1873	  },
  1874	  {
  1875	    "id": "11.1",
  1876	    "proposition": "Перечисление источников правового регулирования отношений Сторон; Требование соблюдать законодательство РФ; Условия и положения Договора, противоречащие правила Платежной системы должны быть приведены в соответствие",
  1877	    "party": "both/neutral",
  1878	    "right_or_obligation": "declaration",
  1879	    "object": "general",
  1880	    "trigger": "standing obligation",
  1881	    "material_terms": "none explicit",
  1882	    "applicability": "in_scope",
  1883	    "applicability_reason": "product=common, lot=common, terminal=common",
  1884	    "materiality": "material"
  1885	  },
  1886	  {
  1887	    "id": "11.2",
  1888	    "proposition": "Номера Карт/Платежных счетов, персональные данные Покупателей, суммы Операций, информация о платеже являются конфиденциальной информацией; Объявляется запрет на передачу конфиденциальной информации третьим лицам; Даётся разрешение на передачу конфиденциальной информации разрешена, только если это тр",
  1889	    "party": "both/neutral",
  1890	    "right_or_obligation": "declaration",
  1891	    "object": "general",
  1892	    "trigger": "standing obligation",
  1893	    "material_terms": "none explicit",
  1894	    "applicability": "in_scope",
  1895	    "applicability_reason": "product=common, lot=common, terminal=common",
  1896	    "materiality": "technical"
  1897	  },
  1898	  {
  1899	    "id": "11.3",
  1900	    "proposition": "Стороны обязуются не разглашать иным лицам полученные сведения о защитных элементов карт; Стороны обязуются не разглашать иным лицам полученные сведения о технологии проведения операций; Стороны обязуются не разглашать иным лицам полученные сведения о финансовом состоянии сторон; Стороны обязуются н",
  1901	    "party": "both/neutral",
  1902	    "right_or_obligation": "declaration",
  1903	    "object": "general",
  1904	    "trigger": "standing obligation",
  1905	    "material_terms": "none explicit",
  1906	    "applicability": "in_scope",
  1907	    "applicability_reason": "product=common, lot=common, terminal=common",
  1908	    "materiality": "material"
  1909	  },
  1910	  {
  1911	    "id": "11.4",
  1912	    "proposition": "изменения и дополнения должны быть в письменной форме; подписаны уполномоченными представителями обеих сторон",
  1913	    "party": "both/neutral",
  1914	    "right_or_obligation": "declaration",
  1915	    "object": "general",
  1916	    "trigger": "standing obligation",
  1917	    "material_terms": "none explicit",
  1918	    "applicability": "in_scope",
  1919	    "applicability_reason": "product=common, lot=common, terminal=common",
  1920	    "materiality": "technical"
  1921	  },
  1922	  {
  1923	    "id": "11.5",
  1924	    "proposition": "РАЗДЕЛ 11 «ПРОЧИЕ УСЛОВИЯ → Все имевшие место до подписания настоящего Договора соглашения, переговоры и переписка между Сторонами по вопросам, изложенным в настоящем Договоре, утрачивают силу с даты ",
  1925	    "party": "both/neutral",
  1926	    "right_or_obligation": "declaration",
  1927	    "object": "general",
  1928	    "trigger": "standing obligation",
  1929	    "material_terms": "none explicit",
  1930	    "applicability": "in_scope",
  1931	    "applicability_reason": "product=common, lot=common, terminal=common",
  1932	    "materiality": "heading"
  1933	  },
  1934	  {
  1935	    "id": "11.6",
  1936	    "proposition": "Договор составлен в определенном количестве экземпляров; указано количество экземпляров Договора для Банка; указано количество экземпляров Договора для Предприятия",
  1937	    "party": "both/neutral",
  1938	    "right_or_obligation": "declaration",
  1939	    "object": "general",
  1940	    "trigger": "standing obligation",
  1941	    "material_terms": "none explicit",
  1942	    "applicability": "in_scope",
  1943	    "applicability_reason": "product=common, lot=common, terminal=common",
  1944	    "materiality": "technical"
  1945	  },
  1946	  {
  1947	    "id": "11.7",
  1948	    "proposition": "Общие слова про то, что приложения являются неотъемлемой частью договора",
  1949	    "party": "both/neutral",
  1950	    "right_or_obligation": "declaration",
  1951	    "object": "general",
  1952	    "trigger": "standing obligation",
  1953	    "material_terms": "none explicit",
  1954	    "applicability": "in_scope",
  1955	    "applicability_reason": "product=common, lot=common, terminal=common",
  1956	    "materiality": "technical"
  1957	  },
  1958	  {
  1959	    "id": "11.8",
  1960	    "proposition": "Предприятие (Заказчик) заверяет, что реализация Товаров/услуг осуществляется в соответствии с требованиями законодательства РФ",
  1961	    "party": "both/neutral",
  1962	    "right_or_obligation": "declaration",
  1963	    "object": "general",
  1964	    "trigger": "standing obligation",
  1965	    "material_terms": "none explicit",
  1966	    "applicability": "in_scope",
  1967	    "applicability_reason": "product=common, lot=common, terminal=common",
  1968	    "materiality": "technical"
  1969	  },
  1970	  {
  1971	    "id": "11.9",
  1972	    "proposition": "запрет передачи обязательств и прав без письменного согласия другой стороны; возможность передачи обязательств для случаев реорганизации стороны",
  1973	    "party": "both/neutral",
  1974	    "right_or_obligation": "right",
  1975	    "object": "general",
  1976	    "trigger": "standing obligation",
  1977	    "material_terms": "none explicit",
  1978	    "applicability": "in_scope",
  1979	    "applicability_reason": "product=common, lot=common, terminal=common",
  1980	    "materiality": "material"
  1981	  },
  1982	  {
  1983	    "id": "11.10",
  1984	    "proposition": "При реорганизации одной из Сторон обязательства переходят к правопреемнику; В случае ликвидации одной из сторон - удовлетворение имущественных требований за счет имущества ликвидируемой стороны",
  1985	    "party": "both/neutral",
  1986	    "right_or_obligation": "declaration",
  1987	    "object": "general",
  1988	    "trigger": "standing obligation",
  1989	    "material_terms": "none explicit",
  1990	    "applicability": "in_scope",
  1991	    "applicability_reason": "product=common, lot=common, terminal=common",
  1992	    "materiality": "material"
  1993	  },
  1994	  {
  1995	    "id": "11.11",
  1996	    "proposition": "Если в договоре не указан сайт - это не является разногласием",
  1997	    "party": "both/neutral",
  1998	    "right_or_obligation": "declaration",
  1999	    "object": "general",
  2000	    "trigger": "standing obligation",
  2001	    "material_terms": "none explicit",
  2002	    "applicability": "in_scope",
  2003	    "applicability_reason": "product=common, lot=common, terminal=common",
  2004	    "materiality": "technical"
  2005	  },
  2006	  {
  2007	    "id": "11.12",
  2008	    "proposition": "Важно само наличие такой или похожей формулировки",
  2009	    "party": "both/neutral",
  2010	    "right_or_obligation": "declaration",
  2011	    "object": "general",
  2012	    "trigger": "standing obligation",
  2013	    "material_terms": "none explicit",
  2014	    "applicability": "in_scope",
  2015	    "applicability_reason": "product=common, lot=common, terminal=common",
  2016	    "materiality": "technical"
  2017	  },
  2018	  {
  2019	    "id": "11.13",
  2020	    "proposition": "Перечень документов, приложенных к договору",
  2021	    "party": "both/neutral",
  2022	    "right_or_obligation": "declaration",
  2023	    "object": "service fees",
  2024	    "trigger": "standing obligation",
  2025	    "material_terms": "none explicit",
  2026	    "applicability": "in_scope",
  2027	    "applicability_reason": "product=common, lot=common, terminal=common",
  2028	    "materiality": "technical"
  2029	  }
  2030	]
AI: [{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 2200, 'limit': 500}, 'id': 'call_00_Ogo7ryhp3YvAcSkzrd3O7389', 'type': 'tool_call'}]
Tool:   2201	    "party": "neutral/definitional",
  2202	    "right_or_obligation": "declaration",
  2203	    "object": "termination/refusal",
  2204	    "trigger": "upon event",
  2205	    "material_terms": "",
  2206	    "applicability": "in_scope",
  2207	    "applicability_reason": "contract clause",
  2208	    "materiality": "material"
  2209	  },
  2210	  {
  2211	    "id": "11.7",
  2212	    "proposition": "В остальном – законодательство РФ.",
  2213	    "party": "neutral/definitional",
  2214	    "right_or_obligation": "declaration",
  2215	    "object": "general",
  2216	    "trigger": "upon event",
  2217	    "material_terms": "",
  2218	    "applicability": "in_scope",
  2219	    "applicability_reason": "contract clause",
  2220	    "materiality": "material"
  2221	  },
  2222	  {
  2223	    "id": "11.8",
  2224	    "proposition": "Изменение существенных условий не допускается, кроме случаев 44-ФЗ.",
  2225	    "party": "neutral/definitional",
  2226	    "right_or_obligation": "right",
  2227	    "object": "general",
  2228	    "trigger": "upon event",
  2229	    "material_terms": "",
  2230	    "applicability": "in_scope",
  2231	    "applicability_reason": "contract clause",
  2232	    "materiality": "material"
  2233	  },
  2234	  {
  2235	    "id": "12",
  2236	    "proposition": "ПРОЧИЕ УСЛОВИЯ",
  2237	    "party": "neutral/definitional",
  2238	    "right_or_obligation": "declaration",
  2239	    "object": "general",
  2240	    "trigger": "upon event",
  2241	    "material_terms": "",
  2242	    "applicability": "in_scope",
  2243	    "applicability_reason": "contract clause",
  2244	    "materiality": "material"
  2245	  },
  2246	  {
  2247	    "id": "12.1",
  2248	    "proposition": "Перемена Исполнителя не допускается, кроме правопреемства при реорганизации.",
  2249	    "party": "neutral/definitional",
  2250	    "right_or_obligation": "right",
  2251	    "object": "general",
  2252	    "trigger": "upon event",
  2253	    "material_terms": "",
  2254	    "applicability": "in_scope",
  2255	    "applicability_reason": "contract clause",
  2256	    "materiality": "material"
  2257	  },
  2258	  {
  2259	    "id": "12.2",
  2260	    "proposition": "При перемене Заказчика права и обязанности переходят к новому Заказчику.",
  2261	    "party": "neutral/definitional",
  2262	    "right_or_obligation": "obligation",
  2263	    "object": "general",
  2264	    "trigger": "upon event",
  2265	    "material_terms": "",
  2266	    "applicability": "in_scope",
  2267	    "applicability_reason": "contract clause",
  2268	    "materiality": "material"
  2269	  },
  2270	  {
  2271	    "id": "12.3",
  2272	    "proposition": "Допускается оказание услуг с улучшенными характеристиками.",
  2273	    "party": "neutral/definitional",
  2274	    "right_or_obligation": "declaration",
  2275	    "object": "general",
  2276	    "trigger": "upon event",
  2277	    "material_terms": "",
  2278	    "applicability": "in_scope",
  2279	    "applicability_reason": "contract clause",
  2280	    "materiality": "material"
  2281	  },
  2282	  {
  2283	    "id": "12.4",
  2284	    "proposition": "Контракт в электронной форме, подписан УКЭП.",
  2285	    "party": "neutral/definitional",
  2286	    "right_or_obligation": "declaration",
  2287	    "object": "general",
  2288	    "trigger": "upon event",
  2289	    "material_terms": "",
  2290	    "applicability": "in_scope",
  2291	    "applicability_reason": "contract clause",
  2292	    "materiality": "material"
  2293	  },
  2294	  {
  2295	    "id": "13",
  2296	    "proposition": "МЕСТА НАХОЖДЕНИЯ, БАНКОВСКИЕ РЕКВИЗИТЫ СТОРОН",
  2297	    "party": "neutral/definitional",
  2298	    "right_or_obligation": "declaration",
  2299	    "object": "general",
  2300	    "trigger": "upon event",
  2301	    "material_terms": "",
  2302	    "applicability": "in_scope",
  2303	    "applicability_reason": "contract clause",
  2304	    "materiality": "heading"
  2305	  },
  2306	  {
  2307	    "id": "Приложение №1",
  2308	    "proposition": "Техническое задание. Объект закупки – услуги эквайринга. Платежно-пропускная система «Барс». Перечень ТСТ. Перечень карт. Сроки. Условия: комиссия за терминалы отсутствует, абонентская плата отсутствует, бесконтактная оплата, вывод QR-кода, расчеты в рублях, возмещение на счет казначейства, перечисл",
  2309	    "party": "neutral/definitional",
  2310	    "right_or_obligation": "declaration",
  2311	    "object": "terminal installation/maintenance",
  2312	    "trigger": "upon event",
  2313	    "material_terms": "",
  2314	    "applicability": "in_scope",
  2315	    "applicability_reason": "contract clause",
  2316	    "materiality": "material"
  2317	  },
  2318	  {
  2319	    "id": "Приложение №1.1",
  2320	    "proposition": "ЗАЯВЛЕНИЕ ПРЕДПРИЯТИЯ НА ПРОВЕДЕНИЕ РАСЧЕТОВ ПО ОПЕРАЦИЯМ ОПЛАТЫ ТОВАРОВ/УСЛУГ (форма).",
  2321	    "party": "neutral/definitional",
  2322	    "right_or_obligation": "declaration",
  2323	    "object": "general",
  2324	    "trigger": "upon event",
  2325	    "material_terms": "",
  2326	    "applicability": "in_scope",
  2327	    "applicability_reason": "contract clause",
  2328	    "materiality": "heading"
  2329	  },
  2330	  {
  2331	    "id": "Приложение №1.2",
  2332	    "proposition": "ИНФОРМАЦИЯ О ТОРГОВО-СЕРВИСНОЙ ТОЧКЕ/РЕСУРСЕ ПРЕДПРИЯТИЯ (форма).",
  2333	    "party": "neutral/definitional",
  2334	    "right_or_obligation": "declaration",
  2335	    "object": "general",
  2336	    "trigger": "upon event",
  2337	    "material_terms": "",
  2338	    "applicability": "in_scope",
  2339	    "applicability_reason": "contract clause",
  2340	    "materiality": "heading"
  2341	  },
  2342	  {
  2343	    "id": "Приложение №2",
  2344	    "proposition": "СПЕЦИФИКАЦИЯ (форма).",
  2345	    "party": "neutral/definitional",
  2346	    "right_or_obligation": "declaration",
  2347	    "object": "general",
  2348	    "trigger": "upon event",
  2349	    "material_terms": "",
  2350	    "applicability": "in_scope",
  2351	    "applicability_reason": "contract clause",
  2352	    "materiality": "heading"
  2353	  }
  2354	]
AI: [{'name': 'write_todos', 'args': {'todos': [{'content': 'Read remaining contract_inventory.json entries to completion', 'status': 'completed'}, {'content': 'Read remaining matrix_inventory.json entries to completion', 'status': 'completed'}, {'content': 'Read remaining contract.txt to completion', 'status': 'completed'}, {'content': 'Identify all material contract inventory items not linked to any matrix item', 'status': 'in_progress'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]}, 'id': 'call_00_qNmYJ9g5c1Nhh5eqVmoZ5345', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read remaining contract_inventory.json entries to completion', 'status': 'completed'}, {'content': 'Read remaining matrix_inventory.json entries to completion', 'status': 'completed'}, {'content': 'Read remaining contract.txt to completion', 'status': 'completed'}, {'content': 'Identify all material contract inventory items not linked to any matrix item', 'status': 'in_progress'}, {'content': 'Classify each as extra_in_contract or not_material with materiality_reason', 'status': 'pending'}, {'content': 'Write contract-only findings to /outputs/working/contract_only_findings.json', 'status': 'pending'}]
AI: Now I have both inventories fully read. Let me now systematically identify which contract inventory items are material and have no matrix analogue. I'll build a comprehensive analysis. Let me first create a helper script to cross-reference the inventories and identify the contract-only items.[{'name': 'write_file', 'args': {'file_path': '/outputs/working/contract_only_analysis.py', 'content': '#!/usr/bin/env python3\n"""Mechanical helper: list contract inventory items with their materiality,\nand identify which matrix topics exist for cross-reference.\nDoes NOT make legal judgments — only organizes data for human review."""\n\nimport json\n\nwith open("/outputs/working/contract_inventory.json", "r") as f:\n    contract = json.load(f)\n\nwith open("/outputs/working/matrix_inventory.json", "r") as f:\n    matrix = json.load(f)\n\n# Collect matrix topics/objects for cross-reference\nmatrix_objects = set()\nmatrix_topics = set()\nfor m in matrix:\n    matrix_objects.add(m.get("object", ""))\n    matrix_topics.add(m.get("proposition", ""))\n\n# Print all material contract items\nprint("=== MATERIAL CONTRACT ITEMS ===")\nfor c in contract:\n    if c.get("materiality") == "material":\n        print(f"  {c[\'id\']}: {c[\'proposition\'][:120]}...")\n        print(f"    object={c[\'object\']}, party={c[\'party\']}, right_or_obligation={c[\'right_or_obligation\']}")\n        print()\n\nprint("\\n=== HEADING/TECHNICAL CONTRACT ITEMS ===")\nfor c in contract:\n    if c.get("materiality") in ("heading", "technical"):\n        print(f"  {c[\'id\']}: [{c[\'materiality\']}] {c[\'proposition\'][:120]}...")\n\nprint(f"\\nTotal contract items: {len(contract)}")\nprint(f"Material: {sum(1 for c in contract if c.get(\'materiality\')==\'material\')}")\nprint(f"Technical: {sum(1 for c in contract if c.get(\'materiality\')==\'technical\')}")\nprint(f"Heading: {sum(1 for c in contract if c.get(\'materiality\')==\'heading\')}")\n'}, 'id': 'call_00_XlSg3zsoCYFhqLL2pduL1556', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/contract_only_analysis.py
AI: [{'name': 'execute', 'args': {'command': 'cd / && python /outputs/working/contract_only_analysis.py 2>&1 | head -300'}, 'id': 'call_00_j9IPzmwC4R4lDU2pEMkv3984', 'type': 'tool_call'}]
Tool: [stderr] At line:32 char:6
[stderr] + cd / && python outputs/working/contract_only_analysis.py 2>&1 | head  ...
[stderr] +      ~~
[stderr] The token '&&' is not a valid statement separator in this version.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : InvalidEndOfLine

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python /outputs/working/contract_only_analysis.py'}, 'id': 'call_00_fmSY1u1aZciVkdHGHFDv6981', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\contract_only_analysis.py", line 8, in <module>
[stderr]     with open("/outputs/working/contract_inventory.json", "r") as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/contract_inventory.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python "C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2/outputs/working/contract_only_analysis.py"'}, 'id': 'call_00_exrUXfYODwUNylSAKryS6545', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\contract_only_analysis.py", line 8, in <module>
[stderr]     with open("/outputs/working/contract_inventory.json", "r") as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/outputs/working/contract_inventory.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'ls "C:/Users/gogel/OneDrive/Рабочий стол/Проекты/skillshot_manual_2/outputs/working/"'}, 'id': 'call_00_SBfymSz6k9INfQJJHwkJ1373', 'type': 'tool_call'}]
Tool: 

    РљР°С‚Р°Р»РѕРі: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        25.06.2026     13:34          47836 build_inventories.py                                                 
-a----        25.06.2026     13:34          97575 contract_inventory.json                                              
-a----        25.06.2026     13:37           1473 contract_only_analysis.py                                            
-a----        25.06.2026     13:37            298 count_matrix.py                                                      
-a----        25.06.2026     13:34         109750 matrix_inventory.json                                                

[Command succeeded with exit code 0]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/contract_only_analysis.py', 'old_string': 'with open("/outputs/working/contract_inventory.json", "r") as f:\n    contract = json.load(f)\n\nwith open("/outputs/working/matrix_inventory.json", "r") as f:\n    matrix = json.load(f)', 'new_string': 'import os\nbase = os.path.dirname(os.path.abspath(__file__))\nwith open(os.path.join(base, "contract_inventory.json"), "r", encoding="utf-8") as f:\n    contract = json.load(f)\n\nwith open(os.path.join(base, "matrix_inventory.json"), "r", encoding="utf-8") as f:\n    matrix = json.load(f)'}, 'id': 'call_00_Cqbi2V5V1bJx3PNS5r6R9460', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/contract_only_analysis.py'

