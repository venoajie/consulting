# app\main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.services.llm import close_llm_service

app = FastAPI(title=settings.APP_NAME)

# Register the shutdown event handler
app.add_event_handler("shutdown", close_llm_service)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}. API is at {settings.API_V1_STR}"}