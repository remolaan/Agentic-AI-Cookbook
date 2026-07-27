from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

translate = (
    ChatPromptTemplate.from_template("Translate '{input}' to French. Reply with only the translation.")
    | llm
    | StrOutputParser()
)

words = ["hello", "goodbye", "thank you", "please", "sorry"]
results = translate.batch([{"input": w} for w in words])
print("=== Batch Translation ===")
for word, translation in zip(words, results):
    print(f"  {word} → {translation}")

sentiment = (
    ChatPromptTemplate.from_template("Classify sentiment of '{input}' as positive/negative/neutral. One word.")
    | llm
    | StrOutputParser()
)

texts = ["I love this!", "This is terrible.", "It's okay."]
results = sentiment.batch([{"input": t} for t in texts])
print("\n=== Batch Sentiment ===")
for text, sentiment in zip(texts, results):
    print(f"  {text} → {sentiment}")
