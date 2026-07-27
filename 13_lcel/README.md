# 13 — LCEL (LangChain Expression Language)

## What is LCEL?

LCEL is the modern way to build chains using the `|` operator. It's declarative, composable, and automatically supports streaming, async, and batch.

## What you'll learn

- `RunnablePassthrough` — pass data through unchanged
- `RunnableParallel` — run multiple chains in parallel
- `RunnableBranch` — conditionally route between chains
- `.assign()` — add computed fields to a dict
- Building complex DAGs with `|`

## Key idea

Everything in LCEL is a `Runnable`. If you can `|` it, you can stream it, batch it, and trace it.
