# 17 — Streaming & Async

## Why Streaming & Async?

**Streaming:** Websites and APIs need to show responses as they're generated — not wait 10 seconds for the full output. Streaming sends tokens one by one.

**Async:** When you need to make multiple LLM calls, async lets you run them **in parallel** instead of one after another.

## Visual: Sync vs Async vs Streaming

```mermaid
flowchart TB
    subgraph "Synchronous (blocking)"
        direction LR
        Q1["❓ Call 1"] --> W1["⏳ Wait 3s"]
        W1 --> R1["✅ Response 1"]
        R1 --> Q2["❓ Call 2"]
        Q2 --> W2["⏳ Wait 3s"]
        W2 --> R2["✅ Response 2"]
    end
    
    subgraph "Async (parallel)"
        direction LR
        Q3["❓ Call 1"] --> P1["⚡ Parallel"]
        Q4["❓ Call 2"] --> P1
        Q5["❓ Call 3"] --> P1
        P1 --> R3["✅ All responses<br/>in ~3s total"]
    end
    
    subgraph "Streaming (real-time)"
        direction LR
        Q6["❓ Ask"] --> S1["Token 1"]
        S1 --> S2["Token 2"]
        S2 --> S3["Token 3"]
        S3 --> S4["..."]
    end
    
    style W1 fill:#fce4ec,color:#000000
    style W2 fill:#fce4ec,color:#000000
    style P1 fill:#e3f2fd,stroke:#1565c0,color:#000000
    style S1 fill:#e8f5e9,color:#000000
    style S2 fill:#e8f5e9,color:#000000
    style S3 fill:#e8f5e9,color:#000000
```

## What You'll Learn

| Method | What It Does | When to Use |
|--------|-------------|-------------|
| `.stream()` | Sync iteration over tokens | CLI apps, simple scripts |
| `.astream()` | Async iteration over tokens | Web servers (FastAPI) |
| `.ainvoke()` | Async single call | Non-blocking operations |
| `asyncio.gather()` | Run multiple async calls in parallel | Batch processing |

## Code Walkthrough

### 1. Synchronous Streaming — `.stream()`

```python
chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"topic": "octopuses"}):
    print(chunk, end="", flush=True)
```

**What it does:** Tokens arrive one by one as the LLM generates them. `flush=True` ensures each token is printed immediately (no buffering).

### 2. Async Streaming — `.astream()`

```python
async def async_stream():
    async for chunk in chain.astream({"topic": "black holes"}):
        print(chunk, end="", flush=True)

asyncio.run(async_stream())
```

**What it does:** Same as streaming, but async. The `async for` loop yields tokens without blocking the event loop — your server can handle other requests while streaming.

```mermaid
flowchart LR
    A["🔧 asyncio.run()"] --> AS["async def<br/>async_stream()"]
    AS --> L["🤖 LLM"]
    L -->|"Token 1"| P["print(chunk)"]
    L -->|"Token 2"| P
    L -->|"Token 3"| P
    
    style AS fill:#e3f2fd,color:#000000
    style L fill:#f3e5f5,color:#000000
```

### 3. Parallel Async Calls — `asyncio.gather()`

```python
async def parallel_calls():
    inputs = [
        {"tone": "funny", "length": "poem", "topic": "cats"},
        {"tone": "serious", "length": "paragraph", "topic": "AI safety"},
        {"tone": "poetic", "length": "haiku", "topic": "the moon"},
    ]
    tasks = [chain.ainvoke(inp) for inp in inputs]
    results = await asyncio.gather(*tasks)
```

**What it does:** Creates 3 async tasks and runs them **simultaneously**. `asyncio.gather` waits for all to complete. Total time ≈ time of the slowest single call (not the sum).

```mermaid
flowchart TB
    M["🏗️ asyncio.gather()"] --> T1["Task 1: funny poem<br/>about cats"]
    M --> T2["Task 2: serious paragraph<br/>about AI safety"]
    M --> T3["Task 3: poetic haiku<br/>about the moon"]
    
    T1 --> W["⏳ ~3 seconds total<br/>(all run in parallel)"]
    T2 --> W
    T3 --> W
    W --> R["📤 All 3 results"]
    
    style T1 fill:#e3f2fd,color:#000000
    style T2 fill:#fff3e0,color:#000000
    style T3 fill:#f3e5f5,color:#000000
    style W fill:#e8f5e9,stroke:#2e7d32,color:#000000
```

## Key Concept: Streaming is Built Into LCEL

Any chain built with `|` supports streaming automatically:

```python
prompt | llm | StrOutputParser()   # ← This streams by default!
```

You don't need special code. Just call `.stream()` or `.astream()`. LangChain handles the plumbing.

## Summary

| You want... | Use... |
|-------------|--------|
| Real-time output in CLI | `chain.stream()` |
| Real-time output in a web server | `chain.astream()` |
| One async call (non-blocking) | `chain.ainvoke()` |
| Many parallel calls | `asyncio.gather(*tasks)` |

- **Streaming** = token-by-token output (real-time UX)
- **Async** = non-blocking operations (handle many requests)
- **Parallel** = multiple LLM calls at once (faster batch processing)
- All LCEL chains support streaming + async by default
