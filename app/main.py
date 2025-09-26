# app\main.py

import asyncio
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.services.llm import close_llm_service
from app.core.db import close_db_connection
from app.core.init_db import init_db

app = FastAPI(title=settings.APP_NAME)

# Register startup and shutdown event handlers
@app.on_event("startup")
async def on_startup():
    # Run DB initialization
    await init_db()

app.add_event_handler("shutdown", close_llm_service)
app.add_event_handler("shutdown", close_db_connection)


app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}. API is at {settings.API_V1_STR}"}