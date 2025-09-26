# app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import query, health

api_router = APIRouter()
api_router.include_router(query.router, prefix="/rag", tags=["RAG"])
api_router.include_router(health.router, prefix="/system", tags=["System"])