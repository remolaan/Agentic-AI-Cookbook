from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")


class State(TypedDict):
    input: str
    validated: bool
    output: str


def validate(state: State) -> Command:
    response = llm.invoke(f"Is this valid input? '{state['input']}'. Reply 'yes' or 'no'.")
    is_valid = "yes" in response.content.lower()
    if is_valid:
        return Command(goto="process", update={"validated": True})
    else:
        return Command(goto="fix", update={"validated": False})


def fix(state: State) -> Command:
    response = llm.invoke(f"Fix this input: '{state['input']}'. Return only the corrected version.")
    return Command(goto="process", update={"input": response.content.strip(), "validated": True})


def process(state: State) -> dict:
    response = llm.invoke(f"Process this: {state['input']}")
    return {"output": response.content}


builder = StateGraph(State)
builder.add_node("validate", validate)
builder.add_node("fix", fix)
builder.add_node("process", process)
builder.add_edge(START, "validate")
builder.add_edge("fix", "process")
builder.add_edge("process", END)

graph = builder.compile()

for input_text in ["Hello world", "$$$ invalid $$$"]:
    result = graph.invoke({"input": input_text, "validated": False, "output": ""})
    print(f"Input: {input_text}")
    print(f"Validated: {result['validated']}")
    print(f"Output: {result['output'][:60]}...\n")
