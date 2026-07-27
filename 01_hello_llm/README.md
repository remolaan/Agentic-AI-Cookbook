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

## Interactive Testing with Gradio

`main_gr.py` gives you a web UI to experiment interactively:

```bash
python 01_hello_llm/main_gr.py
# then open http://localhost:7860
```

### What you can do

| Section | What it shows |
|---------|---------------|
| **⚙️ Prompt Settings** (collapsible) | Set the **system prompt** before chatting |
| **💬 Chat** (always visible) | Type messages, see AI responses |
| **📤 Raw Prompt** (collapsible) | The **exact messages** object sent to the LLM — every `[SystemMessage]`, `[HumanMessage]`, `[AIMessage]` with full content |
| **📥 Raw Response** (collapsible) | The **full response object** including `content` and `response_metadata` |
| **📊 Token Usage** (collapsible) | Prompt tokens, completion tokens, and total (when the provider returns them) |

### Data flow

```mermaid
flowchart LR
    SP["⚙️ System Prompt"] --> CHAT["💬 Chat Interface"]
    CHAT --> BUILD["🧱 Build Messages<br/>System + History + New"]
    BUILD --> INVOKE["⚡ llm.invoke()"]
    INVOKE --> RESP["📥 Raw Response"]
    INVOKE --> TOKENS["📊 Token Usage"]
    BUILD --> PROMPT["📤 Raw Prompt"]
    
    style SP fill:#e3f2fd,stroke:#1565c0
    style CHAT fill:#fff3e0,stroke:#e65100
    style BUILD fill:#f3e5f5,stroke:#7b1fa2
    style INVOKE fill:#fce4ec,stroke:#c62828
    style PROMPT fill:#e8f5e9,stroke:#2e7d32
    style RESP fill:#e8f5e9,stroke:#2e7d32
    style TOKENS fill:#e8f5e9,stroke:#2e7d32
```

## Gradio UI Layout

Here is what the interface looks like when you open `http://localhost:7860`:

```mermaid
flowchart TB
    subgraph Settings["⚙️ Prompt Settings (collapsed by default)"]
        SP["System Prompt textbox"]
    end
    
    subgraph Chat["💬 Chat Interface (always visible)"]
        direction TB
        M1["User: Hello!"]
        M2["AI: Hi! How can I help?"]
        IN["Message input box"]
    end
    
    subgraph Debug["🔍 Debug Panels (collapsed by default)"]
        RP["📤 Raw Prompt Sent<br/>Shows exact messages sent to LLM"]
        RR["📥 Raw Response Received<br/>Shows full response + metadata"]
        TU["📊 Token Usage<br/>Shows prompt / completion / total tokens"]
    end
    
    Settings --> Chat --> Debug
    
    style Settings fill:#e3f2fd,stroke:#1565c0
    style Chat fill:#fff3e0,stroke:#e65100
    style Debug fill:#f3e5f5,stroke:#7b1fa2
    style RP fill:#e8f5e9,stroke:#2e7d32
    style RR fill:#e8f5e9,stroke:#2e7d32
    style TU fill:#e8f5e9,stroke:#2e7d32
```

## Try it yourself

Edit the `topic` variable in `main.py` to ask about different things, or launch `main_gr.py` to experiment freely.
