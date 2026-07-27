# 11 — Advanced Retrieval

## Why Advanced Retrieval?

Basic similarity search (Lesson 10) works, but has limits:

| Problem | Solution |
|---------|----------|
| User phrases question oddly | **MultiQueryRetriever** — generates question variations |
| Need to filter by metadata | **SelfQueryRetriever** — extracts filters from natural language |
| One retriever isn't enough | **EnsembleRetriever** — combines multiple strategies |

## What You'll Learn

| Retriever | What It Does | Visual |
|-----------|-------------|--------|
| `MultiQueryRetriever` | Asks LLM to rephrase question 3 ways, searches each, merges results | Multiple angles |
| `SelfQueryRetriever` | Parses natural language → metadata filters | "Before 2000" → `year < 2000` |
| `EnsembleRetriever` | Weighted blend of multiple retrievers | Best of both worlds |

## Code Walkthrough

### 1. MultiQueryRetriever — Cover All Angles

```python
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm,
)
results = retriever.invoke("Tell me about Python")
```

**What it does:** Takes your question, asks the LLM to generate 3 alternative phrasings, runs all 4 searches (original + 3 variations), and combines the unique results.

```mermaid
flowchart TB
    Q["❓ 'Tell me about Python'"] --> LLM["🤖 LLM"]
    LLM --> V1["Variation 1:<br/>'What is Python?''"]
    LLM --> V2["Variation 2:<br/>'Python features?''"]
    LLM --> V3["Variation 3:<br/>'Python uses?''"]
    
    Q --> VS["🗄️ Vector Store"]
    V1 --> VS
    V2 --> VS
    V3 --> VS
    
    VS --> M["🔀 Merge & Deduplicate"]
    M --> R["📄 Top Results"]
    
    style Q fill:#fff3e0,stroke:#e65100,color:#000000
    style LLM fill:#f3e5f5,stroke:#7b1fa2,color:#000000
    style VS fill:#e3f2fd,stroke:#1565c0,color:#000000
    style M fill:#fce4ec,stroke:#c62828,color:#000000
    style R fill:#e8f5e9,stroke:#2e7d32,color:#000000
```

**Why it helps:** A user might ask "Tell me about Python" — your documents might use "Python programming" or "Python language". Multiple queries cover different phrasings.

### 2. SelfQueryRetriever — Filter by Metadata

```python
metadata_field_info = [
    AttributeInfo(name="year", description="Year the language was created", type="int"),
    AttributeInfo(name="language", description="Programming language name", type="string"),
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Programming languages",
    metadata_field_info=metadata_field_info,
)
results = retriever.invoke("Which languages were created before 2000?")
```

**What it does:** The LLM parses "before 2000" into a filter: `year < 2000`. The retriever applies this filter to the vector search, returning only documents where `year < 2000`.

```mermaid
flowchart LR
    Q["❓ 'Languages before 2000'"] --> LLM["🤖 LLM<br/>Parse filter"]
    LLM --> F["📋 Filter:<br/>year < 2000"]
    F --> VS["🗄️ Vector Store<br/>(search with filter)"]
    Q --> VS
    VS --> R["📄 Results<br/>(only pre-2000 docs)"]
    
    style Q fill:#fff3e0,color:#000000
    style LLM fill:#f3e5f5,color:#000000
    style F fill:#e3f2fd,color:#000000
    style VS fill:#fce4ec,color:#000000
    style R fill:#e8f5e9,color:#000000
```

**Why it matters:** Without SelfQuery, "languages before 2000" would return any document about languages, and you'd need to filter manually. SelfQuery does it in one step.

### 3. EnsembleRetriever — Combine Strategies

```python
from langchain_classic.retrievers import EnsembleRetriever

ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7],
)
```

*(Concept shown — combines keyword search + vector search with weighted scoring.)*

**What it does:** Runs multiple retrievers, scores each result, and returns the best combined ranking. You control the weight of each strategy.

## Key Concept: Retrieval Quality

```mermaid
flowchart LR
    B["Basic Search<br/>One query, one pass"] --> M["🚀 Advanced Search<br/>Multi-query / Filters / Ensemble"]
    M --> R["🎯 Better Recall<br/>+ Better Precision"]
    
    style B fill:#fce4ec,color:#000000
    style M fill:#e3f2fd,color:#000000
    style R fill:#e8f5e9,color:#000000
```

The best single retriever is good. **Combining strategies is better.**

## Summary

| Retriever | Use When |
|-----------|----------|
| `MultiQueryRetriever` | Users might phrase questions differently |
| `SelfQueryRetriever` | Your documents have rich metadata (dates, categories) |
| `EnsembleRetriever` | You want the best of keyword + semantic search |
