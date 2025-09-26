#   app/api/v1/endpoints/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.db import get_db_session

router = APIRouter()

@router.get("/health", status_code=200)
async def check_health(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Checks the health of the service, including the database connection.
    """
    try:
        # Run a simple query to check the database connection
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database_status": db_status
    }