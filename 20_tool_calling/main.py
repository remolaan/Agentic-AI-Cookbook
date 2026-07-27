from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# ============================================================
# 1. @tool decorator — simplest way
# ============================================================
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weathers = {"tokyo": "15°C", "paris": "22°C", "london": "12°C"}
    return weathers.get(city.lower(), f"No data for {city}")


print("=== 1. @tool decorator ===")
print(f"multiply name: {multiply.name}")
print(f"multiply args: {multiply.args}")
print(f"multiply(3, 4) = {multiply.invoke({'a': 3, 'b': 4})}")
print()

# ============================================================
# 2. StructuredTool — with Pydantic schema
# ============================================================
class SearchInput(BaseModel):
    query: str = Field(description="Search query string")
    max_results: int = Field(default=5, description="Max results to return")

def search_web(query: str, max_results: int = 5) -> list[str]:
    return [f"Result {i+1} for '{query}'" for i in range(max_results)]

search_tool = StructuredTool.from_function(
    func=search_web,
    name="web_search",
    description="Search the web for information",
    args_schema=SearchInput,
)

print("=== 2. StructuredTool ===")
print(f"search_tool name: {search_tool.name}")
print(f"search_tool(args={{'query': 'python'}}) = {search_tool.invoke({'query': 'python', 'max_results': 2})}")
print()

# ============================================================
# 3. bind_tools() — attach tools to model
# ============================================================
tools = [multiply, get_weather, search_tool]
llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke("What's 15 * 24 and weather in Paris?")
print("=== 3. bind_tools() ===")
print(f"Content: {response.content}")
print(f"Tool calls: {response.tool_calls}")
print()

# ============================================================
# 4. Tool calling loop
# ============================================================
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

tool_map = {t.name: t for t in tools}

messages = [HumanMessage("What is 8 * 12 and weather in Tokyo?")]
response = llm_with_tools.invoke(messages)
messages.append(response)

for tc in response.tool_calls:
    tool = tool_map[tc["name"]]
    result = tool.invoke(tc["args"])
    messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

final = llm_with_tools.invoke(messages)
print("=== 4. Tool calling loop ===")
print(final.content)

# ============================================================
# 5. Streaming with tool calls
# ============================================================
print("\n=== 5. Streaming with tool calls ===")
for chunk in llm_with_tools.stream([HumanMessage("Calculate 99 * 88")]):
    if hasattr(chunk, "tool_calls") and chunk.tool_calls:
        print(f"Tool call received: {chunk.tool_calls}")
    elif chunk.content:
        print(f"Content: {chunk.content}")
