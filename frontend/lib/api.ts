import { API_BASE_URL } from "./constants";

export async function uploadVideoApi(file: File): Promise<any> {
  console.log("[PIPELINE] upload:start", file.name, `${(file.size / (1024 * 1024)).toFixed(2)}MB`);
  const formData = new FormData();
  formData.append("video", file);
  formData.append("file", file);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s upload timeout

  try {
    const res = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ message: "Upload failed" }));
      console.error("[PIPELINE] upload:failed errorData:", errorData);
      throw new Error(errorData.message || errorData.detail || "Video upload failed on backend.");
    }

    const data = await res.json();
    console.log("[PIPELINE] upload:complete", data);
    return data;
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") {
      console.error("[PIPELINE] upload:timeout (>30s)");
      throw new Error("Video upload timed out after 30 seconds. Please try a smaller video clip.");
    }
    throw err;
  }
}

function normalizeStylePreset(stylePreset: string): string {
  if (stylePreset === "cinematic" || stylePreset === "anime") {
    return "creative";
  }
  if (stylePreset !== "standard" && stylePreset !== "creative") {
    return "standard";
  }
  return stylePreset;
}

export async function generatePromptsApi(
  taskId: string,
  stylePreset: string = "standard",
  sceneThreshold: number = 0.35
): Promise<any> {
  const normalizedStyle = normalizeStylePreset(stylePreset);
  const payload = {
    video_id: taskId,
    task_id: taskId,
    style: normalizedStyle,
    style_preset: normalizedStyle,
    scene_threshold: sceneThreshold,
  };
  console.log("[PIPELINE] generation:start request:", payload);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 90000); // 90s generation timeout

  try {
    const res = await fetch(`${API_BASE_URL}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ message: "Generation failed" }));
      console.error("[PIPELINE] generation:failed errorData:", errorData);
      throw new Error(errorData.message || errorData.detail || "Prompt generation failed on backend.");
    }
    const data = await res.json();
    console.log("[PIPELINE] generation:complete response:", data);
    return data;
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") {
      console.error("[PIPELINE] generation:timeout (>90s)");
      throw new Error("AI Vision generation timed out after 90 seconds. Click 'Retry Generation' to retry using existing extracted frames.");
    }
    throw err;
  }
}

export async function getTaskStatusApi(taskId: string): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/generate/${taskId}`);
  if (!res.ok) {
    throw new Error("Task status check failed");
  }
  return res.json();
}

export async function getHistoryApi(page = 1, limit = 20, style?: string): Promise<any> {
  let url = `${API_BASE_URL}/history?page=${page}&limit=${limit}`;
  if (style) url += `&style=${encodeURIComponent(style)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch generation history");
  return res.json();
}

export async function deleteHistoryItemApi(taskId: string): Promise<boolean> {
  const res = await fetch(`${API_BASE_URL}/history/${taskId}`, { method: "DELETE" });
  return res.ok;
}

export function getDownloadExportUrl(taskId: string, format: string = "txt"): string {
  return `${API_BASE_URL}/download/${taskId}?format=${format}`;
}

export const uploadVideo = uploadVideoApi;
export const generatePrompts = generatePromptsApi;
