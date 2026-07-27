# 09 — Vector Stores

## What are vector stores?

Text is converted into numerical **embeddings** (vectors) that capture meaning. Vector stores index these vectors and let you find documents by **semantic similarity** — not keyword matching.

## What you'll learn

- `FakeEmbeddings` — quick demo (swap to real ones in production)
- `Chroma` — a lightweight, in-memory vector store (zero setup)
- `FAISS` — Facebook's vector search library (faster for larger datasets)
- Similarity search — find the closest chunks to a query

## Key idea

Embeddings + vector store = semantic search. "Tell me about cars" matches a document about "automobiles" even though they share no keywords.
