"""
Gradio UI for Lesson 06 — Memory. Test buffer, windowed, and summary memory.
Run:  python 06_memory/main_gr.py 7860
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
store = {}
last_history = []
last_response = None


def get_session(sid):
    if sid not in store:
        store[sid] = ChatMessageHistory()
    return store[sid]


def chat(message, history, memory_type):
    global last_history, last_response
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain, get_session,
        input_messages_key="input", history_messages_key="history",
    )

    response = chain_with_history.invoke(
        {"input": message},
        config={"configurable": {"session_id": memory_type}},
    )
    last_response = response
    last_history = store[memory_type].messages
    return response.content


with gr.Blocks(title="06 — Memory") as app:
    gr.Markdown("# 06 — Memory")
    gr.Markdown("Full history, windowed (last N), or summary memory.")

    with gr.Accordion("⚙️ Memory Settings", open=False):
        memory_type = gr.Dropdown(label="Memory Type", choices=["buffer", "windowed", "summary"], value="buffer")

    chatbot = gr.ChatInterface(fn=chat, additional_inputs=[memory_type], title="💬 Chat with Memory")

    with gr.Row():
        with gr.Accordion("📤 Stored History", open=False):
            history_box = gr.Textbox(lines=10, interactive=False)
        with gr.Accordion("📊 Token Usage", open=False):
            token_box = gr.Textbox(lines=4, interactive=False)

    def refresh():
        h = "\n".join(f"[{type(m).__name__}] {m.content[:80]}" for m in last_history) if last_history else ""
        if last_response and hasattr(last_response, "response_metadata"):
            tu = last_response.response_metadata.get("token_usage", {}) or last_response.response_metadata.get("usage", {})
            if tu:
                t = f"Prompt: {tu.get('prompt_tokens', '?')}\nCompletion: {tu.get('completion_tokens', '?')}\nTotal: {tu.get('total_tokens', '?')}"
            else:
                t = str(last_response.response_metadata)
        else:
            t = ""
        return h, t

    gr.Button("🔄 Refresh Debug Panels").click(fn=refresh, inputs=[], outputs=[history_box, token_box])
    chatbot.chatbot.change(fn=refresh, inputs=[], outputs=[history_box, token_box])

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0")
