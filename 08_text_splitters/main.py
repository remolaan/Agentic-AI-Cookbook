from dotenv import load_dotenv
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)

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

# --- 1. RecursiveCharacterTextSplitter (recommended) ---
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", ".", " "],
)
chunks = splitter.split_text(text)
print("=== RecursiveCharacterTextSplitter ===")
for i, chunk in enumerate(chunks):
    print(f"  Chunk {i+1} ({len(chunk)} chars): {chunk[:60]}...")
print(f"  Total: {len(chunks)} chunks")
print()

# --- 2. CharacterTextSplitter (simpler) ---
splitter = CharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=10,
    separator="\n",
)
chunks = splitter.split_text(text)
print("=== CharacterTextSplitter ===")
for i, chunk in enumerate(chunks):
    print(f"  Chunk {i+1} ({len(chunk)} chars): {chunk[:50]}...")
print(f"  Total: {len(chunks)} chunks")
print()

# --- 3. Splitting Documents (not just strings) ---
from langchain_core.documents import Document

docs = [Document(page_content=text, metadata={"source": "manual.md"})]
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
split_docs = splitter.split_documents(docs)
print("=== Split Documents ===")
print(f"  {len(docs)} doc → {len(split_docs)} chunks")
print(f"  Metadata preserved: {split_docs[0].metadata}")
