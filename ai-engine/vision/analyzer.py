"""
Main Vision Analyzer orchestrator.
Sends keyframe images to ModelLoader for OpenAI Vision API (single-request with 5-8 frames) or Gemini Multimodal Vision AI Model inference.
Parses model responses via parser.py, with automatic fallback to OpenCV heuristics via fallback.py.
"""
import logging
from typing import List, Dict, Any, Optional

from models.loader import ModelLoader
from .parser import VisionParser
from .fallback import VisionFallbackAnalyzer

logger = logging.getLogger(__name__)


class VisionAnalyzer:
    def __init__(self, model_name: str = "gpt-4o-mini"):
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
        Orchestrate Vision AI inference over 5-8 sampled keyframe images.
        1. Executes SINGLE request OpenAI Vision API with all 5-8 keyframe images if OPENAI_API_KEY is configured.
        2. Falls back to Google Gemini Multimodal Vision if GEMINI_API_KEY is configured.
        3. Parses raw JSON response into structured Analysis JSON.
        4. Automatically falls back to OpenCV heuristic analyzer if vision models are offline.
        """
        meta = metadata or {}
        duration = float(meta.get("duration_seconds", meta.get("duration", 10.0)))
        fps = int(meta.get("fps", 30))

        # Select 5 to 8 frames evenly spaced across 15sec video clip
        sample_frames = self._select_evenly_spaced(frame_paths, max_frames=8)

        raw_vision_response = None
        engine_mode = None

        # 1. Primary: OpenAI Vision API (Single request containing all 5-8 keyframes)
        if self.model_loader.openai_api_key:
            try:
                raw_vision_response = self.model_loader.analyze_frames_openai_vision(
                    frame_paths=sample_frames
                )
                if raw_vision_response:
                    engine_mode = f"OpenAI Vision API Single-Request ({self.model_loader.openai_model})"
            except Exception as exc:
                logger.warning("OpenAI vision analysis failed, falling back: %s", exc)

        # 2. Secondary: Gemini Multimodal Vision (if OpenAI is not configured or failed)
        if not raw_vision_response and self.model_loader.gemini_api_key:
            try:
                raw_vision_response = self.model_loader.analyze_frames_vision_model(
                    frame_paths=sample_frames,
                    video_path=video_path,
                )
                if raw_vision_response:
                    engine_mode = f"Google Gemini Multimodal Video AI ({self.model_loader.model_name})"
            except Exception as exc:
                logger.warning("Gemini vision analysis failed: %s", exc)

        # 3. Parse Vision AI response or fallback to OpenCV heuristics
        if raw_vision_response:
            logger.info("Successfully executed Multimodal Vision AI Model inference (%s).", engine_mode)
            analysis_data = VisionParser.parse_raw_response(raw_vision_response, default_duration=duration, default_fps=fps)
            analysis_data["vision_engine"] = {
                "mode": engine_mode or "Multimodal Vision AI Inference",
                "model_name": self.model_loader.openai_model if self.model_loader.openai_api_key else self.model_loader.model_name,
                "status": "active",
            }
        else:
            logger.info("Vision AI model offline or unavailable. Falling back to OpenCV heuristic computer vision analyzer.")
            analysis_data = VisionFallbackAnalyzer.analyze_fallback(sample_frames, duration=duration, fps=fps)
            analysis_data["vision_engine"] = {
                "mode": "Heuristic Computer Vision Engine (Model Standby)",
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
