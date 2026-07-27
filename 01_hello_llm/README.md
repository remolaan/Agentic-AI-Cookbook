# 01 — Hello LLM

## What is an LLM call?

An LLM (Large Language Model) takes text input (a **prompt**) and returns text output (a **completion**). LangChain wraps this in a unified interface so you can swap models without rewriting your code.

```mermaid
flowchart LR
    P["📝 Your Prompt<br/>'What is LangChain?'"] --> M["🤖 DeepSeek LLM"] --> R["💬 Response<br/>'LangChain is a framework...'"]
    style P fill:#e3f2fd,stroke:#1565c0
    style M fill:#fff3e0,stroke:#e65100
    style R fill:#e8f5e9,stroke:#2e7d32
```

## What you'll learn

- `ChatOpenAI` — the standard interface for chat models
- `.invoke()` — send a message and get a response
- Why LangChain exists: one API for many LLMs

## The code

`main.py` shows three styles of calling DeepSeek:

```mermaid
flowchart LR
    subgraph Style1["Direct invoke"]
        A1["llm.invoke(msg)"] --> B1["Raw response"]
    end
    subgraph Style2["Prompt template"]
        A2["ChatPromptTemplate"] --> B2["Fill variables"] --> C2["llm.invoke(messages)"]
    end
    subgraph Style3["Chain"]
        A3["prompt | llm"] --> B3["chain.invoke({...})"]
    end
```

1. **Direct invoke** — simplest, just ask and print
2. **Prompt template** — inject variables into a reusable prompt
3. **Chain** — combine prompt + model into one callable

## Try it yourself

Edit the `topic` variable to ask about different things.
