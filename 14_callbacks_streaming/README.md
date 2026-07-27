# 14 — Callbacks & Streaming

## Why Callbacks?

Callbacks let you **hook into the LLM lifecycle** — when a request starts, when a token arrives, when an error occurs. Use them for:

- **Logging** — track every LLM call
- **Monitoring** — measure latency, token count
- **Token counting** — track usage for billing
- **UI updates** — show streaming tokens in real-time

## Visual: The LLM Lifecycle

```mermaid
flowchart TB
    S["🚀 on_llm_start()<br/>'Request starting...'"] --> P["⏳ LLM Processing"]
    P --> T["🔤 Stream tokens<br/>(optional)"]
    T --> E["✅ on_llm_end()<br/>'Response received'"]
    P --> ER["❌ on_llm_error()<br/>'Something failed'"]
    
    subgraph "Your Callback Handler"
        S
        E
        ER
        C["💬 Intercept every event"]
    end
    
    style S fill:#e3f2fd,stroke:#1565c0
    style E fill:#e8f5e9,stroke:#2e7d32
    style ER fill:#fce4ec,stroke:#c62828
    style C fill:#fff3e0,stroke:#e65100
```

## What You'll Learn

| Concept | What It Does |
|---------|-------------|
| `BaseCallbackHandler` | Base class for custom handlers — override methods you need |
| `on_llm_start` | Fired when an LLM call begins |
| `on_llm_end` | Fired when the response is complete |
| `on_llm_error` | Fired when an error occurs |
| Streaming | Real-time token-by-token output |

## Code Walkthrough

### 1. Custom Callback Handler

```python
class TokenCounter(BaseCallbackHandler):
    def __init__(self):
        self.token_count = 0

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"[LLM Start] Prompt length: {len(prompts[0])} chars")

    def on_llm_end(self, response, **kwargs):
        tokens = sum(len(generation.message.content.split()) for generation in response.generations[0])
        self.token_count += tokens
        print(f"[LLM End] Generated ~{tokens} words")

    def on_llm_error(self, error, **kwargs):
        print(f"[LLM Error] {error}")

handler = TokenCounter()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", callbacks=[handler])
```

**What it does:** Creates a custom handler that:
1. Prints "[LLM Start]" with prompt length when a call begins
2. Counts tokens and prints "[LLM End]" when the response arrives
3. Prints "[LLM Error]" if something fails

The handler is attached to the LLM via the `callbacks` parameter.

```mermaid
flowchart LR
    U["👤 User calls<br/>llm.invoke()"] --> CB["📋 TokenCounter<br/>(callback handler)"]
    CB --> L["🤖 LLM"]
    L --> CB2["📋 TokenCounter<br/>(on_llm_end)"]
    CB2 --> R["💬 Response"]
    
    style CB fill:#e3f2fd
    style CB2 fill:#e3f2fd
```

### 2. Streaming Tokens

```python
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", streaming=True)
chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"topic": "the ocean"}):
    print(chunk, end="", flush=True)
```

**What it does:** Sets `streaming=True` on the LLM. Instead of waiting for the full response, tokens arrive one by one. `chain.stream()` yields each chunk as it arrives.

```mermaid
flowchart LR
    C["🤖 LLM thinking..."] --> T1["Token 1: 'The'"]
    T1 --> T2["Token 2: ' ocean'"]
    T2 --> T3["Token 3: ' is'"]
    T3 --> T4["Token 4: ' vast'"]
    T4 --> T5["...and so on..."]
    
    subgraph "User sees"
        T1
        T2
        T3
        T4
    end
    
    style T1 fill:#e3f2fd
    style T2 fill:#e3f2fd
    style T3 fill:#e3f2fd
    style T4 fill:#e3f2fd
```

**Without streaming (blocking):** Wait 10 seconds → see full response at once
**With streaming (non-blocking):** See words appear in real-time

## Key Concept: Callbacks Don't Change Behavior

Callbacks are **observers** — they listen but don't modify the chain. You can add or remove them without changing how your chain works. This is the **Observer pattern** in software engineering.

## Summary

- **Callbacks** = hooks into the LLM lifecycle (start, end, error, token)
- Use `BaseCallbackHandler` to create custom observers
- Callbacks are great for logging, monitoring, and token counting
- **Streaming** sends tokens one by one for real-time display
- Any LCEL chain supports streaming automatically via `.stream()`
