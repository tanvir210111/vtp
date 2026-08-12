import { useState } from "react";
import { generatePromptsApi } from "@/lib/api";
import { VideoTaskState } from "@/types/video";

export function useGenerate() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<VideoTaskState | null>(null);

  const generate = async (taskId: string, stylePreset: string = "standard") => {
    setIsGenerating(true);
    setError(null);
    try {
      const data = await generatePromptsApi(taskId, stylePreset);
      setResult(data);
      return data;
    } catch (err: any) {
      setError(err.message || "Failed to generate AI prompts");
      throw err;
    } finally {
      setIsGenerating(false);
    }
  };

  return { isGenerating, error, result, generate };
}
