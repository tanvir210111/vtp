"""
General helper functions for task IDs and time formats.
"""
import uuid
import time

def generate_task_id() -> str:
    """Generate unique task identifier."""
    return f"vtp_task_{uuid.uuid4().hex[:12]}"

def format_duration(seconds: float) -> str:
    """Format seconds into HH:MM:SS string."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
