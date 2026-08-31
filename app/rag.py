import time

class SimpleRAGMemory:
    def __init__(self):
        self.memory = {}

    def get_cached_result(self, query: str):
        query_key = query.lower().strip()
        if query_key in self.memory:
            item = self.memory[query_key]
            # Yin amfani da cache idan bai kai minti 15 ba (seconds 900)
            if time.time() - item['timestamp'] < 900:
                return item['data']
        return None

    def store_result(self, query: str, data: str):
        query_key = query.lower().strip()
        self.memory[query_key] = {
            'data': data,
            'timestamp': time.time()
        }

rag_memory = SimpleRAGMemory()