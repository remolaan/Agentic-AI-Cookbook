# 44 — RAG Query Router

A router examines a user question and sends it to the **best retriever**: docs, Wikipedia, or web search.

```mermaid
flowchart TD
    Q["User question"] --> R["🔀 Query Router"]
    R -->|"technical"| D["📄 Doc Retriever"]
    R -->|"general"| W["🌐 Wikipedia Retriever"]
    R -->|"current"| S["🔍 Web Search"]
    D --> G["🤖 Generate answer"]
    W --> G
    S --> G
    style R fill:#f3e5f5,stroke:#7b1fa2
    style G fill:#e8f5e9,stroke:#2e7d32
```

## What you'll build

- LLM-based router that classifies queries
- Multiple retrieval sources (Chroma, Wikipedia, web)
- Conditional edge routing to the right retriever
- Single generation node regardless of source
