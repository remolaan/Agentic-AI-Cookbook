# 15 — Evaluation

## Why evaluate?

LLM outputs are non-deterministic. You need systematic evaluation to detect regressions, measure quality, and tune prompts.

## What you'll learn

- String evaluators — score a single output
- `CriteriaEvalChain` — evaluate against custom criteria
- `LabeledCriteriaEvalChain` — evaluate against a reference answer
- Building a simple test dataset

## Key idea

Evaluating LLMs is hard. Start with simple criteria (conciseness, correctness, harmlessness) and iterate.
