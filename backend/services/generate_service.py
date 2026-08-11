"""
Generate service executing AI engine pipeline, updating Video DB state, and persisting Prompt records.
"""
import sys
import os
from sqlalchemy.orm import Session
from config.settings import settings
from database.models import VideoTask, Prompt
from utils.logger import logger

# Import AI Engine Pipeline from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ai-engine")))
from pipeline import VideoToPromptPipeline  # type: ignore

class GenerateService:
    @staticmethod
    def process_task(
        task_id: str,
        style_preset: str,
        scene_threshold: float,
        db: Session
    ) -> VideoTask:
        task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
            
        task.status = "processing"
        task.style_preset = style_preset
        db.commit()

        # Set GEMINI_API_KEY in environment
        if settings.GEMINI_API_KEY:
            os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
        
        try:
            pipeline = VideoToPromptPipeline(
                storage_dir=settings.STORAGE_DIR,
                output_dir=settings.OUTPUT_DIR
            )
            result = pipeline.run(
                task_id=task.id,
                video_path=task.file_path,
                style_preset=style_preset,
                scene_threshold=scene_threshold
            )
            
            prompts_dict = result.get("prompts", {})
            selected_prompt_text = prompts_dict.get(style_preset) or prompts_dict.get("standard") or ""

            task.status = "completed"
            task.duration_seconds = result["metadata"]["duration_seconds"]
            task.resolution = result["metadata"]["resolution"]
            task.analysis_json = result["analysis"]
            task.prompts_json = result["prompts"]
            task.poster_url = result["poster_url"]
            
            # Save or update Prompt record
            prompt_rec = db.query(Prompt).filter(Prompt.video_id == task.id).first()
            if not prompt_rec:
                prompt_rec = Prompt(
                    id=f"prompt_{task.id}",
                    video_id=task.id,
                    prompt_style=style_preset,
                    prompt_content=selected_prompt_text,
                    analysis_data=result["analysis"]
                )
                db.add(prompt_rec)
            else:
                prompt_rec.prompt_style = style_preset
                prompt_rec.prompt_content = selected_prompt_text
                prompt_rec.analysis_data = result["analysis"]

            db.commit()
            db.refresh(task)
            return task
        except Exception as e:
            logger.error(f"Error processing AI pipeline for task {task_id}: {e}")
            task.status = "failed"
            db.commit()
            raise e
