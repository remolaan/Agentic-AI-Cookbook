from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from typing import TypedDict

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


@tool
def python_repl(code: str) -> str:
    "Run Python code (simulated)."
    return f"Output of: {code}"


coder = create_react_agent(llm.bind_tools([python_repl]), [python_repl],
    prompt="You are a Python expert. Write and explain code.")
writer = create_react_agent(llm, [],
    prompt="You are a creative writer. Write engaging content.")
analyst = create_react_agent(llm, [],
    prompt="You are a data analyst. Provide clear analysis and insights.")

specialists = {"code": coder, "write": writer, "analyze": analyst}


class State(TypedDict):
    query: str
    category: str
    output: str


def router(state: State) -> dict:
    prompt = f"Categories: code, write, analyze. Which fits? Reply with just the word: {state['query']}"
    cat = llm.invoke(prompt).content.strip().lower()
    cat = "code" if "code" in cat else ("analyze" if "analyze" in cat else "write")
    return {"category": cat}


def run_specialist(state: State) -> dict:
    agent = specialists[state["category"]]
    result = agent.invoke({"messages": [HumanMessage(state["query"])]})
    return {"output": result["messages"][-1].content}


def route(state: State) -> str:
    return state["category"]


builder = StateGraph(State)
builder.add_node("router", router)
builder.add_node("code", run_specialist)
builder.add_node("write", run_specialist)
builder.add_node("analyze", run_specialist)
builder.add_edge(START, "router")
builder.add_conditional_edges("router", route, {"code": "code", "write": "write", "analyze": "analyze"})
builder.add_edge("code", END)
builder.add_edge("write", END)
builder.add_edge("analyze", END)

graph = builder.compile()

for q in ["Write a poem about Python", "What is 2+2? analyze it"]:
    result = graph.invoke({"query": q, "category": "", "output": ""})
    print(f"\n=== Query: {q[:30]}... ===")
    print(f"→ Routed to: {result['category']}")
    print(f"→ {result['output'][:100]}...")
