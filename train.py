import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from model.tokenizer import FataTokenizer
from model.transformer import FataTransformer

# 1. Faɗada Rukunin Bayanai (Multi-Domain Dataset)
dataset_text = [
    # Hausa Knowledge
    "fata ai kwararre ne akan ilimi da fasaha a duniya",
    "barka da zuwa babban tsarin fata ai mai karfi",
    "fata ai yana amsa tambayoyi cikin sauri da kaifi",
    "mu ne gina fasaha mafi karfi a duniya baki daya",
    "fasahar kwamfuta tana taimakawa wajen haɓaka ilimi",
    "fata ai yana iya rubuta lambobin kwamfuta da gyara kuskure",
    
    # English & Coding Knowledge
    "fata ai is the most powerful artificial intelligence in the world",
    "python is a high level programming language used for ai development",
    "fastapi provides fast web frameworks for building high performance apis",
    "pytorch is built for deep learning and neural network training",
    "fata ai can solve complex science logic and algorithm problems"
]

# 2. Shirya Tokenizer & Data Loader
tokenizer = FataTokenizer(vocab_size=10000)
tokenizer.fit(dataset_text)
vocab_size = len(tokenizer.vocab)
print(f"[+] Girman Vocab: {vocab_size}")

class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_len=32):
        self.data = []
        for text in texts:
            encoded = tokenizer.encode(text)
            if len(encoded) > 1:
                self.data.append(torch.tensor(encoded, dtype=torch.long))
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        tensor = self.data[idx]
        x = tensor[:-1]
        y = tensor[1:]
        return x, y

def collate_fn(batch):
    x_list, y_list = zip(*batch)
    x_padded = torch.nn.utils.rnn.pad_sequence(x_list, batch_first=True, padding_value=0)
    y_padded = torch.nn.utils.rnn.pad_sequence(y_list, batch_first=True, padding_value=0)
    return x_padded, y_padded

train_dataset = TextDataset(dataset_text, tokenizer)
dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True, collate_fn=collate_fn)

# 3. Model & Optimization
model = FataTransformer(vocab_size=vocab_size, d_model=256, nhead=8, num_layers=4)
criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.AdamW(model.parameters(), lr=0.0005)

# 4. Horar da Samfurin (Training Loop)
epochs = 200
print("[*] Fara horar da Fata AI...")

for epoch in range(1, epochs + 1):
    total_loss = 0
    model.train()
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        output = model(batch_x)
        
        loss = criterion(output.view(-1, vocab_size), batch_y.view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    if epoch % 50 == 0 or epoch == 1:
        print(f"Epoch {epoch}/{epochs} - Loss: {total_loss/len(dataloader):.4f}")

# 5. Adana Checkpoint
torch.save(model.state_dict(), "fata_checkpoint.pt")
print("[+] An adana sabon horarwa a 'fata_checkpoint.pt' cikin nasara!")