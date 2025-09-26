# app\api\v1\endpoints\query.py

from fastapi import APIRouter, Body, Depends
from app.schemas.query import QueryRequest, QueryResponse, Source
from app.services.llm import ResponseHandler, get_response_handler
from app.api.v1.dependencies import get_api_key

router = APIRouter()

@router.post(
    "/query",
    dependencies=[Depends(get_api_key)]
)
async def process_query(
    request: QueryRequest = Body(...),
    handler: ResponseHandler = Depends(get_response_handler)
) -> QueryResponse:
    answer, sources_data = await handler.call_api(question=request.question, model=request.model)
    
    # Adapt the sources data to the Pydantic model
    sources = [Source(file_path=s.get("source", "N/A"), content=s.get("content", "")) for s in sources_data]
    
    return QueryResponse(answer=answer, sources=sources)