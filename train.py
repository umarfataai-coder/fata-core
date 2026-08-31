import torch
import torch.nn as nn
import torch.optim as optim
from app.model_engine import FataNeuralNetwork

def train_fata_brain():
    print("🚀 Ana Fara Horar da Kwakwalwar Fata AI (Training Phase)...")
    
    # 1. Saita Model da Parameters
    vocab_size = 50000
    model = FataNeuralNetwork(vocab_size=vocab_size)
    model.train()  # Saita a yanayin Horarwa (Training Mode)

    # 2. Optimization da Loss Function (Kamar Gemini Engine)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.001)

    # 3. Kwatancin Bayanan Horarwa (Dummy Dataset Tensors)
    # A nan za a rika ciyar da Model din da ainihin data daga MongoDB Atlas
    dummy_input = torch.randint(0, vocab_size, (4, 32))  # Batch size 4, Sequence length 32
    target_labels = torch.randint(0, vocab_size, (4, 32))

    # 4. Training Loop (Epochs)
    epochs = 5
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # Forward pass (Tunanin Model)
        output = model(dummy_input)
        
        # Reshape output don lissafin kuskure (Loss)
        loss = criterion(output.view(-1, vocab_size), target_labels.view(-1))
        
        # Backward pass (Gyaran Kuskure)
        loss.backward()
        optimizer.step()

        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

    # 5. Adana Checkpoint na Kwakwalwar Fata AI
    checkpoint_path = "fata_checkpoint.pt"
    torch.save(model.state_dict(), checkpoint_path)
    print(f"✅ An gama horarwa! An adana sabuwar kwakwalwa a: {checkpoint_path}")

if __name__ == "__main__":
    train_fata_brain()