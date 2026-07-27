# 13 — LCEL (LangChain Expression Language)

## What is LCEL?

LCEL is the **modern way** to build chains using the `|` (pipe) operator. It's:

- **Declarative** — say *what* to do, not *how*
- **Composable** — any runnable can be combined with `|`
- **Auto-capable** — everything you `|` together gets streaming, async, and batch for free

## Visual: LCEL vs Classic Chains

```mermaid
flowchart TB
    subgraph "Classic (Lesson 05)"
        A1["LLMChain(llm, prompt)"] --> A2["SimpleSequentialChain(chains=[...])"]
        A2 --> A3["SequentialChain(...)"]
    end
    
    subgraph "LCEL (Lesson 13)"
        B1["prompt | llm | parser"]
        B2["RunnableParallel(a=..., b=...)"]
        B3["RunnablePassthrough.assign(...)"]
    end
    
    style A1 fill:#fce4ec,color:#000000
    style A2 fill:#fce4ec,color:#000000
    style A3 fill:#fce4ec,color:#000000
    style B1 fill:#e8f5e9,stroke:#2e7d32,color:#000000
    style B2 fill:#e8f5e9,stroke:#2e7d32,color:#000000
    style B3 fill:#e8f5e9,stroke:#2e7d32,color:#000000
```

## What You'll Learn

| Component | What It Does | Visual |
|-----------|-------------|--------|
| `RunnablePassthrough` | Passes data through unchanged | `input → output` |
| `RunnableParallel` | Runs multiple chains simultaneously | Fork |
| `RunnableBranch` | Routes to different chains based on condition | Switch |
| `.assign()` | Adds computed fields to a dict | Enrich |

## Code Walkthrough

### 1. RunnablePassthrough — Pass Through

```python
chain = {"input": RunnablePassthrough()} | ChatPromptTemplate.from_template("Say: {input}") | llm | StrOutputParser()
```

**What it does:** `RunnablePassthrough()` takes whatever input it receives and passes it through unchanged. Here, it puts the raw input into a dict under the key `"input"` so the template can use `{input}`.

```mermaid
flowchart LR
    I["📥 'Hello!'"] --> P["RunnablePassthrough"]
    P --> D["📦 {'input': 'Hello!'}"]
    D --> T["📝 Template: 'Say: {input}'"]
    
    style P fill:#e3f2fd,color:#000000
    style D fill:#fff3e0,color:#000000
```

### 2. RunnableParallel — Run in Parallel

```python
parallel_chain = RunnableParallel(
    summary=summary_prompt | llm | StrOutputParser(),
    translation=translation_prompt | llm | StrOutputParser(),
)
response = parallel_chain.invoke({"text": "LangChain makes it easy to build LLM apps."})
```

**What it does:** Takes the same input and runs 2 independent chains on it simultaneously. Returns a dict with both results.

```mermaid
flowchart LR
    I["📥 Input text"] --> P["RunnableParallel"]
    P --> S["📝 Summarize<br/>Prompt → LLM → Parser"]
    P --> T["🌍 Translate (French)<br/>Prompt → LLM → Parser"]
    S --> O["📤 Output<br/>{summary: '...',<br/> translation: '...'}"]
    T --> O
    
    style P fill:#f3e5f5,stroke:#7b1fa2,color:#000000
    style S fill:#e3f2fd,color:#000000
    style T fill:#e3f2fd,color:#000000
    style O fill:#e8f5e9,stroke:#2e7d32,color:#000000
```

### 3. `.assign()` — Add Computed Fields

```python
chain = RunnablePassthrough.assign(
    poem=lambda x: ChatPromptTemplate.from_template("Write a poem about {topic}") | llm | StrOutputParser()
)
response = chain.invoke({"topic": "programming"})
# response = {"topic": "programming", "poem": "...poem text..."}
```

**What it does:** Starts with the input dict `{"topic": "programming"}`, passes it through (preserving `topic`), and adds a new key `"poem"` computed by running an LLM chain.

```mermaid
flowchart LR
    I["📥 {topic: 'programming'}"] --> P["RunnablePassthrough"]
    P --> A[".assign()"]
    P --> G["🤖 Generate poem"]
    A --> O["📤 {topic: 'programming',<br/>poem: '...verse...'}"]
    G --> O
    
    style A fill:#e3f2fd,color:#000000
    style G fill:#f3e5f5,color:#000000
    style O fill:#e8f5e9,color:#000000
```

## Key Concept: Everything is a Runnable

In LCEL, every component is a **`Runnable`**:
- Prompts → `Runnable`
- Models → `Runnable`
- Parsers → `Runnable`
- Custom functions → `RunnableLambda`
- Dicts → `RunnableParallel` (automatically)

```python
# These are ALL runnables:
prompt | llm | parser                    # chain
{"key": RunnablePassthrough()}           # dict with passthrough
RunnableParallel(a=chain1, b=chain2)     # parallel
```

**Why it matters:** If it's a Runnable, you can `.invoke()`, `.stream()`, `.batch()`, and `.ainvoke()` it — no extra code needed.

## Summary

| Pattern | Purpose | Example |
|---------|---------|---------|
| `A \| B \| C` | Sequential pipeline | `prompt \| llm \| parser` |
| `RunnableParallel(a=..., b=...)` | Run chains in parallel | `summary + translation` |
| `.assign(key=...)` | Add computed fields | `input + generated poem` |
| `RunnablePassthrough()` | Pass data through | Forward input to next step |

LCEL is the **recommended way** to build chains in modern LangChain (≥0.3).
