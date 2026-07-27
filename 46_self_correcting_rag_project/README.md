# 46 — Self-Correcting RAG

Retrieve → generate → **verify**. If the answer is bad, re-retrieve with refined query and try again.

```mermaid
flowchart TD
    Q["Question"] --> R["🔍 Retrieve"]
    R --> G["🤖 Generate"]
    G --> V["🔎 Verify"]
    V -->|"✅ Good"| O["Output"]
    V -->|"❌ Bad"| RQ["🔄 Refine query"]
    RQ --> R
    style V fill:#fff3e0,stroke:#e65100,color:#000000
    style RQ fill:#f3e5f5,stroke:#7b1fa2,color:#000000
```

## Code Walkthrough

```python
def retrieve(state: State) -> dict:
    result = llm.invoke(f"Search for: {state['query']}")
    return {"context": result.content}

def generate(state: State) -> dict:
    chain = ChatPromptTemplate.from_template("Context: {context}\nQuestion: {question}") | llm | StrOutputParser()
    return {"answer": chain.invoke({"context": state["context"], "question": state["question"]})}

def verify(state: State) -> dict:
    result = llm.invoke(f"Question: {state['question']}\nAnswer: {state['answer']}\nReply PASS or FAIL.")
    return {"passed": "pass" in result.content.lower().split(".")[0]}

def refine(state: State) -> dict:
    return {"query": llm.invoke(f"Suggest a better search query: {state['question']}").content.strip()}

def should_continue(state: State) -> str:
    if state["passed"] or state["attempts"] >= 3:
        return "end"
    return "refine"
```

**What each node does:**
- **`retrieve`** — Searches using the current `query`. First attempt uses the original query. Later attempts use refined queries.
- **`generate`** — Standard RAG: context + question → prompt → LLM → answer.
- **`verify`** — Judges the answer. Returns PASS or FAIL. Simple binary gate.
- **`refine`** — If FAIL, asks the LLM for a better search query and loops back to `retrieve`.
- **`should_continue`** — Conditional edge: pass → END. Fail + attempts < 3 → refine + loop. Fail + attempts >= 3 → END.

**Data flow:** query → retrieve → generate → verify → (PASS → END) OR (FAIL → refine query → retrieve again).

## What you'll build

- Retriever node (simulated with LLM)
- Generator node produces answer
- Verifier node scores answer (pass/fail)
- On fail: refine the query and loop back to retrieve
- Max 3 attempts
