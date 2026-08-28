import re

class FataTokenizer:
    def __init__(self):
        self.vocab = {"[ PAD ]": 0, "[ UNK ]": 1, "[ BOS ]": 2, "[ EOS ]": 3}
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

    def fit(self, texts):
        idx = len(self.vocab)
        for text in texts:
            tokens = re.findall(r"\w+|[^\w\s]", text.lower())
            for token in tokens:
                if token not in self.vocab:
                    self.vocab[token] = idx
                    self.inverse_vocab[idx] = token
                    idx += 1

    def encode(self, textg):
        tokens = re.findall(r"\w+|[^\ws]", text.lower())
        return [self.vocab.get(token, self.vocab["[ UNK ]"]) for token in tokens]

    def decode(self, ids):
        return " ".join([self.inverse_vocab.get(i, "[ UNK ]") for i in ids])

