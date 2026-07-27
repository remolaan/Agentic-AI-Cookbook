# AGENTS.md — LangChain Learning Repository

## Project purpose
Educational repo teaching LangChain from beginner to advanced, topic-by-topic. Each `XX_topic_name/` folder is a self-contained lesson with a `README.md` (concepts) and `main.py` (runnable code). All lessons build sequentially but can be run independently.

## LLM provider
- **DeepSeek Chat** via OpenAI-compatible API: `ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")`
- API key goes in `.env`: `OPENAI_API_KEY=sk-...`
- Do NOT use `langchain-deepseek` package — use `langchain-openai` with custom `base_url`

## Setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then add your DeepSeek key
```

## Running lessons
```bash
# from repo root, activate venv first
python 01_hello_llm/main.py
python 02_prompt_templates/main.py
# ... any lesson independently
```

## Structure
- `00_setup/` — verify environment works (make a single LLM call)
- `01–05/` — Beginner: LLM, prompts, parsers, chat models, chains
- `06–10/` — Intermediate: memory, document loaders, splitters, vector stores, RAG
- `11–15/` — Advanced: retrieval strategies, agents, LCEL, callbacks, evaluation
- `16–18/` — Production: caching, streaming/async, deployment (FastAPI)

## Embeddings
- DeepSeek has no embedding endpoint → lessons 09, 10, 11, 18 use `FakeEmbeddings`
- To use real semantic search, install `sentence-transformers` + `torch` or bring your own OpenAI key

## Key constraints
- Python 3.12 required (3.11 also works, not 3.6)
- Root `README.md` is the roadmap — update it when adding/renaming topics
- `.gitignore` must include `.venv/`, `.env`, `__pycache__/`, `*.egg-info/`
- Only edit `/home/lan/langchain/` — this is the repo root
- Do NOT commit unless explicitly asked
- Do NOT add secrets/keys to any file that could be committed
