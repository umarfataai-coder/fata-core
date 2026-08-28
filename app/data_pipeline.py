import redis
import torch
from torch.utils.data import Dataset, DataLoader

class FataDataStreamer:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    def push_text_chunk(self, stream_name: str, text_chunk: str):
        """Tura sabbin nassoshi zuwa Redis Stream don koyo"""
        self.r.xadd(stream_name, {"text": text_chunk})

    def fetch_batch(self, stream_name: str, count: int = 100):
        """Dauko nassoshi cikin sauri don ciyar da GPU"""
        entries = self.r.xread({stream_name: '0-0'}, count=count)
        data = []
        if entries:
            for stream, messages in entries:
                for msg_id, content in messages:
                    data.append(content['text'])
        return data


class FataDataset(Dataset):
    def __init__(self, tokenized_data: list, seq_len: int = 2048):
        self.data = torch.tensor(tokenized_data, dtype=torch.long)
        self.seq_len = seq_len

    def __len__(self):
        return len(self.data) // self.seq_len

    def __getitem__(self, idx):
        start_idx = idx * self.seq_len
        end_idx = start_idx + self.seq_len
        
        # input_ids (x) da target_ids (y) don hasashen kalma ta gaba (Next Token Prediction)
        x = self.data[start_idx:end_idx]
        y = self.data[start_idx + 1:end_idx + 1]
        return x, y