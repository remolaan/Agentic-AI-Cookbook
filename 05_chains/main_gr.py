"""
Gradio UI for Lesson 05 — Chains. Test basic, sequential, and multi-output chains.
Run:  python 05_chains/main_gr.py 7860
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
last_prompt = []
last_response = None
intermediate = {}


def run_basic_chain(tone, subject):
    global last_prompt, last_response, intermediate
    chain = ChatPromptTemplate.from_template("Write a short {tone} poem about {subject}.") | llm | StrOutputParser()
    result = chain.invoke({"tone": tone, "subject": subject})
    last_prompt = [{"role": "user", "content": f"tone={tone}, subject={subject}"}]
    last_response = result
    intermediate = {"prompt": f"tone={tone}, subject={subject}", "output": result}
    return result


def run_sequential(product):
    global last_prompt, last_response, intermediate
    name_chain = ChatPromptTemplate.from_template("Suggest a name for a {product}. Only output the name.") | llm | StrOutputParser()
    tagline_chain = ChatPromptTemplate.from_template("Write a tagline for a product called {name}.") | llm | StrOutputParser()
    name = name_chain.invoke({"product": product})
    tagline = tagline_chain.invoke({"name": name})
    last_prompt = [{"role": "user", "content": f"Sequential chain: product={product}"}]
    last_response = tagline
    intermediate = {"step1_name": name, "step2_tagline": tagline}
    return f"Name: {name}\n\nTagline: {tagline}"


def run_multi_output(cuisine):
    global last_prompt, last_response, intermediate
    dish_chain = ChatPromptTemplate.from_template("Create a dish description for {cuisine} cuisine.") | llm | StrOutputParser()
    wine_chain = ChatPromptTemplate.from_template("Suggest a wine for this dish: {dish}") | llm | StrOutputParser()
    dish = dish_chain.invoke({"cuisine": cuisine})
    wine = wine_chain.invoke({"dish": dish})
    last_prompt = [{"role": "user", "content": f"Multi-output: cuisine={cuisine}"}]
    last_response = wine
    intermediate = {"dish": dish[:100], "wine": wine[:100]}
    return f"Dish:\n{dish[:200]}...\n\nWine:\n{wine[:200]}..."


def route_chain(chain_type, input1, input2):
    if chain_type == "Basic Chain":
        return run_basic_chain(input1 or "funny", input2 or "a penguin")
    elif chain_type == "Sequential Chain":
        return run_sequential(input1 or "cat-themed coffee shop")
    elif chain_type == "Multi-Output Chain":
        return run_multi_output(input1 or "Italian")


with gr.Blocks(title="05 — Chains") as app:
    gr.Markdown("# 05 — Chains")
    gr.Markdown("Test Basic, Sequential, and Multi-Output chain patterns.")

    with gr.Accordion("⚙️ Settings", open=False):
        chain_type = gr.Dropdown(label="Chain Type", choices=["Basic Chain", "Sequential Chain", "Multi-Output Chain"], value="Basic Chain")
        input1 = gr.Textbox(label="Input 1 (tone / product / cuisine)", value="funny")
        input2 = gr.Textbox(label="Input 2 (subject / leave blank)", value="a penguin learning to code")

    run_btn = gr.Button("🚀 Run Chain", variant="primary")
    output = gr.Textbox(label="Chain Output", lines=8)

    run_btn.click(fn=route_chain, inputs=[chain_type, input1, input2], outputs=output)

    with gr.Accordion("📤 Raw Prompt", open=False):
        raw_prompt_box = gr.Textbox(lines=6, interactive=False)
    with gr.Accordion("📥 Raw Response", open=False):
        raw_response_box = gr.Textbox(lines=6, interactive=False)
    with gr.Accordion("📊 Intermediate Steps", open=False):
        inter_box = gr.Textbox(lines=6, interactive=False)

    def refresh():
        p = "\n".join(f"[{m['role'].upper()}] {m['content']}" for m in last_prompt) if last_prompt else ""
        r = str(last_response) if last_response else ""
        i = "\n".join(f"{k}: {v}" for k, v in intermediate.items()) if intermediate else ""
        return p, r, i

    gr.Button("🔄 Refresh Debug Panels").click(fn=refresh, inputs=[], outputs=[raw_prompt_box, raw_response_box, inter_box])

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0")
