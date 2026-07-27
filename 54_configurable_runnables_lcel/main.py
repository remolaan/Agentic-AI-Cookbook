from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableField

load_dotenv()

base_llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# === 1. configurable_fields — change temperature at runtime ===
configurable_llm = base_llm.configurable_fields(
    temperature=ConfigurableField(id="temp", name="Temperature",
                                   description="LLM creativity 0-1"),
)

chain = ChatPromptTemplate.from_template("Write a {tone} sentence about {topic}.") | configurable_llm | StrOutputParser()

print("=== 1. configurable_fields ===")
result = chain.invoke({"tone": "funny", "topic": "cats"},
                       config={"configurable": {"temp": 0.9}})
print(f"High temp (creative): {result[:60]}...")

result = chain.invoke({"tone": "funny", "topic": "cats"},
                       config={"configurable": {"temp": 0.1}})
print(f"Low temp (precise):  {result[:60]}...\n")

# === 2. configurable_alternatives — swap entire chains ===
strict_chain = ChatPromptTemplate.from_template("Answer very precisely: {input}") | base_llm | StrOutputParser()
creative_chain = ChatPromptTemplate.from_template("Answer creatively with flair: {input}") | base_llm | StrOutputParser()

chain_with_alternatives = strict_chain.configurable_alternatives(
    ConfigurableField(id="style", name="Answer style"),
    default_key="strict",
    creative=creative_chain,
)

print("=== 2. configurable_alternatives ===")
result = chain_with_alternatives.invoke("What is AI?",
    config={"configurable": {"style": "strict"}})
print(f"Strict: {result[:60]}...")

result = chain_with_alternatives.invoke("What is AI?",
    config={"configurable": {"style": "creative"}})
print(f"Creative: {result[:60]}...\n")

# === 3. Combined: fields + alternatives ===
combined = chain_with_alternatives.configurable_fields(
    temperature=ConfigurableField(id="temp")
)

print("=== 3. Combined ===")
result = combined.invoke("Tell me about space",
    config={"configurable": {"style": "creative", "temp": 0.8}})
print(f"Creative + high temp: {result[:60]}...")
