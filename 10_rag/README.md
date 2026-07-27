# 10 — RAG (Retrieval-Augmented Generation)

## What is RAG?

RAG = **Retrieve** relevant documents → **Augment** the prompt with them → **Generate** an answer. This lets the LLM answer questions about data it wasn't trained on.

## The pipeline

```mermaid
flowchart LR
    A["📄 Load<br/>Wikipedia page"] --> B["✂️ Split<br/>500-char chunks"]
    B --> C["🔢 Embed<br/>(vectors)"]
    C --> D["🗄️ Store<br/>Chroma DB"]
    
    Q["❓ User Question"] --> F["🔍 Retrieve<br/>top 3 chunks"]
    D --> F
    F --> G["📝 Augment<br/>Context + Question"]
    G --> H["🤖 Generate<br/>DeepSeek LLM"]
    H --> I["✅ Answer"]
    
    style A fill:#e3f2fd,stroke:#1565c0
    style Q fill:#fff3e0,stroke:#e65100
    style I fill:#e8f5e9,stroke:#2e7d32
    style G fill:#f3e5f5,stroke:#7b1fa2
```

## What you'll learn

- Full end-to-end RAG pipeline
- Using a retriever as a runnable
- Passing retrieved context into a prompt
- The LCEL pattern

```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

## Key idea

RAG is the foundation of most production LLM applications — chatbots over your docs, Q&A over codebases, customer support bots.
