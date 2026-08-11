import { useState } from "react";
import { uploadVideoApi } from "@/lib/api";
import { UploadResponse } from "@/types/api";

export function useUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedData, setUploadedData] = useState<UploadResponse | null>(null);

  const uploadFile = async (file: File) => {
    setIsUploading(true);
    setError(null);
    try {
      const data = await uploadVideoApi(file);
      setUploadedData(data);
      return data;
    } catch (err: any) {
      setError(err.message || "Failed to upload video");
      throw err;
    } finally {
      setIsUploading(false);
    }
  };

  return { isUploading, error, uploadedData, uploadFile, setUploadedData };
}
