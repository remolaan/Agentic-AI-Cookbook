from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
)

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. ConversationBufferMemory (full history) ---
memory = ConversationBufferMemory(return_messages=True)
chain = ConversationChain(llm=llm, memory=memory)

print("=== BufferMemory — Turn 1 ===")
response = chain.invoke("Hi, I'm Alice.")
print("AI:", response["response"])

print()
print("=== BufferMemory — Turn 2 ===")
response = chain.invoke("What's my name?")
print("AI:", response["response"])
print()

# --- 2. ConversationBufferWindowMemory (last 2 turns) ---
memory = ConversationBufferWindowMemory(k=2, return_messages=True)
chain = ConversationChain(llm=llm, memory=memory)

print("=== WindowMemory (k=2) ===")
response = chain.invoke("My favorite color is blue.")
print("AI:", response["response"])
response = chain.invoke("What is my favorite color?")
print("AI:", response["response"])
print()

# --- 3. ConversationSummaryMemory ---
memory = ConversationSummaryMemory(llm=llm, return_messages=True)
chain = ConversationChain(llm=llm, memory=memory)

print("=== SummaryMemory ===")
response = chain.invoke("I love hiking in the mountains and drinking coffee.")
print("AI:", response["response"])
response = chain.invoke("What do you know about me?")
print("AI:", response["response"])
