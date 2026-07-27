# 50 — Agent API Server

Deploy a **multi-agent swarm** behind a **FastAPI** server with streaming, checkpointing, and Docker support.

```mermaid
flowchart LR
    C["Client"] --> API["🌐 FastAPI /ask"]
    API --> S["Swarm Controller"]
    S -->|"research"| R["🔍 Research Agent"]
    S -->|"code"| P["💻 Code Agent"]
    R --> API
    P --> API
    API --> C
    style API fill:#e3f2fd,stroke:#1565c0
    style S fill:#f3e5f5,stroke:#7b1fa2
```

## What you'll build

- FastAPI server with `/ask` endpoint
- Swarm of specialist agents routed by query type
- Streaming responses with SSE
- `MemorySaver` for session persistence
- Dockerfile for deployment
