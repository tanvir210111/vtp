"""
Upload API router.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from typing import Optional
from sqlalchemy.orm import Session
from database.database import get_db
from services.upload_service import UploadService

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def upload_video(
    video: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    upload_file = video or file
    if not upload_file:
        raise HTTPException(status_code=400, detail="No video file provided in payload.")

    try:
        return await UploadService.save_uploaded_file(upload_file, db)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
