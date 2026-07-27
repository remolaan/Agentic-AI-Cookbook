# 08 — Text Splitters

## Why split text?

LLMs have limited context windows. Long documents must be **chunked** into smaller pieces before embedding and retrieval. The splitter must preserve semantic boundaries so each chunk is meaningful on its own.

## What you'll learn

- `RecursiveCharacterTextSplitter` — splits on paragraph → sentence → word (recommended default)
- `CharacterTextSplitter` — splits on a fixed character count
- Token-aware splitting — uses the model's tokenizer, not raw characters
- `chunk_size` and `chunk_overlap` — the two key parameters

## Key idea

Good chunking = smaller than context window but large enough to be self-contained. Overlap prevents cutting a sentence in half.
