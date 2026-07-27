# 45 — Multi-Source RAG

Query **three sources in parallel** — docs, web, and internal knowledge — then **rerank** and generate from the best results.

```mermaid
flowchart TD
    Q["Question"] --> F["📤 Fan-out"]
    F -->|"Send"| D["📄 Docs"]
    F -->|"Send"| W["🌐 Web"]
    F -->|"Send"| K["🧠 Knowledge"]
    D --> R["📋 Rerank & Merge"]
    W --> R
    K --> R
    R --> G["🤖 Generate"]
    style F fill:#f3e5f5,stroke:#7b1fa2
    style R fill:#fff3e0,stroke:#e65100
    style G fill:#e8f5e9,stroke:#2e7d32
```

## What you'll build

- `Send` fans out to 3 retrievers in parallel
- Each retriever returns context from a different source
- Rerank node scores and selects the best context
- Generate node produces final answer
