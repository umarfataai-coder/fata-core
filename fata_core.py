import urllib.request
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Fata AI - Super Intelligence Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    user_id: str
    prompt: str

# Tsarin umarni don amsawa da harshen da mai amfani ya yi magana da shi (Hausa/English)
SYSTEM_INSTRUCTIONS = """
You are Fata AI, an intelligent AI assistant built by Umar.
Always reply in the exact language used by the user. If the user greets or asks in Hausa, respond fluent and respectful Hausa.
Keep responses clear and concise.
"""

def query_ollama_brain(prompt: str) -> str:
    url = "http://127.0.0.1:11434/api/generate"
    
    payload = {
        "model": "llama3.1",
        "prompt": f"{SYSTEM_INSTRUCTIONS}\nUser: {prompt}\nFata AI:",
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "An samu kuskure wajen gina amsa.")
    except Exception as e:
        return f"Gafara dai Shugaba, an samu matsala. Error: {str(e)}"

@app.get("/")
def home():
    return {"status": "Active", "system": "Fata AI Engine Online"}

@app.post("/v1/chat")
async def chat_with_fata(query: Query):
    ai_response = query_ollama_brain(query.prompt)
    return {"status": "success", "response": ai_response}

if __name__ == "__main__":
    print("🚀 Fata AI (Llama 3.1 Engine) is Active on Port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)