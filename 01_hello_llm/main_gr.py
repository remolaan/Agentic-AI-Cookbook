"""
Interactive Gradio UI for Lesson 01 — Hello LLM.
Run:  python 01_hello_llm/main_gr.py
Then open http://localhost:7860

Features:
  - Set system prompt before chatting
  - Chat with DeepSeek
  - Inspect exact raw prompt sent to the LLM
  - Inspect exact raw response received
  - See token usage (when available)
"""
import sys

__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

last_prompt = []
last_response = None


def get_raw_prompt():
    if not last_prompt:
        return "No prompt sent yet."
    lines = []
    for m in last_prompt:
        role = m["role"].upper()
        lines.append(f"[{role}]")
        lines.append(m["content"])
        lines.append("")
    return "\n".join(lines)


def get_raw_response():
    if last_response is None:
        return "No response received yet."
    lines = []
    lines.append(f"Content: {last_response.content}")
    lines.append("")
    lines.append("Response Metadata:")
    if hasattr(last_response, "response_metadata"):
        for k, v in last_response.response_metadata.items():
            lines.append(f"  {k}: {v}")
    else:
        lines.append("  (none)")
    return "\n".join(lines)


def get_token_usage():
    if last_response is None:
        return "No data yet."
    if hasattr(last_response, "response_metadata"):
        meta = last_response.response_metadata
        token_usage = meta.get("token_usage") or meta.get("usage", {})
        if isinstance(token_usage, dict):
            prompt_tk = token_usage.get("prompt_tokens", token_usage.get("input_tokens", "?"))
            completion_tk = token_usage.get("completion_tokens", token_usage.get("output_tokens", "?"))
            total_tk = token_usage.get("total_tokens", "?")
            lines = [
                f"Prompt tokens:      {prompt_tk}",
                f"Completion tokens:  {completion_tk}",
                f"Total tokens:       {total_tk}",
            ]
            return "\n".join(lines)
        return str(token_usage)
    return "Token usage not available from this provider."


def refresh_debug():
    return get_raw_prompt(), get_raw_response(), get_token_usage()


def respond(message, history, system_prompt):
    global last_prompt, last_response

    history_openai = []
    if system_prompt.strip():
        history_openai.append({"role": "system", "content": system_prompt.strip()})
    for h in history:
        history_openai.append({"role": "user", "content": h[0]})
        history_openai.append({"role": "assistant", "content": h[1]})
    history_openai.append({"role": "user", "content": message})

    last_prompt = history_openai

    response = llm.invoke(history_openai)
    last_response = response

    return response.content


with gr.Blocks(title="LangChain — Hello LLM") as app:
    gr.Markdown("# LangChain — 01 Hello LLM")
    gr.Markdown(
        "Chat with DeepSeek via LangChain. "
        "The debug panels auto-populate after each message."
    )

    with gr.Accordion("⚙️ Prompt Settings", open=False):
        system_prompt = gr.Textbox(
            label="System Prompt",
            value="You are a helpful assistant.",
            lines=2,
            placeholder="Set the system behavior here...",
        )

    chatbot = gr.ChatInterface(
        fn=respond,
        additional_inputs=[system_prompt],
        title="💬 Chat",
        description="Type a message and see the AI respond.",
    )

    gr.Markdown("---")
    gr.Markdown("### 🔍 Debug Panels (click to expand)")

    with gr.Accordion("📤 Raw Prompt Sent", open=False):
        raw_prompt_box = gr.Textbox(
            label="Exact messages sent to the LLM",
            lines=8,
            interactive=False,
        )

    with gr.Accordion("📥 Raw Response Received", open=False):
        raw_response_box = gr.Textbox(
            label="Full response object",
            lines=8,
            interactive=False,
        )

    with gr.Accordion("📊 Token Usage", open=False):
        token_box = gr.Textbox(
            label="Token counts",
            lines=4,
            interactive=False,
        )

    refresh_btn = gr.Button("🔄 Refresh Debug Panels", variant="secondary")

    refresh_btn.click(
        fn=refresh_debug,
        inputs=[],
        outputs=[raw_prompt_box, raw_response_box, token_box],
    )

    chatbot.chatbot.change(
        fn=refresh_debug,
        inputs=[],
        outputs=[raw_prompt_box, raw_response_box, token_box],
    )

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0", theme="ocean")
