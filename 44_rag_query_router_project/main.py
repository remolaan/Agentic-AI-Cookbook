from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# Build doc retriever
docs_data = [
    Document(page_content="Python is a high-level programming language.", metadata={"source": "docs"}),
    Document(page_content="Chroma is a vector database for AI applications.", metadata={"source": "docs"}),
]
vectorstore = Chroma.from_documents(docs_data, FakeEmbeddings(size=384))
doc_retriever = vectorstore.as_retriever()


class State(TypedDict):
    question: str
    source: str
    context: str
    answer: str


def router(state: State) -> dict:
    prompt = f"Question: {state['question']}\nIs this about: 'docs' (technical/langchain), 'wiki' (general knowledge), or 'web' (current events)? Reply with just the word."
    source = llm.invoke(prompt).content.strip().lower()
    source = "docs" if "docs" in source else ("wiki" if "wiki" in source else "web")
    return {"source": source}


def retrieve_docs(state: State) -> dict:
    results = doc_retriever.invoke(state["question"])
    return {"context": "\n".join([d.page_content for d in results])}


def retrieve_wiki(state: State) -> dict:
    results = llm.invoke(f"Summarize relevant Wikipedia knowledge for: {state['question']}")
    return {"context": results.content}


def retrieve_web(state: State) -> dict:
    results = llm.invoke(f"Simulate a web search for current info on: {state['question']}")
    return {"context": results.content}


def generate(state: State) -> dict:
    prompt = ChatPromptTemplate.from_template("Answer using this context:\n{context}\n\nQuestion: {question}")
    chain = prompt | llm | StrOutputParser()
    return {"answer": chain.invoke({"context": state["context"], "question": state["question"]})}


def route(state: State) -> str:
    return state["source"]


builder = StateGraph(State)
builder.add_node("router", router)
builder.add_node("docs", retrieve_docs)
builder.add_node("wiki", retrieve_wiki)
builder.add_node("web", retrieve_web)
builder.add_node("generate", generate)
builder.add_edge(START, "router")
builder.add_conditional_edges("router", route, {"docs": "docs", "wiki": "wiki", "web": "web"})
builder.add_edge("docs", "generate")
builder.add_edge("wiki", "generate")
builder.add_edge("web", "generate")
builder.add_edge("generate", END)

graph = builder.compile()

for q in ["What is Python?", "Tell me about LangChain"]:
    result = graph.invoke({"question": q, "source": "", "context": "", "answer": ""})
    print(f"Q: {q}")
    print(f"→ Source: {result['source']}")
    print(f"→ Answer: {result['answer'][:100]}...\n")
