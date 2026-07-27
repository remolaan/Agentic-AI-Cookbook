from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


@tool
def search_knowledge_base(query: str) -> str:
    """Search product documentation."""
    kb = {"return": "Return policy: 30-day return window, item must be unused.",
          "shipping": "Free shipping on orders over $50. Standard delivery 5-7 business days.",
          "warranty": "1-year manufacturer warranty on all electronics."}
    for k, v in kb.items():
        if k in query.lower():
            return v
    return "I couldn't find that in the knowledge base."

@tool
def create_ticket(issue: str, priority: str = "normal") -> str:
    """Create a support ticket."""
    return f"Ticket created for: {issue} (priority: {priority}). Reference: TKT-{hash(issue) % 10000}"

@tool
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order. Requires human approval."""
    interrupt({"type": "refund_approval", "order_id": order_id, "reason": reason})
    return f"Refund processed for order {order_id}."


tools = [search_knowledge_base, create_ticket, process_refund]
llm_with_tools = llm.bind_tools(tools)

system_prompt = SystemMessage(
    "You are a customer support agent. Be helpful and concise. "
    "Use search_knowledge_base to answer questions. "
    "Use create_ticket to escalate issues. "
    "Use process_refund for refunds (it requires approval)."
)


def agent(state: MessagesState) -> dict:
    return {"messages": [llm_with_tools.invoke([system_prompt] + state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "support-1"}}

queries = ["What's your return policy?", "I need a refund for order ABC-123"]
for q in queries:
    try:
        result = graph.invoke({"messages": [HumanMessage(q)]}, config=config)
        print(f"User: {q}")
        print(f"Bot: {result['messages'][-1].content[:100]}...\n")
    except: pass

state = graph.get_state(config)
for task in state.tasks:
    for intr in task.interrupts:
        print(f"⏸️ Pending approval: {intr.value}")

if state.tasks:
    result = graph.invoke(Command(resume="approved"), config=config)
    print(f"\nAfter approval: {result['messages'][-1].content[:100]}...")
