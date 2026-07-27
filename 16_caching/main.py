from dotenv import load_dotenv
import time
from langchain_openai import ChatOpenAI
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache
from langchain_classic.globals import set_llm_cache
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- 1. InMemoryCache ---
set_llm_cache(InMemoryCache())

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

start = time.perf_counter()
r1 = llm.invoke("What is the speed of light?")
print(f"First call: {time.perf_counter() - start:.2f}s")

start = time.perf_counter()
r2 = llm.invoke("What is the speed of light?")
print(f"Cached call: {time.perf_counter() - start:.2f}s")
print(f"Same result: {r1.content == r2.content}")
print()

# --- 2. SQLiteCache (persistent) ---
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

start = time.perf_counter()
r1 = llm.invoke("Tell me a joke about programming.")
print(f"First call: {time.perf_counter() - start:.2f}s")

start = time.perf_counter()
r2 = llm.invoke("Tell me a joke about programming.")
print(f"Cached call: {time.perf_counter() - start:.2f}s")
print()

# Cleanup
import os
os.remove(".langchain_cache.db")
