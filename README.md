# Synonym Retrieval API

A high-performance **FastAPI** service for managing and retrieving word synonyms with **SQLModel** and multi-strategy caching (Redis + in-memory).  
Supports **configurable connection pooling**, **thread-safe cache operations**, and **automatic TTL expiration** for optimized performance.

---

## 🚀 Features

- 🔡 **CRUD operations** for words and synonyms  
- ⚡ **Multi-strategy caching** — Redis (distributed) or in-memory  
- ⏱ **Configurable TTL & auto-expiration** for cache entries  
- 🧵 **Thread-safe, atomic** cache operations  
- 🧩 **Optional connection pooling** for efficient DB access  
- 📊 **Built-in latency metrics** to measure cache performance  
- 🧠 Works with **SQLite**, **PostgreSQL**, or **SQL Server**

---

## 🛠 Tech Stack

- **FastAPI** — async web framework  
- **SQLModel / SQLAlchemy** — ORM + database layer  
- **Redis** — distributed caching backend  
- **CacheTools** — in-memory TTL cache  
- **Python-Dotenv** — environment variable management  
- **Uvicorn** — ASGI server  

---

## 📦 Project Structure

SynonymsAPI/
│
├── main.py
├── models.py
├── database.py
├── config.py
├── cache/
│ ├── init.py
│ ├── base.py
│ ├── memory_cache.py
│ └── redis_cache.py
├── requirements.txt
├── .env
└── .gitignore

---

## ⚙️ Environment Setup

Create a `.env` file in the project root:

```bash
# === APP CONFIG ===
APP_ENV=development
CACHE_BACKEND=redis        # "redis" or "memory"
CACHE_TTL=300              # default cache Time-To-Live (seconds)

# === DATABASE CONFIG ===
USE_POOLING=true
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
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


If using Redis:

docker run -d -p 6379:6379 redis

▶️ Running the API
uvicorn main:app --reload


Visit:

Docs: http://127.0.0.1:8000/docs

Alternate docs: http://127.0.0.1:8000/redoc

🧪 Example Usage
➕ Add a word

POST /words/

{
  "word": "happy",
  "synonyms": ["joyful", "content"]
}

➕ Add new synonyms

POST /words/happy/synonyms/?new_synonyms=cheerful&new_synonyms=glad

🔍 Retrieve synonyms (cached)

GET /words/happy/synonyms/

{
  "word": "happy",
  "synonyms": ["joyful", "content", "cheerful", "glad"],
  "cached": true
}


How Caching Works
Backend	Description	TTL Support	Thread Safe
MemoryCache	Local TTL cache (CacheTools)	✅	✅ (via Lock)
RedisCache	Distributed, persistent cache	✅ Native	✅ Atomic

You can switch between them via .env:

CACHE_BACKEND=memory


or

CACHE_BACKEND=redis

🧩 Optional Connection Pooling

Toggled via .env:

USE_POOLING=true   # enable pooling
USE_POOLING=false  # disable pooling


When enabled, SQLAlchemy manages a configurable connection pool:

POOL_SIZE=10
MAX_OVERFLOW=20

🧱 Database Support

This system supports any SQLModel-compatible database:

SQLite for development

PostgreSQL / MySQL / MSSQL for production

Just change DATABASE_URL in .env:

DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/synonyms

