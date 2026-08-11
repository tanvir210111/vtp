"""
Video payload validation helpers enforcing 15-second duration and MP4/MOV/WEBM formats.
"""
import os
from fastapi import HTTPException
from config.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES, MAX_VIDEO_DURATION_SECONDS

def validate_video_file(filename: str, file_size: int, duration_seconds: float = None):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: MP4, MOV, WEBM"
        )
        
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum threshold of {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
        )

    if duration_seconds is not None and duration_seconds > MAX_VIDEO_DURATION_SECONDS:
        raise HTTPException(
            status_code=400,
            detail=f"Video length ({duration_seconds:.1f}s) exceeds maximum allowed duration of {MAX_VIDEO_DURATION_SECONDS} seconds."
        )
