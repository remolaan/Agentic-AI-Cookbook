# 36 — Supervisor/Worker Agent

A **supervisor** agent receives a task, breaks it into subtasks, and dispatches each to a **worker** using `Send`. Workers report back, and the supervisor compiles the final answer.

```mermaid
flowchart TD
    U["User task"] --> S["👑 Supervisor"]
    S -->|"Send('writer', topic1)"| W1["✍️ Writer A"]
    S -->|"Send('writer', topic2)"| W2["✍️ Writer B"]
    W1 --> J["📋 Join/Compile"]
    W2 --> J
    J --> R["✅ Final Report"]
    style S fill:#f3e5f5,stroke:#7b1fa2
    style W1 fill:#e3f2fd
    style W2 fill:#e3f2fd
    style J fill:#fff3e0
```

## What you'll build

- Supervisor that splits a task into parts
- Workers that execute in parallel via `Send`
- A join node that compiles results
- `operator.add` reducer to merge worker outputs
