"use client";

import { useState } from "react";
import Hero from "@/components/Hero";
import UploadBox from "@/components/UploadBox";
import VideoPreview from "@/components/VideoPreview";
import PromptStyle from "@/components/PromptStyle";
import GenerateButton from "@/components/GenerateButton";
import Loading from "@/components/Loading";
import PromptCard from "@/components/PromptCard";
import FeaturesSection from "@/components/FeaturesSection";
import FaqSection from "@/components/FaqSection";
import { uploadVideo, generatePrompts } from "@/lib/api";
import { StylePresetId } from "@/types/prompt";

export default function HomePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<StylePresetId>("standard");
  const [taskId, setTaskId] = useState<string | null>(null);
  const [stepStatus, setStepStatus] = useState<number>(1);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError(null);
    setResult(null);
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setTaskId(null);
    setResult(null);
    setError(null);
  };

  const handleGenerate = async () => {
    if (!selectedFile) return;

    try {
      setIsProcessing(true);
      setError(null);
      setStepStatus(1);

      // Step 1: Upload video file
      const uploadRes = await uploadVideo(selectedFile);
      const newTaskId = uploadRes.video_id || uploadRes.task_id || uploadRes.id;
      if (!newTaskId) {
        throw new Error(uploadRes.message || "Failed to retrieve upload task ID.");
      }
      setTaskId(newTaskId);

      // Step 2 & 3: Frame extraction & visual analysis
      setStepStatus(2);
      await new Promise((resolve) => setTimeout(resolve, 400));
      
      setStepStatus(3);
      await new Promise((resolve) => setTimeout(resolve, 400));

      // Step 4: Run AI Pipeline Prompt Synthesis
      setStepStatus(4);
      const processRes = await generatePrompts(newTaskId, selectedStyle);
      
      setStepStatus(5);
      setResult(processRes);
    } catch (err: any) {
      console.error("Generation Error:", err);
      setError(err?.message || "Failed to process video. Please check backend connectivity.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-12">
      {/* 1 & 2. Hero Section */}
      <Hero />

      {/* 3, 4, 5, 6, 7. Main Interactive Workspace Section */}
      <section id="upload-section" className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 space-y-8 scroll-mt-20">
        <div className="text-center">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            Upload & Generate Prompt
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium">
            Select your video, pick a prompt style, and let AI synthesize visual prompts.
          </p>
        </div>

        {!result && !isProcessing && (
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-6 sm:p-8 shadow-lg dark:shadow-2xl backdrop-blur-xl space-y-8">
            {/* Upload Area & Preview */}
            <div className="space-y-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                1. Upload Video (Max 15 Sec)
              </h3>
              {selectedFile ? (
                <VideoPreview file={selectedFile} onClear={handleClearFile} />
              ) : (
                <UploadBox onFileSelect={handleFileSelect} error={error} />
              )}
            </div>

            {/* Prompt Style Cards */}
            <div className="space-y-4 pt-4 border-t border-slate-200 dark:border-slate-800">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                2. Select Prompt Style
              </h3>
              <PromptStyle selectedStyle={selectedStyle} onStyleSelect={setSelectedStyle} />
            </div>

            {/* Generate Button */}
            <div className="pt-4 border-t border-slate-200 dark:border-slate-800">
              <GenerateButton
                onClick={handleGenerate}
                disabled={!selectedFile}
                isGenerating={isProcessing}
              />
            </div>
          </div>
        )}

        {/* Loading / Stepper Screen */}
        {isProcessing && (
          <div className="my-8">
            <Loading currentStep={stepStatus} />
          </div>
        )}

        {/* Result Section */}
        {result && !isProcessing && (
          <div className="space-y-6">
            <PromptCard
              prompts={result.prompts || {}}
              analysis={result.analysis}
              taskId={taskId || ""}
            />
          </div>
        )}
      </section>

      {/* 8. Features Section */}
      <FeaturesSection />

      {/* 9. FAQ Section */}
      <FaqSection />
    </div>
  );
}
