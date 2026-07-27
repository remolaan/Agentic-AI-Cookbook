from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- 1. Custom callback handler ---
class TokenCounter(BaseCallbackHandler):
    def __init__(self):
        self.token_count = 0

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"[LLM Start] Prompt length: {len(prompts[0])} chars")

    def on_llm_end(self, response, **kwargs):
        tokens = sum(len(generation.message.content.split()) for generation in response.generations[0])
        self.token_count += tokens
        print(f"[LLM End] Generated ~{tokens} words")

    def on_llm_error(self, error, **kwargs):
        print(f"[LLM Error] {error}")

handler = TokenCounter()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", callbacks=[handler])
response = llm.invoke("Tell me a short story about a robot.")
print(f"Response: {response.content}")
print(f"Total tokens tracked: {handler.token_count}")
print()

# --- 2. Streaming tokens ---
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", streaming=True)
prompt = ChatPromptTemplate.from_template("Write a haiku about {topic}")
chain = prompt | llm | StrOutputParser()

print("=== Streaming output ===")
full = ""
for chunk in chain.stream({"topic": "the ocean"}):
    print(chunk, end="", flush=True)
    full += chunk
print("\n")
