from dotenv import load_dotenv
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    MarkdownHeaderTextSplitter,
    Language,
)
from langchain_core.documents import Document

load_dotenv()

# --- Sample text ---
text = """LangChain is a framework for developing applications powered by large language models.

It simplifies the process of building LLM applications by providing modular components.

The framework has several key features:
- Prompt management: Create and manage prompts easily
- Chains: Combine multiple components into a pipeline
- Agents: Let LLMs decide which tools to use
- Memory: Maintain conversation context
- Retrieval: Connect LLMs to external data sources

LangChain supports many model providers including OpenAI, Anthropic, and open-source models.

It is written in Python and JavaScript/TypeScript."""

# ============================================================
# 1. RecursiveCharacterTextSplitter (recommended default)
# ============================================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, chunk_overlap=20,
    separators=["\n\n", "\n", ".", " "],
)
chunks = splitter.split_text(text)
print("=== RecursiveCharacterTextSplitter ===")
print(f"  {len(chunks)} chunks")
for i, c in enumerate(chunks):
    print(f"  Chunk {i+1}: {c[:50]}...")
print()

# ============================================================
# 2. CharacterTextSplitter (simple)
# ============================================================
chunks = CharacterTextSplitter(chunk_size=80, chunk_overlap=10, separator="\n").split_text(text)
print("=== CharacterTextSplitter ===")
print(f"  {len(chunks)} chunks")
print()

# ============================================================
# 3. PythonCodeTextSplitter
# ============================================================
python_code = """def hello(name):
    print(f"Hello, {name}!")

class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

result = Calculator().add(5, 3)
hello("World")
"""

splitter = PythonCodeTextSplitter(chunk_size=50, chunk_overlap=0)
chunks = splitter.split_text(python_code)
print("=== PythonCodeTextSplitter ===")
print(f"  {len(chunks)} chunks")
for i, c in enumerate(chunks):
    lines = c.strip().split("\n")
    print(f"  Chunk {i+1}: {lines[0][:50]}...")
print()

# ============================================================
# 4. MarkdownHeaderTextSplitter
# ============================================================
markdown = """# Chapter 1
## Section 1.1
This is content under section 1.1.

## Section 1.2
This is content under section 1.2 with more details.

# Chapter 2
## Section 2.1
Content for section 2.1.

### Subsection 2.1.1
Deep content here.
"""

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
    ("#", "Header 1"),
    ("##", "Header 2"),
])
chunks = splitter.split_text(markdown)
print("=== MarkdownHeaderTextSplitter ===")
print(f"  {len(chunks)} chunks")
for c in chunks:
    print(f"  [{c.metadata}] {c.page_content[:40]}...")
print()

# ============================================================
# 5. Language enum — for split_text with language awareness
# ============================================================
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=60,
    chunk_overlap=0,
)
chunks = splitter.split_text(python_code)
print("=== from_language (Python) ===")
print(f"  {len(chunks)} chunks")
for i, c in enumerate(chunks):
    print(f"  Chunk {i+1}: {c.strip()[:50]}...")
print()

# ============================================================
# 6. Splitting Documents (not just strings)
# ============================================================
docs = [Document(page_content=text, metadata={"source": "manual.md"})]
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
split_docs = splitter.split_documents(docs)
print("=== Split Documents ===")
print(f"  {len(docs)} doc → {len(split_docs)} chunks")
print(f"  Metadata preserved: {split_docs[0].metadata}")
