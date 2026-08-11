"""
Download service handling prompt formatting exports.
"""
import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from config.settings import settings

class DownloadService:
    @staticmethod
    def get_export_file(task_id: str, format_type: str = "markdown"):
        ext_map = {
            "markdown": ("markdown", f"{task_id}.md", "text/markdown"),
            "md": ("markdown", f"{task_id}.md", "text/markdown"),
            "json": ("json", f"{task_id}.json", "application/json"),
            "txt": ("txt", f"{task_id}.txt", "text/plain")
        }
        
        if format_type.lower() not in ext_map:
            raise HTTPException(status_code=400, detail=f"Unsupported format '{format_type}'.")
            
        sub_dir, filename, media_type = ext_map[format_type.lower()]
        file_path = os.path.join(settings.OUTPUT_DIR, sub_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Export file not found.")
            
        return FileResponse(
            path=file_path,
            filename=f"video_prompt_{task_id}.{sub_dir if sub_dir != 'markdown' else 'md'}",
            media_type=media_type
        )
