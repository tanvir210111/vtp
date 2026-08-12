"""
FFmpeg & OpenCV video metadata probe, keyframe extraction, and slice engine.
"""
import json
import os
import subprocess
import logging
import cv2
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FFmpegWrapper:
    def __init__(self, ffmpeg_bin: str = "ffmpeg", ffprobe_bin: str = "ffprobe"):
        self.ffmpeg_bin = ffmpeg_bin
        self.ffprobe_bin = ffprobe_bin

    def get_metadata(self, video_path: str) -> Dict[str, Any]:
        """Extract video metadata (width, height, duration, fps, resolution, codec) using FFprobe or OpenCV."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at {video_path}")
        
        # Method 1: Try ffprobe
        cmd = [
            self.ffprobe_bin,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
            
            width = int(video_stream.get("width", 1920))
            height = int(video_stream.get("height", 1080))
            duration = float(data.get("format", {}).get("duration", 10.0))
            fps_str = video_stream.get("r_frame_rate", "30/1")
            if "/" in fps_str:
                num, den = fps_str.split("/")
                fps = float(num) / float(den) if float(den) != 0 else 30.0
            else:
                fps = float(fps_str)
                
            return {
                "width": width,
                "height": height,
                "resolution": f"{width}x{height}",
                "duration_seconds": round(duration, 2),
                "fps": round(fps, 2),
                "codec": video_stream.get("codec_name", "h264"),
                "bitrate": int(data.get("format", {}).get("bit_rate", 5000000))
            }
        except Exception:
            logger.info(f"FFprobe CLI unavailable. Falling back to OpenCV probe for {video_path}.")

        # Method 2: OpenCV fallback metadata extraction
        try:
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1920
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 1080
                fps = float(cap.get(cv2.CAP_PROP_FPS)) or 30.0
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
                duration = round(frame_count / fps, 2) if fps > 0 else 10.0
                cap.release()
                
                return {
                    "width": width,
                    "height": height,
                    "resolution": f"{width}x{height}",
                    "duration_seconds": max(1.0, duration),
                    "fps": round(fps, 2),
                    "codec": "h264",
                    "bitrate": 5000000
                }
        except Exception as e:
            logger.warning(f"OpenCV metadata probe failed: {e}")

        # Method 3: Default fallback
        file_size = os.path.getsize(video_path)
        return {
            "width": 1920,
            "height": 1080,
            "resolution": "1920x1080",
            "duration_seconds": 10.0,
            "fps": 30.0,
            "codec": "h264",
            "bitrate": file_size * 8 // 10
        }

    def extract_frames(self, video_path: str, output_dir: str, interval_sec: float = 1.5) -> List[str]:
        """Extract keyframes at regular intervals using FFmpeg or OpenCV."""
        os.makedirs(output_dir, exist_ok=True)
        output_pattern = os.path.join(output_dir, "frame_%04d.jpg")
        
        # Method 1: Try FFmpeg CLI
        cmd = [
            self.ffmpeg_bin,
            "-y",
            "-i", video_path,
            "-vf", f"fps=1/{interval_sec}",
            "-q:v", "2",
            output_pattern
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            extracted = sorted([
                os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("frame_") and f.endswith(".jpg")
            ])
            if extracted:
                return extracted
        except Exception:
            logger.info("FFmpeg CLI unavailable. Extracting keyframes with OpenCV...")

        # Method 2: Extract keyframes using OpenCV
        extracted_paths = []
        try:
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                fps = float(cap.get(cv2.CAP_PROP_FPS)) or 30.0
                frame_interval = max(1, int(fps * interval_sec))
                
                frame_idx = 0
                saved_count = 0
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    if frame_idx % frame_interval == 0:
                        saved_count += 1
                        out_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
                        cv2.imwrite(out_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                        extracted_paths.append(out_path)
                        
                    frame_idx += 1
                    
                cap.release()
                if extracted_paths:
                    return extracted_paths
        except Exception as e:
            logger.warning(f"OpenCV frame extraction failed: {e}")

        return []

    def extract_audio(self, video_path: str, output_audio_path: str) -> Optional[str]:
        """Extract audio track from video file into MP3 format for speech & audio mood analysis."""
        if not video_path or not os.path.exists(video_path):
            return None

        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
        cmd = [
            self.ffmpeg_bin,
            "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-ar", "16000",
            "-ac", "1",
            output_audio_path
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            if os.path.exists(output_audio_path) and os.path.getsize(output_audio_path) > 1000:
                logger.info("Successfully extracted audio track to %s", output_audio_path)
                return output_audio_path
        except Exception as e:
            logger.info("Audio extraction via FFmpeg CLI skipped or unavailable: %s", e)

        return None
