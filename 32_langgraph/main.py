from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.errors import GraphRecursionError
from langgraph.types import RetryPolicy
import random

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

attempts = [0]


def risky_node(state: MessagesState) -> dict:
    attempts[0] += 1
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return {"messages": [llm.invoke(state["messages"])]}


def safe_node(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("risky", risky_node, retry=RetryPolicy(
    initial_interval=0.1,
    max_attempts=3,
    backoff_factor=2,
))
builder.add_node("safe", safe_node)
builder.add_edge(START, "risky")
builder.add_edge("risky", "safe")
builder.add_edge("safe", END)

graph = builder.compile()

try:
    result = graph.invoke(
        {"messages": [HumanMessage("Say hello")]},
        {"recursion_limit": 10},
    )
    print(f"✅ Success after {attempts[0]} attempt(s)")
    print(f"AI: {result['messages'][-1].content[:60]}")
except GraphRecursionError:
    print("❌ Hit recursion limit!")
except Exception as e:
    print(f"❌ Failed after {attempts[0]} attempts: {type(e).__name__}")

print(f"\nNode 'risky' was called {attempts[0]} time(s)")
