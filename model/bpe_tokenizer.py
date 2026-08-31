import json
from collections import defaultdict

class FataBPETokenizer:
    def __init__(self, vocab_size=1000):
        self.vocab_size = vocab_size
        self.encoder = {}
        self.decoder = {}

    def train(self, texts):
        # Shirya corpus
        words = []
        for text in texts:
            for word in text.split():
                words.append(" ".join(list(word)) + " </w>")
        
        vocab = defaultdict(int)
        for word in words:
            vocab[word] += 1

        # Gina subwords
        for i in range(self.vocab_size):
            pairs = defaultdict(int)
            for word, freq in vocab.items():
                symbols = word.split()
                for j in range(len(symbols) - 1):
                    pairs[symbols[j], symbols[j+1]] += freq
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_vocab = {}
            bigram = " ".join(best)
            replacement = "".join(best)
            for word in vocab:
                w_out = word.replace(bigram, replacement)
                new_vocab[w_out] = vocab[word]
            vocab = new_vocab

        # Gina mapping
        unique_tokens = set()
        for word in vocab.keys():
            unique_tokens.update(word.split())
        
        self.encoder = {token: idx for idx, token in enumerate(["<pad>", "<unk>"] + list(unique_tokens))}
        self.decoder = {idx: token for token, idx in self.encoder.items()}

    def encode(self, text):
        tokens = text.split()
        ids = []
        for t in tokens:
            ids.append(self.encoder.get(t, self.encoder.get("<unk>")))
        return ids

    def decode(self, ids):
        return " ".join([self.decoder.get(i, "<unk>") for i in ids]).replace("</w>", "")

