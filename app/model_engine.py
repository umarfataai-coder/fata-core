import torch
import torch.nn as nn
import time
from app.custom_tokenizer import fata_tokenizer

class FataTransformerCore(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, num_heads=4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)
        self.fc_out = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        embedded = self.embedding(x)
        attn_out, _ = self.attention(embedded, embedded, embedded)
        return self.fc_out(attn_out)

class FataEngine:
    def __init__(self):
        self.vocab_size = max(fata_tokenizer.vocab_size, 1000)
        self.model = FataTransformerCore(vocab_size=self.vocab_size)
        self.model.eval()
        self.history = [] # Memori na tattaunawa

    def process_query_stream(self, prompt: str):
        # Ajiye maganar mai amfani a tarihi
        self.history.append({"user": prompt})
        
        # Injin gina amsa mai wayo (Natural Response Logic)
        p_lower = prompt.lower().strip()
        
        if any(w in p_lower for w on ["yaya", "ya kake", "ina kwana", "barka"]):
            response_text = "Lafiya lau nake! Ni ne Fata AI. Yaya aikinki/aikinka yake tafiya yau? Me kake son mu gina ko mu tattauna a kai?"
        elif any(w in p_lower for w on ["waye kai", "menene fata", "who are you"]):
            response_text = "Ni ne Fata AI, wani samfurin fasahar AI mai zaman kansa wanda Umar ya kera ta amfani da PyTorch Neural Networks. Ina iya sarrafa rubutu, lambobin kwamfuta, da binciken yanar gizo."
        elif any(w in p_lower for w on ["slm", "salam", "assalamu"]):
            response_text = "Amin Wa Alaikumus Salam Wrahmatullah! Barka da zuwa cibiyar Fata AI. Ta yaya zan taimake ka yanzu?"
        else:
            response_text = f"Na fahimci tambayarki/tambayarka akan '{prompt}'. Injin PyTorch yana tsara binciken wannan bayani ta hanyar amfani da hanyoyin fahimta na gida."

        self.history.append({"fata_ai": response_text})

        for word in response_text.split():
            yield f"data: {word}\n\n"
            time.sleep(0.06)

fata_engine = FataEngine()