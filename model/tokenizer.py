import re

class FataTokenizer:
    def __init__(self, vocab_size=5000):
        self.vocab_size = vocab_size
        self.encoder = {"<pad>": 0, "<unk>": 1, "<sos>": 2, "<eos>": 3}
        self.decoder = {idx: token for token, idx in self.encoder.items()}
        self.vocab = self.encoder

    def fit(self, texts):
        words = []
        for text in texts:
            words.extend(re.findall(r'\w+|\S', text.lower()))
        
        idx = len(self.encoder)
        for word in words:
            if word not in self.encoder and idx < self.vocab_size:
                self.encoder[word] = idx
                self.decoder[idx] = word
                idx += 1

    def encode(self, text):
        words = re.findall(r'\w+|\S', text.lower())
        return [self.encoder.get(w, self.encoder["<unk>"]) for w in words]

    def decode(self, ids):
        tokens = [self.decoder.get(i, "") for i in ids]
        return " ".join(tokens).replace(" <pad>", "").strip()