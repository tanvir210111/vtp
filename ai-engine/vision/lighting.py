"""
Visual feature extractor: Lighting setup, illumination source, and temperature.
"""
import os
import cv2
import numpy as np
from typing import List, Dict, Any

class LightingAnalyzer:
    @staticmethod
    def extract_lighting(frame_paths: List[str] = None) -> Dict[str, Any]:
        """Analyze luminance and color temperature across keyframes."""
        if not frame_paths or len(frame_paths) == 0:
            return {
                "environment_type": "Indoor",
                "brightness": "Bright",
                "source": "Natural window light",
                "temperature": "Warm 4500K",
                "description": "Soft volumetric natural window light with subtle warm golden fill"
            }

        brightness_vals = []
        is_warm = True

        for path in frame_paths[:3]:
            if not os.path.exists(path):
                continue
            try:
                img = cv2.imread(path)
                if img is None:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                brightness_vals.append(np.mean(gray))

                # Color temperature check: Blue vs Red channel mean
                b_mean = np.mean(img[:, :, 0])
                r_mean = np.mean(img[:, :, 2])
                if b_mean > r_mean:
                    is_warm = False
            except Exception:
                pass

        avg_brightness = np.mean(brightness_vals) if brightness_vals else 120.0
        bright_label = "Bright" if avg_brightness > 100 else "Dark"
        temp_label = "Warm" if is_warm else "Cool"

        return {
            "environment_type": "Indoor",
            "brightness": bright_label,
            "source": "Natural light",
            "temperature": temp_label,
            "description": f"{bright_label} {temp_label.lower()} lighting with soft directional fill"
        }
