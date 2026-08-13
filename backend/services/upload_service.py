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
from utils.logger import logger
from database.models import VideoTask

class UploadService:
    @staticmethod
    async def save_uploaded_file(file, db: Session) -> dict:
        filename = sanitize_filename(file.filename or "uploaded_video.mp4")
        content_type = getattr(file, "content_type", "unknown")

        logger.info("[UPLOAD] request received")
        logger.info(f"[UPLOAD] filename={filename}")
        logger.info(f"[UPLOAD] content_type={content_type}")
        logger.info("[UPLOAD] upload started")

        task_id = generate_task_id()
        task_upload_dir = ensure_dir(os.path.join(settings.STORAGE_DIR, "uploads", task_id))
        saved_file_path = os.path.join(task_upload_dir, filename)

        # Stream file chunks to disk to minimize memory overhead
        file_size = 0
        async with aiofiles.open(saved_file_path, "wb") as out_file:
            while chunk := await file.read(1024 * 1024):  # 1 MB chunks
                await out_file.write(chunk)
                file_size += len(chunk)

        logger.info(f"[UPLOAD] upload completed ({file_size / (1024 * 1024):.2f} MB)")
        logger.info(f"[UPLOAD] file saved at {saved_file_path}")

        # Validate video format and size
        try:
            validate_video_file(filename, file_size)
        except Exception as ve:
            if os.path.exists(saved_file_path):
                os.remove(saved_file_path)
            raise ve

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

        logger.info(f"[UPLOAD] response sent for task_id={task_id}")

        return {
            "success": True,
            "video_id": task_id,
            "task_id": task_id,
            "filename": filename,
            "duration": duration,
            "message": "Video uploaded successfully."
        }
