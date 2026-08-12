"""
Standard Prompt Generator producing clean, timeline-based, scene-by-scene prompts for AI video generation models.
"""
from typing import Dict, Any, List

class StandardPromptBuilder:
    @staticmethod
    def build_prompt(analysis: Dict[str, Any]) -> str:
        """Generate timeline-based, structured scene-by-scene prompt from Analysis JSON."""
        video_meta = analysis.get("video", {})
        duration = float(video_meta.get("duration", 10.0))
        summary = analysis.get("summary", "")
        
        people_list = analysis.get("people", [])
        person = people_list[0] if people_list else {}
        gender = person.get("gender", "subject")
        age = person.get("age_group", "")
        clothes = person.get("clothes", "")
        
        person_desc = f"{age} {gender}".strip() or "subject"
        if clothes and clothes.lower() not in ["n/a", "none"]:
            person_desc += f" (wearing {clothes})"
            
        actions_list = analysis.get("actions", [])
        actions = ", ".join(actions_list) if actions_list else "observed movement"
        
        objects_list = analysis.get("objects", [])
        objects = ", ".join(objects_list) if objects_list else "scene elements"
        
        camera = analysis.get("camera", {})
        cam_framing = camera.get("framing", "Medium Shot")
        cam_angle = camera.get("angle", "Eye Level")
        cam_move = camera.get("movement", "Static / Tracking")
        
        lighting = analysis.get("lighting", {})
        light_desc = lighting.get("description") or f"{lighting.get('brightness', 'Bright')} {lighting.get('temperature', 'Warm')} lighting sourced from {lighting.get('source', 'environment')}"
        
        colors = analysis.get("colors", {})
        color_tone = f"{colors.get('name', 'Cinematic')} palette ({', '.join(colors.get('palette', []))})"
        
        env = analysis.get("environment", {})
        env_desc = env.get("setting", "location setting")
        
        timeline_items = analysis.get("timeline", [])
        if not timeline_items:
            t1 = min(3.0, round(duration * 0.3, 1))
            t2 = min(7.0, round(duration * 0.7, 1))
            timeline_items = [
                {"label": f"0-{int(t1)}s (Opening Scene)", "scene_id": 1},
                {"label": f"{int(t1)}-{int(t2)}s (Main Action)", "scene_id": 2},
                {"label": f"{int(t2)}-{int(duration)}s (Climax & Resolution)", "scene_id": 3}
            ]
            
        blocks = []
        for idx, item in enumerate(timeline_items):
            label = item.get("label", f"Scene {idx+1}")
            if idx == 0:
                block = f"⏱️ [{label}]\n• Framing & Camera: {cam_framing}, {cam_angle}\n• Environment & Setting: {env_desc}\n• Subject & Wardrobe: {person_desc}\n• Initial Action: {actions}\n• Illumination & Tone: {light_desc}"
            elif idx == 1:
                block = f"⏱️ [{label}]\n• Camera Dynamics: {cam_move}\n• Action Progression: Subject performing {actions} interacting with {objects}\n• Color Grading: {color_tone}\n• Motion Coherence: Smooth temporal kinetics"
            else:
                block = f"⏱️ [{label}]\n• Framing: Close-up / Detailed focal resolution\n• Setting Details: {env_desc}\n• Resolution: Finalizing movement in {actions.lower()}, maintaining exact lighting and photorealistic consistency"
                
            blocks.append(block)
            
        header = f"🎬 STANDARD TIMELINE PROMPT ({duration}s Video Clip)\n"
        if summary:
            header += f"Exact Visual Summary: {summary}\n\n"
            
        return header + "\n\n---\n\n".join(blocks)
