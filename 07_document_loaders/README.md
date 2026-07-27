# 07 — Document Loaders

## What are document loaders?

Document loaders ingest data from various sources and convert them into LangChain `Document` objects (which hold `page_content` + `metadata`).

## What you'll learn

- `TextLoader` — plain text files
- `CSVLoader` — tabular data
- `WebBaseLoader` — scrape web pages
- `WikipediaLoader` — query Wikipedia articles

## Key idea

Document loaders are the **first step** in any RAG pipeline: load → split → embed → store → retrieve → generate.
