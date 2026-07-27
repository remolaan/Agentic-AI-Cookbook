# 33 — Subgraphs

## What are subgraphs?

A subgraph is a **graph inside a graph**. You compile an inner `StateGraph` and add it as a node in the outer graph. The outer graph sees the subgraph as a single step, but internally it runs its own nodes and edges.

```mermaid
flowchart TD
    subgraph "Main Graph"
        A["Greet"] --> SUB["📦 Subgraph<br/>Validate + Capitalize"]
        SUB --> C["Farewell"]
    end
    subgraph "Subgraph (hidden inside)"
        V["Validate"] --> CAP["Capitalize"]
    end
    style SUB fill:#f3e5f5,stroke:#7b1fa2
    style V fill:#e3f2fd
    style CAP fill:#e3f2fd
```

## What you'll learn

- Compile a `StateGraph` separately → subgraph
- Add subgraph as a node via `add_node(name, subgraph.compile())`
- The outer graph treats it as a single step

## Key idea

Subgraphs let you **compose** complex agents from reusable pieces. Each subgraph has its own internal state and logic.
