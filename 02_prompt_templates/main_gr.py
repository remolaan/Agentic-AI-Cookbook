"""
Gradio UI for Lesson 02 — Prompt Templates.
Run:  python 02_prompt_templates/main_gr.py 7860
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


def format_prompt(system, human, few_shot_on, few_shot_examples, user_var):
    parts = []
    if system.strip():
        parts.append({"role": "system", "content": system.strip()})
    if few_shot_on:
        for ex in few_shot_examples:
            parts.append({"role": "user", "content": ex[0]})
            parts.append({"role": "assistant", "content": ex[1]})
    full = human.replace("{input}", user_var)
    parts.append({"role": "user", "content": full})
    return parts


def run(system, human, few_shot_on, few_shot_examples, user_var):
    global last_prompt, last_response
    messages = format_prompt(system, human, few_shot_on, few_shot_examples, user_var)
    last_prompt = messages
    response = llm.invoke(messages)
    last_response = response
    return response.content


with gr.Blocks(title="02 — Prompt Templates") as app:
    gr.Markdown("# 02 — Prompt Templates")
    gr.Markdown("Build a custom prompt with system + human + optional few-shot examples.")

    with gr.Accordion("⚙️ Prompt Settings", open=False):
        system = gr.Textbox(label="System Prompt", value="You are a helpful assistant.", lines=2)
        human = gr.Textbox(label="Human Template", value="Answer this: {input}", lines=1)
        few_shot_on = gr.Checkbox(label="Enable few-shot examples", value=False)
        few_shot_examples = gr.Dataframe(headers=["Input", "Output"], value=[["What is AI?", "AI is..."], ["What is Python?", "Python is..."]], label="Few-Shot Examples")
        user_var = gr.Textbox(label="Input variable", value="Explain machine learning in one sentence.")

    run_btn = gr.Button("🚀 Run Prompt", variant="primary")
    output = gr.Textbox(label="Response", lines=6)

    run_btn.click(fn=run, inputs=[system, human, few_shot_on, few_shot_examples, user_var], outputs=output)

    with gr.Accordion("📤 Raw Prompt Sent", open=False):
        raw_prompt_box = gr.Textbox(lines=8, interactive=False)
    with gr.Accordion("📥 Raw Response", open=False):
        raw_response_box = gr.Textbox(lines=8, interactive=False)
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

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0")
