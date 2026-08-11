"""
Multimodal Vision Model Manager & Inference Engine.
Supports Google Gemini Native Video File Upload API & Image Keyframe API.
Synthesizes model-tailored hyper-accurate prompts for Veo, Sora, Midjourney v6, Flux.1, and Kling AI.
"""
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
    import google.generativeai as legacy_genai
    HAS_LEGACY_GENAI = True
except ImportError:
    HAS_LEGACY_GENAI = False

try:
    from config.settings import settings as backend_settings
except Exception:
    backend_settings = None

logger = logging.getLogger(__name__)


def _load_backend_dotenv_key() -> str:
    """Load GEMINI_API_KEY from backend/.env without exposing it in logs or responses."""
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env"))
    if not os.path.exists(env_path):
        return ""

    with open(env_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == "GEMINI_API_KEY":
                return value.strip().strip('"').strip("'")
    return ""


class ModelLoader:
    def __init__(self, model_name: str = "gemini-3.5-flash"):
        self.model_name = model_name
        self.last_diagnostic: Dict[str, Any] = {}

        configured_key = os.environ.get("GEMINI_API_KEY", "")
        if not configured_key and backend_settings is not None:
            configured_key = getattr(backend_settings, "GEMINI_API_KEY", "") or ""
        if not configured_key:
            configured_key = _load_backend_dotenv_key()
        if configured_key:
            os.environ["GEMINI_API_KEY"] = configured_key

        self.gemini_api_key = configured_key
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        """Check for presence only; Google AI Studio now uses several valid key formats."""
        key = os.environ.get("GEMINI_API_KEY") or self.gemini_api_key
        if not key:
            logger.error("GEMINI_API_KEY is not set. Vision inference cannot start.")
        else:
            logger.info("GEMINI_API_KEY loaded from backend/.env or the runtime environment.")

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

    def _format_exception(self, exc: Exception) -> Dict[str, Any]:
        response = getattr(exc, "response", None)
        return {
            "message": str(exc),
            "status_code": getattr(exc, "status_code", None) or getattr(response, "status_code", None),
            "response_text": getattr(response, "text", None),
        }

    def test_gemini_connection(self, model_name: str = "gemini-2.5-flash") -> Dict[str, Any]:
        """Run a minimal Gemini request to verify the configured key works and capture the exact error if it doesn't."""
        gemini_key = os.environ.get("GEMINI_API_KEY") or self.gemini_api_key
        diagnostic: Dict[str, Any] = {
            "authentication_method": "Google AI Studio API key via google.genai.Client(api_key=...)",
            "model": model_name,
            "vision_inference_ran": False,
            "fallback_used": False,
        }

        if not gemini_key:
            diagnostic.update({"ok": False, "error": "GEMINI_API_KEY is not set"})
            self.last_diagnostic = diagnostic
            return diagnostic

        if not HAS_GENAI_SDK:
            diagnostic.update({"ok": False, "error": "google-genai SDK is not installed"})
            self.last_diagnostic = diagnostic
            return diagnostic

        try:
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model=model_name,
                contents="Reply with one short sentence confirming the Gemini API works.",
            )
            text = getattr(response, "text", None) or ""
            diagnostic.update({"ok": bool(text), "response_preview": text[:200], "error": None})
            if text:
                diagnostic["vision_inference_ran"] = True
            self.last_diagnostic = diagnostic
            return diagnostic
        except Exception as exc:
            diagnostic.update({"ok": False, "error": self._format_exception(exc)})
            self.last_diagnostic = diagnostic
            return diagnostic

    def analyze_frames_vision_model(
        self,
        frame_paths: Optional[List[str]] = None,
        video_path: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> str:
        """Authenticate with Gemini using the current Google AI Studio flow, then analyze frames."""
        gemini_key = os.environ.get("GEMINI_API_KEY") or self.gemini_api_key
        diagnostic: Dict[str, Any] = {
            "authentication_method": "Google AI Studio API key via google.genai.Client(api_key=...)",
            "model": self.model_name,
            "vision_inference_ran": False,
            "fallback_used": False,
        }

        if not gemini_key:
            diagnostic.update({"ok": False, "error": "GEMINI_API_KEY is not set"})
            self.last_diagnostic = diagnostic
            raise RuntimeError(json.dumps(diagnostic, default=str))

        if not HAS_GENAI_SDK:
            diagnostic.update({"ok": False, "error": "google-genai SDK is not installed"})
            self.last_diagnostic = diagnostic
            raise RuntimeError(json.dumps(diagnostic, default=str))

        try:
            client = genai.Client(api_key=gemini_key)
            probe = client.models.generate_content(
                model=self.model_name,
                contents="Reply with one short sentence confirming authentication works.",
            )
            probe_text = getattr(probe, "text", None) or ""
            if not probe_text:
                diagnostic.update({"ok": False, "error": "Gemini auth probe returned no content"})
                self.last_diagnostic = diagnostic
                raise RuntimeError(json.dumps(diagnostic, default=str))
        except Exception as exc:
            diagnostic.update({"ok": False, "error": self._format_exception(exc)})
            self.last_diagnostic = diagnostic
            raise RuntimeError(json.dumps(diagnostic, default=str)) from exc

        diagnostic.update({"ok": True, "response_preview": probe_text[:200], "error": None})
        self.last_diagnostic = diagnostic

        analysis_prompt = prompt or (
            "You are a world-class AI Video Prompt Engineer & Director of Photography (specialized in Google Veo, OpenAI Sora, Midjourney v6, Flux.1, Kling AI, Luma Dream Machine, and Runway Gen-3).\n"
            "Examine this video/frame sequence in extreme technical detail. Perform an exhaustive visual reverse-engineering analysis across ALL 11 dimensions:\n"
            "1. Subjects (demographics, count, spatial layout, posture)\n"
            "2. Objects (materials, surface textures, exact placements)\n"
            "3. Actions (primary movements & physical kinetics)\n"
            "4. Ambience (environmental atmosphere, spatial vibe, setting)\n"
            "5. Wardrobe (outfit style, fabrics, garments, optical accessories)\n"
            "6. Micro-gestures (facial expressions, eye focus, hand gestures)\n"
            "7. Lighting Direction & Temperature (key/fill/rim sources, Kelvin temp, volumetric rays, shadow falloff)\n"
            "8. Optics (lens focal length e.g. 35mm/50mm f/1.4, optical distortion, sensor grade)\n"
            "9. Depth of Field (focal plane separation, background bokeh quality)\n"
            "10. Background Geometry (architectural layout, depth layers, background details)\n"
            "11. Color Palettes (color grade style, hex palette, saturation, contrast ratio)\n\n"
            "MANDATORY PROMPT GENERATION DIRECTIVE:\n"
            "- Do NOT use template placeholders or short single-sentence descriptions.\n"
            "- Each generated prompt in 'model_prompts' MUST be fully written out as a complete, multi-sentence, highly descriptive visual prompt (80-200 words per model prompt).\n"
            "- Tailor each prompt to the target AI model capabilities (Google Veo, OpenAI Sora, Midjourney v6, Flux.1, Kling AI, Runway Gen-3, Luma Dream Machine).\n\n"
            "Return ONLY a valid JSON object matching this exact structure:\n"
            "{\n"
            '  "summary": "Exhaustive multi-sentence visual summary of the scene, action, subject, and atmosphere",\n'
            '  "people": [{"count": 1, "gender": "Male/Female/Neutral", "age_group": "Young Adult/Adult/etc.", "clothes": "Detailed outfit, fabric, style", "accessories": "Items, jewellery, optical glasses", "position": "Exact spatial placement"}],\n'
            '  "objects": ["specific detailed object 1 with material/texture", "object 2", "object 3"],\n'
            '  "actions": ["precise physical movement 1", "micro-gesture 2"],\n'
            '  "camera": {"framing": "Medium Shot", "angle": "Eye Level", "movement": "Slow Pan", "lens": "35mm prime lens f/1.4", "depth_of_field": "Shallow depth of field with creamy bokeh"},\n'
            '  "lighting": {"environment_type": "Indoor/Outdoor", "brightness": "Softly lit", "source": "Volumetric sunlight", "temperature": "Warm 3200K", "description": "Detailed lighting breakdown with direction and shadow fill"},\n'
            '  "colors": {"name": "Cinematic Grade", "palette": ["#2563EB", "#7C3AED", "#F59E0B"], "saturation": "High", "contrast": "High contrast", "description": "Color grading breakdown"},\n'
            '  "environment": {"setting": "Exact location setting", "atmosphere": "Rich atmosphere & vibe", "location_type": "Indoor/Outdoor", "background": "Detailed background geometry & architecture"},\n'
            '  "emotions": {"primary_emotion": "Focused", "confidence": 0.98, "mood_tone": "Cinematic", "emotions_list": ["Focused", "Confident"]},\n'
            '  "model_prompts": {\n'
            '     "veo": "Complete 80-200 word prompt for Google Veo video generation detailing narrative, camera dynamic, lighting, subject action, 4K quality.",\n'
            '     "sora": "Complete 80-200 word prompt for OpenAI Sora detailing physical dynamics, temporal coherence, camera rig, subject movement, 60fps photorealism.",\n'
            '     "midjourney": "Ultra-detailed visual prompt for Midjourney v6 describing subject, wardrobe, micro-gestures, environment, lighting, lens parameters --ar 16:9 --v 6.0 --style raw --stylize 250",\n'
            '     "flux": "Detailed photorealistic description for Flux.1 with micro-textures, volumetric illumination, color grading hex, focal distance.",\n'
            '     "kling": "Detailed video prompt for Kling AI structured into [Camera Movement], [Subject & Action], [Lighting & Atmosphere], [Setting] sections.",\n'
            '     "runway": "Ultra-fluid prompt for Runway Gen-3 Alpha with camera velocity, motion guidance, and depth of field.",\n'
            '     "luma": "Hyper-realistic prompt for Luma Dream Machine highlighting smooth transitions, volumetric lighting, and physical consistency."\n'
            '  }\n'
            "}"
        )

        # Run Google Gemini multimodal inference directly with the current SDK flow.
        if frame_paths and gemini_key:
            try:
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
                        contents=[analysis_prompt, *pil_images],
                    )
                    text = getattr(response, "text", None) or ""
                    if text:
                        diagnostic.update({"vision_inference_ran": True, "fallback_used": False, "error": None})
                        self.last_diagnostic = diagnostic
                        logger.info("Gemini multimodal vision inference completed successfully.")
                        return text
                    raise RuntimeError("Gemini returned an empty response")
            except Exception as exc:
                diagnostic.update({"vision_inference_ran": False, "fallback_used": False, "error": self._format_exception(exc)})
                self.last_diagnostic = diagnostic
                logger.error("Gemini multimodal vision inference failed: %s", exc)
                raise RuntimeError(json.dumps(diagnostic, default=str)) from exc

        diagnostic.update({"vision_inference_ran": False, "fallback_used": False, "error": "No frame paths were provided for Gemini vision inference"})
        self.last_diagnostic = diagnostic
        raise RuntimeError(json.dumps(diagnostic, default=str))
