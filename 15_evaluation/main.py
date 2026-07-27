from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.evaluation import load_evaluator, EvaluatorType

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. Criteria evaluation (score against a criterion) ---
evaluator = load_evaluator(
    "criteria",
    llm=llm,
    criteria="conciseness",
)

response = llm.invoke("What is Python?")
result = evaluator.evaluate_strings(
    prediction=response.content,
    input="What is Python?",
)
print("=== Criteria Evaluation (conciseness) ===")
print(f"Score: {result.get('score')}")
print(f"Reasoning: {result.get('reasoning')}")
print()

# --- 2. Labeled criteria (with reference answer) ---
evaluator = load_evaluator(
    "labeled_criteria",
    llm=llm,
    criteria="correctness",
)

result = evaluator.evaluate_strings(
    prediction="Python is a snake.",
    reference="Python is a high-level programming language.",
    input="What is Python?",
)
print("=== Labeled Criteria Evaluation ===")
print(f"Score: {result.get('score')}")
print(f"Reasoning: {result.get('reasoning')}")
print()

# --- 3. Simple test loop ---
test_cases = [
    {"question": "What is 2+2?", "expected": "4"},
    {"question": "What is the capital of France?", "expected": "Paris"},
]

print("=== Test Loop ===")
for i, case in enumerate(test_cases):
    response = llm.invoke(case["question"])
    result = evaluator.evaluate_strings(
        prediction=response.content,
        reference=case["expected"],
        input=case["question"],
    )
    print(f"  Q{i+1}: {case['question']}")
    print(f"  Score: {result.get('score')}")
    print()
