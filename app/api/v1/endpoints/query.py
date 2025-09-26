# app\api\v1\endpoints\query.py

from fastapi import APIRouter, Body, Depends
from app.schemas.query import QueryRequest, QueryResponse
from app.services.llm import LLMService, get_llm_service

router = APIRouter()

@router.post("/query")
async def process_query(
    request: QueryRequest = Body(...),
    llm_service: LLMService = Depends(get_llm_service)
) -> QueryResponse:
    """
    Receives a user query, processes it through the RAG pipeline,
    and returns a context-aware answer.
    """
    answer = await llm_service.generate_answer(question=request.question)

    return QueryResponse(answer=answer, sources=[])