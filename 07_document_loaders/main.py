from dotenv import load_dotenv
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    WebBaseLoader,
    WikipediaLoader,
)

load_dotenv()

# --- 1. TextLoader (load a local text file) ---
with open("/tmp/sample.txt", "w") as f:
    f.write("LangChain is a framework for developing applications powered by language models.\n")
    f.write("It enables building context-aware reasoning applications.")

loader = TextLoader("/tmp/sample.txt")
docs = loader.load()
print("=== TextLoader ===")
print(f"Loaded {len(docs)} document(s)")
print(f"Content preview: {docs[0].page_content[:80]}...")
print(f"Metadata: {docs[0].metadata}")
print()

# --- 2. CSVLoader ---
with open("/tmp/sample.csv", "w") as f:
    f.write("name,age,city\n")
    f.write("Alice,30,New York\n")
    f.write("Bob,25,London\n")

loader = CSVLoader("/tmp/sample.csv")
docs = loader.load()
print("=== CSVLoader ===")
for doc in docs:
    print(f"  → {doc.page_content}")
print()

# --- 3. WebBaseLoader ---
loader = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain")
docs = loader.load()
print("=== WebBaseLoader ===")
print(f"Loaded {len(docs)} document(s)")
print(f"Title: {docs[0].metadata.get('title', 'N/A')}")
print(f"Content length: {len(docs[0].page_content)} chars")
print()

# --- 4. WikipediaLoader ---
loader = WikipediaLoader(query="Python programming language", load_max_docs=1)
docs = loader.load()
print("=== WikipediaLoader ===")
print(f"Title: {docs[0].metadata.get('title', 'N/A')}")
print(f"Content preview: {docs[0].page_content[:150]}...")
