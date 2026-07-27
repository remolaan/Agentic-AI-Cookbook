from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}: {subject}"


tools = [send_email]
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com").bind_tools(tools)


def agent(state: MessagesState) -> dict:
    response = llm.invoke(state["messages"])
    if response.tool_calls:
        for tc in response.tool_calls:
            interrupt({"question": f"Approve {tc['name']}({tc['args']})?", "tool_call": tc})
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "approval-1"}}

# First invoke — will pause at interrupt
try:
    graph.invoke(
        {"messages": [HumanMessage("Send email to bob@test.com with subject Hello and body Hi")]},
        config=config,
    )
except Exception:
    pass

state = graph.get_state(config)
print("=== Interrupted ===")
for task in state.tasks:
    print(f"  Interrupt: {task.interrupts[0].value}")

# Resume with approval
result = graph.invoke(Command(resume="approved"), config=config)
print("\n=== Final ===")
for m in result["messages"]:
    role = type(m).__name__
    if m.content:
        print(f"  [{role}] {m.content[:100]}")
