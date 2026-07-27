# 16 — Caching & Rate Limits

## Why Cache?

LLM calls are **slow** (1-10 seconds) and **expensive** (pay per token). Caching stores responses so identical requests return instantly without calling the API again.

## Visual: With vs Without Cache

```mermaid
flowchart TB
    subgraph "Without Cache"
        Q1["❓ 'What is the<br/>speed of light?'"] --> L1["🤖 LLM API<br/>🌐 Remote call"]
        L1 --> R1["💬 '299,792,458 m/s'"]
        Q2["❓ 'What is the<br/>speed of light?'"] --> L2["🤖 LLM API<br/>🌐 Remote call (again!)"]
        L2 --> R2["💬 '299,792,458 m/s'"]
    end
    
    subgraph "With Cache"
        Q3["❓ 'What is the<br/>speed of light?'"] --> C1["💾 Cache<br/>❌ Miss"]
        C1 --> L3["🤖 LLM API<br/>🌐 Remote call"]
        L3 --> C2["💾 Cache<br/>✅ Store result"]
        C2 --> R3["💬 '299,792,458 m/s'"]
        
        Q4["❓ 'What is the<br/>speed of light?'"] --> C3["💾 Cache<br/>✅ Hit"]
        C3 --> R4["💬 '299,792,458 m/s'<br/>⚡ Instant!"]
    end
    
    style L1 fill:#fce4ec
    style L2 fill:#fce4ec
    style L3 fill:#e8f5e9
    style C1 fill:#fff3e0
    style C2 fill:#e8f5e9
    style C3 fill:#e8f5e9,stroke:#2e7d32
    style R4 fill:#e8f5e9
```

## What You'll Learn

| Cache Type | Storage | Persistence | Best For |
|-----------|---------|-------------|----------|
| `InMemoryCache` | Python dict | Lost on restart | Development, short-lived apps |
| `SQLiteCache` | SQLite file | Survives restarts | Single-server production |
| Redis cache (custom) | Redis server | Shared across instances | Multi-server production |

## Code Walkthrough

### 1. InMemoryCache

```python
from langchain_core.caches import InMemoryCache
from langchain_classic.globals import set_llm_cache

set_llm_cache(InMemoryCache())

start = time.perf_counter()
r1 = llm.invoke("What is the speed of light?")    # 1st call: ~3 seconds
print(f"First call: {time.perf_counter() - start:.2f}s")

start = time.perf_counter()
r2 = llm.invoke("What is the speed of light?")    # 2nd call: ~0.01 seconds!
print(f"Cached call: {time.perf_counter() - start:.2f}s")
```

**What it does:** Stores responses in a Python dictionary. The first call hits the API. The second call finds the result in the cache and returns instantly.

### 2. SQLiteCache (Persistent)

```python
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))
```

**What it does:** Stores responses in a SQLite database file. The cache survives restarts. Even if you stop and restart your app, cached responses are still there.

```mermaid
flowchart LR
    Q["❓ User Question"] --> C["💾 SQLite Cache"]
    C -->|"Cache hit ✅"| R["💬 Cached Response (instant)"]
    C -->|"Cache miss ❌"| L["🤖 LLM API (slow)"]
    L --> C
    L --> R2["💬 Fresh Response"]
    
    style C fill:#e3f2fd,stroke:#1565c0
    style R fill:#e8f5e9,stroke:#2e7d32
    style L fill:#fce4ec,stroke:#c62828
```

## How Cache Keys Work

The cache key is based on:
- The **model name** (e.g., `deepseek-chat`)
- The **prompt text** (exact string)
- The **parameters** (temperature, max_tokens, etc.)

Even a tiny change in prompt → different key → cache miss.

## When to Cache vs Not Cache

| Cache | Don't Cache |
|-------|-------------|
| Factual questions ("What is the capital of France?") | Creative writing (poems, stories) |
| Common queries in a chatbot | Personalized responses |
| Expensive/rate-limited APIs | Time-sensitive data (stock prices) |
| Repetitive system prompts | Random/varied outputs |

## Summary

- **InMemoryCache** → simple, fast, lost on restart
- **SQLiteCache** → persistent across restarts
- **Cache key** = model + prompt + params (exact match)
- Caching saves **time** and **money**
- Don't cache creative or time-sensitive responses
- For production multi-instance: use Redis or similar shared cache
