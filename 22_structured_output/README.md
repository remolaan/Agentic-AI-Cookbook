# 22 — Structured Output with `with_structured_output()`

## What is Structured Output?

`with_structured_output()` is the **modern** way to get structured data from an LLM. It uses the model's native tool-calling / JSON mode internally — cleaner than `PydanticOutputParser`.

## Code Walkthrough

### `with_structured_output()`
```python
class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    hobbies: list[str] = Field(description="List of hobbies")

structured_llm = llm.with_structured_output(Person, method="function_calling")
result = structured_llm.invoke("Generate a fictional person who loves coding")
print(result.name, result.age, result.hobbies)
```
**What it does:** Creates a new LLM wrapper that **guarantees** structured output. Internally it uses tool calling: it tells the LLM to "call a function" matching your Pydantic model, then parses the arguments into a validated `Person` instance. `result` is a Python `Person` object — you access fields with `result.name`, not string parsing.

**Why `method="function_calling"`:** DeepSeek doesn't support OpenAI's JSON mode. `method="function_calling"` works with any model that supports tool calling. For OpenAI models, the default method works without this parameter.

### Nested models
```python
class Employee(BaseModel):
    address: Address  # ← nested Pydantic model
```
**What it does:** Pydantic models can nest other models. `with_structured_output` handles nesting automatically — the LLM generates nested JSON, and it's validated recursively into Python objects.

### Literal types
```python
class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
```
**What it does:** `Literal` restricts the field to exact string values. The LLM must choose one of the allowed options. Combined with `confidence: float` with `ge=0, le=1`, you get validated, constrained output.

### Extraction pattern
```python
text = "Sarah Johnson, a 34-year-old software engineer..."
result = extractor.invoke(f"Extract info from: {text}")
```
**What it does:** The same `with_structured_output` pattern works for **information extraction** — pass unstructured text and get structured fields back. No regex or manual parsing needed.

## Visual

```mermaid
flowchart LR
    P["📝 Prompt"] --> M["🤖 LLM"]
    M --> S["with_structured_output(PydanticModel)"]
    S --> O["✅ Validated Python object"]
    
    style M fill:#e3f2fd,stroke:#1565c0,color:#000000
    style S fill:#f3e5f5,stroke:#7b1fa2,color:#000000
    style O fill:#e8f5e9,stroke:#2e7d32,color:#000000
```
