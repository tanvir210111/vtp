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
        age = person.get("age_group", "Young Adult")
        clothes = person.get("clothes", "Casual smart attire")
        accessories = person.get("accessories", "Minimalist accessories")
        position = person.get("position", "Center frame")
        
        objects = ", ".join(analysis.get("objects", ["Laptop", "Table"]))
        actions = ", ".join(analysis.get("actions", ["Sitting", "Talking"]))
        
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
        palette_str = ", ".join(colors.get("palette", ["#2563EB", "#7C3AED"]))
        
        env = analysis.get("environment", {})
        setting = env.get("setting", "Modern Studio / Office Workspace")
        atmosphere = env.get("atmosphere", "Professional, clean aesthetic")
        bg = env.get("background", "Softly blurred ambient background")
        
        emotions = analysis.get("emotions", {})
        primary_emotion = emotions.get("primary_emotion", "Happy")
        mood_tone = emotions.get("mood_tone", "Optimistic, energetic, inspiring")
        
        summary_text = analysis.get("summary", "")
        summary_str = f"Summary: {summary_text}\n" if summary_text else ""

        prompt = f"""[SCENE OVERVIEW]
A master-crafted {duration}s cinematic sequence set in {setting}. {atmosphere}. Color graded in {color_name} aesthetic.
{summary_str}
[SUBJECT & CHARACTER BREAKDOWN]
Target Subject: {age} {gender.lower()}, positioned at {position}.
Wardrobe & Styling: Wearing {clothes.lower()}, complemented by {accessories.lower()}.
Emotional Disposition: Expression reflecting {primary_emotion} with a {mood_tone} emotional presence.

[MOTION, ACTION & MICRO-GESTURES]
Primary Actions: The subject is actively engaging in {actions.lower()}.
Interactions & Props: Micro-interactions with props including {objects}. Physical movement exhibits realistic temporal momentum and natural kinetic weight.

[LIGHTING & ATMOSPHERIC DESIGN]
Illumination Profile: {brightness} {temperature.lower()} {env_type.lower()} key lighting originating from {light_source.lower()}.
Volumetrics & Fill: {light_desc}. Soft shadow falloff, accentuating facial geometry and rim lighting around contours.

[CAMERA OPTICS & CINEMATOGRAPHY]
Shot Framing: {framing} shot at {angle}.
Lens Specifications: Filmed on {lens} with {dof.lower()}.
Rig Dynamic: Camera executes a continuous, fluid {movement} maintaining precise focal tracking on the subject.

[ENVIRONMENT, GEOMETRY & BACKGROUND]
Primary Setting: {setting}.
Background Architecture: {bg.lower()}.
Foreground Textures: High surface detail on {objects}, subtle depth separation between subject and surroundings.

[COLOR PALETTE & TEMPORAL CONTINUITY]
Color Grade: {color_name} featuring {saturation.lower()} and {contrast.lower()}.
Key Color Palette Hex: {palette_str}.
Coherence: High temporal consistency, persistent light behavior across all frames, hyper-realistic physical mechanics.
"""
        return prompt.strip()
