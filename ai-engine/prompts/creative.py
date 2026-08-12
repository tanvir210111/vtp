"""
Creative Prompt Generator producing detailed cinematic breakdown prompts.
Outputs structured sections: Overview, Motion & Action, Lighting, Camera, Environment, Character, Continuity & Mood.
"""
from typing import Dict, Any

class CreativePromptBuilder:
    @staticmethod
    def build_creative_prompt(analysis: Dict[str, Any]) -> str:
        """Generate structured cinematic breakdown prompt from Analysis JSON."""
        video_meta = analysis.get("video", {})
        duration = video_meta.get("duration", 10.0)
        
        people_list = analysis.get("people", [])
        person = people_list[0] if people_list else {}
        gender = person.get("gender", "Subject")
        age = person.get("age_group", "")
        clothes = person.get("clothes", "Observed wardrobe")
        accessories = person.get("accessories", "Minimalist accessories")
        position = person.get("position", "Center frame")
        
        objects_list = analysis.get("objects", [])
        objects = ", ".join(objects_list) if objects_list else "scene props"
        
        actions_list = analysis.get("actions", [])
        actions = ", ".join(actions_list) if actions_list else "natural movement"
        
        camera = analysis.get("camera", {})
        framing = camera.get("framing", "Medium Shot")
        angle = camera.get("angle", "Eye Level")
        movement = camera.get("movement", "Slow Tracking Pan")
        lens = camera.get("lens", "35mm prime lens")
        dof = camera.get("depth_of_field", "Shallow depth of field with bokeh")
        
        lighting = analysis.get("lighting", {})
        env_type = lighting.get("environment_type", "Indoor")
        brightness = lighting.get("brightness", "Bright")
        light_source = lighting.get("source", "Natural light")
        temperature = lighting.get("temperature", "Warm")
        light_desc = lighting.get("description", "Soft volumetric lighting")
        
        colors = analysis.get("colors", {})
        color_name = colors.get("name", "Cinematic Grade")
        saturation = colors.get("saturation", "High Saturation")
        contrast = colors.get("contrast", "High Contrast")
        palette_list = colors.get("palette", [])
        palette_str = ", ".join(palette_list) if palette_list else "Natural color tones"
        
        env = analysis.get("environment", {})
        setting = env.get("setting", "Location Setting")
        atmosphere = env.get("atmosphere", "Cinematic visual aesthetic")
        bg = env.get("background", "Background geometry and environment details")
        
        emotions = analysis.get("emotions", {})
        primary_emotion = emotions.get("primary_emotion", "Focused")
        mood_tone = emotions.get("mood_tone", "Cinematic")
        
        summary_text = analysis.get("summary", "")
        summary_str = f"Exact Visual Breakdown: {summary_text}\n" if summary_text else ""

        prompt = f"""[SCENE OVERVIEW & DIRECTED BREAKDOWN]
A master-crafted {duration}s cinematic sequence set in {setting}. {atmosphere}. Color graded in {color_name} style.
{summary_str}
[SUBJECT & CHARACTER BREAKDOWN]
Target Subject: {age} {gender}, positioned at {position}.
Wardrobe & Styling: Wearing {clothes.lower()}, complemented by {accessories.lower()}.
Emotional Disposition: Expression reflecting {primary_emotion} with a {mood_tone} presence.

[MOTION, ACTION & KINETICS]
Observed Actions: The subject is actively engaging in {actions.lower()}.
Key Props & Environment Objects: {objects}. Physical movement exhibits realistic temporal momentum and natural kinetics.

[LIGHTING & ATMOSPHERIC DESIGN]
Illumination Profile: {brightness} {temperature.lower()} {env_type.lower()} key lighting originating from {light_source.lower()}.
Volumetrics & Fill: {light_desc}. Soft shadow falloff and contour highlights.

[CAMERA OPTICS & CINEMATOGRAPHY]
Shot Framing: {framing} shot at {angle}.
Lens Specifications: Filmed on {lens} with {dof.lower()}.
Camera Dynamics: Executing a continuous, fluid {movement} maintaining precise focal tracking on the subject.

[ENVIRONMENT & BACKGROUND GEOMETRY]
Primary Setting: {setting}.
Background Architecture: {bg.lower()}.
Foreground Textures: High surface detail on {objects}, crisp depth separation between subject and surroundings.

[COLOR PALETTE & TEMPORAL CONTINUITY]
Color Style: {color_name} featuring {saturation.lower()} and {contrast.lower()}.
Color Palette: {palette_str}.
Temporal Coherence: High visual consistency, persistent light behavior across frames, hyper-realistic physical mechanics.
"""
        return prompt.strip()
