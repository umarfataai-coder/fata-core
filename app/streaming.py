import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import redis.asyncio as aioredis

app = FastAPI()
redis_client = aioredis.Redis(host="localhost", port=6379, decode_responses=True)

async def fata_token_generator(session_id: str, prompt: str):
    """Tura sakon Fata AI harafi-harafi ta amfani da Server-Sent Events (SSE)"""
    
    # Misalin sarrafa amsa daga enjin Fata AI
    tokens = ["Fata ", "AI ", "tana ", "aiki ", "cikin ", "sauri ", "da ", "kaifi ", "a ", "duniya!"]
    
    for token in tokens:
        await asyncio.sleep(0.05) # Hanzarta fitar sakonsu cikin milisecond 50
        
        # Tura Token zuwa Redis Pub/Sub Channel don sauran sabobi su sani
        payload = json.dumps({"session_id": session_id, "token": token})
        await redis_client.publish(f"channel:{session_id}", payload)
        
        # Fitar da sakon ta gidan yanar gizo
        yield f"data: {payload}\n\n"
        
    yield "data: [DONE]\n\n"

@app.get("/v1/chat/stream")
async def chat_stream(session_id: str, prompt: str):
    return StreamingResponse(
        fata_token_generator(session_id, prompt), 
        media_type="text/event-stream"
    )