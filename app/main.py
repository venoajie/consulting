# app\main.py

import uvloop
uvloop.install()

import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.init_db import init_db

logging.basicConfig(
    level=settings.app.service.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for the application."""
    logger.info(f"Starting Tax Co-Pilot Service v{settings.app.service.version}")
    
    # Create and test DB connection pool
    try:
        logger.info("Creating PostgreSQL connection pool...")
        app.state.db_engine = create_async_engine(
            str(settings.app.database.url),
            pool_pre_ping=True
        )
        async with app.state.db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
        
        # Initialize database schema
        await init_db(app.state.db_engine)

    except Exception as e:
        logger.critical(f"FATAL: Could not connect to PostgreSQL: {e}", exc_info=True)
        sys.exit(1)

    logger.info("Application startup complete.")
    yield
    
    logger.info("Shutting down service.")
    if app.state.db_engine:
        await app.state.db_engine.dispose()
    logger.info("Shutdown complete.")

app = FastAPI(
    title="Tax Co-Pilot RAG Service",
    version=settings.app.service.version,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Tax Co-Pilot Service. See /docs for details."}