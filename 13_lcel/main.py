from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. Basic passthrough ---
chain = {"input": RunnablePassthrough()} | ChatPromptTemplate.from_template("Say: {input}") | llm | StrOutputParser()
response = chain.invoke("Hello LCEL!")
print("=== RunnablePassthrough ===")
print(response)
print()

# --- 2. RunnableParallel — run two chains simultaneously ---
summary_prompt = ChatPromptTemplate.from_template("Summarize this in one sentence: {text}")
translation_prompt = ChatPromptTemplate.from_template("Translate this to French: {text}")

parallel_chain = RunnableParallel(
    summary=summary_prompt | llm | StrOutputParser(),
    translation=translation_prompt | llm | StrOutputParser(),
)
response = parallel_chain.invoke({"text": "LangChain makes it easy to build LLM applications."})
print("=== RunnableParallel ===")
print(f"Summary: {response['summary']}")
print(f"Translation: {response['translation']}")
print()

# --- 3. .assign() — add computed fields ---
chain = (
    RunnablePassthrough.assign(
        poem=lambda x: ChatPromptTemplate.from_template("Write a poem about {topic}") | llm | StrOutputParser() | (lambda t: t.strip())
    )
)
response = chain.invoke({"topic": "programming"})
print("=== .assign() ===")
print(response["poem"])
