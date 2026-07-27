# 22 — Structured Output with `with_structured_output()`

## What is Structured Output?

`with_structured_output()` is the **modern** way to get structured data from an LLM. It uses the model's native tool-calling / JSON mode internally — cleaner than `PydanticOutputParser`.

## Visual

```mermaid
flowchart LR
    P["📝 Prompt"] --> M["🤖 LLM"]
    M --> S["with_structured_output(PydanticModel)"]
    S --> O["✅ Validated Python object"]
    
    style M fill:#e3f2fd,stroke:#1565c0
    style S fill:#f3e5f5,stroke:#7b1fa2
    style O fill:#e8f5e9,stroke:#2e7d32
```
