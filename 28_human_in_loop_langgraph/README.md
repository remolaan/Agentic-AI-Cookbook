# 28 — Human-in-the-Loop

## What is Human-in-the-Loop?

Sometimes the agent shouldn't act without approval. `interrupt()` **pauses** the graph, surfaces a value, and waits for a `Command(resume=...)` to continue.

```mermaid
flowchart TD
    A["🤖 Agent requests tool call"] --> I["⏸️ INTERRUPT<br/>'Approve?'"]
    I -->|"User approves"| T["🛠️ ToolNode runs"]
    I -->|"User rejects"| E["END"]
    T --> A
    style I fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#000000
```

## What you'll learn

- `interrupt(value)` — pause graph execution
- `Command(resume=value)` — resume with user input
- `.invoke()` with `Command` to continue
- Approval patterns before tool execution

## Key idea

`interrupt()` raises a `GraphInterrupt` that's caught by the runtime. The graph pauses, the user decides, then `Command(resume=...)` kicks it back into action.
