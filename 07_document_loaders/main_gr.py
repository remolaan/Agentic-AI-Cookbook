"""
Gradio UI for Lesson 07 — Document Loaders. Test text, CSV, JSON, web, and directory loaders.
Run:  python 07_document_loaders/main_gr.py 7860
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_community.document_loaders import TextLoader, CSVLoader, WebBaseLoader
import json, tempfile, os

load_dotenv()

last_docs = []


def load_docs(loader_type, text_content, csv_content, json_content, url, file_obj):
    global last_docs
    last_docs = []
    try:
        if loader_type == "Text":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write(text_content)
                f.flush()
            loader = TextLoader(f.name)
            last_docs = loader.load()
            os.unlink(f.name)

        elif loader_type == "CSV":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
                f.write(csv_content)
                f.flush()
            loader = CSVLoader(f.name)
            last_docs = loader.load()
            os.unlink(f.name)

        elif loader_type == "JSON":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                f.write(json_content)
                f.flush()
            from langchain_community.document_loaders import JSONLoader
            try:
                loader = JSONLoader(file_path=f.name, jq_schema=".[]", text_content=False)
                last_docs = loader.load()
            except:
                loader = JSONLoader(file_path=f.name, jq_schema=".", text_content=False)
                last_docs = loader.load()
            os.unlink(f.name)

        elif loader_type == "Web":
            loader = WebBaseLoader(url)
            last_docs = loader.load()

        result = ""
        for d in last_docs:
            result += f"--- Document (source: {d.metadata.get('source', '?')}) ---\n"
            result += f"Content: {d.page_content[:300]}\n\n"
        return result

    except Exception as e:
        return f"Error: {e}"


with gr.Blocks(title="07 — Document Loaders") as app:
    gr.Markdown("# 07 — Document Loaders")
    gr.Markdown("Load documents from text, CSV, JSON, or the web. See the raw Document objects.")

    with gr.Accordion("⚙️ Loader Settings", open=False):
        loader_type = gr.Dropdown(label="Loader Type", choices=["Text", "CSV", "JSON", "Web"], value="Text")

    text_content = gr.Textbox(label="Text Content", value="LangChain is a framework for building LLM apps.\nIt supports many integrations.", lines=4, visible=True)
    csv_content = gr.Textbox(label="CSV Content", value="name,age,city\nAlice,30,New York\nBob,25,London", lines=4, visible=False)
    json_content = gr.Textbox(label="JSON Content", value='[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]', lines=4, visible=False)
    url = gr.Textbox(label="URL", value="https://en.wikipedia.org/wiki/LangChain", lines=1, visible=False)

    def toggle_visibility(lt):
        return [
            gr.update(visible=lt == "Text"),
            gr.update(visible=lt == "CSV"),
            gr.update(visible=lt == "JSON"),
            gr.update(visible=lt == "Web"),
        ]

    loader_type.change(fn=toggle_visibility, inputs=loader_type, outputs=[text_content, csv_content, json_content, url])

    run_btn = gr.Button("🚀 Load Documents", variant="primary")
    output = gr.Textbox(label="Loaded Documents", lines=10)

    run_btn.click(fn=load_docs, inputs=[loader_type, text_content, csv_content, json_content, url, gr.State(None)], outputs=output)

    with gr.Accordion("📤 Raw Document Objects", open=False):
        raw_box = gr.Textbox(lines=8, interactive=False)

    def refresh():
        r = ""
        for d in last_docs:
            r += f"page_content: {d.page_content[:200]}\nmetadata: {d.metadata}\n---\n"
        return r

    gr.Button("🔄 Refresh").click(fn=refresh, inputs=[], outputs=raw_box)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0")
