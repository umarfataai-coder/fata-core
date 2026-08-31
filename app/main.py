from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
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
    cached_res = fata_cache.get_cached_response(user_prompt)
    if cached_res:
        return {"prompt": req.prompt, "response": f"[⚡ Fast Redis Cache Response]:\n{cached_res}"}

    response_text = "".join([chunk.replace("data: ", "").replace(" \n\n", " ") for chunk in fata_engine.process_query_stream(user_prompt)])
    fata_cache.set_cached_response(user_prompt, response_text)
    return {"prompt": req.prompt, "response": response_text}

@app.get("/generate-stream")
def generate_stream(prompt: str):
    return StreamingResponse(fata_engine.process_query_stream(prompt), media_type="text/event-stream")

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    analysis_result = fata_vision.process_image(image_bytes)
    return {"filename": file.filename, "analysis": analysis_result}