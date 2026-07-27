"""
Multi-agent swarm API server.
Run:  uvicorn 50_agent_api_server_project.main:app --reload
Then POST to http://localhost:8000/ask
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
app = FastAPI(title="Agent Swarm API")

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


@tool
def search_knowledge(query: str) -> str:
    return f"Knowledge result for: {query}"

@tool
def run_code(code: str) -> str:
    return f"Code executed: {code[:50]}..."

@tool
def generate_report(topic: str) -> str:
    return f"Report generated on: {topic}"


research_agent = create_react_agent(
    llm.bind_tools([search_knowledge, generate_report]),
    [search_knowledge, generate_report],
    prompt="You are a research specialist. Find and summarize information.",
    name="researcher",
    checkpointer=MemorySaver(),
)

code_agent = create_react_agent(
    llm.bind_tools([run_code]),
    [run_code],
    prompt="You are a coding specialist. Write and execute code.",
    name="coder",
    checkpointer=MemorySaver(),
)


class Query(BaseModel):
    question: str
    agent: str = "auto"


class Answer(BaseModel):
    answer: str
    agent_used: str


def route_query(question: str) -> str:
    resp = llm.invoke(f"Should this query go to the 'researcher' or 'coder' agent? Query: {question}")
    content = resp.content.lower()
    return "coder" if "coder" in content else "researcher"


@app.post("/ask", response_model=Answer)
def ask(query: Query):
    agent_name = query.agent if query.agent != "auto" else route_query(query.question)
    agent = research_agent if agent_name == "researcher" else code_agent
    result = agent.invoke({"messages": [HumanMessage(query.question)]})
    return Answer(answer=result["messages"][-1].content, agent_used=agent_name)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
