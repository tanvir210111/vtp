import { VideoTaskState } from "./video";

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface UploadResponse {
  task_id: string;
  filename: string;
  file_size_bytes: number;
  status: string;
  created_at: string;
}

export interface HistoryListResponse {
  total: number;
  page: number;
  limit: number;
  items: Array<{
    task_id: string;
    filename: string;
    style_preset: string;
    created_at: string;
    duration_seconds: number;
    poster_url: string;
    prompt_preview: string;
  }>;
}
