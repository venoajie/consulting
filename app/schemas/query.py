
from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    question: str

class Source(BaseModel):
    file_path: str
    content: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]