from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class SubState(TypedDict):
    text: str


def validate(state: SubState) -> dict:
    if len(state["text"]) < 3:
        return {"text": "INVALID"}
    return {"text": state["text"]}


def capitalize(state: SubState) -> dict:
    return {"text": state["text"].upper()}


sub_builder = StateGraph(SubState)
sub_builder.add_node("validate", validate)
sub_builder.add_node("capitalize", capitalize)
sub_builder.add_edge(START, "validate")
sub_builder.add_conditional_edges(
    "validate",
    lambda s: "capitalize" if s["text"] != "INVALID" else END,
    {"capitalize": "capitalize", END: END},
)
subgraph = sub_builder.compile()


class MainState(TypedDict):
    text: str
    result: str


def greet(state: MainState) -> dict:
    response = llm.invoke(f"Say hello to {state['text']}")
    return {"text": state["text"], "result": response.content}


def farewell(state: MainState) -> dict:
    return {"result": state["result"] + "\n--- Goodbye! ---"}


builder = StateGraph(MainState)
builder.add_node("greet", greet)
builder.add_node("subgraph", subgraph)
builder.add_node("farewell", farewell)
builder.add_edge(START, "greet")
builder.add_edge("greet", "subgraph")
builder.add_edge("subgraph", "farewell")
builder.add_edge("farewell", END)

graph = builder.compile()

result = graph.invoke({"text": "world", "result": ""})
print("=== Subgraph Result ===")
print(f"  Processed text: {result['text']}")
print(f"  Final result: {result['result']}")
