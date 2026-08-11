"""
Main Vision Analyzer orchestrator.
Sends keyframe images & native video file to ModelLoader for Multimodal Vision AI Model inference.
Parses model responses via parser.py, with automatic fallback to OpenCV heuristics via fallback.py.
"""
import logging
from typing import List, Dict, Any, Optional

from models.loader import ModelLoader
from .parser import VisionParser
from .fallback import VisionFallbackAnalyzer

logger = logging.getLogger(__name__)


class VisionAnalyzer:
    def __init__(self, model_name: str = "gemini-3.5-flash"):
        self.model_loader = ModelLoader(model_name=model_name)

    def analyze(
        self,
        frame_paths: List[str],
        video_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        scenes: Optional[List[Dict[str, Any]]] = None,
        timeline: Optional[List[Dict[str, Any]]] = None,
        style_preset: str = "standard",
    ) -> Dict[str, Any]:
        """
        Orchestrate Vision AI inference over native video file or keyframe images.
        1. Passes video file / Base64 frames to Google Gemini / Multimodal Vision AI Model.
        2. Parses raw response into structured Analysis JSON.
        3. Automatically falls back to OpenCV heuristic analyzer if vision model is offline.
        """
        meta = metadata or {}
        duration = float(meta.get("duration_seconds", meta.get("duration", 10.0)))
        fps = int(meta.get("fps", 30))

        sample_frames = self._select_evenly_spaced(frame_paths, max_frames=8)

        raw_vision_response = self.model_loader.analyze_frames_vision_model(
            frame_paths=sample_frames,
            video_path=video_path,
        )

        if raw_vision_response:
            logger.info("Successfully executed Multimodal Vision AI Model inference.")
            analysis_data = VisionParser.parse_raw_response(raw_vision_response, default_duration=duration, default_fps=fps)
            analysis_data["vision_engine"] = {
                "mode": "Google Gemini Native Multimodal Video AI Inference",
                "model_name": self.model_loader.model_name,
                "status": "active",
            }
        else:
            logger.info("Vision AI model offline. Falling back to the OpenCV heuristic computer vision analyzer.")
            analysis_data = VisionFallbackAnalyzer.analyze_fallback(sample_frames, duration=duration, fps=fps)
            analysis_data["vision_engine"] = {
                "mode": "Heuristic Computer Vision Engine (Model Standby)",
                "model_status": "Ready for Qwen2.5-VL / Florence-2 / Ollama Vision",
                "status": "standby",
            }

        if timeline and len(timeline) > 0:
            analysis_data["timeline"] = timeline

        return analysis_data

    @staticmethod
    def _select_evenly_spaced(frame_paths: List[str], max_frames: int = 8) -> List[str]:
        """Pick up to max_frames frames evenly spaced across the full list."""
        if not frame_paths:
            return []

        n = len(frame_paths)
        if n <= max_frames:
            return frame_paths

        step = n / max_frames
        indices = sorted({int(i * step) for i in range(max_frames)})
        return [frame_paths[i] for i in indices]
