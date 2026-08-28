import re
class FataTokenizer:
    def __init__(self):
        self.vocab = {}
    def encode(self, text):
        return [ord(c) for c in text]
    def decode(self, tokens):
        return "".join([chr(t) for t in tokens])
