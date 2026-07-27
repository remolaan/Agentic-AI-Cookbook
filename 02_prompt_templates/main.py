from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    FewShotChatMessagePromptTemplate,
)

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. ChatPromptTemplate (multi-message) ---
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert."),
    ("human", "Tell me a {level} fact about {topic}."),
])
chain = chat_template | llm
response = chain.invoke({"role": "Python", "level": "beginner", "topic": "lists"})
print("=== ChatPromptTemplate ===")
print(response.content)
print()

# --- 2. String PromptTemplate (simpler) ---
string_template = PromptTemplate.from_template(
    "Translate this to {language}: {text}"
)
chain = string_template | llm
response = chain.invoke({"language": "French", "text": "Hello, how are you?"})
print("=== String PromptTemplate ===")
print(response.content)
print()

# --- 3. Few-shot prompting ---
examples = [
    {"input": "LangChain is hard", "sentiment": "negative"},
    {"input": "I love Python", "sentiment": "positive"},
    {"input": "The weather is okay", "sentiment": "neutral"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{sentiment}"),
])
few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the sentiment as positive, negative, or neutral."),
    few_shot_prompt,
    ("human", "{input}"),
])
chain = final_prompt | llm
response = chain.invoke({"input": "I am learning LangChain and it is fun!"})
print("=== Few-shot ===")
print(response.content)
