import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import re
from fastapi import FastAPI
from pydantic import BaseModel
from app.model_engine import fata_brain
from app.rag import rag_memory

app = FastAPI(title="Fata AI - Super Autonomous Agent")

class GenerateRequest(BaseModel):
    prompt: str
    language: str = "auto"

def clean_search_query(prompt: str) -> str:
    p = prompt.lower()
    stop_words = ["binciko min", "binciko", "bincike", "nemo min", "nemo", "sabbin", "labaran", "labarai"]
    for word in stop_words:
        p = p.replace(word, "").strip()
    return f"{p} news" if p else "Nigeria news"

def perform_live_search(user_prompt: str):
    cached = rag_memory.get_cached_result(user_prompt)
    if cached:
        return cached

    search_keyword = clean_search_query(user_prompt)
    encoded_query = urllib.parse.quote(search_keyword)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-NG&gl=NG&ceid=NG:en"
    
    try:
        req = urllib.request.Request(
            rss_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        results = []
        
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text if item.find('title') is not None else ''
            source = item.find('source').text if item.find('source') is not None else 'News'
            if title:
                results.append(f"• [{source}] {title}")

        if results:
            final_data = "\n".join(results)
            rag_memory.store_result(user_prompt, final_data)
            return final_data
            
        return "Babu sakamakon bincike da aka samu a halin yanzu."

    except Exception as err:
        return f"Kuskure lokacin bincike: {str(err)}"

def route_intent(prompt: str):
    p = prompt.lower()
    # Duba ko lissafi ne
    if re.search(r'\d+[\+\-\*\/]\d+', p) or any(k in p for k in ["lissafi", "calculate", "solve"]):
        return "MATH_SOLVER"
    elif any(k in p for k in ["binciko", "bincike", "search", "labarai", "who is", "what is"]):
        return "WEB_SEARCH"
    elif any(k in p for k in ["code", "script", "python", "html", "fastapi", "gina app"]):
        return "CODE_GEN"
    else:
        return "GENERAL_REASONING"

@app.get("/")
def read_root():
    return {"status": "Fata AI Super Core Online"}

@app.post("/generate")
def generate(req: GenerateRequest):
    user_prompt = req.prompt.strip()
    intent = route_intent(user_prompt)
    
    if intent == "MATH_SOLVER":
        response_text = fata_brain.execute_math(user_prompt)
        
    elif intent == "WEB_SEARCH":
        raw_data = perform_live_search(user_prompt)
        response_text = fata_brain.process_general_reasoning(user_prompt, raw_data)
        
    elif intent == "CODE_GEN":
        response_text = fata_brain.generate_code_solution(user_prompt)
        
    else:
        response_text = fata_brain.process_general_reasoning(user_prompt)

    return {
        "prompt": req.prompt,
        "agent_assigned": intent,
        "response": response_text
    }