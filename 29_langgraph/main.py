from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing import Annotated, TypedDict, Sequence
import operator

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    topics: list[str]
    results: Annotated[list[str], operator.add]


def fan_out(state: State):
    pass


def analyze(state: dict) -> dict:
    response = llm.invoke(
        f"Classify sentiment of: '{state['topic']}'. Reply 'positive', 'negative', or 'neutral'."
    )
    return {"results": [f"[{state['topic']}] {response.content.strip().lower()}"]}


def route_topics(state: State) -> list[Send]:
    return [Send("analyze", {"topic": t}) for t in state["topics"]]


builder = StateGraph(State)
builder.add_node("fan_out", fan_out)
builder.add_node("analyze", analyze)
builder.add_edge(START, "fan_out")
builder.add_conditional_edges("fan_out", route_topics, ["analyze"])
builder.add_edge("analyze", END)

graph = builder.compile()

result = graph.invoke({
    "topics": ["I love this!", "This is terrible.", "It's okay I guess."],
    "results": [],
})
print("=== Sentiment Results ===")
for r in result["results"]:
    print(f"  {r}")
