from fastapi import FastAPI
from pydantic import BaseModel
from app.model_engine import fata_engine

app = FastAPI(title="Fata AI - Super Autonomous Agent")

class GenerateRequest(BaseModel):
    prompt: str
    language: str = "auto"

@app.get("/")
def read_root():
    return {"status": "Fata AI Engine Active (PyTorch, Atlas Vector & Code Agent)"}

@app.post("/generate")
def generate(req: GenerateRequest):
    user_prompt = req.prompt.strip()
    response_text = fata_engine.process_query(user_prompt)

    return {
        "prompt": req.prompt,
        "response": response_text
    }