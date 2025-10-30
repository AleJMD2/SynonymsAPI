from fastapi import FastAPI, HTTPException, Request
from sqlmodel import Session, select
from models import Word
from database import engine, init_db
from config import cache
import time

app = FastAPI(title="Synonym Retrieval API (Per-Record + Bulk Caching)")

# === Initialization ===
@app.on_event("startup")
def on_startup():
    init_db()
    print("✅ Database initialized")


# === Latency Tracking Middleware ===
app.state.request_times = []

@app.middleware("http")
async def track_latency(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000  # milliseconds
    app.state.request_times.append(duration_ms)
    print(f"[{request.url.path}] completed in {duration_ms:.2f} ms")
    return response


# === Bulk Retrieval with Per-Record Caching ===
@app.get("/words/")
def get_all_words():
    """
    Retrieve all synonym records.
    Each record is cached individually and includes a metadata flag.
    """
    with Session(engine) as session:
        words = session.exec(select(Word)).all()

    results = []
    for w in words:
        cache_key = f"word:{w.word.lower()}"
        cached = cache.get(cache_key)

        if cached:
            record = cached.copy()
            record["cached"] = True
        else:
            record = {"id": w.id, "word": w.word, "synonyms": w.synonyms, "cached": False}
            # Store record individually for future requests
            cache.set(cache_key, {"id": w.id, "word": w.word, "synonyms": w.synonyms})

        results.append(record)

    return results


# === Get a Specific Word (Cached) ===
@app.get("/words/{word_text}")
def get_word(word_text: str):
    """
    Retrieve a specific word and its synonyms.
    Uses cache for fast access with metadata flag.
    """
    cache_key = f"word:{word_text.lower()}"
    cached_record = cache.get(cache_key)

    if cached_record:
        return {**cached_record, "cached": True}

    with Session(engine) as session:
        word = session.exec(select(Word).where(Word.word == word_text)).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        record = {"id": word.id, "word": word.word, "synonyms": word.synonyms, "cached": False}
        # Cache for future requests
        cache.set(cache_key, {"id": word.id, "word": word.word, "synonyms": word.synonyms})

        return record



