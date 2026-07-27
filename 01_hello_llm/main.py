from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- Style 1: Direct invoke ---
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
response = llm.invoke("What is LangChain?")
print("=== Direct invoke ===")
print(response.content)
print()

# --- Style 2: Prompt template ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Python tutor."),
    ("human", "Explain {topic} in one paragraph aimed at a beginner."),
])

topic = "what an LLM is"
messages = prompt.invoke({"topic": topic})
response = llm.invoke(messages)
print("=== Prompt template ===")
print(response.content)
print()

# --- Style 3: Chain ---
chain = prompt | llm
response = chain.invoke({"topic": "what LangChain is"})
print("=== Chain (prompt | model) ===")
print(response.content)
