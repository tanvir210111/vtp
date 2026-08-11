"""
Application constants and static definitions for Video-to-Prompt MVP.
"""
ALLOWED_MIME_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/webm"
}

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}

MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB max payload
MAX_VIDEO_DURATION_SECONDS = 15.0        # 15 seconds max video length for MVP

SUPPORTED_STYLE_PRESETS = [
    "standard",
    "creative"
]
