# 06 — Memory

## Why memory?

LLMs are stateless — they don't remember past turns. **Memory** gives your chain a short-term or long-term recollection of the conversation so far.

## What you'll learn

- `ConversationBufferMemory` — keeps a full transcript
- `ConversationBufferWindowMemory` — keeps only the last N messages
- `ConversationSummaryMemory` — summarizes older messages to save tokens
- `ConversationKGMemory` — extracts and stores knowledge graph triples

## Key idea

Memory works by modifying the prompt: it injects the conversation history before your new message.
