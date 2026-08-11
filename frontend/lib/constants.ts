import { StylePreset } from "@/types/prompt";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const STYLE_PRESETS: StylePreset[] = [
  {
    id: "standard",
    title: "Standard Timeline",
    description: "Clean, timeline-based (0-2s, 2-5s) scene-by-scene structured prompts for AI video generators.",
    iconName: "Film",
    badge: "Recommended"
  },
  {
    id: "creative",
    title: "Creative Cinematic",
    description: "Detailed cinematic breakdown including motion, camera, lighting, mood, subject, and continuity.",
    iconName: "Sparkles",
    badge: "Cinematic"
  }
];
