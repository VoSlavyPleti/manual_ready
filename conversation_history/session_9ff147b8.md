## Summarized at 2026-06-25T21:20:15.944597+00:00

Human: ## Task: Matrix-to-Contract Comparison - Batch 3 (Matrix items 5.1.6 through 11.13)

You are a legal analyst comparing Bank standard matrix requirements against a counterparty acquiring contract.

### Input files:
- `/inputs/matrix.json` - Bank standard matrix (use `number` as matrix id)
- `/inputs/contract.txt` - Counterparty contract text
- `/outputs/working/clause_index.json` - Source map
- `/outputs/working/legal_propositions.json` - Legal proposition ledger
- `/outputs/working/contract_locator_registry.json` - Contract locator registry (use only `final_allowed=true` locators as contract_ids)

### Contract Profile:
- Product: trade_acquiring
- Lot: 44_fz (government contract under 44-FZ)
- Terminal: pos, smart
- Payment method: card, qr
- Legal regime: 44_fz
- Parties: "Заказчик" = Enterprise/Предприятие, "Исполнитель" = Bank

### Your task:
Analyze these matrix items against the FULL contract text. For each applicable evaluable matrix item, find true legal analogues in the contract.

Matrix items to analyze (Batch 3):
5.1.6, 5.1.7, 5.1.8.1, 5.1.8.2, 5.1.8.3, 5.1.8.4, 5.1.8.5, 5.1.8.6, 5.1.8.7, 5.1.8.8, 5.1.8.9, 5.1.8.10, 5.1.8.11, 5.1.8.12, 5.1.8.13, 5.1.9, 5.1.10, 5.1.11, 5.1.12, 5.1.13, 5.1.14, 5.1.15, 5.1.16, 5.1.17.1, 5.1.17.2, 5.2.1, 5.2.2, 5.2.3, 5.2.4, 5.2.5, 5.2.6, 5.2.7, 5.2.8, 5.2.9, 5.2.10, 5.2.12, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 6.12, 6.13, 6.14, 6.15, 6.16, 6.17, 6.18, 6.20, 6.21, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17, 8.1, 8.2, 9.1, 9.2, 9.3, 10.1, 10.2, 10.3, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.13

### Applicability filtering:
- If `only_for_product` is not "common" and doesn't match "trade_acquiring" or "internet_acquiring", mark as `out_of_scope`
- If `only_for_lot` is not "common" and doesn't match "44_fz", mark as `out_of_scope`
- If `only_for_terminal` is not "common" and doesn't match "pos" or "smart", mark as `out_of_scope`
- If `payment_method` is not "common" and doesn't match "card" or "qr", mark as `out_of_scope`

### Output format:
Write a fragment to `/outputs/working/fragment_batch3.json` with this structure:
```json
{
  "fragment_type": "matrix_batch",
  "assigned_matrix_ids": [...],
  "links": [...],
  "atomic_links": [...],
  "unmatched_matrix": [...],
  "coverage_ledger_matrix": [...]
}
```

Each `link` follows the output-contract schema:
- `matrix_ids`: array of matrix ids in this group
- `contract_ids`: array of contract locators (from registry, final_allowed=true)
- `relationship`: "aligned" or "deviation"
- `legal_topic`: short legal topic
- `matrix_standard`: bank standard requirement
- `contract_position`: contract position
- `matrix_evidence`: short matrix quote
- `contract_evidence`: short contract quote
- `evidence_locators`: []
- `status_reason`: group-level reason
- `risk_level`: "none", "low", "medium", "high"
- `covered_elements`: [...]
- `uncovered_elements`: [...]
- `candidate_contract_ids`: [...]
- `rejected_contract_ids`: [{"contract_id": "...", "reason": "..."}]
- `candidate_search_exhausted`: true
- `search_scope`: "full_contract"
- `discrepancies`: [{"type": "...", "description": "...", "risk": "..."}]

Each `atomic_link`:
- `matrix_id`, `contract_id`, `relationship`, `link_index`, `coverage_role`, `coverage`

Each `unmatched_matrix` item:
- `matrix_id`, `requirement`, `source_evidence`, `evidence_locators`, `status`: "missing_in_contract", `required_type`, `applicability`, `risk_level`, `risk`, `covered_elements`, `uncovered_elements`, `candidate_contract_ids`, `candidate_search_exhausted`, `search_scope`, `rejected_candidates`

Each `coverage_ledger_matrix` item:
- `matrix_id`, `closure`: "linked"|"missing_in_contract"|"out_of_scope"|"not_applicable", `link_indices`, `reason`

### Validation:
After writing the fragment, run:
```bash
python /skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py /outputs/working/fragment_batch3.json --registry /outputs/working/contract_locator_registry.json --assigned-matrix-ids "5.1.6,5.1.7,5.1.8.1,5.1.8.2,5.1.8.3,5.1.8.4,5.1.8.5,5.1.8.6,5.1.8.7,5.1.8.8,5.1.8.9,5.1.8.10,5.1.8.11,5.1.8.12,5.1.8.13,5.1.9,5.1.10,5.1.11,5.1.12,5.1.13,5.1.14,5.1.15,5.1.16,5.1.17.1,5.1.17.2,5.2.1,5.2.2,5.2.3,5.2.4,5.2.5,5.2.6,5.2.7,5.2.8,5.2.9,5.2.10,5.2.12,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,6.10,6.11,6.12,6.13,6.14,6.15,6.16,6.17,6.18,6.20,6.21,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,7.10,7.11,7.12,7.13,7.14,7.15,7.16,7.17,8.1,8.2,9.1,9.2,9.3,10.1,10.2,10.3,11.1,11.2,11.3,11.4,11.5,11.6,11.7,11.8,11.9,11.10,11.11,11.12,11.13"
```

