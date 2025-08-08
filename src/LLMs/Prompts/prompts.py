from enum import Enum

class LLMPrompts(Enum):
    SYSTEM_PROMPT = "\n".join([
        "You are a helpful assistant. Use ONLY the information provided in the context below to answer the user's question.",
        "If you cannot answer using the context, say you don’t know — do NOT make up an answer.",
        "Context:",
        "{context}",
     
        "YOUR Answer:"
        ])
    
    HUMAN_PROMPT ="\n".join([
         "User Question:",
        "{question}"
    ])