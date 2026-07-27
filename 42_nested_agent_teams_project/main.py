from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import create_react_agent, ToolNode, tools_condition
from langchain_core.tools import StructuredTool

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


# --- Child agent: Research specialist (subgraph) ---
def wiki_fn(query: str) -> str:
    return f"Wikipedia: {query} is an important CS concept."

def web_fn(query: str) -> str:
    return f"Web: Latest trends in {query}."

child_tools = [
    StructuredTool.from_function(func=wiki_fn, name="search_wiki", description="Search Wikipedia"),
    StructuredTool.from_function(func=web_fn, name="search_web", description="Search the web"),
]

child_agent = create_react_agent(
    llm.bind_tools(child_tools), child_tools,
    prompt="You are a research assistant. Find information using tools.",
    name="research_agent",
)


# --- Parent graph that embeds child as a subgraph node ---
def parent_agent_node(state: MessagesState) -> dict:
    return {"messages": [AIMessage(content="I'll research this topic for you.")]}


def call_child_agent(state: MessagesState) -> dict:
    result = child_agent.invoke({"messages": state["messages"] + [HumanMessage("Research this topic thoroughly.")]})
    return {"messages": result["messages"]}


builder = StateGraph(MessagesState)
builder.add_node("parent", parent_agent_node)
builder.add_node("child_agent", call_child_agent)
builder.add_edge(START, "parent")
builder.add_edge("parent", "child_agent")
builder.add_edge("child_agent", END)

graph = builder.compile()

result = graph.invoke({"messages": [HumanMessage("Tell me about transformers in AI")]})
print("=== Final Answer ===")
for m in result["messages"]:
    if m.content:
        print(f"[{type(m).__name__}] {m.content[:120]}")
