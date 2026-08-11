"""
Upload service handling file persistence, 15s duration validation, and task registration.
"""
import os
import aiofiles
import cv2
from fastapi import HTTPException
from sqlalchemy.orm import Session
from config.settings import settings
from utils.file import sanitize_filename, ensure_dir
from utils.validator import validate_video_file
from utils.helpers import generate_task_id
from database.models import VideoTask

class UploadService:
    @staticmethod
    async def save_uploaded_file(file, db: Session) -> dict:
        filename = sanitize_filename(file.filename or "uploaded_video.mp4")
        
        # Read file contents & validate format & size
        contents = await file.read()
        file_size = len(contents)
        validate_video_file(filename, file_size)
        
        task_id = generate_task_id()
        task_upload_dir = ensure_dir(os.path.join(settings.STORAGE_DIR, "uploads", task_id))
        saved_file_path = os.path.join(task_upload_dir, filename)
        
        async with aiofiles.open(saved_file_path, "wb") as out_file:
            await out_file.write(contents)
            
        # Calculate video duration
        duration = 10.0
        try:
            cap = cv2.VideoCapture(saved_file_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
            if fps > 0 and frame_count > 0:
                duration = round(frame_count / fps, 1)
            cap.release()
        except Exception:
            duration = 10.0

        # Validate 15-second max duration limit
        if duration > 15.5:
            if os.path.exists(saved_file_path):
                os.remove(saved_file_path)
            raise HTTPException(
                status_code=400,
                detail=f"Video length ({duration:.1f}s) exceeds maximum allowed duration of 15 seconds."
            )

        # Create database record
        task_record = VideoTask(
            id=task_id,
            filename=filename,
            file_path=saved_file_path,
            file_size_bytes=file_size,
            duration_seconds=duration,
            status="uploaded"
        )
        db.add(task_record)
        db.commit()
        db.refresh(task_record)
        
        return {
            "success": True,
            "video_id": task_id,
            "task_id": task_id,
            "filename": filename,
            "duration": duration,
            "message": "Video uploaded successfully."
        }
