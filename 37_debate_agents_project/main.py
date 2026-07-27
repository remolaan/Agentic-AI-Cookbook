from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    topic: str
    pro_argument: str
    con_argument: str
    verdict: str


def proponent(state: State) -> dict:
    msg = [SystemMessage("You argue IN FAVOR of everything. Be enthusiastic and persuasive."),
           HumanMessage(state["topic"])]
    return {"pro_argument": llm.invoke(msg).content}


def opponent(state: State) -> dict:
    msg = [SystemMessage("You argue AGAINST everything. Be critical and skeptical."),
           HumanMessage(state["topic"])]
    return {"con_argument": llm.invoke(msg).content}


def judge(state: State) -> dict:
    prompt = f"Topic: {state['topic']}\n\nFOR:\n{state['pro_argument']}\n\nAGAINST:\n{state['con_argument']}\n\nWho won? State your verdict and why."
    return {"verdict": llm.invoke(prompt).content}


builder = StateGraph(State)
builder.add_node("proponent", proponent)
builder.add_node("opponent", opponent)
builder.add_node("judge", judge)
builder.add_edge(START, "proponent")
builder.add_edge(START, "opponent")
builder.add_edge("proponent", "judge")
builder.add_edge("opponent", "judge")
builder.add_edge("judge", END)

graph = builder.compile()

result = graph.invoke({"topic": "Is AI a net positive for humanity?", "pro_argument": "", "con_argument": "", "verdict": ""})
print("=== Pro Argument ===\n", result["pro_argument"][:200], "...\n")
print("=== Con Argument ===\n", result["con_argument"][:200], "...\n")
print("=== Verdict ===\n", result["verdict"])
