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
        
        people_list = analysis.get("people", [])
        person = people_list[0] if people_list else {}
        people_desc = f"{person.get('count', 1)} person ({person.get('age_group', 'Young Adult')})"
        
        actions = ", ".join(analysis.get("actions", ["Standing", "Talking"]))
        objects = ", ".join(analysis.get("objects", ["Laptop", "Table"]))
        
        camera = analysis.get("camera", {})
        cam_framing = camera.get("framing", "Medium Shot")
        cam_angle = camera.get("angle", "Eye Level")
        cam_move = camera.get("movement", "Static / Tracking")
        
        lighting = analysis.get("lighting", {})
        light_desc = f"{lighting.get('brightness', 'Bright')} {lighting.get('temperature', 'Warm')} lighting"
        
        env = analysis.get("environment", {})
        env_desc = env.get("setting", "Detailed location setting")
        
        timeline_items = analysis.get("timeline", [])
        if not timeline_items:
            # Fallback 3-segment timeline
            t1 = min(3.0, round(duration * 0.3, 1))
            t2 = min(7.0, round(duration * 0.7, 1))
            timeline_items = [
                {"label": f"0-{int(t1)}s", "scene_id": 1},
                {"label": f"{int(t1)}-{int(t2)}s", "scene_id": 2},
                {"label": f"{int(t2)}-{int(duration)}s", "scene_id": 3}
            ]
            
        blocks = []
        for idx, item in enumerate(timeline_items):
            label = item.get("label", f"Scene {idx+1}")
            if idx == 0:
                block = f"{label}\n\n[Framing & Camera]: {cam_framing}, {cam_angle}\n[Setting & Light]: {env_desc} with {light_desc}\n[Subject & Action]: {people_desc}, {actions}\n[Objects]: {objects}"
            elif idx == 1:
                block = f"{label}\n\n[Framing & Camera]: {cam_framing}, {cam_move}\n[Action Dynamics]: Continuous {actions.lower()}\n[Visual Tone]: High quality cinematic focus on {objects}"
            else:
                block = f"{label}\n\n[Framing & Camera]: Close-up reaction shot\n[Setting]: {env_desc}\n[Resolution & Finish]: Crisp focal detail, smooth temporal resolution fade"
                
            blocks.append(block)
            
        return "\n\n---\n\n".join(blocks)
