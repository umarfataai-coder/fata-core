from fastapi import FastAPI

app = FastAPI(title="Fata AI Global Engine")

@app.get("/")
def home():
    return {"status": "Fata AI Online", "architecture": "Multi-Head Transformer"}

@app.post("/chat")
def chat(user_id: str, prompt: str):
    response = f"Fata AI Global Engine Response to: {prompt}"
    return {"response": response}
