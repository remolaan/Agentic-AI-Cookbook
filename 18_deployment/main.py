"""
RAG chatbot server — run with:
  uvicorn 18_deployment.main:app --reload

Then visit http://localhost:8000/docs for the interactive Swagger UI.
"""
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

# --- Build RAG chain at startup ---
loader = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
embeddings = FakeEmbeddings(size=384)
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

template = """Answer based on context. Say "I don't know" if unsure.

Context: {context}
Question: {question}
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- FastAPI app ---
app = FastAPI(title="LangChain RAG Bot")

class Query(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

@app.post("/ask", response_model=Answer)
def ask(query: Query):
    answer = rag_chain.invoke(query.question)
    return Answer(answer=answer)

@app.get("/health")
def health():
    return {"status": "ok"}
