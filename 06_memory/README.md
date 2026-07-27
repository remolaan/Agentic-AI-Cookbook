# 06 — Memory

## Why Memory?

**LLMs are stateless** — they don't remember past turns. Every `invoke()` is a fresh conversation. **Memory** gives your chain a recollection of the conversation so far by injecting history into the prompt.

## Visual: How Memory Works

```mermaid
flowchart TB
    subgraph "Without Memory"
        U1["👤 User: 'Hi, I'm Alice'"] --> L1["🤖 LLM"]
        L1 --> R1["💬 'Hello Alice!'"]
        U2["👤 User: 'What's my name?'"] --> L2["🤖 LLM"]
        L2 --> R2["💬 'I don't know'"]
    end

    subgraph "With Memory (RunnableWithMessageHistory)"
        U3["👤 User: 'Hi, I'm Alice'"] --> MH1["📝 ChatMessageHistory"]
        MH1 --> L3["🤖 LLM + history"]
        L3 --> R3["💬 'Hello Alice!'"]
        U4["👤 User: 'What's my name?'"] --> MH2["📝 ChatMessageHistory"]
        MH2 --> L4["🤖 LLM + history"]
        L4 --> R4["💬 'You said Alice!'"]
    end

    style L1 fill:#fce4ec,stroke:#c62828
    style L2 fill:#fce4ec,stroke:#c62828
    style L3 fill:#e8f5e9,stroke:#2e7d32
    style L4 fill:#e8f5e9,stroke:#2e7d32
    style MH1 fill:#e3f2fd,stroke:#1565c0
    style MH2 fill:#e3f2fd,stroke:#1565c0
```

## What You'll Learn

| Memory Type | What It Stores | When to Use |
|-------------|---------------|-------------|
| `ChatMessageHistory` + `RunnableWithMessageHistory` | Full conversation transcript | Short chats, small contexts |
| Custom `WindowedChatMessageHistory` | Only the last N messages | Long conversations (saves tokens) |
| Manual summarization | AI-generated summary of old messages | Very long conversations |

## Modern Pattern: MessagesPlaceholder + RunnableWithMessageHistory

The modern LangChain way uses two pieces working together:

```mermaid
flowchart LR
    P["📝 Prompt with<br/>MessagesPlaceholder"] --> C["🔗 LCEL Chain<br/>prompt | llm | parser"]
    C --> W["RunnableWithMessageHistory<br/>(wraps chain + history)"]
    W --> H["📁 History Store<br/>ChatMessageHistory"]
    H -.-> P
    
    style P fill:#e3f2fd,stroke:#1565c0
    style W fill:#f3e5f5,stroke:#7b1fa2
    style H fill:#fff3e0,stroke:#e65100
```

### Step 1: Add a history slot in your prompt

```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),  # ← history injected here
    ("human", "{input}"),
])
```

### Step 2: Build an LCEL chain

```python
chain = prompt | llm | StrOutputParser()
```

### Step 3: Wrap with RunnableWithMessageHistory

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}

def get_session(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session,
    input_messages_key="input",
    history_messages_key="history",
)
```

### Step 4: Invoke with a session ID

```python
chain_with_history.invoke(
    {"input": "Hi, I'm Alice."},
    config={"configurable": {"session_id": "abc123"}},
)
```

## Code Walkthrough

### 1. Buffer Memory — Full History

Uses `ChatMessageHistory` (stores everything). The history grows with every turn.

| Turn | History Size |
|------|-------------|
| 1 | 2 messages (H + AI) |
| 2 | 4 messages |
| N | N × 2 messages |

```mermaid
flowchart LR
    T1["Turn 1<br/>Hi I'm Alice"] --> H1["📁 History<br/>H: Hi I'm Alice<br/>AI: Hello Alice!"]
    T2["Turn 2<br/>What's my name?"] --> H2["📁 History<br/>H: Hi I'm Alice<br/>AI: Hello Alice!<br/>H: What's my name?<br/>AI: You're Alice!"]
    
    style H1 fill:#e3f2fd
    style H2 fill:#e3f2fd
```

### 2. Window Memory — Sliding Window

Custom `WindowedChatMessageHistory` keeps only the last `k` exchanges. Older messages are dropped.

```python
class WindowedChatMessageHistory(ChatMessageHistory):
    def add_message(self, message):
        super().add_message(message)
        pairs = self.k * 2
        if len(self.messages) > pairs:
            self.messages = self.messages[-pairs:]
```

```mermaid
flowchart LR
    subgraph "Window k=2"
        T2["Turn 2"] --> T3["Turn 3"] --> P["📝 Prompt<br/>(last 2 turns only)"]
        T1["Turn 1<br/>(dropped!)"] -.-> P
    end
    style T1 fill:#fce4ec,stroke:#c62828
    style T2 fill:#e3f2fd,stroke:#1565c0
    style T3 fill:#e3f2fd,stroke:#1565c0
    style P fill:#fff3e0,stroke:#e65100
```

### 3. Summary Memory — Manual Summarization

No built-in class for this in modern LangChain (it was removed). Instead, use a second LLM call to summarize periodically and feed the summary into the next prompt.

```mermaid
flowchart LR
    A["Long conversation"] --> B["🤖 Summarizer LLM"]
    B --> C["📄 Summary: 'User likes hiking and coffee'"]
    C --> D["📝 Injected into next prompt"]
    
    style B fill:#f3e5f5,stroke:#7b1fa2
    style C fill:#e3f2fd,stroke:#1565c0
```

## Key Concept: History is Just Prompt Injection

Memory works by **modifying the prompt**. Before your message reaches the LLM, the history is injected via `MessagesPlaceholder`. The LLM never "remembers" — it just gets a longer prompt that includes past context.

```mermaid
flowchart LR
    U["👤 User<br/>What's my name?"] --> M["📁 ChatMessageHistory<br/>appends to prompt"]
    M --> P["📄 Augmented Prompt<br/>H: Hi I'm Alice<br/>AI: Hello!<br/>H: What's my name?"]
    P --> L["🤖 LLM sees full history"]
    L --> R["💬 'You're Alice!'"]
    
    style M fill:#e3f2fd,stroke:#1565c0
    style P fill:#fff3e0,stroke:#e65100
    style L fill:#e8f5e9,stroke:#2e7d32
```

## Summary

| Memory | Implementation | Tokens Used | Best For |
|--------|---------------|-------------|----------|
| Buffer | `ChatMessageHistory` | Grows forever | Short chats, demo |
| Window | Custom `WindowedChatMessageHistory(k)` | Fixed (k × message size) | Customer support |
| Summary | Manual LLM summarization | Compressed | Long-running conversations |

**Rule of thumb:** Start with `ChatMessageHistory`. If prompts get too long, switch to windowed or summarization.
