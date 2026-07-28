"""
Gradio UI for Lesson 03 — Output Parsers.
Run:  python 03_output_parsers/main_gr.py 8090
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
from langchain_classic.output_parsers import DatetimeOutputParser
import json

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
last_raw = ""
last_parsed = ""
last_prompt = []
last_response = None

# Prompt template that includes format instructions
base_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}\n\n{format_instructions}"),
])


def run(parser_name, user_input):
    global last_raw, last_parsed, last_prompt, last_response

    result_raw = ""
    result_parsed = ""
    messages = []

    if parser_name == "StrOutputParser":
        prompt = base_prompt.partial(format_instructions="Reply directly and concisely.")
        chain = prompt | llm | StrOutputParser()
        result_raw = chain.invoke({"input": user_input})
        result_parsed = f"(str) {result_raw}"

    elif parser_name == "CommaSeparatedList":
        parser = CommaSeparatedListOutputParser()
        prompt = base_prompt.partial(format_instructions=parser.get_format_instructions())
        chain = prompt | llm | parser
        parsed = chain.invoke({"input": user_input})
        result_raw = str(parsed)
        result_parsed = f"(list) {parsed}"

    elif parser_name == "PydanticOutputParser":
        class Person(BaseModel):
            name: str = Field(description="Full name")
            age: int = Field(description="Age")
            hobbies: list[str] = Field(description="Hobbies")
        parser = PydanticOutputParser(pydantic_object=Person)
        prompt = base_prompt.partial(format_instructions=parser.get_format_instructions())
        chain = prompt | llm | parser
        parsed = chain.invoke({"input": user_input})
        result_raw = str(parsed)
        result_parsed = f"(Person) Name: {parsed.name}\nAge: {parsed.age}\nHobbies: {parsed.hobbies}"

    elif parser_name == "DatetimeOutputParser":
        parser = DatetimeOutputParser()
        prompt = base_prompt.partial(format_instructions=parser.get_format_instructions())
        chain = prompt | llm | parser
        parsed = chain.invoke({"input": user_input})
        result_raw = str(parsed)
        result_parsed = f"(datetime) {parsed}"

    elif parser_name == "JsonOutputParser":
        from langchain_core.output_parsers import JsonOutputParser
        parser = JsonOutputParser()
        prompt = base_prompt.partial(format_instructions=parser.get_format_instructions())
        chain = prompt | llm | parser
        parsed = chain.invoke({"input": user_input})
        result_raw = json.dumps(parsed, indent=2)
        result_parsed = f"(JSON)\n{json.dumps(parsed, indent=2)}"

    last_raw = result_raw
    last_parsed = result_parsed
    last_prompt = [{"role": "user", "content": user_input}]
    last_response = llm.invoke(user_input)

    return last_raw, last_parsed


with gr.Blocks(title="03 — Output Parsers") as app:
    gr.Markdown("# 03 — Output Parsers")
    gr.Markdown("Choose a parser, type input, and see how the raw LLM output differs from the parsed result.")

    with gr.Row():
        parser_dd = gr.Dropdown(label="Parser Type", choices=[
            "StrOutputParser", "CommaSeparatedList", "PydanticOutputParser",
            "DatetimeOutputParser", "JsonOutputParser",
        ], value="StrOutputParser")
        user_input = gr.Textbox(label="Your prompt", value="Generate a fictional person.", lines=1, scale=3)

    run_btn = gr.Button("🚀 Run", variant="primary")

    with gr.Row():
        raw_output = gr.Textbox(label="Raw LLM Output", lines=8, interactive=False, scale=1)
        parsed_output = gr.Textbox(label="Parsed Result", lines=8, interactive=False, scale=1)

    run_btn.click(fn=run, inputs=[parser_dd, user_input], outputs=[raw_output, parsed_output])

    with gr.Row():
        with gr.Accordion("📤 Raw Prompt Sent", open=False):
            raw_prompt_box = gr.Textbox(lines=8, interactive=False)
        with gr.Accordion("📥 Raw Response Metadata", open=False):
            raw_response_box = gr.Textbox(lines=8, interactive=False)
        with gr.Accordion("📊 Token Usage", open=False):
            token_box = gr.Textbox(lines=4, interactive=False)

    def refresh():
        p = "\n".join(f"[{m['role'].upper()}] {m['content'][:200]}" for m in last_prompt) if last_prompt else ""
        r = ""
        if last_response and hasattr(last_response, "response_metadata"):
            r = f"Content: {str(last_response.content)[:200]}\n\nMetadata: {json.dumps(last_response.response_metadata, indent=2, default=str)}"
        t = ""
        if last_response and hasattr(last_response, "response_metadata"):
            tu = last_response.response_metadata.get("token_usage", {})
            if tu:
                t = f"Prompt tokens: {tu.get('prompt_tokens','?')}\nCompletion: {tu.get('completion_tokens','?')}\nTotal: {tu.get('total_tokens','?')}"
        return p, r, t

    gr.Button("🔄 Refresh Debug Panels", variant="secondary").click(
        fn=refresh, inputs=[], outputs=[raw_prompt_box, raw_response_box, token_box]
    )

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    app.launch(server_port=port, server_name="0.0.0.0")
