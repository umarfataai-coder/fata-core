from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from app.model_engine import fata_engine
from app.vision_engine import fata_vision

app = FastAPI(title="Fata AI - Multimodal Autonomous Agent")

class GenerateRequest(BaseModel):
    prompt: str
    language: str = "auto"

@app.get("/")
def read_root():
    return {"status": "Fata AI Engine Active (PyTorch, Atlas Vector, Code Agent & Multimodal Vision)"}

@app.post("/generate")
def generate(req: GenerateRequest):
    user_prompt = req.prompt.strip()
    response_text = fata_engine.process_query(user_prompt)
    return {
        "prompt": req.prompt,
        "response": response_text
    }

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    analysis_result = fata_vision.process_image(image_bytes)
    return {
        "filename": file.filename,
        "analysis": analysis_result
    }