from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send, Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, TypedDict
import operator

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    items: list[str]
    approved: Annotated[list[str], operator.add]
    rejected: Annotated[list[str], operator.add]


def dispatcher(state: State) -> list[Send]:
    return [Send("worker", {"item": item}) for item in state["items"]]


def worker(state: dict) -> dict:
    response = llm.invoke(f"Suggest an improvement for: {state['item']}")
    suggestion = response.content.strip()
    interrupt({"item": state["item"], "suggestion": suggestion, "question": "Approve this suggestion?"})
    return {}


def resume_worker(state: dict, config) -> dict:
    from langgraph.config import get_config
    return {"approved": [state.get("item", "unknown")]}


builder = StateGraph(State)
builder.add_node("dispatcher", dispatcher)
builder.add_node("worker", worker)
builder.add_edge(START, "dispatcher")
builder.add_conditional_edges("dispatcher", lambda s: [Send("worker", {"item": item}) for item in s["items"]], ["worker"])
builder.add_edge("worker", END)

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "swarm-1"}}
try:
    graph.invoke({"items": ["Write documentation", "Fix bug #42", "Add tests"], "approved": [], "rejected": []}, config=config)
except: pass

state = graph.get_state(config)
print("=== Pending approvals ===")
for task in state.tasks:
    for intr in task.interrupts:
        print(f"  Item: {intr.value['item']}")
        print(f"  Suggestion: {intr.value['suggestion']}")
        print()

print("Resuming all with approval...")
for task in state.tasks:
    result = graph.invoke(Command(resume="approved"), config=config)

final = graph.get_state(config)
print(f"Approved: {final.values.get('approved', [])}")
