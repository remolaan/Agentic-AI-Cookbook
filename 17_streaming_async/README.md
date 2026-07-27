# 17 — Streaming & Async

## Why streaming?

Websites and APIs need to show responses as they're generated — not wait 10 seconds for the full output. Streaming sends tokens one by one.

## What you'll learn

- `.stream()` — iterate over tokens as they arrive
- `.astream()` — async streaming with `async for`
- `.ainvoke()` — async version of `.invoke()`
- `asyncio.gather()` — run multiple LLM calls in parallel

## Key idea

Streaming is built into LCEL. Any `Runnable` that supports streaming will stream automatically through `|`.
