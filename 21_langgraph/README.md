# 21 — LangGraph

## What is LangGraph?

LangGraph is the **modern** way to build agents and multi-step workflows. Instead of a linear chain, you define a **state graph** — nodes (processing steps) and edges (transitions). The agent loops through nodes until it decides to stop.

## Visual

```mermaid
flowchart TD
    S["🟢 START"] --> A["🤖 Agent Node<br/>(LLM decides)"]
    A --> T{"Has tool call?"}
    T -->|"Yes"| TN["🛠️ Tool Node<br/>(runs the tool)"]
    TN --> A
    T -->|"No"| E["🔴 END"]
    
    style S fill:#e8f5e9,stroke:#2e7d32,color:#000000
    style E fill:#fce4ec,stroke:#c62828,color:#000000
    style A fill:#e3f2fd,stroke:#1565c0,color:#000000
    style TN fill:#fff3e0,stroke:#e65100,color:#000000
```
