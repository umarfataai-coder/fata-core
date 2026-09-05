import os
import subprocess

print("==========================================")
print("   INJINIYA FATA AI: STARTING ENGINE SETUP")
print("==========================================")

# 1. Shigar da Kayan Aiki (Dependencies Setup)
packages = [
    "fastapi",
    "uvicorn",
    "pydantic"
]

print("[+] Installing AI Backend Tools...")
for pkg in packages:
    subprocess.run(["pip", "install", pkg, "--quiet"])

# 2. Gina Core Server Code na Fata AI
fata_server_code = """
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Fata AI - Super Intelligence Core")

class Query(BaseModel):
    user_id: str
    prompt: str

SYSTEM_INSTRUCTION = "You are Fata AI, a global multimodal super-intelligent assistant."

@app.get("/")
def home():
    return {"status": "Active", "system": "Fata AI Engine Online"}

@app.post("/v1/chat")
async def chat_with_fata(query: Query):
    response_text = f"Fata AI: Na karɓi saƙonku '[{query.prompt}]'. Ina amsa kowace tambaya ta duniya cikin sakan 1."
    return {"status": "success", "response": response_text}

if __name__ == "__main__":
    print("🚀 Fata AI Engine is Running on Port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# Adana Server File (fata_core.py)
with open("fata_core.py", "w", encoding="utf-8") as f:
    f.write(fata_server_code.strip())

print("\n[✔] SUCCESS: An haɗa duk fayilolin Fata AI a cikin folder!")
print("[👉] Kawai rubuta: 'python fata_core.py' domin tada Fata AI Server.")