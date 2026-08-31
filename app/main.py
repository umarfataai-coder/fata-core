from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from app.model_engine import fata_engine
from app.vision_engine import fata_vision
from app.code_agent import fata_code_agent
from app.vector_store import fata_memory

app = FastAPI(title="Fata AI - Autonomous Multimodal Architecture")

app.mount("/static", StaticFiles(directory="static"), name="static")

class CodeRequest(BaseModel):
    code: str

class MemoryRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/generate-stream")
def generate_stream(prompt: str):
    # Idan mai amfani ya nemi abu daga memory
    if "memory" in prompt.lower() or "tuna" in prompt.lower():
        mem_res = fata_memory.search_memory(prompt)
        def stream_memory():
            yield f"data: {mem_res} \n\n"
        return StreamingResponse(stream_memory(), media_type="text/event-stream")
    
    return StreamingResponse(fata_engine.process_query_stream(prompt), media_type="text/event-stream")

@app.post("/execute-code")
def execute_code(req: CodeRequest):
    result = fata_code_agent.execute_python(req.code)
    return {"code": req.code, "output": result}

@app.post("/add-memory")
def add_memory(req: MemoryRequest):
    res = fata_memory.add_memory(req.text)
    return {"status": res}

@app.get("/search-memory")
def search_memory(query: str):
    res = fata_memory.search_memory(query)
    return {"result": res}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    analysis_result = fata_vision.process_image(image_bytes)
    return {"filename": file.filename, "analysis": analysis_result}