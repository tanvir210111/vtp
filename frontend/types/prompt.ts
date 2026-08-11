export type StylePresetId = "standard" | "creative" | "cinematic" | "anime";

export interface StylePreset {
  id: StylePresetId;
  title: string;
  description: string;
  iconName: string;
  badge: string;
}

export type PromptTargetModel = "standard" | "creative" | "midjourney" | "flux" | "sora";
