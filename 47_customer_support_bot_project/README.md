# 47 — Customer Support Bot

A production-ready support bot combining **RAG** (product docs), **memory** (conversation history), **human handoff** (escalation), and **tools** (ticketing, refunds).

```mermaid
flowchart TD
    U["User"] --> A["🤖 Support Agent"]
    KB["📚 Knowledge Base"] --> A
    A -->|"answer"| U
    A -->|"escalate"| H["👤 Human Agent"]
    A -->|"create_ticket"| T["🎫 Ticketing Tool"]
    A -->|"process_refund"| R["💰 Refund Tool"]
    style A fill:#e3f2fd,stroke:#1565c0
    style H fill:#fff3e0,stroke:#e65100
```

## What you'll build

- System prompt with support guidelines
- Knowledge base via simulated RAG
- Tools: `create_ticket`, `process_refund`
- Human escalation via `interrupt()`
- `MemorySaver` for conversation persistence
