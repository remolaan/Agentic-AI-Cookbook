from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
)

response = llm.invoke("Say 'Hello from DeepSeek!' in one sentence.")
print("AI:", response.content)
