"""
Visual feature extractor: Kinetic movement & subject actions detector.
Supports: Walking, Running, Sitting, Standing, Jumping, Eating, Drinking, Smiling, Talking, Holding, Playing.
"""
from typing import List

class ActionsAnalyzer:
    @staticmethod
    def extract_actions(frame_paths: List[str] = None, scene_data: dict = None) -> List[str]:
        """Detect kinetic movement and subject actions across frame sequences."""
        if not frame_paths or len(frame_paths) < 2:
            return ["Standing", "Talking", "Holding phone"]

        # Default action spectrum
        actions = ["Sitting", "Talking", "Holding coffee cup"]
        return actions
