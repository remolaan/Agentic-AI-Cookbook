"""
Gradio UI for Lesson 04 — Chat Models. Multi-turn chat with role-based messages + debug.
Run:  python 04_chat_models/main_gr.py 7860
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
last_prompt = []
last_response = None


def chat(message, history, system_prompt):
    global last_prompt, last_response
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})
    last_prompt = messages
    response = llm.invoke(messages)
    last_response = response
    return response.content


with gr.Blocks(title="04 — Chat Models") as app:
    gr.Markdown("# 04 — Chat Models")
    gr.Markdown("Multi-turn chat with configurable system prompt. Debug panels show each message exchange.")

    with gr.Accordion("⚙️ Settings", open=False):
        system_prompt = gr.Textbox(label="System Prompt", value="You are a helpful assistant.", lines=2)

    chatbot = gr.ChatInterface(
        fn=chat,
        additional_inputs=[system_prompt],
        title="💬 Chat",
        description="Multi-turn conversation with DeepSeek.",
    )

    with gr.Row():
        with gr.Accordion("📤 Raw Prompt (Message List)", open=False):
            raw_prompt_box = gr.Textbox(lines=10, interactive=False)
        with gr.Accordion("📥 Raw Response", open=False):
            raw_response_box = gr.Textbox(lines=10, interactive=False)
        with gr.Accordion("📊 Token Usage", open=False):
            token_box = gr.Textbox(lines=4, interactive=False)

    def refresh():
        p = ""
        if last_prompt:
            for m in last_prompt:
                p += f"[{m['role'].upper()}] {m['content']}\n---\n"
        r = ""
        if last_response:
            r = f"Content: {last_response.content}\n\nMetadata: {last_response.response_metadata}"
        t = ""
        if last_response and hasattr(last_response, "response_metadata"):
            tu = last_response.response_metadata.get("token_usage", {})
            if tu:
                t = f"Prompt: {tu.get('prompt_tokens','?')}\nCompletion: {tu.get('completion_tokens','?')}\nTotal: {tu.get('total_tokens','?')}"
        return p, r, t

    gr.Button("🔄 Refresh Debug Panels").click(fn=refresh, inputs=[], outputs=[raw_prompt_box, raw_response_box, token_box])
    chatbot.chatbot.change(fn=refresh, inputs=[], outputs=[raw_prompt_box, raw_response_box, token_box])

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0")
