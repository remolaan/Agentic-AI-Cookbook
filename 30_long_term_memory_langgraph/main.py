from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.store.memory import InMemoryStore
from langgraph.config import get_store

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
store = InMemoryStore()


def chat(state: MessagesState, config) -> dict:
    user_id = config["configurable"]["user_id"]
    my_store = get_store()

    known = ""
    if my_store:
        items = my_store.search(("users", user_id))
        for item in items:
            known += f"{item.key}: {item.value.get('value', '')}\n"

    prompt = "Say hello and ask how you can help."
    if known:
        prompt = f"You know this about the user: {known}. Greet them and ask how you can help."
    else:
        prompt = "Greet the user warmly and ask their name."

    response = llm.invoke(prompt)
    my_store.put(("users", user_id), config["configurable"]["thread_id"], {"value": prompt})
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("chat", chat)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile(store=store)

config = {"configurable": {"thread_id": "t1", "user_id": "alice"}}
result = graph.invoke({"messages": [HumanMessage("")]}, config=config)
print("=== Turn 1 ===")
print(f"  AI: {result['messages'][-1].content[:80]}")

config2 = {"configurable": {"thread_id": "t2", "user_id": "alice"}}
result = graph.invoke({"messages": [HumanMessage("")]}, config=config2)
print("\n=== Turn 2 (same user, new thread) ===")
print(f"  AI: {result['messages'][-1].content[:80]}")
