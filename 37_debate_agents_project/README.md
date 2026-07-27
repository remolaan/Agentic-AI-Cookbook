# 37 — Debate Agents

Two agents with opposing personas debate a topic. A third **judge** reads their arguments and declares a winner.

```mermaid
flowchart TB
    T["Topic"] --> P1["✅ Proponent<br/>argues FOR"]
    T --> P2["❌ Opponent<br/>argues AGAINST"]
    P1 --> J["⚖️ Judge"]
    P2 --> J
    J --> V["🏆 Verdict"]
    style P1 fill:#e8f5e9,color:#000000
    style P2 fill:#fce4ec,color:#000000
    style J fill:#fff3e0,stroke:#e65100,color:#000000
```

## What you'll build

- Two agents with different system prompts (pro vs con)
- A judge agent that evaluates both sides
- Parallel execution via graph branching
- Conditional edge for the verdict
