"""
Main orchestrator pipeline for Video-to-Prompt AI analysis engine.
Integrates Phase 1 (Frame Extractor), Phase 2 (Scene Detection), Phase 3 (Vision Analysis), Phase 4 (Prompt Generator).
"""
import os
import time
import logging
from typing import Dict, Any

from frame_extractor.extract import FrameExtractor
from frame_extractor.thumbnail import ThumbnailGenerator
from scene_detector.detect import SceneDetector
from scene_detector.timeline import SceneTimelineBuilder
from vision.analyzer import VisionAnalyzer
from prompts.standard import StandardPromptBuilder
from prompts.creative import CreativePromptBuilder
from prompts.formatter import PromptFormatter

logger = logging.getLogger(__name__)

class VideoToPromptPipeline:
    def __init__(self, storage_dir: str = "../storage", output_dir: str = "../output"):
        self.storage_dir = os.path.abspath(storage_dir)
        self.output_dir = os.path.abspath(output_dir)
        
        self.frame_extractor = FrameExtractor()
        self.scene_detector = SceneDetector()
        self.vision_analyzer = VisionAnalyzer()

    def run(
        self,
        task_id: str,
        video_path: str,
        style_preset: str = "standard",
        scene_threshold: float = 0.35
    ) -> Dict[str, Any]:
        """Execute end-to-end video processing and prompt generation pipeline."""
        start_time = time.time()
        
        frames_dir = os.path.join(self.storage_dir, "frames", task_id)
        thumbnails_dir = os.path.join(self.storage_dir, "thumbnails")
        poster_path = os.path.join(thumbnails_dir, f"{task_id}.jpg")
        
        # Step 1: Extract frames & metadata
        extraction_result = self.frame_extractor.process(video_path, frames_dir, interval_sec=1.5)
        metadata = extraction_result["metadata"]
        frame_paths = extraction_result["frame_paths"]
        
        # Step 2: Generate thumbnail poster
        ThumbnailGenerator.generate_poster(frame_paths, poster_path)
        
        # Step 3: Detect scene boundaries & build timeline
        scene_result = self.scene_detector.detect_scenes(
            video_path, frame_paths=frame_paths, video_duration=metadata["duration_seconds"]
        )
        scenes = scene_result.get("scenes", [])
        timeline = SceneTimelineBuilder.build_timeline_json(scenes)
        
        # Step 4: Vision Feature Analysis (Assembles complete Analysis JSON)
        analysis = self.vision_analyzer.analyze(
            frame_paths=frame_paths,
            video_path=video_path,
            metadata=metadata,
            scenes=scenes,
            timeline=timeline,
            style_preset=style_preset
        )
        
        # Step 5: Synthesize Prompts (Standard Timeline + Creative Cinematic + Target AI Models)
        standard_prompt = StandardPromptBuilder.build_prompt(analysis)
        creative_prompt = CreativePromptBuilder.build_creative_prompt(analysis)

        ai_model_prompts = analysis.get("model_prompts", {})

        # Extract comprehensive vision analysis tokens
        summary_val = analysis.get("summary", "")
        subj_str = ", ".join(analysis.get("objects", ["subject"]))
        action_str = ", ".join(analysis.get("actions", ["movement"]))
        
        env_dict = analysis.get("environment", {})
        env_setting = env_dict.get("setting", "detailed location setting")
        env_bg = env_dict.get("background", "softly blurred ambient background")
        env_atmosphere = env_dict.get("atmosphere", "cinematic atmosphere")
        
        cam_dict = analysis.get("camera", {})
        cam_framing = cam_dict.get("framing", "Medium Shot")
        cam_angle = cam_dict.get("angle", "Eye Level")
        cam_move = cam_dict.get("movement", "Slow Pan")
        cam_lens = cam_dict.get("lens", "35mm prime lens")
        cam_dof = cam_dict.get("depth_of_field", "shallow depth of field with bokeh")

        light_dict = analysis.get("lighting", {})
        light_bright = light_dict.get("brightness", "Bright")
        light_temp = light_dict.get("temperature", "Warm")
        light_src = light_dict.get("source", "Natural light")
        light_desc = light_dict.get("description", "cinematic volumetric lighting with soft fill")

        colors_dict = analysis.get("colors", {})
        color_grade = colors_dict.get("name", "Cinematic Grade")
        color_palette = ", ".join(colors_dict.get("palette", ["#2563EB", "#7C3AED"]))

        people_list = analysis.get("people", [])
        if people_list:
            p = people_list[0]
            person_str = f"a {p.get('age_group', 'Young Adult')} {p.get('gender', 'person')}"
            clothes_str = f"wearing {p.get('clothes', 'stylish attire')}"
            pos_str = f"positioned in {p.get('position', 'center frame')}"
        else:
            person_str = "a subject"
            clothes_str = "in clean contemporary outfit"
            pos_str = "in center frame"

        emo_dict = analysis.get("emotions", {})
        emotion_str = emo_dict.get("primary_emotion", "confident")
        mood_str = emo_dict.get("mood_tone", "cinematic")

        facial_expr = emo_dict.get("facial_expression", "")
        eye_gaze = p.get("eye_gaze", "") if people_list else ""
        body_posture = p.get("body_posture", "") if people_list else ""
        hand_gestures = p.get("hand_gestures", "") if people_list else ""

        enrichment_suffix = (
            f"Subject: {person_str}, {clothes_str}, positioned at {pos_str}. "
            f"Facial expression: {emotion_str} ({facial_expr}). Eye direction: {eye_gaze}. Body posture: {body_posture}. Hand gestures: {hand_gestures}. "
            f"Action dynamics: {action_str} with {subj_str}. Environment: {env_setting}, background showcasing {env_bg}, atmosphere: {env_atmosphere}. "
            f"Shot in {cam_framing} at {cam_angle} on a {cam_lens} with {cam_dof}. Camera movement: {cam_move}. "
            f"Lighting: {light_bright} {light_temp.lower()} light from {light_src} ({light_desc}). Color grading: {color_grade} ({color_palette})."
        )

        def _ensure_rich(prompt_str: Optional[str], default_str: str) -> str:
            if not prompt_str or len(prompt_str.split()) < 50:
                if prompt_str:
                    return f"{prompt_str.strip()} {enrichment_suffix.strip()}"
                return default_str
            return prompt_str

        mj_prompt = _ensure_rich(
            ai_model_prompts.get("midjourney"),
            f"Hyper-photorealistic 8k film still of {person_str}, {clothes_str}, {pos_str}. Facial expression: {emotion_str} ({facial_expr}). Eye direction: {eye_gaze}. Posture: {body_posture}. Hand gestures: {hand_gestures}. Actively {action_str} in a {env_setting}. Foreground: {subj_str}, background: {env_bg}. Atmosphere: {env_atmosphere}, mood: {mood_str}. Shot in {cam_framing} from {cam_angle} on a {cam_lens}, {cam_dof}. {light_bright} {light_temp.lower()} lighting sourced from {light_src}, {light_desc}. Color graded in {color_grade} ({color_palette}) --ar 16:9 --v 6.0 --style raw --stylize 250"
        )

        flux_prompt = _ensure_rich(
            ai_model_prompts.get("flux"),
            f"High dynamic range photorealistic film still of {person_str} {clothes_str} performing {action_str} inside {env_setting}. Expression: {emotion_str} ({facial_expr}), gaze: {eye_gaze}, posture: {body_posture}. Crisp micro-textures on {subj_str}, background architecture: {env_bg}. {light_bright} volumetric ray lighting from {light_src}, soft shadow falloff. Captured with {cam_lens} in {cam_framing}, color graded in {color_grade} palette ({color_palette}). Ultra crisp 8k focal clarity."
        )

        sora_prompt = _ensure_rich(
            ai_model_prompts.get("sora"),
            f"Continuous 60fps ultra-realistic video sequence of {person_str} {clothes_str} engaged in {action_str} in {env_setting}. Facial expression: {emotion_str} ({facial_expr}), eye gaze: {eye_gaze}, posture: {body_posture}, gestures: {hand_gestures}. Camera moves in smooth {cam_move} from {cam_framing} at {cam_angle}. Physical collision dynamics with {subj_str}, illuminated by {light_bright} {light_temp.lower()} light ({light_desc}). Strong temporal coherence, photorealistic fluid mechanics, {mood_str} mood."
        )

        veo_prompt = _ensure_rich(
            ai_model_prompts.get("veo"),
            f"Cinematic 4k video sequence of {person_str} {clothes_str} {action_str} at {env_setting}. Facial expression: {emotion_str} ({facial_expr}), eye gaze: {eye_gaze}, posture: {body_posture}. Filmed in {cam_framing} using {cam_lens} with dynamic {cam_move}. Volumetric illumination with {light_desc}, rich {color_grade} color grading ({color_palette}), depth of field: {cam_dof}, smooth physical motion."
        )

        kling_prompt = _ensure_rich(
            ai_model_prompts.get("kling"),
            f"[Camera Movement]: {cam_move} from {cam_framing}. "
            f"[Subject & Action]: {person_str} {clothes_str} {action_str} with {subj_str}. Expression: {emotion_str} ({facial_expr}), gaze: {eye_gaze}, posture: {body_posture}. "
            f"[Lighting & Atmosphere]: {light_desc}, {env_atmosphere}. "
            f"[Setting]: {env_setting}. [Color Tone]: {color_grade} ({color_palette})."
        )

        runway_prompt = _ensure_rich(
            ai_model_prompts.get("runway"),
            f"Cinematic video clip of {person_str} {clothes_str} {action_str} in {env_setting}. Expression: {emotion_str} ({facial_expr}), eye direction: {eye_gaze}, posture: {body_posture}. Camera motion: smooth {cam_move}, {cam_framing}, {cam_lens}. Volumetric lighting from {light_src}, {color_grade} color grading, 4k 60fps, photorealistic consistency."
        )

        luma_prompt = _ensure_rich(
            ai_model_prompts.get("luma"),
            f"Hyper-realistic 4k video shot: {person_str} {clothes_str} performing {action_str} set in {env_setting}. Expression: {emotion_str} ({facial_expr}), posture: {body_posture}, gestures: {hand_gestures}. Dynamic camera work: {cam_move}, {cam_framing}. Soft volumetric lighting, {color_grade} color scheme, smooth motion dynamics."
        )

        all_prompts = {
            "standard": standard_prompt,
            "creative": creative_prompt,
            "midjourney": mj_prompt,
            "flux": flux_prompt,
            "sora": sora_prompt,
            "veo": veo_prompt,
            "kling": kling_prompt,
            "runway": runway_prompt,
            "luma": luma_prompt
        }
        
        # Step 6: Format & Save Reports (TXT, JSON, MD)
        task_output_dir = os.path.join(self.output_dir, "txt")
        os.makedirs(task_output_dir, exist_ok=True)
        txt_path = os.path.join(task_output_dir, f"{task_id}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(PromptFormatter.to_txt(all_prompts))
            
        md_output_dir = os.path.join(self.output_dir, "markdown")
        os.makedirs(md_output_dir, exist_ok=True)
        md_path = os.path.join(md_output_dir, f"{task_id}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(PromptFormatter.to_markdown(task_id, analysis, all_prompts))
            
        json_output_dir = os.path.join(self.output_dir, "json")
        os.makedirs(json_output_dir, exist_ok=True)
        json_path = os.path.join(json_output_dir, f"{task_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(PromptFormatter.to_json(task_id, analysis, all_prompts))
            
        processing_time = round(time.time() - start_time, 2)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "processing_time_sec": processing_time,
            "metadata": metadata,
            "poster_url": f"/storage/thumbnails/{task_id}.jpg",
            "scene_data": scene_result,
            "timeline": timeline,
            "analysis": analysis,
            "prompts": all_prompts,
            "frame_paths": frame_paths
        }
