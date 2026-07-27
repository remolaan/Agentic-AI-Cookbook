from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# ============================================================
# Define tools with @tool decorator
# ============================================================
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weathers = {"tokyo": "15°C, cloudy", "paris": "22°C, sunny", "london": "12°C, rainy"}
    return weathers.get(city.lower(), f"No data for {city}")

tools = [multiply, get_weather]

# ============================================================
# Modern agent using LangGraph
# ============================================================
print("=== LangGraph Agent ===")
agent = create_react_agent(llm, tools)

response = agent.invoke({"messages": [HumanMessage("What is 15 multiplied by 24? Also, what's the weather in Paris?")]})

for m in response["messages"]:
    role = type(m).__name__
    if m.content:
        print(f"  [{role}] {m.content[:150]}")
    elif hasattr(m, "tool_calls") and m.tool_calls:
        for tc in m.tool_calls:
            print(f"  [{role}] 🛠️ Calling {tc['name']}({tc['args']})")
print()
