# 49 — Research Assistant

A **supervisor** agent delegates to 3 specialist workers (Web Search, Data Analysis, Report Writing), then compiles a final research report with **long-term memory**.

```mermaid
flowchart TD
    Q["Research question"] --> S["👑 Supervisor"]
    S -->|"web_search"| W["🌐 Web Searcher"]
    S -->|"analyze"| D["📊 Data Analyst"]
    S -->|"write"| R["✍️ Report Writer"]
    W --> C["📋 Compiler"]
    D --> C
    R --> C
    C --> M["💾 Store in memory"]
    M --> O["📄 Final report"]
    style S fill:#f3e5f5,stroke:#7b1fa2,color:#000000
    style C fill:#fff3e0,stroke:#e65100,color:#000000
    style M fill:#e3f2fd,color:#000000
```

## What you'll build

- Supervisor routes to specialist workers
- Workers each produce a section
- Compiler merges sections into a report
- Report saved to `InMemoryStore` for future retrieval
- Support for follow-up questions referencing past research
