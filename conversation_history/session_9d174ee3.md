## Summarized at 2026-06-25T08:44:36.594735+00:00

Human: Matrix batch 1 comparison
AI: I'll start by reading the skill file and understanding the task structure, then locate the relevant source documents.[{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_plX8JsZ6RRCoHdvFUvrv4050', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': '**/*', 'path': '/'}, 'id': 'call_01_nWb2tOROipIVrWcFHkGG7874', 'type': 'tool_call'}]
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
Tool: ['/.env', '/.git/COMMIT_EDITMSG', '/.git/FETCH_HEAD', '/.git/HEAD', '/.git/ORIG_HEAD', '/.git/config', '/.git/description', '/.git/hooks/applypatch-msg.sample', '/.git/hooks/commit-msg.sample', '/.git/hooks/fsmonitor-watchman.sample', '/.git/hooks/post-update.sample', '/.git/hooks/pre-applypatch.sample', '/.git/hooks/pre-commit.sample', '/.git/hooks/pre-merge-commit.sample', '/.git/hooks/pre-push.sample', '/.git/hooks/pre-rebase.sample', '/.git/hooks/pre-receive.sample', '/.git/hooks/prepare-commit-msg.sample', '/.git/hooks/push-to-checkout.sample', '/.git/hooks/sendemail-validate.sample', '/.git/hooks/update.sample', '/.git/index', '/.git/info/exclude', '/.git/logs/HEAD', '/.git/logs/refs/heads/clear-branch', '/.git/logs/refs/heads/codex/clear_one_skill', '/.git/logs/refs/heads/main', '/.git/logs/refs/heads/one_skill', '/.git/logs/refs/heads/pre=agent', '/.git/logs/refs/heads/test', '/.git/logs/refs/heads/test2', '/.git/logs/refs/heads/test3', '/.git/logs/refs/remotes/origin/HEAD', '/.git/logs/refs/remotes/origin/clear-branch', '/.git/logs/refs/remotes/origin/main', '/.git/logs/refs/remotes/origin/one_skill', '/.git/logs/refs/remotes/origin/pre=agent', '/.git/logs/refs/remotes/origin/test', '/.git/logs/refs/remotes/origin/test2', '/.git/logs/refs/remotes/origin/test3', '/.git/lost-found/other/003f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/lost-found/other/016411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/lost-found/other/0189548f4f27fcb26840150f585a64515d77c26d', '/.git/lost-found/other/01a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/lost-found/other/02e3706e34f211187bd64efa7a9ad51760195d39', '/.git/lost-found/other/02e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/lost-found/other/0312d61983ef80179bfac79abbba1359052f115c', '/.git/lost-found/other/040be927181b9604d69593ffe36ab7303b1a94bc', '/.git/lost-found/other/04378a998f4a8686eb28f62e8833b0f539229714', '/.git/lost-found/other/04602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/lost-found/other/048703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/lost-found/other/0488481d528674a76807703e6625d6284ca8293e', '/.git/lost-found/other/04eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/lost-found/other/057e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/lost-found/other/05c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/lost-found/other/05e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/lost-found/other/0631461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/lost-found/other/074930d053a799cc4f9095e89196437f704205d6', '/.git/lost-found/other/077efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/lost-found/other/07d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/lost-found/other/082169d84ac7751152d7134fa37292c00ba029d0', '/.git/lost-found/other/0846bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/lost-found/other/0a05a2808a79fe98d007bccb3b1060551300dec8', '/.git/lost-found/other/0a32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/lost-found/other/0a401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/lost-found/other/0a56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/lost-found/other/0a962ce910aa746587b34755922bae542449fba9', '/.git/lost-found/other/0b32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/lost-found/other/0b5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/lost-found/other/0bc5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/lost-found/other/0bebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/lost-found/other/0bf720f21f41ce829add4aab5a9a05012208c3f7', '/.git/lost-found/other/0c4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/lost-found/other/0d72d0b2349a404cc4cddb87c836194765377d74', '/.git/lost-found/other/0d753acfba917272cd72f418e9c1352ed20054f6', '/.git/lost-found/other/0e189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/lost-found/other/0f0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/lost-found/other/0f86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/lost-found/other/0f9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/lost-found/other/108486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/lost-found/other/1152abac92eac8d8b605f61e7608e5151d222f07', '/.git/lost-found/other/11b6a93338766923a8e6379405e6fcf4ab828169', '/.git/lost-found/other/11c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/lost-found/other/13360394a41c8fabc39419ab404191a8575e2799', '/.git/lost-found/other/14394b47e18f572003e3d82368702dfd474b70c4', '/.git/lost-found/other/1474c8f7cf8bc22cda503322795cac94ac621675', '/.git/lost-found/other/159a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/lost-found/other/159bfd26b659195df8c8486d12b5e15f948cb808', '/.git/lost-found/other/15be2e474eb938a89e4d7c19737994893197e781', '/.git/lost-found/other/163d050dd4db671d29be7efff1a35864f91ca61d', '/.git/lost-found/other/1645e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/lost-found/other/1683c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/lost-found/other/16de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/lost-found/other/17a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/lost-found/other/17c6782b615441baeb457ee93a458ed7371c9f99', '/.git/lost-found/other/1862eec0af25e420dee69a16ba235f610f20756d', '/.git/lost-found/other/1876a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/lost-found/other/18d512a4ebe9f93cc357a19059984b3398799bee', '/.git/lost-found/other/18fe30c098f75b96caa54450040279f8727780ea', '/.git/lost-found/other/19928324ad53403e47456f49785dd300a6abc1e0', '/.git/lost-found/other/19ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/lost-found/other/1a3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/lost-found/other/1a412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/lost-found/other/1ae3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/lost-found/other/1bb6184cbc8ec7b0b92597da642ddb7baea3f9f0', '/.git/lost-found/other/1bb94dc37fa7ba202e37fb9f730b2c1ffe60c9f8', '/.git/lost-found/other/1bd948006afad9d92ba0af0d9d6aac84b81201ee', '/.git/lost-found/other/1c5c64af7a4a179928feb3e438ba9aeca2b21785', '/.git/lost-found/other/1c6f0d2fcead6d6b9af167efe84b68ab9867253d', '/.git/lost-found/other/1cb460853dbc76ecd603937b1385d60dfe4544da', '/.git/lost-found/other/1ce139b0630235d7cccd5e7233e06fb27e4b7e92', '/.git/lost-found/other/1d80ca727f627adf666f395a0c85e26662ed0d20', '/.git/lost-found/other/1fb978ebe70aba71b3e2d74d673c0459d8480ac6', '/.git/lost-found/other/2083461eff88321aa0feceaab497bc202e7d110e', '/.git/lost-found/other/20d6d5fa6f6982c1d4d8d927ae5e9e121fe42018', '/.git/lost-found/other/21637826d1d04950f4a4d796a9571a8c4d86b806', '/.git/lost-found/other/21c428f3247ee9fb40e38b78c925eea08e7175aa', '/.git/lost-found/other/21d13a0a40c505324dab511aa407e5dc471bcf1c', '/.git/lost-found/other/226a93510d33d1c407aef258f9c39f42e3f298ad', '/.git/lost-found/other/228c08f34331c47620b55794c64c0ff9897f15c0', '/.git/lost-found/other/22baf3300cc31a3540ca4314fd8c58bcb7018353', '/.git/lost-found/other/22e7afb00fe5b7c7602b761800024ed40d25fe21', '/.git/lost-found/other/230d67a0590a4d61346d6dd5ced3f53dd0f1bea2', '/.git/lost-found/other/238faa3816f1afd26933d98bd81001eb92a2c876', '/.git/lost-found/other/242b028657099781ee5f230d30afc0a8af8423df', '/.git/lost-found/other/245ed230dee59261acbdfe117c3db0280411df76', '/.git/lost-found/other/248a3917f8467ac0cc6218d4b046e8e4b2cba851', '/.git/lost-found/other/248fd8353332111067158f2d11e7087f1ac3fe69', '/.git/lost-found/other/2533d1949584c2a0a3b143a5cb4de3f8c1d17758', '/.git/lost-found/other/253f5f1950cdce8f3dd7dca88b26bfcfcb68ad9e', '/.git/lost-found/other/26194e93e2a767b3f44b2bb12906aad486311c49', '/.git/lost-found/other/26204973c5913550889f7735c6c91e3f23eb971d', '/.git/lost-found/other/2676a4fb754239d1306066ad2d8f58004874245b', '/.git/lost-found/other/26bc257b7c543df579db1afcb9248ced695a5433', '/.git/lost-found/other/27e9ed80c1396df06710f8c7782e989d2230e035', '/.git/lost-found/other/2912b2774fce14827260d4c8ec3a58acaebd30aa', '/.git/lost-found/other/29b9a8951ad9517c1953a163da020fe28852bba9', '/.git/lost-found/other/29f91579b798fbdf2436d2f21c966d128bba04fd', '/.git/lost-found/other/2afee31d90e375b801139b051605dc6f5599d9f1', '/.git/lost-found/other/2b77f7188e91b5f41905b979e1453716042a88d6', '/.git/lost-found/other/2b84077d254fc2a1d66d0b4ea82ef3a7fa125c3a', '/.git/lost-found/other/2ba1ae4723622dd7a36a624626a298bc4aede590', '/.git/lost-found/other/2baa9b4b0fd3a53e07dbaa15098f4c45e7419cd6', '/.git/lost-found/other/2bf2efefce1765ad78030310ed9900afb0cd5522', '/.git/lost-found/other/2c59ee393814f03d894d5d8c75ab7512af596f2b', '/.git/lost-found/other/2ca2261abaa3459cab2e6b5aac65911448fb906a', '/.git/lost-found/other/2d209cca9eecd6d9519f21ae66f180d2001554ef', '/.git/lost-found/other/2d808e55af2eb9b6c496d06a8de71c32578f172a', '/.git/lost-found/other/2d926e4fa759b1b3235635ba6668898a635443f9', '/.git/lost-found/other/2d98f0a835a91e49cb26869dc16dea0583feafbe', '/.git/lost-found/other/2e107635a41522a90f0ea3c1f8fbbb3ff8685f1f', '/.git/lost-found/other/2e395785e7e850594fe6874f052e55a0733d4549', '/.git/lost-found/other/2f29d9394aab14b49d63b7303c6549458f4f7158', '/.git/lost-found/other/2f785e870024de3ac7ca3a834b25ca25e9d9cb8e', '/.git/lost-found/other/2f7887c4fbfd68a3721f5d2cdc896c48bf353c5a', '/.git/lost-found/other/2f807662ed402a67cdc3a86d525264af5ff4fb7d', '/.git/lost-found/other/306a8becbe8f0d8eab7964b3986c9f94ff283e20', '/.git/lost-found/other/312308f273d963ad2f881e414e6dc908c7de72c6', '/.git/lost-found/other/313257cee583598c2b1e76531aee4382a34ae791', '/.git/lost-found/other/31919cbc2e7b9a6268f7bd5ade6a59d4902b52dd', '/.git/lost-found/other/31e88c3eb7be2600a07f8a293e0d521af54d6577', '/.git/lost-found/other/31f64f6e3b537ebaddf428c4cb7764d746510f2b', '/.git/lost-found/other/322ad23a9b2322a5eafbb97fd34f393402a04544', '/.git/lost-found/other/323f82bbbb2a2f435ba1a70ab85e6e604de01b6e', '/.git/lost-found/other/325706343725c6011b78dbccbe34e242657d5d49', '/.git/lost-found/other/327e8f6219bc9ac3aaf5c4e5f8a88559dd9c8d9c', '/.git/lost-found/other/328bc3afc9053e448e43ac838fbde8b5a6bff782', '/.git/lost-found/other/32f8032b0690c3e5ab5788e9a392fb328fdde7e4', '/.git/lost-found/other/332c5bfc92dcc95b0fdab72fec060f0f1fde04f7', '/.git/lost-found/other/33a71c56250cf2a2cf3bc20447d3bc0f4722b8c0', '/.git/lost-found/other/3407448373b50404341f30cfe3e19da4562e5b61', '/.git/lost-found/other/341580a820d2cd018774a99fd90cdd4928badc68', '/.git/lost-found/other/34c6a03cca3744f90eb635e4a427cf083aad4110', '/.git/lost-found/other/353eeeb90d31595d072017c457bdb335470c0b79', '/.git/lost-found/other/35425eeca676d4342ab62ffff6195d41b11f03ba', '/.git/lost-found/other/357377a3e9d1596994eb7db5c89ea3b40161b48a', '/.git/lost-found/other/3598090e6a420d70ef76bde587c93ade0de2721e', '/.git/lost-found/other/36228b5f70a00e5ce49800e5c4e6f423a864ae65', '/.git/lost-found/other/3627eb8009d622db55d0b115ad04a86af57dc99d', '/.git/lost-found/other/376c1e88772f0558744c3ec5bf33e514bcbfa5f4', '/.git/lost-found/other/378b9fa979fd0cdcd74fb98be8f965fc64ba96ab', '/.git/lost-found/other/37ab16fcbeb235841f49b53dda4f8a4cb8576605', '/.git/lost-found/other/37eb658dd959056bdc91ca5add0c61677dd55131', '/.git/lost-found/other/3893a9d23c221f7a7587b3bd1bbce3e53451a36b', '/.git/lost-found/other/393d937812a14bacba39114d3fbc6ba4b6f687e1', '/.git/lost-found/other/393f72379d2551529e19191f444ca8ac0324cc09', '/.git/lost-found/other/398f7fdb157e0e718ddb1b583446c83525a9c8c8', '/.git/lost-found/other/3aa11aec8ea158ebe6fa2976edaac47f213d098c', '/.git/lost-found/other/3ae1b05c2a5d648e1e234162415c93a2d566455a', '/.git/lost-found/other/3b05a03bfb9b84a6f82a3f6b6d4fddb652001ca6', '/.git/lost-found/other/3cc5321661d71bea5e919b2dd222d55638ef6474', '/.git/lost-found/other/3d2058541bd6f85fa9d3041eeb94773535041b4e', '/.git/lost-found/other/3d4090fbbcedee422c984f49d6951366d6e87331', '/.git/lost-found/other/3d76e8038eb8c5d0065da0f378418b0929a3e1c7', '/.git/lost-found/other/3dee1d10be4dc43fdf33e57816608eb7f5f762e9', '/.git/lost-found/other/3ec37580b08a3f792df050067bd3383ad9c01df9', '/.git/lost-found/other/3ecc52a19ba9501ffdc2b0775d42316e3eb031db', '/.git/lost-found/other/3f5e76235147c70911902e9f103daf1a7314e95a', '/.git/lost-found/other/3feb49e8ddc04e5c3e85ae2ec34908b7ea1236c6', '/.git/lost-found/other/40758f589a15d70a0fb173d1dd0cd93c2b280b20', '/.git/lost-found/other/40a857d2f4d88afe60d9d223c3874cb9ccb4a55c', '/.git/lost-found/other/421881dda370e44a27a3e93dc9caa1d44579a990', '/.git/lost-found/other/428a345dcc183804917d5077052693bb113f74e0', '/.git/lost-found/other/429074a78b514abba6f272bd54f3011a72c28afc', '/.git/lost-found/other/42fcf8ab7e1224020d789b4b47b37e4eff58c62f', '/.git/lost-found/other/433079b36165ec24a2b3bfa3208be0e72c68112c', '/.git/lost-found/other/447720e79a8bf68b0570557e2603109333a4a04a', '/.git/lost-found/other/44d6e7a95ef488d9350b45e9cfa358ce04beec08', '/.git/lost-found/other/4678157d773d5c250ee875f3fc5ad8cfbb06ae38', '/.git/lost-found/other/46c6456223387aec0a7b111a58be75f442f3c342', '/.git/lost-found/other/46f574b31ea9c081d10dbc24fb57ba3e4b447b6f', '/.git/lost-found/other/472070c0c081ef4c9ea5e73fce87dec51a5e50bd', '/.git/lost-found/other/473daf24f1e540b2f25a569f819a238aacb81035', '/.git/lost-found/other/47eec38c60613993ebddfe34b03b3c993405009b', '/.git/lost-found/other/48355610f438c75b706f3d1b9bb15c49f849800d', '/.git/lost-found/other/49e4545b844c30e3a2dfd5283289f27650feed77', '/.git/lost-found/other/49e5c2487096098aa82596f7c3bf4b154b03263b', '/.git/lost-found/other/4b0ca8a212de55c027ab38e37ffcd17e341d57bc', '/.git/lost-found/other/4b1106adc7b4c0535779dc0c2df302e2e4f26afb', '/.git/lost-found/other/4b4e6a0046c053a95f57754b9088a81834674349', '/.git/lost-found/other/4b5c220106e4b150f1785aca51b4c1516ee7f6f7', '/.git/lost-found/other/4b825dc642cb6eb9a060e54bf8d69288fbee4904', '/.git/lost-found/other/4c109c4291b72213236a54418e69bc70989d3d23', '/.git/lost-found/other/4d64eae0c3986894803d586d4c44ae16906d23f8', '/.git/lost-found/other/4dae699298c4e827eb777a620bc2b0b622a3d043', '/.git/lost-found/other/4daf2d4fb4be2002d0c6f0783065cd4aaa2ef9d5', '/.git/lost-found/other/4db248d2d0362a2baa123bce350af1c3cf725718', '/.git/lost-found/other/4dba40158ad402bdb18ab94f570242af2ecb9f72', '/.git/lost-found/other/4ddb67d026b4d1d9533591627008838db3040342', '/.git/lost-found/other/4e560d39e66ee48393ac86adf8bf92f390ab6282', '/.git/lost-found/other/4e80ac0c1f3b8a9f86cdccef454912a80077d15a', '/.git/lost-found/other/4ed608f4d1b961b4b069673f0dac7b286868f1d4', '/.git/lost-found/other/4f03978e25b1d70dd18b2f1ce83f070616bee53c', '/.git/lost-found/other/4f6403a8bcb6c19a368e929b9a4e12741e1ab55a', '/.git/lost-found/other/4fb85fbb7c372a0b84cd78fa6b55e410e220239f', '/.git/lost-found/other/503b52b471cf3c48677445669dda1dda8fd71c51', '/.git/lost-found/other/50446582fea97fa549a6039a5f0c504364f69e73', '/.git/lost-found/other/509ba1ee9c66d67aa12183a23911275c84c1be12', '/.git/lost-found/other/50ab5d3cf546c8b875e8c8fecb728a69ed6129e1', '/.git/lost-found/other/50c32b19907ec29e0df34ae3dcb64ccbad1bfeed', '/.git/lost-found/other/5135c970168de2f80375b8e8223d8b65ebe722d9', '/.git/lost-found/other/514ef7a257573e892fef8efdc8092aa113f301a6', '/.git/lost-found/other/515672a3eac687eeaa0d5331a88ae03e9eec92ff', '/.git/lost-found/other/51eddaf2d727e3973ab74f8d0d4d5d6925dfccf8', '/.git/lost-found/other/523cfd7c6c11e165293fcbe926464d35abe0f7ea', '/.git/lost-found/other/526cbab8a8237857d96750d81938f8548229fdd4', '/.git/lost-found/other/52a9fd5d5a39c98cf011809f1954ce924858033a', '/.git/lost-found/other/53c00c790d7213e762a416ccbd9fa61f2cc6b27c', '/.git/lost-found/other/549ef64d2ed3890a06bd03ef59952b31b70a5027', '/.git/lost-found/other/54a41810fd052d9463f8d60abf2c75184362b839', '/.git/lost-found/other/55616d36043061c1a3c7f616e099f6a5abde1e72', '/.git/lost-found/other/55769048317ffd40eca0be3cea5a4b9e5ab7cdba', '/.git/lost-found/other/55b747cbbaf511f4d5424f0f1301ed30b1916007', '/.git/lost-found/other/56e2a20d652ee923dad7ebb9d8aeda679efae502', '/.git/lost-found/other/56ea5e17523abc029922afcc9f23f2306cfef729', '/.git/lost-found/other/56f07bf7f1652d395100a1b2e0b96ed2b54e171c', '/.git/lost-found/other/56f3b2f52e650607bcb68a0a89e36251acb754f3', '/.git/lost-found/other/57b04ada3b0285ca34c1a7fdbb9c904e484a2d14', '/.git/lost-found/other/58bf0f7e675b7588a79421a3fabaf0f35e219290', '/.git/lost-found/other/5928f67430c179dc2031c576bf0b24b51d2bca5b', '/.git/lost-found/other/5983ea75fd9362c5a8709fb10cdfa4920f085b40', '/.git/lost-found/other/59a6d7ca7e0bd39f24f74469da806dd2659236c9', '/.git/lost-found/other/59d110fe6522d55e8e5f8650763f5ff86c935b7e', '/.git/lost-found/other/5a1e4a159d9cbf9d18e6e0da20f04e709b36e923', '/.git/lost-found/other/5a41118850b5b97764e3861fc59a901f69f18298', '/.git/lost-found/other/5aed03d61d3a40a4e4d8859a43e5ff373d789afb', '/.git/lost-found/other/5b03c014dcf3dab20b88f5a62dd0865020292ed4', '/.git/lost-found/other/5b3c284ca03de4c25ced51e9aa3a4b488804a44e', '/.git/lost-found/other/5b42a5fe2abb1393cf2b9ac7359176e4aed00c0a', '/.git/lost-found/other/5c40fd7e30b0ae67c6188ae7825d3ecbe2c432b0', '/.git/lost-found/other/5d51b2cf47c9bec0fd8dfc6a5c742839aead66d3', '/.git/lost-found/other/5dc8c414c8a6dcb39eead75672e29a6c7705fa1c', '/.git/lost-found/other/5fc241b5fc5ee3126714b7ec6bb1218f256b2f9d', '/.git/lost-found/other/5ff9751d696b33f83abfca804807e09e998cc015', '/.git/lost-found/other/604dca6b26bd18ef8041517b5520080d7d019360', '/.git/lost-found/other/608826a2afc590737f32a764a625ef1f8c685dd5', '/.git/lost-found/other/60cd35607497b333c4e689ec8c3d7beefb76d5aa', '/.git/lost-found/other/60e755f3531398a88cb2ba67af858c57dd0ab90d', '/.git/lost-found/other/6128184c716e17ff7c4382e61719214b88a65240', '/.git/lost-found/other/612b7e3dac1b05bc83204b5091634dc99d745a5f', '/.git/lost-found/other/613d1efee79b495719629da39214f79500635967', '/.git/lost-found/other/61c62badbeadcca961fde66023da79591e056332', '/.git/lost-found/other/623e4c399c3cf78aa7bff72e26554c85f6869fe6', '/.git/lost-found/other/62a41bba70c8083d3e9792ce06fcf891c6fa24d5', '/.git/lost-found/other/62b286e180ad3b353b79c522e41cac008f3512b0', '/.git/lost-found/other/6372d5b36494f138c1638b3930d8543e77265803', '/.git/lost-found/other/63e70e5456461721b42c484bbee1886cfc8ba39c', '/.git/lost-found/other/63f2e29d53169726763ff4581e6fdcd3236cdb45', '/.git/lost-found/other/640ebd997c31281a5274fbfcdaf9624d3dca7042', '/.git/lost-found/other/64e4f4a1d9a5c5f3af3076ec413de73a3f5a4100', '/.git/lost-found/other/6589cb9582ca26898931b1ff9fa713b99a51fd69', '/.git/lost-found/other/66161534878c9a2771f904c86c37771812f852de', '/.git/lost-found/other/6638f29e468c5eb3550c99e26aff88a106344cba', '/.git/lost-found/other/668ed8f54785171df27bcc3dd3ca6946b7c47b03', '/.git/lost-found/other/669527a55303ac3089986dfdd5be5379da40b8d6', '/.git/lost-found/other/66b958f32ddafa4f75a7a2cb2f24a9e9ccf2a097', '/.git/lost-found/other/66dc9fe2e67543e8bee36d8b809fc2488132e8d1', '/.git/lost-found/other/66f40ce43c80179972266b9fb98da995998b53c3', '/.git/lost-found/other/6702cfd9756562bfb0a3ba9b5abecffb3edd3d4d', '/.git/lost-found/other/6842fe827192bab8f1180cc0a667d476df9cd850', '/.git/lost-found/other/687cde57acd639e44b9f6ecf4bb3b29996c10bc3', '/.git/lost-found/other/6916bfc4ae8a8656910be8213444648b53a2352d', '/.git/lost-found/other/695a1fc4aabfb29ae1d4eb53d8262b001cf0b268', '/.git/lost-found/other/69ba46d4e80a1ca1f7e61de30c5a0973bcf9949f', '/.git/lost-found/other/6a0e4ee850e4136089b231c7385181f3833d64e5', '/.git/lost-found/other/6a10a4c99f71d892813817d6e131c32de5a3a0b8', '/.git/lost-found/other/6ab43d1c8712b075016024e6de4b2cedad30d4fb', '/.git/lost-found/other/6ab5f05565940fa70b59ade18d5824d49687af69', '/.git/lost-found/other/6ac3752495b076c748fd4e5c4984925643feef75', '/.git/lost-found/other/6b7cbd1cdc3ecae6259e767ec077682ab8140d37', '/.git/lost-found/other/6b874d512a6169e56875de8896ae72ca50462b5a', '/.git/lost-found/other/6bb4e0d4dd0ee5445099c82b2bd2f64a53e8d294', '/.git/lost-found/other/6c03949654187bb18a9d56abf3fa548d35436fac', '/.git/lost-found/other/6c5fc2bdd3439593a8643d755e206e6dfc9fc170', '/.git/lost-found/other/6c8a6bf7a8364e9f3c66b02e8af3048c191749db', '/.git/lost-found/other/6ca4f377708c5ecf6907a214a05573cc42b26244', '/.git/lost-found/other/6cabcbec99c44d58b07d21563b56e3e3ecc9cfe5', '/.git/lost-found/other/6d52ba52a8e301203cf321217bf466872849a86e', '/.git/lost-found/other/6df408815ccc8efcd933582508681c4b44e1d871', '/.git/lost-found/other/6e5315c52f4cb6f8f50c68116b2f12db8d110b4c', '/.git/lost-found/other/6f2516ff42249437779576cb418ec04cb76f8024', '/.git/lost-found/other/6f88ec227ecf2f7b141024b1d501544126a224f2', '/.git/lost-found/other/6fba22d4dc0eb6400d9414150d5b70602d6564bf', '/.git/lost-found/other/6fcf161c510c9b98c91a405a36236d1e7e6111f0', '/.git/lost-found/other/7053cc71e49faa648cb55ce0f0bf2b206c62ad69', '/.git/lost-found/other/7065f6674fe7a8235b352054611ce3983ec2b558', '/.git/lost-found/other/70adf55db7d632e16f7262dbf14637069fc748f0', '/.git/lost-found/other/70d153a9884e3f575ceee6df23bed28105af19ad', '/.git/lost-found/other/70f09f86714b5f1a6772acc9824b08e5148482f8', '/.git/lost-found/other/714397ace6f967f7f6c94a8446aad82e62242f3d', '/.git/lost-found/other/719a970b7bedabe76e51c19aef9d38a694ea8de8', '/.git/lost-found/other/721c0dd9c7733231be83aaabfd84464df8fb6044', '/.git/lost-found/other/728c2ace778aeceb83e85f1bcde65cb271b6a15a', '/.git/lost-found/other/72ebd6a7cfdb38fcc2e0b29564a3b301f7782e32', '/.git/lost-found/other/73fa97fd287d2dbdf544f5995bf4f80996e8dc14', '/.git/lost-found/other/7563c407d2437ca7e9fe67a0bdcfbe9439559381', '/.git/lost-found/other/757a9f890df07ca2d991d61cbaabe564c1e908eb', '/.git/lost-found/other/75e403200b7c6f1e192ff409078d9539db59d5f9', '/.git/lost-found/other/762405ef38fefcce716ce0ce148eeeb530e1e89a', '/.git/lost-found/other/769c1bb07714a82c3cd25c50f256f28519da231c', '/.git/lost-found/other/771d4dfee6367426c05c3d82559b5c866bf59ed8', '/.git/lost-found/other/77349909732fef77c64241e680e95994b7ab6894', '/.git/lost-found/other/776a4bea95d8e9f4deeb6e136104a5d9080dbf4b', '/.git/lost-found/other/777c96837cb78e1e50a9d82e0c0bf6c555dba8a3', '/.git/lost-found/other/77de4ba2f2aef9696037ea20f5e791ec8fc33796', '/.git/lost-found/other/77e3948ebbd8863edb49b35b86613591d4c3a2fc', '/.git/lost-found/other/782871526d2a991f40100b5e32cd3ef1fa465125', '/.git/lost-found/other/78dda83637c001a3bbb5b46fbed552151ed51365', '/.git/lost-found/other/790cbbdb4670edaa8647b93e6e6c5a9fc4aaac3a', '/.git/lost-found/other/7996e753f0d39ff8510fa714661f86e7b916a821', '/.git/lost-found/other/79ae734789ab6ce0d184cc720e51c101d3ee0f59', '/.git/lost-found/other/7a60567d3255257a8ec8ffd90b47253fbb7779e1', '/.git/lost-found/other/7a761a5bd14d2eb15e7fc3dfa4290f5d112ec66c', '/.git/lost-found/other/7aa8a776509d35c4b416ce478c310947105abb78', '/.git/lost-found/other/7b00b279b725540bd5e801557be40c425fec033e', '/.git/lost-found/other/7bed1a58912ef89bb40536ec81317ad4e857a3af', '/.git/lost-found/other/7c31bb200ac9ee3c8526031f3f462dcfbc0c6dcd', '/.git/lost-found/other/7c63e8f7e164de6eac3bf0e4c2c3b86a7006969d', '/.git/lost-found/other/7c6466d64311464b5cc235f012e7eefa7a3f7dec', '/.git/lost-found/other/7c7e207d982350b509a2ff479318fe62ed1103fd', '/.git/lost-found/other/7d1fa3cfc7a26b23468ef0231a6be425c10c39c0', '/.git/lost-found/other/7f1ccef0257eae07e1a9d96c9a419839eb69012b', '/.git/lost-found/other/7fbedd5325332884808b4f13376b20b608ba153d', '/.git/lost-found/other/80417b62ee231928cf6e1894ee78ae9d52dced8f', '/.git/lost-found/other/80525b0220584bb2859e90b7b1ecd96124809e0c', '/.git/lost-found/other/806c3e29a41d7902dc4bfb90b274f7bcdd692396', '/.git/lost-found/other/807fe9f45b577f7b4e832f53598c9132f4634217', '/.git/lost-found/other/80d57ddd52a3d347c46ca1ec7bd6611c3832991f', '/.git/lost-found/other/81b0c9d26060eac103e503fee24c4dc875d73a3d', '/.git/lost-found/other/81b84d2f9246fe95414efaf594ce0d66642af224', '/.git/lost-found/other/81c8e0c1332f8beac34dab5b2d8addd868c78d37', '/.git/lost-found/other/83f433e75ff687ed7ad6e622082b3771f4be902a', '/.git/lost-found/other/83fcd0a4b90b111dd78f24830b0cf0fd6f6662e5', '/.git/lost-found/other/8479528c7d38418a08b92817a5605425c6c65ea9', '/.git/lost-found/other/8507cc0d8827de0caf78209b1bc8b409c30929c3', '/.git/lost-found/other/852f59ef505774d2e1cded9189583af9a7fabfbe', '/.git/lost-found/other/8598ecf10a790316c773068fc621b1ec6a8c7462', '/.git/lost-found/other/85efd595e03f195168517e451a0f6351e2f9e69f', '/.git/lost-found/other/877dbd89e8209c09b4e6117d45aa1ffa5c29123a', '/.git/lost-found/other/87bdeed1fa7053bf3f3ee36c8996eb1a85ca4581', '/.git/lost-found/other/884ad461f9de46bba7b5fb8b37d1f4fb913b128f', '/.git/lost-found/other/88a12ae4891c84ce446aaf38698e7f684d05465d', '/.git/lost-found/other/88de5d8898855804a10e46a2b8ed2efdded56c2d', '/.git/lost-found/other/88ee53c9ece8ef43612f9db4cc25aa5614aa26ad', '/.git/lost-found/other/896dd57e7a94ddfe4430921fddcf78e252b7053e', '/.git/lost-found/other/8a2e1744f8d60b47acee31323eb9be5252f3bb71', '/.git/lost-found/other/8a5e5ad2e568b464c38258b18b07105fa93c8eeb', '/.git/lost-found/other/8b0fe43b479ecc9b599ccb21386dcf6243fab6ef', '/.git/lost-found/other/8badb259266160ed2ae90c6d544e84c1f16bdfa2', '/.git/lost-found/other/8bd53ac2f88091ca967b218668ddeb2b8b901b3b', '/.git/lost-found/other/8c532b7669a3fd0dc35dabdd43d2b34db2726089', '/.git/lost-found/other/8c7f0d1ecd32895777182562810997d842a1cc5a', '/.git/lost-found/other/8cdaba2214ca080e13141a212a14fa3492dee9a6', '/.git/lost-found/other/8dcf63db4819ce835831f19b7f843f66cf331057', '/.git/lost-found/other/8e147d7dafa9de53bdfdf1afdd2288c7015dab9b', '/.git/lost-found/other/8e1df140ffb6a1a2e0e1dbc48231a1341416d5ef', '/.git/lost-found/other/8e624b995ed2e8b2f8a1fde05616b92165f1b612', '/.git/lost-found/other/8e6e6dca3e2142e6450e31de9dcc15e1315d11d1', '/.git/lost-found/other/8e8cc43769b3e51927bb486257e5d2389bdfe3e7', '/.git/lost-found/other/8f29fcc619ffc635697fc2d2d468888819a7c05d', '/.git/lost-found/other/8f8a2153b54a03fb30f2d21c11b2fc65b5071796', '/.git/lost-found/other/903e19a32e203d03671b31f6e27ebaa907166d90', '/.git/lost-found/other/9040ad1040d2f81d6eba6d481dc29f2a5f5b2f73', '/.git/lost-found/other/9052c9897d84020cc14786b82536af8a94cad0e3', '/.git/lost-found/other/9124c4e8d7b6925e2de9f96ba7ee66e9cfbd5b4f', '/.git/lost-found/other/91364a90eb688a950083474549ee42e8e0eaf78f', '/.git/lost-found/other/91897ad77d725aab215d18fc41d34a68ad6b142b', '/.git/lost-found/other/91e214a28a493c3c2e35325fb7245d6983ea71ca', '/.git/lost-found/other/921a6caed41c95b6bba1e56724fe34b038245416', '/.git/lost-found/other/924d93052389d0b9434705bfe32ef317528044d9', '/.git/lost-found/other/92f0a102283a69d06abb892c5d78980a6a4d2652', '/.git/lost-found/other/932ab411aba0a979eb6a54f3c43832011843338f', '/.git/lost-found/other/9437d9d6ad6a559a5d535231870cc81d2e5f61e2', '/.git/lost-found/other/94ddb92592b2844dab2a6dbf6b54c3ec65c53adc', '/.git/lost-found/other/9596ea8c380e21e2936eebc4d43cc3da5c3945dc', '/.git/lost-found/other/95b3c141d6f33fa02247dc87531e793b05061531', '/.git/lost-found/other/960849ac9a576a80ffaaf0a558644a959e85d725', '/.git/lost-found/other/96947147a4afca1db6085e927b1a9a03d61ffd73', '/.git/lost-found/other/96f0c3a29711baf739f8d206549147833769309f', '/.git/lost-found/other/970b3536b39e69354428d28cb4461dc2b51077a4', '/.git/lost-found/other/979c845eeee9c7ea69e9be82ea0152129d99ab94', '/.git/lost-found/other/98330f2a74870e2eacf010a3dc6ebf02ba786210', '/.git/lost-found/other/98634d3201e655b428c3720dfc45a1deaf0fd370', '/.git/lost-found/other/98ddac6847239f0b68e04184b7c57cbffa12398f', '/.git/lost-found/other/98e1a00c29c13261193d33d35e8b870695aabfbc', '/.git/lost-found/other/9900a37055c69f4e8b8b84d6c679c7340cf21a2a', '/.git/lost-found/other/990b82d5c7737e7d79db4d7ee986945bee8c8b04', '/.git/lost-found/other/9964532f1952d9499823130c76cd62602dea68b4', '/.git/lost-found/other/99c369006665885b83433b1cada3e5998e5155b2', '/.git/lost-found/other/99d222d5d2d4742cfd70b247b8bceadd95fc4706', '/.git/lost-found/other/9a0d0a46f1f98aeebacd8915237221e8debc95fc', '/.git/lost-found/other/9abb4897f6f8e61f116f836df7fc815e683a5611', '/.git/lost-found/other/9ac9a25da69a69c9c6ecb565b8e855d3d39d4dd0', '/.git/lost-found/other/9ad7f9e4369acab40cfded3808876b7574f9390b', '/.git/lost-found/other/9b3627817278c3f1ea9f6f4fe2f8301d898b829c', '/.git/lost-found/other/9b4e06037e8da97ab1ce8591a052374860695c5f', '/.git/lost-found/other/9bf0e2c09edf77769e6856ecc475bb3bb86e45be', '/.git/lost-found/other/9c27c00a245e6db44d7f5dc05a9cda11bd241541', '/.git/lost-found/other/9c74f64ab7aa883b162a1b9a609b5647bf5cd115', '/.git/lost-found/other/9ca456f075c2c0aaebd5b2ee1a4529343cae45c7', '/.git/lost-found/other/9ce852637d31e71fc377559d79ac748027fea48e', '/.git/lost-found/other/9d3c14c4f7938219293f9b76798d587e36c29b99', '/.git/lost-found/other/9e7bd621f9a76c674f8c274753799ccaf07ab55a', '/.git/lost-found/other/9e7f02dc92c9bc10fba29f964c50c9f139a1f589', '/.git/lost-found/other/9ea482d56803dd81be7b63e60097e6171c004ce5', '/.git/lost-found/other/9ebd3ce8fe0e3f922060aacac32204ed38da03a8', '/.git/lost-found/other/9f2eec154f15568fdd976cb3ae4e296109e7642f', '/.git/lost-found/other/9fc8d58ef08ad56a92992a215cc0d76a5a8e94c9', '/.git/lost-found/other/a04ce92e7a6147503abde51c6d85c05f86763678', '/.git/lost-found/other/a0c6bdb727822d3ab28dd61c67b3b37832815978', '/.git/lost-found/other/a10ae35925626c8b16596f15a53aeab6a11ab5e5', '/.git/lost-found/other/a1ed013aa410ae8695f45a7019736ba3aa4fb275', '/.git/lost-found/other/a25b902ee65824da9fde90776f0ce686e07a4581', '/.git/lost-found/other/a2f2284bc6fa8fc3a142bcbc0414b14049c57475', '/.git/lost-found/other/a338a909318e642c29073226649ebc4667d40b25', '/.git/lost-found/other/a36298d1d7b41881fac3c262062753c14127c8a7', '/.git/lost-found/other/a3caec65273aae2d693f4bfa2ee2a2c3752c2ff6', '/.git/lost-found/other/a3ecb7025e3ede63635a7694860348298f2e6e77', '/.git/lost-found/other/a414fe1ef5a241eff31f88d267edb7378955ec3f', '/.git/lost-found/other/a4309913d0cf5df6e6ccc045ae0f19920001c3eb', '/.git/lost-found/other/a58d7bef5dcad55f29f6dd15f0fc3987e451d1f4', '/.git/lost-found/other/a59b9efc0a9636dce78f5c92fbac5d12d6da5647', '/.git/lost-found/other/a6091b6528df1b125c8e9a0fe31343e9b7e139eb', '/.git/lost-found/other/a60b71d615d71869dca5168f0a99487c02d7cf8d', '/.git/lost-found/other/a67d281fc3a06505d1f68688b8d19c1e7fd55d3c', '/.git/lost-found/other/a6a759f6ee5fe3e0998931bc1eb5f57b6d0a609e', '/.git/lost-found/other/a6bb3453ea72177cf803ae97da3ec7274f8bbe65', '/.git/lost-found/other/a6cc2e6efe55819439b2708bc7ef7d10a3dec179', '/.git/lost-found/other/a7417b0977cd4198ec223dbc7fe686683e6a56d7', '/.git/lost-found/other/a7b0ac4f7ba3b423ba8809cfca928693e9e1b555', '/.git/lost-found/other/a7f0b07ebde57e5af0354e2e76d73b8117ef9cd8', '/.git/lost-found/other/a8767737857edbde46d7c5760f644a3b145c4ec9', '/.git/lost-found/other/a907f6a155563583a84747b32b7897bc06d314d6', '/.git/lost-found/other/a93a02538f4107b5f0f6ba68d1e05106976618c7', '/.git/lost-found/other/a93f4d121ad5241432d6cece42ace11ef7d0d2dc', '/.git/lost-found/other/a9853bc470d2fd3c56ce24576650041dbddde66d', '/.git/lost-found/other/a9ab2c49d5af7d6df614bb0d578636ab64f181e7', '/.git/lost-found/other/aaceb0768852c7f4f7b7c086357a2b8319a67929', '/.git/lost-found/other/aad8d903158dca56e2301e3ac4a33d5c6765216f', '/.git/lost-found/other/ac48e387584c53d2cfd7867eb6983ca441277203', '/.git/lost-found/other/ad01876a896dd65578176da823c8d3eaf54a42cc', '/.git/lost-found/other/ad3b3036bc53b249ae74260b5df361c826ac41ab', '/.git/lost-found/other/ada35cdc23336af6d19f92c7bf023f84ef2c151f', '/.git/lost-found/other/ae67253d3690c041ae2f59e4d478510f04b183f5', '/.git/lost-found/other/af52068b4ddd08dafc65e05439cf72aa219d5e83', '/.git/lost-found/other/af9ff336b88c378508e3cd7eadd284d262242cc6', '/.git/lost-found/other/afa3bad6ecc1a686d44b7bf918da7c679e035577', '/.git/lost-found/other/afb28756840a3cd65e4389c4517d9216301057f4', '/.git/lost-found/other/b07a4b8db64b3990643478d8e05cc9b47efd6416', '/.git/lost-found/other/b11605b4c79cd6f830bc45162a5c28bc0dd0f013', '/.git/lost-found/other/b2913bc33fef9ceb13bae2b1c447cdc6fd1ae360', '/.git/lost-found/other/b2a71cf28f23bb8095e044f07a944b9ca46e36a5', '/.git/lost-found/other/b2f9faaf121213671fb5a7774e930d58f70151a4', '/.git/lost-found/other/b33fdbf692bc1bf33c45a12649e6d8805a7f12ec', '/.git/lost-found/other/b3e1f079730f15c805b6b1810f74a8950f7a5ee5', '/.git/lost-found/other/b40b773210056f26f750cfee0483ec7aa5a89590', '/.git/lost-found/other/b44c8d334c2720cedf3955e92d3a023f4d935c56', '/.git/lost-found/other/b52f477c7218624d8ec93a1acb97bc9bcfa8b9b0', '/.git/lost-found/other/b61fc9ec0d624a6fb5a3ee24de53e66839f36032', '/.git/lost-found/other/b7be51217a56e37c6e38cbbe732a0be92de0bc07', '/.git/lost-found/other/b817d6933884dd6c456522fa9c7215cbedbbc519', '/.git/lost-found/other/b8752d4fdff6b8b0ca56bc1b4d9697f1fa622767', '/.git/lost-found/other/b90b713046a8a15ec14fb0e8ac68bb50d20a22da', '/.git/lost-found/other/ba377d4c5675fe1b5496849fe1448ddee13cdf6d', '/.git/lost-found/other/bb53afb3ef890767ea09e0ec09cc8cf2f9d8b39c', '/.git/lost-found/other/bb920cc2a629754a612a360ab11e2e8a41929ffa', '/.git/lost-found/other/bbfa79a5aaac10800f659c1cf83de2b8f8f90d87', '/.git/lost-found/other/bc4e5bb47af0514e26b1fe0c3254b632c96c026c', '/.git/lost-found/other/bca71aa7a50f8e50f169ad8d7add475fcc88bae9', '/.git/lost-found/other/bcc4a536f944a78bc04830054c79a409585ee7a4', '/.git/lost-found/other/bcdda04baefba90a18ba44b74c2c6eaaddc5d028', '/.git/lost-found/other/bd2a1d030621759771ad4027c2a94150eac7a09f', '/.git/lost-found/other/bd9261ab35b09829e088a6da1aa076e98c524ead', '/.git/lost-found/other/bdbf5e7bd9efb4d363a7232fdec9cad6567d4cbb', '/.git/lost-found/other/be7d6b812f8433589a87bb6495b4dddbe12a0ee9', '/.git/lost-found/other/beb000038b4da9845ad1a638aade10236c7d7703', '/.git/lost-found/other/bef0994468110ae1fc1694af7188bcf5ca0918f1', '/.git/lost-found/other/bf29bfe9c49976b90984553d373029c8f53d8040', '/.git/lost-found/other/c03390e5b753aa22c85f2068144225856150c11c', '/.git/lost-found/other/c0577eb4a15bbf25fd3a5c58452d7f966970a69a', '/.git/lost-found/other/c194da9b62f88b61252dbfce48b0b5362f5e1a35', '/.git/lost-found/other/c198cf463656fd32c0cded88779f2e22d72c4c4d', '/.git/lost-found/other/c19bc78a96c49ef4677eea5af4526afe0617162a', '/.git/lost-found/other/c1d668567275777ab9130946e2e3a7195bb5920c', '/.git/lost-found/other/c1f6cc14efbc61641331679fb61606b1ae829c0f', '/.git/lost-found/other/c2a0ac42490e5986b165952d7702d65c06970ed2', '/.git/lost-found/other/c346cb932c8beb66f5dc30c662c2c41289d3598b', '/.git/lost-found/other/c3f599b00b12002d2a61a73ff0aa13d7524e832d', '/.git/lost-found/other/c415f7c2b19c281f1d670ac1c62606ef4ef79a2b', '/.git/lost-found/other/c4a684183d09535a773af72d1041476920339632', '/.git/lost-found/other/c4e7a00850f5045485ea31f07d406a573c62d04c', '/.git/lost-found/other/c4eb1dcec6f8749915f0f71285c5393955d98c6a', '/.git/lost-found/other/c52fe8f0592d844cbd901ce7bc44e0b1f11e64a7', '/.git/lost-found/other/c574d09175f0180319b6842ccfb2ede440e3a125', '/.git/lost-found/other/c5fdc494e96d7e2815ec1b92abd6cae192d0b95a', '/.git/lost-found/other/c63908d1df7973f503b327b3a48148ecb2a139a7', '/.git/lost-found/other/c68ffcfe5aef9991dd01696a443428d38a0c03a0', '/.git/lost-found/other/c6984ab03c0317af14fcb24630b38be6eca741bd', '/.git/lost-found/other/c6a161ff323e566d554ab18b7d4f58c2e3946d8e', '/.git/lost-found/other/c6a5564c6dd6cdd3429cd3326281f442e6c96cc1', '/.git/lost-found/other/c7a5ab9a45bc9a2e82c6cc9544c5b3c2d09abba8', '/.git/lost-found/other/c7afbe4ad776d0eaa7ec1e8b758d36a48572595d', '/.git/lost-found/other/c7f226c68b6c7fd47dc744bb8e0bdcfcd59110c3', '/.git/lost-found/other/c7fda2d48e4ec697b6ef93c8d41788cd050dd1c3', '/.git/lost-found/other/c829c60a45724554da4b097b17581af2e8a5216e', '/.git/lost-found/other/c8378ac3c120fd9b632b99b60e2700265d8f2195', '/.git/lost-found/other/ca0c53580589aaab2e623db4b1a3811974e04c03', '/.git/lost-found/other/cb68ee666c8f1f8773633ecd067416094eedab53', '/.git/lost-found/other/cb8d4858190a15278307f18d5ea943d1be41019c', '/.git/lost-found/other/cbe58ca7e55701aa03b44dfefd37ab577c6e2699', '/.git/lost-found/other/cd216e02b02ab615377718fc9d57a85fe3bed359', '/.git/lost-found/other/cdfd8467dc6ab25e4cb3c9fbad0356f018dd0263', '/.git/lost-found/other/ce0f148e5050d5462b9fa4a7218443611f540662', '/.git/lost-found/other/ce4226f7495b39011397a2f6a1352391068b55c0', '/.git/lost-found/other/ce57928fd558f7fbc027f3aafbcc951a0a5ff7d8', '/.git/lost-found/other/ce8b9095bbe8c455e3a083d1d2bf00fc3f95b68f', '/.git/lost-found/other/ceaf0b0c7041d998228f7cc55d506013d4e2660f', '/.git/lost-found/other/cf21155b406ffe5d1ec58b2bfb3280f9adc9d734', '/.git/lost-found/other/cf589f7e7cd10bc0893d142bf2b1787bd13a98a9', '/.git/lost-found/other/cf9d67c816b6afce8b699b4509d0482602be5a42', '/.git/lost-found/other/cff0d14042e370123492e5b41e77144ae2b6a234', '/.git/lost-found/other/d04428fc4d2377186583fd4be601a67be5de3ae2', '/.git/lost-found/other/d06cdb63841efd6f9d57da0a49d556d1e0193d21', '/.git/lost-found/other/d0fcc1e31590864b6d8ff451e2fdb118673f4f27', '/.git/lost-found/other/d11859d8b7f96cecfa199c1d97d294e7edb9b643', '/.git/lost-found/other/d16351fb26ba3350c0a7cbe33983581748916efe', '/.git/lost-found/other/d1924c37cf129b3171b889e6d0595a74de2dddce', '/.git/lost-found/other/d196bd9551e1cb5459af29b2dd471c413a752b2c', '/.git/lost-found/other/d1c237bf893070207c137c6b4c8692712bfdd8ff', '/.git/lost-found/other/d21237aa1e63fd7757ca66048f14e65990c070a2', '/.git/lost-found/other/d2453b4648cfb34f34b9758f6146f469b0a57607', '/.git/lost-found/other/d2b4354cce6142de4373869d6869d8d3fc5384dd', '/.git/lost-found/other/d3584209a11765fd9897e316865f6378b924fb08', '/.git/lost-found/other/d3701779a329a7ad2f0c33373d48687b0325a176', '/.git/lost-found/other/d5d57e5acef03490f3e11000082c513a6947397a', '/.git/lost-found/other/d5fe79282acedc0c62e6f1f058c20fec777f0753', '/.git/lost-found/other/d69e4e4828e0e860c901c27d846fdd2695d13a7b', '/.git/lost-found/other/d6a97a089030a7edd8b329c8ae905eda7d8cb77d', '/.git/lost-found/other/d6db780d0f4b775d5c38a76758fbd072c433fc5b', '/.git/lost-found/other/d6ec37f282939964e41bf2de2675c39731b21cf8', '/.git/lost-found/other/d6f6b42a5113049affff24f3057a16240e5b761e', '/.git/lost-found/other/d767ea26e44c64d7e9b3803c0fe5b09b0172b5eb', '/.git/lost-found/other/d77b3a691e389d0ab088e72c10008c645344b08c', '/.git/lost-found/other/d80cd503dfa13d070109f2dab443f74be8f41ab2', '/.git/lost-found/other/d856d9cd9646a8c8567ee9af9551b2e43eb2b2b9', '/.git/lost-found/other/d91fea1942d87936873c4497ea5f8398dbbd1259', '/.git/lost-found/other/d95654384b6318ecb9abec998e2c64599769f652', '/.git/lost-found/other/d9e204dc5438684c55642ac4c4f5edb79aac85b0', '/.git/lost-found/other/da122377427fb4592c6703f54c9850535bb57e00', '/.git/lost-found/other/da129bba6bb8d62d9de2da9a239c1cb59e1a06bf', '/.git/lost-found/other/db1d00fcc5c8d09c5303493b6802f45e19162edc', '/.git/lost-found/other/dbda401cd34b991d08fe06946884135f0eeaaec6', '/.git/lost-found/other/dcac869fe6630d02093d2d6d4d423c3abfc5414f', '/.git/lost-found/other/dd13313f0b99c3e5722ba2f169ec1630d4090956', '/.git/lost-found/other/dd9df54fb86de4a812d2d5c14f9d5d302eb0a895', '/.git/lost-found/other/df212e1724e830f02c6f7c48baa386937ef8a8e4', '/.git/lost-found/other/dfd989fa24c652eda8b3caacf8465401d8a15fe1', '/.git/lost-found/other/dfed33fa2c962d9b941e06eb1904add340c5c1a6', '/.git/lost-found/other/e043fdbdecb337c2509db1da715bc608c7e5c457', '/.git/lost-found/other/e05eb2e28b2f121792aecb7cc2c9d3835a99f45d', '/.git/lost-found/other/e0c9d873acdde10922f8b3fe006a65790cf1d033', '/.git/lost-found/other/e0d3f4acaad9831a78cde41b9465650d8ac882c0', '/.git/lost-found/other/e17608611f7ca0f1bc68ff088dff1d0b226934ef', '/.git/lost-found/other/e1af2f444391dc6bed835532f09731b5f9991ea4', '/.git/lost-found/other/e2391518db03b590ccce8e1cbd97c243d3495201', '/.git/lost-found/other/e25b83ade139fd5d022aeba14351f302855bc80c', '/.git/lost-found/other/e2c5ecab8eb12e570a291601bacaf7b9d74279fa', '/.git/lost-found/other/e2ff6027c01c11460a38172570e89c9eaf403cc7', '/.git/lost-found/other/e31315b59db6da959c44aae02afdea6a956d6749', '/.git/lost-found/other/e3362e7b28e5bc000858f79e7808bca8378d65c3', '/.git/lost-found/other/e3dd33d57725ad5c51131c5a4ff2a6baa90a7bff', '/.git/lost-found/other/e418f732044b83b44c55a3d8bcdce822dda2d201', '/.git/lost-found/other/e44f18e830600f291259dd01272612bfa620c51b', '/.git/lost-found/other/e49b0ca82b56b90bebb8278e7399bca8a0664fcb', '/.git/lost-found/other/e503ca98487014da5da23cb42963fc8f1ba24da0', '/.git/lost-found/other/e520acb374bf8c6935bc34fa047d318e675611e9', '/.git/lost-found/other/e5a46d4f237e3ab7c53f212cb9b976ea970e1344', '/.git/lost-found/other/e5d997d2e7d0dfa63294bb5eb482acc1e88f8980', '/.git/lost-found/other/e674b96ab8e8f0f47f0a21b11a6aab353fd952ad', '/.git/lost-found/other/e780940b9beb3aa95c0e8141615546cc43e3beb2', '/.git/lost-found/other/e82ce186470aab5d29d55e09ed28c972a6631138', '/.git/lost-found/other/e8602005a19d6eee72b7e70d9ac70f5da48bc0f8', '/.git/lost-found/other/e88fed00aaa2ce25272c7f42ea7f6aa0216dbd2a', '/.git/lost-found/other/e988e0b91b3e936c0b22dc2471b12b685e7a32d4', '/.git/lost-found/other/e98a51c0a5e69d042a9a6831d845e3f47b6f877b', '/.git/lost-found/other/e9b1d8f0265d0958e8a5b4a6e8c822f1703e561b', '/.git/lost-found/other/e9e3231e30ffc553ddbfc6f85432deba73d86ba7', '/.git/lost-found/other/ea0d0f9b7b627a6646f6d51864ff418f34902679', '/.git/lost-found/other/eb014d2e1a941a9af381c2744eace9fb4eee73cf', '/.git/lost-found/other/eb19f3b0cff3fca757d4ca80219f4ae1fe43e6e3', '/.git/lost-found/other/eb9cbadf8efbb1fc517fa7295d03720da31509d2', '/.git/lost-found/other/eba33a9bd67e3209a6c680d5018f3a68c9a1efe0', '/.git/lost-found/other/ebceda64425af0c067023a8307110a93375ffd45', '/.git/lost-found/other/ebe2ec685146f680a315f128c349c1dbf90adb00', '/.git/lost-found/other/eccd1e176da943989ae2606c2b88b88a9fc437b9', '/.git/lost-found/other/ece03b567137bf1de7f0e8bf9c5a4966a5713149', '/.git/lost-found/other/ed6fea00087480c1025065a44af8ebd9d7579ceb', '/.git/lost-found/other/ed87c4d1b13d5253f80f8e338600741e25e76691', '/.git/lost-found/other/edd4de5068941df19e47f2c46ba92c179e006fc1', '/.git/lost-found/other/edecb464de5a85816f1a834eabb5a70fda930567', '/.git/lost-found/other/eec85fbed6da5a379fb1231e3cdd297457f45913', '/.git/lost-found/other/eef1dbc15dfd6b66e0695323ee6b6a27d8c8d620', '/.git/lost-found/other/ef2ed056c509290708f0af3df007e352c215f659', '/.git/lost-found/other/ef417fe36253d71abb1df1c24cb00c029f36c191', '/.git/lost-found/other/efc42a741226285057099f826136a954c9f60f10', '/.git/lost-found/other/eff77e32c35f9ef44aabbcab2d36737b118026bd', '/.git/lost-found/other/f06da463f9b4911fb844b3fdf989eb2e4b65229c', '/.git/lost-found/other/f09d1df8015f8bb959b34440b1dd8b37cfb11008', '/.git/lost-found/other/f0bd3f073c0d35a30be9e8db6196f98c10bc36e8', '/.git/lost-found/other/f0d1fee8f3aa5faee3a47eff72cb5f72b64144b8', '/.git/lost-found/other/f0f15c5214e9b65a671bf8c8a746fd62bd3bbb04', '/.git/lost-found/other/f157b9093d30086676020a187f11fac6aa511ac4', '/.git/lost-found/other/f1d80bcd5b7b96a9d8b84da0aa1e0456f8b81c80', '/.git/lost-found/other/f22f4f45cf11ce898f3bb59999bcfb92bcf27878', '/.git/lost-found/other/f2667bb108c5556bddb66621a82124d94e57ffa2', '/.git/lost-found/other/f2a49c9f94a304cbdd8c63e63618f514dd430fdf', '/.git/lost-found/other/f3a1936aa92f749281b00a97f46c85c0f3faeb3d', '/.git/lost-found/other/f42b592f53441bc52a46117d0dd396eb602408a7', '/.git/lost-found/other/f4434f6a34c53588be267f04ba5c83f53c63bcf0', '/.git/lost-found/other/f44a8e423549bc7bdb6a49e232c498f4f4ac1fbf', '/.git/lost-found/other/f6eee227d2cffdc9cd3c598fdd731988f75dab78', '/.git/lost-found/other/f74174bc51b61272e8d1106c065feeb9270bb198', '/.git/lost-found/other/f79731037b392d638382b00776eb115ad82d5a10', '/.git/lost-found/other/f798ab67c883b2c2437da785757dd4acc8ec2802', '/.git/lost-found/other/f7ae7eebd292d07443f6b71fcf69a4d58e600dcf', '/.git/lost-found/other/f7e04c7b89185faa008005238823e991d473d6b9', '/.git/lost-found/other/f809cda2ab8e302b1f5d8d456bc48517331888fa', '/.git/lost-found/other/f83d5ab03367fb5642286c45e104911a5f07b3d7', '/.git/lost-found/other/f8e82125cb443505eecb0d55785a053fdca7692e', '/.git/lost-found/other/f8f69ff5df79ea2afc60bcd584898e85d69dbe70', '/.git/lost-found/other/f9e6c91fc25475e54f13be5d3b540a079341fc2b', '/.git/lost-found/other/fa6978edc179dd7f5080701f86e4b87dba737809', '/.git/lost-found/other/fa71d85dac9e3a9dcafb1eddff0a06d6a1f8d89e', '/.git/lost-found/other/fad5f2c59e6ac92d7d2c2bbda552b8bbaff05be0', '/.git/lost-found/other/fb26b03b1c71350bb0cad1dfdf58d62963cc8c83', '/.git/lost-found/other/fb374affc79708bc948a360c508e21faaab4ebb9', '/.git/lost-found/other/fb69ef7c7afa41527b8ea058d3a983d41b9a6b39', '/.git/lost-found/other/fba48324fd82a30093cb9276fb462866dca04776', '/.git/lost-found/other/fbd5050d803a8bc8ede5dc38f21b85f0d6340f20', '/.git/lost-found/other/fc2ab51db9df28d1cea1ad609b1f6a4be02876d9', '/.git/lost-found/other/fc6e8d45ae5418dae578e0a5cc014fe2cef7d73f', '/.git/lost-found/other/fcc1871fd0b91f9512edff43cb9f9c6d93381ab1', '/.git/lost-found/other/fd209fbb5c2ecd03c306b65055023886d98a12fb', '/.git/lost-found/other/fd618bcb1a6d81feccfa30bda3c1ec83f6c99da9', '/.git/lost-found/other/fd7391d5c0e8395ad01076f9710de2fd352e0f91', '/.git/lost-found/other/fd7996fc223885596b22d096f1c130f9ecca483a', '/.git/lost-found/other/fdc7410fe2c49ac323b138a6420b1573d24b0e87', '/.git/lost-found/other/fdee2ee54a319f9fe963492c028efea79eca32cd', '/.git/lost-found/other/fe7bb38beba7a69323458420123e865a56856a48', '/.git/lost-found/other/fe7cebff670146550df068f2f90bd7399ac8739d', '/.git/lost-found/other/ffbdb38129ee775fef20071909e5ff669e40abf4', '/.git/lost-found/other/ffe72238f13a07462b349f317290814b1d8a21d5', '/.git/objects/00/025daef50b48b9a7c3aa0957f67692b7cf9644', '/.git/objects/00/279ba916b80ee7f054dcfe4bcad5fdf3d0cad4', '/.git/objects/00/3f638d5dfb6119d2afb8b61df9a388a70c6ca9', '/.git/objects/00/5291f4fcabd5eeb99dea4a438422225f9104fc', '/.git/objects/00/646ef1f6f7efeaeb3e5c6a38e238fa5728b8e7', '/.git/objects/00/6f8e8695b0a66ae47eb9f76ad1bc0e7b0f036d', '/.git/objects/00/9107e59a300c960ee6ec2a0fd55630b53e6a77', '/.git/objects/00/a92ed33a5c9c699f84cf5e7ac486d7789874d9', '/.git/objects/00/bb4eb3c57678c53ecdb996159c28d816ca8abe', '/.git/objects/00/bf2ee6092a4428c1c240774794e6c695ff4722', '/.git/objects/01/03d9023b3c0be99b13d162789304c2695289b2', '/.git/objects/01/08acc654101c39e74de3cb6404c4fa80bc7bad', '/.git/objects/01/10b4b49800261c96b2f11847c83fdd04e60b20', '/.git/objects/01/4d2f0fd6dffe4835f741728459499991b22962', '/.git/objects/01/5abae91e08022c92cb6c24e1e1097ec60a9c6b', '/.git/objects/01/6411d1645d062bd7d4c9bee134bd6d3b398669', '/.git/objects/01/72babe377620bb36cde7d6318983b28943f5e9', '/.git/objects/01/7b31bf525f3b189f3119394c79bb4284fddfb0', '/.git/objects/01/81bd6955aab80579d81db279fbd9cf97044fca', '/.git/objects/01/89548f4f27fcb26840150f585a64515d77c26d', '/.git/objects/01/92dc92789e642707957b713071f72a8450b714', '/.git/objects/01/a6c42d3a8669c2cbce5eddad00f286522be614', '/.git/objects/01/bd8bbf0fc579feada35ebba3beadd61b3fa934', '/.git/objects/01/d9bb05d576e6db8b5775d37cbac01368f4fb94', '/.git/objects/01/f4c581d56f69b4e25af1f5ebc05ebec603c3f7', '/.git/objects/01/f88f8377947a49ec1cfa7a9b32b89b69dbef4b', '/.git/objects/02/1d956a833b156e5835bb90f20f2fb257686999', '/.git/objects/02/4337837f4b10ca80598d1b777c7ddb3382a7db', '/.git/objects/02/4da679e39764f8e2a1862074bc7d3a67b39a2e', '/.git/objects/02/54144a053e6691f5da797289b3815221e244ee', '/.git/objects/02/6d0d210de6d3b148a6616c9a49368f14c09c7f', '/.git/objects/02/7cd9077d41da5280567175993abb09c6e81add', '/.git/objects/02/7e36728d1dcc8ff7c167c7c719f406b537c61f', '/.git/objects/02/97c9b7194e6e16e58b7fad80617595ec60797a', '/.git/objects/02/9f3344bdabc6fa51d3a3317b8344c9d12fda27', '/.git/objects/02/b6d0803b43000eff745e76727f7a0785cfb736', '/.git/objects/02/c139017e618c759476e436e3fb5fea75a042b4', '/.git/objects/02/e3706e34f211187bd64efa7a9ad51760195d39', '/.git/objects/02/e65c5fa5fe4ad6dc61f0cdbe002e7fa451d072', '/.git/objects/03/098a8322f9458ba797697f7cfdf272e30f91a7', '/.git/objects/03/09d7c803accd0e64d899fd8e0cfb1098a815d6', '/.git/objects/03/12d61983ef80179bfac79abbba1359052f115c', '/.git/objects/03/21b0ebc8efdee894f75380930206da9f16ece5', '/.git/objects/03/21cc3ec2443f4d85700dfe3f808368fbed568b', '/.git/objects/03/46900bf395f5f0160d317d392abb7aa026c7a3', '/.git/objects/03/56133446ed7dfa697229a2b5c19f243e35f443', '/.git/objects/03/7233cb441e842bfda192053568fe3488f544f4', '/.git/objects/03/7e5e882489a7413c4a62c63d0617b5931284f5', '/.git/objects/03/992f453ea274349984b8262b02650fd1b8bca9', '/.git/objects/03/9efba89af1d0d8bc7aae3c352c34e0c51701af', '/.git/objects/03/c02ba7211ba7f8588931520e8be278972d8269', '/.git/objects/03/c3557176983f991148ff39a6afd493bdf711df', '/.git/objects/03/cdbdebe4e5bc4b0f7a70e153e8be75dafe3324', '/.git/objects/03/d1d893b164cdfc9957a88495c3449fc4538ccb', '/.git/objects/03/f10215da3a690e8f4a1155755ae2b506c5f1b6', '/.git/objects/03/f8520645287e09c8ad96bea9bcb878a9022206', '/.git/objects/04/099990dadacd5c2f9cac501abf5448595db03f', '/.git/objects/04/0be927181b9604d69593ffe36ab7303b1a94bc', '/.git/objects/04/0e0ff5a310da50070b4caaa390e93cc8c45ee2', '/.git/objects/04/29ceebd0dfc380db49c94ca9da53cf3d0c76c1', '/.git/objects/04/2e02d97cc4abc6a96b55d97f34fc76924c9cf9', '/.git/objects/04/378a998f4a8686eb28f62e8833b0f539229714', '/.git/objects/04/42d29efa0ea05d53ea9a8c2b6f9d4d76a65123', '/.git/objects/04/4e235175ddef6dd6b9a05edbd34b9ab69cbbd3', '/.git/objects/04/4ea84e87f27f536235093b99f1e70ff6b0d79a', '/.git/objects/04/5a95c2c2c83fbdc5489e26541666beca91b0c7', '/.git/objects/04/602fa9e7507060764d8177b9fbeea82b94a77a', '/.git/objects/04/6ec8df046968b6bd4058a151de39c720533f28', '/.git/objects/04/74599cf24230b2e6acf617ed53f19eaac1d8b9', '/.git/objects/04/754e0dd161f613e2726da459e85cfbfc1edd59', '/.git/objects/04/771a2ae371a6d614730f8a857a8b401fa5049d', '/.git/objects/04/78eb80cc9a8041214bf273295064af3ab7f7d7', '/.git/objects/04/7fd372aaadd7a538f968712fdbd0e0e9c86415', '/.git/objects/04/80586953887e797aaabcce4f0226ecccea02bd', '/.git/objects/04/8703100e2e6ea370d2f3a44c68c56f5a7c3809', '/.git/objects/04/88481d528674a76807703e6625d6284ca8293e', '/.git/objects/04/89842c6d2c5ddbc9550902039e9b25701d08db', '/.git/objects/04/8f509ce5eadba0a89792ec7f9a5691cecb00b5', '/.git/objects/04/921744c623863c7465f82f0d1af98ebc5ecffa', '/.git/objects/04/99e3e328e479da772baf0797e2fa34d5146993', '/.git/objects/04/9cf58812f1ec14cd7c43edc82532b64bab5b4c', '/.git/objects/04/ba7faa5aee31cca7feb4058574f06ec3a9b645', '/.git/objects/04/bf8e699f88900a6960b666079dba19a77ee7eb', '/.git/objects/04/d557d3b8c74f15dc8b1039d196b50cb8924950', '/.git/objects/04/eb348b50f737e9cc9538859b97f4516e2a0d83', '/.git/objects/04/fc92e910c95c87a567fba0d8e4566649816c3f', '/.git/objects/05/04a514448e0c3c3e4f771ffc84479295824920', '/.git/objects/05/09e635b91d457d88001ca19f7deb59d571fc46', '/.git/objects/05/0b372c851b0ea84569f8654c65fbc6c371b718', '/.git/objects/05/16754f01d0be542a9cfc9c1543fc07b1724272', '/.git/objects/05/429119c92c1ee2c4044621244195ae8bc33e03', '/.git/objects/05/58ff9439de64e491ee9c3bd2097b5b118029b6', '/.git/objects/05/6e214d9916a67615b4d789712bca658fa03435', '/.git/objects/05/7e875a11a7c4cecb41ec844c73cc2eed23c8da', '/.git/objects/05/829e3696de2908b0d40f37f6c20fa8fff8a1c2', '/.git/objects/05/880b7872ddc08ae82b821f1b3abd5c3e5341a3', '/.git/objects/05/91ddc9768f4c685c5053ca3185eb6a633a3717', '/.git/objects/05/a402c383746da97299cc12b9c33d5a2274fcd1', '/.git/objects/05/ae7f245bb7130dc464d00b710cce251cb7bc91', '/.git/objects/05/bc40edd4cc79dbed5bfe63bd8e89ac3473040e', '/.git/objects/05/c6b2e9fcb5f3627d99b0e8d1a5dcbd34652369', '/.git/objects/05/dcaaad2921ef5e63bdab6f62ab24662b8634bb', '/.git/objects/05/e380ae2c1225a808d176cf011b00fee393cbaf', '/.git/objects/06/0b348f7160e9612f996a74560ee786364ec5fe', '/.git/objects/06/121995b0950d829e4f685adf8bef846269580f', '/.git/objects/06/2ba3dc08a841ecebcec4c5c7c0efa5068edf7e', '/.git/objects/06/31461eea8e5edd79ac1ce1e27740fa7c4659ea', '/.git/objects/06/3554b9d4f0504b72bcaf1ed91888688b8df1bc', '/.git/objects/06/3b0eb2461a6c575fabd0087334058e3e7d387d', '/.git/objects/06/418747a855c7847e27bfe23508610c20a60493', '/.git/objects/06/440e122972eb6c98407112d4abcd39c31e9321', '/.git/objects/06/4b36eebdc18055d9b9efab453b240dfd5f9421', '/.git/objects/06/4efa3154548faf37f72f6e16da0f94681fa86a', '/.git/objects/06/839a7dad1e830ff2ba4cc5228781681333e75b', '/.git/objects/06/a8e8ac333fed73af47212fe4626cbaa3b74e82', '/.git/objects/06/b4fa32525254b94d62c83a59084454f8f705fb', '/.git/objects/06/c43ec225095ee1df544729b8b8fec79c0fea0d', '/.git/objects/07/1acfc4227f2b22c838b0a56a59509105e4c2df', '/.git/objects/07/2872ca40aa53c5fcb11aa9a7edd5041033fa64', '/.git/objects/07/2de9a5fdb1ef44cd0b059e266bcf024ebf4697', '/.git/objects/07/358e5fb83f8aa10e322bdff64aa40398232a59', '/.git/objects/07/4930d053a799cc4f9095e89196437f704205d6', '/.git/objects/07/50d849bd563021aa1b9de4dc745fa43bc77e6e', '/.git/objects/07/522cfeed14b2118b137544acb215fd0d23a276', '/.git/objects/07/668e6b5dbd6277a6a85728db272e0b820a459e', '/.git/objects/07/7efc9c2f36f39adeeed1ec668a0970efbf4921', '/.git/objects/07/8adb64a12dcb95981db04caf7568546f5a88b6', '/.git/objects/07/91e2c492831faaf144a90e6af25adaabad38fa', '/.git/objects/07/997cbc1661d4546af788172b66486e4dbaefdf', '/.git/objects/07/c5d56f1363e06e73172965496ce16246dce1f2', '/.git/objects/07/ce7e8216ecdc557e1f1ec524242dd409b4067c', '/.git/objects/07/d150470e12425cb0b2d6a1cd55cd35ff2ff2fb', '/.git/objects/07/d79d89a08562d80d6890844f66241e32b443ba', '/.git/objects/07/d7cf37d2c1b6f4ce851dd47a314f66d89038d7', '/.git/objects/07/ebcf391bfe46a07fd685402467db2e86ed4e0d', '/.git/objects/07/fcb01a9b6e469e5b52f9ac3ab3bbe83a63d95f', '/.git/objects/08/2169d84ac7751152d7134fa37292c00ba029d0', '/.git/objects/08/3a576c7606386c1daaca88824c281693d0ef0f', '/.git/objects/08/42d15769f312e00dbce38c79a209d783d115ea', '/.git/objects/08/46bd8dbb22deb503b2ec4512fb7a7c354cecdf', '/.git/objects/08/4d44439e48fbd75cbc5ae0b0132693e7d839b8', '/.git/objects/08/749be2799a1a1f0697ed2571a4682426ea12ff', '/.git/objects/08/7809de3bad36c3f85c48e62edb51c147e48b77', '/.git/objects/08/7d31d51dfb5a1137d4f25be244cc284a37a076', '/.git/objects/08/9cb3c61a7acbf2a05ce9d4926088affe4663a1', '/.git/objects/08/ba0a8ee50af5b8ff5eb0a82d30bb5229fe2e86', '/.git/objects/08/cd05987a9baa7c8e5f6caa20e79a8a63d3d0d4', '/.git/objects/08/d2a116f15f569082d9e41973dd7e570d5b17d0', '/.git/objects/08/f07511d3e089cb96e804567644ce5381392e51', '/.git/objects/09/04682cc174ebeaaf2e9f366af211a401fbbd99', '/.git/objects/09/0826b708d0c9dcaddbfe121559c5b1486529f8', '/.git/objects/09/1739e89e6bfb98fd5f431dcd801487dba344cd', '/.git/objects/09/25e45208545d1857f69551356dcb6ec82edda1', '/.git/objects/09/2a3dcb3669da7adc41965ed57e1fe8cb86f429', '/.git/objects/09/384094c714fa3c73aeab22ac4fd18d06e8dbf8', '/.git/objects/09/3d21dba99b105a0e82051ab2639b5151325793', '/.git/objects/09/45bee1723c5de6847e799c08785083db839a6c', '/.git/objects/09/46862f3f15d72c8b71d2af4522b4921f6cab96', '/.git/objects/09/4ded1d397e3e5a80c619217287287fb729622c', '/.git/objects/09/4e04d13c87f5a327a7f44ffedc0ce41d9214d0', '/.git/objects/09/8b34de8f71069fae9082ecd1903b6faedce4e6', '/.git/objects/09/916958db8eaa97c465c9bec51a3d1a29863ab8', '/.git/objects/09/b3cd47a8afc2c0c4de3af709b99566a5bf6f37', '/.git/objects/09/d354f2506d543f99742b506f1c5e20b41d2691', '/.git/objects/0a/05a2808a79fe98d007bccb3b1060551300dec8', '/.git/objects/0a/0c8795605b604d1e687339be45eb17e8812bb5', '/.git/objects/0a/2311bad25eea12e3670b5f0c36155e5890d27e', '/.git/objects/0a/32a69a6ec6e5576956ee853c47b27b8d6861b4', '/.git/objects/0a/401b78dafa49a27a46f59d3faf54b63b65c257', '/.git/objects/0a/56b7d89f4104d6a12b42d8b6f4179bc0939089', '/.git/objects/0a/597e37cfb13fe9af1875fc0606d2f7cc0e7ada', '/.git/objects/0a/59bca84a5ae11bd02571a6bf55d97bbeeda3d6', '/.git/objects/0a/5abee36b52e3cd5aff769a0108ab1a3ca51a82', '/.git/objects/0a/613832d0a99485a26bdc2a2a347669c76d3ef1', '/.git/objects/0a/8b1aeacb86cb7efa0c8582e6f109cd1ba8c46a', '/.git/objects/0a/962ce910aa746587b34755922bae542449fba9', '/.git/objects/0a/9c45c7913ebf7c65a190c9b4623116c5083db1', '/.git/objects/0a/a39c684754ee62dfc0ef9866f409e95d192bb7', '/.git/objects/0a/a4f3386b7abde99d77a8a42c0e0c9a6e0c4514', '/.git/objects/0a/bc810e4c97279e80fa5610d8d2838b94e3bb03', '/.git/objects/0a/cc9185dc5580459d7b19eaf9bc4561109d5cbb', '/.git/objects/0a/d395ba510ce17075f27e7d6f4920547464887a', '/.git/objects/0a/e25708036bf7db64f0327ea004917ad42ea679', '/.git/objects/0a/f7b1d6071a1948ae9d76d28fbb7c496bea8020', '/.git/objects/0b/32a64183ea4ed4f45d547d0d69c6efd03e6bd2', '/.git/objects/0b/4829e05344126422455e538c3f872330bac02b', '/.git/objects/0b/4ba29f97f87d85705e1dbacdbd901e825ab2a4', '/.git/objects/0b/5c093d67b5443b9efe596880b950fe478e93c9', '/.git/objects/0b/5d3ac18d6fbd99afb581479554b58fc4183e02', '/.git/objects/0b/5ddb6e3cc1e790ce56a4a35da6e1aca2720e47', '/.git/objects/0b/94a8d00ef25b126437e3b831d3c47331ec09ef', '/.git/objects/0b/9c1ff14d0729b8ca054bf3b70a31ed6ea3724f', '/.git/objects/0b/aa622887f5563517e122f9b16213710af9e5cb', '/.git/objects/0b/bcef51f80d0155f83a276423028a01a50cd92e', '/.git/objects/0b/be894f6158df6217aac34e5062d723091507dd', '/.git/objects/0b/c26acc5a1d060a7a7085eab6ce811422715108', '/.git/objects/0b/c5e541ab7db8fea9b58b2c13fd46b00959dfb5', '/.git/objects/0b/d9338bbd511117b1f70cc1e59c6bd691580e94', '/.git/objects/0b/ebe41378726eb546288bbf7d2eab84189d6ed7', '/.git/objects/0b/eeb928e68e50f79b601ffeb2721e89a635ed95', '/.git/objects/0b/f720f21f41ce829add4aab5a9a05012208c3f7', '/.git/objects/0b/fb909231e10a90dcfd4ca08fc34ad154b9686a', '/.git/objects/0c/00cb9ca737f2be5b9cff166bcef532262ec699', '/.git/objects/0c/03f3f202ea13e8d79942013dd4334cc5e7ebea', '/.git/objects/0c/0bdbfa2459da2f07c4ab0c874834200ff6278e', '/.git/objects/0c/3e4d5d6ea3196693b9472f7d8b823513fa235a', '/.git/objects/0c/4b8aeb5e5749bec419baf06069759fc045bb72', '/.git/objects/0c/60a48fe702d1f4eb0d7dc24a73a35b850c8eb1', '/.git/objects/0c/614b8e0f3afd25e895d9491c2a30e5913af606', '/.git/objects/0c/6358b6057a1b224be62ad80a00d87614631b60', '/.git/objects/0c/64a4d48bda41945b4888b51a9e960d8fbfcf0f', '/.git/objects/0c/81eca4c8d2b7bf0a503cdacdfdc66ed1715c2a', '/.git/objects/0c/9d4a1d27f542f5c5fdf5684e73c718676e06a7', '/.git/objects/0c/a878bc7c1f09046bb15719383794b9ecba57f8', '/.git/objects/0c/b3be9041c3eaf49139e8d49ef95f361352c397', '/.git/objects/0c/c5b534f4425eeb8b3f6bb9a32803cb055d7ff3', '/.git/objects/0c/c625939a9cc324e29d3b2de079d11735728b58', '/.git/objects/0c/d0ce18b1d6a46a554b87e2dc0bd115429eb484', '/.git/objects/0c/e0b926ac0c36b6e353c377ebc74e59bc0561c0', '/.git/objects/0c/e65ae661206b963a23be69dbcc77c2bfdba45a', '/.git/objects/0c/f07378ed3afd105c193d8b1b209dfec5785402', '/.git/objects/0c/f6c89b58f55c9aaff91eca9869cd2c17c0a47f', '/.git/objects/0c/fed93b45cb80e866637f3e266fde5459ea49fb', '/.git/objects/0d/15ae1524fab34c31c9c1ed0bb3e65a55951524', '/.git/objects/0d/195c3ade96d5880482daa65889a072069468be', '/.git/objects/0d/315a864dbeb1ff8b62f267f614e3fb239b3518', '/.git/objects/0d/3b08adf9c7ed270b6d5889540ad4437d5f0b98', '/.git/objects/0d/453df5063969c6130eb9ab5f086b45b2321f9f', '/.git/objects/0d/5256345daf7cbdefa3bc826d1e64513a214cf8', '/.git/objects/0d/5d4ed9115a075bdb83c3da8e5d5d95bfebf06a', '/.git/objects/0d/72d0b2349a404cc4cddb87c836194765377d74', '/.git/objects/0d/753acfba917272cd72f418e9c1352ed20054f6', '/.git/objects/0d/8883bb012284d6c3c617deaf7758946852971f', '/.git/objects/0d/97da9f70aa97244bea12a6d8024c006575e5c8', '/.git/objects/0d/bcae139c196ceada45a4720daaf5908702ecc7', '/.git/objects/0d/c7d460490f110521abbce48d8939e546425dc5', '/.git/objects/0d/d9afc1c58e48f8e6e7af3414041106af38ff05', '/.git/objects/0d/db7f9b502bca441642e7d54c6c212f0b6673ff', '/.git/objects/0e/0761bb314058c32679440d8686420159c31db0', '/.git/objects/0e/189b31f7dcfb116ba1781be5bb5d54bd41041e', '/.git/objects/0e/19651c4d48fa439f5123ab04cd94245f216743', '/.git/objects/0e/5f82aa92d0553cc9b4fd2cb4dbd2739e2ee8f0', '/.git/objects/0e/7262601e46c40b320da44a929f151c2c114032', '/.git/objects/0e/abd83d251910f3dbe9afcb67d962c186a2ca8c', '/.git/objects/0e/b37de8ca5ba7a34797b3355f41cf01b22ff008', '/.git/objects/0e/be1fc27f8d238046aea951e6caa693563a5db1', '/.git/objects/0e/f556b4beacab982c37a6ba626b68c12a03a3ae', '/.git/objects/0e/fcc5d9fbd21558e1d5c24872e4a1bfab7f3685', '/.git/objects/0f/0fd7c9c9227536929d8dbccd17cebd51cea76a', '/.git/objects/0f/138f0796a06e405b352d9b196d634fe03272bd', '/.git/objects/0f/17f23b4277ae965b175409f9ef0ca8fe5faca8', '/.git/objects/0f/272f7f62bbef400af52029018e0b40f2e84d63', '/.git/objects/0f/2c1f18c6195cd349bfc1bcf75c63a4676aa178', '/.git/objects/0f/375603ef57e02e9fb0b574a426b1efba49d8e8', '/.git/objects/0f/3a6ec84962b576c06d6f3836465b86e5b3f10e', '/.git/objects/0f/3f373dbe68457e2f332b53419313c5297f50fa', '/.git/objects/0f/54a10edafd4f6d7e03edbb6dc48a45c44aad67', '/.git/objects/0f/573afb56cf5cd6dd86621f5e5c4d7eeff7c726', '/.git/objects/0f/5968785d1283804001ca49ccf77d63eac98e02', '/.git/objects/0f/7e32dc222c7d9c81f5f3e241496ba69be2baad', '/.git/objects/0f/86a023e15a5799c8ab4b6e83f38d4c8b1a13bc', '/.git/objects/0f/904c72f18187d5c05f93cb546a711f8c3a9f02', '/.git/objects/0f/9209089f7c1036e89d7dbeaeefd1ad16a0ee18', '/.git/objects/0f/a19e3e148a3e82579b6e266e89dc11d898930c', '/.git/objects/0f/b3ec07ae5333277f64ed812af5f0f22e48fb1f', '/.git/objects/0f/f56f42c9ecca878a4c0e2e836e52a449662082', '/.git/objects/10/18a2334d5c1968f40c2f478fb1f2867e67b8b5', '/.git/objects/10/261e06f4cf6f32be1271762e4e2656d3227141', '/.git/objects/10/36c4359913cb364e8129ef0b26eb5dec343083', '/.git/objects/10/64453d1e30d78cd388f816b907f7b742375e31', '/.git/objects/10/7c2333f5bcbcad6ce31755c9b4b4c72e960d28', '/.git/objects/10/8486aa16f8b5f2eb525d9c860949a60ac34a76', '/.git/objects/10/9488d1db9f25b656ca5a4eed3b42ca6c3bd9f0', '/.git/objects/10/9674e0533514d7be518ce93f1318966acdaffa', '/.git/objects/10/ac366f495ba690682ed41a0ddb0004802f5ee2', '/.git/objects/10/ae7490a1f6894c54b727bd84a05889b1db8ffc', '/.git/objects/10/b37de565a520d0c743bf3d148cffdb597a14df', '/.git/objects/10/b4f635a80dd5742205f90e9a48383eb5a45dac', '/.git/objects/10/b5e2bbd4086ddc791db7fc3a786213e5107286', '/.git/objects/10/b839896461248c56e80d5915ed1ec52914b2d9', '/.git/objects/10/c8846d5380b664959d63759591c3a6f604540a', '/.git/objects/10/cc3dd9ffce62367bfd3e274024a84fa4bbf4fc', '/.git/objects/10/e1a2f389c4804375ce951f98069ea0e864c3f6', '/.git/objects/10/e5e5a2fb3b0739fa07632f8bacc69cd115ba17', '/.git/objects/11/073d080b9f772afb962eaa10e3583a841100fd', '/.git/objects/11/0a03a57b065c62b17946ce2f9c27ae14cd09e9', '/.git/objects/11/52abac92eac8d8b605f61e7608e5151d222f07', '/.git/objects/11/562ae195fafe5127b0a1577159048b0af6fbc4', '/.git/objects/11/68066a747c3bef2d6e633b2347c20cc6b56404', '/.git/objects/11/6968b47e00996915b67531127f0954c7ddd1a4', '/.git/objects/11/7f881842de701288d44a04738aeddf2eb62771', '/.git/objects/11/848596c43002718041db85d44d4f17fef2fd2d', '/.git/objects/11/a8a92beabf4c3b84689c4b3815e4c19b948151', '/.git/objects/11/b6a93338766923a8e6379405e6fcf4ab828169', '/.git/objects/11/c044d348cd73163f05a9c3b2909019bf4150b1', '/.git/objects/11/e01dd8395bcb4499bbae87a8fa5d396b5bb9a0', '/.git/objects/11/e234b29ee21a975610c871bc3aca80ba403997', '/.git/objects/11/f3df8ac49a0be182d46132407e50090bc85a7e', '/.git/objects/12/3bbafac5135532670900b0daeade243b64415e', '/.git/objects/12/46c37c3be32064b636700c62bc59120a41a208', '/.git/objects/12/482204acdc7b5906f6985edd7052cf24e81715', '/.git/objects/12/60fee99a4cfcbd9d4ffb0eb2de091a7a472b7b', '/.git/objects/12/782408d18b12ea7c1fd9e5d39ddbfa2040ef21', '/.git/objects/12/8150674170b66350257cc719da038a61a568bf', '/.git/objects/12/8991f222be89980a285c1a719170f19cebd863', '/.git/objects/12/a298fd576dee88bdd1d5b4f72dedf5ebe264d9', '/.git/objects/12/bac80bceda99fedc73290309b748399405be41', '/.git/objects/12/db0c6cc3d0ec7d7834be73cbded60279418c53', '/.git/objects/12/ecf89d4939f447a2a13eb6a8584268d822df06', '/.git/objects/12/f27c213102a0ac8c26ec5d35886d36e011d04c', '/.git/objects/13/0454723003170e9f3e6ed225d66f809f6b6dad', '/.git/objects/13/049a15f6a54c096b02c7573999db421178a726', '/.git/objects/13/0b070345feb323ae3fde1c7d932945f3191106', '/.git/objects/13/2b510d6d7bcd743b4cbf1ea79259bf32a0098f', '/.git/objects/13/2c537172da3f2875b3ce54f4b1f5af4cd1eb1f', '/.git/objects/13/31cd4e5b63c9aa3bfc3c37f80674cc03c74071', '/.git/objects/13/360394a41c8fabc39419ab404191a8575e2799', '/.git/objects/13/3c2a7f8f0c8e8798adb0c95502b796e8304aa0', '/.git/objects/13/53a7a4fc4f5419b52d1dc280f7536194c60122', '/.git/objects/13/92a68ba7c0702c66b4fb266ffd087081b1e141', '/.git/objects/13/d4e7409000e6a4b0bf0196e7c4db9005e68a3a', '/.git/objects/13/e514857a46401864fca0265d1d7e83a40fc30c', '/.git/objects/13/fb8a33b9d96c2a9ff445c20dea718e895df5e4', '/.git/objects/14/28bfd5a05e95735a945cf34906ebf3948fa13a', '/.git/objects/14/3334e584ff71080c606f29c1ef42924bbe453d', '/.git/objects/14/394b47e18f572003e3d82368702dfd474b70c4', '/.git/objects/14/3df4c79cc8ee0249f8509549e5377882a28010', '/.git/objects/14/740e00ca060ea5ea55d359d8e94b78c9b27bad', '/.git/objects/14/74c8f7cf8bc22cda503322795cac94ac621675', '/.git/objects/14/818693e025769bce36db9ab228de95282c660c', '/.git/objects/14/8c20fa8c56ae81068aded6b9a8f2a59fc229dd', '/.git/objects/14/9215c98341f0291662bea80be4491d80cce454', '/.git/objects/14/93fb5b0b0a7a8c28aa2e0e11e3024fdd6605a4', '/.git/objects/14/a51ee6f2160b21205c9afd9f7cc99748092bde', '/.git/objects/14/a5b829f9591df4d9d656268f7ad309be05e97f', '/.git/objects/14/b14cb4896fb71ae400bad91fd17aca2dc37cdd', '/.git/objects/14/c258aa37b196e7602622c9d90721c7cdfc96e5', '/.git/objects/14/c2a807581505e916cb62d8d2195af8a6c9fe9b', '/.git/objects/14/dcb371d5f4cc65cc76297ddc5125507b9752fc', '/.git/objects/14/e09849fda36affbc8abb417ca8b46778461bc7', '/.git/objects/14/e4ef69520a217c61e1dfd2f8b23fab0b8f65dc', '/.git/objects/14/f842403e89680c08c9e914aa7da06da74192d5', '/.git/objects/14/fe9bb6670802ae36d1022630b687088b71c35d', '/.git/objects/15/098da0ba5b0e2d399d8688a8a0b6a0fcd68d1d', '/.git/objects/15/3e02e9a9c73af7f51d590516702350390c0c12', '/.git/objects/15/5f8df967724158d80873e629c6c12bb65c8d00', '/.git/objects/15/6d79f56790f38a4c9d716aa1e76e0d9eaa5ee3', '/.git/objects/15/709f6e54c6706e2d1debd66e87ab969ed3cb3b', '/.git/objects/15/80c27de69b78994d59b6f22fa0e0da62c8705f', '/.git/objects/15/934046b41baa7c1df153b1fa8b4f7b45d6d363', '/.git/objects/15/9a11018b3d33d8eb168b6a1a565f70b3874135', '/.git/objects/15/9bfd26b659195df8c8486d12b5e15f948cb808', '/.git/objects/15/bcd112607d47deea3216fc8137482fd0a57dfd', '/.git/objects/15/be2e474eb938a89e4d7c19737994893197e781', '/.git/objects/15/fc480833c1c814d413e14a2421b5ffed74028f', '/.git/objects/15/fd3d807851be39f668587b875d1bd9356e1171', '/.git/objects/15/ff558cf9cbc3541c227c019c1ff2b0afc0e4c8', '/.git/objects/16/22c65984231f8952831bb55b298781f51ed32a', '/.git/objects/16/282c3c9e7f94259ee473e3b448a4bf153f7faf', '/.git/objects/16/3d050dd4db671d29be7efff1a35864f91ca61d', '/.git/objects/16/45e0141c84a5d338b3e0bde5c3a4c30f05102e', '/.git/objects/16/4b7fafb2c4bcbb6315f95870ae3efbf8a82241', '/.git/objects/16/50783e350f6307c3535eb8300baa648a123c58', '/.git/objects/16/5d22d6f5554de58d1281ade7295158d4e62312', '/.git/objects/16/6de2e7604a6a403e37c7580a2396b1c77703a9', '/.git/objects/16/7230ee6e97a40999b7b1b46b089e48951a1158', '/.git/objects/16/83c29855a1711cfb4c85bcd36a6a497a46dd25', '/.git/objects/16/9b7c3ac237ddbfd037e96566cae9579871112a', '/.git/objects/16/a2cab9c4e32851d2754116ca26b4ead49cd1a3', '/.git/objects/16/a6b6c10cf2c147d781304dcd12f19322706a4f', '/.git/objects/16/bc644bbb95c0d296bea492b5595b361a93b9fa', '/.git/objects/16/d1e49e991257dccbb3cf2869412da65640aa07', '/.git/objects/16/d466f5d6f6422fc565801d9d97c0bd71bf6a5a', '/.git/objects/16/de7d0bc43866f4573019d564ac08d4f8eea2f0', '/.git/objects/16/f919383aca2b4bce706604aedfea22eb53d4d2', '/.git/objects/17/08da67f2248817035645f0eead4b6b5a023a1c', '/.git/objects/17/110ef00ea00c8b277ccc1969e941960bcdb9d2', '/.git/objects/17/12e4e54ab123623ddb99788dfcd22ca63f147e', '/.git/objects/17/13e1eac64de51e326768dd2f182be6420c8c24', '/.git/objects/17/2a1aecedf8f730cc736adab0896ebcd8f4ecd2', '/.git/objects/17/49a45900cab2305e03dcc84a1bacdc83b5c650', '/.git/objects/17/6546fcce9f60340b03abf2872c11a034082436', '/.git/objects/17/9ec7dd1edfe1baa93d1908ae452873cde0813f', '/.git/objects/17/a7554a0ca31ea30842e18f3d1a9a30f54ec031', '/.git/objects/17/a81efd91baac6d0f9b7b97418a758f2e456b40', '/.git/objects/17/c6782b615441baeb457ee93a458ed7371c9f99', '/.git/objects/18/05a2dd4a8437e8c9e8fdc04ab4260ee0b2aeac', '/.git/objects/18/05f56abd31c9fa832a4d2e4d2a6525282bd60f', '/.git/objects/18/0a30f4465131f600b52b5c8f8a41d4887cf32a', '/.git/objects/18/17fab90bcdedb3058f97f246f59ae272ad2c5e', '/.git/objects/18/21c73daef08582322b9bc4a31cd5880b8adb89', '/.git/objects/18/3171671f787123e587964ba3c4fcf139c40889', '/.git/objects/18/5c9bede1c02917cd4743d154dc42b2cd03cb25', '/.git/objects/18/62eec0af25e420dee69a16ba235f610f20756d', '/.git/objects/18/76a2d804d63aaa68f7f32d2cdc14185714278d', '/.git/objects/18/88c3e87775cf3cfca934be2e7ec03a6696f1da', '/.git/objects/18/9863df3ed4479c15d6680c8622e96ee0d0be8a', '/.git/objects/18/b3b55a80a1942fe133c9ace4bf055c01d9ad0f', '/.git/objects/18/ba4542dad707bf99c1a2adcfa404250cc1b089', '/.git/objects/18/d512a4ebe9f93cc357a19059984b3398799bee', '/.git/objects/18/ef4273b710a54a42f8d3e9bde696c1024a7b8b', '/.git/objects/18/f82c64090708721c25b1e7896d72fd0873be55', '/.git/objects/18/fbc8999394da7378100f6b400106be1234cae6', '/.git/objects/18/fe30c098f75b96caa54450040279f8727780ea', '/.git/objects/19/29b4d821dbc5d88f2c4c6d8839d0fedf3fa95f', '/.git/objects/19/5b074ba1d8f9cefb2257753cff1029f9892c07', '/.git/objects/19/67856dd6c0cf834184b8074bf96bd27d1d1cbb', '/.git/objects/19/704e0cd5db5fec06dd7c57009e47296c0c4411', '/.git/objects/19/8afff444fc2597b22ebb81827317a058d5d305', '/.git/objects/19/928324ad53403e47456f49785dd300a6abc1e0', '/.git/objects/19/bc9e08c030c0958b8cfcb118ef4e6a076e1bfe', '/.git/objects/19/d15ee65c1ad2342c69a499567a3d8e33d985d2', '/.git/objects/19/ded65fb060984405248fb64a74c46cd5c30bd8', '/.git/objects/19/df64437a4daafb76d0c80d72781063e732cc80', '/.git/objects/19/eac84456408b48017f9b8f7012a31d357f9ded', '/.git/objects/19/ef249a5908e6c6f084c18763897a644a28241b', '/.git/objects/19/fc4aad4089856ed15007cdce1ab6d36334698e', '/.git/objects/1a/04525ea6855d36a41a4720d225e21887989682', '/.git/objects/1a/22181ef0ac06c928b1ade28aae4b43e1b12cb7', '/.git/objects/1a/2753848f8639473628dd7181b675289eedd891', '/.git/objects/1a/38b5577a7a7ecb92c28362927b10d12cae6cb4', '/.git/objects/1a/3d1d26fcaacd2823b81e326ffca9fdfa58d430', '/.git/objects/1a/412f9779d45d9ae9d43dfac14cf5ab0a27bd9a', '/.git/objects/1a/789d6391ac1059bf44744e16bd82208bcf825c', '/.git/objects/1a/7adf1b642469d585dfee765c7f93ba59f6d63c', '/.git/objects/1a/7b119a11b008be1ded0bd9ca1ddfad0e5a5260', '/.git/objects/1a/8cfcaa66700c9a9630054d0b790be56800ad4e', '/.git/objects/1a/92bc0612cc609c6b1cabd35c7b04aba33abfc4', '/.git/objects/1a/955782d22785e3c692639e34ac42ecd1ad95be', '/.git/objects/1a/a876353fd8f7049e2abc2fb1fb5245905b991d', '/.git/objects/1a/bb94d4c0919eb7eb99cc9789830d5ef359b48f', '/.git/objects/1a/bf3ec50e284c4a38d8ea30a9c827014145d73a', '/.git/objects/1a/cb54093be1c2b283021bce603fce39cd8f4e49', '/.git/objects/1a/d989e5f29b4bf9e48e4b5b15a78ef6c572eae7', '/.git/objects/1a/e3ab2623d40253c472d74b5ff8a709df3e07a1', '/.git/objects/1a/f2cf9b84d9c743823d3d37acc8320dbaf6f8fd', '/.git/objects/1a/f40bbfa396e5c7c03af2156636160c39967a5a', '/.git/objects/1a/fcc87003afe09c0245ee2e2f90a48f107eea91', '/.git/objects/1a/fe522d67bb11ef6df1ef598c4a6077cbdbf43f', '/.git/objects/1b/2651a7254d50dd505d130cb119b1e0f63b274d', '/.git/objects/1b/297017feb7427e872083cfba46fdd2d1f5d1f1', '/.git/objects/1b/b6184cbc8ec7b0b92597da642ddb7baea3f9f0', '... [results truncated, try being more specific with your parameters]']
AI: Let me find the actual input files and reference documents.[{'name': 'glob', 'args': {'pattern': 'inputs/**/*', 'path': '/'}, 'id': 'call_00_7V08j3IuVHAm4yICp6Pw8705', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'outputs/**/*', 'path': '/'}, 'id': 'call_01_zJx3NBQwMyYkxFu84qcT6924', 'type': 'tool_call'}, {'name': 'glob', 'args': {'pattern': 'references/**/*', 'path': '/'}, 'id': 'call_02_5yofIc8G7OvneoCSTGCZ7937', 'type': 'tool_call'}]
Tool: ['/inputs/contract.txt', '/inputs/matrix.json']
Tool: ['/.venv/Lib/site-packages/langchain_core/outputs/__init__.py', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/__init__.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/chat_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/generation.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/llm_result.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/__pycache__/run_info.cpython-314.pyc', '/.venv/Lib/site-packages/langchain_core/outputs/chat_generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/chat_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/generation.py', '/.venv/Lib/site-packages/langchain_core/outputs/llm_result.py', '/.venv/Lib/site-packages/langchain_core/outputs/run_info.py', '/outputs/working/build_inventories.py', '/outputs/working/contract_inventory.json', '/outputs/working/matrix_inventory.json']
Tool: ['/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', '/skills/acquiring-discrepancy-analysis/references/output-contract.md']
AI: Good. The inventories already exist. Let me read the key files: the matrix, contract, inventories, and reference documents.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 200}, 'id': 'call_00_A2gNiwHhr7mvhqyCdKCH0228', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 200}, 'id': 'call_01_wC3A0L6Qxz9YQxrhKUOb0832', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'limit': 200}, 'id': 'call_02_RBej17vWgOXpP3RBuUgr2426', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'limit': 200}, 'id': 'call_03_JZAmjiPVojfWphdA4XPR7375', 'type': 'tool_call'}]
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
AI: Now let me continue reading the matrix and contract to understand the full scope, and also read the reference documents.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_djZIzPh2e1r0Xb2Fs8DT4187', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'offset': 200, 'limit': 300}, 'id': 'call_01_4LA1EznI9hxu3VBo52Aj8195', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/output-contract.md', 'limit': 200}, 'id': 'call_02_tUP2omDBRN2oygdQPKdU6707', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/references/comparison-patterns.md', 'limit': 200}, 'id': 'call_03_5qNx0Xfq2mIwhrIT0vhO8593', 'type': 'tool_call'}]
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
AI: Now let me read the rest of the matrix and contract inventories to understand the full scope, and also read the remaining matrix items.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'offset': 200, 'limit': 300}, 'id': 'call_00_jHC2MpcZKrgBIjjj5w7p7768', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 200, 'limit': 300}, 'id': 'call_01_a73RAzaYK92V6jCwXhtd7771', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 500, 'limit': 300}, 'id': 'call_02_AF05w8tzu5u5Cu2vuFbg6373', 'type': 'tool_call'}]
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
AI: Now I have a good understanding of the structure. Let me check how many matrix items there are and understand the batch assignment. Let me also read the remaining matrix items and contract inventory.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\') as f:\n    matrix = json.load(f)\nprint(f\'Total matrix items: {len(matrix)}\')\nfor i, m in enumerate(matrix):\n    print(f\'{i}: {m[\\"number\\"]} - materiality check: {m.get(\\"required_type\\",\\"?\\")} - product: {m.get(\\"only_for_product\\",\\"?\\")}\')\n"'}, 'id': 'call_00_S8H9trUzwcR39sMwQmca8209', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 7
[stderr]     print(f'{i}: {m[" number\]}
[stderr]                     ^
[stderr] SyntaxError: unterminated string literal (detected at line 7)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\') as f:\n    matrix = json.load(f)\nprint(\'Total matrix items:\', len(matrix))\nfor i, m in enumerate(matrix):\n    num = m[\'number\']\n    req = m.get(\'required_type\',\'?\')\n    prod = m.get(\'only_for_product\',\'?\')\n    print(f\'{i}: {num} | {req} | {prod}\')\n"'}, 'id': 'call_00_bF9lzUZ5xEtG706dctHl8138', 'type': 'tool_call'}]
Tool: Total matrix items: 169
0: 2.1 | mandatory | common
1: 2.2 | mandatory | common
2: 2.3.1 | mandatory | common
3: 2.3.2 | mandatory | common
4: 2.3.3 | optional | common
5: 2.3.4 | optional | common
6: 2.3.5 | mandatory | common
7: 2.3.6 | mandatory | common
8: 2.3.7 | optional | common
9: 2.4 | optional | common
10: 2.5.1.1 | mandatory | internet_acquiring
11: 2.5.2.1 | mandatory | trade_acquiring
12: 2.6.1.1 | mandatory | trade_acquiring
13: 2.6.2.1 | mandatory | trade_acquiring
14: 2.6.2.2 | mandatory | trade_acquiring
15: 2.6.3.1 | mandatory | trade_acquiring
16: 2.6.3.2 | mandatory | trade_acquiring
17: 2.7 | optional | common
18: 3.1 | optional | common
19: 3.2 | optional | common
20: 3.3 | mandatory | common
21: 4.1.1 | optional | common
22: 4.1.2 | optional | common
23: 4.1.3 | optional | trade_acquiring
24: 4.2.1 | mandatory | common
25: 4.2.2 | optional | common
26: 4.2.3 | optional | common
27: 4.2.4 | optional | common
28: 4.2.5 | mandatory | common
29: 4.2.6 | mandatory | common
30: 4.2.7 | mandatory | common
31: 4.2.8 | mandatory | common
32: 4.2.9 | mandatory | common
33: 4.2.10 | mandatory | common
34: 4.2.11 | mandatory | common
35: 4.2.12 | optional | common
36: 4.2.13 | mandatory | common
37: 4.2.14 | mandatory | common
38: 4.2.15 | mandatory | common
39: 4.2.16.1 | mandatory | common
40: 4.2.16.2 | mandatory | common
41: 4.2.16.3 | mandatory | common
42: 4.2.17 | mandatory | internet_acquiring
43: 4.2.18 | mandatory | common
44: 4.2.19 | mandatory | common
45: 4.2.20.1 | mandatory | trade_acquiring
46: 4.2.20.2 | mandatory | trade_acquiring
47: 4.2.20.3 | mandatory | trade_acquiring
48: 4.2.20.4 | mandatory | trade_acquiring
49: 4.2.20.5 | mandatory | trade_acquiring
50: 4.2.20.6 | mandatory | trade_acquiring
51: 4.2.20.7 | mandatory | trade_acquiring
52: 4.2.21.1 | mandatory | internet_acquiring
53: 4.2.21.2 | mandatory | internet_acquiring
54: 4.2.21.3 | mandatory | internet_acquiring
55: 4.2.21.4 | mandatory | internet_acquiring
56: 4.2.21.5 | mandatory | internet_acquiring
57: 4.2.21.6 | mandatory | internet_acquiring
58: 4.2.21.7 | mandatory | internet_acquiring
59: 4.2.21.8 | mandatory | internet_acquiring
60: 4.2.22 | optional | trade_acquiring
61: 4.2.23 | optional | trade_acquiring
62: 4.2.24 | optional | common
63: 4.2.25 | optional | common
64: 4.2.26 | mandatory | internet_acquiring
65: 5.1.1.1 | mandatory | common
66: 5.1.1.2 | mandatory | common
67: 5.1.1.3 | mandatory | common
68: 5.1.1.4 | mandatory | common
69: 5.1.1.5 | mandatory | common
70: 5.1.1.6 | mandatory | trade_acquiring
71: 5.1.2 | mandatory | common
72: 5.1.3 | mandatory | common
73: 5.1.4 | mandatory | common
74: 5.1.5 | mandatory | common
75: 5.1.6 | mandatory | common
76: 5.1.7 | mandatory | common
77: 5.1.8.1 | optional | common
78: 5.1.8.2 | optional | common
79: 5.1.8.3 | optional | common
80: 5.1.8.4 | optional | internet_acquiring
81: 5.1.8.5 | optional | internet_acquiring
82: 5.1.8.6 | optional | common
83: 5.1.8.7 | optional | common
84: 5.1.8.8 | optional | trade_acquiring
85: 5.1.8.9 | optional | common
86: 5.1.8.10 | optional | common
87: 5.1.8.11 | optional | common
88: 5.1.8.12 | optional | common
89: 5.1.8.13 | optional | common
90: 5.1.9 | mandatory | common
91: 5.1.10 | mandatory | common
92: 5.1.11 | mandatory | common
93: 5.1.12 | optional | common
94: 5.1.13 | optional | common
95: 5.1.14 | mandatory | common
96: 5.1.15 | optional | common
97: 5.1.16 | mandatory | common
98: 5.1.17.1 | optional | trade_acquiring
99: 5.1.17.2 | optional | trade_acquiring
100: 5.2.1 | mandatory | internet_acquiring
101: 5.2.2 | mandatory | internet_acquiring
102: 5.2.3 | mandatory | trade_acquiring
103: 5.2.4 | optional | common
104: 5.2.5 | optional | common
105: 5.2.6 | optional | trade_acquiring
106: 5.2.7 | optional | common
107: 5.2.8 | mandatory | common
108: 5.2.9 | optional | trade_acquiring
109: 5.2.10 | mandatory | common
110: 5.2.12 | optional | internet_acquiring
111: 6.1 | mandatory | common
112: 6.2 | mandatory | common
113: 6.3 | mandatory | common
114: 6.4 | mandatory | common
115: 6.5 | mandatory | common
116: 6.6 | mandatory | common
117: 6.7 | mandatory | trade_acquiring
118: 6.8 | mandatory | trade_acquiring
119: 6.9 | mandatory | trade_acquiring
120: 6.10 | mandatory | trade_acquiring
121: 6.11 | mandatory | trade_acquiring
122: 6.12 | mandatory | trade_acquiring
123: 6.13 | mandatory | trade_acquiring
124: 6.14 | mandatory | trade_acquiring
125: 6.15 | mandatory | trade_acquiring
126: 6.16 | mandatory | trade_acquiring
127: 6.17 | mandatory | trade_acquiring
128: 6.18 | mandatory | trade_acquiring
129: 6.20 | mandatory | common
130: 6.21 | mandatory | common
131: 7.1 | mandatory | common
132: 7.2 | mandatory | common
133: 7.3 | mandatory | common
134: 7.4 | mandatory | common
135: 7.5 | mandatory | common
136: 7.6 | mandatory | common
137: 7.7 | mandatory | common
138: 7.8 | optional | common
139: 7.9 | optional | common
140: 7.10 | optional | common
141: 7.11 | optional | common
142: 7.12 | optional | common
143: 7.13 | mandatory | internet_acquiring
144: 7.14 | mandatory | common
145: 7.15 | mandatory | common
146: 7.16 | mandatory | common
147: 7.17 | mandatory | common
148: 8.1 | mandatory | common
149: 8.2 | mandatory | common
150: 9.1 | mandatory | common
151: 9.2 | mandatory | common
152: 9.3 | mandatory | common
153: 10.1 | mandatory | common
154: 10.2 | mandatory | common
155: 10.3 | mandatory | common
156: 11.1 | optional | common
157: 11.2 | optional | common
158: 11.3 | optional | common
159: 11.4 | optional | common
160: 11.5 | optional | common
161: 11.6 | optional | common
162: 11.7 | optional | common
163: 11.8 | optional | common
164: 11.9 | optional | common
165: 11.10 | optional | common
166: 11.11 | optional | common
167: 11.12 | optional | common
168: 11.13 | optional | common

