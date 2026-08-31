from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from app.model_engine import fata_engine
from app.vision_engine import fata_vision
from app.code_agent import fata_code_agent

app = FastAPI(title="Fata AI - Multimodal Autonomous Agent")

app.mount("/static", StaticFiles(directory="static"), name="static")

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/generate-stream")
def generate_stream(prompt: str):
    return StreamingResponse(fata_engine.process_query_stream(prompt), media_type="text/event-stream")

@app.post("/execute-code")
def execute_code(req: CodeRequest):
    result = fata_code_agent.execute_python(req.code)
    return {"code": req.code, "output": result}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    analysis_result = fata_vision.process_image(image_bytes)
    return {"filename": file.filename, "analysis": analysis_result}