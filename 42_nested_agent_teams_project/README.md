# 42 — Nested Agent Teams

A parent agent treats a child agent as a **tool**. The child agent runs its own graph internally, and the parent sees only the final result.

```mermaid
flowchart TD
    subgraph "Parent Graph"
        P["👑 Parent Agent"]
        T["🤖 Agent Tool<br/>(subgraph)"]
        P --> T
        T --> P
    end
    subgraph "Subgraph (hidden)"
        C["Child Agent"] --> CT["Child Tools"]
        CT --> C
    end
    style P fill:#f3e5f5,stroke:#7b1fa2
    style T fill:#fff3e0,stroke:#e65100
```

## What you'll build

- A child agent compiled as a subgraph
- The subgraph wrapped as a `Tool`
- Parent agent calls the tool like any other function
- Subgraph runs its own internal loop
