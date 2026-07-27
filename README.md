# LangChain Learning Repository

A step-by-step journey through LangChain — from your first LLM call to production-ready deployments.

## Prerequisites

- Python 3.12 (3.11 works too)
- A [DeepSeek API key](https://platform.deepseek.com) (free to sign up)

## Quick Start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your DEEPSEEK_API_KEY
```

## Lessons

| # | Topic | What you'll learn |
|---|-------|-------------------|
| 00 | **Setup** | Verify your environment works |
| 01 | Hello LLM | First LLM call, basic completion |
| 02 | Prompt Templates | Structured prompts, variables, few-shot |
| 03 | Output Parsers | Structured outputs (list, JSON, Pydantic) |
| 04 | Chat Models | System/human/ai messages, chat history |
| 05 | Chains | LLMChain, SequentialChain, RouterChain |
| 06 | Memory | Conversation memory, summaries, windowing |
| 07 | Document Loaders | Load PDF, CSV, HTML, YouTube, Wikipedia |
| 08 | Text Splitters | Chunking strategies, semantic splitting |
| 09 | Vector Stores | Embeddings, Chroma/FAISS, similarity search |
| 10 | RAG | Full retrieve → augment → generate pipeline |
| 11 | Advanced Retrieval | Self-query, multi-query, ensemble retrievers |
| 12 | Agents | ReAct, tools, toolkits, agent executors |
| 13 | LCEL | LangChain Expression Language, runnables |
| 14 | Callbacks & Streaming | Tracing, token-by-token output |
| 15 | Evaluation | Testing and scoring LLM outputs |
| 16 | Caching & Rate Limits | Cache layers, throttling |
| 17 | Streaming & Async | Async chains, streaming to HTTP |
| 18 | Deployment | FastAPI wrapper, Docker, env config |

## Running a lesson

```bash
python 01_hello_llm/main.py
```

Every lesson is self-contained. The README in each folder explains the concepts.
