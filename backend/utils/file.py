"""
File IO and sanitized file naming helpers.
"""
import os
import re

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal or invalid characters."""
    filename = os.path.basename(filename)
    filename = re.sub(r"[^\w\.-]", "_", filename)
    return filename

def ensure_dir(dir_path: str) -> str:
    """Ensure directory path exists on filesystem."""
    os.makedirs(dir_path, exist_ok=True)
    return dir_path
