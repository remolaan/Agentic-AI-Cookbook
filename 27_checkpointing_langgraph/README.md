# 27 — Checkpointing

## What is checkpointing?

Checkpointing saves the graph state after **every step**. This means the graph can be paused, resumed, and replayed. Each conversation gets a **thread_id** — separate sessions stay isolated.

```mermaid
flowchart LR
    subgraph "Thread abc-123"
        T1["Turn 1"] --> C1["💾 Checkpoint"]
        C1 --> T2["Turn 2"]
        T2 --> C2["💾 Checkpoint"]
    end
    style C1 fill:#fff3e0,stroke:#e65100,color:#000000
    style C2 fill:#fff3e0,stroke:#e65100,color:#000000
```

## What you'll learn

- `MemorySaver` — in-memory checkpointer
- `configurable={"thread_id": "..."}` — session identity
- `get_state()` — inspect current state
- `get_state_history()` — past checkpoints (time travel)

## Key idea

Without checkpointing, each `invoke()` is fresh. With it, the graph remembers everything across turns — like memory for agents.
