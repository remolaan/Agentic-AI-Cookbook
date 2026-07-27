from dotenv import load_dotenv
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. Synchronous streaming ---
prompt = ChatPromptTemplate.from_template("Tell me 3 fun facts about {topic}")
chain = prompt | llm | StrOutputParser()

print("=== Sync stream ===")
for chunk in chain.stream({"topic": "octopuses"}):
    print(chunk, end="", flush=True)
print("\n")

# --- 2. Async streaming ---
async def async_stream():
    print("=== Async stream ===")
    async for chunk in chain.astream({"topic": "black holes"}):
        print(chunk, end="", flush=True)
    print()

asyncio.run(async_stream())

# --- 3. Parallel async calls ---
async def parallel_calls():
    prompt = ChatPromptTemplate.from_template("Write a {tone} {length} about {topic}")
    chain = prompt | llm | StrOutputParser()

    inputs = [
        {"tone": "funny", "length": "poem", "topic": "cats"},
        {"tone": "serious", "length": "paragraph", "topic": "AI safety"},
        {"tone": "poetic", "length": "haiku", "topic": "the moon"},
    ]

    tasks = [chain.ainvoke(inp) for inp in inputs]
    results = await asyncio.gather(*tasks)

    print("=== Parallel async ===")
    for i, result in enumerate(results):
        print(f"  Result {i+1}: {result[:50]}...")

asyncio.run(parallel_calls())
