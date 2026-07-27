from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    question: str
    query: str
    context: str
    answer: str
    passed: bool
    attempts: int


def retrieve(state: State) -> dict:
    result = llm.invoke(f"Search for information about: {state['query']}")
    return {"context": result.content, "attempts": state["attempts"] + 1}


def generate(state: State) -> dict:
    prompt = ChatPromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}\nAnswer based only on context.")
    chain = prompt | llm | StrOutputParser()
    return {"answer": chain.invoke({"context": state["context"], "question": state["question"]})}


def verify(state: State) -> dict:
    prompt = f"Question: {state['question']}\nAnswer: {state['answer']}\n\nDoes this answer the question well? Reply PASS or FAIL with reason."
    result = llm.invoke(prompt).content
    passed = "pass" in result.lower().split(".")[0]
    return {"passed": passed}


def refine(state: State) -> dict:
    prompt = f"Original: {state['question']}\nPrevious attempt: {state['answer']}\n\nSuggest a better search query to find missing information. Reply with just the query."
    return {"query": llm.invoke(prompt).content.strip()}


def should_continue(state: State) -> str:
    if state["passed"] or state["attempts"] >= 3:
        return "end"
    return "refine"


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("verify", verify)
builder.add_node("refine", refine)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "verify")
builder.add_conditional_edges("verify", should_continue, {"refine": "refine", "end": END})
builder.add_edge("refine", "retrieve")

graph = builder.compile()

result = graph.invoke({"question": "What are the latest advances in AI?", "query": "latest advances in AI 2024",
                        "context": "", "answer": "", "passed": False, "attempts": 0})
print(f"=== Result after {result['attempts']} attempt(s) ===")
print(f"Passed: {result['passed']}")
print(f"\nAnswer: {result['answer'][:200]}...")
