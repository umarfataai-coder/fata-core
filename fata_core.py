import urllib.request
import json
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Fata AI - Enterprise Engine Core")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Saita SQLite Database domin adana tattaunawa
def init_db():
    conn = sqlite3.connect("fata_memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            sender TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Query(BaseModel):
    user_id: str
    prompt: str

SYSTEM_INSTRUCTIONS = """You are Fata AI, a super-intelligent AI assistant created by Umar. 
Always remember the context of the conversation. 
Respond fluently in the language used by the user (Hausa or English). Be helpful and precise."""

def save_message(user_id: str, sender: str, message: str):
    conn = sqlite3.connect("fata_memory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, sender, message) VALUES (?, ?, ?)", (user_id, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id: str, limit: int = 10) -> str:
    conn = sqlite3.connect("fata_memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, message FROM chat_history 
        WHERE user_id = ? ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    
    # Maida tattaunawa cikin jeri
    history_text = ""
    for sender, msg in reversed(rows):
        history_text += f"\n{sender}: {msg}"
    return history_text

def query_ollama_brain(user_id: str, prompt: str) -> str:
    url = "http://127.0.0.1:11434/api/generate"
    
    # Adana sakon user a DB
    save_message(user_id, "User", prompt)
    
    # Kwasho tarihin tattaunawa daga Database
    context = get_chat_history(user_id, limit=6)
    full_prompt = f"{SYSTEM_INSTRUCTIONS}\nConversation History:\n{context}\nFata AI:"
    
    payload = {
        "model": "llama3.1",
        "prompt": full_prompt,
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.loads(response.read().decode('utf-8'))
            ai_reply = result.get("response", "An samu kuskure.")
            
            # Adana amsar AI a DB
            save_message(user_id, "Fata AI", ai_reply)
            return ai_reply
    except Exception as e:
        return f"Gafara dai Shugaba, an samu matsala wajen sadarwa: {str(e)}"

@app.get("/")
def home():
    return {"status": "Active", "system": "Fata AI Enterprise Core with SQLite Memory"}

@app.post("/v1/chat")
async def chat_with_fata(query: Query):
    ai_response = query_ollama_brain(query.user_id, query.prompt)
    return {"status": "success", "response": ai_response}

if __name__ == "__main__":
    print("🚀 Fata AI (Database-Backed Core) is Running on Port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)