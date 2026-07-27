# 03 — Output Parsers

## Why output parsers?

LLMs return raw text. **Parsers** convert that text into structured data — lists, datetimes, Pydantic objects, or JSON.

## What you'll learn

| Parser | Input → Output | Use case |
|--------|---------------|----------|
| `StrOutputParser` | raw text → cleaned string | Simple answers |
| `CommaSeparatedListOutputParser` | "a, b, c" → `["a","b","c"]` | Lists |
| `PydanticOutputParser` | text → validated Pydantic class | Structured data (classic) |
| `DatetimeOutputParser` | text → `datetime` object | Dates/times |
| `OutputFixingParser` | bad output → auto-fixed output | Error recovery |
| `JsonOutputParser` | text → Python dict/list | JSON data |

## Modern vs Classic

For structured output in modern LangChain, prefer `.with_structured_output()` (see lesson 22) over `PydanticOutputParser`. Both are shown here since you'll encounter both.
