"""
Content-aware scene boundary detector using PySceneDetect (primary) and OpenCV Histogram Difference (fallback).
"""
import os
import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class SceneDetector:
    def __init__(self, threshold: float = 27.0):
        self.threshold = threshold

    def detect_scenes(
        self,
        video_path: str,
        frame_paths: Optional[List[str]] = None,
        video_duration: float = 10.0
    ) -> Dict[str, Any]:
        """
        Detect scene boundaries in a video file or frame list.
        Tries PySceneDetect first, falls back to OpenCV histogram difference.
        """
        if not video_path or not os.path.exists(video_path):
            return self._build_single_scene(video_duration, frame_paths)

        # 1. Try PySceneDetect (Primary)
        try:
            scenes = self._detect_pyscenedetect(video_path, frame_paths)
            if scenes and len(scenes) > 0:
                return {
                    "scene_count": len(scenes),
                    "scenes": scenes
                }
        except Exception as e:
            logger.info(f"PySceneDetect boundary detection fallback: {e}")

        # 2. Try OpenCV Histogram Difference (Fallback)
        try:
            scenes = self._detect_opencv_histogram(video_path, frame_paths, video_duration)
            if scenes and len(scenes) > 0:
                return {
                    "scene_count": len(scenes),
                    "scenes": scenes
                }
        except Exception as e:
            logger.warning(f"OpenCV histogram scene detection fallback: {e}")

        # 3. Final Fallback: Single Scene
        return self._build_single_scene(video_duration, frame_paths)

    def _detect_pyscenedetect(self, video_path: str, frame_paths: Optional[List[str]]) -> List[Dict[str, Any]]:
        from scenedetect import detect, ContentDetector
        
        scene_list = detect(video_path, ContentDetector(threshold=self.threshold))
        if not scene_list:
            return []
            
        scenes = []
        for i, (start_time, end_time) in enumerate(scene_list, start=1):
            start_sec = round(start_time.get_seconds(), 2)
            end_sec = round(end_time.get_seconds(), 2)
            dur_sec = round(end_sec - start_sec, 2)
            
            thumb_path = self._select_thumbnail_frame(start_sec, end_sec, frame_paths, i)
            
            scenes.append({
                "id": i,
                "start": start_sec,
                "end": end_sec,
                "duration": max(0.1, dur_sec),
                "thumbnail": thumb_path
            })
            
        return scenes

    def _detect_opencv_histogram(
        self,
        video_path: str,
        frame_paths: Optional[List[str]],
        video_duration: float
    ) -> List[Dict[str, Any]]:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return []
            
        fps = float(cap.get(cv2.CAP_PROP_FPS)) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        actual_duration = round(total_frames / fps, 2) if (fps > 0 and total_frames > 0) else video_duration
        
        cuts = [0.0]
        prev_hist = None
        frame_idx = 0
        step = max(1, int(fps * 0.25))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_idx % step == 0:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
                cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                
                if prev_hist is not None:
                    comp = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                    if comp < 0.50:
                        cut_sec = round(frame_idx / fps, 2)
                        if cut_sec > cuts[-1] + 0.4:
                            cuts.append(cut_sec)
                            
                prev_hist = hist
            frame_idx += 1
            
        cap.release()
        
        scenes = []
        for i in range(len(cuts)):
            start_sec = cuts[i]
            end_sec = cuts[i + 1] if i + 1 < len(cuts) else actual_duration
            dur_sec = round(end_sec - start_sec, 2)
            
            thumb_path = self._select_thumbnail_frame(start_sec, end_sec, frame_paths, i + 1)
            
            scenes.append({
                "id": i + 1,
                "start": start_sec,
                "end": end_sec,
                "duration": max(0.1, dur_sec),
                "thumbnail": thumb_path
            })
            
        return scenes

    def _build_single_scene(self, video_duration: float, frame_paths: Optional[List[str]]) -> Dict[str, Any]:
        thumb_path = frame_paths[0] if (frame_paths and len(frame_paths) > 0) else "scene_1.jpg"
        return {
            "scene_count": 1,
            "scenes": [
                {
                    "id": 1,
                    "start": 0.0,
                    "end": round(video_duration, 2),
                    "duration": round(video_duration, 2),
                    "thumbnail": thumb_path
                }
            ]
        }

    def _select_thumbnail_frame(
        self,
        start_sec: float,
        end_sec: float,
        frame_paths: Optional[List[str]],
        scene_idx: int
    ) -> str:
        if not frame_paths or len(frame_paths) == 0:
            return f"scene_{scene_idx}.jpg"
            
        mid_time = (start_sec + end_sec) / 2.0
        idx = min(len(frame_paths) - 1, max(0, int(mid_time // 1.5)))
        return frame_paths[idx]
