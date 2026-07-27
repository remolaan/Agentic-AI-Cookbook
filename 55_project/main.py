"""
LangGraph Functional API — @entrypoint and @task decorators.
Demonstrates writing workflows as decorated Python functions instead of StateGraph.
"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


@task
def research_topic(topic: str) -> str:
    """Step 1: Research the topic."""
    return llm.invoke(f"Research '{topic}' and provide key facts.").content


@task
def analyze_facts(facts: str) -> str:
    """Step 2: Analyze the findings."""
    return llm.invoke(f"Analyze these facts:\n{facts}").content


@task
def write_summary(analysis: str) -> str:
    """Step 3: Write a summary."""
    return llm.invoke(f"Summarize in 2 sentences:\n{analysis}").content


@entrypoint(checkpointer=MemorySaver())
def research_workflow(topic: str) -> dict:
    facts = research_topic(topic).result()
    analysis = analyze_facts(facts).result()
    summary = write_summary(analysis).result()
    return {"topic": topic, "summary": summary}


config = {"configurable": {"thread_id": "research-1"}}
result = research_workflow.invoke("Quantum computing basics", config)
print("=== Research Workflow ===")
print(f"Topic: {result['topic']}")
print(f"Summary: {result['summary'][:200]}...")
