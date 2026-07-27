"""
Gradio UI for Lesson 03 — Output Parsers.
Run:  python 03_output_parsers/main_gr.py 7860
"""
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers import DatetimeOutputParser, OutputFixingParser
import json

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

PARSERS = {
    "StrOutputParser": StrOutputParser,
    "CommaSeparatedList": CommaSeparatedListOutputParser,
    "PydanticOutputParser": PydanticOutputParser,
    "DatetimeOutputParser": DatetimeOutputParser,
    "JsonOutputParser": None,
}

last_raw = ""
last_parsed = ""


def run(parser_name, user_input):
    global last_raw, last_parsed
    prompt = ChatPromptTemplate.from_messages([("human", "{input}")])

    if parser_name == "StrOutputParser":
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"input": user_input})
        last_raw = result
        last_parsed = f"String: {result}"
        return result, last_parsed

    elif parser_name == "CommaSeparatedList":
        parser = CommaSeparatedListOutputParser()
        chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
        result = chain.invoke({"input": user_input})
        last_raw = str(result)
        last_parsed = f"List: {result}"
        return last_raw, last_parsed

    elif parser_name == "PydanticOutputParser":
        class Person(BaseModel):
            name: str = Field(description="Full name")
            age: int = Field(description="Age")
            hobbies: list[str] = Field(description="Hobbies")
        parser = PydanticOutputParser(pydantic_object=Person)
        chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
        result = chain.invoke({"input": user_input})
        last_raw = f"{result}"
        last_parsed = f"Name: {result.name}\nAge: {result.age}\nHobbies: {result.hobbies}"
        return last_raw, last_parsed

    elif parser_name == "DatetimeOutputParser":
        parser = DatetimeOutputParser()
        chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
        result = chain.invoke({"input": user_input})
        last_raw = str(result)
        last_parsed = f"Datetime: {result}"
        return last_raw, last_parsed

    elif parser_name == "JsonOutputParser":
        from langchain_core.output_parsers import JsonOutputParser
        parser = JsonOutputParser()
        chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
        result = chain.invoke({"input": user_input})
        last_raw = json.dumps(result, indent=2)
        last_parsed = f"JSON:\n{json.dumps(result, indent=2)}"
        return last_raw, last_parsed

    return "Select a parser", ""


with gr.Blocks(title="03 — Output Parsers") as app:
    gr.Markdown("# 03 — Output Parsers")
    gr.Markdown("Test different parsers on LLM output. See how each one transforms the raw response.")

    with gr.Accordion("⚙️ Parser Settings", open=False):
        parser_dd = gr.Dropdown(label="Parser Type", choices=list(PARSERS.keys()), value="StrOutputParser")

    user_input = gr.Textbox(label="Input Prompt", value="List 3 programming languages and their creators.", lines=2)
    run_btn = gr.Button("🚀 Run", variant="primary")

    with gr.Row():
        raw_output = gr.Textbox(label="Raw LLM Output", lines=6, interactive=False)
        parsed_output = gr.Textbox(label="Parsed Result", lines=6, interactive=False)

    run_btn.click(fn=run, inputs=[parser_dd, user_input], outputs=[raw_output, parsed_output])

    with gr.Accordion("📤 Raw Prompt Sent", open=False):
        gr.Textbox(label="Messages sent to LLM", lines=6, value="See terminal output.", interactive=False)
    with gr.Accordion("📥 Raw Response Metadata", open=False):
        gr.Textbox(label="Response object", lines=6, interactive=False)
    with gr.Accordion("📊 Token Usage", open=False):
        gr.Textbox(label="Token counts", lines=4, interactive=False)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7860
    app.launch(server_port=port, server_name="0.0.0.0")
