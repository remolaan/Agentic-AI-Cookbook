# 32 — Error Handling

## What is error handling?

LangGraph lets you configure `RetryPolicy` on nodes — if a node fails, it retries automatically with exponential backoff.

```mermaid
flowchart TD
    N["Node: risky_operation"] --> F{"Fails?"}
    F -->|"Yes"| R1["Retry 1<br/>0.5s wait"]
    R1 --> F
    F -->|"Yes"| R2["Retry 2<br/>1.0s wait"]
    R2 --> F
    F -->|"Yes: max retries"| E["💥 Error raised"]
    F -->|"No"| OK["✅ Success"]
```

## What you'll learn

- `RetryPolicy` — `initial_interval`, `max_attempts`, `backoff_factor`
- Node-level retry via `add_node(..., retry=RetryPolicy(...))`
- `recursion_limit` — max steps before `GraphRecursionError`
- `NodeError` — inspect failures

## Key idea

Retry policies make agents resilient. Always set a `recursion_limit` to prevent infinite loops.
