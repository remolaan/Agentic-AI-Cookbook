from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

load_dotenv()
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
parser = StrOutputParser()

positive = ChatPromptTemplate.from_template("Respond positively: {input}") | llm | parser
negative = ChatPromptTemplate.from_template("Respond negatively: {input}") | llm | parser
neutral  = ChatPromptTemplate.from_template("Respond neutrally: {input}")  | llm | parser

branch = RunnableBranch(
    (lambda x: "great" in x.lower() or "love" in x.lower(), positive),
    (lambda x: "bad" in x.lower() or "hate" in x.lower(),   negative),
    neutral,
)

for text in ["I love this!", "This is bad.", "The sky is blue."]:
    print(f"Input: {text}\nOutput: {branch.invoke(text)}\n")
