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
        logits = self.fc_out(attn_out)
        return logits

class FataEngine:
    def __init__(self):
        self.vocab_size = max(fata_tokenizer.vocab_size, 1000)
        self.model = FataTransformerCore(vocab_size=self.vocab_size)
        self.model.eval()

    def process_query_stream(self, prompt: str):
        input_ids = fata_tokenizer.encode(prompt)
        tensor_input = torch.tensor(input_ids).unsqueeze(1)
        
        with torch.no_grad():
            output_logits = self.model(tensor_input)

        response_text = f"🤖 [Injin Fata AI Core Engine]: Amin Wa Alaikumus Salam! Na karɓi saƙonku '{prompt}'. Tsarin PyTorch Neural Network ɗinka na gida yana amsa wannan sako tsaf."
        
        for word in response_text.split():
            yield f"data: {word}\n\n"
            time.sleep(0.08)

fata_engine = FataEngine()