from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# Note: DeepSeek doesn't support OpenAI's JSON mode (response_format).
# We use method="function_calling" which uses tool calling internally.
# For OpenAI: llm.with_structured_output(Model) works with default method.

# ============================================================
# 1. Basic with_structured_output
# ============================================================
print("=== 1. Basic with_structured_output ===")

class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    hobbies: list[str] = Field(description="List of hobbies")

structured_llm = llm.with_structured_output(Person, method="function_calling")
result = structured_llm.invoke("Generate a fictional person who loves coding and hiking")
print(f"Name: {result.name}")
print(f"Age: {result.age}")
print(f"Hobbies: {result.hobbies}")
print(type(result))
print()

# ============================================================
# 2. Nested models
# ============================================================
print("=== 2. Nested models ===")

class Address(BaseModel):
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    country: str = Field(description="Country name")

class Employee(BaseModel):
    name: str = Field(description="Employee name")
    role: str = Field(description="Job title")
    salary: int = Field(description="Annual salary in USD")
    address: Address = Field(description="Home address")

structured_llm = llm.with_structured_output(Employee, method="function_calling")
result = structured_llm.invoke("Create an employee record for a senior engineer in London")
print(f"Name: {result.name}")
print(f"Role: {result.role}")
print(f"Salary: ${result.salary}")
print(f"Address: {result.address.street}, {result.address.city}, {result.address.country}")
print()

# ============================================================
# 3. Literal types (enum-like)
# ============================================================
print("=== 3. Literal types ===")

class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(description="Overall sentiment")
    confidence: float = Field(description="Confidence score 0-1", ge=0, le=1)
    explanation: str = Field(description="Why this sentiment")

structured_llm = llm.with_structured_output(SentimentResult, method="function_calling")
result = structured_llm.invoke("I absolutely love this new phone! The camera is incredible.")
print(f"Sentiment: {result.sentiment}")
print(f"Confidence: {result.confidence}")
print(f"Explanation: {result.explanation}")
print()

# ============================================================
# 4. List of structured outputs
# ============================================================
print("=== 4. List output ===")

class Recipe(BaseModel):
    name: str = Field(description="Recipe name")
    cook_time_minutes: int = Field(description="Cooking time")
    ingredients: list[str] = Field(description="Required ingredients")

class RecipeCollection(BaseModel):
    recipes: list[Recipe] = Field(description="List of recipes")

structured_llm = llm.with_structured_output(RecipeCollection, method="function_calling")
result = structured_llm.invoke("Suggest 3 quick vegetarian dinner recipes")
for r in result.recipes:
    print(f"  🍳 {r.name} ({r.cook_time_minutes}min)")
    print(f"     {', '.join(r.ingredients[:3])}...")
print()

# ============================================================
# 5. Extraction from text
# ============================================================
print("=== 5. Information extraction ===")

class ExtractedPerson(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")
    occupation: str = Field(description="Job or occupation")

extractor = llm.with_structured_output(ExtractedPerson, method="function_calling")
text = "Sarah Johnson, a 34-year-old software engineer from Austin, loves rock climbing."
result = extractor.invoke(f"Extract info from: {text}")
print(f"Name: {result.name}, Age: {result.age}, Job: {result.occupation}")
