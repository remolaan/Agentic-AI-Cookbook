# LangChain Learning Repository

A step-by-step journey through LangChain — from your first LLM call to production-ready deployments.

```mermaid
%%{init: {'theme':'neutral', 'flowchart': {'curve': 'basis'}}}%%
flowchart LR
    A["🚀 Setup<br/>00"] --> B["01 Hello LLM"]
    B --> C["02 Prompts"] --> D["03 Parsers"] --> E["04 Chat Models"] --> F["05 Chains"]
    F --> G["06 Memory"] --> H["07 Loaders"] --> I["08 Splitters"] --> J["09 Vector Stores"] --> K["10 RAG"]
    K --> L["11 Advanced Retrieval"] --> M["12 Agents"] --> N["13 LCEL"] --> O["14 Callbacks"] --> P["15 Evaluation"]
    P --> Q["16 Caching"] --> R["17 Streaming"] --> S["18 Deployment 🚢"]
    
    style A fill:#e1f5fe,stroke:#01579b,color:#01579b
    style S fill:#e8f5e9,stroke:#2e7d32,color:#2e7d32
    style K fill:#fff3e0,stroke:#e65100,color:#e65100
```

## Phases

```mermaid
%%{init: {'theme':'neutral'}}%%
quadrantChart
    title LangChain Learning Roadmap
    x-axis "Simple" --> "Complex"
    y-axis "Fundamental" --> "Applied"
    quadrant-1 "Ready to Build 🛠️"
    quadrant-2 "Production 🚢"
    quadrant-3 "Beginner 🌱"
    quadrant-4 "Advanced 🧠"
    "00 Setup": [0.15, 0.2]
    "01-05 Basics": [0.25, 0.25]
    "06-10 RAG": [0.45, 0.4]
    "11-15 Advanced": [0.65, 0.65]
    "16-18 Production": [0.85, 0.85]
```

## Prerequisites

- Python 3.12 (3.11 works too)
- A [DeepSeek API key](https://platform.deepseek.com) (free to sign up)

## Quick Start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

## How a lesson works

Each lesson shows you the concept and the code side by side:

```mermaid
flowchart LR
    subgraph README["README.md 📖"]
        CONCEPT["What & Why"] --> DIAGRAM["Visual Flow"] --> CODE_EXPLAIN["Code Walkthrough"]
    end
    subgraph CODE["main.py 💻"]
        RUN["python main.py"] --> LLM_CALL["LLM Call 🔥"] --> OUTPUT["See Results ✅"]
    end
    README -.-> CODE
```

## Lessons

### 🌱 Beginner — Basics

| # | Lesson | What you build | Core concept |
|---|--------|---------------|--------------|
| 00 | **Setup** | Environment test | `ChatOpenAI` to DeepSeek |
| 01 | **Hello LLM** | First LLM call | `.invoke()`, prompt templates, chains |
| 02 | **Prompt Templates** | Reusable prompts | Variables, roles, few-shot |
| 03 | **Output Parsers** | Structured output | `StrOutputParser`, `PydanticOutputParser` |
| 04 | **Chat Models** | Multi-turn chat | System/human/AI messages |
| 05 | **Chains** | Pipeline steps | `LLMChain`, `SequentialChain` |

**Data flow in a chain:**

```mermaid
sequenceDiagram
    participant U as User
    participant P as Prompt
    participant M as Model
    participant O as Output
    U->>P: "Explain {topic}"
    P->>M: Formatted message
    M->>O: Raw text
    O->>U: Clean answer
```

### 🔍 Intermediate — RAG & Memory

| # | Lesson | What you build | Core concept |
|---|--------|---------------|--------------|
| 06 | **Memory** | Chat with recall | `BufferMemory`, `SummaryMemory` |
| 07 | **Document Loaders** | Ingest data | `TextLoader`, `CSVLoader`, `WebBaseLoader` |
| 08 | **Text Splitters** | Chunk documents | `RecursiveCharacterTextSplitter` |
| 09 | **Vector Stores** | Semantic search | Chroma, FAISS, embeddings |
| 10 | **RAG** | Ask your documents | Full retrieval pipeline |

**RAG pipeline:**

```mermaid
flowchart LR
    A["📄 Load<br/>Documents"] --> B["✂️ Split<br/>into chunks"]
    B --> C["🔢 Embed<br/>(vectors)"]
    C --> D["🗄️ Store<br/>Vector DB"]
    E["❓ User Question"] --> F["🔍 Retrieve<br/>similar chunks"]
    D --> F
    F --> G["📝 Augment<br/>Prompt + Context"]
    G --> H["🤖 Generate<br/>Answer"]
    H --> I["✅ Final Answer"]
    
    style A fill:#e3f2fd,stroke:#1565c0
    style E fill:#fff3e0,stroke:#e65100
    style I fill:#e8f5e9,stroke:#2e7d32
```

### 🧠 Advanced — Agents & LCEL

| # | Lesson | What you build | Core concept |
|---|--------|---------------|--------------|
| 11 | **Advanced Retrieval** | Smarter search | `MultiQuery`, `SelfQuery` |
| 12 | **Agents** | AI with tools | ReAct loop, tool calling |
| 13 | **LCEL** | Composable chains | `|` operator, `RunnableParallel` |
| 14 | **Callbacks & Streaming** | Live output | Token streaming, custom handlers |
| 15 | **Evaluation** | Test quality | Criteria evaluation |

**Agent loop:**

```mermaid
flowchart TD
    Q["User Question"] --> T["🤔 Think<br/>What tool to use?"]
    T --> A["⚡ Act<br/>Call the tool"]
    A --> O["👀 Observe<br/>Get result"]
    O --> D{"Done?"}
    D -->|No| T
    D -->|Yes| R["📢 Final Answer"]
    
    style Q fill:#fff3e0,stroke:#e65100
    style R fill:#e8f5e9,stroke:#2e7d32
```

### 🚢 Production — Ship It

| # | Lesson | What you build | Core concept |
|---|--------|---------------|--------------|
| 16 | **Caching** | Save money | InMemory, SQLite cache |
| 17 | **Streaming & Async** | Real-time | `async`, `astream`, `asyncio.gather` |
| 18 | **Deployment** | REST API | FastAPI, Docker, uvicorn |
| 19 | **Gradio UI** | Web interfaces | `gr.ChatInterface`, streaming, RAG UI |

### 🎨 Bonus

| File | What it does |
|------|-------------|
| `chat.py` | Terminal chatbot (no UI needed) |
| `gradio_chat.py` | One-file Gradio web chatbot |

## Running a lesson

```bash
source .venv/bin/activate
python 01_hello_llm/main.py
```

Every lesson is self-contained. The `README.md` in each folder explains the concepts, and `main.py` is ready to run.

## Running the Gradio apps

```bash
# Quick chat (one file, no lesson):
python gradio_chat.py

# Full 3-tab Gradio lesson:
python 19_gradio/main.py
```

Then open `http://localhost:7860` in your browser.
