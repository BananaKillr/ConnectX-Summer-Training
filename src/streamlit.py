import streamlit as st
import requests

# ==== CONFIG ====
API_BASE = "http://localhost:8000/api"  # Change to your FastAPI host
UPLOAD_ENDPOINT = f"{API_BASE}/data/upload"
CHAT_ENDPOINT = f"{API_BASE}/chat/chat"

st.set_page_config(page_title="📄 RAG Chatbot", page_icon="🤖", layout="wide")

# ==== SESSION STATE ====
if "messages" not in st.session_state:
    st.session_state.messages = []  # List of {"role": "user"/"assistant", "content": str}

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

# ==== TITLE ====
st.title("🤖 RAG-powered Chatbot")
st.write("Ask questions about your uploaded PDFs!")

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

    # Display immediately
    st.chat_message("user").markdown(prompt)

    # Call API
    try:
        res = requests.post(CHAT_ENDPOINT, json={"question": prompt})
        if res.status_code == 200:
            bot_reply = res.json().get("response", "")
        else:
            bot_reply = f"⚠ Error: {res.json().get('response', 'Unknown error')}"
    except Exception as e:
        bot_reply = f"⚠ Exception: {e}"

    # Append bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)
