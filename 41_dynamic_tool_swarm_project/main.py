from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.types import Send
from typing import Annotated, Sequence
import operator

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


@tool
def search_web(query: str) -> str:
    return f"Simulated result for: {query}"

@tool
def calculate(expr: str) -> str:
    return f"Calculated: {eval(expr)}"

@tool
def get_time(city: str) -> str:
    return f"Time in {city}: 12:00 PM"

tools = [search_web, calculate, get_time]
llm_with_tools = llm.bind_tools(tools)


class State(MessagesState):
    tool_outputs: Annotated[list[str], operator.add]


def agent(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def dispatch(state: State) -> list[Send]:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return [Send("tool_runner", {"tc": tc}) for tc in last.tool_calls]
    return []


def tool_runner(state: dict) -> dict:
    tc = state["tc"]
    tool_map = {t.name: t for t in tools}
    tool = tool_map.get(tc["name"])
    if tool:
        result = tool.invoke(tc["args"])
        return {"tool_outputs": [f"{tc['name']}({tc['args']}) = {result}"]}
    return {"tool_outputs": [f"Unknown tool: {tc['name']}"]}


def final_answer(state: State) -> dict:
    context = "\n".join(state["tool_outputs"])
    prompt = f"Tool results:\n{context}\n\nAnswer the original question based on these results."
    return {"messages": [AIMessage(content=llm.invoke(prompt).content)]}


builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("dispatch", dispatch)
builder.add_node("tool_runner", tool_runner)
builder.add_node("final_answer", final_answer)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent",
    lambda s: [Send("tool_runner", {"tc": tc}) for tc in (s["messages"][-1].tool_calls if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else [])],
    ["tool_runner"])
builder.add_edge("tool_runner", "final_answer")
builder.add_edge("final_answer", END)

graph = builder.compile()

result = graph.invoke({"messages": [HumanMessage("What's 15*24 and time in Paris?")], "tool_outputs": []})
for m in result["messages"]:
    if m.content:
        print(f"[{type(m).__name__}] {m.content[:100]}")
print(f"\nTool outputs: {result.get('tool_outputs', [])}")
