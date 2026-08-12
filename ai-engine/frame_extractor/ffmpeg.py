"""
FFmpeg & OpenCV video metadata probe, keyframe extraction, and slice engine.
"""
import json
import os
import subprocess
import logging
import cv2
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class FFmpegWrapper:
    def __init__(self, ffmpeg_bin: str = "ffmpeg", ffprobe_bin: str = "ffprobe"):
        self.ffmpeg_bin = ffmpeg_bin
        self.ffprobe_bin = ffprobe_bin

    def get_metadata(self, video_path: str) -> Dict[str, Any]:
        """Extract video metadata (width, height, duration, fps, resolution, codec) using FFprobe or OpenCV."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at {video_path}")
        
        logger.info("[PIPELINE] video:metadata:start: %s", video_path)

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
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
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
                
            meta = {
                "width": width,
                "height": height,
                "resolution": f"{width}x{height}",
                "duration_seconds": round(duration, 2),
                "fps": round(fps, 2),
                "codec": video_stream.get("codec_name", "h264"),
                "bitrate": int(data.get("format", {}).get("bit_rate", 5000000))
            }
            logger.info("[PIPELINE] video:metadata:loaded (FFprobe): %s", meta)
            return meta
        except subprocess.TimeoutExpired:
            logger.warning("[PIPELINE] FFprobe subprocess timed out (>10s). Falling back to OpenCV probe.")
        except Exception as e:
            logger.info(f"[PIPELINE] FFprobe CLI unavailable ({e}). Falling back to OpenCV probe for {video_path}.")

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
                
                meta = {
                    "width": width,
                    "height": height,
                    "resolution": f"{width}x{height}",
                    "duration_seconds": max(1.0, duration),
                    "fps": round(fps, 2),
                    "codec": "h264",
                    "bitrate": 5000000
                }
                logger.info("[PIPELINE] video:metadata:loaded (OpenCV): %s", meta)
                return meta
        except Exception as e:
            logger.warning(f"[PIPELINE] OpenCV metadata probe failed: {e}")

        # Method 3: Default fallback
        file_size = os.path.getsize(video_path)
        meta = {
            "width": 1920,
            "height": 1080,
            "resolution": "1920x1080",
            "duration_seconds": 10.0,
            "fps": 30.0,
            "codec": "h264",
            "bitrate": file_size * 8 // 10
        }
        logger.info("[PIPELINE] video:metadata:loaded (Default fallback): %s", meta)
        return meta

    def extract_frames(self, video_path: str, output_dir: str, interval_sec: float = 1.5) -> List[str]:
        """Extract keyframes at regular intervals using FFmpeg or OpenCV."""
        logger.info("[PIPELINE] extraction:start: %s -> %s", video_path, output_dir)
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
            subprocess.run(cmd, capture_output=True, check=True, timeout=10)
            extracted = sorted([
                os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("frame_") and f.endswith(".jpg")
            ])
            if extracted:
                for idx, path in enumerate(extracted, start=1):
                    logger.info("[PIPELINE] extraction:frame:%d -> %s", idx, path)
                logger.info("[PIPELINE] extraction:complete (FFmpeg): %d frames", len(extracted))
                return extracted
        except subprocess.TimeoutExpired:
            logger.warning("[PIPELINE] FFmpeg frame extraction timed out (>10s). Falling back to OpenCV.")
        except Exception as e:
            logger.info(f"[PIPELINE] FFmpeg CLI unavailable ({e}). Extracting keyframes with OpenCV...")

        # Method 2: Extract keyframes using OpenCV
        extracted_paths = []
        try:
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                fps = float(cap.get(cv2.CAP_PROP_FPS)) or 30.0
                frame_interval = max(1, int(fps * interval_sec))
                
                frame_idx = 0
                saved_count = 0
                max_read_frames = 1800  # Safeguard limit: max 60s @ 30fps
                
                while frame_idx < max_read_frames:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    if frame_idx % frame_interval == 0:
                        saved_count += 1
                        out_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
                        cv2.imwrite(out_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                        extracted_paths.append(out_path)
                        logger.info("[PIPELINE] extraction:frame:%d -> %s", saved_count, out_path)
                        
                    frame_idx += 1
                    
                cap.release()
                if extracted_paths:
                    logger.info("[PIPELINE] extraction:complete (OpenCV): %d frames", len(extracted_paths))
                    return extracted_paths
        except Exception as e:
            logger.warning(f"[PIPELINE] OpenCV frame extraction failed: {e}")

        logger.warning("[PIPELINE] extraction:empty - returning []")
        return []

    def extract_audio(self, video_path: str, output_audio_path: str) -> Optional[str]:
        """Extract high-fidelity 44.1kHz audio track from video file for precise speech & acoustic analysis."""
        if not video_path or not os.path.exists(video_path):
            return None

        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
        cmd = [
            self.ffmpeg_bin,
            "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-q:a", "0",
            "-ar", "44100",
            "-ac", "2",
            output_audio_path
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=10)
            if os.path.exists(output_audio_path) and os.path.getsize(output_audio_path) > 1000:
                logger.info("[PIPELINE] audio:extracted: %s", output_audio_path)
                return output_audio_path
        except subprocess.TimeoutExpired:
            logger.warning("[PIPELINE] FFmpeg audio extraction timed out (>10s). Skipping audio.")
        except Exception as e:
            logger.info("High-fidelity audio extraction via FFmpeg CLI skipped: %s", e)

        return None

    @staticmethod
    def filter_sharp_frames(frame_paths: List[str], target_count: int = 12) -> List[str]:
        """Filters keyframe images based on OpenCV Laplacian variance sharpness score to discard motion blur."""
        if not frame_paths or len(frame_paths) <= target_count:
            return frame_paths

        scored_frames = []
        for path in frame_paths:
            if not os.path.exists(path):
                continue
            try:
                img = cv2.imread(path)
                if img is not None:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                    scored_frames.append((path, variance))
                else:
                    scored_frames.append((path, 0.0))
            except Exception:
                scored_frames.append((path, 0.0))

        if not scored_frames:
            return frame_paths

        # Keep top sharpest frames
        scored_frames.sort(key=lambda x: x[1], reverse=True)
        top_k = max(target_count, int(len(scored_frames) * 0.75))
        sharp_paths = set([f[0] for f in scored_frames[:top_k]])

        # Maintain chronological order of selected sharp frames
        chronological_sharp = [p for p in frame_paths if p in sharp_paths]

        if len(chronological_sharp) <= target_count:
            return chronological_sharp

        step = len(chronological_sharp) / target_count
        indices = sorted({int(i * step) for i in range(target_count)})
        return [chronological_sharp[i] for i in indices]
