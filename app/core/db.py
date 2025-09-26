# app\core\db.py
    
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Request

# The engine is now created and managed in main.py's lifespan
# This file now only provides the session dependency

async def get_db_session(request: Request) -> AsyncSession:
    """FastAPI dependency to get a database session from the connection pool."""
    engine = request.app.state.db_engine
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session