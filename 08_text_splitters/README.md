# 08 — Text Splitters

## Why split text?

LLMs have limited context windows. Documents must be **chunked** into smaller pieces. The splitter must preserve semantic boundaries.

## Splitters shown

| Splitter | Best for | Splits on |
|----------|----------|-----------|
| `RecursiveCharacterTextSplitter` | General text (recommended) | Paragraph → sentence → word |
| `CharacterTextSplitter` | Simple fixed-size chunks | Character count |
| `PythonCodeTextSplitter` | Python code | Functions, classes, methods |
| `MarkdownHeaderTextSplitter` | Markdown docs | Headers (preserves structure) |
| `from_language(Language.PYTHON)` | Any language | Language-aware splitting |

## Key parameters

- `chunk_size` — max characters per chunk
- `chunk_overlap` — overlap between chunks (prevents cutting sentences)
