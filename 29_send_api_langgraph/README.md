# 29 — Send API (Dynamic Parallelism)

## What is the Send API?

`Send(node, arg)` lets you **dynamically** fan out to multiple nodes in parallel. It's like `add_conditional_edges` but instead of routing to one node, it routes to **many** — each with its own argument.

```mermaid
flowchart TD
    S["START"] --> F["Fan-out node"]
    F -->|"Send('process', item1)"| P1["Process A"]
    F -->|"Send('process', item2)"| P2["Process B"]
    F -->|"Send('process', item3)"| P3["Process C"]
    P1 --> J["Join"]
    P2 --> J
    P3 --> J
    J --> E["END"]
    style F fill:#f3e5f5,stroke:#7b1fa2,color:#000000
    style P1 fill:#e3f2fd,color:#000000
    style P2 fill:#e3f2fd,color:#000000
    style P3 fill:#e3f2fd,color:#000000
```

## What you'll learn

- `Send(node, arg)` — send a message to a specific node
- Returning a list of `Send` from a node to fan out
- All `Send` instances execute in parallel
- Results merge back via the state reducer

## Key idea

`Send` enables map-reduce patterns. One node decides what work to do and fans out to N parallel workers. The `add_messages` reducer merges results automatically.
