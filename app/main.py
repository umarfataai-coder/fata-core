from fastapi import FastAPI
from app.memory import FataMemory
app = FastAPI(title="Fata AI Global Engine")
memory = FataMemory()
@app.get("/"):
def home():
    return {"status": "Fata AI Online", "architecture": "Multi-Head Transformer"}
@app.post("/chat"):
def chat(user_id: str, prompt: str):
    response = f"Fata AI Global Engine Response to: {prompt}"
    memory.save_chat(user_id, prompt, response)
    return {"response": response, "history": memory.get_history(user_id)}
