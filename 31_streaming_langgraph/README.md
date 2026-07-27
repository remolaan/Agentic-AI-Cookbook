# 31 — Streaming

## What is streaming in LangGraph?

LangGraph supports **7 stream modes** that let you inspect graph execution as it happens — not just the final result.

```mermaid
flowchart LR
    G["Graph runs..."] --> S["stream(mode='values')"]
    S --> P1["📤 Full state at each step"]
    G --> S2["stream(mode='updates')"]
    S2 --> P2["📤 Only node outputs"]
    G --> S3["stream(mode='messages')"]
    S3 --> P3["📤 Token by token"]
    style G fill:#e3f2fd,stroke:#1565c0
    style S fill:#fff3e0,stroke:#e65100
    style S2 fill:#fff3e0,stroke:#e65100
    style S3 fill:#fff3e0,stroke:#e65100
```

## What you'll learn

- `stream(mode="values")` — full state each step
- `stream(mode="updates")` — only node output changes
- `stream(mode="messages")` — token-level streaming
- Comparing modes

## Key idea

`"values"` = complete picture. `"updates"` = what changed. `"messages"` = real-time tokens.
