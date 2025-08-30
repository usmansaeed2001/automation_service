import os, json, hashlib
from fastapi import FastAPI, Request, HTTPException
from fastapi import APIRouter, HTTPException
from app.db.db_connection import db_manager

router = APIRouter()

@router.post("/webhooks/kajabi")
async def kajabi(payload: dict):
    dedupe_key = payload.get("id") or hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    # Use the shared database connection for idempotent insert
    try:
        db_manager.execute_insert(
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
