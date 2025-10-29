import json
import redis
from .base import BaseCache

class RedisCache(BaseCache):
    def __init__(self, host="localhost", port=6379, db=0, default_ttl=300):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.default_ttl = default_ttl

    def get(self, key: str):
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value, ttl: int = None):
        serialized = json.dumps(value)
        self.client.setex(key, ttl or self.default_ttl, serialized)

    def delete(self, key: str):
        self.client.delete(key)

    def clear(self):
        self.client.flushdb()
