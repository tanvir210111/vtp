"""
Timeline builder module for converting detected scenes into structured prompt timeline formats.
"""
from typing import List, Dict, Any

class SceneTimelineBuilder:
    @staticmethod
    def build_timeline_json(scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert scene list into structured timeline range labels.
        Example output:
        [
            {"label": "0-3s", "scene_id": 1},
            {"label": "3-8s", "scene_id": 2}
        ]
        """
        timeline = []
        for s in scenes:
            scene_id = s.get("id") or s.get("scene_id") or 1
            start_int = int(round(s.get("start", s.get("start_time", 0.0))))
            end_int = int(round(s.get("end", s.get("end_time", 0.0))))
            
            label = f"{start_int}-{end_int}s"
            timeline.append({
                "label": label,
                "scene_id": scene_id,
                "start": s.get("start", 0.0),
                "end": s.get("end", 0.0),
                "duration": s.get("duration", 0.0)
            })
            
        return timeline

    @staticmethod
    def build_timeline_summary(scenes: List[Dict[str, Any]]) -> str:
        """Format scene cut timeline into structured human readable text."""
        lines = []
        for s in scenes:
            scene_id = s.get("id") or s.get("scene_id") or 1
            start_t = s.get("start", s.get("start_time", 0.0))
            end_t = s.get("end", s.get("end_time", 0.0))
            dur = s.get("duration", round(end_t - start_t, 2))
            
            lines.append(
                f"Scene #{scene_id} [{start_t}s - {end_t}s] (Duration: {dur}s)"
            )
        return "\n".join(lines)
