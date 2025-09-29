from fastapi import APIRouter, Depends
from datetime import datetime
import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.get("/healthz")
async def healthz():
    """Liveness probe endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router.get("/readyz")
async def readyz():
    """Readiness probe endpoint"""
    # Add any readiness checks here (database connectivity, etc.)
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}
