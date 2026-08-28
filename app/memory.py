import redis
class FataMemory:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
    def save_chat(self, user_id, user_msg, ai_response):
        self.client.rpush(f"chat:{user_id}", f"User: {user_msg}")
        self.client.rpush(f"chat:{user_id}", f"Fata: {ai_response}")
    def get_history(self, user_id):
        return self.client.lrange(f"chat:{user_id}", 0, -1)
