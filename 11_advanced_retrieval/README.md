# 11 — Advanced Retrieval

## Why advanced retrieval?

Basic similarity search isn't always enough. You might need:
- **Multi-query** — generate variations of the user's question to cover different phrasings
- **Self-query** — let the LLM extract metadata filters from natural language
- **Ensemble** — combine results from multiple retrievers

## What you'll learn

- `MultiQueryRetriever` — creates multiple query variations, searches each, combines results
- `SelfQueryRetriever` — parses search filters from the question
- `EnsembleRetriever` — weighted blending of multiple retrieval strategies

## Key idea

The best single retriever is good. Combining strategies is better.
