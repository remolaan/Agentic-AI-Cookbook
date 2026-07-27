from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing import Annotated, TypedDict
import operator

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    question: str
    contexts: Annotated[list[dict], operator.add]
    best_context: str
    answer: str


def fan_out(state: State):
    pass


def route_to_retrievers(state: State) -> list[Send]:
    return [Send("retrieve", {"source": src, "question": state["question"]}) for src in ["docs", "web", "knowledge"]]


def retrieve(state: dict) -> dict:
    prompts = {
        "docs": f"Answer based on technical documentation: {state['question']}",
        "web": f"Answer based on web search results: {state['question']}",
        "knowledge": f"Answer based on general knowledge: {state['question']}",
    }
    result = llm.invoke(prompts[state["source"]])
    return {"contexts": [{"source": state["source"], "text": result.content}]}


def rerank(state: State) -> dict:
    items = "\n\n".join([f"[{c['source']}] {c['text'][:100]}" for c in state["contexts"]])
    prompt = f"Question: {state['question']}\n\nCandidates:\n{items}\n\nWhich source is most relevant? Just say: docs, web, or knowledge"
    best = llm.invoke(prompt).content.strip().lower()
    best_source = "docs" if "docs" in best else ("web" if "web" in best else "knowledge")
    best_text = next((c["text"] for c in state["contexts"] if c["source"] == best_source), state["contexts"][0]["text"])
    return {"best_context": best_text}


def generate(state: State) -> dict:
    prompt = ChatPromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}\nAnswer:")
    chain = prompt | llm | StrOutputParser()
    return {"answer": chain.invoke({"context": state["best_context"], "question": state["question"]})}


builder = StateGraph(State)
builder.add_node("fan_out", fan_out)
builder.add_node("retrieve", retrieve)
builder.add_node("rerank", rerank)
builder.add_node("generate", generate)
builder.add_edge(START, "fan_out")
builder.add_conditional_edges("fan_out", route_to_retrievers, ["retrieve"])
builder.add_edge("retrieve", "rerank")
builder.add_edge("rerank", "generate")
builder.add_edge("generate", END)

graph = builder.compile()

result = graph.invoke({"question": "What is a transformer model?", "contexts": [], "best_context": "", "answer": ""})
print(f"Q: What is a transformer model?")
print(f"A: {result['answer'][:200]}...")
