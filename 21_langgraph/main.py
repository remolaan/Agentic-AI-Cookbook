from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, create_react_agent
from typing import TypedDict, Annotated, Sequence
import operator

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# ============================================================
# 1. Define tools
# ============================================================
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    data = {"tokyo": "15°C", "paris": "22°C", "london": "12°C"}
    return data.get(city.lower(), f"No data for {city}")

tools = [multiply, get_weather]

# ============================================================
# 2. Prebuilt LangGraph agent (simplest)
# ============================================================
print("=== 1. create_react_agent (prebuilt) ===")
agent = create_react_agent(llm, tools)
response = agent.invoke({"messages": [HumanMessage("What's 5 * 3 and weather in Paris?")]})
for m in response["messages"]:
    role = type(m).__name__
    content = m.content if m.content else "[tool call]"
    print(f"  [{role}] {content[:100]}")
print()

# ============================================================
# 3. Custom StateGraph (full control)
# ============================================================
print("=== 2. Custom StateGraph ===")

class AgentState(TypedDict):
    messages: Annotated[Sequence, operator.add]
    next: str

from langchain_core.messages import AIMessage
import json

def call_model(state):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return "end"

tool_node = ToolNode(tools)

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "agent")

app = graph.compile()

result = app.invoke({"messages": [HumanMessage("Multiply 7 by 8")]})
for m in result["messages"]:
    role = type(m).__name__
    content = m.content if m.content else "[tool call]"
    print(f"  [{role}] {content[:100]}")
print()

# ============================================================
# 4. System prompt + persistent state
# ============================================================
print("=== 3. Agent with system prompt ===")
system = SystemMessage("You are a math tutor. Always show your work.")

result = app.invoke({"messages": [system, HumanMessage("What is 12 * 15?")]})
for m in result["messages"]:
    role = type(m).__name__
    if m.content:
        print(f"  [{role}] {m.content[:120]}")
