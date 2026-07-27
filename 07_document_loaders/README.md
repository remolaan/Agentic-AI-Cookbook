# 07 — Document Loaders

## What are document loaders?

Document loaders ingest data from various sources and convert them into LangChain `Document` objects (`page_content` + `metadata`).

## Loaders shown

| Loader | Source | Format |
|--------|--------|--------|
| `TextLoader` | Local file | `.txt` |
| `CSVLoader` | Local file | `.csv` |
| `JSONLoader` | Local file | `.json` (with jq queries) |
| `DirectoryLoader` | Directory | Any (filter by glob) |
| `WebBaseLoader` | URL | HTML |
| `WikipediaLoader` | Wikipedia | Wiki articles |
| `UnstructuredMarkdownLoader` | Local file | `.md` |

**Tip:** LangChain has 100+ loaders. Install the right package for your source (e.g., `pypdf` for PDFs, `unstructured` for Word/PPT).
