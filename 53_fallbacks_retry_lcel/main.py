from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. with_fallbacks — try backup if primary fails ---
primary = (
    ChatPromptTemplate.from_template("Answer concisely: {input}")
    | llm
    | StrOutputParser()
)

backup = (
    ChatPromptTemplate.from_template("Provide a brief answer to: {input}")
    | llm
    | StrOutputParser()
)

with_fallbacks = primary.with_fallbacks([backup])

print("=== 1. with_fallbacks ===")
result = with_fallbacks.invoke("What is Python?")
print(f"  {result[:80]}...\n")

# --- 2. with_retry — retry on failure ---
chain_with_retry = (
    ChatPromptTemplate.from_template("Answer concisely: {input}")
    | llm
    | StrOutputParser()
).with_retry(stop_after_attempt=3)

print("=== 2. with_retry ===")
result = chain_with_retry.invoke("What is LangChain?")
print(f"  {result[:80]}...\n")

# --- 3. with_retry on a RunnableLambda ---
import random

def flaky_call(input_dict: dict) -> str:
    if random.random() < 0.6:
        raise ValueError("Simulated random failure!")
    return llm.invoke(f"Answer: {input_dict['input']}").content

flaky_runnable = RunnableLambda(flaky_call).with_retry(stop_after_attempt=5)
chain = (
    ChatPromptTemplate.from_template("{input}")
    | flaky_runnable
)

print("=== 3. RunnableLambda + with_retry ===")
try:
    result = chain.invoke({"input": "Say hello"})
    print(f"  {result[:60]}...")
except Exception as e:
    print(f"  Failed: {e}")

# --- 4. Combined: retry first, then fallback ---
robust = chain_with_retry.with_fallbacks([backup])
print("\n=== 4. Retry + Fallback combined ===")
result = robust.invoke("Explain machine learning")
print(f"  {result[:80]}...")
