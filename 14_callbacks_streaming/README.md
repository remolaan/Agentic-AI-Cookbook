# 14 — Callbacks & Streaming

## Why callbacks?

Callbacks let you hook into the LLM lifecycle: when a request starts, when a token arrives, when an error occurs. You use them for logging, monitoring, token counting, and UIs.

## What you'll learn

- `BaseCallbackHandler` — create custom handlers
- Streaming tokens in real-time
- Counting tokens with a callback
- LangSmith integration (optional)

## Key idea

Callbacks are the standard way to observe and extend LangChain without modifying your chain code.
