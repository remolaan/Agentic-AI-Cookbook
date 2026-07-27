# 12 — Agents

## What are agents?

Agents give an LLM **tools** (functions it can call) and let it decide *how* to accomplish a task. Instead of following a fixed chain, the LLM plans, calls tools, observes results, and iterates.

## The agent loop (ReAct)

```mermaid
flowchart TD
    Q["❓ User Question<br/>'What's 15 × 24?'"] --> T["🤔 THINK<br/>'I need to multiply'"]
    T --> A["⚡ ACT<br/>Call multiply(15, 24)"]
    A --> O["👀 OBSERVE<br/>Result: 360"]
    O --> D{"Done?"}
    D -->|"No (or need more info)"| T
    D -->|"Yes"| R["📢 FINAL ANSWER<br/>'15 × 24 = 360'"]
    
    style Q fill:#fff3e0,stroke:#e65100
    style R fill:#e8f5e9,stroke:#2e7d32
    style T fill:#e3f2fd,stroke:#1565c0
    style A fill:#fce4ec,stroke:#c62828
    style O fill:#f3e5f5,stroke:#7b1fa2
```

## What you'll learn

- `create_react_agent` — ReAct (Reason + Act) agent
- `Tool` — wrap any Python function as a tool
- Agent executor — runs the agent loop (think → act → observe → repeat)
- Built-in tools — Wikipedia, calculator, search

## Key idea

Agents = LLM + Tools + Loop. The LLM decides which tool to call and when the task is done.
