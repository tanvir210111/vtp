"use client";

import { useState, useRef, ChangeEvent, DragEvent } from "react";
import { UploadCloud, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import { formatBytes } from "@/lib/utils";

interface UploadBoxProps {
  onFileSelect: (file: File) => void;
  isUploading?: boolean;
  selectedFile?: File | null;
  error?: string | null;
}

export default function UploadBox({
  onFileSelect,
  isUploading = false,
  selectedFile = null,
  error = null,
}: UploadBoxProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndProcessFile = (file: File) => {
    setValidationError(null);
    const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    
    if (![".mp4", ".mov", ".webm"].includes(ext)) {
      setValidationError("Unsupported video format. Please upload MP4, MOV, or WEBM.");
      return;
    }

    // Check duration limit (15 seconds max)
    const video = document.createElement("video");
    video.preload = "metadata";
    video.onloadedmetadata = () => {
      window.URL.revokeObjectURL(video.src);
      if (video.duration > 15.5) {
        setValidationError(`Video duration (${Math.round(video.duration)}s) exceeds the maximum limit of 15 seconds.`);
      } else {
        onFileSelect(file);
      }
    };
    video.onerror = () => {
      onFileSelect(file);
    };
    video.src = URL.createObjectURL(file);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndProcessFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndProcessFile(e.target.files[0]);
    }
  };

  const displayError = validationError || error;

  return (
    <div className="w-full">
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-300 ${
          isDragOver
            ? "border-blue-600 bg-blue-600/10 dark:bg-blue-600/20 shadow-md scale-[1.01]"
            : selectedFile
            ? "border-emerald-500 bg-emerald-500/5 dark:bg-emerald-500/10"
            : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 hover:border-blue-500 hover:bg-white dark:hover:bg-slate-900 shadow-xs"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="video/mp4,video/quicktime,video/webm"
          className="hidden"
          onChange={handleFileChange}
        />

        {isUploading ? (
          <div className="flex flex-col items-center py-6">
            <Loader2 className="h-12 w-12 text-blue-600 dark:text-blue-400 animate-spin mb-4" />
            <p className="text-base font-bold text-slate-900 dark:text-white">Uploading video file...</p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium">Ingesting video stream metadata</p>
          </div>
        ) : selectedFile ? (
          <div className="flex flex-col items-center py-4">
            <div className="h-14 w-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-600 dark:text-emerald-400 mb-3 shadow-xs">
              <CheckCircle2 className="h-8 w-8" />
            </div>
            <p className="text-base font-bold text-slate-900 dark:text-white max-w-md truncate">{selectedFile.name}</p>
            <p className="text-xs font-mono font-semibold text-emerald-600 dark:text-emerald-400 mt-1">
              Ready for processing ({formatBytes(selectedFile.size)})
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-3 underline hover:text-slate-900 dark:hover:text-white">Click or drag to replace video</p>
          </div>
        ) : (
          <div className="flex flex-col items-center py-6">
            <div className="h-16 w-16 rounded-2xl bg-blue-600/10 border border-blue-600/20 flex items-center justify-center text-blue-600 dark:text-blue-400 mb-4 shadow-xs">
              <UploadCloud className="h-8 w-8 text-cyan-600 dark:text-cyan-400" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">Drag and drop your video file</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm">
              Supported Formats: <strong className="text-slate-900 dark:text-slate-200">MP4, MOV, WEBM</strong>
            </p>
            <div className="mt-2.5 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-[11px] font-semibold text-amber-600 dark:text-amber-400 shadow-xs">
              ⚡ Max Duration: 15 Seconds
            </div>
            <button
              type="button"
              className="mt-6 rounded-xl bg-blue-600 hover:bg-blue-700 px-6 py-2.5 text-xs font-bold text-white shadow-md transition-all"
            >
              Browse Files
            </button>
          </div>
        )}
      </div>

      {displayError && (
        <div className="mt-4 flex items-center gap-2 rounded-xl bg-red-500/10 border border-red-500/20 p-4 text-xs text-red-600 dark:text-red-400 font-semibold">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <span>{displayError}</span>
        </div>
      )}
    </div>
  );
}
