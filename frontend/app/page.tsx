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
  const [stepState, setStepState] = useState<
    | "idle"
    | "uploading"
    | "extracting"
    | "analyzing"
    | "generating"
    | "completed"
    | "failed"
  >("idle");
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

    let extractTimer: NodeJS.Timeout | null = null;
    let generateTimer: NodeJS.Timeout | null = null;

    try {
      setIsProcessing(true);
      setError(null);
      
      console.log("[PIPELINE] upload:start");
      setStepState("uploading");

      // Step 1: Upload video file
      const uploadRes = await uploadVideo(selectedFile);
      console.log("[PIPELINE] upload:complete", uploadRes);
      const newTaskId = uploadRes.video_id || uploadRes.task_id || uploadRes.id;
      if (!newTaskId) {
        throw new Error(uploadRes.message || "Failed to retrieve upload task ID.");
      }
      console.log("[PIPELINE] task_id:", newTaskId);
      setTaskId(newTaskId);

      // Step 2 & 3: Frame extraction & visual analysis
      console.log("[PIPELINE] extraction:start");
      setStepState("extracting");

      // Progressively update step state as backend processes video
      extractTimer = setTimeout(() => {
        console.log("[PIPELINE] analysis:start");
        setStepState("analyzing");
      }, 2000);

      generateTimer = setTimeout(() => {
        console.log("[PIPELINE] generation:start");
        setStepState("generating");
      }, 5000);

      // Step 4: Run AI Pipeline Prompt Synthesis on Backend
      console.log("[PIPELINE] generate request", { task_id: newTaskId, style: selectedStyle });
      const processRes = await generatePrompts(newTaskId, selectedStyle);
      
      if (extractTimer) clearTimeout(extractTimer);
      if (generateTimer) clearTimeout(generateTimer);

      console.log("[PIPELINE] generate response:", processRes);

      // Validate response
      if (!processRes || processRes.success !== true) {
        throw new Error(processRes?.message || "Generation failed on backend.");
      }
      if (processRes.status !== "completed") {
        throw new Error(processRes.message || `Generation did not complete (status=${processRes.status})`);
      }
      const prompts = processRes.prompts || {};
      const promptKeys = Object.keys(prompts || {});
      console.log("[PIPELINE] prompts keys:", promptKeys);

      const hasStandard = Array.isArray(prompts.standard) ? prompts.standard.length > 0 : !!prompts.standard;
      const hasCreative = Array.isArray(prompts.creative) ? prompts.creative.length > 0 : !!prompts.creative;
      if (!hasStandard && !hasCreative) {
        throw new Error("AI pipeline completed but returned no prompts.");
      }

      setStepState("completed");
      console.log("[PIPELINE] completed successfully");
      setResult(processRes);
    } catch (err: any) {
      if (extractTimer) clearTimeout(extractTimer);
      if (generateTimer) clearTimeout(generateTimer);
      
      console.error("[PIPELINE] execution error:", err);
      setStepState("failed");
      setError(err?.message || "Failed to process video frame extraction. Please check backend connectivity or try another clip.");
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

        {!result && !isProcessing && !error && (
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
            <Loading currentState={stepState} />
          </div>
        )}

        {/* Error Notification Banner */}
        {error && !isProcessing && (
          <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-6 shadow-lg backdrop-blur-xl space-y-4 text-left">
            <div className="flex items-start gap-3">
              <div className="h-10 w-10 rounded-xl bg-red-500/20 border border-red-500/40 flex items-center justify-center text-red-500 font-bold text-xl shrink-0">
                ⚠️
              </div>
              <div className="space-y-1">
                <h4 className="text-base font-bold text-red-600 dark:text-red-400">Pipeline Execution Error</h4>
                <p className="text-xs text-red-800 dark:text-red-300 font-medium leading-relaxed">{error}</p>
              </div>
            </div>
            <div className="pt-2 flex items-center gap-3">
              <button
                onClick={() => handleGenerate()}
                className="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl shadow-md transition-all cursor-pointer"
              >
                Retry Generation
              </button>
              <button
                onClick={handleClearFile}
                className="px-5 py-2.5 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-xs rounded-xl transition-all cursor-pointer"
              >
                Choose Another Video
              </button>
            </div>
          </div>
        )}

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
