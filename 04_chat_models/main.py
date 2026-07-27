from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. Role-based messages ---
messages = [
    SystemMessage("You are a sarcastic assistant. Answer with a straight face but a hint of irony."),
    HumanMessage("What is the meaning of life?"),
]
response = llm.invoke(messages)
print("=== Role-based messages ===")
print(response.content)
print()

# --- 2. Multi-turn conversation ---
messages = [
    SystemMessage("You are a friendly math tutor."),
    HumanMessage("What is 12 × 15?"),
]
response = llm.invoke(messages)
print("=== Turn 1 ===")
print("AI:", response.content)

messages.append(AIMessage(response.content))
messages.append(HumanMessage("Now explain it step by step."))

response = llm.invoke(messages)
print()
print("=== Turn 2 (with history) ===")
print("AI:", response.content)
print()

# --- 3. Convert ChatPromptTemplate to messages ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You speak like a {era} philosopher."),
    ("human", "Share your thoughts on {topic}."),
])
messages = prompt.invoke({"era": "Ancient Greek", "topic": "technology"})
response = llm.invoke(messages)
print("=== From ChatPromptTemplate ===")
print(response.content)
