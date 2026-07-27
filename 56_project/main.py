"""
Production-Grade Advanced RAG — 6 patterns combined.
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field
from typing import TypedDict

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- Vector store ---
docs_data = [
    Document(page_content="Python is a high-level programming language.", metadata={"source": "docs"}),
    Document(page_content="Chroma is a vector database for storing embeddings.", metadata={"source": "docs"}),
    Document(page_content="RAG = Retrieve + Augment + Generate.", metadata={"source": "docs"}),
    Document(page_content="Agents use tools to interact with external systems.", metadata={"source": "docs"}),
]
vectorstore = Chroma.from_documents(docs_data, FakeEmbeddings(size=384))
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ============================================================
# 1. Query Router
# ============================================================
class RAGState(TypedDict):
    question: str
    route: str
    context: str
    answer: str
    passed: bool
    attempts: int


def route_question(state: RAGState) -> dict:
    response = llm.invoke(f"Classify: 'facts' (factual) or 'chat' (general)?\n{state['question']}")
    return {"route": "facts" if "facts" in response.content.lower() else "chat"}


# ============================================================
# 2. Factual RAG — retrieve + generate
# ============================================================
def retrieve(state: RAGState) -> dict:
    docs = retriever.invoke(state["question"])
    return {"context": "\n".join([d.page_content for d in docs])}


def generate(state: RAGState) -> dict:
    chain = ChatPromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}\nAnswer:") | llm | StrOutputParser()
    return {"answer": chain.invoke({"context": state["context"], "question": state["question"]})}


# ============================================================
# 3. Self-Verification
# ============================================================
class Score(BaseModel):
    score: float = Field(description="Correctness 0-1")
    passed: bool = Field(description="Pass or fail")


def verify(state: RAGState) -> dict:
    verifier = llm.with_structured_output(Score, method="function_calling")
    result = verifier.invoke(f"Question: {state['question']}\nAnswer: {state['answer']}\nScore correctness.")
    return {"passed": result.passed, "attempts": state["attempts"] + 1}


def route_after_verify(state: RAGState) -> str:
    if state["passed"] or state["attempts"] >= 3:
        return "end"
    return "retrieve"


# ============================================================
# 4. Conversational — chat with memory
# ============================================================
def chat_response(state: RAGState) -> dict:
    return {"answer": llm.invoke(f"Answer conversationally: {state['question']}").content}


# ============================================================
# Build graph
# ============================================================
builder = StateGraph(RAGState)
builder.add_node("route", route_question)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("verify", verify)
builder.add_node("chat", chat_response)
builder.add_edge(START, "route")
builder.add_conditional_edges("route", lambda s: s["route"], {"facts": "retrieve", "chat": "chat"})
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "verify")
builder.add_conditional_edges("verify", route_after_verify, {"retrieve": "retrieve", "end": "chat"})
builder.add_edge("chat", END)

graph = builder.compile(checkpointer=MemorySaver())

# ============================================================
# Run
# ============================================================
for q in ["What is Chroma?", "Tell me a fun fact"]:
    result = graph.invoke({"question": q, "route": "", "context": "", "answer": "", "passed": False, "attempts": 0},
                          {"configurable": {"thread_id": q[:8]}})
    print(f"Q: {q}")
    print(f"A: {result['answer'][:120]}...")
    print(f"Route: {result['route']}, Attempts: {result['attempts']}\n")

# ============================================================
# 5. Agentic RAG
# ============================================================
@tool
def search_knowledge(query: str) -> str:
    """Search documentation."""
    docs = vectorstore.similarity_search(query)
    return "\n".join([d.page_content for d in docs])

agent = create_react_agent(llm.bind_tools([search_knowledge]), [search_knowledge])
print("=== Agentic RAG ===")
result = agent.invoke({"messages": [HumanMessage("What is Python and what is RAG?")]})
for m in result["messages"]:
    if m.content:
        print(f"  [{type(m).__name__}] {m.content[:120]}")
