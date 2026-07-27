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


tools = [multiply]
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com").bind_tools(tools)


def agent(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

print("=== Mermaid Diagram ===")
print(graph.get_graph().draw_mermaid())
print()

print("=== ASCII Diagram ===")
print(graph.get_graph().draw_ascii())
print()

print("=== Node Count ===")
print(f"  {len(graph.get_graph().nodes)} nodes")
