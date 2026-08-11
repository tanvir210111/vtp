"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import UploadBox from "@/components/UploadBox";
import VideoPreview from "@/components/VideoPreview";
import PromptStyle from "@/components/PromptStyle";
import GenerateButton from "@/components/GenerateButton";
import Loading from "@/components/Loading";
import { useUpload } from "@/hooks/useUpload";
import { useGenerate } from "@/hooks/useGenerate";
import { StylePresetId } from "@/types/prompt";

export default function UploadPage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<StylePresetId>("cinematic");
  
  const { isUploading, error: uploadError, uploadFile } = useUpload();
  const { isGenerating, error: genError, generate } = useGenerate();

  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);
    try {
      await uploadFile(file);
    } catch (e) {
      console.error("Upload error", e);
    }
  };

  const handleStartGeneration = async () => {
    if (!selectedFile) return;
    try {
      const uploadRes = await uploadFile(selectedFile);
      const genRes = await generate(uploadRes.task_id, selectedStyle);
      
      // Navigate to results page with taskId query parameter
      router.push(`/result?taskId=${genRes.task_id}`);
    } catch (e) {
      console.error("Generation pipeline failed", e);
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white">Upload & Analyze Video</h1>
        <p className="text-sm text-gray-400 mt-1">Select your video clip and visual style preset to begin prompt synthesis.</p>
      </div>

      {(isUploading || isGenerating) ? (
        <Loading />
      ) : (
        <div className="space-y-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <UploadBox
                onFileSelect={handleFileSelect}
                isUploading={isUploading}
                selectedFile={selectedFile}
                error={uploadError || genError}
              />
            </div>
            <div>
              <VideoPreview file={selectedFile} />
            </div>
          </div>

          <div className="rounded-2xl border border-surface-border bg-surface/40 p-6 backdrop-blur-md">
            <PromptStyle
              selectedStyle={selectedStyle}
              onStyleSelect={(id) => setSelectedStyle(id)}
            />
          </div>

          <div className="pt-2">
            <GenerateButton
              onClick={handleStartGeneration}
              disabled={!selectedFile || isUploading}
              isGenerating={isGenerating}
            />
          </div>
        </div>
      )}
    </div>
  );
}
