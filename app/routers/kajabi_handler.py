import os, json, hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi import APIRouter, HTTPException
from app.db.db_connection import get_db_manager, DatabaseManager

router = APIRouter()

def get_db() -> DatabaseManager:
    """Dependency to get database manager instance"""
    return get_db_manager()

@router.post("/webhooks/kajabi")
async def kajabi(payload: dict, db: DatabaseManager = Depends(get_db)):
    dedupe_key = payload.get("id") or hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    # Use the shared database connection for idempotent insert
    try:
        db.execute_insert(
            """
            INSERT INTO outbox(provider, dedupe_key, payload)
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (provider, dedupe_key) DO NOTHING
            """,
            ("kajabi", dedupe_key, json.dumps(payload)),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"ok": True}
