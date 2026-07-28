"""
Gradio UI for Lesson 09 — Vector Stores.
Run:  python 09_vector_stores/main_gr.py 8090
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import gradio as gr
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

embeddings = FakeEmbeddings(size=384)

DEFAULT_DOCS = [
    "LangChain is a framework for building LLM apps.",
    "Chroma is a vector database for AI applications.",
    "FAISS enables fast similarity search on dense vectors.",
    "Python is a versatile programming language.",
    "Embeddings convert text into numerical vectors.",
    "RAG combines retrieval with generation for better answers.",
    "Agents use tools to interact with external systems.",
]

vectorstore = None


def rebuild_index(doc_strings, query):
    global vectorstore
    docs = [Document(page_content=t.strip()) for t in doc_strings.split("\n") if t.strip()] or [
        Document(page_content=t) for t in DEFAULT_DOCS
    ]
    vectorstore = Chroma.from_documents(docs, embeddings)
    idx_count = vectorstore._collection.count()

    if not query.strip():
        return f"Indexed {idx_count} documents", "", ""

    results = vectorstore.similarity_search_with_score(query, k=3)
    out = ""
    for doc, score in results:
        out += f"[score: {score:.2f}] {doc.page_content}\n\n"
    return f"Indexed {idx_count} documents", out.strip(), f"Query: {query}"


with gr.Blocks(title="09 — Vector Stores") as app:
    gr.Markdown("# 09 — Vector Stores")
    gr.Markdown("Build a vector index from documents and search by semantic similarity.")

    docs_input = gr.Textbox(label="Documents (one per line)", lines=6,
                             value="\n".join(DEFAULT_DOCS))
    query_input = gr.Textbox(label="Search Query", value="What converts text to numbers?", lines=1)
    run_btn = gr.Button("🚀 Index & Search", variant="primary")

    with gr.Row():
        stats = gr.Textbox(label="Index Status", lines=2, interactive=False)
        results = gr.Textbox(label="Search Results (with scores)", lines=8, interactive=False)

    run_btn.click(fn=rebuild_index, inputs=[docs_input, query_input], outputs=[stats, results, gr.Textbox(visible=False)])

    gr.Markdown("---")
    gr.Markdown("**Note:** Uses FakeEmbeddings (random vectors). Results show similarity scores — lower = more similar.")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
