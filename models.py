from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from sqlalchemy.ext.mutable import MutableList 

class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str = Field(index=True, unique=True)
    synonyms: List[str] = Field(
        default_factory=list,
        sa_column=Column(MutableList.as_mutable(JSON))  # Track changes
    )
