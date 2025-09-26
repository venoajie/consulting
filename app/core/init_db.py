# app\core\init_db.py
from sqlalchemy import text
from app.core.db import engine
from app.models.knowledge_document import Base

async def init_db():
    """
    Initializes the database by creating the vector extension and all tables.
    This is called on application startup.
    """
    async with engine.begin() as conn:
        # Check if the vector extension is installed and install it if not
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        
        # Create all tables defined by our ORM models
        await conn.run_sync(Base.metadata.create_all)