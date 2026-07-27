from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    input: str
    sentiment: str


def analyze_sentiment(state: State) -> dict:
    response = llm.invoke(
        f"Classify the sentiment as 'positive' or 'negative': {state['input']}"
    )
    sentiment = response.content.strip().lower()
    sentiment = "positive" if "positive" in sentiment else "negative"
    return {"sentiment": sentiment}


def handle_positive(state: State) -> dict:
    response = llm.invoke(f"The user said something positive: {state['input']}. Reply warmly.")
    return {"input": response.content}


def handle_negative(state: State) -> dict:
    response = llm.invoke(f"The user said something negative: {state['input']}. Reply empathetically.")
    return {"input": response.content}


def router(state: State) -> str:
    return state["sentiment"]


builder = StateGraph(State)
builder.add_node("analyze", analyze_sentiment)
builder.add_node("positive", handle_positive)
builder.add_node("negative", handle_negative)
builder.add_edge(START, "analyze")
builder.add_conditional_edges("analyze", router, {"positive": "positive", "negative": "negative"})
builder.add_edge("positive", END)
builder.add_edge("negative", END)

graph = builder.compile()

for text in ["I love this!", "This is terrible."]:
    result = graph.invoke({"input": text, "sentiment": ""})
    print(f"Input: {text}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Output: {result['input'][:60]}...\n")
