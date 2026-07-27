from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


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
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
llm_with_tools = llm.bind_tools(tools)


def agent(state: MessagesState) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

result = graph.invoke({"messages": [HumanMessage("What's 5 * 3 and weather in Paris?")]})
for m in result["messages"]:
    role = type(m).__name__
    if m.content:
        print(f"  [{role}] {m.content[:80]}")
    elif hasattr(m, "tool_calls") and m.tool_calls:
        print(f"  [{role}] 🛠️ {[t['name'] for t in m.tool_calls]}")
