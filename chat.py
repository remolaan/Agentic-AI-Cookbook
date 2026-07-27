from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

print("LangChain + DeepSeek Chatbot")
print("Type 'quit' to exit.\n")

while True:
    msg = input("> ")
    if msg.lower() in ("quit", "exit", "q"):
        break
    response = llm.invoke(msg)
    print("AI:", response.content)
    print()
