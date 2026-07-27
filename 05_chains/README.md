# 05 — Chains

## What is a chain?

A chain links multiple steps together: prompt → model → parser. LangChain provides pre-built chains for common patterns.

```mermaid
flowchart LR
    Q["Question"] --> P["📝 Prompt"] --> M["🤖 LLM"] --> R["💬 Response"]
    style Q fill:#e3f2fd,stroke:#1565c0
    style P fill:#fff3e0,stroke:#e65100
    style M fill:#fce4ec,stroke:#c62828
    style R fill:#e8f5e9,stroke:#2e7d32
```

## What you'll learn

- `LLMChain` — the classic prompt → model wrapper
- `SimpleSequentialChain` — run chains one after another, passing output as input

```mermaid
flowchart LR
    A["Step 1<br/>Name the product"] --> B["Output: name"] --> C["Step 2<br/>Write tagline for name"] --> D["Output: tagline"]
    style A fill:#e3f2fd,stroke:#1565c0
    style C fill:#fff3e0,stroke:#e65100
```

- `SequentialChain` — multi-input / multi-output chains

```mermaid
flowchart LR
    A["Cuisine type"] --> B["Dish description"] --> C["Wine pairing"]
    B --> D["📄 dish_description"]
    C --> E["📄 wine_pairing"]
```

## Modern vs Classic

Newer LangChain (≥0.3) prefers **LCEL** (`|` operator) over chain classes. Both are shown here so you recognize older code when you see it.
