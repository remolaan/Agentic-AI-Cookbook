from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda, RunnablePick, RunnableAssign
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain as chain_decorator

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
print()

# --- 4. RunnableLambda — wrap any Python function ---
def word_count(text: str) -> dict:
    return {"count": len(text.split()), "text": text}

count_chain = RunnableLambda(word_count)
result = count_chain.invoke("Hello world this is a test")
print("=== RunnableLambda ===")
print(f"  Words: {result}")
print()

# --- 5. RunnablePick — select specific keys ---
data = {"question": "What is AI?", "context": "AI is...", "answer": "Artificial Intelligence"}
picker = RunnablePick("answer")
print("=== RunnablePick ===")
print(f"  {picker.invoke(data)}")
print()

# --- 6. @chain decorator — turn any function into a chain ---
@chain_decorator
def custom_pipeline(topic: str) -> str:
    prompt = ChatPromptTemplate.from_template("Write a haiku about {topic}")
    response = (prompt | llm | StrOutputParser()).invoke({"topic": topic})
    return response.upper()

result = custom_pipeline.invoke("coding")
print("=== @chain decorator ===")
print(f"  {result}")
print()

# --- 7. RunnableAssign — explicit key assignment ---
assigner = RunnableAssign(
    mapper=RunnableParallel(upper=RunnableLambda(lambda x: x.upper() if isinstance(x, str) else str(x).upper()))
)
result = assigner.invoke({"text": "hello"})
print("=== RunnableAssign ===")
print(f"  {result}")
