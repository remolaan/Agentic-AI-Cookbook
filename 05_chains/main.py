from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# ============================================================
# 1. Basic Chain — prompt | llm | parser
# ============================================================
prompt = ChatPromptTemplate.from_messages([
    ("human", "Write a short {tone} poem about {subject}."),
])
chain = prompt | llm | StrOutputParser()
response = chain.invoke({"tone": "funny", "subject": "a penguin learning to code"})
print("=== Basic Chain (prompt | llm) ===")
print(response)
print()

# ============================================================
# 2. Sequential Chain — pipe one chain's output into another
# ============================================================
name_chain = (
    ChatPromptTemplate.from_messages([
        ("human", "Suggest a name for a {product}. Only output the name, nothing else."),
    ])
    | llm
    | StrOutputParser()
)

tagline_chain = (
    ChatPromptTemplate.from_messages([
        ("human", "Write a short tagline for a product called {name}."),
    ])
    | llm
    | StrOutputParser()
)

# Chain them: product → name → tagline
seq_chain = name_chain | (lambda name: {"name": name}) | tagline_chain
response = seq_chain.invoke("cat-themed coffee shop")
print("=== Sequential Chain (chained LCEL) ===")
print(f"Tagline: {response}")
print()

# ============================================================
# 3. Multi-Output Chain — RunnableParallel
# ============================================================
dish_chain = (
    ChatPromptTemplate.from_messages([
        ("human", "Create a detailed dish description for {cuisine} cuisine."),
    ])
    | llm
    | StrOutputParser()
)

# Chain that takes dish_description and suggests wine
wine_chain = (
    ChatPromptTemplate.from_messages([
        ("human", "Suggest a wine pairing for this dish: {dish_description}"),
    ])
    | llm
    | StrOutputParser()
)

# Build a multi-step pipeline
multi_chain = (
    RunnablePassthrough.assign(
        dish_description=dish_chain
    )
    | RunnablePassthrough.assign(
        wine_pairing=wine_chain
    )
)

response = multi_chain.invoke({"cuisine": "Italian"})
print("=== Multi-Output Chain (assign) ===")
print("Dish:", response["dish_description"])
print()
print("Wine:", response["wine_pairing"])
