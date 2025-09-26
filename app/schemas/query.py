# app\schemas\query.py
from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    model: Optional[str] = None

class Source(BaseModel):
    file_path: str
    content: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]