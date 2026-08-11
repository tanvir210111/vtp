"""
History API router matching exact specification.
"""
from typing import Optional
from datetime import datetime
import traceback
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["History"])

@router.get("")
def list_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    style: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        skip = (page - 1) * limit
        total, items = HistoryService.get_history(db, skip=skip, limit=limit, style=style)
        
        formatted_items = []
        for item in items:
            created_val = getattr(item, "created_at", None)
            created_str = ""
            if created_val:
                if isinstance(created_val, datetime):
                    created_str = created_val.strftime("%Y-%m-%d %H:%M")
                else:
                    created_str = str(created_val)

            formatted_items.append({
                "id": str(getattr(item, "id", "")),
                "video": str(getattr(item, "filename", "")),
                "style": str(getattr(item, "style_preset", "standard") or "standard"),
                "created_at": created_str
            })
            
        return formatted_items
    except Exception as e:
        print("History API Exception:\n", traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}")
def delete_history_item(task_id: str, db: Session = Depends(get_db)):
    success = HistoryService.delete_task(task_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "status": "deleted", "task_id": task_id}
