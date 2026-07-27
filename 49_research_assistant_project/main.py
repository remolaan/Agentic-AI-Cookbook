from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Send
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, TypedDict
import operator

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
store = InMemoryStore()


class ResearchState(TypedDict):
    question: str
    sections: Annotated[list[str], operator.add]
    report: str


def supervisor(state: ResearchState) -> Send:
    prompt = f"Research topic: {state['question']}\nWhat 3 aspects should we research? One per line."
    topics = [t.strip("- ").strip() for t in llm.invoke(prompt).content.strip().split("\n") if t.strip()]
    return {"topics": topics[:3]}


def router(state: ResearchState) -> list[Send]:
    topics = state.get("topics", ["overview", "key developments", "future outlook"])
    return [Send("worker", {"aspect": t, "question": state["question"]}) for t in topics]


def worker(state: dict) -> dict:
    response = llm.invoke(f"Research this aspect of '{state['question']}': {state['aspect']}. Write 2-3 sentences.")
    return {"sections": [f"## {state['aspect']}\n{response.content.strip()}"]}


def compiler(state: ResearchState) -> dict:
    report = f"# Research: {state['question']}\n\n" + "\n\n".join(state["sections"])
    store.put(("research", state["question"].lower()[:20]), "report", {"report": report})
    return {"report": report}


builder = StateGraph(ResearchState)
builder.add_node("supervisor", supervisor)
builder.add_node("worker", worker)
builder.add_node("compiler", compiler)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", router, ["worker"])
builder.add_edge("worker", "compiler")
builder.add_edge("compiler", END)

graph = builder.compile(store=store)

result = graph.invoke({"question": "Impact of AI on healthcare", "sections": [], "report": ""})
print("=== Research Report ===\n")
print(result["report"][:300])
print("...\n")

# Retrieve from memory
items = list(store.search(("research",)))
print(f"=== Stored in memory: {len(list(store.search(('research',))))} report(s) ===")
for item in store.search(("research",)):
    print(f"  - {item.key}")
