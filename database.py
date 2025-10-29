from sqlmodel import SQLModel, create_engine
from config import (
    DATABASE_URL,
    USE_POOLING,
    POOL_SIZE,
    MAX_OVERFLOW,
    POOL_TIMEOUT,
    POOL_RECYCLE,
)

def create_db_engine():
    if USE_POOLING:
        print("Using connection pooling")
        return create_engine(
            DATABASE_URL,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_timeout=POOL_TIMEOUT,
            pool_recycle=POOL_RECYCLE,
            pool_pre_ping=True,
            echo=False,
        )
    else:
        print("Pooling disabled — using default connection behavior")
        return create_engine(
            DATABASE_URL,
            poolclass=None,   # disables SQLAlchemy pooling
            echo=False,
        )

engine = create_db_engine()

def init_db():
    SQLModel.metadata.create_all(engine)
