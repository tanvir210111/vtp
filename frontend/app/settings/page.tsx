"use client";

import { useState } from "react";
import { Sliders, Check, Server, Eye } from "lucide-react";

export default function SettingsPage() {
  const [saved, setSaved] = useState(false);
  const [apiUrl, setApiUrl] = useState("http://localhost:8000/api");
  const [defaultStyle, setDefaultStyle] = useState("standard");
  const [sceneThreshold, setSceneThreshold] = useState("0.35");
  const [enableQwen, setEnableQwen] = useState(true);

  const handleSave = (e: any) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">Application Settings</h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium">Configure backend endpoints, vision engine sensitivity, and AI model defaults.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* API Settings */}
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-6 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Server className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            <span>Backend Server Connectivity</span>
          </h3>

          <div>
            <label className="block text-xs font-bold text-slate-900 dark:text-white mb-1.5">FastAPI Base URL</label>
            <input
              type="text"
              value={apiUrl}
              onChange={(e: any) => setApiUrl(e.target.value)}
              className="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 px-4 py-2.5 text-sm font-mono text-slate-900 dark:text-white focus:border-blue-600 focus:outline-none transition-colors"
            />
          </div>
        </div>

        {/* Vision Pipeline Settings */}
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-6 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Eye className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
            <span>AI Pipeline Parameters</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-900 dark:text-white mb-1.5">Default Prompt Style</label>
              <select
                value={defaultStyle}
                onChange={(e: any) => setDefaultStyle(e.target.value)}
                className="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 px-4 py-2.5 text-sm text-slate-900 dark:text-white focus:border-blue-600 focus:outline-none transition-colors font-medium"
              >
                <option value="standard">Standard (Timeline-based)</option>
                <option value="creative">Creative (Cinematic Breakdown)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-900 dark:text-white mb-1.5">Scene Detection Sensitivity (SSIM)</label>
              <input
                type="number"
                step="0.05"
                min="0.1"
                max="0.9"
                value={sceneThreshold}
                onChange={(e: any) => setSceneThreshold(e.target.value)}
                className="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 px-4 py-2.5 text-sm font-mono text-slate-900 dark:text-white focus:border-blue-600 focus:outline-none transition-colors"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <div>
              <p className="text-sm font-bold text-slate-900 dark:text-white">Deep Qwen2-VL Analysis</p>
              <p className="text-xs text-slate-600 dark:text-slate-400 font-medium">Perform deep multimodal visual captioning on extracted frame sequences.</p>
            </div>
            <input
              type="checkbox"
              checked={enableQwen}
              onChange={(e: any) => setEnableQwen(e.target.checked)}
              className="h-5 w-5 rounded border-slate-200 dark:border-slate-800 text-blue-600 focus:ring-blue-600"
            />
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center justify-end">
          <button
            type="submit"
            className="inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-700 px-6 py-3 text-sm font-bold text-white shadow-md transition-all"
          >
            {saved ? (
              <>
                <Check className="h-4 w-4" />
                <span>Settings Saved!</span>
              </>
            ) : (
              <>
                <Sliders className="h-4 w-4" />
                <span>Save Configuration</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
