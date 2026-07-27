# 46 — Self-Correcting RAG

Retrieve → generate → **verify**. If the answer is bad, re-retrieve with refined query and try again.

```mermaid
flowchart TD
    Q["Question"] --> R["🔍 Retrieve"]
    R --> G["🤖 Generate"]
    G --> V["🔎 Verify"]
    V -->|"✅ Good"| O["Output"]
    V -->|"❌ Bad"| RQ["🔄 Refine query"]
    RQ --> R
    style V fill:#fff3e0,stroke:#e65100
    style RQ fill:#f3e5f5,stroke:#7b1fa2
```

## What you'll build

- Retriever node (simulated with LLM)
- Generator node produces answer
- Verifier node scores answer (pass/fail)
- On fail: refine the query and loop back to retrieve
- Max 3 attempts
