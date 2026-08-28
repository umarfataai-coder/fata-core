import time
import redis
from fastapi import Request

class FataTelemetry:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    def log_request_metrics(self, endpoint: str, latency_ms: float, status_code: int):
        """Adana bayanan saurin amsawa a cikin Redis Time-Series data"""
        timestamp = int(time.time())
        metric_key = f"metrics:{endpoint}:{timestamp}"
        
        pipeline = self.r.pipeline()
        pipeline.hset(metric_key, "latency", latency_ms)
        pipeline.hset(metric_key, "status", status_code)
        pipeline.expire(metric_key, 86400) # Rike bayanan na tsawon kwana 1
        pipeline.incr("total_global_requests")
        pipeline.execute()

    def get_global_stats(self):
        """Dauko jimillar amfani da Fata AI a duniya"""
        total_reqs = self.r.get("total_global_requests") or 0
        return {"total_requests_processed": int(total_reqs)}