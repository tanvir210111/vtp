"""
Generate API router supporting video_id, style, and task_id parameters.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import VideoTask
from services.generate_service import GenerateService

router = APIRouter(prefix="/generate", tags=["Generate"])

class GenerateRequest(BaseModel):
    video_id: Optional[str] = None
    task_id: Optional[str] = None
    style: Optional[str] = "standard"
    style_preset: Optional[str] = "standard"
    scene_threshold: float = 0.35

@router.post("")
def generate_prompts(req: GenerateRequest, db: Session = Depends(get_db)):
    target_id = req.video_id or req.task_id
    if not target_id:
        raise HTTPException(status_code=400, detail="Missing required 'video_id' or 'task_id' field.")

    style_name = req.style or req.style_preset or "standard"

    try:
        task = GenerateService.process_task(
            task_id=target_id,
            style_preset=style_name,
            scene_threshold=req.scene_threshold,
            db=db
        )
        prompts = task.prompts_json or {}
        selected_prompt = prompts.get(style_name) or prompts.get("standard") or (list(prompts.values())[0] if prompts else "")

        return {
            "success": True,
            "prompt_id": f"prompt_{task.id}",
            "video_id": task.id,
            "task_id": task.id,
            "style": style_name,
            "prompt": selected_prompt,
            "status": task.status,
            "duration_seconds": task.duration_seconds,
            "resolution": task.resolution,
            "poster_url": task.poster_url,
            "analysis": task.analysis_json,
            "prompts": task.prompts_json
        }
    except Exception as e:
        # Build structured error response
        error_type = type(e).__name__
        stage = getattr(e, "stage", "pipeline") if hasattr(e, "stage") else "pipeline"
        message = str(e) or "Unknown error during generation"
        # Log is handled in service; avoid leaking secrets here
        payload = {
            "success": False,
            "status": "failed",
            "task_id": target_id,
            "message": message,
            "error_type": error_type,
            "stage": stage,
        }
        return JSONResponse(status_code=400, content=payload)

@router.get("/{task_id}")
def get_task_status(task_id: str, db: Session = Depends(get_db)):
    task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    prompts = task.prompts_json or {}
    selected_prompt = prompts.get(task.style_preset or "standard") or prompts.get("standard") or ""

    return {
        "success": True,
        "prompt_id": f"prompt_{task.id}",
        "video_id": task.id,
        "task_id": task.id,
        "filename": task.filename,
        "style": task.style_preset or "standard",
        "prompt": selected_prompt,
        "status": task.status,
        "duration_seconds": task.duration_seconds,
        "resolution": task.resolution,
        "poster_url": task.poster_url,
        "analysis": task.analysis_json,
        "prompts": task.prompts_json
    }
