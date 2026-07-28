"""
Gradio UI for Lesson 08 — Text Splitters.
Run:  python 08_text_splitters/main_gr.py 8090
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import gradio as gr
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    MarkdownHeaderTextSplitter,
    Language,
)
from langchain_core.documents import Document

SAMPLE_TEXT = """LangChain is a framework for developing applications powered by large language models.

It simplifies the process of building LLM applications by providing modular components.

The framework has several key features:
- Prompt management: Create and manage prompts easily
- Chains: Combine multiple components into a pipeline
- Agents: Let LLMs decide which tools to use
- Memory: Maintain conversation context
- Retrieval: Connect LLMs to external data sources

LangChain supports many model providers including OpenAI, Anthropic, and open-source models.

It is written in Python and JavaScript/TypeScript."""


def split_text(splitter_name, text, chunk_size, chunk_overlap):
    if not text.strip():
        text = SAMPLE_TEXT

    if splitter_name == "RecursiveCharacterTextSplitter":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "],
        )
    elif splitter_name == "CharacterTextSplitter":
        splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="\n"
        )
    elif splitter_name == "PythonCodeTextSplitter":
        splitter = PythonCodeTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        text = """def hello(name):
    print(f"Hello, {name}!")

class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

result = Calculator().add(5, 3)
hello("World")"""
    elif splitter_name == "MarkdownHeaderTextSplitter":
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ("#", "Header 1"), ("##", "Header 2"),
        ])
        text = """# Chapter 1
## Section 1.1
Content under section 1.1.

## Section 1.2
Content under section 1.2.

# Chapter 2
## Section 2.1
Content for section 2.1."""
    else:
        return "Unknown splitter", ""

    if splitter_name == "MarkdownHeaderTextSplitter":
        chunks = splitter.split_text(text)
        result = ""
        for i, c in enumerate(chunks):
            result += f"--- Chunk {i+1} (metadata: {c.metadata}) ---\n{c.page_content}\n\n"
        return result, f"{len(chunks)} chunks"
    else:
        chunks = splitter.split_text(text)
        result = ""
        for i, c in enumerate(chunks):
            result += f"--- Chunk {i+1} ({len(c)} chars) ---\n{c}\n\n"
        return result, f"{len(chunks)} chunks | total: {sum(len(c) for c in chunks)} chars"


with gr.Blocks(title="08 — Text Splitters") as app:
    gr.Markdown("# 08 — Text Splitters")
    gr.Markdown("Split text into chunks using different strategies.")

    with gr.Row():
        splitter_dd = gr.Dropdown(label="Splitter", choices=[
            "RecursiveCharacterTextSplitter", "CharacterTextSplitter",
            "PythonCodeTextSplitter", "MarkdownHeaderTextSplitter",
        ], value="RecursiveCharacterTextSplitter")
        chunk_size = gr.Slider(label="Chunk Size", minimum=20, maximum=500, value=100, step=10)
        chunk_overlap = gr.Slider(label="Overlap", minimum=0, maximum=100, value=20, step=5)

    with gr.Row():
        text_input = gr.Textbox(label="Input Text", value=SAMPLE_TEXT, lines=8, scale=3)
        run_btn = gr.Button("🚀 Split", variant="primary", scale=1)

    with gr.Row():
        output = gr.Textbox(label="Chunks", lines=12, interactive=False, scale=3)
        stats = gr.Textbox(label="Statistics", lines=3, interactive=False, scale=1)

    run_btn.click(fn=split_text, inputs=[splitter_dd, text_input, chunk_size, chunk_overlap], outputs=[output, stats])

    gr.Markdown("---")
    gr.Markdown("**Tip:** PythonCode and Markdown splitters auto-load sample content when no input is provided.")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
