from fastapi import FastAPI, HTTPException, Query, Request
from sqlmodel import Session, select
from models import Word
from database import engine, init_db
from config import cache
import time

app = FastAPI(title="Synonym Retrieval API with Caching")

@app.on_event("startup")
def on_startup():
    init_db()

# Initialize a simple in-memory stats object
app.state.request_times = []

@app.middleware("http")
async def track_latency(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000  # milliseconds
    app.state.request_times.append(duration_ms)
    print(f"[{request.url.path}] completed in {duration_ms:.2f} ms")
    return response


# ➕ Add a new word with optional synonyms
@app.post("/words/", response_model=Word)
def create_word(word: Word):
    with Session(engine) as session:
        existing = session.exec(select(Word).where(Word.word == word.word)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Word already exists.")
        session.add(word)
        session.commit()
        session.refresh(word)
        return word

# ➕ Add new synonyms to an existing word
@app.post("/words/{word_text}/synonyms/")
def add_synonyms(word_text: str, new_synonyms: list[str] = Query(...)):
    with Session(engine) as session:
        word = session.exec(select(Word).where(Word.word == word_text)).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found.")

        # Add only unique new synonyms
        for s in new_synonyms:
            if s not in word.synonyms:
                word.synonyms.append(s.lower())

        session.add(word)
        session.commit()
        session.refresh(word)

        # Invalidate or refresh cache
        cache_key = f"synonyms:{word_text.lower()}"
        cache.set(cache_key, word.synonyms)
        return {"word": word.word, "synonyms": word.synonyms, "updated": True}

# 🔍 Get all words
@app.get("/words/", response_model=list[Word])
def get_all_words():
    with Session(engine) as session:
        return session.exec(select(Word)).all()

# 🔍 Get synonyms (cached)
@app.get("/words/{word_text}/synonyms/")
def get_synonyms(word_text: str):
    cache_key = f"synonyms:{word_text.lower()}"
    cached = cache.get(cache_key)

    if cached:
        return {"word": word_text, "synonyms": cached, "cached": True}

    with Session(engine) as session:
        word = session.exec(select(Word).where(Word.word == word_text)).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found.")

        cache.set(cache_key, word.synonyms)
        return {"word": word.word, "synonyms": word.synonyms, "cached": False}
