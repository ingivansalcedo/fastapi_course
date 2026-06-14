from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import DATABASE_URL, get_db

# ==================== ENDPOINTS TEST ====================

api_router = APIRouter()


@api_router.get("/health")
async def health_check():
    return {"status": "ok", "database_url": DATABASE_URL}


@api_router.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    