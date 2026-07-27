from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


def chat_node(state: MessagesState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()

result = graph.invoke({"messages": [HumanMessage("Hi, I'm Alice.")]})
print("=== Turn 1 ===")
for m in result["messages"]:
    print(f"  [{type(m).__name__}] {m.content}")

result = graph.invoke({"messages": [HumanMessage("What's my name?")]})
print("\n=== Turn 2 (no history — stateless) ===")
for m in result["messages"]:
    print(f"  [{type(m).__name__}] {m.content}")
