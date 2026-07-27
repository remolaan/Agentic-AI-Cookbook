# 26 — ToolNode

## What is ToolNode?

`ToolNode` executes tool calls inside a LangGraph. It reads the last `AIMessage`'s `tool_calls`, runs each tool, and returns `ToolMessage` results.

```mermaid
flowchart TD
    A["🤖 Agent LLM"] --> T{"tool_calls?"}
    T -->|"Yes"| TN["🛠️ ToolNode<br/>runs tools in parallel"]
    TN --> A
    T -->|"No"| E["END"]
    style A fill:#e3f2fd,stroke:#1565c0
    style TN fill:#fff3e0,stroke:#e65100
```

## What you'll learn

- `ToolNode(tools)` — run tools from LLM requests
- `tools_condition()` — built-in router: "tools" if tool_calls else END
- Combining `ToolNode` + conditional edge for a ReAct loop

## Key idea

`ToolNode` is the bridge between "LLM wants to call a tool" and "the tool actually runs". It handles parallel execution automatically.
