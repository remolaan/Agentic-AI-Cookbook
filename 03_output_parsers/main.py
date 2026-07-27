from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# ============================================================
# 1. StrOutputParser — plain text cleanup
# ============================================================
from langchain_core.output_parsers import StrOutputParser

chain = ChatPromptTemplate.from_messages([
    ("human", "Tell me a fun fact about {animal}."),
]) | llm | StrOutputParser()
print("=== StrOutputParser ===")
print(chain.invoke({"animal": "octopus"}))
print()

# ============================================================
# 2. CommaSeparatedListOutputParser
# ============================================================
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
chain = ChatPromptTemplate.from_messages([
    ("human", "List 5 {topic}. {format_instructions}"),
]).partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({"topic": "programming languages"})
print("=== CommaSeparatedList ===")
print(result, type(result))
print()

# ============================================================
# 3. PydanticOutputParser (classic way)
# ============================================================
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age")
    hobbies: list[str] = Field(description="Hobbies")

parser = PydanticOutputParser(pydantic_object=Person)
chain = ChatPromptTemplate.from_messages([
    ("human", "Generate a fictional person. {format_instructions}"),
]).partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({})
print("=== PydanticOutputParser ===")
print(f"  {result.name}, {result.age}, {result.hobbies}")
print()

# ============================================================
# 4. DatetimeOutputParser
# ============================================================
from langchain_classic.output_parsers import DatetimeOutputParser

parser = DatetimeOutputParser()
chain = ChatPromptTemplate.from_messages([
    ("human", "When was {event}? {format_instructions}"),
]).partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({"event": "the first moon landing"})
print("=== DatetimeOutputParser ===")
print(f"  {result}")
print()

# ============================================================
# 5. OutputFixingParser — auto-fix bad output
# ============================================================
from langchain_classic.output_parsers import OutputFixingParser

# Simulate bad output by asking for wrongly formatted data
class Joke(BaseModel):
    setup: str = Field(description="Joke setup")
    punchline: str = Field(description="Joke punchline")

bad_parser = PydanticOutputParser(pydantic_object=Joke)
fixing_parser = OutputFixingParser.from_llm(parser=bad_parser, llm=llm)

# This might produce bad JSON; the fixing parser auto-corrects it
chain = ChatPromptTemplate.from_messages([
    ("human", "Tell a joke about programming. {format_instructions}"),
]).partial(format_instructions=bad_parser.get_format_instructions()) | llm | fixing_parser
result = chain.invoke({})
print("=== OutputFixingParser ===")
print(f"  Setup: {result.setup}")
print(f"  Punchline: {result.punchline}")
print()

# ============================================================
# 6. JsonOutputParser (simpler than Pydantic)
# ============================================================
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
chain = ChatPromptTemplate.from_messages([
    ("human", "List 3 countries and their capitals as JSON. {format_instructions}"),
]).partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({})
print("=== JsonOutputParser ===")
for item in result:
    print(f"  {item}")
