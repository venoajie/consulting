# app\api\v1\endpoints\query.py

from fastapi import APIRouter, Body, Depends
from app.schemas.query import QueryRequest, QueryResponse
from app.services.llm import ResponseHandler, get_response_handler
from app.api.v1.dependencies import get_api_key

router = APIRouter()

@router.post(
    "/query",
    dependencies=[Depends(get_api_key)] # Apply security dependency here
)
async def process_query(
    request: QueryRequest = Body(...),
    handler: ResponseHandler = Depends(get_response_handler)
) -> QueryResponse:
    answer = await handler.call_api(question=request.question, model=request.model)
    return QueryResponse(answer=answer, sources=[])