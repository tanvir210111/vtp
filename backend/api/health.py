"""
Health check API endpoint matching exact specification.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def health_check():
    return {
        "status": "ok",
        "version": "1.0.0"
    }
