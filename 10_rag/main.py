import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

# --- Load ---
loader = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain")
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")

# --- Split ---
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunks")

# --- Embed & Store ---
embeddings = FakeEmbeddings(size=384)
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- Prompt (Augment) ---
template = """Answer the question based ONLY on the following context.
If the context doesn't contain the answer, say "I don't know".

Context:
{context}

Question:
{question}

Answer:"""
prompt = ChatPromptTemplate.from_template(template)

# --- LLM (Generate) ---
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- Chain ---
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- Ask ---
question = "What is LangChain used for?"
print(f"\nQuestion: {question}")
answer = chain.invoke(question)
print(f"Answer: {answer}")

question = "Who created LangChain?"
print(f"\nQuestion: {question}")
answer = chain.invoke(question)
print(f"Answer: {answer}")

# Cleanup
import shutil
shutil.rmtree("./chroma_db", ignore_errors=True)
