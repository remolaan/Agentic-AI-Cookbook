from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic.agents import Tool
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- Custom tools ---
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

def get_weather(city: str) -> str:
    """Get the current weather for a city (simulated)."""
    weathers = {"tokyo": "15°C, cloudy", "paris": "22°C, sunny", "london": "12°C, rainy"}
    return weathers.get(city.lower(), f"No data for {city}")

tools = [
    Tool(name="Multiply", func=multiply, description="Multiply two numbers. Input: two numbers separated by comma."),
    Tool(name="Weather", func=get_weather, description="Get weather for a city. Input: city name."),
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
]

# --- ReAct agent ---
prompt = PromptTemplate.from_template(
    "Answer the following question. You have access to these tools:\n\n"
    "{tools}\n\n"
    "Use this format:\n"
    "Question: the input question\n"
    "Thought: you should always think about what to do\n"
    "Action: the tool name to use\n"
    "Action Input: the input to the tool\n"
    "Observation: the tool's result\n"
    "... (repeat Thought/Action/Action Input/Observation as needed)\n"
    "Thought: I now know the final answer\n"
    "Final Answer: the final answer\n\n"
    "Question: {input}\n\n"
    "Available tools: {tool_names}\n"
    "{agent_scratchpad}"
)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

response = agent_executor.invoke({"input": "What is 15 multiplied by 24? Also, what's the weather in Paris?"})
print("\n=== Final Answer ===")
print(response["output"])