[Command succeeded with exit code 0]
AI: Now I understand the full scope. There are 169 matrix items. The task says "Matrix batch 1 comparison" — I need to work on the first batch. Let me set up my task plan and start the analysis. The skill says to split material matrix ids into 3-5 batches. I'll work on batch 1 which covers matrix items from the beginning (roughly items 0-40 or so, covering sections 2 and early 3/4).

Let me set up my working plan and begin the detailed legal comparison.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix items for batch 1 (matrix ids 2.1 through ~4.2.11, approximately items 0-34)', 'status': 'in_progress'}, {'content': 'Read full contract text for relevant sections (sections 1-5, appendices)', 'status': 'pending'}, {'content': 'Perform legal comparison for each batch 1 matrix item against contract', 'status': 'pending'}, {'content': 'Build links, atomic_links, and unmatched_matrix for batch 1', 'status': 'pending'}, {'content': 'Write batch 1 fragment to /outputs/working/batch_1_fragment.json', 'status': 'pending'}, {'content': 'Provide summary of batch 1 findings', 'status': 'pending'}]}, 'id': 'call_00_cUkXJhh0huwpgZDZ0tN79572', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix items for batch 1 (matrix ids 2.1 through ~4.2.11, approximately items 0-34)', 'status': 'in_progress'}, {'content': 'Read full contract text for relevant sections (sections 1-5, appendices)', 'status': 'pending'}, {'content': 'Perform legal comparison for each batch 1 matrix item against contract', 'status': 'pending'}, {'content': 'Build links, atomic_links, and unmatched_matrix for batch 1', 'status': 'pending'}, {'content': 'Write batch 1 fragment to /outputs/working/batch_1_fragment.json', 'status': 'pending'}, {'content': 'Provide summary of batch 1 findings', 'status': 'pending'}]
AI: Let me read the remaining matrix items I need for batch 1 and also the remaining contract inventory entries.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/matrix_inventory.json', 'offset': 500, 'limit': 200}, 'id': 'call_00_T5R70RJw1UV9XrfE86wf3791', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_inventory.json', 'offset': 500, 'limit': 300}, 'id': 'call_01_yBkKTqq4sJzuUh471ESp7216', 'type': 'tool_call'}]
Tool:    501	    "material_terms": "none explicit",
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
Tool:    501	    "material_terms": "",
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
   701	    "party": "neutral/definitional",
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
AI: Now I have a thorough understanding of both documents. Let me define batch 1 scope. Based on the skill's instruction to split into 3-5 batches, I'll take batch 1 as matrix items 0 through approximately 40 (matrix ids 2.1 through 4.2.16.3), which covers the core registration, document exchange, subject matter, and merchant obligations sections.

