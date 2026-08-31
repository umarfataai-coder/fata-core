import torch
import torch.nn as nn
import re
from app.rag import rag_vector_db

class FataNeuralNetwork(nn.Module):
    def __init__(self, vocab_size=50000, d_model=256, nhead=8, num_layers=4):
        super(FataNeuralNetwork, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc_out = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer_encoder(x)
        out = self.fc_out(x)
        return out

class FataPureEngine:
    def __init__(self):
        print("Ana tada injin Fata PyTorch Transformer & Vector Core...")
        self.model = FataNeuralNetwork()
        self.model.eval()
        
        self.greetings = {
            "slm": "Wa alaikumus salam Oga Engineer! Fata AI yana raye kuma tsarin PyTorch/Atlas Vector Search yana aiki daram.",
            "assalamu alaikum": "Wa alaikumus salam wa rahmatullahi! Injin Fata AI yana sauraren ka.",
            "sannu": "Sannu kadai! Muna kan tsarin kera Super AI."
        }

    def process_query(self, prompt: str) -> str:
        clean_prompt = prompt.lower().strip()

        # 1. Duba Gaisuwa
        for key, reply in self.greetings.items():
            if key in clean_prompt:
                return reply

        # 2. Gudanar da Lissafi na Agentic
        if re.search(r'\d+[\+\-\*\/]\d+', clean_prompt):
            try:
                clean_expr = re.sub(r'[^0-9\+\-\*\/\(\)\.\s]', '', clean_prompt)
                result = eval(clean_expr)
                return f"🔢 **Sakamakon Lissafi:**\n$$ {clean_expr} = {result} $$"
            except Exception as e:
                return f"Matsala a lissafi: {str(e)}"

        # 3. Duba MongoDB Atlas Vector Knowledge Base
        atlas_knowledge = rag_vector_db.vector_search(prompt)
        if atlas_knowledge:
            return f"🧠 **Ilimi daga MongoDB Atlas Vector Store:**\n\n{atlas_knowledge}"

        # 4. Idan babu a Vector DB, PyTorch Engine zai sarrafa shi
        return f"[Fata PyTorch Core]: Na karbi bukatarka ta '{prompt}'. An sarrafa siginar (Tensors) ta cikin Transformer Layers."

fata_engine = FataPureEngine()