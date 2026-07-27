# 38 — Agent Router Team

A **router** agent examines a user query and sends it to the right specialist agent: a coder, a writer, or an analyst.

```mermaid
flowchart TD
    Q["User query"] --> R["🔀 Router"]
    R -->|"code"| C["💻 Coder Agent"]
    R -->|"write"| W["✍️ Writer Agent"]
    R -->|"analyze"| A["📊 Analyst Agent"]
    C --> O["📤 Final output"]
    W --> O
    A --> O
    style R fill:#f3e5f5,stroke:#7b1fa2
    style C fill:#e3f2fd
    style W fill:#e8f5e9
    style A fill:#fff3e0
```

## What you'll build

- `RouterRunnable` to route between specialist `create_agent` instances
- Three agents with different system prompts and tools
- Conditional edge routing from the router's output
