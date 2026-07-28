"""
Gradio UI for Lesson 02 — Prompt Templates.
Chat interface that wraps your messages with a template behind the scenes.
Run:  python 02_prompt_templates/main_gr.py 8090
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


def chat(message, history, system_prompt, human_template, few_shot_on, few_shot_examples):
    global last_prompt, last_response

    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    if few_shot_on:
        for ex in few_shot_examples:
            if isinstance(ex, dict):
                messages.append({"role": "user", "content": ex["Input"]})
                messages.append({"role": "assistant", "content": ex["Output"]})
            else:
                messages.append({"role": "user", "content": ex[0]})
                messages.append({"role": "assistant", "content": ex[1]})
    for h in history:
        if isinstance(h, dict):
            messages.append({"role": h["role"], "content": h["content"]})
        else:
            user_msg = human_template.replace("{input}", h[0])
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": h[1]})

    user_msg = human_template.replace("{input}", message)
    messages.append({"role": "user", "content": user_msg})

    last_prompt = messages
    response = llm.invoke(messages)
    last_response = response
    return response.content


with gr.Blocks(title="02 — Prompt Templates") as app:
    gr.Markdown("# 02 — Prompt Templates")
    gr.Markdown("Type a message below. The template wraps your input before sending to the LLM.")

    with gr.Accordion("⚙️ Template Settings", open=False):
        system = gr.Textbox(label="System Prompt", value="You are a helpful assistant.", lines=2)
        human_template = gr.Textbox(label="Human Template (use {input})", value="Answer this: {input}", lines=1)
        few_shot_on = gr.Checkbox(label="Enable few-shot examples", value=False)
        few_shot_examples = gr.Dataframe(
            headers=["Input", "Output"],
            value=[["What is AI?", "AI is artificial intelligence."], ["What is Python?", "Python is a programming language."]],
            label="Few-Shot Examples",
            col_count=(2, "int"),
        )

    chatbot = gr.ChatInterface(
        fn=chat,
        additional_inputs=[system, human_template, few_shot_on, few_shot_examples],
        title="💬 Chat",
        description="Your message gets wrapped in the template. Check debug panels to see the full prompt.",
    )

    with gr.Row():
        with gr.Accordion("📤 Raw Prompt Sent (formatted)", open=False):
            raw_prompt_box = gr.Textbox(lines=10, interactive=False)
        with gr.Accordion("📥 Raw Response", open=False):
            raw_response_box = gr.Textbox(lines=10, interactive=False)
        with gr.Accordion("📊 Token Usage", open=False):
            token_box = gr.Textbox(lines=4, interactive=False)

    def refresh():
        p = ""
        if last_prompt:
            for m in last_prompt:
                p += f"[{m['role'].upper()}] {str(m['content'])[:200]}\n---\n"
        r = ""
        if last_response:
            r = f"Content: {last_response.content}\n\nMetadata: {last_response.response_metadata}"
        t = ""
        if last_response and hasattr(last_response, "response_metadata"):
            tu = last_response.response_metadata.get("token_usage", {})
            if tu:
                t = f"Prompt tokens: {tu.get('prompt_tokens','?')}\nCompletion: {tu.get('completion_tokens','?')}\nTotal: {tu.get('total_tokens','?')}"
        return p, r, t

    gr.Button("🔄 Refresh Debug Panels", variant="secondary").click(
        fn=refresh, inputs=[], outputs=[raw_prompt_box, raw_response_box, token_box]
    )
    chatbot.chatbot.change(fn=refresh, inputs=[], outputs=[raw_prompt_box, raw_response_box, token_box])

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
