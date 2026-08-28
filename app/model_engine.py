import torch
from model.transformer import FataEngineModel

class FataInferenceEngine:
    def __init__(self):
        # Saitunan Fata Model (Zamu iya haɓaka num_layers zuwa 32+ a lokacin production)
        self.vocab_size = 50257
        self.embed_dim = 768
        self.num_layers = 12
        self.num_heads = 12
        self.ff_dim = 3072
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = FataEngineModel(
            self.vocab_size, self.embed_dim, self.num_layers, self.num_heads, self.ff_dim
        ).to(self.device)
        
        self.model.eval() # Sanya samfurin a hanyar gudanarwa (evaluation mode)

    def generate(self, prompt_tokens: list, max_new_tokens: int = 50) -> list:
        input_ids = torch.tensor([prompt_tokens], dtype=torch.long).to(self.device)
        
        with torch.no_grad():
            for _ in range(max_new_tokens):
                logits = self.model(input_ids)
                next_token_logits = logits[:, -1, :]
                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
                input_ids = torch.cat([input_ids, next_token], dim=1)
                
        return input_ids.squeeze(0).tolist()