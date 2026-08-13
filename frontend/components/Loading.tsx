"use client";

import { Upload, Layers, Eye, Sparkles, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface LoadingProps {
  currentState?:
    | "idle"
    | "uploading"
    | "uploaded"
    | "extracting"
    | "extracted"
    | "analyzing"
    | "generating"
    | "completed"
    | "failed";
}

export default function Loading({ currentState = "uploading" }: LoadingProps) {
  const steps = [
    { id: 1, label: "Uploading...", icon: Upload },
    { id: 2, label: "Extracting Frames...", icon: Layers },
    { id: 3, label: "Analyzing Video...", icon: Eye },
    { id: 4, label: "Generating Prompt...", icon: Sparkles },
    { id: 5, label: "Done", icon: CheckCircle2 },
  ];

  const getStepNumber = (state: string): number => {
    switch (state) {
      case "uploading":
        return 1;
      case "uploaded":
      case "extracting":
        return 2;
      case "extracted":
      case "analyzing":
        return 3;
      case "generating":
        return 4;
      case "completed":
        return 5;
      case "failed":
        return 1;
      default:
        return 1;
    }
  };

  const currentStep = getStepNumber(currentState);

  return (
    <div className="flex flex-col items-center justify-center p-8 sm:p-12 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-lg dark:shadow-2xl backdrop-blur-xl">
      <div className="relative mb-6">
        <div className="h-16 w-16 rounded-full border-4 border-blue-600/20 border-t-blue-600 animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center text-cyan-600 dark:text-cyan-400">
          <Sparkles className="h-6 w-6 animate-pulse" />
        </div>
      </div>

      <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Processing Video AI Pipeline</h3>
      <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-md text-center mb-8 font-medium">
        Extracting scene keyframes, analyzing camera motion, lighting tones, and generating ready-to-use prompts...
      </p>

      {/* 5-Step Stepper */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-2.5 w-full max-w-2xl">
        {steps.map((step) => {
          const StepIcon = step.icon;
          const isDone = currentStep > step.id;
          const isCurrent = currentStep === step.id;

          return (
            <div
              key={step.id}
              className={cn(
                "flex items-center gap-2 p-2.5 rounded-lg border text-xs font-bold transition-all shadow-xs",
                isDone && "bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400",
                isCurrent && "bg-blue-600/10 border-blue-600 text-blue-600 dark:text-blue-400 shadow-md animate-pulse",
                !isDone && !isCurrent && "bg-slate-50 dark:bg-slate-950/40 border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500"
              )}
            >
              <StepIcon className="h-4 w-4 shrink-0" />
              <span className="truncate">{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
