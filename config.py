import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# === CACHE SETTINGS ===
CACHE_BACKEND = os.getenv("CACHE_BACKEND", "memory")  # default to memory cache
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

# === DATABASE SETTINGS ===
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./synonyms.db")
USE_POOLING = os.getenv("USE_POOLING", "true").lower() == "true"

# === REDIS SETTINGS ===
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# === CONNECTION POOL SETTINGS ===
POOL_SIZE = int(os.getenv("POOL_SIZE", "5"))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "10"))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", "1800"))

# Choose cache backend dynamically
from cache.memory_cache import MemoryCache
from cache.redis_cache import RedisCache

if CACHE_BACKEND == "redis":
    cache = RedisCache(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        default_ttl=CACHE_TTL,
    )
else:
    cache = MemoryCache(default_ttl=CACHE_TTL)
