from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.model_engine import fata_engine
from app.vision_engine import fata_vision
from app.cache import fata_cache

app = FastAPI(title="Fata AI - Multimodal Autonomous Agent")

app.mount("/static", StaticFiles(directory="static"), name="static")

class GenerateRequest(BaseModel):
    prompt: str
    language: str = "auto"

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/generate")
def generate(req: GenerateRequest):
    user_prompt = req.prompt.strip()
    
    # 1. Duba ko amsar tana cikin Redis Cache
    cached_res = fata_cache.get_cached_response(user_prompt)
    if cached_res:
        return {
            "prompt": req.prompt,
            "response": f"[⚡ Fast Redis Cache Response]:\n{cached_res}"
        }

    # 2. Idan babu a cache, a sarrafa shi ta PyTorch Engine
    response_text = fata_engine.process_query(user_prompt)
    
    # 3. Adana amsar a Redis Cache don gaba
    fata_cache.set_cached_response(user_prompt, response_text)
    
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