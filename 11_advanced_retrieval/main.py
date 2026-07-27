import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_classic.retrievers import MultiQueryRetriever, SelfQueryRetriever
from langchain_classic.chains.query_constructor.base import AttributeInfo

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
embeddings = FakeEmbeddings(size=384)

# --- Sample documents with metadata ---
docs = [
    Document(page_content="Python was created by Guido van Rossum in 1991.", metadata={"year": 1991, "language": "Python"}),
    Document(page_content="JavaScript was created by Brendan Eich in 1995.", metadata={"year": 1995, "language": "JavaScript"}),
    Document(page_content="TypeScript adds static types to JavaScript.", metadata={"year": 2012, "language": "TypeScript"}),
    Document(page_content="Rust focuses on safety and performance.", metadata={"year": 2010, "language": "Rust"}),
    Document(page_content="Python is great for data science and AI.", metadata={"year": 1991, "language": "Python"}),
]
vectorstore = Chroma.from_documents(docs, embeddings)

# --- 1. MultiQueryRetriever ---
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm,
)
results = retriever.invoke("Tell me about Python")
print("=== MultiQueryRetriever ===")
for doc in results:
    print(f"  → {doc.page_content}")
print()

# --- 2. SelfQueryRetriever ---
metadata_field_info = [
    AttributeInfo(name="year", description="Year the language was created", type="int"),
    AttributeInfo(name="language", description="Programming language name", type="string"),
]
retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Programming languages",
    metadata_field_info=metadata_field_info,
)
results = retriever.invoke("Which languages were created before 2000?")
print("=== SelfQueryRetriever ===")
for doc in results:
    print(f"  → {doc.page_content}")
