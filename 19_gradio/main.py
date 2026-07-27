"""
Gradio UIs for LangChain — 3 apps in one file.
Run:  python 19_gradio/main.py
Then open http://localhost:7860
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
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# ============================================================
# App 1: Simple Chat
# ============================================================
def simple_chat(message, history):
    history_openai = []
    for h in history:
        history_openai.append({"role": "user", "content": h[0]})
        history_openai.append({"role": "assistant", "content": h[1]})
    history_openai.append({"role": "user", "content": message})
    return llm.invoke(history_openai).content

# ============================================================
# App 2: Streaming Chat (tokens arrive live)
# ============================================================
def stream_chat(message, history):
    history_openai = []
    for h in history:
        history_openai.append({"role": "user", "content": h[0]})
        history_openai.append({"role": "assistant", "content": h[1]})
    history_openai.append({"role": "user", "content": message})

    streaming_llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
    )
    for chunk in streaming_llm.stream(history_openai):
        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content

# ============================================================
# App 3: RAG Q&A over a Wikipedia page
# ============================================================
loader = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
embeddings = FakeEmbeddings(size=384)
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

template = """Answer based ONLY on this context. Say "I don't know" if unsure.

Context: {context}
Question: {question}
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def rag_chat(message, history):
    return rag_chain.invoke(message)

# ============================================================
# Build the multi-tab Gradio app
# ============================================================
with gr.Blocks(title="LangChain + Gradio") as app:
    gr.Markdown("# LangChain + Gradio 🚀")
    gr.Markdown("Three apps showing different Gradio + LangChain patterns.")

    with gr.Tab("💬 Simple Chat"):
        gr.ChatInterface(
            simple_chat,
            title="Chat with DeepSeek",
            description="Basic chatbot. Type anything!",
        )

    with gr.Tab("⚡ Streaming Chat"):
        gr.ChatInterface(
            stream_chat,
            title="Streaming Chat",
            description="Tokens appear as they're generated.",
            type="messages",
        )

    with gr.Tab("📚 RAG Q&A"):
        gr.ChatInterface(
            rag_chat,
            title="RAG over Wikipedia",
            description="Ask about LangChain. Uses FakeEmbeddings (demo mode).",
        )

if __name__ == "__main__":
    app.launch()