Let me now perform the detailed legal comparison for batch 1. I'll work through each matrix item systematically.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read full matrix items for batch 1 (matrix ids 2.1 through ~4.2.11, approximately items 0-34)', 'status': 'completed'}, {'content': 'Read full contract text for relevant sections (sections 1-5, appendices)', 'status': 'completed'}, {'content': 'Perform legal comparison for each batch 1 matrix item against contract', 'status': 'in_progress'}, {'content': 'Build links, atomic_links, and unmatched_matrix for batch 1', 'status': 'pending'}, {'content': 'Write batch 1 fragment to /outputs/working/batch_1_fragment.json', 'status': 'pending'}, {'content': 'Provide summary of batch 1 findings', 'status': 'pending'}]}, 'id': 'call_00_BmhBgK7PMXm6b5oJxQFC0313', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read full matrix items for batch 1 (matrix ids 2.1 through ~4.2.11, approximately items 0-34)', 'status': 'completed'}, {'content': 'Read full contract text for relevant sections (sections 1-5, appendices)', 'status': 'completed'}, {'content': 'Perform legal comparison for each batch 1 matrix item against contract', 'status': 'in_progress'}, {'content': 'Build links, atomic_links, and unmatched_matrix for batch 1', 'status': 'pending'}, {'content': 'Write batch 1 fragment to /outputs/working/batch_1_fragment.json', 'status': 'pending'}, {'content': 'Provide summary of batch 1 findings', 'status': 'pending'}]
AI: Now let me read the specific matrix items I need for the detailed comparison. Let me get the full enriched text for the key matrix items in batch 1.[{'name': 'execute', 'args': {'command': 'python3 -c "\nimport json\nwith open(\'/inputs/matrix.json\') as f:\n    matrix = json.load(f)\n# Print items 0-41 (batch 1: 2.1 through 4.2.16.3)\nfor i in range(0, 42):\n    m = matrix[i]\n    print(f\'=== ITEM {i}: {m[\\"number\\"]} ===\')\n    print(f\'required_type: {m[\\"required_type\\"]}\')\n    print(f\'only_for_product: {m[\\"only_for_product\\"]}\')\n    print(f\'main_idea: {m[\\"main_idea\\"][:200]}\')\n    print(f\'enriched_text: {m[\\"enriched_text\\"][:300]}\')\n    print()\n"'}, 'id': 'call_00_dBiwj1oApdSOFaS79A0C7034', 'type': 'tool_call'}]
Tool: [stderr] File "<string>", line 8
[stderr]     print(f'=== ITEM {i}: {m[" number\]}
[stderr]                              ^
[stderr] SyntaxError: unterminated string literal (detected at line 8)

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': "python3 << 'PYEOF'\nimport json\nwith open('/inputs/matrix.json') as f:\n    matrix = json.load(f)\nfor i in range(0, 42):\n    m = matrix[i]\n    num = m['number']\n    req = m['required_type']\n    prod = m['only_for_product']\n    idea = m['main_idea'][:200]\n    txt = m['enriched_text'][:300]\n    print(f'=== ITEM {i}: {num} ===')\n    print(f'required: {req} | product: {prod}')\n    print(f'main_idea: {idea}')\n    print(f'text: {txt}')\n    print()\nPYEOF"}, 'id': 'call_00_0q8vJHw8KyuNDu5bjni75207', 'type': 'tool_call'}]
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
[stderr] At line:36 char:4
[stderr] + for i in range(0, 42):
[stderr] +    ~
[stderr] Missing opening '(' after keyword 'for'.
[stderr] At line:47 char:11
[stderr] +     print()
[stderr] +           ~
[stderr] An expression was expected after '('.
[stderr]     + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
[stderr]     + FullyQualifiedErrorId : MissingFileSpecification

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'write_file', 'args': {'file_path': '/outputs/working/print_batch1.py', 'content': "import json\nwith open('/inputs/matrix.json') as f:\n    matrix = json.load(f)\nfor i in range(0, 42):\n    m = matrix[i]\n    num = m['number']\n    req = m['required_type']\n    prod = m['only_for_product']\n    idea = m['main_idea'][:200]\n    txt = m['enriched_text'][:300]\n    print(f'=== ITEM {i}: {num} ===')\n    print(f'required: {req} | product: {prod}')\n    print(f'main_idea: {idea}')\n    print(f'text: {txt}')\n    print()\n"}, 'id': 'call_00_JjgRm08wFMRHP07GsnrD8739', 'type': 'tool_call'}]
Tool: Updated file /outputs/working/print_batch1.py
AI: [{'name': 'execute', 'args': {'command': 'python3 /outputs/working/print_batch1.py'}, 'id': 'call_00_BBYcQwUZ13JOhZcg8fcI2122', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\print_batch1.py", line 2, in <module>
[stderr]     with open('/inputs/matrix.json') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/inputs/matrix.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'execute', 'args': {'command': 'ls /inputs/'}, 'id': 'call_00_VwyLMSVqzDHWuHrvNZ1Z5946', 'type': 'tool_call'}]
Tool: 

    РљР°С‚Р°Р»РѕРі: C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\inputs


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        25.06.2026     13:31         118239 contract.txt                                                         
-a----        23.06.2026     10:26         231542 matrix.json                                                          

