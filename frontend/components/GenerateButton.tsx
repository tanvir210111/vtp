"use client";

import { Sparkles, Loader2, ArrowRight } from "lucide-react";

interface GenerateButtonProps {
  onClick: () => void;
  disabled?: boolean;
  isGenerating?: boolean;
}

export default function GenerateButton({
  onClick,
  disabled = false,
  isGenerating = false,
}: GenerateButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || isGenerating}
      className={`w-full relative flex items-center justify-center gap-3 rounded-xl px-8 py-4 text-base font-bold text-white transition-all duration-200 shadow-lg ${
        disabled
          ? "bg-[#CBD5E1] text-[#94A3B8] cursor-not-allowed shadow-none"
          : "bg-[#2563EB] hover:bg-[#1D4ED8] shadow-[#2563EB]/25 hover:scale-[1.01] active:scale-[0.99]"
      }`}
    >
      {isGenerating ? (
        <>
          <Loader2 className="h-5 w-5 animate-spin" />
          <span>Generating Prompt...</span>
        </>
      ) : (
        <>
          <Sparkles className="h-5 w-5" />
          <span>Generate Prompt</span>
          <ArrowRight className="h-5 w-5" />
        </>
      )}
    </button>
  );
}