If validation fails, fix the errors and re-run until it passes. Return the validation result.
AI: I'll start by reading the skill file and all input files to understand the data structures.[{'name': 'write_todos', 'args': {'todos': [{'content': 'Read skill file and all input files', 'status': 'in_progress'}, {'content': 'Read matrix.json for batch 3 items (5.1.6-11.13)', 'status': 'pending'}, {'content': 'Read contract.txt, clause_index.json, legal_propositions.json, contract_locator_registry.json', 'status': 'pending'}, {'content': 'Analyze each matrix item against contract text', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, coverage_ledger_matrix', 'status': 'pending'}, {'content': 'Write fragment_batch3.json', 'status': 'pending'}, {'content': 'Validate with validate_fragment.py and fix errors', 'status': 'pending'}]}, 'id': 'call_00_H84MFvJFiJa3lB5iDyfA3246', 'type': 'tool_call'}]
Tool: Updated todo list to [{'content': 'Read skill file and all input files', 'status': 'in_progress'}, {'content': 'Read matrix.json for batch 3 items (5.1.6-11.13)', 'status': 'pending'}, {'content': 'Read contract.txt, clause_index.json, legal_propositions.json, contract_locator_registry.json', 'status': 'pending'}, {'content': 'Analyze each matrix item against contract text', 'status': 'pending'}, {'content': 'Build links, atomic_links, unmatched_matrix, coverage_ledger_matrix', 'status': 'pending'}, {'content': 'Write fragment_batch3.json', 'status': 'pending'}, {'content': 'Validate with validate_fragment.py and fix errors', 'status': 'pending'}]
AI: [{'name': 'read_file', 'args': {'file_path': '/skills/acquiring-discrepancy-analysis/SKILL.md', 'limit': 1000}, 'id': 'call_00_VpRHIOS74mTh5cF36lmc2926', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 500}, 'id': 'call_01_aOgDU77sf0iswDaNOhb34888', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_locator_registry.json', 'limit': 500}, 'id': 'call_02_LK1l33v7RgFw3TWbCQJH6403', 'type': 'tool_call'}]
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
    17	- `references/delegation-contract.md` before delegating subagent work or merging
    18	  subagent fragments.
    19	
    20	## Purpose
    21	
    22	Find and explain:
    23	
    24	- Bank-standard matrix requirements preserved by the contract;
    25	- true analogues that deviate from the Bank standard;
    26	- applicable matrix requirements absent from the contract;
    27	- legally meaningful contract terms with no matrix analogue.
    28	- matrix requirements that are out of scope for the current contract profile,
    29	  closed in the internal ledger without final risk reporting.
    30	
    31	The review is risk-oriented. Missing a real risk is worse than marking a
    32	borderline issue as `deviation`, but weak thematic matches must not be promoted
    33	into legal links.
    34	
    35	## Inputs And Outputs
    36	
    37	Inputs:
    38	
    39	- `inputs/matrix.json`: Bank standard matrix. Use `number` as the matrix id.
    40	  Analyze `main_idea`, `topics`, `enriched_text`, obligation fields, and
    41	  applicability filters.
    42	- `inputs/contract.txt`: full counterparty contract text. Use printed clause
    43	  ids or real document locators visible in this file.
    44	
    45	Final outputs:
    46	
    47	- `/outputs/discrepancy_analysis.json`: source-of-truth machine artifact.
    48	- `/outputs/discrepancy_analysis.xlsx`: mechanical table export from JSON.
    49	
    50	Working artifacts belong under `/outputs/working/`.
    51	
    52	## Source Hierarchy
    53	
    54	Use the source text as the legal authority:
    55	
    56	1. Matrix `enriched_text`, `main_idea`, `topics`, and applicability fields.
    57	2. Contract clause text and real printed locators from `inputs/contract.txt`.
    58	3. Working ledgers as indexes and evidence aids.
    59	
    60	Do not decide status from extracted fields alone. When a status depends on a
    61	deadline, amount, penalty, party, trigger, procedure, channel, scope, or
    62	consequence, re-read the source text.
    63	
    64	## Required Artifacts And Contracts
    65	
    66	Create the artifacts in this order. Each later step depends on the earlier
    67	artifact contract.
    68	
    69	### 1. Source Preflight
    70	
    71	Check `inputs/contract.txt` before analysis:
    72	
    73	- real clause numbering is present;
    74	- deep clause numbers are not visibly collapsed or shifted;
    75	- repeated locators have enough context to distinguish source rows;
    76	- text is readable and not corrupted by encoding.
    77	
    78	If the contract text is not usable, stop and write
    79	`/outputs/working/source_preflight_error.json`. Do not run legal analysis on
    80	invalid text.
    81	
    82	### 2. Clause Index
    83	
    84	Create `/outputs/working/clause_index.json`.
    85	
    86	It is a source map only. It must include:
    87	
    88	- every matrix `number`;
    89	- every contract clause, operative parent, definition, appendix/table row, and
    90	  unnumbered operative provision;
    91	- source text or source locator for each row;
    92	- context for duplicate printed contract ids.
    93	
    94	Do not use `clause_index` to decide legal status. It only proves source
    95	coverage and valid ids. Never overwrite it with a batch subset.
    96	
    97	Also create `/outputs/working/contract_locator_registry.json` from the same
    98	source map. It is the closed list of source locators. Final `contract_id`
    99	values may use only registry rows with `final_allowed = true`. Appendix starts,
   100	table anchors, and unnumbered source anchors may be `evidence_only`; cite them
   101	through `evidence_locators`, not as final `contract_id` values.
   102	
   103	### 3. Legal Proposition Ledger
   104	
   105	Create `/outputs/working/legal_propositions.json`.
   106	
   107	This is the mandatory legal evidence ledger. It must contain `matrix` and
   108	`contract` arrays. Every evaluable proposition should include:
   109	
   110	- `id`: matrix number or printed contract locator;
   111	- `source_text`: text used for legal comparison;
   112	- `source_excerpt`: short quote supporting the normalized proposition;
   113	- `type`: `operative`, `definition`, `heading`, `parent_framework`,
   114	  `appendix`, `table`, or `technical`;
   115	- `materiality`: `evaluable`, `not_material`, `heading`, or `needs_source_review`;
   116	- `protected_party`, `bound_party`;
   117	- `right_or_obligation`;
   118	- `legal_object`;
   119	- `trigger`;
   120	- `deadline`;
   121	- `amount_formula_cap`;
   122	- `procedure_channel`;
   123	- `liability_remedy`;
   124	- `scope_options`;
   125	- `consequence`;
   126	- `applicability_filters` where available.
   127	
   128	If a legally meaningful row cannot be normalized, mark it
   129	`needs_source_review` and explain the missing element. It is not fully
   130	processed until the source text has been reviewed. Do not proceed to final
   131	matching with unresolved source-review rows that could affect status.
   132	
   133	The ledger is an evidence table, not a substitute for the source. Matching may
   134	use it to find candidates. Status must still be confirmed against source text.
   135	
   136	Run the mechanical check before matching:
   137	
   138	```bash
   139	python skills/acquiring-discrepancy-analysis/scripts/validate_working_artifacts.py --matrix inputs/matrix.json --contract inputs/contract.txt --working outputs/working
   140	```
   141	
   142	Fix invalid working artifacts before delegating comparison work.
   143	When delegating, follow `references/delegation-contract.md`. Validate every
   144	subagent fragment before merge:
   145	
   146	```bash
   147	python skills/acquiring-discrepancy-analysis/scripts/validate_fragment.py <fragment-path> --registry outputs/working/contract_locator_registry.json
   148	```
   149	
   150	### 4. Contract Product Profile
   151	
   152	Create `/outputs/working/contract_product_profile.json`.
   153	
   154	Extract from the contract:
   155	
   156	- product and payment channels;
   157	- lot/procurement type;
   158	- terminal/payment-device scope;
   159	- payment methods;
   160	- legal regime (`44_fz`, `223_fz`, `commercial`, `common`, or `unknown`).
   161	
   162	Apply matrix filters before status:
   163	
   164	- `common` applies to every contract.
   165	- A filtered matrix item applies only when the profile matches
   166	  `only_for_product`, `only_for_lot`, `only_for_terminal`, or `payment_method`.
   167	- Mandatory applicable missing = high risk.
   168	- Out-of-scope / non-applicable matrix items are not final risks. Close them in
   169	  `coverage_ledger.matrix` as `out_of_scope` or `not_applicable` with a short
   170	  profile-based reason. Do not put them in final `unmatched_matrix`.
   171	- Optional applicable missing = low or conditional risk.
   172	- Slash-separated alternatives are options unless the matrix says all options
   173	  are mandatory.
   174	- Placeholder or blank in an applicable material term = low-risk `deviation`.
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
   193	## Bidirectional Matching
   194	
   195	Perform both directions.
   196	
   197	Matrix to contract:
   198	
   199	- for each applicable evaluable matrix proposition, retrieve all contract
   200	  clauses that collectively cover the Bank-standard requirement;
   201	- include parent, child, appendix, payment, procedure, liability, and framework
   202	  clauses only when they provide material coverage or legally cure a gap.
   203	- if a child clause is selected, check whether its parent carries operative
   204	  legal meaning for the same topic; if a parent is selected, check whether its
   205	  children contain the material elements;
   206	- for payment, acceptance, liability, termination, and document-exchange
   207	  requirements, keep the legal package together: operative clause, basis,
   208	  deadline, procedure, remedy, consequence, and any incorporated appendix/table
   209	  row that changes coverage;
   210	- a framework or legal-compliance clause may be a standalone analogue only when
   211	  it carries the same legal object or allocates the same risk, duty, or remedy.
   212	
   213	Contract to matrix:
   214	
   215	- for each evaluable contract proposition, find the matrix analogue group;
   216	- if none exists and the term has independent legal effect, classify it as
   217	  `extra_in_contract`;
   218	- if it is non-operative, close it as `not_material` only in the ledger.
   219	
   220	Group related ids into many-to-many `links`. One matrix id may need several
   221	contract clauses. One contract clause may cover several matrix ids.
   222	
   223	### Uncovered Element Closure Rule
   224	
   225	For every applicable evaluable matrix item, identify the material provisions
   226	that must be covered: party, legal object, duty/right, trigger, deadline,
   227	amount, formula, cap, penalty, scope, procedure, channel, liability, remedy,
   228	exception, and consequence.
   229	
   230	If any material provision remains uncovered after the first candidates are
   231	found, continue candidate search across the full contract index before
   232	finalizing status. This rule applies to both `missing_in_contract` and
   233	`deviation`.
   234	
   235	Document the closure for each final matrix-side finding:
   236	
   237	- `covered_elements`: provisions actually covered by final contract candidates;
   238	- `uncovered_elements`: provisions still missing, changed, narrowed, or
   239	  weakened;
   240	- `candidate_contract_ids`: contract clauses accepted as true analogues or
   241	  package candidates;
   242	- `rejected_contract_ids`: clauses reviewed but rejected, with short legal
   243	  reasons;
   244	- `candidate_search_exhausted`: `true` only after all contract clauses have
   245	  been checked through `clause_index` / `legal_propositions`;
   246	- `search_scope`: `full_contract`, `targeted_domain`, or `not_completed`.
   247	- `evidence_locators`: registry evidence-only anchors, if a cited appendix or
   248	  table supports the source evidence but is not itself a final contract clause.
   249	
   250	Status rules for the closure:
   251	
   252	- `aligned` is allowed only when `uncovered_elements` is empty.
   253	- `deviation` is allowed only when true analogue candidates exist and the
   254	  remaining changed/missing provisions were not cured by any other contract
   255	  clause after a full-contract sweep.
   256	- `missing_in_contract` is allowed only when the full-contract sweep found no
   257	  true analogue.
   258	- `candidate_search_exhausted = false` or `search_scope = not_completed` means
   259	  the matrix item is not ready for final output.
   260	
   261	Keep the sweep efficient. Use `clause_index` and `legal_propositions` to scan
   262	all clauses. Re-read source text only for plausible candidates, hard terms, and
   263	rejected clauses whose legal object is close enough to need explanation.
   264	
   265	## Group-Level Status
   266	
   267	Assign status to the group, not to each atomic pair.
   268	
   269	- `aligned`: the contract package preserves the matrix legal result.
   270	- `deviation`: a true analogue exists, but any material element is changed,
   271	  narrowed, weakened, omitted, shifted, or blank.
   272	- `missing_in_contract`: no true contract analogue exists for an applicable
   273	  matrix requirement.
   274	- `extra_in_contract`: a legally meaningful contract proposition has no matrix
   275	  analogue.
   276	- `not_material`: internal ledger closure only; exclude from final report.
   277	- `out_of_scope` / `not_applicable`: internal matrix closure only; exclude from
   278	  final report because the requirement does not apply to the current product,
   279	  lot, terminal, payment method, or legal regime.
   280	
   281	Material elements include party, legal object, operative act, trigger,
   282	deadline, amount, formula, cap, penalty, scope, procedure, channel, liability,
   283	remedy, exception, Bank right, merchant duty, and consequence.
   284	
   285	Hard terms must be compared directly:
   286	
   287	- same material deadline/amount/procedure in the same legal obligation can be
   288	  `aligned`;
   289	- changed value or missing value is `deviation`;
   290	- a hard term from another clause counts only when that clause expressly
   291	  governs the same obligation or is explicitly incorporated;
   292	- a neighboring date, amount, or procedure for another legal object cannot cure
   293	  the gap.
   294	
   295	Do not downgrade for formal differences alone: heading, title, appendix label,
   296	permitted option selection, equivalent mandatory-law mechanism, or wording
   297	style.
   298	
   299	Do not downgrade for low-risk notes when the legal result is preserved. If the
   300	reason says the difference is merely terminological, beneficial to the Bank,
   301	already incorporated through another clause, or caused only by a mandatory
   302	44-FZ/EIS mechanism that preserves the Bank's practical right, keep `aligned`.
   303	
   304	44-FZ/EIS procedure is not a deviation by itself. It becomes `deviation` only
   305	when it materially worsens or changes a Bank-standard term: payment timing,
   306	acceptance control, withholding right, penalty/cap, termination power, protected
   307	party, evidence channel, or enforceability.
   308	
   309	Liability, penalty, cap, and remedy provisions must be reviewed as a group.
   310	Before marking a liability group `aligned`, check the amount, formula, cap,
   311	trigger, protected party, excluded delay/non-delay buckets, and claim procedure
   312	across the whole package.
   313	
   314	## Risk Calibration
   315	
   316	Use `risk_level` consistently:
   317	
   318	- `none`: only for `aligned`;
   319	- `low`: optional applicable missing, placeholder, formal but legally manageable
   320	  gap;
   321	- `medium`: material deviation that can affect performance, evidence, payment,
   322	  control, liability, or enforceability;
   323	- `high`: mandatory missing, changed protected party, major payment/remedy
   324	  change, important Bank right omitted, or broad contract-only risk.
   325	
   326	Every `deviation`, `missing_in_contract`, and `extra_in_contract` must include
   327	a short evidence-based reason. Use concise quotes rather than long excerpts.
   328	
   329	## Final QA
   330	
   331	Before writing final artifacts:
   332	
   333	- verify `clause_index` covers all source ids;
   334	- verify `legal_proposition_ledger` has no unresolved
   335	  `needs_source_review` rows that can affect final status;
   336	- verify every matrix id is closed as `linked`, `missing_in_contract`,
   337	  `out_of_scope`, `not_applicable`, or source-based `not_evaluable` in
   338	  `coverage_ledger`;
   339	- verify every applicable evaluable matrix id is linked or in
   340	  `unmatched_matrix`;
   341	- verify every final matrix-side link or missing row has exhausted candidate
   342	  search evidence: covered/uncovered elements, accepted candidates, rejected
   343	  close candidates, and `candidate_search_exhausted = true`;
   344	- verify out-of-scope / non-applicable matrix ids are not in final
   345	  `unmatched_matrix`;
   346	- verify every material contract id is closed as linked or extra;
   347	- verify `coverage_ledger` is derived from final `links`,
   348	  `unmatched_matrix`, and `unmatched_contract`;
   349	- verify every final id is visible in source text;
   350	- verify `aligned` has no material discrepancy;
   351	- verify every `deviation` has a named legal gap and evidence;
   352	- verify weak candidates are not in final `links`;
   353	- verify non-material contract rows are absent from final `unmatched_contract`;
   354	- verify summary counts equal final arrays.
   355	
   356	## Output Discipline
   357	
   358	Follow `references/output-contract.md`.
   359	
   360	Final contract locators are closed-class values. Do not invent corrected,
   361	translated, parenthetical, semantic, or derived appendix ids such as
   362	`Приложение_1_п5`. If the source location is an appendix/table anchor rather
   363	than a contract clause, put it in `evidence_locators` and link the nearest real
   364	final-allowed contract clause only when it provides material coverage.
   365	
   366	The final JSON must contain:
   367	
   368	- `analysis_profile`
   369	- `links`
   370	- `atomic_links`
   371	- `unmatched_matrix`
   372	- `unmatched_contract`
   373	- `coverage_ledger`
   374	- `summary`
   375	
   376	`links` carry group-level legal findings. `atomic_links` are traceability
   377	projections only and must inherit the group relationship. Do not assign
   378	separate final pair-level statuses.
   379	
   380	## Tools And Scripts
   381	
   382	Use helper scripts for mechanical work: source extraction, indexing,
   383	normalization checks, batch completeness, coverage validation, JSON schema
   384	checks, and Excel export. Do not put legal mapping or status decisions into
   385	hardcoded scripts.
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
   101	    "source_text": "банк-эмитент – кредитная организация, являющаяся участником платежной системы и осуществляющая эмиссию карт;",
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
AI: Let me continue reading the remaining files needed.[{'name': 'read_file', 'args': {'file_path': '/outputs/working/contract_locator_registry.json', 'offset': 500, 'limit': 500}, 'id': 'call_00_gzKGpyTNV0LXbY9shOFf5854', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'offset': 500, 'limit': 500}, 'id': 'call_01_fGICrOgT8riIaC42adUw0161', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/outputs/working/legal_propositions.json', 'limit': 500}, 'id': 'call_02_Gp8TDYCglfniqfbhMCIi9389', 'type': 'tool_call'}]
Tool:    501	    "line_end": 49,
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
   601	  },
   602	  {
   603	    "locator": "4.2",
   604	    "type": "operative",
   605	    "source_text": "В случае если действующим законодательством Российской Федерации и извещением о проведении закупки предусмотрены требования, предъявляемые к лицам, оказывающим услуги, составляющие предмет настоящего контракта (объект закупки), Исполнитель должен соответствовать таким требованиям. Исполнитель должен иметь лицензию на осуществление банковских операций, соответствующих виду предмета контракта (основание: Федеральный закон от 02.12.1990 N 395-1 \"О банках и банковской деятельности\"), за исключением случая, указанного в части 9 статьи 13 Федерального закона от 02.12.1990 № 395-1 «О банках и банковской деятельности» и в Федеральном законе «О национальной платежной системе».",
   606	    "source_excerpt": "В случае если действующим законодательством Российской Федерации и извещением о проведении закупки предусмотрены требования, предъявляемые к лицам, оказывающим услуги, составляющие предмет настоящего контракта (объект закупки), Исполнитель ",
   607	    "source_locator": "4.2",
   608	    "line_start": 64,
   609	    "line_end": 65,
   610	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   611	    "final_allowed": true,
   612	    "evidence_only": false
   613	  },
   614	  {
   615	    "locator": "4.3",
   616	    "type": "operative",
   617	    "source_text": "Оказание услуг осуществляется Исполнителем по адресу местоположения точек приема к оплате пластиковых карт (эквайринга) торгово-сервисных точек (ТСТ). Перечень ТСТ указан в Приложении № 1. В целях регистрации нового ТСТ в рамках настоящего контракта Заказчик после заключения контракта предоставляет Исполнителю заявление Заказчика на проведение расчетов по операциям с использованием банковских карт и информацию о ТСТ Заказчика/изменение информации о ТСТ заказчика, подписанную уполномоченным представителем заказчика.",
   618	    "source_excerpt": "Оказание услуг осуществляется Исполнителем по адресу местоположения точек приема к оплате пластиковых карт (эквайринга) торгово-сервисных точек (ТСТ). Перечень ТСТ указан в Приложении № 1. В целях регистрации нового ТСТ в рамках настоящего ",
   619	    "source_locator": "4.3",
   620	    "line_start": 66,
   621	    "line_end": 67,
   622	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   623	    "final_allowed": true,
   624	    "evidence_only": false
   625	  },
   626	  {
   627	    "locator": "4.4",
   628	    "type": "operative",
   629	    "source_text": "Оплата по контракту осуществляется по безналичному расчёту платёжным поручением путём перечисления Заказчиком денежных средств на счёт Исполнителя, указанный в настоящем контракте. В случае изменения счета Исполнителя он обязан в двухдневный срок в письменной форме сообщить об этом Заказчику с указанием новых реквизитов расчётного счёта. В противном случае все риски, связанные с перечислением Заказчиком денежных средств на указанный в настоящем контракте счёт Исполнителя, несёт Исполнитель. Оплата оказанной услуги осуществляется по цене единицы услуги исходя из объема фактически оказанной услуги, но в размере, не превышающем максимального значения цены контракта.",
   630	    "source_excerpt": "Оплата по контракту осуществляется по безналичному расчёту платёжным поручением путём перечисления Заказчиком денежных средств на счёт Исполнителя, указанный в настоящем контракте. В случае изменения счета Исполнителя он обязан в двухдневны",
   631	    "source_locator": "4.4",
   632	    "line_start": 68,
   633	    "line_end": 69,
   634	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   635	    "final_allowed": true,
   636	    "evidence_only": false
   637	  },
   638	  {
   639	    "locator": "4.5",
   640	    "type": "operative",
   641	    "source_text": "Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг и производится ежемесячно.",
   642	    "source_excerpt": "Срок оплаты оказанных услуг составляет не более 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг и производится ежемесячно.",
   643	    "source_locator": "4.5",
   644	    "line_start": 70,
   645	    "line_end": 70,
   646	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   647	    "final_allowed": true,
   648	    "evidence_only": false
   649	  },
   650	  {
   651	    "locator": "4.5.1",
   652	    "type": "operative",
   653	    "source_text": "Услуги, оказанные в ноябре оплачиваются в срок не позднее 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг, но не позднее 30 декабря 2025 года.",
   654	    "source_excerpt": "Услуги, оказанные в ноябре оплачиваются в срок не позднее 7 (семи) рабочих дней с даты подписания Заказчиком документа о приемке оказанных услуг, но не позднее 30 декабря 2025 года.",
   655	    "source_locator": "4.5.1",
   656	    "line_start": 71,
   657	    "line_end": 71,
   658	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   659	    "final_allowed": true,
   660	    "evidence_only": false
   661	  },
   662	  {
   663	    "locator": "5",
   664	    "type": "operative",
   665	    "source_text": "ОБЯЗАТЕЛЬСТВА СТОРОН",
   666	    "source_excerpt": "ОБЯЗАТЕЛЬСТВА СТОРОН",
   667	    "source_locator": "5",
   668	    "line_start": 72,
   669	    "line_end": 72,
   670	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   671	    "final_allowed": true,
   672	    "evidence_only": false
   673	  },
   674	  {
   675	    "locator": "5.1",
   676	    "type": "operative",
   677	    "source_text": "Исполнитель обязуется:",
   678	    "source_excerpt": "Исполнитель обязуется:",
   679	    "source_locator": "5.1",
   680	    "line_start": 73,
   681	    "line_end": 73,
   682	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   683	    "final_allowed": true,
   684	    "evidence_only": false
   685	  },
   686	  {
   687	    "locator": "5.1.1",
   688	    "type": "operative",
   689	    "source_text": "Установить Заказчику и подготовить к эксплуатации Электронные терминалы для проведения операций в течение 5 (пяти) рабочих дней с даты подписания контракта. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными материалами, предоставленными Банком. Разместить на сайте: ___________________ обучающие материалы для прохождения инструктажа сотрудниками Заказчика.",
   690	    "source_excerpt": "Установить Заказчику и подготовить к эксплуатации Электронные терминалы для проведения операций в течение 5 (пяти) рабочих дней с даты подписания контракта. Провести первичный инструктаж работников ТСТ в соответствии с инструктивными матери",
   691	    "source_locator": "5.1.1",
   692	    "line_start": 74,
   693	    "line_end": 74,
   694	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   695	    "final_allowed": true,
   696	    "evidence_only": false
   697	  },
   698	  {
   699	    "locator": "5.1.2",
   700	    "type": "operative",
   701	    "source_text": "Ежемесячно формировать и направлять Заказчику документ о приемке в соответствии с пунктами 8.3.1 и 8.3.2. Контракта.",
   702	    "source_excerpt": "Ежемесячно формировать и направлять Заказчику документ о приемке в соответствии с пунктами 8.3.1 и 8.3.2. Контракта.",
   703	    "source_locator": "5.1.2",
   704	    "line_start": 75,
   705	    "line_end": 75,
   706	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   707	    "final_allowed": true,
   708	    "evidence_only": false
   709	  },
   710	  {
   711	    "locator": "5.1.3",
   712	    "type": "operative",
   713	    "source_text": "Обеспечить соответствие оказанных услуг предъявляемым к ним требованиям законодательства Российской Федерации.",
   714	    "source_excerpt": "Обеспечить соответствие оказанных услуг предъявляемым к ним требованиям законодательства Российской Федерации.",
   715	    "source_locator": "5.1.3",
   716	    "line_start": 76,
   717	    "line_end": 76,
   718	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   719	    "final_allowed": true,
   720	    "evidence_only": false
   721	  },
   722	  {
   723	    "locator": "5.1.4",
   724	    "type": "operative",
   725	    "source_text": "Обеспечивать круглосуточную работоспособность Электронных терминалов. В случае выхода из строя Электронного терминала, обеспечить Заказчика исправным Электронным терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Исполнителем заявки от Заказчикам по номеру службы поддержки Банка.",
   726	    "source_excerpt": "Обеспечивать круглосуточную работоспособность Электронных терминалов. В случае выхода из строя Электронного терминала, обеспечить Заказчика исправным Электронным терминалом Банка не позднее 3 (трех) рабочих дней с даты получения Исполнителе",
   727	    "source_locator": "5.1.4",
   728	    "line_start": 77,
   729	    "line_end": 77,
   730	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   731	    "final_allowed": true,
   732	    "evidence_only": false
   733	  },
   734	  {
   735	    "locator": "5.1.5",
   736	    "type": "operative",
   737	    "source_text": "Предоставлять Заказчику полную и точную информацию об услугах, а также о ходе исполнения своих обязательств по настоящему контракту, в том числе о сложностях, возникающих при исполнении контракта.",
   738	    "source_excerpt": "Предоставлять Заказчику полную и точную информацию об услугах, а также о ходе исполнения своих обязательств по настоящему контракту, в том числе о сложностях, возникающих при исполнении контракта.",
   739	    "source_locator": "5.1.5",
   740	    "line_start": 78,
   741	    "line_end": 78,
   742	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   743	    "final_allowed": true,
   744	    "evidence_only": false
   745	  },
   746	  {
   747	    "locator": "5.1.6",
   748	    "type": "operative",
   749	    "source_text": "Осуществлять круглосуточную авторизацию;",
   750	    "source_excerpt": "Осуществлять круглосуточную авторизацию;",
   751	    "source_locator": "5.1.6",
   752	    "line_start": 79,
   753	    "line_end": 79,
   754	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   755	    "final_allowed": true,
   756	    "evidence_only": false
   757	  },
   758	  {
   759	    "locator": "5.1.7",
   760	    "type": "operative",
   761	    "source_text": "Обеспечивать электронные терминалы, установленные у заказчика/ТСТ, рекламно-информационными материалами, необходимыми для проведения операций с использованием карт;",
   762	    "source_excerpt": "Обеспечивать электронные терминалы, установленные у заказчика/ТСТ, рекламно-информационными материалами, необходимыми для проведения операций с использованием карт;",
   763	    "source_locator": "5.1.7",
   764	    "line_start": 80,
   765	    "line_end": 80,
   766	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   767	    "final_allowed": true,
   768	    "evidence_only": false
   769	  },
   770	  {
   771	    "locator": "5.1.8",
   772	    "type": "operative",
   773	    "source_text": "На основании полученной от Заказчика расчетной информации, переданной от Электронного терминала Исполнителю, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный (текущий) счет Заказчика суммы Операций оплаты в валюте проведения операции (рубли РФ). Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов. В случае технического сбоя при передаче Электронной сверки итогов/ невозможности проведения Предприятием/ТСТ или отсутствия Электронной сверки итогов по иным причинам, перечислять Заказчику суммы Операций, по истечении 3 (трех) календарных дней с момента последней Электронной сверки итогов, проводить расчеты по всем Операциям с данной ТСТ;",
   774	    "source_excerpt": "На основании полученной от Заказчика расчетной информации, переданной от Электронного терминала Исполнителю, не позднее 2 (двух) рабочих дней с даты получения расчетной информации Исполнителю перечислять на расчетный (текущий) счет Заказчик",
   775	    "source_locator": "5.1.8",
   776	    "line_start": 81,
   777	    "line_end": 83,
   778	    "section_context": "• п. 2.3.7. Контракта – в дату обращения в службу поддержки Банка",
   779	    "final_allowed": true,
   780	    "evidence_only": false
   781	  },
   782	  {
   783	    "locator": "5.1.9",
   784	    "type": "operative",
   785	    "source_text": "Осуществлять обработку персональных данных, полученных от заказчика, а также обеспечить конфиденциальность и защиту обрабатываемых персональных данных в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональных данных» (далее – Закона 152-ФЗ). Принимать необходимые правовые, организационные и технические меры или обеспечивать их принятие для защиты получаемых от заказчика персональных данных от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения персональных данных, а также от иных неправомерных действий в отношении получаемых от заказчика персональных данных.",
   786	    "source_excerpt": "Осуществлять обработку персональных данных, полученных от заказчика, а также обеспечить конфиденциальность и защиту обрабатываемых персональных данных в соответствии с требованиями Федерального закона от 27 июля 2006 № 152-ФЗ «О персональны",
   787	    "source_locator": "5.1.9",
   788	    "line_start": 84,
   789	    "line_end": 84,
   790	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   791	    "final_allowed": true,
   792	    "evidence_only": false
   793	  },
   794	  {
   795	    "locator": "5.1.10",
   796	    "type": "operative",
   797	    "source_text": "Исполнитель в соответствии с контрактом перечисляет Заказчику суммы операций оплаты услуг, совершенных на предприятии Заказчика/торгово-сервисных точках (ТСТ) с использованием карт.",
   798	    "source_excerpt": "Исполнитель в соответствии с контрактом перечисляет Заказчику суммы операций оплаты услуг, совершенных на предприятии Заказчика/торгово-сервисных точках (ТСТ) с использованием карт.",
   799	    "source_locator": "5.1.10",
   800	    "line_start": 85,
   801	    "line_end": 85,
   802	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   803	    "final_allowed": true,
   804	    "evidence_only": false
   805	  },
   806	  {
   807	    "locator": "5.2",
   808	    "type": "operative",
   809	    "source_text": "Исполнитель вправе:",
   810	    "source_excerpt": "Исполнитель вправе:",
   811	    "source_locator": "5.2",
   812	    "line_start": 86,
   813	    "line_end": 86,
   814	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   815	    "final_allowed": true,
   816	    "evidence_only": false
   817	  },
   818	  {
   819	    "locator": "5.2.1",
   820	    "type": "operative",
   821	    "source_text": "Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате стоимости услуг по настоящему контракту.",
   822	    "source_excerpt": "Требовать от Заказчика своевременного исполнения обязательств по приемке и оплате стоимости услуг по настоящему контракту.",
   823	    "source_locator": "5.2.1",
   824	    "line_start": 87,
   825	    "line_end": 87,
   826	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   827	    "final_allowed": true,
   828	    "evidence_only": false
   829	  },
   830	  {
   831	    "locator": "5.2.2",
   832	    "type": "operative",
   833	    "source_text": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств.",
   834	    "source_excerpt": "Принять решение об одностороннем отказе от исполнения контракта по основаниям, предусмотренным Федеральным законом № 44-ФЗ, ГК РФ для одностороннего отказа от исполнения отдельных видов обязательств.",
   835	    "source_locator": "5.2.2",
   836	    "line_start": 88,
   837	    "line_end": 88,
   838	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   839	    "final_allowed": true,
   840	    "evidence_only": false
   841	  },
   842	  {
   843	    "locator": "5.2.3",
   844	    "type": "operative",
   845	    "source_text": "Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов, расположенных на территории заказчика/ТСТ. Производить замену электронных терминалов, а также обновлять программное обеспечение электронного терминала, уведомив заказчика не менее чем за два рабочих дня до даты замены или обновления;",
   846	    "source_excerpt": "Осуществлять проверку технического состояния и порядка эксплуатации электронных терминалов, расположенных на территории заказчика/ТСТ. Производить замену электронных терминалов, а также обновлять программное обеспечение электронного термина",
   847	    "source_locator": "5.2.3",
   848	    "line_start": 89,
   849	    "line_end": 89,
   850	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   851	    "final_allowed": true,
   852	    "evidence_only": false
   853	  },
   854	  {
   855	    "locator": "5.2.4",
   856	    "type": "operative",
   857	    "source_text": "Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций;",
   858	    "source_excerpt": "Допускается осуществлять удаленное обновление программного обеспечения, не затрагивающее порядок проведения операций;",
   859	    "source_locator": "5.2.4",
   860	    "line_start": 90,
   861	    "line_end": 90,
   862	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   863	    "final_allowed": true,
   864	    "evidence_only": false
   865	  },
   866	  {
   867	    "locator": "5.2.5",
   868	    "type": "operative",
   869	    "source_text": "Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции. Для анализа спорных ситуаций исполнитель также может потребовать от заказчика предоставления копии контрольной ленты, письменного заявления заказчика с изложением обстоятельств проведения операции, счетов за предоставленные товары/услуги, товарные или кассовые чеки и другие документы, необходимые для проведения анализа обстоятельств проведения операции или претензионной работы;",
   870	    "source_excerpt": "Запрашивать документы по операциям не позднее тринадцати месяцев с даты совершения операции. Для анализа спорных ситуаций исполнитель также может потребовать от заказчика предоставления копии контрольной ленты, письменного заявления заказчи",
   871	    "source_locator": "5.2.5",
   872	    "line_start": 91,
   873	    "line_end": 91,
   874	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   875	    "final_allowed": true,
   876	    "evidence_only": false
   877	  },
   878	  {
   879	    "locator": "5.2.6",
   880	    "type": "operative",
   881	    "source_text": "В случае изменения реквизитов исполнителя, указанных в контракте, уведомить об этом заказчика в письменном виде путем направления информации в адрес заказчика в течение трех рабочих дней;",
   882	    "source_excerpt": "В случае изменения реквизитов исполнителя, указанных в контракте, уведомить об этом заказчика в письменном виде путем направления информации в адрес заказчика в течение трех рабочих дней;",
   883	    "source_locator": "5.2.6",
   884	    "line_start": 92,
   885	    "line_end": 92,
   886	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   887	    "final_allowed": true,
   888	    "evidence_only": false
   889	  },
   890	  {
   891	    "locator": "5.2.7",
   892	    "type": "operative",
   893	    "source_text": "В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении заказчика на проведение расчетов по операциям с использованием банковских карт/информации о ТСТ;",
   894	    "source_excerpt": "В целях получения информации по операциям направлять запросы на адрес электронной почты заказчика/ТСТ, указанный в заявлении заказчика на проведение расчетов по операциям с использованием банковских карт/информации о ТСТ;",
   895	    "source_locator": "5.2.7",
   896	    "line_start": 93,
   897	    "line_end": 93,
   898	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   899	    "final_allowed": true,
   900	    "evidence_only": false
   901	  },
   902	  {
   903	    "locator": "5.2.8",
   904	    "type": "operative",
   905	    "source_text": "Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.",
   906	    "source_excerpt": "Требовать от заказчика предоставления документов и сведений, необходимых для осуществления функций, предусмотренных требованиями действующего законодательства.",
   907	    "source_locator": "5.2.8",
   908	    "line_start": 94,
   909	    "line_end": 94,
   910	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   911	    "final_allowed": true,
   912	    "evidence_only": false
   913	  },
   914	  {
   915	    "locator": "5.2.9",
   916	    "type": "operative",
   917	    "source_text": "В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению Контракта при наступлении следующих событий:",
   918	    "source_excerpt": "В одностороннем порядке приостановить Авторизации для ТСТ и/или провести мероприятия по расторжению Контракта при наступлении следующих событий:",
   919	    "source_locator": "5.2.9",
   920	    "line_start": 95,
   921	    "line_end": 95,
   922	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   923	    "final_allowed": true,
   924	    "evidence_only": false
   925	  },
   926	  {
   927	    "locator": "5.2.9.1",
   928	    "type": "operative",
   929	    "source_text": "нарушение Заказчиком условий Контракта;",
   930	    "source_excerpt": "нарушение Заказчиком условий Контракта;",
   931	    "source_locator": "5.2.9.1",
   932	    "line_start": 96,
   933	    "line_end": 96,
   934	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   935	    "final_allowed": true,
   936	    "evidence_only": false
   937	  },
   938	  {
   939	    "locator": "5.2.9.2",
   940	    "type": "operative",
   941	    "source_text": "внесение данных Заказчика в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;",
   942	    "source_excerpt": "внесение данных Заказчика в перечень организаций и физических лиц, в отношении которых имеются сведения об их причастности к экстремистской деятельности, терроризму или финансированию распространения оружия массового уничтожения;",
   943	    "source_locator": "5.2.9.2",
   944	    "line_start": 97,
   945	    "line_end": 97,
   946	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   947	    "final_allowed": true,
   948	    "evidence_only": false
   949	  },
   950	  {
   951	    "locator": "5.2.9.3",
   952	    "type": "operative",
   953	    "source_text": "при наличии у Исполнителя подозрений, что Операции в ТСТ совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;",
   954	    "source_excerpt": "при наличии у Исполнителя подозрений, что Операции в ТСТ совершаются в целях легализации (отмывания) доходов, полученных преступным путем, или финансирования терроризма;",
   955	    "source_locator": "5.2.9.3",
   956	    "line_start": 98,
   957	    "line_end": 98,
   958	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   959	    "final_allowed": true,
   960	    "evidence_only": false
   961	  },
   962	  {
   963	    "locator": "5.2.9.4",
   964	    "type": "operative",
   965	    "source_text": "получение негативной информации о Заказчике/ТСТ от органов государственной власти РФ и/или Платежных систем;",
   966	    "source_excerpt": "получение негативной информации о Заказчике/ТСТ от органов государственной власти РФ и/или Платежных систем;",
   967	    "source_locator": "5.2.9.4",
   968	    "line_start": 99,
   969	    "line_end": 99,
   970	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   971	    "final_allowed": true,
   972	    "evidence_only": false
   973	  },
   974	  {
   975	    "locator": "5.2.9.5",
   976	    "type": "operative",
   977	    "source_text": "получение информации о мошенничестве в ТСТ стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных систем, полученные c использованием факсимильной связи, по электронной почте (e-mail);",
   978	    "source_excerpt": "получение информации о мошенничестве в ТСТ стороны договорились, что достаточным подтверждением мошеннического характера проведенных Операций является информация, поступившая от Банков-эмитентов Исполнителю, или уведомления от Платежных сис",
   979	    "source_locator": "5.2.9.5",
   980	    "line_start": 100,
   981	    "line_end": 101,
   982	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   983	    "final_allowed": true,
   984	    "evidence_only": false
   985	  },
   986	  {
   987	    "locator": "5.2.9.6",
   988	    "type": "operative",
   989	    "source_text": "осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций;",
   990	    "source_excerpt": "осуществление ремонта помещений ТСТ, препятствующее осуществлению Операций;",
   991	    "source_locator": "5.2.9.6",
   992	    "line_start": 102,
   993	    "line_end": 102,
   994	    "section_context": "Датой получения расчетной информации Исполнителем является дата рабочего дня, следующего за днем совершения операции Электронной сверки итогов.",
   995	    "final_allowed": true,
   996	    "evidence_only": false
   997	  },
   998	  {
   999	    "locator": "5.2.9.7",
  1000	    "type": "operative",
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
Tool:      1	{
     2	  "matrix": [
     3	    {
     4	      "id": "2.1",
     5	      "source_text": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предоставляет заявление на расчеты и информацию о ТСТ, подписанное уполномоченным лицом; Банк может отказать в регистрации ТСТ без указания причины; Предприятие обязано предоставить обновленную информацию о ТСТ при ее изменении; Информация о новых устройствах предоставляется с указанием их количества В целях регистрации новой ТСТ в рамках настоящего Договора Предприятие предоставляет в Банк Заявление Предприятия на проведение расчетов по операциям оплаты товаров/услуг в соответствии с Приложением 1 к настоящему Договору и Информацию о ТСТ Предприятия/изменение информации о ТСТ Предприятия, подписанную уполномоченным представителем Предприятия, по форме Приложения № 1.1 к Договору. Банк вправе отказать в регистрации соответствующей ТСТ без объяснения причин, уведомив об этом Предприятие в соответствии с п. 2.3 Договора. При изменении информации о ТСТ Предприятие предоставляет в Банк в соответствии с п.2.3 Договора Информацию о ТСТ, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия. При подключении дополнительных Электронных терминалов/Смарт-терминалов Банка/при подключении программного обеспечения для дополнительных Смарт-терминалов Предприятия, а также 2D сканера Предприятие предоставляет в Банк в соответствии с п.2.3 настоящего Договора информацию по форме Информация о ТСТ, указанной в Приложении № 1.1 к Договору, оформленную на бумажном носителе или в электронном виде, подписанную уполномоченным представителем Предприятия с указанием количества вновь подключаемых Электронных терминалов/Смарт-терминалов Банка/сканеров.",
     6	      "source_excerpt": "Важен факт, что для регистрации договора банку нужно заявление. В заявлении должна быть указана полная информация необходимая для регистрации договора. Банк имеет право отказать без объяснений Для регистрации новой ТСТ Предприятие предостав",
     7	      "type": "operative",
     8	      "materiality": "evaluable",
     9	      "protected_party": "Bank",
    10	      "bound_party": "Enterprise",
    11	      "right_or_obligation": "right",
    12	      "legal_object": "ТСТ (торгово-сервисная точка)",
    13	      "trigger": "изменение/реорганизация",
    14	      "deadline": "",
    15	      "amount_formula_cap": "согласно Тарифам Банка",
    16	      "procedure_channel": "способы, указанные в п.2.3 Договора",
    17	      "liability_remedy": "",
    18	      "scope_options": [],
    19	      "consequence": "отказ в регистрации/услуге",
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
    41	      "materiality": "evaluable",
    42	      "protected_party": "Bank",
    43	      "bound_party": "Enterprise",
    44	      "right_or_obligation": "duty",
    45	      "legal_object": "Операции оплаты",
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
    71	      "materiality": "evaluable",
    72	      "protected_party": "Bank",
    73	      "bound_party": "Enterprise",
    74	      "right_or_obligation": "duty",
    75	      "legal_object": "ТСТ (торгово-сервисная точка)",
    76	      "trigger": "",
    77	      "deadline": "",
    78	      "amount_formula_cap": "согласно Тарифам Банка",
    79	      "procedure_channel": "электронные каналы связи",
    80	      "liability_remedy": "",
    81	      "scope_options": [],
    82	      "consequence": "признание юридической силы",
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
   103	      "materiality": "evaluable",
   104	      "protected_party": "Bank",
   105	      "bound_party": "Enterprise",
   106	      "right_or_obligation": "duty",
   107	      "legal_object": "Документы по операциям",
   108	      "trigger": "",
   109	      "deadline": "",
   110	      "amount_formula_cap": "",
   111	      "procedure_channel": "система ДБО",
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
   133	      "materiality": "evaluable",
   134	      "protected_party": "both",
   135	      "bound_party": "Enterprise",
   136	      "right_or_obligation": "duty",
   137	      "legal_object": "ТСТ (торгово-сервисная точка)",
   138	      "trigger": "",
   139	      "deadline": "",
   140	      "amount_formula_cap": "согласно Тарифам Банка",
   141	      "procedure_channel": "письмо с доставкой нарочным/курьером",
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
   163	      "materiality": "evaluable",
   164	      "protected_party": "both",
   165	      "bound_party": "Enterprise",
   166	      "right_or_obligation": "duty",
   167	      "legal_object": "ТСТ (торгово-сервисная точка)",
   168	      "trigger": "",
   169	      "deadline": "",
   170	      "amount_formula_cap": "согласно Тарифам Банка",
   171	      "procedure_channel": "заказное письмо",
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
   193	      "materiality": "evaluable",
   194	      "protected_party": "Bank",
   195	      "bound_party": "Enterprise",
   196	      "right_or_obligation": "duty",
   197	      "legal_object": "Документы по операциям",
   198	      "trigger": "",
   199	      "deadline": "",
   200	      "amount_formula_cap": "",
   201	      "procedure_channel": "E-invoicing/СФЕРА-Курьер",
   202	      "liability_remedy": "",
   203	      "scope_options": [],
   204	      "consequence": "признание юридической силы",
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
   224	      "materiality": "evaluable",
   225	      "protected_party": "Bank",
   226	      "bound_party": "Enterprise",
   227	      "right_or_obligation": "duty",
   228	      "legal_object": "Документы по операциям",
   229	      "trigger": "",
   230	      "deadline": "",
   231	      "amount_formula_cap": "",
   232	      "procedure_channel": "электронные каналы связи",
   233	      "liability_remedy": "",
   234	      "scope_options": [],
   235	      "consequence": "признание юридической силы",
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
   255	      "materiality": "evaluable",
   256	      "protected_party": "Bank",
   257	      "bound_party": "Enterprise",
   258	      "right_or_obligation": "duty",
   259	      "legal_object": "ТСТ (торгово-сервисная точка)",
   260	      "trigger": "запрос Банка",
   261	      "deadline": "",
   262	      "amount_formula_cap": "",
   263	      "procedure_channel": "электронные каналы связи",
   264	      "liability_remedy": "ответственность за нарушение",
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
   290	      "materiality": "evaluable",
   291	      "protected_party": "Bank",
   292	      "bound_party": "Enterprise",
   293	      "right_or_obligation": "duty",
   294	      "legal_object": "Документы по операциям",
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
   318	      "materiality": "evaluable",
   319	      "protected_party": "Bank",
   320	      "bound_party": "Enterprise",
   321	      "right_or_obligation": "duty",
   322	      "legal_object": "Операции оплаты",
   323	      "trigger": "подключение",
   324	      "deadline": "",
   325	      "amount_formula_cap": "согласно Тарифам Банка",
   326	      "procedure_channel": "",
   327	      "liability_remedy": "",
   328	      "scope_options": [
   329	        "SberPay",
   330	        "SberPayOnline",
   331	        "Интернет-эквайринг"
   332	      ],
   333	      "consequence": "",
   334	      "applicability_filters": {
   335	        "required_type": "mandatory",
   336	        "only_for_product": "internet_acquiring",
   337	        "only_for_lot": "common",
   338	        "only_for_terminal": "common",
   339	        "payment_method": "common"
   340	      },
   341	      "main_idea": "Важен факт, что бесконтактная оплата подключается автоматически",
   342	      "topics": [
   343	        "SberPayOnline подключается автоматически при подключении Интернет-эквайринга",
   344	        "используется единый тариф по Интернет-эквайрингу"
   345	      ],
   346	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayOnline: → при подключении Интернет-эквайринга SberPayOnline подключается автоматически с применением единого тарифа по Интернет-эквайрингу;"
   347	    },
   348	    {
   349	      "id": "2.5.2.1",
   350	      "source_text": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; наличие документа 'Информация о ТСТ' Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ.",
   351	      "source_excerpt": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением подключение SberPayFaceScan оформляется на бумажном носителе; подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия; н",
   352	      "type": "operative",
   353	      "materiality": "evaluable",
   354	      "protected_party": "Bank",
   355	      "bound_party": "Enterprise",
   356	      "right_or_obligation": "duty",
   357	      "legal_object": "ТСТ (торгово-сервисная точка)",
   358	      "trigger": "",
   359	      "deadline": "",
   360	      "amount_formula_cap": "согласно Тарифам Банка",
   361	      "procedure_channel": "",
   362	      "liability_remedy": "",
   363	      "scope_options": [
   364	        "SberPay",
   365	        "SberPayFaceScan"
   366	      ],
   367	      "consequence": "",
   368	      "applicability_filters": {
   369	        "required_type": "mandatory",
   370	        "only_for_product": "trade_acquiring",
   371	        "only_for_lot": "common",
   372	        "only_for_terminal": "common",
   373	        "payment_method": "sber_pay_face_scan"
   374	      },
   375	      "main_idea": "Важен факт, что возможность принятия оплаты по биометрии оформляется отдельным заявлением",
   376	      "topics": [
   377	        "подключение SberPayFaceScan оформляется на бумажном носителе",
   378	        "подключение SberPayFaceScan требует подписи уполномоченного представителя Предприятия",
   379	        "наличие документа 'Информация о ТСТ'"
   380	      ],
   381	      "enriched_text": "Возможность совершения Операций оплаты с использованием SberPay предоставляется в следующем порядке и на следующих условиях: → SberPayFaceScan: → Подключается дополнительно к Торговому эквайрингу на основании оформленной на бумажном носителе и подписанной уполномоченным представителем Предприятия Информации о ТСТ."
   382	    },
   383	    {
   384	      "id": "2.6.1.1",
   385	      "source_text": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ.",
   386	      "source_excerpt": "Для приема QR на смарт-терминал не нужно отдельное ПО OR-код подключается при установке Смарт-терминала Банка; OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ Возможность совершения Операций оплаты по QR-код",
   387	      "type": "operative",
   388	      "materiality": "evaluable",
   389	      "protected_party": "Bank",
   390	      "bound_party": "Enterprise",
   391	      "right_or_obligation": "duty",
   392	      "legal_object": "ТСТ (торгово-сервисная точка)",
   393	      "trigger": "установка",
   394	      "deadline": "",
   395	      "amount_formula_cap": "согласно Тарифам Банка",
   396	      "procedure_channel": "",
   397	      "liability_remedy": "",
   398	      "scope_options": [
   399	        "Плати QR"
   400	      ],
   401	      "consequence": "",
   402	      "applicability_filters": {
   403	        "required_type": "mandatory",
   404	        "only_for_product": "trade_acquiring",
   405	        "only_for_lot": "common",
   406	        "only_for_terminal": "smart",
   407	        "payment_method": "qr"
   408	      },
   409	      "main_idea": "Для приема QR на смарт-терминал не нужно отдельное ПО",
   410	      "topics": [
   411	        "OR-код подключается при установке Смарт-терминала Банка",
   412	        "OR-код подключается при установке ПО Банка для Смарт-терминала Предприятия в ТСТ"
   413	      ],
   414	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Смарт-терминалов: → ОR-код подключается при установке Смарт-терминала Банка/при установке программного обеспечения Банка для Смарт-терминала Предприятия в ТСТ."
   415	    },
   416	    {
   417	      "id": "2.6.2.1",
   418	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка возможность использования QR-кода на ККТ с собственным ПО Предприятия; подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API); порядок и условия подключения QR-API описаны на Официальном сайте Банка Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;",
   419	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте бан",
   420	      "type": "operative",
   421	      "materiality": "evaluable",
   422	      "protected_party": "Bank",
   423	      "bound_party": "Enterprise",
   424	      "right_or_obligation": "duty",
   425	      "legal_object": "ТСТ (торгово-сервисная точка)",
   426	      "trigger": "подключение",
   427	      "deadline": "",
   428	      "amount_formula_cap": "согласно Тарифам Банка",
   429	      "procedure_channel": "Официальный сайт Банка",
   430	      "liability_remedy": "ответственность за нарушение",
   431	      "scope_options": [
   432	        "Плати QR"
   433	      ],
   434	      "consequence": "",
   435	      "applicability_filters": {
   436	        "required_type": "mandatory",
   437	        "only_for_product": "trade_acquiring",
   438	        "only_for_lot": "common",
   439	        "only_for_terminal": "common",
   440	        "payment_method": "qr"
   441	      },
   442	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре.  Важен факт возможности использовать QR через QR-API. Важен факт, что информация о QR-API - на сайте банка",
   443	      "topics": [
   444	        "возможность использования QR-кода на ККТ с собственным ПО Предприятия",
   445	        "подключение осуществляется через передачу информации от Банка к Предприятию через API (QR-API)",
   446	        "порядок и условия подключения QR-API описаны на Официальном сайте Банка"
   447	      ],
   448	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при наличии у Предприятия собственного программного обеспечения Банк предоставляет возможность использования QR-кода на ККТ посредством передачи Банком Предприятию информации через API (далее − QR-API). Порядок, условия и ответственность сторон при подключении QR-API размещены на Официальном сайте Банка;"
   449	    },
   450	    {
   451	      "id": "2.6.2.2",
   452	      "source_text": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ; подключение динамического QR-кода зависит от ПО ККТ; при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора; первая операция оплаты QR-кодом активирует услугу; Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора; подключение QR-кода производится согласно Приложениям №1 и №1.1 Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору.",
   453	      "source_excerpt": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия возможность проведения операций оплаты по QR-коду на",
   454	      "type": "operative",
   455	      "materiality": "evaluable",
   456	      "protected_party": "Bank",
   457	      "bound_party": "Enterprise",
   458	      "right_or_obligation": "duty",
   459	      "legal_object": "ТСТ (торгово-сервисная точка)",
   460	      "trigger": "",
   461	      "deadline": "",
   462	      "amount_formula_cap": "согласно Тарифам Банка",
   463	      "procedure_channel": "",
   464	      "liability_remedy": "",
   465	      "scope_options": [
   466	        "Плати QR"
   467	      ],
   468	      "consequence": "",
   469	      "applicability_filters": {
   470	        "required_type": "mandatory",
   471	        "only_for_product": "trade_acquiring",
   472	        "only_for_lot": "common",
   473	        "only_for_terminal": "common",
   474	        "payment_method": "qr"
   475	      },
   476	      "main_idea": "ВАЖНО проверить, что в договоре идёт речь о СОБСТВЕННЫХ терминалах Предприятия. Если это не так,то данный риск не содержится в договоре. Важно, что Банк не делает доработок ПО Предприятия",
   477	      "topics": [
   478	        "возможность проведения операций оплаты по QR-коду на электронных терминалах и ККТ",
   479	        "подключение динамического QR-кода зависит от ПО ККТ",
   480	        "при отсутствии своего ПО Предприятие дорабатывает его самостоятельно или через Вендора",
   481	        "первая операция оплаты QR-кодом активирует услугу",
   482	        "Банк передает параметры QR-кода QR-Вендору через API на основе отдельного договора",
   483	        "подключение QR-кода производится согласно Приложениям №1 и №1.1"
   484	      ],
   485	      "enriched_text": "Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов, работающих под управлением ККТ Предприятия, возможны следующие виды подключения динамического QR-кода в зависимости от программного обеспечения ККТ: → при отсутствии у Предприятия собственного программного обеспечения с возможностью подключения QR-кода Предприятие самостоятельно дорабатывает его с привлечением Вендора . Проведение первой Операции оплаты с использованием QR-кода в ТСТ обозначает активацию Предприятием услуги QR-кода.Банк может передавать Вендору параметры формирования QR-кода (далее – QR-Вендор) для дальнейшей передачи его Предприятию, после доработки программного обеспечения для ККТ, через API на основании отдельно заключенного договора с Вендором. Подключение QR-кода (в том числе с подключением через QR-API и/или QR-Вендор) осуществляется на основании Приложения №1 и Приложения №1.1 к настоящему Договору."
   486	    },
   487	    {
   488	      "id": "2.6.3.1",
   489	      "source_text": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-терминалах, Электронных терминалах, ККТ Предприятия предоставляется в следующем порядке и на следующих условиях: → Для Электронных терминалов при подключении на них QR-кода Вендором, которым является Банк: → QR-код подключается при установке Электронного терминала в ТСТ;",
   490	      "source_excerpt": "Данный риск относится только к терминалам предоставленным Банком. Важен факт, что QR подключается сразу при установке QR-код подключается при установке Электронного терминала в ТСТ Возможность совершения Операций оплаты по QR-коду на Смарт-",
   491	      "type": "operative",
   492	      "materiality": "evaluable",
   493	      "protected_party": "Bank",
   494	      "bound_party": "Enterprise",
   495	      "right_or_obligation": "duty",
   496	      "legal_object": "ТСТ (торгово-сервисная точка)",
   497	      "trigger": "подключение",
   498	      "deadline": "",
   499	      "amount_formula_cap": "согласно Тарифам Банка",
   500	      "procedure_channel": "",
AI: Let me continue reading the remaining parts of the contract and the matrix items I need.[{'name': 'read_file', 'args': {'file_path': '/inputs/contract.txt', 'limit': 500}, 'id': 'call_00_HtMGpNUxhKlGlOdnkvE05634', 'type': 'tool_call'}, {'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 500, 'offset': 1000}, 'id': 'call_01_zusSz2n8tAVFY5MVjnIj8539', 'type': 'tool_call'}]
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
Tool:   1001	  "only_for_terminal":"common",
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
AI: I now have a comprehensive understanding of the data. Let me continue reading the remaining matrix items I need for batch 3.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 500, 'offset': 1500}, 'id': 'call_00_vSOzhuUUKWtTcZeHlO0c1660', 'type': 'tool_call'}]
Tool:   1501	  ],
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
  1701	  ],
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
AI: Let me continue reading the remaining matrix items.[{'name': 'read_file', 'args': {'file_path': '/inputs/matrix.json', 'limit': 500, 'offset': 2000}, 'id': 'call_00_Ocz0KFNOakeVCRhUUuOW5963', 'type': 'tool_call'}]
Tool:   2001	  ],
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

