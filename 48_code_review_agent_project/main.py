from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class ReviewReport(BaseModel):
    score: int = Field(description="Score 1-10")
    bugs: list[str] = Field(description="Bugs found")
    style_issues: list[str] = Field(description="Style issues")
    security_concerns: list[str] = Field(description="Security concerns")
    verdict: str = Field(description="PASS, FAIL, or NEEDS_WORK")


@tool
def check_style(code: str) -> str:
    """Check code style and formatting."""
    issues = []
    if len(code) < 50: issues.append("Code is too short for meaningful review")
    if "    " not in code and "\t" not in code: issues.append("No indentation found")
    return "\n".join(issues) if issues else "Style looks good."

@tool
def check_security(code: str) -> str:
    """Scan code for security vulnerabilities."""
    issues = []
    if "eval(" in code: issues.append("Use of eval() detected - security risk")
    if "password" in code.lower(): issues.append("Hardcoded password detected")
    return "\n".join(issues) if issues else "No security issues found."

@tool
def analyze_logic(code: str) -> str:
    """Analyze code logic for potential bugs."""
    issues = []
    if "TODO" in code: issues.append("Unresolved TODO found")
    if "pass" in code: issues.append("Empty pass statement found")
    if len(code.split("\n")) > 20: issues.append("Function is too long, consider refactoring")
    return "\n".join(issues) if issues else "Logic appears sound."


tools = [check_style, check_security, analyze_logic]
llm_with_tools = llm.bind_tools(tools)

structured_llm = llm.with_structured_output(ReviewReport, method="function_calling")


def agent(state: MessagesState) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def generate_report(state: MessagesState) -> dict:
    msgs = "\n".join([f"{type(m).__name__}: {m.content[:200]}" for m in state["messages"]])
    report = structured_llm.invoke(f"Based on this code review conversation, generate a structured report:\n{msgs}")
    return {"messages": [HumanMessage(f"# Review Report\nScore: {report.score}/10\nVerdict: {report.verdict}\nBugs: {report.bugs}\nStyle: {report.style_issues}\nSecurity: {report.security_concerns}")]}


def route(state: MessagesState) -> str:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return "report"


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_node("report", generate_report)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route, {"tools": "tools", "report": "report"})
builder.add_edge("tools", "agent")
builder.add_edge("report", END)

graph = builder.compile()

code = "def process(data):\n    eval(data)\n    password = 'secret123'\n    # TODO: add validation\n    pass"
result = graph.invoke({"messages": [HumanMessage(f"Review this code:\n{code}")]})
print("=== Review Result ===")
print(result["messages"][-1].content)
