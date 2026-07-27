from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

load_dotenv()


class State(TypedDict):
    text: str
    steps: int


def node_a(state: State) -> dict:
    return {"text": state["text"].upper(), "steps": state["steps"] + 1}


def node_b(state: State) -> dict:
    return {"text": state["text"] + "!!", "steps": state["steps"] + 1}


builder = StateGraph(State)
builder.add_node("capitalize", node_a)
builder.add_node("exclaim", node_b)
builder.add_edge(START, "capitalize")
builder.add_edge("capitalize", "exclaim")
builder.add_edge("exclaim", END)

graph = builder.compile()

result = graph.invoke({"text": "hello world", "steps": 0})
print(f"Result: {result}")
print(f"Text: {result['text']}")
print(f"Steps: {result['steps']}")
