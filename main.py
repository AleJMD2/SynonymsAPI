from fastapi import FastAPI, Request
from sqlmodel import Session, select
from models import Word
from database import engine, init_db
from config import cache
import time

app = FastAPI(title="Synonym Retrieval API (Read-Only with Per-Record Caching)")

# === Initialization ===
@app.on_event("startup")
def on_startup():
    init_db()


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
    The system supports only full-table retrieval (no single record lookups).
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


