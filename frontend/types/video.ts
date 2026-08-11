export interface VideoMetadata {
  width: number;
  height: number;
  resolution: string;
  duration_seconds: number;
  fps: number;
  codec: string;
  bitrate: number;
}

export interface VideoTaskState {
  task_id: string;
  filename: string;
  file_size_bytes: number;
  status: "idle" | "uploaded" | "processing" | "completed" | "failed";
  duration_seconds?: number;
  resolution?: string;
  poster_url?: string;
  analysis?: VisualAnalysis;
  prompts?: Record<string, string>;
  created_at?: string;
}

export interface VisualAnalysis {
  subject: string;
  action: string;
  environment: string;
  objects: string[];
  camera: {
    movement: string;
    shot_type: string;
    lens: string;
    framing: string;
  };
  lighting: string;
  colors: {
    name: string;
    hex_codes: string[];
    description: string;
  };
  mood: string;
}
