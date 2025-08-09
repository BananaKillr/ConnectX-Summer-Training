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

## ⚙️ 1. Environment Setup

### Step 1 — Create Python Environment
Use **Python 3.12**:
```bash
# Create a virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

Step 2 — Install Dependencies

Dependencies are listed in:

src/requirements.txt

Install them:

pip install -r src/requirements.txt



📂 4. Project Structure
Documents/                     # (Example folder for uploaded PDFs)
src/
│
├── Agents/                    # Intelligent agents
│   ├── LangGraphAgent.py       # LangGraph conversation flow agent
│   └── __init__.py
│
├── Config/                     # Configuration files
│   ├── config.py               # Loads env variables and settings
│   └── __init__.py
│
├── Database/                   # Document storage
│   ├── datastore/              # Original uploaded files
│   ├── vectordb/                # Vector embeddings for retrieval
│   └── embedding/               # Embedding logic
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

🔑 2. Environment Variables

The project uses a .env file for API keys and configuration.
Step 1 — Create .env

Copy the example file:

cp .env.example .env

Step 2 — Fill in values

All environment variables are loaded in src/Config/config.py.
You must update .env with:

GOOGLE_API_KEY=your_google_api_key_here

…and any other variables required.
🚀 3. Running the Project
Step 1 — Start the Backend (FastAPI)

uvicorn main:app --reload

Step 2 — Start the Frontend (Streamlit)

streamlit run streamlit.py
