# 02 — Prompt Templates

## Why prompt templates?

Hard-coding prompts works for one-offs. In real apps you need to:
- Reuse the same structure with different values (user names, dates, products)
- Switch between system / human / AI roles
- Add **few-shot examples** to guide the model

## What you'll learn

- `ChatPromptTemplate` — multi-message templates
- `PromptTemplate` — simpler string-based templates
- `FewShotChatMessagePromptTemplate` — append examples to your prompt

## Key idea

Templates use `{variable}` placeholders. You fill them in with `.invoke()` or a chain.
