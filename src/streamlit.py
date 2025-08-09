import streamlit as st
import requests

# ==== CONFIG ====
API_BASE = "http://localhost:8000/api"  # Change to your FastAPI host
UPLOAD_ENDPOINT = f"{API_BASE}/data/upload"
CHAT_ENDPOINT_RAG = f"{API_BASE}/chat/chat"
CHAT_ENDPOINT_LANGGRAPH = f"{API_BASE}/langgraph/chat_langgraph"

st.set_page_config(page_title="📄 Multi-Mode Chatbot", page_icon="🤖", layout="wide")

# ==== SESSION STATE ====
if "messages" not in st.session_state:
    st.session_state.messages = []  # List of {"role": "user"/"assistant", "content": str}
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "RAG"  # Default mode

# ==== SIDEBAR ====
st.sidebar.title("📂 Upload Documents")
uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and processing PDF..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        try:
            res = requests.post(UPLOAD_ENDPOINT, files=files)
            if res.status_code == 200:
                st.sidebar.success(f"✅ {uploaded_file.name} processed successfully!")
            else:
                st.sidebar.error(f"❌ Failed: {res.json().get('response', 'Unknown error')}")
        except Exception as e:
            st.sidebar.error(f"⚠ Error: {e}")

# Chat mode selector
st.sidebar.markdown("### 💬 Chat Mode")
mode_choice = st.sidebar.radio(
    "Select Chat Mode:",
    ("RAG", "LangGraph"),
    index=0
)
st.session_state.chat_mode = mode_choice

# ==== TITLE ====
st.title("🤖 Multi-Mode Chatbot")
st.write(f"Current mode: **{st.session_state.chat_mode}**")

# ==== CHAT DISPLAY ====
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

# ==== CHAT INPUT ====
if prompt := st.chat_input("Type your question..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Choose endpoint based on mode
    if st.session_state.chat_mode == "RAG":
        endpoint = CHAT_ENDPOINT_RAG
    else:
        endpoint = CHAT_ENDPOINT_LANGGRAPH

    # Call API
    try:
        res = requests.post(endpoint, json={"question": prompt})
        if res.status_code == 200:
            bot_reply = res.json().get("response", "")
        else:
            bot_reply = f"⚠ Error: {res.json().get('response', 'Unknown error')}"
    except Exception as e:
        bot_reply = f"⚠ Exception: {e}"

    # Append bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)
