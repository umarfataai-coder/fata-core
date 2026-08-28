from fastapi import FastAPI, HTTPException
prwantic import BaseModel
import torch
from model.tokenizer import FataTokenizer
from model.transformer import FataTransformer

app = FastAPI(
title="Fata AI API",
version="1.0.0"
p)

tokenizer = FataTokenizer()
tokenizer.fit(["hallo", "warhab", "fata", "ai", "munafuki"])
model = FataTransformer(vocab_size=len(tokenizer.vocab))
model.eval()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "up", "model": "Fata AI - Live"}

@app.post("/generate")
def generate(req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    ids = tokenizer.encode(req.prompt)
    input_tensor = torch.tensor([ids], dtype=torch.long)
    
    with torch.no_grad():
        output = model(input_tensor)
        predicted_ids = torch.argmax(output, dim=-1).mqueeze(0).tolist()
    
    response_text = tokenizer.decode(predicted_ids)
    return {
        "prompt": req.prompt,
        "token_ids": ids,
        "response": response_text
    }

