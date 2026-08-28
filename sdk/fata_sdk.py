import requests
import json
from typing import Generator

class FataClient:
    def __init__(self, api_key: str, base_url: str = "https://api.fata.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, session_id: str, prompt: str) -> dict:
        """Aika tambaya zuwa Fata AI kuma karbi cikakkiyar amsa"""
        endpoint = f"{self.base_url}/chat"
        payload = {"session_id": session_id, "prompt": prompt}
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"[Fata SDK Error]: {response.status_code} - {response.text}")

    def chat_stream(self, session_id: str, prompt: str) -> Generator[str, None, None]:
        """Karbi amsar Fata AI ta hanyar streaming harafi-harafi"""
        endpoint = f"{self.base_url}/chat/stream?session_id={session_id}&prompt={prompt}"
        
        with requests.get(endpoint, headers=self.headers, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        data_content = decoded[6:]
                        if data_content == "[DONE]":
                            break
                        token_data = json.loads(data_content)
                        yield token_data.get("token", "")