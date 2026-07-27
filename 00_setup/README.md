# 00 — Setup

## What this is

A smoke test to confirm your environment is ready. It loads your API key, creates a ChatOpenAI client pointed at DeepSeek, and asks the model a simple question.

## What to check

- Python ≥ 3.11 is installed
- Virtual environment is activated
- `pip install -r requirements.txt` completed
- `.env` file exists with `DEEPSEEK_API_KEY=sk-...`

## Run it

```bash
python 00_setup/main.py
```

Expected output:

```
Hello from DeepSeek!
AI: Hello! How can I assist you today?
```
