from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import LLMChain, SimpleSequentialChain, SequentialChain

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# --- 1. LLMChain (classic) ---
prompt = ChatPromptTemplate.from_messages([
    ("human", "Write a short {tone} poem about {subject}."),
])
chain = LLMChain(llm=llm, prompt=prompt)
response = chain.invoke({"tone": "funny", "subject": "a penguin learning to code"})
print("=== LLMChain ===")
print(response["text"])
print()

# --- 2. SimpleSequentialChain ---
chain_1 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_messages([
        ("human", "Suggest a name for a {product}. Only output the name."),
    ]),
    output_key="name",
)
chain_2 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_messages([
        ("human", "Write a tagline for a product called {name}."),
    ]),
    output_key="tagline",
)
seq_chain = SimpleSequentialChain(chains=[chain_1, chain_2])
response = seq_chain.invoke("cat-themed coffee shop")
print("=== SimpleSequentialChain ===")
print("Name + Tagline:", response["output"])
print()

# --- 3. SequentialChain (multi-input / multi-output) ---
chain_1 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_messages([
        ("human", "Create a detailed dish description for {cuisine} cuisine."),
    ]),
    output_key="dish_description",
)
chain_2 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_messages([
        ("human", "Suggest a wine pairing for this dish: {dish_description}"),
    ]),
    output_key="wine_pairing",
)
multi_chain = SequentialChain(
    chains=[chain_1, chain_2],
    input_variables=["cuisine"],
    output_variables=["dish_description", "wine_pairing"],
)
response = multi_chain.invoke({"cuisine": "Italian"})
print("=== SequentialChain ===")
print("Dish:", response["dish_description"])
print()
print("Wine:", response["wine_pairing"])
