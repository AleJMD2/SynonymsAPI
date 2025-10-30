# Synonym Retrieval API

A high-performance **FastAPI** service for **bulk retrieval** of word synonyms.  
Each synonym record is cached **individually** (Redis or in-memory) with **configurable TTL** and a **metadata indicator** showing whether it came from cache.
## Tech Stack

- **FastAPI** – async web framework  
- **SQLModel** – ORM for structured word data  
- **Redis / CacheTools** – caching backends  
- **Python-Dotenv** – environment variable management  
- **Uvicorn** – ASGI server

## ⚙️ Environment Setup

Create a `.env` file in your project root:

# === APP CONFIG ===
APP_ENV=development

# === CACHING ===
CACHE_BACKEND=memory        # "redis" or "memory"
CACHE_TTL=300              # default TTL in seconds

# === DATABASE ===
USE_POOLING=false
DATABASE_URL=sqlite:///./synonyms.db

# === REDIS CONFIG ===
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# === OPTIONAL POOL SETTINGS ===
POOL_SIZE=5
MAX_OVERFLOW=10
POOL_TIMEOUT=30
POOL_RECYCLE=1800

🧰 Installation
# Clone repository
git clone https://github.com/<yourusername>/synonym-retrieval-api.git
cd synonym-retrieval-api

# Create virtual environment
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Running the API
uvicorn main:app --reload


Visit:

Docs: http://127.0.0.1:8000/docs

Metrics: http://127.0.0.1:8000/metrics/latency