[Command succeeded with exit code 0]
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/print_batch1.py'}, 'id': 'call_00_vjJd3qLqsn7gXQcDfajX1632', 'type': 'tool_call'}]
Tool: [stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\gogel\OneDrive\Р Р°Р±РѕС‡РёР№ СЃС‚РѕР»\РџСЂРѕРµРєС‚С‹\skillshot_manual_2\outputs\working\print_batch1.py", line 2, in <module>
[stderr]     with open('/inputs/matrix.json') as f:
[stderr]          ~~~~^^^^^^^^^^^^^^^^^^^^^^^
[stderr] FileNotFoundError: [Errno 2] No such file or directory: '/inputs/matrix.json'

Exit code: 1
[Command failed with exit code 1]
AI: [{'name': 'edit_file', 'args': {'file_path': '/outputs/working/print_batch1.py', 'old_string': "with open('/inputs/matrix.json') as f:", 'new_string': "with open('inputs/matrix.json') as f:"}, 'id': 'call_00_mKKHoiYjhdU8lt0TVZsB1939', 'type': 'tool_call'}]
Tool: Successfully replaced 1 instance(s) of the string in '/outputs/working/print_batch1.py'
AI: [{'name': 'execute', 'args': {'command': 'python3 outputs/working/print_batch1.py 2>&1 | head -200'}, 'id': 'call_00_e0Qi5EFn0L2eYpK1hQx75007', 'type': 'tool_call'}]
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
[stderr] python3 outputs/working/print_batch1.py 2>&1 | head -200
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

