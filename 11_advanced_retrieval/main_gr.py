"""
Gradio UI for Lesson 11 — Advanced Retrieval.
Run:  python 11_advanced_retrieval/main_gr.py 8090
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_classic.retrievers import MultiQueryRetriever, SelfQueryRetriever
from langchain_classic.chains.query_constructor.base import AttributeInfo

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
embeddings = FakeEmbeddings(size=384)

SAMPLE_DOCS = [
    Document(page_content="Python was created by Guido van Rossum in 1991.", metadata={"year": 1991, "language": "Python"}),
    Document(page_content="JavaScript was created by Brendan Eich in 1995.", metadata={"year": 1995, "language": "JavaScript"}),
    Document(page_content="TypeScript adds static types to JavaScript.", metadata={"year": 2012, "language": "TypeScript"}),
    Document(page_content="Rust focuses on safety and performance.", metadata={"year": 2010, "language": "Rust"}),
    Document(page_content="Python is great for data science and AI.", metadata={"year": 1991, "language": "Python"}),
]

vectorstore = Chroma.from_documents(SAMPLE_DOCS, embeddings)
base_retriever = vectorstore.as_retriever()


def run_multi_query(question):
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
    results = retriever.invoke(question)
    out = ""
    for i, d in enumerate(results):
        out += f"[{i+1}] {d.page_content} (meta: {d.metadata})\n"
    return out.strip()


def run_self_query(question):
    metadata_field_info = [
        AttributeInfo(name="year", description="Year created", type="int"),
        AttributeInfo(name="language", description="Language name", type="string"),
    ]
    retriever = SelfQueryRetriever.from_llm(
        llm=llm, vectorstore=vectorstore,
        document_contents="Programming languages",
        metadata_field_info=metadata_field_info,
    )
    results = retriever.invoke(question)
    out = ""
    for i, d in enumerate(results):
        out += f"[{i+1}] {d.page_content} (meta: {d.metadata})\n"
    return out.strip()


def run(question, retriever_type):
    if not question.strip():
        return "Enter a question.", ""
    if retriever_type == "MultiQueryRetriever":
        r = run_multi_query(question)
        return r, ""
    elif retriever_type == "SelfQueryRetriever":
        r = run_self_query(question)
        return "", r
    return "", ""


with gr.Blocks(title="11 — Advanced Retrieval") as app:
    gr.Markdown("# 11 — Advanced Retrieval")
    gr.Markdown("MultiQuery generates query variations. SelfQuery uses metadata filters from natural language.")

    with gr.Row():
        retriever_dd = gr.Dropdown(label="Retriever Type",
                                    choices=["MultiQueryRetriever", "SelfQueryRetriever"],
                                    value="MultiQueryRetriever")
        question_input = gr.Textbox(label="Question", value="Tell me about Python", scale=3)

    run_btn = gr.Button("🚀 Retrieve", variant="primary")

    with gr.Row():
        mq_output = gr.Textbox(label="MultiQuery Results", lines=8, interactive=False)
        sq_output = gr.Textbox(label="SelfQuery Results", lines=8, interactive=False)

    def run_and_route(question, rt):
        if rt == "MultiQueryRetriever":
            r = run_multi_query(question)
            return r, ""
        else:
            r = run_self_query(question)
            return "", r

    run_btn.click(fn=run_and_route, inputs=[question_input, retriever_dd],
                  outputs=[mq_output, sq_output])

    gr.Markdown("---")
    gr.Markdown("**Tip:** SelfQuery supports filters like 'languages created before 2000' or 'languages with static typing'.")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
