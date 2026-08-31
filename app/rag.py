import pymongo
from sentence_transformers import SentenceTransformer

class AtlasVectorRAG:
    def __init__(self):
        # Model din sarrafa rubutu zuwa Vector Embeddings
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # MongoDB Atlas Connection
        self.mongo_uri = "mongodb+srv://USER:PASSWORD@cluster0.mongodb.net/fata_db?retryWrites=true&w=majority"
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
            self.db = self.client["fata_ai"]
            self.collection = self.db["knowledge_vectors"]
            print("MongoDB Atlas Vector Store: Ready.")
        except Exception as e:
            print(f"Atlas Connection Error: {e}")

    def generate_embedding(self, text: str):
        return self.embedder.encode(text).tolist()

    def store_knowledge(self, topic: str, content: str):
        """Adana sabon ilimi a matsayin Vector"""
        vector = self.generate_embedding(content)
        doc = {
            "topic": topic,
            "content": content,
            "content_vector": vector
        }
        self.collection.insert_one(doc)
        return "An adana ilimi a Vector DB."

    def vector_search(self, query: str):
        """Binciken ilimi ta hanyar Vector Similarity Search"""
        query_vector = self.generate_embedding(query)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "content_vector",
                    "queryVector": query_vector,
                    "numCandidates": 10,
                    "limit": 1
                }
            }
        ]
        try:
            results = list(self.collection.aggregate(pipeline))
            if results:
                return results[0]["content"]
        except Exception:
            pass
        return None

rag_vector_db = AtlasVectorRAG()