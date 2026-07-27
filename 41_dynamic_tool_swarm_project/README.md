# 41 — Dynamic Tool Swarm

An LLM decides **which tools to call and how many workers to spawn** based on the task. Each tool call becomes a parallel worker via `Send`.

```mermaid
flowchart TD
    Q["User query"] --> A["🤖 Agent LLM"]
    A -->|"tool_calls"| D["📤 Dynamic Dispatch"]
    D -->|"Send('tool_runner', tc1)"| T1["🛠️ Tool 1"]
    D -->|"Send('tool_runner', tc2)"| T2["🛠️ Tool 2"]
    T1 --> J["📋 Join"]
    T2 --> J
    J --> F["🤖 Final response"]
    style A fill:#e3f2fd,color:#000000
    style D fill:#f3e5f5,stroke:#7b1fa2,color:#000000
    style J fill:#fff3e0,stroke:#e65100,color:#000000
```

## What you'll build

- LLM decides how many tools to call
- `Send` fans out to one worker per tool call
- Join node collects all results
- LLM generates final answer from all tool outputs
