from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing import Annotated, TypedDict
import operator

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    task: str
    topics: list[str]
    sections: Annotated[list[str], operator.add]
    report: str


def supervisor(state: State) -> dict:
    response = llm.invoke(f"Break this task into 3 subtopics. One per line:\n{state['task']}")
    topics = [t.strip("- ").strip() for t in response.content.strip().split("\n") if t.strip()]
    return {"topics": topics[:3]}


def router(state: State) -> list[Send]:
    return [Send("worker", {"topic": t}) for t in state["topics"]]


def worker(state: dict) -> dict:
    response = llm.invoke(f"Write 2 sentences about: {state['topic']}")
    return {"sections": [f"## {state['topic']}\n{response.content.strip()}"]}


def joiner(state: State) -> dict:
    return {"report": "\n\n".join(state["sections"])}


builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("worker", worker)
builder.add_node("joiner", joiner)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", router, ["worker"])
builder.add_edge("worker", "joiner")
builder.add_edge("joiner", END)

graph = builder.compile()

result = graph.invoke({"task": "Explain benefits of exercise", "topics": [], "sections": [], "report": ""})
print("=== Final Report ===\n")
print(result["report"])
