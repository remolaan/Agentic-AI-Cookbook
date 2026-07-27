from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


def chat(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("chat", chat)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)
graph = builder.compile()

input_msg = {"messages": [HumanMessage("Tell me a short joke.")]}

print("=== stream(mode='values') — full state each step ===")
for chunk in graph.stream(input_msg, stream_mode="values"):
    msgs = chunk.get("messages", [])
    if msgs:
        print(f"  State has {len(msgs)} messages, last: {msgs[-1].content[:40]}...")

print("\n=== stream(mode='updates') — node outputs ===")
for output in graph.stream(input_msg, stream_mode="updates"):
    for node_name, node_output in output.items():
        print(f"  Node '{node_name}' updated state")

print("\n=== stream(mode='messages') — token by token ===")
for msg_meta, _ in graph.stream(input_msg, stream_mode="messages"):
    if hasattr(msg_meta, "content") and msg_meta.content:
        print(msg_meta.content, end="", flush=True)
print()
