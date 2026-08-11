"use client";

import { useState } from "react";
import CopyButton from "./CopyButton";
import { Sparkles, Eye, Camera, Lightbulb, Palette, Activity } from "lucide-react";

interface PromptCardProps {
  prompts: Record<string, string>;
  analysis?: any;
  taskId: string;
}

export default function PromptCard({ prompts, analysis, taskId }: PromptCardProps) {
  const [activeTab, setActiveTab] = useState<string>("veo");

  const tabs = [
    { id: "veo", label: "Google Veo" },
    { id: "sora", label: "OpenAI Sora" },
    { id: "standard", label: "Standard (Timeline)" },
    { id: "creative", label: "Creative (Cinematic)" },
    { id: "midjourney", label: "Midjourney v6" },
    { id: "flux", label: "Flux.1" },
  ];

  const currentPrompt = prompts[activeTab] || prompts["veo"] || prompts["standard"] || "";

  // Safe String Helper Formatters for Vision Breakdown
  const getLightingText = () => {
    if (!analysis?.lighting) return "Volumetric rim lighting";
    if (typeof analysis.lighting === "string") return analysis.lighting;
    return analysis.lighting.description || `${analysis.lighting.brightness || "Bright"} ${analysis.lighting.temperature || "Warm"} lighting`;
  };

  const getCameraText = () => {
    if (!analysis?.camera) return "Medium Tracking Shot";
    if (typeof analysis.camera === "string") return analysis.camera;
    return `${analysis.camera.framing || "Medium Shot"}, ${analysis.camera.movement || "Tracking shot"}`;
  };

  const getLensText = () => {
    if (!analysis?.camera) return "35mm prime lens";
    if (typeof analysis.camera === "string") return "35mm prime lens";
    return analysis.camera.lens || "35mm prime lens";
  };

  const getColorText = () => {
    if (!analysis?.colors) return "Cinematic Grade";
    if (typeof analysis.colors === "string") return analysis.colors;
    return analysis.colors.name || "Cinematic Grade";
  };

  const getSubjectActionText = () => {
    const peopleArr = analysis?.people;
    const peopleStr = Array.isArray(peopleArr) && peopleArr.length > 0
      ? `${peopleArr[0].count} Subject (${peopleArr[0].age_group || "Young Adult"})`
      : "";
    const objectsStr = Array.isArray(analysis?.objects) ? analysis.objects.join(", ") : (analysis?.subject || "Subject & Objects");
    const actionsStr = Array.isArray(analysis?.actions) ? analysis.actions.join(", ") : (analysis?.action || "Kinetic motion");
    
    return {
      subject: peopleStr ? `${peopleStr} interacting with ${objectsStr}` : objectsStr,
      action: actionsStr
    };
  };

  const { subject, action } = getSubjectActionText();

  return (
    <div className="w-full space-y-6">
      {/* Extracted Vision Breakdown */}
      {analysis && (
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-6 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <Eye className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
            <span>Vision Engine Analysis</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 p-3 shadow-xs">
              <span className="text-slate-600 dark:text-slate-400 font-semibold flex items-center gap-1.5 mb-1">
                <Camera className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" /> Camera & Motion
              </span>
              <p className="text-slate-900 dark:text-white font-bold">{getCameraText()}</p>
              <p className="text-slate-500 dark:text-slate-400 mt-1 font-mono">{getLensText()}</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 p-3 shadow-xs">
              <span className="text-slate-600 dark:text-slate-400 font-semibold flex items-center gap-1.5 mb-1">
                <Lightbulb className="h-3.5 w-3.5 text-amber-500" /> Lighting
              </span>
              <p className="text-slate-900 dark:text-white font-bold">{getLightingText()}</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 p-3 shadow-xs">
              <span className="text-slate-600 dark:text-slate-400 font-semibold flex items-center gap-1.5 mb-1">
                <Palette className="h-3.5 w-3.5 text-purple-600 dark:text-purple-400" /> Color Grade
              </span>
              <p className="text-slate-900 dark:text-white font-bold">{getColorText()}</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 p-3 md:col-span-2 lg:col-span-3 shadow-xs">
              <span className="text-slate-600 dark:text-slate-400 font-semibold flex items-center gap-1.5 mb-1">
                <Activity className="h-3.5 w-3.5 text-emerald-500" /> Subject & Kinetic Actions
              </span>
              <p className="text-slate-900 dark:text-white font-bold">{subject}</p>
              <p className="text-slate-600 dark:text-slate-300 mt-1 font-medium">{action}</p>
            </div>
          </div>
        </div>
      )}

      {/* Output Tabs & Content */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-6 shadow-lg dark:shadow-2xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-cyan-600 dark:text-cyan-400 animate-pulse" />
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Generated Prompt Result</h3>
          </div>

          <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-950 p-1 rounded-xl border border-slate-200 dark:border-slate-800 overflow-x-auto max-w-full">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all whitespace-nowrap ${
                  activeTab === tab.id
                    ? "bg-blue-600 text-white shadow-sm"
                    : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Prompt Text Block */}
        <div className="relative rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/90 p-5 font-mono text-sm leading-relaxed text-slate-900 dark:text-slate-100 shadow-inner">
          <pre className="whitespace-pre-wrap font-sans text-sm selection:bg-blue-500/20 leading-relaxed font-medium">
            {currentPrompt}
          </pre>
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-200 dark:border-slate-800">
          <div className="flex flex-wrap items-center gap-2">
            <CopyButton text={currentPrompt} />

            <a
              href={taskId ? `/api/download/${taskId}?format=txt` : "#"}
              download
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-800 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-xs"
            >
              <span>Download TXT</span>
            </a>

            <a
              href={taskId ? `/api/download/${taskId}?format=json` : "#"}
              download
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-800 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-xs"
            >
              <span>Download JSON</span>
            </a>

            <a
              href={taskId ? `/api/download/${taskId}?format=markdown` : "#"}
              download
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-800 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-xs"
            >
              <span>Download Markdown</span>
            </a>
          </div>

          <a
            href="/upload"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-xs font-bold text-white shadow-md transition-all"
          >
            <Sparkles className="h-4 w-4" />
            <span>Generate Again</span>
          </a>
        </div>
      </div>
    </div>
  );
}
