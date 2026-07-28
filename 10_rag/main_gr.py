"""
Gradio UI for Lesson 10 — RAG Pipeline.
Run:  python 10_rag/main_gr.py 8090
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
embeddings = FakeEmbeddings(size=384)

DEFAULT_KB = """LangChain is a framework for developing applications powered by large language models.
It simplifies the process of building LLM applications by providing modular components.
Chroma is a vector database for AI applications, designed to store and retrieve embeddings.
RAG stands for Retrieval-Augmented Generation, combining document search with LLM generation.
Agents use tools to interact with external systems and APIs."""


def run_rag(kb_text, question, k_chunks):
    docs = [Document(page_content=t.strip()) for t in kb_text.strip().split("\n") if t.strip()]
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": int(k_chunks)})

    template = """Answer based ONLY on the context below. If unsure, say "I don't know".

Context:
{context}

Question:
{question}

Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    retrieved = retriever.invoke(question)
    context_text = "\n\n".join(f"[{i+1}] {d.page_content}" for i, d in enumerate(retrieved))
    answer = rag_chain.invoke(question)

    return answer, context_text, f"Retrieved {len(retrieved)} chunks | KB: {len(chunks)} chunks"


with gr.Blocks(title="10 — RAG Pipeline") as app:
    gr.Markdown("# 10 — RAG (Retrieval-Augmented Generation)")
    gr.Markdown("Load knowledge → split → embed → store → retrieve → generate.")

    kb_input = gr.Textbox(label="Knowledge Base (one fact per line)", lines=8,
                           value=DEFAULT_KB)
    with gr.Row():
        question_input = gr.Textbox(label="Your Question", value="What is RAG?", scale=3)
        k_slider = gr.Slider(label="Retrieve top K", minimum=1, maximum=5, value=3, step=1, scale=1)

    run_btn = gr.Button("🚀 Ask RAG", variant="primary")

    answer_output = gr.Textbox(label="Answer", lines=4, interactive=False)
    context_output = gr.Textbox(label="Retrieved Context", lines=8, interactive=False)

    run_btn.click(fn=run_rag, inputs=[kb_input, question_input, k_slider],
                  outputs=[answer_output, context_output, gr.Textbox(visible=False)])

    gr.Markdown("---")
    gr.Markdown("**Note:** Uses FakeEmbeddings for demo. Results improve with real embeddings (OpenAI/HuggingFace).")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
