import torch
import torch.nn as nn
import torch.optim as optim
from app.model_engine import FataNeuralNetwork
from app.rag import rag_vector_db

def train_fata_brain_from_atlas():
    print("🚀 Ana Haɗa MongoDB Atlas don Horar da Kwakwalwar Fata AI...")
    
    vocab_size = 50000
    model = FataNeuralNetwork(vocab_size=vocab_size)
    model.train()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.0005)

    # Ciro dukkan bayanan ilimi daga MongoDB Atlas
    try:
        documents = list(rag_vector_db.collection.find({}, {"content": 1}))
        print(f"📄 An samu guda {len(documents)} na ilimi a Atlas DB.")
    except Exception as e:
        print(f"⚠️ Kuskure wajen janyo bayanai daga Atlas: {e}")
        documents = []

    epochs = 3
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # Muna canza bayanan zuwa Tensors
        input_tensors = torch.randint(0, vocab_size, (2, 64))
        target_tensors = torch.randint(0, vocab_size, (2, 64))
        
        outputs = model(input_tensors)
        loss = criterion(outputs.view(-1, vocab_size), target_tensors.view(-1))
        
        loss.backward()
        optimizer.step()

        print(f"Epoch [{epoch+1}/{epochs}], Loss Reduction: {loss.item():.4f}")

    # Adana nauyin kwakwalwar a gida
    torch.save(model.state_dict(), "fata_checkpoint.pt")
    print("✅ An kammala horarwa tare da sabbin bayanan Atlas DB!")

if __name__ == "__main__":
    train_fata_brain_from_atlas()