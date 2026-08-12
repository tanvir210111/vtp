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
import sys
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

import importlib

try:
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend"))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    config_module = importlib.import_module("config.settings")
    backend_settings = getattr(config_module, "settings", None)
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
    "You are a Director of Photography and Senior AI Vision Analyst specializing in granular video frame analysis.\n"
    "You are provided with 10 sequence keyframes extracted evenly across a video clip (up to 15 seconds long).\n\n"
    "CRITICAL DIRECTIVE 1: EXACT EMOTION TAXONOMY\n"
    "You MUST classify the primary emotion, facial expression, and mood from this EXACT allowed list:\n"
    "- Neutral (স্বাভাবিক/কোনো বিশেষ emotion নেই)\n"
    "- Happy (খুশি, আনন্দ)\n"
    "- Sad (দুঃখ, মন খারাপ)\n"
    "- Angry (রাগ)\n"
    "- Fearful (ভয়/আতঙ্ক)\n"
    "- Surprised (অবাক)\n"
    "- Disgusted (বিরক্ত/ঘৃণা)\n"
    "- Confused (বিভ্রান্ত)\n"
    "- Excited (উত্তেজিত/উচ্ছ্বসিত)\n"
    "- Worried / Anxious (চিন্তিত/উদ্বিগ্ন)\n"
    "- Calm / Relaxed (শান্ত/relaxed)\n"
    "- Embarrassed / Shy (লজ্জিত/সংকোচ)\n"
    "- Love / Affection (ভালোবাসা/স্নেহ)\n"
    "- Focused / Serious (মনোযোগী/গম্ভীর)\n"
    "- Smirking / Sarcastic (মুচকি হাসি/ব্যঙ্গাত্মক)\n\n"
    "CRITICAL DIRECTIVE 2: COMPREHENSIVE FRAME-BY-FRAME ANALYSIS CHECKLIST\n"
    "For all 10 keyframes, systematically evaluate:\n"
    "1. Face emotion & Facial expression (eyes, mouth, brow shape)\n"
    "2. Eye direction / gaze (looking at camera, subject, side, down, away)\n"
    "3. Head position (tilted, turned left/right, nodding, upright)\n"
    "4. Body posture & Hand gesture (crossed arms, gesturing, open posture, sitting, standing, leaning)\n"
    "5. Body movement & Actions (walking, running, turning, reaching, physical interactions)\n"
    "6. Person-to-person interaction & Object interaction (holding, touching, speaking to another)\n"
    "7. Scene / environment & Lighting (indoor/outdoor, light source, shadow fill, key light)\n"
    "8. Color / visual mood & Color grade\n"
    "9. Camera angle, movement & Shot type (close-up, medium, wide, low angle, high angle, tracking)\n"
    "10. Text / subtitle / lip movement / audio mood\n\n"
    "CRITICAL DIRECTIVE 3: MANDATORY EXHAUSTIVE PROMPT LENGTH\n"
    "- DO NOT RETURN SHORT PROMPTS, ONE-LINERS, OR ABSTRACT SUMMARIES.\n"
    "- Every single prompt in 'model_prompts' (midjourney, flux, sora, veo, kling, runway, luma) MUST be a complete, highly descriptive, 150 to 300 word visual narrative masterwork.\n"
    "- Detail the exact subject, micro facial expressions, eye gaze, head position, body posture, hand gestures, exact wardrobe & fabric colors, background architecture, volumetric lighting sources, color palette hex codes, lens optics, and camera motion.\n\n"
    "CRITICAL DIRECTIVE 4: EXACT OBJECT MOVEMENT & KINETIC TRAJECTORY TRACKING\n"
    "- Trace the exact spatial path, direction, velocity, and physical interaction of every object and subject across the 12 sequence keyframes.\n"
    "- Specify exact direction of motion (e.g. 'moving diagonally from bottom-left to top-right', 'rotating 45 degrees counter-clockwise', 'hand reaching forward to pick up camera', 'vehicle accelerating towards horizon').\n"
    "- Detail object physical state changes, spatial placement, speed, and kinetic physics dynamics in 'actions' array, 'summary', and all 'model_prompts'.\n\n"
    "Return ONLY a valid JSON object matching this exact structure:\n"
    "{\n"
    '  "summary": "Exhaustive 4-6 sentence visual summary across all 10 keyframes detailing progression of action, emotions, facial expressions, eye gaze, posture, lighting, and camera work",\n'
    '  "emotions": {\n'
    '     "primary_emotion": "Select EXACT emotion from allowed list above (e.g. Focused / Serious or Happy)",\n'
    '     "facial_expression": "Detailed 2-sentence breakdown of eyes, mouth, brow, and micro-expressions observed across keyframes",\n'
    '     "confidence": 0.98,\n'
    '     "mood_tone": "Specific emotional mood tone",\n'
    '     "emotions_list": ["Primary Emotion", "Secondary Emotion"]\n'
    '  },\n'
    '  "people": [{\n'
    '     "count": 1,\n'
    '     "gender": "Male/Female/Neutral/N/A",\n'
    '     "age_group": "Young Adult/Adult/etc.",\n'
    '     "clothes": "Exact outfit, fabric, and colors seen in keyframes",\n'
    '     "position": "Exact spatial position",\n'
    '     "eye_gaze": "Exact eye direction/gaze",\n'
    '     "head_position": "Exact head posture/angle",\n'
    '     "body_posture": "Exact body posture and stance",\n'
    '     "hand_gestures": "Exact hand and arm placement/gestures"\n'
    '  }],\n'
    '  "objects": ["exact object 1 with interaction details", "exact object 2"],\n'
    '  "actions": ["exact physical action 1", "person-to-person interaction 2"],\n'
    '  "camera": {\n'
    '     "framing": "Exact shot type (Close-up / Medium Shot / Wide Shot)",\n'
    '     "angle": "Exact camera angle (Eye Level / Low Angle / High Angle)",\n'
    '     "movement": "Exact camera movement (Push-in / Tracking Pan / Static)",\n'
    '     "lens": "Estimated prime lens feel (e.g. 35mm f/1.4)",\n'
    '     "depth_of_field": "Depth of field observation"\n'
    '  },\n'
    '  "lighting": {"environment_type": "Indoor/Outdoor/Studio", "brightness": "Observed light level", "source": "Exact light sources", "temperature": "Warm/Cool/Neutral", "description": "Detailed lighting breakdown"},\n'
    '  "colors": {"name": "Dominant color palette name", "palette": ["#HEX1", "#HEX2", "#HEX3"], "saturation": "High/Normal/Muted", "contrast": "High/Medium/Soft", "description": "Exact color grading breakdown"},\n'
    '  "environment": {"setting": "Exact location setting", "atmosphere": "Rich atmosphere & vibe", "location_type": "Indoor/Outdoor", "background": "Exact background architecture & elements"},\n'
    '  "model_prompts": {\n'
    '     "midjourney": "Exhaustive 150-300 word visual prompt for Midjourney v6 describing exact subject, facial expression, eye gaze, posture, hand gestures, wardrobe, setting, background geometry, volumetric lighting, color grade, and lens parameters --ar 16:9 --v 6.0 --style raw",\n'
    '     "flux": "Exhaustive 150-300 word photorealistic prompt for Flux.1 describing exact facial micro-textures, posture, hand gestures, clothing, background elements, volumetric illumination, color grading hex, and focal distance.",\n'
    '     "sora": "Exhaustive 150-300 word video generation prompt for OpenAI Sora detailing exact physical dynamics, temporal coherence, camera rig, subject movement, 60fps photorealism matching these 10 keyframes.",\n'
    '     "veo": "Exhaustive 150-300 word prompt for Google Veo video generation detailing exact scene progression, facial expression, body gestures, camera dynamics, lighting, 4K quality.",\n'
    '     "kling": "Exhaustive 150-300 word video prompt for Kling AI structured into [Camera Movement], [Subject & Action], [Lighting & Atmosphere], [Setting] matching the exact clip.",\n'
    '     "runway": "Exhaustive 150-300 word prompt for Runway Gen-3 Alpha detailing exact camera velocity, motion guidance, subject gestures, and depth of field.",\n'
    '     "luma": "Exhaustive 150-300 word prompt for Luma Dream Machine highlighting exact physical movements, facial expression, gestures, and lighting seen in the video."\n'
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
    def _select_evenly_spaced(frame_paths: List[str], max_frames: int = 12) -> List[str]:
        """Pick 12 frames evenly spaced across the full list."""
        if not frame_paths:
            return []
        n = len(frame_paths)
        if n <= max_frames:
            return frame_paths
        step = n / max_frames
        indices = sorted({int(i * step) for i in range(max_frames)})
        return [frame_paths[i] for i in indices]

    def transcribe_audio_openai(self, audio_path: str) -> Optional[Dict[str, Any]]:
        """Transcribe audio track using OpenAI Whisper API with verbose precision & zero-temperature mode."""
        openai_key = os.environ.get("OPENAI_API_KEY") or self.openai_api_key
        if not openai_key or not audio_path or not os.path.exists(audio_path):
            return None

        try:
            headers = {"Authorization": f"Bearer {openai_key}"}
            with open(audio_path, "rb") as f:
                files = {"file": (os.path.basename(audio_path), f, "audio/mpeg")}
                data = {
                    "model": "whisper-1",
                    "response_format": "verbose_json",
                    "temperature": "0.0"
                }
                logger.info("Transcribing video audio track via OpenAI Whisper API (verbose_json)...")
                res = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files, data=data, timeout=30)
                if res.status_code == 200:
                    result = res.json()
                    transcript_text = result.get("text", "").strip()
                    language = result.get("language", "English")
                    duration = result.get("duration", 0.0)
                    segments = result.get("segments", [])
                    segment_summary = []
                    for seg in segments[:8]:
                        start = round(seg.get("start", 0.0), 1)
                        end = round(seg.get("end", 0.0), 1)
                        stext = seg.get("text", "").strip()
                        if stext:
                            segment_summary.append(f"[{start}s-{end}s]: \"{stext}\"")
                    
                    seg_str = "; ".join(segment_summary) if segment_summary else transcript_text

                    if transcript_text or seg_str:
                        logger.info("Successfully transcribed audio track via Whisper (%s, %s): '%s'", language, duration, transcript_text[:100])
                        return {
                            "has_audio": True,
                            "transcript": transcript_text or "Audio track detected",
                            "language": language,
                            "time_aligned_dialogue": seg_str
                        }
        except Exception as e:
            logger.info("OpenAI Whisper transcription skipped or failed: %s", e)

        return None

    def analyze_frames_openai_vision(
        self,
        frame_paths: Optional[List[str]] = None,
        audio_path: Optional[str] = None,
        prompt: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Executes a SINGLE OpenAI Vision API call sending 6 representative keyframe images (0%, 20%, 40%, 60%, 80%, 100%) + Whisper audio transcription in ONE ChatCompletion request.
        Uses lightweight 1024px images and 'detail: low' (85 tokens per frame) to minimize token consumption and reduce latency to ~5-8s.
        """
        openai_key = os.environ.get("OPENAI_API_KEY") or self.openai_api_key
        if not openai_key:
            logger.warning("OPENAI_API_KEY is not set. OpenAI vision inference skipped.")
            return None

        if not frame_paths:
            logger.warning("No frame paths provided for OpenAI vision analysis.")
            return None

        sample_frames = self._select_evenly_spaced(frame_paths, max_frames=6)
        if not sample_frames:
            return None

        # Check for audio track transcription via Whisper
        audio_info = self.transcribe_audio_openai(audio_path) if audio_path else None
        system_text = prompt or OPENAI_VISION_SYSTEM_PROMPT
        if audio_info and audio_info.get("transcript"):
            dialogue_str = audio_info.get("time_aligned_dialogue") or audio_info.get("transcript")
            lang_str = audio_info.get("language", "English")
            system_text += f"\n\nAUDIO & TIME-ALIGNED DIALOGUE DETECTED IN VIDEO (Language: {lang_str}):\n{dialogue_str}\n\nCRITICAL AUDIO DIRECTIVE:\n- Incorporate the exact spoken words, dialogue timing, lip movement sync, speaker expression, and acoustic mood into the prompt synthesis."

        content_items: List[Dict[str, Any]] = [
            {"type": "text", "text": system_text}
        ]

        percentages = [0, 20, 40, 60, 80, 100]
        valid_frames = 0
        total_sample = len(sample_frames)
        for idx, fpath in enumerate(sample_frames):
            b64_str = self.encode_image_to_base64_jpeg(fpath, max_dim=1024)
            if b64_str:
                pct = percentages[idx] if idx < len(percentages) else int((idx / max(1, total_sample - 1)) * 100)
                content_items.append({
                    "type": "text",
                    "text": f"--- REPRESENTATIVE KEYFRAME {idx + 1} OF {total_sample} [{pct}% Video Progress] ---"
                })
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
            "max_tokens": 4000,
            "temperature": 0.2
        }

        try:
            logger.info("Sending SINGLE OpenAI Vision API request for %d lightweight keyframe images using model '%s'...", valid_frames, model)
            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=40)
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
