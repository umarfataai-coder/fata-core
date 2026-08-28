import torch
import torch.nn as nn
from torch.cuda.amp import autocast, GradScaler
from model.transformer import FataEngineModel
from torch.utils.data import DataLoader

def train_fata_core():
    # 1. Saitunan Na'ura da Samfuri
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Fata Engine]: Ana amfani da na'ura mai karfi ta: {device}")

    # Saitunan Fata AI High-Performance Architecture
    vocab_size = 50257
    embed_dim = 2048
    num_layers = 24
    num_heads = 16
    ff_dim = 8192
    
    model = FataEngineModel(vocab_size, embed_dim, num_layers, num_heads, ff_dim).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
    scaler = GradScaler() # Don haɓaka saurin GPU ta AMP

    model.train()
    criterion = nn.CrossEntropyLoss()

    print("[Fata Engine]: An fara gudanar da Pre-training Loop...")

    # (Misalin gwajin horo na gaskiya - Dummy batch don tabbatar da tsari)
    dummy_input = torch.randint(0, vocab_size, (4, 512)).to(device)
    dummy_target = torch.randint(0, vocab_size, (4, 512)).to(device)

    optimizer.zero_grad()

    # Mixed Precision Forward Pass
    with autocast():
        logits = model(dummy_input)
        loss = criterion(logits.view(-1, vocab_size), dummy_target.view(-1))

    # Backward Pass tare da Scaler don gudun kuskure a lissafi
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

    print(f"[Fata Engine]: Sakamakon Horon Farko (Loss): {loss.item():.4f}")
    
    # Adana nauyin samfuri (Checkpointing)
    torch.save(model.state_dict(), "fata_model_checkpoint.pt")
    print("[Fata Engine]: An adana Model Checkpoint a 'fata_model_checkpoint.pt' successfully!")

if __name__ == "__main__":
    train_fata_core()