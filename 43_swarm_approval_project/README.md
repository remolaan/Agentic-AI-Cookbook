# 43 — Swarm with Human Approval

Multiple workers process items in parallel, but every result requires **human approval** before being accepted. Workers pause at `interrupt()` and wait.

```mermaid
flowchart TD
    Q["Task"] --> F["📤 Fan-out"]
    F --> W1["Worker 1"]
    F --> W2["Worker 2"]
    W1 --> I1["⏸️ Interrupt: Approve?"]
    W2 --> I2["⏸️ Interrupt: Approve?"]
    I1 -->|"✅ Resume"| C["📋 Collector"]
    I2 -->|"✅ Resume"| C
    I1 -->|"❌ Reject"| E["END"]
    I2 -->|"❌ Reject"| E
    style I1 fill:#fff3e0,stroke:#e65100,color:#000000
    style I2 fill:#fff3e0,stroke:#e65100,color:#000000
```

## What you'll build

- Parallel workers via `Send`
- Each worker pauses with `interrupt()` for approval
- `Command(resume=...)` to continue or reject
- Collector merges approved results
