"use client";

import { STYLE_PRESETS } from "@/lib/constants";
import { StylePresetId } from "@/types/prompt";
import { Film, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface PromptStyleProps {
  selectedStyle: StylePresetId;
  onStyleSelect: (id: StylePresetId) => void;
}

const iconMap = {
  Film,
  Sparkles
};

export default function PromptStyle({ selectedStyle, onStyleSelect }: PromptStyleProps) {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white">Select Prompt Generation Style</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">Choose between timeline-based structured output or rich cinematic breakdown</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {STYLE_PRESETS.map((preset) => {
          const Icon = iconMap[preset.iconName as keyof typeof iconMap] || Film;
          const isSelected = selectedStyle === preset.id;

          return (
            <div
              key={preset.id}
              onClick={() => onStyleSelect(preset.id)}
              className={cn(
                "relative flex flex-col justify-between rounded-xl border p-5 cursor-pointer transition-all duration-200 shadow-xs",
                isSelected
                  ? "border-blue-600 bg-blue-600/5 dark:bg-blue-600/10 ring-2 ring-blue-600/20 shadow-md"
                  : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-slate-300 dark:hover:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-900"
              )}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div
                    className={cn(
                      "h-10 w-10 rounded-xl flex items-center justify-center transition-colors shadow-xs",
                      isSelected ? "bg-blue-600 text-white" : "bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400"
                    )}
                  >
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className={cn(
                    "text-[11px] font-bold tracking-wide uppercase px-2.5 py-0.5 rounded-full border shadow-2xs",
                    isSelected
                      ? "bg-blue-600/10 border-blue-600/30 text-blue-600 dark:text-blue-400"
                      : "bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400"
                  )}>
                    {preset.badge}
                  </span>
                </div>
                <h4 className="text-base font-bold text-slate-900 dark:text-white mb-1.5">{preset.title}</h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{preset.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
