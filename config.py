import os

class Config:
    PROJECT_NAME = "Fata AI Global"
    VERSION = "1.0.0-PROD"
    
    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
    # Security & Performance
    MAX_TOKENS_PER_REQUEST = 4096
    RATE_LIMIT_PER_MINUTE = 60 # Maximum 60 requests per minute per IP