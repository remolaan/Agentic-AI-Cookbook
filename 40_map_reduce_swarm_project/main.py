from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing import Annotated, TypedDict
import operator

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    items: list[str]
    results: Annotated[list[str], operator.add]
    final: str


def fan_out(state: State):
    pass


def route_items(state: State) -> list[Send]:
    return [Send("worker", {"item": item}) for item in state["items"]]


def worker(state: dict) -> dict:
    response = llm.invoke(f"Summarize this in one sentence: {state['item']}")
    return {"results": [f"- {state['item']} → {response.content.strip()}"]}


def collector(state: State) -> dict:
    return {"final": "\n".join(state["results"])}


builder = StateGraph(State)
builder.add_node("fan_out", fan_out)
builder.add_node("worker", worker)
builder.add_node("collector", collector)
builder.add_edge(START, "fan_out")
builder.add_conditional_edges("fan_out", route_items, ["worker"])
builder.add_edge("worker", "collector")
builder.add_edge("collector", END)

graph = builder.compile()

items = [
    "Python is a versatile programming language.",
    "Chroma is a vector database for AI.",
    "LangChain simplifies LLM application development.",
]
result = graph.invoke({"items": items, "results": [], "final": ""})
print("=== Summaries ===\n")
print(result["final"])
