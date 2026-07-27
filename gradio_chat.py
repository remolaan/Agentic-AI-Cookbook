"""
Quick Gradio chat UI for DeepSeek.
Run:  python gradio_chat.py
Then open http://localhost:7860
"""
import sys

__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


def chat(message, history):
    history_openai = []
    for h in history:
        history_openai.append({"role": "user", "content": h[0]})
        history_openai.append({"role": "assistant", "content": h[1]})
    history_openai.append({"role": "user", "content": message})
    response = llm.invoke(history_openai)
    return response.content


gr.ChatInterface(
    chat,
    title="LangChain + DeepSeek Chatbot",
    description="Ask anything — powered by DeepSeek via LangChain",
).launch()
