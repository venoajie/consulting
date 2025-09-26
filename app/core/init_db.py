# app\core\init_db.py
        
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from app.models.knowledge_document import Base

async def init_db(engine: AsyncEngine):
    """Initializes the database using the provided engine."""
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        await conn.run_sync(Base.metadata.create_all)