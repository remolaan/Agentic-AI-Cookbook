from dotenv import load_dotenv
from langchain_community.document_loaders import (
    TextLoader, CSVLoader, WebBaseLoader, WikipediaLoader,
    JSONLoader, DirectoryLoader,
)
from langchain_core.documents import Document

load_dotenv()

# ============================================================
# 1. TextLoader
# ============================================================
with open("/tmp/sample.txt", "w") as f:
    f.write("LangChain is a framework for building LLM apps.\nIt supports many integrations.")

loader = TextLoader("/tmp/sample.txt")
docs = loader.load()
print("=== TextLoader ===")
print(f"  {docs[0].page_content[:60]}...")
print()

# ============================================================
# 2. CSVLoader
# ============================================================
with open("/tmp/sample.csv", "w") as f:
    f.write("name,age,city\nAlice,30,New York\nBob,25,London\n")

loader = CSVLoader("/tmp/sample.csv")
docs = loader.load()
print("=== CSVLoader ===")
for d in docs:
    print(f"  → {d.page_content}")
print()

# ============================================================
# 3. JSONLoader
# ============================================================
with open("/tmp/sample.json", "w") as f:
    f.write('{"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}')

loader = JSONLoader(file_path="/tmp/sample.json", jq_schema=".users[]", text_content=False)
docs = loader.load()
print("=== JSONLoader ===")
for d in docs:
    print(f"  → {d.page_content}")
print()

# ============================================================
# 4. DirectoryLoader — load all files in a dir
# ============================================================
import os
os.makedirs("/tmp/mydocs", exist_ok=True)
with open("/tmp/mydocs/readme.md", "w") as f:
    f.write("# My Doc\n\nThis is a markdown document.")
with open("/tmp/mydocs/notes.txt", "w") as f:
    f.write("Just some plain text notes.")

loader = DirectoryLoader("/tmp/mydocs", glob="**/*.md", loader_cls=TextLoader)
docs = loader.load()
print("=== DirectoryLoader (.md only) ===")
for d in docs:
    print(f"  → [{d.metadata.get('source', '?')}] {d.page_content[:40]}...")
print()

# ============================================================
# 5. WebBaseLoader
# ============================================================
loader = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain")
docs = loader.load()
print("=== WebBaseLoader ===")
print(f"  Title: {docs[0].metadata.get('title', 'N/A')}")
print(f"  Length: {len(docs[0].page_content)} chars")
print()

# ============================================================
# 6. WikipediaLoader
# ============================================================
loader = WikipediaLoader(query="Python programming language", load_max_docs=1)
try:
    docs = loader.load()
    print("=== WikipediaLoader ===")
    if docs:
        print(f"  Title: {docs[0].metadata.get('title', 'N/A')}")
except:
    print("=== WikipediaLoader ===")
    print("  (Wikipedia API unavailable)")
print()
