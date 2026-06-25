Ниже README-ready блок.

```mermaid
flowchart TD
    U["User / runner"] --> M["main.py"]

    M --> C["clean_run_outputs()
    clears outputs/ and stray discrepancy_analysis.json"]

    C --> A["Deep Agent: orchestrator"]

    A --> S["Load skill:
    skills/acquiring-discrepancy-analysis/SKILL.md
    + references/output-contract.md
    + references/comparison-patterns.md"]

    A --> I["Build working inventories"]
    I --> MI["/outputs/working/matrix_inventory.json"]
    I --> CI["/outputs/working/contract_inventory.json"]

    MI --> BATCH_SPLIT["Split material matrix ids into 3-5 batches"]
    CI --> BATCH_SPLIT

    BATCH_SPLIT --> B1["Subagent:
    matrix-comparison-batch
    batch 1"]
    BATCH_SPLIT --> B2["Subagent:
    matrix-comparison-batch
    batch 2"]
    BATCH_SPLIT --> B3["Subagent:
    matrix-comparison-batch
    batch N"]

    B1 --> BF1["/outputs/working/batch_1_fragment.json"]
    B2 --> BF2["/outputs/working/batch_2_fragment.json"]
    B3 --> BF3["/outputs/working/batch_N_fragment.json"]

    MI --> CE["Subagent:
    contract-extra-review"]
    CI --> CE
    CE --> CF["/outputs/working/contract_only_findings.json"]

    BF1 --> MERGE["Orchestrator merge"]
    BF2 --> MERGE
    BF3 --> MERGE
    CF --> MERGE

    MERGE --> DRAFT["Draft merged artifact:
    links
    atomic_links
    unmatched_matrix
    unmatched_contract
    summary"]

    DRAFT --> QA["Subagent:
    discrepancy-qa"]

    QA --> QA_REPORT["QA error list:
    schema, ids, coverage,
    empty contract_ids,
    atomic_links,
    summary counts"]

    QA_REPORT --> FIX["Orchestrator correction pass"]
    DRAFT --> FIX

    FIX --> FINAL["/outputs/discrepancy_analysis.json"]

    FINAL --> V["main.py verify_discrepancy_artifact()"]

    V --> OK["Validated final artifact"]
    V --> ERR["RuntimeError if schema / ids / coverage invalid"]
```

```mermaid
sequenceDiagram
    participant Runner as Runner / main.py
    participant O as Orchestrator
    participant Skill as acquiring-discrepancy-analysis skill
    participant MB as matrix-comparison-batch subagents
    participant CE as contract-extra-review subagent
    participant QA as discrepancy-qa subagent
    participant FS as outputs filesystem
    participant Val as verify_discrepancy_artifact

    Runner->>FS: Clear outputs/ and output/
    Runner->>O: Start Deep Agent with USER_PROMPT
    O->>Skill: Read legal methodology and references
    O->>FS: Create /outputs/working/

    O->>FS: Write matrix_inventory.json
    O->>FS: Write contract_inventory.json

    O->>MB: Assign matrix id batches
    MB->>Skill: Apply legal analogue and status rules
    MB->>FS: Write batch fragments with links, atomic_links, unmatched_matrix

    O->>CE: Review full contract inventory for contract-only terms
    CE->>Skill: Apply contract-only materiality rules
    CE->>FS: Write contract_only_findings.json

    O->>FS: Read batch fragments and contract-only findings
    O->>O: Merge graph artifact

    O->>QA: Validate merged artifact
    QA->>FS: Return QA findings / error list

    O->>O: Apply final structural corrections
    O->>FS: Write /outputs/discrepancy_analysis.json

    Runner->>Val: Validate final artifact
    Val->>FS: Check real ids, schema, coverage, summary, atomic links
    Val-->>Runner: Success or RuntimeError
```

**Subagents**

| Subagent | Role | Input | Output |
|---|---|---|---|
| `matrix-comparison-batch` | Сопоставляет assigned matrix ids с договором many-to-many | `matrix_inventory.json`, `contract_inventory.json`, skill refs, batch ids | `links`, `atomic_links`, `unmatched_matrix` для своего batch |
| `contract-extra-review` | Ищет существенные пункты договора без аналога в матрице | полный `contract_inventory.json` + `matrix_inventory.json` | `unmatched_contract`: `extra_in_contract` или `not_material` |
| `discrepancy-qa` | Проверяет структуру, покрытие, ids и юридическую консистентность artifact | merged draft artifact / fragments | список ошибок; не переписывает юридический анализ |

**Final Artifact**

```text
/outputs/discrepancy_analysis.json
```

Содержит:

```text
links              grouped many-to-many legal relationships
atomic_links       row-level matrix_id + contract_id pairs
unmatched_matrix   bank-standard requirements missing in contract
unmatched_contract contract terms without matrix analogue
summary            derived counts
```