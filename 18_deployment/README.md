# 18 — Deployment

## Why deployment?

A LangChain app running in your terminal isn't useful to anyone else. This lesson wraps a RAG chain in a FastAPI server and shows how to Dockerize it.

## What you'll learn

- FastAPI + LangChain — expose chains as HTTP endpoints
- Streaming responses with FastAPI's `StreamingResponse`
- Environment-based configuration
- A `Dockerfile` for containerized deployment

## Key idea

For production, add auth, rate limiting, monitoring (LangSmith), and horizontal scaling behind a load balancer.
