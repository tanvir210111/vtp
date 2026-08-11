"""
Poster thumbnail & grid storyboard preview creator.
"""
import os
from typing import List
from PIL import Image, ImageDraw, ImageFont

class ThumbnailGenerator:
    @staticmethod
    def generate_poster(frame_paths: List[str], output_path: str, target_size=(640, 360)) -> str:
        """Create primary poster thumbnail image from middle keyframe."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if frame_paths and os.path.exists(frame_paths[0]):
            mid_index = len(frame_paths) // 2
            with Image.open(frame_paths[mid_index]) as img:
                poster = img.copy()
                poster.thumbnail(target_size)
                poster.save(output_path, "JPEG", quality=85)
                return output_path
                
        # Fallback thumbnail
        img = Image.new("RGB", target_size, color=(20, 24, 33))
        draw = ImageDraw.Draw(img)
        draw.text(( target_size[0]//2 - 60, target_size[1]//2 - 10 ), "VIDEO PREVIEW", fill=(200, 210, 230))
        img.save(output_path, "JPEG")
        return output_path

    @staticmethod
    def generate_storyboard_grid(frame_paths: List[str], output_path: str) -> str:
        """Combine up to 4 keyframes into a 2x2 storyboard poster grid."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas = Image.new("RGB", (1280, 720), color=(10, 12, 16))
        
        frames_to_use = frame_paths[:4]
        positions = [(0, 0), (640, 0), (0, 360), (640, 360)]
        
        for idx, path in enumerate(frames_to_use):
            if os.path.exists(path):
                with Image.open(path) as frame:
                    resized = frame.resize((640, 360))
                    canvas.paste(resized, positions[idx])
                    
        canvas.save(output_path, "JPEG", quality=85)
        return output_path
