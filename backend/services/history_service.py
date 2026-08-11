"""
History CRUD service for managing past generation tasks.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from database.models import VideoTask

class HistoryService:
    @staticmethod
    def get_history(db: Session, skip: int = 0, limit: int = 20, style: Optional[str] = None):
        try:
            query = db.query(VideoTask)
            if style:
                query = query.filter(VideoTask.style_preset == style)
                
            total = query.count()
            items = query.order_by(VideoTask.id.desc()).offset(skip).limit(limit).all()
            return total, items
        except Exception as err:
            print("History DB Query Error:", err)
            db.rollback()
            return 0, []

    @staticmethod
    def delete_task(task_id: str, db: Session) -> bool:
        try:
            task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
            if task:
                db.delete(task)
                db.commit()
                return True
            return False
        except Exception:
            db.rollback()
            return False
