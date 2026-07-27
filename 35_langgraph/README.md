# 35 — Command (Multi-Action)

## What is Command?

`Command` lets a node do **multiple things at once**: update state, add messages, jump to a specific node, and resume from an interrupt — all in one return.

```mermaid
flowchart TD
    N["Node returns<br/>Command(goto='next', update={...})"]
    N --> U["✏️ State updated"]
    N --> G["➡️ Graph jumps to 'next'"]
    style N fill:#f3e5f5,stroke:#7b1fa2
    style U fill:#e3f2fd
    style G fill:#fff3e0
```

## What you'll learn

- `Command(goto=node_name)` — jump to a specific node
- `Command(update=dict)` — update state directly
- `Command(resume=value)` — resume from interrupt
- Combining all three in one return

## Key idea

Without `Command`, a node can only return state updates. With `Command`, it can **control the flow** — jump, update, and resume in one shot.
