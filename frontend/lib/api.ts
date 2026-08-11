import { API_BASE_URL } from "./constants";

export async function uploadVideoApi(file: File): Promise<any> {
  const formData = new FormData();
  formData.append("video", file);
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ message: "Upload failed" }));
    throw new Error(errorData.message || errorData.detail || "Upload failed");
  }

  return res.json();
}

export async function generatePromptsApi(
  taskId: string,
  stylePreset: string = "standard",
  sceneThreshold: number = 0.35
): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      video_id: taskId,
      task_id: taskId,
      style: stylePreset,
      style_preset: stylePreset,
      scene_threshold: sceneThreshold,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ message: "Generation failed" }));
    throw new Error(errorData.message || errorData.detail || "Prompt generation failed");
  }

  return res.json();
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
