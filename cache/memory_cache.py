from cachetools import TTLCache
from threading import Lock
from .base import BaseCache
import json

class MemoryCache(BaseCache):
    def __init__(self, maxsize=1000, default_ttl=300):
        self.cache = TTLCache(maxsize=maxsize, ttl=default_ttl)
        self.lock = Lock()

    def get(self, key: str):
        with self.lock:
            value = self.cache.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value, ttl: int = None):
        serialized = json.dumps(value)
        with self.lock:
            self.cache[key] = serialized

    def delete(self, key: str):
        with self.lock:
            self.cache.pop(key, None)

    def clear(self):
        with self.lock:
            self.cache.clear()
