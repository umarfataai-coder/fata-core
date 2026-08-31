import torch
import torch.nn as nn
import re
from app.rag import db_manager

# Ainihin Kwakwalwar Fata AI (Transformer Block)
class FataNeuralNetwork(nn.Module):
    def __init__(self, vocab_size=50000, d_model=256, nhead=8, num_layers=4):
        super(FataNeuralNetwork, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        # Injin Transformer mai gane zurfin magana (kamar Gemini)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        self.fc_out = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        # Wannan shine inda Fata ke gudanar da tunani (Reasoning)
        x = self.embedding(x)
        x = self.transformer_encoder(x)
        out = self.fc_out(x)
        return out

class FataPureEngine:
    def __init__(self):
        print("Ana tada injin Fata PyTorch Transformer...")
        self.model = FataNeuralNetwork()
        self.model.eval() # Saita model ɗin a yanayin aiki
        
        self.greetings = {
            "slm": "Wa alaikumus salam Oga Engineer! Fata AI yana raye kuma tsarin PyTorch yana aiki.",
            "assalamu alaikum": "Wa alaikumus salam wa rahmatullahi! Injin Fata AI yana sauraron ka.",
            "sannu": "Sannu kadai! Muna kan tsarin kera Super AI."
        }

    def process_query(self, prompt: str) -> str:
        clean_prompt = prompt.lower().strip()

        # 1. Duba Redis Cache don amsa mai gaggawa (0.001s)
        cached_res = db_manager.get_quick_response(clean_prompt)
        if cached_res:
            return cached_res

        # 2. Gane gaisuwa nan take
        for key, reply in self.greetings.items():
            if key in clean_prompt:
                db_manager.store_quick_response(clean_prompt, reply)
                return reply

        # 3. Gudanar da Lissafi na Agentic
        if re.search(r'\d+[\+\-\*\/]\d+', clean_prompt):
            try:
                clean_expr = re.sub(r'[^0-9\+\-\*\/\(\)\.\s]', '', clean_prompt)
                result = eval(clean_expr)
                ans = f"🔢 **Sakamakon Lissafi:**\n$$ {clean_expr} = {result} $$"
                db_manager.store_quick_response(clean_prompt, ans)
                return ans
            except Exception as e:
                return f"Matsala a lissafi: {str(e)}"

        # 4. Aiki da PyTorch Model wajen sarrafa sabon tunani
        default_reply = f"[Fata PyTorch Core]: Na karbi bukatarka ta '{prompt}'. Siginar (Tensors) na ratsa cikin Transformer Layers don samo amsa daga MongoDB Atlas."
        db_manager.store_quick_response(clean_prompt, default_reply)
        return default_reply

fata_engine = FataPureEngine()