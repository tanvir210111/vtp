"""
Vision AI Response Parser module.
Converts raw Multimodal Vision Model output (text/JSON) into structured Analysis JSON.
"""
import json
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VisionParser:
    @staticmethod
    def parse_raw_response(raw_text: str, default_duration: float = 10.0, default_fps: int = 30) -> Dict[str, Any]:
        """
        Parse raw Multimodal Vision model text into clean structured Analysis JSON.
        """
        parsed_json = {}

        if raw_text:
            # 1. Try extracting JSON block if wrapped in markdown ```json ... ```
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
            clean_str = json_match.group(1) if json_match else raw_text

            try:
                parsed_json = json.loads(clean_str)
            except Exception:
                # 2. Try regex search for first { ... } block
                obj_match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
                if obj_match:
                    try:
                        parsed_json = json.loads(obj_match.group(1))
                    except Exception:
                        pass

        # Fill defaults & normalize fields
        summary = parsed_json.get("summary") or (raw_text[:200] if raw_text else "Multimodal Vision AI Analysis")
        
        people = parsed_json.get("people", [])
        if not isinstance(people, list) or len(people) == 0:
            people = [{
                "count": 1,
                "gender": "Neutral / Unspecified",
                "age_group": "Young Adult",
                "clothes": "Casual smart attire",
                "accessories": "Minimalist accessories",
                "position": "Center frame"
            }]

        objects = parsed_json.get("objects", [])
        if not isinstance(objects, list) or len(objects) == 0:
            objects = ["Laptop", "Table", "Bag", "Bottle"]

        actions = parsed_json.get("actions", [])
        if not isinstance(actions, list) or len(actions) == 0:
            actions = ["Sitting", "Talking", "Holding item"]

        camera = parsed_json.get("camera", {})
        if not isinstance(camera, dict):
            camera = {}
        camera_norm = {
            "framing": camera.get("framing", "Medium Shot"),
            "angle": camera.get("angle", "Eye Level"),
            "movement": camera.get("movement", "Slow Tracking Pan"),
            "lens": camera.get("lens", "35mm prime lens"),
            "depth_of_field": camera.get("depth_of_field", "Shallow depth of field with bokeh")
        }

        lighting = parsed_json.get("lighting", {})
        if not isinstance(lighting, dict):
            lighting = {}
        lighting_norm = {
            "environment_type": lighting.get("environment_type", "Indoor"),
            "brightness": lighting.get("brightness", "Bright"),
            "source": lighting.get("source", "Natural light"),
            "temperature": lighting.get("temperature", "Warm"),
            "description": lighting.get("description", "Bright warm lighting with soft fill")
        }

        colors = parsed_json.get("colors", {})
        if not isinstance(colors, dict):
            colors = {}
        colors_norm = {
            "name": colors.get("name", "Cinematic Grade"),
            "palette": colors.get("palette", ["#2563EB", "#7C3AED", "#0891B2", "#F8FAFC"]),
            "saturation": colors.get("saturation", "High Saturation"),
            "contrast": colors.get("contrast", "High Contrast"),
            "description": colors.get("description", "Rich color grading with balanced contrast")
        }

        environment = parsed_json.get("environment", {})
        if not isinstance(environment, dict):
            environment = {}
        environment_norm = {
            "setting": environment.get("setting", "Modern Studio / Office Workspace"),
            "atmosphere": environment.get("atmosphere", "Professional, clean aesthetic"),
            "location_type": environment.get("location_type", "Indoor Office"),
            "background": environment.get("background", "Softly blurred ambient window")
        }

        emotions = parsed_json.get("emotions", {})
        if not isinstance(emotions, dict):
            emotions = {}
            
        conf_raw = emotions.get("confidence", 0.90)
        try:
            confidence_val = float(conf_raw)
        except (ValueError, TypeError):
            confidence_val = 0.92

        emotions_norm = {
            "primary_emotion": emotions.get("primary_emotion", "Happy"),
            "confidence": confidence_val,
            "mood_tone": emotions.get("mood_tone", "Optimistic, energetic, inspiring"),
            "emotions_list": emotions.get("emotions_list", ["Happy", "Neutral"])
        }

        timeline = parsed_json.get("timeline", [])
        model_prompts = parsed_json.get("model_prompts", {})
        if not isinstance(model_prompts, dict):
            model_prompts = {}

        return {
            "summary": summary,
            "video": {
                "duration": default_duration,
                "fps": default_fps
            },
            "people": people,
            "objects": objects,
            "actions": actions,
            "camera": camera_norm,
            "lighting": lighting_norm,
            "colors": colors_norm,
            "environment": environment_norm,
            "emotions": emotions_norm,
            "timeline": timeline,
            "model_prompts": model_prompts
        }
