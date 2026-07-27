# 40 — Map-Reduce Swarm

A **swarm** of identical worker agents processes items in parallel (map phase), then a **collector** merges results (reduce phase).

```mermaid
flowchart TD
    S["📦 Input items"] --> F["📤 Fan-out"]
    F -->|"Send"| W1["Worker 1"]
    F -->|"Send"| W2["Worker 2"]
    F -->|"Send"| W3["Worker 3"]
    F -->|"Send"| W4["Worker N"]
    W1 --> C["📋 Collector<br/>operator.add"]
    W2 --> C
    W3 --> C
    W4 --> C
    C --> R["📤 Final merged result"]
    style F fill:#f3e5f5,stroke:#7b1fa2
    style C fill:#fff3e0,stroke:#e65100
```

## What you'll build

- `Send` fan-out to N parallel workers
- Worker agents that process one item each
- `operator.add` reducer for automatic merging
- Collector node for final formatting
