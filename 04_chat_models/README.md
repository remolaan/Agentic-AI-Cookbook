# 04 — Chat Models

## LLMs vs Chat Models

| LLM | Chat Model |
|-----|-----------|
| Input: plain string | Input: list of messages |
| `text-davinci-003` (legacy) | `gpt-3.5-turbo`, `deepseek-chat` |
| One role: user | Three roles: system, human, AI |

DeepSeek (like GPT) is a **chat model**. You send structured messages with roles.

## What you'll learn

- System message — sets behavior/tone
- Human message — user input
- AIMessage — model response (you can feed it back for conversation)
- `ChatMessageHistory` — keep track of a multi-turn conversation

## Key idea

Chat models are stateless. To have a conversation, YOU must maintain message history and send it with every request.
