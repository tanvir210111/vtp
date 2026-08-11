"""
Download API router.
"""
from fastapi import APIRouter, Query
from services.download_service import DownloadService

router = APIRouter(prefix="/download", tags=["Download"])

@router.get("/{task_id}")
def download_export(task_id: str, format: str = Query("markdown")):
    return DownloadService.get_export_file(task_id, format)
