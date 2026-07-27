# 30 — Long-Term Memory

## What is long-term memory?

`BaseStore` provides a **persistent key-value store** that lives **outside** the graph's state. Data stored here survives across threads, sessions, and restarts.

```mermaid
flowchart LR
    subgraph "Graph (ephemeral state)"
        G["MessagesState<br/>per-thread"]
    end
    subgraph "Store (persistent)"
        S["📦 InMemoryStore<br/>cross-session"]
    end
    G -->|"search()"| S
    G -->|"put()"| S
    style S fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000000
```

## What you'll learn

- `InMemoryStore` — persistent key-value store
- `store.put(namespace, key, value)` — save data
- `store.search(namespace)` — query data
- Cross-session memory — remember user facts

## Key idea

State is per-thread and resets. Store is global and persists. Use store for user profiles, preferences, and long-term facts.
