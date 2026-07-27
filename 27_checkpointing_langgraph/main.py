from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


def chat(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("chat", chat)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "alice-1"}}

# Turn 1
result = graph.invoke(
    {"messages": [HumanMessage("Hi, I'm Alice.")]}, config=config
)
print("=== Turn 1 ===")
print(f"  AI: {result['messages'][-1].content}")

# Turn 2 — graph remembers thread
result = graph.invoke(
    {"messages": [HumanMessage("What's my name?")]}, config=config
)
print("=== Turn 2 ===")
print(f"  AI: {result['messages'][-1].content}")

# Inspect stored state
state = graph.get_state(config)
print(f"\n=== Stored State ===")
print(f"  Messages stored: {len(state.values['messages'])}")
for m in state.values["messages"]:
    print(f"  [{type(m).__name__}] {m.content[:40]}...")
