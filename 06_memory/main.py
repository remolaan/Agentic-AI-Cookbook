from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")

# Shared prompt with a history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer concisely."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# ============================================================
# 1. BufferMemory — Full history (RunnableWithMessageHistory)
# ============================================================
print("=== BufferMemory — Full History ===")

store = {}

def get_session(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session,
    input_messages_key="input",
    history_messages_key="history",
)

response = chain_with_history.invoke(
    {"input": "Hi, I'm Alice."},
    config={"configurable": {"session_id": "buffer_1"}},
)
print(f"Turn 1 — AI: {response}")

response = chain_with_history.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "buffer_1"}},
)
print(f"Turn 2 — AI: {response}")

# Show the stored history
history = store["buffer_1"].messages
print(f"History stored: {len(history)} messages")
for m in history:
    print(f"  [{type(m).__name__}] {m.content[:50]}")
print()

# ============================================================
# 2. WindowMemory — Custom trim to last k messages
# ============================================================
print("=== WindowMemory (k=2) ===")

class WindowedChatMessageHistory(ChatMessageHistory):
    k: int = 2

    def add_message(self, message):
        super().add_message(message)
        pairs = self.k * 2
        if len(self.messages) > pairs:
            self.messages = self.messages[-pairs:]

window_store = {}

def get_window_session(session_id: str):
    if session_id not in window_store:
        window_store[session_id] = WindowedChatMessageHistory(k=2)
    return window_store[session_id]

window_chain = RunnableWithMessageHistory(
    chain,
    get_window_session,
    input_messages_key="input",
    history_messages_key="history",
)

response = window_chain.invoke(
    {"input": "My favorite color is blue."},
    config={"configurable": {"session_id": "window_1"}},
)
print(f"Turn 1 — AI: {response}")

response = window_chain.invoke(
    {"input": "What is my favorite color?"},
    config={"configurable": {"session_id": "window_1"}},
)
print(f"Turn 2 — AI: {response}")

# Add a third turn — first turn should be dropped
response = window_chain.invoke(
    {"input": "I also like pizza."},
    config={"configurable": {"session_id": "window_1"}},
)
print(f"Turn 3 — AI: {response}")

window_history = window_store["window_1"].messages
print(f"History stored: {len(window_history)} messages (max {2*2})")
print()

# ============================================================
# 3. SummaryMemory — Manual summarization example
# ============================================================
print("=== SummaryMemory ===")

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the conversation so far concisely. Preserve key facts about the user."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

summary_chain = summary_prompt | llm | StrOutputParser()

summary_store = {}

def get_summary_session(session_id: str):
    if session_id not in summary_store:
        summary_store[session_id] = ChatMessageHistory()
    return summary_store[session_id]

summary_chain_with_history = RunnableWithMessageHistory(
    summary_chain,
    get_summary_session,
    input_messages_key="input",
    history_messages_key="history",
)

# Turn 1
response = summary_chain_with_history.invoke(
    {"input": "I love hiking in the mountains and drinking coffee."},
    config={"configurable": {"session_id": "summary_1"}},
)
print(f"Turn 1 — AI: {response}")

# Summarize the history so far
print("\nSummarizing conversation so far...")
summarizer_llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
hist = summary_store["summary_1"].messages
history_text = "\n".join(f"{type(m).__name__}: {m.content}" for m in hist)
summary = summarizer_llm.invoke(
    f"Summarize this conversation in 1-2 sentences, keeping key user facts:\n\n{history_text}"
)
print(f"Summary: {summary.content}")

# Turn 2 (with summary injected manually)
response = summary_chain_with_history.invoke(
    {"input": f"What do you know about me? (Here's a summary of our chat: {summary.content})"},
    config={"configurable": {"session_id": "summary_1"}},
)
print(f"Turn 2 — AI: {response}")
