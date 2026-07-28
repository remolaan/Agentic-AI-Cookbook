"""
Gradio UI for Lesson 12 — LangGraph Agents.
Run:  python 12_agents/main_gr.py 8090
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    data = {"tokyo": "15°C, cloudy", "paris": "22°C, sunny", "london": "12°C, rainy"}
    return data.get(city.lower(), f"No data for {city}")


@tool
def get_time(city: str) -> str:
    """Get current time in a city."""
    times = {"tokyo": "09:30", "paris": "02:30", "london": "01:30", "new york": "20:30"}
    return times.get(city.lower(), "Time data not available")


tools = [multiply, get_weather, get_time]
agent = create_react_agent(llm.bind_tools(tools), tools)

last_tool_calls = []
last_response = ""


def chat(message, history):
    global last_tool_calls, last_response
    result = agent.invoke({"messages": [HumanMessage(message)]})
    tool_calls = []
    for m in result["messages"]:
        if hasattr(m, "tool_calls") and m.tool_calls:
            for tc in m.tool_calls:
                tool_calls.append(f"🛠️ {tc['name']}({tc['args']})")
        if m.content and m == result["messages"][-1]:
            last_response = m.content
    last_tool_calls = tool_calls
    return result["messages"][-1].content


with gr.Blocks(title="12 — LangGraph Agents") as app:
    gr.Markdown("# 12 — LangGraph Agents")
    gr.Markdown("An agent with tools: **multiply**, **get_weather**, **get_time**. The LLM decides which to call.")

    chatbot = gr.ChatInterface(
        fn=chat,
        title="💬 Agent Chat",
        description="Ask the agent to calculate, check weather, or get time in a city.",
    )

    with gr.Row():
        with gr.Accordion("🛠️ Tool Calls (last request)", open=False):
            tool_box = gr.Textbox(lines=4, interactive=False)
        with gr.Accordion("🤖 Agent's Full Response", open=False):
            response_box = gr.Textbox(lines=6, interactive=False)
        with gr.Accordion("📊 Available Tools", open=False):
            gr.Textbox(
                value="• multiply(a, b) — multiply two numbers\n"
                      "• get_weather(city) — weather for a city\n"
                      "• get_time(city) — current time in a city",
                lines=4, interactive=False,
            )

    def refresh():
        return "\n".join(last_tool_calls) if last_tool_calls else "", last_response

    gr.Button("🔄 Refresh Tool Info").click(fn=refresh, inputs=[], outputs=[tool_box, response_box])
    chatbot.chatbot.change(fn=refresh, inputs=[], outputs=[tool_box, response_box])

    gr.Markdown("---")
    gr.Markdown("**Example queries:** `What is 15 * 24?`, `Weather in Paris?`, `What's the time in Tokyo?`, `Calculate 8*12 and weather in London`")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
