from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import (
    StrOutputParser,
    CommaSeparatedListOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. StrOutputParser ---
parser = StrOutputParser()
chain = ChatPromptTemplate.from_messages([
    ("human", "Tell me a fun fact about {animal}."),
]) | llm | parser
response = chain.invoke({"animal": "octopus"})
print("=== StrOutputParser ===")
print(response)
print()

# --- 2. CommaSeparatedListOutputParser ---
parser = CommaSeparatedListOutputParser()
chain = ChatPromptTemplate.from_messages([
    ("human", "List 5 {topic}. {format_instructions}"),
]).partial(format_instructions=parser.get_format_instructions()) | llm | parser
response = chain.invoke({"topic": "programming languages"})
print("=== CommaSeparatedListOutputParser ===")
print(response)
print(type(response))
print()

# --- 3. PydanticOutputParser ---
class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age")
    hobbies: list[str] = Field(description="List of hobbies")

parser = PydanticOutputParser(pydantic_object=Person)
chain = ChatPromptTemplate.from_messages([
    ("human", "Generate a fictional person. {format_instructions}"),
]).partial(format_instructions=parser.get_format_instructions()) | llm | parser
response = chain.invoke({})
print("=== PydanticOutputParser ===")
print(f"Name: {response.name}")
print(f"Age: {response.age}")
print(f"Hobbies: {response.hobbies}")
