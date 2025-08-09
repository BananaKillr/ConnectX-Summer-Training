# ConnectX-Summer-Training
# 📚 LangGraph + RAG Chatbot

This project combines:
- **RAG (Retrieval-Augmented Generation)** for answering questions from uploaded documents.
- **LangGraph** for controlled conversation flows and message management.

It provides:
1. **Backend** (FastAPI) with endpoints for:
   - Uploading documents
   - Querying via RAG
   - Querying via LangGraph
2. **Frontend** (Streamlit) chat interface.

---

```
## ⚙️ 1. Environment Setup
```

### Step 1 — Create Python Environment  
Use **Python 3.12**:
```bash
# Create a virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### Step 2 — Install Dependencies  

Dependencies are listed in:
```
src/requirements.txt
```

Install them:
```bash
pip install -r src/requirements.txt
```

---

```
## 🔑 2. Environment Variables
```

The project uses a `.env` file for API keys and configuration.

### Step 1 — Create `.env`  
Copy the example file:
```bash
cp .env.example .env
```

### Step 2 — Fill in values  

All environment variables are loaded in:
```
src/Config/config.py
```
You must update `.env` with:
```
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=
EMBEDDING_MODEL_NAME=
Qdrant_db_path=./datastore
Qdrant_distance_method=dot
TEXT_EMBEDDING_MODEL_SIZE=
```

---


## 🚀 3. Running the Project

### Step 1 — Start the Backend (FastAPI)
```bash
uvicorn main:app --reload
```

### Step 2 — Start the Frontend (Streamlit)
```bash
streamlit run streamlit.py
```

---

## 📂 4. Project Structure

```
Documents/                    
src/
│
├── Agents/                    
│   ├── LangGraphAgent.py       # LangGraph conversation flow agent
│   └── __init__.py
│
├── Config/                     # Configuration files
│   ├── config.py               # Loads env variables and settings
│   └── __init__.py
│
├── Database/                   # Document storage
│   ├── vectordb/                # Vector embeddings for retrieval
│
├── LLMs/                       # Large Language Model integrations
│   ├── Embedding.py             # Generates embeddings from text
│   ├── Gemini.py                # Google Gemini LLM wrapper
│   ├── Prompts/                 # Prompt templates for queries
│   └── __init__.py
│
├── Routes/                     # API endpoints
│   └── ...                     # (Files for FastAPI routes)
│
├── main.py                     # FastAPI entrypoint
├── streamlit.py                 # Streamlit chat UI
├── requirements.txt             # Dependencies
├── .env                         # Environment variables (ignored in Git)
├── .env.example                 # Example .env template
├── langgraph.png                # LangGraph diagram (generated)
└── README.md                    # This file
```

---

## 🧠 5. How it Works


1. **Upload PDF** (via Streamlit sidebar) → sent to `/data/upload` endpoint → stored in `Database/datastore` and processed into vector embeddings in `Database/vectordb`.

2. **Ask a Question** in chat:
   - **RAG Mode** → Sends query to `/chat/chat` → Retrieves relevant chunks from vector DB → Passes context to LLM.
   - **LangGraph Mode** → Sends query to `/langgraph/chat_langgraph` → Processes via LangGraph’s state machine to manage conversation limits and structured responses.

3. **Response** is displayed in Streamlit chat.

---

## 📊 6. Key Components


- **LangGraphAgent.py**
  - Defines a LangGraph workflow with nodes:
    - `check_counter` → checks message limit
    - `call_llm` → sends query to Gemini API
    - `end_conversation` → stops when limit exceeded

- **config.py**
  - Central place for reading `.env` variables.

- **Embedding.py**
  - Generates embeddings from text for retrieval.

- **Gemini.py**
  - Wrapper for Google Gemini API.

- **Qdrant.py**
  - Integrates with Qdrant vector DB to create collections and store embeddings/texts.

- **Routes/**
  - API routes for:
    - Uploading documents, chunking, embedding, storage
    - Querying chat (RAG & LangGraph)

---


### Tips

- Keep your API keys private (never commit `.env` to GitHub).
- Start with **RAG mode** to understand basic retrieval before diving into LangGraph logic.
- Check `langgraph.png` to see a diagram of your LangGraph workflow.
- Experiment with prompt templates in `LLMs/Prompts`.
