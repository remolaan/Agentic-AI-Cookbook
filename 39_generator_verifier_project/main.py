from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    topic: str
    draft: str
    feedback: str
    passed: bool
    attempts: int


def generate(state: State) -> dict:
    feedback = state.get("feedback", "")
    prompt = f"Write a clear explanation of: {state['topic']}"
    if feedback:
        prompt += f"\n\nPrevious feedback to address: {feedback}"
    return {"draft": llm.invoke(prompt).content, "attempts": state["attempts"] + 1}


def verify(state: State) -> dict:
    prompt = f"Evaluate this explanation of '{state['topic']}'. Score pass/fail. If fail, explain why:\n\n{state['draft']}"
    result = llm.invoke(prompt).content.lower()
    passed = "pass" in result and "fail" not in result.split(".")[0]
    feedback = result if not passed else ""
    return {"passed": passed, "feedback": feedback}


def should_continue(state: State) -> str:
    if state["passed"] or state["attempts"] >= 3:
        return "end"
    return "generate"


builder = StateGraph(State)
builder.add_node("generate", generate)
builder.add_node("verify", verify)
builder.add_edge(START, "generate")
builder.add_edge("generate", "verify")
builder.add_conditional_edges("verify", should_continue, {"generate": "generate", "end": END})

graph = builder.compile()

result = graph.invoke({"topic": "How does a transformer model work?", "draft": "", "feedback": "", "passed": False, "attempts": 0})
print(f"=== Result after {result['attempts']} attempt(s) ===")
print(f"Passed: {result['passed']}")
print(f"\nDraft:\n{result['draft'][:200]}...")
