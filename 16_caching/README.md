# 16 — Caching & Rate Limits

## Why cache?

LLM calls are slow and expensive. Cache identical requests to save time and money. Rate limits prevent hitting API quotas.

## What you'll learn

- In-memory cache — store results in a dict
- SQLite cache — persistent cache across restarts
- Rate limiting middleware — throttle requests
- `BaseCache` — implement your own cache backend

## Key idea

Cache aggressively. Use SQLite for persistence across sessions, use Redis for production multi-instance deployments.
