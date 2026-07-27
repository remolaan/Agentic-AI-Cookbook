import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from dotenv import load_dotenv
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

# Using FakeEmbeddings for demo (no downloads, no API key).
# Swap to real embeddings (OpenAI, HuggingFace, etc.) in production.
embeddings = FakeEmbeddings(size=384)

documents = [
    Document(page_content="LangChain is a framework for building LLM apps."),
    Document(page_content="Chroma is a vector database for AI applications."),
    Document(page_content="FAISS enables fast similarity search on dense vectors."),
    Document(page_content="Python is a versatile programming language."),
    Document(page_content="Embeddings convert text into numerical vectors."),
]

# --- Build vector store ---
vectorstore = Chroma.from_documents(documents, embeddings)
print("=== Chroma Vector Store ===")
print(f"Indexed {vectorstore._collection.count()} documents")
print()

# --- Similarity search ---
query = "What converts text to numbers?"
results = vectorstore.similarity_search(query, k=2)
print(f"Query: '{query}'")
for doc in results:
    print(f"  → {doc.page_content}")
print()

# --- Similarity search with score ---
results = vectorstore.similarity_search_with_score("Python coding", k=2)
print("With scores (lower = more similar):")
for doc, score in results:
    print(f"  [{score:.3f}] {doc.page_content}")
print()

# --- FAISS (faster for larger datasets) ---
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(documents, embeddings)
results = vectorstore.similarity_search("vector database", k=1)
print("=== FAISS ===")
print(f"  → {results[0].page_content}")
print()

# Cleanup Chroma persistence directory
import shutil
import os
chroma_dir = "./chroma_db"
if os.path.exists(chroma_dir):
    shutil.rmtree(chroma_dir, ignore_errors=True)
