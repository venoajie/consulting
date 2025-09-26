# app\core\db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create an asynchronous engine
engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True, # Checks connection vitality before use
)

# Create a session factory
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False, # Allows objects to be used after commit
)

async def get_db_session() -> AsyncSession:
    """FastAPI dependency to get a database session."""
    async with AsyncSessionFactory() as session:
        yield session

async def close_db_connection():
    """Application shutdown event handler to dispose of the engine."""
    await engine.dispose()