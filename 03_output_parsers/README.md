# 03 — Output Parsers

## Why output parsers?

LLMs return raw text. When you need structured data — a list, a JSON object, a typed Python object — you need a **parser** to convert the text into a usable format.

## What you'll learn

- `StrOutputParser` — strips extra whitespace, returns plain text
- `CommaSeparatedListOutputParser` — "a, b, c" → `["a", "b", "c"]`
- `PydanticOutputParser` — LLM output → validated Python dataclass

## Key idea

A parser is a **runnable** that goes at the end of your chain: `prompt | model | parser`.
