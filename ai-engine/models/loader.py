"""
Multimodal Vision Model Manager & Inference Engine.
Supports OpenAI Vision API (single-request with all 5-8 keyframe images) & Google Gemini Multimodal Video API.
Synthesizes model-tailored hyper-accurate prompts for Veo, Sora, Midjourney v6, Flux.1, and Kling AI.
"""
import io
import json
import os
import time
import base64
import logging
import requests
import warnings
from typing import List, Dict, Any, Optional
from PIL import Image

warnings.filterwarnings("ignore")

try:
    from google import genai
    HAS_GENAI_SDK = True
except ImportError:
    HAS_GENAI_SDK = False

try:
    from config.settings import settings as backend_settings
except Exception:
    backend_settings = None

logger = logging.getLogger(__name__)


def _load_backend_dotenv_keys() -> Dict[str, str]:
    """Load API keys from backend/.env without exposing them in logs or responses."""
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env"))
    keys = {}
    if not os.path.exists(env_path):
        return keys

    with open(env_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            keys[key.strip()] = value.strip().strip('"').strip("'")
    return keys


OPENAI_VISION_SYSTEM_PROMPT = (
    "You are an expert Director of Photography and Senior AI Video Prompt Engineer.\n"
    "You are analyzing 5 to 8 sequence keyframes extracted from a specific video clip (up to 15 seconds long).\n\n"
    "CRITICAL DIRECTIVE: HYPER-FAITHFUL VISUAL REVERSE ENGINEERING\n"
    "- Your analysis MUST be 100% faithful to the EXACT visual content in the provided keyframe images.\n"
    "- DO NOT use generic placeholders or hallucinate details that are not in the video.\n"
    "- Identify the EXACT subject (person, animal, vehicle, landscape, 3D object), exact wardrobe & clothing colors, exact spatial layout, exact background environment, exact physical actions occurring across frames, exact lighting sources, and exact color palette.\n"
    "- In 'model_prompts' (midjourney, flux, sora, veo, kling, runway, luma), write complete, multi-sentence (80-200 word) prompts describing the PRECISE visual details observed in these keyframe images so an AI generator can reproduce this exact video.\n\n"
    "Return ONLY a valid JSON object matching this exact structure:\n"
    "{\n"
    '  "summary": "Exhaustive multi-sentence visual summary of the exact scene, action, subject, camera motion, and atmosphere across these keyframes",\n'
    '  "people": [{"count": 1, "gender": "Male/Female/Neutral/N/A", "age_group": "Young Adult/Adult/etc.", "clothes": "Exact outfit, fabric, and colors seen in keyframes", "accessories": "Exact optical glasses, hats, jewellery, or N/A", "position": "Exact spatial position in frame"}],\n'
    '  "objects": ["exact detailed object 1 seen in frames", "exact object 2", "exact object 3"],\n'
    '  "actions": ["exact physical movement 1 observed across frames", "micro-gesture 2"],\n'
    '  "camera": {"framing": "Exact framing (e.g. Medium Close-up)", "angle": "Exact angle (e.g. Low Angle / Eye Level)", "movement": "Exact observed motion (e.g. Push-in / Tracking Pan / Handheld)", "lens": "Estimated prime lens feel (e.g. 35mm f/1.4)", "depth_of_field": "Depth of field observation"},\n'
    '  "lighting": {"environment_type": "Indoor/Outdoor/Studio", "brightness": "Observed light level", "source": "Exact light sources (e.g. Golden hour sun, Overhead fluorescent, Neon sign)", "temperature": "Warm/Cool/Neutral", "description": "Detailed lighting breakdown with direction and shadow fill"},\n'
    '  "colors": {"name": "Dominant color palette name", "palette": ["#HEX1", "#HEX2", "#HEX3"], "saturation": "High/Normal/Muted", "contrast": "High/Medium/Soft", "description": "Exact color grading breakdown"},\n'
    '  "environment": {"setting": "Exact location (e.g. Modern kitchen, Mountain trail, Industrial warehouse)", "atmosphere": "Rich atmosphere & vibe", "location_type": "Indoor/Outdoor", "background": "Exact background architecture & elements"},\n'
    '  "emotions": {"primary_emotion": "Primary facial or scene emotion", "confidence": 0.98, "mood_tone": "Cinematic mood", "emotions_list": ["emotion1", "emotion2"]},\n'
    '  "model_prompts": {\n'
    '     "midjourney": "Ultra-detailed visual prompt for Midjourney v6 describing the EXACT subject, clothing, setting, composition, lighting, and lens parameters --ar 16:9 --v 6.0 --style raw",\n'
    '     "flux": "Detailed photorealistic description for Flux.1 with exact surface micro-textures, volumetric illumination, color grading hex, and focal distance.",\n'
    '     "sora": "Complete 80-200 word prompt for OpenAI Sora detailing exact physical dynamics, temporal coherence, camera rig, subject movement, 60fps photorealism matching these keyframes.",\n'
    '     "veo": "Complete 80-200 word prompt for Google Veo video generation detailing exact scene progression, camera dynamics, lighting, subject action, 4K quality.",\n'
    '     "kling": "Detailed video prompt for Kling AI structured into [Camera Movement], [Subject & Action], [Lighting & Atmosphere], [Setting] matching the exact clip.",\n'
    '     "runway": "Ultra-fluid prompt for Runway Gen-3 Alpha detailing exact camera velocity, motion guidance, and depth of field.",\n'
    '     "luma": "Hyper-realistic prompt for Luma Dream Machine highlighting exact physical movements and lighting seen in the video."\n'
    '  }\n'
    "}"
)



class ModelLoader:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.last_diagnostic: Dict[str, Any] = {}

        dotenv_keys = _load_backend_dotenv_keys()

        # Load OpenAI credentials
        openai_key = os.environ.get("OPENAI_API_KEY", "")
        if not openai_key and backend_settings is not None:
            openai_key = getattr(backend_settings, "OPENAI_API_KEY", "") or ""
        if not openai_key:
            openai_key = dotenv_keys.get("OPENAI_API_KEY", "")
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        self.openai_api_key = openai_key

        openai_model = os.environ.get("OPENAI_MODEL", "")
        if not openai_model and backend_settings is not None:
            openai_model = getattr(backend_settings, "OPENAI_MODEL", "") or ""
        if not openai_model:
            openai_model = dotenv_keys.get("OPENAI_MODEL", "gpt-4o-mini")
        self.openai_model = openai_model or "gpt-4o-mini"

        # Load Gemini credentials
        gemini_key = os.environ.get("GEMINI_API_KEY", "")
        if not gemini_key and backend_settings is not None:
            gemini_key = getattr(backend_settings, "GEMINI_API_KEY", "") or ""
        if not gemini_key:
            gemini_key = dotenv_keys.get("GEMINI_API_KEY", "")
        if gemini_key:
            os.environ["GEMINI_API_KEY"] = gemini_key
        self.gemini_api_key = gemini_key

        self._validate_api_keys()

    def _validate_api_keys(self) -> None:
        if self.openai_api_key:
            logger.info("OPENAI_API_KEY active. Model: %s", self.openai_model)
        elif self.gemini_api_key:
            logger.info("GEMINI_API_KEY active. Model: %s", self.model_name)
        else:
            logger.warning("No API keys found. System will fallback to OpenCV heuristics.")

    @staticmethod
    def encode_image_to_base64_jpeg(image_path: str, max_dim: int = 1024) -> Optional[str]:
        """Convert keyframe image to resized JPEG base64 string for efficient OpenAI API requests."""
        if not os.path.exists(image_path):
            return None
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                if max(img.size) > max_dim:
                    img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                return base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            return None

    @staticmethod
    def encode_image_to_base64(image_path: str) -> Optional[str]:
        """Convert a keyframe image file into a Base64 string."""
        if not os.path.exists(image_path):
            return None
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            return None

    @staticmethod
    def _select_evenly_spaced(frame_paths: List[str], max_frames: int = 8) -> List[str]:
        """Pick 5 to 8 frames evenly spaced across the full list."""
        if not frame_paths:
            return []
        n = len(frame_paths)
        if n <= max_frames:
            return frame_paths
        step = n / max_frames
        indices = sorted({int(i * step) for i in range(max_frames)})
        return [frame_paths[i] for i in indices]

    def analyze_frames_openai_vision(
        self,
        frame_paths: Optional[List[str]] = None,
        prompt: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Executes a SINGLE OpenAI Vision API call sending ALL 5-8 keyframe images in ONE ChatCompletion request.
        Uses 'detail: low' (85 tokens per frame) to minimize token consumption and reduce latency.
        """
        openai_key = os.environ.get("OPENAI_API_KEY") or self.openai_api_key
        if not openai_key:
            logger.warning("OPENAI_API_KEY is not set. OpenAI vision inference skipped.")
            return None

        if not frame_paths:
            logger.warning("No frame paths provided for OpenAI vision analysis.")
            return None

        sample_frames = self._select_evenly_spaced(frame_paths, max_frames=8)
        if not sample_frames:
            return None

        content_items: List[Dict[str, Any]] = [
            {"type": "text", "text": prompt or OPENAI_VISION_SYSTEM_PROMPT}
        ]

        valid_frames = 0
        for fpath in sample_frames:
            b64_str = self.encode_image_to_base64_jpeg(fpath, max_dim=1024)
            if b64_str:
                content_items.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64_str}",
                        "detail": "low"
                    }
                })
                valid_frames += 1

        if valid_frames == 0:
            logger.error("Failed to encode any valid keyframe images for OpenAI Vision API.")
            return None

        model = model_name or self.openai_model or "gpt-4o-mini"
        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": content_items
                }
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": 2500,
            "temperature": 0.2
        }

        try:
            logger.info("Sending SINGLE OpenAI Vision API request for %d keyframe images using model '%s'...", valid_frames, model)
            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=45)
            if res.status_code == 200:
                data = res.json()
                choice = data.get("choices", [{}])[0]
                text = choice.get("message", {}).get("content", "")
                if text:
                    logger.info("OpenAI Vision API single-request inference completed successfully.")
                    return text
                logger.error("OpenAI Vision API returned empty content.")
            else:
                logger.error("OpenAI API returned status %d: %s", res.status_code, res.text)
        except Exception as exc:
            logger.error("OpenAI Vision API request failed: %s", exc)

        return None

    def analyze_frames_vision_model(
        self,
        frame_paths: Optional[List[str]] = None,
        video_path: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> Optional[str]:
        """Authenticate with Gemini and analyze frames."""
        gemini_key = os.environ.get("GEMINI_API_KEY") or self.gemini_api_key
        if not gemini_key or not HAS_GENAI_SDK:
            return None

        try:
            client = genai.Client(api_key=gemini_key)
            if frame_paths:
                pil_images = []
                for path in frame_paths:
                    if os.path.exists(path):
                        try:
                            with Image.open(path) as image:
                                pil_images.append(image.copy())
                        except Exception as exc:
                            logger.exception("Could not open frame %s: %s", path, exc)

                if pil_images:
                    response = client.models.generate_content(
                        model=self.model_name,
                        contents=[prompt or OPENAI_VISION_SYSTEM_PROMPT, *pil_images],
                    )
                    text = getattr(response, "text", None) or ""
                    if text:
                        return text
        except Exception as exc:
            logger.error("Gemini multimodal vision inference failed: %s", exc)

        return None
