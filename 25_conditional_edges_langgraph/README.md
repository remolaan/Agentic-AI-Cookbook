# 25 — Conditional Edges

## What are conditional edges?

A conditional edge routes to **different nodes** based on the current state. The router function looks at the state and returns the name of the next node.

```mermaid
flowchart TD
    S["START"] --> C["Check sentiment"]
    C -->|"positive"| P["Positive handler"]
    C -->|"negative"| N["Negative handler"]
    P --> E["END"]
    N --> E
    style C fill:#fff3e0,stroke:#e65100
    style P fill:#e8f5e9,stroke:#2e7d32
    style N fill:#fce4ec,stroke:#c62828
```

## What you'll learn

- `add_conditional_edges(source, router, path_map)` — routing logic
- Router function returns a node name string
- `path_map` dict maps return values to node names

## Key idea

The router function gets the full state and returns the **name** of the next node. If the name doesn't match any node, the graph stops.
